# LEDGER — developmental-timing PREDICTOR BATTERY (v6 #1)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each open
item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (the claim was tested and is *not* established) · **[L]** locked
measured input.

## What this is
v5 (`LEDGER_dev_timing.md`) put the package's central order claim at risk and reported an **honest
null**: measured promoter-stiffness γ does **not** predict the order in which 7 genuine-master
features first appear in the human embryo (Spearman ρ = −0.018, exact-permutation p = 0.986). γ is
only *one* molecular quantity readable from those same promoters. v6 #1 asks the obvious next
question with the **same apparatus and zero tuning**:

> Keep the locked Carnegie stages and the exact-permutation Spearman test. **Swap the input
> variable.** Does a *different* measured promoter quantity predict the staging order?

The grade for each predictor is set **by its own evidence**. This is the governance's whole purpose:
a battery of candidate predictors is put at risk of falsification, and whatever comes out is reported.

## The battery (fixed a priori, never tuned to the stages)
Tested against the SAME locked 7-feature stage vector (`data/dev_timing.json`):

`otic_placode/PAX2/CS9 · optic_vesicle/PAX6/CS10 · upper_limb_bud/TBX5/CS12 ·
olfactory_placode/LHX2/CS13 · lower_limb_bud/TBX4/CS13 · digital_rays/HOXD13/CS17 ·
tooth_germ/PAX9/CS18`

| predictor | what it measures | source |
|---|---|---|
| `gamma` | NN promoter stacking stiffness | **locked** `morpho_gamma.json` (re-confirms v5) |
| `gc` | G+C fraction | **locked** `morpho_gamma.json` |
| `cpg_oe` | CpG observed/expected ratio | computed from promoter sequence |
| `tata` | TATA-box (`TATAAA`) density / kb | computed from promoter sequence |
| `gcbox` | GC-box / Sp1 (`GGGCGG`) density / kb | computed from promoter sequence |
| `caat` | CAAT-box (`CCAAT`) density / kb | computed from promoter sequence |

Each motif is the canonical core consensus, fixed **before** any correlation was seen, counted on
both strands as overlapping occurrences per kb. Promoter **length** is *not* a predictor: the window
is a fixed TSS−2000..+500 (2501 bp) for all 7 genes, so length has zero variance and is degenerate.

`gamma` and `gc` are read **verbatim** from the locked measured table — never recomputed here — so
the `gamma` column is bit-identical to v5's. (Self-check `gamma_matches_dev_timing` confirms its rank
correlation equals dev_timing's spinodal ρ exactly, since `spinodal` is strictly monotone in γ.)

## The result (the headline of this ledger)
**No predictor passes.** K = 6, Bonferroni α = 0.05/6 = 0.00833:

| predictor | Spearman ρ | exact perm p | Bonferroni p | positive? | grade |
|---|---|---|---|---|---|
| `gamma`  | −0.018 | 0.986 | 1.000 | no  | **[O]** |
| `gc`     | −0.108 | 0.821 | 1.000 | no  | **[O]** |
| `cpg_oe` | +0.432 | 0.329 | 1.000 | yes | **[O]** |
| `tata`   | +0.399 | 0.476 | 1.000 | yes | **[O]** |
| `gcbox`  | −0.624 | 0.144 | 0.867 | no  | **[O]** |
| `caat`   | +0.468 | 0.292 | 1.000 | yes | **[O]** |

**Conclusion:** measured proximal-promoter **composition** — not merely stiffness — is **evidently
not** the molecular correlate of human developmental timing for these features. This **widens** the
v5 null from "γ" to "γ + GC + CpG o/e + the three core promoter motifs". Overall grade: a measured
**[O]**, *tested and not matching* — the honest, stronger position, not a hedge.

## Power: what n = 7 can and cannot say (disclosed, not buried)
With n = 7 and the single tie in the stage vector (two CS13 features), the **exact-permutation
floor** — the smallest p *any* predictor could possibly reach — is **0.00079** (best achievable
|ρ| = 0.991 over the 5040 orderings). Because 0.00079 < α = 0.00833, Bonferroni significance **was
reachable**: this is a real null on a live test, not a dead apparatus. But the bar is a *near-perfect*
monotone predictor, which is a very high standard at this n. The best observer here (`cpg_oe`,
uncorrected p = 0.329) is nowhere near it.

