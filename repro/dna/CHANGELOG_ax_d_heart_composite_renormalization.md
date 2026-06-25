# CHANGELOG — Appendix D · challenging the heart: composite renormalization to measured cardiac mechanics

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.13 + Appendix A (the γ gene-clock, whose heart result was an honest null) + Appendix C
(the jamming renormalization tower). This increment adds **Appendix D — Heart composite-renormalization
accuracy**, a new applied volume that re-attacks the case that *failed* in Appendix A. It is **add-only**:
no chapter, appendix, number, grade, equation, table, or DOI of v1.13 or any prior appendix is altered.
One new section is added (the site goes from 19 to **20** sections), the contents/sitemap/meta/gate are
extended, and Appendix C gains a forward nav link.

## Why

The heart is the case the framework got wrong, honestly. Appendix A's morphogenesis gene-clock predicted
the **order** in which organ features emerge from the spinodal of the material **γ**, and that order was
verified; but it also tested whether γ predicts **when**, in absolute developmental time, features appear,
and for the heart that was a clean **null** — γ orthogonal to timing, *sharpest in the heart*, Spearman
ρ = +0.071, exact p = 0.882, graded **[O]**. The corpus discipline is that a null is not swept away but is
a discovery waiting for its mechanism (**반증 = 발견**). So Appendix D does not try to make γ predict the
heart — it cannot, and the reason is exact — but asks **what does**, and whether the Appendix C
renormalization tower, pointed at the heart with **measured** data, can explain the failure.

## What is upgraded from Appendix C

Appendix C climbed a tower of **one** phase (cells) packed in **void**, and its absolute moduli were `[O]`
placeholders. Two changes make an **accuracy** test possible:

1. **A real two-phase composite.** Myocardium is cells embedded in a stiff collagen ECM, not cells in void,
   so the second phase is the matrix (modulus B_ecm > 0), not void (B = 0). The exact elastic-mixture
   theorems bracket the composite with **both** phases real:
   ```
   Voigt (upper)  B_V = φ_cell·B_cell + φ_ecm·B_ecm        [V] exact
   Reuss (lower)  1/B_R = φ_cell/B_cell + φ_ecm/B_ecm       [V] exact
   B_R ≤ B_eff ≤ B_V   (Hill 1952; no free parameter)
   ```
2. **Measured cardiac phase moduli** (all `[L]`, cited): single-cardiomyocyte AFM (immature hiPSC-CM
   ~1.25 kPa, Pires 2019; adult rat ~35 kPa, transverse AFM), decellularized myocardial **ECM** (LV ~5 kPa,
   SAN ~17 kPa, AJP-Heart 2024), and the tissue stiffening trajectory (0.1 + 0.3·day kPa chick;
   E2 < 1 → E14 ~10 kPa murine; adult 10–50 kPa) — Majkut, Idema, Swift, Krieger, Liu & Discher 2013,
   *Curr. Biol.* 23:2434-2439, whose proteomics identifies **collagen + excitation-contraction proteins**
   as the daily drivers of the rise.

## The three results, stated once

> **A — pure cell-jamming is insufficient (the falsification, parameter-free).** Cells in void cap at the
> single-cell modulus. The embryonic cell (~1.25 kPa) fully jammed reaches at most ~1.25 kPa, yet the tissue
> stiffens to ~10 kPa (E14) and ~18 kPa (adult) — a rise of 8–14× **past** the ceiling. The stiff ECM phase
> and/or cell maturation is **necessary**; the pure-jamming tower is **falsified** for the trajectory. A
> strict inequality on measured moduli, matching the proteomics. `[V]`.
>
> **B — γ is orthogonal to the stiffening (the explanation of the null).** γ is sequence-fixed, identical at
> every stage, hence **time-invariant**; a constant cannot encode a ~14× ramp, so γ ⊥ trajectory by logical
> necessity — reproducing the Appendix A heart null (ρ = +0.071, p = 0.882) and **explaining** it: the
> timing axis is **composition (ECM)**, orthogonal to the material. `[V]` + `[L]`.
>
> **C — the exact bracket contains the measured tissue (consistency).** From measured ventricular inputs
> (cell ~35, LV ECM ~5 kPa, φ_cell ~0.8) the exact bracket is **[15.9, 29] kPa** and **contains** the
> measured adult ventricular tissue (~18 kPa). The tissue sits **low** in the bracket because isolated cells
> (35 kPa AFM) are stiffer than bulk tissue — a known effect, and exactly why the named obstacle is a single
> **co-registered** preparation. `[L]` / `[O]`.

