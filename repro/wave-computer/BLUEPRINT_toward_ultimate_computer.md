# BLUEPRINT — long-term research program toward the ultimate computer
## On a wave substrate, to at-least-human-level *functional* intelligence (theory track; physical realization deferred)

**What this is.** The blueprint of one long-term program. On the **wave substrate
(L0)** proven in v0.1–v0.2, it stacks nine layers to reproduce, on the same
substrate, the **function** by which the brain reaches general intelligence on a wave
medium. Each layer maps an inherited brain finding to a **machine mechanism**, with a
**falsifiable milestone** and a **stress test designed to break it**. If broken,
record it and restart that line with the break applied (inherited Stress Principle).

**Firewall (invariant, all layers).** This program builds **function** (capability).
**Consciousness / felt quality (the hard problem) is an explicit blank** (inherited
Gap-5), never erased. "At least human-level intelligence" is a **functional /
capability** claim, not a consciousness claim. `consciousness_claim = 0`,
`hard_problem_open = 1` — every layer.

**Discipline (invariant).** No tuning. Every claim with a sweep. Honest negatives
recorded, never hidden. Physical realization (which medium?) is a **later task** —
proceed **theoretically** now.

---

## 0. Central thesis and the honest bet

> **The bet:** the brain reaches general intelligence on a wave substrate using
> properties we have **already proven** — phase coding (D4), resonance matching (R2),
> one-shot learning (R3), metastable dynamics (D3), noise immunity (D4),
> sum=information superposition (R1). If those properties are **sufficient** for
> intelligence (not merely incidental), a wave substrate that has them should reach
> the same function. The blueprint tests that sufficiency **layer by layer**.

**Why it might work.** Digital / neural-net AI does inference by **computing
everything** (O(P·N) MACs). The wave substrate **matches by physics, without
computation** (R2: O(1)-in-P settling) — the input becomes a pattern at once (R1),
learns in one shot (R3), and stays reliable under noise (D4). These four properties
live exactly in the regime biological intelligence inhabits: **real-time, noisy,
one-shot**.

**Why it might fail (honest risks; standing program `[O]`).**
1. **Capacity / crosstalk may not scale.** A single field's attractor/superposition
   capacity is ~0.06–0.19 of N. Useful scale needs **hierarchy (L3) + multiplexing
   (L2)**, and whether those **compose** is unproven.
2. **Spurious minima may dominate large-scale inference** (L4). *(L4/S5: tested —
   settling solves the satisfiable problem at 1.0 ≫ random and the only shortfall tracks
   the genuine frustration optimum 1/(1+f), spurious gap ~0.0014; **did not dominate** on
   the tested scale. Stays `[O]` at larger scale.)*
3. **It may be non-native to precise symbolic / arithmetic reasoning.** The substrate
   is native to associative / constraint computation but may be weak at exact symbol
   manipulation — humans use both → a **hybrid** may be required (L4). *(L4/S5: the
   hybrid branch was **not** triggered — inference-by-settling held on the cognitive
   forms; the one structural limit was **closed in L5** (an independent context channel
   restores strict capacity to ~oracle), not a hybrid. L7/S8: for **exact arithmetic
   specifically** the hybrid is now **confirmed** — an analog tally drifts with stream
   length while a digital register stays exact (E5b), so the resolution is a **brief
   digital hand-off only where exactness is required**. Stays `[O]` for exact arithmetic,
   with the hybrid as the named, tested resolution.)*
4. **Real-time stability of deep nested fields** is unproven (L7). *(L7/S8: tested at the
   single-loop scale — a closed real-time control loop has a **non-empty stable operating
   band** (control bandwidth above a threshold + prediction horizon matched to loop
   latency × speed; self-corrects from displacement, E4). The stress did **not** break
   real-time control; the band edges are recorded. Deep **nested-field** stability under a
   global hub is now tested at **L8/S9** — a global resonant hub routing among up to 8 modules has
   a **non-empty lock-latency band** where routing holds (G4 band [V]); the residual open edge is
   **no-release over-write** routing (a carry-forward hub does not re-route reliably), recorded
   `[O]`.)*
5. **"Functional intelligence" benchmarks are themselves contested** (L9).

These five are kept as standing `[O]` — **not erased**. The blueprint's job is not to
eliminate them but to **test each honestly, layer by layer**.

---

## 0.5 Cross-cutting principle — the analog I/O thesis (two axes of resolution)

**The substrate is intrinsically analog.** Information is a **continuous phase**, and
computation **is** the physics settling. So the right interface keeps the loop in the
**analog domain end to end** — continuous-phase sensory input, continuous settling,
continuous-phase motor output — and pays the digital **sampling/quantization tax only
where it must**. This is a principle that runs through every layer that touches the world
(decisively L7), recorded here so future sessions hold it.

