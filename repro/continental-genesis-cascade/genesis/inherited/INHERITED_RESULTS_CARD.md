# INHERITED RESULTS CARD — self-contained statement of every upstream result this volume uses

**Purpose:** make Continental-Genesis **logically self-contained**. A fresh session that cannot reach
Zenodo still has, here, the actual inherited claims (equations, grades, provenance) that the 16 screens
and 20 modules build on. Where the inherited *source* is physically shipped in this package it is noted;
where it is not (two DOIs I do not carry), the load-bearing result is stated in full so the argument
stands without it.

**Convention of the parent volumes:** `[LOCK]` = locked primitive · `[DERIVE]` = proved/computed to a
stated tolerance · `[GATE]` = falsifiable, conditional. (Continental-Genesis then re-grades how *it* uses
each result on its own [F]/[V]/[L]/[O] scale.)

---

## I1 — The marginal jammed substrate is a fluid: c² = B/ρ  `[LOCK]`
**Statement.** A jammed packing at the isostatic margin (contact number z = 2d) has **zero relaxed shear
reserve** — the relaxed shear modulus vanishes, `G_relaxed ∝ (z − 2d) → 0`, while the **bulk modulus B
stays finite**. It therefore shears freely, resists compression, and carries exactly **one** elastic
(longitudinal sound) speed: **c² = B/ρ**. That single-speed signature *is* the defining acoustic mark of a
fluid. So the medium is **"a fluid by arrangement,"** not by melting.
**Provenance.** VP physics foundation (concept DOI 10.5281/zenodo.17932566) and the Configured Continuum /
fluid-dynamics volume (concept DOI 10.5281/zenodo.17972568, §3). **Shipped here:** `inherited/fluid-dynamics-engine/marginal_fluidity.py` (runs standalone) and the foundational PDF.
**Where Continental-Genesis uses it.** M11/CG-26 (the mantle is a hot jammed solid *near* unjamming that
flows like a heavy fluid on long timescales — the same substrate, bounded by S-waves to be solid not magma)
and M16/CG-31 (a zero-relaxed-shear medium has no restoring force against a transport perturbation →
symmetry-breaking is *permitted*).

## I2 — Rotation is the unjamming switch; the R19 jammed ⇄ unjammed bistable rupture  `[DERIVE]`
**Statement.** A **rigid** rotation extends no bond (it costs a rigid packing nothing — verified to machine
zero), but a **differential** rotation shears the packing; at the margin there is no shear reserve to resist
it, so **rotation drives unjamming**. The unjamming/attractor balance (stiffness vs inflow) has a global
attractor at `x★ = α` with `F′(x★) = −(π/2)⁵`. This is the R19 jammed⇄unjammed bistable switch
(void-suction / unjamming rupture) — the engine shared with the Recent-Sequence Cascade (v28).
**Provenance.** VP physics (DOI 10.5281/zenodo.17932566); Atlantic-opening geodynamics
(DOI 10.5281/zenodo.17978934). **Shipped here:** `inherited/fluid-dynamics-engine/unjam_inflow.py` and
`axioms.py` (both run standalone). The two source *packages* themselves are **not** carried in this bundle
(I do not have them); this card states the load-bearing result, and v28 re-verifies the full engine
(`inherited_engine/validate_all.py` → 39/39 there).
**Where Continental-Genesis uses it.** M01 (engine inheritance) and the whole opening/closing rupture
picture (the basin opens by unjamming; the antipode closes).

## I3 — Rotation forces a three-body (C₃) core  `[DERIVE]`
**Statement.** A co-rotating **pair** cannot self-propel (a No-Go theorem), so the minimal interaction of a
rotating arrangement is the irreducible **three-body triangle U₃**. Equivalently, odd-cycle (C₃)
frustration is forced: a triangular arrangement of rotating cores cannot two-colour, so they **must
co-rotate**. (Energy leaves the conservative core only through rearrangement events, `ε_bind = Θσ ≥ 0`.)
**Provenance.** Configured Continuum / fluid-dynamics (DOI 10.5281/zenodo.17972568, §4). **Shipped here:**
`inherited/fluid-dynamics-engine/axioms.py` (runs standalone).
**Where Continental-Genesis uses it.** M17/CG-33 — the "three co-rotating cells meet" motif is legitimately
inherited (it is the minimal forced unit), not an arbitrary picture.

## I4 — Co-rotation → merger → Ekman through-flow (inflow **and** updraft are one loop)  `[DERIVE]`
**Statement.** (a) Odd-cycle (C₃) frustration **forces co-rotation**; (b) co-rotating vortices **merge**
into one larger coherent rotation (opposite-sign vortices do not); (c) a coherent rotation drives an
**Ekman through-flow**: radial **inflow** transport ∝ √(ν/Ω) at the base, continuing as **axial outflow**
— i.e. *radial inflow → axial outflow*, the "eye updraft." Inflow at the base and uprise/outflow at the
centre are **one mass-conserving circulation**, not rivals.
**Provenance.** Configured Continuum / fluid-dynamics (DOI 10.5281/zenodo.17972568, §11 / App-K).
**Shipped here:** `inherited/fluid-dynamics-engine/corotation.py` (runs standalone; its own output prints
*"radial inflow → axial outflow: rotation forces a through-flow (eye updraft)"*).
**Where Continental-Genesis uses it.** M17/CG-33 (corrected v2): the typhoon-analogue vent is one loop —
rotation organizes the convergent feed and the axial updraft; **buoyancy** (energy from below, M05/M11)
supplies the lift. This inherited line is exactly why the earlier "inflow not ejection" split was retracted.

## I5 — The VP-SPEC constitution (firewall)  `[meta]`
**Statement.** Present-tense observables are load-bearing ([V]/[F]); absolute dates and deep-time sequences
are RECORD, forbidden as load-bearing in **both** directions; occurrence capped at [O]; **no fitted
parameters**; SEED=19 + double-SHA-256 determinism; mark-never-erase corrections; falsification = discovery.
**Provenance.** The shared VP-SPEC. **Shipped here:** stated in full in `GOVERNANCE.md`.
**Where Continental-Genesis uses it.** Everywhere — it is the grading and audit discipline of all 20
modules and the self-audit (M14/AUDIT-1).

---

## What is shipped vs pointed-to (honest inventory)
- **Shipped in this bundle** (`inherited/fluid-dynamics-engine/`): the fluid-dynamics foundational
  whitepaper PDF, and four runnable inherited scripts — `marginal_fluidity.py` (I1), `unjam_inflow.py` +
  `axioms.py` (I2/I3), `corotation.py` (I4). These reproduce the inherited *mechanisms* offline.
- **Pointed-to only** (not in this bundle, but their load-bearing results are stated above in I1–I2):
  the VP physics package (DOI 10.5281/zenodo.17932566) and the Atlantic geodynamics package
  (DOI 10.5281/zenodo.17978934). v28 carries and re-verifies the full engine; this volume inherits the
  result and points to the source. When this volume matures, ship that engine bundle alongside too.

**Bottom line for a fresh session:** with this card + `GOVERNANCE.md` + the shipped fluid-dynamics engine
scripts, every inherited result the argument leans on is either **reproducible here** or **stated in full
here**. The package is logically self-contained; only the two upstream *source packages* (physics,
geodynamics) remain external, and their results are written out above so nothing in the chain is left
dangling on an unreachable DOI.
