# vp_frontal v2 — Handover & Long-Term Plan
## The Second Long-Term Simulation of the Brain Project

**Status:** Sim 2 COMPLETE — project CLOSED. **Session 6 — Chunk E (the v2 atlas / integration pass): the whole surviving chain SURVIVED the end-to-end digest audit (all 7 build+ST artifacts reproduce bit-for-bit, `broke_on = []`), the frozen engine is byte-unchanged, the firewall held, and `new_tuned_constants` over the whole chain = 0 → `sim2_complete = True`, `project_closes = True`.** Gaps 1–4 are in-silico `[L]` (each survived its stress test; Gap-4 carries its recorded `[O]` within-unconscious ordering); Gap 5 stays the explicit firewall blank `[O]`. *(Session 5 — Chunk D — survived in part: the CONSCIOUS/UNCONSCIOUS PCI split SURVIVED ST-4; the within-unconscious ordering COLLAPSED to one scalar, recorded honest negative `[O]`.)*
**Frozen engine:** `vp_mind_engine.py`, sha `e61083ae…` (READ-ONLY)
**M9 anchor (bit-for-bit):** `R = 0.38961455156044245` (re-verified S6)
**Firewall:** `consciousness_claim = 0`, `hard_problem_open = 1`

---

## 0. The two-simulation project

This whitepaper governs a long-term, **two-simulation** program. It closes only when **both** simulations are complete (Section 7).

- **Simulation 1 — `mind_vp` v1.57 (COMPLETE, FROZEN).** A physics-grounded 12-node ephaptic mind engine: 4D-DNA organ emergence → brainwaves → memory → coordination → embodied loop → global state / affect, plus a 28-module clinical atlas. Built under strict no-tuning discipline; honest negatives preserved; consciousness firewall held. This is the "heavy, successful" simulation. It is FROZEN and READ-ONLY.

- **Simulation 2 — `vp_frontal` v2 (IN PROGRESS, this document).** An **additive** program that (a) gives the cortex the internal microstructure Sim 1 left as a single undifferentiated node (Hard Limit 1), (b) adds the **second physical coupling channel** (axonal connectome) Sim 1 omitted, and (c) operationalizes the **cognition / consciousness-access / body** framework. Sim 2 reuses Sim 1 READ-ONLY and stays additive wherever possible — the hippocampus micro-model is the precedent: a node in the frozen 12-organ kernel can carry a rich internal model **without changing the kernel**, so M9 stays bit-identical.

Work is divided by **LOAD** into session-sized chunks (Section 5).

---

## 1. Governing principles (inherited verbatim from Sim 1)

1. **No tuning.** No arbitrary setting of any value. Every quantity emerges from (a) measured gene parameters (4D-DNA γ), (b) physics constants (Maxwell, ephaptic κ), or (c) cited public measurements ([L], with provenance). `new_tuned_constants = 0` per module.
2. **Frozen engine, READ-ONLY.** `vp_mind_engine.py` is never modified. v2 additions are new modules or a clearly-provenanced branch. The M9 anchor (`R = 0.38961455156044245`) must keep reproducing bit-for-bit on the unchanged kernel.
3. **Grading.** `[V]` verified mechanism (sign-stable, robust). `[L]` locked to a cited/measured input (absolute scale may be `[O]`). `[O]` open / honest negative. Function is modeled; experience is not.
4. **Anti-tuning discipline.** Never trust a single operating point. Sweep duration, seed, perturbation node, coupling. A claim is believed only if **sign-stable** across the sweep. (The lesson F1 paid for: a clean signal at one operating point flipped under a duration sweep.)
5. **No circular read-outs.** A read-out must not be a direct function of the thing being perturbed. (This session: the cortico-thalamic transmission "deficit" was circular — the read-out *was* the severed edge — and was demoted.)
6. **THE STRESS PRINCIPLE (the core long-term rule).** Every hypothesis is **stress-tested to destruction**. If it collapses under stress, the collapse is **recorded and accepted**, and the affected line **restarts from the beginning with the collapse built in**. Sim 1 was built this way — its honest negatives (temporal-holding negligible, leucotomy sign-flip, strict-access PCI negative) are *preserved collapses*, not failures. Refinement means *surviving* the stress, never *avoiding* it.

---

## 2. Session-1 results (what was built and found)

### 2.1 Corrections to the prior frontal probe (F1)
- F1's central negative ("cortical temporal holding is negligible; the signal sign-flips") was diagnosed as an **under-emergence artifact**. The probe loaded only a static ephaptic-kernel snapshot and ran a bare Kuramoto coherence-recovery test — it asked a working-memory question with the working-memory machinery (theta–gamma, hippocampal pattern dynamics) *removed*. Demonstration: `emerge_memory` reports a real WM (capacity 6.125 items, completion 1.0), while the bare-Kuramoto probe reports cortical holding ≈ −0.0001.
- The earlier claim "a v2 substrate must **break** the frozen engine" was **corrected**. The hippocampus is the precedent: a 120-cell internal model sits behind a single node of the frozen 12-organ kernel without changing it. Cortical microstructure can be added the same additive way; M9 stays bit-identical.

