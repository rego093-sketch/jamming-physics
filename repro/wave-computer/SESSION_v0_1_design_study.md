# SESSION v0.1 — design study (substrate L0)
## A wave-substrate computer that stores / computes / patterns with phase itself

**Status:** v0.1 — the four core properties of the substrate proven in-silico. Not
hardware (design + proof).
**Inherits:** brain `vp_frontal v2` (B1–B5) + physics `vp_physics v0.11.0` (P1–P3).
Detail → `INHERITANCE_MANIFEST.md`.
**Firewall:** `consciousness_claim = 0`, `hard_problem_open = 1`. Function only.
**Discipline:** no tuning (`new_tuned_constants = 0`), every claim with a sweep,
honest negatives recorded.
**Reproduce:** `repro/wave_compute_core.py` → `wave_compute_results.json`
(digest `e9fdd3bc…`), figure `repro/wave_compute_atlas.png`.

---

## 0. One-line thesis

> **A bit is a static 0/1. A wave carries information in its phase θ.** The brain
> computes reliably with noisy, unreliable neurons by putting information in **phase,
> not amplitude**, doing computation as **medium relaxation, not clocked
> fetch-execute**, and operating in a **metastable band below full coherence**. The
> decisive payoff of these three is one thing — **physics-level error correction** —
> so a wave machine communicates and computes in noise that would break a digital one
> (D4: **BER ≈ 0.03% at negative SNR −2.3 dB, 22% raw bit errors**). This is not a
> faster digital computer; it is a **different machine species**.

---

## 1. Thesis: why a wave is a better compute primitive than a bit

A digital computer's primitive is a **static bit** — information is in the signal's
**amplitude**. Additive noise corrupts it directly: SNR is the limit; error
correction is bolted on top.

The brain's primitive is an **oscillation** — information is in the **relative phase**
of rhythms. This is better for physical reasons:
1. **Phase is a collective property.** Even if one oscillator is buried in noise, the
   collective phase averages noise away.
2. **Attractors pull errors back.** If a stored phase pattern is a stable point, a
   noise-perturbed state is *physically* drawn back to the nearest pattern — error
   correction for free.
3. **Phase locking is a threshold phenomenon.** As long as coupling beats noise, the
   lock does not break continuously.

All three are what `vp_frontal v2` confirmed in the brain in-silico (B1–B4). This
study moves them to a *machine* and runs them.

---

## 2. The substrate: near-field-coupled oscillators, clock-free, at the metastable edge

The substrate is a **field of phase-coupled oscillators**.
- **State**: phase `θ_i` of each oscillator. **One datum = one standing phase
  pattern.**
- **Medium (coupling field)**: a symmetric Hebbian matrix `J` — the in-silico analog
  of the ephaptic near-field (B1, P3). Coupling is **by field**, not digital wiring;
  its spatial form is the 1/r² near-field Green function (P3).
- **Dynamics**: gradient descent on the phase energy
  `E(θ) = −½ Σ_ij J_ij cos(θ_i − θ_j)` →
  `dθ_i/dt = Σ_j J_ij sin(θ_j − θ_i)`. Its **minima are the stored patterns**
  (continuous / wave-form associative memory; XY/Kuramoto form).
- **clock-free (P2)**: no global clock. **Time = the settling itself.** No
  fetch-execute — computation is physics. Same as the brain self-timed by its rhythms
  (B2) and the jamming lattice propagating clock-free (P2).
- **medium stiffness `g` (P1)**: the coupling-field gain `g` plays the role of medium
  stiffness (B in `c²=B/ρ`); it sets the operating band (§3 D3).

**Core scheme — all three operations come from the same medium, same dynamics:**

| Operation | Digital machine | Wave substrate (this design) |
|---|---|---|
| **store** | write a bit to a cell | **sculpt an attractor** in the field J → datum = standing phase pattern |
| **compute** | clocked fetch-execute | **relaxation** of the phase field → to the nearest attractor = pattern completion |
| **pattern** | a separate circuit | the **metastable band** supports coexisting phase patterns |
| **communicate** | amplitude code + bolt-on ECC | **phase code + attractor correction** (physics-level) |

---

## 3. The three operations — each demonstrated

Every claim is a number from an actual sweep (not prose). Figure
`wave_compute_atlas.png`. Simulation: N = 256 oscillators, deterministic (fixed seed
19), no tuning.

### 3.1 [D1] store — store a wave (datum = attractor)

Store P random ±1 patterns in the Hebbian field; cue each cleanly → settle →
**reproduce the stored pattern (overlap ≥ 0.95)** = success. Recall vs load `α = P/N`:

| α (=P/N) | P | clean-cue recall |
|---|---|---|
| 0.02 | 5 | **1.000** |
| 0.04 | 10 | **1.000** |
| 0.06 | 15 | **0.989** |
| 0.08 | 20 | 0.558 |
| 0.10 | 26 | 0.109 |
| 0.14 | 36 | 0.000 |

