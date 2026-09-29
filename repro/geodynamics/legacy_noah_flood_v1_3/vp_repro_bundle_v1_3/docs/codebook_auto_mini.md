# Codebook (auto, mini)

## R10_bulk_density_summary.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R10_bulk_density_summary.csv`
- rows: 1
- cols: 6

| column | inferred_type |
|---|---|
| Q1 | float |
| Median | float |
| Q3 | float |
| method | str |
| n | int |
| QC_flag | str |

## R10_compaction_curve.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R10_compaction_curve.csv`
- rows: 1
- cols: 6

| column | inferred_type |
|---|---|
| phi0 | float |
| c | float |
| z_min_m | int |
| z_max_m | int |
| reference | str |
| QC_flag | str |

## R10_seismic_summary.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R10_seismic_summary.csv`
- rows: 1
- cols: 8

| column | inferred_type |
|---|---|
| line_id | str |
| lat | float |
| lon | float |
| thickness_m | float |
| thickness_sigma_m | float |
| facies | str |
| method | str |
| QC_flag | str |

## R6_IntCal_Marine_combined.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R6_IntCal_Marine_combined.csv`
- rows: 4
- cols: 4

| column | inferred_type |
|---|---|
| calBP | int |
| C14_age | int |
| C14_sigma | int |
| curve_id | str |

## R7_DeltaR_Med_repro.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R7_DeltaR_Med_repro.csv`
- rows: 3
- cols: 9

| column | inferred_type |
|---|---|
| region | str |
| site | str |
| layer | str |
| marine_id | str |
| terr_id | str |
| deltaR | int |
| deltaR_sigma | int |
| window_ka | str |
| QC_flag | str |

## R8_RSL_repro.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R8_RSL_repro.csv`
- rows: 2
- cols: 11

| column | inferred_type |
|---|---|
| basin | str |
| site | str |
| datum | str |
| proxy | str |
| age_model | str |
| Age_BP | int |
| RSL_m | float |
| RSL_sigma | float |
| tectonic_corr | float |
| GIA_model | str |
| QC_flag | str |

## R9_SPD_repro.csv
- path: `data/mini/pf_whitepaper_v1_3_minidata_data/R9_SPD_repro.csv`
- rows: 2
- cols: 10

| column | inferred_type |
|---|---|
| lab_id | str |
| material | str |
| context | str |
| lat | float |
| lon | float |
| C14_age | int |
| C14_sigma | int |
| delta13C | float |
| curve | str |
| provenance | str |
