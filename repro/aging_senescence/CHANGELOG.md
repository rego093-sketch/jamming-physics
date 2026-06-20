# CHANGELOG — Aging & Senescence (aging_senescence_vp_site)

All notable changes to this package. Versioning is semver + phase tag. The reproducible result hash
(SEED=19, 2×sha256 identical) is recorded at each science-affecting change.

## v1.4.0-writing — 2026-06-19
Closing synthesis + citation layer. This release adds the paper's **conclusion** and a complete **LaTeX/PDF**
edition. No engine or number changed — the result hash is byte-identical to v1.3.0
(`62d5e1eb93db8963…`); v1.4.0 is a content-and-citation release.

### New closing chapter (canonical content)
- **§14 "Conclusion: the genome fixes the ruler, not the lifespan"**
  (`docs/14-conclusion-genome-fixes-the-ruler-not-the-lifespan/`), the final chapter, drawn from the
  package's own measured results (no new measurement):
  - The genome fixes the **ruler** — the aging-master promoter γ, the node inventory, and the reservoir law
    dwell ≈ γ^1.5 — and that layer is measured from sequence **[V]**.
  - It does **not** fix the realized lifespan: senescent-cell accumulation rate, telomere attrition rate,
    and absolute calendar age are runtime.
  - It separates two kinds of open item — **uncomputed** (the absolute calendar rates, §7/§8, closable by an
    external clock) from **underdetermined** (the off-γ-axis location of the lifespan lever, which is
    measured and not closable by more computation). The cross-species null is audited robust (§9), so the γ
    flatness is a result, not a failure to detect.
  - Synthesizes §9 (human aging genes not special; TP53 CV 3.5% across a 4–211 yr span; longevity switch =
    copy number, off-axis), §10 (archaic ≈ modern on the γ axis; observation only), and §11 (telomere γ =
    1.3298, a universal constant; keystone is reservoir **dynamics**, not γ).
  - States the epistemic posture: observation under the constitution; an **[O]** is a correctly labelled
    truth, not a failure; an open conclusion is the strongest position when the object is underdetermined.
- Site regenerated to **14 chapters** (hub, nav chain §13 → §14, _meta, sitemap, llms, manifest); all gates
  green; determinism unchanged.

### New deliverables — complete TeX + PDF (no omissions)
- **`aging_senescence_vp_whitepaper_v1_4_0.tex`** and **`aging_senescence_vp_whitepaper_v1_4_0.pdf`**
  (17 pages): one whitepaper rendered from the canonical multi-page HTML, all **14 chapters** in order, with
  every answer, abstract, vp-card, list, and table preserved. XeLaTeX + DejaVu fonts (full Greek/maths
  coverage), justified, A4.
- **`build_tex.py`**: the deterministic HTML→LaTeX generator (walks `docs/` in chapter order; reports any
  unhandled tag — currently none). The PDF cannot drift from the canonical HTML because every figure already
  lives in that HTML.

### DOI
- The DOI is the published Zenodo **concept** DOI `10.5281/zenodo.20756155`, rendered as a resolving link
  throughout (HTML and the PDF/TeX front matter). A new Zenodo *version* is being minted under this concept
  DOI; the concept DOI itself is unchanged and never fabricated.


Scientific addition: a telomere deep-dive and an archaic↔present-day aging-promoter comparison, both run
under a strict OBSERVATION-ONLY constitution. The motivation was the §9 finding that, of the four aging
masters, TERT (telomere maintenance) is the single residual lifespan lead — the telomere may be the key,
so the package now (a) locates exactly where the telomere lever sits, and (b) measures the four masters
across a cross-sectional set of dated genomes (present-day, three Neanderthal, one Denisovan, two ancient
modern human). The engine grows two reproducible modules and the site grows two chapters; the result hash
changes (new science) and is re-pinned. The published Zenodo concept DOI is wired throughout.

### Constitution (OBSERVATION ONLY)
- The archaic comparison reports **measured present-states** of a cross-sectional set: per-individual γ,
  the γ spread per gene, and which promoter positions differ. The package makes **no claim about how any
  state arose or about any process relating the individuals**; shared genotype states are reported as
  observed co-occurrences. This is enforced in the module docstrings, the chapter prose, the data-file
  charter, and the grading (the meaning of the co-occurrences is [O]).

### New engine modules (reproducible, deterministic)
- **`repro/_engine/archaic_discriminant.py`** (RA8). Re-derives γ bit-for-bit from a committed cache of
  reconstructed promoters (offline reproduce loop: 25/25 sequences match the atlas). Reports, per gene:
  the γ value in each of seven dated individuals, the γ spread (every per-gene range < 0.0016, widest
  FOXO3 0.001536), the homozygous-derived substitution counts (archaic load TP53 8 / CDKN2A 6 / FOXO3 6 /
  **TERT 13** — TERT carries the most), and the **invariance of the two recurrent TERT cancer-promoter
  regulatory positions** across the whole set. Measured states [V]; interpretation of WHY [O].
