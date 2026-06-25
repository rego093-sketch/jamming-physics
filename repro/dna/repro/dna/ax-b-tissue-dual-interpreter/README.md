# Tissue-level DUAL interpreter — lifting the cell-level γ/A4 split to the tissue scale (이원화)

> ## INTEGRATED LAW — one morphogen field, two orthogonal projections · *(precision-exact tissue dualization — claim-strip)*
>
> **At the cell level, ONE stiffness signal `s(x)` is read two orthogonal ways: `γ = LEVEL = mean(s)`
> (how much) and `A4 = SHAPE = robust_z(s)` (the pattern, mean removed). This chapter proves the
> *tissue* level admits the SAME dualization, made EXACT. ONE morphogen field `c(x)` solving the
> screened-Poisson equation `D·∇²c − c/τ + source = 0` is read two orthogonal ways: `LEVEL = mean(c)
> → SIZE` and `SHAPE = robust_z(c) → FORM` (territory boundaries). The two readings are orthogonal
> projections of the same field, exactly as γ and A4 are. The size and form machinery is `[V]` exact
> to machine epsilon (precision earned); the map from this machinery to a real organ's *mass* and a
> real tissue's *anatomy* is `[O]` — accuracy NOT yet claimed, each behind a NAMED measured-data
> obstacle. This supersedes Appendix A's coarse N=32 Jacobi morphogenesis solver, which is retained
> ONLY as a convergence witness that demonstrates its own roughness.**
>
> | tissue channel | closed form | mirrors (cell level) | grade |
> |---|---|---|---|
> | intrinsic length `λ = √(Dτ)` | `60.0 µm` from measured `D, τ` | the material constant | **[L]**-grounded (Kicheva 2007) |
> | **LEVEL** = `mean(c)` → **SIZE** | `(λ/L)·tanh(L/λ)` | **γ** = window-mean of `s` | **[V]** exact (precision) |
> | **SHAPE** = `robust_z(c)` → **FORM** | `x_k = L − λ·acosh(θ_k·cosh(L/λ))` | **A4** = `robust_z(s)` (same operator) | **[V]** exact (precision) |
> | orthogonality **LEVEL ⟂ SHAPE** | SHAPE invariant under scale & offset to `~5e-15` | γ ⟂ A4 (ρ=0.939 same field, max\|corr\|=0.327) | **[V]** exact |
> | territory threshold `θ` | positional-information cutoff | the R19 switch point | **[F]** (θ-robust over [0.3, 0.7] required) |
> | supply exponent `α` (extent ~ `devtime^α`) | one UNIVERSAL rule, never per-organ | the segmentation-clock dosage | **[F]** model-only |
> | **SIZE magnitude vs real organ mass** | engine does NOT compare (would be back-fit) | dwell null (ρ=0.11) at cell level | **[O]** — needs growth-rate atlas |
> | **FORM partition vs real anatomy** | engine does NOT compare (would be back-fit) | exact-anatomy null at cell level | **[O]** — needs Hi-C/Micro-C contact map |
>
> **Verification.** `python3 -m tissue.gate` passes **7/7** (`G1` exactness <1e-9 · `G2` supersession
> of the coarse Jacobi · `G3` orthogonality to machine ε · `G4` zero inline magic numbers · `G5`
> non-fit invariant · `G6` 2×SHA-256 determinism · `G7` honest grades, no false victory). Completion
> is honestly **False**: the two accuracy channels are `[O]` with named obstacles. Full ledger:
> `LEDGER.md`. The old `emergence_trajectory.py` N=32 Jacobi (λ recovered as 60.55 µm, a **0.92%
> coarse-grid artifact**) is **superseded, not patched** — it survives only inside
> `field.convergence_to_closed_form()` as proof that the roughness was the *solver*, not the physics.

---

## Why this chapter exists

The v1.13 site grew tissue-level form **roughly**: a coarse Jacobi relaxation on a 32-point grid, a
1-D axis collapse taken on faith, an `int(L//width)` floor for counting territories, and two inline
magic numbers (`dwell(K=0.6, brake=0.5)`) that never appeared in any parameter database. That is
*precision theatre* — it produces a number, but the number carries a discretization error and rests
on un-stated constants.

The cell level does not have this problem. There, **one** signal `s(x)` is projected two ways and
both projections are exact arithmetic on the sequence. The fix for the tissue level is therefore not
to *tune* the Jacobi solver — it is to **find the same dual structure and make it exact**.

