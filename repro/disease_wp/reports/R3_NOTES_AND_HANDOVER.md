# R3 — investigation notes & handover

**Phase:** R3 (reproducible burden ordering — a deterministic "suffering order" over the 35 dossiers) — **investigation only, no whitepaper prose.**
**Status:** complete and banked. R3 gate **PASS (9/9)**. Clean handover point.
**Governing standard:** VP-SPEC v1.8 (authoring discipline switches on at Phase W1, not yet).

---

## Read this first — the one honest limitation that frames everything

The order is a **provisional, `[H]`-grade prioritization device, not a registry-locked ranking.** Of the five
burden axes, only **onset** is registry-grade (HPO) for most of the cohort. The HPO Clinical-course and
Mortality branches are sparse, and HPO has **no** severity- or disability-magnitude branch, so for most
diseases **progression, severity, mortality, and disability are inferred from the cited MedGen definition text
(`[H]`)**, with the matched phrase recorded on every value. Concretely (grade coverage over 35):

| axis | `[L]` registry | `[H]` cited-text | `[O]` open |
|---|---|---|---|
| O onset | 20 | 11 | 4 |
| P progression | 1 | 13 | 21 |
| S severity | 0 | 24 | 11 |
| M mortality | 1 | 16 | 18 |
| D disability | 0 | 8 | 27 |

Because most diseases are missing at least one axis, the spec-faithful composite grade `grade_floor` is `[O]`
for most of the cohort; the value that is actually computed floors to `[H]` (`grade_present`). **The validation
/ upgrade path is a dedicated natural-history registry pass** (Orphanet natural history + clinical synopsis,
OMIM clinical synopsis, GBD / published survival curves) to lift P/S/M/D to `[L]`/`[V]` **before** any W-phase
prose locks the order. The lexicon was developed in-sample against this cohort's definitions (a transparent
extraction heuristic, not an independent oracle) — that is precisely why an independent registry source must
confirm or replace these `[H]` proxies. None of this is a reason to distrust the *mechanics*: every value is
graded, cited, and falls out of the text deterministically. It is a statement about **source strength**, and it
is stated up front so the next phase does not over-read the order.

---

## What R3 produced (all reproducible, all grade-tagged; living code, not in the frozen manifest)

### The deliverable — `data/curated/burden_scores.{csv,json}` (schema `disease_wp.burden_scores/v1`)
- **35 diseases**, each with five graded burden components `{value, grade, source|obstacle}` on the axes
  **O P S M D** (definitions and tier values in `methodology/BURDEN_INDEX.md`).
- **Per-axis sourcing precedence** (strict, recorded on every value): `[L]` HPO annotation where one exists →
  `[H]` value read from the declared fixed lexicon over the cited MedGen `clinical_definition` (matched phrase
  recorded) → `[O]` obstacle named, value **never guessed**.
- **Composite** `raw_burden` = renormalised **mean of the axes actually scored** (a missing axis is *excluded*,
  never imputed). Two floor grades reported: `grade_floor` (min over all 5 axes; any missing → `[O]`) and
  `grade_present` (min over scored axes only).
- **Treatability deferred to R4**: every record carries `R_treat = 1.0`, `[O]` (R4 `treatments.csv` not yet
  built), so `burden_score == raw_burden` floored to `[O]`. **The primary order is the pre-treatment
  `raw_burden`.**
- **Determinism**: the builder prints a `burden-set sha256` over its artifacts; **burden-set sha
  `0f788821e0fc`** (the R3 gate re-runs the builder twice and asserts the digest is identical).

### Rankability — which diseases are *placed*
- Declared majority-coverage threshold: **`rankable = axes_scored >= 3`** (of 5). Only rankable diseases are
  placed in the ordered suffering-order (contiguous ranks 1..N, `raw_burden` non-increasing). Diseases with 1–2
  scored axes are reported separately as **"not placed — insufficient axis coverage"** (`rank = null`).
- This phase: **17 placed, 18 not placed.** The threshold corrects a real artifact — a single-axis disease
  (e.g. EDS type 4, onset-only, would read `raw_burden = 1.00`) otherwise crowds the top of a renormalised
  mean. One fixed declared cut, not a tuned parameter.
- Top of the placed order (pre-treatment `raw_burden`): Achondrogenesis type II 0.917 → Tyrosinemia type I
  0.817 → Classic homocystinuria 0.738 → alpha-thalassemia 0.733 → Niemann-Pick type A 0.700 → … (full table in
  the CSV).

### Sensitivity — no single weighting presented as truth
- Order recomputed under five weightings (equal/onset-heavy/mortality-heavy/severity-heavy/drop-disability),
  Spearman vs the equal default **over the placed order**: equal 1.00 (by construction), onset-heavy 0.949,
  mortality-heavy 0.944, severity-heavy 0.938, drop-disability 0.974. **The order is stable under reweighting.**

### Lexicon — `methodology/BURDEN_LEXICON.md` (generated from the builder SSOT)
- The declared regex tiers (O/P/S/D) plus the mortality classifier, emitted as documentation from the single
  source of truth in `code/pipeline/r3_burden_index.py`. Regenerated on every build; never hand-edited.

