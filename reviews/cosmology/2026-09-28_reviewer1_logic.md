# Cosmology volume: review 1 of 3 (derivation chain and inheritance)

**Reviewer:** 1 of 3 (lens: derivation chain, inheritance from physics, declared seams)
**Date:** 2026-09-28
**Scope read:** AGENTS.md; physics `lt-light-chain-doubts-and-resolutions` (Links 1 to 8, incl. 6a); physics `w0` scorecard, `17-extensions` (EP scope update), `axg`, `05` (α = 2/π); cosmology hub, 00, 01, 02 (all five sub-pages), 03, 03.1, 06, 06.1, 07, 08, 09 (BH), 10, 11, 12, 13 (partial), 16 (ledger, predictions, open problems), App. A, C, D, G, I (partial), `_decl.json`, `repro/cosmology/` tree, `IRREPRODUCIBILITY_LEDGER.md`.
**Rule applied:** data decides the theory. A claim counts only when data support it and code in the repo reproduces it. Anything else goes on a data-pending list and is not argued.
**No file under docs/ or repro/ was edited.**

---

## Summary table

| id | sev | one line |
|---|---|---|
| C1 | critical | The equivalence principle is sold as a "theorem" (Ch 3). Physics now claims it only at the cap level, marks it [O] beyond that, and cosmology's own Ch 1 rates break it. |
| C2 | critical | The inflow profile contradicts itself: Ch 3 has v ∝ 1/r², while Ch 9 (the BH river and the light bending) has v = c√(R_s/r) and calls it "the inflow of Chapter 3". |
| C3 | critical | Light and GWs are called *shear* waves of the lattice (Ch 2, Ch 11). The physics substrate has G → 0 and explicitly claims no shear wave. |
| C4 | critical | The a₀ = cH₀/2π chain has four gaps: κ_opt changes identity three times, two unrelated 2π's are conflated, the full-cycle choice is post hoc, and the ν interpolation is borrowed from MOND/RAR. |
| C5 | critical | Dark matter as a "deficit" contradicts Ch 3 and Ch 12 ("only a sink gravitates") and the no-void axiom P1 (the core has "no quanta"). |
| C6 | critical | Code is missing. Only 1 science script exists in `repro/cosmology`. The ~10 scripts and the Pantheon+ data cited on the pages are absent. |
| M1 | major | The 633/532 two-line ratio, which physics has retired as evidence, is still used as a "D-independent test", a "reality-mapping" closure and a "datum on record". |
| M2 | major | The cell a = 6.33×10⁻¹⁹ m is treated as a physical SI anchor and LOCKed. Physics says it depends on the arbitrary N = 10¹² container, so E_QG = 882 GeV, the gamma-burst spectrum and the BH core all inherit N. |
| M3 | major | Parts of the post-Newtonian sector that physics marks [O] (full metric, PPN γ) are called "forced" here. The redshift rests on the C1 EP "theorem". Light bending is derived two incompatible ways. |
| M4 | major | The grading vocabulary is out of date ([O] = "external input"; no [V]/[L]/[H]). [F] is attached to data fits and to identifications. |
| M5 | major | The dispersion prediction cannot fail: App G says detection kills the framework, while §16.1 says detection "confirms" it. The hub calls it "parameter-free" even though it depends on N. |
| M6 | major | The "single input" ν_H = 3π⁴+1 has no observable consequence: it cancels against the fitted κ. What remains is its composition dependence, which is falsified (C1). |
| M7 | major | The E/B reading on the Goldstone page is the older one. It is not synced with physics Link 6a ([H], data-pending lattice run). E2 and the amplification A are never inherited. |
| M8 | major | Prediction 1 ("a₀ tracks H₀ across epoch/environment") is not defined in a static cosmology, and its criterion is asymmetric. Ch 7's environment-dependent κ_opt implies a ~9 % a₀ variation that no page states. |
| M9 | major | There are two separate flat-curve mechanisms (the Ch 6 ν law and the Ch 8 isothermal deficit). They are never reconciled, so the mass could be double-counted. |
| m1–m8 | minor | Badge, notation, dropped conditions, neutron extension, D-sensitivity, headline inconsistency, P4 wording, ownership notes. |

