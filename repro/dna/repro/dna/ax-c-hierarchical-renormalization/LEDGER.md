# LEDGER — hierarchical scale-renormalization interpreter

Per-channel honest grading. Generated from `hierarchy/grading.py` (the single
source of truth); do not edit by hand — re-run `run.py` / regenerate.

Grades: **[L]** measured/universal/theorem-grounded · **[V]** verified exact (precision) · 
**[F]** model/fiat (modelling choice) · **[O]** open obstacle (accuracy untested).

| # | channel | grade | basis |
|---|---|---|---|
| 1 | density renormalization  rho' = phi * rho | **[V]** | exact: void carries no mass, so aggregate density is the packing fraction times the unit density; mass/volume conservation. Deterministic, bit-for-bit. |
| 2 | exact composite bounds  B_Reuss = 0,  B_Voigt = phi * B_unit | **[V]** | exact elastic-mixture THEOREMS (Reuss 1929 isostress lower; Voigt 1889 isostrain upper) with a void phase B_void=0; evaluated exactly. The effective modulus is GUARANTEED inside this bracket. |
| 3 | wave-speed softening ratio per rung  c'/c = sqrt(J(phi)) | **[V]** | exact: the VP master relation c^2=B/rho applied at both levels gives c'/c = sqrt(B'/B * rho/rho') = sqrt(phi*J / phi) = sqrt(J). Deterministic closed form. |
| 4 | renormalization-group composition (R∘R associativity) | **[V]** | exact: climbing two rungs equals one combined rung to < 1e-9 (semigroup property); the ladder is a consistent RG flow. |
| 5 | monotone wave-speed softening up the tower (uniform phi) | **[V]** | exact RG theorem of the idealized ladder: J<1 for every phi<1, so c strictly decreases each rung. Holds for any phi<1 with no ECM stiffening; that proviso is stated. |
| 6 | rigidity-onset shape  J(phi) = sqrt((phi-phi_c)/(1-phi_c)) | **[L]** | the SHAPE is the composition of two CITED universals: excess coordination Delta_z ~ (phi-phi_c)^(1/2) (O'Hern 2003) and rigidity G ~ Delta_z (Wyart 2005). Not a free choice; read from the locked DB. |
| 7 | jamming anchors  phi_c, z_iso=2d, onset exponent 1/2 | **[L]** | independently published universals (O'Hern-Silbert-Liu-Nagel 2003; Maxwell isostatic counting; Wyart-Nagel-Witten 2005), read from the locked DB; no fit. |
| 8 | RG-ladder framing (repeated coarse-graining of jammed units) | **[L]** | the jamming transition admits a renormalization-group / scaling description (Goodrich-Liu-Sethna 2016) and applies to CELL packings (Bi-Lopez-Schwarz-Manning 2015); grounds the ladder construction. |
| 9 | orthogonality  mechanical LEVEL ⟂ SHAPE | **[V]** | SHAPE = robust_z(B(x)) is invariant under both LEVEL moves (field scale, uniform stiffness offset) to machine epsilon (analytic) + geometry moves SHAPE (numeric). Same robust_z as cell-level A4. |
| 10 | scale classification ledger (every channel tagged L0..L4) | **[L]** | a declaration, not a computed quantity: each corpus reading channel is tagged with the structural level it reads and how it connects to the tower. Carries no fitted number; exists so scale cannot drift. |
| 11 | per-rung packing fraction profile phi_k (demonstration climb) | **[F]** | a documented jammed profile (all phi in (phi_c,1)) standing in for measured per-rung stereology; the operator is GENERAL in phi -- measured fractions change only the numbers, not the machinery. |
| 12 | ladder length scales L0..L4 (cell~10um, tissue~100um, ...) | **[F]** | generic textbook orders of magnitude, used ONLY to count units-per-rung (a reported volume ratio); the dimensionless flow does not depend on them at all. |
| 13 | ABSOLUTE modulus at each biological level (B in Pa) | **[O]** | ACCURACY untested. The single-unit modulus is a generic placeholder and sets absolute magnitude only; the engine does NOT compare to a measured modulus (that would be back-fit). |
| 14 | REAL per-rung packing fraction phi(level) | **[O]** | ACCURACY untested. The demonstration phi profile is a modelling choice; the real per-level cell packing fraction is unmeasured here. |
| 15 | REAL monotonicity vs ECM stiffening (cartilage, bone) | **[O]** | ACCURACY untested. The idealized flow softens monotonically; real extracellular-matrix mineralization can RAISE the unit modulus and break monotonicity. Not modelled; flagged as the named obstacle. |

## Locked constants (zero inline magic numbers)

`lock_manifest()` reports **inline_magic_numbers = 0**. 
Every number used by the interpreter is one of:

| constant | value | grade | provenance |
|---|---|---|---|
| `phi_c` | 0.639 | [L] | Onset-of-jamming packing fraction phi_c for 3D frictionless spheres ~ random close packing ~0.639: O'Hern, Silbert, Liu & Nagel 2003, Phys. Rev. E 68:011306 ('Jamming at zero T and zero applied stress'). At phi_c the bulk AND shear moduli simultaneously become non-zero. Bernal 1960 / Scott & Kilgour 1969 give RCP~0.6366. FRICTION and POLYDISPERSITY shift phi_c down (frictional ~0.55-0.58) -- which is exactly why the ABSOLUTE biological value is graded [O], not this universal anchor. |
| `dimension_d` | 3 | [L] | Physical space dimension d=3. Enters the isostatic coordination z_iso = 2d. |
| `z_isostatic` | 6 | [L] | Maxwell isostatic coordination z_iso = 2d = 6 in 3D (Maxwell 1864 counting argument; exact). At the jamming point the packing is marginally rigid with z = z_iso (O'Hern et al. 2003). |
| `coordination_onset_exponent` | 0.5 | [L] | Excess coordination above isostatic scales as Delta_z = z - z_iso ~ (phi - phi_c)^(1/2): O'Hern et al. 2003 PRE 68:011306 (Eq. 6 / Fig. 9), confirmed across potentials, polydispersity, and dimension. Universal exponent 1/2; not fitted. |
| `rigidity_coordination_exponent` | 1.0 | [L] | The rigidity that emerges CONTINUOUSLY at the transition (the shear modulus, which vanishes at phi_c) is set by the excess connectivity above isostaticity: G ~ Delta_z (linear in excess contacts): Wyart, Nagel & Witten 2005 EPL 72:486; Liu & Nagel 2010 Annu. Rev. Condens. Matter Phys. 1:347. Composing with Delta_z ~ (phi-phi_c)^(1/2) gives the continuous rigidity onset ~ (phi-phi_c)^(1/2). |
| `unit_bulk_modulus_pa` | 1000.0 | [O] | [O] Single-cell elastic modulus E ~ 0.1-10 kPa varies by cell type and method (AFM nanoindentation, optical-tweezer/optical-stretcher, micropipette aspiration): Hochmuth 2000 J. Biomech. 33:15; Guck et al. 2005 Biophys. J. 88:3689. A generic 1 kPa central placeholder stands in; the per-cell-type MEASURED modulus is the named obstacle. Absolute B-flow is [O]. |
| `unit_density_kg_per_m3` | 1070.0 | [L] | Mammalian cell mass density ~1.03-1.10 g/mL (slightly denser than water): e.g. Grover et al. 2011 PNAS 108:10992 (suspended microchannel resonator). Generic central value; used only as the density anchor of the ladder. The DIMENSIONLESS softening ratio does not depend on it. |

## Gate (fail-closed)

| check | result |
|---|---|
| `H1_effective_modulus_in_exact_bracket` | **PASS** |
| `H2_jamming_threshold_sharp_onset` | **PASS** |
| `H3_density_renormalization_exact` | **PASS** |
| `H4_rg_flow_softening_and_composition` | **PASS** |
| `H5_orthogonality_level_perp_shape` | **PASS** |
| `H6_no_inline_magic_numbers` | **PASS** |
| `H7_non_fit_invariant` | **PASS** |
| `H8_determinism_2x_sha256` | **PASS** |
| `H9_honest_grades_and_scale_coverage` | **PASS** |
| **overall** | **PASS (9/9)  sha=9e8092715032c8a5** |

## Completion — honestly False

`completion.complete = False`. the renormalization MACHINERY is precision-exact ([V]) and the rigidity onset is [L]-grounded, but the ABSOLUTE biological moduli and the REAL per-rung packing fractions are accuracy-untested [O]; named obstacles below. Precision (정밀) is earned; accuracy (정확) is not yet claimed.

Open channels (accuracy NOT claimed):

- **[O] ABSOLUTE modulus at each biological level (B in Pa)** — obstacle: measured per-scale modulus atlas (elastography MRE/USE, AFM nanoindentation, micro-rheology) across cell -> tissue -> organ
- **[O] REAL per-rung packing fraction phi(level)** — obstacle: measured cell packing fraction at each level by confocal/EM stereology (and ECM volume fraction)
- **[O] REAL monotonicity vs ECM stiffening (cartilage, bone)** — obstacle: per-tissue ECM / mineralization stiffness contribution (e.g. measured cartilage/bone modulus vs cell modulus)

What would close it: supply the named measured datasets (per-scale modulus atlas + per-rung stereology + ECM contribution), feed the measured phi profile and B0 into the SAME operator, compare the predicted softening trajectory to a measured elastography ladder with a shuffle control, pre-register the sign; then and only then mark 정확.

Reference hierarchical reading hash: `cc6d03258ecc6a10`

---

*precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
