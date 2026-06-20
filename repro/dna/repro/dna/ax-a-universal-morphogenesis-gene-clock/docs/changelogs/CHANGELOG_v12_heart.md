# CHANGELOG — v12 (single-organ deep dive: the heart)

**One line:** the heart's OWN developmental program is resolved into its crisp sub-stage milestones
and run through the SAME falsifiable gene-clock timing test — the fair, single-system version of the
v10 organ-timing test. Result: an **honest, robust [O] null**, sharper than the 8-organ one.
**Add-only, no engine edit.** `verify_all.py` **PASS 14/14**.

---

## Why v12

v10 tested "does measured DNA (promoter stiffness γ) predict organ-appearance timing?" across 8
visceral organs and returned an honest null (ρ=−0.414, p=0.360, [O]). But that test mixed
heterogeneous organs with only soft cross-system staging, leaving the objection: *maybe it failed
because the systems and staging were noisy, not because γ is the wrong predictor.*

The heart is the textbook gold standard for crisp human developmental staging. v12 does the **fair,
single-system** test: resolve the heart's own cascade into well-staged milestones and ask whether γ
predicts their order — on one coherent system, with full power disclosure.

## What v12 does

Resolves the heart into 8 crisp milestones, each tagged with its **canonical specifier master**, and
fetches each gene's **real γ** via the **identical** NCBI→SantaLucia pipeline (NKX2-5 reproduces the
`organ_atlas` value bit-for-bit — same pipeline guaranteed):

| milestone | specifier | observed CS |
|---|---|---|
| cardiac crescent / specification | NKX2-5 | 9 |
| heart-tube fusion | GATA4 | 10 |
| cardiac looping / RV | HAND2 | 11 |
| second heart field / OFT | ISL1 | 12 |
| chamber formation / identity | TBX5 | 13 |
| endocardial cushion / valve | SOX9 | 14 |
| ventricular septation | MEF2C | 15 |
| outflow-tract septation | TBX1 | 16 |

The model's sub-stage schedule is `argsort(spinodal(γ))` (same one switch, max|Δ|=2.2e-16). The test
reports Spearman ρ, Pearson r, and an **exact** permutation p (n=8 → n!=40320), with a ±1 CS jitter
robustness band and a non-blindness proof.

## Result — honest [O] null, sharper than v10

- **Spearman ρ = +0.0714**, **exact permutation p = 0.882** (two-sided, n!=40320), Pearson r = −0.030
  → grade **[O]**.
- **Vivid failure mode:** the cardiac master **NKX2-5** (first event in vivo, CS9) is ranked
  near-**last** by γ; **MEF2C** (late septation) is ranked **first** — γ gets the developmental
  anchors backwards.
- **Robust:** over 2000 ±1-CS jitter re-encodings, max ρ = 0.395 vs the ρ_crit = 0.714 needed for
  p<0.05 → **0%** reach significance. The null does not depend on staging round-off.
- **Non-blind:** a synthetic γ ordered to the stages gives ρ = +1.000 (a [V] **would** be reported if
  the data supported it); a shuffle gives mean|ρ| = 0.323. The [O] is a true negative, not a dead test.

**Conclusion:** promoter thermodynamic stiffness γ is **orthogonal to developmental timing — even
inside one tightly-regulated organ's own cascade.** This establishes the project's central
methodological result on the best-characterised single system with full power disclosure: γ fixes
*what/order* of structure deterministically **[V]**, but does **not** predict *when, vs biology*
**[O]**.

## New gate — `verify_heart_substages.py` (PASS 5/5)

1. **ONE SWITCH** — `gene_clock.spinodal == morpho_core.spinodal` (2.2e-16).
2. **LOCKED CITED INPUT** — `heart_substages.json` [L] provenance; every gene a cardiac master;
   integer stages; sha frozen; γ-independent & not back-fit (|ρ|<0.99). **Identical-pipeline
   guarantee:** heart-γ corr(γ,GC)=0.999 and NKX2-5 == `organ_gamma.json` value.
3. **GRADE == EVIDENCE** — order==argsort(spinodal); grade [V] iff (perm p<0.05 and ρ>0) else [O];
   **and** the null is robust (±1 jitter never reaches significance).
4. **FALSIFIABILITY** — synthetic-ordered γ → ρ→1; shuffle → small ⇒ true null.
5. **DETERMINISM** — two `calibrate()` runs → identical result sha.

## Files

- **New code:** `code/heart_substages.py`, `code/verify_heart_substages.py`.
- **New data (locked/cached):** `code/data/fetch_heart_gamma.py` (the fetch pipeline),
  `code/data/heart_gamma.json` (real cardiac-gene γ), `code/data/heart_promoters.cache.json`
  (cached sequences → γ reproduces offline), `code/data/heart_substages.json` (locked cited staging).
- **New docs:** `CHANGELOG_v12_heart.md`, `LEDGER_heart.md`, `HANDOFF_v12_heart.md`,
  `WHY_THE_NULL_AND_MODEL_LIMITS.md` (the interpretive thesis: why the null is principled, the
  endpoint-knowable / middle-distortable structure, and the ordinal-vs-systemic limit of a
  genomic-readout model), `repro/morpho/expected/heart_substages_verify.json`.
- **Gate suite:** 11 → **12 gates**. **Source pin:** 63 → **69 files** (+2 code, +1 fetch, +3 data).
- **Unchanged (verified, drift 0):** every governed v11 file is byte-identical — no engine edit, no
  fork, no change to the form/organ pipeline.

## Honest scope (grades in `LEDGER_heart.md`)

The one-specifier-per-milestone map is a forced choice **[F]** (cardiac TFs are pleiotropic;
documented). Staging is locked/cited/γ-independent **[L]**; γ is real/read-only **[L]**; the schedule
**order** is **[V]**; the timing-vs-biology claim is **[O]** (null). n=8 → power-limited (disclosed),
the same ceiling as the 8-organ test. The only lever to a positive result remains a different measured
modality (expression-onset / chromatin accessibility), which stays **[O] data-blocked**.

## Verify

```
python3 verify_all.py                    # OVERALL: PASS (14/14)   [see HANDOFF runtime note]
python3 code/heart_substages.py          # print the cardiac sub-stage test + honest null
python3 code/verify_heart_substages.py   # the gate alone -> PASS 5/5
python3 code/data/fetch_heart_gamma.py   # re-fetch/confirm real cardiac γ (offline from cache)
```