---

## Critical

### C1. The equivalence principle as a "theorem" is superseded by physics and contradicted by cosmology's own inputs
- **Pages:** `docs/cosmology/03-gravity-momentum-absorbed-inflow/` (step 9); `docs/cosmology/10-post-newtonian-sector/`; `docs/cosmology/16-honest-ledger-falsifiable-predictions/` (row "Post-Newtonian sector"); `docs/cosmology/01-single-input-inflow-rate/`; `docs/cosmology/11-gravitational-waves-medium-perturbations/` (dipole argument).
- **Evidence (cosmology):** "the equivalence principle follows as a theorem"; "a body's inertial mass is m=βQ with the same universal β for all matter"; "obtained here as a theorem rather than assumed as a postulate". In Ch 10: "The redshift follows cleanly from the equivalence-principle theorem already proved in Chapter 3."
- **Evidence (physics, current):** `17-extensions`, Update 2026-09-28: "The equivalence principle is claimed only at the velocity-saturation (cap) level … Beyond the cap it is not claimed … the rate-to-mass relation differs between proton and electron … EP beyond the cap [O], obstacle = absolute 9.8 m/s² from the lattice."
- **Internal contradiction:** Ch 1 sets ν_e = 1 s⁻¹ and ν_p = 3π⁴ ≈ 292 s⁻¹ and stresses "the electron contributes a whole unit … not a mass-weighted fraction". So the rate per unit mass is (1/m_e) for the electron against (292/1836)(1/m_e) = 0.159/m_e for the proton, a factor of about 6.3. The claim m = βQ with a universal β is therefore false for the framework's own particles. Two further effects follow:
  - Ch 1 admits a composition spread of Q/M of about 0.2 % between hydrogen and heavier matter.
  - Q counts nucleons, not mass-energy. Nuclear binding energy (about 0.8 % between H and Fe) therefore also makes Q/M depend on composition.

  Both are about 10¹² to 10¹³ times larger than the MICROSCOPE/Eöt-Wash bounds (~10⁻¹⁵). Ch 1 calls this spread a "known, sub-percent uncertainty", but in fact it is a falsified prediction.
- **Simulation B cannot fail:** the acceleration is coded as a = κQ_source/r² with no Q₂ in it, so the "1.9e-14 identical trajectories" check holds by construction. The same applies to Ch 11's "no dipole radiation": dipole radiation vanishes only if the gravitational charge is proportional to inertial mass.
- **Why it matters:** the EP is load-bearing for Ch 3, Ch 10 (redshift), Ch 11 (dipole) and the ledger. Cosmology upgrades a parent item that is [O], and does so against its own inputs.
- **Fix:**
  - Downgrade the EP to physics' current scope: [F?] at the cap level, [O] beyond it.
  - Delete "theorem" and the m = βQ step, or mark m = βQ as [H] with the proton/electron conflict stated.
  - Add the composition-dependence estimate against MICROSCOPE as an explicit **conflicting** row in §16.
  - Re-ground the Ch 10 redshift on physics §18 (the processing-rate clock), not on the EP.
  - Retire Simulation B as evidence, since it cannot fail.

### C2. Two incompatible inflow profiles
- **Pages:** `03-gravity-momentum-absorbed-inflow/` (steps 3 to 6) against `09-black-holes-jets-critical-inflow/` (horizon, light bending), `03-gate-physics-saturation-critical-radius/`.
- **Evidence:** Ch 3: "the inward flux through a sphere of radius r equals the annihilation rate … The inflow speed falls as 1/r²", and the force is F = Q₂ m_q v(r), which is ∝ 1/r² only because v ∝ 1/r². Ch 9: "The inflow of Chapter 3 reaches the wave speed at a finite radius: with v_inflow(r)=c√(R_s/r)"; "A wave in a medium falling at v(r)=c√(R_s/r) … n(r)≃1+v²/c²=1+R_s/r".
- **Why it matters:** these cannot both hold.
  - A 1/r² inflow reaches c at r = √(Q/(4πn₀c)), not at 2GM/c².
  - If the true profile is r^(-1/2), the Ch 3 force law becomes F ∝ r^(-1/2), not 1/r².
  - The black-hole horizon and the Eddington bending (which the volume "owns" as of v2) therefore do not follow from the Ch 3 derivation. They are imported in Painlevé–Gullstrand form under a claim of continuity.
