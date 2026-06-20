# MASTER MANUAL — homeostasis_thermometabolic_vp_site (v0.6.0)

Concept DOI: [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934) (CC BY 4.0) · method DOI (borrowed three-lever technology): 10.5281/zenodo.20733420.

Self-contained operating manual for the package. Read order for a fresh session: `START_HERE.md` →
`CHARTER.md` → this file → `repro/run_all.py` output → `docs/thermometabolic/`.

## 1. What this package is

A physics-derived study of one question — **does an organism DEFEND an internal setpoint or TRACK its
environment?** — that unifies thermoregulation, brown-fat thermogenesis, the torpor/hibernation switch,
whole-body energy homeostasis, and metabolic disease as ONE coupled setpoint-dynamics problem on the
shared R19 bistable switch. Disease is a subset, not the start. Observation only — **no evolutionary
language** anywhere.

## 2. The one substrate (vendored, never modified)

`inherited/vp_substrate.py` provides the R19 jamming-lattice switch `ds/dt = γs − s³ + h` with
`spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`, `settle(g,h,s0)`, plus the FitzHugh-Nagumo `Neuron` and the
`Organ` emergence helper. Two readings carry the whole package:
- a **defended setpoint** = a deep R19 basin whose well resists an ambient drive (endothermy / euglycemia /
  the lipostat);
- a **switch between two regulated attractors past the spinodal** = a discrete state flip (the torpor
  transition). The substrate is byte-identical across versions (sha256 prefix `5664800b…`).

## 3. File map

```
START_HERE.md / CHARTER.md            research program (self-contained)
VERSION (0.6.0) / PHASE (writing)
VP_SPEC_v1_8.md                       governing spec (in-package copy)
inherited/
  vp_substrate.py                     VENDORED R19 + FHN (DO NOT modify)
  organ_gamma.json                    measured γ atlas (PDK4 now measured; _to_measure empty)
  organ_identity.md                   node identity (CITED from DNA)
  crossspecies_thermo_panel.json      14-species × 8-gene torpor/BAT panel (107 cells) + seq cache (offline re-derive; UNCHANGED since v0.3.0)
repro/
  _engine/
    endotherm_ectotherm.py            FOUNDATIONAL: Q1/Q2/Q3 + four NULLs incl. panel-level RH8 (γ) and RH9 (CpG O/E) (the heart)
    vp_trm_engine.py                  node emergence + the defended-setpoint dynamics + stress_targets()
  _verify/
    stress_tests.py                   16-target battery (wired to the engine)
    gates.py                          determinism + research/writing PHASE gate
  _pathology/
    setpoint_failure.py               disease = derived loop-gain-drop law (T2D/obesity/MetS/MODY)
    restoration_levers.py             analgesic three-lever tech applied (S1/S2/S3 + gates)
    precision_routing.py              compartment routing map (PRECISION/REGIONAL/SYSTEMIC + γ-independence proof)
  run_all.py                          research entry point
tools/
  build_docs.py                       deterministic VP-SPEC v1.8 site generator (drift-0 self-verify)
docs/
  thermometabolic/{slug}/index.html   1 hub + 32 chapter pages (canonical)
  robots.txt / sitemap.xml / llms.txt access layer (C4)
  thermometabolic/_meta.json          summary card (§9)
reports/                              emergence_results.json, research_complete.json (generated)
manifest/ , IRREPRODUCIBILITY_LEDGER.md
CHANGELOG.md / MASTER_MANUAL.md / COMPLETION_LEDGER.md / HANDOVER.md   four-document SSOT
```

## 4. How to reproduce (offline, deterministic)

```
python3 repro/run_all.py            # rebuilds every number; prints foundational + dynamics + 16/16 + gates
python3 tools/build_docs.py         # regenerates the site with a C1 drift-0 self-verify
```

Determinism: SEED=19, BLAS pinned to 1 thread, round-before-hash, sorted keys. The engine result is
2×sha256 identical (engine sha256 `08f50d6d…`); the site is byte-identical on regeneration (site sha256
`3bb5657b…`); the cross-species reads re-derive offline bit-for-bit from the vendored cache.

## 5. The answers (what the research found)

- **Q1 — gene criterion:** the divide is the PRESENCE of a drivable {UCP1 furnace + ADRB3 command} pair,
  not a γ value [L]. ADRB3 does not resolve to an ortholog in the ectotherms queried [O]. The deeper
  criterion is the DYNAMICS (a defended attractor), since a silenced furnace (pig pseudogene) still
  defends.
