# VP Continental-Genesis — package README (v1.8)

**Why does dry land exist? A composition-and-buoyancy answer, built on the VP jamming engine.**

A *physically-permitted, occurrence-open* hypothesis for the origin of the two-tier crust:
the ocean is the mantle's thin transient skin; continents are light felsic crust **distilled**
from that skin by a submarine rift's compressional + thermal + (wet) re-melting cascade, made
emergent by basin subsidence. A **sibling** to the Recent-Sequence Cascade (v28), sharing its
engine and firewall, asking the **earlier** question.

- **Author:** Young Jae Lee · **ORCID** 0009-0002-7535-8245 · **License** CC BY 4.0 · https://jamming-physics.org/
- **Inherited:** VP physics **DOI 10.5281/zenodo.17932566** · Atlantic geodynamics **DOI 10.5281/zenodo.17978934** · Configured Continuum (fluid-dynamics) **DOI 10.5281/zenodo.17972568**
- **This volume — concept DOI 10.5281/zenodo.20827711** (resolves to the latest version on Zenodo).
- **Motto:** falsification = discovery.
- **This package:** 25 modules · 23 SEED=19 double-SHA-256 gated screens · ledger CG-1…CG-39 + AUDIT-1.

## VP-SPEC v1.9 canonical (new)
- **`WHITEPAPER.html`** is the **single self-contained canonical** for this volume under **VP-SPEC v1.9**
  (answer-first, honest [F]/[V]/[L]/[O] grade badges, self-contained `vp-card` per locked quantity,
  inherits-strip, JSON-LD, English only). It integrates the **full** prose of all 25 modules and the
  supporting documents — **nothing condensed** — into 30 chapters / 118 numbered sub-chapters (§N.x).
  Open it in any browser (offline-portable). Generated deterministically by `tools/build_canonical_html.py`.
- The v1.9 cards/registries are under `docs/` (`_meta.json`, `_decl.json`, `registry/concepts.json`,
  `registry/modules.json`, `llms.txt`, `assets/css/site.css`). See `VP_SPEC_v1_9_APPLICATION.md` for what
  was applied. **No LOCK constant, screen, or module science changed** — the science is byte-identical.

## Read order (for a fresh session)
0. `WHITEPAPER.html` — **the canonical** (VP-SPEC v1.9): the whole volume, sub-chaptered, retrieval-ready.
1. `00_MASTER_SEED.md` — **start here**: single-file handoff; the whole state, grades, and next task in one read.
2. `WHITEPAPER.md` — thesis + the graded chain.
3. `GOVERNANCE.md` — the constitution (firewall, [F]/[V]/[L]/[O] grading, mark-never-erase, no-tuning).
4. `modules/01..25` — the step-by-step governed record (honest grades; the rejections kept, not erased).
5. `BLUEPRINT_and_GRADED_LEDGER.md` — full ledger (CG-1…CG-39 + AUDIT-1) + leverage-ranked roadmap.
6. `PUZZLE_MAP.md` — evidence discipline (degenerate items kept out of the evidence column).
7. `inherited/INHERITED_RESULTS_CARD.md` + `inherited/fluid-dynamics-engine/` — the inherited engine, **shipped**: every upstream result stated in full, plus four runnable inherited scripts + the foundational PDF (so the package is self-contained without Zenodo).
8. `NO_TUNING_THESIS.md` — the architectural thesis (one inherited kernel, **no fitted parameter**, **no per-stage added mechanism**), parallel to `WHITEPAPER.md`/`GOVERNANCE.md`; its falsifier surface is machine-gated at `repro/no_tuning_falsifier_screen.py` (screen 19).

## What this is / is not
**Is:** a composition+buoyancy account of *why dry land exists*, with a feasible, chronology-free
mechanism chain and 23 SEED=19 double-SHA-256 gated screens, honestly graded. The spine is a
connected [F]/[V] chain (see `00_MASTER_SEED.md` §SPINE); the rest is [L]/[O] by design.
**Is not:** a claim that the sequence occurred; a claim about any absolute age; or an attack on
the U-Pb zircon dates (that route is closed — module 07). Dates/sequences stay RECORD; *when/how-fast*
stays [O], both directions.

