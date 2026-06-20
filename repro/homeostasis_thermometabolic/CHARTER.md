# CHARTER — Thermometabolic Homeostasis: Endothermy, Thermogenesis, Torpor, and Metabolic Disease as Setpoint Dynamics

**paper_id:** `homeostasis_thermometabolic_vp_site`  ·  **code:** `trm`  ·  **branch:** integrative (thermal + energy setpoint dynamics)  ·  **version:** 0.6.0  ·  **concept DOI:** [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)  ·  **license:** CC BY 4.0

> **v0.6.0 — research signed off, site landed.** Every named master is measured (PDK4 promoted
> TO-MEASURE → γ=1.4112 via the identical DNA pipeline; an 8-gene × 14-species torpor/BAT panel — 107
> cells — is vendored and offline-reproducible, UNCHANGED since v0.3.0). The 16-target stress battery is
> all PASS — reproduced [V], with RT5 (Kleiber), RH8 (the panel-level γ hibernation NULL), and RH9 (the
> methylation-substrate CpG-O/E NULL, the firewalled regulatory-layer object) passing AS [O] with stated
> obstacles per the bar below. Pathology instantiates one derived
> loop-gain-drop law per disease (T2D/obesity/metabolic syndrome/MODY); restoration applies the
> analgesic three-lever technology (S1 restore-gain / S2 reduce-forcing / S3 remove-sensitiser) with
> S3-honesty, forbidden-claim, and falsification gates all green. **v0.6.0 adds Layer R — the
> precision-routing layer** (the analgesic local-anaesthesia mirror): each restoration target is placed on
> a CITED compartment map and classed PRECISION / REGIONAL / SYSTEMIC, with routability ([F]) kept distinct
> from deliverability ([O]) and a PROVEN γ-independence gate (the map is byte-identical under a perturbed γ
> atlas). The engine is unchanged. Canonical multi-page HTML built by `tools/build_docs.py` with a C1
> drift-0 self-verify.

## Scope (one line)
Starts from the endotherm-vs-ectotherm question -- does the organism DEFEND an internal setpoint or TRACK the environment? -- and covers thermoregulation, brown-fat thermogenesis, the torpor/hibernation switch, whole-body energy homeostasis, and metabolic disease as ONE coupled setpoint-dynamics problem. Disease is a subset.

## What this package emerges and circulates
This is an INTEGRATIVE package: its primary objects are LOOPS, SETPOINTS and (for the thermometabolic
axis) a discrete SWITCH — not single organs. It re-emerges NO organs; it imports the already-emerged
organs and their dynamics from the per-system packages through the cited seams below (SSOT), and adds
the loop closure + the setpoint dynamics. Node identity + order are owned by DNA (measured γ, never
fitted); nodes whose γ is not yet in the atlas are honest **to-measure** inputs.

