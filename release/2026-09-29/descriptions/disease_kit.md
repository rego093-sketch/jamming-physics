# VP Disease Kit — contents

## Summary
This volume (Rare Disease Reproduction KIT, tier 8 of the VP corpus) is a per-disease reproduction kit for 839 monogenic rare diseases: for each, it reads the causal gene's promoter γ, places the lesion on the R19 cusp (barrier γ²/4, spinodal), and states a corrective direction under a structure-only firewall, with magnitude [O]. It inherits from disease_wp, and adds one module: the per-disease corrective direction, now labelled an interpretation, with magnitude [O]. The headline is classed in the claims ledger as **interpretation**: in code the corrective sign is `−DIRINT[emergent_axis_direction]`, and the axis direction follows the curated lesion role × mechanism (LOF → supply, GOF → reduce), not γ; γ sets only the barrier size and spinodal. The recovery of established standard of care (322 match / 29 novel / 488 hold of 839) is an **identity**-class consistency check, largely by construction, not independent validation. Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to each disease and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation. The magnitude firewall is absolute: direction only, no dose, concentration, regimen or effect size.

## What changed in this version (2026-09-29)
**Corrections**
- Headline relabelled: "per-disease corrective direction [F], magnitude [O]" → "per-disease corrective direction (interpretation), magnitude [O]" (manifest, `make_manifest`, `build_index`, AGENTS.md, hub).
- "Corrective direction is forced [F]" replaced on the hub, §01, §03 and all 839 disease pages by "an interpretation of the model (a code output whose sign follows from the cited lesion role and mechanism)"; emergent-axis "DOWN/UP [F]" → "(cited role × mechanism)"; switch/disease-direction [F] tokens removed.
- "Recovering the standard of care" as "genuine validation" → "consistency check, partly by construction" (hub, §03; "validation signal for the logic" replaced on 319 pages; the VALIDATION SIGNAL key annotated on 839 pages).
- R19 cusp geometry "[V] verified" → "code output" in the evidence tables of all 839 pages (barrier = γ²/4 and s_on = ±√γ are algebraic identities; AADC 1.3688 → 0.4684 / 0.6164 checked).
- Each template replacement was an exact string with an asserted count; no [F] or [V] token remains on any disease page; "direction only [O]" and "magnitude [O]" unchanged. No numeric change.

**New experiments and results**
- None. Light two-reviewer review (`reviews/biology/2026-09-29_disease_kit_review.md`): `repro/disease_kit/repro/run_all.py` OVERALL PASS (6 stages; 72 resolved, 13 suspended; all per-disease, module, site and system-inheritance hashes drift 0). Counts reconcile (322 + 29 + 488 = 839). Coverage gap found: the in-repo package is v0.32 with 85 disease analyses, while the site is release 0.42.1 with 839 disease pages, so about 750 pages lack an in-repo reproduction path.
- Magnitude-firewall audit (corpus lineage, 2026-09-29): 0 hits for doses, concentrations, regimens or targets; every page repeats the no-dose notice; one borderline qualitative dosing phrase in a §03 table row (no number) noted.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub (one correction note); the [F] badges and "[F] forced" legend → "interpretation". Manifest grades: forced 0 / verified 0, open 846.

**Reproduction package changes**
- `repro/disease_kit/` is unchanged since the 2026-06-24 state (package v0.32.0). The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Registry integration of the reading rule and of the disease_kit relabel (manifest, `make_manifest`, `build_index`, AGENTS.md, page_notes, hashes, lineage, homepage, sitemap; gate clean).
- Link audit (2026-09-28): stale repro paths and stale site slugs (e.g. `/disease/`) repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final" — 871 disease_kit pages — and 2026-06-24).

## Claim status (claims ledger)
Counts: interpretation 1 · identity 2 · open 1 · anchor-restatement 0 · independent-prediction 0.
- Headline: per-disease corrective direction, magnitude [O] — interpretation — sign follows curated LOF/GOF lesion role × mechanism, not γ; γ sets only barrier/spinodal.
- Recovery of standard of care as validation (322 match / 29 novel / 488 hold of 839) — identity — agreement largely by construction; consistency check, not independent validation.
- R19 cusp geometry per disease (e.g. AADC γ 1.3688; barrier 0.4684; spinodal 0.6164) — identity — γ²/4, √γ algebra on measured γ.
- Reproducibility of site release 0.42.1 — open — 85 of 839 diseases have in-repo repro (run_all PASS for the 85); ~750 pages lack a reproduction path (package v0.32).

## Open items
- Magnitude [O] for every disease (magnitude firewall); agents are mechanism-direction labels graded [O]; 846 [O] items on the pages (manifest).
- Publish the 0.42.1 reproduction inputs for the roughly 750 disease pages that lack them.
- Author decisions (review): reword §03's heading "Why a recovery counts as validation" and the sentence "main evidence … tracking real biology"; update `repro/disease_kit/tools/build_disease_site.py`, which still emits the old [F]/[V] labels (do not rebuild into `docs/`); run `tools/record_page_notes.py`.

## Reproduction
The ZIP contains `docs/disease_kit/` (the published HTML pages: hub, 6 section pages, 839 disease pages under `dz/`), `repro/disease_kit/` (code and data, package v0.32.0), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main check: `python3 repro/disease_kit/repro/run_all.py` (6 stages, hash drift report); direction logic `repro/disease_kit/pipeline/treatment_switch.py`; gates `repro/disease_kit/pipeline/honesty_gate.py`, `repro/disease_kit/pipeline/indirect_lever_gate.py`; per-disease analyses in `repro/disease_kit/diseases/` (registry `diseases/_registry.json`).
- SEED = 19 (engine and validation scripts). No network needed for `run_all.py`; `repro/disease_kit/fetch/` and the `validation/_v*_fetch_*.py` scripts need network.

## Citation and links
- Site: https://jamming-physics.org/disease_kit/
- Concept DOI: 10.5281/zenodo.20755262
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
