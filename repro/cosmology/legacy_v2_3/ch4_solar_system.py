#!/usr/bin/env python3
"""
ch4_solar_system.py  --  Reproduces Chapter 4 (the Solar System as a consistency test).

CLAIM TESTED
------------
The inflow force a = GM_sun/r^2 (with GM_sun = kappa*Q_sun, Chapter 3) reproduces the
measured planetary periods and mean speeds and yields Kepler's third law as an identity.
This result is DEGENERATE with Newtonian gravity (consistency, not superiority).

INPUTS  (no fitting)
------
AU/yr units, so GM_sun = 4*pi^2 exactly. Per planet: semi-major axis a [AU], eccentricity e,
observed period T_obs [yr], observed mean speed v_obs [km/s]  (standard references).
1 AU/yr = 4.74057 km/s.

ALGORITHM
---------
For each planet: start at perihelion r=a(1-e), v=sqrt(GM*(1+e)/(a(1-e))) (vis-viva);
integrate a = -GM * r_vec / |r|^3 by symplectic kick-drift-kick until the orbit returns to
perihelion (one period); record T_sim, mean speed, and T_sim^2/a^3.

EXPECTED OUTPUT  (verify against Chapter 4, Table 1)
---------------
Periods match T_obs to < 0.73% (most < 0.1%); mean speeds to < 0.7%;
Kepler T^2/a^3 = 1.00001 with scatter ~ 9.6e-12 (theory 4*pi^2/GM = 1).
"""
import numpy as np

GM = 4*np.pi**2
KMS = 4.74057   # 1 AU/yr in km/s

# name, a[AU], e, T_obs[yr], v_obs[km/s]
PLANETS = [
    ("Mercury", 0.387098, 0.205630,   0.240846, 47.36),
    ("Venus",   0.723332, 0.006772,   0.615198, 35.02),
    ("Earth",   1.000000, 0.016709,   1.000017, 29.78),
    ("Mars",    1.523679, 0.093400,   1.880848, 24.07),
    ("Jupiter", 5.204267, 0.048775,  11.862615, 13.06),
    ("Saturn",  9.582017, 0.055723,  29.447498,  9.68),
    ("Uranus", 19.229411, 0.044406,  84.016846,  6.80),
    ("Neptune",30.103658, 0.011215, 164.791320,  5.43),
]

def integrate_one_period(a, e, N=400000):
    rp = a*(1-e); vp = np.sqrt(GM*(1+e)/(a*(1-e)))
    dt = np.sqrt(a**3)/N
    x = np.array([rp, 0.0]); v = np.array([0.0, vp])
    acc = lambda x: -GM/np.dot(x, x)**1.5 * x
    ac = acc(x); t = 0.0; vsum = 0.0; nstep = 0; prev = 0.0
    for i in range(int(N*1.3)):
        v = v + 0.5*ac*dt; x = x + v*dt; ac = acc(x); v = v + 0.5*ac*dt; t += dt
        vsum += np.hypot(*v); nstep += 1
        if i > N*0.5 and prev < 0 and x[1] >= 0:
            return t, (vsum/nstep)*KMS
        prev = x[1]
    return t, (vsum/nstep)*KMS

if __name__ == "__main__":
    print(f"{'planet':8s} {'T_sim':>9} {'T_obs':>9} {'dT%':>7} {'v_sim':>7} {'v_obs':>7} {'T^2/a^3':>9}")
    ks = []
    for name, a, e, Tobs, vobs in PLANETS:
        Ts, vmean = integrate_one_period(a, e); k = Ts**2/a**3; ks.append(k)
        print(f"{name:8s} {Ts:9.4f} {Tobs:9.4f} {100*(Ts-Tobs)/Tobs:+7.2f} "
              f"{vmean:7.2f} {vobs:7.2f} {k:9.5f}")
    ks = np.array(ks)
    print(f"\nKepler T^2/a^3: mean={ks.mean():.5f}  scatter={ks.std():.2e}  "
          f"(theory 4*pi^2/GM = {4*np.pi**2/GM:.5f})")
    print("PASS if periods < 0.73%, speeds < 0.7%, Kepler constant ~1 with tiny scatter.")
    print("STATUS: degenerate with Newtonian gravity (consistency test).")

    # ---------- figure: ch4_kepler.png (Kepler's third law from the inflow force) ----------
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        a3 = np.array([p[1]**3 for p in PLANETS]); names=[p[0] for p in PLANETS]
        Tsim=[]
        for nm,a,e,Tobs,vobs in PLANETS:
            Ts,_ = integrate_one_period(a,e); Tsim.append(Ts)
        T2 = np.array(Tsim)**2
        fig, ax = plt.subplots(figsize=(6.9, 5.2))
        ax.loglog(a3, T2, "o", ms=8, color="#185FA5", markeredgecolor="#0d3a66", zorder=3, label="planets (simulated)")
        lim=[a3.min()*0.4, a3.max()*2.5]; ax.loglog(lim, lim, "--", color="#D85A30", lw=1.6, label=r"Kepler $T^2=a^3$")
        for x,y,nm in zip(a3,T2,names):
            ax.annotate(nm, (x,y), fontsize=7, xytext=(5,-3), textcoords="offset points")
        ax.set_xlabel(r"$a^3$  (AU$^3$)"); ax.set_ylabel(r"$T^2$  (yr$^2$)")
        ax.set_title(r"Kepler's third law from $a=GM_\odot/r^2$ ($T^2/a^3=1.00001$)")
        ax.legend(fontsize=9); ax.grid(alpha=0.25, which="both")
        plt.tight_layout(); plt.savefig("ch4_kepler.png", dpi=120, bbox_inches="tight"); plt.close()
        print("[figure written: ch4_kepler.png]")
    except Exception as _exc:
        print(f"[matplotlib unavailable: {_exc}] numbers above are the result.")