It exists. The morphogen field obeys a *linear* screened-Poisson equation, so for the separable
geometry (a full source face with zero-flux side walls) the field is **exactly one-dimensional** and
has a **closed form**:

```
c(x) = cosh((L − x)/λ) / cosh(L/λ),     λ = √(Dτ)
```

From this single field the two channels fall out in closed form:

```
LEVEL = mean(c) = (λ/L)·tanh(L/λ)                  →  SIZE   (cell-level γ, lifted)
SHAPE = robust_z(c),  boundaries  x_k = L − λ·acosh(θ_k·cosh(L/λ))   →  FORM   (cell-level A4, lifted)
```

No grid. No magic numbers. The territory boundaries reproduce their threshold `c(x_k)=θ` to ten
decimal places; the LEVEL integral matches a 2-million-point quadrature to `<1e-9`. **That is what
"정밀" (precision) means, and it is now real at the tissue scale.**

---

## The dualization, side by side

| | LEVEL (γ-mirror) | SHAPE (A4-mirror) |
|---|---|---|
| cell level | `γ = mean(s)` over a window | `A4 = robust_z(s) = (s−median)/(1.4826·MAD)` |
| tissue level | `mean(c)` of the morphogen field | `robust_z(c)` — **identical operator**, byte-for-byte |
| reads | **how much** (size / dosage) | **the pattern** (territory boundaries / form) |
| under "more source" | scales | **invariant** (to ~5e-15) |
| under "more background" | shifts | **invariant** (to ~9e-15) |
| under "change geometry (λ)" | rescalable | **moves** (it is the shape) |

The bottom three rows are the orthogonality proof: SHAPE ignores everything LEVEL responds to, and
moves only when the geometry — the actual form — changes. `LEVEL ⟂ SHAPE`, exactly, with no
"approximately."

---

## What is honestly NOT done (the two [O] obstacles)

Precision is not accuracy. The interpreter computes the size *budget* and the form *partition*
exactly, but it **never compares them to a real organ**, because doing so without measured data would
be back-fitting. Two named obstacles stand between this chapter and an accuracy claim:

1. **SIZE vs real organ mass — `[O]`.** Closing it needs a *measured* per-organ developmental
   growth-rate atlas (staged organ-mass trajectories). The engine deliberately does not read one.
2. **FORM vs real anatomy — `[O]`.** Closing it needs *measured* enhancer–promoter contact
   (Hi-C / Micro-C / capture-C) or a staged tissue-territory boundary map, then a rank test against
   the predicted boundaries with a shuffle control and a pre-registered sign.

Until those datasets are supplied and the pre-registered test is run, the honest grade is `[O]`, and
`completion.complete` is **False**. This is the handover's anti-false-victory rule, enforced in one
place (`grading.py`).

---

## Layout

```
ax-b-tissue-dual-interpreter/
├── param_db.json            constants (D, τ→λ, θ, α) with grade + provenance — the ONLY source of numbers
├── run.py                   top-level runner → writes expected/*.json + RESULT.txt
├── README.md                this file
├── LEDGER.md                per-channel grade ledger (honest [L]/[V]/[F]/[O])
├── tissue/
│   ├── __init__.py          package surface
│   ├── lock.py              LOCK: every constant from param_db.json; lock_manifest() ⇒ magic-numbers = 0
│   ├── field.py             EXACT closed forms (planar cosh + 3-D Yukawa) + Jacobi kept only as witness
│   ├── level.py             LEVEL = mean(c) → SIZE
│   ├── shape.py             SHAPE = robust_z(c) → FORM (same robust_z as cell-level A4)
│   ├── orthogonality.py     two-knob + geometry-panel proof that LEVEL ⟂ SHAPE
│   ├── grading.py           the ONE place precision≠accuracy is enforced; LEDGER + completion_status
│   ├── interpreter.py       interpret_tissue() = LEVEL ⊕ SHAPE ⊕ orthogonality ⊕ grades; reading_hash
│   └── gate.py              fail-closed gate G1..G7;  python3 -m tissue.gate
└── expected/                deterministic outputs (regenerated by run.py)
```

## Reproduce

```bash
cd ax-b-tissue-dual-interpreter
python3 -m tissue.gate     # G1..G7, exit 0 iff all pass
python3 run.py             # prints the dual reading; writes expected/*.json + RESULT.txt
```

Both are deterministic: re-running yields byte-identical serializations (2×SHA-256).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
