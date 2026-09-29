# BC6 — Rectenna optimized at realistic ESS temperatures (300–600 °C)

This test was pre-registered in `PREREG.json`. Run `python3 bc6_run.py` to reproduce it; the output goes to `RESULT.json`. The author noted that the ESS interior runs at several hundred °C, so the 67 °C case is not realistic.

**Setup**
- **Optimized variable:** the diode resistance R. Raising R raises the rectification gain but lowers the RC cutoff frequency.
- **Diode limit:** the ideal-diode curvature limit, β = q/(2nkT_c).
- **Validity condition:** the square-law regime must hold, V_ac ≤ nkT/q.
- **Comparison:** a thermoelectric module on the same absorbed net flux.

## Optimized outputs, W/m² (ideal diode n = 1, junction C = 10⁻¹⁸ F)

| Store | Optimal R / f_c | Rectenna | η on net flux | TE, ZT = 1 | TE, bulk CuO (ZT 0.05) | Carnot |
|---|---|---|---|---|---|---|
| 300 °C | 7.5 kΩ / 21 THz | **163** | 3.0 % | 576 | 43 | 2 675 |
| 400 °C | 6.0 kΩ / 27 THz | **431** | 4.0 % | 1 363 | 103 | 6 086 |
| 500 °C | 3.5 kΩ / 45 THz | **882** | 4.6 % | 2 733 | 208 | 11 830 |
| 600 °C | 2.5 kΩ / 63 THz | **1 573** | 5.0 % | 4 913 | 377 | 20 756 |

The model was also run with a realistic ideality factor, n = 1.5, and a larger junction capacitance, C = 10⁻¹⁷ F:
- With n = 1.5, output is about half.
- With C = 10⁻¹⁷ F, output is about one-tenth. The optimum moves to a lower R, which lowers the gain.

| # | Prediction | Verdict |
|---|---|---|
| P1 | The square-law regime keeps the rectenna below 6.25 % of the net flux | PASS (max 5.0 %) |
| P2 | At 500 °C the output is ≥ 100 W/m² | PASS (882) |
| P3 | A ZT = 1 thermoelectric beats the optimized rectenna at every temperature | PASS (about 3× better) |
| P4 | C = 10⁻¹⁷ F cuts the output by more than 2× | PASS (about 9×) |

## Conclusions
1. **At realistic ESS temperatures the angle route (rectenna) delivers about 0.16–1.6 kW/m².** That is roughly 3–5 % of the net flux and 6–8 % of the Carnot limit. This is a practical output level. It is the upper limit for an ideal diode with a very small junction (10⁻¹⁸ F).
2. **What limits it:** the small-signal regime (V ≤ kT/q, which caps η at about 6 %), the junction capacitance, and the diode ideality factor. Leaving the small-signal regime would need a separate model of large-signal rectification of broadband thermal noise, which remains open [O].
3. **Ranking on the same flux, today:**
   - commercial thermoelectric (ZT ≈ 1): 14 % at 500 °C;
   - optimized rectenna: 4.6 %;
   - black copper's own CuO used as a thermoelectric: 1.1 %.
4. **Practical design.** The black copper does the **absorbing**. The conversion stage should be either a thermoelectric module or a rectenna array, with the ESS hot side above 500 °C and the cold side as cold as possible. The rectenna becomes competitive only if Cu/CuO nano-junctions can reach C ≤ 10⁻¹⁸ F and an ideality factor near 1 at about 30 THz or above. That needs measurement.

All inputs are declared model limits; the grade is [V mech].
