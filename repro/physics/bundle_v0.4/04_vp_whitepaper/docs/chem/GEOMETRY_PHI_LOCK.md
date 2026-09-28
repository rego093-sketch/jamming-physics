# Geometry-classified dilution bounds (phi_eff) — LOCK note

## Purpose

To reduce "selection arbitrariness" in multi-atom (polyatomic) handling, we introduce a small, machine-checkable layer:

- fix (LOCK) a **geometry classifier** for a small set of representative polyatomic molecules;
- fix (LOCK) a **geometry-dependent upper bound** for the dilution factor phi_eff;
- mechanically verify that the Step7 dataset implies phi_eff values that do not violate those bounds.

This does **not** claim that every molecule is fully solved by a single closed-form geometric constant. It is a reproducibility / audit layer:

- "Given the dataset and a locked classifier, do representative molecules satisfy conservative geometric bounds?"

## Definitions

- Atomic pressure index values (P_idx(atom)) are taken from the Step7 external inspection CSV.

- For a molecule with stoichiometry {n_i}:

  P_avg_atom = (sum_i n_i * P_idx(atom_i)) / (sum_i n_i)

- The observed dilution factor in Step7 is then:

  phi_eff = P_idx(molecule) / P_avg_atom

Interpretation: phi_eff < 1 indicates an effective volumetric dilution / void-sharing relative to the stoichiometric average.

## Locked targets

- CH4 (tetrahedral)
- H2O (bent)
- NH3 (trigonal pyramidal)

These are selected because they are ubiquitous and commonly used as "stress tests" for polyatomic rules.

## Locked geometry upper bounds

We lock conservative upper bounds (not per-molecule fits):

- tetrahedral:  pi/(3*sqrt(2))  ≈ 0.74048
- bent:         3/4             = 0.75
- trigonal pyramidal: pi/4      ≈ 0.78540

These bounds are checked by the script:

- `04_vp_whitepaper/scripts/run_chem_geometry_phi.py`

and the results are exported for the paper as:

- `04_vp_whitepaper/outputs/chem/table_geometry_phi_bounds.tex`

## Why this helps (defense)

1) The classifier is fixed in a LOCK file (no hidden "choose geometry" freedom).

2) The constants are fixed and documented as upper bounds, preventing silent tuning.

3) The check is deterministic and leaves a gate report under `gate/reports/`.
