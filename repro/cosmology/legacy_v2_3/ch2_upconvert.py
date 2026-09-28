#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_upconvert.py -- can the ARRIVING wave make gamma locally? (the up-conversion test)
=====================================================================================

A second escape from the gamma-ray-burst dispersion tension (Ch.2): perhaps no gamma
propagates at all. What crosses the cosmos is the collective lattice wave (the
non-dispersive low-k mode = the gravitational wave); the gamma is then produced
locally, when that arriving wave shakes our lattice. The wave arrives gentle but
enormously energetic (a very stiff medium), so the energy is there (ch2_gammacontent.py).
The question this script settles: can a gentle, long-wavelength (low-k) wave actually
shake the lattice down to the gamma (cell, high-k) scale?

ANSWER (honest, negative for a *gentle* wave):
  - Up-conversion low-k -> high-k requires nonlinearity, and the nonlinear term only
    competes with the linear one when the per-bond strain is of order unity:
    (nonlinear)/(linear) ~ beta*(strain)^2 ~ 1  =>  strain ~ O(1).
  - This threshold is DIMENSION-INDEPENDENT (it is per-bond): 1D and 3D both show
    ~0% high-k content until the strain approaches ~1.
  - A non-dispersively propagated wave is necessarily SMOOTH (low-k), hence low-strain
    (strain ~ the metric strain h ~ 1e-22 for an arriving burst wave). That is ~20
    ORDERS below the threshold. So a gentle arriving wave cannot generate gamma.

What 3D *does* change: once nonlinear, the cascade to small scales is richer; and
3D focusing (converging inflows) raises the strain -- but that happens at the
*converging source* (the burst), not in the *diverging* wave that reaches us. So 3D
helps make gamma at the source (which then faces propagation), not at arrival.

Bottom line: neither route escapes. Source-emitted gamma disperses off the front
(ch2_burstprop.py); a gentle arriving wave is ~20 orders too weak to make gamma
locally (this script). Both point to the same requirement: gamma must be the exact
continuum (Box_c) mode, non-dispersive at all k (Ch.2, sec:goldstone / sec:stiffness).

