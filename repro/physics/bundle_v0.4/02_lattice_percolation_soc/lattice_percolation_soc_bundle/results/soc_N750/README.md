# SOC percolation pinning reruns — N=750 (seeds 45–48)

This folder contains **supplementary rerun artifacts** for the SOC percolation pinning module at a larger system size (**N=750**).
These files are provided as a **robustness / N-scaling sanity check** for the amplification observable

\[
A := \frac{a_\mathrm{med}}{g_\*}.
\]

**Important:** This dataset is **NON-LOCK**: it is **not used to set any locked constants** in the white paper.
It is included to strengthen reproducibility by demonstrating that the N-scaling behavior is consistent with the
baseline N=200 run already included in this deposit.

## Raw data

- `soc_results_N750_seed45.csv`
- `soc_results_N750_seed46.csv`
- `soc_results_N750_seed47.csv`
- `soc_results_N750_seed48.csv`

Each CSV is an avalanche log with columns:

`step,type,S,eps,g_star,a_med,A`

Some avalanches report `g_star=0`, producing `A=0` by construction. Summary statistics therefore filter on `g_star>1e-12`.

## Summaries

- `soc_N750_summary.json` : aggregated + per-seed statistics and a scaling check
- `soc_N750_per_seed_summary.csv` : per-seed table
- `soc_N750_aggregate_summary.csv` : aggregated one-row table
- `soc_N750_scaling_check.json` : explicit comparison vs baseline and unit realization

## Scaling check (headline)

Let the baseline be the N=200 run (`../soc_run3_summary.json`) and the unit realization anchor be `../mst_unit_realization.json`.

Under fixed microscopic threshold `g0` and unit box `L=1`, typical distances scale as `N^(-1/3)`; hence `A` is expected
to scale approximately as `N^(-1/3)` if the `g_star` distribution is stable.

Across seeds 45–48 (104 avalanches; 98 with `g_star>0`), the observed mean is:

- `A_mean(N=750) ≈ 5.693e+05`

The prediction from the unit realization anchor:

- `A_pred_from_A_geo ≈ 5.684e+05`

Relative error:

- `(A_mean - A_pred)/A_pred ≈ +1.629e-03`

## Script

- `soc_percolation_pinning_N750_clean_colab.py` is the user-provided Colab script used to produce the raw CSV artifacts.

