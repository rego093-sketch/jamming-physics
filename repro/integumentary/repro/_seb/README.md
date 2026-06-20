# `_seb` — the sebaceous duct: pilosebaceous occlusion as a hysteretic jamming switch (target T7)

The package's physical class is **jamming** (a barrier/interface driven past a spinodal by an external
insult). The pilosebaceous duct is a textbook member that the prior targets did not cover: a follicular
channel that, when the **net occlusion drive** (androgen-driven sebum + infundibular hyperkeratinization
+ *C. acnes*, minus clearance) rises past a spinodal, **snaps shut into a comedo** — and, crucially,
**reopens only at a lower drive** (a true hysteresis loop, the signature of a first-order jam, not a
reversible threshold). This module emerges that duct as the **shared R19 jamming switch**
(`vp_substrate` + `skn_dynamics`, the same machinery as T1/T2) running on a **newly measured** sebaceous
master-gene γ (**PRDM1/Blimp1**, gene 639, the sebaceous-lineage master — Horsley et al., *Cell* 2006).
It is a **new organ on a measured (fetched + cached + vendored) γ**, promoted `to_measure → fetched →
vendored` exactly as MITF/EDAR were. It is a **research artifact**: it writes `reports/seb_results.json`
and does **not** touch the core writing gate; the core T1..T5+oncology battery hash is **unchanged**.

This implements `HANDOFF_NEXT_STEPS.md` §5.2 (mechanism-first) for the acne/HS lane previously flagged
as *"NOT YET MODELABLE — the sebaceous organ/target does not exist in the package."* The target now exists.

## Run

```
python repro/run_seb.py
```

Prints the organ emergence (measured PRDM1 γ, offline-reproduced), the jamming/hysteresis mechanism,
the disease → mechanism map, the mechanism + clinical-sign + intervention-reversal battery, the
opposite-mode discriminant, selected readouts, and the 2×sha256 determinism check; writes
`reports/seb_results.json`.

## The no-tuning rule (VP-SPEC C0/C3)

> γ is **measured** — PRDM1 proximal-promoter nearest-neighbour ΔG37 (SantaLucia 1998) over the cached
> NCBI window TSS−2000..+500, the **same pipeline** validated to reproduce MITF and EDAR byte-for-byte.
> The duct's two basins (patent / comedo) and its switch are the **substrate** R19 jam; the occlusion
> set-points (healthy −0.3; the comedo/rupture loads) are **dimensionless regime scales `[F]`**, **not**
> fitted to a lesion count. What the substrate **predicts** — a **discontinuous** snap at the upper
> spinodal, **hysteretic** reopening at a lower spinodal, a **patent** healthy duct, and every disease
> direction + intervention reversal — is `[V]`. The absolute comedo/lesion counts and the sebum
> excretion rate are the `[O]` obstacles (a per-gland calibration), inherited from the sebaceous target.

Why this matters: PRDM1 is the **lowest-γ organ in the atlas**, so its functional spinodal opens
**earliest** — an honest **emergence-order prediction** graded by **sign**, not chosen to land anywhere.
The jam's discontinuity and hysteresis come straight from R19; nothing here is tuned to a clinical number.

## Disease → knob (2) — each a signed shift on the **one** jam

| disease | knob moved | intervention (knob reversed) |
|---|---|---|
| acne vulgaris | standing **high** net occlusion (sebum + hyperkeratinization + *C. acnes*) → past the upper spinodal → comedo; *C. acnes* amplifier makes it **inflammatory** | comedolytic + sebostatic + antimicrobial (retinoid / isotretinoin) → occlusion below the **lower** spinodal → duct reopens |
| hidradenitis suppurativa (HS) | the **same** jam in **deeper** apocrine-bearing follicles → heavier plug **ruptures** into the dermis → a chronic scarring **sinus-tract** sub-state acne lacks | biologic (anti-TNF/IL-17) de-inflames the **active** jam, but the ruptured tract is structural → drive reduction does **not** reopen it; **deroofing/excision** resets the scar |

## The headline check — opposite-mode discriminant

The **same** jam, driven to **opposite depth/reversibility**, reproduces clinically **opposite**
entities with **no new constant**, across three axes:

- **reversibility** — superficial acne (drive-down **reopens** it) ↔ deep HS rupture (the same drive-down
  level that clears acne **leaves the scar**; only physical removal resets it).
- **inflammatory sign** — the *C. acnes* amplifier toggles a fixed jam **inflammatory ↔ comedonal**
  (de-inflaming leaves the duct jammed but non-inflammatory).
- **depth** — HS jams at a **heavier** plug load than acne (the rupture branch is reachable only there).

`run_seb.py` asserts all three (`all_opposite_pairs_reproduced`). The "same drive-down, opposite
outcome" pair is the substrate's clean account of *why isotretinoin clears acne but not established HS
tracts.*

## Files

- `sebaceous_duct.py` — the jam (`jamming_hysteresis`), the net-occlusion model (`net_occlusion`), the
  duct-outcome continuation (`_duct_outcome`/`_form_then`/`_treat_from`), the 2 diseases, and
  `sebaceous_summary()`.
- `seb_verify.py` — the mechanism + clinical-sign + intervention-reversal battery, the discriminant, the
  γ-provenance check, the determinism check, and `seb_gate()` (this layer's research-first lock).

## Honest notes

- **discontinuity + hysteresis** — the substrate gives a clean first-order jam (up-jump ≈ 2.0 at the
  upper spinodal, reopening at the lower spinodal, loop width ≈ 2.0); these are `[V]` shape claims, not
  fitted magnitudes.
- **absolute counts** — comedo/lesion counts, Hurley-stage extent and sebum excretion rate are `[O]`
  (need a per-gland calibration); the layer is graded on **direction, discontinuity, hysteresis and
  reversibility**, not on a fitted number.
- **rupture thresholds** — the deep-branch rupture predicate uses regime-scale `[F]` thresholds
  (`RUPTURE_PLUG`, `RUPTURE_INFLAM`); the superficial comedo never reaches them, which is the point.
- **core untouched** — this layer reuses the substrate + the engine emitter only; it does not modify
  `_engine`, `_oncology`, or `_verify`, so `repro/run_all.py`'s result hash is unchanged.
