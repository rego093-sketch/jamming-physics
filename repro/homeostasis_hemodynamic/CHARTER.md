# CHARTER — Hemodynamic Homeostasis: Arterial Pressure, Volume, and Hypertension as Setpoint Reset

**paper_id:** `homeostasis_hemodynamic_vp_site`  ·  **code:** `hmd`  ·  **branch:** integrative (pressure / volume / perfusion setpoint)  ·  **version:** 0.7.0 (comfort-logic intervention layer)

## Scope (one line)
Mean arterial pressure (MAP) is owned by no single organ; this package closes the CO x SVR x volume loop from the per-system seams and studies its fast (baroreflex) and slow (RAAS/pressure-natriuresis) defense -- with essential hypertension modeled as a setpoint RESET (the exact parallel of the lipostat reset in obesity) and chronic heart failure as an R19 basin collapse. Low pressure is the symmetric counterpart: hypotension is not one disease but a NODE DECOMPOSITION of the same loop (orthostatic/autonomic, adrenal, distributive, hypovolemic, cardiogenic). The universality of the framework is tested by deriving the defended setpoint as an EMERGENT property of loop accretion across organism grade (open systems -> incidental pressure; single-circuit fast reflex -> error-regulated; closed + effector + integrator -> defended).

## v0.7.0 upgrade (comfort-logic intervention layer — the analgesic three-lever technique, ported)
This revision ports the three-lever intervention technique from the non-opioid analgesic whitepaper
(`analgesic_threshold_logic_v2.0`, concept DOI `10.5281/zenodo.20733420`) and applies it — within this
package's existing scope (the loop-dysregulation diseases: essential hypertension + chronic heart
failure) — to the defended arterial-pressure setpoint. It rests entirely on results this package already
proved: the MAP loop is an integral controller that **rejects** an operating-point push back to its
reference (RP4) while a **reference reset** is durable (T1). Read structurally, that counter-regulation
IS the antihypertensive side-effect class; a reference-reset direction provokes none. The new layer
(`repro/_intervention/`) maps three levers onto this — H1 reset-reference (counter-regulation-free,
DNA-grounded on REN/SIX2 γ), H2 restore-buffer (low), H3 unload-effector (paired-only, rejected alone) —
plus HP1–HP7 hypothesis-only proposals, a declared-weight axis ranking, a per-axis honesty gate, a
falsification register, and a fail-closed forbidden-claim firewall. Battery 21→26 (IV1–IV5); docs
13→21 pages (§13–§20, one page per idea). The concept DOI `10.5281/zenodo.20756801` is registered and
hardcoded. **Firewall boundary:** the package states a structural prediction about which lever directions
provoke the loop's counter-regulation; it asserts no molecule, regimen, efficacy, tolerability, or safety
result (`[O]`), and "counter-regulation-free" is structural, not a clinical claim. No medical responsibility.

## v0.2.0 upgrade (what this revision added)
The previous revision was a research SKELETON. This revision EXCAVATED the fundamentals the CHARTER asks
for and made the stress battery genuinely green (9/9 computed discriminants, no silent passes):
1. **Sensory transduction layer** (`repro/_sensory/`) — the molecular transducers beneath the
   controllers: baroreceptor **PIEZO1/2** mechanosensor (fast loop) and macula-densa **NKCC2** NaCl
   chemosensor (slow loop). Afferent firing confirmed as a shared-R19 spike train. (S1, S2)
2. **Closed setpoint loops** (`repro/_engine/vp_hmd_loops.py`, RP1–RP5) — MAP from seams; baroreflex
   buffering + PIEZO-KO labile; kidney integral controller (perfect adaptation); hypertension setpoint
   reset (opposed back); HF basin collapse (saddle-node fold). All RUN and PASS.
3. **Literature interaction map** (`build_interaction_map()`, 7 nodes / 11 edges; `LITERATURE.md`) —
   sensory cell → afferent → integrator/controller → effector → MAP → feedback, each edge graded + anchored.
4. **Fundamental-vs-symptomatic therapy** (`repro/_therapy/fundamental_targets.py`, T1, T2) — the more
   fundamental treatment of the two major diseases, matching the clinical evidence base in both directions.
