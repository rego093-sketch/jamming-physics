# Non-Opioid Analgesic Target Map — 27 DNA-grounded targets

## Summary
This volume (Analgesic Threshold Logic, tier 8 of the VP corpus) maps 27 nociception genes to a promoter γ read and the R19 switch threshold |h_sp| = (2/(3√3))·γ^1.5 (barrier γ²/4), sorts them into three correction levers L1/L2/L3, and states proposals P1–P6 as corrective directions only. It inherits from neuro (and, through it, the dna γ ruler), and adds one module: the three-lever L1/L2/L3 therapeutic logic. The headline, three levers from 27 gene γ/|h_sp| reads, is classed in the claims ledger as **interpretation**: γ places each gene on the |h_sp| scale, but lever placement and direction come from cited channel physiology, not from γ. The companion headline number corr(γ, GC) = 0.99898 is an **identity** of the SantaLucia table (random sequence gives about 0.9996), a consistency check rather than a finding. Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to pain thresholds and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation. The magnitude firewall is absolute: no dose, concentration, regimen or effect size is given.

## What changed in this version (2026-09-29)
**Corrections**
- "read [V]" replaced by "read: code output" on the hub (27 occurrences) and on target-scn9a, target-scn10a and target-ngf: the γ read is a deterministic code output from the promoter window and the SantaLucia table, not a test against external data.
- corr(γ, GC) = 0.99898 annotated as table-intrinsic (a consistency check, not verification).
- "[F] forced by the reads" split by kind: order by |h_sp| → code output (consistency); lever placement and direction → interpretation anchored to cited physiology; mechanism (e.g. Binshtok 2007 differential block) → observation + interpretation.
- Lever pages' "the promoter reads place each gene in lever L1" identified as an overstatement (γ places the gene on the |h_sp| scale only).
- Prioritisation: [F] → code output that depends on the declared editorial weights (0.40 / 0.35 / 0.25) on cited 1–5 tiers.
- Proposals P1–P6 and the falsification page: [F] → interpretation (untested hypotheses); the framework falsifier "does γ track expression-switch behaviour?" stays [O].
- precision-local-anaesthesia: [F] → observation (Binshtok 2007) + interpretation. No numeric change.

**New experiments and results**
- None. Light two-reviewer review (`reviews/biology/2026-09-29_analgesic_threshold_review.md`): `repro/run_all.py` gives 10/10 module gates PASS but overall FAIL, because the forbidden-claim scanner (`05-intervention-logic/expected/claim_scan.json`) no longer finds the moved `docs/` sources, so the published pages are not scanned by the volume's own scanner. `03-threshold-map/expected/threshold_map.json` matches all 27 γ and |h_sp| values on the hub (0 mismatches); `02 nav_gate.json` corr 0.998978, drift 0.
- Magnitude-firewall audit (corpus lineage, 2026-09-29): 0 hits for doses, concentrations, regimens or targets in this volume. Named agents appear as cited observations only.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub (one correction note); grade legend relabelled on grading-and-honesty and how-to-read-this-map (code output / consistency / observation / interpretation / [O]).

**Reproduction package changes**
- `repro/analgesic_threshold/` is unchanged since the 2026-06-24 state. The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Link audit (2026-09-28): stale repro paths and stale site slugs (e.g. `/analgesic/`) repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24).

## Claim status (claims ledger)
Counts: interpretation 2 · identity 2 · anchor-restatement 1 · open 1 · independent-prediction 0.
- Headline: three levers L1/L2/L3 from 27 nociception gene γ/|h_sp| — interpretation — 0 mismatches page vs code; lever placement from cited physiology, not γ.
- corr(γ, GC) = 0.99898 (0.998978) — identity — property of the SantaLucia table (random sequence ~0.9996).
- |h_sp| and barrier per gene (e.g. SCN9A 0.638545 / 0.49098) — identity — algebra on measured γ.
- Target prioritisation — anchor-restatement — depends on declared editorial weights 0.40 / 0.35 / 0.25.
- Proposals P1–P6 (e.g. differential block) — interpretation — direction/class only; untested hypotheses.
- Volume gate — open — 10/10 module PASS, overall FAIL (claim_scan hash drift: scanner misses moved docs/).

## Open items
- Framework falsifier [O]: does γ track expression-switch behaviour?
- All magnitudes (dose, concentration, effect size) [O] by design (magnitude firewall).
- Author decisions (review): apply the same relabel to the remaining 24 target pages and the 5 lever pages (same template); repoint the claim scanner to `docs/analgesic_threshold/` so the overall gate passes; run `tools/record_page_notes.py`.

## Reproduction
The ZIP contains `docs/analgesic_threshold/` (the published HTML pages), `repro/analgesic_threshold/` (code and data), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main check: `python3 repro/analgesic_threshold/repro/run_all.py` (10 module gates; overall FAIL expected until the scanner is repointed); hashes in `repro/analgesic_threshold/repro/expected_sha256.json`.
- γ reads and gate: `repro/analgesic_threshold/repro/02-read-nav-channels/gate_nav_channels.py`; threshold map: `repro/analgesic_threshold/repro/03-threshold-map/`.
- SEED = 19 (`repro/analgesic_threshold/repro/_engine/vp_neuro_engine.py`). No network needed: `02-read-nav-channels/fetch_nav_channels.py` (run by `run_all.py`) reads offline from the bundled promoter cache when present.

## Citation and links
- Site: https://jamming-physics.org/analgesic_threshold/
- Concept DOI: 10.5281/zenodo.20733420
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
