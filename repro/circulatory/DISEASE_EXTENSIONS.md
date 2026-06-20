# DISEASE EXTENSIONS — Single-Mechanism Circulatory Disorders (Research Task Charter)

**paper:** `circulatory_vp_site`  ·  **code:** `cir`  ·  **status of this document:** DONE (T8–T17 implemented in v0.2.0; discriminants pass, sections emitted)

## 0. Completion status (read first)

| deliverable | state |
|---|---|
| v0.1.0 whitepaper (organ emergence + T1–T7 + oncology kernel) | **DONE** — gates green, canonical HTML emitted in `docs/` |
| T8–T17 single-mechanism disease extensions (this document) | **DONE** — v0.2.0: 10 discriminants pass, sections §10–§19 emitted, gate re-signed |

This charter shipped as the backlog for the disease program; in v0.2.0 all ten tasks are IMPLEMENTED.
Each was drop-in to the existing engine and stress battery (no new integrated model): T8–T10 on the
Windkessel, T11–T14 on the renal/osmostat loops, T15–T17 on hepatic clearance. See §10–§19 of the paper.

## 1. Scope and exclusions

IN SCOPE — disorders expressible as **one parameter knob** on a mechanism the engine already contains:
the Windkessel hemodynamics (`windkessel`), the renal Starling + tubuloglomerular-feedback + ADH/osmostat
loops (`renal_steadystate`, `osmostat`), and the well-stirred hepatic clearance (`hepatic_clearance`).
Each disease must land on a quantity the engine **already outputs** (MAP/SBP/DBP/PP/τ, GFR/P_GC/RBF,
osmolality, E/F/CL_H).

OUT OF SCOPE — anything requiring integration across systems or a sub-model the package does not own:
atherosclerosis / coronary artery disease (lipid + inflammation + plaque), heart failure as such (the heart
is a *boundary condition* here, not an internal pump model), thrombosis / embolism (coagulation cascade),
diabetes mellitus (multi-organ metabolism). These belong to sibling packages and are reached only through
cited seam variables — never re-emerged here (SSOT, CHARTER §"Physical-class boundary").

## 2. Inherited discipline (VP-SPEC, non-negotiable)

1. **Research-first.** Each task ships only after its discriminant passes inside `repro/_verify/stress_tests.py`
   and the gate is re-signed (`gates.write_research_complete()`); `tools/build_docs.py` stays locked until then.
2. **No-tuning of mechanism.** The disease is a *named setting* of an existing parameter, not a new fudge term.
   Only the dose/severity → knob scale may be calibrated, and it is graded `[CAL]`, never silent.
3. **Honest grades (C3).** Relation = `[F]`; simulation reproduces the shape/contrast = `[V]`;
   clinical band / cited anchor = `[L]`; absolute population number = `[O]` with a stated obstacle.
4. **Deterministic.** stdlib + numpy, BLAS-pinned, `2×sha256` identical, round-before-hash.
5. **Contrast, not curve-fit.** Every discriminant pairs the diseased setting against the healthy baseline
   (or against the opposite-sign disorder) so a PASS means a *mechanistic separation*, not a tuned number.

## 3. Task families

Engine hooks (already present in `repro/_engine/vp_cir_engine.py`):
`windkessel(...) -> {MAP_mmHg, SBP_mmHg, DBP_mmHg, PP_mmHg, tau_meas_s, tau_RC_s}`;
`renal_steadystate(P_a, tgf=) -> {GFR_mL_min, P_GC_mmHg, RBF_mL_min}`;
`osmostat(load, loop=) -> osmolality`;
`hepatic_clearance(Qh=, fu=, clint=, F_abs=) -> {E, F, CL_H_mL_min}`.
Resting constants: `SVR_REST=1.10`, `C_ART_REST=1.40`, `K_F=12.5`, `Q_H=1500`, `FU_PROP=0.11`,
`CLINT_PROP=40909`, `GFR_SET=125`, `OSM_SET=287`.

### Family A — Hemodynamics (`windkessel`: MAP = CO×SVR, τ = R×C)

**A1 / T8 — Arterial stiffening → isolated systolic hypertension (widened pulse pressure).** *[highest-confidence prediction]*
- Knob: arterial compliance `C_ART` ↓ (aging / arteriosclerosis).
- Predicted observables: SBP ↑, DBP ~flat or ↓, **PP ↑**, τ = R·C ↓.
- Discriminant (T8): sweep `C_ART` over a wide stiffening range at fixed CO·SVR; require (i) PP increases
  monotonically as C falls, (ii) τ shortens in lockstep with C, (iii) SBP and DBP diverge (PP/MAP rises),
  (iv) a stiff setting reaches an ISH-like point (SBP ≥ 140, DBP < 90 surrogate) while MAP moves little.
