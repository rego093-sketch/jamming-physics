# TREATMENT_INDEX — treatment-mechanism survey & residual-burden offset  *(Phase R4 — finalized)*

## Purpose and honest framing

Phase R3 produced a deterministic **pre-treatment** burden order (`raw_burden`). The clinically relevant
quantity, though, is *residual* burden — what is left **after** the best available therapy. R4 surveys, for
each of the 35 cohort diseases, the established disease-directed therapy, its mechanism (stated **only when
mechanistically established**, constitution C-D3), and an `evidence_status` that maps to a fixed efficacy
offset `e`. The offset turns `raw_burden` into a residual `burden_score = raw_burden · (1 − e)`.

This is **investigation only** (no whitepaper prose). It is also, like the R3 burden axes, an **`[H]`-grade
device, not a registry-locked clinical-evidence ranking.** The one honest limitation is stated up front below
and is the analogue of R3's "only onset is `[L]`" caveat.

> **The single honest limitation.** No `[L]` registry/label source is pulled in R4. Treatment evidence comes
> from two `[H]` tiers (below): in-package **cited-definition** statements, and a curated **established
> standard-of-care** table. The grade is uniformly `[H]` (inference from established science / cited text,
> basis recorded), **never `[L]`**. Pinning each therapy to an accession-dated source (FDA label, GeneReviews
> "Management"/"Treatment of Manifestations", OMIM clinical management, Orphanet) is the **`[L]` validation
> pass** — the precondition for any W-phase prose to treat the residual order as more than provisional. This
> mirrors exactly how R3 deferred the natural-history registry pass for P/S/M/D.

## Evidence tiers (declared precedence; recorded on every row)

For each disease the survey takes the **first** applicable basis and records the tier, grade, and exact basis:

1. **`[H]` definition** — the **in-package, already-`[L]`-cited** MedGen `clinical_definition` discusses the
   therapy and its effect. The matched phrase is recorded verbatim as the basis (detection patterns in
   `methodology/TREATMENT_LEXICON.md`, generated from the builder SSOT). This is the **strongest** `[H]` tier:
   it is anchored to a cited source already inside the package. (12 / 35 diseases.)
2. **`[H]` standard-of-care** — where the definition is silent or under-specifies, the established
   standard-of-care therapy class is assigned from the curated table `methodology/treatment_rules.csv`. The
   row records the **named therapy/modality**, the **mechanism where established**, the source **class**
   (GeneReviews "Management" / FDA label / OMIM clinical management) **without a fabricated accession**, and
   the obstacle `obstacle_for_L` naming the deferred accession-dated verification. This is a weaker,
   **knowledge-anchored** `[H]`: it is an inference from established clinical science, not a registry figure.
   (23 / 35 diseases.)
3. **`[O]` open** — reserved for a disease where the established therapy is genuinely undetermined and any
   assignment would be a guess. (None required for this well-characterized cohort; genuinely **untreatable**
   diseases are *not* `[O]` — they are `evidence_status = none`, `e = 0`, a positive `[H]` statement that no
   disease-directed therapy exists, e.g. perinatal-lethal achondrogenesis type II.)

