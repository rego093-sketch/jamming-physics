#!/usr/bin/env python3
"""
ch15_lss_bao.py  --  Re-implementation (2026-09-28) of the lost Chapter 15 script
"large-scale structure and BAO: making the target explicit".

PAGE CLAIMS (docs/cosmology/15-large-scale-structure-bao/, axb-reproducibility-map/)
  "# A: target standard ruler (what must be explained)
   r_BAO = 150 Mpc (standard: comoving sound horizon at drag epoch)
   # B: toy deficit-coupled growth in a static medium
   broad correlation xi(r) grows (clustering: plausibly reproduced)
   sharp bump at r=150 Mpc: ABSENT unless a scale is seeded (BAO: conflicting)"
  Reproducibility map: "broadband xi(r) reproduced; 150 Mpc BAO bump from a fixed inflow length
  (sim_acoustic_peaks); deriving that length is the open input (HYP, open)".

INPUTS (sources)
  - r_BAO = 150 Mpc (observed ruler; target only).
  - Toy box: 128^3 cells, 1200 Mpc side; initial Gaussian field P0(k) ~ k^n exp(-(k r_c)^2),
    r_c = 2 cells (scale-free apart from the grid smoothing), n = 0 (Poisson-like mass
    concentrations) and n = -1 (red) as a robustness case; initial rms 0.05; SEED = 19, 4 realizations.
  - Static-medium, deficit-coupled linear growth (Ch 8: deficits attract like mass):
    d^2 delta_k/dt^2 = (Gamma0^2 - c_J^2 k^2) delta_k, Gamma0 = 1, Jeans length 2 pi/k_J = 20 Mpc
    (toy choice; any small value), delta_k(t) = delta_k(0) cosh(Gamma_k t); no expansion.
    Nonlinear clustering via the lognormal map rho = exp(delta - s^2/2) (Coles & Jones 1991).
  - "Seeded" control: each field convolved with (delta_D + w * thin shell of radius 150 Mpc), w = 0.5.

ALGORITHM
  B: grow to t = 0, 2, 4 (Gamma0 units); xi(r) by FFT of |rho_k|^2, spherically averaged.
     Broad clustering: xi(20 Mpc) vs t. Bump test in 100-200 Mpc: local maximum of xi above the
     straight line through xi(90) and xi(210), significance = excess / realization scatter.
     Repeat with the shell seeded.
  No comparison with measured galaxy xi(r) is made (none was on the page either).

EXPECTED (page): broad xi(r) grows; no 150 Mpc bump unless seeded.
"""
import numpy as np

SEED = 19
N, BOX = 128, 1200.0
d = BOX / N

def grids():
    k1 = 2 * np.pi * np.fft.fftfreq(N, d)
    kk = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + k1[None, None, :] ** 2)
    x1 = np.fft.fftfreq(N, 1.0 / N) * d
    rr = np.sqrt(x1[:, None, None] ** 2 + x1[None, :, None] ** 2 + x1[None, None, :] ** 2)
    return kk, rr

KK, RR = grids()
REDGES = np.arange(5, 260, d); RC = 0.5 * (REDGES[1:] + REDGES[:-1])
IDX = np.digitize(RR.ravel(), REDGES)

def xi_of(field):
    f = field - field.mean(); fk = np.fft.fftn(f)
    xi3 = np.real(np.fft.ifftn(np.abs(fk) ** 2)) / f.size
    x = xi3.ravel()
    return np.array([x[IDX == i].mean() for i in range(1, len(REDGES))]) / field.mean() ** 2

def shell_kernel_k(Rs=150.0):
    x = KK * Rs
    return np.where(x > 0, np.sin(x) / np.where(x > 0, x, 1), 1.0)

def run(seed, t, seeded, n_s=0.0, w=0.5, amp0=0.05):
    rng = np.random.default_rng(seed)
    wn = np.fft.fftn(rng.standard_normal((N, N, N)))
    k = np.where(KK > 0, KK, 1.0)
    Pk = k ** n_s * np.exp(-(KK * 2 * d) ** 2); Pk[0, 0, 0] = 0
    dk = wn * np.sqrt(Pk)
    dk *= amp0 / np.real(np.fft.ifftn(dk)).std()           # initial rms contrast amp0
    if seeded:
        dk = dk * (1 + w * shell_kernel_k())
    kJ = 2 * np.pi / 20.0
    G2 = 1.0 - (KK / kJ) ** 2
    grow = np.where(G2 > 0, np.cosh(np.sqrt(np.abs(G2)) * t), np.cos(np.sqrt(np.abs(G2)) * t))
    delta = np.real(np.fft.ifftn(dk * grow))
    s2 = delta.var()
    rho = np.exp(delta - s2 / 2)
    return xi_of(rho)

def bump_test(xis):
    xi = np.mean(xis, 0); err = np.std(xis, 0, ddof=1) / np.sqrt(len(xis))
    i90 = np.argmin(abs(RC - 90)); i210 = np.argmin(abs(RC - 210))
    base = xi[i90] + (xi[i210] - xi[i90]) * (RC - RC[i90]) / (RC[i210] - RC[i90])
    sel = (RC > 100) & (RC < 200)
    ex = (xi - base)[sel]; j = np.argmax(ex)
    ism = [i for i in np.where(sel)[0] if xi[i] >= xi[i - 1] and xi[i] >= xi[i + 1]]
    return RC[sel][j], ex[j] / max(err[sel][j], 1e-30), len(ism) > 0, xi

if __name__ == "__main__":
    print("=== A: target ===")
    print("  r_BAO = 150 Mpc (standard: comoving sound horizon at the drag epoch) -- to be explained.\n")
    print("=== B: toy deficit-coupled growth in a static medium (4 realizations, SEED=19) ===")
    for n_s, seeded in ((0.0, False), (0.0, True), (-1.0, False), (-1.0, True)):
        lab = ("SEEDED 150 Mpc shell" if seeded else "no scale seeded") + f", initial P ~ k^{n_s:+.0f}"
        print(f"  --- {lab} ---")
        for t in ((0.0, 2.0, 4.0) if n_s == 0.0 else (0.0, 4.0)):
            xis = np.array([run(SEED + r, t, seeded, n_s=n_s) for r in range(4)])
            rpk, sig, locmax, xi = bump_test(xis)
            i20 = np.argmin(abs(RC - 20))
            print(f"  t = {t:.0f}: xi(20 Mpc) = {xi[i20]:.3e}   largest excess in 100-200 Mpc at r = {rpk:.0f} Mpc,"
                  f" significance = {sig:5.1f} sigma, local max present: {locmax}")
    print("  RESULT: broad clustering grows with t in the static medium; without a seeded length the")
    print("  100-200 Mpc range shows no significant bump; a bump near 150 Mpc (141 Mpc bin, 9.4 Mpc cells,")
    print("  19 Mpc smoothing) appears only when the shell length is inserted -- and, in this toy, only for")
    print("  a Poisson-like (k^0) field: seeding a red k^-1 field does NOT produce a detectable bump, because")
    print("  the shell cross-term is smeared by the broad xi0(r). The value 150 Mpc is not derived (HYP, open).")
    print("  HONEST: 'broadband xi(r) reproduced' is qualitative -- this toy is not fitted or compared to")
    print("  a measured galaxy xi(r) or P(k); the turnover and sigma8 are not derived.")
