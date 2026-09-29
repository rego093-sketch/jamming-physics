# Fluid-dynamics ("Configured Continuum") — Reviewer 2 of 3
## Lens: code, data and grades. Does runnable code reproduce the Navier–Stokes numbers on the pages?

Date: 2026-09-29 · Reviewer 2 (code/data) · Nothing under `docs/` or `repro/` was edited. Scratch work is in the session scratchpad (`r2fd/`).
Code root below: `R = repro/fluid-dynamics/repro/fluid-dynamics/`.
Environment: Python 3.11, numpy 2.4.6, scipy 1.17.1, pandas 3.0.6. Runs used `PYTHONDONTWRITEBYTECODE=1`.

---

## 0. Verdict

1. **The code does not solve the Navier–Stokes problem in the sense of the Millennium question (3-D global regularity), and it doesn't try to.** It contains two standard, correct pseudo-spectral solvers (`ns2d.py` for 2-D and `ns3d.py` for 3-D, both periodic, 2/3-dealiased, integrating-factor RK4). They run at modest resolution and Reynolds number: 2-D N ≤ 320, and 3-D N ≤ 128 at ν = 0.008, Re_λ ≈ 40–60. Every run shows a smooth solution. No script computes a blow-up diagnostic: no max|ω|(t), no Beale–Kato–Majda integral, no analyticity-strip width, no growth of high-k energy toward a singularity. The pages agree with this. §14 and `IRREPRODUCIBILITY_LEDGER.md` say global regularity is "not claimed" and remains an open `[GATE]`. The author's statement "solved the Navier–Stokes equations" is therefore contradicted by the volume's own text and is not supported by any code.
2. **The solvers work.** The author never benchmarked them against exact or standard solutions, so I did. `ns2d` reproduces the exact 2-D Taylor–Green decay to 1e-14. `ns3d` reproduces the exact ABC/Beltrami decay to 8e-15, has E(0) = 0.125 for 3-D Taylor–Green, and satisfies dE/dt = −2νZ to 3.5e-6. The numerical core is sound.
3. **Script → file mapping is complete.** All 32 `.py` names on the pages exist under `R/` (§1). Two data or result files that the pages name are missing: `ns_reference_table_pinned.txt` (ax-x) and the N = 512 "blind DNS" pipeline (§8). Several displayed numbers have no shipped regeneration path (§3, F-05, F-07, F-09).
4. **Most of the NS-flavoured "PASS" results are in-model or definitional.** Examples: the energy budget dE/dt = −2νZ is an identity of 2-D NS; max ε_ν = 2νZ(0) is trivially ∝ ν; the "Onsager saturation" is an ODE whose sink b·E is imposed by hand. **No external data are used anywhere.** There is no DNS database, no experiment, and no observational dataset. The "tropical cyclone / ocean eddy" audit runs on synthetic samples whose generator is not shipped. The volume states: "All constituent results are the author's own and are merged here without external citation, by design" (ax-x).
5. **The grading system is out of line with the corpus.** The volume uses `[LOCK]/[DERIVE]/[GATE]` rather than `[F]/[V]/[L]/[O]`. As a result the manifest records `grades = {forced 0, verified 0, open 0, hypothesis 0}`, there is no `[V mech]`/`[V data]` split, and the irreproducibility ledger attests "zero [O]" even though several displayed numbers cannot be regenerated in-package.
6. **Hard defects found:**
   - Several "PASS" verdicts are printed as string literals, not computed (`transition_dp_final.py`, `ns3d.py`, `lattice_inflow.py`).
   - Three scripts write to a hard-coded `/home/claude/v3work/` path and crash on any other machine.
   - `axioms.py` fails its own stated pass threshold.
   - The 3-D solver-validation figures on the pages (1e-16, 1e-14) are 8 and 2 orders of magnitude better than what the code produces.
   - The corpus gate currently FAILs `repro_sha256` for this volume, because of `__pycache__` handling.

---

## 1. Script map (pages → repro)

