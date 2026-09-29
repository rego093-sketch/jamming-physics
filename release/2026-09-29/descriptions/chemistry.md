## Summary
VP Chemistry & Electromagnetism inherits the jammed substrate and the light chain from the physics volume and adds one module: electromagnetism and bonding read on the same substrate, with chemistry built from one electron picture (the electron as a rotating quantum on the lattice). The headline, following the physics volume's §LT Link 6a, is that the electric field E is the transverse swing of the rotating quanta and the magnetic field B is the lattice's rotational response; this is graded [H] and classed as interpretation in the claims ledger (no numeric test; the lattice run that would test it is data-pending). The earlier "c² = B/ρ reproduced to 0.06%" is now stated as a 1-D consistency check (identity), not evidence, and φ = 0.7405 is labelled as the FCC crystal value, not random close packing. The chemistry results (Bohr radius, Aufbau order, conduction, band-edge colours, d-band catalysis) are standard physics evaluated from measured and calibration inputs; the application chapters are engineering estimates.

## What changed in this version (2026-09-29)
**Corrections**
- Headline changed: the retracted reading "longitudinal E, transverse B [F]" and "light = the only longitudinal wave" withdrawn on the hub and §1; E = transverse swing, B = lattice rotational response, two polarizations, |E| = c|B|, and why each is felt (F = qE; F = qv×B, compass) stated, graded [H], synced with physics §LT Link 6a.
- The 0.06% figure relabelled as a 1-D chain consistency check (holds by construction, depends on packet width); evidence for c² = B/ρ referred to the physics volume's 3-D isostatic test and E2 (hub, §1, §2).
- φ = 0.7405 relabelled as the FCC crystal value (not RCP) across manifest, _decl, homepage, concepts, corpus guide and build tools.
- §2: "single anchor" clarified as one physical picture; measured inputs mₑ and α_em plus [CAL] calibration inputs; results are standard quantum mechanics evaluated from those inputs.
- §3: the "χ→0 longitudinal EM mode" reading of current withdrawn (conduction numbers stand); iron's moment ≈ 2.2 μ_B graded [O]; the 7/7 magnetism count uses an empirical threshold and is [CAL].
- §4: band-edge rule identified as standard solid-state physics; CdSe/cadmium-red pigment statement corrected.
- §5: CT.4–CT.6 (resonance reading refuted by CT.7) superseded; ΔG_H values are mostly DFT literature values [CAL].
- §6: application chapter graded as estimates (page badge [F] withdrawn; ledger [F?]); magnetic-amplitude desalination refuted (≈10⁻² k_BT per channel).
- §7: headline efficiency 2.6–4.4% identified as mechanical; heat-to-electricity is 1.35–2.27% (0.21% bare device); India 30 TWh/yr figure is a projection [H], not [CAL]; payback rests on an assumed capital cost; material inputs awaiting sources.
- §7 black copper: converter verdict recomputed with CuO (p-type semiconductor, ~204 µV/K) instead of copper metal (1.8 µV/K): the ~100 nm coating holds 3×10⁻⁵ K (still not a converter, reason corrected); bulk CuO ZT ≤ 0.05; a Cu/CuO junction is a real thermocouple (~202 µV/K); original module kept for the record. The VP χ-conversion proposal is kept as [O] with bench test BC4 pre-registered; the closed-store vs cold-side design tension recorded (rejected-heat handling left to field engineering).
- Open-items register (axO): extended with the E/B sector, the unrecovered §1–§6 code status and the §7 device comparison; reconstructed re-examination shows all four items stay open, and the stated bond-order correlation r = +0.18 re-runs at +0.10 (not reproduced).
- Correction notes (lt-note) on all 9 pages.
- R19 kernel no longer claimed by this volume (_decl).

**New experiments and results**
- LE1 heat vs straight motion (light angle): near-longitudinal threshold hc/D = mₑc²/2 = 255.5 keV; thermal peak at χ = 45° needs ~8.4×10⁸ K and stays isotropic; a straight electron reaches it at ~0.36 MV; 511 keV light at χ = 30°; P1–P4 true; X-ray sawtooth of the m-chain formula flagged [O].
- BC1 why black / electron tracking: P1, P3, P4 PASS; P2, P5 FAIL (no net charge current without a junction).
- BC2 black-Cu boundary IR → current: P1–P6 PASS; isothermal boundary gives zero (detailed balance); 67 °C store ~6 µW/m² at ideal yield; needs a cold side.
- BC4 radiative vs conductive voltage at matched temperature: bench protocol pre-registered (standard null 0 V, systematic bound 0.2 µV, threshold 3 µV with sign reversal); not run.
- BC5 IR rectenna (angle route): P1, P3, P4, P5 PASS; P2 cutoff FAIL (1 THz passes 7%, predicted < 5%); 67 °C store ~26 mW/m² (~4000× BC2), 500 °C ~23 W/m²; bottleneck is the small-signal diode (≥ 30 THz).
- BC6 rectenna at realistic store temperatures (300–600 °C): P1–P4 PASS; 3–5% of net flux (square-law cap ~6%); a ZT = 1 thermoelectric gives ~3× more; bulk CuO thermoelectric 0.04–0.38 kW/m².
- ESS1 hot-surround absorber: P1, P3, P4 PASS; P2 FAIL (front face radiates the store to the sky at night).
- ESS2 cavity in hot sand: P2, P3, P4 PASS; P1 accumulates FAIL; absorber-side loss 68 → 0.9 kWh/30 d, effective absorptance 0.998 [V mech]; the limit moves to store insulation (ΔT = η·α·Ḡ·A_coll/UA [F]).

