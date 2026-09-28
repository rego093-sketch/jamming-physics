#!/usr/bin/env python3
"""
ch5_mercury_capture.py  --  Re-implementation (2026-09-28) of the lost Chapter 5 (v2) script
                            "Mercury 3:2 capture probability".

CLAIM TESTED  (docs/cosmology/05-axial-spin-tidal-locking-inflow/ "The 3:2 capture probability,
               computed (v2)"; 16-open-problems-gathered/; axj log #5)
------------
Page text: "for the constant-Q model Goldreich & Peale (1966) give P_cap ~ 0.07, while core-mantle
friction and a chaotically higher past eccentricity raise it to ~0.55-0.73 (Correia & Laskar
2004). A vectorised ensemble integration of the resonant pendulum
    gamma'' = -1/2 w0^2 sin 2 gamma - drift - friction(gamma')
(libration period 15.7 yr, matching the observed 12-15 yr) reproduces the mechanism: capture is
probabilistic, falling as the tidal sweep speeds up (1.00 -> 0.06) and rising with friction."
The capture probability is standard spin-orbit physics (not framework-specific); the tidal torque
is the gradient of the inflow (Ch 5), which at this level is identical to conventional tides.

INPUTS  (no fitting)
------
* Mercury: e = 0.2056, orbital period P_orb = 87.969 d (JPL fact sheet).
* Triaxiality (B-A)/C = 1.2e-4 (the value the page states for Mercury).
* Resonance strengths H(p,e): Goldreich-Peale e-function series (same truncated series as the
  legacy ch5_spin_tidal.py part D).
* Tidal models (the only choice, and it is the one the page says the probability depends on):
    viscous / constant time-lag :  torque_p ∝ -H_p^2 (theta' - p n)
    constant-Q (constant lag)   :  torque_p ∝ -H_p^2 sign(theta' - p n)      (Goldreich & Peale 1966)
  Near theta' = 3n/2 each model splits into a constant drift K and a gamma'-dependent part.
* Ensemble: 1000 initial phases on a uniform deterministic grid (no random numbers).

ALGORITHM
---------
(1) libration period of the 3:2:  w0 = n sqrt(3 (B-A)/C * H(3/2,e)); analytic, and measured by
    integrating the conservative averaged pendulum in physical time.
(2) capture probability for a slow drift across the separatrix (energy-balance / GP formula):
      P = (dE_upper + dE_lower) / dE_upper, separatrix gamma' = w0 cos gamma
      viscous : P = 2 / (1 + pi K / (2 eps w0))           (K/eps fixed by the H_p)
      const-Q : P = 2 K1 / (K0 + K1)                         (K1 = H_{3/2}^2, K0 = sum of the rest)
    and a vectorised ensemble check of each formula.
(3) sweep: P versus sweep speed x = pi K/(2 eps w0) on a doubling grid x = 1/4 ... 64
    (grid fixed a priori; its endpoint sets the smallest P printed).
(4) friction: add a core-mantle-like linear damping eps_c gamma' at Mercury's viscous K; P vs eps_c/eps.
(5) eccentricity: viscous-model P at e = 0.10, 0.206, 0.30 (series truncated; e <~ 0.3).
EXPECTED OUTPUT (page): libration period 15.7 yr; P falling 1.00 -> 0.06 with sweep speed, rising
with friction; constant-Q P ~ 0.07 (GP66, literature); 0.55-0.73 (CL04, literature, not re-run).
DEPENDENCIES: numpy (matplotlib optional). Deterministic.
"""
import numpy as np

E_MERC = 0.2056
P_ORB_D = 87.969
BAC = 1.2e-4
DAY = 86400.0; YR = 365.25*DAY


def Hpe(e):
    """Goldreich-Peale resonance strengths (truncated series), p = spin/orbit ratio."""
    return {0.5: -e/2 + e**3/16,
            1.0: 1 - 5*e**2/2 + 13*e**4/16,
            1.5: 7*e/2 - 123*e**3/16,
            2.0: 17*e**2/2 - 115*e**4/6,
            2.5: 845*e**3/48,
            3.0: 533*e**4/16}


