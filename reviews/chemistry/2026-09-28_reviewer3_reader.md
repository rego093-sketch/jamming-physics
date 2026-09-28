# Chemistry volume — Reviewer 3 (reader lens) — 2026-09-28

Scope: `docs/chemistry/index.html` + 8 sub-pages (§1–§7 + open-items register). Lens: an ordinary AI / educated non-specialist reading once, top to bottom. No files under `docs/` or `repro/` were edited.
Cross-checked against the physics volume (`docs/physics/lt-light-chain-doubts-and-resolutions/` Link 6a, `docs/physics/10-…`, `docs/physics/14-…`, `docs/physics/01-…` updates dated 2026-09-28), `AGENTS.md`, and `registry/vp.manifest.json`.

Severity: **critical** = a reader will leave holding a claim the corpus itself has withdrawn, or cannot tell input from output; **major** = a reader is likely to misread status or lose the thread; **minor** = friction / polish.

---

## A. What E and B are (the central reader question)

### R3-01 — critical — §1 EM.4 states the superseded "longitudinal E, transverse B" reading as [F]
Page: `docs/chemistry/01-electromagnetism-jammed-lattice-light/`
Evidence: heading "EM.4 The E/B geometry: longitudinal E, transverse B [F]"; "the electric field is the force directed along the light (propagation) direction; the magnetic field is the force directed at 90° to it."
Physics now says the opposite and marks the old reading withdrawn: physics §LT Link 6a "Correction to earlier editions. Earlier editions called the straight, along-the-ray component 'the electric field' … Measurement does not allow that. … No light oscillates along its own direction of travel in vacuum." and physics §14 "Earlier text that took the along-ray component as E is superseded." Physics also grades the new identification **[H]**, not [F].
Fix: replace EM.4 with the current account and grade it [H]. Suggested wording:
> **EM.4 What E and B are on the lattice, and why we feel them [H]** (current reading; inherited from physics §LT Link 6a). A light wave on the jammed lattice has three parts. (1) The *carrier*: the one surviving elastic branch, a longitudinal compression wave whose speed is c² = B/ρ. It sets the speed and the direction energy flows (the ray), but it is **not** a field. (2) The *electric field E*: the sideways (transverse) swing of the rotating quanta that the carrier carries. (3) The *magnetic field B*: the neighbouring grains turning in answer to that swing. E and B are both perpendicular to the ray and to each other, |E| = c|B|, and energy flows along the ray (S = E × B). **Why we feel E:** a charge (a quantum with synchronised rotation) is pushed sideways by the passing swing, F = qE — this is what a voltmeter, antenna or retina registers, and a polarizer passes only the swing along its axis. **Why we feel B:** a charge at rest is not dragged by a turning medium, but a moving charge is deflected sideways, F = qv × B; a compass needle, whose own quanta turn together, lines up with the local turning. Near a charge at rest only the swing strain remains (static E); near a steady current only the turning remains (static B). *Earlier editions of this chapter called the along-ray component "E"; that reading is superseded.*
Keep the |B|/|E| = v/c line only as the moving-charge result, and say which it is.

### R3-02 — critical — "light is one longitudinal wave" is the headline on hub, §1, §2, yet §1–§4 also say light is transverse; the reader is never told how both are true
Pages: hub; §1 lede + EM.2 + EM.6; §2 cited box + CH.6/CH.15; §3 CM.1; §4 CC.0/CC.8.
Evidence: hub "leaving a single longitudinal wave at c² = B/ρ"; §1 "leaving one longitudinal wave, light, at c² = B/ρ"; §2 box "light is the single longitudinal wave"; vs. §1 EM.6 "its transverse, propagating part is light"; §2 CH.6 "light as rotational transverse wave"; §3 CM.1 "Light is a transverse electromagnetic wave"; §4 "visible light is the transverse electromagnetic wave".
Fix: everywhere the headline appears, write "the one surviving elastic branch is longitudinal and sets c² = B/ρ; light is the transverse swing that this carrier carries." Hub sentence suggestion: "…leaving a single longitudinal elastic branch at c² = B/ρ. That branch is the carrier: it fixes the speed of light. Light itself — the electric and magnetic fields — is the transverse swing of the rotating quanta that the carrier carries (§1 EM.4)."

