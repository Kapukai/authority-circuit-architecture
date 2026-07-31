#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "index.html",
    "src/app.js",
    "src/replay.mjs",
    "src/styles.css",
    "tests/replay.test.mjs",
    "examples/original.dpr.json",
    "examples/replay.dpr.json",
    "docs/WORK_ORDER.md",
    "docs/ADR-0001.md",
    "docs/THREAT_MODEL.md",
    "docs/CAPABILITY_PLAN.md",
    "RELEASE_NOTES.md",
]

errors = []
for relative in REQUIRED:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"missing: {relative}")

for relative in ("examples/original.dpr.json", "examples/replay.dpr.json", "examples/divergent-replay.dpr.json"):
    try:
        json.loads((ROOT / relative).read_text())
    except Exception as exc:
        errors.append(f"invalid JSON {relative}: {exc}")

for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts:
        data = path.read_bytes()
        if len(data) == 0:
            errors.append(f"empty: {path.relative_to(ROOT)}")

if errors:
    print("FAIL")
    print("\n".join(f"- {item}" for item in errors))
    sys.exit(1)

manifest = {}
for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts):
    manifest[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()

(ROOT / "CHECKSUMS.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"PASS: {len(manifest)} files verified")
