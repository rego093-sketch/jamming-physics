# MASTER MANUAL — Aging & Senescence (aging_senescence_vp_site)

How this package is built, how to reproduce it, and how to rebuild the site. Self-contained: it carries
the vendored substrate, the VP-SPEC, and the measured node identities. Constitution C0 overrides on any
conflict.

## 1. What this package is
The **integrative capstone (temporal) layer** of VP Theory. Aging is modeled as the slow loss of defense
gain of every homeostatic setpoint, plus the accumulation of cells stuck in irreversible R19 attractors
(senescence), and it is the dominant risk multiplier for every pathology kernel. It emerges no organs
owned elsewhere; it inherits node identity γ from DNA (SSOT) and adds the temporal dynamics.

## 2. The substrate (vendored — never re-derive)
`inherited/vp_substrate.py` holds the R19/FHN math (do not modify; SEED=19):
- field: `sdot(s,g,h) = g·s − s³ + h`  (two basins)
- `barrier(g) = g²/4`     — stability barrier between basins
- `spinodal(g) = 2(g/3)^1.5` — drive |h| past which one basin disappears (discontinuous flip)
- `settle(g,h,s0)`, `is_on(...)`, `dwell(g,brake) = g^1.5/(K+brake)` — switch run-length / reservoir
- `seed_everything(SEED)`, `Organ`, `Neuron`, `dominant_freq`

## 3. Node identities (measured γ — vendored)
`inherited/organ_gamma.json` (`genes`): TP53 1.429832 · CDKN2A 1.442444 · FOXO3 1.594156 · TERT 1.553876.
γ = −mean SantaLucia 1998 NN ΔG37 over the promoter window TSS−2000..+500 (2501 bp); MEASURED, never
fitted; each row carries its NCBI accession, strand, and window. The fifth node (systemic setpoint drift)
is diffuse (no master gene). γ sets each node's barrier (γ²/4) and dwell (γ^1.5), hence the emergence
order (γ ascending): senescence → arrest switch → telomere maintenance → longevity signaling.

## 4. The research program (RA1–RA7)
Deterministic R19 simulations. RA1–RA6 in `repro/_engine/aging_dynamics.py`; RA7 in
`repro/_engine/xspecies_discriminant.py`.
- RA1 setpoint drift — creep inside the basin, then catastrophic flip past the spinodal (one law, two faces).
- RA2 senescence — supra-spinodal arrest is one-way (absorbing); arrested cells accumulate.
- RA3 reservoir depletion — finite well, capacity ~ γ^1.5; telomere loss = exhaustion, not a special clock.
- RA4 hallmarks — all ten map to RA1/RA2/RA3 mechanisms, no orphans.
- RA5 risk multiplier — shrinking barrier ⇒ rising Kramers hazard ⇒ convex age-incidence (oncology seam).
- RA6 rate of aging — a dominant shared rate (0.889) plus per-system residuals.
- RA7 cross-species — human aging genes are not special; no γ switch; the switch is TP53 copy number [L].

## 5. Pathology (derived, non-rare diseases)
`repro/_pathology/setpoint_failure.py`. One law: an age-related loop-gain drop d lowers effective gain to
γ(1−d), shrinking the barrier (drift) and the spinodal (catastrophe). Sarcopenia = monotone drift;
frailty/multimorbidity = accelerating co-failure across setpoints; aging-as-cancer = convex crossing
hazard. Rare/monogenic (progeroid) forms belong to `disease_wp` and enter only as a cited parameter.

## 6. How to reproduce (research)
```
python repro/run_all.py            # emergence + RA1–RA7 battery + pathology + gates
python repro/_verify/gates.py      # research_gate (determinism + all_targets_pass + all_green)
```
Determinism: the engine emits a byte-identical result on two runs — `d6506074f9f9ae61…`. The cross-species
γ reproduces offline from `inherited/aging_promoters.cache.json` (no network needed). To re-fetch from NCBI
(provenance only; cache stays canonical): run `repro/_engine/fetch_gamma_xspecies.py`.

## 7. How to (re)build the site (writing)
Writing is **locked** until research is signed off:
```
python repro/_verify/gates.py          # confirm all_green
python -c "import sys;sys.path.insert(0,'repro/_verify');import gates;gates.write_research_complete()"
echo writing > PHASE
python tools/build_docs.py             # delegates to tools/render_site.py
```
`tools/render_site.py` pulls every displayed number from the engine modules, so the canonical HTML cannot
drift from the reproducible result (C1). It emits `docs/<slug>/index.html` ×11 + hub + `_meta.json` +
`sitemap.xml` + `robots.txt` + `llms.txt` + `manifest/aging_senescence_vp_site.csv`. CSS is local at
`docs/assets/css/site.css`.

## 7b. How to build the citation-layer PDF (publication phase)
```
python tools/build_pdf.py              # docs/  ->  pdf/aging_senescence_vp_site.pdf
```
`tools/build_pdf.py` builds the whitepaper **from the canonical HTML**, not from the engine: it parses
`docs/<slug>/index.html` and lays out one document — a citation title page (full title, author + ORCID,
version, the published `DOI: 10.5281/zenodo.20756155`, the hub URL, the SEED=19 result hash, abstract,
headline results) → contents → the **13 chapters** in the same order with the same prose and the same
numbers. Because the numbers already live in the engine-generated HTML (C1), the PDF cannot drift.
Web-only furniture (breadcrumb/page nav, JSON-LD, the claim-strip GitHub/DOI link) is dropped; answer-first,
abstract, body, tables, vp-cards and honest grades are kept. Fonts are embedded DejaVu (Serif body / Sans
headings / Mono hashes) for full Greek and math-symbol coverage. The build is invariant
(`rl_config.invariant = 1`), so two runs are byte-identical. It refuses while the writing lock is on and
requires the site to be built first, so the order is always `build_docs.py` → `build_pdf.py`.