- **Fix:** either
  - (a) derive a single profile from the medium, or
  - (b) declare the Ch 9 river velocity a separate identification ([H]), state that it is not the Ch 3 conservation flux, and grade the horizon and bending as conditional on it.

  Record the seam in App D.

### C3. "Light = shear/transverse wave" and "GW = propagating shear" contradict the substrate
- **Pages:** `02-light-lattice-elastic-wave-sharpest/` (steps 1 and 2, simulation), `11-gravitational-waves-medium-perturbations/`, §16 ledger row "Gravitational waves".
- **Evidence:** Ch 2: "Transverse waves are light. The shear (transverse) mode of the lattice carries the two polarizations of light … This identifies light with the transverse elastic wave." Ch 11: "A gravitational wave is a propagating shear of the same medium … one medium with one elastic modulus and one density"; "the shear character of the gravitational perturbation removes [the breathing mode]". Ledger: "transverse lattice shear gives two TT polarizations".
- **Physics (current):** Link 2: at z = 6 "G is driven to zero … exactly one propagating elastic speed … It is a longitudinal speed." Link 6a / Doubt 6a: "there is no transverse shear wave, and the framework does not claim one"; the polarizations come from the rotating quanta, E = swing, B = rotational response, [H].
- **Further problems:**
  - A shear wave in a G → 0 medium has speed √(G/ρ) → 0. So "c_gw = √(K/ρ) = c automatically" contradicts "GW = shear".
  - If the GW rides the one longitudinal branch instead, the scalar breathing mode that Ch 11 rules out is exactly what you get.
  - The Ch 2 speed and isotropy evidence comes from a 1-D mass–spring chain and an **fcc crystal with coordination 12**. That is a shear-rigid crystal, not the isostatic jammed packing, so it does not test the physics claim. A 1-D pulse at a√(K/m) is also a textbook identity that cannot fail.
- **Fix:**
  - Rewrite Ch 2 steps 1 and 2 to physics Links 2 and 6a: longitudinal scaffold c² = B/ρ plus the transverse swing of rotating quanta, [H].
  - Ch 11 must state which branch carries GWs and how TT polarization arises without a shear modulus. Until a lattice run shows it, make it [O] or [H] with that run as the data-pending item.
  - Retire the fcc and 1-D checks as evidence for the jammed substrate.

### C4. The a₀ = cH₀/2π chain: gaps, conflation, post-hoc choice, borrowed law
- **Pages:** `06-galactic-rotation-derivation-a0-ch0/` (steps 2 to 5), `06-why-galactic-rotation-distinguishing/`, `axg-governance-no-tuning-lock-gate/` (anti-circular chain), `axf-…` scorecard ("a₀ … [F]"), `16-open-problems-gathered/`.
- **Gap 1: κ_opt changes identity.**
  - Ch 7 defines κ_opt as a photon **energy-loss coefficient** (dE/E = −κ_opt ds), [INPUT] fixed by the Hubble law.
  - Ch 6 step 2 turns it into "a universal background **inflow**", with no derivation linking photon attenuation to a mass flow of the medium.
  - Ch 6 step 4 then turns it into "the background lattice wave's spatial frequency—a wavenumber". An attenuation coefficient is not a wavenumber of any wave.
  - Each re-identification is a hidden assumption.
