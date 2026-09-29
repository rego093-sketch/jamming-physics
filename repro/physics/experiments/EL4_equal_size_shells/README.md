# EL4 — Stiff zone as equal-size, gapless shells (reduced physics)

This test was pre-registered in `PREREG.json`. To reproduce it, run `python3 el4_run.py`, which writes `RESULT.json`.

## Rules
- **Author's rules:**
  1. Beads at the same distance from the proton have the same size.
  2. The stiff zone has no gaps.
  3. Beads shrink by the same rule, so size is proportional to radius, s ∝ r.
  4. At the outer edge, beads have the normal size D.
- **Corpus rule:** coordination z = 6. Each bead therefore touches 4 neighbours within its shell, 1 inward and 1 outward, so each shell is tiled in a square pattern.

## Result (pure geometry)
**1/α = 4π/ε = √(4π n)**. Here ε is the bead size divided by its radius, and n is the number of beads per shell, which is the same for every shell. The rules reduce the full 3-D problem to this single number.

| Route for n | n | 1/α |
|---|---|---|
| Proton consumption per electron-second, ν_p = 3π⁴ | 292.2 | 60.6 |
| Mass ratio, 6π⁵ | 1836.1 | 151.9 (+10.8 %) |
| Proton structure, 82 + 7 | 89 | 33.4 |
| **Required for 137** | **1494** | 137.04 |

No route hits. Reaching 137 needs about **1.5×10³ beads per shell** (ε = 0.092). That is 5.1 ν_p, or 0.81 of the mass ratio. The zone then has an outer radius of 10.9 D and spans about 126 self-similar shells out from the proton radius. The value of n is the one quantity a reduced radial simulation, or a count from the full simulation, has to supply. It is not fitted here.
