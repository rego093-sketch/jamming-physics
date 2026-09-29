# NC1 — Newtonian-closure gate (G-Newton) on a sheared particle arrangement

**Grade: [V mech]** — these are mechanism checks inside explicit particle models. They do not derive Navier–Stokes for any real fluid, and they say nothing about the VP vacuum beyond what the model contains.
Pre-registration: `PREREG.json` (written before any physics run; its sha256 is stored in `RESULT.json`).
Run: `python3 nc1_run.py` (numpy only, SEED = 19), then `python3 nc1_run.py --posthoc-p4` (the non-gating diagnostic described below).

## What was tested
The docs/fluid-dynamics §6 gate: the balance laws are exact, but is the closure σ = −pI + 2ηD, with η obtained *from the arrangement*, actually earned? Reviewers also noted that §3 and §6 put the Newtonian regime on opposite sides of the isostatic margin. The model uses 2-D bidisperse harmonic disks (N = 512, radius ratio 1.4, isostatic contact number z_iso = 2d = 4) under Lees–Edwards shear.

- **Model A** (athermal, overdamped, Durian mean-field drag). Measures σ_xy(γ̇) at 9 packing fractions φ from 0.70 to 0.86 and 6 shear rates γ̇ from 3e-5 to 1e-2.
- **Model B** (thermal inertial liquid, φ = 0.70, T = 0.01). Measures η two independent ways:
  - (1) SLLOD NEMD stress, a boundary-driven route that uses the virial stress;
  - (2) periodic body force A·cos(ky), which reads η from the steady velocity profile. It uses no Lees–Edwards boundaries and no stress.
- **Model C** (control: athermal inertial, pair damping only).

## Results (the pre-registered verdicts)
| | prediction | result | verdict |
|---|---|---|---|
| P1 | Newtonian below φ_J: flow index \|n−1\| ≤ 0.10 over the 3 lowest rates, η plateau within 20% | n = 1.070 / 0.957 / 0.957 at φ = 0.70 / 0.75 / 0.80; η ratio of the two lowest rates = 0.86 / 1.10 / 1.06 | **PASS** |
| P2 | η grows as φ → φ_J | η = 0.140, 0.317, 0.551, 1.12, 3.04 (φ = 0.70…0.82), strictly increasing, 21.8× overall; fit η ∝ (φ_c − φ)^−β gives φ_c = 0.846, β = 1.77 | **PASS** |
| P3 | yield stress above φ_J | local n = 0.27 (φ = 0.85) and 0.23 (φ = 0.86); Herschel–Bulkley σ_y = 2.6e-4 ± 0.4e-4 and 9.7e-4 ± 0.7e-4 | **PASS** |
| P4 | η_NEMD = η_PP within 20% | route 2 at the registered amplitudes (A = 0.002 / 0.004) was **nonlinear and diverged** | **FAIL** (not evaluable) |
| P5 (control, not gating) | athermal inertial: Bagnold scaling, n ∈ [1.7, 2.3] | n = 2.01 | PASS |

Also measured, near the margin: at φ = 0.83 n = 0.68, at φ = 0.84 n = 0.46. The mean contact number at the lowest rate is z = 2.08 → 3.54 for φ = 0.70 → 0.82, 3.98 at φ = 0.84, and 4.36 at φ = 0.86.
NEMD η in model B is flat across γ̇ = 0.002–0.02: 0.087 ± 0.013, 0.104, 0.098, 0.096. That is a thermal Newtonian liquid.

### Why P4 failed, and the post-hoc check
The body-force amplitude was pre-set assuming η ≈ 1, but the liquid has η ≈ 0.1. The steady profile would therefore need V = ρA/(ηk²) ≈ 0.26–0.5, which is a peak shear rate of 0.06–0.1 and a Reynolds number of roughly 8. V kept growing without settling (0.57 at t ≈ 1800), and the integration then blew up (z → 20).
This is a protocol-design error, not evidence for or against a material η, and the verdict stays FAIL.

A non-gating re-run used amplitudes chosen for the linear regime: A = 2e-4 and 4e-4, giving V = 0.025 and 0.053, with the transient lengthened to 1000 time units. It gives:
- η_PP = 0.102 ± 0.006 and 0.097 ± 0.003, mean 0.0997;
- against η_NEMD = 0.0959, a **ratio of 0.96**.

The registered amplitudes were too large (see above). The routes agree in the linear regime, but this needs a fresh pre-registered run before it can be graded.

## What this does and does not show about Navier–Stokes
**Shows ([V mech]):**
- In a model arrangement with a declared dissipation channel (viscous drag, or thermal agitation with a thermostat), the steady shear stress is linear in the rate. The viscosity is finite and set by the arrangement (η ∝ contact statistics, growing with z).
- The Newtonian closure is *earned* there, with η in model B a single material number (NEMD rate-independent; the post-hoc two-route check agrees).

**Placement of the Newtonian regime (bears on the §3/§6 seam):** Newtonian behaviour lives **strictly on the unjammed, hypostatic side** (φ < φ_J, z < 4):
- As z → 2d, η diverges (φ_c ≈ 0.846) and the response turns critically shear-thinning (n ≈ 0.46 at φ = 0.84).
- Above the margin there is a yield stress.

So the isostatic margin itself is *not* a Newtonian fluid in this model: it is the point where the Newtonian η ends. A §3 reading of "marginal packing = fluid", taken as "Newtonian at z = 2d", is contradicted here. A reading of "fluid on approach from below, with η set by distance to the margin" is supported.

**Newtonian is not generic:**
- The athermal inertial control gives Bagnold σ ∝ γ̇² (n = 2.01).
- The closure therefore depends on the dissipation mechanism as well as the arrangement. Contact geometry alone does not force n = 1.

**Does not show:**
- The full tensor form: only σ_xy was measured, and neither the isotropy of 2ηD nor normal-stress differences.
- Compressible or bulk viscosity.
- 3-D (2-D is the declared reduction).
- Finite-size scaling of φ_J (N = 512 only).
- A proper critical exponent: the β fit uses 5 points far from φ_J and is not the literature β.
- Anything about the VP substrate specifically (the disks are a generic model).

## Deviations
- Wall time was 53 min (73 min user CPU), not the ≤15 min budget. The cores were shared with other jobs; N and strain were not reduced.
- The P4 protocol error and the post-hoc re-run are described above.

All deviations are also listed in `RESULT.json` under `deviations`.
