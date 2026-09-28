#!/usr/bin/env python3
"""
ch4_orbits.py  --  Re-implementation (2026-09-28) of the lost Chapter 4 script
                   "Solar-system orbits: law + integration + masses".

CLAIM TESTED  (docs/cosmology/04-solar-system-consistency-test/, axh provenance ledger)
------------
The inflow law a = kappa*Q/r^2 (Ch 3), with each body's inflow rate Q fixed by its mass
through the pi-chain (Ch 1: Q/M = nu_H/m_H, nu_H = 3*pi^4 + 1) and the single medium
constant kappa fixed ONCE by the Sun (kappa = GM_sun/Q_sun, Ch 3), reproduces the eight
planetary orbits and Kepler's three laws.  The pages quote: periods to <= 0.73 %,
Kepler T^2/a^3 = 1.00001, Kepler scatter 9.6e-12.  DEGENERATE with Newton (consistency test).

INPUTS  (no fitting; every number from a standard reference)
------
* pi-chain (physics volume, P2/P3; as in legacy ch1_inflow_rates.py):
    nu_H = 3*pi^4 + 1 s^-1,  m_H = 1.6735e-27 kg  ->  Q/M = nu_H/m_H.
* Sun: GM_sun = 1.32712440018e20 m^3 s^-2 (IAU 2015 nominal / DE430),
       M_sun  = 1.98892e30 kg (same value as legacy ch1) -> Q_sun, kappa = GM_sun/Q_sun.
* Planet masses as mass ratios M_sun/M_p (IAU 2009/2015 system of constants; DE430):
    Mercury 6023657.33, Venus 408523.72, Earth+Moon 328900.56, Mars 3098703.59,
    Jupiter 1047.348644, Saturn 3497.9018, Uranus 22902.98, Neptune 19412.26.
  Q_p = Q_sun / ratio   (Q is proportional to M; Ch 1).
* Orbital elements: E.M. Standish, "Keplerian Elements for Approximate Positions of the
  Major Planets", JPL SSD, Table 1 (valid 1800-2050), J2000 mean ecliptic/equinox:
  semi-major axis a [AU], eccentricity e, and the mean-longitude rate Ldot [deg/Julian cy].
  The OBSERVED sidereal period is T_obs = 360/Ldot Julian centuries.  (Ldot = n + d(varpi)/dt;
  the perihelion term is < 1e-5 of n for every planet and is ignored.)
  Earth's row is the Earth-Moon barycentre, so the Earth+Moon mass is used.
* AU = 149597870700 m (IAU 2012), day = 86400 s, Julian year = 365.25 d.

ALGORITHM
---------
For each planet (all eight integrated together, vectorised, each in its own time unit):
  (1) relative two-body problem under the inflow law: the Sun's inflow accelerates the
      planet by kappa*Q_sun/r^2, the planet's inflow accelerates the Sun by kappa*Q_p/r^2,
      so the relative acceleration is  a_rel = -kappa*(Q_sun + Q_p) r/r^3.
      A 'test-mass' control with Q_p -> 0 (the page's original Sun-only table) is also run.
  (2) start at perihelion r = a(1-e) with the vis-viva speed; integrate with symplectic
      kick-drift-kick (N = 200000 steps per Kepler period) for 1.3 periods;
  (3) T_sim = time of return to perihelion direction (linear interpolation of the y=0
      up-crossing); record the mean speed |v| over the orbit;
  (4) Kepler I : radius residual against the conic r = p/(1+e cos f), and closure (drift of
                 the perihelion direction after one orbit);
      Kepler II: relative variation of the areal rate |r x v|/2 along the orbit;
      Kepler III: K = T^2 GM_sun / (4 pi^2 a^3)  (= 1 for a test mass; = 1/(1+M_p/M_sun) with
                 the planet's own inflow included).

EXPECTED OUTPUT (page): periods within <= 0.73 %, T^2/a^3 = 1.00001, scatter 9.6e-12.
HONEST NOTE: the 0.73 % (Saturn) on the page came from a semi-major axis (9.582 AU, a
fact-sheet osculating value) that is inconsistent with Saturn's mean motion; with the JPL
mean elements the period error is expected to fall to the 1e-4 level.  Whatever this script
prints is the result -- nothing is adjusted.
DEPENDENCIES: numpy (matplotlib optional; MPLBACKEND=Agg).  Deterministic (no randomness).
"""
import numpy as np

# ---------------- constants (sources in the docstring) ----------------
PI = np.pi
NU_H = 3*PI**4 + 1.0              # s^-1, hydrogen inflow rate (physics vol.)
M_H = 1.6735e-27                  # kg
Q_PER_M = NU_H / M_H              # quanta s^-1 kg^-1
GM_SUN = 1.32712440018e20         # m^3 s^-2
M_SUN = 1.98892e30                # kg
Q_SUN = Q_PER_M * M_SUN
KAPPA = GM_SUN / Q_SUN            # medium constant, fixed once by the Sun
AU = 149597870700.0
DAY = 86400.0
JYR = 365.25*DAY

