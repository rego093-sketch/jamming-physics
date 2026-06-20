# R4 — investigation notes & handover

**Phase:** R4 (treatment-mechanism survey + residual-burden offset over the 35 dossiers) — **investigation only, no whitepaper prose.**
**Status:** complete and banked. R4 gate **PASS (11/11)**; R3 gate still **PASS (9/9)** after R4. Clean handover point.
**Governing standard:** VP-SPEC v1.8 (authoring discipline switches on at Phase W1, not yet).

---

## Read this first — the one honest limitation that frames everything

The treatment evidence is **`[H]`, not `[L]`.** No accession-dated registry/label source is pulled in R4. Every
one of the 35 therapy assignments is graded `[H]` (inference from a cited in-package source or established
clinical science, with the basis recorded), and **no row claims `[L]`.** Evidence comes from two declared tiers:

| tier | n | what backs the row | strength |
|---|---|---|---|
| `[H]` **definition** | 12 | the in-package, already-`[L]`-cited MedGen `clinical_definition` itself discusses the therapy + effect; the builder independently re-reads it and records the matched phrase | strongest `[H]` (anchored to cited in-package text) |
| `[H]` **standard_of_care** | 23 | the established SoC therapy class from `methodology/treatment_rules.csv` — named modality + mechanism + source **class** (GeneReviews Management / FDA label / OMIM clinical management), accession deferred | knowledge-anchored `[H]` |

**The validation / upgrade path is a dedicated accession-dated `[L]` treatment pass** (pull the specific FDA
label, GeneReviews "Management"/"Treatment of Manifestations" section, OMIM clinical management, or Orphanet
record for each therapy and pin the accession + date) **before** any W-phase prose treats the residual order as
more than provisional. This is the exact analogue of R3's deferred natural-history registry pass — and it is
stated up front for the same reason: the curated table encodes established clinical knowledge faithfully and
nothing is fitted to a ranking, but knowledge-anchored assignment is precisely *why* an independent labelled
source must confirm (or correct) each `[H]` class. None of this is a reason to distrust the *mechanics*: every
row is graded, every basis is recorded, the offset and the residual composite fall out deterministically, and
the 12 definition-tier rows are corroborated against real in-package text (gate-enforced 12/12).

---

## What R4 produced (all reproducible, all grade-tagged; living code, not in the frozen manifest)

