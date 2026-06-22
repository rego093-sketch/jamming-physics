# INHERITANCE MANIFEST — vp_wave_computer (self-contained)

This program inherits **only what the wave-substrate computer needs** from two frozen
source whitepapers — not everything in them. This file **captures the inherited
content itself** (values, facts, principles), so a new session needs **only this
archive**: the source whitepapers are **not required**.

Inherited content is **cited as principle/provenance, never used as a fitting
target**. No value here is tuned to. `new_tuned_constants = 0`.

**This program's own provenance (distinct from the inherited sources below).**
Author **Young Jae Lee** (ORCID `0009-0002-7535-8245`), program **jamming-physics.org**,
license **CC BY 4.0**, **concept DOI `10.5281/zenodo.20783570`** (all versions; metadata in
`CITATION.cff`). The two source whitepapers cited below are **upstream inheritance** —
their content is captured here so this archive stands alone; this DOI identifies the
**wave-substrate program itself**, not the upstream sources.

---

## A. From the brain whitepaper — `vp_frontal v2` (Sim 2, CLOSED)

**Source identity (for provenance only; file not needed):**
`mind_vp_site_v1_57_with_frontal/START_HERE_HANDOVER_v2.md`; frozen engine
`vp_mind_engine.py` sha `e61083ae…` (READ-ONLY); M9 anchor
`R = 0.38961455156044245`; firewall `consciousness_claim = 0`,
`hard_problem_open = 1`. Grading scheme `[V]` verified mechanism / `[L]` locked to a
cited input / `[O]` open or honest negative. **Stress Principle:** every hypothesis
is stress-tested to destruction; a collapse is recorded and the line restarts with
the collapse built in.

| # | Inherited principle | Captured facts (the actual inherited content) | Role in this program |
|---|---|---|---|
| **B1** | **Ephaptic near-field coupling** | In tissue every brain rhythm is **sub-wavelength**: frontal gamma 40 Hz → λ ≈ 913 m, hypothalamus 2 Hz → λ ≈ 4082 m, brain ≈ 0.15 m. The emerged frontal population radiates at ~c (front speed/c = 1.015), but inside the brain coupling is therefore **quasi-static near-field**, i.e. **ephaptic** (field/proximity), not radiative. Tissue params: σ = 0.30 S/m, ε_r = 1e5, L_brain = 0.15 m. | The coupling field `J` (symmetric Hebbian) is the in-silico analog of the ephaptic near-field. Coupling is **by field**, not by digital wiring. |
| **B2** | **Phase (Kuramoto) coupling + order parameter R** | The engine is a 12-node phase-coupled ephaptic ring; the M9 anchor is the order parameter `R = 0.38961455156044245`. | Information carrier is **phase θ**, not amplitude. Dynamics are phase-coupling relaxation. |
| **B3** | **Metastable (critical) operating band** | Gap-1 causal window (sign-stable across a 36-cell seed×duration×node sweep): field **OFF** → R = 0.04, PCI = 0 (access floor); field at **measured** coupling → R = 0.39, PCI = 0.118 (metastable, access open); **over-driven** → R = 0.54, PCI = 0.110 (arousal high, access collapses = seizure/vegetative). The access peak sits at ~3× the measured coupling (interior peak + over-drive collapse). | Computation lives **below full coherence**: full sync (R→1) = one global state = zero information; over-drive degrades. Demonstrated qualitatively in L0/D3. The **number** R = 0.39 is **not transferred** (a different order parameter at a different scale); only the **principle**. |
| **B4** | **Attractor pattern-completion (autoassociator)** | Hippocampal/cortical micro-model: a Hopfield-type autoassociator behind one node of the frozen kernel; pattern completion = 1.0; hub topology `N_HUBS = K = 7` carries the long-range edges; hub-cut collapses distant binding (sign-stable, ST-2). | Stored waves (phase patterns) are recovered from corrupted cues by **relaxation** = computation (L0/D2) and the basis of noise clean-up (L0/D4) and resonance match (L1/R2). |
| **B5** | **Theta-gamma multiplexing, capacity ~7** | Emerged working-memory capacity ≈ 7.2 items (engine 6.125; Miller range) from the measured FOXG1 γ = 1.4737 — a slow theta carrier nesting ~7 gamma cycles (cross-frequency coupling). | **Roadmap (L2)**: multiplex several data into the phase-slots of one slow carrier. Cited now; to be built when sequences/WM are added. |

**Firewall inherited verbatim:** this program models **function only** — storage,
computation, communication, and the cognitive layers above. **No consciousness
claim.** `consciousness_claim = 0`, `hard_problem_open = 1`.

---

## B. From the physics whitepaper — `vp_physics v0.11.0` (only what is needed)

**Source identity (for provenance only; file not needed):** author-sealed v0.8,
src_pin `305a5a24…`; topic index `vp/manifest/physics.csv`. The whitepaper is large;
**only three principles are inherited.** Its particle-mass / quantum-mapping /
gravity chapters are **not inherited** (irrelevant to a wave computer).

| # | Inherited principle | Captured facts (the actual inherited content) | Role in this program |
|---|---|---|---|
| **P1** | **Wave-in-medium law `c² = B/ρ`** | "Jamming Spine — from an Independently Measured Lattice Stiffness to the Speed of Light `c² = B/ρ`": a medium's wave speed is set by its **bulk modulus B** and **density ρ**. | Any wave computer's speed/bandwidth is set by the **medium's stiffness/density**. The coupling-field gain `g` plays the role of the "stiffness" B (L0/D3 medium-stiffness axis). |
| **P2** | **Clock-free lattice propagation** | "Implementing the speed of light (**clock-free** c) and lattice propagation": time **emerges from the medium**, not from an external clock. | The substrate has **no global clock**. Time = the medium's own relaxation. No fetch-execute — **computation is the settling physics**. Matches the brain being self-timed by its rhythms (B2). |
| **P3** | **1/r² near-field Green function** | "Force: lattice tension, the `1/r²` Green-function form, and the EM-sector"; Appendix R "deriving the absolute scale of electromagnetic force". | Same mathematical form as the ephaptic near-field (B1). The coupling field's spatial form is the near-field Green function — the **two whitepapers meet in the same near-field physics**. |

*(The jamming↔unjamming transition in "Appendix L: 4-3-1 State Dictionary" pairs
conceptually with the B3 critical band, but is only cited, not built on, in v0.1.)*

---

## C. What is deliberately NOT inherited (scope, stated honestly)

- Physics: particle-mass, quantum-mapping, gravity chapters (13, 15, 18, …) — **not
  inherited**.
- Brain: the 28-module clinical atlas, psychiatric discriminants — **not inherited**.
- **No value from either whitepaper is used as a fitting input.** Citations are
  *direction / principle*, not fitting targets.

---

## D. The one-line synthesis

**The brain (ephaptic near-field · phase coupling · metastability · attractors) and
the physics (medium wave `c² = B/ρ` · clock-free propagation · 1/r² near-field) meet
in one picture: "compute by phase, in a near-field medium, at the metastable edge,
self-timed."** Layer 0 runs that picture and proves it; the blueprint tests whether
it scales to general function.
