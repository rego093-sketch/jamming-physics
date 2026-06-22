# vp_frontal v2 — Session-3 Handover Note

**One bounded load this session: Chunk B — Gap-2 build (additive cortical micro-model) + ST-2.**
**Outcome: the frontal phenotype SURVIVED the stress test (non-circular, topological, sign-stable).**

> The living plan is `START_HERE_HANDOVER_v2.md` (now updated through S3). This note is the Session-3 record. The Session-1 and Session-2 records (`HANDOVER_v2_SESSION1.md`, `HANDOVER_v2_SESSION2.md`) are frozen, untouched.

---

## What was done

Built two modules in `repro/frontal/_frontal_v2/` and ran both to completion: the Gap-2 micro-model, then its stress test.

### 1. Gap-2 build — `cortical_microcircuit.py`

The hippocampus precedent applied to cortex: a frozen `Hippocampus` autoassociator behind one node of the 12-organ kernel, but with its connectivity re-organized into a **hub topology**.

- **Construction (all grounded, `new_tuned_constants = 0`):** `N_HUBS = K = 7` (the emerged WM capacity) long-range hubs carry **all** long-range edges; non-hubs wire only locally within radius `r = N/(2K) = 9`; the hub-mediated recurrent settle **is** the reentrant loop. Grounded constants: FOXG1 γ 1.4737, emerged K = 7, `barrier(FOXG1) = 0.542948`. Engine READ-ONLY.
- **Non-circular read-outs:** `far_binding` cues a *near* block and measures recovery of a *distant* block (never the perturbed edge); the control is a mass-matched **random-local** cut.
- **Found:** hub-edge cut collapses distant binding (0.857 → 0.724); the mass-matched random-local cut spares it (→ 0.850); the hub−random gap is monotone and sign-stable (0 → **+0.126**). On an **all-to-all** substrate the gap is ≈ 0 (0.0019) → the effect is **topological**, not generic. A **scattered** (non-local) cue gives only a weak gap (0.009) → the binding is **long-range-specific**.
- **Honest residual:** `LHX2 == FOXG1` to the read-out — the cell-gain gene `g` never enters the sign() dynamics, so the phenotype is purely **topological / gene-blind**.
- **Grade:** `[V]` topological hub-dependence of long-range binding; `[O]` absolute magnitudes & gene-specificity. Internal digest `417a8319…`.

### 2. ST-2 — `cortical_microcircuit_st2.py`

Imports the **exact** build model (non-circular at the code level — the stress test attacks the real model, not a re-implementation). Asserts the M9 anchor bit-for-bit; `new_tuned_constants = 0`.

- **Sweep:** 3 seed cohorts (C1 19–22, C2 23–26, C3 27–30) × durations 20/40/60 = **9 cells**.
- **Three signed, falsifiable features:** `F_noncircular` (behavioural distant bind-gap, shown against the *circular* hub-mass-drop control: hub-cut drops 0.60 vs random-cut 0.000), `F_topological` (bind-gap exceeds the all-to-all control), `F_setshift` (hub-lesion perseveration delta — establish attractor A, cue B on the near block, measure the distant block still resting on A). Believed only if **sign-stable** across all 9.

#### Honest debug record (the Stress Principle in action)

The **first** ST-2 run reported a set-shift perseveration delta of **exactly +0.0000** across all 9 cells — an apparent break. It was **not** reported as a finding. Diagnosis: the `_settle` helper reset `self.hp.W = self.W` internally, silently ignoring the lesioned `W` passed to it (`far_binding` worked because it swaps `self.W`; the set-shift path passed `W` as an argument, which `_settle` discarded → every cell settled un-lesioned → ambiguous). Fix: added an optional `W=None` parameter to `CorticalMicrocircuit._settle` (default behaviour unchanged → the **build digest stayed identical at `417a8319…`**), and passed `W` explicitly in `setshift_perseveration`. A bug-induced null is a construction fault, not a scientific break — recording it here keeps the audit trail honest.

## Result

After the fix, the phenotype SURVIVED. `phenotype_sign_stable = True`, `broke_on = []`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| non-circular (distant bind-gap, not the cut edge) | 9 | 0 | 0 | True |
| topological (gap exceeds all-to-all control) | 9 | 0 | 0 | True |
| set-shift (hub-lesion perseveration delta) | 9 | 0 | 0 | True |

Perseveration delta ranged **+0.033 → +0.172**, sign-stable across all durations. Internal digest `a3d2e409…`.

**Engine invariance (re-verified S3):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact); `engine_tree_unchanged = True`; `m0_16_subtree_unchanged = True`. The additive discipline held — the frozen kernel is byte-unchanged.

## Grade & honest residual

- **Gap-2 → `[L]` in-silico** (the phenotype survives stress). The additive micro-model is **sufficient**; the kernel fork ("resolve cortex inside the kernel" — which breaks M9) is **not** triggered; M9 stays bit-identical.
- **`[O]` carried forward:** the effect is **gene-blind** — `g` is absent from the sign() dynamics, so absolute magnitudes and gene-specificity are not shown.
- **Anti-tuning note:** the set-shift delta is **duration-invariant** because the autoassociator settles fast — so the sweep confirms **no flip** (the anti-tuning guard), not duration-dependence. A sign-stable-across-the-sweep result is exactly what "believed" requires here.
- Firewall held: `consciousness_claim = 0`, `hard_problem_open = 1`. Function modeled; experience not. This is an in-silico model stress-test result — **not** validated neuroscience and not clinical guidance.

## Artifacts (in `repro/frontal/_frontal_v2/`)

- `cortical_microcircuit.py` — the Gap-2 build (deterministic → cells are call-invariant).
- `cortical_microcircuit_results.json` — internal digest `417a8319…`, matches `expected_cortical_microcircuit_sha256.json`.
- `cortical_microcircuit_st2.py` — the ST-2 stress test (imports the exact build model).
- `cortical_microcircuit_st2_results.json` — internal digest `a3d2e409…`, matches `expected_cortical_microcircuit_st2_sha256.json`.
- `cortical_microcircuit_st2.png` — 2-panel: binding gap vs cut-fraction per cohort + perseveration delta vs duration, verdict in suptitle.

## Next session — Chunk C (per Section 5 of the whitepaper)

ST-2 did **not** break, so the plan proceeds (no restart owed).

**Chunk C = Gap-3:** the full grounded connectome (cited tractography — Klein 2010; *J Neurosci* 43:7780, 2023; Öngür & Price 1998; Radley 2006) + **O×W orthogonality (ST-3)**: perturb `W` alone (sociality read-out falls, capacity preserved?) and `O` alone (reverse?). *Break for ST-3:* the axes are not separable (one factor, not two). *If broken:* the autism/ID double dissociation collapses to a single factor and the clinical mapping is rewritten. ~2 sessions (build, then stress).

*Apply the Stress Principle — build it, then break it before trusting it.*
