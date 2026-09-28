#!/usr/bin/env python3
"""
ch10_post_newtonian.py  --  Re-implementation (2026-09-28) of the lost Chapter 10 script.

CLAIM TESTED  (docs/cosmology/10-post-newtonian-sector/, axb reproducibility map row 10)
------------
The medium reproduces the classical post-Newtonian tests, DEGENERATE with general relativity,
conditional on its two response coefficients gamma = beta = 1:
  * light bending through the gravitational index  n(r) = 1 + (1+gamma) GM/(r c^2):
        page: "solar grazing ray: alpha = 1.751 arcsec (Eddington 1.75; GR-degenerate)"
  * Shapiro delay  dt = (1+gamma) GM/c^3 ln(4 r1 r2 / b^2):   page: "up to 240 us"
  * gravitational redshift  dnu/nu = g h / c^2:                page: "2.5e-15 over 22.5 m"
  * Mercury perihelion under the PPN effective potential, gamma = beta = 1:
        page: "Newton control: perihelion drift = 0.0 arcsec/century;
               PPN (g=b=1): perihelion drift = 42.98 arcsec/century (observed 43)";
        map:  "(degenerate; Yoshida-4 cross-check +42.4")"
  * Gravity Probe B geodetic precession (gamma-controlled):     page: "6606 mas/yr"
OPEN (not computed, as on the page): beta from first principles; the gravitomagnetic
(frame-dragging, 39 mas/yr) coefficient.  The redshift uses the equivalence principle as
imported from the physics volume (velocity-saturation/cap level) -- it is NOT re-derived here.

INPUTS  (no fitting)
------
GM_sun = 1.32712440018e20 m^3 s^-2; R_sun = 6.957e8 m (IAU 2015 nominal); c = 299792458 m/s;
AU = 1.495978707e11 m; Mars at 1.5237 AU (superior conjunction geometry);
Mercury a = 0.38709927 AU, e = 0.20563593 (JPL Standish Table 1);
Pound-Rebka: g = 9.80665 m/s^2, h = 22.5 m;  GP-B: GM_earth = 3.986004418e14, R_E = 6.371e6 m,
altitude 642 km (circular polar orbit).  gamma, beta are set to 1 (the page's stated condition).

ALGORITHM
---------
A) Fermat ray: integrate d(x)/ds = p/n, d(p)/ds = grad n (RK4, step 1e-3 r) for a ray with impact
   parameter b = R_sun from x = -1e5 b to +1e5 b; deflection = angle of the final p.
   Shapiro: integrate (n-1)/c along the straight Earth -> grazing -> Mars path; round trip = 2x.
B) Mercury: RK4 (400 steps per orbit is ample; 2000 used) of the PPN test-body equation
      a = -GM r/r^3 + GM/(c^2 r^3) [ (2(gamma+beta) GM/r - gamma v^2) r + 2(1+gamma)(r.v) v ]
   for 100 Julian years (415 orbits); the perihelion longitude is the angle of the Laplace-Runge-
   Lenz vector, averaged per orbit, and its secular drift is a linear fit in time.  Newton
   control = same code with the 1/c^2 term off.  A 50-orbit scan over (gamma,beta) checks the
   (2+2gamma-beta)/3 scaling.
C) GP-B geodetic rate for a circular orbit: Omega = (gamma + 1/2) (GM)^(3/2) / (c^2 r^(5/2)).
EXPECTED OUTPUT: 1.751"; ~240 us; 2.5e-15; Newton 0.0, PPN 42.98 "/cy; ~6.6 "/yr.
DEPENDENCIES: numpy (matplotlib not used). Deterministic.
"""
import math
import numpy as np

GM = 1.32712440018e20
RSUN = 6.957e8
C = 299792458.0
AU = 1.495978707e11
ARCSEC = math.pi/(180*3600)
JYR = 365.25*86400.0


