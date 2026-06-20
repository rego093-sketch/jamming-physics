# BURDEN_INDEX — a deterministic, reproducible "suffering order"  *(Phase R3 — finalized)*

## Purpose and honest framing

The author asked for diseases ordered "by how much they make people suffer." Subjective suffering is
individual and not directly measurable. So this whitepaper does **not** rank suffering itself. It defines a
**structured burden proxy**: a transparent, deterministic score built from *observable, published* clinical
attributes. The ordering it produces is a **prioritization device for whitepaper coverage and triage**, and is
explicitly **not** a value judgment about any patient or a claim about anyone's inner experience.

This framing is a scientific scoping decision, and it is what makes the index honest and reproducible — not a
hedge. Under VP-SPEC C1, the *index* is a deterministic function of cited inputs; the inputs themselves are
*observed* values (respected and cited, never "reproduced").

## Components (each normalized to [0, 1]; higher = greater burden)

| symbol | component | bins → value (deterministic) |
|---|---|---|
| **O** | onset earliness (more life-years affected) | congenital/neonatal 1.0 · infantile 0.85 · childhood 0.7 · juvenile 0.55 · adult 0.35 · late-adult 0.2 |
| **P** | progression | static 0.2 · slowly progressive 0.5 · rapidly progressive 0.8 · lethal-progressive 1.0 · *variable spectrum 0.5* |
| **S** | symptom / pain severity | mild 0.25 · moderate 0.5 · severe 0.75 · profound 1.0 · *variable spectrum 0.5* |
| **M** | mortality (life-expectancy impact) | normal 0.0 · near-normal+qualified-risk 0.4 · severely-reduced/premature 0.7 · *variable spectrum 0.7* · early-lethal 1.0 |
| **D** | functional disability | independent 0.2 · partial support 0.5 · high support 0.75 · fully dependent 1.0 |

Tier values are fixed *a priori* by clinical meaning. They are **not** chosen to produce any particular
ordering: each disease's value falls out deterministically from which tier its cited text matches.

## Realized per-axis sourcing precedence (what the builder actually does)

For each axis the builder takes the **first** source that is available, in this strict order, and records the
grade and the exact basis (matched phrase / HPO term) on every value:

1. **[L] registry** — a structured HPO annotation, where one exists. Onset uses HPO C-aspect onset terms
   (`code/pipeline/r3_burden_index.py` → `score_onset`); progression uses HPO Clinical-course (aspect C);
   mortality uses the HPO Mortality/Aging subtree (HP:0040006). These are *observed inputs*, cited to
   `phenotype.hpoa v2026-06-06`.
2. **[H] cited-text inference** — a value read from the cited MedGen `clinical_definition` by a **declared,
   fixed lexicon** (`methodology/BURDEN_LEXICON.md`, generated from the `PATTERNS`/classifier SSOT in the
   builder). The matched phrase is recorded verbatim as the basis.
3. **[O] open** — when neither a registry annotation nor a definition phrase is present, the axis is left
   unscored, the obstacle is named, and the value is **never guessed**.

**Honest limitation (front and centre).** Of the five axes, only **onset** is registry-grade for most of the
cohort. The HPO Clinical-course / Mortality branches are sparse (progression annotated for 1/35 diseases,
mortality for 3/35), and HPO has **no** severity or disability magnitude branch. Consequently **P, S, M, and D
are, for most diseases, `[H]` inferences from the cited definition text**, not `[L]` registry figures. The
ordering is therefore an **`[H]`-grade provisional prioritization device**, not a registry-locked ranking. The
validation/upgrade path is a dedicated natural-history registry pass (Orphanet natural history + clinical
synopsis, OMIM clinical synopsis, GBD/published survival curves) to lift P/S/M/D to `[L]`/`[V]` **before** any
W-phase prose locks the order. See the R3 handover.

## Refinement rules (declared; each produces an `[H]` value with its basis recorded)

- **Mortality refinement of a coarse HPO flag.** HPO Mortality/Aging annotations encode phenotype
  *presence* (often at low/uncertain frequency, e.g. "Death in infancy" 1/1), not lifespan *magnitude*. When
  the cited definition states an explicit lifespan-bounding fact — a near-normal-lifespan claim, a qualified
  complication risk, or a variable lethal-to-normal spectrum — that statement **refines** the HPO presence
  flag, and the value is graded `[H]` with the HPO term noted as corroboration. (E.g. achondroplasia: HPO
  "Death in infancy" present, but the definition states "life span … near normal" with a qualified
  craniocervical "risk of death in infancy" → M = 0.4 `[H]`, not 1.0.)
