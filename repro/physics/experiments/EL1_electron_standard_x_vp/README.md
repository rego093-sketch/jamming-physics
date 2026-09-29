# EL1 — The electron: standard data × whitepaper definition

This test was pre-registered in `PREREG.json` before it was run. To reproduce it, run `python3 el1_run.py`; it is deterministic, involves no fitting, and writes `RESULT.json`.

## Inputs

- **Standard data:** CODATA 2018 values; the electron's point-like bound (< 1e-18 m); and the Seebeck coefficients of 15 elemental metals.
- **Whitepaper definitions:**
  - the electron is one c-rotation unit (§14);
  - it has one annihilation event per electron-second (ν_e = 1, §9.3/§12);
  - D = 2λ_C (§13);
  - the stand-off outside the proton's compressed quanta is the atomic radius (§14);
  - the author's reverse reading: a parasitic c-rotator that moves host to host.

## Results

| # | Inference | Result |
|---|---|---|
| P1 | A charge circulating at c with the measured moment needs radius r_μ = 2μ_e/(ec) = **386.607 fm**. This equals **D/4π·(1+a_e)**. | **PASS** (difference 7e-11). Grade [L]: this is consistency through the D anchor, not independent evidence. |
| P2 | Rotation energy ħc/r_μ equals the rest energy m_e c². | **PASS** (−0.12 %, which is the a_e term). |
| P3 | Atomic stand-off in rotator radii: a₀/r_μ = **136.88 = (1/α)/(1+a_e)**. | **PASS**, exact. *Consequence:* the claim "the electron stands off outside compressed quanta" is **the same problem as deriving α_em**. The corpus takes α_em as a measured input (§14.5), so this stays **[O]**. |
| P4 | Is the charge spread over a host quantum (R_ext), or is it a point charge circulating at c (R_pt)? | **R_ext FAIL:** D exceeds the point-like bound by a factor of 4.9e6. **R_pt survives.** |
| P5 | Reverse reading with one host-temperature preference as the direction rule. It predicts a single Seebeck sign for all metals. | **FAIL:** 9 metals are negative and 6 positive, so the best universal sign fits only 60 %. |
| P6 | Minimum parasite motion is one host (D) per electron-second = 4.9 pm/s. | Non-discriminating: this is about 1e18 below atomic speeds (αc). |

Structural echo (not evidence): the event-rate radius D/(2π²) equals (2/π) times the moment radius, up to the (1+a_e) factor.

## Combined picture

1. **The electron is a point charge circulating at c on radius ƛ_C = D/4π.** This one picture reproduces three measured quantities: the rest energy (ħc/r), the magnetic moment (g ≈ 2, with the small a_e left over) and the Compton scale. The same picture is the *zitterbewegung* interpretation in the standard literature (Hestenes). What VP adds is the identification of its scale with the host quantum, r = D/4π.
2. **"Rotation crossing the host boundary" must mean the circulation's field crossing the boundary, not charge smeared over the host.** The smeared reading is excluded by collider data.
3. **The stand-off equals 1/α rotator radii.** Deriving why compressed quanta cannot host or feed the electron is therefore the same as deriving α_em. It is a well-posed open target [O].
4. **The reverse (parasite) reading is consistent with everything tested.** It does not contradict the sink/inflow reading, electron stability (> 6.6e28 yr in ordinary matter, where absorbable quanta are always present), or Pauli exclusion. On exclusion, a qualitative [H] reading is that one host holds two rotation senses. The reading **cannot** set the direction of electron flow through a single temperature preference, because the metals disagree in sign. Direction in a conductor needs material-specific structure: band structure in standard terms, host arrangement in VP terms. That remains [O].
