# ONS1 — independent ADG re-implementation of the metriplectic vortex gas

**Target:** Pillar IV of the fluid-dynamics volume, which rests on the manuscript
*"Vortex-Merger Thermodynamics in 2D Turbulence: A Metriplectic Scenario for the
Onsager Anomaly"*. The claim tested: event dissipation `eps_bind` and total dissipation
`eps_tot` (units E0/T0) level off at `eps_sat ≈ 0.2`, with a spread of a few percent, as
r_c goes 0.01 → 0.005 → 0.002. The data behind the claim is
`metriplectic-onsager/data/raw/epsilon_events_ensemble.csv`, and the code that
generated it was never shipped.

**Verdict: NOT REPRODUCED.** Grade for the Pillar IV `eps_sat ≈ 0.2` claim: **[O]**.

`PREREG.json` was saved before any code was written. It fixes the model, units,
window, seeds (101–105) and the pass criteria P1–P3. Nothing was tuned toward 0.2.

## What was built (`adg_vortex_gas.py`, numpy + stdlib)

- **Vortices:** N like-signed point vortices with Γ = 1 on a 2π torus.
- **Hamiltonian:** `H_flow = ½ Σ_{i≠j} Γ_iΓ_j G`. G is the zero-mean doubly periodic
  Green's function, computed as a row sum over images (M = 3, error about 1e-7). It was
  checked for symmetry, periodicity and the Laplacian, and its gradient and Hessian were
  checked against finite differences.
- **Mergers:** when two vortices come within r_c, they are replaced by one vortex with
  circulation Γ_i+Γ_j at the circulation-weighted centre, and `H_int += −ΔH_flow`.
- **Units:** E0 = H_flow at switch-on, T0 = L/U0 with U0 = √(2E0)/L. Window [0.2, 1.0] T0.
- **Initial state:** 5 Gaussian clumps (σ = 0.3), then a Hamiltonian pre-run of 0.05 T0.
- **Integrator:** AVF (mean-value discrete-gradient) step, SM Eq. 18–19, with 3-point
  Gauss–Legendre quadrature and a Newton solve. Deviation from PREREG: a pure AVF step is
  ill-posed for tight co-rotating pairs. At ωdt ≫ 1 Newton diverges, and resolving those
  pairs needs about 10⁵ steps per T0. So stiff pairs are integrated by an exact rotation
  inside a Strang split (rotation dt/2 | AVF on the rest dt | rotation dt/2). As a result,
  energy is conserved only up to the splitting error: the net H_flow drift over the window
  is at most 3e-3 E0.
- **Scale reduction (decided from timing only):** N = 64 and N = 32 with 5 seeds × 3 r_c,
  plus merger-free runs at N = 32, 64 and 128 that record first-passage distances. The
  paper used N = 500–2000. Running at that N was out of reach here: the implicit step
  costs O(N²), and the 4 cores were shared with other jobs.

## Results

| N | r_c | eps_bind | eps_tot | mergers per run (N_final) |
|---|---|---|---|---|
| 64 | 0.010 | 0.0000 | 0.0004 | 0.2 (63.8) |
| 64 | 0.005 | 0.0000 | 0.0004 | 0.2 (63.8) |
| 64 | 0.002 | 0.0028 ± 0.0062 | 0.0029 | 0.2 (63.8) |
| 32 | all | 0.0000 | 0.0002 | 0 |

Against the paper's values of about 0.19 / 0.21: **P1 is undefined (0/0), P2 fails and
P3 fails.**

- **Almost no mergers.** Like-signed point vortices co-rotate and hardly ever come within
  an r_c that is much smaller than the spacing between vortices. In the merger-free runs,
  the number of *new* pairs that dropped below d = 0.02 inside the window was 0 in all
  12 runs (N = 32, 64, 128). Pairs dropping below 0.05 and 0.1 were common.
- **The one in-window merger was a numerical artefact.** It happened at N = 64,
  r_c = 0.002, seed 101: a pre-bound pair slowly contracted. When dt is halved the merger
  disappears.
- **Caveat on scale.** An N ≈ 1000 gas is denser, so these runs cannot rule out mergers
  there. But nothing in the model's dynamics suggests an r_c-independent rate.

## Is the plateau there "by construction"? (the reviewer's objection)

**T2 — where the released energy comes from.** Every logged merger released exactly the
pair self-term −Γ_iΓ_j G(r_ij): the ratio is 1.000. For unit vortices this is
(1/2π) ln(1/r_c) + g0, with g0 = 0.0839. That gives 0.817, 0.927 and 1.073 at the three
r_c values. So the release per merger grows like ln(1/r_c); it is not independent of r_c.

**T3 — changing the energy bookkeeping without changing the dynamics:**
- **Gauge shift of G** (the dynamics are identical): every merger's release moves by
  +0.209, which is +25% at r_c = 0.01.
- **SM-literal minimum-image log:** the release becomes 0.73–0.99 per merger.
- **Finite-core accounting** (Rankine cores, a = r_c/2, area conserved): the release is
  0.044 per merger at every r_c. That means about 95% of the SM "binding energy" is
  renormalised self-energy.

Because of these shifts, the absolute eps level is set by bookkeeping convention, so a
value of 0.2 cannot be a result that holds independently of that convention.

**The shipped CSV** (`csv_checks.py` → `csv_checks.json`):
- **C1:** `n_mergers + N_final ≠ N` in **45/45** rows, with an excess of 28–642. Each
  merger removes exactly one vortex, so these two columns should always add up to N.
- **C2:** n_mergers scales **exactly** as 1/r_c: it is 5.0× larger at r_c = 0.002 than at
  0.01. A smaller merger cross-section should not produce more mergers.
- **C3:** Several columns follow exact patterns:
  - Each seed's eps_bind deviation from the mean is identical across r_c (to 1e-16).
  - `eps_tot − eps_bind` is identical across r_c for each seed.
  - The seed std is bitwise equal at all three r_c.
  - `Re_eff·r_c = 10 + log10(1 + (N−500)/1000)` exactly.

  Taken together, this is the signature of a generated table (a base value plus a
  per-seed offset), not the output of simulations.
- **C4:** eps_bind per merger falls to 0.21× between r_c = 0.01 and 0.002. Point-vortex
  binding energy, however, requires it to rise, by about 1.31×.

## Files

- `PREREG.json`: the pre-registration.
- `adg_vortex_gas.py`: the model and main runner.
- `run_diag.py`: the merger-free first-passage runs and the dt-halving check.
- `analyze.py`: builds `RESULT_raw.json`.
- `csv_checks.py`: the CSV checks.
- `runs_*.json`: per-run records, including every merger event.
- `RESULT.json`: the curated result.

To reproduce, run:

```
python3 adg_vortex_gas.py '{"N":[64,32],"out":"runs_main.json"}'
python3 run_diag.py
python3 csv_checks.py
python3 analyze.py
```

Total runtime is about 30 min wall-clock on 4 shared cores.

The `docs/` directory was not edited.
