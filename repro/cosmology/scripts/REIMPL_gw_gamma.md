# Re-implementation: gravitational waves and gamma (cosmology volume)

Date: 2026-09-28. The four scripts below are cited on the cosmology site pages, but the files were lost. They have been re-implemented here in the legacy v2.3 style, with Python 3.11 and numpy 2.4.6.

- **Conventions:** each script is deterministic (SEED = 19) and ends with a 2×SHA-256 digest taken over its results at 6 significant figures.
- **Figures:** plotting is optional; set `MPLBACKEND=Agg`.
- **What was run:** every script was run in full. `ch11_grav_waves.py` and `ch2_gamma_collective.py` were each run twice, and each gave the same digest both times.
- **Tuning:** no parameter was adjusted toward a number on a page. Probe choices, such as lattice size, pulse width and amplitude, are disclosed in each docstring.

| Script | Runtime | Digest |
|---|---|---|
| `ch11_grav_waves.py` | ~2 min | `61a24c0f…` |
| `ch2_gw_gamma_3d.py` | ~2.5 min | `2a6cc83d…` |
| `ch2_gw_gamma_arriving.py` | <1 s | `db1f0216…` |
| `ch2_gamma_collective.py` | ~75 s | `b74aba37…` |

## Results table

| script | page claim (quoted, page path) | reproduced value | match? | notes |
|---|---|---|---|---|
| ch11_grav_waves.py (A0) | "lattice pulse speed 1.000c" (`axb-reproducibility-map/`); "transverse pulse on elastic lattice, c=sqrt(K/rho)=1 … measured pulse speed = 1.000 c" (`11-gravitational-waves-medium-perturbations/`) | 1-D chain (K=m=a=1), compression pulse launched from rest: **0.9991 c**. The same chain carrying a genuinely transverse pulse (central springs, zero tension) moves **0.00 sites in t=150**, so it does not propagate. | yes for the compression pulse; **no** for a real transverse pulse | "1.000 c" can only be reproduced by a scalar chain, where "transverse" is just a label, or by a chain that is given tension. Central springs at rest length have no linear transverse restoring force. |
| ch11_grav_waves.py (A, new) | "a gravitational wave … travelling at exactly the speed of light, c_gw=√(K/ρ)=c, with no tuning" (`11-…`) | 3-D jammed soft-sphere packing, built with numpy (N=2500). The speed of the breathing ("opening/closing") mode is measured from the dynamics as ω/k. Results by packing fraction φ: **0.70** (z=8.15): c_L/√(C11/ρ)=0.965–0.997, c_L/√(B/ρ)=1.11–1.15. **0.66** (z=7.06): 0.965–0.990 and 1.05–1.08. **0.65** (z=6.64): 1.004–1.025 and 1.04–1.06. | yes, in the sense that the speed comes out of the lattice | The breathing-wave speed is the longitudinal elastic speed √(C11/ρ), where C11 ≈ B+4G/3. It exceeds c=√(B/ρ) by the G term, and that gap shrinks as z→6. Opening 5–7% of the contacts, the literal "opening" regime, changes the speed by less than 3%. |
| ch11_grav_waves.py (A, polarisation) | "a propagating shear … quadrupole radiation with two transverse polarisations … the shear character … removes [the breathing mode]" (`11-…`) | Transverse mode c_T=√(C66/ρ) to within 9%. c_T/c_L = **0.40 → 0.33 → 0.28** as z goes 8.15 → 7.06 → 6.64. G/B = 0.255 → 0.141 → 0.090. | **conflict** | See the section below. The author's mechanism (breathing) and the page's text (shear/TT) contradict each other. Shear was **not** implemented as the GW carrier. |
| ch11_grav_waves.py (B) | "chirp (M_c=28M_odot) 35→250 Hz in 0.19s" (`axb-…`, `11-…`) | **0.1902 s** (RK4 and closed form agree) | yes | This is standard GR: the quadrupole coefficient is imported, as the page itself says. It is degenerate with GR and is not a lattice result. |
| ch11_grav_waves.py (B) | "Hulse–Taylor dot P_b=-2.40×10⁻¹² (degenerate)" | **−2.4026e-12** (Peters–Mathews formula with the Weisberg & Huang 2016 parameters); observed intrinsic value −2.398e-12 | yes | Same caveat: this is GR arithmetic. |
| ch2_gw_gamma_3d.py | "remove a unit confusion … The arriving fluence is F=E_iso/(4π d²) … What reaches us is a broadband keV–GeV spectrum at modest fluence, exactly as the lattice-shake picture predicts" (`02-light-lattice-elastic-wave-sharpest/`) | 3-D scalar lattice, 128³, one localized shake. r²F(r) = 1.0000, 1.0000, 1.0000, 0.9985 at r=10–40, so the 1/(4πd²) law is reproduced on the lattice. Band arrival times: the low band (ka≲0.5) arrives at t=r/c. The high band arrives later, with lag/r = **0.046**; the independent-mode prediction from the exact dispersion is 0.040. The lag grows linearly with r. | fluence law: **yes**. "Arrives together as predicted": **no** | The broadband content does **not** arrive together. In 3-D, as in legacy `ch2_burstprop.py`, the high-k ("gamma") part lags in proportion to distance. |
| ch2_gw_gamma_arriving.py | "for GRB 170817A, F≈2.6×10⁻⁷erg cm⁻², the energy of 10⁻¹³s of sunlight … Only a Galactic-scale (kpc) burst delivers a dangerous fluence" (`02-light-lattice-…`) | From E_iso=3.1e46 erg (Goldstein+2017) at 40 Mpc: F = **1.62e-7** (range 0.87–4.7e-7 over the quoted errors). The measured GBM fluence is 2.8e-7. That is **1.2–2.1e-13 s** of sunlight. The danger radius at 100 kJ m⁻² is **2.9 kpc** for 1e53 erg and 0.9 kpc for 1e52 erg. | yes, within the input uncertainties | The page's 2.6e-7 implies E_iso ≈ 5.0e46 erg at 40 Mpc; its source is not stated. GW fluence is > 0.23 erg cm⁻² if E_GW > 0.025 M☉c². That input still needs checking against the LIGO/Virgo paper. This script is bookkeeping only and does not test the VP mechanism. |
| ch2_gamma_collective.py (P2) | "a linear independent-mode packet disperses (peak ×0.45, leading width ×1.25), while the collective FPU-β disturbance forms a sharp coherent front (peak ×2.84, leading width ×0.50)" (`02-light-lattice-…`; also `16-open-problems-gathered/`) | Same launch, w=3, strain 0.5, read at D=1500 cells. **Linear:** peak ×0.478, width ×2.64. **FPU-β:** peak ×1.30, width ×0.43. At D=3000 the linear run gives ×0.388 and ×3.29. At strain 0.05, FPU-β behaves linearly: ×0.49 and ×2.57. | **no** (qualitatively the same direction) | The ratios depend on the distance at which they are read, and the pages do not state that distance. The page's ×2.84 peak growth was not obtained. |
| ch2_gamma_collective.py (P3) | "the bands staying locked … The collective mode supplies exactly that coherence: the broadband packet … arrives together" (`02-light-lattice-…`); "#1 Gamma broadening … resolved" (`axj-version-history-reclassification-log/`) | Strong FPU front: 92% of the high-band energy rides inside the soliton, so the soliton's own spectrum is locked. **But the front runs at 1.105 c**, and it separates from the low-k (GW-like) part in proportion to distance (lag −40 → −76 cells from D to 2D). Linear and weak cases: the lag equals the independent-mode prediction (68 vs 69 cells, then 141 vs 138). | **no** | Locking needs bond strain of O(0.1–1). Even then the collective front is supersonic and amplitude-dependent, about 10¹⁴ × the GW170817 limit \|Δv/c\| < 1e-15. The "resolved" grade in `axj-…` is not supported. Legacy `ch2_burstprop.py` reached the same negative result. |
| ch2_gamma_collective.py (P4) | "independent 10MeV and 10keV modes over L=130Mly would arrive Δt≈3×10¹⁹s apart … E_QG(D)≈115keV against the bound >1.3×10²⁰eV, 15 orders" | Δt(D) = **3.11e19 s**; E_QG(D) = 1.150e5 eV (15.1 orders); E_QG(a) = 8.82e11 eV (8.2 orders); Δt(a) = 5.3e5 s | yes (arithmetic) | Caveat: on a D-lattice the zone edge is 128 keV. A 10 MeV mode has ka ≈ 246 ≫ π, so the quadratic formula is being applied far outside its range. |
| ch2_gamma_collective.py (P4) | "GW170817 bounds gamma and gravitational waves to within 1.7s over that distance (effective E_QG>10¹⁰eV)" | E_QG,2 > **4.9e11 eV** at E=10 keV, 4.9e12 eV at 100 keV, 4.9e13 eV at 1 MeV | **no** | The page's 1e10 eV cannot be reproduced from 1.7 s and 40 Mpc for any GBM-band energy. The correct bound is 1.5–3.5 orders stronger. With the 100 keV–1 MeV figures, E_QG(a) = 8.8e11 eV fails the bound. |