- **Gap 2: step 3 is dimensional analysis only.** "A rate-per-length κ_opt combined with … c defines an acceleration … the acceleration below which the background processing … is no longer negligible compared with a body's own inflow." No comparison of the two inflows is computed.
- **Gap 3: two different 2π's are conflated.** Ch 6 says the 2π "is the framework's canonical full-cycle constant 2π=α/δ=(2/π)/(1/π²) … the same 2π that gives m_p/m_e = 2π·3π⁴". Physics §5.1 defines α = ⟨|cos θ|⟩ = 2/π, a rectification average. The wavenumber-to-wavelength 2π (λ = 2π/k) is a different quantity. Equal numerical value is not shared provenance. The scorecard entry "Geometric 2π=α/δ [F] (verified)" certifies arithmetic, not the identification.
- **Gap 4: the choice is post hoc.** The page admits that the "identification of the relevant length as the full wavelength rather than the reduced λ̄=R_H (which would give the bare cH₀)" is a "modelling choice", supported by "the ~90 % empirical match". The bare cH₀ would be 5.7× too large. The 2π is therefore selected by the data it is then said to predict. The coincidence a₀ ≈ cH₀/2π has been known since Milgrom (1983). "part D … places the coefficient in the consistent band k≈5–7" is a fit of the coefficient to the empirical scale.
- **Gap 5: the deep-regime law is borrowed.** Step 5 says "The two limits are forced, not chosen", but the status block says "The interpolation function ν is taken in the standard RAR form rather than derived". Flat curves and the BTFR (v⁴ = a₀GM) come entirely from that borrowed ν. No inflow mechanism yields a = √(a₀ g_N). App G's anti-circular chain nonetheless says "The radial-acceleration relation and flat curves follow from steps 3 and 5". This is a silent seam to the MOND/McGaugh literature.
- **Also:** H₀ is [INPUT] in both volumes (physics w0: "κ_opt=H₀/c … [INPUT]"). The "derivation" is at most a relation between two measured scales. The ~10 % shortfall (0.87 to 0.94) is not graded against the McGaugh et al. uncertainty.
- **Why it matters:** this is the volume's headline and its "one distinguishing result". It is graded [F] "derived", and App G says "'derived' is reserved for [F]".
- **Fix:**
  - Grade a₀ = cH₀/2π as [H]: identification of the attenuation rate with a background wave, full-cycle length chosen.
  - Grade the numerical agreement as [V data] at ~10 %, with the empirical a₀ uncertainty quoted.
  - Declare the ν interpolation as imported (MOND/RAR literature) in App D.
  - Delete "forced, not chosen" and "the same 2π as 6π⁵", or keep them only as numerology notes.
  - Put a derivation of κ_opt as an inflow on the [O] list with its obstacle.

### C5. Dark matter as a "deficit" contradicts Ch 3, Ch 12 and the no-void axiom
- **Pages:** `08-dark-matter-vacuum-deficit/`, `12-cosmological-puzzles-that-dissolve/`, `03-gravity-momentum-absorbed-inflow/`, `01-single-input-inflow-rate/` (P1).
- **Evidence:**
  - Ch 12: "only a sink—a region that annihilates quanta—produces a net inward flow and therefore gravitates. A uniform … background … exerts no gravitational force."
  - Ch 8: "The deficit gravitates … v²=GM_def/r". A deficit is an absence of medium, not a sink.
  - Ch 3 assumes "n₀ the undisturbed number density of the medium (a universal constant)" around every sink. That leaves no room for a steady 1/r² density deficit, which Ch 8 simply asserts ("The depletion profile that a steady sink leaves is isothermal, ρ_def ∝ 1/r²").
  - Ch 8: "inside r_dark there are no quanta … literally empty". P1 (Ch 1 and physics Link 1): "fully packed (“no-void”)", and Ch 3 step 2 derives the inflow **from** no-void refilling.
- **Why it matters:** the chapter violates the axiom its own gravity derivation depends on. It also gives missing medium a positive gravitational sign without derivation (naively, a missing positive density behaves like negative mass relative to the background). The "microphysics behind the galactic law of Ch 6" is therefore not inherited from Ch 3. It is a new, undeclared mechanism.
- **Fix:**
  - Either derive the deficit's sign and profile from the Ch 3 momentum-absorption law, or grade Ch 8 [HYP] with an explicit seam: "departs from P1 (voids allowed in the deficit core)".
  - Reconcile it with Ch 12's "only sinks gravitate".
  - Grade the "absolute zero = dark" identification [H].

