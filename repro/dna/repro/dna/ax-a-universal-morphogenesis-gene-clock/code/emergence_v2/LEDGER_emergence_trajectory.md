# LEDGER — reduced-order reaction-diffusion trajectory layer (Phase 3)

Honest, per-quantity grading under the project's C3 discipline. The trajectory engine
(`emergence_trajectory.py`) turns the **measured morphogen biophysics** in the locked DB into
an absolute **length** scale and a reproducible **spatial partition** of a growing 3-D domain —
exactly as Phase 1 turned the measured protein half-life into an absolute **time** scale. It reads
**only** `param_db.json`; it never reads the validation targets and never reads any real anatomy.

**The legitimacy rule (unchanged):** a parameter is a valid input iff it is (a) a UNIVERSAL law or
(b) an INDEPENDENTLY measured/published value, carried in the DB with provenance. A violation is only
a value WE chose to match a target. The gate's **NON-FIT invariant** asserts the engine never reads a
target, so every DB constant is a locked input `[L]`, not a back-fit. **No shape is fitted to anatomy.**

## The physics, in one line

Linear steady-state screened Poisson `D·∇²c − c/τ + source = 0`; intrinsic length `λ = √(D·τ)`,
set entirely by the two measured constants. A face source gives `c(x) ∝ exp(−x/λ)`; thresholds carve
nested territories at `x_k = λ·ln(1/θ_k)` (Wolpert positional information / French-flag). The domain
**elongates** over developmental time by the same universal supply rule as Phases 1–2.

| quantity | grade | basis |
|---|---|---|
| morphogen diffusion `D` (0.1–10 µm²/s, central 1.0) | **[L]** | Kicheva et al. 2007 (Science); Yu 2009 — measured effective morphogen diffusion, in `param_db.morphogen` |
| morphogen clearance `τ` (≈60 min) | **[L]** | Kicheva et al. 2007 — measured clearance timescale, in `param_db.morphogen` |
| **intrinsic length** `λ = √(D·τ) = 60 µm` | **[L]-grounded** | derived from the two measured constants only; **recovered from the solved 3-D field to <1%** (60.55 µm at N=32) and convergent under grid refinement — a property of the physics, not the mesh. The DB's own D-range maps to λ ∈ [19, 190] µm, bracketing real morphogen gradients (Bicoid/FGF/Nodal/Shh). Not fitted. **(Phase 7 promotes this aside [F] → [L]-grounded: `verify_emergence_morphogen.py` 8/8 PASS confronts the band with six directly-measured gradient lengths; geom-mean factor 1.91 < 3, 5/6 in band, independent set Bicoid/Nodal/Shh 3/3 — see `LEDGER_morphogen_length.md`.)** |
| threshold `θ` (territory cutoff) | **[F]** | `param_db.kinetics.relay_threshold_theta`; a documented modelling choice. Gate asserts θ-robustness over [0.3,0.7]. |
| **positional partition / realized coarse FORM** | **[F]** | ordered nested territories of width `λ·ln(1/θ)`; boundaries land at their physical positions `k·λ·ln(1/θ)` (within ~1%). A reproducible spatial partition **emerges**; it is a mechanism demo, not an anatomy. |
| domain growth (axial extent ~ `devtime^α`, α=1) | **[F]** | `param_db.allometry.growth_supply_exponent_alpha`; the single UNIVERSAL supply rule reused from Phases 1–2, applied identically. Not tuned to any size. |
| **apical negative-allometry** (apical fraction ~ `L^(−0.96)`) | **[F]** | MECHANISM: a fixed physical length λ inside a growing domain forces the leading territory's fraction to fall ∝ 1/L — the **same sign** Phase 2 measured (brain-type negative allometry), recovered here from first principles, with **no fraction fitted**. |
| **exact, validated 3-D anatomy** | **[O]** | needs measured tissue mechanics (stiffness/viscosity time-course), real source geometry, advection/growth coupling, and HPC at cell resolution. Deliberately **not** attempted; comparing this coarse form to a real organ by tuning would be the forbidden back-fit. |

**Gate:** `verify_emergence_trajectory.py` → **7/7 PASS**
(1 DB-sourced · 2 non-fit invariant · 3 determinism 2× sha `b2b34a770f5a` · 4 **grid-robust**: λ_field→√(Dτ),
error 0.98%→0.92%→0.79% decreasing, ordering grid-independent · 5 **θ-robust**: nested ordering invariant,
boundaries == λ·ln(1/θ) · 6 non-blind: planted λ recovered R²=1, shuffle R²→0 · 7 grades declared).

## What this layer adds vs Phases 1–2

Phase 1 gave an absolute **time** scale (onset in hours from measured half-life); Phase 2 gave an
allometric **growth law** (cited exponents predicting fraction-change, graded [O]). Phase 3 gives an
absolute **length** scale and a reproducible **spatial partition** from measured morphogen biophysics,
and — as a bonus — **re-derives the sign of Phase 2's allometry mechanistically** (fixed λ in a growing
domain). The axis stays the same: γ fixes *order/identity* `[V]`; systemic parameters fix the *realized*
when/how-big/where — `[L]` where measured (λ-scale), `[F]` where modelled (partition, growth), `[O]`
where the cell-resolution form is data/compute-blocked.

## Honest residuals (recorded, not hidden)

- The realized form is a **coarse positional partition**, not a curved organ. With a *localized* source
  the 3-D field acquires geometric spreading (Green's function `∝ exp(−r/λ)/r`), so the *intrinsic* λ is
  measured from the clean full-face geometry; a curved 3-D bud is qualitative only. Both remain `[F]`.
- The negative-allometry exponent (−0.96) is the *mechanism* sign and magnitude for a fixed-λ apical
  zone; it is **not** claimed to equal any measured organ's exponent (that comparison stays `[O]`).
- τ is carried as a single central value (≈60 min); widening it to its measured range only rescales λ
  within the cited band and does not change any ordering or grade.