### Cross-species confound audit (v1.2.0)
`repro/_verify/xspecies_robustness_audit.py` is an independent verification layer that audits the
§9 result for the confounds the per-gene tests ignored. It re-derives γ bit-for-bit from the cached
promoters (engine untouched) and runs: GC-confound (γ↔GC≈1), body-mass correction (intrinsic-longevity
residual), Felsenstein 1985 phylogenetic independent contrasts on a dated tree, multivariate LOOCV,
leave-one-out, switch-threshold robustness, and a TERT focus. Deterministic (SEED=19); the artifact
hash is `c771cf7e…` and is imported by `tools/render_site.py` so §9 prose is generated from its numbers.
Run `python repro/_verify/xspecies_robustness_audit.py` for the full JSON + verdict. Finding: the null is
robust (the weak shared 4-gene lean is fully confound-attributable); TERT is the residual [O] exception.

### Telomere keystone + archaic observation (v1.3.0)
Two reproducible engine modules extend the cross-species result, both deterministic (no seeds needed —
pure arithmetic over the cached promoters) and both re-deriving γ bit-for-bit from a committed cache.
- `repro/_engine/archaic_discriminant.py` (**RA8**, OBSERVATION ONLY): measures the four masters across a
  cross-sectional set of seven dated genomes (present-day GRCh37 reference; Altai, Vindija 33.19,
  Chagyrskaya Neanderthals; Denisova; Ust'-Ishim and Loschbour ancient modern humans). Each promoter is
  the GRCh37 reference plus that individual's homozygous-derived FILTER-pass substitutions. It reports
  per-individual γ, the γ spread per gene (every range < 0.0016), the substitution counts (TERT carries
  the most archaic substitutions, 13), and the invariance of the two recurrent TERT cancer-promoter
  positions. Constitution: the package reports measured present-states only and makes no claim about how
  any state arose; the meaning of the co-occurrences is [O]. Offline reproduce loop: 25/25 sequences match.
- `repro/_engine/telomere_keystone.py` (**RA9**): measures the canonical telomere repeat (TTAGGG)n at
  γ = 1.3298 — strand-symmetric, the lowest γ of any aging sequence here, length-independent (a near-exact
  universal constant) — and synthesises RA7 + RA8 + the γ^1.5 reservoir law into the verdict that the
  telomere is the keystone of aging **dynamics, not γ**: the lever is off the promoter-γ axis (reservoir
  length + attrition). γ-invariance [V]; reservoir law [F]; the synthesis [O]; rates [L].
- `repro/_engine/fetch_gamma_archaic.py` documents the online provenance path (Ensembl GRCh37 + Max Planck
  EVA VCFs). Both modules are wired into `vp_age_engine.circulate()` (keys `archaic_observation_RA8`,
  `telomere_keystone_RA9`); the result hash is re-pinned at `62d5e1eb…`. Chapters §10/§11 render from them;
  the previous pathology/reproducibility chapters are §12/§13.

## 8. Grading discipline (C1/C3) and no-tuning
LOCK → Derive → Gate. Every constant is a measured input or a derived value, never chosen to hit a target.
Grades: [V] verified (measured/reproduced) · [L] cited anchor · [O] open (with a stated obstacle). Every
[O] item is collected in `IRREPRODUCIBILITY_LEDGER.md` and cross-checked against the HTML.

## 9. DOI
**`10.5281/zenodo.20756155`** — the published Zenodo **concept DOI** (resolves at
https://doi.org/10.5281/zenodo.20756155). It is a single constant (`DOI_TBD`) in each generator
(`tools/render_site.py` and `tools/build_pdf.py`) and is rendered as a resolving link in the HTML
(JSON-LD, claim-strip, footer) and on PDF page 1. Each version increment is uploaded as a new Zenodo
version under this concept DOI; the `cross_volume_doi` registry entry in the parent framework is added
when convenient.

## 10. File map
```
START_HERE.md  CHARTER.md  VP_SPEC_v1_8.md  VERSION(1.4.0-writing)  PHASE(writing)
CHANGELOG.md  MASTER_MANUAL.md  COMPLETION_LEDGER.md  HANDOVER.md  IRREPRODUCIBILITY_LEDGER.md
inherited/  vp_substrate.py  organ_gamma.json  organ_identity.md
            aging_gamma_xspecies.json  aging_promoters.cache.json
repro/      run_all.py
  _engine/  vp_age_engine.py  aging_dynamics.py  xspecies_discriminant.py  fetch_gamma_xspecies.py
  _verify/  stress_tests.py  gates.py  xspecies_robustness_audit.py
  _pathology/ setpoint_failure.py
reports/    emergence_results.json  research_complete.json  XSPECIES_ROBUSTNESS_AUDIT.md
tools/      render_site.py  build_docs.py  build_pdf.py
docs/       index.html  _meta.json  sitemap.xml  robots.txt  llms.txt  assets/css/site.css
            01-…/ … 11-…/  (each index.html)
pdf/        aging_senescence_vp_site.pdf   (citation layer, built from docs/)
manifest/   aging_senescence_vp_site.csv
```