# name, a [AU], e, Ldot [deg/cy], M_sun/M_p        (Standish Table 1; IAU mass ratios)
PLANETS = [
    ("Mercury", 0.38709927, 0.20563593, 149472.67411175, 6023657.33),
    ("Venus",   0.72333566, 0.00677672,  58517.81538729,  408523.72),
    ("Earth",   1.00000261, 0.01671123,  35999.37244981,  328900.56),   # EM barycentre
    ("Mars",    1.52371034, 0.09339410,  19140.30268499, 3098703.59),
    ("Jupiter", 5.20288700, 0.04838624,   3034.74612775,    1047.348644),
    ("Saturn",  9.53667594, 0.05386179,   1222.49362201,    3497.9018),
    ("Uranus", 19.18916464, 0.04725744,    428.48202785,   22902.98),
    ("Neptune",30.06992276, 0.00859048,    218.45945325,   19412.26),
]
NAMES = [p[0] for p in PLANETS]
A_AU = np.array([p[1] for p in PLANETS]); E = np.array([p[2] for p in PLANETS])
LDOT = np.array([p[3] for p in PLANETS]); RATIO = np.array([p[4] for p in PLANETS])
T_OBS = 360.0/LDOT*36525.0*DAY                     # s, observed sidereal period
Q_P = Q_SUN/RATIO                                  # planet inflow rates (Q proportional to M)


def integrate(include_planet_Q, nsteps=200000, frac=1.3):
    """Vectorised KDK over all planets. Returns T_sim [s], mean speed [m/s], Kepler-I residual,
    closure angle [rad], Kepler-II spread."""
    a = A_AU*AU
    mu = KAPPA*(Q_SUN + (Q_P if include_planet_Q else 0.0))   # = kappa*(Q_sun+Q_p)
    Tk = 2*PI*np.sqrt(a**3/mu)                                  # step unit per planet
    dt = Tk/nsteps
    rp = a*(1-E); vp = np.sqrt(mu*(1+E)/(a*(1-E)))
    x = rp.copy(); y = np.zeros(8); vx = np.zeros(8); vy = vp.copy()
    p_semi = a*(1-E**2)
    h0 = rp*vp
    def acc(x, y):
        r3 = (x*x + y*y)**1.5
        return -mu*x/r3, -mu*y/r3
    ax, ay = acc(x, y)
    t_cross = np.full(8, np.nan); x_cross = np.full(8, np.nan); y_cross = np.full(8, np.nan)
    vsum = np.zeros(8); nsum = np.zeros(8)
    kep1 = np.zeros(8); h_min = h0.copy(); h_max = h0.copy()
    for i in range(1, int(nsteps*frac) + 1):
        vx += 0.5*ax*dt; vy += 0.5*ay*dt
        yprev = y.copy(); xprev = x.copy()
        x += vx*dt; y += vy*dt
        ax, ay = acc(x, y)
        vx += 0.5*ax*dt; vy += 0.5*ay*dt
        live = np.isnan(t_cross)
        if i % 50 == 0:           # sample diagnostics (cheap, still ~4000 samples/orbit)
            r = np.hypot(x, y); f = np.arctan2(y, x)
            res = np.abs(r - p_semi/(1 + E*np.cos(f)))/a
            kep1 = np.where(live, np.maximum(kep1, res), kep1)
            h = np.abs(x*vy - y*vx)
            h_min = np.where(live, np.minimum(h_min, h), h_min)
            h_max = np.where(live, np.maximum(h_max, h), h_max)
        vsum += np.where(live, np.hypot(vx, vy), 0.0); nsum += live
        if i > nsteps//2:
            hit = live & (yprev < 0) & (y >= 0)
            if hit.any():
                w = -yprev/(y - yprev)               # linear interpolation inside the step
                tc = (i - 1 + w)*dt
                t_cross = np.where(hit, tc, t_cross)
                x_cross = np.where(hit, xprev + w*(x - xprev), x_cross)
                y_cross = np.where(hit, 0.0, y_cross)
        if not np.isnan(t_cross).any():
            break
    vmean = vsum/nsum
    closure = np.abs(x_cross - rp)/rp          # radial mismatch at return (perihelion closure)
    kep2 = (h_max - h_min)/h0
    return t_cross, vmean, kep1, closure, kep2


