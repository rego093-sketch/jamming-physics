# Changelog for rotcore-sim-prf DOI archive

## v1.3.9

- Recomputed TRIAD medians (`data/triad_v139.csv`) directly from `data/metrics_long_v1.3.9.csv`.
- Recomputed rel_med and R2 in `data/Aprime_ext_v139.csv` from `metrics_long_v1.3.9.csv`, and added an explicit R2 definition to METRICS_SPEC.
- Recomputed auxiliary metrics (`data/metrics_aux_v139.csv`) from `metrics_long_v1.3.9.csv`.
- Copied the robust/coverage/identity-residual summaries to v1.3.9 files (`data/metrics_robust_v139.csv`, etc.), leaving the original v1.3.8
  versions under `legacy/`.
- Moved all v1.3.6 and v1.3.8 snapshot tables into the `legacy/` subdirectory; they are no longer used for the final Tables 3, S1, S2, S5, or S6.


## v1.3.8

- Recomputed all per-case/per-method summary metrics directly from `data/metrics_long_v1.3.8.csv`.
- Fixed an inconsistency in the 2D Turbulence summary rows of the earlier v1.3.6 snapshot
  (median relative error and Spearman correlation had been duplicated across methods).
- Added `data/Aprime_ext_v138.csv` and `data/metrics_aux_v138.csv` to reflect the corrected v1.3.8 aggregates.
- Moved the old v1.3.6 snapshot tables (`triad_v136.csv`, `Aprime_ext_v136.csv`, `metrics_aux_v136.csv`,
  `inner_core_v136.csv`, `conv6_v136.csv`) into the `legacy/` subdirectory.

## v1.3.7

- Introduced `data/metrics_long_v137.csv` and robust error summaries (`metrics_robust_v137.csv`,
  `coverage_v137.csv`, `identity_resid_v137.csv`, `shape_stats_v137.csv`).

## v1.3.6

- Initial single-snapshot audit tables used for the first inline version of the PRF manuscript.
