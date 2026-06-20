# NEXT_INSTRUCTIONS — digestive_vp_site handoff (remaining disease program)

**Read order for a fresh window:** `START_HERE.md` → `CHARTER.md` → this file. This file is the
disease-by-disease work order for everything not yet built. It enriches `FUTURE_WORK.md` (the roadmap)
with, for **every remaining disease**: the ownership ruling (mine vs `disease_wp`), the VP-native
mechanism (which parameter moves), the discriminant target, the **treatment-target reading** (which
parameter an effective therapy moves and in which direction — a mechanistic prediction; absolute
efficacy is always `[O]`), the grade, and the substrate extension required.

Per the user's standing instruction, the deliverable is a single zip and the remaining program ships
with it (this file). Build research-first, one module at a time, each gated by its discriminant under
wide sweeps; new primitives go into the substrate single-source (never fitted); every `[O]` carries a
stated obstacle in `IRREPRODUCIBILITY_LEDGER.md`.

---

## 0. State of play (built, v0.16.0)

> **v0.16.0 = §30 builds the live cross-package harness (the last frontier item, OUT OF GATE):** a runner loads THIS volume together with its sibling VP volumes (circulatory, musculoskeletal, neuro) in ONE process and confirms, against the LIVE sibling engines, the cross-volume identities the §27 seam and §28 analgesic layers had to take on trust — the shared R19 substrate (spinodal |h_sp| = 2(g/3)^1.5 and barrier g²/4 byte-identical, cross-volume drift 0), circulatory's live `hepatic_clearance()` reproducing the vendored snapshot (Q_H=1500 mL/min, E=0.75, F=0.25, CL_H=1125 mL/min), the inherited 27-target analgesic map re-deriving through every volume's own spinodal (drift 0, musculoskeletal the built second host), and the neuro nociceptor the §18→`mind` one-way pointer targets (Na_V1.7/SCN9A, master PRDM12 — the §28 L1 channel). The harness runs **outside every gate**: the research gate (`repro/run_all.py`) and the canonical build compute nothing in it and never import a sibling, so each volume re-establishes its trusted state from its own archive with the siblings **absent** (verify-alone); the sibling engines are **loaded by file path, not imported** (zero sibling import statements in the harness, self-checked); and the harness digest hashes only the in-package digestive-side contract, so it is byte-identical with or without the siblings on disk (`21509b67…`). It is a verification layer — **no new primitive, no new claim, no new `[O]`** — and the engine (`2d363033…`) / disease (`a2c32ff9…`) / C6 (`cbc73465…`) / seam (`757a8dea…`) / analgesic (`720a4229…`) digests are all UNCHANGED, the rebuild byte-identical, the research gate all-green. Live check: `python repro/run_harness.py` with the siblings present (5 checks PASS).
>
> **v0.15.0 = §29 closes the in-substrate digestive Tier-1 surface by REUSE (no new primitive, no sibling package):** dyssynergic defecation (the §16 gate at the anorectal outlet), Hirschsprung (a §4 segmental aganglionic block), MODY (a targeted §12 secretory lesion), hepatic GSD type I (a crippled §6 glycogen-buffer release) and autoimmune gastritis (the §22 flare corpus-localised) — the three monogenic items gene-key → `disease_wp`. D14 sits above the engine, so only the disease digest moves (`2e98a0d7…`→`a2c32ff9…`, now D1–D14); the engine / C6 / seam / analgesic digests are UNCHANGED, the rebuild is byte-identical, and the research gate stays all-green.
>
> **v0.14.0 = publication-finalisation release (no new disease module).** Two presentation-layer steps,
> both above the engine. **(1) DOI minted (v0.13.0):** the confirmed Zenodo concept DOI
> `10.5281/zenodo.20755319` (version-independent) is baked single-source from `tools/build_docs.py` (the
> `CONCEPT` constant) into every canonical artifact — each claim-strip and footer renders it as a resolvable
> doi.org link, `_meta.json` / `llms.txt` carry it, and the ScholarlyArticle / CreativeWorkSeries JSON-LD emit
> a machine-readable identifier (PropertyValue propertyID=DOI + sameAs). **(2) Discoverability front-matter
> (v0.14.0):** three overview pages were added under the full VP-SPEC v1.8 canonical scaffolding — `/about/`
> (the scale of the work, the DNA-grounded emergence, the full 29-section scope, reproducibility + honest
> grading), `/methods/` (master-gene promoter → γ = −mean NN stacking ΔG (SantaLucia 1998) → R19 jamming
> switch, with a live γ table), and `/faq/` (an FAQPage-schema page of 11 Q&A for Google rich-results / AI
> ingestion) — framing this as a grounded, deterministic, DNA-emergent model rather than a toy, and competing
> on open search discoverability. `BUILD_DATE` / `datePublished` / sitemap `lastmod` are the 2026-06-19 mint
> date. The engine / disease / C6 / seam / analgesic digests are all UNCHANGED, the rebuild is byte-identical,
> and the research gate stays all-green. The §29 in-substrate closure and the §30 live cross-package harness (above) are now built
> (v0.15.0, v0.16.0); the remaining program (cross-package analgesic propagation to the `circulatory` / `neuro` sibling packages —
> musculoskeletal already carries it) is what is left.

Mechanism **and** treatment are documented for the **fourteen** built disease sections (plus the C6 neoplastic extension §19–§21):

- **§11** gastric dysrhythmia + gastroparesis (perturbs §2/§3) — [V]/[L]/[O]
- **§12** diabetes type 1 / type 2 spectrum (perturbs §5/§6) — [V]/[L]/[O]
- **§13** gastritis + peptic ulcer (reuses §7/§10 barrier kernel) — [V]/[L]/[O]
- **§14** intestinal motility / transit disorders (perturbs §4) — [V]/[L]-pending/[O]
- **§15** scattered Tier-1 perturbations — dumping, reflux-erosion, insulinoma/reactive-hypo, FD-motility,
  SIBO-stasis (**Group A**, no new primitive; shipped v0.4.0) — [V]/[L]/[O]
