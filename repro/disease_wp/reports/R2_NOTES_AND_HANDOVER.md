# R2 — investigation notes & handover

**Phase:** R2 (disease enrichment, mechanism assignment, per-disease dossiers) — **investigation only, no whitepaper prose.**
**Status:** complete and banked. R2 gate **PASS (7/7)**. Clean handover point.
**Governing standard:** VP-SPEC v1.8 (authoring discipline switches on at Phase W1, not yet).

---

## What R2 produced (all reproducible, all provenance- and grade-tagged)

### The ROADMAP R2 deliverable — `data/curated/disease_index.csv`
- **6,170 rows** (6,167 in-scope after boundary review · 3 moved out), every row enriched beyond the R1 scaffold with:
  `inheritance_class / inheritance_grade / inheritance_source`, `mechanism_class / mechanism_grade / mechanism_source`,
  `clinical_definition`, and a new `cns_cross_reference` column.
- **Inheritance** (bulk MedGen esummary over all in-scope CUIs, `code/pipeline/r2_enrich_inscope.py`):
  `[L]` stated = 2,011 · `[O]` not-stated = 4,159 (each `[O]` names the obstacle, never guessed).
- **Mechanism** (`code/pipeline/r2_mechanism.py`): `[L]` = 697 · `[H]` = 1,046 · `[O]` = 4,424.
  Classes: not_curated 4,424 · loss-of-function 1,054 · haploinsufficiency 646 · gain-of-function 15 ·
  dominant-negative 12 · dom-neg/haploinsuff 9 · imprinting 6 · dosage 1.
- Deterministic; **index sha `a274e25a00bb`** (confirmed by repeated identical runs).

### Boundary review (`code/pipeline/r2_boundary_review.py`)
- Conservative CNS-primacy pass. **3 pure-CNS GM2 diseases moved out of scope**, each logged with reason:
  Tay-Sachs (`C0039373`), Tay-Sachs variant AB (`C0268275`), Sandhoff (`C0036161`).
- **31 boundary cases kept in** and annotated with `cns_cross_reference=true` (storage/metabolic diseases with a
  secondary CNS footprint whose primary burden is systemic). All other rows `cns_cross_reference=false`.

### 35 per-disease dossiers (`data/curated/dossiers/<slug>.json`, schema `disease_wp.dossier/v1`)
- Pre-registered cohort (`methodology/dossier_cohort.csv`): **18 flagship + 17 extension**. The strict algorithmic
  rule (single-gene + OMIM + `[L]` mechanism + HPO annotations) yielded 582 — too broad and diluted to curate by
  hand this phase — so the documented cohort is the manifest, with a per-row inclusion rationale.
- Every dossier field is a **graded object `{value, grade, source|obstacle}`** — no bare values anywhere
  (enforced by the gate). Fields: identity (entity/CUI/UID/OMIM codes + source/genes/tier/system_class/in_scope/
  cns_cross_reference); inheritance; molecular_mechanism; gene_function (NCBI RefSeq summary per gene);
  variant_spectrum (ClinVar germline-classification distribution per gene); and clinical
  {organ_systems, cardinal_symptoms, age_of_onset, prevalence, clinical_definition}.
- Field-grade tally (all fields × diseases): `[L]` dominant, with honest `[H]`/`[O]` where the source is silent.
- Deterministic; **dossier-set sha `b70b12d01e75`** (confirmed by repeated identical runs).
  NOTE: was `aba06f038e4d` at R2 closeout; updated by the v0.5.1 erratum E1 (FAH geneid 2175->2184;
  see reports/R4_NOTES_AND_HANDOVER.md). Only tyrosinemia_type_i.json changed; downstream digests identical.
- `_cohort_index.json` carries the cohort roster + the OMIM-join supplement audit.