5. **Pathology laws** (`repro/_pathology/setpoint_failure.py`) — the placeholder is replaced by the
   derived reset law (P* = P0 + dPset, opposed back) and the derived collapse law
   (saddle-node at spinodal(kappa*) = |load|), each self-confirmed against the loop sweep.

Determinism holds across all new modules under one hash (VP-SPEC C1). Writing stays LOCKED:
PHASE is kept at `research` for a clean handover; the next session flips PHASE=writing to unlock build.

## What this package emerges and circulates
This is an INTEGRATIVE package: its primary objects are LOOPS, SETPOINTS, SENSORS and the disease
attractor structure. Its node identities are grounded in real DNA — each control node's master-gene γ is
MEASURED from the actual human promoter (NN-stacking ΔG37, SantaLucia 1998) and validated against the locked
DNA atlas bit-for-bit, never fitted. On those grounded identities it closes the multi-organ loop, builds the
molecular sensory layer, and reconstructs the setpoint/basin dynamics. The canonical derivation of organ
identity and developmental order remains the DNA volume's (SSOT); this package re-measures the relevant
master-gene γ in-package and imports the circuit-level seams below. The one named master not yet in the atlas
at v0.2.0 — `REN` — has since been MEASURED in-package on the identical NN pipeline (validated by reproducing
SIX2 exactly); no nodes remain to-measure.

### Control nodes
- **kidney_volume_integrator** (`SIX2`) — γ=1.5556 (vendored, measured [V]) — pressure-natriuresis + RAAS volume control (the slow integrator) — *dyn:* setpoint-loop — *anchor:* Na/volume handling [L]
- **raas_endocrine** (`REN`) — γ=1.3634 (measured in-package on the validated NN pipeline, never fitted) — renin-angiotensin-aldosterone slow pressure/volume control — *dyn:* slow-loop — *anchor:* RAAS setpoint [L]; REN gamma measured [V]
- **baroreflex** (`(baroreflex_arc)`) — no single master gene (circuit/derived/diffuse) — autonomic fast pressure buffer (cite cardioresp/neuro) — *dyn:* fast-buffer — *anchor:* baroreflex gain [L]; circuit, cite siblings
- **vascular_resistance** (`(vascular_tone)`) — no single master gene (circuit/derived/diffuse) — SVR / Windkessel tone (cite circulatory vessels) — *dyn:* effector — *anchor:* SVR; cite circulatory

### Sensory transducer nodes (the fundamental layer — NEW in v0.2.0)
- **baroreceptor** — transducer **PIEZO1/PIEZO2** (mechanically activated cation channel) — reads arterial-wall stretch ~ pressure — fast loop — feeds `baroreflex` — identity [L] (Zeng 2018: double-KO abolishes baroreflex → labile hypertension)
- **macula_densa** — transducer **NKCC2** (apical Na-K-2Cl cotransporter, furosemide-sensitive) — reads luminal NaCl ~ distal delivery/GFR — slow loop — feeds `raas_endocrine` (renin, inverse) + `kidney_volume_integrator` (TGF) — identity [L]

### Seams IN (inherited / cited — the loop is closed from these, not re-emerged)
- cardioresp: cardiac output + baroreflex edge (cited); carotid-body + cardiopulmonary receptors (cited afferent seams, NOT re-emerged)
- circulatory: vascular resistance / Windkessel (cited)
- DNA: kidney identity (SIX2) + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these setpoints; siblings cite them)
- defended MAP (systemic; this pkg is SSOT for the pressure setpoint)
- pressure coupling -> homeostasis_thermometabolic (metabolic syndrome cluster)

## Research program (status: RP1–RP9 + S1–S2 + T1–T2 + C1 + CAL1–CAL7 all PASS)

The defining variable -- MAP -- is owned by NO single organ; it is the product of a multi-organ loop.
This package closes that loop from the per-system seams, reads it through the sensory layer, and studies
its setpoint defense and its failure (hypertension, heart failure), in parallel with the thermometabolic
package.

- **RP1 [PASS]** MAP = CO (seam: cardioresp) x SVR (seam: circulatory) + CVP. Resting MAP = 93.0 mmHg
  from the seam variables, err 0.0; owned by no single organ. relation [V] · numeric [L] · abs [O].
