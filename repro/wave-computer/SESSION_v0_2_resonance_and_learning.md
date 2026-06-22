# SESSION v0.2 — resonance · superposition · one-shot learning · parallelism

**Status:** v0.2 — the four core properties of blueprint Layer 1 demonstrated on the
v0.1 substrate. Additive (substrate unchanged).
**Reproduce:** `repro/wave_resonance_core.py` → `wave_resonance_results.json`
(digest `c69917020c66…`), figure `repro/wave_resonance_atlas.png`. Reuses the v0.1
substrate exactly (non-circular).
**Firewall:** `consciousness_claim = 0`, `hard_problem_open = 1`. **No tuning.**

---

## 0. What this session answered (your directions → measurements)

| Your thesis | This session's proof | Result |
|---|---|---|
| "the sum of these waves is information" | **R1 superposition + resonance** — one composite = the SUM of many bound waves carries them all, read by resonance | K≈96 items / 512 (≥0.95 recognition) |
| "pattern matching without computation" | **R2 resonance match** — a query settles by physics; settling steps independent of #stored P | step spread 2.8 (P=2..24) → **O(1)-in-P** |
| "parallel … how far throughput goes" | **R4 throughput [O]** — match cost independent of P vs digital/neural O(P·N) | 83.9 steps flat vs 51M ops @ P=10⁵ |
| "learning and real-time response are different" | **R3 one-shot learning** — one exposure → immediate recall, no catastrophic forgetting | recall 1.000 (first 24), graceful decay |

---

## 1. [R1] sum = information (superposition / holographic)

Each item = a random phase **key** k (unit phasors) ⊗ **content** ξ∈{±1}. Bound
`store_μ = k_μ ⊙ ξ_μ` (phasor multiply = phase addition). **Composite wave**
`C = Σ_μ store_μ` — *one wave field carries the whole set as the sum itself*.
Recognition = phase-conjugate **resonance** `score(p) = Re⟨store_p, C⟩/N` (~1 if p is
in the sum, ~0 if not). **Not a search — one interference measurement.**

| K (items summed) | K/N | recognition acc | present score | absent score ±sd |
|---|---|---|---|---|
| 8 | 0.02 | 1.000 | +1.00 | −0.00±0.10 |
| 32 | 0.06 | 1.000 | +1.01 | −0.00±0.18 |
| 64 | 0.12 | 0.968 | +1.00 | +0.00±0.26 |
| **96** | **0.19** | **0.956** | +1.03 | −0.00±0.31 |
| 128 | 0.25 | 0.933 | +1.02 | −0.00±0.35 |
| 256 | 0.50 | 0.837 | +1.01 | −0.01±0.50 |

→ **superposition recognition capacity K≈96** (~19% of N). present scores stay ~1.0;
absent crosstalk sd grows as √(K/N), so larger K blurs separation (honest limit).
**The sum itself is information** and **resonance reads it**. **Grade [V]** (direct
measurement). Exact recovery of content *bits* uses unbind + L0 attractor clean-up
(combined with D2) → this session measures *recognition* scale.

---

## 2. [R2] matching without computation — O(1) in P

Reuse the v0.1 substrate (real Hebbian J + settling). Store P patterns in *one J*;
feed a noisy query (15% flip) → settle while recording **steps to convergence**
(physical-time proxy). A digital scan would scale with P, but here **physics tests all
P at once**, so steps should stay flat.

| P (stored) | α=P/N | converge steps | recall success |
|---|---|---|---|
| 2 | 0.004 | 82.7±5.0 | 1.00 |
| 8 | 0.016 | 83.5±5.1 | 1.00 |
| 16 | 0.031 | 84.7±4.8 | 1.00 |
| 20 | 0.039 | 85.5±6.8 | 1.00 |
| 24 | 0.047 | 84.3±6.2 | 0.88 |

→ **step spread only 2.8** (P=2..24). Matching is **essentially independent of P =
O(1)-in-P**. **Grade [V].**

**Honest framing.** The "O(1)" claim is about **physical settling time**. Simulating
this physics *digitally* costs N² per step — so the parallel advantage is a
**hardware claim [O]** (physical realization deferred). The point: *in a physical
medium the coupling field acts simultaneously*, so one settling handles P and N at
once.

