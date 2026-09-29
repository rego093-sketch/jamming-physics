# BC5 — Black copper as an infrared rectenna

This experiment was pre-registered in `PREREG.json` before it was run. To reproduce it, run `python3 bc5_run.py`; it writes `RESULT.json`.

**The idea being tested (author).** Turning heat into electricity needs a change of **angle**, not high photon energy. The light has to go from transverse (χ ≈ 90°) to longitudinal conduction (χ → 0), and this should be possible at low energy. Electricity, radio antennas and gravitational-wave detection all work this way. The engineering form of the idea has three parts:
- the nanostructure acts as an antenna array (coherent pickup);
- the Cu/CuO junction acts as a diode (sets the direction);
- the difference between the hot store and the cold side supplies the net flow.

## Results (T_c = 293 K, absorptance 0.96)

The best diode case is β = 5 A/W, R_d = 1 kΩ, f_c = 100 THz.

| Store | Fraction passed, f_c = 1 / 10 / 30 / 100 THz | Input per antenna | Rectification η | Output, best | Output, f_c = 30 THz | Output, weak diode | Carnot limit |
|---|---|---|---|---|---|---|---|
| 67 °C | 0.07 / 0.48 / 0.80 / 0.97 | 1.3e-8 W | 8e-5 | **0.026 W/m²** | 0.018 | 1.8e-5 | 45 W/m² |
| 150 °C | 0.06 / 0.44 / 0.77 / 0.96 | 4.1e-8 W | 2.5e-4 | 0.33 W/m² | 0.21 | 2.1e-4 | 412 |
| 300 °C | 0.05 / 0.38 / 0.71 / 0.94 | 1.0e-7 W | 6.5e-4 | 3.3 W/m² | 1.9 | 1.9e-3 | 2 671 |
| 500 °C | 0.04 / 0.33 / 0.64 / 0.91 | 2.1e-7 W | 1.3e-3 | **23 W/m²** | 11 | 0.011 | 11 820 |

| # | Prediction | Verdict |
|---|---|---|
| P1 | Isothermal gives zero: a diode cannot rectify its own thermal noise (second law) | **PASS** |
| P2 | At 67 °C, f_c = 1 THz passes < 5 % and 30 THz passes > 50 % | **FAIL**: 1 THz passes 7 %; 30 THz passes 80 % as predicted |
| P3 | At 67 °C the input per antenna is below 1e-7 W and η is below 1e-3, so the small-signal diode is the bottleneck | **PASS** |
| P4 | The best rectenna exceeds the BC2 photoemission bound by ≥ 100× | **PASS**: 4 056× |
| P5 | At 500 °C the output exceeds 1 W/m² | **PASS**: 23 W/m² |

## Reading
1. **The author's point holds: this is an angle problem, not an energy problem.** The same 67 °C store gives about 6 µW/m² through the photon-energy route (BC2, internal photoemission) and about 26 mW/m² through the angle route (rectenna), roughly 4 000× more. Low-energy infrared can be turned into a directed current.
2. **The bottleneck is the diode.** Each antenna receives only about 10 nW. A square-law diode converts roughly in proportion to its input power, so η is about 10⁻⁴. The output rises steeply with store temperature, with η ∝ (T_h² − T_c²) on top of the growth of the flux itself. That makes a **hot store** the main lever, reaching 23 W/m² at 500 °C.
3. **Frequency response matters.** The diode must respond at roughly 30 THz or more to catch most of the spectrum. The metal/insulator/metal junction's RC time is the engineering limit.
4. **Temperature difference is required.** When the store and the rectenna are at the same temperature, the output is zero.

The diode figures β = 0.5–5 A/W and R_d = 100–1000 Ω are **optimistic declared inputs**, typical of DC zero-bias MIM diodes; responsivity at THz is lower. Everything here is a model bound, graded [V mech]. The BC4 bench test and a measured Cu/CuO diode β(f) are the next data needed.
