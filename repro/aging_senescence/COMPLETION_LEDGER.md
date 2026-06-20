# COMPLETION LEDGER — Aging & Senescence  ·  v1.4.0-writing  ·  2026-06-19

Single source of truth for what is done, the gate status, and the deliverables. C0: one zip, no
fragmentation; the returned archive is the original package plus everything added this session.

## v1.4.0-writing addition — closing conclusion + complete TeX/PDF
A content-and-citation release: no engine or number changed (result hash byte-identical to v1.3.0,
`62d5e1eb93db8963…`).
- New closing chapter (canonical content): **§14 "Conclusion: the genome fixes the ruler, not the lifespan"**
  (`docs/14-conclusion-genome-fixes-the-ruler-not-the-lifespan/`). Synthesises §9 (human aging genes not
  special; longevity switch = copy number, off-axis), §10 (archaic ≈ modern on the γ axis, observation only),
  and §11 (telomere γ = 1.3298, a universal constant; keystone is reservoir dynamics, not γ) into the
  epistemic conclusion: the genome fixes the ruler but not the realized lifespan, which is **underdetermined**
  by the γ axis (the lever lives off-axis in dosage and reservoir dynamics) rather than merely uncomputed.
  Separates uncomputed [O] (absolute calendar rates, need an external clock) from underdetermined [O]
  (off-γ-axis lifespan lever, measured). Grade: synthesis over [V] reads and measured nulls; the chapter badge
  is [O] (its subject is what stays open). Constitution-clean (observation-only; no avoid-list terms).
- Site regenerated to **14 chapters** (hub, nav §13 → §14, _meta, sitemap, llms, manifest); all gates green.
- New deliverables: **`aging_senescence_vp_whitepaper_v1_4_0.tex`** + **`.pdf`** (17 pages, all 14 chapters,
  no omissions; XeLaTeX + DejaVu) and the generator **`build_tex.py`** (HTML→LaTeX, unhandled tags: none).
- DOI: published Zenodo **concept** DOI `10.5281/zenodo.20756155` wired through HTML + PDF; new Zenodo version
  to be minted under it.

## v1.3.0-writing addition — telomere deep-dive + OBSERVATION-ONLY archaic comparison
Prompted by the §9 finding that TERT (telomere maintenance) is the single residual lifespan lead, the
package adds (a) a telomere deep-dive that locates where the telomere lever sits, and (b) a cross-sectional
comparison of the four aging masters across seven dated genomes. New science → the engine result hash
changes to **`62d5e1eb93db89630c4cd288951540e36ee1c0d8d243945d8b4337188e528c81`** (SEED=19, 2×sha256
identical); supersedes `d6506074…`.
- New engine module (SSOT): `repro/_engine/archaic_discriminant.py` (**RA8**, OBSERVATION ONLY). Re-derives
  γ bit-for-bit from `inherited/archaic_promoters.cache.json` (sha256 `bb22cbf5…`; offline reproduce 25/25).
  Reports per-individual γ, γ spread per gene (every range < 0.0016, widest FOXO3 0.001536), substitution
  counts (archaic load TP53 8 / CDKN2A 6 / FOXO3 6 / **TERT 13**), and TERT cancer-hotspot invariance.
- New engine module (SSOT): `repro/_engine/telomere_keystone.py` (**RA9**). Telomere repeat (TTAGGG)n
  γ = 1.3298 — strand-symmetric, lowest γ of any aging sequence, length-independent (universal constant);
  verdict: the telomere is the keystone of aging **dynamics, not γ** (lever off the promoter-γ axis:
  reservoir length + attrition).
- New provenance fetcher: `repro/_engine/fetch_gamma_archaic.py` (Ensembl GRCh37 + Max Planck EVA VCFs,
  GRCh37-aligned). New data: `inherited/archaic_promoters.cache.json`, `inherited/aging_gamma_archaic.json`.
- **Constitution (OBSERVATION ONLY):** the archaic comparison reports measured present-states of the set
  only; no claim about how any state arose or any process relating the individuals. Enforced in the module
  docstrings, the §10/§11 chapter prose, and the data-file charter; the meaning of the co-occurrences is [O].
- **Site:** §10 "Archaic and present-day aging promoters" (RA8) and §11 "The telomere keystone: dynamics,
  not γ" (RA9) inserted after the cross-species chapter; pathology→§12, ledger→§13; all cross-refs fixed;
  stale folders removed; hub/llms/sitemap/manifest/_meta regenerate to 13 chapters.
- **DOI:** the published Zenodo concept DOI `10.5281/zenodo.20756155` is wired throughout (HTML + PDF),
  rendered as a resolving link; the prior `TBD` placeholder is retired.
