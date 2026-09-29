# BC4: black-copper voltage under radiative vs conductive heating (a bench test)

This is a **pre-registered physical experiment that has not been run yet.** It needs a bench. `bc4_predict.py` works out the standard-physics null, the systematic budget and the decision threshold, all before any data exist. Its output is `PREDICTION.json`.

## The idea
A VP proposal, graded [O], says the black CuO nanostructure tilts incoming infrared (transverse, χ≈90°) directly into directed conduction (χ→0) in copper. Standard physics says a thermoelectric voltage depends only on the temperatures. The two views separate at **matched temperatures:**

| | Standard physics | VP χ-conversion |
|---|---|---|
| ΔV = V(radiative) − V(conductive), same T_front and T_back | 0 | ≠ 0 |
| Sign when the plate is flipped (C4) | — | reverses with the radiation direction |
| Uncoated control (C3) | 0 | 0 |

## Pre-computed numbers
The table assumes a 3 mm Cu plate, a cooled back face and leads of the same Cu clamped to bare copper.

| Emitter | Net flux | ΔT through the plate | Systematic bound | Photon-drag ceiling | Threshold |
|---|---|---|---|---|---|
| 67 °C | 206 W/m² | 1.6 mK | 0.2 µV | 5e-17 V | 3 µV |
| 150 °C | 1 223 W/m² | 9.2 mK | 0.2 µV | 3e-16 V | 3 µV |
| 300 °C | 5 352 W/m² | 40 mK | 0.2 µV | 1e-15 V | 3 µV |

- **Copper conducts heat too well to hold a temperature difference.** Even at 300 °C the drop through the plate is 40 mK. Every standard voltage is therefore at the sub-µV level.
- **A lead that touches the black face adds an artifact.** That lead forms a CuO/Cu thermocouple (S ≈ 204 µV/K for p-CuO films), which gives up to 8 µV. The protocol avoids this by clamping every lead to bare Cu.
- **Photon drag is far below any detection.** It is the standard "light pushes electrons along its direction" effect, and it is measured in gold films.
- **Consequence:** any radiation-specific voltage above 3 µV that reverses sign when the plate is flipped would be a clean signal that standard physics does not predict.

## Status
The proposal is **kept, open [O]**, until this test is run. A null result would be recorded as an upper bound on the χ-conversion voltage. It would not be a disproof of the idea beyond that bound.