### Deliverable 1 — `data/curated/treatments.{csv,json}` (schema `disease_wp.treatments/v1`)
The ROADMAP R4 deliverable. **35 diseases**, each with the established disease-directed therapy (`modality`),
its `mechanism` **stated only where mechanistically established** (constitution C-D3), an `evidence_status`, and
the efficacy offset `e` it maps to. Core columns are exactly the ROADMAP contract
(`entity, modality, mechanism, evidence_status, grade, provenance`); extended columns carry the gene, CUI, `e`,
`R_treat`, tier, the runtime-corroboration result, the source class, and the deferred-`[L]` obstacle.
- **Runtime corroboration (no drift, like R2's runtime-validated `omim_join_supplement`).** The builder
  independently re-reads each dossier's `clinical_definition` and records whether it contains a
  treatment-efficacy phrase (boolean + matched phrase + category). **All 12 definition-tier rows corroborate**
  (the gate fails otherwise); the matched phrase is each row's recorded basis.
- **`evidence_status` distribution:** disease-modifying substantial 21 / partial 9 / symptomatic 3 / none 2.
- **`none` is a positive `[H]` finding** (no disease-directed therapy alters the course), distinct from `[O]`
  (therapy undetermined): **NPD-A** (ERT is approved for non-CNS ASMD but the lethal neurologic course is *not
  amenable* — text-corroborated by "may not be amenable to ERT") and **perinatal-lethal achondrogenesis type
  II**.
- **Conservatism (no fabricated cure, C-D3): no disease is assigned `curative`** at the disease level. HSCT,
  organ transplant, and gene addition are real for several of these diseases but are donor-/timing-/genotype-
  limited rather than the universal standard of care; assigning `curative` would overstate residual benefit.
  The strongest class used is **disease-modifying (substantial)**.
- **Offset map `e` — single source of truth** (in the builder, re-derived by the gate): curative 0.85 /
  substantial 0.55 / partial 0.30 / symptomatic 0.10 / none 0.00; `R_treat = 1 − e`. **treatments sha
  `f5ba4f0e438d`.**

### Deliverable 2 — `data/curated/burden_residual.{csv,json}` (schema `disease_wp.burden_residual/v1`)
The clinically relevant order: what is left **after** best available therapy.
- Reads the **banked R3 `raw_burden` UNCHANGED** (the gate verifies it is not mutated) and applies
  `burden_score = raw_burden · (1 − e)`.
- **Re-ranks the 17 placed diseases** by residual `burden_score`; the 18 not-placed stay not-placed
  (`rank = null`). The placed set is exactly the R3 rankability cut (`axes_scored ≥ 3`) — therapy adds no
  burden axes.
- **Residual grade is now `[H]`** (was `[O]` in R3 while treatability was deferred): the floor of the burden-
  axis present-grade and the `[H]` treatability grade.
- **residual sha `d41d4e95b8b1`.**

### The headline result — pre-treatment vs residual order
The re-ranking does exactly what it should: **untreatable diseases rise, effectively-treated diseases fall.**

| residual rank | disease | R3 raw rank | Δ | `e` | residual |
|---|---|---|---|---|---|
| 1 | Achondrogenesis type II | 1 | · | 0.00 | 0.917 |
| 2 | Niemann-Pick type A | 5 | +3 | 0.00 | 0.700 |
| 3 | alpha-thalassemia | 4 | +1 | 0.10 | 0.660 |
| 4 | Becker muscular dystrophy | 15 | +11 | 0.10 | 0.504 |
| 5 | Osteogenesis imperfecta | 10 | +5 | 0.30 | 0.448 |
| 6 | Duchenne muscular dystrophy | 12 | +6 | 0.30 | 0.441 |
| 7 | Fabry disease | 14 | +7 | 0.30 | 0.394 |
| 8 | Tyrosinemia type I | 2 | −6 | 0.55 | 0.368 |
| … | (full table in the CSV) | | | | |

The two genuinely untreatable diseases hold the top; the symptomatic-only diseases (Becker MD +11,
alpha-thalassemia) rise; the substantially-treated metabolic diseases drop hard (Tyrosinemia I −6, classic
homocystinuria −7, cystic fibrosis −5, Hurler/Gaucher/Pompe −5). This is the inversion R3's handover
anticipated.

### Residual sensitivity — no single weighting presented as truth
Residual order recomputed under the five R3 weightings, Spearman vs the equal-weight residual default over the
placed order: **equal 1.00, onset-heavy 0.980, mortality-heavy 0.976, severity-heavy 0.985,
drop-disability 0.993. The residual order is stable under reweighting** (and slightly *more* stable than the R3
raw order, because the offset compresses the spread).

### Lexicon — `methodology/TREATMENT_LEXICON.md` (generated from the builder SSOT)
The treatment-efficacy detection `PATTERNS` (modality / efficacy / efficacy-negative categories), emitted as
documentation from the single source of truth in `code/pipeline/r4_treatment_survey.py`. Used **only** to
confirm a definition-tier row's cited text discusses therapy — **not** to infer the efficacy class. The 23 SoC-
tier definitions correctly do **not** match (which is exactly why they need the curated table). Regenerated on
every build; never hand-edited.

### Investigation gate (`reports/r4.gate.json`) — **PASS (11/11)**
`treatments_graded_no_guess` · `evidence_status_in_vocab` · `efficacy_offset_correct` ·
`definition_corroboration_consistent` · `residual_composite_correct` · `raw_burden_unchanged_from_R3` ·
`residual_ranking_deterministic_2x` · `cohort_complete_35` · `treatability_no_fabricated_cure` ·
`residual_sensitivity_present` · `engine_pin_drift_zero`. The gate independently re-derives the offset map and
the residual composite, **re-executes both builders twice** to assert determinism (rather than trusting a
recorded digest), confirms R3's `raw_burden` is read unchanged, and re-verifies the governed engine pin.

---

## Confirmed, reusable findings (so the next session does not re-derive them)

- **The two-tier split is empirically clean, not a convenience.** Scanning all 35 cached definitions for
  treatment language, **only the 12 definition-tier diseases match and all 23 SoC-tier diseases do not** — the
  SoC-tier diseases' MedGen blurbs describe untreated natural history only (Wilson, Gaucher, Fabry, Hurler,
  hemochromatosis, CAH, homocystinuria are famously treatable yet their definitions are silent on therapy).
  This is *why* a curated layer is necessary: pure definition-extraction would have marked them treatability-
  `[O]` and defeated R4's purpose.
