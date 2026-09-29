# Integumentary emergence · VP Theory

## Summary
This volume reads the skin as the body's barrier and its responses to external stimuli on the R19 switch. The switch thresholds are read from measured master-gene promoter γ: TP63 1.3643, KRT14 1.4894, MITF 1.3945 and EDAR 1.3696. It inherits the γ ruler and node atlas from **dna**, the time layer from **circadian** and setpoint drift from **aging_senescence**. It adds one module: barrier + external stimulus, with UV as the melanoma key. The claims ledger records the headline as an **interpretation**, and its one quantitative prediction (intermittent-burst UV raises melanoma RR) as an **independent prediction** whose direction matches observation. The magnitude of that prediction overshoots the observed summary RR by about 3.5× and depends on the chosen dose grid, so only the direction is claimed. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its dependence on inputs, grid or step stated), a consistency check or an interpretation. The former [F]/[V] grades are relabelled in place, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- §1 and hub: the developmental order epidermis → appendage → melanocyte → keratinocyte, read off γ as a "falsifiable consequence", is now interpretation, with building [O] per dna §RB. The ranking puts keratinocyte (KRT14) last. Observation: K14 is expressed in the surface ectoderm from about E9.5 (Byrne, Tainsky & Fuchs 1994), well before EDAR-dependent hair placodes at about E14.5 (Headon & Overbeek 1999).
- §5: epidermal turnover "~28 d lands in the cited 28–40 d window" [V] is true by construction. In `skn_dynamics.py` the ratio d_phase/d_phase ≡ 1, so the total is 2 × the 14 d input. It is relabelled consistency, and the answer and abstract now read "(2 × 14 by construction)".
- §7: the melanoma "burst RR up to ~5.7×" is now "modelled" and input-dependent (2.2 / 5.7 / 7.0 at cumulative dose 4 / 6 / 8, in model units). The observed summary RR 1.61 (CI 1.31–1.99; Gandini 2005) is placed next to the model number. The direction matches; the magnitude does not.
- §11–§13: the "[F] forced (substrate)" occlusion and adhesion set-points are dimensionless regime scales of the cubic. They are relabelled consistency (substrate).
- §1: a double-escaped arrow (`&amp;rarr;`) that rendered literally in the abstract was fixed.

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub. The grade legends on the hub and all 14 chapter footers now read "Labels (reading rule 2026-09-29): consistency · code output · [L] · [O]". On all pages outside the existing lt-note asides: [V] → code output, [F] → consistency, "simulation-verified" → "simulated". Manifest grade counts forced 15 / verified 40 → 0 / 0; open 91 is unchanged.
- Reading-versus-building notes were added to §1 and the hub.

**Reproduction package changes**
- No code or data change under `repro/integumentary/`. The whitepaper `repro/integumentary/paper/integumentary_vp_site_v1.0.0_whitepaper.pdf` and its `.tex` were added to the package in the June snapshot ("Final"). They predate the corrections above.

**Site/metadata**
- Biology reading-rule registry integration: `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed. The work-in-progress snapshot commits for the organ volumes were included.
- Recurrence guards: integrity checks in the gate, the manifest generator fixed, and `_decl` inheritance aligned.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume and added its `_decl.json`.

## Claim status (claims ledger)
Counts: interpretation 2 · identity 2 · independent-prediction 1 (5 rows).
- Barrier + external stimulus; UV → melanoma key (TP63 1.3643, KRT14 1.4894, MITF 1.3945, EDAR 1.3696) — interpretation — the γ are code outputs; the mapping is interpretation.
- Developmental order epidermis → appendage → melanocyte → keratinocyte from γ — interpretation — conflicts with observation (keratinocyte ranked last; K14 ~E9.5 before placodes ~E14.5).
- Epidermal turnover ~28 d in the cited 28–40 d window — identity — total = 2 × the 14 d input.
- Intermittent-burst UV raises melanoma RR (5.674, model units) — independent prediction — the direction matches Gandini 2005 (1.61); the magnitude overshoots by ~3.5× and is input-dependent (2.2 / 5.7 / 7.0).
- Occlusion / adhesion set-points "[F] forced (substrate)" — identity — dimensionless regime scales of the cubic.

## Open items
- Developmental order, size and timing of the skin and its appendages: building is [O] (dna §RB).
- The melanoma magnitude is not claimed. Only the direction is robust; absolute risk and every clinical magnitude are [O] under the magnitude firewall.
- The manifest counts 91 [O] markers across the volume's pages (open items as stated there).

## Reproduction
The ZIP contains `docs/integumentary/` (the published HTML pages), `repro/integumentary/` (engine, oncology kernel, inherited substrate, reports, whitepaper), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/integumentary && python3 repro/run_all.py`. It finishes with all PASS, and determinism is 2×SHA-256 identical.
- Turnover dynamics: `repro/integumentary/repro/_engine/skn_dynamics.py`. UV / melanoma kernel: `repro/integumentary/repro/_oncology/carcinogen_dose_response.py`.
- Gates: `repro/integumentary/repro/_verify/gates.py`.
- SEED = 19 (`repro/integumentary/inherited/vp_substrate.py`). No network is needed.

## Citation and links
- Site: https://jamming-physics.org/integumentary/
- Concept DOI: 10.5281/zenodo.20754541
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
