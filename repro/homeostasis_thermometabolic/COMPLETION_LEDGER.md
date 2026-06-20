# COMPLETION LEDGER — homeostasis_thermometabolic_vp_site (v0.6.0)

A line per deliverable with its gate status and grade. This ledger is the single place to verify that the
package is complete and honest. Gates re-run from `repro/run_all.py` and `tools/build_docs.py`.

Concept DOI: **[10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)** (CC BY 4.0).

## Gate summary (all green)

| gate | result | evidence |
|---|---|---|
| determinism (2×sha256 identical) | **PASS** | engine sha256 `08f50d6d96370e7ba66d697d104098b7df7ceb65af457203985fa4ae9229dcab` |
| node emergence | **PASS** | 8 measured nodes + 2 diffuse circuits; `_to_measure` empty |
| stress battery (16 targets) | **PASS 16/16** | RT1–RD4 + RH8 + RH9 all PASS; RT5, RH8, RH9 pass AS [O] with obstacle stated |
| offline cross-species re-derivation | **PASS** | `crossspecies_thermo_panel.json` cache (14 species × 8 genes, 107 cells) → bit-identical (drift 0); panel UNCHANGED since v0.3.0 |
| original read γ values byte-identical | **PASS** | RH9 reads CpG O/E from the existing cache; every read γ value and the original 19 cache entries are unchanged |
| research gate `all_green` | **PASS** | `reports/research_complete.json` |
| restoration S3-honesty (fail-closed) | **PASS** | every S3 link [O] cited; declared set present |
| restoration forbidden-claim scan | **PASS** | no dosing/synthesis/efficacy/safety hits |
| restoration falsification register | **PASS** | SP1–SP3 + FRAMEWORK present |
| precision routing determinism (2×sha256) | **PASS** | routing sha256 `21021e79e667721f3f1efece0592e8b618b2641ea3e9693d9cb889a03022010f` |
| precision γ-independence (fail-closed, THE FIREWALL PROOF) | **PASS** | map byte-identical under a perturbed γ atlas; only the carried γ-context column moves |
| precision anatomy-honesty (fail-closed) | **PASS** | every compartment assignment cited; SYSTEMIC nodes not oversold; behind-barrier primaries graded [O] |
| precision forbidden-claim scan (restoration scan + DELIVERY class) | **PASS** | no dose/injection/implant/catheter-as-fact hits |
| precision falsification register | **PASS** | PR1–PR3 + FRAMEWORK present |
| site C1 drift-0 self-verify | **PASS (drift 0)** | site sha256 `3bb5657bb75e5bb312c925434d4cd6382440b0acc2a2933def3cd3fc51ef6f80` |
| llms.txt < 5 KB | **PASS** | 4424 bytes |
| substrate byte-identical | **PASS** | `vp_substrate.py` sha256 prefix `5664800b…` (unmodified) |

## Stress targets (16/16)

| id | target | status | grade |
|---|---|---|---|
| RT1 | setpoint-defend vs track (endo pins, ecto tracks) | PASS | [V] |
| RT2 | thermostat: sub-spinodal step corrected | PASS | [V] mech / [L] ~37 °C |
| RT3 | endothermy cost: rises with defence | PASS | [V] trade-off / [L] ratio / [O] absolute |
| RT4 | continuum vs discrete: discontinuous jump at spinodal | PASS | [V] |
| RT5 | Kleiber 3/4 exponent | PASS (as [O]) | [O] obstacle stated |
| RG1 | brown-fat thermogenesis defends setpoint | PASS | [V] |
| RG3 | fever (regulated shift) vs hyperthermia (lost control) | PASS | [V] |
| RH1 | torpor SWITCH: hysteresis loop width 1.30 | PASS | [V] |
| RH2 | torpor is a regulated low attractor | PASS | [V] |
| RH4 | bear vs human: present-but-silenced switch | PASS | [V] reads / [O] gating |
| RH6 | interbout arousal as a slow FHN oscillator | PASS | [V] mech / [L] period |
| RH8 | torpor panel: 0/8 genes' promoter γ separates hibernators across 14 species; group gaps ARE GC gaps (cross-gene r=0.9957) | PASS | [V] reads + GC-confound / [O] no-marker conclusion |
| RH9 | methylation substrate: 0/8 genes' CpG O/E separates hibernators; CpG O/E is a distinct read from γ (cross-cell r=0.5601) and far less GC-loaded (0.4927 vs 0.9955) — a second static layer is blind to hibernation | PASS | [V] reads + γ/CpG-O/E dissociation / [O] no-marker + dynamic-regulation external |
| RE1 | glucose homeostat returns to setpoint | PASS | [V] mech / [L] ~5 mM |
| RE2 | lipostat opposes chronic over/underfeeding | PASS | [V] |
| RD4 | hibernation bridge (torpor vs insulin resistance) | PASS | [V] framing / [O] biology |

## Required deliverables (from the session brief)