### C6. The code for almost every claim is absent from the repo
- **Pages:** every chapter's "Simulation and verification" and "Reproducibility" blocks, `axb-reproducibility-map/`, `repro/cosmology/IRREPRODUCIBILITY_LEDGER.md`.
- **Evidence:** `find repro -path "*cosmology*" -name "*.py"` finds exactly one science script, `repro/cosmology/repro/cosmology/02-back-calculation-broadband-gamma-spectrum/ch2_backcalc_spectrum.py` (the rest are build tools). The following are cited but absent from the repo: `ch2_light.py`, `ch2_goldstone.py`, `ch2_lightangle.py`, `ch2_gamma_collective.py`, `ch6_galaxy_rar.py` (incl. "part D"), `ch7_lattice_optics.py` and `Pantheon+_extract.tsv` ("shipped with the package"), the Ch 3 Simulations A to C, the Ch 10 ray and perihelion integrator, `derive_acoustic_length.py` (which the ledger points to at `repro/cosmology/14-cmb-anisotropies-acoustic-scale/`, a path that does not exist), and `phys_import_06_light_mapping_massfree/` ("gate G-LIGHT-MAP-Q: PASS"). The SPARC 175-galaxy run lives in an external archive (zenodo 17622357).
- **Why it matters:** under "a claim counts only when data support it and code reproduces it", every quantitative result except the Ch 2.2 back-calculation is currently data-pending. This includes the SPARC/NGC 2403 fit, the Pantheon+ χ² values, the 43″ and 1.751″ checks, and the "Goldstone" rotor run. `_decl.json` reports `verified: 0`, which is consistent with this, but the pages present these results as run.
- **Fix:** restore the scripts and data into `repro/cosmology/<chapter>/` with SEED = 19 and hashes. Until then, mark each such result "data-pending (code not in repo)" on its page and in the ledger. Correct the dangling path in the IRREPRODUCIBILITY_LEDGER.

---

## Major

### M1. Physics has retired the 633/532 two-line ratio as evidence; cosmology still uses it
- **Pages:** `02-angle-account-quasi-longitudinal-gamma/` (intro and §realmap), `02-light-lattice-elastic-wave-sharpest/` (reproducibility), `axc-two-length-scales-d-versus/`, `16-open-problems-gathered/`, `axg` LOCK list ("the optical anchors (632.99 nm and the 532 nm cross-check)"), `00-how-read-this-volume/` v2 note.
- **Evidence:** "A D-independent test follows … 633/532=1.190, regardless of the unknown spacing D"; "The angle account above is pinned to reality through exactly one ratio … (λ/D)₆₃₃/(λ/D)₅₃₂=633/532=1.18983 … gate G-LIGHT-MAP-Q: PASS"; "One datum is now on record … D is the mapping scale for the visible band".
- **Physics:** Doubt 5a: "retired as evidence. With D held fixed, that ratio equals 632.99/532 for any value of D and for any medium, so it cannot fail." Doubt 5b likewise retires RCROSS.
- **Fix:** remove the ratio as a test, closure or datum everywhere. Replace it with a citation to physics Link 5 (E2 PASS [V] at ±10 %, conditional on N = 200 and g₀ = 2×10⁻⁷) as the actual light-to-electron link.

### M2. The cell a = 6.33×10⁻¹⁹ m is treated as physical and LOCKed; physics says it is an arbitrary container
- **Pages:** `02-light-lattice-elastic-wave-sharpest/`, `02-goldstone-…/`, `02-gamma-burst-…/`, `02-back-calculation-…/`, `09-black-holes-jets-critical-inflow/`, `16-three-falsifiable-predictions/`, `axa`, `axc`, `axd`, `axg` (LOCK).
- **Evidence:** "a = 6.33×10⁻¹⁹ m — VP fundamental cell spacing"; "the cell size … is the SI anchor of the vacuum packing"; "E_QG,2 = √2·hc/(πa) ≈ 882 GeV"; BH "n_max ~ a⁻³ ≈ 4×10⁵⁴ m⁻³"; the gamma back-calculation "rests on no tuned constant" and "only ħ, c and the locked cell a enter".
- **Physics:** Doubt 4b: "N is only the size of the container … Quantities that use the lattice length a directly … inherit the choice of N." w0: "N=10¹² [H] (declared split integer)".
- **Why it matters:**
  - Every a-based number is conditional on an arbitrary N: the 882 GeV dispersion scale, the "8 orders" tension, the gamma-band reach of a "2-cell" shake, and the BH core density.
  - Changing N by 10³ moves E_QG by 10³.
  - The back-calculation's "width-independent … no tuned constant" claim is false, because its gamma reach is set by N.
  - That a sharp pulse is broadband is Fourier's theorem, which cannot fail.
