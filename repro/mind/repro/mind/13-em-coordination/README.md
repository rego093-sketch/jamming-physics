# repro/mind/13-em-coordination

REPRODUCES OFFLINE (verified mechanism). The M9 inter-organ ephaptic-coordination module is
shipped **inside the engine** (`../_engine/vp_mind_engine.py`, function `emerge_coordination()`)
and runs as part of the full emergence (`../_engine/run_all.py`). Its measured-input atlas is
`../_engine/data/brain_organ_atlas.json`. Re-checked bit-for-bit by `../_verify/run_regression.py`
and gated by `../../../tools/gate.py` (SSOT drift 0). Seed = 19, BLAS single-threaded, 2x run ->
identical sha256.

## What it emerges

Eight brain organs (neocortex, hippocampus, thalamus, striatum, cerebellum, hypothalamus,
midbrain, brainstem), coupled ONLY by the near-field that the neuro chain measured, then studied
for the coordination that emerges:

- **M9.0** near-field locality: coupling kernel ~ 1/r^3 (neuro 18), nearest-neighbour dominated
  (nn2 share ~ 0.80) -- not a global broadcast.
- **M9.1** synchronization transition: order R rises from ~0.32 (uncoupled) toward ~1.0 (full lock)
  as coupling grows; the critical fraction Kc/omega0 ~ 1.
- **M9.2** the MEASURED operating point: at kappa = 0.5496 the system sits at R ~ 0.44 with non-trivial
  variance -> a **partial / metastable** regime (neither free drift nor seizure-like global lock).
- **M9.3** cancel-vs-augment (the neuro 9/19 decisive test, in silico): cancel R ~ 0.32, measured
  R ~ 0.44 (+0.12), augment R ~ 0.54 -> the field **causally contributes** coordination.
- **M9.4** robustness: bands perturbed +/-20% keep the partial regime -> not a band-tuning artifact.
- **M9.5** communication-through-coherence: a real engine Neuron's phase-response curve is biphasic
  (advance AND delay) -> phase-gated communication windows.
- **M9.6** theta-gamma PAC: a measured-strength slow field shifts a fast region's bifurcation
  parameter; amplitude is modulated at the slow rhythm. Non-circular -- MI is zero with the field
  cancelled, clearly present at measured kappa (>1000x a phase-shuffled control), stronger when
  augmented.
- **M9.7** traveling wave: a cortical chain with a conduction-delay gradient develops a monotone
  phase gradient -> a wave at the conduction speed (timing ionic [O]).

## Grades (honest)

- gamma per organ -- **[F] measured input**, read VERBATIM from the neuro master-gene data files
  (`repro/neuro/_engine/data/{sensory_organ_gamma.json, spinal_master_genes.json}`); SantaLucia 1998
  nearest-neighbour stacking, the same metric the DNA volume uses.
- ephaptic coupling kappa = dVm/threshold = 0.2748/0.5 = 0.5496 -- **[F] measured fraction**
  (neuro 19; Anastassiou 2011), NOT tuned to any target.
- 1/r^3 locality -- **[V]** measured near-field falloff (neuro 18).
- partial/metastable regime, field's causal contribution, CTC, PAC, traveling wave -- **[V]**
  simulation-verified mechanism.
- absolute band centre frequencies in Hz, ring geometry, R_brain, conduction speed -- **[O]**
  representative; band IDENTITY is cited, absolute Hz is not read from any window.
- whether cognition biologically USES this coordination -- **[O] OPEN**; `medium_efficacy_tested = 0`.
  The obstacle is explicit: the behaviour-labelled in-vivo field-cancel-vs-augment intracranial
  recording named in neuro 9/19 has not been performed.

## Provenance of the two project-fetched masters

Four organs reuse the four masters of section 3 (FOXG1, EN1, SIM1, LHX2) and three more are already
in the neuro atlas (GBX2 thalamus, OTX2 midbrain). Two were fetched THIS project by the identical
NCBI eutils + SantaLucia pipeline:

- `extra_masters.json` -- the fetched values (GSX2 striatum 1.4606, PHOX2B brainstem 1.3608, plus
  NKX2-1 / TCF7L2 / DLX2 fetched alongside but not used in the final 8-organ loop).
- `fetch_extra_masters.py` -- the fetch script (esearch -> esummary -> efetch promoter window
  [TSS-2000, TSS+500], 2501 bp coding strand; gamma = -mean(NN dG37)).

corr(gamma, GC) = 0.9968 across the 8-organ atlas, consistent with the wider atlas (0.994-0.995) --
a MEASURED correlation of read-only inputs, not a fitted target.

## Run

    cd ../_engine && python3 run_all.py        # emerges M0..M9, freezes expected_sha256.json
    cd ../_verify && python3 run_regression.py # bit-for-bit + mechanism invariants (seed=19)

## Frontier-paper caveat

The regression demonstrates the mechanism behaves as claimed; it does NOT confirm any functional
theory of consciousness, and there is no validated marker of consciousness (PCI = honest negative,
section 12). M9 shows what the MEASURED field CAN do (mechanism, [V]); whether biological cognition
USES it is OPEN. The dependency on neuro is one-way (objects and numbers cited, never re-derived).
