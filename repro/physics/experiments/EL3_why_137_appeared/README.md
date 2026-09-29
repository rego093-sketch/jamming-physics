# EL3: why 137 appeared in EL2 (an audit of the experimental conditions)

This audit was pre-registered in `PREREG.json`; run it with `python3 el3_run.py`, which writes `RESULT.json`. One change was made before the script's first successful run: the formula that splits the EL2 residual was corrected. The first draft used the reduced-mass factor, but the EL2 target already contains it. The script had not produced any output before this change.

## Why EL2 got 137 to 1×10⁻⁵
1. **Anchor condition.** D<sub>anch</sub> is locked to 2λ_C (§13), so D/4π is exactly the reduced Compton length ƛ_C.
2. **Input condition.** The a₀ that EL2 used (52.918 pm) is the CODATA Bohr radius, and CODATA computes it as ƛ_C/α. It is not an independent size measurement.
3. Given (1) and (2), a₀/(D/4π) = 1/α **by construction**. The residual of 1×10⁻⁵ comes from rounding a₀ (+5.3×10⁻⁶) and from higher-order terms in the energy-ratio target (−5×10⁻⁶). **The match is circular and is not evidence.**

## What survives without the circularity
- **D from its independent route** (D = 2πλ_ref/A, with A from the jamming run):
  - lattice A (central value 7.79×10⁵): 1/α = **130.2**, 5 % low;
  - lattice A range [6.95, 8.53]×10⁵: 1/α from **116 to 143**, so 137 lies inside;
  - circulation length, median 4.96 pm: **134.1**;
  - circulation length, selected best 4.8542 pm: 136.99. This case is already retired as evidence.
- **This check is test E2 and nothing more.** E2 is the claim that A links the light wavelength to 2λ_C at ±10 %. The number 137 itself enters through the hydrogen size.

## What VP has to explain
- In VP units the hydrogen stand-off is **a₀/D = 1/(4πα) = 10.905 quantum diameters**, which is 11 − 0.095.
- **The 4π is geometric.** It comes from D = 2λ_C and ƛ = λ/2π, so it does not depend on the choice of units. This answers one of the three reasons §14.5 gave for withdrawing the old form 4π(11 − δ): that the 4π was an SI ε₀ artefact.
- **"Why 11 layers" is still not forced.** That was the first withdrawal reason, and it stands.
- **Running of α (137 → 128).** In this reading, the atomic value is the *static stand-off*. Higher-energy probes reach inside the stiff zone. This is [H].
- **What would decide it.** The number of stiff-quantum layers around the proton (about 11, i.e. a radius of about 10.9 D) is a full-simulation observable. If the full 3-D simulation counts about 11 layers, the stand-off principle predicts 1/α to the precision of that count. If it counts a different number, the principle does not produce α.