def model_coeffs(e):
    """Drift/dissipation split of the tidal torque near theta' = 1.5 n (units of n, common factor dropped)."""
    H = Hpe(e); H2 = {p: H[p]**2 for p in H}
    # viscous: torque = -sum H_p^2 (1.5 n + gamma' - p n)  =  -K - eps*gamma'
    K_v = sum(H2[p]*(1.5 - p) for p in H2); eps_v = sum(H2.values())
    # constant-Q: torque = -sum_{p != 1.5} H_p^2 sign(1.5-p) - H_{1.5}^2 sign(gamma')
    K0 = sum(H2[p]*np.sign(1.5 - p) for p in H2 if p != 1.5); K1 = H2[1.5]
    return K_v, eps_v, K0, K1


def w0_over_n(e, bac=BAC):
    return np.sqrt(3*bac*abs(Hpe(e)[1.5]))


def P_viscous(x):            # x = pi K / (2 eps w0)
    return min(1.0, 2/(1 + x))


def ensemble(torque, gdot0=1.2, t_end=None, dt=0.1, nphase=1000, K_scale=None):
    """Averaged pendulum in units w0 = 1:  g'' = -1/2 sin 2g + torque(g').
    Start above the separatrix with gamma' = gdot0 and a uniform grid of phases; return the fraction
    inside the separatrix (E < 1/4) at the end."""
    g = np.linspace(0, np.pi, nphase, endpoint=False)
    w = np.full(nphase, gdot0)
    nsteps = int(t_end/dt)
    for _ in range(nsteps):
        w += (-0.5*np.sin(2*g) + torque(w))*dt
        g += w*dt
    Eng = 0.5*w**2 - 0.25*np.cos(2*g)
    return float(np.mean(Eng < 0.25))