- **§16** sphincter-gate disorders — GERD, achalasia, esophageal spasm, sphincter of Oddi, on the **first
  Tier-2 primitive** (a tonically-closed R19 gate `gate_open`, added single-source to
  `inherited/vp_substrate.py`; GERD↔achalasia = one gate, two opposite failures; **Group B / B1**, shipped
  v0.5.0) — [V]/[O]
- **§17** gastric accommodation reservoir — functional dyspepsia, post-prandial distress / early satiation,
  on the **second Tier-2 primitive** (the same §2 R19 switch read as a fundic wall; `wall_stiffness` /
  `reservoir_compliance` / `meal_pressure` added single-source to `inherited/vp_substrate.py`; stiffness
  `k = 3s² − g`, compliance `C = 1/k`, impaired accommodation → premature meal pressure; maximal-compliance
  yield point = R19 spinodal, exact [F]; **Group B / B2**, shipped v0.6.0) — [V]/[F]/[O]
- **§18** visceral afferent-gain disorders — IBS-C/-D/-M + functional abdominal pain, on the **third
  Tier-2 primitive** (the same R19 element read as a visceral afferent; `afferent_gain` / `afferent_signal`
  added single-source to `inherited/vp_substrate.py`; susceptibility `χ = 1/k = 1/(3s² − g)` — the SAME
  curvature inverse §17 reads as fundic compliance; IBS = a §14 transport-bias motility subtype (orders
  IBS-C → IBS-M → IBS-D by retained fraction) + a raised afferent gain (visceral hypersensitivity: gain
  rise, allodynia, spontaneous firing past the spinodal); functional abdominal pain = raised gain at
  normal motility; the gain diverges at the R19 spinodal = the §17 reservoir yield; felt pain → `mind`
  (firewall); **Group B / B3**, shipped v0.7.0) — [V]/[F]/[O]
- **§22** immune relapsing-inflammation — IBD (relapse hysteresis + induction≠maintenance asymmetry +
  colitis→barrier→cancer bridge to the cited UC anchor, closing the §21 small-bowel boundary), celiac in the
  antigen-dependent regime, on the **first Tier-3 primitive** (`flare_state` / `flare_burden` /
  `inflammatory_barrier_scale`; **Group C / C1**, shipped v0.9.0) — [V]/[F]/[L]/[O]
- **§23** exocrine autodigestion — acute pancreatitis (autocatalytic latch, pre-threshold-only) + large-reserve
  EPI / PERT, on the **second Tier-3 primitive** (`autoactivation_threshold` / `autodigestion_latched`; CFTR
  gene-key → `disease_wp`; **Group C / C2**, shipped v0.9.0) — [V]/[F]/[L]/[O]
- **§24** perfusion / vascular — mesenteric ischaemia (demand-driven margin collapse + acute occlusion flip with
  a time-critical salvage window) + ischaemic colitis + NAFLD/MASLD (reuses §12; lipid layer a `circulatory`
  seam), on the **third Tier-3 primitive** (`perfusion_threshold` / `viability_margin` / `tissue_viable`;
  **Group C / C3**, shipped v0.10.0) — [V]/[F]/[O]
- **§25** hepatobiliary / bile — cholelithiasis (metastable supersaturation + barrier-gated nucleation +
  dissolution hysteresis), stasis / cholecystitis cited to the §16 B1 gate and §22 C1 flare, on the **fourth
  Tier-3 primitive** (`nucleation_barrier` / `supersaturation_drive` / `stone_nucleates`; **Group C / C4**,
  shipped v0.10.0) — [V]/[F]/[O]
- **§26** structural / mechanical — diverticular disease (Laplace herniation past P = tension/radius, weaker-wall
  lower threshold, fibre treatment the geometry in reverse), diverticulitis = §22 C1 flare, mechanical fixed-block
  obstruction = the §14 functional-module counterpart, on the **fifth Tier-3 primitive** (`laplace_pressure` /
  `herniation_threshold` / `wall_herniates`; **Group C / C5**, shipped v0.10.0) — [V]/[F]/[O]
- **§27** cross-system seam wiring — the circulatory hepatic interface (Q_H=1500 mL/min, E=0.75, F=0.25; circulatory
  the SSOT owner) consumed as the §24 NAFLD/MASLD and §25 bile-delivery substrate, and the mind felt-symptom seam
  (visceral pain §18, biliary colic §25) a one-way forward-defer pointer; firewall enforced by an architectural lock
  (zero sibling imports; a metabolic state with no felt/HPA key). Citation/pointer-only, never a sibling code import
  (own seam layer `repro/_seams/seam_wiring.py`, 2×sha256; **shipped v0.11.0**) — [V]/[O]
