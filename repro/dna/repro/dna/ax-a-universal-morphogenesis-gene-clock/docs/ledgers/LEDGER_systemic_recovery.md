# LEDGER — Systemic-Parameter Shape Emergence (통합 등급 / integrated grades)

> **v1.9.1 systemic-recovery fold-in.** Add-only over the v12 appendix. This ledger is the single
> grade-of-record for the folded-in `code/emergence_v2/` engines + `code/analyses/` boundary studies,
> and it states the **integrated law** that re-reads Appendix A's measured null as a boundary and
> fills past it with provenance-graded *systemic parameters*. The whitepaper §1–§13, the appendix
> engines, the measured γ / Carnegie-stage tables, and every null value are **unchanged**.
>
> **DOI of record:** `10.5281/zenodo.20471407` — maintained; this is a new living-version snapshot.
>
> **Grades:** **[V]** in-package verified/reproduced (2× sha256) · **[L]** locked & cited independent
> measurement or universal law (legitimate to use) · **[F]** fixed modelling choice (documented) ·
> **[O]** open: a missing *measured* input is named, nothing is claimed.

---

## 0. 통합 법칙 / The integrated law

**내재 γ는 *무엇이 / 어떤 순서로* 를 결정론적으로 고정한다 [V]. 그러나 *언제 / 얼마나 큰가* 는 어떤
정적 게놈 스칼라도 담지 못하는 *systemic·관계적* 양이다. 그 systemic 파라미터(시간 = 동역학,
크기 = dosage)를 넣으면 *실현된 양*이 회복된다 — 그 파라미터가 *측정되면* [L], *모델뿐이면* [F],
*없으면* [O].**

> Intrinsic promoter-stiffness γ deterministically fixes **what** forms and in **which order** [V].
> **When** and **how large** is a systemic, relational quantity no static genomic scalar can carry;
> supply the systemic parameter (time = dynamics, size = dosage) and the realized quantity is
> recovered — graded by the *provenance* of that parameter, never by fitting it to the target.

| axis | intrinsic γ | systemic parameter | grade |
|---|---|---|---|
| emergence **order** | `argsort(spinodal γ)` | — | **[V]** |
| timing (relative order) | null (ρ=0.07) | relay network topology | **[F]** recovered (ρ=0.44, core 0.85) |
| timing **absolute clock** | — | measured protein half-life (Schwanhäusser 2011) | **[L]**-grounded *(Phase 1)* |
| **body / face shape** | dwell core | E (lifestyle-energy **dosage**) | **[L]** H²=0.51, twin +37% |
| organ ratio-change (growth) | — | cited allometric exponent | **[L]-grounded** (widened n=11: ρ=0.80, exact p=0.0047; pre-registered set) |
| organ **absolute mass** | dwell null (ρ=0.11) | measured coefficient / growth atlas | **[O]** |
| continuum **3-D trajectory** (positional info) | — | measured morphogen D·τ → λ=√(Dτ) | **[L]**-scale (λ=60 µm) / partition·form **[F]** *(Phase 3)* |
| exact anatomy (cell resolution) | — | measured tissue mechanics + HPC | **[O]** (back-fit forbidden) |

The architecture that *guarantees* the [L] reading: **the engine reads only `param_db.json`
(measured γ + cited/universal parameters) and never the validation targets.** The gates' **NON-FIT
invariant** enforces that separation, so a DB value is grounded, not back-fit.

---

## 1. Phase 1 — heart (dynamics → absolute timing)

`code/emergence_v2/emergence_engine.py` + `verify_emergence.py` → **gate 7/7 PASS** (result-hash
`939ae9924a6c`).

| quantity | grade | basis |
|---|---|---|
| emergence **order** of cardiac sub-stage masters | **[V]** | `argsort(spinodal γ)` from measured γ; deterministic readout. |
| **onset** in *absolute hours* | **[L]**-grounded | relay ODE with rate = ln2 / half-life, half-life **46 h measured** (Schwanhäusser 2011, `param_db`); onset emerges in real time units (~46 h/stage, window ~184 h ≈ 7.7 d) **without fitting to the target**. |
| **size** = dwell(γ) × (available time)^α, α=1 | **[F]** | one universal supply rule; size *emerges*, not claimed against measured mass. |
| size vs **measured** organ mass | **[O]** | measured growth coefficient absent. |