**Relabelled grades / reading rule**
- E/B [H]; 0.06% → consistency check; application chapters → estimates; iron moment [O]; magnetism count and ΔG_H [CAL]; India figure [H]; black-Cu χ-conversion [O].

**Reproduction package changes**
- Author's DOI package v1.0 (2026-06-14) vendored under repro/chemistry/legacy_v1_0_2026-06-14/: SHA-256 79/79, verify_chemistry 39/39 run and deterministic, numeric-drift gate PASS, applications 9/9; restores 36 of 37 missing cited scripts; every decimal number on the current §1–§6 pages but two is present in the package.
- New module repro/chemistry/repro/chemistry/07-low-grade-waste-heat-electricity/vp_blackcu_cuo_correction.py; reconstructed repro/chemistry/ax-o-open-items-register/vp_open_items_reexam.py (electron-affinity dataset absent, carried not re-run).
- New experiment folders repro/chemistry/experiments/{LE1, BC1, BC2, BC4, BC5, BC6, ESS1, ESS2}; reviews under reviews/chemistry/ and a cosmology–chemistry synthesis review.

**Site/metadata**
- Manifest headline, adds (phi_FCC) and homepage synced; corpus link audit repaired stale repro and site URLs; Highwire citation meta regenerated; registry hashes and lineage updated.

## Claim status (claims ledger)
6 rows: interpretation 1 · identity 2 · open 3.
- EM on the jammed substrate: E = transverse swing, B = lattice rotation (headline) — interpretation — no numeric test; reviewers note §1 EM.4 text and textbook results graded [F] as over-grading.
- c² = B/ρ "reproduced to 0.06%" — identity — packet-width dependent (0.955–0.9995 for σ = 2–20 sites); not agreement with any datum.
- Case harness 32/32 PASS over a 114-row case ledger — open — ledger records verify_chemistry.py and cases_fixed.csv as not in the repo; the vendored v1.0 package now carries a verify_chemistry.py that runs 39/39.
- §7 low-grade waste heat → electricity — open — η_mech 2.65–4.44%, η_elec 1.35–2.27%, device alone 0.21%; no hardware data compared.
- Black copper converts infrared into directed current (VP χ-conversion) — open — BC1 no net current without a junction; BC2 zero at equal T; BC6 standard rectenna 3.0–5.0% of net flux; only BC4 (bench, not run) discriminates.
- LE1 near-longitudinal threshold hc/D = mₑc²/2 = 255.5 keV — identity — algebra given D = 2λ_C,e; no measured photon angle compared.

## Open items
- E/B lattice run (rotating-grain lattice showing the transverse swing and rotational response) — data-pending, [H].
- BC4 bench test of black-Cu χ-conversion (radiative vs conductive voltage at matched temperature) — pre-registered, needs a bench; proposal stays [O].
- X-ray sawtooth of the m-chain angle formula (100 kV → 58°, 255 kV → 90°) [O], testable by measurement.
- Iron moment (band effect) [O]; absolute catalytic rates, promoters, current densities and the OER scaling break [O].
- Open-items register: Morse β vs bond order (r = +0.10, stated +0.18 not reproduced); ideal/measured strength ratio not constant; SEMF magic-number sign change; electron-affinity check not re-runnable (dataset absent).
- §7: comparison with a published thermomagnetic generator data-pending; closed-store vs cold-side design tension left to field engineering.

## Reproduction
The ZIP contains docs/chemistry/ (the published HTML pages), repro/chemistry/ (code and data), LEDGER.json (this volume's claims-ledger rows), CORPUS_GUIDE.md and MANIFEST.sha256 (SHA-256 of every file).
Main checks (Python 3 with numpy, no network needed):
- `python3 repro/chemistry/legacy_v1_0_2026-06-14/VP_Chemistry_EM_DOI_Package_v1/core/code/verify_chemistry.py` — the v1.0 verification harness (see that package's README.md and SHA256SUMS.txt).
- `python3 repro/chemistry/ax-o-open-items-register/vp_open_items_reexam.py` — open-items re-examination.
- `python3 repro/chemistry/repro/chemistry/07-low-grade-waste-heat-electricity/vp_blackcu_cuo_correction.py` and the other §7 modules in that folder.
- Experiments: `le1_run.py`, `ess1_run.py`, `ess2_run.py`, `bc5_run.py` and the BC1/BC2/BC6 run scripts in repro/chemistry/experiments/<name>/ (each with PREREG.json and RESULT.json); BC4 holds the bench protocol and `bc4_predict.py` (writes PREDICTION.json; the bench run itself is not done).
Deterministic scripts use SEED = 19 where randomness is involved.

## Citation and links
- Site: https://jamming-physics.org/chemistry/
- Concept DOI: 10.5281/zenodo.20680540
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