`grep -ohE '[A-Za-z0-9_]+\.py' docs/fluid-dynamics` gives 32 distinct names. Every one resolves to exactly one file under `R/`, except `validate_all.py`, which has three byte-identical copies in `01-`, `06-` and `13-`.

| script | location under R/ | ran? | result |
|---|---|---|---|
| ns2d.py | 06-pillar-i…/ | yes (1.3 s) | matches `ns2d.out.txt` exactly |
| validate_all.py (×3) | 01-/06-/13- | yes | **ImportError as shipped** (F-10). With `PYTHONPATH=06:09`, 5/5 PASS and numbers identical to the page (dE 2.9e-8, dZ 5.4e-6, budget 4.4e-6) |
| ns3d.py | 09-…/ | yes, full `__main__` (2 m 24 s) | numbers identical to `ns3d.out.txt`; closing text differs (stale .out, F-11). Validation line **dE/E = 1.0e-8, div = 4.1e-12** vs page 1e-16 / 1e-14 (F-02) |
| run3d.py, measure3d.py | 09-… | not run (needs hours plus an unshipped `state.npz`) | only N = 128 output shipped (F-05) |
| metriplectic_vortex.py | 09-… | yes | matches `.out.txt`; stochastic budget residual **0.333** (F-04) |
| axioms.py | 04-… | yes | matches `.out.txt`; reduction error 1.8e-15 **> its own 1e-15 pass bar** (F-12) |
| length_selection.py | 08-… | yes (54 s) | matches (slope 0.4643) |
| verify_rotcore.py | 07-… | yes | **FileNotFoundError** with the default path; with `./rotcore` it gives 2.83e-12 PASS (F-08) |
| mdr_universality.py | 12-… | yes | matches `p5_consolidated.out.txt` exactly |
| event_rg.py, event_flux.py, multid_flux.py, universality.py, corotation.py, extensibility.py, lattice_inflow.py, rigid_shell.py, unjam_inflow.py | 05/09/10/11/03 | yes (0–74 s each) | all match their `.out.txt` exactly |
| marginal_fluidity.py | 03-… | stopped at 180 s | the first 46 output lines match `.out.txt` byte for byte |
| transition_dp.py | 03-… | stopped at 180 s | the first 35 lines match (timings aside). The script **ends by writing to `/home/claude/v3work/…`** and would crash (F-06) |
| transition_dp_refine.py / _final.py / _2d.py | 03-… | not run (> 3 min) | code read. `_final` hard-codes its consolidated table (F-06) |
| dissipation_avalanche.py, dev64.py, analyze*.py, embed96.py, run_p4.py, consolidate_p4.py, decay.py, analyze_ce.py, nonequilibrium_dissipation.py | 09-… | not run (multi-call, checkpointed, > 3 min; need unshipped `state64/96.npz`) | captured outputs compared with pages (F-07) |
| "run-all / gate" | — | — | no volume-level run-all script exists. `validate_all.py` covers 5 checks only. `tools/gate.py` is structural (hashes, slugs) and runs no science code (F-14) |

**Missing files named on pages:**
- `ns_reference_table_pinned.txt` (ax-x: "The full table ships as …"). Absent from the whole repo.
- The §8 "companion DNS (spectrally rotating forcing, ETDRK4, N = 512) … blind pipeline β̂ ≈ 0.501 … shuffle test". No code or data are shipped for it.
- The §9 "negative control: naive contact-merger rule, residual ≈ 0.49". No code or output is shipped (`grep -ri 'contact.merger\|0\.49'` over repro/fluid-dynamics returns nothing).
- The offline ADG integrator that produced `metriplectic-onsager/data/raw/epsilon_events_ensemble.csv`. Its README says it was "produced offline"; the solver is not shipped.
- `rotcore/audit-source/code/scripts/recompute_v136.py` is a placeholder. It prints: "This is a placeholder… synthetic demos not regenerated here."

---

## 2. Independent solver benchmarks (reviewer-run; the author ran none)

Script: `scratchpad/r2fd/bench.py`, which imports the shipped `ns2d`/`ns3d` unmodified.

