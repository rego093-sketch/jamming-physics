# CHANGELOG — Chronobiology (circadian_vp_site)

All notable changes to this package. Versions follow the VP four-document SSOT discipline
(CHANGELOG / MASTER_MANUAL / COMPLETION_LEDGER / HANDOVER produced at each increment).
Engine determinism: seed = 19, result sha256 reproduces bit-for-bit (2× identical).

## v0.3.0 — 2026-06-19 — DOI assigned + VP-SPEC v1.8 retrieval-readiness completed + grounding chapter
**Phase:** writing (unchanged). The research body and engine are **untouched** — result sha256
`417823934d6e3c0ad3ced5890a6da2da4da7ce7da57a693ded769b7f5dce612c` is byte-identical to v0.2.0
(2× identical, seed=19); `vp_substrate.py` byte-identical. This increment is the **writing-phase finalisation**
the v0.2.0 handover scheduled: assign and wire the DOI, complete C4 retrieval-readiness, and foreground the
measured-DNA grounding. All site numbers remain pulled live from the engine, so nothing can drift.

### Added — measured-DNA grounding chapter (the "this is not a toy" page)
- `docs/circadian/00-grounding-measured-dna-emergence/` — a new front chapter (§0) that states, answer-first and
  self-contained, that this volume is a **deterministic derivation seeded by a measured clock-gene γ**, not a
  casual simulation. It foregrounds: the measured BMAL1/ARNTL well **γ = 1.33348** (Gene ID 406, NC_000011.10,
  computed as −mean(NN stacking ΔG37, SantaLucia 1998) over 2500 promoter dinucleotides via the shared DNA
  pipeline; 2501-bp promoter cached, sha256 `7293be92e4ad…`, offline-reproducible; **never fitted**); the single
  deterministic engine (seed=19, result sha256 `417823934d6e…`, 2× identical); the **8 falsifiable
  discriminants** (RC1–RC6 + TX1) with live numbers and grades; and the honesty triad (derived [V] / cited [L] /
  open [O] with stated obstacle). Every number is pulled live from the engine.

### Added — DOI assignment + wiring (CHARTER/handover writing-phase task)
- **Concept DOI 10.5281/zenodo.20755413** (resolves to latest) assigned to the volume; v0.2.0 snapshot =
  **version DOI 10.5281/zenodo.20755414** (Zenodo, CC BY 4.0, published 2026-06-19).
