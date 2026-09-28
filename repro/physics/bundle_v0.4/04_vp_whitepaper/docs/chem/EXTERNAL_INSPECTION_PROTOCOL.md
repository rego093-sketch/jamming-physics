# External inspection protocol (bulk literature validation)

This folder documents the **bulk literature inspection dataset** used to validate the VP chemistry amplitude rule in Sec.18.

## Dataset

- **Dataset ID:** `VP_STEP7_EXT_INSPECTION_FULL_V1`
- **File:** `04_vp_whitepaper/data/chem/external_inspection/VP_STEP7_EXT_INSPECTION_FULL_V1.csv`

The file is a CSV with comment lines starting with `#`.

### Columns

- `ID` : stable row identifier
- `GROUP` : one of `Atom`, `Metal`, `Molecule`, `Complex`, `Solid`, `Failure`
- `FORMULA` : chemical formula label (informational)
- `Z_AVG` : informational effective Z label used in the source compilation
- `R_COV_AVG(pm)` : informational effective radius label used in the source compilation
- `P_IDX` : normalized pressure index used by the VP amplitude rule
- `CALC_AMP(fm)` : model amplitude computed from the VP rule
- `OBS_REF_AMP(fm)` : reference amplitude extracted from external literature sources
- `ERROR(%)` : percent error defined as `(CALC_AMP - OBS_REF_AMP) / OBS_REF_AMP * 100`
- `SOURCE_REF` : source category tag (see below)
- `STATUS` : `PASS` if within tolerance, else `FAIL*` (may include a failure reason suffix)

### Declared rule used in this dataset

The dataset header declares:

- `r_eff = r_vac / sqrt(P_idx)`
- `r_vac = 245.9 fm`
- gate tolerance: `±5%`

This DOI bundle includes a deterministic validator script that:

1. re-computes `CALC_AMP` from `(r_vac, P_IDX)`
2. re-computes `ERROR(%)`
3. verifies that `STATUS` matches the declared tolerance

**Important:** the dataset includes informational fields (`Z_AVG`, `R_COV_AVG(pm)`) which are not required to validate the numerical gate itself.

## Sources

This dataset is a **compiled extract** (not raw scans) referencing the following source families:

- `[1] CRC Handbook of Chemistry and Physics, 97th Ed.`
- `[2] NIST Atomic Spectra Database & CCCBDB`
- `[3] Pauling, L., "The Nature of the Chemical Bond", 1960.`
- `[4] Surface Science Reports (for metallic radii/constants)`

Because some sources (e.g., CRC) are copyrighted, the DOI bundle does **not** redistribute full source tables.
Instead, the bundle provides:

- a locked extracted dataset (this CSV)
- a deterministic validation script
- a gate report that records pass/fail statistics and explicit boundary cases

If you have institutional access to the source material, you can rebuild/extend this dataset by following the template in `docs/chem/EXTERNAL_INSPECTION_TEMPLATE.md`.

## Rebuilding / extending

To extend the dataset, add new rows following the same schema. Then run:

```bash
python3 04_vp_whitepaper/scripts/run_chem_external_inspection.py
```

This will regenerate:

- `04_vp_whitepaper/outputs/chem/external_inspection_summary.json`
- `04_vp_whitepaper/outputs/chem/table_external_inspection_summary.tex`
- `gate/reports/gate_report_chem_external_inspection.json`


## Traceability (chain-of-custody)

For a formal mapping of each `OBS_REF_AMP(fm)` value to an explicit raw source value and a declared conversion rule, see:

- `docs/chem/TRACEABILITY_SPEC.md`
- `data/chem/traceability_spec_v3.txt`
- `data/chem/traceability/traceability_table_v1.csv`
