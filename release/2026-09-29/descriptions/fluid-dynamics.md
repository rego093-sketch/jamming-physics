## Summary
The Configured Continuum is the fluid-dynamics volume of the VP corpus. It inherits the jammed substrate from the physics volume and adds one module: continuum flow on the jammed medium, with the balance laws obtained from the particle arrangement. Mass and momentum balance follow exactly (Irving–Kirkwood identity applied to the jammed medium, [F]); the step to Navier–Stokes needs a Newtonian closure, which the pre-registered test NC1 finds on the unjammed side of the margin in a 2-D soft-disk model (flow index 0.96–1.07, viscosity rising 21.8× toward φ_c ≈ 0.846, yield stress above; [V mech]). The claims ledger classes this headline as interpretation: it is a standard soft-disk rheology result, and no external fluid data are used anywhere in the volume. The volume's stated key result — the three-sphere (C₃) structure forcing co-rotation and a one-axis through-flow that closes in 3-D (82 = 81 + 1, carried from the physics volume) — is a reduced test ([F] geometry, [V mech] in-model chain) and is classed open in the ledger. Global regularity of Navier–Stokes and the 3-D Onsager anomaly are not claimed.

## What changed in this version (2026-09-29)
**Corrections**
- Scope and key-result note added to the hub, §01 and §14: the volume's strength is stated at what the code supports (balance laws [F]; Newtonian closure [V mech, 2-D]; three-sphere C₃ → one-axis through-flow as a reduced test; dissipation by events [V mech]; length selection data-pending; global regularity not claimed, no reduction shown). Headline changed accordingly.
- Grade vocabulary mapped onto corpus grades: [LOCK] → [L]; [DERIVE] → [F] for identities and [V mech] for in-model runs; [GATE] → [O]. Checks that hold by construction (RCCI identity, 3-D Gauss closure, metriplectic saturation, event-RG plateau) relabelled as consistency checks, not tests.
- §03: the Newtonian regime is placed below the isostatic margin (unjammed side, z = 2.1–3.5); at the margin (z ≈ 3.98) viscosity diverges and the flow shear-thins (n = 0.46); the earlier contradiction between §3 and §6 is resolved.
- §06: Newtonian-closure gate tested (NC1); the derivation covers pair forces, and the three-body term's effect on the closure is [O].
- §08: sign of the viscous term in the amplitude equation corrected (it damps the k² term); the selected length comes from the prescribed forcing annulus; nonlinear run gives β̂ = 0.464 (not 0.501), finer run 0.424; β ≈ 0.5 is established only on the synthetic data of the JFM package (its small DNS demo gives 0.000 at N = 64); DNS confirmation data-pending.
- §09: 3-D solver energy conservation corrected to about 10⁻⁸ in inviscid runs (not 10⁻¹⁶), divergence about 4×10⁻¹²; the stochastic budget check leaves a 33% residual, not 2%; the avalanche exponent change 1.60 → 1.46 is a grid-size effect at fixed ν (estimator changed after the N = 64 run), not a Reynolds trend; metriplectic saturation is [F in-model]; the PRL ensemble CSV is under clarification (n_mergers + N_final ≠ N); 3-D Onsager anomaly not claimed.
- §11: marked as carrying the key result, with its seams to the dna and physics volumes declared; the full 3-D run (U₃ coupled to 3-D Navier–Stokes) stated as a computational limit.
- Correction notes (lt-note) on 8 pages: hub, 01, 03, 06, 08, 09, 11, 14.
- Declarations: the R19 kernel is no longer claimed by this volume (_decl); primitives aligned.

**New experiments and results**
- NC1 Newtonian closure (pre-registered; 2-D bidisperse harmonic disks, N = 512, Lees–Edwards shear, SEED = 19): P1 Newtonian below φ_J PASS; P2 η grows toward φ_J PASS (21.8×, φ_c = 0.846); P3 yield stress above φ_J PASS; P4 two η routes FAIL as registered (protocol error: body-force amplitude drove the run nonlinear); post-hoc non-gating rerun ratio 0.96 (needs fresh pre-registration); P5 athermal Bagnold control PASS (n = 2.01).
- C3E1 three-sphere directed ejection, dynamical 3-D test (pre-registered): P1, P2, P3, P5 (balance sub-criterion), P6 FAIL; P4 formal PASS. Author review: independent-model test without the volume's three-body kernel U₃, so not a test of the volume's mechanism; numbers kept as a record.
- ONS1 independent re-implementation of the forward-merger point-vortex gas: ε_sat ≈ 0.2 NOT REPRODUCED (P1 undefined, P2 and P3 FAIL); Pillar IV ε_sat ≈ 0.2 graded [O]; the shipped PRL ensemble CSV found internally inconsistent (n_mergers + N_final ≠ N in all 45 rows). Author review: a different model from Pillar IV's metriplectic_vortex.py.

**Relabelled grades / reading rule**
- Corpus grade mapping above; ε_sat ≈ 0.2 → [O]; Newtonian closure → [V mech, 2-D]; three-sphere frustration and 3-D closure [F], merger–Ekman–outflow chain [V mech].