## Verify in five minutes (offline, no network)
Every screen is self-contained, deterministic (SEED=19), and prints `REPRO GATE: PASS` on its last line.
```bash
cd repro
python3 buckling_stress_screen.py                     # compression-face stress bar (M04)
python3 wet_solidus_thermal_screen.py                 # heat -> granite, wet solidus (M05)
python3 pseudo_isochron_caveat.py                     # isochron non-uniqueness caveat (M07)
python3 isostasy_emergence_screen.py                  # emergence-by-subsidence + Moho (M06)
python3 buoyancy_gating_screen.py                     # buoyant load gates compression; smooth floor (M08)
python3 buoyancy_signflip_screen.py                   # sign-flip + CG-22 breaker test (M09)
python3 isostatic_compensation_law_screen.py          # compensation law + gravity test (M10)
python3 mantle_jamming_state_screen.py                # mantle = jammed solid near unjamming, not magma (M11)
python3 convective_state_screen.py                    # present-state synthesis + asymmetry edge (M12)
python3 asymmetry_and_divergence_screen.py            # asymmetry degenerate; divergence = origin (M13)
python3 firewall_self_audit_screen.py                 # self-audit: imported-chronology breaches + fixes (M14)
python3 assembly_causal_chain_screen.py               # opening -> one-sided-mass causal chain (M15)
python3 symmetry_breaking_inheritance_screen.py       # inherited symmetry-breaking capacity (M16)
python3 upwelling_cell_hypothesis_screen.py           # typhoon analogue: forced up-and-out vent, corrected v2 (M17)
python3 granite_carbonate_dichotomy_screen.py         # granite/limestone = two faces; resolves CG-12 (M19)
python3 closed_loop_dissolution_screen.py             # the 'convergence-origin' gap dissolves; residual=budget (M20)
python3 r1_budget_screen.py                            # R1 budget: freeboard + hypsometry [F]/[V] + steady volume [L] (M21)
python3 area_fraction_attractor_screen.py             # area fraction = percolation attractor [L]; R2 three margins (M22)
python3 no_tuning_falsifier_screen.py                 # NT-1/NT-2 falsifier surface, machine-checked; F5 -> CG-39 (screen 19)
python3 continental_rheology_screen.py               # CG-39: coherence lifts stirred f toward the ceiling [L] (screen 20)
python3 continental_yield_screen.py                  # CG-39 refinement: yield rheology FALSIFIED as closer; [O]/[L] (screen 21)
python3 percolation_connectivity_screen.py           # CG-39 resolution: ceiling is z-dependent; 0.41 is the z=4 value [L]/[O] (screen 22)
python3 plate_connectivity_screen.py                 # CG-39 closeout: plate network z~6 (Euler) -> ceiling 0.46-0.50; 0.41 not forced [L]/[O] (screen 23)
# each tail -> REPRO GATE: PASS
```
One-liner to verify all 23 at once:
```bash
cd repro && for s in *.py; do python3 "$s" | tail -1; done   # expect 23x REPRO GATE: PASS
```
Integrity of the whole tree (from package root):
```bash
sha256sum -c MANIFEST.sha256   # expect: all OK
```

## Status — all 23 gates PASS (hashes regenerated at v1.8)
| Screen | Gate (2×SHA256) |
|---|---|
| buckling_stress_screen | `811aba1d…20f3` |
| wet_solidus_thermal_screen | `01e659c1…3a64` |
| pseudo_isochron_caveat | `3f835b8c…f610` |
| isostasy_emergence_screen | `f2c426e5…e805` |
| buoyancy_gating_screen | `a87f1a89…51b3` |
| buoyancy_signflip_screen | `a51a6693…ee1e` |
| isostatic_compensation_law_screen | `b309631e…38ed` |
| mantle_jamming_state_screen | `8c732f37…c9c0` |
| convective_state_screen | `f5b55cbd…35bb` |
| asymmetry_and_divergence_screen | `985b4c39…d6b6` |
| firewall_self_audit_screen | `f783764c…61d2` |
| assembly_causal_chain_screen | `6ed0210a…c79a` |
| symmetry_breaking_inheritance_screen | `ca63495c…a551` |
| upwelling_cell_hypothesis_screen | `399566a3…9716` |
| granite_carbonate_dichotomy_screen | `7cbaa628…0efb` |
| closed_loop_dissolution_screen | `779a2269…cb0c` |
| r1_budget_screen | `99972920…b2fa` |
| area_fraction_attractor_screen | `bfd00bd9…2cb0` |
| no_tuning_falsifier_screen | `e50d212e…9fac` |
| continental_rheology_screen | `a8badd89…4226` |
| continental_yield_screen | `a4683e2f…ede9` |
| percolation_connectivity_screen | `49a92b6c…9f98` |
| plate_connectivity_screen | `c34e8ada…025b` |