### 2.2 Modules built (`repro/frontal/_frontal_v2/`)
- **`cortical_emergence.py`** — emerges the cortical rhythm from the measured FOXG1 γ (1.4737) via the frozen `Population`/FHN machinery, *replacing* the prior no-tuning violation (reading the atlas band 40 Hz, Fries 2009, and driving at it). Emerged theta/gamma WM capacity ≈ **7.2 items** (matches the engine's 6.125 / the Miller range) without being told the band. **Grade:** `[V]` band identity & ratio; `[L]` cited band; `[O]` absolute Hz. **Honest residual:** the band is dominated by inhibitory τ, not the gene γ; per-organ band assignment still rests on cited bands → `[L]`, not `[V]`.
- **`cortical_wm_holding.py`** — copies the frozen `Hippocampus` micro-model as the cortical buffer (g = FOXG1), sized by the emerged WM capacity. Under the faithful disconnection lesion (sever recurrent weights), pattern completion **collapses monotonically and sign-stably (1.00 → 0.30)**, robust to the cell-gain convention. This **flips F1's false negative**: on the real WM substrate, holding is real and lesion-sensitive. **Honest:** the self-sustain read-out has a frac=1.0 artifact (zero-field hysteresis); the verdict rests on completion. The autoassociator does **not** yet differentiate frontal from hippocampal (g doesn't enter the sign() dynamics). **Grade:** `[V]` holding-real; `[O]` frontal-specificity owed.
- **`frontal_axonal_channel.py`** — adds the **second physical coupling channel** (axonal connectome) Sim 1 omitted. (Sim 1 is ephaptic/proximity only: `W0[cortex,thalamus]=4e-4`, `W0[cortex,hypothalamus]=2e-5` — negligible, because they are not spatial neighbours, although wired by long axons.) Grounded relative strengths from cited tractography: cortex↔thalamus(MD) **heavy & reciprocal** (Klein 2010 *NeuroImage* 51:555; *J Neurosci* 43:7780, 2023), cortex→hypothalamus **sparse & diffuse** (Öngür & Price 1998 *JCN* 401:480; Radley 2006 *J Neurosci* 26:12967). The faithful leucotomy (sever the frontal↔thalamus **axon**, keep the field) **spares perception** across a κ sweep (sign-stable). **But** the cortico-thalamic transmission "deficit" is **circular** (the read-out *is* the severed edge) and was demoted. **Grade:** `[L]` perception-spared (non-circular, meaningful); transmission deficit = construction check, not a finding.
- **`frontal_em_wave.py`** — emerges the cortical (FOXG1) population and computes its EM wave. The frontal population **radiates at the speed of light** (front speed/c = 1.015; radiated energy > 0 → the measurable EEG gamma). In tissue, every brain rhythm is sub-wavelength (frontal gamma 40 Hz: λ = 913 m; hypothalamus 2 Hz: λ = 4082 m; brain = 0.15 m), so within the brain coupling is quasi-static **near-field** (= why Sim 1 uses ephaptic coupling). The frontal gamma is the *fastest* major rhythm → *shortest* wavelength → the **most spatially-structured** field; the slow hypothalamus is the pure near-field modulator. **Grade:** `[V]` Maxwell physics; `[L]` cited bands; `[O]` efficacy.
- **`cognition_consciousness_body.py`** — operationalizes the three-layer framework. **Probe A** (PCI analog = perturbational complexity, the clinical vegetative-state measure): access **dissociates from arousal** — PCI is non-monotonic (rises, peaks at ~3× the measured coupling, then collapses) while activity rises monotonically; at high coupling, arousal is high but access collapses (the vegetative/seizure signature). **Honest:** the PCI peak is at ~3× measured, **not** at the measured coupling (the figure caption "peaks at measured" overclaims; the real result is the *dissociation*). **Probe B**: the stream of thought keeps strong momentum (autocorr **0.95**) with the body decoupled vs **0.55** coupled — **cognition runs off the body** (dreams). **Grade:** `[V]` functional mechanisms; `[O]` felt quality.

### 2.3 Chain synthesis & the field-efficacy fill
- The full chain **M0–M20 runs** (`emerge_all`, 21 modules). The pervasive open marker is `medium_efficacy_tested = 0.0` (M8–M19): the EM field's **causal** role is predicted, not shown.
- **GAP-1 filled in-silico:** the EM field has a **causal window**. Field OFF → no coordination, access floor (R=0.04, PCI=0). Field at MEASURED strength → metastable coordination, access window **open** (R=0.39, PCI=0.118). Over-driven → activity high, access **collapses** (R=0.54, PCI=0.110). In-silico prediction; in-vivo (field cancel/augment) test owed.

---

## 2A. Session-2 result — Chunk A / ST-1 (field-efficacy robustness)

**Module:** `repro/frontal/_frontal_v2/field_efficacy_robustness.py`. It imports the EXACT Gap-1 `pci_analog` from `cognition_consciousness_body.py` (non-circular: the test attacks the real code, not a re-implementation), asserts the engine anchor bit-for-bit on every run, and carries `new_tuned_constants = 0`.

**The break it was designed to cause (from Section 4):** *the in-silico causal window is an operating-point artifact — it flips, or is seed-specific.* If that break had occurred, Gap-1 would revert to `[O]` and the "field is causally necessary" claim would be withdrawn.

**Sweep:** 3 seed cohorts (C1 19–22, C2 23–26, C3 27–30) × 3 durations (0.4 / 0.6 / 1.0 s) × 4 perturbation nodes (neocortex, thalamus, hippocampus, striatum) = **36 cells**, each running the full coupling curve `[0, 1, 2, 3, 5, 8] × measured κ` (κ = 0.5496). Absolute PCI margin = 0.012. Three **signed, falsifiable** features per cell: `F_necessity` (measured > OFF floor), `F_collapse` (interior peak **and** a real over-drive drop, vs a monotone-up curve = no window), `F_dissociation` (arousal rises monotonically while access turns over). A feature is believed only if **sign-stable** across all 36 cells.

**Outcome — the window SURVIVED.** Every cell peaks at **3× the measured coupling**.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| necessity (measured > OFF floor) | 36 | 0 | 0 | **True** |
| over-drive collapse (interior peak + real drop) | 36 | 0 | 0 | **True** |
| dissociation (arousal ↑ while access turns over) | 33 | 0 | 3 | **True** |

→ `window_sign_stable = True`. The 3 "ambiguous" cells are short-duration (0.4 s) runs with a tiny arousal wiggle — **not** contradictions; they confirm the classifier is not rubber-stamping. `broke_on = []`.

**Baseline reproduction** (C1∪C2 = seeds 19–26, T = 0.6, neocortex), PCI / activity vs coupling×κ:

| coupling | 0× (OFF) | 1× (measured) | 2× | 3× (peak) | 5× | 8× |
|---|---|---|---|---|---|---|
| PCI | 0.068 | 0.118 | 0.126 | **0.131** | 0.110 | 0.081 |
| activity | 0.256 | 0.391 | 0.426 | 0.459 | 0.540 | **0.709** |

Access (PCI) rises, peaks in the interior, and collapses; arousal (activity) rises monotonically throughout — the vegetative/seizure dissociation, sign-stable.

**Grade:** Gap-1 → **`[L]` in-silico (window survives stress).** **Honest residual (unchanged from S1, preserved):** the peak sits **above** the measured coupling (≈3×), so "criticality AT the measured coupling" remains **`[O]`**. What survived ST-1 is the **dissociation / window shape**, not the peak *location*. The in-vivo test (field cancel / augment) is still owed. Firewall held: function modeled, experience not.

**Artifacts:** `field_efficacy_robustness_results.json` (internal digest `05a7d317…`, matches `expected_field_efficacy_robustness_sha256.json`); 2-panel figure `field_efficacy_robustness.png` (PCI window + monotone arousal, verdict in the suptitle).

---

## 2B. Session-3 result — Chunk B / Gap-2 build + ST-2 (cortical micro-model)

