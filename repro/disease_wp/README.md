# Genetic & Rare Disease Whitepaper — working package (v0.17, Phase R15 complete — curated PMC-OA severity lift round 7: Acute intermittent porphyria 0.50[H]→0.75[L] (sub-rankable, no lock), Achondroplasia [O]→0.75[L] (rankable, retains mortality [H], no lock), Phenylketonuria [O]→0.75[L] — PKU's onset+disability were already [L], so this completes its order-lock as a disclosed CONSEQUENCE (set 5/35→6/35, +Phenylketonuria); R15 gate PASS 16/16, unmet-need gate PASS 6/6, W1 gate PASS 17/17, boundary gate PASS 6/6)

A single-author research whitepaper on **systemic-body genetic and rare diseases**: their molecular mechanisms,
a reproducible burden ordering, and established treatment mechanisms. Brain, nerve, heart, and affect are owned
by the sibling neuro/mind whitepapers and are not re-covered here (`SCOPE.md`). A **second** sibling boundary —
against the 13 body-system packages (acquired/common/loop-dysregulation disease, incl. carcinogen-driven
cancers) — keeps this volume to **monogenic/rare** disease and prevents redundant research; it is governed by
`SCOPE.md` → *Sibling body-system packages*, constitution **C-D10**, and the carried cross-package master map
`VP_FRAMEWORK_MAP.md`, and its wiring is gate-checked by `tools/boundary_gate.py`.

Governed by **VP-SPEC v1.8** (bundled). Authoring language: **English**. Author reporting: **Korean**.

## What is in this package

```
disease_wp/
├── ROADMAP.md                 ← READ FIRST. Phased plan: investigate (R1–R4) → write (W1+) under VP-SPEC.
├── VP_FRAMEWORK_MAP.md        ← cross-package master map (author, KR): etiologic-class ownership boundary vs the 13 body-system packages (§6); carried here so the boundary travels with the volume
├── VP_SPEC_v1_8.md            ← governing standard (LOCK reference)
├── CONSTITUTION_disease.md    ← project rules (subordinate to VP-SPEC §0)
├── SCOPE.md                   ← in/out boundary + multi-system rule
├── methodology/
│   ├── DISEASE_TAXONOMY.md    ← inheritance × mechanism × organ axes
│   ├── BURDEN_INDEX.md        ← deterministic "suffering order" (reproducible, C1) — R3, finalized
│   └── BURDEN_LEXICON.md      ← R3: declared regex tiers + mortality classifier (generated from builder SSOT)
│   ├── DATA_PROVENANCE.md     ← NCBI sources + citation rules
│   ├── mechanism_rules.csv    ← R2: curated cited molecular-mechanism class rules (8)
│   ├── dossier_cohort.csv     ← R2: pre-registered 35-disease dossier cohort (18 flagship + 17 ext)
│   ├── omim_join_supplement.csv ← R2: HPO-name-verified OMIM joins for series-number concepts
│   ├── TREATMENT_INDEX.md     ← R4: treatment-survey method + residual offset (two honest [H] tiers)
│   ├── treatment_rules.csv    ← R4: curated established standard-of-care table (35 diseases)
│   └── TREATMENT_LEXICON.md   ← R4: treatment-efficacy detection patterns (generated from builder SSOT)
├── code/emergence_v2/         ← carried normal-development baseline engine (drift 0, 5/5 gates)
├── code/pipeline/             ← R1–R4 living pipeline (r1_*, r2_*, r3_*, r4_* ; not in the frozen engine pin)
├── data/raw/                  ← cached NCBI/HPO/ClinGen sources (self-contained, no rebuild network)
│   ├── clinvar/ clingen/ medgen/ hpo/  ← gene resources, dosage scores, esummaries, phenotype.hpoa+hp.obo
├── data/curated/
│   ├── disease_index_base.csv ← R1: 7,672 diseases, scope-partitioned (sha ddfbcac71d6b)
│   ├── disease_index.csv      ← R2 deliverable: 6,167 in-scope, inheritance+mechanism graded (sha a274e25a00bb)
│   ├── dossiers/<slug>.json   ← R2: 35 per-disease dossiers + _cohort_index.json (set sha 94818007c9cc)
│   ├── burden_scores.{csv,json} ← R3: deterministic burden order over the 35 dossiers (burden-set sha 0f788821e0fc)
│   ├── treatments.{csv,json}  ← R4 deliverable: treatment survey, 35 diseases, two [H] tiers (treatments sha f5ba4f0e438d)
│   └── burden_residual.{csv,json} ← R4: residual (post-treatment) order, raw_burden·(1−e) (residual sha d41d4e95b8b1)
├── reports/                   ← r1/r2/r3/r4.gate.json (PASS 5/5·7/7·9/9·11/11) · consolidation.gate.json (10/10)
│   └── w1.gate.json           ← W1 authoring gate PASS 15/15 (drift-0, retrieval, no-fab-cure, engine-pin)
├── tools/                     ← W1 living code (NOT in the frozen engine pin)
│   ├── w1_build.py            ← deterministic site generator (sha d9e39b356c24; site-set sha c97175f90cb1)
│   ├── w1_gate.py             ← W1 authoring gate (sha 95e2d8cb7f4f)
│   └── boundary_gate.py       ← sibling-package boundary WIRING guard (map+SCOPE+C-D10+README present); PASS 6/6
├── docs/                      ← ▶ W1.1 CANONICAL SITE — one standalone HTML per disease (Google/RAG-ready)
│   ├── disease/index.html     ← volume hub (CreativeWorkSeries JSON-LD, links every page)
│   ├── disease/01-classification-burden-treatment-framework/index.html   ← framework §1 (method + grades)
│   ├── disease/<NN-slug>/index.html   ← 17 PLACED diseases §2–§18, residual-burden order, ONE PAGE EACH
│   │                                    (answer-first, MedicalCondition+ScholarlyArticle+Breadcrumb JSON-LD)
│   ├── disease/_meta.json     ← volume summary card (sha b4f28df8e6e5)
│   ├── assets/css/site.css    ← shared stylesheet (no inline CSS/JS, no katex, max page 15 KB)
│   ├── sitemap.xml robots.txt llms.txt   ← 19 URLs · 7 crawlers allowed · LLM index (<5 KB)
├── IRREPRODUCIBILITY_LEDGER.md ← C3: volume-level provisional-[H] condition + per-field [O] items
├── MANIFEST_governed.sha256   ← governed pin over the engine (15 .py/.json) — UNCHANGED by W1
└── VERSION
```

