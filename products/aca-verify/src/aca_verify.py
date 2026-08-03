#!/usr/bin/env python3
"""Deterministic interpreter for declared ACA Decision Proof Record predicates."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
DEFAULT_PROFILE = PRODUCT / "profiles" / "aca-dpr-baseline-v0.1.json"

VALID_STATES = {"ALLOW", "DENY", "HOLD", "CONFLICT", "REVOKED", "ESCALATE"}
VALID_VALUES = {"TRUE", "FALSE", "UNKNOWN", "CONFLICTED", "EXPIRED", "REVOKED"}
FAIL_VALUES = {"FALSE", "CONFLICTED", "EXPIRED", "REVOKED"}
VALID_REMEDY_STATES = {"NONE", "AVAILABLE", "ACTIVE", "COMPLETED", "FAILED"}
CANONICAL_REQUIREMENTS = {"ACA-120", "ACA-130", "ACA-140", "ACA-150"}
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


class InvalidInput(ValueError):
    """The record or profile cannot be deterministically interpreted."""


def require_nonempty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidInput(f"{field} must be a non-empty string")
    return value


def load_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InvalidInput(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidInput(f"{path}: expected a JSON object")
    return value


def validate_datetime(value: object, field: str) -> None:
    text = require_nonempty_string(value, field)
    if not RFC3339_RE.fullmatch(text):
        raise InvalidInput(f"{field} must be an RFC 3339 date-time with a UTC offset")
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidInput(f"{field} must be an RFC 3339 date-time with a UTC offset") from exc


def validate_record(record: dict) -> None:
    """Validate the complete constraint surface of the public v0.1 DPR schema.

    The checks also add deterministic safety constraints that the current schema
    cannot express, including unique predicate IDs and digest syntax.
    """
    required = {"record_id", "profile_id", "rule_version", "evaluated_at", "state", "predicates", "remedy"}
    missing = sorted(required - set(record))
    if missing:
        raise InvalidInput(f"record missing required fields: {', '.join(missing)}")

    require_nonempty_string(record["record_id"], "record_id")
    require_nonempty_string(record["profile_id"], "profile_id")
    require_nonempty_string(record["rule_version"], "rule_version")
    validate_datetime(record["evaluated_at"], "evaluated_at")
    if record["state"] not in VALID_STATES:
        raise InvalidInput(f"invalid decision state: {record['state']!r}")

    predicates = record["predicates"]
    if not isinstance(predicates, list):
        raise InvalidInput("predicates must be an array")
    seen: set[str] = set()
    for index, item in enumerate(predicates):
        prefix = f"predicates[{index}]"
        if not isinstance(item, dict):
            raise InvalidInput(f"{prefix} must be an object")
        missing_item = sorted({"id", "value", "source"} - set(item))
        if missing_item:
            raise InvalidInput(f"{prefix} missing fields: {', '.join(missing_item)}")
        predicate_id = require_nonempty_string(item["id"], f"{prefix}.id")
        require_nonempty_string(item["source"], f"{prefix}.source")
        if predicate_id in seen:
            raise InvalidInput(f"duplicate predicate: {predicate_id}")
        seen.add(predicate_id)
        if item["value"] not in VALID_VALUES:
            raise InvalidInput(f"invalid value for {predicate_id}: {item['value']!r}")
        digest = item.get("evidence_hash")
        if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
            raise InvalidInput(f"{prefix}.evidence_hash must be sha256 followed by 64 lowercase hexadecimal characters")

    remedy = record["remedy"]
    if not isinstance(remedy, dict):
        raise InvalidInput("remedy must be an object")
    missing_remedy = sorted({"status", "route"} - set(remedy))
    if missing_remedy:
        raise InvalidInput(f"remedy missing fields: {', '.join(missing_remedy)}")
    if remedy["status"] not in VALID_REMEDY_STATES:
        raise InvalidInput(f"invalid remedy status: {remedy['status']!r}")
    if not isinstance(remedy["route"], str):
        raise InvalidInput("remedy.route must be a string")
    deadline = remedy.get("deadline")
    if deadline is not None:
        validate_datetime(deadline, "remedy.deadline")


def validate_profile(profile: dict) -> None:
    if profile.get("schema") != "kapukai.aca-verify-profile.v0.1":
        raise InvalidInput("unsupported profile schema")
    require_nonempty_string(profile.get("profile_id"), "profile.profile_id")
    require_nonempty_string(profile.get("profile_version"), "profile.profile_version")
    if profile.get("claim_scope") != "PARTIAL_PROFILE_CONFORMANCE":
        raise InvalidInput("v0.1 profiles must declare partial conformance")
    rules = profile.get("rules")
    if not isinstance(rules, list) or not rules:
        raise InvalidInput("profile requires at least one rule")
    required = {"predicate_id", "mandatory", "evidence_hash_advisory", "requirement_id", "question", "minimum_repair"}
    seen: set[str] = set()
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict) or not required <= set(rule):
            raise InvalidInput(f"profile rule {index} is incomplete")
        predicate_id = require_nonempty_string(rule["predicate_id"], f"profile.rules[{index}].predicate_id")
        if predicate_id in seen:
            raise InvalidInput(f"duplicate profile predicate: {predicate_id}")
        seen.add(predicate_id)
        if not isinstance(rule["mandatory"], bool) or not isinstance(rule["evidence_hash_advisory"], bool):
            raise InvalidInput(f"profile rule {predicate_id} flags must be booleans")
        if rule["requirement_id"] not in CANONICAL_REQUIREMENTS:
            raise InvalidInput(f"non-canonical requirement: {rule['requirement_id']}")
        require_nonempty_string(rule["question"], f"profile rule {predicate_id} question")
        require_nonempty_string(rule["minimum_repair"], f"profile rule {predicate_id} minimum_repair")


def canonical_hash(value: dict) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def evaluate(record: dict, profile: dict) -> dict:
    validate_record(record)
    validate_profile(profile)
    if record["profile_id"] != profile["profile_id"]:
        raise InvalidInput("record profile_id does not match the selected profile")
    if record["rule_version"] != profile["profile_version"]:
        raise InvalidInput("record rule_version does not match the selected profile version")

    supplied = {item["id"]: item for item in record["predicates"]}
    declared = {rule["predicate_id"] for rule in profile["rules"]}
    findings: list[dict] = []
    has_failure = False
    has_unknown = False
    has_warning = False

    for rule in profile["rules"]:
        item = supplied.get(rule["predicate_id"])
        value = "MISSING" if item is None else item["value"]
        mandatory = rule["mandatory"]
        if mandatory and value in FAIL_VALUES:
            outcome, has_failure = "FAIL", True
        elif mandatory and value in {"MISSING", "UNKNOWN"}:
            outcome, has_unknown = "INDETERMINATE", True
        elif not mandatory and value != "TRUE":
            outcome, has_warning = "WARN", True
        elif rule["evidence_hash_advisory"] and not item.get("evidence_hash"):
            outcome, has_warning = "WARN", True
        else:
            outcome = "PASS"
        findings.append({
            "predicate_id": rule["predicate_id"],
            "value": value,
            "outcome": outcome,
            "mandatory": mandatory,
            "requirement_id": rule["requirement_id"],
            "question": rule["question"],
            "minimum_repair": None if outcome == "PASS" else rule["minimum_repair"],
        })

    unevaluated = sorted(set(supplied) - declared)
    if unevaluated:
        has_warning = True
        for predicate_id in unevaluated:
            findings.append({
                "predicate_id": predicate_id,
                "value": supplied[predicate_id]["value"],
                "outcome": "WARN",
                "mandatory": False,
                "requirement_id": "ACA-140",
                "question": "Is this supplied predicate governed by the selected profile?",
                "minimum_repair": "Remove the predicate or select a profile that explicitly evaluates it.",
            })

    remedy = record["remedy"]
    if not remedy["route"].strip():
        has_failure = True
        findings.append({
            "predicate_id": "remedy.route",
            "value": "MISSING",
            "outcome": "FAIL",
            "mandatory": True,
            "requirement_id": "ACA-150",
            "question": "Is an operational remedy route recorded?",
            "minimum_repair": "Record an accessible remedy route and responsible actor.",
        })

    findings.sort(key=lambda item: (item["requirement_id"], item["predicate_id"]))
    if has_failure:
        conformance, reliance = "FAIL", "ACTION_BLOCKED"
    elif has_unknown:
        conformance, reliance = "INDETERMINATE", "HUMAN_REVIEW_REQUIRED"
    elif has_warning:
        conformance, reliance = "WARN", "HUMAN_REVIEW_REQUIRED"
    else:
        conformance, reliance = "PASS", "NOT_ESTABLISHED"

    affected = sorted({f["requirement_id"] for f in findings if f["outcome"] != "PASS"})
    return {
        "schema": "kapukai.aca-verification-result.v0.1",
        "verifier_version": "0.1.1-candidate",
        "claim_scope": "PARTIAL_PROFILE_CONFORMANCE",
        "verification_basis": "DECLARED_PREDICATES",
        "evidence_assurance": "DECLARED_DIGESTS_ONLY",
        "profile_id": profile["profile_id"],
        "profile_version": profile["profile_version"],
        "decision_state": record["state"],
        "record_id": record["record_id"],
        "record_hash": canonical_hash(record),
        "conformance": conformance,
        "reliance_status": reliance,
        "affected_requirements": affected,
        "unevaluated_predicates": unevaluated,
        "findings": findings,
        "limitations": [
            "The interpreter evaluates declared predicates; it does not independently establish their factual truth.",
            "Digest syntax is validated, but artifact existence and digest binding are not established by this record.",
            "Conformance is limited to the declared machine-checkable profile.",
            "This result is not a determination of truth, legality, legitimacy, credibility, or authorization.",
            "Human authorization remains separately required for consequential action."
        ]
    }


def render_text(result: dict) -> str:
    lines = [
        f"ACA VERIFY DECLARED-PREDICATE RESULT: {result['conformance']}",
        f"Reliance: {result['reliance_status']}",
        f"Record: {result['record_id']}",
        f"Profile: {result['profile_id']} (partial conformance)",
        "Basis: supplied declarations; facts and artifact bindings not independently established",
        "",
    ]
    marks = {"PASS": "OK", "WARN": "!", "FAIL": "X", "INDETERMINATE": "?"}
    for finding in result["findings"]:
        lines.append(f"[{marks[finding['outcome']]}] {finding['predicate_id']}: {finding['outcome']} ({finding['requirement_id']})")
        if finding["minimum_repair"]:
            lines.append(f"    Repair: {finding['minimum_repair']}")
    lines.extend(["", "Verification is not authorization."])
    return "\n".join(lines)


def render_html(result: dict) -> str:
    rows = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            html.escape(f["predicate_id"]), html.escape(f["outcome"]),
            html.escape(f["requirement_id"]), html.escape(f["minimum_repair"] or "None"))
        for f in result["findings"]
    )
    return ("<!doctype html><meta charset='utf-8'><title>ACA Verify candidate</title>"
            "<style>body{font:16px system-ui;max-width:960px;margin:3rem auto;padding:0 1rem}"
            "table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:.6rem;text-align:left}</style>"
            f"<h1>ACA Verify declared-predicate result: {html.escape(result['conformance'])}</h1>"
            f"<p><strong>Reliance:</strong> {html.escape(result['reliance_status'])}</p>"
            f"<p><strong>Record:</strong> {html.escape(result['record_id'])}</p>"
            "<p><strong>Candidate partial-profile interpretation only.</strong> Supplied facts and artifact bindings are not independently established. Verification is not authorization.</p>"
            f"<table><thead><tr><th>Predicate</th><th>Outcome</th><th>ACA</th><th>Minimum repair</th></tr></thead><tbody>{rows}</tbody></table>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aca-verify")
    parser.add_argument("record", type=Path)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--format", choices=("text", "json", "html"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true", help="return failure for WARN as well as FAIL")
    args = parser.parse_args(argv)
    try:
        result = evaluate(load_object(args.record), load_object(args.profile))
    except InvalidInput as exc:
        print(f"ACA VERIFY INPUT ERROR: {exc}", file=sys.stderr)
        return 3
    rendered = (json.dumps(result, indent=2, sort_keys=True) if args.format == "json"
                else render_html(result) if args.format == "html" else render_text(result))
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if args.strict and result["conformance"] == "WARN":
        return 1
    return {"PASS": 0, "WARN": 0, "FAIL": 1, "INDETERMINATE": 2}[result["conformance"]]


if __name__ == "__main__":
    raise SystemExit(main())
