# LEDGER — tissue-level dual interpreter

Per-channel honest grading. Generated from `tissue/grading.py` (the single
source of truth); do not edit by hand — re-run `run.py` / regenerate.

Grades: **[L]** measured-grounded · **[V]** verified exact (precision) · 
**[F]** model/fiat (modelling choice) · **[O]** open obstacle (accuracy untested).

| # | channel | grade | basis |
|---|---|---|---|
| 1 | intrinsic length lambda = sqrt(D*tau) | **[L]** | composed of two MEASURED morphogen constants (D, tau; Kicheva 2007), read from the locked DB; no fit |
| 2 | LEVEL projection = mean(c) = (lambda/L)*tanh(L/lambda) | **[V]** | exact closed-form integral of the screened-Poisson field; deterministic, bit-for-bit |
| 3 | SHAPE projection = robust_z(c); territory boundaries x_k = L - lambda*acosh(theta_k*cosh(L/lambda)) | **[V]** | exact closed-form threshold crossings; SAME robust_z operator as the cell-level A4; deterministic |
| 4 | orthogonality LEVEL ⟂ SHAPE | **[V]** | SHAPE invariant under source-scale and background-offset to machine epsilon (analytic) + non-redundant on a geometry panel (numeric) |
| 5 | territory partition theta | **[F]** | positional-information threshold; modelling choice; interpreter required theta-robust over [0.3, 0.7] |
| 6 | developmental supply exponent alpha (extent ~ devtime^alpha) | **[F]** | single UNIVERSAL rule applied identically to all; never per-organ |
| 7 | SIZE magnitude vs real organ mass | **[O]** | ACCURACY untested. Needs a MEASURED per-organ developmental growth-rate atlas; the engine does NOT compare (would be back-fit) |
| 8 | FORM (territory partition) vs real anatomy | **[O]** | ACCURACY untested. Needs MEASURED enhancer-promoter contact (Hi-C/Micro-C/capture-C) or a tissue-territory boundary map |

## Locked constants (zero inline magic numbers)

`lock_manifest()` reports **inline_magic_numbers = 0**. 
Every number used by the interpreter is one of:

| constant | value | grade | provenance |
|---|---|---|---|
| `diffusion_D_um2_per_s` | 1.0 | [L] | Typical morphogen effective diffusion ~0.1-10 um^2/s (e.g. Bicoid, FGF, Nodal): Kicheva et al. 2007 (Science); Yu et al. 2009. Central value; target-independent. |
| `morphogen_decay_min` | 60.0 | [L] | Morphogen clearance timescale ~tens of minutes-hours: Kicheva et al. 2007. Generic central value. |
| `territory_theta` | 0.5 | [F] | Activation threshold (fraction of steady state) at which a regulator is counted ON. Modelling choice; engine is required to be theta-robust over [0.3,0.7] (asserted in gate). |
| `growth_alpha` | 1.0 | [F] | Dosage(size supply) ~ (developmental time available)^alpha, single UNIVERSAL exponent applied to ALL organs identically (not per-organ). alpha=1 is the documented modelling choice; not tuned to any mass. |

Derived: **λ = √(Dτ) = 60.0000 µm** (the intrinsic morphogen length).

## Gate (fail-closed)

| check | meaning | result |
|---|---|---|
| `G1_exactness` | closed-form LEVEL integral & every boundary crossing exact to <1e-9 | **PASS** |
| `G2_supersession_of_coarse_jacobi` | old N=32 Jacobi error shrinks toward exact λ; transverse var ~0 (field is exactly 1-D) | **PASS** |
| `G3_orthogonality_level_perp_shape` | SHAPE invariant under source-scale & background-offset to machine ε; geometry moves SHAPE | **PASS** |
| `G4_no_inline_magic_numbers` | lock manifest: 0 magic numbers; every constant has provenance | **PASS** |
| `G5_non_fit_invariant` | reading identical with/without a decoy validation target present | **PASS** |
| `G6_determinism_2x_sha256` | two serializations hash identically | **PASS** |
| `G7_honest_grades_no_false_victory` | only sanctioned grades; accuracy channels [O] with named obstacle; completion False | **PASS** |
| **overall** | | **PASS (7/7)  sha=fa024befe8a8669e** |

## Completion — honestly False

`completion.complete = False`. two channels precision-exact but accuracy-untested [O]; named obstacles below. Precision (정밀) is earned; accuracy (정확) is not yet claimed.

Open channels (accuracy NOT claimed):

- **[O] SIZE magnitude vs real organ mass** — obstacle: per-organ developmental growth-rate atlas (e.g. staged organ-mass trajectories)
- **[O] FORM (territory partition) vs real anatomy** — obstacle: measured chromatin contact (Hi-C/Micro-C/capture-C) or staged tissue-territory boundary map

What would close it: supply the named measured datasets, run the rank test vs barrier/contact with a shuffle control, pre-register the sign; then and only then mark 정확.

Reference dual reading hash (L=360 µm): `439121ca97202cdc`

---

*precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