| benchmark | setting | result |
|---|---|---|
| 2-D Taylor–Green, exact ω = 2 sin x sin y·e^{−2νt} (ns2d) | N = 64, ν = 0.01, T = 5 | max error **1.0e-14** ✔ |
| 3-D ABC/Beltrami, exact u₀e^{−νt} (ns3d) | N = 32, ν = 0.05, T = 2 | max error **7.8e-15** ✔ |
| 3-D Taylor–Green (Brachet IC), energy budget (ns3d) | N = 32, Re = 100, t ≤ 3 | E(0) = 0.1250 (exact 0.125); max rel. err. of dE/dt = −2νZ **3.5e-6** ✔ (enstrophy peak near t ≈ 9 not reached; too short to compare with Brachet et al.) |
| ns3d inviscid energy drift vs dt | N = 32, T = 1.5 | dt = 0.01 → 1.0e-8; 0.005 → 4.3e-10; 0.0025 → 2.0e-11 (≈ dt^4.5: RK4 truncation, **not** machine precision) |

**Not done anywhere in the volume:**
- Taylor–Green enstrophy-peak comparison with Brachet et al. (1983).
- Kolmogorov-flow instability threshold.
- Lid-driven cavity (not possible with a periodic spectral code anyway).
- E(k) ∝ k^{-5/3} inertial-range check or comparison with a DNS database (JHTDB, Kaneda–Ishihara).
- Any blow-up / regularity diagnostic.

Resolution and Reynolds number actually reached:

| run | resolution | Reynolds number / resolution quality |
|---|---|---|
| 2-D | N ≤ 320 | ν ≥ 5e-4; "Re_eff" = U_rms·2π/ν ≤ ~3400, inflated by using the box size as the length |
| 3-D | N ≤ 128 | ν = 0.008 fixed; Re_λ ≈ 57–60 at the start of decay (p9 output); k_max·η = 0.89 at N = 64 (under-resolved), ≈ 1.3–1.5 at N = 96 |

---

## 3. Findings

Severity: **C** critical · **H** high · **M** medium · **L** low.

### F-01 [C] The claim "solved Navier–Stokes" has no support in code or pages
- **Where:** author framing. Relevant pages: §14 ("Global regularity is compressed to one gate, not claimed"), §01, `IRREPRODUCIBILITY_LEDGER.md` G1.
- **Evidence:**
  - The only NS runs are smooth periodic solutions at modest Re (§2 above).
  - No diagnostic anywhere targets finite-time singularity.
  - The 3-D work concerns filtered energy-flux statistics (Onsager-type), not regularity.
  - "Rearrangement events supply a physical regularization valve" (§14) is prose with no corresponding code.
- **Fix:** the author should stop describing the volume as having solved NS. If the regularity "recast" is to be kept, grade it `[O]` with its obstacle stated. Any "valve" claim needs a computation, for example a regularized model with events, showing bounded ‖ω‖_∞ where plain NS is being pushed toward blow-up (Kerr / Hou–Luo-type initial data).

### F-02 [H] The 3-D solver-validation numbers on the pages are wrong by orders of magnitude
- **Pages:** ax-o ("ΔE/E∼10⁻¹⁶ … divergence-freeness ∼10⁻¹⁴"), §9 (same), ax-b line "inviscid energy conserved to ∼10⁻¹⁶".
- **Ran:** `ns3d.inviscid_energy_check()`.
- **Got:** **dE/E = 1.0e-8, div = 4.1e-12.** `avalanche_N64.out.txt` separately shows dE/E = 4.7e-9. The dt scan (§2) shows this is RK4 time truncation; the code never reaches 1e-16.
- **Also:** the `(PASS)` in `ns3d.py:107` is a literal string, with no threshold behind it.
- **Fix:** quote the measured 1e-8 and 4e-12 together with dt, or show dE/E → round-off as dt → 0. Make the PASS a computed comparison against a stated tolerance.