- Wired across the canonical site by `tools/build_docs.py`: JSON-LD `identifier` + `isPartOf.sameAs`
  (https://doi.org/…) on every page; claim-strip **"DOI snapshot"** link (replacing `DOI: pending`); page
  footers; the hub note/footer; `llms.txt`/`llms-full.txt`.
- `registry/cross_volume_doi.{csv,md}` created — the circadian self-entry (concept + version DOI) and the cited
  **mind** affect-seam entry (SIGN-only firewall recorded).

### Added — VP-SPEC v1.8 C4 retrieval-readiness completion
- **JSON-LD upgraded to the 6-R.4 chapter schema:** `ScholarlyArticle` now carries `identifier`,
  `datePublished`/`dateModified`, `isBasedOn` (the repro tree), and a per-chapter `knowsAbout` keyword array;
  `isPartOf` is a `CreativeWorkSeries` with `sameAs` DOI. The **hub** JSON-LD is now `CreativeWorkSeries` with a
  full `hasPart` chapter list, `identifier`/`sameAs` DOI, `datePublished`, `inLanguage`, and author `sameAs`.
- **Google Scholar (§12 Phase 7):** Highwire `citation_*` tags added to the hub head (citation_title, _author,
  _publication_date, _doi, _fulltext_html_url, _abstract_html_url, _language).
- **SEO:** per-page `meta keywords` (volume base + per-chapter terms), `meta author`, `robots`
  (index,follow,max-snippet,max-image-preview), `link rel=license`, Open Graph + Twitter-card tags on every
  page and the hub.
- `docs/circadian/_meta.json` (VP-SPEC §9 summary card) created — title, DOI, measured-input block,
  headline results, 9 chapters with one-liners/grades/words, totals.
- `sitemap.xml` now enumerates the §0 page (10 URLs); `manifest/circadian_vp_site.csv` gains the §0 row.

### Added — citation layer (Zenodo PDF/TeX, VP-SPEC §12.C, headed C2)
- `tools/build_paper.py` — on-demand citation-PDF generator: extracts the **canonical HTML verbatim** into a
  LaTeX article (the extract.py role) and pulls the reproducibility numbers LIVE from the engine, so the PDF
  cannot drift from the site. Output (a 9-page, text-based PDF) carries the §12.C page-1 line
  ("Living version: <hub URL> · DOI 10.5281/zenodo.20755413"), full PDF metadata (title/author/subject/
  keywords), absolute URLs, an abstract, and a front "Reproducibility & grounding" box (measured γ provenance
  + seed=19 + engine sha + 8 falsifiable discriminants). Per **headed C2**, the generated `.tex`/`.pdf` are the
  citation layer and are **NOT** bundled into this reproducibility zip — they are deposited alongside it on
  Zenodo. `build_paper.py` itself ships so the frozen snapshot can regenerate the PDF.

### Changed
- `VERSION` 0.2.0 → **0.3.0**. `CHARTER.md`, `START_HERE.md`, `docs/README.md`, `MASTER_MANUAL.md`,
  `COMPLETION_LEDGER.md` — version bump + DOI status (TBD → assigned) + §0 grounding chapter reflected.
- `tools/build_docs.py` — DOI/SEO/citation/JSON-LD wiring; `copy_css()` made idempotent for standalone re-emit
  (skips when the vendored stylesheet is already in place). The generator remains the agent of conversion;
  no body number is hand-typed.
- Handover rotated: `HANDOVER_v0_2_0_to_v0_3_0.md` consumed → `HANDOVER_v0_3_0_to_v0_4_0.md`.

### Discipline (unchanged, re-verified)
- `vp_substrate.py` byte-identical; engine result sha256 `417823934d6e…` 2× identical (seed=19).
- `tools/build_docs.py` re-emits `docs/` **idempotently** (byte-identical across rebuilds).
- No tuning: every constant is a measured input or a derived value. Firewall held: TIMING perturbation + SIGN to
  mind only; the felt quality stays in mind (consciousness_claim=0); efficacy=0; not medical advice;
  rare/monogenic forms → disease_wp. Every [O] carries a stated obstacle.

## v0.2.0 — 2026-06-19 — research signed off + full canonical write
**Phase:** research → **writing** (gate opened: stress battery 8/8 green, research_complete.json all_green, PHASE=writing).

### Added — research body (engine)
- `repro/_engine/vp_clk_engine.py` (513 lines) — the circadian oscillator engine on the vendored FHN/R19
  substrate (`vp_substrate.py` byte-identical). Eight discriminants, all PASS:
  - **RC1** free-running limit cycle (76 regular cycles, cv=0.003691) + depolarisation-block control (1 beat).
  - **RC2a/RC2b** biphasic light PRC (advance 0.185022 / delay −0.129012 cyc) + Arnold tongue (locking range
    widens 5→15 with zeitgeber strength).
  - **RC3** coupled-network synchronisation transition (coherence 0.596→0.99993) + master-led entrainment
    (peripheral drift vs master falls 0.003823→0.002956).
  - **RC4** HPA setpoint gating (gated cortisol amp 0.976237 vs ablated 0.0) — mind-cited kinetics, no new constant.
  - **RC5** misalignment (signed demand-projection 1.227923→−1.364039 across the phase gap; PRC-bounded
    re-entrainment 0→12 cycles).
  - **RC6** circadian–mood seam (HPA flattening index 0→2.11085) — supplies mind's locked circadian contributor.
  - **TX1** chronotherapy (correct phase corrects 2.56→0 h; wrong phase worsens 5.44→11.2 h; efficacy=0).
  - Deterministic aggregate result sha256 `417823934d6e3c0ad3ced5890a6da2da4da7ce7da57a693ded769b7f5dce612c`.
- `inherited/clock_promoters.cache.json`, `inherited/organ_gamma.json` — **measured** BMAL1 well
  γ=1.33348 (ARNTL, Gene ID 406, NC_000011.10, seq sha256 7293be92…) fetched via the DNA NN pipeline
  (SantaLucia 1998, NCBI eutils); grade [V], never fitted.
- `inherited/mind_seam.json` — cited seam params (HPA cascade window [15,40] min; valence geometry; the
  depression locked-contributor note; coordination anchor R=0.38961455156044245; coupling-vs-bias map).
  Firewall: SIGN only, efficacy=0, magnitude [O], consciousness_claim=0.
- `repro/_verify/stress_tests.py` — SUITE_SPEC wires all 8 suites (RC1–RC6 + TX1) to the live discriminants,
  each with a wide-sweep description, grade and (for [O]) a stated obstacle. `run_battery()` → 8/8 PASS.
- `repro/_pathology/setpoint_failure.py` — 5 failures wired to live discriminants (circadian sleep-wake
  disorders; shift-work metabolic/CV; IARC-2A night-shift cancer; circadian-misalignment depression [mind seam];
  circadian disruption in autism [mind cross-ref]) + `management()` chronotherapy section (4 levers, wrong-phase
  warning, efficacy=0). Rare/monogenic forms cross-referenced to disease_wp.

### Added — canonical site (writing phase)
- `tools/build_docs.py` — per-title canonical SEO HTML generator (VP-SPEC v1.8 §6); refuses while writing is
  locked; pulls every number LIVE from the engine so prose cannot drift from the shipped result.
- `docs/circadian/` — hub + 8 chapters (§1 scope, §2 free-running, §3 entrainment/PRC, §4 master-vs-network,
  §5 setpoint gating, §6 misalignment/disease, §7 circadian–mood seam, §8 chronotherapy). Each page:
  answer-first block, JSON-LD ScholarlyArticle + BreadcrumbList, claim-strip (grade + LOCK→Derive→Gate +
  reproduce link + DOI), vp-cards, prev/next nav, CC-BY footer.
- `docs/assets/css/site.css` — vendored verbatim (2723 bytes) from the mind package stylesheet.
- `docs/{robots.txt, sitemap.xml, llms.txt, llms-full.txt}` — 8-crawler robots, full sitemap (lastmod
  2026-06-19), and llms summaries with the cross-volume seam note.

### Changed
- `VERSION` 0.1.0-research → **0.2.0**.
- `CHARTER.md` — version bump; research program annotated as executed (RC1–RC6 + TX1 all green); disease
  section extended with the two seam-derived conditions and the chronotherapy management block.
- `manifest/circadian_vp_site.csv` — populated with 8 chapter rows (slug, title, section, status, grade,
  words, displayed numbers).
- `IRREPRODUCIBILITY_LEDGER.md` — BMAL1 γ row marked RESOLVED; added the open quantities with stated
  obstacles (absolute phase; inter-tissue lags; absolute incidence/RR; depression-handle magnitude;
  per-pulse chronotherapy gain).

### Discipline
- `vp_substrate.py` byte-identical (coupling, entrainment and gating are NEW dynamics added on top — the
  package's job). Every constant is a measured input or a derived value; none chosen to hit a target.
- Firewall held throughout: this package models the TIMING perturbation of the HPA setpoint and exports a
  SIGN to mind; it does not model depression/autism itself; the felt quality stays in mind
  (consciousness_claim=0); efficacy=0 on all treatments; not medical advice.

## v0.1.0-research — (skeleton, as received)
- CHARTER, START_HERE, VP-SPEC v1.8, FHN/R19 substrate vendored, node identities (1 to-measure γ), the
  research-first gate (writing locked until the stress battery is green), and stubs for the engine,
  stress battery, pathology and `build_docs.py`.
