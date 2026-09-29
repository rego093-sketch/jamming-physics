## Summary
This volume (Ionic Homeostasis, tier 7 of the VP corpus) models calcium-phosphate, acid-base and electrolyte balance as defended setpoints: Ornstein–Uhlenbeck setpoint loops, a calcium loop and a two-timescale acid-base buffer, built on the R19 switch. It inherits from musculoskeletal and circadian, and adds one module: the mineral / acid-base / electrolyte setpoint loops. The headline statement (these setpoints, with node identity and order from measured master-gene γ) is classed in the claims ledger as **interpretation**: the "identity and order from γ" part conflicts with the corpus rule (identity from the DNA atlas, order from regulatory-cascade depth, building [O]) and is now bracketed [O] on the hub. The OU setpoint laws are identities of the process, the Winters compensation slope 1.105 is a code output of a chosen controller exponent that falls below the cited range, and one measured-sequence test (ATP1A1 promoter γ does not order six species by loop gain) is a recorded negative. Biology reading rule: the volume accepts established observations and uses them; it shows how the DNA reading (γ) and the VP mapping apply to ionic homeostasis and does not decide theory. Every statement is an observation (cited), a code output (reproducible, input dependence stated), a consistency check (holds by construction), or an interpretation.

## What changed in this version (2026-09-29)
**Corrections**
- Hub: "Node identity and order come from measured master-gene γ" bracketed as interpretation / [O], with a link to /dna/ (order is from regulatory-cascade depth; building is open, dna §RB).
- §3 acid-base: the Winters slope 1.105 was presented as "matching ~1.2–1.5"; it is now stated as a code output of the chosen controller pCO₂* = 40·(HCO₃/24)^0.6 that lies below the range the page quotes (Albert, Dell & Winters 1967; the code gate accepts 1.0–1.6). The pH return to 7.401 is marked as holding by construction.
- §1: the OU laws (Var·2k/σ² = 1, error·k = 1, zero integral error) relabelled from [V] to consistency (identities of the OU process); "γ supplies k" relabelled as interpretation.
- §2 calcium: values marked as dependent on the chosen load and deficit; the negative deficit nadir (−0.0435) is flagged as non-physical; only return to setpoint is a loop property.
- Measured γ values labelled "[V] measured input" read as code outputs on measured sequence. No numbers or author text removed.

**New experiments and results**
- None. A light review (`reviews/biology/2026-09-29_homeostasis_ionic_review.md`) re-ran `ri1_calcium()` and `ri2_acidbase()`; printed numbers match the pages (pH 7.167 / 7.307 / 7.401, slope 1.105; peak 2.1283, nadir −0.0435, final 1.0003). Network fetchers were not run. Firewall clean: dosing is [O] throughout.

**Relabelled grades / reading rule**
- Biology reading rule note added to the hub; claim strip on §1 changed from "[V] mechanism" to "code output + consistency; γ→k interpretation"; brackets added on §1–§3. One correction note (lt-note) on the hub.
- Manifest grade counts set to forced 0 / verified 0 (previously 18 / 31); open 17 unchanged. `_decl.json` regenerated.

**Reproduction package changes**
- `repro/homeostasis_ionic/` is unchanged since the 2026-06-24 state. The release ZIP is now built deterministically by `tools/build_release.py` and adds LEDGER.json and MANIFEST.sha256.

**Site/metadata**
- Registry integration of the reading rule for this volume (manifest, page_notes, hashes, lineage, homepage, sitemap; gate clean).
- Link audit (2026-09-28): stale repro paths and stale site slugs (e.g. `/homeostasis-ionic/`) repointed to existing paths (corpus-wide repair of 6,642 links).
- Highwire citation meta generated for the hub from the manifest; gate guards against escaped comments, raw LaTeX and citation-meta drift.
- Gate fails if a page loses a correction note (`registry/page_notes.json`); claims ledger entries published (/claims-ledger/).
- Initial repository import and consolidation commits (2026-06-20 "VP Theory site", 2026-06-22 "Final", 2026-06-24).

## Claim status (claims ledger)
Counts: interpretation 2 · identity 1 · anchor-restatement 1 · independent-prediction 1 · open 0.
- Headline: mineral / acid-base / electrolyte setpoints; identity and order from measured master-gene γ — interpretation — conflicts with AGENTS.md / dna §RB; bracketed [O].
- OU setpoint laws (Var·2k/σ² = 1, error·k = 1, zero integral error) — identity — 1, 1, 0 by the OU process; "γ supplies k" is interpretation.
- Winters compensation slope — anchor-restatement — 1.105 below the cited ~1.2–1.5; set by chosen controller exponent (not fitted; it misses); pH 7.401 return by construction.
- Calcium setpoint loop return — interpretation — values depend on chosen load/deficit; negative nadir non-physical.
- ATP1A1 promoter γ does not order species by loop gain — independent-prediction — null (honest negative on measured sequence across six species).

## Open items
- 17 [O] items stated on the pages (manifest open = 17): absolute magnitudes and clinical efficacy (magnitude firewall; dosing [O] throughout), the γ → absolute value mapping, incidence, and node developmental order / building (dna §RB).
- Controller exponent for acid-base compensation is chosen, not sourced; the slope does not reach the cited range.
- Author decision: remaining per-page grade labels are left as authored and covered by the hub reading rule.

## Reproduction
The ZIP contains `docs/homeostasis_ionic/` (the published HTML pages), `repro/homeostasis_ionic/` (code and data), `DESCRIPTION.md`, `LEDGER.json`, `CORPUS_GUIDE.md` (AGENTS.md) and `MANIFEST.sha256`.
- Main checks: `python3 repro/homeostasis_ionic/repro/run_all.py` and `repro/homeostasis_ionic/repro/_verify/gates.py`.
- Loops: `repro/homeostasis_ionic/repro/_engine/vp_loops.py` (`ri1_calcium`, `ri2_acidbase`).
- SEED = 19 (`vp_loops.py`, `inherited/vp_substrate.py`). No network needed for the checks; `repro/homeostasis_ionic/repro/_engine/fetch_gamma.py` and `comparative_gamma.py` re-fetch promoter sequence and need network.

## Citation and links
- Site: https://jamming-physics.org/homeostasis_ionic/
- Concept DOI: 10.5281/zenodo.20755910
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