- **The efficacy class is a declared judgment, the regex only confirms cited text.** The class lives in
  `treatment_rules.csv` (graded `[H]`); the lexicon is a corroboration check, not a class-inference. Keep this
  separation when the `[L]` pass arrives — the labelled source confirms/repairs the *class*, the corroboration
  check stays as in-package anchoring.
- **`R_treat` is now live and `[H]`.** The R3 no-op (`R_treat = 1.0`, `[O]`) is replaced; the residual
  `burden_score` is meaningful. Use `burden_residual.{csv,json}` for the clinically relevant order and
  `burden_scores.{csv,json}` for the pre-treatment order — both are legitimate, answering different questions.
- **R3 is fully intact.** R4 is strictly additive: it reads `burden_scores.json` and writes new files; it never
  touches the R3 builder, gate, or artifacts. `reports/r3.gate.json` re-runs **PASS 9/9**, and the gate's
  `raw_burden_unchanged_from_R3` check proves every residual record's `raw_burden` equals the R3 banked value.
- **Determinism holds across runs** (date pinned `RETRIEVED=2026-06-17`, manual Spearman, no scipy). treatments
  sha `f5ba4f0e438d`, residual sha `d41d4e95b8b1`.

---

## Known limitations carried forward (all transparent and graded)

1. **Treatment evidence is `[H]`, not `[L]`** (see the framing section). The accession-dated `[L]` treatment
   pass is the upgrade path. This is the single most important caveat.
2. **R3's P/S/M/D limitation still stands underneath.** The residual order inherits R3's `[H]` burden axes; the
   natural-history registry pass (R3 handover) is still owed. Two deferred `[L]` passes therefore gate W1: the
   **treatment** accession-dating (R4) and the **natural-history** registry pass (R3).
3. **No curative class by design.** Where a one-time definitive option genuinely exists for a *subset* (HSCT for
   Hurler/Gaucher, gene therapy for hemophilia B / sickle), it is recorded inside the modality text but the
   disease-level class stays disease-modifying. The `[L]` pass can revisit whether any disease's *standard of
   care* has become curative (this changes fast — e.g. gene therapies).
4. **Mechanism stated only where established.** For the genuinely supportive-only diseases (EDS classic, Becker
   MD) `mechanism_established = no` and the text says "supportive only" rather than asserting a mechanism
   (C-D3).

---

## Next session — the consolidation gate, then Phase W1

