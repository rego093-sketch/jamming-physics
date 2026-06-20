# repro/neuro/04-code-working-memory

CAUSAL CLAIM — SEPARATE LANE. capacity = theta/gamma -> 7+-2 is reproduced by module `10_wm_capacity.py` (numpy); the causal step (tACS on theta changes capacity) is the cited human tACS result, NOT this offline harness. The one link with causal evidence; its support is the published manipulation, not a bundled simulation.

Offline regression for the bundled artifacts: `../_verify/run_regression.py` (REGRESSION PASS, seed=7, bit-for-bit). 'SEPARATE LANE' = reproduced by the `neuro_extension` module suite (numpy/scipy; module 11 and the Stage-5 reads also need OpenNeuro ds004117 / ds004752), which is honest per the SPEC lane rules.
