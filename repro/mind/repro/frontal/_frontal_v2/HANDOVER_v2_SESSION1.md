# vp_frontal v2 — Handover & Long-Term Plan
## The Second Long-Term Simulation of the Brain Project

**Status:** Sim 2 opened. Session 1 of N complete.
**Frozen engine:** `vp_mind_engine.py`, sha `e61083ae…` (READ-ONLY)
**M9 anchor (bit-for-bit):** `R = 0.38961455156044245`
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

## 3. The brain chain and the five gaps

The mechanism chain (gene → cell → rhythm → coordination → memory → stream → selection → body → loops back: **the rotation**) is **complete at the mechanism level**. Five gaps remain; four are fillable (hypotheses entered), the fifth is open by principle.

| # | Gap | Status | Hypothesis (the fill) |
|---|-----|--------|-----------------------|
| 1 | EM field causal efficacy | **filled in-silico** | The field has a causal window; present at measured strength it opens access, cancelled/over-driven it shuts. In-vivo owed. |
| 2 | Cortical microstructure | in progress | Frontal executive fn emerges from cortico-cortical long-range hubs + the gamma broadcaster role; an additive cortical micro-model (hippocampus precedent) yields the phenotype. |
| 3 | Axonal connectome (W-axis) | grounded ordering | Long-range wiring carries routing (W); the autism/ID double dissociation lives here — autism = W-fault (local over-coordination → stereotypy), intellectual disability = O-fault (capacity ↓, W intact → preserved sociality). |
| 4 | Access window (consciousness) | mechanism shown | Consciousness = the subset of cognition reaching global EM coordination (high PCI); intuition = the remainder (cognition ≫ access). Quantitative clinical-PCI match owed. |
| 5 | Felt quality (hard problem) | **OPEN by principle** | Not simulation-fillable. The firewall. Left as an explicit blank; the chain closes **with** this blank, never by erasing it. |

---

## 4. Verification scenario for new sessions (stress tests)

Each hypothesis gets a test **designed to break it**. If it breaks, record the break and **restart that line with the break applied** (the Stress Principle).

- **ST-1 — EM field efficacy robustness (priority 1).** Is the in-silico causal window sign-stable across seed, duration, and perturbation node (F3-style cohort sweep)? *Break:* the window is an operating-point artifact (flips / seed-specific). *If broken:* Gap-1 reverts to `[O]`; the "field is causally necessary" claim is withdrawn; the coordination layer is re-examined.
- **ST-2 — cortical micro-model non-circularity.** Build Gap-2's micro-model. Does the frontal phenotype appear in a read-out **independent of the perturbed edge**? Is set-shifting sign-stable under a duration sweep? *Break:* the phenotype only appears in a circular read-out, or flips. *If broken:* the additive micro-model is insufficient; reconsider resolving cortex **inside** the kernel — which breaks M9 (a major fork).
- **ST-3 — O×W orthogonality (autism/ID).** Perturb W alone (sociality read-out falls, capacity preserved?) and O alone (reverse?). *Break:* the axes are not separable (one factor, not two). *If broken:* the autism/ID double dissociation collapses to a single factor; the clinical mapping is rewritten.
- **ST-4 — access-window clinical match.** Does the PCI-collapse curve **distinguish** anesthesia vs vegetative vs sleep (against clinical PCI values), or collapse to one scalar? *Break:* the analog does not separate the states. *If broken:* the PCI analog is insufficient; Gap-4 reverts to honest negative.

*(Gap 5 has no stress test — it is not a claim.)*

---

## 5. Load division (session-sized chunks)

The long-term work is chunked so each new session carries **one bounded load**:

- **Chunk A (next):** ST-1 — field-efficacy robustness. One cohort-sweep module. ~1 session.
- **Chunk B:** Gap-2 build — additive cortical micro-model (cortico-cortical hubs + reentrant loop), then ST-2. ~2 sessions (build, then stress).
- **Chunk C:** Gap-3 — full grounded connectome + O×W orthogonality (ST-3). ~2 sessions.
- **Chunk D:** Gap-4 — PCI clinical match (ST-4), incl. `emerge_sleep_architecture` (REM vs deep sleep). ~1–2 sessions.
- **Chunk E:** integration pass — re-run the whole chain with surviving hypotheses; update grades; produce the v2 atlas. ~1 session.

**Rule:** a session does ONE chunk (or part). It ends by updating this whitepaper with results + the next chunk's entry. If a stress test breaks a hypothesis, the next session **restarts that chunk with the break applied**.

---

## 6. Reproduction & provenance

- Frozen engine: `repro/frontal/_engine/vp_mind_engine.py` (READ-ONLY, sha `e61083ae…`).
- v2 modules: `repro/frontal/_frontal_v2/` (`cortical_emergence`, `cortical_wm_holding`, `frontal_axonal_channel`, `frontal_em_wave`, `cognition_consciousness_body`).
- M9 anchor: `R = 0.38961455156044245` (must reproduce bit-for-bit).
- Gene data: `_engine/data/brain_organ_atlas.json` (FOXG1 γ 1.4737; full per-organ bands), `brain_organ_gamma.json`.
- Cited connectome (Gap 3): Klein 2010 *NeuroImage* 51:555; *J Neurosci* 43:7780 (2023); Öngür & Price 1998 *JCN* 401:480; Radley 2006 *J Neurosci* 26:12967.
- Tissue EM params: σ = 0.30 S/m, ε_r = 1e5, L_brain = 0.15 m.
- Every module prints its grades and `new_tuned_constants = 0`.

---

## 7. The project's end condition

This whitepaper closes when **both** simulations are complete:
- **Sim 1:** COMPLETE (frozen).
- **Sim 2:** COMPLETE when Gaps 1–4 have either **survived** their stress tests (`[V]`/`[L]`) or been recorded as **honest negatives** (`[O]`), Gap 5 remains the explicit firewall blank, and the v2 atlas reproduces.

The brain chain is then "complete" in the project's sense: **every link is verified, grounded, or an honest open — with nothing tuned and nothing falsely filled.**

---

*End of Session-1 handover. Next session: open Chunk A (ST-1, field-efficacy robustness). Apply the Stress Principle — break it before trusting it.*