### Emergence links (optional `[H]` enrichment)
- Six developmental diseases are mapped to the morphogenesis engine quantity they perturb (achondroplasia →
  growth-plate length scale λ=√(Dτ); ACG2 → diffusion term D; OI → Layer-2 matrix mechanics; Marfan → TGF-β
  morphogen; EDS-classic → collagen fibrillogenesis; EDS4 → vascular matrix), citing the pinned read-only
  baseline `code/emergence_v2/`. (Two stale CUIs — ACG2, EDS-classic — were corrected this phase so all six
  attach.)

### Investigation gate (`reports/r3.gate.json`) — **PASS (9/9)**
`components_graded_no_guess` · `floor_rule_correct` · `composite_renormalised_mean` · `treatability_deferred_R4`
· `weights_recorded` · `ranking_deterministic_2x` · `sensitivity_present` · `cohort_complete_35` ·
`rankability_consistent`. The gate independently re-derives the no-guess rule (every grade carries its evidence)
and **re-executes the builder twice** to assert determinism, rather than trusting a recorded digest.

---

## Confirmed, reusable findings (so the next session does not re-derive them)

- **Only onset is registry-structured** at R2 grade. P/S/M/D are definition-derived `[H]` for most diseases —
  this is a property of HPO's annotation coverage, not a gap in the build. Plan the registry pass accordingly.
- **HPO mortality annotations are presence flags, not magnitudes.** Three OMIMs carry a Mortality/Aging term
  (Achondroplasia "Death in infancy" 1/1; ACG2 "Stillbirth"; Gaucher "Death in infancy" 1/2). The builder's
  **mortality-refinement rule** lets an explicit lifespan-bounding sentence in the definition refine such a flag
  to `[H]` (achondroplasia → M 0.4, Gaucher → M 0.7 spectrum); ACG2 stays `[L]` 1.0 because its definition has
  no bounding statement to refine "Stillbirth".
- **Mortality reads *untreated* natural history.** Treatment benefit belongs to `R_treat` (R4), so an explicit
  untreated-lethality statement is scored even when a high *treated* survival rate is also reported (Tyrosinemia
  type I → M 1.0, from "death in the untreated child usually occurs before age ten years").
- **Spectrum handling is principled.** A within-entity range (both ends stated, or variability predicated of
  severity/phenotype, or "ranges from X to Y") scores the midpoint; a bare "continuum"/"spectrum" word naming a
  *parent classification* does not (NPD-A stays severe 0.75, not a 0.5 spectrum); comparative references to
  *other* forms ("more severe forms of X") do not anchor X's own severity (VWD type 1 → 0.5 from its own
  "vary widely", not 0.75).
- **Determinism holds across runs** (date pinned `RETRIEVED=2026-06-17`, manual Spearman, no scipy). Burden-set
  sha `0f788821e0fc`.

---

## Known limitations carried forward (all transparent and graded)

1. **P/S/M/D are mostly `[H]` definition-inferences** (see the framing section). The order is provisional until
   a registry natural-history pass. This is the single most important caveat.
2. **`R_treat` is a no-op in R3** (R4 not built). The post-treatment `burden_score` is not yet meaningful; use
   `raw_burden`. Several top-ranked diseases are in fact highly treatable when caught early (Tyrosinemia I with
   nitisinone, Pompe with ERT, homocystinuria/PKU/MSUD with diet) — R4 will move them down the *residual*-burden
   order, which is the clinically relevant one.
3. **In-sample lexicon.** Tier values are fixed a priori by clinical meaning and nothing is fitted to a ranking,
   but the regexes were written against this cohort's phrasing. Registry validation is the replacement path, not
   a refinement of the regexes.
4. **18 diseases are not placed** (1–2 axes). They are scored and reported, just not ranked. The registry pass
   will populate more axes and bring most of them above the 3-axis threshold.

---

## Next session — Phase R4 (investigation only)

Per `ROADMAP.md`, R4 is the **treatment-mechanism survey** → `data/curated/treatments.csv`, which finally
populates `R_treat` and turns `raw_burden` into a residual `burden_score`.
- Build `treatments.csv` over the 35 dossiers: per disease, the best available therapy class and an
  `evidence_status` mapped to the efficacy offset `e` in `BURDEN_INDEX.md` (curative 0.85 / disease-modifying
  substantial 0.55 / partial 0.30 / symptomatic 0.10 / none 0.00). Cite each (FDA label, OMIM clinical
  management, GeneReviews "Management"). Grade `[L]` where cited, `[O]` where unknown — **never guessed**.
- Re-run the burden builder so `burden_score = raw_burden·(1−e)` is populated; re-run the sensitivity pass on
  the residual order; extend the gate with a `treatability_graded` check (every `R_treat` carries evidence).
- **Strongly recommended in parallel: the registry natural-history pass** to lift P/S/M/D from `[H]` to
  `[L]`/`[V]` (Orphanet, OMIM clinical synopsis, GBD/survival). This is the precondition for any W-phase prose
  to treat the order as more than provisional.
- Do **not** start whitepaper prose until W1. R3 (like R1/R2) is investigation only.

### Run order (R3, for reference / re-banking)
```
python3 code/pipeline/r3_burden_index.py     # builds burden_scores.{csv,json} + BURDEN_LEXICON.md
python3 code/pipeline/r3_gate.py             # writes reports/r3.gate.json  -> PASS (9/9)
```
The R3 pipeline is **living code** (post-dates the R2 freeze) and is intentionally **not** in
`MANIFEST_governed.sha256`; the R2 governed set is unchanged (drift 0).
