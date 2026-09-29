# BC2 — Black-copper boundary in the ESS: infrared → directed electron motion?

This test was pre-registered in `PREREG.json` before it was run. To reproduce, run `python3 bc2_run.py`; it is deterministic and writes `RESULT.json`. **All six predictions pass** (P1–P6).

The setup, as the author specified it:
- the copper is bulk, and only its surface is nano-coated black (CuO);
- the boundary sits inside the hot-sand ESS and collects the store's infrared.

## Results (per m² of boundary, absorptance 0.96)

| Store T | Photons above the CuO gap | Carnot limit of net flux | Best power, ideal yield (φ_B) | Best power, Fowler yield | Net drift speed v_d |
|---|---|---|---|---|---|
| 67 °C (ESS2) | 9e-18 | 45 W | **6e-6 W** (0.1 eV) | ~1e-18 W | 5e-8 m/s |
| 150 °C | 5e-14 | 412 W | 3e-4 W (0.2 eV) | 8e-13 W | 5e-8 m/s |
| 300 °C | 5e-10 | 2 670 W | 0.19 W (0.5 eV) | 1e-8 W | 4e-9 m/s |
| 500 °C | 3e-7 | 11 800 W | **37 W** (0.5 eV) | 1e-4 W | 9e-8 m/s |

- **P1 [F].** A boundary at the store temperature, fully inside the ESS, gives **exactly zero** net power. At equal temperature the reverse photoemission and the thermionic leakage balance the forward current. This is detailed balance, the second law.
- **P2.** At 67 °C even the ideal case gives about 6 µW/m².
- **P3.** Fowler, the realistic hot-electron yield of a metal, is 10⁻⁵ to 10⁻¹² of the ideal case.
- **P4.** At 500 °C with a cold side, the ideal case reaches 37 W/m². The route is limited by temperature; physics does not forbid it.
- **P5.** Electrons in Cu move at the Fermi speed (1.6e6 m/s) in all directions. The *net directed* part is at most about 1e-7 m/s.
- **P6.** A 100 nm coating carrying 1 kW/m² has ΔT = 3e-5 K. Even at 1 mV/K that gives only 3e-8 V. The coating alone cannot be a thermoelectric.

## Reading

1. **Why the coating does not create charge carriers.** Store infrared (0.08–0.2 eV photons) lies far below the CuO gap (1.35 eV). The black coating therefore traps it as heat. It does not create electron–hole pairs.
2. **The only sub-gap route is internal photoemission, and it is weak.** A photon absorbed in the copper can send a hot electron over the Cu/CuO barrier φ_B. The same barrier leaks back a thermionic dark current, J0 = A*T² e^(−φ_B/kT), with a prefactor of about 1e11 A/m². That leakage, not the absorption, is what limits the output.
3. **Electricity needs a cold side.** Output appears only when heat flows *through* the boundary from the hot store to something colder. That makes the device a heat engine, bounded by Carnot. Its best version is a real junction facing the hot store: a narrow-gap p–n TPV cell, or a bulk thermoelectric across a millimetre-scale temperature difference, not across the coating. This is ESS3.
4. **In the corpus's χ language, graded [H].** Long-wave store IR is transverse (χ ≈ 90°). The black boundary turns it into rotation, i.e. temperature. Directed, near-longitudinal conduction (χ → 0) needs a barrier that picks one direction, and that same barrier leaks backwards through thermal rotation. The black colour maximises collection. It does not supply the direction.

All values are model bounds from declared, literature-form inputs (Richardson A*, Fowler with E_F(Cu) = 7 eV). They are not measurements, and are graded [V mech].
