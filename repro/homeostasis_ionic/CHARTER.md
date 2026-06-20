# CHARTER — Mineral and Acid-Base Homeostasis: Calcium-Phosphate, pH, and Electrolyte Setpoints

**paper_id:** `homeostasis_ionic_vp_site`  ·  **code:** `ion`  ·  **branch:** integrative (mineral / acid-base / electrolyte setpoint)  ·  **version:** 0.8.0 (research COMPLETE; writing built; cross-species axis + Tier-2 disease coverage + Tier-3 molecular transport dynamics & per-species γ + therapeutic-organizing three-lever principle added; concept DOI assigned)
**DOI:** TBD — assigned after writing & publication (추후 업데이트). Concept DOI + cross_volume_doi registry entry are added in the writing phase, not now.

## Scope (one line)
The third homeostasis axis: calcium-phosphate (PTH<->vitamin-D<->bone<->kidney<->gut), acid-base pH (respiratory CO2 + renal HCO3, a two-timescale buffer), and electrolyte (Na/K) setpoints defended as coupled loops. Osteoporosis and acid-base/electrolyte disorders are the disease axis.

## What this package emerges and circulates
Primary objects are LOOPS / OSCILLATORS / sense-organ instruments — node identity + order are owned by
DNA (measured γ, never fitted); nodes whose γ is not yet in the atlas are honest **to-measure** inputs.
It re-emerges NO organs owned elsewhere; it cites the seams below (SSOT) and adds its own dynamics.

### Nodes
- **parathyroid_pth** (`GCM2`) — γ=**1.4642** (measured [V]) — PTH secretion: the fast calcium-raising effector — *dyn:* setpoint-loop — *anchor:* serum Ca ~2.4 mM setpoint [L]
- **calcium_sensing_receptor** (`CASR`) — γ=**1.3299** (measured [V]) — the calcium SENSOR (setpoint comparator) — *dyn:* setpoint-comparator — *anchor:* Ca setpoint sensing [L]
- **vitamin_d_axis** (`VDR`) — γ=**1.4243** (measured [V]) — slow calcium-absorption control (gut/kidney) — *dyn:* slow-loop — *anchor:* vitamin-D Ca absorption [L]
- **bone_mineral_reservoir** (`RUNX2`) — γ=**1.2414** (measured [V]) — bone as the calcium/phosphate buffer (remodeling stores/releases) — *dyn:* reservoir — *anchor:* bone Ca buffer [L]
- **kidney_mineral_acidbase** (`SIX2`) — γ=1.5556 (vendored, measured [V]) — renal Ca/PO4 handling + HCO3 regeneration (acid-base integrator) — *dyn:* setpoint-loop — *anchor:* renal HCO3/Ca handling [L]

### Seams IN (inherited / cited)
- cardioresp: respiratory CO2 for the fast acid-base arm (cited)
- circulatory: renal perfusion / clearance (cited)
- musculoskeletal: bone identity (DNA SSOT) -- here in the mineral-reservoir role, not a fork
- digestive: gut Ca absorption (cited)
- DNA: identity + order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- defended serum Ca / PO4 + blood pH (systemic; this pkg is SSOT for mineral/acid-base setpoints)
- Na/K <-> volume coupling -> homeostasis_hemodynamic

## Research program (excavated)

The THIRD homeostasis axis (after thermometabolic and hemodynamic): mineral (calcium-phosphate) and
acid-base (pH) and electrolyte setpoints, each a defended attractor of a multi-organ loop. Calcium and
pH are owned by no single organ -- they are loop quantities, so this is integrative like the other two
homeostasis packages.

- **RI1** Calcium setpoint: serum Ca ~2.4 mM is defended by the PTH<->vitamin-D<->bone<->kidney<->gut loop
  (CASR is the sensor, PTH the fast effector, vitamin-D the slow effector, bone the reservoir).
  *Discriminant:* a Ca load/deficit is corrected back to setpoint; loop gain holds the value. [V], setpoint [L].
- **RI2** Acid-base: blood pH ~7.4 is defended by a TWO-TIMESCALE buffer -- respiratory CO2 (fast, seam to
  cardioresp) + renal HCO3 regeneration (slow, kidney). *Discriminant:* Henderson-Hasselbalch two-timescale
  correction of an acid/base load. [V], setpoint [L].
