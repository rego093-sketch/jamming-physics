# Extraction Protocol (chemistry tables)

This document defines a minimal, audit-friendly protocol for turning
external reports (PDF / lab notebook / simulation logs) into the locked
CSV inputs used by the VP whitepaper chemistry module.

## Goal

- Avoid "hand-copied" numbers without provenance.
- Provide a deterministic mapping:
  **source document → extraction steps → extracted CSV → derived tables**.

## Required artifacts per source

For each external source that feeds `data/chem/observed_amplitudes.csv`:

1. A stable identifier
   - Prefer a DOI.
   - If no DOI exists, include a versioned local identifier (e.g., `internal_report_YYYYMMDD_v1`).

2. A copy of the source if redistribution is allowed
   - Place in `04_vp_whitepaper/docs/chem/sources/`.
   - If redistribution is *not* allowed, include:
     - bibliographic metadata
     - an unambiguous locator (title/authors/year/venue/pages)
     - a hash of the locally held original (so auditors can verify the exact file existed).

3. Extraction notes
   - Exact page/figure/table numbers.
   - Any unit conversions (with equations).
   - Any averaging/windowing rules.

4. Extraction output
   - A CSV row (or multiple) in `data/chem/observed_amplitudes.csv` with
     the `source_tag` and `source_detail` pointing back to the above.

## Prohibited

- Post-hoc tuning (changing the extraction rule after seeing whether it supports √2).
- Reporting only supporting cases without logging fails/unknowns.