- Anchor to verify: pulse-pressure vs arterial-stiffness relation; population PP widening with age
  (Framingham-type). Grade: relation `[F]` / shape `[V]` / clinical bands `[L]` / absolute risk `[O]`.

**A2 / T9 — Essential hypertension (resistance-driven).**
- Knob: `SVR` ↑. Observable: MAP ↑ with MAP = CO×SVR preserved.
- Discriminant (T9): SVR sweep crosses a hypertension threshold (MAP surrogate of 140/90) while the Ohm
  identity holds < 1 %; contrast with a CO-driven MAP rise to show same MAP, different mechanism.
- Anchor: resistance hypertension hemodynamics. Grade `[F]` / `[V]` / `[L]`.

**A3 / T10 — Hypotension / shock subtypes (one MAP, two routes).**
- Knob: hypovolemic = CO ↓ vs distributive = SVR ↓.
- Discriminant (T10): two-path contrast — both settings drive MAP below a shock surrogate (~65 mmHg) from
  distinct knobs; verify the engine separates the routes (CO vs SVR) at equal MAP.
- Anchor: shock classification, MAP < 65 perfusion threshold. Grade `[F]` / `[V]` / `[L]`.

### Family B — Renal (`renal_steadystate` + `osmostat`)

**B1 / T11 — Diabetes insipidus (central / nephrogenic).** *[high-confidence prediction]*
- Knob: ADH-loop gain → 0 in `osmostat`.
- Predicted observable: under a water deficit, osmolality climbs (hypernatremia surrogate) and **fails to return**
  to OSM_SET; dilute-urine analogue.
- Discriminant (T11): kill loop gain, impose graded water-deficit loads; require sustained osmolality
  elevation (no setpoint recovery) and a several-fold larger residual than the intact loop (contrast).
- Anchor: DI plasma Na⁺/osmolality, inappropriately dilute urine. Grade shape `[V]` / anchor `[L]` / absolute `[O]`.

**B2 / T12 — SIADH (ADH excess, opposite sign of DI).**
- Knob: sustained ADH bias ↑ in `osmostat`.
- Discriminant (T12): force water retention; require osmolality driven and **held below** OSM_SET
  (hyponatremia / low serum osm surrogate), with the DI task as the mirror-image contrast.
- Anchor: SIADH (serum Na < 135, low plasma osm, concentrated urine). Grade `[V]` / `[L]`.

**B3 / T13 — Chronic kidney disease / GFR staging.**
- Knob: filtration coefficient `K_F` ↓ (or effective nephron number ↓).
- Discriminant (T13): scale `K_F` so GFR steps through KDIGO-like thresholds (≈ 90 / 60 / 45 / 30 / 15
  mL/min); require autoregulation still flattens GFR at each reduced level (TGF intact, lower plateau).
- Anchor: KDIGO GFR categories G1–G5. Grade relation `[F]` / staging `[V]` / cut-offs `[L]` / prevalence `[O]`.

**B4 / T14 — Autoregulation breakthrough (hypertensive nephropathy surrogate).**
- Knob: renal perfusion `P_a` pushed **beyond** the 80–180 mmHg plateau.
- Discriminant (T14): extend the T3 perfusion sweep past the plateau; require P_GC (and GFR) to rise once
  autoregulation saturates, and report the breakthrough pressure — a glomerular-barotrauma surrogate.
- Anchor: autoregulatory range limits, glomerular hypertension. Grade `[V]` / `[L]`. *(Uses the engine's
  hemodynamic and renal blocks together — same package, not external integration.)*

### Family C — Hepatic (`hepatic_clearance`: E = fu·CLint/(QH+fu·CLint), F = 1−E)

**C1 / T15 — Cirrhosis / hepatic impairment drug clearance.** *[high-confidence prediction]*
- Knob: intrinsic clearance `CLINT` ↓.
- Predicted observable: for a high-E drug, E ↓ → **F ↑** (oral over-exposure → dose reduction needed).
- Discriminant (T15): scale CLint down; require high-E (propranolol-like) F to rise by a clinically
  meaningful factor, while a low-E drug is comparatively spared (contrast); tie magnitude to a severity grade.
- Anchor: Child-Pugh-based dose adjustment; hepatic-impairment PK. Grade relation `[F]` / shape `[V]` /
  adjustment bands `[L]` / absolute exposure `[O]`.