→ **storage capacity `α_c ≈ 0.06`** (~15 patterns / 256 oscillators), consistent with
known continuous (XY) associative-memory capacity (below discrete Hopfield 0.14 —
the continuous phase memory is "softer"; §6 honest limit). **Grade: [V]** storage /
capacity (direct measurement, matches known theory).

### 3.2 [D2] compute — compute with waves (pattern completion = settling physics)

Feed a **corrupted cue** of a stored wave (flip some bits + phase jitter), settle →
how much is recovered. Overlap before vs after settling (α=0.06):

| corruption (fraction of bits flipped) | cue (before) | recovered (after) |
|---|---|---|
| 0% | +1.000 | +0.994 |
| 5% | +0.898 | **+0.995** |
| 10% | +0.797 | **+0.968** |
| 15% | +0.703 | **+0.958** |
| 20% | +0.602 | **+0.965** |
| 25% | +0.500 | +0.887 |
| 30% | +0.398 | +0.876 |
| 35% | +0.297 | +0.639 |
| 40% | +0.203 | +0.394 |
| 45% | +0.102 | +0.096 |

→ **critical corruption ≈ 20%**: flip 1/5 of bits and still fully recover (≥0.95).
Inside the basin, settling yields output *cleaner than the input* = **physics-level
error correction**. Outside the basin (≳40%), recovery fails (honest negative: 45% →
0.10). **Grade: [V]** pattern completion (non-circular — the recovered target is the
whole pattern, not the flipped bits).

Why this is "computation": no fetch-execute, no instructions. **The physics of an
input phase state settling to the nearest stored attractor** is content-addressable
recall / constraint satisfaction / pattern completion.

### 3.3 [D3] pattern regime — computation lives below full coherence

Sweep the medium-stiffness gain `g` and read recall (computation) and the global
order parameter `R` (15%-corrupted cue, α=0.06):

| gain g | recall overlap | global R |
|---|---|---|
| 0.00 (field OFF) | +0.703 | 0.043 |
| 0.25 | +0.944 | 0.049 |
| 0.50 | **+0.996** | 0.044 |
| 1.00 | +0.965 | 0.059 |
| 2.00 | +0.940 | 0.049 |
| 4.00 | +0.860 | 0.045 |
| 8.00 | +0.832 | 0.061 |

Two things appear:
1. An **interior optimum** (g ≈ 0.5); **field OFF (g=0)** has no stored structure so
   recall sits at cue level; **over-drive (g≫1) degrades** computation. This is
   *qualitatively the same structure* as the brain's Gap-1 **interior peak +
   over-drive collapse** (access peaks in the interior, collapses when over-driven).
   The over-drive decline in this minimal model is *gentle* — unlike the brain's
   sharper turnover (honest difference).
2. **Global R stays ~0.05 throughout.** This is not a defect but the **signature of
   distributed information**: balanced ±1 patterns put half the phases at 0 and half
   at π → they cancel in the global mean → R≈0. If R=1 (full sync) all phases are
   equal = one pattern = **only one storable state** = zero memory. **So R must be
   low for many patterns to coexist.** The brain running at R=0.39 (not full sync) is
   *the same lesson at whole-brain scale* — to compute, stay *below* full coherence
   (B3).

