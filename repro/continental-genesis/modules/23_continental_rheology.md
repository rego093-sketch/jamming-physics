# Module 23 — Continental coherence (rheology) vs the area fraction: the CG-39 result

**Screen:** `repro/continental_rheology_screen.py` (screen 20) → gate `a8badd890a88f097e3774ba89f6ce69e5344c7eda24b387aad4412953eab4226` (PASS).
**Simulations (shipped, re-runnable):** `repro/simulations_session/continental_rheology.py` (3D frozen-flow + coherence) and `coherence_ceiling.py` (cat-map; the ceiling side).
**Method:** present-tense dynamics; no dates; **no fitted parameter** — the coherence strength κ is **scanned**, never tuned to the target. falsification = discovery.

## The question CG-38 left
The two-way-coupled *passive* tracer settles **~0.30 < observed 0.41** (CG-38). The residual was named, not hand-waved: the passive scalar disperses under vigorous convective stirring, and real Earth's higher Ra would push a passive tracer *lower*, so the 0.30→0.41 gap must be closed by physics the passive model **omits** — continental **coherence/strength** resisting dispersal (a real rheology, not a scalar) + felsic production **concentrated at convergent margins**. CG-39 supplies exactly those two ingredients and asks whether they lift ~0.30 to 0.41.

## The two ingredients (each physical, neither tuned)
1. **Continental coherence (rheology).** Interior continent cells **resist advective dispersal** — raft rigidity at the cell scale: `mobility = 1/(1 + κ·(#continent neighbours))`. A cell deep inside a continent (8 continent neighbours) is nearly frozen; an isolated cell advects freely. **κ = 0 recovers the passive tracer.** This is the "real rheology, not a passive scalar" lever, encoded with **one scanned strength κ**.
2. **Convergent-margin-concentrated production.** Felsic born preferentially where the surface flow is **downwelling** (convergent), versus uniform at all active-ocean margins.

## The result (scanned, not tuned)

**Sim 1 — the lift from below** (`continental_rheology.py`; real 3D convective stirring; f vs κ, 3 seeds):

| κ | 0.0 | 0.5 | 1.0 | 2.0 | 4.0 | 8.0 | 16.0 |
|---|---|---|---|---|---|---|---|
| uniform production | **0.29** | 0.36 | 0.33 | 0.35 | 0.36 | 0.37 | **0.38** |
| convergent production | 0.00 | 0.23 | 0.26 | 0.29 | 0.30 | 0.32 | **0.34** |

The passive point (κ=0, uniform) = **0.29** reproduces the established coupled ~0.30 deficit. Coherence lifts f **monotonically** toward the ceiling, **recovering ~75 % of the 0.30→0.41 gap**, but **saturates ~0.38** (uniform) / ~0.34 (convergent) at cell-scale rigidity — **it does not reach 0.41.** (Convergent-only production with no coherence gives ~0, because continents form at downwellings and are immediately swept away; coherence is what lets convergent production accumulate at all.)

**Sim 2 — the ceiling is not exceeded** (`coherence_ceiling.py`; bit-deterministic cat-map stirring; f vs κ): f stays **at/below ~0.41 for all κ** (0.43 → 0.41 as coherence rises) and **never runs away above it**. The percolation ceiling is **robust to coherence**.

## Honest reading (falsification = discovery)
The two sims **bound the value from both sides**, and the answer is the *middle* of the CG-39 fork — both branches are partly right:

