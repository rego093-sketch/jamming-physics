# CHANGELOG — homeostasis_thermometabolic_vp_site

All notable changes to this package. Grades: [V] simulation-verified · [F] forced · [L] measured · [O] open (obstacle stated).
The vendored substrate `inherited/vp_substrate.py` is byte-identical across every version (sha256 prefix `5664800b…`); only science-neutral and research-fill changes are recorded here.

## [0.6.0] — 2026-06-19 — the precision-routing layer: compartment-restricted restoration (the analgesic local-anaesthesia mirror)

**Concept DOI (this whitepaper): [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)** (CC BY 4.0). Substrate `inherited/vp_substrate.py` byte-identical (sha256 prefix `5664800b…`). This version executes the v0.5.0 HANDOVER's named forward priority #3 — the **optional precision layer** — done fully self-contained, with **no external data, no panel mutation, no live fetch**, and **no change to the engine** (the cross-species panel, every read γ value, and the engine result are byte-identical; engine sha256 stays `08f50d6d…`). The new module is a restoration-LAYER extension, surfaced like the three-lever module (in `repro/run_all.py`, not folded into `circulate()`), so the 16-target stress battery and `research_gate.all_green` are untouched.

### The science (a tissue-compartment routing map, firewalled — with a PROOF)
- **The mirror.** The analgesic package distinguishes a SYSTEMIC threshold-raiser (acts body-wide) from a PRECISION local anaesthetic (a regional block confined to one nerve's territory). The same distinction, re-read for the setpoint-restoration levers, asks WHERE each lever's node acts: a single tissue COMPARTMENT (a precision route) or many (systemic). Each restoration target is placed on a CITED anatomical compartment map and classed **PRECISION** (one compartment), **REGIONAL** (2–3), or **SYSTEMIC** (≥4 compartments, or a distributed immune/stromal node with no single locus), by a parameter-free rule on the cited compartment count.
- **Result.** Nodes split **2 PRECISION / 5 REGIONAL / 2 SYSTEMIC**. The two clean precision routes are UCP1→brown fat (BAT) and MC4R→hypothalamus (a single cited compartment each); INSR (the ubiquitous insulin receptor, 4 dominant compartments) and TNF (a distributed inflammatory program) are honestly SYSTEMIC — restoration cannot be confined to one place. Three NAMED routes span the spectrum: a **BAT-targeted** route (the cleanest precision), a **central appetite-axis** route (precision anatomy but a blood-brain-barrier [O] deliverability obstacle), and a **hepatic glucose-disposal** route (the honest distributed case — a body-wide receptor, so a dominant-compartment route, not a single-compartment block).
- **Routability [F] vs deliverability [O].** The map keeps WHICH compartment (cited anatomy, [F]) distinct from whether an intervention can REACH it (an [O] deliverability obstacle: the blood-brain barrier for central targets, the small/variable BAT depot, the no-single-locus problem for a distributed node). No obstacle is silently dropped.
- **The firewall is PROVEN, not asserted.** The routing specificity is a parameter-free reciprocal of the cited compartment COUNT; γ is never an input to it, only carried alongside as the promoter switch-threshold context. `gamma_independence_gate()` recomputes the whole map under a drastically perturbed γ atlas and confirms every routing field (compartments / primary / specificity / tier) is **byte-identical** while **only** the carried γ-context column moves — the read is present but firewalled out of the routing. (Visible in the rendered table: the ordering is precision-first, and MC4R, the LOWEST-γ node, sits at the top because it is single-compartment — not because of γ.)

### Code (science-neutral additions; no tuning, no evolution/selection language)
- `repro/_pathology/precision_routing.py` (new): the cited `COMPARTMENTS` / `ROUTING` maps, the three `NAMED_ROUTES`, the parameter-free `_tier` / `_breadth` classification, and four fail-closed gates — `gamma_independence_gate()` (the firewall proof), `anatomy_honesty_gate()` (every assignment cited; SYSTEMIC nodes not oversold; behind-barrier primaries graded [O]), `forbidden_claim_scan()` (the analgesic scan EXTENDED with a DELIVERY class: no injection/implant/catheter/dose-as-fact; reuses the restoration scan machinery), and `falsification_register()` (PR1–PR3 + FRAMEWORK). Deterministic: its own 2×sha256 self-check (routing sha256 `21021e79…`). It reads the γ atlas read-only and never touches the panel or the substrate.
- `repro/run_all.py`: added block **[5b] PRECISION ROUTING** between restoration and gates — prints the tier split, the named routes, the γ-independence proof, the gate results, and the routing determinism line. `circulate()`, `stress_targets()`, the 16-target battery, and `research_gate` are unchanged.

### Site
- `tools/build_docs.py`: added two restoration-group chapters — **§R "Precision routing: regional vs systemic restoration"** (the concept, the three tiers, routability-vs-deliverability, and the γ-independence proof with a vp-card) and **§RM "The compartment routing map"** (the full 9-node table with carried γ-context and deliverability, the three named routes, and the PR1–PR3 + FRAMEWORK falsifiers) — placed after §P, before §G. Every number is engine-pulled at generation time. Hub abstract / llms.txt / _meta.json gained a one-line precision-routing note (γ firewalled out of the routing). Site is now **1 hub + 32 chapter pages**; C1 drift 0; llms.txt 4424 bytes (<5KB). **Site sha256:** `3bb5657b…`.

---

## [0.5.0] — 2026-06-19 — the regulatory-layer object: a methylation-substrate NULL (RH9 / NULL-4)

**Concept DOI (this whitepaper): [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)** (CC BY 4.0). Substrate `inherited/vp_substrate.py` byte-identical (sha256 prefix `5664800b…`). This version executes the v0.4.0 HANDOVER's named forward priority #3 — the firewalled **regulatory-layer object** — done self-contained: a second, GC-normalized sequence read of the *same* vendored panel, with **no fabrication, no panel mutation, and no live fetch**. The cross-species panel is UNCHANGED (the original 19 cache entries and every read γ value stay byte-identical); RH9 is computed from the cache already on disk.

### The science (a second pre-registered NULL, closing a second static layer)
- **Why a second layer.** RH8 showed no promoter γ separates hibernators, but γ (a nearest-neighbour stacking-stiffness read) is **almost entirely GC-loaded** across this panel (cross-cell r(γ,GC)=0.9955), so the honest objection is that RH8 only ruled out GC. The natural answer is the methylation **substrate**: **CpG observed/expected** (Gardiner-Garden & Frommer 1987) — the CpG-island architecture DNA methylation acts on — which is **GC-NORMALIZED** by construction (observed CpG ÷ the C,G-expected count), so it is *not* a restatement of GC.
- **Pre-registered NULL-4 (RH9) — confirmed.** Across the same 8 torpor/BAT genes × 14 species (7 hibernators vs 5 non-hibernators among endotherms), **0 of 8 genes** has a CpG-O/E range that cleanly separates hibernators — all ranges overlap, and no gene survives Bonferroni (smallest exact-permutation p≈0.057). CpG O/E is a **genuinely distinct read from γ** (cross-cell r(γ,CpG O/E)=0.5601, clearly sub-unit) and **far less GC-loaded** (r(CpG O/E,GC)=0.4927 vs 0.9955 for γ). **Reading:** two *independent* static sequence layers — stacking stiffness and methylation-substrate architecture — are both flat across hibernation status. Neither encodes hibernation capacity; the capability is **DYNAMIC regulatory gating** of genes present in all (humans included), readable only in an in-vivo torpor↔euthermia methylation/expression contrast (**cited, [O] external** — the offline-reproducibility invariant precludes vendoring processed in-vivo data, so this is the named honest next step, not a stub).

### Code (science-neutral additions; no tuning, no evolution/selection language)
- `repro/_engine/endotherm_ectotherm.py`: added `null_cpg_oe_does_not_track_hibernation()` (NULL-4) plus the parameter-free helper `_cpg_oe` (Gardiner-Garden & Frommer 1987) and the module note `CITED_DYNAMIC_REGULATION` (the external [O] dynamic-regulation step, with named citations). Separation is judged purely by CpG-O/E range overlap; the γ↔CpG-O/E dissociation and the GC-loading contrast are reported via parameter-free cross-cell Pearson r, **never used as a fitted gate**. NULL-1/2/3 and `rederive_offline()` are untouched and still pass; all original read γ values are byte-identical.
- `repro/_engine/vp_trm_engine.py`: surfaced NULL-4 in `foundational_analysis()` and `circulate()`, and wired a new stress target **RH9** (PASS iff `null_holds` **and** the two static reads are distinct) into `stress_targets()`. **Stress battery 15 → 16 targets, all PASS.**
- `repro/_verify/stress_tests.py`, `repro/run_all.py`: RH9 added to the suite list and the entry report (count 15 → 16; NULL-4 line printed).
- Determinism preserved: 2×sha256 identical; offline re-derivation of all 107 cells bit-for-bit (drift 0). **Engine sha256 changes** (expected, new code): `08f50d6d…`. The original 19 cache entries and all original read γ values are byte-identical and unchanged.

### Site
- `tools/build_docs.py`: added chapter **§11.2 "NULL: the methylation substrate does not mark hibernation either"** (answer-first, vp-cards, a per-gene CpG-O/E table, JSON-LD), placed after §11.1; hub / llms.txt / _meta.json updated from "three pre-registered nulls" to four, and "15/15" to "16/16". Site is now **1 hub + 30 chapter pages**; C1 drift 0; llms.txt 3996 bytes (<5KB). **Site sha256:** `51af55ce…`.

---

## [0.4.0] — 2026-06-19 — hibernation-bridge expansion: the 8-gene torpor-panel NULL (RH8)

**Concept DOI (this whitepaper): [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)** (CC BY 4.0). Substrate `inherited/vp_substrate.py` byte-identical (sha256 prefix `5664800b…`). This version executes the strongest forward research priority from the v0.3.0 HANDOVER: widen the present-but-silenced hibernation NULL (RH4, one gene) into a pre-registered panel-level NULL across many hibernating species and the whole declared torpor program (RH8).

### The science (the headline is a strengthened negative result)
- **Cross-species panel widened from 3 genes × 7 species to 8 genes × 14 species.** Genes added: PPARGC1A (mitochondrial coactivator), DIO2 (thyroid activation), CIDEA (brown-fat identity), FGF21 (metabolic-state hormone), SLC2A4/GLUT4 (insulin-responsive glucose transporter), joining UCP1 / ADRB3 / PDK4. Species added: Urocitellus parryii, Marmota marmota, Mesocricetus auratus, Microcebus murinus (a torpor-capable PRIMATE), Ursus americanus, Cavia porcellus (GC-matched rodent control), Oryctolagus cuniculus, joining the original seven. **88 new promoters fetched** from NCBI RefSeq under the identical vendored convention; panel now holds 107 measured cells (5 absent cells are real orthology gaps in the two ectotherm assemblies, recorded honestly).
- **Pre-registered NULL (RH8) — confirmed and quantified.** Among endotherms (7 hibernators vs 5 non-hibernators), **0 of 8 genes** has a promoter γ range that cleanly separates hibernators from non-hibernators — all 8 ranges overlap. Every group-mean γ gap co-signs and co-scales with the group GC gap: cross-gene **Pearson r(Δγ, ΔGC) = 0.9957**, near unit slope. The one nominally low-p gene (ADRB3, exact permutation p≈0.024) fails Bonferroni (0.05/8), is GC-matched, has fully overlapping ranges, and runs biologically backwards — i.e. it is the GC confound, not a torpor signal. **Reading:** hibernation capability is REGULATORY gating of genes that are PRESENT in non-hibernators too (humans included), not a sequence-level γ threshold. A clean negative result is the contribution; the firewall is upheld at panel scale.

### Code (science-neutral additions; no tuning, no evolution/selection language)
- `repro/_engine/endotherm_ectotherm.py`: added `null_torpor_panel_gamma_does_not_track_hibernation()` (NULL-3) plus parameter-free helpers `_panel_gc`, `_cell_gamma_gc`, `_pearson`, `_exact_perm_p` (exhaustive permutation, deterministic, no RNG) and the module constant `TORPOR_PROGRAM_GENES`. Separation is judged purely by γ-range overlap; the GC confound is reported via parameter-free sign-agreement and a cross-gene Pearson r, never used as a fitted gate. Existing `null_pdk4_gamma_does_not_mark_hibernation()` (NULL-2/RH4) and `rederive_offline()` are untouched and still pass.
- `repro/_engine/vp_trm_engine.py`: surfaced NULL-3 in `foundational_analysis()` and `circulate()`, and wired a new stress target **RH8** (torpor-program promoter panel does not encode hibernation capacity; PASS iff `null_holds`) into `stress_targets()`. RH4 retained. **Stress battery 14 → 15 targets, all PASS.**
- `repro/_verify/stress_tests.py`, `repro/run_all.py`: RH8 added to the suite list and the entry report (count 14 → 15; NULL-3 line printed).
- Determinism preserved: 2×sha256 identical; offline re-derivation of all 107 cells bit-for-bit (drift 0). **Engine sha256 changes** (expected, new code): `e5cfa00a…`. The original 19 cache entries and all original read γ values are byte-identical and unchanged.
- `tools/fetch_thermo_panel.py`: faithful vendored fetcher (idempotent; never mutates cached cells; NCBI etiquette: tool/email/backoff/rate-limit) recorded for provenance. The panel ships pre-fetched; NCBI is contacted only if a cell is absent.

### Site
- `tools/build_docs.py`: added chapter **§11.1 "NULL: no promoter in the torpor panel marks hibernation"** (answer-first, vp-cards, a per-gene table, JSON-LD), placed after §11 (bear-vs-human); hub/llms.txt updated from "two pre-registered nulls" to three. Site is now **1 hub + 29 chapter pages**; C1 drift 0; llms.txt 3729 bytes (<5KB). **Site sha256:** `31fdc105…`.

---



**Concept DOI (this whitepaper): [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)** (CC BY 4.0). Distinct from the borrowed restoration-method DOI 10.5281/zenodo.20733420 (analgesic three-lever technology). All site DOI placeholders are finalized to the concept DOI; the engine is unaffected (engine sha256 unchanged).

This version takes the package from a research skeleton (all 14 stress targets TODO) to a complete,
gate-green research program with a canonical multi-page HTML site. The path 0.1.0 → 0.2.0 → 0.3.0 was
executed in one session; the package ships once, at 0.3.0.

### DNA emergence (default; actively applied)
- **PDK4 promoted TO-MEASURE → measured [V]** (γ=1.4112, NC_000007.14, promoter window TSS−2000..+500)
  via the *identical* DNA `fetch_morpho_gamma` pipeline (NN-stacking ΔG37, SantaLucia 1998). No named
  master remains unmeasured; `_to_measure` is now empty.
- **Cross-species furnace/torpor panel vendored** (`inherited/crossspecies_thermo_panel.json`): UCP1 +
  ADRB3 + PDK4 across 7 species (human, mouse, rat, pig, ground squirrel, zebrafish, frog), with a
  sequence cache so every read re-derives **offline bit-for-bit** [V].
- `inherited/organ_gamma.json`, `inherited/organ_identity.md`, and the engine ORGAN_ROWS updated to reflect
  the measured PDK4 node.

### Foundational module — endotherm vs ectotherm (the heart) [new]
- `repro/_engine/endotherm_ectotherm.py`: answers the three required questions with **no evolutionary
  language** (observation only):
  - **Q1 gene criterion** — the divide is the PRESENCE of a drivable {UCP1 furnace + ADRB3 command} pair,
    not a γ value [L]; ADRB3 absent in the ectotherms queried [O].
  - **Q2 mechanism** — one R19 parameter (basin depth): endotherm setpoint sensitivity 0.054 vs ectotherm
    1.394 [V]; "defends iff spinodal(g) > ambient amplitude".
  - **Q3 range** — γ spans only ~1.22–1.50 and does NOT track the divide; the real range is in the
    dynamics (metabolic factor ~5–10× [L], discontinuous regime boundary [V]).
  - **Two pre-registered NULLs** [V]: UCP1 γ does not separate endo/ecto (GC-confounded; pig pseudogene
    sits among functional rodents); PDK4 γ does not mark hibernation (deep-hibernator γ not elevated →
    present-but-silenced switch, RH4).

### Engine dynamics — the defended setpoint loops [filled]
- `repro/_engine/vp_trm_engine.py`: implemented the remaining stress targets as R19 dynamics —
  `thermostat_step` (RT2), `bat_thermogenesis` (RG1), `fever_vs_hyperthermia` (RG3),
  `torpor_hysteresis_sweep` (RH1, central — hysteresis loop width 1.30 → bistable SWITCH),
  `torpor_regulated` (RH2), `glucose_homeostat` (RE1), `lipostat` (RE2), `hibernation_bridge` (RD4).
  `stress_targets()` aggregates all 14 with honest grades; `circulate()` now emits the full result.

### Stress battery — 14/14 PASS
- `repro/_verify/stress_tests.py` wired to the engine. RT1–RD4 all PASS; RT5 (Kleiber) passes **as [O]
  with a stated obstacle** per the CHARTER bar (reproduced [V] OR honestly flagged [O]). Determinism
  2×sha256 identical (engine sha256 `25dd4e40…`).

### Pathology — disease as setpoint failure (a subset) [filled]
- `repro/_pathology/setpoint_failure.py`: one **derived law** from R19 — a loop-gain drop d gives
  g_eff=g(1−d), shrinking the barrier and lowering the crossing threshold; a chronic forcing then DRIFTS
  (sub-spinodal) or CROSSES (supra-spinodal) the setpoint. Instantiated per disease: T2D (crossed),
  obesity (drift), metabolic syndrome (coupled crossing), MODY (imported parameter). Shape [V], anchors
  [L], absolute incidence [O].

### Restoration — the analgesic three-lever technology, applied [new]
- `repro/_pathology/restoration_levers.py`: SETPOINT-RESTORATION via the three-lever frame from
  `analgesic_threshold_logic_v2_0` (method DOI 10.5281/zenodo.20733420): **S1** restore loop gain / deepen
  basin (INSR/LEPR/PPARG), **S2** reduce pathological forcing (MC4R/GHRL/UCP1/ADRB3), **S3** remove the
  upstream sensitising/uncoupling program (PDK4 hibernation-bridge misfire + inflammation, [O] cited).
  Includes target prioritisation (declared weights B/U/D, γ never folded into score), an **S3 honesty
  gate** (fail-closed), a **forbidden-claim scan** (dosing/synthesis/efficacy/safety), and a
  **falsification register** (SP1–SP3 + FRAMEWORK). All restoration gates PASS. Firewall: γ is never a
  glucose/HbA1c/dose/clinical effect; HYPOTHESES only, no medical responsibility.

### Canonical site (VP-SPEC v1.8, C1–C4) [new]
- `tools/build_docs.py`: deterministic generator emitting **1 hub + 28 chapter pages** under
  `docs/thermometabolic/{slug}/` — answer-first (40–60 words), abstract, claim-strip, ScholarlyArticle +
  BreadcrumbList JSON-LD, canonical link, vp-cards, prev/next nav. Access layer: `robots.txt` (7 agents),
  `sitemap.xml`, `llms.txt` (3.5 KB < 5 KB), `_meta.json`. **C1 drift-0 self-verify** passes (site sha256
  `61480d17…`, byte-identical on regeneration). No TeX bundled (C2). The site is SPLIT into pages, not one
  long HTML; the package still ships as ONE zip (C0).

### Governance
- Four-document SSOT created (CHANGELOG / MASTER_MANUAL / COMPLETION_LEDGER / HANDOVER); VERSION → 0.3.0;
  PHASE → writing; IRREPRODUCIBILITY_LEDGER and manifest regenerated.

## [0.2.0] — 2026-06-19 — logical research-fill (internal milestone)
- All 14 stress targets implemented as R19 dynamics and brought to green; foundational endotherm/ectotherm
  module written and validated; pathology law derived; restoration levers built. (Folded into the 0.3.0
  ship — not released separately.)

## [0.1.0-research] — prior — research skeleton
- Charter, START_HERE, vendored substrate + γ atlas (PDK4 = to-measure), engine emergence + oscillator
  scaffolding, 14-target stress battery (all TODO), pathology + docs stubs, PHASE=research (writing locked).
