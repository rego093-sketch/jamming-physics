# External inspection dataset template

This template explains how to extend the bulk literature inspection dataset used in Sec.18.

## 1) Add a row

Append a new row to:

- `04_vp_whitepaper/data/chem/external_inspection/VP_STEP7_EXT_INSPECTION_FULL_V1.csv`

Data rows must match the header:

```text
ID,GROUP,FORMULA,Z_AVG,R_COV_AVG(pm),P_IDX,CALC_AMP(fm),OBS_REF_AMP(fm),ERROR(%),SOURCE_REF,STATUS
```

### Required fields

- `ID`: unique, stable identifier (e.g., `VP-C019`)
- `GROUP`: `Atom`, `Metal`, `Molecule`, `Complex`, `Solid`, or `Failure`
- `FORMULA`: a display label (e.g., `CO2`, `Fe2O3`, `NH3`)
- `P_IDX`: numeric pressure index used in your amplitude model
- `OBS_REF_AMP(fm)`: reference amplitude (external literature extraction)
- `SOURCE_REF`: coarse source tag (e.g., `[2] NIST`)

### Derived fields (recommended to compute programmatically)

Given the lock constant `r_vac = 245.9 fm`:

- `CALC_AMP(fm) = r_vac / sqrt(P_IDX)`
- `ERROR(%) = 100 * (CALC_AMP - OBS_REF_AMP) / OBS_REF_AMP`

Status convention:

- `PASS` if `abs(ERROR(%)) <= 5.0`
- otherwise `FAIL` or `FAIL_*` (optionally include a failure reason label)

## 2) Capture provenance

For each `OBS_REF_AMP(fm)` value, record a reproducible locator in your own notes (and ideally in a separate JSON sidecar in the DOI bundle):

- source family: NIST / CRC / book / journal
- dataset identifier / DOI / URL (if public)
- page / table / figure number
- measurement conditions (T, P, state, etc.)

The DOI bundle does not redistribute copyrighted scans, but provenance metadata should still be recorded.

## 3) Validate

Run:

```bash
python3 04_vp_whitepaper/scripts/run_chem_external_inspection.py
```

This will regenerate the summary table + gate report.

## 4) What counts as “good”

A stronger claim requires:

- reporting the full distribution (not only “PASS” examples)
- explicitly listing failures and boundary cases
- stable row IDs and stable source locators

