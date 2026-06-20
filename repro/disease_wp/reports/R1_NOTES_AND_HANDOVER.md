# R1 — investigation notes & handover

**Phase:** R1 (disease universe & classification scaffold) — **investigation only, no whitepaper prose.**
**Status:** core complete and banked. Clean handover point.
**Governing standard:** VP-SPEC v1.8 (authoring discipline switches on at Phase W1, not yet).

---

## What R1 produced (all reproducible, all provenance-tagged)

### Raw enumeration pool (`data/raw/`)
- `clinvar/gene_condition_source_id.tsv` — NCBI ClinVar gene↔condition map, **13,447 associations**
  (pulled 2026-06-17 from `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id`).
- `medgen/` — MGSAT/MGSTY/HPO-mapping RRF files + **18 cached MedGen esummary responses** (re-runs do not re-hit NCBI).

### Base index (`data/curated/disease_index_base.csv`) — the scaffold
- **7,672 unique diseases** (aggregated by MedGen CUI), each with gene list, OMIM MIM, organ-system hint,
  in-scope flag, and provenance. Built by `code/pipeline/r1_build_index.py` (deterministic; sha `ddfbcac71d6b`).
- Scope split: **6,170 in-scope (systemic)** · **1,502 excluded** (1,282 neuro / 170 cardiac / 37 psych — all flagged with reason, none dropped).
- System-hint spread (in-scope): metabolic 770, connective/skeletal 422, eye 298, hematologic 186, ear 182,
  dermatologic 172, renal 159, endocrine 122, cancer-predisp 108, pulmonary/exocrine 89, GI 54, immunologic 52,
  hepatic 50, lysosomal 21, unclassified-systemic 3,498.

### Investigation gate (`reports/r1.gate.json`) — **PASS (5/5)**
provenance_complete · dedup_unique_cui · scope_logged · in_scope_binary · entity_present.

### Enriched seed (`data/curated/disease_index_seed.csv`) — R2 path demonstrated
- **18 flagship in-scope diseases** enriched with **mode-of-inheritance + clinical definition + semantic type**
  pulled from **NCBI MedGen esummary** (`code/pipeline/r1b_enrich_flagship.py`).
- Inheritance is a clean, cited, graded pull (`[L]` when stated, `[O]` when MedGen has none). All assignments
  verified correct: CF/PKU/Gaucher/Wilson/Pompe/etc. = AR; Marfan = AD; OI = AD+AR; Fabry = X-linked;
  hemophilia A & DMD = X-linked recessive.

---

## Confirmed, reusable findings (so the next session does not re-derive them)

1. **NCBI is fully open here.** E-utilities + ClinVar/MedGen FTP all reachable. Key DBs: clinvar, medgen, omim,
   gene, dbvar, gtr, snp, pubmed, mesh.
2. **The clean inheritance source is MedGen esummary**, field `conceptmeta → <ModeOfInheritance><Name>`.
   `MGSAT NCBI_CURATION_MOI` is too sparse (only 19 concepts); HPO-mapping file is term-CUIs, not disease annotations.
   MedGen efetch `rettype=xml` returns HTTP 400 — use **esummary JSON**, not efetch.
3. **MedGen esummary also returns the clinical definition + semantic type** in the same call — one call gives
   inheritance, definition, and type.
4. **gene_condition_source_id has some blank-gene rows** (phenotypic-series-level associations) — R2 fills the
   gene from NCBI Gene/ClinVar where the base row is empty (e.g., Gaucher, Pompe came through with blank gene at CUI level).

---

## Known limitations (honest, for R2 to resolve — not defects)

- **Scope filter is NAME-BASED and provisional.** It matches the disease *name* as a proxy for the primary
  system. It will mis-bin entities whose name does not signal the primary system. One such miss was caught and
  fixed this session (Huntington/Rett/Angelman now excluded). **R2 must verify scope from actual organ-involvement
  data**, especially for these boundary classes:
  - **Lysosomal/storage diseases with primary CNS** (Tay-Sachs, neuronopathic Gaucher, Niemann-Pick A/C) — currently
    in-scope under "lysosomal"; per SCOPE.md primary-system rule some belong to the sibling. **Flag for boundary review.**
  - **Neurocutaneous** (tuberous sclerosis, NF1) — multi-system; keep in-scope, cross-reference CNS.
  - **Metabolic with primary CNS** — review case-by-case.
- **`inheritance_class` / `mechanism_class` are `PENDING_R2`** in the base index (only the 18-disease seed has inheritance).
- Two flagship names missed the index match (`Sickle cell`, `G6PD deficiency`) — they exist under variant names; fix the match strings in `r1b_enrich_flagship.py`.

---

## Next session — Phase R2 (still investigation only)

**Goal:** turn the 6,170-row in-scope base index into per-disease dossiers (inheritance + mechanism + clinical fields).

Run order (the pipeline is in `code/pipeline/`):
1. `python3 code/pipeline/r1_build_index.py` — regenerate base index (verify sha `ddfbcac71d6b`).
2. Extend `r1b_enrich_flagship.py` into a **bulk** enricher over all in-scope CUIs (batch MedGen esummary;
   respect ≤3 req/s; cache every response under `data/raw/medgen/`). Output `disease_index.csv` with inheritance
   + clinical definition + semantic type populated.
3. Add **mechanism_class** enrichment: per-disease, derive LoF/GoF/dominant-negative/haploinsufficiency/dosage/
   repeat/imprinting from OMIM + ClinVar variant spectrum + PubMed (cite PMID/MIM; grade honestly; do not guess).
4. Apply the **boundary review** to the lysosomal/neurocutaneous/metabolic-CNS classes above; move primary-CNS
   entities to `in_scope=false` with reason.
5. Re-run an R2 investigation gate (extend `r1_gate.py`): inheritance-complete, mechanism-graded, boundary-resolved.

**Do NOT start whitepaper prose** until the consolidation gate in `ROADMAP.md` passes (after R2–R4).

---

## Reproduce R1 from scratch

```bash
# (raw files already cached in data/raw/; to re-pull:)
curl -s "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id" -o data/raw/clinvar/gene_condition_source_id.tsv
python3 code/pipeline/r1_build_index.py        # -> disease_index_base.csv  (sha ddfbcac71d6b)
python3 code/pipeline/r1_gate.py               # -> reports/r1.gate.json     PASS (5/5)
python3 code/pipeline/r1b_enrich_flagship.py   # -> disease_index_seed.csv   (18 enriched)
```

Engine baseline unchanged and still verifiable: `sha256sum -c MANIFEST_governed.sha256` → all OK.
