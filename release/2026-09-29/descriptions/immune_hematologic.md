## Summary
This volume reads the immune and blood-forming organs as populations of R19 switches. Their thresholds are read from measured master-gene promoter γ: RUNX1 1.3225, TLX1 1.4228, FOXN1 1.4533 and PAX5 1.4892. It inherits the γ ruler and node atlas from **dna**, the time layer from **circadian** and setpoint drift from **aging_senescence**. It adds one module: population thresholds on the R19 switch. The claims ledger records the headline as an **interpretation**. The γ values are code outputs on sequence whose four promoter windows were checked byte-exact against NCBI GRCh38.p14, a genuine observation-level provenance check. Reading them as population thresholds is interpretation. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its dependence on inputs, grid or step stated), a consistency check or an interpretation. The former [F]/[V] grades are relabelled in place, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- §3 and hub: the lineage order from γ ranking, with "endpoints match embryology", was graded [V]. It is now code output (the ranking) plus interpretation, with building [O] per dna §RB. The ranking puts bone-marrow haematopoiesis first, but bone marrow is the last haematopoietic site colonised, after yolk sac, AGM, fetal liver and spleen (Tavian & Péault 2005). The page had conflated the early RUNX1 AGM programme (North et al. 1999) with the bone-marrow organ.
- §3: "the shared-drive race confirms the order dynamically" is relabelled a consistency check. Under one rising drive each switch commits at its own spinodal, so the commit order and spacing (0.0213 vs 0.0211) reproduce the γ ranking by construction.
- §15 and hub: "the optimal re-boost interval emerges at the measured half-life" is corrected. The horizon is set to n_b·t_θ, so boosting every t_θ covers 100 % by construction. r* = 1 is read on a 7-point grid, and the "half-life" is a model output (D = 0.28, θ = 0.5). Therapy content remains direction / class only.
- §16–§21: seam and harness "[V]/[F]" badges record cross-package drift 0 and pointer declarations. They are relabelled consistency checks between shipped engines, not biological verification.
- The γ provenance "[V] canonical derivation" is relabelled observation (measured).

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub. The legend now reads "measured inputs or model outputs". On all pages outside the existing lt-note asides: [V] → code output and [F] → consistency. Manifest grade counts forced 4 / verified 38 → 0 / 0.
- Reading-versus-building notes were added to §3 and the hub.

**Reproduction package changes**
- None. Code and data under `repro/immune_hematologic/` are unchanged since the previous version.

**Site/metadata**
- Biology reading-rule registry integration: `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed. The work-in-progress snapshot commits for the organ volumes and the sibling light reviews (circadian, aging_senescence, inheritance) were included.
- Recurrence guards: integrity checks in the gate, the manifest generator fixed, and `_decl` inheritance aligned.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume.

## Claim status (claims ledger)
Counts: interpretation 3 · identity 2 (5 rows).
- Population thresholds on the R19 switch read from measured γ (RUNX1 1.3225, TLX1 1.4228, FOXN1 1.4533, PAX5 1.4892) — interpretation — residual 0 on sequence provenance (promoter windows byte-exact vs NCBI GRCh38.p14).
- Lineage order from γ ranking; "endpoints match embryology" — interpretation — conflicts with the observed site sequence (bone marrow colonised last). Was [V]; order [O].
- Shared-drive race confirms the order dynamically (commit spacing 0.0213 vs 0.0211) — identity — reproduces the γ ranking by construction.
- Optimal re-boost interval emerges at measured half-life (r* = 1; PF 1.00 / 0.38 / 0.49 at r = 1 / 0.25 / 3) — identity — the horizon construction guarantees full coverage at r = 1; the half-life is a model output.
- Thymic involution raises escape and lowers naive export (escape 0.29 % → 3.71 %; naive export 32.9 % → 15.9 %) — interpretation — model outputs of chosen parameters; no external comparison reported.

## Open items
- Developmental order, size and timing of the haematopoietic and lymphoid organs: building is [O] (dna §RB).
- Every therapy item is direction / class only. Doses, titres and real-time schedules are withheld under the magnitude firewall.
- An external comparison for the thymic-involution outputs is not yet made (review).

## Reproduction
The ZIP contains `docs/immune_hematologic/` (the published HTML pages), `repro/immune_hematologic/` (engines, dynamics and therapy scripts, inherited substrate and inheritance kit, reports), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/immune_hematologic && python3 repro/run_all.py` (see `repro/immune_hematologic/repro/REPRODUCE.md`). The stress battery takes longer than two minutes.
- Focused scripts, each under 7 s: `repro/immune_hematologic/repro/_dynamics/lineage_order.py`, `repro/immune_hematologic/repro/_dynamics/emergent_durable_boost.py` and `repro/immune_hematologic/repro/_dynamics/emergent_immunosenescence.py`.
- Gates: `repro/immune_hematologic/repro/_verify/gates.py`.
- SEED = 19. No network is needed for the checks. Only the optional sequence cross-check `repro/immune_hematologic/inherited/ncbi_verify.py` contacts NCBI.

## Citation and links
- Site: https://jamming-physics.org/immune_hematologic/
- Concept DOI: 10.5281/zenodo.20755280
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
