# CHANGELOG — universal_morphogenesis_geneclock v8

Built on neuro_emergence_chain_integrated v1.9 (VP-SPEC C3 no-tuning governance).
**Add-only, no engine edits, no fork of `organism/core.py`, NO new measured input, NO new feature.**
Unified entry `verify_all.py` now **PASS 10/10** (eight gates 5/5 + sha256 source/measured-input pin
drift 0 + eight fidelity baselines leaf drift 0).

## v8 — harden the n=10 developmental-timing null (robustness), and document the MYF5 dead-end

v7 widened the dev-timing test to n=10 and reported an honest null with ample power (every predictor
[O]; exact-permutation floor lifted to 2.2e-6). The v7 HANDOFF named MYF5 → first myotome (n→11) as the
next clean feature. v8 investigates it, finds it cannot be cleanly locked, and instead hardens the n=10
result.

### MYF5 → myotome: investigated from the primary literature and NOT locked
A locked stage must be a genuine, citable, single-stage measured input — never one picked from an
ambiguous range. MYF5/myotome fails for two independent reasons:
- **Gene precedes structure.** MYF5 is first expressed in the *dermomyotome*, before the myotome forms
  (Ott et al., Development 1991: "myf-5 … first detected in the earliest somites … in the dermomyotome,
  before formation of the dermatome, myotome and sclerotome"). The other ten [V] masters turn on at
  their named primordium; MYF5 would not.
- **No crisp single stage.** First-myotome appearance is progressively distributed (somite CS9+,
  dermomyotome CS11–12, myotome after), spanning CS11–13 across sources; the Carnegie literature gives
  no single "myotome at CS X" the way it does for the limb buds.

Locking it would mean choosing one stage from a range AND papering over the dermomyotome/myotome
distinction — disguised tuning. So n stays at 10. The remaining 42-table genes (EDAR/FOXN1/HOXC13 →
hair [late/fetal], MSX1 → tooth [redundant], BMP4 [pleiotropic], LEF1 [multi-feature], TYR/GLI3 [F]) are
likewise unsuitable. **The clean [V]-master + crisp-Carnegie-stage set is saturated at n=10** — itself a
real finding.

### What v8 verifies instead (two robustness probes; predictor values fixed, only the stage target varies)
- **Stage ±1 ordinal robustness.** dev_timing.json's _method *claims* the rank test is "robust to
  ±1-stage encoding uncertainty"; v8 *tests* it. Perturbing each of the 10 stages by ±1 CS (20
  perturbations) flips no predictor to [V], and the smallest perm p over all is **0.119** (≫ Bonferroni
  α=8.3e-3). The [O] conclusion is stable under the documented uncertainty.
- **Leave-one-out jackknife.** Dropping any single feature (n=9) flips no predictor to [V], and every
  fold retains power (floor ≤ 2.2e-5 < α). The most favorable fold (drop tooth_germ) lifts tata to
  ρ=+0.830, raw perm p=0.024 — but Bonferroni (×6=0.143) keeps it [O]. Even the best subset for the
  composition trend fails honest correction.
- **Non-blind control.** A synthetic comonotone predictor (ρ=1.000) flips to [V] at n=10 and in every
  fold → the no-flip result is a true negative.

### Result (reported, not tuned)
The n=10 every-predictor-[O] null is **ROBUST**: stable under ±1 stage uncertainty and to single-feature
removal, power retained throughout, machinery provably non-blind. Proximal-promoter composition does not
predict Carnegie staging order, and this does not hinge on the exact stage encoding or any one feature.

### New gate, new files
New gate: **`verify_dev_timing_robust`** (PASS 5/5) → gate suite is now **eight gates**.
New files:
- `code/dev_timing_robust.py` (two robustness probes + positive control + locked-input consistency)
- `code/verify_dev_timing_robust.py` (the gate)
- `LEDGER_dev_timing_robust.md`, `CHANGELOG_v8.md`
- `repro/morpho/expected/dev_timing_robust_verify.json` (new fidelity baseline)

`expected_sha256.json` now pins **51** files (was 49; +2 code, no new data). All seven prior gates
remain 5/5, untouched.

---