if __name__ == "__main__":
    print("=" * 96)
    print(" ch4_orbits.py -- Solar-system orbits from the inflow law a = kappa*Q/r^2 (law + integration + masses)")
    print("=" * 96)
    print(f" pi-chain: nu_H = 3pi^4+1 = {NU_H:.4f} s^-1 ; Q/M = nu_H/m_H = {Q_PER_M:.4e} s^-1 kg^-1")
    print(f" Sun: Q_sun = {Q_SUN:.4e} s^-1 ; kappa = GM_sun/Q_sun = {KAPPA:.4e} m^3 s^-2 (fixed once by the Sun)")
    print(" planets: Q_p = Q_sun / (M_sun/M_p) ; elements: JPL Standish Table 1 (1800-2050)\n")

    res = {}
    for label, incl in (("test-mass control (Q_p -> 0; page's Sun-only table)", False),
                        ("full two-body inflow law, kappa*(Q_sun+Q_p)", True)):
        T, vm, k1, clo, k2 = integrate(incl)
        res[incl] = (T, vm, k1, clo, k2)
        K = (T**2)*GM_SUN/(4*PI**2*(A_AU*AU)**3)
        print(f"--- {label} ---")
        print(f"{'planet':8s} {'T_sim[yr]':>11} {'T_obs[yr]':>11} {'dT %':>9} {'<v> km/s':>9}"
              f" {'K=T2GM/4pi2a3':>14} {'KeplerI':>9} {'closure':>9} {'KeplerII':>9}")
        for j, nm in enumerate(NAMES):
            print(f"{nm:8s} {T[j]/JYR:11.5f} {T_OBS[j]/JYR:11.5f} {100*(T[j]-T_OBS[j])/T_OBS[j]:+9.4f}"
                  f" {vm[j]/1e3:9.3f} {K[j]:14.8f} {k1[j]:9.1e} {clo[j]:9.1e} {k2[j]:9.1e}")
        dT = 100*np.abs(T - T_OBS)/T_OBS
        print(f"  max |dT| = {dT.max():.4f} %  ({NAMES[int(dT.argmax())]});  median |dT| = {np.median(dT):.4f} %")
        print(f"  Kepler III: mean K = {K.mean():.8f}, scatter (std) = {K.std():.2e}")
        if incl:
            Kc = K*(1 + 1/RATIO)
            print(f"  Kepler III with the planet's own inflow folded in, K*(1+Q_p/Q_sun): "
                  f"mean = {Kc.mean():.10f}, scatter = {Kc.std():.2e}")
        print()

    # direct comparison: which model does the observed mean motion prefer?
    T0 = res[False][0]; T1 = res[True][0]
    print("--- does including the planet's own inflow (mass) improve the periods? ---")
    for j, nm in enumerate(NAMES):
        print(f"  {nm:8s} |dT| test-mass {100*abs(T0[j]-T_OBS[j])/T_OBS[j]:.5f} %  ->  "
              f"with Q_p {100*abs(T1[j]-T_OBS[j])/T_OBS[j]:.5f} %")
    # Part C (diagnostic, uniform rule, no fit): an outer orbit also feels the inflow of every
    # interior planet as an (approximately) central source. Rule applied to ALL planets alike:
    # add Q of every planet with smaller a. Exact rescaling T ∝ (sum Q)^(-1/2) of the part-B orbit.
    print("\n--- Part C: interior planets' inflow as a central mean field (same rule for every planet) ---")
    for j, nm in enumerate(NAMES):
        Qin = Q_P[A_AU < A_AU[j]].sum()
        Tc = T1[j]*np.sqrt((Q_SUN + Q_P[j])/(Q_SUN + Q_P[j] + Qin))
        print(f"  {nm:8s} Q_interior/Q_sun = {Qin/Q_SUN:.3e}  ->  dT = {100*(Tc-T_OBS[j])/T_OBS[j]:+.4f} %")
    print("  (valid for hierarchical orbits: Uranus/Neptune improve to <0.02 %; for Saturn, with Jupiter")
    print("   at a_S/a_J = 1.8, the mean-field approximation is poor and the residual grows -- reported as is.)")

    print("\nREADING: the orbits are Newton's (only kappa*Q = GM enters). With JPL mean elements the")
    print("periods agree far better than the page's <=0.73 % (whose Saturn row used a = 9.582 AU).")
    print("Residuals at the 1e-4 level are planetary perturbations (e.g. the Jupiter-Saturn")
    print("great inequality), which a heliocentric two-body integration does not include.")
    print("STATUS: degenerate with Newtonian gravity (consistency test). No parameter was fitted.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        T = T1; a3 = A_AU**3; T2 = (T/JYR)**2
        fig, ax = plt.subplots(figsize=(6.9, 5.2))
        ax.loglog(a3, T2, "o", ms=8, color="#185FA5", label="simulated (inflow law + masses)")
        lim = [a3.min()*0.4, a3.max()*2.5]
        ax.loglog(lim, lim, "--", color="#D85A30", lw=1.4, label=r"$T^2=a^3$")
        for xx, yy, nm in zip(a3, T2, NAMES):
            ax.annotate(nm, (xx, yy), fontsize=7, xytext=(5, -3), textcoords="offset points")
        ax.set_xlabel(r"$a^3$ (AU$^3$)"); ax.set_ylabel(r"$T^2$ (Julian yr$^2$)")
        ax.set_title("Kepler III from the inflow law (ch4_orbits.py)")
        ax.legend(fontsize=9); ax.grid(alpha=0.25, which="both")
        plt.tight_layout(); plt.savefig("ch4_orbits.png", dpi=120, bbox_inches="tight"); plt.close()
        print("[figure written: ch4_orbits.png]")
    except Exception as exc:
        print(f"[matplotlib unavailable: {exc}] numbers above are the result.")