- **Grades:** RA8 per-individual γ / spread / substitution counts / hotspot invariance **[V]**; RA9
  telomere-repeat γ invariance + lowest-γ ranking **[V]**, reservoir law **[F]**; the dynamical-keystone
  synthesis and the meaning of the archaic co-occurrences **[O]**; telomere length/attrition rates **[L]**.
- §9 (`tools/render_site.py`) and the ledger updated; `docs/` + PDF regenerated; `research_complete.json`
  re-emitted (all gates green).

## v1.2.0-writing addition — unbiased confound audit of the §9 cross-species result
Prompted by the question of whether the original per-gene-only design (or analysis bias) had under-tested
the headline, an independent audit re-derives γ bit-for-bit and corrects the four confounds the per-gene
tests ignored. The emergence engine is untouched (result hash byte-identical `d6506074f9f9ae61…`).
- New module (SSOT): `repro/_verify/xspecies_robustness_audit.py` — GC confound, body-mass correction,
  Felsenstein 1985 phylogenetic independent contrasts, multivariate LOOCV, leave-one-out, switch-threshold,
  TERT focus. Deterministic SEED=19; artifact sha256 `c771cf7ee871f99d0a8d8ad0e994bc46c9679644187153d8265b5bf4c170531e` (byte-identical 2 runs).
- New report: `reports/XSPECIES_ROBUSTNESS_AUDIT.md`.
- **Finding:** the null is **robust** — γ is a GC proxy (0.96–1.00); the weak shared 4-gene lean (raw
  combined p≈0.054) is fully confound-attributable (body-mass p=0.16; PIC p=0.55; multivariate LOOCV
  label-perm p=0.115; raw p≈0.05 unstable to leave-one-out). **Corrections:** "no trend" → "weak
  confound-attributable lean"; TERT re-graded to the suggestive exception **[O]** (survives body-mass
  correction, largest PIC contrast, still p≈0.12). **Scope:** "no γ-axis signature," not "no longevity
  genetics" (off-axis levers: TP53 copy number; telomerase suppression, Gomes 2011).
- §9 (`tools/render_site.py`) updated and `docs/` + PDF regenerated from the audit numbers.
- PDF rebuilt: `0299fc5f173d656118a3ebc31a1f01ccfd3514d9786abdeadf25d10b602fe88e` (162.4 KB, deterministic);
  supersedes the prior `a12afb7c…`. New canonical `docs/` HTML tree sha256 `b5294467bbdced61…`.

## v1.1.0-writing addition — the citation-layer PDF
The publication-phase PDF is built **from the canonical HTML** (no restructuring): `tools/build_pdf.py`
parses `docs/` and emits one whitepaper — title page (DOI=TBD + hub URL on page 1) → contents → the 11
chapters in the same order, with the same prose and the same engine numbers (C1, cannot drift). Web-only
furniture is dropped; answer-first / abstract / tables / vp-cards / honest grades are kept.
- Artifact: `pdf/aging_senescence_vp_site.pdf`, 15 pages, A4, fully embedded DejaVu fonts.
- Determinism: invariant build, byte-identical across two runs —
  sha256 `a12afb7cf8cfb506eafbb791d9f6342462e30da44ce427e8cd35e4ab98fa1427`.
- Science untouched: engine result hash still `d6506074f9f9ae61…`; canonical `docs/` hash unchanged.
- No new graded claims, no new `[O]`; the PDF reproduces the canonical content one-to-one.

## Gate status (all green)
| gate | result |
|---|---|
| determinism (2×sha256 identical) | PASS — `d6506074f9f9ae61375b5c127b637aa6df4dc49eea821801749011a3fa66aae9` |
| emergence_ok (nodes emerge from measured γ) | PASS |
| stress battery RA1–RA7 all_targets_pass | PASS (7/7) |
| research_gate all_green | PASS |
| research signed off (reports/research_complete.json) | PASS |
| PHASE | writing (unlocked) |
| offline cross-species reproduction | PASS (37/37 checked, 0 mismatches) |
| citation PDF determinism (2×sha256 identical) | PASS — `a12afb7cf8cfb506eafbb791d9f6342462e30da44ce427e8cd35e4ab98fa1427` |

