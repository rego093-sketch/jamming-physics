# LE1: why light emerges, and whether heat or straight motion gives gamma-like light

This experiment was pre-registered in `PREREG.json` before it was run. Run `python3 le1_run.py` to reproduce it; the output is written to `RESULT.json`. It uses the light chain from the whitepaper, as coded in `legacy_v1_0_2026-06-14/.../vp_light_emergence.py` and `vp_light_angle.py`.

## Why light emerges: what the simulation shows
1. **A disturbance becomes a wave that travels at c.** A local push injected into a 1-D chain of quanta turns into a wave moving at speed c. At long wavelengths the wave obeys ω = cq, i.e. λ = c/ν, which is the behaviour of light (PART 1–2, graded [V]).
2. **The lattice stiffness sets c.** The relation is c² = B/ρ (PART 3, graded [F]).
3. **Only one wave type survives at the isostatic point.** In a 2-D triangular lattice with z = 6, the transverse speed c_T drops to 0 as the shear margin goes to 0. Only the longitudinal wave survives (PART 4, graded [V]).
4. **The propagation angle is set by geometry.** Light that exists travels at angle χ, with sin χ = λ/(mD), m = ⌈λ/D⌉ and D = 2λ_C (PART 5, graded [F]).

**Answer:** light is the one elastic wave that survives in the jammed lattice. Heat (the rotation of quanta) is only the *source* of the disturbance. Whether that light is near-transverse or near-longitudinal depends on **λ compared with D**, not on how hot the source is.

## Results

| # | Result | Verdict |
|---|---|---|
| P1 | Light enters the near-longitudinal (m = 1) regime at photon energy hc/D = **m_e c²/2 = 255.5 keV** exactly. | PASS [F] |
| P2 | For the peak of thermal light to reach χ = 45°, the source must be at **T = 8.4×10⁸ K**. At 3000 K, the fraction of thermal photons with λ < D is 10^(−429 000), i.e. zero. At 10⁸ K the peak is still at 84°. | PASS |
| P3 | A single electron accelerated in a straight line reaches χ = 45° at **361 kV**, χ = 15° at 1 MV and χ = 1.5° at 10 MV. | PASS |
| P4 | Electron–positron annihilation light (511 keV) has λ = D/2, giving m = 1 and **χ = 30°**. | PASS |
| P5 | Thermal emission carries no net momentum in any direction, whatever the temperature. Bremsstrahlung from a straight electron beam is observed to point forward. | observation / argument |

## Conclusions
1. **Gamma-like angles need energy concentrated into one quantum, not temperature.** Heat spreads its energy over every quantum at about kT each, so reaching the same angle takes about 10⁹ K, the regime of stellar cores and nuclear reactions. A charge moving in a straight line concentrates the energy into one carrier. About 0.36 MV is enough, which is what an X-ray tube or small accelerator does.
2. **Heat gives no direction.** Even thermal gamma rays at 10⁹ K are emitted in all directions. Electricity, meaning directed conduction (χ → 0), needs **straight motion of charges driven by a field or a junction**: an asymmetry. Heat supplies the energy; straight motion or asymmetry supplies the direction.
3. **Heat pushes away from conduction.** In the corpus (chemistry EM.6), the conduction angle χ → 0 requires small amplitude inside a medium. Heat increases amplitude, which tilts χ toward transverse, i.e. toward radiation. Ultra-high temperature therefore produces more light, not electricity. Heat can drive a current only through a device with an asymmetry, such as a thermocouple, a thermionic converter (hot cathode with a different collector work function) or a TPV cell, and the Carnot limit applies. This matches BC2 and BC4.
4. **The angle formula has a sawtooth [O].** Because m jumps by whole numbers, sin χ = λ/(mD) is not monotonic in the X-ray band. For example, 100 kV gives χ = 58°, but 255.5 kV gives 89.9°. Measuring the transmission angle of X-rays across that band could therefore falsify the formula. This is recorded as an open prediction.
