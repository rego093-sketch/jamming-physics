# Module 25 — CG-39 closeout: the plate network is ~6-connected, so 0.41 is regime-right, not forced

**Screen:** `repro/plate_connectivity_screen.py` (screen 23) → gate `c34e8adab1af568e45b4cbb4dfe763d7abfbdcd2c223a10b26e07ff40399025b` (PASS).
**Method:** exact topology (Euler) + the screen-22 percolation calibration; **no fitted parameter**; present-tense. falsification = discovery.

## The question this closes
Screen 22 (module 24) showed the percolation ceiling is connectivity-dependent — f\* ≈ 0.41 at z = 4, ≈ 0.50 at z = 6 — and left one decidable question: **is the real ocean/plate network z = 4 (→ 0.41) or z ≈ 6 (→ 0.50)?** That single number sets the predicted value. This module answers it not by guessing but by **exact topology**.

## The answer (exact, not estimated)
A sphere tiled into **F** plates whose boundaries meet at **triple junctions** (the generic, mechanically stable case — quadruple junctions are unstable) satisfies Euler's formula V − E + F = 2 together with the triple-junction count 2E = 3V. Eliminating V gives **E = 3F − 6**, hence the mean number of neighbours per plate:

$$ z \;=\; \frac{2E}{F} \;=\; 6 - \frac{12}{F}. $$

This is exact. For realistic plate counts:

| F (plates) | 7 | 12 | 15 | 25 | 52 |
|---|---|---|---|---|---|
| z = 6 − 12/F | 4.29 | 5.00 | 5.20 | 5.52 | 5.77 |

The ~15 commonly-cited plates give **z = 5.2**; even the full 52-plate catalogue gives 5.8. **The natural plate network is ~6-connected, not 4** — closer to a triangular tiling (z = 6, f\* ≈ 0.50) than to the square grid (z = 4, f\* ≈ 0.41) the simulation happened to use.

## Honest reading (falsification = discovery)
A z ≈ 5–6 network sits between the bracketing integer connectivities, so its implied percolation ceiling is **f\* ≈ 0.46–0.50** — which **overshoots** observed 0.41. Three plain consequences:

1. **The answer to "z = 4 or z ≈ 6" is z ≈ 6.** So the clean "0.41 = z = 4 threshold" coincidence (screen 22) is **not** the natural network's prediction. The natural network predicts a *higher* ceiling than observed.

2. **Observed 0.41 sits below the natural-network ceiling.** It lands in the band where the convective stirring holds the fraction *down* (the 0.30–0.38 undershoot, screens 20–21). So 0.41 is best read as **(connectivity ceiling ≈ 0.46–0.50) − (a stirring undershoot)** — an interplay, not a single forced number.

3. **What survives is the claim that was actually load-bearing.** The continental fraction is a **percolation-bounded quantity in the correct regime — a sub-majority ~0.4–0.5**, not ~0.1 or ~0.9. The kernel chain (c²=B/ρ → felsic accumulates and cannot subduct → the ocean skin must stay connected to subduct) **fixes that regime**. It does **not** uniquely pin 0.41; the exact value lies inside a **~0.30–0.50 model bracket** spanned by (connectivity choice) × (stirring vigour).

## Final grade and closeout
- **[L]** — the continental fraction is a percolation-bounded **sub-majority (~0.4–0.5)**, forced by the kernel. This is robust across every test in screens 18–23.
- **[O]** — the **exact value 0.41** is set by the connectivity-ceiling-minus-stirring interplay and sits within model uncertainty; it is **not** uniquely forced by any single clean argument.

**CG-39 is CLOSED.** The residual that began as "lift the coupled 0.30 to 0.41" was chased to its floor across five tests — coherence (recovers ~75 %, saturates 0.38), yield rheology (saturates 0.34 even rigid, *falsified* as the closer), the connectivity-dependence of the ceiling, and finally the exact plate topology. The honest end state is **regime-yes, exact-value-no**: the mechanism is real and predicts the right order; the precise number is contingent. Occurrence/timing stays **[O]** forever.

## Ledger impact
- **CG-39 ✓ (CLOSED)** added (mark-never-erase): plate topology gives z = 6 − 12/F ≈ 5–6, so the natural-network ceiling f\* ≈ 0.46–0.50 overshoots observed 0.41; 0.41 is regime-correct (~0.4–0.5, kernel-fixed, **[L]**) but not uniquely forced (exact value within a ~0.30–0.50 bracket, **[O]**). CG-39 closes — falsification = discovery.
