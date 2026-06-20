# `_pathology` — major integumentary diseases on the package's own mechanisms

This module simulates the major integumentary diseases **without introducing a single new
constant**. Every disease is a *named perturbation of one knob that already exists* in the
verified target battery (T1..T5 / oncology), and every intervention is **the same knob reversed**.
It is a **research artifact**: it writes `reports/pathology_results.json` and does **not** touch the
writing gate. The core battery (`repro/run_all.py`) is untouched and remains the gate of record
(its determinism sha is unchanged by this module).

## Run

```
python repro/run_pathology.py
```

Prints the disease→mechanism map, the clinical-sign + intervention-reversal battery, the
opposite-sign discriminant, selected readouts, and the 2×sha256 determinism check; writes
`reports/pathology_results.json`.

## The one rule

> A disease may only **move a knob the package already has**. It may not add a constant, a basin,
> or a free parameter. If the cited absolute magnitude is not derivable in-package, the disease
> **inherits the parent target's `[O]` obstacle** (see `IRREPRODUCIBILITY_LEDGER.md`).

## Ownership (master map §6)

This package owns the **acquired / multifactorial / dynamics-key** skin diseases and the **dynamics
side** of borderline genetic ones (the gene-lesion fact is `disease_wp`'s, imported by gene-key).
Single-gene rare genodermatoses are not in this lane. The full coverage audit (covered / out-of-lane
/ not-yet-modelable) and next steps are in `../../HANDOFF_NEXT_STEPS.md`.

## Disease → mechanism → knob (13)

| disease | target | knob moved | intervention (knob reversed) |
|---|---|---|---|
| atopic dermatitis | T1 | chronic standing deficit `h_base<0` → reserve collapses | emollient: reduce `|h_base|` |
| contact dermatitis | T1 | acute insult crosses the spinodal → discontinuous collapse | avoidance + active barrier repair (re-cross +spinodal) |
| ichthyosis | T1+T4 | shedding drive toward the spinodal → shed time diverges | keratolytic/retinoid: strong shedding drive past spinodal |
| psoriasis | T4 | exit drive past the differentiation spinodal → autonomous advance | anti-proliferative: drop drive below spinodal |
| chronic / diabetic / pressure wound | T2 | unjam drive below the package's critical drive → non-closure | debridement / growth factor: raise above critical |
| vitiligo | T3 | autoimmune drive pushes viability below spinodal → melanin 0 | narrowband UVB: re-cross +spinodal (hysteretic) |
| melasma / hyperpigmentation | T3 | pro-melanogenic synthesis drive → regulated overshoot | depigmenting / photoprotection: lower synthesis drive |
| albinism (OCA) | T3→oncology | melanin screen removed → hazard rises | sunscreen: exogenous screen |
| hypohidrotic ectodermal dysplasia | T5 | EDAR-LOF caps `m_max` → danger band at lower load | external cooling: lower the load |
| primary hyperhidrosis | T5 | recruitment threshold `theta_on` lowered → sweats at rest | antiperspirant / anticholinergic / botulinum: raise threshold |
| heat stroke | T5 | thermal load exceeds capacity → runaway | rapid cooling + load reduction below the runaway onset |
| skin cancer (melanoma/SCC/BCC) | oncology | intermittent-vs-cumulative dichotomy + pigment-loss burst | reduce UV intensity/dose; avoid sunburn; restore screen |
| actinic keratosis | oncology | fewer multistage hits → precursor field (high prevalence, low conversion) | sun protection (lower dose) + field treatment |

## The headline check — opposite-sign discriminant

The **same** R19 switch, driven with **opposite** signs, reproduces clinically **opposite** poles with
**no new constant**, across three switches: turnover (psoriasis ↔ ichthyosis), barrier (intact ↔
atopic), **melanin (melasma ↔ vitiligo)**, **sweat (hyperhidrosis ↔ HED)**, and photoprotection
(healthy tan ↔ pigment loss). `run_pathology.py` asserts all five
(`all_opposite_pairs_reproduced`).

## Files

- `skin_pathology.py` — the 13 diseases + `opposite_sign_pairs(results)` + `pathology_summary()`.
- `pathology_verify.py` — the binary clinical-sign + intervention-reversal battery and determinism check.

## Honest notes

- **psoriasis** — threshold + several-fold smooth acceleration is `[V]`; absolute transit in days is `[O]` (T4). The cited 3–5 d window is the anchor `[L]`, not a fitted number.
- **atopic dermatitis** — the dimensionless **barrier-reserve collapse** is the primary `[V]` signature; baseline-TEWL magnitude is secondary `[O]`.
- **thermo probes** — this module integrates its own thermo sweeps at a coarser, fully-converged resolution (`_TH_T`/`_TH_DT`) for speed; the engine (`skn_dynamics.thermo_run`) defaults are untouched, so the core `run_all.py` hash is unaffected.
