#!/usr/bin/env python3
"""
ch14_cmb_aniso.py  --  Re-implementation (2026-09-28) of the lost Chapter 14 script
"CMB anisotropies and the acoustic scale: making the target explicit".

PAGE CLAIM (docs/cosmology/14-cmb-anisotropies-acoustic-scale/, axb-reproducibility-map/)
  "# A: target angular scale from the first peak
   ell_peak = 220 -> theta_peak = pi/220 = 0.82 deg (standard: sound-horizon angle)
   # B: single lattice correlation length, toy power spectrum
   one coherence scale -> one broad bump near ell~220
   harmonic peaks at ell~540, 810: NOT reproduced (needs coherent oscillation)"
  Grade on the page: badge 'conflicting'; text: HYP, open.  (The toy INSERTS the scale.)

INPUTS (sources)
  - Observed peak multipoles ell ~ 220, 540, 810 (Planck 2018 TT; as quoted on the page).
  - Flat-sky toy map: 512 x 512 pixels, 20 deg x 20 deg (pixel 2.34 arcmin, ell_Nyq ~ 4600).
  - ONE coherence scale: Gaussian-derivative (Laplacian-of-Gaussian) kernel of width sigma,
    whose power (ell sigma)^4 exp(-(ell sigma)^2) peaks at ell sigma = sqrt(2). sigma is set so
    the bump sits at the Part-A target ell = 220 (i.e. the scale is INSERTED, as the page says).
  - SEED = 19 white noise.

ALGORITHM
  A: theta = pi / ell_1.
  B: white-noise map -> convolve with the single-scale kernel -> FFT -> azimuthally binned C_ell
     (bin width 30), averaged over 8 realizations (sample variance). Count PROMINENT local maxima
     in 50 < ell < 1200 (height > 1.2 x both flanking minima; detection rule, not physics), and test whether any maximum lies within +/-40 of ell = 540 or 810.

EXPECTED (page): theta = 0.82 deg; exactly one bump near 220; no peaks at 540 / 810.
"""
import numpy as np

SEED = 19

def part_a(ell=220):
    th = np.pi / ell
    return th, np.degrees(th)

def prominent_maxima(c, C, prom=0.2):
    """Local maxima whose height exceeds BOTH flanking minima by > prom (relative)."""
    out = []
    for i in range(1, len(C) - 1):
        if not (C[i] >= C[i - 1] and C[i] >= C[i + 1]):
            continue
        lmin = C[:i + 1][::-1]; j = 0
        while j + 1 < len(lmin) and lmin[j + 1] <= lmin[j]: j += 1
        rmin = C[i:]; k = 0
        while k + 1 < len(rmin) and rmin[k + 1] <= rmin[k]: k += 1
        if C[i] > (1 + prom) * max(lmin[j], rmin[k]) or (j == len(lmin) - 1 and C[i] > (1 + prom) * rmin[k]):
            out.append(c[i])
    return out

def part_b(N=512, side_deg=20.0, ell_target=220.0, seed=SEED, nreal=8):
    rng = np.random.default_rng(seed)
    L = np.radians(side_deg)
    lx = 2 * np.pi * np.fft.fftfreq(N, d=L / N)
    ell = np.sqrt(lx[:, None] ** 2 + lx[None, :] ** 2)
    sig = np.sqrt(2.0) / ell_target               # the ONE coherence scale (inserted)
    kern = (ell * sig) ** 2 * np.exp(-0.5 * (ell * sig) ** 2)
    P = 0.0
    for _ in range(nreal):                          # average realizations: sample variance
        m = np.real(np.fft.ifft2(np.fft.fft2(rng.standard_normal((N, N))) * kern))
        P = P + np.abs(np.fft.fft2(m)) ** 2 / nreal
    edges = np.arange(20, 2000, 30); cen = 0.5 * (edges[1:] + edges[:-1])
    idx = np.digitize(ell.ravel(), edges); Pr = P.ravel()
    Cl = np.array([Pr[idx == i].mean() for i in range(1, len(edges))])
    sel = (cen > 50) & (cen < 1200)
    c, C = cen[sel], Cl[sel]
    peaks = prominent_maxima(c, C)
    return cen, Cl, peaks, np.degrees(sig)

if __name__ == "__main__":
    th, thd = part_a()
    print("=== A: target angular scale ===")
    print(f"  ell_peak = 220 -> theta = pi/220 = {th:.5f} rad = {thd:.3f} deg   (page: 0.82 deg)")
    for l in (540, 810):
        print(f"  harmonic target ell = {l}: ratio to 220 = {l/220:.2f}")
    print("\n=== B: single coherence length (inserted at the Part-A scale), toy C_ell ===")
    cen, Cl, peaks, sd = part_b()
    print(f"  kernel width sigma = {sd*60:.2f} arcmin; prominent maxima in 50<ell<1200: "
          f"{[int(p) for p in peaks]}")
    print(f"  number of bumps = {len(peaks)}")
    for l in (540, 810):
        hit = any(abs(p - l) <= 40 for p in peaks)
        print(f"  peak near ell={l}: {'PRESENT' if hit else 'ABSENT'}")
    print("  RESULT: one coherence scale -> one broad bump; the harmonic series is NOT reproduced.")
    print("  HONEST: the bump position is INSERTED (sigma chosen from the target), not derived; see")
    print("  sim_acoustic_peaks.py / derive_acoustic_length.py for the follow-up program (HYP, open).")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, os
        plt.figure(figsize=(6.5, 4)); plt.plot(cen, Cl / Cl.max(), color="#185FA5")
        for l in (220, 540, 810): plt.axvline(l, ls=":", color="gray")
        plt.xlim(0, 1300); plt.xlabel(r"$\ell$"); plt.ylabel(r"$C_\ell$ (norm.)")
        plt.title("single coherence length: one bump, no harmonics")
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs", "ch14_cmb_aniso.png")
        plt.tight_layout(); plt.savefig(p, dpi=110); print(f"  [figure written: {p}]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}]")
