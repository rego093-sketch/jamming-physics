# Cosmology volume — Reviewer 2 of 3: data, code and grades

Date: 2026-09-28 · Scope: `docs/cosmology/*/index.html` (42 pages + hub), `repro/cosmology/` · Lens: "data decides the theory". A claim counts only when data support it and code reproduces it.
No files under `docs/` or `repro/` were edited. My re-analysis scripts are in the session scratchpad (`sn.py`, `rar.py`). The inputs were public Pantheon+SH0ES.dat (PantheonPlusSH0ES/DataRelease on GitHub) and SPARC `NGC2403_rotmod.dat` (a GitHub mirror, villano-lab/galactic-spin-W1, because astroweb.cwru.edu is blocked here).

## Summary table

| id | sev | topic |
|---|---|---|
| C1 | critical | The science code is almost entirely missing: 1 of ~55 cited scripts exists, and neither dataset is shipped |
| C2 | critical | The NGC 2403 fit values (Υ = 0.567, χ²/dof = 1.99) come out exactly at a₀ = 1.2×10⁻¹⁰ (empirical), not at the "derived" 1.08×10⁻¹⁰ |
| C3 | critical | The Pantheon+ comparison is called "statistically degenerate", but its own numbers give Δχ² ≈ +87 against ΛCDM |
| M1 | major | a₀ = cH₀/2π is graded [F] despite a flagged modelling choice, an undrived ν, an [INPUT] H₀ and a coefficient chosen from data (look-elsewhere) |
| M2 | major | The scorecard grades over-promote: Solar System, SNe, angular-size minimum, Bullet and lensing γ = 1 |
| M3 | major | Grade vocabulary does not match AGENTS.md: [O] is used to mean "external input" ([L]), and there is no [V] anywhere |
| M4 | major | Gates check SEO and format only; no science number is gated; the digest is not pinned |
| M5 | major | Present-day data are excluded as "out of scope" (CMB peaks, BBN abundances, BAO fitted with ΛCDM) |
| M6 | major | Bullet cluster: the lede and the executive summary say "reproduced", but the page says toy/degenerate; the offset comes from chosen ICM parameters |
| M7 | major | Gamma dispersion is labelled "[O] relaxed", while the page itself shows an 8–15 order conflict |
| m1–m8 | minor | Numeric and consistency nits (below) |

---

## C1 (critical): the cited reproduction code and data are absent from `repro/cosmology`
- Evidence: `axb-reproducibility-map` says: "Every quantitative claim is reproduced by the companion package: thirty-four standalone Python scripts and two real datasets (SPARC `NGC2403_rotmod.dat`; Pantheon+ `Pantheon+_extract.tsv`)." `axh-provenance-ledger…` says: "Items marked S are reproducible from the scripts in repro/cosmology/slug/".
- What I ran: I extracted every `*.py` name cited on the pages (about 55 distinct science scripts, e.g. `ch6_galaxy_rar.py`, `ch7_lattice_optics.py`, `ch7_sne.py`, `ch8_bullet.py`, `ch8_bullet_offset.py`, `ch8_lensing_consistency.py`, `ch9_cmb_floor.py`, `ch9_lattice_cmb.py`, `ch4_orbits.py`, `ch_spin_locking.py`, `ch5_mercury_capture.py`, `ch_hubble_tension.py`, `derive_acoustic_length.py`, `ch2_gamma_collective.py`, `sim_acoustic_peaks.py`, …). I then ran `find` across the repo and checked git history (`git log --all`).
- Result: the only science script present is `repro/cosmology/repro/cosmology/02-back-calculation-broadband-gamma-spectrum/ch2_backcalc_spectrum.py`. None of the others was ever committed; only their PNG outputs exist in `docs/cosmology/assets/img/`. Neither dataset is in the repo. The pipeline source `src/cosmology/VP_EarthCosmos_v2.tex`, `split.py` and `render_eq.js` are also absent. The a₀/SPARC-175 claim points to an external Zenodo archive (10.5281/zenodo.17622357) that is not mirrored or hash-pinned. `IRREPRODUCIBILITY_LEDGER.md` lists `repro/cosmology/14-…/derive_acoustic_length.py` and `repro/cosmology/07-…/` as repro paths, but neither exists.
- Consequence: by the corpus's own rule, every "S"-marked number in App. H (SNe, Bullet offset, lensing γ = 1, CMB floor, spin 12/12, Mercury capture, Hubble tension, jets) is currently **data-pending / code-pending**.
- Fix: commit the 34+ scripts and both data files (or scripts that fetch the data, with SHA-256 pins) under `repro/cosmology/<slug>/`, and add them to `repro_sha256`. Until then, add every S-row to a "code-pending" table in `IRREPRODUCIBILITY_LEDGER.md` and change "Every quantitative claim is reproduced" to state the true count.
- The one script that does exist ran fine (<1 s). It printed ħc/a = 311.7 GeV, E(ka=0.1) = 31.17 GeV, sharp/smooth gamma-reach invariance, and digest `4ceacc27f7be…a63a74a`. These match the page. Its docstring gives a wrong self-path (`02-light-lattice-elastic-wave-sharpest/`), it sits under a doubled `repro/cosmology/repro/cosmology/` path, and it cites the missing `ch2_gamma_collective.py`.

