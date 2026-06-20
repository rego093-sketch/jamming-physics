# §20 — Completing the sensory atlas (reproduction)

`complete_sensory_atlas.py` emerges the **four remaining sensory modalities** — touch,
pain, proprioception, vestibular — from their master genes' **real measured γ**
(read-only, fetched from NCBI by `../_engine/data/fetch_full_sensory_gamma.py`,
window TSS−2000..+500, SantaLucia 1998 NN table — the *same scale* as the taste and
organ atlases), on the same R19 switch that fires the neuron and emerged eye/ear/
olfactory/skin/taste in §12.

Run: `python3 complete_sensory_atlas.py` (deterministic; prints a result-block sha256).
Data: `../_engine/data/full_sensory_gamma.json` (the 4 new modalities) +
`../_engine/data/sensory_organ_gamma.json` (the existing 5, read-only roster).

## What it shows

- **γ is a real read-out**, not a free parameter: corr(γ,GC)=0.9975 over the 14 new
  master/transducer genes (organ atlas 0.994, taste 0.995) `[F]`.
- **presence by STATE** (master cis ON → present; OFF → absent even with partners intact) `[F]`;
  **developmental ORDER** from the γ-set spinodal (vestibular → proprioceptor → nociceptor) `[F]`;
  **relative SIZE** from DWELL ∝ γ^1.5 `[F]`.
- **somatosensory triad on the one emerged skin organ** (TP63, §12): low-threshold touch
  and warmth vs a **HIGH-threshold** nociceptor that is silent for innocuous stimuli and
  fires only above the **measured** TRPV1 heat threshold (43 °C, Caterina 1997). The
  threshold ORDER (pain HIGH vs touch/warmth LOW) is forced/measured `[F]`/`[V]`.
- **proprioception closes the §11 reflex loop**: the muscle spindle (RUNX3 · PIEZO2; human
  PIEZO2 loss abolishes proprioception, Chesler 2016) supplies the Ia afferent whose firing
  rises with stretch, feeding the stretch-reflex arc (rejection ×10.4) `[V]`.
- **vestibular directionality**: the hair cell (ATOH1 · OTOP1; Atoh1-null = no hair cells,
  Bermingham 1999) gives a **signed** response to acceleration — +0.6 → 22 spikes, −0.6 → 17 —
  unlike unsigned pressure `[V]`.

## Cited measured inputs (locked, not tuned)

- TRPV1 heat-activation threshold ≈ 43 °C (Caterina et al. 1997) — the nociceptor's heat arm.
- PIEZO2 stretch transduction; human loss abolishes proprioception/touch (Chesler et al. 2016;
  Ranade et al. 2014; Woo et al. 2015).
- ATOH1 as hair-cell master (Bermingham et al. 1999); PRDM12 as nociceptor-lineage master
  (loss → congenital insensitivity to pain).
- All γ values: −mean(NN stacking ΔG) on real human promoter sequence (SantaLucia 1998).

## What stays open `[O]` (Layer-2; see `IRREPRODUCIBILITY_LEDGER.md`)

Absolute organ size, absolute developmental time, absolute firing rates, the absolute
mechanical noxious threshold, and the absolute vestibular resting rate/gain — each needs
external calibration and is marked `[O]`, never asserted as evidence. The forced results are
the developmental order, the relative-size order, and the high-vs-low threshold order.

This chapter completes the sensory inventory: with vision/hearing/smell/taste/vestibular (the
five special senses) and the somatosensory touch/warmth/pain/proprioception, **all nine human
modalities emerge from measured γ and transduce into the low-frequency spike train**.