def n_index(x, y, gam=1.0):
    return 1.0 + (1 + gam)*GM/(math.hypot(x, y)*C**2)


def ray_deflection(b, gam=1.0, Lfac=1e5):
    k = (1 + gam)*GM/C**2
    def rhs(s):
        x, y, px, py = s
        r = math.hypot(x, y); n = 1 + k/r
        gx = -k*x/r**3; gy = -k*y/r**3
        return (px/n, py/n, gx, gy)
    x0 = -Lfac*b
    s = (x0, b, n_index(x0, b, gam), 0.0)
    while s[0] < Lfac*b:
        h = 1e-3*math.hypot(s[0], s[1])
        k1 = rhs(s)
        k2 = rhs(tuple(s[i] + 0.5*h*k1[i] for i in range(4)))
        k3 = rhs(tuple(s[i] + 0.5*h*k2[i] for i in range(4)))
        k4 = rhs(tuple(s[i] + h*k3[i] for i in range(4)))
        s = tuple(s[i] + h*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6 for i in range(4))
    return -math.atan2(s[3], s[2])       # bending toward the Sun (positive)


def shapiro_one_way(r1, r2, b, gam=1.0, N=2_000_001):
    """Straight path from Earth (x=-sqrt(r1^2-b^2)) to Mars (x=+sqrt(r2^2-b^2)) at impact b."""
    x1 = -math.sqrt(r1**2 - b**2); x2 = math.sqrt(r2**2 - b**2)
    # substitution x = b sinh(u) resolves the peak at closest approach
    u = np.linspace(math.asinh(x1/b), math.asinh(x2/b), N)
    x = b*np.sinh(u); dx = b*np.cosh(u)
    integrand = (1 + gam)*GM/(np.sqrt(x**2 + b**2)*C**2)*dx
    du = u[1] - u[0]
    return (integrand.sum() - 0.5*(integrand[0] + integrand[-1]))*du/C


def ppn_acc(x, y, vx, vy, gam, bet, on):
    r2 = x*x + y*y; r = math.sqrt(r2); r3 = r2*r
    ax = -GM*x/r3; ay = -GM*y/r3
    if on:
        v2 = vx*vx + vy*vy; rv = x*vx + y*vy
        f = GM/(C**2*r3)
        c1 = 2*(gam + bet)*GM/r - gam*v2; c2 = 2*(1 + gam)*rv
        ax += f*(c1*x + c2*vx); ay += f*(c1*y + c2*vy)
    return ax, ay


def mercury_drift(norbits, gam=1.0, bet=1.0, on=True, spo=2000, a_au=0.38709927, e=0.20563593):
    a = a_au*AU; rp = a*(1 - e); vp = math.sqrt(GM*(1 + e)/rp)
    T = 2*math.pi*math.sqrt(a**3/GM); h = T/spo
    x, y, vx, vy = rp, 0.0, 0.0, vp
    ts, angs = [], []
    acc_ang = 0.0; cnt = 0; unwrap_prev = None
    for i in range(int(norbits*spo)):
        def f(s):
            ax, ay = ppn_acc(s[0], s[1], s[2], s[3], gam, bet, on)
            return (s[2], s[3], ax, ay)
        s = (x, y, vx, vy)
        k1 = f(s)
        k2 = f(tuple(s[j] + 0.5*h*k1[j] for j in range(4)))
        k3 = f(tuple(s[j] + 0.5*h*k2[j] for j in range(4)))
        k4 = f(tuple(s[j] + h*k3[j] for j in range(4)))
        x, y, vx, vy = (s[j] + h*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6 for j in range(4))
        # Laplace-Runge-Lenz vector (Newtonian osculating) -> perihelion longitude
        hz = x*vy - y*vx; r = math.hypot(x, y)
        Ax = vy*hz/GM - x/r; Ay = -vx*hz/GM - y/r
        ang = math.atan2(Ay, Ax)
        acc_ang += ang; cnt += 1
        if cnt == spo:
            ts.append((i + 1 - spo/2)*h); angs.append(acc_ang/cnt); acc_ang = 0.0; cnt = 0
    ts = np.array(ts); angs = np.unwrap(np.array(angs))
    slope = np.polyfit(ts, angs, 1)[0]                 # rad/s
    return slope*100*JYR/ARCSEC                         # arcsec per Julian century


