# CHANGELOG — v1.12 · single-file → multi-page canonical split

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.11. This increment restores the **canonical multi-page layout** mandated by VP-SPEC v1.8 §4
(retrieval-readiness): the authored single-file deviation of v1.9–v1.11 is split, by code, into a hub plus
one standalone page per section. No body prose, number, or grade is changed — the split is mechanical and
reversible.

## Why
v1.9–v1.11 shipped `docs/dna/index.html` as one monolithic file — an authored deviation noted in those
changelogs. VP-SPEC v1.8 §4 / C4 require the canonical retrieval layout used by every other paper in the
repository (`docs/physics/…`): an answer-first hub and self-contained per-section pages, each independently
crawlable and quotable. v1.12 brings the DNA paper back onto that canonical layout without touching the
author body.

## The split is done by code, not by hand
- **`build_multipage_dna.py`** (new) is the exact inverse of `build_single_file_dna.py`. It parses the
  monolith's 17 `<section data-slug=…>` blocks and emits, deterministically:
  - `docs/dna/index.html` — the **hub**: paper `<h1>`, answer-first paragraph, lede, abstract, claim-strip,
    a short overview, the full table of contents (links rewritten to `/dna/{slug}/`), a cross-links block,
    and JSON-LD (`ScholarlyArticle` + `CreativeWorkSeries` whose `hasPart` lists all 17 section URLs +
    `BreadcrumbList`). The jamming-branch cross-link to `/physics/` is preserved.
  - `docs/dna/{slug}/index.html` — **17 section pages**, one per slug in reading order. Each promotes the
    section's `<h2 id>` to a page `<h1>`, carries `crumb → h1 → p.answer → p.abstract → claim-strip →
    vp-cards → body → prev/next nav`, and a per-page JSON-LD (`ScholarlyArticle` + `BreadcrumbList`).
  - `docs/robots.txt`, `docs/sitemap.xml`, `docs/llms.txt` — the retrieval triplet (previously **absent**),
    now generated: 7 named crawlers + default-allow; 18 URLs (hub + 17) with `lastmod 2026-06-17`;
    `llms.txt` 2,324 B (< 5 KB budget).
- **Reading order preserved.** Document order = `prev/next` order: §0 → §I → §II → §1 … §13 → Appendix A.
  Slugs are taken verbatim from `_meta.json` (`chapters[] + appendices[]`), so the page tree is a
  byte-faithful re-expansion of the manifest.

## Answer-first repair (§1–§7)
The monolith's §1–§7 had no `p.answer` block (only §0, §I, §II, §8–§13, Appendix A did). The split would
have failed VP-SPEC's answer-first requirement on those seven pages. The builder now inserts, where absent,
`<p class="answer">{one_liner}</p>` sourced from the curated `_meta.json` `one_liner` for that section. This
is additive, deterministic metadata (word-count-excluded under VP-SPEC body rules) — not new prose.

## Cross-reference rewrite
The monolith body carried mixed, inconsistent cross-refs (`#s{n}-{slug}` anchors, leftover `/dna/{slug}/`,
and `/dna/#s{n}-{slug}`). All are normalized to canonical `/dna/{slug}/` page links. The rewrite replaces the
`/dna/#s…` form first, then bare `#s…` longest-first, so no `/dna//dna/` corruption can occur. No
non-section `#anchor` references exist in the body.

## What is **not** changed (fidelity)
- **Author body byte-faithful.** Per-section paragraph text is preserved verbatim — a full word-diff of all
  17 sections against the source monolith reports **0 missing words**. Only the editable surfaces VP-SPEC
  permits are added (answer blocks, breadcrumb/nav chrome, per-page metadata, internal links).
- **`docs/assets/css/site.css` is byte-identical** to v1.11 (2,653 B, unchanged). The split pages render
  exactly as the monolith did; no new styling is introduced — consistent with the `vp_physics` reference,
  which also leaves `.answer`/`.vp-card` to browser defaults. Presentation is not silently enhanced.
- **Numbers, grades, DOI, repro pointers unchanged.** Reproduction stays deterministic and read-only.

## Verification (`gate_multipage.py`, new)
A companion gate verifies the split. Result: **PASS 200 · WARN 0 · FAIL 0 · VERDICT PASS**. Checks include:
17 pages = manifest rows; exactly one `<h1>` per page; answer-first on every page; `title ≤ 90` &
`subject ≤ 45` (VP-SPEC 6-D); valid JSON-LD; correct `canonical`; **no leftover `#s…` anchors**; every
internal link resolves; per-page `size ≤ 300 KB` (largest 11,913 B) & `DOM ≤ 3000`; `prev/next` present;
hub orphan count 0; hub `/physics/` branch link present; robots names 7 bots; sitemap URL count = page count;
`llms.txt < 5 KB`; **C2** (no `.tex`/`.eq_list`/body `.txt` introduced); and completeness (vp-card counts
match, answer paragraphs verbatim, paragraph text preserved). Structured result:
`reports/dna-v1_12-multipage.gate.json` (with build + gate script SHA-256).

## Files
- **new** `build_multipage_dna.py` — deterministic splitter (inverse of `build_single_file_dna.py`).
- **new** `gate_multipage.py` — multi-page verification gate.
- **new** `docs/dna/{slug}/index.html` ×17 — section pages.
- **new** `docs/robots.txt`, `docs/sitemap.xml`, `docs/llms.txt` — retrieval triplet.
- **new** `reports/dna-v1_12-multipage.gate.json` — gate report.
- **rewritten** `docs/dna/index.html` — monolith replaced by the canonical hub.
- **updated** `docs/dna/_meta.json` — `version → 1.12`; `layout` field rewritten to describe the multi-page
  restoration and to reference this changelog.
- **unchanged** `docs/assets/css/site.css`, `manifest/dna.csv` body figures, `repro/`, prior changelogs.