- **RI3** Bone as the calcium buffer: chronic Ca demand draws on the bone mineral reservoir via remodeling
  (overlaps musculoskeletal -- bone IDENTITY from DNA, here in the mineral-reservoir ROLE, not a fork).
  *Discriminant:* the reservoir/setpoint trade-off; sustained demand depletes the reservoir. [V].
- **RI4** Electrolyte: Na/K setpoints and their coupling to volume (seam to hemodynamic). *Discriminant:*
  Na/K deviations are corrected by renal handling; the volume<->pressure coupling. [V].
- **RI5** Phosphate: PO4 co-regulation with Ca (the FGF23 axis). *Discriminant:* Ca-PO4 product held;
  FGF23 as the phosphate-lowering arm. [V]/[O].
- Grades (C3): loop mechanism [V]; cited setpoints (Ca 2.4 mM, pH 7.4) [L]; absolute fluxes [O].

## Major diseases (non-rare) — covered here; rare/monogenic → disease_wp
Disease is modeled as a failure of a defended setpoint / clock / sense organ on the SAME R19 substrate.
The MAJOR (common, polygenic, acquired, age-related) diseases of this system are covered here; RARE and
monogenic forms are owned by disease_wp and only cross-referenced (entered here as a cited parameter).
Grades: anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle).
- **osteoporosis** ← chronic Ca/bone setpoint imbalance -> net reservoir depletion (post-menopausal / age)
  - anchor/grade: bone-density loss vs cited rates [L]; reservoir depletion [V]; cross-ref reproductive(estrogen) + aging
- **primary hyperparathyroidism** ← PTH setpoint reset upward -> hypercalcemia
  - anchor/grade: setpoint reset [V]; cited Ca/PTH [L]; rare genetic forms -> disease_wp
- **metabolic acidosis / alkalosis** ← the acid-base defense (renal or respiratory) fails
  - anchor/grade: two-timescale buffer failure [V]; cited pH [L]
- **common electrolyte disorders** ← hyper/hypo- natremia / kalemia (volume + renal handling)
  - anchor/grade: setpoint deviation vs cited [L]; loop [V]
- **nephrolithiasis (calcium stones)** ← supersaturation once the Ca/oxalate solubility threshold is exceeded
  - anchor/grade: crossing a solubility threshold [V]; cited [L]

## RESEARCH RESULTS (v0.2.0 — completed, all gates green)

All five master-gene γ MEASURED (NCBI promoters, SantaLucia 1998), validated bit-for-bit vs vendored SIX2.
Developmental order (γ asc): **bone(1.2414) < CaSR(1.3299) < vitD(1.4243) < PTH(1.4642) < kidney(1.5556)**.
Determinism: research_gate + run_all byte-identical across 2 runs (sha `35d31461…`).

**Substrate→control law (the fundamental).** A defended setpoint is an OU attractor dx/dt=−k(x−x*)+load+noise;
loop gain k sets rejection error load/k, correction time 1/k, variance σ²/2k. The node barrier b=γ²/4 supplies
k: barrier monotone ↑ in γ and perturbation-displacement monotone ↓ in γ (both verified). OU laws reproduced
(Var·2k/σ²≈1, err·k≈1, integral arm zeroes error). → γ sets setpoint STABILITY; the value stays cited. [V]

**Stress battery (RI1–RI5, all PASS):**
- RI1 calcium: Ca load→peak 2.13, deficit→nadir, returns to setpoint 1.0003 (Brown 4-param PTH; CaSR Hill≈3). [V]/[L]
- RI2 acid-base: pH 7.167→(fast resp, Winters slope 1.10)→7.307→(slow renal)→7.401; two-timescale buffer. [V]/[L]
- RI3 bone reservoir: serum Ca held (dev 0.032) while reserve depletes 1.00→0.43 monotonically = osteoporosis substrate. [V]
- RI4 electrolyte: Na 140 / K 4.2 loads corrected by renal handling; Na↔volume↔pressure cited to hemodynamic. [V]/[L]
- RI5 phosphate: PO4 load corrected; FGF23 arm; Ca×PO4 max 1.399 < precipitation 1.6. [V]/[O TmP/GFR]