## The carried engine (`code/emergence_v2/`)

A DB-grounded morphogenesis engine carried verbatim from the DNA package. It forward-simulates normal
development from **measured, cited** biophysical parameters and grades every quantity honestly
(`[V]` law / `[L]` measured-grounded / `[F]` universal rule / `[O]` needs more data). It **never fits to
targets** (NON-FIT invariant). It is the *normal-development baseline* against which developmental diseases are
read. It is read-only here.

Run the gates (each is deterministic; numpy + scipy required):

```bash
cd code/emergence_v2
python3 verify_emergence.py            # cardiac engine        → 7/7
python3 verify_emergence_organs.py     # organ allometry       → 6/6
python3 verify_emergence_trajectory.py # reduced-order RD form → 7/7
python3 verify_emergence_organs_wide.py# widened organ set     → 8/8
python3 verify_emergence_morphogen.py  # λ=√(D·τ) length band   → 8/8  (band sha 4ea1c7b4111c)
```

Verify the engine has not drifted:

```bash
sha256sum -c MANIFEST_governed.sha256   # expect: all OK
```

## What to do next

Phases **R0–R4 are complete**, the **▣ consolidation gate has PASSED (10/10)**, the **canonical Phase-W1 site is
built** (one standalone HTML per disease, hub + framework §1 + 21 placed pages in residual-burden order + 14
not-placed + 2 mechanism-class chapters; W1 gate PASS 17/17), and **eleven cumulative registry `[L]` passes have now
landed** (R5–R15; the R3/R4 banked files stay byte-identical, each later pass is a dedicated additive stage):
- **R5** — treatment accession-dating to GeneReviews Management → `[L]` 33/35 (2 retain `[H]`: no disease-directed therapy).
- **R6** — Orphanet natural-history register → onset `[L]` 28/35 (+1 mortality), 1st order_locked.
- **R7** — open-source natural-history pass: **disability `[L]` 4→13/35** from the openly published **GBD 2013
  disability-weights table** (4 diseases promoted into the placed order; PKU's definition-overstated tier corrected
  downward by the published weight), plus **2 mortality axes independently corroborated** from PMC survival
  literature. The OMIM clinical synopsis is **worked around** (no obtainable key; datacenter-IP-blocked) —
  clean-skipped with the obstacle named, severity not guessed.
