#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "README.md",
    ROOT / "docs" / "WORK_ORDER.md",
    ROOT / "human-authorization.schema.json",
    ROOT / "examples" / "authorized.example.json",
]

PROHIBITED_IN_CODE = [
    "auto_authorize",
    "automatic_authorization",
    "infer_consent",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")


def main() -> int:
    failures = 0
    for path in REQUIRED:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")
            failures += 1

    if failures:
        return 1

    schema = json.loads((ROOT / "human-authorization.schema.json").read_text())
    example = json.loads((ROOT / "examples" / "authorized.example.json").read_text())

    required = set(schema.get("required", []))
    missing = sorted(required - set(example))
    if missing:
        fail(f"example missing schema-required fields: {', '.join(missing)}")
        failures += 1

    if example.get("state") == "AUTHORIZED":
        attestation = example.get("human_attestation", {})
        if attestation.get("affirmative") is not True:
            fail("AUTHORIZED record lacks affirmative human attestation")
            failures += 1
        if not example.get("authorized_scope"):
            fail("AUTHORIZED record lacks explicit scope")
            failures += 1
        if not example.get("affected_rights_and_interests"):
            fail("AUTHORIZED record lacks affected-rights analysis")
            failures += 1
        if not example.get("reason_for_authorization"):
            fail("AUTHORIZED record lacks reasons")
            failures += 1

    for path in ROOT.rglob("*.py"):
        lowered = path.read_text(encoding="utf-8").lower()
        for phrase in PROHIBITED_IN_CODE:
            if phrase in lowered and path.name != "verify.py":
                fail(f"prohibited automation phrase in {path.relative_to(ROOT)}: {phrase}")
                failures += 1

    if failures:
        return 1

    print("PASS: EDS-0004 authorization boundary, schema, and example verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
