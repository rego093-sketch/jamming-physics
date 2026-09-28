# MM2 — theta-locked hippocampal module

**Question.** Coupled oscillators whose natural frequencies are spread out (dispersed cortical inputs) lose associative recall. Mind §MW claims that recall happens inside the hippocampus, where every input is locked to one theta carrier. Does that locking rescue recall? And does the memory content still come from the stored couplings, not from the locking?

**Model.** This uses the unmodified `wave_compute_core` (`hebbian_field`, `pattern_to_phase`, and the same Euler step as `relax`). Two terms are added and written in the frame of the theta carrier. Carrier invariance lets the carrier itself drop out.

    dθ_i/dt = Δω_i + Σ_j J_ij sin(θ_j − θ_i) − κ sin(2θ_i)

- **Δω_i ~ N(0, σ)** is each unit's frequency offset from the carrier. It models the dispersion.
- **κ** is the strength of theta locking.
  - The second-harmonic form locks *frequency* to theta.
  - It keeps both stored phases (0 and π relative to theta) stable, so it favours neither bit.
  - This form is a modelling choice and is graded [H].
- **Identity check.** With σ = κ = 0 the update is identical to `relax` (`identity_with_core: true`).

**Setup.** Setup was pre-registered in `PREREG.json` before the run.
- 256 units in 4 blocks, with 15 stored episodes.
- 2 congruent cue blocks with 0.8 rad jitter.
- 40 fresh seeds: 6000–6039. The exploratory seeds 1000–1029 are excluded.
- Readout is the phase-invariant sign overlap; recall counts as a success when it is ≥ 0.9.

## Result: all five predictions PASS

| Prediction | Condition | Recall |
|---|---|---|
| P1 collapse | σ = 0.4, no locking | **0 %** |
| P2 rescue | σ = 0.4, κ = 0.3 | **82.5 %** |
| P3 content from memory | σ = 0.4, κ = 0.3, **J = 0** | **0 %** |
| P4 over-locking | σ = 0, κ = 0.8 | **0 %** |
| P5 amplification survives | σ = 0.4, κ = 0.3, 1 → 4 congruent cues | 10 → 82.5 → 95 → 97.5 %; incongruent (4 cues) 2.5 % |

Grid (2 congruent cues):

| σ \ κ | 0 | 0.1 | 0.3 | 0.5 |
|---|---|---|---|---|
| 0.0 | 78 % | 100 % | 100 % | 40 % |
| 0.2 | 18 % | 75 % | 95 % | 88 % |
| 0.4 | 0 % | 0 % | 83 % | 93 % |
| 0.6 | 0 % | 0 % | 8 % | 58 % |

## What it means

1. **Dispersion kills recall, and theta locking restores it.** This is the mechanism mind §MW proposed. The global coherence of R ≈ 0.39 between cortical regions can coexist with good recall inside a theta-locked hippocampus.
2. **Locking carries no content.** Without stored couplings, locking recalls nothing (P3). The memory is in the synapses; theta only makes them readable.
3. **There is a working window.** Locking must be stronger than the frequency spread and weaker than the associative (memory) field. Locking that is too strong freezes every unit onto theta, noise included, and recall fails (P4; σ = 0 with κ = 0.5 already drops to 40 %). This window is a testable prediction: phase locking to theta should help memory up to a point, and hyper-synchronous theta should impair it.
4. **Multimodal amplification (MM1) survives dispersion** once the inputs are theta-locked (P5).

**Grade.** [V mech]: reproduced inside the model under a pre-registered test that could have failed. The identification with the brain is [H], and so is the form of the locking term. The in-vivo measurement of theta phase-locking against recall is literature [L], not this code; see mind §MW.

Run: `python3 mm2_run.py` (about 30 s, deterministic).
