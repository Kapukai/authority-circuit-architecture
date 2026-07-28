#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
for f in allow hold-unknown conflict revoked deny; do
 echo "=== $f ==="
 .venv/bin/python -m kapu.cli "examples/$f.json" | .venv/bin/python -c 'import json,sys;d=json.load(sys.stdin);print(d["state"],d["reason_code"],"executed=",d["execution"]["executed"])'
done