**Reproduction package changes**
- transition_dp*.py no longer write to a hard-coded absolute working path; validate_all.py imports resolve (5/5 PASS); verify_rotcore.py default path fixed (PASS, 2.8×10⁻¹²).
- Author's unpublished JFM length-selection package vendored for reference under repro/fluid-dynamics/jfm_length_selection_v4 (with a note: β ≈ 0.5 is on synthetic data).
- New experiment folders repro/fluid-dynamics/experiments/{NC1_newtonian_closure, C3E1_three_sphere_directed_ejection, ONS1_adg_vortex_gas}.
- Three independent reviews added under reviews/fluid-dynamics/ (Navier–Stokes logic; code and data; reader).

**Site/metadata**
- Leaked LaTeX removed across 36 pages (\ref → chapter links, \S, \emph, \dots, verbatim → pre, \end{document}, stray brackets); 3 stray '<' escaped.
- Corpus link audit repaired stale GitHub repro and site URLs; Highwire citation meta regenerated from the manifest; homepage card and manifest headline updated; corpus integrity checks added to the gate.

## Claim status (claims ledger)
7 rows: interpretation 1 · open 3 · identity 2 · anchor-restatement 1.
- Balance laws from the arrangement; Newtonian closure below the jamming margin (headline) — interpretation — NC1 P1–P3 PASS, P4 FAIL as registered (post-hoc 0.96); in-model only, no external rheology data.
- Three-sphere C₃ → one-axis through-flow, closed in 3-D, 82 = 81 + 1 carries over to fluids — open — C3E1: D_sys = 0.118 vs noise 0.133, 81-core lobe D ∝ ε (no amplification); C3E1 lacks U₃, and a 3-D run with U₃ does not exist.
- Navier–Stokes global regularity recast / events as regularization valve — open — not claimed; no blow-up diagnostic in any script.
- Onsager-type dissipation anomaly, ε_sat ≈ 0.2 (Pillar IV) — identity — saturation set by hand in metriplectic_vortex.py; shipped stochastic budget residual 0.333; ONS1 did not reproduce 0.2.
- Transition class: five directed-percolation exponents — anchor-restatement — ν_∥ 5.6% off, θ_s 7% off; final run's own sum 0.4395 vs DP 0.4732; gates re-run after changing fit windows.
- Avalanche exponent τ in [1.40, 1.50] — open — τ = 1.596 at N = 64 (outside band); 1.46 at N = 96 (h ≥ 4 only); tension, not a pass.
- Length selection β ≈ 1/2 — identity — shipped slope 0.4643, finer run 0.4237; follows from the imposed dispersion; the N = 512 DNS value 0.501 has no code in the repo.

## Open items
- Full 3-D implementation of the three-sphere mechanism (U₃ coupled to 3-D Navier–Stokes with vortex stretching at high Re): a computational limit; the key result stays a reduced test.
- Effect of the three-body term U₃ on the Newtonian closure [O]; 3-D closure and the full stress tensor data-pending.
- P4 second η route: post-hoc agreement (ratio 0.96) needs a fresh pre-registration.
- Length-selection β ≈ 0.5: DNS confirmation data-pending.
- Pillar IV ε_sat ≈ 0.2 [O]; the PRL ensemble CSV awaits the author's clarification of column meanings or the original ADG code.
- 3-D Onsager anomaly and Navier–Stokes global regularity: not claimed.
- The volume uses no external fluid data (review F-13).

## Reproduction
The ZIP contains docs/fluid-dynamics/ (the published HTML pages), repro/fluid-dynamics/ (code and data), LEDGER.json (this volume's claims-ledger rows), CORPUS_GUIDE.md and MANIFEST.sha256 (SHA-256 of every file).
Main checks (Python 3 with numpy, no network needed):
- `python3 repro/fluid-dynamics/experiments/NC1_newtonian_closure/nc1_run.py` (SEED = 19), then `--posthoc-p4` for the non-gating diagnostic.
- `python3 repro/fluid-dynamics/experiments/C3E1_three_sphere_directed_ejection/c3e1_run.py`.
- repro/fluid-dynamics/experiments/ONS1_adg_vortex_gas/: `adg_vortex_gas.py`, `analyze.py`, `csv_checks.py`.
- `validate_all.py` (e.g. repro/fluid-dynamics/repro/fluid-dynamics/13-synthesis-reproducibility-spine/validate_all.py; 5/5 PASS) and repro/fluid-dynamics/repro/fluid-dynamics/07-pillar-ii-geometric-arrangement-fixes/verify_rotcore.py.
- Three-sphere reduced test: repro/fluid-dynamics/repro/fluid-dynamics/11-cross-scale-extensibility-one-arrangement/corotation.py and lattice_inflow.py.
Known irreproducible items are listed in repro/fluid-dynamics/IRREPRODUCIBILITY_LEDGER.md.

## Citation and links
- Site: https://jamming-physics.org/fluid-dynamics/
- Concept DOI: 10.5281/zenodo.17972568
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
