# Reproducibility Map — The Earth–Cosmos Volume

This package lets any reader (or an AI auditor) **verify every quantitative claim** of the
Earth–Cosmos volume by running short, self-contained scripts and checking their output against
the **exact expected values** listed below. Each script states, in its own docstring, the claim
it tests, its inputs, its algorithm, and its expected output. There is **no fitting and there
are no free parameters** anywhere in this package: every number follows from the π-chain anchor
(physics volume, DOI `10.5281/zenodo.17932566`) plus textbook masses and orbital elements.

## How to run

Run everything at once with `bash run_all.sh` (deterministic; all 27 scripts verified to run end-to-end, ~4 min total), or run scripts individually:

```
python3 ch1_inflow_rates.py
python3 ch3_gravity.py
python3 ch3_gate.py
python3 ch4_solar_system.py
python3 ch5_spin_tidal.py
python3 ch_galactic_spin.py
python3 ch6_galaxy_rar.py
python3 ch7_lattice_optics.py
python3 ch8_deficit.py
python3 ch8_bullet.py
python3 ch9_lattice_cmb.py
python3 ch12_sunspot.py
python3 ch_accuracy_dashboard.py
python3 ch10_ledger.py
python3 ch2_light.py
python3 ch2_lightangle.py
python3 ch2_grb.py
python3 ch2_goldstone.py
python3 ch2_stiffness.py
python3 ch2_relativistic.py
python3 ch2_gammashot.py
python3 ch2_collision.py
python3 ch2_shake.py
python3 ch2_gammacontent.py
python3 ch2_burstprop.py
python3 ch2_jammed2d.py
python3 ch2_upconvert.py
```

Requirements: Python ≥ 3.8 and `numpy`. `matplotlib` is optional (only for the figure in
`ch3_gravity.py`; the script runs without it). Each script is deterministic — no random seeds
are used; the integrators are symplectic kick–drift–kick, so results are reproducible to
machine precision on any platform.

## How to audit (AI-level)

For each row of the table below: (1) open the named script and read its docstring (claim,
inputs, algorithm); (2) run it; (3) compare the printed numbers to the **Expected output**
column; (4) read the **Status** column to know whether the result is meant to match standard
physics (*degenerate*), to go beyond it (*distinguishing*), or to be a flagged tension
(*conflicting*). A claim passes iff the printed numbers match to the stated precision and the
logic in the docstring contains no gap. The same numbers appear in the corresponding chapter
of the whitepaper, so the paper and the code are mutually checkable.

## Master verification table

| Whitepaper claim | Script | What it computes | Expected output | Status |
|---|---|---|---|---|
| Ch.1: inflow rate fixed by π-chain | `ch1_inflow_rates.py` | νₚ=3π⁴, νₑ=1, ν_H=3π⁴+1; Q/M; per-body Q | νₚ=292.2273, ν_H=293.2273, m_p/m_e=1836.118, Q/M=1.7522e29; Sun Q=3.485e59 … Moon Q=1.286e52 (Table 1) | internally coherent, externally unverified (anchor) |
| Ch.3 §4: force is 1/r², not 1/r⁵ | `ch3_gravity.py` (A) | stability of r⁻ⁿ central orbit (1% perturbation) | n=2 → r∈[1.00,1.04] **BOUNDED**; n=5 → r→41.3 **RUNAWAY** (stable iff n<3) | internal success (selects 1/r²) |
| Ch.3 §7: equivalence principle | `ch3_gravity.py` (B) | two test bodies, Q differing ×10⁴, in one field | max trajectory difference **1.88e-14** (identical) | internal success (EP as theorem) |
| Ch.3 §6: mass/G split is conventional | `ch3_gravity.py` (C) | orbit under (κ,Q) vs (κ/10⁶, Q·10⁶) | max trajectory difference **2.73e-13** (identical) | internal success (only κQ=GM is physical) |
| **Ch.3 gate physics: saturation + critical radius** | `ch3_gate.py` | speed limit → flux bound ‖S‖≤c·e_a; saturation Γ=Γ_max·g(e_a); choke radius from 1/r² drive | g(e_a)→1 (rate saturates at **g★**); r_ch=√(K_F/Bc)=**1.000** (measured 1.001), choked interior u=c | **mechanism shown (toy)**; G absolute value (four-wall) **open**; existence degenerate w/ capped force + standard horizon |
| Ch.4: orbits, periods, Kepler from inflow | `ch4_solar_system.py` | integrate 8 planets one period each under a=GM⊙/r² | periods Δ<0.73%, speeds Δ<0.7%, **T²/a³=1.00001 (scatter 9.6e-12)** | **degenerate** with Newton (consistency) |
| Ch.5: spin & tidal lock from inflow | `ch5_spin_tidal.py` | intrinsic spin-up; tidal locking; Earth–Moon tidal gradient; **Mercury 3:2 (part D)** | ω→v_sw/a; ω_spin/n: 4→**1.000**; Δg=**4.88e-5**=2GML/R³; **3:2 dominant non-sync (|H|=0.65), libration 23.8°, trapped at e=0.206** | degenerate (standard tidal physics); **3:2 mechanism reproduced**, capture **probability** model-dependent (open) |
| **Ch.6: galaxies & a₀ (DISTINGUISHING)** | `ch6_galaxy_rar.py` | **a₀=cH₀/2π**; one law Kepler→flat; NGC 2403 fit; **part E: α/δ=2π by cos-integration** | a₀(70)=**1.082e-10** (0.90× obs); ratio→1 (high g), →√(a₀gN) (low g); NGC 2403 **Υ=0.567, χ²/dof=1.99**; **α/δ=6.28319=2π** | **distinguishing** (a₀ derived); curve degenerate with MOND/DM; **2π=α/δ derived**, full-vs-reduced wavelength open |
| **Ch.7: cosmology** | `ch7_lattice_optics.py` | d_L=(c/H₀)(1+z)ln(1+z) on Pantheon+; angular-size minimum | VP **χ²/dof=0.50** vs ΛCDM 0.44 (Δμ≤0.145 mag); **z_min=1.72 (=e−1) vs ΛCDM 1.61** | SNe **degenerate** (dark energy interpretation-contingent); angular-size min **distinguishing** |
| **Ch.8: dark matter = deficit** | `ch8_deficit.py` | one deficit → flat curve + dark core + lensing | r_dark=1.0, dM/dr=4π≈**12.57** (flat); **core ρ=0 = absolute zero = no quanta = DARK**; rays bend | RAR coupling + darkness **explanatory**; amplitude degenerate; lensing sign now GR-matched (n=1−4Φ/c²>1), Bullet quantitative **open** |
| **Ch.8: colliding clusters** | `ch8_bullet.py` | deficit transport in a merger → lensing/gas offset vs τ_Δ/τ_coll | L_off=0.952; offset rises **0.15→0.86 L_off** with transition at τ_Δ~τ_coll (C1); √(Dτ)/L_off≈**0.04** (C2 pass) | offset existence **degenerate** w/ collisionless DM; **mechanism shown (toy), quantitative cluster gate open**; post-merger reattachment a proposed discriminator |
| **Ch.9: CMB = present lattice emission** | `ch9_lattice_cmb.py` | thermal lattice emission; black holes = critical inflow | **⟨KE⟩/⟨PE⟩=0.998**, dispersion slope→c (thermal modes = light); R_s, **n_max≈4e54** (no singularity), L≈**6e45 erg/s** (jets) | CMB mechanism **present** (not relic); 2.725K **not derived**; Big-Bang **objection** raised, no origin asserted |
| **Ch.10: honest ledger** | `ch10_ledger.py` | renders the per-chapter status chart (solid/degenerate/distinguishing/tension) + 3 boxed predictions | `ch10_ledger.png` (renderer, no new sim) | the volume's self-audit; lists what would falsify it |
| **Ch.5 transparency: galactic inflow vs planetary spin** | `ch_galactic_spin.py` | Ω_gal, a_gal, galactic tide; gal/solar tidal ratio per planet; tuning factor to matter at Earth | a_gal≈**1.96e-10** (~a₀ scale, near-uniform→no internal effect); gal/solar tide **1.2e-18 (Merc) … 5.4e-13 (Nep)**; needs **~5e16×** to matter at Earth | **negligible** for planetary spin (sized, not asserted); spins **accommodated** by local accretion; galactic tide non-negligible only for the Oort cloud |
| App E: sunspot as inflow-sink (HYP/SPEC) | `ch12_sunspot.py` | converging-inflow/downdraft sink: field concentration, cooling, Wilson depression | Bz 100 G→~3 kG; T~3800 K (~82% throughput cut); Wilson ~300 km | **conjecture (HYP/SPEC)**, degenerate with magnetoconvection; distinguishing claim = causal order; tension = observed flux-emergence-first; **not a result** |
| **Accuracy across scales (dashboard)** | `ch_accuracy_dashboard.py` | per-observable inputs (M/F/D) + predicted/observed/%/label, grouped by scale; figure | a₀ **90%** (distinguishing); NGC2403 **94%**, Kepler ≤**0.73%**, Moon/Mercury **100%** (degenerate); Venus sign (**accommodated**); galactic tide on planets **negligible** | synthesis; **no fitting** (imports per-chapter numbers); only free astrophysical param in the volume is Υ(NGC2403)=0.567 |

