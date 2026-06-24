# Reproducibility — Continental Genesis & the Recent-Sequence Cascade

Paper ID: `continental-genesis-cascade`  ·  Code: `cgc`  ·  Tier 1 (Earth-science cluster)
Canonical whitepaper: https://jamming-physics.org/continental-genesis-cascade/
License: CC BY 4.0  ·  ORCID: 0009-0002-7535-8245

This single volume merges two source whitepapers under one jamming kernel. The
repro tree is split to match:

```
repro/continental-genesis-cascade/
├── genesis/   ← PART I  : Continental Genesis
│   ├── repro/        per-claim screening scripts (CG-1 … CG-39, AUDIT-1)
│   ├── modules/      derivation module pages
│   ├── inherited/    fluid-dynamics-engine inherited from the flow volume
│   └── tools/        build / hashing utilities
└── cascade/   ← PART II : Recent-Sequence Cascade
    ├── modules/             gate pages (S0, void-suction, deglaciation, causal closure …)
    ├── repro/               cascade screening scripts + data
    ├── inherited_engine/    void-suction + unjamming engine inherited from geodynamics
    ├── concepts/            cascade concept cards
    ├── cg_inheritance/      shared Continental-Genesis inheritance bridge
    ├── fossil_audit/        magnitude-ratio / occurrence-cap audit data + results
    ├── dna_emergence/       γ-atlas tie-ins (animal / plant)
    └── OPEN_FRONTIER.html, GLACIATION_PETROLEUM_OVERVIEW.html, …
```

## Paper ↔ repro ↔ DOI map

| Part | Source whitepaper                  | DOI                         | Repro subtree |
|------|------------------------------------|-----------------------------|---------------|
| I    | Continental Genesis (v1.9)         | 10.5281/zenodo.20827711     | `genesis/`    |
| II   | Recent-Sequence Cascade (v30)      | 10.5281/zenodo.20827806     | `cascade/`    |

Inherited volumes (LOCK, not re-derived here):
physics 10.5281/zenodo.17932566 · geodynamics 10.5281/zenodo.17978934 ·
geochronology 10.5281/zenodo.20568673 · fluid-dynamics 10.5281/zenodo.17972568 ·
dna 10.5281/zenodo.20471407.

Inherited modules: `kernel`, `dna_interpretation`, `rotor_inflow`.

## Method discipline

LOCK → Derive → Gate. No fitted parameters. γ values measured via the NCBI
SantaLucia-1998 nearest-neighbour ΔG pipeline. 2×SHA-256 determinism (`seed19`).
Honest grading: [F]orced / [V]erified / [O]pen / [L] hypothesis. Falsification = discovery.

Rendered grade totals for the merged volume: forced 43 · verified 15 · open 11 · hypothesis 10.

## Maintainer note (manifest regeneration)

The site manifest row for this volume was hand-appended (the 30 pre-existing
frozen rows are byte-identical). To regenerate `registry/vp.manifest.json` with
the standard tool instead, first register this volume in `tools/make_manifest.py`
by adding `continental-genesis-cascade` to the `ORDER` list and giving it an
entry in `REL` (inherits = [physics, geodynamics, geochronology, fluid-dynamics, dna];
adds = [continental-genesis, recent-sequence-cascade]), then add the matching
record to `tools/master.json`. Until then, do not re-run `make_manifest.py`
blindly, as it would drop the hand-appended row.
