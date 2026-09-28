# Cosmology reproduction package v2.3 (recovered legacy)

**Provenance.** The author supplied this package on 2026-09-28 as `VP_reproducibility_v2_3.zip`, describing it as older material. It predates the current site pages. It is vendored unchanged; only the figure PNGs and the whitepaper `.tex` are left out.

**Run.** `bash run_all.sh` needs Python ≥ 3.8 and numpy. It takes about 4 minutes and is deterministic. On 2026-09-28 it gave **27 ok, 0 failed** with numpy 2.4.6. The full output is in `RUN_2026-09-28.log`.

**Data included.**
- `NGC2403_rotmod.dat` (SPARC)
- `Pantheon+_extract.tsv` (Pantheon+, N = 1580; Scolnic et al. 2022, Brout et al. 2022)

## What the recovered code settles

1. **NGC 2403 fit.** `ch6_galaxy_rar.py` (C) fits at the empirical a₀ = 1.2×10⁻¹⁰ m/s². It does not use the derived cH₀/2π. The code says so in a comment (`a0 = 1.2e-10  # empirical RAR scale (for the fit)`). The page values Υ = 0.567 and χ²/dof = 1.99 come from that empirical-a₀ fit.
2. **The 2π in a₀ = cH₀/2π.**
   - `ch6_galaxy_rar.py` (D) states that the data fix the coefficient k in a₀ = cH₀/k only to 5–7. At H₀ = 70 the central value is about 5.7.
   - The code's own words: "the coefficient is SELECTED by motivation + match, NOT derived … Only a0 ~ cH0 is secure."
   - The site pages grade the 2π [F]. The code does not support that grade.
3. **Supernovae.**
   - `ch7_lattice_optics.py` (A) reproduces χ²/dof = 0.499 (VP) against 0.444 (ΛCDM) on the same 1580 SNe.
   - That is Δχ² ≈ 0.055 × 1578 ≈ 87 in favour of ΛCDM, with diagonal errors only.
   - The code labels the result "degenerate / comparable". The data say VP is disfavoured.
   - χ²/dof < 1 for both models shows the diagonal errors are inflated. With the full covariance the gap would not shrink.
4. **Honest labels already present in this code** that the pages dropped:
   - the Hubble-tension mechanism is "a candidate mechanism … NOT a parameter-free prediction";
   - the curve shape is "degenerate with MOND/dark halos".

## Still missing

About 24 scripts are cited on the site pages but are not in this package or anywhere in the repo. Until code is recovered, the results that rest on them are data-pending:

- `ch10_post_newtonian.py`
- `ch11_grav_waves.py`
- `ch12_puzzles.py`
- `ch13_bbn.py`
- `ch14_cmb_aniso.py`
- `ch15_lss_bao.py`
- `ch2_gamma_collective.py`
- `ch2_gw_gamma_3d.py`
- `ch2_gw_gamma_arriving.py`
- `ch4_orbits.py`
- `ch5_mercury_capture.py`
- `ch7_sne.py`
- `ch8_bullet_offset.py`
- `ch8_lensing_consistency.py`
- `ch9_cmb_floor.py`
- `ch_hubble_tension.py`
- `ch_jet_acceleration.py`
- `ch_solar_activity.py`
- `ch_spin_locking.py`
- `derive_acoustic_length.py`
- `acoustic_length_hypothesis_interpretation.py`
- `probe_subhorizon_desert.py`
- `sim_acoustic_peaks.py`

Several of these are later versions of scripts in this package; for example, `ch7_sne.py` likely supersedes `ch7_lattice_optics.py` (A).
