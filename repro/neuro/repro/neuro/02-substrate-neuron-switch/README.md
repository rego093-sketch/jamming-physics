# repro/neuro/02-substrate-neuron-switch

REPRODUCES OFFLINE (model). `_verify/inputs/neural_function_results.json` — neuron period/fast = 123.1 (period >> switch timescale => low frequency); freq_vs_tau monotone; coupled population coherence. Re-checked by `_verify/run_regression.py`.

Offline regression for the bundled artifacts: `../_verify/run_regression.py` (REGRESSION PASS, seed=7, bit-for-bit). 'SEPARATE LANE' = reproduced by the `neuro_extension` module suite (numpy/scipy; module 11 and the Stage-5 reads also need OpenNeuro ds004117 / ds004752), which is honest per the SPEC lane rules.
