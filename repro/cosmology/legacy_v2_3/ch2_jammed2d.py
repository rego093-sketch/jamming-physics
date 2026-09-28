#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_jammed2d.py -- Does a JAMMED (density=1, no-void) vacuum remove light's dispersion?
=======================================================================================

THE QUESTION (the user's correction)
------------------------------------
A loose 1D FPU lattice (ch2_blastwave.py) found "coherence and high-k are mutually
exclusive". But the VP vacuum is not loose -- it is JAMMED by the no-void rule
(bi-um-geum-ji). Encode that cleanly as INCOMPRESSIBILITY: density is held = 1
everywhere at all times, i.e. the displacement field stays divergence-free,
div(u) = 0. Does maintaining density = 1 make a broadband disturbance propagate
COHERENTLY (all wavelengths together), rescuing the gamma-ray-burst dispersion?

This is physically the right encoding: an incompressible medium propagates only
TRANSVERSE (shear) waves -- and in the VP angle theory light IS a transverse
oscillation -- so density = 1 naturally selects the light-like modes.

WHAT THIS SCRIPT DOES (reproducibly, no fitting, no RNG)
-------------------------------------------------------
On a 2D elastic lattice with genuine finite-difference discreteness (so lattice
dispersion is real, not assumed away by a spectral method):
  Part 1  DISPERSION omega(k): transverse and longitudinal branches, for a
          COMPRESSIBLE lattice vs the INCOMPRESSIBLE one (density = 1 enforced by
          projecting the velocity divergence-free every step).
  Part 2  REAL-SPACE: launch a broadband transverse (= light) pulse; measure its
          spreading, compressible vs incompressible.
  Part 3  REAL-SPACE: launch a compression (longitudinal) pulse; show what density=1
          does to it.
  Part 4  THE DEFICIT LOCK: the transverse group-velocity deficit at the gamma
          photon's wavevector, and what (if anything) could change it.

WHAT IT FINDS (honest)
----------------------
 - density = 1 does NOT change the transverse (light) dispersion: v_g/c = cos(ka/2),
   IDENTICAL to the compressible lattice (Parts 1-2). It only FREEZES the longitudinal
   (compression) channel, which cannot propagate in an incompressible medium (Part 3).
 - So jamming does NOT give coherent broadband transmission of light. The dispersion
   is a robust property of the DISCRETE lattice, independent of the no-void rule.
 - The deficit is LOCKED by (c, a): 1 - v_g/c = (E/E_QG)^2 with E_QG = sqrt(8) hbar c/a
   ~ 882 GeV, fixed once c = light speed and a = 6.33e-19 m are set. Incompressibility
   cannot change c or a, so the gamma-burst conflict survives jamming (Part 4).

CONCLUSION (this SHARPENS the volume rather than rescuing it). The dispersion escape
is NOT delivered by the jammed/incompressible nature of the vacuum. It genuinely
requires the SEPARATE, load-bearing postulate that light is the exact CONTINUUM
(box_c) mode -- light does not see the lattice spacing (effective a -> 0 for light).
Non-dispersive + finite-c is exactly the box_c mode; a discrete lattice gives
dispersive-finite-c; incompressibility gives non-dispersive-infinite-c (instantaneous
pressure) or dispersive-finite-c (shear) -- never non-dispersive-AND-finite-c except
the postulated continuum mode. The continuum postulate is thus the irreducible crux,
distinct from (and not implied by) jamming.

Requires: numpy. matplotlib optional. Deterministic.
"""

import numpy as np

# =====================================================================
#  DISCLOSED PARAMETERS
# =====================================================================
# toy 2D lattice
Nx, Ny = 256, 96          # grid                                       # (toy)
a      = 1.0              # lattice spacing                            # (toy)
cT     = 1.0              # shear (transverse) speed                   # (toy)
cL     = np.sqrt(3.0)     # longitudinal speed, compressible case      # (toy; Poisson-like)
cL_inc = 60.0             # "incompressible": longitudinal frozen (large) # (toy)
# real-world anchors (Part 4)
hbar_c_eV_m = 1.97327e-7  # hbar*c in eV*m                             # MEASURED
a_phys = 6.33e-19         # m   lattice spacing (physics volume)       # DERIVED
E_phot = 31.0             # GeV GRB 090510 highest-energy photon       # MEASURED

# =====================================================================
#  2D elastic engine (finite-difference operators -> real lattice dispersion)
# =====================================================================
kx = 2*np.pi*np.fft.fftfreq(Nx); ky = 2*np.pi*np.fft.fftfreq(Ny)
KX, KY = np.meshgrid(kx, ky, indexing="ij")
Gx = 1j*np.sin(KX*a)/a; Gy = 1j*np.sin(KY*a)/a        # FD gradient symbols
G2 = np.abs(Gx)**2 + np.abs(Gy)**2; G2[0, 0] = 1.0

def lap(f):
    return (np.roll(f, 1, 0)+np.roll(f, -1, 0)+np.roll(f, 1, 1)+np.roll(f, -1, 1)-4*f)/a**2
def ddx(f): return (np.roll(f, -1, 0)-np.roll(f, 1, 0))/(2*a)
def ddy(f): return (np.roll(f, -1, 1)-np.roll(f, 1, 1))/(2*a)

def project(vx, vy):
    """Leray projection: remove the longitudinal part so div(v)=0 (density = 1)."""
    vxh = np.fft.fft2(vx); vyh = np.fft.fft2(vy)
    dot = (np.conj(Gx)*vxh + np.conj(Gy)*vyh)/G2
    vxh -= Gx*dot; vyh -= Gy*dot
    return np.real(np.fft.ifft2(vxh)), np.real(np.fft.ifft2(vyh))

def force(ux, uy, incompressible):
    if incompressible:
        return cT**2*lap(ux), cT**2*lap(uy)              # shear only; longitudinal frozen
    div = ddx(ux) + ddy(uy)
    return (cT**2*lap(ux) + (cL**2-cT**2)*ddx(div),
            cT**2*lap(uy) + (cL**2-cT**2)*ddy(div))

def run(ux, uy, vx, vy, incompressible, steps, dt):
    if incompressible: vx, vy = project(vx, vy)
    Fx, Fy = force(ux, uy, incompressible); hist = []
    for s in range(steps):
        vx = vx+0.5*Fx*dt; vy = vy+0.5*Fy*dt
        if incompressible: vx, vy = project(vx, vy)
        ux = ux+vx*dt; uy = uy+vy*dt
        Fx, Fy = force(ux, uy, incompressible)
        vx = vx+0.5*Fx*dt; vy = vy+0.5*Fy*dt
        if incompressible: vx, vy = project(vx, vy)
        if s % max(steps//8, 1) == 0 or s == steps-1:
            e = (vx**2+vy**2+ux**2+uy**2).sum(axis=1)
            hist.append((s*dt, e.copy()))
    return ux, uy, vx, vy, hist

def rms_x(e):
    xs = np.arange(len(e)); m = (xs*e).sum()/e.sum()
    return np.sqrt(((xs-m)**2*e).sum()/e.sum())

print("="*86)
print(" ch2_jammed2d.py -- does a JAMMED (density=1, no-void) vacuum remove light dispersion?")
print("="*86)

# =====================================================================
#  PART 1 -- dispersion: compressible vs incompressible
# =====================================================================
def branches(kx_, ky_, cL_):
    sx, sy = np.sin(kx_*a), np.sin(ky_*a)
    Lap = (4/a**2)*(np.sin(kx_*a/2)**2 + np.sin(ky_*a/2)**2)
    D = cT**2*Lap*np.eye(2) + (cL_**2-cT**2)/a**2*np.array([[sx*sx, sx*sy], [sx*sy, sy*sy]])
    return np.sqrt(np.maximum(np.linalg.eigvalsh(D), 0))   # [transverse, longitudinal]

def vg_T(cL_, axis="x"):
    ks = np.linspace(1e-3, np.pi, 400); wT = []
    for k in ks:
        kx_, ky_ = (k, 0.0) if axis == "x" else (k/np.sqrt(2), k/np.sqrt(2))
        wT.append(branches(kx_, ky_, cL_)[0])
    wT = np.array(wT); return ks, np.gradient(wT, ks)/np.gradient(wT, ks)[0]

print("\n[Part 1] transverse (= light) group velocity v_g/c along a lattice axis:")
ks, vgC = vg_T(cL);     ks, vgI = vg_T(cL_inc)
for kq in [0.1, 0.5, 1.0, 2.0]:
    i = np.argmin(abs(ks-kq))
    print(f"    ka={kq:>4}:  compressible {vgC[i]:.4f}   incompressible(density=1) {vgI[i]:.4f}   "
          f"cos(ka/2)={np.cos(kq/2):.4f}")
print("    => IDENTICAL: maintaining density = 1 does not change the light dispersion.")
print("       (the longitudinal branch, by contrast, is frozen to ~infinite frequency.)")

# =====================================================================
#  PART 2 -- real-space broadband transverse (= light) pulse
# =====================================================================
print("\n[Part 2] real-space broadband TRANSVERSE (light) packet -- spreading over distance:")
x = np.arange(Nx); x0 = 55; sig = 8.0; k0 = 1.5       # high-k carrier -> disperses
envx = np.exp(-((x-x0)/sig)**2); om = 2*np.sin(k0/2)
for inc in [False, True]:
    uy = np.outer(envx*np.cos(k0*(x-x0)), np.ones(Ny))
    vy = np.outer(om*envx*np.sin(k0*(x-x0)), np.ones(Ny))   # rightward traveling packet
    ux = np.zeros((Nx, Ny)); vx = np.zeros((Nx, Ny))
    _, _, _, _, h = run(ux, uy, vx, vy, inc, 1250, 0.08)
    sp = rms_x(h[-1][1])/rms_x(h[0][1])
    tag = "INCOMPRESSIBLE(density=1)" if inc else "compressible"
    print(f"    {tag:>26}: packet width x{sp:.2f}  (disperses; v_g=cos(k0/2)={np.cos(k0/2):.2f})")
    if not inc: shear_hist = h
    else: shear_hist_inc = h
print("    => the light pulse disperses the SAME with or without density = 1.")

# =====================================================================
#  PART 3 -- real-space compression (longitudinal) pulse
# =====================================================================
print("\n[Part 3] real-space COMPRESSION (longitudinal) pulse:")
cprof = np.exp(-((x-55)/8.0)**2)
ux2 = np.zeros((Nx, Ny)); vx2 = np.outer(-cL*np.gradient(cprof), np.ones(Ny))
Ei = (vx2**2).sum()
vp, _ = project(vx2, np.zeros((Nx, Ny)))
print(f"    compressible : propagates at c_L (fast).")
print(f"    incompressible(density=1): projection retains {100*(vp**2).sum()/Ei:.0f}% of its energy "
      f"-> FROZEN (the medium has no room to compress).")

# =====================================================================
#  PART 4 -- the deficit lock
# =====================================================================
E_lat = hbar_c_eV_m/a_phys/1e9            # GeV, zone-boundary scale hbar c / a
E_QG  = np.sqrt(8.0)*E_lat                 # GeV, deficit normalization sqrt(8) hbar c / a
deficit = (E_phot/E_QG)**2
print("\n[Part 4] the dispersion deficit is LOCKED by (c, a):")
print(f"    E_lattice = hbar c / a = {E_lat:.0f} GeV   (a = {a_phys:.2e} m, c = light speed)")
print(f"    E_QG = sqrt(8) * E_lattice = {E_QG:.0f} GeV")
print(f"    transverse deficit of a {E_phot:.0f} GeV photon: 1 - v_g/c = (E/E_QG)^2 = {deficit:.2e}")
print( "    incompressibility cannot change c or a, so this deficit -- and the GRB conflict -- survives.")

print("\n" + "="*86)
print(" CONCLUSION: density = 1 (jamming/no-void) freezes the compression channel but leaves")
print(" the transverse (light) mode dispersing as cos(ka/2). Jamming does NOT remove the")
print(" dispersion. The escape requires the SEPARATE postulate that light is the exact")
print(" continuum (box_c) mode (light does not see the lattice spacing) -- now isolated as")
print(" the irreducible crux, distinct from the jammed nature of the vacuum.")
print("="*86)

# =====================================================================
#  FIGURE
# =====================================================================
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axA, axB, axC) = plt.subplots(1, 3, figsize=(15.5, 4.8))

    # (A) dispersion: transverse (overlap) + longitudinal (frozen)
    wTc = np.array([branches(k, 0, cL)[0] for k in ks])
    wLc = np.array([branches(k, 0, cL)[1] for k in ks])
    wTi = np.array([branches(k, 0, cL_inc)[0] for k in ks])
    axA.plot(ks, wTc, color="#1f77b4", lw=2.4, label="transverse (light) -- compressible")
    axA.plot(ks, wTi, color="#ff7f0e", lw=1.4, ls="--", label="transverse (light) -- density=1")
    axA.plot(ks, wLc, color="#7f7f7f", lw=1.6, label="longitudinal -- compressible")
    axA.annotate("longitudinal frozen\n(density=1): -> off chart", (2.2, wLc[np.argmin(abs(ks-2.2))]),
                 fontsize=8, color="#555", ha="center")
    axA.set_xlabel("wavenumber  ka"); axA.set_ylabel(r"$\omega(k)$")
    axA.set_title("(A) Dispersion: the light branch is\nIDENTICAL with or without density=1", fontsize=10)
    axA.legend(fontsize=7.5, loc="upper left")

    # (B) real-space: final energy profile of the light packet, compressible vs density=1
    xs = np.arange(Nx)
    axB.plot(xs, shear_hist[-1][1], color="#1f77b4", lw=2.4, label="compressible")
    axB.plot(xs, shear_hist_inc[-1][1], color="#ff7f0e", lw=1.4, ls="--", label="density=1 (incompressible)")
    spf = rms_x(shear_hist[-1][1])/rms_x(shear_hist[0][1])
    axB.set_xlabel("position x (lattice sites)"); axB.set_ylabel("light-packet energy")
    axB.set_title(f"(B) Real-space light packet (dispersed x{spf:.1f}):\nIDENTICAL with or without density=1", fontsize=10)
    axB.set_xlim(0, Nx); axB.legend(fontsize=8)

    # (C) the deficit lock
    Es = np.logspace(-1, 3, 200)
    axC.loglog(Es, (Es/E_QG)**2, color="#d62728", lw=2.2)
    axC.axvline(E_phot, color="gray", ls=":", lw=1.2)
    axC.axhline(deficit, color="gray", ls=":", lw=1.2)
    axC.plot([E_phot], [deficit], "o", color="#d62728", ms=8)
    axC.annotate(f"31 GeV photon\n1 - v_g/c = {deficit:.1e}", (E_phot, deficit),
                 textcoords="offset points", xytext=(-90, 18), fontsize=8,
                 bbox=dict(boxstyle="round", fc="#fdecea", ec="#d62728"))
    axC.set_xlabel("photon energy E (GeV)")
    axC.set_ylabel(r"transverse deficit $1-v_g/c=(E/E_{QG})^2$")
    axC.set_title(f"(C) Deficit locked by (c, a):\n$E_{{QG}}=\\sqrt{{8}}\\,\\hbar c/a\\approx{E_QG:.0f}$ GeV, fixed", fontsize=10)

    fig.suptitle("A jammed (density=1, no-void) vacuum freezes compression but leaves LIGHT dispersing as "
                 "cos(ka/2):\njamming does not remove the dispersion -- the continuum (box_c) postulate "
                 "remains the irreducible crux", fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig("ch2_jammed2d.png", dpi=150)
    print("[figure written: ch2_jammed2d.png]")
except Exception as e:
    print(f"[figure skipped: {e}]")
