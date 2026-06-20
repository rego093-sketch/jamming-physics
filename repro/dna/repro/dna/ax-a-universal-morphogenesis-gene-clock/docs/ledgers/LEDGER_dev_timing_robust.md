# LEDGER — developmental-timing ROBUSTNESS, hardening n=10 (v8)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each open
item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (the claim was tested and is *not* established) · **[L]** locked
measured input.

## What this is
v7 (`LEDGER_dev_timing_wide.md`) widened the dev-timing test to **n = 10** and reported an honest null
with **ample power** (every predictor `[O]`; the exact-permutation **floor was lifted to 2.2e-6**, so
significance *was* reachable — the moderate positive composition trend got a fair test and still did not
pass). The v7 HANDOFF named the next clean feature as **MYF5 → first myotome** (n → 11). v8 does two
things, both honest and both add-only:

1. **Investigates MYF5/myotome from the primary literature** — and finds it **cannot be cleanly
   locked** (below). It is therefore **not added**, documented rather than forced.
2. Since the clean feature set is saturated at n = 10, **hardens the n = 10 null** by *verifying* two
   robustness properties the package asserts but never tested.

## MYF5 → myotome: investigated and NOT locked (the honest negative)
Under VP-SPEC C3 a locked stage must be a **genuine, citable, single-stage** measured input — never one
picked from an ambiguous range. MYF5/myotome fails that bar for two independent reasons, both from the
primary literature:

- **Gene/structure staging mismatch.** MYF5 is first expressed in the **dermomyotome**, *before* the
  myotome forms — Ott et al., *Development* 111:1097 (1991): "myf-5 sequences were first detected in the
  earliest somites … in the dermomyotome, **before formation of the dermatome, myotome and sclerotome**".
  The MYF5 protein literally precedes the structure it would be tagged to. The other ten `[V]` masters
  do not have this problem (each turns on in/at its named primordium).
- **No crisp single Carnegie stage.** The myotome's first appearance is **progressively distributed**
  (rostral somites differentiate before caudal; somite CS9+, dermomyotome rotation between CS11–12, the
  myotome thereafter), and the Carnegie literature gives no crisp single "myotome first appears at
  CS X" the way it does for, e.g., "upper limb bud first recognizable at stage 12" (O'Rahilly &
  Gardner). The first-myotome span across sources is **CS11–13**.

Locking MYF5 at a single CS would mean choosing one stage from an ambiguous range **and** papering over
the dermomyotome/myotome distinction — the tuning anti-pattern in disguise. So n stays at **10**.

The remaining 42-table candidates are likewise unsuitable as clean single-feature `[V]` masters with
crisp Carnegie staging: **EDAR/FOXN1/HOXC13 → hair** (first follicles are late/fetal, ~week 9–12, soft);
**MSX1 → tooth** (redundant with PAX9, same structure/stage); **BMP4 → beak/jaw/feather** (pleiotropic,
no single clean human primordium); **LEF1 → hair/whisker/tooth/mammary** (multi-feature, `[F]`-like for
any one); **TYR/GLI3** (`[F]` effectors, not masters). **The clean `[V]`-master + crisp-Carnegie-stage
feature set is therefore saturated at n = 10**, and widening further requires either softer staging
(forbidden) or a different data modality (data-blocked). This saturation is itself a real finding.

## What v8 verifies instead: two robustness probes (no new inputs, no free parameters)
Both probes hold the **predictor values fixed** (they are sequence/table-derived) and vary only the
**target** (the locked stage vector) — exactly the right way to test target-encoding robustness. Both
reuse the validated DP exact-permutation engine; neither has any knob to tune.

### Probe 1 — stage ±1 ordinal robustness (verifies an asserted property)
`data/dev_timing.json`'s `_method` claims the rank test is "**robust to ±1-stage encoding
uncertainty**". v8 *tests* that: it perturbs each of the 10 locked stages by ±1 CS (one at a time — 20
perturbations) and re-runs both the γ/spinodal test and the 6-predictor battery.

**Result:** no predictor flips to `[V]` under any perturbation, and the **smallest perm p over all 20
perturbations is 0.119** — still far above the Bonferroni α = 8.3e-3. The `[O]` conclusion is **stable**
under the documented ±1 uncertainty. (Max |ρ| reached over all perturbations: 0.566.)

