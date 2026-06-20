# MERGE NOTE — three rejected manuscripts folded into The Configured Continuum

**Scope:** fluid-dynamics lane only (VP_SPEC v1.6). No other paper touched.
Concept DOI of the host whitepaper: `10.5281/zenodo.17972568`.

All three are the author's own unregistered/rejected manuscripts, folded in as
**reproduction/evidence backing** for existing whitepaper claims — not added to
the 6-paper registry (Ch.2 LOCK), not promoted to new whitepapers.

---

## Fold 1 — Metriplectic / Onsager  →  §9 Pillar IV + Appendix E
- Former standalone DOI `10.5281/zenodo.17758705`.
- ADD `repro/fluid-dynamics/09-pillar-iv-dissipative-arrangement-sets/metriplectic-onsager/`
  (full ADG ensemble + NS reference 64/256/512 + robustness). `PROVENANCE.md` added.
- The in-page `metriplectic_vortex.py` reference model is kept; ensemble
  `eps_tot_mean ~0.205–0.216` matches its plateau `I=0.21`, extends `Re_eff~5000`.
- EDIT ax-e claim-strip GitHub link: paper-root → the metriplectic-onsager folder.

## Fold 2 — RCCI rotcore audit  →  §7 Pillar II + Appendix G
- Former standalone package `rotcore-doi-v1_3_9`
  (manuscript `rotcore_prf_manuscript_single_v1.3.6.tex`).
- The v139 result CSVs were ALREADY present in `…/07-…/rotcore/` and are
  byte-identical — NOT duplicated. What was missing (now added) is the
  generation provenance:
  ADD `repro/fluid-dynamics/07-pillar-ii-geometric-arrangement-fixes/rotcore/audit-source/`
  = metric generators (`code/scripts/`), formal metric spec
  (`docs/METRICS_SPEC_*.json`), v138 legacy tables, source manuscript, audit
  trail. `PROVENANCE.md` added.
- EDIT ax-g claim-strip GitHub link: paper-root → the §7 section folder.

## Fold 3 — AGC anomalous geometric contraction  →  §10 Reach (foreign domains)
- Former standalone package `AGC_DOI_v3`: "Anomalous Geometric Contraction of
  Hyper-Rotating Cores via Shockwave Confinement in High-Density Stiff Media"
  (compressible Euler / HLLC / Tait EOS / negative-centrifugal).
- This phenomenon was absent from the whitepaper (Tait/HLLC/centrifugal/stiff-
  media all 0 hits) → genuine gap. It is a foreign-domain reach of the
  rotation-arrangement mechanism, which is what §10 collects.
  ADD `repro/fluid-dynamics/10-reach-universality-same-mechanism-foreign/agc-rotating-core-contraction/`
  (per-figure/table CSVs, grid-convergence + toy-contraction data/figures,
  Euler–HLLC solver template). `PROVENANCE.md` added.
- §10 now cites AGC in body prose (a number-free foreign-domain reach paragraph)
  and links it in the claim-strip; manifest §10 words recomputed accordingly
  under the v0.8 counter. See MIGRATION_REPORT_v0_8.md.

---

## Spec-compliance summary
- Lane rule (Ch.1): everything under fluid-dynamics. OK.
- Registry (Ch.2 LOCK): untouched; no 7th paper. OK.
- Large-data (Ch.12-D): folds are 688K / 752K / 972K — all far below the
  100MB threshold → in-repo is correct, no Zenodo offload. OK.
- No duplication: rotcore v139 CSVs not re-copied (verifier reads the originals).
- Caches: all `__pycache__` / `*.pyc` stripped.
- Phase 1–3 gate (`reports/1-3-flu.gate.json`): UNAFFECTED. The only docs edits
  are two claim-strip hrefs (ax-e, ax-g); `.claim-strip` is excluded from the
  body word count (Ch.8), and external links are not the internal-link check.
  Section/word/SVG counts unchanged.

## Author follow-ups (NOT done here — need tools/ or Zenodo access)
1. Re-run `tools/gate.py` for the **Phase 7** gate (Ch.12): every claim-strip
   GitHub link must be 1:1 with a real folder. ax-e and ax-g now resolve to real
   folders, so this should pass once pushed.
2. **AGC editorial hook (Fold 3):** to make AGC a *cited* reach example, add one
   sentence in §10 body (or a dedicated appendix, e.g. `ax-y-…`) referencing
   `agc-rotating-core-contraction/`. That edit changes body word count, so it is
   left to you; update `manifest/fluid-dynamics.csv` words for that section if
   you do it, then re-run the gate.
3. **Zenodo:** mark old records `17758705` (metriplectic) and the rotcore/AGC
   records as *isSupersededBy / isVersionOf* the Configured Continuum record
   `17972568`, or leave them historical.
4. Optional: regenerate figures locally so committed PNGs match your latest runs.

## FINAL STATUS
After the v0.8 migration + two root-cause gate corrections, **fluid-dynamics passes Phase 1/2/3** under the bundled (v1.7) gate; physics still passes too. Full detail in MIGRATION_REPORT_v0_8.md.

