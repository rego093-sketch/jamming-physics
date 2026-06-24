# Session simulations — R1/R2 (the v1.3 build)

Runnable code behind modules 21–22 and screens 17–18. All use **SEED=19** and **no fitted parameter**.
The deterministic, load-bearing claims are sealed in the two gated screens
(`repro/r1_budget_screen.py`, `repro/area_fraction_attractor_screen.py`); these scripts are the heavier
numpy/scipy simulations that those screens summarise, shipped so the findings are independently
re-runnable. Recorded outputs are stored next to each script (`*.out.txt`, `*_record.txt`).

Requires `numpy` and `scipy`.

## Files

- **`rbc3d.py`** — an infinite-Prandtl (mantle) 3D Boussinesq Rayleigh–Bénard convection solver,
  pseudo-spectral (Fourier in x,y; sine/cosine modal basis in z; free-slip, fixed-T walls). Velocity is
  slaved to temperature (Stokes, infinite Pr). Extends the inherited `ns3d` spectral approach with
  buoyancy. Includes 2/3 dealiasing.

- **`validate_solver.py`** → `validate_solver.out.txt`. Validates the solver against the **analytic
  free-free onset** `Ra_c = 27π⁴/4 ≈ 657.5`. Single-eigenmode growth matches linear theory to ~1e-7;
  onset crosses zero at Ra = 657.6. (The convection analogue of `ns3d`'s inviscid energy-conservation
  self-check.)

- **`percolation_attractor.py`** → `percolation_attractor.out.txt`. (1) Static percolation: the ocean
  network stops spanning at continent fraction **f\* ≈ 0.407** (planar site p_c ≈ 0.5927). (2) A
  self-organizing loop with a physical connectivity throttle (a fragmenting ocean subducts weakly) pins
  the steady fraction at **f = 0.39–0.41** across a 4× production/destruction range — a rate-insensitive
  attractor. (Stochastic; endpoints vary at the ±0.005 level.)

- **`convection_and_tracer.py`** → `convection_and_tracer.out.txt`. Runs the validated 3D convection to a
  steady state (cellular surface: downwelling area fraction **0.46**, ~20 cells), then drives a
  continental tracer with the **real convective surface flow** (frozen-flow). The percolation throttle still
  bounds f, but the **value is coupling-sensitive**: frozen-flow stirring gives **f = 0.24–0.32** (vs
  static 2D 0.39–0.41). The convection step takes ~2 min.

- **`coupled_rbc3d.py`** — the **two-way-coupled** solver: extends `rbc3d.py` with a continent **insulation**
  heat source (zero-mean = self-limiting). Run directly (`python3 coupled_rbc3d.py`) for the **re-validation**:
  with C=0 it reproduces Ra_c = 657.5 exactly — the proof the coupling does not corrupt the solver.

- **`coupled_driver.py`** → `coupled_run_record.txt`. The **checkpointed** two-way-coupled run: convection
  co-evolves with the continental tracer (continents ride the large-scale flow = raft rigidity; same accretion
  rule as the frozen-flow test). Usage: `python3 coupled_driver.py <ckpt.npz> <budget_steps> <q_insul>` —
  rerun to continue from the checkpoint. **Result:** within the stable window the coupled fraction settles
  **~0.30** (~0.27–0.36), robust to coupling strength — confirming the frozen-flow lower bound, **not**
  reaching 0.41. (Numerical note: at Ra=10⁴, 64×64×12 is stable only for a finite window — even the q=0
  baseline eventually blows up — so a fully-converged long run needs higher resolution / implicit stabilization.)

## Honest status (carried identically in the modules, ledger, and master seed)

- Freeboard, bimodal hypsometry, near-marginal emergence: **[F]/[V]** (module 21 / screen 17 / CG-37).
- Volume steady state (present-tense flux ratio): **[L]**.
- Area fraction = marginal-connectivity (percolation) attractor: **[L]** (module 22 / screen 18 / CG-38).
  Confirmed as a robust **bounding mechanism** (~0.25–0.41) across **three** settings: static 2D (0.39–0.41),
  3D-frozen (0.24–0.32), and **3D-two-way-coupled (~0.30)**.
- **The decisive two-way-coupled run is DONE** (falsification = discovery): it confirmed **~0.30**, not the observed 0.41.
  The 0.30→0.41 gap is the sharpened residual — omitted continental rheology (coherence resisting dispersal)
  + convergent-margin-concentrated production (real Earth's higher Ra would stir a passive tracer even lower),
  plus a numerically-stable high-Ra long run.
- Occurrence/timing stays **[O]** forever (firewall). No deep-time growth curve is used anywhere.
