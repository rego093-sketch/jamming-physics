# FINDINGS — increment E6 (the cochlear traveling-wave ENVELOPE: FORM forced, the sharpness Q the [O])

**Status:** DELIVERED (v0.7.0) — **turns the seed's DEEPEST [O] (BLUEPRINT-E1) from a black box into a
CHARACTERISED one**. Deterministic module `run.py` (2×sha256 identical: `cf174f7a…`), small gate `gate.py`
(7/7 PASS), folded into `tools/verify_seed.py` foundation list. **NO inherited byte changed** — E6 fetches
no new gene, folds nothing into the cache/atlas, and triggers **no re-freeze** (every frozen hash is
byte-identical to v0.6.0). No constant tuned.

## What E6 builds
The inherited `vp_sound_wave.py` names its own deepest gap in plain words: the exponential stiffness map
gives the traveling-wave **PEAK PLACE** (inverse-Greenwood), but the full fluid-loaded dispersive
traveling-wave **ENVELOPE** is *"the named [O] this seed exists to take up."* E1 forced the peak place; E3
forced the active cube root; **E6 takes up the envelope itself** — and does it the only honest way. It does
**not** close the [O] by choosing a sharpness (that would be tuning, forbidden). It **characterises** the
[O]: it proves the envelope FORM is forced by the frozen substrate, and that **exactly one** dimensionless
scalar — the sharpness Q — remains open, with a proof that fixing it numerically *is* tuning.

The keystone is structural: **the envelope is a one-parameter family in Q. Every LOCATION in it is forced
and Q-invariant; every MAGNITUDE scales with Q and is fixed by no inherited constant.** Model the partition
near its place as a driven damped resonator whose natural frequency is the **frozen** Greenwood CF(x); the
BM-velocity response is the universal single-pole resonance `|V(ω)|² ∝ ω²/[(ω0²−ω²)²+(ω0ω/Q)²]`. From that
one form, with no free choice but Q, the peak place, the apical-cutoff side, and the group-delay peak all
fall out fixed, while the width, height, slope, and absolute delay all carry Q and nothing else.

| feature of the envelope | what sets it | status |
|---|---|---|
| **peak place** (where a tone peaks) | frozen √-law / Greenwood CF(x) = E1 place | **forced, Q-invariant [F]/[V]** |
| **apical cutoff** (which side dies) | reactance sign `χ=1−(f/CF)²` flips at CF | **forced, Q- & κ-free [F]/[V]** |
| **group-delay peak** (where delay is max) | resonance phase, peaks at CF | **forced, Q-invariant (high-Q) [F]/[V]** |
| **−3 dB width / sharpness** | the single scalar **Q** (damping r, active gain) | **[O] — a number = tuning** |
| **cutoff slope** (dB/octave) | Q + fluid mass-loading prefactor | **[O]** |
| **peak gain / height** | active gain fraction G (E3) | **[O] (= E3)** |
| **absolute group delay** (ms) | Q, ρ, duct height H, BM mass | **[O]** |

## Results (every number reproduced offline, bit-for-bit)
- **The amplifier gene reproduces; nothing inherited moved.** SLC26A5 (prestin / OHC active amplifier)
  recomputes from the frozen cache as γ(level)=1.4023 + A4 shape (amp 0.18186, range 0.74919), bit-for-bit
  with the atlas (A4 = signal − γ, |mean(shape)|<1e-9). E6 fetched no gene and changed **no inherited
  byte** — the full frozen-hash set is identical to v0.6.0 (gate G2 verifies). The amplifier is reproduced
  here only to anchor the E3 bridge; its γ is **never** used as a damping, a Q, or a force. **[V]**
- **The PEAK sits at CF for EVERY Q — the keystone.** The BM-velocity peak is at ω=ω0 independently of the
  damping (analytic: `d/dω[ω²/((ω0²−ω²)²+(ω0ω/Q)²)]=0 ⇒ ω=ω0` exactly), verified on a grid for
  Q∈{0.8,10,100} with max|ω_peak−ω0|=2.0e-06 ≤ one grid step (7.0e-06). And ω0(x)=CF(x) is the **inherited**
  Greenwood place, so the envelope peak **is** E1's forced place: f=500/2000/8000 Hz peak at
  x=0.2817/0.5300/0.8059, equal to the E1 inverse-Greenwood place to |Δ|=0.0000. The near-peak FORM is the
  universal single-pole resonance; its LOCATION is forced. **[F]/[V]**
