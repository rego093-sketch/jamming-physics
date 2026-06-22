# SESSION v0.8 — L7 embodiment / real-time control (control = continuous settling; end-to-end analog loop)

**Module:** `repro/wave_embodiment_core.py` (reuses L0 `wave_compute_core` — `hebbian_field`,
`relax` clean-up = D4 noise immunity, `overlap`, `pattern_to_phase` — and L6
`wave_world_model_core` — `forward_predict`, `_train_world_model`,
`analytic_transition_coupling` — exact, non-circular; nothing frozen or prior edited; tracking
error is measured against the WORLD's true target, never a function of the trained trace).
**Figure:** `repro/wave_embodiment_atlas.png` (8 panels). **Digest:** `17aa27bf34b72f57…`
(deterministic, bit-for-bit, single-core OpenBLAS). **Firewall:** `consciousness_claim = 0`,
`hard_problem_open = 1`. **`new_tuned_constants = 0`.**

**Concept DOI:** `10.5281/zenodo.20783570` (reflected in `CITATION.cff` and the doc tops).

---

## Why this session

L0–L6 gave the substrate storage, an algebra, metastable trajectories, hierarchy, resonance
inference, two complementary stores, and a self-supervised forward model — but every one of
them ran **off-line**, reacting to or predicting from a stored cue. None of them was **in a
loop with a world**. L7's job (BLUEPRINT §9, §12) is to put the L6 forward model in a **closed,
real-time sensorimotor loop**: sensory input continuously perturbs the field, the settled state
drives action, and the loop closes in real time — clock-free (P2), no batch. The milestone:
**real-time closed-loop control of a simulated agent by continuous settling; immediacy of
input→pattern→action; stability under perturbation**, with a sweep of control bandwidth and
latency and a stress test designed to break it.

This session also carries a **standing directive from the principal**, made testable as the
layer's organizing thesis — the **analog I/O thesis**. The substrate is intrinsically analog
(information is a continuous phase; computation is the physics settling), so the right interface
keeps the loop in the analog domain end to end and pays the digital sampling/quantization tax
only where it must. The directive's two-axes claim is the spine of the layer:

> "High resolution" hides **two different axes**. (1) **Dimensional / spatial resolution**
> (many channels, high-dimensional state): analog **dominates** — each channel carries a
> continuous value, all channels are integrated by one physics relaxation in parallel, and no
> per-channel sampling/quantization tax is paid (optical Fourier: a lens does a 2-D transform in
> O(1); a memristor crossbar does a matrix product by Ohm's law in O(1); the brain runs a rich
> sensorimotor loop with **no ADC/DAC** at ~20 W). (2) **Single-value bit depth** (one number to
> many places): analog is **capped** — channel noise bounds the effective bits per channel
> (Shannon `C = B·log₂(1+S/N)`). Same coin, two sides. The advantage lives **only while the loop
> stays analog**; exact symbolic arithmetic needs a brief **digital hand-off** (the hybrid).

L7 inherits the **S7 seed limit** as a binding question: the L6 error-gated operator is
**directionally** the L2 transition coupling (cosine ≈ 0.81) but **not magnitude-identical** —
does a controller **acting on the predicted state** need the full-magnitude operator, or does
**prediction-sufficiency suffice**? E3 answers it inside the control loop.

---

## The closed loop (entirely on L0 + L6, non-circular)

Each tick of the clock-free loop:
- **SENSE** — a **graded analog** sensory channel observes the (delayed) target place as a
  continuous phase: `obs = θ_place + σ·𝒩` (true phase plus Gaussian phase noise). `cos(obs)` is a
  **confidence-bearing soft vote** (magnitude = certainty). An optional **ADC** quantizes the
  observation to `b` bits at the boundary.
- **CLEAN-UP** — the L0 attractor field relaxes the observation onto the nearest valid place:
  **D4 noise immunity at the sensory front end** (the soft votes are integrated in parallel by
  the relaxation).
- **PREDICT** — the L6 forward model **forward-settles one step** (anticipates the **next** place)
  to compensate the loop's **sensorimotor latency**. A reactive controller, lacking prediction,
  **lags one step** behind a moving target.
- **ACT** — a **continuous, rate-limited phase step** drives the agent state toward the desired
  place (**control = continuous settling**). An optional **DAC** quantizes the motor output.

The world then advances the target one tick; repeat. The **sensorimotor delay** (one tick) is
the realistic embodiment condition that makes prediction earn its place: by the time the agent's
settling completes and the motor acts, the target has already moved.

---

## What was built and found (each claim with a sweep; honest negatives kept)

### E1 — closed-loop control by continuous settling  **[V]**  (the L7 milestone)
Track a target moving one place/tick through a one-tick delay; sweep sensory noise
`σ ∈ {0.3,0.6,0.9,1.2}` × seeds. **Forward** control (anticipates +1) holds the target
(error `0.000 → 0.004`); **reactive** control (cleans the delayed cue, no prediction) **lags one
place** (`≈0.96`, near chance); **open-loop** (no feedback) **drifts** (`≈0.77`). Forward beats
reactive and open-loop by `> 0.3` at every noise level, sign-stable. **The verified claim:** the
substrate performs **real-time closed-loop control by continuous settling**, and the embodiment
value of the forward model is **compensating loop latency** — exactly the role prediction plays in
a delayed sensorimotor loop. The stress (forward no better than reactive/open-loop) **did not
fire**.

### E2 — analog I/O beats ADC/DAC, and the dimensional advantage scales  **[V]**  (the directive's headline)
**E2a — quantization tax `[V, simulated]`.** Run the same loop end-to-end **analog** vs through a
`b`-bit **ADC** (sensory) + `b`-bit **DAC** (motor), under graded noise σ=1.0. The **1-bit loop
pays a tax** (`0.159`) the analog loop avoids (`0.001`) — the `b`-bit boundary discards the graded
noise-margin the settling would integrate (**D4 at the I/O boundary**). **Honest:** the tax
**closes at 2 bits** (`0.009`) — the tax is a low-bit-depth phenomenon, recorded, not hidden.
**E2b — dimensional advantage `[V, simulated]`.** Sweep the substrate dimension
`N ∈ {48,96,192,288}`. The per-channel analog-vs-1-bit gap is **sign-stable positive**
(`0.096 → 0.163`), so the **aggregate advantage `N × gap` GROWS with dimension**
(`4.6 → 15.5 → 31.2 → 42.1`) — "**the gap widens as resolution rises**" in absolute
tracked-information terms. The mechanism is the directive's exactly: the per-channel advantage is
paid **once** by the parallel physics but **N times** by a serial-digital pipeline.
**E2c — parallelism / latency form `[O]`, principle, inherits R4.** Under L0's **R4 parallelism
principle**, the analog settling integrates all N channels in **O(1)** physical time while a
serial-digital read is **O(N)**; in a fixed real-time deadline this turns the dimensional edge
into a **throughput/latency edge that grows with sensory dimension** (the optical-Fourier /
memristor-crossbar O(1) point). This is recorded as **principle, not a measured wall-clock**, and
stays `[O]` exactly as R4 (physical parallelism) is `[O]`. The stress (no advantage at any
`b`/noise, or advantage not scaling with dimension) **did not fire**.

### E3 — prediction-sufficiency vs magnitude-identity  **[V]**  (resolves the inherited S7 [O])
Run the closed loop with (i) the **L6 error-gated operator** `J_asym` (prediction-sufficient,
measured cosine **0.803** to the analytic L2 coupling) vs (ii) the **analytic L2 transition
coupling** itself (magnitude-identical, cosine = 1). Sweep sensory noise
`σ ∈ {0.6,1.0,1.4,1.8}`. In the **working regime** (σ ≤ 1.4, where the controller tracks) the two
operators track **identically** (difference `0.000 → −0.009`); only at **extreme noise** (σ=1.8),
**where both controllers are already failing**, does the full operator show a **marginal**
robustness edge (`−0.047`). **Resolution:** **prediction-sufficiency SUFFICES for embodied
control** — acting on the predicted state does **not** need magnitude-identity in the operating
regime; **the inherited S7 [O] is resolved [V]** for the embodiment question, with the marginal
extreme-noise edge recorded honestly. The stress ("magnitude-identity required") **did not fire**
in the working regime.

### E4 — stability / bandwidth / latency  **[V]**  (the blueprint's L7 stress; honest band recorded)
Probe the closed loop's **stable operating band**.
- **E4a — control-bandwidth frontier.** Sweep the motor rate at matched speed; below a **threshold
  rate (0.5)** the agent cannot slew fast enough and tracking **breaks** (`0.60 → 0.37` below;
  `0.00` above). The bandwidth must exceed what the target's motion demands.
- **E4b — latency / horizon frontier.** Sweep target speed at a fixed +1 predictor; **only the
  matched speed** (delay × speed = horizon = 1) tracks (`0.00`); off-nominal speeds **over- or
  under-anticipate** (`sp0.5 = 0.48`, `sp2.0 = 0.96`). The prediction horizon must **match the
  loop latency × target speed** — a multi-step rollout (W2) would widen this range (future work).
- **E4c — self-correction.** Started **displaced** (random initial phase), the loop **re-acquires
  by settling** — a contraction — within `≤ 3` ticks at high bandwidth and not at all below the
  threshold (it is the same frontier). **The verified claim:** a **non-empty stable operating band
  exists**; the band's edges (bandwidth threshold + matched horizon) are the **honest recorded
  limits**. The stress ("latency/instability breaks real-time control") **did not break the path**;
  it **bounds** the operating band.

### E5 — the honest two-sides caveat  **[O] + [O]**  (the directive's own counterpoints; recorded, not hidden)
- **E5a — single-channel bit depth is Shannon-capped `[O by design]`.** Ask a single analog phase
  channel (averaged over an 8-oscillator block) to carry `L` levels under noise σ, decode to the
  nearest level. **Effective bits saturate** below the requested levels at high request, with the
  **ceiling rising as SNR rises** (σ=0.2 → **5.05 b**, σ=0.5 → **3.78 b**, σ=1.0 → **2.76 b**).
  Per-channel precision is **bounded by channel SNR** (Shannon `C = B·log₂(1+S/N)`): asking for
  more levels past the noise floor yields no more distinguishable bits. **The analog strength is
  DIMENSIONAL (E2), not single-value bit depth** — same coin, two sides, exactly as the directive
  states. (This is the honest negative that **balances the E2 headline**.)
- **E5b — exact arithmetic needs a digital hand-off `[O], hybrid`.** Maintain an **exact count**
  over a stream: an analog accumulator adds ~1 per occurrence with gain noise (**drifts**); a
  digital register increments exactly. The analog exact-count accuracy **decays with stream
  length** (`0.96 → 0.41` as K: 5→80) while the **digital register stays exact** (`1.00`). **Hand
  off to digital ONLY at the moment exactness is required** — the **hybrid** the directive names,
  and the concrete form of the **standing L4 [O]** on exact symbolic arithmetic.

---

## L7 verdict (honestly)

**The substrate controls in real time, in a closed analog loop, by continuous settling.** The
forward model holds a moving target through sensorimotor delay where a reactive controller lags
and open-loop drifts (E1 [V]); the **analog loop beats a b-bit ADC/DAC loop** under graded noise
(D4 at the I/O boundary; the tax closes at higher b) and the **aggregate analog advantage grows
with state dimension** — the directive's headline — with the O(1)-vs-O(N) latency form recorded
as the R4-inherited principle (E2 [V]; E2c [O]); **prediction-sufficiency suffices for control**,
resolving the inherited S7 [O] (E3 [V]); and a **stable operating band exists** with its edges
recorded (E4 [V]). **Four milestone capabilities [V].** The honest two-sides caveat is recorded,
not hidden: **single-channel bit depth is Shannon-capped** and **exact arithmetic needs a digital
hand-off** (E5 [O]×2) — precisely the limits the directive itself names, with the hybrid as the
named resolution.

**The directive, settled.** The analog-I/O thesis is now **tested**, not merely asserted: analog
**dominates the dimensional axis** (E2, parallel physics, no quantization tax) and is **capped on
the single-value bit-depth axis** (E5a, Shannon), with the **hybrid** (E5b) covering exact
arithmetic. Its strongest form — O(1) parallel settling vs O(N) serial digital — is the
**R4-inherited principle** (E2c [O]); physical realization stays deferred.

**Discipline upheld.** Every claim swept and sign-stable; control is **continuous settling** on
the frozen L0 substrate and prediction is the **L6 forward model** — no read-out is circular
(tracking error is vs the **world's** true target; the operator cosine is computed against the
analytic L2 coupling, not the trained trace); the motor **rate** is a **swept** control-bandwidth
axis (E4), reported, not tuned; `SETTLE`/`DELAY` are dynamics constants, not fitted; brain anchors
(R=0.39, WM≈7) are **not** transferred; `new_tuned_constants = 0`; firewall held at every step;
digest reproduces bit-for-bit on a single core across repeated runs.

**Layer status after S8. L7 embodiment / real-time control — MET & GRADED.** Strongly positive
(4/4 milestone lines [V]) with the directive's two honest counterpoints recorded ([O]: per-channel
Shannon cap; [O]: exact-arithmetic digital hand-off) and the parallelism/latency form held as the
R4-inherited principle ([O]). The inherited **S7 seed limit is resolved [V]** (prediction-
sufficiency suffices for control). Exposed dependency → **L8 global integration / functional
access** (a global metastable resonant hub that broadcasts the dominant pattern across the L1–L7
modules; a functional PCI-analog), which now has **embodied modules to integrate** and inherits
L7's honest **operating-band** limit (a global hub must route among modules **within** their
bandwidth/latch bands).

**Artifacts.** `wave_embodiment_core.py` (+`wave_embodiment_results.json`
+`wave_embodiment_atlas.png` +`expected_digest_v0_8.json`), `make_figure_v0_8.py` (8-panel
E1 control / E2a tax / E2b dimensional / E3 prediction-sufficiency / E4a bandwidth / E4b horizon /
E5a Shannon cap / E5b hybrid hand-off), `CITATION.cff` (concept DOI `10.5281/zenodo.20783570`).
`check_completeness.py` updated to re-run and pin this module. Digest `17aa27bf34b72f57…`,
deterministic.