## Update — tools/ kit found in physics_site_v0_8, and AGC now linked in §10

The physics site archive (`physics_site_v0_8_PRECISE_FIX`) contains the full
Phase-0 kit: `tools/gate.py`, `inventory.py`, `split.py`, `render_eq.js`,
`build_hub.py`, `derive_meta.py`. It PASSes on the physics paper. **But it is a
newer generation than the toolchain that built this fluid archive**, so it
cannot gate fluid as-is. Concrete evidence (ran the real gate on fluid):
- Display-eq is counted via the `data-eq="…"` attribute on each eq `<img>`
  (physics: 1281 present). Fluid eq figures have only `alt="…"`, no `data-eq`
  → the gate sees `display 0 != N` for every section with display equations.
- Manifest schema differs: physics `paper_id,code,slug,title,star,words,…` vs
  fluid `no,code,slug,title,words,…`.
- Word counter differs: `inventory.word_count` =
  `len(re.findall(r"[A-Za-z0-9][A-Za-z0-9\-'’/×·]*", text))` over `<main>` minus
  aside/abstract/h1/.pn. On fluid §10 it yields **818**, but the fluid manifest
  says **809** — i.e. the fluid manifest was produced by a *different* counter,
  so fluid already fails this gate's ±0.5% word check before any edit.

Implication: to gate fluid with these tools it must first be **migrated** to the
v0.8 convention — a content-preserving operation: (a) regenerate the manifest
`words` (and schema) with `inventory.word_count`, and (b) add `data-eq="{eq-id}"`
to the 40 eq `<img>` tags (id derivable from the SVG basename, e.g. `flu-06-002`).
That migration is a project-level decision (it changes the manifest the author
has been using) and the v1.7 gate's content checks (abstract-number ⊆ body,
key-figure) may surface pre-existing page issues that must not be fixed by
altering meaning/numbers. It was therefore NOT done unilaterally.

What WAS done now (gate-neutral, verified with the real `gate.words_of`):
- EDIT §10 claim-strip — added an explicit third link
  `AGC reach exhibit (GitHub)` → the `agc-rotating-core-contraction/` folder.
  It sits inside `<aside class="claim-strip">`, which the word counter strips,
  so `words_of(§10)` is **818 before and after** (zero word impact). External
  github href is not subject to the internal-link check. So AGC is now surfaced
  directly on the §10 page, with no gate regression under either toolchain.

DONE: the v0.8 migration was carried out (the user chose it); the AGC §10 body
sentence is now added and the manifest recounted with the v0.8 tool. Full details
and the remaining Phase-2 analysis are in MIGRATION_REPORT_v0_8.md.

## Verification run (검수 — actually executed, not just present)
- Fold 1 metriplectic: `src.parameter_sweep`, `NS_reference/generate_viscous_data.py`,
  `src.plot_dissipation_saturation`, `src.check_eps_saturation_universality` all
  ran clean. `dissipation_vs_Re_metriplectic.csv` reproduced **byte-identical**;
  NS CSV reproduced identical to machine precision (1-ULP float-repr only). The
  author's shipped data-of-record files were restored after the check; the one
  genuinely new figure `figures/eps_saturation_universality.png` (README §5) was
  kept. eps_tot clusters 0.205–0.216, matching plateau I=0.21.
- Fold 2 rotcore: `verify_rotcore.py ./rotcore` → **PASS, worst mismatch 2.83e-12**
  (matches the published claim). All three `METRICS_SPEC_*.json` parse; all four
  `code/scripts/*.py` compile.
- Fold 3 AGC: all data CSVs parse (note: `fig2`, `tableS1`, `cylinder…coefficients`,
  `shocktube_reference_solution` are header-only **skeletons** in the source
  package — substantive data is in fig3/fig4/figS1/sensitivity/tables/toy_model);
  `figure_table_mapping.json` valid; `euler2d_solver_template.py` compiles; toy
  contraction `R_eq/R0` decreases with M_rot as expected (contraction trend).

## Word-count / manifest decision (why §10 body was NOT auto-edited)
The gate's body word count is computed from the source (.tex)-derived rule, not
from HTML text; an HTML recount overshoots by ~4–9% even after excluding
abstract/claim-strip/nav/h1/figures, so it cannot be reproduced to the ±0.5%
gate tolerance without `tools/split.py`/`gate.py`. To avoid leaving a gate FAIL,
no body prose or manifest `words` value was guessed. The AGC §10 citation
sentence is therefore left as the author's editorial step (run `tools/gate.py`
to recount after adding it). The §10 claim-strip already deep-links to the
section folder that now contains `agc-rotating-core-contraction/`, so AGC is
reachable from the page today.

## Merge instructions (Ch.5 — author runs)
From repo root: `unzip` (overwrite allowed) → confirm Phase 7 gate →
commit: `phase-merge fluid-dynamics rejected-manuscripts (lane OK)`.
