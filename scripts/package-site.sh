#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="$(tr -d '[:space:]' < VERSION)"
NAME="ACA-site-${VERSION}"
SOURCE="$ROOT/site/standards/authority-circuit"
OUTPUT="$ROOT/dist/site"
STAGE="$OUTPUT/$NAME/authority-circuit"

python3 scripts/validate.py
test -f "$SOURCE/index.html"

rm -rf "$OUTPUT"
mkdir -p "$STAGE"
cp -R "$SOURCE"/. "$STAGE/"

find "$OUTPUT/$NAME" \( -name '.DS_Store' -o -name '._*' \) -delete

(
  cd "$OUTPUT/$NAME"
  find . -type f ! -name MANIFEST.sha256 -print0 \
    | sort -z \
    | xargs -0 sha256sum > MANIFEST.sha256
)

(
  cd "$OUTPUT"
  zip -qr "${NAME}.zip" "$NAME"
  tar -czf "${NAME}.tar.gz" "$NAME"
  sha256sum "${NAME}.zip" "${NAME}.tar.gz" > "${NAME}.artifacts.sha256"
)

echo "Site deployment artifacts:"
find "$OUTPUT" -maxdepth 1 -type f -printf '  %f\n' | sort