### Nodes
- **brown_adipose_thermogenesis** (`UCP1`) — γ=1.4054 (vendored, measured [V]) — uncoupled proton leak = heat, not ATP (the endotherm furnace) — *dyn:* thermogenic-switch — *anchor:* BAT cold-induced thermogenesis [L]
- **sympathetic_thermo_drive** (`ADRB3`) — γ=1.4462 (vendored, measured [V]) — beta3-adrenergic activation of BAT (cold -> heat command) — *dyn:* effector — *anchor:* cold-induced drive [L]
- **white_adipose_storage** (`PPARG`) — γ=1.3902 (vendored, measured [V]) — lipid storage + adipokine secretion (the lipostat storage node) — *dyn:* storage — *anchor:* adiposity setpoint [L]
- **melanocortin_appetite** (`MC4R`) — γ=1.272 (vendored, measured [V]) — hypothalamic energy-balance setpoint (intake control) — *dyn:* setpoint-loop — *anchor:* lipostat / appetite setpoint [L]
- **leptin_feedback** (`LEPR`) — γ=1.4554 (vendored, measured [V]) — adiposity feedback signal (storage -> brain) — *dyn:* feedback — *anchor:* leptin feedback gain [L]
- **insulin_glucose_effector** (`INSR`) — γ=1.4956 (vendored, measured [V]) — insulin-mediated glucose disposal (the euglycemia effector) — *dyn:* feedback — *anchor:* euglycemia setpoint ~5 mM [L]
- **ghrelin_hunger** (`GHRL`) — γ=1.355 (vendored, measured [V]) — gut hunger signal (drives intake; opposes leptin) — *dyn:* feedback — *anchor:* hunger drive [L]
- **torpor_fuel_switch** (`PDK4`) — γ **to-measure** (named master `PDK4`; fetch via DNA pipeline, never fitted) — metabolic fuel-switch to lipid + glucose sparing (torpor-associated program) — *dyn:* torpor-switch — *anchor:* torpor metabolic suppression [L]; PDK4 gamma TO-MEASURE
- **preoptic_thermostat** (`(hypothalamic_thermostat)`) — no single master gene (circuit/derived/diffuse) — preoptic setpoint comparator (the thermostat itself; circuit, no single master) — *dyn:* setpoint-comparator — *anchor:* thermal setpoint ~37C [L]
- **torpor_arousal_rhythm** (`(torpor_arousal_cycle)`) — no single master gene (circuit/derived/diffuse) — periodic interbout arousal during hibernation (slow relaxation oscillator) — *dyn:* oscillator — *anchor:* interbout arousal period (days) [L] TO-ANCHOR

### Seams IN (inherited / cited — the loop is closed from these, not re-emerged)
- digestive: pancreas-liver glucose homeostat CORE (cited, SSOT) -- this pkg closes the whole-body loop
- musculoskeletal: insulin-mediated glucose disposal arm (cited)
- integumentary + circulatory: heat-dissipation arm (vasodilation/sweat, cited)
- immune: pyrogen drive for fever (cited)
- mind: brain appetite/arousal edge (cross-referenced, not re-emerged)
- DNA: node identity (obesity_gamma masters) + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these setpoints; siblings cite them)
- defended core temperature + metabolic rate (systemic; this pkg is SSOT for the thermal/energy setpoints)
- MAP coupling note -> homeostasis_hemodynamic (metabolic syndrome cluster)
- monogenic metabolic lesions <-> disease_wp (parameter in / trajectory out)

## Research program (excavated; fill top-down, gate each layer)

This package does NOT start from disease. It starts from the question that DIVIDES homeotherms from
poikilotherms -- does the organism actively DEFEND an internal setpoint against the environment, or
TRACK the environment? -- and treats temperature, metabolism, torpor, and metabolic disease as one
coupled setpoint-dynamics problem. Disease is the last layer, not the first.

### Layer T -- Endothermy vs ectothermy (the foundational setpoint question)
- **RT1** In R19 terms, what distinguishes a setpoint-DEFENDING loop (homeotherm) from a setpoint-
  TRACKING system (poikilotherm)? Hypothesis: endothermy = an active control loop whose regulated
  attractor has a basin deep enough (loop gain high enough) to resist ambient drive; ectothermy = no
  active attractor, core state slaved to ambient. *Discriminant:* under an ambient-temperature drive
  sweep, does core temperature stay pinned (defended attractor) or follow the line (tracking)? [V]
- **RT2** The thermal setpoint as a regulated attractor: model the preoptic hypothalamic thermostat
  (comparator: setpoint vs core -> effector recruitment). *Discriminant:* a step in ambient is
  corrected back to setpoint with a cited gain/latency. setpoint ~37C [L]. [V]
- **RT3** The ENERGETIC COST of endothermy: holding a setpoint requires a high idling metabolic rate
  (the furnace runs hot even at rest). *Discriminant:* the basal metabolic rate needed to defend the
  setpoint against a cited heat-loss rate; the thermal-stability/energy-cost trade-off that makes
  endothermy a different basin from ectothermy. abs rate [O], ratio [V].
