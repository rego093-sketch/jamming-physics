# repro/dna/lactase-three-layer-stack

**v1.9 research extension — the COMPLETE lactase interpretation: γ → M → E, no gray zone**

Brings the three layers together on one locus and produces an **exhaustive [F]/[O] ledger**.
The point is not a new dynamical trick — it is *completeness*: every quantity of the lactase
interpretation is graded **[F]** (read from structure) or **[O]** (open, with a stated
obstacle). Nothing is left silently unaddressed. That is what "no gray zone" means — not that
sequence yields everything (it cannot), but that the boundary is exhaustive and explicit.

Claim grade: **principle-demonstration** · `LEDGER_no_gray_zone.md` is the headline artifact.

## The three layers

- **γ (material)** — LCT conserved human+mouse, |Δγ|=0.034 (same material). Persistence is not
  a γ difference. Fully [F].
- **M (methylation substrate)** — local CpG hotspot (O/E 0.78) is where environment writes; same
  γ + two methylation trajectories → opposite, discontinuous, hysteretic STATE. Structure/
  direction [F]; absolute β/age/rates [O].
- **E (structure)** — the layer the gray zone was hiding. DNA is read structurally, not linearly:
  the helix and folding bring distant positions together.
  - **E1 helical/nucleosome** — the WW ~10.4 bp arrangement signal (LCT ACF 100th pctl vs
    shuffle) gates the substrate's accessibility; γ sees 0% (it is in the order). The gate's
    direction (occluded → drive cannot reach → switch frozen) is [F]; actual occupancy [O] (MNase-seq).
  - **E2 looping** — LCT promoter + MCM6 enhancer (~14 kb, within loop range) read as one unit
    [F-direction]; actual contact [O] (Hi-C).

## The integration (R19)

`state = settle(γ, a_acc · (H_BASE − λ·M(age)))` — γ read-only material; M the methylation
substrate drift; a_acc the structural accessibility gate. Three [F] axes (material, methylation,
accessibility), each demonstrated.

## Run

```bash
python3 run.py     # -> gate=PASS, determ=PASS, fidelity 100% -> SLUG VERIFICATION: PASS
```

`LEDGER_no_gray_zone.md` (the exhaustive grade table) is regenerated from the engine results.
Frozen output: `expected/`. Measured features: `../_engine/data/lactase_interpretation.json`
(γ + CpG + structure, all READ-ONLY, NCBI efetch). Engine: `../_engine/lactase_three_layer_4d.py`.

## Honest boundary

The **[O]** items are the explicit edge of what sequence yields; each names the external
measurement (WGBS, MNase-seq, Hi-C) that would close it. **Orthogonal ≠ predictive**: the
E-layer signals are shown to exist and be γ-invisible; whether they improve phenotype prediction
is the external-data validation task, not claimed here.

- `structure_signals.py` + `expected/structure_signals.json`: deterministically reproduces the Layer-E sequence-intrinsic structure signals (helical ACF/percentile, poly(dA:dT) density, CTCF core scan) the engine reads as [F] from `inputs/human_LCT_promoter.fa`. Wires the formerly-frozen `["structure"]` constants (0 drift); run twice -> bit-identical.