**Sensory seam (감각세포 연결).** Homeostatic sensors = sensory-cell transducers; all 8 measured sensors are valid
R19 instruments, sharpness monotone in γ. Crown jewel **OTOP1** (proton channel = sour-taste receptor AND
otoconia CaCO3 pH-keeper) couples acid-base ↔ Ca-carbonate mineral ↔ vestibular gravity sense; BPPV at the seam.
Cited identities [L] + instrument check [V].

**Literature cross-checks.** 7 anchors (Brown 1991/1983, Henderson-Hasselbalch, Winters 1967, Na/K, Ca×PO4, OU) +
9 molecular interactions; all 4 sim-vs-literature cross-checks consistent.

**Pathology — 6 derived failure modes (all demonstrated):** loop-gain drop (Var blow-up ratio 5.15≈5.0), setpoint
drift (defends 1.150), reservoir depletion, buffer-arm failure, spinodal/threshold crossing (discontinuous),
instrument failure. 7 diseases mapped (osteoporosis, primary hyperPTH, metabolic acidosis/alkalosis, electrolyte
disorders, nephrolithiasis, ADH1, BPPV); rare/monogenic forms enter as cited parameters (→ disease_wp).

**Fundamental therapy (근본적 치료책) — failure-keyed taxonomy (5 classes) + 2 demonstrations:**
- T1 set-point reset: calcilytic/calcimimetic shifts comparator back, normalizes defended value 1.150→1.000
  (encaleret CALIBRATE Phase-3 positive 2025 for ADH1; cinacalcet down for hyperPTH). [V]/[L]
- T2 reservoir refill vs withdrawal-slow: anabolic refills 1.00 > anti-resorptive 0.85 > untreated 0.33 →
  anabolic-first derived (teriparatide/abaloparatide/romosozumab vs bisphosphonate/denosumab). [V]/[L]
- 4 frontier hypotheses: **ALL FOUR now QUANTIFIED [V]** — H-DUAL anti-sclerostin+anti-DKK1 anabolic window
  dual 12.79 > single 1.08 > untreated 0.00 (single window closes; Florio 2016 [L]) and H-OTOC otoconial
  calcite saturation Ω drops below 1 under acidosis (0.695) / hypocalcemia (0.755) (Frontiers 2025 [L]) were
  quantified in v0.3.0; **H-RESET** (generalize sensor recalibration — defended attractor == comparator
  set-point for every Hill slope, so allosteric reset is durable while symptom control relapses; residual
  0.15 vs ~0; CaSR/ENaC/ASIC/OTOP1; encaleret CALIBRATE / cinacalcet [L]) and **H-ARM** (restore failed
  acid-base arm at source — OU law, restoring k tightens variance & rejects fresh load by k_high/k_low≈4.0×
  vs lifelong buffering; dRTA → ADV7103/Sibnayal [L]) are quantified in **v0.4.0**. Direction [V]; absolute
  magnitudes [O]; human clinical efficacy [H].

**v0.3.0 research increment (TmP/GFR closure + frontier quantification):**
- RI5 renal phosphate threshold TmP/GFR is now **COMPUTED exactly** (Walton-Bijvoet 1975 nomogram,
  `renal_phosphate.py`): normal 1.114 mmol/L (in reference 0.80–1.35 [L]); FGF23/PTH lower it (XLH 0.450 <
  normal < hypoPTH 2.342, direction [V]/[L]). The old blanket [O] is narrowed to a precise by-design residual:
  γ sets loop STABILITY, not the absolute VALUE (value is [CAL]/[F], not γ-derivable). Additive modules; the
  research gate sha is unchanged (`35d31461…`, all_green) — γ-emergence + stress battery untouched.