- **RP2 [PASS]** Fast buffer — baroreflex: a 20 mmHg step is buffered 75% (open-loop gain 3); PIEZO
  double-KO removes transduction → labile (no buffering). shape [V] · gain/latency [L].
- **RP3 [PASS]** Slow loop — RAAS + renal pressure-natriuresis (Guyton): the kidney (SIX2) is the
  integrator. Two transient volume loads correct to the SAME setpoint (spread 0.0 = perfect adaptation,
  "infinite gain"). shape [V] · anchor [L] · absolute setpoint [O].
- **RP4 [PASS]** Setpoint defense vs setpoint RESET: essential hypertension = the curve RESETS to defend
  a HIGHER pressure (+20 mmHg attractor-shift); an operating-point drug is opposed back to the reset
  reference. Exact parallel of the lipostat reset in obesity. shape [V] · risk anchor [L] · abs [O].
- **RP5 [PASS]** Decompensation — chronic heart failure as the cardiac high-output basin ANNIHILATING in
  a saddle-node fold (as contractility κ falls at fixed load), distinct from a reset. fold [V] · markers [L] · abs [O].
- **S1 [PASS]** Baroreceptor PIEZO1/2 mechanosensor: intact firing monotone in pressure; KO flat; afferent = shared-R19 spike train. curve [V] · identity [L] · abs Hz [O].
- **S2 [PASS]** Macula-densa NKCC2 chemosensor: renin DECREASES and TGF INCREASES with luminal NaCl (both monotone); SGLT2i raises delivered NaCl → restores TGF. shape [V] · identity [L] · abs [O].
- **T1 [PASS]** Hypertension therapy: an operating-point drug is opposed back (not durable) while a renal REFERENCE reset durably lowers the defended pressure. direction [V] · clinical durability [L] · abs effect [O].
- **T2 [PASS]** HF therapy: effector-flog (inotrope) SHRINKS the barrier margin M = spinodal(κ) − |load|
  (accelerated collapse, PROMISE) while load-reduce + cycle-break GROWS it (basin restored, four pillars). direction [V] · clinical mortality [L] · abs [O].
- **RP6 [PASS]** Orthostatic/autonomic hypotension = loss of the FAST buffer (the symmetric counterpart of RP2): a downward postural step is buffered intact but passes fully under autonomic failure / PIEZO-KO. shape [V] · gain/latency [L] · abs [O].
- **RP7 [PASS]** Adrenal insufficiency = the renal reference resets DOWN (lost RAAS set-point; mirror of RP4): a fluid bolus is opposed back to the low reference while restoring the reference (mineralocorticoid) is durable. shape [V] · clinical [L] · abs [O].
- **RP8 [PASS]** Distributive/vasoplegic shock = the RESISTANCE EFFECTOR (SVR) collapses (distinct from the RP5 cardiac arm): MAP falls below the perfusion floor even with doubled CO; a vasopressor (restore SVR) beats inotrope-only. shape [V] · clinical [L] · abs [O].
- **RP9 [PASS]** Hypovolemic shock = the VOLUME SUBSTRATE is depleted: renal natriuresis is excrete-only, so a volume EXCESS self-corrects (RP3) but a volume DEFICIT is a fold the kidney cannot self-correct -- only external volume restores it. shape [V] · clinical [L] · abs [O].
- **C1 [PASS]** Universality: a defended pressure setpoint EMERGES by loop accretion -- incidental (open systems) → error-regulated (single-circuit fast reflex) → defended (closed + effector + integrator); the defended regime requires all three legs simultaneously. emergence [V] · phylogeny [L] · abs per taxon [O].
- **CAL1–CAL7 [PASS]** Absolute-scale calibration (`repro/_calibration/scale_calibration.py`): each declared absolute `[O]` scale is closed by `[CAL]` = cited anchor → already-locked `[V]` relation (no new substrate math) → independent cross-check with a computed discriminant. **CAL1** mmHg pressure scale (CO/SVR/CVP → RP1, all land in clinical bands); **CAL2** baroreflex gain (G=3 → buffered 0.75 + residual mmHg); **CAL3** firing Hz (one F_max anchor → whole sigmoid; ~50 Hz at setpoint); **CAL4** macula-densa NaCl/GFR (operating point → NKCC2 curve, honest ~2× note); **CAL5** hypertension reset in clinical SBP; **CAL6** therapy effect sizes (RDN within 15 %; HF signs match); **CAL7** perfusion floor (≥65 mmHg) + orthostatic threshold (≥20 mmHg). `[CAL]` is calibration, **not** derivation — first-principles absolute scales stay `[O]`; five residual items (disease incidence, single-nephron GFR/K_m, trial HR/NNT, per-taxon pressures, exact transition clade) stay `[O]`, not forced.
- Grades (C3): product/ratio/direction [V]; cited setpoints/gains/mortality [L]; absolute pressures, incidence, firing rates, GFR, effect sizes [O]; calibrated-to-clinical-scale (anchor+propagate+cross-check) [CAL].