**C2 / T16 — Portosystemic shunt / portal hypertension.**
- Knob: fraction of hepatic blood flow bypassing hepatocytes (effective `Q_H` available for extraction ↓).
- Discriminant (T16): shunt-fraction sweep; require first-pass E ↓ → F ↑, with **flow-limited (high-E) drugs
  most affected** — a direct corollary of the T5 clearance-flow-elasticity result.
- Anchor: shunt effect on first-pass metabolism (e.g. propranolol in cirrhosis). Grade `[F]` / `[V]` / `[L]`.

**C3 / T17 — Enzyme induction / inhibition (drug–drug interaction).**
- Knob: `CLINT` × factor (induction up, inhibition down).
- Discriminant (T17): CLint perturbation; require E/F shift with the correct regime signature — low-E drugs
  flow-insensitive but **CLint-sensitive** (capacity-limited), high-E drugs the opposite. Reuses the T5
  elasticity discriminant under a perturbed CLint.
- Anchor: typical DDI fold-changes. Grade `[F]` / `[V]` / `[L]`.

## 4. Execution protocol (per task)

1. **Verify the anchor** with a literature search; record the cited band and source (PMID/DOI) — no invented numbers.
2. **Add the discriminant** `tN_<name>()` to `repro/_verify/stress_tests.py` following the T1–T7 shape
   (wide sweep + healthy/opposite contrast; `_suite(...)` return with value, grade, obstacle-if-open).
3. **Add any disease setting** as a *named parameter call* on the existing engine functions — do not add a new
   mechanism. If a severity→knob scale is needed, expose it as a `[CAL]` constant and log it in the ledger.
4. **Re-gate:** run `repro/run_all.py`; confirm `all_green`; `gates.write_research_complete()`.
5. **Extend the paper:** add the section to `tools/build_docs.py` (`build_sections`) — answer-first 40–60 words,
   one `vp-card` per cited locked quantity, grades in the claim-strip — and rebuild `docs/`.
6. **Log [O] items** (absolute incidence/prevalence) in `IRREPRODUCIBILITY_LEDGER.md` with the obstacle.

## 5. Priority (highest predictive payoff first)

1. **A1 / T8** arterial stiffening → pulse-pressure widening — lands directly on PP and τ the engine already prints.
2. **B1 / T11 + B2 / T12** DI ↔ SIADH — clean mirror-image sodium/osmolality disorders on the ADH loop.
3. **C1 / T15** hepatic impairment → F rise — the clinical liver-disease dose rule is literally F = 1 − E.
4. B3/T13 CKD staging, C2/T16 shunt, A2/T9 hypertension, then A3/T10, B4/T14, C3/T17.

## 6. Status ledger

| ID | disease | family | engine knob | observable | grade plan | status |
|---|---|---|---|---|---|---|
| T8  | isolated systolic HTN (arterial stiffening) | hemodynamic | C_ART ↓ | PP↑, τ↓ | [F]/[V]/[L]/[O] | DONE |
| T9  | essential hypertension | hemodynamic | SVR ↑ | MAP↑ | [F]/[V]/[L] | DONE |
| T10 | hypotension / shock subtypes | hemodynamic | CO↓ \| SVR↓ | MAP↓ | [F]/[V]/[L] | DONE |
| T11 | diabetes insipidus | renal/osmo | ADH gain→0 | osm↑, no recovery | [V]/[L]/[O] | DONE |
| T12 | SIADH | renal/osmo | ADH bias↑ | osm↓ | [V]/[L] | DONE |
| T13 | chronic kidney disease (GFR staging) | renal | K_F ↓ | GFR steps | [F]/[V]/[L]/[O] | DONE |
| T14 | autoregulation breakthrough | renal+hemo | P_a > plateau | P_GC↑ | [V]/[L] | DONE |
| T15 | cirrhosis / hepatic impairment PK | hepatic | CLINT ↓ | F↑ | [F]/[V]/[L]/[O] | DONE |
| T16 | portosystemic shunt | hepatic | Q_H bypass | E↓, F↑ | [F]/[V]/[L] | DONE |
| T17 | enzyme induction/inhibition (DDI) | hepatic | CLINT × | E/F shift | [F]/[V]/[L] | DONE |

## 7. Definition of done (per task)

A task is DONE when: its discriminant passes with a healthy/opposite contrast (not a tuned single point);
the cited anchor is recorded with a source; grades are assigned with obstacles for every `[O]`; the gate is
re-signed `all_green`; and a canonical HTML section is emitted. Until all ten are DONE, this document ships
with the paper as the outstanding backlog.
