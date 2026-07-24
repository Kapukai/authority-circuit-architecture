#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="$(tr -d '[:space:]' < VERSION)"
RELEASE_NAME="ACA-${VERSION}"
DIST_DIR="$ROOT/dist"
STAGE_DIR="$DIST_DIR/$RELEASE_NAME"

python3 scripts/validate.py
if [[ "${SKIP_PDF_BUILD:-0}" != "1" ]]; then
  ./scripts/build.sh
fi
test -f docs/build/ACA_Standards_Program_v0.1.pdf

rm -rf "$DIST_DIR"
mkdir -p "$STAGE_DIR"

copy_tree() {
  local source="$1"
  local destination="$2"
  mkdir -p "$STAGE_DIR/$destination"
  cp -R "$source"/. "$STAGE_DIR/$destination/"
}

copy_tree docs/tex docs/tex
copy_tree schemas schemas
copy_tree examples examples
copy_tree site site
copy_tree scripts scripts
mkdir -p "$STAGE_DIR/docs/build"
cp docs/build/ACA_Standards_Program_v0.1.pdf "$STAGE_DIR/docs/build/"
cp README.md ROADMAP.md GOVERNANCE.md CONTRIBUTING.md SECURITY.md \
  CHANGELOG.md CITATION.cff LICENSE.md VERSION "$STAGE_DIR/"

find "$STAGE_DIR" \( -name '.DS_Store' -o -name '._*' \) -delete

(
  cd "$STAGE_DIR"
  find . -type f ! -name MANIFEST.sha256 -print0 \
    | sort -z \
    | xargs -0 sha256sum > MANIFEST.sha256
)

(
  cd "$DIST_DIR"
  zip -qr "${RELEASE_NAME}.zip" "$RELEASE_NAME"
  tar -czf "${RELEASE_NAME}.tar.gz" "$RELEASE_NAME"
  sha256sum "${RELEASE_NAME}.zip" "${RELEASE_NAME}.tar.gz" \
    > "${RELEASE_NAME}.artifacts.sha256"
)

echo "Release artifacts:"
find "$DIST_DIR" -maxdepth 1 -type f -printf '  %f\n' | sort
