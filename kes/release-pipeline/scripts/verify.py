#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
required=['README.md','kes-release.schema.json','scripts/release.py','scripts/verify.py','docs/WORK_ORDER.md','docs/ADR-0002.md','docs/THREAT_MODEL.md','docs/RELEASE_POLICY.md','examples/eds-0003.release.json','tests/test_release.py','RELEASE_NOTES.md']
errors=[f'missing: {x}' for x in required if not (ROOT/x).is_file()]
try: json.loads((ROOT/'kes-release.schema.json').read_text()); json.loads((ROOT/'examples/eds-0003.release.json').read_text())
except Exception as exc: errors.append('invalid JSON: '+str(exc))
p=subprocess.run([sys.executable,str(ROOT/'tests/test_release.py')],capture_output=True,text=True)
if p.returncode: errors.append(p.stdout+p.stderr)
if errors:
    print('FAIL'); print('\n'.join('- '+x for x in errors)); raise SystemExit(1)
sums={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and 'dist' not in p.parts}
(ROOT/'CHECKSUMS.json').write_text(json.dumps(sums,indent=2)+'\n')
print(f'PASS: {len(sums)} files verified')