- **RT4** Continuum or discrete? Heterotherms and regional endothermy (tuna/billfish/some sharks,
  brooding pythons) sit between the regimes. *Discriminant:* is there an R19 spinodal separating the
  two strategies, or a smooth gradient? Test across cited species metabolic data. [V]
- **RT5** Kleiber allometry: metabolic rate ~ mass^(3/4). *Discriminant:* does the substrate reproduce
  the 3/4 (not 2/3) scaling exponent, or is the exponent an [O] needing external calibration?

### Layer G -- Thermogenesis & heat balance (the effectors)
- **RG1** Brown-adipose UCP1 uncoupling = proton leak -> heat, not ATP. Emerge BAT (UCP1, measured g)
  and model the thermogenic SWITCH: cold -> sympathetic -> ADRB3 -> UCP1 -> heat. *Discriminant:* a
  cold step recruits thermogenesis to defend the setpoint; cold-induced rate matches cited BAT output.
- **RG2** The cooling arm: vasodilation/sweat (seam to integumentary + circulatory). Bidirectional
  defense -- the thermostat must push BOTH ways. *Discriminant:* a heat load is corrected by the
  dissipation arm to setpoint (symmetry of defense).
- **RG3** Fever = a REGULATED setpoint ELEVATION (not a control failure) driven by immune pyrogens
  (seam to immune). *Discriminant:* fever is an upward setpoint shift (the loop now defends a higher
  value), distinguishable from hyperthermia (defense overwhelmed). A setpoint-shift, not a basin loss.

### Layer H -- Torpor / hibernation (the big comparative axis -- "is it just a switch?")
- **RH1 (central)** Is the euthermia<->torpor transition a DISCRETE bistable flip (two regulated
  attractors separated by an R19 spinodal, with HYSTERESIS) or a CONTINUOUS metabolic dial?
  *Discriminant:* sweep the torpor drive (declining photoperiod/ambient/fuel signal) UP and DOWN;
  hysteresis-loop width > 0 with a discontinuous jump => SWITCH; smooth reversible tracking => DIAL.
  Uses `torpor_switch_probe()` in the engine (R19 spinodal framing). mechanism [V].
- **RH2** Torpor is REGULATED, not mere cooling: the animal DEFENDS a LOW setpoint during torpor. So
  torpor = switching the thermostat's SETPOINT parameter to a low value, not abandoning regulation.
  *Discriminant:* during steady torpor, a perturbation below the low setpoint is actively corrected.
- **RH3** DNA implementation: how is the torpor program encoded? Is there a master regulator or a
  distributed transcriptional program (fuel-switch to lipid + glucose sparing, e.g. PDK4 axis)?
  Torpor-program master gamma is TO-MEASURE via the DNA pipeline (named candidates, not invented).
  *Discriminant:* does a small regulatory set gate the whole program (switch) or is it polygenic?
- **RH4 (why bears, not humans)** Is hibernation a switch that humans ALSO possess but keep locked,
  or a capability humans lack? Test the "present-but-suppressed switch" hypothesis by cross-species
  comparison (the DNA package already does human/mouse/snake/Drosophila): are the torpor-program genes
  + regulatory elements present in the human genome in a silenced state, or absent? [V]/[O]. This is
  the literal answer to "단지 그것이 스위치 개념인지".
- **RH8 (the panel-level test of RH4)** Widen RH4 from one fuel-switch gene to the whole declared torpor
  program (8 fuel-switch / BAT-identity genes) across many hibernating species (deep hibernators, a
  torpor-capable primate, daily heterotherms) plus GC-matched non-hibernating controls. *Pre-registered
  discriminant:* does ANY promoter γ separate hibernators from non-hibernators? *Result:* no — 0/8 genes
  separate, and every group γ gap IS the group GC gap (cross-gene r(Δγ,ΔGC)=0.9957). Hibernation is
  regulatory gating of present genes, not a γ threshold. [V] reads + GC confound / [O] no-marker
  conclusion (small n; species are not phylogenetically independent draws).
