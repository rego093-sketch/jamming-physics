# Chapter content — Environment as a structural methylation layer (VP-SPEC §6/§6-R ready)

> Drop-in content for `docs/dna/environment-methylation-layer/index.html`. English only
> (VP_SPEC). Answer-first ≤60 words, self-contained claims, `[F]`/`[O]` grades, vp-cards
> for cited locked quantities. Body adds only to the canonical DNA whitepaper (append-only).

---

## answer (`<p class="answer">`, 40–60 words)

Lactase persistence is not a difference in the lactase gene's material: the LCT promoter
reads at the same γ in human and mouse (|Δγ| = 0.034, same-material scale). The difference
lives in a methylation substrate read from structure — a local CpG hotspot (O/E 0.78) the
single-scalar average hides — driving a discontinuous, hysteretic switch. **[F]**

## abstract (`<p class="abstract">`)

Environment is not an external scalar added to a switch; it is written onto DNA at specific
CpG positions, and that substrate is readable from sequence. At the lactase locus the master
gene LCT is conserved (present human and mouse) and its material is conserved (|Δγ| = 0.034 <
0.05), so lactase persistence cannot be a γ difference. A local CpG hotspot (O/E 0.78, 2.3×
the 2.5 kb mean) seeds a methylation layer M whose age-driven accumulation flips the LCT
switch off discontinuously; the persistence cis variant lowers that rate. The silencing is
hysteretic (lactase is not re-inducible), so dietary "adaptation" sits above the DNA layer.

## claim grades (`.claim-strip`)

- Page grade: **[F]** forced (structure / direction read from measured γ and CpG substrate).
- Open quantities: **[O]** absolute methylation β, absolute age-of-silencing, rate
  magnitudes, microbiome plasticity (see ledger).

## vp-cards (self-contained cards for cited locked quantities, §6-R.2)

```html
<aside class="vp-card" data-locked="same-material">
  <b>same-material scale = 0.05</b> — the snake-ZRS |Δγ| the whitepaper treats as "same γ".
  Below it, a phenotype difference is NOT in the material. <b>[F]</b> forced.
  <a href="/dna/state-switch-on-or-off/#zrs">canonical derivation §4</a>
</aside>

<aside class="vp-card" data-locked="spinodal">
  <b>|h_sp| = (2/3√3)·γ^1.5</b> — the γ-set drive past which a basin disappears: makes the
  switch flip DISCONTINUOUS (no half-state). <b>[F]</b> forced.
  <a href="/dna/material-threshold-scale/#spinodal">canonical derivation §2</a>
</aside>
```

## body (append-only; the science)

**Lactase persistence is a regulation question, not an inventory question.** Every human
carries LCT; the trait is whether the switch stays on past weaning. The kit's existing logic
applies directly: SET is conserved (LCT present in human and mouse) and the material is
conserved — the LCT promoter reads γ = 1.315 in human, 1.350 in mouse, |Δγ| = 0.034, below
the snake-ZRS same-material scale. So the persistence/non-persistence difference cannot live
in the LCT material, exactly as limblessness cannot live in the snake ZRS γ.

**The difference lives in a layer the single scalar discards.** Reducing the promoter to one
number γ ≈ GC erases the dinucleotide CpG signal, which carries where environment writes onto
DNA. Read directly from structure, the LCT regulatory region holds a local CpG hotspot:
window O/E reaches 0.78 — 2.3× the 2.5 kb average of 0.34 that a scalar reports — and the
human locus retains 1.8× more of this substrate than mouse. This hotspot is the designed
exposure to the drive, read rather than asserted (the revised I3 design clause).

**The methylation layer M.** γ stays read-only. A dynamic variable M, seeded by the measured
CpG substrate and accumulating with age, lowers the switch's effective drive h_eff = h_base −
λ·M. When h_eff crosses the γ-set spinodal the LCT state flips off discontinuously — the same
R19 bistability as every other switch, now driven by a structural, environment-coupled layer.
Two methylation trajectories on the *same* γ give opposite outcomes: a high age-rate silences
LCT; the persistence cis variant's low rate keeps it on. γ is blind to the difference; M
resolves it.

**The silencing is hysteretic, and that is the honest payoff.** Once methylation has flipped
the switch off, lowering methylation does not turn it back on, because the baseline drive is
itself sub-spinodal. This matches the biology — human lactase is not re-induced. So the common
observation that regular dairy improves tolerance is not lactase returning; it is a layer
above the DNA switch (colonic microbiome and physiological tolerance), which this model does
not claim. The same machinery is trainable for a trait whose baseline drive clears the
spinodal: fixed versus trainable is sub- versus supra-spinodal baseline.

**What stays open.** Absolute methylation level, the absolute age of silencing, the rate
magnitudes, and the above-DNA plasticity are Layer-2 [O] — calibration and external data, not
sequence. What is admissible is which switch, the same-material check, the methylation
substrate read from structure, and the direction of its tuning.