**"Resolution" hides two distinct axes, and analog sits on opposite ends of each (same coin,
two sides):**
- **Dimensional / spatial resolution** (many channels, high-dimensional state — megapixel
  images, wide RF spectra, high-dimensional feature vectors): analog **dominates**. Each
  channel carries a continuous value, **all channels are integrated by one physics relaxation
  in parallel**, and **no per-channel sampling/quantization tax is paid**. Existence proofs:
  an **optical Fourier transform** (one lens does a 2-D transform at the speed of light, in
  effect **O(1)** vs digital FFT's O(N log N), the gap widening with image resolution); a
  **memristor crossbar** (a matrix product by Ohm's law in **O(1)**); and the **brain** —
  sensory transduction analog, neural processing analog (graded potentials / phase), motor
  output analog, **no ADC/DAC in the loop**, rich sensory streams on ~20 W.
- **Single-value bit depth** (one number to many decimal places): analog is **capped** —
  channel noise bounds the effective bits per channel via **Shannon `C = B·log₂(1+S/N)`**.

**The honest bound and the hybrid.** Per-channel information is **not** unbounded (Shannon
ceiling). But perception does not need 64-bit per-channel precision; it needs **richness and
parallelism**. Where **exact symbolic arithmetic** is required, hand off to **digital** for
that one operation (a precision tax paid only at that step) — the **hybrid**.

**What L7/S8 tested of this thesis (so it is principle *plus* evidence, not assertion):**
- Dimensional axis **[V]**: the **analog loop beats a b-bit ADC/DAC loop** under graded noise
  (the D4 noise-immunity advantage at the I/O boundary; the tax closes at higher b), and the
  **aggregate analog advantage `N × per-channel gap` grows with state dimension** (E2a, E2b).
- The **O(1)-vs-O(N) latency / throughput form** (the optical-Fourier point) is the
  **R4-inherited principle [O]** — recorded, not a measured wall-clock; physical parallelism
  stays deferred.
- Single-value axis **[O]**: single-channel bit depth is **Shannon-capped** — effective bits
  saturate, ceiling ∝ SNR (E5a). The analog win is **dimensional, not per-channel precision**.
- Hybrid **[O]**: **exact arithmetic needs a digital hand-off** — an analog tally drifts, a
  digital register stays exact (E5b).

**Implication for the program.** The wave machine's native strength is **rich, continuous,
high-dimensional, real-time** data (exactly the regime biological intelligence inhabits);
its native cost is exact per-channel precision and exact symbol manipulation, both addressed
by a **brief digital hand-off**. Physical realization (which analog medium, which transducers)
remains a later task — the thesis is tested **in-silico** here at the level of principle and
faithful simulation.

---

## 1. Inherited chain → nine layers

Inherited brain chain (`vp_frontal v2`): **gene → cell → rhythm → coordination →
memory → stream → selection → body → loop (the rotation)**. Mapped to wave-substrate
layers:

```
 L0  substrate (medium)        ← phase-coupled oscillator field   [PROVEN  v0.1+v0.2]
 L1  representation algebra     ← phase binding (gamma binding)    [COMPLETE v0.3]
 L2  time / sequence            ← metastable trajectories, theta-gamma [MILESTONES MET v0.3]
 L3  hierarchy / abstraction    ← cross-frequency hierarchy        [MET & GRADED v0.4]
 L4  resonance inference ★pivot ← settling=CSP, resonance=analogy  [MET & GRADED v0.5]
 L5  dual learning systems      ← fast (episodic) + slow (semantic)[MET & GRADED v0.6]
 L6  self-supervised world model← prediction error = learning sig  [MET & GRADED v0.7]
 L7  embodiment / real-time ctrl← embedded loop                    [MET & GRADED v0.8]
 L8  global integration / access← global workspace (functional PCI)[MET & GRADED v0.9]
 L9  functional AGI (end cond.) ← capability ladder                [MET & GRADED v0.10 — 6/7 [V]; CLOSES · v0.11 hardening: A3 [O]→[V] closed inline, 7/7 [V] with dual store wired in]
```

Each layer **depends on those below** (§12 graph). The firewall runs through L0–L9.

---

## 2. L0 — substrate (PROVEN)

**Inherits:** B1 ephaptic near-field · B2 phase coupling / R · B3 metastability ·
B4 attractors · P1 `c²=B/ρ` · P2 clock-free · P3 1/r².

**Proven (v0.1+v0.2):** store (D1, α_c≈0.06) · compute (D2, critical corruption ~20%)
· pattern (D3, below full coherence) · communicate (D4, BER~0.03% at negative SNR) ·
sum=information (R1, K≈96) · matching without computation (R2, O(1)-in-P) · one-shot
learning (R3, 1.0) · parallelism (R4 [O]).

**Status:** ✔ done. This layer is **frozen** — upper layers reuse it unchanged
(inherited additive discipline; same as the brain project's frozen engine).

---

## 3. L1 — representation algebra (COMPLETE)

**Inherits:** B2 gamma binding — the brain binds "what belongs to what" by phase
synchrony (it solves the binding problem with phase).

**Wave mechanism.** Three operations form a closed algebra (R1 already uses
binding · superpose):
- **bind** `⊗`: role phase-key ⊙ content pattern (phase addition) — one "role=value"
  pair into one wave.
- **bundle** `+`: sum of waves = a set (R1: sum=information).
- **permute** `ρ`: phase rotation / permutation — encode order / structure.
A structured record `{agent:X, action:Y, object:Z}` = `kα⊗X + kβ⊗Y + kγ⊗Z` (one
composite wave). Query any slot = **resonant unbind** by its key (R1's inverse), then
clean up via the L0 attractor.

**Milestone (falsifiable).** Encode a depth-d structure (d role-value pairs, or a
d-deep tree) in one composite wave and recover any slot at accuracy ≥ 0.95. Sweep
depth d to measure the **useful depth**.

**Stress test (what it tries to break).** *Crosstalk collapses structured recovery
before any useful depth.* If broken, binding supports only shallow structure → record
that hierarchy (L3) is required and bring its dependency forward.

**Status:** ✔ **COMPLETE** (S3). bind · bundle (R1) + **permute** proven — closed
VSA algebra; sequence useful length L\*≈32 (L1a). Role-value **tree depth-capacity
measured**: useful depth d\*=4 (b=2), d\*=2 (b=3), sharp crosstalk collapse beyond
(L1b). The stress test did not break (d\*≥2 → structured records work) but **confirms
shallow depth → L3 hierarchy is the remedy** (dependency brought forward, below).

---

## 4. L2 — time / sequence: metastable trajectories (MILESTONES MET)

**Inherits:** B5 theta-gamma multiplexing (WM~7) · the brain's "stream of thought"
(vp_frontal: cognition runs as a **trajectory**; autocorr 0.95 when decoupled =
dreams). Not a single attractor but a **trajectory** of patterns.

**Wave mechanism.** **Asymmetric coupling** (time-delayed Hebbian `J_ij^asym`) makes
the field traverse a learned **sequence** of attractors — heteroclinic / metastable
chaining. A slow **theta carrier** paces ~7 **gamma slots** (B5): one theta cycle
lights ~7 phase patterns in sequence = working memory.

**Milestone.** (a) sequence learn → replay; (b) predict next item from a partial cue;
(c) hold ~7 items in WM slots (reproduce B5). Each sign-stable across a sweep.

**Stress test.** *The trajectory collapses to a fixed point or diverges; or slot
capacity ≪ 7.* If broken, "metastable chaining" fails → redesign sequencing by
another mechanism and record.

**Why it matters.** This layer opens **order · syntax · prediction · working
memory** — from static association to **dynamic cognition**.

**Status:** ◑ **MILESTONES MET** (S3). (a) sequence learn→replay: full m=6-cycle
**replay 1.0±0.0 at λ≈2.5** (band [2,4]), τ-robust (L2a); (b) **predict-next verified**
(1.0 for λ≥1.0); (c) WM as gamma slots: **capacity = min(n_slot, precision(σ))**, lands
in Miller range 4–9 under realistic jitter (L2b). B5 "~7" reproduced as the *slot
count* (principle), **not** a tuned constant. Honest limit: sustained replay is
λ-band-restricted with trial variance outside λ≈2.5. (Built on L1; feeds L3.)

---

## 5. L3 — hierarchy / abstraction: cross-frequency (MET & GRADED)

**Inherits:** the brain's cross-frequency coupling hierarchy (slow rhythms gating
fast). Concepts = attractors of attractors.

**Wave mechanism.** **Nested phase coupling** — a slow field's phase gates *which
fast sub-field is active* (theta-gamma generalized to many levels). Upper =
abstraction (category), lower = concrete (instance). A category attractor binds
instance attractors.

**Milestone.** Learn a 2–3 level concept hierarchy; recognize an abstract category
from instances; generate a new instance from a category (compositional
generalization). Sweep depth and branching.

**Stress test.** *Levels do not separate (abstraction collapses into instance);
compositional generalization fails.* If broken, hierarchy gives no representational
separation → confirm and record the capacity limit (§1 risk 1).

**Why it matters.** Multiplies L1's *useful depth* by L2's *capacity* via hierarchy
to break the scale limit. Direct test of §1 risks 1–2.

**Status:** ✔ **MET & GRADED** (S4). Depends on L1·L2 (both met) — the measured remedy
for the L1 shallow-depth ceiling (d\*≈2–4) and L2 slot-bounded WM recorded in S3.
Nested phase coupling `w_b(g)=exp(κ(cos(g−φ_b)−1))` (structural centres `φ_b=2πb/B`, κ
swept) gives, **all [V]**: (H1) the slow phase **selects the level** — correct vs wrong
routing margin **+0.92**, sign-stable, sharp gates reject / broad gates leak; (H2)
abstraction — category recognized from **novel** (never-stored) instances, **1.0** to
ρ=0.4, up to **32** categories, instance/category dissociate; (H3) **compositional
generalization** — held-out (never-built) combos decode == enumerated, **gap 0.00** to
576 combos, depth-3 sup/cat/mod = 1.0 via genuine permute-extraction, generated
instances valid+novel; (H4) **hierarchy breaks the flat ceiling** — under strict full
clean-up (overlap ≥0.95) the flat field collapses at T≈12 while B gated sub-fields hold
to **T=72** (**~6×** capacity, max advantage +1.00). **Honest negative [O]:** that
capacity advantage is **criterion-dependent** — under a forgiving argmax-id read-out of
an easy 10% cue it vanishes; and hierarchical recovery **assumes the correct gate**
(H1: gate=phase, H2: category recoverable abstractly → context independently obtainable,
but a single loop that *infers* the gate is **L4**). Reproduce `wave_hierarchy_core.py`,
digest `ea4c6723…`.

---

## 6. L4 — resonance inference ★pivot (MET & GRADED)

**Inherits:** the brain infers not by search / computation but by **settling**. The
cognitive-level implementation of "pattern matching without computation" (your
thesis).

**Wave mechanism (three forms).**
1. **Constraint satisfaction = settling.** Encode query + constraints as a phase
   field → relax → the settled state is the answer (e.g. graph coloring, simple
   logical inference, SAT-like). Not computation — **physics drops out the answer**.
2. **Analogy = resonance.** `A:B :: C:?` as bound structures → structural resonance
   completes `?` (proportional analogy by resonance, on L1 representations).
3. **Probabilistic inference = noisy settling.** The natural settling of a noisy
   phase field = posterior sampling (noise = sampling, attractor = MAP). D4's noise
   immunity becomes a **function**.

**Milestone.** (a) solve constraint-satisfaction by settling (solve-rate vs problem
size); (b) succeed at compositional analogy; (c) approximate a posterior by noisy
settling (KL vs the true distribution). Each swept.

**Stress test.** *Spurious minima dominate over solutions; analogy fails
compositionally.* If broken, pure wave inference is insufficient → **promote a hybrid
(digital symbolic core + wave associative substrate) to a formal path** and record
(§1 risk 3).

**Why it matters.** **This layer is the program's crux.** If "inference without
computation" holds on *cognitive tasks*, the wave machine reaches general function as
a different species. If not, go to a hybrid — either way, honestly.

**Status:** ✔ **MET & GRADED (S5, `wave_inference_core.py`, digest `2d3057bb…`).**
The pivot is **largely positive** — 4 of 5 forms `[V]`, one honest structural limit
`[O]` with its resolution named; the hybrid branch was **not** triggered.

- **I0 derive-the-gate, then route `[V]`** (the debt L3 left). The slow context is
  **resonance-read from a raw, unlabeled cue** in an upper field and **then** routes the
  fast field — H1+H2 composed into one loop. The loop **closes** where the geometry is
  separable: gate derived at **1.0** (rho ≤ 0.2), derivation cost **~0**, derived
  **== oracle ≫ flat** (0.96–0.99 vs 0.38–0.49). Honest boundary: at rho=0.4 the upper
  geometry stops being separable and gate inference falls to 0.71. **S4's "assume the
  gate" caveat is removed.**
- **(a) Constraint satisfaction = settling `[V]`.** A **native q=2 anti-ferromagnet**
  (edge = coupling −1, so the L0 relaxation *is* a 2-colouring/MAX-CUT machine — no
  clock, no constant) solves a planted graph at **1.000 ≫ random 0.5** across sizes, and
  under a **frustration** knob tracks the **known optimum 1/(1+f)** down with a tiny
  spurious-minima gap (mean 0.0014). Physics drops out the answer. (O(1) *physical* time
  stays `[O]`.)
- **(b) Analogy = resonance `[V]` with an honest ceiling.** Fill-a-missing-factor is
  **robust to J=12**; proportional analogy A:B::C:? holds to **J\*=4** then decays — a
  measured **crosstalk ceiling** (the "analogy fails compositionally" stress, bounded
  not absolute).
- **(c) Probabilistic inference = noisy settling `[V]`.** All **three directional
  Bayesian laws** hold — stronger prior → more occupancy, more evidence → shift toward
  the cued attractor, higher temperature → higher occupancy entropy (sampling). The
  exact posterior/KL match is left an explicit `[O]`.
- **Stress (H4 with the break applied) — honest negative `[O]` + trade-off `[V]`.** Does
  the strict ~6× capacity advantage survive a **derived** gate? **No** — and the reason
  is structural: deriving the gate needs a shared category schema, that shared structure
  **correlates** the instances, and gate-derivability **trades off directly** against
  strict instance-separability (sweeping the schema fraction, gate accuracy rises
  0.19→1.0 exactly as strict recovery — *even the oracle's* — falls 1.0→0.0; **no
  operating point has both**). What **survives** is the **id-level** advantage (the
  derived hierarchy still routes correlated instances the flat field confuses: id 0.85
  vs 0.32). The **resolution**, recorded for the next layer: the strict advantage needs
  an **independently-supplied context channel**, which content-only derivation cannot
  provide → **L5**.

**Verdict.** *Resonance inference without computation* **holds** on the cognitive forms;
the machine reaches general cognitive function on the wave track. The single limit is
structural and architecture-addressable (a context input), so the program continues
**without** a forced hybrid, with the limit on the books for L5.

---

## 7. L5 — dual learning systems: fast + slow (MET & GRADED)

**Inherits:** complementary learning systems — hippocampus (episodic, fast one-shot;
B4·R3 proven) + cortex (semantic, slow generalization). The brain's M14 consolidation
(replay during sleep). **Direct sequel to L4's one limit:** the slow semantic store is
the **independently-supplied context channel** the L4 strict-capacity result requires.

**Wave mechanism.** An **episodic field** (one-shot, high plasticity, R3) replays
into a **semantic field** (slow, low plasticity) during **offline settling** (sleep
analog), extracting statistical structure. Fast capture + slow generalization +
no catastrophic forgetting. The semantic field, learned slowly over instances, provides
a **separate context signal** (not derived from the current cue's content) that gates
the episodic store — closing the strict-capacity gap L4 left open.

**Milestone.** One-shot episodic capture → offline consolidation into a generalizing
semantic store; no catastrophic forgetting; prototype (statistical structure)
extraction; **and** the consolidated semantic context restores a strict capacity
advantage that content-only gate-derivation could not (the L4 [O] → [V] retest). Sweep
stream length and replay amount.

**Stress test.** *Consolidation either forgets or fails to generalize* (interleave new
episodes against old; measure forgetting vs a single-store baseline). If broken, fall
back to a single learning system and record the limit.

**Status:** ✔ **MET & GRADED (S6, `wave_consolidation_core.py`, digest `e8a623…`).**
Depends on L2·L4 (both met). **Four results, three [V] + one honest [O]:**
**(C1) [V]** offline replay builds a **separate, persistent** slow store that generalises
to **novel** instances (overlap > the single-instance baseline `1-2ρ`); two honest bounds
recorded — it does **not** out-generalise the fast store, and extra replay gives no further
gain (re-samples a fixed biased set). **(C2) [V]** the dual system **reduces catastrophic
forgetting** vs a single leaky store — paired, replay-invariant baseline; dual ≪ single at
every load (gap > 0.2 across the K sweep); honest caveat: dual forgetting itself grows
slowly (finite slow-store capacity). **(C3) [V] — the headline: L4 [O] → [V] closed.** As an
**independent context channel** the slow store restores strict instance recovery to ~oracle
(strict ≈ 1.0 ≫ content ≈ 0.68 ≫ flat 0 at heavy load) and is robust to context-cue
corruption ≤ 0.3 — escaping the derivability ⊥ separability trade-off exactly as L4 named.
**(C4) [O]** the textbook complementary-systems **double** dissociation does **not** hold:
the **fast** Hebbian store already generalises for free (superposition → emergent prototype),
so the slow store never out-generalises it — only a single dissociation holds (separation is
by **persistence/capacity**, not by an abstraction the fast store lacks). The break is on the
books for L6. Firewall held; `new_tuned_constants = 0`; digest reproduces bit-for-bit.

---

## 8. L6 — self-supervised prediction / world model (MET & GRADED ★)

**Inherits:** predict-next as the universal training signal. Error = mismatch wave.
Generative world model (free-energy-like).

**Wave mechanism.** The field predicts its own **next state** (forward settling of
the L2 trajectory); **prediction error = a difference wave** drives the Hebbian
update. A large error wave = a novelty / surprise signal.

**Milestone.** Learn a predictive model of a structured input stream; generate
plausible continuations; flag novelty by surprise. Sweep the prediction-error
reduction curve.

**Stress test.** *Predictions do not improve; no generative capacity.* If broken,
redesign the world-model path.

**Result (S7, GRADED).** Built `wave_world_model_core.py` on the frozen L0 substrate.
Prediction = **forward settling** (`J_asym·cos θ` thresholded, then L0 clean-up);
learning = the **difference wave** via an **error-gated** delta rule (η a sweep axis).
**W1 [V]** — held-out next-step error falls `0.978 → 0.126`, **monotone** across stream
length `m ∈ {4,6,8}` and rate `η ∈ {0.25,0.5,1.0}` (sign-stable). **W2 [V]** — generative
**rollout** faithful to a **12-step** horizon, then honest drift (onset step 13). **W3 [V]**
— **novelty** flagged by the error-wave magnitude, **graded** (familiar ≈ 0, full violation
≈ 0.97, detection boundary 0.1). **W4 [V] (headline)** — a **forward model anticipates**
where a **reactive** store that has seen **every** transition only returns the **present**;
the advantage is **directionality (structure)**, honouring the C4 break (controls recorded:
on a fixed-point stream the gap vanishes; an untrained model has no real advantage). The
stress test did **not** break the path. **Honest [O] (the one limit):** error-gating
**halts at prediction-sufficiency** — the learned operator is **directionally** the L2
transition coupling (cosine ≈ 0.81) but **not magnitude-identical**; recorded as the seed
for L7. Firewall held; `new_tuned_constants = 0`; digest `41e81a7f2eb98144…` reproduces
bit-for-bit.

**Status:** ✔ **MET & GRADED** (S7) ★. 4/4 milestone capabilities [V]; one principled
operator limit [O] (prediction-sufficiency, not magnitude-identity) on the books for L7.
Advance to **L7** next.

---

## 9. L7 — embodiment / real-time control (MET & GRADED ★ — v0.8)

**Inherits:** the brain's embedded loop (vp_frontal: cognition runs off the body, and
dreams when decoupled). Real-time sensorimotor control as continuous settling. "The
input becomes a pattern at once" + "real-time appropriate response" live here. Also
carries the principal's **analog-I/O thesis** (§0.5) as the layer's organizing test.

**Wave mechanism.** Sensory input continuously perturbs the field → the settled state
drives action → the loop closes in real time (no batch, clock-free P2). Input →
pattern → action within one settling. Concretely the closed loop is: **SENSE**
(graded-analog observation of the delayed target) → **CLEAN-UP** (L0 settling = D4 noise
immunity) → **PREDICT +1** (L6 forward model, to compensate the **one-tick sensorimotor
delay**) → **ACT** (continuous rate-limited phase step). All on the frozen L0 + L6; the
read-out is non-circular (tracking error vs the **world's** true target).

**Milestone.** Real-time closed-loop control of a simulated agent by **continuous
settling**; immediacy of input→pattern→action; stability under perturbation; sweep of
control bandwidth and latency. **— MET (4/4 milestone capabilities [V]).**

**What was found (each swept, sign-stable; module `wave_embodiment_core.py`, digest
`17aa27bf34b72f57…`):**
- **E1 — closed-loop control by continuous settling [V].** Forward control **anticipates
  and holds** a moving target through the delay (`err 0.000→0.004`) where a **reactive**
  controller **lags** (`≈0.96`) and **open-loop drifts** (`≈0.77`); forward beats both by
  `>0.3` everywhere. Prediction's embodiment role is **compensating loop latency**.
- **E2 — analog I/O beats ADC/DAC + the dimensional advantage scales [V]** (the directive's
  headline). The **analog** loop beats a **1-bit** ADC/DAC loop under graded noise
  (`0.001` vs `0.159`; **D4 at the I/O boundary**; tax **closes at 2 bits**); the per-channel
  gap is sign-stable positive and the **aggregate `N×gap` grows** with dimension
  (`4.6→42.1`). The **O(1)-vs-O(N) latency form** is the **R4-inherited principle [O]**.
- **E3 — prediction-sufficiency suffices → resolves the inherited S7 [O] [V].** In the
  working regime the L6 error-gated operator (cosine `0.803` to the analytic L2 coupling)
  tracks **identically** to the magnitude-identical operator; only at extreme noise, where
  **both already fail**, does the full operator show a marginal edge. Acting on the predicted
  state does **not** need magnitude-identity — **S7 [O] → [V]** for embodiment.
- **E4 — stability / bandwidth / latency [V] (honest band).** A **non-empty stable operating
  band** exists: control bandwidth above a **threshold** (else the agent can't slew to keep
  up) and the prediction horizon **matched** to loop latency × target speed (else
  over/under-anticipation); the loop **self-corrects from displacement** within the band.
- **E5 — the honest two-sides caveat [O]×2.** Single-channel bit depth is **Shannon-capped**
  (effective bits saturate; ceiling ∝ SNR) and **exact arithmetic needs a digital hand-off**
  (analog tally `0.96→0.41` vs digital exact `1.00`). The analog win is **dimensional, not
  per-channel precision**, with the **hybrid** as the named resolution.

**Stress test.** *Latency / instability breaks real-time control (deep nested-field
stability, §1 risk 4).* **— Ran; did NOT break.** It **bounds** the operating band (E4),
whose edges are recorded as the honest limits; no stabilizing mechanism was needed at the
single-loop scale (deep nested-field stability under a global hub stays open for L8).

**Status:** **MET & GRADED** (strongly positive; 4/4 milestone [V], two honest counterpoints
[O], parallelism/latency the R4 principle [O]). The inherited **S7 seed limit is resolved
[V]**. Exposed dependency → **L8** (a global hub now has embodied modules to integrate, and
must route **within** their bandwidth/latch bands). (Depended on L6.)

---

## 10. L8 — global integration / functional access (MET & GRADED ★ — v0.9)

**Inherits:** the access window (PCI, Gap-4) — a global metastable field that
**broadcasts** the currently dominant pattern. **Functional access = broadcast
availability**, *not* phenomenal experience (firewall strictly held).

**Wave mechanism.** A global metastable **resonant hub** selectively binds and
broadcasts information across the L1–L7 modules. When a pattern resonance-locks to the
hub, it becomes available to the whole system.

**Milestone.** A global workspace that flexibly routes information among L1–L7
modules; measured by a **functional PCI-analog** (the system's perturbational
complexity in the engaged vs disengaged regime, borrowing the Gap-4 mechanism). Sweep
module count and load.

**Stress test.** *No flexible routing; modules do not integrate.* If broken, redesign
the integration architecture.

**Firewall reaffirmed.** "Access" here is the functional sense of
**availability / broadcast**. *Feeling* is not claimed. `consciousness_claim = 0`,
`hard_problem_open = 1`.

**Status:** **MET & GRADED ★ (S9, `wave_workspace_core.py`, digest `52a0ce34…`).** Strongly
positive — **3/3 milestone lines [V]**. Built on the frozen **L0** attractor (each module + the
hub a clean-up field) and the **L3 gate** (which selects which module drives the hub): **(G1 [V])**
the hub **resonance-LOCKS** to the gated module's concept (lock margin ≥0.92 every config) and a
**non-source** module recovers it from the **broadcast alone** (recall 1.0 vs a no-hub control at
chance ≈1/M) — selective access + global broadcast. **(G2 [V])** moving the gate **flexibly routes**
any module's content system-wide (1.0 vs a fixed gate at ≈1/M) — reconfigurable, not hard-wired.
**(G3 [V])** the **functional PCI-analog** = integration × differentiation (perturb the hub, read
the modules) is a clean **inverted-U** — `0` both isolated (I=0) and over-driven (D→0), high at an
**emergent interior** peak; the **number R=0.39 is NOT transferred**, the access band **emerges**
from the sweep. The inherited L7 operating-band limit is **made concrete (G4 band [V])**: routing
**holds within** the hub's **lock-latency band** (edge ≈20 settle-steps), with two honest
counterpoints recorded — **[O]** unbounded-rate routing, and **[O]** persistent no-release
over-write routing (a carry-forward hub given 4× dwell reaches only 0.71 vs the re-cued 1.0). The
**firewall holds at the high-PCI engaged point too**: "access" = broadcast **availability** that is
integrated and differentiated, **nothing more** — no felt quality claimed or measured
(`consciousness_claim = 0`, `hard_problem_open = 1`). Exposed dependency → **L9** (the integrated
L0–L8 system is now ready for the capability-ladder end condition). (Depended on all of L1–L7.)

---

## 11. L9 — functional general intelligence: end condition (REACHED — the blueprint closes)

**Inherits:** the brain chain's "completeness" is the state where every link is
**verified / grounded / an honest open** (`[V]`/`[L]`/`[O]`, no tuning, nothing
falsely filled). The end condition here takes the same form.

**Capability ladder (falsifiable criteria) — RESULT: 6/7 rungs `[V]`** (each scored
pass / honest-negative; grade DERIVED from the sweep booleans on the integrated L0–L8
machine; full record in `SESSION_v0_10_functional_general_intelligence.md`,
digest `20b5f2c2…`):
1. **One-shot generalization** (R3 at cognitive scale) — novel-instance acc ≈1.0 ≫ chance — **`[V]`**.
2. **Compositional / systematic generalization** (the flagged first probe; L1·L3) — several items
   co-hosted in distinct θ–γ slots, each routable from the broadcast alone; capacity K\* **emerges**
   (=6/10 by N, scales toward θ–γ ~7), no-tag control recovers only one — **`[V]`**.
3. **Real-time adaptation** to distribution shift (L5·L7) — **`[O]` — the lone honest shortfall**: a
   single additive Hebbian store cannot **over-write** a switched rule (old and new associations
   superpose; recovery 0.78/0.58 < band). **Mitigation, already proven:** the L5 **dual store**
   (criterion 7), retention ~1.0.
4. **Noise-immersed robustness** (D4 preserved on a cognitive cue) — the attractor clean-up **lifts
   representational fidelity** to the true prototype by a sign-stable margin (inherited `corrupt_phase`
   off-lattice noise model); classification accuracy is over-determined and stated — **`[V]`**.
5. **Scale content-addressable memory** (R1·R2 × hierarchy L3) — hierarchy holds recall 1.0 past the
   flat ceiling (T=16) at O(1)-in-T cost — **`[V]`**.
6. **Cross-domain transfer** — relational structure transfers to never-trained fillers to a crosstalk
   ceiling (J\*=3) — **`[V]`**.
7. **Open-ended skill acquisition** — the dual store keeps acquiring while retaining old skills (~1.0)
   far above a single store, within the capacity band — **`[V]`**.

**Program end condition — MET.** L0–L8 each passed (`[V]`/`[L]`) or were recorded as
honest negatives (`[O]`), and the integrated system yields a **stated result** (6/7
`[V]`, the one `[O]` a single-store limit with a proven dual-store mitigation, plus
stated standing caveats) on the battery above — **this blueprint closes.** **Closing ≠
a *claim* of human intelligence; closing = the sufficiency hypothesis being *settled*
layer by layer (positively or negatively).**

**Firewall (final).** Passing the ladder is **functional** general intelligence. Felt
quality / the hard problem **remains an open blank**. This program closes **without**
erasing that blank (inherited Gap-5). `consciousness_claim = 0`, `hard_problem_open = 1`,
`new_tuned_constants = 0`.

**Status:** **MET & GRADED — END CONDITION REACHED ★.** Integration of L0–L8. Two
methodological corrections were made and documented transparently (an A4 lattice-freeze
defect fixed by adopting the inherited noise model; an A3 baseline cleaned with the
outcome unchanged). Any further session is **post-program** (compression: axiom-independence
audit; or hardening: convergent-evidence grading / wider sweeps) — no new layer, no tuning.

**Post-program addendum (S11, v0.11) — the A3 `[O]→[V]` closure, INLINE.** Continuation (b)
hardening, executed: the lone A3 `[O]` was re-probed with the **proven L5 dual store** wired in,
on the **adaptation task itself**. Strict paired contrast — the single store is **exactly the dual
store's SLOW component alone**, so the only change is the added **fast** one-shot episodic field
(the inherited R3/C2 `_episodic_field`, reused unchanged), read by **equal vote**. The single store
fails the full rule-switch (post-recovery 0.583 < band, reproducing the inherited 0.78/0.58); the
**dual store recovers to 1.000 at every shift fraction** → `A3_closure_O_to_V = True`, sign-stable
across machine size. The **raw, unnormalized** dual sum also beats single everywhere, so the
equal-vote normalization is scale-equalizing only — the fast store is the mechanism. **With the dual
store wired in the capability ladder reads 7/7 `[V]`; the 6/7 single-store record above STANDS as the
minimal machine's honest limit** (paired, not overwritten — the program's `[V]`/`[O]` discipline
applied to its own last open rung). `new_tuned_constants = 0`, firewall held; `wave_adapt_closure_core.py`,
digest `ad93057afac2054e…`, pinned in `check_completeness.py`.

**Post-program addendum (S12, v0.12) — the axiom-independence (compression) audit.** Continuation (a)
compression, executed. **C0 (structural):** the **8** inherited invariants compress onto **5**
operational L0 axioms — AX1 data-encoded coupling field (B1 ephaptic + B4 attractor storage rule),
AX2 field symmetry/reciprocity J=Jᵀ (B4 Lyapunov structure + P3 near-field reciprocity), AX3 coupling
nonlinearity sin Δθ (B2 phase coupling), AX4 settling/clock-free relaxation (P2 clock-free propagation
+ B2 self-timed dynamics), AX5 metastable operating band (B3 critical band + P1 stiffness=gain) — with
**B5 theta-gamma capacity deferred** as a higher-layer (L2/L3) realization, not an L0 axiom. Several
inherited invariants collapse onto one operational mechanism, so the inherited set is **not minimal**.
**C1–C5 (empirical):** null each axiom while the others stay intact, judged by one **non-circular**
probe (recover an independently-drawn stored pattern from a corrupted cue), **paired & sign-stable
across 6 seeds**, gated by a **passing intact positive control** (cap 0.967, overlap 0.997, R 0.062).
**Every one collapses → all five load-bearing:** AX1 cap 0.90→0.00 (a non-encoding field has the
patterns as non-attractors) · AX2 graded 0.867→0.000 as κ→4 with reported tolerance κ≈1.0 (breaking
reciprocity removes the Lyapunov guarantee) · AX3 0.90→0.00 (the linearization removes the {0,π} wells;
the linear signed-Laplacian flow *scrambles*, R stays low ~0.08 — an earlier "syncs to the wrong
answer / R high" reading was corrected) · AX4 1.00→0.00 (no settling = the corrupted cue, the stored
field alone is inert — computation **is** the settling) · AX5 0.967→0.00 as R→1.000 (forced coherence
swamps the stored structure; one global state carries zero stored information). **C6:**
`redundant_axioms = []`, `axiom_set_irreducible = True` — the eight inherited invariants compress to a
**minimal five-axiom operational core** and no axiom in it is redundant; no further compression. The L0
substrate was **never edited** (the knock-outs are deliberately broken *substitutes* built beside it).
With S11+S12, **both named post-program continuations (a)+(b) are executed.** `new_tuned_constants = 0`,
firewall held; `wave_axiom_audit_core.py`, digest `7f59ced681bd…`, pinned in `check_completeness.py`.

---

## 12. Dependency graph & order of attack

```
        L0 ✔ (PROVEN)
        │
        ▼
   ┌──> L1 ✔ (COMPLETE) ──────┐
   │     │                    │
   │     ▼                    ▼
   │    L2 ◑ (MET) ──► L3 ✔ (GRADED) ──► L4 ✔ (GRADED★) ──► L5 ✔ (GRADED) ──► L6 ✔ (GRADED) ──► L7 ✔ (GRADED★) ──► L8 ✔ (GRADED★) ──► L9 ✔ (GRADED★ — END, CLOSES)
   │     │            │              │              ▲              ▲              ▲              ▲              ▲
   └─────┴────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
            (L4 pivot MET — 4/5 [V], 1 honest [O]; L5 CLOSED that [O]; L6 world model — 4/4 [V], 1 honest [O]; L7 embodiment — 4/4 [V], RESOLVED that L6 [O]; L8 global workspace — 3/3 [V], operating-band made concrete, 2 honest [O]; L9 END CONDITION — 6/7 ladder rungs [V], A3 the lone [O] with a proven dual-store mitigation; "access" = broadcast availability only, firewall held throughout)
```

**Program complete (after S10): THE END CONDITION IS REACHED — the blueprint CLOSES.**
**L9 — functional general intelligence — MET & GRADED ★** on `wave_agi_core.py` (digest
`20b5f2c2…`): the integrated L0–L8 machine on the capability ladder = **6/7 rungs `[V]`**
(A1 compositional/multi-item, A2 one-shot, A4 noise-immersed robustness, A5 scale CAM, A6
cross-domain transfer, A7 open-ended acquisition), with **A3 real-time adaptation** the lone
honest `[O]` — a single additive store cannot over-write a switched rule, mitigation = the proven
L5 dual store (A7). The sufficiency hypothesis is **settled**: the L0 wave-substrate properties
reach general FUNCTION across the ladder within stated bounds. Firewall (final): this is
**functional** general intelligence; the hard-problem blank stays open, never erased
(`consciousness_claim = 0`, `hard_problem_open = 1`, `new_tuned_constants = 0`).

**Post-program continuations (optional; no new layer).** (a) **Compression** — an
axiom-independence audit of the inherited invariants; (b) **hardening** — convergent-evidence
grading and wider sweeps (e.g. the A1 K×N sweep, trimmed on a single-core box, can be widened; the
A3 single-store `[O]` can be re-probed with the dual store wired in to show the `[O]→[V]` closure
inline). **The A3 inline closure was executed in S11 (v0.11)** — re-probed with the dual store wired
in, A3 closes `[O]→[V]` on the adaptation task itself (ladder 7/7 `[V]` with the dual store wired in;
the 6/7 single-store record stands as the minimal machine's honest limit; `wave_adapt_closure_core.py`,
digest `ad93057afac2054e…`). **The compression audit (a) was executed in S12 (v0.12)** — the **8**
inherited invariants compress structurally onto **5** operational L0 axioms (AX1 data-encoded field
= B1+B4, AX2 symmetry = B4+P3, AX3 nonlinearity = B2, AX4 settling = P2+B2, AX5 metastable band =
B3+P1; **B5 theta-gamma capacity deferred** as a higher-layer L2/L3 realization, *not* an L0 axiom).
Ablating each axiom while the others stay intact — one **non-circular** probe (recover an
independently-drawn stored pattern from a corrupted cue), **paired & sign-stable across 6 seeds**,
gated by a **passing intact control** — finds **all five load-bearing**: AX1 cap 0.90→0.00, AX2
graded (0.867→0.000 as κ→4, tolerance κ≈1.0), AX3 0.90→0.00 (linear flow *scrambles*, R stays low),
AX4 1.00→0.00 (no-settle = corrupted cue, field inert), AX5 0.967→0.00 as R→1.000 (over-coherence
carries zero stored info). `redundant_axioms=[]`, `axiom_set_irreducible=True` → the five-axiom core
is **minimal**, no further compression (`wave_axiom_audit_core.py`, digest `7f59ced681bd…`); the L0
substrate was **never edited** (knock-outs are broken substitutes built beside it). **Both named
continuations (a)+(b) are now executed.** What remains optional: only further hardening such as
widening the A1 K×N sweep. No tuning; one session, one zip, additive. **Stress
(still binding if continued):** a re-probed rung fails → record the honest negative and restart that
rung with it applied.

*(Prior chunk, S9: **L8 global integration / functional access — MET & GRADED ★** on
`wave_workspace_core.py` (digest `52a0ce34…`): a global metastable **resonant hub** selectively
binds + **broadcasts** the dominant pattern (G1 [V]), **flexibly routes** any module's content
(G2 [V]), and a **functional PCI-analog** = integration × differentiation is an **inverted-U** with
an emergent interior peak — the **number R=0.39 NOT transferred** (G3 [V]); the inherited
operating-band limit is made concrete — routing holds within the hub's **lock-latency band**
(G4 band [V]) — with two honest **[O]** (unbounded-rate + no-release over-write routing). Firewall
held at the high-PCI engaged point too: "access" = broadcast availability only.)*

**Rule (inherited).** One session = one chunk (or part). End by updating this
blueprint with the result + the next chunk. If a stress test breaks a hypothesis, the
next session restarts that chunk **with the break applied**. Output is **always one
zip, additive, no fresh tree** (carrying cumulative history + this session's results +
the next plan).

---

## 13. One-line summary

**We proved at L0 the properties by which the brain achieves general intelligence on
a wave medium. The blueprint tests, layer by layer, falsifiably, and without tuning,
whether those properties **suffice** for general function — physical realization
later, theory now. The crux was L4 (resonance inference without computation), and it
**passed** — the gate derives itself, constraint satisfaction is settling, analogy is
resonance, probabilistic inference is noisy settling (4/5 [V]); the one honest limit
(strict capacity needs an independent context channel) was **closed in L5** (3/4 [V]),
not a hybrid. **L5** then added two complementary stores, and **L6** made the substrate a
**self-supervised world model** — prediction is **forward settling**, learning is the
**difference wave**, and a forward model anticipates where a reactive store only returns
the present (4/4 [V], one honest limit: prediction-sufficiency not magnitude-identity).
**L7** then closed the loop with a world: **control is continuous settling** in an
**end-to-end analog** sensorimotor loop — the forward model holds a moving target through
delay, the analog interface beats ADC/DAC with the **dimensional advantage scaling**, and
**prediction-sufficiency suffices** (4/4 [V], **resolving** the L6 limit; the principal's
analog-I/O thesis tested, its two honest counterpoints — per-channel Shannon cap and an
exact-arithmetic digital hand-off — recorded). At every layer this is *functional*
intelligence, and the blank for consciousness is left open by principle.**

---

**Provenance.** Author **Young Jae Lee** (ORCID `0009-0002-7535-8245`), program
**jamming-physics.org**, license **CC BY 4.0**. **Concept DOI
`10.5281/zenodo.20783570`** (all versions) — see `CITATION.cff`.