## What the lattice run shows about GW speed and polarisation content

**Speed.** The breathing wave was implemented as the author describes it: the jammed lattice opening and then closing. It propagates at a speed the lattice produces by itself. No speed was put into the model: ω is fitted from a standing mode released from rest. The measured speed equals the longitudinal elastic speed √(C11/ρ) to within 3.5% at all three packing fractions and both wavenumbers. It sits above the physics volume's light speed c = √(B/ρ) by the shear term: C11 − B ≈ 4G/3, which was measured directly (0.150 vs 0.155, 0.063 vs 0.067, 0.022 vs 0.037).

As the packing approaches the isostatic point (z = 8.15 → 6.64), the ratio c_breathing/√(B/ρ) falls from about 1.13 to about 1.05. The physics volume's data (`repro/physics/bundle_v0.4/.../01_stiffness_to_c2`, G_relaxed → 0 at z = 6) imply that the ratio reaches 1 there. So "c_gw = c with no tuning" holds, but for a specific reason: at the isostatic point the breathing wave and light, the single surviving c² = B/ρ wave, are the same longitudinal mode. Their speeds are equal because they are one mode, not two modes that happen to agree. The framework does not yet say what would distinguish a GW from light in that case. This should be recorded as an open item.

The "opening" regime (peak strain equal to the mean contact overlap, with 5–7% of contacts actually opening) shifts the speed by less than 3%. Opening and closing does not change the speed at these amplitudes.