- **The ASYMMETRY is FORCED by the reactance sign — apical cutoff, not basal.** The partition reactance
  `χ(x;f)=1−(f/CF(x))²` is **positive** (stiffness-controlled, real wavenumber, the wave **propagates**)
  basal of the place and **negative** (mass-controlled, imaginary wavenumber, **evanescent**) apical of it.
  So a tone propagates basal of x\* and is **cut off apical** of it — the textbook gradual-tail / steep-
  apical-cutoff asymmetry, with the SIGN robust to the [O] cutoff-steepness scale κ∈{2,6,12,25} (apical
  10%-width < basal 10%-width for every κ; κ sets the slope, not the side). The cutoff's **existence and
  side** are forced and Q- and prefactor-free; its **slope in dB/octave** needs Q + the fluid mass-loading
  prefactor → [O] (N2). **[F]/[V]**
- **The sharpness is EXACTLY one scalar Q — the −3 dB bandwidth is ω0/Q.** The half-power roots of `|V|²`
  satisfy `ω²∓(ω0/Q)ω−ω0²=0`, whose difference is **ω0/Q exactly**: for Q∈{3,10,30,100} the numeric
  −3 dB velocity bandwidth equals ω0/Q to machine precision (max|Δ|=1.0e-16). The peak PLACE is Q-invariant
  (above); only the WIDTH carries Q. So the envelope's sharpness is precisely the single dimensionless
  scalar Q — nothing more, nothing less. **[F]/[V]**
- **The active amplifier is NEGATIVE DAMPING — the E3 bridge.** The active process enters as negative
  damping, `Q_eff = Q0/(1−G)` in the gain fraction G: for G=0/0.5/0.8/0.95 the effective Q rises
  5→10→25→100 (sharper, taller). As G→1 the net linear damping → 0 and the linear gain diverges — capped by
  the cubic; **at** the critical point (the R19 cubic g=0) the steady response is the **inherited** cube
  root `settle(0,F) ≈ F^(1/3)` (fitted exponent 0.333333 over F∈[0.1,100], |Δ|=1.3e-15). The active
  process SHARPENS the envelope (raises Q_eff), RAISES the peak gain, and at criticality imposes the E3
  compressive cube root. The **direction** is forced; the gain **magnitude** G (proximity μ to the
  bifurcation) is the inherited E3 [O] (N3). **[F]/[V]**
- **The GROUP DELAY peaks at CF.** The resonance phase lag `Φ(ω)=atan2(ω0ω/Q, ω0²−ω²)` rises
  0→π/2(at ω0)→π, and the group delay `τ=+dΦ/dω` peaks at ω0 with magnitude **2Q/ω0**: for Q∈{5,20,80} the
  delay peak sits at ω→ω0 (0.99498→0.99969→0.99999 as Q grows) with τ_max = 10.025/40.006/160.001 matching
  2Q/ω0 = 10/40/160. The cochlear group delay is greatest **at** the characteristic place (location forced,
  high-Q); the peak magnitude 2Q/ω0 scales with Q, so the absolute delay in ms is [O] (N4). **[F]/[V]**
- **The META-result — one knob, and fixing it is tuning.** Varying Q ×10 (10→100) leaves the peak place
  invariant (ω=1.000002) while the −3 dB bandwidth scales exactly ∝1/Q (0.10000→0.01000). LOCATIONS forced
  and Q-invariant: peak place (A), apical-cutoff side (B), group-delay peak (E). MAGNITUDES that scale with
  Q: peak width/Q10dB (C), peak gain/height (D), cutoff slope (B), absolute group delay (E). **None** of
  those magnitudes is fixed by an inherited constant — the √-law fixes ω0 (the place), the wave speed
  √(B/ρ) fixes propagation, and γ is promoter STRUCTURE only (firewall), **not** a damping. The only things
  that set Q are the partition damping r and the active gain, neither derivable without a measured/fitted
  number. Therefore a **closed numeric envelope = a CHOICE of Q = TUNING (forbidden)**. E6 does not close
  the [O]; it **characterises** it: FORM forced, exactly ONE scalar Q open. **[F]**