| # | requirement | status | where |
|---|---|---|---|
| 1 | endotherm vs ectotherm + mechanism difference (Q1 gene criterion / Q2 how-much / Q3 range), NO evolution | **DONE** | `endotherm_ectotherm.py`; §1–§6, §11 |
| 2 | related diseases + 개선책 grounded in #1, applying the analgesic three-lever tech | **DONE** | `setpoint_failure.py`, `restoration_levers.py`; §15–§S3, §P |
| 3 | DNA emergence is default — inherit + actively apply | **DONE** | PDK4 promoted to measured; cross-species panel; §2, §11 |
| 4 | research the diseases owned by this package (T2D/obesity/MetS — hibernation bridge) | **DONE** | §16–§19 |
| 5 | apply VP-SPEC v1.8 — SPLIT into multiple HTML pages | **DONE** | 1 hub + 32 chapter pages under `docs/thermometabolic/` |
| 6 | inherit what's needed, update files, return ONE zip | **DONE** | single bundle (C0) |

## v0.5.0 increment (the regulatory-layer object, HANDOVER #3)

| item | status | grade | where |
|---|---|---|---|
| RH9 / NULL-4: methylation-substrate (CpG O/E) panel does not mark hibernation | **DONE** | [V] reads + dissociation / [O] conclusion | `null_cpg_oe_does_not_track_hibernation()`; §11.2 |
| CpG O/E is a distinct read from γ (cross-cell r=0.5601) and GC-normalized (r(CpG O/E,GC)=0.4927 vs γ 0.9955) | **DONE** | [V] parameter-free | engine + §11.2 |
| dynamic torpor methylation/expression state named as the honest external next step | **DONE** | [O] external (cited, not derived) | `CITED_DYNAMIC_REGULATION`; §11.2 firewall |
| panel + all original read γ values byte-identical (RH9 computed from existing cache) | **DONE** | — | no panel mutation; offline drift 0 |

## v0.6.0 increment (the precision-routing layer, HANDOVER #3 — the analgesic local-anaesthesia mirror)

| item | status | grade | where |
|---|---|---|---|
| compartment routing map: each restoration target placed on a CITED anatomical compartment map | **DONE** | [F] cited anatomy | `precision_routing.py`; §RM |
| parameter-free tier rule: PRECISION (1 comp) / REGIONAL (2–3) / SYSTEMIC (≥4 or distributed node) — split 2/5/2 | **DONE** | [F] structural | `_tier`/`_breadth`; §R, §RM |
| three named routes (BAT-targeted precision · central appetite-axis [O] BBB · hepatic glucose-disposal distributed) | **DONE** | [F] routing / [O] deliverability | `NAMED_ROUTES`; §RM |
| routability [F] kept distinct from deliverability [O] (BBB, small BAT depot, no-single-locus) — no obstacle dropped | **DONE** | [F]/[O] separated | `anatomy_honesty_gate()`; §R, IRREPRODUCIBILITY_LEDGER |
| γ-independence PROVEN: map byte-identical under a perturbed γ atlas; only carried γ-context moves | **DONE** | [V] firewall proof | `gamma_independence_gate()`; §R vp-card |
| engine UNCHANGED (surfaced like the three-lever module, not in `circulate()`); 16/16 + research gate untouched | **DONE** | — | engine sha256 `08f50d6d…` byte-identical; panel + γ values unchanged |

## Pages (1 hub + 32 chapters)

Foundational: how-to-read-this-map, endotherm-vs-ectotherm, the-gene-criterion,
null-ucp1-gamma-does-not-separate, the-thermostat, energetic-cost-of-endothermy, continuum-or-switch,
kleiber-allometry. Thermogenesis/fever: brown-fat-thermogenesis, fever-vs-hyperthermia. Torpor:
torpor-switch, torpor-is-regulated, bear-vs-human, null-no-promoter-marks-hibernation,
null-methylation-substrate-does-not-mark-hibernation, arousal-rhythm.
Energy: glucose-homeostat, lipostat.
Disease: disease-as-setpoint-failure, type-2-diabetes, obesity, metabolic-syndrome, hibernation-bridge.
Restoration: restoration-the-three-lever-method, restoration-lever-1-restore-loop-gain,
restoration-lever-2-reduce-pathological-drive, restoration-lever-3-remove-sensitising-program,
restoration-prioritisation, precision-routing-regional-vs-systemic, precision-routing-compartment-map.
Honesty: grading-and-honesty, falsification.

## Open items (graded [O], obstacle stated — see IRREPRODUCIBILITY_LEDGER.md)

Absolute BMR, the Kleiber exponent, the absolute torpor metabolic-rate drop, the silenced-switch gating
circuitry (now tested at TWO static sequence layers: RH8 shows no promoter γ marks hibernation and RH9
shows the GC-normalized methylation-substrate architecture does not either — but the regulatory gating
that does is DYNAMIC and cited, not derived, and species are not phylogenetically independent draws), the
DYNAMIC torpor methylation/expression contrast itself (RH9's named [O] external step; the offline invariant
precludes ingesting processed in-vivo data in-package), the universal ADRB3-absence claim, absolute disease
incidence, the PDK4 co-upregulation biology, and all restoration clinical magnitudes. The v0.6.0
precision-routing layer adds named DELIVERABILITY obstacles, all [O]: central (MC4R/hypothalamus) access
across the blood-brain barrier, BAT-depot access (small and variable in adult humans), and the no-single-locus
problem for the distributed SYSTEMIC nodes (INSR's ubiquitous receptor, TNF's body-wide program) — routability
(cited anatomy, [F]) is known but reachability is not asserted. Each is open by construction (the substrate
carries structure, not Layer-2 magnitude) and is named, never hidden.
