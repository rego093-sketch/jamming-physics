# REPRODUCE

```
python repro/run_all.py               # research entry: emerge, circulate, probes, stress + pathology, gate
python repro/_engine/vp_*_engine.py   # emergence JSON (+ sha256)
python repro/_verify/gates.py         # research gate + writing-lock status

# writing phase (only after research is green + PHASE=writing):
echo writing > PHASE
python tools/build_docs.py            # deterministic per-title canonical HTML into docs/ (VP-SPEC v1.8)

# publication phase (PHASE=published; gate unlocks for {writing, published}):
python tools/build_docs.py            # re-render HTML with the concept DOI emitted
python tools/build_tex.py             # deterministic LaTeX from the same corpus -> dist/sensory_organ_vp_site.tex
bash   tools/build_pdf.sh             # reproducible pdflatex compile -> dist/sensory_organ_vp_site.pdf
```

Determinism (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed; round-before-hash; sorted
JSON keys. Two engine runs yield an identical sha256. The HTML generator is likewise deterministic — numbers
are loaded from the verified result, BUILD_DATE is fixed (no wall-clock), so docs/ rebuilds byte-identically.
The PDF/TeX is generated from the **same** authored prose-as-data and the **same** verified numbers as the
HTML (so it cannot drift from the site); `build_pdf.sh` sets SOURCE_DATE_EPOCH and the .tex sets
`\pdfinfoomitdate` / `\pdftrailerid`, so the PDF is byte-identical across independent compiles.
No hand-entered numbers. stdlib + numpy only (PDF step also needs pdflatex + the Times/Helvetic psnfss fonts).
