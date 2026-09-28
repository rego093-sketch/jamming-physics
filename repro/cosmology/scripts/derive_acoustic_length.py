#!/usr/bin/env python3
"""
derive_acoustic_length.py  --  Re-implementation (2026-09-28) of the lost Ch 14.1/15 audit
"attacking the three criteria head-on" (deterministic, constants only).

PAGE CLAIMS (docs/cosmology/14-acoustic-length-structurally-hard/; also 15-large-scale-structure-bao/,
             16-open-problems-gathered/, 16-honest-ledger-falsifiable-predictions/, axj-...)
  (i)  "The inflow clock sets only microscopic scales -- the per-nucleon length c/nu_p ~ 10^3 km, and a
       cosmic-mean inflow length far larger than the horizon -- which miss 150 Mpc by roughly nineteen
       and thirty-five orders of magnitude. The only scales of cosmological order are the Hubble length
       c/H0 ~ 4300 Mpc and 2 pi c/H0. Reaching 150 Mpc would require dividing the Hubble length by
       ~28.6, a pure order-ten number with no forced origin in the pi-chain nu_n = n pi^(2(n-1)) ...
       Criterion (i) therefore does not close."
  (ii) "standing-wave cavity: peaks at k*L/pi = 1,2,3,4 heights 1.00, 0.20, 0.91, 0.17
        odd>even alternation: 1st>2nd and 3rd>2nd (baryon signature)
        isolated shell |sinc|^2: peaks shifted, heights 1.00, 0.35, 0.18, 0.11"
       with Theta(k) = (1+R) cos(kL) - R and Silk damping; R and the damping scale are standard inputs.
  (iii) "A 150 Mpc standing wave is ... nu ~ 3e-17 Hz. A 10 GeV burst photon sits at nu ~ 2e24 Hz --
       some forty-one orders higher ... c/a only about two orders above the gamma-ray scale."
  Tally on the page: (iii) closed, (ii) closed at mechanism level, (i) OPEN.

INPUTS (sources)
  - c, h, eV (CODATA 2018); 1 Mpc = 3.0856775814913673e22 m; G = 6.674e-11.
  - H0 = 70 km/s/Mpc (the page's "28.6 at H0 = 70"); target L = 150 Mpc (observed ruler; TARGET only).
  - nu_p = 3 pi^4, nu_H = 3 pi^4 + 1, pi-chain nu_n = n pi^(2(n-1)) (legacy ch1_inflow_rates.py).
  - m_H = 1.6735e-27 kg; a = 6.33e-19 m (legacy ch9_lattice_cmb.py); D = 4.8526e-12 m (Ch 2 page).
  - rho_c = 3 H0^2 / (8 pi G).
  - "cosmic-mean inflow length" is RECONSTRUCTED here as c / (per-cell inflow rate) with per-cell
    rate = (nu_H/m_H) * rho_c * a^3 (inflow quanta per second per lattice cell at the mean
    cosmic density). The page does not print the formula; this reading reproduces its 35 orders.
  - Baryon loading R = 0.6 (page: "the R ~ 0.6 used in the height calculation").
  - Damping (standard input, not tuned): Planck 2018 angular scales 100 theta_* = 1.0411,
    100 theta_D = 0.1606 (values quoted from memory of Planck 2018 VI, Table 2) -> k_D L =
    pi theta_*/theta_D; Hu & Sugiyama amplitude damping exp(-(k/k_D)^2), power exp(-2(k/k_D)^2).
  - 10 GeV photon; lattice cut-off frequency c/a.

ALGORITHM
  (i)  tabulate every framework length and log10(L/150 Mpc); factor F = (c/H0)/150 Mpc; distance of
       F to every pi-chain member (n = 1..5) and to a small set of 'natural' geometric factors.
  (ii) numerically maximise |Theta|^2 D^2 on kL/pi in [0.5, 4.5]; report positions and heights
       (normalised to the first); same for the thin-shell |sin x / x|^2 side lobes; also the undamped
       cavity as a bracket.
  (iii) nu_L = c/(2L); nu_gamma = E/h; orders of separation; c/a vs nu_gamma.

EXPECTED (page): (i) ~19 and ~35 orders; F ~ 28.6; no forced origin -> OPEN.
  (ii) cavity 1.00, 0.20, 0.91, 0.17 (alternating); shell 1.00, 0.35, 0.18, 0.11.  (iii) 41 orders.
"""
import numpy as np

c = 2.99792458e8; h = 6.62607015e-34; eV = 1.602176634e-19; G = 6.674e-11
Mpc = 3.0856775814913673e22
H0 = 70e3 / Mpc; L_T = 150 * Mpc
nu_p = 3 * np.pi ** 4; nu_H = nu_p + 1; m_H = 1.6735e-27
a = 6.33e-19; D = 4.8526e-12
rho_c = 3 * H0 ** 2 / (8 * np.pi * G)

def criterion_i():
    rate_cell = (nu_H / m_H) * rho_c * a ** 3
    L = {"lattice cell a": a, "light scale D": D, "c/nu_H (hydrogen)": c / nu_H,
         "c/nu_p (per nucleon)": c / nu_p, "cosmic-mean inflow length (recon.)": c / rate_cell,
         "Hubble length c/H0": c / H0, "a0 length 2 pi c/H0": 2 * np.pi * c / H0}
    F = (c / H0) / L_T
    chain = {f"nu_{n} = {n} pi^{2*(n-1)}": n * np.pi ** (2 * (n - 1)) for n in range(1, 6)}
    geo = {"2": 2, "pi": np.pi, "2pi": 2 * np.pi, "4pi": 4 * np.pi, "pi^2": np.pi ** 2,
           "2pi^2": 2 * np.pi ** 2, "4pi^2": 4 * np.pi ** 2, "8pi": 8 * np.pi, "e^pi": np.e ** np.pi}
    return L, F, chain, geo