## C2 (critical): the NGC 2403 fit reproduces at the empirical a₀, not at the derived a₀
- Page: `06-galactic-rotation-derivation-a0-ch0` says: "fits the measured rotation curve of NGC 2403 (73 points, SPARC) … at the derived a₀ … The fit gives Υ=0.567 … and χ²/dof=1.99". `06-why…` adds "(with a 3 km s⁻¹ error floor)".
- What I ran (`rar.py`): SPARC NGC2403_rotmod (73 points). I used the standard RAR ν(y) = 1/(1−e^{−√y}) with a 3 km/s floor added in quadrature, and fitted a single Υ_disk.
  - a₀ = 1.082×10⁻¹⁰ (the derived value): **Υ = 0.606, χ²/dof = 2.57**
  - a₀ = 1.2×10⁻¹⁰ (the empirical MOND/RAR value): **Υ = 0.567, χ²/dof = 1.99**, which is exactly the page's numbers
  - The "simple" and "standard" ν, and a max(err, 3) floor, all give different numbers. Only the (RAR-exp, quadrature, a₀ = 1.2e-10) combination reproduces 0.567 / 1.99.
  - Fitting a₀ and Υ jointly on this galaxy gives a₀ ≈ 1.7×10⁻¹⁰, χ²/dof = 1.09. This single galaxy does not prefer the derived value.
- Interpretation: the published fit was most likely run at the empirical a₀, so the claim "at the derived a₀, a₀ is not fitted" is not supported by its own numbers. This cannot be checked definitively because `ch6_galaxy_rar.py` is missing (C1).
- Fix: publish `ch6_galaxy_rar.py`, re-run at 1.082e-10, and report Υ ≈ 0.61 and χ²/dof ≈ 2.6 (or whatever the script actually gives). Report the 1.2e-10 fit alongside it as the reference. The SPARC-175 claim ("median RMS ≈ 13 km/s at the derived a₀ … indistinguishable from MOND within 0.1 km/s") needs the same audit. Its "fixed mass-to-light ratios and a single gas-thickness prescription" were chosen in a five-fold cross-validation, which means they are fitted parameters. Disclose them as such (no-tuning rule).

## C3 (critical): "degenerate" SN fit, but Δχ² ≈ 87
- Page: `07-non-expanding-lattice-optics-cosmology` says: "χ²/dof=0.50, against χ²/dof=0.44 for ΛCDM … a static medium with no dark energy fits the Hubble diagram as well as accelerating ΛCDM". The ledger says: "statistically degenerate … a data limitation, not a contradiction". The two laws "differ by at most |Δμ|=0.145 mag".
- What I ran (`sn.py`): Pantheon+SH0ES.dat with z_HD > 0.01 and non-calibrators gives **N = 1580**. I used `m_b_corr` with the diagonal errors and one marginalised offset.
  - VP d_L = (c/H₀)(1+z)ln(1+z): χ² = 787.9, χ²/dof = **0.499** (reproduced)
  - ΛCDM Ω_m = 0.3: χ² = 701.4, χ²/dof = **0.444** (reproduced)
  - **Δχ² = +86.6 against VP with the same number of free parameters.** Against best-fit ΛCDM (Ω_m ≈ 0.35), Δχ² = +93.8. Even the empty Milne law fits better than VP (χ² = 731).
  - Binned weighted residuals of VP: −0.055 (z < 0.1), 0.00, +0.061, +0.072, **+0.20 mag (z > 1)**, a clear systematic trend. ΛCDM residuals stay within about 0.06.
  - |Δμ| between the laws: 0.235 mag (same H₀) and 0.33 mag (each at its best offset) over the data range. **I could not reproduce 0.145.**
