# CHANGELOG — DNA paper v1.9 → v1.9 + Appendix A (gene-clock application merge)

Author-directed **application merge** under VP-SPEC v1.8. The applied package
`universal_morphogenesis_geneclock v12 (heart)` is folded into the DNA paper as **Appendix A
(응용편/부록)**. Nothing in chapters §1–§13 is changed; the merge is **add-only** at the paper level,
exactly the allowed additions in VP-SPEC §1 (abstract/answer, claim-strip, vp-card, internal links,
metadata) plus a new appendix section and its verification lane. The constitution (§0) governs:
**C1** reproducibility, **C2** HTML-canonical / no bundled TeX, **C3** every `[O]` names its obstacle,
**C4** retrieval-readiness — all preserved and re-checked.

DOI of record stays **10.5281/zenodo.20471407** (concept DOI). This is a new living-version snapshot.

---

## 1. What was merged, and where

The appendix is folded in following the **single-file-canonical pattern this paper already uses**
(chapters are `<section id="s{no}-…">` anchors in one `docs/dna/index.html`, per CHANGELOG_v1_9 §3),
not the multi-page §3/§6 layout. The appendix is therefore a new `<section>`, not a new page — no
fragmentation (§0).

| layer | change |
|---|---|
| **Canonical HTML** `docs/dna/index.html` | one new `<section data-section="A" data-slug="ax-a-universal-morphogenesis-gene-clock">` after §13; a TOC entry (`Appendix A`); and the paper-level JSON-LD `ScholarlyArticle.hasPart` extended from 13 → 14. answer-first `<p class="answer">`, abstract, two claim-strips, and three self-contained `vp-card`s (R19 switch, γ, the timing-null result). 73.7 KB → 82.7 KB, 717 → 766 DOM nodes (within VP-SPEC §8 ≤300 KB / ≤3000). |
| **Verification layer** `repro/dna/ax-a-universal-morphogenesis-gene-clock/` | the **entire** geneclock package (`code/`, `data/`, `results/`, `repro/morpho/expected/`, `verify_all.py`, `expected_sha256.json`, all LEDGERs/CHANGELOGs/HANDOFFs/README/REPRODUCE/PROJECT_SUMMARY/WHY_THE_NULL). Placed inside the **dna lane** so the merge stays within one paper's paths (§1 lane rule). The package imports the paper's switch as a single sha256-pinned source and is self-contained for reproduction. |
| **Derived index** `manifest/dna.csv`, `docs/dna/_meta.json` | one appendix row in the manifest; an additive `appendices[]` block + a `merged` marker in `_meta.json`. The 13 chapter rows are **byte-untouched**. |
| **C3 register** `IRREPRODUCIBILITY_LEDGER.md` (new at root) | aggregates the paper's standing `[O]` themes and the appendix's `[O]` items (timing null + model boundaries), each naming its measured-input obstacle, and points to the per-section ledgers. |
| **Reports** `reports/dna-appendixA-geneclock-merge.gate.json` | this session's gate record (below). |

---

## 2. Why this is a faithful application of the paper (not a bolt-on)

- **One switch.** The appendix's `spinodal(γ)=2(γ/3)^1.5` is asserted bit-identical to the body engine
  and the neural-emergence engine at run time (`max|Δ| = 2.2e-16 < 1e-12`). The same R19 primitive that
  reads DNA in §1–§13 schedules morphogenesis here.
- **Same measured γ.** Every per-gene γ is `mean(−NN ΔG37)` (SantaLucia 1998) from NCBI promoters by the
  identical pipeline, corr(γ,GC)=0.994–0.998, read-only and never fitted.
- **It tests the paper's own thesis in the time axis.** The paper's central claim is that γ is the
  *threshold scale*, not the *locus of difference*. The appendix asks whether γ predicts developmental
  *timing* and answers with an honest, sharpened **null** (heart: ρ=+0.071, exact p=0.882; the cardiac
  master NKX2-5 is ranked near-last by γ), graded `[O]` with the apparatus proven non-blind (synthetic
  γ→ρ=1.000). γ fixes *what / what order* `[V]`, not *when* `[O]`.

---

## 3. Constitutional gate (re-checked at merge)

- **C1 reproducibility** — appendix `verify_all.py` PASS **14/14** (12 gates 5/5 + sha256 source pin over
  **69 files, drift 0** + 12 fidelity baselines, leaf drift 0). Re-verified **from the new appendix path**:
  pin drift 0; core determinism gates (gene_clock, heart_substages, dev_timing) re-run PASS 5/5 with 2×
  sha256 identical. Reproduction path unbroken by relocation.
- **C2 HTML-canonical / no TeX** — `find` for `*.tex`, `*.eq_list.*`, `render_eq.js` across the **whole
  merged tree** returns empty. The appendix's canonical text is the HTML section; the verification layer
  is code + measured data, no TeX.
- **C3 `[O]` obstacles** — every appendix `[O]` (timing null; absolute size; facial-bone aging; no
  morphometric validation; single H²; Layer-2/3 geometry; pleiotropic specifier choice) names its
  measured-input obstacle and is aggregated in `IRREPRODUCIBILITY_LEDGER.md`, cross-referenced to the
  appendix's own ledgers.
- **C4 retrieval-readiness** — appendix section is answer-first; each locked quantity it cites (switch, γ)
  carries a self-contained `vp-card` with value + meaning + grade + canonical link; JSON-LD
  `ScholarlyArticle.hasPart` updated and valid; static HTML; all 14 TOC anchors resolve.

What is **not** changed: any wording, number, equation, or table in §1–§13; any byte of the appendix's
locked engines and measured γ/stage tables (imported, sha256-pinned, reproduced).

---

## 4. Author-directed deviations (recorded, not silent)

Consistent with CHANGELOG_v1_9 §3. This is an **application merge / new version**, not a conversion
session, so the §1 "본문 무변경 (conversion-only edits)" rule is honored at the chapter level (§1–§13
untouched) while the paper gains an appendix — which §0 (no fragmentation; return the original material
with additions folded in) and the author's instruction direct.

| VP-SPEC clause | this merge | why it still honors the principle |
|---|---|---|
| §3/§6 multi-page, section-per-folder | appendix is one anchored `<section>`, package under `repro/dna/ax-a-…/` | follows the paper's existing single-file-canonical pattern; C4 hooks (answer-first, vp-card, JSON-LD) hold at section level; §8 size/DOM limits met |
| §3 appendix slug `ax-{letter}-` | `ax-a-universal-morphogenesis-gene-clock`, anchor `#sA-…` | appendix slug convention applied within the single-file anchor scheme |
| §1 lane (one paper's paths only) | all additions under `docs/dna/`, `repro/dna/`, `manifest/dna.csv`, `reports/` | the merge never leaves the dna lane |

Package: `dna_vp_site_INTEGRATED_v1_9_appendixA_geneclock.zip` (repo-relative paths).