- **Fix:**
  - Relabel a everywhere as "a = λ_ref/N, conditional on N = 10¹² [H]" and drop it from the LOCK list as a physical anchor.
  - State each a-dependent result as conditional on N.
  - Recast the D-versus-a question in App C: D is measured (2λ_C,e) and a is a container choice, so they are not two competing physical lengths.

### M3. Post-Newtonian results are upgraded beyond physics' [O], and bending is derived two ways
- **Pages:** `10-post-newtonian-sector/`, `09-black-holes-jets-critical-inflow/`, `08-dark-matter-vacuum-deficit/`.
- **Evidence:** Ch 10: "γ=1 … follows from the equation of state of the medium rather than being fitted"; "γ=1 (forced by the index)". Yet: "the value already imported in Chapter 8 for the lensing sign (the “GR-matched index, γ=1”)". Ch 9 derives the same 1.752″ from n ≃ 1 + v²/c², justifying the square only by "the bending is sense-independent under inflow reversal".
- **Physics w0:** "Only the clock rate (g_tt) is reproduced. Orbits, light bending, Shapiro delay and gravitational waves need the full metric. Obstacle: the spatial metric and the PPN parameters γ, β."
- **Why it matters:**
  - γ = 1 is set to match GR ("GR-matched"), which contradicts "forced".
  - The two bending derivations are independent and neither is computed from K(ρ). The Ch 9 one additionally relies on the C2 profile.
- **Fix:**
  - Grade PPN γ as [O], or as [H] under the Ch 9 river identification.
  - Keep β and gravitomagnetism [O].
  - Pick one bending derivation and state its closure.
  - Re-ground the redshift on physics §18.

### M4. The grading vocabulary is out of date, and [F] sits on fits
- **Pages:** `axg-governance-no-tuning-lock-gate/`, `axf-executive-summary-one-page-result/`, `00-how-read-this-volume/`, `_decl.json`.
- **Evidence:** "[O] open—an external empirical input (e.g. G, H₀, the masses)". The vocabulary has no [V]/[L]/[H]. The scorecard gives [F] to "Supernova Hubble diagram … χ²/dof=0.50", "Solar-system orbits … periods ≤0.73 %", "Bulk inflow ∝ mass", "a₀ … [F] dist".
- **Why it matters:** the corpus meanings are: [O] = open with the obstacle named, [L] = anchored input, [V data] = passed a test against data. Measured inputs such as H₀ and G should be [L]. Data comparisons are [V data] (when code exists), not [F]. Identifications (light = wave, E/B, κ_opt as a wavenumber, deficit = absolute zero) are [H]. With the current vocabulary, the physics [H] items cannot be carried across correctly.
- **Fix:** adopt the corpus legend [F]/[V mech]/[V data]/[L]/[H]/[O], regrade the scorecard, and regenerate `_decl.json`.

### M5. The dispersion prediction is contradictory and cannot fail
- **Pages:** `16-three-falsifiable-predictions/` against `axg-governance-no-tuning-lock-gate/`; the hub summary of `16-honest-ledger-…`.
- **Evidence:** §16.1: "detection would confirm a transverse-lattice character of light, while continued non-detection favours the quasi-longitudinal reading". App G criterion (4): the framework is killed by "a confirmed transverse vacuum dispersion at the rate the flat reading gives, which the angle account forbids". Ledger summary: "Its sharpest, most distinguishing claim is a parameter-free prediction of gamma-ray vacuum dispersion".
- **Why it matters:** as written, both outcomes support the framework. The prediction is also not parameter-free (M2), and at the stated scale it is already excluded by Fermi by 8 orders. The distinguishing result is also named inconsistently: the hub says a₀; the ledger says dispersion.
- **Fix:** state one failure condition. For example, "any quadratic dispersion detected below E_QG,2 < 1.3×10¹¹ GeV refutes the quasi-longitudinal reading", or whichever is intended. Remove "parameter-free" and use one headline.