- **`repro/_engine/telomere_keystone.py`** (RA9). Measures the canonical telomere repeat (TTAGGG)n at
  **γ = 1.3298** — identical on both strands (the SantaLucia table is strand-symmetric), the **lowest γ of
  any aging-related sequence** in the package, and length-independent to <0.5% (a near-exact universal
  constant). Synthesizes RA7 (TERT cross-species lead) + RA8 (TERT archaic substitution lead) + the
  reservoir law (capacity ~ γ^1.5): the telomere is the keystone of aging **dynamics, not γ** — the lever
  acts off the promoter-γ axis through reservoir length and attrition rate. γ-invariance [V]; reservoir
  law [F]; the dynamical-keystone synthesis [O]; telomere length/attrition rates [L, cited].
- **`repro/_engine/fetch_gamma_archaic.py`** — documented online provenance path (Ensembl GRCh37 reference
  + Max Planck EVA high-coverage VCFs, GRCh37-aligned, reconstructed as reference + homozygous-derived
  FILTER-pass substitutions). The committed cache is the canonical offline source.

### Data (vendored, offline-reproducible)
- **`inherited/archaic_promoters.cache.json`** (sha256 `bb22cbf5b95cd05c…`): 25 reconstructed promoter
  windows (7 individuals × 4 genes, Chagyrskaya TERT-only) with per-window substitution lists; the package
  re-derives γ from it without network.
- **`inherited/aging_gamma_archaic.json`**: the 25-row γ atlas with method, charter, reconstruction rule,
  assembly note, and per-individual provenance [L] (Prüfer 2014/2017; Meyer 2012; Fu 2014; Lazaridis 2014;
  Mafessoni 2020).

### Site (new chapters; renumbered tail)
- **§10 "Archaic and present-day aging promoters"** (RA8) and **§11 "The telomere keystone: dynamics, not
  γ"** (RA9) inserted after the cross-species chapter. The previous **pathology** and **reproducibility**
  chapters are renumbered **§12** and **§13**; all internal cross-references updated; stale chapter folders
  removed. The hub, llms.txt, sitemap, manifest, and `_meta.json` regenerate to 13 chapters.

### DOI
- Wired the published **Zenodo concept DOI `10.5281/zenodo.20756155`** throughout (render_site, JSON-LD,
  claim-strip, footer, llms.txt, `_meta.json`, and the PDF front matter), rendered as a resolving link.
  The prior `TBD` placeholder is retired.

### Determinism / hashes
- Engine result hash **changes** (new science): from `d6506074f9f9ae61…` to
  **`62d5e1eb93db89630c4cd288951540e36ee1c0d8d243945d8b4337188e528c81`** (SEED=19, 2×sha256 identical).
- `reports/research_complete.json` regenerated; all gates green (determinism, emergence, stress battery).
- The §9 headline (human-not-special; longevity switch is off the γ axis) is unchanged and reinforced:
  RA9 makes the off-axis location of the telomere lever explicit and measured.


Rigor addition: an unbiased confound audit of the §9 cross-species result, prompted by the question of
whether the original per-gene-only design (or author/analysis bias) had under-tested the headline. The
emergence engine is untouched — the result hash is byte-identical (`d6506074f9f9ae61…`) — but §9 prose,
the IRREPRODUCIBILITY_LEDGER, and the PDF are regenerated from the audit's numbers.

### Audit (new reproducible verification layer)
- **`repro/_verify/xspecies_robustness_audit.py`** (SSOT, deterministic SEED=19; two runs byte-identical;
  artifact sha256 `c771cf7ee871f99d0a8d8ad0e994bc46c9679644187153d8265b5bf4c170531e`). Re-derives γ
  bit-for-bit from the cached promoters and corrects the four confounds the per-gene tests ignored:
  (1) **GC confound** — γ↔GC = 0.96–1.00, so γ is a GC proxy; GC↔lifespan is the same null, so the null is
  not a transform artifact; (2) **body-mass** — the combined lean drops to p=0.16 on the intrinsic-longevity
  residual; (3) **phylogeny** — Felsenstein 1985 independent contrasts on a dated tree collapse the combined
  lean to corr +0.17 (p=0.55): the short-lived rodents are one clade, so the raw lean was pseudoreplication;
  (4) **multivariate** — the 4-gene γ vector classifies long/short at 80% LOOCV but label-perm p=0.115 (not
  above chance). Plus leave-one-out (raw p≈0.05 is unstable: drop dog→0.021, drop human→0.044), switch-
  threshold robustness (a clean gap is manufacturable only by excluding mid-lifespan species), and a TERT
  focus.