- **R8** — **severity `[L]`** from the open **HPO Severity subtree (HP:0012824)** via a cited obligate dominant-sequela
  join (Achondrogenesis type II → 2nd order_locked).
- **R9–R15** — **curated PMC open-access** dominant-sequela literature lifting **progression** and **severity**, the
  tier **DERIVED by the frozen R3 tier function** over the verbatim cited sentence (no new cut-points). Niemann-Pick
  type A progression → tier 1.0 (3rd order_locked, R9); Marfan severity 0.50→0.75 completes the **4th** order_lock
  (R11); Duchenne MD severity 0.50→0.75 completes the **5th** order_lock (R12) — DMD being the only cohort disease
  with all **five** axes scored and every one registry-`[L]` — plus Fabry/Marfan/HT-1 grade-only corroborations. R13
  then adds Maple syrup urine disease severity 0.50→0.75 (via 'life-threatening') plus Cystic fibrosis and Pompe
  progression grade-only; R14 adds Classic homocystinuria and Fabry disease severity 0.50→0.75 plus Becker muscular
  dystrophy progression grade-only — **none of the R13/R14 lifts completes a new order-lock** (each lifted disease
  retains another `[H]` scored axis). **R15** adds three severity lifts, all to tier 0.75 via 'severe': Acute
  intermittent porphyria 0.50→0.75 (only 2 scored axes — sub-rankable, **no lock**), Achondroplasia `[O]`→0.75
  (rankable but retains mortality `[H]`, **no lock**), and Phenylketonuria `[O]`→0.75 — because PKU's onset and
  disability were **already** `[L]`, this completes its order-lock as a **disclosed CONSEQUENCE** (not engineered: S
  and D are orthogonal axes from different sources, and the cited sentence passes every criterion independently), so
  the lock set **moves 5/35 → 6/35 (+Phenylketonuria)**. Every
  declined statement (spectrum / comparative / umbrella / historical / form-specific / sub-phenotype) is recorded with
  its per-disease reason in the `severity_litcurate*_excluded.csv` family and surfaced in the ledger; **Hb SS disease**,
  **Alpha-1-antitrypsin deficiency**, **Hemophilia A** and (new at R15) **21-OHD CAH** / **Hemochromatosis type 1** /
  **Wilson disease** are noted obstacle-bound or frontier entities.

**order_locked 6/35** (Achondrogenesis type II, Niemann-Pick type A, Tyrosinemia type II, Marfan syndrome, Duchenne
muscular dystrophy, Phenylketonuria). The **burden order remains provisional `[H]`** (carried on every page) because **17 placed diseases
still carry at least one `[H]` axis** — overwhelmingly **severity**, which is only *partially* liftable from open data
(most diseases have no defensible obligate / non-comparative / non-spectrum disease-level magnitude). The **OMIM
clinical-synopsis path stays REMOVED** (key unobtainable for an individual researcher), not deferred; raising the rest
of severity/progression depends on a cited disease-level OA magnitude becoming retrievable (see
`reports/R15_NOTES_AND_HANDOVER.md` and `FUTURE_WORK.md`). Verify the current state with `python3 tools/w1_gate.py`
and the pipeline gates `python3 code/pipeline/r15_gate.py` (and r1–r14). The full versioned history is in `VERSION`; the
open-item ledger is `IRREPRODUCIBILITY_LEDGER.md`. See also `ROADMAP.md`.

## Build / verify the W1 site

```bash
python3 tools/w1_build.py                        # emits docs/ — 19 pages (site-set sha c97175f90cb1, deterministic)
python3 tools/w1_gate.py                          # W1 authoring gate PASS 15/15 (drift-0 vs CSVs, retrieval, no-fab-cure, engine pin)
```

## Reproduce the investigation (R1 → R4)

