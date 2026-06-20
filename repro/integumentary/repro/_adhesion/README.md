# `_adhesion` — cell adhesion: keratinocyte cohesion as a hysteretic binding jam (target T8)

The package's physical class is **jamming** (a barrier/interface/bond driven past a spinodal by an
external insult). Cell **adhesion** is a textbook member that the prior targets did not cover: adherent
keratinocytes are **jammed** together (the ON basin), a blister is the bond **unjammed** (the OFF basin),
and an autoantibody is a **de-adhesive drive** that, once it crosses a spinodal, makes the bond **detach
discontinuously** — and, crucially, **re-adhere only when the antibody is cleared well past the level that
broke it** (a true hysteresis loop, the signature of a first-order jam, not a reversible threshold). This
module builds that adhesion switch as the **shared R19 jamming switch** (`vp_substrate` + `skn_dynamics`,
the same machinery as T1/T2) running on the **already-measured** keratinocyte master-gene γ
(**KRT14**, γ = 1.4894, the *"keratin barrier mechanics / structural integrity"* organ). Desmosomes
(cell-cell) and hemidesmosomes (cell-matrix) both **anchor the keratin intermediate-filament network**,
so junctional adhesion is intrinsic to the keratinocyte organ — this is a **new target on an existing
measured organ** (the **hair-cycle pattern**, not the sebaceous new-organ pattern): **no γ is fetched and
none is fitted.** It is a **research artifact**: it writes `reports/adhesion_results.json` and does **not**
touch the core writing gate; the core T1..T5+oncology battery hash is **unchanged**, and so are the
pathology, hair-cycle and sebaceous layer hashes.

This implements `HANDOFF_NEXT_STEPS.md` §5.2 (mechanism-first — *"an adhesion T8 switch next"*) for the
autoimmune-bullous lane previously flagged as *"NOT YET MODELABLE — needs a cell-adhesion target ...
Missing target."* The target now exists.

## Run

```
python repro/run_adhesion.py
```

Prints the target note (existing measured KRT14 γ, no new fit), the binding-jam/hysteresis mechanism, the
disease → mechanism map, the mechanism + clinical-sign + intervention-reversal battery, the
opposite-property discriminant, selected readouts, and the 2×sha256 determinism check; writes
`reports/adhesion_results.json`.

## The no-tuning rule (VP-SPEC C0/C3)

> γ is **measured** — KRT14 is already vendored from the DNA gene-clock (the same organ the T1 barrier
> page uses); the adhesion target adds **no new γ and fits none**. The bond's two basins (adherent /
> blister) and its switch are the **substrate** R19 jam; the constitutive adhesion **reserve** and the
> antibody **titres** are **dimensionless regime scales `[F]`** (fractions of the KRT14 spinodal), **not**
> fitted to a titre, blister count or body-surface area. What the substrate **predicts** — a
> **discontinuous** detachment at the spinodal, **hysteretic** re-adhesion only above the upper spinodal,
> an **adherent** healthy bond, the cleavage **plane** selected by the targeted compartment, the
> **Nikolsky sign** as a derived consequence of which bond fails, and every disease direction +
> intervention reversal — is `[V]`. The absolute blister counts, antibody titre (IU/mL), micrometre
> cleavage depth and involved body-surface area are the `[O]` obstacles (a per-junction calibration),
> inherited from the adhesion target.

Why this matters: the same switch, the **same spinodal** and the **same antibody magnitude**, with **only
the targeted adhesion compartment** differing (cell-cell desmosomal ↔ cell-matrix hemidesmosomal), flip
the cleavage plane, the Nikolsky sign and the blister tension. The jam's discontinuity and hysteresis come
straight from R19; nothing here is tuned to a clinical number.

## Disease → knob (2) — each a signed de-adhesion on the **one** switch