### Curation artifacts (`methodology/`)
- `mechanism_rules.csv` — **8 curated, cited molecular-mechanism class rules**: collagen → dominant-negative/
  haploinsufficiency; FBN1 → dominant-negative/haploinsufficiency; CFTR → loss-of-function; HBB+sickle →
  gain-of-function; HBB+thalassemia → loss-of-function; Beckwith-Wiedemann/Russell-Silver → imprinting;
  repeat-expansion → repeat; FGFR3 → gain-of-function (constitutive receptor activation; achondroplasia Gly380Arg).
- `dossier_cohort.csv` — the pre-registered 35-disease manifest (cui, entity, tier, system_class, inclusion_rationale).
- `omim_join_supplement.csv` — **cited curation artifact**, 11 rows over 6 concepts, each validated against
  `phenotype.hpoa` at build time, mapping concepts whose MedGen conceptmeta lacks a usable OMIM (or is a
  phenotypic-**series** number) to HPO-name-verified type-level OMIMs. Notable: osteogenesis imperfecta — series
  number `120150` carries **zero** HPO annotations; the phenotypes live on the COL1A1/COL1A2 classic type OMIMs
  (166200 / 166210 / 166220 / 259420), which are unioned in. PKU `261600`; β-thal `613985`; Gaucher umbrella →
  230800/230900/231000; MSUD `248600`; Pompe/GSD-II `232300`.

### Investigation gate (`reports/r2.gate.json`) — **PASS (7/7)**
`inheritance_complete` · `mechanism_graded_no_guess` · `boundary_resolved` · `provenance_complete` ·
`dossier_schema_valid` · `dossier_cohort_complete` · `grade_vocab_consistent`.
The gate independently re-derives the no-guess rule: every grade must carry its evidence — a cited source for
`[L]`/`[H]`, a named obstacle for `[O]`. (This caught a real defect during R2: `[O]` inheritance/mechanism fields
were initially copied into dossiers with the obstacle text mislabeled under `source`; the builder now routes `[O]`
evidence to `obstacle`. Fixed and re-passed.)

---

## Confirmed, reusable findings (so the next session does not re-derive them)

1. **ClinGen dosage scores are cached** at `data/raw/clingen/ClinGen_gene_curation_list_GRCh38.tsv`. Column map:
   col0 = gene, col4 = haploinsufficiency (HI) score, cols6–11 = HI PMIDs, col12 = triplosensitivity (TS) score,
   cols14–19 = TS PMIDs. Counts: **HI=3 (sufficient evidence for haploinsufficiency) = 324 genes**; **TS=3 = 1**;
   **HI=30 (gene associated with AR phenotype) = 533**. The mechanism cascade uses HI=3 → haploinsufficiency `[L]`
   (with PMIDs), TS=3 → dosage `[L]`, and HI=30 as AR corroboration for the recessive → loss-of-function `[H]` step.
2. **Bulk MedGen enrichment path** = MedGen esummary over CUIs; the clean inheritance field is
   `conceptmeta → <ModeOfInheritance><Name>`; OMIM cross-refs are `conceptmeta` entries with `SAB="OMIM"` (parse the
   `Name` value as the MIM). 30/35 cohort concepts had ≥1 conceptmeta OMIM; the other 5 are handled by the
   OMIM-join supplement. Cached responses live under `data/raw/medgen/`; **re-runs do not re-hit NCBI.**
3. **NCBI Gene + ClinVar per-gene cache** at `data/raw/clinvar/cohort_gene_resources.json` (all 40 cohort genes):
   GeneID + RefSeq Summary (gene function; all 40 have summaries) + ClinVar germline-classification distribution
   via `[Germline classification]` esearch filters (P/LP/VUS/LB/B). **These categories overlap and are NOT summed.**
   Example CFTR: GeneID 1080, P=2294 LP=1123 VUS=3616 LB=3160 B=3252, total distinct=6390.
