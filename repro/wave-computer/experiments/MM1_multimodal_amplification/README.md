# MM1 — multimodal cue amplification (pre-registered)

**Question.** In the frozen phase-coded core (`wave_compute_core.py`, unmodified), does combining sensory cues from the same episode amplify recall, and does mixing cues from different episodes suppress it?

**Protocol.** `PREREG.json` was committed first (defc9e2), then `mm1_run.py` was run. The setup has four 64-unit modality blocks (think colour, smell, companion, place), 15 stored episodes, a cue phase jitter of 0.8 rad, and 40 fresh seeds (5000–5039). Recall counts as a success when |overlap| ≥ 0.9.

**Result (`RESULT.json`).**

| cued modalities | same episode (coherent) | different episodes (incoherent) |
|---|---|---|
| 1 | 35% | — |
| 2 | 78% | 3% |
| 3 | 88% | 3% |
| 4 | **90%** | **5%** |

- P1 amplification: **PASS** (monotone rise, +55 points from 1 to 4 cues).
- P2 interference: **PASS** (85 points between coherent and incoherent at 4 cues).

**Reading.** Cues that share an episode's phase add constructively and cross the recall threshold. Cues from different episodes add destructively and block recall. This is a property of the model: it is [V mech], reproduced in-model. The biological statement it supports (the hippocampus combines theta-locked multisensory input) is [H]. Data-pending: human recall versus the number of congruent and incongruent cue modalities.

**Limit.** The effect depends on memory load. At load ≥ 0.10 recall fails even with four cues, and with clean cues at low load a single cue can suffice.
