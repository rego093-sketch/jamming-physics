# EM1 — Hair-bundle behaviour emerging from its molecular elements (one simple tissue unit)

The test was pre-registered in `PREREG.json`. The model was corrected once, before the second run; the reason is recorded in `PREREG_AMENDMENT.json`. To reproduce, run `python3 em1_run.py` (about 3 minutes); it writes `RESULT.json`. The first run is kept as `RESULT_run1_gamma_in_motor_term.json`.

**Author's principle.** Complex structures cannot be emerged realistically, because their environment cannot be matched. Simple tissues emerge accurately. Here the elements and their constants are observations, taken from the Nadrowski, Martin & Jülicher 2004 bundle model:
- gating springs,
- transduction channels,
- adaptation motors,
- calcium feedback.

The bundle's behaviour is not set anywhere in the model; it has to emerge.

## Runs

| Run | What happened |
|---|---|
| 1 | My transcription multiplied the motor force by γ = 0.14. With that error the channels were all shut at rest (Po = 0), and nothing emerged. This is an implementation error, recorded as FAIL. |
| 2 (amended) | The operating point is Po ≈ 0.85. At the reported motor force the system has a lightly damped 13.7 Hz mode. |

## Results (run 2) against observation

| # | Prediction | Result | Verdict |
|---|---|---|---|
| P1 | A self-sustained oscillation emerges, and the reported F_max = 50.3 pN lies inside the oscillating window | An oscillation **does emerge**, but only for F_max = **48–49.5 pN**. At 50.3 pN the bundle is quiescent (damped at about 13 Hz). | **FAIL** (the reported value is about 1 pN outside the window) |
| P2 | At 50.3 pN: 5–50 Hz and 20–150 nm | Nothing at 50.3 pN. Inside the window: **37 nm peak-to-peak at 5.8–6.7 Hz**, within the observed 5–50 Hz and 20–80 nm (Martin & Hudspeth 2001; Martin et al. 2003). | **FAIL** as registered (checked at 50.3 pN); matches the observation inside the window |
| P3 | Just on the quiescent side, a local compression exponent between 0.25 and 0.45 appears over some force decade | Local exponents over 1–32 pN are 0.12 / 0.17 / 0.25 / 0.35 / 0.46 / 0.58. The **1–10 pN average is 0.22 and the 1–32 pN average is 0.32**. | **PASS** |
| P4 | One bundle does not go below 0.25 (the organ-level 0.2 would then need the whole cochlea) | One bundle reaches 0.12–0.22 | **FAIL**: my expectation was wrong |

## Reading
- **What emerges from the elements alone:**
  - self-sustained oscillation, of the relaxation type: the amplitude is constant across the window and switches on abruptly;
  - an abrupt, switch-like onset under a force of about 1 pN;
  - compressive growth whose average exponent over 1–10 to 1–32 pN is **0.22–0.32**. The observed basilar-membrane range is 0.2–0.33, and single bundles are observed at about 1/3. The ear pages had *assumed* 1/3; here the range emerges from the elements.
- **What does not match:** the model oscillates about 1 pN below the published F_max. The operating point is sensitive to that constant, so this is recorded as a mismatch, not tuned away.
- **What is not attempted:** the whole cochlea (travelling wave, many coupled bundles) is a complex structure and stays [O].