**v0.4.0 research increment (frontier program complete — H-RESET + H-ARM):**
- The last two bare-[H] frontier hypotheses are now quantified to a reproduced mechanism (`frontier_quant.py`
  `h_reset_generalization`, `h_arm_restoration`), completing the four-hypothesis program begun in v0.3.0.
  **H-RESET** reuses the volume's own inverse-sigmoid comparator (`pth_curve`): the defended attractor equals
  the comparator set-point for every Hill steepness (a structural identity, not a fit), so an allosteric reset
  relocates the defended value durably (residual ~0) while symptom control relapses on withdrawal (residual
  0.15) — the direction holds for the whole ionic-sensor family CaSR/ENaC/ASIC/OTOP1. **H-ARM** reuses the
  volume's own OU law (err=load/k, Var=σ²/2k): restoring the failed arm (raising k) tightens variance and
  rejects a fresh acid load by the factor k_high/k_low (≈4.0×; excursion 2.00→0.50), whereas lifelong
  buffering cancels only the mean and must be sustained. Anchored to encaleret Phase-3 CALIBRATE / cinacalcet
  (A-RESET [L]) and distal-RTA → ADV7103/Sibnayal (A-ARM [L]). Direction [V]; magnitudes [O]; clinical [H].
  Additive only — the research gate sha is unchanged (`35d31461…`, all_green); docs concat sha advanced to
  `6d6a2000…` (rebuild byte-identical).

