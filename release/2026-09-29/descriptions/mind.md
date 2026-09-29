## Summary
Felt Cognition is a functional model of the stream of thought. It inherits one premise from `wave-computer`: carrier-invariant phase computation, which is a possibility result only, and no numbers cross. It also inherits the neuron, rhythm and working-memory layer from `neuro`, and the γ ruler and atlas from `dna`. Its one added module is felt cognition on attractors: an engram is a bistable attractor, mood is a persistent switch, and the stream of thought is a serial selection among γ-eddies. The headline is now "memory from waves": the brainwave is a carrier, sensory low-frequency cues set relative phase, and the hippocampus sums congruent cues. In the claims ledger this headline is an **interpretation**. The pre-registered in-model predictions passed ([V mech]; MM1 recall 35/78/88/90% for 1–4 congruent cues, and 3–5% with mixed cues). No human data has yet been compared quantitatively; the literature support ([L]) is qualitative. Carrier invariance itself is an **identity**. The global coherence R ≈ 0.39 and working memory ≈ 6.1 are **anchor restatements**. The biology reading rule applies. Statements are observation, code output (input dependence stated), consistency check or interpretation. Building-layer claims are [O] per `dna` §RB. Disease-lever chapters give corrective direction only, never a magnitude.

## What changed in this version (2026-09-29)
**Corrections**
- New premise chapter §MW, "Memory From Waves". It covers carrier invariance (from `wave-computer`); brainwave as carrier and sensory cues as relative phase; hippocampal summation of congruent cues; and the inheritance edges. R 0.39 is restated as global coherence, not hippocampal phase locking. The earlier headline was "stream of thought = serial select among γ-eddies".
- The brainwave is stated as quasi-static, not radiative at c; E and B follow physics Link 6a.
- Working memory f_γ/f_θ is labelled [L]. The mind engine's 6.1 depends on hand-chosen τ_inh (60/6), with a τ-dependent range of 4.4–8.0.
- The γ notations are disambiguated (f_γ, γ_DNA, engine g).
- Building-layer statements are [O] (dna §RB). The lever chapters separate the promoter threshold from the membrane threshold.
- §28: critical slowing is corrected. §29: euthymia is corrected to the h ≈ 0 hysteresis band. "Causal" is withdrawn for the R anchor, and the depressive < euthymic < manic ordering is labelled model sweep output.
- §20 and §21 are marked as superseded by §26. §23 is labelled "synthetic cerebra".
- The organ-emergence chapter carries the reading-vs-building note: γ-order is superseded, order comes from cascade depth, and building is [O].

**New experiments and results**
- MM1, multimodal cue amplification (pre-registered, run on the wave-computer core): PASS [V mech]. Recall rises from 35% (1 congruent cue) to 90% (4 cues); mixed cues give 5% (interference PASS).
- MM2, theta-locked hippocampal module (pre-registered, 40 new seeds): 5/5 PASS [V mech].
  - At dispersion σ = 0.4, recall is 0% without locking and 82.5% with locking (κ = 0.3).
  - Removing the stored couplings gives 0%, so locking carries no content.
  - Over-locking (κ = 0.8) gives 0%, which defines a working window.
  - Multimodal amplification survives dispersion: 10% → 97.5% with 1 → 4 congruent cues, 2.5% incongruent.
- A human-literature section was added to §MW 5a ([L], qualitative):
  - Rutishauser 2010 (theta phase locking predicts memory);
  - Lehmann & Murray 2005, Thelen 2015 and Shams & Seitz 2008 (congruent multisensory benefit);
  - Clouter 2017 and Wang 2018 (4 Hz phase-synchronous associative memory).

**Relabelled grades / reading rule**
- A [V mech] legend was added: reproduced in the model, not against external data. WM → [L].
- Gates that are true by construction are relabelled [F]:
  - §48–§50 (K3 L = R/R_anchor, C1, T1);
  - hysteresis = 2·spinodal;
  - §29 drive = spinodal(g).
- Correction notes were added on 51 pages (hub + 50 chapters).

**Reproduction package changes**
- The MM1 and MM2 experiment packages are shipped under `repro/wave-computer/experiments/`, because this volume inherits them.
- 55 repro links were fixed.

**Site/metadata**
- The corpus DAG now has physics → wave-computer → mind, neuro → mind and dna → mind. Seam edges +2; manifest, `_decl` and AGENTS were updated; gate_shared_infra is REQUIRED PASS.
- The manifest and homepage headline were regenerated.
- The hub TOC gained §30–§50. Five `<` characters were escaped.
- The corpus link audit repaired stale links.
- Highwire citation meta was added to the hub.
- Corpus integrity checks were added to the gate.
- Earlier site-assembly snapshot commits ("VP Theory site", "Final", "1111111", June 2026) included dropping dangling font preloads and fixing 2 stale mind links. No claim changed.

## Claim status (claims ledger)
Counts: interpretation 2 · identity 2 · anchor-restatement 2 (independent-prediction 0, open 0).
- Memory from waves: a brainwave carrier plus congruent cues summed in the hippocampus — interpretation — in-model [V mech], pre-registered (MM1 35/78/88/90%; mixed 3–5%). No human data compared quantitatively.
- Carrier invariance: bit-identical recall at carrier ω 0, 1, 10, 100 — identity — holds by construction ([F] in-model).
- Frequency dispersion limit and theta-lock window — interpretation — recall 0.85 → 0.21 as σ_ω/K goes from 0 to 0.59; MM2 lock 82.5%, no lock 0%, over-lock 0% (in-model).
- Global coherence anchor R ≈ 0.39 — anchor-restatement — frozen engine anchor (0.38961455; a second value, 0.3283, appears in §14). "Causal" is withdrawn.
- WM θ/γ ≈ 6.1 in the mind engine — anchor-restatement — τ-dependent, 4.4–8.0.
- Gates §48–§50, hysteresis = 2·spinodal, §29 drive = spinodal(g) — identity — cannot fail; relabelled [F].

## Open items
- Same-subject quantitative comparison of hippocampal theta locking (PLV) against recall accuracy (data-pending).
- A recall curve over the number of cue modalities, measured within one design (data-pending).
- The over-locking side (hypersynchronous theta → memory damage) [O].
- The missing `THETA_CAP_VIRTUAL_CLINICAL_HONEST.md`, and recomputation of the gate `tree_ok` (flagged by the review).
- The hard problem and felt experience remain an open frontier.
- Building-layer claims [O] (dna §RB).
- Clinical magnitudes are withheld [O]; lever chapters give direction only.

## Reproduction
The ZIP contains `docs/mind/` (the published HTML pages), `repro/mind/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- Engine: `cd repro/mind/repro/mind/_engine && python3 run_all.py`. This recomputes the emergence and checks it against `expected_sha256.json`.
- Regression: `cd repro/mind/repro/mind/_verify && python3 run_regression.py`, which checks bit-identity and mechanism invariants at SEED = 19.
- Boundary and terminology locks: `python3 verify_boundary.py` and `python3 verify_terminology.py`, both run from `repro/mind/`.
- The inherited MM1 and MM2 experiments: `repro/wave-computer/experiments/MM1_multimodal_amplification/mm1_run.py` and `repro/wave-computer/experiments/MM2_theta_locked_hippocampus/mm2_run.py`.
- No network access is needed. Promoter γ inputs are cached.

## Citation and links
- Site: https://jamming-physics.org/mind/
- Concept DOI: 10.5281/zenodo.20694404
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
