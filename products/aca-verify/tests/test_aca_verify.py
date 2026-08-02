#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aca_verify", ROOT / "src" / "aca_verify.py")
aca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aca)
profile = aca.load_object(ROOT / "profiles" / "aca-dpr-baseline-v0.1.json")

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

failing = aca.evaluate(aca.load_object(ROOT / "examples" / "failing-decision.json"), profile)
assert set(failing["affected_requirements"]) == {"ACA-120", "ACA-140", "ACA-150"}
assert all(f["minimum_repair"] for f in failing["findings"] if f["outcome"] != "PASS")
print("PASS: ACA Verify deterministic conformance outcomes verified")
