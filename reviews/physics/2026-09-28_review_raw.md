# Physics volume — raw review findings (2026-09-28)

> **Status: raw reviewer output, NOT yet adversarially verified.** Individual findings may be wrong, overstated, or duplicated across reviewers. The verified, prioritized report is produced in a later step.

Reviewers: 10 chapter-group readers + 5 cross-cutting lenses (numerics, look-elsewhere, mainstream physics, repro code, cross-volume/rendering).

Totals: 245 findings — critical 45, major 156, minor 44.

| reviewer | critical | major | minor |
|---|--:|--:|--:|
| review:front | 4 | 11 | 2 |
| review:gov-notation | 4 | 9 | 5 |
| review:axioms-semantic | 3 | 13 | 4 |
| review:rectification-core-120 | 3 | 11 | 1 |
| review:proton-event-electron | 4 | 8 | 1 |
| review:light-realization | 3 | 11 | 2 |
| review:mass-force | 3 | 15 | 4 |
| review:qm-doi-time-gravity | 4 | 9 | 6 |
| review:extensions | 4 | 11 | 3 |
| review:appendices | 2 | 14 | 2 |
| lens:numerics | 3 | 6 | 4 |
| lens:look-elsewhere | 3 | 9 | 1 |
| lens:mainstream-physics | 2 | 9 | 2 |
| lens:repro-code | 1 | 10 | 4 |
| lens:cross-volume-and-rendering | 2 | 10 | 3 |


## review:front

### 1. [critical] Light is identified with the longitudinal mode (c²=B/ρ, G→0), yet the same volume identifies light with the transverse (∇·=0) sector and helicity ±1: the two cannot both hold in an elastic medium

- **category:** physics-validity
- **location:** physics hub (docs/physics/index.html, 'Canonical results'); w0 concept card; rf forced chain; sp §S2.3; 14-force §14.0.6 and §14.0 genesis; 10 §10.9; cross-volume docs/chemistry/01-electromagnetism-jammed-lattice-light

**Quote.** sp S2.3: "the relaxed (non-affine) shear modulus vanishes, G_relaxed→ 0, while the bulk modulus B stays finite ... The transverse wave dies; one longitudinal speed survives, c^{2}=B/\rho=K" | §14: "Identify E with the VP displacement field u. Its longitudinal part (∇·u, compression = deficit) is the static Coulomb field ...; its transverse, propagating part is light" | §14.0.6: "On the transverse (∇·=0) subspace, source-free Maxwell is exactly the first-order curl square-root of the core wave operator Box_c" | §14.0: "photons carry helicity ±1 (circular polarization = a rotating field)" | chemistry: "leaving one longitudinal wave, light, at c² = B/ρ"

**Evidence.** In isotropic linear elasticity the displacement splits into u_L (curl-free) with c_L² = (B + 4G/3)/ρ and u_T (divergence-free) with c_T² = G/ρ. The spine's own verified result G_relaxed → 0 at z = 6 gives c_L² → B/ρ and c_T → 0: the transverse sector does not propagate at all. So 'c² = B/ρ' is the speed of the longitudinal (compression) mode, which has one polarization and helicity 0, while §14.0.6 needs the divergence-free sector to propagate at c with two helicity ±1 states. The chemistry volume resolves this by saying light *is* longitudinal, which contradicts §14 and the observed transversality of light (photon-mass bounds, PDG m_γ < 1e-18 eV, limit any longitudinal admixture to far below 1e-3). §10.9's compromise, 'near-transverse' with cos χ(633) = cos 89.9378° = 1.09e-3 longitudinal scaffold, is a third, different picture. This is the classic Cauchy/Green elastic-aether obstruction, and the root volume never addresses it. The [V] grade on c² = B/ρ only verifies the textbook jamming result (§11.6.1 itself says: "This is the textbook isostatic-jamming result (O'Hern–Silbert–Liu–Nagel; Wyart; Olsson–Teitel)"). It does not verify that light is this mode.

**Proposed improvement.** Split the headline into two graded claims: (i) [V] 'at isostaticity the simulated packing's only propagating bulk mode has c² = B/ρ' (textbook, cite O'Hern 2003), and (ii) [O] 'this mode is light', with the transversality obstruction stated as its obstacle. To repair the physics, look at a micropolar (Cosserat) or MacCullagh-type rotational-elastic medium. There the curl (twist) stiffness κ carries transverse waves at c² = κ/ρ and the irrotational mode is suppressed. Then show in the simulation that the transverse/twist mode survives at the jamming point and the longitudinal one does not. Until then, remove 'c² = B/ρ' from the hub's 'Canonical results' line and make the physics and chemistry volumes say the same thing about which polarization light is.

### 2. [critical] The 80-digit locked A is back-computed from a 3-significant-figure placeholder Δt=1.86e-21 s, so 'cΔt/a = A', A_geo (0.16%), Tₑ≈1 s (+0.56%) and c_env = c_ref are circular

- **category:** circularity
- **location:** 11-realization §11.3 (A lock, Δt derivation, §11.3.3 definition of c_ref); 01-governance §1.9 A1, A3; w5 §W.5.1 step 'Time'; w6 ledger row 'Lattice unit time Δt'; repro/physics/tools/vp_numeric_ssot.py; 12 §12

**Quote.** §11.3: "A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599." and "The tick follows from the amplification; cΔt/a=A closes exactly." | vp_numeric_ssot.py: DT = D("1.86e-21"),  # Δt (3 유효숫자, realization) ... ("A_geo","cΔt/a",...,"[H] Δt 3 s.f. ⚠placeholder") | §1.9 A3: "Tₑ≈1 s ( +0.6%), and A_geo (0.16%) — five quantities" | §1.9 A1: "The non-trivial content is that c_env comes out equal to c_ref; the framework does not assume this, it shows it" | W.5.1: "Time. Δ t follows from a/c_ref." | W.6: "Lattice unit time Δ t | — | — | ✓ | from a/c_ref"

**Evidence.** With 90-digit Decimal arithmetic, c·(1.86e-21 s)/a with a = 6.3299121257859865746e-19 m gives 880918.977703440000000748733895383659091520244925650031008026876905438425800635992…, which matches the locked A in all 80 printed digits. So A was computed from a round Δt, and Δt = A·a/c_ref reproduces that same input; 'closes exactly' is a tautology. The repro tool itself calls Δt a 3-s.f. placeholder. Consequences: (1) Tₑ = (D/a)³·Δt·6/5 = 1.0056 s is linear in the placeholder (Δt = 1.85e-21 gives 1.0002 s), so the '+0.56%' is the third significant figure of an input. (2) A_geo := cΔt/a *is* the locked A. Its '0.16%' agreement with the simulation compares A_mean(N=750) = 5.69e5 against it. Using the quoted numbers and N^(−1/3) scaling from N = 200, I get +0.35%, and the median (used everywhere else) gives −16.1%. At N = 200 the median 8.02e5 is −9.0% from A_geo. (3) §11.3.3 *defines* c_ref := A·a/Δt, so any lattice speed of A cells per tick equals c_ref in SI by construction, and A1's 'result' is a definition. (4) W.5.1 and W.6 misstate the formula: a/c_ref = 2.11e-27 s, not 1.86e-21 s. The missing factor is A, a simulation quantity whose magnitude W.6 admits scales as 1/g₀ (chosen).

**Proposed improvement.** State openly in §11.3 that A := c_ref·Δt/a is a definition and that Δt = 1.86e-21 s is an [INPUT]/placeholder, and give its historical source. Otherwise derive Δt from the simulation A at a pre-registered g₀, with an uncertainty, and propagate that to Tₑ with error bars. Remove Tₑ and A_geo from the A3 'surviving five' coincidence count, since both depend on the placeholder and are not independent of each other. Downgrade A1 from 'Resolved [F]' to 'definitional identity (c_env ≡ c_ref by §11.3.3)'. Correct W.5.1 and W.6 to 'Δt = A·a/c_ref, provenance: placeholder/simulation (S), not measurement (M)'.

### 3. [critical] 'Single anchor, DOF = 1' does not survive a full count: there are at least two independent dimensionful anchors (λ_ref/N and mₑ), a placeholder (Δt or g₀), a chosen integer N, and many discrete model choices

- **category:** grading-honesty
- **location:** 01-governance §1.8.1 DOF ledger, §1.9 A5; rf 'What goes in, what comes out'; w0 'single measurement anchor' paragraph and W.2.1 SSOT rows N, mₑ, g₀; w5 §W.5.1/§W.5.4; w6 honest-reading note (i); ov bullet 1; all concept cards 'λ_anchor ... (DOF = 1)'

**Quote.** §1.8.1: "Geometry (no DOF): canonical cell = cube; canonical core =82; canonical shell =7; canonical reduction integer 5π for the Higgs channel. Single empirical anchor (1 DOF): λ_ref=632.99nm ... The total tunable DOF count is therefore exactly one" | RF: "The only SI inputs are h, c, and one length anchor" vs RF: "The electron mass is the calibration node: mₑc²=2hc/D is the Compton relation fixing the mass scale—an anchor, not a prediction" | W.2.1: "| mₑ | CODATA | canon_lock | §13.5 | mass-scale anchor | anchor", "| N | 10¹² | canon_lock | §11.2 | split integer | lock", "| g₀ | 2×10⁻⁷ | analysis_lock | §10.3 | microscopic gap threshold | chosen" | W.0: "Any closure quoted at [F]{} or [H]{} level does not use any other empirical input" | OV: "One SI anchor (632.99 nm ≡ mₑ by Compton)" | A5: "The choice is operational, not theoretical: any other anchor in the window predicts the same dimensionless ratios."

**Evidence.** Counting what the outputs actually use: (1) The physical lattice scale is a = λ_ref/N. m_H = hc/(5π a) is linear in N: N = 10^11, 10^12, 10^13 give 12.47, 124.70 and 1247 GeV. So N = 10^12 is a free discrete choice, and the N-invariance table in §1.8.2 only covers dimensionless outputs. (2) The line choice matters. With the framework's own second RCROSS channel (532 nm) and the same N, m_H = 148.4 GeV (+18.5%). A5 ('any other anchor would do') and W.5.4 ('changing λ_ref by 5% ... the measurement excludes') cannot both be true. (3) mₑ from CODATA is a second, independent dimensionful anchor. It fixes D_anch = 2λ_C,e = 4.85262 pm and so r_p, m_p, Tₑ and χ(λ). The claimed bridge D = 2πλ/A does not tie it to λ_ref: with the locked A = 880918.977, 2π·632.99 nm/A = 4.515 pm (−7.0%). Reproducing 2λ_C,e needs A = 819,599. W.6 itself shows D ∝ g₀ (26, 5.2 and 1.0 pm at g₀ = 1e-6, 2e-7, 4e-8), so the 'jamming route' D is set by the chosen g₀ plus a best-bin pick from a 7% distribution. (4) Δt is a placeholder (see the circularity finding). (5) Discrete choices listed as '0 DOF': h vs ħ in U_lat and L_q, the 4/a² normalisation in σ₀, 6 − 1 faces, [MAP-1]/[MAP-2], the bounding-cube vs sphere measure in Tₑ (1.0056 vs 0.527 vs 0.333 s), and C₃ with n = 3.

**Proposed improvement.** Replace §1.8.1 with a per-output input ledger: m_p/m_e uses 0 continuous inputs and k enumerated discrete choices; m_H uses 1 continuous input (a = λ_ref/N, with N and the line choice declared as choices); r_p and m_p use mₑ; Tₑ uses a, mₑ and Δt. Drop 'DOF = 1' from the concept cards and scorecard. Delete '632.99 nm ≡ mₑ by Compton' from OV. Rewrite A5 to say that the Higgs closure holds only for the pair (633 nm, N = 10^12), i.e. that a = 6.33e-19 m is the actual physical input and has no independent derivation.

### 4. [critical] 6π⁵ and 5π are graded [F] 'forced' although they rest on model identifications, sit 1.1×10⁶σ and 4.6σ from measurement, and §1.10 declares residuals are never falsifiers; the grade-promotion rules contradict each other

- **category:** grading-honesty
- **location:** w0 scorecard rows mₚ/mₑ and m_H; rf forced list and forced-coefficient ledger; 01-governance §1.8.3 (assert), §1.8.4, §1.10 'What we do not call falsifiers'; 08 §8.0.6(C); bt meta-lesson; 00-prologue §0.1.1; 11 §11.6.5 table

**Quote.** W.0: "mₚ/mₑ = 6π⁵=2π· 3π⁴ ... | 1836.118 vs measured 1836.153 | [F]{} | -19ppm" | §1.10: "The following are not legitimate falsifiers: (i) "the closure has a 0.4% residual" — the residual is reported openly and is part of the deliverable" | §1.8.3: "assert abs(mp_me_measured/pi**5 - 6) < 2e-4" | §8.0.6: "A definition is not a theorem; no integral can derive [MAP-1]/[MAP-2] ... It is graded [F]{} under that lock" | Prologue §0.1.1: "[H] Hypothesis: Includes closures, idealizations, approximations, model choices" and "retroactively promoting [H] to [F] is not allowed" | BT: "If step 3 closes, the grade is upgraded from [H]{} to [F]{}. ... the Higgs 5π coefficient and the electron 1-second value are at step 2" | RF Forced list: "the Higgs coefficient 5π (§13.3)" | §11.6.5: "6π⁵=1836.118 (CODATA 1836.153, -19 ppm) ... | PASS"

**Evidence.** CODATA 2022 m_p/m_e = 1836.152673426(32), and 6π⁵ = 1836.1181087, so the residual is −18.82 ppm = 1.08×10⁶ standard deviations. m_H: U_lat/5π = 124.695 GeV vs PDG 125.20 ± 0.11 GeV, a −0.403% residual = 4.6σ. As exact 'forced' identities both are excluded by data. The integrals ⟨|cosθ|⟩ = 2/π and δ = 1/π² are theorems. 'Proton = 3 sectors, each costing one inter-sector lock of 1/δ' ([MAP-1]/[MAP-2]) is a physical model choice, which by the prologue's own taxonomy is [H]. §1.10 then removes the only way the data could falsify the claims (a residual of any size 'is not a falsifier'), and Kill-1 can only be triggered by a 'hidden knob'. The self-falsification assertion uses tolerance 2e-4 while the actual deviation is |1836.152673426/π⁵ − 6| = 1.13e-4. That threshold is about 1.8× the observed residual, i.e. set after seeing it. BT tells the reader to upgrade [H] → [F], the prologue forbids exactly that, and BT puts 5π at step 2 ([H]) while RF and §1.8.1 list it as forced / geometry (no DOF). §11.6.5 labels a 10^6σ discrepancy as 'PASS'.

**Proposed improvement.** Use a two-part grade: [F] for the mathematics ('given MAP-1/MAP-2, ν₃ = 3π⁴') and [H] for the physical identification ('m_p/m_e = 6π⁵'), with 5π marked [H] everywhere, consistent with BT. Declare an a-priori theory-error budget, for example 'tree-level exact; corrections O(δ^k) of stated sign'. Then either derive the −18.8 ppm (sign and size) as a pre-registered correction, or record the exact identity as falsified at 10^6σ and the approximate one as surviving at the stated order. Add a falsifier to §1.10: 'a residual exceeding the declared correction budget kills the identification'. Set the §1.8.3 tolerance from that budget, not from the observed residual. Make the prologue and BT agree on whether [H] → [F] promotion is allowed and under what test.

### 5. [major] No look-elsewhere estimate is given; computed ones show the Higgs match is ~1.4σ-level and 'length in, mass out' is just unit conversion through h and c

- **category:** numerology-look-elsewhere
- **location:** w5 §W.5.4; rf 'The one test that settles isn't this circular?'; 01-governance §1.9 A3; ml meta-meta-lesson

**Quote.** W.5.4: "it is a non-trivial coincidence between the measured wavelength of a helium–neon laser and the measured Higgs mass ... changing λ_ref by 5% moves m_H by 5% to a value the measurement excludes. The closure is therefore predictive, not circular." | RF: "(B) the anchor-using result returns a different kind of quantity—the Higgs m_H=hc/(a·5π)=124.7 GeV puts in a length and gets out a mass" | A3: "The joint probability of the surviving five under a six-line geometric chain with one anchor is the structural claim. This is not proof; it is a coincidence count."

**Evidence.** The joint probability is claimed but never computed. My Monte Carlo estimates (seed 19): (a) Higgs. Coefficient family k·π^j (k = 1..6, j = 0..3; 24 distinct mantissas per decade), with N free over powers of ten. P(some member within ±0.40%) = 0.084. With k ≤ 8 and a 1/1, 1/2, 1/4 normalisation, P = 0.19, and it grows further if the laser line is also free. (b) m_p/m_e. Family p·π^k (p ≤ 12, k ≤ 8) gives P(within 19 ppm) = 3.5e-4; p/q·π^k (q ≤ 4) gives 1.0e-3. This is a real but modest signal, and it was first noted by Lenz (1951), before the n-fold law was built to reproduce it. (c) r_p/λ_C,p = 0.63625 (CODATA 2022) vs 2/π (+0.058%). Family p/q·π^k (p, q ≤ 6, |k| ≤ 2) gives P ≈ 0.024. Sensitivity of m_H to λ_ref is what any one-number match shows, so it does not make the closure 'predictive'. With h and c exact in SI, a length and a mass are interconvertible (m = h/(cL)). The only non-trivial content of the Higgs 'prediction' is the dimensionless number m_H·a·c/h = 0.06366 vs 0.06392.

**Proposed improvement.** Add a subsection to W.5 / §1.9 A3 that fixes the formula grammar before looking (allowed integers, π powers, normalisations, h vs ħ, N choices) and reports P-values like the ones above for each headline. State that the evidential weight is essentially the 6π⁵ coincidence (p ~ 1e-3) plus r_p ≈ 4ħ/(m_p c) (p ~ 0.02), and that the Higgs match is weak (p ~ 0.1). Replace 'predictive, not circular' with 'non-circular, single-number coincidence'.

### 6. [major] The π in the 'forced' Higgs coefficient 5π and in R_p/L_q = 2/π comes from using h rather than ħ, not from a rectification integral

- **category:** unit-dimension
- **location:** rf 'The π's are integrals, not numerology'; w0 rows Rₚ/L_q and m_H; 13 §13.3.2–13.3.3; 11 §11.6.4; 00-prologue Misreading 1

**Quote.** RF: "The π's are integrals, not numerology — read this before any π appears. Every π is one rotation averaged." | §13.3: "σ₀^(k) := 4 σ_geom^(k)/a²" and "σ_geom^(k) := π(a/2)² = (π/4)a²" | §11.6.4: "Writing the rectified stiffness αx⁻⁵ against the inflow x⁻⁴ (inflow coefficient normalised to unity), the equilibrium αx⁻⁵=x⁻⁴ forces x^*=α, i.e. rₚ/λ_(C,p)=2/π"

**Evidence.** m_H = hc/(5π a) = 2πħc/(5π a) = (2/5)·ħc/a, with no π. R_p = (2/π)·λ_C,p = (2/π)·2πħ/(m_p c) = 4ħ/(m_p c), with no π; 4ħ/(m_p c) = 0.841236 fm is a well-known numerical near-coincidence with the proton charge radius. In both headline cases the 'averaged rotation' π is exactly the 2π in h = 2πħ, so it can be moved in or out by choosing h or ħ in U_lat = hc/a and L_q = h/(m_p c). The π in σ₀ also depends on normalising the disk area by (a/2)² through the factor 4/a². Normalising by the cube face area a² gives π/4 per channel and σ_eff = 5π/4. §11.6.4 admits that 'the exponents −5, −4 fix only that equilibrium occurs at the stiffness-to-inflow coefficient ratio', so the 2/π comes from setting the inflow coefficient to 1 in h-based Compton units.

**Proposed improvement.** State every headline in ħ units as well (m_H = (2/5)ħc/a; r_p = 4ħ/(m_p c); r_p = 2ħ/(3π⁵ m_e c)). Grade the h-vs-ħ and normalisation choices as declared discrete choices in the DOF ledger, and remove 'every π is one rotation averaged' for those items. Keep the rectification-integral argument only where the π survives a change of convention (for example the π⁵ in m_p/m_e).

### 7. [major] The exponent n−1 in νₙ = nπ^{2(n−1)} (and so the '5' in 6π⁵) is given two incompatible derivations

- **category:** internal-inconsistency
- **location:** rf forced-chain note; 08 §8.0.5(II) vs §8.0.6(A)–(B) and (D); 13 §13.3.4 shared-lemma note; 00-prologue Misreading 1

**Quote.** RF: "the exponent 5 in 6π⁵ is 1+2(n-1) with n=3, leaving no free slot." | §8.0.5(II): "For an n-sector object the number of independent inter-sector phase locks is dim(ℝⁿ/span{1ₙ})=n−1, which is the same linear-algebra count as the Higgs channel reduction 6-1=5" | §8.0.6(A): "the C₃ ring-closure Σ_in_i=0 (§8.0.3) fixes the global phase as a gauge choice and removes no rectification" ... "⟨Wₙ⟩=δⁿ"; (B): "s_n=n⟨W_n⟩⁻¹=nδ⁻ⁿ, ν_n=s_nδ=nδ^{−(n−1)}" | Misreading 1: "the exponent 5 is forced by sector counting (electron n=1 plus proton 3-quark composition with n=3)"

**Evidence.** In §8.0.5(II) the −1 comes from removing one gauge lock out of n. In §8.0.6(A)–(B) the gauge removes nothing (⟨W₃⟩ = δ³), and the −1 comes from the single-nozzle factor δ in ν = sδ. These are different mechanisms, and only exactly one of them may act to get π⁴. Applying both gives ν₃ = 3π², so m_p/m_e = 6π³ = 186.0. Applying neither gives ν₃ = 3π⁶, so m_p/m_e = 6π⁷ = 18,122. Misreading 1 gives a third account ('n = 1 plus n = 3', which sums to 4, not 5). The 'shared lemma' that is supposed to make 5π non-Higgs-specific (§13.3.4) therefore does not actually operate in the §8.0.6 integral.

**Proposed improvement.** Pick one mechanism for the −1 and state it identically in RF, §8.0.5, §8.0.6, §13.3.4 and the prologue. If it is the ν = sδ nozzle factor, drop the claim that the gauge lemma 'fixes the nucleon exponent' and the 5π/6π⁵ 'one forced source, three uses' argument. Add the counterfactual table (6π³, 6π⁵, 6π⁷) to show which modelling step selects the observed value.

### 8. [major] The grade vocabulary is inconsistent across the front matter, and the hub's max-precedence aggregation inflates chapter grades

- **category:** grading-honesty
- **location:** 00-prologue §0.1.1; w0 legend and W.3.2 tag legend; w6 simulation-map table; concept cards on rf/wsum/w0/w5/w6/ml; physics hub claim ledger; AGENTS.md §5

**Quote.** Prologue: "[H] Hypothesis: Includes closures, idealizations, approximations, model choices" vs W.0: "[H]{} = derived structure, coefficient closed under the single anchor" vs W.3.2: "[H]{} calibrated/locked by a stated procedure" | card: "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." | card: "D = 4.8526 pm — Quantum (anchor) diameter ... [F] forced." vs W.2.1 "2λ_(C,e) | anchor-derived" | card: "g* = c²·Ψ_yield — Gravity-cap mechanism ... [F] forced." vs W.3.2 "Ψ_yield=1.091×10⁻¹⁶ m⁻¹ | [O]" | W.6: "Jamming packing φ_jam≈0.63 (zero physical constants in input) | ... | [F]" vs W.0 "φ_jam = 0.633 ... [V] verified" | hub: "Claim ledger across graded sections: 12 forced, 1 hypothesis (precedence forced > verified > hypothesis > open)" and "17. Extensions (Optional Reading) ... forced" vs Prologue C10: "All extensions are conditional claims ([H])"

**Evidence.** The letter [H] means 'hypothesis' in the prologue and in repro/physics/IRREPRODUCIBILITY_LEDGER.md, but 'anchored/calibrated' in W.0 and W.3.2. AGENTS.md calls the same class [L]. [F] is used for a measured anchor (λ_ref), an anchor-derived length (D from CODATA mₑ), a mechanism whose magnitude is [O] (g*), and simulation measurements (φ_jam, c-emergence and SOC pinning in the W.6 map), while W.0 and W.3.2 grade the same simulation outputs [V]. The hub labels each chapter with its *strongest* claim, so §11 (which contains the Δt placeholder), §17 (declared [H] extensions, absolute g [O]), §18 and §1 Governance (a rules chapter) all display 'forced', and a methods chapter (the Prologue) displays 'hypothesis'.

**Proposed improvement.** Adopt one legend corpus-wide ([F] theorem / [V] test passed / [L] anchored input / [H] model hypothesis / [O] open) and regenerate every card and table from it. Never grade an empirical input [F]. Grade simulation outputs [V]. Aggregate chapter grades by weakest link, or show the full distribution (e.g. 'F:3 V:2 H:4 O:2'), instead of max-precedence.

### 9. [major] Stale front-matter claims contradict the corrected body: r_p as a LOCK input, mₑ and the Coulomb scale as derived outputs, and the π²-wrong electron-mass formula

- **category:** internal-inconsistency
- **location:** 00-prologue §0.1.2 (C4, C8, C9); w0 W.2 ledger and W.3.1 gate table; 13 §13.5.3 and §13.6 vs §13.5.4

**Quote.** C4: "the “proton radius” rₚ=rproton is treated as a separate CANON LOCK input" vs W.0: "rₚ = D_anch/(6π⁶) (predicted; was input)" | W.2: "Proton radius rₚ (canon_lock)" (LOCK-inputs column) | C8: "The document includes the numerical results that the proton mass mₚ and electron mass mₑ are obtained as mₚ≈0.938 GeV, mₑ≈0.511 MeV" vs RF: "an anchor, not a prediction (§13.5.4)" | C9: "This document claims that the absolute scale of a “charge-interaction force” can be derived internally" vs W.0: "the EM coupling magnitude is an open input (αₑₘ from measurement, §14.5), not a VP prediction" | W.2: "Electron radius rₑ=(D_anch/2)δ"; W.3.1: "mₑ (electron mass; mₑ=U_lat/S) | realization_lock: U_lat; analysis_lock: S; canon_lock: rₑ"; §13.6: "m_e=U_lat/S=U_lat/(r_e/a)" vs §13.5.4: "Earlier drafts conflated the two, inserting a spurious factor δ=1/π² into mₑ."

**Evidence.** With r_e = (D_anch/2)·δ = λ_C,e/π² = 0.2458 pm, the formula still printed in W.3.1 and §13.6 gives m_e = U_lat·a/r_e = hc/r_e = π²·m_e c² = 9.8696 × 0.51100 MeV = 5.043 MeV, which is exactly the artifact §13.5.4 says was removed. The prologue claim list (C4, C8, C9) still describes an older version in which r_p was an input and the charge-force magnitude was derived. Both contradict the current scorecard and the framework's own 'a LOCK is never edited' rule, since r_p moved from LOCK input to prediction without the W.2 ledger being versioned.

**Proposed improvement.** Update prologue C4, C8 and C9 to the current status (r_p predicted under LOCK-NU-N; mₑ an anchor; Coulomb magnitude [O]). Move r_p to the derived column in W.2 and record the LOCK version-up. In W.2, W.3.1, §13.5.3 and §13.6, replace S = r_e/a with S = λ_C,e/a (the §13.5.4 correction), and add a regression gate to vp_numeric_ssot.py that fails if 'U_lat/(r_e/a)' reappears.

### 10. [major] Headline overclaims ('reproduces QED, GR and the Standard Model', 'a dozen constants from one anchor') are inflated by scorecard padding; the independent physical comparisons number about three

- **category:** structure-redundancy
- **location:** rf 'A rival vacuum'; ml meta-meta-lesson and 'Where the framework is strongest'; w0 scorecard; w5 §W.5.3

**Quote.** RF: "The framework reproduces the empirical results of quantum electrodynamics, general relativity, and the Standard Model while rejecting their mechanisms." | ML: "their joint weight—a dozen constants from one anchor with no free coefficient—is itself the substantive claim" | W.0: "Is not: a prediction of any number not yet measured." | W.0 rows "α = 2/π", "δ = 1/π²", "Rₚ/L_q = 2/π", "σ_geom/L_q²=4/π", "ν_p,can=3π⁴=292.227s⁻¹" | W.0: "α_em⁻¹ = 4π(11 - 35/32·tfrac2π²·3/7) | 137.0364 (numerical coincidence) vs measured 137.0360"

**Evidence.** α and δ are mathematical constants, not physical results. σ_geom/L_q² = π(R_p/L_q)² = 4/π is the same result as R_p/L_q = 2/π. ν_p = (m_p/m_e)/2π is the same result as 6π⁵. r_p = D/(6π⁶) combines 6π⁵, R_p/L_q and the mₑ anchor. The independent physical comparisons are: m_p/m_e (−18.8 ppm), r_p·m_p·c/ħ = 4 (+0.058% vs CODATA 2022), and m_H·a·c/h = 1/(5π) (−0.40%). Only the last uses λ_ref, so 'a dozen constants from one anchor' does not hold. QED precision observables (g−2, Lamb shift), GR's G, and the SM coupling and mass spectrum are not reproduced; α_em, G and H₀ are [INPUT]/[O]. The α_em row carries a contrived formula (4π(11 − 15/(16π²)) = 137.0364, +3.0 ppm), while RF quotes a different form, 4π(11 − δ) = 136.957 (−578 ppm). Showing near-misses of this kind on the one-page scorecard invites the numerology reading the document wants to avoid.

**Proposed improvement.** Replace the RF sentence with the scorecard's own honest mode ('single-anchor consolidation; no unmeasured constant yet predicted'). Restructure W.0 into three tiers: mathematical constants (α, δ); independent physical comparisons (the three above, each with P-value and data vintage); derived restatements (σ/L_q², ν_p, r_p forms). Move the α_em formulas out of the scorecard into §14.5.

### 11. [major] The one 'narrow-sense prediction' (B1, χ(633) = 89.9378°) is not falsifiable as specified: its stated width covers the whole allowed range, and the canonical anchor gives a different value

- **category:** missing-test-or-prediction
- **location:** w0 W.3.2 row χ(633)/χ(532); 01-governance §1.9 B1 and §1.10 Kill criterion 3; ml 'Where the framework is weakest'; 10 §10.9 and §10.9.1

**Quote.** W.3.2: "χ(633)=89.9378^(∘), χ(532)=89.8248^(∘) | [V] | ... | zero fit freedom; only D enters; these are the pre-registered B1 numbers" | §1.10: "This criterion is therefore "armed"" | §10.9.1: "their stated width is the χ-distribution induced by the ℓ_rot spread (§11.6)" and "Using the full-precision anchor λ_ref=632.99121257859865746 nm instead shifts λ/D to 130443.1730, crossing the integer ceiling to m=130444 and χ=89.7960^(∘)"

**Evidence.** sinχ = (λ/D)/⌈λ/D⌉ depends only on the fractional part of λ/D ≈ 1.3×10⁵, so χ always lies in [asin(1 − 1/m), 90°) = [89.776°, 90°). Sweeping D over the declared ±3.5% ℓ_rot spread gives χ ∈ [89.772°, 89.998°], the entire admissible band, so no measurement inside the band can falsify it. Even a ±0.03% band in D keeps χ within ±0.05° of 89.9378° only 25% of the time. The framework's own locked anchor gives 89.7960°, not the committed 89.9378°, which differs only in how λ_ref is rounded. The reference 'lattice/anisotropy axis' is undefined (gate G-ISO is OPEN). A ~1e-3 longitudinal component of visible light would also have to be reconciled with existing transversality and photon-mass constraints.

**Proposed improvement.** Before calling Kill-3 'armed', (i) define the reference axis operationally, (ii) commit a prediction that does not depend on the fractional part of λ/D. One option is the predicted distribution, uniform in sinχ over [1 − 1/m, 1]; another is a two-wavelength observable with a finite, stated width. (iii) Name an instrument and precision able to see a 0.06–0.2° departure from transversality, and show the prediction is not already excluded. Until then, grade B1 [O] 'not yet testable', not [V].

### 12. [major] The front matter cites results whose gates are UNLOGGED under its own rules, while the repro dossier reports them PASS/[F] with no physics gate reports present

- **category:** reproducibility-code
- **location:** w0 W.3.0/W.3.1; 00-prologue §0.4(3); repro/physics/verification_dossier/GROUNDING_LEDGER.md and SIMULATION_GROUNDING_AUDIT.md; repro/physics/tools/vp_numeric_ssot.py

**Quote.** W.3.0: "without the corresponding Gate reports, the conclusion remains automatically UNLOGGED/INCONCLUSIVE" | W.3.1 rows for a, Δt, U_lat, rₑ, mₑ, mₚ, m_H, mₚ/mₑ: "| UNLOGGED |" | §0.4(3): "Results with FAIL or INCONCLUSIVE verdicts are not used as evidence in later sections" | GROUNDING_LEDGER.md: "| Δt (시간 틱) | G-DT | [F] | PASS |", "| m_H | G-MH | [F] | PASS |" | vp_numeric_ssot.py: "[H] Δt 3 s.f. ⚠placeholder"

**Evidence.** By the document's own admissibility rule, every mass-sector headline (m_p/m_e, m_H, m_e, m_p, U_lat, a, Δt) is UNLOGGED and may not be cited as evidence. W.0 and RF nevertheless present them at [F]. The dossier claims PASS/[F] for the same gates, including Δt, which the SSOT tool in the same repro package flags as a placeholder. `find` over the repository returns no physics gate_report_*.json (only DNA ones), so the PASS verdicts cannot be checked from this repo. Gate thresholds are never stated; a gate that passes m_H at 4.6σ and m_p/m_e at 10^6σ has tolerances loose enough that it tests nothing.

**Proposed improvement.** Ship gate/reports/gate_report_{a,dt,Ulat,me,mp,mH,mp_me}.json in repro/physics with explicit thresholds, and derive each threshold from a declared theory-error budget. Then update W.3.1 from UNLOGGED to PASS/FAIL with paths. Make the dossier agree with the SSOT tool (Δt: [L]/placeholder, not [F]). Until then, W.0 should mark these rows 'UNLOGGED' as its own charter requires.

### 13. [major] The gravity time-dilation row is graded [F] 'exact Schwarzschild, machine-exact', but it is an algebraic identity once √(2GM/r) is put in, and that is the known river / Painlevé–Gullstrand picture

- **category:** grading-honesty
- **location:** w0 scorecard rows 'Gravity time dilation = river' and 'Universality (LPI)'; rf Forced tier; 00-prologue Misreading 4; 18 §18.6–18.7

**Quote.** W.0: "Gravity time dilation = river √(1−2GM/rc²) | exact Schwarzschild, machine-exact to NS strong field | [F]{} | G-RIVER; v_river=√(2GM/r) (§18.6)" | §18.7: "The incompressible mass-current that books the sink's steady consumption falls as 1/r²; the time-dilation velocity is the potential (free-fall/river) velocity and falls as 1/√r" | RF Forced tier: "gravity as sink inflow with the equivalence principle derived (§17.4)" vs W.0: "Universality (LPI) = rotor isotropy η_rotor→1 | EP its acceleration face | [F?]{}" | Misreading 4: "The framework explicitly forbids GM/R² at Earth-scale"

**Evidence.** G-RIVER checks √(1 − (√(2GM/r))²/c²) ≡ √(1 − 2GM/rc²), which holds for every GM and r, so 'machine-exact from the Moon to a neutron star' has no discriminating power. The river speed is the Newtonian escape speed, with G as an [INPUT]. §18.7 admits it is not the velocity of the medium's sink flow (that falls as 1/r²), so the picture of 'a clock at rest in a moving medium' does not use a velocity the medium actually has. Flat-space-plus-inflow reproduction of Schwarzschild is Painlevé–Gullstrand (1921–22) / Hamilton & Lisle (Am. J. Phys. 76, 519, 2008) and is uncited. The scorecard itself records that the sector is 'observationally degenerate with GR', which is honest, but that is incompatible with an [F] 'result'. RF also lists the equivalence principle as 'derived' (Forced tier) while W.0 grades it [F?].

**Proposed improvement.** Regrade the row as 'reproduces GR's river form given the Newtonian potential [INPUT]; no distinct prediction' ([L] or reproduction), cite the prior art, and drop 'machine-exact' as evidence. Make RF match W.0 on the equivalence principle ([F?]/[H]). Reconcile Misreading 4 ('forbids GM/R²') with the use of GM/r in §18.6.

### 14. [major] The 'run this' boxes cannot falsify anything: the keystone measures no stiffness and reproduces textbook jamming, and the five-line box only evaluates constants

- **category:** missing-test-or-prediction
- **location:** rf 'The collective stiffness is measured', 'Run this — the keystone', 'anchor-free predictions — five lines', 'Tiered reading'; 00-prologue Misreading 5

**Quote.** RF: "What comes out is decisive: the packing fraction settles on its own to φ_jam≈0.64 (random close packing) and the mean contact number rises through the isostatic z=6. That this emerges with nothing put in is the evidence that the stiffness is a measured number, not a free knob." | RF: "Two minutes. Run the two code boxes above ... If the boxes do not print as stated, the framework is wrong—stop and report the failure."

**Evidence.** I ran the keystone box (numpy 2.4.6). It prints 'jamming onset phi_jam = 0.626' with ⟨z⟩ = 5.67 at the detected onset, so the reproduction is honest, but the onset rule (z ≥ 5.4 and U/N > 1e-7) and the radius sweep are hand-set. The code computes no modulus and no wave speed, so it cannot show that 'the stiffness is measured'. Frictionless soft spheres jamming at φ ≈ 0.64 with z → 6 is the standard O'Hern et al. (PRE 68, 011306, 2003) result for any such packing and says nothing about the vacuum. SI c cannot come out of a dimensionless run without a, Δt and c_ref (see the circularity finding). The five-line box evaluates 2/π, 1/π² and 6π⁵; it can only 'fail' if the Python interpreter is broken, so it is not a test of the framework.

**Proposed improvement.** Relabel the boxes as 'reproduce the arithmetic / reproduce textbook jamming'. Add a real falsification box: in the same packing, measure c_L and c_T against Δz and state which one the framework identifies with light (tying into the transversality issue), or pre-register a numeric threshold with a theory-error budget for m_p/m_e and m_H that the boxes check. Remove 'If the boxes do not print as stated, the framework is wrong'.

### 15. [major] AGENTS.md calls the substrate 'random close packing (φ ≈ 0.7405)'; 0.7405 is the FCC/HCP Kepler density, while the physics volume measures φ_jam ≈ 0.633

- **category:** cross-volume
- **location:** /home/user/jamming-physics/AGENTS.md lines 23, 37, 172 (also docs/AGENTS.md, docs/index.html, registry/concepts.json per grep); physics w0 concept card φ_jam; chemistry CH.13

**Quote.** AGENTS.md: "Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405). Light is its elastic wave: `c² = B/ρ`." | AGENTS.md: "`c²=B/ρ` (0.06% sim); `φ_RCP=0.7405`" | AGENTS.md: "simulation-validated to ~0.06%" | physics W.0: "φ_jam = 0.633 — Isostatic jamming/packing fraction (z to 6); distinct from 2/π = 0.6366. [V] verified." | chemistry CH.13: "FCC/HCP π/(3√2) = 0.7405"

**Evidence.** π/(3√2) = 0.74048 is the maximal (ordered) sphere-packing density. Random close packing / the jamming point is about 0.64, and the physics volume's own measured value is 0.633 (keystone code: 0.626). The top-level machine-reading manual therefore misstates the root volume's central substrate parameter by +17%. The '~0.06%' figure for c² = B/ρ appears nowhere in the physics volume; it comes from the chemistry volume, which also calls light 'one longitudinal wave' (see the transversality finding).

**Proposed improvement.** Correct AGENTS.md, docs/AGENTS.md, the manifest and the hub concept registry to 'jammed at random close packing, φ_jam ≈ 0.63–0.64 (physics W.0)'. Label 0.7405 as the FCC close-packing fraction used only in chemistry crystal geometry. Either source the 0.06% figure to a physics-volume table or remove it from the physics headline. Regenerate the aggregates from vp.manifest.json as AGENTS.md §9 requires.

### 16. [minor] Residual baselines are stale or uninformative: r_p is compared to a rounded locked 0.8412 and to CODATA 2018, and the sign flips with CODATA 2022

- **category:** grading-honesty
- **location:** w0 scorecard row rₚ and W.2.1 cross-checks; 01-governance §1.8.3 comment, §1.8.4, §1.9 A3; 13 §13.3.8; repro/physics/tools/vp_numeric_ssot.py (CANON ME, MEAS RP_CODATA, MPME)

**Quote.** W.0: "rₚ = D_anch/(6π⁶) (predicted; was input) | 0.84125 fm vs locked 0.8412 | [F]{} | +61ppm" | §1.9 A3: "rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm)" | vp_numeric_ssot.py: "ME     = D(\"9.1093837015e-31\")", "RP_CODATA=D(\"0.8414\")"

**Evidence.** 0.8412 is a 4-significant-figure rounded number (rounding interval ±59 ppm), so '+61 ppm vs locked' (R3/R4 in the Residual Map) is not a physical residual. CODATA 2022 gives r_p = 0.84075(64) fm, so D/6π⁶ = 0.841251 fm is +0.060% = +0.78σ, and the sign flips from the quoted −0.018% (CODATA 2018 0.8414(19)). The SSOT tool also hardcodes CODATA 2018 mₑ (9.1093837015e-31; CODATA 2022 is 9.1093837139e-31) and m_p/m_e 1836.15267343 (CODATA 2022: 1836.152673426(32)).

**Proposed improvement.** Report every residual against the current measurement with its uncertainty and a σ-distance (r_p: +0.060%, +0.78σ; m_p/m_e: −18.8 ppm, 1.1×10⁶σ; m_H: −0.40%, 4.6σ vs PDG 125.20 ± 0.11 GeV). Drop the '+61 ppm vs locked 0.8412' residual from the scorecard. Update the SSOT constants to CODATA 2022 and record the data vintage in each row.

### 17. [minor] Rendering leaks, a wrong cross-reference, an incomplete legend and garbled descriptions in the front matter

- **category:** presentation-rendering
- **location:** 11 §11.2 heading; 00-prologue (C7) equation alt text; w0 α_em row and table cells; ml 'For the contributor'; 10 §10.9 alt; 01 §1.9 A1; w0 grade legend; rf forced-coefficient ledger; cm and r5 stub chapters

**Quote.** "11.2 Deriving a=λ_ref/N→aVPm" | prologue alt: "a = \aVP, \qquad \Delta t = 1.86\times" | W.0: "4π(11 - 35/32·tfrac2π²·3/7)" | ML: "What an additional version must emphnot do." | W.0 cells: "[F]{}" | A1: "See §W.4 prong A." | RF ledger: "3π⁴=νₚ | 3 sectors (C₃) × 1/π survival" | W.0 legend defines only "[F]{} ... [H]{} ... [O]{}" while rows use "[V]", "[H]+{}", "[F?]{}", "[INPUT]", "negative"

**Evidence.** I checked the leaks in the deployed HTML (docs/physics/*/index.html): unexpanded LaTeX macros (\aVP, \Danchpm, \tfrac, \emph) and empty braces after grade tags. 'Prong A' is in W.5, not W.4 (W.4 is 'Known constraints'). '3 sectors × 1/π survival' does not give π⁴; the law is 3·(1/δ)^{n−1}. The CM and R5 'chapters' contain only a pointer sentence each, yet they appear as separate hub entries.

**Proposed improvement.** Expand the macros at build time and add a build gate that fails on '\\[A-Za-z]+' in alt text or headings and on 'tfrac|emph|{}' in rendered text. Fix the A1 cross-reference to §W.5. Complete the W.0 legend. Correct the RF ledger description. Fold the CM and R5 stubs into redirects instead of chapter entries.

**Strengths noted:**
- Residuals are reported rather than hidden, and the document explicitly refuses to migrate coefficients (5π vs 4.98π); this is the right instinct and should be kept as the rules above are tightened.
- α_em and the absolute value of g are honestly graded [O] with their obstruction stated, and the α_em closed form is explicitly barred from evidential use.
- The gravity sector publishes an honest negative (G-CAP-DEPART: observationally degenerate with GR, no surviving distinct prediction), which is rare and valuable.
- W.6's honest-reading notes (A ∝ 1/g₀; D is a distribution and its match is a central-tendency or best-bin match, 'not a parameter-free derivation') are exemplary and should be propagated to §1.9 A3, EA v33, and §3.4, where the older, stronger wording survives.
- The v34 rule that 'evidence not externally re-executable does not count' is a genuine methodological strength.
- The code boxes are runnable and honest about their output: the keystone reproduced 'phi_jam = 0.626' exactly as documented.
- The repro SSOT tool (vp_numeric_ssot.py) regenerates every displayed number from canonical inputs, reduces the scattered residuals to two independent ones, runs a drift gate, and even flags Δt as a placeholder; this infrastructure makes the corrections above straightforward.
- The RF's Layer A (mathematics) / Layer B (physical identification) split is the correct framing; applying it consistently to the grades (math [F], identification [H]) would resolve most of the grading findings.
- Two dimensionless near-coincidences are genuinely precise and worth keeping as the core empirical content: m_p/m_e ≈ 6π⁵ (−18.8 ppm; look-elsewhere p ~ 1e-3) and r_p ≈ 4ħ/(m_p c) (+0.06%, within 1σ of CODATA 2022).


## review:gov-notation

### 1. [critical] The DOF ledger's 'exactly one tunable input' claim is false: at least five more inputs enter the headline numbers

- **category:** grading-honesty
- **location:** 01-governance-no-tuning-lock-gate §1.8.1 (DOF ledger), header lock cards (λ_anchor, D), §1.9 A7; cross-checked against 03 §3.4, 11 §11.2–11.3, 13 §13.5.4, repro/physics/tools/vp_numeric_ssot.py (CANON), repro/physics/registry/vp_locks.csv

**Quote.** "Single empirical anchor (1 DOF): λ_ref=632.99nm, used to fix a once." / "No per-particle calibration, no fitted coupling, no tunable exponent enters anywhere. The total tunable DOF count is therefore exactly one, and it is exposed in step 3." / "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." — versus 03 §3.4: "D_anch:=2λ_(C,e)=4.8526pm — the same 632.99 nm / mₑ anchor used everywhere else"; 13: "It is the single calibration node of the mass sector—an anchor, not evidence."; A7: "the absolute magnitude 9.80665m/s² is honestly an external anchor (back-substituted in App G)."; vp_numeric_ssot.py: "ME     = D(\"9.1093837015e-31\"),            # 전자질량 (CODATA)"; vp_locks.csv: "alpha-em,α_em,≈ 1/137,Electromagnetic fine-structure constant; a measured input — NOT derived"

**Evidence.** (1) m_e: D_anch = 4.852620477e-12 m equals 2h/(m_e c) with CODATA-2018 m_e to 7.5e-11 relative (2h/(m_e c) = 4.852620477366e-12 m), so D_anch is the electron Compton wavelength, i.e. m_e is an input. r_p = D/(6π⁶), m_e = 2hc/D and χ all depend on it. 632.99 nm and λ_C,e are two independent measured numbers: their ratio 130442.92 is used, not predicted. (2) N = 10¹² is a declared split integer (11 §11.2; graded [H] in the w0 scorecard). m_H = hcN/(5π λ_ref) = 124.695 GeV is proportional to N (see next finding). (3) Δt = 1.86e-21 s is given to 3 s.f., and the 80-digit locked A is c·(1.86e-21 s)/a exactly (recomputed: 880918.977703440000000748733895383659…, identical to the printed value). So Δt has no derivation independent of itself. (4) α_em is a measured input (vp_locks.csv). (5) The absolute gravity scale is back-substituted from 9.80665 m/s². (6) canon_lock still holds r_p = 8.412e-16 m, 'the validator-enforced proton radius' (vh v0.4.1). The ledger also declares discrete structural choices zero-DOF ('integers up to 7', powers of π, 6/5, 5π, 82/89), but choosing from a discrete family is a degree of freedom (quantified in the look-elsewhere finding).

**Proposed improvement.** Replace §1.8.1 with a complete input table. Give one row each for λ_ref, m_e (or D_anch), N, Δt (or A), α_em, g_⊕/m_q, the r_p lock, h and c. Each row states: measured or chosen, continuous or discrete, and exactly which outputs depend on it (e.g. m_H ∝ N/λ_ref; T_e ∝ N²·Δt; r_p, m_e and χ ∝ D). Restate the claim honestly: 'the dimensionless ratios m_p/m_e and R_p/λ_C,p use no continuous input; dimensional outputs use λ_ref, N, m_e and Δt.' Drop 'exactly one' unless N and Δt are derived. Grade λ_anchor and D as anchors ([L]/[H]), not [F].

### 2. [critical] The Higgs mass and the electron 1-second depend on the arbitrary split N = 10¹² and on the laser line; the N-invariance table is a tautology that hides this

- **category:** unit-dimension
- **location:** 01 §1.8.2 (N-invariance table), §1.9 A2, A3, A5; 11 §11.2 (a = λ_ref/N); 13 §13.3–13.5; 12 §12 (T_e)

**Quote.** "| m_H/U_lat | 1/(5π) | 1/(5π) | 1/(5π)" / "Confirmed by the released code; no N enters the closure equations." / A5: "The choice is operational, not theoretical: any other anchor in the window predicts the same dimensionless ratios." / 11 §11.2: "N is locked in analysis_lock and cannot be changed after seeing the result." / 13: "The predictive mass results are the dimensionless ratio mₚ/mₑ=6π⁵ (which carries no anchor) and the length-in/mass-out Higgs (W.5)" / 12: "computes Tₑ≈ (D/a)³τ_VP× 6/5 and yields ≈ 1.0s"

**Evidence.** a = λ_ref/N, U_lat = hc/a and m_H = U_lat/(5π) give m_H = hcN/(5π λ_ref). Computed: N = 10⁹ gives 0.1247 GeV, N = 10¹² gives 124.695 GeV, and N = 10¹⁵ gives 124,695 GeV. With N fixed, the RCROSS 532 nm channel as anchor gives m_H = 148.37 GeV, and 611.97 nm gives 128.98 GeV. The −0.40% Higgs result is therefore the statement hc/(5π m_H) ≈ λ_He-Ne/10¹². That depends on the SI metre and on base 10. T_e = (D/a)³·Δt·6/5 = 1.0056 s, which the text itself says scales as N² ('Tₑ∝ N² scaling invariance'). It is compared with the SI second, which is a human convention (9,192,631,770 Cs periods). The §1.8.2 table lists only m_H/U_lat = 1/(5π), which is N-free by construction, so 'confirmed by the released code' tests nothing. A5 is true only for ratios; the dimensional Higgs 'prediction' changes by 19% between the framework's own two channels. Where N is filed is also inconsistent: canon_lock in the w0 scorecard ('| N | 10¹² | canon_lock |'), analysis_lock in §11.2. Under §1.2.3, a physical scale belongs in realization_lock.

**Proposed improvement.** Add rows 'm_H [GeV]' and 'T_e [s]' to the §1.8.2 table showing their ∝N and ∝N² scaling. Then do one of two things: derive N from physics (a reason why λ_ref/a is exactly 10¹²), or regrade the absolute Higgs mass and T_e as unit-dependent [H]/NON-EVIDENCE and remove them from A3's surviving set. Qualify A5 with 'dimensionless ratios only; m_H ∝ 1/λ_ref'. File N in exactly one lock category.

### 3. [critical] A1's claim that c_env = c_ref 'is a result' is circular: Δt is defined through c_ref, and A is back-computed from Δt

- **category:** circularity
- **location:** 01 §1.8.1 (universal-constants bullet), §1.9 A1 (graded 'Resolved [F]'); 02 §2.3.2, §2.3.5 (eq. a_over_dt), §2.6; 11 §11.3.3, §11.6.2; repro/physics/tools/vp_numeric_ssot.py; reports/phase4-physics.gate.json

**Quote.** A1: "Resolved [F]." … "The non-trivial content is that c_env comes out equal to c_ref; the framework does not assume this, it shows it (§11.6)." / 11 §11.3.3: "Fix the reference speed constant c_ref as an operational quantity defined by the ratio of the “effective propagation length per tick” to the “tick time”." / 02 §2.3.5: "c_ref is defined as a constant of an external reference channel used to fix the realized speed unit a/Δ t." / 11 §11.6.2: "Going from the dimensionless amplification A (a pure number, output of the simulation) to a stiffness with units of (length/time)² requires one length scale — the lattice unit a — to set the absolute magnitude." / vp_numeric_ssot.py: "주: 80자리 A(cΔt/a)는 §3.4가 'placeholder' 면책 → 드리프트 아님(검사 제외)"

**Evidence.** §11.3.3 defines c_ref := A·a/Δt and solves for Δt = A·a/c_ref. The locked 80-digit A equals c·(1.86e-21 s)/a exactly (recomputed to 90 digits; the '…0000000748733…' tail is the signature of the rounded Δt). So A and Δt are the same number written two ways, which violates §2.6's 'Circular dependency is forbidden.' The realized speed unit is a/Δt = 340.32 m/s. Any lattice speed of A cells per tick then converts to exactly c_ref by construction, so the 'agreement' is a unit calibration, not a derivation. §11.6.2 also contains a dimensional error: a length alone cannot turn a pure number into (length/time)², and the only time scale available (Δt) is itself fixed by c_ref. On grading: A1 is marked [F], but its supporting layers §11.6.2 and §11.6.3 are graded [H], and the air check reproduces c_sound only 'within the expected order of magnitude'. The repro gate explicitly exempts A from the drift check as a 'placeholder'.

**Proposed improvement.** Regrade A1 to [H]. State plainly that the simulation fixes c only in lattice units (cells per tick) and that conversion to m/s uses c_ref, so c_env = c_ref is a calibration. A non-circular test needs either Δt from an independent observable that does not use c, or a dimensionless prediction (e.g. A from the simulation at the physical N, with its distribution) compared with an independently derived value. Remove the 80-digit A from the locks and lock A only as a simulation output with its spread. Complete eq. (a_over_dt) in §2.3.5 as c_ref = A·a/Δt so the dependency is visible. Correct the dimensional statement in §11.6.2.

### 4. [critical] The 'armed' light-angle prediction (B1 / Kill criterion 3) is not sharp; the '0.03% in D ⇒ >1° in χ' claim is mathematically impossible

- **category:** missing-test-or-prediction
- **location:** 01 §1.9 B1, §1.10 Kill criterion 3 and the 'Added in v0.2.0' note; 03 §3.4 (D precision); 10 §10.9.1 (input-convention note)

**Quote.** B1: "χ(532.0nm)=89.8248^(∘) at the canonical D_anch; hypersensitive, 0.03% in D" … "⇒>1^(∘) in χ)" / Kill 3: "spread as the stated width)." … "This criterion is therefore \"armed\"; it remains unused only in the sense that the measurement has not yet been performed." / 03 §3.4: "so D is pinned to only 0.04% ( 4×10⁻⁴)" / 10: "Using the full-precision anchor λ_ref=632.99121257859865746 nm instead shifts λ/D to 130443.1730, crossing the integer ceiling to m=130444 and χ=89.7960^(∘)"

**Evidence.** With sinχ = λ/(mD) and m = ⌈λ/D⌉, we get sinχ > (λ/D)/(λ/D+1). That confines χ to (89.776°, 90°] at 633 nm (λ/D = 130442.92) and to (89.755°, 90°] at 532 nm, for any D. The maximum possible swing is 0.224°, so '>1° in χ' cannot happen. One step in m corresponds to 7.67 ppm in D (9.12 ppm at 532 nm). D's declared 0.04% precision spans about 52 steps. A Monte Carlo (seed 19, D uniform over ±0.02%) gives a 90% interval of [89.781°, 89.950°], a minimum of 89.776° and a maximum of 89.9996°. The 'D-distribution spread as the stated width' is therefore the entire allowed range: any near-transverse result passes. The committed numbers are also artifacts of rounded inputs. λ = 632.99 nm gives 89.9378°, while the physical iodine-stabilised He–Ne line (632.99121258 nm) gives 89.7960°. At 532.00, 532.05, 532.10 and 532.20 nm, χ = 89.825°, 89.888°, 89.767° and 89.866°; real '532 nm' DPSS lines sit near 532.1–532.3 nm. Two values of λ_ref (632.99 and 632.99121257859865746 nm) are in use, which breaks SSOT. Finally, the observable ('transverse angle against a lattice/anisotropy axis') has no operational definition (§10.9.2 G-ISO is [O]), and Lorentz-invariance tests already bound vacuum anisotropy of c at roughly 1e-17.

**Proposed improvement.** Downgrade B1 and Kill criterion 3 from 'armed' to 'candidate (not yet falsifiable)'. To arm them: (i) define the apparatus and the reference axis, and show the effect is not already excluded by modern Michelson–Morley bounds; (ii) commit to one physical wavelength (the frequency-stabilised BIPM value) and D = 2λ_C,e at CODATA precision, so χ is fixed to better than one m-step; (iii) publish the window together with its prior-predictive sharpness, i.e. the probability that a uniform draw on (89.776°, 90°] lands inside it; (iv) delete the '>1°' sentence and the 532 nm entry unless a line known to <1 ppm is specified.

### 5. [major] Headline relations miss the data by 10⁶σ (m_p/m_e) and 4.6σ (m_H), yet residuals are declared 'not falsifiers' and no theory tolerance is pre-registered

- **category:** grading-honesty
- **location:** 01 header card (m_p/m_e [F]), §1.8.3 five-line check, §1.8.4, §1.10 'What we do not call falsifiers', §1.4 (pre-registration rule)

**Quote.** "m_p/m_e = 6π⁵ — Proton-electron mass ratio as 2π·ν_p = 6π⁵ (−19 ppm vs measurement). [F] forced." / "(i) \"the closure has a 0.4% residual\" — the residual is reported openly and is part of the deliverable" / §1.4: "Pre-registration: the decision expression, thresholds, tolerances, cross-channel layout, and log format must be fixed in gate_lock before results are produced." / "assert abs(mp_me_measured/pi**5 - 6) < 2e-4"

**Evidence.** 6π⁵ = 1836.118109, against CODATA-2022 1836.152673426(32). The difference is −18.8 ppm, or 1.08×10⁶ σ. As an exact [F] equality this relation is excluded. m_H = 124.695 GeV against PDG-2024 125.20 ± 0.11 GeV is −0.40%, or −4.6σ (−3.3σ against PDG-2022 125.25 ± 0.17). The check's tolerance of 2e-4 on m_p/m_e/π⁵ (33 ppm) was set with the answer already known: 6π⁵ ≈ m_p/m_e is F. Lenz's 1951 observation (Phys. Rev. 82, 554), which the text does not cite. Declaring residuals non-falsifying, without any stated theoretical uncertainty, means no Gate on m_p/m_e or m_H can ever FAIL. That contradicts §1.4's requirement to pre-register tolerances and makes Kill criterion 2 toothless for the headline numbers.

**Proposed improvement.** For each headline relation, pre-register a theory-error model in gate_lock: 'leading-order relation; corrections expected ≤ ε' with a numeric ε. Gate as PASS only if |residual| ≤ ε. Rewrite §1.10(i) as 'a residual outside the pre-registered ε is a falsifier'. Regrade 6π⁵ and 5π from [F] to [H] (approximate relation) until a correction term is derived. Cite Lenz (1951) as prior art.

### 6. [major] The no-tuning 'proof' tools cannot detect discrete selection; A3's joint probability is asserted but never computed, and most of its 'five survivors' are not independent evidence

- **category:** numerology-look-elsewhere
- **location:** 01 §1.8.3 (five-line and geometric checks), §1.8.4 (forced-coefficient test), §1.9 A3; 11 §11.6.5 (A_geo 0.16%); repro/physics/tools/vp_numeric_ssot.py line 111

**Quote.** "This refusal to migrate is itself a structural signature: it is what distinguishes a derivation from a fit." / "if a reader's run prints anything other than ALL PASS, the framework is wrong and the" / A3: "rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm), Tₑ≈1 s ( +0.6%), and A_geo (0.16%)" … "The joint probability of the surviving five under a six-line geometric chain with one anchor is the structural claim. This is not proof; it is a coincidence count." / 11: "the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%" / tool: "[H] Δt 3 s.f. ⚠placeholder"

**Evidence.** The five-line script only evaluates the claimed closed forms. The geometric checks assert arithmetic facts (lattice counts 19/27/81/123, 2/π, 1/π², the ring sum) that cannot fail. So 'ALL PASS' verifies arithmetic, not the framework. The forced-coefficient test rules out continuous nudges (the Higgs would need 4.9798π) but not the choice of (6, π⁵) or 5π from a family. I estimated look-elsewhere probabilities as the local family density times the tolerance window. Family {p·π^n; p ≤ 7, 0 ≤ n ≤ 7} (56 values, matching the ledger's 'integers up to 7'): P(hit within 18.8 ppm of m_p/m_e) ≈ 3.4e-4. With rationals p/q (p, q ≤ 7, −2 ≤ n ≤ 7; 350 values) it is ≈ 1.1e-3. For U_lat/m_H within 0.40%: 0.054 (simple family) to 0.27 (rational family), before the N and anchor freedom, which pushes it toward 1. For r_p/λ_C,p = 2/π: ≈ 0.012 at 0.02%, or ≈ 0.15 at CODATA-2018's own 0.23% uncertainty. T_e ≈ 1 s is in SI units, and its +0.6% is only about twice the ±0.27% rounding of the 3-s.f. Δt. A_geo compares against a value the repro tool itself labels a placeholder. The text defines A through the median, yet A_med(750) = 4.76e5 lies 16% below the A_mean used for the match. With the natural scaling (N = 200 → 750) I get +0.35% for the mean and −16% for the median, so the 0.16% cannot be reproduced from what is stated. The evidential weight of A3 therefore reduces to roughly one coincidence, 6π⁵, which is pre-existing.

**Proposed improvement.** Replace §1.8.4 with a pre-registered look-elsewhere computation: define the expression grammar actually allowed and the list of targets that were tried, compute the trial factor, and report a global p-value for A3's set. Drop T_e and A_geo from the surviving set. Count r_p only for its 2/π content, at CODATA-2022 uncertainty. Specify the median-vs-mean choice and the scaling reference for A_geo in analysis_lock before re-running. Rewrite the §1.8.3 closing sentence to say the script checks reproducibility of the arithmetic, not truth.

### 7. [major] The '+61 ppm' r_p / ν_p cross-check is a rounding artifact; the real discrepancy is +18.8 ppm, which is the m_p/m_e residual

- **category:** math-error
- **location:** 02 §2.2.1 (exception clause), §2.2.3(B) r_p status note; 01 §1.9 A3; vh v0.4.1 (canon_derived ν_p = 292.2451560); repro/physics/tools/vp_numeric_ssot.py (RP_LCK)

**Quote.** 02 §2.2.3(B): "the forced (2/π)λ_(C,p)=0.8412 fm is its +61 ppm cross-check." / 02 §2.2.1: "the value retained in canon_lock is now its +61 ppm cross-check reference." / 01 A3: "the νₚ length route (+61 ppm) is the same chain as" / tool: "RP_LCK = D(\"8.412e-16\")"

**Evidence.** D/(6π⁶) = 0.8412515 fm. The canon_lock r_p = 8.412e-16 m is (2/π)λ_C,p = 0.8412356 fm (CODATA m_p) rounded to 4 significant figures. Then 0.8412515/0.8412 − 1 = +61.2 ppm, whereas 0.8412515/0.8412356 − 1 = +18.8 ppm. The +18.8 ppm is exactly the 6π⁵ residual: with D = 2λ_C,e, D/(6π⁶) ÷ (2/π)λ_C,p = (m_p/m_e)_meas/6π⁵. The same holds for ν_len = D/(2 r_p,lock)/π² = 292.24516 (+61.2 ppm vs 3π⁴); with the unrounded r_p it is 292.23277 (+18.8 ppm). So 42 ppm of the advertised discrepancy is the ±59 ppm half-width of a 4-digit rounding. Separately, '−0.018% vs CODATA 0.8414 fm' is 0.08σ of the 2018 uncertainty (±0.0019 fm), so quoting it as a precision residual is misleading. Against CODATA-2022 (0.84075(64) fm) it is +0.060%, i.e. +0.78σ.

**Proposed improvement.** Either lock r_p unrounded or remove the lock. Restate the cross-check as '+18.8 ppm, identical to the m_p/m_e residual (not independent)'. Regenerate canon_derived ν_p. Update to CODATA-2022 r_p and quote residuals in σ, not %.

### 8. [major] r_p is both a canonical input and a derived prediction, violating the chapter's own no-overloading and SSOT rules; 'core radius' is silently equated with the rms charge radius

- **category:** internal-inconsistency
- **location:** 02 §2.1.5(B) table, §2.2.1, §2.2.2, §2.2.3(B), §2.1.6, §2.7; 01 §1.2.5 (dependency direction)

**Quote.** "| r_p | CAN-INPUT | radius (locked) | OBJ-CORE reference radius (meaning must be locked)" / "r_p : canonical radius (defined as the proton core radius)." / "The value of r_p is locked as a canonical input value; the unit is locked as length." / "Under LOCK-NU-N (§8.0.5), r_p is a derived prediction r_p=D_anch/(6π⁶)=0.84125 fm, not a free canonical input" / §2.1.6: "The same symbol simultaneously has different hierarchy types (CAN-INPUT vs REAL-PRIMARY, etc.)."

**Evidence.** One symbol, r_p, currently carries two values (0.84125 fm predicted, 0.8412 fm locked) and two hierarchy types (CAN-INPUT in the table and list, derived in the status note). Under §2.1.6 and §2.4.4 (R2) that is an immediate FAIL. The 'Exception, v0.2.1' clause is a patch by interpretation, which §2.7 forbids ('conflicts are not repaired by interpretation'). The same subsection mixes pre- and post-v0.2.1 statements, contrary to the §1.2.6 no-mixing rule. On meaning: CODATA's r_p is the rms charge radius √⟨r²⟩ from hydrogen/muonic-hydrogen spectroscopy and scattering. A geometric core radius R is not the same quantity (a uniform sphere has r_rms = √(3/5)R = 0.775R; a thin shell has r_rms = R). §2 Priority 1(iii) requires locking 'the measurement convention to which the numeric value is bound', and no such identification is stated.

**Proposed improvement.** Split the symbol into r_p^pred := D/(6π⁶) (CAN-DERIVED) and r_p^ref (OBS-REF: CODATA-2022 rms charge radius). Remove r_p from the CANON list and add λ_C,e/m_e instead, since that is the real input. Add an explicit mapping 'core radius ≡ rms charge radius' graded [H] with its justification, or compute the rms radius of the model's charge distribution.

### 9. [major] The governance chapter contradicts itself on the LOCK taxonomy (four categories vs three) and on where Gates, PASS.rules and log schemas live

- **category:** internal-inconsistency
- **location:** 01 'Declaration of LOCK', §1.2 / §1.2.1 / §1.2.4, §1.3.2(C), §1.3.4, §1.3.5, §1.4; 11 §11.5.3 table; w0 scorecard

**Quote.** "At minimum, this document separates LOCK into the following four categories." (canon/realization/gate/protocol) vs §1.2: "LOCK is separated into three types by role." … "The three LOCKs have different roles and must not be mixed." / §1.4: "must be fixed in gate_lock before results are produced" vs §1.3.5: "PASS.rules is included in analysis_lock and cannot be modified after seeing results." and §1.3.2(C): "Stack order and conditions are pre-registered in analysis_lock." / §1.3.4: "The log format (JSON/YAML/CSV) is fixed in protocol_lock" / 11: "| Tolerance dev_max | gate_lock.rcross.dev_max |" and "| Split integer N (e.g., 10¹²) | analysis_lock.anchor_split.N |" vs w0: "| N | 10¹² | canon_lock | §11.2 | split integer | lock"

**Evidence.** The same chapter defines the LOCK system two incompatible ways: {canon, realization, gate, protocol} and {canon, realization, analysis}. Gate thresholds are pre-registered in gate_lock in one place and in analysis_lock in another. Log schemas are in protocol_lock in one place and analysis_lock (§1.2.4) in another. Downstream chapters use both sets, and the split integer N is filed in two different locks. This breaks the chapter's own rule 'Every fact lives at exactly one address' in the very place that defines the addresses.

**Proposed improvement.** Adopt one taxonomy, for example canon/realization/analysis with gate and protocol as named sub-registries of analysis. Rewrite the Declaration of LOCK, §1.2–§1.4 and the §11.5.3 mapping table to match. Add a registry lint that fails on any reference to a non-existent lock category or on an item filed in two locks.

### 10. [major] The LOCK/Gate/PASS.rules machinery is declared but not implemented, so by §1.3.8 every headline sentence is a 'forbidden pattern'

- **category:** reproducibility-code
- **location:** 01 §1.2.4, §1.2.5, §1.3.3–§1.3.9; repro/physics/registry/vp_locks.csv; repro/physics/tools/gate.py; repro/physics/tools/vp_numeric_ssot.py

**Quote.** §1.3.8: "No-Gate conclusion forbidden: numerical/law statements without Gate identifiers or verdict status (PASS/FAIL/INCONCLUSIVE)." / §1.2.4: "Therefore the analysis_lock identifier must appear in every conclusion sentence." / gate.py: "# phase 4 = 수치 드리프트 게이트(SSOT: tools/vp_numeric_ssot.py)."

**Evidence.** Across all 49 extracted physics chapter texts, the mandated '[LOCK:…]' / '[GATE:…]' tags occur only in chapter 01 (9 hits, all inside the templates themselves). No canon_lock.json, realization_lock.json, analysis_lock.json or PASS.rules file exists in the repository. vp_numeric_ssot.py hard-codes CANON, and its optional loader finds nothing. registry/vp_locks.csv has 10 rows with unversioned ids ('delta', 'alpha', 'anchor', …) and no version or hash. The implemented gates (gate.py phases 1–4) check word counts, equation/figure/table counts, page size and numeric display drift. None of G-SYM, G-LOCK, G-REG or G-NT exists as code (grep of repro/physics/tools finds none), and no Gate record with the §1.3.4 fields (gate_id, lock_refs, thresholds, fail_labels) exists. By the chapter's own rules, the headline numbers therefore have no conclusion admissibility.

**Proposed improvement.** Either implement a minimal version: (a) publish versioned lock JSONs with lock_id = content hash; (b) emit one Gate record per headline claim with the §1.3.4 fields and a pre-registered threshold; (c) add a linter that fails any [F]/[V] numeric claim lacking a lock_id and gate_id (derive_meta.py already writes data-locked attributes that could carry them). Or cut §1.1–§1.3 down to the rules actually enforced and mark the rest 'design intent — not yet enforced'. Being truthful about enforcement is itself a No-Tuning requirement.

### 11. [major] Grades are never defined in the governance chapter; measured anchors are graded [F]; hybrid and inflated grades; [H] clashes with the corpus-wide [L]

- **category:** grading-honesty
- **location:** 01 header lock cards, chapter lede, §1.9 preamble, A1, A2, A7; repro/physics/registry/vp_locks.csv; AGENTS.md §5

**Quote.** "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." / "D = 4.8526 pm — Quantum (anchor) diameter that fixes the lattice length scale. [F] forced." / lede: "Grade [F] forced." / "Each item is either resolved ([F]{}/[H]{}) with a pointer to the resolution, or flagged open ([O]{})" / A2: "Partially resolved [H]+." / A7: "Resolved [F]+[O]." / AGENTS.md: "`[L]` anchored / locked — rests on a single declared empirical anchor (a LOCK)."

**Evidence.** The governance chapter defines PASS/FAIL/INCONCLUSIVE and the CT-* claim types but never defines [F]/[V]/[H]/[O] and gives no crosswalk between the two systems. A measured wavelength cannot be 'forced', and D = 2λ_C,e is an m_e calibration, yet both carry [F] (the w0 scorecard itself calls D 'anchor-derived'). A1 is [F] although its support (§11.6.2 and §11.6.3) is [H]. The chapter as a whole is graded '[F] forced' although it consists of declarations (CT-DEF). Across the physics texts [H] appears 61 times, plus hybrids ('[H]+' ×7, '[F]+[O]' ×3, '[V/committed]'). AGENTS.md defines no [H], using [L] for anchored. LaTeX residues '[F]{}' remain in the text.

**Proposed improvement.** Add a §1.0 'Grades' section that defines each grade, maps grades to Gate verdicts and CT types, and states the rule grade(conclusion) ≤ min grade(premises). Regrade λ_anchor and D to [L] (anchor), A1 to [H], and the governance chapter to CT-DEF (no grade). Replace hybrid grades with one grade per sub-claim. Make [H] vs [L] consistent with AGENTS.md across the corpus.

### 12. [major] Symbol clashes that the notation chapter's own rules would mark as immediate FAIL (D_anch/ℓ_rot/cube edge, g*, α, δ, R_p/r_p, L_q/λ_C, a)

- **category:** internal-inconsistency
- **location:** 02 §2.1.2(B)(C), §2.1.5(B)(C) tables, §2.1.6, §2.2.3(E), §2.4.3(C); 01 §1.8.1, §1.10 Kill 2; wsum; 09 §9.4; 11 §11.6.1; 17 §17.4; registry/vp_locks.csv; AGENTS.md (cosmology row)

**Quote.** §2.4.3(C): "The representative-length symbol of a cube cell may be written as L_cell or D_anch, etc., but regardless of the spelling the geometry_meaning must be locked as edge." / 01 §1.8.1: "Geometry (no DOF): canonical cell = cube" / §2.1.5(B): "| D_anch | CAN-INPUT | diameter or length (locked) | OBJ-CELL or canonical cell length (meaning must be locked)" / §2.2.3(E): "Therefore, replacing ℓ_rot by D_anch, or redefining the meaning of D_anch from ℓ_rot, is forbidden." vs wsum: "Quantum diameter D=ℓ_rot: definition §3.4" / §2.1.2(C): "a and Δ t are not reused with other meanings (e.g., area or acceleration)." / vp_locks.csv: "cap,g*,c²·Ψ_yield,Gravity-cap mechanism: a yield-limited acceleration ceiling" vs 11: "the percolation gap g^* and the structural amplification A = a/g^*" / §2.1.2(B): "Component indices are written as Greek letters or coordinate subscripts: α, β or x,y,z." / Kill 2: "Rₚ/L_q=2/π, σ/L_q²=4/π, α=2/π, δ=1/π² are claimed as fixed geometric outputs."

**Evidence.** (a) D_anch is at once a cube-cell edge (§2.4.3(C) together with 'canonical cell = cube'), a quantum diameter (lock card, §3.4), equal to ℓ_rot (wsum, §9.4, which §2.2.3(E) forbids), and 2λ_C,e. The registry table leaves it as 'diameter or length': this is RD-AMB, CELL-CONFLICT and overloading in one. (b) g^* is a percolation gap with dimension L (A = a/g^*), while g_*, written 'g*' in the lock registry, is an acceleration L T⁻²: a DIM-MISMATCH on the same glyph. (c) α stands for the rectification 2/π, α_em and a component index. (d) Bare δ is used for rectification although §2.1.6 prescribes δ_rect; δ_proj and δ_eff also appear. (e) The proton radius is written both r_p and Rₚ, and its Compton wavelength as L_q, λ_C and λ_(C,p) (13: 'λ_(C,p)≡λ_C'). (f) 'a' is reserved, yet a_med (median neighbour distance) is used in physics, and a₀ = cH₀/2π, an acceleration, in cosmology. That is exactly the reuse §2.1.2(C) names. (g) Table entries 'CAN-INPUT or OBS-REF' (ℓ_rot), 'REAL-DERIVED or CAN-DERIVED' (T_p, T_n) and 'OBJ-VP or …' (a) leave types unresolved, contrary to §2.1.6.

**Proposed improvement.** Publish the actual symbol registry (one row per symbol: object_id, geometry_meaning, dimension, hierarchy type) and run an overloading lint. Rename: D_q ≡ 2λ_C,e for the quantum diameter; L_cell for the cube edge; ℓ_rot^sim (OBS-REF) for the simulated circulation length; g_gap vs g_cap; α_rect vs α_em; δ_rect; unify on r_p and λ_C,p; a_med → d_med. Record the cosmology a₀ as a cross-volume exception or rename it. Resolve every 'or' in the §2.1.5 tables.

### 13. [major] The lede's claim that '89/82 legitimately tracks mₙ>mₚ (gravity)' is unquantified, contradicts chapter 14, and re-purposes a demoted factor after the fact

- **category:** physics-validity
- **location:** 01 lede/abstract and §1.9 A4; 14 §14.0.4; 01 §1.1.2 (A), (G)

**Quote.** 01: "The 89/82 legitimately tracks mₙ>mₚ (gravity), not Coulomb." / 14: "it tracks the mₙ≈mₚ core, not charge"

**Evidence.** 89/82 = 1.085366, while m_n/m_p = 1.0013784 (CODATA 2022). Neither chapter gives any functional relation between them. Chapter 14 says the factor tracks near-equality (m_n ≈ m_p); the chapter-01 lede says it tracks the inequality (m_n > m_p). The neutron–proton mass difference (1.293 MeV) comes from m_d − m_u and electromagnetic self-energy, not from gravity. The 89/82 factor was demoted as an overfit in K_C (−0.43%). Moving it to a new sector without a new quantitative, pre-registered test is the post-hoc meaning change that §1.1.2(A) and (G) label FAIL-NT-DEF. A physics claim also does not belong in the lede of a governance chapter.

**Proposed improvement.** Remove the sentence from the governance lede. If the claim is kept in chapter 14, state a quantitative relation between 89/82 and a measured mass-sector observable, with a pre-registered tolerance. Otherwise grade it [O] or NON-EVIDENCE, as was done for the α_em closed form, and make the chapter 01 and 14 wordings agree.

### 14. [minor] The rectification-constant card is wrong, and the canonical-input list picks the derived constant

- **category:** math-error
- **location:** 01 and 02 header lock cards (α, δ); 02 §2.2.2, §2.2.3(D); registry/vp_locks.csv

**Quote.** "α = 2/π — Geometric rectification ratio (full-wave to half-wave mean); the single rectification anchor. [F] forced." / 02 §2.2.2: "δ : a rectification constant (dimensionless)."

**Evidence.** The mean of a full-wave rectified sine is 2/π and the mean of a half-wave rectified sine is 1/π, so the full-wave/half-wave ratio is 2, not 2/π. 2/π is the full-wave mean relative to the peak. δ = 1/π² = α²/4 is derived from α (or from π), yet δ is listed as a canonical input while α, called 'the single rectification anchor', is not. δ's gloss 'a max-entropy measure' is never explained.

**Proposed improvement.** Change the gloss to 'mean of |sin| (full-wave rectified mean / peak) = 2/π'. List α (or neither, since both are π-derived) as CAN-DERIVED from π, and record δ := α²/4 as CAN-DERIVED. Explain or remove 'max-entropy'.

### 15. [minor] The dimension registry treats energy and force as base dimensions and has no charge dimension

- **category:** unit-dimension
- **location:** 02 §2.1.3(B)

**Quote.** "Energy dimension: E" / "Force dimension: F"

**Evidence.** E = M L² T⁻² and F = M L T⁻² are not independent of L, T and M. Treating them as base dimensions stops a dimensional checker from catching mismatches between derived quantities (for example U_lat = hc/a in J versus F_lat = hc/a² in N) unless each is hand-tagged. There is no current/charge dimension even though the volume treats Coulomb, K_C and α_em, and no temperature. An actual dimensional slip survives in 11 §11.6.2 ('one length scale' is said to yield (length/time)²).

**Proposed improvement.** Use SI base dimensions (L, M, T, I, Θ) with E and F derived. Store a dimension vector per registry symbol and auto-check every registered equation (e.g. with pint) as the G-SYM gate.

### 16. [minor] Kill criterion 1 is worded backwards, and a meta-lesson contradicts the unified B1 status in the same section

- **category:** internal-inconsistency
- **location:** 01 §1.10 Kill criterion 1; §1.9 'Meta-lessons' vs §1.9 B1

**Quote.** "If any reader can show that a published prediction (e.g., mₚ/mₑ=6π⁵) is actually free of a coefficient that we silently fitted, the no-tuning claim collapses." / Meta-lessons: "it has not yet made a narrow-sense forward prediction. Both facts are honest." vs B1: "wordings of this item (\"no narrow-sense prediction\", \"the most important open item\") and the contrary wordings of"

**Evidence.** 'Free of a fitted coefficient' is the no-tuning claim itself; the kill condition should be 'depends on a coefficient that was silently fitted'. B1 says the wording 'no narrow-sense prediction' has been replaced everywhere, yet the meta-lesson a few lines below still says the framework 'has not yet made a narrow-sense forward prediction'.

**Proposed improvement.** Reword Kill 1 as 'depends on a coefficient (continuous or discrete) that was selected after seeing the data'. Update the meta-lesson to match B1's single status (or to the downgraded status proposed above).

### 17. [minor] A7 mischaracterises the hierarchy problem, and Kill criterion 4 commits no numerical onset

- **category:** physics-validity
- **location:** 01 §1.9 A7; §1.10 Kill criterion 4

**Quote.** "This separation is isomorphic to the standard-physics hierarchy problem: a force law fixes shape, not coupling magnitude." / "A controlled experiment that exhibits clean 1/R² dependence without a saturation onset, at scales where the cap should be active, would falsify the gravity portion of the framework."

**Evidence.** The hierarchy problem concerns the sensitivity of the Higgs mass (the electroweak scale) to much higher scales (the Planck scale) under radiative corrections. It is not the general fact that a force law leaves its coupling free. Kill 4 names no acceleration, radius or velocity at which the cap 'should be active'. Because Ψ_yield is back-substituted per body (g_⊕/c²), no existing inverse-square test (torsion balances at sub-mm range, lunar laser ranging, satellite geodesy) can be said to meet or violate it.

**Proposed improvement.** Drop the hierarchy-problem analogy or state the correct one. For Kill 4, commit a numerical onset (e.g. predicted saturation acceleration or radius for a named body or experiment) before measurement, and check it against existing inverse-square-law bounds.

### 18. [minor] Rendering and structure defects in the rule-defining chapters

- **category:** presentation-rendering
- **location:** 01 section headings and §1.2.3/§1.2.4 titles; 02 §2.1.2(A)(B), symbol-registry list, §2.2.4, §2.4.4(R3), §2.4.5(A), eq. a_value_lock alt text

**Quote.** "### 1.2.3 Definition of realizationₗock (unit-realization freezing)" / "symbol: the symbol string (e.g., a, D_anch, r_p, stringℓ_rot, etc.)." / "(e.g., ℓ_rot=lrot)" / "Diameterleftrightarrowradius conversion, cubeleftrightarrowsphere mapping" / "X denotes only a result produced by a pre-registered averaging operator." / alt text "a \;=\; \aVP."

**Evidence.** Confirmed in the deployed HTML (docs/physics/0{1,2}-…/index.html). Underscores render as subscript glyphs (realizationₗock, analysisₗock, gateₗock, unitₙame, conversionₚolicy). Macros are unexpanded in visible prose ('lrot', 'stringℓ_rot', 'leftrightarrow'). The overbar the chapter mandates for averages is lost ('X'), and the bold-italic vector convention is not rendered. The SVG for a = 6.3299…×10⁻¹⁹ m is correct, but its alt text is '\aVP', which is what screen readers and AI extractors see. Section order is 1.4, 1.5, 1.1, 1.2, 1.3, 1.8, 1.9, 1.10 (1.6 and 1.7 are missing) and 2.5, 2.6, 2.7, 2.1–2.4 with unnumbered heads. A Korean button label '재현 코드 (GitHub)' appears on the English page.

**Proposed improvement.** Fix the TeX-to-HTML conversion for \_, \leftrightarrow, \overline and \boldsymbol. Expand macros in alt text. Renumber sections in reading order (or restore §1.6 and §1.7). Add a phase-2 gate that fails on residual 'leftrightarrow', '\\[a-zA-Z]+' in alt text, and subscript-letter artefacts.

**Strengths noted:**
- §1.1.2's taxonomy of tuning modes (definition, value, closure, Gate, selection, protocol, external justification), with FAIL-NT-* labels and version-up-only change, is a useful checklist that most speculative-physics work lacks.
- The framework has recorded real self-demotions: the Coulomb 89/82 '−0.43%' was reclassified as an overfit, the α_em closed form was marked COINCIDENCE/NON-EVIDENCE and excluded, 'three independent routes' to D was retracted to 'one anchor', the ν_p length route is not double-counted, and A6 openly flags the missing external replication.
- The diameter/radius/cell-geometry discipline in §2.4 (explicit derived symbols such as r₀ := D/2, immediate-FAIL labels) targets a real and common source of factor-of-2 errors.
- There is code-backed numeric consistency: vp_numeric_ssot.py regenerates the displayed numbers from one input set and fails the build on display drift, and the five-line check lets anyone reproduce the closed forms in seconds.
- The v0.8 input-convention note in §10.9.1 openly documents that the full-precision λ_ref changes χ. That disclosure is honest, even though its conclusion (the prediction is not sharp) has not yet been drawn.
- IRREPRODUCIBILITY_LEDGER.md states a specific obstacle for each non-reproducible [O] item (absolute g, α_em), as the framework's own rules require.


## review:axioms-semantic

### 1. [critical] The axioms (infinite rigidity, full packing, no pair potential) rule out the substrate used to verify c²=B/ρ

- **category:** physics-validity
- **location:** 03-axioms-primitives-volume-particle-lattice: VP-A1, VP-A2, [D-5], [A-1], §3.1.5, §3.2.5.1, VP-N1. Cross-refs: sp-jamming-spine S2.1–S2.4; 11-realization-units-t-rcross §11.6 table

**Quote.** "Incompressible: the internal volume of a VP does not change." | "Define Full Packing as the property that the union of VP occupied regions fills the domain." | "any configuration that violates it is judged inadmissible and cannot be used as an input for derivation/verification." | "A universal interaction assumed as a function of distance only: adding a universal function f(d_(ij)) for every VP pair (i,j) and using it as the ground for all later derivations." | SP: "S2.1 [axiom]. VP particles are infinitely rigid and fully packing, so the vacuum is a jammed lattice." ... "reproduced for the harmonic-contact substrate" | ch11: "| Jamming point | φ_jam=0.633, z→6 isostatic, K=2.05×10⁴ | lattice_3d_jam_percolation.py"

**Evidence.** The [V] result for c²=B/ρ (SP S2.3–S2.4) comes from the O'Hern–Silbert–Liu–Nagel harmonic-contact model, U_ij=(k/2)(σ−r_ij)² for r_ij<σ. In that model every bit of elasticity comes from particles overlapping. [A-1] forbids overlap and says such configurations "cannot be used as an input for … verification". The model also rests on a universal distance-only pair function, which §3.1.5 prohibits by name, and on global energy minimization, which §3.1.5 also prohibits as an "optimization goal".

B is measured in units of the spring constant k (SP: B_Born=0.90/1.13/1.40 at N=256/512/1024). A1 sets exactly that k to infinity. In the Stone limit k→∞, B→∞ at and above φ_J (hard-sphere pressure diverges like 1/(φ_J−φ)), so c²=B/ρ is not finite.

Full packing fails numerically: φ_jam=0.633 leaves 1−0.633=36.7% of the domain empty. The [D-5] reinterpretation ("fills" means "no new degrees of freedom for empty space") does not save it, because it leads to a dilemma:
- If Ω_i is the sphere, A2 is false (φ=0.633≠1).
- If Ω_i is the Voronoi cell (φ=1 automatically), A1's fixed volume is false, since Voronoi volumes change with every rearrangement.

Two smaller conflicts: under A2 the "occupancy-based" control parameter of §3.2.5.1 is always 1, so it cannot vary monotonically. And VP-N1 introduces finite K_soft and K_jam, although [A-1] says no later section treats rigidity as a tunable value.

**Proposed improvement.** Pick one consistent substrate and rewrite §3.1 to match it.
- Option A (matches the evidence): VPs are frictionless soft spheres with a finite contact stiffness k, declared as a CL-R closure, with all outputs reported in units of k/σ. Packing fraction becomes a state variable with φ_J≈0.64. Move "pairwise contact law" and "energy minimization" off the §3.1.5 forbidden list and into declared closures.
- Option B: keep Stone rigidity and full packing, redo S2 with an event-driven hard-particle model (where moduli are entropic, ∝nk_BT, and diverge at φ_J), and show that a finite c still emerges.

Until one of these is done, regrade c²=B/ρ as "[V] for harmonic soft spheres; link to the VP axioms [O]".

### 2. [critical] The 'minimal axiom set' is not the one actually used: 9 more [A]-axioms appear downstream, several on §3.1.5's forbidden list, and the axiom list differs between chapters

- **category:** internal-inconsistency
- **location:** 03 'VP axiom set', §3.1.1, §3.1.3, §3.1.5, primitive_chain, tagline, §3.2 tag. Cross-refs: 00 prologue; 05 §5.2.5 [A-5.2-U0..U4]; 09 §9.2.5 [A-9.2-S1, S2]; 13 [A-13.2-1], [A-13.6-1]

**Quote.** "This section locks infinite rigidity, full packing, and the local rule as [A] for the VP world" | "(VP-A4) Adjacency axiom: lattice/graph as a primary object" | "Three axioms and a list of forbidden smuggled assumptions." | ch00: "Axiom step: lock infinite rigidity (Stone), full packing, and the existence of a jamming regime." | §3.1.5: "Axiomatizing a probability distribution: fixing a specific distribution (e.g., a particular noise model or randomness) as a primary axiom for the initial condition or update process and justifying results as a consequence of that distribution." | ch05: "[A-5.2-U1] full-cycle uniformity (Null): the distributions of θ,φ take the uniform distribution of (delta_uniform_measure) as the default state" | "[A-5.2-U3] product measure (uncorrelated): when no bias/constraint information exists, the joint measure is treated as the product measure" | "Double rectification survives at $1/π²$ under the max-entropy measure" | ch09: "[A-9.2-S1] Canonical stationarity axiom (existence and convergence of long-time averages)" | "[A-9.2-S2] δ-universality axiom (value fixation in applicable regimes)" | ch13: "[A-13.2-1] Mass–resistance correspondence axiom" | "[A-13.6-1] Mass = resistance axiom (operational axiom)"

**Evidence.** The primitive_chain claims "VP axiom set ⟹ … ⟹ rectification / events / realization / mass / force". But none of α=2/π, δ=1/π², ν_p=3π⁴ or m_p/m_e=6π⁵ follows from A1–A3 alone:
- α=⟨|cosθ|⟩ needs the uniform measure [A-5.2-U1].
- δ also needs the product measure [A-5.2-U3]. That is a maximum-entropy choice, and it hits three §3.1.5 prohibitions at once: a probability distribution, a maximized global objective, and assumed isotropy.
- ν_can=sδ needs ergodic stationarity [A-9.2-S1] and δ-universality [A-9.2-S2].
- All masses need [A-13.2-1].

Sensitivity (computed numerically): with an anisotropic phase density p(θ)∝1+b·cos2θ, ⟨|cosθ|⟩=(2/π)(1+b/3). b=0.03 moves α from 0.636620 to 0.642986 (+1.0%). An anisotropy of order 10⁻⁴ shifts α by tens of ppm, the size of the 6π⁵ residual. So the "[F] forced" numbers are exactly as forced as the uniformity axiom.

The axiom count itself is inconsistent:
- The top of ch03 lists four axioms (VP-A1..A4, including "Identity" and "Adjacency").
- §3.1 lists three ([A-1..A-3]); adjacency is demoted to [D-6] and identity is missing.
- The tagline says "Three"; the §3.2 tag says "VP-A1..A4".
- ch00 and ch01 replace the local rule with "existence of a jamming regime".

[A-13.2-1] and [A-13.6-1] state the identical equation m=U_lat/σ_eff twice, breaking the chapter's rule that redundant statements across axioms are forbidden.

**Proposed improvement.** Put a single canonical axiom table in §3.1 that lists every [A] used anywhere: A1 Stone, A2 packing, A3 locality, U1 uniform measure, U3 product measure, S1 stationarity, S2 δ-universality, M1 mass–resistance. Mark each as a physical postulate or a convention/closure.

Then:
- Amend §3.1.5 so it no longer forbids items the framework actually adopts.
- Add a matrix of headline result × axioms used.
- Relabel α, δ, 3π⁴ and 6π⁵ as "[F] given {U1, U3, S1, S2}" instead of unconditional [F].
- Test U1/U3 directly: run a KS test on phase-angle histograms from the rotation simulations.

### 3. [critical] The wrong wave survives: the axioms imply an incompressible (transverse-only) medium, but the spine keeps only the longitudinal mode and calls it light

- **category:** physics-validity
- **location:** 03 VP-A1, [A-1], [A-2]. Cross-refs: sp-jamming-spine S2.3; 10 §10.9

**Quote.** "Incompressible: the internal volume of a VP does not change." | "Inside the domain D, space is fully occupied by VPs ([D-5])." | SP: "The transverse wave dies; one longitudinal speed survives," | ch10: "On the jammed lattice, light propagates as a transverse oscillation of the rotating quanta"

**Evidence.** In an isotropic elastic continuum, c_L²=(B+4G/3)/ρ and c_T²=G/ρ. The spine's result G_relaxed→0 at z=6 gives c_T→0, so no transverse wave. What remains is a single longitudinal compression wave, c²=B/ρ, with one polarization.

Light has two transverse polarizations and no longitudinal mode (Malus's law; photon helicity ±1).

The axioms point the other way. A1+A2 (incompressible bodies, no free volume) give ∇·u=0 in the continuum limit, i.e. B→∞ and c_L→∞. That removes the longitudinal wave and leaves transverse waves, provided G>0. This is the 19th-century Green/MacCullagh/Kelvin elastic-aether route.

So the axioms and the spine go in opposite directions, and neither gives a transverse wave at speed c:
- The spine has a longitudinal-only wave.
- §10.9 has a transverse oscillation carried by a medium whose transverse modulus is zero.

This undercuts the physical reading of the headline c²=B/ρ.

**Proposed improvement.** State explicitly which elastic mode is light.
- If transverse, the relevant relation is c²=G/ρ (or a MacCullagh rotational-elastic modulus), and the isostatic G→0 result becomes a problem, not support.
- If longitudinal, derive two polarizations and the absence of a longitudinal photon, which looks impossible.

Add a concrete check to the jamming bundle: diagonalize the dynamical matrix at z≈6 and report the polarization content (transverse fraction) of the lowest-q propagating modes and how many propagating polarizations exist. Register "exactly two transverse polarizations at speed c" as a falsifier.

### 4. [major] D_anch is at once a cube edge, a 'quantum diameter', a circumference and ℓ_rot — an immediate FAIL under the chapter's own G-SYM and CANON-REF rules

- **category:** internal-inconsistency
- **location:** 03 §3.3.2, §3.3.6, §3.3 tag, §3.4 anchor block and Concept links, §3.4.1–3.4.6; 04 §4.3.3 R-BASE-001. Cross-refs: 09 §9.4; 10 §10.9; sp S3; 05 §5.2.6; 08 grinder; repro/physics/registry/vp_locks.csv

**Quote.** "Define the representative length D_anch of the canonical Anchor Cell as the edge length of CELL-CUBE." | "No symbol-meaning conflict: D_anch must be locked as edge in CELL-CUBE and cannot be used as a diameter or radius in the same context." | "Diameter is diameter: the G-SYM tripwire is set here." | "The quantum diameter is carried as a single anchored constant, D_anch:=2λ_(C,e)=4.8526pm" | "Concept links: D=ℓ_rot is computed in §9.4" | "Using ℓ_rot to redefine the meaning or value of canonical inputs such as D_anch, rₚ, δ, π is forbidden." | "ℓ_rot is used as an input of the mandatory derivation chain without promotion (without a version-up)." | SP: "The quantum diameter is one2π phase winding,D=2π a_{phys}=2πλ/A." | vp_locks.csv: "d-anch,D,4.8526 pm,Quantum (anchor) diameter that fixes the lattice length scale.,F" | ch04 R-BASE-001: "- \"drive: DRV-ROT\"" | ch05: "If one uses δ as a universal constant as-is in a regime where a drive axis or anisotropy axis such as DRV-ROT is turned on in the regime coordinates" | ch08: "[V] grinder MDin: rotation / out: 79–82-cell core"

**Evidence.** One symbol carries three geometric meanings:
- a cube edge (§3.3.2);
- a sphere diameter (§3.4, the registry, the SP table);
- a circumference 2π·a_phys (SP S3: "the rotational circumference 2π is the natural length").
§3.3.6 declares any such mixed use an "immediate FAIL".

Separately, §3.4, ch09 and ch10 set D=ℓ_rot. Yet ℓ_rot is a CANON-REF quantity, locked as a diameter scoped to rotation-driven (DRV-ROT) regimes, and it has a different value (4.8542 pm vs D_anch=4.852620 pm, +0.03%). §3.4.2 and §3.4.6 forbid exactly this identification.

It also brings a DRV-ROT quantity into the base regime R-BASE-001, whose registry entry forbids DRV-ROT extrapolation. ch05 forbids using δ as universal in DRV-ROT regimes, yet the δ-based ν_p is the "grind rate" of the rotation-driven grinder simulation (ch08).

By the framework's own rules, the canonical chain therefore fails both G-SYM and FAIL-REG-EXTRAP.

**Proposed improvement.** - Rename the cell edge (e.g. L_cell) and keep D for the quantum length. Say once whether D is a diameter or a circumference: D=2π·a_phys is the circumference of a circle of radius a_phys.
- Replace every "D=ℓ_rot" with "ℓ_rot≈D (CANON-REF cross-check, DRV-ROT regime)".
- Either formally promote ℓ_rot via §3.4.4 or remove it from the mandatory chain.
- Declare the regime (DRV-NONE or DRV-ROT) of ν_p=3π⁴ and of δ explicitly.
- Add a G-SYM lint to tools/gate.py that fails when "D_anch" appears next to "diameter".

### 5. [major] §3.4's 'jamming route reproduces D to 0.04%' is best-of-N post-selection (the median is off by +2.2%), which §3.4.3.2 itself forbids; the retracted 'three independent roads' tag is still there

- **category:** grading-honesty
- **location:** 03 §3.4 header tag, anchor block, 'Honest precision of D', §3.4.3.2. Cross-refs: 11 §11.6; sp S3; vh v0.4.1; 10 §10.9

**Quote.** "One quantum diameter, three independent roads, one stated width." | "It is not determined three independent times" | "the jamming simulation independently reproduces the length to 0.04% (4.8542pm — a selected length with a 7% distribution, scale-anchored to A_geo=cΔ t/a at 0.16%; §11.6)" | "Honest precision of D. The anchor and its corroborating routes span 4.8523–4.8542pm, so D is pinned to only 0.04%" | "Post-selection / post-correction: selecting among multiple candidate ℓ_rot values the one that favors a conclusion" | ch11: "median 4.96 pm with a best-matched avalanche at 4.8542 pm (target 4.85)" | vh: "removes the apparent circularity of listing the defining identity D=2λ_(C,e) as an “independent” route." | ch10: "D is independently triangulated (§3.4: 2λ_(C,e)=6π⁶rₚ=2πλ/A)"

**Evidence.** Computed:
1. The median circulation length is 4.96 pm vs D=2λ_C,e=4.852620 pm, i.e. +2.21%. The 0.04% figure comes from picking the avalanche closest to the known target 4.85 pm. That is exactly the post-selection §3.4.3.2 calls "immediate FAIL".
2. The target is not independent. A_target=2πλ/D=2π·632.99 nm/4.852620 pm=8.196×10⁵ is back-computed from D. The corpus's own A values give quite different D=2πλ/A:
   - A=8.0×10⁵ → 4.971 pm
   - A=8.1×10⁵ → 4.910 pm
   - A=8.20×10⁵ (the "target") → 4.850 pm
   - A=880918.977… (shown in §11, equal to A_geo=cΔt/a) → 4.515 pm (−7.0%)
3. The "proton route" 4.8523 pm is 6π⁶×0.8412 fm, where 0.8412 fm is the locked, rounded value of (2/π)λ_C,p. Unrounded it equals 2λ_C,e·(6π⁵/μ)=4.85253 pm (−18.8 ppm): algebraically the anchor itself, not a separate route.

So the "0.04% spread" is rounding plus post-selection, not the precision of D. Since D:=2λ_C,e, D is known to CODATA's m_e precision (about 3×10⁻¹⁰).

The cited scripts (jamming_rotation_485pm_study.py, ellrot_verify.py) are not in the repository.

**Proposed improvement.** - Rewrite the corroboration sentence as: "the jamming circulation-length distribution has median 4.96 pm (+2.2% vs D) and ~7% width; order-of-magnitude corroboration only".
- Report the median with a bootstrap CI, plus the look-elsewhere-corrected probability that an avalanche lands within ±0.04% of the target by chance.
- Delete the "[F] multipath … three independent roads" tag and state D's precision as CODATA's.
- Present the proton route as the identity it is.
- Fix "independently triangulated" in ch10 §10.9.
- Deposit the scripts with their seeds.

### 6. [major] The 'hypersensitive' light-angle prediction is mathematically false: χ stays within [89.78°, 90°) for any D, so a 0.03% change in D cannot move it by more than 1°

- **category:** math-error
- **location:** 03 §3.4 anchor block ("(ii) The anchor forces a falsifiable prediction"). Cross-ref: 10 §10.9 lightangle_master

**Quote.** "through §10.9 the value of D fixes the visible-light propagation angle χ hypersensitively (0.03% in D ⇒ >1^(∘) in χ). A fitted constant cannot generate a narrow-sense optical prediction of this kind; this is the framework's answer to objection B1." | "both channels remain near-transverse (χ≈ 89.8–89.9^(∘), a D-limited distribution)" | ch10: "a 0.03% change in D shifts the visible-light angle by more than a degree. A direct measurement of the transverse angle of visible light against a lattice/anisotropy axis would therefore pin D to 0.001%"

**Evidence.** Using the book's formula sinχ=λ/(mD) with m=⌈λ/D⌉: for λ=632.99 nm, λ/D≈130444. Then 1−sinχ=f/m with f=m−λ/D in [0,1), so χ always lies in [arcsin(1−1/(m+1)), 90°) = [89.776°, 90°), whatever D is.

Computed values:
- D=4.852620 pm → χ=89.943°
- D=4.8523 pm → 89.848°
- D=4.8541 pm (+0.03%) → 89.819°
- D=4.8542 pm → 89.838°
- D=4.96 pm (+2.2%) → 89.950°

Scanning D over ±0.04% gives χ between 89.776° and 89.998°. The largest possible shift is 0.22°, not more than 1°.

χ depends only on the fractional part f. Just fixing f requires knowing D to 1/m=7.7×10⁻⁶. Any D′ whose λ/D′ differs by an integer lands in the same band (aliasing). So a measurement of χ can neither "pin D to 0.001%" nor distinguish candidate D values.

The "lattice axis" is also undefined operationally: vacuum isotropy is bounded at about Δc/c~10⁻¹⁸ by modern Michelson–Morley tests (e.g. Nagel et al. 2015).

**Proposed improvement.** Remove "(0.03% in D ⇒ >1° in χ)" and the claim that this answers objection B1. Either withdraw the χ prediction or restate it correctly: "for 633 nm, 0<90°−χ≤0.224°, independent of D at the 10⁻⁵ level". Grade it [O] until an observable lattice axis and a measurement protocol are defined.

### 7. [major] χ_ST and Point-J measure connectivity, not rigidity: the switch fires at mean contact number z̄≈1.5, four times below the isostatic z=6 used elsewhere

- **category:** physics-validity
- **location:** 03 §3.2.3.1–3.2.3.3, §3.2.5; 04 §4.3.2(E), §4.3.4.3. Cross-refs: 10 (R-c1); sp S2.2

**Quote.** "Spanning alone (χ_span=1) does not define “stiffness.”" | "The “stiff/non-stiff” used here is not grounded on external continuum notions such as elastic moduli." | "we define the location of Point-J as the smallest u at which χ_ST transitions from 0 to 1." | "This section fixes only the definition and does not force a particular value (e.g., κ_ST=2) as an axiom." | ch10: "(R-c1) Rigid regime: χ_c=χ_ST=1." | SP: "giving the isostatic thresholdz=2d=6"

**Evidence.** A min-cut ≥ κ_ST condition tests how well the graph is connected. Rigidity needs constraint counting instead (Maxwell–Calladine: z≥2d for frictionless spheres), or a rigidity-matrix rank or pebble-game test.

I implemented χ_ST exactly as defined (spanning plus edge min-cut ≥ κ_ST=2 between opposite faces) on a bond-diluted simple-cubic contact network, L=10, 20 samples per point, seed 19:

| z̄ | P(χ_ST=1) |
|---|---|
| 1.28 | 0.00 |
| 1.41 | 0.10 |
| 1.51 | 0.60 |
| 1.90 | 1.00 |

At the switch, Maxwell counting leaves at least 1−z̄/6≈75% floppy modes.

κ_min grows like L²: at p=0.5 it is about 10, 28 and 56 for L=6, 10 and 14. So any fixed integer κ_ST is trivially met by any spanning cluster in a macroscopic domain, and u_J falls onto the connectivity-percolation threshold (simple-cubic bond p_c=0.2488, i.e. z̄≈1.5).

A trivial counterexample: two disjoint straight chains from V⁻ to V⁺ give χ_ST=1 at κ_ST=2 while about 2/3 of their degrees of freedom are floppy.

ch10 uses χ_ST as the rigidity/propagation switch, while SP uses z=2d=6, so the corpus has two incompatible definitions of "jammed". Also, §3.2.3.2 says κ_ST is not fixed, but the §4.3.4.3 bins (KAPPA-0/1 ⇒ backbone forbidden) effectively fix κ_ST=2.

**Proposed improvement.** Redefine χ_ST as a rigidity test: a Maxwell–Calladine count including self-stress states, a 3D rigidity-matrix rank or pebble game on the contact network, or a positive relaxed shear modulus from the dynamical matrix. If a cut criterion is kept, normalize it (κ_min/L^(d−1)). Then show the redefined Point-J coincides with SP's z_iso=6, re-run the ch10 switch, and deposit the check script.

### 8. [major] The pressure definition is degenerate (P is either 0 or ∞) and, under A1+A2, never defined — so it cannot supply the finite B that c²=B/ρ needs

- **category:** math-error
- **location:** 04 §4.1.2 table, §4.1.3.1–4.1.3.4

**Quote.** "| pressure | P | scalar | [E L⁻³], U_lat/a³ | boundary compression protocol → minimal relaxation cost W(ε) → P:=lim_(ε→0^+)W(ε)/Δ V(ε)" | "Cost unit per one local update: lock as U_lat (energy unit)." | "Cost coefficient: lock a weight ω_upd per local-update type in analysis_lock (the default value may be locked as 1)." | "where Ω_i^(ε,rel) must be an admissible configuration that satisfies non-penetration, full packing, and the local rules." | "If relaxation fails and cannot return to an admissible configuration, then W(ε) is undefined and is recorded as a failure mode."

**Evidence.** W(ε)=U_lat·min Σω_upd only takes values in {0}∪[U_lat·ω_min, ∞); with the default ω=1, W is an integer multiple of U_lat. So W(ε)/(A_□ε) is either 0 for all small ε (P=0) or at least U_lat·ω_min/(A_□ε), which goes to ∞ (P=∞). A finite nonzero limit is impossible.

Worse, A1 fixes each VP's volume and A2 makes Σ_i|Ω_i|=|𝒟_□|. After compression, |𝒟_□(ε)|=|𝒟_□|−A_□ε is smaller than Σ_i|Ω_i|, so no admissible configuration of the same VPs exists. FM-NODEF fires for every ε>0 unless VPs leave the domain — which would be an open boundary, not a compression.

So B=−V·dP/dV cannot be built inside the framework's own L0–L3 machinery. The finite B of the spine comes from a harmonic potential that lies outside this definition.

**Proposed improvement.** Define pressure mechanically, consistent with the substrate actually simulated: the virial P=(1/3V)Σ r_ij·f_ij with a declared contact law, or P=−∂E/∂V; for hard particles, use the collision (kinetic) pressure. If a cost-based definition is kept, make the cost continuous in ε (e.g. a displacement cost) and state how VPs exit through an open face. Derive B from this P and link it explicitly to S2.

### 9. [major] Charge Q=q₀·sgn(V·n_Q) depends on the frame, can only be −1, 0 or +1, is not additive, and has no conservation law

- **category:** physics-validity
- **location:** 04 §4.1.2 table, §4.1.6.1–4.1.6.4

**Quote.** "Charge is defined as “the sign of the residual directionality left by the shell structure”." | "Lock the sign-determination axis (charge axis) n_Q by" | "n_Q must not be chosen after seeing the result; the selection rule must be locked in analysis_lock." | "| charge | Q | signed scalar | [Q] (independent dimension), unit q₀ | shell(7) cancellation convention → survival vector V → sign indicator q:=sgn(V·n_Q) → Q:=q₀ q"

**Evidence.** q=sgn(V·n_Q) with n_Q in {x̂, ŷ, ẑ} is not invariant under rotations. For V=(0.3, −0.5, 0.8), q is +1 for n_Q=x̂, −1 for ŷ and +1 for ẑ. Rotating the object 180° about ẑ flips q for n_Q=x̂.

Physical charge is:
- invariant under rotations and boosts;
- additive (nuclei carry Ze with Z up to 118; quarks carry ±1/3 e and ±2/3 e);
- exactly conserved.

This definition can only output −q₀, 0 or +q₀, has no rule for composites, and nothing in the [A-3] local updates conserves it. Locking n_Q in advance prevents tuning but does not remove the frame dependence.

**Proposed improvement.** Define charge through a quantity that is rotation-invariant and additive, e.g. a chirality pseudoscalar of the shell (sign of s_a·(s_b×s_c)) or an integer topological winding number. Prove it is invariant under SO(3) and conserved under admissible local updates, and test additivity: two proton cores → +2, proton plus electron → 0. Grade the charge map [O] until this is done.

### 10. [major] Grade inflation on the chapter and its header cards: axioms, conventions and empirical anchors are labelled [F] forced

- **category:** grading-honesty
- **location:** 03 page-header grade and the five vp-cards; §3.2/§3.3/§3.4 tags; VP-N1; repro/physics/registry/vp_locks.csv; repro/physics/tools/vp_numeric_ssot.py

**Quote.** "This chapter fixes, for the entire document, the minimal building blocks of the world as primitives. Grade [F] forced." | "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." | "m_p/m_e = 6π⁵ — Proton-electron mass ratio as 2π·ν_p = 6π⁵ (−19 ppm vs measurement). [F] forced." | "[F] multipath anchor identity" | "this document proposes the following minimal operational closure candidates." | SSOT code: ("D=2λ_C,e","(pm)",f(q['D2lamCe']*P,6),"[H] =D_anch")

**Evidence.** - By the chapter's own §3.1.1, axioms are [A] ("not further derived") and definitions are [D] (conventions). Neither is "forced".
- A measured laser wavelength is an anchor ([L]/[H]) by definition, not [F].
- D_anch=2λ_C,e is built from CODATA m_e. The SSOT code grades it [H]; the page and vp_locks.csv grade it [F].
- 6π⁵=1836.118109 vs CODATA 2022 m_p/m_e=1836.152673426(32): −18.8 ppm, which is −1.08×10⁶σ. A formula excluded at 10⁶σ cannot carry an unqualified [F].
- VP-N1 introduces free closure parameters (τ_break, τ_heal, K_soft, K_jam, ξ_th) on a page graded [F].

**Proposed improvement.** - Grade §3.1 [A]/[D] (no F) and §3.2–§3.3 [D].
- Grade §3.4, λ_anchor and D as [L], and sync the "d-anch" and "anchor" rows of vp_locks.csv.
- Grade VP-N1 [H] (closure candidate).
- Split 6π⁵ into "[F] structure given {U1, U3, S1, S2}" and "[O] −18.8 ppm residual (≈10⁶σ at CODATA precision), obstacle stated".
- Have the gate check that page, card, registry and SSOT grades agree.

### 11. [major] m_e is an input presented as an output, and the 'single anchor (DOF=1)' is actually two measured inputs (λ_ref and m_e)

- **category:** circularity
- **location:** 03 §3.4 anchor block; λ_anchor header card. Cross-refs: 13 §13.5; w0 W.2 (mₑ listed as anchor)

**Quote.** "(i) The ratios are π-forced: D/rₚ=π(mₚ/mₑ)=6π⁶, so fixing D fixes rₚ,mₚ,mₑ and the rest with no further input — there is no tunable knob." | "D_anch:=2λ_(C,e)=4.8526pm — the same 632.99 nm / mₑ anchor used everywhere else" | "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework." | w0: "mass-scale anchor | anchor"

**Evidence.** D:=2λ_C,e=2h/(m_e c)=4.852620 pm is computed from CODATA m_e (vp_numeric_ssot.py: ME=9.1093837015e-31 "CODATA"). Then m_e c²=2hc/D returns 0.51099895 MeV — the input, exactly. So "fixing D fixes … mₑ with no further input" is a tautology.

Meanwhile the realization chain (a, U_lat=hc/a, m_H) runs on λ_ref=632.99 nm. These are two independent measured inputs, merged under one name as "632.99 nm / mₑ anchor". The only link between them is A, whose target 2πλ/D=8.196×10⁵ is itself computed from both. The honest count is DOF=2, plus the exact SI constants h and c.

The genuine outputs of D are:
- m_p, via 6π⁵ (−18.8 ppm);
- r_p=D/6π⁶=0.84125 fm. This equals 4ħ/(m_p c) to 19 ppm and is +0.06% (+0.78σ) from CODATA 2022's 0.84075(64) fm. The scorecard still compares against CODATA 2018's 0.8414 fm.

**Proposed improvement.** State the inputs as {λ_ref, m_e} (plus exact h, c), DOF=2. Remove mₑ from the list of things D "fixes", and relabel the λ_anchor card as "one of two empirical anchors". Update the r_p comparison to CODATA 2022 and cite the known r_p≈4ħ/(m_p c) coincidence as prior art.

### 12. [major] VP-N1 makes vacuum stiffness depend on observation time, which predicts dispersion and a low-frequency cutoff — but no bound is derived or tested

- **category:** missing-test-or-prediction
- **location:** 03 VP-N1 (De, eggshell state machine, ξ-closure). Cross-ref: sp S2.2 (SOC avalanches)

**Quote.** "the relevant observable is dynamic stiffness, not static stiffness, and the same configuration can appear “soft” or “hard” depending on observation time / driving rate." | "Therefore, whenever critical scales such as c², g_*, and g^* appear in a conclusion, one must always record the protocol (time window / driving rate / geometry) together; without that record, the result is treated as INCONCLUSIVE." | SP: "overshoot triggers a local unjamming avalanche that relaxes it (self-organised criticality)"

**Evidence.** If B and G depend on De=τ_relax/τ_obs, then c²(ω)=B(ω)/ρ is dispersive. For a Maxwell-viscoelastic medium, transverse waves also stop propagating below ω_c~1/τ_relax.

Both effects are tightly bounded by observation:
- Fermi-LAT GRB 090510 (z=0.903) delivered a 31 GeV photon within ~0.83 s after ~7.3 Gyr of travel, so |Δv/c| ≲ 0.83/(2.3×10¹⁷ s) ≈ 4×10⁻¹⁸ across keV–GeV.
- The photon-mass bound m_γ<1×10⁻¹⁸ eV (PDG) gives ω_c≲1.5×10⁻³ s⁻¹, i.e. τ_relax≳7×10² s.
- GW170817 bounds |c_gw−c|/c ≲ 10⁻¹⁵.

The SOC avalanches of S2.2 imply a finite τ_relax, and VP-N1 even makes c² protocol-dependent, yet none of these constraints is stated.

**Proposed improvement.** Add a "vacuum rheology constraints" subsection. Derive from the ξ-dynamics the implied c(ω) and ω_c, compare them with the GRB time-of-flight, photon-mass and GW170817 bounds, and register "Δc/c > 10⁻¹⁷ between radio and GeV" as a falsifier. Either state that c is protocol-independent (the vacuum is always at De≫1) or quantify the predicted deviation.

### 13. [major] The §4 governance machinery (analysis_lock, regime_id, closure registries, Gate stacks) is not implemented anywhere; by its own rules no headline has conclusion status, and every chapter's 'reproduction code' link is dead

- **category:** reproducibility-code
- **location:** 04 §4.4, §4.8, §4.2.9, §4.3.3–4.3.5; 03 §3.2.1 [LOCK] and page-header link; repro/physics/; w0 W.3.1

**Quote.** "A closure/map without Gates cannot generate a valid conclusion." | "Every conclusion sentence must include regime_id. If regime_id is missing, the sentence is judged INCONCLUSIVE." | "[LOCK] The reporting schema for this definition of φ—protocol / time window / judgement function—is sealed in 04_vp_whitepaper/LOCK/fluidity_phi_lock.json." | w0: "UNLOGGED | gate/reports/gate_report_mp_me.json" | link: "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/physics/03-axioms-primitives-volume-particle-lattice/"

**Evidence.** A search of the repository outside docs/ finds none of the following:
- any analysis_lock, canon_lock or realization_lock file;
- fluidity_phi_lock.json;
- any regime_id, R-BASE-001, CS-BASE-CORE-001 or CL-* closure ID;
- any physics gate_report*.json.

The scorecard lists the Gates for a, Δt, U_lat, m_e, m_p, m_H and m_p/m_e as UNLOGGED.

tools/gate.py checks word, figure and equation counts and numeric display drift. It does not check G-SYM, G-REG or G-NT.

All 47 physics pages link "재현 코드 (GitHub)" to repro/physics/<slug>/ directories that do not exist (47 of 47).

The simulation scripts cited as evidence are absent: jamming_rotation_485pm_study.py, ellrot_verify.py, bulk.py, relaxed_shear.py, lattice_3d_jam_percolation.py, final_verification.py, verify_amplification_A.py.

Under §4.8 and §4.3.5, every headline is therefore INCONCLUSIVE by the framework's own rules.

**Proposed improvement.** Choose one of two routes:
- Implement a minimal version: repro/physics/locks/{canon,analysis,realization}_lock.json, a regimes.yaml containing R-BASE-001, a closures.yaml, and a gate phase that checks every [F]/[V] claim carries a regime_id, closure_ids and a logged Gate report. Deposit the jamming bundle, or a DOI-pinned archive with SHA-256 hashes.
- Or soften §4.8 and §4.3.5 to "target protocol" and show "Gate status: UNLOGGED" on each headline card.

Either way, fix the 47 dead links.

### 14. [major] '1:1 semantic mapping' is not well-defined: every example map in the chapter is many-to-one

- **category:** internal-inconsistency
- **location:** 04 'Global principles for 1:1 semantic mapping', §4.1.1, §4.1.2 table, §4.4 template, §4.1.4–4.1.6

**Quote.** "1:1 correspondence: an item in one layer connects to an item in another layer only via 1:1 correspondence. If a 1:N or N:1 relation is needed, it must be decomposed into a new intermediate object and/or a new explicit conversion rule." | "Each quantity is defined only by a 1:1 mapping L1→L2→L3" | "definition: (aggregation rule: mean/median/min-cut-based, etc.)" | "| deficit | D_def | scalar | [1] (default), optionally [L⁻³] | contact degree z_i → reference degree z_ref → d_i:=max(0,z_ref-z_i) → D_def:=frac1|V|Σ_i d_i"

**Evidence.** - The deficit map sends {z_i}, a vector of |V| integers, to one number. With z_ref=6, z=(6,4), (4,6) and (5,5) all give 𝒟_def=1.
- The charge map sends 7 vectors (21 real numbers) to q in {−1, 0, +1}.
- The flux map sums any number of events into ΔN_Σ.
- The throat template's "mean/median/min-cut" rule is an aggregation.

None of these is injective, so "1:1" cannot mean a bijection. Taken literally, the N:1 "decomposition" rule would forbid the chapter's own definitions. What is actually meant is "one registered map_id from one from-item to one to-item" — a registry convention, not a mathematical property.

**Proposed improvement.** Replace "1:1 correspondence" with "registered single-valued map": a function f: X_from→X_to with a unique map_id. Many-to-one aggregation is allowed but must declare what information is discarded (its fibres or sufficient statistic) and its invariances, e.g. rotation invariance for charge. Drop the "1:N/N:1 must be decomposed" clause or make it precise.

### 15. [major] The '1 symbol – 1 meaning – 1 unit' rule is broken for a, φ, 𝒟, ℰ and r₀, including a 1.2×10⁶ clash between two 'lattice lengths' and a 6/π error in the flux token volume

- **category:** internal-inconsistency
- **location:** 04 global principles, §4.1.1, §4.1.4.3; 03 §3.2.1, §3.3 tag, §3.3.3. Cross-refs: 12 §12.1; sp S3; 13 §13.5; tools/vp_numeric_ssot.py

**Quote.** "1 symbol–1 meaning–1 unit: the same symbol has exactly one meaning (object attribution + geometric meaning + admissible operation scope) and exactly one unit dimension across the entire document." | "The token size is locked as the VP unit volume a³." | "[F] geometry conventionsin: VP diameter $a$" | ch12: "$κ_vp=π/6$ / out: $φ_jam=(π/6)N_vp(a/D)³$" | SP: "so the lattice resolution isa_{phys}=λ/A" | SSOT: A_VP   = D("6.3299121257859865746e-19"),   # a, VP 지름 | "r₀ is half of the edge length of the canonical Anchor Cell; it does not automatically carry the geometric meaning of a radius."

**Evidence.** 1. If a is the VP diameter (§3.3 tag; ch12 uses v_vp=(π/6)a³), the VP volume is (π/6)a³=0.5236a³. So J=a³·ΔN/(A_Σ·ΔT) overcounts volume flux by 6/π=1.910.
2. "a" is the VP diameter a=6.33×10⁻¹⁹ m in the SSOT and realization, while SP calls a_phys=λ/A=632.99 nm/8.196×10⁵=7.72×10⁻¹³ m "the lattice resolution". The two differ by a factor of 1.22×10⁶: D_anch/a=7.67×10⁶, but D/a_phys=2π.
3. φ is the fluidity index φ(P;W) in §3.2.1, but φ_jam is the packing fraction (vp_locks.csv).
4. 𝒟 is both the domain and the deficit indicator 𝒟_def. ℰ is both the contact edge set (ℰ_c, E_B) and the event set (ℰ_0 in ch09; "event set E" in §4.1.1). J/𝔍 and B/𝓑 also double up (flux vs jamming lattice; bulk modulus vs backbone).
5. r₀ is "not a radius" here, but ch13 sets it equal to λ_C,e (m_e=hc_ref/r₀).

**Proposed improvement.** Run an automated symbol-table lint across all chapters. Specific fixes:
- Use v_vp=κ_vp·a³ with κ_vp=π/6 in the flux definition.
- Rename fluidity φ→f_unjam, deficit 𝒟_def→Δ_def, and the event set →𝔈.
- Distinguish a_VP (6.33×10⁻¹⁹ m) from a_phys (λ/A), and explain physically why the "lattice resolution" is 10⁶ VP diameters.
- Write λ_C,e instead of r₀ in §13.

### 16. [major] Three incompatible values for the substrate packing fraction: A2 (φ=1), the physics volume's φ_jam=0.633, and the corpus guide's 'random close packing φ≈0.7405' (which is FCC/HCP, not RCP)

- **category:** cross-volume
- **location:** 03 [A-2], [D-5]; repro/physics/registry/vp_locks.csv; AGENTS.md §1 TL;DR and §6 row 4; docs/chemistry/_decl.json

**Quote.** "Inside the domain D, space is fully occupied by VPs ([D-5])." | vp_locks.csv: "phi-jam,φ_jam,0.633,Isostatic jamming/packing fraction (z to 6); distinct from 2/π = 0.6366.,V" | AGENTS.md: "Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405)." | chemistry _decl.json: "\"phi_RCP=0.7405\","

**Evidence.** π/(3√2)=0.74048 is the Kepler maximum for crystalline FCC/HCP packing. Random close packing, i.e. jamming of monodisperse frictionless spheres, is about 0.64 (φ_J≈0.639), consistent with the physics volume's own 0.633 and ch18's "φ_jam≈0.64".

The chemistry body itself correctly says "FCC/HCP π/(3√2)=0.7405". But its declaration file and the corpus reading guide label that number φ_RCP and assign it to the vacuum, while the axioms say φ=1. A reader who follows AGENTS.md ("read physics first") meets three different values for the one defining number of the substrate.

**Proposed improvement.** Use one substrate number in all volumes: in physics, φ_J≈0.633–0.64 (after resolving the A2 conflict). Relabel chemistry's 0.7405 as φ_FCC (crystal packing of atoms, not the vacuum), fix AGENTS.md §1/§6 and chemistry/_decl.json, and regenerate the aggregates from the manifest.

### 17. [minor] Dimension errors: 'mₑ=2hc/D' and 'mass = energy ÷ dimensionless' are energies, and ν_p=3π⁴ is given units of s⁻¹

- **category:** unit-dimension
- **location:** 03 §3.4 'Honest precision of D'; 04 §4.1.3.2 and the 1-symbol-1-unit principle. Cross-refs: 13 [A-13.6-1] and the boxed m_e equation; 09 §9.4 SSOT note

**Quote.** "Consequently every D-anchored output inherits this 0.04%: mₑ=2hc/D" | "Cost unit per one local update: lock as U_lat (energy unit)." | "Fix the mass scale of an object O as “lattice unit energy” divided by a “dimensionless resistance (effective cross-section coefficient).”" | "ν_p,can=3π⁴≈ 292.227s⁻¹"

**Evidence.** [hc/D] = J·m/m = J. 2hc/D=8.187×10⁻¹⁴ J=0.511 MeV, which is m_e c²; the mass is m_e=2h/(cD)=9.109×10⁻³¹ kg. Likewise U_lat divided by a dimensionless σ_eff is an energy. 3π⁴ is a pure number, so "s⁻¹" presupposes a tick unit that is never stated.

This is numerically harmless once c² (or the tick) is inserted, but these are exactly the "unit jumps" that §4 declares prohibited.

**Proposed improvement.** Write m_e c²=2hc/D (or m_e=2h/(cD)). Restate [A-13.x] as m(O)c²=U_lat/σ_eff, or declare natural units c=1 once, globally. Give ν_p,can as "events per canonical tick" or state the time unit.

### 18. [minor] Structure: sections are out of order, axioms and closure rules are stated twice with different content, and the 'Forced' part heading dangles at the end of §4

- **category:** structure-redundancy
- **location:** 03 (order: VP-A block, Stone, Cell, 3.5, then 3.1–3.4); 04 (order: 4.4–4.8, then 4.1–4.3; 4.5 vs 4.2.1; 4.6 vs 4.2.7; two L0–L3 lists); end of 04

**Quote.** "Each axiom has a distinct meaning; redundant statements across axioms are forbidden." | "3.5 Coupling the VP axioms with the cell definition: what is prior and what is derived?" | "The global principles fixed in this chapter—“1:1 semantic mapping”, “closure DAG”, “failure modes”, and “Gate required”—are not re-explained in later chapters." | "Forced — Results With No Adjustable Content" | "Everything here follows from geometry, counting, and the rectification integrals of the Read-First decoder. There is no knob"

**Evidence.** - §3.5 comes before §3.1, and §4.4–§4.8 come before §4.1–§4.3.
- The axioms appear twice (VP-A1..A4 plus VP-N1, then [A-1]..[A-3]) with different membership, contradicting the chapter's own ban on redundant axiom statements.
- The closure "five duties" appear in §4.5 and again in §4.2.1; the DAG rules in §4.6 and again in §4.2.7.
- L0–L3 are defined twice with different contents (L0 contains "cell, event" in one list and "local update (event)" in the other).
- The <h2 class="part"> heading "Forced — Results With No Adjustable Content … There is no knob" sits at the bottom of §4, whose content is roughly 40 locked choices (κ_ST, z_ref, n_Q, ξ_th, τ_break, τ_heal, s₁, s₂, …). It reads as §4's verdict.

**Proposed improvement.** Renumber and reorder both chapters. Keep one axiom block and one closure/DAG block, merge the two L0–L3 lists, and move the part heading to the top of the §SP page.

### 19. [minor] Small inconsistencies in the §4 taxonomies (FM-STR, G-NT, FM-NUMERIC, κ_ST, the χ_open flux cap, the single-valued R_cell axis)

- **category:** internal-inconsistency
- **location:** 04 §4.7, §4.4, §4.2.6, §4.1.5.4, §4.1.6.4, §4.3.2(B), §4.3.4.3; 03 §3.2.3.2, VP-N1 flux cap

**Quote.** "FM-STR: the shell-vector generation convention or the cancellation convention is not locked (structure is unspecified)." | "Mandatory base Gates: every closure requires at least G-SYM, G-LOCK, G-REG, and G-NT." | "FM-NUMERIC: the contact-graph construction convention is not locked, so z_i is not reproducible." | "This section fixes only the definition and does not force a particular value (e.g., κ_ST=2) as an axiom." | "Whether a nonzero flux can exist in the regime χ_(rm open)=0 is judged separately by the protocol definition." | "In the canonical regime, only CELL-CUBE is allowed."

**Evidence.** - FM-STR is used for charge but is missing from the "pre-registered" taxonomy in §4.7 (FM-SYM, SCOPE, NONUNIQUE, NODEF, NUMERIC, XCROSS, REP, NT).
- The §4.4 map template's required_gates omit G-NT, although §4.2.6 makes it mandatory.
- FM-NUMERIC ("numerical instability") is used for "convention not locked", which is FM-SYM or FM-NODEF.
- κ_ST is declared unfixed in §3.2.3.2, but §4.3.4.3 hard-wires KAPPA-0/1 ⇒ backbone forbidden, i.e. κ_ST=2.
- The cap |J|≤c_ref·χ_open forces J=0 whenever χ_open=0, so it cannot be "judged separately".
- R_cell has only one allowed value, so it is not really an axis.

**Proposed improvement.** - Add FM-STR to §4.7, or map it to FM-NODEF.
- Add G-NT to the template.
- Relabel the misused FM-NUMERIC items.
- State κ_ST=2 explicitly in analysis_lock, or decouple R_κ from κ_ST.
- Rewrite the cap as |J|≤c_ref when open, and "J=0 or a protocol-defined leak rate" when closed.
- Drop R_cell as an axis or give it a second allowed value.

### 20. [minor] The α card mis-describes 2/π: the full-wave to half-wave mean ratio is 2, not 2/π, and this contradicts the δ card

- **category:** math-error
- **location:** 03 header vp-card "alpha"; repro/physics/registry/vp_locks.csv row "alpha"; axd glossary

**Quote.** "α = 2/π — Geometric rectification ratio (full-wave to half-wave mean); the single rectification anchor." | "δ = 1/π² — Double-rectification survival constant (product of two half-wave means; a max-entropy measure)."

**Evidence.** The full-wave rectified mean is ⟨|sinθ|⟩=2/π and the half-wave mean is ⟨max(sinθ,0)⟩=1/π, so their ratio is 2. The δ card uses a half-wave mean of 1/π (1/π·1/π=1/π²), so reading the α card as a ratio gives 2, not 2/π. §5 defines α=⟨|cosθ|⟩, which is the full-wave mean itself.

**Proposed improvement.** Change the card to: "α=2/π=⟨|cosθ|⟩, the full-wave-rectified mean relative to the peak (twice the half-wave mean 1/π)", then regenerate the card and the registry row.

**Strengths noted:**
- The anti-tuning discipline is unusually explicit: the contact predicate, κ_ST, thresholds, visualization mode and boundary sets must all be pre-registered, and a new lock_id is the only legal way to change them. This is a real defence against the garden of forking paths.
- The cube/sphere visualization mappings are mathematically correct (r_vis=(3/4π)^(1/3)·D_anch, inverse (4π/3)^(1/3)·r_vis), and forbidding mixed modes is good practice.
- Separating 'spanning' from 'robust spanning', and counting fragile spanning as non-stiff, is a sensible structural idea; it only needs a rigidity criterion in place of a connectivity one.
- The Deborah-number framing of dynamic rigidity (De=τ_relax/τ_obs) and the explicit split between trigger and time-scale in the ξ-closure are standard, testable rheology.
- The closure DAG, with its named forbidden cycle patterns, and the failure-mode taxonomy are thoughtful and could become genuinely useful once implemented in code.
- §3.4 already concedes that D is a single anchor and that the jamming length is 'a selected length with a 7% distribution'. The v0.4.1 log records that reclassification openly, and the SSOT script's residual map (R1–R8) is honest bookkeeping.
- The proton-radius cross-check arithmetic is correct: D/6π⁶=0.84125 fm lies within 0.8σ of CODATA 2022 (0.84075(64) fm).


## review:rectification-core-120

### 1. [critical] §6.3 'derives' R_p from a λ_C that was computed backwards from R_p, so the round trip proves nothing; the measured Compton wavelength gives a cleaner, non-circular result

- **category:** circularity
- **location:** 06-continuum-core-model-deriving-rp §6.3.3–§6.3.4 (eqs S06_03_lC_value_lock, S06_03_Rp_value, S06_03_lC_from_Rp); §6.1.3 [D-6.1-3]/[D-6.1-4]; repro/physics/verification_dossier/PHASE1-2_AUDIT_FINDINGS.md:43; repro/physics/tools/vp_numeric_ssot.py (RP_LCK, MEAS RP_CODATA)

**Quote.** §6.3.3: "In this section, assume that the following value is locked by canon_lock: ... \lambda_C = 1.3213538700998668\ \mathrm{fm}." §6.3.4: "which matches (S06_03_lC_value_lock). Therefore the locks Rₚ/L_q=α and L_q=λ_C are numerically consistent within the same version". §6.1.3: "This section uses only (i) the existence of ψ as an internal variable of the continuum core model and (ii) the fact that “cycle completion” is locked at 2π." Dossier: "| λ_C,p | (π/2)r_p | 1.321354 fm | PASS |"

**Evidence.** python: (π/2)×0.8412 = 1.3213538700998668. That matches every digit of the 'locked' λ_C, so the value is the target radius 0.8412 fm multiplied by π/2. It is not the proton Compton wavelength. CODATA 2022 gives h/(m_p c) = 1.32140985360 fm, and the locked value is −42.4 ppm off it, about 10^5 times the CODATA relative uncertainty (3e-10). §6.1 defines λ_C only as the first root of ψ(R)=2π for a ψ that is never specified, so the chapter itself gives λ_C no numerical content. The number comes in through 'assume ... locked', and the dossier records its origin as (π/2)r_p. §6.3.3→§6.3.4 is therefore R_p → λ_C → R_p, and the 'consistency' check is an identity. The non-circular version is stronger: (2/π)·h/(m_p c) = 4ħ/(m_p c) = 0.841236 fm. Against CODATA 2022 r_p = 0.84075(64) fm that is +0.00049 fm = +0.76σ; against muonic H (2013) 0.84087(39) fm it is +0.94σ. The repo baseline 'RP_CODATA=0.8414' is CODATA 2018 and is out of date.

**Proposed improvement.** (1) In §6.3.3, use λ_C,p = h/(m_p c) = 1.32140985360 fm (CODATA 2022) and say plainly that this brings in the measured m_p. The alternative, m_p = 6π⁵ m_e, carries the −18.8 ppm residual; the tool already notes R2 = −R1. (2) Delete the §6.3.4 back-calculation, or relabel it 'identity, not a check'. (3) Declare the seam 'internal phase-completion length ≡ proton Compton wavelength' as an explicit [H] identification in §6.1. (4) Report R_p = 4ħ/(m_p c) = 0.841236 fm against CODATA 2022 0.84075(64) fm (+0.76σ) and update the MEAS baseline in vp_numeric_ssot.py.

### 2. [critical] R_p/L_q = 2/π is fixed by where the author puts the 1/α factor, not by any balance; graded [F] (and the 'attractor' [V]) although it is a definition

- **category:** grading-honesty
- **location:** 06 §6.2.3–§6.2.5 (S06_02_Pi4_def, S06_02_Pi5_def, balance); 06 overview 'Where the two aggregate cost functions are defined'; 06 §6.1.4 (G4); sp-jamming-spine S4; repro/physics/verification_dossier/GROUNDING_LEDGER.md (r_p row)

**Quote.** "\Pi_{4}(R) := \Pi_\star\, \frac{1}{\alpha}\, f_A(R)\, f_\Omega(R)"; "Unlike the collapse term, the rigidity term does not include 1/α."; "the exponents R⁻⁴ and R⁻⁵ are derived and locked internally from domain/boundary/counting conventions"; "[F] balance ... Two pressures cross once; the crossing is the proton radius."; G4: "Therefore the only canonical choice that removes redundancy in the core selection length is η=1, i.e., L_q=λ_C."; sp: "obeys ̇x=α x^{-5}-x^{-4}" ... "the proton radius is dynamically selected, not a fine-tuned balance"

**Evidence.** Write Π4 = Π*·A·L⁴/(16π²R⁴) and Π5 = Π*·B·L⁵/(16π²R⁵). Setting them equal gives R/L = B/A exactly. Π*, 16π² and the dilution factors all cancel, so the ratio is whatever B/A the author inserts. The chapter sets A = 1/α, B = 1. Other choices are just as 'rectification-motivated'. The rigidity term is also a radial transfer, so rectifying both or neither gives R = λ_C = 1.3214 fm. Putting 1/α on Π5 gives 2.0757 fm, and α² gives 0.5355 fm. Taking L_q = ħ/(m_p c), i.e. η = 2π, adds no constant beyond π, which contradicts G4's uniqueness claim, and gives 0.1339 fm. The two 'dilutions' are also one factor counted twice: f_A = L²/(4πR²) and f_Ω = (1/4π)(L/R)² = L²/(4πR²) are identical, so the −4 exponent is chosen, not derived. The sp 'global attractor' ẋ = αx⁻⁵ − x⁻⁴ has x* = α by construction. F'(x*) = −α⁻⁵ is algebra, and any 1-D flow with one positive root converges to it, so the ledger's '[V]+[F] ... simulation confirms fixed point 2/π' confirms nothing independent. Look-elsewhere: the family (p/q)π^k·ħ/(m_p c) with p,q ≤ 8 coprime and |k| ≤ 2 has 37 members in [0.5,1.5] fm. For a random target in [0.6,1.1] fm, some member lies within 0.76σ (CODATA 2022) 3.5% of the time. The match is mildly notable (p ≈ 0.035), not forced.

**Proposed improvement.** Regrade §6.2 as [D] (construction) plus [H] (the identification with the proton radius), and state the hypothesis compactly as r_p = 4ħ/(m_p c). Report the look-elsewhere number above. Make B/A an output rather than an insertion: measure the inflow (r⁻⁴) and stiffness (r⁻⁵) prefactors in the substrate MD at an Ω fixed independently, not 'inflow coefficient unity'. Relabel the attractor as a [D] consistency property. Remove f_Ω, or justify it as physically distinct from f_A. Pre-register 0.84124 fm against upcoming r_p determinations.

### 3. [critical] Product-measure assumption behind δⁿ (and ν_n = nπ^{2(n−1)}) conflicts with the chapter's own 120° sum-zero lock: the survival product is identically 0 or about 2× larger

- **category:** internal-inconsistency
- **location:** 05 §5.2.4 [A-5.2-U0], §5.2.6.2 (Trigger T2), §5.0 decoder row 'Generalised n-rectification'; 07 'Topological necessity of 3 sectors' and '120° condition' (S07_n_sum_zero); cross-ref 08 §8.0.5(II), §8.0.6(A)

**Quote.** 05: "The derivation in this section uses the assumption that the canonical measure on (θ,φ) factorizes as a product measure." / "If the assumption fails, the universal value of δ is not claimed; the case is handled as a falsification trigger (5.2.6)." 07: "Also lock their sum to be zero (center cancellation):" / "the 3-sector (120°) structure is not a choice but a geometric consequence of “minimality + sum-zero closure.”" 08: "the C₃ ring-closure Σ_in_i=0 (§8.0.3) fixes the global phase as a gauge choice and removes no rectification. Under the §5.2 product measure ([A-5.2-U0]) the joint survival is the product"

**Evidence.** The ν_3 = 3π⁴ route needs the three sectors' directional half-wave factors to be independent uniform phases, giving ⟨Π[cosθ_i]+⟩ = (1/π)³. Two cases were checked. (a) The sector directions are locked at 120°, θ_i = θ + 2πi/3 (§7). Then cosθ_1 + cosθ_2 + cosθ_3 = 0, so the three cannot all be positive, and the product is identically 0 for every θ (numerical average = 0.0). (b) §8.0.5 reads the directional phase as an inter-sector relative phase, and relative phases around a closed ring satisfy θ_3 = −(θ_1+θ_2). Grid integration then gives ⟨Π[cosθ_i]+⟩ = 0.06587 = 2.04/π³, not 1/π³ = 0.03225. Either way [A-5.2-U0] fails under the framework's own geometry, and §5.2.4 says δ's universal value is then 'not claimed'. In case (b) the pairwise trigger T2 (C_uv) cannot catch the failure, because θ_1 and θ_3 are pairwise independent while the triple is not. Also, §8.0.5 counts only n−1 independent inter-sector locks yet assigns n independent phase pairs in ⟨W_n⟩ = δⁿ.

**Proposed improvement.** State explicitly how the per-sector phases (θ_i, φ_i) relate to the locked axes n_i. If they are the axis directions, retract δⁿ for C₃ objects. If they are relative phases, compute the constrained joint average (≈2.04/π³ for the directional part) and redo ν_3. Extend T2 to a joint-independence test (e.g. compare the empirical ⟨Π u_i⟩ with Π⟨u_i⟩) so n>2 dependence is detectable. Until then, regrade ν_n = nπ^{2(n−1)} from [F] to [H].

### 4. [major] R_p is defined as a sharp core-boundary radius but compared with the measured rms charge radius; the model's own rms is 16–22% smaller

- **category:** physics-validity
- **location:** 06 'Definition of the core region and the core boundary', §6.2.5, §6.4.3 [C-82/7-01]; sp-jamming-spine S4; w0-result-scorecard line 106

**Quote.** 06: "Define the core radius Rₚ as a transition point of χ_core(R)." / "R_{82} := \mathrm{Agg}\Bigl(\{\|\mathbf{x}_i-\mathbf{x}_c\|\}_{i\in\mathcal{B}_{82}}\Bigr) \equiv R_p"; sp: "Hencer_p=(2/π)λ_{C,p}=0.8412fm (CODATA charge radius0.8414fm,-0.02%)"

**Evidence.** CODATA/muonic r_p is the rms charge radius √⟨r²⟩, taken from the slope of the Sachs form factor G_E(Q²). The chapter's R_p is a boundary (transition) radius, and chapter 6 never uses the words 'rms' or 'charge radius'. For a uniform sphere of boundary R, rms = √(3/5)R = 0.7746R, which gives 0.652 fm for R = 0.8412 fm. For the chapter's own discrete core (the 81 sites with R² ≤ 6, boundary at √6): Σr² = 342, ⟨r²⟩ = 4.222, rms = 2.055, so rms/R_boundary = 0.839 and rms = 0.706 fm. Both are 0.13–0.19 fm below 0.84075(64) fm, i.e. >200σ. The 0.76σ agreement holds only if R_p is itself the rms radius, which the definitions contradict.

**Proposed improvement.** Specify the observable. Either (a) redefine R_p as √⟨r²⟩ of a stated charge (or 'rotation') density produced by the model and show it equals (2/π)λ_C, or (b) keep R_p as a boundary radius and derive the model's rms charge radius before comparing with CODATA. Add a gate 'G-RP-OBS' that compares like with like. Mention the magnetic radius (r_M ≈ 0.85 fm) as a second, independent observable the model should also predict.

### 5. [major] α=2/π and δ=1/π² are circle (S¹) averages, but the substrate is 3-D and §6.2 itself normalises directions over 4π sr; the isotropic 3-D values are 1/2 and 1/16

- **category:** physics-validity
- **location:** 05 §5.1.1 [D-5.1-2], §5.1.2, §5.2.2, §5.2.5 (max-entropy argument); 06 §6.2.2 vs §6.2.3.2

**Quote.** 05: "cosθ is a definitional choice as the minimal sign-changing projection function over a full cycle." / "[F] forced integral"; 06 §6.2.2: "Here θ is an angular variable aggregated with the uniform measure over one full cycle [0,2π)"; 06 §6.2.3.2: "Normalize the full directional space by the total solid angle 4π."

**Evidence.** The integrals are correct: on S¹, ⟨|cos|⟩ = 0.636620 = 2/π and ⟨[cos]+⟩ = 0.318310 = 1/π (checked numerically). For an isotropic (maximum-entropy) direction in 3-D, the measure is uniform on S² (μ = cosθ uniform on [−1,1]). There ⟨|cosθ|⟩ = 1/2, ⟨[cosθ]+⟩ = 1/4, and δ_3D = 1/16 = 0.0625, which is 0.617×(1/π²). §6.2 uses the 3-D sphere for dilution (4π sr, A = 4πR²) and the 2-D circle for rectification in the same derivation. With α_3D = 1/2 the same balance gives R_p = 0.5·1.3214 = 0.661 fm (−21%). §5.2.5's maximum-entropy argument fixes 'uniform' only once a base manifold is chosen, and choosing S¹ is exactly the step not argued. The [F] label therefore applies to the integral, not to its physical use.

**Proposed improvement.** Split the grade: the integral ⟨|cos|⟩_{S¹} = 2/π is [F]; the claims that 'this physical projection lives on S¹, uses cos, and uses |·| (or [·]+)' are [D] choices, to be listed in the provenance table. Give a physical reason for S¹, e.g. the phase is a rotation angle about a fixed axis, and then make §6.2's dilution consistent with it (2-D) or its rectification consistent with 4π (3-D). Add a sensitivity line showing the S² consequences (α = 1/2, δ = 1/16).

### 6. [major] The n-fold law uses 1/δ as an amplifier, which §5's own role restriction forbids, and absorbs δ into lengths

- **category:** internal-inconsistency
- **location:** 05 §5.0 decoder row 'Generalised n-rectification'; 05 §5.3.2.3, §5.4 (Role restriction), §5.3.6 (No absorption); 07 header (ν_p = 3π⁴) and §7.3.3.2; cross-ref 08 §8.0.6(B), §8.0.5(II)

**Quote.** 05: "| Generalised n-rectification | νₙ = nπ²⁽⁽ⁿ⁻¹⁾ | n orientations, n-1 rotation-pairs averaged" [as printed: "νₙ = nπ²⁽ⁿ⁻¹⁾"]; "Role restriction: α and δ are used only as rectification constants. Reinterpreting them as a new meaning (e.g., a different coefficient or a different correction term) is forbidden."; "No absorption: it is forbidden to absorb δ into the definition of a geometric coefficient Γ(O) or into the definition of unit scales (a,Δ t,U_lat) to make δ disappear superficially."; 07: "By definition 0≤ N_δ≤ N₀."; 08: "s_n=n\,\langle W_n\rangle^{-1}=n\,\delta^{-n}" / "Equivalently, in radius form, rₙ=r₀δ^(n)/n."

**Evidence.** In §5 δ is a survival fraction: ν = δν₀, and N_δ ≤ N₀. Each extra AND-constraint can only lower a rate. ν_n = nπ^{2(n−1)} = n·δ^{−(n−1)} does the opposite. Adding sectors (more constraints) raises the rate by π² ≈ 9.87 per lock, so ν_3/ν_1 = 3π⁴ ≈ 292 > 1. §8.0.6 gets there only by redefining the attempt rate as the inverse survival, s_n = nδ^{−n}, and by moving δ into a length, r_n = r₀δⁿ/n. Those are the 'reinterpretation' and 'absorption' moves §5.4 and §5.3.6 declare immediately invalid. The §5 decoder presents the result as '(n−1) rotation-pairs averaged', which reads averaging as multiplying by π² instead of by 1/π².

**Proposed improvement.** Either (a) introduce the inverse-survival ('resistance') rate law as a new closure with its own symbol (e.g. κ := 1/δ), its own derivation, a grade of [D]/[H], and an explicit exemption from §5.3.6; or (b) derive why a lower joint survival probability must raise the event rate. Correct the §5.0 decoder reading of νₙ so it shows the inversion.

### 7. [major] 'Why this cannot be tuning' is contradicted by the decoder's own flexibility; 6π⁵ is a 1951 coincidence that misses the measurement by ~10⁶σ yet is graded [F]

- **category:** numerology-look-elsewhere
- **location:** 05 §5.0 'Decoder table' and 'Why this cannot be tuning'; 05 page header (m_p/m_e = 6π⁵ [F]); registry/vp_locks.csv row mp-me; cross-ref 13 §13.5.4

**Quote.** "There is no place to insert a free coefficient: π does not adjust, 2 does not adjust, the integer counts are fixed by the lattice."; "| Higgs channel | m_H = U_lat/(5π) | 5 channels (cell-face count minus global-reference) / one rotation averaged"; "| Mass ratio | mₚ/mₑ = 6π⁵ | 6 paired contributions, 5 nested rotations"; "| Electron rest mass | mₑ c² = 2hc/D | two endpoints / one Compton length"; "m_p/m_e = 6π⁵ — Proton-electron mass ratio as 2π·ν_p = 6π⁵ (−19 ppm vs measurement). [F] forced."

**Evidence.** (1) Products of the two constants generate a dense grammar: α^a δ^b = 2^a π^{−a−2b}, with α/δ = 2π exactly. Add integer prefactors and every 2^a π^k (k ≡ a mod 2) is reachable. (2) The decoder reads the same π differently in different places. 'One rotation averaged' is 2/π in α but plain π in 5π. The 6 in 6π⁵ is '6 paired contributions' in §5.0 but 3 sectors × (α/δ = 2π) in §8.0.5. The 2 in 2hc/D is 'two endpoints', although D ≡ 2λ_C,e by definition; §13 itself calls mₑc² = 2hc/D 'true by construction'. (3) Look-elsewhere: n·π^k with n ≤ 12, k ≤ 8 gives 10 values in [1000,3000], and the chance that one lies within 19 ppm of a random target is 0.04%. With (p/q)π^k, p,q ≤ 12, there are 89 values and the chance is 0.32%. That is notable, but it is a number, not 'forced'. The relation was published by Lenz, Phys. Rev. 82, 554 (1951). (4) As an exact identity, 6π⁵ = 1836.118109 against CODATA 2022 1836.152673426(32) is off by −18.82 ppm = −1.08×10⁶σ. An [F] 'forced' result cannot carry an unexplained 10⁶σ residual.

**Proposed improvement.** Replace the 'cannot be tuning' paragraph with a quantitative look-elsewhere statement: define the formula grammar and report the chance-match probability as above. Regrade 6π⁵ from [F] to [H] with a stated theory uncertainty (≥19 ppm), or predict the correction term that closes the −18.8 ppm. Remove mₑc² = 2hc/D from the 'forced' decoder, or mark it 'calibration identity'. Fix one reading per factor of π (with or without the 2) and apply it uniformly.

### 8. [major] '3 sectors is not a choice' holds only in a chosen 2-D plane; in 3-D the minimum is 4 (the framework's own tetrahedral certificate), and n=3 is the only integer that reproduces m_p/m_e

- **category:** grading-honesty
- **location:** 07 'Topological necessity of 3 sectors' and '(Proposition) 3 is minimal and 120° is forced'; 07 '2D sector plane and unit axes'; 06 §6.4.3 [C-82/7-08]; cross-ref 08 §8.0.5(I)

**Quote.** 07: "To physically enclose a center point (Core) in a 2D cross section, at least three vectors are required (two vectors are linear; four vectors are overcomplete)." / "thus the 3-sector (120°) structure is not a choice but a geometric consequence of “minimality + sum-zero closure.”" / "The choice of the plane (which 2D subspace of which coordinate system) is locked in analysis_lock." 06: "In 3D, four points are the minimal non-coplanar simplex."

**Evidence.** A positively spanning set in R^d needs at least d+1 vectors: 3 in a plane, 4 in space (tetrahedral, 109.47°). The 2-D restriction is an input ('the choice of the plane ... is locked'), and §6.4 uses the 4-point simplex as the minimal 3-D structure. Minimality also does not select anything: four vectors are 'overcomplete' but allowed. The step from three charge states (±,0) to three spatial sectors is not argued. The cube's rotation group has C₂, C₃ and C₄ axes, so C₃ is picked. The integer carries all the weight: through m_p/m_e = 2π·ν_n with ν_n = nπ^{2(n−1)}, n = 2 gives 4π³ = 124.03, n = 4 gives 8π⁷ = 24162.3, and only n = 3 gives 1836.12. So n is in effect selected by the target.

**Proposed improvement.** Grade n = 3 as [D]/[H] and give its actual motivation, e.g. an explicit identification with three valence constituents and C₃ rather than C₄. Or derive from the substrate dynamics why the relevant phase space is a 2-D plane, which would also address the S¹ vs S² issue. Drop 'not a choice'.

### 9. [major] 82 = 81+1 is not uniquely forced: the R²≤6 cut is one of several empty-shell closures, and the '+1' is placed at the centre (already counted) in some chapters and at the nozzle in others

- **category:** internal-inconsistency
- **location:** 07 §7.1.5.2 reading note and lattice table; cross-ref 00-prologue line 473, 14 line 42, 08 §8.0.5(I)

**Quote.** 07: "(Single source: the geometric necessity of 82=3⁴+1 — the R²≤6 packing 81 plus the single irreducible nozzle residual that does not 3-divide — together with 7=1+6, 89=82+7, ...)"; prologue: "82 = 81+1 (one central locked quantum, neutron core)"; 14: "where 81=3⁴ is exactly the number of integer-lattice points with R²≤6 (independently verified) and the +1 is the central rotation."

**Evidence.** The counts are correct (verified: R² ≤ 2, 3, 6, 9 give 19, 27, 81, 123; R² = 7 is empty). But the empty shells up to 39 are R² = 7, 15, 23, 28, 31, 39, with cumulative counts 81, 251, 461, 619, 739, so 'closed by an empty shell' does not single out 81. R² ≤ 3 (27 = 3³, the full 3×3×3 cube) is an equally natural closure. 81 = 3⁴ is a numerical coincidence of the ball count, not a 3³·3 construction. The 81 sites already include the origin (count at R² = 0 is 1), so a '+1 central quantum/rotation' would double-occupy an occupied site. Chapter 7 instead places the +1 at the 'nozzle'. The location of the one site that distinguishes 82 from 81 is inconsistent across chapters.

**Proposed improvement.** Fix one location for the +1 and give its coordinates. If it is central, explain the double occupancy, or recount as 80 + 1 + 1. State the closure rule that picks R² ≤ 6 over R² ≤ 3 or R² ≤ 14 before counting (pre-registered), and grade 82 as [D] until an independent dynamical selection exists. §14 itself says 89 is not reproduced by simulation.

### 10. [major] Integerization: the symmetric-case formula breaks sum preservation for N≡2 (mod 3), and the projection rule can never produce the min-variance splits used for 82/89

- **category:** math-error
- **location:** 07 'Definition of real-valued sector scores s_i' (symmetric-input output eq.), 'Integerization (sum-preserving) rule', §7.1.3–§7.1.5

**Quote.** "\left(\left\lfloor\dfrac{N}{3}\right\rfloor,\left\lfloor\dfrac{N}{3}\right\rfloor,\left\lceil\dfrac{N}{3}\right\rceil\right)\ \text{and its permutations},& N\not\equiv 0\ (\mathrm{mod}\ 3)"; "s_i\ge 0\quad (i=1,2,3), \qquad \text{and at least one } s_i \text{ is } 0."; "Define integerization as “the integer allocation closest to the fractions f_i,”"

**Evidence.** (1) For N = 89 (r = 2), (⌊89/3⌋, ⌊89/3⌋, ⌈89/3⌉) = (29,29,30), which sums to 88 ≠ 89. That violates the chapter's invariant k₁+k₂+k₃ = N. The correct form for r = 2 is (m, m+1, m+1). (2) For S > 0 the shift s_i = p_i − p_min makes some f_i = 0. That sector gets k̃ = 0 with residual 0 and can never be among the ≤ 2 top residuals, so k_min = 0 for every non-symmetric u. For example u = n₁ gives (N,0,0), and u at 30° gives (59,30,0) for N = 89. The splits (30,30,29) and (28,27,27) in §7.1 come only from the separate minimum-variance rule, which ignores u entirely. Two incompatible algorithms are both called 'the integerization rule', and the directional input u never affects the nucleon counts.

**Proposed improvement.** Correct the symmetric branch to (m, m+r_1, m+r_2) with r ones assigned by π_sec, i.e. (m,m,m+1) for r = 1 and (m,m+1,m+1) for r = 2. Say which rule governs which object (projection rule vs minimum variance), rename one of them, and state explicitly that the nucleon splits do not depend on u.

### 11. [major] The 3-sector residual labels cannot give 'proton charged, electron shell opposite, neutron core neutral' for any locked (π_sec, n_Q)

- **category:** internal-inconsistency
- **location:** 07 'Residual (non-cancelled) vector and the link to charge/electron labels', §7.1.6.2, §7.4.4–§7.4.5; cross-ref 14 line 42 and §14.0.4

**Quote.** 07: "Therefore the integerization rule in this chapter is a “super-convention” for charge/electron labels: labels cannot be introduced separately by bypassing the integerization rule." / "If N≡ 1(mod3) and the output is a permutation of (m,m,m+1), then V points along the sector axis that receives “+1.”"; label: "\texttt{NEUTRAL}, & \|\mathbf{V}\|<V_{\min}\ \vee\ s_Q(\mathbf{V})=0"; 14: "This 82 is the neutron core (charge-neutral; the most uniform 3-partition is 82=28+27+27, Δ_(max)=1)"

**Evidence.** With minimum-variance integerization and π_sec = (1,2,3): 7 → (3,2,2) gives V = n₁; 82 → (28,27,27) gives V = n₁; 89 → (30,30,29) gives V = −n₃. All three have ‖V‖ = 1, so no V_min threshold can separate them. Because 7 ≡ 82 ≡ 1 (mod 3), the electron shell and the neutron core always get the same V, and therefore the same label, for any single locked (π_sec, n_Q). I scanned all 6 permutations × 36,000 axis angles n_Q. There are 71,988 configurations in which 89 and 7 get opposite signs, and in 0 of them is 82 NEUTRAL. §14 calls 82 'charge-neutral' because it is '28+27+27', which contradicts §7.4.5, where that split gives a non-degenerate V.

**Proposed improvement.** Mark §7.4 as superseded by the §14.0.4 nozzle-charge mechanism and remove the 'super-convention' sentence. Or redesign the label so it depends on more than N mod 3. Either way, delete the '28+27+27 ⇒ neutral' argument in §14.

### 12. [major] Units: ν_p = 3π⁴ is a pure number but is locked in s⁻¹; it is used as dimensionless in 6π⁵ and dimensional in build times, and the two T_build definitions differ by 1.8×10¹⁸

- **category:** unit-dimension
- **location:** 07 §7.2.1 (S07_02_nu_can_def), §7.2.5, §7.5.1 (S07_Tbuild_tick), §7.5.2 (S07_Tbuild_rate), header of §7.2; cross-ref 08 §8.0.5(IV), 09 §9.4 line 569, 12

**Quote.** 07: "Definition (S07_02_nu_can_def) is the definition of “events per unit time,” and the unit of ν_p,can is locked as [s⁻¹]."; "T_{\mathrm{build}} := N\,\Delta t."; "T_{\mathrm{build}} := \frac{N}{\nu}."; "Two integers, one rate, the n-p split in seconds."; 08: "\nu_{p,\mathrm{can}} &= 3\pi^{4}=292.227\ \mathrm{s^{-1}}" and "\frac{m_{p}}{m_{e}} &= 2\pi\,\nu_{p,\mathrm{can}}"; 09: "Here “Hz=s⁻¹” reads the canonical second as equivalent to the SI second"

**Evidence.** 3π⁴ and the §9.4 length route s_p·δ = (D_anch/2r_p)·δ are both ratios of lengths, i.e. dimensionless. m_p/m_e = 2π·ν_p only makes sense if ν_p is dimensionless. §7.2 nevertheless gives T_p = 89/(3π⁴) s = 0.3046 s, T_n = 0.2806 s and T_p − T_n = 23.95 ms. Those numbers depend on the SI second, a human convention (Cs-133, 9,192,631,770 Hz). The only bridge to SI is §12's T_e ≈ 1 s, graded [H]+, and its measure choice alone moves T_e by −47%. Separately, T_build = NΔt (Δt = 1.86e-21 s) gives 89Δt = 1.66e-19 s, while N/ν gives 0.305 s. The two definitions of the same symbol differ by 1.84×10¹⁸, which is the symbol overloading §5.5 calls immediately invalid.

**Proposed improvement.** Define ν_p ≡ ν_p,can/ν_e,can as a dimensionless ratio (= 3π⁴) and express build times in units of the electron period T_e (T_p = 89/(3π⁴)·T_e). Any SI-second value then inherits §12's [H]+ grade and cannot be [F]. Rename one of the two build times (e.g. T_tick vs T_rate) and state the regime in which each applies.

### 13. [major] T_p/T_n = 89/82 is graded [F] but has no observable, and it runs opposite in sign (and ~62× in size) to the n–p mass split it is said to 'track'

- **category:** missing-test-or-prediction
- **location:** 07 §7.2 header and §7.2.5; cross-ref 01 line 9/519/611, 14 line 107, 05 §5.3.4 (Ξ = N_δ/N_ref)

**Quote.** 07: "[F] build timesin: $νₚ$ / out: $Tₚ/Tₙ=89/82$; $Tₚ-Tₙ=7/ν$Two integers, one rate, the n-p split in seconds."; 01: "The 89/82 legitimately tracks mₙ>mₚ (gravity), not Coulomb."; 14: "the proton and neutron share the same 82 core, hence nearly equal mass"

**Evidence.** N_p = 89 > N_n = 82, so the p-structure has more counts and a longer build. Under §5.3.4's mass form m = U_lat·Γ·Ξ with Ξ ∝ counts, that makes the proton heavier. The measured split has the opposite sign: m_n/m_p = 939.56542052/938.27208816 = 1.0013784. In size, 89/82 − 1 = 0.0854 is 62× the measured 0.00138. §1's claim that 89/82 'tracks m_n > m_p' therefore has the wrong sign, and §14 says both nucleons share the 82 core, so 89/82 should not enter the masses at all. No observable is named for T_p, T_n or 7/ν.

**Proposed improvement.** Either name the observable T_p/T_n corresponds to and test it (as written it fails the n–p mass sign), or downgrade §7.2 to [D] bookkeeping with no physical claim. Remove or correct the §1 sentence 'The 89/82 legitimately tracks mₙ>mₚ'. A genuine target would be m_n − m_p = 1.29333 MeV from the model; register it as [O].

### 14. [major] The §6.4 cross-section gate fails when run on the chapter's own 81-site core; no pre-registered threshold exists anywhere in the repo

- **category:** reproducibility-code
- **location:** 06 §6.4.3 [C-82/7-01], [C-82/7-02], [C-82/7-07]; 06 §6.2.1; 05 §5.2.6 (T1–T3); 07 §7.1.4 (π_sec), §7.4.3 (n_Q), §7.4.4.2 (V_min); repro/physics/registry/vp_locks.csv

**Quote.** 06: "\left|I_{\sigma,82}-\frac{4}{\pi}\right|>\varepsilon_{\sigma} \quad\Longrightarrow\quad \texttt{FAIL-CORE82-SIGMA}." / "The tolerance (allowable error) ε_R must be registered in advance in gate_lock" / "R is an aggregation coordinate inside the canonical cell (CELL-CUBE); the cell geometry is not replaced by a sphere." / "Mixing the cell geometry (cube) and a visualization sphere when computing cross sections or radii."; 05: "With the threshold ε_bias locked in gate_lock,"

**Evidence.** I ran [C-82/7-02] on the R² ≤ 6 core (81 sites), taking the boundary at √6 so that R_82 = R_p, and L_q = (π/2)R_p. The z-projection is 21 columns, and its convex hull is the octagon (±2,±1),(±1,±2) with area 14. That gives I_σ = 14/6·(2/π)² = 0.946 (convex hull) or 21/6·(2/π)² = 1.418 (column count), against 4/π = 1.273, i.e. −26% or +11%. The test fails, or its verdict depends on an unspecified ProjArea choice. No file named gate_lock, analysis_lock or canon_lock exists in the repo (find returns nothing). registry/vp_locks.csv has no threshold rows, and no numeric value of ε_bias, ε_corr, ε_δ, ε_R, ε_σ, V_min, π_sec or n_Q appears anywhere in the chapter texts. §6.2.1 forbids replacing the cube cell with a sphere, then uses A = 4πR² and σ = πR_p², the mixing [C-82/7-07] calls FAIL.

**Proposed improvement.** Publish the gate_lock/analysis_lock files with the numeric thresholds and the discrete choices (Agg, ProjArea, n_σ, B_82, π_sec, n_Q). Add a script that runs [C-82/7-01..08] and T1–T3 on the shipped 82-core coordinates, and report the verdict, including a FAIL if that is the result. Resolve the cube/sphere contradiction in §6.2.1.

### 15. [minor] Presentation slips: wrong descriptor for α, decoder reading of δ contradicts its derivation, garbled 'half-cycle of a sine', and 16-digit false precision

- **category:** presentation-rendering
- **location:** 06 page header / registry vp_locks.csv row alpha; 05 §5.0 decoder table and 'Why this cannot be tuning'; 06 §6.3.5–§6.3.6

**Quote.** "α = 2/π — Geometric rectification ratio (full-wave to half-wave mean); the single rectification anchor."; "| Double rectification | δ = 1/π² | two rotations averaged, both ends summed"; "⟨cosθ⟩=2/π from the half-cycle of a sine"; "&=2.223045751056016\ \mathrm{fm}^2."

**Evidence.** The full-wave mean ⟨|cos|⟩ = 2/π and the half-wave mean ⟨[cos]+⟩ = 1/π have ratio 2, not 2/π. δ is built from half-wave factors [·]+, i.e. one end only. Summing both ends (|cos|) would give α² = 4/π² = 0.405, not 1/π². ⟨cosθ⟩ over a full cycle is 0. The 2/π value is the average of sinθ over [0,π] or of cosθ over [−π/2,π/2]. σ_geom is quoted to 16 significant figures from a 4-s.f. input (0.8412), and the 'Invariant I' check σ/L_q² = 4/π is (2/π)²·π, pure algebra.

**Proposed improvement.** Change α's descriptor to 'full-wave rectified mean of a unit cosine (mean/peak)'. Change δ's reading to 'two independent half-wave (one-end) averages'. Rewrite the sine example as ⟨sinθ⟩_{[0,π]} = 2/π. Round derived numbers to input precision (σ_geom ≈ 2.223 fm²), and label Invariant I as an algebraic identity, not a numerical check.

**Strengths noted:**
- The integrals are carried out explicitly and correctly: ⟨|cosθ|⟩=2/π and ⟨[cosθ]+⟩=1/π on S¹ (checked numerically), and δ's product-measure assumption is stated openly as [A-5.2-U0] with named falsification triggers T1–T5. That is a good template, and it only needs thresholds and a joint-independence test.
- Symbol discipline is good: α (rectification) is explicitly separated from α_em, which is honestly graded [O] as a measured input and not derived.
- §7.1's minimum-variance lemma, the complete N=3m+r classification and S₂,min = 3m²+2mr+r are correct. The lattice-shell counts 19/27/81/123 and the Legendre empty shell R²=7 check out exactly.
- §7.1.8 honestly demotes the n_r=5 / φ_pack=82/125 radial route to a non-load-bearing, back-calculated consistency indicator instead of claiming it as a prediction. The same self-downgrading should be applied elsewhere.
- The repro tool vp_numeric_ssot.py regenerates the numbers deterministically from declared inputs, labels residual baselines, and admits that the r_p 'prediction' is not independent of the 6π⁵ residual (R2 = −R1).
- Once the circular λ_C is removed, a crisp and testable statement remains: r_p = (2/π)·h/(m_p c) = 4ħ/(m_p c) = 0.841236 fm, within 0.76σ of CODATA 2022 (0.84075±0.00064 fm). With the observable definition fixed, this is worth promoting as the pre-registered prediction.


## review:proton-event-electron

### 1. [critical] Canonical 'rates' ν_n are dimensionless length ratios, yet they are quoted in s⁻¹/Hz and used as per-second physical quantities

- **category:** unit-dimension
- **location:** 08-discrete-proton-structure-82-7 §8.0.5(IV), §8.5.1–8.5.2; 09-event-quantum-definition-canonical-event §9.2.2.2, §9.3.1, §9.3.4.2, §9.4.2, §9.4.3.3; 12-electron-1-second-cross-check §12.2.4.2, §12.2.5.1; cross-refs 07 §7.2.1, 14 §14.0.4, repro/physics/tools/vp_timegravity_ssot.py

**Quote.** §8.0.5(IV): "\nu_{p,\mathrm{can}} &= 3\pi^{4}=292.227\ \mathrm{s^{-1}} ... \frac{m_{p}}{m_{e}} &= 2\pi\,\nu_{p,\mathrm{can}} = 2\pi\cdot 3\pi^{4}=6\pi^{5}=1836.118"; §9.2.2.2: "s := \lim_{T\to\infty}\frac{N_0(t;T)}{T}"; §9.4.2: "Define the proton scale factor sₚ as the following dimensionless ratio."; §9.4.3.3: "Here “Hz=s⁻¹” reads the canonical second as equivalent to the SI second; the equivalence judgment is performed by the unit-realization (cross-validation) Gate."; §12.2.5.1: "\mathbb{E}\!\left[N_{e}[n_1,n_2)\right] = \Delta T."; §8.5.1: "Assumptions: reduced units c=1, quantum diameter d=1"; §8.5.2: "The steady annihilation throughput equals the canonical event rate νₚ=3π⁴≈ 292.23s⁻¹"; ch14: "The source strength Q is the annihilation rate: νₚ=3π⁴≈292s⁻¹ and νₑ=1s⁻¹ (§12)"

**Evidence.** §9.2.2.2 defines the attempt rate s as counts per time (dimension T⁻¹). §9.3.4.2 (s_e := r_0/r_e) and §9.4.2 (s_p := D/(2r_p)) then redefine it as a length ratio with no dimensions. δ = 1/π² has no dimensions, so ν_p = s_p·δ = D/(2π² r_p) = 292.245 is a pure number, and ν_e := 1 is a pure number too. The mass identity m_p/m_e = 2πν_p has consistent dimensions only if ν_p has none. Read literally as 292.227 s⁻¹, the ratio m_p/m_e would carry s⁻¹. The text puts off the Hz reading to a gate, G-E1S, which never receives a decision rule or verdict (§12.5). Eq. (S12_02_ENe_general) sets a count equal to a time (E[N_e] = ΔT). (S12_02_Tevent) does the reverse: T_e^(event) := N_e/ν_e = N_e. Both hold only if ν_e = 1 s⁻¹ is assumed, and that is the claim the chapter says it tests. §8.5.2 reports an MD result of '292.23 s⁻¹' from a run in reduced units (c = 1, d = 1), where the natural time unit is d/c; a per-SI-second rate cannot come out of that without a conversion, and the bundle is not in repro/physics/. Downstream results are built on the s⁻¹ reading: ch7 gives T_p = 89/ν_p = 0.3046 s ('the n-p split in seconds'), and ch14 and the TIME_GRAVITY ledger use 292 s⁻¹ and 1 s⁻¹ as gravitational source strengths.

**Proposed improvement.** Declare every ν_n dimensionless (in units of ν_e). Remove 's⁻¹'/'Hz' from §8.0.5(IV), §8.5.2, §9.4.3.3, §13.5.6, the scorecard, TIME_GRAVITY_NUMERIC_LEDGER.csv and the ch7 build times. Either rename s_p/s_e as 'scale ratio', or write s_p = (D/2r_p)/τ_* with τ_* an explicit dimensionful constant graded [L]/[O]. Rewrite (S12_02_ENe_general) and (S12_02_Tevent) as E[N_e] = ν_e·ΔT with units shown. State that identifying the canonical unit with the SI second is an open [O] conjecture until ν_e is derived as a multiple of a natural rate such as m_e c²/h. Add unit tags to vp_numeric_ssot.py so that attaching s⁻¹ to a length ratio FAILs the gate.

### 2. [critical] T_e ≈ 1 s comes from SI-convention inputs (N = 10¹², the He–Ne line, a round Δt with A back-solved to 80 digits); it is not derived

- **category:** circularity
- **location:** 12-electron-1-second-cross-check ('Grade of Tₑ≈1s', O(1) table, §12.2.2); inputs from 11-realization-units-t-rcross §11.2–11.3; 01-governance §1.9 A5

**Quote.** §12: "computes Tₑ≈ (D/a)³τ_VP× 6/5 and yields ≈ 1.0s"; §11.3: "A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599" and "The tick follows from the amplification; $cΔ t/a=A$ closes exactly."; §11.2: "N = 10^{12}."; §1.9 A5: "any other anchor in the window predicts the same dimensionless ratios."; §12: "the natural time scale to traverse one Compton volume comes out at 1s."

**Evidence.** (1) Computed with 80-digit Decimal: c·(1.86×10⁻²¹ s)/a, with a = 632.99121257859865746 nm/10¹², reproduces the locked A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599 in every printed digit. So Δt = 1.86×10⁻²¹ s, a 3-significant-figure round number, is the input and A is the output. 'Closes exactly' is therefore an identity, not a check. (2) T_e = (D/a)³Δt·6/5 = (2λ_C,e·N/λ_ref)³Δt·6/5 = 4.5054×10²⁰ × 1.86×10⁻²¹ × 1.2 = 1.0056 s. Changing only conventions (Δt held fixed, as the chapter does) moves it: λ_ref = 532 nm (the second RCROSS channel) gives 1.694 s; N = 2⁴⁰ instead of 10¹² gives 1.337 s; both together give 2.25 s. At fixed A, T_e ∝ N², so N = 10¹¹ gives 0.010 s. A5 is right that dimensionless ratios survive a change of anchor, but T_e is not dimensionless. (3) In natural units T_e = 7.807×10²⁰ ħ/(m_e c²), while 1 SI s = 7.763×10²⁰ ħ/(m_e c²). That second number carries the Cs-133 definition (9 192 631 770 periods) and the historical 1/86400-of-a-day second. No theory that lacks atomic-clock physics can output it except through its inputs. (4) The 'volume-reaches-c heuristic' needs one cell per tick, processed serially, over 4.5×10²⁰ cells. A signal at c crosses D in D/c = 1.6×10⁻²⁰ s.

**Proposed improvement.** Reclassify 'T_e ≈ 1 s' as a unit-convention coincidence ([O], and not evidence). Quote T_e in natural units (T_e·m_e c²/ħ ≈ 7.8×10²⁰) and ask whether that pure number can be derived. State the dependence explicitly: T_e ∝ N³λ_ref⁻³Δt. Delete the 80-digit A and show Δt as a declared input graded [L], or derive Δt without using c·(a chosen number). If a time prediction is wanted, pre-register a dimensionless ratio of the canonical time to a measured physical time.

### 3. [critical] The n-fold exponent n−1 comes from inconsistent survival accounting; applied consistently, §9.2's own theorem gives ν_n = n, and C₃ ring closure makes the joint survival exactly zero

- **category:** math-error
- **location:** 08-discrete-proton-structure-82-7 §8.0.5(II), §8.0.6(A),(B),(D); 09-event-quantum-definition-canonical-event §9.2.4.1, [T-9.2-1]

**Quote.** §8.0.5(II): "For an n-sector object the number of independent inter-sector phase locks is ... n-1"; §8.0.6(A): "the C₃ ring-closure Σ_in_i=0 (§8.0.3) fixes the global phase as a gauge choice and removes no rectification." and "\prod_{i=1}^{n}\langle w_i\rangle=\delta^{\,n}=\pi^{-2n}"; §8.0.6(B): "s_n=n\,\langle W_n\rangle^{-1}=n\,\delta^{-n},\qquad \nu_n=s_n\,\delta=n\,\delta^{-(n-1)}"; §8.0.6(D): "Nucleon (here): N=n sectors ⇒ n-1 independent inter-sector locks, giving the exponent in νₙ=nπ²⁽ⁿ⁻¹⁾."; §9.2.4.1: "Define δ as the following mean survival coefficient."

**Evidence.** §9.2 defines δ as the mean survival weight of the attempts being counted, and proves ν = s·δ from that definition. For an n-sector attempt the survival weight is W_n, with ⟨W_n⟩ = δⁿ (§8.0.6(A)). Applied consistently, [T-9.2-1] gives ν_n = s_n⟨W_n⟩ = nδ⁻ⁿ·δⁿ = n, so ν₃ = 3 and 2πν₃ = 18.85. Taking instead the n−1 independent locks of §8.0.5(II)/(D) (⟨W⟩ = δ^{n−1}, s = n⟨W⟩⁻¹, ν = sδ) gives ν₃ = 3π² = 29.6 and 2πν₃ = 6π³ = 186.0. Only the mixed reading gives 3π⁴: the attempt rate from δ⁻ⁿ, the survival from a single δ. §8.0.6 also asserts both 'removes no rectification' (exponent n) and the gauge lemma (exponent n−1). In addition, §8.0.5(II) says the directional phase is the inter-sector relative phase, so θ_i are the directions of the sector vectors. Σn_i = 0 for three unit vectors imposes 2 constraints, not one global phase: it forces 120° spacing, hence Σcos θ_i = 0 and at least one [cos θ_i]_+ = 0. Numerically, max over the global phase of Π_k[cos(θ+2πk/3)]_+ = 0.0 exactly. It is also 0 for 2×10⁵ random ring-closed 3D triples projected on random axes. Under the stated closure the joint directional survival is identically 0, not δ³. The product measure needs the sector phases to be independent, which contradicts their being ring-locked.

**Proposed improvement.** Choose one model and derive the exponent once. Either: independent sectors (product measure, no ring lock), with ν_n computed from [T-9.2-1] using ⟨W_n⟩. Or: ring-locked sectors, with the constrained integral actually computed. Report the exponent that results. If it is not n−1, take 3π⁴ out of the forced chain. Remove the text asserting both 'removes no rectification' and the n−1 gauge count.

### 4. [critical] The gravitational source ratio ν_p:ν_e = 292:1 differs from the inertial ratio 1836:1 by an asymmetric '2π = α/δ' map, giving composition-dependent active mass about 8 orders above bounds

- **category:** physics-validity
- **location:** 08-discrete-proton-structure-82-7 §8.0.5(IV); 09-event-quantum-definition-canonical-event (chapter concept link), §9.3; cross-refs 13 §13.5.4–13.5.5, 14 §14.0.4, 17 §17.4.0

**Quote.** §8.0.5(IV): "The factor 2π=α/δ is the derived ratio of the two rectification constants (§13.5.5), not a reporting convention."; §9: "the annihilation/event rate defined here is the root cause of gravity (§17.4.0, cap §17.4)"; ch14: "The source strength Q is the annihilation rate: νₚ=3π⁴≈292s⁻¹ and νₑ=1s⁻¹ (§12), consistent with mₚ/mₑ=2πνₚ=6π⁵."; ch17: "\text{annihilation rate } \nu_{\mathrm{ann}} \;\xrightarrow{\times 2\pi}\; \text{mass}"; ch13: "\lambda_{C,e}:=r_0=\frac{D_{\mathrm{anch}}}{2}" and "\lambda_C=\frac{\pi}{2}\,r_p"

**Evidence.** In ch13 the electron's Compton length is its rate radius divided by δ (λ_C,e = r_0 = r_e/δ). The proton's is its rate radius divided by α (λ_C,p = (π/2)r_p = r_p/α). So m_p/m_e = (α/δ)(r_e/r_p) = 2πν_p: the 2π is the ratio of two different conversion constants applied to the two particles. §17.4.0 states one universal map, 'rate ×2π → mass'. Applied to the electron (ν_e = 1) it gives m_e = 2π, and m_p/m_e = ν_p/ν_e = 3π⁴ = 292.2, not 1836. ch14 makes the event rate the gravitational source (Q_p = 292, Q_e = 1, neutron 'identical inflow'). An electron's active gravitational mass relative to a nucleon is then 1/292.2 = 3.42×10⁻³, against an inertial 5.45×10⁻⁴. Model: Q = ν_p(Z+N) + ν_e·Z, m = atomic mass. Then (Q/m)_Al27/(Q/m)_Fe56 − 1 = −4.2×10⁻⁴; the electron term alone, Δ(Z/A)(1/292.2 − 1/1836.15), is 4.7×10⁻⁵. For Ti48/Pt195 the difference is 1.1×10⁻³. The lunar laser ranging bound on the Al/Fe active-to-inertial mass difference (Bartlett & van Buren 1986) is < 4×10⁻¹², so this is excluded by 7–8 orders of magnitude. §17.4's 'equivalence principle as a result' covers only the passive response.

**Proposed improvement.** Choose one of two routes. (a) Make the rate→mass map universal, which forces ν_e = 1/(2π) or ν_p = 6π⁵, and redo LOCK-NU-N. (b) State that gravitational source strength is proportional to inertial mass, not to event rate, and remove 'Q is the annihilation rate' from ch9/ch14/ch17. Add an equivalence-principle gate that predicts the active and passive composition dependence for Al/Fe and Ti/Pt and compares it with the LLR and MICROSCOPE bounds (η(Ti,Pt) ~ 10⁻¹⁵).

### 5. [major] The [F] grade for LOCK-NU-N / 6π⁵ is overclaimed: it was built to fit Lenz 1951, the electron 'check' cannot fail, and an exact identity is excluded at ~10⁶σ

- **category:** grading-honesty
- **location:** 08-discrete-proton-structure-82-7 §8.0.5(III)–(IV), §8.0.6(C); 00-prologue; ea-epistemic-audit-log; repro/physics/registry/vp_locks.csv

**Quote.** §8.0.5(III): "The electron case is a nontrivial check: the law reproduces the independently defined electron clock of §9.3, it is not fitted to it."; §8.0.6(C): "It is graded [F]{} under that lock, by the same standard that grades α=2/π and δ=1/π² as [F]{}."; prologue: "Lenz 1951 for mₚ/mₑ=6π⁵ as numerical coincidence"; audit log: "Lenz (1951) characterization changed from "numerical coincidence" to "preceded the present derivation" (so that external readers do not read the Lenz mention as a concession that our result is also numerology)."

**Evidence.** 6π⁵ = 1836.118109 against CODATA 2022 1836.152673426(32): −18.8 ppm, which is −1.08×10⁶σ. A 'forced' exact identity is therefore excluded unless a correction with derived sign and size is supplied. None is. The electron case is automatic: ν₁ = 1·x⁰ = 1 for any base x, and s₁ = δ⁻¹ is §9.3's own definition, so it cannot fail. That leaves one non-trivial data point (n = 3), and it is the value known since Lenz 1951. Enumerating natural variants of the construction: 7 rate laws {nδ^-(n-1), nδ^-n, δ^-(n-1), δ^-n, nδ^-(n-2), (n−1)δ^-(n-1), n!δ^-(n-1)} × 8 mass maps {1, α/δ, 1/δ, 1/α, α, δ/α, 2, π}. Three of the 56 combinations give exactly 6π⁵ (for example nδ⁻ⁿ·α also does); no other is within 1%. Look-elsewhere (seed 19, 2×10⁵ log-uniform targets in [10², 10⁴]): the chance that a random target is matched within 19 ppm is 4×10⁻⁴ for a·π^b (a ≤ 12, b ≤ 8; 108 forms), 3×10⁻³ for p/q·π^b (1001 forms) and 6×10⁻³ for half-integer powers (1911 forms). Lenz's hit is notable as a search result. The later derivation adds evidence only if its choices were fixed in advance, and they were not. The out-of-sample outputs are never stated: n = 2 gives ν = 2π², which under the mass map is 4π³ m_e = 63.4 MeV; n = 4 gives 8π⁷ m_e = 12.35 GeV. Neither corresponds to a known particle, and the text does not say whether n ≠ 1, 3 is allowed.

**Proposed improvement.** Downgrade LOCK-NU-N, 3π⁴ and 6π⁵ to [H], a hypothesis resting on a known coincidence (also in vp_locks.csv). Cite F. Lenz, Phys. Rev. 82, 554 (1951) in §8.0.5 and §13.5. Replace 'nontrivial check' with 'consistency of definitions'. Publish the variant enumeration and look-elsewhere numbers. State the domain of n: either commit to predictions for n ≠ 3 or say that n = 3 is the only instance. Carry −18.8 ppm as an unexplained residual that a correction term must account for.

### 6. [major] The r_p 'prediction' and the ν_p length cross-check compare the framework's formula with its own rounded value; +61 ppm is rounding plus the Lenz residual

- **category:** circularity
- **location:** 08-discrete-proton-structure-82-7 §8.0.5(IV); 09-event-quantum-definition-canonical-event §9.4 (header, SSOT note, §9.4.5.2); cross-refs sp-jamming-spine, 01 §1.9 A3, repro/physics/tools/vp_numeric_ssot.py

**Quote.** §8.0.5(IV): "r_{p} &= \frac{D_{\mathrm{anch}}}{6\pi^{6}}=0.84125\ \mathrm{fm} && \text{\emph{prediction}\quad}({+}61\ \mathrm{ppm}\ \text{vs locked}\ 0.8412)"; §9.4: "The length route lands 61 ppm from canon — the same chain as the $-19$ ppm."; spine: "r_p=(2/π)λ_{C,p}=0.8412fm (CODATA charge radius0.8414fm,-0.02%)"; §1.9 A3: "rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm)"; §9.4.5.2: "Hence, locking rₚ to (S09_04_rp_lock) simultaneously fixes the corresponding ν_p,can to the single value (S09_04_nup_numeric)."

**Evidence.** D/(6π⁶) = 2λ_C,e/(6π⁶) = 4ħ/(m_p c) with m_p replaced by 6π⁵m_e. With CODATA 2022 values, 4ħ/(m_p c) = 0.8412356 fm and D/(6π⁶) = 0.8412515 fm; the +18.8 ppm gap is the Lenz residual. The 'locked 0.8412' is (2/π)λ_C,p, i.e. the framework's own formula with measured m_p, rounded to 4 digits: 0.8412/0.8412356 − 1 = −42.4 ppm. So +61.2 ppm = 18.8 + 42.4, and it carries no information about the radius. vp_numeric_ssot.py already records R4 = R3 and R2 = −R1. The length-route ν_p = D/(2π²·0.8412 fm) = 292.2452 differs from 3π⁴ by the same +61.2 ppm. Against measurements, the prediction is +596 ppm (+0.78σ) from CODATA 2022 0.84075(64) fm, +454 ppm (0.98σ) from muonic hydrogen 0.84087(39) fm, and −177 ppm from CODATA 2018 0.8414(19) fm. §1.9 uses CODATA 2018 and §8.0.5 uses the locked value, so one number has two comparators and neither is current. The 61 ppm is also below the chapter's own D-precision floor ('D-limited to ~0.04%', i.e. 400 ppm). §9.4.5 treats r_p as the input that fixes ν_p = 292.2451560, which contradicts the SSOT note that 3π⁴ is canonical. The relation r_p ≈ 4ħ/(m_p c) has also appeared before in the literature.

**Proposed improvement.** Compare r_p only with CODATA 2022 (0.84075(64) fm) and report +0.78σ. Drop '+61 ppm' as a cross-check, or relabel it 'rounding + R1'. State that, given λ_C = (π/2)r_p, r_p = D/(6π⁶) is algebraically the same claim as 6π⁵ and not an independent prediction; remove the 'removes one empirical degree of freedom' wording. Delete the 'single value' sentence in §9.4.5.2, or recast §9.4 as a derived consistency identity.

### 7. [major] The [H]+ grade for T_e is unsupported: the 'two independent paths' are one formula, the measure and factor were picked after the fact, G-E1S has no rule, and the cited scripts are not in the repo

- **category:** grading-honesty
- **location:** 12-electron-1-second-cross-check ('Grade of Tₑ≈1s', O(1) table, §12.5); w0-result-scorecard; 01 §1.9 A2

**Quote.** §12: "The "+" denotes that this is a derived value backed by two independent load-bearing paths under a single anchor — the reproducible code (B) and the canonical geometry (G)"; "Only the bounding-cube measure lands on the clock"; "Tₑ∝ N² scaling invariance"; "it is the same factor that closes the Higgs mass to within -0.40%"; §12.5: "The concrete judgment rule for G-E1S (e.g., self-consistency of the 1-second window computed from Δ t and event rates, log completeness, sensitivity/error budget, falsification triggers) is completed in the subsequent sections of this chapter."; scorecard: "Tₑ=NΔ t, N=N₇₅₀"

**Evidence.** Path (B) 'computes Tₑ≈(D/a)³τ_VP×6/5', which is the same closed form as path (G). One line of arithmetic (4.5054×10²⁰ × 1.86×10⁻²¹ × 1.2 = 1.0056 s) reproduces it, so the two paths are not independent. The measure and the channel factor come from a larger set: {cube, sphere π/6, jam 0.633·π/6} × {1, 6/5, 5/6} gives 0.838/1.006/0.698, 0.439/0.527/0.366 and 0.278/0.333/0.232 s. Only cube × 6/5 is within 1% of 1 s. 'N² scaling invariance' is really a dependence: at fixed A, T_e ∝ N², and N = 10¹¹ gives 0.010 s. The Higgs closure uses 5π, not 6/5, and m_H = hcN/(5πλ_ref) depends on the same N and λ_ref (124.69 GeV at 633 nm, 148.37 GeV at 532 nm), so it gives no independent support. The scorecard formula (T_e = NΔt, N = N₇₅₀) differs from §12's. No G-E1S rule or verdict appears in §12.1–12.3 or in repro/physics/reports. By §12's own rule ('time-based conclusions lose status unless PASS'), every time-based conclusion is therefore without status. The scripts lattice_3d_jam_percolation.py and electron_one_second.py are not in repro/physics/.

**Proposed improvement.** Grade T_e [O] (or withdraw it). Count (B) and (G) as a single path. Publish the full 9–12-variant table as the look-elsewhere estimate. Define G-E1S with a pre-registered tolerance and record its verdict, or remove the 'final gate' language. Put the scripts in repro/physics with sha256. Reconcile the scorecard formula with §12.

### 8. [major] The §8.0 single-nozzle geometry and §8.2's tetrahedral quad contradict each other; the partition is not forced, and the minimality argument gives 5, not 7

- **category:** internal-inconsistency
- **location:** 08-discrete-proton-structure-82-7 §8.0.3, §8.0.4, §8.2 (I), §8.2.5

**Quote.** §8.0.3: "Whatever inflow exists must be carried by the remaining 2 points (the fixed axis pair)."; §8.0.4: "the six cancelling points (the "2+4") are exactly the three antipodal cyclic pairs whose vector sum vanishes (§8.0.3)"; "The single-inlet structure is a forced geometric consequence of C₃ symmetry breaking; no empirical input enters."; §8.2(I): "Sum-zero cancellation of three vectors always lies in a plane and thus cannot enforce 3D isotropic cancellation." and "Therefore, to maximize cancellation while including both "one pair" and "one quad", the shell requires at least 2+4=6 vectors."

**Evidence.** I enumerated by brute force all partitions of the 7 points {(1,1,1)} ∪ {6 ring points} into (pair, quad, survivor). There are exactly 3. In all of them the survivor is the nozzle and the quad is two antipodal pairs: a planar rectangle with normalized dot products −1 and ±1/3. None is the regular tetrahedron (all dots −1/3) that §8.2(I) requires. Every tetrahedral quad among cube vertices contains an axis point ({(1,1,1),(1,−1,−1),(−1,1,−1),(−1,−1,1)} or its negative), so §8.0.4's correspondence fails. C₃ permutes the 3 partitions, so choosing one breaks the symmetry used to derive it; the Select closure of §8.2.5 is doing the work. §8.0.3's argument that antipodal pairs carry no net flux applies equally to the axis pair: (1,1,1) + (−1,−1,−1) = 0. Making one end 'open' is therefore an extra input that breaks inversion symmetry. On minimality: if coplanar cancellation is inadmissible, the smallest isotropic cancelling set is the tetrahedron (4 points), and the smallest shell with one survivor is 5. The criterion as stated does not motivate adding a collinear pair.

**Proposed improvement.** Either redefine the quad as 'two antipodal pairs' and drop the isotropy argument, or build the tetrahedral quad with an axis point and re-derive which point survives. Declare the inversion-breaking choice of open end as an explicit lock. Regrade §8.0.4 and §8.2's '7 = 2+4+1' from [F] to definitional/[H].

### 9. [major] The 89 = 82 + 7 count double-counts points: the nozzle sits in both 82 and 7, the shell points lie inside the R² ≤ 6 core, and the 'residual match' is a tautology

- **category:** internal-inconsistency
- **location:** 08-discrete-proton-structure-82-7 §8.0.2, §8.0.5(I), §8.1.3.2, §8.2(III); 07 §7.2.2

**Quote.** §8.0.5(I): "The “+1” in 82=81+1 is the same single-nozzle residual as the “1” in 7=1+6" and "build count 89=82+7 — core + shell (§7.1.5, §7.2)."; §8.0.2: "The eight body diagonals of the boundary cube R²≤6, that is the points (±1,±1,±1)"; §8.2(III): "In this version, N_str=89 (structure count in §7.2) and N_core=82 (core construction in §8.1) are locked, so the residual is 7. This matches the minimality result"; §7.2.2: "N_p:=82+7=89."; §8.1.3.2: "The point |y|=0 (the center point) is excluded by default in this section."

**Evidence.** (i) If the +1 in 82 and the 1 in 7 are the same nozzle, the core ∪ shell has at most 81 + 1 + 6 = 88 distinct points, not 89. (ii) The points (±1,±1,±1) have R² = 3 and are already among the 81 lattice points with R² ≤ 6 (shell counts for R² = 0..6: 1, 6, 12, 8, 6, 24, 24; total 81), so the 'shell' lies inside the core. (iii) 89 = 3·29 + 2 leaves a residual of 2, which contradicts the claim of a single irreducible residual. (iv) N_str is defined in §7.2.2 as 82 + 7, so '89 − 82 = 7 matches' is an identity, not a check. (v) The 81 of R² ≤ 6 includes the origin, while §8.1's algorithmic core excludes the center by default, so the two 'cores' are different point sets.

**Proposed improvement.** Publish explicit coordinates for every core and shell point, with a uniqueness check. Decide whether the nozzle belongs to the core or the shell, and correct 89 if necessary. If the shell is meant to sit outside R² ≤ 6, give its coordinates. Delete §8.2(III) or base it on an independently derived N_str. Make §8.1's center convention agree with the 81-point count.

### 10. [major] §8.4 electron emission: the charge-sign convention contradicts ch14, and the implied baryon/lepton-number violation is never tested

- **category:** physics-validity
- **location:** 08-discrete-proton-structure-82-7 §8.4 (header, §8.4.1.5, §8.4.2.2); cross-ref 14 §14.0.4, status list

**Quote.** §8.4: "The electron is the ejected complement of a completed proton — its charge label comes with the ejection."; §8.4.1.5: "\texttt{ELECTRON}, & q(\mathbf{V}_{\mathrm{surv}})=+1"; ch14: "quantized to one unit (proton: net +1 at the nozzle; electron: -1)"; ch14: "γ→ p^++e^- is forbidden in the Standard Model (baryon and lepton number) but allowed here, since only charge/L_z is conserved."

**Evidence.** §8.4 labels q = +1 as ELECTRON, while ch14 gives the electron −1, so the sign conventions contradict each other. The emission (the electron is ejected at t_emit = t_build when the proton completes) has no antineutrino and no lepton-number bookkeeping. ch14 accepts γ → p⁺ + e⁻. By crossing or time reversal, the same vertex allows p + e⁻ → photons (≈ 938.8 MeV), i.e. hydrogen annihilation. Two further consequences follow. A two-body n→p-like emission gives a single-energy electron, which the continuous β spectrum contradicts (the historical evidence for the neutrino). And hydrogen stability is tested directly: water Cherenkov proton-decay searches, with two free-hydrogen protons per molecule, set limits of ≳10³³ yr on modes with GeV-scale electromagnetic final states. No rate is derived, so no comparison is possible.

**Proposed improvement.** Fix the sign: ELECTRON ↔ q = −1, or choose n_Q so that the proton is +1. Either add lepton-number and antineutrino accounting, or state that §8.4 is a bookkeeping label with no dynamical claim. Derive, or at least bound, the p e⁻ → γ rate and compare it with proton/hydrogen-decay limits. Give the energy spectrum of the emitted electron.

### 11. [major] Anchor inputs are graded [F]; 'DOF = 1' leaves out m_e, N, Δt and the locked r_p; §9.4's 'same A' statement contradicts §3.4

- **category:** grading-honesty
- **location:** 09-event-quantum-definition-canonical-event (header chips, §9.4 cross-links); repro/physics/registry/vp_locks.csv; 03 §3.4; 13 §13.5.4

**Quote.** ch9 header: "D = 4.8526 pm — Quantum (anchor) diameter that fixes the lattice length scale. [F] forced."; vp_locks.csv: "anchor,λ_anchor,632.99 nm,Single empirical anchor (DOF = 1); the only measured length input to the framework.,F"; §9.4: "the structural identity D=2πλ/A (with the same A fitting both 633 and 532 nm)"; §3.4: "A₆₃₃/A₅₃₂=λ₆₃₃/λ₅₃₂=633/532 with D cancelling"

**Evidence.** §9.4 sets 'D_anch = 2λ_(C,e)', which requires the measured m_e, and §13.5.4 itself calls this 'an anchor, not evidence'. Under AGENTS.md, both D and λ_anchor are therefore [L], not [F]. The results in §8, §9 and §12 actually use at least m_e (through D), λ_ref = 632.99 nm, N = 10¹² (a convention), Δt = 1.86×10⁻²¹ s (3 significant figures), the locked r_p = 0.8412 fm, the 6/5 channel factor and the bounding-cube measure. That is not DOF = 1. §9.4 says one A fits both wavelengths, while §3.4 requires A₆₃₃/A₅₃₂ = 633/532 for a common D; both cannot hold. With the locked A = 880918.98, 2π·632.99 nm/A = 4.515 pm, which is 7.0% below 4.8526 pm. The A that would reproduce D is 8.196×10⁵.

**Proposed improvement.** Regrade D and λ_ref as [L] in the chapter chips and in vp_locks.csv. List N and Δt as declared conventions/inputs. Replace 'DOF = 1' with a per-result input ledger. Correct the §9.4 'same A' sentence.

### 12. [major] §8.1/§8.3: the construction takes 82 as an input, no parameters or data are shipped, and the shell gates were never run

- **category:** reproducibility-code
- **location:** 08-discrete-proton-structure-82-7 §8.1 header, §8.1.2, §8.1.9, §8.3.5

**Quote.** §8.1: "The 82-core is shipped as data: coordinates, hierarchy, and who touches whom."; §8.1.2: "N_{\mathrm{core}}:=82." and "If any of the above items are not locked, the outputs of this section are undefined and are judged INCONCLUSIVE."

**Evidence.** ALG-CORE82-SELECT takes N_core = 82 as an input and returns 82 points whenever the grid is large enough, so it cannot test the integer. Every parameter (R_p, L_q, d_min, γ_c, h_grid, B, ε_pos, K_max, N₀, K_b, Agg, TB) is marked '(locked)', but no values are given anywhere. The files X82.csv, G82.edgelist, layers82.csv and params82.yaml do not exist in the repository (find returns nothing). No G-SHELL7-6C1S verdict is recorded in the text or in repro/physics/reports. By §8.1.2's own rule, the §8.1–§8.4 outputs are INCONCLUSIVE, yet the chapter grades §8.0 and §8.4 as [F].

**Proposed improvement.** Ship params82.yaml, X82.csv (for example the 81 R² ≤ 6 lattice points plus the nozzle), the contact graph and the G-SHELL7 verdict logs under repro/physics with sha256. Add a test in which 82 is an output, not an input (for example, count lattice points inside a radius derived elsewhere), so that it can fail.

### 13. [minor] Leftovers from the 2+2+4+1 erratum, unexpanded macros in equation alt-text, and section-order and wording slips

- **category:** presentation-rendering
- **location:** 08 §8.2.5, §8.3.6, §8.4.3.1, §8.0.2, §8.0.5(IV); 09 §9.4.1, §9.4.3.2; 12 section order

**Quote.** §8.3.6: "“This shell data satisfies two-pair + one-quad cancellation and non-degenerate survival under the threshold s_(min).”"; §8.4.3.1: "shell_partition: (P1*,P2*,Q*,u*)"; §8.2.5: "The conditions (S08_02_two_pairs) and (S08_02_quad) can admit multiple solutions."; §9.4.1 alt-text: "D_{\mathrm{anch}}=\Danchm, \\ &r_p=\rprotonm"; §8.0.5(IV) alt-text: "\text{\Fm{}}"; §8.0.2: "The eight body diagonals of the boundary cube R²≤6"

**Evidence.** The v0.2.0 erratum (2+2+4+1 = 9 corrected to 2+4+1) did not reach §8.2.5, §8.3.6 or the §8.4.3.1 schema, which still refer to two pairs or P2*. The <img alt> text is the layer that AI and screen readers consume, and in §9.4.1 and §9.4.3.2 it contains undefined macros (\Danchm, \rprotonm), so the locked input values are invisible there. §8.0.5 contains \Fm{}. Literal '[F]{}' and '[H]+{}' braces appear in the running text, and '[H]+' is not in the AGENTS.md grade vocabulary. Eight cube vertices make four body diagonals, not eight, and they lie at R² = 3, not on the boundary of R² ≤ 6. Chapter 12 prints §12.4 and §12.5 before §12.1.

**Proposed improvement.** Fix the stale two-pair/P2* text in §8.2.5, §8.3.6 and §8.4.3.1. Expand the macros in the alt text (D_anch = 4.8526×10⁻¹² m, r_p = 0.8412×10⁻¹⁵ m). Strip '{}' after grade tags and settle on one grade vocabulary. Correct 'eight body diagonals' to 'eight vertices (four body diagonals) at R² = 3'. Renumber chapter 12 in reading order.

**Strengths noted:**
- §8.0.6(C) separates the forced integral from the two definitional maps ([MAP-1]/[MAP-2]) in so many words, which makes it easy to see where the physical hypothesis sits. That is the right structure to keep, with the grade changed.
- The 2+2+4+1 = 9 error is corrected in the open with a version tag and a pointer, instead of being edited away silently.
- §12's G-TE-O1 table shows the unfavourable measures (sphere −47%, jam −67%) next to the favourable one, and the non-reproducible full-simulation evidence was downgraded. This is good epistemic practice to build on.
- §8.5.2's 'Scope' paragraph states plainly that the MD core is amorphous and that 82 = 81+1 holds by construction, not as an MD output.
- vp_numeric_ssot.py regenerates the numbers deterministically, runs a drift gate, and has a residual map that recognizes only two independent residuals (R2 = −R1, R5 = R3+R1). The text should adopt that accounting.
- §9.2 keeps definitions, axioms and theorem clearly apart, states the stationarity axiom explicitly, and makes the conditions for δ = 1/π² (independent uniform phases, product measure) visible.
- §1.9 A3 keeps α_em and the Coulomb overfit out of the coincidence count, which shows a working instinct for look-elsewhere discipline.


## review:light-realization

### 1. [critical] Light is identified with the one mode that is longitudinal; the two transverse polarizations are never derived, and the volume contradicts itself on this point

- **category:** physics-validity
- **location:** docs/physics/sp-jamming-spine-verified-physical-backbone S2.3; docs/physics/11-realization-units-t-rcross §11.6.1; docs/physics/10-implementing-speed-light-clock-free §10.9 (band table); cross-volume: docs/chemistry/01-electromagnetism-jammed-lattice-light EM.4, EM.7, EM.12.4

**Quote.** SP S2.3: "The transverse wave dies; one longitudinal speed survives," | §11.6.1: "That the surviving elastic response is a single longitudinal speed c²=B/ρ is now demonstrated, not asserted" | §10.9: "On the jammed lattice, light propagates as a transverse oscillation of the rotating quanta" ... "χ=90^(∘) (pure transverse) is never reached, since it would require cosχ=0 and leave no longitudinal component with which to propagate." | table: "Gamma | 1fm–1pm | 0.01^(∘)–12^(∘) (quasi-longitudinal)" | chemistry EM.12.4: "it yields the compression (Coulomb/E) sector rigorously but not the independent transverse-vector (magnetic/radiative) sector."

**Evidence.** In an isotropic elastic continuum c_L² = (B + 4G/3)/ρ and c_T² = G/ρ. As G_relaxed → 0 with B finite, c_T → 0 and the only propagating mode left is the irrotational one, u = ∇φ. That mode is scalar, with ONE polarization state per wavevector. Light has two transverse polarizations (helicity ±1) and no propagating longitudinal mode (k·E = 0 in vacuum). So the mechanism the volume verifies (S2.4, five observables) removes exactly the transverse modes light needs and keeps the one mode light lacks. The classical elastic-solid ether theories (Green, MacCullagh, Kelvin's 'labile' ether) needed the opposite limit.

The volume also contradicts itself. SP and §11.6.1 say the transverse wave dies, while §10.9 says light is a transverse oscillation that must keep a longitudinal component (cosχ ≠ 0). Chemistry EM.4 goes further and makes E longitudinal ('the electric field is the force directed along the light (propagation) direction'). The chemistry volume openly grades the radiative transverse sector [O], but that sector is light itself.

Existing data contradict it:
(i) The band table makes 1 fm–1 pm γ-rays quasi-longitudinal. A 961 keV γ-ray (λ = 1.29 pm, so λ/D = 0.266, m = 1, χ = 15.4°) had its circular polarization (helicity) measured in the 1958 Goldhaber–Grodzins–Sunyar experiment. The Crab's 0.1–1 MeV emission shows about 46% linear polarization (INTEGRAL, 2008). A quasi-longitudinal wave has no azimuthal polarization degree of freedom.
(ii) The polarization count sets an absolute number. One polarization gives σ_SB/2 = 2.835×10⁻⁸ instead of 5.670×10⁻⁸ W m⁻² K⁻⁴. The corpus's blackbody check (chemistry EM.7) writes u ∝ ν²(...) and tests only Wien's peak x = 5(1−e^{−x}), which does not depend on the prefactor, so the factor-of-2 test was never run.

**Proposed improvement.** (1) Downgrade 'c² = B/ρ is the speed of light' from [V] to [O] on every card (§10 and §11 headers, SP, hub, AGENTS). Add a plain statement: 'the substrate currently supports one scalar longitudinal mode; light's two transverse polarizations are not derived.'
(2) Add a gate G-POL that counts the substrate's propagating polarizations at ω > 0. PASS requires exactly 2 transverse and 0 longitudinal.
(3) A constructive route uses the framework's own plenum axiom. 'Void-forbidden' means ∇·u = 0, i.e. B → ∞. That turns the longitudinal sector into an instantaneous constraint, the Coulomb part, much as in Coulomb gauge. The transverse modes that remain would have c² = G_eff/ρ or, since the quanta rotate, a micropolar (Cosserat/MacCullagh) rotational modulus: c² = κ/I. Derive that speed and its polarization count. This requires giving up G → 0 at isostaticity as the mechanism for light.
(4) Add the absolute Stefan–Boltzmann constant as the falsification test of the polarization count. Delete the 'quasi-longitudinal γ' row or confront it with γ-ray polarimetry.

### 2. [critical] 'c is derived' does not hold: c's SI value enters through c_ref, c_env = c_ref is an identity, the length anchor is itself c/f, and unbounded stiffness would give c = ∞

- **category:** circularity
- **location:** docs/physics/11-realization-units-t-rcross §11.1, §11.2.1, §11.3.3; docs/physics/10-implementing-speed-light-clock-free §10.6; docs/physics/01-governance-no-tuning-lock-gate §1.8.1, §1.9 A1; docs/physics/w5-anti-circular-logic-chain-light W.5.1; docs/physics/ea-epistemic-audit-log v35

**Quote.** §1.9 A1: "Resolved [F]. ... The non-trivial content is that c_env comes out equal to c_ref; the framework does not assume this, it shows it (§11.6)." | §11.1.4.1 (prohibited): "After computing an internal-derived c or realized c, writing a justification statement that uses agreement with c_ref as a basis." | §11.3.3: "c_ref := ℓ_eff/Δt" with "ℓ_eff := A·a" | audit v35: "an independent measurement of percolation propagation speed c_env against the stiffness K=A²" | W.5: "the lattice is treated as having unbounded local stiffness. This is what makes c a derived, not assumed, output." | §11.2.1: "λ_ref = 632.99121257859865746 nm"

**Evidence.** (a) §11.3 defines c_ref := A·a/Δt, and the realized speed is c := (a/Δt)·c̃ = c_ref·c̃/A. The audit log sets K = A², so c̃_env = √K = A and c_env(SI) = (a/Δt)·A = c_ref identically. The 'agreement' is a definition, and A1 is exactly the use that §11.1.4.1 forbids (FAIL-CREF-PREDICT).
(b) λ_ref is c divided by the CIPM iodine-stabilized He–Ne frequency, f = 473 612 353 604 kHz. Computing c/f gives 632.99121257859865746054 nm, identical to λ_ref to all 20 digits. So the 'single length anchor' is c_ref divided by a clock measurement referenced to the Cs second. It follows that Δt = A·a/c_ref = A/(N·f) = 880918.98/(10¹²·4.736×10¹⁴ Hz) = 1.86×10⁻²¹ s. c_ref cancels, and Δt is (A/N) times the He–Ne optical period (2.111×10⁻¹⁵ s). 'No external clock assumed' is therefore not true.
(c) The CIPM relative uncertainty is 2.1×10⁻¹¹, so only about 11 digits of λ_ref are meaningful.
(d) With B → ∞ at finite ρ, c = √(B/ρ) → ∞. A finite c needs finite contact stiffness. The released code uses 'harmonic soft-sphere overlaps' (U = ½Σov², i.e. k = 1), so c̃ = a√(k/m) is set by the chosen k/m. The DOF ledger lists neither k/m nor this dependence.

**Proposed improvement.** (1) Rewrite A1 to say: 'c is an input (c_ref). The framework claims only that the lattice supports a single signal speed; its SI value is not derived.' Grade it [INPUT]/[L], and apply the framework's own FAIL-CREF-PREDICT label to A1 and to the W.3 row 'their agreement is a result'.
(2) Drop 'clock-free' from the §10 title, or define it honestly as applying to the dimensionless c̃ only.
(3) Declare the contact stiffness ratio k/m (B/ρ in lattice units) as an input, and reconcile it with the infinite-rigidity axiom (S2.1, W.5).
(4) Record λ_ref as c/f_ref with 11 significant figures and u_r = 2.1×10⁻¹¹.

### 3. [critical] No dispersion relation or preferred-frame test: any discreteness scale the volume names is excluded by high-energy photon data, and the isotropy premise of §18.2 conflicts with §10.9's lattice axis

- **category:** missing-test-or-prediction
- **location:** docs/physics/10-implementing-speed-light-clock-free §10.9 (band table), §10.9.2 (G-ISO); docs/physics/11-realization-units-t-rcross §11.2; docs/physics/sp-jamming-spine S2.4; docs/physics/axk Appendix K.3; docs/physics/18-time-and-gravity §18.2

**Quote.** §10.9 table: "Gamma | 1fm–1pm | 0.01^(∘)–12^(∘) (quasi-longitudinal)" | §10.9.2: "The committed angles of §10.9.1 presuppose a lattice/anisotropy axis." | §18.2: "the jammed medium's rest response is isotropic" | SP S2.4 table: "ω^{*}∝Δ z→ 0(τ→∞) | vibrational spectrum" | App. K.3: "The continuum acoustic model is reliable for Kn_λll 1, and breaks down (strong kinetic attenuation / non-continuum behavior) as Kn_λ→ O(1)."

**Evidence.** (a) Zone edges. The corpus itself uses the chain dispersion ω = 2√(k/m)|sin(qa/2)|. The zone-edge photon energy πħc/L is 0.979 TeV for L = a (0.633 am), 1.11 MeV for ℓ_eff = A·a (0.558 pm), and 128 keV for D (4.85 pm). LHAASO (2021) detected photons up to 1.4 PeV, about 1430 times the a-zone edge.
(b) The volume's own Knudsen gate. λ(1.4 PeV) = 8.9×10⁻²² m, so Kn = a/λ ≈ 715. By Appendix K's criterion, continuum propagation should have broken down.
(c) GRB 090510 (z = 0.903, comoving distance ≈ 3.15 Gpc, ≈ 3.2×10¹⁷ s of travel). For its 31 GeV photon, qa = 0.0994 and 1 − v_g/c = 1.24×10⁻³, giving a delay of ≈ 4.0×10¹⁴ s (≈ 13 Myr). The observed delay is ≲ 1 s.
(d) §10.9 puts 1 fm–1 pm γ-rays on a D = 4.85 pm chain with m = 1, i.e. wavelengths far below the lattice unit.
(e) SP uses ω* → 0 as a verification observable. In the jamming literature it cites, modes above ω* are not plane waves (boson-peak/diffuson regime). At the claimed isostatic operating point there is then no ballistic regime at finite frequency.
(f) Preferred frame. §18.2 forces √(1−v²/c²) using an isotropic rest response, while §10.9 needs an anisotropy axis. Optical-cavity Michelson–Morley tests bound Δc/c at about 10⁻¹⁷–10⁻¹⁸.

**Proposed improvement.** (1) Add a subsection that states the VP-wave dispersion relation ω(k) and names which length (a, ℓ_eff or D) is the discreteness scale for light.
(2) Pre-register a gate G-DISP that confronts it with Fermi-LAT GRB 090510 and LHAASO 1.4 PeV. This is the kind of kill test the framework says it wants.
(3) Resolve the conflict between the isotropy premise (§18.2) and the anisotropy axis (§10.9), and give G-ISO a quantitative bound against cavity experiments.
(4) Until both gates pass, grade 'light = c² = B/ρ wave' [O].

### 4. [major] The locked A = 880918.977… (80 digits) is c·Δt/a back-computed from Δt = 1.86e-21 s; §11.3 runs the dependency backwards, and the symbol A carries at least four different values

- **category:** circularity
- **location:** docs/physics/11-realization-units-t-rcross §11.3 (header, [D-11.3-3], §11.3.3–11.3.4); docs/physics/axc-archive-schema-file-tree C.3; repro/physics/tools/vp_numeric_ssot.py; docs/physics/w0-result-scorecard W.3.2; docs/physics/10-implementing-speed-light-clock-free §10.3.5.1, §10.5

**Quote.** §11.3 header: "The tick follows from the amplification; $cΔ t/a=A$ closes exactly." | "A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599." | schema C.3: "inputs": { "a_m": 6.3299121257859865746e-19, "dt_s": 1.86e-21, | SSOT tool: DT     = D("1.86e-21"),                    # Δt (3 유효숫자, realization) | W.3.2: "| A=880918.977… | [V]/[H] | ... | measured from the lattice (a_med/g^*), not a free fit"

**Evidence.** Computing c·(1.86×10⁻²¹ s)/a gives 880918.97770344000000074873389538365909152024492565003100802687690543842580063599281…, identical to the locked A in all 80 printed digits. The realization_lock schema and the SSOT generator both treat Δt = 1.86e-21 (3 significant figures) as the INPUT. So:
- '§11.3 Deriving Δt = A·a/c_ref' reverses the actual dependency, and 'closes exactly' is a tautology.
- A_geo = cΔt/a is not an independent anchor; it is the chosen Δt re-expressed.
- The 80 digits carry 3 significant figures of information.

The A that fixes D is a different number: 2πλ_ref/D = 819,598.63. That is 7.48% below A_lock; using A_lock instead would give D = 4.5148 pm. The measured A_med(N=200) = 8.02×10⁵ is −8.96% from A_lock and −2.15% from 2πλ/D.

The symbol A also denotes:
- Amp(G_throat, B, F) in §10.5;
- the occupancy ratio κ_bb, formerly also called A (§10.3.5.1);
- a_med/g*, which is N-dependent (§10.3.11).

The chapter's own G-SYM gate ('no conflicts in symbols') would fail.

**Proposed improvement.** (1) Relabel Δt = 1.86×10⁻²¹ s as a declared [INPUT] with 3 significant figures, state where it historically came from, and write A_Δt := cΔt/a = 8.81×10⁵ (DERIVED, 3 s.f.).
(2) Rename the distinct quantities: A_D := 2πλ/D = 8.196×10⁵; A_Δt := cΔt/a = 8.809×10⁵; A_SOC(N, g0) := a_med/g*. State which one enters each formula.
(3) Remove the claim that one measured number corroborates both A_D and A_Δt.
(4) Correct the W.3.2 row that calls 880918.977… 'measured from the lattice'.

### 5. [major] The 'measured' amplification A_SOC is the declared threshold g0 and the box size N restated; the 0.16% match is inside statistical noise and uses a switched statistic

- **category:** numerology-look-elsewhere
- **location:** docs/physics/11-realization-units-t-rcross §11.6.1, §11.6.5 (measured-value robustness; empirical table); docs/physics/10-implementing-speed-light-clock-free §10.2.2–10.2.4, §10.3.11; docs/physics/sp-jamming-spine S3; w0 W.3.2 (g₀ row)

**Quote.** §11.6.5: "N=200 gives A_med=8.02×10⁵ (83 avalanches; p10–p90 4.4–21×10⁵)" ... "hence A N^(-1/3), while the pinning ratio g^*/g₀ stays near unity (1.14 at N=200, 1.24 at N=750)" ... "the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%" | §10.3.11: "A_(pred)≈ 5.684e+05 (relative error 1.63e-03)" | W.3.2: "g₀=2×10⁻⁷ | [H] | SOC input (declared) | chosen threshold" | §10.2.2.1: "the contact graph edges are the single source of truth (SSOT) for throat candidates"

**Evidence.** (a) For N monodisperse spheres at φ_jam = 0.633 in a unit box, the contact diameter is d = (6φ/πN)^{1/3}: 0.1822 at N = 200 and 0.1173 at N = 750. Using the declared g0 = 2×10⁻⁷ and the reported g*/g0 values, d/g* = 7.99×10⁵ and 4.73×10⁵. The measured A_med are 8.02×10⁵ and 4.76×10⁵, agreeing to 0.4% and 0.8%. So A_SOC ≈ d/(1.2·g0): its magnitude is fixed by the chosen g0 (SP concedes 'A ∝ 1/g_0') and by N (§11.6.5 concedes A ∝ N^{-1/3}).
(b) In the physical limit N → ∞ at fixed g0, A → 0 and D = 2πλ/A → ∞. The N = 200 closeness to 8.2×10⁵ is therefore a box-size coincidence.
(c) Under §10.2's own definitions (E_th := E_c, g_ij = max(0, d_ij − d0)), contact edges have g_ij ≈ 0 up to the contact tolerance. That makes g_c bounded by a locked input, which is why g*/g0 ≈ 1.
(d) Statistics. A p10–p90 range of 4.4–21×10⁵ implies a lognormal σ ≈ 0.61 and a relative standard error of the mean of ≈ 6.6% for n = 104. A 0.16% 'match' is well inside that noise.
(e) Switched statistic. N = 200 is compared by median, N = 750 by mean. The N = 750 median (4.764×10⁵) is −16.0% from A_lock·(200/750)^{1/3} = 5.670×10⁵.
(f) The quoted A_pred = 5.684×10⁵ implies N_ref = 201.5 rather than 200; with 200 the deviation is 0.40%.

**Proposed improvement.** (1) List g0 (in units of the particle diameter) and N_sim as inputs in the DOF ledger.
(2) Run g0 ∈ {1, 2, 4}×10⁻⁷ and N ∈ {200, 750, 2000, 5000}. Publish A(g0, N) with bootstrap CIs and an N → ∞ extrapolation.
(3) Pre-register which statistic (mean or median) is compared.
(4) Stop citing the 'jamming route' (the 4.8542 pm best avalanche) and the 'A_geo 0.16%' as independent corroboration of D or Δt.
(5) Grade A's magnitude [O] (input-determined).

### 6. [major] The operational ρ_eff (drift probe) cannot measure inertia: its stated dimension is wrong, a rigid translation is a zero mode, and it is not the quantity the [V] modules compute

- **category:** math-error
- **location:** docs/physics/10-implementing-speed-light-clock-free §10.1.2, §10.1.3.3, §10.1.4.1–10.1.4.3, §10.1.5.1, §10.9.1 (setup)

**Quote.** "Define the drift parameter u∈(-u_(max),u_(max)) as a dimensionless probe." | "The dimension of ρ_eff is locked as energy·time²/length⁵" | "Define the relaxation cost (energy unit) as follows. The unit energy U_lat is a locked reference energy unit via realization_lock, and the update weight ω_upd(k) is locked via analysis_lock." | §10.9.1: "The medium is specified only by density ρ=1 (the sole inertial property), perfect elasticity, stiffness B=c², zero friction"

**Evidence.** (a) Dimension. With u dimensionless and W_drift an energy, ρ_eff = V0⁻¹·d²W/du² has the dimension energy/length³, the same as B_eff, not the stated energy·time²/length⁵. The missing (time/length)² is exactly c². So c̃² = B_eff/ρ_eff is a ratio of two static stiffnesses and contains no kinematic information.
(b) Physics. T_u translates every coordinate rigidly, so every d_ij is unchanged. With the periodic boundaries the released code uses (pbc(d, L)), no relaxation update is needed: W_drift ≡ 0, ρ_eff = 0, and FAIL-C-RHO-NONPOS fires by construction. With fixed walls the probe measures wall-contact stiffness instead. No static configuration cost can yield inertia.
(c) W is a weighted count of discrete updates. It is piecewise-constant in ε, so d²W/dη² at η = 0 is either 0 or undefined.
(d) The symmetric B estimator needs η₋ = −η₊ (dilation). Dilation opens one-sided harmonic contacts (W = 0 for η < 0) and creates voids that the plenum axiom forbids.
(e) The actually executed modules use harmonic energies, with ρ set by hand to 1. The [V] tag on c² = B/ρ therefore attaches to a different definition than the one this chapter 'locks'.

**Proposed improvement.** (1) Replace §10.1.4 with a kinetic definition, ρ_eff := V0⁻¹·∂²K/∂v², with a declared VP mass as an input. Alternatively, measure c̃ directly from time-of-flight or from the long-wavelength slope of ω(q) from the dynamical matrix, and take B_eff from the Hessian (Born minus non-affine).
(2) Correct the dimension statement.
(3) Say explicitly which estimator the bundle implements and mark the §10.1 probes as unimplemented specification.

### 7. [major] 'Simulation-validated to 0.06%' is the discretization dispersion of a 1-D chain with c set as input; the G-LIGHT-MAP-Q checks are algebraic identities, and the negative control is hard-coded

- **category:** grading-honesty
- **location:** docs/physics/10-implementing-speed-light-clock-free header card and §10.9.1 (Gate G-LIGHT-MAP-Q; negative control); docs/physics/11-realization-units-t-rcross header card; AGENTS.md §2; docs/chemistry/01-electromagnetism-jammed-lattice-light EM.2; repro/eye/inherited/vp_light_emergence_quantum.py

**Quote.** card: "c² = B/ρ — Speed of light as the lattice elastic-wave speed (bulk modulus over density); simulation-validated. [V] verified." | chemistry EM.2: "The energy centroid propagates at c₍measured) = 0.99940 versus the closed form c₍theory) = a√(k/m) = 1 — a 0.06 % agreement." | §10.9.1: "A standard scalar continuum wave on the same medium (ρ=1, B=c², friction 0), launched at the same angle χ, measures transverse wavelengths 6.750D and 14.250D" | repro: "def emerge_wave_quantum(N=2000, sigma=18.0, steps=600):" and "continuum = 1.5*chain              # generic scalar continuum (paper: 6.75D,14.25D)"

**Evidence.** (a) Where 0.06% comes from. On a nearest-neighbour chain, a Gaussian packet of width σ sites has an energy-centroid speed ⟨cos(qa/2)⟩ ≈ 1 − 3/(16σ²). Computed: σ = 18 gives 0.99940 (deficit 0.0598%); σ = 5 gives 0.746%; σ = 100 gives 0.0019%. The script uses sigma = 18.0 with c = 1.0 hard-set and an assert tolerance of 5%. So '0.06%' reflects the chosen packet width, not a validation precision.
(b) 'c² = B/ρ verified to machine precision' is an identity: in 1-D, B = ka and ρ = m/a, so B/ρ = ka²/m ≡ c².
(c) The 1-D chain has no disorder, no contact network, no isostaticity and no transverse sector. It tests nothing specific to the jammed vacuum.
(d) G-LIGHT-MAP-Q:
- (2) |m·sinχ·D/λ − 1| < 1e-7 restates the definition sinχ = λ/(mD).
- (3) The ratio 1.189831 = 632.99/532 by construction.
- (4) 'Phase speed = c' follows from the inputs B = c², ρ = 1.
- (5) The negative control is a multiplication by 1.5 (6.75/4.5 = 14.25/9.5 = 1.5 exactly), not a simulation.
(e) The framework defines [V] as 'passed a test built to falsify it against external data'. None of these checks can fail.

**Proposed improvement.** (1) Remove 'simulation-validated to ~0.06%' from AGENTS, the homepage, the chemistry abstract and the physics cards; call the 1-D run a code sanity check.
(2) Add a check that can fail. In the 3-D packings of SP S2, measure c_L and c_T from the dynamic structure factor versus Δz, and compare with √((B + 4G/3)/ρ) and √(G/ρ) taken from the Hessian. Report the Ioffe–Regel frequency.
(3) Re-label G-LIGHT-MAP-Q as a determinism/integrity gate, not [V], and replace the hard-coded control with an actual continuum simulation.

### 8. [major] The light-angle 'prediction' is undetermined at the volume's own D precision, depends on rounded inputs, misstates its range, and is graded [F]+[V] while G-ISO is open

- **category:** grading-honesty
- **location:** docs/physics/10-implementing-speed-light-clock-free §10.9 (master formula, band table, falsifiable-prediction para), §10.9.1 (result table, setup, derived tick); docs/physics/03-axioms-primitives §3.4

**Quote.** §10.9 box: "[F]+[V] light angle" | "Because m≥ λ/D by construction, sinχ≤ 1 holds automatically; χ=90^(∘) (pure transverse) is never reached" | "Visible | 380–750nm | 89.8^(∘)–89.9^(∘) (near-transverse)" | "a 0.03% change in D shifts the visible-light angle by more than a degree" | §10.9.1: "(λ/D)₆₃₃/(λ/D)₅₃₂=1.189831=633/532 cancels D and any mass scale — the relative mapping is anchor-free and falsifiable" | "No mass value enters the dynamics anywhere" | "τ_q:=D/c=2h/(mₑc²)" | §3.4: "D is pinned to only 0.04%"

**Evidence.** (a) χ is a sawtooth in λ/D with period 1, i.e. Δλ = D = 4.853 pm (7.67 ppm at 633 nm). §3.4 gives D only to 0.04%, so λ/D is uncertain by about ±52 integers. The 7% ℓ_rot spread covers about 9131 periods. Either way χ is smeared over [89.776°, 90°], and the committed 89.9378° carries no information.
(b) The inputs are rounded. At the anchor's full value, 632.99121 nm, χ = 89.7960° (the text itself concedes this). The 532.0 nm used is not the iodine-stabilized Nd:YAG line, 532.245036 nm, which gives λ/D = 109681.98 and χ = 89.9680°. A He–Ne laser's wavelength in air (632.816 nm) gives 89.781°.
(c) 'Never reached' is false: whenever λ/D is an integer, sinχ = 1 and χ = 90°. Sampling 380–750 nm gives 89.711°–89.9998°, not 89.8–89.9°. The X-ray row also reaches 90° at every λ = kD.
(d) The 'falsifiable' ratio 1.189831 is 632.99/532, the ratio of the two input wavelengths, so it cannot fail.
(e) 'Mass-free' is misleading: D = 2h/(m_e·c), so the sole input λ/D = λ·m_e·c/2h.

**Proposed improvement.** (1) Re-grade §10.9 [O]: G-ISO is open and no observable or axis is defined.
(2) Restate the prediction as a distribution. With D uncertain, frac(λ/D) ~ U(0,1) and cosχ ≈ √(2(m − λ/D)/m). Say what an experiment would actually measure.
(3) Use metrological vacuum wavelengths with their uncertainties.
(4) Delete 'χ = 90° never reached', correct the visible range, drop 'mass-free', and remove the ratio-identity 'falsifier'.

### 9. [major] RCROSS has never been run or reported, and its channel definitions contradict each other; as written it is either a tautology or it fails

- **category:** internal-inconsistency
- **location:** docs/physics/11-realization-units-t-rcross header, 'Declaration of the cross-validation system', §11.4.2–11.4.7; docs/physics/03-axioms §3.4; docs/physics/09 §9.4 cross-links; docs/physics/10 §10.9 ('Why the 633 nm mapping works'); docs/physics/w0 W.3 gate table; docs/physics/axc C.3

**Quote.** §11: "No single anchor decides anything: two channels or no conclusion." ... "If RCROSS is not PASS, realized values do not have the status of conclusions." | rcross_report: "dt_633: ... dt_532: ..." | W.3: "| Δ t (time tick; realization) | ... | UNLOGGED |" | §3.4: "the cross-consistency reduces to A₆₃₃/A₅₃₂=λ₆₃₃/λ₅₃₂=633/532 with D cancelling" | §10.9: "The same amplification A (hence the same D) reproduces the relation at both 632.99 and 532nm" | §9.4: "with the same A fitting both 633 and 532 nm" | C.3: "lambda_ref_nm": [633.0, 532.0]

**Evidence.** Nowhere in the physics text or repro/physics are there numerical values for dt_633, dt_532, dev or dev_max. The W.3 table lists the a and Δt gates as UNLOGGED. By the chapter's own rule, a and Δt therefore have no conclusion status, yet the chapter carries an [F] badge.

The channel definitions are mutually exclusive:
- §3.4 makes A_k ∝ λ_k (a tautology once A_k := 2πλ_k/D).
- §10.9 and §9.4 say one A fits both wavelengths, which would force D to differ by 19% between channels.

Under the framework's own relations:
- common a with A_k ∝ λ_k gives Δt^(k) ∝ λ_k and dev = 0.173;
- a_k = λ_k/N gives Δt^(k) ∝ λ_k² and dev = 0.344;
- dev = 0 only if both channels are given the same A and a, which is not a test.

The lock schema also stores 633.0 nm, whereas §11.2 uses 632.99121… nm.

**Proposed improvement.** (1) Specify a quantity that each channel measures independently and that could disagree.
(2) Set dev_max numerically before running, and publish rcross_report.json with manifest and checksums.
(3) Until then, mark a and Δt as [INPUT], remove 'RCROSS two-wavelength sealing' from W.3.2, and change the chapter badge from [F].
(4) Reconcile §3.4 with §9.4/§10.9.

### 10. [major] The split integer N = 10¹² is an undeclared degree of freedom; the N-invariance table leaves out the one output that depends on it, and the Higgs match is what chance predicts

- **category:** numerology-look-elsewhere
- **location:** docs/physics/11-realization-units-t-rcross §11.2.1 [D-11.2-2]; docs/physics/01-governance §1.8.1–1.8.2; docs/physics/w5 W.5.4; docs/physics/w0 W.3.2 (N row)

**Quote.** §11.2: "N is a dimensionless integer ... N is locked in analysis_lock and cannot be changed after seeing the result." | §1.8.2 table: "m_H/U_lat | 1/(5π) | 1/(5π) | 1/(5π)" ... "Confirmed by the released code; no N enters the closure equations." | W.3.2: "N=10¹² | [H] | (declared split integer) | a chosen split; no dimensionless output depends on it (§1.8.2 N-invariance)" | W.5.4: "The number 1958.7 GeV (for U_lat=hc/a) is then divided by the pure geometric factor 5π"

**Evidence.** a = λ_ref/N, so U_lat = hc·N/λ_ref and m_H = U_lat/(5π) ∝ N. N = 10¹¹, 10¹² and 10¹³ give m_H = 12.47, 124.7 and 1247 GeV. m_H/m_p = 132.90 × (N/10¹²) is dimensionless and depends on N, contrary to W.3.2. The §1.8.2 row m_H/U_lat = 1/(5π) is N-free by definition. The DOF ledger ('exactly one') leaves out N, the choice of laser line and the coefficient family.

Look-elsewhere estimate. Take 14 common laser lines (325–1550 nm), 21 coefficients n·π^j (n = 1–7, j = 0–2) and a free power of ten: 294 combinations. The chance per combination of landing within ±0.4% of 125.20 GeV is 2·ln(1.004)/ln(10) = 0.35%, so about 1.04 hits are expected. Enumeration finds exactly one (632.99 nm, 5π, N = 10¹²). P(at least one hit) ≈ 0.65.

**Proposed improvement.** (1) Add N, the line choice and the coefficient family to the §1.8.1 DOF ledger.
(2) Replace the N-invariance row with m_H/m_p, showing its linear N-dependence.
(3) Report the look-elsewhere p ≈ 0.65 next to the −0.40% residual.
(4) Either derive N = 10¹² from the lattice (e.g. a geometric count), or grade m_H [H]/coincidence.

### 11. [major] Header cards and chapter badges contradict the section-level grades

- **category:** grading-honesty
- **location:** docs/physics/10-implementing-speed-light-clock-free header (badge + cards); docs/physics/11-realization-units-t-rcross header (badge + cards); docs/physics/sp-jamming-spine S5 ledger

**Quote.** §10/§11 header: "Grade [F] forced." | card: "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." | cards: "ν_p = 3π⁴ — Canonical proton event-rate from the n-fold law ν_n = nπ^(2(n−1)). [F] forced." and "m_p/m_e = 6π⁵ — ... [F] forced." | SP S5: "ν_p=3π^{4};m_p/m_e=6π^{5};D/r_p=6π^{6} | [D] | one definition textsc[MAP-1]"

**Evidence.** - An empirical input cannot be 'forced'; λ_anchor needs an [INPUT]/[L] tag.
- ν_p and 6π⁵ are carded [F], but the Jamming Spine ledger grades them [D] (they rest on one definitional identification, MAP-1).
- The §10 and §11 chapter badges read [F], while their load-bearing contents are Δt [H], N [H], A [V]/[H], §11.6.2–3 [H], §10.9.1 [V]+[H], and a gate table showing UNLOGGED.
- The card 'c² = B/ρ [V]' conflicts with the [O] status of the transverse radiative sector (see the polarization finding).
- The card 'D = 4.8526 pm [F]' conflicts with §3.4, which calls D 'a single anchored constant' equal to 2λ_C,e, i.e. m_e is an input.

These cards are what readers and AI summaries see first. AGENTS §5 forbids silent upgrades, so this matters.

**Proposed improvement.** (1) Generate every card from one grade registry (repro/physics/registry/vp_locks.csv).
(2) Add a gate that fails when a card's grade differs from the section ledger.
(3) Set each chapter badge to the weakest load-bearing grade, and introduce an [INPUT] tag for anchors.

### 12. [major] §11.6.3 misdescribes Appendix K: the air 'cross-check' takes v_s as an input and cannot rule out circularity

- **category:** grading-honesty
- **location:** docs/physics/11-realization-units-t-rcross §11.6.3; docs/physics/axk-methodological-validation-via-classical-gas K.2–K.5

**Quote.** §11.6.3: "reproduces c_sound,air within the expected order of magnitude" ... "It does, however, falsify the alternative reading that the c²=K relation is a circular reuse of the speed of light." | App. K.2: "We use representative macroscopic inputs $v_s \approx 343\,\mathrm{m/s}$" ... "K.2.1 Step 1: Temperature from sound speed" | K.5: "It does not by itself prove any specific VP lattice value"

**Evidence.** Appendix K reproduces nothing about sound speed. It takes v_s = 343 m/s as an input, infers T = 293 K from it, and then infers λ_mfp ≈ 66 nm from viscosity. It is a textbook kinetic-theory inversion. Nothing computed for air can bear on whether c_light was reused in §11.3, where c_ref := A·a/Δt is used by definition. Appendix K itself limits its claim to a 'methodological' one. Its Knudsen criterion actually works against the framework (see the dispersion finding).

**Proposed improvement.** (1) Delete the 'falsify ... circular' sentence and describe Appendix K as a methodological analogue in which v_s is an input.
(2) If an air test is wanted, predict v_s out of sample from a declared jammed-packing model with stated inputs and report the residual.

### 13. [major] 'Stiffness forces the radius' (§11.6.4): the value 2/π is put in by normalizing the inflow coefficient; the comparison also uses a superseded CODATA value

- **category:** physics-validity
- **location:** docs/physics/11-realization-units-t-rcross §11.6.4 ('Why the forced balance lands at 2/π'; 'What is, and is not, doing the work'); docs/physics/sp-jamming-spine S4

**Quote.** "Writing the rectified stiffness αx⁻⁵ against the inflow x⁻⁴ (inflow coefficient normalised to unity), the equilibrium αx⁻⁵=x⁻⁴ forces x^*=α, i.e. rₚ/λ_(C,p)=2/π." | "the exponents -5,-4 fix only that equilibrium occurs at the stiffness-to-inflow coefficient ratio" | SP S4: "(CODATA charge radius0.8414fm,-0.02%)"

**Evidence.** Write the two terms with general coefficients, S·x⁻⁵ = I·x⁻⁴. Then x* = S/I, and with x measured in λ_C,p the result r_p = (2/π)λ_C,p is equivalent to assuming I·λ_C,p = S/α. The value comes from the normalization, not from the dynamics. Global stability (F′(x*) = −(π/2)⁵) says nothing about where the fixed point sits. The predicted (2/π)λ_C,p = 0.841236 fm. Against CODATA 2022, r_p = 0.84075(64) fm, the residual is +0.058% (0.76σ), not '−0.02%' against the superseded 0.8414 fm.

**Proposed improvement.** (1) Grade the numerical value [H]: 'hypothesis: the inflow coefficient equals the stiffness coefficient/α in λ_C,p units'. Alternatively, derive the inflow coefficient from the lattice.
(2) Keep [F] only for the existence and stability of the fixed point.
(3) Update the comparison to CODATA 2022.

### 14. [major] The manual calls the substrate 'random close packing φ ≈ 0.7405'; that is crystalline FCC packing, and it contradicts the measured φ_jam = 0.633 and the G → 0 mechanism

- **category:** cross-volume
- **location:** AGENTS.md §1 TL;DR and §6 catalog row 4; docs/index.html (chemistry card); vs docs/physics/11-realization-units-t-rcross §11.6.5 (empirical table); docs/physics/rf-read-first code comment

**Quote.** AGENTS §1: "Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405)." | homepage: "φ_RCP = 0.7405" | §11.6.5: "Jamming point | φ_jam=0.633, z→6 isostatic" | rf: "If phi self-organises to random-close-packing (~0.64) with contacts <z> -> 6"

**Evidence.** π/√18 = 0.74048 is the FCC/HCP crystalline close-packing fraction; chemistry CH.13 labels it correctly. Random close packing is ≈ 0.64, and physics measures 0.633. An FCC packing is hyperstatic (z = 12 > 2d = 6), so its shear modulus is finite and transverse waves survive. That is the opposite of the isostatic G → 0 mechanism the physics volume relies on. The main AI manual and the homepage therefore describe a substrate that is inconsistent with the physics.

**Proposed improvement.** Correct the headline in registry/vp.manifest.json to 'φ_J ≈ 0.64 (measured 0.633, isostatic z = 6)', then regenerate AGENTS.md, the homepage, llms.txt and the JSON-LD from it, as §9.4 of AGENTS prescribes.

### 15. [minor] Lost tildes make sentences meaningless; unexpanded macros in alt text; symbol collisions

- **category:** presentation-rendering
- **location:** docs/physics/10-implementing-speed-light-clock-free/index.html §10.1.7.1 (line 186), §10.7 (line 81), §10.5/10.6 header chips; §10.9 eq:lightangle_master alt text; docs/physics/11-realization-units-t-rcross §11.1.2, eq phy-11-000 alt text; §10.4.4.1

**Quote.** "In this case c is not defined and c is also not defined." | "All conclusions in this chapter (χ_c, δ_eff, backbone, A, c, c) must be sealed" | "clock-free $c:=(a/Δ t)tilde c$" | alt text "D=\Danchpm" and "a=\aVP" | "configs/thresholds.yaml: d₀,γ_c and percolation/backbone thresholds."

**Evidence.** In the actual HTML prose (not just the text extraction), the tilde on c̃ is lost, so 'c̃ and c' reads 'c and c'. The same happens with x̃/x and ṽ/v in §11.1.2 ('internal velocity v and realized velocity v'). One header chip shows raw 'tilde c'. Equation alt text contains the unexpanded macros \Danchpm and \aVP, which screen readers and AI extractors see. γ_c collides with the corpus-wide γ (the DNA stiffness).

**Proposed improvement.** (1) Render c̃, x̃, t̃, ṽ with a combining tilde (U+0303), or write 'c_int'.
(2) Expand the custom macros in alt text at build time.
(3) Rename γ_c (e.g. to κ_c).

### 16. [minor] Chapter 10 is mostly unexecuted specification; its defined amplification (κ_bb) and gate stack are never computed

- **category:** structure-redundancy
- **location:** docs/physics/10-implementing-speed-light-clock-free §10.1–10.7 (esp. §10.3.5.1 disambiguation, §10.3.6–10.3.10, §10.4.1)

**Quote.** §10.4.1: "This section presents no computational results; it only defines “which file is generated with which role under which conventions, and how it is sealed.”" | §10.3.5.1: "The released percolation code computes A=a_med/g^* (median neighbour spacing over the critical percolation throat), not this occupancy ratio."

**Evidence.** About 880 of the chapter's 1060 lines are lock, gate and file-tree specification. By the chapter's own disambiguation, κ_bb and its G-SS-STAT, G-SS-PIN, G-SS-ROBUST and G-AMP-A stack are never evaluated. The W_iso/W_drift probes of §10.1 are also not what the modules compute. The only numbers in the chapter are §10.3.11 (A scaling) and §10.9 (light angle), which a reader reaches only after the boilerplate. This hides exactly where the physics is weakest.

**Proposed improvement.** (1) Move §10.1–10.7's generic procedure to the governance chapter or an appendix.
(2) Open §10 with: the observable definitions actually implemented, a results table with confidence intervals, and a clearly marked list of open problems (polarization count, dispersion, isotropy, ρ definition).
(3) Delete κ_bb or implement it.

**Strengths noted:**
- §11.1 sets a strong anti-circularity rule: c_ref may anchor units but never justify results, with FAIL-CREF-PREDICT, -SINGLE and -RETRO labels that can be checked from logs. Most of the circularity fixes above only require applying this rule to §1.9 A1 and W.3.2.
- The §10.9.1 'input convention' note openly shows that 632.99 versus 632.99121 nm changes m and χ. Disclosing the hypersensitivity is the right instinct and makes the problems easy to audit.
- §10.9.2 (G-ISO) registers, before any lab claim, the obligation to reconcile the angle prediction with precision propagation data. That is the right structure and only needs quantitative bounds.
- The Jamming Spine (S2.4) correctly reproduces the textbook isostatic-jamming results with five observables (G_relaxed → 0 with B finite, ω* → 0; O'Hern–Silbert–Liu–Nagel, Wyart), with its scope honestly noted.
- The §11.6.5 non-claim note, forbidding use of the numerical closeness of φ_jam ≈ 0.633, 2/π and 632.99 nm, is good anti-numerology practice.
- The §10.2.5 union-find percolation and backbone-extraction algorithms are specified precisely and deterministically, and the §11.3.5 first-order error budget for Δt is correct.
- SP S3 and S5 already concede that 'A is anchored to cΔt/a' and that 'Δt independent of c' is an open loop. Promoting these concessions into the headline grades would make the volume much more consistent.


## review:mass-force

### 1. [critical] Gravity sourced by annihilation rate violates the weak equivalence principle by about 10^11 times the MICROSCOPE bound, or else contradicts 6π⁵

- **category:** physics-validity
- **location:** 14-force-lattice-tension-1-r2 §14.0.4 ('Charge and gravity are decoupled'); cross-ref 17-extensions §17.4.0 ('From annihilation rate to force')

**Quote.** The source strength Q is the annihilation rate: νₚ=3π⁴≈292s⁻¹ and νₑ=1s⁻¹ (§12), consistent with mₚ/mₑ=2πνₚ=6π⁵. ... the proton and neutron share the same 82 core, hence nearly equal mass and identical inflow  ||  (ch.17) Using the framework's mass–rate identity m = 2π · ν_ann

**Evidence.** If the gravitational source is Q=ν (ν_e=1, ν_p=3π⁴) while inertial mass follows m_p/m_e=6π⁵, then Q/m is 1 for the electron and 3π⁴/6π⁵=1/(2π)=0.159 for the proton. Per unit inertial mass the electron gravitates 2π times harder than the proton. Neutrons are given 'identical inflow' to protons even though m_n−m_p=1.293 MeV. For MICROSCOPE's Ti/Pt pair (Z/A=0.458 vs 0.400) I computed η=2Δ(Q/m)/Σ(Q/m)=2.5×10⁻⁴. About 1.7×10⁻⁴ of that comes from the electron term alone, ≈(2π−1)(m_e/m_N)Δ(Z/A). The MICROSCOPE final result (PRL 129, 121102, 2022) is η(Ti,Pt)=(−1.5±2.3±1.5)×10⁻¹⁵, so the prediction is excluded by about 11 orders of magnitude. The escape route does not work either. If ch.17's universal m=2πν_ann holds, then m_p/m_e=ν_p/ν_e=3π⁴=292.2, not 6π⁵=1836.1. The triple {ν_e=1, ν_p=3π⁴, m_p/m_e=2πν_p} forces a non-universal mass-to-rate ratio, and so a composition-dependent gravity.

**Proposed improvement.** Make the gravitational source strictly proportional to inertial mass (Q∝m) and state how ν maps to mass for every species with one universal constant. Then check that m_p/m_e=6π⁵ survives. Add an explicit WEP gate (|η|<10⁻¹⁴ for Ti/Pt and Be/Ti) to the kill criteria of §1.10 and run it. Remove the claim of 'identical inflow' for neutrons, or show that it reproduces m_n/m_p=1.00138.

### 2. [critical] Maxwell's transverse sector contradicts the framework's own verified result that the transverse elastic wave dies (G_relaxed→0); the §14.0.6b source construction is inconsistent

- **category:** internal-inconsistency
- **location:** 14-force-lattice-tension-1-r2 §14.0.6 ('Electric field = VP displacement', 'Source-free Maxwell as a curl-factorization', Lemma), §14.0.6b; cross-ref sp-jamming-spine S2.3 and 11 §11.6.1

**Quote.** Identify mathbf E with the VP displacement field mathbf u. Its longitudinal part (∇·mathbf u, compression = deficit) is the static Coulomb field of §14.0.5; its transverse, propagating part is light  ||  with boldsymbolΨ=mathbf E+iZ₀mathbf H, the single equation i∂ₜboldsymbolΨ=c∇×boldsymbolΨ (∇·boldsymbolΨ=0) yields ∂ₜmathbf E=c²∇×mathbf H, ∂ₜmathbf H=-∇×mathbf E  ||  the momentum balance ρₘ∂ₜ²mathbf u=ρₘ c²∇²mathbf u+mathbf f ... the charge density is the longitudinal compression that the defect maintains, ρ_q∝-∇·mathbf E  ||  (spine) the relaxed (non-affine) shear modulus vanishes,G_{relaxed}→ 0, while the bulk modulusBstays finite ... The transverse wave dies; one longitudinal speed survives

**Evidence.** (1) In an isotropic elastic continuum (Navier–Cauchy, ρü=(λ+μ)∇(∇·u)+μ∇²u+f), transverse waves travel at c_T²=G/ρ and longitudinal ones at c_L²=(K+4G/3)/ρ. The spine and §11.6.1 grade [V] the statement that G_relaxed→0 and that only a longitudinal speed c²=B/ρ survives. That leaves the transverse sector, which ch.14 calls light and which the curl factorization lives on, with zero stiffness: c_T=0, so there is no transverse wave to factor. (2) The momentum balance ρü=ρc²∇²u+f can hold for all u only if λ+μ=0. That gives K=λ+2μ/3=−G/3<0 and c_L=c_T, which contradicts c²=B/ρ>0 with G→0. If it is restricted to u_T, then E=−∂ₜu_T is divergence-free and ρ_q∝−∇·E≡0, so the 'charge conservation as an identity' has no charge in it. (3) The surviving longitudinal mode would be a longitudinally polarized 'light', the failure that sank the 19th-century elastic aethers (Green 1838, MacCullagh 1839, Kelvin's labile aether). Transverse polarization optics and Casimir measurements, which count 2 polarizations at the ~1% level, exclude it. (4) Dimension slip: with Ψ=E+iZ₀H, i∂ₜΨ=c∇×Ψ gives ∂ₜE=(1/ε₀)∇×H and ∂ₜH=−(1/μ₀)∇×E. The stated pair holds only for Ψ=E+icB; [c²∇×H]=A·m⁻⁰·s⁻² does not match [∂ₜE]=V·m⁻¹·s⁻¹.

**Proposed improvement.** State which modulus sets the transverse speed and reconcile it with the G→0 spine, since one of the two must go. For example, use a Cosserat (MacCullagh-type rotational-elasticity) energy ∝|∇×u|², where curl coupling is forced and the longitudinal mode is absent, and show that the jammed packing realizes it. Downgrade 'source-free Maxwell is contained ([F])' to [H] until then. Fix Ψ to E+icB. Turn §14.4 into a real test: compute the Casimir pressure for the full elastic mode spectrum. Any propagating longitudinal mode changes the pressure by O(1), which existing data already constrain.

### 3. [critical] The Higgs 'prediction' scales linearly with an arbitrary decimal split N=10¹² and with a He–Ne metrology laser line

- **category:** circularity
- **location:** 13-mass-u-lat-m-h §13.1, §13.3.7 and chapter card; 11-realization §11.2; 01-governance §1.8.1–1.8.2; rf-read-first; w0 scorecard

**Quote.** λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced.  ||  (ch.11) N = 10^{12} ... a := \frac{\lambda_{\mathrm{ref}}}{N}  ||  (ch.01) | m_H/U_lat | 1/(5π) | 1/(5π) | 1/(5π) ... Confirmed by the released code; no N enters the closure equations.  ||  (rf) the Higgs m_H=hc/(a·5π)=124.7 GeV puts in a length and gets out a mass ... this is “one length in, the Higgs out.”  ||  (w0) a chosen split; no dimensionless output depends on it (§1.8.2 N-invariance)

**Evidence.** m_H=hc/(5πa)=N·hc/(5πλ_ref)=N×0.124695 eV. With N=10⁹ this gives 0.1247 GeV, and with N=10¹⁵ it gives 1.247×10⁵ GeV. The N-invariance table checks only m_H/U_lat, which is trivially N-free, and hides that the one dimension-bearing prediction is directly proportional to N. λ_ref=632.99121257859865746 nm is exactly c/(473 612 353 604 kHz), the CIPM-recommended ¹²⁷I₂-stabilised He–Ne frequency; c/f reproduces all 20 digits. So U_lat=10¹²×E_γ(He–Ne)=10¹²×1.958703 eV, and the Higgs mass becomes 10¹²×(a neon-laser photon energy)/(5π). No physical route is given from a neon discharge line or from powers of ten (a property of the SI decimal system) to the electroweak scale. rf also lists m_H under 'Calibrated (input × structure)' while using it as the non-circular test.

**Proposed improvement.** Either derive N from physics (for example as a counted lattice ratio with its uncertainty) and show it is not tied to base-10/SI conventions, or reclassify m_H as a one-DOF calibration of N·λ_ref and remove it from the anti-circularity argument in rf/W.5. Replace the N-invariance table with one that shows m_H in GeV for each N. Add N and the He–Ne choice to the DOF ledger of §1.8.1.

### 4. [major] 'One energy feeds all masses' is not true: a cancels from m_p, m_e and every force; m_e is a second empirical input; the unification theorem is a tautology

- **category:** grading-honesty
- **location:** 13-mass-u-lat-m-h lede, §13.2, §13.4 status note, §13.5.4, §13.6 [T-13.6-1]; 14 §14.1.2/§14.1.6; 03 §3.4

**Quote.** One energy feeds all masses — defined once, referenced everywhere.  ||  the realization scale a therefore cancels in mₚ=U_lat/Sₚ=hc/λ_C and plays no physical role here. The integral is bookkeeping  ||  The single mass-scale calibration node is the electron: mₑc²=2hc/D_anch  ||  Thus each mass is unified as the outcome of a single lattice energy U_lat differentiated by the object-specific resistance coefficient σ_eff.

**Evidence.** m_p=hc/λ_C and m_e=2hc/D do not depend on a. So does every force: F=F_lat(a/R)²Γ=Γhc/R², and e_map=e. U_lat, and with it λ_ref and N, enters only m_H. D_anch:=2λ_C,e=2h/(m_e c)=4.852620 pm is fixed by the measured electron mass. That is an empirical input independent of λ_ref: λ_ref/D=130443.17, and no relation between them is derived. So the empirical DOF count is at least 2 (λ_ref, m_e), plus the choice of N, not the '1 DOF' in the chapter card and in §1.8.1. T-13.6-1 holds for any mass whatever, because σ_eff is chosen per object (a sum of areas for H, a ratio of lengths for p and e) and is therefore equivalent to defining σ_eff:=U_lat/m.

**Proposed improvement.** Rewrite the lede as: 'U_lat is the Higgs-sector scale; the p and e masses are Compton relations independent of a.' Update the DOF ledger to list m_e (via D_anch) as anchor #2 and N as a declared choice. Present [T-13.6-1] as a definition, not a theorem, or delete it.

### 5. [major] The Higgs miss is 4.6σ, not a 'published residual'; the residual policy makes the claim unfalsifiable, and a look-elsewhere estimate gives p≈0.04–0.16

- **category:** numerology-look-elsewhere
- **location:** 13-mass-u-lat-m-h §13.3.7 ('Measured value comparison', 'No-tuning fingerprint'); 01 §1.10; w0 row m_H

**Quote.** The PDG-tabulated Higgs boson mass is m_H^exp=125.20± 0.11GeV (CODATA/PDG 2024). ... ≈ -4.0×10⁻³ (-0.40%)  ||  A tuning workflow would never accept a 5π that misses by 0.40%; it would migrate to 4.98π.  ||  (ch.01) The following are not legitimate falsifiers: (i) "the closure has a 0.4% residual"

**Evidence.** (124.695−125.20)/0.11=−4.59σ. The prediction's own uncertainty is negligible: λ_ref is known to about 10⁻¹¹. So the [H] closure is excluded unless a theory uncertainty of at least 0.4% was declared in advance, and none was. Refusing to 'migrate to 4.98π' does not show the absence of tuning. The selection happens earlier, in the choice of form: k in U_lat/(kπ), radius or diameter normalization, and N. Look-elsewhere check (seed 19): for a log-uniform target in [60,250] GeV, the family {U_lat/(kπ)}, k=1..12, lands within ±0.40% with p≈0.044. The modest family {U_lat·c/(kπ^j)}, c∈{1,¼,4}, j=0..2, gives p≈0.16. Including N makes p≈1. No gate report exists (w0: 'UNLOGGED'; no gate_report_mH.json in repro/physics).

**Proposed improvement.** Pre-register a theory-uncertainty budget for tree-level 5π, then report the pull, which is a FAIL at the stated precision. Drop residual item (i) from the 'not falsifiers' list. Report the look-elsewhere p-value next to the number. Make the channel logic predict m_W, m_Z, v=246 GeV or m_t, or explain why only the Higgs is a 'cell channel mode'. Ship gate_report_mH.json.

### 6. [major] The factors 5 and π in σ_eff(H)=5π are convention-dependent (normalization, cell size, gauge semantics), not forced

- **category:** physics-validity
- **location:** 13-mass-u-lat-m-h §13.2.4.2, §13.3.2–§13.3.4 (D-13.3-2, D-13.3-4, D-13.3-6, D-13.3-7); cross-ref 03 CELL-CUBE (edge D_anch)

**Quote.** \sigma_{0}^{(k)} := \frac{4\,\sigma_{\mathrm{geom}}^{(k)}}{a^2}  ||  \tilde{\sigma}_{\mathrm{eff}}(\mathcal{O}) :=\frac{\sigma_{\mathrm{geom}}(\mathcal{O})}{L_{\mathrm{ref}}^{2}}, where L_ref is the normalization length (e.g., L_q or a)  ||  For each face f∈F, define that a “channel state variable” (e.g., phase/displacement/update count) is recorded as a real number u_f.  ||  Grade: [F]{} for the geometric factor 5π

**Evidence.** (a) π per channel is just the area of a disk divided by its own radius squared. The chapter's standard form (§13.2.4.2, L_ref=a) gives σ₀=π/4, σ_eff=5π/4 and m_H=498.8 GeV. The factor 4 (L_ref=a/2) is chosen, not forced. (b) The canonical cell is a cube of edge D_anch=4.85 pm, yet each face 'channel' is a single VP disk of diameter a=6.3×10⁻¹⁹ m, about 7.7×10⁶ times smaller than the face. Using the face area would change σ₀ by about 10¹⁴. (c) u_f is left semantically undefined. Under the cube group O_h, the 6 face variables decompose as A1g⊕Eg⊕T1u (1+2+3). For normal displacements the unobservable modes are the rigid translations T1u, leaving 3 (or 2 once breathing is also removed). Only a phase-like u_f singles out A1g alone. Alternative counts give U/(3π)=207.8, U/(2π)=311.7, U/(4π)=155.9, U/(6π)=103.9, 8 vertices−1 → U/(7π)=89.1, 12 edges−1 → 56.7 GeV. (d) The substrate is an amorphous jammed packing (z→6 on average), so a cube is a declared convention (CELL-CUBE), not a geometric fact.

**Proposed improvement.** Define u_f physically, derive which O_h modes are gauge from a lattice energy function, and justify L_ref=a/2 against the §13.2.4.2 standard and the D-sized cell. Until then, grade 5π as [H] (a meaning-layer choice), consistent with how LOCK-NU-N treats [MAP-1]/[MAP-2].

### 7. [major] The 'shared gauge lemma' does not support 5=6−1: the nucleon derivation does not use it, the α_em use is a different quotient taken from a withdrawn section, and ν₁=1 is automatic

- **category:** circularity
- **location:** 13-mass-u-lat-m-h §13.3.4 (Shared-lemma note); 08 §8.0.5(II)–(III), §8.0.6(A),(B),(D); 14 §14.5.3–§14.5.4

**Quote.** The same forced lemma fixes the nucleon exponent (n sectors → n-1, §8.0.5) and the αₑₘ sign-microstate count (7 shells → 2⁶, §14.5.3). The factor 5 is therefore not a Higgs-specific choice.  ||  (ch.8 §8.0.6A) the C₃ ring-closure Σ_in_i=0 (§8.0.3) fixes the global phase as a gauge choice and removes no rectification  ||  s_n=n⟨W_n⟩^{-1}=nδ^{-n}, ν_n=s_nδ=nδ^{-(n-1)}  ||  The electron case is a nontrivial check: the law reproduces the independently defined electron clock of §9.3, it is not fitted to it.  ||  (§14.5.4) no sentence elsewhere in this document may cite §14.5 as a derivation or prediction of αₑₘ

**Evidence.** (1) In §8.0.6 the exponent n−1 comes from δ^{−n}·δ (the single-nozzle rate law ν=sδ). The same passage says explicitly that the gauge removes no rectification, which contradicts §8.0.5(II)'s reading via dim(Rⁿ/span 1). (2) n·x^{n−1}=1 at n=1 for every x, so the 'nontrivial check' ν₁=1 holds automatically. The law is then pinned by one data point, ν₃≈292. For example, (√3π²)^{n−1} also gives ν₁=1 and ν₃=3π⁴ but differs at n=2 (17.09 vs 2π²=19.74), and no n=2 object tests it. (3) The α_em 2⁶ counts the Z₂ quotient {±1}⁷/{±1} (a global sign flip), not R⁷/span{1} (an additive shift). It is also taken from a construction §14.5.4 declares non-citable. The linear-algebra lemma is trivially true; all the physics is in the choice of N and of the gauge mode, and a 'recurrence' does not transfer forcing.

**Proposed improvement.** Delete the claim that the shared lemma supports 5, or restrict it to the Higgs. Make §8.0.5 and §8.0.6 agree on where n−1 comes from. Remove the §14.5.3 citation from §13.3.4 and §8.0.6(D) to honor §14.5.4. State that ν₁=1 is a normalization, not a check, and propose an n=2 test or downgrade the n-fold law.

### 8. [major] m_p/m_e=6π⁵ is graded [F] 'forced' yet measurement excludes it as exact by ~10⁶σ; Lenz 1951 is missing and the r_p 'prediction' double-counts

- **category:** grading-honesty
- **location:** 13-mass-u-lat-m-h §13.5 banner, §13.5.5.4, §13.5.6, §13.3 'No-tuning fingerprint'; ea audit log; repro/physics/tools/vp_numeric_ssot.py

**Quote.** [F] identityin: two Compton lengths / out: $mₚ/mₑ=2πνₚ=6π⁵=1836.118$ ($-19$ ppm)  ||  The same pattern holds for mₚ/mₑ=6π⁵≈ 1836.12 (residual -19ppm from measured 1836.15) and for the predicted proton radius rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm).  ||  (audit log) Lenz (1951) characterization changed from "numerical coincidence" to "preceded the present derivation"

**Evidence.** CODATA 2022 gives m_p/m_e=1836.152673426(32), while 6π⁵=1836.1181087: Δ=−18.82 ppm, a pull of −1.1×10⁶σ. A forced exact identity is therefore falsified unless a correction term is stated. For scale, α_em²=5.3×10⁻⁵ would be the right order. The same numerical identity was published by F. Lenz, Phys. Rev. 82, 554 (1951). §13.5 does not cite it, and the audit log shows the wording was softened. Look-elsewhere check: for (p/q)·π^k with p,q≤12 and k≤8, a log-uniform target in [10³,3×10³] lands within 18.8 ppm with p≈3.0×10⁻³; for n·π^k with n≤12, p≈3.4×10⁻⁴. That is notable but not decisive. r_p=D/(6π⁶)=0.841251 fm is algebraically 6π⁵ together with r_p=(2/π)λ_C,p=4ħ/(m_p c). Its offset from 4ħ/(m_p c) is exactly +18.8 ppm, which the repro script itself labels 'R2 = −R1'. So it is not a second independent success. Against CODATA 2022 r_p=0.84075(64) fm it is +0.060% (+0.8σ), not the '−0.018% vs 0.8414' taken from CODATA 2018.

**Proposed improvement.** Grade 6π⁵ as 'leading-order structure [F]; exactness [O]' and pre-register the sign and size of the correction that must close −18.8 ppm. Cite Lenz 1951 in §13.5 and report the look-elsewhere p-value. In the fingerprint list, present r_p as a test of r_p·m_p=4ħ/c only, against CODATA 2022.

### 9. [major] The §13.4 'prediction' of m_p round-trips the measured proton mass through a 4-digit rounding; its +42 ppm residual is rounding error

- **category:** circularity
- **location:** 13-mass-u-lat-m-h §13.4 banner, §13.4.5.1–§13.4.5.3; cross-ref 02 §2.2 r_p status, 06 §6.3 banner

**Quote.** [F] predictionin: $λ_C=(π/2)rₚ$ / out: $Sₚ=λ_C/a=2087.476$; $mₚ=hc/λ_C=0.93831$ GeV  ||  Using the canonical input r_p=0.8412\times 10^{-15}\ \mathrm{m}  ||  (ch.02) the forced (2/π)λ_(C,p)=0.8412 fm is its +61 ppm cross-check  ||  (ch.06) in: $λ_C=1.32135$ fm / out: $Rₚ=0.8412$ fm

**Evidence.** (2/π)·h/(m_p c) with CODATA m_p gives 0.8412356 fm, and rounding to 0.8412 is a −42.4 ppm change. §13.4 then returns m_p=(2/π)hc/r_p=0.938312 GeV, which is +42.4 ppm against 0.9382721 GeV: exactly the rounding error. The λ_C used, 1.3213538700998668 fm, is (π/2)×0.8412, not the measured 1.3214099 fm, and ch.06 derives R_p from that λ_C. So the chain is m_p(measured) → λ_C,p → (2/π)λ_C,p → round → m_p. The identification L_q=λ_C (with h rather than ħ) is itself a factor-2π meaning-layer choice. Using the declared canonical route (r_p=D/6π⁶) gives m_p=6π⁵m_e=938.2544 MeV (−18.8 ppm), a different number from the one printed.

**Proposed improvement.** Delete the §13.4.5 numerics or recompute them from r_p=D/(6π⁶), and label the section 'identity (no independent content)'. State that the only physical claim is r_p·m_p=4ħ/c, flag the h-vs-ħ identification as a meaning-layer choice, and remove the '[F] prediction' banner.

### 10. [major] The unification theorem and ratio gates still use the electron radius r_e, which §13.5.4 calls spurious: m_e comes out π² too large and several invariants cannot equal 1

- **category:** internal-inconsistency
- **location:** 13-mass-u-lat-m-h §13.5.3 (boxed S), §13.5.4, §13.6.2.3, §13.6.3 (T-13.6-1), §13.7.5 (I_Ue, I_He, I_pe, I_Se)

**Quote.** \boxed{ S=\frac{D_{\mathrm{anch}}}{2a\pi^2} }  ||  Earlier drafts conflated the two, inserting a spurious factor δ=1/π² into mₑ.  ||  When the electron radius rₑ and the realization length a are locked, define the electron resistance integral ... S := \int_{0}^{r_e}\frac{dR}{a} = \frac{r_e}{a}  ||  m_e&=\frac{U_{\mathrm{lat}}}{S}=\frac{U_{\mathrm{lat}}}{r_e/a}

**Evidence.** The symbol S gets two definitions in one section: r_e/a (§13.5.3, boxed) and r_0/a (§13.5.4). This breaks the chapter's own 'no redefinition' rule. With the §13.6 definition, T-13.6-1 gives m_e=hc/r_e=2π²hc/D=π²×0.510999=5.043 MeV. Combining §13.5.4's m_e with §13.6's S gives I_Ue=r_e/r_0=δ=0.101 and I_He=I_pe=π²=9.87, so those gates would FAIL. I_UH, I_Up and I_Sp equal 1 by construction and compare nothing to measurement. None of the nine invariants involves external data, and no ratio report is in the repro bundle.

**Proposed improvement.** Replace r_e by r_0=λ_C,e in §13.5.3, §13.6.2.3 and I_Se, and remove the vestigial §13.5.5.2. Give S one definition. Replace the tautological invariants with gates against external data under a pre-registered dev_max (m_H vs PDG, m_p/m_e vs CODATA, r_p vs CODATA 2022) and publish the sealed reports.

### 11. [major] §14.0.4 gets the mass–resistance relation backwards: the proton has the small resistance coefficient

- **category:** internal-inconsistency
- **location:** 14-force-lattice-tension-1-r2 §14.0.4 ('Proton heavy', table); 13 §13.2 [A-13.2-1]

**Quote.** The 82 core members are large sub-quantum blocks (SQ, §6.4); large blocks present a large effective cross-section/resistance σ_eff (§13.2), hence large mass.  ||  (ch.13) m(\mathcal{O}) = \frac{U_{\mathrm{lat}}}{\sigma_{\mathrm{eff}}(\mathcal{O})}

**Evidence.** The axiom makes mass inversely proportional to σ_eff. Numerically S_p=λ_C/a=2087.48, while the electron's Compton-length coefficient is S_e=r_0/a=3.833×10⁶, 1836 times larger. The proton is heavy because its resistance is small, the opposite of the §14.0.4 narrative. The 82-block count enters no mass formula in ch.13 at all; m_p comes from λ_C, and 6π⁵ comes from 3 sectors.

**Proposed improvement.** Rewrite 'Proton heavy' in terms of the short mass-bearing length λ_C,p, or explain why the axiom is inverse. Drop 'large blocks ⇒ large mass' unless 82 is shown to enter a mass formula.

### 12. [major] The static Coulomb mechanism is asserted, and its sign rule and range contradict the stated field theory

- **category:** physics-validity
- **location:** 14-force-lattice-tension-1-r2 §14.0.5 (bullets 'Why a force exists', 'Why long-range'), §14.1.5.1; §14.0.6 (E = displacement)

**Quote.** E=\frac{\kappa_\phi}{2}\int|\nabla\phi|^2\,d^3x,\qquad \nabla^2\phi=-\rho  ||  the medium relaxes it — E_int=kq₁q₂/r. Sign rule: like sources ⇒ repel, opposite ⇒ attract (the electrostatic, positive-definite strain structure — not the relativistic-scalar convention).  ||  synchronization spontaneously breaks a global U(1) (the common phase), giving a massless Goldstone mode ⇒ infinite-range 1/r²  ||  This is the same derivation in both cases.

**Evidence.** (i) If the medium relaxes φ under a linear source coupling H=∫[(κ/2)|∇φ|²−ρφ], minimizing gives E_int=−q₁q₂/(4πκr), so like sources attract, as in scalar exchange. Like-repel needs φ to be a Gauss-law constraint field, which is the vector (A₀) structure the text rejects. (ii) One scalar Poisson mechanism cannot make all-positive gravitational sinks attract and like charges repel. The hydrodynamic source analogy gives like-attract (Bjerknes, and the Lagally force on a source, F=−ρ_f m U). (iii) By shift symmetry, Goldstone modes of a global U(1) couple derivatively (ρ∂ₜθ, J·∇θ), so static charges produce no 1/r Goldstone potential. (iv) In §14.0.6's elastic reading (charge = compression source of u), a centre of dilatation gives u∝r̂/r² with ∇·u=0 outside the source. Two such centres in an infinite isotropic linear-elastic medium have zero interaction energy (Eshelby 1956), so there is no 1/r² force.

**Proposed improvement.** Write one action (fields, kinetic-term signs, source coupling) and derive E_int with its sign for both charge and gravity sources. Drop the Goldstone argument, or build on the emergent-photon literature (Bjorken 1963; Nambu 1968; Kraus–Tomboulis 2002), which needs a vector order parameter. Reconcile the φ-field model of §14.0.5 with the u-field model of §14.0.6.

### 13. [major] The departure 'only charge is conserved (γ→p⁺e⁻ allowed)' also allows hydrogen to annihilate and the proton to decay, both excluded to >10³⁴ yr

- **category:** physics-validity
- **location:** 14-force-lattice-tension-1-r2 §14.0.4 ('Why electron and not antiproton'), §14.0.7 ('Baryon/lepton number not fundamental')

**Quote.** Because only charge (L_z) is conserved here — not a separate baryon number — the cheapest balancer is the bare electron (p+e^-≈ 938.8 MeV) rather than an antiproton  ||  γ→ p^++e^- is forbidden in the Standard Model (baryon and lepton number) but allowed here, since only charge/L_z is conserved. This is a genuine departure

**Evidence.** If charge/L_z is the only conserved quantity, the reverse process p+e⁻→photons (net charge 0) is allowed by detailed balance, and so are charge-conserving decays p→e⁺π⁰ and p→e⁺γ. Super-Kamiokande bounds τ(p→e⁺π⁰)>2.4×10³⁴ yr (PRD 102, 112011, 2020), and bulk hydrogen is stable. Photon beams far above the 938.8 MeV threshold produce e⁺e⁻ and p p̄ but no p e⁻ final states. The text gives no barrier or selection rule.

**Proposed improvement.** Name the conserved quantity or barrier that makes p and H stable for ≥10³⁴ yr. Give a cross-section for γZ→p e⁻ Z and compare it with existing photoproduction data. Otherwise withdraw the departure or mark it [O] with this tension stated.

### 14. [major] Qualitative EM mechanisms contradict well-measured data: the conduction medium, the atomic 'stand-off', and the 'weak' neutron moment

- **category:** physics-validity
- **location:** 14-force-lattice-tension-1-r2 §14.0.6 ('Conduction vs. radiation', 'Why the electron cannot reach the proton'), §14.0.4 (neutron)

**Quote.** (ii) the medium — electric conduction propagates through the quanta inside the copper atoms (and along the wire), not through vacuum or air.  ||  the electron's closest approach is the outside of that host quantum — a finite stand-off that plays the role of the atomic radius  ||  its internal (angularly twisted) nucleon rotation occasionally leaks past the host boundary, producing a weak residual electromagnetism — the neutron magnetic moment μₙ≠0

**Evidence.** Signal speed on a line is set by the dielectric: v=c/√ε_r, about 0.66c for solid polyethylene coax and about 0.95–0.99c for air-spaced coax with identical copper. The field energy flows in the dielectric (Poynting), not through copper, whose skin depth is about 2 µm at 1 GHz. The host quantum has diameter D=4.8526 pm, so the stand-off is D/2=2.43 pm, while the Bohr radius is 52.92 pm (21.8× larger). The stand-off is also mass-independent, whereas muonic hydrogen's orbit, a₀·m_e/m_red=0.285 pm, lies 8.5× inside D/2 and its Lamb shift agrees with QED plus Coulomb. μ_n=−1.913 μ_N vs μ_p=+2.793 μ_N gives |μ_n/μ_p|=0.685 (the quark-model −2/3), not a 'weak residual'.

**Proposed improvement.** Remove these statements or mark them [O], with each tension stated. If kept, turn each into a quantitative prediction: velocity factor vs conductor material, the stand-off radius's dependence on orbiting mass, and μ_n/μ_p.

### 15. [major] The 'four-force unity' regime map misdescribes the weak and strong interactions and is promoted from [H] to 'Forced' in the read-first summary

- **category:** grading-honesty
- **location:** 14-force-lattice-tension-1-r2 §14.1.5.3 table and Status; rf-read-first 'Forced (no adjustable content)'

**Quote.** | Weak / decay | Phase-transition gate; discrete annihilation events | Per-event decay rates; not a static force at all | per-event  ||  | Strong (nuclear) | 82-core jamming, short-range deficit collapse | Confining force inside rₚ | lesssim 1fm  ||  [H] for the regime map  ||  (rf) Higgs coefficient 5π (§13.3); the 1/r² shape and four-force unity

**Evidence.** The weak neutral current produces a static parity-violating electron–nucleus potential ∝G_F Q_W δ³(r), measured by atomic parity violation (Cs 6S–7S, Wood et al. 1997, 0.35%). The nuclear force binds nucleons at separations of 1–2.5 fm, outside r_p=0.84 fm; the deuteron rms radius is 2.13 fm. So neither row matches known phenomenology. The chapter grades the map [H], but rf lists 'four-force unity' under Forced.

**Proposed improvement.** Keep [H] everywhere and fix rf's Forced list. Revise the weak and strong rows to account for static APV and the inter-nucleon force range, or drop the 'not four forces' claim until each row makes a quantitative prediction.

### 16. [major] The '[F] F_bridge=mc²/D verified to four digits across the particle list' has no derivation or script, and is an identity if masses are input

- **category:** reproducibility-code
- **location:** 14-force-lattice-tension-1-r2 §14.1.5.2 and Status; w0 scorecard row v0.5.0; 17 §17.4.0

**Quote.** Computing both sides independently for the standard particle list (electron, muon, tau, proton, neutron, pion, kaon, etc.), the framework's particle-card output matches F_bridge to four significant digits across every entry.  ||  [F] for the F_bridge=mc²/D identity verified across the particle list

**Evidence.** No physics chapter derives m_μ, m_τ, m_π or m_K (a grep for muon/kaon/pion returns only this sentence). No tool in repro/physics/tools computes a 'bridge' or 'particle card'. With PDG masses on both sides, mc²/D equals mc²/D identically. The chain 'ν_ann ×2π → m' used here is also inconsistent with ν_e=1 and m_p/m_e=2πν_p (see the WEP finding). Yet w0 advertises the claim as an 'easy-to-miss derived result' and ch.17 relies on it.

**Proposed improvement.** Publish the particle-card code and inputs, and show which side is computed independently; otherwise delete the claim and its w0/ch.17 citations. Grade it [O] meanwhile.

### 17. [major] 'Event rates' carry s⁻¹ yet enter a dimensionless mass ratio, which ties results to the SI second

- **category:** unit-dimension
- **location:** 13-mass-u-lat-m-h §13.5.5.3, §13.5.6; 14 §14.0.4; 08 §8.0.5(IV)

**Quote.** \nu_{p,\mathrm{can}}=3\pi^{4}\approx 292.227\ \mathrm{s^{-1}}  ||  \nu_{p,\mathrm{can}} = \left(\frac{D_{\mathrm{anch}}}{2r_p}\right)\left(\frac{1}{\pi^2}\right)  ||  (ch.14) νₚ=3π⁴≈292s⁻¹ and νₑ=1s⁻¹

**Evidence.** ν_p,can=(D/2r_p)δ is a pure number, but it is quoted in s⁻¹ and then used in m_p/m_e=2πν_p, which must be dimensionless. If ν_e=1 s⁻¹ is physical, the theory depends on the SI second, defined by the ¹³³Cs hyperfine transition (9 192 631 770 Hz). Rescaling time units (for example to minutes) changes ν_e to 60 and breaks m_p/m_e=2πν_p unless ν_p rescales too, which the fixed value 3π⁴ does not.

**Proposed improvement.** Drop s⁻¹ and treat ν as dimensionless structural numbers, or express physical rates in a derived lattice time unit (for example Δt) and write m_p/m_e=2π(ν_p/ν_e) explicitly.

### 18. [major] Overclaimed grade badges and banners: page-level [F], an [F] empirical anchor, '|qₑ|=|qₚ| exact', a 'derived' 9% diagnosis, and a Casimir 'cross-examination'

- **category:** grading-honesty
- **location:** 13 page header and cards; 14 page header, §14.0 banner and closing Grade, §14.2 banner and reading note, §14.0.4 (89/82), chapter lede vs §14.4.1

**Quote.** (ch.13) Grade [F] forced.  ||  λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); ... [F] forced.  ||  [F] genesisin: rotation + pockets / out: $|qₑ|=|qₚ|$ exact  ||  the genesis dynamics are [H] (hypothesis)  ||  The 9% diagnosis is itself a derived sector-separation result — the negative carries positive content.  ||  the gravity-sector A is √(8.81/7.41)=1.090× larger — exactly the ≈9% shortfall  ||  Consequently the ratio 89/82 is a gravity/mass-sector quantity  ||  The vacuum-stiffness story is cross-examined against the Casimir 1/d⁴ law.

**Evidence.** Both chapters carry [F] page badges, yet ch.13 contains a calibration node and an [H] Higgs closure, and ch.14 contains superseded, [H] and [O] material. A measured anchor cannot be 'forced'; by the framework's own taxonomy it is [L]. The banner claims charge equality is exact, while the body says [H] and the author's own Monte Carlo does not reproduce the 6+1 occupancy. (2π/α)²=741,360 uses the measured α, so √(A/741360)=1.0901 restates the mismatch rather than deriving anything. The actual shortfall is 1−0.9174=8.3%, not '≈9% exactly'. No mass or gravity observable equals 89/82=1.0854 (m_n/m_p=1.00138), so relabelling it 'gravity-sector' is post hoc. §14.4.1 itself says the Casimir section 'adds no VP-specific content'.

**Proposed improvement.** Make page and section badges show the weakest grade present, and grade the anchor [L]. Change the §14.0 banner to [H]. Delete the 'derived sector-separation result' sentence and the 89/82 relabelling. Reword the Casimir lede to 'non-contradiction check'.

### 19. [minor] Stale links to the superseded Coulomb route remain in live definitions, and e_map is tautological

- **category:** internal-inconsistency
- **location:** 14-force-lattice-tension-1-r2 §14.1.5 intro, §14.3 scope note, §14.3.3, §14.3.4, §14.3.5, §14.0.5

**Quote.** where K_C^(VP) is the absolute constant fixed in §14.2.  ||  that ratio is Nₚ/Nₙ from the structure counts of §7.2.2 ... the Coulomb structure ratio 89/82 of §14.2  ||  The previous subsections derive the Coulomb constant from the lattice field strength hc/a² with amplification A^(-1/2)  ||  with κ_φ the phase stiffness (∝ A, the measured amplification of §11.6)

**Evidence.** The live force law (§14.3.3) and e_map (§14.3.4) point to the superseded constant K_C^(VP)=2.2971×10⁻²⁸ N·m². Under the live coupling K_C=α_emħc=k_e e²=2.3071×10⁻²⁸, e_map=√(K_C/k_e)=e by construction, so it measures nothing. §14.0.5 ties the EM phase stiffness to A in the same paragraph that evicts A from EM. PASS_C still references Γ_C.

**Proposed improvement.** Point §14.3.3–§14.3.5 to K_C=α_emħc (measured) and delete e_map or label it an identity. Remove 'κ_φ ∝ A' and the 89/82 'Coulomb structure ratio' wording, and rewrite the §14.1.5 opening sentence.

### 20. [minor] Outdated or inconsistent reference values (r_p, k_e, m_e, the Higgs source, the m_e comparison)

- **category:** math-error
- **location:** 13 §13.3.7, 'No-tuning fingerprint'; 14 §14.0.4 eq. for m_e; repro/physics/tools/vp_numeric_ssot.py (MEAS, CANON, k_e)

**Quote.** (−0.018% vs CODATA 0.8414 fm)  ||  m_H^exp=125.20± 0.11GeV (CODATA/PDG 2024)  ||  m_e=\frac{hc}{\lambda_{C,e}}=\frac{hc}{r_0}=\frac{2hc}{D}=0.5109\ \mathrm{MeV}\quad(\text{measured }0.51100;\ {-}0.03\%  ||  (script) q["k_e"]     = c["C"]**2 * D("1e-7")

**Evidence.** CODATA 2022 gives r_p=0.84075(64) fm, so the prediction is +0.060% (+0.78σ), not −0.018%. CODATA does not tabulate m_H; the source is PDG 2024. k_e=c²×10⁻⁷ is the pre-2019 exact value; post-2019, k_e=8.9875517862(14)×10⁹ (CODATA 2022). The script uses CODATA 2018 m_e=9.1093837015e-31 rather than 9.1093837139e-31. With D_anch:=2λ_C,e, 2hc/D=0.51099895 MeV exactly. The '−0.03%' corresponds to D=4.8542 pm (the jamming length), contradicting §13.5.4's statement that this is a calibration node, not evidence.

**Proposed improvement.** Update to CODATA 2022 and PDG 2024 and cite them correctly. In §14.0.4 write m_e=0.51099895 MeV (calibration, by construction) and move the 4.8542 pm comparison to a separate D cross-check.

### 21. [minor] '82 = 3⁴ + 1' counts the centre twice when 81 is read as the lattice points with R²≤6; the m_n − m_p sign test is missing

- **category:** internal-inconsistency
- **location:** 14-force-lattice-tension-1-r2 §14.0.2 (and Status 'geometry vs. dynamics')

**Quote.** N_{\text{core}}=3^4+1=82 ... where 81=3⁴ is exactly the number of integer-lattice points with R²≤6 (independently verified) and the +1 is the central rotation.  ||  Through 82 the construction is geometric and firm

**Evidence.** The count of integer points with R²≤6 is 1+6+12+8+6+24+24=81, and it already includes the origin (R²=0). A '+1 central rotation' at the centre therefore puts two units at the origin. Otherwise the 82nd unit must sit off-centre at R²≥8 (since R²=7 is empty), which breaks the claimed symmetry. The '3 bodies × 27' reading and the 'R²≤6 ball' reading are different sets that merely share the cardinality 81. The picture also gives the proton 7 more members than the neutron but does not predict the sign of m_n−m_p=+1.293 MeV.

**Proposed improvement.** State which set of 82 positions is meant and where the +1 sits, or drop 'geometric and firm'. Add a pre-registered sign (and ideally size) for m_n−m_p as a test of the 82/89 picture.

### 22. [minor] Rendering defects: a raw '<a' swallows text and LaTeX residue appears in visible prose; §14.1 is numbered out of order

- **category:** presentation-rendering
- **location:** docs/physics/14-force-lattice-tension-1-r2/index.html §14.1.4, §14.0.6, §14.2, §14.5; docs/physics/13-mass-u-lat-m-h/index.html §13.3.4, §13.4.1, §13.7.5

**Quote.** the region R<a is classified as <em>outside the geometric-dilution regime</em>  ||  (Definition) Saturation handling ... For the out-of-regime region (R<a), this section does not use D_dil.  ||  with boldsymbolΨ=mathbf E+iZ₀mathbf H  ||  Light emphis the electromagnetic wave  ||  noindent[SUPERSEDED — record only  ||  (Amp\`ere)  ||  (ItextsubscriptUH)  ||  U_lat:=dfrachc_refa  ||  ### 14.1.8 Anisotropic extension ... ### 14.1.6 ... ### 14.1.5

**Evidence.** The raw HTML contains 'R<a' unescaped (twice). Browsers parse '<a is classified as <em>' as an anchor start tag, so the text disappears; the extracted text reads 'the region Routside the geometric-dilution regime'. There is no MathJax or KaTeX on the page, so strings like mathbf E/B (31×), boldsymbol, Box_c, emph*, noindent (9×), Amp\`ere, [F]{}, dfrac, textsubscript (9×) and 'square' appear verbatim. The equation alt text also has an unexpanded '\aVP'. Subsections run 14.1.4 → 14.1.8 → 14.1.6 → 14.1.5.

**Proposed improvement.** HTML-escape '<' as &lt; in prose, convert the LaTeX macros in body text to Unicode or rendered math, expand \aVP in the alt text, and renumber §14.1. Add a build gate that rejects unescaped '<' followed by a letter and any backslash-free TeX macro names in visible text.

**Strengths noted:**
- §14.5 withdraws the α_em closed form honestly and for correct reasons: the 4π is an SI artefact, α runs, and the fit is degenerate (I checked 4π(11−(35/32)(2/π²)(3/7))=137.03641 at +3.0 ppm, while 4π³+π²+π=137.03630 at +2.2 ppm, so the degeneracy argument holds).
- §13.4's status note and §13.5.4 openly state that a cancels, that the electron is the calibration node, and that the earlier π² confusion is on record. That is the right instinct and should be carried through §13.6–§13.7.
- §14.4 Casimir is correctly labelled non-contradiction, not derivation. Its numbers check out (|P|=1.30×10⁵ Pa at 10 nm, the 1/d⁴ table, and the PFA sphere–plate form −π³ħcR/(360d³)), and it demands a pre-registered screening function before any deviation claim.
- All arithmetic in §13.1–§13.5, §14.1.3 and §14.2 reproduces to the quoted digits: U_lat=1958.7033116641 GeV, m_H=124.6949256 GeV, S_p=2087.47585, F_lat=4.957713×10¹¹ N, K_C^(VP)=2.29713×10⁻²⁸, e_map=1.5987×10⁻¹⁹ C.
- repro/physics/tools/vp_numeric_ssot.py reduces the scattered ppm residuals to two independent ones and itself flags R2=−R1. This is exactly the discipline needed, and it should be extended to external-data gates.
- The isotropy lemma (the only SO(3)-invariant rank-3 tensor is ε_ijk, so a first-order local isotropic vector operator must be a curl) is correct and cleanly separates the forced step from its premises.
- §14.0.2 treats occupancy settling as 'operator testimony, not evidence' and discloses the author's own Monte Carlo result that contradicts the hand-set 6+1 configuration. That kind of candour gives the corpus credibility.


## review:qm-doi-time-gravity

### 1. [critical] River identity (G-RIVER) is an algebraic tautology, and the 'river' velocity is not the medium's own velocity. The claim is circular and imported from GR

- **category:** circularity
- **location:** docs/physics/18-time-and-gravity §18.0, §18.6, §18.7, §18.10; repro/physics/tools/vp_timegravity_ssot.py gate_river(); docs/physics/17-extensions-optional-reading §17.4.3, §17.4.4(ii); hub physics.txt line 56; scorecard w0 line 52

**Quote.** §18.0: "a clock is the medium's processing rate, and a clock slows by exactly the kinematic factor of its velocity relative to the local medium." / §18.7: "The incompressible mass-current that books the sink's steady consumption falls as $1/r^2$; the time-dilation velocity is the potential (free-fall/river) velocity and falls as $1/\sqrt{r}$" / vp_timegravity_ssot.py: "identical = (fr == fs)            # v_river^2 = 2GM/r  =>  1 - v_river^2/c^2 = 1 - 2GM/rc^2" / §17.4.4: "the implied consistency surface (drift ≈194 km/s at Earth's surface, ρ_eff≈3.06 kg/m³, B_eff≈2.7×10¹⁷ Pa under M1)" / §18.0: "No external relativistic postulate is used as a derivation basis anywhere in this chapter" / hub: "the river identity makes gravitational time dilation exact Schwarzschild. forced"

**Evidence.** (a) G-RIVER defines v_river := sqrt(2GM/r) and then checks by floating-point equality that sqrt(1-v_river^2/c^2) = sqrt(1-2GM/rc^2). That is an algebraic identity: any theory passes it, so 'machine-exact to NS strong field' tests nothing. (b) The organising principle of §18.0 uses the clock's velocity relative to the local medium, but §18.7 says the medium's actual (incompressible) flow goes as 1/r^2. Put the medium velocity into the §18.0 law. With the framework's own M1 drift of 194 km/s at Earth's surface: v^2/2c^2 = 2.09e-7, against the measured GM/(R c^2) = 6.96e-10 (x301). The ground-vs-GPS (r=26,560 km) difference is 2.087e-7, against the measured/GR value of 5.29e-10 (x394). The radial law would be r^-4 instead of r^-1, which the Galileo-5/6 eccentric-orbit redshift tests exclude at the ~3e-5 level (Delva et al. 2018). (c) Suppose instead the medium really flows at v_river ~ r^-1/2. Steady continuity, div(rho v)=0, then forces rho ~ r^-3/2 (rho(2R)/rho(R)=0.354). With the framework's c^2=K/rho_eff and fixed K, c(2R)/c(R)=2^(3/4)=1.68, so the single constant c inside sqrt(1-v^2/c^2) is not constant. Either way the identity fails. (d) Setting the flow speed to the escape velocity presupposes that the medium itself free-falls in the Newtonian potential its own inflow is supposed to create. §17.4.3 also states that the cap mechanism 'cannot be' Newtonian GM/R^2. Identifying the clock-slowing velocity with the free-fall-from-infinity velocity is exactly the Painleve-Gullstrand 'river model' of GR (Hamilton & Lisle 2008). That is an import, contradicting §18.0.

**Proposed improvement.** 1. Regrade G-RIVER from [F] to [H]: 'the clock-slowing velocity is identified with the PG free-fall velocity'. Say explicitly that this is imported from GR.
2. Relabel the gate as an algebraic consistency check, not a verification.
3. Derive the medium's velocity and density field for a sink from continuity plus momentum balance in the compressible medium (K, rho_eff). Compute dtau/dt(r) from that field.
4. Pre-register the r-dependence against Gravity Probe A (1.4e-4) and Galileo-5/6 (~3e-5).
5. State which physical field the clock couples to. The current 'two velocities' device must not be used to swap fields after the fact.
6. Update the hub and scorecard entries that call this 'forced'.

### 2. [critical] The exact factor sqrt(1-v^2/c^2) is not 'forced' by isotropy: isotropy fixes only the longitudinal/transverse ratio, and a hidden 'no transverse change' assumption selects the Lorentz factor

- **category:** grading-honesty
- **location:** docs/physics/18-time-and-gravity §18.1, §18.2, §18.3, §18.10; repro/physics/tools/vp_exact_sqrt.py; scorecard w0 lines 50-51; docs/physics/14 §14.0.6 cross-ref

**Quote.** §18.2: "The rate must therefore be independent of the winding orientation $\theta$, which forces $T$ to be $\theta$-independent" ... "Any other contraction leaves a residual orientation dependence (a Michelson-Morley fringe for the winding); isotropy admits only $\kappa=\sqrt{1-v^2/c^2}$." / §18.3: "both are framework assets, so this is grade [F]" / §18.1: "the rotation-emission clock is not a light-clock — no photon is bounced across $D$. The motion result of §18.2 is built on the winding's own geometry and the medium signal speed, never on a light-clock shortcut." / §18.2: "To leading order this is the self-wake / refill-competition result (the refill budget diverted to the moving body's plenum displacement scales as $v^2/c^2$)" / vp_timegravity_ssot.py: "def f_motion_exact(v):           # sqrt(1 - v^2/c^2)   exact factor is [O] (not derived from medium)"

**Evidence.** I checked the T(theta) formula; it is the correct Michelson round trip. Now allow a transverse scale d(v) as well as the longitudinal kappa: T(theta) = 2L*sqrt(kappa^2 c^2 cos^2 + d^2 (c^2-v^2) sin^2)/(c^2-v^2). Isotropy then only requires kappa = d*sqrt(1-v^2/c^2), and the rate becomes sqrt(1-v^2/c^2)/d. Computed at v=0.6c:
- d=0.8 gives kappa=0.64, anisotropy 8.9e-16, rate = 1.000 (no dilation at all).
- d=1.0 gives 0.800.
- d=1.25 gives kappa=1 (no contraction), rate 0.640.
The script fixes d=1 implicitly and minimises over kappa only, so the 'unique minimizer' is an artefact of that assumption. This is the textbook Robertson-Mansouri-Sexl structure: Michelson-Morley-type isotropy fixes only the longitudinal/transverse ratio. The absolute dilation needs Kennedy-Thorndike and Ives-Stilwell experiments.
Further problems:
- The premise 'the moving clock's rate is orientation-independent' is the empirical MM null result. It does not follow from nu_e being a scalar at rest.
- The 'Michelson-for-winding' T(theta) is literally the Michelson light-clock round trip, which contradicts the §18.1 guardrail.
- The leading 1-v^2/2c^2 '[F leading]' attributed to 'self-wake/refill competition' has no derivation anywhere in the corpus. A grep finds 'self-wake' only in §18.2 and the scorecard, which cites §18.2.
- The SSOT module still grades the exact factor [O]. The upgrade [O]->[F] (CHANGELOG_v0_10_0) therefore rests on the unstated d=1.

**Proposed improvement.** 1. Regrade the exact factor as conditional: [L] anchored on the empirical MM/KT/IS null results, or [H] given 'no transverse deformation'. Keep full dynamics [O].
2. Add d(v) to vp_exact_sqrt.py and print the surviving one-parameter family.
3. Either derive d(v)=1 from the medium dynamics (e.g. the Heaviside/Searle field of the actual lattice excitation) or cite the KT/IS bounds (~1e-8, e.g. Botermann et al. 2014) as the anchor.
4. Supply the self-wake derivation of the coefficient 1/2, or drop the separate [F leading] line.
5. Reword the §18.1 'not a light-clock' guardrail.

### 3. [critical] The QM 'completion note' maps only a single-particle notation; entanglement and Bell violation are absent and structurally excluded by the framework's locality

- **category:** missing-test-or-prediction
- **location:** docs/physics/15-quantum-mechanics-mapping-completion-note §15.1.3, §15.2.4, 'Open — What This Framework Does Not Claim'; docs/physics/18-time-and-gravity §18.5; hub physics.txt line 62

**Quote.** §15.1.2: "The definitions above are operational: they construct a state field directly from event-log aggregates and do not invoke axioms from any external theory." / §15.2.4: "m^\star := \operatorname*{arg\,max}_{m\in\mathcal{M}} \ \mathcal{G}_m\big(C_m(k_0,M);\Theta_m\big)." / §18.5: "there is no faster channel because there is no void to bypass through" / §15 Open: "Stated plainly. §12 (electron one-second) carries an unresolved O(1) factor. Other open items are flagged in place within their parent sections in Part I—αₑₘ (§14.5, non-evidence) and the absolute magnitude of gravity (§17.4, a proven obstruction = the hierarchy problem)."

**Evidence.** The state space S = {psi : Z^d -> C} is one-particle l^2(Z^d). There is no tensor-product or configuration space for N particles, so entangled states cannot even be written down. I grepped all 48 physics chapter texts and the whole docs/ HTML tree. 'entangl', 'Bell', 'CHSH', 'superposition', 'interference' and 'double slit' have zero QM occurrences; the only hit is 'entangled' used figuratively in cosmology §AXC.
In the framework, outcomes are a deterministic function (argmax) of local event counts, and §18.5 states there is no faster-than-c channel. That is a local deterministic hidden-variable model, so Bell/CHSH forces |S| <= 2. Quantum mechanics predicts 2*sqrt(2) = 2.83, and loophole-free experiments measure S = 2.42 +/- 0.20 (Hensen et al. 2015; also Giustina 2015, Shalm 2015). The framework therefore cannot reproduce observed quantum correlations without violating one of its own stated principles. The §15 open list omits this entirely.

**Proposed improvement.** 1. Retitle §15 as a 'single-particle notation mapping'.
2. Add explicit [O] items to the Open list: multi-particle state space, entanglement, Bell/CHSH, no-signalling.
3. State which Bell assumption the lattice gives up. Preferred-frame nonlocal dynamics is compatible with an ether but contradicts §18.5's 'no faster channel'; the other option is giving up measurement independence. Grade that choice honestly.
4. Pre-register a CHSH value computed from a two-detector event-log simulation. If S <= 2 comes out, record it as a falsification (FAILPACK).

### 4. [critical] The spine's only surviving wave is longitudinal, but light is transverse with two polarizations, and §15.5 silently uses two

- **category:** physics-validity
- **location:** docs/physics/sp-jamming-spine-verified-physical-backbone S2.3, S5; docs/physics/10-implementing-speed-light-clock-free §10.9; docs/physics/14-force-lattice-tension-1-r2; docs/physics/15 §15.5.1

**Quote.** Spine S2.3: "the relaxed (non-affine) shear modulus vanishes,G_{relaxed}→ 0, while the bulk modulusBstays finite (compression needs no surplus). The transverse wave dies; one longitudinal speed survives," / §10.9: "On the jammed lattice, light propagates as a transverse oscillation of the rotating quanta" / §14: "Light is nearly — not exactly — transverse: χ≈89.9^∘" / §15.5.1: "Including the usual electromagnetic prefactors gives g(ν)=8πν²/c_ref³,"

**Evidence.** G->0 with finite B at isostaticity is correct textbook jamming (O'Hern/Liu/Nagel). But it means the medium carries only compression waves, like a fluid.
- A longitudinal wave has one polarization state. It cannot account for Malus's law, photon helicity +/-1, or birefringence.
- A transverse displacement wave in a G->0 medium has speed sqrt(G/rho) -> 0. So the chapters that call light (nearly) transverse at chi=89.9 deg contradict the spine's mechanism for c.
- Quantitatively: §15.5.1's 8*pi*nu^2/c^3 counts two transverse polarizations. With the spine's single longitudinal mode, g(nu) = 4*pi*nu^2/c^3. The Planck energy density and the Stefan-Boltzmann constant would then be halved, a factor-2 error ruled out by radiometry and the CMB spectrum.
- The [V] on 'c^2=B/rho' verifies the simulated lattice's own acoustic identity (sound speed = sqrt(B/rho)). That is not a test of its identification with the speed of light, which in any case is an ANCHOR (§16.4: c_ref 'This document does not derive it').

**Proposed improvement.** 1. Split the grade: lattice acoustics c_L^2 = B/rho is [V]; 'light = this wave' is [H]; the polarization count is [O].
2. Either add a rotational/micropolar (Cosserat) stiffness sector that supports exactly two transverse modes at speed c with a suppressed longitudinal branch, and derive it; or state the polarization obstacle as an open problem.
3. Derive the factor 2 in §15.5.1 rather than importing 'the usual electromagnetic prefactors'.
4. Reconcile §10.9/§14 ('transverse') with S2.3 ('transverse wave dies').

### 5. [major] 'The geom channel equals exact Schwarzschild' for orbits, light bending and gravitational waves is asserted; only the static-clock component g_tt is reproduced

- **category:** physics-validity
- **location:** docs/physics/18-time-and-gravity §18.6, §18.8, §18.10; repro/physics/tools/vp_cap_depart.py header

**Quote.** §18.8: "while redshift, orbits, light bending, and gravitational waves are the uncapped \emph{geom} channel, which equals exact Schwarzschild by §18.6." / §18.8: "the geom channel is exact Schwarzschild everywhere accessible" / §18.10: "the gravity sector yields ... observationally degenerate with GR"

**Evidence.** §18.6 derives only the static-clock lapse sqrt(1-2GM/rc^2), i.e. g_tt. Everything else listed is untouched:
- Light deflection (1.75") and Shapiro delay need the spatial metric (gamma_PPN = 1; Cassini gives gamma-1 = (2.1+/-2.3)e-5).
- Perihelion advance needs beta_PPN.
- Gravitational waves are dynamical, and the Schwarzschild solution is static and contains none. The spine's G->0 medium has only compression modes, while LIGO/Virgo polarization tests (GW170814) favour tensor over pure scalar modes and GW170817 bounds |c_gw/c - 1| < ~1e-15.
- Generic scalar/inflow gravity radiates dipole/monopole power, but the Hulse-Taylor decay matches GR's quadrupole formula (Pdot_obs/Pdot_GR = 0.9983 +/- 0.0016).
- Acoustic-metric obstruction (cf. Visser 1998, CQG 15, 1767): a flow obeying continuity at v ~ r^-1/2 has rho ~ r^-3/2. Its effective metric is only conformal to PG-Schwarzschild, which changes timelike geodesics (orbits).
A grep of the whole physics volume finds no perihelion, Shapiro, PPN, binary-pulsar or GW computation. The 'honest negative' (degenerate with GR) is therefore unproven: the sector may instead be excluded.

**Proposed improvement.** 1. Replace 'equals exact Schwarzschild' with 'reproduces the static-clock rate g_tt; other sectors [O]'.
2. Derive the medium's effective (acoustic) metric including the conformal factor, and compute gamma_PPN, beta_PPN, light deflection, Shapiro delay, perihelion advance, GW speed and polarization content, and binary-pulsar radiation reaction.
3. Grade 'degenerate with GR' as [O] until those numbers exist, and pre-register them against Cassini, LLR, PSR B1913+16, the double pulsar and GW170817.

### 6. [major] Born rule, superposition and collapse are definitional: psi is built from the counts it 'predicts', cannot interfere destructively, and the argmax gate contradicts Born statistics

- **category:** circularity
- **location:** docs/physics/15-quantum-mechanics-mapping-completion-note §15.1.2, §15.1.5, §15.2.3-§15.2.5, §15.3.1, §15.3.6 (V-S1); chapter header

**Quote.** "Here (S15_02_Pm_bornform) is not derived from the foundations of standard QM. It is an identity that holds equivalently by construction from the event-log definition and (S15_01_psi_def)." / header: "Collapse becomes a counting protocol with a Gate, not a mystery." / §15.1.5: "Assume a regime in which tick evolution is linear and translation-invariant" / (V-S1): "whether the event frequencies of the two channels σ=±1 match the predicted frequencies computed from (S15_02_Pm)"

**Evidence.** (1) P_m = C_m/C_tot, and |psi|^2 = rho holds by definition, so the 'Born form' is an identity; the text admits this. The physical Born rule is predictive: it gives outcome frequencies over repeated trials from a state prepared before measurement. Here psi is computed from the same window's detections, so gate V-S1 compares a quantity with itself.
(2) The map from event log to psi is nonlinear, while linear evolution U is simply assumed. Counterexample (M=10): logs N=(2,0,0), (0,2,0), (0,0,2) give psi1+psi2+psi3 = 0 (|psi|^2 ~ 7e-32, complete destructive interference). The merged log (2,2,2) has rho = 0.6 and Z = 0, so its phase is undefined. For two logs, the superposition has |psi|^2 = 0.2 but the merged log has 0.4. Counts are additive, so dark fringes cannot be represented.
(3) No dispersion Omega(kappa) or Schroedinger/Dirac equation is given.
(4) The argmax gate always selects the most-populated channel. A 50/50 beam splitter would then give a deterministic outcome, not 50/50 statistics.
(5) §15.3.1 requires observables only to be 'linear'. The Robertson step Im z = <[A,B]>/2i needs them to be self-adjoint.

**Proposed improvement.** 1. Replace 'Collapse becomes a counting protocol ... not a mystery' with a neutral description.
2. Specify the dynamics that generates event logs from a prepared state, so P_m is predicted before the window.
3. Show how merged logs map to psi1+psi2 (i.e. where interference comes from), or record superposition as [O].
4. Replace argmax with a stochastic selection rule and derive its statistics.
5. Define arg Z at Z = 0, and require observables to be self-adjoint.
6. Add a pre-registered double-slit fringe-visibility gate.

### 7. [major] Two incompatible gravity 'caps': Appendix G puts Earth exactly at yield (g*=9.80665 m/s^2), while §18.8's velocity-yield reading excludes that by ~4 orders of magnitude

- **category:** internal-inconsistency
- **location:** docs/physics/axg-geometric-derivation-gravity-lattice-yield header card, provenance note, G.0, G.2.3-G.2.4; docs/physics/18-time-and-gravity §18.5, §18.8; §17.4.2 Result 2; repro/physics/tools/vp_cap_depart.py

**Quote.** App G card: "g* = c²·Ψ_yield — Gravity-cap mechanism: a yield-limited acceleration ceiling (Beverloo-type discharge). [F] forced." / App G: "$\Psi_{\mathrm{yield}} := \frac{9.80665}{c^{2}}$" / "Each body carries its own back-substituted yield value Ψ_(rm yield)^(body)" / §18.8: "$r_{\mathrm{fluid}}=\frac{r_s}{\alpha^2}$" ... "earlier-yield readings ($\alpha<0.69$ at the NS surface, $\alpha<0.82$ at the BH light ring) are excluded" / G.2.3: "$\Psi_{\rm geom}(R) \;\equiv\; \frac{R_s}{2R^2} \;=\; \frac{GM}{c^2R^2} \quad [m^{-1}]$"

**Evidence.** (1) Since Psi_yield := 9.80665/c^2, g* = c^2 Psi_yield is 9.80665 identically, and the App G script puts Earth at x = 1.000000 by construction. Grading that [F] is a tautology.
(2) §18.8 reads the cap as fluidization where v_river = alpha*c. Earth-at-yield then implies alpha = v_esc/c = 11186/299792458 = 3.73e-5, deep inside the range §18.8 calls excluded (alpha < 0.82). Conversely, the 'most forced' alpha = 1 puts Earth's cap at g = c^4/(4GM) = 5.07e18 m/s^2, 17 orders above App G's g*.
(3) §17.4.2 Result 2 (p ~ rho v^2) implies a velocity (potential-depth) threshold, not an acceleration threshold.
(4) Back-substituting Psi_yield per body makes the cap unfalsifiable.
(5) The 'geometric derivation' defines Psi_geom := GM/(c^2 R^2) and multiplies by c^2, so Newton is inserted by definition. Psi (m^-1) is also not a curvature: tidal/Riemann curvature scales as GM/(c^2 r^3), in m^-2.
(6) NICER's mass-radius inference assumes GR light bending and redshift, so 'excluded by GR-consistency of NS pulse profiles' is not a model-independent exclusion. The ringdown bound |eps_Omega| < 0.05 is uncited.

**Proposed improvement.** 1. Pick one cap parameter (alpha or Psi_yield), give the map between them, and retire the other.
2. Regrade the App G card to [L]/[O] (back-substituted, tautological at Earth).
3. Either fix a universal cap and confront it with all bodies, or declare the cap unfalsifiable.
4. Retitle App G (e.g. 'Newtonian-form parameterization and saturation ansatz') and drop the 'curvature' wording or fix its units.
5. Refit NICER profiles under the modified surface metric before claiming exclusion, and cite the ringdown bound.

### 8. [major] The hard cap with the canonical Psi_yield is contradicted by polar gravimetry, and the offered 'gentle' kernels fail at Earth itself

- **category:** physics-validity
- **location:** docs/physics/axg-geometric-derivation-gravity-lattice-yield G.1, G.3.2, G.3.3, G.6 script, provenance note

**Quote.** "$g_{\rm restore} \equiv c^2\Psi_{\rm eff} = c^2\min(\Psi_{\rm geom},\Psi_{\rm yield}) = \min(g_{\rm pot},g_\star).$" / "g_{\rm restore}\ (\le g_\star) & \text{Contact / Surface mode (contact/static)}" / "$\Phi_{\rm J}(x)=1-e^{-x} \quad\Rightarrow\quad g_{\rm restore}=g_\star(1-e^{-x}).$" / script: "YIELD_MODE = "earth"" / "It is a back-substitution from the measured surface gravity of Earth at the standard reference (CODATA g₀=9.80665ms⁻²)."

**Evidence.** (1) WGS84 normal gravity at the pole is 9.83218 m/s^2, 0.26% above g* = 9.80665. Contact gravimeters (spring/superconducting) and free-fall absolute gravimeters agree worldwide at the microGal (~1e-9 g) level. min(g_pot, g*) predicts a 0.26% contact deficit at high latitudes, which is not seen.
(2) I extracted and ran the G.6 script. At Earth it gives g_janssen = 6.21, g_tanh = 7.48 and g_sqrt_janssen = 7.81 m/s^2, against 9.82 measured. At the Moon, sqrt-Janssen gives 3.83 against 1.62 (x2.36). These kernels are offered in G.3.3 without being flagged as excluded.
(3) The script uses g_limit = GM/R^2 = 9.8203, not the text's 9.80665 (a 0.14% mismatch).
(4) g0 = 9.80665 is a conventional standard (CGPM 1901), not a CODATA-measured surface gravity.

**Proposed improvement.** 1. State that Earth is not at yield, or give the cap value that survives polar gravimetry.
2. Mark Phi_J, Phi_H and tanh as excluded by Earth/Moon surface data, or remove them.
3. Make the script use the text's value, or vice versa.
4. Correct the provenance of g0.
5. Register the contact-vs-free-fall difference at the poles as the cap's falsifier.

### 9. [major] The equivalence principle is called 'derived' but not shown; pressure-driven coupling predicts O(1) composition dependence

- **category:** physics-validity
- **location:** docs/physics/17-extensions-optional-reading §17.4.2 Results 2 and 5; docs/physics/axg provenance note; docs/physics/18-time-and-gravity §18.9, §18.10

**Quote.** "Result 5 — Mass-independence (equivalence principle as a derived result). Because the cap responds to the velocity field, not to the mass content of the column, two columns of different mass content fall with the same acceleration in the cap regime." / "Result 2 — Velocity drives pressure. Below the cap, p ∝ ρ v²" / §18.10: "[\mathrm{F?}] & \text{universality }\eta_{\mathrm{rotor}}\!\to\!1\ (\text{LPI}=\text{rotor isotropy; EP its acceleration face})" / §18.9: "the empirical handle is the nuclear $p/n$ systematics"

**Evidence.** The Result 5 argument is about the medium columns, not about how a test body couples to the flow. If the coupling is through the pressure field of Result 2, the force on a body is -V grad p, which scales with its volume, so its acceleration goes as 1/rho_body. For titanium (4.51 g/cm^3) against platinum (21.45 g/cm^3) the ratio is 4.76, i.e. eta ~ O(1). MICROSCOPE measures eta(Ti,Pt) = (-1.5 +/- 2.3 +/- 1.5)e-15.
The grades disagree: App G and §17.4 call the EP a 'derived result', while §18.10 grades it [F?]. In addition, the App G two-channel split (contact reading <= g*, free fall = g_pot) is itself an EP-type discrepancy between weight and free-fall acceleration whenever the cap engages. The empirical handle named in §18.9 ('nuclear p/n systematics') is not the relevant one: the actual constraints come from MICROSCOPE/Eot-Wash (weak EP), lunar laser ranging (Nordtvedt, ~1e-4) and clock-redshift universality.

**Proposed improvement.** 1. Derive the force on a test body in the inflow and show its acceleration is independent of composition, internal binding energy and gravitational self-energy (Nordtvedt) to a stated order.
2. Until then, grade the EP [F?] everywhere, including App G and §17.4.2.
3. Pre-register MICROSCOPE, LLR and Galileo redshift-universality as falsifiers.

### 10. [major] The preferred-frame (Lorentz-ether) sector is never confronted with Michelson-Morley/KT/IS, Hughes-Drever/SME or gamma-ray dispersion bounds, and the corpus's own dispersion scales are already excluded

- **category:** missing-test-or-prediction
- **location:** docs/physics/18-time-and-gravity §18.2, §18.3, §18.10; docs/physics/10 §10.9; spine S0/S3; docs/cosmology/axc-two-length-scales-d-versus

**Quote.** §18.3: "This is Lorentzian ether mechanics (a preferred medium frame, a dynamical contraction) — the opposite of special relativity, which it reproduces." / §18.2: "the jammed medium's rest response is isotropic ($\phi_{\mathrm{jam}}$, $z{=}6$ carry no preferred direction)" / §10.9: "A direct measurement of the transverse angle of visible light against a lattice/anisotropy axis would therefore pin D to 0.001%" / §18.10: "principally $a_0=cH_0/2\pi$ (galactic rotation) and the $\gamma$-ray dispersion mode." / cosmology AXC: "the quadratic dispersion scale is E_(QG)=√(2)hc/(πℓ), which is 115keV for ℓ=D but 882GeV for ℓ=a"

**Evidence.** The physics volume never mentions Kennedy-Thorndike, Ives-Stilwell, Hughes-Drever, the SME, MICROSCOPE or Nordtvedt; I grepped all chapters. Beyond that:
- §10.9 introduces a measurable 'lattice/anisotropy axis' for light. That contradicts the §18.2 isotropy premise on which the exact factor rests. Modern Michelson-Morley experiments bound light-speed anisotropy at ~1e-18 (Nagel et al. 2015).
- I recomputed the cosmology volume's quadratic dispersion scales: E_QG,2 = sqrt(2)hc/(pi*l) = 882 GeV for l = a = 6.33e-19 m, and 115 keV for l = D. The Fermi-LAT GRB 090510 bound is E_QG,2 >~ 1.3e11 GeV (Vasileiou et al. 2013; LHAASO GRB 221009A gives a similar order). Both scales are excluded, by ~8 orders (a) and ~15 orders (D).
- For l = D, photons above hc/D = 255 keV already have lambda < D, yet photons up to PeV are observed propagating over kpc-Gpc distances.
- §18.10 nevertheless places the framework's testability on the 'gamma-ray dispersion mode'.
- The spine's 'linear dispersion omega = cq (verified R^2 ~ 0.99)' is valid only for q*l << 1, and the lattice's full dispersion relation is never stated.

**Proposed improvement.** 1. Add a Lorentz-violation budget section: state the lattice dispersion relation explicitly.
2. Compute the implied Robertson-Mansouri-Sexl parameters (alpha, beta, delta) and SME coefficients (photon k_F/c_munu; b_mu and c_munu for e, p, n), and note which vanish by symmetry.
3. Compare them with MM (~1e-18), KT/IS (~1e-8, Botermann et al. 2014), clock-comparison SME bounds (~1e-29 GeV) and Fermi/H.E.S.S./LHAASO time-of-flight limits.
4. Reconcile the §10.9 lattice axis with the §18.2 isotropy premise.
5. If the gamma-dispersion mode is already excluded, record it (FAILPACK) rather than listing it as the main test.

### 11. [major] An 'infinitely rigid' and 'incompressible' medium contradicts the finite signal speed c^2 = B/rho

- **category:** internal-inconsistency
- **location:** docs/physics/sp-jamming-spine-verified-physical-backbone S2 heading, S2.1, S2.4; docs/physics/17 §17.4.0.1; docs/physics/18-time-and-gravity §18.7

**Quote.** Spine: "## S2. Infinite stiffness→ c²: the single signal speed (verified)" / "S2.1 [axiom]. VP particles are infinitely rigid and fully packing, so the vacuum is a jammed lattice." / S2.4: "reproduced for the harmonic-contact substrate" / §17.4.0.1: "to accelerate a body one must displace the surrounding full, incompressible plenum" / §18.7: "The incompressible mass-current"

**Evidence.** For hard (infinitely rigid) particles, pressure and elastic moduli diverge at jamming, so B -> infinity and c^2 = B/rho -> infinity. An incompressible medium (div v = 0) likewise has K -> infinity. A finite c needs finite contact stiffness, which is why the simulations use harmonic contacts (B_Born ~ O(1) in contact units). That stiffness is an unmeasured parameter, and c itself is an ANCHOR (§16.4), so no value of c follows from the jamming picture. Treating the flow as incompressible is a low-Mach approximation (v << c). It fails exactly where §18.6/§18.8 claim exactness (v_river/c = 0.59-0.69 at neutron-star surfaces).

**Proposed improvement.** 1. Replace 'infinitely rigid' with 'stiff harmonic contacts of stiffness k (unmeasured)', and grade c^2 = B/rho as [L] through the c anchor.
2. Replace 'incompressible' with 'low-Mach approximation', and restrict every 'exact to all orders' claim to regimes where the compressible corrections have actually been computed.

### 12. [major] The quantum diameter D is not a lattice output: A ~ N^-1/3 has no thermodynamic limit, and the quoted matches depend on box size and on mean-vs-median

- **category:** grading-honesty
- **location:** docs/physics/sp-jamming-spine-verified-physical-backbone header cards, S0, S3, S5; docs/physics/11-realization-units-t-rcross (A scaling paragraph)

**Quote.** Spine S3: "The measured circulation length has median4.96pm with best avalanche4.854pm (target4.85);4.96vs4.85is a distribution offset (theAmedian sits 2.3%belowA_{target}=8.20×10^{5}), not a structural error." / §11: "N=200 gives A_med=8.02×10⁵ ... N=750 (seeds 45–48, 104 events), gives A_med=4.76×10⁵, A_mean=5.69×10⁵. The decrease with N is predicted" / header: "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." / "D = 4.8526 pm — Quantum (anchor) diameter that fixes the lattice length scale. [F] forced." / S5: "absolute pm scale (the value4.85) | Am"

**Evidence.** A ~ N^-1/3 means A -> 0 as the box grows. From D = 2*pi*lambda/A:
- N=200 median: D = 4.96 pm.
- N=750 median: D = 8.36 pm.
- N=750 mean: D = 6.99 pm.
The target A = 8.196e5 corresponds to N ~ 187 under the stated N^-1/3 law, so the value of D is set by the choice of box size. The spine's '2.3% below target' uses only N=200. The '0.16%' match (§11) uses the mean at N=750 against an anchor rescaled by N^-1/3. Mean and median differ by 20%, so a 0.16% agreement carries no evidential weight. 'Best avalanche 4.854 pm' is post-selection.
The canonical D = 4.852620477 pm equals 2*lambda_C,e exactly, i.e. it is fixed by the electron mass, not by the 633 nm anchor plus the lattice.
The grades are also inconsistent:
- An empirical anchor and D are carded [F] 'forced', while S5 grades D 'Am'.
- S0 grades rotation => z = 2d as [H]->[V], while S5 open loop (1) says '[H]'.
- An axiom is graded '[F](axiom)'.

**Proposed improvement.** 1. Grade D as ANCHOR (= 2*lambda_C,e).
2. Grade A's absolute value [O], finite-size dependent; report A(N) with a finite-size extrapolation and confidence intervals.
3. Drop 'best avalanche' as evidence.
4. Fix the header cards (anchor -> [L]/ANCHOR; axiom -> its own category) and reconcile the S0 and S5 grades.

### 13. [major] Forced proton radius: global stability does not force the location; the match is a ~3%-level look-elsewhere coincidence quoted against outdated CODATA

- **category:** numerology-look-elsewhere
- **location:** docs/physics/sp-jamming-spine-verified-physical-backbone S4, S5 row 'forced radius'

**Quote.** "The fixed point is unique (one positive root) and globally stable (every positive initial radius converges tox^{*}): the proton radius is dynamically selected, not a fine-tuned balance. Hencer_p=(2/π)λ_{C,p}=0.8412fm (CODATA charge radius0.8414fm,-0.02%)." / S5: "forced radiusr_p=(2/π)λ_{C,p} | [F]/[V] | global stable attractor"

**Evidence.** xdot = alpha x^-5 - x^-4 has x* = alpha for any alpha. The stated F'(x*) = -alpha^-5 = -9.56 is correct, but any 1D flow with a single sign change is globally attracting. The location therefore comes entirely from the postulated exponents (-5, -4) and from putting alpha on the r^-5 term; stability says nothing about 'fine-tuning'.
Numbers: r_p = (2/pi) h/(m_p c) = 0.841236 fm. CODATA 2022 gives 0.84075(64) fm, so the deviation is +0.058% (+0.76 sigma). The quoted -0.02% uses CODATA 2018.
Look-elsewhere estimate: I took the 57 distinct simple prefactors (p/q) pi^k with p, q <= 6 and k in [-2, 2], within [0.25, 4]. The expected number within +/-1 sigma of r_p/lambda_C,p is 0.031, so about a 3% chance per choice. Further trial factors (lambda_C vs reduced lambda_C, charge vs Zemach radius) raise that.

**Proposed improvement.** 1. Grade r_p as [H], conditional on the force-law exponents and coefficient, until those are derived from the lattice.
2. Quote CODATA 2022.
3. Report a look-elsewhere p-value with a declared candidate set.
4. Remove the claim that global stability implies 'not fine-tuned'.

### 14. [minor] Machine ledgers and gate files contradict the chapter's grades and verdicts; one gate passes vacuously at double precision

- **category:** reproducibility-code
- **location:** repro/physics/reports/time_gravity.gate.json; repro/physics/tools/vp_timegravity_ssot.py; repro/physics/tools/vp_cap_depart.py; repro/physics/reports/TIME_GRAVITY_NUMERIC_LEDGER.csv row 20

**Quote.** time_gravity.gate.json: "\"grade\": \"[F?] (exact form conditional on exact-sqrt [O])\"" and for G-CAP-DEPART "\"verdict\": \"REGISTERED\", \"grade\": \"[VP] open prediction\"" / vp_cap_depart.py: "The theory's empirical testability therefore rests on the OTHER channel: cosmological (1+z) time dilation (still open)." / ledger: "Earth,6.961311e-10,0.999999999220376,0.999999999220376,0.000e+00,2.423e-19,[F]@O(c^-2)"

**Evidence.** §18.10 grades G-RIVER and the exact factor [F]. The SSOT module and the gate file still say [F?] and [O]. G-CAP-DEPART is an 'honest negative' in §18.8 but an open, registered prediction in the gate file. The testability channel named in the script (cosmological 1+z) differs from §18.10 (a0 and gamma dispersion). In REL-MATCH, the leading-vs-exact departure for Moon and Earth prints 0.000e+00 against a predicted 2.4e-19, because double precision cannot resolve it; the O(x^2) PASS is therefore vacuous there. This breaks the volume's own single-source rule (§16.2: 'Truth has one address per item; copies are bugs').

**Proposed improvement.** 1. Generate chapter grades, gate JSON and ledger CSVs from one grade table.
2. Compute REL-MATCH with mpmath, or compare series coefficients analytically.
3. Align the testability statement across §18.10, the scorecard and vp_cap_depart.py.

### 15. [minor] §16's mandated reproducibility artifacts are absent, so by its own rules the release is a schema FAIL; the §18 gates were designed after the data they are tested on

- **category:** reproducibility-code
- **location:** docs/physics/16-doi §16.1.3, §16.2.2-§16.2.6, §16.3.3, §16.3.7, §16.5.1, §16.5.3; repro/physics/

**Quote.** "Missing metadata is treated as a failure via (S16_01_TSCH)." / "Uploading/distribution is forbidden in a failing state." / "SSOT: 04_vp_whitepaper/docs/citations/CITE_REGISTRY.csv" / "PASS.rules must be stated in the pre-registration file, and post-run changes are forbidden."

**Evidence.** I searched the whole repo (find). None of protocol.yaml/json, canon_lock.json, realization_lock.json, analysis_lock.json, run_log.jsonl, registry_snapshot.json, release_manifest.json, DOI_MAP.csv, scripts/doi_audit.py or CITE_REGISTRY.csv exists; repro/physics has only registry/vp_locks.csv plus ad-hoc gate JSONs. G-CAP-DEPART cites 'Empirical anchors (web-sourced 2024-2025)' and has no timestamped pre-registration digest. It was constructed after the NICER and GWTC-3 results it is tested against.

**Proposed improvement.** 1. Either implement the §16 schema (even minimally: protocol.json + digest + run_log.jsonl per gate) or rewrite §16 as aspirational policy.
2. Timestamp and hash every gate's thresholds before running it.
3. Mark gates built after seeing the data as post-hoc.

### 16. [minor] Blackbody section contradicts itself on whether quantization is postulated, and is classified GEOM despite importing statistics and the polarization count

- **category:** internal-inconsistency
- **location:** docs/physics/15 §15.5 intro, §15.5.2, §15.5.3; docs/physics/16-doi §16.4.1-§16.4.2

**Quote.** §15.5: "(the Planck hypothesis stated in lattice language, with h_VP calibrated to data; grade CALIB, §16.4)" vs §15.5.3: "This is not “postulating E=n hν” but follows from the fact that n is an event count and thus must be an integer (discreteness)." / §16.4: "Blackbody spectral form | GEOM" with "GEOM: closes using only integer/geometric definitions internal to the document, with no dependence on external numerical values or definitions." / §15.5.2: "Under linear elastic response, the strain rate ε is proportional to frequency. Hence the minimum barrier energy ε_b required to penetrate the shell ... satisfies"

**Evidence.** That n is an integer does not make each crossing cost exactly h*nu. The latter is the quantization postulate, as the section's own opening admits. The spectral form depends on Boltzmann weights, k_B T and the imported 8*pi prefactor (two polarizations), so it does not meet the GEOM definition. An elastic energy barrier scales with strain amplitude squared, not strain rate, so 'eps_b ~ strain-rate ~ nu' does not follow. h is listed as an ANCHOR (§13.1) and h_VP as a separate CALIB fitted to blackbody data, without stating whether h_VP = h is tested or assumed.

**Proposed improvement.** 1. Delete the 'not postulating' sentence.
2. Reclassify the spectral form as CALIB/[H].
3. Either derive eps_b ~ nu or label it an ansatz.
4. State h_VP = h as an identification ([L]) or report the fitted h_VP/h with an uncertainty.

### 17. [minor] The spin-like label's parity behaviour is wrong for spin: spin projection is parity-even

- **category:** physics-validity
- **location:** docs/physics/15 §15.3.5 Lemma T-S1

**Quote.** "Spatial parity reverses the rotation sense (θₛ↦-θₛ, so Φ↦-Φ and σ↦-σ): the label set is a single parity orbit +1,-1, a forced Z₂."

**Evidence.** Angular momentum and spin are axial vectors. Under 3D spatial inversion, S -> S, so a spin projection on a fixed axis is P-even (it is T-odd). theta_s -> -theta_s is a mirror reflection in the sector plane, not parity. A label that flips under parity behaves like helicity, or like a 2D reflection, not like the 'two-valued spin projection' it is mapped to. A Z2 also cannot reproduce non-commuting spin components or the cos^2(theta/2) Stern-Gerlach statistics.

**Proposed improvement.** 1. Replace 'parity' with 'mirror reflection', or map sigma to time-reversal.
2. Note that SU(2) structure (non-commuting components, 4*pi periodicity) is [O].
3. Add a Stern-Gerlach angle-dependence gate.

### 18. [minor] The 'four-wall theorem' is labelled a proven no-go, but it is an obstacle list whose Wall 3 premise the spine contradicts

- **category:** grading-honesty
- **location:** docs/physics/18-time-and-gravity §18.5; docs/physics/17 §17.4.4 Walls 3-4; spine S3

**Quote.** §18.5: "(the four-wall theorem, §17.4.4: a proven no-go, grade [O])" / §17.4.4: "[F] derived no-go" / Wall 3: "the largest natural combinatorial factors are products of integers up to 7 times powers of π, of order 10⁰ to 10². The 22-order shortfall is structural, not a tuning gap." / Wall 4: "This is the standard hierarchy problem of mainstream physics." / spine: "the10^{5}-fold optical-to-quantum bridge and the2π closure are supplied by the lattice"

**Evidence.** The spine itself credits the lattice with dimensionless factors of 1e5-1e6 (A ~ 8e5; D/a ~ 7.7e6), so 'at most 10^2' does not hold. Exponential suppression (e.g. e^-x with x ~ 51 gives 7e-23) readily produces 1e-22. Wall 4 appeals to the hierarchy problem rather than proving anything. The same result is graded [F] in §17.4.4 and [O] in §18.5.

**Proposed improvement.** 1. Call it an 'obstacle enumeration' ([H]), not a theorem.
2. Use a single grade everywhere.
3. Discuss exponential or dynamical suppression as a possible escape route, instead of excluding it by assertion.

### 19. [minor] Cross-volume packing-fraction inconsistency: 0.7405 is labelled random close packing, while physics uses phi_jam ~ 0.64

- **category:** cross-volume
- **location:** docs/index.html (VP Chemistry & EM card); AGENTS.md §1; docs/physics/18-time-and-gravity §18.8

**Quote.** homepage: "φ_RCP = 0.7405 single anchor φ_RCP=0.7405" / AGENTS.md: "Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405)." / §18.8: "($z{=}6$, $\phi_{\mathrm{jam}}\!\approx\!0.64$)"

**Evidence.** pi/(3*sqrt(2)) = 0.74048 is the FCC/HCP (Kepler) maximum packing, not random close packing (~0.64). The chemistry hub correctly calls 0.7405 the 'close-packing fraction'. The physics volume's argument about isostatic, marginally rigid jamming (z = 6) belongs to the random-packing point, phi ~ 0.64. A reader following AGENTS.md gets the wrong substrate.

**Proposed improvement.** 1. Relabel 0.7405 as phi_FCC (ordered close packing) on the homepage, in AGENTS.md and in the manifest.
2. State once which packing (FCC 0.7405 or RCP/jamming 0.64) is the vacuum substrate, and use it consistently across volumes.

**Strengths noted:**
- The honest negative is genuinely valuable. §18.8/G-CAP-DEPART concludes that the gravity sector has no surviving prediction distinct from GR, and puts the framework's testable weight elsewhere. That is rare, good practice.
- App G's provenance note states that Psi_yield = 9.80665/c^2 is back-substituted, not derived. §17.4.4 refuses to canonize the operator's unreleased full-gravity simulation ('operator testimony, not evidence').
- The Michelson-type round-trip formula T(theta; kappa, v) in §18.2 is algebraically correct; I re-derived it. The deterministic modules reproduce their ledgers bit-for-bit (EXACT_SQRT_LEDGER.csv regenerated identical).
- §15 labels its QM correspondences as notation mappings, marks H-Pmap/H-S1/H-STAT1 as hypotheses, and forbids standard-QM axioms as derivation grounds. The lattice commutator [X,P] = (i hbar/2)(T + T^-1) and the Robertson inequality derivation are mathematically correct.
- Spine S2.4 uses real isostatic-jamming physics: relaxed shear modulus -> 0 at z = 2d with finite bulk modulus, located through five independent observables, and cites O'Hern/Wyart/Olsson-Teitel. The fixed-point stability derivative F'(x*) = -(pi/2)^5 is computed correctly.
- §18.7's explicit separation of the 1/r^2 mass-current from the r^-1/2 potential velocity shows that the author noticed the tension. It only needs to be followed to its consequence.


## review:extensions

### 1. [critical] The framework's own event rates break the equivalence principle at about 10^-4, yet Result 5 grades the EP as [F] 'derived'

- **category:** physics-validity
- **location:** docs/physics/17-extensions-optional-reading §17.4.0 ('From annihilation rate to force'), §17.4.2 Result 5, §17.4.4(ii) one-scalar reduction and (v) p1; cross-ref §12 (nu_e,can), W0 scorecard (nu_p,can), §18.10 ([F?] universality)

**Quote.** Using the framework's mass–rate identity m = 2π · ν_ann (the rectification bracket α/δ = 2π, see §5.0)" | "In this framework the annihilation rate Q plays the role of the source strength." | "inflow-momentum chain (F=Qₜp₁(r), p₁=m_q v(r), void-forbidden continuity" | "p_{1}^{(\oplus)}\;=\;\frac{g\,m_{\mathrm H}}{\nu_{\mathrm H}}\;=\;5.597\times10^{-29}" | "Result 5 — Mass-independence (equivalence principle as a derived result). Because the cap responds to the velocity field, not to the mass content of the column, two columns of different mass content fall with the same acceleration in the cap regime." | §12: "(i) the canonical electron event rate ν_e,can:=1 (9.3)" | W0: "ν_p,can=3π⁴=292.227s⁻¹

**Evidence.** nu_H is never defined in the physics volume. It appears only inside the G formula. Inverting the stated p1 gives it: nu_H = g·m_H/p1 = 9.80665×1.6735575e-27/5.597e-29 = 293.227 s^-1 = 3π⁴ + 1 = nu_p,can + nu_e,can. (p1 recomputes to 5.5970e-29, and m_q(M1, φ=0.633) to 2.890e-34, confirming this.) The framework's rates therefore give annihilation rate per unit mass nu_p/m_p = 3π⁴/(6π⁵ m_e) = 1/(2π m_e) for the proton and nu_e/m_e = 1/m_e for the electron, a ratio of 2π. The 'identity' m = 2π·nu fails for the electron (2π·nu_e,can = 2π ≠ m_e/m_e = 1). Per (ii) the force on a test body is F = Q_t·p1, so its acceleration a = Q_t p1/m_t goes as Q_t/m_t = κ_p[1 + (2π−1) f_e], where f_e is the electron mass fraction. Here I made the most favourable assumption: neutrons and binding energy take the proton ratio. f_e(Ti-48) = 22×5.4858e-4/47.948 = 2.517e-4 and f_e(Pt-195) = 2.195e-4, giving η(Ti,Pt) = 5.283×3.22e-5 = 1.70e-4. MICROSCOPE (Touboul et al. 2022, PRL 129, 121102) measured η(Ti,Pt) = (−1.5 ± 2.3 ± 1.5)×10^-15, so the model is excluded by about 4×10^10. Be/Ti gives η = −4.3e-5, against the Eöt-Wash bound (0.3 ± 1.8)×10^-13. Result 5 addresses only the column's mass content, not composition. The single hydrogen ratio (nu_H/m_H) used in the G formula silently assumes the universality that Result 5 claims to derive. §18.10 already grades universality [F?], which is inconsistent with [F] here.

**Proposed improvement.** Downgrade Result 5 (and the scorecard and Read-First statement 'equivalence principle derived') from [F] to [H]/[O]. Register a gate G-EP: derive Q/m for e, p, n and for nuclear binding energy from the canon, then require |η(Ti,Pt)| < 1e-14 and |η(Be,Ti)| < 3e-13 before any EP claim. Replace 'm = 2π·ν_ann' with the ratio form m_p/m_e = 2π·nu_p/nu_e and state explicitly that m/nu depends on species. Alternatively, declare that gravitational coupling goes as mass and not as annihilation rate. In that case withdraw 'annihilation rate is the source quantity' and accept that the EP is an input. Define nu_H explicitly wherever it is used.

### 2. [critical] §17.4.3 forbids GM/R² and §17.4.6 claims altitude-independent surface gravity, while the same chapter, its SSOT code and Kill criterion 4 rest on 1/R²

- **category:** internal-inconsistency
- **location:** §17.4.1, §17.4.2 Result 4, §17.4.3, §17.4.6, §17.4.7; §17.4.4(ii); repro/physics/verification_dossier/GRAVITY_REPRODUCIBILITY_MAP.md; governance Kill criterion 4 (01-governance); prologue Misreading 4

**Quote.** Experimental observation (and numerical simulation in the bundle) shows a velocity-dependent rise to a plateau." | "Therefore, whatever Newtonian gravity is, in this framework it cannot be the local cap mechanism; the two phenomena live at different scales and the framework currently addresses only the cap." | "Why the surface gravity is independent of altitude column-height above each body — Beverloo-type height-independence." | "forward closure reproduces g=GM/R² at machine precision (the reduction is exact Newton re-parameterized — stated plainly)" | SSOT: "| 자유공기 기울기 | −2·g0/R | g0,R_E | −0.3079 mGal/m | [F] |" | Kill criterion 4: "A controlled experiment that exhibits clean 1/R² dependence without a saturation onset, at scales where the cap should be active, would falsify the gravity portion of the framework." | "Take a jammed lattice with no rigid container walls

**Evidence.** The measured free-air gradient is −0.3086 mGal/m. The repo's own gate G-GRAV-FREEAIR passes by computing the Newtonian −2g0/R = −0.3079 mGal/m (+0.24%). That is a clean 1/R² dependence at the very surface where the cap is claimed to be active, which is exactly the Kill-criterion-4 condition. A height-independent g would give a gradient of 0. At 400 km (ISS), g = 9.820×(6371/6771)² = 8.69 m/s², 11.5% lower. The Moon's orbital acceleration, 2.70e-3 m/s² = g(R⊕/r)², confirms 1/r² out to 60 R⊕. §17.4.3 cites no experiment for the 'velocity-dependent rise to a plateau' of gravity at fixed R. Beverloo's law (W = Cρ√g(D−kd)^{5/2}) is empirical, contains √g, and so cannot explain g. Its height independence comes from Janssen wall-friction screening, but the setup has 'no rigid container walls' and the engines use 'friction 0'. Meanwhile §17.4.4(ii) reproduces GM/R² exactly, and §18 uses √(2GM/r).

**Proposed improvement.** Withdraw §17.4.3 and the 'height-independence' claim wherever it appears: Result 4, §17.4.6, §17.4.7, App G, the §14 table entry 'height-independent', governance A8(ii), and prologue Misreading 4. Either declare Kill criterion 4 triggered for the reading 'cap = surface gravity', or restrict the cap explicitly to contact/normal-force mechanics (as §18.8 already does) and give one quantitative, pre-registered departure from Newton with its size. Cite the 'experimental observation' or delete it. Do not invoke Beverloo or Janssen in a wall-less, frictionless setting.

### 3. [critical] The headline 'g* = c²·Ψ_yield [F] forced' is a definition (Ψ_yield := g*/c²), so its body-independence says nothing, and App G's saturation kernels are an unlocked choice

- **category:** circularity
- **location:** §17.4.2 Results 2 and 7, §17.4.6, §17.4.7; W0 scorecard headline card; App G (axg) provenance note and code

**Quote.** Result 7 — Saturation relation. g_(*) = c²· Ψ_yield as a structural relation (skeleton)" | "Ψ_yield=g_(*)/c²; see App G" | W0: "g* = c²·Ψ_yield — Gravity-cap mechanism: a yield-limited acceleration ceiling (Beverloo-type discharge). [F] forced. canonical derivation §17" | "the cap formula g_(*)=c²·Ψ_yield is universal across bodies" | "The numerical value of Ψ_yield at each body, back-substituted from the observed surface gravity there." | App G code: "psi_earth_from_g = g_pot_earth / c2" ... "g_restore = g_limit * frac" | "The ratio g_(⊕)/g_Moon≈ 6.05 from microscopic primitives without additionally specifying the lattice yield-threshold ratio at the two bodies.

**Evidence.** Because Ψ_yield is defined as g*/c², 'g* = c²Ψ_yield' is an identity, and it is 'universal across bodies' only because it is a definition. Back-substituting Ψ_yield per body means the 'explanation' of inter-body differences is g = c²(g/c²). Newton predicts g_Moon/g⊕ = 1.6243/9.8203 = 0.1654 from M and R; §17.4.6 concedes the framework does not. App G computes Ψ from Newton's GM/R² (YIELD_MODE='earth') and then applies one of five hand-picked kernels. At x = 1 these give Earth's own g as 9.82 (hard clip), 9.72 (soft64), 7.48 (tanh), 6.21 (1−e^{−x}) or 7.81 m/s² (sqrt-Janssen): a 37% spread from an unlocked functional choice. With a universal g_limit, Jupiter (24.8 m/s²) and the Sun (274 m/s²) are capped at ≤ 9.82 m/s². Spectroscopic solar log g = 4.44 (cgs), which is exactly the hydrostatic 'contact' gravity, rules that out. So the universal-Ψ reading is falsified and the per-body reading is empty.

**Proposed improvement.** Present g* = c²Ψ_yield as notation with no grade, and remove it from the one-page scorecard's headline cards. Change 'explains inter-body differences' to 're-parameterizes'. If a cap is kept, give Ψ_yield an independent operational definition that does not use g (e.g. p_yield/(ρ_eff c² ℓ), with p_yield and ℓ measured in the jammed-lattice simulation), so that g* = c²Ψ becomes a testable prediction. Lock a single kernel in analysis_lock before any comparison. State that the Sun and white dwarfs (log g ≈ 8) test any universal cap.

### 4. [critical] One medium, two velocity fields: the 1/r² point-sink inflow (≈194 km/s at the surface) contradicts the √(2GM/r) 'river' (11.2 km/s) used for time dilation, and the sink's velocity potential is mistaken for a force potential

- **category:** physics-validity
- **location:** §17.4.0 (sink-Green's-function chain; grade line), §17.4.4(ii) implied consistency surface; cross-ref §18.6–18.7

**Quote.** $\nabla^{2}\phi = -\sigma \;\Longrightarrow\; \phi(r) \propto \frac{Q}{4\pi r},$" | "and the resulting gradient force on a test element of the surrounding lattice is" | "Grade: [F]for the inflow law; [F]for the sink-Green's-function equivalence." | "the implied consistency surface (drift ≈194 km/s at Earth's surface, ρ_eff≈3.06 kg/m³, B_eff≈2.7×10¹⁷ Pa under M1) is reported for R1, not claimed." | §18.6: "a clock held static in a gravity well is therefore a clock at rest in a \emph{moving} medium — equivalently, a clock moving relative to the local medium at the free-fall ("river") velocity." | §18.7: "The incompressible mass-current that books the sink's steady consumption falls as $1/r^2$; the time-dilation velocity is the potential (free-fall/river) velocity and falls as $1/\sqrt r$

**Evidence.** For a point sink obeying continuity, φ is a velocity potential: v = ∇φ ∝ Q/(4πr²). A medium element's acceleration is Dv/Dt = ∇(v²/2) ∝ Q²/r⁵, not Q/r². The electrostatic analogy therefore gives a velocity, not a force. Recomputing the M1 surface (Q⊕ = M⊕ν_H/m_H = 1.046e54 s^-1, V_q = 5.98e-35 m³, φ = 0.633) gives v = 193.8 km/s, which matches the stated drift. If clocks slow with velocity relative to the local medium, this flow gives v²/2c² = 2.09e-7 at the surface, against GR's GM/(Rc²) = 6.96e-10 (a factor of 301), and a radial profile of r⁻⁴ instead of r⁻¹. Conversely, the river v = √(2GM/r) (11.19 km/s at the surface) has ∇·v = (3/2)√(2GM) r^{-3/2} ≠ 0. That requires absorption spread through all of space, which contradicts 4πφr²v = Q_s V_q with a point sink. A single medium has a single velocity at each point, and §18.7's 'must not be conflated' does not say which velocity the medium actually has.

**Proposed improvement.** Choose one kinematic field and derive both the force law and the time dilation from it. For a Painlevé–Gullstrand river, drop the point-sink continuity and the m_q chain, or specify a distributed absorption density ∝ r^{-3/2} and its physical origin. For the 1/r² mass current, show why clocks do not respond to it. Downgrade the §17.4.0 [F] grades to [H] until then. Add a gate G-ONEFIELD: one velocity field must reproduce both GPS/Gravity Probe A dilation and 1/r² acceleration.

### 5. [major] The 'fullness theorem' is proved without a sink term and then used where annihilation is exactly such a sink; positivity is also not fullness

- **category:** math-error
- **location:** §17.4.0.1 (fullness theorem and its four consequences); cross-ref §11.6, §14

**Quote.** The “empty space is forbidden” rule used above is not an extra assumption: it is a theorem of the full-packing axiom (VP-A2) together with continuity. Let a number density n obey ∂ₜ n+∇·(nmathbf v)=0 under a no-flux boundary" | "Inflow = gravity (derived, §17.4.0): annihilation would open a void; (fullness) forbids it" | "The speed limit c (derived, §11.6): the full jammed medium has a single signal speed, the elastic wave speed c²=K/ρ_eff; there is no faster channel because there is no void to bypass through." | §11: "That the surviving elastic response is a single longitudinal speed c²=B/ρ is now demonstrated, not asserted" | §14: "its transverse, propagating part is light

**Evidence.** The Lagrangian result n = n₀exp(−∫∇·v) > 0 holds only for source-free continuity. Annihilation adds −σ: dn/dt = −n∇·v − σ. With ∇·v = 0 this gives n = n₀ − σt, which empties at t = n₀/σ. The theorem therefore says nothing about the one case it is invoked for. Even without sinks it guarantees only n > 0, not n ≥ n_J (jammed): ∇·v = 1/τ gives n = n₀e^{−t/τ}, which falls below any jamming threshold while satisfying the theorem. On the speed limit, an elastic solid has two signal speeds, c_L² = (K + 4G/3)/ρ and c_T² = G/ρ. §14 makes light the transverse part, while §11.6 says the surviving speed is longitudinal (B/ρ). Near isostatic jamming G/K → 0, so c_T → 0.

**Proposed improvement.** State void exclusion as an axiom, i.e. the hard constraint n ≡ n_J, which then forces ∇·v = −σ/n_J (exactly the sink-flow model), and drop the word 'theorem'. Grade items 3–4 (inertia, third law) as [H] analogies. Reconcile light's transverse polarization with a longitudinal c² = B/ρ, or show which modulus sets the transverse speed.

### 6. [major] The four-wall 'theorem' ([F] derived no-go, 'a proof') rests on false premises, aims at the wrong target (the conventional g⊕ rather than G), and its own pinned note contradicts it

- **category:** grading-honesty
- **location:** §17.4.4 claim strip, Walls 2–4, recovery program, pinned status correction; §17.4.7

**Quote.** [F] derived no-go" | "The single anchor λ_ref=632.99 nm enters into dimensionless ratios via small geometric factors (2, π, integers up to 7)." | "the largest natural combinatorial factors are products of integers up to 7 times powers of π, of order 10⁰ to 10². The 22-order shortfall is structural, not a tuning gap." | "This is the standard hierarchy problem of mainstream physics." | "(b) the value emerged with no such input — which would be a counterexample to this theorem." | "its conclusion is henceforth to be cited in the corrected form: “not derivable at presently accessible computational scale without an external input”, never “not mappable.”" | §17.4.7: "the four-wall theorem (§17.4.4) is a derived no-go—a proof, by enumeration of the four obstacles, that the absolute magnitude cannot follow from these microscopic inputs alone

**Evidence.** Wall 3's premise is contradicted by the framework's own factors: 6π⁵ = 1836 (10^3.26), D/r_p = 6π⁶ = 5768, A = 880,919, D/a = 7.67×10⁶, and the split integer N = 10¹² (a = λ_ref/N, §11). The ratio arithmetic itself is right: Ψ/λ⁻¹ = 6.9e-23 = 10^-22.16. Wall 2 relies on a = 6.33e-19 m, which is λ_ref/10¹², a declared convention (N-invariance, §1.8.2), not a physical scale. Wall 4 misstates the hierarchy problem, which concerns the radiative instability of the Higgs mass (m_H ≪ M_Pl), not the underivability of force constants. g⊕ = 9.80665 is the CGPM 1901 standard. Earth's actual g runs from 9.780 to 9.832 m/s² (Somigliana, in the repo) and depends on M⊕, R⊕ and Ω, so no theory derives it from microphysics. The universal target is G, or α_G = Gm_p²/(ħc) = 5.906e-39, which is the real analogue of α_em. A 'proof' that admits a possible counterexample and can be overturned by an HPC run is not [F]. The pinned note ('resource bound', 'never not mappable') and §17.4.7 ('proof ... cannot follow') say opposite things.

**Proposed improvement.** Retitle it 'four obstacles' and grade it [O] with a list of obstacles. Restate the open problem as deriving α_G (or G in lattice units), which is independent of any body. Apply the 'α_em class' analogy to α_G, not to g⊕. Remove the hierarchy-problem framing from Wall 4. Correct Wall 3 to acknowledge the framework's own 10³–10¹² factors. Make §17.4.7 match the pinned correction.

### 7. [major] The Pantheon+ fit is reported as 'degenerate' although the chapter's own χ²/dof values imply Δχ² ≈ 95; the cosmology volume breaks §17.2.5's embargo, and the reciprocity justification points in a circle

- **category:** cross-volume
- **location:** §17.5 head box; §17.2.5 mandatory Gate stack; cosmology/07-non-expanding-lattice-optics-cosmology (Simulation and verification; Status; Open/flagged)

**Quote.** fit there to the real Pantheon+ compilation (χ²/dof=0.50 vs 0.44 for ΛCDM; honestly recorded as degenerate, no observational advantage claimed)" | §17.2.5: "in that state one cannot output strong cosmological conclusions such as “dark energy is unnecessary.”" | cosmology Ch.7: "No dark energy is needed." | "compilation (1580 supernovae with z>0.01, calibrators removed)" | "with a single marginalised offset (absorbing H₀ and the absolute magnitude)" | "The data therefore do not distinguish them" | cosmology: "is justified at the level of the lattice optics in the physics volume" | physics §17.5: "conditionally on a reciprocity/focusing step which that volume itself registers as its own hard gate

**Evidence.** Both models have one free offset (Ω_Λ = 0.7 is fixed), and there are about 1579 degrees of freedom. Δχ² = (0.50 − 0.44)×1579 ≈ 95, or 79–111 allowing for 2-decimal rounding. That is a likelihood ratio of about e^47 ≈ 10^20, a decisive preference for ΛCDM, not degeneracy. χ²/dof = 0.44 also means the diagonal errors are about 1.5× too large; rescaling to χ²/dof = 1 gives Δχ² ≈ 215. 'Comparable to per-supernova scatter' is the wrong criterion when 1580 SNe are combined. §17.2.5 forbids 'dark energy is unnecessary' until PASS_COSMO-ALT, whose TOL, BLR and SINK gates are unmet, yet the downstream volume says so outright. A grep of every physics chapter finds no reciprocity/Etherington derivation, so each volume points to the other for it.

**Proposed improvement.** Report Δχ², ΔAIC and ΔBIC using the full Pantheon+ STAT+SYS covariance. Replace 'degenerate' and 'No dark energy is needed' with the quantitative preference, and quote Δχ² rather than χ²/dof ratios in §17.5. Enforce the §17.2.5 embargo across volumes, e.g. a cross-volume gate that fails any 'no dark energy' string while PASS_COSMO-ALT is unmet. Either derive d_A = d_L/(1+z)² in the physics volume or remove the cosmology volume's claim that it is justified there.

### 8. [major] §17 calls ℓ_rot an 'optional', not-yet-adopted constant, but the core route already sets D = ℓ_rot, which §2 forbids without versioning

- **category:** internal-inconsistency
- **location:** §17.1.5, §17.3.2 OP-ROT, §17.5.2 handover note; cross-ref §2 (notation rule), §3.4, §9, §10.9, §14.0, Executive Summary

**Quote.** Treat the rotational length ℓ_rot as an optional extension constant. If ℓ_rot is adopted, fix the following rule:" | "(OP-ROT) Conditions for adopting ℓ_rot: specify the minimum requirements (observations/experiments/estimators) needed when including ℓ_rot in a LOCK." | "The lattice-step mechanism link (per-step loss ε at the ℓ_rot scale)" | §2: "Therefore, replacing ℓ_rot by D_anch, or redefining the meaning of D_anch from ℓ_rot, is forbidden." | §10: "(each of effective diameter D=ℓ_rot)" | §3.4: "Concept links: D=ℓ_rot is computed in §9.4

**Evidence.** The core chain (§3.4, §9.4, §10.9's light-angle falsifier, §14.0's rotating quanta) and the Executive Summary all identify ℓ_rot with the canonical diameter D = 2λ_C,e = 4.8526 pm. §2 declares that identification forbidden unless promoted through the §2.2.6 versioning procedure. §17 still treats adopting ℓ_rot as an open problem (OP-ROT) and an optional lock. So a quantity that is labelled optional already carries the framework's sharpest optical prediction, and §17.5 hangs the redshift loss step on it.

**Proposed improvement.** Either run the §2.2.6 version bump that promotes ℓ_rot to canon (D_anch), then delete the 'optional' wording and OP-ROT, or remove D = ℓ_rot from §3.4, §9, §10 and §14. Record the decision in the VH reclassification log.

### 9. [major] Material from the 'optional' chapter is graded [F] and exported as headline results, contrary to the prologue's rule that extensions are [H]

- **category:** grading-honesty
- **location:** §17 page header (answer line, claim strip, vp-cards); §17.4 promotion note; prologue §0.2.1 (C10); W0 scorecard; Read-First; §18.10

**Quote.** The rotation/anisotropy extension includes the following two categories. Grade [F] forced." | "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." | "m_p/m_e = 6π⁵ — Proton-electron mass ratio as 2π·ν_p = 6π⁵ (−19 ppm vs measurement). [F] forced." | prologue: "All extensions are conditional claims ([H]) with declared regimes and closures" | "The locks and derivations remain here in §17.4 (SSOT unchanged); §18 references them." | Read-First: "gravity as sink inflow with the equivalence principle" / "derived (§17.4). The physics is decided here.

**Evidence.** One chapter-level grade of [F] covers pure definitions (§17.1–17.3), an embargoed open-tier module (§17.5, graded [H]/INCONCLUSIVE in its own text) and back-substituted gravity. The prologue says extensions are [H] and 'do not strengthen or weaken the conclusion status of required-route results', yet the gravity cap lives in this 'optional' chapter and is the canonical SSOT for the featured §18 and for the scorecard's [F] card. An empirical anchor labelled [F] 'forced' contradicts the grade legend; it should be [L]. The 6π⁵ card on this page reads [F] while differing from CODATA 1836.15267343(11) by −18.8 ppm, which is 3.1×10⁵ σ. The EP is [F] in §17.4.2 but [F?] in §18.10.

**Proposed improvement.** Replace the chapter grade with per-section grades: definitions ungraded, §17.5 [H]/[O], and the §17.4 items graded individually. Move the §17.4 SSOT into §18 or a required-route appendix so that 'optional' means optional. Relabel the anchor [L]. Give 6π⁵ a grade that reflects its measured discrepancy. Harmonize the EP grade, taking the lower of the two.

### 10. [major] The SSOT gravity gates are identities or circular (a hard-coded 0.0 and Newton-derived densities), and the text blames a rounding residue on rotation

- **category:** circularity
- **location:** §17.4.4(iii) mapping-symmetry lemma; repro/physics/tools/vp_gravity_ssot.py; GRAVITY_REPRODUCIBILITY_MAP.md gates G-GRAV-TERRAIN, G-GRAV-BODY

**Quote.** (verified
0.16519 vs 0.16531, the residue being the bodies' known rotation/oblateness offsets)" | code: "v["tc_residual_vp_newton"]=0.0   # 정의상 동일 1/r² 적분 → 항등" | "v["g_moon"]=C["G0"]*(C["RHO_MOON"]/C["RHO_E"])*(C["R_MOON"]/C["R_E"])" | "G_MOON   = 1.62,             # 달 표면중력 (m/s^2)" | "TAU_Q  = 1.62e-20,           # 격자 틱 τ_q = D/c (realization, 3 s.f.)" | "2) 중간 단계에서 절대 반올림하지 않는다.

**Evidence.** G-GRAV-TERRAIN compares a hard-coded 0.0 against a threshold of 1e-6, so it cannot fail. G-GRAV-BODY uses NASA mean densities, which are themselves 3M/(4πR³) from Newtonian GM, so it checks Newton against Newton. Its −0.01% agreement comes from the rounded baseline 1.62: the true lunar GM/R² = 4.9028e12/1.7374e6² = 1.6243, so the SSOT's 1.6199 is actually −0.27% off. In the text, 0.16519 = (3340/5514)(1737.4/6371) and 0.16531 = (M_m/M_E)(R_E/R_m)². Both are pure Newtonian ratios with no rotation term. Their 0.07% gap equals the density rounding (true ρ_Moon = 3342.2, not 3340). Rotation at 45° is 1.7e-3 of g, 25× larger than the gap and absent from both ratios. Rounding τ_q to 1.62e-20 (exact D/c = 1.61866e-20) breaks the script's own rule 2. It turns G* = 5.295e-28 (text) into 5.30e-28 (drift gate EXPECT '5.30'). The SSOT's N_samples = 1/(v/c)² = 3.57e54, while the §17.4.4 text says N ~ 10^48, which assumes σ = 1e-3.

**Proposed improvement.** Relabel identity checks as '[identity], not evidence' and remove them from the PASS tally. Compare the Moon against GM-based g with unrounded inputs. Delete the 'rotation/oblateness' explanation. Compute τ_q from D/c without rounding. Reconcile the N-samples definition between the text and the code.

### 11. [major] The cited gravity evidence modules and reduced engines are missing from the repo, the page's code link is dead, result numbering is off, and the 'vr = const' check is 2D

- **category:** reproducibility-code
- **location:** §17.4.4 (R1 decision aid, (iv), (v)), §17.4.5; page claim strip link; repro/physics/verification_dossier/GROUNDING_LEDGER.md

**Quote.** Five independent reduced engines (a 2D jamming MD with conservative harmonic contacts, perfect elasticity," | "— 80 runs in all, zero tuned parameters" | "(module 07_absorption_rule_study/:" | "the hourglass law (throughput pinned to the event rate, load-independent over a 25,794× range;" / "Beverloo-type, Result 2)" | "equal acceleration (the up–down difference is ν-invariant; the equivalence principle as a result," / "Result 3)" | "the inflow continuity vr=const (matched to 3%)" | GROUNDING_LEDGER: "| 흡수 운동량 규칙 (R1) | 07_absorption_rule_study | [V] |" | link: "repro/physics/17-extensions-optional-reading/

**Evidence.** find over the whole repo turns up no 07_absorption_rule_study, 08_gravity_mapping_attempt, 09_cap_calibration_attempt or 10_column_engine, none of the five reduced engines, and neither the modules/rot_aniso nor the modules/jet_regime tree that §17.1.7/§17.2.7 'fix'. repro/physics holds only tools/*.py. The page's GitHub link goes to a directory that does not exist. Even so, GROUNDING_LEDGER grades 07 and 10 as [V]. Under the chapter's own v34 rule, evidence that cannot be re-executed is testimony. In §17.4.2 Beverloo is Result 4 and the EP is Result 5, but §17.4.5 cites them as Results 2 and 3. 'vr = const' is two-dimensional (cylindrical) continuity; a 3D point sink needs vr² = const, so the engines never test the claimed 3D 1/r² law.

**Proposed improvement.** Publish the modules, with seeds and RESULTS sha256, under repro/physics/17-extensions-optional-reading/, or downgrade their [V] to testimony. Fix the link and the result numbering. Add a 3D engine test of v·r² = const. Mark the module file trees as 'planned' until they exist.

### 12. [major] No energy-sink gate for gravitational inflow, although the chapter's own consistency surface implies about 6×10^30 W dissipated at Earth

- **category:** missing-test-or-prediction
- **location:** §17.4.2 Result 3; §17.4.4(ii) consistency surface; contrast §17.5.5

**Quote.** Result 3 — Momentum only, energy zero at the cap. The cap state transmits momentum density but supports no net energy flow (the kinetic energy is dissipated locally into the jamming stiffness)." | "(drift ≈194 km/s at Earth's surface, ρ_eff≈3.06 kg/m³," | §17.5.5: "Therefore a sink model is required: where does the lost energy go (lattice heating, transfer to background radiation, local re-emission, etc.)?

**Evidence.** From the M1 numbers: Earth absorbs Q⊕ = 1.046e54 events/s × m_q = 2.89e-34 kg, i.e. ṁ = 3.0e20 kg/s, one Earth mass every 5.5 h. The kinetic energy dissipated 'locally' is ½ṁv² = 0.5×3.0e20×(1.94e5)² = 5.7e30 W. That is 1.5×10⁴ solar luminosities and 1.2×10¹⁷ times Earth's 47 TW heat flow. The ram pressure is ρv² = 1.1e11 Pa. §17.5.5 rightly requires a sink model before any photon energy loss can be accepted, but gravity's inflow gets no such requirement.

**Proposed improvement.** Register G-GRAV-SINK, symmetric with §17.5.5: any recovered R1 specification and any m_q/ρ_eff surface must state where the inflow's energy and mass go, and must pass Earth's heat-flow and mass-constancy budgets (e.g. lunar-laser-ranging limits on dM/dt) before it is registered.

### 13. [major] The anisotropic backbone (arg max of a product of link weights) is degenerate or ill-posed, and the normalization and dilution kernel hold only in 3D although u ∈ R^d

- **category:** math-error
- **location:** §17.1.3 (normalization, dilution kernel), §17.1.4 (backbone), §17.2.3 Earth correspondence

**Quote.** $\begin{equation} W(\gamma):=\prod_{\hat{\ell}\in\gamma} w(\hat{\ell}) \end{equation}$" | "\operatorname*{arg\,max}_{\gamma\in\Gamma(\mathbf{x}\to\mathbf{y})} W(\gamma)" | "$\begin{equation} \langle g\rangle_{\mu} := \frac{1}{2}\int_{-1}^{1} g(\mu)\,d\mu = 1 \end{equation}$" | "\mathbf{u}\in\mathbb{R}^d" | "Domain Λ: corresponds to a latitude–longitude band (2D manifold) on a rotating planet.

**Evidence.** On a hypercubic lattice every minimal x→y path has the same number of links in each direction, so W is the same for all of them and the arg max is a total tie. Δ_bb would then depend only on the tie-break. If longer paths are allowed, ⟨g⟩ = 1 with β_g > 0 forces g > 1 in some directions, and detours along w > 1 links raise W without limit (short of self-avoidance). The 'backbone' then becomes a space-filling snake. (1/2)∫dμ is the isotropic measure only in d = 3. In d = 2, the setting of the chapter's own Earth example, g = 1 + bP₂(μ) averages to 1 + b/4 (numerically 1.125 for b = 0.5). The kernel (a/R)² is likewise 3D-specific; the general form is (a/R)^{d−1}.

**Proposed improvement.** Define the backbone as a minimum-cost (Fermat travel-time) path with cost Σ|ℓ|/g(μ), or as the current-carrying backbone of a resistor network with conductances g(μ(ℓ̂)). Use the d-dependent measure ∝ (1−μ²)^{(d−3)/2}dμ with its own normalization, and the kernel (a/R)^{d−1}. Add a worked 2D and 3D example with one locked g(μ).

### 14. [major] The limitation taxonomy has no class for 'model falsified by data', which allows failures to be relabelled as regime or measurement issues

- **category:** grading-honesty
- **location:** §17.3.1 (limitation classes), §17.3.6

**Quote.** Limitations are classified not as “model failure” but as “outside-regime application” or “non-verifiability.”" | "Limitations are classified, not confessed" | "$\begin{equation} \mathcal{C}_{\mathrm{lim}} = \{\mathrm{REGIME\_OUT},\mathrm{IDENTIFIABILITY},\mathrm{NUMERICS},\mathrm{MEASUREMENT},\mathrm{DEPENDENCY}\} \end{equation}$

**Evidence.** None of the five classes, nor REVOKED (which covers integrity and no-tuning violations only), records the case where a pre-registered prediction fails on data. That is a textbook conventionalist stratagem. It also conflicts with the corpus rule '반증 = 발견' (falsification = discovery) and with the concrete failures found above: the free-air gradient against height-independence, and MICROSCOPE against the EP.

**Proposed improvement.** Add a class FALSIFIED = {gate id, dataset, version, magnitude of failure}, and require that REGIME_OUT can only be declared in the protocol before the run. Log the gravity-sector failures (height-independence, EP composition) under it.

### 15. [major] The G-GRAV-MAP supersession gate is too loose (a factor 2–3 band on m_q) and its band edges do not follow from the stated inputs

- **category:** missing-test-or-prediction
- **location:** §17.4.4(ii) and (v)

**Quote.** Gate G-GRAV-MAP is registered: any future derivation
or R1-recovered absorption spec must land m_q inside the convention band
[1.51,4.57]×10⁻³⁴ kg — PASS would close the absolute magnitude and supersede the
four-wall theorem by construction" | "the m_q band is narrowed to the sphere branch
[2.28,4.56]×10⁻³⁴ kg =128–256 eV/c²" | "with the residual O(1) being the inflow-anisotropy factor η∈[1,1.82]

**Evidence.** At fixed convention G ∝ m_q, so a PASS pins G down only to within ×3.02 (first band) or ×2.00 (narrowed band), while G is known to 2.2e-5 (CODATA 2018). The lower edge 2.28e-34 matches no tabulated convention (M1 = 2.890, M2 = 4.566). 4.56/2.28 = 2.00, but the stated η range is 1.82, so the band cannot be rebuilt from the inputs given. Allowing four conventions plus a continuous η creates a look-elsewhere freedom that the gate never counts.

**Proposed improvement.** Lock the convention and η in analysis_lock before any derivation. Make the pass criterion |G_pred/G_CODATA − 1| ≤ the derivation's own stated uncertainty (a first-principles claim should aim for ≤ 1%). Report the number of conventions tried as a trials factor. Derive the band edges explicitly.

### 16. [minor] Defects in the jet and regime definitions: bipolar jets are capped at J ≤ 1/2, the symbol M is overloaded, the balance identity uses unsigned counts, §17.2.6 is missing, and 'singularity replacement' is mislabelled

- **category:** math-error
- **location:** §17.2.2 (event flux, consistency identity, collimation index), §17.2.3 (P_J, M_J), §17.2.4 title, §17.2.5 PASS_SINK, numbering 17.2.5→17.2.7

**Quote.** A value near 1 indicates a strongly collimated outflow, while a value near 0 indicates a widely distributed flux over directions." | "where Ξₛ(n,e,k) is an indicator for whether a sector-s event occurred on link e from node n at time-window k." | "$\begin{equation} P_J := \frac{1}{M}\sum_{i=1}^{M} \mathbb{I}[\mathcal{J}_i\ge \mathcal{J}_{\star}] \end{equation}$" | "17.2.4 Core-saturation regime (singularity replacement) (definition)" | "\frac{I_{\mathrm{sink}}}{I_{\mathrm{bg}}^{\max}}\le 1+\epsilon_{\mathrm{SINK}}^{\star}

**Evidence.** With a single cone, a symmetric bipolar jet (the usual astrophysical case) can reach at most J = 0.5, and isotropic outflow gives the cone's solid-angle fraction (1−cosθ)/2, e.g. 0.017 for 15°, rather than 0. M is used for the flux window length, for the number of sub-windows (P_J, M_J) and for the axis-fluctuation metric M_J/M_*. A 0/1 indicator has no orientation, so ΔN_Σ = ΣJ = Σ F_ev cannot express net outflow minus inflow, and the storage term is missing. Allowing I_sink up to (1+ε)·I_bg^max lets a prediction exceed an upper bound. The section numbers jump from 17.2.5 to 17.2.7. 'Singularity replacement' asserts a physical result, whereas the section only forbids claiming singularities, and §18 says the geometric channel is exact Schwarzschild, which includes r = 0.

**Proposed improvement.** Use axial (±d̂) cones and normalize J against its isotropic baseline. Rename the persistence count (e.g. N_w). Use oriented flux (out − in) and add the storage term. Require I_sink ≤ I_bg^max. Renumber the sections. Rename E-CORE to 'core-saturation regime (no singularity claim)'.

### 17. [minor] LaTeX residue and broken rendering in key passages, including a heading that reads 'does emphnot predict'

- **category:** presentation-rendering
- **location:** docs/physics/17-extensions-optional-reading/index.html: page abstract, §17.4.4 computational wall and (v) p1 alt text, §17.4.6 heading, §17.5 banners, §17.5.2/§17.5.6, equation cross-references throughout

**Quote.** What the hourglass theorem does emphnot predict (and what is explicit future work)." | "noindent[OPEN-TIER PHENOMENOLOGY — S17.5.6 hard Gates unmet" | "footnotesize(relocated from S10.8 in v0.5.0" | "gtrsim10¹⁵ cells vs  10³: short by  10¹²" | "(1.58×10⁶)  10⁻²² shows" | "so seed
averaging would need N 10⁴⁸" | "supplies the map zleftrightarrow D" | "for zll 1 one has" | "\Om\ \text{input-equivalent}" | "Jets, cores, and cosmology are filed as regimes with conditions — not as conclusions. 2π." | "(S17_02_Dz_def) is incompatible

**Evidence.** Missing ∼/≈ symbols make orders of magnitude read as bare numbers (' 10² events', 'N 10⁴⁸'). Raw macros show in the text: emph, noindent, footnotesize, gtrsim, leftrightarrow, ll, an undefined \Om, '[O]{}', '[H]{}', 'hatd', 'mathbf v', 'sₚath'. The HTML contains 86 equation references rendered as raw labels such as '(S17_02_Dz_def)' rather than numbers. The abstract ends with a stray '2π.'. 'Rewriting in C gains <10²' is unescaped HTML.

**Proposed improvement.** Run the TeX→HTML converter with macro definitions for \emph, \noindent, \footnotesize, \gtrsim, \sim, \ll, \leftrightarrow and \Om (or replace them). Number equations and resolve the cross-references. Escape '<'. Add a CI check that fails the build on residual backslash-free macro names.

### 18. [minor] The optional route promised in the prologue and scorecard (SOC, throughput ceiling, scale-up, gates G-ANISO/G-SOC/G-PATH/G-CAP/G-UP) is not what Ch. 17 contains, and the companion volume goes by different names

- **category:** structure-redundancy
- **location:** prologue §0.2.4–0.2.5; W0 W.2.1 table; §17.1–17.2 gate names; §17.4.6/§17.5 volume references

**Quote.** SOC amplification extension: locks event-cluster (avalanche) definitions and amplification coefficients, and derives distributions/scale invariance/pinning conditions." | W0: "| Rotation-drive length ℓ_rot (protocol/realization family) | Anisotropy / SOC / jets (optional route; Ch. 17)" | "(G-AN1) Normalization check for g(μ)" | "companion Earth–Cosmos volume (“The Earth–Cosmos Volume:
Gravity, Planetary Motion, Galactic Dynamics, and Cosmology as Vacuum Inflow — A Simulation-Grounded Account,”

**Evidence.** Ch. 17 has no SOC, throughput-ceiling or scale-up sections; SOC lives in §10.3. It uses the gate names G-AN1–3, G-ROT, G-JET1–3 and G-LOG in place of the promised G-ANISO/G-SOC/G-PATH/G-CAP/G-UP, and it 'derives' nothing, offering only definitions. The companion volume at DOI 10.5281/zenodo.20568874 is catalogued as 'Vacuum-Inflow Cosmology' but is called the 'Earth–Cosmos volume' here.

**Proposed improvement.** Bring the prologue's and scorecard's list of optional-route contents into line with what Ch. 17 actually contains, or point to §10.3 for SOC. Use one set of gate names. Refer to the companion volume by its catalogue title and id.

**Strengths noted:**
- §17.5 and §17.2.5 set out the right discriminators for a static-space redshift: time dilation, Tolman surface brightness, blurring, the energy sink and the CMB T(z). They cite the literature (Lubin & Sandage 2001; Goldhaber et al. 2001) and put an explicit embargo on cosmological conclusions. This is exactly the gate stack a referee would ask for.
- The §17.5.3 mechanism note is admirably candid. It says achromaticity is asserted, not derived, and names the ν-dependence of Compton, Rayleigh and plasma losses.
- The §17.4.4 recovery programme is a model of self-audit. The historical 9.8 m/s² claim is demoted to testimony, and forensic reading of the old record exposes two sim-fitted O(1) factors (1.05, 1.735) and a targeted v*. The conditions R1–R4 for re-adjudication are listed in advance.
- Most of the chapter's arithmetic reproduces exactly from stated inputs: G* = gD/c² = 5.295e-28, the m_q table (162.1/256.1/84.9/134.1 eV), p1 = 5.597e-29, the drift of 193.8 km/s, and the fall-time tick counts 1.93e11 and 6.15e13.
- The κ calibration/validation split, the CR/LOCK admission gates (PASS_ID/STAB/TRACE/NT) and the DEPRECATED/REVOKED rules are sound research-governance practice.
- The ratio idea in the mapping-symmetry lemma, testing ratios in which the unknown absolute cancels, is a good design principle once it is applied to non-circular inputs.
- §18.8's recorded honest negative, that the gravity sector is observationally degenerate with GR, is valuable and should be carried back into §17.4's wording.


## review:appendices

### 1. [critical] App M's absolute Higgs mass depends on the arbitrary split N = 10^12 and on which laser line is the anchor. The 'N-invariance' check tests only a ratio that holds by definition.

- **category:** numerology-look-elsewhere
- **location:** docs/physics/axm-mass-grand-unification-geometric-differentiation (M.0, M.1(1), Theorem M.2.1); 13-mass-u-lat-m-h §13.3/§13.3.7; 01-governance §1.8.2; 11-realization §11.2.1 [D-11.2-2]; w0 §W.3.2 table

**Quote.** App M: "m_H=\frac{U_{\mathrm{lat}}}{5\pi}"; §11.2: "N = 10^{12}."; §1.8.2 table: "| m_H/U_lat | 1/(5π) | 1/(5π) | 1/(5π)" and "Confirmed by the released code; no N enters the closure equations."; W.3.2: "N=10¹² | [H] | (declared split integer) | a chosen split; no dimensionless output depends on it (§1.8.2 N-invariance)"; §13.3: "The PDG-tabulated Higgs boson mass is m_H^exp=125.20± 0.11GeV" and "[H]{} for closing the coefficient at the -0.40% level under the single anchor λ_ref=632.99nm"

**Evidence.** m_H = U_lat/(5π) = h·c·N/(5π·λ_ref), so m_H scales linearly with N. The dimensionless ratio m_H/m_e = N·D_anch/(10π·λ_ref). Computed values: N=1e9 gives 244.02; N=1e12 gives 244,022; N=1e15 gives 2.44e8; N=2^40 gives 268,305 (m_H = 137.10 GeV). The measured ratio is 245,010. The §1.8.2 table lists only m_H/U_lat = 1/(5π), which is the definition σ_eff = 5π and so is trivially N-invariant. The W.3.2 statement 'no dimensionless output depends on it' is therefore false. λ_ref = 632.99121257859865746 nm is c/f of the iodine-stabilised He-Ne standard (c/473612353604 kHz reproduces all digits). Using the other RCROSS anchor listed in realization_lock (532 nm) gives m_H = 148.37 GeV. The residual (124.695−125.20)/0.11 is −4.6σ, which the text never states. Look-elsewhere: the integer family n·π^k (n≤12, k≤3) has 24 members per decade, so the expected number of chance hits within ±0.40% is 0.08. The rational family p/q·π^k (p,q≤12) has 123 members per decade, giving 0.43 expected hits. This is before pricing the choice of N and of the laser line. The 'No-tuning fingerprint' (refusing 4.98π) guards the wrong knob; the knob that sets the GeV value is N.

**Proposed improvement.** Downgrade the absolute m_H to [O] 'numerical observation', or to [H] conditional on N, until N (equivalently a) is fixed by physics independent of λ_ref. Add m_H/m_e and m_H/m_p rows to the §1.8.2 N-invariance table showing their linear N-dependence, and correct the W.3.2 row. Quote the residual as −4.6σ against PDG 2024. Add a look-elsewhere paragraph with the enumerated candidate family. State plainly that the claim is m_H ≈ 10^12·hc/(5π·λ_HeNe(I2)).

### 2. [critical] App K's own regime gate predicts that vacuum waves break down near the lattice scale. The framework never computes this, and photon data rule out an ordinary lattice by many orders of magnitude.

- **category:** missing-test-or-prediction
- **location:** docs/physics/axk-methodological-validation-via-classical-gas (K.0, K.2, K.3, K.4 table, K.5); axl-4-3-1-state-dictionary L.1, L.5; cross-ref w0 §W.3 (G_relaxed row), 11-realization §11.2

**Quote.** K.3: "breaks down (strong kinetic attenuation / non-continuum behavior) as Kn_λ→ O(1)"; K.4: "| Wave type | Longitudinal pressure wave | EM / lattice wave in VP medium" and "| Auxiliary macro input | η (transport / damping gate) | VP transport/damping gate (protocol-defined)"; K.0: "Given: macroscopic wave data and macroscopic transport data of a known discrete medium."; K.2: "together with γ≈ 1.4 and molar mass M≈ 28.97g/mol."; L.5: "In VP language, the background vacuum is State 4 (a jammed stiff lattice) that supports coherent propagation."; W.3: "G_relaxed→0 at z_iso=2d=6"

**Evidence.** (i) The air inversion is not black-box. It needs the molecular mass m = M/N_A, which is a microscopic input, plus an assumed hard-sphere Chapman–Enskog model. The VP column has no measured transport coefficient ('protocol-defined'), so the step that makes the air inversion well-posed has no vacuum counterpart. (ii) The vacuum analogue of Kn ~ O(1) is never evaluated. For a lattice of spacing a = 6.33e-19 m the Brillouin cutoff is λ_min = 2a, i.e. E_max = hc/2a = 979 GeV. For D = 4.85 pm it is 128 keV. LHAASO (Nature 594, 33 (2021)) observed photons up to 1.4 PeV, whose wavelength 1.24e-21 m is about a/500. A nearest-neighbour lattice gives v_g/c ≈ 1−(ka)²/8. For the 31 GeV photon of GRB 090510 (z = 0.903; Abdo et al., Nature 462, 331 (2009)), ka = 0.099, so Δv/c = 1.2e-3. Over ~2.3e17 s of travel that is a delay of ~3e14 s; the observed delay is ≲1 s, a 14-order conflict. (iii) The main text places the vacuum at the isostatic point (G→0, z = 6). There the jamming literature (Silbert–Liu–Nagel PRL 95, 098301 (2005); Wyart–Nagel–Witten EPL 72, 486 (2005); Xu et al. PRL 102, 038001 (2009)) shows the boson-peak frequency ω* ∝ Δz → 0, and plane waves above ω* become diffusive (Ioffe–Regel crossover). That contradicts L.5's 'stiff lattice that supports coherent propagation'.

**Proposed improvement.** Add a vacuum dispersion gate (e.g. G-DISP). Compute ω(k) and ω* from the dynamical matrix of the jammed packing already used for c²=B/ρ (the bundle already produces dos_omega_star.png). Map the result to photon energy through the declared lattice scale. Confront it with Fermi-LAT GRB 090510, LHAASO PeV photons and the MAGIC/H.E.S.S. Lorentz-violation bounds (quadratic E_QG ≳ 1e11 GeV). Then either derive exact non-dispersion together with a reason why ω* does not go to 0, or record the issue as [O] with the obstacle stated. Reword K.0/K.4 to admit that M and the collision model are microscopic inputs with no VP analogue.

### 3. [major] App M's 'mass grand-unification theorem' and its gate G-RATIO-MASS-UNIFICATION are true by definition; the gate can only fail on file sealing.

- **category:** circularity
- **location:** docs/physics/axm-mass-grand-unification-geometric-differentiation M.0, M.2.1, M.3, M.4, M.5; repro/physics/verification_dossier/SIMULATION_GROUNDING_AUDIT.md; VH v0.2.1

**Quote.** M.3: "By definition, ideally I_H=Iₚ=Iₑ=1 should hold (a channel that numerically reconfirms identical definitions)."; M.4: "PASS ⟺ dev_max≤ dev_tol AND (sealing/lock_id/schema match)"; dossier: "번들 게이트 로스터 = 시뮬 검증된 주장:" … "| G-MH | m_H | PASS |", "| G-ME | m_e | PASS |", "| G-MP | m_p | PASS |"; VH v0.2.1: "the resistance integral Sₚ=λ_C/a is bookkeeping and the realization scale a cancels."

**Evidence.** The definition m(X) := U_lat/σ_eff(X) makes I = m·σ/U_lat ≡ 1 identically, so dev_max is only floating-point roundoff (~1e-16). The next finding demonstrates this: App M's own script produces m_e = 5.04 MeV, ten times wrong, and I_e is still exactly 1, so the gate passes. For the electron and proton, U_lat/S = hc/λ_C with a cancelling. The 'unification' therefore says only that each mass equals hc divided by its Compton wavelength, which is the definition of the Compton wavelength. The only content beyond definitions is m_H, which is covered in the first finding. Yet the dossier lists G-MH, G-ME and G-MP as 'simulation-verified claims'.

**Proposed improvement.** Retitle App M 'bookkeeping identity m = hc/λ_C (a cancels)' and drop 'theorem' and 'grand unification'. Replace G-RATIO-MASS-UNIFICATION with gates against external data at pre-registered tolerances: m_p/m_e vs CODATA in ppm, and m_H vs PDG in σ. Remove G-MH, G-ME and G-MP from every list of simulation-verified claims.

### 4. [major] App M's script still puts the withdrawn π² factor into the electron mass (gives 5.04 MeV), although the version history says App M was synchronised with App E.

- **category:** reproducibility-code
- **location:** docs/physics/axm-mass-grand-unification-geometric-differentiation M.5 (verify_appendix_M.py) vs M.1(3); axe E.0 banner; vh v0.5.0

**Quote.** App M script: "r_e = (D_anch/2.0) * delta" / "S = r_e / a_m" / "m_e = U_lat_GeV / S"; App M prose M.1(3): "Define the electron resistance integral over the mass-bearing Compton length (§13.5.4; not the event-rate radius rₑ=r₀δ, which governs only νₑ=1)"; VH v0.5.0: "App. E corrected in place to the §13.5.4 canon (spurious π² removed; script asserts 0.511 MeV) with App. M synchronized"; App E banner: "which inserts a spurious factor π² into mₑ (yielding ≈ 5.04 MeV)"

**Evidence.** Using the script's own inputs: U_lat = hc/a = 1958.703 GeV. With the correct length, S = (D/2)/a = 3.833e6 and m_e = 0.51100 MeV. The script instead uses S = r_e/a = 3.884e5, giving m_e = 5.0434 MeV, a factor π² = 9.87 too large and exactly the error App E's banner withdraws. Because I_e = m_e·S/U_lat = 1 regardless, the script's gate still reports PASS. The same script also reports m_p = 938.312 MeV from the rounded locked r_p (see the App P finding).

**Proposed improvement.** Change the script to `lam_Ce = D_anch/2.0; S = lam_Ce/a_m` and add App E's assertion `abs(m_e/5.10999e-4-1)<2e-3`. Correct the VH v0.5.0 sentence. Add a CI job that runs every published snippet (App E/F/M/P/R) against the shipped lock files and compares its output with the numerals printed on the pages.

### 5. [major] Measured anchors and back-substituted quantities are badged '[F] forced', and the grade letters mean different things in different documents.

- **category:** grading-honesty
- **location:** repro/physics/registry/vp_locks.csv (drives vp-cards on vh, axd, axe, axf, axm, axr pages); axd D.0; w0 §W.3.2 legend; 08 §8.0.6(C); vh preamble and v0.4.1; AGENTS.md §5; repro/physics/IRREPRODUCIBILITY_LEDGER.md

**Quote.** vp_locks.csv: "anchor,λ_anchor,632.99 nm,Single empirical anchor (DOF = 1); the only measured length input to the framework.,F"; "d-anch,D,4.8526 pm,Quantum (anchor) diameter that fixes the lattice length scale.,F"; "cap,g*,c²·Ψ_yield,Gravity-cap mechanism: a yield-limited acceleration ceiling (Beverloo-type discharge).,F"; "mp-me,m_p/m_e,6π⁵,Proton-electron mass ratio as 2π·ν_p = 6π⁵ (−19 ppm vs measurement).,F"; App E: "coinciding with the §13.5.4 calibration node (an anchor, not a prediction)"; W.3.2: "Ψ_yield=1.091×10⁻¹⁶ m⁻¹ | [O] | (intentionally no code) | back-substituted per body"; W.3.2 legend: "[V]{} simulation-measured (script+seed in bundle); [H]{} calibrated/locked by a stated procedure"; §8.0.6: "It is graded [F]{} under that lock"; VH: "No [F]{} coefficient was changed to close a residual."

**Evidence.** By the framework's own vocabulary an empirical anchor is [L] (AGENTS.md) or [H] (W.3.2), never [F]; yet λ_ref and D (which is m_e via D = 2h/(m_e c)) carry [F]. For g*: c²·Ψ_yield = 8.98755e16 × 1.091e-16 = 9.805 m/s², i.e. the magnitude is g back-substituted; only the functional form could be [F]. For 6π⁵: 1836.118109 vs 1836.152673426(32) is −18.8 ppm, about 10^6 σ at the 1.7e-11 relative uncertainty. A relation contradicted at that level cannot be 'forced' without the residual being carried as an [O] obstacle. The [V] tag means 'simulation-measured' in W.3.2 but 'passed a test built to falsify it against external data' in AGENTS.md. [H] means 'calibrated' in W.3.2 and 'hypothesis (가설)' in the irreproducibility ledger. On the VH headline: if D is [F], its re-anchoring (v0.2.1/v0.4.1) from the jamming value 4.8542 pm, which gives m_e = 0.51082 MeV (−0.033%), to 2λ_Ce, which makes m_e exact by construction, is an [F] value changed to close a residual. That contradicts the VH sentence 'No [F] coefficient was changed to close a residual'. The App D line 'Rectification constants … locked by geometric-mean/projection conventions' also sits uneasily beside their [F] badges.

**Proposed improvement.** Grade λ_ref, D_anch (= m_e) and N as [L]/anchor. Display g* as 'form [F] / magnitude [O]'. Display 6π⁵ as '[F] structure; −18.8 ppm residual [O] (obstacle: …)'. Show conditional grades explicitly, e.g. [F | MAP-1,2]. Publish one grade-vocabulary file and generate AGENTS.md §5, W.3.2, the ledgers and the site cards from it. Reword the VH sentence to acknowledge the D re-anchoring.

### 6. [major] The claim of exactly one degree of freedom contradicts App E, App D and App C: there are two measured anchors (λ_ref and m_e) and a chosen split N, plus two further locked inputs (r_p and Δt).

- **category:** internal-inconsistency
- **location:** 01-governance §1.8.1; axe E.0/E.3; 13-mass-u-lat-m-h §13.5.4; axd D.0/D.1; axc C.2/C.3; 03-axioms §3.4

**Quote.** §1.8.1: "Single empirical anchor (1 DOF): λ_ref=632.99nm, used to fix a once." and "The total tunable DOF count is therefore exactly one"; §13.5.4 card: "The mass sector spends its one calibration here — and says so."; App D: "Dₐnch Anchor length (canonical input)."; §3.4: "D_anch:=2λ_(C,e)=4.8526pm — the same 632.99 nm / mₑ anchor used everywhere else"; App C canon_lock: "\"r_p_m\": 0.8412e-15,"; realization_lock: "\"dt_s\": 1.86e-21,"

**Evidence.** D_anch = 2h/(m_e c) is fixed by the measured electron mass. Nothing in the chain derives λ_ref/λ_Ce = 260,886.6. The only proposed link, D = 2πλ/A, uses a simulated A with 7% spread, and with the locked A it gives 4.515 pm, not 4.853 pm (see the A-overloading finding). So the outputs depend on two independent measured continuous anchors: λ_ref (which sets a, U_lat and m_H) and m_e (which sets D, r_p and m_p). On top of these is the discrete choice N = 10^12. r_p = 0.8412 fm and Δt = 1.86e-21 s are also locked inputs, consumed by the App F/M/P/R scripts and by the §9.4 and §13.4 numerics. The phrase '632.99 nm / m_e anchor' merges two independent measurements into one.

**Proposed improvement.** Rewrite the DOF ledger as: continuous anchors {λ_ref, m_e via D_anch}; discrete choice {N}; locked conveniences {r_p lock, Δt}, or remove the latter. Add a dependency table showing which outputs are anchor-free (m_p/m_e, r_p/λ_C,p), which depend on m_e (r_p in fm) and which depend on λ_ref and N (m_H). Fix the 'only measured length input' card accordingly.

### 7. [major] The '+61 ppm cross-check' is 19 ppm of real residual plus 42 ppm from rounding. The locked r_p = 0.8412 fm is the model's own value rounded, not a measurement.

- **category:** circularity
- **location:** vh v0.2.1 and v0.4.1; axc C.2 canon_lock; 09 §9.4; 13 §13.3 'No-tuning fingerprint'; w0 cross-check paragraph; repro/physics/verification_dossier/NUMERIC_LEDGER.md

**Quote.** VH: "the forced (2/π)λ_(C,p)=0.8412 fm is now its +61 ppm cross-check (equivalently +19 ppm vs. the mₚ/mₑ=6π⁵ residual)"; VH: "the length-anchored νₚ=D_anch/(2rₚ)δ=292.245 is retained as a +61 ppm cross-check only"; VH v0.4.1: "r_(pₘ)=8.412×10⁻¹⁶ unchanged (the validator-enforced proton radius)"; §13.3: "(−0.018% vs CODATA 0.8414 fm)"

**Evidence.** (2/π)λ_C,p = 4ħ/(m_p c) = 0.8412356 fm, and the locked 0.8412 fm is this value rounded to 4 significant figures (−42.4 ppm). The prediction D/(6π⁶) = 0.8412515 fm sits +18.8 ppm above the exact (2/π)λ_C,p (the 6π⁵ residual) and +61.2 ppm above 0.8412. So 61 ≈ 19 + 42 (rounding); the two are not 'equivalent'. Likewise ν_p: 292.2452 (locked r_p), 292.2328 (exact (2/π)λ_C,p) and 3π⁴ = 292.2273. The 'cross-check' therefore compares the model with a rounded copy of itself. The meaningful external test is D/(6π⁶) against CODATA 2022 r_p = 0.84075(64) fm: +596 ppm, +0.78σ. (Against the CODATA 2018 value 0.8414(19) quoted in the text it is −0.08σ; §14 cites CODATA 2022 for α while r_p uses 2018.)

**Proposed improvement.** Remove r_p_m from canon_lock, or relabel it '(2/π)λ_C,p rounded — not data'. Delete the '+61 ppm cross-check' wording on the roughly 10 pages where it appears. Quote the r_p prediction (0.84124–0.84125 fm) against CODATA 2022 and muonic hydrogen (0.84087(39)) in σ. Pre-register it against upcoming measurements (PRad-II, MUSE, AMBER) with an explicit kill threshold (e.g. >3σ).

### 8. [major] App F gives a pure number the units s⁻¹, interprets a residual that is only a rounding artifact, and its body contradicts its own banner.

- **category:** unit-dimension
- **location:** docs/physics/axf-discrete-decomposition-hypothesis-event-rate F.0 banner vs body, F.1 (interpretation), F.2 (82×4−9×4), F.4 script

**Quote.** "Section 9.4 derived ν_p,can≈ 292.245156s⁻¹ from only LOCK inputs (D_anch, rₚ, δ)"; "Using the LOCK value of 9.4 ((S09_04_nup_numeric)), N_act = 292, ε = 0.2451560251…"; "ε can be interpreted as a residual oscillation/fluctuation component remaining due to the limits of rectification (δ) and integer lattice matching."; banner: "(its residual 0.245 is not 3π⁴'s 0.227)"; "Core discrete number: N_core:=82 (consistent with the core definition in 7.2)"

**Evidence.** ν = s_p·δ = D/(2r_p)/π² is metres over metres and so dimensionless. Attaching s⁻¹ presupposes one event per SI second, a human unit defined by caesium-133, which makes the claim unit-dependent. The residual ε changes with the rounding of r_p: 0.2452 (locked 0.8412), 0.2328 (exact (2/π)λ_C,p), 0.2273 (3π⁴), 0.1757 (CODATA 2018 r_p), 0.4016 (CODATA 2022 r_p). A quantity that moves by a factor of 2 with the choice of rounding carries no physics, so the Zitterbewegung-like reading rests on an artifact. The banner and §9.4's title ('νₚ,can=3π⁴≈292.23 — length cross-check') say the canonical value is 3π⁴, yet the body still calls 292.245 'ν_p,can' and 'the LOCK value'. For 4·82 − 4·9 = 292, the '4-point' and '9-input' units are, as F.2 admits, chosen after the fact, and no count of alternative decompositions is given. §7 has no §7.2 defining the core; per VH v0.2.0, 82 is sourced in §7.1/§8.0.

**Proposed improvement.** Drop s⁻¹, or state the unit-time assumption explicitly and grade the per-second reading [O]. Rename ν_p,can to ν_p,len in F.0–F.4. Either delete the ε interpretation or add the rounding-dependence table above. Move 4(82−9) into a numerology box with a count of alternative decompositions. Fix the §7.2 pointer.

### 9. [major] App P's proton-mass 'derivation' just restates r_p = 4ħ/(m_p c), an uncited prior-art relation. Its script prints the rounded-lock value instead of the claimed prediction.

- **category:** physics-validity
- **location:** docs/physics/axp-lattice-origin-proton-mass-integral P.1, P.3, P.4; 13-mass-u-lat-m-h §13.4 card; sp-jamming-spine S4

**Quote.** P.1: "Under the same version, assume the following two links are locked." (r_p/L_q=2/π, L_q=λ_C); P.3: "m_p=\frac{h\,c_{\mathrm{ref}}}{\lambda_C} =\frac{2}{\pi}\frac{h\,c_{\mathrm{ref}}}{r_p}"; §13.4 card: "mₚ=hc/λ_C=0.93831 GeV ($a$ cancels)"; S4: "The fixed point is unique (one positive root) and globally stable (every positive initial radius converges tox^{*}): the proton radius is dynamically selected, not a fine-tuned balance."

**Evidence.** m_p = 2hc/(π·r_p) is equivalent to r_p = 4ħ/(m_p c) = 0.8412356 fm. That numerical relation has been published before (e.g. Haramein 2013, r_p = 4ℓ_P m_P/m_p) and is not cited. App P's script uses the locked r_p = 0.8412 fm and gets m_p = 938.312 MeV (+42 ppm); §13.4 prints this as 0.93831 GeV. The claimed prediction, 6π⁵·m_e, is 938.254 MeV (−18.8 ppm). With measured radii the route gives 938.089 MeV (CODATA 2018) or 938.814 MeV (CODATA 2022, +0.058%), with a ±0.076% error inherited from r_p, about 40× worse than 6π⁵. The 'forced' 2/π comes from ẋ = αx⁻⁵ − x⁻⁴. Its fixed point is x* = α only because the exponents were chosen to differ by 1 (in general αx^-p = x^-q gives x* = α^{1/(p−q)}). Any one-dimensional ODE with a single sign change is globally stable, so the simulation confirms algebra, not physics.

**Proposed improvement.** Recast App P as 'the r_p–m_p relation r_p = 4ħ/(m_p c)'. Grade it [H], conditional on the exponent choice (−5, −4), unless those exponents are derived independently. Cite the prior art. Make the r_p comparison (CODATA 2022, +0.78σ) its genuine test. In §13.4 print m_p = 6π⁵·m_e = 938.254 MeV, not the value computed from the rounded lock.

### 10. [major] Several downgrades recorded in the version history have quietly come back in later text: the 'three independent roads' card for D, α_em in the canonical list, α_em as a use of the forced lemma, r_p as an input, and a cherry-picked 0.04% precision.

- **category:** internal-inconsistency
- **location:** 03-axioms §3.4 (v0.8 section card + body); 08 §8.0.6(D); 14 §14.5; axc C.2; vh v0.2.1, v0.4.1, v0.5.0; w0 §W.3.2

**Quote.** §3.4 card: "[F] multipath anchor identity … One quantum diameter, three independent roads, one stated width."; VH v0.4.1: "The presentation of D as “three independent routes” is replaced by the precise statement: D is a single anchor"; §3.4: "By contrast the canonical π/integer results — 3π⁴, 6π⁵, 5π, αₑₘ⁻¹, α=2/π, δ=1/π², 82=81+1 — contain no D and carry their stated (exact or independently-graded) accuracy"; §8.0.6(D): "Fine structure (§14.5.3): N=7 shell signs ⇒ 7-1=6 free signs" … "the recurrence across three independent constants is a structural signature, not three tunings."; §14.5: "Many distinct closed forms built from small integers and π land on 137.036 to comparable accuracy"; VH v0.2.1: "The three computed values (electron-Compton 4.8526, proton 4.8523, jamming 4.8542 pm) span 0.04%"; W.3.2: "a selected best-avalanche from a 7% distribution (median 4.96 pm)"

**Evidence.** The v0.8 auto-generated section card for §3.4 restores the retracted 'three independent roads' and grades it [F], directly above body text that says the opposite. α_em⁻¹ was demoted to coincidence/non-evidence in v0.5.0 but still appears in §3.4's list of canonical results, and §8.0.6(D) still counts it as evidence of a 'structural signature'. r_p was reclassified as a prediction in v0.2.1 but remains an input in canon_lock (App C) and is asserted by the App M/P/R scripts. The '0.04% span' is set by 4.8542 pm, the best avalanche selected against a 4.85 target from a distribution with median 4.96 pm (+2.2%, 7% width). The 4.8523 pm 'proton' value is 6π⁶ times the rounded 0.8412. An unselected statement would be: jamming median 4.96 pm, +2.2%, about 0.3 widths away — corroborative, but nowhere near 0.04%.

**Proposed improvement.** Add a build gate that scans the cards, answer-first and abstract layers for retracted phrases ('three independent', α_em in canonical lists) and fails the build if any appear. Remove α_em from §3.4 and from §8.0.6(D), or mark it 'demoted use'. Remove r_p_m from canon_lock inputs. State D's jamming corroboration as median ± width rather than the selected best avalanche.

### 11. [major] Apps H and L use two-dimensional rigidity thresholds (4/3/2) that contradict the main text's 3D isostatic point z = 6. App H also reuses the symbol δ and omits its table, coupling constant and code.

- **category:** internal-inconsistency
- **location:** docs/physics/axh-theory-geometric-rigidity-v2-1 H.1–H.4; axl-4-3-1-state-dictionary L.1, L.3, L.5; cross-ref w0 §W.3 (z_iso=2d=6), 05 (δ=1/π²), axb B.0 SSOT rule

**Quote.** App H: "\delta \equiv 4 - N." and "U_{\mathrm{barrier}} = \frac{C_{\mathrm{geo}}}{4-N}" and "k ≡ C_geo/E_th is a dimensionless geometric coupling constant" and "[LOCK] Appendix H table is missing."; App L: "| 4 | gtrsim 4 | Solid (e.g., ice): shape preserved, high stiffness | Jammed lattice / space-like regime." and "In the 2D cross-section language used in the main text, enclosing a core point requires at least three vectors (a minimum three-sector closure)."; App B: "(ii) defining the same concept with different values in different files"

**Evidence.** The main text and the VH card put the vacuum at the 3D isostatic point z_iso = 2d = 6, with shear modulus G → 0. Apps H and L instead use rigidity at N = 4, liquid at 3 and forbidden 2, which is the 2D Maxwell count. In App H's law the barrier C/(4−N) diverges at N = 4 and turns negative for N > 4. The 'solid' State 4 (N ≳ 4) of App L therefore lies outside the domain of the rigidity law it is meant to label. L.3's enclosure argument is explicitly two-dimensional. In 3D a positively spanning set needs d+1 = 4 vectors, so State 3 would fail to enclose volume too. L.5's 'stiff lattice' conflicts with G → 0 at the isostatic point. δ ≡ 4−N collides with the canonical δ = 1/π², which is an SSOT violation by App B's own rule. k is never given, the table is missing, and the lock, data and script files are not in the repository, yet the dossier reports G-RIGIDITY-V2-1 as PASS.

**Proposed improvement.** Redo the thresholds with 3D Maxwell counting (z_c = 6 frictionless, or d+1 = 4 frictional, stating which) consistent with §11.6. Rename the gap variable (e.g. Δ_N) and state the law's domain and its behaviour at N ≥ 4. Publish k, the case-study table and the script, or withdraw App H and mark it [O]. Rewrite L.3 for three dimensions.

### 12. [major] App A proves only textbook lemmas (correctly). None of the framework-specific [F] results has a lemma, and the one physics-linked lemma is credited with work it does not do.

- **category:** structure-redundancy
- **location:** docs/physics/axa-mathematical-lemmas-proof-sketches A.1–A.7, Application A.3.1; 08 §8.0.6(A),(B),(D)

**Quote.** A.3.1: "If V=R⁶, W=span1₆, and 1₆=(1,1,1,1,1,1), then dim(W)=1 and dim(V)=6, hence by (AppA_dim_quotient) we have dim(V/W)=5."; §8.0.6(A): "fixes the global phase as a gauge choice and removes no rectification."; §8.0.6(D): "Nucleon (here): N=n sectors ⇒ n-1 independent inter-sector locks, giving the exponent in νₙ=nπ²⁽ⁿ⁻¹⁾." and "Equation (S08_06_gauge_lemma) is a theorem (forced, no free coefficient)"

**Evidence.** I checked the proofs: the Cauchy–Schwarz expansion with λ = ⟨x,y⟩/‖y‖², Parseval via orthogonality, and Robertson via z − z̄ = 2i·Im z are all correct. But all seven lemmas are standard textbook results. None of the framework-specific [F] claims appears: ⟨|cosθ|⟩ = 2/π, ⟨[cosθ]_+⟩ = 1/π, the δ^n product measure, the n-fold law, 82 = 3⁴+1 via the three-square theorem, the §14.0.6 isotropy lemma, Lemma T-S1, or the §18.2 exact-√ uniqueness. A.3.1 is the only lemma tied to the physics, and §8.0.6(D) calls it the 'single forced source' of the nucleon exponent n−1. Yet §8.0.6(A) says gauge removal 'removes no rectification', and in (B) the n−1 actually comes from multiplying by one δ in ν = sδ (s_n·δ = n·δ^−(n−1)). Moreover dim(R^N/span 1) = N−1 holds for every N, so its 'recurrence' cannot be evidence; the load is carried by the choices of N and of the channel cross-section π.

**Proposed improvement.** Restructure App A as 'framework lemmas'. For each [F] derivation give a precise statement, its hypotheses and a proof, marking which hypotheses are definitional (MAP-1/2). Compress the textbook lemmas into a short cited list. Correct §8.0.6(D) to name the true source of the n−1 exponent, and drop the 'structural signature' argument.

### 13. [major] The appendix scripts, lock files and simulation modules are missing from the repository, all 47 'reproduction code' links are dead, and App B's random-number generator specification is ambiguous.

- **category:** reproducibility-code
- **location:** axe E.5, axf F.4, axm M.5, axp P.4, axr R.4, axh H.4, axb B.1, axc C.0; repro/physics/; every physics page header; AGENTS.md §5

**Quote.** App E script: "canon = read_json(\"registry/canon_lock.json\")"; App H: "The following files fully reproduce the numerical table used in this appendix:"; page header: "<a href=\"https://github.com/rego093-sketch/jamming-physics/tree/main/repro/physics/axe-geometric-origin-electron-mass-direct/\" rel=\"noopener\">재현 코드 (GitHub)</a>"; App B: "To eliminate implementation differences across external RNG libraries, we lock the following xorshift128+ as the standard generator." and "s_1\leftarrow s_0,\;\; s_0\leftarrow s_1" and "Split the 32-byte hash digest into the upper 8 bytes and the lower 8 bytes,"; App C: "v4.<major>.<minor>.<patch>/"; AGENTS.md: "deterministic builds, `SEED = 19`"

**Evidence.** `git ls-files` finds no verify_appendix_*.py, no registry/*_lock.json, no run_rigidity_theory_v2_1.py and none of the jamming-spine, SOC or light-mapping modules. repro/physics/tools contains only site and numeric-SSOT tooling. Of the 47 physics pages that link to repro/physics/<slug>/, all 47 targets are missing. B.1's pseudocode, read literally as sequential assignment (s1←s0, then s0←s1), makes the generator emit a constant; I tested this and got 9744039709070652578 on every call. Read as a simultaneous swap it matches the reference xorshift128+ (Vigna 2014). Byte order for uint64(digest[..]) is unspecified. The prose says 'upper/lower 8 bytes' but the formula takes digest[0:8] and [8:16]. The '32-bit' mapping promised in the B.1.2 title is never given. No tool implements this RNG. AGENTS.md's 'SEED = 19' contradicts B.1's SHA-256 seed_id, and App C's v4.x.y release tree contradicts the document versions v0.2–v0.8 (and repro v0.9–v0.11).

**Proposed improvement.** Ship registry/*.json and the verify_appendix_*.py scripts under repro/physics/, or point the links at the exact Zenodo bundle paths, and run them in CI. Rewrite B.1 unambiguously, e.g. `t=s0; s=s1; s0=s; t^=t<<23; …; s1=t; return t+s`, with explicit byte order and published test vectors. Reconcile the seed convention with AGENTS.md and align the version scheme.

### 14. [major] The 80-digit amplification factor A is simply c·Δt/a with the locked Δt = 1.86e-21 s, so §11.3 'derives' its own input. The symbol A also carries at least three different values.

- **category:** circularity
- **location:** docs/physics/axc-archive-schema-file-tree C.3 (realization_lock); 11-realization §11.3.1/§11.3.4 and §11.6 'Measured-value robustness'; 03-axioms §3.4 eq. D=2πλ/A

**Quote.** App C: "\"dt_s\": 1.86e-21,"; §11.3 card: "The tick follows from the amplification; $cΔ t/a=A$ closes exactly."; §11.3: "A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599."; §11.6: "the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%"; ea: "equals 2πλ/A where λ=632.99nm and A 10⁶ is the jamming amplification"

**Evidence.** 299792458 × 1.86e-21 / 6.3299121257859865746e-19 = 880918.977703440000000748733895…, which is exactly the printed A. So A was computed from the 3-significant-figure Δt that App C stores as an input, and §11.3 'derives' Δt = A·a/c back from it; that is why it 'closes exactly'. The same symbol takes at least three values. A_lock = 880,919. The A implied by D = 2πλ/A is 2π·632.991 nm/4.8526 pm = 819,599; with A_lock, 2πλ/A = 4.515 pm (−7%). The simulations give A_med(N=200) = 8.02e5 and A_mean(N=750) = 5.69e5. That is an SSOT violation under App B's rule (ii). On the '0.16%': rescaling to the only other size quoted (N = 200) gives 5.69e5·(750/200)^{1/3} = 884,008, which is +0.35% from A_lock. Moreover, the mean of 104 heavy-tailed events with a p10–p90 spread of 4.4–21e5 (σ_ln ≈ 0.61) has a standard error of about 6.6%. A 0.2–0.35% agreement is well inside that noise and cannot 'pin' A.

**Proposed improvement.** State Δt = 1.86e-21 s as the locked input and A_geo := cΔt/a as a derived quantity quoted to 3 significant figures, and drop §11.3's reverse derivation. Use distinct symbols (A_geo, A_633, A_SOC(N)). Report A_SOC with its standard error and state the rescaling reference explicitly.

### 15. [major] The corpus glossary calls φ = 0.7405 'random close packing' and makes it the vacuum's packing. That is Kepler's crystalline FCC packing, and it contradicts the physics volume's φ_jam = 0.633 at z = 6.

- **category:** cross-volume
- **location:** docs/concepts/index.html (φ ≈ 0.7405 and φ_RCP entries); docs/index.html (chemistry row); AGENTS.md §1; vh vp-card φ_jam; docs/chemistry/02-chemistry-single-anchor CH.13

**Quote.** concepts: "φ ≈ 0.7405 — Jammed substrate (the vacuum) — The single physical claim of the whole framework: the vacuum is a jammed elastic solid at random close packing." and "φ_RCP = 0.7405 — Random-close-packing fraction — Packing fraction of the vacuum substrate (random close packing). [F] forced . canonical §2 ⚠ DISTINCT from φ_jam = 0.840 (2D jamming onset) and φ_iso = 0.633 (isostatic z→6)."; VH card: "φ_jam = 0.633 — Isostatic jamming/packing fraction (z to 6); distinct from 2/π = 0.6366. [V] verified."; chemistry: "crystal density = sphere packing (Kepler) → 0.7405"

**Evidence.** π/(3√2) = 0.74048 is the Kepler maximum for ordered FCC/HCP packing, with coordination z = 12 (hyperstatic) and a finite shear modulus. Random close packing of monodisperse spheres is about 0.64 (Scott & Kilgour 1969; O'Hern et al., PRE 68, 011306 (2003), φ_J ≈ 0.64), and the physics volume's own simulation gives 0.633 at z → 6. The physics mechanism (G → 0 at z_iso = 6, leaving only c² = B/ρ) cannot hold for an FCC packing at 0.7405. The chemistry volume itself labels 0.7405 as Kepler. The symbol φ_jam also means 0.633 in physics and 0.840 in the corpus glossary.

**Proposed improvement.** Change the corpus headline to 'jammed at the isostatic point, φ_J ≈ 0.63–0.64 (physics §11.6: 0.633, z → 6)'. Relabel 0.7405 as 'Kepler FCC/HCP close packing (crystal, not RCP)' and remove it as the vacuum's packing fraction. Use distinct symbols (φ_J^{3D}, φ_J^{2D}, φ_FCC) and regenerate AGENTS.md, the homepage and the concepts page from the manifest.

### 16. [major] The version-history appendix stops at v0.8.0 and still calls v0.6.0 'this version'. Later numeral changes, a grade upgrade from [O] to [F], and an after-the-fact rule choice are not logged there.

- **category:** internal-inconsistency
- **location:** docs/physics/vh-appendix-version-history-reclassification-log (preamble; v0.6.0 heading; v0.6.0 column campaign); 18-time-and-gravity §18.3; repro/physics/CHANGELOG_v0_9.md, CHANGELOG_v0_10_0.md; w0 §W.3.2

**Quote.** VH: "This appendix is the consolidated version record: the body states only the current position, and the version-to-version history lives here."; VH: "v0.6.0 (Handover & Reproducibility Edition; this version)."; CHANGELOG_v0_10_0: "**정확√(운동 시간지연)**: [O] 전부 미유도 → **[F] 값 강제**"; CHANGELOG_v0_9: "§18.2.3 표: 원자 진폭을 1/(2π²)로 재스케일 (H 4854→245.8, C 2623→132.9"; §18.3: "Grade: value [F]; full-vector dynamics [O] (=§14.0.6)."; VH v0.6.0: "absorption-rule analysis_lock exercised (rule B)"; W.3.2: "LOCK exercised 2026-06-11 under operator delegation: rule B (conserving) adopted — rule A yields identically zero force"

**Evidence.** Releases v0.9–v0.11 changed numerals and grades, but the changes appear only in Korean changelogs under repro/, not in the appendix that claims to be the consolidated record. The changes are: the atomic-amplitude table rescaled by 1/(2π²) ≈ 1/19.7; T_b/T_m changed from 1.6 to √2.5; displayed values 292.244 → 292.245 and +57 → +61 ppm; and a grade upgrade from [O] to [F] for the exact time-dilation factor. AGENTS.md anti-pattern 5 requires an upgrade from [O] to rest on a passing falsification test. G-EXACT-SQRT is a numerical uniqueness check of a derivation, not a test against external data. Separately, the absorption-rule lock was 'exercised' after the decision table showing each rule's outcome had been computed, which is model selection with the outcome known. The VH records it as a routine discipline event.

**Proposed improvement.** Add v0.9, v0.10 and v0.11 entries to the VH with a before/after row for every numeral and grade change, and remove 'this version' from v0.6.0. Record the [O]→[F] upgrade together with the test that justifies it, or keep the value at [H] until an external discriminating test exists. Tag the rule-B adoption 'post-hoc selection (outcomes known)'. Generate the VH from the changelogs so the two cannot drift apart.

### 17. [minor] The App D glossary contradicts the main text: α is described wrongly, r_e is mislabelled, the status of D_anch is inconsistent, and key symbols are missing.

- **category:** internal-inconsistency
- **location:** docs/physics/axd-glossary-index D.0, D.1 and vp-cards; vp_locks.csv alpha row; 05 §5.1; axe E.1; docs/concepts λ_anchor entry; 03 §3.4

**Quote.** "α = 2/π — Geometric rectification ratio (full-wave to half-wave mean); the single rectification anchor. [F] forced."; "rₑ Electron radius (canonical definition)."; "Dₐnch Anchor length (canonical input)."; "a Realized length (volume-particle diameter)."; concepts: "⚠ Distinct from D (quantum size, 4.852620 pm) and from the canonical Anchor-Cell length D_anch"; §5.1 card: "α=⟨|cos|⟩=2/π — The full-cycle magnitude average"

**Evidence.** The full-wave rectified mean is 2/π and the half-wave mean is 1/π, so their ratio is 2, not 2/π. §5.1 correctly defines α = ⟨|cosθ|⟩. D.1 calls r_e 'the electron radius', but App E restricts it to an event-rate radius, r_e = D/(2π²) = 245.8 fm, which also collides with the standard classical electron radius (2.818 fm). The concepts page says D and D_anch are distinct, while §3.4 defines D_anch := 2λ_C,e = D. Two different 'diameters', a = 6.33e-19 m and D = 4.85 pm (a ratio of 7.7e6), have no entry explaining the difference. A, N, λ_ref, ν_n, κ_H, φ_jam, Ψ_yield, τ_q, g*, S and S_p are all absent from the 'symbol index'.

**Proposed improvement.** Generate App D from the same SSOT as the vp-cards. Reword α as 'full-cycle rectified mean ⟨|cosθ|⟩ = 2/π (half-wave mean 1/π)'. Rename r_e to r_ν,e (event-rate radius) with a warning about the classical radius. Make the D/D_anch statements agree, and add the missing symbols with their grade and section.

### 18. [minor] Rendering and notation defects: a printed inner-product axiom is false, LaTeX commands leak into the pages, a table is missing, auto-generated summaries are garbled, and mass is written where energy is meant.

- **category:** presentation-rendering
- **location:** axa A.0(2), A.3, A.4, page lede; axb B.2; axc C.1–C.6 headings, lede; axr R.0–R.4; axk K.3/K.4; axl L.1 and Part II intro; vh body; axh H.4; axe E.3 / axm M.0 / axp P.3

**Quote.** "(Conjugate symmetry) ⟨ x,y⟩ = ⟨ y,x⟩."; "The norm is defined by |x|:=√(⟨ x,x⟩)."; "Z_N=0,1,…,N-1"; "## C.1 registryₛnapshot schema (SSOT sealing)"; "noindent[SUPERSEDED — record only (App.R banner); not a Coulomb-scale derivation; current canon: S14.0/S14.5]"; "Kn_λll 1"; "| 4 | gtrsim 4 |"; "[F]{}"; "textbackslash WPVersion"; "The following tree is locked as the minimal immutable structure. 2/pi."; "[LOCK] Appendix H table is missing."; "The academic body (Part I, §W through Appendix K)"; App E: "m_e:=\frac{U_{\mathrm{lat}}}{S}" vs "m_e c^{2}=\frac{h\,c}{\lambda_{C,e}}"

**Evidence.** The complex conjugate bar was lost in conversion. As printed, conjugate symmetry together with linearity in the first slot gives ⟨ix,ix⟩ = i²⟨x,x⟩ = −‖x‖², which contradicts positivity, so the printed axioms are inconsistent for complex spaces. Norm double bars and set braces are also lost. Heading underscores turn into subscript glyphs, and the commands \noindent (8 times), \ll, \gtrsim and \textbackslash appear raw. The auto-generated ledes end in stray tokens ('2/pi.', '4π.', '3π⁴.'). App L hosts the Part II introduction, which says Part I ends at App K although App L–R follow it. U_lat/S is an energy, so writing m_e := U_lat/S and then m_e c² = hc/λ is dimensionally inconsistent unless c = 1.

**Proposed improvement.** Fix the LaTeX-to-HTML converter for \overline, \|, \{\}, \ll, \gtrsim, \noindent and underscores in headings, and add a render-lint gate that fails on raw backslash commands or '{}' fragments. Regenerate the ledes from curated sentences. Restore the App H table or delete the placeholder. Write m c² := U_lat/σ_eff (energy) throughout Apps E, M and P.

**Strengths noted:**
- App E corrects its old π² error in place and says so in a banner (the earlier route gave ≈5.04 MeV) instead of hiding it; §13.5.4 openly calls m_e = 2hc/D a calibration, 'an anchor, not a prediction'.
- App R is honestly marked SUPERSEDED and its stated factor is right: F_VP/F_Coulomb = √2/(π⁴·α_em) = 1.9895, which does not depend on r_p. Equivalently, the route would have implied α_em ≈ √2/π⁴ ≈ 1/68.9, off by a factor of 2.
- The App A proofs I checked are correct: Cauchy–Schwarz with correct handling of complex conjugates, Parseval via DFT orthogonality, and Robertson via z − z̄ = 2i·Im z.
- App K's worked numbers are correct: T = 292.8 K, collision diameter d = 3.69 Å and mean free path = 66 nm all reproduce. K.5 states its claim level modestly.
- Apps F, K and L are labelled NON-LOCK and kept out of the PASS/FAIL set, and F.3 lists concretely what would be needed to promote App F.
- §13.3 publishes the −0.40% Higgs residual rather than moving to 4.98π, and §14.5 openly demotes the α_em closed form as a coincidence with many rivals.
- The VH v0.6.0 forensic entries admit that the historical 9.8 m/s² was a targeted closure with two simulation-fitted O(1) factors, and treat operator testimony as non-evidence.
- App B's governance design is sound in principle: pre-registered FAIL codes, INCONCLUSIVE not usable as evidence, deterministic seeded sampling and Kahan summation.
- The r_p prediction D/(6π⁶) = 0.84125 fm is a genuine, falsifiable number currently +0.78σ from CODATA 2022; together with the pre-registered light angles χ(633) and χ(532) it is the strongest candidate for a flagship pre-registered test.


## lens:numerics

### 1. [critical] The 'derivation' of the time tick is circular: the locked 80-digit A is exactly c·(1.86e-21 s)/a, so Δt = A·a/c_ref gives back its own input, and the '0.16%' A_geo match cannot be reproduced

- **category:** circularity
- **location:** physics §11.3 (11-realization-units-t-rcross, 'Deriving Δt=(A·a)/c_ref'), §11.6.5 'Measured-value robustness', §3.4, SP S3(iii), W.0 reproducibility map, §1.9 A1/A3; repro/physics/tools/vp_numeric_ssot.py

**Quote.** §11.3: "## 11.3 Deriving Δ t=(A· a)/c_ref→1.86× 10⁻²¹s" … "The tick follows from the amplification; $cΔ t/a=A$ closes exactly." … "A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599."  §11.6.5: "more sharply, the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%."  W.0: "A=880918.977… | [V]/[H] | verify_amplification_A.py; … | measured from the lattice (a_med/g^*), not a free fit".  §1.9 A1: "The non-trivial content is that c_env comes out equal to c_ref; the framework does not assume this, it shows it (§11.6)."  vp_numeric_ssot.py: ("A_geo","cΔt/a",f(q['A_geo'],4),"[H] Δt 3 s.f. ⚠placeholder")

**Evidence.** Decimal arithmetic (90 digits): c·(1.86e-21)/a with a = 6.3299121257859865746e-19 m gives 880918.977703440000000748733895383659091520244925650031008026876905438425800635992…, which is the locked A digit for digit. The run of zeros '…3440000000074873…' is the signature of dividing a round 1.86e-21 s. So Δt = 1.86e-21 s came first, A was computed from it, and §11.3 then 'derives' Δt from A. A·a/c returns 1.8599999…e-21 s. It follows that A_geo := cΔt/a ≡ A, by definition. The repo's own SSOT tool labels it a '⚠placeholder', but the text presents it as a derivation and as 'measured from the lattice'. The simulation values do not match it: A_med(N=200) = 8.02e5 is −8.96% from 880919. The stated N^(-1/3) rescaling gives A_geo·(750/200)^(-1/3) = 567,012. Against A_mean(750) = 5.69e5 that is +0.35%, and against A_med(750) = 4.76e5 it is −16.05%. Neither is 0.16%. The −16.05% (a fraction of 0.1605) suggests a percent/fraction slip. The statistic also swaps from median (N=200) to mean (N=750), and the stated p10–p90 spread is 4.4e5–2.1e6, a factor of about 5, so no 0.16% agreement is meaningful at that sample size (104 events). The same identity makes 'c_env = c_ref' true by construction: lattice speed maps to m/s only through a/Δt, and Δt was defined as A·a/c_ref. §1.9 A3 lists 'A_geo (0.16%)' as one of the five surviving coincidences.

**Proposed improvement.** Rewrite §11.3 to say plainly that Δt = 1.86e-21 s is a declared realization input [INPUT] and A := cΔt/a is derived from it, or else lock A from a specific named simulation output (seed, N, estimator) and carry its real statistical uncertainty (bootstrap CI, likely ±20–50%). Delete the '0.16%' claim, or publish verify_A_scaling.py with the exact scaling reference N and estimator that produce it. Remove A_geo from the §1.9 A3 coincidence count. Downgrade A1 'Resolved [F]' to 'c_env = c_ref holds by the unit map (definitional)'. The only non-trivial content is isotropy and linear dispersion in lattice units, which should be graded separately.

### 2. [critical] Rates and the electron period are tied to the SI second: ν_p = 3π⁴ s⁻¹, ν_e = 1 s⁻¹, T_e ≈ 1 s. A dimensionless ratio is given units, and T_e scales as N²

- **category:** unit-dimension
- **location:** §7.2.1 (07-3-sector…), §9.3–9.4 (09-event-quantum…), §8.0.5, §12 (12-electron-1-second…), §14.0 (14-force…), §1.9 A2/A3, W.0 scorecard

**Quote.** §7.2.1: "the unit of ν_p,can is locked as [s⁻¹]."  §9.4: "$\nu_{p,\mathrm{can}}=\frac{r_e}{r_p}$" and "Here “Hz=s⁻¹” reads the canonical second as equivalent to the SI second".  §14.0: "νₚ=3π⁴≈292s⁻¹ and νₑ=1s⁻¹ (§12)".  §12: "bounding-cube cells, (D/a)³ | 1.0056 s | +0.56%" … "Only the bounding-cube measure lands on the clock" … "small-lattice direct count, Tₑ∝ N² scaling invariance, and the 5-of-6 three-fold channel ratio".  W.0: "N=10¹² | [H] | (declared split integer) | a chosen split; no dimensionless output depends on it (§1.8.2 N-invariance)"

**Evidence.** (1) §9.4 writes ν_p,can = r_e/r_p, a ratio of two lengths, so it is dimensionless. §7.2.1 locks the same quantity in s⁻¹. Both cannot hold. (2) If ν_p really carries s⁻¹, then m_p/m_e = 2πν_p = 6π⁵ is dimensionless only in SI seconds. In ms it would read 1.836. (3) T_e = (6/5)(D/a)³Δt. Here D/a = 2λ_C,e·N/λ_ref = 7.666e6 and (D/a)³ = 4.505e20, giving T_e = 1.0056 s. But (D/a)³ ∝ N³ and Δt = A·a/c ∝ 1/N, so T_e ∝ N². Holding everything else fixed, N = 10⁹ gives T_e = 1.006e-6 s, N = 2⁴⁰ gives 1.216 s, and N = 10¹⁵ gives 1.006e6 s. So 'T_e ≈ 1 s' is a property of the declared N = 10¹² and the declared Δt = 1.86e-21 s (see the A/Δt finding). It is not a physical output. The dimensionless ratio T_e/τ_q (τ_q = D/c) also depends on N², which contradicts 'no dimensionless output depends on it'. (4) The measure was chosen after seeing the candidates: cube 1.0056 s, sphere 0.527 s, jam-weighted sphere 0.333 s. (5) The SI second is a human convention (9,192,631,770 Cs-133 periods, historically 1/86400 day). No lattice mechanism can make an electron period land on it unless the unit is put in by hand. Yet 'T_e ≈ 1 s (+0.6%)' is counted in the §1.9 A3 five-item coincidence count.

**Proposed improvement.** Make ν_n = nπ^{2(n−1)} explicitly dimensionless, a count per canonical electron event with ν_e ≡ 1 by definition, and delete every 's⁻¹'/'Hz' attached to 3π⁴ and ν_e. Remove 'T_e ≈ 1 s' from the evidence set (§1.9 A2/A3, W.0 scorecard). If kept, restate it as the dimensionless T_e/τ_q = (6/5)(D/a)³(Δt/τ_q), show its N² dependence, and grade it [INPUT]/definitional. Also correct the W.0 row 'no dimensionless output depends on N'.

### 3. [critical] The Higgs 'prediction' scales linearly with the decimal split N and the He–Ne wavelength; the N-invariance table hides this, two sections contradict each other, and the miss is −4.6σ

- **category:** numerology-look-elsewhere
- **location:** §1.8.1–1.8.2 (01-governance…), §1.9 A5, §W.5.4 (w5-anti-circular…), §13.3 (13-mass…), W.0/W.2.1 scorecard

**Quote.** §1.8.2: "| m_H/U_lat | 1/(5π) | 1/(5π) | 1/(5π)" … "Confirmed by the released code; no N enters the closure equations."  §1.9 A5: "The choice is operational, not theoretical: any other anchor in the window predicts the same dimensionless ratios."  §W.5.4: "it is a non-trivial coincidence between the measured wavelength of a helium–neon laser and the measured Higgs mass" … "changing λ_ref by 5% moves m_H by 5% to a value the measurement excludes."  §13.3: "m_H^exp=125.20± 0.11GeV"

**Evidence.** m_H = U_lat/(5π) = hc·N/(5π·λ_ref) = 1958.7033 GeV/(5π) = 124.6949 GeV, and the arithmetic is correct. The N-invariance table lists m_H/U_lat, which is the coefficient 1/(5π) and trivially N-free. It does not list m_H or the dimensionless ratio m_H/m_p = N·λ_C,p/(5π·λ_ref). That ratio is 0.1329 at N = 10⁹, 132.9 at 10¹², 1.33e5 at 10¹⁵, and 146.1 at N = 2⁴⁰; measured is 133.44. So the one anchor-dependent headline depends on a base-10 choice of N as much as on λ_ref. A5 says any anchor gives the same predictions, while W.5.4 says a 5% change in λ_ref is excluded by data. They contradict each other. The residual −0.505 GeV equals −4.6σ against PDG 125.20 ± 0.11. A look-elsewhere Monte Carlo (seed 19, log-uniform target coefficient in [3,100]) gives the chance that some p·π^k (p ≤ 10, k ≤ 3) lands within 0.40% at about 7.0%, and for p/q·π^k (q ≤ 3) about 14.6%. That is per choice of laser line, with N free to cover every decade. A second standard line (e.g. 532, 1064 nm) roughly doubles it. This is not evidence at the level implied by 'non-trivial coincidence'.

**Proposed improvement.** Replace the §1.8.2 table with m_H/m_e, m_H/m_p and T_e/τ_q evaluated at N = 10⁹, 10¹², 10¹⁵, and 2⁴⁰, stating plainly that m_H ∝ N/λ_ref. List N as a second declared input. Reconcile A5 with W.5.4: either m_H is anchor-dependent (then drop A5's claim) or it isn't. Report the Higgs residual as −4.6σ, not only −0.40%. Add a pre-declared look-elsewhere estimate over (anchor line) × (N) × (coefficient grammar). Until a physical reason fixes N and the neon transition, grade m_H [O]/coincidence, matching the α_em treatment.

### 4. [major] The 'exactly one DOF' claim is false: m_e (λ_C,e) is a second measured anchor, several further inputs are declared 'chosen', and measured anchors are graded [F] forced

- **category:** grading-honesty
- **location:** §1.8.1 DOF ledger, §W.5.1, §3.4, W.0 scorecard boxes (λ_anchor, D), W.2.1 SSOT table, W.6 provenance ledger

**Quote.** §1.8.1: "Single empirical anchor (1 DOF): λ_ref=632.99nm, used to fix a once." … "The total tunable DOF count is therefore exactly one, and it is exposed in step 3."  §3.4: "D_anch:=2λ_(C,e)=4.8526pm — the same 632.99 nm / mₑ anchor used everywhere else".  W.0: "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." and "D = 4.8526 pm — Quantum (anchor) diameter that fixes the lattice length scale. [F] forced."  W.2.1: "| g₀ | 2×10⁻⁷ | analysis_lock | §10.3 | microscopic gap threshold | chosen".  W.6: "re-running the released code at g₀=10⁻⁶,2×10⁻⁷,4×10⁻⁸, which gives D≈ 26,5.2,1.0 pm"

**Evidence.** D = 2λ_C,e = 2h/(m_e c) = 4.852620 pm uses the CODATA electron mass. W.2.1 itself lists 'mₑ | CODATA | canon_lock | mass-scale anchor'. D/a = 7.666e6 is not claimed as a derived integer or closed form, so λ_ref and m_e are independent empirical scales. That makes at least 2 DOF. r_p, m_p, m_e, τ_q and χ all ride on m_e, not on λ_ref. Other declared or chosen inputs that move outputs: N = 10¹² (m_H ∝ N, T_e ∝ N²), Δt = 1.86e-21 s (A is computed from it), g₀ = 2e-7 (A ∝ 1/g₀; D varies 26 → 1.0 pm over the stated g₀ range), the κ_vp cell-measure choice (T_e changes by a factor of 3), Ψ_yield per body, and α_em. Grading a measured wavelength and a CODATA-derived length as '[F] forced' conflicts with the legend ('[F] = derived from fixed geometry'). The repo's NUMERIC_LEDGER grades D as [H]. The same quantity carries [F] and [H] in different places.

**Proposed improvement.** Rewrite §1.8.1 as a complete input ledger: λ_ref [INPUT], m_e or λ_C,e [INPUT], N [DECLARED], Δt [DECLARED], g₀ [DECLARED], cell-measure choice [DECLARED], Ψ_yield per body [INPUT], α_em [INPUT], and state which outputs depend on each. Re-grade the W.0 boxes: λ_anchor → [INPUT]/anchor, D → [H]/anchor-derived. Keep the claim that dimensionless π-forms (6π⁵, 2/π) use neither anchor. That claim is true and is the defensible core.

### 5. [major] The proton-radius chain rests on a back-computed λ_C and a rounding artifact, and is scored against an outdated CODATA value

- **category:** math-error
- **location:** §6.3.3–6.3.4 (06-continuum-core…), §8.0.5 (IV), §9.4 SSOT note, §13.4/§13.5, §2 r_p status, W.0/W.2.1, VH log, §1.8.3 five-line check, §1.9 A3; reports/NUMERIC_LEDGER.md

**Quote.** §6.3.3: "In this section, assume that the following value is locked by canon_lock:" "$\begin{equation} \lambda_C = 1.3213538700998668\ \mathrm{fm}. \end{equation}$" and "### 6.3.4 Back-calculation (consistency): reconstructing λ_C from Rₚ=0.8412fm".  §8.0.5: "the former canonical-input value 0.8412fm is kept only as a +61ppm cross-check (within the proton-radius measurement spread)".  VH: "the forced (2/π)λ_(C,p)=0.8412 fm is now its +61 ppm cross-check (equivalently +19 ppm vs. the mₚ/mₑ=6π⁵ residual)".  W.2.1: "the length-route νₚ=D_anch/(2rₚ)δ=292.245 agrees with 3π⁴ to +61 ppm".  §1.9 A3: "rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm)"

**Evidence.** (π/2)×0.8412 = 1.3213538700998668 exactly, so the 'locked' λ_C is back-computed from the rounded radius. It is not the proton Compton wavelength (CODATA 1.32140985539 fm) and is off by −42.4 ppm. §6.3.3 then 'derives' R_p = 0.8412 fm from it, and §6.3.4's 'consistency check' is a tautology. With the true λ_C,p, (2/π)λ_C,p = 0.8412356 fm = 4ħ/(m_p c). D/(6π⁶) = 0.8412515 fm is +18.8 ppm from that, which is just the 6π⁵ residual, since D/(6π⁶) ≡ (2/π)λ_C,p·(μ_meas/6π⁵). The quoted '+61 ppm' = (0.8412515/0.8412000 − 1) is 42 ppm of rounding plus 19 ppm of 6π⁵ residual, so it is an artifact. The ledger nonetheless calls it 'independent residual #2'. The '[V]' length route ν = (D/2r_p)δ with unrounded r_p equals μ_meas/(2π) = 292.2303. It is the measured mass ratio restated; the value 292.245 only comes from rounding. Against the external value: CODATA 2018 0.8414(19) fm gives −177 ppm (−0.08σ), but CODATA 2022 r_p = 0.84075(64) fm gives +596 ppm (+0.78σ). The text uses 2018 for r_p while citing CODATA 2022 for α and PDG 2024 for m_H. Prior art and look-elsewhere: r_p ≈ 4ħ/(m_p c) is a previously published numerical relation, which should be checked and cited. The chance that r_p/ƛ_p falls within 1σ (0.076%) of an integer ≤ 10 is about 0.6%, and of a p/q with q ≤ 4 about 2.5% (Monte Carlo).

**Proposed improvement.** Delete the 0.8412 'locked' value, the back-computed λ_C, §6.3.4, and all '+61 ppm' / '292.245 [V]' statements. State one relation: r_p = (2/π)λ_C,p = 4ħ/(m_p c) = 0.841236 fm. Note that D/(6π⁶) differs from it only by the 6π⁵ residual, so it is not an independent prediction. Quote the residual against CODATA 2022 (+0.76σ for 4ħ/m_p c) with σ, pin every reference to one CODATA/PDG vintage, and cite the prior appearance of r_p ≈ 4ħ/m_p c with a look-elsewhere estimate.

### 6. [major] The 'committed' light angles come from rounding the wavelength input, so kill criterion 3 is not a sharp test

- **category:** missing-test-or-prediction
- **location:** §10.9 / §10.9.1 (10-implementing-speed-light…), §1.10 Kill criterion 3, §3.4 'Honest precision of D', W.0 reproducibility map, SP S3(ii)

**Quote.** §10.9.1: "Using the full-precision anchor λ_ref=632.99121257859865746 nm instead shifts λ/D to 130443.1730, crossing the integer ceiling to m=130444 and χ=89.7960^(∘)".  §1.10: "(χ(633)=89.9378^(∘), χ(532)=89.8248^(∘), with the D-distribution spread as the stated width)".  §3.4: "D = 4.853\ \mathrm{pm}\quad(\text{4 significant figures; the 4th digit uncertain at }\sim 0.04\%)".  §10.9.1: "the ratio (λ/D)₆₃₃/(λ/D)₅₃₂=1.189831=633/532 cancels D and any mass scale — the relative mapping is anchor-free and falsifiable."

**Evidence.** sin χ = x/⌈x⌉ with x = λ/D. Recomputed with D = 4.852620477 pm: 632.99 nm → x = 130442.923, χ = 89.9378°. Full anchor 632.99121258 nm → χ = 89.7960°. HeNe air wavelength 632.816 nm → 89.7832°. 532.0 nm → 89.8248°. The actual I₂-stabilised doubled Nd:YAG line, 532.245036 nm, gives x = 109681.98 and χ = 89.9680°. Because 1 − x/m = (1 − frac(x))/m, χ can be anything in (90° − √(2/m), 90°) = (89.776°, 90°) for 633 nm, depending only on the fractional part of λ/D. A 7.7 ppm change in D moves frac(x) by a full cycle. The document's own stated D precision (0.04% = 400 ppm) spans about ±52 integer steps. So even its own model does not predict χ within that window. The 'committed' numbers depend on rounding 632.99121 → 632.99 and on the nominal 532.0. The two-wavelength ratio 1.189831 = 632.99/532.0 is an input ratio divided by itself, so it cannot fail.

**Proposed improvement.** Withdraw 89.9378°/89.8248° as the B1 commitment. Either (a) commit only to the one prediction the formula actually makes robustly: χ lies in (90° − √(2/m), 90°), with a uniform-in-frac(x) distribution unless D is pinned below 1 ppm. Or (b) declare D ≡ 2λ_C,e exactly (known to 3e-10), use the vacuum I₂-stabilised wavelengths (632.99121258 nm, 532.24503610 nm), and commit to χ = 89.7960° and 89.9680° with a propagated uncertainty. Remove the RCROSS ratio test from the list of falsifiable checks. Keep G-ISO open.

### 7. [major] Exact forms graded [F] miss by about 10⁶σ (6π⁵) and 4.6σ (5π), but residuals are ruled out as falsifiers, and the look-elsewhere logic that demoted α_em is not applied to them

- **category:** numerology-look-elsewhere
- **location:** §1.8.4, §1.9 A3, §1.10 'What we do not call falsifiers', §8.0.5 (IV), §13.3/§13.5, §14.5 status note and §14.5.4, W.0 scorecard

**Quote.** §1.10: "(i) "the closure has a 0.4% residual" — the residual is reported openly and is part of the deliverable".  §1.9 A3: "The joint probability of the surviving five under a six-line geometric chain with one anchor is the structural claim. This is not proof; it is a coincidence count."  §14.5: "Many distinct closed forms built from small integers and π land on 137.036 to comparable accuracy (e.g. 4π³+π²+π=137.036…), so matching the number does not single out this assembly." and "The 4π is unit-dependent, not physical here."

**Evidence.** 6π⁵ = 1836.118109 against μ = 1836.152673426(32) (CODATA 2022, relative σ 1.7e-11): −18.8 ppm ≈ −1.1×10⁶σ. 5π: −0.40% = −4.6σ against PDG. A result called 'forced' has no free parameters, so unless a theoretical uncertainty or correction series is stated, both results are formally excluded. §1.10 then says residuals are not falsifiers, which makes the [F] results unfalsifiable. Look-elsewhere (Monte Carlo, seed 19, log-uniform targets in [10², 10⁴]): the chance of hitting within 18.8 ppm with p·π^k (p ≤ 12, k ≤ 8) is 4.1e-4, and with p/q·π^k (p, q ≤ 12) it is 2.9e-3. So 6π⁵ (Lenz 1951, cited in §0) is a genuinely unlikely coincidence, but not beyond chance for a moderate grammar. 5π at 0.4% has p ≈ 7–15% (see the m_H finding). The §14.5 reason (i) that demotes α_em (4π(11 − …) at +3.03 ppm; 4π³+π²+π at +2.2 ppm) is the same look-elsewhere argument, and it applies equally to 6π⁵ and 5π. §14.5 reasons (ii) and (iii) are physically wrong. α⁻¹ = 137.036 in every unit system, so a 4π inside a formula for a pure number is not a unit artifact. And if 'running' disqualified α, it would disqualify m_H as well, whose pole and MS-bar values also differ at the percent level.

**Proposed improvement.** For each [F] closed form, state a theoretical-uncertainty model before comparing: e.g. 'leading order; the first correction is O(x) with x = …'. Then report the residual in units of that uncertainty. Pre-register a formula grammar and publish the look-elsewhere p-value for 6π⁵, 5π, 4ħ/m_p c and the α form under one common rule. Replace §1.10 (i) with an explicit tolerance whose violation is a falsifier. Rewrite §14.5 to rest on reason (i) only, and either apply the same rule consistently (re-grade 5π to [O]/coincidence) or justify, with numbers, why 6π⁵ passes and α does not. Recount §1.9 A3 after removing T_e and A_geo (see those findings): three items remain, each with its own p-value.

### 8. [major] The 0.04% three-route agreement on D reflects picking the best of about 83 avalanches plus a rounded-r_p route, and the stated 0.04% precision floor conflicts with residuals quoted at 19–61 ppm

- **category:** numerology-look-elsewhere
- **location:** §3.4 'multipath anchor identity' and 'Honest precision of D', §11.6.5, W.0 reproducibility map (ℓ_rot row), W.2.1 cross-checks, SP S3 counterexamples

**Quote.** §3.4: "the jamming simulation independently reproduces the length to 0.04% (4.8542pm — a selected length with a 7% distribution, scale-anchored to A_geo=cΔ t/a at 0.16%; §11.6)" and "The anchor and its corroborating routes span 4.8523–4.8542pm, so D is pinned to only 0.04%".  §11.6.5: "the 633-channel circulation length has median 4.96 pm with a best-matched avalanche at 4.8542 pm (target 4.85)."  W.0: "ℓ_rot=4.8542 pm | [V] | … | a selected best-avalanche from a 7% distribution (median 4.96 pm)"

**Evidence.** The three routes: 2λ_C,e = 4.852620 pm (CODATA, known to 3e-10). 6π⁶ × 0.8412 = 4.8523 pm, which uses the rounded r_p, itself (2/π)λ_C,p, i.e. λ_C,e again, so it is not independent. And 4.8542 pm is the best of about 83–104 avalanches whose median is 4.96 pm (+2.2%). Taking a Gaussian centred at 4.96 pm with 3.5–7% width, the chance that at least one of 83–104 draws falls within ±0.04% of 4.8526 pm is 30–54%. The 'corroboration' is therefore expected by chance. The honest jamming estimate is the median, 4.96 pm (+2.2%), with a ~7% spread. Declaring a 0.04% (400 ppm) 'precision floor' on D and propagating it to r_p is also inconsistent with quoting r_p residuals of +19 and +61 ppm, and with the ppm-level χ table.

**Proposed improvement.** Report the jamming route as its median ± a dispersion or bootstrap interval (e.g. 4.96 pm, p10–p90), with the target at its percentile, and drop 'best-matched avalanche' from every corroboration claim. Remove the 6π⁶·r_p route from the D triangulation, since it is λ_C,e again. State D ≡ 2λ_C,e as an exact definition carrying CODATA precision. Delete the '0.04% floor' language, or apply it consistently to every D-derived residual.

### 9. [major] The gravity cap's 'height-independence' and 'surface-condition' readings contradict standard gravimetry, which already meets kill criterion 4; they also contradict §18.8

- **category:** physics-validity
- **location:** §17.4.6 (17-extensions-optional-reading), Appendix G (axg-…) G.0–G.1, §14.1.5.3 regime table, §1.10 Kill criterion 4, W.0 scorecard; vs §18.8 (18-time-and-gravity)

**Quote.** §17.4.6: "Why the surface gravity is independent of altitude column-height above each body — Beverloo-type height-independence." and "different effective Ψ_yield at different surface conditions (granite vs sediment, dry vs water-saturated, sea level vs mountaintop)".  App. G: "at Earth's surface Ψ_(rm geom)≈Ψ_(rm yield)^((⊕)), so the representative value observed at the surface g≈ 9.8rm m/s² is interpreted not as “a value that grows without bound as mass increases,” but as a value near the lattice yield limit." and "$0 \le g_{\rm restore} \le g_\star.$" and "back-substitution from the measured surface gravity of Earth at the standard reference (CODATA g₀=9.80665ms⁻²)".  §1.10: "A controlled experiment that exhibits clean 1/R² dependence without a saturation onset, at scales where the cap should be active, would falsify the gravity portion of the framework."

**Evidence.** The quantities that surface (contact-mode) spring gravimeters read follow Newton at Earth's surface. The measured free-air gradient, 0.3086 mGal/m, matches 2g/R = 2×9.80665/6.371e6 = 3.079e-6 s⁻² = 0.3079 mGal/m, which is the clean 1/R² dependence that kill criterion 4 names, measured exactly where App. G says the cap is active. On Everest the free-air drop is ≈0.0273 m/s² (0.28%), so 'sea level vs mountaintop' is already explained by 1/R² with no Ψ change. Normal gravity at the poles is 9.83218 m/s², +0.26% above the 'cap' g* = 9.80665. The equator is 9.78033 (−0.27%). So g_restore ≤ g* is violated at the poles unless Ψ is refitted place by place. Absolute (free-fall, 'geom' channel) and relative (contact, 'restore' channel) gravimeters agree at the µGal level (~1e-9 g), which leaves no room for two distinct channels at the surface. Finally, 9.80665 m/s² is the conventional standard gravity adopted by the CGPM in 1901, an exact defined number, not a measured value. §18.8 separately concludes that the gravity sector is 'observationally degenerate with GR', which is incompatible with height-independent surface gravity. (Arithmetic check: Ψ_yield = 9.80665/c² = 1.0911e-16 m⁻¹ matches the quoted value.)

**Proposed improvement.** Remove 'height-independence' and 'terrain-dependent Ψ_yield' from the [F] 'universal' list in §17.4.6 and from the §14.1.5.3 regime table. Either state explicitly that the cap is inactive at planetary surfaces (consistent with §18.8), or record that kill criterion 4 is met by gravimetry (free-air gradient; absolute-vs-relative gravimeter agreement) and mark the cap FAIL. Replace 'measured surface gravity … CODATA g₀' with 'conventional standard gravity g_n (exact by definition)'.

### 10. [minor] The four-digit F_bridge = mc²/D 'verification' is an algebraic identity, yet it is graded [F] and counted as a no-tuning fingerprint

- **category:** circularity
- **location:** §14.1.5.2 (14-force-lattice-tension…), W.2 'Easy-to-miss derived results', EA log v36

**Quote.** §14.1.5.2: "the framework's particle-card output matches F_bridge to four significant digits across every entry. This is not a new independent derivation; it is the closure of the mass–rate–force chain" … "[F] for the F_bridge=mc²/D identity verified across the particle list".  EA v36: "Internal consistency check F=mc²/D to four significant digits across all particles. This became the no-tuning fingerprint (Part I §14.1.5.2)."

**Evidence.** The card force is built as ν_ann × 2π → m → × c²/D, so it equals mc²/D by construction. An identity cannot distinguish tuned from untuned inputs. Agreement to only four digits, rather than machine precision, just shows the card stores rounded intermediates. Presenting this as a fingerprint of no-tuning and grading it [F]/'verified' inflates the evidence count.

**Proposed improvement.** Relabel as an internal bookkeeping identity (a unit test), not evidence. Fix the rounding so it closes to machine precision. Remove it from W.2's 'derived results' and from the no-tuning fingerprint.

### 11. [minor] Load-bearing simulation scripts are not in the repository, the irreproducibility ledger omits them, and the drift gate enforces a non-CODATA Coulomb constant

- **category:** reproducibility-code
- **location:** repro/physics/IRREPRODUCIBILITY_LEDGER.md; repro/physics/tools/vp_numeric_ssot.py (CANON, MEAS, BAD_PATTERNS); §14.2.1 (k_e); W.6/§11.6.5 script maps

**Quote.** IRREPRODUCIBILITY_LEDGER.md lists only "## 1. 절대 중력 크기" and "## 2. 전자기 미세구조 상수".  vp_numeric_ssot.py: MEAS = dict(MPME=D("1836.15267343"), RP_CODATA=D("0.8414"), MH_PDG=D("125.20")) and (r"8\.9875517923", "8.9875517923e9","8.9875517874e9","c²·1e-7 = 8987551787.37").  §14.2.1: "$k_{e}=8.9875517874\times 10^{9}\ \mathrm{N\cdot m^{2}/C^{2}}$"

**Evidence.** None of the scripts cited as load-bearing (lattice_3d_jam_percolation.py, soc_percolation_pinning.py, verify_amplification_A.py, verify_A_scaling.py, electron_one_second.py, light_emergence_massfree.py, final_verification.py, proton_radius_model.py, rcross_validate.py) exist anywhere in /home/user/jamming-physics; they live only in an external Zenodo zip. The repo's tools recompute closed forms only, so A, D (4.8542 pm), T_e, c² = B/ρ, and the 0.16% claim cannot be re-run from the repo. The ledger nevertheless lists only two irreproducible items. The drift gate also marks as 'bad' 8.9875517923e9, which is the CODATA 2018 value 1/(4πε₀) with ε₀ = 8.8541878128e-12. It enforces c²×1e-7 = 8.9875517874e9, the pre-2019 exact value. CODATA 2022 gives 8.9875517862e9. Reference vintages are mixed: m_e and r_p from 2018, α from 2022, m_H from PDG 2024.

**Proposed improvement.** Vendor the load-bearing scripts, with seeds and summary JSONs, into repro/physics, or add each missing item (A, D selection, T_e, c² = B/ρ, A_geo 0.16%, χ) to the irreproducibility ledger with its obstacle. Pin one reference set (CODATA 2022 + PDG 2024) in a single constants file. Fix the drift gate to accept the CODATA k_e, or better, drop k_e entirely, since §14.2 is superseded.

### 12. [minor] Homepage and AGENTS.md call 0.7405 'random close packing', but it is the FCC/HCP (Kepler) density; the physics volume itself uses φ_jam ≈ 0.633–0.64

- **category:** cross-volume
- **location:** AGENTS.md §1 TL;DR and §6 catalog row 4; docs/index.html (chemistry card); vs physics hub, W.0, §11.6.5, §18.8; chemistry CH.13

**Quote.** AGENTS.md: "Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405)." and "`c²=B/ρ` (0.06% sim); `φ_RCP=0.7405`".  Chemistry body: "Crystal packing fractions are pure geometry: FCC/HCP π/(3√2) = 0.7405".  Physics W.0: "φ_jam = 0.633 — Isostatic jamming/packing fraction (z to 6); distinct from 2/π = 0.6366."  §18: "isostatic jamming ($z{=}6$, $\phi_{\mathrm{jam}}\!\approx\!0.64$)"

**Evidence.** π/(3√2) = 0.74048 is the maximal ordered (Kepler) packing density. Random close packing of monodisperse spheres is ≈0.64, consistent with the physics volume's own simulated φ_jam = 0.633 at z = 6. The aggregate pages therefore mislabel the substrate's packing fraction and contradict the root volume.

**Proposed improvement.** In AGENTS.md, the homepage, and the manifest headline, change to 'jammed at random close packing (φ_RCP ≈ 0.64; simulated φ_jam = 0.633)'. Keep 0.7405 only where FCC/HCP crystal packing is meant (chemistry CH.13). Regenerate the aggregates from the manifest.

### 13. [minor] The 89/82 ratio is said to 'track m_n > m_p', but 89 is assigned to the proton and 89/82 is 1.085, while m_n/m_p is 1.0014; another section says it tracks m_n ≈ m_p

- **category:** internal-inconsistency
- **location:** §1 lead and §1.9 A4 (01-governance…), §7.2.2 (07-3-sector…), §14.0 (14-force…)

**Quote.** §1: "The 89/82 legitimately tracks mₙ>mₚ (gravity), not Coulomb."  §7.2.2: "$N_p:=82+7=89.$" … "$N_n:=82.$"  §14.0: "Consequently the ratio 89/82 is a gravity/mass-sector quantity (it tracks the mₙ≈mₚ core, not charge)"

**Evidence.** 89/82 = 1.08537, while m_n/m_p = 1.001378. With N_p = 89 > N_n = 82, any monotone count→mass reading predicts m_p > m_n, the wrong sign (m_n − m_p = +1.293 MeV). §1 says 'm_n > m_p' and §14.0 says 'm_n ≈ m_p', which are different claims.

**Proposed improvement.** Either derive a stated quantitative map from (82, 89) to (m_n − m_p)/m_p that has the right sign and magnitude, or remove 'tracks m_n > m_p' and describe 89/82 only as a structural count ratio with no mass claim.

**Strengths noted:**
- All closed-form arithmetic I recomputed from CODATA values matches the text: 6π⁵ = 1836.118109 (−18.82 ppm), 3π⁴ = 292.227273, U_lat = hc/a = 1958.70331 GeV, m_H = 124.694926 GeV, τ_q = D/c = 1.618659959e-20 s, T_e measures 1.0056 / 0.527 / 0.333 s, χ = 89.9378° for the stated inputs, the α form = 137.036415 (+3.03 ppm), and the lattice counts 19/27/81/123 (3D) and 21 (2D).
- The demotions are genuine: α_em is re-graded to [O] as a coincidence, the 89/82 Coulomb factor is retracted as overfit, the absolute gravity magnitude is openly back-substituted, and §18.8 records an honest negative (the gravity sector is degenerate with GR). This is the grading discipline working as intended.
- Coefficients are not migrated to close residuals (5π stays 5π, not 4.98π). The residuals are published, and the SSOT tool states the baseline for each residual and internally flags the 80-digit A as a placeholder.
- The framework attempts real pre-registration: explicit kill criteria, a committed light-angle number, the registered open gate G-ISO, and a public disclosure that the full-precision wavelength moves χ. Once the inputs are fixed (see the light-angle finding), this is the right structure for a falsifiable claim.
- The distinction between c_ref as input and c_env as output is the right one to draw conceptually. c² = B/ρ with G → 0 at isostatic z = 6 correctly reproduces textbook jamming scaling (O'Hern, Liu, Nagel, Wyart).


## lens:look-elsewhere

### 1. [critical] The Higgs 'prediction' m_H = U_lat/(5π) depends on two arbitrary choices, N = 10^12 and the He–Ne laser line; the N-invariance table hides this

- **category:** numerology-look-elsewhere
- **location:** docs/physics/01-governance-no-tuning-lock-gate §1.8.2, §1.9 A5; docs/physics/w5-anti-circular-logic-chain-light §W.5.4; docs/physics/11-realization-units-t-rcross §11.2; docs/physics/13-mass-u-lat-m-h §13.1, §13.3.7

**Quote.** §1.8.2: "| m_H/U_lat | 1/(5π) | 1/(5π) | 1/(5π)" ... "Confirmed by the released code; no N enters the closure equations." §W.5.4: "it is a non-trivial coincidence between the measured wavelength of a helium–neon laser and the measured Higgs mass, mediated by a six-line algebraic derivation containing no free parameters." §1.9 A5: "any other anchor in the window predicts the same dimensionless ratios." §11.2: "N is locked in analysis_lock and cannot be changed after seeing the result."

**Evidence.** The formula is U_lat = hc/a with a = λ_ref/N, so m_H = hcN/(5π λ_ref). In other words, U_lat is exactly 10^12 × the energy of one He–Ne photon (hc/632.99121 nm = 1.95870 eV → 1958.70 GeV). The N-invariance table lists m_H/U_lat, which is 1/(5π) by definition, so the table tests nothing. The actual output in GeV scales linearly with N: N=10^11 gives 12.47 GeV, N=10^12 gives 124.69 GeV, N=10^13 gives 1246.9 GeV, and N=2^40 gives 137.1 GeV. The dimensionless ratio m_H/m_p = Nλ_C,p/(5πλ_ref) also depends on N, which contradicts A5. It also depends on which laser line is used: 532 nm gives 148.4 GeV, 543.5 nm gives 145.2, 612 nm gives 129.0, 780.24 nm gives 101.2, 1064 nm gives 74.2 and 1550 nm gives 50.9 GeV. The 0.40% hit therefore exists only because a neon atomic transition (a metrology convention) was paired with a decimal power of ten. How surprising is the hit at fixed U_lat? The target is U_lat/m_H,exp = 15.6446 and 5π = 15.708 (+0.405%). By Monte Carlo over a log-uniform target in the surrounding decade, n·π^k (n≤12, k∈[−6,8], 180 forms) lands within 0.405% with P≈0.088, and (p/q)·π^k (p,q≤12, 1365 forms) with P≈0.48. With N and the laser line free, P→1. The hit is also 4.6σ from the value the page itself quotes: (124.695−125.20)/0.11 = −4.59σ.

**Proposed improvement.** (1) Replace the §1.8.2 row with m_H[GeV] evaluated at N=10^9, 10^12 and 10^15 (0.1247, 124.69 and 124,695 GeV) and state plainly that m_H scales with N/λ_ref. (2) Remove the sentence in A5 claiming the ratios are anchor-independent, or restrict it to ratios that truly contain neither N nor λ. (3) Either derive N and the choice of anchor transition from the lattice (a must become an output) or downgrade m_H to [O] as a "numerical observation conditional on (λ_ref, N)". (4) Take m_H out of the §1.9 A3 coincidence set. (5) Rewrite §W.5.4 to say that the relation links a neon 3s2→2p4 photon energy × 10^12 to m_H, and that no mechanism for that is offered.

### 2. [critical] 'DOF = 1 / no tuning' leaves out at least four continuous inputs and all discrete choices; the tests used to prove no-tuning cannot detect choosing among formulas

- **category:** grading-honesty
- **location:** docs/physics/01-governance-no-tuning-lock-gate §1.8.1, §1.8.3, §1.8.4; docs/physics/w0-result-scorecard-one-page-summary §W.0, §W.2.1 (header chips on every chapter page); docs/physics/05-geometric-rectification-constants-single-source §5.0; docs/physics/13-mass-u-lat-m-h §13.4.5; docs/physics/axp-… P.4; repro/physics/tools/vp_numeric_ssot.py

**Quote.** Chip: "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." §1.8.1: "The total tunable DOF count is therefore exactly one, and it is exposed in step 3." SSOT table: "| mₑ | CODATA | canon_lock | §13.5 | mass-scale anchor | anchor" and "| g₀ | 2×10⁻⁷ | analysis_lock | §10.3 | microscopic gap threshold | chosen". App P script: "assert abs(r_p/8.412e-16 - 1) < 5e-4, \"canon r_p not reconciled to v0.4.1 (0.8412 fm)\"". vp_numeric_ssot.py: "ME     = D(\"9.1093837015e-31\"),            # 전자질량 (CODATA)". §1.8.4: "A tuning workflow would have used the residual to migrate the coefficients by an arbitrarily small amount: 5π→ 4.98π". §5.0: "There is no place to insert a free coefficient: π does not adjust, 2 does not adjust, the integer counts are fixed by the lattice."

**Evidence.** The volume's own tables and code list these as inputs:
- continuous: λ_ref (a He–Ne line picked from a menu of metrology lines); m_e (CODATA), which fixes D = 2λ_C,e; N = 10^12; g₀ = 2×10⁻⁷, marked "chosen", which sets A ∝ 1/g₀ and hence Δt and T_e; r_p = 0.8412 fm (locked), still asserted in the App P/M scripts, and §13.4.5 computes the "predicted" m_p from it (λ_C = (π/2)·0.8412 fm → 0.938312 GeV, +42 ppm); Δt = 1.86e-21 s, labelled a 3-significant-figure placeholder in the repo tool.
- discrete: the n-fold law's prefactor, exponent, per-lock factor and conversion factor (≈4 choices); κ_H = 6−1 and the per-channel π normalization (2); the T_e cell measure, 1 of 3; the best-of-M avalanche for D; mean versus median for A; and in the α_em form 4π, 11 = 7+3+1, δ₀ = 2/π², 35/32 and 3/7 (5).
That is about 4–5 continuous inputs and ≥12 discrete selections, not 1. With a closed-form grammar, the tuning happens by choosing among discrete forms, not by nudging coefficients. Nobody would migrate 5π→4.98π because that would break the integer story, so declining to do so shows nothing. The five-line check asserts arithmetic identities (e.g. 2/π = 0.6366…; lattice counts 19/27/81/123, which I verified are correct), so it cannot fail and cannot catch any fitted choice. The header chips grade the empirical anchor λ_ref and D = 2λ_C,e as "[F] forced", which contradicts the SSOT table (anchor / anchor-derived).

**Proposed improvement.** Replace §1.8.1 with a two-column ledger: (a) continuous inputs, listing λ_ref, m_e, N, g₀, r_p(locked, where still used) and Δt(placeholder), each with its value and the claims that consume it; (b) discrete selections, listing each choice point, the alternatives that were available, and the one taken. Report 'effective DOF = continuous + log2(number of alternatives) summed over selections'. Grade λ_ref and D as [L]. Retire the 5π→4.98π argument. Replace the five-line check with a script that enumerates the declared grammar and reports look-elsewhere p-values (see the protocol finding).

### 3. [critical] Claims graded [F] 'forced' and 'exact' are excluded by measurement at 10^6σ (6π⁵) and 4.6σ (5π), and the falsification rules exempt residuals

- **category:** grading-honesty
- **location:** docs/physics/w0-result-scorecard-one-page-summary §W.0; docs/physics/sp-jamming-spine-verified-physical-backbone; docs/physics/01-governance-no-tuning-lock-gate §1.10 'What we do not call falsifiers'; docs/physics/13-mass-u-lat-m-h §13.3.7, §13.5.5

**Quote.** W.0: "| mₚ/mₑ = 6π⁵=2π· 3π⁴ (νₚ via LOCK-NU-N §8.0.5) | 1836.118 vs measured 1836.153 | [F]{} | -19ppm". SP: "All three statements are exact; none is inflated and none is diminished." §1.10: "(i) \"the closure has a 0.4% residual\" — the residual is reported openly and is part of the deliverable". §13.3.7: "m_H^exp=125.20± 0.11GeV"

**Evidence.** 6π⁵ = 1836.118109 and CODATA 2022 gives m_p/m_e = 1836.152673426(32). The residual is −18.82 ppm, i.e. −1.08×10⁶ standard deviations (−3.1×10⁵σ against CODATA 2018). As an exact 'forced' identity it is therefore refuted. The same holds for m_H = 124.695 GeV against 125.20 ± 0.11 GeV (−4.6σ, using the page's own error bar). Neither claim states a theoretical uncertainty. Declaring that a residual is not a falsifier then makes the two headline numbers immune to any measurement. Publishing the residual openly is honest, but it does not turn a failed exact claim into a success.

**Proposed improvement.** For every quantitative [F] claim, state before comparison either 'exact' or 'leading order, with the correction of order X still open'. Grade 6π⁵ as '[F] structure / [O] correction: an 18.8 ppm term is required and not derived'. Grade m_H as [O] (it fails at 4.6σ unless a theory error of ≥0.5 GeV is declared and justified). Add a kill criterion: 'if the derived correction to 6π⁵ does not reproduce −18.82 ± 0.02 ppm, LOCK-NU-N is falsified.' Delete 'exact' from the SP spine sentence.

### 4. [major] How surprising 6π⁵ is: a real ~10⁻³ coincidence, but found by Lenz in 1951; the n-fold law was fitted to it afterwards, and a label was softened for rhetorical reasons

- **category:** numerology-look-elsewhere
- **location:** docs/physics/08-discrete-proton-structure-82-7 §8.0.5 (III), §8.0.6 (B)–(C); docs/physics/vh-appendix-version-history-reclassification-log v0.2.1; docs/physics/ea-epistemic-audit-log-what-happened v40; docs/physics/00-prologue-how-use-this-document (Misreading 7)

**Quote.** §8.0.5: "The electron case is a nontrivial check: the law reproduces the independently defined electron clock of §9.3, it is not fitted to it." §8.0.6 [MAP-2]: "and the n sectors contribute additively (prefactor n, §7.1)". VH v0.2.1: "rₚ reclassified from a free canonical input to a derived prediction rₚ=D_anch/(6π⁶)=0.84125 fm under LOCK-NU-N (§8.0.5)". EA v40: "Lenz (1951) characterization changed from \"numerical coincidence\" to \"preceded the present derivation\" (so that external readers do not read the Lenz mention as a concession that our result is also numerology)." Prologue: "Lenz 1951 for mₚ/mₑ=6π⁵ as numerical coincidence"

**Evidence.** Monte Carlo with a log-uniform target in the decade around 1836 and a 18.8 ppm tolerance:
- n·π^k (n≤12, k∈[−6,8]; 25 forms per decade): P(≥1 hit) = 4.1×10⁻⁴, about 11.3 bits.
- (p/q)·π^k (p,q≤12; 175 forms per decade): P = 2.9×10⁻³, about 8.4 bits.
This is a genuinely notable coincidence. But it was known before the framework: VH v0.2.1 shows ν_p was previously the length-route value with r_p as a free input, and 3π⁴ was adopted afterwards. A law adopted after the target is known is an accommodation. The probability that it reproduces 6π⁵ is ≈1 whether or not VP is true, so it adds almost no evidence beyond Lenz's bare observation.

The law's own choice points span a grammar about the size of family A. ν_n = g(n)π^{2(n−1)} passes the 'nontrivial' n=1 check for any g with g(1)=1. For n=3 the candidates give different ratios: g=n → 6π⁵ = 1836; g=n² → 5508; g=n! → 3672; g=2^{n−1} → 2448; g=1 → 612. Only the prefactor that the data select was chosen. [MAP-2] also sums over sectors ('additively'), while §8.0.6(A) requires them to survive simultaneously (AND → product) — two incompatible logics for the same sectors.

The EA log changes a label specifically to avoid appearing as numerology, and the prologue still carries the old wording. That is inconsistent and contrary to the volume's own honest-grading rule.

**Proposed improvement.** Restore 'Lenz (1951) observed the numerical coincidence 6π⁵; LOCK-NU-N was adopted in v0.2.1 with that value known' and remove the rhetorical relabel from EA v40. Delete 'nontrivial check' for n=1. Tabulate the alternative g(n), exponent and per-lock-factor choices with their outputs, so readers can see how large the effective grammar is. Credit the 6π⁵ hit only at the level of the P≈4×10⁻⁴ observation, not as confirmation of the VP mechanism.

### 5. [major] The exponent n−1 is justified in two incompatible ways, and the 'one lemma, three uses' argument relies on the α_em construction the volume itself declares non-evidence

- **category:** internal-inconsistency
- **location:** docs/physics/08-discrete-proton-structure-82-7 §8.0.5 (II), §8.0.6 (A),(B),(D); docs/physics/13-mass-u-lat-m-h §13.3.3–13.3.4; docs/physics/14-force-lattice-tension-1-r2 §14.5.3; docs/physics/05-geometric-rectification-constants-single-source §5.0 decoder

**Quote.** §8.0.5(II): "which is the same linear-algebra count as the Higgs channel reduction 6-1=5 (§13.3.4). Independent locks accumulate by the §5.2 product measure". §8.0.6(A): "the C₃ ring-closure Σ_in_i=0 (§8.0.3) fixes the global phase as a gauge choice and removes no rectification." §8.0.6(D): "Fine structure (§14.5.3): N=7 shell signs ⇒ 7-1=6 free signs, i.e. 2⁶ projection microstates in β_disc=210/192=35/32." ... "the recurrence across three independent constants is a structural signature, not three tunings." §14.5.3: "(contrast 6π⁵, 3π⁴, α=2/π, δ=1/π², which are single forced integrals)". §5.0: "| Higgs channel | m_H = U_lat/(5π) | 5 channels (cell-face count minus global-reference) / one rotation averaged"

**Evidence.** §8.0.5(II) gets exponent n−1 because the gauge mode removes one lock. §8.0.6(A) says the gauge removes no rectification, giving ⟨W_n⟩ = δ^n. There n−1 reappears only from ν = s·δ in (B), i.e. one δ multiplied back, not from dim(R^n/span 1). So the gauge lemma is not the source of the nucleon exponent. The 'three uses' list includes the α_em 2⁶ count, which §14.5 labels COINCIDENCE/NON-EVIDENCE and bars from supporting any conclusion. Using it to argue 'structural signature, not three tunings' breaks that bar. §14.5.3 calls 6π⁵ and 3π⁴ 'single forced integrals', but §8.0.6(C) says they rest on the definitional maps [MAP-1]/[MAP-2] plus the α/δ conversion. The §5.0 decoder reads the Higgs π as 'one rotation averaged', while §13.3.3 derives it as a disk area π(a/2)² normalized by a²/4. It reads 6π⁵ as '6 paired contributions, 5 nested rotations', while the derivation gives 6 = 2(from α/δ)·3(sectors) and π⁵ = π(α/δ)·π⁴(two locks). A decoder that can relabel any π^k after the fact places no constraint.

**Proposed improvement.** Choose one derivation of n−1 and delete the other. Remove the α_em item from the §8.0.6(D) list, and remove the 'structural signature' sentence, or rest it only on the two non-quarantined uses. Change §14.5.3's contrast to 'single forced integral plus the [MAP-1]/[MAP-2] definitional lock'. Make the decoder table repeat the actual derivation provenance of each factor rather than a separate narrative.

### 6. [major] α_em formula: a 3 ppm hit is expected within its grammar; the formula was refined from 4π(11−δ) (−578 ppm) to 4π(11−(15/16)δ), and the reproduction dossier still checks the old form

- **category:** numerology-look-elsewhere
- **location:** docs/physics/14-force-lattice-tension-1-r2 §14.5.1–14.5.4; docs/physics/w0-result-scorecard-one-page-summary; repro/physics/reports/DOUBT_REMOVAL_MAP.md:26, reports/FORCED_CHAIN_MAP.md:78, reports/PHASE1-2_AUDIT_FINDINGS.md:50 (same in verification_dossier/)

**Quote.** §14.5.3: "α_{em,\mathrm{VP}}^{-1} =4\pi\left(11-\frac{35}{32}\cdot\frac{2}{\pi^{2}}\cdot\frac{3}{7}\right) \approx 137.0364." and "The +3 ppm agreement should accordingly be read as evidence conditional on that identification, not as an independent zero-parameter prediction." FORCED_CHAIN_MAP.md: "α_em ≈ 1/137      측정 입력.  4π(11−δ)=136.957 ≠ 137.036 → coincidence/non-evidence (→ D3)"

**Evidence.** The correction factors multiply out to (35/32)·2·(3/7) = 15/16, so the formula is 4π(11 − (15/16)/π²) = 137.036415 (+3.03 ppm vs 137.035999177). The dossier's 4π(11−1/π²) = 136.9568 (−577.7 ppm). The x required in 4π(11 − x/π²) is 0.937826, and 15/16 is the only fraction with q≤16 within tolerance. I enumerated the grammar P·(n ± (p/q)·π^−j) with P∈{π, 2π, 4π, π²}, n≤59, p/q≤2 with q≤32, and j∈{1,2,3}: about 9.2×10⁵ forms. For a random target in [120,160] the chance of at least one hit within 3.1 ppm is P = 0.79, so a ppm-level hit is expected. The §14.5 status note already concedes this ('many integer-and-π forms match 137.036 to ppm'), which is to its credit. However, §14.5.3 still calls it 'evidence conditional on that identification', contradicting 'NON-EVIDENCE'. And the repo audit justifies the label with a formula that is not the one on the page.

**Proposed improvement.** Delete the 'evidence conditional on…' sentence from §14.5.3. Correct the three dossier files to evaluate the published δ_proj form (137.0364, +3.0 ppm), and record the δ → (15/16)δ refinement as a trial in a failures/trials ledger. Apply §14.5's three demotion criteria (the assembly is not forced; there is degeneracy in the grammar; units/scale are conventions) consistently to 6π⁵ and 5π, and publish the result of doing so.

### 7. [major] The amplification A = 880918.977 presented as measured [V] is exactly cΔt/a, while Δt is fixed by Aa/c; the '0.16% match' ignores a ~7% statistical error

- **category:** circularity
- **location:** docs/physics/w0-result-scorecard-one-page-summary §W.3.2; docs/physics/11-realization-units-t-rcross §11.6; docs/physics/01-governance-no-tuning-lock-gate §1.9 A3; repro/physics/tools/vp_numeric_ssot.py

**Quote.** W.3.2: "| A=880918.977… | [V]/[H] | verify_amplification_A.py; soc_percolation_pinning.py (seeds logged) | measured from the lattice (a_med/g^*), not a free fit" and "| Δ t=1.86×10⁻²¹ s | [H] | … | locked via Δ t=Aa/c_ref with RCROSS two-wavelength sealing". §11.6: "the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%". Tool: "(\"A_geo\",\"cΔt/a\",f(q['A_geo'],4),\"[H] Δt 3 s.f. ⚠placeholder\")"

**Evidence.** c·(1.86×10⁻²¹ s)/(6.3299121×10⁻¹⁹ m) = 880918.9777 reproduces the tabulated 'measured' A to 9 digits. The number is therefore a placeholder Δt converted into A, not a simulation output. The simulations give A_med = 8.02×10⁵ (N=200) and A_med = 4.76×10⁵ / A_mean = 5.69×10⁵ (N=750). Δt is locked from A and A_geo from Δt, which is circular. The '0.16%' uses the mean at N=750 but the median at N=200, and does not say which reference N was used for the N^{−1/3} rescaling. Using N_ref = 200 (the other run), 880919·(200/750)^{1/3} = 5.670×10⁵, off by 0.35%. From the stated p10–p90 range (4.4–21×10⁵), a lognormal has σ_ln ≈ 0.61 and CV ≈ 0.67. For 104 events that gives SEM ≈ 6.6%, so the 0.16% agreement is ~0.02σ and carries almost no information. Yet A_geo is counted as one of the five surviving coincidences in §1.9 A3.

**Proposed improvement.** Re-tag A = 880918.977 as '[H] = cΔt/a (definition), not a measurement'. Report the simulated A as median ± bootstrap CI at each N. Pre-declare the statistic (median) and the scaling reference N. State the agreement as 'consistent within ~7% (1σ)'. Remove A_geo from the A3 coincidence set until Δt is fixed independently of A.

### 8. [major] Some corroborating numbers are chosen from distributions or option sets after the fact: the best-of-M avalanche for D and the one-of-three cell measure for T_e

- **category:** numerology-look-elsewhere
- **location:** docs/physics/11-realization-units-t-rcross §11.6; docs/physics/03-axioms-primitives-volume-particle-lattice §3.4; docs/physics/12-electron-1-second-cross-check (O(1) residual table); docs/physics/01-governance-no-tuning-lock-gate §1.9 A3

**Quote.** §11.6: "over the 82-core the 633-channel circulation length has median 4.96 pm with a best-matched avalanche at 4.8542 pm (target 4.85)." §3.4: "the jamming simulation independently reproduces the length to 0.04% (4.8542pm — a selected length with a 7% distribution". §12: "Only the bounding-cube measure lands on the clock". A3: "The joint probability of the surviving five under a six-line geometric chain with one anchor is the structural claim."

**Evidence.** I simulated drawing M avalanches from a distribution with median 4.96 pm and 7% spread, then picking the one closest to 4.8526 pm. The chance that the best lies within 0.04% is 0.31 for M=83, 0.37 for M=104 and 0.58 for M=200. The median best deviation is 0.061% for M=104. So '0.04%' is what selection alone produces, and the median (+2.2%) is the honest figure. For T_e, three admissible cell measures give 1.0056 s, 0.527 s and 0.333 s, and the one that lands is kept. That is a trials factor of 3 before any other freedom (N, g₀; see the unit finding). §1.9 A3 then treats T_e, A_geo and the r_p/D chain as independent coincidences, but never computes the 'joint probability' it says is the structural claim.

**Proposed improvement.** Report the jamming D as median with a 68% interval (4.96 pm, ±7%) and drop the 'reproduces to 0.04%' and RCROSS 'PASS' wording. For T_e, derive the measure (gate G-TE-O1) before counting it, and meanwhile record a trials factor of 3. Recompute A3 as an explicit product of look-elsewhere-corrected p-values (see the protocol finding). On present numbers, nearly all the evidential weight is in 6π⁵ (~8–11 bits) and r_p/λ_C,p = 2/π (~3.5–6 bits); m_H, T_e and A_geo add ≈0 bits once N, g₀ and selection are counted.

### 9. [major] The electron '1 second' and ν_p = 292 s⁻¹ give a dimensionless lattice ratio SI units; T_e scales as N², contrary to the N-invariance claim

- **category:** unit-dimension
- **location:** docs/physics/09-event-quantum-definition-canonical-event §9.4; docs/physics/12-electron-1-second-cross-check (grade box); docs/physics/13-mass-u-lat-m-h §13.5.6; docs/physics/14-force-lattice-tension-1-r2 §14.0; docs/physics/01-governance-no-tuning-lock-gate §1.8.2, §1.9 A2

**Quote.** §9.4: "Here “Hz=s⁻¹” reads the canonical second as equivalent to the SI second; the equivalence judgment is performed by the unit-realization (cross-validation) Gate." §14.0: "νₚ=3π⁴≈292s⁻¹ and νₑ=1s⁻¹ (§12)". §12: "the geometry path itself triangulated three ways (small-lattice direct count, Tₑ∝ N² scaling invariance, and the 5-of-6 three-fold channel ratio)". §13.5.6: "ν_{p,\mathrm{can}}=3\pi^{4}\approx 292.227\ \mathrm{s^{-1}}"

**Evidence.** ν_n = nπ^{2(n−1)} is a pure number. Attaching s⁻¹ implies the electron's event rate is exactly 1 per SI second. The SI second is a human unit: 9,192,631,770 Cs-133 periods, historically 1/86400 of a mean solar day. No lattice mechanism can land on it except by coincidence of conventions. §13.5 writes m_p/m_e = 2π·ν_p with ν_p in s⁻¹, which mixes a dimensionless ratio with a rate. The formula T_e = (6/5)(D/a)³Δt with a = λ/N and Δt = Aa/c gives T_e ∝ A·N², hence ∝ N²/g₀. At fixed locked Δt: N=10^11 → 0.0101 s, N=10^12 → 1.0056 s, N=10^13 → 100.6 s. '≈1 s' therefore depends on the decimal choice N = 10^12 and the chosen threshold g₀. Calling N² scaling an 'invariance' contradicts §1.8.2 ('no N enters the closure equations').

**Proposed improvement.** Write ν_p/ν_e = 3π⁴ as dimensionless everywhere and drop 'Hz' and 's⁻¹'. Reclassify 'T_e ≈ 1 s' as a unit-convention coincidence conditional on (λ_ref, N, g₀), graded [O], and remove it from the §1.9 A3 set. In §1.8.2 add rows for T_e and m_H showing their N dependence. If the claim is to stay, derive the Cs-133 hyperfine frequency (or the SI second) from the lattice; otherwise it cannot be physical.

### 10. [major] The only pre-registered prediction (light angle χ) disagrees with the framework's own canonical inputs and, within its stated width, rules out nothing

- **category:** missing-test-or-prediction
- **location:** docs/physics/10-implementing-speed-light-clock-free §10.9, §10.9.1; docs/physics/01-governance-no-tuning-lock-gate §1.9 B1, §1.10 Kill criterion 3; docs/physics/11-realization-units-t-rcross §11.2

**Quote.** §10.9.1 table: "| 632.99 nm | 130442.9232 | 130443 | 89.9378^(∘) | 141.59D" and "their stated width is the χ-distribution induced by the ℓ_rot spread (§11.6)." §1.9 B1: "hypersensitive, 0.03% in D ⇒>1^(∘) in χ". §11.2: "λ_{\mathrm{ref}} = 632.99121257859865746\ \mathrm{nm}."

**Evidence.** The formula is sinχ = λ/(mD) with m = ⌈λ/D⌉. With the canonical λ_ref = 632.99121258 nm and D_anch = 4.852620477 pm, λ/D = 130443.1730 and m = 130444, giving χ(633) = 89.7960°, not the committed 89.9378°. The committed value comes from the rounded λ = 632.99 nm, a 1.9 ppm change that moves χ by 0.14°. χ is a sawtooth function of the fractional part of λ/D: a relative change of 2×10⁻⁶ in D shifts χ by 0.14°. Its full range is bounded, χ ∈ [90° − √(2/m) rad, 90°) = [89.776°, 90°). So '0.03% ⇒ >1°' is impossible; the maximum swing is 0.224°. D's stated honest precision (0.04%, spanning ~52 integer wraps) and the ℓ_rot spread (7%) both cover the whole band. Uniformly drawing D in ±0.04% gives χ between 89.776° and 89.999°, with only 4.9% of draws within ±0.01° of 89.9378°. As registered, the prediction forbids nothing inside the near-transverse band. The lattice axis it is measured against is also unspecified (G-ISO open).

**Proposed improvement.** Recompute the committed table from the canonical locked inputs and correct the '>1°' statement to 'max 0.224° (633 nm)'. Recognize that χ at a given λ cannot be predicted beyond 'χ ∈ [89.78°, 90°)' unless D is known to ≲10⁻⁷. Either commit to that set-level statement together with a specific, measurable axis and protocol, or pre-register a quantity that varies smoothly with D. Retract 'Kill criterion 3 is armed' until then.

### 11. [major] The 'mass grand-unification' gate cannot fail: it passed with the withdrawn electron-mass formula, which is wrong by a factor π²

- **category:** reproducibility-code
- **location:** docs/physics/axm-mass-grand-unification-geometric-differentiation M.3–M.5; docs/physics/axe-geometric-origin-electron-mass-direct (correction banner, E.2); docs/physics/13-mass-u-lat-m-h §13.5.3.3, §13.6

**Quote.** App M script: "r_e = (D_anch/2.0) * delta" / "S = r_e / a_m" / "I_e = (m_e * S) / U_lat_GeV"; M.3: "By definition, ideally I_H=Iₚ=Iₑ=1 should hold (a channel that numerically reconfirms identical definitions)." App E: "the spurious universal-regime form S=D_anch/(2aπ²) of earlier drafts is withdrawn". §13.5.3.3: "\boxed{ S=\frac{D_{\mathrm{anch}}}{2a\pi^2} }"

**Evidence.** In M.5, m_H = U_lat/(5π), m_p = U_lat/S_p and m_e = U_lat/S, and then I_X = m_X·σ_X/U_lat. Each invariant is therefore identically 1, dev_max ≡ 0, and G-RATIO-MASS-UNIFICATION always returns PASS. The script still uses the withdrawn S = r_e/a with r_e = (D/2)δ. That gives m_e = 1958.703 GeV/388,374 = 5.043 MeV (π² × 0.511 MeV), and the gate still PASSes, which shows it tests nothing. No line compares any output with a measured value. §13.5.3.3 still presents the withdrawn formula as a boxed result, while §13.5.4 and App E say it is wrong.

**Proposed improvement.** Fix M.5 to use λ_C,e/a. Replace the tautological invariants with external-comparison gates that have pre-registered tolerances and theory errors (e.g. |m_H − 125.20|/√(0.11² + σ_th²) ≤ 2, |6π⁵/1836.152673426 − 1| ≤ σ_th). Strike or visibly mark §13.5.3.3 as superseded. Add a CI test that runs every appendix script and diffs its output against the text.

### 12. [major] No look-elsewhere or model-comparison analysis exists; the 'coincidence count' is stated but never computed. A credibility protocol is proposed

- **category:** missing-test-or-prediction
- **location:** docs/physics/01-governance-no-tuning-lock-gate §1.9 A3, §1.10 'Demarcation from pseudoscience'; docs/physics/05-geometric-rectification-constants-single-source §5.0; repro/physics/tools/ (no LEE tool)

**Quote.** A3: "This is not proof; it is a coincidence count." §1.10 table: "| Hidden numerology | decoder table π/2 | §5.0". §5.0: "these are not numerology, they are integrals."

**Evidence.** The volume's defence against numerology is a narrative decoder plus refusing to migrate coefficients. Neither measures how many forms were available. My scans (seed 19) give the following probabilities of a chance hit: m_p/m_e at 18.8 ppm, P = 4.1×10⁻⁴ (n·π^k) or 2.9×10⁻³ ((p/q)π^k); U_lat/m_H at 0.4%, P = 0.088 or 0.48; r_p/λ_C,p at 0.06% (CODATA 2022), P = 0.013 or 0.087, where 7/11 fits better than 2/π (175 vs 578 ppm); α⁻¹ at 3 ppm under the δ-corrected grammar, P = 0.79. The corpus also records at least three documented after-the-fact insertions or removals: 89/82 in the Coulomb constant (−0.43%, later evicted as overfit); δ → (15/16)δ in α_em; the δ/Compton switch in m_e. These are trials that any significance statement has to count.

**Proposed improvement.** Adopt and publish this protocol:
(1) Pre-register the grammar. Before any new comparison, deposit on Zenodo with a SHA-256 the exact expression grammar G (allowed integers, π powers, rationals, operators) with a description-length prior P(e) ∝ 2^−L(e), plus the list of target constants and their tolerances.
(2) Look-elsewhere scan. Add repro/physics/tools/lee_scan.py, which enumerates G, computes for each claim p = P(∃e∈G: |e/T−1| ≤ ε) for log-uniform T over the plausible decade, and multiplies by the number of targets tried, including failures from a public trials ledger (Coulomb 89/82, α_em refinements, m_n/m_p via 89/82, and so on). Gate the text on its output.
(3) Bayesian comparison. Each claim must declare a theory error σ_th before comparison. Compute the Bayes factor K = p(x|H_VP, σ_th)/p(x|H_null), with an Occam factor 1/|G_eff| for selection within the grammar, and give K ≈ 1 to accommodations of values known beforehand (6π⁵). Worked example: a pre-declared σ_th = 20 ppm against a log-uniform null over two decades gives a likelihood ratio of about 5.9×10⁴; dividing by |G_eff| ≈ 180 gives K ≈ 300 for 'a Lenz-type π law', but ≈1 for the VP mechanism specifically, because it was fitted afterwards.
(4) Blind prediction. Use the frozen grammar, with no new choices, to commit to quantities not yet measured or not yet precise, before the measurement. Candidates: the −18.82 ppm correction to 6π⁵; r_p to ±0.01%, testable against upcoming PRad-II/MUSE/AMBER results; a quantitative m_n − m_p from the 82/89 structure. Publish the hash in advance.
(5) Blinding. Have a second person hold out a set of constants that the author evaluates only after the grammar is frozen.

### 13. [minor] CODATA editions are mixed, precision is stated far beyond what the inputs support, and prior literature for r_p = 4ħ/(m_p c) is not credited

- **category:** presentation-rendering
- **location:** docs/physics/13-mass-u-lat-m-h §13.3.7, 'No-tuning fingerprint'; docs/physics/01-governance-no-tuning-lock-gate §1.9 A3; docs/physics/14-force-lattice-tension-1-r2 §14.5; docs/physics/w0-result-scorecard-one-page-summary §W.2.1; repro/physics/tools/vp_numeric_ssot.py

**Quote.** §13.3: "rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm)"; tool: "MEAS = dict(MPME=D(\"1836.15267343\"), RP_CODATA=D(\"0.8414\"), MH_PDG=D(\"125.20\"))"; §14.5: "(Reference value (e.g., NIST/CODATA 2022): inverse fine-structure constant αₑₘ⁻¹=137.035999177(21)."; §13.3.7: "m_H = \frac{1958.7033116641428}{5\pi}\ \mathrm{GeV} = 124.69492564072544\ \mathrm{GeV}"

**Evidence.** α is quoted from CODATA 2022, but r_p (0.8414 fm), m_p/m_e (1836.15267343) and m_e (9.1093837015e-31) are CODATA 2018 values. Against CODATA 2022 r_p = 0.84075(64) fm, the prediction 0.841251 fm is +0.060% (+0.78σ), not −0.018%. The relation r_p = (2/π)λ_C,p is identical to r_p = 4ħ/(m_p c) = 0.841236 fm, which has appeared in earlier literature (e.g. Haramein 2013); it deserves a citation and a look-elsewhere statement. Quantities are printed to 17–20 significant figures (124.69492564072544 GeV; λ_ref = 632.99121257859865746 nm), although the volume states D is known to only 4 significant figures and m_H is ±0.09%.

**Proposed improvement.** Switch all reference values to CODATA 2022 / PDG 2024 and cite the edition next to each number. Restate the r_p residual as +0.060% (0.8σ). Cite prior appearances of 4ħ/(m_p c) and of 6π⁵ (Lenz 1951). Round displayed outputs to their honest precision (e.g. m_H = 124.69 GeV, U_lat = 1958.70 GeV) and keep the long digits only in machine files.

**Strengths noted:**
- §14.5 is an excellent model of honest demotion. It withdraws the α_em 'derivation' and explains why: the formula's assembly is not forced, 4π(11−…) is one of many integer-and-π forms (it cites 4π³+π²+π as a degenerate rival), and α runs with energy. That same standard, applied uniformly, is the key improvement for 6π⁵ and 5π.
- The residuals are published rather than hidden: −18.8 ppm, −0.40%, +61 ppm, +0.56%. The repo's vp_numeric_ssot.py reduces them to two independent residuals (R1, R3) and marks Δt as a placeholder. This is exactly the kind of bookkeeping a referee wants.
- The ch.05 rectification integrals (⟨|cosθ|⟩ = 2/π, ⟨[cosθ]₊⟩ = 1/π, product measure → 1/π²) are correct and cleanly derived. The T1–T5 falsification triggers for δ (bias, correlation, numerical mismatch, definition drift, out-of-regime use) are well designed and testable.
- The lattice counts quoted in ch.07/§1.8.3 (19, 27, 81, 81, 123 for R² ≤ 2, 3, 6, 7, 9) are correct; I re-verified them. The Legendre 'R²=7 empty' observation is right.
- Errata are recorded in place rather than silently fixed (the App E banner on the π² electron-mass error, the §14.2 eviction of the 89/82 Coulomb factor, the VH reclassification log). The author already honestly concedes that 6π⁶ = π·6π⁵ is not independent, and that the ν_p length route is the same chain as m_p/m_e.


## lens:mainstream-physics

### 1. [critical] The headline 'light = the jammed solid's surviving longitudinal wave, c²=B/ρ with G→0' contradicts the volume's own transverse light, its Maxwell rewrite, and its blackbody law

- **category:** physics-validity
- **location:** sp-jamming-spine-verified-physical-backbone (S0 table, S2.3, S5); 11-realization-units-t-rcross §11.6.1; 10-implementing-speed-light-clock-free §10.9, §10.9.1; 14-force-lattice-tension-1-r2 §14.0.1, §14.0.6, §14.0.6b; 15-quantum-mechanics-mapping-completion-note §15.5.1; w0 scorecard row 'c² = B/ρ … [V]'

**Quote.** SP S2.3: "the relaxed (non-affine) shear modulus vanishes,G_{relaxed}→ 0, while the bulk modulusBstays finite (compression needs no surplus). The transverse wave dies; one longitudinal speed survives" | §10.9: "On the jammed lattice, light propagates as a transverse oscillation of the rotating quanta" | §14.0.6b: "On the transverse elastic rewrite (mathbf E:=-∂ₜmathbf u_T, mathbf B:=∇×mathbf u) … the momentum balance ρₘ∂ₜ²mathbf u=ρₘ c²∇²mathbf u+mathbf f turns the second equation into ∂ₜmathbf E=c²∇×mathbf B-mathbf f/ρₘ" | §14.0.1: "photons carry helicity ±1 (circular polarization = a rotating field)" | §15.5.1: "Including the usual electromagnetic prefactors gives g(ν)=8πν²/c_ref³"

**Evidence.** In an isotropic elastic medium ρü = (K+4G/3)∇(∇·u) − G∇×∇×u, so c_L² = (K+4G/3)/ρ and c_T² = G/ρ. The spine's own [V] result (G_relaxed→0, B finite) therefore leaves exactly one propagating branch, and it is longitudinal (helicity 0). Light has two transverse helicity ±1 states and no longitudinal one. The volume cites that fact itself in §14.0.1, and it needs it in §15.5.1: the factor 8π in g(ν) is 2 polarizations × 4π. (1) The §14.0.6b Maxwell rewrite uses the transverse field u_T. Its second equation follows from ρü_T = G∇²u_T, which gives ∂ₜE = (G/ρ)∇×B. The wave speed of the 'Maxwell sector' is therefore √(G/ρ), not √(B/ρ), and the spine drives it to 0. Writing 'ρₘc²∇²u' with c² = B/ρ for the transverse part is the error. (2) Blackbody: with the spine's single longitudinal mode, g(ν) = 4πν²/c³ and σ_SB halves: 2.835e-8 vs 5.670e-8 W m⁻² K⁻⁴. Quinn & Martin (1985) measured σ = 5.66967(76)e-8, which is −1.2e-4 (0.9σ) from the 2-polarization value and 3730σ from the 1-polarization value. (3) A helicity-0 photon coupled to charge compression would allow single-photon 0⁺→0⁺ (E0) transitions. These are strictly absent; for example, the 6.05 MeV 0⁺ state of ¹⁶O decays only by internal pair creation. (4) The 19th-century elastic aether problem was the mirror image of this one. To get transverse-only light, Green, MacCullagh and Kelvin had to remove the longitudinal mode (incompressible, or Kelvin's contractile K = −4G/3) while keeping shear finite. The spine does the reverse and presents the reverse as the verification. (5) §10.1.5.1 *defines* c̃² := B_eff/ρ_eff as an 'internal propagation indicator'. No time-of-flight or dispersion measurement shows that the carrier of light travels at √(B/ρ). The [V] only covers the textbook jamming statement G→0, B finite.

**Proposed improvement.** Split the grade. The [V] should cover only 'G_relaxed→0, B finite at z=2d (O'Hern/Wyart)'. Mark 'light is this mode' as [O], with the obstacle stated: a G=0 medium has no transverse branch, which conflicts with two polarizations, E0 selection rules and σ_SB. For a real fix, change the substrate model. One candidate is a micropolar (Cosserat) or MacCullagh rotational-elastic medium. There the propagating EM mode would be the rotation/twist mode with speed set by a rotational stiffness, and the longitudinal mode must be shown to be non-propagating (a constraint), not merely slow. Then derive g(ν) = 8πν²/c³ instead of importing the 8π. Add a gate that computes the longitudinal and transverse dynamic structure factors S_L(q,ω) and S_T(q,ω) in the simulated packing, counts the propagating branches, and measures their speeds by time of flight. Retitle the hub ('the Speed of Light as Its Elastic-Wave Speed') until that gate passes.

### 2. [critical] No quantitative Lorentz-violation analysis for a vacuum with a grain size, a preferred frame and a global axis; the volume's own lattice scale is excluded by ~8 orders of magnitude

- **category:** missing-test-or-prediction
- **location:** 18-time-and-gravity §18.3; 14-force-lattice-tension-1-r2 §14.0.1, §14.1.1; 11-realization-units-t-rcross §11.2.2; 15-quantum-mechanics-mapping-completion-note §15.1.4; 10-implementing-speed-light-clock-free §10.9.2

**Quote.** §18.3: "This is Lorentzian ether mechanics (a preferred medium frame, a dynamical contraction) — the opposite of special relativity, which it reproduces." | §11.2.2: "Define a as the fundamental diameter of the volume particle (VP)." with "a=6.3299121257859865746×10⁻¹⁹ m" | §14.0.1: "all quanta share one rotation axis because they are synchronized … a common axis hat z gives a global angular momentum L_z" | §10.9.2: "(ii) under which protocols the angle signature averages away (which is why isotropy-class precision propagation experiments need not have seen it)"

**Evidence.** The words 'Lorentz invariance', 'Michelson', 'Hughes–Drever' and 'SME' appear nowhere in the physics volume ('Lorentz' occurs only twice, both in §18). Three explicitly Lorentz-violating structures are present. (a) A discrete grain a = 6.33e-19 m, with a Brillouin zone in §15.1.4. If light is the lattice's elastic wave (the headline), the zone-edge cutoff is E = hc/(2a) = 9.8e11 eV, about 1 TeV. LHAASO has detected photons up to 1.4 PeV (Cao et al., Nature 594, 33 (2021)). Generic nearest-neighbour lattice dispersion gives Δv/c ≈ (ka)²/24. For the 31 GeV photon from GRB 090510, ka = 0.0994, so Δv/c = 4.1e-4: a delay of ~3e6 yr over 7.3 Gyr. The observed bound is Δv/c ≲ 6e-20 (Vasileiou et al. 2013, E_QG,2 ≳ 1e11 GeV). The equivalent E_QG,2 = √24·ħc/a = 1.5e3 GeV. Consistency would require a ≲ 7e-27 m, about 8 orders of magnitude below the stated a. (a is also fixed by the decimal split N = 10¹², a convention.) (b) A cosmic director ẑ shared by all rotating quanta, which carry charge. Such a background is exactly what clock-comparison and comagnetometer experiments bound: neutron SME c-coefficients ≲1e-29 (Smiciklas et al., PRL 107, 171604 (2011)). (c) A 'lattice/anisotropy axis' for light (§10.9), against modern Michelson–Morley tests: Δc/c ≲ 1e-17 (Herrmann et al. 2009) and ~1e-18 (Nagel et al., Nat. Commun. 6, 8174 (2015)). Lorentz-ether theory is empirically equivalent to SR only if *every* sector is Lorentz covariant with the same c. The §18.2 argument covers one model clock. Matter–light limiting-speed equality is bounded at ~1e-11 (Hohensee et al., PRL 102, 170402 (2009)) and is not addressed.

**Proposed improvement.** Add a dedicated [O] section, 'Emergent Lorentz invariance'. It should state which length sets photon dispersion (a, D or λ/A), write down the resulting dispersion relation ω(k), and compare it with Fermi-LAT GRB, LHAASO and vacuum-Cherenkov bounds. That comparison will either force a ≲ 1e-26 m or require an argument that light is not a lattice wave at scale a. It should also map ẑ and the χ-axis onto SME coefficients (c_μν, b_μ, k_F) and check them against the Data Tables for Lorentz and CPT Violation (Kostelecký & Russell). Until then the headline must carry the preferred-frame status explicitly, not only §18.3. The analog-gravity literature (Barceló–Liberati–Visser, Living Rev. Rel. 2011) is the natural template: it treats Lorentz symmetry as low-energy emergent and quantifies its breakdown.

### 3. [major] The 'unique, forced' √(1−v²/c²) in §18.2 rests on an unstated transverse-invariance assumption and on the Michelson–Morley result as a premise

- **category:** grading-honesty
- **location:** 18-time-and-gravity §18.2, §18.3, §18.10; repro/physics/tools/vp_exact_sqrt.py

**Quote.** §18.2: "The rate must therefore be independent of the winding orientation $\theta$, which forces $T$ to be $\theta$-independent: … \boxed{\,\kappa=\sqrt{1-v^2/c^2}\,}\quad(\text{unique})" | §18.3: "both are framework assets, so this is grade [F]." | vp_exact_sqrt.py docstring: "NO RELATIVITY is used (no Lorentz invariance, no spacetime geometry)."

**Evidence.** The T(θ;κ,v) formula lets only the longitudinal scale vary (κ) and silently fixes the transverse scale at ℓ = 1. With a transverse factor ℓ(v), the round trip is T = 2L·√(κ²c²cos²θ + ℓ²(c²−v²)sin²θ)/(c²−v²). Isotropy then fixes only κ/ℓ = √(1−v²/c²), and the clock rate becomes √(1−v²/c²)/ℓ, which is undetermined. I checked this numerically at v = 0.6 (exact light round trips). ℓ = 1.0, 1.1 and 0.9 all give anisotropy below 1e-15, with rates 0.800, 0.727 and 0.889 respectively. This is the known Lorentz/Robertson–Mansouri–Sexl degeneracy: Michelson–Morley constrains only the β−δ combination, while Kennedy–Thorndike and Ives–Stilwell (Botermann et al., PRL 113, 120405 (2014)) are independent experiments. The premise 'the moving clock's rate is orientation-independent' is also not a consequence of the medium's rest-frame isotropy. It is the ether-wind null result itself, imported as an assumption. So the value is 'forced' only given ℓ = 1 and MM-isotropy of moving matter. The derivation of the exact factor is Lorentz–FitzGerald (1889–1904), correctly reproduced, but it is not an [F] consequence of the medium.

**Proposed improvement.** Regrade §18.2 to '[F] conditional on (i) moving-clock isotropy (the MM null result as input) and (ii) ℓ(v) = 1 (RMS δ = 0)'. Grade the premise ℓ = 1 [H] until it is derived from the medium's dynamics; that is the same open item as the '[O] full-vector dynamics'. Extend vp_exact_sqrt.py with an ℓ parameter to demonstrate the degeneracy openly. Cite Kennedy–Thorndike and Ives–Stilwell as the separate empirical inputs that fix the remaining freedom.

### 4. [major] G-RIVER uses a medium velocity (√(2GM/r)) that §18.7 concedes the medium does not have; the physical mass current (∝1/r²) would give the wrong redshift law

- **category:** internal-inconsistency
- **location:** 18-time-and-gravity §18.0, §18.6, §18.7, §18.8; axg-geometric-derivation-gravity-lattice-yield G.2

**Quote.** §18.6: "Gravity is inflow, so the medium near a sink is genuinely moving inward; a clock held static in a gravity well is therefore a clock at rest in a \emph{moving} medium" | §18.7: "The incompressible mass-current that books the sink's steady consumption falls as $1/r^2$; the time-dilation velocity is the potential (free-fall/river) velocity and falls as $1/\sqrt{r}$" | §18.8: "redshift, orbits, light bending, and gravitational waves are the uncapped \emph{geom} channel, which equals exact Schwarzschild by §18.6"

**Evidence.** The stated principle (§18.9) is that a clock slows by its velocity relative to the local medium. By §18.7 the medium's actual velocity is the mass current v ∝ 1/r², which is what continuity with an incompressible steady sink gives. Applied literally, the dilation deficit would be v²/2c² ∝ r⁻⁴, not GM/rc². The 1/r potential dependence of the redshift is measured: Gravity Probe A at 7e-5 (Vessot et al. 1980), and the eccentric Galileo 5/6 satellites at 2.5e-5 (Delva et al., PRL 121, 231101 (2018)). G-RIVER instead inserts the Newtonian escape speed by hand. √(1−v_river²/c²) ≡ √(1−2GM/rc²) is then an algebraic identity, the Painlevé–Gullstrand / Hamilton–Lisle 'river model', not a medium result. A physical flow with v ∝ r^{-1/2} and a steady sink needs ρ ∝ r^{-3/2} (from ρvr² = const). That makes c² = B/ρ vary with r unless B ∝ ρ is imposed. Visser (CQG 15, 1767 (1998)) showed that an acoustic metric obeying continuity reproduces Schwarzschild only up to a conformal factor, which matters for clocks and for timelike orbits (β), though not for null rays. §18.6 derives only g_tt. Light bending and Shapiro delay (γ; Cassini γ−1 = (2.1±2.3)e-5) and perihelion (β) are not derived, yet §18.8 asserts them.

**Proposed improvement.** Either derive v(r) from the medium's own continuity and momentum equations (compressible, with a stated equation of state), show that it equals √(2GM/r), and compute the full acoustic metric including its conformal factor, checking PPN γ and β; or downgrade G-RIVER to '[H] kinematic identity given the choice v = v_esc'. Remove 'orbits, light bending, and gravitational waves … equals exact Schwarzschild' from §18.8 until γ and β are computed. State explicitly which velocity field advects light and which one clocks see.

### 5. [major] GR tests beyond the static clock rate (GW speed and polarization, binary-pulsar radiation, frame dragging) are absent, and the inviscid G→0 medium appears unable to pass them

- **category:** missing-test-or-prediction
- **location:** 18-time-and-gravity §18.8, §18.10; 10-implementing-speed-light-clock-free §10.9.1 (medium specification); sp-jamming-spine S2.3

**Quote.** §18.10: "negative & gravity sector observationally degenerate with GR (G-CAP-DEPART)" | §18.8: "the gravity sector yields \emph{no surviving prediction distinct from GR in accessible regimes}" | §10.9.1: "The medium is specified only by density ρ=1 (the sole inertial property), perfect elasticity, stiffness B=c², zero friction, and the void-forbidden (jammed-plenum) condition"

**Evidence.** 'Degenerate with GR' has been shown only for the static g_tt. A search of the whole physics volume finds no GW170817, polarization, quadrupole, binary pulsar, frame dragging, Lense–Thirring, Shapiro or perihelion. (1) GW speed: −3e-15 ≤ (v_GW − c)/c ≤ 7e-16 (Abbott et al., ApJL 848, L13 (2017)). The framework does not say what propagates a change in the sink field; the Poisson/Green-function inflow of §17.4.0 is instantaneous as written. (2) Polarization: a G→0, zero-friction medium carries only a compressional (scalar/breathing) mode. GW170814 favours pure tensor over pure scalar with a Bayes factor above 1000 (Abbott et al., PRL 119, 141101 (2017)). (3) Radiation reaction: the double pulsar confirms the GR quadrupole formula to 1.3e-4 (Kramer et al., PRX 11, 041050 (2021)); scalar-medium gravity generically adds monopole/dipole losses. (4) Frame dragging: a medium with zero friction and zero shear modulus cannot transmit torque from a rotating body. Gravity Probe B measured −37.2 ± 7.2 mas/yr (GR −39.2; Everitt et al., PRL 106, 221101 (2011)), which is 5.2σ from zero. §18.8 also uses black-hole ringdown (|ε_Ω| < 0.05) as a GR-consistency check, but ringdown is a Kerr (rotating) phenomenon that the river construction does not contain.

**Proposed improvement.** Replace 'observationally degenerate with GR' with 'degenerate in g_tt; other sectors [O]', and register explicit [O] items with their obstacles. GW speed: specify the propagation equation of the deficit field. Polarization: show a tensor mode exists in a G→0 medium, or record the conflict. Quadrupole: compute the energy loss of a binary sink pair. Frame dragging: provide a torque-transmission mechanism in an inviscid, shear-free medium (a Doran-type 'twisting river'). Each of these is a sharp, pre-registrable test that existing data can decide.

### 6. [major] EM sector: the Goldstone mechanism cannot produce a Coulomb force, E is given three incompatible identities, and the 'derived' charge conservation is vacuous

- **category:** physics-validity
- **location:** 14-force-lattice-tension-1-r2 §14.0.5, §14.0.6, §14.0.6b, §14.0.7; 15-quantum-mechanics-mapping-completion-note §15.4.3 (BN1); w0 scorecard 'source-free Maxwell contained'

**Quote.** §14.0.5: "Why long-range (unscreened): synchronization spontaneously breaks a global U(1) (the common phase), giving a massless Goldstone mode ⇒ infinite-range 1/r²." and "Sign rule: like sources ⇒ repel, opposite ⇒ attract (the electrostatic, positive-definite strain structure — not the relativistic-scalar convention)." | §14.0.6: "Identify mathbf E with the VP displacement field mathbf u. Its longitudinal part (∇·mathbf u, compression = deficit) is the static Coulomb field of §14.0.5" | §14.0.6b: "Taking the divergence and using ∇·(∇×mathbf B)=0 gives charge conservation as an identity" | §15.4.3: "(BN1) Target-text dynamical generators such as gauge fields, gauge symmetry, Lagrangians, and action integrals."

**Evidence.** (1) A Goldstone boson of a global U(1) has a shift symmetry and so couples only derivatively, through (∂_μθ)J^μ. For a conserved current this is a total derivative, so static conserved charges do not source it and there is no Coulomb potential. If the coupling is made non-derivative, the U(1) is explicitly broken, the mode is no longer massless, and spin-0 exchange makes like charges *attract*. Like-repel requires odd-spin (vector) exchange, which is exactly the gauge structure that BN1 bans; §14.0.5 imposes the sign by fiat. A Goldstone is also a single scalar mode, not two transverse polarizations. (2) E is identified three ways: as −∇φ of a phase field (§14.0.5), as the displacement u (a length, §14.0.6), and as −∂ₜu_T (a velocity, §14.0.6b). These are dimensionally and physically incompatible. (3) With E := −∂ₜu_T, ∇·E ≡ 0 identically. So ρ_q ∝ −∇·E ≡ 0, and 'charge conservation as an identity' reduces to 0 = 0. (4) Taking the displacement reading at face value: in linear isotropic elasticity a point compression source (centre of dilatation) has u = C r̂/r², so ∇·u = 0 outside the core. Its far field is pure shear with energy 8πGC²/r₀³ ∝ G, and two such sources in an infinite isotropic medium have zero interaction (Eshelby 1956). With the spine's G→0 the 'Coulomb field' carries no energy and no force. (5) With gauge structure banned there is no vector potential, so the Aharonov–Bohm phase for B = 0 outside a shielded solenoid (Tonomura et al., PRL 56, 792 (1986)) has no account. The [F] label on 'source-free Maxwell contained' certifies only the Riemann–Silberstein identity i∂ₜΨ = c∇×Ψ, which is true for any transverse field with speed c. It does not show that the medium has such a field (see the transverse-speed issue).

**Proposed improvement.** Fix one identification of (E, B, ρ_q, J) in terms of medium variables and derive Gauss's law ∇·E = ρ_q/ε₀ with ρ_q ≠ 0, Ampère–Maxwell and the Lorentz force from it. Then show that the propagating sector has exactly two transverse polarizations at speed c. Drop the 'global Goldstone ⇒ 1/r²' argument, or show explicitly how a static conserved charge sources the mode. Add the Aharonov–Bohm effect as a registered test. Downgrade the scorecard line 'source-free Maxwell contained' from [F] to [H] until the medium's transverse sector is exhibited.

### 7. [major] Stated departure 'γ→p⁺+e⁻ allowed' implies hydrogen annihilation p e⁻→γγ, which conflicts with proton and hydrogen stability and with collider data

- **category:** physics-validity
- **location:** 14-force-lattice-tension-1-r2 §14.0.4 ('Why electron and not antiproton'), §14.0.7

**Quote.** §14.0.7: "Baryon/lepton number not fundamental. γ→ p^++e^- is forbidden in the Standard Model (baryon and lepton number) but allowed here, since only charge/L_z is conserved." | §14.0.4: "the cheapest balancer is the bare electron (p+e^-≈ 938.8 MeV) rather than an antiproton (p+bar p≈ 1876 MeV)"

**Evidence.** If only charge/L_z is conserved, then under microscopic reversibility (CPT or detailed balance) a nonzero amplitude for γγ→p e⁻ implies a nonzero amplitude for p e⁻→γγ. A hydrogen atom (938.8 MeV) would then annihilate into two ~470 MeV photons. Nucleon-decay searches exclude GeV-scale electromagnetic final states at τ ≳ 1e33–1e34 yr (e.g. τ(p→e⁺π⁰) > 2.4e34 yr, Super-K, PRD 102, 112011 (2020)), about 24 orders of magnitude above the age of the universe. The volume's own energetic argument (the p e⁻ threshold at 0.94 GeV is below the p p̄ threshold at 1.88 GeV) predicts that γγ→p e⁻ should dominate proton production in two-photon collisions between 0.94 and 1.88 GeV. Two-photon measurements at e⁺e⁻ colliders see γγ→p p̄ from threshold (e.g. Belle, PLB 621, 41 (2005)) and no p e⁻ channel.

**Proposed improvement.** Either identify the conserved quantity in the model that forbids p e⁻→photons (for example, conservation of the 82-core count as an effective baryon number), which then also forbids γ→p e⁻ and removes the 'departure'; or compute the predicted p e⁻→γγ rate and compare it with Super-K limits. Remove the matter–antimatter 'potential payoff' until then.

### 8. [major] The event-count wavefunction is a local, single-field construction, so Bell violations and entanglement cannot be reproduced, and Bell's theorem is not discussed

- **category:** missing-test-or-prediction
- **location:** 15-quantum-mechanics-mapping-completion-note §15.1.2, §15.2.3, chapter header; 03-axioms-primitives-volume-particle-lattice [A-3]; 18-time-and-gravity §18.5 (fullness: no faster channel)

**Quote.** §15.1.2: "The definitions above are operational: they construct a state field directly from event-log aggregates and do not invoke axioms from any external theory." | §15.2.3: "It is an identity that holds equivalently by construction from the event-log definition" | [A-3]: "Locality: every change (rearrangement, relaxation, driving, transport) is expressed as a composition of local updates that depend only on the local neighborhood N(i) ([D-8])." | §18.5: "there is no faster channel because there is no void to bypass through" | header: "Collapse becomes a counting protocol with a Gate, not a mystery."

**Evidence.** ψ(n) = √ρ e^{iφ} is one complex number per lattice node, built from local event counts, with outcomes selected by local gates, local updates only [A-3] and a maximal signal speed c (§18.5). This is a local-realistic model, so Bell's theorem bounds it by CHSH |S| ≤ 2. Loophole-free experiments violate that bound: S = 2.42 ± 0.20 (Hensen et al., Nature 526, 682 (2015)), Giustina and Shalm (PRL 115, 250401/250402 (2015)), and S = 2.0747 ± 0.0033 (Storz et al., Nature 617, 265 (2023), about 22σ). Setting-choice correlations were pushed back 7.8 Gyr in the cosmic Bell test (Rauch et al., PRL 121, 080403 (2018)). In addition, a single field on physical space cannot represent an entangled N-particle state ψ(x₁,…,x_N) on configuration space (EPR pairs, the helium ground state). The Born rule is an identity by construction (|ψ|² ≡ ρ); its physical content, interference from linear superposition, rests on the assumed 'regime in which tick evolution is linear' (§15.1.5). 'Not a mystery' therefore overstates what is shown.

**Proposed improvement.** Register an explicit [O] item, 'Bell nonlocality / entanglement', with the obstacle stated: [A-3] plus the no-faster-channel rule imply a Bell-local model. State which escape the framework takes (explicit nonlocal lattice correlation, which conflicts with §18.5, or superdeterminism) and what that choice predicts for cosmic-Bell tests. Add a gate that runs a CHSH protocol on the event model (two separated detectors, independently drawn settings) and reports S. Rephrase the chapter tagline to a notation mapping.

### 9. [major] Spin-½, the electron g-factor and the running of α_em are neither derived nor registered as open items; a classical charged rotor gives g=1

- **category:** missing-test-or-prediction
- **location:** 15-quantum-mechanics-mapping-completion-note §15.3.5 (Lemma T-S1, H-S1); 14-force-lattice-tension-1-r2 §14.0.4, §14.5

**Quote.** §15.3.5: "what remains hypothesis (H-S1 proper, [H]{}) is (i) that physical one-quantum states are in this regime, and (ii) the identification of σ with the target-text spin-tfrac12 projection (magnitude ħ/2, the SU(2) double cover, the statistics link), which this lemma does not address." | §14.0.4: "charge | rotation sense at the universal near-c speed (structure-independent) | |qₑ|=|qₚ| exactly" | §14.5: "The electromagnetic coupling runs with energy (α⁻¹≈137 in the Thomson/IR limit, ≈128 at the Z scale)."

**Evidence.** The spin label σ = sgn ΔΦ is defined relative to one rotation sense tied to the global synchronisation axis. Real spin-½ gives ±ħ/2 along *every* axis, with sequential Stern–Gerlach statistics cos²(θ/2), and requires a 4π rotation to return to itself: neutron interferometry measured 704 ± 38° (Werner et al., PRL 35, 1053 (1975); Rauch et al. 1975). A Z₂ sign label cannot supply either property. The electron is modelled as a classical fast rotor whose charge is its rotation sense. A classical body with co-located mass and charge has gyromagnetic ratio g = 1, while g/2 = 1.00115965218059(13) is measured to 0.13 ppt (Fan et al., PRL 130, 071801 (2023)), and a_e = α/2π + … is the most precisely confirmed prediction in physics. The words 'g-factor', 'gyromagnetic' and 'anomalous moment' appear nowhere in the volume. The running of α is honestly used to reject numerology in §14.5, but no screening or vacuum-polarization mechanism is offered in the medium, and none is registered as [O].

**Proposed improvement.** Add [O] ledger entries with obstacles: (i) SU(2)/4π periodicity and arbitrary-axis spin statistics; (ii) the electron g = 2 and a_e(α); (iii) the scale dependence of α (the QED β-function, which a polarizable medium could in principle supply). A cheap first test is to compute the gyromagnetic ratio of the framework's own rotor electron. If it comes out as 1, record that as a falsification of the classical picture rather than leaving it unstated.

### 10. [major] Substrate model conflicts: the rigid-particle axiom versus the soft harmonic-contact verification, and a vanishing plane-wave window at the isostatic point

- **category:** physics-validity
- **location:** 03-axioms-primitives-volume-particle-lattice (VP-A1, [A-1], VP-A2); sp-jamming-spine S0, S2 heading, S2.4, S3; 10-implementing-speed-light-clock-free §10.1.5.1; 11-realization-units-t-rcross §11.6.5 (φ_jam=0.633); 18-time-and-gravity §18.5

**Quote.** [A-1]: "Non-overlap is not relaxed after seeing results; any configuration that violates it is judged inadmissible and cannot be used as an input for derivation/verification." | SP S2 heading: "Infinite stiffness→ c²: the single signal speed (verified)" | SP S2.4: "The result is the textbook isostatic-jamming scaling (O'Hern–Silbert–Liu–Nagel; Wyart; Olsson–Teitel) reproduced for the harmonic-contact substrate" and "ω^{*}∝Δ z→ 0(τ→∞)" and "B_{Born}staysO(1)throughout (0.90/1.13/1.40atN{=}256/512/1024)" | §11.6.5: "Jamming point | φ_jam=0.633"

**Evidence.** (1) The O'Hern harmonic model has energy (k/2)δ² for overlap δ > 0, so the verification substrate is made of overlapping soft spheres. Under the volume's own [A-1] those configurations are 'inadmissible … for derivation/verification'. For harmonic contacts, B just above φ_J scales as k_n/σ. In the Stone limit k→∞, B→∞ and c→∞; for truly rigid spheres the moduli are entropic (∝ k_BT) and vanish in the athermal limit. So 'infinite stiffness → finite c²' holds only for the soft model that the axioms forbid. (2) A medium with zero static shear modulus is a fluid in shear, not an 'elastic solid'. (3) In jammed packings, plane-wave-like modes exist only below ω* ∝ Δz; above it lies a plateau of anomalous, diffusive modes (Silbert–Liu–Nagel, PRL 95, 098301 (2005); Wyart–Nagel–Witten 2005; Vitelli et al., PRE 81, 021301 (2010)). The volume's own measurement ω*→0 shows that the ballistic window closes exactly at the operating point z = 2d. The vacuum instead propagates light dispersion-free from radio to PeV γ-rays. 'Linear dispersion verified R²≈0.99' is many orders of magnitude weaker than photon dispersion bounds. (4) c is *defined* as √(B_eff/ρ_eff) (§10.1.5.1), not measured as a propagation speed. (5) B_Born grows 1.40/0.90 = 1.56× from N = 256 to 1024, so it is not a converged material constant. (6) φ_jam = 0.633 leaves 36.7% of space outside the particles, which sits uneasily with full packing (VP-A2) and with '§18.5: no void to bypass through'.

**Proposed improvement.** Choose one contact law, state the physical contact stiffness, and reconcile it with VP-A1 (for example, relax the Stone axiom to 'stiff but finite'). Report the Ioffe–Regel crossover frequency against Δz, and state at what finite Δz the vacuum operates and what dispersion it implies. Measure a signal speed directly (a pulse time of flight in the packing) and compare it with √(B/ρ). Show B converging with N. State how the 36.7% interstitial volume is consistent with the full-packing axiom and the fullness theorem.

### 11. [major] The pre-registered light-angle falsifier (Kill-3, B1) is ill-posed: a mathematical overstatement, frame dependence, and a committed window that includes the standard-physics value

- **category:** math-error
- **location:** 10-implementing-speed-light-clock-free §10.9 (table, 'Falsifiable prediction'), §10.9.1, §10.9.2; 01-governance-no-tuning-lock-gate §1.10 Kill criterion 3; w0 scorecard row χ(633)

**Quote.** §10.9: "Near χ 90^(∘), cosχ is tiny, so χ is extremely sensitive to D: a 0.03% change in D shifts the visible-light angle by more than a degree." | table: "| Visible | 380–750nm | 89.8^(∘)–89.9^(∘) (near-transverse)" | Kill-3: "(χ(633)=89.9378^(∘), χ(532)=89.8248^(∘), with the D-distribution spread as the stated width)" and "This criterion is therefore "armed"" | header: "[F]+[V] light angle"

**Evidence.** Since sinχ = x/⌈x⌉ with x = λ/D, χ is a sawtooth in λ with period D = 4.853 pm, and it is confined to [arcsin((m−1)/m), 90°). At 633 nm that range is [89.7756°, 90°), a width of 0.2244°. Scanning D by ±0.03% gives χ between 89.7757° and 89.9977°, a maximum shift of 0.222°. 'More than a degree' is therefore impossible. At 380 nm, χ = 89.742°, outside the tabulated 89.8–89.9°. One sawtooth period is a fractional wavelength change of D/λ = 7.7e-6, which is a Doppler velocity of 2.3 km/s. Earth's orbital motion (29.8 km/s) sweeps λ/D through ~13 periods over a year, Earth's rotation (0.465 km/s) through 0.2 periods daily, and motion relative to the CMB through ~161 periods. The committed angles are therefore frame-dependent unless a preferred frame is named. The He-Ne Doppler gain width (~1.5 GHz, about 2.0 pm = 0.41 D) already spans a large part of one period. The volume's own input-rounding note shows the same hypersensitivity: 632.99 nm gives m = 130443 and χ = 89.9378°, while 632.99121 nm gives m = 130444 and χ = 89.7960°. The stated width is the 7% D distribution, which spans ~9,000 periods, so the committed window is the whole [89.776°, 90°) band. That band includes the Maxwell value of exactly 90° as its limit, so no near-transverse measurement can falsify it. G-ISO (the axis definition) is still open, so the header grade '[F]+[V]' and the label 'armed' are not supported.

**Proposed improvement.** Correct the '>1 degree' sentence (the maximum is about 0.22° at 633 nm) and the visible-band row. Relabel Kill-3 as 'not armed until G-ISO passes'. Reformulate the prediction as a frame-specified, Doppler-robust observable: for example, the predicted sidereal and annual modulation of a propagation anisotropy in a named frame. That observable could then be compared directly with existing cavity Michelson–Morley bounds (~1e-18), turning an untestable number into a sharp test.

### 12. [minor] Circular electron-mass 'result': m_e = 2hc/D with D defined as 2λ_C,e

- **category:** circularity
- **location:** 14-force-lattice-tension-1-r2 §14.0.4 ('Electron light'); sp-jamming-spine S1 table; 10-implementing-speed-light-clock-free §10.9.1

**Quote.** §14.0.4: "m_e=\frac{hc}{\lambda_{C,e}}=\frac{hc}{r_0}=\frac{2hc}{D}=0.5109\ \mathrm{MeV}\quad(\text{measured }0.51100;\ {-}0.03\%,\ \text{within the }D\text{ precision" | SP S1: "wavelength relationD=2πλ/A=2λ_{C,e}" | §10.9.1: "D_anch=4.852620477 pm"

**Evidence.** 2λ_C,e = 2 × 2.42631023867 pm = 4.85262047734 pm, while D_anch = 4.852620477 pm; the relative difference is −7e-11. With the canonical D, 2hc/D = 0.51099895 MeV, which equals m_ec² to 1e-10. The quoted '−0.03%' is just the truncation of 0.5109 (itself −0.019%). m_e goes in through D and comes back out, so this is not a prediction. The formula also writes a mass equal to an energy (hc/λ); it should read m_ec² = hc/λ_C.

**Proposed improvement.** Label the line 'consistency identity (D ≡ 2λ_C,e), not a derivation', remove the percentage agreement, and fix the units (m_ec² = hc/λ_C). Present m_e as a derived output only along a route where D comes from the jamming amplification A alone. Carry that route's actual 7% spread.

### 13. [minor] Cross-volume substrate error: 0.7405 is labelled 'random close packing' but is the FCC/Kepler density

- **category:** cross-volume
- **location:** AGENTS.md §1 TL;DR table and §6 catalog row 4 (chemistry headline); cf. physics 11-realization-units-t-rcross §11.6.5 and 18-time-and-gravity §18.8

**Quote.** AGENTS.md: "Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405)." and "`φ_RCP=0.7405`" | physics §11.6.5: "Jamming point | φ_jam=0.633, z→6 isostatic"

**Evidence.** π/(3√2) = 0.74048 is the FCC/HCP (Kepler) close-packing density. Random close packing of monodisperse spheres is about 0.64 (O'Hern et al. 2003: φ_J ≈ 0.639), which the physics volume itself uses (φ_jam = 0.633; §18.8 'φ_jam ≈ 0.64'). The corpus-level description of the root substrate therefore disagrees with the root volume, and it names a crystalline density for an explicitly amorphous (isostatic, z = 6) packing.

**Proposed improvement.** Correct the AGENTS.md/manifest wording and the chemistry headline to either 'RCP φ ≈ 0.64' or 'FCC close packing 0.7405'. If the chemistry volume really uses 0.7405, state why a crystalline density applies to an amorphous jammed vacuum.

**Strengths noted:**
- The α_em withdrawal in §14.5 is a model of honest grading. It concedes that the 4π is a unit artefact, that α runs (137 → 128), that many small-integer-and-π forms hit 137.036, and that direct lattice attempts gave O(0.1–0.7); α_em is recorded as [O] measured input.
- §18.3 and §18.8 state the preferred-frame (Lorentz-ether) status plainly and record a genuine negative: the gravity cap yields no prediction distinct from GR in accessible regimes. Many alternative frameworks hide exactly this.
- §10.9.2 (G-ISO) registers, before any claim, that the light-angle prediction must first reconcile with precision propagation data. That is the right instinct, and the fix above builds on it.
- The jamming statement itself (G_relaxed→0 with B finite at z=2d, via Maloney–Lemaître linear response, AQS and ω*) is textbook-correct, and it is cross-checked by five observables.
- The §14.0.6 isotropy lemma (ε_ijk is the only isotropic rank-3 tensor, so the curl is the unique first-order operator) and the Lemma T-S1 split between 'conditional theorem' and 'hypothesis' for the spin label are mathematically correct and carefully graded.
- vp_exact_sqrt.py correctly and reproducibly reconstructs the Lorentz–FitzGerald contraction from finite-c round trips (deterministic, sha256-gated). It only needs its hidden ℓ=1 premise surfaced.
- Operator testimony (the unreleased full-physics runs) is explicitly not counted as evidence (the 'v34 rule'), which is a strong governance practice.


## lens:repro-code

### 1. [critical] The 6π⁵ 'self-falsification' checks cannot fail, and they hide that 6π⁵ as an exact [F] identity is off by about 10⁶ σ

- **category:** missing-test-or-prediction
- **location:** docs/physics/01-governance-no-tuning-lock-gate/ §1.8.3 (5-line check + companion geometric-count check); docs/physics/axm-…, axp-…, axr-… (embedded verify code); docs/physics/w0-result-scorecard-one-page-summary/ (m_p/m_e row graded [F])

**Quote.** "Copy-pasted into a Python interpreter, this returns ALL PASS or an AssertionError pointing to the failed claim: if a reader's run prints anything other than ALL PASS, the framework is wrong" ; "assert abs(mp_me_measured/pi**5 - 6) < 2e-4" ; "assert [cnt(k) for k in (2,3,6,9)] == [19,27,81,123]" ; appendix code: "assert abs(r_p/8.412e-16 - 1) < 5e-4, \"canon r_p not reconciled to v0.4.1 (0.8412 fm)\"" ; scorecard: "| mₚ/mₑ = 6π⁵=2π· 3π⁴ (νₚ via LOCK-NU-N §8.0.5) | 1836.118 vs measured 1836.153 | [F]{} | -19ppm"

**Evidence.** I ran the companion check and it printed ALL PASS. Every assert except one is a fact of arithmetic: the value of 2/π, the value of 1/π², lattice-point counts, and the fact that six cube diagonals sum to zero. These pass on any conforming Python, whatever the physics. The one assert that depends on physics is mp_me/π⁵ − 6 = 1.129e-4, tested against a tolerance of 2e-4. That tolerance was evidently chosen after seeing the data (margin 1.77×). The five-line check only prints 6π⁵, 1/(5π) and D/(6π⁶), and printing a formula cannot reveal whether the formula was chosen to fit. Against CODATA 2022 m_p/m_e = 1836.152673426(32), 6π⁵ = 1836.118109 has a residual of −0.034565, which is −1.08×10⁶ σ. Graded [F] ('follows necessarily') with no declared theory uncertainty, the identity is excluded outright. The appendix r_p assert allows 500 ppm, 8× looser than the +61 ppm residual it claims to check.

**Proposed improvement.** 1. Replace the 'ALL PASS' scripts with a pre-registered test: publish the predicted value, a declared theory uncertainty (or the size and sign of the correction term the framework expects), and the pass/fail rule before comparing with data. 2. Grade 6π⁵ as '[F] leading-order form; exact value [O]' (or [L]), and state that as an exact identity it is excluded at ~10⁶ σ. 3. Delete the sentence 'if a reader's run prints anything other than ALL PASS, the framework is wrong', because the asserts cannot fail. 4. Tighten the r_p assert to the precision actually claimed.

### 2. [major] The 'second independent residual' R3 (+61.2 ppm) is R1 plus the rounding of the 0.8412 fm lock, so the ν_p 'length route [V]' is circular

- **category:** circularity
- **location:** repro/physics/tools/vp_numeric_ssot.py L74-76, L117-132; repro/physics/tools/gate.py phase4 L150-154; repro/physics/verification_dossier/NUMERIC_LEDGER.md (nu_p_length row); docs/physics/rf-read-first-what-this-is/ (residual note); docs/physics/06-continuum-core-model-deriving-rp/ §6.2; docs/physics/09-event-quantum-definition-canonical-event/ §9.4; docs/physics/13-mass-u-lat-m-h/ (length cross-check)

**Quote.** vp_numeric_ssot.py: "잔차 지도 — 독립 잔차는 단 2개(R1,R3); 나머지는 그 조합/부호반전" and ("R3","길이 ν_p vs 기하 3π⁴",f"{R3:+.2f} ppm","독립#2 (=r_p,pred/r_p,locked)") ; gate.py: "if abs(r3-_D(\"61.2\"))>_D(\"0.5\"): viol.append({\"ssot_residual_drift\":str(r3)})" ; rf: "the scattered −19/+19/+42/+61 ppm reduce to two independent residuals R1,R3." ; §6: "\lambda_C &=\frac{\pi}{2}\times 0.8412\ \mathrm{fm} \notag\\ &= 1.3213538700998668\ \mathrm{fm}" ; ledger: "| nu_p_length | (D/(2*r_p))*delta | 292.245156 | s^-1 | [V] | vs geometric 3pi^4: +61.2 ppm |"

**Evidence.** The framework's own r_p rule is r_p = (2/π)λ_C,p. With it, ν_len = D/(2r_p)·δ = 2λ_Ce/(2·(2/π)λ_Cp)/π² = (m_p/m_e)/(2π) identically. I checked this with Decimal at 50 digits. With the unrounded (2/π)λ_Cp = 0.84123564 fm, ν_len = 292.232774 = 1836.15267343/(2π), so R3 = +18.82 ppm, exactly −R1. The locked 0.8412 fm is 42.37 ppm below 0.84123564, and the half-ulp of a 4-significant-figure number is 59.4 ppm. The two effects combine: (1+18.82e-6)(1+42.37e-6)−1 = +61.20 ppm, which is the reported R3. R5 (+42.37 ppm, printed in §13 as '2πνₚ≈1836.23 (+42 ppm vs measured)') is therefore purely the rounding. §6 also shows λ_C = (π/2)×0.8412 fm = 1.32135387 fm, back-solved from the output. The measured CODATA λ_C,p is 1.32140986 fm, which differs by exactly −42.4 ppm. The gate enforces 61.2 ± 0.5 ppm, so it locks in a rounding artefact to 0.1 ppm. §9.4 and §1.9 A3 do say the length route is 'the same chain', which contradicts 'independent #2' and the [V] grade.

**Proposed improvement.** 1. State that there is one physical residual, R1 = −18.82 ppm. 2. Report the lock rounding separately as a precision note (−42.4 ppm, within its ±59 ppm half-ulp). 3. Regrade ν_p,length from [V] to 'algebraic identity (= measured m_p/m_e ÷ 2π)', and drop it from any list of independent confirmations. 4. In §6, substitute the CODATA λ_C,p. 5. Remove the gate.py 61.2-ppm check and the '+57 ppm' blacklist, or else lock r_p to ≥8 significant figures.

### 3. [major] The numeric drift gates are 4-literal blacklists and pass a page with fabricated values (tested)

- **category:** reproducibility-code
- **location:** repro/physics/tools/vp_numeric_ssot.py BAD_PATTERNS L137-142; repro/physics/tools/gate.py phase4; repro/physics/tools/vp_timegravity_ssot.py DRIFT_RULES L164-172; repro/physics/tools/vp_gravity_ssot.py check_dir L146-171; repro/physics/IRREPRODUCIBILITY_LEDGER.md §5

**Quote.** vp_numeric_ssot.py: "(b) 본문 표기값이 정준 재생성과 어긋나면 자동 탈락(FAIL)시킨다." ; IRREPRODUCIBILITY_LEDGER: "표시 드리프트 0 은 `gate.py --phase 4`(정본 HTML 대상)가 보장한다." ; vp_timegravity_ssot.py: "1836.118109, 5e-5, \"6*pi^5\")," ; vp_gravity_ssot.py: "txts=glob.glob(os.path.join(d,\"**\",\"*.txt\"),recursive=True)"

**Evidence.** In a scratch copy I wrote a page claiming '6π⁵ = 1836.153', 'm_H = U_lat/5π = 125.20 GeV', 'r_p = D/6π⁶ = 0.8499 fm', 'ν_p = 3π⁴ = 292.30', a free-air gradient of −0.3100 and a Pikes Peak TC of 35.00 mGal. The results were: `vp_numeric_ssot.py --check` → 'RESULT: PASS (0 drift class)'; `vp_timegravity_ssot.py --check` → 'DRIFT GATE: PASS'; `vp_gravity_ssot.py --check` → '[PASS]'. Three causes: (i) BAD_PATTERNS only rejects four historical typos ('+57 ppm', '292.244', '0.841248', '8.9875517923'). (ii) The 6π⁵ tolerance is 5e-5 (50 ppm), wider than the −19 ppm residual that is the headline, so a text that silently erases the residual still passes (rel 1.9e-5). (iii) vp_gravity_ssot scans only *.txt. On the canonical docs/physics it found 0 files and still printed '[PASS] … 0 txt 드리프트 없음'. Its EXPECT table (5186, 3388, 1798, 5.30, 3.6) and its 'forbidden' dict are never used.

**Proposed improvement.** 1. Build a positive registry of (symbol, regex that captures the displayed number, SSOT value, display precision). Every occurrence of a registered symbol in docs/**/index.html must round-match the SSOT to its displayed digits. 2. Set tolerances below the residuals being defended; for 6π⁵, match 1836.118 to 3 decimals. 3. Scan HTML, not .txt, and FAIL when the scan finds 0 files. 4. Add mutation tests to CI: inject known-wrong values and assert that the gate returns FAIL.

### 4. [major] Several 'gates' compare a quantity with itself and are then cited as verification (G-RIVER, TC identity, PASS-A/ASTRO, manifest counts, REL-MATCH)

- **category:** grading-honesty
- **location:** repro/physics/tools/vp_timegravity_ssot.py gate_river L83-92, gate_rel_match; repro/physics/tools/vp_cap_depart.py z_vp_geom; repro/physics/tools/tc_compute.py L33-43; repro/physics/tools/vp_gravity_ssot.py L89; repro/physics/tools/vp_inflow_competition.py PASS-A/ASTRO; repro/physics/tools/reconcile_derived_to_html.py docstring; docs/physics/18-time-and-gravity/ §18.6, §18.8, §18.10; docs/physics/w0-result-scorecard-one-page-summary/

**Quote.** "identical = (fr == fs)            # v_river^2 = 2GM/r  =>  1 - v_river^2/c^2 = 1 - 2GM/rc^2" ; §18.6: "vp_timegravity_ssot.py verifies \eqref{eq:phy-18-009} to machine precision for bodies from the Moon to a neutron-star surface" ; scorecard: "| Gravity time dilation = river √(1−2GM/rc²) | exact Schwarzschild, machine-exact to NS strong field | [F]{} |" ; tc_compute.py: "TCfw.append(tc/mGal)" with comment "프레임워크 유입항: 동일 1/r² 합 (정의상 동일) — 항등 확인용" ; vp_gravity_ssot.py: "v[\"tc_residual_vp_newton\"]=0.0   # 정의상 동일 1/r² 적분 → 항등" ; reconcile: "phase1/phase2 단어수·식수 검사는 by construction 통과한다"

**Evidence.** (1) G-RIVER defines v_river = sqrt(2GM/R) and then checks that sqrt(1−v_river²/c²) equals sqrt(1−2GM/Rc²). That is float equality of one expression written two ways. The code says so ('algebraic identity'), yet §18 says it 'verifies … to machine precision'. The scorecard grades it [F]; the script and time_gravity.gate.json grade it '[F?]'. (2) vp_cap_depart z_vp_geom ≡ z_gr, identical by the same substitution. (3) tc_compute appends the same `tc` to both the 'standard' and the 'framework' arrays, then prints 'max abs diff 0.00e+00 … 실측과 동일' (no measurement is involved). vp_gravity_ssot hardcodes the VP−Newton residual as 0.0, grades it [F], and gravity.gate.json records G-GRAV-TERRAIN PASS. (4) PASS-A (a common factor f cancels in ν_p/ν_e) and ASTRO (G cancels in g_Moon/g_Earth) are cancellations of the kind x·f/(y·f) = x/y. (5) reconcile_derived_to_html rewrites the manifest counts from the HTML, and phases 1 and 2 then compare the manifest with the same HTML. (6) REL-MATCH prints 'Earth … depart(lead vs exact)=0.000e+00 ~ x^2/2=2.423e-19'. Here x²/2 is below double-precision epsilon (2.2e-16), so the 0 is cancellation. The selftest `dep <= 1.0 * x**2` for Earth therefore passes vacuously.

**Proposed improvement.** 1. Move these into a 'unit tests / algebraic identities' section and remove them from the evidence and PASS tables. 2. Make the G-RIVER grade the same everywhere ([F?] or '[F] given the river premise'). 3. State that the physics lies in the premise (a static clock ticks at the local-medium kinematic rate, the Painlevé–Gullstrand 'river model' of Hamilton & Lisle 2008), not in the equality. 4. For REL-MATCH, compute the departure in the expansion variable x, e.g. with log1p or a series, or use mpmath, so that O(x²) is resolved for weak fields.

### 5. [major] The mass-rate identity 'm = 2πν' with ν_e = 1, applied to both particles, gives m_p/m_e = 3π⁴, not 6π⁵

- **category:** internal-inconsistency
- **location:** repro/physics/tools/vp_timegravity_ssot.py L48-50; repro/physics/tools/vp_exact_sqrt.py header; repro/physics/tools/vp_inflow_competition.py mp_me_under_common_f; docs/physics/18-time-and-gravity/ lock list (§18.1); docs/physics/13-mass-u-lat-m-h/ §13.5; docs/physics/17-extensions-optional-reading/ §17.4.0

**Quote.** vp_timegravity_ssot.py: "NU_E  = 1.0                      # electron canonical event rate, eq phy-12-014   [F]" and "MP_ME = 6.0 * math.pi**5         # = 2*pi*NU_P  (mass-rate identity m = 2*pi*nu)   [F]" ; vp_exact_sqrt.py: "the electron rate nu_e (hence mass m_e = 2*pi*nu_e) is ISOTROPIC" ; §18: "\nu_e:=1\ (\text{§12}),\qquad \nu_p=3\pi^4\ (\text{§8.0.5, LOCK-NU-N}),\qquad m=2\pi\,\nu\ (\text{§13.5})" ; §13: "\frac{m_p}{m_e} &= \frac{1}{\pi}\left(\frac{D_{\mathrm{anch}}}{r_p}\right) = \frac{1}{\pi}\bigl(2\pi^{2}\,\nu_{p,\mathrm{can}}\bigr) = 2\pi\,\nu_{p,\mathrm{can}}"

**Evidence.** Taking the stated locks literally: m_e = 2π·ν_e = 2π and m_p = 2π·3π⁴ = 6π⁵, so m_p/m_e = 3π⁴ = 292.227, not 1836.118. The 2π survives only if the electron's mass is ν_e without the 2π, which contradicts vp_exact_sqrt ('m_e = 2*pi*nu_e'). In the §13 derivation that actually does the work, ν_p is defined as D/(2π² r_p) = δ·D/(2r_p), a dimensionless ratio of lengths, and ν_e never appears. Elsewhere ν_p is '292.227 s⁻¹' and ν_e is '1 s⁻¹'. An event rate equal to a pure number in SI seconds depends on the SI second unless ν_e = 1 is declared to be the unit. That is an [H]+ claim in the scorecard ('Electron Tₑ≈ 1s | [H]+'), yet the code grades NU_E [F]. vp_inflow_competition computes m_p/m_e = 2π·(ν_p/ν_e), so its PASS-A check inherits the same ambiguity.

**Proposed improvement.** 1. Pick one bookkeeping and use it everywhere. Either (a) ν_p ≡ δ·D/(2r_p) is dimensionless and m_p/m_e = (α/δ)·ν_p, dropping 'm = 2πν' and ν_e from the lock list, or (b) m ∝ ν with one proportionality constant for both particles, in which case the 2π must come from somewhere stated. 2. Fix the code comments to match. 3. Grade ν_e = 1 s⁻¹ the same in code and scorecard ([H]+). 4. Label ν_p's unit as 'per electron tick', not s⁻¹.

### 6. [major] A_geo is circular: the 80-digit 'locked' A is exactly cΔt/a with Δt = 1.86e-21, and Δt is then 'derived' from A; the 0.16 % match cannot be reproduced

- **category:** circularity
- **location:** docs/physics/11-realization-units-t-rcross/ §11.3.1–11.3.4 and 'Measured-value robustness'; docs/physics/01-governance-no-tuning-lock-gate/ §1.9 A3; repro/physics/tools/vp_numeric_ssot.py L79, L111, L165

**Quote.** §11.3: "A = 880918.97770344000000074873389538365909152024492565003100802687690543842580063599." and "\boxed{ \Delta t = \frac{A\cdot a}{c_{\mathrm{ref}}} }" ; claim strip: "$cΔ t/a=A$ closes exactly." ; §11: "the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%" ; §1.9 A3: "Tₑ≈1 s ( +0.6%), and A_geo (0.16%) — five quantities" ; SSOT: "(\"A_geo\",\"cΔt/a\",f(q['A_geo'],4),\"[H] Δt 3 s.f. ⚠placeholder\")"

**Evidence.** Computing c·(1.86e-21 s)/a at 90 digits gives 880918.977703440000000748733895383659091520244925650031008026876905438425800635992…, which matches all 80 displayed digits of the 'locked' A. So A was produced from a Δt given to 3 significant figures, and then Δt = A·a/c is presented as the derived result: a round trip. The 3-s.f. Δt carries a ±0.27 % half-ulp, so 80 digits (and the ~0.16 % comparison) are finer than the input allows. The 0.16 % match does not follow from the published numbers. Scaling A_geo by (200/750)^(1/3) = 0.64366 gives 567,012. That differs from A_mean(750) = 5.69e5 by +0.35 %, and from A_med(750) = 4.76e5 by −16.1 %. The comparison also picks mean over median after the fact. w6 itself says A's magnitude 'scales as 1/g₀ … tracks a numerical/threshold scale'. verify_A_scaling.py, which is cited as the reproduction, is not in the repository. Even so, A_geo is counted as one of the 'surviving five' pieces of joint evidence.

**Proposed improvement.** 1. Remove A_geo from the joint-evidence count in §1.9 A3. 2. Show A = cΔt/a to 3 significant figures and label Δt as the input (or A, but not both). 3. If the A_sim ↔ A_geo comparison stays, pre-register g₀, the statistic (mean or median) and the N-scaling reference. 4. Ship verify_A_scaling.py together with the summaries it reads.

### 7. [major] IRREPRODUCIBILITY_LEDGER lists 2 items while ~40 cited simulation scripts are missing from the repo; it describes an [O]-audit gate that does not exist; SEED=19 does not apply to physics

- **category:** reproducibility-code
- **location:** repro/physics/IRREPRODUCIBILITY_LEDGER.md §1–5; docs/physics/w6-provenance-ledger-which-numbers-come/; docs/physics/w0-result-scorecard-one-page-summary/; docs/physics/11-realization-units-t-rcross/; repro/physics/tools/gate.py; AGENTS.md §5

**Quote.** Ledger: "패키지 내부의 결정론 재생성으로 **재현할 수 없는 정량**을 한 곳에 모은다" and "헌법 게이트(VP-SPEC 8장)는 ① 모든 `[O]` 항목이 본문에 사유를 가지는지, ② 본 원장이 그 항목·사유·위치를 빠짐없이 집계하는지를 정본 HTML 과 교차 확인한다." ; w6: "Items marked S are reproducible from AQD_DOI_bundle_unified_v0.4.0_2026-06-05.zip" ; w0: "| Ψ_yield=1.091×10⁻¹⁶ m⁻¹ | [O] | (intentionally no code)" and "| [O] | 08_gravity_mapping_attempt/, 10_column_engine/ (deterministic; sha256 gated)" ; AGENTS.md: "Reproducibility: deterministic builds, `SEED = 19`"

**Evidence.** The physics text names more than 40 distinct scripts. I searched the whole repository for 21 of them (lattice_3d_jam_percolation.py, soc_percolation_pinning.py, jamming_rotation_485pm_study.py, electron_one_second.py, full_gravity_sim.py, verify_appendix_P/R.py, 01_stiffness_to_c2/bulk.py, ellrot_verify.py, rcross_validate.py, validate_bundle.py, …) and found 0. The external Zenodo zip is named in the HTML but not pinned by sha256 anywhere in repro/ or registry/. So φ_jam = 0.633 (graded [V] in w0 but [F] in w6), A ≈ 8.0e5, D = 2πλ/A, the emergence of c, the SOC g*/g₀, Tₑ path (B), the m_q band and Ψ_yield cannot be regenerated from this package. By the ledger's own definition they belong in it. Also missing from the ledger are the [O] items full-vector contraction (§14.0.6), I-TIME-3 cosmological (1+z) and Ψ_yield. gate.py has phases 1, 2, 3/5/6, 4 and search, and none of them reads the ledger or audits [O] items; the repo-level tools/gate.py has no such check either. No physics tool uses randomness, so 'SEED = 19' is vacuous here. The stochastic runs (text: 'seeds 45–48', 'multi-seed') live only in the unpinned bundle. The ledger also calls Newtonian/GR ratios computed from NASA masses and G a VP 'reproduction' ('Moon→중성자별 전 구간 비율 … 결정론 재생성'), and lists the equivalence principle as reproduced, although no code computes it.

**Proposed improvement.** 1. Vendor the bundle into repro/physics, or pin it with DOI, file name, sha256 and a file manifest. 2. Add one ledger row for every S-item and every [O] item, each with its obstacle. 3. Implement the promised gate: parse every [O] on docs/physics/* and require a matching ledger row. 4. State that the physics tools are closed-form and seed-free, and record the actual seeds of the bundle runs.

### 8. [major] Committed gate reports cannot be regenerated and contradict their own scripts; the gravity pipeline reproduces a section that no longer exists

- **category:** reproducibility-code
- **location:** repro/physics/README_PHYSICS_DELIVERABLE.md §4; repro/physics/tools/gate.py read_manifest; repro/physics/reports/time_gravity.gate.json; repro/physics/reports/gravity.gate.json; repro/physics/verification_dossier/GRAVITY_REPRODUCIBILITY_MAP.md; repro/physics/CHANGELOG_v0_9_3.md, CHANGELOG_v0_10_0.md; repro/physics/tools/reconcile_derived_to_html.py; docs/physics/17-extensions-optional-reading/ §17.4.7

**Quote.** README: "python3 tools/gate.py --phase 1 --paper physics" ; gate.py: "return list(csv.DictReader(open(f\"manifest/{p}.csv\",encoding=\"utf-8\")))" ; time_gravity.gate.json: "\"A\": 58," / "\"B_per_A_MeV\": 8.784" and "\"verdict\": \"REGISTERED\"," "\"grade\": \"[VP] open prediction\"" ; CHANGELOG_v0_9_3: "**§17.4.7 (NEW)**: \"Spatial reproduction against measurement\" — free-air −0.3079 mGal/m (+0.24%)" ; CHANGELOG_v0_10_0: "**§17.4 본문·수식(phy-17-0xx)·수치 전부 verbatim 보존**" ; reconcile: "(예: §17.4 → §18 승격 후 잔존한 phy-17-085/086/087)"

**Evidence.** (1) The manifest/physics.csv file is absent from the repository. In a sandbox, gate.py phases 1, 2, 3 and search stop with a FileNotFoundError on manifest/physics.csv. inventory.py, which would regenerate it, needs the unshipped source TeX. The committed PASS reports therefore cannot be reproduced; only phase 4 runs. (2) time_gravity.gate.json records an iron peak of A=58, 8.784 MeV and cites INFLOW_COMPETITION_LEDGER.csv. The script whose sha matches (0b5aa2e3…) outputs '=> peak A=60, B/A=8.734 MeV', and A=58 is not on its grid. 58 / 8.784 only appears from a fine-grid scan that is not shipped. (3) The same JSON calls G-CAP-DEPART a 'REGISTERED … [VP] open prediction … falsifier'. vp_cap_depart.py and §18.8 conclude the opposite ('OBSERVATIONALLY NULL … no surviving prediction'), and vp_cap_depart.py is missing from module_sha256. (4) The current §17.4.7 is '### 17.4.7 Honest summary'. No physics page contains 'mGal', 'Pikes', '−0.3079' or '21.46', and §17 display equations end at phy-17-084. reconcile_derived_to_html.py deleted phy-17-085..087 as 'orphans'. That contradicts 'verbatim 보존', yet vp_gravity_ssot.py, tc_compute.py, the DEM, gravity.gate.json (PASS) and GRAVITY_REPRODUCIBILITY_MAP ('본 맵은 §17.4.7 본문 잔차표의 권위 출처다') still certify it.

**Proposed improvement.** 1. Ship manifest/physics.csv, or have gate.py derive what it needs from docs/. 2. Regenerate every *.gate.json with a script that writes it straight from module output; forbid hand-edited gate JSON and record the generator's sha in each report. 3. Restore the §17.4.7 spatial-reproduction content, or retire the gravity SSOT/DEM/gate as archival and say so in the CHANGELOG. 4. Make reconcile_derived_to_html.py report orphan SVGs instead of deleting them.

### 9. [major] Gravity SSOT and tc_compute: textbook Newtonian geodesy graded as VP [F]/[V], 'measured' baselines that are formulas, and unit and sign errors

- **category:** physics-validity
- **location:** repro/physics/tools/vp_gravity_ssot.py compute()/print_ledger L75-131; repro/physics/tools/tc_compute.py §[3] L45-60, §[4] L77-78; repro/physics/reports/gravity.gate.json

**Quote.** vp_gravity_ssot.py: "(\"free-air gradient\",\"-2·g0/R (mGal/m)\",     f\"{v['fa_grad']:.4f}\",\"[F]\")," ; "FA_STD   = -0.3086,          # 표준 자유공기 기울기 (mGal/m)" ; "v[\"g_moon\"]=C[\"G0\"]*(C[\"RHO_MOON\"]/C[\"RHO_E\"])*(C[\"R_MOON\"]/C[\"R_E\"])" ; tc_compute.py: "g_std =g_base+g_fa+g_bg+TC0" ; output: "자유공기(-0.3086·z) = -13.3 mGal  [VP: (R/(R+h))²]" and "Bouguer(+0.0419ρ·z) = +4.8 mGal  [VP: 유입원 밀도]"

**Evidence.** (1) −2g0/R, Ω²R, Somigliana, g ∝ ρR and the terrain integral are standard Newtonian formulas evaluated with measured G, ρ and R. None contains a VP quantity, so [F] ('forced by the substrate') overstates it. The honest label is 'consistency with Newton'. (2) −0.3086 mGal/m is the GRS80 normal-gravity theoretical gradient, not a measurement, so the 'R-FA +0.24% 외부' residual compares two Newtonian formulas. The 'oblateness' share is defined as total − centrifugal and then graded [F]. (3) The Moon: GM/R² = 4.9048695e12/1737.4e3² = 1.6249 m/s², while the code gives 1.6200, i.e. −0.30 %. The printed −0.01 % is against a 3-s.f. '1.62', and g0 = 9.80665 (a conventional value that includes rotation) is used instead of GM⊕/R⊕² = 9.8203. (4) tc_compute prints g_fa*1000 labelled 'mGal'. The true values are −0.3086×4300 = −1327 mGal and +0.1119×4300 = +481 mGal, so the labels are off by 100×. (5) Sign error: with complete Bouguer anomaly BA = g_obs − γ + 0.3086h − 0.1119h + TC, a zero-anomaly prediction is γ − 0.3086h + 0.1119h − TC. The code adds TC, an error of 2×21.46 = 42.9 mGal. The 'predicted absolute g 9.79243' also ignores isostatic compensation; Bouguer anomalies in the Front Range are roughly −200 mGal. (6) Line 77 computes cos_avg_local and line 78 overwrites it (dead code).

**Proposed improvement.** 1. Regrade the rows [N] (Newtonian reference, not a VP test) or [CAL]. 2. Label −0.3086 as 'GRS80 normal gradient'. 3. Use GM-based g for the Moon/Earth ratio and quote the residual against 1.625. 4. Fix the mGal labels (×1e5) and the TC sign in tc_compute. 5. Drop the 'predicted absolute g', or add an isostatic model and a measured station value with its uncertainty.

### 10. [major] The residual map has no uncertainties: m_H is a −4.6σ miss, the r_p baseline is stale, and anchor-dependent U_lat/m_H are graded [F]

- **category:** grading-honesty
- **location:** repro/physics/tools/vp_numeric_ssot.py MEAS L38, rows L100-102, residuals R6–R8; repro/physics/verification_dossier/numeric_ledger.json; docs/physics/13-mass-u-lat-m-h/ §13.3; docs/physics/11-realization-units-t-rcross/ §11.2; docs/physics/w0-result-scorecard-one-page-summary/

**Quote.** "MEAS = dict(MPME=D(\"1836.15267343\"), RP_CODATA=D(\"0.8414\"), MH_PDG=D(\"125.20\"))" ; "(\"U_lat\",\"hc/a (GeV)\",f(q['U_lat'],6),\"[F]\")," ; §13: "The PDG-tabulated Higgs boson mass is m_H^exp=125.20± 0.11GeV (CODATA/PDG 2024)." ; §11.2: "N = 10^{12}." and "a := \frac{\lambda_{\mathrm{ref}}}{N}." ; numeric_ledger.json: "\"symbol\": \"m_H\", … \"grade\": \"F\""

**Evidence.** m_H = 124.694926 GeV against 125.20 ± 0.11 is (124.695−125.20)/0.11 = −4.59σ. It is reported everywhere only as '−0.40 %' and listed next to −19 ppm as a 'small residual'. r_p: the SSOT uses CODATA 2018 0.8414(19). With CODATA 2022 r_p = 0.84075(64) fm, R6 goes from −0.0177 % to +0.0596 % (+0.78σ; muonic-H 0.84087(39): +0.98σ). The sign flips, although the conclusion (consistent) holds. U_lat = hc/a with a = λ_ref/N, where λ_ref = 632.99121258 nm (the I₂-stabilised He-Ne standard) and N = 10¹² is a locked decimal power. U_lat and m_H therefore scale as N/λ_ref, meaning they depend on a laboratory laser line and a choice of SI decimal. They are anchor-dependent ([L]/[H] in the framework's own vocabulary), not [F]. The grade of m_H is 'F' in numeric_ledger.json, '[F_geo/H]' in the SSOT and '[F]/[H]' in the HTML.

**Proposed improvement.** 1. Add uncertainties to MEAS and print the pull (σ) next to every % and ppm residual. 2. Record m_H = U_lat/5π as a failed or [O] closure at 4.6σ unless a theory-uncertainty model is declared. 3. Update the r_p baseline to CODATA 2022, keeping 2018 as history. 4. Grade U_lat and m_H as [L] (anchored on λ_ref and N) everywhere, and state why N = 10¹² is not a free choice (or count it as a second DOF).

### 11. [major] The φ ≈ 0.7405 'random close packing' label on the corpus front page contradicts the root volume's φ_jam ≈ 0.633–0.64

- **category:** cross-volume
- **location:** AGENTS.md §1 TL;DR and §6 catalog row 4; docs/index.html (chemistry card); docs/chemistry/02-chemistry-single-anchor/; docs/physics/11-realization-units-t-rcross/ (measured-values table); repro/physics/tools/vp_cap_depart.py L3 verdict; repro/physics/tools/build_search_layer.py gen_llms

**Quote.** AGENTS.md: "| What is the substrate? | Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405). Light is its elastic wave: `c² = B/ρ`. |" ; homepage: "φ_RCP = 0.7405" ; chemistry: "Crystal packing fractions are pure geometry: FCC/HCP π/(3√2) = 0.7405" ; physics §11: "| Jamming point | φ_jam=0.633, z→6 isostatic, K=2.05×10⁴ | lattice_3d_jam_percolation.py" ; vp_cap_depart.py: "(z=6, phi_jam~0.64)" ; build_search_layer.py: "modeled as a jammed, infinitely-rigid granular lattice (random close packing), so the speed of light is the lattice elastic-wave speed c² = B/ρ"

**Evidence.** π/(3√2) = 0.740480 is the Kepler FCC/HCP crystalline maximum, not random close packing. RCP and the isostatic jamming point used by the physics volume are about 0.64 (φ_jam = 0.633 from its own simulation). The corpus-level description of the root substrate is therefore wrong by 17 % and mislabels a crystalline constant as RCP. The chemistry body itself correctly calls 0.7405 FCC/HCP. Separately, the generated llms/hub text says the constituents are 'infinitely rigid' and also that c² = B/ρ is finite. With B → ∞, c → ∞ unless ρ also diverges. The text (§1.9 A1) instead invokes an 'unbounded-stiffness postulate' whose c_env = √K is finite, and that reconciliation is never stated where the claim is made.

**Proposed improvement.** 1. Change AGENTS.md, the homepage card and vp.manifest to 'φ_jam ≈ 0.64 (RCP / isostatic, physics §11)'. 2. Where 0.7405 is quoted (chemistry crystals), call it 'FCC/HCP π/(3√2)'. 3. Reword 'infinitely rigid' to match the stiffness postulate actually used (finite K per unit ρ), or add one sentence explaining how infinite rigidity yields finite c.

### 12. [minor] G-EXACT-SQRT: the κ-scan is a light clock re-solving an algebraic condition, not a derivation 'without relativity'

- **category:** grading-honesty
- **location:** repro/physics/tools/vp_exact_sqrt.py header + main(); repro/physics/reports/time_gravity.gate.json G-EXACT-SQRT; docs/physics/18-time-and-gravity/ §18.2–18.3, §18.10; docs/physics/w0-result-scorecard-one-page-summary/

**Quote.** gate JSON: "κ=sqrt(1-v^2/c^2) is the unique anisotropy-zeroing contraction (no relativity, no light-clock)" ; script: "the contraction is NOT assumed; it is the unique minimizer, recovered to ~1e-6." ; "T(theta; kappa, v) = 2L * sqrt( kappa^2 c^2 cos^2(theta) + (c^2 - v^2) sin^2(theta) ) / (c^2 - v^2)" ; scorecard: "| Exact factor √(1−v²/c²) (value) | forced by finite-c closure + electron-rate isotropy | [F]{} |"

**Evidence.** T(θ) is the round-trip time of a c-signal over an arm of proper length L, i.e. a light clock, and 'rate = T0/T' defines the clock's tick as that round trip. Isotropy requires κ²c² = c² − v², which is solvable by hand. The golden-section search only re-finds the root; the output shows anisotropy 4e-16 at κ_forced, so 'found, not assumed' adds no evidence. The physics sits in two premises: (P1) the electron clock is a c-closure and (P2) its rate is isotropic when moving. P2 is the relativity principle for that clock. The Kennedy–Thorndike logic shows that contraction alone does not dilate clocks that are not c-round-trips, so the result's scope is conditional on P1.

**Proposed improvement.** 1. Grade the result '[F | P1, P2]' with both premises spelled out, or [H]. 2. Drop 'no relativity, no light-clock' and 'NOT assumed'. 3. Keep the scan as a unit test of the algebra.

### 13. [minor] The page-grade generator breaks ties optimistically, so §14 (coupling [O]) is published as 'Grade [F] forced'

- **category:** grading-honesty
- **location:** repro/physics/tools/derive_meta.py page_grade L156-165; docs/physics/14-force-lattice-tension-1-r2/ (answer-first paragraph); also 10-…, 11-…

**Quote.** "GRADE_PRIORITY = \"FVHO\"" ; "best = sorted(cnt, key=lambda g: (-cnt[g], GRADE_PRIORITY.index(g)))[0]" ; §14 answer: "Charge is the bookkeeping of one synchronized rotation; the coupling size is honestly measured. … Grade [F] forced."

**Evidence.** The page grade is the most frequent claim-strip grade, and ties resolve F > V > H > O. Recomputing on docs/physics gives: §14 {F:1, O:1} → 'F'; §11 {F:1, H:1, V:1} → 'F'; §10 {F:1, V:1} → 'F'. §14's load-bearing quantitative content (α_em, the coupling magnitude) is [O], yet the machine-generated answer-first text and JSON-LD headline it as 'forced'.

**Proposed improvement.** Use weakest-link aggregation (the page grade is the weakest grade among its claim strips), or publish the grade mix, e.g. '[F]×1 · [O]×1'.

### 14. [minor] The 'drift fix' for k_e bans the CODATA 2018 value and installs the pre-2019 exact c²·10⁻⁷, mislabelled as measured

- **category:** unit-dimension
- **location:** repro/physics/tools/vp_numeric_ssot.py L78, L110, BAD_PATTERNS L141; repro/physics/tools/gate.py phase4 (b); docs/physics/14-force-lattice-tension-1-r2/ eq S14_02_ke_e_values

**Quote.** "(r\"8\\.9875517923\",                                     \"8.9875517923e9\",\"8.9875517874e9\",\"c²·1e-7 = 8987551787.37\")," ; "(\"k_e\",\"c²·1e-7\",f(q['k_e'],4),\"[측정상수]\")," ; §14: "k_{e}=8.9875517874\times 10^{9}\ \mathrm{N\cdot m^{2}/C^{2}}"

**Evidence.** Since the 2019 SI revision μ₀ (hence k_e) is measured. From ε₀: CODATA 2018 gives 1/(4πε₀) = 8.9875517923(14)e9 and CODATA 2022 gives 8.9875517862(14)e9. c²·1e-7 = 8.98755178737e9 is the obsolete exact value. It sits 3.5σ from CODATA 2018 and 0.86σ from 2022. The gate treats the correct 2018 value as 'drift', and the SSOT labels a definition-derived number '[측정상수]'. The numerical impact is tiny (≈5e-10), but the gate enforces an incorrect provenance.

**Proposed improvement.** Take k_e from CODATA 2022 (8.9875517862(14)e9) with its uncertainty, remove the blacklist entry, and label the value 'CODATA 2022 (measured since 2019 SI)'.

### 15. [minor] Housekeeping: duplicated and divergent ledgers, a mislabelled backup, three different tool fingerprints, stale reports

- **category:** structure-redundancy
- **location:** repro/physics/reports/ vs repro/physics/verification_dossier/; repro/physics/tools/.r6_backup/; repro/physics/*.csv, tools/*.csv, reports/*.csv; repro/physics/CHANGELOG_v0_11_0.md; repro/physics/reports/STATUS_physics.md; repro/physics/REMOVAL_REPORT.md; repro/physics/verification_dossier/NUMERIC_LEDGER.md; repro/physics/tools/vp_gravity_ssot.py dem_sha256

**Quote.** CHANGELOG_v0_11_0: "- r6 백업: `tools/.r6_backup/`(derive_meta·gate 의 r6 원본)." and "- 도구 지문 tools_sha16: `7d2cedb4a2e553ba`(r7 도구 반영)." ; STATUS_physics.md: "- 표준 기계: **r6** (tools_sha16 = f637878baee1d719)." ; NUMERIC_LEDGER.md: "(기계 산출: `remediation/numeric_ledger.json`)" ; REMOVAL_REPORT: "**46개 섹션**" and "번호장이 §17에서 끝남(§18 없음)."

**Evidence.** (1) Ten files are byte-identical in reports/ and verification_dossier/. NUMERIC_LEDGER.md exists in both and differs: the reports/ copy lacks the r_e row, so there are two 'single sources of truth'. (2) The four ledger CSVs are triplicated (tools/, reports/, root). (3) .r6_backup/gate.r6_then_r7.py.bak is byte-identical to the current r7 gate.py, so it is not an r6 backup. (4) tools_sha16 appears as 45a66283fb91acdc in the phase reports (it matches the current tools, as I recomputed), 7d2cedb4a2e553ba in CHANGELOG_v0_11_0 and f637878baee1d719 in STATUS. (5) The remediation/ path does not exist. (6) REMOVAL_REPORT says '46 sections, no §18', but §18 now exists (47 chapters). (7) vp_gravity_ssot computes the DEM sha256 but never compares it with the pinned bbe98730… value, so the claimed 'sha256 고정' is not enforced. (8) The scripts write CSVs into the current working directory, so running them from the repo root litters it. (9) The '2×sha256' determinism check hashes the same pure function twice in one process. On the plus side, my independent re-run reproduced all four CSVs byte-for-byte against the committed hashes.

**Proposed improvement.** 1. Keep one dossier directory and delete or symlink the other. 2. Generate NUMERIC_LEDGER.md from numeric_ledger.json. 3. Delete .r6_backup, since git history is the backup. 4. Emit tools_sha16 into every report automatically and drop hand-written fingerprints. 5. Assert the DEM sha against the pinned value. 6. Write outputs to an explicit --out directory. 7. Replace the in-process double hash with a comparison against committed hashes (as time_gravity.gate.json does). 8. Mark REMOVAL_REPORT as historical.

**Strengths noted:**
- The four standard-library ledger scripts (vp_timegravity_ssot, vp_exact_sqrt, vp_cap_depart, vp_inflow_competition) ran cleanly. Each reproduced its committed CSV byte-for-byte, and the output hashes match the module_sha256 entries in time_gravity.gate.json.
- vp_cap_depart.py is a genuinely adversarial test. It checks the cap against NICER PSR J0740 and ringdown data, and it records an honest negative: the gravity sector is degenerate with GR, and the surviving α window conflicts with marginal-isostatic jamming. §18.8 reports this plainly.
- The α_em closed form 4π(11−…) = 137.0364 is explicitly demoted to 'coincidence / non-evidence' and kept out of the evidence count. Residuals are published rather than tuned away (5π is not moved to 4.98π).
- vp_numeric_ssot.py computes at 60-digit Decimal precision, never rounds intermediates, and labels every residual with its baseline. That is a good basis for a real display-drift gate once the check is made positive and not a blacklist.
- The w6 'honest-reading notes' state candidly that the size of A tracks the threshold g₀ (A ∝ 1/g₀) and that D = 2πλ/A is a central-tendency match, not a parameter-free derivation.
- The DEM input for the terrain computation is frozen as .npy with a recorded sha256 and a fetch script, which is good practice for external-data reproducibility.


## lens:cross-volume-and-rendering

### 1. [critical] The root volume does not contain the R19 kernel it is credited with owning

- **category:** cross-volume
- **location:** docs/physics/_decl.json (adds, primitives); docs/physics/index.html (hub 'Defines' strip); registry/vp.manifest.json (physics row, primitives.R19); registry/concepts.json (r19_switch, spinodal, barrier, phi_rcp, stiffness_shell, jammed_substrate); registry/modules.json (kernel, light_emergence); AGENTS.md §3.3; docs/index.html (architecture box); all 47 docs/physics/*/index.html

**Quote.** _decl.json: "adds": ["jammed-substrate", "c2=B/rho", "R19-normal-form", "constants:mp/me=6pi^5"], "primitives": ["emergence", "jammed_c2"] | hub: <span class="lbl">Defines:</span><a href="/modules/#kernel">R19 switch</a> | concepts.json: "id": "r19_switch", "symbol": "ṡ = g·s − s³ + h", "grade": "F", "owner": "physics", "href": "/physics/03-axioms-primitives-volume-particle-lattice/", "loc": "§3" | modules.json light_emergence: "a single photon is one R19 flip" | AGENTS.md: "| physics | — (root) | jammed substrate, `c²=B/ρ`, R19 normal form, constants |" | homepage: "Vacuum substrate — VP Theory c² = B/ρ · R19 bistable switch"

**Evidence.** grep over all 47 chapter texts and HTML for R19, bistab, double-well, s^3/s³, 'normal form', spinodal: zero hits in any chapter; the single hit for 'R19' in docs/physics is the hub's auto-generated 'Defines' link. §3 (the r19_switch canonical href) contains no cubic, no g, no h, no s. The manifest's own scanner (tools/make_manifest.py, pattern 'R19|bistable') leaves physics OUT of primitives.R19.volumes (25 volumes, physics absent), so the same file says physics 'adds R19-normal-form' and 'does not carry R19'. Of 20 concepts with owner=physics, 5 have canonical hrefs in other volumes (spinodal and barrier -> /dna/how-to-read-a-locus/, phi_rcp -> /chemistry/02..., stiffness_shell -> /fluid-dynamics/ax-j..., annihilation -> /cosmology/01...), and 2 (r19_switch, jammed_substrate 'φ ≈ 0.7405') point into physics §3 where the stated symbol does not appear. The cubic ṡ = g s − s³ + h appears first in digestive, ear, mind, eye, neuro, nose, inheritance, homeostasis_ionic; not even dna writes it out. Conversely physics is counted in the 'Emergence from measured γ 29/32' bar only because the pattern is 'emerge|emergence|emerges' (24 word hits in physics), although γ = −mean NN stacking ΔG, 'stacking', 'SantaLucia' and 'promoter' occur 0 times in physics. The root node of the inheritance DAG that every biology volume cites for its kernel therefore does not contain that kernel; physics' seams.json 'cited_by' still lists dna and neuro as '[F] derives_from' physics.

**Proposed improvement.** Either (a) add a physics chapter (or a §3 subsection) that actually derives the double-well normal form from the stiffness-shell barrier already present in §15 ('rigidity-shell barrier') and Appendix H (Boltzmann escape over U_barrier), states g, h, s physically, derives spinodal h* = 2(g/3)^{3/2} and barrier g²/4, and grades each step honestly (at present it could only be [H]); or (b) move ownership of r19_switch/spinodal/barrier to the volume that first derives them, delete 'R19-normal-form' from physics.adds and the hub 'Defines: R19 switch' strip, and redraw the DAG so R19 enters at that volume. Replace keyword-count primitives with explicit per-volume declarations checked by a gate that fails when a declared canonical href does not contain the symbol.

### 2. [critical] Light is declared the sole surviving LONGITUDINAL mode (G→0) yet also a TRANSVERSE helicity-±1 wave

- **category:** internal-inconsistency
- **location:** docs/physics/sp-jamming-spine-verified-physical-backbone (S2.3); docs/physics/11-realization-units-t-rcross (§11.6.1); docs/physics/14-force-lattice-tension-1-r2 (§14.0); docs/physics/10-implementing-speed-light-clock-free (§10.9); registry/modules.json (light_emergence); docs/chemistry/01-electromagnetism-jammed-lattice-light and 02-chemistry-single-anchor

**Quote.** SP: "The transverse wave dies; one longitudinal speed survives" | §14: "its transverse, propagating part is light — the transverse oscillation of rotating quanta" | §14: "photons carry helicity ±1 (circular polarization = a rotating field)" | §10.9: "short wavelengths (gamma) span m=1 and run nearly along the lattice axis (χ→0^(∘))" | modules.json: "Light is the lattice's single surviving longitudinal elastic wave (c² = B/ρ, shear modulus → 0)" | chemistry §1: "leaving one longitudinal wave, light, at c² = B/ρ" vs chemistry §2: "light is the rotational transverse wave (Chapter EM)"

**Evidence.** In an isotropic elastic solid c_L² = (B + 4G/3)/ρ and c_T² = G/ρ. The spine's verified result is G_relaxed → 0 at z = 2d = 6, which gives c_L² → B/ρ (the headline) and c_T → 0: no transverse elastic wave propagates. But light has two transverse polarizations and helicity ±1 — which §14 itself asserts — and a longitudinal mode carries helicity 0. §10.9 then makes gamma rays near-longitudinal (χ→0°), contradicting the helicity ±1 of gamma photons (measured by Compton polarimetry) and ∇·E = 0 in vacuum. So the headline 'c² = B/ρ: the speed of light is the lattice elastic-wave speed' identifies c with the speed of a mode that has the wrong polarization, while the chapter that needs transverse light (§14) relies on a mode the spine says 'dies'. The inconsistency propagates verbatim to modules.json and chemistry, and chemistry contradicts itself between §1 and §2.

**Proposed improvement.** State explicitly which mode light is. If transverse, the medium must be micropolar/Cosserat (rotational degrees of freedom of the 'rotating quanta') and c must be derived from a rotational/couple-stress modulus, not B; derive that and re-run the five-observable test for the rotational modulus. If longitudinal, confront it with photon helicity ±1, the absence of longitudinal polarization, and gamma-ray polarimetry, and downgrade c² = B/ρ-as-light to [H]/[O]. Until then change the SP/§11 grade from [V] to [H] for 'light = the surviving mode' (the [V] applies only to G_relaxed → 0), and make modules.json and chemistry §1/§2 use one consistent statement.

### 3. [major] Aggregates give the vacuum packing fraction as 0.7405 (FCC/Kepler); the physics volume uses φ_jam ≈ 0.633–0.64 (RCP)

- **category:** cross-volume
- **location:** AGENTS.md §1 TL;DR and §3.3/§6 (chemistry row); registry/vp.manifest.json framework.kernel.substrate and primitives.jammed_c2.pattern; registry/concepts.json phi_rcp and jammed_substrate; docs/index.html (chemistry card); vs docs/physics/rf-read-first-what-this-is, w0-result-scorecard-one-page-summary, 11-realization-units-t-rcross; docs/chemistry/02-chemistry-single-anchor

**Quote.** AGENTS.md: "| What is the substrate? | Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405). Light is its elastic wave: `c² = B/ρ`. |" | manifest: "substrate": "c^2 = B/rho (vacuum = jammed elastic solid, phi~0.7405)" | concepts.json phi_rcp: "symbol": "φ_RCP = 0.7405" ... "statement": "Packing fraction of the vacuum substrate (random close packing).", "disambig": "DISTINCT from φ_jam = 0.840 (2D jamming onset) and φ_iso = 0.633 (isostatic z→6)." | physics RF: "settles on its own to φ_jam≈0.64 (random close packing)" | W0: "φ_jam = 0.633 — Isostatic jamming/packing fraction (z to 6)" | chemistry: "FCC/HCP π/(3√2) = 0.7405, BCC 0.6802, SC 0.5236"

**Evidence.** π/(3√2) = 0.740480 is the Kepler/FCC/HCP maximum (crystalline) packing density; 3D monodisperse random close packing is ≈0.64 (O'Hern et al. 2003: φ_J ≈ 0.639). Physics measures φ_jam = 0.633 (§11 table, W0) and the RF quick-check prints 'phi_jam = 0.626 [RCP 0.64]'. Chemistry uses 0.7405 correctly, for crystal packing of atoms in metals, not for the vacuum. The registry turned chemistry's crystal number into the vacuum substrate's 'RCP', assigned it to physics (owner=physics, grade F), renamed the physics φ_jam to 'φ_iso', and made up 'φ_jam = 0.840' (a 2D disk value that appears nowhere in physics). The manifest's jammed_c2 scanner also keys on the literal '0\.7405'. An AI following AGENTS.md ('read it first') will learn the wrong substrate density.

**Proposed improvement.** Change AGENTS.md §1, manifest kernel.substrate and concepts jammed_substrate to 'random close packing, φ_jam ≈ 0.633 (isostatic z → 6; simulation, [V])'. Delete concept phi_rcp, or rename it 'φ_FCC = π/(3√2) = 0.7405 (crystal packing; chemistry)' with owner=chemistry. Remove the fictitious 'φ_jam = 0.840' disambiguation. Change the chemistry headline/adds 'φ_RCP = 0.7405' to 'φ_FCC'. Drop '0\.7405' from the jammed_c2 pattern.

### 4. [major] Grade tallies published for physics disagree with each other and with the text, and the homepage hides all [V]/[O] items

- **category:** grading-honesty
- **location:** docs/physics/_decl.json grades; registry/vp.manifest.json physics.grades; docs/index.html physics card; docs/physics/index.html (hub overview line); docs/physics/_meta.json; docs/llms.txt; registry/modules.json kernel.reach; AGENTS.md §4 vs §7

**Quote.** _decl.json/manifest: "grades": {"forced": 26, "verified": 0, "open": 0, "hypothesis": 2} | homepage: "VP Theory c² = B/ρ ; mₚ/mₑ = 6π⁵ (−19 ppm) jammed lattice c²=B/ρ 6π⁵ 26 forced" | hub: "Claim ledger across graded sections: 12 forced, 1 hypothesis" and "49 chapters · 8005 equations · 51 tables · 138713 source words" | llms.txt: "projected across 30 open-access volumes" | modules.json: "All 30 volumes inherit this object: 23/30 carry R19 explicitly, 27/30 emerge from it."

**Evidence.** Counting graded tags in the visible text of the 47 physics chapters (vp-cards excluded) gives [F] 142, [H] 68, [V] 35, [O] 31 (plus [F?], [C]). Page-level badges: 13 forced + 1 hypothesis, since §18's _meta 'no' is the integer 18 rather than a string, which probably explains the hub's 12. The registry/homepage figure 'verified 0, open 0' removes exactly the grades that qualify physics: c² = B/ρ [V], φ_jam [V], α_em [O], absolute g [O], Coulomb K_C [O]. Hub statistics are stale: _meta.json gives 47 chapters (not 49), 6463+1272 = 7735 equations (not 8005), 48 tables (not 51), 135,133 words (not 138,713), even though the hub states 'this overview is generated deterministically'. Other aggregate counts disagree too: llms.txt says 30 volumes while listing 32; modules.json says 23/30 and 27/30 while the homepage says 25/32 and 29/32; the AGENTS §7 manifest example has R19 24 / gamma 25 while the §4 table has R19 25 / γ 24.

**Proposed improvement.** Generate _decl.grades from the same tag scan the hub uses, report all four classes (F/V/H/O) on the homepage card, and add a gate that fails when hub, _decl, manifest and homepage disagree. Cast _meta 'no' to string and rebuild the hub stats. Regenerate llms.txt, modules.json 'reach' and the AGENTS §7 example from the manifest, as AGENTS §9 rule 4 already requires.

### 5. [major] Four incompatible grade vocabularies, and the same quantity carries different grades on different surfaces

- **category:** grading-honesty
- **location:** AGENTS.md §5; docs/physics/w0-result-scorecard-one-page-summary (legend, cards, table); docs/physics/w6-provenance-ledger-which-numbers-come; physics abstract (docs/physics/_meta.json, hub); docs/physics/15-quantum-mechanics-mapping-completion-note; docs/physics/17-extensions-optional-reading (Result 2/7); registry/concepts.json (lambda_anchor, D_quantum, electron_second, seed19, double_sha256); repro/physics/site_seed/grade_vocab_physics.csv

**Quote.** AGENTS.md: "`[L]` anchored / locked — rests on a single declared empirical anchor" | W0 legend: "[H]{} = derived structure, coefficient closed under the single anchor;" vs hub "precedence forced > verified > hypothesis > open" and grade_vocab "[H],11,g-hypothesis" | abstract: "Forced (...), Calibrated (dimension-bearing values carrying a single empirical length anchor, λ_ref=632.99 nm ...), and Open" | §15: "with h_VP calibrated to data; grade CALIB" | card: "λ_anchor = 632.99 nm — Single empirical anchor (DOF = 1); the only measured length input to the framework. [F] forced." | W0: "φ_jam = 0.633 — ... [V] verified." vs W6: "Jamming packing φ_jam≈0.63 (zero physical constants in input) | lattice_3d_jam_percolation.py → real3d_run_summary.json | [F]" | card: "g* = c²·Ψ_yield — Gravity-cap mechanism ... [F] forced." vs §17: "Ψ_yield=g_(*)/c²"

**Evidence.** AGENTS defines F/V/L/O. Physics never uses [L] and instead uses [F], [H], [V], [O], [F?], [H]+, [INPUT], CALIB, 'Calibrated', 'negative' and '[V]/Am'. [H] means 'hypothesis' on page badges, in the hub precedence and in the repro vocabulary, but 'closed under the single anchor' in the W0 legend. The W0 legend also omits [V], although two vp-cards on the same page carry [V]. The same object gets conflicting grades: the empirical λ_anchor is [F] forced (it should be [L]/Calibrated); D is '[F] forced' on its card while §3.4 says 'The quantum diameter is carried as a single anchored constant'; φ_jam is [V] in W0/VH but [F] in W6; c² = B/ρ is [V] on its card but 'Wave-speed c emergence ... [F]' in W6; Tₑ ≈ 1 s is '[H]+' in W0 but electron_second is F in concepts.json; colour_closure is V in concepts.json but '[F]+[V]' in §10; seed19 and double_sha256 (procedural facts) are graded V ('verified against external data'). g* = c²·Ψ_yield carries [F] although Ψ_yield is defined as g*/c², which makes the formula an identity (§17 Result 2), and its per-body value is back-substituted.

**Proposed improvement.** Adopt one vocabulary across the corpus: map [H] to either 'hypothesis' or [L], not both, and add CALIB/[INPUT] -> [L]. Put one legend (including [V]) at the top of W0 and in AGENTS. Regrade: λ_anchor and D -> [L]; g* = c²Ψ_yield -> 'definition (Ψ_yield := g/c²), magnitude [O]'; seed/hash -> a 'procedure' tag rather than a grade. Add a registry gate that fails when a concept's grade differs from the grade printed at its canonical href.

### 6. [major] Amplification A and quantum diameter D are called 'parameter-free' and 'verified', but W6 shows they track the input threshold g₀

- **category:** internal-inconsistency
- **location:** physics abstract (docs/physics/_meta.json abstract → hub/homepage/JSON-LD); docs/physics/03-axioms-primitives-volume-particle-lattice §3.4; docs/physics/11-realization-units-t-rcross §11.3, §11.6; docs/physics/w6-provenance-ledger-which-numbers-come

**Quote.** abstract: "the amplification A=a_med/g^* (median spacing over the critical percolation throat) is a parameter-free lattice output" ... "The dynamical results above (single speed, forced radius, amplification) are verified" | §3.4: "the jamming simulation independently reproduces the length to 0.04% (4.8542pm — a selected length with a 7% distribution, scale-anchored to A_geo=cΔ t/a at 0.16%; §11.6)" | W6: "The magnitude A 10⁶ therefore scales as 1/g₀ — verified by re-running the released code at g₀=10⁻⁶,2×10⁻⁷,4×10⁻⁸, which gives D≈ 26,5.2,1.0 pm respectively. It thus tracks a numerical/threshold scale, not a scale-free physical invariant." | §11.6: "the SOC-measured A_mean(750)=5.69×10⁵ matches the unit-realization anchor A_geo=cΔ t/a (scaled by N^(-1/3)) to 0.16%"

**Evidence.** W6 (graded [H]) shows that D = 2πλ/A varies by a factor of 26 across the three input thresholds, and that 4.85 pm is either the median +2.4% (4.96 pm) or a 'best-bin selection'. So the abstract's 'parameter-free ... verified' and §3.4's 'independently reproduces ... to 0.04%' contradict the volume's own provenance ledger. A_geo is not independent either: §11.3 defines Δt = A·a/c_ref with A = 880918.977... (printed to 77 digits), so A_geo = cΔt/a returns A by construction. The '0.16%' match also involves unstated choices. Scaling A_geo by (200/750)^{1/3} gives 567,012, which is +0.35% from A_mean = 5.69×10⁵ and −16.1% from the median 4.76×10⁵ (the statistic that defines A = a_med/g*). Getting 0.16% needs an unstated reference N ≈ 203. N=200 gives A_med = 8.02×10⁵ and N=750 gives 4.76×10⁵, so A also depends on N.

**Proposed improvement.** Rewrite the abstract, §3.4 and §11.6 to match W6: 'A's dimensionless structure is simulation-backed; its magnitude scales as 1/g₀ and N^{-1/3} and is fixed by the unit anchor [L]; D = 4.85 pm is consistent with the simulated distribution (median 4.96 pm), not derived.' Drop '0.04%' as a corroboration. State the A_geo comparison with its reference N and statistic, or remove it. Print A to the precision its distribution supports (about 1 significant figure). Pre-register one g₀-independent observable (e.g. the shape of the D distribution) as the real test.

### 7. [major] The light-angle 'armed falsifier' and the 633/532 'closure' carry no predictive content

- **category:** circularity
- **location:** registry/modules.json (light_emergence.self_completeness); docs/physics/10-implementing-speed-light-clock-free §10.9 and §10.9.1; docs/physics/03-axioms-primitives-volume-particle-lattice §3.4; docs/physics/01-governance-no-tuning-lock-gate (objection B1)

**Quote.** modules.json: "their ratio closes ((λ/D)₆₃₃/(λ/D)₅₃₂ = 632.99/532). The single anchor (633) alone could be dismissed as a fit; the second line (532) closing against the same invariant is what proves D was not tuned. The committed angles χ(633)/χ(532) are an armed falsifier — a wrong D breaks the closure." | §3.4: "in D=2πλ/A the cross-consistency reduces to A₆₃₃/A₅₃₂=λ₆₃₃/λ₅₃₂=633/532 with D cancelling, so the two-wavelength agreement is a ratio independent of the value or rounding of D" | §10: "The same amplification A (hence the same D) reproduces the relation at both 632.99 and 532nm" | §10: "a 0.03% change in D shifts the visible-light angle by more than a degree"

**Evidence.** (λ₁/D)/(λ₂/D) ≡ λ₁/λ₂ for every D, so the 'closure' cannot fail, as §3.4 itself says. §10's 'same amplification A (hence the same D) ... at both' contradicts §3.4's A₆₃₃/A₅₃₂ = 633/532: with D fixed, A must scale with λ. For the angle, sinχ = λ/(mD) with m = ⌈λ/D⌉ gives χ = 90° − √(2ε/m) rad, where ε ∈ [0,1) is the ceiling remainder. For 633 nm (m ≈ 130443) χ therefore always lies in (89.776°, 90°] for ANY D near 4.85 pm, and the maximum swing is 0.224°, not '>1°'. The committed χ(633) = 89.9378° comes from λ/D = 130442.9232. A 1 ppm change in D gives χ = 89.898°, and 4 ppm gives 89.826°. §3.4 says D is known only to 0.04% (±52 in λ/D), which leaves the remainder ε completely undetermined, and swapping 632.99 for the full-precision anchor already moves χ to 89.7960° (the §10.9.1 note). No experiment named in the volume measures a 'propagation angle' of free light against a lattice axis.

**Proposed improvement.** Remove the 'proves D was not tuned' and 'armed falsifier' language from modules.json and §10. Mark the 633/532 check as 'identity (D cancels), no evidential weight' and fix the '>1°' statement to 'χ ∈ (89.78°, 90°], set by the sub-ppm remainder of λ/D'. If the angle is to be a falsifier, name the observable (instrument, expected signal size, a χ-distribution width predicted from D's 7% distribution) and pre-register it with a D-independent prediction.

### 8. [major] 6π⁵ is graded [F] forced although it misses CODATA by ~10⁶ σ, and the 'self-falsification' script cannot fail

- **category:** grading-honesty
- **location:** docs/physics/w0-result-scorecard-one-page-summary; docs/physics/01-governance-no-tuning-lock-gate §1.8.3 (companion geometric-count check); vp-card mp_me on all pages; registry/concepts.json mp_me; physics abstract

**Quote.** W0: "mₚ/mₑ = 6π⁵=2π· 3π⁴ (νₚ via LOCK-NU-N §8.0.5) | 1836.118 vs measured 1836.153 | [F]{} | -19ppm" | abstract: "the numerical ladder 3π⁴→6π⁵ rests on one definitional identification" | §1.8.3: "assert abs(mp_me_measured/pi**5 - 6) < 2e-4" ... "if a reader's run prints anything other than ALL PASS, the framework is wrong and the reader has found a real error, not a presentation issue."

**Evidence.** 6π⁵ = 1836.1181087. CODATA 2022 m_p/m_e = 1836.152673426(32), so the residual is −18.82 ppm = −1.08×10⁶ σ (−3.1×10⁵ σ against CODATA 2018's ±1.1×10⁻⁷). As an exact 'forced' identity it is excluded. It survives only as an approximate relation with an unexplained residual, and the abstract admits it rests on a definitional identification. I ran the §1.8.3 script: it prints ALL PASS. Its assertions are arithmetic facts (the numerical value of 2/π, a lattice-point count, Legendre's three-square theorem, a C₃ ring summing to zero) plus m_p/m_e/π⁵ − 6 = 1.13×10⁻⁴ checked against a tolerance of 2×10⁻⁴, i.e. 1.8× the known residual. None of these can fail for any state of nature, so the claim that a failure would show 'the framework is wrong' misdescribes the test. Look-elsewhere: 176 distinct values n/d·π^k (n, d ≤ 12, −2 ≤ k ≤ 8) fall in [500, 5000], and ±19 ppm windows around them cover ~0.29% of that log-range. The hit is notable but modest (Lenz 1951 already found it, and the volume cites that).

**Proposed improvement.** Regrade m_p/m_e = 6π⁵ as [H] (or 'structure [F], exactness [O]: −18.8 ppm residual unexplained') on the card, in W0 and in concepts.json, and state the σ-distance against CODATA 2022. Rename the §1.8.3 script an 'arithmetic consistency check' and drop the 'framework is wrong' sentence. Publish the look-elsewhere estimate (search space, trials factor) next to the claim. Pre-register what would falsify the ladder, e.g. a predicted next-order correction with a sign and size fixed before comparison.

### 9. [major] The 'c² = B/ρ simulation-validated to ~0.06%' that AGENTS.md attributes to physics is a 1-D chain identity from chemistry; physics takes c as an input

- **category:** cross-volume
- **location:** AGENTS.md §2 item 1 and §6 row 4; registry/vp.manifest.json chemistry.headline; docs/chemistry/01-electromagnetism-jammed-lattice-light; docs/physics/11-realization-units-t-rcross §11.3; W0 card c² = B/ρ

**Quote.** AGENTS.md: "**Substrate** — `c² = B/ρ` (speed of light = elastic-wave speed of the jammed lattice; simulation-validated to ~0.06%) ... This is `physics`." | chemistry §1: "The energy centroid propagates at c₍measured) = 0.99940 versus the closed form c₍theory) = a√(k/m) = 1 — a 0.06 % agreement." | physics §11.3: "Δ t = ℓ_eff/c_ref = 5.5761397188×10⁻¹³ m / 299 792 458 m/s"

**Evidence.** The 0.06% figure appears nowhere in physics. It comes from chemistry's 1-D harmonic chain m ü_n = k(u_{n+1} − 2u_n + u_{n−1}). For that chain B = k·a and ρ = m/a, so B/ρ = k a²/m = c² identically, and the 0.06% shortfall is just the group velocity v_g = c·cos(qa/2) of a finite-q Gaussian packet (cos(qa/2) = 0.9994 ⇒ qa ≈ 0.069). It checks the integrator, not the vacuum. Physics' own c² = B/ρ lives in lattice units (§11 table: K = 2.05×10⁴), and the SI value of c enters as the input c_ref in Δt = A·a/c_ref. c is therefore not predicted. c² = B/ρ is the textbook P-wave speed of a medium with G = 0, and the physical content of the [V] is G_relaxed → 0 at isostaticity (a known jamming result: O'Hern 2003, Wyart 2005).

**Proposed improvement.** In AGENTS.md and the manifest, attribute the 0.06% to chemistry and relabel it 'numerical check of a 1-D chain (identity), not a test of the vacuum'. In physics, say plainly that the validated statement is 'G_relaxed → 0 while B stays finite at z = 6 [V]', that c² = B/ρ follows from linear elasticity [F], and that the SI value of c is an input (c_ref), not an output.

### 10. [major] Front-page claims ('reproduces QED, GR and the Standard Model', '0 fitted parameters') go beyond what the volume grades

- **category:** grading-honesty
- **location:** docs/physics/rf-read-first-what-this-is ('A rival vacuum, not a reinterpretation'); docs/index.html ('0 fitted parameters'); docs/llms.txt; AGENTS.md §0; vs docs/physics/14-force-lattice-tension-1-r2 §14.5, 15-quantum-mechanics-mapping-completion-note, 17-extensions-optional-reading §17.4, 01-governance-no-tuning-lock-gate §1.8

**Quote.** RF: "The framework reproduces the empirical results of quantum electrodynamics, general relativity, and the Standard Model while rejecting their mechanisms." | homepage: "0 fitted parameters" | llms.txt: "Every number measured, never fitted." | §1: "The total tunable DOF count is therefore exactly one" | §15: "with h_VP calibrated to data; grade CALIB" | §17: "the absolute value 9.80665 m/s² at Earth's surface is back-substituted" | §14: "this section reproduces the standard QED ideal-Casimir result (the 240, the π², and the magnitude are textbook values), so it adds no VP-s[pecific]..."

**Evidence.** By its own ledger the volume does not derive α_em ([O], measured input); takes c (c_ref), h (h_VP 'calibrated to data') and per-body g (back-substituted) as inputs; reproduces Casimir only by importing the QED textbook result; and records the gravity sector as 'no surviving prediction distinct from GR'. No QED precision observable (g−2, Lamb shift) and no Standard Model content beyond m_p/m_e, m_H and r_p is computed. 'Reproduces the empirical results of QED, GR and the SM' is therefore an overclaim against the volume's own grades. '0 fitted parameters' conflicts with the volume's 'DOF = 1' tunable anchor plus its CALIB/[INPUT] items. AGENTS §0 says 'the one free-looking parameter [is] a stiffness γ, measured from DNA' and never mentions physics' own anchor λ_ref = 632.99 nm.

**Proposed improvement.** Replace the RF sentence with a scoped version, e.g. 'reproduces, with one length anchor and measured α_em, c and h: m_p/m_e to −19 ppm, m_H to −0.40%, r_p to +0.06%, and GR's time-dilation/redshift at the degenerate level; QED precision tests and the SM gauge/flavour structure are not addressed [O].' Change the homepage and llms.txt to '1 anchor (λ_ref) + declared measured inputs (c, h, α_em, per-body g); no fitted coefficients', and add λ_ref to AGENTS §0/§2.

### 11. [major] Reproducibility surface is broken: all 47 per-chapter repro links 404, core scripts are not in the repo, and manifest hashes match no commit

- **category:** reproducibility-code
- **location:** claim-strip on all 47 docs/physics/*/index.html; docs/physics/index.html ('every page carries its own reproducibility strip'); repro/physics/; registry/vp.manifest.json (physics content_sha256, repro_sha256); AGENTS.md §7; repro/physics/verification_dossier/SIMULATION_GROUNDING_AUDIT.md

**Quote.** chapter strip: <a href="https://github.com/rego093-sketch/jamming-physics/tree/main/repro/physics/03-axioms-primitives-volume-particle-lattice/" rel="noopener">재현 코드 (GitHub)</a> | hub: "every page carries its own reproducibility strip (DOI + repro/ deep link)" | manifest: "content_sha256": "6ec421fc342a0050d6b77ad693f1166b3ba490922ac234e06f36506d2dba95cf", "repro_sha256": "a4d2a0c79dd5e9cb854395bc1cc192d9a161c331e66902d9674922de611ce0ae" | W6: "reproducible from AQD_DOI_bundle_unified_v0.4.0_2026-06-05.zip ... via the entry points lattice_3d_jam_percolation.py, rcross_validate.py" | audit: "## 진짜 잔여 2 — 중력 m_q / 절대 g (공개된 [O])"

**Evidence.** 0 of 47 chapter-level repro links resolve: origin/main has only repro/physics/{registry,reports,site_seed,templates,tools,verification_dossier}, with no per-slug directories. The scripts behind every [V] physics number (lattice_3d_jam_percolation.py, soc_percolation_pinning.py, jamming_rotation_485pm_study.py, light_emergence_massfree.py, verify_appendix_*.py) are absent from the repository and exist only in a Zenodo zip. I recomputed tools/make_manifest.py's dir_content_hash: docs/physics = 878e3db3…, repro/physics = 9e81abbf…, the same at commits 51f6aef, 5cec8d6 and 5895347 (docs 14446d14… at 7d1620f). None of these equals the manifest's 6ec421…/a4d2a0…. Across the corpus 0/32 volumes match both hashes. Under AGENTS §7's own rule the state is 'suspect'. The dossier still shows chemistry-removal residue: residuals '2' and '3' with no '1', an empty code block, and an orphaned 'back-fit이 아님 (공정성 확인):' heading with nothing under it.

**Proposed improvement.** Point the per-page strip at existing paths (repro/physics/tools/ or a per-chapter index file), or generate the per-slug folders. Vendor the jamming/SOC/light-mapping scripts into repro/physics (or add a fetch-and-verify script with the Zenodo file hash). Rebuild the manifest in CI from the committed tree and fail the build on hash mismatch. Clean the dossier residue, and add an English summary of the IRREPRODUCIBILITY_LEDGER (which is currently Korean-only).

### 12. [major] Raw LaTeX leaks into 27 of 48 physics pages (629 tokens); the 'verified backbone' chapter and §18 are the worst

- **category:** presentation-rendering
- **location:** docs/physics/*/index.html, worst: sp-jamming-spine-verified-physical-backbone, 18-time-and-gravity, 14-force-lattice-tension-1-r2, 13-mass-u-lat-m-h, 10-implementing-speed-light-clock-free, w0-result-scorecard-one-page-summary, 06-continuum-core-model-deriving-rp (pre block); H1 of sp/06/10/11/13/14

**Quote.** SP table: "marginal⇒ shear modulusG_{relaxed}→ 0, bulkBfinite" and "l@<strong>Two sizes:</strong> protonr_p=0.8412fm|quantumD=4.8526pm (=6π^{6}r_p)" | §18: "the saturating channel $g_{\mathrm{restore}}$ is a \emph{contact} normal-force effect" | W0: "α_em⁻¹ = 4π(11 - 35/32·tfrac2π²·3/7)" and "[F]{} = derived from fixed geometry" | §14: "giving |mathbf B| (v/c)|mathbf E|" and "noindent[SUPERSEDED — record only" | §6: "\item LOCK: Lock the definitions ... in \texttt{analysis\_lock}/\texttt{gate\_lock}." | H1: "Jamming Spine — ... Speed of Light $c²=B/ρ$ and the Forced Proton Radius $rₚ=(2/π)λ_(C,p)$"

**Evidence.** Visible-text scan (alt text, <pre>, <code>, <script> excluded): 301 raw $…$ spans on 22 pages (no KaTeX/MathJax is loaded anywhere, so none renders); 91 '[F]{}'/'[H]{}'/'[O]{}'/'[V]{}' remnants on 13 pages; 41 '^(∘)' degree signs on 7 pages; 50 bare 'mathbf/mathrm' on 5 pages; 23 'noindent' on 3 pages; 5 'tfrac'; 89 backslash macros (\emph, \texttt, \textbf, \eqref) all in §18; 112 raw ^{…}/_{…} (95 in SP, 17 in §18). That is 629 tokens on 27 pages. There are also missing spaces around former inline math in SP, a tabular spec 'l@' leak, dropped '∼' ('A 10⁶', '( 10^{-15}m)', '|B| (v/c)|E|'), 6 H1 headings with raw $…$, one verbatim block containing a LaTeX itemize, and 6 equation alt texts with undefined author macros (\aVP, \Danchpm), which AI readers extracting alt text see verbatim. The SVG equations themselves render correctly (1272 files present, glyphs expanded).

**Proposed improvement.** Run SP and §18 through the same LaTeX→SVG/Unicode pipeline as the other chapters. Replace '[X]{}' with the badge span, '^(∘)' with '°', and 'mathbf X' with bold X. Restore '∼'. Strip $ from H1/hub titles (the <title> already has clean text). Expand \aVP/\Danchpm in alt text. Add a build gate that fails on /\$|\\[a-z]+|\{\}|\^\(∘\)|noindent|tfrac/ in visible text.

### 13. [minor] Every chapter prints its lead twice (16 print it three times) with stray tokens; pointer-stub pages; §18 is left out of the reading chain

- **category:** structure-redundancy
- **location:** all 47 docs/physics/*/index.html (<p class="answer"> + <p class="abstract">); rf-, w0-, vh-, w5-, 15-, 17-, 18-, axb-, axc-, axf-, axp-, ov-, 12- pages (stray tokens); cm-, r5-, axglink-, axepmr-, ov- (stubs); 18-time-and-gravity (nav); docs/physics/index.html (chapter order); 17-extensions-optional-reading §17.4 ('Earth–Cosmos volume')

**Quote.** RF: "Read First: This document does not reinterpret established physics ..." followed by "This document does not reinterpret established physics ... every familiar law is a behaviour of that medium. 5π." then the same sentence again in the body | W0 abstract ends "from what is earned. 4π." | §3 answer: "If χ_ST=0 we classify as non-stiff; if χ_ST=1 we classify as stiff." | CM: "The seven-item misreadings list was moved to the prologue (§0.5) in v0.5.0" | §17: "owned, as celestial applications, by the Earth–Cosmos volume (per-body appendix; same concept-DOI lineage)"

**Evidence.** 47/47 pages print the abstract inside the 'answer' paragraph and again as 'abstract'. 16 pages print it a third time as the first body paragraph (RF, CM, R5, OV, VH, W5, ML, BT, AXA/B/C/G/K/L, AXGLINK, §18). At least 13 abstracts end in an orphan 'key token' ('5π.', '4π.', '2π.', '2π/3.', 'z=6.', 'Ω=0,…,M-1.', '2/pi.', '3π⁴.', 'λ_C=(π/2)rₚ.', 'π-and-2.', 'δ=1/π².'), injected by the v0.11 answer-first generator (CHANGELOG_v0_11_0). Five pages (CM 114 words, R5 135, AXGLINK 150, AXEPMR 197, OV 254) only point elsewhere, yet count as chapters and sit at the end of the hub despite being titled 'front-loaded'. §18 has no prev/next links (§12.next = §1 and §17.next = §11, a leftover of the v0.9 re-wiring when the old chemistry §18 was removed). The hub order runs 10, 14, 17, 18, 11, 13, 15, 12, 1, 16. §17.4 still names an 'Earth–Cosmos volume', which does not exist among the 32 (VH says it was re-pointed to cosmology's DOI). physics/seams.json lists 'outgoing': [] even though §17/§18 hand off to cosmology Ch 7.

**Proposed improvement.** Render either the answer or the abstract, not both, and strip the key-token suffix. Fold the five stubs into redirects or anchors. Put §18 into the prev/next chain and sort the hub by section number, with the reader's-guide pages in a separate block. Rename 'Earth–Cosmos volume' to 'Vacuum-Inflow Cosmology (10.5281/zenodo.20568874)' and declare the physics→cosmology seams in seams.json.

### 14. [minor] Korean UI strings on English pages, and an author-name casing that differs only in physics

- **category:** presentation-rendering
- **location:** claim-strip, vp-cards and prev/next nav on 47 docs/physics/*/index.html (lang="en"); JSON-LD author on 47 physics chapter pages; repro/physics/*.md

**Quote.** "재현 코드 (GitHub)" / "DOI 스냅샷" / "백서 목차" / "용어" | JSON-LD: "author":{"@type":"Person","name":"Young jae Lee"

**Evidence.** 224 Korean UI strings on 47 English pages: 용어 ×84, 재현 코드 (GitHub) ×47, DOI 스냅샷 ×47, 백서 목차 ×46. Only physics and cosmology carry the Korean strip/nav; chemistry, for example, shows 'Reproduction code (GitHub)' and 'DOI snapshot'. 'Young jae Lee' appears in the JSON-LD of all 47 physics chapter pages and in no other volume; everywhere else, including the physics hub, it is 'Young Jae Lee', which can split author identity in Scholar/ORCID matching. The reproduction ledgers (IRREPRODUCIBILITY_LEDGER.md, SIMULATION_GROUNDING_AUDIT.md, CHANGELOGs) are Korean-only.

**Proposed improvement.** Use the English strings chemistry already uses ('Reproduction code (GitHub)', 'DOI snapshot', 'Contents', 'Glossary'), or set lang per span. Fix the JSON-LD author to 'Young Jae Lee' in the chapter template. Add English versions (or summaries) of the repro ledgers.

### 15. [minor] The proton-radius residual is quoted three ways, one of them a rounding artifact, and none against CODATA 2022

- **category:** internal-inconsistency
- **location:** docs/physics/w0-result-scorecard-one-page-summary (table); docs/physics/13-mass-u-lat-m-h; physics abstract; docs/physics/01-governance-no-tuning-lock-gate (5-line script comment)

**Quote.** W0: "rₚ = D_anch/(6π⁶) (predicted; was input) | 0.84125 fm vs locked 0.8412 | [F]{} | +61ppm" | §13: "rₚ=D_anch/(6π⁶) (−0.018% vs CODATA 0.8414 fm)" | abstract: "rₚ=(2/π)λ_(C,p)=0.8412 fm (CODATA charge radius 0.8414 fm)" | script: "# 1836.1181..., 0.063662..., 0.841251... (CODATA r_p = 0.8414 fm"

**Evidence.** D/(6π⁶) = 0.8412515 fm. The locked value (2/π)λ_C,p = 0.8412356 fm, so the true difference is +18.8 ppm (the 6π⁵ residual again). The '+61 ppm' comes from comparing against the 4-digit rounding 0.8412, and it compares to the framework's own lock rather than to data. Against CODATA 2018 (0.8414(19) fm) the difference is −0.018%. Against CODATA 2022 (0.84075(64) fm) it is +0.060% = +0.78σ. The same script uses the CODATA 2022 m_p/m_e but the CODATA 2018 r_p.

**Proposed improvement.** Quote one residual per quantity against one CODATA edition (2022): r_p = 0.84125 fm vs 0.84075(64) fm, +0.06% (0.8σ). Separately note that D/(6π⁶) and (2/π)λ_C,p differ by exactly the 6π⁵ residual (18.8 ppm). Drop '+61 ppm'.

**Strengths noted:**
- Several non-claims are recorded plainly: the α_em closed form 4π(11 − …) = 137.0364 is labelled coincidence/non-evidence [O]; the old Coulomb −0.43% is reclassified as overfit; the gravity sector is recorded as degenerate with GR (G-CAP-DEPART), and the cosmology volume reaches the same verdict, so that seam is consistent across volumes.
- W6's 'honest-reading notes' (A ∝ 1/g₀; D is a distribution, and 4.85 pm is a median/best-bin match) are exemplary self-audit. The fix above is to bring the abstract and §3.4 into line with them, not to weaken them.
- §3.4 states the real precision floor of D (0.04%) and openly notes that D cancels in the 633/532 cross-check. Absolute g is kept [O] through an explicit four-wall obstruction argument.
- Prior art for 6π⁵ (Lenz 1951) is cited in the prologue.
- Link integrity is good: all 1,363 internal hrefs/anchors in the physics pages resolve, and all 1,272 equation SVGs exist and render with author macros expanded.
- The LOCK → Derive → Gate discipline, the per-claim verdict tables, and the version/reclassification log give a referee a clear audit trail of what changed and why.