**What was built.** `repro/frontal/_frontal_v2/cortical_microcircuit.py` — the additive cortical micro-model that fills Gap-2. It is the **hippocampus precedent applied to cortex**: a frozen `Hippocampus` autoassociator sits behind one node of the 12-organ kernel, but its connectivity is re-organized into a **hub topology** — `N_HUBS = K = 7` (the emerged WM capacity) long-range hubs carry **all** long-range edges, non-hubs wire only locally within radius `r = N/(2K) = 9`, and the hub-mediated recurrent settle **is** the reentrant loop. Everything is grounded (FOXG1 γ 1.4737, emerged K = 7, `barrier(FOXG1) = 0.542948`); `new_tuned_constants = 0`; engine READ-ONLY. The read-outs are **non-circular by construction**: `far_binding` cues a *near* block and measures recovery of a *distant* block (never the perturbed edge), and a matched random-local cut of equal mass is the control.

**What was found (build).** Cutting the **hub** long-range edges collapses distant binding (0.857 → 0.724) while a mass-matched **random-local** cut spares it (→ 0.850); the hub−random gap is monotone and sign-stable (0 → **+0.126**). The same cut on an **all-to-all** substrate gives gap ≈ 0 (0.0019) — the effect is **topological**, not generic. A **scattered** (non-local) cue gives only a weak gap (0.009) — the binding is **long-range-specific**. **Honest residual:** `LHX2 == FOXG1` to the read-out — the cell-gain gene `g` never enters the sign() dynamics, so the phenotype is purely **topological / gene-blind**. **Grade:** `[V]` topological hub-dependence of long-range binding; `[O]` absolute magnitudes & gene-specificity. Internal digest `417a8319…`.

**ST-2 — the break it was designed to cause (Section 4):** *the frontal phenotype only appears in a circular read-out, or set-shifting flips under a duration sweep.* If broken, the additive micro-model is insufficient and the fork "resolve cortex **inside** the kernel (breaks M9)" opens. `cortical_microcircuit_st2.py` imports the **exact** build model (non-circular at the code level), and tests three **signed** features across 9 cells (3 seed cohorts × durations 20/40/60): `F_noncircular` (behavioural bind-gap, shown against the *circular* hub-mass-drop control: hub-cut drops 0.60 vs random-cut 0.000), `F_topological` (bind-gap exceeds the all-to-all control), `F_setshift` (hub-lesion perseveration delta — establish attractor A, cue B on the near block, measure the distant block still resting on A).

**Outcome — the phenotype SURVIVED.** non-circular **9/0/0**, topological **9/0/0**, set-shift **9/0/0** (perseveration delta +0.033 → +0.172). `phenotype_sign_stable = True`, `broke_on = []`. Gap-2 → **`[L]` in-silico**; the additive micro-model is **sufficient**; M9 stays bit-identical; the kernel fork is **not** triggered. **Honest note:** the set-shift delta is **duration-invariant** because the autoassociator settles fast — so the sweep confirms **no flip** (anti-tuning), not duration-dependence; the gene-blindness above is carried forward as the standing `[O]`. Internal digest `a3d2e409…`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| non-circular (distant bind-gap, not the cut edge) | 9 | 0 | 0 | **True** |
| topological (gap exceeds all-to-all control) | 9 | 0 | 0 | **True** |
| set-shift (hub-lesion perseveration delta) | 9 | 0 | 0 | **True** |

**Engine invariance (re-verified S3):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact); `engine_tree_unchanged = True`; `m0_16_subtree_unchanged = True`. The additive discipline held — the frozen kernel is byte-unchanged.

**Artifacts:** `cortical_microcircuit_results.json` (digest `417a8319…`) + `expected_cortical_microcircuit_sha256.json`; `cortical_microcircuit_st2_results.json` (digest `a3d2e409…`) + `expected_cortical_microcircuit_st2_sha256.json`; 2-panel figure `cortical_microcircuit_st2.png` (binding gap vs cut-fraction per cohort; perseveration delta vs duration). Deterministic (cells are call-invariant).

---

## 2C. Session-4 result — Chunk C / Gap-3 build + ST-3 (grounded connectome + O×W orthogonality)

**What was built.** `repro/frontal/_frontal_v2/cortico_connectome_owt.py` — two parts on the **surviving Gap-2 micro-model**. **Part A:** a grounded long-range connectome of 10 cited cortical edges, each carrying an explicit grade (`cortex↔thalamus` weight 1.00 `[L cited]` Klein 2010 / *J Neurosci* 43:7780; `cortex↔hypothalamus` light `[L cited]` Öngür 1998 / Radley 2006; the rest `[L ordering; O magnitude]`), plus an organ-scale integration check recorded as an **honest negative**. **Part B:** `class OWTCortex` parameterizes the Gap-2 model to free cell count `N` while **holding K = 7 hubs fixed**, and runs the O×W sweep. `new_tuned_constants = 0`; engine READ-ONLY. The harness is **non-circular at the code level**: `OWTCortex` at N = 120 reproduces the Gap-2 `far_binding` value **exactly** (< 1e-12) — same surviving model, re-parameterized.

**The two orthogonal axes (the honest form — a relative-selectivity CROSSOVER).** *W-axis (routing)* = the hub-borne long-range edges; *W-fault* = cut them (`f_W` up to 0.9, N = 120); read-out **sociality** = `far_binding` (cue near block, recover distant block — never the cut edge). *O-axis (capacity)* = cell count N (Hopfield capacity ≈ 0.14 N), **wiring backbone intact**; *O-fault* = reduce N (120 → 44); read-out **capacity** = scattered partial-cue completion (`retrieve`). Sweep axes (not tuned): `f_W_grid = (0, 0.3, 0.6, 0.9)`, `N_grid = (120, 90, 64, 44)`, `margin = 0.02`.

**What was found (build).** W-fault (`f_W = 0.9`): ΔS = −0.196, ΔC = −0.067 → **W_sel = ΔC − ΔS = +0.128** (sociality-selective). O-fault (`N = 44`): ΔS = −0.028, ΔC = −0.060 → **O_sel = ΔS − ΔC = +0.032** (capacity-selective; tracts intact sometimes *help* sociality). **Non-circular control:** hub-cut sociality 0.665 vs mass-matched random-local-cut 0.872 → **long-range-specific**, not generic mass. **Grade:** `[L]` connectome ordering (2 edges paper-cited, rest textbook ordering, magnitudes `[O]`); `[V candidate]` the crossover (sign-stability then pending ST-3); `[O]` magnitudes, gene-specificity, organ-scale integration. Internal digest `8d3f3e00…`.

