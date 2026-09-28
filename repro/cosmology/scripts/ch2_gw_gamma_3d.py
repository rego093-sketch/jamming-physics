#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_gw_gamma_3d.py  --  Chapter 2 ("What actually arrives", v2): one 3-D lattice shake, watched
from increasing distance -- how much arrives per unit area, and in which band.
=================================================================================================
Re-implementation (2026-09-28) of the lost script cited by
  docs/cosmology/02-light-lattice-elastic-wave-sharpest/  ("What actually arrives (v2)")

PAGE CLAIM (verbatim)
  "ch2_gw_gamma_3d.py and ch2_gw_gamma_arriving.py remove a unit confusion that would make such
   bursts sound catastrophic. The often-quoted '10^53 erg' is a source energy, back-calculated by
   integrating the inferred isotropic luminosity over 4 pi and the emitting volume; it is not what
   reaches a detector. The arriving fluence is F = E_iso/(4 pi d^2) ... What reaches us is a
   broadband keV-GeV spectrum at modest fluence, exactly as the lattice-shake picture predicts."

WHAT THIS SCRIPT DOES (the lattice half; the astrophysical numbers are in ch2_gw_gamma_arriving.py)
  A 3-D simple-cubic lattice, ONE scalar displacement per site (the single longitudinal /
  breathing channel that survives at the isostatic point, G -> 0; physics volume 01/02),
  nearest-neighbour springs K = m = a = 1 (long-wave speed c = 1). A localized shake (Gaussian,
  width 3 cells, from rest) is released at the centre. We measure, without putting in any law:
   (1) the energy that has crossed spheres of radius r = 10, 20, 30, 40 -> fluence F(r) =
       E_crossed / (4 pi r^2); test r^2 F(r) = const (the 1/(4 pi d^2) law) and energy conservation.
   (2) the arrival time at each sphere of the low band (|k|a < 0.5, the long-wave, GW-like part)
       and of the high band (|k|a > 0.5, the 'gamma' part of the calibration ka = 0.1 <-> 31 GeV),
       i.e. does the broadband packet ARRIVE together? (3-D version of legacy ch2_burstprop.py.)

INPUTS: none physical; K = m = a = 1 lattice units. Grid 128^3 is a container (reflections from
  the box are excluded by stopping at t = 50 < 64). Shake width 3 cells is a probe choice
  (sharp = broadband). No page number enters the code.
EXPECTED OUTPUT (run 2026-09-28): r^2 F(r) constant to 0.15% (r = 10..40); energy drift -6.6e-4
  (velocity Verlet); low band arrives at t = r/c; high band later, lag/r = 0.046 (independent-mode
  prediction from the exact sc dispersion 0.040), growing linearly with r. The fluence law is
  confirmed; 'the broadband packet arrives together' is not.
DETERMINISM: SEED = 19 (no RNG path); 2 x SHA-256 over 6-sig-fig results.
DEPENDENCIES: numpy; matplotlib optional (MPLBACKEND=Agg). Runtime ~2 min.
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

Ng = 128; DT = 0.1; T_END = 50.0; W = 3.0; KS = 0.5
c0 = Ng // 2
ax = np.arange(Ng) - c0
X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2).astype(np.float32)
k1 = 2 * np.pi * np.fft.fftfreq(Ng)
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
KMAG = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2)
LOWMASK = KMAG < KS
# exact sc-lattice dispersion omega = 2 sqrt(sum sin^2(k_i/2)); |group velocity|
OMEGA = 2 * np.sqrt(np.sin(KX / 2) ** 2 + np.sin(KY / 2) ** 2 + np.sin(KZ / 2) ** 2)
_om = np.where(OMEGA > 0, OMEGA, 1.0)
VG = np.sqrt(sum((np.sin(K) / _om) ** 2 for K in (KX, KY, KZ)))
del KX, KY, KZ, _om

def lap(u):
    return (np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1)
            + np.roll(u, 1, 2) + np.roll(u, -1, 2) - 6 * u)

def edens(u, v):
    """Site energy density: kinetic + half of the three forward bonds + half of the backward ones."""
    e = 0.5 * v * v
    for a in range(3):
        d = np.roll(u, -1, a) - u
        e += 0.25 * d * d + 0.25 * np.roll(d, 1, a) ** 2
    return e

WLOW = np.exp(-(KMAG / KS) ** 4)          # smooth low-pass (avoids sharp-cutoff ringing)

def band_split(f):
    F = np.fft.fftn(f)
    lo = np.real(np.fft.ifftn(F * WLOW))
    return lo, f - lo

RADII = (10, 20, 30, 40)

def evolve(u):
    """Linear lattice evolution from rest; returns sample times, energy beyond each radius, E(0), E(end)."""
    v = np.zeros_like(u); a = lap(u); E0 = edens(u, v).sum()
    ts, cr = [], []
    nsteps = int(T_END / DT)
    for s in range(nsteps + 1):
        if s % 10 == 0:
            e = edens(u, v); ts.append(s * DT); cr.append([e[R > r].sum() for r in RADII])
        v += 0.5 * a * DT; u += v * DT; a = lap(u); v += 0.5 * a * DT
    return np.array(ts), np.array(cr), E0, edens(u, v).sum()

def mean_arrival(ts, cr):
    """Energy-weighted mean crossing time of each sphere (from the cumulative crossed energy)."""
    dE = np.diff(cr, axis=0); tm = 0.5 * (ts[1:] + ts[:-1])
    dE = np.clip(dE, 0, None)
    return (tm[:, None] * dE).sum(0) / dE.sum(0)

