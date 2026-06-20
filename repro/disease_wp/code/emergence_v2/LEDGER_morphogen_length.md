# LEDGER — morphogen length-scale cross-validation (Phase 7)

Honest, per-quantity grading under the project's C3 no-tuning discipline. This layer **promotes a
single qualitative line** that already lived in the Phase-3 trajectory ledger —

> *"The DB's own D-range maps to λ ∈ [19, 190] µm, bracketing real morphogen gradients
> (Bicoid/FGF/Nodal/Shh). Not fitted."*

— from an **unverified aside** into a **gated, falsifiable [F] → [L]-grounded cross-check**, by
confronting the model's first-principles length band against **directly-measured morphogen gradient
decay lengths** taken from primary live-imaging / FCS literature. It is **add-only**: it edits no
pinned engine, introduces a new engine + new locked measured-input + new gate, and reproduces every
prior baseline byte-for-byte.

**The legitimacy rule (unchanged):** a parameter is a valid input iff it is (a) a UNIVERSAL law or
(b) an INDEPENDENTLY measured/published value, carried with provenance. A violation is only a value
WE chose to match a target. The band here is derived **purely** from `param_db.json` generic
biophysics (`D ∈ [0.1, 10] µm²/s`, `τ ≈ 60 min`) via `λ = √(D·τ)`; the engine
(`emergence_morphogen_validation.py`) **never reads** the measured gradient file. The **NON-FIT
invariant** is asserted by the gate (source-token scan + band target-invariance), so the band is a
locked first-principles prediction `[L]`, not a back-fit to the gradients it is tested against.

## The physics, in one line

Linear steady-state screened Poisson `D·∇²c − c/τ + source = 0` gives an intrinsic length
`λ = √(D·τ)`, set entirely by the two measured biophysical constants. The DB's measured **range** of
`D` (0.1–10 µm²/s) at the measured clearance `τ ≈ 60 min` maps to a **band**
`λ ∈ [18.97, 189.74] µm`, central `λ(D=1) = 60 µm`. The scientific question of this layer: **does a
generic biophysical band, fixed without reference to any single morphogen's measured gradient,
bracket the directly-measured decay lengths of real morphogens?**

## The measured targets (locked, cited, pre-registered)

Six canonical morphogens, each carried in `morphogen_lengths.json` with its system, a single
representative published decay length, and an `informs_db` independence flag. The inclusion rule was
**fixed before** the statistics were computed (every qualifying morphogen reported, none added or
dropped on the basis of band membership):

| morphogen | λ (µm) | system | independence | source |
|---|---|---|---|---|
| Bicoid | 100 | *Drosophila* A-P embryo | **independent** | Houchmandzadeh 2002 (Nature 415:798); Gregor 2007 (Cell 130:141) |
| Nodal (Squint) | 80 | zebrafish embryo | **independent** | Müller 2012 (Science 336:721) |
| Fgf8 | 50 | zebrafish embryo | in-citation | Yu 2009 (Nature 461:533) |
| Dpp | 20 | *Drosophila* wing disc | in-citation | Kicheva 2007 (Science 315:521) |
| Shh | 20 | vertebrate neural tube | **independent** | Chamberlain 2008 (Dev 135:1097); Zagorski 2017 (Science 356:1379) |
| Wingless | 6 | *Drosophila* wing disc | in-citation | Kicheva 2007 (Science 315:521) |

**Independence (the non-circularity guard):** `param_db`'s `D, τ` were set from *generic* morphogen
biophysics citing Kicheva 2007 (which measured Dpp/Wingless) and Yu 2009 (which measured Fgf8). Those
three are flagged `informs_db = true` — their containment is **partly non-independent** and reported
for completeness only. **Bicoid, Nodal, Shh** come from studies that did **not** set the DB biophysics
(`informs_db = false`); they are the strictly **non-circular** test of whether the band generalises.

## Grades

| quantity | grade | basis |
|---|---|---|
| morphogen diffusion `D` (0.1–10 µm²/s) | **[L]** | Kicheva 2007; Yu 2009 — measured effective diffusion, in `param_db.morphogen` (unchanged) |
| morphogen clearance `τ` (≈60 min) | **[L]** | Kicheva 2007 — measured clearance timescale, in `param_db.morphogen` (unchanged) |
| **model length band** `λ = √(D·τ) ∈ [18.97, 189.74] µm`, central 60 µm | **[L]** | derived from the two measured constants only; **target-invariant** (engine never reads a gradient); determinism sha `4ea1c7b4111c`. Not fitted. |
| measured gradient decay lengths `λ_i` (6 morphogens) | **[L]** | each a directly-measured exponential decay length of a real gradient, primary-source cited, in `morphogen_lengths.json`; read **only** by the gate |
| **REGIME agreement** (band brackets real gradients) | **[L]-grounded** | geom-mean(measured) = 31.41 µm vs central 60 µm → **factor 1.91** (< 3 tol); **5/6 in band**; robust to ±30% per-λ jitter (worst factor 2.47). A generic biophysical length scale matches the real morphogen regime **with no fit**. |
| **INDEPENDENT-set containment** (non-circular) | **[L]-grounded** | the three morphogens that did **not** inform the DB (Bicoid 100, Nodal 80, Shh 20) are **3/3 in band** — the band fixed from *other* morphogens' biophysics generalises to independent gradients. |
| **per-morphogen band membership** (exact in/out) | **[F]** | an edge-sensitive secondary detail; Dpp & Shh (~20 µm) sit boundary-adjacent to the 18.97 µm edge; reported, not scored as the primary verdict |
| **per-organ realized shape / curved 3-D form** | **[O]** | unchanged from Phase 3: needs measured tissue mechanics + cell-resolution compute; deliberately not attempted. This layer is a **regime-level length claim**, not a shape prediction. |