- **Mortality reads untreated natural history.** Treatment benefit is deferred to `R_treat` (R4), so an
  explicit *untreated* lethality statement ("death in the untreated child usually occurs before age ten
  years") is scored in M even when the same definition reports a high *treated* survival rate.
- **Severity / progression spectra.** When a definition explicitly states a within-entity range — both a
  mild/slow end and a severe/fatal end, or variability predicated of the entity's severity/phenotype, or an
  explicit "ranges from X to Y" — the axis is scored at the midpoint (0.5 for S and P; 0.7 for the
  lethal-inclusive M spectrum). A bare "continuum"/"spectrum" word that names a *parent classification* (while
  the entity is one pole of it) does **not** trigger the spectrum rule, and comparative references to *other*
  forms ("more severe forms of X") do not anchor X's own severity.

## Composite

```
raw_burden   = mean of the axis values that are actually scored        # missing axis EXCLUDED, never imputed
burden_score = raw_burden · R_treat                                    # treatability lowers residual burden
```

The composite is a **renormalized mean over present axes** (equivalently, equal weights restricted to the
scored axes). A missing axis is excluded rather than imputed to 0 (which would silently penalize) or to any
filled value (which would be a guess). **Default weights (declared, equal):**
`w_O = w_P = w_S = w_M = w_D = 0.20`, recorded in the gate output.

## Treatability offset (reduces *residual* burden) — deferred to R4

| `evidence_status` | efficacy offset `e` |
|---|---|
| curative / effectively normalizing | 0.85 |
| disease-modifying (substantial) | 0.55 |
| disease-modifying (partial) | 0.30 |
| symptomatic only | 0.10 |
| none (incurable, no modifier) | 0.00 |

Residual factor `R_treat = 1 − e`, sourced from R4 `treatments.csv`. **R4 is not yet built**, so in R3 every
record carries `R_treat = 1.0` graded `[O]` (obstacle: treatability deferred), and `burden_score == raw_burden`
floored to `[O]`. **The primary order is the pre-treatment `raw_burden`** (the quantity that is actually
populated in R3); the post-treatment `burden_score` becomes meaningful only once R4 lands.

## Grade of each score (VP-SPEC C3 honesty)

Every component value carries a grade tied to its evidence:
- **[L]** — registry-stated and cited (an HPO annotation; an observed input).
- **[H]** — inference from the cited MedGen `clinical_definition`; the matched phrase is recorded as basis.
- **[V]** — derived from a quantitative published distribution (reserved; **none used in R3**).
- **[O]** — open/unavailable; the obstacle is named; the value is not guessed.

**Floor rule.** Two floor grades are reported per disease (floor order **[O] < [H] < [L] < [V] < [F]**):
`grade_floor` = min over **all five** axis grades (so any unscored axis makes it `[O]`, the spec-faithful
"only as trustworthy as its weakest input"); `grade_present` = min over the **scored** axes only (the
trustworthiness of the value that was actually computed). For most of the cohort `grade_floor = [O]` (an axis
is missing) while `grade_present = [H]`.

## Rankability (which diseases are *placed* in the order)

`raw_burden` is a renormalized mean over the scored axes; a mean over fewer than a majority of the five axes is
not a meaningful aggregate (a disease scored on onset alone would read 1.00 from a single axis and crowd the
top). One fixed, declared threshold is therefore applied:

```
rankable = (axes_scored >= 3)        # majority of 5
```

Only **rankable** diseases are placed in the ordered suffering-order (contiguous ranks 1..N, `raw_burden`
non-increasing). Diseases with 1–2 scored axes are reported separately as **"not placed — insufficient axis
coverage"** with `rank = null`. This is a declared coverage cut, **not** a tuned parameter.

## Sensitivity (no single weighting presented as truth)

The builder recomputes the order under five weightings — equal (default), onset-heavy, mortality-heavy,
severity-heavy, and drop-disability (core-4) — and reports the Spearman rank correlation of each against the
default, computed over the **placed** order. (R3 run: equal 1.00 by construction; the other four 0.94–0.97,
i.e. the order is stable under reweighting.)

## Reproducibility (why this satisfies C1)

- Binning, lexicon, classifier, weights, composite, floor, and rankability rule are fixed and deterministic:
  same dossier inputs → same scores → same order.
- The builder prints a `burden-set sha256` over its emitted artifacts; the R3 gate (`code/pipeline/r3_gate.py`)
  re-executes the builder twice and asserts the digest is identical (verified PASS this phase).
- Clinical inputs are cited per row (HPO `phenotype.hpoa v2026-06-06`; MedGen `clinical_definition` per the R2
  dossiers). The *index* is the package's reproducible contribution; the *inputs* are observed values.
- The R3 pipeline is **living code** (it post-dates the R2 freeze) and is intentionally **not** part of
  `MANIFEST_governed.sha256`.

## A note on lexicon development (no-tuning honesty)

The `[H]` lexicon was developed by reading **this cohort's** definitions and writing regex tiers that parse
standard clinical phrasing (onset words, "rapidly progressive", "severe", lethality timing, etc.). This is a
transparent **extraction heuristic developed in-sample**, not an independent oracle. The no-tuning invariant is
respected in the sense that matters: tier values are fixed by clinical meaning a priori, every value is graded
`[H]` with its matched phrase recorded, and nothing is fitted to a desired ranking — the values fall out of the
text deterministically. But in-sample development is exactly why the **registry pass is the validation path**:
an independent natural-history source must confirm (or replace) these `[H]` proxies before the order is treated
as anything more than a provisional prioritization device.

## Explicitly out of this index

- No attempt to weigh one patient's suffering against another's.
- No quality-of-life dollar valuation; no allocation/triage-of-care use — coverage prioritization only.
- Rare-but-mild and common-but-severe are kept distinct (prevalence is *not* folded into burden).

## R6 — natural-history registry pass (Orphanet/Orphadata): the validation path, executed

The "registry pass is the validation path" named above has now been run (phase R6,
`code/pipeline/r6_naturalhistory_registry.py`). It is the methodological upgrade R5 deferred:
where R5 (GeneReviews) could only **corroborate** a definition tier against free chapter text (value frozen),
Orphadata's fields are **structured and entity-anchored** — every value attaches to an ORPHAcode — so a
registry `[L]` here may **supersede** a prior `[H]`/`[O]` and **move `raw_burden`**. The R3/R4 banked files
are untouched; the cumulative R5+R6 registry layer (`data/curated/*_registry.*`) carries the lift.

**Sources (CC BY 4.0, sha-pinned, retrieved 2026-06-17):** `en_product1.xml` (OMIM↔ORPHA cross-refs with
mapping relation), `en_product9_ages.xml` (`AverageAgeOfOnset`), `en_product4.xml` (HPO phenotypes per
ORPHAcode with Orphanet frequency). OMIM clinical synopsis is deliberately NOT used (licensed/copyrighted).

**Declared, a-priori lift rules (no tuning; enforced by `code/pipeline/r6_gate.py`):**

- **JOIN — Exact only.** A disease lifts only from an Orphanet concept its OMIM maps to with relation `E`
  (exact) in `en_product1`. `BTNT`/`NTBT` (broader/narrower) are recorded as context but never lift. Several
  exact ORPHAcodes → their onset/HPO sets are unioned.
- **Onset (O)** ← earliest `AverageAgeOfOnset` category on the **same a-priori earliness scale** as the tier
  table above:

  | Orphanet AverageAgeOfOnset | onset tier O |
  |---|---|
  | Antenatal · Neonatal | 1.0 |
  | Infancy | 0.85 |
  | Childhood | 0.7 |
  | Adolescent | 0.55 |
  | Adult | 0.35 |
  | Elderly | 0.2 |
  | "All ages" · "No data available" | (recorded, **no** tier — does not lift) |

  O is the **earliest** usable category combined with any existing HPO-`[L]` onset; a registry `[L]`
  supersedes a prior `[H]`/`[O]`.
- **Mortality (M)** ← `en_product4` HPO terms under **HP:0040006** (Mortality/Aging) carrying an R3
  `MORT_VAL` tier **and** Orphanet frequency ≥ Frequent. M = most-severe qualifying tier; supersedes.
- **Progression (P)** ← `en_product4` HPO terms under **HP:0031797** (Clinical course) with an R3 `PROG_VAL`
  tier **and** frequency ≥ Frequent. Same supersede rule.
- **Frequency gate** = {Obligate (100%), Very frequent (99–80%), Frequent (79–30%)}. Phenotypes at
  Occasional/Very-rare/Excluded do **not** characterise typical natural history and are ignored (the same
  over-trigger risk that made R5 withhold `[O]`-fill). Declared a priori.
- **Severity (S) / Disability (D)** are **not** lifted: Orphadata carries no structured severity- or
  disability-**magnitude** tier (frequency-annotated phenotypes only). Each open S/D axis records that
  Orphanet was consulted and no tier exists, deferring to the OMIM clinical synopsis (licensed) / GBD /
  published functional & survival literature — never guessed.
- **Add-only / absence-safe.** Orphanet **absence** never downgrades or removes a banked value.

**Result (this cohort).** Onset → registry `[L]` 25→28; mortality `[L]` 7→8 (Hurler only); progression
unchanged (no qualifying course term at ≥Frequent — honest null); S/D unchanged (no Orphadata tier).
Promotions 0 (no not-placed disease reaches ≥3 registry axes without an S/D tier). **`order_locked` 0→1** =
Tyrosinemia type II (its three scored axes O/S/D are all registry-grade): its burden **value** is
registry-locked, while the cohort **order** stays provisional `[H]` (its rank still depends on `[H]`-valued
neighbours). The order is therefore **still a provisional prioritisation device** until S/D/most-P are lifted
from an independent magnitude source — but onset, the one axis that drove most of the order, is now
registry-grade rather than an in-sample lexicon proxy.
