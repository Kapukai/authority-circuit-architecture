#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
.venv/bin/python -m pip install -e . >/dev/null
.venv/bin/python -m pytest -q
.venv/bin/python -m kapu.cli examples/allow.json > /tmp/kapu-allow.json
grep -q '"state": "ALLOW"' /tmp/kapu-allow.json
.venv/bin/python -m kapu.cli examples/hold-unknown.json > /tmp/kapu-hold.json
grep -q '"state": "HOLD"' /tmp/kapu-hold.json
echo; echo "KAPU-0001 verification: PASS"
