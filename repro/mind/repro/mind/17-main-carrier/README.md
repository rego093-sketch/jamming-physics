# Chapter 17 — Main High-Frequency Carrier (M16)

**Status (v1.19):** PROMOTED into the engine as **M16**. This chapter verifies that the
promoted engine reproduces the carrier result bit-for-bit and that the original study's
13 gates still pass on it.

## What M16 is
The sleep dissociation (deep SWS has the largest delta yet is least responsive) forces the
access-correlated wave to be **not** raw amplitude but the structured **high-frequency
carrier** present in wake/REM and suppressed in deep SWS. M16 emerges that carrier from its
**measured** source (GABA_A τ = 6.0 ms, Destexhe 1998; PV fast-spiking gamma generators),
tracks its activity range (Stage A), its state-selectivity — structured-fast beats
large-unstructured-slow (Stage B), its metastable operative window vs silence / global-sync
(Stage C), and how many carriers run in **parallel** with content **reinstated** from the
slow index (Stage D), plus the honesty ledger (Stage E).

## Provenance / promotion
- Ported **verbatim** from `_consciousness/vp_main_carrier_emergence.py` (helpers prefixed
  `_mc_`, data path adapted); the standalone study is kept as the **pre-promotion freeze**
  (headline `8d05cfec…`).
- The engine's M16 reproduces that exact headline (`8d05cfec…`), so every gate input and
  invariant matches the study bit-for-bit.
- **No new tuned constant.** The carrier τ is the measured GABA_A value; the slow leg of the
  carrier : slow ratio is the engine **[O]** `tau_inh = 60` — the theta-pacing anchor is
  **OWED [O]** (see `_consciousness/theta_pacing_anchor_status.py`, Task 2B).

## Invariants (11, frozen)
carrier_over_slow_ratio 6.125 · parallel_capacity_slots 6 · recall_structured_carrier 1.0 ·
big_unstructured_recall 0.7 · recall_metastable_measured 1.0 · recall_globalsync_seizure
0.69166̄ · reinstatement_fidelity_mean 1.0 · crosstalk_mean 0.49666̄ · medium_efficacy_tested 0 ·
hard_problem_open 1 · new_tuned_constants 0.

## Honest scope
M16 is a **measured-grounded measurement, NOT a consciousness claim**: medium efficacy 0,
hard problem **OPEN**, consciousness_claim 0, PCI honest negative. The carrier is a *necessary
substrate signature*, not a sufficiency proof.

## Verify
```
python3 verify_main_carrier.py
```
Exit 0 iff: (a) engine M16 headline == `8d05cfec…`; (b) the 11 engine M16 invariants match
the freeze; (c) the study reproduces the same headline and all **13/13** gates pass; (d) the
always-run regression locks the same `mc_*` carrier invariants.
