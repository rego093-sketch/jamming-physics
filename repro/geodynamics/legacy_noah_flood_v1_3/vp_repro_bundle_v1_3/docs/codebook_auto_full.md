# Codebook (auto, full)

## coast_line.csv
- path: `data/full/datasets_v1_2/A_coastline/coast_line.csv`
- rows: 4
- cols: 5

| column | inferred_type |
|---|---|
| id | str |
| age_Ma | int |
| shoreline_type | str |
| quality_flag | int |
| coastline_buffer_km | float |

## leafwax_dD_master.csv
- path: `data/full/datasets_v1_2/B_isotopes/leafwax_dD_master.csv`
- rows: 4
- cols: 11

| column | inferred_type |
|---|---|
| site | str |
| formation | str |
| member | str |
| lat_dd | float |
| paleolat_dd | float |
| age_model | str |
| sample_type | str |
| dD_C29_permil_VSMOW | float |
| dD_sigma | float |
| d18O_carb_permil_VPDB | float |
| qc_flag | int |

## raw_data.csv
- path: `data/full/datasets_v1_2/C_coal_geochem/raw_data.csv`
- rows: 4
- cols: 10

| column | inferred_type |
|---|---|
| basin | str |
| site | str |
| core_id | str |
| depth_m | float |
| seam_id | str |
| TOC_wt_pct | float |
| Tmax_C | int |
| HI_mgHCgTOC | int |
| VCr_ratio | float |
| qc_flag | int |

## bone_histology.csv
- path: `data/full/datasets_v1_2/DINO_THERM/bone_histology.csv`
- rows: 8
- cols: 6

| column | inferred_type |
|---|---|
| Specimen_ID | str |
| Genus | str |
| Location | str |
| Bone_Element | str |
| Primary_Tissue_Type | str |
| LAGs_Present | int |

## cranial_CT_metrics.csv
- path: `data/full/datasets_v1_2/DINO_THERM/cranial_CT_metrics.csv`
- rows: 4
- cols: 5

| column | inferred_type |
|---|---|
| Specimen_ID | str |
| Genus | str |
| Cranial_Feature | str |
| Internal_Surface_Area_m2 | float |
| Functional_Interpretation | str |

## aDNA_QC_summary.csv
- path: `data/full/datasets_v1_2/PF_pack/aDNA_QC_summary.csv`
- rows: 5
- cols: 5

| column | inferred_type |
|---|---|
| Sample_ID | str |
| Species | str |
| Coverage | float |
| Damage_Rate_5prime | float |
| Fragment_Length_Mean | float |

## contamination_checks.csv
- path: `data/full/datasets_v1_2/PF_pack/contamination_checks.csv`
- rows: 4
- cols: 6

| column | inferred_type |
|---|---|
| Sample_ID | str |
| mtDNA_Contamination_Rate | float |
| mtDNA_CI | str |
| X_Chromosome_Reads | int |
| Y_Chromosome_Reads | int |
| Sex_Check_Result | str |

## coverage_match_report.csv
- path: `data/full/datasets_v1_2/PF_pack/coverage_match_report.csv`
- rows: 2
- cols: 6

| column | inferred_type |
|---|---|
| Comparison_Group | str |
| Subsampling_Strategy | str |
| Target_Coverage | int |
| Final_Mean_Coverage_Group1 | float |
| Final_Mean_Coverage_Group2 | float |
| Notes | str |

## human_MC1R_directionality_summary.csv
- path: `data/full/datasets_v1_2/PF_pack/human_MC1R_directionality_summary.csv`
- rows: 1
- cols: 5

| column | inferred_type |
|---|---|
| Analysis | str |
| Metric | str |
| Coefficient | float |
| P_Value | float |
| Notes | str |

## human_pigment_freq_by_region_time.csv
- path: `data/full/datasets_v1_2/PF_pack/human_pigment_freq_by_region_time.csv`
- rows: 6
- cols: 5

