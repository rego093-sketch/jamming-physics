## Summary
This volume (Rare Disease Mechanisms, tier 8 of the VP corpus) presents per-disease gene-key mechanism cases: 35 disease pages and 2 mechanism-class pages that read each disease's key gene on the R19 switch and rank diseases by an unmet-burden residual, `burden = raw_burden · (1 − e)`. It inherits from dna, and adds one module: the per-disease gene-key mechanism cases. The headline residual ranking is classed in the claims ledger as an **anchor restatement**: `e` is a declared a-priori evidence bin, not a clinical effect size, and the residual is a code output of those bins and equal weights; it reruns byte-identically but the order moves under reweighting (ρ 0.89–0.98), and the pages already declare the order a provisional [H] device. Clinical inputs are cited observations (GeneReviews and accession-dated sources). Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to each disease and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation. The magnitude firewall is absolute: treatments are named only as observed standard of care, with no dose or effect size.

## What changed in this version (2026-09-29)
**Corrections**
- §1: the abstract drops "[V] law"; legend rows [V] and [F] annotated as not used for biological claims; the completion criterion "[L]/[V]" becomes "[L] (observation)" (a published distribution is an observation).
- §1 and pages 02, 07, 17, 18: the efficacy offset `e` annotated as a declared a-priori bin, not a clinical effect size; the residual sentence annotated as "a code output of declared bins".
- Mechanism-class pages 37 and 38: "[F] mechanism class" → "observation: mechanism class" (grouping by mechanism is an observation-based classification, not forced); the hub entries relabelled the same way.
- No numeric change.

**New experiments and results**
- None. Light two-reviewer review (`reviews/biology/2026-09-29_disease_wp_review.md`): `r3_burden_index.py`, `r4_burden_residual.py` and `r15_severity_litcurate.py` rerun byte-identically (the registry files the pages read match: PKU 0.3375 rank 16, CF 0.3075 rank 17, DMD 0.4760 rank 6, achondrogenesis 0.9167 rank 1). `r15_gate.py` on a pristine copy: FAIL, 15/16 — `prior_round_artifacts_preserved` fails because 10 R9–R14 CSVs no longer match their recorded digests (pre-existing).
- Magnitude-firewall audit (corpus lineage, 2026-09-29): 0 hits for doses, concentrations, regimens or targets in this volume.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub (one correction note); grade vocabulary otherwise kept ([L] registry / [H] inference / [O] open). Manifest grades unchanged (open 12, hypothesis 24).

**Reproduction package changes**
- `repro/disease_wp/` code and data are unchanged since the 2026-06-24 state. `docs/disease_wp/_decl.json` now declares the R19 primitive (decl inheritance aligned). The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Recurrence guards: integrity checks wired into the gate (`tools/check_integrity.py`), manifest generator fixed, decl inheritance aligned.
- Link audit (2026-09-28): stale repro paths and stale site slugs (e.g. `/disease/`) repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24).

## Claim status (claims ledger)
Counts: anchor-restatement 1 · interpretation 2 · open 1 · identity 0 · independent-prediction 0.
- Headline: burden = raw_burden·(1−e) residual ranking (e.g. PKU 0.3375 r16, CF 0.3075 r17, DMD 0.4760 r6) — anchor-restatement — byte-identical rerun; order moves under reweighting (ρ 0.89–0.98); e are declared bins, not clinical effect sizes.
- Per-disease gene-key mechanism cases (35 disease pages) — interpretation — mechanism reading [H] on observed inputs.
- Mechanism-class grouping (pages 37, 38) — interpretation — observation-based classification, not forced.
- Pipeline gate — open — 15/16; `prior_round_artifacts_preserved` FAIL (R9–R14 digest drift, pre-existing).

## Open items
- 12 [O] and 24 [H] items graded on the pages (manifest); the ranking order is a provisional [H] device.
- Clinical magnitudes [O] by design (magnitude firewall).
- Author decisions (review): apply the two template edits to the remaining disease pages ("[L]/[V]" still on 03, 20, 23; the residual sentence on all placed pages); consider showing the residual score's grade as "code output" rather than [L]; re-freeze or explain the R9–R14 digest drift; run `tools/record_page_notes.py`.

## Reproduction
The ZIP contains `docs/disease_wp/` (the published HTML pages), `repro/disease_wp/` (code and data), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main checks: `python3 repro/disease_wp/code/pipeline/r15_severity_litcurate.py` (the registry files the pages read), `repro/disease_wp/code/pipeline/r3_burden_index.py`, `repro/disease_wp/code/pipeline/r4_burden_residual.py`, and the gate `repro/disease_wp/code/pipeline/r15_gate.py` (15/16 expected until the R9–R14 digests are re-frozen). Governed hashes: `repro/disease_wp/MANIFEST_governed.sha256`.
- SEED not applicable: the ranking scripts use no random sampling and rerun byte-identically. No network needed for the checks; the fetch stages (e.g. `r5_genereviews_fetch.py`, `r7_litsurvival_fetch.py`, `r2_cohort_medgen.py`) need network.

## Citation and links
- Site: https://jamming-physics.org/disease_wp/
- Concept DOI: 10.5281/zenodo.20763842
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