## R1 and R2 — addressed; the two-way-coupled 3D run is now EXECUTED (v1.3)
R1 was the named decisive test (does the loop distil the **observed** ~40 % felsic / freeboard / Moho?).
It is now **addressed on present-tense grounds**, firewall-clean. The naive form — *rate × time = volume* —
needs a duration ([O]), exactly where mainstream growth curves smuggle deep time in; so R1 is reformulated
as a **present-tense fixed point** (modules 21–22, screens 17–18):
- **Freeboard** (B1): isostasy + the measured water volume reproduces the observed freeboard — textbook
  ρ_c=2800 overshoots to +1915 m, but the **measured** bulk density/thickness hits observed ~+840 m; the
  lever is the distilled-felsic density deficit. **[F]/[V]**.
- **Bimodal hypsometry** (B2): two peaks (+1544 / −3686 m, separation ~5.2 km); continents **near-marginal**
  (emergent by only the top ~30 % of the relief). **[F]/[V]**.
- **Steady-state volume** (A): a present-tense flux **ratio** P/D ~ O(1) (production ~1–3 vs destruction
  ~1.5–3 km³/yr) → sustainable. **[L]**.
- **Area fraction**: a **self-organized marginal-connectivity (percolation) attractor** of the ocean
  network (planar f\*≈0.407; 2D self-organized band 0.39–0.41). A **validated** infinite-Pr 3D Boussinesq
  solver (onset Ra_c = 27π⁴/4 ≈ 657.5, matched to ~1e-7) shows the attractor **survives** in real
  convection. **The two-way-coupled 3D run is now EXECUTED** (v1.3; insulation feedback + raft rigidity
  co-evolving with convection; re-validated C=0 → Ra_c=657.5): the coupled fraction settles **~0.30**
  (~0.27–0.36), robust to coupling strength — **confirming the frozen-flow lower bound and the percolation
  mechanism, but NOT reaching the observed 0.41**. The attractor is thus a robust bound (**~0.25–0.41**)
  across three settings (2D 0.39–0.41 / 3D-frozen 0.24–0.32 / 3D-coupled ~0.30). **[L]**.

**R2 (identity) is resolved by the three marginal attractors** — substrate at the unjamming margin
(`c²=B/ρ`), freeboard at the sea-level margin, area at the percolation margin. VP is the
marginal-criticality **foundation beneath** mantle convection, **not a competitor** to it: the convection
loop is essentially mainstream; VP supplies the criticality physics under it. No fitted parameter, no
deep-time curve enters anywhere.

**The decisive run is done — and it did the honest thing (falsification = discovery).** The two-way-coupled run did **not**
confirm the convenient 0.41; it confirmed **~0.30** and **sharpened** the residual. The gap (0.30 → 0.41)
points to physics the **passive** tracer omits: continental **coherence/strength** resisting dispersal (a real
rheology, not a scalar), felsic production **concentrated at convergent margins**, sphere geometry, internal
heating — and real Earth's far higher Ra (~10⁶–10⁷) would stir a passive tracer **even lower**, so the gap is
genuine. So the open residual is no longer "run the coupled case" but **supply that omitted physics** (plus a
numerically-stable high-Ra long run — at Ra=10⁴, 64×64×12 is stable only for a finite window). The coupled
solver + driver + recorded run are shipped in `repro/simulations_session/`. Occurrence/timing stays **[O]**
forever. falsification = discovery.
