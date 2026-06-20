# 07-pillar-ii-geometric-arrangement-fixes
Verifies: Pillar II: RCCI identity <=1e-15; published audit tables to 2.83e-12. Run: python verify_rotcore.py ./rotcore.
Section: §7 — Pillar II --- Geometric: arrangement fixes length (whitepaper v2.1, concept DOI 10.5281/zenodo.17972568)

## Reproduction map
- `verify_rotcore.py` (+ `.out.txt`) — the RCCI audit verifier (run: `python verify_rotcore.py ./rotcore`).
- `rotcore/*_v139.csv` — frozen v139 audit result tables consumed by the verifier.
- `rotcore/audit-source/` — generation provenance folded in from the standalone
  `rotcore-doi-v1_3_9` package: the metric generators (`code/scripts/`), the
  formal metric definitions (`docs/METRICS_SPEC_*.json`), v138 legacy tables,
  the source manuscript, and the audit trail. The v139 CSVs are NOT duplicated
  there (they live one level up). See `rotcore/audit-source/PROVENANCE.md`.