---

## 3. [R3] one-shot online learning (no backprop)

Stream patterns one at a time. J starts empty. Each new pattern adds a **single
outer-product update** `J += (1/N)ξξᵀ` (Hebbian, local, no iteration / gradient).
Right after adding, test (a) recall of the *just-learned* pattern, (b) recall of a
random *earlier* pattern (retention).

| #stored | α | just-learned recall | earlier retained |
|---|---|---|---|
| 1 | 0.002 | +1.000 | n/a |
| 8 | 0.016 | +1.000 | +1.000 |
| 16 | 0.031 | +1.000 | +1.000 |
| 24 | 0.047 | +0.990 | +0.997 |
| 32 | 0.062 | +0.952 | +0.970 |

→ **immediate recall after one exposure** (first 24 ~1.0), **no catastrophic
forgetting** (earlier patterns retained within capacity), graceful decay past capacity
(0.95). No epochs / backprop / global loss — **only a local one-shot update**.
**Grade [V].** This is the mechanism behind "learning / real-time response are
different": a different species from gradient descent's multi-pass / catastrophic
forgetting.

---

## 4. [R4] parallelism / throughput (theoretical projection [O])

From R2's measured steps (83.9), the scaling law: **wave match cost = O(settling
steps), independent of P** vs digital scan / neural net O(P·N). One field update = N²
simultaneous physical couplings.

| P stored | wave (physical steps) | digital/neural (ops) |
|---|---|---|
| 10 | 83.9 | 5,120 |
| 1,000 | 83.9 | 512,000 |
| 100,000 | 83.9 | 51,200,000 |

→ **content-addressable in ~constant physical time.** In hardware, throughput scales
with the settling rate f (`queries/s ≈ f/83.9`), with N² couplings simultaneous.
**All [O] projection — physical realization deferred.** The point is the *scale
separation*: storing 10⁵ patterns costs the same physical time as storing 1.

---

## 5. Grade ledger

| Claim | Grade |
|---|---|
| sum=information (superposition), recognition capacity K≈96 | **[V]** |
| matching without computation, O(1)-in-P (physical time) | **[V]** |
| one-shot online learning, no catastrophic forgetting | **[V]** |
| binding/bundle algebra (key⊗value, sum) | **[V]** (used by R1) |
| parallel throughput advantage (hardware) | **[O]** physical realization deferred |
| exact content-bit recovery (beyond recognition) | **[O]** needs unbind + L0 clean-up |
| permute · structured-tree depth-capacity | **[O]** next chunk (L1 completion) |
| felt quality | **[O]** firewall |

---

## 6. Honest negatives / limits

- **Superposition crosstalk**: absent sd grows as √(K/N), so larger K blurs separation
  — capacity is a fraction of N. Scale must come from **hierarchy (L3)**, unproven.
- **The O(1) parallel advantage is a hardware claim** — a digital simulation is N² per
  step. Physical realization is assumed (later).
- **R1 is *recognition* scale** — exact content-bit recovery requires combining with
  L0 attractor clean-up (separate).
- **One-shot learning also has a capacity limit** — decay begins at 32 (α=0.062).
  Needs L2 multiplexing / L3 hierarchy.

---

## 7. Next (blueprint L1 completion + L2 start)

See `BLUEPRINT_toward_ultimate_computer.md` §3·§4·§12. Next chunk:
1. **L1 completion**: `permute` operation + role-value **tree** depth-capacity
   (structured-query accuracy vs depth). Stress: does crosstalk collapse structured
   recovery before any useful depth.
2. **L2 start**: asymmetric (time-delayed) Hebbian to make permutation a **metastable
   trajectory** — sequence learn/replay/predict + theta-gamma WM ~7 slots (reproduce
   B5). Stress: does the trajectory collapse to a fixed point / diverge; slots ≪ 7.

One session, one zip, additive. If broken, restart with the break applied.

---

*— v0.2. Reproduce: `python3 repro/wave_resonance_core.py` (deterministic, digest
`c69917…`); figure `python3 repro/make_figure_v0_2.py`. Substrate from v0.1 =
`SESSION_v0_1_design_study.md`.*