4. **HPO clinical join recipe** (the heart of the dossier clinical block):
   - `data/raw/hpo/phenotype.hpoa.gz` and `data/raw/hpo/hp.obo.gz`, both **version 2026-06-06**
     (`https://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa` and `.../obo/hp.obo`).
   - Join `phenotype.hpoa` by **bare OMIM number** (`database_id` is `OMIM:NNNNNN`; strip the prefix).
   - Aspect codes: `P` = phenotypic abnormality, `C` = clinical course (onset), `I` = inheritance, `M` = modifier.
   - **Organ systems** = roll each `P`-aspect HPO term up to the direct children of `HP:0000118`
     ("Phenotypic abnormality"); those 23 children are the organ-system categories.
   - **Cardinal symptoms** = top-15 `P`-aspect terms by annotated frequency (HPO frequency terms ranked
     HP:0040280..285, plus `n/m` and `%` literals), each carrying its PMID/OMIM reference.
   - **Onset** = `C`-aspect terms under the onset subtree root `HP:0003674`.
5. **Cohort manifest rationale is documented, not arbitrary.** It is pre-registered in `methodology/dossier_cohort.csv`
   precisely because the strict algorithmic selector over-selected (582). When R3+ wants to scale dossiers, widen the
   manifest deliberately; do not silently switch selectors.

---

## Known limitations carried forward (all transparent and graded)

- **Disease-level mechanism for multi-gene / CNV syndromes.** A single ClinGen HI=3 gene can stamp
  "haploinsufficiency" at the disease level even for a duplication syndrome (e.g. 17p11.2 microduplication via RAI1).
  This is ClinGen-sourced and graded `[L]`, but **disease-level mechanism precision is reserved for the curated
  dossiers**; the bulk index value is gene-evidence-level, not disease-level. Do not over-read the bulk column.
- **Prevalence is mostly `[O]`.** MedGen definitions rarely state prevalence, so most dossiers carry `[O]` with the
  obstacle named (only Cystinosis / Fabry / PKU had an `[L]` figure minable from the definition). **R3/Orphanet is the
  intended fill** for prevalence and incidence.
- **A few honest-thin dossiers** (all defensible, not errors): β-thal & α-thal have sparse HPO coverage at the correct
  in-scope OMIM (richer subtypes are different genes / CNS syndromes, correctly excluded by scope); Cystinuria & von
  Willebrand mechanism = `[O]` (incompletely-dominant / complex — honestly not guessed).
- **Date-stamped digest.** Each dossier embeds today's `generated` date, so the dossier-set sha is reproducible
  within a run/day; the pipeline inputs and logic are otherwise fully deterministic (verified by 2× identical runs).

---

## Next session — Phase R3 (investigation only)

**Goal:** the reproducible burden ordering ("suffering order") over the in-scope diseases, per
`methodology/BURDEN_INDEX.md` (deterministic, C1). R2 produced its inputs: the graded `disease_index.csv` and the
35 dossiers. R3 stays investigation-only — **no whitepaper prose** until the W1 consolidation gate.

**Reproduce R1 → R2 (then begin R3):**
```bash
python3 code/pipeline/r1_build_index.py          # base index            (sha ddfbcac71d6b)
python3 code/pipeline/r1_gate.py                 # R1 gate               PASS 5/5
python3 code/pipeline/r2_enrich_inscope.py       # disease_index.csv + inheritance (cached MedGen)
python3 code/pipeline/r2_boundary_review.py      # CNS boundary moves + cns_cross_reference col
python3 code/pipeline/r2_mechanism.py            # mechanism_class       (index sha a274e25a00bb)
python3 code/pipeline/r2_cohort_medgen.py        # cohort MedGen cache   (OMIM cross-refs)
python3 code/pipeline/r2_cohort_gene_resources.py# NCBI Gene + ClinVar per cohort gene
python3 code/pipeline/r2_build_dossiers.py       # 35 dossiers           (set sha b70b12d01e75)
python3 code/pipeline/r2_gate.py                 # R2 gate               PASS 7/7
sha256sum -c MANIFEST_governed.sha256            # engine pin            drift 0 (15/15)
```
All raw sources are cached under `data/raw/` — the rebuild needs **no network**.
