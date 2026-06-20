# geodynamics (Atlantic) — VP-SPEC v1.8 site build

One self-contained build of the Atlantic Expansion paper (`geodynamics`), upgraded from the
VP-SPEC v1.6 multi-page-site standard to **VP-SPEC v1.8** (Constitution C4 — Retrieval-Readiness).
Gate: **VERDICT PASS — 901 checks, 0 failed, 61 soft warnings**
(`reports/phase1-2-geodynamics.gate.json`). The conversion stays mechanical and deterministic:
re-running `generate.py` reproduces a byte-identical `docs/` tree, and the per-chapter
`manifest/geodynamics.csv` is byte-identical to the v1.6 manifest — i.e. **the body is unchanged**;
the v1.8 edits touch only `head` / `answer` / `abstract` / `claim-strip` / `vp-card` / internal
links / JSON-LD, exactly as the spec's edit surface allows (§ "본문 무변경").

## What changed v1.6 → v1.8 (Constitution C4 / chapter 6-R)
- **answer-first** (`6-R.3`): every chapter opens with `<p class="answer">` — a self-contained
  40–60-word direct answer (entity + key value/conclusion + gate verdict). Excluded from the body
  word count, so the manifest is invariant. Built deterministically from {subject, abstract, body};
  an anti-confabulation assert guarantees every number in the answer already occurs in the source.
- **self-contained vp-cards** (`6-R.2`): for every *locked quantity this body cites* (μ_eff,
  φ_jam, Ω-NoGo floor, z_iso), the page carries one `aside.vp-card` with value + meaning + grade +
  a link to its single canonical derivation — except on the quantity's own canonical section. The
  generator and the gate share one registry (`common.VP_CARDS`), so the emitted-card set equals the
  body-cited set by construction.
- **richer chapter JSON-LD** (`6-R.4`): `ScholarlyArticle` now declares `isPartOf` a
  `CreativeWorkSeries`, `identifier`/`sameAs` (DOI), `author.sameAs` (ORCID),
  `datePublished`/`dateModified`, `isBasedOn` (repro URL) and `knowsAbout`. Hub schema is now a
  `CreativeWorkSeries` (`hasPart` → all 33 chapters) plus `BreadcrumbList`.
- **access layer** (`6-R.5`): new `docs/robots.txt` (7 AI/search bots: Googlebot, Bingbot,
  OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended), `docs/sitemap.xml`
  (34 locs = hub + 33 chapters = every `index.html`), `docs/llms.txt` (1817 B, < 5 KB) and
  `docs/llms-full.txt` (canonical body as plain-text markdown).
- **Constitution C3**: `IRREPRODUCIBILITY_LEDGER.md` at repo root. This paper has **zero `[O]`
  (irreproducible) items** — every headline number reproduces from the bundle engines
  (`validate_all.py` → 39/39 PASS); the two HOLDs are evidence gates, not reproducibility obstacles.
- **gate upgrade** (`§8`): `gate.py` gained the **search gate** (answer-first present + first +
  40–60 w; vp-card set == body-cited locked set; JSON-LD valid in `<head>` with ORCID/DOI; robots
  7-bot / sitemap / llms.txt access checks; soft long-paragraph warnings) and the **constitution
  gate** (C2 no `.tex`/`.eq_list.*`/`txt/` body; C3 ledger present + every `[O]` chapter covered;
  C1 `_meta.json` ↔ written-chapter and manifest-sum agreement). Checks went **505 → 901**.

## Layout
- `docs/geodynamics/**` — the generated site: a hub (`index.html`) + 33 chapter pages, each with
  the §6 template (subject/desc, answer, abstract, claim-strip, vp-cards, prev/next nav, JSON-LD).
- `docs/robots.txt` · `docs/sitemap.xml` · `docs/llms.txt` · `docs/llms-full.txt` — v1.8 access layer.
- `docs/eq/geodynamics/*.svg` — 73 display equations rendered from LaTeX via MathJax.
- `manifest/geodynamics.csv` — per-chapter word/equation/figure/table counts (== gate; == v1.6).
- `repro/geodynamics/{slug}/` — one folder per chapter; demonstration chapters carry the actual
  NumPy engines (19 wired) from the paper's bundle.
- `src/geodynamics/atl_bundle/` — the paper's reproducibility bundle (single source;
  `validate_all.py` → 39/39 PASS).
- `IRREPRODUCIBILITY_LEDGER.md` — Constitution C3 ledger (zero `[O]` items).
- `build/` — the toolchain. Paper-specific: `common.py` (registry + concept DOI + `VP_CARDS` +
  retrieval-readiness helpers), `sections_data.py` + `eqs.json` (auto-converted), `atl_convert.py`
  (the `.tex`→site converter). `generate.py`, `gate.py`, `make_repro.py`, `render_eq.mjs`.

## Rebuild
```
cd build
npm install mathjax-full
python3 atl_convert.py                 # .tex -> sections_data.py + eqs.json
node render_eq.mjs > eq_dims.txt        # -> docs/eq/geodynamics/*.svg
python3 generate.py                     # -> docs/geodynamics/**, manifest, _meta.json,
                                        #    robots.txt, sitemap.xml, llms.txt, llms-full.txt, LEDGER
python3 make_repro.py                   # -> repro/geodynamics/{slug}/
python3 gate.py                         # -> reports/…gate.json   (VERDICT: PASS, 901 checks)
```

## Key facts locked
- Registry id `geodynamics`, **concept DOI 10.5281/zenodo.17978934** everywhere (the cover's
  `…935` typo is corrected; no version DOI is emitted).
- §10 convergence wiring: the hub and the physical-justification chapter link `/physics/` and
  `/fluid-dynamics/`; the chronology-firewall chapter links `/geochronology/`.
- The resistance-collapse chapter (§14) is the **canonical derivation** for μ_eff ≈ 2.2×10⁻³
  (no melt), φ_jam = 0.840 and z_iso; §16 is canonical for the Ω-NoGo floor (μ_eff ≥ 10⁻²). Every
  other chapter that cites one of these gets a self-contained `vp-card` linking back here.
- The chronology chapter (§20) keeps the firewall posture (U–Pb ages conceded,
  chronology-agnostic); no absolute-age number is claimed, so none is `[O]`.

## Honest scope
This is a **deterministic mechanical conversion** of `atl_whitepaper_r18.tex`; numbers and wording
are preserved (body unchanged from v1.6). Display equations are MathJax-exact; inline math is
best-effort unicode (occasionally compressed spacing). The answer-first blocks, vp-cards and
llms-full.txt are deterministic *re-statements / extracts* of the existing body, not new claims.
A green gate certifies **structural/format conformance, retrieval-readiness (C4) and the
reproducibility-constitution checks (C1–C3) + convergence wiring** — not peer-review of the
science. At merge, reconcile against the canonical Phase-0 kit (shared `tools/`, master
`slugs.csv`, shared CSS) and carry in `config/constraints.yml`, per the handoff BUILD_NOTES.