### F-03 [H] The 3-D "resolution-converged across N = 64, 80, 96, 128" claim cannot be checked from shipped material, and parts conflict
- **Pages:** §9, ax-o, §13 ledger, §14.
- **Evidence:**
  - Only `measure3d_N128.out.txt` is shipped. There are no N = 64/80/96 measurement outputs and no `state*.npz`.
  - `run3d_run_log.txt` has 11 lines with no N recorded. It shows one spin-up segment reaching only t = 2.26 from random initial data, and one "N = 128 equilibration" of t = 0.64, which is well under one large-eddy turnover time. Enstrophy is still rising (Z 3.9 → 8.9), so the field is not statistically stationary.
  - The page's N = 128 entries (60 %, 14 %, 0.80) match the shipped ℓ = 0.13 row (59 %, 14 %, 0.797). They do not match the ℓ = 0.10 row (62 %, 13 %, 0.819). The filter scale behind each N column is therefore undocumented.
  - The convergence sentence in `ns3d.py` is a hard-coded print.
  - At fixed ν, varying N tests grid convergence of one flow at Re_λ ≈ 60. It says nothing about Re-dependence.
- **Fix:** ship the four measure3d outputs with ℓ stated, plus the state files or checksums. Label the result "grid-converged at Re_λ ≈ 60". Add a null model, such as a random-phase field with the same E(k), to show that "top 20 % of strain carries 60 % of forward flux" is not generic to any correlated field.

### F-04 [H] The "Onsager saturation" is imposed by construction, and the shipped stochastic run contradicts "budget closes within 2 %"
- **Pages:** §9, §13 lead ("the budget … closes within 2%"), validate_all [4]/[5], exec summary ("an Onsager-type anomaly … reproduced").
- **Evidence:**
  - `metriplectic_vortex.steady()` is dE/dt = I − aνE − bE with ν-independent b set by hand. ε_bind → I as ν → 0 is algebra. The docstring and page admit "by construction", yet it is still counted as PASS evidence.
  - The shipped stochastic realization prints `eps_tot 0.27998` against I = 0.21, with **budget_residual 0.333**. Cause: injection is averaged over T = 400 and the sinks over T_w = 300, with a mixed AREA normalization.
  - The "viscous reference branch" is 2-D decaying NS, where max ε_ν = 2νZ₀ is trivially ∝ ν and 2-D has no energy anomaly. Setting a 0-D model beside it shows nothing about NS.
  - The ensemble in `metriplectic-onsager/` has `Re_eff = 1000.0` exactly (a set value, not a measured one) and its ADG solver is absent.
- **Fix:**
  - Grade saturation as definitional (`[F]` of the model), not as evidence of an anomaly.
  - Fix the normalization in `run()`.
  - Either ship the ADG solver or grade the ensemble `[O]`.
  - Remove "Onsager-type anomaly reproduced" from §01.

### F-05 [H] The pinned NS reference table (ax-x) is not shipped, and the shipped reference CSVs follow a different protocol
- **Evidence:**
  - `ns_reference_table_pinned.txt` is missing.
  - `metriplectic-onsager/NS_reference/generate_viscous_data.py` uses N = 64, a 20-vortex initial condition, and t_max = 2. That is not ax-x's "seed 7, k_peak = 4, Z₀ = 1.476, T = 8, window [2, 8]".
  - The 256² and 512² CSVs have no generator.
- **Ran:** ns2d with the ax-x protocol (N = 128) → ⟨Re_eff⟩ = 27.4, 106.7, 263.8, 602.7, 1657, 3436 for ν = 0.05 … 0.001, and max ε = 2νZ₀ exactly.
- **Comparison:** the shipped CSVs give Re_eff = 53, 147, 308, 636 (N = 64) and 630/1611/3252 (256²). They do not match.
- **Fix:** ship the pinned file together with a generator script, or remove the sentence.

### F-06 [H] The transition-class consolidated table is hard-coded and assembled from mixed runs, and the scripts crash
- **Pages:** §3 box "Transition class — five exponents, no tuning", §13 ledger row T.
- **Hard-coding:** `transition_dp_final.py:97-100` prints `delta = 0.158 … PASS`, `nu_par = 1.637 … PASS`, `hyperscaling sum = 0.662 … PASS` as **string literals**.
- **Where the literals come from:**
  - 0.158 is the refine run's *raw* δ (0.1577). The same run's extrapolated value is δ = 0.1769, and stage 1 gave 0.1220 with `GATE[2] decay exponent: FAIL`.
  - 0.662 is built with the refine run's θ_s = 0.386. The final run's θ_s = 0.335 and δ′ = 0.105 give a sum of 0.4395 (DP 0.4732), as printed in the same output.