| disease | knob moved | intervention (knob reversed) |
|---|---|---|
| pemphigus vulgaris | an anti-**desmoglein** (DSG3) titre drives the **cell-cell** compartment below the spinodal → **intraepidermal** (suprabasal) split; the failing bond *is* the lateral bond → **Nikolsky positive**, **flaccid** blister | **rituximab / immunosuppression** clears the antibody → net adhesion returns above the spinodal → bond re-adheres (a partial titre reduction does **not** — the hysteresis) |
| bullous pemphigoid | an anti-**BP180** (COL17A1, hemidesmosomal) titre drives the **cell-matrix** compartment below the spinodal → **subepidermal** split; the cell-cell bonds are intact (whole epidermis lifts as a roof) → **Nikolsky negative**, **tense** blister | **corticosteroid / immunosuppression** clears/suppresses the antibody → bond re-adheres (a partial reduction does **not**) |

## The headline check — opposite-property discriminant

The **same** adhesion switch, the **same** KRT14 spinodal and the **same** antibody magnitude, with the
autoantibody driving one compartment or the other, reproduce clinically **opposite** entities with **no new
constant**, across three axes:

- **cleavage plane** — intraepidermal/suprabasal (PV) ↔ subepidermal/junctional (BP).
- **Nikolsky sign** — positive (PV: the failing bond *is* the cell-cell bond, so a tangential shear
  propagates the split) ↔ negative (BP: the cell-cell bonds are intact, so the shear does not propagate).
- **blister tension** — flaccid thin-roof (PV) ↔ tense full-roof (BP).

`run_adhesion.py` asserts all three (`all_opposite_pairs_reproduced`). That one binary choice — which
compartment the antibody targets — flips all three clinical properties is the substrate's clean account of
*why a suprabasal autoantibody gives a fragile, shear-spreading blister while a junctional one gives a
tense, intact-roofed one.*

## Files

- `adhesion_switch.py` — the binding jam (`adhesion_hysteresis`), the net-adhesion model
  (`net_adhesion`), the compartment-outcome continuation (`_compartment_outcome`/`_separate_then`/
  `_treat_from`), the derived Nikolsky rule (`_nikolsky_positive`), the 2 diseases, and
  `adhesion_summary()`.
- `adhesion_verify.py` — the mechanism + clinical-sign + intervention-reversal battery, the discriminant,
  the γ-provenance check (existing measured KRT14, no new fit), the determinism check, and
  `adhesion_gate()` (this layer's research-first lock).

## Honest notes

- **discontinuity + hysteresis** — the substrate gives a clean first-order jam (detachment jump ≈ 2.1 at
  the lower spinodal, re-adhesion at the upper spinodal, loop width ≈ 2.0); these are `[V]` shape claims,
  not fitted magnitudes.
- **adherent healthy set-point** — the healthy bond sits at net adhesion ≈ 1.4, **above** the upper
  spinodal, so the antibody must overcome a finite reserve to detach it, and clearing the antibody (not a
  partial dip) is what returns it above threshold — the hysteresis is the clinical "sustained
  immunosuppression" rule.
- **Nikolsky as a derivation** — the Nikolsky sign is **not** a fitted flag: it is positive iff the failing
  plane is the cell-cell (lateral) bond, a logical consequence of which compartment the antibody targets.
- **absolute counts** — blister counts, antibody titre (IU/mL), cleavage depth and body-surface area are
  `[O]` (need a per-junction calibration); the layer is graded on **direction, discontinuity, hysteresis,
  plane and Nikolsky sign**, not on a fitted number.
- **acquired ≠ congenital (lane split)** — these are **acquired autoimmune** blistering diseases
  (dynamics-key, ours). The **congenital** single-gene blistering disease **epidermolysis bullosa**
  (COL7A1 / KRT5 / KRT14 / LAMB3 …) is **gene-key** and belongs to `disease_wp` (HANDOFF §3); this layer
  does not model it.
- **core untouched** — this layer reuses the substrate + the engine emitter only; it does not modify
  `_engine`, `_oncology`, or `_verify`, so `repro/run_all.py`'s result hash is unchanged.