**v0.5.0 remediation increment (cross-species axis — the audit's largest gap):**
- A v0.4.0 audit found the volume modeled ONE species (human) and could not say which animals use ions
  precisely versus conform to the environment. `comparative_ionoregulation.py` (NEW) adds that axis on the
  SAME R19 substrate, reusing the volume's OWN OU law (step error = load/k) with a single knob — the loop
  gain k that defends the internal milieu against the salinity load. Cited strategies [L]: osmoconformer
  (k 1.0, tracks environment 100%) < urea-retaining elasmobranch (2.0) < freshwater/marine teleost regulator
  (3.0) < terrestrial mammal (4.0, tracks 25% = tightest, this volume's baseline). Reproduced: under a
  salinity load the conformer is dragged to 1.00 while the terrestrial regulator holds at 0.25 — ratio 4.0×
  == gain ratio k_reg/k_conf; the excursion is monotone in k. Separation [V]; absolute k & salinity tolerance
  [O]; per-species master-gene γ not yet measured [O]/[H]. Surfaced in `run_all` [10] + docs §10; A-OSMO
  anchor added. Additive — research gate sha unchanged (`35d31461…`); docs concat sha advanced to `d6a67a25…`
  (10 section pages). The roadmap for the remaining gaps (Mg / CKD-MBD / humoral hypercalcemia in Tier-2;
  transporter gating dynamics + per-species γ in Tier-3) is in `REMEDIATION_PLAN.md`.

**v0.6.0 remediation increment (Tier-2 disease coverage — Mg / CKD-MBD / humoral hypercalcemia):**
- The same v0.4.0 audit asked whether every ion-imbalance disease was covered. The pathology chapter closed
  seven representative diseases on six failure modes and let rare/specific forms enter as a cited parameter;
  three further MAJOR diseases were named but not yet modelled. `tier2_ion_diseases.py` (NEW) closes them by
  REUSING the existing six failure modes — no new primitive: **G2 magnesium** (hypo-/hypermagnesemia) is the
  loop-gain-drop / buffer-arm-failure mode read on a third defended ion via the volume's own `ou_setpoint`
  (err=load/k): a failed arm (low k) under an Mg-loss drive yields hypomagnesemia (TRPM6/Gitelman), under an
  Mg-intake drive hypermagnesemia, both monotone in 1/k, ratio == gain ratio, variance blow-up. **G3 CKD-MBD**
  is a multi-arm loop-gain drop of the renal integrator: stepping the renal gain down drives the cited KDIGO
  cascade — PO4 up (err=load/k), 1,25-vitD down, Ca down, PTH up (secondary hyperparathyroidism) all monotone,
  the Ca×PO4 product near-normal early and climbing to the precipitation ceiling in advanced CKD. **G4 humoral
  hypercalcemia of malignancy** is a set-point drift UP: an exogenous unsuppressible PTHrP drive relocates the
  defended Ca up (the inverse of the T1 reset) with endogenous PTH appropriately suppressed — the clinical
  fingerprint. Directions [V]; cited setpoints/variants/guidelines [L] (Mg ~0.85 mM; TRPM6 Schlingmann 2002;
  Gitelman SLC12A3; KDIGO 2017 CKD-MBD; PTHrP Stewart 2005 NEJM); absolute magnitudes / CKD timing [O].
  Surfaced in `run_all` [11] (GATES → [12]) + docs §11; anchors A-MG, A-CKD, A-PTHRP added. Additive — research
  gate sha unchanged (`35d31461…`); docs advanced to **11 section pages**. Remaining: Tier-3 (transporter gating
  dynamics; per-species master-gene γ), per `REMEDIATION_PLAN.md`.

**v0.7.0 remediation increment (Tier-3 — molecular transport dynamics G5 + per-species γ G6; completes "cover everything"):**
- The v0.4.0 audit's last two open items are now closed. **G5** (`transport_dynamics.py`, NEW) adds the one new
  FORCED primitive — the **GHK constant-field flux** through a gated channel (reverses exactly at the Nernst
  potential, rectifies) plus Boltzmann/Hill gating — the molecular "how" beneath the loop arms. Its central
  result is a CONNECTION: the membrane flux slope at the setpoint **k = −dJ/dC IS the OU loop gain** the rest of
  the volume already runs on [V] (it recovers Var=σ²/2k and err=load/k, rises linearly with channel number, and
  a loss-of-function transporter drops k by the gain ratio — the loop-gain-drop *at the membrane*, the molecular
  reading of TRPV5/6 → renal Ca wasting, ENaC/SCNN1A → PHA1, H⁺-ATPase/ATP6V → distal RTA). GHK+gating [F];
  k=−dJ/dC = OU gain [V]; absolute single-channel conductances / channel densities [O].
- **G6** (`comparative_gamma.py`, NEW; `comparative_promoters.cache.json`) is an **HONEST NEGATIVE**, reported
  not hidden: the osmoregulatory master gene **ATP1A1** (Na⁺,K⁺-ATPase α-1) promoter γ was MEASURED across six
  species (Pacific oyster / elephant shark / thorny skate / zebrafish / Xenopus / human) by the same NN-stacking
  pipeline, human-anchored and offline-reproducible [V], the pipeline sound (two independent elasmobranchs agree
  to γ±0.0003). But γ is non-monotone in the loop gain k (Spearman 0.65; the k=3.0 Xenopus γ exceeds the k=4.0
  human) and tracks promoter GC almost perfectly (Spearman 1.0) — so per-species γ is the wrong instrument and
  the within-genome γ-ladder does not transfer cross-genome. The comparative absolute k stays [O], now with that
  GC confound as its documented reason rather than a bare placeholder.
- Surfaced in `run_all` [12]/[13] (GATES → [14]) + docs §12/§13; anchors A-GHK, A-TRPV, A-ENAC, A-HATPASE,
  A-ATP1A1 added. Additive — research gate sha unchanged (`35d31461…`); docs advanced to **13 section pages**
  (rebuild byte-identical). The only new [O] is G5's absolute electrophysiological calibration. This completes
  the Tier roadmap (`REMEDIATION_PLAN.md` F: all three audit axes covered).

**v0.8.0 therapeutic-organizing increment (three-lever principle — cross-volume inheritance + owned-disease remediation; concept DOI assigned):**
- A genuinely new layer beyond the completed Tier roadmap. The volume inherits a **therapeutic-organizing technology
  from the non-opioid analgesic volume** (concept DOI **10.5281/zenodo.20733420**) and proves it on this volume's own
  DNA-grounded loop — the five organs already emerged from MEASURED master-gene γ (RUNX2 1.2414 · CASR 1.3299 ·
  VDR 1.4243 · GCM2 1.4642 · SIX2 1.5556; NCBI + SantaLucia 1998; never fitted) → barrier b=γ²/4 → loop gain k. The
  levers are read off that measured chain, so this is a DNA-grounded therapeutic frame, not a toy.
- **Three-lever principle** (`three_lever.py`, NEW): a defended setpoint dx/dt=−k(x−x*)+load+noise has exactly three
  independent handles — **L1** load (source), **L2** loop gain k (gain), **L3** target x* (setpoint). Asymmetry theorem
  on the volume's own OU law: *only L2 tightens the variance σ²/2k* (L1 lowers the mean only; L3 relocates the defended
  value durably) [V]. The **L2 gain ceiling per arm is the measured-γ barrier b=γ²/4** — monotone in γ, deepest SIX2,
  shallowest RUNX2 [V]. The 27 non-opioid analgesic targets map one-to-one onto L1/L2/L3 [L] (same R19 threshold
  object at two sites). **Crosswalk:** every therapy already in this volume re-reads as exactly one lever (set-point
  resets = L3; reservoir refill / dual-antibody / renal-HCO₃-arm restore = L2; otoconia / stone-spinodal / driver
  removal = L1), all validated live [V].
- **Disease remediation** (`disease_remediation.py`, NEW): the nine **owned** diseases each get a **primary lever
  SELECTED from the corrupted OU parameter**, demonstrated on the OU law, turned into a cited honestly-graded
  improvement. Distinctive calls: osteoporosis **anabolic-first** (refill the gain before holding the drain);
  hyperparathyroidism & ADH1 = **setpoint resets** (cinacalcet down / encaleret up); CKD-MBD = **multi-arm failure
  needing all three levers**; calcium stones = **fixed-threshold disease where L2 does not apply** (L1 + L3). Owned =
  common/polygenic/acquired/age-related loop disorders; rare/monogenic → disease_wp (cited), carcinogen cancers →
  mechanistic volumes; **VP_FRAMEWORK_MAP §6 boundaries not crossed**.
- Surfaced in `run_all` [15]/[16] (GATES → [17]) + docs §14/§15/§16. Additive — research gate sha unchanged
  (`35d31461…`, all_green, determinism 2×sha256 identical); the two therapy modules import only `vp_loops`/existing
  modules and do not feed the gate; the engine tree is byte-identical. Docs advanced to **16 section pages**. No new
  [O] item (both modules reuse the existing OU law; absolute clinical magnitudes remain [O]/[H] as before).

### Writing manifest (built — `docs/`, VP-SPEC v1.8)
Hub + **16 section pages**, each answer-first + JSON-LD (ScholarlyArticle + BreadcrumbList) + claim-strip +
vp-card + English body + sitemap.xml + robots.txt (7 bots) + llms.txt. Numbers pulled deterministically at
build time (no hand-entry); rebuild byte-identical. Sections: 01 substrate-loop-gain · 02 calcium-loop ·
03 acid-base-two-timescale · 04 bone-reservoir-osteoporosis · 05 electrolyte-Na/K · 06 phosphate-FGF23 ·
07 sensory-seam · 08 disease-as-setpoint-failure · 09 fundamental-therapy · 10 comparative-ionoregulation ·
11 magnesium-CKD-MBD-humoral-hypercalcemia · 12 molecular-transport-dynamics-GHK-gating ·
13 comparative-master-gene-γ-honest-negative · 14 three-lever-therapeutic-principle (source/gain/setpoint) ·
15 mineral-bone-disease-three-levers (osteoporosis/hyperparathyroidism/CKD-MBD) ·
16 acid-base-electrolyte-stone-disease-three-levers.
The concept DOI **10.5281/zenodo.20755910** is embedded throughout (JSON-LD identifier/sameAs, claim-strip,
footer, llms.txt), with a cross-volume citation to the analgesic DOI 10.5281/zenodo.20733420.
**Remaining (next session):** cross_volume_doi registry entry alongside sibling volumes; cross-link the seams to
sibling volumes once all volumes share a site root; optional SVG equation figures. (All Tier axes and the
therapeutic-organizing layer are DONE; the concept DOI is assigned and embedded.)

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase + C1/C3 in research. C0 overrides on conflict.
- **Research-first:** SATISFIED — stress battery green, `reports/research_complete.json` signed off, `PHASE=writing`. `tools/build_docs.py` has been run; `docs/` is built.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **DOI:** TBD — assigned after writing & publication (추후 업데이트). Concept DOI + cross_volume_doi registry entry are added in the writing phase, not now.
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state passes by files only.