- **Gates re-run until passing:** spreading went GATE[3] FAIL → GATE[3′] FAIL → GATE[3″] PASS, after the fit windows were changed.
- **Loose tolerances:** ν∥ is 5.6 % off, θ_s 7 % off, a is 2σ off, and the 2-D ratio is 2σ off. All are marked PASS, and the tolerances were not stated in advance.
- **Crash:** `transition_dp.py:236,238`, `transition_dp_refine.py:129` and `transition_dp_final.py:108` write to `/home/claude/v3work/…` and raise FileNotFoundError after 3–4 minutes of computation.
- **Fix:** compute the table from one run with pre-declared tolerances, write outputs relative to `__file__`, and report the failed gates alongside the passes.

### F-07 [H] The avalanche exponent is not pre-registered in practice: the estimator changed after a failed test
- **Pages:** §9 ("genuine prediction … band fixed in advance"; "τ = 1.60 → 1.46 … clean finite-Reynolds trend"), §13.
- **Evidence:**
  - `avalanche_N64.out.txt` says "PRE-REGISTERED tau in [1.40,1.50]: TENSION (measured 1.596)".
  - The N = 96 field was then made by spectral embedding at the **same ν**.
  - The "robust" estimator was switched from all thresholds (N = 64) to h ≥ 4 only (N = 96). `avalanche_N96.out.txt` itself says h ≥ 3 gives 1.479. At h = 2 and h = 3, the N = 96 MLE is 1.713 and 1.677, outside the band. The log-bin value is 1.39, below the band.
  - Because ν is fixed, the 1.60 → 1.46 drift is a numerical-resolution effect, **not** a Reynolds trend.
  - `mdr_universality.py` then uses the h = 3 pool with a third estimator (log-bin over [2, s₉₉.₅], τ₀ = 1.419).
- **Fix:** state the estimator in advance and apply it identically at both N. Grade this `[O]`/tension until it holds at matched estimator and increasing Re.

### F-08 [M] Pillar II audit: the verifier checks less than the ledger says, the data are synthetic, and the default path is broken
- **Broken default:** `verify_rotcore.py` with no argument raises FileNotFoundError (`../rotcore/data/…`). ax-a's run line `python verify_rotcore.py` omits the needed `./rotcore`, and its verbatim block is garbled ("RCCI audit ( 0, B finite, c^2 = B/rho", with the marginal_fluidity line merged in).
- **Ledger rows the verifier does not back:**
  - The verifier recomputes robust summary metrics from `metrics_long_v1.3.9.csv` and compares them with `metrics_robust_v139.csv`. That is internal consistency of one sample file with its own summary.
  - §13 ledger rows "RCCI identity … verify_rotcore.py 10⁻¹⁵" and "Identity-residual tables vs published … reproduced" are **not** checked by this script. It reads only those two CSVs.
- **Synthetic data:** the samples (400 per case, φ ≈ 0.10) are synthetic ("synthetic demos not regenerated here"), but §7/§01 present them as "tropical cyclone, ocean eddy" regimes without saying so.
- **Fix:** label them synthetic surrogates (`[V mech]` at best), ship the generator, add the identity/residual checks, and fix the default path.

### F-09 [M] Length selection: lead text overstates, and the convergence claim is contradicted by a finer run
- **Pages:** §8 lead ("nonlinear and blind DNS recover β ≈ 0.501"); body ("slope ≈ 0.46, converging to 1/2 as binning/resolution improve").
- **Ran:** shipped settings (12 wavelengths, N = 128) → slope **0.4643**, per-case k/k* = 0.986–1.066.
- **Finer run:** 16 wavelengths, N = 192 → slope **0.4237**, k/k* up to 1.142. This moves *away* from 0.5.
- **Other points:**
  - The N = 512 DNS β̂ = 0.501 has no shipped code.
  - The model is 2-D Swift–Hohenberg, not NS. The one-half law follows from the imposed dispersion λ = μ + εk² − σk⁴.
