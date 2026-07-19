#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 ACA-160 'Document Title'"
  exit 1
fi
ID="$1"
TITLE="$2"
SLUG="$(echo "$ID" | tr '[:upper:]' '[:lower:]')"
FILE="docs/tex/sections/${SLUG}.tex"
cat > "$FILE" <<EOF
\\chapter{${ID} --- ${TITLE}}
\\section{Status}
Working Draft.
\\section{Scope}
Define scope.
\\section{Normative Requirements}
\\begin{requirement}[${ID}-001]
An implementation SHALL ...
\\end{requirement}
EOF
echo "Created $FILE"