Illustration (`[F]`): a composition-flow trajectory at fixed measured phase moduli reproduces the
embryonic→adult span (0.16 → 23.5 kPa, monotone, starting soft via early unjamming, ending in the adult
band). The discovery: **the heart's stiffening axis is composition (ECM) + maturation, not material γ** —
which is precisely why γ was orthogonal to heart timing in Appendix A.

## What is honestly NOT claimed (the three open obstacles)

`completion.complete = False`. This is **not** a 100%-accurate heart. The exact bracket `[V]`, the
falsification of pure jamming `[V]`, the explanation of the null `[V]`, the measured phase moduli `[L]`, and
the bracket-consistency `[L]` are in hand. A **tight zero-parameter trajectory prediction** is not — three
accuracy channels remain **[O]**:

1. **co-registered developmental series** — one preparation giving, per stage, `(E_tissue, φ_ecm, φ_cell,
   B_cell, B_ecm)`. With it the composite predicts `E_tissue(t)` with **zero** free parameters and the match
   becomes a tight accuracy `[V]`.
2. **active tension** (myosin) vs passive composite — Majkut's contraction wave speed is linear in `E_t`
   (active), distinct from the passive VP elastic wave `c = √(B/ρ)`.
3. **large-strain** nonlinear strain-stiffening — the bracket here is the small-strain modulus.

The distance to a tight accuracy claim is **one named measured dataset**. The machinery, the measured phase
moduli, the falsification, and the explanation are already in place.

## What changed (all add-only)

New reproduction package `repro/dna/ax-d-heart-composite-renormalization/`:

- `heart/` — 7 modules + package init:
  - `lock` (every measured cardiac input from `param_db.json`, **zero inline magic numbers**),
  - `composite` (the exact two-phase Voigt/Reuss bracket with both phases real; the cells-in-void ceiling
    for the falsification; the VP wave speed `c = √(B/ρ)`),
  - `trajectory` (the measured tissue trajectory + the predicted composition-flow trajectory; non-fit: the
    prediction never reads the target),
  - `decomposition` (the three parameter-free results — A jamming insufficiency, B γ orthogonality,
    C bracket consistency — and the axis identification),
  - `grading` (the **one** place precision ≠ accuracy; `LEDGER` + `completion_status`),
  - `interpreter` (`interpret_heart()` ⊕ `reading_hash` 2×SHA-256),
  - `gate` (fail-closed `D1..D9`; `python3 -m heart.gate`).
- `param_db.json` — measured cardiac moduli, volume fractions, and the tissue trajectory, each with grade +
  provenance; the target trajectory is separated from the physical inputs so a prediction cannot read it.
- `run.py` — top-level runner → `expected/*.json` + `RESULT.txt` (deterministic; 2×SHA-256).
- `README.md`, `LEDGER.md` — the result narrative and the auto-generated honest grade ledger.

New HTML section `docs/dna/ax-d-heart-composite-renormalization/index.html` (VP-SPEC v1.8, answer-first,
prev → Appendix C).

Site wiring (extended, not rewritten):
- `docs/dna/_meta.json` — appendix **D** row appended (chapters 16 + appendices 4 = 20).
- `docs/sitemap.xml` — AX-D URL added (hub + 20 = 21 `<loc>`).
- `docs/dna/index.html` — hub TOC `<li class="apx">`, JSON-LD `hasPart`, see-also cross-link, and the
  overview count ("three applied appendices" → "four applied appendices").
- `docs/dna/ax-c-hierarchical-renormalization/index.html` — forward nav `Appendix D →`.
- `gate_multipage.py` — section/hub-link count `19 → 20`.

## Verification

- `python3 -m heart.gate` → **PASS 9/9** (`D1` two-phase bracket exact · `D2` bracket contains measured
  tissue · `D3` pure jamming insufficient/falsified · `D4` γ orthogonal/reproduces Appendix A null · `D5`
  composition trajectory spans measured · `D6` no magic · `D7` non-fit · `D8` determinism · `D9` honest
  grades/no false victory); `completion.complete = False`.
- `python3 run.py` → deterministic; reference reading hash `a01f16ecc3637ed8`; gate `sha=94355b40c40c3791`;
  byte-identical across runs.
- `python3 gate_multipage.py` → **PASS 230, WARN 1, FAIL 0** (the single WARN is the pre-existing
  source-monolith diff that is warn-only).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
*The heart that failed is now understood — its stiffening axis identified, its modulus bracketed by measured*
*phases, its prior null explained. One co-registered measurement closes it.*
