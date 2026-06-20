# TREATMENT_LEXICON — treatment-efficacy detection patterns  *(generated from r4_treatment_survey.py)*

This file is written by `code/pipeline/r4_treatment_survey.py` from its `PATTERNS` constant (the single source of truth), so it cannot drift from the code.

## Role (narrow, by design)

These patterns are used **only** to confirm that a *definition*-tier disease's **already-`[L]`-cited** MedGen `clinical_definition` discusses the therapy and its effect, and to record the **matched phrase** as that row's recorded basis (runtime corroboration). They are **not** used to infer the efficacy class — that class is the declared curated judgment in `methodology/treatment_rules.csv`, graded `[H]`. A *standard-of-care*-tier row does **not** need a lexicon match (its basis is the named curated therapy + source class); the gate requires corroboration **only** for the 12 definition-tier rows.

Matching is case-insensitive; the **first** pattern (top-to-bottom) that hits is recorded with its category and the literal matched substring.

## Categories

- **modality** — a named disease-directed therapy class appears (enzyme replacement, chelation, transfusion, transplantation, a named enzyme-pathway drug, or dietary therapy).
- **efficacy** — the text states that treatment changes the clinical course (managed-course/normalized outcome, treatment-from-onset response, prophylactic/perioperative treatment, treatment-initiation benefit).
- **efficacy_negative** — a named therapy exists but the text states this disease's course is **not amenable** to it (supports an honest `evidence_status = none`, e.g. NPD-A's lethal neurologic course).

## Patterns (single source of truth)

| # | category | basis label | patterns (regex, case-insensitive) |
|---|---|---|---|
| 1 | modality | enzyme replacement therapy | `enzyme[- ]replacement` · `\bERT\b` |
| 2 | modality | chelation therapy | `chelation` · `chelating` · `chelat\w*` |
| 3 | modality | transfusion therapy | `transfusion` |
| 4 | modality | transplantation | `transplantation` · `transplant\b` |
| 5 | modality | small-molecule / enzyme-pathway drug | `nitisinone` · `hydroxyurea` · `cysteamine` · `cystine-depleting` · `sapropterin` · `betaine` · `penicillamine` · `tolvaptan` · `givosiran` · `hemin` |
| 6 | modality | dietary therapy | `low[- ]tyrosine diet` · `low[- ]phenylalanine diet` · `low Phe diet` · `thiamine therapy` · `branched-chain.{0,30}diet` · `methionine-restricted` · `tyrosine.{0,20}restriction` · `dietary.{0,20}restriction` |
| 7 | efficacy | treatment-from-onset response | `treated from birth` · `treated from early infancy` · `diagnosed and treated` · `treatment.{0,20}from early infancy` |
| 8 | efficacy | managed-course / normalized outcome | `with proper management` · `improves prognosis` · `improved survival` · `improved .{0,20}survival` · `survival rate` · `with these treatment interventions` · `remain asymptomatic with continued treatment` |
| 9 | efficacy | prophylactic / perioperative treatment | `prophylactic treatment` · `postoperative treatment` · `pre- and postoperative treatment` |
| 10 | efficacy | treatment-initiation benefit | `initiation of treatment` · `prompt initiation of treatment` · `lowering blood Phe` |
| 11 | efficacy_negative | named therapy not amenable to this course | `may not be amenable to` · `does not (?:alter|reduce|impact)` · `not amenable to ERT` |

## Definition-tier match distribution (this run)

- **modality**: 8 of the 12 definition-tier diseases matched here first.
- **efficacy**: 4 of the 12 definition-tier diseases matched here first.
- **efficacy_negative**: 0 of the 12 definition-tier diseases matched here first.
