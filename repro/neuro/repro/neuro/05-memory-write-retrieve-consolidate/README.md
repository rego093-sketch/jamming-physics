# repro/neuro/05-memory-write-retrieve-consolidate

MODEL — SEPARATE LANE. NMDA write, attractor retrieval (~0.138N), consolidation/reconsolidation, CREB allocation are reproduced by modules 19-22 (numpy). Anchors: Ribot gradient, Nader reconsolidation, CREB allocation = literature.

Offline regression for the bundled artifacts: `../_verify/run_regression.py` (REGRESSION PASS, seed=7, bit-for-bit). 'SEPARATE LANE' = reproduced by the `neuro_extension` module suite (numpy/scipy; module 11 and the Stage-5 reads also need OpenNeuro ds004117 / ds004752), which is honest per the SPEC lane rules.
