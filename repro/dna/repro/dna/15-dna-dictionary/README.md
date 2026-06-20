# §II — The DNA Dictionary (engine-generated)

A **Dictionary of reads, not traits.** For each curated locus it lists ONLY the
locked engine's mechanical Layer-1 read — the material **γ** (stacking stiffness),
its R19 threshold scale (**spinodal** |h_sp| = (2/3√3)·γ^1.5, **barrier** γ²/4),
GC, CpG density, and whether the R19 well is **bistable** (can-fire). STATE (on/off),
sign, dosage and timing are **runtime** and are not assigned. Nothing is hand-labelled.

## Reproduce
```
python3 build_dictionary.py     # -> expected/dictionary.json (26 loci, sorted by γ)
python3 gate_dictionary.py      # -> OVERALL: PASS (2/2)
```

## Gate (fail-closed)
1. **Determinism** — `build()` twice; the two JSON dumps share one sha256.
2. **Baseline pin** — every reported value (γ, GC, CpG, spinodal, barrier) equals the
   frozen `../_verify/regression_baseline.json` to 1e-9 for all 26 covered loci.
   This anchors the Dictionary to the same locked truth the package regression pins;
   the engine re-derives **human_SOX2 γ = 1.287315** every run.

## What the table shows (read, do not over-read)
- 26 loci span **γ 1.264–1.444**; **all are R19-bistable** (every locus *can* fire — STATE is runtime).
- γ is an affine read of GC (the paper's corr(γ,GC)=0.998): the table sorts almost monotonically in GC.
- **human_ZRS γ=1.264** and **snake_LMBR1 γ=1.290** read nearly the same, yet the limb enhancer is ON in
  one lineage and OFF in the other — the Dictionary makes visible that **γ is blind to on/off**.
- Same gene across species sits at comparable γ (human/mouse SOX2, PAX6, OTX2 …) — the cross-species
  near-invariance, read locus-by-locus.

Engine: `repro/dna/_verify/engine/dna_interpreter.py` (locked). Sequences:
`repro/dna/_verify/inputs/sequences_v6/*.fa` (26 curated loci).