**Honest statement:** this substrate's global R (~0.05) is **not claimed to
reproduce** the brain's R=0.38961. They are different order parameters at different
scales (N=256 phase memory vs the 12-organ ephaptic ring). **The principle ("compute
below full coherence") is inherited and demonstrated** — the number is not
transferred. **Grade: [L]** locked to the metastability principle (cited + qualitative
demonstration); number match not claimed → **[O]**.

---

## 4. [D4] communication through noise — "communication works even with heavy noise"

Transmit an N-symbol codeword through additive white Gaussian noise (AWGN), recover.
Compare three schemes at **matched energy** (`E_s = 1`). Codewords = stored attractor
patterns (a structured code the receiver knows).
- **phase (BPSK)**: bit → phase {0, π} → symbol `x = e^{iθ} = ±1`.
- **amplitude (OOK)**: bit → amplitude {0, A}, with `A = √2` for equal mean energy.
- **phase + attractor clean-up**: feed decoded phases back into the receiver's
  attractor field and settle → physics correction.

Bit error rate (BER) vs noise σ (SNR in parentheses):

| σ (SNR) | amplitude OOK | phase BPSK | **phase + clean-up** |
|---|---|---|---|
| 0.30 (+10.5 dB) | 0.0079 | 0.0002 | **0.0000** |
| 0.50 (+6.0 dB) | 0.0806 | 0.0210 | **0.0000** |
| 0.70 (+3.1 dB) | 0.1562 | 0.0721 | **0.0000** |
| 0.90 (+0.9 dB) | 0.2125 | 0.1310 | **0.0000** |
| 1.10 (**−0.8 dB**) | 0.2571 | 0.1870 | **0.0000** |
| 1.30 (**−2.3 dB**) | 0.2979 | 0.2239 | **0.0003** |
| 1.50 (**−3.5 dB**) | 0.3136 | 0.2513 | 0.0044 |

Three conclusions:
1. **Phase beats amplitude at every noise level** (BPSK ~3 dB better than OOK at
   matched energy — textbook, and the simulation matches the closed-form Q-function:
   e.g. at σ=0.5, BPSK sim 0.021/thy 0.023, OOK sim 0.081/thy 0.079). Carrying
   information in phase rather than amplitude is more robust — **a mechanical proof of
   why the brain uses phase coding**.
2. **A structured phase code + attractor clean-up is ~error-free at *negative SNR*.**
   At −0.8 dB (noise > signal, raw BER 19%) clean-up gives **BER = 0**; at −2.3 dB
   (raw 22%) still **0.03%**. As long as corruption is inside the basin, physics
   erases the errors. → **your thesis "communication works even with heavy noise" is
   demonstrated end-to-end.**
3. **Outside the basin, clean-up also fails** (rises to 0.44% at −3.5 dB) — an honest
   limit. It does not beat unbounded noise, but it pushes reliability far past the
   digital (SNR) limit.

**Grade: [V]** phase > amplitude (matches theory, sign-stable throughout) + attractor
clean-up's negative-SNR reliability (in-silico).

---

## 5. Grade ledger

| Claim | Grade | Basis |
|---|---|---|
| phase-pattern storage (datum=attractor), capacity α_c≈0.06 | **[V]** | D1, matches XY associative-memory theory |
| pattern completion by settling (critical corruption ~20%) | **[V]** | D2, non-circular read-out |
| phase coding > amplitude coding (matched energy) | **[V]** | D4, matches closed-form Q-function |
| attractor clean-up → reliable comms at negative SNR | **[V]** | D4 in-silico |
| near-field coupling medium (ephaptic analog) | **[L]** | B1·P3 cited, J is its analog |
| clock-free self-timing | **[L]** | P2 cited, computation = settling |
| compute below full coherence (metastable) | **[L]** | B3 cited + D3 qualitative |
| medium wave `c²=B/ρ` sets speed/bandwidth | **[L]** | P1 cited (principle), g as stiffness |
| reproduce the brain R=0.39 *number* | **[O]** | not claimed — different scale/order parameter |
| theta-gamma multiplexing (capacity~7) | **[O]** | B5 cited only, not built (roadmap) |
| physical hardware | **[O]** | v0.1 is a math substrate, no device selected |
| arbitrary algorithms (general-purpose) | **[O]** | native to association/CSP/completion, not general |
| felt quality (hard problem) | **[O]** | firewall. `consciousness_claim=0`, `hard_problem_open=1` |

---

## 6. Honest negatives / what is NOT shown

- **Density is not yet competitive.** α_c≈0.06 is below digital memory density and
  below discrete Hopfield (0.14) — continuous phase memory is softer. **The win is
  noise immunity / content-addressable completion, not density.** That trade-off is
  stated plainly.
- **No number match** (§3.3): the brain's R=0.39 is not transferred. Principle only.
- **The receiver must know the codebook** to clean up (D4). Not unconditional
  correction of arbitrary bit strings — correction of a *structured code* (as the
  brain corrects learned representations).
- **Not general-purpose.** This substrate does not natively run *arbitrary functions*.
  Native operations are **settling / completion / constraint satisfaction /
  associative recall**. Not a general replacement for digital logic — a *different
  species*.
- **Theta-gamma multiplexing not built** (B5) — the key brain mechanism for raising
  capacity by phase-slot multiplexing is roadmap [O].
- **Physical medium not selected.** Which medium (photonic / spintronic / acoustic /
  superconducting oscillators) is §7 [O].
- **Energy / speed / scaling vs CMOS not analyzed.** Out of v0.1 scope.
- **Firewall**: function only. Not consciousness — left open by principle
  (`hard_problem_open=1`).

---

## 7. Roadmap (next program)

See `BLUEPRINT_toward_ultimate_computer.md`. Immediate next: theta-gamma multiplexing
(L2), metastable sequence computation, physical-realization candidate comparison,
hybrid architectures, and the inherited Stress Principle applied to every new claim.

---

*— vp_wave_computer v0.1 design study. Reproduce: `python3 repro/wave_compute_core.py`
(deterministic, digest `e9fdd3bc…`); figure `python3 repro/make_figure.py`.
Inheritance → `INHERITANCE_MANIFEST.md`.*