## Per-script summary

### `ch1_inflow_rates.py`
- **Claim.** The vacuum-annihilation (inflow) rate is forced by the π-chain: per nucleon
  νₚ=3π⁴≈292.227 s⁻¹, per electron νₑ=1 s⁻¹, per hydrogen atom ν_H=3π⁴+1≈293.227 s⁻¹; for bulk
  matter Q∝M with Q/M=ν_H/m_H=1.7522×10²⁹ quanta s⁻¹ kg⁻¹.
- **Inputs.** π; atomic mass unit m_u=1.66054e-27 kg; hydrogen mass m_H=1.6735e-27 kg; body
  masses (standard references).
- **Verify.** Printed constants and per-body table reproduce Chapter 1, Table 1. Ratios are
  exact (Q∝M); absolute values use the hydrogen anchor (heavier elements ≈0.2% lower — stated
  in §1.3 of the chapter).

### `ch3_gravity.py`
- **(A) 1/r² vs 1/r⁵.** A gravitating body is a *sink* that absorbs inflow momentum (force
  ∝ v_inflow ∝ 1/r²), not a tracer carried by the flow (which would feel (v·∇)v ∝ 1/r⁵). A
  central r⁻ⁿ force has stable circular orbits iff n<3, so a 1% perturbation stays bounded for
  n=2 and runs away for n=5 — the printed verdict. This is the chapter’s “why this and not
  that” step.
- **(B) Equivalence principle.** Inertia = inflow rate, so the test body’s Q appears in both
  the force (∝Q) and the inertia (∝Q) and cancels; two bodies differing in Q by 10⁴ follow
  identical orbits (1.88e-14).
- **(C) mass/G degeneracy.** Only κQ=GM enters an orbit; rescaling κ→κ/10⁶, Q→Q·10⁶ leaves the
  orbit identical (2.73e-13).
- **Note.** The strong-field *absolute* values (light bending 1.752″, the Schwarzschild
  coefficient, the absolute G) are **not** derived here — physics volume
  (DOI `10.5281/zenodo.17932566`). The saturation and critical-radius **mechanism**, however, is
  now shown by `ch3_gate.py` (below).

### `ch3_gate.py`
**Gate physics** (cosmos-volume PART 08: *Critical Radius, Choking, Saturation, Throughput*).
Shows the *mechanism* behind two results Chapter 3 imports — the saturating restoring channel
g★ and the inflow-reaches-c critical radius — from one ingredient, a finite transport speed.
- **(1) Flux bound (Prop. 8.1).** ‖v‖≤c forces **‖S‖≤c·e_a**, so the mean transport velocity
  u=S/e_a≤c. (Same bound ⇒ tr T≤c²·e_a ⇒ isotropic closure κ_T≤c²/3.)
