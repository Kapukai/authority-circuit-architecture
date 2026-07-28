#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "[1/7] Create isolated clean-room environment"
python3 -m venv "$TMP/venv"
echo "[2/7] Upgrade packaging tools"
"$TMP/venv/bin/python" -m pip install --upgrade pip setuptools wheel >/dev/null
echo "[3/7] Install KAPU with test dependencies"
"$TMP/venv/bin/python" -m pip install -e "$ROOT[dev]" >/dev/null
echo "[4/7] Run complete test suite"
cd "$ROOT"
"$TMP/venv/bin/python" -m pytest -q
echo "[5/7] Verify deterministic DPR endpoint"
"$TMP/venv/bin/python" -m kapu.cli examples/allow.json > "$TMP/decision.json"
"$TMP/venv/bin/python" -m kapu.dpr_cli build "$TMP/decision.json" --created-at 2026-07-28T12:00:00+00:00 > "$TMP/dpr-a.json"
"$TMP/venv/bin/python" -m kapu.dpr_cli verify "$TMP/dpr-a.json"
"$TMP/venv/bin/python" -m kapu.dpr_cli build "$TMP/decision.json" --created-at 2026-07-28T12:00:00+00:00 > "$TMP/dpr-b.json"
cmp "$TMP/dpr-a.json" "$TMP/dpr-b.json"
echo "[6/7] Reject tracked build artifacts"
if git -C "$REPO" ls-files | grep -E '(^|/).*\.egg-info/' >/dev/null; then
  echo "FAIL: tracked *.egg-info files remain" >&2
  git -C "$REPO" ls-files | grep -E '(^|/).*\.egg-info/'
  exit 1
fi
echo "[7/7] Show repository state"
git -C "$REPO" status --short
echo
echo "KAPU-0002.1 RELEASE GATE: PASS"
echo "Clean-room installation, tests, deterministic DPR, and repository hygiene are green."