| column | inferred_type |
|---|---|
| Time_Bin | str |
| Region | str |
| Allele | str |
| Frequency | float |
| Std_Error | float |

## human_pigment_variants.tsv
- path: `data/full/datasets_v1_2/PF_pack/human_pigment_variants.tsv`
- rows: 9
- cols: 9

| column | inferred_type |
|---|---|
| Sample_ID | str |
| Accession | str |
| Species | str |
| Site | str |
| Age_BP | int |
| rsID | str |
| Allele_1 | str |
| Allele_2 | str |
| DP | int |

## mammoth_LOF_burden_tests.csv
- path: `data/full/datasets_v1_2/PF_pack/mammoth_LOF_burden_tests.csv`
- rows: 4
- cols: 7

| column | inferred_type |
|---|---|
| Gene | str |
| Group | str |
| LOF_Variant_Count | int |
| Total_Samples | int |
| P_Value | float |
| Odds_Ratio | float |
| Normalization_Rule | str |

## mammoth_elephant_diff_coding.csv
- path: `data/full/datasets_v1_2/PF_pack/mammoth_elephant_diff_coding.csv`
- rows: 3
- cols: 6

| column | inferred_type |
|---|---|
| Gene | str |
| Protein_Change | str |
| Functional_Domain | str |
| Predicted_Effect | str |
| Tool | str |
| Tool_Version | str |

## mammoth_gene_variants.tsv
- path: `data/full/datasets_v1_2/PF_pack/mammoth_gene_variants.tsv`
- rows: 6
- cols: 1

| column | inferred_type |
|---|---|
| Sample_ID,Species,Gene,Position,Ref_Allele,Alt_Allele,Effect,PROVEAN_Score | str |

## sedadna_angiosperm_fraction.csv
- path: `data/full/datasets_v1_2/PF_pack/sedadna_angiosperm_fraction.csv`
- rows: 11
- cols: 9

| column | inferred_type |
|---|---|
| Core_ID | str |
| Layer_ID | str |
| Age_BP | int |
| CI_Lower_BP | int |
| CI_Upper_BP | int |
| Read_Count | int |
| Angiosperm_Fraction | float |
| Bootstrap_CI_Lower | float |
| Bootstrap_CI_Upper | float |

## sedadna_metadata_min.csv
- path: `data/full/datasets_v1_2/PF_pack/sedadna_metadata_min.csv`
- rows: 3
- cols: 8

| column | inferred_type |
|---|---|
| Core_ID | str |
| Site | str |
| Country | str |
| Lat | float |
| Lon | float |
| Primer_Set | str |
| Reference_DB | str |
| Reference_DB_Version | str |

## leaf_cuticle_SI.csv
- path: `data/full/datasets_v1_2/PLANT_E1E2/leaf_cuticle_SI.csv`
- rows: 5
- cols: 6

| column | inferred_type |
|---|---|
| 표본_ID | str |
| 속 (유사종) | str |
| 위치 | str |
| 기공_지수_% | float |
| 잎_가장자리_유형 | str |
| 물방울_끝_존재 | int |

## tree_rings.csv
- path: `data/full/datasets_v1_2/PLANT_E1E2/tree_rings.csv`
- rows: 4
- cols: 5

| column | inferred_type |
|---|---|
| 표본_ID | str |
| 속 (유사종) | str |
| 위치 | str |
| 평균_나이테_폭_mm | float |
| 나이테_경계_정의 | str |

## Nile_early_strata.csv
- path: `data/full/datasets_v1_2/R10_Nile/Nile_early_strata.csv`
- rows: 6
- cols: 2

| column | inferred_type |
|---|---|
| Years_After_Event_t0 | int |
| Deposited_Thickness_m | float |

## bulk_density_summary.csv
- path: `data/full/datasets_v1_2/R10_Nile/bulk_density_summary.csv`
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

