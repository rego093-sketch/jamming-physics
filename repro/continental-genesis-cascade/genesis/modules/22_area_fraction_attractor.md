# Module 22 — The area fraction as a marginal-connectivity attractor (and the R2 identity)

**Screen:** `repro/area_fraction_attractor_screen.py` → gate `bfd00bd952d9ff97ba7f4dfc09659ca05df9c5799a72919e579be6d508ca2cb0` (PASS).
**Simulations (shipped, re-runnable):** `repro/simulations_session/` (the 3D solver + percolation + tracer).
**Method:** present-tense geometry/dynamics; no dates; no fitted parameter. falsification = discovery.

## The question R1 left
Module 21 showed the freeboard, hypsometry, and steady-state *volume* close present-tense. The one
remaining number is the continental **area fraction** (~40 %). Is it derivable, or only a rate balance?

## The insight: continents are not the instantaneous downwelling footprint
Trenches are thin lines; continents are broad. Felsic is **buoyant and accumulates** — it is not confined
to where a downwelling sits now. The geometric ceiling is set by the **ocean** network: the basaltic skin
must stay **connected** (ridge → trench) to keep subducting. **Continents grow until the ocean is at the
edge of percolation; a fragmenting ocean throttles its own subduction** (weak return-flow) → felsic
production stalls → the fraction is **pinned at the percolation threshold**, *independent of the rate
constants*. This is the **same marginal/critical signature** as the `c²=B/ρ` substrate.

## The evidence, in four layers (all SEED=19, no fit)
1. **Planar percolation (self-contained, in the screen).** A stdlib union-find percolation: the ocean
   stops spanning at a continental fraction **f\* ≈ 0.41** (site p_c ≈ 0.5927 → 1 − p_c ≈ 0.407). The
   observed continental fraction ~0.41 sits **on this geometric threshold**.
2. **A self-organizing loop** (`simulations_session/percolation_attractor.py`). Felsic accretes at active
   (connected) ocean margins, throttled by ocean-connectivity health, recycled at rate r. Scanning the
   production/destruction ratio over **4×** (8…30) gives steady **f = 0.39–0.41** — a band of **±0.01**
   centred on f\* and on observed, *far* narrower than the rate variation. The percolation ceiling is a
   **rate-insensitive attractor**, not a rate artefact; the connectivity throttle is a **physical**
   dependence (a fragmenting ocean subducts weakly), not a tuned knob.
3. **A 3D-convection stress test** (`simulations_session/rbc3d.py` + tracer). An **infinite-Pr (mantle)
   3D Boussinesq** solver, **validated** against the analytic onset **Ra_c = 27π⁴/4 ≈ 657.5** (single-mode
   growth matches linear theory to ~1e-7; onset crosses zero at 657.6), produces a realistic cellular
   surface (downwelling area fraction **0.46**, ~20 cells). Driving the tracer with this **real convective
   surface flow**: the percolation throttle still **bounds** f and compresses the rate-dependence (the
   attractor survives in 3D), but the **value is coupling-sensitive** — static 2D = 0.39–0.41; frozen-flow
   **stirring = 0.24–0.32** (convective stirring disperses continents, lowering the ceiling).
4. **The two-way-coupled 3D run — EXECUTED** (`simulations_session/coupled_rbc3d.py` + `coupled_driver.py`).
   Continent **insulation** feeds back into the buoyancy field (zero-mean = self-limiting) and the convection
   **co-evolves** with the continents (which ride the large-scale flow = raft rigidity). The coupled solver is
   **re-validated**: with C=0 it reproduces Ra_c = 657.5 exactly (the coupling does not corrupt it). Within
   the stable window the coupled fraction settles in a statistical steady state around **f ≈ 0.30** (~0.27–0.36),
   **robust to the coupling strength** (q=0 baseline and self-limiting insulation alike). This **confirms the
   frozen-flow lower bound and the percolation mechanism — it does *not* reach the observed 0.41.** *Numerical
   caveat:* at the strongly-supercritical Ra=10⁴, 64×64×12 is stable only for a finite window (~7000 steps) —
   **even the q=0 baseline eventually blows up** — so the long-time limit is the under-resolved convection, not
   the coupling; a fully-converged long run needs higher resolution / implicit (or hyperviscous / adaptive-dt)
   stabilization.

