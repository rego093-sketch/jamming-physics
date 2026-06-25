# CHANGELOG — Appendix C · classifying the levels and climbing the tower by scale renormalization

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.13 + Appendix B (cell γ/A4 and tissue LEVEL/SHAPE, two scales). This increment adds
**Appendix C — Hierarchical renormalization interpreter**, a new applied volume that repairs Appendix B's
over-simplification on two counts: it used only **two** scales, left **unconnected**, and carried only the
**chemical** (morphogen) axis. It is **add-only**: no chapter, appendix, number, grade, equation, table, or
DOI of v1.13 or Appendix B is altered. One new section is added (the site goes from 18 to **19** sections),
the contents/sitemap/meta/gate are extended, and Appendix B gains a forward nav link.

## Why

DNA is read at more than one scale, and the body is not two scales but a **tower**: molecule → cell →
tissue → organ → body, where each level is **built by packing the level below**. Appendix B made the
tissue scale exact, but it left two things over-simplified.

1. **Only two scales, unconnected.** It dualized the cell (γ/A4) and the tissue (LEVEL/SHAPE) but treated
   them as islands: the tissue's intrinsic length `λ` came from a *looked-up* diffusion constant, not from
   anything the cell *is*. There was no operator that climbs the tower and *derives* a level from the one
   below.
2. **Only the chemical axis.** Appendix B's tissue channel was the *morphogen* field — patterning/chemistry.
   The instruction driving this work names the missing axis directly: **"세포들이 모이면 그자체로 부피이자
   강성이 될것이다"** — when cells gather they become, by that very act, both a **volume** and a
   **stiffness**. That is **mechanics**, and the two-scale chemical picture did not have it.

The fix is **not** to bolt more chemistry on, but to supply the missing **mechanical renormalization
operator** and a **classification** that says, for every channel, which level it reads. A packing of soft
units at volume fraction `φ` acquires its own modulus and density, and the VP master relation `c² = B/ρ`
— the **same** relation the core thesis applies to the vacuum as a jammed elastic solid — holds at every
level.

## The operator, stated once (Appendix C applies it one rung up)

> **Units `(B, ρ)` packed at fraction `φ` become an aggregate.** Density renormalizes exactly:
> `ρ' = φ·ρ` (void carries no mass). Stiffness is bracketed by two **exact** elastic-mixture theorems —
> Reuss isostress floor `0` (an unjammed packing has no rigidity) and Voigt isostrain ceiling `φ·B` — and
> placed inside the bracket by the jamming rigidity fraction: `B' = φ·B·J(φ)`. The wave speed renormalizes
> as `c' = √(B'/ρ') = c·√J`, so the **softening ratio per rung is exactly `√J`**, and because `J ∈ [0,1]`
> the mechanical signal speed **decreases monotonically** up the tower for any `φ < 1`.

The rigidity fraction has a **grounded** shape, not a fitted one:

```
J(φ) = 0,                          φ ≤ φ_c    (fluid; Reuss floor)
J(φ) = √((φ − φ_c)/(1 − φ_c)),     φ >  φ_c
```

It is the composition of two **cited universals**: the excess coordination above the isostatic Maxwell
count `z_iso = 2d` grows as `(φ − φ_c)^½` (O'Hern, Silbert, Liu & Nagel 2003, PRE 68:011306), and the
rigidity that emerges continuously at the transition grows linearly in that excess coordination (Wyart,
Nagel & Witten 2005, EPL 72:486). The `[0,1]` normalization is a documented bounding choice; the two exact
bounds are what the gate enforces. The renormalization-**group** framing — repeated coarse-graining — is
itself grounded in the jamming transition's emergent scale invariance (Goodrich, Liu & Sethna 2016, PNAS
113:9745) and its application to **cell** packings, not just inert grains (Bi, Lopez, Schwarz & Manning
2015, Nat. Phys. 11:1074).

Verified (gate **9/9**): across a 400-point `φ` sweep the effective modulus **always** lies in the exact
`[Reuss, Voigt]` bracket; below `φ_c` the rigidity fraction is **exactly 0** (sharp onset); the density law
`ρ' = φ·ρ` is exact to machine epsilon; the softening ratio equals `√J` exactly and the operator
**composes** (climbing two rungs equals one combined rung to `< 1e-9` — a consistent RG semigroup); the
mechanical LEVEL/SHAPE are orthogonal to machine epsilon with the **identical** `robust_z` operator as the
cell-level A4; zero inline magic numbers; non-fit invariant (identical output with a decoy target present);
2×SHA-256 determinism; honest grades with full scale-classification coverage.

Demonstration climb (generic cell `B₀ = 1 kPa` [O], `ρ₀ = 1070 kg/m³` [L], documented jammed `φ` profile
[F]): wave speed `0.9667 → 0.6836 → 0.5748 → 0.5349` m/s across cell → tissue → organ → body, with exact
per-rung `√J = 0.7071 / 0.8409 / 0.9306`, monotone decreasing.

## The classification (the "분류")