- **(2) Saturation.** The active→stored rate is **Γ=Γ_max·g(e_a)** with g∈[0,1], g(0)=0 (e.g.
  Hill g=e^n/(K^n+e^n)). Since g≤1 the rate cannot exceed Γ_max → the restoring channel
  **saturates** (= g★). Verified: g(0)=0, g(K_Γ)=0.5, g(5K_Γ)=0.96→1; all families in [0,1].
- **(3) Emergent critical radius.** Inverse-square drive |F_r|=K_F/r² gives demand u_dem=K_F/(Br²),
  which meets the cap c at **r_ch=√(K_F/Bc)** (analytic 1.000, measured 1.001 in units r_ch=1).
  Inside r_ch the flow is **choked** (u pinned at c, χ_S=u_dem/c≥1) — a horizon-like critical
  radius from a flux capacity bound alone.
- **Honest scope.** Toy/normalised units (c=B=K_F=1); c, K_F, B, K_Γ, n are **inputs**. Does
  **not** derive the absolute value of G/g★ (four-wall **open**) or R_s=2GM/c² (linear-in-M is the
  uncapped geometric channel; the inverse-square *choke* radius scales as √K_F). Critical-radius
  existence is **degenerate** with the standard horizon; the distinguishing content is the
  finite, non-singular choked interior (Ch 9). No RNG; no fitting.

### `ch4_solar_system.py`
- **Claim.** The inflow force a=GM⊙/r² (GM⊙=κQ⊙) reproduces measured planetary periods, mean
  speeds, and Kepler’s third law.
- **Inputs.** AU/yr units (GM⊙=4π²); per-planet a, e, observed T and v (standard references).
- **Verify.** Printed table matches Chapter 4, Table 1 (periods <0.73%, speeds <0.7%, Kepler
  constant 1.00001 with scatter 9.6e-12). **Status: degenerate with Newton** — a consistency
  test, not a claim of superiority. Importance is economy (one π-fixed number Q does it all)
  and that the *same* Q gives non-Newtonian galaxies in Chapter 6.

### `ch5_spin_tidal.py`
- **(D) Mercury 3:2.** Eccentric spin–orbit pendulum θ''=-(σ²/2)(a/r)³sin(2θ-2f)-drag. Resonance strengths H(p,e) at e=0.206 (3:2 dominant non-sync, |H|=0.65); 3:2 a stable lock (resonant angle librates, 1.5 turns/orbit); capture: e=0.206→ω/n=1.5 (3:2), e=0.01→1.0 (1:1). Figure ch5_mercury.png. HONEST: capture probability is tidal-model/triaxiality dependent (consistency, not forced).
- **(A) Intrinsic spin.** A body accreting a one-sided (swirling) inflow spins up until its
  surface co-rotates with the swirl: torque dL/dt=Ṁa(v_sw−ωa) vanishes at ω_eq=v_sw/a. The
  script confirms ω→v_sw/a. Spin can be retrograde if the swirl is (Venus).
- **(B) Tidal locking.** The primary's inflow gradient drives a fast spin to synchronous
  rotation on a circular orbit: ω_spin/n: 4→1.000 (the Moon). **Honest limit:** the linear-lag
  model gives 1:1 but **not** Mercury's 3:2 resonance (needs a resonant constant-Q model, not
  implemented — flagged open).
- **(C) Tidal field = inflow gradient.** For the Earth–Moon system Δg=4.88e-5 m/s² equals the
  tidal approximation 2GML/R³, i.e. the tidal field is the gradient of the gravitational inflow
  (no separate postulate).
- **Status:** degenerate with standard tidal theory at the level of the torque; the content is
  that spin and tides follow from the single inflow principle.

### `ch6_galaxy_rar.py`  (with data file `NGC2403_rotmod.dat`)
- **(D) coefficient bound.** Empirical a0 fixes k in a0=cH0/k only to O(1) (k≈5–7, central ~5.7 at H0=70).
- **(E) 2π = α/δ (derived).** Reproduces α=<|cos|>=2/π and δ=((1/2π)∫[cos]_+)²=1/π² by direct cos integration, ratio α/δ=6.283185=2π (the SAME 2π as in m_p/m_e=2π·3π⁴, phys.vol §13.5.5). Wave identity: κ_opt=H0/c (wavenumber) → full wavelength λ=2π/κ_opt → a0=c²/λ=cH0/2π. Residual: full-vs-reduced wavelength (flagged).
- **(A) a₀ derivation — DISTINGUISHING.** The background inflow rate κ_opt=H₀/c becomes an
  acceleration a₀=c²κ_opt/(2π)=cH₀/(2π): 1.04–1.13e-10 for H₀=67.4–73 (≈90% of the empirical
  1.2e-10). MOND must *postulate* a₀; here it is *derived* from H₀. The long-noted coincidence
  a₀≈cH₀/2π is the content, not an accident.
- **(B) One law, two limits.** a=gN·ν(gN/a₀): high gN → a=gN (Kepler, ratio 1); low gN →
  a=√(a₀gN) (flat curve, BTFR v⁴=a₀GM).
- **(C) NGC 2403.** SPARC rotation curve reproduced by the law at the derived scale with one
  stellar Υ=0.567, χ²/dof=1.99, 73 points; outer V: observed 134, model 126, baryons-only 53
  km/s. No dark halo.
- **Honest status.** The curve *shape* is degenerate with MOND and with a tuned dark-matter
  halo (fitting one galaxy does not select the model). The *distinguishing* content is the
  derived scale a₀=cH₀/2π and the Solar-System-to-galaxy unification (~10 decades). The exact
  factor **2π is horizon/Unruh-motivated, not derived** (only a₀∼cH₀ is secure). **Prediction:**
  a₀ should track local/cosmic H₀ (MOND predicts a₀ constant) — the cleanest near-term test.