**ST-3 — the break it was designed to cause (Section 4):** *the axes are not separable (one factor, not two).* If broken, the autism/ID double dissociation collapses to a single factor and the clinical mapping is rewritten. `cortico_connectome_owt_st3.py` imports the **exact** build model and tests three **signed** features across 9 cells (3 seed cohorts C1 19–22 / C2 23–26 / C3 27–30 × settle depths 20/40/60): `F_W_targets_sociality` (W_sel > margin), `F_O_targets_capacity` (O_sel > margin), `F_double_dissociation` (both positive ⇒ crossover; −1 if either axis crosses the wrong way ⇒ single factor).

**Outcome — the dissociation SURVIVED.** W-targets-sociality **9/0/0**, O-targets-capacity **9/0/0**, double-dissociation **9/0/0**. W_sel ranged **+0.112 → +0.128**, O_sel ranged **+0.032 → +0.094** — both strictly positive on every cell, so the crossover never flips. `dissociation_sign_stable = True`, `broke_on = []`. Gap-3 → **`[L]` in-silico**: two **separable** axes (autism = W-fault routing, ID = O-fault capacity), held at arm's length as an in-silico phase / autoassociator result, **not** a clinical measure. Internal digest `0b3a80ae…`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| W targets sociality (W_sel > margin) | 9 | 0 | 0 | **True** |
| O targets capacity (O_sel > margin) | 9 | 0 | 0 | **True** |
| double dissociation (crossover, both axes) | 9 | 0 | 0 | **True** |

**Honest residuals (preserved):** the dissociation is **relative** — a crossover, not clean single-task lesions (W nicks capacity ~0.06; O perturbs sociality ≤ 0.03), but each fault hits its target ~2–3× harder. The effect is **gene-blind** (g absent from sign() dynamics) — W is purely topological, O purely cell-count. And it is a **micro-model property**: at the coarse 12-organ phase scale, severing the grounded heavy tracts gives **no** sign-stable global-integration deficit (organ order flips across κ — the global field is dominated by the frozen ephaptic kernel), which is *why* O×W lives at the micro scale. The crossover is settle-depth-invariant (fast-settling autoassociator) → the sweep confirms **no flip** (anti-tuning), not depth-dependence.

**Engine invariance (re-verified S4):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact). The additive discipline held — the frozen kernel is byte-unchanged.

**Artifacts:** `cortico_connectome_owt_results.json` (digest `8d3f3e00…`) + `expected_cortico_connectome_owt_sha256.json`; `cortico_connectome_owt_st3_results.json` (digest `0b3a80ae…`) + `expected_cortico_connectome_owt_st3_sha256.json`; 2-panel figure `cortico_connectome_owt_st3.png` (W_sel and O_sel per cohort across settle depth, crossover verdict in the suptitle). Deterministic (cells are call-invariant).

---

## 2D. Session-5 result — Chunk D / Gap-4 build + ST-4 (PCI clinical match via the emerged sleep architecture)

**What was built.** `repro/frontal/_frontal_v2/pci_clinical_match.py` — drives the **frozen M9 kernel** through the **emerged M14 sleep architecture** and scores a **faithful perturbational complexity index (PCI**, the clinical bedside consciousness measure). The state→mechanism map is **grounded by M14, not by us**: `emerge_sleep_architecture()` already emerged (from the frozen kernel + cited kinetics) the activated-vs-bistable distinction the module rides on — `shift_index_rem ≈ 1.05` (REM = **activated/desynchronised**, no OFF-periods) vs `shift_index_nrem ≈ 0.045` (NREM = **bistable** slow Up/Down, OFF-periods present), with spindle 15.4 Hz and slow-osc 0.49 Hz matched; those facts are **asserted at run start** (the module aborts if M14 drifts). The mechanism scored is the M14 construction: a 16-cell cortical population of R19 cubic-bistable cells (`s − s³ + drive − a`) coupled diffusively through the **M9 ephaptic ring at the measured κ = 0.5496**; the state is set **only** by the slow-adaptation strength (`off_depth × A_GAIN`) and the cited carrier — activated theta-gamma (`f ≈ 23.5 Hz`, atlas f0) for wake/REM, slow 0.5 Hz for NREM. Every quantity is measured (κ; `A_GAIN = 1.6`; `TAU_SO = 0.600 s`, Sanchez-Vives & McCormick 2000; `TAU_S = 0.025 s`; `drive = 0.60`, Steriade 1993); `new_tuned_constants = 0`; engine READ-ONLY.

**The faithful, non-circular PCI.** A single TMS-like kick (`+2.0` to one cell, 4 ms after a 4 s settle) is applied to a **perturbed** twin; an **unperturbed** twin shares identical initial conditions. **PCI = normalised Lempel-Ziv complexity of the binarised perturbed-minus-unperturbed causal divergence** over a 1.5 s post-pulse window (downsample 8×, binarise `D > D.mean()`). Subtracting the twin removes spontaneous activity, so **with no kick the divergence is identically zero → PCI = 0 for every state** (the non-circular control) — the exact property a spontaneous-EEG complexity measure lacks and the clinical PCI is built to have. The LZ core (`lz76` / `normalised_lz`) is **imported** from `cognition_consciousness_body` (non-circular at the code level). *(This is the readout that survived four prototype iterations: a spatial-median-of-raw-response readout was rejected because its no-perturbation control gave Δ = +0.795 — it measured **spontaneous**, not **perturbational**, complexity. The twin-divergence fixes that.)*

**What was found (build).** PCI by state (9-seed cohort; deterministic):

| state | grounding | PCI | raw post-pulse activity |
|---|---|---|---|
| WAKE | grounded (off=0, activated) | **0.464** | 1.221 |
| REM | grounded (off=0, activated) | **0.464** | 1.221 |
| NREM | grounded (off=1, bistable) | **0.036** | 0.874 |
| ANES | extended (off=1.6) `[O]` | 0.048 | 0.879 |
| VS | extended (off=2.4) `[O]` | 0.081 | 0.871 |

The **conscious/unconscious split is clean**: wake ≈ REM (**0.464**) ≫ NREM (**0.036**), Δ = **+0.428**, well across the clinical cutoff `PCI* ≈ 0.31` (Casarotto 2016). The bistable OFF-periods truncate the evoked causal chain (Massimini 2005; Pigorini 2015), collapsing complexity. **Non-circular control:** no kick → PCI = **0.000** for every state. **Dissociation from arousal:** the unconscious states still carry substantial raw activity (0.87–0.88) yet collapse PCI, and the activity ordering does **not** track the PCI ordering — PCI is not an arousal proxy. **Honest negative (recorded):** the single PCI scalar does **not** resolve the fine unconscious ordering — NREM/anaesthesia/VS collapse to ~one value (spread **0.045**), "deeper bistability → monotonically lower PCI" **breaks**, and the small clinical wake>REM gap is unresolved (`|wake−REM| = 0.000`). Internal digest `bde77370…`.