### Probe 2 — leave-one-out jackknife (rules out a one-feature artifact)
Drop each feature in turn (n = 9) and re-run the battery. **Result:** no predictor flips to `[V]` in any
of the 10 folds, and **every fold retains power** (its exact-permutation floor ≤ 2.2e-5 < α, so each
fold genuinely *could* have detected a signal). The null is neither an artifact of one feature nor a
real signal masked by one outlier. Per-predictor ρ range across the 10 folds:

| predictor | ρ range across folds |
|---|---|
| gamma | [−0.445, −0.159] |
| gc | [−0.487, −0.176] |
| cpg_oe | [+0.176, +0.544] |
| **tata** | **[+0.393, +0.830]** |
| gcbox | [−0.680, −0.291] |
| caat | [+0.245, +0.665] |

The most striking fold: **dropping `tooth_germ`** (CS18, the latest feature, "out of order" relative to
its low γ) lifts `tata` to **ρ = +0.830** with raw perm p = 0.024 — yet Bonferroni (×6 = 0.143) keeps it
`[O]`. So even the *most favorable* subset for the composition trend does not survive honest
multiple-testing correction. This is the cleanest possible statement of the null: the positive trend is
direction-real and feature-sensitive, but never significant.

### Falsifiability — the robustness procedure is not blind
A synthetic predictor comonotone with the base stages (ρ = 1.000, perm p ≈ 0) **flips to `[V]` at n = 10
AND in every jackknife fold**. So the no-flip result for the real predictors is a **true negative**, not
a dead procedure.

## The result (reported, not tuned)
The **n = 10 every-predictor-`[O]` null is ROBUST** — stable under ±1 stage uncertainty and to
leave-one-out feature removal, with power retained throughout, and the machinery provably detects a real
signal when one is present. Proximal-promoter composition does not predict Carnegie staging order, and
this conclusion does not hinge on the exact stage encoding or any single feature.

## Files (this item)
- `code/dev_timing_robust.py` — the two robustness probes + positive control + locked-input consistency.
- `code/verify_dev_timing_robust.py` — the gate (PASS 5/5).
- `repro/morpho/expected/dev_timing_robust_verify.json` — frozen fidelity baseline.

`verify_all.py` GATES extended to **8**; the suite is now **PASS 10/10** (8 gates 5/5 + source pin drift
0 + 8 fidelity baselines leaf drift 0). `expected_sha256.json` pins **51** files (was 49; +2 code).
**No new measured input, no new feature, no engine edit.**

## Invariants added this session
- `verify_dev_timing_robust.py` enforces: stage ±1 perturbation flips no predictor to `[V]` and never
  drives any perm p below the Bonferroni α; leave-one-out flips no predictor and every fold retains
  power; the positive control (synthetic comonotone) **does** flip (non-blind); the analysis runs on the
  exact locked n = 10 inputs (original 7 bit-identical, 3 appended, stage shas frozen) with the predictor
  matrix bit-identical to `dev_timing_wide`'s. If any of these breaks, the robustness claim is void.

## NEXT from here (obstacles named)
1. **Widening n further is blocked by input quality, not effort.** MYF5/myotome and the remaining
   42-table genes are too soft/fetal/redundant/pleiotropic to lock cleanly (above). A genuinely new
   `[V]`-master feature would need a primordium with a crisp single Carnegie stage *and* a master gene
   whose onset coincides with it — none remains in the current table. **Obstacle**: this requires either
   a new curated master→primordium pair with textbook-crisp staging, or a larger measured γ table.
2. **[O] data modality remains the main scientific lever** (unchanged from v7): expression-onset or
   chromatin-accessibility at the master loci, which would test a *different measured quantity* rather
   than more of the same promoter composition. **Obstacle**: needs an external developmental atlas added
   as a *locked* input; none is in the package, so it stays data-blocked.
3. Standing items unchanged: life-course kg/BMI calibration (`[O]`); person-specific depot map (`[F]`);
   GWAS sign/magnitude; size law on a real scan; `[F]→[V]` upgrades.