- **Data.** `NGC2403_rotmod.dat` shipped with the package; source SPARC (Lelli, McGaugh &
  Schombert 2016). Only Υ is fitted; a₀ is not.

### `ch7_lattice_optics.py`  (with data file `Pantheon+_extract.tsv`)
- **(A) No dark energy needed — degenerate.** The static lattice-optics distance
  d_L=(c/H₀)(1+z)ln(1+z) fits the Pantheon+ Hubble diagram (1580 SNe) with χ²/dof=0.50, against
  ΛCDM's 0.44; the two differ by at most |Δμ|=0.145 mag over z<2.3 (≈ the per-SN scatter). So
  the supernovae do **not** prefer either: **"dark energy" is interpretation-contingent.**
- **(B) Angular-size minimum — distinguishing.** With d_A=d_L/(1+z)², a standard ruler is
  smallest at **z=e−1≈1.72** (VP) vs ≈1.61 (ΛCDM) — a distance-ladder-free discriminator
  (conditional on the lattice realizing refractive focusing; see honest status).
- **(C) Hubble tension — candidate mechanism (HYP/SPEC).** Redshift is a path integral, so the
  inferred slope H_inf(D)=c⟨κ_opt⟩ is a line-of-sight average. With κ_opt=κ₀(1+η·δ_bg),
  H_local/H_global=1+η·δ_loc; the observed 73/67≈1.09 needs η·δ_loc≈0.09 (e.g. an O(1) sensitivity
  to a ~10% local density anomaly). Prints the relation and plausible (η,δ_loc) pairs. **Honest:**
  not a parameter-free fit; testable via H₀ correlating with local density and direction.
- **Not tired light.** Time dilation is built in (1+z=n_obs/n_em → observed (1+z) light-curve
  stretch) — the decisive break; classical static tired light predicts none and is excluded.
  Surface brightness dims as (1+z)⁻⁴ only **under the focusing assumption** (else (1+z)⁻²).
- **Honest status.** SNe fit uses *diagonal* errors (full covariance would tighten, degeneracy
  holds); the reciprocity d_A=d_L/(1+z)² (→ both z_min and (1+z)⁻⁴) is justified in the physics
  volume but is a **hard gate** in the cosmos optics module — without focusing, dimming is (1+z)⁻²
  and θ(z) has no minimum. BAO/fσ8 fit with standard ΛCDM (degenerate); CMB is Chapter 9.
- **Data.** `Pantheon+_extract.tsv` (columns zHD, m_b_corr, err, IS_CALIBRATOR), from Pantheon+
  (Scolnic et al. 2022; Brout et al. 2022). Only a marginalised offset is fitted.

### `ch8_deficit.py`
One depletion profile (sourced by baryonic annihilation) gives three effects at once:
- **(A) Gravitates — flat curve.** ρ_def∝1/r² → M_def∝r (large-r slope dM/dr=4π≈12.57) → v rises
  through the core then flattens to √(4πGA). Microphysical origin of Chapter 6's deep regime.
- **(B) Dark = absolute zero (the key point).** Inside r_dark=√(A/ρ_amb)=1.0 the medium is fully
  annihilated: ρ=0 → **no quanta → absolute zero** (temperature is quantum rotation) and no medium
  to carry light → empty, cold, **DARK**. The dark-matter core *is* the absolute-zero region.
- **(C) Lenses.** The surrounding density gradient (stiffness K falling faster than ρ → c²=K/ρ
  down → n>1) bends rays toward the deficit; the core is opaque. **Lensing sign is the GR-matched
  n≈1−4Φ_eff/c²>1 (post-Newtonian γ=1), locked to the rotation-curve potential; the open item is
  whether no-slip survives a joint RC+lensing fit — physics volume.**
- **RAR coupling automatic:** the deficit is the baryons' annihilation shadow, so it tracks the
  baryons (a puzzle for particle dark matter). **Bullet Cluster:** mechanism now demonstrated by
  `ch8_bullet.py` (see below); quantitative gate still open, not claimed as a success.
  **Absolute zero is reached here (deficit cores), not in normal space**
  (which keeps the CMB floor, Ch 9) — Chapters 8 and 9 are one account of the medium's temperature.

### `ch8_bullet.py`
The sharpest test of any non-particle deficit account: merging clusters (the "Bullet Cluster"
class) where the **lensing mass is offset from the X-ray gas**. Implements the cosmos-volume
PART 09 sec.9.4 transport model for the deficit field Δ(x,t),
`∂_t Δ + ∇·(Δ u_Δ − D_Δ ∇Δ) = (1/τ_Δ)(Δ_eq − Δ)`, for a bullet subcluster crossing a larger one
(galaxies ballistic; gas braked by a ram-pressure pulse; deficit on a 1-D grid), and measures the
lensing(Σ_eff = Σ_baryon+Σ_def)-vs-gas centroid offset just after pericentre.
- **Separation conditions** (C1) slow relaxation τ_Δ≫τ_coll, (C2) small diffusion
  √(D_Δ τ_coll)≪L_off, (C3) deficit advects with the **collisionless** galaxies, not the gas.
- **Result.** L_off=0.952; normalised offset rises monotonically from the stellar-baryon floor
  (**≈0.15 L_off**, fast relaxation, MOND-like failure) to the lensing-on-galaxies ceiling
  (**≈0.86 L_off**, slow relaxation, collisionless-DM-like), transition at **τ_Δ~τ_coll** = (C1);
  √(D_Δ τ_coll)/L_off≈**0.04** (C2 pass). Fractions f_gas=0.85, M_def:M_baryon=5:1 (as in real
  clusters) so a large offset is not a weighting artefact.
- **Honest scope.** Toy/normalised units: **no real masses, velocities, or weak-lensing maps**, so
  the observed ~0.2 Mpc offset of any specific system is **not** predicted; the PART 09 sec.9.6
  quantitative cluster gate (χ² vs real lensing+X-ray) is **open**. The offset's **existence is
  degenerate** with collisionless dark matter. **Discriminator (flagged, not tested):** finite τ_Δ
  predicts slow post-merger **reattachment** of the lensing peak toward the gas; collisionless dark
  matter never reattaches. No RNG; no fitting.

