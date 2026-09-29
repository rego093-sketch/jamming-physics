## Summary
Jamming Geodynamics inherits the jammed substrate from the physics volume and continuum flow from the fluid-dynamics volume, and adds one module: jamming ↔ unjamming yield of the lithosphere applied to continental break-up and Atlantic opening. The headline criterion — break-up when the effective driving stress exceeds the yield stress (Ψ_eff > Ψ_y) — is classed as identity in the claims ledger: a yield criterion holds by definition, and the continent-scale magnitudes that would make it bite on Earth are HOLD. The shipped engine (atl_bundle) reproduces the standard 2-D jamming fraction φ_jam ≈ 0.840 from a packing simulation (independent prediction of standard jamming physics, residual −0.002 vs the classic 0.842), and runs 39/39 PASS. The pre-registered predictions P1–P35 are specifications awaiting data (HOLD), and the volume is chronology-agnostic.

## What changed in this version (2026-09-29)
**Corrections**
- Update note on 13 pages (01, 04, 06, 16, 18, 20, 21, 22, 23, 24, 31, 32, 33): the file names given for prediction tests P1–P35 (p15_*.py scripts, *_gate.json results, DataPack CSVs such as atl_opening_points.csv) are pre-registration specifications, not shipped code or data. Each prediction is HOLD (data pending) — not a failed test and not lost code. The shipped code is the atl_bundle engine (validate_all.py 39/39 PASS; every script, result and figure matches SHA256SUMS.txt).

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- PASS verdicts listed for P4, P16, P19, P20, P24 (r16 matrix) and P29 coherence are now read as HOLD (data pending), since no shipped code or data reproduces them; P29 had already been downgraded to HOLD (r18) and P21 is FAIL.

**Reproduction package changes**
- Legacy Noah-flood whitepaper data bundles v1.2–v1.3 vendored under repro/geodynamics/legacy_noah_flood_v1_3/ as source data for the HOLD predictions (RSL at 8 sites, IntCal20/Marine20/ΔR, Nile-delta cores, leaf-wax δD, tree rings, coal geochemistry, aDNA tables, bone histology). `reproduce_all.py` ends hardgate PASS; checksums 83 OK, 2 MISSING (whitepaper .tex deliberately excluded), 2 FAIL (QA report regenerated after the checksum list, same in the pristine bundle); every data file matches. PDF/TeX and nested zips excluded.
- Missing-script baseline annotated (12 geodynamics HOLD specifications counted as pre-registration, not gaps).

**Site/metadata**
- Corpus link audit repaired stale GitHub repro and site URLs; Highwire citation meta regenerated from the manifest; corpus integrity checks added to the gate.

## Claim status (claims ledger)
7 rows: identity 1 · independent-prediction 1 · interpretation 1 · open 4.
- Break-up when Ψ_eff > Ψ_y (headline) — identity — holds by definition; continent-scale magnitudes HOLD (§16).
- Jamming fraction from a first-principles 2-D packing simulation — independent-prediction — φ_jam = 0.840 vs 0.842 (residual −0.002); reproduces standard jamming physics; the 2-D value is paired with the 3-D z_iso = 6 in the friction engine (flagged, fix deferred).
- Friction collapse by unjamming (liquefaction, not melt) — open — μ_eff ≈ 2.2×10⁻³ at ΔT ≈ 25 K is 20–90× below the observed dynamic weakening range 0.05–0.2; follows from assumed parameters; validate_all C19c labels it "honest HOLD" (needs pore pressure within 0.37% of lithostatic).
- P1: Atlantic rim passive-margin dominated — interpretation — R_sub = 0.057 (threshold ≤ 0.25) from literature segment lengths; not discriminating against standard plate tectonics.
- Suction runaway (Λ > 1) at continental scale — open — d_crit ≈ 12 km not directly observable; master-scale extrapolation HOLD.
- Rapid (kyr-scale) Atlantic opening and absolute chronology — open — not claimed numerically; P8 recast as a non-refutation (magnetic stripes give relative time only).
- Pre-registered module verdicts P4, P16, P19, P20, P24, P29 — open — no code or data in the repo reproduces the PASS verdicts; effectively HOLD; P21 FAIL.

## Open items
- P1–P35 prediction tests: HOLD until the pre-registered pipelines are run on data (the vendored v1.2–v1.3 bundles may feed P16, P19 and P29).
- Continent-scale yield magnitudes and suction-runaway scaling (Λ ∼ d²/W) HOLD; not lab-reproducible at continental geometry.
- Load-bearing μ_eff requires near-lithostatic pore pressure (HOLD).
- φ_jam 2-D value (0.840) paired with 3-D z_iso = 6 in the friction engine: numeric fix deferred.
- Absolute chronology: the volume is chronology-agnostic; U-Pb break-up ages conceded at full strength.

## Reproduction
The ZIP contains docs/geodynamics/ (the published HTML pages), repro/geodynamics/ (code and data), LEDGER.json (this volume's claims-ledger rows), CORPUS_GUIDE.md and MANIFEST.sha256 (SHA-256 of every file).
Main checks (Python 3, no network needed):
- `python3 repro/geodynamics/src/geodynamics/atl_bundle/validate_all.py` — engine validation, 39/39 PASS; outputs checked against SHA256SUMS.txt in that bundle.
- Engine modules in repro/geodynamics/src/geodynamics/atl_bundle/engine/ (e.g. jamming_microderive.py, vp_jamming_friction.py, p1_plate_boundaries.py, c4_scalability.py, c19_master_scale.py).
- Legacy data bundle: `python3 scripts/reproduce_all.py` inside repro/geodynamics/legacy_noah_flood_v1_3/vp_repro_bundle_v1_3/ (hardgate).
Known HOLD and irreproducible items are listed in repro/geodynamics/IRREPRODUCIBILITY_LEDGER.md. Deterministic scripts use SEED = 19 where randomness is involved.

## Citation and links
- Site: https://jamming-physics.org/geodynamics/
- Concept DOI: 10.5281/zenodo.17978934
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