Honest nuance worth recording: three composition predictors (`cpg_oe`, `tata`, `caat`) show a
**moderate positive** rank trend (ρ ≈ +0.40 … +0.47) — a faint hint that higher CpG/motif density
*might* track later appearance — but none survives even the uncorrected test, let alone Bonferroni.
n = 7 simply cannot resolve an effect of that size. This is a motivation, not a finding.

## Quantity-by-quantity

| quantity | grade | basis |
|---|---|---|
| Carnegie stage vector (7 features) | **[L]** | locked, cited, γ-independent; sha256 frozen and **identical** to `dev_timing.json`'s pin |
| `gamma`, `gc` per gene | **[L]** | read verbatim from locked `morpho_gamma.json`; never recomputed |
| 4 promoter sequences (TBX5/TBX4/HOXD13/PAX9) | **[L]** | **byte-for-byte** copy of `morpho_promoters.cache.json` (gate-checked identical) |
| 3 promoter sequences (PAX2/PAX6/LHX2) | **[F]** | re-fetched once by the IDENTICAL pipeline and frozen; reproduce locked γ within assembly drift (below) |
| `cpg_oe`, `tata`, `gcbox`, `caat` per gene | **[V]** | deterministic composition of the frozen sequences with fixed a-priori definitions |
| "promoter composition predicts staging" | **[O]** | **tested and rejected** (all six predictors null); reported, not tuned |
| non-sequence predictors (expression onset, chromatin accessibility) | **[O]** | **data-blocked**: the developmental expression/accessibility atlas is not in the package |

## Provenance honesty: the re-fetch residuals
PAX2/PAX6/LHX2 have no in-package cached sequence (the sensory table stored only derived γ/gc), so
their promoters were re-fetched in 2026-06 by `fetch_morpho_gamma.py`'s exact pipeline. The re-fetch
reproduces the **locked** sensory values to within assembly-version drift:

| gene | |Δγ| vs locked | |Δgc| vs locked |
|---|---|---|
| LHX2 | 0.0000 | 0.0000 |
| PAX6 | 0.0000 | 0.0004 |
| PAX2 | 0.0003 | 0.0000 |

The largest residual (3–4 × 10⁻⁴) is **far below** the inter-gene γ spread (~0.14), confirming the
correct promoters; a wrong-gene fetch would drift by ≳10⁻². Per VP-SPEC C3 the locked γ/GC tables are
**never overwritten** — these residuals are *recorded*, and the gate tolerates only this drift
(`tol = 5×10⁻³`, ~15× the largest residual and ~30× below a wrong-gene error), so it still catches a
genuine mis-fetch.

## Why this is not a failure
The no-tuning rule exists precisely so a result like this is surfaced rather than massaged. The
apparatus is provably non-blind: a synthetic predictor made comonotone with the stages scores
ρ = +1.000 at exact-permutation p = 0.0004, and a shuffle collapses it (self-check
`apparatus_detects_signal`). So the all-[O] battery is a **true** null. The package now *knows* — and
reports — that proximal-promoter sequence is an internal device, not a predictor of real staging.

## What this licenses next (honest open items)
1. **[O] widen the feature table (power).** n = 7 is the binding constraint. Add more unambiguous
   single-master features with defensible first-appearance stages to lift the permutation floor and
   give the moderate positive composition trend a fair test. *Obstacle: each new feature needs a
   genuine [V] master and a citable Carnegie stage.*
2. **[O] change data modality (data-blocked).** Developmental timing is more plausibly governed by
   *expression onset* / enhancer activity / chromatin accessibility than by proximal-promoter
   composition. Testing that needs an external developmental expression/accessibility atlas that is
   **not in the package** — so it stays [O] until that locked input is added.

## Gate (`verify_timing_predictors.py`, PASS = 5/5)
1. **GRADE == EVIDENCE** — each predictor's grade is [V] iff Bonferroni p < α and ρ > 0, else [O];
   overall grade consistent.
2. **LOCKED INPUTS** — stage sha256 frozen & equal to dev_timing's; 4 copied sequences byte-identical;
   3 fetched reproduce locked γ within tol; γ rank correlation equals dev_timing's.
3. **FALSIFIABILITY** — the battery detects a comonotone signal (ρ→1, p < 0.05) and collapses on a
   shuffle → true null.
4. **NO-TUNING MOTIFS + POWER** — every motif equals its fixed a-priori string; Bonferroni applied;
   the exact-permutation floor is computed and its reachability disclosed.
5. **DETERMINISM** — two `calibrate()` runs → identical result sha256.