### `ch9_lattice_cmb.py`
- **(4) Planck shape from quantized modes.** Bose-Einstein occupation of the lattice modes gives u(ω)∝ω³/(e^{ℏω/kT}−1) (Wien peak ℏω/kT=2.82); RJ recovered classically; lattice cutoff deviation ~1e-30 at the CMB peak (Planck to ~30 decimals). Absolute T still not derived.
**Scope discipline:** explains a present fact (the CMB) by present physics; asserts no cosmic
origin; raises a present-physics objection to the Big Bang singularity (a question, not an
alternative).
- **Part 1 — CMB as present emission.** A warm lattice thermalises (⟨KE⟩/⟨PE⟩=0.998) and its
  thermal excitations lie on ω=c|k| (= light) → a warm medium radiates a thermal microwave
  background **now**, not as a relic. **Honest:** the absolute 2.725 K is **not** derived (CMB
  energy ~80× starlight) — physics volume.
- **Part 2 — black holes (present objects).** Horizon = critical inflow point (v=c at R_s);
  finite jamming density n_max~1/a³≈4e54/m³ (**no singularity**); rotating inflow → equatorial
  disk (R_c=ℓ²/GM) + evacuated poles → **jets**; power L~εṀc²≈6e45 erg/s (AGN-scale).
