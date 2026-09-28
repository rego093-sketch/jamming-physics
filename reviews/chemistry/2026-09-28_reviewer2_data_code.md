# Chemistry volume ("VP Chemistry & EM") — Reviewer 2 of 3: data, code, grades

Date: 2026-09-28 · Scope: `docs/chemistry/**/index.html` (hub + §1–§7 + §8 open register), `docs/chemistry/_meta.json`, `_decl.json`, `repro/chemistry/**`, `registry/vp.manifest.json` (chemistry row).
Lens: "data decides the theory". A claim counts only if (a) an external data source is stated and (b) code in the repo reproduces the number.
No files under `docs/` or `repro/` were edited. Scratch work: `/tmp/claude-0/.../scratchpad/r2chem/`.

## What I ran

| Run | Result |
|---|---|
| All 9 modules in `repro/chemistry/repro/chemistry/07-low-grade-waste-heat-electricity/`, each run twice | All 9 `RESULT sha256` prefixes match README and page (7c8246ab, 64e26ee6, 0067cbe1, d6d8a9ab, 0a3af6ec, aa45e145, aa296c82, 13d054c5, b59d22a5). Stdout identical on re-run. Each run took under 5 s. |
| `find` for every module/ledger named on §1–§8 | **44 of 53 referenced files are missing from the repo** (see F-01). |
| My own 1-D harmonic-chain leapfrog (`r2chem/chain.py`): Gaussian displacement pulse, energy-centroid speed, c_theory = 1 | Measured c = 0.955, 0.980, 0.993, 0.998, 0.9995 for packet width σ = 2, 3, 5, 10, 20 sites. So the "0.06 %" figure is set by the packet width (see F-02). |
| Independent recomputation of textbook numbers quoted on the pages (`r2chem/nh3.py` plus one-liners) | Ammonia equilibrium table (500 K: 10.8/76.3/82.6/87.3 %; 700 K: 0.6/29.1/40.7/52.4 %), T* = 463 K, Cu E_F = 7.05 eV, v_d = 0.074 mm/s, v_F = 1.57×10⁶ m/s, τ = 2.5×10⁻¹⁴ s, ℓ = 39 nm, λ_e(5.65 eV) = 5.16 Å, Wien 300 K peak = 9.66 µm, B for U_mag = k_BT ≈ 6.18×10³ T, pigment edges hc/E_g, Faraday 18.66 mmol/A·h, Dulong–Petit alumina 1223 J/kg·K, thermoelectric ZT = 1 → 5.5 %. **All reproduce from standard textbook formulas.** These are consistency checks of standard physics on [CAL] inputs, not tests of VP (see F-08). |

---

## Findings

### F-01 · CRITICAL · Code for §1–§6 and §8 is missing from the repository
**Pages:** hub, §1–§6, §8 (every "Reproduction code (GitHub)" link on §1–§6 points to `repro/chemistry/`, which holds only the §7 folder, a ledger and gate JSONs).
**Evidence:**
- Hub: "The work is fully reproducible (48 deterministic standard-library Python modules, six case ledgers, verification harnesses, and numeric-drift gates)".
- §2 CH.17: "Thirty deterministic, standard-library modules and a 114-row case ledger (cases_fixed.csv) … 32/32 PASS".
- §6 CA.9: "Six deterministic, standard-library modules and three case ledgers (29 rows) … (6/6 PASS, 29 rows)".
- §2 status line: "Every numeric claim is reproduced by a deterministic, standard-library module (2× sha256 identical)".