- **RH9 (the methylation-substrate test — the regulatory-layer object)** RH8 ruled out the stacking-
  stiffness layer, but γ is ~entirely GC-loaded across this panel (cross-cell r(γ,GC)=0.9955), so a
  skeptic could say only GC was tested. Read the methylation SUBSTRATE instead: CpG observed/expected
  (Gardiner-Garden & Frommer 1987), which is GC-NORMALIZED, over the same 8 genes × 14 species.
  *Pre-registered discriminant:* (i) does any gene's CpG-O/E range separate hibernators? (ii) is CpG O/E
  dissociated from γ? *Result:* 0/8 genes separate; CpG O/E is a distinct read from γ (cross-cell
  r(γ,CpG O/E)=0.5601) and far less GC-loaded (r(CpG O/E,GC)=0.4927). Two independent static sequence
  layers are both blind to hibernation — the capability is DYNAMIC regulatory gating of present genes,
  readable only in an in-vivo torpor↔euthermia methylation/expression contrast (cited, [O] external; the
  offline invariant precludes ingesting in-vivo data in-package). Computed from the existing cache — the
  panel and every read γ value are byte-identical. [V] reads + γ/CpG-O/E dissociation / [O] no-marker +
  dynamic-regulation external.
- **RH5** Depth gradient: daily torpor (small mammals) vs deep multiday hibernation (bears, ground
  squirrels). Same switch at different depths, or different mechanisms? *Discriminant:* one bistable
  axis with a tunable depth, vs distinct switches (parallels the digestive slow-wave gradient question).
- **RH6** Interbout arousals: hibernators periodically rewarm. The torpor-arousal rhythm is a SLOW
  relaxation oscillator (confirmed in the engine as an FHN). *Discriminant:* the arousal period and the
  cost/benefit of transiently leaving the torpor basin. period (days) [L].
- **RH7** Metabolic PROTECTION: hibernators survive low-glucose/low-temperature states that would
  damage a non-hibernator. *Hypothesis bridge to disease:* the torpor program is a SAFE, regulated
  version of metabolic suppression; metabolic disease may be an UNSAFE, chronic, uncoupled misfire of
  the same machinery (see RD4). [V]/[O].

### Layer E -- Energy homeostasis (the fuel side; nodes have measured gamma)
- **RE1** Whole-body glucose homeostat: extend the digestive pancreas-liver core (CITED, SSOT) with
  the muscle disposal arm (musculoskeletal seam) + adipose storage + brain sensing. euglycemia ~5 mM
  is a DEFENDED attractor. *Discriminant:* a glucose load returns to setpoint via the closed loop. [V]
- **RE2** Lipostat / adiposity setpoint: the leptin-melanocortin circuit (LEP/LEPR/POMC/MC4R/AGRP/NPY,
  measured gamma) -- storage signal -> appetite. *Discriminant:* a defended adiposity setpoint; chronic
  over/underfeeding is opposed by the loop. [V]
- **RE3** Thermo-fuel COUPLING: cold -> eat more AND burn more; the thermal and fuel loops share the
  furnace. *Discriminant:* cold raises both intake and expenditure in a coupled way (one shared node).
- **RE4** Adipose plasticity: white (storage, PPARG/CEBPA) vs brown (thermogenic, UCP1) vs beige; the
  white<->beige "browning" switch links storage to thermogenesis. *Discriminant:* browning shifts the
  energy balance toward dissipation (an R19 switch in adipocyte state).

### Layer D -- Disease as setpoint/attractor failure (the SUBSET, last)
- **RD1** T2D = the glucose loop's defense failing: insulin resistance lowers loop gain -> setpoint
  drifts high -> the system settles in a hyperglycemic attractor. An attractor-shift, modeled in
  `_pathology/setpoint_failure.py`. anchor [L] / shape [V] / absolute [O].