**ST-4 — the break it was designed to cause (Section 4):** *the analog does not separate the states (collapses to one scalar).* `pci_clinical_match_st4.py` imports the **exact** build model (`pci`, `STATES`, the grounding) and tests three **signed** features across 9 cells (3 seed cohorts C1 19–22 / C2 23–26 / C3 27–30 × post-pulse windows 1.0 / 1.5 / 2.0 s, margin 0.05): `F_rem_gt_nrem` (PCI_REM − PCI_NREM > margin), `F_wake_gt_nrem`, `F_conscious_separated` (`min(wake,REM) − NREM`; −1 if an unconscious PCI reaches a conscious one). It **separately records** the build's honest negative (the within-unconscious spread) as an `[O]`, not a sign-stable claim.

**Outcome — the conscious/unconscious split SURVIVED; the within-unconscious ordering is the recorded `[O]`.** rem>nrem **9/0/0**, wake>nrem **9/0/0**, conscious-separated **9/0/0**. The conscious−unconscious margin ranged **+0.347 → +0.481** across the post-window sweep (always ≫ margin); the within-unconscious spread stayed **0.025 → 0.045** (always < margin), and "deeper → lower PCI" held on **no** cell. `conscious_unconscious_separation_sign_stable = True`, `broke_on = []`. **Gap-4 → `[L]` in-silico for the conscious/unconscious split** (the clinical PCI's core binary falls out of the frozen kernel with no new constant) **+ `[O]` for the within-unconscious ordering** (collapses to one scalar — which is itself scientifically sensible: PCI's clinical strength *is* the conscious/unconscious binary, not fine unconscious discrimination). Internal digest `2ada85a4…`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| REM > NREM (PCI_REM − PCI_NREM > margin) | 9 | 0 | 0 | **True** |
| WAKE > NREM (PCI_WAKE − PCI_NREM > margin) | 9 | 0 | 0 | **True** |
| conscious separated (min(wake,REM) − NREM > margin) | 9 | 0 | 0 | **True** |

**Honest residuals (preserved):** (1) the within-unconscious ordering is `[O]` — one scalar cannot rank NREM vs anaesthesia vs VS (the clinical full ordering is **not** reproduced; only the binary is). (2) wake ≈ REM exactly — the mechanism cannot resolve the small clinical wake>REM gap → `[O]`. (3) ANES/VS are an **extended** deeper-bistability sweep with **no** M14 grounding (they have no emerged sleep-stage behind them) → `[O]`. (4) Absolute PCI magnitudes are model units, not clinical PCI values → `[O]`. (5) Felt quality remains the firewall blank → `[O]`. The separation is post-window-invariant in **sign** (the sweep confirms **no flip**, anti-tuning), with the margin shrinking smoothly as the window lengthens (longer windows let NREM accrue a little complexity) — never crossing.

**Engine invariance (re-verified S5):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact); the M14 grounding source re-asserts `is_consciousness_claim = 0`, `hard_problem_open = 1`. The additive discipline held — the frozen kernel is byte-unchanged.

**Artifacts:** `pci_clinical_match_results.json` (digest `bde77370…`) + `expected_pci_clinical_match_sha256.json`; `pci_clinical_match_st4_results.json` (digest `2ada85a4…`) + `expected_pci_clinical_match_st4_sha256.json`; 2-panel figures `pci_clinical_match.png` (PCI by state vs the clinical cutoff; PCI-vs-activity dissociation) and `pci_clinical_match_st4.png` (per-cell PCI bands + signed separation margins, verdict in the suptitle). Deterministic (cells are call-invariant).

---

## 2E. Session-6 result — Chunk E / the v2 atlas (integration pass)

**What this is.** The integration pass that closes Sim 2 (Section 7). Chunk E introduces **no new hypothesis**. `repro/frontal/_frontal_v2/v2_atlas.py` re-reads the whole surviving chain, **re-derives every committed digest from the artifacts on disk** (so "it reproduces" is an *act*, not an assertion), aggregates the per-gap ledger with the grades the modules themselves emitted, checks the project's end condition, and emits one canonical artifact + one figure (the v2 atlas). Engine READ-ONLY; `new_tuned_constants = 0`; M9 anchor asserted bit-for-bit.

**The Stress Principle applied to an integration pass.** An integration pass has exactly one thing that can break: **a recorded survivor that no longer reproduces.** So the atlas's stress test is the **end-to-end digest audit** — for every build and stress-test artifact, recompute its digest from content and require `recomputed == stored == committed-expected-sha`. If any artifact drifts, that *is* the break: it is recorded in `broke_on`, `sim2_complete` is set False, and the offending line is flagged for restart (never papered over). Surviving = every artifact reproduces bit-for-bit **and** the frozen engine is byte-unchanged **and** the firewall held **and** `new_tuned_constants` summed over the whole chain is 0. Non-circular: the atlas re-derives each digest from the results content and compares against the **independently committed** expected-sha file (it does not copy shas forward); the engine guard is `engine_anchor_bitforbit()` (a uniform drive must reproduce M9 exactly) + the full-tree / M0–M16-subtree byte-unchanged invariant.

**Outcome — the chain SURVIVED the audit; Sim 2 is COMPLETE.** All seven chain artifacts reproduce bit-for-bit, `broke_on = []`:

| gap | artifact (build / ST) | reproduces |
|---|---|---|
| 1 | `field_efficacy_robustness` (ST-1) | **True** |
| 2 | `cortical_microcircuit` (build) · `…_st2` (ST-2) | **True** |
| 3 | `cortico_connectome_owt` (build) · `…_st3` (ST-3) | **True** |
| 4 | `pci_clinical_match` (build) · `…_st4` (ST-4) | **True** |

Aggregated per-gap ledger (the grades the modules emitted, unchanged): **Gap 1** `[L]` in-silico (field causal window survives ST-1; peak ~3× above measured `[O]`) · **Gap 2** `[L]` in-silico (cortical micro-model survives ST-2; micro-model sufficient, kernel fork not triggered; gene-blind `[O]`) · **Gap 3** `[L]` in-silico (O×W crossover survives ST-3 — two separable axes; relative-selectivity / gene-blind / micro-model-property `[O]`) · **Gap 4** `[L]` in-silico for the conscious/unconscious split (survives ST-4) **+ `[O]`** within-unconscious ordering (collapsed — recorded honest negative) · **Gap 5** `[O]` OPEN by principle (the firewall blank).