**What I found:** only 9 `.py` files exist, all for §7. The missing files are:
- **§1 (EM):** `vp_light_emergence.py`, `vp_electromagnetism.py`, `vp_light_angle.py`, `vp_refraction.py`, `vp_em_field_dynamics.py`
- **§2:** `vp_atomic.py`, `vp_valence.py`, `vp_molecular_geometry.py`, `vp_crystal_field.py`, `vp_statistical_thermo.py`, `vp_equilibrium.py`, `vp_kinetics.py`, `vp_solution_chemistry.py`, `vp_electrochemistry.py`, `vp_organic_chemistry.py`, `vp_crystal_packing.py`, `vp_gauss_shells.py`, `verify_chemistry.py`, `cases_fixed.csv`, `cases_em.csv`
- **§3:** `vp_copper_conduction.py`, `vp_iron_magnetism.py`
- **§4:** `vp_molecular_color.py`
- **§5:** `vp_platinum_catalysis.py`, `vp_pt_resonance_sim.py`, `vp_pt_reproduction.py`
- **§6:** `vp_dband_catalysis.py`, `vp_ammonia_synthesis.py`, `vp_water_electrolysis.py`, `vp_magnet_desalination.py`, `vp_ess_thermal.py`, `vp_new_materials.py`, `vp_co2_reduction.py`, `verify_applications.py`
- **§8 / ledger:** `vp_open_items_reexam.py`, `vp_bond_energy.py`, `vp_strength.py`, `vp_shell_correction.py`, `vp_dblock_chemistry.py`, `vp_desalination.py`

**Claims with no code in the repo:**
- **§1:** c² = B/ρ "0.06 %"; the 2-D triangular c_T → 0; D = 6π⁶ r_p (+18.8 ppm); the 1/r² exponent scan; |B|/|E| = v/c; Stokes |S₃| = S₀; χ(632.8) = 89.892° and χ(532) = 89.825°; Wien; Snell/rainbow; the EM.12 pulse speed 1.0001, Poynting residual 3e-2 and energy drift 3e-4.
- **§2:** a₀, Ry, the 9/9 formulas, VSEPR angles, H₂ C_v, S°, T* order, pH 2.88, Daniell 1.10 V, packing, magic numbers.
- **§3:** every number.
- **§4:** every number.
- **§5:** the volcano, the band edge at 4.5 eV, "LDOS ~2 %", CV 0.84, r = −0.91.
- **§6:** every number, including r = −0.97 (ε_d vs ΔE_CO), OER 0.37 V, the ammonia table and the ESS figures.
- **§8:** r = +0.18 (Morse β vs bond order), "sign correct 8/18".

The "32/32 PASS" and "6/6 PASS" harness results cannot be checked.
**Fix:** commit the modules, ledgers and harnesses under `repro/chemistry/` (the Zenodo snapshot may hold them). Until then, change the reproducibility statements to "code in DOI snapshot, not in repo" and list every item above as data-pending (table at the end). Make the module counts agree (hub 48, CH.17 30 + 2, CA.9 6).

### F-02 · HIGH · The "0.06 %" c² = B/ρ check is presented as the evidence for light emergence
**Pages:**
- Hub abstract: "light emerges at c² = B/ρ reproduced to 0.06%"; "The keystone is that light is not assumed but emerges … reproduced by a deterministic simulation to 0.06%".
- §1 lede: "matched by a deterministic simulation to 0.06%".
- §2 claim strip: "c² = B/ρ … reproduced to 0.06%. **[V] verified**".
- §1 EM.9 ledger: "c² = B/ρ … [F]/[V] … vp_light_emergence.py".
- `registry/vp.manifest.json` headline: "c²=B/ρ (0.06% sim)".

**Evidence from the body (§1 EM.2):** "A 1-D chain of quanta … integrated by leapfrog … c_measured = 0.99940 versus … a√(k/m) = 1 — a 0.06 % agreement … c²=B/ρ is verified to machine precision."

