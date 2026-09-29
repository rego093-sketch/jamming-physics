# Endotherm vs Ectotherm, the Defended Setpoint, and Metabolic Disease

## Summary
This volume (Thermometabolic Homeostasis, tier 7 of the VP corpus) models body temperature and metabolic rate as a defended setpoint: an Ornstein–Uhlenbeck setpoint loop with three correction levers, built on the R19 switch `ṡ = g·s − s³ + h`. It inherits from digestive, aging_senescence and circadian (per the manifest), and its one added module is the OU-setpoint/three-lever loop with an endotherm-vs-ectotherm sensitivity comparison. The headline, setpoint sensitivity 0.054 (endotherm) vs 1.394 (ectotherm), is classed in the claims ledger as an **anchor restatement**: it is set by the chosen loop gains (g_endo = 1.40, g_ecto = 0.18), and moves when those gains move (for example g_endo 1.0 gives 0.107); 1.394 is a collapse fraction above 1, i.e. overshoot into the other well, not one-to-one tracking. A separate finding survives as a code output on measured sequence: promoter γ does not separate endotherms from ectotherms nor mark hibernation (four nulls; the UCP1 gap is GC-confounded). Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to thermoregulation and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation.

## What changed in this version (2026-09-29)
**Corrections**
- Headline 0.054 vs 1.394 relabelled from "[V] simulation-verified" to code output of chosen loop gains; the input dependence is stated on the hub and on `endotherm-vs-ectotherm/`, and the "~26×" ratio is no longer presented as a measurement.
- The meaning of 1.394 corrected: it is a collapse fraction |s−s0|/2s0, and a value above 1 means overshoot past the other well, not "almost one-to-one" tracking.
- Torpor hysteresis width 1.3000 relabelled from [V] to consistency: any bistable cubic has width 2·h_sp (1.275 at g = 1.40); the printed value is a sweep-grid artefact (1.32 / 1.30 / 1.29 / 1.28 at 121–961 points). The text/card mismatch in jump positions (±0.6500 vs ±0.6376) is noted.
- "16/16 stress targets" relabelled from [V] to self-consistency checks of the model, not data tests.
- The four γ nulls (endo/ecto, hibernation) relabelled from [V] to code output on measured promoters; the code's own [O] on the conclusion (small n) is kept.
- Cited observations added next to the claims (Bennett & Ruben 1979; Geiser 2004; Heldmaier et al. 2004). No numeric result was changed and no author text was deleted.

**New experiments and results**
- None. A light two-reviewer review (`reviews/biology/2026-09-29_homeostasis_thermometabolic_review.md`) re-ran the engine functions: printed numbers match the pages exactly (0.053581 / 1.394014; width 1.3, h_sp 0.637588). Magnitude firewall clean: every restoration chapter withholds dose, efficacy and clinical magnitude.

**Relabelled grades / reading rule**
- Biology reading rule note added after the h1 of the hub; claim strips on the hub, `endotherm-vs-ectotherm/` and `torpor-switch/` relabelled (code output / consistency / interpretation). Three correction notes (lt-note) in total.

**Reproduction package changes**
- `repro/homeostasis_thermometabolic/` is unchanged since the 2026-06-24 state. The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Link audit (2026-09-28): stale GitHub repro paths and stale site slugs (e.g. `/thermometabolic/`) on this volume's pages repointed to existing `docs/homeostasis_thermometabolic/` and `repro/` paths (part of a corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Correction notes are now protected: the gate fails if a page loses one (`registry/page_notes.json`).
- Claims ledger entries for this volume published (`registry/claims_ledger.json`, /claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24) that placed the pages and reproduction package in the single corpus repository.

## Claim status (claims ledger)
Counts: anchor-restatement 1 · identity 2 · independent-prediction 1 · interpretation 0 · open 0.
- Headline: endotherm 0.054 vs ectotherm 1.394 setpoint sensitivity — anchor-restatement — set by chosen loop gains; g_endo 1.0 → 0.107, g_ecto 0.30 → 1.246, drive 0.20 → 0.033 / 1.309.
- Torpor hysteresis loop width 1.3000 (h_sp 0.637588) — identity — exact 2·h_sp = 1.275; grid gives 1.32/1.30/1.29/1.28.
- 16/16 stress targets pass — identity — self-consistency checks, not data tests.
- γ does not separate endo/ecto, nor mark hibernation (four nulls) — independent-prediction — null result (group gaps = GC gaps); n small, conclusion [O].

## Open items
- Absolute loop gains are [O] (code docstring); the endo/ecto sensitivities cannot be read as measurements until gains are sourced.
- The γ nulls rest on a small panel; the conclusion is graded [O] by the code.
- No torpor observation is compared numerically with the hysteresis width.
- Therapy/restoration magnitudes are withheld (magnitude firewall); direction only.
- Author decision: the per-page grade labels beyond the three edited pages remain as authored and are covered by the hub reading rule.

## Reproduction
The ZIP contains `docs/homeostasis_thermometabolic/` (the published HTML pages), `repro/homeostasis_thermometabolic/` (code and data), `DESCRIPTION.md`, `LEDGER.json` (this volume's claims-ledger rows), `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main checks: `python3 repro/homeostasis_thermometabolic/repro/run_all.py` (writes `reports/`) and `repro/homeostasis_thermometabolic/repro/_verify/gates.py`.
- Headline and torpor sweeps: `repro/homeostasis_thermometabolic/repro/_engine/endotherm_ectotherm.py` (`setpoint_defense_sweep`) and `repro/homeostasis_thermometabolic/repro/_engine/vp_trm_engine.py` (`torpor_hysteresis_sweep`).
- SEED = 19 (`repro/homeostasis_thermometabolic/inherited/vp_substrate.py`). No network needed, except `repro/homeostasis_thermometabolic/tools/fetch_thermo_panel.py`, which re-fetches the promoter panel.

## Citation and links
- Site: https://jamming-physics.org/homeostasis_thermometabolic/
- Concept DOI: 10.5281/zenodo.20756934
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