### M6. The "single input" ν_H has no observable consequence
- **Pages:** `01-single-input-inflow-rate/`, `03-gravity-momentum-absorbed-inflow/`, `axg` (anti-circular chain step 1).
- **Evidence:** Ch 3: "Rescaling Q→cQ and κ→κ/c leaves κQ unchanged … the framework fixes the product; how one chooses to call part of it “G” and part of it “mass” is a matter of units." κ is fitted to GM_⊙.
- **Why it matters:**
  - The absolute ν_H = 3π⁴+1 cancels from every orbit, so the claim that "one number fixed by π … carries the whole of gravitation" does no work.
  - The only survivors are the per-body ratios (= mass ratios) and the proton/electron composition term, which is the part that is falsified (C1).
  - ν in s⁻¹ also carries physics' time-unit bookkeeping (Δt declared; SP S3(iii)), which cosmology drops.
- **Fix:** state plainly that gravity uses only κQ, which is equivalent to GM [L], and that ν_H enters no tested prediction. Keep ν_H as provenance only.

### M7. Out-of-date E/B reading; E2 and A are not inherited
- **Pages:** `02-goldstone-continuum-mode-dispersionless/`, `02-light-lattice-elastic-wave-sharpest/`, `axd-index-imports-physics-volume/`.
- **Evidence:** "the electric field is the displacement (polar), the magnetic field the rotational twist (axial)", with no grade. The App D row "Vacuum = jammed granular medium; c²=K/ρ (P1)" is imported as "established".
- **Physics (current):** Link 6a gives "E = transverse swing, B = the lattice's rotational response, ray = carrier and energy flow", graded [H], with the lattice run data-pending. Link 7 gives "the lattice's surviving wave is identified with light", [H] supported by E2.
- **Fix:**
  - Update the wording to Link 6a and grade it [H], citing the data-pending run.
  - Add App D rows for E2 ([V] ±10 %, conditions) and for the amplification A (which carries scale). Import "light = lattice wave" as [H], not as established.
  - Grade the "Goldstone" U(1) account as physics does (the physics volume grades it Hm).

### M8. Prediction 1 (a₀ tracks H₀) is ill-defined and in tension with Ch 7
- **Pages:** `16-three-falsifiable-predictions/`, `axg` criterion (1), `07-non-expanding-lattice-optics-cosmology/` Part C, `07-hubble-tension-line-of-sight-averaging/`.
- **Evidence:** "the galactic acceleration scale should track the local environment and cosmic epoch … its absence would favour MOND"; "a₀ failing to track cH₀/2π across redshift". Ch 7: "κ_opt=κ₀(1+ηδ_bg) … H_local/H_global = 1+ηδ_loc … reach the observed 73/67≈1.09".
- **Why it matters:**
  - In a static medium, "H₀ at epoch z" is not defined unless the E-COSMO evolution of ρ_eff (physics: open) is specified.
  - "Absence would favour MOND" is not a kill condition, so App G and §16.1 disagree.
  - If κ_opt is environment-dependent at the 9 % level, then a₀ must vary by about 9 % between environments. That is a quantitative prediction no page states.
- **Fix:** state a₀(environment) = a₀(1+ηδ) with the same η as the Hubble-tension mechanism, give the expected magnitude, and state the epoch dependence (or "none, pending E-COSMO"). Make absence a stated kill condition.