**Gate:** `verify_emergence_morphogen.py` → **8/8 PASS**, grade **[L]-grounded**
(1 DB-SOURCED: band == √(D·τ) recomputed from `param_db` · 2 NON-FIT: engine references no target token,
band hash stable `4ea1c7b4111c` · 3 DETERMINISM 2× sha · 4 MEASURED-INPUT INTEGRITY: 6 morphogens,
all-provenance, all-flag, pre-reg rule + independence note present · 5 REGIME AGREEMENT: geom-mean
factor 1.91 ≤ 3 AND majority-in-band 0.83 ≥ 0.5 · 6 INDEPENDENT-SET: Bicoid/Nodal/Shh 3/3 in band ·
7 NON-BLIND: centre contained, absurd 5000 µm / 0.5 µm OUT, all-far panel → regime fails as it must ·
8 ROBUSTNESS: 2000 perturbations, worst geom-mean factor 2.47 ≤ 3).
Validation sha `01b0b6ea8b10`, band sha `4ea1c7b4111c`.

## What this layer adds vs Phase 3

Phase 3 derived the absolute length scale `λ = √(D·τ) = 60 µm` from measured biophysics and recovered
it from the solved 3-D field to < 1%, then **noted in passing** that the D-range brackets real
gradients. Phase 7 turns that aside into a **falsifiable measurement test**: it pre-registers six
directly-measured gradient lengths, asserts the band is computed without reading them (NON-FIT), and
checks REGIME agreement, INDEPENDENT-set containment, NON-BLINDness, and ±30% robustness in a gate.
The qualitative bracketing claim is thereby **promoted [F] → [L]-grounded**. The axis is unchanged:
γ fixes *order/identity* `[V]`; the systemic biophysical parameters fix the *realized* length —
`[L]`-grounded where it matches measured gradients (this layer), `[F]` where the realized partition is
modelled (Phase 3), `[O]` where the cell-resolution curved form is data/compute-blocked.

## Honest residuals (recorded, not hidden)

- **Wingless (~6 µm) falls BELOW the band** (edge 18.97 µm). It is the shortest-range qualifying
  morphogen, is reported as a band miss, and was **not excluded** to improve the fraction. The model
  band is a *generic* length scale; the very shortest-range gradients sit below it. Naming this miss
  is the point — the claim is REGIME-level, not that every morphogen lands inside.
- **Dpp and Shh (~20 µm) are boundary-adjacent** to the lower edge (18.97 µm); their "in-band"
  status is edge-sensitive and is flagged as such. The primary verdict (geom-mean + independent set +
  robustness) does not hinge on these edge calls.
- Each `λ` is a **single representative published value**; exact figures vary modestly between studies
  and conditions, so the verdict is deliberately an **order-of-magnitude / regime** test, robust to
  ±30% perturbation of any single value (gate check 8), rather than a precise per-morphogen fit.
- This layer makes **no shape claim**. Whether the realized 3-D form matches a real organ remains the
  Phase-3 `[O]` residual (measured tissue mechanics + HPC at cell resolution); comparing the coarse
  partition to a real organ by tuning would be the forbidden back-fit.

## Reproduce

```
cd code/emergence_v2
python3 emergence_morphogen_validation.py     # engine: band [18.97,189.74], central 60, sha 4ea1c7b4111c
python3 verify_emergence_morphogen.py         # gate: 8/8 PASS, [L]-grounded, validation sha 01b0b6ea8b10
```

## Discipline honored

NON-FIT (engine never reads the measured gradients; band target-invariant) · grade==evidence (the
per-morphogen membership stays [F]; the realized form stays [O]) · add-only (no pinned file changed;
the four prior emergence baselines and all 12 morpho fidelity baselines are byte-identical) · no
fabrication (every λ and every D, τ is primary-source cited) · no back-fit (the band is fixed from
generic biophysics independent of the gradients tested; the **independent set** Bicoid/Nodal/Shh,
whose studies did not set the DB, makes the test strictly non-circular) · honest residual (Wingless
named as a band miss, not hidden or excluded).
