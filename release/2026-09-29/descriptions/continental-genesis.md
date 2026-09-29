## Summary
Continental Genesis inherits the jammed substrate from the physics volume, the jamming ↔ unjamming engine from the geodynamics volume and the continuum engine from the fluid-dynamics volume, and adds one module: continental genesis as a two-face rupture distillation of felsic crust (the opening face floors a basin; the antipodal downwelling/compression face flux-melts hydrated skin to granite). It re-poses "why dry land exists" as a question of composition and buoyancy (a two-tier crust), not of age; the claims ledger classes this headline as interpretation, since standard geology gives the same buoyancy explanation. Its budget result R1 (isostasy plus the measured ocean volume gives freeboard +840 m with no fitted parameter) is classed as anchor restatement: the exact hit comes from choosing one crustal density/thickness pair, while the sign and ~1 km order are a genuine Airy-isostasy output. A bidirectional chronology firewall keeps the occurrence and timing of continent formation [O].

## What changed in this version (2026-09-29)
**Corrections**
- None to the volume's claims or grades. A light review (reviews/earth/2026-09-29_continental_genesis_and_cascade_light_review.md) found the grading discipline stricter than the corpus average and required no correction; its one low-priority suggestion (a reader glossary for internal abbreviations such as State-4, S0, SH-5, M47, CG-39) is not yet applied.

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- None.

**Reproduction package changes**
- None to repro/continental-genesis/.

**Site/metadata**
- Rendering: raw $$ display math (§26, z = 2E/F = 6 − 12/F) converted to text, and escaped asterisks that broke italics (f* in §23, §25, §26) fixed on the hub page.
- Highwire citation meta regenerated from the manifest; corpus gate now fails on raw LaTeX or escaped comments in visible text and on citation-meta drift.
- Corpus bookkeeping: the orphan merged continental-genesis-cascade hub removed; the manifest generator now carries all 32 volumes including this one; homepage and corpus-guide counts regenerated.

## Claim status (claims ledger)
6 rows: interpretation 2 · anchor-restatement 1 · identity 1 · open 2.
- Dry land exists because of composition + buoyancy (two-tier crust), not age (headline) — interpretation — qualitative; the chronology firewall runs both ways.
- R1: isostasy + measured ocean volume reproduces observed freeboard with no fitted parameter — anchor-restatement — +840 m at ρ_c = 2835, H_c = 30 km (0 m residual for the selected pair; +333 to +1075 m for the other listed inputs).
- Bimodal hypsometry (two peaks ~5.2 km apart) — identity — land peak +744 to +1244 m high, ocean peak ~300–800 m shallow; the ocean peak restates the measured mean ocean depth; two model levels are bimodal by construction.
- Convergence is the forced downwelling limb of mantle convection — interpretation — Ra ≈ 5.85×10⁶ from assumed mantle parameters; standard mantle-convection physics.
- Continental area fraction is a percolation-bounded attractor — open — coupled 3-D run 0.30 (0.27–0.36) vs observed 0.41 (−0.11); value [O], bound [L]; plate-network connectivity z ≈ 5–6 gives a ceiling of 0.46–0.50, so 0.41 is not forced (CG-39).
- Occurrence and timing of continent formation — open — [O] by the volume's own rule, kept open permanently.

## Open items
- Occurrence, timing and rate of continent formation: [O] in both directions (chronology firewall); dates and sequences are kept as record.
- Continental area fraction: the executed 3-D coupled run misses the observed 0.41; the connectivity-dependent ceiling leaves the value [O] (CG-38/CG-39).
- The volume's own self-audit (§15) demotes 7 imported chronological readings to [O]; its puzzle map lists about 3–4 real edges, ~12 degenerate items, ~7 shared gaps and 6 strains.
- Reader glossary for internal abbreviations (light-review suggestion, pending).

## Reproduction
The ZIP contains docs/continental-genesis/ (the published HTML pages), repro/continental-genesis/ (code and data, including BLUEPRINT_and_GRADED_LEDGER.md, GOVERNANCE.md, NO_TUNING_THESIS.md, PUZZLE_MAP.md and the inherited engine), LEDGER.json (this volume's claims-ledger rows), CORPUS_GUIDE.md and MANIFEST.sha256 (SHA-256 of every file).
Main checks (Python 3, offline, no network):
- 23 self-contained screens in repro/continental-genesis/repro/, each deterministic (SEED = 19, double-SHA-256 gated) and ending with `REPRO GATE: PASS`: `cd repro/continental-genesis/repro && for s in *.py; do python3 "$s" | tail -1; done`.
- Key screens: r1_budget_screen.py (freeboard and hypsometry), area_fraction_attractor_screen.py, plate_connectivity_screen.py, no_tuning_falsifier_screen.py, firewall_self_audit_screen.py.
- Package integrity: repro/continental-genesis/MANIFEST.sha256.

## Citation and links
- Site: https://jamming-physics.org/continental-genesis/
- Concept DOI: 10.5281/zenodo.20827711
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
