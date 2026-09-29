# GW2: rotating quanta carried on the VP scaffold

**Principle.** Everything comes from the lattice. **VP** is the medium. It is never empty, and it carries c² = B/ρ. **Quanta** are the rotating units riding on VP, and they can be absent, momentarily or in a steady deficit. The observations come first: gravitational waves travel at c with tensor polarisation (+, ×), and light is transverse with two polarisations.

**Model.** The model is the 3-D problem reduced to the ray, as the corpus allows for excessive computation.
- **Scaffold.** A chain along the ray with m = k = a = 1, so c_L = 1. It is always full.
- **Quanta.** Rotors about the ray axis, each coupled to the local strain by V = ½κ(θ − gε)². The coupling is two-way, so the rotors also load the scaffold.
- **Gap.** Sites 3000–3599 have no quanta.
- **Readout.** A ring of test points around the ray reads the field change of body-fixed dipoles (l = 1) or traceless quadrupoles (l = 2).

**Pre-registration.** `PREREG.json` was committed before the first run (commit "GW2: pre-register…"). No exploratory run was made.

## Result (`python3 gw2_run.py`, about 11 s, deterministic)

| Prediction | Result |
|---|---|
| P1: c is maintained with or without quanta | **PASS**: strain-peak speed 0.993 / 0.996 / 0.996 c before / in / after the gap |
| P2: the rotation pattern is carried at c and reappears after the gap on schedule | **PASS**: 0.993 c before, 0.996 c after, 0.996 c for arrival across the gap. The amplitude inside the gap is 0, since there is nothing to rotate |
| P3: heavy quanta lag, so carrying needs fast rotation | **FAIL**: heavy quanta (rotor frequency = pulse frequency) are also carried at 1.001–1.002 c |
| P4: quadrupole quanta give two states 45° apart and no breathing; dipole quanta give two states 90° apart | **PASS**: monopole fraction ~1e-27, harmonic purity 1.0, overlap between the two states ~1e-14 |

## Reading

1. **VP holds c.** A region without quanta is transparent. The scaffold carries the pulse through at c, which is the distinction between quanta and VP in its simplest form.
2. **The transverse state is carried.** A quantum's rotation is driven by the scaffold strain at its own site, so the rotation pattern moves with the scaffold at c. That is why gravitational waves and light have the same speed.
3. **P3 failed, and that is informative.** The pattern is driven site by site, not propagated rotor to rotor, so heavy quanta change only its amplitude and phase lag, not its speed. Carrying does not require fast internal rotation.
4. **Polarisation content.**
   - Quadrupolar quanta, turning about the ray, change the field on a transverse ring only in the cos 2φ / sin 2φ harmonics. That gives exactly two states, + and ×, 45° apart, with **no breathing (scalar) part**, which is what LIGO–Virgo observe.
   - Dipolar quanta give the helicity-1 pattern of light, with two states 90° apart.
   - This part is geometry [F].

## Grades and limits

- **(1)–(2): [V mech]** in a reduced ray model.
- **(4): [F] geometric.**
- **The coupling form: [H].** "Quanta driven by the local scaffold strain" is an assumption of the model, not derived from contacts.
- **Not shown:**
  - |E| = c|B|;
  - which multipole a given source excites (a binary inspiral is quadrupolar, a charge is dipolar);
  - the full 3-D packing with frictional contacts;
  - the high-k dispersion of the scaffold (cos(ka/2)), which remains the open gamma-ray issue.
