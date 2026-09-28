#!/usr/bin/env python3
"""
ch_hubble_tension.py  --  Chapter 7.1: the Hubble tension as line-of-sight averaging of kappa_opt.

Re-implementation (2026-09-28) of a script cited on the site but lost. It extends part (C) of
legacy_v2_3/ch7_lattice_optics.py (which only did the algebra 1 + eta*delta_loc) by propagating
light through an explicit density field. numpy only.

CLAIM ON THE PAGES
------------------
  07-hubble-tension-line-of-sight-averaging: "ch_hubble_tension.py ... propagating light through a
     structured density field with kappa_opt(rho) = kbar (1+delta)^eta reproduces the 73/67
     magnitude for eta*delta_loc ~ 0.08 and exhibits the predicted H0-density correlation (slope
     set by eta), while the eta-delta_loc degeneracy and the sign of eta ... remain open".
  Same page, earlier paragraph (ch7_lattice_optics.py part C): "reproduced for eta*delta_loc ~ 0.09".
  axj / 16-open-problems: "73/67, eta*delta_loc ~ 0.08 (ch_hubble_tension.py)".
  The pages grade this HYP/SPEC: eta and delta_loc are NOT fixed by the framework.

MODEL
  ln(1+z(D)) = INT_0^D kappa_opt(s) ds,   kappa_opt = kbar (1+delta(s))^eta / <(1+delta)^eta>_global
  so a deep average returns H_global = c*kbar exactly, and a ladder that fits
  ln(1+z) = (H/c) D over a local window returns H_local.

INPUTS (sources; every item marked [HAND] is chosen here, not derived or measured)
  target ratios (measured): 73/67 = 1.0896 (page rounding);
      73.04/67.4 = 1.0837 (SH0ES, Riess et al. 2022 ApJL 934 L7; Planck 2018 VI, A&A 641 A6).
      Mapping Planck's CMB-inferred 67.4 onto the VP "deep line-of-sight average" is itself an
      interpretive assumption of the page (the VP volume rejects the LCDM CMB fit it comes from).
  [HAND] ladder window D = 100 .. 600 Mpc (~ SH0ES Hubble-flow SNe, 0.023 < z < 0.15), sources
         uniform in volume (n(D) ~ D^2), slope fitted through the origin.
  [HAND] part A: a top-hat local anomaly of radius R_loc around the observer.
  [HAND] part B: a 1-D log-normal random field along each sightline, cell 1 Mpc, Gaussian
         smoothing length L_s = 20 Mpc, log-amplitude sigma_g in {0.1, 0.2, 0.4}, SEED = 19.
  [FREE, not fixed] eta and delta_loc -- scanned, never tuned.

ALGORITHM
  A) Analytic: H_local/H_global - 1 = X * f(R_loc),  X = (1+delta_loc)^eta - 1,
     f = sum_D n(D) D min(D,R) / sum_D n(D) D^2. Solve for the X (hence eta*delta_loc along the
     eta-delta degeneracy line) that gives each measured ratio.
  B) Field: 2^20 Mpc of log-normal field; 16384 observers on a regular grid; each looks in +x and
     -x. For each sightline compute H_local/H_global; regress ln(H_local/H_global) on the
     window-weighted mean of ln(1+delta) (slope should be eta) and on the mean delta inside a
     200 Mpc local sphere (an observable proxy). Report direction scatter (+x vs -x) and the
     fraction of observers that see a ratio >= 1.0837.

EXPECTED OUTPUT: eta*delta_loc needed ~ ln(1.0837) = 0.080 .. ln(1.0896) = 0.086 in the full-
  filling limit (R_loc >= 600 Mpc), larger for smaller anomalies; regression slope ~ eta.

DETERMINISM: SEED = 19. Runtime ~ 10 s. DEPENDENCIES: numpy (matplotlib optional).
"""
import os
import numpy as np

