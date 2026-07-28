#!/usr/bin/env bash
set -euo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"

echo "[1/5] Install editable package"
.venv/bin/python -m pip install -e . >/dev/null

echo "[2/5] Full test suite"
.venv/bin/python -m pytest -q

echo "[3/5] Build deterministic DPR"
.venv/bin/python -m kapu.cli examples/allow.json > /tmp/kapu-decision.json
.venv/bin/python -m kapu.dpr_cli build /tmp/kapu-decision.json   --created-at 2026-07-28T12:00:00+00:00 > /tmp/kapu-dpr.json

echo "[4/5] Validate and independently verify DPR"
.venv/bin/python -m kapu.dpr_cli verify /tmp/kapu-dpr.json

echo "[5/5] Rebuild and compare golden output"
.venv/bin/python -m kapu.dpr_cli build /tmp/kapu-decision.json   --created-at 2026-07-28T12:00:00+00:00 > /tmp/kapu-dpr-2.json
cmp /tmp/kapu-dpr.json /tmp/kapu-dpr-2.json

echo
echo "KAPU-0002 verification: PASS"
echo "Decision Proof Record generation is deterministic and tamper-evident."