The systemic parameter (a **measured dynamical constant**, the half-life) is what turns the
γ-timing null into a grounded absolute clock — intrinsic γ alone is orthogonal to timing
(ρ=+0.071, exact-perm p=0.882; NKX2-5 ranked near-last by γ).

---

## 2. Phase 2 — visceral organs + allometric growth (dosage / scaling → ratio-change)

`code/emergence_v2/emergence_organs.py` + `verify_emergence_organs.py` → **gate 6/6 PASS**
(result-hash `40225433a67a`).

| quantity | grade | basis |
|---|---|---|
| 8-organ emergence order (Part A) | **[V]** + dwell **[F]** | measured γ readout + relative dwell. |
| **allometric law** f ~ M_body^(b−1), cited mammalian exponent b | **[L]** | Stahl 1965 / Kleiber-regime exponents, read as a **universal law**, not tuned. |
| does cited b predict human organ **ratio-change**? | **[O]** (n=8) → **[L]** (widened n=11) | Spearman(e_pred = b−1, e_obs) = **+0.690**, exact-perm **p = 0.069** (n = 40320, 8 organs) → graded [O] at the time (`grade == evidence`). **Phase 5 widening (pre-registered, n=11): ρ=+0.800, exact p=0.0047 → promoted [L]**; wide gate 8/8 sha d82eeb925973, see `code/emergence_v2/LEDGER_organ_allometry_wide.md`. |
| **brain anchor** | **[V]** (within-test) | brain has the most-negative predicted *and* observed allometry (e_obs(brain) = −0.559). |
| honest residual | **[O]** | measured human-brain slope (−0.559) is steeper than the cited value (−0.25). |

Validation targets (ICRP-89) live in `validation_targets.json`, **separated from the engine**; the
gate scores post-hoc only. The headline obeys the no-tuning rule: a large but p=0.069 effect is
reported as **[O]**, not forced to [V].

---

## 3. Phase 3 — reduced-order RD trajectory layer (measured D·τ → positional information)

`code/emergence_v2/emergence_trajectory.py` + `verify_emergence_trajectory.py` → **gate 7/7 PASS**
(result-hash `b2b34a770f5a`).

| quantity | grade | basis |
|---|---|---|
| intrinsic length **λ = √(Dτ) = 60 µm** | **[L]**-grounded | from **measured** morphogen D·τ (`param_db.morphogen`, Kicheva 2007); DB D-range brackets λ ∈ [19, 190] µm (Bicoid/FGF/Nodal/Shh). |
| λ recovered in the solved 3-D field | **[V]** | screened-Poisson `D∇²c − c/τ + source = 0` (deterministic Jacobi); λ_field → √(Dτ) within < 1% (grid err N=24/32/48 = 0.978 / 0.919 / 0.785 %, decreasing = grid convergence, physics not lattice). |
| nested **positional-information** partition (French-flag) | **[F]** | threshold θ partitions territories of width λ·ln(1/θ); boundaries match physics k·λ·ln(1/θ) within ~1%. |
| growth-zone **negative allometry as a first-principles mechanism** | **[F]** | fixed λ in a growing axis drops apical-territory fraction ∝ L⁻¹ (fit exponent −0.96 ≈ −1 analytic) — Phase-2 negative allometry *re-derived*, fraction **not** fitted. |
| exact 3-D anatomy (cell resolution) | **[O]** | measured tissue mechanics + HPC absent; back-fit forbidden. |

Non-blind: planted λ* = 37 recovered R² = 1.0000; shuffled R² = 0.008.

---

## 4. Boundary analyses (`code/analyses/`)

Reduced-order recoveries that motivate the law; **all [F] (no tuning)** unless an input is measured:

- `reduced_order_timing.py` — heart timing recovered from γ (ρ=0.07) to network-depth / relay
  (ρ=0.44, core 0.85); above random-DAG upper tail, θ-invariant, non-blind. **[F]**. Absolute dates,
  same-depth fine order → **[O]**.
- `shape_emergence_dosage.py` — dwell(γ) alone gives the organ-mass null (ρ=0.11); inserting
  **dosage** (E) makes body shape emerge (**H²=0.51**, twin +37 %, measured-heritability [L] anchor).
  Organ absolute mass via dosage → **[O]**.
- `emergence_with_parameter.py` — PoC that *actually uses* the parameter to grow (time, size) shape
  **without target-fitting**. **[F]**; measured-validated shape → **[O]**.
