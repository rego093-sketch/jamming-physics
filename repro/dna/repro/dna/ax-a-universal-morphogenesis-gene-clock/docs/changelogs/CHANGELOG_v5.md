# CHANGELOG — v5

Built on **neuro_emergence_chain_integrated v1.9** governance (VP-SPEC C3: every constant is a
measured input or a derived value, never tuned). Two **add-only** deliverables; **no engine edits**,
no fork of `organism/core.py`. **All five gates PASS 5/5.**

## Added

### 1 · Developmental-timing calibration — *an honest null result*
Tests the framework's central open claim: does measured promoter-stiffness γ predict real
human-embryo (Carnegie) staging?

- `code/dev_timing.py` — `load_dev_timing`, `derived_schedule(γ)`, `calibrate(γ)` (Spearman ρ, exact
  n!=5040 permutation p, Pearson; **grade set by evidence**: [V] iff `perm_p<0.05 AND ρ>0` else [O]),
  `apparatus_detects_signal` (synthetic γ∝stage → ρ=1.0, proves the test isn't blind),
  `stages_independent_of_gamma` (anti-back-fit), `write_results`.
- `code/data/dev_timing.json` — **[L] locked, cited** first-appearance Carnegie stages of 7 master
  features (PAX2, PAX6, TBX5, LHX2, TBX4, HOXD13, PAX9); O'Rahilly & Müller / Larsen's / UNSW Hill;
  frozen by sha256.
- `code/verify_dev_timing.py` — 5-check gate enforcing **grade == evidence** → **PASS (5/5)**.
- `LEDGER_dev_timing.md` — quantity-by-quantity grading.

**Result:** ρ(spinodal, observed CS) = **−0.018**, exact permutation p = **0.986**. Measured promoter
stiffness γ is **not** the molecular correlate of developmental timing. The order claim is downgraded
from an *untested hedge* to a *measured [O]* (tested-and-not-matching) — a **stronger, more honest**
position. Nothing was tuned to soften this; surfacing it is the governance working as intended.

### 2 · Life-course coupling — gene clock (TIME) × adipose (ENERGY) = one continuous fold
Runs the developmental time axis and the adipose energy axis **together on one genome**.

- `code/life_course.py` — `assert_one_continuous_fold` (both folds == body fold, 2.2e-16), `DevTarget`
  (gene-clock body frozen at τ as a point-sampleable SDF; at τ=1 → full lean target), `LifeCourse`
  (`trajectory`, `baseline_preserved`, `sampler`), `default_life` (infant→child→adolescent→adult-lean
  →surplus→heavy).
- `code/demo_life_course.py` — renders `results/life_course_face.png` and `life_course_body.png`
  (reuses `demo_adipose`'s render path), writes `results/life_course.json`.
- `code/verify_life_course.py` — 5-check gate (one fold; measured-γ identity; monotone A↑/occupancy↑;
  baseline preserved bit-for-bit; determinism) → **PASS (5/5)**.
- `LEDGER_life_course.md` — quantity-by-quantity grading.

**Headline:** child → adult → heavier adult is **one R19 switch**, expressed first in time then in
energy. At the lean reference α≡0 and the inflated field equals the pure gene-clock field
**bit-for-bit**, so Layer-3 convergence is untouched.

## Changed (docs only)
- `README.md` — v5 banner; new **v5** section (both deliverables); life-course figures added to the
  results table; **the v3 "developmental timing not claimed" note updated** to record that v5 tested
  it and found a null; run commands extended.
- `HANDOFF.md` — NEXT #1 (timing calibration) marked **DONE (honest null)**; Layer-4 NEXT #4
  (couple to time clock) marked **DONE**; new v5 session update + v6 NEXT list + new invariants.

## Unchanged / preserved (enforced by gates)
- The engine, the R19 switch, the measured γ tables (42-gene morpho, 59-gene obesity — the 42
  bit-identical inside the 59), the emergence order, and the Layer-3 convergence proof are all
  preserved bit-for-bit. The three prior gates (`verify_gene_clock`, `verify_morpho_plus`,
  `verify_adipose`) were re-run and stay **5/5**.

## Gate suite (v5)
```
verify_gene_clock    PASS (5/5)
verify_morpho_plus   PASS (5/5)
verify_adipose       PASS (5/5)
verify_dev_timing    PASS (5/5)   <- new
verify_life_course   PASS (5/5)   <- new
```
