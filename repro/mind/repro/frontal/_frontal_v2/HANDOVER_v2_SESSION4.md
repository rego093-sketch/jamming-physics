# vp_frontal v2 — Session-4 Handover Note

**One bounded load this session: Chunk C — Gap-3 build (full grounded connectome + O×W orthogonality) + ST-3.**
**Outcome: the O×W double dissociation SURVIVED the stress test (sign-stable crossover, two separable axes).**

> The living plan is `START_HERE_HANDOVER_v2.md` (now updated through S4). This note is the Session-4 record. The Session-1, Session-2, and Session-3 records (`HANDOVER_v2_SESSION{1,2,3}.md`) are frozen, untouched.

---

## What was done

Built two modules in `repro/frontal/_frontal_v2/` and ran both to completion: the Gap-3 grounded-connectome + O×W build, then its stress test.

### 1. Gap-3 build — `cortico_connectome_owt.py`

Two parts on the **surviving Gap-2 micro-model** (the autoassociator behind one node of the 12-organ kernel, in its hub topology). Engine READ-ONLY; `new_tuned_constants = 0`.

**Part A — grounded long-range connectome.** Ten cited cortical long-range edges, each carrying an explicit grade so the audit trail separates what is *cited* from what is *ordered* from what is *guessed*:
- `cortex ↔ thalamus`, weight 1.00 — `[L cited]` (Klein 2010 *NeuroImage* 51:555; *J Neurosci* 43:7780, 2023 — the heavy reciprocal MD–PFC leucotomy tract).
- `cortex ↔ hypothalamus`, light — `[L cited]` (Öngür & Price 1998; Radley 2006).
- the remaining edges (corticostriatal, cortico-hippocampal, etc.) — `[L ordering; O magnitude]` (textbook ordering of relative tract weight; absolute magnitudes stay `[O]`).
- An **organ-scale integration check** was run on the 12-organ kernel with these grounded weights and recorded as an **honest negative** (see Honest residual below).

**Part B — O×W on the micro-model.** `class OWTCortex` parameterizes the Gap-2 model to free the cell count `N` while **holding `K = 7` hubs fixed** (the emerged WM capacity). Two orthogonal faults, two non-circular read-outs:
- **W-axis (routing)** = the hub-borne long-range edges. *W-fault* = cut them (`f_W` up to 0.9, `N` fixed at 120). Read-out **sociality** = `far_binding` (cue a *near* block, recover a *distant* block — never the cut edge).
- **O-axis (capacity)** = cell count `N` (Hopfield capacity ≈ 0.14 N), **wiring backbone intact** ("fewer neurons, white matter preserved"). *O-fault* = reduce `N` (120 → 44). Read-out **capacity** = scattered partial-cue completion (`retrieve`), which loads on cell count, W-light.
- **Sweep axes (not tuned constants):** `f_W_grid = (0.0, 0.3, 0.6, 0.9)`, `N_grid = (120, 90, 64, 44)`, `margin = 0.02`.

**Found (the honest form of a double dissociation — a relative-selectivity CROSSOVER):**
- W-fault (`f_W = 0.9`): ΔS = −0.196, ΔC = −0.067 → **W_sel = ΔC − ΔS = +0.128** (sociality-selective: routing loss hits distant binding ~3× harder than completion).
- O-fault (`N = 44`): ΔS = −0.028, ΔC = −0.060 → **O_sel = ΔS − ΔC = +0.032** (capacity-selective: cell loss hits completion harder; tracts intact sometimes *help* sociality).
- **Reuse-equivalence (non-circular at the code level):** `OWTCortex` at `N = 120` reproduces the Gap-2 `far_binding` value **exactly** (< 1e-12) — the O×W harness is the *same* surviving model, re-parameterized, not a re-implementation.
- **Non-circular control:** hub-cut sociality 0.665 vs mass-matched random-local-cut 0.872 → the deficit is **long-range-specific**, not generic mass.
- **Grade:** `[L]` grounded connectome ordering (2 edges paper-cited, rest textbook ordering, magnitudes `[O]`); `[V candidate]` the O×W crossover at micro-model scale (sign-stability then pending ST-3); `[O]` absolute magnitudes, gene-specificity, organ-scale single-tract integration. Internal digest `8d3f3e00…`.