Requires numpy; matplotlib optional. Deterministic (no RNG).
"""

import numpy as np

# ---------- 1D: high-k generation vs strain ----------
def run_1d(A, beta=1.0, N=2048, steps=8000, dt=0.01, m0=2, thr=1.5):
    i = np.arange(N); k0 = 2*np.pi*m0/N
    x = A*np.sin(k0*i); v = np.zeros(N)
    k = 2*np.pi*np.fft.rfftfreq(N); w2 = 4*np.sin(k/2)**2
    def acc(x):
        d = np.diff(np.concatenate([[x[-1]], x, [x[0]]])); f = d[1:]-d[:-1]
        if beta:
            c = d**3; f = f + beta*(c[1:]-c[:-1])
        return f
    def spec(x, v):
        Ek = 0.5*np.abs(np.fft.rfft(v)/N)**2 + 0.5*w2*np.abs(np.fft.rfft(x)/N)**2
        return Ek
    a = acc(x); E0 = spec(x, v).sum(); strain0 = np.abs(np.diff(x)).max()
    for s in range(steps):
        x = x + v*dt + 0.5*a*dt*dt; an = acc(x); v = v + 0.5*(a+an)*dt; a = an
    Ek = spec(x, v); hi = 100*Ek[k > thr].sum()/E0; econs = Ek.sum()/E0
    return strain0, hi, econs

# ---------- 3D: same test, smaller lattice ----------
def run_3d(A, beta=1.0, N=24, steps=1500, dt=0.01, m0=2, thr=1.5):
    ks = 2*np.pi*np.fft.fftfreq(N)
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing='ij'); KMAG = np.sqrt(KX**2+KY**2+KZ**2)
    w2 = 4*(np.sin(KX/2)**2+np.sin(KY/2)**2+np.sin(KZ/2)**2)
    i = np.arange(N); X, Y, Z = np.meshgrid(i, i, i, indexing='ij'); k0 = 2*np.pi*m0/N
    u = A*(np.sin(k0*X)+0.7*np.sin(k0*Y+1)+0.5*np.sin(k0*Z+2)); v = np.zeros_like(u)
    def force(u):
        acc = -6.0*u; nl = np.zeros_like(u)
        for d in (0, 1, 2):
            R = np.roll(u, -1, d); L = np.roll(u, 1, d); acc = acc + R + L
            if beta: nl += (R-u)**3-(u-L)**3
        return acc + beta*nl
    def spec(u, v):
        Ek = 0.5*np.abs(np.fft.fftn(v)/N**3)**2 + 0.5*w2*np.abs(np.fft.fftn(u)/N**3)**2
        return Ek
    def strain(u):
        return max(np.abs(np.roll(u, -1, d)-u).max() for d in (0, 1, 2))
    a = force(u); E0 = spec(u, v).sum(); s0 = strain(u)
    for s in range(steps):
        u = u + v*dt + 0.5*a*dt*dt; an = force(u); v = v + 0.5*(a+an)*dt; a = an
    Ek = spec(u, v); hi = 100*Ek[KMAG > thr].sum()/E0; econs = Ek.sum()/E0
    return s0, hi, econs

print("="*78)
print(" ch2_upconvert.py -- can a gentle arriving wave shake the lattice to gamma?")
print("="*78)
print(" high-k ('gamma', |k|>1.5) energy %, generated from a low-k wave, at MATCHED strain\n")
print(f"   {'target strain':>13} {'1D strain':>10} {'1D high-k%':>11} {'(E)':>5} {'3D strain':>10} {'3D high-k%':>11} {'(E)':>5}")
k0_1d=2*np.pi*2/512
k0_3d=2*np.pi*2/24
rows=[]
for s_target in [0.1, 0.3, 0.6, 0.9, 1.5]:
    A1=s_target/k0_1d
    A3=s_target/(k0_3d*0.95)
    s1,h1,e1=run_1d(A1, N=512)
    s3,h3,e3=run_3d(A3, N=24, steps=1200)
    print(f"   {s_target:13.2f} {s1:10.3f} {h1:11.3f} {e1:5.2f} {s3:10.3f} {h3:11.3f} {e3:5.2f}")
    rows.append((s1,h1,s3,h3))
print()
print(" Reading: high-k stays ~0% until strain ~ O(1), in BOTH 1D and 3D -- the threshold")
print(" is per-bond, hence dimension-independent. A non-dispersively propagated wave is")
print(" smooth (low-k), so its strain ~ h ~ 1e-22: about 20 ORDERS below threshold.")
print(" => a gentle arriving wave cannot generate gamma locally. (Reliable in the gentle")
print("    regime; at strain >~1 the integrator loses energy, but the arriving wave is gentle.)")
print("="*78)

# ---------------- figure ----------------
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    s1 = [r[0] for r in rows]; h1 = [r[1] for r in rows]
    s3 = [r[2] for r in rows]; h3 = [r[3] for r in rows]
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.plot(s1, h1, "o-", color="#1f77b4", lw=1.8, ms=7, label="1D lattice")
    ax.plot(s3, h3, "s--", color="#d62728", lw=1.8, ms=7, label="3D lattice")
    ax.axvspan(1e-3, 0.5, color="#d9f0d9", alpha=0.6, zorder=0)
    ax.text(0.06, 50, "gentle wave\n(real arriving wave\nlives near strain ~1e-22,\nfar off to the left)",
            fontsize=8.5, va="center", color="#256029")
    ax.axvline(1.0, color="gray", ls=":", lw=1.2)
    ax.text(1.02, 5, "nonlinearity\nturns on (~strain 1)", fontsize=8.5, color="#555")
    ax.set_xlabel("per-bond strain of the disturbance")
    ax.set_ylabel("high-k ('gamma') energy generated  [%]")
    ax.set_title("Up-conversion needs strain ~ O(1), in 1D and 3D alike (dimension-independent).\n"
                 "A gentle (smooth, low-k) arriving wave is ~20 orders too weak to make gamma locally.",
                 fontsize=10)
    ax.set_ylim(-3, 60); ax.legend(fontsize=9, loc="center right")
    fig.tight_layout(); fig.savefig("ch2_upconvert.png", dpi=150)
    print("[figure written: ch2_upconvert.png]")
except Exception as e:
    print(f"[figure skipped: {e}]")
