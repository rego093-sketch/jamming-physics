#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_burstprop.py -- does a collective burst carry its gamma content coherently?
===============================================================================

This is the DECISIVE test for the burst-as-collective-disturbance reading of the
gamma-ray-burst dispersion tension (Ch.2). The hope is that a gamma-ray burst is
a single coherent disturbance (like the gravitational wave the same merger emits),
so that all its wavelengths -- including the gamma band -- travel together and
arrive together, dissolving the Fermi dispersion bound.

The test launches a churning broadband disturbance on the lattice and splits it,
as it propagates, into its low-k part (the long-wavelength envelope, what a
detector would register as a gravitational wave) and its high-k part (the gamma
content). It then tracks where each part is.

RESULT (honest, negative for the dispersion rescue):
  - The low-k envelope travels as a coherent front at ~c.
  - The high-k (gamma) content travels at v_g = c*cos(ka/2) < c and SEPARATES,
    lagging the front by ~(1 - cos(ka/2)) * distance.
  - This happens at the SAME rate whether the disturbance is weak (near-linear)
    or strong (nonlinear): the nonlinearity that keeps the envelope coherent does
    NOT bind the gamma content to it. (The ch2_grb.py coherence is the low-k
    envelope; the gamma rides off it.)
  - Over a cosmological baseline the lag is the original conflict, unchanged:
    at ka ~ 0.1 and D ~ 9 Gly it exceeds the observed bound by ~15 orders.

Conclusion: the collective-disturbance / gravitational-wave picture answers the
energy and (candidate) spectrum questions (ch2_gammacontent.py) but does NOT close
the dispersion problem. That still requires the separate condition that gamma
propagate as the exact continuum (Box_c) mode -- light not seeing the lattice
spacing -- exactly the protection examined in Ch.2 (sec:goldstone, sec:stiffness).
A jammed/incompressible (density=1) vacuum does not supply it either
(ch2_jammed2d.py): jamming rescales c but leaves the transverse dispersion cos(ka/2)
unchanged.

Requires numpy; matplotlib optional. Deterministic (no RNG).
"""

import numpy as np

N = 24000; x = np.arange(N, dtype=float)
k_hi = 1.0                      # gamma-like carrier; v_g = cos(0.5) ~ 0.878 c (toy, exaggerated vs real ka~0.1)

def force(u, beta):
    lin = np.zeros_like(u); lin[1:-1] = u[2:]-2*u[1:-1]+u[:-2]
    if beta == 0: return lin
    du = np.diff(u); cube = du**3; nl = np.zeros_like(u); nl[1:-1] = cube[1:]-cube[:-1]
    return lin + beta*nl

def split(u, ksplit=0.45):
    uh = np.fft.rfft(u); kk = 2*np.pi*np.fft.rfftfreq(N)
    lo = uh.copy(); lo[kk >= ksplit] = 0
    hi = uh.copy(); hi[kk <  ksplit] = 0
    return np.fft.irfft(lo, N), np.fft.irfft(hi, N)

def cen(p):
    p = np.abs(p)**2; s = p.sum(); return (x*p).sum()/s if s > 0 else 0.0

def run(amp, beta, steps=4000, dt=0.05, snaps=()):
    x0 = 2000.0; W = 120.0; env = np.exp(-((x-x0)/W)**2)
    base = env + 0.6*env*np.cos(k_hi*(x-x0))
    u = amp*base; v = -amp*np.gradient(base); F = force(u, beta)
    sep = []; shot = {}
    for s in range(steps+1):
        if s % 200 == 0:
            lo, hi = split(u); sep.append((cen(lo)-x0, cen(hi)-x0))
        if s in snaps: shot[s] = u.copy()
        u = u + v*dt + 0.5*F*dt*dt; Fn = force(u, beta); v = v + 0.5*(F+Fn)*dt; F = Fn
    return np.array(sep), shot

print("="*80)
print(" ch2_burstprop.py -- does a burst carry its gamma (high-k) content coherently?")
print("="*80)
print(f" gamma-like carrier ka={k_hi}: v_g = cos(ka/2) = {np.cos(k_hi/2):.3f} c ; low-k front ~ 1.0 c\n")
sepW, shotW = run(0.02, 1.0, snaps=(0, 4000))
sepS, shotS = run(0.50, 1.0, snaps=(0, 4000))
for tag, sep in [("WEAK (near-linear)", sepW), ("STRONG (nonlinear)", sepS)]:
    front = sep[-1, 0]; lag = sep[-1, 0]-sep[-1, 1]
    print(f" {tag:>20}: front moved {front:4.0f}, gamma lag {lag:4.0f}  "
          f"(predicted (1-cos)·dist = {(1-np.cos(k_hi/2))*front:.0f})")
print(" => gamma separates at v_g=cos(ka/2), same for weak and strong: the burst does NOT")
print("    carry its gamma content coherently. Over cosmological distance this IS the conflict.")
print("="*80)

# ---------------- figure ----------------
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 4.8))
    u0 = shotS[0]; uF = shotS[4000]; loF, hiF = split(uF)
    axA.plot(x, u0/np.abs(u0).max()+3.2, color="#888", lw=0.8, label="initial churning disturbance")
    axA.plot(x, loF/np.abs(uF).max()+1.6, color="#1f77b4", lw=1.0, label="after: low-k (GW-like) front")
    axA.plot(x, hiF/np.abs(uF).max(), color="#d62728", lw=0.8, label="after: high-k (gamma) content")
    clF = cen(loF); chF = cen(hiF)
    axA.annotate("", xy=(clF, 0.55), xytext=(chF, 0.55), arrowprops=dict(arrowstyle="<->", color="k"))
    axA.text((clF+chF)/2, 0.85, "gamma lags\n(dispersed off)", ha="center", fontsize=8)
    axA.set_xlim(1800, 4200); axA.set_yticks([]); axA.set_xlabel("position (lattice sites)")
    axA.set_title("(A) The churning front smooths toward low-k;\nits gamma (high-k) content lags behind", fontsize=10)
    axA.legend(fontsize=7.5, loc="upper right")
    axB.plot(sepW[:, 0], sepW[:, 0]-sepW[:, 1], "o-", color="#1f77b4", lw=1.6, label="weak (near-linear)")
    axB.plot(sepS[:, 0], sepS[:, 0]-sepS[:, 1], "s--", color="#d62728", lw=1.6, label="strong (nonlinear)")
    d = np.linspace(0, sepS[:, 0].max(), 50)
    axB.plot(d, (1-np.cos(k_hi/2))*d, color="k", ls=":", lw=1.2, label=r"$(1-\cos\frac{ka}{2})\times$distance")
    axB.set_xlabel("distance travelled by the front (sites)")
    axB.set_ylabel("gamma lag = front $-$ gamma position (sites)")
    axB.set_title("(B) The lag grows linearly with distance, same for\nweak and strong (nonlinearity does not help)", fontsize=10)
    axB.legend(fontsize=8, loc="upper left")
    fig.suptitle("Decisive test: a collective disturbance does NOT carry its gamma content coherently. The gamma (high-k)\n"
                 "separates at $v_g=c\\cos(ka/2)$ regardless of strength \u2014 over cosmological distance this is the Fermi "
                 "conflict, unchanged", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.90]); fig.savefig("ch2_burstprop.png", dpi=150)
    print("[figure written: ch2_burstprop.png]")
except Exception as e:
    print(f"[figure skipped: {e}]")