if __name__ == "__main__":
    np.random.seed(SEED)
    u0 = np.exp(-(R.astype(float) / W) ** 2)
    ts, crossed, E0, Eend = evolve(u0.copy())
    lo0, hi0 = band_split(u0)
    hi_frac0 = edens(hi0, np.zeros_like(u0)).sum() / E0
    # by linearity each band can be launched on its own and timed without any later filtering
    tsl, crl, E0l, _ = evolve(lo0.copy()); tsh, crh, E0h, _ = evolve(hi0.copy())
    tl_r = mean_arrival(tsl, crl); th_r = mean_arrival(tsh, crh)
    radii = RADII

    print("=" * 92)
    print(" ch2_gw_gamma_3d.py -- one 3-D lattice shake: fluence vs distance, and band arrival times")
    print("=" * 92)
    print(f" 3-D scalar (breathing-channel) lattice {Ng}^3, K = m = a = 1 (c = 1); shake width {W} cells")
    print(f" energy conservation: E(end)/E(0) - 1 = {Eend/E0-1:.2e};  high-band (|k|a>~{KS}) share of the"
          f" source energy = {hi_frac0:.3f}")
    print("\n (1) fluence law.  E_crossed(r) = energy beyond radius r at t = 50")
    print("     r     E_crossed/E0    F(r) = E_crossed/(4 pi r^2)    r^2 F(r) / (r^2 F)_{r=10}")
    ref = None; res = {"seed": SEED, "fluence": {}, "lag": {}}
    for i, r in enumerate(radii):
        Ec = crossed[-1, i]; F = Ec / (4 * np.pi * r * r)
        ref = ref or r * r * F
        print(f"    {r:3d}     {Ec/E0:.5f}        {F:.4e}                      {r*r*F/ref:.4f}")
        res["fluence"][r] = sig(r * r * F / ref)
    print("     => wherever (essentially) all the energy has crossed, r^2 F is constant: a detector at d receives")
    print("        E/(4 pi d^2), not E (geometry + energy conservation). Where E_crossed/E0 < 1 the missing part is")
    print("        slow high-k content still in transit -- the dispersion of (2), not a failure of the law.")

    print("\n (2) mean energy-arrival time at radius r, low band vs high band launched separately (linearity)")
    print("     r     t_low     t_high    lag = t_high - t_low    lag / r")
    lags = []
    for i, r in enumerate(radii):
        tl, th = tl_r[i], th_r[i]
        lags.append(th - tl)
        print(f"    {r:3d}    {tl:6.2f}    {th:6.2f}       {th-tl:6.2f}               {(th-tl)/r:.4f}")
        res["lag"][r] = sig(th - tl)
    slope = np.polyfit(radii[1:], lags[1:], 1)[0]       # r = 10 still near-field
    # independent-mode expectation from the EXACT sc dispersion and the source's own spectrum:
    # each band's energy moves at its energy-weighted |v_g|; lag/r = 1/<v_g>_hi - 1/<v_g>_lo
    F0 = np.abs(np.fft.fftn(u0)) ** 2 * OMEGA ** 2
    Elo = F0 * WLOW ** 2; Ehi = F0 * (1 - WLOW) ** 2
    inv_vg = lambda Ek: (Ek * (1 / np.maximum(VG, 1e-6))).sum() / Ek.sum()
    pred = inv_vg(Ehi) - inv_vg(Elo)
    print(f"     fitted d(lag)/dr (r = 20-40) = {slope:.4f}   independent-mode prediction <1/v_g>_hi - <1/v_g>_lo"
          f" = {pred:.4f}")
    print("     => the high band (the 'gamma' of the ka<->E calibration) arrives LATER, by an amount growing")
    print("        in proportion to distance: in 3-D, as in 1-D (ch2_burstprop.py), one shake does not")
    print("        deliver its broadband content together. Over 40 Mpc this is the Fermi/GW170817 tension,")
    print("        unchanged (see ch2_gamma_collective.py P4).")
    res["lag_slope"] = sig(slope); res["Econs"] = sig(Eend / E0 - 1)
    print(f"\nDETERMINISM-DIGEST (2xSHA-256, 6 sig-fig): {digest(res)}")
    print(f"runtime {time.time()-T0:.0f} s")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
        rr = np.array(radii, float); Fr = np.array([crossed[-1, i] / (4 * np.pi * r * r) for i, r in enumerate(radii)])
        axs[0].loglog(rr, Fr, "o", label="lattice: E_crossed/(4 pi r^2)")
        axs[0].loglog(rr, Fr[0] * (rr[0] / rr) ** 2, "--", label="r^-2")
        axs[0].set_xlabel("r [cells]"); axs[0].set_ylabel("fluence"); axs[0].legend()
        for i, r in enumerate(radii):
            axs[1].plot(tsl, crl[:, i] / E0l, color=f"C{i}", lw=1.2, label=f"r={r} low band")
            axs[1].plot(tsh, crh[:, i] / E0h, color=f"C{i}", ls="--", lw=1.2)
        axs[1].set_xlabel("t"); axs[1].set_ylabel("fraction of band energy beyond r")
        axs[1].set_title("low band (solid) vs high band (dashed)"); axs[1].legend(fontsize=7)
        plt.tight_layout(); plt.savefig("ch2_gw_gamma_3d.png", dpi=110)
        print("[figure written: ch2_gw_gamma_3d.png]")
    except Exception as exc:
        print(f"[figure skipped: {exc}]")
