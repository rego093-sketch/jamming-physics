# rotcore-sim-prf v1.3.9 (DOI archive)

This deposit contains code and data to reproduce the numerical tables in the PRF submission
"Rotational Core Capacity Diagnostics: A reproducible identity–prediction cross-check with DOI-inline tables."

This version supersedes v1.3.8 by making all per-case/per-method summary tables directly reproducible from the
sample-level file `data/metrics_long_v1.3.9.csv`, and by isolating earlier snapshot tables under `legacy/`.

## Contents

- `manuscript/` — TeX sources for the manuscript (see main repository for the latest text).
- `data/metrics_long_v1.3.9.csv` — Sample-level table (case, method, L_core, phi, N_star, s, r_pred, r_meas).
- `data/triad_v139.csv` — TRIAD medians per case (L_core_med, phi_med, N_med(A)), recomputed from `metrics_long_v1.3.9.csv`.
- `data/Aprime_ext_v139.csv` — Extended A' table: best per-method hyperparameters and rel_med [%] with denominator r_pred, plus R2,
  all recomputed from `metrics_long_v1.3.9.csv`.
- `data/metrics_aux_v139.csv` — Auxiliary single-scale metrics: MAE, MAPE[%] (pred denom), Spearman rho, recomputed from `metrics_long_v1.3.9.csv`.
- `data/metrics_robust_v139.csv` — Robust error summaries per case/method (rel_med, MAE/MAPE, NRMSE, Spearman rho, with bootstrap CIs).
- `data/coverage_v139.csv` and `data/coverage_ci_v139.csv` — Coverage within ±10%/±20% and corresponding 95% Wilson CIs.
- `data/identity_resid_v139.csv` and `data/identity_resid_ci_v139.csv` — Identity residual summaries and bootstrap CIs.
- `data/shape_stats_v139.csv` — Per case/method summaries of shape factor s and blob count N_star (median, IQR, 5th/95th percentiles).

- `legacy/metrics_long_v1.3.8.csv`, `legacy/triad_v138.csv`, `legacy/Aprime_ext_v138.csv`, `legacy/metrics_aux_v138.csv`,
  `legacy/metrics_robust_v138.csv`, `legacy/coverage_v138.csv`, `legacy/coverage_ci_v138.csv`,
  `legacy/identity_resid_v138.csv`, `legacy/identity_resid_ci_v138.csv`, `legacy/shape_stats_v138.csv`,
  and the original v1.3.6 snapshot tables (`legacy/triad_v136.csv`, `legacy/Aprime_ext_v136.csv`,
  `legacy/metrics_aux_v136.csv`, `legacy/inner_core_v136.csv`, `legacy/conv6_v136.csv`) are kept for historical reference only.
  They are not used to produce the final Tables 3, S1, S2, S5, or S6 in the manuscript.

- `code/environment.yml` — Minimal environment (Python, NumPy, pandas).
- `code/scripts/compute_robust_v137.py`, `code/scripts/coverage_v137.py`, `code/scripts/identity_residual_v137.py`,
  `code/scripts/recompute_v136.py` — Original scripts used to generate v1.3.7 robust tables and v1.3.6 snapshots.
- `docs/METRICS_SPEC_v1.3.9.json` — Machine-readable specification of all metrics and v1.3.9 files.

## Version history (abridged)

- v1.3.9 — Recomputed all per-case/per-method summary tables (TRIAD medians, extended A', auxiliary metrics) directly from
  `data/metrics_long_v1.3.9.csv`, and added an explicit R2 definition. Isolated all earlier v1.3.6/v1.3.8 snapshot tables under `legacy/`.
- v1.3.8 — Recomputed per-case/per-method summary metrics directly from `data/metrics_long_v1.3.8.csv`;
  fixed an inconsistency in the 2D Turbulence summary rows of the earlier v1.3.6 snapshot.
- v1.3.7 — Introduced sample-level table `data/metrics_long_v137.csv` and robust error summaries.
- v1.3.6 — Initial single-snapshot audit tables used for the first inline version of the PRF manuscript.
