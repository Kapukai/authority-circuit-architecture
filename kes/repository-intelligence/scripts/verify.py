#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
required=["README.md","scripts/analyze.py","scripts/verify.py","tests/test_analyze.py","docs/WORK_ORDER.md","docs/ADR-0003.md","docs/THREAT_MODEL.md","docs/CLASSIFICATION.md","RELEASE_NOTES.md"]
errors=[f"missing: {p}" for p in required if not (ROOT/p).is_file()]
proc=subprocess.run([sys.executable,str(ROOT/"tests/test_analyze.py")],capture_output=True,text=True)
if proc.returncode: errors.append(proc.stdout+proc.stderr)
if errors:
    print("FAIL"); print("\n".join("- "+e for e in errors)); raise SystemExit(1)
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob("*")) if p.is_file() and "dist" not in p.parts}
(ROOT/"CHECKSUMS.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(f"PASS: {len(manifest)} files verified")