R1–R4 investigation is now **complete** (disease universe → enrichment/dossiers → burden order → treatment
survey + residual order). Per `ROADMAP.md`, the next step is the **▣ CONSOLIDATION GATE** ("stop investigating,
start writing"), and only after it passes does **Phase W1** authoring begin under full VP-SPEC v1.8 discipline.

Recommended order for the next session:
- **Run the consolidation gate** against the R1–R4 deliverables (provenance-complete, scope-locked, grade-
  complete, reproducible). Decide explicitly whether the two deferred `[L]` passes are prerequisites for W1 or
  are scheduled as early-W tasks with the order flagged provisional in the prose.
- **The two deferred `[L]` passes** (each lifts a provisional `[H]` order toward registry-locked):
  1. **Treatment accession-dating** — pin each of the 35 therapies to an FDA label / GeneReviews "Management" /
     OMIM clinical management / Orphanet accession + date; upgrade `treatments.csv` grades from `[H]` to `[L]`
     where confirmed, correct any class the labelled source contradicts.
  2. **Natural-history registry pass** (R3) — lift P/S/M/D from `[H]` to `[L]`/`[V]`.
- Do **not** start whitepaper prose until W1. R4 (like R1–R3) is investigation only.

### Run order (R4, for reference / re-banking)
```
python3 code/pipeline/r4_treatment_survey.py   # builds treatments.{csv,json} + TREATMENT_LEXICON.md
python3 code/pipeline/r4_burden_residual.py    # builds burden_residual.{csv,json} (reads R3 raw_burden unchanged)
python3 code/pipeline/r4_gate.py               # writes reports/r4.gate.json  -> PASS (11/11)
```
The R4 pipeline is **living code** (post-dates the R2 freeze) and is intentionally **not** in
`MANIFEST_governed.sha256`; the governed engine set is unchanged (drift 0, 15/15).

---

## Erratum E1 — FAH gene resolution (RESOLVED, v0.5.1)

While reading the cohort dossiers, one R2 artifact error was found, and it has since been fixed under PI
direction. Recorded here in full for the audit trail.

**Symptom.** The **Tyrosinemia type I** dossier's `gene_function` block resolved the symbol **FAH** to Entrez
**2175 (FANCA, Fanconi anemia)** instead of FAH's correct ID **2184 (fumarylacetoacetate hydrolase)**, so that
one RefSeq-summary narrative was FANCA's, not FAH's.

**Root cause.** `code/pipeline/r2_cohort_gene_resources.py:gene_info()` resolved a symbol via NCBI
`esearch db=gene` with `FAH[sym] AND Homo sapiens[orgn]` and then blindly took `ids[0]`. The `[sym]` index also
matches historical aliases of *other* genes: "FAH" is a legacy alias (FA-H) of **FANCA**, so the query returned
two records — `['2175', '2184']`, FANCA first — and `ids[0]` picked FANCA. (Verified live: FANCA aliases include
`FA, FA-H, FA1, FAA, FACA, FAH, FANCH`.) Only the gene-narrative was affected; the ClinVar `variant_spectrum`
used a separate `FAH[gene]` ClinVar query, which did **not** collide (FAH=940 records vs FANCA=7144), so those
counts were always correct.

**Fix (root cause, not a hand-edit).**
1. `gene_info()` now selects the candidate whose **official symbol** (`esummary` `name`) exactly equals the
   query symbol, instead of `ids[0]`; if no candidate's official symbol matches, it records an obstacle rather
   than guessing. This hardens *every* cohort gene against the same alias-collision class, not just FAH.
2. The stale FAH cache entry in `data/raw/clinvar/cohort_gene_resources.json` was deleted and the builder
   re-run, so the corrected entry (geneid 2184, `fumarylacetoacetate hydrolase`, authentic NCBI RefSeq summary
   — "...Implicated in tyrosinemia type I.") is a genuine **builder output**, not a manual patch. ClinVar block
   re-fetched identical (total 940).
3. Dossiers regenerated: **exactly one file changed** (`tyrosinemia_type_i.json`); the other 34 are
   byte-identical. The dossier-set sha moved `aba06f038e4d -> b70b12d01e75` (expected and documented).

**Containment verified.** Downstream digests are **unchanged** (burden_scores, treatments, burden_residual all
byte-identical), because no R3/R4 stage reads `gene_function`. After the fix, **all gates re-pass**: R1 5/5,
R2 7/7, R3 9/9, R4 11/11; engine pin drift 0 (15/15). The corrected `gene_function` is graded `[L]` with source
`NCBI Gene:2184 RefSeq Summary; retrieved 2026-06-17`.

**Residual recommendation.** At the consolidation gate, run a one-pass sweep re-verifying every dossier's
`gene_function` official symbol == the cohort gene symbol (the new `gene_info()` guard already enforces this on
rebuild, so the sweep is a confirmation, not a re-resolution).