def cavity_heights(R=0.6, kDL=None, n=4):
    x = np.linspace(0.5, n + 0.5, 400001) * np.pi               # x = kL
    Th = (1 + R) * np.cos(x) - R
    Dm = np.exp(-(x / kDL) ** 2) if kDL else 1.0
    P = (Th * Dm) ** 2
    pos, hts = [], []
    for j in range(1, n + 1):
        s = (x > (j - 0.5) * np.pi) & (x < (j + 0.5) * np.pi)
        i = np.argmax(P[s]); pos.append(x[s][i] / np.pi); hts.append(P[s][i])
    hts = np.array(hts)
    return np.array(pos), hts / hts[0]

def shell_heights(n=4):
    x = np.linspace(1e-6, (n + 1.5) * np.pi, 800001); P = (np.sin(x) / x) ** 2
    pk = [i for i in range(1, len(P) - 1) if P[i] > P[i - 1] and P[i] > P[i + 1]][:n]
    return x[pk] / np.pi, P[pk] / P[pk[0]]

def criterion_iii(E_GeV=10.0):
    nu_L = c / (2 * L_T); nu_g = E_GeV * 1e9 * eV / h; nu_a = c / a
    return nu_L, nu_g, np.log10(nu_g / nu_L), nu_a, np.log10(nu_a / nu_g)

if __name__ == "__main__":
    print("=== Criterion (i): derive the length from framework constants ===")
    L, F, chain, geo = criterion_i()
    for k, v in L.items():
        print(f"  {k:36s} {v:11.3e} m  = {v/Mpc:11.3e} Mpc   log10(L/150 Mpc) = {np.log10(v/L_T):+7.2f}")
    print(f"  required factor F = (c/H0)/150 Mpc = {F:.3f}  (H0 = 70)")
    best = min(chain.items(), key=lambda kv: abs(np.log(kv[1] / F)))
    print("  pi-chain members: " + ", ".join(f"{k.split(' =')[0]}={v:.3g}" for k, v in chain.items()))
    print(f"    nearest: {best[0]} = {best[1]:.3f} ({100*(best[1]/F-1):+.0f}%)  -> no pi-chain member near F")
    near = sorted(geo.items(), key=lambda kv: abs(np.log(kv[1] / F)))[:3]
    print("  nearest simple geometric factors: " + ", ".join(f"{k}={v:.2f} ({100*(v/F-1):+.1f}%)" for k, v in near))
    print("  RESULT (i): NOT CLOSED. No framework length within tuning-free reach; choosing a factor")
    print("  to land on 28.6 would be post-hoc tuning. Missing object: a cosmological cavity length.\n")

    print("=== Criterion (ii): peak heights from a genuine standing wave ===")
    kDL = np.pi * 1.0411 / 0.1606
    for lab, kd in (("undamped (bracket)", None), (f"Planck-damped k_D L = {kDL:.2f}", kDL)):
        p, hh = cavity_heights(kDL=kd)
        print(f"  cavity, R=0.6, {lab:26s}: peaks kL/pi = {np.round(p, 3).tolist()}  heights = {np.round(hh, 2).tolist()}")
        print(f"    odd>even alternation: 1st>2nd {hh[0] > hh[1]}, 3rd>2nd {hh[2] > hh[1]}, 3rd>4th {hh[2] > hh[3]}")
    ps, hs = shell_heights()
    print(f"  isolated shell |sin x/x|^2 side lobes: kL/pi = {np.round(ps, 3).tolist()}  heights = {np.round(hs, 2).tolist()}"
          f"  (monotone, no alternation)")
    print("  PAGE: cavity heights 1.00, 0.20, 0.91, 0.17 -- the page's damping scale is not recorded; with the")
    print("  Planck-derived damping above the 3rd/4th heights come out lower (see table). The alternation")
    R = 0.6; kmin = np.pi * np.sqrt(10 / np.log((1 + 2 * R) ** 2))
    print(f"  (the mechanism claim) survives while k_D L > {kmin:.2f} (3rd > 2nd); the specific heights depend on")
    print("  the damping input, which is external (standard-model) physics, not derived here.")
    print("  RESULT (ii): closed at the level of mechanism only (R and k_D are external standard inputs).\n")

    print("=== Criterion (iii): gamma-ray dispersion limit ===")
    nL, ng, od, na, oa = criterion_iii()
    print(f"  nu(150 Mpc standing wave) = c/2L = {nL:.2e} Hz;  nu(10 GeV) = {ng:.2e} Hz;  separation {od:.1f} orders")
    print(f"  lattice c/a = {na:.2e} Hz, {oa:.1f} orders above the 10 GeV scale (pre-existing Ch 2 tension)")
    print("  RESULT (iii): closed -- the background is a near-DC offset on gamma-ray scales.\n")
    print("TALLY: (iii) closed; (ii) closed at mechanism level; (i) OPEN (no constant moved).")