```bash
python3 code/pipeline/r1_build_index.py          # base index (sha ddfbcac71d6b)
python3 code/pipeline/r1_gate.py                 # R1 gate PASS 5/5
python3 code/pipeline/r2_enrich_inscope.py       # disease_index.csv + inheritance (cached MedGen)
python3 code/pipeline/r2_boundary_review.py      # CNS boundary moves + cns_cross_reference col
python3 code/pipeline/r2_mechanism.py            # mechanism_class (index sha a274e25a00bb)
python3 code/pipeline/r2_cohort_medgen.py        # cohort MedGen cache (OMIM cross-refs)
python3 code/pipeline/r2_cohort_gene_resources.py# NCBI Gene + ClinVar per cohort gene
python3 code/pipeline/r2_build_dossiers.py       # 35 dossiers (set sha 94818007c9cc)
python3 code/pipeline/r2_gate.py                 # R2 gate PASS 7/7
python3 code/pipeline/r3_burden_index.py         # burden_scores.{csv,json} (burden-set sha 0f788821e0fc)
python3 code/pipeline/r3_gate.py                 # R3 gate PASS 9/9
python3 code/pipeline/r4_treatment_survey.py     # treatments.{csv,json} + TREATMENT_LEXICON.md (treatments sha f5ba4f0e438d)
python3 code/pipeline/r4_burden_residual.py      # burden_residual.{csv,json} (residual sha d41d4e95b8b1)
python3 code/pipeline/r4_gate.py                 # R4 gate PASS 11/11
python3 code/pipeline/consolidation_gate.py      # consolidation gate PASS 10/10 (subsumes R1–R4; R→W pivot)
sha256sum -c MANIFEST_governed.sha256            # engine pin drift 0
```

## Reproducibility status (this package)

- Engine carried with **drift 0** across relocation: 5/5 emergence gates re-pass at the new path; morphogen
  `validation sha 01b0b6ea8b10` / `band sha 4ea1c7b4111c` identical to the DNA package closeout.
- Governed pin self-verifies OK (15 files).
- **R1** base index deterministic (sha `ddfbcac71d6b`); R1 gate **PASS 5/5**.
- **R2** enriched index deterministic (sha `a274e25a00bb`); 35-dossier set deterministic
  (set sha `94818007c9cc`, confirmed by repeated identical runs; was `b70b12d01e75` after the v0.5.1
  erratum E1 FAH-geneid fix, `aba06f038e4d` before it; moved to `94818007c9cc` by the v0.5.2 erratum E2
  Gaucher `variant_spectrum` grade-completeness fix — exactly one dossier changed, downstream byte-identical);
  R2 gate **PASS 7/7**.
- **R3** burden order deterministic (burden-set sha `0f788821e0fc`, gate re-runs the builder 2×); R3 gate
  **PASS 9/9**. 17 of 35 diseases placed (>= 3 of 5 axes scored), 18 reported as not-placed. HONEST: only
  onset is registry-grade for most diseases; progression/severity/mortality/disability are mostly `[H]`
  inferences from the cited definition text, so the order is a provisional prioritization device pending a
  registry natural-history pass (see `reports/R3_NOTES_AND_HANDOVER.md`).
  All disease data is provenance- and grade-tagged; no grade appears without its evidence
  (cited source for `[L]`/`[H]`, named obstacle for `[O]`); nothing is guessed.
- **R4** treatment survey deterministic (treatments sha `f5ba4f0e438d`, residual sha `d41d4e95b8b1`; gate
  re-runs both builders 2×); R4 gate **PASS 11/11**. 35/35 diseases graded for treatment mechanism on a
  two-tier `[H]` basis (12 in-package cited definition, 23 curated standard-of-care), **12/12 definition-tier
  rows text-corroborated**; no row claims `[L]` and no disease is assigned a fabricated cure. Residual (post-
  treatment) burden re-ranks the 17 placed diseases by `raw_burden · (1 − e)` with the banked R3 `raw_burden`
  gate-verified unchanged; residual grade `[H]`. The accession-dated treatment `[L]` pass (FDA label /
  GeneReviews / OMIM / Orphanet) is the documented deferred validation path (see
  `reports/R4_NOTES_AND_HANDOVER.md`).
- **CONSOLIDATION** gate **PASS 10/10** (`reports/consolidation.gate.json`) — the explicit R→W pivot. It
  subsumes R1–R4 (re-runs every investigation gate, asserts each PASSes) and independently re-derives, across
  the four curated datasets, that the cohort identity is one stable 35-CUI set, that every graded field carries
  a source (non-`[O]`) or a named obstacle (`[O]`) with `[L]`/`[V]` dossier sources carrying a date/accession,
  that the `_cohort_index` grade summary has no drift, that inheritance/mechanism/gene agree across
  `disease_index`/dossiers/treatments/burden, that the cohort is scope-clean and every index exclusion is
  logged, that the Erratum-E1 gene_function symbol sweep holds, that no fabricated cure is asserted, and that
  the engine pin is drift-0. **Project is cleared for Phase W1** under the recorded provisional-order condition
  above. Writes no whitepaper prose. Living code (`code/pipeline/consolidation_gate.py`); not in the frozen pin.
