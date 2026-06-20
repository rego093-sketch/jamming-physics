# CHANGELOG — v2.0 multi-page canonical conversion

Converted the analgesic_threshold_logic whitepaper from a single-file canonical
(`docs/index.html`) to a **multi-page canonical HTML edition**, mirroring
`vp_physics_v0_11_0_html_canonical_merge_material` under VP-SPEC v1.8.

## Why
Per the author's instruction: split the HTML by subheading AND per analgesic target
while keeping each page self-contained (C4 retrieval-readiness), delivered as one archive.
The vp_physics structure is the binding reference: hub + one `/{slug}/index.html` per
section, shared `/assets/css/site.css`, `robots.txt`, `sitemap.xml`, `llms.txt`, `_meta.json`.

## What changed (presentation only — no number, grade, or claim changed)
- `docs/` is now the multi-page tree:
  - `docs/analgesic/index.html` — hub (CollectionPage + CreativeWorkSeries hasPart + ToC + cross-links)
  - `docs/analgesic/{slug}/index.html` — 40 self-contained §6 pages:
    1 how-to-read · 5 lever pages (L1/L2/L3/master/context) · **27 per-target pages** ·
    prioritisation · precision-local-anaesthesia · proposals · falsification ·
    grading-and-honesty · for-pharma-and-researchers · for-patients-and-public
  - `docs/assets/css/site.css` — canonical VP-SPEC stylesheet (+ analgesic grade badges)
  - `docs/robots.txt` (7 named bots + default allow), `docs/sitemap.xml` (41 URLs), `docs/llms.txt`
  - `docs/analgesic/_meta.json` — summary card (§9), layout declared, 27 target reads listed
- Every page: answer-first `<p class="answer">`, JSON-LD ScholarlyArticle + BreadcrumbList,
  claim-strip, prev/next nav, footer. Each target page is individually deep-linkable.
- Generator `build_multipage_analgesic.py` emits the whole tree deterministically from the
  canonical engine JSON (γ/|h_sp| byte-faithful → drift 0).

## Discipline preserved (VP-SPEC v1.8 C1–C4)
- Firewall intact on every page: γ reads promoter switch-threshold structure only; every
  clinical magnitude is `[O]`.
- M5 forbidden-claim scanner updated to scan the relocated `data-claim` sections across
  `docs/**/index.html` (still fail-closed; self-tests live). PASS on the multi-page site.
- `run_all.py` 11/11 PASS, drift 0 (re-frozen), offline. No DOI fabricated (pending, Zenodo).
- 9 `[O]` open classes unchanged in `IRREPRODUCIBILITY_LEDGER.md`; 0 ungraded items.