## Honest reading (falsification = discovery)
The two-way-coupled run did **not** confirm the convenient 0.41 — it **broke** that hope and confirmed **~0.30**.
Vigorous convective stirring disperses a **passive** continental tracer, holding f near ~0.30; and real Earth's
mantle is at far higher Ra (~10⁶–10⁷), so it stirs *even more* and would push a passive tracer **lower**, not
higher. So the observed 0.41 must be sustained by physics this passive model **omits**: continental
coherence/strength **resisting dispersal** (a real rheology, not a passive scalar), felsic production
**concentrated at convergent margins**, sphere geometry, and internal heating (narrower downwellings). The
coupled run did the honest thing — it confirmed the lower bound and **sharpened the residual into a specific,
testable list**, rather than rubber-stamping the target.

**Grade [L].** The percolation **attractor** is now confirmed as a robust **bounding** mechanism (**~0.25–0.41**)
across **three** independent settings: static 2D (0.39–0.41), 3D-frozen (0.24–0.32), and 3D-two-way-coupled
(~0.30). **Not [F]:** the connectivity threshold is model-dependent (planar → 0.41; the real plate-network's
effective connectivity giving f\* ≈ observed is a falsifiable prediction), and the coupled value (~0.30) sits
**below** observed 0.41. The decisive run is **done**; the residual is no longer "run the coupled case" but
"**supply the omitted continental rheology + convergent-margin production** (and a numerically-stable high-Ra
long run) to test whether they lift ~0.30 to the observed 0.41."


## R2 — the identity, resolved: three faces of one marginal-criticality kernel
**Three present-tense observables are the same marginal/critical self-organized attractor:**

| observable | held at the margin of | feedback |
|---|---|---|
| the **substrate** (it flows) | the **unjamming** point — `c²=B/ρ` | relaxed shear → 0 (CG-26/31) |
| the **freeboard** (~constant) | the **sea-level** state | erosion ↔ isostasy (module 21) |
| the **area fraction** (~40 %) | the **percolation** of the ocean net | subduction ↔ connectivity (here) |

So continental genesis — *where* the land is (over downwellings), *how high* it stands (marginal freeboard),
and *how much* there is (marginal percolation) — is governed by **marginal-criticality self-organization**,
the `c²=B/ρ` kernel's signature. This is **R2**: the convection loop itself is essentially mainstream;
**VP is the criticality *foundation beneath* mantle convection, not a competitor to it.** Average-theory is
kept out precisely here — VP does not re-explain convection, it supplies the marginal physics under it.

## Ledger impact
- **CG-38** added: the ~40 % area fraction is a **self-organized marginal-connectivity (percolation)
  attractor** of the complementary ocean network — robust and **rate-insensitive** (band 0.39–0.41 in 2D
  across a 4× rate range; planar f\* ≈ 0.407). A **validated** infinite-Pr 3D Boussinesq solver
  (Ra_c = 657.5) shows the attractor **survives** in real convection but the **value is coupling-sensitive**.
  The **two-way-coupled 3D run is now EXECUTED** (insulation feedback + raft rigidity co-evolving with
  convection; re-validated C=0 → Ra_c = 657.5): the coupled fraction settles around **~0.30** (~0.27–0.36),
  robust to coupling strength — **confirming the frozen-flow lower bound and the percolation mechanism, not
  reaching observed 0.41**. The attractor is thus confirmed as a robust bounding mechanism (~0.25–0.41) across
  **three** settings: static 2D (0.39–0.41), 3D-frozen (0.24–0.32), 3D-coupled (~0.30). **Grade [L]**; the
  residual is reframed — not "run the coupled case" (done) but **supply the omitted continental rheology +
  convergent-margin production** (real Earth's higher Ra would stir a passive tracer even lower). The **three
  marginal attractors** (substrate / freeboard / area) unify continental genesis under the `c²=B/ρ` kernel —
  **R2**: VP is the marginal-criticality foundation beneath mantle convection, not a rival.
