# Evidence materials — index

This package is **evidence-complete and English-only**. Every claim rendered in the `docs/`
site is backed by material included here, and the whole site reproduces byte-for-byte from the
source JSONs (`python3 tools/build_disease_site.py`).

## What backs each on-page claim
- **R19 switch / cusp geometry** — derived from the measured promoter gamma of each gene; the
  values printed on every disease page come from `outputs/mapped_levers.json` and
  `outputs/actionability_index.json`. Deterministic (SEED-fixed, 2x SHA-256).
- **Mapped existing agents (the "MATCH / validation signal" rows)** — each carries its literature
  source citation, rendered inline in the agents table. 947 distinct
  (disease, citation) rows are carried in `outputs/mapped_levers.json` and shown on the pages.
- **Surfaced candidate leads (direction-only [O])** — each carries prior-art provenance:
  228 of 233 candidates have a `prior_art_source`; all 233 have a `prior_art_note`
  (`outputs/surfaced_candidates.json`).
- **Recovered standard-of-care validation** — chapter `03-validation-recovered-standard-of-care`
  is built from the MATCH set in the source JSONs (not from any external file).

## Evidence directories
- `outputs/` — the **4 source JSONs the builder reads** (`actionability_index.json`,
  `mapped_levers.json`, `surfaced_candidates.json`, `candidate_register.json`) plus
  `firewall_log.json`. These fully reproduce the site.
- `inputs/` — the **upstream corpus**: `disease_inputs.json` (the canonical per-disease
  corrective-agent table with all literature `source` citations) and `kit_reads.json` (the full
  per-disease cusp reads and answer text). These are the raw inputs the JSONs above were compiled
  from. (Superseded 160- and 560-disease snapshots were dropped.)
- `validation/` — the **preregistered falsification record**: V1-V18 `*_PREREGISTRATION.json`
  (hypotheses + criteria fixed before each test) plus the data-fetch scripts and rendered reports.

## Integrity
- `SITE_BUILD_MANIFEST.sha256` — SHA-256 of every site file + a tree-digest
  (`sha256` over the sorted `{path}  {hash}` block; matches `build_disease_site.py`).
- `EVIDENCE_MANIFEST.sha256` — 2x SHA-256 of every evidence file (outputs + inputs + validation).
  Both the per-file hash and the tree-digest formulas are written into the manifest header, so the
  roll-up digest is independently reproducible (per-file: `sha256(sha256(bytes).hex())`; tree-digest:
  the same 2x SHA-256 over the sorted `{path}  {hash}` block).

## Release labelling (two labels, one register state)
Two version strings appear in this package and they are **not in conflict**:
- **Package / site release** — `0.42.1-trackA.merged_3of3` — the label of this Track-A merged
  build; it is what the site, `SITE_README.md`, and `docs/disease/_meta.json` display.
- **Candidate-register mint stamp** — `outputs/candidate_register.json.release` =
  `0.40.0-repurposing.3` — the release at which the 233-row candidate register was first minted.
  The register is **append-only and hash-chained**, so this field is preserved as an honest record
  of when those rows were produced and is intentionally **not** overwritten.

Both labels denote the **same register state**. The chain head
`fc8598ec13f74a9e94d405d1be25573f13e4c0b7f93d3c96e958de9cfc01f658` is computed as
`sha256(prev + canonical(row))` over the genesis seed and the 233 rows **only** — the `release`
string is metadata and is **not** part of the hash pre-image (see `pipeline/build_candidate_register.py`).
The chain head is therefore identical under both labels, which is the cryptographic proof that the
rows carried into `0.42.1-trackA.merged_3of3` are byte-for-byte the rows minted at
`0.40.0-repurposing.3`.

## English-only note
Per request this package contains no Korean. Eight Korean-language narrative summaries
(`V9..V16 *_INHERITANCE_CHECKPOINT*.md`) were therefore omitted; their canonical, machine-readable
content is preserved in the corresponding `V9..V16 *_PREREGISTRATION.json` files, which are
included. No machine-readable evidence was lost.