- **§28** **INHERITED analgesic target logic for visceral pain** — *this layer was NOT in the roadmap; it was inherited
  on request and is now built and continuously applied.* Vendors the sibling whitepaper `analgesic_threshold_logic`
  v2.0 (concept DOI 10.5281/zenodo.20733420, version DOI …20733421; CC BY 4.0) as `inherited/analgesic_targets.json`
  and applies it via `repro/_analgesic/analgesic_logic.py`: each pain gene's promoter `γ = −mean(NN stacking ΔG,
  SantaLucia 1998)` is placed on the R19 firing-threshold scale `|h_sp| = spinodal(γ) = 2(g/3)^1.5`, **byte-identical
  to this package's own `vp_substrate.spinodal`** (= the §18 afferent spinodal) — so all 27 non-opioid target reads
  re-derive through the local substrate at **drift exactly 0**. The 27 sort into three drug-class levers (L1 reduce
  the inward current Na_V/Ca_V/ASIC/P2X/TRP, L2 open the K_V7 brake, L3 remove the NGF/CGRP drive), each **raising
  the §18 firing threshold / lowering the §18 gain `χ=1/k` back to baseline** — a *cited drug-class pointer* for IBS
  hypersensitivity (§18), functional abdominal pain (§18), functional-dyspepsia pain (§17), biliary colic (§25),
  oesophageal-spasm pain (§16). Firewall **inherited verbatim**: `γ` reads promoter STRUCTURE only (never a voltage /
  potency / dose / in-vivo selectivity / clinical effect); every clinical magnitude + the *felt* pain are `[O]` /
  `mind`; `δ` is structural, not a dose; nothing prescribes. Own application layer (2×sha256 `720a4229…`), dedicated
  stress suite **DZA**; the engine / disease / oncology digests are **unchanged** by the integration (**Group D /
  inherited**, shipped v0.12.0) — [V]/[F]/[O]
- **§29** **Remaining in-substrate Tier-1 surface CLOSED by REUSE** (no new primitive, no sibling package) — the five disorders FUTURE_WORK §1A–§1D left enumerated, built by reuse: dyssynergic defecation (the §16 gate read at the anorectal outlet — the bolus retained when the outlet stays closed while propulsion is intact, the gate-not-drive distinction from colonic inertia §14), Hirschsprung (a §1 emergence + §4 segmental aganglionic block — absent oscillators block aboral transit progressively, never traverse the deep zone, retain the bolus proximal = proximal dilatation; RET gene-key → `disease_wp`), MODY (a targeted partial β-secretory lesion on the §12 homeostat — a distinct, stable, regulated curve unlike the §12 type-1 runaway; PDX1/HHEX gene-key → `disease_wp`), hepatic GSD type I (a crippled §6 hepatic glycogen-buffer release — fasting hypoglycaemia + failed counter-regulation; G6PC gene-key → `disease_wp`), and autoimmune gastritis (the §22 relapsing-inflammation flare read corpus-localised + the §7 barrier — a regional barrier lesion + an acid-output drop coupled to it, driver suppression recovering both). Every phenotype emerges under wide sweeps; dedicated stress suite **DZ14**; the three monogenic items are imported-lesion seams owned by `disease_wp` with the consequence dynamics owned here; felt and absorptive magnitudes are `[O]`. Only the disease digest moves (`2e98a0d7…`→`a2c32ff9…`); engine / C6 / seam / analgesic unchanged (**shipped v0.15.0**) — [V]/[L]/[O]
- **§30** **Live cross-package harness — OUT OF GATE** (a verification layer; no new primitive, no new claim, no new `[O]`) — a runner that loads THIS volume together with its sibling VP volumes (circulatory, musculoskeletal, neuro) in ONE process and confirms, against the LIVE sibling engines, the four cross-volume identities the §27 seam and §28 analgesic layers had taken on trust: (1) the **shared R19 substrate** — every volume's firing-threshold spinodal |h_sp| = 2(g/3)^1.5 and barrier g²/4 byte-identical (cross-volume drift 0); (2) the **circulatory hepatic seam** — circulatory's live `hepatic_clearance()` reproducing the vendored snapshot (Q_H=1500 mL/min, E=0.75, F=0.25, CL_H=1125 mL/min); (3) the **inherited 27-target analgesic map** re-deriving bit-for-bit through every volume's own spinodal (drift 0), musculoskeletal the built second host reading its levers on the same spinodal; (4) the **neuro felt-symptom endpoint** — the peripheral nociceptor the §18→`mind` one-way pointer targets (Na_V1.7/SCN9A, master PRDM12 — the §28 L1 channel), a HIGH-threshold polymodal cell on the shared substrate. Runs outside every gate: the research gate and the canonical build compute nothing here and never import a sibling — verify-alone preserved (each volume re-establishes its trusted state from its own archive with the siblings absent), the engines loaded by file path not imported (zero sibling import statements, self-checked), the harness digest hashing only the in-package contract so it is byte-identical with or without the siblings on disk (`21509b67…`). Engine / disease / C6 / seam / analgesic digests all unchanged. Build sibling-free; live check `python repro/run_harness.py` with siblings present (5 checks PASS) (**shipped v0.16.0**) — [V]/[F]

Engine fingerprint `circulate()` sha256 `2d363033…` (**unchanged** across all disease + primitive + seam + inherited-analgesic work — the
disease layer, the new primitives, the seam layer and the inherited analgesic layer are consumed *above* the engine, never inside it). Disease layer
digest sha256 `a2c32ff9f1af…` (D1–D14; the §27 seam and §28 analgesic layers import the disease layer read-only and are **unchanged** by D14 — both import the disease layer read-only), 2×sha256
deterministic. The C6 oncology extension adds `validate_c6` / `c6_digest` (C6 digest sha256 `cbc73465…`, 2×sha256, **unchanged**). The §27 seam
layer carries its own digest `repro/_seams/seam_wiring.py` 2×sha256 `757a8dea…` (this moved from the pre-§28 value `ecce55ce…` for one architectural
reason only: the seam firewall scans every package `.py`, now counts 11 files (was 10), found the new analgesic file, and re-confirmed **0 sibling
imports** — the firewall holds and the new layer sits inside it). The §28 analgesic layer carries its own digest `repro/_analgesic/analgesic_logic.py`
2×sha256 `720a4229…`. Battery: T1–T5 + ONC + **ONC2** + **DZ1–DZ14** + DZD + **the §27 seam suite** + **DZA (analgesic)** all PASS; **28 sections**
built (§19–§21 = C6 neoplastic extension; §27 = seam wiring; §28 = inherited analgesic target logic). Unifying hypotheses: **#1 (one ICC lesion) demonstrated** (§11+§14), joined
by the **GERD↔achalasia one-gate mirror** (§16); **#2 (barrier-scale continuum) DEMONSTRATED** — shown along
gastritis→ulcer→first-cancer-step in §13 and now extended across **metaplasia→carcinoma (Barrett's, Correa),
inflammation×bias and bias×bias synergy (HCC, ESCC), and reversible barrier-scale reduction (H. pylori MALT) in
§19–§21** — the barrier-scale continuum now spans gastritis → ulcer → metaplasia → carcinoma across organs;
#3 (homeostat capacity/gain) shown across IGT→T2→T1 in §12. Functional dyspepsia is split into its two mechanical
halves — the §15 emptying axis and the §17 accommodation axis. A new identity is added by §28: **the analgesic firing-threshold scale `|h_sp| =
spinodal(γ)` IS the §18 visceral-afferent spinodal** — one R19 spinodal read by the §17 reservoir as maximal compliance, by §18 as the gain
divergence, and by §28 as the firing threshold the three drug-class levers raise. The engine `circulate()` emitted-result sha256 `2d363033…` is **unchanged**.

---

## 1. The build recipe (the pattern that produced D1–D4 — follow it verbatim)

1. **Probe the substrate first** (a throwaway script): find the one parameter whose sweep produces the
   phenotype *monotonically and robustly*, with the disease as an emergent regime — never tune to a
   target. Watch for the saturation trap (measure a *rate* in a fixed short window, not a completed
   process).
2. **Implement** in `repro/_disease/disease_modules.py`: a generalised function on the validated module,
   plus per-disease readers, each returning a `treatment` key (the model's target reading). `lru_cache`
   the `validate_dN()`. Add it to `validate()` and `status()`.
3. **Gate it**: add a `dzN_*` suite in `repro/_verify/stress_tests.py` and append to `SUITES`; add a line
   to `repro/run_all.py` section [5]. The writing gate auto-covers it.
4. **Write the section** in `tools/build_docs.py`: a `body_*` function pulling live numbers (incl. a
   **Treatment (model reading)** paragraph), a `SECTIONS` dict entry (answer-first **40–60 words**,
   abstract, `knows`, `desc`, grade), and 1 data table. Remove the built items from `ROADMAP_GROUPS`;
   update `headline_results`, the hub note/intro, and `llms.txt`.
5. **Narrative docs**: `FUTURE_WORK.md` (move to Built table + ✅ rows), `IRREPRODUCIBILITY_LEDGER.md`
   (new `[O]` + falsifiable predictions), `CHARTER.md`/`START_HERE.md`/`REPRODUCE.md` (DZ line, version),
   bump `VERSION`.
6. **Sign off + build + verify**: `gates.write_research_complete()` → `echo writing > PHASE` →
   `python tools/build_docs.py`; confirm engine sha unchanged, audit clean, idempotent (byte-identical
   rebuild), and fresh-extract validation (run_all green + docs byte-identical).
7. **Package** one consolidated zip to `/mnt/user-data/outputs/`, rooted at `digestive_vp_site/`.

---

## 2. Ownership filter (which digestive diseases are MINE)

From the MASTER MAP §6 contract: split by **etiology**, not body part. The digestive machine package owns
**acquired / multifactorial / common, dynamics-key** disease. `disease_wp` owns **single-gene / rare /
hereditary** disease (gene-key). Tie-breaks: a common acquired disease with a monogenic subtype → I own
"common + dynamics", `disease_wp` owns the named gene subtype (bidirectional cross-ref); carcinogen
cancers → me; hereditary cancer syndromes → `disease_wp`. New primitives I add (sphincter gate,
accommodation reservoir, afferent-gain term, immune/exocrine/perfusion/lipid/wall layers) belong to this
package and must be vendored single-source into `inherited/vp_substrate.py`.

---

## 3. Remaining work — group A: scattered Tier-1 (NEXT; fully in-substrate, no new primitive)

These reuse already-validated modules and should be built first (same effort class as D1–D4). Suggested
packaging: one module **D5** (a few §sections, or one combined "additional Tier-1 perturbations"
section). All are MINE.

| disease | owner | module reused | mechanism (parameter moved) | discriminant | treatment-target (model) | grade |
|---|---|---|---|---|---|---|
| **Dumping syndrome** | me | §2/§4 | emptying gate too open / flux gain ↑ → too-rapid emptying & transit (the *mirror* of §11 gastroparesis and §14 slow-transit) | emptying/transit *rate rises* monotonically as the gate/flux gain rises, overshooting normal | slow the gate: dietary modification + agents that *reduce* emptying/flux gain (the inverse target of prokinetics); the model predicts the same knob, opposite sign | [V] mech / [L] anchor / [O] abs |
| **Reflux esophagitis** (mucosal-injury part) | me | §7 kernel | acid-exposure as a sustained bias `h` lowers the esophageal mucosal barrier → erosion crossing (identical kernel to §13) | erosion RR rises convexly with acid-exposure *time/dose* (reuse the §13 erosion curve on an esophageal barrier) | lower `h`: acid suppression (PPI) moves back down the convex curve; (the reflux *source* needs the Tier-2 sphincter gate — cross-ref group B) | [V] mech / [L] anchor / [O] abs |
| **Insulinoma / reactive hypoglycemia** | me | §5/§6 | an autonomous insulin source (un-regulated secretion term) → glucose *undershoots* setpoint (the mirror of §12 type-1 capacity loss) | persistent low glucose emerges from an unregulated insulin drive; nadir deepens with the autonomous term | remove/limit the autonomous source (resection of an insulinoma; for reactive hypoglycemia, blunt the post-prandial insulin spike); model: cap the unregulated secretion term | [V] mech / [L] setpoint / [O] abs |
| **Functional dyspepsia (motility component)** | me | §2 (+§11) | weakened gastric slow-wave + delayed emptying (a mild §11 lesion) | delayed-emptying component reproduces at mild pacemaker/amplitude reduction; symptom mapping deferred | prokinetics raise the effective contraction (as §11); the postprandial-distress part needs the Tier-2 accommodation reservoir (group B) | [V] partial / [O] felt |
| **SIBO (motility part)** | me | §4 (+ small periodic element) | loss of the periodic housekeeping sweep (MMC) → stasis → overgrowth proxy. The motility part (stasis from absent periodic high-amplitude sweeps) is near-Tier-1; the bacterial load is `[O]` | a stasis metric (retained fraction) rises when periodic strong-coupling sweeps are removed | restore the sweep: prokinetics / motilin-class agents that reinstate periodic propulsion; bacterial load reduction is out-of-model | [V] motility / [O] bacterial load |

Note SIBO needs a small periodic-sweep element; if you keep strictly to "no new primitive", defer the
MMC sweep to group B and ship only the stasis-from-low-drive reading here.

---

## 4. Remaining work — group B: Tier-2 (ONE new small primitive each)

Add the primitive to `inherited/vp_substrate.py` single-source (derive its form from the R19/FHN
substrate; do not fit). All MINE.

### B1. Sphincter / valve control-loop (new: a tonic-relaxation gate element)
A gate is a tonically-closed element that opens on a coordinated relaxation signal; model it as an R19
element biased to the closed basin that the passing slow-wave transiently flips, gating §4 transport.

| disease | mechanism | discriminant | treatment-target (model) | grade |
|---|---|---|---|---|
| **GERD (LES incompetence)** | gate tone ↓ → retrograde transport when the gate fails against the gradient | net oral (retrograde) flux emerges when the LES gate opens against the gradient | raise gate tone / lower intra-gastric drive; reduce reflux events (the esophagitis *consequence* is §13/reflux-erosion) | [V] |
| **Achalasia** | LES fails to relax + aperistalsis | distal gate stuck closed + loss of coordinated propagation → stasis/dilatation | open the stuck gate (pneumatic dilation / myotomy / botulinum to the gate); model: force the gate-open transition | [V] |
| **Esophageal spasm / jackhammer / nutcracker** | uncoordinated or excessive contraction amplitude | loss of orderly phase wave / amplitude blow-up emerges (a §4 coupling pathology + gate) | reduce contraction amplitude / restore coordination (smooth-muscle relaxants); model: lower amplitude or restore phase order | [V] |
| **Sphincter of Oddi dysfunction** | biliary/pancreatic outlet gate dysregulation | outflow-obstruction proxy from a stuck gate | relax/ablate the gate (sphincterotomy); model: restore gate-open transition (biliary seam noted) | [V] |

### B2. Gastric accommodation reservoir (new: a compliance/volume element)
A fundic compliance that absorbs meal volume without a pressure spike.

| disease | mechanism | discriminant | treatment-target (model) | grade |
|---|---|---|---|---|
| **Functional dyspepsia (postprandial distress)** | impaired fundic accommodation → premature pressure rise, early satiation | reservoir compliance ↓ ⇒ premature pressure rise on a fixed meal | restore accommodation (fundic-relaxing agents); model: raise the compliance term | [V] partial (+ afferent gain for symptoms) |

### B3. Visceral afferent gain (new: an afferent-gain term; SEAM to /neuro/, /mind/ — firewall kept)
A peripheral gain on the visceral afferent signal. Felt/affective interpretation stays in `mind` (do not
re-emerge HPA or felt experience here — peripheral term only).

| disease | mechanism | discriminant | treatment-target (model) | grade |
|---|---|---|---|---|
| **IBS (IBS-C / IBS-D / IBS-M)** | altered §4 motility (transport bias sets the subtype) + raised afferent gain | constipation/diarrhea subtype emerges from the transport bias; hypersensitivity from raised afferent gain | subtype-directed motility correction (as §14) + lower afferent gain (neuromodulators); brain-gut/felt stays in `mind` | [V] motility / [O] felt |
| **Functional abdominal pain** | afferent gain ↑ without a structural lesion | pain-signal proxy ↑ at normal motility | lower afferent gain (central/peripheral neuromodulation); peripheral term only here | [O] felt |

---

## 5. Remaining work — group C: Tier-3 (NEW layer; honest `[O]` with stated obstacle)

> **ALL FIVE Tier-3 layers are now BUILT** — C1 (immune, §22) + C2 (exocrine-autodigestion, §23) shipped
> **v0.9.0**, and C3 (perfusion/vascular, §24) + C4 (hepatobiliary/bile, §25) + C5 (structural/mechanical,
> §26) shipped **v0.10.0** — see §8 items 6–7. The specs below are retained as the historical work order
> (each `### Cn` section now corresponds to a shipped `§(23+n)` section); seam-wiring (§8 item 8) is now **DONE** (§27, v0.11.0).