`hierarchy/classify.py` tags **every** corpus reading channel with the structural level it reads and how it
connects to the tower, in one place so scale cannot drift: NN-stacking → γ sets `B` at the **base** (L0→L1);
the A4 coordinate is the cell-level instance of the split (L0→L1); the R19 switch and methylation drive are
intra-cell, **orthogonal** to the mechanical tower (L1); the morphogen LEVEL/SHAPE are the **chemical** axis
at L2, running **alongside** the tower; the packing `φ`/`J`/`B_eff`/`ρ_eff`/`c_eff` **are** the tower
(L1→L4); `z_iso` is the universal anchor; `c²=B/ρ` is the through-line (L0→L4). The chemical and mechanical
axes **meet** at the tissue territories: the morphogen SHAPE defines the territories, and those territories
are the natural packing-fraction domains the mechanical SHAPE reads.

## What is honestly NOT claimed (the three open obstacles)

Precision is not accuracy. The operator computes the softening trajectory and the stiffness pattern
exactly, but it **never compares them to a real organ's measured stiffness**, because doing so without
measured data would be back-fitting. Three named obstacles stand between Appendix C and an accuracy claim,
all graded **[O]**:

1. **ABSOLUTE modulus at each level** — needs a measured per-scale modulus atlas (elastography MRE/USE, AFM
   nanoindentation, micro-rheology) across cell → tissue → organ.
2. **REAL per-rung packing fraction** — needs measured cell packing fraction at each level (confocal/EM
   stereology) plus the ECM volume fraction.
3. **REAL monotonicity vs ECM stiffening** — extracellular-matrix mineralization (cartilage, bone) can
   *raise* the unit modulus and break the monotonic softening; not modelled, flagged as the obstacle.

Until those datasets are supplied and a pre-registered test of the predicted softening trajectory against a
measured elastography ladder is run with a shuffle control, the honest grade is **[O]** and
`completion.complete` is **False**. The discipline is enforced in exactly one place (`hierarchy/grading.py`).

## What changed (all add-only)

New reproduction package `repro/dna/ax-c-hierarchical-renormalization/`:

- `hierarchy/` — 11 modules + package init:
  - `lock` (every constant from `param_db.json`, **zero inline magic numbers**; `lock_manifest()`),
  - `jamming` (rigidity emergence `J(φ)`: the "강성/stiffness" half — O'Hern + Wyart, cited),
  - `renorm` (the operator `R`: `ρ'=φρ`, the exact Reuss/Voigt bracket, `c'=c·√J`, and `compose_two` for the
    RG-semigroup associativity witness),
  - `ladder` (the explicit biological tower + `climb()` — each level *derived* from the one below),
  - `level` (mechanical LEVEL = `mean(B(x))`, the γ-mirror),
  - `shape` (mechanical SHAPE = `robust_z(B(x))`, **byte-identical** `robust_z` to the cell-level A4),
  - `orthogonality` (two-knob + geometry-panel proof that LEVEL ⟂ SHAPE),
  - `classify` (the scale-classification ledger — the "분류"),
  - `grading` (the **one** place precision ≠ accuracy is enforced; `LEDGER` + `completion_status`),
  - `interpreter` (`interpret_hierarchy()` = classify ⊕ climb ⊕ LEVEL/SHAPE ⊕ orthogonality ⊕ composition ⊕
    grades; `reading_hash` 2×SHA-256),
  - `gate` (fail-closed `H1..H9`; `python3 -m hierarchy.gate`).
- `param_db.json` — jamming anchors (`φ_c`, `z_iso=2d`, exponents), exact composite bounds, the ladder length
  scales, and the unit mechanics, each with grade + provenance.
- `run.py` — top-level runner → `expected/*.json` + `RESULT.txt` (deterministic; 2×SHA-256).
- `README.md`, `LEDGER.md` — the integrated-law claim-strip and the honest per-channel grade ledger.

New HTML section `docs/dna/ax-c-hierarchical-renormalization/index.html` (VP-SPEC v1.8, answer-first,
prev → Appendix B).

Site wiring (extended, not rewritten):
- `docs/dna/_meta.json` — appendix **C** row appended (chapters 16 + appendices 3 = 19).
- `docs/sitemap.xml` — AX-C URL added (hub + 19 = 20 `<loc>`).
- `docs/dna/index.html` — hub TOC `<li class="apx">`, JSON-LD `hasPart`, see-also cross-link, and the
  overview count ("one applied appendix" → "three applied appendices").
- `docs/dna/ax-b-tissue-dual-interpreter/index.html` — forward nav `Appendix C →`.
- `gate_multipage.py` — section/hub-link count `18 → 19`.

## Verification

- `python3 -m hierarchy.gate` → **PASS 9/9** (`H1` bracket · `H2` jamming threshold · `H3` density exact ·
  `H4` √J + RG composition · `H5` orthogonality · `H6` no magic · `H7` non-fit · `H8` determinism · `H9`
  grades + scale coverage); `completion.complete = False`.
- `python3 run.py` → deterministic; reference hierarchical reading hash `cc6d03258ecc6a10`; gate
  `sha=9e8092715032c8a5`.
- `python3 gate_multipage.py` → **PASS 219, WARN 1, FAIL 0** (the single WARN is the pre-existing
  source-monolith diff that is warn-only).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