- The reduced χ² < 1 for both models comes from diagonal errors that already fold in systematics. It hides a very large likelihood difference. Calling the fit "degenerate" is therefore not supported by the page's own data. With diagonal errors, the data disfavour the VP law at roughly √87 ≈ 9σ (formal).
- Fix: report χ² (not only χ²/dof) and Δχ², and run with the full STAT+SYS covariance (`Pantheon+SH0ES_STAT+SYS.cov`). Change the status from "degenerate" to "disfavoured (Δχ² ≈ 87, diagonal errors); full-covariance test pending". Correct 0.145. Remove "fits … as well as ΛCDM" from the page, the ledger B row, and the App. F scorecard ("[F] deg").

## M1 (major): a₀ = cH₀/2π is over-graded [F] and carries look-elsewhere risk
- The App. F scorecard gives "a₀=cH₀/2π; Kepler→flat; RAR — [F] dist". App. H says "forced: 2*pi is geometric, not fitted".
- On the same pages, the author concedes all of the following:
  1. "What remains a modelling choice … the identification of the relevant length as the full wavelength λ_bg rather than the reduced R_H";
  2. "The interpolation function ν is taken in the standard RAR form rather than derived";
  3. H₀ (κ_opt) is "[INPUT] — fixed from data";
  4. "the empirical scale independently places the coefficient in the consistent band k≈5–7".
- Choosing the coefficient 2π because it lands in the band that the data allow is a post-hoc selection. `14-acoustic-length-structurally-hard` itself calls exactly that forbidden: "choosing such a factor to land on the target is precisely the post-hoc tuning the governance forbids". Candidate coefficients 1, 2, π, 2π, 4π, 6 (from cH₀/k) span 0.5–6.8×10⁻¹⁰. At least two "natural" choices (2π and 6) fall in the empirical band, so the look-elsewhere risk is real. The cH₀/2π ≈ a₀ coincidence is long known (Milgrom 1983), and the page says so.
- Fairness: the empirical a₀ carries a systematic error of about 20% (McGaugh+2016: 1.20 ± 0.02 (stat) ± 0.24 (sys) ×10⁻¹⁰). "90%" is therefore within 0.5σ_sys. That is consistent, but it is not a discriminating test. The page should quote the error bar instead of "90%".
- Fix: grade as [F+O] or [L|H₀] (structure forced, λ-vs-ƛ identification HYP, ν borrowed, H₀ input). Add a look-elsewhere note. State the empirical a₀ with its uncertainty.
- Data-pending: the "a₀ tracks H(z)" prediction can already be confronted with high-z rotation curves (e.g. Genzel+2017/2020, Milgrom 2017 commentary). Either run that comparison or list it as data-pending with named datasets. Note also that a₀ ∝ H(z) needs an H(z) in a model declared non-expanding; state which quantity evolves.