## Stress battery (RA1–RA7) — measured outcomes
| target | status | key value | grade |
|---|---|---|---|
| RA1 setpoint drift | PASS | creep-in-basin + catastrophic flip (jump 0.790) | [V] |
| RA2 senescence stuck-attractor | PASS | irreversible; arrested fraction 0.391 | [V] |
| RA3 reservoir depletion | PASS | capacity ~ γ^1.5; all wells empty | [V]/[O] |
| RA4 hallmarks map | PASS | 10 hallmarks, 0 orphans | [V]/[O] |
| RA5 risk multiplier | PASS | convex; 52.3× over ages 40→80 | [V]/[O] |
| RA6 rate of aging | PASS | shared-rate fraction 0.889 | [V]/[O] |
| RA7 cross-species discriminant | PASS | human not special (|z|<1); TP53 CV 3.5%; switch = copy number | [V]/[O]/[L] |

## The scientific question (user's axis) — answered
**Are human aging genes different from animals, or is there a special switch?**
Two-sided, honest answer (docs/09):
1. **Human is NOT special** — every gene within the mammalian distribution (|z|<1; TP53 z=+0.09,
   CDKN2A +0.02, FOXO3 +0.31, TERT +0.64). Null on the human-switch hypothesis.
2. **TP53 nearly flat** across 4→211 yr (CV 3.5%): elephant ≈ human ≈ mouse. [V]
3. **No discontinuous γ longevity switch** — overlap in 3/4 genes; γ–lifespan trend positive but
   non-significant. γ is a weak modulator, not a switch. [O]
4. **The real switch is OFF the γ axis: COPY NUMBER** — elephant ~20 TP53 copies at unchanged per-copy
   γ (1.4269) ⇒ ~20× gate dosage. Conserved identity substrate + divergent dynamics = aging. [L]

## Deliverables built this session
- inherited/organ_gamma.json (masters vendored), inherited/aging_gamma_xspecies.json,
  inherited/aging_promoters.cache.json
- repro/_engine/aging_dynamics.py (RA1–RA6), repro/_engine/xspecies_discriminant.py (RA7),
  repro/_engine/fetch_gamma_xspecies.py (online fetcher), rewired vp_age_engine.py
- (v1.3.0) repro/_engine/archaic_discriminant.py (RA8), repro/_engine/telomere_keystone.py (RA9),
  repro/_engine/fetch_gamma_archaic.py (provenance), inherited/archaic_promoters.cache.json +
  inherited/aging_gamma_archaic.json (vendored, offline-reproducible)
- repro/_verify/stress_tests.py (RA1–RA7), reports/research_complete.json
- repro/_pathology/setpoint_failure.py (derived law)
- docs/: hub + 13 chapter pages + _meta.json + sitemap.xml + robots.txt + llms.txt + assets/css/site.css
- manifest/aging_senescence_vp_site.csv
- tools/render_site.py (generator), tools/build_docs.py (delegates)
- Governance: CHANGELOG.md, MASTER_MANUAL.md, COMPLETION_LEDGER.md, HANDOVER.md;
  IRREPRODUCIBILITY_LEDGER.md updated; VERSION → 1.0.0-writing.
- (v1.1.0) pdf/aging_senescence_vp_site.pdf (citation layer) + tools/build_pdf.py (canonical-HTML→PDF
  generator); governance four-doc SSOT refreshed; VERSION → 1.1.0-writing.

## Site conformance (VP-SPEC v1.8)
- answer-first on every page (40–60 words) · JSON-LD ScholarlyArticle + BreadcrumbList valid ·
  self-contained vp-cards for cited locked quantities · claim-strip with LOCK→Derive→Gate + repro link ·
  English body · per-page ≤8 KB, ≤103 DOM nodes (limits 300 KB / 3000) · robots 7 bots · llms.txt 2.3 KB ·
  no broken internal links · DOI = 10.5281/zenodo.20756155 (published Zenodo concept DOI, resolving link).

## Open items (carried, with obstacles) — see IRREPRODUCIBILITY_LEDGER.md
- γ–lifespan trend [O] (small panel, GC confound, phylogenetic non-independence)
- (v1.3.0) meaning of the archaic genotype co-occurrences [O] (constitution: a present-state snapshot is silent on how a state arose)
- (v1.3.0) telomere "keystone is dynamics, not γ" synthesis [O] (organizes measured facts; an interpretation, not an in-package derivation)
- absolute incidence / lifespan / calendar rate [O] (need external calibration)
- pathology relative scales T, h [O] (shape only; absolute not claimed)

## Not in scope (owned elsewhere)
- Rare / monogenic accelerated-aging (progeroid) syndromes → disease_wp (entered here only as a parameter).
- DOI assignment **done**: Zenodo concept DOI `10.5281/zenodo.20756155` minted and wired into HTML + PDF.
  Remaining publication-phase items: upload the v1.3.0 zip as a new Zenodo version under the concept DOI,
  push the `repro/aging/<slug>/` folders to GitHub, and add the `cross_volume_doi` registry entry.
