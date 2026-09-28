#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_gammacontent.py -- gamma wavelengths live INSIDE ordinary lattice waves
===========================================================================

Premise (the burst-as-stiff-medium-event reading of Ch.2):
A gamma-ray burst is not light that propagates; it is a violent, volumetric
disturbance of the (very stiff) vacuum lattice -- the same disturbance whose
long-wavelength part is measured as a gravitational wave. This script makes two
quantitative points behind that reading, with no fitting and no RNG.

(1) SPECTRUM. A localized lattice disturbance contains a band of wavelengths.
    A *churning* (multi-scale / turbulent) disturbance carries content all the
    way into the gamma band and up to the lattice zone-boundary, whereas a
    smooth disturbance does not. Crucially the spectral SHAPE is independent of
    amplitude: a tiny-amplitude churning wave has the same gamma fraction as a
    huge one. So "gamma is present" is set by the disturbance's structure;
    "the energy is enormous" is set by its amplitude.

(2) ENERGETICS. Light is one quantum of the lattice mode (E = hbar*omega).
    A burst is the whole shaken 3D volume: E_burst / E_photon ~ (number of
    grains shaken). With E_burst ~ 1e53 erg and a 31 GeV gamma quantum this is
    ~2e54; equivalently a fully gamma-excited region of only ~1 m^3 holds an
    entire burst's energy -- a measure of how stiff and dense the medium is.

Calibration (framework): E(k) = 2*(hbar c/a)*sin(ka/2), hbar c/a = 311 GeV, so a
31 GeV photon sits at ka = 0.10 (= 63 lattice spacings) and the zone boundary
(ka = pi) is ~620 GeV. Lattice spacing a = 6.33e-19 m.

This supports the EMISSION side. It does NOT by itself address propagation;
ch2_burstprop.py shows the high-k (gamma) content disperses off the front, so the
dispersion tension is not closed here (see Ch.2, the burst/stiff-medium section).