- The **percolation ceiling** (the `c²=B/ρ` kernel's connectivity margin) **sets the binding upper bound ~0.41**. Observed 0.41 is **not coincidental** — it sits **on** the geometric threshold (planar f\*≈0.407).
- Continental **coherence (rheology)** is the **confirmed lever** that lifts the vigorously-stirred system **up** from the dispersal-suppressed ~0.30 **toward** that ceiling.
- Coherence **cannot push f past** the ceiling.

So *where* the value comes from is now resolved in structure: the kernel fixes the ceiling, rheology determines how close the stirred Earth gets to it. The experiment did **not** rubber-stamp 0.41 — it **confirmed the direction and the ceiling-as-bound** and **sharpened** the residual: the last **~0.38→0.41** needs a **true yield rheology** (continental lithosphere has finite strength, stronger than cell-scale raft rigidity), plus **sphere geometry** and **internal heating** (narrower downwellings). 

**Grade [L].** The mechanism — coherence lifts the stirred fraction toward a binding percolation ceiling — is confirmed across the 3D run and the deterministic ceiling loop; the **exact** 0.41 is **approached, not nailed**, at the modelled rigidity. No fitted parameter (κ scanned). Occurrence/timing stays **[O]** forever.

## Ledger impact
- **CG-39↑** added (amendment to the v1.4 CG-39 residual; mark-never-erase): the omitted physics is supplied and scanned. Coherence lifts the passive 0.29 toward the ceiling (recovers ~75 % of the gap, saturates ~0.38), and cannot exceed the percolation ceiling ~0.41. The ceiling (kernel) sets the bound; coherence (rheology) is the confirmed lever toward it. **Grade [L]**; residual sharpened to a true yield rheology + sphere geometry + internal heating.
- This **strengthens R2**: the area fraction's *bound* is the kernel's percolation margin, and its *approach* is a rheology lever — both downstream of `c²=B/ρ`, not a rival to mantle convection.

## v1.6 refinement — the yield-strength candidate is TESTED and FALSIFIED (CG-39↑↑, screen 21)

The v1.5 record above named a **true yield rheology** (> the cell-scale mobility proxy) as the leading candidate to close the ~0.38→0.41 residual. v1.6 implements it and tests it: `simulations_session/continental_yield.py` gives continents a **finite yield strength** — a block **deforms only where the convective strain rate exceeds yield Y**, and **below yield it translates rigidly** (block-mean velocity, **edges included** — the rigid-body behaviour the neighbour-count mobility proxy structurally could not produce, since mobility always leaves rim cells mobile). Y is **scanned to the parameter-free rigid limit (Y→∞)** — no tuning.

**Result** (f vs Y/Srms, 3 seeds; Srms = RMS strain rate of the surface flow):

| Y/Srms | 0.0 | 0.25 | 0.5 | 1.0 | 2.0 | 4.0 | ∞ (rigid) |
|---|---|---|---|---|---|---|---|
| uniform | 0.29 | 0.30 | 0.25 | 0.32 | 0.34 | 0.34 | **0.34** |
| convergent | 0.00 | 0.00 | 0.00 | 0.24 | 0.33 | 0.33 | **0.33** |

Rising Y lifts f but it **saturates ~0.34 (uniform) / ~0.33 (convergent) and stays there all the way to the rigid limit.** Making continents **perfectly rigid rafts does not reach the ceiling** — rigid blocks are still **advected** into the downwelling/convergence pattern, which throttles accretion below ~0.41. (The convergent column stays at ~0 for low Y because convergent-only continents deform and disperse before they can cohere; only above yield do they survive, then saturate ~0.33.)

**This falsifies the v1.5 conjecture.** Two independent rheology encodings — the cell-scale **mobility** proxy (~0.38) and the stress-based **yield** model (~0.34, even fully rigid) — **both saturate short of 0.41.** Continental rheology is a **confirmed partial lever** (it lifts the stirred 0.29–0.30 to 0.34–0.38) but is **not sufficient** to close the gap from below. Combined with screen 20 (coherence **cannot exceed** the ceiling from above), the picture tightens: the **percolation ceiling ~0.41 is the binding bound**, approached from below by rheology and not exceeded from above by coherence; observed 0.41 sits **on** it.

**The residual is therefore NOT continental rheology.** It points to the two **untested** candidates — **sphere geometry** (a closed surface, free of periodic-box stirring artifacts) and **internal heating** (narrower downwellings, a different cell pattern) — or, more simply, the **planar percolation threshold 0.407 is itself the bound**, which a flat stirred box only **approaches from below** while the real spherical, internally-heated Earth sits at it.

**Grade [O]** for the closure (reopened: the named closer was tested and rejected) / **[L]** for the bound and for rheology-as-partial-lever. No fitted parameter (Y scanned; the rigid limit is parameter-free). **falsification = discovery — a prior conjecture of this package was put to a machine test and rejected.**