## compaction_curve.csv
- path: `data/full/datasets_v1_2/R10_Nile/compaction_curve.csv`
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

## global_delta_CI_100yr.csv
- path: `data/full/datasets_v1_2/R10_Nile/global_delta_CI_100yr.csv`
- rows: 8
- cols: 3

| column | inferred_type |
|---|---|
| Years_After_Event_t0 | int |
| Global_Discharge_Gt_per_yr_Lower_CI | int |
| Global_Discharge_Gt_per_yr_Upper_CI | int |

## nile_core_map.csv
- path: `data/full/datasets_v1_2/R10_Nile/nile_core_map.csv`
- rows: 3
- cols: 5

| column | inferred_type |
|---|---|
| Years_After_Event_t0 | int |
| Core_ID | str |
| Deposited_Thickness_m | float |
| Thickness_Uncertainty_m | float |
| Estimated_Areal_Extent_km2 | int |

## seismic_profile_summary.csv
- path: `data/full/datasets_v1_2/R10_Nile/seismic_profile_summary.csv`
- rows: 2
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

## IntCal20_Marine20_full_raw.csv
- path: `data/full/datasets_v1_2/R6_IntCal_Marine/IntCal20_Marine20_full_raw.csv`
- rows: 8
- cols: 4

| column | inferred_type |
|---|---|
| calBP | int |
| C14_age | int |
| C14_sigma | int |
| curve_id | str |

## IntCal20_NH_raw.csv
- path: `data/full/datasets_v1_2/R6_IntCal_Marine/IntCal20_NH_raw.csv`
- rows: 4
- cols: 4

| column | inferred_type |
|---|---|
| calBP | int |
| C14_age | int |
| C14_sigma | int |
| curve_id | str |

## Marine20_raw.csv
- path: `data/full/datasets_v1_2/R6_IntCal_Marine/Marine20_raw.csv`
- rows: 4
- cols: 4

| column | inferred_type |
|---|---|
| calBP | int |
| C14_age | int |
| C14_sigma | int |
| curve_id | str |

## DeltaR_intake.csv
- path: `data/full/datasets_v1_2/R7_DeltaR_Med/DeltaR_intake.csv`
- rows: 3
- cols: 7

| column | inferred_type |
|---|---|
| region | str |
| site | str |
| layer | str |
| deltaR | int |
| deltaR_sigma | int |
| window_ka | str |
| QC_flag | str |

## RSL_intake.csv
- path: `data/full/datasets_v1_2/R8_RSL/RSL_intake.csv`
- rows: 4
- cols: 8

| column | inferred_type |
|---|---|
| basin | str |
| site | str |
| datum | str |
| Age_BP | int |
| RSL_m | float |
| tectonic_corr | float |
| GIA_model | str |
| QC_flag | str |

## Australia1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Australia1.csv`
- rows: 9
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## Crete1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Crete1.csv`
- rows: 9
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## Cyprus1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Cyprus1.csv`
- rows: 8
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## Greece1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Greece1.csv`
- rows: 9
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## Israel1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Israel1.csv`
- rows: 8
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## Japan1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Japan1.csv`
- rows: 9
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## NewZealand1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/NewZealand1.csv`
- rows: 10
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## Turkey1.csv
- path: `data/full/datasets_v1_2/R8_RSL/sites_plus/Turkey1.csv`
- rows: 7
- cols: 4

| column | inferred_type |
|---|---|
| Age_BP | int |
| RSL_m | float |
| Uncertainty_m | float |
| Note | str |

## C14_intake.csv
- path: `data/full/datasets_v1_2/R9_SPD/C14_intake.csv`
- rows: 2
- cols: 8

| column | inferred_type |
|---|---|
| lab_id | str |
| material | str |
| context | str |
| lat | float |
| lon | float |
| C14_age | int |
| C14_sigma | int |
| QC_flag | str |
