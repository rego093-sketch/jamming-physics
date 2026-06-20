# repro/neuro/08-output-motor

DIRECTION — SEPARATE LANE. Cerebellar supervised learning, reflex arc (stretch-reflex ~9.4x), motor unit (size principle; force-frequency ~3.9x) are reproduced by modules 26-28 (numpy). Anchors: Marr-Albus-Ito, Sherrington, Henneman, De Luca = literature. Absolute gains/latencies = OPEN.

Offline regression for the bundled artifacts: `../_verify/run_regression.py` (REGRESSION PASS, seed=7, bit-for-bit). 'SEPARATE LANE' = reproduced by the `neuro_extension` module suite (numpy/scipy; module 11 and the Stage-5 reads also need OpenNeuro ds004117 / ds004752), which is honest per the SPEC lane rules.
