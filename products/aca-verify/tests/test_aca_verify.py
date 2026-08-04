#!/usr/bin/env python3
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aca_verify", ROOT / "src" / "aca_verify.py")
aca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aca)
profile = aca.load_object(ROOT / "profiles" / "aca-dpr-baseline-v0.1.json")


def rejected(record: dict, message: str) -> None:
    try:
        aca.evaluate(record, profile)
        raise AssertionError(f"record unexpectedly accepted: {message}")
    except aca.InvalidInput as exc:
        assert message in str(exc), (message, str(exc))


expected = {
    "passing-decision.json": ("PASS", "NOT_ESTABLISHED"),
    "warning-decision.json": ("WARN", "HUMAN_REVIEW_REQUIRED"),
    "failing-decision.json": ("FAIL", "ACTION_BLOCKED"),
    "indeterminate-decision.json": ("INDETERMINATE", "HUMAN_REVIEW_REQUIRED"),
}
for name, outcome in expected.items():
    record = aca.load_object(ROOT / "examples" / name)
    first = aca.evaluate(record, profile)
    second = aca.evaluate(record, profile)
    assert first == second
    assert (first["conformance"], first["reliance_status"]) == outcome
    assert first["claim_scope"] == "PARTIAL_PROFILE_CONFORMANCE"
    assert first["verification_basis"] == "DECLARED_PREDICATES"
    assert first["evidence_assurance"] == "DECLARED_DIGESTS_ONLY"
    assert any("does not independently establish" in item for item in first["limitations"])

passing = aca.load_object(ROOT / "examples" / "passing-decision.json")

bad_hash = copy.deepcopy(passing)
bad_hash["predicates"][0]["evidence_hash"] = "sha256:placeholder"
rejected(bad_hash, "64 lowercase hexadecimal")

empty_source = copy.deepcopy(passing)
empty_source["predicates"][0]["source"] = ""
rejected(empty_source, "source must be a non-empty string")

bad_date = copy.deepcopy(passing)
bad_date["evaluated_at"] = "yesterday"
rejected(bad_date, "RFC 3339")

date_only = copy.deepcopy(passing)
date_only["evaluated_at"] = "2026-08-02"
rejected(date_only, "UTC offset")

timezone_free = copy.deepcopy(passing)
timezone_free["evaluated_at"] = "2026-08-02T00:00:00"
rejected(timezone_free, "UTC offset")

bad_deadline = copy.deepcopy(passing)
bad_deadline["remedy"]["deadline"] = "next Tuesday"
rejected(bad_deadline, "remedy.deadline")

bad_remedy = copy.deepcopy(passing)
bad_remedy["remedy"]["status"] = "MAYBE"
rejected(bad_remedy, "invalid remedy status")

duplicate_profile = copy.deepcopy(profile)
duplicate_profile["rules"].append(copy.deepcopy(duplicate_profile["rules"][0]))
try:
    aca.evaluate(passing, duplicate_profile)
    raise AssertionError("duplicate profile predicate accepted")
except aca.InvalidInput as exc:
    assert "duplicate profile predicate" in str(exc)

advisory_profile = copy.deepcopy(profile)
advisory_profile["rules"][0]["mandatory"] = False
advisory_record = copy.deepcopy(passing)
advisory_record["predicates"][0]["value"] = "UNKNOWN"
assert aca.evaluate(advisory_record, advisory_profile)["conformance"] == "WARN"

extra_record = copy.deepcopy(passing)
extra_record["predicates"].append({
    "id": "ungoverned.claim",
    "value": "TRUE",
    "source": "synthetic-source",
    "evidence_hash": "sha256:" + "8" * 64,
})
extra_result = aca.evaluate(extra_record, profile)
assert extra_result["conformance"] == "WARN"
assert extra_result["unevaluated_predicates"] == ["ungoverned.claim"]

failing = aca.evaluate(aca.load_object(ROOT / "examples" / "failing-decision.json"), profile)
assert set(failing["affected_requirements"]) == {"ACA-120", "ACA-140", "ACA-150"}
assert all(f["minimum_repair"] for f in failing["findings"] if f["outcome"] != "PASS")

with tempfile.TemporaryDirectory() as directory:
    warning_path = ROOT / "examples" / "warning-decision.json"
    normal = subprocess.run([sys.executable, str(ROOT / "src" / "aca_verify.py"), str(warning_path)], check=False)
    strict = subprocess.run([sys.executable, str(ROOT / "src" / "aca_verify.py"), str(warning_path), "--strict"], check=False)
    assert normal.returncode == 0
    assert strict.returncode == 1

print("PASS: hardened ACA Verify declared-predicate interpretation verified")
