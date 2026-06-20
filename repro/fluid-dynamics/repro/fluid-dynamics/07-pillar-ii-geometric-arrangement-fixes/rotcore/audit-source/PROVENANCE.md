# Provenance — rotcore audit source (§7 Pillar II / Appendix G)

This `audit-source/` folder is the **generation provenance** for the RCCI
rotation-core audit whose *frozen result tables* already live one level up in
`../rotcore/*_v139.csv` and are checked by `../../verify_rotcore.py`.

It was folded in from the author's standalone package
`rotcore-doi-v1_3_9` (manuscript `rotcore_prf_manuscript_single_v1.3.6.tex`,
not registered as a separate paper). The whitepaper already shipped the v139
output CSVs + the verifier; what was missing was *how those metrics are
defined and produced*. This folder fills that gap:

- `code/scripts/` — the recompute / coverage / identity-residual / robustness
  generators (`recompute_v136.py`, `coverage_v137.py`,
  `identity_residual_v137.py`, `compute_robust_v137.py`).
- `docs/METRICS_SPEC_v137/v1.3.8/v1.3.9.json` — the formal metric definitions
  (this is the spec the verifier's identity/coverage checks rely on).
- `legacy/*_v138.csv` — the previous-version tables, kept for version history.
- `manuscript/` — the source manuscript (PRF single-column draft).
- `reports/metrics_long_v137_match.csv`, `CHANGELOG.md` — audit trail.

The **already-present, byte-identical v139 CSVs are NOT duplicated here** —
they remain in `../rotcore/` because that is the path `verify_rotcore.py`
reads (`python verify_rotcore.py ./rotcore`). This folder is read-only
provenance; running the verifier does not require it.

Numbers unchanged: RCCI identity ≤ 1e-15, published audit tables to 2.83e-12
(see `../../README.md`).

---
## v1.8 note — manuscript source removed under Constitution C2
`manuscript/rotcore_prf_manuscript_single_v1.3.6.tex` was removed from this
distribution to satisfy VP-SPEC v1.8 Constitution C2 (no TeX body source in the
package; `find . -name '*.tex'` must be 0). The audit's **reproduction**
provenance is unaffected — the metric generators (`code/scripts/`), the formal
metric spec (`docs/METRICS_SPEC_*.json`), the v138/v139 result CSVs, and the
audit trail (`CHANGELOG.md`, this file) all remain. The manuscript write-up is a
citation-layer artifact, retrievable from its source package `rotcore-doi-v1_3_9`.
