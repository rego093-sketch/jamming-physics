# Pathology findings — major integumentary diseases on the package's own mechanisms

**Package:** `integumentary_vp_site` · **module:** `repro/_pathology` · **as of:** v0.3.0
**Author:** Young Jae Lee (ORCID 0009-0002-7535-8245)
**Reproduce:** `python repro/run_pathology.py` → `reports/pathology_results.json`
**Governance:** VP-SPEC v1.8 (no new constants; 2×sha256 determinism; honest grading `[V]`/`[L]`/`[O]`).

This is a **research artifact**, not a written whitepaper. It does **not** touch the writing gate. The
core target battery (`repro/run_all.py`) is unchanged and remains the gate of record — its determinism
hash `1fb59f556e01…` is identical before and after this module was added.

---

## What was asked, and the constraint imposed

Address **all** of the diseases that fall to this package (the integumentary package per the framework
ownership contract, §6 of the master map) — their **fundamental mechanism** and their **treatment** —
and document them. The discipline taken: a disease may only **move a knob the package already has** (one
of the verified targets T1..T5 or the oncology kernel). No disease may add a constant, a basin, or a free
parameter, and each **intervention is the same knob reversed**. Where a cited absolute magnitude is not
derivable in-package, the disease **inherits the parent target's `[O]` obstacle**. The result is a test
of the **shape** the substrate forces — a direction, a threshold, a discontinuity, a fold — graded `[V]`,
against a cited clinical **direction** graded `[L]`.

