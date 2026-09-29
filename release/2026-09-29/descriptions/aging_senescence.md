# Aging & Senescence — a VP Theory volume

## Summary
This volume (tier 7 of the VP corpus) reads aging as the drift of defended homeostatic setpoints over time on the R19 switch, with a node table of measured promoter γ for aging master genes (TP53, CDKN2A, FOXO3, TERT), deterministic simulations of setpoint drift, a stuck senescence attractor, reservoir (telomere) depletion and a shared aging axis, and a cross-species longevity discriminant. It inherits from dna, and adds one module: setpoint drift over time, with the cross-species test of whether aging genes are special. The headline, human aging genes are not special in promoter γ (|z| < 1; TP53 CV 3.52 %, human z 0.088, permutation p 0.114), is classed in the claims ledger as an **independent prediction** with a null result on measured sequence; the reading that the longevity lever is TP53 copy number is an interpretation of cited cancer-resistance data. Most other headline numbers (cancer-incidence rise, barrier-shrink hazard ratio, one aging axis, senescence fraction) are anchor restatements set by chosen model inputs, and the cross-species lifespan span is corrected from "fifty-fold" to about 32-fold. Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to aging and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation.

## What changed in this version (2026-09-29)
**Corrections**
- Input dependence stated for the headline numbers: 52.3× cancer-incidence rise is set by the Armitage–Doll stage count (25.0 / 52.3 / 107.9× at 5 / 6 / 7 stages) and contains no barrier/Kramers term despite §7's wording; the §12 hazard ratio 135× equals exp(Δb/T) with chosen T (about 18,000 / 135 / 12× at T = 0.05 / 0.1 / 0.2); §8 PCA-1 share 0.889 comes from synthetic curves of one functional form (0.986 / 0.889 / 0.682 with noise); §4 senescence fraction 0.391 depends on the base hazard (0.224 / 0.391 / 0.625).
- Cross-species lifespan span corrected: hub, §9 and §14 said "4–211 yr, fifty-fold"; the bowhead has no γ, so the data span is 3.8–122.5 yr, about 32-fold. The previous Zenodo abstract's "fifty-fold" is superseded.
- Order from γ corrected: §2 "emergence order by ascending γ" and §14 "γ fixes what and in what order" conflict with the corpus rule (order from regulatory-cascade depth; building [O], dna §RB).
- Interpretation no longer stated as fact: §9 "TP53 copy number is the longevity switch" is an interpretation of cancer-resistance observations (Abegglen 2015; Sulak 2016); §4 "senescence is irreversible" is qualified by reversal on p53/p16 inactivation in some cells (Beauséjour 2003).
- By-construction results relabelled from [V] to consistency: §5 depletion steps = γ^1.5 / 0.02; §6 hallmark table hand-entered ("no orphans" guaranteed); §11 telomere-repeat γ and strand symmetry follow from the table.
- Hallmarks coverage noted: the map uses the 10-item list; the 2023 update has 12 (disabled macroautophagy and dysbiosis unmapped). The §10 present-day TP53 γ (1.4333) vs §2 atlas value (1.4298) difference is flagged as unexplained.
- Cited observations added per chapter (López-Otín 2013, 2023; Dimri 1995; Krishnamurthy 2004; Beauséjour 2003; Hayflick 1965; Harley 1990; Armitage & Doll 1954; Oh 2023; Fried 2001). No numbers changed, nothing deleted.

**New experiments and results**
- None. A light review (`reviews/biology/2026-09-29_aging_senescence_review.md`) re-ran `run_all.py` (battery completed; gates step hit the 120 s limit), RA1–RA6 and `xspecies_discriminant.discriminant()`, plus parameter reruns for the input-dependence figures above. Printed numbers match the pages. Firewall clean.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub (labels, input-dependent headlines, corrected span); one lt-note on each of §1–§14 (15 correction notes on 15 pages).
- Manifest grade counts set to forced 0 / verified 0 (previously 8 / 31); open 3 unchanged. `_decl.json` regenerated.

**Reproduction package changes**
- `repro/aging_senescence/` is unchanged since the 2026-06-24 state (the whitepaper PDF/TeX v1.4.0 and `ZENODO_METADATA.md` inside it still carry the pre-correction wording, including "fifty-fold"; the HTML pages are the corrected source). The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Registry integration of the reading rule (manifest, page_notes, hashes, lineage, homepage, sitemap; gate clean); work-in-progress snapshot and review commits for this volume.
- Link audit (2026-09-28): stale repro paths (e.g. `aging/`) and stale site slugs repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24).

## Claim status (claims ledger)
Counts: independent-prediction 1 · anchor-restatement 4 · identity 1 · open 1 · interpretation 0.
- Headline: human aging genes not special in promoter γ (|z| < 1; TP53 CV 3.52 %, human z 0.088, perm p 0.114) — independent-prediction — null (z includes the human value); TP53-copy-number reading is interpretation.
- Cancer incidence rise with age (52.32×) — anchor-restatement — 25.0 / 52.3 / 107.9× at 5 / 6 / 7 stages.
- Barrier-shrink hazard ratio, §12 (135×) — anchor-restatement — = exp(Δb/T), set by chosen T.
- One aging axis, PCA-1 share §8 (0.889) — anchor-restatement — 0.986 / 0.889 / 0.682 at noise 0.05 / 0.15 / 0.30.
- Senescence fraction, §4 (0.391) — anchor-restatement — 0.224 / 0.391 / 0.625 at base hazard 0.006 / 0.012 / 0.024; irreversibility claim conflicts with Beauséjour 2003.
- Depletion steps, hallmark coverage, telomere-repeat γ (89 / 78 steps; no orphans; γ 7.98 / 6) — identity — steps = γ^1.5 / 0.02; hand-entered table; table symmetry.
- Lifespan span of the γ panel (stated 4–211 yr, fifty-fold) — open — data span 3.8–122.5 yr (~32-fold); bowhead has no γ.

## Open items
- Three [O] items stated on the pages (manifest open = 3): the absolute calendar rates, incidences and lifespans are uncomputed (they need an external clock or calibration); the realized-lifespan lever lies off the γ axis (underdetermined by promoter sequence); developmental order and building stay [O] (dna §RB).
- The corrected span is carried by correction notes; the original "fifty-fold" / "4–211 yr" wording remains in the author's body text on the hub, §9 and §14.
- Hallmarks map to be extended to the 2023 12-item list.
- Explain or reconcile the TP53 γ difference between §10 (1.4333) and §2 (1.4298).
- Author decision: update the whitepaper PDF/TeX and `ZENODO_METADATA.md` in `repro/aging_senescence/` to the corrected span and labels.
- The gates step of `run_all.py` exceeded 120 s in review.

## Reproduction
The ZIP contains `docs/aging_senescence/` (the published HTML pages), `repro/aging_senescence/` (code, data, whitepaper v1.4.0 PDF/TeX), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main checks: `python3 repro/aging_senescence/repro/run_all.py` and `repro/aging_senescence/repro/_verify/gates.py`; robustness audit `repro/aging_senescence/repro/_verify/xspecies_robustness_audit.py`.
- Dynamics RA1–RA6: `repro/aging_senescence/repro/_engine/aging_dynamics.py`; cross-species test: `repro/aging_senescence/repro/_engine/xspecies_discriminant.py`.
- SEED = 19. No network needed for the checks; `repro/aging_senescence/repro/_engine/fetch_gamma_xspecies.py` re-fetches promoters and needs network.

## Citation and links
- Site: https://jamming-physics.org/aging_senescence/
- Concept DOI: 10.5281/zenodo.20756155
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