- **Big Bang objection.** If even a black hole cannot confine energy to a point (finite density;
  pumps it out as jets), how could the Big Bang's initial singularity? **A question grounded in
  present physics; no alternative origin is asserted** (cosmic history is out of scope — not
  verifiable to this work's precision).

### `ch2_light.py`
- **(A) Speed emergence — solid.** A right-moving pulse on a mass-spring lattice travels at
  c=a√(K/m): simulated 0.999, 1.998, 3.997 for K=1,4,16 (∝√K, R²=1), independent of amplitude
  (1.998 at amp=1 and amp=3). => **c²=K/ρ**, the foundation of the whole volume.
- **(B) Vacuum dispersion — THE CONFLICT (reproduced, not hidden).** A lattice disperses:
  v_g=c·cos(ka/2). The quadratic scale E_QG=√2·hc/(πℓ) = **115 keV** (ℓ=D=4.854pm) or **882 GeV**
  (ℓ=a=6.33e-19 m). Fermi GRB 090510 bound: E_QG,2 > 1.3e11 GeV = 1.3e20 eV. => predicted
  dispersion too strong by **15 orders (D) / 8 orders (a)** → **decisive conflict** unless light
  is effectively dispersionless (open). GW170817: v_GW=c (|dv|/c<1e-15) — a natural success.
- **(C) Angle theory (now load-bearing).** sin χ=λ/(mD): γ(1pm)→11.9° (longitudinal), green(532nm)→89.80°,
  red(633nm)→89.93°, radio(1m)→90° (transverse=light). D-independent: at a common order
  sin χ∝λ → sin χ_633/sin χ_532=633/532=1.190.
- **Honest status:** speed emergence **solid**; the transverse-mode vacuum dispersion reads as the
  volume's sharpest tension (8–15 orders vs Fermi), but the angle account (part C; `ch2_lightangle.py`)
  classifies γ as **quasi-longitudinal** — a different mode whose dispersion is *not* the transverse
  v_g=c·cos(ka/2) and is **not yet derived**. So this is **REFRAMED** from a flat conflict into an
  **open dynamical item** (not resolved): if that branch's ω(k), once derived, again gives keV–GeV
  dispersion the conflict returns. Consistent with the Fermi null at the mechanism level; the angle
  relation itself is externally falsifiable (§10.9).

### `ch2_lightangle.py`
- **Reproduces the physics-volume §10.9 angle table.** sin χ=λ/(mD), m=⌈λ/D⌉, D=4.854 pm. Output:
  radio(1m)→90.0°, red(633nm)→89.93°, green(532nm)→89.85°, X-ray(0.1nm)→intermediate,
  γ(1pm)→11.9°, γ(1fm)→0.012°; GeV-band γ → χ≈0.01–0.015°.
- **Point:** radio/visible light is near-transverse (χ→90°, as observed); gamma is **quasi-longitudinal**
  (χ→0°) — a *different mode* from optical light, not the same mode at short λ.
- **Why it matters (the reframing):** the Ch.2 dispersion conflict applied the **transverse** dispersion
  v_g=c·cos(ka/2) (k=2π/λ) to gamma. The angle table says gamma is the *other* branch, so that
  8–15-order figure rests on a mode identification the framework rejects → the "decisive conflict" is
  **downgraded** to conditional. It does **not** resolve the question: the quasi-longitudinal branch's
  ω(k) is not derived and cannot be read off the angle (naive attempts are self-inconsistent), so the
  residue is an **open dynamical** problem. Consistent with Fermi (no dispersion) at the mechanism level.
- **Honest status:** angle relation **internally derived (physics vol §10.9) + externally falsifiable**;
  gamma reclassification **reframes** the dispersion tension (not resolved); quasi-longitudinal
  dynamics **open**.

### `ch2_grb.py`
- **Reproduces the collective-disturbance mechanism** on the SAME lattice that carries light.
  Contrasts (A) an independent high-k photon packet (linear) vs (B) the disturbance launched when
  two inward inflows collide (nonlinear FPU-β).
- **Output:** (A) high-k packet **spreads ×11.1** (v_g=cos(k0/2)=0.732c<c → disperses); (B) collision
  pulse stays **coherent ×1.0** (dispersionless, like a GW — nonlinearity balances dispersion, a
  soliton/compression front). Contrast factor ≈ **11.1**.
- **Why it matters (first strand of the reframing):** the ch2 dispersion conflict assumes a burst is
  a stream of **independent** high-k photons. If instead a GRB is a **collective** disturbance (as the
  Fermi source GRB 090510 — a merger burst — and GW170817's GW+GRB-within-1.7s suggest), it arrives
  dispersionless, removing that assumption. Pairs with `ch2_lightangle.py` (second strand: gamma is
  quasi-longitudinal).
- **Honest status (the script says so itself):** toy normalised units; does **NOT** derive the
  keV–GeV gamma spectrum and does **NOT** close the dispersion problem; whether real GRBs are in this
  coherent regime is **open**. Mechanism shown; degenerate with the standard merger account on the
  GW–GRB coincidence.

### `ch2_goldstone.py`
- **Tests the deeper Goldstone/Maxwell mechanism** (physics-vol §14.0): light = Goldstone mode of the
  synchronized rotation-phase. (1) **Synchronization:** a mean-field Kuramoto ensemble with spread
  natural frequencies locks for strong coupling — order parameter **r→0.96** (common axis forms),
  incoherent at K=0. (2) **Goldstone dispersion:** the synced medium's mode is ω=2√(J/I)|sin(k/2)|
  (sim matches analytic <1%): **linear/dispersionless (v_g→c_eff) at long wavelength**, curving at high k.
- **Why it matters (deepest strand):** box_c (Maxwell) gives ω=ck **exactly** (dispersionless). The ch2
  conflict treats light as a generic phonon; §14.0 treats it as the Goldstone/Maxwell mode. The sim
  confirms dispersionless light at the radio/visible band where it's observed dispersionless.
- **Honest status:** synchronization → dispersionless **low-energy** light is a real win; it does **NOT**
  make gamma (high-k) dispersionless — the bare spin-wave curves there. Exact box_c up to gamma needs the
  §10.9 m=1 geometry or the curl-coupling being physically forced, which physics-vol §14.0.6/14.0.7 grades
  **Hm (hypothesis)**. The OPEN item is located precisely: is the EM Goldstone mode exactly box_c up to gamma?

### `ch2_stiffness.py`
- **Substrate-level point, quantitative** (physics-vol §0.5 N3/N4, §10.0): c is the VP lattice's
  **collective-stiffness** speed (exists without quanta), and ω=ck is **forced by symmetry** (grade Fm),
  with N4 making c a **causal ceiling** (nothing exceeds c).
- **Output (1) ceiling:** elastic lattice gives v_g=c·cos(ka/2) ≤ c for all k, amplitude-independent;
  long-wavelength v_g→c (dispersionless). **(2) gamma residual at the fundamental VP spacing a=6.33e-19 m:**
  E_QG,2 = √2·hc/(πa) ≈ **882 GeV** (vs 115 keV at the quantum diameter D) — still **~8 orders below** the
  Fermi GRB 090510 bound (1.3e11 GeV). Only the exact-continuum limit (E_QG,2→∞) clears Fermi.
- **Why it matters:** separates **forced** from **open**. The dispersionless *law* (ω=ck) and the *ceiling*
  are symmetry-forced (Fm); the only open item is whether light realizes the **exact continuum box_c**
  (no O((ka)²) lattice correction) up to gamma — i.e. the EM-mode "protection," graded Hm in §14.0.6.
- **Honest status:** the collective-stiffness ceiling is real and forced; the discrete realization still
  disperses (8-order residual at gamma); full resolution needs the exact-continuum protection. OPEN, but
  the open part is now a single well-posed quantitative question.

### `ch2_relativistic.py`
- **The quantitative Fermi gate** (physics-vol §0.5 N4, §14.0.5): two energy→velocity laws with
  **opposite** energy dependence. **Phonon** (non-rel., discrete, massless mode): Δv/c=+(E/E_QG)² —
  GROWS with E (the 882 GeV conflict). **Relativistic** (the c-ceiling structure): Δv/c=½(E₀/E)² —
  SHRINKS with E (anti-dispersion), v_g<c always; **massless (E₀=0) ⇒ v=c exactly, dispersionless**.
- **Output:** KG-lattice confirms v_g≤c throughout; massive mode's v_g rises toward c with energy
  (anti-dispersion); massless continuum mode at c. Fermi: relativistic law meets the bound for
  E₀≲10 eV and exactly for massless light; phonon law gives the 882 GeV residual.
- **Why it matters:** the relativistic c-ceiling makes **high energy the SAFEST case**, opposite to the
  naive "conflict worsens at high E." Light is the massless Goldstone mode → dispersionless. The
  "conflict" is the artifact of applying the non-relativistic phonon law to light.
- **Honest status:** still OPEN — on the lattice even a massless mode carries the phonon v_g=c·cos(ka/2);
  exact-c is a continuum statement, so the lattice-vs-continuum (exact box_c / protection) item remains
  (Hm). Linear collective coherence does NOT change the central velocity; the coherence-length question
  reduces to the protection question. (C) reframed the conflict favorably but did not close it.

### `ch2_gammashot.py`
- **"Shoot a gamma and watch it move"** (user's suggestion): a 2D lattice launch of a gamma (high-k)
  vs visible (low-k) wave packet, watching propagation, peak/front speed, and transverse spread.
- **Output:** the gamma packet **disperses** — peak speed ≈0.43c (=c·cos(ka/2)) vs visible ≈0.98c;
  the gamma beam spreads **LESS** transversely (×1.5) than visible (×3.7), i.e. **no 90° fan-out**
  (shorter wavelength diffracts less → tighter beam).
- **Why it matters:** directly *demonstrates* the dispersion is real for any lattice wave packet, and
  *refutes* the conjecture that gamma energy escapes sideways at 90°. (The textbook signal-velocity=c
  is an impulse-only, exponentially-tiny forerunner a smooth gamma pulse does not carry.)
- **Honest status:** CONFIRMS the dispersion rather than removing it. The resolution cannot live in the
  packet's motion → it must be that light is NOT a lattice packet but the massless continuum mode
  (v_g=c exactly, §2.7–2.9). Sharpens the one open item; does not close it.

### `ch2_collision.py`
- **Collision test** (user's correction: probe with a destructive collision, not a tuned wave): a
  head-on packet collision plus an amplitude scan and a wavelength scan on a 1D lattice.
- **Output:** (1) colliding packets pass through unchanged; (2) speed is **identical** for amplitude
  ×1/×3/×8 (gentle → destructive) — amplitude-independent, set by the stiffness; (3) speed **falls
  with wavelength** at fixed stiffness K (≈c at k=0.2, ≈0.04c at k=2.6), tracking c·cos(ka/2).
- **Why it matters:** separates the two parts of the "stiffness ⇒ c" argument. The stiffness
  correctly fixes the speed regardless of amplitude/violence (the user is right on the **amplitude
  axis**); but the dispersion is a **wavelength** effect from the discreteness, which constant
  stiffness does NOT remove — it vanishes only in the continuum.
- **Honest status:** confirms amplitude-independence (settled) and isolates the open item to the
  wavelength/discreteness axis. A physical case FOR light = continuum elastic-stress mode (§0.5),
  but does not derive that the discreteness residual is exactly zero. Open (Hm).

### `ch2_shake.py`
- **Shake test** (user's relay/re-emission picture: what crosses space is the lattice vibration,
  re-emitted region to region, not the original packet): shake the lattice and watch the vibration
  travel and spread, for a long-wave vs a gamma-wavelength vibration.
- **Output:** long-wave vibration relays at c (~0.99c) and stays coherent (RMS ×1.1); gamma-wavelength
  vibration travels at v_g (~0.58c) and **smears by ×16** over even less distance.
- **Why it matters:** confirms the user's inference — a literal short-wave (gamma) packet would
  disperse away over cosmic distance, so what we detect must be the coherent continuum vibration.
  The data force light = the dispersionless continuum mode; the lattice-vibration relay is the
  physical mechanism. (The true causal front is at c but is an exponentially-tiny forerunner.)
- **Honest status:** supports the continuum/relay picture and the data-driven inference. Does NOT
  derive that the discreteness residual is exactly zero — the exact-continuum realization (light is
  exactly the continuum elastic/Goldstone mode) is the one open Hm item.

### `ch2_gammacontent.py`
- **Gamma wavelengths inside lattice waves** (the burst-as-stiff-medium-event reading): (1) a churning
  / multi-scale disturbance carries broadband content reaching the gamma band and the lattice cutoff,
  while a smooth wave does not, and the gamma fraction is **amplitude-independent**; (2) energetics —
  light is one quantum, a burst is the whole shaken 3D volume, so E_burst/E_photon ~ V/a³.
- **Output:** churning front reaches the gamma band (~8% in 10–50 GeV at this calibration); smooth wave
  0%; fraction identical at amp ×1 and ×1e-4. E_burst/E_photon ≈ 2e54 for ~1e53 erg / 31 GeV; a fully
  gamma-excited ~1 m³ holds one burst; c⁴/G ≈ 1.2e44 N (= the modulus K in c²=K/ρ).
- **Why it matters:** supplies the burst's energy budget and a candidate spectrum (the gaps left by
  `ch2_grb.py`), and shows the gamma is many quanta over a volume, not a large per-quantum energy.
- **Honest status:** EMISSION side only. Does NOT address propagation (see `ch2_burstprop.py`).

### `ch2_burstprop.py`
- **Decisive propagation test:** launch a churning broadband disturbance and split it, as it propagates,
  into its low-k part (the GW-like front) and high-k part (the gamma content); track where each goes.
- **Output:** the low-k envelope travels at ~c; the high-k (gamma) content travels at v_g = c·cos(ka/2)
  < c and **separates**, lagging by (1−cos(ka/2))×distance — at the **same rate weak or strong** (the
  nonlinearity that keeps the envelope coherent does not bind the gamma to it). Matches the cos(ka/2)
  prediction.
- **Why it matters:** the decisive test of whether a burst carries its gamma coherently. It does not.
  Over cosmological distance the lag is the original Fermi conflict (ka~0.1, D~9 Gly → ~15 orders).
- **Honest status:** NEGATIVE for the dispersion rescue. The collective/gravitational-wave picture
  answers energy & spectrum but does NOT close the dispersion tension; that still needs the exact-
  continuum (□_c) mode (`ch2_goldstone.py`/`ch2_stiffness.py`). A jammed/density=1 vacuum doesn't help
  either (`ch2_jammed2d.py`).

### `ch2_jammed2d.py`
- **Density=1 (jammed / no-void) test in 2D:** does incompressibility remove the transverse (light)
  dispersion? Compare a compressible vs an incompressible (Leray-projected) lattice.
- **Output:** incompressibility **freezes the longitudinal channel** (a compression pulse is fully
  projected out) but leaves the **transverse dispersion cos(ka/2) unchanged** (identical compressible
  vs incompressible at all ka). Jamming rescales c, not the normalised dispersion.
- **Why it matters:** tests the no-void ⟺ density=1 idea as a dispersion escape. For light, it is not one.
- **Honest status:** CLARIFYING / negative. The deficit is locked to the transverse branch; density=1
  does not touch it.

### `ch2_upconvert.py`
- **Up-conversion test** (the second escape: maybe no gamma propagates — the wave crosses the cosmos and the
  gamma is produced locally when it shakes our lattice). Asks whether a gentle, long-wavelength (low-k) wave
  can shake the lattice down to the gamma (cell, high-k) scale, in 1D and in 3D.
- **Output:** high-k ("gamma") fraction generated stays at the per-cent level or below until the per-bond
  **strain approaches ~1**, and the threshold is the **same in 1D and 3D** (it is per-bond, hence
  dimension-independent). A non-dispersively propagated wave is smooth, so its strain ~ h ~ 1e-22 — about
  **20 orders below threshold**.
- **Why it matters:** settles the "local production" escape. A gentle arriving wave carries the energy
  (`ch2_gammacontent.py`) but is ~20 orders too weak to make the gamma. 3D changes the cascade richness and
  adds focusing, but focusing acts at the **converging source** (the merger), not in the **diverging** wave
  that reaches us.
- **Honest status:** NEGATIVE for local production. Together with `ch2_burstprop.py` (source-emitted gamma
  disperses off the front), both escapes fail → gamma must be the exact continuum (□_c) mode
  (`ch2_goldstone.py`/`ch2_stiffness.py`). (Numerics reliable in the gentle regime; at strain >~1 the
  integrator loses energy, but that regime is irrelevant — the arriving wave is gentle.)

## Status: complete

All ten chapters of the Earth–Cosmos Volume are covered. **Twenty-seven** runnable scripts (ch1–ch9, plus
ch3_gate, ch8_bullet, ch2_lightangle, ch2_grb, ch2_goldstone, ch2_stiffness, ch2_relativistic, ch2_gammashot, ch2_collision, ch2_shake, ch2_gammacontent, ch2_burstprop, ch2_jammed2d, ch2_upconvert, and the four transparency/synthesis scripts **`ch_galactic_spin.py`**, **`ch12_sunspot.py`** (App E), **`ch_accuracy_dashboard.py`**, and the Chapter-10 ledger renderer **`ch10_ledger.py`**) reproduce every quantitative claim — including the
vacuum-dispersion **tension** (ch2): both the transverse-mode estimate (`ch2_light.py`) and the
§10.9 angle reclassification (`ch2_lightangle.py`) and the collective-disturbance mechanism
(`ch2_grb.py`), and the Goldstone/Maxwell synchronization account (`ch2_goldstone.py`), and the collective-stiffness ceiling with the gamma residual at scale a (`ch2_stiffness.py`), and the relativistic energy–velocity law (`ch2_relativistic.py`) that together **reframe** it from a flat conflict into an open dynamical item, made reproducible rather than hidden. Chapter 10 is a synthesis (the honest
ledger); its figure `ch10_ledger.png`, rendered by **`ch10_ledger.py`**, summarises the degenerate / distinguishing / reframed labels
and the three falsifiable predictions, and **`ch_accuracy_dashboard.py` / Fig. `ch_accuracy_dashboard.png`** give the per-scale accuracy table with every input tagged measured / free / derived.


*Reproducibility map v1 — covers Chapters 1–10 (complete) plus the Ch.5 galactic-inflow transparency test, the App E sunspot conjecture, and the cross-scale accuracy dashboard. 27 scripts + 2 datasets. Updated as each subsequent chapter and
its script are completed.*

### `ch10_ledger.py` -- Honest-ledger synthesis (Chapter 10, TRANSPARENT)
Renders `ch10_ledger.png`: the per-chapter status chart (foundational/solid; degenerate consistency checks; distinguishing & testable; sharpest tension) plus the three boxed falsifiable predictions. No new simulation -- a classification/rendering of the numbers produced by the per-chapter scripts. DEPENDENCIES: matplotlib.

### `ch12_sunspot.py` -- Solar activity (Appendix E, HYP/SPEC, exploratory)
Sunspot as an inflow-driven converging/downdraft SINK. (1) flow toward a subsurface sink = converging inflow + central downdraft (Duvall et al. 1996); (2) flux freezing concentrates Bz 100 G -> ~3 kG (inflow organizes the field); (3) cooling by ~82% throughput suppression -> T~3800 K; (4) Wilson depression ~300 km from the magnetic-pressure deficit. Figure ch12_sunspot.png. HONEST: HYP/SPEC, degenerate with standard magnetoconvection; distinguishing claim = causal order (inflow-first vs field-first dynamo); tension = observed flux-emergence-first. Surface Evershed/moat outflow NOT modelled (separate component). Not a result.

### `ch_galactic_spin.py` -- Galactic inflow vs planetary spin (Ch 5, TRANSPARENT)
Full parameter transparency: all galactic-inflow knobs disclosed, free/tunable ones flagged (PASS_THROUGH_FRAC, EXTRA_GAL_TIDE). Galactic inflow at the Sun a_gal=v^2/R~2e-10 m/s^2 (~a0 scale) but a near-UNIFORM field -> no internal effect (equivalence principle); only the tidal gradient ~Omega^2~8e-31/s^2 acts internally = 1e-13..1e-18 of the Sun's tide at the planets -> NEGLIGIBLE. Obliquities 0-177deg uncorrelated with the galactic direction. To matter at Earth needs ~5e16x the measured galactic tide (unphysical). Planetary spins are ACCOMMODATED (not predicted) by accretion history. Figure ch_galactic_spin.png.

### `ch_accuracy_dashboard.py` -- Accuracy across scales (synthesis, TRANSPARENT)
The cross-scale audit asked for by the user: one row per observable giving the inputs (each tagged M=measured / F=free / D=derived), the predicted value, the observed value, the % accuracy, and an honest label (predicted / distinguishing / degenerate / accommodated / negligible / open). Groups: GALACTIC (a0=cH0/2pi = 90% of the RAR scale, the one *distinguishing* row; NGC 2403 fit 94% with the single free Upsilon; BTFR slope 4), SOLAR-SYSTEM (Kepler periods <=0.73%, the Sun's *local* inflow, degenerate), SPIN/SAT (Moon 1:1 and Mercury 3:2 reproduced = degenerate; Venus retrograde *accommodated* by a free swirl sign), and the GALACTIC KNOB sized honestly (galactic tide on planets = 1e-18..1e-13 of the Sun's = negligible; ~5e16x tuning to matter at Earth). **No fitting in this script** -- every number is imported unchanged from ch6_galaxy_rar.py / ch4_solar_system.py / ch5_spin_tidal.py / ch_galactic_spin.py, so the dashboard is mutually checkable against them. The honest message: the disclosed galactic variables solve the *galactic* scale; planetary spins are local/accommodated and the galactic knob adds nothing measurable. Figure ch_accuracy_dashboard.png (panel A accuracy-by-label bars; panel B the negligible galactic tide per planet).
