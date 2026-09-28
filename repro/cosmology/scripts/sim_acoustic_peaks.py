#!/usr/bin/env python3
"""
sim_acoustic_peaks.py  --  Re-implementation (2026-09-28) of the lost Ch 14/15 follow-up simulation
"can a static inflow/lattice medium, with no hot dense past and no synchronized clock, produce the peaks?"

PAGE CLAIMS (docs/cosmology/14-cmb-anisotropies-acoustic-scale/, 15-large-scale-structure-bao/,
             axb-reproducibility-map/, axj-version-history-reclassification-log/)
  "# Part 1: the harmonic series needs phase coherence (a synchronized clock)
   synchronized phases -> peaks at k = pi,2pi,3pi (ratios 1:2:3)
   random phases -> flat 0.5, NO peaks (series not in the dispersion law)
   # Part 2: one fixed inflow-shell length R_s supplies the scale
   center-shell correlation: bump at r = R_s = 150 Mpc
   shell P(k)=|sin(kR)/(kR)|^2: zeros at k = n*pi/R_s (BAO/CMB wiggle spacing)
   # Part 3: continuous random driving does NOT help
   white-noise driving -> smooth P(k) (corr 0.99 with 1/omega^2), 0 peaks
   harmonic peaks need a resonant cavity (standing waves), not noise"
  Also: "What a single shell does not give for free is the precise 1:2:3 peak-height pattern".
  Status on the page: HYP, open (R_s = 150 Mpc is INSERTED, not derived).

INPUTS (sources)
  - Units c_s t_rec = 1 (Part 1). R_s = 150 Mpc: the observed BAO ruler (inserted, page says so).
  - Part 2 box: 128^3 cells, 1200 Mpc side (9.375 Mpc cells), 300 random centres, each carrying
    a thin spherical shell of equal weight (4000 Fibonacci points, cloud-in-cell).
  - Part 3: 64 lattice modes omega_k = k (c = 1), Langevin damping gamma = 0.05, T = 1;
    cavity contrast: 1-D chain of 200 masses, fixed ends vs absorbing (graded-damping) ends,
    white-noise force at one site.
  - SEED = 19 for every random draw.

ALGORITHM
  P1: P(k) = <cos^2(k + phi)> over 4000 realizations with phi = 0 (synchronized) or U(0, 2 pi).
  P2: centre-shell cross-correlation by FFT, spherically averaged -> location of the bump;
      spherically averaged |FT(shell template)|^2 -> positions of minima vs n pi / R_s; side-lobe
      heights of the shell spectrum (height-pattern check).
  P3: time-averaged <x_k^2> of the driven modes; Pearson corr with 1/omega^2; count prominent
      maxima (> 1.2 x flanking minima). Cavity: Welch periodogram of one site; count resonances.

EXPECTED (page): P1 peaks at pi,2pi,3pi (1:2:3); random -> flat 0.5.  P2 bump at 150 Mpc; zeros
  at n pi/R_s.  P3 corr ~0.99 with 1/omega^2, 0 peaks; peaks only with a resonant cavity.
"""
import numpy as np

SEED = 19

def prominent_maxima(x, y, prom=0.2):
    out = []
    for i in range(1, len(y) - 1):
        if y[i] >= y[i - 1] and y[i] >= y[i + 1]:
            j = i
            while j > 0 and y[j - 1] <= y[j]: j -= 1
            k = i
            while k < len(y) - 1 and y[k + 1] <= y[k]: k += 1
            if y[i] > (1 + prom) * max(y[j], y[k]):
                out.append(x[i])
    return out

# ---------------- Part 1 ----------------
def part1(nreal=4000, seed=SEED):
    k = np.linspace(0.05, 3.5 * np.pi, 700)
    sync = np.cos(k) ** 2
    rng = np.random.default_rng(seed)
    rnd = np.mean(np.cos(k[None, :] + rng.uniform(0, 2 * np.pi, (nreal, k.size))) ** 2, axis=0)
    return k, sync, rnd

# ---------------- Part 2 ----------------
def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)