### 2. ST-3 — `cortico_connectome_owt_st3.py`

Imports the **exact** build model (`OWTCortex._cond` etc. — the stress test attacks the real model). Asserts the M9 anchor bit-for-bit; `new_tuned_constants = 0`.

- **Sweep:** 3 seed cohorts (C1 19–22, C2 23–26, C3 27–30) × settle depths 20/40/60 = **9 cells**.
- **Three signed, falsifiable features:** `F_W_targets_sociality` (W_sel > margin), `F_O_targets_capacity` (O_sel > margin), `F_double_dissociation` (both positive ⇒ crossover / two factors; scored −1 if either axis crosses the wrong way ⇒ a single factor). Believed only if **sign-stable** across all 9.

## Result

The dissociation SURVIVED. `dissociation_sign_stable = True`, `broke_on = []`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| W targets sociality (W_sel > margin) | 9 | 0 | 0 | True |
| O targets capacity (O_sel > margin) | 9 | 0 | 0 | True |
| double dissociation (crossover, both axes) | 9 | 0 | 0 | True |

W_sel ranged **+0.112 → +0.128** and O_sel ranged **+0.032 → +0.094** across the cohort × settle-depth grid — both strictly positive on every cell, so the crossover never flips. Internal digest `0b3a80ae…`.

**Engine invariance (re-verified S4):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact). The additive discipline held — the frozen kernel is byte-unchanged.

## Grade & honest residual

- **Gap-3 → `[L]` in-silico** (the O×W crossover survives stress). The autism(W) / ID(O) mapping stands as **two separable axes, not one factor** — but as an *in-silico phase / autoassociator* result, held at arm's length from any clinical measure.
- **`[O]` carried forward — the dissociation is RELATIVE, not absolute.** It is a *crossover*: each fault has a small off-target effect (W nicks capacity ~0.06; O perturbs sociality ≤ 0.03) but hits its target ~2–3× harder. These are not clean single-task lesions.
- **`[O]` gene-blind.** `g` is absent from the sign() dynamics, so the W-axis is purely **topological** and the O-axis purely **cell-count**; gene-specificity is not shown.
- **Honest negative (micro-model property).** At the coarse 12-organ phase scale, severing the grounded heavy tracts gives **no** sign-stable global-integration deficit (the organ order flips across κ — the global field is dominated by the frozen ephaptic kernel). This is exactly *why* O×W is a **micro-model** property and not an organ-scale one — recorded rather than hidden.
- **Anti-tuning note:** the crossover is **settle-depth-invariant** (identical across 20/40/60) because the autoassociator settles fast — so the sweep confirms **no flip** (the anti-tuning guard), which is what "believed" requires here.
- Firewall held: `consciousness_claim = 0`, `hard_problem_open = 1`. Function modeled; experience not. This is an in-silico model stress-test result — **not** validated neuroscience and not clinical guidance.

## Artifacts (in `repro/frontal/_frontal_v2/`)

- `cortico_connectome_owt.py` — the Gap-3 build (grounded connectome + O×W; deterministic → cells are call-invariant).
- `cortico_connectome_owt_results.json` — internal digest `8d3f3e00…`, matches `expected_cortico_connectome_owt_sha256.json`.
- `cortico_connectome_owt_st3.py` — the ST-3 stress test (imports the exact build model).
- `cortico_connectome_owt_st3_results.json` — internal digest `0b3a80ae…`, matches `expected_cortico_connectome_owt_st3_sha256.json`.
- `cortico_connectome_owt_st3.png` — 2-panel: W_sel and O_sel per cohort across settle depth + the crossover verdict in the suptitle.

## Next session — Chunk D (per Section 5 of the whitepaper)

ST-3 did **not** break, so the plan proceeds (no restart owed).

**Chunk D = Gap-4:** the **PCI clinical match (ST-4)** — drive the frozen kernel through an emerged sleep architecture (`emerge_sleep_architecture`) and test whether the perturbational-complexity ordering (wake > REM > NREM) emerges *without tuning*. *Break for ST-4:* the complexity ordering does not separate the states, or separates them only by a tuned constant. *If broken:* the consciousness-correlate mapping is not reproduced and the claim is withdrawn. ~2 sessions (build, then stress).

*Apply the Stress Principle — build it, then break it before trusting it.*
