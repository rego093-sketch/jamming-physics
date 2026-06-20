# repro/dna/environment-methylation-layer

**v1.9 research extension — Workstream A: the environment-writable methylation layer M**

The worked answer to: *environment is reflected in DNA structurally — where is that
variable, and how do we READ it (instead of treating environment as a free external
scalar `h`)?* Validated on the **lactase locus** (LCT / MCM6), measured live from NCBI.

Claim grade: **principle-demonstration** (structure/direction `[F]`; absolute β/age `[O]`).

## What this closes

The interpreter reduces each promoter to one scalar `γ = mean(−NN dG)` (≈GC within a
catalog), *computes* `cpg_density`/`atrun` and then **discards** them; methylation/motif
reading is absent. But the layer where environment writes onto DNA — reversibly, at
specific CpG positions — is the CpG methylation substrate, which the preliminary
investigation showed is ~orthogonal to γ (`corr(CpG O/E, γ)=+0.42`, R²18%). The revised
constitution (I3 design clause) demands that an environment-sensitive trait state **which**
switch is built to be exposed to the drive, read from **structure** — not asserted. This
case cashes that note.

## The lactase result (all measured, READ-ONLY)

- `[F]` **SET conserved** — LCT present in human AND mouse.
- `[F]` **γ conserved** — `|Δγ(LCT)|` human–mouse = **0.034** < 0.05 (snake-ZRS "same
  material") → lactase persistence is **not** a difference in the LCT material.
- `[F]` **methylation substrate, read from structure** — the LCT regulatory region carries
  a **local CpG hotspot** (O/E_localmax **0.78**, 2.3× the 2.5 kb mean 0.34 that a single
  scalar erases), retained **1.8×** more than mouse → a methylation-tunable switch exists.
- `[F]` **same γ, opposite outcome** — adding M (seeded by the CpG substrate, driven by
  age) lowers the switch drive; non-persistence **silences** LCT (discontinuous R19 flip);
  the persistence cis variant (MCM6 −13910) keeps it ON. γ is identical in both → γ-blind,
  M-resolved.
- `[F]` **hysteresis** — once silenced, lowering methylation does **not** restore LCT
  (baseline drive is sub-spinodal). This matches the biology: human lactase is not
  re-inducible → the observed "drink milk and adapt" is a layer **above** the DNA switch
  (gut microbiome / physiology), explicitly **outside** this model.

What stays `[O]`: absolute methylation β, absolute age-of-silencing, the rate magnitudes
(κ, λ, h_base), and the microbiome/physiology plasticity. See `IRREPRODUCIBILITY_LEDGER.md`.

## Run

```bash
python3 run.py     # -> gate=PASS, determ=PASS, fidelity 100% -> SLUG VERIFICATION: PASS
```

Frozen reference output lives in `expected/`. The dynamics are pure arithmetic on locked γ
(deterministic, 2×sha256 identical). Measured sequence + provenance:
`../_engine/data/lactase_interpretation.json`; input FASTA mirrored in `inputs/`. Engine:
`../_engine/methylation_layer_4d.py`.

## Data provenance

`γ`/CpG computed with the kit pipeline (SantaLucia NN; Gardiner-Garden & Frommer O/E) on
promoter windows fetched live via NCBI efetch (2026-06-15): LCT human (GRCh38
NC_000002.12, TSS−2000..+500), Lct mouse (GRCm39 NC_000067.7), MCM6 −13910 enhancer
(GRCh38, ~14 kb upstream of LCT TSS). Coordinates from NCBI gene esummary.
