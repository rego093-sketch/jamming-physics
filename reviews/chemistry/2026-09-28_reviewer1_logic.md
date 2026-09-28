# Chemistry volume — Reviewer 1 of 3 (derivation chain & inheritance)

Date: 2026-09-28 · Scope: docs/chemistry/* (hub + §1–§8), docs/chemistry/_decl.json, seams.json, repro/chemistry/, and the chemistry rows of registry/vp.manifest.json / docs/index.html.
Parent reference: AGENTS.md; docs/physics/lt-light-chain-doubts-and-resolutions/ (Links 2, 5, 6, 6a, 7); docs/physics/14-force-lattice-tension-1-r2/ (Update 2026-09-28 note); docs/physics/sp-jamming-spine-verified-physical-backbone/.
No file under docs/ or repro/ was edited.

## Summary verdict

Chemistry has not caught up with physics' current (2026-09-28) account of light. Physics now says: c comes from the longitudinal scaffold; **E is the transverse swing of the rotating quanta; B is the lattice's rotational response; the along-ray part is the carrier, not a field**. This is graded [H], and the lattice run is data-pending. Chemistry §1 still teaches the superseded picture ("longitudinal E, transverse B [F]") and says "light is the single longitudinal wave." Chemistry §3 builds its whole explanation of copper conduction on "electricity = longitudinal EM mode." Several parent [H]/[V at ±10%] results are shown as [F]/[F]/[V]. The pages never explain why people feel E and B. The φ = 0.7405 problem is **a labelling error only**: every chemistry page uses 0.7405 correctly, as FCC/HCP crystal packing. No derived number depends on calling it φ_RCP. The wrong label sits in the metadata layer (_decl.json, manifest, homepage, the ambiguous hub abstract). There is also a large undeclared seam: most of the "forced" chemistry is standard quantum mechanics and statistical mechanics that is imported, not derived from the substrate. Finally, the §1–§6 reproduction code that the pages cite is not in the repository.

---

## A. E/B picture and light (Link 6a consistency)

### R1-01 · critical · docs/chemistry/01-electromagnetism-jammed-lattice-light/index.html (EM.4)
Evidence: heading "EM.4 The E/B geometry: longitudinal E, transverse B [F]"; "the electric field is the force directed along the light (propagation) direction; the magnetic field is the force directed at 90° to it."
Why: physics Link 6a says this is the exact reading it retracted ("Earlier editions called the straight, along-the-ray component 'the electric field'… Measurement does not allow that"). The physics §14 update note also calls it superseded. So chemistry contradicts measured data (E ⟂ ray, Malus's law) and its own parent. It also grades the retracted reading [F], while the parent grades even the corrected reading only [H].
Fix: rewrite EM.4 to inherit Link 6a word for word as provenance. Longitudinal scaffold = speed c and energy-flow direction (not a field). E = transverse swing (the wave's substance). B = the lattice's rotational response, ⟂ ray and ⟂ E, with |E| = c|B| for radiation. Grade [H], lattice run data-pending, and cite §LT Link 6a as the seam. Keep the moving-charge relation |B| = (v/c)|E| (really B = v×E/c²) as the near-field of a moving source, clearly separated from the radiation ratio.

### R1-02 · critical · §1 hub abstract, EM.2, EM.9; §2 claim strip; hub index.html
Evidence: "leaving a single longitudinal wave at c² = B/ρ" (hub); "light is the unique surviving longitudinal wave of the jammed lattice" (EM.2); §2 strip: "light is the single longitudinal wave that survives… [V] verified."
Why: in the parent, the longitudinal branch is only the *carrier* that sets c. Light's substance is the transverse swing, and "there is no longitudinal light" (Link 6a). Calling light "a longitudinal wave" is the old error. It is also the exact objection (Doubt 6a) that physics answers by separating speed from polarization.
Fix: say "c is set by the single surviving longitudinal branch, c² = B/ρ; light is the transverse swing of the rotating quanta carried on it." Apply everywhere, including metadata one-liners (_meta.json chapter 1 one_liner, modules page "light_emergence" description, which also says "single surviving longitudinal elastic wave").

### R1-03 · critical · §1 EM.6; §3 CM.1, CM.4, CM.6, CM.14
Evidence: EM.6 "Its longitudinal part (∇·u, compression = deficit) is the static Coulomb field; its transverse, propagating part is light… Electric conduction is the extreme-longitudinal limit (χ→0)". CM.1 "The same free-electron sea reflects the transverse wave and transmits the longitudinal one." CM.4 "This longitudinal disturbance is the current." CM.6 "Signal velocity ∼ c: the longitudinal field disturbance".
Why:
(i) Under Link 6a the along-ray component is the carrier and "not itself a radiating field". A static E is the "swing strain" near a charge (Link 6a), not a longitudinal compression. So "longitudinal = Coulomb/E" and "conduction = longitudinal EM mode" both rest on the retracted identification.
(ii) The explanation also conflicts with data. A DC/low-frequency current is driven by an E field along the conductor inside it. The signal on a wire travels as a guided TEM mode whose fields outside the wire are transverse to it, and energy flows through the surrounding field (Poynting). A longitudinal density wave of the electron sea is a plasmon, which is a different thing from current.
(iii) χ in physics Link 6 is the angle between the quantum chain and the lattice axis. Nothing in the parent gives χ → 0 for conduction, so this is a silent extension.
Fix: remove the "conduction = χ→0 longitudinal EM" thesis, or regrade it as [H] with a stated test, a declared seam, and the conflicts with data (TEM mode, Poynting flow outside the wire) acknowledged. The plasma-frequency, skin-depth and Drude results (CM.3, CM.5, CM.7) are standard and do not need it.

### R1-04 · major · §1 EM.12 (whole addendum) and §8 O.3
Evidence: "supplies them in the longitudinal (E-sector, pressure P) form"; "the longitudinal (E-sector) electrodynamics is now complete and reproducible"; "yields the compression (Coulomb/E) sector rigorously"; S = P v called "the longitudinal counterpart of EM's ∂ₜu + ∇·(E×H)=0".
Why: the P–v system is the acoustics of the scaffold. Under the current parent reading it is the carrier, not E. So "closing the E-sector" and "Poynting flow" (acoustic intensity P·v, not E×B) claim more than the math delivers. Energy conservation, uniqueness and the light cone of the carrier are fine, but they are statements about c, not about E. The addendum's own "c_measured = 1.0001" is also a tautology of the integrator (c = √(K/ρ) by construction).
Fix: relabel EM.12 as "dynamics and causality of the longitudinal carrier (sets c and the light cone)". Remove "E-sector", "Coulomb/E" and "Poynting" wording, or map them explicitly: S_EM = E×B is along the ray and equals the carrier's energy-flow direction per Link 6a. Update O.3 ("longitudinal electrodynamics is complete") the same way.

### R1-05 · major · §1 EM.9/EM.12.4/EM.12.5; §8 O.2 — stale relative to physics §14
Evidence: chemistry: "Full vector E/B curl (Faraday/Ampère, magnetic absolute) [O] — principal open structural item", citing "physics §14.0.6".
Why: physics §14 now says source-free Maxwell is "contained… an exact identity ([F]-grade)", with only the curl-coupling premise [H] and the sources' magnitude open. Physics §14's 2026-09-28 note also says §14.0.6's displacement definition of E is superseded by Link 6a. Chemistry cites a superseded subsection and gives a status that no longer matches the parent. This one is a downgrade, not an upgrade, but it is still silent drift across the seam.
Fix: cite §LT Link 6a and the current §14 status. Where the parent now puts the open problem is: curl-coupling premise [H]; source magnitude (α_em) [CAL]; E/B lattice run data-pending.

### R1-06 · major · §1 EM.5; EM.10 falsifier; ledger
Evidence: "Polarization as rotation (helicity) [F]"; falsifier "If circular light is not pure rotation (|S₃| ≠ S₀), helicity-as-rotation is wrong."
Why:
(a) The parent defines polarization as the direction of E (the swing) and grades the two-polarization geometry [H]. Chemistry grades it [F] and never states that polarization = direction of E, which is what Malus's law measures.
(b) |S₃| = S₀ for (1, ±i)/√2 is a definition of circular polarization, so the "falsifier" cannot fail. The same kind of evidence was retired in physics (Doubts 5a/5b).
Fix: state "polarization = direction of the transverse swing E; two states because the transverse plane has two directions [H], lattice run data-pending (inherited, Link 6a)". Drop the Stokes self-check as evidence, or label it a consistency display.

### R1-07 · major · all chemistry pages — missing "why we feel E and B"
Evidence: none of §1–§8 explains how the fields act on matter in the new picture. §3 CM.8 gives only the superseded "tilted axis → twist" story for B.
Why: this was requested, and the parent has it (Link 6a: the swing pushes a charge sideways, F = qE; a turning medium deflects only moving charges, F = qv×B; a compass aligns with the local turning). Chemistry is the volume where this matters most: voltmeters, color, photochemistry and magnets in §4 and §7.
Fix: add a short inherited box in §1 (cite Link 6a, no re-derivation), and cross-link it from §3 CM.8/CM.9 and §7 CA.9a, which already uses F = q(E + v×B) correctly.

---

## B. Grade upgrades of parent results

### R1-08 · major · §1 EM.2 heading, EM.9 rows 1–2, hub "[F] forced" strip, §2 strip "[V]"
Evidence: "Light emergence — the keystone [F]/[V]"; "reproduced by a deterministic simulation to 0.06%"; "c²=B/ρ is verified to machine precision"; the 1-D chain "c_measured = 0.99940 versus c_theory = a√(k/m) = 1".
Why: AGENTS.md: "The older '~0.06%' figure is a 1-D wave-packet check, not the evidence." In a 1-D harmonic chain c = a√(k/m) holds by construction, so it cannot fail. The parent's evidence is the 3-D five-observable margin test for c² = B/ρ ([V]), plus E2 at ±10% for the lattice-to-light link ([V]). The claim "the lattice's surviving wave is light" is graded [H] in physics Link 7. Chemistry presents the identification as forced and verified. The 0.06% figure is also the manifest headline for this volume.
Fix: grade "one surviving longitudinal speed" [V] (inherited, Link 2, five observables). Grade "that wave carries light" [H] (Link 7) with E2 PASS ±10% as support. Demote 0.06% to "illustrative 1-D check, not evidence" in the hub, §1, §2 strip, _meta and manifest headline.

### R1-09 · major · §1 EM.2 "Quantum diameter [F]" and EM.9 row "D = 2λ_C,e = 6π⁶ rₚ [F]"; hub strip "mₚ/mₑ = 6π⁵ … [F] forced (cross-volume, measured residual)"
Evidence: "The module verifies D = 6π⁶ rₚ to within +18.8 ppm, which is exactly the headline residual mₚ/mₑ = 6π⁵".
Why:
(a) D = 2λ_C,e is the electron anchor (a measured input), and D = 2πλ/A is [V] only at ±10% (E2). Absolute A/g₀ is [O] (Link 4). It is not [F].
(b) D/rₚ = π·mₚ/mₑ is an identity (physics SP: "the mass ratio in disguise"). So "verifies D = 6π⁶ rₚ" is the mass-ratio claim restated, not an independent check. Calling it a check is circular.
(c) The parent grade is [F | LOCK-NU-N], conditional on the declared mapping, with the residual [O]. Chemistry drops the conditional.
Fix: D: [L] (anchor mₑ) with the E2 [V ±10%] link. Label the 6π⁶ relation as "same residual by identity, not an independent test". Copy the parent grade tag exactly.

### R1-10 · major · §1 EM.6/EM.10, §2 CH.16 — fragile "forward predictions" for χ
Evidence: "χ(632.8 nm) = 89.892° and χ(532 nm) = 89.825°"; "If χ(632.8 nm) ≠ 89.892°… the angle law is refuted."
Why: recomputing sinχ = λ/(mD), m = ⌈λ/D⌉:
- D = 2λ_C,e (CODATA): 632.800 nm → 89.892°; 632.990 nm → 89.938° (the physics Link 6 table); 632.991 nm (the CIPM line that physics E2 uses) → 89.791°; 532 nm → 89.825°.
- D = 4.8526 pm (the value chemistry prints): 632.8 nm → 89.815°; 532 nm → 89.945°.
A 1 pm (1.6 ppm) change in λ, or rounding D to five digits, moves χ by up to about 0.15°. That is larger than the quoted differences. Chemistry also uses a different HeNe wavelength (632.8) from physics (632.99/632.991), so the "committed predictions" do not match the parent table. No measurement procedure for χ is named (what instrument measures a 0.1° tilt of a quantum chain?). Separately, Link 6a says the along-ray part is not a field, so "a small falsifiable departure from the textbook exactly-transverse wave" can no longer mean a longitudinal field component. The falsifier "if the visible angle is exactly 90°, the picture is wrong" therefore has no observable attached.
Fix: inherit the parent table (λ = 632.99/532 nm, D = 2λ_C,e at full precision) as provenance. State the sensitivity: m is an integer and the digits jump. Either name an observable (physics Doubt 6b: a measured transverse-angle *distribution*) or grade the χ values [H], not [F]/[VP-pred].

### R1-11 · minor · §1 EM.1 "[H]→[V]" charge genesis; EM.3 "Why a force exists [F]"; EM.4 "no monopoles" [F]
Why: these are qualitative identifications (charge = synchronised rotation; B as a rotation, so it has no divergence). EM.1 cites γγ → e⁺e⁻ and photon helicity, but these show only that the picture is compatible with data. The "[V]" in "[H]→[V]" has no test named on this page. The physics §14 genesis grade should be copied with its tag, not rephrased.
Fix: copy the parent grades and cite §14.0.x. Name the test behind any [V].

---

## C. Packing fraction (0.7405)

### R1-12 · major (metadata) / minor (pages) · docs/chemistry/_decl.json; registry/vp.manifest.json (lines 12, 145–146, 307, 313); docs/index.html (374–375); docs/chemistry/index.html (line 36)
Evidence: _decl "adds": ["EM-on-same-substrate", "phi_RCP=0.7405", "bonding"]. Manifest kernel "vacuum = jammed elastic solid, phi~0.7405". Primitive "jammed_c2": "form": "c^2 = B/rho (random close packing)", "pattern": "…|0\\.7405". Headline "φ_RCP = 0.7405". Hub abstract: "the close-packing fraction 0.7405".
Page usage (all correct): §2 CH.1 "the FCC packing fraction π/(3√2)"; CH.13 "FCC/HCP π/(3√2) = 0.7405, BCC 0.6802, SC 0.5236"; CH.15 "sphere packing (Kepler) → 0.7405"; §6 "FCC/HCP π/(3√2)=0.7405".
Does any derived number depend on it? **No.** In the chemistry pages 0.7405 appears only as the ordered FCC/HCP crystal packing, used for FCC metal densities (<2%). That use is correct and must stay 0.7405. The vacuum/light chain inherited from physics runs through the isostatic contact number z = 2d = 6, not through φ. No chemistry number uses φ_RCP ≈ 0.64 or φ_jam ≈ 0.63–0.64.
What changes if the correct value is used: nothing numerical in chemistry. Only the labels change: (i) the vacuum's packing fraction is φ_jam ≈ 0.64 (RCP), not 0.7405; (ii) chemistry's 0.7405 is φ_FCC, a Kepler/Hales geometric fact about crystals, not a property of the vacuum and not a module chemistry "adds" on the substrate. The manifest primitive pattern also matches "0.7405". That inflates the jammed_c2 coverage count for any volume that cites FCC packing, so the count has to be regenerated after the fix.
Fix: _decl/manifest "adds": replace "phi_RCP=0.7405" with nothing, or with "phi_FCC=0.7405 (crystal geometry)". Change the kernel substrate to "phi_jam ≈ 0.64 (RCP; z = 6 isostatic)". Remove 0.7405 from the jammed_c2 pattern. Change the headline to "c² = B/ρ (inherited); arccos(−1/3); Δ_tet/Δ_oct = 4/9". Hub: "the FCC crystal packing fraction 0.7405". Regenerate homepage and llms from the manifest (AGENTS §9.4).

---

## D. Seams and inheritance declarations

### R1-13 · major · §2 CH.2–CH.13 (whole chemistry body); hub "from a single anchor… no adjustable parameters"
Evidence: "The only observational input is the electron mass mₑ"; a₀, Ry from ħ, mₑ, c, α_em; "Aufbau degeneracy 2(2l+1)"; Thomson problem; crystal-field spherical harmonics; Sackur–Tetrode; Drude/Fermi gas; Newns–Anderson. All graded [F].
Why: these results use the standard Schrödinger/Pauli/Fermi–Dirac machinery, ħ, spin, and many [CAL] constants. None of this is derived from the jammed substrate on these pages, and no seam to physics §15 ("quantum mechanics mapping") or to textbook QM is declared. Grading textbook QM/stat-mech results [F] ("forced… zero free parameters") makes them look like consequences of the substrate. They are imported standard physics. This is silent borrowing (AGENTS §3.2 rule 5, §8.4). "Single anchor" is also contradicted by the volume's own [CAL] list: α_em, B, ν, ΔH, pKa, E°, n, spin–orbit, and more.
Fix: add a seam declaration at the top of §2: "Imported without re-derivation: non-relativistic QM (Schrödinger, Pauli, spin), statistical mechanics, point-charge crystal field; bridge to substrate = physics §15 [grade as there]". Introduce a grade or tag for "standard physics, imported" (for example [F-std] or [IMP]), or keep [F] only for pure geometry (arccos(−1/3), 4/9, π/(3√2)). Change "single anchor" to "one anchor plus the declared [CAL] set".

### R1-14 · major · §1 EM.12 — undeclared external seam (AQD)
Evidence: "Source: AQD — Axiomatic Quantized Dynamics, NOCAL v1.1, DOI 10.5281/zenodo.17423870"; theorems "QP-0002-001/002", "F-A/B/C", "QP-0002-U121", microcausality graded [F].
Why: AQD is outside the 32-volume tree. docs/chemistry/seams.json lists only physics. The microcausality and uniqueness theorems are graded [F] but have no proof or code in this repository. Under "data decides the theory", they are provenance-only.
Fix: add AQD as an outgoing seam in seams.json and _decl (relation "imports_from", grade as-is). Grade the theorems [L] (external anchor) unless the proof or code is vendored.

### R1-15 · major · repro/chemistry — cited modules absent
Evidence: pages cite vp_light_emergence.py, vp_electromagnetism.py, vp_em_field_dynamics.py, vp_light_angle.py, vp_atomic.py, vp_molecular_geometry.py, vp_crystal_field.py, vp_crystal_packing.py, vp_copper_conduction.py, vp_iron_magnetism.py, verify_chemistry.py ("32/32 PASS", "48 modules", "114-row case ledger"). repro/chemistry/ contains only the §7 modules (9 files). Paths are inconsistent (research/foundation/, code/foundation/, bare).
Why: every [F]/[V] number in §1–§6 is "reproduced by a module", but no such module is in the repository. Under the author's rule these claims are code-pending. The gate reports (phase-chm-v17/v18) check HTML structure, not the physics.
Fix: vendor the modules and ledgers under repro/chemistry/, with one path convention, and add them to repro_sha256. Until then, mark §1–§6 numeric claims "code-pending (module not in repo)".

### R1-16 · minor · docs/chemistry/index.html inherits strip; _decl.json
Evidence: hub "Inherits: R19 switch · Quantum light"; _decl "owns_terms": ["c2_brho", "kramers"]; "primitives": [..., "kramers", "fhn"].
Why:
(a) Chemistry (tier 1) inherits only physics. AGENTS §2 says R19 is first stated in dna, and no chemistry page uses R19 (0 hits).
(b) c²=B/ρ belongs to the root (physics). Chemistry "owning" c2_brho breaks single-source-of-truth.
(c) Kramers and FHN appear nowhere in the chemistry pages (0 hits). Arrhenius (CH.9) is not Kramers, and there is no FHN.
(d) "adds" lists three modules, but the contract says exactly one.
Fix: inherits strip → "Quantum light (physics)". Remove R19. Move c2_brho to uses_terms and let physics own it. Drop the kramers/fhn primitives or justify them with page text. Pick one added module (for example "EM + bonding on the jammed substrate") and regenerate the manifest counts.

### R1-17 · minor · §3 opening
Evidence: "(The physics whitepaper took the 'why Fe and not Cu' criterion as an empirical input, §14; here it is derived.)"
Why: this is a legitimate add-only statement, but the result is graded [F]/[CAL]/[O] using the standard Hund/exchange (Bethe–Slater-type, D/d > 1.5) criterion. That is imported solid-state physics, and the seam should say so.
Fix: name the imported criterion and its source in the seam line.

---

## Priority order for the author
1. R1-01/02/03: rewrite EM.4, EM.2/hub wording and the §3 conduction thesis to the Link 6a picture ([H], data-pending), and add "why we feel E and B" (R1-07).
2. R1-08/09/10: restore the parent grades (identification [H]; E2 ±10%; D anchored; 0.06% not evidence; χ sensitivity).
3. R1-12: fix φ labels in the metadata layer (no numbers change).
4. R1-13/14/15: declare the QM/stat-mech and AQD seams; vendor or mark missing code.