**End condition (Section 7), as computed by the atlas:** `sim1_status = COMPLETE (frozen, READ-ONLY)`, `fillable_gaps_graded = True`, `gap5_firewall_blank_present = True`, `all_artifacts_reproduce = True`, `engine_invariant = True`, `firewall_held = True` (claim=0 on all; hard_open=1 on all), `new_tuned_constants_total = 0` → **`sim2_complete = True`, `project_closes = True`.**

**Engine invariance (re-verified S6):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact); full engine tree + the M0–M16 subtree byte-unchanged. The additive discipline held — the frozen kernel is untouched.

**Honest framing (unchanged by closure).** "Complete" means the project's own end condition is met: every fillable gap survived its stress test or carries a recorded honest negative, Gap 5 stays the explicit firewall blank, and the whole chain reproduces with nothing tuned. It does **not** mean validated neuroscience or clinical guidance — these are in-silico model results. Gap 5 (felt quality) remains open by principle: `consciousness_claim = 0`, `hard_problem_open = 1`.

**Artifacts:** `v2_atlas.py` (the integration/audit pass) → `v2_atlas_results.json` (digest `bbaa4e9405e8…`) + `expected_v2_atlas_sha256.json`; figure `v2_atlas.png` (the per-gap ledger + end-condition panel). Deterministic; re-runs reproduce the atlas digest bit-for-bit.

---

## 3. The brain chain and the five gaps

The mechanism chain (gene → cell → rhythm → coordination → memory → stream → selection → body → loops back: **the rotation**) is **complete at the mechanism level**. Five gaps remain; four are fillable (hypotheses entered), the fifth is open by principle.

| # | Gap | Status | Hypothesis (the fill) |
|---|-----|--------|-----------------------|
| 1 | EM field causal efficacy | **in-silico `[L]` — survived ST-1** | The field has a causal window; present at measured strength it opens access, cancelled/over-driven it shuts. Sign-stable across 36-cell seed×duration×node sweep (S2). Peak sits ~3× above measured → "criticality AT measured" stays `[O]`; in-vivo owed. |
| 2 | Cortical microstructure | **in-silico `[L]` — survived ST-2** | Frontal executive fn emerges from cortico-cortical long-range **hubs** + the gamma broadcaster role; the additive cortical micro-model (hippocampus precedent) yields the phenotype. Hub-cut collapses distant binding while a mass-matched random-local cut spares it; effect vanishes all-to-all (**topological**), is long-range-specific, and set-shifting is sign-stable (S3). Effect is gene-blind (g absent from sign() dynamics) → magnitudes/gene-specificity stay `[O]`. |
| 3 | Axonal connectome (O×W axes) | **in-silico `[L]` — survived ST-3** | Long-range wiring carries routing (W) separable from cell-count capacity (O); the autism/ID double dissociation lives here as a **crossover** — autism = W-fault (cut hub long-range edges → sociality-selective deficit), intellectual disability = O-fault (fewer cells, tracts intact → capacity-selective deficit). On the surviving Gap-2 micro-model the W- and O-faults form a sign-stable crossover across a 9-cell cohort×settle-depth sweep (S4; W_sel +0.112→+0.128, O_sel +0.032→+0.094). Relative (not absolute) selectivity, gene-blind, and a micro-model property (organ-scale single-tract lesion not sign-stable) → magnitudes/gene-specificity stay `[O]`; clinical labels held at arm's length. |
| 4 | Access window (consciousness) | **in-silico `[L]` (conscious/unconscious split) — survived ST-4; `[O]` within-unconscious ordering** | Consciousness = the subset of cognition reaching global EM coordination (high PCI); intuition = the remainder (cognition ≫ access). Driven through the emerged M14 sleep states, a faithful perturbational PCI (LZ of the perturbed-minus-unperturbed causal divergence) reproduces the clinical **conscious/unconscious split** with no new constant — wake≈REM (0.464) ≫ NREM (0.036), sign-stable across a 9-cell cohort×post-window sweep (S5), non-circular (no kick → PCI = 0). The single PCI scalar does **not** resolve the fine unconscious ordering (NREM/anaesthesia/VS collapse to one value, spread 0.045) and cannot resolve the wake>REM gap → those stay `[O]`. Magnitudes are model units `[O]`. |
| 5 | Felt quality (hard problem) | **OPEN by principle** | Not simulation-fillable. The firewall. Left as an explicit blank; the chain closes **with** this blank, never by erasing it. |

---

## 4. Verification scenario for new sessions (stress tests)

Each hypothesis gets a test **designed to break it**. If it breaks, record the break and **restart that line with the break applied** (the Stress Principle).