- **RD2** Obesity = the lipostat setpoint drifting UP (leptin resistance) -> defended at higher
  adiposity. Setpoint drift, not simply "eating too much". *Discriminant:* the defended setpoint moves.
- **RD3** Metabolic syndrome = CO-failure of multiple coupled loops (glucose + lipid + pressure[seam
  to hemodynamic]); why they cluster -> a shared upstream node. *Discriminant:* one perturbation moves
  several setpoints together.
- **RD4** The hibernation bridge: is insulin resistance a normally-adaptive, torpor-like fuel-sparing
  state that becomes pathological when chronic and uncoupled from a real torpor program (RH7)? A deep,
  falsifiable hypothesis unique to this framework. [V]/[O].
- **RD5** Monogenic forms (MODY, MC4R obesity, congenital leptin deficiency): the disease_wp package
  owns the GENE lesion; here it enters as a loop PARAMETER perturbation and the systemic trajectory is
  computed. Composition with disease_wp, not duplication.

### Cross-cutting
- Grade discipline (C3): mechanism/ratio [V]; cited setpoints/rates [L]; absolute metabolic rates and
  absolute incidence [O] with stated obstacles. No silent absolute claims, no fitted gamma.
- Comparative method: reuse the DNA multi-species pipeline for RT4/RH4 (cross-species gamma is an
  established move in this project).

## Pathology (disease as setpoint/attractor failure — a SUBSET, not the starting point)
Disease is modeled as a failure of a defended setpoint (loop-gain drop / setpoint drift / attractor-
shift) on the SAME R19 substrate. Composition with disease_wp: monogenic lesion = parameter in (cited);
systemic trajectory = computed here. Polygenic/acquired disease lives here as loop dysregulation.
Grades: anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle).
- **type 2 diabetes** ← insulin resistance -> glucose-loop gain drop -> hyperglycemic attractor
  - anchor/grade: RR / progression vs cited risk (BMI, HbA1c cohorts) [L]; attractor-shift shape [V]; absolute incidence [O]
- **obesity** ← leptin resistance -> lipostat setpoint drifts up -> defended at higher adiposity
  - anchor/grade: defended-setpoint drift vs cited energy-balance data [L]; shape [V]; absolute [O]
- **metabolic syndrome** ← co-failure of coupled glucose+lipid+pressure loops (shared upstream node)
  - anchor/grade: cluster co-movement vs cited prevalence [L]; multi-loop [V]; absolute [O]
- **(MODY / monogenic, via disease_wp)** ← gene lesion = a loop PARAMETER perturbation; trajectory computed here
  - anchor/grade: parameter from disease_wp [cited]; systemic trajectory [V]

**Restoration (the analgesic three-lever technology, firewalled).** For each setpoint failure, three levers:
S1 restore loop-gain, S2 reduce the pathological forcing, S3 remove the sensitising program. Each S3 link is
[O] cited; the γ-|h_sp| read is carried beside the editorial priority score, never folded into it; the
module passes S3-honesty / forbidden-claim / falsification gates.

**Layer R — Precision routing (the local-anaesthesia mirror).** A second reading of the restoration levers
asks WHERE each lever's node acts: the analgesic package separates a SYSTEMIC threshold-raiser (body-wide)
from a PRECISION local block (one nerve's territory); the same distinction places each restoration target on
a CITED anatomical COMPARTMENT map and classes it PRECISION (1 compartment) / REGIONAL (2–3) / SYSTEMIC (≥4,
or a distributed immune/stromal node) by a parameter-free rule on the cited compartment count. Routability
(which compartment, cited anatomy [F]) is kept distinct from deliverability (whether an intervention can REACH
it — blood-brain barrier, small BAT depot, no-single-locus; [O]). The firewall is PROVEN, not asserted:
`gamma_independence_gate()` recomputes the whole map under a perturbed γ atlas and the routing geometry is
byte-identical — γ is carried only as the promoter switch-threshold context, never an input to the routing.

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase + C1/C3 in research. C0 overrides on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and research signed off.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state passes by files only.
