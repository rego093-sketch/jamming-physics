# lattice_percolation_soc_bundle (DOI-ready)

This archive contains code + results that support a discrete 3D jammed-lattice model:
- 3D jamming + percolation extraction of an effective neck gap δ_eff (aka g*)
- SOC (self-organized critical) pinning that yields a robust amplification factor A ~ 10^6
- MST Option–B **unit realisation** using an operational anchor at 633 nm
- A sparse-sampled **visible carrier (633/532 nm)** wave demo on the realised lattice units

## Quick start

Install:
```bash
pip install -r requirements.txt
```

Run everything (regenerate results/ and images/):
```bash
python code/run_all.py
```

Run only the MST unit realisation + RCROSS:
```bash
python code/mst_optionb_unit_realization.py
```

Run only the visible-wave carrier demo:
```bash
python code/lattice_visible_wave_emergence.py
```

## Main outputs

- `results/soc_run3_avalanches.csv` : avalanche log including `A_post`
- `results/soc_N750/` : supplementary N=750 rerun logs (seeds 45–48) + summaries (N-scaling sanity check)
- `results/mst_unit_realization.json` : realised lattice units `(a, Δt)` from the 633 nm operational anchor
- `results/mst_rcross.csv` + `images/mst_rcross.png` : RCROSS(633/532) report
- `results/visible_wave_summary.json` + `images/visible_wave_*` : visible-carrier demo artifacts

## Reproducibility

- Pre-registered thresholds are bundled as `config/thresholds.yaml` (also copied to `./thresholds.yaml`).
- File checksums are recorded in `manifest_sha256.txt`.

See `docs/` for Korean documentation and the included PDF manuscripts.