- **Report:** `reports/XSPECIES_ROBUSTNESS_AUDIT.md` — full methods, tables, regrade, references.

### What changed in §9 (`tools/render_site.py` → regenerated `docs/`)
- **Corrected over-strong wording:** "no trend" → "a weak shared lean that is fully confound-attributable."
  All four masters lean the same way (every per-gene ρ>0) and the combined raw ρ=+0.64 (p=0.054), but it
  vanishes under body-mass correction and collapses under phylogenetic contrasts.
- **New subsection** "Robustness audit: the shared lean is confound, not signal" with the corrected results.
- **TERT re-graded** from "modulator" to the **suggestive exception [O]**: most lifespan-leaning, the only
  master whose lean survives body-mass correction (ρ=+0.54) and with the largest PIC contrast (+0.58), but
  never significant (p≈0.12). Tied to off-axis telomerase-suppression biology (Gomes 2011).
- **Scope sharpened:** "no longevity gene" = "no signature on the promoter-γ (=GC) axis," *not* "no longevity
  genetics" — real levers are off-axis (TP53 copy number; telomerase regulation).
- **Grade line:** human-not-special + TP53 flatness + confound-attributable-lean **[V]**; residual TERT
  **[O]**; off-γ-axis levers **[L]**.

### Determinism / hashes
- Engine result hash **unchanged**: `d6506074f9f9ae61375b5c127b637aa6df4dc49eea821801749011a3fa66aae9`.
- Audit artifact: `c771cf7ee871f99d0a8d8ad0e994bc46c9679644187153d8265b5bf4c170531e` (byte-identical 2 runs).
- PDF rebuilt from updated §9: `0299fc5f173d656118a3ebc31a1f01ccfd3514d9786abdeadf25d10b602fe88e`
  (162.4 KB, deterministic across two runs). The prior `a12afb7c…` PDF hash is superseded.
- The headline conclusion is unchanged and **strengthened**: the null is now robust to GC, body-mass,
  phylogenetic, and multivariate confounds — not merely untested against them.

## v1.1.0-writing — 2026-06-19
Publication-phase addition: the citation-layer PDF. Science is unchanged — the engine result hash is
byte-identical to v1.0.0 (`d6506074f9f9ae61…`) and the canonical `docs/` site is untouched.

### Writing (citation layer)
- **PDF generated from the canonical HTML** (`tools/build_pdf.py` → `pdf/aging_senescence_vp_site.pdf`).
  The generator parses the per-section HTML in `docs/` and lays out one whitepaper: title page →
  contents → the 11 chapters, in the same order with the same prose and the same numbers. Because every
  displayed figure already lives in the engine-generated canonical HTML (C1), the PDF cannot drift from
  the reproducible result; no value is entered by hand. Web-only furniture (breadcrumb/page nav, JSON-LD,
  the claim-strip GitHub/DOI link) is dropped; the scholarly content (answer-first, abstract, body,
  tables, vp-cards, honest grades) is kept.
- **Front matter on page 1 (C4 citation requirement):** full title, author + ORCID, version, branch,
  `DOI: TBD` (rendered as a non-resolving placeholder — never fabricated), the hub URL
  `https://jamming-physics.org/aging/`, the reproduction-code URL, CC BY 4.0, the SEED=19 result hash,
  the abstract, and the four headline results.
- **Typesetting:** A4, DejaVu Serif body / DejaVu Sans headings / DejaVu Mono hashes — full Greek (γ) and
  math-symbol (γ², γ^1.5, ΔG37, ≈, −, en-dash) coverage, so no glyph renders as a box. Running header
  (volume + hub) and footer (author · CC BY 4.0 · DOI TBD · SEED=19 · page) on every content page.
- **Determinism:** reportlab is built in invariant mode (`rl_config.invariant = 1`), so two builds are
  byte-identical. Artifact: `pdf/aging_senescence_vp_site.pdf`, 15 pages,
  sha256 `a12afb7cf8cfb506eafbb791d9f6342462e30da44ce427e8cd35e4ab98fa1427` (stable across two runs).
- **Lock preserved:** `build_pdf.py` refuses while `gates.writing_locked()` is True and requires the
  canonical site to be built first, exactly like `build_docs.py`.

### Cross-check (PDF mirrors canonical, no drift)
- Engine result hash unchanged: `d6506074f9f9ae61…`. Canonical `docs/` hash unchanged.
- Spot-checked tokens present in the PDF text and matching the canonical numbers: the SEED=19 result
  hash, human TP53 γ 1.4298, elephant per-copy γ 1.4269, risk multiplier 52.3×, arrested fraction 0.391,
  TP53 CV 3.5%, shared-rate fraction 0.889, permutation p 0.114, anchors Abegglen 2015 / Sulak 2016.