- `NULL_존재이유_그리고_모델한계.md` — why the genome stores conditional *rules*, not *values*:
  endpoints encoded, the **middle (trajectory · timing · size) emerges**; a cell-constant scalar γ
  cannot carry cell-to-cell *differences*.

---

## 5. Re-label of the old `grow_to_target` geometry demo (numbers unchanged)

The Layer-2/3 scan-fitting demo (`code/grow_to_target.py`, `demo_morpho_plus.py`) converges:
global surface **RMS 2.31 → 0.055**, **Chamfer → 0.000**; per organism **head 0.06 / bird 0.08 /
quadruped 0.10 / fish 0.07**. These figures are **real and reproducible** and verify **target-fitting
geometry [V]**.

**But this is *not* realized shape emergence.** The **scan supplies the coordinates** (the demo's own
header: *"DNA/engine sets S0 (size, symmetry); the scan sets the individual's coordinates"*), and **no
systemic parameter** (dynamics or dosage) produced the realized form. *As shape emergence*, the demo
is therefore graded **[O]**.

Contrast — **the only axis in this package whose realized shape comes from a *measured* systemic
parameter** is the gene×environment fat-fold `form(P,E)` driven by lifestyle-energy **dosage**:
variance decomposition **H²=0.51** (twin-anchored [L], `morpho_decomposition.py`), MZ-twin divergence
+37 % body / +25 % lower-face roundness. The gene-clock independently fixes feature **order/identity**
[V]; what scan-fitting does *not* establish is that any DNA-or-systemic quantity realized the
coordinates.

> This is a **label/interpretation correction only**. The demo's code and every number are unchanged
> (`grow_to_target.py` byte-identical; `LEDGER_gene_clock.md` convergence rows re-graded
> `[V] fit-to-scan · [O] as realized emergence` with numbers verbatim).

---

## 6. Verification & integrity (single entry: `verify_all.py`)

The three emergence gates are wired into the appendix verification lane add-only:

- **[1] / [1b] gate suite** — 12 morpho gates (`OVERALL: PASS 5/5` each) + **3 emergence gates**
  (`emergence_v2/verify_emergence{,_organs,_trajectory}.py`, native `OVERALL: 7/7 · 6/6 · 7/7 →
  PASS`). Emergence gates are location-independent (load engine + `param_db.json` via `__file__`).
- **[2] source integrity** — sha256 pin over every `code/**/*.py` and measured-input `*.json`;
  **80 files pinned** (was 69; +8 `emergence_v2` + 3 `analyses`), **drift 0**.
- **[3] morpho fidelity** — regenerated `results/*_verify.json` vs frozen `repro/morpho/expected/`,
  leaf-for-leaf, drift 0 (existing baselines preserved byte-for-byte).
- **[3b] emergence fidelity** — for the JSON-less emergence gates, the cross-session pin is each
  gate's PASS count + engine result-hash, frozen in
  `repro/morpho/expected/emergence_gate_baseline.json`
  (`7/7 939ae9924a6c · 6/6 40225433a67a · 7/7 b2b34a770f5a`).

```
python3 verify_all.py            # OVERALL: PASS (18/18)
python3 verify_all.py --list     # the 80 governed/pinned files
python3 verify_all.py --freeze   # deliberate re-pin (refuses unless every gate passes)
```

Re-freezing is always a deliberate, gate-passing act (neuro-style: refuses to freeze unless every
gate passes first).

---

## 7. Honesty constraints carried forward (VP-SPEC C3 no-tuning)

1. **No invented measurements.** Absent measured inputs stay **[O]** (organ absolute mass, exact 3-D
   anatomy, absolute developmental dates).
2. **No back-fit.** The engine never reads a validation target (NON-FIT invariant, gate-checked).
3. **Model re-runs are not measured-validated shape.** Reduced-order = **[F]**; measured-validated =
   **[O]**.
4. **`grade == evidence`.** A large effect with p > 0.05 is reported **[O]** (organ allometry
   ρ=0.69, p=0.069).
5. **Add-only.** §1–§13, the locked engines, and every measured value are unchanged to the byte;
   only interpretation labels were corrected (the `grow_to_target` re-label).

> The result this fold-in demonstrates is **not** "we reproduced exact 4-D anatomy." It is that γ's
> boundary — what it does (order, identity) vs. what it cannot do (realized timing, size) — is drawn
> rigorously, and the far side is filled with **provenance-graded systemic parameters**: [L] when
> measured, [F] when model-only, [O] when absent. No number was retracted to stack the law on top of
> the null — that is the evidence the discipline held.