**Ownership (master map §6).** This package owns the **acquired / multifactorial / dynamics-key** skin
diseases, and the **dynamics side** of borderline genetic ones (the gene-lesion fact itself is
`disease_wp`'s, imported by gene-key). Single-gene rare genodermatoses are **not** in this lane. The
coverage audit and the handoff of out-of-lane and not-yet-modelable conditions are in
`HANDOFF_NEXT_STEPS.md`.

---

## Result summary — 13 diseases, all pass

Every disease passes both a **clinical-sign** test (does the mechanism reproduce the cited
direction/threshold/discontinuity?) and an **intervention-reversal** test (does reversing the same knob
undo it?). Determinism is bit-identical across two runs.

| disease | parent target | substrate signature `[V]` | key readout | absolute `[O]` |
|---|---|---|---|---|
| atopic dermatitis | T1 | barrier **reserve** collapses with the chronic deficit | reserve 1.00 → 0.55 → 0.25; emollient → 0.90 | TEWL magnitude |
| contact dermatitis | T1 | **acute** insult crosses the discontinuous collapse | TEWL jumps ×20 at insult ≈ spinodal; repair → 1.0 | TEWL magnitude |
| ichthyosis | T1+T4 | shed time **diverges** near the spinodal (retention) | SC residence ×6.6; keratolytic resets | SC residence (days) |
| psoriasis | T4 | **threshold** + several-fold **autonomous** acceleration | held below spinodal (~28 d) → ×20.8 above; drug returns it | transit (days) |
| chronic / diabetic / pressure wound | T2 | non-closure **below** the package's own critical unjam drive | drive 0.15 critical: below → no closure | closure rate (µm·h⁻¹) |
| vitiligo | T3 | melanocyte viability lost **discontinuously** → melanin 0 | melanin 1.43 → 0; narrowband UVB → 1.43 | repigmentation dose |
| melasma / hyperpigmentation | T3 | melanin **regulated overshoot** (opposite pole of vitiligo) | melanin ×3.1 baseline; depigmenting → baseline | melanin OD |
| albinism (OCA) | T3→oncology | melanin **screen removed** raises carcinogenesis hazard | cancer hazard RR ×2.58; sunscreen → ×1.13 | incidence |
| hypohidrotic ectodermal dysplasia | T5 | capped sweat → danger band at **lower load** | core 4.60 vs 2.05 at load 2.5; cooling → 1.70 | set-point (°C) |
| primary hyperhidrosis | T5 | recruitment threshold **lowered** (opposite pole of HED) | sweat onset load 0.2 vs 0.3; therapy → dry | sweat rate |
| heat stroke | T5 | capacity **exceeded** → runaway above saturation | slope ×0.77 → ×2.0 past load 2.55; cooling → controlled | critical 40 °C |
| skin cancer (melanoma / SCC / BCC) | oncology | intermittent-vs-cumulative **dichotomy** + pigment-loss burst | melanoma intermittent RR 5.67; pigment-loss burst RR 10.59 | incidence & RR |
| actinic keratosis | oncology | SCC **precursor**: fewer multistage hits → far more prevalent | field prevalence 0.96 vs SCC 0.18 at same UV | prevalence/conversion |

---

## The headline — one switch, opposite drives, opposite clinic, zero tuning

The strongest single statement the module makes is the **opposite-sign discriminant**: the *same* R19
switch, driven with *opposite* signs, reproduces clinically *opposite* poles with **no new constant**.
Five checks now hold (`all_opposite_pairs_reproduced = true`), spanning **three different switches**:

1. **Turnover (T4 · TP63)** — psoriasis *accelerates* (autonomous advance past the spinodal) vs ichthyosis *retains* (shed time diverging at the spinodal).
2. **Barrier (T1 · KRT14)** — intact skin holds *full reserve* vs atopic skin's *collapsed reserve*.
3. **Melanin (T3 · MITF)** — melasma *overshoots* (melanin ×3.1) vs vitiligo *loses* it (melanin → 0). Same switch, opposite direction.
4. **Sweat (T5 · EDAR)** — hyperhidrosis *over-recruits* (onset load lowered, sweats at rest) vs HED *under-sweats* (capacity capped, overheats). Same switch, opposite direction.
5. **Photoprotection (T3 feedback)** — a healthy tan *attenuates* UV vs pigment loss leaving it *unattenuated*.

That a single bistable element, perturbed in opposite directions on three independent organ switches,
lands on the correct opposite clinical phenotypes — without any parameter chosen to make it so — is the
no-tuning content of the module.

---

## Two honest reframings (what the substrate does and does not say)

**Psoriasis is a threshold, not a fitted day-count.** In a deterministic bistable substrate you cannot
cross a barrier by relaxation; you can only slide once the barrier vanishes at the spinodal. So the
faithful psoriatic signature is: below the differentiation spinodal the basal cell is **held** (slow
homeostatic conveyor, ~28–40 d); at and above it it advances **autonomously**, and that advance time
falls **smoothly and ~20-fold** as the drive intensifies. That threshold + several-fold acceleration is
the `[V]` content. The **absolute transit in days** is **not** predicted (it inherits the T4 obstacle
`[O]`); the cited ~3–5 d vs ~28–40 d window is reported as the clinical **anchor** `[L]`, not back-fitted.

**Atopic dermatitis is a reserve collapse, not a TEWL multiple.** A small sub-spinodal standing deficit
barely moves the steady barrier state, so the baseline-TEWL number is uninformative (≈1.05×) and its
magnitude is the same `[O]` as T1. The faithful signature is the **dimensionless barrier reserve** — the
additional insult before the discontinuous collapse — which falls monotonically from ≈1.0 to ≈0.25 of the
spinodal as the deficit deepens. (Contact dermatitis is its acute complement: the *crossing event* itself.)

---

## Grades, in one line each

- **`[L]` clinical anchors** — the cited *direction* of each disease (barrier defect/flare; acute breach;
  retention; several-fold faster transit; failure to close; depigmentation; hypermelanosis; elevated
  cancer risk; heat intolerance; excessive sweating; heat-stroke runaway; intermittent- vs cumulative-UV
  cancer; precursor abundance).
- **`[V]` mechanism shapes** — direction, threshold, discontinuity, fold, and the five-way opposite-sign
  discriminant, all forced by the R19 substrate with no new constant.
- **`[O]` absolute magnitudes** — every absolute number (TEWL flux, days, °C, incidence, RR magnitude,
  melanin OD) inherits its parent target's stated obstacle; none is fitted (`IRREPRODUCIBILITY_LEDGER.md`).

**Determinism:** pathology results 2×sha256 identical; core T1..T5+ONCO battery hash unchanged.
