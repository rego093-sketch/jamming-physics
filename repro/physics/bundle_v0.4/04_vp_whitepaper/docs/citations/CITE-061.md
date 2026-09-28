# CITE-061 — CO2 case: decomposition / thermal drive (scalar + context)

- **DOI:** 10.5281/zenodo.17932567 (this deposit)
- **Used in:** Sec.18.3.2 and Sec.18.6.2 (`[cite: 61, 65]`, `[cite: 61]`)
- **Type:** derived scalar + contextual setup note
- **Gate status:** PASS (scalar)

## Scalar definition

- **System:** CO2
- **Observed amplitude:** ±300 fm (bond break)
- **Base amplitude (derived):** ~205 fm
- **Ratio:** ~1.46

## Bundle pointers

- Input data: `04_vp_whitepaper/data/chem/observed_amplitudes.csv` (CO2 row)
- Derived check: `04_vp_whitepaper/outputs/chem/sqrt2_validation.json` (CO2 row)
- Gate report: `runs/*/outputs/gate_reports/gate_report_chem_sqrt2_validation.json`

## Notes

The numeric temperature label (e.g., "1800 K equivalent") is treated as *context* unless a primary run log is included.
