# IRREPRODUCIBILITY LEDGER — 16-muscle-force-length (VP-SPEC C3)

Every `[O]` item in this slug, its **specific obstacle**, and its location. Per Constitution
C3, an `[O]` without a stated obstacle is a gate FAIL. The reproducible part (the force–length
law on the descending limb and plateau) is **derived from locked structural constants and
validated against GHJ-1966 measured landmarks** — the three single-valued landmarks
(zero_long, plateau_bot, steepen) to max |Δ| = 0.020 µm, and the plateau top by **containment**
(the measured 2.20 falls at the lower edge of the derived 2.20–2.25 range, not an exact-endpoint
hit); only the items below are `[O]`.

| # | `[O]` item | obstacle (why it cannot be derived here) | location |
|---|------------|-------------------------------------------|----------|
| M1 | **short-side zero at ≈1.27 µm** | The short-side zero is a thick-filament **crumpling/buckling** limit. It is set by the filament's mechanical compliance under axial compression against the Z-discs, not by overlap length. Length geometry derives the *onset* of Z-collision (steepen = A+z = 1.65 µm) but not the force-zero of the deformed filament. | `vp_muscle_force_law.py` `[O]` block; `force_length()` returns NaN below plateau |
| M2 | **ascending-limb tension values (S < 2.05 µm)** | Below the plateau, opposing thin filaments double-overlap, drag with wrong polarity, and the lattice compresses. Net tension depends on interference + compliance, not on a single overlap length, so it is not derivable from the locked dimensions alone. | same block; curve returns `[O]` for S<plateau_bot |
| M3 | **absolute tension scale (N or N·m⁻²)** | Only the *normalised* shape is geometric. Absolute force needs cross-bridge **number × unitary force × activation fraction** — none fixed by filament length. | header LOCK note; `force_length()` is 0..1 |
| M4 | **filament dimensions from ruler-protein sequence** | The thin-filament length is biologically set by **nebulin** (a molecular ruler) and the thick filament by titin/myosin packing. Deriving A, I from NEB/TTN sequence (repeat count → length) is an open structural-biology mapping (contested repeat-to-length stoichiometry), so the dimensions are taken as the measured **LOCK**, not re-derived. | header LOCK; this is why A, I, b, z are inputs |

## What is NOT in this ledger (because it reproduces)

- `zero_long = A + 2I + z = 3.65 µm` — derived, matches GHJ measured 3.65 (|Δ|=0).
- `plateau_bot = 2I + z = 2.05 µm` — derived, matches GHJ 2.05 (|Δ|=0).
- `plateau_top = 2I + z + b = 2.20–2.25 µm` — derived as a RANGE (the bare zone `b` is itself a measured range [0.15, 0.20] µm, so the plateau top is a range, not a single number). GHJ's measured 2.20 is validated by **CONTAINMENT** — it falls at the **lower edge** of the derived range — NOT by an exact-endpoint `|Δ|=0` hit. Reporting `|Δ|=0` would require picking `b=0.15` to land on the target, which is choosing a number to hit a measurement; VP-SPEC C1 forbids that.
- `steepen = A + z = 1.65 µm` — derived (thick ends bump Z-discs), matches GHJ 1.67 (|Δ|=0.02).
- descending-limb tension **linear in overlap** between plateau_top and zero_long — the core GHJ result, derived.

## Cross-reference to sibling reproductions (other slugs / sessions)

- **MYOD1 cell-fate γ window** is `[O]` in the muscle-cell emergence: MYOD1 is NCBI-real
  (Gene 4654, chr11 NC_000011.10:17719570–17722135) but the exact 2501-bp window for γ=1.4933 is
  **undocumented** in the framework (locus γ brackets 1.44–1.56) — unlike LCT, whose window was
  bundled and NCBI-verified. Obstacle: missing provenance, not missing physics.
- **Neural-code decoding** is `[O]` framework-wide: the neural signal *is* electromagnetic and is
  measured (electrophysiology = E-face, MEG = B-face); what is open is the precise **information
  content** of the spike/field patterns, not the existence of the EM signal.
