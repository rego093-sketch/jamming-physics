# Chapter 18 — Autism as a three-axis fault (T / O / W)

**Status (v1.32):** in-silico mechanism on the READ-ONLY engine cerebrum (`vp_mind_engine`,
tree `0fbf4988…`). **efficacy = 0 · not a diagnosis · NOT medical advice.**

## Claim verified
On the emerged cerebrum, autism is read as **three separable faults**, each with a distinct,
reproducible fingerprint in the pair **(ΔPAC, ignition fold)**:
- **T** (threshold / E-I): PAC down, ignition fold **raised**.
- **O** (output / catecholamine gain): PAC down, fold **normal**.
- **W** (long-range wiring): PAC **unchanged** (= health to precision), fold normal, with a
  local-over / long-range-under locality imbalance the other two lack.

A 17-gene moderate-ASD cohort (15 atlas + 2 live NCBI: GABRA5, MACROD2; γ via SantaLucia 1998,
window [TSS−2000, TSS+500]) partitions T(6)/O(7)/W(4); severe DEE/syndromic genes are
pre-registered excluded. *Which* fault any individual's autism is, is held **open**.

## Reproduce
```
cd ../_verify && python3 run_all_d9.py
```
Exit shows D9.0–D9.4 `repro=True tree=True pac=True honest=True`, engine byte-unchanged.
The three-axis partition + (ΔPAC, ignition) discriminant are D9.0 (`51ebcaf6…`) and the
mechanism discriminant module; see `_verify/autism_cohort_moderate_ncbi.py`,
`_verify/autism_mechanism_discriminant.py`.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1.