## M2 (major): other scorecard rows are over-promoted (`axf-executive-summary-one-page-result`)
- Solar-system orbits "[F] deg, periods ≤0.73%": GM_⊙ = κQ_⊙ is *calibrated on the Sun* (`cos_locks.json`: badge "calibrated"), so any 1/r² law returns Kepler. This is an accommodation, i.e. [L]. The table says "residuals track small differences between the adopted semi-major axes", but Saturn's +0.73% is the Jupiter–Saturn perturbation / osculating-element effect, and the text should say so. The text also claims "scatter 9.6×10⁻¹²" while the table shows 1.00000 and 1.00001.
- SN Hubble diagram "[F]": this is a fit with an input rate and a marginalised offset, and it is disfavoured (C3). The grade should be [L]/data-disfavoured.
- Angular-size minimum z = e−1 "[F]": the page says it is conditional on the reciprocity/focusing assumption, and that assumption is itself open (item ii). Grade [F|HYP-focusing].
- Dark matter row "[F]/[O] **dist** … Bullet 0.2–0.6 Mpc; lensing γ=1": the §8 pages label both the Bullet offset and the lensing as *degenerate*. γ = 1 is imposed ("under no-slip matching to general relativity (Φ=Ψ…)"), and `ch8_lensing_consistency.py` then infers the deficit mass from the rotation fit and assumes it lenses as mass. That is circular, not a test.
- Mercury: the libration period 15.7 yr is compared with an "observed 12–15 yr". The long-period free libration of Mercury is a theoretical estimate, not a measured value. Give the source or relabel it. The capture probability "7–73%" spans a factor of 10 and is not a result.

## M3 (major): the grade semantics do not match AGENTS.md
- The App. F legend defines "[O] open (external empirical input)" and uses "[F+O]", "[HYP]" and "[SPEC]". In AGENTS.md, an external anchor is **[L]** and [O] means an open problem with a stated obstacle. `_decl.json` / the manifest record `verified: 0`. No claim in the volume passed a falsification test built against data, yet the scorecard carries 15 [F] marks. The "self-falsification check" in App. H is `(2/π)/(1/π²) == 2π`, an identity that cannot fail.
- Fix: map the volume's grades to [F]/[V]/[L]/[O](+[H]). Give κ, κ_opt, H₀, the CMB 2.725 K, L_150 and g_* the grade [L]. Replace the identity check with a genuine falsifiable one, e.g. a₀ from the SPARC RAR fit with its error bar versus cH₀/2π.

## M4 (major): the gates never touch science numbers
- `reports/phase-v1_12-final-audit.gate.json` shows "PASS 24/24". All the checks are C4/SEO/sitemap/llms/answer-first. No tool in `repro/cosmology/tools/` executes a science script (no subprocess/runpy). The digest printed by the one script (`4ceacc27…`) appears nowhere in `docs/` or `repro/`, so it gates nothing. App. B says "no random seeds", which contradicts the corpus `SEED = 19` rule.
- Fix: add a gate that runs each `repro/cosmology/<slug>/*.py` and compares its printed headline numbers and 2×SHA-256 digest with the values on the page.

## M5 (major): data that exists today is excluded from the comparison
- App. F says: "big-bang nucleosynthesis, the acoustic peaks, and structure-formation history are out of scope by design, not unsolved." But the CMB angular power spectrum (Planck), the present-day ⁴He/D abundances and BAO are *present-day observables*. `14-cmb-anisotropies…` concedes "harmonic peaks at ℓ~540, 810: NOT reproduced". §7 says "the BAO and growth (fσ₈) data—which we fit with standard ΛCDM and therefore regard as degenerate". Fitting BAO with ΛCDM is not a VP fit, so it cannot establish degeneracy.
- Fix: in the ledger, list these as **conflicting / data-pending**, not out of scope. Planck TT peaks 2 and 3 are "not reproduced". BAO needs a VP fit to DESI/BOSS D_V/r_d with the VP distance law. Y_p = 0.245 is a present-day measured abundance and should be data-pending.

## M6 (major): the Bullet cluster claim is overstated in the lede and summaries
- Lede: "This reproduces the Bullet-Cluster-type separation between lensing mass and gas without a dark-matter particle". App. F: "reproducing the Bullet-Cluster offset (0.2–0.6 Mpc)".
- The body says the toy model is in normalised units with M_def:M_bar = 5:1 *inserted* ("as in real clusters", which is the DM fraction put in by hand), and that the quantitative χ² gate is open. `ch8_bullet_offset.py` produces 0.41 Mpc from chosen ICM values (n_e = 0.01 cm⁻³, v = 4700 km/s, Σ = 0.3 kg m⁻²). Sweeping n_e over 0.002–0.024 to "span" the observed band is a parameter scan, not a prediction. Per the page, the physics is ram pressure, identical to ΛCDM. The claim τ_Δ ≫ τ_coll "by construction" is argued, not computed. The inconsistency also shows up internally: `ch8_bullet.py` is quoted as "≃0.86 L_off" on one page and "≃0.75 L_off at τ_Δ=5τ_coll" on another.
- Fix: lede → "mechanism demonstrated (toy); magnitude degenerate with ΛCDM ram-pressure; quantitative gate open". Mark M_def/M_bar and the ICM parameters as inputs. Data-pending: Clowe+2006 κ map and Chandra X-ray centroid.