**Problems:**
1. A 1-D monatomic chain has no shear mode and no contact-number physics. It cannot test the claimed mechanism (G → 0 at the isostatic z = 2d = 6 while B survives). The only thing it tests is that a discrete wave equation propagates at a√(k/m).
2. In 1-D, B = k·a and ρ = m/a by definition, so c² = B/ρ = ka²/m "to machine precision" is an identity, not a test.
3. The 0.06 % is the lattice-dispersion residual of the chosen packet width. It is not agreement with any datum. My chain gives 0.955 → 0.9995 as σ goes from 2 to 20 sites.
4. The actual 3-D evidence (the physics volume's five-observable isostatic test and the pre-registered test E2, λ–D link PASS at ±10 %) is **never cited in chemistry**.
5. The body mentions a "2-D triangular lattice" c_T → 0 check, but there is no code for it (F-01).

AGENTS.md §2 already says the 0.06 % is "a 1-D wave-packet check, not the evidence".
**Fix:**
- Rewrite the hub abstract, §1 lede and §2 strip along these lines: "c² = B/ρ is inherited from VP Theory (3-D five-observable isostatic test; E2 at ±10 %). A 1-D chain illustrates the discrete wave speed (0.06 %, packet-width dependent)."
- Downgrade the 1-D row to "illustration" and remove "[V] verified" from the §2 strip.
- Remove `c2_brho` from `_decl.json` `owns_terms`. Chemistry inherits this term (EM.0: "This chapter does not re-derive it").

### F-03 · HIGH · No external data source is cited anywhere in the volume
**Pages:** all of them. A grep for reference markers (author, year, DOI other than the volume's own and the AQD DOI, CRC, NIST, Kittel, Nørskov 2005, Trasatti, Hori 1994, Peterson 2010) finds only name-drops ("Hammer–Nørskov", "Hori", "Peterson–Nørskov", "Slater", "Clementi–Raimondi"). There is no bibliography and no data file.

Unsourced data tables that the grades depend on:
- **§3:** the Bethe–Slater D/d values (Cr 1.18, Mn 1.47, Fe 1.63, Co 1.82, Ni 1.98); Curie temperatures; moments 2.22, 1.72, 0.62 µ_B; σ_Cu.
- **§4:** E_g for 9 pigments; Δ = 20 300 cm⁻¹.
- **§5:** ΔG_H* and log j₀ for 7 metals; ε_d (Pt −2.25, Au −3.56 eV); φ_Pt = 5.65 eV.
- **§6:**
  - ΔH/ΔS for NH₃; ε_d/ΔE_CO sets (r = −0.97); E° table.
  - The scaling offsets 3.2 eV (OOH–OH) and 0.74 eV (CO→CHO).
  - χ_v(water); seawater 27 bar; α of black Cu.
- **§7:** Gd T_c; Cu Seebeck 1.8 µV/K; NdFeB ΔB; India fleet ~110 M units; capital costs.

The §5 table calls ΔG_H* "measured". Values of that kind are normally DFT-computed (Nørskov et al. 2005), not measured. The r = −0.91 "non-circular test" depends on where the ε_d set came from.
**Fix:** add a per-chapter data-source table (value, source, measured vs DFT). Label computed ΔG_H* as "DFT (literature)". Put the data in `repro/chemistry/data/` as CSV with provenance columns.

### F-04 · HIGH · §7 headline efficiency is mechanical, not electrical
**Page:** `docs/chemistry/07-low-grade-waste-heat-electricity/`.
**Evidence:**
- Lede: "Low-grade waste heat to electricity … replaced by a Carnot-bounded thermomagnetic engine reaching η ≈ 2.6–4.4%".
- CA.11: "The practical window is η ≈ 2.6–4.4% (34–58% of Carnot)".
- CA.10: "≈ 0.4% at ΔT = 25 K".

**What I ran:**
- `vp_regenerator_microchannel.py`: "NET eta_mech=4.44% … eta_elec=2.27%" and "eta_mech=2.65% … eta_elec=1.35%".
- `vp_thermomagnetic_regenerative.py`: ε = 0.90 gives eta_mech 2.74 % and eta_elec 1.40 %; ε = 0.95 gives 4.05 % and 2.07 %.
- `vp_thermomagnetic_design.py`: bare eta = 0.41 % (mechanical). Electrical is 0.21 % per the regenerative module.

The code computes heat-to-electricity as mechanical efficiency × η_coil (0.6) × η_PE (0.85), which is about half. The ~290 W and ~23 kW outputs on the page do use electrical efficiency, so the page mixes the two.
**Fix:** state the heat-to-electricity efficiency as **η_elec ≈ 1.35–2.27 %** (mechanical 2.6–4.4 %) in the lede, CA.11 and the CA.13 ledger. Grade η_coil = 0.6 and η_PE = 0.85 as assumptions.

### F-05 · HIGH · §7 "[V] verified / simulation-measured" covers closed-form arithmetic, a string-printing module and a hand-tuned toy
**Page:** §7 chapter chip "[V] verified"; CA.9c, CA.10, CA.11, CA.13.

**Evidence from the code:**
- **CA.9c, `vp_blackcu_absorber_not_generator.py`:** the module only prints fixed strings. Its hash is `sha256(np.array([S_cu, Tmelt_cu]))`, taken over two hard-coded constants. The page calls this "[V] simulation-measured". The page also says α ≈ 0.96 while the module prints ~0.95.
- **CA.10, `vp_thermomagnetic_oscillator.py`:** a normalized model with hand-set parameters (`tau=0.55  # thermal lag (key for self-oscillation)`, `A=2.6; lam=0.32`, `b_elec=0.55`, `Thot=0.95; Tcold=0.05`). It shows that a limit cycle exists inside the model. It does not show operation "on a 15–25 K span", which the page claims, and it has no link to SI units.
- **CA.10 and CA.11, `vp_thermomagnetic_design.py` / `vp_thermomagnetic_regenerative.py`:** closed-form algebra on unsourced material inputs (`Lh = 3000 J/kg`, `cp = 500`, `Ms = 1.0e6 A/m`, `Tc = 310 K`, `wt = 3 K`). The regenerative law η = Carnot/[1+(1−ε)R] is stated without derivation or source. The page says Tc is tuned to 40–60 °C, but the code uses 37 °C.
- **None of these is compared with a published thermomagnetic-generator prototype.** That comparison is the external data that would make any of them [V].

**Fix:**
- Change the §7 chapter chip to mixed [F]/[H].
- Regrade CA.9c from [V] to [F] (a textbook fact: Seebeck of Cu, melting point).
- Regrade the oscillator to "[H] in-model existence".
- Regrade design and regenerative to [H] with the material inputs marked [CAL] and cited.
- Add a data-pending entry: "benchmark η_elec against published TMG prototypes".

### F-06 · MEDIUM · §7 engineering and economic claims: grade and input disclosure
**Page:** §7 CA.12 and CA.13.
**Evidence:**
- "Across India's ~110 million room air-conditioners this is of order 30 TWh/yr **[CAL]**". This is a projection, so it should be [H]. [CAL] means a measured constant.
- "Better heat rejection and a higher-COP unit save ~30% … three to four times the harvester". In `vp_waste_heat_scale.py` this is an input, `sav_eff=0.30*Pac`, not a result.
- The same module hard-codes the harvester efficiency: `eta_elec=0.023`.
- `vp_datacenter_economics.py` hard-codes `eta_mech=0.577*Carnot`, uses a 20 K span (§7 elsewhere uses 25 K) and assumes capital of "$90,000–130,000" with no source. The payback of 4–6 years comes straight from those assumptions.
- The page does grade per-unit and data-centre figures [H] in CA.13, which is good. The India TWh figure and the 3–4× comparison are not graded that way.

**Fix:**
- Regrade the India TWh figure to [H].
- Mark "~30 % efficiency saving" as an assumed input and cite a source.
- Disclose all economic inputs on the page: price, capital, hours, grid CO₂ factor, and the ΔT = 20 K choice.
- Separate the physics block (CA.8–CA.11) from the engineering/economics block (CA.12) with an explicit "not physics, not VP-derived" label.

### F-07 · MEDIUM · "Standard-library" claim is false for the code that exists; hashes are not stdout hashes
**Page:** §7 status line: "Every numeric claim is reproduced by a deterministic, standard-library module (2× sha256 identical)". §1, §2 and §6 say the same about their missing modules.
**Evidence:** all 9 §7 modules `import numpy` (their own headers say "standard-library + numpy only"). The RESULT hash is taken over `numpy.float64.tobytes()` of selected arrays, not over stdout, so it can change across numpy, BLAS or platform versions.
**Fix:** change the wording to "Python 3 + numpy", pin the numpy version in a `requirements.txt`, and state what is hashed.

### F-08 · MEDIUM · Chapter chips "[F] forced" on §2/§3/§4/§6 are inflated; textbook results are graded as VP-forced
**Pages / evidence:**
- **§6:** chapter chip "[F] forced". Its own ledger CA.7 grades the d-band apexes, the OER limit, the absorber and ε_d → binding as [F?], [V] or [CAL]. The claim strip says "ε_d … [CAL]→[F]", which contradicts CA.7 "[F?]".
- **§3:** chip "[F] forced". The lede says "iron a net moment ≈ 2.2 μ_B … Both follow from d-band occupation, not from adjustable parameters". Its own CM.13 says "Fe 2.22, Co 1.72, Ni 0.62 μ_B — an itinerant/band effect marked [O]", and the Hund count used gives 4.90 µ_B.
- **§2 CH.10 and CH.11:** "pH 2.88 (measured 2.87) [F]" and "Daniell 1.10 V (matches measured) [F]". Both are textbook formulas applied to [CAL] inputs (pKa, E°). Their agreement with measurement is not a test of the jammed-lattice substrate. The same holds for the ammonia table, Faraday, Carnot, Dulong–Petit and Stefan–Boltzmann in §6. I reproduced all of them without any VP input (see "What I ran").
- **§5:** the CT.8 "[V] reproduces platinum" is a reproduction of established Newns–Anderson / Hammer–Nørskov physics on literature ε_d. The page says so, but the hub attributes it to the single anchor ("a single d-band descriptor reproduces why platinum is the optimal hydrogen catalyst"). CT.6 still says "platinum's catalytic efficiency — read in the VP picture as electron-amplitude-wavelength resonance — is what makes the low-voltage electrolysis … feasible". That is stale text: CT.7 refutes it on the same page.

**Fix:**
- Set chapter chips to the lowest grade that carries the headline: §3 → [F]/[CAL]/[O], §6 → [F?].
- Add a grade or tag such as "[F-std] standard physics, VP-consistent" for textbook results, so VP-specific forced claims stand apart.
- Delete or rewrite the stale sentence in CT.6.
- Fix the §3 lede: 2.2 µ_B is [O].

### F-09 · MEDIUM · §3 "7/7, no fitted magnetic parameter" relies on an empirical threshold
**Page:** §3 CM.11 and CM.12.
**Evidence:** "above a critical value (≈ 1.5) the exchange integral is positive … [F]/[CAL]"; "7/7 classification [F] … with no fitted magnetic parameter".
The D/d values have no source (F-03). The threshold 1.5 is the empirical Bethe–Slater crossing, and it sits between Mn at 1.47 and Fe at 1.63, so it effectively decides the Mn/Fe split. The 7/7 is therefore a classification with a calibrated boundary, not a forced derivation.
**Fix:** grade CM.12 [F]+[CAL] (or [F?]) and cite the D/d source and the origin of the threshold. A stronger test would be to apply the same rule outside the late-3d row (4d/5d, alloys such as Heusler Cu₂MnAl) as a falsifier.

### F-10 · LOW–MEDIUM · §4 pigment table is inconsistent with its own rule (CdSe)
**Page:** §4 CC.5 and CC.7.
**Evidence:** the table has "CdSe cadmium red · 1.73 · 717 · red (only deep red reflected)". CC.7 says "Black: gap smaller than every visible photon (E_g < 1.8 eV …)", and CC.2 defines visible as 400–700 nm.
By the chapter's own rule, E_g = 1.73 eV (edge 717 nm) absorbs all visible light, so the prediction is black or dark brown. Pure CdSe is in fact dark. "Cadmium red" pigment is the CdS·Se solid solution, which already has its own row.
This table is used as a falsification test ("tested across the cadmium series").
**Fix:** relabel the row as "CdSe (pure) → black/dark brown (rule-consistent)", or give the cadmium-red solid-solution E_g (~1.8–2.0 eV). Consider also noting TiO₂ (edge 407 nm, just inside the 400–700 window in CC.2).

### F-11 · LOW · Cross-document mismatches
- `IRREPRODUCIBILITY_LEDGER.md` #12 cites `vp_desalination.py`; the page (§6 CA.4) says `vp_magnet_desalination.py`. Neither file exists.
- The ledger #12 reason is "채널 가로 자기에너지 ~10⁻² k_BT" (magnetic energy across the channel ~10⁻² k_BT). The page's primary argument is U_mag/k_BT ~ 10⁻⁹. The 10⁻² figure is the Lorentz-force argument.
- §1 EM.2: "verifies D=6π⁶ rₚ to within **+18.8 ppm**, which is exactly the headline residual mₚ/mₑ = 6π⁵ (**−19 ppm**)". The signs are opposite without explanation.
- §7 README and page, data-centre figures: the page says "9% of the unit's cooling electricity" for the 10 kW AC (from `vp_regenerator_microchannel`, 294 W), while the 9 % (8.7 %) actually comes from the 1-ton AC in `vp_waste_heat_scale`. That is two different units, though the numbers happen to be close.
- Module counts: hub 48, CH.17 30 (32 with EM), CA.9 6. §5, §4 and §3 modules are not counted in any harness.

### F-12 · LOW · Registry and seam labels (grade-relevant)
- `registry/vp.manifest.json` headline "φ_RCP = 0.7405" and `_decl.json` `adds: "phi_RCP=0.7405"`. The chemistry pages correctly call 0.7405 the FCC/HCP value (CH.13). The "RCP" label in the registry and `_decl.json` is wrong (RCP ≈ 0.64) and should become `phi_FCC=0.7405`.
- Hub badge "Inherits: R19 switch". Chemistry's only declared parent is physics, and R19 is first stated in dna (downstream). No chemistry page uses R19. Drop the badge or declare the seam.
- `_decl.json` `owns_terms: ["c2_brho", …]` conflicts with inheritance from physics (F-02).

---

## Data-pending register (proposed entries)

| # | Claim (page) | Missing | Needed to close |
|---|---|---|---|
| DP-1 | c² = B/ρ 1-D check 0.06 %, 2-D c_T → 0 (§1 EM.2) | code; not evidence | commit `vp_light_emergence.py`; cite physics five-observable test + E2 as the evidence |
| DP-2 | χ(632.8 nm) = 89.892°, χ(532 nm) = 89.825° (§1 EM.6) | code, and no measurement | commit `vp_light_angle.py`; state an experimental protocol (this is the volume's only novel forward prediction) |
| DP-3 | EM.12 pulse 1.0001, Poynting residual 3e-2, energy 3e-4 | code | commit `vp_em_field_dynamics.py` |
| DP-4 | D = 6π⁶ r_p (+18.8 ppm) | code; sign | commit code; reconcile sign with −19 ppm |
| DP-5 | §2 numbers (a₀, Ry, VSEPR, C_v, S°, T*, pH, E°cell, packing, magic numbers), ledgers `cases_fixed.csv` (114 rows) and `cases_em.csv` (16 rows) | code + ledgers | commit the 30 modules, ledgers and `verify_chemistry.py` |
| DP-6 | §3 Cu plasma/skin/Drude; Fe 7/7 | code + D/d source | commit 2 modules; cite D/d + threshold |
| DP-7 | §4 pigment/d–d/FEM table | code + E_g sources | commit `vp_molecular_color.py`; cite E_g |
| DP-8 | §5 volcano, band edge 4.5 eV, LDOS 2 %, CV 0.84, r = −0.91 | code + ΔG_H/j₀/ε_d sources (measured vs DFT) | commit 3 modules + data CSV |
| DP-9 | §6 r = −0.97, NH₃ volcano apex E_N ≈ −0.5 eV, OER 0.37 V, ESS 46 kWh / 5.4 d, absorber ±W | code + sources | commit 7 modules, 3 ledgers, `verify_applications.py` |
| DP-10 | §8 r = +0.18 (Morse β), 8/18 EA sign, ~22 % IE error | code | commit `vp_open_items_reexam.py` and 4 dependents |
| DP-11 | §7 η_elec 1.35–2.27 %, ~290 W, ~23 kW | external benchmark | compare with published thermomagnetic-generator prototype efficiencies; cite material properties (L, c_p, M_s, T_c) |
| DP-12 | §7 India 30 TWh/yr, "efficiency saves 3–4×", payback 4–6 yr | sources for fleet size, 30 % saving, capital cost, tariff | cite or mark [H]-assumption |

## Items checked and found sound
- The 9 §7 modules run deterministically and reproduce every hash and number quoted on the §7 page, apart from the mech/elec labelling (F-04) and α 0.95 vs 0.96.
- The refutations in CA.9a (static B does no work: KE constant, ⟨v_x⟩ ≈ −0.006 vs −1.74 with E) and CA.9b (COP·η_Carnot = 1, loop −65 %) are correctly computed. Their conclusions are standard physics, which is appropriately graded [F].
- The textbook numbers I recomputed (see "What I ran") all agree with the page.
- The body of §1 EM.2 does honestly say "1-D chain". The misstatement is in the hub, the lede, the §2 strip and the manifest (F-02).
- The §5 self-refutation (CT.7) and the §6 CA.4 magnetic-desalination refutation are good practice. Their code is missing (F-01).
