# MIGRATION REPORT — fluid-dynamics → VP-SPEC v1.8

**Package:** `fluid-dynamics_vp-spec_complete_merged` · **paper_id:** `fluid-dynamics` (`flu`)
**Title:** *The Configured Continuum* · **concept DOI:** 10.5281/zenodo.17972568 · **branch:** jamming
**Upgraded:** 2026-06-15 · **Target standard:** VP-SPEC **v1.8**
**Starting state:** v1.6/v1.7 conventions (toolchain gen "v0.8"); Phase 1/2/3 gates already passing.

This volume was brought from v1.6/v1.7 to the **v1.8** standard. The body — every sentence, number,
and equation of the nine-paper science — was **not changed** (Ch.1: code is the agent of conversion;
no body meaning or numbers altered). All work is additive (abstract-adjacent metadata, retrieval
hooks, registries, gate phases) or constitutional removal (TeX/lane hygiene). The five gates —
Phase 1, Phase 2, Phase 3, **search**, **constitution** — all **PASS**.

---

## 1. Constitution C2 — single canonical = HTML, TeX not bundled

Removed from the distribution (handoff zip must contain no `.tex`, no `*.eq_list.*`, no `txt/` body):

| removed | why |
|---------|-----|
| `src/fluid-dynamics/foundational_whitepaper.tex` | C2: TeX source is not bundled in the canonical package |
| `tools/split.py`, `tools/render_eq.js` | TeX→HTML toolchain belongs upstream of the canonical artifact, not in the handoff |
| `repro/.../rotcore/audit-source/manuscript/…_v1.3.6.tex` (+ empty `manuscript/` dir) | literal `find -name '*.tex'` must be 0 |
| `vp_chemistry_whitepaper_v1_0.zip` (nested sibling, at v1.6 with `txt/`+TeX) | **lane violation** — a different paper's package inside this one fails the gate |

**Kept (correctly):** 908 rendered equation **SVGs** (canonical equation form); `img alt`/`title`
LaTeX (accessibility metadata, explicitly *not* a removable source per spec §0/§6/§7);
`foundational_whitepaper.pdf` (citation-layer snapshot — the C2 gate forbids TeX-family, not PDF).
**Provenance preserved:** a v1.8 pointer note was appended to the rotcore
`audit-source/PROVENANCE.md` — reproduction provenance (scripts + `METRICS_SPEC` + CSVs) is intact;
the removed manuscript remains retrievable from the upstream source package (rotcore-doi-v1_3_9).

Post-state: `*.tex` = **0**, `*.eq_list.*` = **0**, `txt/` body dirs = **0**, canonical SVGs = **908**.

## 2. Constitution C4 — retrieval-readiness (new in v1.8)

