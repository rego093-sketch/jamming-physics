# DATA_PROVENANCE — NCBI sources and citation rules

All disease facts in the R-phases come from NCBI (confirmed reachable in R0). Each fact is **observed** (VP-SPEC
C1: "관찰값은 존중한다") — respected and cited, never claimed as "reproduced." The whitepaper's reproducible
contribution is the *analysis* built on these inputs (classification, burden index), not the inputs themselves.

## Source databases (E-utilities; all confirmed available)

| DB | use |
|---|---|
| **MedGen** | medical-genetics concepts (CUI), the spine of `disease_index.csv` |
| **OMIM** (via MedGen/OMIM links) | gene–phenotype catalog, inheritance, onset |
| **Gene** | gene records, function, location |
| **ClinVar** | variant ↔ disease ↔ clinical significance distribution |
| **dbVar** | structural variants / CNVs (microdeletion-microduplication syndromes) |
| **dbSNP** | small-variant identifiers |
| **GTR** (Genetic Testing Registry) | testing availability → clinical actionability signal |
| **PubMed** | primary literature for molecular mechanism, prevalence, treatment mechanism |
| **MeSH** | controlled vocabulary for consistent disease/term naming |
| **protein / nuccore** | sequence-level detail when a mechanism needs it |

## Provenance rule (every collected fact)

Each datum carries: `source_db`, `accession` (e.g., OMIM #, MedGen CUI, ClinVar VCV, PMID), `retrieval_date`,
and a **grade** (`[V]/[L]/[O]` per `BURDEN_INDEX.md`). A fact without provenance does not enter `data/curated/`.

## E-utilities etiquette (so collection stays clean and unthrottled)

- Base: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` — `esearch` → `esummary`/`efetch`; `elink` for cross-DB links.
- Rate: ≤ 3 requests/second without an API key. With an author API key + `&email=`, up to 10/s. Add a small
  delay between calls; batch IDs with `epost` where possible.
- Cache every raw response under `data/raw/<db>/<query>.json` with the retrieval date, so R-phase pulls are
  themselves reproducible and re-runs do not re-hit NCBI unnecessarily.
- Prefer structured endpoints (esummary JSON, ClinVar VCV XML) over scraping HTML.

## Copyright / reuse

Store **facts and identifiers** (gene, variant class, inheritance, prevalence figure, mechanism statement with
PMID), not long verbatim text from articles. Mechanism descriptions in the whitepaper are written in our own
words and cited by PMID/accession.

## Separation of observed vs reproduced (the core C1 discipline)

- **Observed (cited, respected):** prevalence, onset, clinical significance, survival figures, the *fact* that a
  therapy exists — all from NCBI.
- **Reproduced (our deterministic layer):** the inheritance/mechanism classification logic, the burden index and
  its ranking, and any morphogenesis-baseline annotation from `code/emergence_v2/`.

Keeping these two columns distinct is what lets the W-phase gate certify "the released numbers reproduce and
nothing observed was silently edited."