## Fundamental treatment of the major diseases (the "근본 치료책")
The loop structure yields a SHARP, falsifiable distinction the visible-mechanism view misses, and it
matches the clinical evidence base in BOTH directions (module `repro/_therapy/`):
- **Hypertension** is an integral-controller setpoint RESET → treat the **renal reference** (denervation,
  sustained Na/weight reduction, RAAS blockade, baroreflex activation), not the operating point. Durable
  BP reduction tracks reference reset; operating-point pushes are rejected back. Anchors: renal
  denervation durable & time-increasing (FDA-approved 2023); diuretic/renal backbone required [L].
- **Chronic heart failure** is an R19 basin COLLAPSE → treat the **margin** M = spinodal(κ) − |load| by
  reducing load + breaking the maladaptive neurohormonal cycle (four pillars), never by flogging the
  effector. Mortality benefit tracks margin growth; inotropes shrink it. Anchors: PROMISE (milrinone
  +28% mortality) vs four pillars (ARNI/BB/MRA/SGLT2i) [L]. SGLT2i links to the macula-densa sensor.

## Pathology (disease as setpoint reset / basin collapse — derived laws)
Disease is modeled as a failure of a defended setpoint on the SAME R19 substrate, with the laws now
DERIVED (not placeholder), in `repro/_pathology/setpoint_failure.py`:
- **essential hypertension** — integral-controller RESET. Law P* = P0 + dPset; the defended attractor
  shifts by EXACTLY dPset and operating-point pushes are rejected back. setpoint-reset shape [V]; RR vs
  cited risk (Na, BMI cohorts) [L]; absolute incidence [O].
- **chronic heart failure** — saddle-node BASIN COLLAPSE. Law: the high-output fixed point exists iff
  spinodal(κ) > |load|, annihilating at κ* solving spinodal(κ*) = |load| (closed form matches the sweep).
  collapse dynamics [V]; progression vs cited markers [L]; absolute rate [O].
Composition with disease_wp: monogenic lesion = parameter in (cited); systemic trajectory = computed here.

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase + C1/C3 in research. C0 overrides on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and research signed off. Research is GREEN and signed off (`reports/research_complete.json`, all_green=true); PHASE=`writing`, docs published.
- **v0.4.0:** the one ledger `[O]→[V]` elevation is done — REN master-gene γ is now measured (1.3634) on the validated NN pipeline (reproduces SIX2 exactly, never fitted; cache + `measure_gamma.py` in `inherited/`). No masters remain to-measure.
- **v0.5.0:** symmetry + universality completed — hypotension node-decomposition (`repro/_pathology/hypotension_family.py`, RP6–RP9 + cardiogenic + node-specific therapy T3) and cross-organism setpoint emergence (`repro/_comparative/setpoint_emergence.py`, C1). Stress battery 9/9 → 14/14, all on the existing primitives (no new substrate math), deterministic under one hash.
- **v0.6.0:** absolute-scale `[CAL]` calibration track added (`repro/_calibration/scale_calibration.py`, wired into the engine + gated CAL1–CAL7). Each of the nine declared absolute `[O]` scales gets a companion `[CAL]` row: cited anchor → already-locked `[V]` relation (no new substrate math, C1) → independent cross-check with a computed discriminant; first-principles derivation stays `[O]` (calibration ≠ derivation, mirroring absolute *g* in the physics volume) and five genuinely un-calibratable items stay residual-`[O]` (not forced into a pass). Stress battery 14/14 → 21/21, deterministic under one hash; ledger gains a "Calibrated (v0.6.0)" section.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state passes by files only.
