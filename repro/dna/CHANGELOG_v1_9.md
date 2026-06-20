# CHANGELOG — DNA paper v1.8 → v1.9

Author-directed correction + consolidation release. Builds on
`dna_vp_site_INTEGRATED_v1_8_ch01-12` plus the v1.8 §13 append. Nothing scientific
is silently changed: γ, the locked grammar, and every chapter's numbers are
preserved; the one retired claim is **deprecated, not deleted**.

DOI of record stays **10.5281/zenodo.20471407** (concept DOI). v1.9 is a new
living-version snapshot; the published Zenodo deposit is unchanged by this repo
edit and would be re-archived on the author's next release.

---

## 1. Scientific corrections (the substance)

### 1.1 Helical claim — DEPRECATED / RETIRED (irreversible), not deleted
- **What changed.** The §10 prose claim that a *global* ~10.4 bp helical period
  sits "at the 100th percentile against a composition-matched shuffle" is now
  marked **superseded** in place (a visible `aside.superseded` note), and a
  **retired-register tombstone** is added to §8.
- **Why.** An absolute, global periodicity read from an arbitrary window edge is a
  composition surrogate for nucleosome spacing — not a statement about whether a
  specific element can contact a specific partner.
- **Superseded by.** The **anchor-relative** phase `contact_competent` (§13):
  whether a motor and its nearest anchor sit on the same rotational helical face.
- **Kept, not erased.** The original sentence remains, flagged; the global
  statistic survives only as a *descriptive composition fact*, never as a
  coordinate/contact claim.
- **Code.** `repro/dna/11-…/cross_kingdom_engine.py::helical()` carries a
  **DEPRECATED (v1.9)** banner (comment + docstring only). Its computed values are
  **unchanged** (verified: human/fly/arabidopsis reproduce the frozen
  `expected/cross_kingdom_results.json` bit-for-bit), so §11's reproduction is
  intact. The function is retained solely to reproduce §11's frozen results.

### 1.2 Coordinate grammar — RESTORED (additive)
- §13 adds the A4 coordinate read (shell · anchor · loop · anchor-relative helix)
  that §11/§12 lacked, using real motors from re-acquired NCBI feature tables
  (`repro/dna/13-…/inputs_annot/`, frozen with provenance + sha256).

### 1.3 Methylation — KEPT and PROMOTED
- Raw `cpg_density` (conflates with GC) is demoted to a secondary aux note; CpG
  **O/E** is the primary environment measure. §13 reproduces the §12 layer
  bit-for-bit (52 quantities + 4-regime auto-detector).

### 1.4 γ — IMMUTABLE (untouched)
- `human_SOX2` γ = **1.287315**, re-checked by a §13 gate every run.

### 1.5 Helical stress test — `contact_competent` graded at CHANCE (not assumed)
- A §11-style stress test (`repro/dna/13-…/stress_helical/`) asks whether the anchor-relative
  `contact_competent` flag carries element-level signal. **Result: AT CHANCE** — pooled over 246
  TSS↔nearest-anchor pairs across 10 cross-kingdom regions, the same-face rate is 0.337 vs the
  analytic chance 0.340 (permutation z = −0.09). Real TSS positions are not helically phased to the
  composition-shell anchors.
- **Honest three-way grading (no gray zone):** (1) the *global* WW ~10.5 bp periodicity is a REAL
  descriptive nucleosome-propensity signal (elevated above shuffle in all 12); (2) the anchor-relative
  `contact_competent` flag is deterministic Layer-1 **geometry but at chance biologically**, so it is
  reported as geometry, not a functional-contact claim; (3) realized functional contact is **Layer-2**.
  The stress test *vindicates* the two-layer thesis. The §13 paper section and `LEDGER_unified.md`
  carry this grading; the stress test is frozen (seed 19, feature tables with provenance + sha256).
- **On "100%":** achievable for the *geometry* (every locus gets a phasing read), not for the
  *realized functional contact* (Layer-2). The helical axis that could be promoted to a richer
  coordinate is the local nucleosome propensity, not the chance-level contact flag.

---

## 2. Structure — single-file canonical paper

- **The whole DNA paper is now one file: `docs/dna/index.html`** (70.8 KB, one
  `<h1>`, 13 `<section>`s, ~710 DOM nodes — within the VP-SPEC §8 limits of
  ≤300 KB / ≤3000 nodes).
- The 13 per-section pages `docs/dna/{slug}/index.html` are **removed** (the paper
  is no longer fragmented). Each chapter is a `<section id="s{no}-{slug}">` reached
  by anchor.
- **URL migration:** `/dna/{slug}/` → `/dna/#s{no}-{slug}`. On deployment the
  author adds the 301 map (per VP-SPEC §3); in this repo deliverable the anchors
  and this note stand in for it.
- The **verification layer is unchanged**: `repro/dna/{slug}/` (01–13) stays
  per-section, and every section's claim-strip still links to its `repro/dna/…/`
  folder (no broken links).
- Consolidation was performed by `build_single_file_dna.py` (deterministic:
  extract each `<main>`, demote headings one level, drop per-page nav, wrap in a
  section, inject only the two v1.9 correction notes). No chapter wording or number
  was otherwise altered.

