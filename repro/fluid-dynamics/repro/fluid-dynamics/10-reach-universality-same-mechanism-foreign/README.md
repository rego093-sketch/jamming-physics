# 10-reach-universality-same-mechanism-foreign
Verifies: Reach U1-U3: Burgers saturation; capacity identity d=2..5 to 1e-16; Turing k* to 6-8%. Run: python universality.py.
Section: §10 — Reach and universality: the same mechanism in foreign domains (whitepaper v2.1, concept DOI 10.5281/zenodo.17972568)

## Reproduction map
- `universality.py` (+ `.out.txt`) — reach exhibits U1–U3 (Burgers / capacity / Turing).
- `agc-rotating-core-contraction/` — foreign-domain reach exhibit folded in from
  the standalone `AGC_DOI_v3` package: anomalous geometric contraction of
  hyper-rotating cores under shockwave confinement in stiff media (compressible
  Euler / HLLC / Tait EOS, negative-centrifugal effect). Per-figure/table CSVs,
  grid-convergence + toy-contraction data and figures, Euler–HLLC solver
  template. See `agc-rotating-core-contraction/PROVENANCE.md`.
  Now cited in §10 body prose (foreign-domain reach paragraph) and linked in the
  §10 claim-strip ("AGC reach exhibit").
