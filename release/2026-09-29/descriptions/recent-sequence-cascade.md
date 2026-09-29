# The VP Recent-Sequence Cascade

## Summary
The VP Recent-Sequence Cascade inherits from the continental-genesis, physics, geodynamics and dna volumes and adds one module: a coupled Flood → Glaciation → Atlantic-opening relaxation driven by the release of a jammed deep-water reservoir (S0). The volume states its own level of claim: it is a construction, not a claim about history — whether the cascade occurred is [O] in both directions, and absolute dates are kept as record only. Its headline, one relaxation read as flood, ice and Atlantic, is physically permitted, with an 8:1 compression in the number of mechanisms and fitted parameters relative to the mainstream graded [L]; the claims ledger classes it as interpretation, because 8:1 is a parsimony count, not a likelihood, and it rests on the S0 release (SH-5), which is [O]. The volume's own stress test (M52) finds no present-tense observable that discriminates it from the mainstream (all six discriminators degenerate).

## What changed in this version (2026-09-29)
**Corrections**
- Headline graded as the body states: "one cause closes 9 present-tense phenomena (8:1 vs mainstream)" replaced by "one relaxation read as flood, ice, Atlantic — physically permitted, occurrence open [O]; mechanism compression 8:1 [L], no present-tense discriminator" in the manifest; the homepage card, which displayed 8:1 without its grade, fixed to match the body (light review, fix 1).

**New experiments and results**
- None. A light review (reviews/earth/2026-09-29_continental_genesis_and_cascade_light_review.md) read the volume in full: all 6 cited files exist, the inherited engine reruns at 39/39, and the fossil audit runs on 179,689 radiocarbon dates.

**Relabelled grades / reading rule**
- The headline now carries the body's grades (occurrence [O]; 8:1 [L]); no page grade changed.

**Reproduction package changes**
- None to repro/recent-sequence-cascade/.

**Site/metadata**
- Highwire citation meta regenerated from the manifest for the hub; corpus bookkeeping (orphan merged continental-genesis-cascade hub removed; manifest generator now carries all 32 volumes; homepage and corpus-guide counts regenerated; corpus integrity checks in the gate).

## Claim status (claims ledger)
6 rows: interpretation 3 · anchor-restatement 2 · open 1.
- One untuned cause (S0 release) closes 9 present-tense phenomena; 8:1 mechanism compression vs mainstream (headline) — interpretation — 8:1 [L] is a parsimony count, not a likelihood; rests on S0 release (SH-5) [O].
- Deglaciation is recent (order 10⁴ yr) because post-glacial rebound is ongoing — anchor-restatement — η = 10²¹ Pa·s comes from GIA inversions that assume the deglacial load history, so recency is partly built in; mainstream GIA gives the same order.
- Dual-redox glacial meltwater model reproduces oil quality across provinces — anchor-restatement — 6/6 class matches; API weights hand-set and per-province scores assigned, not independently measured.
- Early-Holocene human remains are sparse in the global radiocarbon record — interpretation — raw counts over 179,689 dates reproduce ([V] as an observation); attributing a cause is [O].
- Stress test vs mainstream — interpretation — 0 discriminating present-tense advantage; all 6 discriminators degenerate.
- Occurrence of the cascade and absolute dates — open — [O] in both directions; dates kept as record only.

## Open items
- Occurrence of the cascade (Flood → glaciation → Atlantic opening): [O] in both directions.
- S0 release (SH-5): the deep-water inventory bound exceeds the largest requirement by ~10× [V] (M50), but the releasable fraction and mechanism stay [O].
- No present-tense discriminator against the mainstream (M52); a discriminating observable remains to be found.
- Inherited geodynamics engine pairs the 2-D φ_jam = 0.840 with the 3-D z_iso = 6: numeric fix deferred (light review, fix 2).

## Reproduction
The ZIP contains docs/recent-sequence-cascade/ (the published HTML pages), repro/recent-sequence-cascade/ (code and data, with its own README, reproducibility map, data checklist, glossary and MANIFEST.sha256), LEDGER.json (this volume's claims-ledger rows), CORPUS_GUIDE.md and MANIFEST.sha256 (SHA-256 of every file).
Main checks (Python 3, offline unless stated):
- `python3 repro/recent-sequence-cascade/repro/verify_all.py` and the module screens in that folder (e.g. m47_causal_closure_ledger.py for 8:1, m50_s0_reservoir_budget_bound.py, m52_tier4_mainstream_stress_test.py, m44_deglaciation_recency_gia.py, m42_oil_quality_model.py).
- `python3 repro/recent-sequence-cascade/inherited_engine/validate_all.py` — inherited geodynamics engine, 39/39 PASS.
- `python3 repro/recent-sequence-cascade/fossil_audit/fossil_counts.py` — radiocarbon fossil counts.
- dna_emergence/animal/repro/run_all.py and dna_emergence/plant/repro/run_all.py (fetch_ncbi.py needs network to refresh inputs).
Deterministic scripts use SEED = 19.

## Citation and links
- Site: https://jamming-physics.org/recent-sequence-cascade/
- Concept DOI: 10.5281/zenodo.20827806
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
