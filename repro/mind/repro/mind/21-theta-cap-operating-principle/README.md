# Chapter 21 — Operating principle + physical-feasibility review

**Status (v1.32):** operating principle **[F]** forced by VC1–VC5; physical feasibility **[O]**
open (literature review, no engine claim). **efficacy = 0 · NOT medical advice · not a dosing
protocol.**

## The forced operating mode
If a θ-cap is to supply the W-axis function at all, the dynamics pin the mode on all sides:
- **Floor (VC1).** Below the window the cap does nothing; only C-FORCE routes (inj 0.08–0.10).
- **Ceiling (VC5).** Above the window the adverse over-sync fraction rises monotonically
  (0.14 → 0.57 → 0.99 → 1.0 → 1.0) and is minimised at the window; a *fixed* amplitude
  over-syncs milder cases (FINDING-VC5c), so amplitude must be **matched to the deficit**.
- **No banking (VC2).** No plasticity ⇒ no carryover; intermittent dosing reverts to the deficit.
- **Sustainable (VC3).** Continuous duty-shaped operation is molecularly safe below the fold.

⇒ **minimum-effective, deficit-matched, continuous.** A wearable drug with no half-life past removal.

## Physical feasibility = OPEN
Every *component* exists in research form today — θ-band tACS; closed-loop phase-locked
EEG-tACS; multi-electrode phase-shifted montages built to alter long-range connectivity
(in-phase coordinates, anti-phase disorganises); individualised MRI-optimised targeting;
wearable home delivery — but the **specific assembly** (individualised + phase-structured +
amplitude-windowed + network-targeted + continuous) does **not**. Four obstacles keep it [O]:
(1) no in-vivo readout of the wiring deficit to set the matched amplitude; (2) the narrow
window risks over-sync (seizure analogue); (3) spatial targeting of broken long-range edges at
depth; (4) the plasticity sign is phase-dependent (wrong phase depotentiates). Feasibility of
the apparatus is **not** evidence of benefit.

## Reproduce
```
cd ../_verify && python3 run_all_vc.py
```
Grounding: VC1 `eae5e190…` (floor), VC2 `51362445…` (drug principle), VC3 `d045928f…`
(continuous safety), VC5 `527ee1df…` (ceiling / deficit-matching).

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1.