---

## 3. Conscious deviations from VP-SPEC v1.8 (author-directed)

These are intentional and recorded here so they are not silent violations. The
author directed single-file management while preserving the constitution's
substance; the constitution (§0) overrides the structural chapters (§3/§6).

| VP-SPEC clause | Letter | This release | Why it still honors the principle |
|---|---|---|---|
| §3 / C4 "multi-page, section-per-folder" | per-section pages | one file, sections as anchors | C4's enforced requirements — answer-first, self-contained passages, JSON-LD, static HTML — all hold per section; §8 size/DOM limits met |
| §1 "본문 무변경; only head/answer/abstract/strip/card/links" | conversion-session rule | author correction edits §10/§8 prose + §11 code comment | this is an **author correction / new version**, not a conversion session; §0 C1+C3 *require* honest retired-claim handling |
| §6 chapter template (per page) | per-page head/JSON-LD | one paper-level `ScholarlyArticle` with `hasPart`, plus per-section answer-first + claim-strip + vp-cards | structured data + retrieval hooks preserved at both paper and section level |

What is **not** deviated: C1 reproducibility (all numbers regenerate, 2× sha256
on §13; §11 values unchanged; γ pinned), C2 (HTML canonical, no bundled TeX), C3
(every [O] names a closing dataset; retired register carries the helical tombstone),
C4 substance (answer-first, self-contained, JSON-LD, static HTML).

---

## 4. Gate status (v1.9)

- §13 engine: determinism 2× sha256 identical, 9/9 gates PASS, fidelity PASS, γ = 1.287315.
- §11 helical(): comment-only deprecation; frozen values reproduce (drift 0).
- Single file: 1 `<h1>`, 13 sections, JSON-LD ×2 valid (paper `hasPart` = 13),
  §10 supersede note + §8 tombstone present, all 13 TOC anchors resolve, 0 leftover
  page-nav, ≤300 KB / ≤3000 nodes.
- Locked grammar, γ inputs, and unchanged chapters' science: byte-identical.

Package: `dna_vp_site_INTEGRATED_v1_9_single_file.zip` (repo-relative paths).

---

## 4. v1.9 stress battery + defensive guards (second-session consolidation)

Append-only verification work folded into the dna lane (`repro/dna/…`). **Nothing
scientific is silently changed:** γ, the NN table, the A4 pipeline, the methylation
engine, every threshold, and all frozen `expected/` remain **byte-identical** to the
v1.9 originals. Corrections live in a new **wrapper layer**, never in the locked engines.
All artifacts deterministic (2×sha256); session gate `reports/dna-ch14-defensive-guards.gate.json` PASS.

### 4.1 Stress battery (4 probes, one per layer + engine) — `stress_*/`
- **Material γ** (`02-…/stress_gamma_vs_gc/`): γ≈GC confirmed within-genome; refined with a
  small (~1%) CpG-coupled dinucleotide term; **inverts at GC ≈ 20%** (bound).
- **A4 coordinate** (`13-…/stress_coordinate_stability/`): anchor *positions* robust (93%
  within 2 kb); anchor *count* is `min_shell_bp`-resolution-set (bound).
- **Methylation auto-detector** (`12-…/stress_detector_adversarial/`): generalizes within
  plant/vertebrate regimes and declines out-of-category honestly; **false-positives PLANT
  below ~25% GC** (Plasmodium, Dictyostelium). Surfaced a latent panel error.
- **Engine robustness** (`_verify/stress_abnormal_inputs/`): no engine silently wrong;
  `run_key` raises an opaque IndexError on sub-window input (one gap).

### 4.2 Defensive guards — `14-defensive-guards/` (new chapter, wrapper layer)
- `detect_regime_safe` (GC floor 0.25 → suppress+flag below it), `run_key_safe` (clean `[O]`
  on `len<W`), `bulk_contexts_safe` (case-normalize). Import the locked engines single-source
  + sha256-pinned; **locked engines unchanged.**
- `stress_guards.py`: methylation raw 17/19 → **guarded 19/19**, fixing Plasmodium +
  Dictyostelium with **zero regressions**; run_key/bulk gaps fixed. OVERALL_PASS.
- `stress_guard_validation/`: GC floor **validated out-of-sample** — caught a *third*
  false-positive (Entamoeba 24.5%); guarded 7/7; no real methylator < 31.6% GC.

### 4.3 Correction (author-permitted: fix wrong content)
- The §12 ledger's "auto-detector all test cases correct" is corrected to "correct within
  ~33–45% GC and for out-of-panel plants/mammals; bounded below ~25% GC."
- The shipped panel's Plasmodium call `PLANT_global_CG_CHG_CHH` is corrected to `no_global`
  at the guard layer (raw call retained for audit). Bounds aggregated in §08/§09/§12/§13 ledgers.
- **Declared residual risk:** a GC<25% genome with genuine global 5mC would be down-graded;
  none known (3 extreme-AT non-methylators caught, 6 real methylators all ≥ 31.6% GC).
