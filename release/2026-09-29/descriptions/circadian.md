# Chronobiology — the circadian oscillator network, entrainment, and clock-disruption disease

## Summary
This volume (Circadian Oscillator, tier 7 of the VP corpus) is the time layer of the biology tiers: a relaxation (FitzHugh–Nagumo-type) oscillator network built on the R19 switch, with entrainment, a phase-response curve, master-vs-network coupling, setpoint gating, misalignment disease and a chronotherapy direction. It inherits from dna, and adds one module: the time layer, with the measured BMAL1/ARNTL promoter γ = 1.33348 (2501 bp, GC 0.443) as its DNA reading. The headline is classed in the claims ledger as **interpretation**: γ recomputes bit-for-bit from the cached promoter, but every oscillator in the engine runs at γ = 1.0, so "the clock is seeded by the measured γ" holds only for the node table, not for the dynamics. Clock emergence from a single cell was not attempted and is [O], because published clock rate constants are fitted to a ~24 h period and letting 24 h "emerge" from them would be circular. Biology reading rule: the volume accepts established observations of the clock (a free-running period near 24 h, light entrainment, the phase-response curve, shift-work findings) and uses them; it shows how the DNA reading (γ) and the VP mapping apply and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation.

## What changed in this version (2026-09-29)
**Corrections**
- Hub, §0, §1: "a measured input graded [V]" relabelled "DNA reading"; §0 notes that the oscillators run at γ = 1.0 (`vp_clk_engine.py` l.116–295), so the measured γ does not enter the dynamics.
- §6: the "PRC-bounded" jet-lag re-entrainment rate is stated as a code input (`max_shift_per_cycle`), not a derived result; the observation it restates (Aschoff 1975; Waterhouse 2007) is cited.
- §8 chronotherapy: marked as arithmetic on entered values; the light/melatonin antiphase follows from two hard-coded phases, not from a reproduced effect; direction/class only (no dose, lux or timing window).
- §5–§7: results that hold by construction relabelled from [V] to consistency (ablated constant drive gives amplitude 0; alignment and flattening indices are cosine projections; `sign_consistent_with_mind` is set True in code).
- §3: Arnold-tongue counts noted to saturate at the sweep size (15 of 15).
- Missing observations cited: human period ~24.2 h (Czeisler 1999), human light PRC (Khalsa 2003), peripheral self-sustained clocks (Yoo 2004), IARC Monograph 124. No numbers changed, nothing deleted.

**New experiments and results**
- Simple-tissue (single-cell) clock emergence assessed alongside the neuro EM2 squid-axon experiment and left [O] with the reason stated on the hub (clock constants are period-fitted; no sourced constants). No new experiment was run on this volume.
- Light review (`reviews/biology/2026-09-29_circadian_review.md`) re-ran the RC1–RC6 and TX1 probes; every printed number matches the pages (free run 76 beats, cv 0.003691; PRC +0.185 / −0.129; tongue [5, 11, 15, 15, 15]; coherence 0.596 → 0.99993). `run_all.py` did not finish within 120 s. Firewall clean.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub; one lt-note with input dependence or consistency status on each of §0 and §2–§8 (nine correction notes on nine pages, including the emergence [O] update).
- Manifest grade counts set to verified 0 (previously 7). `_decl.json` regenerated.

**Reproduction package changes**
- `repro/circadian/` is unchanged since the 2026-06-24 state. The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Registry integration of the reading rule (manifest, page_notes, hashes, lineage, homepage, sitemap; gate clean); work-in-progress snapshot and review commits for this volume.
- Link audit (2026-09-28): stale repro paths and stale site slugs repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24).

## Claim status (claims ledger)
Counts: interpretation 3 · anchor-restatement 2 · identity 1 · independent-prediction 0 · open 0.
- Headline: measured BMAL1/ARNTL γ = 1.33348 seeds the clock — interpretation — γ recomputes bit-for-bit, but all oscillators run at γ = 1.0.
- Free-running oscillation precision (76 beats, cv 0.003691) — interpretation — model output of chosen parameters; human period ~24.2 h not compared numerically.
- Entrainment PRC and Arnold tongue — interpretation — tongue saturates at sweep size; human light PRC not compared.
- Jet-lag re-entrainment, PRC-bounded — anchor-restatement — rate is a code input.
- Chronotherapy: light and melatonin act in antiphase — anchor-restatement — direction/class only; arithmetic on entered phases.
- Gating ablation, misalignment and flattening indices — identity — hold by construction.

## Open items
- Single-cell clock emergence [O]: no sourced, non-period-fitted rate constants.
- Making the measured γ enter the oscillator dynamics (currently γ = 1.0 throughout) is not done.
- Quantitative comparison with the human period and human light/melatonin PRCs is not done.
- Chronotherapy timing and any dose are withheld (magnitude firewall); direction only.
- `run_all.py` exceeds 120 s in review; full-battery timing is not recorded.

## Reproduction
The ZIP contains `docs/circadian/` (the published HTML pages), `repro/circadian/` (code and data), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main checks: `python3 repro/circadian/repro/run_all.py` (long-running) and `repro/circadian/repro/_verify/gates.py`; individual probes RC1–RC6 and TX1 in `repro/circadian/repro/_engine/vp_clk_engine.py`.
- SEED = 19 (`vp_clk_engine.py`, `inherited/vp_substrate.py`). No network needed (the ARNTL promoter is cached).

## Citation and links
- Site: https://jamming-physics.org/circadian/
- Concept DOI: 10.5281/zenodo.20755413
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
