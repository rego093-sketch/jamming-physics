# LEDGER — Appendix D · heart composite-renormalization accuracy test

Honest per-channel grades. The point of this appendix is to push toward **accuracy**
(정확), not just precision (정밀), on the heart — the case that *failed* in Appendix A.
So this ledger is explicit about which results are parameter-free measured/logical
truths, which are consistency checks, and which remain illustrations or open obstacles.

| grade | meaning |
|---|---|
| `[L]` | locked: independently measured/published value or exact theorem, cited |
| `[V]` | verified: exact theorem / logical certainty / parameter-free inequality (precision) |
| `[F]` | fixed modelling choice (monotone schedule / central value); declared |
| `[O]` | open: precision/consistency real but the tight co-registered measurement is absent; named |

## Channels

| channel | grade | basis |
|---|:---:|---|
| exact two-phase bracket  B_Reuss <= B_eff <= B_Voigt  (cell + ECM) | `[V]` | exact elastic-mixture theorems (Voigt 1889 isostrain upper, Reuss 1929 isostress lower, Hill 1952 bounds) with BOTH phases real (B>0); evaluated exactly. No free parameter. |
| RESULT A -- pure cell-jamming insufficiency (falsification) | `[V]` | parameter-free inequality on MEASURED moduli: embryonic cell ceiling (~1.25 kPa) << measured tissue (~10-18 kPa), so the stiff ECM phase / cell maturation is necessary; pure jamming (Appendix C) is falsified for the trajectory. |
| RESULT B -- gamma orthogonal to the stiffening (explanation of the null) | `[V]` | logical certainty: gamma is sequence-fixed -> time-invariant -> cannot encode a rising trajectory; reproduces the measured Appendix A heart null (rho=+0.071, p=0.882). |
| measured phase moduli (cell, ECM) and tissue trajectory | `[L]` | independently measured, cited: single-cardiomyocyte AFM (immature ~1.25 kPa, adult ~35 kPa), decellularized myocardial ECM (LV ~5, SAN ~17 kPa), myocardium stiffening 0.1+0.3*day / E2<1 -> E14~10 / adult 10-50 kPa. |
| RESULT C -- two-phase bracket contains the measured ventricular tissue | `[L]` | consistency: the exact bracket from measured ventricular inputs (cell 35, LV ECM 5 kPa, phi_cell 0.8) contains the measured adult ventricular tissue (~18 kPa). Input-sensitive (isolated cells stiffer than bulk); a tight prediction needs a co-registered preparation. |
| composition-flow trajectory reproduces the embryonic->adult span | `[F]` | illustration: monotone measured-grounded schedules (ECM fraction rising, cell jamming ramping) at FIXED measured phase moduli reproduce the stiffening span; the schedule SHAPE is a modelling choice, the phase moduli are measured. |
| collagen volume-fraction trajectory phi_ecm(t) | `[F]` | the RISE is measured (collagen rises faster than heart weight; neonatal-high collagen); the exact per-stage fraction shape is a documented monotone choice standing in for co-registered stereology. |
| TIGHT quantitative trajectory prediction (zero free parameters) | `[O]` | ACCURACY not yet tight. Needs a SINGLE co-registered developmental series in ONE preparation: (E_tissue, phi_ECM, phi_cell, B_cell, B_ECM) per stage. With it the composite predicts E_tissue(t) parameter-free and the match becomes a tight accuracy [V]. |
| active tension contribution (myosin) vs passive composite | `[O]` | ACCURACY untested. Majkut shows the contraction wave speed is LINEAR in E_t (active), distinct from the passive VP elastic wave c=sqrt(B/rho); separating active from passive needs a measured tension series. |
| large-strain (nonlinear strain-stiffening) behaviour | `[O]` | ACCURACY untested. Collagen and myocardium strain-stiffen; the bracket here is the small-strain modulus. Large-strain needs a measured stress-strain curve per stage. |

## Earned-completion test

`completion.complete = False`

the heart is converted from an unexplained Appendix-A null into a mechanistically explained, exactly-bracketed, falsification-tested case: the stiffening axis is composition (ECM)+maturation, pure jamming is falsified [V], gamma-orthogonality is explained [V], and the exact bracket from measured ventricular inputs contains the measured tissue [L]. But a TIGHT zero-parameter trajectory prediction is not yet made -- three accuracy channels remain [O]. Precision/consistency earned; full accuracy not yet claimed.

### Open accuracy obstacles (named)

- **TIGHT quantitative trajectory prediction (zero free parameters)** → needs: co-registered developmental series (tissue modulus + both volume fractions + both phase moduli) in one preparation
- **active tension contribution (myosin) vs passive composite** → needs: measured active-tension vs passive-stiffness decomposition per developmental stage
- **large-strain (nonlinear strain-stiffening) behaviour** → needs: measured per-stage stress-strain curves (nonlinear modulus)

**Distance to close:** ONE measured dataset (named above). The machinery, the measured phase moduli, the falsification, and the explanation are already in place.

**What would close it:** obtain the co-registered developmental series in one preparation, feed measured (phi_ECM, phi_cell, B_cell, B_ECM) per stage into the SAME composite, predict E_tissue(t) with zero free parameters, compare to the measured E_tissue(t) with a shuffle control and a pre-registered sign; then and only then mark the heart trajectory 정확.

---

*precision (정밀) ≠ accuracy (정확). 반증 = 발견. The heart is mechanistically
explained and exactly bracketed — not yet quantitatively closed.*
