# Hierarchical scale-renormalization interpreter — classifying the levels and climbing the tower

> ## INTEGRATED LAW — one renormalization operator, the whole biological tower · *(precision-exact scale renormalization — claim-strip)*
>
> **Appendix B dualized exactly TWO scales (cell `γ/A4`; tissue morphogen `LEVEL/SHAPE`) and treated
> them as UNCONNECTED — tissue constants were looked up, never *derived* from the cell — and carried
> only the CHEMICAL (morphogen) axis. That was an over-simplification on two counts: only two scales
> with no rule to climb between them, and the MECHANICAL axis missing entirely. This chapter repairs
> both. It CLASSIFIES every reading channel by the structural level it reads
> (`L0` molecular → `L1` cell → `L2` tissue → `L3` organ → `L4` body), and it CLIMBS the tower with a
> renormalization operator `R` so each level's stiffness, density and wave speed are *derived* from
> the level below by jamming physics — the formal statement of "세포들이 모이면 그자체로 부피이자
> 강성이 될것이다" (cells gather and become, by that very act, both VOLUME and STIFFNESS). The
> machinery is `[V]` exact to machine epsilon (precision earned); the ABSOLUTE biological moduli are
> `[O]` — accuracy NOT yet claimed, each behind a NAMED measured-data obstacle.**
>
> | renormalization channel | closed form | grade |
> |---|---|---|
> | density renormalization `ρ' = φ·ρ` | void carries no mass | **[V]** exact (mass/volume conservation) |
> | exact bracket `0 = B_Reuss ≤ B' ≤ B_Voigt = φ·B` | Reuss isostress / Voigt isostrain bounds | **[V]** exact theorems |
> | wave-speed softening per rung `c'/c = √J(φ)` | VP master `c²=B/ρ` applied twice | **[V]** exact (precision) |
> | RG composition `R∘R` (associativity) | climbing two rungs = one combined rung `<1e-9` | **[V]** exact (semigroup) |
> | rigidity onset `J(φ) = √((φ−φ_c)/(1−φ_c))` | `Δz ~ (φ−φ_c)^½` ∘ `G ~ Δz` | **[L]**-grounded (O'Hern 2003 + Wyart 2005) |
> | jamming anchors `φ_c, z_iso=2d, exponent ½` | published universals | **[L]** (O'Hern 2003; Maxwell) |
> | mechanical **LEVEL** = `mean(B(x))` | the effective modulus (how stiff) | **[V]** exact — mirrors cell **γ** |
> | mechanical **SHAPE** = `robust_z(B(x))` | the stiffness pattern (where stiff) | **[V]** exact — mirrors cell **A4** |
> | orthogonality **LEVEL ⟂ SHAPE** | SHAPE invariant under LEVEL moves to `~1e-15` | **[V]** exact |
> | scale classification (every channel → `L0..L4`) | a declaration, no fitted number | **[L]** grounded |
> | **ABSOLUTE modulus at each level (Pa)** | engine does NOT compare (would be back-fit) | **[O]** — needs elastography/AFM atlas |
> | **REAL per-rung packing fraction `φ(level)`** | demonstration profile stands in | **[O]** — needs stereology |
> | **REAL monotonicity vs ECM stiffening** | not modelled (cartilage/bone can raise `B`) | **[O]** — needs ECM modulus data |
>
> **Verification.** `python3 -m hierarchy.gate` passes **9/9** (`H1` effective modulus in the exact
> `[Reuss, Voigt]` bracket across a 400-point `φ` sweep · `H2` sharp jamming threshold (`J=0` below
> `φ_c`) · `H3` density renormalization exact · `H4` `√J` softening + RG composition · `H5`
> orthogonality to machine ε · `H6` zero inline magic numbers · `H7` non-fit invariant · `H8` 2×SHA-256
> determinism · `H9` honest grades **and** full scale-classification coverage). Completion is honestly
> **False**: three accuracy channels are `[O]` with named obstacles. Full ledger: `LEDGER.md`.

---

## Why this chapter exists

Appendix B made the tissue scale exact, but it left two things over-simplified.

**First, only two scales, unconnected.** It dualized the cell (`γ/A4`) and the tissue
(`LEVEL/SHAPE`) but treated them as two islands: the tissue's intrinsic length `λ` came from a
*looked-up* diffusion constant, not from anything the cell *is*. Real biology is not two scales —
it is a **tower**: molecule → cell → tissue → organ → body, and each level is built by **packing the
level below**. There was no operator that climbs it.

**Second, only the chemical axis.** Appendix B's tissue channel was the *morphogen* field — the
patterning/chemistry axis. But the user's instruction names a different, missing axis directly:
*"세포들이 모이면 그자체로 부피이자 강성이 될것이다"* — when cells gather they become, by that very
act, both a **volume** and a **stiffness**. That is **mechanics**, not chemistry, and Appendix B did
not have it.

This chapter supplies the missing operator. A packing of soft units at volume fraction `φ` acquires
its own bulk modulus `B` and density `ρ` — and the VP master relation `c² = B/ρ` (the SAME relation
the VP core thesis applies to the vacuum, *vacuum as a jammed elastic solid*) holds at **every**
level. The renormalization operator `R` is the map from the units' `(B, ρ)` to the aggregate's
`(B', ρ')`, applied one structural level up at a time.

---

## The renormalization operator R (one rung up)

For units `(B, ρ)` packed at volume fraction `φ`:

```
DENSITY  (the "부피/volume" half)   ρ' = φ·ρ                         — EXACT, void has no mass   [V]
STIFFNESS(the "강성/stiffness" half) 0 = B_Reuss ≤ B' ≤ B_Voigt = φ·B — EXACT elastic-mixture bracket [V]
                                    B' = φ·B·J(φ),  J(φ) ∈ [0,1]     — placed in the bracket by jamming
VP MASTER(the through-line)         c' = √(B'/ρ') = c·√J             — EXACT, c²=B/ρ applied twice  [V]
```

so the **wave-speed softening ratio per rung is exactly `√J`**, and because `J ∈ [0,1]` the
mechanical signal speed **decreases monotonically** up the tower for any `φ<1` (an exact RG theorem
of the idealized ladder). The rigidity fraction

```
J(φ) = 0,                          φ ≤ φ_c    (unjammed → fluid → Reuss floor)
J(φ) = √((φ − φ_c)/(1 − φ_c)),     φ >  φ_c
```

has a **`[L]`-grounded shape**: it is the composition of two *cited universals* — the excess
coordination `Δz ~ (φ−φ_c)^½` (O'Hern, Silbert, Liu & Nagel 2003) and the rigidity `G ~ Δz`
(Wyart, Nagel & Witten 2005). The `[0,1]` normalization is a documented bounding choice; the two
**exact** bounds (Reuss `0`, Voigt `φ·B`) are what the gate enforces, and the effective modulus is
*guaranteed* to lie inside them.

That the jamming transition admits a renormalization-group / scaling description at all is itself
grounded (Goodrich, Liu & Sethna 2016), as is applying jamming to a packing of **cells** rather than
inert grains (Bi, Lopez, Schwarz & Manning 2015).

---

## The classification (the "분류")

Every reading channel in the corpus is tagged with the structural level it reads and how it connects
to the tower, in ONE place (`hierarchy/classify.py`) so the scale of every read is declared and
cannot drift:

| channel | reads level | connects to the tower |
|---|---|---|
| NN stacking ΔG → `γ` (material LEVEL) | `L0` molecular → `L1` cell | sets `B` at the BASE (the cell's intrinsic stiffness) |
| `A4` coordinate (shell / anchor / phase) | `L0` → `L1` | the cell-level instance of the LEVEL/SHAPE split |
| `R19` switch (spinodal, barrier) | `L1` cell | intra-cell; orthogonal to the mechanical tower |
| CpG O/E → methylation drive `h` | `L1` cell (env. write) | intra-cell; orthogonal to the mechanical tower |
| morphogen `LEVEL = mean(c)` → SIZE | `L2` tissue | the CHEMICAL axis at `L2` — runs *alongside* the tower |
| morphogen `SHAPE = robust_z(c)` → FORM | `L2` tissue | the territories ARE the `φ(x)` domains the mechanical SHAPE reads |
| packing `φ`, jamming `J`, `B_eff, ρ_eff, c_eff` | `L1→L4` (every rung) | **IS** the tower (the operator `R`) |
| isostatic `z_iso = 2d` | structural invariant | the universal anchor that makes rigidity parameter-free |
| VP master `c² = B/ρ` | `L0→L4` (through-line) | the invariant carried up every rung; softens by `√J` |

The chemical axis (Appendix B) and the mechanical axis (this appendix) **meet** at the tissue
territories: the morphogen `SHAPE` defines the territories, and those territories are the natural
packing-fraction domains `φ(x)` that the mechanical `SHAPE` reads.

---

## The climb (a worked demonstration)

Starting at the cell with a generic `B₀ = 1 kPa` `[O]` and `ρ₀ = 1070 kg/m³` `[L]`, and a
documented jammed `φ` profile `[F]` (each rung above `φ_c`, standing in for measured stereology
`[O]`), the operator climbs:

| level | φ | B (Pa) | ρ (kg/m³) | c (m/s) | `c/c_prev = √J` |
|---|---|---|---|---|---|
| cell | base | 1000.0 | 1070.0 | 0.9667 | — |
| tissue | 0.7292 | 364.63 | 780.30 | 0.6836 | 0.707107 |
| organ | 0.8195 | 211.29 | 639.45 | 0.5748 | 0.840896 |
| organ system / body | 0.9097 | 166.47 | 581.74 | 0.5349 | 0.930605 |

The wave speed decreases monotonically (each `√J < 1`). **The softening ratio per rung is EXACT;
the absolute moduli are `[O]`** — swapping the demonstration `φ` profile and `B₀` for a measured
elastography/AFM atlas changes only the numbers, never the machinery (the gate's non-fit invariant,
`H7`, asserts exactly this).

---

## The mechanical LEVEL / SHAPE (the cell γ/A4 split, lifted to the aggregate)

At any structural level the spatial stiffness map `B(x) = B_unit · φ(x) · J(φ(x))` is read two
orthogonal ways, with the SAME `robust_z` operator as the cell-level `A4` (byte-for-byte):

| | LEVEL (γ-mirror) | SHAPE (A4-mirror) |
|---|---|---|
| reads | **how stiff** (the effective modulus) | **where stiff** (the stiffness pattern + cliffs) |
| operator | `mean(B(x))` | `robust_z(B(x)) = (B − median)/(1.4826·MAD)` |
| under "scale the field" | scales | **invariant** (to `~1e-15`) |
| under "add a stiffness background" | shifts | **invariant** (to `~1e-15`) |
| under "change the packing geometry" | rescalable | **moves** (it is the shape) |

The bottom three rows are the orthogonality proof: SHAPE ignores everything LEVEL responds to and
moves only when the geometry — the actual stiffness pattern — changes. `LEVEL ⟂ SHAPE`, exactly,
with no "approximately."

---

## What is honestly NOT done (the three [O] obstacles)

Precision is not accuracy. The operator computes the softening trajectory and the stiffness
pattern *exactly*, but it **never compares them to a real organ's measured stiffness**, because
doing so without measured data would be back-fitting. Three named obstacles stand between this
chapter and an accuracy claim:

1. **ABSOLUTE modulus at each level — `[O]`.** Needs a *measured* per-scale modulus atlas
   (elastography MRE/USE, AFM nanoindentation, micro-rheology) across cell → tissue → organ.
2. **REAL per-rung packing fraction — `[O]`.** Needs *measured* cell packing fraction at each level
   (confocal/EM stereology), plus the ECM volume fraction.
3. **REAL monotonicity vs ECM stiffening — `[O]`.** The idealized flow softens monotonically; real
   extracellular-matrix mineralization (cartilage, bone) can *raise* the unit modulus and break it.
   Closing it needs the per-tissue ECM stiffness contribution.

Until those datasets are supplied and a pre-registered test (predicted softening vs a measured
elastography ladder, with a shuffle control and a pre-registered sign) is run, the honest grade is
`[O]`, and `completion.complete` is **False**. This is the handover's anti-false-victory rule,
enforced in one place (`hierarchy/grading.py`).

---

## Layout

```
ax-c-hierarchical-renormalization/
├── param_db.json            constants (jamming φ_c/z_iso/exponents, composite bounds, ladder, unit
│                            mechanics) with grade + provenance — the ONLY source of numbers
├── run.py                   top-level runner → writes expected/*.json + RESULT.txt
├── README.md                this file
├── LEDGER.md                per-channel grade ledger (honest [L]/[V]/[F]/[O])
├── hierarchy/
│   ├── __init__.py          package surface
│   ├── lock.py              LOCK: every constant from param_db.json; lock_manifest() ⇒ magic-numbers = 0
│   ├── jamming.py           rigidity emergence J(φ): the "강성/stiffness" half (O'Hern + Wyart, cited)
│   ├── renorm.py            the operator R: ρ'=φρ, the exact Reuss/Voigt bracket, c'=c·√J, composition
│   ├── ladder.py            the explicit biological tower + climb() (each level DERIVED from below)
│   ├── level.py             mechanical LEVEL = mean(B(x)) (the γ-mirror)
│   ├── shape.py             mechanical SHAPE = robust_z(B(x)) (same robust_z as cell-level A4)
│   ├── orthogonality.py     two-knob + geometry-panel proof that LEVEL ⟂ SHAPE
│   ├── classify.py          the scale-classification ledger: every channel tagged L0..L4 (the "분류")
│   ├── grading.py           the ONE place precision≠accuracy is enforced; LEDGER + completion_status
│   ├── interpreter.py       interpret_hierarchy() = classify ⊕ climb ⊕ LEVEL/SHAPE ⊕ orthogonality ⊕ grades
│   └── gate.py              fail-closed gate H1..H9;  python3 -m hierarchy.gate
└── expected/                deterministic outputs (regenerated by run.py)
```

## Reproduce

```bash
cd ax-c-hierarchical-renormalization
python3 -m hierarchy.gate     # H1..H9, exit 0 iff all pass
python3 run.py                # prints the classification + climb; writes expected/*.json + RESULT.txt
```

Both are deterministic: re-running yields byte-identical serializations (2×SHA-256).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
