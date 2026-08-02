#!/usr/bin/env python3
"""Deterministic partial-profile interpreter for ACA Decision Proof Records."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
DEFAULT_PROFILE = PRODUCT / "profiles" / "aca-dpr-baseline-v0.1.json"
ROOT = PRODUCT.parent.parent
VALID_STATES = {"ALLOW", "DENY", "HOLD", "CONFLICT", "REVOKED", "ESCALATE"}
VALID_VALUES = {"TRUE", "FALSE", "UNKNOWN", "CONFLICTED", "EXPIRED", "REVOKED"}
FAIL_VALUES = {"FALSE", "CONFLICTED", "EXPIRED", "REVOKED"}


class InvalidInput(ValueError):
    pass


def load_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InvalidInput(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidInput(f"{path}: expected a JSON object")
    return value


def validate_record(record: dict) -> None:
    required = {"record_id", "profile_id", "rule_version", "evaluated_at", "state", "predicates", "remedy"}
    missing = sorted(required - set(record))
    if missing:
        raise InvalidInput(f"record missing required fields: {', '.join(missing)}")
    if record["state"] not in VALID_STATES:
        raise InvalidInput(f"invalid decision state: {record['state']!r}")
    if not isinstance(record["predicates"], list):
        raise InvalidInput("predicates must be an array")
    seen = set()
    for item in record["predicates"]:
        if not isinstance(item, dict) or not {"id", "value", "source"} <= set(item):
            raise InvalidInput("each predicate requires id, value, and source")
        if item["id"] in seen:
            raise InvalidInput(f"duplicate predicate: {item['id']}")
        seen.add(item["id"])
        if item["value"] not in VALID_VALUES:
            raise InvalidInput(f"invalid value for {item['id']}: {item['value']!r}")
    remedy = record["remedy"]
    if not isinstance(remedy, dict) or not {"status", "route"} <= set(remedy):
        raise InvalidInput("remedy requires status and route")


def validate_profile(profile: dict) -> None:
    if profile.get("schema") != "kapukai.aca-verify-profile.v0.1":
        raise InvalidInput("unsupported profile schema")
    if profile.get("claim_scope") != "PARTIAL_PROFILE_CONFORMANCE":
        raise InvalidInput("v0.1 profiles must declare partial conformance")
    rules = profile.get("rules")
    if not isinstance(rules, list) or not rules:
        raise InvalidInput("profile requires at least one rule")
    required = {"predicate_id", "mandatory", "evidence_hash_advisory", "requirement_id", "question", "minimum_repair"}
    for rule in rules:
        if not isinstance(rule, dict) or not required <= set(rule):
            raise InvalidInput("profile rule is incomplete")
        if rule["requirement_id"] not in {"ACA-120", "ACA-130", "ACA-140", "ACA-150"}:
            raise InvalidInput(f"non-canonical requirement: {rule['requirement_id']}")


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
    findings = []
    has_failure = False
    has_unknown = False
    has_warning = False

    for rule in profile["rules"]:
        item = supplied.get(rule["predicate_id"])
        value = "MISSING" if item is None else item["value"]
        if value in FAIL_VALUES:
            outcome = "FAIL"
            has_failure = True
        elif value in {"MISSING", "UNKNOWN"}:
            outcome = "INDETERMINATE"
            has_unknown = True
        elif rule["evidence_hash_advisory"] and not item.get("evidence_hash"):
            outcome = "WARN"
            has_warning = True
        else:
            outcome = "PASS"
        findings.append({
            "predicate_id": rule["predicate_id"],
            "value": value,
            "outcome": outcome,
            "requirement_id": rule["requirement_id"],
            "question": rule["question"],
            "minimum_repair": None if outcome == "PASS" else rule["minimum_repair"],
        })

    remedy = record["remedy"]
    if not str(remedy.get("route", "")).strip():
        has_failure = True
        findings.append({
            "predicate_id": "remedy.route",
            "value": "MISSING",
            "outcome": "FAIL",
            "requirement_id": "ACA-150",
            "question": "Is an operational remedy route recorded?",
            "minimum_repair": "Record an accessible remedy route and responsible actor.",
        })

    if has_failure:
        conformance, reliance = "FAIL", "ACTION_BLOCKED"
    elif has_unknown:
        conformance, reliance = "INDETERMINATE", "HUMAN_REVIEW_REQUIRED"
    elif has_warning:
        conformance, reliance = "WARN", "HUMAN_REVIEW_REQUIRED"
    else:
        conformance, reliance = "PASS", "NOT_ESTABLISHED"

    failed = sorted({f["requirement_id"] for f in findings if f["outcome"] != "PASS"})
    return {
        "schema": "kapukai.aca-verification-result.v0.1",
        "verifier_version": "0.1.0",
        "claim_scope": "PARTIAL_PROFILE_CONFORMANCE",
        "profile_id": profile["profile_id"],
        "profile_version": profile["profile_version"],
        "decision_state": record["state"],
        "record_id": record["record_id"],
        "record_hash": canonical_hash(record),
        "conformance": conformance,
        "reliance_status": reliance,
        "affected_requirements": failed,
        "findings": findings,
        "limitations": [
            "Conformance is limited to the declared machine-checkable profile.",
            "This result is not a determination of truth, legality, legitimacy, credibility, or authorization.",
            "Human authorization remains separately required for consequential action."
        ]
    }


def render_text(result: dict) -> str:
    lines = [
        f"ACA VERIFY: {result['conformance']}",
        f"Reliance: {result['reliance_status']}",
        f"Record: {result['record_id']}",
        f"Profile: {result['profile_id']} (partial conformance)",
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
    return ("<!doctype html><meta charset='utf-8'><title>ACA Verify</title>"
            "<style>body{font:16px system-ui;max-width:960px;margin:3rem auto;padding:0 1rem}"
            "table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:.6rem;text-align:left}</style>"
            f"<h1>ACA Verify: {html.escape(result['conformance'])}</h1>"
            f"<p><strong>Reliance:</strong> {html.escape(result['reliance_status'])}</p>"
            f"<p><strong>Record:</strong> {html.escape(result['record_id'])}</p>"
            "<p>Partial profile conformance only. Verification is not authorization.</p>"
            f"<table><thead><tr><th>Predicate</th><th>Outcome</th><th>ACA</th><th>Minimum repair</th></tr></thead><tbody>{rows}</tbody></table>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aca-verify")
    parser.add_argument("record", type=Path)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--format", choices=("text", "json", "html"), default="text")
    parser.add_argument("--output", type=Path)
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
    return {"PASS": 0, "WARN": 0, "FAIL": 1, "INDETERMINATE": 2}[result["conformance"]]


if __name__ == "__main__":
    raise SystemExit(main())