Generated deterministically by `tools/derive_search.py` (idempotent; edits only the head JSON-LD and
the answer/vp-card hooks — all outside the gate's body-word-count region):

- **Answer-first** `<p class="answer">` on **all 38** pages — each **condensed from that page's
  sealed `.abstract`** into **whole sentences** (not invented; abstract numbers are a verified subset
  of the body), targeting 40–60 words, with the page grade badge, inserted right after `</h1>`. The
  derivation takes complete sentences only — it never truncates mid-clause, strips orphan
  code/LaTeX-source artifacts, drops dangling fragments where a sealed abstract was itself cut off,
  and de-duplicates any borrowed body sentence — so every answer is grammatical, self-contained prose
  with all rendered symbols preserved verbatim. The gate's `words_of()` was updated to **exclude**
  this paragraph from the body word count (an `<aside>` vp-card was already excluded), so the ±0.5%
  C1 word parity is preserved — confirmed by Phase 1/2 still passing.
- **`aside.vp-card`** for the one signature cross-cited locked quantity **`c² = B/ρ`** (`cs2`) —
  **5 cards** on the pages that cite it (§01, §06, §13, §14, ax-b); the derivation-home page (§03)
  is correctly **excluded**. Registry-driven via `registry/locked_quantities.fluid-dynamics.json`.
- **JSON-LD enrichment** — each chapter `ScholarlyArticle` gained `isPartOf` a `CreativeWorkSeries`
  with `identifier` (DOI), `dateModified` (2026-06-15), `isBasedOn` (repro URL), and `knowsAbout`;
  the hub gained `CollectionPage` → `CreativeWorkSeries` + `hasPart` + `BreadcrumbList`.
- **Machine access layer** (`docs/`): `robots.txt` (allows the 7 named bots — Googlebot, Bingbot,
  OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended — + sitemap ref);
  `sitemap.xml` (**39 URLs** == 39 `index.html`: 1 hub + 38 chapters); `llms.txt` (2,155 B < 5 KB);
  `llms-full.txt` (full extract, via `tools/extract.py`).

## 3. Constitution C3 — irreproducibility ledger (new artifact)

`IRREPRODUCIBILITY_LEDGER.md` created. Finding: this volume has **zero `[O]` items** — every
displayed quantity (ratios, dimensionless invariants, exponents, shapes) regenerates from
`repro/fluid-dynamics/{slug}/`. The ledger records this empty set with positive attestation and,
critically, **disambiguates** the two open **`[GATE]` theorems** (global regularity; the infinite-Re
Onsager/Duchon–Robert flux mechanism) as **unproven propositions, not irreproducible measurements** —
so they are correctly excluded from the `[O]` ledger. Cross-referenced to §14 and §3. The
constitution gate confirms `O_pages == []` consistently with the ledger.

## 4. v1.7 cross-reference layer

`registry/cross_volume_doi.csv` (10 cols × 9 rows) and `registry/cross_volume_doi.md` created
**verbatim from spec Ch.2** (no web re-research). Carries each sibling volume's code, full/short
title, concept DOI, latest-version resolution, headline result, branch, and site slug; marks
fluid-dynamics as the current volume. `registry/locked_quantities.fluid-dynamics.json` added as the
vp-card injector source.

## 5. Gate toolchain — additive v1.8 update

`tools/gate.py` extended (originals preserved: `tools/originals/gate.py.orig` pre-anti-fabrication,
`tools/originals/gate.py.v17.orig` pre-v1.8):

- `words_of()` now strips `<p class="answer">` before counting (spec mandates the answer paragraph be
  excluded from body words; otherwise the addition would break ±0.5% parity).
- **`phase_search()`** (C4): answer-first present + first-after-`h1` + self-contained; vp-card for
  each cited locked quantity; JSON-LD parses with ORCID + DOI; hub has `CreativeWorkSeries` +
  `BreadcrumbList`; `robots.txt` lists the 7 bots; `sitemap` count == page count; `llms.txt` < 5 KB.
  Soft warnings only for answer word-range and long paragraphs.
- **`phase_constitution()`** (C1/C2/C3): no `tex`/`eq_list`/`txt`; per-section word parity ±0.5% with
  `data-eq == eq_display` and `Σ data-eq == display-SVG count` and `_meta` totals; ledger exists and
  every `[O]` page appears in it.

Both new phases wired into the CLI dispatch (`search`, `constitution`). Existing phase1/phase2/phase356
logic untouched. This mirrors how the prior migration ratified the anti-fabrication fix.

## 6. Other

`docs/fluid-dynamics/_meta.json` gained two **non-numeric** top-level provenance fields
(`spec_version: "VP-SPEC v1.8"`, `spec_upgraded: "2026-06-15"`); the chapter word/equation arrays are
## 7. Final wording pass

The shipped answer-first copy was read end to end and the derivation hardened so that no extraction
artifact reaches the page. Four defect classes were removed **at the tool level** (not by
hand-editing pages, which preserves determinism): mid-sentence ellipsis truncation from the old
60-word hard cap; a leading orphan `)}` LaTeX delimiter carried inside some sealed abstracts;
raw-LaTeX **source** echoes (e.g. `\nabla^2\psi`) pulled from the body when an abstract was short;
and dangling tails on the two pages (ax-s, ax-w) whose sealed abstracts were themselves cut off
mid-word. Semantic symbols that genuinely live in the sealed abstract (e.g. `ρuv`, `Thetaσ`) are
reproduced verbatim and were **not** altered — only non-semantic code/markup noise was stripped.
`tools/derive_search.py` carries the fix; all 38 answers were regenerated, the tool re-confirmed
idempotent, and the five gates re-run green.

---

## Gate results (all PASS)

| phase | verdict | key counts |
|-------|---------|------------|
| 1 (structure/words) | **PASS** | per-section word parity holds after answer-paragraph addition |
| 2 (equations/links) | **PASS** | — |
| 3 (hub/nav)         | **PASS** | — |
| **search** (C4)     | **PASS** | 38 answers · 5 vp-cards · 39 sitemap URLs · 7 bots · llms 2,155 B · 0 violations (23 soft warnings: 22 long-para + 1 answer-length) |
| **constitution** (C1/C2/C3) | **PASS** | tex/eq_list/txt = 0 · `Σ data-eq 40 == display-SVG 40` · `O_pages == []` · ledger present · 0 violations |

The 23 search warnings are all **soft**, with **0 violations**. 22 are long-paragraph notices on the
dense physics body, which Ch.1 forbids rewriting, so they stand by design. The 1 answer-length notice
is ax-c, whose answer is a single complete sentence just over the 60-word target: trimming it would
require the mid-clause truncation we deliberately avoid, so the whole sentence is kept. Answer lengths
run 32–62 words (median 45; 24 of 38 inside the 40–60 target), every one a complete, grammatical
sentence.

_VP-SPEC v1.8 upgrade complete — 2026-06-15._