Each needs a layer the substrate does not yet contain. Build the layer single-source, derive its switch
form from R19, and grade the un-anchored quantities `[O]` with the obstacle in the ledger. All MINE
except where a sibling/`disease_wp` cross-ref is noted.

### C1. Immune / inflammation layer (no immune primitive yet)
Obstacle: needs a relapsing-inflammation element coupling to the barrier. **Bridge to §7**: the
inflammation→barrier-collapse→dysplasia step reuses the §7 kernel, giving the IBD→colorectal-cancer
continuity once the immune driver exists.
- **IBD (Crohn's, ulcerative colitis)** — mechanism: relapsing inflammation drives the §7 barrier down
  (flares = barrier-scale excursions); treatment-target: suppress the inflammatory drive (raise barrier
  scale back), and the model frames dysplasia surveillance via the shared §7 step. Grade `[V]` bridge /
  `[O]` immune driver.
- Microscopic colitis; eosinophilic esophagitis/gastroenteritis; autoimmune pancreatitis/hepatitis — same
  obstacle. Treatment-target: remove the antigen/eosinophil/immune driver; barrier recovers.
- **Celiac disease** — mechanism: antigen (gluten)-driven immune villous atrophy → absorption coupling to
  §1B falls; treatment-target: antigen removal (gluten-free) → villous/absorption recovery. Obstacle:
  immune villous-atrophy layer. (Common + HLA-linked but not single-gene → MINE; HLA priors cross-ref.)
- Infectious enterocolitis (C. difficile/pseudomembranous, viral, bacterial) — obstacle: microbial +
  immune layer. Treatment-target: clear the pathogen / restore flora.

### C2. Exocrine secretion + autodigestion layer (pancreas module is endocrine-only)
Obstacle: no zymogen/trypsin autoactivation primitive — a **positive-feedback enzyme switch**; the
candidate is an R19 switch in an *autocatalytic* regime, to be derived not fitted.
- **Acute pancreatitis** — mechanism: zymogen autoactivation crosses into a runaway (autocatalytic) basin
  → autodigestion; discriminant: a threshold trigger flips the enzyme switch to the runaway state;
  treatment-target: supportive (the model predicts irreversibility past the autocatalytic threshold —
  remove the trigger *before* threshold). Grade `[V]` mech (once derived) / `[O]` abs.
- Chronic pancreatitis (fibrosis, exocrine insufficiency), EPI, CF-GI/pancreatic — same obstacle
  (secretory/ductal layer). Treatment-target: enzyme replacement (EPI); CF is gene-key → cross-ref
  `disease_wp` (CFTR) while I own the ductal-secretion dynamics.

### C3. Perfusion / vascular layer — ✅ BUILT §24 (v0.10.0)
Obstacle: no perfusion field. **Overlaps `circulatory` sibling — cite, do not re-emerge.**
- Mesenteric ischemia (acute/chronic), ischemic colitis — mechanism: perfusion below a tissue-viability
  threshold → barrier/motility failure; treatment-target: restore perfusion (revascularization). `[O]`.
- GI bleeding (variceal/non-variceal), angiodysplasia — sibling-owned vascular event; cite `circulatory`.

### C4. Hepatobiliary / bile layer — ✅ BUILT §25 (v0.10.0) (SEAM to `circulatory`; metabolic overlap + bile chemistry in-scope)
- **NAFLD / MASLD / NASH** — mechanism: the insulin-resistance overlap maps to the §5 homeostat (gain
  loss) + a new lipid-handling primitive; treatment-target: restore insulin sensitivity (as §12 type-2)
  + reduce lipid load. `[V]` for the IR overlap / `[O]` lipid primitive.
- Cirrhosis, viral/alcoholic hepatitis, cholestasis — hepatic structural layer, **sibling-owned; cite**.
- Cholelithiasis (gallstones), cholecystitis, biliary dyskinesia — needs a gallbladder contractile
  control-loop (small) + bile-chemistry; biliary dyskinesia partly reuses the B1 gate; treatment-target:
  restore gallbladder emptying / remove stones.
- Hepatic encephalopathy — **SEAM to `mind` (firewall)**; only the metabolic ammonia source is in-scope
  here; treatment-target (ammonia lowering) noted, felt/cognitive effect stays in `mind`.

### C5. Structural / mechanical layer — ✅ BUILT §26 (v0.10.0) (Laplace wall-mechanics primitive)
- Diverticular disease/diverticulitis — mechanism: wall weakness + segmental high pressure (pressure
  couples to §4); treatment-target: lower segmental pressure (fibre) / manage inflammation.
- Mechanical obstruction: hernia (incl. hiatal), volvulus, intussusception, adhesive obstruction —
  mechanism: a fixed luminal block (distinct from §14 *functional* obstruction); treatment-target:
  relieve the block (often surgical). Note this is the **mechanical** counterpart that §14 explicitly
  excludes (patent lumen there).
- Megacolon (toxic/acquired); anorectal (hemorrhoids, fissure, fistula) — wall-mechanics primitive.

### C6. Neoplastic — extend the §7 kernel to more sites (this is high-value and *near*-Tier-1)
Reuses the built barrier-Kramers kernel; needs only per-site cited anchors (and a metaplasia step for
Barrett's). Expected anchor `[L]` / shape `[V]` / absolute incidence `[O]`, exactly as §8–§10. **MINE**
(carcinogen/acquired); hereditary syndromes cross-ref `disease_wp`.
- Esophageal carcinoma (adeno via **Barrett's metaplasia** — add a metaplasia step before the kernel;
  squamous via smoking/alcohol anchors).
- Gastric subtypes (intestinal vs diffuse), gastric **MALT lymphoma** (H. pylori-driven — reuses the §10
  g_Hp link), **GIST**.
- Small-bowel adenocarcinoma; gastroenteropancreatic **NET** (carcinoid; pancreatic NET vs the ductal
  adeno already at §9).
- **HCC**, cholangiocarcinoma (SEAM to hepatobiliary; HCC anchor = aflatoxin×HBV, overlaps `circulatory`).
- Anal carcinoma (HPV anchor). Familial syndromes (FAP, Lynch) = germline barrier-scale priors →
  `disease_wp` owns the syndrome, I cross-ref the kernel.
Treatment-target framing for all C6: the kernel makes *prevention/risk-reduction* the lever (remove the
carcinogenic bias / eradicate H. pylori to raise the barrier scale, as §13); therapy of established tumors
is out-of-model.

---

## 6. disease_wp cross-references (NOT mine to build — declare the seam both ways)

Per §6.1/§6.2, these are gene-key and owned by `disease_wp`; I own any common/dynamics counterpart and
**import the gene-key parameter** when the live cross-package wiring exists (currently a declared, unwired
contract — MASTER MAP §9.2). Cross-ref both directions:
- **MODY** = GCK/HNF setpoint-parameter defect → `disease_wp` owns the gene subtype; §12 owns common
  diabetes + dynamics (import the GCK setpoint parameter to compute the MODY trajectory).
- **Glycogen storage disease (hepatic, e.g. type I)** = gene-key buffer-enzyme defect → `disease_wp`; §6
  owns the counter-regulation dynamics (show §6 buffer failure when the gene-crippled buffer is imported).
- **Hirschsprung disease** = RET aganglionosis → `disease_wp` owns the gene lesion; §14 can demonstrate
  the motility consequence (a segment with absent oscillators blocks transit) as an imported-lesion seam.
- **Cystic fibrosis GI/pancreatic** = CFTR → `disease_wp`; I own the ductal-secretion dynamics (C2).
- **Familial cancer syndromes** (FAP, Lynch, Li-Fraumeni, hereditary RCC/VHL) → `disease_wp` owns the
  germline barrier-scale prior; my §7-kernel sites (C6) cross-ref it as a shifted baseline barrier scale.

---

## 7. Discipline (do not drift)

- **No-tuning:** find the parameter whose sweep *emerges* the phenotype; never migrate coefficients to hit
  a target. Anchors are *cited and locked* `[L]`, calibrated by a single bisection to one anchor at most.
- **New primitives single-source:** add to `inherited/vp_substrate.py` and derive the switch form from
  R19/FHN; the substrate file is otherwise vendored/immutable.
- **`[O]` honesty:** every open quantity carries a stated obstacle in `IRREPRODUCIBILITY_LEDGER.md`; record
  falsifiable predictions for the record.
- **Gate + canonical + single zip:** writing stays locked until `research_gate` is all-green and
  `PHASE=writing`; HTML is canonical (answer-first/JSON-LD/claim-strip/vp-card, C2/C4); return exactly one
  consolidated zip rooted at `digestive_vp_site/` (no fragmentation, C0).
- **Treatment for every disease:** the user requires mechanism **and** treatment. Each new section needs a
  **Treatment (model reading)** paragraph: the target parameter, the direction, and the regime/threshold
  where the model predicts the therapy works (efficacy absolute value `[O]`).

---

## 8. Suggested order for the next sessions

1. ✅ **DONE — Group A (D5, §15)**: dumping, reflux-erosion, insulinoma/reactive-hypo, FD-motility,
   SIBO-stasis (in-substrate, no new primitive). Shipped v0.4.0; completes the Tier-1 surface and the
   §11/§14 too-fast-vs-too-slow mirror.
2. ✅ **DONE — Group B / B1 (§16)**: the sphincter-gate primitive (a tonically-closed R19 gate, single-source
   in `inherited/vp_substrate.py`) + GERD / achalasia / esophageal spasm / sphincter of Oddi. Shipped v0.5.0;
   GERD↔achalasia realize the one-gate / two-opposite-failures mirror.
3. ✅ **DONE — Group B / B2 (§17)**: the gastric accommodation-reservoir primitive (the same §2 R19 switch read
   as a fundic wall — `wall_stiffness` `k = 3s² − g`, `reservoir_compliance` `C = 1/k`, `meal_pressure` `P = V·k`,
   single-source in `inherited/vp_substrate.py`) → functional dyspepsia post-prandial distress / early satiation:
   impaired accommodation stiffens the reservoir so a fixed meal raises pressure prematurely (impaired operating
   point ~91% of the stiff baseline; compliance falls in lock-step); the maximal-compliance yield point is the R19
   spinodal (exact [F]); treatment raises the compliance term. Shipped v0.6.0; splits functional dyspepsia into its
   §15 emptying half and its §17 accommodation half.
4. ✅ **DONE — Group B / B3 (§18)**: the visceral afferent-gain primitive (the same R19 element read as a
   visceral afferent — `afferent_gain` / `afferent_signal`, susceptibility `χ = 1/k = 1/(3s² − g)`, single-source
   in `inherited/vp_substrate.py`) → IBS subtypes (IBS-C/-D/-M, the §14 transport bias ordering the subtype by
   retained fraction) + functional abdominal pain. The afferent gain is the SAME `1/k` the §17 reservoir reads as
   fundic compliance (one curvature, two readings), diverging at the SAME R19 spinodal = the §17 reservoir yield;
   visceral hypersensitivity (gain rise + allodynia + spontaneous firing past the spinodal) is [V]/[F], the felt
   pain stays in `mind` behind the **firewall** (peripheral afferent term only). Shipped v0.7.0; the diarrhoea-side
   absolute magnitude hits the §15 conserved-bolus ceiling (honest [O]).
5. ✅ **DONE — C6 neoplastic extension (§19–§21)**: reused the §7 barrier-Kramers kernel with per-site cited
   anchors plus ONE new substrate reading — a metaplasia precursor compartment (`metaplastic_scale` /
   `metaplasia_barrier_drop`, single-source in `inherited/vp_substrate.py`). §19 the Barrett's→EAC + gastric-Correa
   metaplasia step (precursor RR≈11/≈3.6 locked; malignant crossing rate-limited on the precursor; dysplasia ladder
   accelerates; ablation/eradication restores g → rate collapses); §20 the HBV×aflatoxin (inflammation×bias) and
   smoking×alcohol (bias×bias) synergies generalizing the §10 interaction (joint≈22/≈17 super-additive, with a
   falsifiable sub-multiplicative prediction near the spinodal); §21 reversible H. pylori MALT (regresses on g-restore)
   + single-driver HPV anal carcinoma + the honest out-of-kernel boundary (GIST/NET → `disease_wp`, small-bowel
   adenocarcinoma → C1 immune layer, cholangiocarcinoma → hepatobiliary+immune / circulatory seam). Shipped v0.8.0;
   **unifying hypothesis #2 (barrier-scale continuum) demonstrated** — gastritis → ulcer → metaplasia → carcinoma
   across organs on one kernel. Anchors [L] / rate-limiting, ladder shape & synergy [V] / absolute incidence + exact
   ladder ratios + the four boundary sites [O].
6. ✅ **DONE — Group C / C1+C2 (§22, §23)** — the first two Tier-3 cross-system primitives, shipped **v0.9.0**:
   §22 the **immune relapsing-inflammation** layer (a self-sustaining R19 flare basin — `flare_state` /
   `flare_burden` / `inflammatory_barrier_scale`, single-source in `inherited/vp_substrate.py`): IBD shows
   relapsing-remitting **hysteresis** (flip-to-flare drive > return-to-remission drive) forcing the
   **induction≠maintenance** dose asymmetry (induction thr≈0.885, maintenance thr≈0.115 — the same mid-dose
   holds remission but cannot break a flare); the cumulative-burden bridge lowers the **same §7 barrier** the
   §10 kernel uses for H. pylori, so colitis-associated CRC RR rises to the cited UC anchor (RR≈2.4, Jess 2012)
   and **collapses to 1.0 on sustained remission — closing the §21 small-bowel-adenocarcinoma boundary** on the
   inflammation route; celiac + the immune enteropathies are the **antigen-dependent regime** (driver removal →
   remission). §23 the **exocrine autodigestion** layer (an autocatalytic R19 switch — `autoactivation_threshold`
   / `autodigestion_latched`): acute pancreatitis's autoactivation threshold rises with the protective inhibitor
   (SPINK1 ↑; PRSS1-gain ↓), a sub-threshold trigger decays safely but a supra-threshold trigger **LATCHES
   irreversibly** (pre-threshold-only intervention; a strong inhibitor past the spinodal abolishes the basin),
   and chronic EPI is the mirror (large reserve → steatorrhea only past ~90% acinar loss, DiMagno 1973; PERT
   rescue); CFTR gene-key → `disease_wp`. Stress suites `DZ9`/`DZ10` green, disease digest `9d8998c74468…`,
   engine sha `2d363033a1ef…` and C6 digest `cbc73465…` both unchanged. [V] mechanisms / [F] spinodal thresholds
   + the autocatalytic latch / [L] colitis-CRC + >90%-loss anchors / [O] absolute incidences + celiac absorptive
   magnitude + established-disease (necrosis / organ-failure) outcomes + felt components (→ `mind`).
7. ✅ **DONE — Group C / C3–C5 (§24, §25, §26)** — the remaining three Tier-3 cross-system primitives, shipped
   **v0.10.0**: §24 the **perfusion / vascular** layer (a perfusion-viability switch — `perfusion_threshold` /
   `viability_margin` / `tissue_viable`, single-source in `inherited/vp_substrate.py`, bias h = perfusion −
   demand): chronic mesenteric ischaemia (intestinal angina) is a demand-driven viability-margin collapse that
   crosses to deficit post-prandially and is restored by revascularisation, acute mesenteric ischaemia / ischaemic
   colitis is a forced viable→ischaemic **flip** with a time-critical **salvage window** (= 2·spinodal — partial /
   late reperfusion stays infarcted), and NAFLD/MASLD reuses the §12 type-2 gain-loss homeostat unchanged with the
   hepatic lipid-deposition layer a declared `circulatory` seam. §25 the **hepatobiliary / bile** layer (a
   nucleation barrier — `nucleation_barrier` / `supersaturation_drive` / `stone_nucleates`): cholelithiasis is
   metastable supersaturation that nucleates only past CSI > 1 + spinodal (the Kramers crossing) with **dissolution
   hysteresis** (a formed stone persists below saturation — UDCA only on small early stones), gallbladder stasis =
   the §16 B1 gate seam, cholecystitis = B1 gate + the cited §22 C1 flare, cholesterol delivery = `circulatory`
   seam, biliary colic = `mind`. §26 the **structural / mechanical** layer (a Laplace wall-mechanics switch —
   `laplace_pressure` / `herniation_threshold` / `wall_herniates`): diverticular disease is herniation once P =
   tension/radius clears spinodal(g_wall) (low-fibre small radius raises P; a weaker aging / collagen wall crosses
   lower), fibre treatment is the geometry in reverse, diverticulitis = the cited §22 C1 flare, and the mechanical
   fixed-block obstructions (hernia incl. hiatal, volvulus, intussusception, adhesions) = the §14 functional-module
   structural counterpart (surgical, out-of-model). Stress suites `DZ11`/`DZ12`/`DZ13` green, disease digest
   `a2c32ff9f1af…`, engine sha `2d363033a1ef…` and C6 digest `cbc73465…` both unchanged. [V] mechanisms / [F]
   spinodal thresholds (the ischaemic-flip + rescue, nucleation + dissolution, and herniation thresholds, plus the
   Kramers nucleation time) / [O] absolute perfusion/demand, CSI, and pressure/strength scales + structural
   infarction + the cited B1/C1 and `circulatory`/`mind` seams.
8. ✅ **DONE — wired the declared seams** (§27, shipped **v0.11.0**), citation/pointer-only per the neuro↔mind project boundary (no sibling import; each package verifies alone with the siblings absent): the circulatory hepatic interface (Q_H=1500 mL/min, E=0.75, F=0.25 — circulatory is the SSOT owner by its CHARTER 'Seams OUT') is recorded once in `inherited/cross_references.json` (verified against circulatory's `hepatic_clearance()` at vendoring) and **consumed** as the delivery substrate the §24 NAFLD/MASLD lipid load (insulin-resistance core reusing the §12 type-2 homeostat) and the §25 biliary cholesterol (nucleation thermodynamics) sit on, the lipid-handling and absolute-CSI scale handed back as circulatory's [O]; the `mind` felt-symptom seam (visceral pain §18, biliary colic §25) is a **one-way forward-defer pointer** carrying no consumed value (→ mind's M18 interoception route, Saper 2002); and the **firewall is enforced by an architectural lock** — zero sibling imports across every package python file and a metabolic state with no felt/HPA key — the SAME lock mind runs neuro-side. New layer `repro/_seams/seam_wiring.py` + `inherited/cross_references.json` (+ loader); stress suite `DZS` green; engine sha `2d363033…`, disease digest `a2c32ff9f1af…` and C6 digest `cbc73465…` all **UNCHANGED** (the seam layer carries its own 2×sha256 digest `ecce55ce…`, separate from the engine and disease layers, exactly as C6 does). [V] the consumed circulatory interface + the §12-homeostat reuse / nucleation thermodynamics resting on it / [F] the firewall + the mind one-way pointer / [O] the lipid-handling + cholesterol-delivery magnitude (circulatory's) and the felt pain/affect (mind's). REMAINING — the **live cross-package harness** (running both sibling engines in one process, outside each gate so the verify-alone guarantee holds): the `circulatory`
   lipid-deposition (NAFLD/MASLD, §24) and cholesterol-delivery (bile, §25) seams, and the `mind` felt-symptom
   seams (biliary colic §25, visceral pain §18). Beyond Tier-3, the non-neoplastic peristalsis / homeostat /
   barrier targets and the remaining roadmap (GI bleeding, cirrhosis/hepatitis, megacolon, anorectal) stay
   enumerated in `FUTURE_WORK.md`. Keep the three unifying hypotheses front-of-mind (#1 done; **#2 done via C6
   §19–§21**; #3 already shown in §12). Same verbatim recipe (§1) for any new layer — one new R19-derived
   primitive, no tuning, every `[O]` with its obstacle, the gate green, HTML canonical, one zip.