- **Fix:** attribute 0.501 only to the unshipped DNS and grade it `[O]` until shipped. Drop "converging" or demonstrate it.

### F-10 [M] validate_all.py cannot run from any of its three locations
- `import metriplectic_vortex` lives in `09-`, but copies sit in `01-`/`06-`/`13-`. As shipped: ModuleNotFoundError.
- ax-a presents "validate_all.py returns 5/5 PASS … verbatim from a clean run".
- **Fix:** add a `sys.path` insert, or co-locate `metriplectic_vortex.py`.

### F-11 [M] Stale captured output and hard-coded conclusions
- `ns3d.out.txt` says "converged across N=64,80,96" while the code prints "N=64,80,96,128". The .out was not regenerated after the edit.
- `multid_flux.py:76` prints "(stable across N=192,256,320 …)" as a literal, and only N = 192 is run or shipped. The page's own figures for that claim drift monotonically (top-20 %: 63 → 61 → 58 %; half-area: 12 → 14 → 16 %), which is weakening concentration, not "resolution-stable".
- `lattice_inflow.py:67` prints "PASSES" unconditionally.
- **Fix:** compute or omit these; regenerate the `.out` files.

### F-12 [M] axioms.py fails its own criterion
- The page (§4 box) and README state "pass: reduction error ≤ 10⁻¹⁵". Measured: **1.8e-15**.
- Part (2), "real dipole self-propels at v = 0.1592", evaluates the formula Γ/2πd. It is not a simulation.
- `U2_forces` takes `A=np.exp` but uses an inconsistent `Ap = −exp(−r)`. This is harmless (A is unused) but sloppy.
- **Fix:** set a tolerance appropriate to double precision (e.g. 1e-13 relative) and relabel (2) as analytic.

### F-13 [M] The grade system does not follow the corpus, and the ledger's "zero [O]" is untrue in substance
- **Grade vocabulary:**
  - Pages use `[LOCK]` (10–15), `[DERIVE]` (44), `[GATE]` (39), and no `[F]/[V]/[L]/[O]`.
  - The manifest therefore records all grade counts as 0.
  - There is no `[V mech]` vs `[V data]` distinction.
- **In-model vs external data:**
  - Every "PASS" is in-model (`[V mech]`) or definitional.
  - Nothing is tested against external data:
    - DP experiments (Couette/channel 2016, pipe 2024) are cited without references and with no quantitative comparison. Only β = 0.276 is quoted, and no model β is compared with it.
    - "Virk's MDR" is asserted to match but is never loaded.
    - Vassilicos's law is compared only with the author's own Re_λ 37–60 decay, a 0.2-decade fit window.
- **Items `IRREPRODUCIBILITY_LEDGER.md` should list as `[O]` (C3) but does not:** it attests "every displayed quantity … deterministically reproducible". These cannot be regenerated in-package:
  - β̂ = 0.501 (N = 512 DNS)
  - the ADG ensemble (ε_tot 0.205–0.216, Re_eff ~5000)
  - the negative-control residual 0.49
  - the 3-D N = 64/80/96 figures
  - the pinned NS table
  - the 256²/512² NS reference
- **Definitional checks labelled PASS:**
  - event_rg: power-law recursion with zero exponent sum → constant
  - U2 capacity identity 1e-16
  - DNA identity residual 0
  - RCCI identity
  - max ε_ν ∝ ν
- **"No row uses a fitted parameter" (§13):** metriplectic a = 2.0, b = 0.55 and I = 0.21 are free choices, and the pseudogap θ = 0.45 and q = 0.35 are "flagged" parameters.
- **Fix:**
  - Map LOCK → [L], DERIVE → [F], GATE → [O].
  - Add [V mech] / [V data].
  - Move the unshipped numbers into the ledger as [O] with their obstacle.
  - Relabel the identities as consistency checks.