### R3-03 — major — §1 EM.6, EM.12, register O.3 and §3 CM.1/CM.4 build on "longitudinal E-sector electrodynamics" and "electricity = longitudinal EM wave (χ→0)" without reconciling with the correction
Pages: §1 EM.6, EM.12.1–12.5; §3 CM.1, CM.4, CM.14; register O.2/O.3.
Evidence: EM.6 "Its longitudinal part (∇·u, compression = deficit) is the static Coulomb field"; EM.12.4 "the longitudinal (E-sector) electrodynamics is now complete"; O.3 "The longitudinal electrodynamics is complete"; CM.4 "This longitudinal disturbance is the current … straighter even than a γ-ray."
Under physics Link 6a, an along-ray oscillation "belongs to the scaffold, which carries energy but is not itself a radiating field." The reader now holds two incompatible pictures. Also, mainstream physics places the energy of a DC circuit in the field around the wire (Poynting), not inside the metal; the chapter contradicts that without flagging it.
Fix: (a) rename EM.12 "Dynamics of the carrier (scalar pressure P): wave equation, energy flow, light cone" and state that it governs the carrier and hence the speed/causality, not E itself; (b) re-grade "electricity = χ→0 longitudinal EM wave" and "signal runs through the atomic-internal quanta" as [H] and add one sentence acknowledging the mainstream account (energy flows in the field around the conductor) and what observation would separate the two; (c) update register O.2 "Absolute vector sector": physics Link 6a now supplies a lattice reading of Faraday/Ampère–Maxwell ("a changing swing drives the medium to turn, and a changing turn drives the swing") at [H]; the register should cite that and keep the *magnitude* open.

### R3-04 — major — 0.06 % is presented as the evidence for c² = B/ρ
Pages: hub (twice), §1 lede + EM.2, §2 cited box, manifest headline.
Evidence: "reproduced by a deterministic simulation to 0.06%"; EM.2 shows it is a 1-D mass–spring chain whose closed-form speed is a√(k/m) — the check measures leapfrog accuracy, and "c²=B/ρ is verified to machine precision" is an identity for that chain. AGENTS §2: "The older '~0.06%' figure is a 1-D wave-packet check, not the evidence" (evidence = five 3-D observables, test E2 ±10 %).
Fix: hub/§1 lede: "c² = B/ρ is the speed of the one elastic branch that survives at the isostatic point; the physics volume verifies this on five observables in 3-D (test E2, ±10 %). A 1-D wave-packet check here reproduces the chain's own closed-form speed to 0.06 % — a numerical sanity check, not the evidence." Change the §2 cited-box grade text accordingly.

## B. "Single anchor": input vs output

### R3-05 — critical — "single anchor" is used in two senses and the reader cannot see inputs vs outputs
Pages: hub, §2 CH.2/CH.15, register.
Evidence: hub "From one anchor, the electron as a rotational dent…" (a *picture*); §2 CH.2 "The only observational input is the electron mass mₑ (the anchor). With the EM coupling αₑₘ [CAL] and π…" (a *measured number*, immediately followed by a second measured input). The body then uses many further [CAL] inputs (spectroscopic B, ν; ΔH; pKₐ; E°; n; spin–orbit; ε_d; ΔG_H; E_g; Curie points; D/d ratios). Physics now states "It is one of two measured anchors: the other is the electron mass" (λ_anchor = 632.99 nm) — so even at the substrate level there are two anchors.
Fix: add at the top of §2 (and a one-line pointer on the hub) an explicit input/output table:
> **What goes in, what comes out.** *Measured anchors (inherited from physics):* electron mass mₑ (fixes the quantum diameter D = 2λ_C,e) and the He–Ne length anchor 632.99 nm. *Measured constant used, not derived:* αₑₘ ≈ 1/137 [CAL]. *Pure geometry, no input:* 109.47°, 4/9, packing fractions, shell integers. *Per-substance measured inputs [CAL]:* bond enthalpies, spectroscopic constants, pKₐ, standard potentials, band gaps, d-band centres, Curie temperatures. *Outputs:* a₀, Ry (from mₑ, αₑₘ, ħ, c — the textbook formulas), and the forced results listed in CH.14.
State plainly that "anchor" in the hub means the *conceptual* starting picture (electron = rotational dent), and that the *numerical* anchors are the two above.