## M7 (major): gamma-ray dispersion is labelled "relaxed"
- The §2 page states that the transverse lattice estimate is "8–15 orders" beyond the Fermi GRB 090510 bound (E_QG,2 > 1.3×10²⁰ eV). My order-of-magnitude check: at ka ≈ 0.1 (31 GeV), δv/c ~ (ka)²/24 ≈ 4×10⁻⁴, which gives a delay of about 10¹³–10¹⁴ s over a z ≈ 0.9 path against an observed delay of ≲1 s. The page's own "Δt ≈ 3×10¹⁹ s" (a different scale) points the same way. The rescue (quasi-longitudinal/collective mode) is a mechanism whose scripts are missing (C1). The ledger's "[O] relaxed, not fully closed" and the scorecard's "reframed conf→open" understate a live conflict with data.
- Fix: grade it "conflicting [O], rescue HYP (code-pending)" until a propagation simulation with a cosmological baseline exists.

## Minor
- m1 (CMB floor, `09-microwave…`): u_* ≈ 5.2×10⁻¹⁶ J m⁻³ is back-computed from the observed 2.725 K and the assumed factor 80, so "the energy balance … closes self-consistently" is circular. Also cite the COB measurement used for "within the band" (e.g. Lauer+2022 New Horizons, about 11–16 nW m⁻² sr⁻¹, giving about 4–7×10⁻¹⁶ J m⁻³).
- m2 (Hubble tension): "reproduced for ηδ_loc ≈ 0.09" (and 0.08 in the v2 text) is a two-parameter tune to one number. It is correctly tagged HYP; replace "reproduced" with "reachable".
- m3 (App. H 5-line check): the comment "RAR scale ~1.08e-10" mislabels the prediction as the empirical scale, which is ~1.2e-10.
- m4 (SPARC): "175 rotation-dominated late-type galaxies": SPARC has 175 galaxies of all types. Give the quality cuts and the number of galaxies actually used.
- m5 (§7): time dilation is "built in". Cite the data it is compared with (Blondin+2008; DES 2024 b ≈ 1) and give its error bar.
- m6 (§7): the angular-size discriminator is honestly scoped as presently undecidable. This is good practice.
- m7 (`IRREPRODUCIBILITY_LEDGER.md`): the summary says "none is a contradiction with observation". C3 and M7 contradict this.
- m8: `02-back-calculation…/ch2_backcalc_spectrum.py` claims a "zero tuned constants" invariant, but the illustrative widths w = 2/5000 are chosen; its width sweep does support the qualitative conclusion.

## Proposed data-pending / code-pending entries (for the ledger)
| item | needs |
|---|---|
| NGC 2403 fit at derived a₀ | `ch6_galaxy_rar.py` + SPARC file (sha-pinned); re-run at 1.082e-10 |
| SPARC-175 vs MOND | the archive 10.5281/zenodo.17622357 mirrored; M/L and thickness disclosed as fitted |
| a₀ ∝ H(z) | high-z RC sample comparison (Genzel+ KMOS3D/SINS) |
| SN Hubble diagram | full Pantheon+ covariance; report Δχ² |
| Bullet offset | Clowe+2006 κ map + Chandra X-ray; χ² |
| BAO | VP-law fit to DESI DR1/BOSS D_V/r_d |
| CMB peaks 2–3, BBN Y_p, D/H | listed as conflicting/data-pending, not out of scope |
| γ-ray dispersion rescue | propagation code over a cosmological baseline vs Fermi GRB 090510 |
| All App. H "S" rows | commit scripts; gate numbers + digests |