### F-14 [M] The corpus gate FAILs repro_sha256 for fluid-dynamics because of __pycache__ handling
- **Ran:** `python3 tools/gate.py` → `[FAIL] repro_sha256 integrity — drift: ['fluid-dynamics']`.
- **Cause:**
  - The manifest's `dfa5ecb1…` equals `dirhash` **including** the untracked, git-ignored `08-…/__pycache__/length_selection.cpython-311.pyc` (dated 2026-09-28 22:45).
  - A clean clone (no .pyc) hashes to `d06d47a8…` and fails.
  - Any script run that writes .pyc also fails. At present `06-/__pycache__` and `09-/__pycache__` (00:28–00:29 today, from concurrent review runs) cause the drift.
- **Fix:**
  - Make `tools/gate.py`'s `dirhash` skip `__pycache__` and other `.gitignore`d files.
  - Regenerate the manifest from a clean tree.
  - Delete the three `__pycache__` dirs. I did not delete them because the brief says not to modify `repro/`.

### F-15 [L] Minor
- (a) "Exact in 1D Burgers / 100 %" (§13 ledger, §01) against measured ∫ε_ν / (Δu)³/12 = 1.08–1.11. The §9 body honestly says ~10 %.
- (b) LaTeX residue on pages: `Section~\ref{…}`, `\vspace{1em}`, `\rule`, `\end{document}` (ax-x), `\Rey`, `\eps`, stray `)}` (ax-d/ax-o/ax-w).
- (c) All 22 appendix pages link to the repro root, not to the chapter folder holding the script.
- (d) `Re_eff = U_rms·2π/ν` uses the box size, which inflates Re by ~4–6× relative to integral-scale Re.
- (e) `marginal_fluidity.py`: pooled G_rel = a(z − z₀) has R² = 0.45. The smallest sampled z is 6.39 and no sample has G_rel ≈ 0, so z₀ = 5.99 is an extrapolation. The CI [5.49, 6.29] is honest but wide.
- (f) `metriplectic_vortex.steady()` normalizes U_rms by an extra 1/L "so Urms ~ O(0.5)", which is an arbitrary rescaling of the reported Re_eff.

---

## 4. What reproduces cleanly (credit)

- Every captured `.out.txt` that I could run within 3 minutes regenerates bit-for-bit, apart from wall-clock times: ns2d, ns3d (numbers), axioms, length_selection, metriplectic_vortex, mdr_universality, event_rg, event_flux, multid_flux, universality, corotation, extensibility, lattice_inflow, rigid_shell, unjam_inflow, and prefixes of marginal_fluidity and transition_dp.
- Seeds are fixed and outputs are deterministic.
- Page numbers for Pillar I (2.9e-8, 5.4e-6, 4.4e-6), §8 (0.46, k* to 1e-3), §9 2-D flux (63 %, 12 %, 0.28), the rotcore table (4.1 %/93 %/+0.80 … 55 %/−0.26) and P5 (1.37 ± 0.04) all match the code.
- The solvers are correct (§2).
- The pages are candid in places: "by construction" (§9), global regularity "not claimed" (§14), the Virk asymptote left as a GATE.

## 5. Priority fix list
1. Remove the "solved Navier–Stokes" framing (F-01).
2. Correct the ns3d validation numbers (F-02).
3. Un-hard-code and fix the paths in `transition_dp*` (F-06).
4. Ship or `[O]`-grade the unshipped numbers: N = 512 DNS, ADG ensemble, 3-D N = 64/80/96, pinned table, negative control (F-03/04/05/09/13).
5. Pre-declare the avalanche estimator (F-07).
6. Label the rotcore data as synthetic (F-08).
7. Fix the `validate_all` import and `verify_rotcore` default path (F-10/F-08).
8. Adopt the corpus grades with [V mech]/[V data] (F-13).
9. Fix the gate hash handling and clean `__pycache__` (F-14).
10. Add standard benchmarks (Taylor–Green enstrophy peak vs Brachet, E(k) vs a JHTDB snapshot) and at least one regularity diagnostic (max|ω|, BKM) if any regularity language is kept.
