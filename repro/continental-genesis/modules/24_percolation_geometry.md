# Module 24 — The percolation ceiling is connectivity-dependent: resolving the CG-39 either/or

**Screen:** `repro/percolation_connectivity_screen.py` (screen 22) → gate `49a92b6c3db69f8b83ea46fc67298e7283f7b049d4345fea6d121d5ba9a59f98` (PASS).
**Method:** pure geometric percolation thresholds (stdlib union-find, SEED=19); **no fitted parameter**; present-tense. falsification = discovery.

## The question this closes
v1.6 (module 23 / screen 21) left the residual as an either/or: does the stirred fraction (~0.34–0.38) **close to 0.41** with untested physics (sphere geometry, internal heating), **or** is the planar percolation ceiling 0.407 the real bound with observed 0.41 sitting on it? A full spherical **convection** solver is out of scope in this session, so the **geometry** candidate is tested where it is actually *decidable*: a percolation threshold depends on the network's **coordination number z**, and changing the surface geometry (square grid → triangulated sphere → hexagonal tiling) changes z. So the sharp, answerable form of "does geometry matter" is: **is the ceiling f\* universal, or is it the value for z = 4?**

## The result (verified, not recalled)

Continent ceiling f\* = 1 − p_c (the fraction where the **ocean** network stops spanning) vs coordination z, by one union-find:

| coordination z | geometry it represents | ceiling f\* |
|---|---|---|
| z = 4 | square grid (the simulation's ocean connectivity) | **~0.41** |
| z = 6 | triangular / a geodesic-sphere tiling | **~0.50** |
| z = 8 | square + diagonals (dense connectivity) | **~0.61** |

f\* **rises strongly with connectivity** (higher z → the ocean spans more easily → it tolerates *more* continent before disconnecting). The observed continental fraction ~0.41 matches **only the z = 4 case**.

## Honest reading (falsification = discovery)
**The percolation ceiling is NOT a geometry-universal constant.** It is the z-dependent threshold, ranging ~0.41 (z=4) → ~0.61 (z=8) over reasonable connectivities. Three consequences, stated plainly:

1. **0.41 is the z = 4 value** — the 4-connected ocean the simulation grid uses (`scipy.label` default = 4-neighbour). The earlier statement "observed 0.41 sits **on** the percolation ceiling" holds **only for 4-connectivity**.

2. **Reaching exactly 0.41 is therefore NOT a missing-convection-physics gap.** Sphere geometry or internal heating would not "close" 0.34→0.41 — the 0.41 target is itself the z=4 threshold. The stirred-box undershoot (0.34–0.38; screens 20–21) sits *below* the z=4 ceiling because vigorous stirring + a finite box hold it there; it is not evidence of a missing mechanism that lifts the ceiling.

3. **The match to observation becomes a falsifiable empirical claim:** the effective coordination of the real subductable-ocean network is ≈ 4. This is **not obviously right** — a naive plate-adjacency graph (each major plate borders ~5–6 others) is z ≈ 5–6 and would predict f\* ≈ 0.45–0.50, *not* 0.41. Whether the right model is a continuum/grid ocean (z ≈ 4) or a plate-adjacency network (z ≈ 5–6) is **open**, and it decides the predicted value. This is exactly the falsifiable prediction the ledger flagged earlier ("the real plate-network connectivity giving f\*≈observed"), now made quantitative.

## What this does to the grade
- The area fraction **is a percolation bound** — confirmed and now characterised across geometries (the mechanism is robust). **[L]**.
- The **specific value 0.41** is **connectivity-contingent**, requiring z ≈ 4. This **downgrades** the certainty of the value relative to the v1.5 "attractor at 0.41" framing — the honest direction. **[O]** for the value, pending the real-network connectivity.

This is a deliberate downgrade: a machine test of geometry-robustness showed the value is less forced than v1.5 implied. The mechanism survives; the number is contingent.

## Remaining untested levers (named, not faked)
Two candidates from v1.6 remain untested here and would refine — but **not overturn** — this conclusion:
- **Internal heating** in the Cartesian box (narrower downwellings): a convection-pattern test of whether the *stirred* value approaches the z-appropriate ceiling more closely. It changes the approach, not the ceiling's z-dependence.
- **Full spherical convection** (a closed-surface solver): out of reliable scope in this session; flagged honestly rather than approximated. It would fix the *effective z* of a real convecting spherical ocean — the very quantity this module shows is decisive.

## Ledger impact
- **CG-39↑↑↑** added (mark-never-erase): the ceiling is connectivity-dependent (~0.41 at z=4 → ~0.61 at z=8); 0.41 is the z=4 value; the residual either/or resolves to "the ceiling is the bound, its value is contingent on connectivity"; the observed match is a falsifiable claim that the real ocean network is effectively ~4-connected (naive plate-adjacency z≈5–6 would predict ~0.45–0.50). **Grade [L]** bound / **[O]** value. The area-fraction value certainty is **downgraded** from v1.5 — falsification = discovery.
