#!/bin/sh
# Reproduce VP_Chemistry_EM.pdf. Requires: pandoc, xelatex (TeX Live), Latin Modern + DejaVu fonts.
cd "$(dirname "$0")"
pandoc 00_front_full.md EM_CHAPTER_EN.md EM12_dynamics.md CHEMISTRY_CHAPTER_EN.md \
  CM_CHAPTER_EN.md CC_CHAPTER_EN.md CT_CHAPTER_EN.md CA_CHAPTER_EN.md CA_CO2.md \
  appendix_open.md 99_conclusion_full.md \
  -s -o ../VP_Chemistry_EM.tex --template=default.tex -H header_q.tex \
  -V mainfont="Latin Modern Roman" -V monofont="DejaVu Sans Mono" -V monofontoptions="Scale=0.85" \
  -V geometry:margin=2.4cm -V fontsize=10pt -V linestretch=1.05 \
  -V colorlinks=true -V linkcolor=RoyalBlue -V urlcolor=RoyalBlue --toc --toc-depth=2
cd .. && xelatex -interaction=nonstopmode VP_Chemistry_EM.tex && xelatex -interaction=nonstopmode VP_Chemistry_EM.tex
