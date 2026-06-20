# IRREPRODUCIBILITY LEDGER — 20-complete-sensory-atlas (VP-SPEC C3)

This capstone completes the human sensory inventory: the four remaining modalities
(touch · pain · proprioception · vestibular) emerge from their master genes' **measured**
stacking stiffness γ — the same READ-ONLY primitive that writes DNA genes and fires neurons —
and each is wired to a transducer whose **defining property is measured, never tuned**. Per
Constitution C3, every `[O]` quantity carries a stated obstacle below; an `[O]` without an
obstacle is a gate FAIL.

**Grades.** `[F]` read from γ-structure · `[V]` verified/reproduced in-package · `[L]` peer-reviewed
(cited, not re-derived) · `[O]` empirically open but **dataset/obstacle-named**.

## The reproducible core (NOT in this ledger because it reproduces)

- **γ of 14 sensory master genes** recomputed in-package from cached NCBI promoters (GRCh38, the
  reproducible `[TSS−2000, TSS+500]` window; SantaLucia-1998 NN stacking table), **bit-for-bit
  deterministic** (2×sha256 identical, frozen hash). `[F]`
- **γ is a real read-out, not free:** `corr(γ, GC) = 0.997` over the new genes (organ atlas 0.994,
  taste 0.995) — γ tracks the measured sequence, so the organs emerge from biology, never fitted. `[F]`
- **presence is STATE, not γ:** each new organ is `present` only when its R19 switch is settled ON
  (drive above spinodal), `absent` at zero drive — parts-present ≠ trait. `[V]`
- **developmental ORDER** vestibular → proprioceptor → nociceptor, derived from the spinodal each
  switch clears as the drive ramps (|h_sp| 0.6588 < 0.6832 < 0.7757). `[F]`
- **relative SIZE order** nociceptor > proprioceptor > vestibular (DWELL ∝ γ^1.5, monotone in γ). `[F]`
- **threshold ORDER** nociceptor **HIGH** vs touch/warmth **LOW**: on the one emerged skin organ, an
  innocuous 35 °C warmth and a gentle 0.2 press fire thermo/mechano but leave the nociceptor **silent**,
  while 50 °C heat and 1.0 press drive **both** — the contrast is anchored to the measured TRPV1 43 °C
  (Caterina 1997). `[F]`/`[V]`/`[L]`
- **proprioceptive loop closure:** the spindle's Ia firing rises monotonically with stretch and feeds
  the §11 `ReflexArc`, which **opposes** the disturbance (closed-loop error 0.0481 vs open 0.5000,
  rejection ×10.4) — the loop now closes onto an ACTUAL afferent organ, not an abstract "stretch". `[V]`
- **vestibular directionality:** equal-magnitude accelerations of opposite sign give **different** firing
  (signed about rest), unlike unsigned pressure — from hair-cell morphological polarisation (Hudspeth). `[V]`

## The open items

| # | `[O]` item | obstacle (why it cannot be derived here) | location |
|---|------------|-------------------------------------------|----------|
| S1 | **absolute organ size (µm / cell count)** | Only the *relative* size is geometric (DWELL ∝ γ^1.5 is monotone in the measured γ, so the **order** is forced). Absolute physical size needs proliferation rate × cell-cycle time × apoptosis fraction — none fixed by the γ window. **Closes with:** stereology / organ-mass measurement. A magnitude, not the order. | `complete_sensory_atlas.py` `[3]`; `Organ.size()` is a ∝ value |
| S2 | **absolute developmental time (hours / days)** | The **order** of emergence is the spinodal each switch clears (derived, locked). The **absolute clock** — when in real gestation each switch flips — depends on morphogen kinetics and is not in the γ reading. **Closes with:** a timed developmental-staging dataset. Refines the timestamps, not the order. | `[2]`; `functional_spinodal()` values |
| S3 | **absolute firing rates (Hz)** | Spike **counts** here are Layer-2 illustrative — what is locked is the threshold ORDER and the silent/fires contrast, not the rate magnitude (the rate-coding biophysics is the R19/EM layer, §2/§14). **Closes with:** single-unit afferent recordings (microneurography). A magnitude on an already-evidenced contrast. | `[4]`–`[6]`; `len(...["spikes"])` |
| S4 | **absolute mechanical noxious threshold `P_NOX`** | The nociceptor's **heat** threshold is MEASURED and cited (`T_NOX = 43.0 °C`, TRPV1, Caterina 1997 — *not* in this ledger). The **mechanical** noxious threshold `P_NOX = 0.5` (normalised) has no single cited constant; only its placement ABOVE the innocuous-touch range is needed for the locked threshold order. **Closes with:** quantitative algometry / nociceptor mechanical-threshold data. The *order* (high vs low) is forced; the *value* is open. | `vp_neuro_engine.py` `Nociceptor.P_NOX`; engine `[O]` note |
| S5 | **vestibular resting discharge + gain `REST`** | Hair cells have a non-zero resting discharge that the signed response rides on; `REST = 0.5` (and the ±0.5 gain) is a model operating-point choice. The **directionality** (signed ≠ unsigned) is the verified claim and does not depend on the exact resting value. **Closes with:** vestibular-afferent resting-rate recordings (e.g. Goldberg–Fernández). The sign asymmetry is `[V]`; the absolute rate is `[O]`. | `vp_neuro_engine.py` `VestibularReceptor.REST`; engine `[O]` note |

## What is explicitly MEASURED (locked input, cited — so NOT `[O]`)

- **`T_NOX = 43.0 °C`** — TRPV1 heat-activation threshold, Caterina 1997. This is the anchor that makes the
  nociceptor HIGH-threshold by construction (silent at 35 °C, fires at 50 °C); it is a locked measured
  input, not a tuned number.
- **master-gene identities** — PRDM12 (nociceptor; Chen 2015), RUNX3 (proprioceptor; Inoue 2002),
  ATOH1 (hair-cell master; Bermingham 1999), PIEZO2 (mechanotransduction; Woo 2015 / Chesler 2016 human
  loss-of-function), POU4F3/OTOP1/OTOG (hair-cell / otolith). Cited, not re-derived. `[L]`

## Cross-references to sibling reproductions

- **neuro §12 (organ emergence, 4D).** Identical method — master-gene γ + spinodal order + DWELL ∝ γ^1.5.
  §12 emerged the five special-sense organs (eye/ear/olfactory/skin/taste); this chapter emerges the four
  remaining modalities and so **completes the nine-modality roster**.
- **neuro §11 (reflex arc).** That chapter referenced an abstract "stretch feedback"; the **S5/loop** work
  here replaces it with an ACTUAL muscle-spindle afferent (Proprioceptor → ReflexArc), closing the loop.
- **neuro §16 / §17 (force / spinal CPG).** The **S3** firing-magnitude boundary is exactly the handoff to
  those biophysical layers — `[O]` here for the same reason §17's `[B2]` is a category boundary: rate and
  force are the above-γ R19/EM/cross-bridge layers, not the γ identity layer.
- **taste (§10/§12) and the DNA volume.** The γ metric is the **same** primitive validated bit-for-bit
  against frozen LCT values elsewhere; the four new promoters were fetched and cached by the **identical**
  pipeline/window/NN-table as taste (γ,GC correlation 0.997 ≈ taste 0.995 confirms the read-out is real).