if __name__ == "__main__":
    print("=" * 92)
    print(" ch5_mercury_capture.py -- probability of capture into Mercury's 3:2 spin-orbit resonance")
    print("=" * 92)
    H = Hpe(E_MERC)
    n = 2*np.pi/(P_ORB_D*DAY)
    r = w0_over_n(E_MERC)
    P_lib_an = 2*np.pi/(r*n)/YR
    print(f"(1) libration: e={E_MERC}, (B-A)/C={BAC:.1e}, H(3/2,e)={H[1.5]:.4f}  ->  w0/n = {r:.5f}")
    print(f"    analytic small-amplitude libration period = {P_lib_an:.2f} yr")
    # numerical: conservative averaged pendulum in physical time, small amplitude
    w0 = r*n; dtp = (2*np.pi/w0)/4000; g = 0.05; wv = 0.0; t = 0.0; crossings = []
    prev = g
    for i in range(4000*6):
        wv += -0.5*w0**2*np.sin(2*g)*dtp; g += wv*dtp; t += dtp
        if prev < 0 <= g: crossings.append(t)
        prev = g
    P_lib_num = np.mean(np.diff(crossings))/YR
    print(f"    integrated pendulum libration period       = {P_lib_num:.2f} yr   (page: 15.7 yr; observed 12-15 yr)")

    K_v, eps_v, K0, K1 = model_coeffs(E_MERC)
    x_M = np.pi*(K_v/eps_v)/(2*r)       # K/eps is in units of n; w0 = r n
    print(f"\n(2) tidal-model split near theta'=1.5n at e={E_MERC}:")
    print(f"    viscous : K/eps = {K_v/eps_v:.4f} n  (pseudo-synchronous spin 1.5-K/eps = {1.5-K_v/eps_v:.3f} n)")
    print(f"              x = pi K/(2 eps w0) = {x_M:.2f}  ->  P_cap = 2/(1+x) = {P_viscous(x_M):.3f}")
    PQ = 2*K1/(K0 + K1)
    print(f"    const-Q : K0 = {K0:.4f}, K1 = H(3/2)^2 = {K1:.4f}  ->  P_cap = 2K1/(K0+K1) = {PQ:.3f}")
    print(f"    (page, citing GP66 'constant-Q': P ~ 0.07)")

    # ensemble checks of both formulas (w0 = 1 units)
    eps = 5e-4
    Kv = x_M*2*eps/np.pi
    Pv_ens = ensemble(lambda w: -Kv - eps*w, t_end=2.9/Kv)
    k1 = 1e-3; k0 = k1*K0/K1; delta = 0.02
    PQ_ens = ensemble(lambda w: -k0 - k1*np.tanh(w/delta), t_end=2.9/(k0 + k1*0.0) if k0 > 0 else 1e4, dt=0.02)
    print(f"    ensemble (1000 phases): viscous P = {Pv_ens:.3f} (formula {P_viscous(x_M):.3f});"
          f"  const-Q P = {PQ_ens:.3f} (formula {PQ:.3f})")

    print("\n(3) sweep speed: P versus x = pi K/(2 eps w0), eps = 5e-4 w0 (viscous torque)")
    xs = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64]
    Ps = []
    for x in xs:
        K = x*2*eps/np.pi
        P = ensemble(lambda w, K=K: -K - eps*w, t_end=min(2.9/K, 12/eps) + 4/eps)
        Ps.append(P)
        print(f"    x = {x:6.2f}  ensemble P = {P:.3f}   formula {P_viscous(x):.3f}")

    print("\n(4) friction: extra linear (core-mantle-like) damping eps_c at Mercury's viscous K")
    Pf = []
    for f in (0, 1, 3, 10, 30):
        et = eps*(1 + f)
        P = ensemble(lambda w, et=et: -Kv - et*w, t_end=2.9/Kv)
        Pf.append(P)
        print(f"    eps_c/eps = {f:3d}  ensemble P = {P:.3f}   formula {min(1, 2/(1 + np.pi*Kv/(2*et))):.3f}")

    print("\n(5) eccentricity (viscous model, formula; series truncated, e <~ 0.3):")
    for e in (0.10, 0.206, 0.30):
        Kv_e, eps_e, _, _ = model_coeffs(e)
        if Kv_e <= 0:
            print(f"    e = {e:5.3f}  K/eps = {Kv_e/eps_e:+.3f} n: pseudo-synchronous spin {1.5-Kv_e/eps_e:.3f} n lies ABOVE"
                  f" 1.5 n -> the viscous drift never reaches the 3:2 (no capture formula applies)")
            continue
        x = np.pi*(Kv_e/eps_e)/(2*w0_over_n(e))
        print(f"    e = {e:5.3f}  x = {x:6.2f}  P = {P_viscous(x):.3f}")

    print("\nREADING: capture is probabilistic; P falls as the sweep speeds up and rises with friction.")
    print("The ~7 % figure is reproduced by the VISCOUS (constant time-lag) torque at (B-A)/C = 1.2e-4;")
    print("the frequency-independent constant-Q torque gives a much larger P (see (2)). The CL04 values")
    print("0.55-0.73 (core-mantle friction + chaotic eccentricity) are cited, not re-derived here.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.8, 4.4))
        xx = np.logspace(np.log10(0.2), np.log10(80), 200)
        ax.semilogx(xx, [P_viscous(v) for v in xx], color="#D85A30", lw=1.6, label="formula 2/(1+x)")
        ax.semilogx(xs, Ps, "o", color="#185FA5", label="ensemble (1000 phases)")
        ax.axvline(x_M, ls=":", color="#555", label=f"Mercury, viscous (x={x_M:.1f})")
        ax.set_xlabel(r"sweep speed $x=\pi K/(2\varepsilon\omega_0)$"); ax.set_ylabel(r"$P_{\rm cap}$(3:2)")
        ax.set_title("Mercury 3:2 capture probability"); ax.legend(fontsize=8); ax.grid(alpha=0.25)
        plt.tight_layout(); plt.savefig("ch5_mercury_capture.png", dpi=120, bbox_inches="tight"); plt.close()
        print("[figure written: ch5_mercury_capture.png]")
    except Exception as exc:
        print(f"[matplotlib unavailable: {exc}] numbers above are the result.")
