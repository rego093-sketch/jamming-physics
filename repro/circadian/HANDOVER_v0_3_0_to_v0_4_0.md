# HANDOVER — circadian_vp_site  v0.3.0 → v0.4.0

A fresh session can resume from this file alone. Read order: **START_HERE → CHARTER → MASTER_MANUAL → this.**
State passes by files only; nothing here depends on chat history.

## Where v0.3.0 left the package
- **PHASE = writing.** Research signed off and **unchanged** — engine `vp_clk_engine.py`, 8 discriminants
  (RC1–RC6 + TX1) all PASS, aggregate result sha256
  `417823934d6e3c0ad3ced5890a6da2da4da7ce7da57a693ded769b7f5dce612c` (seed=19, 2× identical),
  `vp_substrate.py` byte-identical. `tools/build_docs.py` re-emits `docs/` idempotently.
- **DOI assigned and wired.** Concept **10.5281/zenodo.20755413** (resolves to latest); v0.2.0 snapshot =
  version DOI 10.5281/zenodo.20755414 (Zenodo, CC BY 4.0). Wired across the site (JSON-LD identifier/sameAs,
  claim-strip "DOI snapshot", Highwire citation tags, footers, llms). Recorded in
  `registry/cross_volume_doi.{csv,md}`.
- **VP-SPEC v1.8 C4 retrieval-readiness complete.** 6-R.4 JSON-LD on every page (ScholarlyArticle + identifier +
  datePublished + isBasedOn + per-chapter knowsAbout; hub = CreativeWorkSeries + hasPart + BreadcrumbList);
  Google Scholar Highwire tags on the hub; per-page SEO (keywords/author/robots/OG/Twitter); `docs/circadian/
  _meta.json` (VP-SPEC §9 card); sitemap = 10 URLs.
- **New §0 grounding chapter** — `docs/circadian/00-grounding-measured-dna-emergence/`: the answer-first "this is
  a measured-DNA-seeded deterministic derivation, not a toy" page (measured γ provenance, reproducibility hash,
  8 falsifiable discriminants, [V]/[L]/[O] triad). 10 pages total (hub + §0 + §1–§8).
- Four-document SSOT + VERSION 0.3.0 + CHARTER/START_HERE/README DOI bump + 9-row manifest + irreproducibility
  ledger all current.

## How to verify in 60 seconds
```
cat VERSION                      # 0.3.0
cat PHASE                        # writing
python repro/run_all.py          # battery 8/8, gates all_green, determinism True (sha 417823934d6e…)
python tools/build_docs.py       # re-emits docs/ identically (idempotent); 10 pages
grep -c '10.5281/zenodo.20755413' docs/circadian/index.html   # DOI present in hub
```

## What v0.4.0 should pick up (in priority order)
1. **Author Zenodo enrichment (not blocking the site).** The Zenodo record currently has a minimal title
   ("circadian_vp_site_v0_2_0"); enrich its metadata (human title/description/keywords to match the canonical
   title), and add `related identifiers: isDescribedBy → https://jamming-physics.org/circadian/` (VP-SPEC §12.B,
   the site↔Zenodo back-link). When a fresh release zip is deposited, refresh the version DOI in
   `registry/cross_volume_doi.{csv,md}` and the build constant `VERSION_DOI`.
2. **PDF citation layer (VP-SPEC §12.C) — generator now ships.** `tools/build_paper.py` produces the citation
   PDF from the canonical HTML on demand (`python tools/build_paper.py` → `../paper/circadian_vp_site.tex`,
   then `xelatex` twice; numbers pulled live from the engine; page-1 living-version/DOI line + filled PDF
   metadata + absolute URLs). Per headed C2 the `.tex`/`.pdf` stay OUT of the reproducibility zip — deposit
   them as separate files on the Zenodo record. After deposit, set the hub `citation_pdf_url` to the Zenodo
   PDF direct link.
3. **Sibling setpoint seams OUT.** This package is SSOT for circadian phase/timing and currently *demonstrates*
   gating only on the HPA (cortisol) axis. The thermometabolic / hemodynamic / ionic packages should import the
   gating signal for core-temperature and blood-pressure rhythm; add their cross-refs here as cited parameters
   (do **not** re-emit organs owned elsewhere).
4. **Sleep architecture seam to neuro.** RC4/RC5 touch sleep–wake; the neuro package owns spindle/CPG/sleep
   physiology. Wire a cited seam (process-S/process-C two-process framing) rather than re-deriving it.
5. **Seasonality / photoperiod (RC7).** Day-length encoding (SCN compression/decompression of the active phase)
   as a *measured anchor* extension of the entrainment chapter — keep absolute phase [O].
6. **disease_wp cross-references.** Familial advanced/delayed sleep-phase (PER2/CK1δ), non-24h in blindness —
   monogenic, owned by disease_wp; enter here only as cited parameters if invoked.

## Hard constraints (do not regress)
- `vp_substrate.py` stays byte-identical; coupling/entrainment/gating are the new dynamics on top.
- No tuning: every constant is a measured input or a derived value; SEED=19; 2× sha256 identical before release.
- Every site number stays **pulled live from the engine** via `build_docs.py` (no hand-typed values), and the
  generator stays idempotent.
- Firewall: this package models the TIMING perturbation of setpoints and exports a SIGN to mind; it does not
  model depression/autism itself. Felt quality stays in mind (consciousness_claim=0). efficacy=0 on all
  treatments; not medical advice. Rare/monogenic forms → disease_wp.
- Every new [O] must enter `IRREPRODUCIBILITY_LEDGER.md` with a stated obstacle, or the gate FAILs.
- Four-document SSOT (CHANGELOG/MASTER_MANUAL/COMPLETION_LEDGER/HANDOVER) regenerated at the next increment;
  English deliverables, Korean session communication, direct execution without confirmation pauses.

## Pointers
- Measured input: BMAL1/ARNTL γ=1.33348 (gene 406, NC_000011.10, promoter sha256 7293be92…) —
  `inherited/organ_gamma.json` + `inherited/clock_promoters.cache.json`.
- Mind seam params: `inherited/mind_seam.json` (cited; firewall metadata inside).
- Engine entry: `repro/_engine/vp_clk_engine.py::research_findings()` returns every chapter number.
- Site generator: `tools/build_docs.py` (constants block at top: SITE, PAPER_SLUG, CONCEPT_DOI, VERSION_DOI,
  MIND_DOI, GENE_*, SEED, BASE_KW, KW). DOI/SEO/citation/JSON-LD all live there.
- DOI registry: `registry/cross_volume_doi.{csv,md}`. Summary card: `docs/circadian/_meta.json`.