**Runtime corroboration (no drift, like R2's runtime-validated supplement).** The builder independently
re-reads each dossier's `clinical_definition` and records whether it contains a treatment-efficacy phrase
(boolean + matched phrase). Every `definition`-tier row **must** corroborate (the gate fails otherwise); the
matched phrase is the row's recorded basis. The efficacy **class** itself is the declared judgment in
`treatment_rules.csv` (graded `[H]`), not a regex inference — the regex only confirms the cited text discusses
treatment here, anchoring the `definition`-tier rows to real in-package text.

## Efficacy offset `e` (BURDEN_INDEX.md, reproduced) and residual factor

| `evidence_status` | meaning (declared, by clinical effect on natural history) | offset `e` | `R_treat = 1 − e` |
|---|---|---|---|
| **curative** | one-time / definitive normalization that resolves the disease | 0.85 | 0.15 |
| **disease-modifying (substantial)** | converts an otherwise fatal/severe course into substantially normalized survival or function, or normalizes the primary defect | 0.55 | 0.45 |
| **disease-modifying (partial)** | meaningfully slows / reduces, but the disease still progresses significantly | 0.30 | 0.70 |
| **symptomatic** | manages symptoms / supportive only; does not alter the disease trajectory | 0.10 | 0.90 |
| **none** | no established disease-directed therapy (incurable, no modifier) | 0.00 | 1.00 |

The class is assigned by the **declared rule in the middle column**, applied uniformly and recorded per row —
**not** chosen to produce any ordering (no-tuning). **Conservatism:** no disease in this cohort is assigned
`curative` at the disease level, because the definitive options (HSCT, organ transplant, gene addition) are
donor-/timing-/genotype-limited rather than the universal standard of care; assigning `curative` would
overstate residual benefit. The strongest class used is `disease-modifying (substantial)`.

## Residual composite and re-ranking

```
burden_score = raw_burden · R_treat = raw_burden · (1 − e)
```

`raw_burden` is read **unchanged** from the banked R3 deliverable `data/curated/burden_scores.json` (R4 does
**not** mutate R3). The **placed** set (the R3 rankability cut `axes_scored ≥ 3`) is unchanged — therapy adds
no burden axes — but the placed diseases are **re-ordered by residual `burden_score`** (the clinically
relevant order). The 18 not-placed diseases stay not-placed (`rank = null`). A second sensitivity pass
recomputes the residual order under the five R3 weightings.

## Grade of each treatment row (VP-SPEC C3 / constitution C-D3)

- **`[H]`** — every assigned therapy in this cohort (both tiers). Definition-tier basis = matched in-package
  phrase; standard-of-care-tier basis = named therapy + source class, accession-dated `[L]` verification
  deferred.
- **`[O]`** — open/undetermined therapy (none needed here).
- `evidence_status = none` is a **positive `[H]` finding** (no disease-directed therapy exists), distinct from
  `[O]` (therapy undetermined). C-D3: no cure is fabricated; the genuinely untreatable (e.g. NPD-A's lethal
  neurologic course, achondrogenesis type II) are recorded as `none` with the obstacle named.

## Medical-safety scope (constitution C-D4)

Modality and mechanism are described at the level of *how the therapy works*. **No dosing, no individualized
advice, no diagnosis.** Clinical decisions belong to qualified clinicians. This survey is a research-coverage
prioritization device, not clinical guidance.

## Reproducibility (why this satisfies C1)

- The curated table, the detection lexicon, the offset map, the residual composite, and the re-ranking rule
  are fixed and deterministic: same dossiers + same `treatment_rules.csv` → same `treatments.csv` → same
  residual order.
- `r4_treatment_survey.py` prints a `treatments sha256`; `r4_burden_residual.py` prints a `residual sha256`.
  `r4_gate.py` re-executes both builders twice and asserts the digests are identical.
- Inputs are cited per row; the *survey + residual composition* is the package's reproducible contribution,
  the *clinical facts* are observed/established values (C-D1).
- The R4 pipeline is **living code** (post-dates the R2 freeze) and is **not** part of
  `MANIFEST_governed.sha256`; the governed engine pin is re-verified drift-0 each session.

## A note on the curated table (no-tuning honesty)

`treatment_rules.csv` encodes the established standard-of-care therapy class for each disease from clinical
knowledge. The no-tuning invariant is respected in the sense that matters: the efficacy class follows the
declared natural-history rule above, the basis (named therapy, mechanism where established) is recorded, the
grade is the honest `[H]`, and nothing is fitted to a desired residual order. But knowledge-anchored
assignment is exactly **why the accession-dated `[L]` pass (FDA label / GeneReviews / OMIM management /
Orphanet) is the validation path** — an independent labelled source must confirm (or correct) each `[H]` class
before the residual order is treated as anything more than a provisional prioritization device.