SEED = 19
C_KMS = 299792.458
T_PAGE = 73.0 / 67.0
T_MEAS = 73.04 / 67.4
D_WIN = np.arange(100.0, 601.0, 1.0)          # [HAND] ladder window, Mpc
NW = D_WIN ** 2                                # sources uniform in volume
HERE = os.path.dirname(os.path.abspath(__file__))


def slope_through_origin(D, y, n):
    return np.sum(n * D * y) / np.sum(n * D * D)


def part_A():
    print("--- (A) top-hat local anomaly, analytic (eta, delta_loc free; degeneracy made explicit) ---")
    for R in (100.0, 200.0, 300.0, 600.0):
        f = slope_through_origin(D_WIN, np.minimum(D_WIN, R), NW)
        line = [f"  R_loc = {R:5.0f} Mpc: filling f = {f:.3f};"]
        for name, T in (("73/67", T_PAGE), ("73.04/67.4", T_MEAS)):
            X = (T - 1) / f
            line.append(f" {name}: need (1+d)^eta-1 = {X:.4f}")
        print("".join(line))
    print("  Degeneracy line for the full-filling case (f = 1), target 73.04/67.4 = %.4f:" % T_MEAS)
    for eta in (-1.0, -0.3, 0.5, 1.0, 2.0):
        d = T_MEAS ** (1 / eta) - 1
        print(f"    eta = {eta:+.2f}: delta_loc = {d:+.4f}, eta*delta_loc = {eta*d:.4f}, "
              f"eta*ln(1+delta_loc) = {eta*np.log1p(d):.4f}")
    print(f"  => eta*ln(1+delta_loc) = ln(T) = {np.log(T_MEAS):.4f} (73.04/67.4) or {np.log(T_PAGE):.4f} (73/67);")
    print("     eta*delta_loc itself ranges ~0.075-0.09 along the line. Only the combination is fixed;")
    print("     every (eta, delta_loc) pair on the line gives the same ratio.")


def lognormal_field(n, Ls, sig, rng):
    g = rng.standard_normal(n)
    k = np.fft.rfftfreq(n, d=1.0)
    g = np.fft.irfft(np.fft.rfft(g) * np.exp(-0.5 * (2 * np.pi * k * Ls) ** 2), n)
    g *= sig / g.std()
    return g                                     # ln(1+delta) + sig^2/2


