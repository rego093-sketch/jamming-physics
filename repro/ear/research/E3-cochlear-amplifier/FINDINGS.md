# FINDINGS — increment E3 (the cochlear active amplifier: cube-root compression)

**Status:** DELIVERED (v0.4.0). Deterministic module `run.py` (2×sha256 identical:
`e357a450…`), small gate `gate.py` (7/7 PASS), folded into `tools/verify_seed.py` foundation list.
Inherited foundation untouched (frozen hashes valid). No constant tuned.

## What E3 builds
The outer-hair-cell **cochlear amplifier** — the active process powered by **prestin (`SLC26A5`)** —
**emerged** from the *inherited* R19 substrate, sitting on the inherited √-law place map. The keystone
is parameter-free: the basilar-membrane response **compresses as the cube root of the drive**,
`r ∝ F^(1/3)`, and the **1/3 exponent is forced by the substrate's cubic nonlinearity** — not fitted.
The amplifier and the E1 tip-link transduction switch are shown to be the **same R19 cubic in two
regimes**: bistable (all-or-none detection, E1) vs critical (compressive amplification, E3).

## Results (every number reproduced offline, bit-for-bit)
- **Amplifier gene reproduces.** `SLC26A5` (prestin) γ + A4 recompute from the frozen promoter cache
  and equal the atlas bit-for-bit; A4 = signal − γ (|mean(shape)| < 1e-9). γ=1.4023, node
  `cochlear_amplifier`. **[V]**
- **Cube-root fixed point — analytic, from the inherited cubic.** The inherited `sdot(s,g,h)=g·s−s³+h`
  at criticality `g=0` has its zero at `s*=F^(1/3)`: evaluating the *inherited* `sdot` at `s=F^(1/3)`
  gives max|residual| = **5.7e-13** over 7 decades of drive. The cube root **is** the inherited cubic's
  critical fixed point, with no constant chosen. **[F]**
- **Compression exponent — verified on the inherited integrator.** `settle(0,F)` converges to `F^(1/3)`
  on the converged drive range F∈[0.1, 100]; the **fitted** exponent (slope of log r vs log F, *read
  off, not imposed*) = **0.333333**, |exponent − 1/3| = 1.3e-15, max rel.err vs F^(1/3) = 9.2e-15. **[V]**
- **Same cubic, two regimes.** With `g=γ_TMC1=1.3028` the response is **all-or-none** across the
  spinodal (the E1 switch, OFF −0.71 → ON +1.31); with `g=0` the *same drives* give the **continuous
  compressive cube root** s=h^(1/3). One substrate equation; bistable detection ∥ critical amplification.
  **[F]**
- **Gain compresses as F^(−2/3).** Gain r/F fits exponent **−0.666667** (|Δ|=1.2e-15); faint drives are
  amplified **100×** more than loud across the tested range — the dynamic-range compression that lets the
  ear span ~120 dB. Exponent/direction **[F]**; absolute gain/dB **[O]**.
- **Amplifier's place in the lineage.** argsort(spinodal(γ)) over the MET + hair-cell genes places
  **SLC26A5 between PCDH15 (0.6233) and ATOH1 (0.6588)** at spinodal 0.6391. **[F]** order; γ measured **[L]**.
- **Uniform compression across the tonotopic bank.** Each place x carries CF=Greenwood(x) (place map
  re-verified, max|ratio−1|=2.2e-16); the local amplifier is the same critical cubic, so the compression
  exponent is **1/3 at every place** (CF-independent) — compression is uniform across frequency. **[F]**
- **Oscillatory-Hopf corroboration.** The 2-D Hopf normal form at μ=0, on resonance (the OAE-emitting
  active oscillator the literature names "Hopf"), gives steady-amplitude exponent **0.3515** — the same
  cube root, with a finite-averaging numerical bias (~0.02; see N5). The exact result is the analytic
  fixed point above. **[V]**

## Honest negatives / open items — the E3→E4 starting line (preserved, not hidden)
- **N1.** The absolute **gain / dB of amplification / dynamic-range-in-dB / sharpness Q** are **[O]** — a
  numerical value would require **tuning** a constant (forbidden). Only the exponent (1/3) and the
  direction (compression) are forced. *Obstacle:* magnitude needs a measured/tuned gain or Q.
- **N2.** The cube root matches the **FORM** of measured cochlear compression, but the measured I/O
  **slope value** (study-dependent, ~0.2–0.5 dB/dB) and the absolute curve are **[O]**.
- **N3.** Otoacoustic-emission **frequencies and amplitudes** are **[O]** — they need the per-place gain,
  Q, and an operating point just above the bifurcation (μ slightly > 0), none derivable without a tuned
  constant.
- **N4.** Prestin's actual **electromotile/piezoelectric force** is **NOT** read from γ — the firewall
  holds: γ reads promoter STRUCTURE only. The amplifier's **magnitude** is not derivable from γ; only the
  gene's spinodal-order place and the compression **exponent** are forced.
- **N5.** The inherited integrator **under-converges** to the cube-root fixed point at *very small* drive
  (the restoring force ∝ s³ vanishes near s=0); the rigorous **[F]** is the analytic fixed point, the
  **[V]** is on the stated converged range, and the oscillatory-Hopf exponent carries a ~0.02 bias.

## Bridge to the goal (E4)
E3 is pre-disease but **neighbours the E4 congenital-deafness goal**: outer-hair-cell / prestin
dysfunction is itself a deafness mechanism (e.g. `SLC26A5` variants; OHC loss → loss of the amplifier →
the elevated thresholds and lost compression of sensorineural hearing loss). The R19 reading of E4 will
be **direction-only under the firewall** — the amplifier failing to operate at criticality (loss of the
F^(−2/3) gain) is the structural hypothesis, stated as a proposal, never a diagnosis or a dose.

## Naming note (flagged, not silently fixed)
This increment delivers **BLUEPRINT-E3** (the active amplifier) and is shipped in the unambiguous folder
`research/E3-cochlear-amplifier/`. **BLUEPRINT-E2** (the MET switch) shipped in v0.3.0 inside the folder
labelled `E1-place-and-traveling-wave`; **BLUEPRINT-E1** (the full fluid-loaded, dispersive traveling-wave
**ENVELOPE**) remains the named **[O]** — closing it would require **tuning Q** (forbidden). The E-folder
numbering inconsistency introduced in v0.3.0 stands flagged; a future session should reconcile
`BLUEPRINT.md`'s E-numbering with the folder names.

## Firewall
γ read promoter STRUCTURE only (never a motor force, gain, voltage, dose, or effect). No disease claim
(E3 is pre-disease). The percept of loudness is the mind volume's.
