#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_gamma_collective.py  --  Chapter 2: does a COLLECTIVE (nonlinear) lattice disturbance carry
a broadband 'gamma' packet coherently, where independent modes would disperse?
=================================================================================================
Re-implementation (2026-09-28) of the lost script cited by
  docs/cosmology/02-light-lattice-elastic-wave-sharpest/   ("Quantifying the collective-mode
                                                            reconciliation (v2)")
  docs/cosmology/16-open-problems-gathered/                 (open problem #1, "Advanced (v2)")
  docs/cosmology/axj-version-history-reclassification-log/  (#1 "Gamma broadening ... resolved")
  docs/cosmology/axh-provenance-ledger-five-line-reproducibility/ ("Gamma collective mode")
  docs/cosmology/02-back-calculation-broadband-gamma-spectrum/  (companion of ch2_backcalc_spectrum)

PAGE CLAIMS (02-light-lattice..., verbatim)
  "a linear independent-mode packet disperses (peak x0.45, leading width x1.25), while the
   collective FPU-beta disturbance forms a sharp coherent front (peak x2.84, leading width x0.50),
   the bands staying locked."
  "independent 10MeV and 10keV modes over L=130Mly would arrive Delta t ~ 3x10^19 s apart ...
   (E_QG(D) ~ 115keV against the bound >1.3x10^20 eV, 15 orders) -- yet GW170817 bounds gamma and
   gravitational waves to within 1.7s over that distance (effective E_QG > 10^10 eV)."

WHAT THIS SCRIPT DOES
  P1  Broadband by Fourier: a localized shake of width w cells carries power up to k ~ 1/w.
  P2  Same localized, right-moving strain pulse launched on the SAME chain (K = m = a = 1, c = 1,
      legacy ch2_grb.py / ch2_burstprop.py conventions) twice: linear (beta = 0) and FPU-beta
      (beta = 1). Leading-front diagnostics as the page defines them: peak and FWHM of the
      forward-most coherent structure, end / start.
  P3  The decisive BAND-LOCK test the page asserts ("the bands staying locked"): split the field
      into a low-k band (ka < 0.5, what a GW-like detector sees) and a high-k band (ka > 0.5, the
      'gamma' content), and measure how far the high band trails the low band after distances
      D1 and 2*D1, linear vs nonlinear. Locked bands => lag independent of D.
      Also: the collective front's own speed (supersonic => amplitude-dependent speed).
  P4  Astrophysical arithmetic: the dispersion lag Delta t = (L/c)(E/E_QG)^2 with v_g = c cos(ka/2)
      => E_QG = sqrt(8) hbar c / ell; ell = D = 4.854 pm and ell = a = 6.33e-19 m (locked, physics
      volume); L = 40 Mpc (GW170817), Delta t_obs = 1.7 s.

INPUTS (sources): hbar c = 197.3269804 MeV fm (CODATA 2018); D = 4.854e-12 m, a = 6.33e-19 m (physics
  volume locks, as in legacy ch2_light.py); 40 Mpc and 1.7 s (Abbott et al. 2017, ApJL 848, L13);
  Fermi GRB 090510 bound E_QG,2 > 1.3e20 eV (Abdo et al. 2009 / Vasileiou et al. 2013, as in ch2_light.py).
  Lattice: beta = 1, pulse width w = 3, strain amplitudes 0.5 (strong) and 0.05 -- probe choices,
  disclosed, not fitted to any page number (none of the page ratios is used anywhere).

EXPECTED OUTPUT: see REIMPL_gw_gamma.md (the run of 2026-09-28 is quoted there).
DETERMINISM: SEED = 19 (no RNG path is taken); 2 x SHA-256 over 6-sig-fig results.
DEPENDENCIES: numpy; matplotlib optional (MPLBACKEND=Agg). Runtime ~1 min.
"""
import json, hashlib, time
import numpy as np

SEED = 19
T0 = time.time()

def sig(x, n=6):
    x = float(x)
    if x == 0.0 or not np.isfinite(x):
        return x
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))

def digest(obj):
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(hashlib.sha256(blob).digest()).hexdigest()

# ============================================================================= lattice
N = 4000; DT = 0.05; W = 3.0; X0 = 300.0
n_idx = np.arange(N, dtype=float)

def force(u, beta):
    du = np.diff(u)                       # strain on each bond
    t = du + beta * du ** 3               # bond tension (FPU-beta)
    F = np.zeros_like(u); F[:-1] += t; F[1:] -= t
    F[0] = F[-1] = 0.0                    # clamped ends (never reached)
    return F

def launch(A):
    """Right-moving localized strain pulse: eps_n = A exp(-((n-X0)/W)^2); v = -c*eps (c = 1)."""
    eps = A * np.exp(-((n_idx[:-1] + 0.5 - X0) / W) ** 2)
    u = np.concatenate([[0.0], np.cumsum(eps)]); u -= u[-1]  # u -> 0 ahead of the pulse
    v = np.zeros(N); v[1:] = -eps; v[0] = -eps[0]
    v = -np.gradient(u)                   # d'Alembert right-mover, c = 1
    return u, v

def run(A, beta, t_marks):
    u, v = launch(A); F = force(u, beta)
    out = {}; nsteps = int(round(max(t_marks) / DT)); marks = {int(round(t / DT)): t for t in t_marks}
    for s in range(nsteps + 1):
        if s in marks:
            out[marks[s]] = np.diff(u).copy()
        v += 0.5 * F * DT; u += v * DT; F = force(u, beta); v += 0.5 * F * DT
    return out

def leading_front(eps):
    """Forward-most structure with |eps| > 0.3 * max|eps|: its peak and FWHM (cells)."""
    a = np.abs(eps); thr = 0.3 * a.max()
    front = np.nonzero(a > thr)[0].max()
    lo = max(front - 40, 0); k = lo + np.argmax(a[lo:front + 1])
    pk = a[k]; half = 0.5 * pk
    i = k
    while i > 0 and a[i] > half: i -= 1
    j = k
    while j < len(a) - 1 and a[j] > half: j += 1
    # linear interpolation of the half-maximum crossings
    xl = i + (half - a[i]) / (a[i + 1] - a[i]); xr = j - 1 + (a[j - 1] - half) / (a[j - 1] - a[j])
    return pk, xr - xl, k

def bands(eps, ks=0.5):
    E = np.fft.rfft(eps); k = 2 * np.pi * np.fft.rfftfreq(len(eps))
    lo = E.copy(); lo[k >= ks] = 0; hi = E.copy(); hi[k < ks] = 0
    return np.fft.irfft(lo, len(eps)), np.fft.irfft(hi, len(eps))

def centroid(f):
    p = f * f; return (n_idx[:len(f)] * p).sum() / p.sum()

# ============================================================================= main
if __name__ == "__main__":
    np.random.seed(SEED)
    print("=" * 94)
    print(" ch2_gamma_collective.py -- collective (FPU-beta) front vs independent modes; band locking")
    print("=" * 94)

    # ---- P1 broadband by Fourier
    k = np.linspace(0, np.pi, 20001); Pk = np.exp(-(k * W) ** 2 / 2)       # |FT of Gaussian width W|^2
    frac = lambda k0: Pk[k >= k0].sum() / Pk.sum()
    print(f"\n[P1] a localized shake of width w = {W:.0f} cells is broadband: power fraction at ka > 0.1"
          f" = {frac(0.1):.3f}, ka > 0.5 = {frac(0.5):.3f}, ka > 1 = {frac(1.0):.3f}")
    print("     (calibration of ch2_backcalc_spectrum.py: E = (hbar c / a) ka, ka = 0.1 <-> 31 GeV)")

    # ---- P2 leading-front diagnostics
    D1 = 1500.0; t1 = D1; t2 = 2 * D1                  # distances ~ c*t
    res = {"seed": SEED}
    print(f"\n[P2] same right-moving strain pulse (w = {W:.0f}), linear vs FPU-beta (beta = 1), after t = {t1:.0f}")
    print("        case                 peak end/start   leading FWHM end/start   front speed (c=1)")
    rows = {}; keep_snaps = {}
    for A in (0.5, 0.05):
        for beta in (0.0, 1.0):
            snaps = run(A, beta, [0.0, t1 - 200.0, t1, t2]); keep_snaps[(A, beta)] = snaps
            p0, w0, k0 = leading_front(snaps[0.0]); p1, w1, k1 = leading_front(snaps[t1])
            _, _, kb = leading_front(snaps[t1 - 200.0])
            vf = (k1 - kb) / 200.0
            lo1, hi1 = bands(snaps[t1]); lo2, hi2 = bands(snaps[t2])
            lag1 = centroid(lo1) - centroid(hi1); lag2 = centroid(lo2) - centroid(hi2)
            ehi = lambda f: (f * f).sum()
            hi0 = bands(snaps[0.0])[1]
            # fraction of the high band's energy still inside the leading-front window (+-5 w)
            win = lambda f, kc: (f[max(kc - 15, 0):kc + 16] ** 2).sum() / max((f * f).sum(), 1e-300)
            _, _, k2 = leading_front(snaps[t2])
            lock1 = win(hi1, k1); lock2 = win(hi2, k2)
            tag = f"A={A:<4} {'FPU-beta' if beta else 'linear  '}"
            rows[tag] = dict(A=A, beta=beta, peak_ratio=p1 / p0, width_ratio=w1 / w0, v_front=vf,
                             lag1=lag1, lag2=lag2, lock1=lock1, lock2=lock2,
                             hi_frac0=ehi(hi0) / ehi(snaps[0.0]), hi_frac1=ehi(hi1) / ehi(snaps[t1]))
            print(f"     {tag:22s}   x{p1/p0:6.3f}          x{w1/w0:6.3f}                 {vf:.4f}")
    print("     page: linear x0.45 / x1.25 ; FPU-beta x2.84 / x0.50")

    print(f"\n[P3] BAND LOCK: centroid lag of the high band (ka>0.5, 'gamma') behind the low band (ka<0.5)")
    print(f"     after D1 ~ {D1:.0f} and D2 ~ {2*D1:.0f} cells; and the share of high-band energy still")
    print(f"     riding in the leading front (+-15 cells). Locked => lag constant, share ~ 1.")
    print("        case                 lag(D1)   lag(D2)   high-band share in front: D1    D2")
    for tag, r in rows.items():
        print(f"     {tag:22s}  {r['lag1']:8.1f}  {r['lag2']:8.1f}                         "
              f"{r['lock1']:.3f}  {r['lock2']:.3f}")
    # independent-mode prediction: each band's centroid moves at its power-weighted group velocity
    vg = np.cos(k / 2); lo_m = k < 0.5; hi_m = k >= 0.5
    dv = (Pk[lo_m] * vg[lo_m]).sum() / Pk[lo_m].sum() - (Pk[hi_m] * vg[hi_m]).sum() / Pk[hi_m].sum()
    print(f"     independent-mode prediction D * (<v_g>_low - <v_g>_high) = {dv*D1:.1f} (D1), {dv*2*D1:.1f} (D2)")

    # ---- P4 astrophysical arithmetic
    hbarc_eVm = 197.3269804e6 * 1e-15
    Dm, am = 4.854e-12, 6.33e-19
    EQG = lambda ell: np.sqrt(8) * hbarc_eVm / ell
    Mpc = 3.0856775814913673e22; c = 299792458.0
    L = 40 * Mpc; Lc = L / c; ly = 9.4607304725808e15
    E1, E2 = 10e6, 10e3
    dtD = Lc * (E1 ** 2 - E2 ** 2) / EQG(Dm) ** 2
    dta = Lc * (E1 ** 2 - E2 ** 2) / EQG(am) ** 2
    zoneD = np.pi * hbarc_eVm / Dm
    print(f"\n[P4] L = 40 Mpc = {L/ly/1e6:.0f} Mly, L/c = {Lc:.3e} s")
    print(f"     E_QG(D) = {EQG(Dm):.4g} eV,  E_QG(a) = {EQG(am):.4g} eV,  Fermi bound 1.3e20 eV"
          f"  -> {np.log10(1.3e20/EQG(Dm)):.1f} / {np.log10(1.3e20/EQG(am)):.1f} orders")
    print(f"     10 MeV vs 10 keV, quadratic law:  Delta t(D) = {dtD:.2e} s   Delta t(a) = {dta:.2e} s")
    print(f"     CAVEAT: on a D-lattice the zone edge is pi*hbar*c/D = {zoneD/1e3:.0f} keV; a 10 MeV mode has")
    print(f"     ka = {E1*Dm/hbarc_eVm:.0f} >> pi, so the quadratic formula is used far outside its range.")
    for Eg in (10e3, 100e3, 1e6):
        bound = Eg * np.sqrt(Lc / 1.7)
        print(f"     GW170817 (1.7 s, all lag attributed to dispersion) at E_gamma = {Eg/1e3:6.0f} keV: "
              f"E_QG,2 > {bound:.2e} eV")
    res.update(P1=[sig(frac(0.1)), sig(frac(0.5))],
               P2={t: {k2: sig(v) for k2, v in r.items()} for t, r in rows.items()},
               P4={"EQG_D": sig(EQG(Dm)), "EQG_a": sig(EQG(am)), "dt_D": sig(dtD), "dt_a": sig(dta),
                   "bound_10keV": sig(1e4 * np.sqrt(Lc / 1.7))})

    r5 = rows["A=0.5  FPU-beta"]; r05 = rows["A=0.05 FPU-beta"]
    print("\n[READING]")
    print(f"  * Strong front (strain 0.5): ~{100*r5['lock2']:.0f}% of the high-k energy rides inside the soliton front --")
    print("    the soliton's OWN spectrum is locked. But the front runs at "
          f"{r5['v_front']:.3f} c (supersonic, amplitude-dependent),")
    print("    so it separates from the low-k (GW-like) part in proportion to distance (lag "
          f"{r5['lag1']:.0f} -> {r5['lag2']:.0f}). A 10% speed excess is")
    print("    ~1e14 times the GW170817 limit |dv/c| < 1e-15: this 'coherence' does not reconcile GW170817.")
    print(f"  * Weak front (strain 0.05): FPU-beta behaves linearly (peak x{r05['peak_ratio']:.2f}, lag grows as the")
    print("    independent-mode prediction). Locking needs O(0.1-1) bond strain; an arriving wave has strain")
    print("    ~1e-22 (legacy ch2_upconvert.py), so any real propagating burst is in the LINEAR regime.")
    print("  * Page ratios (x0.45/x1.25 ; x2.84/x0.50) are NOT reproduced; the leading-front ratios also depend")
    print("    on the distance at which they are read (not stated on the page).")
    print("\n[SCOPE] Toy lattice units. omega(k) of the quasi-longitudinal branch is NOT derived here (open).")
    print(f"\nDETERMINISM-DIGEST (2xSHA-256, 6 sig-fig): {digest(res)}")
    print(f"runtime {time.time()-T0:.0f} s")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 4.3))
        for beta, col in ((0.0, "tab:orange"), (1.0, "tab:red")):
            s = keep_snaps[(0.5, beta)]
            _, _, kk = leading_front(s[t1])
            xs = np.arange(len(s[t1])) - kk
            ax[0].plot(xs, s[t1], color=col, lw=1, label=("FPU-beta" if beta else "linear") + f", t={t1:.0f}")
            lo, hi = bands(s[t1]); ax[1].plot(xs, hi, color=col, lw=1, label=("FPU-beta" if beta else "linear") + " high band")
        for a_ in ax:
            a_.set_xlim(-600, 60); a_.set_xlabel("cells relative to leading front"); a_.legend(fontsize=8)
        ax[0].set_title("strain after propagation (A=0.5, w=3)"); ax[1].set_title("high-k (ka>0.5) content")
        plt.tight_layout(); plt.savefig("ch2_gamma_collective.png", dpi=110)
        print("[figure written: ch2_gamma_collective.png]")
    except Exception as exc:
        print(f"[figure skipped: {exc}]")
