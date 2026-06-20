# Demonstration I - radiocarbon, the homogeneous case

Validates the leave-one-out reservoir correction (RMSE 418->141 yr on the
Elk Hills shell-charcoal series; 739->453 yr on the Lake Chichancanab
leaf-wax/macrofossil pairs). The reservoir/dead-carbon contaminant is
atomically homogeneous and invisible within a single date, so it is handled
by external offset correction and tested out-of-sample.

## Data (here)
- `data/real_case_FRE_shell_charcoal.csv` - Elk Hills (CA-KER-116) pairs.
- `data/real_case_Vindija_bone_pretreatments.csv` - Legacy/UF/HYP bone.
- `data/real_case_leafwax_macro_pairs.csv` - Lake Chichancanab pairs.

## Full pipeline
The hierarchical model + LOO driver ships in the companion radiocarbon
package: Zenodo doi:10.5281/zenodo.17718893 (R/Stan; `code/run_all.sh`). All final numbers are
recorded in the CSVs above so they can be recomputed independently.
