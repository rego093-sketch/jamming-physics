# `_vasomotor` — neurovascular reactivity: cutaneous vasomotor tone as a hysteretic jam (target T9)

The package's physical class is **jamming** (a barrier/interface/bond/channel driven past a spinodal by an
external drive). Cutaneous **vasomotor tone** is a member the prior targets did not cover: a dilated vessel
is **jammed ON** (the flushed basin), a constricted vessel is **OFF** (the quiescent/ischemic basin), and a
sustained reactivity drive is what carries the vessel **past a lock** into a fixed state. This module builds
that vasomotor switch as the **shared R19 jamming switch** (`vp_substrate` + `skn_dynamics`, the same
machinery as T1/T2) running on the **already-measured** appendage master-gene γ (**EDAR**, γ = 1.3696, the
organ the atlas labels *"hair follicle / sweat gland (**thermoregulation interface**)"*). The cutaneous
thermoregulatory interface has **two autonomic effector arms** — the **sudomotor** arm (sweat glands, the
T5 target and the hyperhidrosis/HED diseases) and the **vasomotor** arm (skin blood flow, flushing).
Rosacea is a dysregulation of the **vasomotor** arm — the **vascular mirror of hyperhidrosis** on the
sudomotor arm — so it is intrinsic to this organ. This is a **new target on an existing measured organ**
(the **hair-cycle / adhesion pattern**, not the sebaceous new-organ pattern): **no γ is fetched and none is
fitted.** It is a **research artifact**: it writes `reports/vasomotor_results.json` and does **not** touch
the core writing gate; the core T1..T5+oncology battery hash is **unchanged**, and so are the pathology,
hair-cycle, sebaceous and cell-adhesion layer hashes.

This implements `HANDOFF_NEXT_STEPS.md` §5.2 (mechanism-first — the **neurovascular module for rosacea**)
for the rosacea lane previously flagged *"NOT YET MODELABLE — needs a neurovascular / inflammatory module
(flushing, dermal vessel reactivity) … Missing mechanism (dermal perfusion is an inherited citation, not a
dynamics target here)."* The target now exists.

## The SSOT seam is not crossed

