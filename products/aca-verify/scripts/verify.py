#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md", "src/aca_verify.py", "profiles/aca-dpr-baseline-v0.1.json",
    "examples/passing-decision.json", "examples/warning-decision.json",
    "examples/failing-decision.json", "examples/indeterminate-decision.json",
    "tests/test_aca_verify.py", "docs/WORK_ORDER.md", "docs/THREAT_MODEL.md",
    "docs/PUBLIC_DISCLOSURE_BOUNDARY.md", "RELEASE_NOTES.md"
]
for rel in required:
    assert (ROOT / rel).is_file(), f"missing {rel}"
for path in list((ROOT / "profiles").glob("*.json")) + list((ROOT / "examples").glob("*.json")):
    json.loads(path.read_text(encoding="utf-8"))
subprocess.run([sys.executable, str(ROOT / "tests" / "test_aca_verify.py")], check=True)
for name, code in (("passing-decision.json", 0), ("warning-decision.json", 0),
                   ("failing-decision.json", 1), ("indeterminate-decision.json", 2)):
    result = subprocess.run([sys.executable, str(ROOT / "src" / "aca_verify.py"),
                             str(ROOT / "examples" / name), "--format", "json"],
                            capture_output=True, text=True)
    assert result.returncode == code, (name, result.returncode, result.stderr)
    parsed = json.loads(result.stdout)
    assert parsed["claim_scope"] == "PARTIAL_PROFILE_CONFORMANCE"
print("PASS: ACA Verify package verified")
