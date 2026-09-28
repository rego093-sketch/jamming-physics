#!/usr/bin/env python3
"""
ch9_cmb_floor.py  --  Re-implementation (2026-09-28) of the lost Chapter 9 script
"the temperature floor made quantitative: the dark-matter contrast and the energy balance".

PAGE CLAIM (docs/cosmology/09-microwave-background-present-lattice-emission/)
  (A) "Two regions are integrated under identical dynamics ... ordinary space, in perpetual
      radiative contact with the ever-present light of the medium ... and a vacuum-deficit region,
      in which the annihilated medium provides no such contact. Started identically hot, ordinary
      space relaxes to a nonzero floor and holds it, while the deficit region decays to absolute zero."
  (B) "u = aT^4 with a = 4 sigma/c = 7.566e-16 J m^-3 K^-4. The observed background T = 2.725 K
      corresponds to u_CMB = 4.17e-14 J m^-3; the volume's stated relation u_CMB ~ 80 u_* then
      implies a starlight density u_* ~ 5.2e-16 J m^-3, within the band of the measured cosmic
      optical background."  + "grain energy hbar c/a ~ 312 GeV ... ~3.6e15 K".
  Status on the page: mechanism shown, balance consistent, ABSOLUTE 2.725 K still anchored [O].

INPUTS (sources)
  - Lattice units m = k = a = 1 (same convention as legacy ch9_lattice_cmb.py).
  - Bath temperature T_bath = 1 (lattice units) for the light-bathed region: the "ever-present
    light" is modelled as a thermal bath (fluctuation-dissipation pair). Deficit region: same
    damping, NO bath noise (annihilated medium -> no radiative contact).
  - SI constants: sigma_SB = 5.670374419e-8, c = 2.99792458e8, hbar, k_B (CODATA 2018).
  - T_CMB = 2.725 K (FIRAS). Factor 80 = the volume's stated u_CMB/u_* (NOT derived here).
  - Lattice spacing a = 6.33e-19 m (legacy ch9_lattice_cmb.py / physics volume).
  - Cosmic optical background (for the "within the band" check), converted u = 4 pi I / c:
    Lauer et al. 2022 (New Horizons, ApJL 927 L8): 16.37 +/- 1.47 nW m^-2 sr^-1;
    Postman et al. 2024 (ApJ 972 95): 11.16 +/- 1.65 nW m^-2 sr^-1.

ALGORITHM
  A: two 1-D harmonic chains (N=400), identical initial velocities at T0 = 5, velocity-Verlet
     plus Langevin damping gamma = 0.5; the bathed chain also gets noise sqrt(2 gamma T_bath / dt).
     Integrate to t = 1000; report <T_kin> over t > 200 for both.
  B: Stefan-Boltzmann arithmetic; back-compute u_*; compare with the COB band; also the forward
     direction (measured u_COB x 80 -> T) to expose the circularity.
  Deterministic: numpy default_rng(SEED=19).

EXPECTED (page): A: bathed floor > 0 held; deficit -> 0.   B: a = 7.566e-16, u_CMB = 4.17e-14,
  u_* = 5.2e-16 inside the COB band; hbar c/a ~ 312 GeV ~ 3.6e15 K.
HONEST NOTES printed at run time: the floor value in A is the bath temperature BY CONSTRUCTION
  (fluctuation-dissipation), so A shows the contrast, not a temperature; B is circular because
  u_* is back-computed from the observed 2.725 K and the assumed factor 80.
"""
import numpy as np

SEED = 19

def two_regions(N=400, T0=5.0, T_bath=1.0, gamma=0.5, dt=0.05, t_end=1000.0, seed=SEED):
    rng = np.random.default_rng(seed)
    v0 = rng.normal(0.0, np.sqrt(T0), N); v0 -= v0.mean()
    acc = lambda x: np.roll(x, 1) - 2 * x + np.roll(x, -1)
    out = {}
    for name, bath in (("light-bathed space", True), ("vacuum deficit", False)):
        x = np.zeros(N); v = v0.copy(); a = acc(x)
        nsteps = int(t_end / dt); ts = []; Ts = []
        noise_rng = np.random.default_rng(seed + 1)
        for i in range(nsteps):
            v += 0.5 * dt * a; x += dt * v; a = acc(x); v += 0.5 * dt * a
            # Langevin step (exact OU update of velocities)
            c1 = np.exp(-gamma * dt)
            if bath:
                v = c1 * v + np.sqrt((1 - c1 ** 2) * T_bath) * noise_rng.standard_normal(N)
            else:
                v = c1 * v
            if i % 20 == 0:
                ts.append(i * dt); Ts.append(np.mean(v ** 2))
        ts = np.array(ts); Ts = np.array(Ts)
        out[name] = (ts, Ts, Ts[ts > 200].mean(), Ts[-1])
    return out