def cic(pos, N, box, w):
    g = np.zeros((N, N, N)); x = pos / (box / N) - 0.5
    i0 = np.floor(x).astype(int); f = x - i0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                ww = w * (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                np.add.at(g, ((i0[:, 0] + dx) % N, (i0[:, 1] + dy) % N, (i0[:, 2] + dz) % N), ww)
    return g

def radial_avg(field3, rgrid, edges):
    idx = np.digitize(rgrid.ravel(), edges); f = field3.ravel()
    return np.array([f[idx == i].mean() if np.any(idx == i) else np.nan for i in range(1, len(edges))])

def part2(N=128, box=1200.0, Rs=150.0, ncen=300, npts=4000, seed=SEED):
    rng = np.random.default_rng(seed)
    cen = rng.uniform(0, box, (ncen, 3)); sph = fib_sphere(npts) * Rs
    shell_pos = (cen[:, None, :] + sph[None, :, :]).reshape(-1, 3) % box
    Dc = cic(cen, N, box, np.ones(ncen)); Ds = cic(shell_pos, N, box, np.full(len(shell_pos), 1.0 / npts))
    Dc -= Dc.mean(); Ds -= Ds.mean()
    xi = np.real(np.fft.ifftn(np.fft.fftn(Dc) * np.conj(np.fft.fftn(Ds))))
    d = box / N; ax = np.fft.fftfreq(N, 1.0 / N) * d
    r = np.sqrt(ax[:, None, None] ** 2 + ax[None, :, None] ** 2 + ax[None, None, :] ** 2)
    redges = np.arange(0, 400, d); rc = 0.5 * (redges[1:] + redges[:-1])
    xir = radial_avg(xi, r, redges); r_bump = rc[np.nanargmax(np.where(rc > 30, xir, -np.inf))]
    # shell template power spectrum
    T = cic(sph % box, N, box, np.full(npts, 1.0 / npts))
    Pk3 = np.abs(np.fft.fftn(T)) ** 2
    kax = 2 * np.pi * np.fft.fftfreq(N, d)
    kk = np.sqrt(kax[:, None, None] ** 2 + kax[None, :, None] ** 2 + kax[None, None, :] ** 2)
    dk = np.pi / box                                           # half the fundamental: fine bins
    kedges = np.arange(0.0, np.pi / d, dk); kc = 0.5 * (kedges[1:] + kedges[:-1])
    Pk = radial_avg(Pk3, kk, kedges)
    lp = np.log(Pk)
    def parab(i):                                              # 3-point parabolic refinement
        den = lp[i - 1] - 2 * lp[i] + lp[i + 1]
        return kc[i] + 0.5 * dk * (lp[i - 1] - lp[i + 1]) / den if den != 0 else kc[i]
    # minima / side-lobe maxima of the measured shell spectrum (k R/pi units), first 6
    mins = [parab(i) for i in range(1, len(Pk) - 1) if Pk[i] < Pk[i - 1] and Pk[i] < Pk[i + 1]][:6]
    maxs = [(kc[i], Pk[i]) for i in range(1, len(Pk) - 1) if Pk[i] > Pk[i - 1] and Pk[i] > Pk[i + 1]][:4]
    return rc, xir, r_bump, kc, Pk, np.array(mins) * Rs / np.pi, maxs

# ---------------- Part 3 ----------------
def part3(nmode=64, gamma=0.05, T=1.0, dt=0.02, t_end=4000.0, seed=SEED):
    rng = np.random.default_rng(seed)
    w = np.arange(1, nmode + 1) * (np.pi / nmode) * 4        # omega_k = c k, spread 0.2..12.6
    x = np.zeros(nmode); v = np.zeros(nmode); acc2 = np.zeros(nmode); n = 0
    c1 = np.exp(-gamma * dt); s1 = np.sqrt((1 - c1 ** 2) * T)
    nsteps = int(t_end / dt); burn = int(0.2 * nsteps)
    for i in range(nsteps):
        v += -0.5 * dt * w ** 2 * x; x += dt * v; v += -0.5 * dt * w ** 2 * x
        v = c1 * v + s1 * rng.standard_normal(nmode)
        if i > burn and i % 5 == 0:
            acc2 += x ** 2; n += 1
    X2 = acc2 / n
    corr = np.corrcoef(X2, 1 / w ** 2)[0, 1]
    corr_log = np.corrcoef(np.log(X2), np.log(1 / w ** 2))[0, 1]
    pk = prominent_maxima(w, X2)
    y = X2 * w ** 2 / T                                         # equipartition-normalised (flat = 1)
    n3 = int(np.sum(y > 1 + 3 * y.std()))
    return w, X2, corr, corr_log, pk, y.std(), n3

def cavity(Nm=200, fixed=True, dt=0.2, nsteps=2 ** 17, seed=SEED):
    """1-D chain (c = 1, a = 1), white-noise force at site 7, record site 61."""
    rng = np.random.default_rng(seed)
    gam = np.full(Nm, 0.002)
    if not fixed:                                             # absorbing ends (graded damping)
        ramp = np.linspace(0, 1, 40) ** 2 * 0.8
        gam[:40] += ramp[::-1]; gam[-40:] += ramp
    x = np.zeros(Nm); v = np.zeros(Nm); rec = np.empty(nsteps)
    def acc(x):
        xp = np.concatenate(([0.0], x, [0.0]))                # fixed (Dirichlet) ends
        return xp[2:] - 2 * x + xp[:-2]
    a = acc(x)
    for i in range(nsteps):
        f = np.zeros(Nm); f[7] = rng.standard_normal() / np.sqrt(dt)
        v += 0.5 * dt * (a - gam * v + f); x += dt * v; a = acc(x); v += 0.5 * dt * (a - gam * v)
        rec[i] = x[61]
    seg = 2 ** 14; win = np.hanning(seg); P = 0
    for s in range(0, nsteps - seg + 1, seg // 2):
        P = P + np.abs(np.fft.rfft(win * (rec[s:s + seg] - rec[s:s + seg].mean()))) ** 2
    om = 2 * np.pi * np.fft.rfftfreq(seg, dt)
    sel = (om > 0.004) & (om < 0.2)
    return om[sel], P[sel], prominent_maxima(om[sel], P[sel], prom=1.0)

if __name__ == "__main__":
    print("=== Part 1: is the harmonic series in the dispersion law, or in phase coherence? ===")
    k, sync, rnd = part1()
    pk = prominent_maxima(k, sync)
    print(f"  synchronized phases: peaks at k/pi = {[round(float(p/np.pi), 3) for p in pk]}  "
          f"ratios {[round(float(p/pk[0]), 3) for p in pk]}")
    print(f"  random phases: mean = {rnd.mean():.4f}, max|dev from 0.5| = {np.abs(rnd-0.5).max():.4f}, "
          f"prominent peaks = {len(prominent_maxima(k, rnd))}")
    print("  RESULT: 1:2:3 needs a synchronized start; random phases -> flat 0.5.\n")

    print("=== Part 2: one fixed inflow-shell length R_s = 150 Mpc (INSERTED) ===")
    rc, xir, rb, kc, Pk, mins, maxs = part2()
    print(f"  centre-shell correlation bump at r = {rb:.1f} Mpc  (cell 9.4 Mpc; target 150)")
    print(f"  shell P(k) minima at k R_s/pi = {[round(float(m), 3) for m in mins]}  (sinc^2 zeros: 1,2,3,...)")
    h = [p for _, p in maxs]
    xs = np.array([4.4934, 7.7253, 10.9041, 14.0662]); sinc2 = (np.sin(xs) / xs) ** 2
    print(f"  shell side-lobe heights, measured (norm. to 1st side lobe): {[round(float(x/h[0]), 2) for x in h]}")
    print(f"  shell side-lobe heights, analytic |sin x/x|^2:              {[round(float(x/sinc2[0]), 2) for x in sinc2]}"
          f"  -> monotone fall, NO odd/even alternation")
    print("  RESULT: one fixed length gives the bump at R_s and the wiggle spacing pi/R_s; it does")
    print("  not give the 1:2:3 height pattern, and R_s itself is inserted (not derived).\n")

    print("=== Part 3: continuous random driving vs a resonant cavity ===")
    w, X2, corr, corr_log, pk3, sd, n3 = part3()
    print(f"  white-noise-driven modes: corr(<x^2>, 1/omega^2) = {corr:.4f} (linear), "
          f"{corr_log:.4f} (log-log)")
    print(f"  maxima by the naive 20%-prominence rule: {len(pk3)} at omega = {[round(float(p), 2) for p in pk3]};"
          f" but <x^2> omega^2/T scatters {sd:.2f} rms (finite sampling) and {n3} modes exceed 1+3 sigma"
          f" -> no significant peak")
    om_f, P_f, pk_f = cavity(fixed=True); om_o, P_o, pk_o = cavity(fixed=False)
    L = 201.0
    print(f"  driven chain, FIXED ends (cavity L={L:.0f}): {len(pk_f)} resonances, first at omega*L/(pi c) = "
          f"{[round(float(p*L/np.pi), 2) for p in pk_f[:8]]}")
    print(f"  driven chain, ABSORBING ends (no cavity): {len(pk_o)} resonances")
    print("  RESULT: noise gives a smooth ~1/omega^2 spectrum; discrete peaks need a fixed cavity length.")
    print("  HONEST: nothing here derives 150 Mpc; that is derive_acoustic_length.py's criterion (i).")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, os
        fig, ax = plt.subplots(1, 4, figsize=(17, 3.8))
        ax[0].plot(k / np.pi, sync, label="synchronized"); ax[0].plot(k / np.pi, rnd, label="random phase")
        ax[0].set_xlabel(r"$c_s k t/\pi$"); ax[0].legend(fontsize=8); ax[0].set_title("P1 phase coherence")
        ax[1].plot(rc, xir); ax[1].axvline(150, ls=":", color="gray"); ax[1].set_xlabel("r (Mpc)"); ax[1].set_title("P2 centre-shell corr.")
        ax[2].semilogy(kc * 150 / np.pi, Pk); ax[2].set_xlabel(r"$kR_s/\pi$"); ax[2].set_title("P2 shell P(k)")
        ax[3].semilogy(om_f, P_f, label="fixed ends"); ax[3].semilogy(om_o, P_o, label="absorbing"); ax[3].legend(fontsize=8)
        ax[3].set_xlabel(r"$\omega$"); ax[3].set_title("P3 cavity vs no cavity")
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs", "sim_acoustic_peaks.png")
        plt.tight_layout(); plt.savefig(p, dpi=100); print(f"  [figure written: {p}]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}]")