## Honest negatives / open items (preserved, not hidden)
- **N1.** The absolute **SHARPNESS is [O]**: Q / Q10dB / the −3 dB bandwidth in Hz / the peak gain in dB.
  Only the FORM (single-pole resonance), the EXACT bandwidth LAW (=ω0/Q), and the peak PLACE are forced. A
  number for Q would require **tuning** — forbidden.
- **N2.** The apical cutoff **SLOPE (dB/octave) is [O]** — it needs Q plus the long-wave fluid mass-loading
  prefactor (∝√(ρ/(H·m))). Only the cutoff's **existence** and **side** (apical) are forced (the reactance
  sign), robust to the decay scale κ.
- **N3.** The active gain **MAGNITUDE** (the fraction G, equivalently the proximity μ to the Hopf/critical
  point) is the **inherited E3 [O]**. E6 forces only the **direction** (active → higher Q_eff, higher gain,
  → cube-root compression at criticality), never the amount of gain.
- **N4.** The **ABSOLUTE group delay (ms)**, the phase in cycles, and the traveling-wave **speed** are [O]
  — they need ρ, the duct height H, and the BM mass (Lighthill / Zweig hydrodynamics). Only that the delay
  **peaks at CF** (location) and that phase accrues monotonically through CF is forced.
- **N5.** The model is the **LONG-WAVE (1-D, WKB) approximation**. The full 2-D/3-D fluid problem, the
  short-wave region right at the peak, the "second filter," and the active feedback's spatial extent are
  **not** captured — the deeper [O] hydrodynamics. The forced results here are the near-peak resonance
  FORM, the reactance-sign cutoff, and the Q-invariances — not the full waveform.
- **N6.** **Two-tone suppression, distortion products, and combination tones** (the active nonlinearity's
  products) are downstream of the cubic but are **not** derived in this envelope — [O].
- **N7.** The felt percept of **pitch and timbre** is the **mind** volume's (firewall); E6 moves only the
  physical/mechanical envelope, not the experience.

## Why this matters, honestly stated
E6 is the discipline's hardest test: the seed was **named after** this open derivation — the inherited wave
module flags the fluid-loaded envelope as *"the named [O] this seed exists to take up"* — and the temptation
is to "solve" it by picking a sharpness that looks like a real cochlea. E6 refuses. Instead it proves what
the frozen substrate **does** force: the peak sits at the inherited place for every Q, the cutoff is apical
because the reactance changes sign there, the bandwidth is exactly ω0/Q, the active amplifier is negative
damping landing on the E3 cube root, and the group delay peaks at CF. Then it proves what the substrate
**cannot** force without a fitted number — the single scalar Q — and shows that the whole envelope is a
one-parameter family in it. The result is a black box turned into a **characterised** box: not a closed
number, but a precise statement of exactly which one number is irreducibly open and why writing it down
would be tuning. That is worth more than a pretty curve, because it is **falsifiable and honest**: every
forced claim is checkable, and the single [O] is named, not hidden.

## Naming note (flagged, not silently fixed)
Delivered in the unambiguous folder `research/E6-traveling-wave-envelope/` — this is **BLUEPRINT-E1
CONTENT** (the traveling-wave ENVELOPE, the seed's named [O]). To preserve every frozen hash and the
no-omission set, the **existing folders are NOT renamed**; the v0.3.0 label slip (BLUEPRINT-E2, the MET
switch, shipped in the folder labelled `E1`) therefore still stands flagged as a separate bookkeeping item.
What E6 changes is the **substance**: BLUEPRINT-E1's envelope now has a home and a characterised [O], rather
than being only a deferred target. A future session may reconcile `BLUEPRINT.md`'s E-numbering with the
folder names.

## Firewall
γ read promoter STRUCTURE only — it is **NOT** the partition damping, **NOT** the quality factor Q, **NOT**
the active force, a gain, a delay, or a clinical effect (the amplifier gene is reproduced offline ONLY to
anchor the E3 bridge and to show no inherited byte moved). **No disease claim** here — E6 is macromechanics;
it neighbours the E4 deafness goal but states none. No molecule, dose, in-vivo selectivity, or efficacy;
nothing diagnosed or treated. Every magnitude is **[O]** with its obstacle named. The percept of pitch and
timbre is the **mind** volume's.
