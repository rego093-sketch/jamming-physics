## Summary
This volume (tier 7 of the VP corpus) treats arterial pressure as a defended setpoint: `MAP = CVP + CO×SVR` held by a baroreflex (proportional) loop and a renal integral controller, with hypertension read as a reset of the defended reference and heart failure as a shrinking barrier margin on the R19 switch. It inherits from cardioresp, circulatory and circadian, and adds one module: the defended `MAP = CVP + CO×SVR` loop. The headline, MAP = 93 mmHg with error 0, is classed in the claims ledger as an **identity**: SVR is derived from the 93 mmHg target (SVR = (93 − 4)/5 with cited resting CO 5 L/min and CVP 4 mmHg), so the closure holds by construction. The therapy reading (resetting the reference is durable, an operating-point push is transient) is kept as a direction only; its sizes are chosen model inputs and are withheld from the pages under the magnitude firewall. Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to blood-pressure control and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation.

## What changed in this version (2026-09-29)
**Corrections**
- Therapy sizes withheld (magnitude firewall): the reset, operating-point-drug and reference-reset sizes in `_therapy/fundamental_targets.py` are chosen model inputs returned 1:1 by the integral controller. Pages (§6, §9, §13, hub via §14, hypertension-reset, fundamental-therapy, comfort-logic) now state directions only ("size = chosen model input"); the earlier numeric durable/transient drops are removed from the text.
- CAL6 (agreement of the model's durable drop with the cited renal-denervation observation) recorded as circular: it compares a chosen input with the citation. CAL1, CAL2 and CAL5 marked as consistency/arithmetic.
- Headline MAP = 93 mmHg "error 0" relabelled from [V] to consistency (arithmetic on cited inputs), with observed ranges (Guyton & Hall) and the SVR construction stated.
- Baroreflex residual (75 % buffered, 1/(1+G) with anchored G = 3) and "perfect adaptation, spread 0" (defining property of integral control) relabelled as consistency.
- "Node identity fixed by master-gene γ" and "kidney developmental order (DNA)" clarified: identity comes from the DNA atlas, γ sets the switch threshold, and building (including order) is [O] (dna §RB).
- Comfort proposal and prioritisation (§17, §18) relabelled from [F] forced to interpretation.

**New experiments and results**
- None. A light two-reviewer review (`reviews/biology/2026-09-29_homeostasis_hemodynamic_review.md`) re-ran `_therapy/fundamental_targets.py`, `map_from_seams()` and `rp2_baroreflex()`; printed numbers match the pages.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub; TOC grade labels changed ("[V] sim-reproduced" → "code output"; §1 → "consistency (arithmetic)"; §17–§18 "[F]" → "interpretation"). Six correction notes (lt-note) across six pages.
- Manifest grade counts for this volume set to forced 0 / verified 0 (previously 14 / 65); open 5 unchanged. `_decl.json` regenerated.

**Reproduction package changes**
- `repro/homeostasis_hemodynamic/` is unchanged since the 2026-06-24 state. The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Registry integration of the reading rule (manifest, page_notes, hashes, lineage, homepage, sitemap refreshed; gate clean); lineage entry records the withheld therapy sizes.
- Link audit (2026-09-28): stale GitHub repro paths and stale site slugs on this volume's pages repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24).

## Claim status (claims ledger)
Counts: identity 2 · anchor-restatement 2 · interpretation 3 · independent-prediction 0 · open 0.
- Headline: MAP = CVP + CO×SVR = 93 mmHg, error 0 — identity — 0 by construction (SVR derived from the 93 target).
- Hypertension reset and therapy: durable vs transient lowering — anchor-restatement — direction/class only; output equals the chosen input (varies 1:1); CAL6 circular.
- Baroreflex residual fraction (75 % buffered, 1/(1+G)) — anchor-restatement — set by anchored gain G = 3.
- Perfect adaptation of the integral controller (spread 0) — identity — defining property of integral control.
- Heart-failure margin sign (+0.180 / −0.139) — interpretation — model outputs; sign read against cited trials (PROMISE, PARADIGM-HF).
- Node identity fixed by master-gene γ; kidney order from DNA — interpretation — conflicts with AGENTS.md / dna §RB (identity from atlas, order [O]).
- Comfort proposal and prioritisation — interpretation — biological hypotheses and ranking.

## Open items
- Five [O] items stated on the pages (manifest open = 5): absolute first-principles scales are left open, with obstacles named in `repro/homeostasis_hemodynamic/IRREPRODUCIBILITY_LEDGER.md` (absolute calibration chapter), and the §20 comfort firewall (a structural prediction with no medical responsibility) is [O].
- Developmental order and building of the nodes stay [O] (dna §RB).
- Therapy magnitudes: [O] by design (magnitude firewall); direction only.
- Author decision: whether to keep the durable-drop figure on these pages at all, given the firewall (the review's "needs author" item; pages now state it as a chosen input).
- Author decision: per-page [V] badges in sub-pages are left as authored and covered by the hub reading rule.

## Reproduction
The ZIP contains `docs/homeostasis_hemodynamic/` (the published HTML pages), `repro/homeostasis_hemodynamic/` (code and data), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main checks: `python3 repro/homeostasis_hemodynamic/repro/run_all.py` and `repro/homeostasis_hemodynamic/repro/_verify/gates.py` (see `repro/homeostasis_hemodynamic/repro/REPRODUCE.md`).
- Loops and headline: `repro/homeostasis_hemodynamic/repro/_engine/vp_hmd_loops.py` (`map_from_seams`, `rp2_baroreflex`); therapy directions: `repro/homeostasis_hemodynamic/repro/_therapy/fundamental_targets.py`.
- SEED = 19 (`repro/homeostasis_hemodynamic/inherited/vp_substrate.py`). No network needed.

## Citation and links
- Site: https://jamming-physics.org/homeostasis_hemodynamic/
- Concept DOI: 10.5281/zenodo.20756801
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