def energy_balance():
    sig = 5.670374419e-8; c = 2.99792458e8; hbar = 1.054571817e-34; kB = 1.380649e-23
    a_rad = 4 * sig / c
    T = 2.725; u_cmb = a_rad * T ** 4; u_star = u_cmb / 80.0
    cob = {"Lauer+2022": (16.37, 1.47), "Postman+2024": (11.16, 1.65)}
    band = {k: (4 * np.pi * (I - e) * 1e-9 / c, 4 * np.pi * I * 1e-9 / c, 4 * np.pi * (I + e) * 1e-9 / c)
            for k, (I, e) in cob.items()}
    a_lat = 6.33e-19
    E_grain = hbar * c / a_lat; T_grain = E_grain / kB
    return a_rad, u_cmb, u_star, band, E_grain / 1.602176634e-10, T_grain

if __name__ == "__main__":
    print("=== PART A: light-bathed space vs vacuum deficit (identical dynamics, identical hot start) ===")
    res = two_regions()
    for k, (ts, Ts, Tm, Tf) in res.items():
        print(f"  {k:20s}: <T_kin>(t>200) = {Tm:.4f}   T_kin(t=1000) = {Tf:.3e}")
    fl = res["light-bathed space"][2]; df = res["vacuum deficit"][3]
    print(f"  RESULT: bathed floor {fl:.3f} (> 0, held);  deficit {df:.1e} (-> absolute zero)")
    print("  HONEST: the floor equals T_bath = 1 by fluctuation-dissipation construction; the run")
    print("  shows the CONTRAST (contact vs no contact), it does not produce a temperature value.\n")

    print("=== PART B: Stefan-Boltzmann energy balance ===")
    a_rad, u_cmb, u_star, band, EG, TG = energy_balance()
    print(f"  a = 4 sigma/c = {a_rad:.4e} J m^-3 K^-4")
    print(f"  u_CMB = a (2.725 K)^4 = {u_cmb:.4e} J m^-3")
    print(f"  u_* = u_CMB / 80 = {u_star:.3e} J m^-3   (80 = stated ratio, input)")
    inside = []
    for k, (lo, mid, hi) in band.items():
        ok = lo <= u_star <= hi; inside.append(ok)
        Tfwd = ((80 * np.array([lo, mid, hi]) / a_rad) ** 0.25)
        print(f"  COB {k:12s}: u = {mid:.2e} [{lo:.2e}, {hi:.2e}] J m^-3 -> u_* inside 1-sigma: {ok};"
              f"  forward 80*u_COB -> T = {Tfwd[1]:.2f} K [{Tfwd[0]:.2f}, {Tfwd[2]:.2f}]")
    print(f"  grain: hbar c / a = {EG:.1f} GeV,  hbar c/(a k_B) = {TG:.2e} K;  "
          f"log10(T_grain/2.725 K) = {np.log10(TG/2.725):.1f} orders")
    print("  HONEST: u_* is BACK-COMPUTED from the observed 2.725 K and the assumed factor 80, so the")
    print("  'balance closes' statement is a consistency check, not a derivation; the factor 80 (the")
    print("  lattice's absolute emission rate) is not derived. Absolute 2.725 K remains [O]/anchored.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, os
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.3))
        for k, col in (("light-bathed space", "#C0392B"), ("vacuum deficit", "#2C3E50")):
            ts, Ts, _, _ = res[k]; a1.plot(ts, Ts, color=col, lw=0.8, label=k)
        a1.axhline(1, ls="--", color="#C0392B", lw=0.8, alpha=.6); a1.axhline(0, ls="--", color="gray", lw=0.8)
        a1.set_xlabel("time (lattice units)"); a1.set_ylabel(r"$T_{\rm kin}$"); a1.legend(fontsize=8)
        a1.set_title("A: light keeps space off zero; deficit reaches it")
        T = np.logspace(-0.4, 0.8, 50); a2.loglog(T, a_rad * T ** 4, color="#2C3E50")
        a2.plot(2.725, u_cmb, "o", color="#C0392B"); a2.set_xlabel("T (K)"); a2.set_ylabel(r"$u=aT^4$ (J/m$^3$)")
        a2.set_title("B: Stefan-Boltzmann floor (2.725 K anchored)")
        plt.tight_layout(); p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs", "ch9_cmb_floor.png")
        plt.savefig(p, dpi=110); print(f"  [figure written: {p}]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}]")
