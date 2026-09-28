# Cosmology: re-implemented reproduction scripts (2026-09-28)

The site pages cite about 50 scripts. Twenty-seven of them came back in the author's older package, [`../legacy_v2_3/`](../legacy_v2_3/), and still run. The other **23 had been lost and were re-implemented here** from what the pages say they did.

- **No tuning.** No parameter was adjusted to reach a page number. Where a page number does not come out, the honest result is kept and the mismatch is listed below.
- **Requirements.** numpy only (matplotlib is optional and needs `MPLBACKEND=Agg`). Output is deterministic, and every script runs in under about 3 minutes.
- **Detail.** The full table of page claim versus reproduced value, one row per script, is in the `REIMPL_*.md` files in this folder.

| Group | Scripts | Report |
|---|---|---|
| Orbits (Kepler, core) | ch4_orbits, ch5_mercury_capture, ch_spin_locking, ch10_post_newtonian | [REIMPL_orbits.md](REIMPL_orbits.md) |
| Gravitational waves, gamma | ch11_grav_waves, ch2_gw_gamma_3d, ch2_gw_gamma_arriving, ch2_gamma_collective | [REIMPL_gw_gamma.md](REIMPL_gw_gamma.md) |
| Supernovae, lensing, Bullet | ch7_sne, ch_hubble_tension, ch8_bullet_offset, ch8_lensing_consistency | [REIMPL_sne_lensing.md](REIMPL_sne_lensing.md) |
| CMB, acoustic length | ch9_cmb_floor, ch14_cmb_aniso, sim_acoustic_peaks, derive_acoustic_length, acoustic_length_hypothesis_interpretation, probe_subhorizon_desert, ch15_lss_bao | [REIMPL_cmb_acoustic.md](REIMPL_cmb_acoustic.md) |
| Puzzles, BBN, jets, Sun | ch12_puzzles, ch13_bbn, ch_jet_acceleration, ch_solar_activity | [REIMPL_misc.md](REIMPL_misc.md) |

## Headline outcomes

- **Kepler.** Every planetary period comes out within 0.06% when the planet masses are included, and T²/a³ = 1.00000000. The 0.73% quoted on the page traced back to a wrong Saturn semi-major axis in the old script.
- **Post-Newtonian.** Light bending is 1.7512″, Mercury's perihelion advance is 42.99″/century, and the redshift is 2.455e-15. All three are degenerate with GR, as the pages say.
- **Supernovae.** The page numbers reproduce: χ²/dof = 0.499 (VP) against 0.444 (ΛCDM). That gap is **Δχ² = +86.6 in favour of ΛCDM**, with one marginalised offset in each model and diagonal errors. The fit is not degenerate.
- **Bullet offset.** It does **not** reproduce. The page gives 0.41 Mpc. With the page's own inputs, 0.275 Mpc comes out from a uniform path and 0.497 Mpc from a β-model. The inputs are hand-chosen, and the mechanism is plain ram pressure, so the offset does not test the deficit.
- **Gravitational waves.** On a 3-D jammed packing, the "opening and closing" (breathing) wave propagates at a speed that comes from the lattice itself, √(C11/ρ) to within 3.5%. As G → 0 it approaches √(B/ρ).
  - At the isostatic point only this one scalar (breathing) polarisation survives, because shear dies with G.
  - The ch.11 page's claim of "shear, two TT polarisations" is therefore not supported by the lattice.
  - How a purely scalar polarisation compares with detector-network polarisation tests is an open item.
- **Gamma collective front.** The page ratios do not reproduce. The strong front keeps about 92% of its high-k content, but only while travelling at 1.105c, which depends on amplitude. The bound E_QG > 10¹⁰ eV does not follow. The correct bound is at least 4.9×10¹¹ eV.
- **CMB and acoustic.**
  - These reproduce: θ = 0.818°, a single bump near ℓ ≈ 220 with no higher peaks, r_s = 144.4 Mpc, and the synchronised-phase peaks.
  - These do not: the cavity peak heights, the 10-decade gap (20.1 comes out), the 0.075c velocity (0.035c comes out), β̂ (0.464 comes out, not 0.501), and 3π² (3.7% off, not within 1%).
- **BBN, jets, Sun.** Y_p = 0.250 is textbook arithmetic, not a VP output; a rough independent estimate gives 0.19. For jets, Γ∞ = w₀ follows from Bernoulli, so it is an input rather than a prediction, and the opening angles fail for GRBs. The solar negative result reproduces. The page's "10¹²⁰" is 10¹²² by its own numbers.

External values that were quoted from memory, such as the COB measurements, the Planck θ_D and the GW170817 E_GW, are flagged in the reports and need checking against the source papers.