### R3-06 — major — "forced / derived" is used for textbook results computed from measured inputs; reader cannot tell VP-new from standard physics
Pages: hub, §2, §3, §4, §6.
Evidence: §2 "Daniell cell E°cell = 1.10 V (matches measured) … [F]" (a difference of two measured E° values); "With K_w = 10⁻¹⁴, pure water has pH 7 [F]"; a₀ "Δ +0.0000%" (exact by construction given α, mₑ); §3 Bethe–Slater D/d criterion (empirical 1930s curve, threshold ≈1.5, measured D/d) presented as "here it is derived … no fitted magnetic parameter [F]"; §4 particle-in-a-box, band-gap edge; §6 Hammer–Nørskov, Hori, Peterson–Nørskov. Hub: "derives both chemistry and electromagnetism using only π-geometry and the electromagnetic inverse-square law".
Fix: add a column or tag to each ledger row: **VP-specific** (e.g., c from the lattice, charge = synchronised rotation, propagation angle χ) vs **standard physics re-run in VP language** (Drude, Bethe–Slater, Sabatier/d-band, Sackur–Tetrode, Nernst). Re-grade Daniell 1.10 V, pH 7, and the 7/7 magnetism table as [F given CAL]. Soften hub: "derives the electromagnetic foundation from the lattice and re-expresses standard chemistry on it, using measured constants where marked".

## C. Contradictions and superseded content

### R3-07 — major — §5 CT.4–CT.6 (refuted amplitude-wavelength resonance) are still written as live content; CT.6 still asserts it
Page: `docs/chemistry/05-platinum-catalysis-d-band-descriptor/`
Evidence: CT.5 "This makes the hypothesis actionable for electrode design"; CT.6 [F]/[CAL] "platinum's catalytic efficiency — read in the VP picture as electron-amplitude-wavelength resonance — is what makes the low-voltage electrolysis … feasible." The refutation arrives only in CT.7. Page chip reads "[H] hypothesis" although the page's final verdict is the established Newns–Anderson/d-band picture.
Fix: put a banner on CT.4, CT.5 and the CT.6 closing paragraph: "**Superseded (refuted in CT.7).** Retained as the record of a tested hypothesis." Delete or rewrite the CT.6 sentence: "platinum's efficiency comes from its d-band energy (CT.8); the amplitude-wavelength reading is refuted." Change the page chip to e.g. "[CAL]/[F?] established · [H] refuted".

### R3-08 — major — propagation-angle falsifier disagrees with physics and cannot be reproduced from the stated D
Pages: §1 EM.6/EM.10, §2 CH.16.
Evidence: chemistry "χ(632.8 nm) = 89.892°"; physics §LT table "632.99 nm … 89.9378°" (I₂-stabilised He–Ne anchor). Using the D printed in chemistry (4.8526 pm / 4852.6 fm) gives χ(632.8 nm) ≈ 89.815°, not 89.892° (89.892° needs D = 2λ_C,e to full precision). Physics also now states "the D-sensitivity is up to ≈0.17° per 0.03%" and "the two-line ratio is arithmetic, so it is not evidence". Reader also never gets m defined ("sinχ = λ/(mD)" with m = ⌈λ/D⌉).
Fix: use the physics anchor line (632.99 nm → 89.9378°) or state both with the vacuum/air wavelength difference; define m = ⌈λ/D⌉ and D = 2λ_C,e exactly; add physics' sensitivity caveat; re-grade from [F] falsifier to "forward map, [F] given D; sensitivity 0.17° per 0.03 % in D".

### R3-09 — minor — sign flip of the 6π⁶ residual in one paragraph
Page: §1 EM.2. Evidence: "verifies D=6π⁶ rₚ to within +18.8 ppm, which is exactly the headline residual mₚ/mₑ = 6π⁵ (-19 ppm)". Fix: explain the sign convention (ratio vs its inverse) or use one sign; also define rₚ (the stiffness-shell fixed point, "x̂ = 2/π") before use.

### R3-10 — minor — "infinitely rigid" grains vs a finite bulk modulus is not explained
Pages: hub, §1 EM.2. Evidence: hub "an infinitely rigid, fully packing jamming lattice"; EM.2 "[F, axiom] Infinitely rigid, fully packing quanta". A reader asks how infinitely rigid grains give finite B and a finite c. Fix: one sentence: "The grains themselves do not deform; the lattice's stiffness B comes from how the packing's contacts transmit load, which is finite." Also "Rotation (temperature) drives the contact number…" — "temperature of the vacuum" is undefined; add a clause.

