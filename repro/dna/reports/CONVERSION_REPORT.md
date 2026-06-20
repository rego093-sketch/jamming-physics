# VP_SPEC v1.6 Conversion — 4D DNA Blueprint (paper_id: `dna`) — v13 content

## Result: GATE PASS — Phase 1+2, 108 checks, 0 fail
Code-driven build (per SPEC §1.1; the model did not transcribe HTML). Source = the v13 five-register English track, ported with **no meaning/number change**.

## Output (drop-in at repo root)
| path | role |
|---|---|
| `docs/dna/index.html` | hub — overview + five-register map + TOC + branch link |
| `docs/dna/{01..08}/index.html` | 8 chapters (one register/section → one slug) |
| `docs/dna/_meta.json` | summary card (§9): ≤80-word abstract, headline_results, chapters |
| `docs/assets/css/site.css` | stylesheet (~4 KB, ≤50 KB) |
| `manifest/dna.csv` | deterministic slug table (§3.5) |
| `reports/phase2-dna-full.gate.json` | gate result |
| `repro/dna/_verify/` + per-slug READMEs | self-contained regression (offline PASS) |

## SPEC conformance
- **§6 template**: title pattern `{topic ≤45} — 4D DNA Blueprint §N | Jamming Physics`; description 80–160; single h1; abstract-first with unicode math; claim-strip (grade badge **only where the source grades**; `LOCK → Derive → Gate`; GitHub repro + DOI links); prev/next; JSON-LD `ScholarlyArticle` + `BreadcrumbList`; common footer (DOI/ORCID/CC BY 4.0).
- **§3 slugs**: deterministic, `{NN}-` prefix, stopwords removed, recorded in manifest.
- **§7 math**: **all inline unicode** — γ, γ², γ^1.5, `corr(γ,GC)=0.998`, spinodal ∝ γ^1.5, barrier γ²/4, ṡ = −(s³ − γs − h). **Zero display equations → no `/eq/` SVGs, no `render_eq.js` dependency.**
- **§9 `_meta.json`**: present; chapters carry grade + word counts.
- **§10 cross-links**: each register links to the others; the branch line links to the jamming program; all internal links gate-verified (0 broken).
- **§8 gate PASS**: section count, h1=1, abstract text-math, title/description length, no `class="katex"`, link integrity, HTML ≤300 KB, DOM ≤3000, hub orphans 0, cross-branch ref.

## ⚠ AUTHOR-LOCK FLAGS — registry conflicts (reported, **not** changed; §1 "표준서와 충돌하는 제안은 보고만")
The §2 registry row for `dna` is LOCKed to the **v11/v12 two-layer** paper; **v13 supersedes it**. I used the LOCKed values in metadata and flag three items for author resolution:
1. **Title** — registry: *"A Deterministic Two-Layer Interpretation of DNA"*. v13 is five-register. Used as-is in `_meta.json` / JSON-LD `isPartOf.name`. → recommend updating the registry **title** (the short name **"4D DNA Blueprint"** is unaffected and stays).
2. **Headline** — registry representative result: `form ← γ (Layer 1); quantity ← φ (Layer 2)` (two-layer). The pages/`_meta.json` `headline_results` use the v13 content reads: `corr(γ,GC)=0.998` · cross-species `CV 0.1–2%` · `SET: OTX 1 vs 3+`. → recommend updating the registry **headline** column.
3. **DOI / source** — DOI `10.5281/zenodo.20471407` and the single-source `.tex`/PDF predate the five-register refinement. → recommend a **new Zenodo version** for v13 so the citation/snapshot matches.

These are LOCK items (registry, `src/.tex`, DOI are author-owned). The conversion is otherwise content-accurate to v13.

## repro/ note (lane)
Per SPEC lane rules (§1.6), populating `repro/` is technically separate from a Phase-2 paper session. It is included here so the package is a **complete drop-in** and the claim-strip links resolve. Reproduce scope is honest per slug: the **γ census and the ZRS γ reproduce exactly** via `repro/dna/_verify` (`python3 run_regression.py` → REGRESSION PASS, 28 cases, seed=7); **OTX-family decimals and the ENVIRONMENT cases are principle-demonstration / literature** (flagged in their READMEs).

## Merge (§5)
1. unzip at the repo root — paths are repo-relative (`docs/`, `manifest/`, `reports/`, `repro/`).
2. confirm `reports/phase2-dna-full.gate.json` is PASS.
3. resolve the three author-LOCK flags above (registry title/headline + new DOI version).
4. commit → GitHub Pages serves `docs/dna/`.

## Out of scope here (site-wide phases — need all 6 papers, not the single DNA paper)
- `concepts/` glossary (Phase 4) · top `index.html` + `sitemap.xml` (Phase 5) · Scholar `citation_*` tags + Zenodo back-links (Phase 7).
