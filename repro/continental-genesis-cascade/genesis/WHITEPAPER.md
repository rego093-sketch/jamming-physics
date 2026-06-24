# WHITEPAPER — Continental Genesis: why dry land exists

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · https://jamming-physics.org/
**Foundations inherited:** VP physics **DOI 10.5281/zenodo.17932566** · Atlantic geodynamics **DOI 10.5281/zenodo.17978934**
**This volume — concept DOI 10.5281/zenodo.20827711** (resolves to the latest version on Zenodo).
**Motto:** falsification = discovery.

---

## The question

Mainstream geology explains how the two-tier crust is *recycled*, but not cleanly why it *exists in the first place* — why there is light, emergent **dry land** at all, sitting above heavy ocean floor. This volume asks that origin question under the firewall.

> **Why does dry land exist?** The answer is **composition + buoyancy, not age.** Begin from a water-covered world with only a thin mantle skin and no continents. A rift opens; its centre founders into a deep basin floored by bare mantle skin; the displaced skin is pushed sideways, thickened and folded; the lateral push and burial **heat** the thickened, **water-bearing** pile; the wet pile **partially melts**, distilling a light **felsic** (granitic) fraction that rises, cools, and — being too light to sink back — **accumulates** as buoyant crust. Dry land is that distilled, accumulated felsic; the ocean is the basic mantle skin it stands above. Land need not *rise*; the basin *subsides*, and emergence follows by isostasy.

This reframes "why land" away from the clock and onto the **mechanism that makes light crust**.

## The chain (each step graded honestly)

| # | Step | Mechanism | Grade | Screen |
|---|---|---|---|---|
| 1 | Submarine extension floors a basin | rift → centre subsides; mantle skin spreads in to floor it | **[V]** | seafloor spreading is observed |
| 2 | Ocean floor = mantle's transient skin | basaltic, young, subducted; not a continent-like permanent layer | **[V]** w/ Moho concession | module 03 |
| 3 | Push → thicken / fold the skin | lateral compression (the *opposite ledger* of the opening) buckles/thickens | **[F]** | `buckling_stress_screen.py` |
| 4 | Push + burial → heat | shear heating + thermal blanketing warm the thickened pile | **[F]/[V]** | module 05 |
| 5 | Wet pile → partial melt → granite | water lowers the solidus; felsic fraction distils and rises | **[F]/[L]** | `wet_solidus_thermal_screen.py` |
| 6 | Light felsic floats & accumulates | too light to re-sink → permanent buoyant crust | **[V]** | isostasy |
| 7 | Emergence by basin subsidence | isostasy is relative; deep basin lets land stand proud (no special lift) | **[F]** | `isostasy_emergence_screen.py` |
| — | Pacific 70%, "huge push", which-ocean-first, the first felsic seed | magnitude / rate / order | **[O] both ways** | firewalled |

## What is established, and what is not

**Established (present-tense / forced):**
- The two-tier crust (felsic ~2.8 / basaltic ~2.9 over mantle ~3.3) is what makes dry land + ocean basins **possible at all** — composition, not age. **[V]**
- Emergence needs only buoyancy + relief; **basin subsidence suffices** — no catastrophic lift required. **[F]** (4.45 km freeboard from Airy balance; screen 4).
- The push needed to fold the skin is a **calculable stress bar** (hundreds of MPa at long wavelength) — feasible. **[F]** (screen 1).
- Water makes the heat→granite step work; a **wet** crust melts where a dry one does not. **[F]** with water (screen 2).
- The Moho-depth asymmetry (ocean ~7 km / continent ~35 km) is **consistent** with thin-skin-vs-distilled-accumulation. **[V]** consistency (screen 4).

**Not established (open, both ways):**
- *When* and *how fast* the felsic accumulated — [O], firewalled.
- *Which* basin opened first / the "Pacific" specificity — [O].
- The **first felsic seed** (how the very first light crust nucleated with no pre-existing land to erode) — [O], honestly the deepest gap, open in mainstream too.
- That **pure extension** (no deep water path) distils **continent-scale** felsic — only [L] (Iceland yields minor rhyolite); a subduction-like deep-water path strengthens it.

## On the zircon clock (what this volume does NOT claim)

It does **not** claim the 4 Ga U-Pb ages are fake. The thermal-reset refutation **fails on its own constants** (≈8–11 orders of magnitude; the zircon stays closed) and **violates the firewall** (privileging "young"). This volume holds those ages as **RECORD**, routes *when* to **[O]**, and keeps only the honest, valid **caveat** that an isochron age is **non-unique** (a mixing line is algebraically identical to an isochron) — which *supports* the firewall, and is never load-bearing for recency. (Module 07, `pseudo_isochron_caveat.py`.)

*This is a seed. It establishes a composition-and-buoyancy answer to "why dry land," with a feasible, chronology-free mechanism chain and 23 SEED=19 double-SHA-256 gated screens, honestly graded. As of v1.8 the chain CLOSES logically (the convergence is the forced downwelling limb of mantle convection; modules 19–20) AND the quantitative test R1 is addressed present-tense (modules 21–22): isostasy + the measured water volume reproduces the observed freeboard and bimodal hypsometry (~5 km separation) with no fitted parameter and no deep-time curve — **[F]/[V]**; the ~40% area fraction is a self-organized marginal-connectivity (percolation) attractor whose **value** is a connectivity-dependent percolation threshold — the natural plate network is z≈6 (Euler), implying a ceiling ~0.46–0.50 *above* observed, so the exact 0.41 is within a ~0.30–0.50 model bracket (modules 24–25) — **[L]** sub-majority regime / **[O]** exact value. The **two-way-coupled 3D run is now EXECUTED** (insulation feedback + raft rigidity co-evolving with convection; re-validated C=0 → Ra_c≈657.5): the coupled fraction settles **~0.30**, confirming the frozen-flow lower bound and the percolation mechanism but **not** reaching the observed 0.41 — the attractor is a robust bound (~0.25–0.41) across three settings (2D 0.39–0.41 / 3D-frozen 0.24–0.32 / 3D-coupled ~0.30), and the 0.30→0.41 gap is sharpened into omitted physics (continental rheology resisting dispersal, convergent-margin-concentrated production; real Earth's higher Ra would stir a passive tracer even lower). R2 (identity) is resolved by the three marginal attractors (substrate / freeboard / area): VP is the criticality foundation beneath mantle convection, not a rival. falsification = discovery; occurrence/timing stays [O] forever. Built to grow.*