- **Q2 — mechanism / magnitude:** one R19 parameter, basin depth. Endotherm setpoint sensitivity 0.054 vs
  ectotherm 1.394 under the same ambient sweep [V].
- **Q3 — range:** γ spans only ~1.22–1.50 and does NOT track the divide (NULL). The range lives in the
  dynamics — a metabolic factor ~5–10× [L] and a discontinuous regime boundary [V].
- **Four pre-registered NULLs** [V]: (1) UCP1 γ does not separate endo/ecto (GC-confounded; pig pseudogene
  in the functional-rodent envelope); (2) PDK4 γ does not mark hibernation (deep-hibernator γ not elevated →
  present-but-silenced switch); (3) **RH8 — the whole 8-gene torpor/BAT panel across 14 species: 0/8 genes'
  promoter γ separates hibernators; every group γ gap IS a GC gap (cross-gene r(Δγ,ΔGC)=0.9957)**; (4) **RH9 —
  the methylation SUBSTRATE (CpG observed/expected, GC-normalized) of the same panel ALSO fails to separate
  hibernators (0/8), and is a DISTINCT read from γ (cross-cell r(γ,CpG O/E)=0.5601; far less GC-loaded,
  r(CpG O/E,GC)=0.4927 vs 0.9955). Two independent static sequence layers are both blind to hibernation →
  the capability is DYNAMIC regulatory gating, [O] external.** Hibernation is regulatory gating of present
  genes, not a static promoter read. [V] reads + dissociation / [O] no-marker conclusion (small n, species not
  phylogenetically independent; dynamic regulation cited, not derived).
- **Torpor (RH1, central):** euthermia↔torpor is a bistable SWITCH — hysteresis loop width 1.30, jumps at
  ±0.6376 [V]; the low torpor state is itself regulated (RH2) [V].
- **Disease (subset):** one derived loop-gain-drop law — T2D crosses to the hyperglycemic basin, obesity
  drifts the adiposity setpoint up, metabolic syndrome crosses as a coupled cluster, MODY enters as an
  imported parameter. Shape [V], anchors [L], absolute incidence [O].
- **Hibernation bridge (RD4):** PDK4 fuel-sparing is reversible in torpor (defended low setpoint) but a
  chronic supra-spinodal misfire in insulin resistance (crossed and stuck). Same machinery, opposite
  regulatory status.
- **Precision routing (Layer R, the analgesic local-anaesthesia mirror):** each restoration target is placed
  on a CITED anatomical compartment map and classed **PRECISION** (1 compartment), **REGIONAL** (2–3), or
  **SYSTEMIC** (≥4, or a distributed immune/stromal node) by a parameter-free rule on the cited compartment
  count. Nodes split **2 PRECISION / 5 REGIONAL / 2 SYSTEMIC**: the clean precision routes are UCP1→brown fat
  and MC4R→hypothalamus; INSR (ubiquitous receptor) and TNF (distributed program) are honestly SYSTEMIC. The
  map keeps routability (which compartment, cited anatomy [F]) distinct from deliverability (whether an
  intervention can REACH it — blood-brain barrier, small BAT depot, no-single-locus; [O]). **γ-independence is
  PROVEN**: `gamma_independence_gate()` recomputes the whole map under a drastically perturbed γ atlas and the
  routing geometry is byte-identical — only the carried γ-context column moves. [F] routing / [O] deliverability.

## 6. The firewall (binding)

γ reads promoter switch-threshold STRUCTURE only. It is **never** a temperature, metabolic rate, glucose
level, HbA1c, dose, in-vivo selectivity, or clinical effect — those are Layer-2 and graded [O]. The
disease and restoration chapters are falsifiable HYPOTHESES grounded in the foundational setpoint
mechanism, not medical advice. No clinical responsibility.

## 7. No-tuning discipline

Every γ is a measured input; spinodal/barrier are the locked R19 forms; the disease forcing/gain
descriptors are declared and cited, never fitted to hit a number. Restoration target weights are declared
editorial choices; the γ-|h_sp| read is carried beside the priority score and never folded into it. The
precision-routing specificity is a parameter-free reciprocal of the cited compartment COUNT; γ is never an
input to the routing, only carried as the promoter switch-threshold context — and this is not asserted but
PROVEN by `gamma_independence_gate()` (the map is byte-identical under a perturbed γ atlas).
