# REPRODUCE

> **digestive_vp_site v0.16.0** · DOI (concept): [10.5281/zenodo.20755319](https://doi.org/10.5281/zenodo.20755319) · CC BY 4.0 · ORCID 0009-0002-7535-8245.
> **v0.16.0 — §30 builds the live cross-package harness (the last frontier item, OUT OF GATE).** A runner loads THIS volume together with its sibling VP volumes (circulatory, musculoskeletal, neuro) in ONE process and confirms, against the LIVE sibling engines, the cross-volume identities the §27 seam and §28 analgesic layers had taken on trust: the shared R19 substrate (spinodal |h_sp| = 2(g/3)^1.5 and barrier g²/4 byte-identical, cross-volume drift 0), circulatory's live `hepatic_clearance()` reproducing the vendored snapshot (Q_H=1500 mL/min, E=0.75, F=0.25, CL_H=1125 mL/min), the inherited 27-target analgesic map re-deriving through every volume's own spinodal (drift 0, musculoskeletal the built second host), and the neuro nociceptor the §18→`mind` one-way pointer targets (Na_V1.7/SCN9A, master PRDM12). **Verify-alone is preserved:** `repro/run_all.py` (the research gate) and `tools/build_docs.py` (the canonical build) compute nothing in the harness and never import a sibling, so each volume re-establishes its entire trusted state from its own archive with the siblings **absent**; the sibling engines are **loaded by file path, not imported** (zero sibling import statements in the harness, self-checked); and the harness digest hashes only the in-package digestive-side contract, so it is byte-identical with or without the siblings on disk (`21509b67…`). The harness is a **verification layer — no new primitive, no new claim, no new `[O]`** — and the engine (`2d363033…`), disease (`a2c32ff9…`), C6 (`cbc73465…`), seam (`757a8dea…`) and analgesic (`720a4229…`) digests are all UNCHANGED, the rebuild byte-identical. To run the live cross-volume check, place the sibling archives alongside this one and run `python repro/run_harness.py` (or set `VP_SIBLING_CIRCULATORY` / `VP_SIBLING_MUSCULOSKELETAL` / `VP_SIBLING_NEURO` to their roots); with the siblings absent it skips cleanly and exits 0. Prior releases below.
> **v0.15.0 — §29 closes the in-substrate digestive Tier-1 surface by REUSE.** The five disorders the roadmap left enumerated (FUTURE_WORK §1A–§1D) are built by reusing already-validated modules / primitives, with **no new substrate primitive and no sibling package**: dyssynergic defecation (the §16 gate read at the anorectal outlet — the achalasia mirror; the bolus is retained when the outlet stays closed while the propulsive drive is intact, the gate-not-drive distinction from colonic inertia), Hirschsprung (a §4 segmental aganglionic block — absent oscillators on the §1 emergence — with proximal dilatation), MODY (a targeted partial β-secretory lesion on the §12 homeostat giving a distinct, regulated curve unlike the §12 type-1 runaway), hepatic GSD type I (a crippled §6 glycogen-buffer release giving fasting hypoglycaemia and failed counter-regulation), and autoimmune gastritis (the §22 relapsing-inflammation flare read corpus-localised, dropping the §7 barrier and acid together). The three monogenic items (Hirschsprung RET, MODY PDX1/HHEX, GSD-I G6PC) are gene-key — imported-lesion seams owned by `disease_wp` with the consequence dynamics owned here. D14 sits **above** the engine and the seam / analgesic layers import the disease layer read-only, so only the **disease** digest moves (`2e98a0d7…` → `a2c32ff9…`); the engine (`2d363033…`), C6 oncology (`cbc73465…`), seam (`757a8dea…`) and analgesic (`720a4229…`) digests are all **UNCHANGED** and the docs rebuild is **byte-identical**. Felt and absorptive magnitudes stay `[O]`. Prior releases below.
> v0.14.0 is the publication-finalisation release (no new disease module): **(1)** the DOI is baked single-source from `tools/build_docs.py` (`CONCEPT`) into every claim-strip/footer (resolvable doi.org link), `_meta.json`, `llms.txt`, and the ScholarlyArticle / CreativeWorkSeries JSON-LD identifier (v0.13.0); **(2)** three VP-SPEC v1.8 overview pages — `/about/`, `/methods/` (live γ table) and `/faq/` (FAQPage schema, 11 Q&A) — are added for Google / AI-search discoverability (v0.14.0). Both are metadata/presentation above the engine, so every digest below (engine `2d363033…`, disease `2e98a0d7…`, C6 `cbc73465…`, seam `757a8dea…`, analgesic `720a4229…`) is UNCHANGED and the docs rebuild is byte-identical.

## Research phase (writing stays locked until these are green)
```
python repro/run_all.py                          # emerge, circulate, stress battery + oncology, gate report
python repro/_engine/vp_dig_engine.py            # emergence + all dynamics digest JSON (+ sha256)
python repro/_verify/stress_tests.py             # T1–T5 + ONC + ONC2 + DZ1–DZ14 + DZS + DZA + DZD battery under WIDE sweeps
python repro/_oncology/carcinogen_dose_response.py   # carcinogen barrier-Kramers kernel + 3 site anchors + C6 extension (validate_c6, 2×sha256)
python repro/_disease/disease_modules.py         # disease modules D1–D13 (§11–§18, §22–§26) + 2×sha256 digest
python repro/_seams/seam_wiring.py               # §27 cross-system seam layer: circulatory hepatic interface consumed + mind felt-symptom firewall (architectural lock) + 2×sha256 digest
python repro/_analgesic/analgesic_logic.py       # §28 INHERITED analgesic target layer: 27 non-opioid targets re-derived on this package's §18 spinodal (drift 0) → 3 drug-class levers + 2×sha256 digest
python repro/_verify/gates.py                    # research gate + writing-lock status
```

## Sign-off → writing phase
```
python -c "import sys;sys.path.insert(0,'repro/_verify');sys.path.insert(0,'repro/_engine');sys.path.insert(0,'repro/_oncology');sys.path.insert(0,'repro/_disease');import importlib;importlib.import_module('gates').write_research_complete()"
echo writing > PHASE
python tools/build_docs.py                        # emit canonical HTML into docs/ (refuses while locked)
```

Determinism (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed; no RNG dependence (noise-free
integrations); round-before-hash; sorted JSON keys. Two engine runs yield an identical sha256, and
`tools/build_docs.py` is idempotent (byte-identical docs on re-run). Numbers shown anywhere are regenerated
by the engine — no hand-entered values. stdlib + numpy only.

## What each target shows
- **T1** gastric pacemaker = robust limit cycle (ISI CV < 3% across drive 0.40–0.70); rate anchored ~3 cpm.
- **T2** aboral gradient: one gastric clock predicts duodenum 11.1 cpm > ileum 7.5 cpm, monotone over N & drive.
- **T3** peristalsis: a phase gradient transports a bolus +12 segments aborally; reverses (−1) under control.
- **T4** glucose load → ~5 mM setpoint via a graded R19 insulin-switch population.
- **T5** hypoglycaemia → glucagon/hepatic counter-regulation, bounded (< 9 mM rebound).
- **ONC** carcinogen kernel reproduces cited RR shapes (colorectal 1.18/50 g·day, pancreatic 1.91/50 py)
  and H. pylori × diet super-additivity (joint 4.4 > additive-null 3.3); absolute incidence is [O].
- **ONC2** C6 neoplastic extension (§19–§21): a Barrett's/Correa metaplasia precursor step (precursor RR≈11/≈3.6,
  rate-limiting; the dysplasia ladder accelerates; ablation/eradication lowers the next-step rate), HCC (HBV×aflatoxin,
  joint≈22) and ESCC (smoking×alcohol, joint≈17) synergy reproduce super-additivity AND predict sub-multiplicativity,
  gastric MALT regresses on g-restore, anal SCC monotone in HPV bias; the out-of-kernel boundary (GIST/NET/small-bowel/
  cholangio) is stated; the C6 validation digest is 2×sha256-deterministic; absolute incidence + the four boundary sites are [O].
- **DZ1** gastric dysrhythmia + gastroparesis (§11): τ_s crosses the EGG band (brady<2.5 / normal~3 / tachy>3.7
  cpm); a faster *coupled* ectopic focus entrains tachygastria (≈6.4 cpm); ICC density grades emptying to ~24%
  at severe depletion, 0 with none. Mechanism [V], band [L], absolute emptying rate [O].
- **DZ2** diabetes T1/T2 (§12): on one homeostat, β-capacity loss drives accelerating hyperglycaemia past 7 mM
  (~11 mM, catastrophic); insulin-sensitivity loss settles a stable elevated setpoint (~7 mM, compensated); the
  matched-depth gap widens. Two-axis emergence [V], FPG thresholds [L], absolute prevalence [O].
- **DZ3** gastritis/peptic ulcer (§13): erosion RR rises monotone+convex on the §7 kernel (slope calibrated to
  the cited NSAID ulcer RR≈4); gastric ulcers cross by failed defence (low g), duodenal by acid excess (high h);
  chronic Hp shares the §10 cancer-step g_Hp=0.92. Shape+split+continuum [V], anchor [L], incidence [O].
- **DZ4** intestinal motility (§14): reducing propulsive drive slows transit monotonically (slow-transit
  constipation) and collapses below a threshold (colonic inertia, refractory); falling ICC density → functional
  pseudo-obstruction with a patent lumen (CIPO); a transient drive loss → reversible paralytic ileus; and ONE ICC
  lesion collapses both gastric emptying (§11) and gut transit (§14). Mechanisms [V], transit anchors [L]-pending,
  absolute transit time [O]. Each disorder also carries a model treatment-target reading.
- **DZ5** scattered Tier-1 perturbations (§15): early dumping = the same carbohydrate load delivered faster
  → a monotone-higher glucose peak, late dumping = a biphasic peak-then-reactive-hypoglycaemia crossing the
  cited 3.9 mM (the mechanical rapid-emptying magnitude is an honest [O], needing the Tier-2 reservoir/pyloric
  brake); reflux-oesophagitis erosion is monotone+convex on the shared §13 Kramers kernel; insulinoma is the
  mirror of §12 type 1 (fasting falls below 3.9 mM, recovers on source removal) with reactive hypoglycaemia
  sharing the late-dumping undershoot; functional dyspepsia is a mild point on the §11 ICC axis (distinct from
  severe gastroparesis); SIBO stasis is the retained proximal fraction rising as §4 propulsive drive falls.
  Mechanisms [V], hypo+NSAID anchors [L], dumping magnitude/nadir + SIBO bacterial load + FD felt component
  [O]. Each disorder also carries a model treatment-target reading.
- **DZ6** sphincter-gate disorders (§16, the first Tier-2 primitive): a tonically-closed R19 gate (the R19
  switch held in the closed basin; resistance = tone + spinodal, derived from R19, never fitted) gives two
  opposite diseases on ONE gate — GERD (the gate fails CLOSED: retrograde reflux burden rises monotonically
  as LES tone falls, 0→18 of 21 transient-driven events, continent→incompetent) and achalasia (the SAME
  gate fails OPEN: the relaxation drive can no longer clear the resistance, so the bolus is retained →
  antegrade stasis, with aperistalsis compounding) — the gate analogue of the §11/§14 one-ICC-lesion mirror.
  Esophageal spasm is a §4 coordination pathology (net transit collapses as coordination is lost and raising
  amplitude cannot rescue it — the jackhammer signature); sphincter of Oddi is the same gate at the biliary
  outlet (stuck-gate outflow obstruction). Motor readings [V]; felt chest pain and absolute reflux frequency /
  clearance / outflow [O]. Each disorder also carries a model treatment-target reading.
- **DZ7** gastric accommodation reservoir (§17, the second Tier-2 primitive): the same §2 R19 switch read as a
  fundic wall — vagal accommodation relaxes the contracted wall toward its yield point; wall stiffness
  `k = 3s² − g` sets compliance `C = 1/k` and a fixed-meal pressure `P = V·k`, all derived from R19, never
  fitted. Impaired accommodation stiffens the reservoir so a fixed meal raises pressure prematurely
  (functional dyspepsia, post-prandial distress / early satiation): the impaired operating point reaches
  ~91% of the maximally-stiff baseline pressure while compliance falls in lock-step, monotone across a wide
  accommodation sweep; the maximal-compliance yield point is exactly the R19 spinodal (closed-form identity,
  [F]); the treatment axis is explicit (raising the compliance term lowers the meal pressure). This is the
  accommodation half of functional dyspepsia, mechanically separable from the §15 emptying half. Pressure /
  compliance axis [V], yield identity [F]; felt post-prandial distress (→ B3 afferent gain + `mind` firewall)
  and absolute meal-volume / pressure scale (→ barostat/manometry) [O].
- **DZ8** visceral afferent gain (§18, the third Tier-2 primitive): the same R19 element read as a visceral
  afferent — its static susceptibility to a wall-distension input is the restoring-curvature inverse
  `χ = ds*/dh = 1/k = 1/(3s² − g)`, the SAME quantity the §17 reservoir reads as fundic compliance (one
  curvature, two readings), derived from R19, never fitted. IBS is two things at once: a §14 transport-bias
  motility subtype (the bias orders IBS-C retained 0.64 → IBS-M 0.30 → IBS-D 0.00, with the diarrhoea-side
  absolute magnitude pinned at the §15 conserved-bolus ceiling — honest [O]) plus a raised afferent gain.
  Visceral hypersensitivity: the gain `χ=1/k` and the fixed-distension signal rise monotonically (allodynia
  ×1.99) and past the R19 spinodal a normal distension flips the element discontinuously into spontaneous
  firing. Functional abdominal pain: the pain proxy rises at normal motility (no structural lesion). The gain
  diverges exactly at the R19 spinodal = the §17 reservoir yield (max abs diff 0.0 vs compliance; self-
  consistent vs the simulated response, rel err 1.8e-4). Subtype ordering + hypersensitivity gain/allodynia
  [V], gain=compliance identity + divergence-at-spinodal [F]; felt pain (→ `mind` firewall) and absolute
  rapid-transit magnitude / stool frequency (→ §15 ceiling) [O]. Carries a model treatment-target reading.
- **DZ9** immune relapsing-inflammation (§22, the first Tier-3 primitive): a relapsing mucosal inflammation is
  the §2 R19 switch with a SELF-SUSTAINING flare basin (`flare_state`/`inflammatory_barrier_scale`, derived
  from R19, never fitted). IBD shows relapsing-remitting HYSTERESIS (the flip-to-flare drive exceeds the
  return-to-remission drive — a flare persists as the trigger recedes), forcing the induction-vs-maintenance
  dose ASYMMETRY (induction past antigen+spinodal ≈ 0.885, maintenance ≈ 0.115 — the same mid-dose holds
  remission but cannot break a flare). The cumulative-burden bridge lowers the SAME §7 barrier the §10 kernel
  uses for H. pylori, so colitis-associated colorectal-cancer RR rises monotonically to the cited UC anchor
  (RR≈2.4, Jess 2012) and collapses to 1.0 on sustained remission — closing the §21 small-bowel-adenocarcinoma
  boundary on the inflammation route. Celiac (and microscopic / eosinophilic / autoimmune) is the
  antigen-dependent regime (driver removal → remission, barrier/villous recovery). Hysteresis + asymmetry +
  burden→barrier→cancer continuity [V], spinodal thresholds [F], colitis-CRC anchor [L]; absolute incidence,
  celiac absorptive magnitude (→ absorption layer), felt component (→ `mind` firewall) [O]. Carries a model
  treatment-target reading.
- **DZ10** exocrine autodigestion (§23, the second Tier-3 primitive): the pancreatic zymogen cascade is the §2
  R19 switch with an AUTOCATALYTIC self-amplification term (active trypsin activates trypsinogen) —
  `autoactivation_threshold`/`autodigestion_latched`, derived from R19, never fitted. The autoactivation
  threshold rises with the protective inhibitor (SPINK1 ↑; PRSS1-gain / SPINK1-loss ↓); a sub-threshold
  trigger decays safely but a supra-threshold trigger LATCHES (the +g·s term self-sustains with the trigger
  removed) — irreversible to any parameter move, so intervention is PRE-threshold only (only a strong inhibitor
  past the spinodal abolishes the basin). Chronic mirror: a large secretory reserve delays EPI/steatorrhea
  until ~90% acinar loss (DiMagno 1973), adequacy monotone in residual capacity, and PERT restores output above
  the digestive demand. Threshold-rises-with-inhibitor + irreversible latch (pre-threshold-only) +
  strong-inhibitor reversibility + large-reserve EPI + PERT rescue [V], the latch a forced R19 hysteresis [F],
  the >90%-loss reserve threshold [L]; absolute trigger/inhibitor + demand scales and established-disease
  outcomes (necrosis, organ failure) [O]; CFTR gene-key → `disease_wp`. Carries a model treatment-target reading.
- **DZ11** perfusion-viability (§24, the third Tier-3 primitive): a perfused tissue is the §2 R19 switch resting
  in the VIABLE basin with bias `h = perfusion − demand` — `perfusion_threshold`/`viability_margin`/`tissue_viable`,
  derived from R19, never fitted. Chronic mesenteric ischaemia (intestinal angina): the viability margin above the
  rescue threshold falls as post-prandial demand rises and crosses to deficit (revascularisation restores a positive
  margin). Acute mesenteric ischaemia / ischaemic colitis: a sudden occlusion FLIPS viable→ischaemic past
  `demand − spinodal`, and reperfusion recovers the tissue only WITHIN the salvage window (`= 2·spinodal` — partial /
  late reperfusion stays infarcted). NAFLD/MASLD reuses the §12 type-2 gain-loss homeostat unchanged; the hepatic
  lipid-deposition layer is a declared `circulatory` seam. Demand-driven margin collapse + revascularisation rescue +
  forced occlusion flip + time-critical salvage window + §12 reuse [V], the ischaemic-flip and rescue thresholds
  exact spinodal identities [F]; absolute perfusion/demand scales, structural infarction, and the `circulatory` lipid
  layer [O]. Carries a model treatment-target reading.
- **DZ12** hepatobiliary/bile (§25, the fourth Tier-3 primitive): cholesterol-bile crystallisation is the §2 R19
  switch with the dissolved phase as the rest basin and the cholesterol saturation index (CSI) as the bias —
  `nucleation_barrier`/`supersaturation_drive`/`stone_nucleates`, derived from R19, never fitted. Supersaturation
  (CSI>1) is METASTABLE not sufficient — a stone nucleates only past `CSI > 1 + spinodal` (the Kramers crossing) —
  and a formed stone then shows dissolution HYSTERESIS, persisting below saturation and redissolving only far below
  it (which is exactly why UDCA dissolution works only on small, early, near-saturation stones). Gallbladder stasis =
  the §16 B1 sphincter-gate seam, cholecystitis = the B1 gate + the cited §22 C1 flare, biliary dyskinesia = the B1
  gate, the nucleation time = the §7 Kramers rate. Metastable supersaturation + barrier-gated nucleation + dissolution
  hysteresis [V], the nucleation and dissolution thresholds exact spinodal identities and the nucleation time the
  Kramers rate [F]; absolute CSI scale, the B1/C1 stasis/flare seams, and the `circulatory`/`mind` seams [O]. Carries
  a model treatment-target reading.
- **DZ13** structural/wall (§26, the fifth Tier-3 primitive): the colonic wall is the §2 R19 element resting intact
  (s=−√g) driven by the segmental Laplace pressure `P = tension / radius` — `laplace_pressure`/`herniation_threshold`/
  `wall_herniates`, derived from R19, never fitted. By `P = tension/radius` a low-fibre diet (small hard stools, strong
  segmenting contractions) raises the wall pressure as the radius falls, and once `P > spinodal(g_wall)` the intact
  wall HERNIATES into a diverticulum; a weaker wall (aging connective tissue, Ehlers–Danlos/Marfan collagen) has a
  lower threshold and herniates at a fixed pressure a normal wall withstands. Treatment is the geometry in reverse:
  fibre bulks the stool (larger radius) and softens segmenting (lower tension), dropping P below threshold.
  DiverticulITIS = the cited §22 C1 flare; the mechanical fixed-block obstructions (hernia incl. hiatal, volvulus,
  intussusception, adhesions) = the §14 functional-module structural counterpart (surgical, out-of-model). Laplace
  pressure rising as radius falls + discontinuous herniation + lower threshold of a weaker wall + fibre treatment [V],
  the herniation threshold an exact spinodal identity [F]; absolute pressure/strength scales, the §22 C1 diverticulitis
  seam, and the §14 obstruction counterpart [O]. Carries a model treatment-target reading.
- **DZ14** remaining in-substrate Tier-1 surface (§29, REUSE — no new primitive, no sibling package): the five disorders FUTURE_WORK §1A–§1D left enumerated are closed by reuse — dyssynergic defecation = the §16 gate read at the anorectal outlet (the achalasia mirror; the bolus is retained when the outlet stays closed while the propulsive drive is intact — gate, not drive, the falsifiable distinction from colonic inertia); Hirschsprung = a §1 emergence + §4 transport segmental aganglionic block (absent oscillators block aboral transit progressively, never traverse the deep aganglionic zone, retain the bolus proximal at the transition zone = proximal dilatation; RET gene-key → `disease_wp`); MODY = a targeted partial β-secretory lesion on the §12 homeostat (a distinct, stable, regulated elevated curve unlike the §12 type-1 catastrophic runaway; PDX1/HHEX gene-key → `disease_wp`); hepatic GSD type I = a crippled §6 hepatic glycogen-buffer release (fasting glucose drifts hypoglycaemic + the counter-regulation can no longer return to setpoint; G6PC gene-key → `disease_wp`); autoimmune gastritis = the §22 relapsing-inflammation flare read corpus-localised + the §7 barrier (a regional barrier lesion + an acid-output drop coupled to it, driver suppression recovering both) [V] every emergent mechanism / [L] the PDX1/HHEX and G6PC gene links / [O] felt straining (→ `mind`), absolute scales, the B12/iron malabsorption magnitude (absorption layer), the carcinoid boundary (`disease_wp`). Carries a model treatment-target reading.
- **DZS** cross-system seam wiring (§27, the v0.11.0 seam layer; the engine + disease digests stay UNCHANGED): the
  circulatory hepatic interface — Q_H=1500 mL/min, E=0.75, F=0.25, CL_H=1125 mL/min, circulatory the SSOT owner by
  its CHARTER ‘Seams OUT’ — is recorded once in `inherited/cross_references.json` (verified against circulatory’s
  `hepatic_clearance()` at vendoring) and CONSUMED, with no sibling code import, as the delivery substrate the §24
  NAFLD/MASLD lipid load (insulin-resistance core reusing the §12 type-2 homeostat) and the §25 biliary cholesterol
  (nucleation thermodynamics, CSI=1.385) sit on; both readings consume the identical snapshot (SSOT-consistent). The
  `mind` felt-symptom seam (visceral pain §18, biliary colic §25) is a one-way forward-defer POINTER carrying no
  consumed value (→ mind’s M18 interoception route, Saper 2002). The FIREWALL is enforced by an architectural lock —
  zero circulatory/mind/neuro code imports across every package python file, and a metabolic state with no felt/HPA
  key — the SAME lock mind runs neuro-side (adversarially tested: it catches a planted sibling import). [V] the
  consumed circulatory interface (cited DOI 10.5281/zenodo.20754354 + named function) + the §12-homeostat reuse and
  nucleation thermodynamics resting on it / [F] the firewall + the mind one-way pointer / [O] the lipid-handling and
  absolute cholesterol-delivery magnitude (circulatory’s) and the felt pain/affect (mind’s, DOI 10.5281/zenodo.20694404).
- **DZA** INHERITED analgesic target logic (§28, the v0.12.0 analgesic layer; the engine + disease + oncology digests stay
  UNCHANGED): the sibling whitepaper `analgesic_threshold_logic` v2.0 (concept DOI 10.5281/zenodo.20733420, CC BY 4.0) is
  vendored into `inherited/analgesic_targets.json` and applied via `repro/_analgesic/analgesic_logic.py`. Each pain gene’s
  promoter γ = −mean(NN stacking ΔG, SantaLucia 1998) is placed on the R19 firing-threshold scale |h_sp| = spinodal(γ) =
  2(g/3)^1.5 — BYTE-IDENTICAL to this package’s own `inherited/vp_substrate.spinodal`, the SAME spinodal the §18 visceral-
  afferent gain χ = 1/k diverges at — so re-deriving all 27 non-opioid target reads through the local substrate reproduces
  the inherited firing thresholds at drift exactly 0. The 27 sort into three drug-class levers (L1 reduce the inward current
  Na_V/Ca_V/ASIC/P2X/TRP, L2 open the K_V7 brake, L3 remove the NGF/CGRP drive), each RAISING the §18 firing threshold /
  lowering the gain back to baseline — a cited drug-class POINTER for IBS hypersensitivity (§18), functional abdominal pain
  (§18), functional-dyspepsia pain (§17), biliary colic (§25) and oesophageal-spasm pain (§16); the GI burden prioritisation
  (declared weights, γ never folded into the score) surfaces Na_V1.8 → NGF → Na_V1.7; a precision visceral-LA map pairs the
  four gut nociceptor entry ports with a charged threshold-raiser. FIREWALL inherited verbatim — γ reads promoter STRUCTURE
  only (never a voltage/potency/dose/in-vivo-selectivity/effect), so [V] each lever lowers the §18 gain + the burden re-
  derivation / [F] the drift-0 inheritance (analgesic scale = §18 spinodal), the three-lever identity, the declared-weight
  prioritisation, the precision-block mechanism shape / [O] every clinical magnitude (potency, dose, in-vivo selectivity,
  differential-block ratio, efficacy) and the felt pain (mind’s, DOI 10.5281/zenodo.20694404); δ is structural, not a dose.
  Carries a model treatment-target reading. Imports only the shared substrate + the disease modules, so the firewall holds
  and the analgesic layer is itself 2×sha256 deterministic (own digest, distinct from the engine/disease/oncology digests).
- **DZD** the whole disease layer digest is 2×sha256 identical across runs (deterministic) [V].
