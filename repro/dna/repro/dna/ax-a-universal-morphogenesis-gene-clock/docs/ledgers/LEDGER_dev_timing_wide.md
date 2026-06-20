# LEDGER — developmental-timing WIDE test, n→10 (v7 #2)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each open
item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (the claim was tested and is *not* established) · **[L]** locked
measured input.

## What this is
v5 (`LEDGER_dev_timing.md`) reported an **honest null**: measured promoter-stiffness γ does **not**
predict the order in which 7 genuine-master features first appear in the human embryo (Spearman
ρ = −0.018, exact-permutation p = 0.986). v6 (`LEDGER_timing_predictors.md`) widened that null from
*stiffness* to *proximal-promoter composition* — a 6-predictor battery (γ, GC, CpG o/e, TATA/GC-box/
CAAT density), **every predictor [O]** — and named the binding limitation explicitly: at **n = 7** the
exact-permutation **floor was 7.9e-4**, the test's power ceiling, and the one moderately positive
composition trend (`cpg_oe`/`tata`/`caat`, ρ ≈ +0.40…+0.47) could not be resolved. v7 #2 does exactly
the named next step, with the **same apparatus and zero tuning**:

> Keep the locked Carnegie stages and the exact-permutation Spearman test. **Add more genuine
> [V]-master features** (n → 10) so the floor drops and the composition trend gets a fair test.

The grade for each test is set **by its own evidence**. Widening the table can only *help* a real
signal show up; it cannot manufacture one. Whatever comes out is reported.

## The three new features (each pinned from a primary source BEFORE any correlation)
Added on top of the locked 7 (`data/dev_timing.json`, loaded byte-for-byte and unchanged):

| feature | master | CS | primordium | source |
|---|---|---|---|---|
| `foxg1_cerebral_vesicle` | **FOXG1** | **14** | future cerebral hemispheres (telencephalic vesicle) | Müller & O'Rahilly 1988, **PMID 3377191** |
| `mitf_rpe_pigment` | **MITF** | **15** | retinal pigment epithelium, first melanisation | O'Rahilly & Müller; melanogenesis lit, **PMID 1927245** |
| `sox9_chondrification` | **SOX9** | **17** | first chondrification (cartilage of first elements) | O'Rahilly & Müller, **Publ. 637** (cond. CS16, chondrif. CS17–18) |

The full n = 10 stage vector is therefore
`[9, 10, 12, 13, 13, 14, 15, 17, 17, 18]` (the 7 locked stages, then the 3 new) — two tie-pairs
(13×2, 17×2). `approx_day` values are contextual only and never enter the rank test.

### Two documented scope corrections (FOXG1, SOX9): [F]→[V] for the *specific* feature
The broad morpho atlas tags **FOXG1** and **SOX9** as `[F]` because there they each stand in for a
whole vague program (`cranium`; `cartilage/skeleton+otic+feather`). For the **specific** features used
here they are the canonical **[V]** masters, and this is recorded, not applied silently:
- **FOXG1** is THE master telencephalon transcription factor for the cerebral hemispheres — it is
  literally the gene named in the title of the CS14 staging paper (PMID 3377191).
- **SOX9** is THE master chondrogenic TF (necessary + sufficient for chondrogenesis); for "first
  chondrification" it is unambiguously the master.
- **MITF** was already a `[V]` master in dev_timing's `V_MASTERS` (melanocyte/RPE master TF).

`dev_timing_wide.V_MASTERS_WIDE = DT.V_MASTERS ∪ {FOXG1, SOX9}`; the gate records the correction.

## Locked γ is never overwritten — the new masters reproduce it
γ and GC are read **verbatim** from the locked `morpho_gamma.json` (never recomputed for the schedule).
The new promoter cache (`data/dev_timing_ext_promoters.cache.json`) supplies **raw sequence only**, for
the composition predictors, and each new gene's frozen sequence is checked to reproduce the **locked**
γ/GC:

