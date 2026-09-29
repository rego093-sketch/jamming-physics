## Summary
Wave Computer is a design study of a clock-free computer in which information is carried by oscillator phase and the computation is the physics settling to a fixed point (layers L0–L9, with the hard problem of consciousness declared open). It inherits only from `physics` (P2, clock-free settling on the jammed substrate) plus literature principles (Kuramoto; Hopfield 1982; Lisman & Jensen 2013). In this version, citations of `mind` (R = 0.39) and `neuro` (6.125) are withdrawn as inheritance; they were only ever metadata. The one module it adds is clock-free phase computation. The headline is now stated as the premise that `mind` uses: phase computation depends only on phase differences, so it is carrier-invariant and low-frequency thought is possible. In the claims ledger this is an **identity**: a common carrier frequency cancels in the rotating frame, so it holds by algebra and has no external residual. Its stated limit is frequency dispersion. Recall holds only while σ_ω ≲ 0.1–0.2 K. The broader thesis ("compute by phase") is ledgered as an **interpretation**: it was tested only inside the model, and no hardware or brain data is compared.

## What changed in this version (2026-09-29)
**Corrections**
- The headline was restated as a premise: carrier invariance (identical recall at ω = 0, 1, 10, 100; speed set by the coupling K) together with its limit from frequency dispersion. The earlier headline was "compute by phase on a clock-free wave medium".
- Inheritance was re-sourced to physics plus literature principles. B1–B5 now rest on neuro §19 (ephaptic coupling), Kuramoto, Hopfield 1982, and Lisman & Jensen 2013. The mind anchor (R = 0.39) and the theta–gamma capacity (6.125) enter no computation and are withdrawn as inheritance.
- B5 attribution corrected. The engine's 6.125 uses g = 1.0; with the FOXG1 DNA γ = 1.4737 it would be 7.23. Working memory is now cited as f_γ/f_θ ≈ 6–7 [L] from `neuro`.
- The "Miller 4–9 [V]" working-memory landing is regraded [O]. It depends on the input slot count and on a chosen jitter σ = 1.2 rad, and stays [O] until γ phase jitter is measured. The min(slots, precision) law is [V mech].
- P1 ("g plays B") and P3 (1/r²) are regraded as analogies [H].
- A grade legend was added. [V mech] means reproduced in the model with deterministic seeds; it is not [V data]. Closed-form identities and results true by construction are [F]. The brain rhythm is stated as quasi-static, not radiative (agreeing with neuro §18). The R19 switch is stated as not used in this volume.
- The hub's dispersion note now points to MM2.

**New experiments and results**
- MM1, multimodal cue amplification on the wave-computer core (pre-registered): PASS [V mech]. Recall rises from 35% with 1 congruent cue to 90% with 4. Four mixed or incongruent cues give 5% (interference PASS). The effect depends on load: recall fails at load ≥ 0.10. The biological reading is [H], with no human data.
- MM2, theta-locked hippocampal module (pre-registered, 40 new seeds): 5/5 predictions PASS [V mech]. At σ = 0.4, recall is 0% without locking and 82.5% with locking (κ = 0.3). Removing the stored couplings (J = 0) gives 0%, so locking carries no content. Over-locking (κ = 0.8) gives 0%, so locking works only inside a window. Multimodal amplification survives dispersion. The second-harmonic locking form is a modelling choice [H].

**Relabelled grades / reading rule**
- Miller landing [V] → [O]; P1 and P3 → [H]; the [V mech] vs [V data] distinction introduced; identities → [F].

**Reproduction package changes**
- `repro/wave-computer/experiments/MM1_multimodal_amplification/` and `repro/wave-computer/experiments/MM2_theta_locked_hippocampus/` were added (PREREG.json, run script, RESULT.json, README).

**Site/metadata**
- The volume was integrated into the corpus site and repository (docs + repro, 2026-09-29), together with eye, ear, nose and inheritance.
- The corpus DAG was set to physics → wave-computer → mind, with two seam edges added. The manifest and `_decl` inherits now read `physics`, and gate_shared_infra is REQUIRED PASS.
- The R19 kernel is no longer claimed by this volume in `_decl`, and its primitives were aligned.
- The homepage headline was regenerated from the manifest.
- Highwire citation meta was added to the hub (title, author, DOI, language).
- Corpus integrity checks were added to the gate: links, cited scripts and aggregate drift.
- Earlier site-assembly snapshot commits ("Final", "11111", "1111111", June 2026) carried no claim changes.

## Claim status (claims ledger)
Counts: interpretation 2 · identity 1 · anchor-restatement 1 · open 2 (independent-prediction 0).
- Information carried by oscillator phase; settling to a fixed point is the computation — interpretation — no external comparison (12 pinned in-model simulations).
- Carrier invariance ⇒ low-frequency thought possible — identity — n/a (algebra in the rotating frame; this is the only result that crosses to `mind`).
- Capability ladder L0–L8: 6/7 rungs (minimal store) and 7/7 (dual store); axioms 8 → 5 irreducible — interpretation — rungs and criteria defined in-model; ablation over 6 seeds.
- Working-memory capacity = min(slots, phase precision) lands in Miller 4–9 (~7 slots) — anchor-restatement — inside 4–9, but the slot count comes from the literature theta/gamma ratio (~7).
- MM1 congruent cues amplify recall, incongruent cues suppress it — open — in-model PASS (35% → 90%; 5% incongruent); human data pending.
- MM2 theta locking rescues recall lost to dispersion — open — in-model 5/5 PASS (0 → 82.5% at σ 0.4; no-J 0%; over-lock 0%); hippocampal data not compared.

## Open items
- Miller 4–9 landing [O] until γ phase jitter is measured.
- Human recall as a function of the number of congruent and incongruent modalities, measured in one design (data-pending).
- Same-subject comparison of hippocampal theta locking (PLV) against recall accuracy (data-pending).
- The over-locking side (hypersynchronous theta → memory impairment) [O].
- The hard problem of consciousness stays declared open (firewall: consciousness_claim = 0).
- P1 and P3 remain analogies [H]; the second-harmonic locking form is a modelling choice [H].

## Reproduction
The ZIP contains `docs/wave-computer/` (the published HTML pages), `repro/wave-computer/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- Layer results L0–L9: the `repro/wave-computer/repro/wave_*_core.py` scripts with their `*_results.json` and `expected_digest*.json` files. Verify all layers with `python3 repro/check_completeness.py`, run from `repro/wave-computer/`. The layers are deterministic and bit-for-bit.
- MM1: `python3 repro/wave-computer/experiments/MM1_multimodal_amplification/mm1_run.py` (compare with its RESULT.json and PREREG.json).
- MM2: `python3 repro/wave-computer/experiments/MM2_theta_locked_hippocampus/mm2_run.py` (compare with its RESULT.json and PREREG.json).
- SEED = 19 where a seed is used. No network access is needed.

## Citation and links
- Site: https://jamming-physics.org/wave-computer/
- Concept DOI: 10.5281/zenodo.20783570
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
