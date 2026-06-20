# HANDOVER — cardioresp_vp_site (→ next session)

**State at handover:** v0.5.0 · PHASE = writing · `OVERALL: PASS (11/11), drift 0` ·
concept DOI `10.5281/zenodo.20755371`. Read this top-to-bottom, then resume without confirmation.

---

## 1. What just shipped (v0.5.0)

The reproducibility technology of `analgesic_threshold_logic` v2.0 (`10.5281/zenodo.20733420`) was
**missing from this package's roadmap**; v0.5.0 inherits it, applies it in full, binds this package's
concept DOI, and records the retroactive-application plan for the siblings. **No scientific result
changed** — the engine output is byte-identical to v0.4.0 (sha `25900a90079a…`).

Concretely, now present and gated:
- `manifest/SHA256SUMS.txt` (frozen last), `repro/_verify/repro_manifest.py`, `claim_scanner.py`,
  `doc_integrity.py`; drift-0 + offline gates in `gates.py`; suite section [7] in `repro/run_all.py`.
- `CONSTITUTION.md`; four-document SSOT (`CHANGELOG` / `MASTER_MANUAL` / `COMPLETION_LEDGER` / this file).
- Concept DOI wired site-wide (pages, hub, JSON-LD, `_meta.json`, `llms.txt`, CSS pill); build made
  wall-clock-free (`RELEASE_DATE = 2026-06-18`); placeholders removed.
- **Canonical site expanded (writing phase) to VP-SPEC v1.8 retrieval-ready depth — 14 pages** (12
  sections + hub + index): new §10 (DNA emergence chain gene → γ → R19 switch → oscillator), §11
  (shared-substrate spectrum: Mayer waves, airway-tone switch, obstructive-apnea regime, periodic
  breathing, fever co-scaling, cough — firewall-clean), §12 (methods/reproducibility). DNA-emergence
  grounding foregrounded; SEO surface (keywords/OG/Twitter/Highwire/`knowsAbout`) strengthened; ledger
  has a third [O] row for §11. Engine output unchanged.
- `zenodo/` whitepaper (PDF + TeX) + `ZENODO_METADATA.md` (excluded from the manifest).

## 2. How to verify on entry

```
python repro/run_all.py        # expect: OVERALL: PASS (11/11 checks), drift 0
```

If R6 reports FAIL on a fresh checkout, the manifest simply needs re-freezing (fail-closed by design):

```
python repro/_verify/repro_manifest.py freeze
python repro/run_all.py
```

## 3. Invariants you must not break

- **Firewall (CONSTITUTION A1).** γ is a stacking-stability read, never a clinical magnitude. No drug,
  dose, therapy, efficacy, or safety language reaches `docs/` — the fail-closed scanner (R7) enforces it.
- **Freeze the manifest LAST.** Any edit to a hashed file (anything outside `reports/` and `zenodo/`)
  after the freeze invalidates R6. Re-freeze, then re-run.
- **Do not hardcode the manifest file-count** in any hashed governance doc — it is computed by
  `repro_manifest.verify()` at runtime. (Stating "11/11 gates" / "drift 0" is fine; those are fixed.)
- **Keep the build wall-clock-free.** `RELEASE_DATE` is pinned; do not reintroduce `datetime.today()`.
- **`zenodo/` is excluded from the manifest** (LaTeX may embed timestamps). Keep deposit artifacts there.
- **Grades.** Only {[F],[V],[L],[O]}; every [O] needs an obstacle in the ledger (R8/R9).

## 4. Next work (in priority order)

1. **Retroactive application to siblings (FUTURE_WORK §8).** Execute the inheritance checklist on the
   existing packages, scanner-vocabulary-tuned per package. Suggested order by clinical-surface risk:
   `mind_vp_site` → `disease_wp` → `neuro_emergence_chain_integrated` → `dna_vp_site` →
   `universal_morphogenesis_geneclock` → the pure-physics set (`vp_physics`, `geodynamics`, `cosmology`,
   `fluid_dynamics`). Build the apparatus into `integumentary_vp_site` (v0.3.0) at source.
2. **Science roadmap (FUTURE_WORK §§0–7).** Mayer-wave baroreflex (~0.1 Hz, reuses T5) → asthma
   methacholine dose–response (reuses the oncology Kramers kernel) → OSA pharyngeal switch + loop-gain →
   periodic-breathing spectrum → fever HR–RR co-scaling → cough excitation threshold → the cor pulmonale
   seam (awaits the circulatory package). Each enters `docs/` only after it passes its discriminant under
   wide sweeps with no per-target tuning, and only with an honest grade.
3. **Zenodo deposit.** Upload the v0.5.0 zip + `zenodo/*.pdf` + `zenodo/*.tex` under concept DOI
   `10.5281/zenodo.20755371`; confirm the landing page matches `zenodo/ZENODO_METADATA.md`.

## 5. Conventions (unchanged)

Single author Young Jae Lee (ORCID 0009-0002-7535-8245); CC BY 4.0. One zip per delivery, root
`cardioresp_vp_site/`, package-relative paths, English body, Korean session chat. Four-document SSOT at
every version increment. No self-deprecating language; the [F]/[V]/[L]/[O] vocabulary is the honesty
mechanism, not a tone. Direct execution, no confirmation pauses.