| gene | sequence source | recomputed γ | locked γ | residual |
|---|---|---|---|---|
| **MITF** | byte-for-byte copy of `morpho_promoters.cache.json` | 1.3945 | 1.3945 | **0** (exact) + byte-identical |
| **SOX9** | byte-for-byte copy of `morpho_promoters.cache.json` | 1.4598 | 1.4598 | **0** (exact) + byte-identical |
| **FOXG1** | re-fetched 2026-06, identical pipeline (NC_000014.9 +, TSS−2000..+500) | 1.4735 | 1.4737 | **2e-4** (≤ tol 5e-3) |

The FOXG1 residual (Δγ = 2e-4, ΔGC = 4e-4) is assembly-version drift — three orders of magnitude
below the inter-gene γ spread (~0.14) — so the correct promoter is confirmed without ever editing a
locked value.

## The exact-permutation engine (the technical heart of v7)
At n = 7 the apparatus brute-forced all 7! = 5 040 label permutations through `scipy` per predictor.
At n = 10 that is 10! = 3 628 800 per predictor × 6 predictors — far too slow that way. The key fact:

> Under the exact permutation null, Spearman ρ is an **affine function** of
> `S = Σ_i rank_x[i]·rank_y[perm][i]`. For any predictor with distinct values (rank vector a
> permutation of 1..n) the null distribution of ρ depends **only on the stage-rank multiset and n**.

So the exact null distribution of `S` is computed **once** by dynamic programming over the (tiny)
multiset of remaining stage ranks, and reused for every predictor and the floor. Predictor ties (e.g.
equal motif counts) are handled by giving that predictor its own rank multiset in the same DP. Ranks
are scaled ×2 so midranks are integers and the DP keys are **exact integers**; ρ is recovered from `S`
by the exact affine map (asserted equal to `scipy.spearmanr` to 1e-9 on the observed pairing, so the
`|ρ| ≥ |ρ_obs|` boundary is exact). Tied stage values are counted **with multiplicity** so the DP total
is exactly n! — matching a true exact permutation test. Runtime at n = 10: ~0.02 s.

**The engine is validated before it is trusted at n = 10** (gate check 3): the DP reproduces the v5
brute-force oracle (`DT._perm_p`, `scipy` per permutation) **bit-for-bit at n = 7 and n = 8** (both
tie structures, distinct-valued *and* tied probes), and an independent vectorised oracle at **n = 9**
(itself cross-checked against `scipy`-brute at n = 7). No unproven fast path reaches the n = 10 claim.

## The result (computed, reported whatever it is)
Widening to n = 10 **lifts the exact-permutation floor from 7.9e-4 to 2.2e-6** — Bonferroni
significance (α = 0.05/6 = 8.3e-3) is now **amply reachable**. With that power in hand:

| | ρ | exact perm p | Bonferroni p | grade |
|---|---|---|---|---|
| **γ / spinodal** (test 1) | −0.280 | 0.429 | — | **[O]** |
| `gamma` | −0.280 | 0.429 | 1.000 | [O] |
| `gc` | −0.311 | 0.379 | 1.000 | [O] |
| `cpg_oe` | +0.402 | 0.248 | 1.000 | [O] |
| `tata` | **+0.490** | 0.183 | 1.000 | [O] |
| `gcbox` | −0.434 | 0.215 | 1.000 | [O] |
| `caat` | +0.455 | 0.187 | 1.000 | [O] |

**Every test is [O].** The headline is *not* "still null because underpowered" — the floor (2.2e-6)
shows the test now has ample power. The moderate positive composition trend survived the widening
(`tata` ρ = +0.49, `caat` +0.46, `cpg_oe` +0.40) and got a fair test, and it **still does not reach
significance** (best raw perm p = 0.183). So this is a **real null at n = 10**, not a power artifact:
proximal-promoter composition does not predict Carnegie staging order even with the floor lifted. The
γ/spinodal test reconfirms the v5/v6 sign and null on the wider table. Reported, not tuned.

