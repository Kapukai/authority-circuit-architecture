#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "[1/5] Validate required files"
test -f "$ROOT/KES-CONSTITUTION.md"
test -f "$ROOT/kes/capabilities/registry.json"
test -f "$ROOT/kes/schemas/work-order.schema.json"
echo "[2/5] Run planner unit tests"
python3 -m unittest discover -s "$ROOT/kes/tests" -p 'test_*.py'
echo "[3/5] Plan KES example"
python3 "$ROOT/kes/scripts/plan_capabilities.py" "$ROOT/kes/examples/KES-WO-0001.json" >/tmp/kes-plan.json
grep -q '"verification"' /tmp/kes-plan.json
echo "[4/5] Plan EDS example"
python3 "$ROOT/kes/scripts/plan_capabilities.py" "$ROOT/kes/examples/EDS-WO-0001.json" >/tmp/eds-plan.json
grep -q '"product"' /tmp/eds-plan.json
grep -q '"security"' /tmp/eds-plan.json
echo "[5/5] Secret hygiene scan"
if grep -RInE '(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|password[[:space:]]*=[[:space:]]*[^$<{])' "$ROOT" \
  --exclude='verify.sh' \
  --exclude='SECRETS_AND_ACCESS.md' \
  --exclude-dir='.git' \
  --exclude-dir='.venv' \
  --exclude-dir='node_modules' \
  --exclude-dir='dist' \
  --exclude-dir='build' \
  --exclude-dir='site-packages' \
  --exclude-dir='__pycache__'; then
  echo "FAIL: possible secret committed"
  exit 1
fi
echo "KES-WO-0001 verification: PASS"
