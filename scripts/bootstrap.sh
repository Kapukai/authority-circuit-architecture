#!/usr/bin/env bash
set -euo pipefail

echo "Kapukai Authority Circuit bootstrap"
command -v git >/dev/null || { echo "git is required"; exit 1; }

if command -v latexmk >/dev/null; then
  echo "latexmk found"
elif command -v pdflatex >/dev/null; then
  echo "pdflatex found"
else
  echo "No LaTeX compiler found."
  echo "macOS: brew install --cask mactex-no-gui"
  echo "Debian/Ubuntu: sudo apt-get install texlive-latex-extra latexmk"
fi

echo "Ready."