if __name__ == "__main__":
    print("=" * 88)
    print(" ch10_post_newtonian.py -- classical tests from the gravitational index, gamma = beta = 1")
    print("=" * 88)
    # A: light bending
    alpha = ray_deflection(RSUN)/ARCSEC
    alpha_an = 4*GM/(C**2*RSUN)/ARCSEC
    print("# A: ray through n(r)=1+(1+gamma)GM/(r c^2), Fermat bending, gamma=1")
    print(f"solar grazing ray: alpha = {alpha:.4f} arcsec  (analytic 4GM/c^2b = {alpha_an:.4f}; Eddington 1.75; GR-degenerate)")
    alpha0 = ray_deflection(RSUN, gam=0.0)/ARCSEC
    print(f"  control gamma=0 (Newtonian-corpuscle half value): alpha = {alpha0:.4f} arcsec")
    # Shapiro
    r1 = 1.0*AU; r2 = 1.5237*AU
    dt1 = shapiro_one_way(r1, r2, RSUN)
    dt_an = 2*GM/C**3*math.log(4*r1*r2/RSUN**2)
    print(f"Shapiro delay Earth-Mars, grazing: one way {dt1*1e6:.1f} us (analytic {dt_an*1e6:.1f} us);"
          f" round trip {2*dt1*1e6:.1f} us  (page: 'up to 240 us')")
    # redshift
    print(f"Pound-Rebka redshift g h/c^2 = {9.80665*22.5/C**2:.3e}   (page 2.5e-15; EP imported, not re-derived)")

    # B: Mercury perihelion
    print("\n# B: Mercury under PPN effective potential, gamma=beta=1 (RK4, 2000 steps/orbit, 100 yr)")
    a = 0.38709927*AU; e = 0.20563593
    T = 2*math.pi*math.sqrt(a**3/GM); norb = 100*JYR/T
    d_newton = mercury_drift(norb, on=False)
    d_ppn = mercury_drift(norb)
    d_an = 6*math.pi*GM/(a*(1 - e**2)*C**2)/T*100*JYR/ARCSEC
    print(f"Newton control: perihelion drift = {d_newton:.3f} arcsec/century")
    print(f"PPN (g=b=1): perihelion drift = {d_ppn:.2f} arcsec/century   (analytic {d_an:.2f}; observed 43)")
    print("  (gamma,beta) scaling check over 50 orbits, expected factor (2+2gamma-beta)/3:")
    for g_, b_ in ((1, 1), (0, 0), (1, 0), (0.5, 1)):
        d = mercury_drift(50, gam=g_, bet=b_, spo=1000)
        print(f"    gamma={g_:<4} beta={b_:<3}: {d:7.2f} \"/cy   ratio to (1,1) analytic = {d/d_an:.4f}"
              f"  expected {(2+2*g_-b_)/3:.4f}")

    # C: GP-B geodetic
    GME = 3.986004418e14; r = 6.371e6 + 642e3
    om = 1.5*GME**1.5/(C**2*r**2.5)
    print(f"\n# C: GP-B geodetic (gamma+1/2)(GM)^1.5/(c^2 r^2.5) = {om*JYR/ARCSEC*1e3:.0f} mas/yr"
          f"  (page 6606; point-mass circular orbit, no J2)")
    print("  frame dragging (39 mas/yr) and beta from first principles: OPEN, not computed.")
    print("\nSTATUS: all four tests degenerate with GR, conditional on gamma = beta = 1 (redshift: neither).")
