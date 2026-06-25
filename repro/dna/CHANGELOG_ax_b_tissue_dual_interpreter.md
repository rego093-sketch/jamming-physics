# CHANGELOG — Appendix B · the cell-level γ/A4 LEVEL–SHAPE split lifted exactly to the tissue scale

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.13 (γ↔A4 stated as LEVEL vs SHAPE). This increment adds **Appendix B — Tissue-level dual
interpreter**, a new applied volume that takes the cell-level level/shape decomposition and proves the
*tissue* level admits the same split, **made exact**. It is **add-only**: no chapter, appendix, number,
grade, equation, table, or DOI of v1.13 is altered. One new section is added (the site goes from 17 to
18 sections), the contents/sitemap/manifest/meta are extended, and Appendix A gains a forward nav link.

## Why

DNA is read at more than one scale. v1.13 made the **cell**-level read dual: one stiffness signal `s(x)`
projected into **γ = LEVEL = mean(s)** (how much) and the **A4 coordinate = SHAPE = robust_z(s)** (the
pattern, mean removed), two orthogonal projections of one field. The **tissue**-level read in Appendix A,
by contrast, grew form **roughly**: a coarse 32-point Jacobi relaxation, a one-dimensional axis collapse
taken on faith, an integer-floor territory count, and two inline constants — a dwell gain and a brake —
that appear in no parameter database. That is *precision theatre*: it returns a number, but the number
carries a discretization error and rests on unstated constants.

The cell level shows the standard to meet. The correct fix is therefore **not to tune the Jacobi solver**
but to find the same dual structure at the tissue scale and make it exact. It exists, because the
morphogen obeys a **linear** equation.

## The relationship, stated once (Appendix B states it at the tissue scale)

> **One morphogen field. LEVEL is its mean. SHAPE is the same field with that mean removed.** The steady
> screened-Poisson gradient `D·∇²c − c/τ + source = 0` has a single length scale `λ = √(Dτ)`. For a full
> source face with zero-flux side walls the field is **exactly one-dimensional** (transverse variance is
> zero, not small) with the closed form `c(x) = cosh((L−x)/λ)/cosh(L/λ)`. From it:
> **LEVEL = mean(c) = (λ/L)·tanh(L/λ) → SIZE** (the tissue mirror of γ) and
> **SHAPE = robust_z(c) → FORM**, with territory boundaries `x_k = L − λ·acosh(θ_k·cosh(L/λ))`
> (the tissue mirror of A4, using the **identical** `robust_z` operator). `LEVEL ⟂ SHAPE`, exactly.

Verified: the LEVEL integral matches a two-million-point quadrature to **< 1e-9**; every territory
boundary reproduces its own threshold `c(x_k)=θ` to **ten decimals**; SHAPE is invariant under scaling
the source (to ~5×10⁻¹⁵) and adding a background (to ~9×10⁻¹⁵) and moves only when the geometry changes.
The old Jacobi solver recovered `λ` as **60.55 µm vs the exact 60.00** — a **0.92% coarse-grid artifact**
— and is retained **only** as a convergence witness whose error shrinks toward the exact value as the
grid refines, proving the roughness was the *solver*, not the physics.

## What is honestly NOT claimed (the two open obstacles)

Precision is not accuracy. The interpreter computes the size **budget** and the form **partition**
exactly, but it **never compares them to a real organ**, because doing so without measured data would be
back-fitting. Two named obstacles stand between Appendix B and an accuracy claim, both graded **[O]**:

1. **SIZE magnitude vs real organ mass** — needs a measured per-organ developmental growth-rate atlas.
2. **FORM partition vs real anatomy** — needs measured chromatin contact (Hi-C / Micro-C / capture-C) or
   a staged tissue-territory boundary map, then a pre-registered rank test with a shuffle control.

Until those datasets are supplied and the pre-registered test is run, the honest grade is **[O]** and
`completion.complete` is **False**. This is the anti-false-victory discipline, enforced in exactly one
place in the code (`tissue/grading.py`).

## What changed (all add-only)

New reproduction package `repro/dna/ax-b-tissue-dual-interpreter/`:

- `tissue/` — 8 modules + package init: `lock` (every constant from `param_db.json`, **zero inline magic
  numbers**), `field` (exact closed forms — planar `cosh` + 3-D Yukawa with a self-contained Lambert W —
  plus the old Jacobi kept only as a witness), `level` (LEVEL→SIZE), `shape` (SHAPE→FORM, the same
  `robust_z` as the cell-level A4), `orthogonality` (two-knob + geometry-panel proof), `grading` (the one
  place precision≠accuracy lives; honest `[L]/[V]/[F]/[O]` ledger + `completion_status`), `interpreter`
  (`interpret_tissue` = LEVEL ⊕ SHAPE ⊕ orthogonality ⊕ grades), `gate` (fail-closed G1–G7).
- `run.py`, `README.md`, `LEDGER.md`, `param_db.json`, `expected/` (deterministic outputs).
- **Verification:** `python3 -m tissue.gate` → **PASS 7/7** (G1 exactness < 1e-9 · G2 supersession of the
  coarse Jacobi · G3 orthogonality to machine ε · G4 zero magic numbers · G5 non-fit invariant · G6
  2×SHA-256 determinism · G7 honest grades, completion False).

New site section `docs/dna/ax-b-tissue-dual-interpreter/index.html` (VP-SPEC structure: answer-first,
`vp-card` declaration blocks, `claim-strip`, prev/next nav), plus registrations:

1. **`docs/dna/index.html`** — Appendix B added to the JSON-LD `hasPart` series, the contents list
   (`<li class="apx">`), and the key-findings cross-links.
2. **`docs/dna/_meta.json`** — Appendix B appended to `appendices` (id `B`, repro path, verify line,
   `central_result_grade: precision-verified / accuracy-open`).
3. **`docs/dna/ax-a-universal-morphogenesis-gene-clock/index.html`** — footer nav gains `Appendix B →`.
4. **`docs/sitemap.xml`** — new URL added (lastmod 2026-06-25).
5. **`manifest/dna.csv`** — Appendix B row appended.
6. **`gate_multipage.py`** — section/hub counts updated 17 → 18; site gate re-run **PASS 208 / FAIL 0**.

## Relationship to the handover ledger

This addresses two frozen items in `HANDOVER_dna_v1_13`:

- **M1** (the dynamic channel was never run; only the static γ-LEVEL projection): the tissue read here
  *is* the dynamic morphogen channel — the steady state of reaction-diffusion — now run in closed form
  rather than on a coarse grid, with the honest accuracy gap named as **[O]**, not declared closed.
- **M5** (single-cell "accuracy" is really precision): the same precision≠accuracy discipline is now
  enforced at the tissue scale, with the size/form machinery graded `[V]` (precision) and the map to real
  organs graded `[O]` (accuracy untested).

It advances the rigor frontier's **P4** (SHAPE on real regions against contact data) and **P5** (the
dynamic field), supplying the exact dynamic field and the exact SHAPE partition, and stating precisely
which measured datasets would convert each from precision to accuracy.

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