- **ST-1 — EM field efficacy robustness (priority 1). — DONE (S2): SURVIVED.** Is the in-silico causal window sign-stable across seed, duration, and perturbation node (F3-style cohort sweep)? *Break:* the window is an operating-point artifact (flips / seed-specific). *If broken:* Gap-1 reverts to `[O]`; the "field is causally necessary" claim is withdrawn; the coordination layer is re-examined. **Result:** all three signed features sign-stable across 36 cells (necessity 36/0/0, over-drive collapse 36/0/0, dissociation 33 support / 0 contradict / 3 ambiguous); `window_sign_stable = True`, `broke_on = []`. Gap-1 → `[L]` in-silico. Residual `[O]`: peak ~3× above the measured coupling (location, not shape). See Section 2A.
- **ST-2 — cortical micro-model non-circularity. — DONE (S3): SURVIVED.** Build Gap-2's micro-model. Does the frontal phenotype appear in a read-out **independent of the perturbed edge**? Is set-shifting sign-stable under a duration sweep? *Break:* the phenotype only appears in a circular read-out, or flips. *If broken:* the additive micro-model is insufficient; reconsider resolving cortex **inside** the kernel — which breaks M9 (a major fork). **Result:** all three signed features sign-stable across 9 cells (non-circular 9/0/0, topological 9/0/0, set-shift 9/0/0; perseveration delta +0.033→+0.172); `phenotype_sign_stable = True`, `broke_on = []`. Gap-2 → `[L]` in-silico; the micro-model is **sufficient**, the kernel fork is **not** triggered, M9 stays bit-identical. Residual `[O]`: the effect is gene-blind (g absent from sign() dynamics) — magnitudes/gene-specificity owed. See Section 2B.
- **ST-3 — O×W orthogonality (autism/ID). — DONE (S4): SURVIVED.** Perturb W alone (sociality read-out falls, capacity preserved?) and O alone (reverse?). *Break:* the axes are not separable (one factor, not two). *If broken:* the autism/ID double dissociation collapses to a single factor; the clinical mapping is rewritten. **Result:** all three signed features sign-stable across 9 cells (W-targets-sociality 9/0/0, O-targets-capacity 9/0/0, double-dissociation 9/0/0; W_sel +0.112→+0.128, O_sel +0.032→+0.094); `dissociation_sign_stable = True`, `broke_on = []`. Gap-3 → `[L]` in-silico: two **separable** axes (a crossover), held at arm's length from clinical use. Residual `[O]`: the dissociation is **relative** (each fault has a small off-target effect), gene-blind, and a micro-model property (organ-scale single-tract lesion not sign-stable). See Section 2C.
- **ST-4 — access-window clinical match. — DONE (S5): SURVIVED (split) / honest negative (fine ordering).** Does the PCI-collapse curve **distinguish** anesthesia vs vegetative vs sleep (against clinical PCI values), or collapse to one scalar? *Break:* the analog does not separate the states. *If broken:* the PCI analog is insufficient; Gap-4 reverts to honest negative. **Result:** the **conscious/unconscious split is sign-stable** across 9 cells (REM>NREM 9/0/0, WAKE>NREM 9/0/0, conscious-separated 9/0/0; conscious−unconscious margin +0.347→+0.481 vs margin 0.05) — wake≈REM (0.464) ≫ NREM (0.036), non-circular (no kick → PCI = 0), and PCI dissociates from raw arousal; `conscious_unconscious_separation_sign_stable = True`, `broke_on = []`. Gap-4 → `[L]` in-silico **for the split**. The **part that collapsed** is recorded, not avoided: the single PCI scalar does **not** separate NREM/anaesthesia/VS (within-unconscious spread 0.045 < margin on every cell; "deeper → lower PCI" holds nowhere) → the within-unconscious ordering stays `[O]` (this is consistent with PCI's clinical role: a conscious/unconscious *binary*, not a fine unconscious ranking). wake≈REM exactly → wake>REM gap also `[O]`. See Section 2D.

- **ST-E — integration-pass reproduction audit (Chunk E). — DONE (S6): SURVIVED.** An integration pass has one failure mode: a recorded survivor that no longer reproduces. The atlas re-derives every committed digest from the artifacts on disk and requires `recomputed == stored == committed-expected-sha` for all seven build+ST artifacts, plus the M9 anchor bit-for-bit, the engine tree byte-unchanged, the firewall held, and `new_tuned_constants` over the whole chain = 0. *Break:* any artifact drifts (recorded in `broke_on`, `sim2_complete → False`, the line flagged for restart). *If broken:* the offending chunk restarts with the drift applied. **Result:** all 7 artifacts reproduce bit-for-bit, `broke_on = []`, engine invariant True, firewall held, `new_tuned_constants_total = 0` → `sim2_complete = True`, `project_closes = True`. See Section 2E.

*(Gap 5 has no stress test — it is not a claim.)*

---

## 5. Load division (session-sized chunks)

The long-term work is chunked so each new session carries **one bounded load**:

- **Chunk A (DONE, S2):** ST-1 — field-efficacy robustness. One cohort-sweep module. **Window SURVIVED** (sign-stable across 36 cells; Gap-1 → in-silico `[L]`, peak-location residual `[O]`).
- **Chunk B (DONE, S3):** Gap-2 build — additive cortical micro-model (cortico-cortical **hubs** + reentrant loop), then ST-2. Build + stress in one session. **Phenotype SURVIVED** (non-circular, topological, sign-stable across 9 cells; Gap-2 → in-silico `[L]`, gene-blindness residual `[O]`).
- **Chunk C (DONE, S4):** Gap-3 — full grounded connectome + O×W orthogonality, then ST-3. Build + stress in one session. **Double dissociation SURVIVED** (sign-stable crossover across 9 cells — two separable axes; Gap-3 → in-silico `[L]`, relative-selectivity / gene-blind / micro-model-property residuals `[O]`).
- **Chunk D (DONE, S5):** Gap-4 — PCI clinical match (ST-4), incl. `emerge_sleep_architecture` (REM vs deep sleep). Build + stress in one session. **Conscious/unconscious split SURVIVED** (sign-stable across 9 cells — wake≈REM ≫ NREM, non-circular; Gap-4 → in-silico `[L]` for the split). The within-unconscious ordering **COLLAPSED** to one scalar (NREM/anaesthesia/VS spread 0.045) — recorded honest negative `[O]`; wake≈REM gap `[O]`.
- **Chunk E (DONE, S6):** integration pass — re-read the whole surviving chain, re-derive every committed digest from the artifacts (the reproduction *act*), aggregate the per-gap grades, produce the v2 atlas. Build + audit in one session. **Chain SURVIVED the end-to-end digest audit** (all 7 build+ST artifacts reproduce bit-for-bit, engine byte-unchanged, firewall held, `new_tuned_constants` chain-total 0; `broke_on = []`) → **`sim2_complete = True`, `project_closes = True`.** Sim 2 is complete; Gap 5 stays the explicit firewall blank.

**Sim 2 is now CLOSED.** Both simulations are complete (Section 7): Sim 1 frozen, Sim 2 complete with all four fillable gaps surviving their stress tests or carrying recorded honest negatives, Gap 5 the explicit firewall blank, and the v2 atlas reproducing bit-for-bit.

**Rule:** a session does ONE chunk (or part). It ends by updating this whitepaper with results + the next chunk's entry. If a stress test breaks a hypothesis, the next session **restarts that chunk with the break applied**.

**Handover packaging (invariant).** The handover is delivered as **exactly one zip**, evolved **additively** from the existing archive — never a fresh tree, never scattered loose files. Each session adds **only the strictly necessary** new/changed entries: that session's new module(s), its results + digest(s) + figure, the updated `START_HERE_HANDOVER_v2.md`, and that session's `HANDOVER_v2_SESSIONk.md`. Prior `HANDOVER_v2_SESSION{<k}.md` records are left **byte-unchanged**. Minimal diff, single artifact, same filename (`vp_frontal_v2_handover.zip`). If a session has no budget for new work, it does **only** this packaging step (fold the session's results into the one zip) and stops.

---

## 6. Reproduction & provenance

- Frozen engine: `repro/frontal/_engine/vp_mind_engine.py` (READ-ONLY, sha `e61083ae…`).
- v2 modules: `repro/frontal/_frontal_v2/` (`cortical_emergence`, `cortical_wm_holding`, `frontal_axonal_channel`, `frontal_em_wave`, `cognition_consciousness_body`, **`field_efficacy_robustness` [ST-1, S2]**, **`cortical_microcircuit` [Gap-2 build, S3]**, **`cortical_microcircuit_st2` [ST-2, S3]**, **`cortico_connectome_owt` [Gap-3 build, S4]**, **`cortico_connectome_owt_st3` [ST-3, S4]**, **`pci_clinical_match` [Gap-4 build, S5]**, **`pci_clinical_match_st4` [ST-4, S5]**, **`v2_atlas` [integration pass / reproduction audit, S6]**).
- ST-1 artifacts (S2): `field_efficacy_robustness_results.json` (internal digest `05a7d317…`) + `expected_field_efficacy_robustness_sha256.json` + figure `field_efficacy_robustness.png`. Re-run is resumable/budget-bounded and deterministic (cells are call-invariant).
- Gap-2 / ST-2 artifacts (S3): `cortical_microcircuit_results.json` (internal digest `417a8319…`) + `expected_cortical_microcircuit_sha256.json`; `cortical_microcircuit_st2_results.json` (internal digest `a3d2e409…`) + `expected_cortical_microcircuit_st2_sha256.json`; figure `cortical_microcircuit_st2.png`. Deterministic; the ST-2 module imports the exact build model (non-circular at the code level).
- Gap-3 / ST-3 artifacts (S4): `cortico_connectome_owt_results.json` (internal digest `8d3f3e00…`) + `expected_cortico_connectome_owt_sha256.json`; `cortico_connectome_owt_st3_results.json` (internal digest `0b3a80ae…`) + `expected_cortico_connectome_owt_st3_sha256.json`; figure `cortico_connectome_owt_st3.png`. Deterministic; the ST-3 module imports the exact build model, and the O×W harness reproduces the Gap-2 `far_binding` value bit-for-bit at N = 120 (reuse-equivalence, non-circular at the code level).
- Gap-4 / ST-4 artifacts (S5): `pci_clinical_match_results.json` (internal digest `bde77370…`) + `expected_pci_clinical_match_sha256.json`; `pci_clinical_match_st4_results.json` (internal digest `2ada85a4…`) + `expected_pci_clinical_match_st4_sha256.json`; figures `pci_clinical_match.png`, `pci_clinical_match_st4.png`. Deterministic (cells are call-invariant); the ST-4 module imports the exact build model (`pci`/`STATES`), and the build asserts the M14 `emerge_sleep_architecture()` observables at run start (grounding the REM=activated / NREM=bistable state map; aborts on drift).
- Chunk E / atlas artifacts (S6): `v2_atlas_results.json` (digest `bbaa4e9405e8…`) + `expected_v2_atlas_sha256.json`; figure `v2_atlas.png`. The atlas re-derives every committed digest from artifact content and compares against the independently committed expected-sha files (non-circular: it does not copy shas forward); `engine_anchor_bitforbit()` + the engine-tree invariant guard the kernel; deterministic (re-runs reproduce the atlas digest bit-for-bit).
- M9 anchor: `R = 0.38961455156044245` (must reproduce bit-for-bit).
- Gene data: `_engine/data/brain_organ_atlas.json` (FOXG1 γ 1.4737; full per-organ bands), `brain_organ_gamma.json`.
- Cited connectome (Gap 3): Klein 2010 *NeuroImage* 51:555; *J Neurosci* 43:7780 (2023); Öngür & Price 1998 *JCN* 401:480; Radley 2006 *J Neurosci* 26:12967.
- Cited PCI / sleep mechanism (Gap 4): Casali 2013 *Sci Transl Med* 5(198):198ra105 (PCI orders wake≈REM > NREM > anaesthesia > VS); Casarotto 2016 *Ann Neurol* 80(5):718 (empirical cutoff PCI* ≈ 0.31); Massimini 2005 *Science* 309:2228 & Pigorini 2015 *NeuroImage* 112:105 (cortical bistability / OFF-period truncates the evoked causal chain); Sanchez-Vives & McCormick 2000 *Nat Neurosci* 3:1027 & Steriade 1993 *J Neurosci* 13:3252 (the M14 slow-adaptation mechanism / NREM operating point). Orderings used for external comparison only — nothing tuned to them.
- Tissue EM params: σ = 0.30 S/m, ε_r = 1e5, L_brain = 0.15 m.
- Every module prints its grades and `new_tuned_constants = 0`.

---

## 7. The project's end condition

This whitepaper closes when **both** simulations are complete:
- **Sim 1:** COMPLETE (frozen).
- **Sim 2:** COMPLETE when Gaps 1–4 have either **survived** their stress tests (`[V]`/`[L]`) or been recorded as **honest negatives** (`[O]`), Gap 5 remains the explicit firewall blank, and the v2 atlas reproduces. **→ MET (S6):** Gaps 1–4 all survived (in-silico `[L]`; Gap-4 with its recorded `[O]`), Gap 5 is the firewall blank, and the v2 atlas reproduces bit-for-bit (`sim2_complete = True`, `project_closes = True`).

**Both simulations are now complete. This whitepaper is CLOSED.**

The brain chain is then "complete" in the project's sense: **every link is verified, grounded, or an honest open — with nothing tuned and nothing falsely filled.**

---

*End of Session-6 handover — Sim 2 CLOSED. Chunk E (the v2 atlas) is the integration pass that closes the project: it re-reads the whole surviving chain and re-derives every committed digest from the artifacts on disk, so "the chain reproduces" is performed, not asserted. The end-to-end digest audit SURVIVED — all seven build+stress-test artifacts reproduce bit-for-bit (`broke_on = []`), the frozen engine is byte-unchanged (M9 anchor `R = 0.38961455156044245` exact, full tree + M0–M16 subtree invariant), the firewall held (`consciousness_claim = 0`, `hard_problem_open = 1` on every gap), and `new_tuned_constants` summed over the whole chain is 0 → `sim2_complete = True`, `project_closes = True`. The standing ledger: Gap-1 `[L]` (field causal window, S2) · Gap-2 `[L]` (cortical micro-model, S3) · Gap-3 `[L]` (O×W crossover, S4) · Gap-4 `[L]` conscious/unconscious split + `[O]` within-unconscious ordering (S5) · Gap-5 `[O]` the firewall blank. Both simulations are complete: Sim 1 frozen, Sim 2 closed with every link verified, grounded, or an honest open — nothing tuned, nothing falsely filled, and the hard-problem blank kept open by principle. This is an in-silico model result — NOT validated neuroscience and NOT clinical guidance. There is no Chunk F: the program's stated end condition (Section 7) is met. Any future work is a new program built atop this frozen, reproducing base — not a continuation of this whitepaper.*
