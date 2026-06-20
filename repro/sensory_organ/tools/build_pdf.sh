#!/usr/bin/env bash
# build_pdf.sh -- compile the generated whitepaper to a byte-reproducible PDF.
# Reproducibility: SOURCE_DATE_EPOCH + FORCE_SOURCE_DATE freeze pdftex's date; the .tex sets
# \pdfinfoomitdate / \pdftrailerid so creation/mod dates and the trailer id are omitted/fixed.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG="$(cd "$HERE/.." && pwd)"
DIST="$PKG/dist"
TEX="sensory_organ_vp_site.tex"

# fixed epoch == BUILD_DATE 2026-06-18 00:00:00 UTC (matches _sns_render.BUILD_DATE)
export SOURCE_DATE_EPOCH="$(date -u -d '2026-06-18 00:00:00' +%s)"
export FORCE_SOURCE_DATE=1

cd "$DIST"
# two passes: ToC + section refs resolve on the second
for i in 1 2; do
  pdflatex -interaction=nonstopmode -halt-on-error "$TEX" >/dev/null 2>&1 || {
    echo "pdflatex pass $i FAILED; tail of log:"; tail -40 "${TEX%.tex}.log"; exit 1; }
done
# clean aux artifacts, keep tex + pdf
rm -f "${TEX%.tex}.aux" "${TEX%.tex}.log" "${TEX%.tex}.out" "${TEX%.tex}.toc"
echo "OK -> $DIST/${TEX%.tex}.pdf"
