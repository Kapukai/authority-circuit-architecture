#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/docs/tex"
mkdir -p ../build

if command -v latexmk >/dev/null; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
else
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build main.tex
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../build main.tex
fi

mv ../build/main.pdf ../build/ACA_Standards_Program_v0.1.pdf
echo "Built docs/build/ACA_Standards_Program_v0.1.pdf"