## Falsifiability (must keep passing or the null is meaningless)
- **Non-blind at n = 10**: a synthetic predictor comonotone with the stages scores ρ → 1.000 with
  exact perm p < 0.05; a shuffle collapses to ρ ≈ +0.09. The apparatus detects a real signal.
- **DP == oracle** on all probed cases at n = 7, 8 (brute-force) and n = 9 (vectorised).
- **Original 7 unchanged**: the first 7 features here are bit-identical to `dev_timing.json`
  (gene + stage), the 3 new are appended; stage sha for the 7 equals dev_timing's frozen sha.
- **New stages γ-independent**: perturbing the measured γ table moves no stage; the new stages are
  not a suspiciously perfect match to the γ order (|ρ| = 0.280 < 0.99 → not back-fitted).

## Files (this item)
- `code/dev_timing_wide.py` — the n = 10 dual test + the DP exact-permutation engine + self-checks.
- `code/verify_dev_timing_wide.py` — the gate (PASS 5/5): grade==evidence over both tests; locked
  inputs; falsifiability incl. DP-engine validation; no-tuning motifs + disclosed lifted floor;
  determinism.
- `code/data/dev_timing_ext.json` — the 3 new **locked** Carnegie stages (provenance + scope notes).
- `code/data/dev_timing_ext_promoters.cache.json` — MITF/SOX9 byte-for-byte copies + frozen FOXG1
  re-fetch (residuals recorded).
- `repro/morpho/expected/dev_timing_wide_verify.json` — frozen fidelity baseline.

`verify_all.py` GATES extended to **7**; the suite is now **PASS 9/9** (7 gates 5/5 + source pin
drift 0 + 7 fidelity baselines leaf drift 0).

## Invariants added this session
- `data/dev_timing_ext.json` is **frozen**: the 3 stages stay integer and γ-independent; never
  overwrite a locked γ/GC to chase a match.
- `data/dev_timing_ext_promoters.cache.json` is **frozen**: MITF/SOX9 sequences stay byte-identical
  to `morpho_promoters.cache.json` and reproduce the locked γ **exactly**; the FOXG1 sequence
  reproduces the locked γ within assembly-drift tol (5e-3).
- `verify_dev_timing_wide.py` enforces **grade == evidence** over both tests, Bonferroni correction,
  a-priori motifs, and the disclosed permutation floor (which must stay **below** the n = 7 floor of
  7.9e-4 — more features, more power, by construction).
- The **DP exact-permutation engine must keep matching** the brute-force/vectorised oracles at
  n = 7, 8, 9, and its non-blind self-test (synthetic comonotone → ρ = 1.0, perm p < 0.05) must keep
  passing, or the all-[O] null is meaningless.

## NEXT from here (obstacles named)
1. **More [V]-master features still helps** — the next clean candidate is **MYF5 → first myotome**,
   deliberately *excluded* from v7 (it would be n = 11) because its first-appearance staging is too
   soft for a locked input: the first myotome spans CS11–13 across sources (somite CS9, myotomal
   differentiation CS10–11, "myotomes fuse at 10.5–12 mm" in the Manual of Human Embryology).
   **Obstacle**: pin a single citable first-myotome CS *and* re-fetch + freeze the MYF5 promoter
   (reproducing its locked γ) before it can be added. Other pleiotropic/effector genes in the
   42-gene table are `[F]` for any single feature and would confound the test.
2. **[O] data modality** — proximal-promoter composition is now exhausted (all [O] at n = 10 with
   ample power). The remaining honest lever is a **different measured quantity**: expression-onset or
   chromatin-accessibility at the master loci. **Obstacle**: this needs an external developmental
   atlas added as a *locked* input; none is in the package, so the claim stays data-blocked.
3. Standing items unchanged: life-course kg/BMI calibration ([O]); person-specific depot map ([F]);
   GWAS sign/magnitude and the size law on a real scan; `[F]→[V]` upgrades.
