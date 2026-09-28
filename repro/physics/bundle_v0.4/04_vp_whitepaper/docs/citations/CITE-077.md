# CITE-077 — Seawater process: H2O & ion amplitude ranges (device/environment)

- **DOI:** 10.5281/zenodo.17932567 (this deposit)
- **Used in:** Sec.18.3.2, Sec.18.6.3 (`[cite: 77, 83]`, `[cite: 77, 102]`, `[cite: 77]`)
- **Type:** derived scalars (operational range)
- **Gate status:** PASS (H2O/Na+ scalars)

## Scalars included in the bundle

- **H2O operational range:** ±255–275 fm (represented by 265 fm in the dataset)
- **Na+ ion expansion example:** 320 fm

## Bundle pointers

- Input data: `04_vp_whitepaper/data/chem/observed_amplitudes.csv` (H2O, Na+ rows)
- Derived check: `04_vp_whitepaper/outputs/chem/sqrt2_validation.json` (H2O, Na+ rows)
- Gate report: `runs/*/outputs/gate_reports/gate_report_chem_sqrt2_validation.json`

## Notes

The Cl- upper value (e.g., 340 fm) used in the narrative is not explicitly stored as a separate row in this version; treat that extension as contextual unless a dedicated row/dataset is added in a future DOI version.