def part_B():
    print("\n--- (B) light propagated through a structured log-normal field (SEED=19) ---")
    n = 2 ** 20
    Ls = 20.0                                    # [HAND]
    iD = D_WIN.astype(int)
    obs = np.arange(0, n - 1000, (n - 1000) // 16384)[:16384] + 700
    out = {}
    for sig in (0.1, 0.2, 0.4):                  # [HAND]
        rng = np.random.default_rng(SEED)
        g = lognormal_field(n, Ls, sig, rng)
        lnrho = g - 0.5 * sig ** 2               # ln(1+delta)
        for eta in (-0.3, 0.5, 1.0, 2.0):
            w = np.exp(eta * lnrho)
            w /= w.mean()                        # deep average -> H_global exactly
            cw = np.concatenate([[0.0], np.cumsum(w)])
            cl = np.concatenate([[0.0], np.cumsum(lnrho)])
            cd = np.concatenate([[0.0], np.cumsum(np.expm1(lnrho))])
            ratios, lnbar, dsph = [], [], []
            for sgn in (+1, -1):
                if sgn > 0:
                    I = cw[obs[:, None] + iD[None, :]] - cw[obs][:, None]
                    L = cl[obs[:, None] + iD[None, :]] - cl[obs][:, None]
                    S = (cd[obs + 200] - cd[obs]) / 200.0
                else:
                    I = cw[obs][:, None] - cw[obs[:, None] - iD[None, :]]
                    L = cl[obs][:, None] - cl[obs[:, None] - iD[None, :]]
                    S = (cd[obs] - cd[obs - 200]) / 200.0
                ratios.append(np.sum(NW * D_WIN * I, 1) / np.sum(NW * D_WIN ** 2))
                lnbar.append(np.sum(NW * D_WIN * L, 1) / np.sum(NW * D_WIN ** 2))
                dsph.append(S)
            r = np.array(ratios); lb = np.array(lnbar); ds = np.array(dsph)
            both = (r[0] * r[1]) ** 0.5
            ds2 = 0.5 * (ds[0] + ds[1])
            slope_ln = np.polyfit(lb.ravel(), np.log(r.ravel()), 1)[0]
            slope_sph = np.polyfit(ds2, np.log(both), 1)[0]
            corr_sph = np.corrcoef(ds2, np.log(both))[0, 1]
            out[(sig, eta)] = dict(sd=np.std(np.log(r.ravel())), dirs=np.std(np.log(r[0] / r[1])),
                                   p=np.mean(r.ravel() >= T_MEAS), s1=slope_ln, s2=slope_sph, c2=corr_sph)
    print("  sigma_g  eta   | slope d lnH / d<ln(1+d)>_LOS | slope vs 200-Mpc-sphere delta (corr) |"
          " rms lnH_loc | rms ln(H+x/H-x) | P(H_loc/H_glob >= 1.0837)")
    for (sig, eta), o in out.items():
        print(f"   {sig:4.2f}  {eta:+.2f}  |            {o['s1']:+.3f}             |"
              f"           {o['s2']:+.3f} ({o['c2']:+.2f})           |   {o['sd']:.4f}   |"
              f"     {o['dirs']:.4f}      |   {o['p']:.4f}")
    print("  Reading: the LOS-weighted slope recovers eta (to second order in sigma), so a measured")
    print("  H0-density slope would fix eta, and then delta_loc. The sign of the slope is the sign of")
    print("  eta. Direction dependence (+x vs -x) is of the same size as the observer-to-observer")
    print("  scatter. Whether 1.0837 is typical or rare depends ENTIRELY on the hand-chosen field")
    print("  amplitude sigma_g and smoothing L_s, which the framework does not supply.")
    print("  NOTE: the correlation is built into the model (ln(1+z) is a path integral of")
    print("  (1+delta)^eta); the simulation shows its amplitude and scatter, it is not independent")
    print("  evidence for the mechanism.")
    return out


if __name__ == "__main__":
    print("=== ch_hubble_tension.py : Hubble tension as line-of-sight averaging (HYP/SPEC) ===")
    part_A()
    out = part_B()
    print("\nPAGE CLAIM 'reproduces 73/67 for eta*delta_loc ~ 0.08': REPRODUCED as a statement about")
    print("  the combination eta*ln(1+delta_loc) = ln(73.04/67.4) = 0.080 when the local anomaly fills the")
    print("  ladder window; it is NOT a prediction (the target ratio is the input). If the anomaly is")
    print("  smaller than the window (R_loc < 600 Mpc) the needed contrast grows (table A).")
    print("PAGE CLAIM 'predicted H0-density correlation, slope set by eta': REPRODUCED (by construction).")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        etas = np.linspace(-2, 2, 400); etas = etas[np.abs(etas) > 0.05]
        fig, ax = plt.subplots(figsize=(6, 4))
        for T, lab in ((T_MEAS, "73.04/67.4"), (T_PAGE, "73/67")):
            ax.plot(etas, T ** (1 / etas) - 1, label=lab)
        ax.set_ylim(-0.6, 0.6); ax.axhline(0, color="k", lw=0.5)
        ax.set_xlabel("eta"); ax.set_ylabel("delta_loc needed (full filling)")
        ax.set_title("eta-delta_loc degeneracy line"); ax.legend()
        plt.tight_layout(); plt.savefig(os.path.join(HERE, "ch_hubble_tension.png"), dpi=110)
        print("  [figure written: ch_hubble_tension.png]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}] numbers above are the result.")