> The dermal-**perfusion magnitude** stays an **inherited circulatory citation** (CHARTER *"Seams IN:
> circulatory dermal perfusion (cited)"*) and is **not re-emerged** here. This target adds **only the
> vasomotor reactivity dynamics** the seam note says is missing — a reactivity threshold and a hysteretic
> fixation — on the shared R19 switch. The fixed digital-ischemia / ulcer state of **secondary Raynaud**
> (connective-tissue disease) and the rosacea inflammatory effector chemistry beyond the LL-37/Demodex
> amplifier flag are **immune/rheumatology sibling-package seams**, named not modeled.

## Run

```
python repro/run_vasomotor.py
```

Prints the target note (existing measured EDAR γ, no new fit; the seam), the reactivity-jam/hysteresis
mechanism, the disease → mechanism map, the mechanism + clinical-sign + intervention-reversal battery, the
opposite-property discriminant, selected readouts, and the 2×sha256 determinism check; writes
`reports/vasomotor_results.json`.

## The no-tuning rule (VP-SPEC C0/C3)

> γ is **measured** — EDAR is already vendored from the DNA gene-clock (the same organ the T5
> thermoregulation page and the hair-cycle layer use); the vasomotor target adds **no new γ and fits none**.
> The vessel's two basins (dilated / constricted) and its switch are the **substrate** R19 jam; the resting
> tone, the reactivity gains and the trigger/constrictor drives are **dimensionless regime scales `[F]`**
> (fractions of the EDAR spinodal), **not** fitted to a flush magnitude, an erythema index, a vessel density
> or a digital temperature. What the substrate **predicts** — a **discontinuous** lock at each spinodal,
> **hysteretic** re-normalisation only across the opposite spinodal, a **responsive** healthy vessel in the
> reversible middle, reversibility being a uniform consequence of **whether a drive crosses its lock**, and
> every disease direction + intervention reversal — is `[V]`. The absolute erythema index, vessel density,
> flush magnitude, digital temperature, attack frequency and involved body-surface area are the `[O]`
> obstacles (a per-vessel calibration; the perfusion magnitude is an inherited circulatory seam), inherited
> from the vasomotor target.

Why this matters: the same switch and the **same spinodals**, driven in **opposite directions** (a standing
vasodilator drive vs a cold vasoconstrictor drive), give two clinically **opposite** vasomotor diseases. The
jam's discontinuity and hysteresis come straight from R19; nothing here is tuned to a clinical number.

## Disease → knob (2) — each a signed vasomotor drive on the **one** switch

| disease | knob moved | intervention (knob reversed) |
|---|---|---|
| rosacea | a standing **vasodilator reactivity** drive (lowered flush threshold; heat/alcohol/UV/spice) carries the net dilator drive **above the upper spinodal** → the vessel **locks dilated** (fixed erythema/telangiectasia); the LL-37/Demodex amplifier on the same dilated background gives the **papulopustular** subtype | **anti-inflammatory** therapy (metronidazole/ivermectin/azelaic acid/doxycycline) clears the papulopustular inflammation; a vasoconstrictor (**brimonidine**) blanches transiently but does **not** reset the fixed vessels (hysteresis) — only **laser/IPL** physically resets the telangiectasia |
| Raynaud phenomenon | a cold/stress **vasoconstrictor** drive carries the net dilator drive negative into the constricted/ischemic basin → the white-blue-red digital **vasospastic attack**; primary Raynaud is reversible (it crosses no lock) | rewarming, cold avoidance, and a **vasodilator / calcium-channel blocker** (nifedipine) abort the attack; the fixed digital-ischemia/ulcer state is the **secondary**-Raynaud (connective-tissue-disease) seam |

## The headline check — opposite-property discriminant

The **same** vasomotor switch and the **same** EDAR spinodals, driven in opposite directions, reproduce
clinically **opposite** entities with **no new constant**, across three axes:

- **direction** — vasodilation (rosacea: net drive above the upper spinodal) ↔ vasoconstriction (Raynaud:
  net drive negative into the constricted basin).
- **reversibility** — fixed telangiectasia (rosacea: the drive **crosses** the upper lock, so the dilated
  state is fixed) ↔ reversible vasospasm (primary Raynaud: the attack **stays short of** the lock and
  returns on rewarming). Reversibility is a uniform consequence of **whether a drive crosses its lock**, not
  a per-disease flag.
- **vascular vs inflammatory (within rosacea)** — erythematotelangiectatic (vascular, the dilation/fixation
  story) ↔ papulopustular (the inflammatory LL-37/Demodex amplifier on the same dilated background).

`run_vasomotor.py` asserts all three (`all_opposite_pairs_reproduced`). That a single switch generates a
fixed-dilation disease and a reversible-constriction disease — from the **drive sign and the lock rule
alone**, on a single reused EDAR γ — is the substrate's clean account of *why rosacea flushes and fixes while
Raynaud blanches and reverses.*

## Files

- `vasomotor_switch.py` — the reactivity jam (`vasomotor_hysteresis`), the net-drive model
  (`net_vasodilator`), the state-outcome / excursion continuations (`_state_outcome`/`_excursion_returns`/
  `_fix_then`/`_constrict_from_fixed`), the 2 diseases, and `vasomotor_summary()`.
- `vasomotor_verify.py` — the mechanism + clinical-sign + intervention-reversal battery, the discriminant,
  the γ-provenance check (existing measured EDAR, no new fit), the determinism check, and
  `vasomotor_gate()` (this layer's research-first lock).

## Honest notes

- **discontinuity + hysteresis** — the substrate gives a clean first-order jam with **two** locks
  (dilate-lock at the upper spinodal ≈ +1.0, constrict-lock at the lower spinodal ≈ −1.0, loop width ≈ 2.0);
  these are `[V]` shape claims, not fitted magnitudes.
- **responsive healthy set-point** — the healthy vessel rests at net drive ≈ −0.3, in the **reversible
  middle** (|v| < 1), so it flushes and constricts reversibly and locks neither way; a lock is reached only
  when a *sustained* drive carries it past a spinodal.
- **reversibility as a derivation** — the reversible-flush ↔ fixed-telangiectasia and reversible-vasospasm
  ↔ fixed-ischemia distinctions are **not** fitted flags: a vessel is fixed iff its drive **crossed a
  lock**, a logical consequence of the drive magnitude relative to the spinodal.
- **brimonidine vs laser** — a partial vasoconstrictor leaves the net drive above the lower lock, so a fixed
  telangiectasia stays dilated (a transient blanch only); the structural reset is **laser/IPL**, exactly as
  the deeper sebaceous tract needs **deroofing** rather than drive reduction.
- **absolute magnitudes** — erythema index, vessel density, flush magnitude, digital temperature, attack
  frequency and body-surface area are `[O]` (need a per-vessel calibration; the perfusion magnitude is an
  inherited circulatory seam); the layer is graded on **direction, discontinuity, hysteresis, the lock rule
  and the inflammatory amplifier**, not on a fitted number.
- **seam not crossed** — the dermal-perfusion magnitude stays an inherited circulatory citation; only the
  reactivity dynamics is added. The secondary-Raynaud fixed-ischemia state and the deeper rosacea immune
  chemistry are sibling-package seams, named not modeled.
- **core untouched** — this layer reuses the substrate + the engine emitter only; it does not modify
  `_engine`, `_oncology`, or `_verify`, so `repro/run_all.py`'s result hash is unchanged.
