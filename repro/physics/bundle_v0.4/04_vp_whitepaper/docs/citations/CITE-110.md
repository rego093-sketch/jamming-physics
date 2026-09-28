# CITE-110 — SOC percolation pinning reruns (N=750; seeds 45–48)

- **DOI:** 10.5281/zenodo.17932567 (this deposit)
- **Used in:** Sec.10.3.11 (`[cite: 110]`)
- **Type:** rerun dataset / reproducibility artifact (NON-LOCK)
- **Gate status:** PASS (artifact sealed); interpretation is NON-LOCK

## What this is

This cite-ID points to supplementary rerun artifacts for the SOC percolation pinning module at larger system size **N=750**.
The goal is to provide a robustness / N-scaling sanity check for the amplification observable

\[
A := \frac{a_\mathrm{med}}{g_\*}.
\]

These reruns are **not used** to set any locked constants.

## Bundle pointers

- Raw logs:
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_results_N750_seed45.csv`
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_results_N750_seed46.csv`
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_results_N750_seed47.csv`
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_results_N750_seed48.csv`
- Summaries:
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_N750_summary.json`
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_N750_scaling_check.json`
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_N750_per_seed_summary.csv`
- Script reference:
  - `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_N750/soc_percolation_pinning_N750_clean_colab.py`

## Notes

- Summary statistics exclude rows with `g_star=0` by applying `g_star>1e-12`.
- The scaling check compares N=750 results against:
  - baseline N=200 run: `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_run3_summary.json`
  - unit realization anchor: `02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/mst_unit_realization.json`
