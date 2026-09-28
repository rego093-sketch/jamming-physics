# DOI

**Zenodo DOI (reserved / deposit identifier):** `10.5281/zenodo.17932567`

- Canonical resolver: https://doi.org/10.5281/zenodo.17932567
- This DOI is used as the **single persistent identifier** for all internal artifacts in this unified bundle (text + code + data + logs), unless a submodule is later released as a separate Zenodo record.

## How to cite

- For the whole bundle, use the DOI above (see `CITATION.cff`).
- For the VP white paper PDF/TeX, cite the same DOI and mention the file path: `04_vp_whitepaper/`.

## Internal citation policy (no missing DOI)

The VP white paper contains internal bracket references of the form `[cite: XX]`.
All such cite-IDs are resolved via the **DOI-anchored citation registry** embedded in the PDF (Appendix I) and also stored as:

- `04_vp_whitepaper/docs/citations/CITE_REGISTRY.csv`
- `04_vp_whitepaper/docs/citations/CITE_REGISTRY.md`

Each registry entry includes:
- cite-ID
- short label
- type (simulation / report / device / note)
- DOI (this Zenodo DOI)
- bundle file paths (evidence)
- Gate status (PASS/UNLOGGED/INCONCLUSIVE)
