# EM2 — A squid giant axon built from its measured membrane elements (simple-tissue emergence)

This test was pre-registered in `PREREG.json`. One setting was changed before run 2; the change is recorded in `PREREG_AMENDMENT.json`. To reproduce, run `python3 em2_run.py` (about 1 s); it writes `RESULT.json`. Run 1 is kept as `RESULT_run1_weak_stimulus.json`.

**Inputs.** Every input is an observation from Hodgkin & Huxley 1952:
- the Na, K and leak conductances, with their measured voltage- and time-dependence;
- membrane capacitance;
- axoplasm resistivity;
- axon radius (238 µm);
- temperature (18.5 °C).

The spike and its conduction velocity are not put into the model; they have to emerge.

## Results

| # | Prediction | Result | Verdict |
|---|---|---|---|
| P1 | Conduction velocity within 15 % of the measured 21.2 m/s | **18.96 m/s** (−10.6 %). HH's own 1952 hand computation gave 18.8 m/s. | **PASS** |
| P2 | Spike amplitude 90–120 mV from rest | 95.8 mV | PASS |
| P3 | All-or-none threshold | A 1 ms pulse of ≤ 8 µA/cm² gives ≤ 7.7 mV; 10 µA/cm² gives 88 mV | PASS |
| P4 | Refractory period | A second stimulus 2 ms later gives 0.6 mV; 15 ms later it gives 93.8 mV | PASS |

Run 1 launched no spike, because the stimulus was too weak for an axon with a length constant of about 1 cm. That was a stimulation setting, and it is recorded as such.

## Reading
- **What emerges from the measured elements alone:** the action potential, its threshold, its refractoriness, and a conduction velocity within 11 % of the measured value on the same axon.
- **Where this sits in the corpus:** the neuro volume *interprets* the neuron as R19 + slow recovery (a FitzHugh–Nagumo reduction). EM2 shows that the underlying behaviour follows from the measured elements themselves. The reduction is therefore an interpretation of an emergent fact, not the source of it.

## Not attempted (left [O])
- **Sinoatrial node cell (cardioresp):** the model repositories (Physiome, BioModels) cannot be reached from this environment, so no sourced constant set could be loaded.
- **Single-cell circadian clock (circadian):** published clock models set their rate constants so that the period comes out near 24 h. Letting 24 h "emerge" from those constants would be circular.
