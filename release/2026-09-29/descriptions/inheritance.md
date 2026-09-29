# VP Inheritance — environmental inheritance on one switch

## Summary
VP Inheritance reads heritability as one R19 switch with two channels. It inherits the γ ruler, the A4 coordinate and the node atlas from `dna`, and adds one module: an unwritable γ ruler (SET) plus a writable A4 coordinate. On that basis it covers environmental inheritance, the RNA layer and a gene-therapy lever path. The headline "one switch, two channels: γ (SET) + writable A4" is unchanged in wording. It is now ledgered as an **interpretation**; it was formerly graded [F], and the decomposition has no numeric test. The volume's only held-out test, that γ ordering predicts CRISPRi knockdown resistance (Replogle 2022), is recorded as a **null**: ρ = −0.076, p = 0.63, K562, n = 43. Because γ and GC are near-collinear, that test cannot separate γ from GC. The biology reading rule applies to every page. The volume accepts established observations and uses them. Each statement is an observation (cited), a code output (input dependence stated), a consistency check (holds by construction) or an interpretation. The magnitude firewall holds: every dose, titre, interval and schedule is [O], and the only numbers are in model units.

## What changed in this version (2026-09-29)
**Corrections**
- §1: the SET/drive decomposition was relabelled from [F] to interpretation. The page cites a counter-observation: the environment can also mutate DNA (Kong 2012).
- §14: the corrective sign was relabelled as observation plus interpretation. It recovers the textbook oncogene/suppressor classification (Vogelstein 2013).
- §6: the claim that imprinted escapees survive both erasures is flagged as conflicting with observation. Imprints are erased in primordial germ cells and reset by sex (Hajkova 2002; Reik & Walter 2001). ρ = 1.00 at fixed D holds by construction.
- §11 and §18 (gene-therapy lever map): the γ edit sizes are flagged as entered model values that are not physically plausible. A single base substitution moves promoter γ by at most about 0.0013. Coding edits do not change promoter γ. Gene addition (AAV) is missing from the map. γ* follows from the chosen h_cap. Only the direction is given.
- Results true by construction were flagged as consistency, not [V]:
  - §4: add, veto and latch.
  - §5: p² and γ-ranked survival at fixed D.
  - §12 and §13: spinodal monotonicity.
  - §16: the 13/13 paternal/maternal asymmetry, which follows from a paternal burst shorter than the crossing time.
  - The "18/18 green" scoreboard, which counts in-model checks.
- Grid and parameter artefacts were disclosed:
  - §9: the "optimum at 0.40" is the first point of a plateau.
  - §7: the maternal contact fraction of 0.00 rests on n = 2.
  - §8: the MFPT values differ by about 2%.
  - §17: the saRNA vs mRNA difference depends on the chosen windows.
  - FV8: only 3 of 7 GOF genes fall on the predicted side.
- Missing observations were cited on the relevant chapters:
  - two demethylation waves (Seisenberger 2012);
  - *C. elegans* small-RNA inheritance (Rechavi 2011);
  - sperm tsRNA (Chen 2016; Sharma 2016);
  - the mammalian debate (Heard & Martienssen 2014);
  - trained immunity and its disputed inheritance (Netea 2016; Katzmarski 2021; Kaufmann 2022);
  - antibody waning with persistent memory B cells after mRNA vaccination (Levin 2021; Goel 2021);
  - approved siRNA, ASO, editing and AAV therapies.

**New experiments and results**
- None new. The existing held-out results were re-run by the reviewer, and the printed numbers match the pages: TG5 series 0.45 / 0.7238; FV8 point-biserial 0.4852, p 0.0274, GC-partialled 0.4731.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub. The two chapter-list [F] tags became "interpretation".
- Each of the 19 chapters and the hub carries one note stating its input dependence, its consistency status, or the conflicting and missing observations (20 notes). No number was changed and nothing was deleted.

**Reproduction package changes**
- None to code. The reviewer re-ran `engine/env_to_germline.py`, `engine/lever_map.py` and `engine/feasibility_validation.py`, and the outputs match the pages.

**Site/metadata**
- The volume was integrated into the corpus site and repository (docs + repro, 2026-09-29).
- The biology reading rule was integrated into the registry for 16 volumes, including this one. Manifest forced/verified counts were set to 0 (previously 4 forced / 35 verified); `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed; the gate is CLEAN.
- The corpus link audit repaired stale GitHub repro links and jamming-physics.org URLs.
- Highwire citation meta was added to the hub.
- Earlier site-assembly snapshot commits ("Final", "11111", "1111111", June 2026) carried no claim changes. They included the shared-core dependency map and a fix to owner self-inheritance.

## Claim status (claims ledger)
Counts: interpretation 1 · independent-prediction 2 · anchor-restatement 1 · identity 2.
- One switch, two channels: unwritable γ ruler (SET) + writable A4 coordinate — interpretation — no numeric test (former [F]).
- Held-out FV5: γ ordering predicts CRISPRi knockdown resistance — independent-prediction — **null**: wrong sign and non-significant (ρ = −0.0760, p = 0.6283, K562; RPE1 ρ = +0.2141; GC-partialled ρ = 0.1259, p = 0.43).
- FV8: γ separates GOF vs LOF genes — independent-prediction — passes at p = 0.027 (point-biserial 0.4852), but the effect is weak and not VP-specific (textbook oncogene/suppressor split).
- Gene-therapy lever map, where an edit shifts γ past γ* = 1.4598 — anchor-restatement — edit sizes are entered values; direction only.
- Environment-to-germline transmission series (TG5) and imprint escapees surviving both erasures — identity — holds by construction at fixed D; the escapee claim conflicts with observed PGC erasure.
- Paternal/maternal asymmetry 13/13 and the "18/18 green" scoreboard — identity — in-model checks.

## Open items
- All magnitudes are withheld [O]: dose, titre, interval and schedule. Only the corrective direction is given.
- Author decisions from the review:
  - replace the entered γ edit sizes with physically sourced shifts, or retire the lever magnitudes;
  - add gene addition (AAV) to the lever map;
  - reconcile or retract §6 (escapees) against observed PGC erasure.
- The γ-vs-GC separation cannot be decided by FV5 (ρ(γ, GC) ≈ 0.99). A test on the sequence-specific channels is pending; see dna GC1.
- The listed missing observations are to be integrated.

## Reproduction
The ZIP contains `docs/inheritance/` (the published HTML pages), `repro/inheritance/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- All checks: from `repro/inheritance/`, run `python3 repro/run_all.py`.
- Individual engines (run from `repro/inheritance/`):
  - `engine/two_channel.py`
  - `engine/rna_layer.py`
  - `engine/a4_layer.py`
  - `engine/env_to_germline.py`
  - `engine/germline_escapee.py`
  - `engine/coordinate_heritability.py`
  - `engine/lever_map.py`
  - `engine/gene_therapy.py`
  - `engine/feasibility_validation.py` (the held-out FV tests)
- SEED = 19 where a seed is used. No network access is needed. The held-out data sets are cached in `repro/inheritance/bvalidation/*.cache.json`, and γ is read from `repro/inheritance/inherited/`. The `data/fetch_*.py` scripts, which re-fetch those inputs, are the only steps that need network access.

## Citation and links
- Site: https://jamming-physics.org/inheritance/
- Concept DOI: 10.5281/zenodo.20783547
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
