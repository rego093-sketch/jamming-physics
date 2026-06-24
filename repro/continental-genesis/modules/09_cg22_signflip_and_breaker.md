# Module 09 — CG-22 sharpening: the buoyancy sign-flip and the breaker

**Screen:** `repro/buoyancy_signflip_screen.py` → gate `a51a6693b515ed48cdee49da8ddcfa1b8640fd1281b4458de79588e800f2ee1e` (PASS).
**Outcome:** the test did its job — it **broke the strong form** of CG-22. The core survives bounded. **falsification = discovery.**

## What was tested
CG-22 (M08): *negative-buoyancy ocean skin sheds compression by subduction and stays smooth; only positive-buoyancy felsic crust crumples.* The promised test: predict where ocean lithosphere flips net-negative, and check whether that boundary **is** the smooth/crumpled map boundary — a present-tense [V] test that could falsify the gate.

## [1] The sign-flip — computed ([F])
Half-space cooling gives the net buoyancy B(age) = (ρ_m−ρ_cr)·h_cr − ρ_m·α·ΔT·2√(κt/π):

| age | B_net (10⁶ kg/m²) | depth | sign |
|---|---|---|---|
| 2 Ma | +1.60 | 2995 m | POS (resists subduction) |
| 5 Ma | +0.91 | 3283 m | POS |
| **11 Ma** | **−0.01** | **3661 m** | **flip** |
| 20 Ma | −0.99 | 4065 m | NEG (subductable) |
| 80 Ma | −4.78 | 5630 m | NEG |
| 150 Ma | −7.58 | 6787 m | NEG |

**Sign-flip t\* ≈ 11 Ma** (sensitivity 7.5–15.4 Ma over reasonable crust/ΔT), depth **~3.7 km** — a *small fraction* of the ~180 Ma seafloor range. So most of the deep Pacific floor is older/deeper than t\* and is **net-negative**, consistent with M08.

## [2] The honest finding — the proposed test MIS-MAPS
The sign-flip is the **young-vs-old ocean** boundary. But crumpling is gated by **felsic LOAD** (ocean vs continent), and **both** young and old ocean lack that load → **neither crumples** into thick relief. So "sign-flip boundary vs smooth/crumpled boundary" compares **different axes**. The smooth/crumpled boundary is the **ocean/continent (load) boundary** (M08), *not* the ocean buoyancy-sign boundary. **Stating this honestly is the result** — the test as proposed cannot confirm the gate, because it targets the wrong boundary.

## [3] The real breaker — central Indian Ocean ([V] counter-case)
A documented present-tense falsifier of CG-22's **absolute** form: in the **central Indian Ocean**, **old (~50–80 Ma, net-negative)** oceanic lithosphere is **folding under intraplate compression *without* subducting** — long-wavelength lithospheric folds (~100–300 km), gravity/geoid undulations, reverse faulting, large intraplate earthquakes. So negative-buoyancy bare skin **can** deform; it does **not always** shed compression by subduction. The strong claim is **falsified**.

## [4] The bounded, surviving claim (the refinement)
- **THICK crumpling (mountain-scale relief) remains gated to felsic-loaded (positive-buoyancy) crust** — this **survives**: there are *no bare-ocean mountain belts*.
- Bare ocean skin under compression **either subducts** (if a zone is available) **or**, where it cannot, folds only into **long-wavelength, low-amplitude undulations** (central Indian Ocean) — never thick relief (it is thin; M04 buckling threshold rises as the plate thins).

**→ CG-22 is DOWNGRADED: [F] law → [L] bounded tendency, with a logged exception.**

## Honest ledger impact
- **CG-22** refined to **[L]** (bounded tendency), not the [F] law M08 first stated — *marked, not erased* (M08's strong wording stands with this refinement appended).
- **CG-23** added: the central Indian Ocean is the standing falsifier that bounds the gate, and a live test target (does the long-λ/low-amplitude limit hold wherever bare skin is compressed without a subduction outlet?).
- The proposed sharpening *strengthened the program's credibility by breaking its own overreach* — the firewall working as intended. The thesis's core (thick relief needs felsic load; the deep floor is bare negative-buoyancy skin) is unscathed.