### Grades
- No new graded claims and no new `[O]` items: the PDF reproduces the canonical content one-to-one. The
  IRREPRODUCIBILITY_LEDGER is unchanged and still cross-checks against the canonical HTML.

## v1.0.0-writing — 2026-06-19
First complete edition: research signed off (all gates green) and the canonical HTML site built.

### Research (engine + verification)
- **Masters vendored.** TP53, CDKN2A, FOXO3, TERT promoter γ measured from NCBI RefSeq and written to
  `inherited/organ_gamma.json` (γ = −mean SantaLucia 1998 NN ΔG37 over TSS−2000..+500; never fitted).
  `_to_measure` is now empty. Values: TP53 1.429832, CDKN2A 1.442444, FOXO3 1.594156, TERT 1.553876.
- **RA1–RA6 implemented** as real deterministic R19 simulations in `repro/_engine/aging_dynamics.py`:
  RA1 setpoint drift (creep + catastrophic flip, jump 0.790), RA2 senescence stuck-attractor
  (irreversible; arrested fraction 0.391), RA3 reservoir depletion (capacity ~ γ^1.5; all wells empty),
  RA4 hallmarks map (10 hallmarks, 0 orphans), RA5 risk multiplier (convex; 52.3× over 40→80),
  RA6 rate of aging (shared-rate fraction 0.889).
- **RA7 cross-species discriminant added** (`repro/_engine/xspecies_discriminant.py`): the headline
  result. Human aging-gene γ is NOT special (|z|<1 on every gene), no discontinuous γ longevity switch,
  TP53 nearly flat across 4–211 yr (CV 3.5%); the longevity switch is off the γ axis (TP53 copy number,
  [L]). Reproduces offline from the promoter cache (37/37, 0 mismatches).
- **Cross-species data vendored**: `inherited/aging_gamma_xspecies.json` (44 gene×species rows + analysis),
  `inherited/aging_promoters.cache.json` (offline bit-for-bit cache). Online fetcher added at
  `repro/_engine/fetch_gamma_xspecies.py` (network guarded; cache is canonical).
- **Stress battery rewritten** (`repro/_verify/stress_tests.py`): RA1–RA7 call the real functions and
  compute PASS/FAIL from measured booleans. `all_targets_pass = True`.
- **Pathology derived** (`repro/_pathology/setpoint_failure.py`): one law g_eff = γ(1−d) shrinks barrier
  (drift) and spinodal (catastrophe). Sarcopenia (monotone drift), frailty (accelerating co-failure,
  critical drops 0.28–0.58), aging-as-cancer (convex hazard, 135× over 30→90). All shapes reproduce.
- **Determinism**: engine emits a byte-identical result on two runs — `d6506074f9f9ae61…`.
- **Gates green**: `research_gate().all_green = True`; `reports/research_complete.json` written;
  `PHASE = writing`.

### Writing (canonical site)
- Built 11-chapter canonical site under `docs/` via `tools/render_site.py` (numbers pulled from the
  engine, so HTML cannot drift from the reproducible result — C1). `tools/build_docs.py` now delegates
  to it (lock preserved).
- Each page: answer-first `<p class="answer">` (40–60 words), abstract, claim-strip, self-contained
  `vp-card`s for every cited locked quantity, JSON-LD ScholarlyArticle + BreadcrumbList, English body.
- Hub `docs/index.html` (CreativeWorkSeries), `_meta.json`, `manifest/aging_senescence_vp_site.csv`,
  `docs/sitemap.xml`, `docs/robots.txt` (7 AI/search bots), `docs/llms.txt` (<5 KB),
  `docs/assets/css/site.css` (8 KB).
- DOI rendered as a non-resolving `TBD` placeholder everywhere; assigned on publication.

### Grades
- [V]: every mechanism (RA1–RA6) and the cross-species null (human-not-special, TP53 flatness).
- [L]: the copy-number longevity switch (Abegglen 2015 JAMA; Sulak 2016 eLife); cited decline anchors.
- [O]: γ–lifespan trend (small panel, GC confound, phylogeny); all absolute rates/incidence/lifespans.
  All [O] items carry a stated obstacle in `IRREPRODUCIBILITY_LEDGER.md`.

## v0.1.0-research — (inherited skeleton)
- Self-contained research skeleton: CHARTER (RA1–RA6 program), vendored substrate (`vp_substrate.py`:
  R19/FHN, barrier, spinodal, dwell), node identities as honest to-measure inputs, research/writing gate,
  stub pathology + build_docs, VP-SPEC v1.8. Writing locked until research green.