### R3-11 — minor — 0.7405 labelled φ_RCP in machine files; hub wording invites confusion with the substrate's jamming fraction
Pages: hub ("the close-packing fraction 0.7405"); `docs/chemistry/_decl.json` ("phi_RCP=0.7405"); `registry/vp.manifest.json` headline/adds.
The pages themselves correctly say FCC/HCP π/(3√2). Fix: hub "the crystalline (FCC/HCP) close-packing fraction 0.7405 — not the vacuum's random-close-packing jamming fraction ≈ 0.64"; rename `phi_RCP` → `phi_FCC` in `_decl.json` and the manifest (regenerate, don't hand-edit).

## D. Separation of physics / verified / applications / open

### R3-12 — major — application and economic sketches carry [F]/[V] page chips; a reader will read them as verified results
Pages: §6 (chip "[F] forced"), §7 (chip "[V] verified").
Evidence: §6 CA.5 "a 1 m³ store holds ~46 kWh … [F?]", "τ≈5.4 days [F?]"; §7 CA.12 "Across India's ~110 million room air-conditioners this is of order 30 TWh/yr [CAL]" (a projection labelled *calibration*); "a 1 MW data centre … payback of ~4–6 years [H]" (an economic estimate labelled *hypothesis*); §7 "[V]" = "simulation-measured" of textbook thermodynamics, whereas AGENTS defines [V] as "passed a test built to falsify it against external data".
Fix: (a) add a banner at the top of §6 and §7: "**Applications chapter.** Physics results here are standard thermodynamics/surface science re-used; device sizes, fleet totals and payback figures are engineering sketches, not verified results, and nothing here tests the VP substrate." (b) introduce a distinct tag, e.g. **[APP] engineering estimate**, for CA.5 storage sizing, CA.6 net-watt figures, CA.12 fleet/payback; do not use [CAL] or [H] for them. (c) change page chips to "[APP] application · [O] refuted mechanisms". (d) either align the chemistry legend's [V] with AGENTS ("verified against external data") or rename the simulation grade (e.g. [S] simulated).

### R3-13 — major — grade legend is not on the hub, differs between pages, and differs from AGENTS
Pages: hub (no legend); §2 legend (F, F?, CAL, V, O); §6/§7 legend adds H and "[O] open / refuted"; §1 uses [VP-prediction]; AGENTS uses F/V/L/O.
Evidence: §6/§7 "[O] open / refuted" — AGENTS: "[O] is an honest gap", not a refutation; §7 CA.9 grades three *refuted* mechanisms "[O]".
Fix: one legend on the hub, linked from every page; map chemistry grades to corpus grades ([CAL] ≈ [L] anchor); add a separate **[R] refuted** tag so refuted ≠ open.

### R3-14 — major — open-items register is incomplete although it claims "every [O]/[H] item"
Page: `docs/chemistry/ax-o-open-items-register-what-is-honestly/`
Evidence: "This appendix consolidates every [O] / [H] item carried in this volume". Missing: §7 [H] "rotation-amplitude → electric field" generator and device/economic projections; §6 [O] microkinetics, promoter effects, OER scaling-relation circumvention, CO₂RR C–C coupling; §2 [O] lone-pair magnitude, absolute rates/stereoselectivity, absolute pKₐ/E°; §3 [O] itinerant (non-integer) moments; §4 [O] multi-band colour; §5 surviving testable claim (quantum-confinement oscillation). The register cites "the retracted √(2.5) rule", which appears nowhere else in the volume.
Fix: add rows O.4 "Applications" and O.5 "Refuted (kept for record)" covering the above; add one line explaining the √(2.5) rule or drop the reference.

## E. Structure and rendering

### R3-15 — major — raw LaTeX leaks in inline text on 7 of 9 pages
Evidence (counts of leaked tokens: §1 51, §2 34, §5 10, §6 10, §3 5, §4 5, register 7): "mathbf B", "90^∘", "tfrac32 R", "mathrm pKₐ", "barλ₍C,e)", "Δ G₍mathrm H^)", "[Ti(mathrm H₂mathrm O)₆]³⁺", "20300 mathrmcm⁻¹", "n_dle 5", "αge0.98", "N₂ + 3H₂ leftharpoons 2NH₃", "εₐ rightarrow ε_d", "CO₂⁽bullet-)", "expansion 0.00 le cτ", "tₐᵣᵣge dist/c", "ointmathbf S", "5.16 AA" (Å). Subscripts also render as "λ₍C,e)" with mismatched brackets. Display equations (SVG, all 100 % present) are fine.
Fix: re-run the inline-math conversion (Pandoc → Unicode) with \mathbf, \mathrm, ^\circ, \tfrac, \le/\ge, \rightleftharpoons, \rightarrow, \AA, \bullet handled; add a gate that fails the build on `mathbf|mathrm|\^∘|tfrac|leftharpoons|rightarrow| AA\b`.

### R3-16 — major — markdown asterisks mangled (italics swallowed "*" in adsorbate notation; stray "*")
Pages: §5, §6 (CO₂ section), §4, §1.
Evidence: "^CO", "^COOH", "^*OCHO" (should be *CO, *COOH, *OCHO — the "adsorbed" star); "(Chapter CT, §CA).*"; §4 "subtracts* selected wavelengths … read through the size of a gap.*"; §5 "geometric* form … catalysis.*"; §1 "the known residual of the theory*".
Fix: escape adsorbate stars (\*CO) in source and rebuild; remove stray asterisks.

### R3-17 — major — every page from §3 on opens with a truncated sentence fragment; chapter codes are never mapped to § numbers
Pages: §3 "(chemistry). Status grades as in Chapter EM."; §4 "(crystal field), and Chapter CM."; §5 "Chapter CM. Related to the VP Application whitepaper"; §6 "CT (catalysis), EM (electromagnetism). Status grades:"; §7 "CA (chemistry applications), CM (conduction/magnetism, Chapter 3)."
The "Builds on: …" lead-in was lost in conversion. Pages cross-reference "Chapter EM / CH / CM / CC / CT / CA", but the hub and nav use §1–§8 only.
Fix: restore "Builds on: Chapter EM (§1), Chapter CH (§2) …"; add a line on the hub: "Section codes: EM = §1, CH = §2, CM = §3, CC = §4, CT = §5, CA = §6–§7, O = §8."

### R3-18 — minor — section-number collisions and an orphan section
Pages: §6 and §7. Evidence: §6 has "CA.8 Falsification criteria", "CA.9 Reproducibility"; §7 reuses "CA.8 The question", "CA.9 Three refuted mechanisms" … "CA.13". §6's CO₂ section ("Application: CO₂ Electrocatalytic Reduction") is unnumbered, appended after the master ledger and reproducibility, and absent from ledger CA.7. Hub contents for §6 does not mention CO₂ though the hub abstract headlines "why copper alone turns CO₂ into hydrocarbons".
Fix: renumber §7 as CW.1–CW.6 (or CA.10+); number CO₂ as CA.7a and move it before the ledger; add its rows to CA.7.

### R3-19 — minor — hub gaps: inheritance chip, contents blurbs, abstract coverage, counts
Page: hub. Evidence: "Inherits: R19 switch · Quantum light" — R19 appears nowhere in the volume and the manifest lists `inherits: ["physics"]` (AGENTS: R19 first stated in dna). Contents blurbs are cut mid-word ("the Coulomb 1/r², the", "arcco", "set which wavelengths tr"). Abstract does not mention §6 applications or §7 waste heat. Module counts disagree: hub "48 … modules, six case ledgers"; §2 "Thirty … modules", "32/32 PASS", ledgers of 114 + 16 rows; §6 "Six … modules and three case ledgers (29 rows)".
Fix: chip → "Inherits: VP Theory (substrate, c² = B/ρ, mₑ and 632.99 nm anchors)"; complete the blurbs; add an abstract sentence: "Two application chapters (§6–§7) re-use standard surface science and thermodynamics, refute three device mechanisms, and size one thermomagnetic harvester as an engineering estimate"; state one reconciled module/ledger count.

### R3-20 — minor — undefined terms/symbols before use
Pages: §1, §2. Evidence: "physics §SP", "m-chain", "A" (lattice amplification), "AQD", "NOCAL v1.1", "QP-0002-002", "Pauli–Jordan function", "K" (vs B), "[CAL]" (used in EM.0 before any legend), "rotational dent" (never defined in plain words), untranslated link text "용어" in the cited boxes of §1 and §2.
Fix: a short glossary box at the top of §1 (rotational dent = the local deficit left by one synchronised rotation; K = B; m = ⌈λ/D⌉; AQD = the external axiomatic-dynamics source, with DOI); replace "용어" with "Glossary".

### R3-21 — minor — lede overstates a result the body leaves open
Page: §3. Evidence: lede "in iron an exchange-split d-band leaves a net moment ≈ 2.2 μ_B"; body CM.13 "(The metallic moments are non-integer — Fe 2.22 … an itinerant/band effect marked [O]…)". The body derives only the Hund count (4.90 μ_B) and the class. Fix: lede "…leaves unpaired d-rotations that align into a ferromagnet (the measured 2.2 μ_B moment is itinerant and open, [O])". Also CM.10 table omits Cr while CM.12 includes it — add Cr (3d⁵4s¹, 5 unpaired).

---

## Navigation check (pass)
Hub links all 8 sub-pages; prev/next chain §1→§2→…→§7→§8 is complete and in order; §8 has no "next" (correct). All 100 % of display-equation SVGs referenced exist.
