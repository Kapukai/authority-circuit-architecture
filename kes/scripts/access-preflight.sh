#!/usr/bin/env bash
set -euo pipefail
echo "KES access preflight (values are never printed)"
check_env() {
  local name="$1"
  if [[ -n "${!name:-}" ]]; then echo "PASS env:$name configured"; else echo "INFO env:$name not configured"; fi
}
command -v git >/dev/null && echo "PASS git installed" || echo "FAIL git missing"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "PASS inside Git repository"
  git remote -v | sed -E 's#(https://)[^/@]+:[^/@]+@#\1***:***@#g'
else
  echo "INFO not currently inside a Git repository"
fi
if command -v gh >/dev/null 2>&1; then
  gh auth status >/dev/null 2>&1 && echo "PASS GitHub CLI authenticated" || echo "INFO GitHub CLI not authenticated"
else
  echo "INFO GitHub CLI not installed (git push may still work through credential manager)"
fi
check_env OPENAI_API_KEY
check_env ANTHROPIC_API_KEY
check_env DATABASE_URL
check_env KAPUKAI_DEPLOY_HOST
echo "Never paste passwords, private keys, tokens, or API-key values into chat or commit them."
