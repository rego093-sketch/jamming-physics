# Traceability spec (VP chemistry amplitude)

This document formalizes the *chain-of-custody* for reference amplitudes used in Sec.18.

## Why this file exists

The bulk inspection dataset `VP_STEP7_EXT_INSPECTION_FULL_V1` stores a column `OBS_REF_AMP(fm)`.
That column is intended to be grounded in external measurement/handbook sources, while avoiding redistribution of copyrighted tables.

To prevent 'black-box' criticism, each reference amplitude should be traceable to:

1) a concrete raw source value (with units)
2) a specific source identifier (book / database / paper)
3) a declared conversion rule ID (even if the rule is non-linear or geometry-dependent)

## Files

### Definitive spec (recommended)

- Spec text (V3): `04_vp_whitepaper/data/chem/traceability_spec_v3.txt`
  - includes the physical definition of the scaling constant `K`
  - includes a rigorous Rule-B derivation example for `CH4`

### Machine-readable seed tables

- Traceability table seed (V3): `04_vp_whitepaper/data/chem/traceability/traceability_table_v3_seed.csv`
- Source registry (V3): `04_vp_whitepaper/data/chem/traceability/sources_v3.json`

### Legacy (kept for provenance)

- `04_vp_whitepaper/data/chem/traceability_spec_v1.txt`
- `04_vp_whitepaper/data/chem/traceability/traceability_table_v1.csv`
- `04_vp_whitepaper/data/chem/traceability/sources_v1.json`

## Status in this DOI bundle

- The DOI bundle includes a **seed subset** (not a full raw-data mirror).
- The design goal is that every row in the bulk inspection dataset can be upgraded to have a row-level trace entry (raw value + rule + source detail).

When the seed tables are expanded (including stable identifiers such as database entry IDs and, where possible, page/table numbers), the dataset can be upgraded from an *integrity-gated compilation* to a *traceability-gated validation artifact*.