### M9. Two flat-curve mechanisms are never reconciled
- **Pages:** `06-galactic-rotation-derivation-a0-ch0/`, `08-dark-matter-vacuum-deficit/`.
- **Evidence:** Ch 8: "v_flat=√(4πGA) … the same deep-regime result derived in Chapter 6, now with a microphysical origin." Ch 6 obtains flat curves from the modified law a = ν(g_N/a₀) g_N, which already accounts for the full rotation (the SPARC fit uses no halo).
- **Why it matters:**
  - If the deficit also gravitates, adding it to the Ch 6 law double-counts.
  - If it replaces the law, the BTFR v⁴ = a₀GM does not follow, because the deficit amplitude A is free and not tied to a₀.
  - Ch 6 did not derive the deep regime; it borrowed ν (C4).
- **Fix:** state that Ch 8 is the proposed microphysics of the ν law, derive A in terms of a₀ and M_bar, and otherwise grade Ch 8's flat-curve claim [HYP].

---

## Minor

- **m1.** Hub badge "Inherits: R19 switch" (`docs/cosmology/index.html`). R19 is first stated in `dna`, and cosmology inherits only from physics (AGENTS §3.3). No cosmology page uses R19. Remove the badge.
- **m2.** Notation: cosmology writes c² = K/ρ throughout, while physics and AGENTS use c² = B/ρ. Align, or declare K ≡ B.
- **m3.** ν_p = 3π⁴ and 6π⁵ are imported as "fixed geometrically / [F]" (`01`, `axf`). Physics grades them [F | LOCK-NU-N], "forced once the declared survival→rate mapping is accepted", with a −18.8 ppm residual [O]. Carry the condition and the residual.
- **m4.** P2 "Each nucleon annihilates … at the canonical rate". The physics derivation is for the proton (§8, §13). The extension to neutrons is silent. Declare the seam or mark it [H].
- **m5.** `02-angle-account-…`: "measuring the transverse angle of visible light … would pin D to ~0.001 %". Physics Doubt 6b corrected the sensitivity (±0.03 % in D moves χ ≤ 0.17°, with integer jumps). Recompute or cite Link 6b.
- **m6.** P4 (`01`) says "the exact Lorentz factor's value forced". Physics w0 lists GR beyond g_tt as [O]. Quote physics' grade for §18 verbatim.
- **m7.** App D mixes ownership: "Light bending 1.752″ … this vol." while Ch 10 says γ = 1 is "imported in Chapter 8 (GR-matched)". The reciprocity d_A = d_L/(1+z)² is "derived in neither volume" (good), yet Ch 7 relies on it for z_min and the Tolman (1+z)⁻⁴ claim. Grade both as conditional in the scorecard (currently "[F] deg").
- **m8.** Ch 7 is labelled "static/non-expanding", but P4 requires a cosmic-time evolution of ρ_eff with rate H₀, i.e. a time-dependent medium (and so a time-varying c_med/n). State this in Ch 7 and Ch 12, where the horizon and flatness problems "never arise (static)".

---

## Data-pending list (not to be argued until code or data exist in the repo)
1. The E/B lattice run (inherited from physics Link 6a), which is needed for Ch 2 and Ch 11 (TT polarization).
2. The SPARC 175-galaxy CV, the NGC 2403 fit, and "part D" (`ch6_galaxy_rar.py`, absent).
3. The Pantheon+ fit and z_min (`ch7_lattice_optics.py` and data, absent).
4. Ch 3 Simulations A to C; the Ch 10 ray trace and perihelion (absent).
5. The Goldstone rotor run (`ch2_goldstone.py`, absent); the angle table (`ch2_lightangle.py`, absent; physics has `light_emergence_massfree.py`, which could be cited instead).
6. The acoustic-length and BAO scripts (absent; the ledger path is dangling).
7. A MICROSCOPE-level composition test of Q/M (C1). This is not pending: the rates as stated already conflict with it.

## Suggested order of repair
C6 (restore code, so each claim can be checked) → C1/C2/C3 (re-sync with physics' current EP scope, choose one inflow profile, adopt the Link 2/6a light account) → C4/C5 (regrade a₀ and dark matter honestly as [H] + [V data]) → M1/M2/M4 (retire the 633/532 ratio, make a conditional on N, adopt the corpus grade legend) → the rest.