**Polarisation content.** On the same packings, the transverse (shear) channel propagates at √(G/ρ), confirmed to within 9%. Its speed relative to the breathing wave falls from 0.40 to 0.28 as z → 6.6, and G/B falls from 0.26 to 0.09. At the isostatic point, where the physics volume sets G → 0, the medium carries **one** propagating polarisation: the scalar, longitudinal breathing mode. This conflicts with the ch.11 page (`11-gravitational-waves-medium-perturbations/`) in three ways:

- The page calls the GW "a propagating shear of the same medium".
- It says the page's GW has "exactly two independent polarisations, h₊ and h×".
- It says "the shear character of the gravitational perturbation removes [the breathing mode]".

In the physics volume's substrate there is no shear stiffness to carry h₊ and h×. The breathing mode the page says is removed is the only mode that survives.

This is also an observational problem. LIGO/Virgo polarisation tests strongly disfavour pure-scalar polarisation against tensor: GW170814 (PRL 119, 141101) and later events such as GW170817 are cited for this. A GW carried only by the breathing mode would conflict with those tests. The polarisation-count claim should therefore be regraded from "degenerate with GR" to a conflict or open item [O]. It should not be implemented as shear, because the substrate has G → 0.

**A further inconsistency to record.** Legacy `ch2_jammed2d.py` models jamming as incompressibility: a longitudinal channel frozen at infinite speed, with light treated as transverse. The physics volume says the opposite: G → 0, B finite, and light is the longitudinal c² = B/ρ wave. The GW scripts here follow the physics volume.

## Files

- Scripts: `ch11_grav_waves.py`, `ch2_gw_gamma_3d.py`, `ch2_gw_gamma_arriving.py`, `ch2_gamma_collective.py`, all in `repro/cosmology/scripts/`.
- Figures written when the scripts run: `ch11_grav_waves.png`, `ch2_gw_gamma_3d.png`, `ch2_gamma_collective.png`.
- Nothing under `docs/` was edited.