Requires numpy; matplotlib optional. Deterministic.
"""

import numpy as np

hbar_c_over_a = 311.0           # GeV               DERIVED (a = 6.33e-19 m, c = light speed)
def E_of_k(ka): return 2*hbar_c_over_a*np.sin(np.clip(ka, 0, np.pi)/2)   # GeV

N = 200000; a = 1.0
x = np.arange(N)*a; xc = N/2
k = 2*np.pi*np.fft.rfftfreq(N, a); ka = k*a
Egev = E_of_k(ka)

print("="*78)
print(" ch2_gammacontent.py -- gamma wavelengths inside ordinary lattice waves")
print("="*78)
print(f" calibration: E(ka=0.10) = {E_of_k(0.10):.1f} GeV (the Fermi photon);  "
      f"zone boundary E(pi) = {E_of_k(np.pi):.0f} GeV")
print(f"              31 GeV photon  = {2*np.pi/0.10:.0f} lattice spacings (ka=0.10)\n")

def fractions(u):
    P = np.abs(np.fft.rfft(u))**2; tot = P.sum()
    band  = (Egev >= 1e-3) & (Egev <= 50.0)     # MeV .. 50 GeV
    highg = (Egev >= 10.0) & (Egev <= 50.0)      # 10 .. 50 GeV
    return P, 100*P[band].sum()/tot, 100*P[highg].sum()/tot

A = 0.01
smooth = A*np.exp(-((x-xc)/4000.0)**2)
moder  = A*np.exp(-((x-xc)/40.0)**2)
turb = np.zeros(N)
for s, off in [(3,0),(6,15),(2,-25),(9,40),(4,-60),(1.5,8)]:
    turb += A*np.exp(-((x-xc-off)/s)**2)
turb *= np.cos((x-xc)/3.0)                       # fine structure (churning)

print(" (1) spectral content of three SLIGHT disturbances (differ only in sharpness):")
for name, u in [("smooth large wave", smooth), ("moderate pulse", moder),
                ("turbulent (churning) front", turb)]:
    _, inband, high = fractions(u)
    print(f"     {name:>28}: MeV-50GeV {inband:5.1f}% ,  10-50 GeV {high:7.4f}%")
_, _, h1 = fractions(turb); _, _, h2 = fractions(turb*1e-4)
print(f"     amplitude-invariance: 10-50 GeV fraction at amp x1 = {h1:.4f}% , at amp x1e-4 = {h2:.4f}%")
print("     => gamma wavelengths are present even in a SLIGHT wave; amplitude sets the energy.\n")

# (2) energetics
c = 2.998e8; G = 6.674e-11; erg = 1e-7; eV = 1.602e-19; GeV = 1e9*eV; a_phys = 6.33e-19
Eph = 31*GeV; E_burst = 1e53*erg; Nq = E_burst/Eph; V = Nq*a_phys**3
print(" (2) energetics  (light = one quantum ; burst = whole shaken 3D volume):")
print(f"     one 31 GeV photon = {Eph:.2e} J ;  GRB ~1e53 erg = {Nq:.1e} gamma quanta")
print(f"     E_burst / E_light = {Nq:.1e}  = number of grains shaken (1 quantum/grain)")
print(f"     fully gamma-excited volume for one burst = {V:.2f} m^3  (side ~{V**(1/3):.1f} m)")
print(f"     vacuum stiffness revealed by GWs: c^4/G = {c**4/G:.2e} N  (= the modulus K in c^2=K/rho)")
print("="*78)

# ---------------- figure ----------------
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 4.8))
    w = 200; sl = slice(int(xc-w), int(xc+w))
    axA.plot(x[sl]-xc, turb[sl], color="#d62728", lw=1.3)
    axA.set_title("(A) A slight 'churning' lattice disturbance\n(small amplitude, multi-scale)", fontsize=10)
    axA.set_xlabel("position (lattice sites)"); axA.set_ylabel("displacement"); axA.set_xlim(-w, w)
    for name, u, c_ in [("smooth large wave", smooth, "#1f77b4"),
                        ("moderate pulse", moder, "#2ca02c"),
                        ("turbulent (churning) front", turb, "#d62728")]:
        P = np.abs(np.fft.rfft(u))**2; Pn = P/P.max(); m = Egev > 1e-4
        o = np.argsort(Egev[m]); axB.loglog(Egev[m][o], Pn[m][o], color=c_, lw=1.5, label=name, alpha=0.85)
    axB.axvspan(1e-3, 50, color="#fff3cd", alpha=0.5, zorder=0)
    axB.axvline(31, color="gray", ls=":", lw=1.3); axB.text(31, 1.4e-6, "31 GeV\n(Fermi)", fontsize=8, ha="center", color="#444")
    axB.axvline(622, color="k", ls="--", lw=1.0); axB.text(622, 2e-2, "lattice\ncutoff\n~620 GeV", fontsize=7.5, ha="center")
    axB.set_xlim(1e-3, 1.5e3); axB.set_ylim(1e-7, 3)
    axB.set_xlabel("photon energy  E = 2(\u0127c/a)sin(ka/2)  [GeV]"); axB.set_ylabel("spectral power (normalised)")
    axB.set_title("(B) Energy content of the SAME disturbance:\nchurning fronts reach the gamma band; smooth ones don't", fontsize=10)
    axB.legend(fontsize=7.5, loc="lower left")
    fig.suptitle("Gamma wavelengths live inside ordinary lattice waves: a churning disturbance carries content from low-k\n"
                 "(measured as a gravitational wave) up into the gamma band \u2014 amplitude sets the energy, not whether gamma is present",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.91]); fig.savefig("ch2_gammacontent.png", dpi=150)
    print("[figure written: ch2_gammacontent.png]")
except Exception as e:
    print(f"[figure skipped: {e}]")
