#!/usr/bin/env python3
"""
ch8_bullet_offset.py  --  Chapter 8: size of the Bullet-Cluster lensing-gas offset (physical units).

Re-implementation (2026-09-28) of a script cited on the site but lost. The toy transport model
(legacy_v2_3/ch8_bullet.py) set the MECHANISM in normalised units; this script computes the
MAGNITUDE from ram-pressure stripping. numpy only.

CLAIM ON THE PAGES
------------------
  08-dark-matter-vacuum-deficit: "a_ram = rho_ICM v^2 / Sigma_gas ... For a physical cool-core
     density (n_e ~ 0.01 cm^-3), a collision speed v ~ 4700 km/s and a bullet gas column
     Sigma ~ 0.3 kg m^-2, the lensing-gas offset is ~ 0.41 Mpc, spanning the observed 0.2-0.6 Mpc
     band across the physical density range n_e ~ 0.002-0.024 cm^-3."
  axh / axj / 16-open-problems: "Bullet offset 0.2-0.6 Mpc (ch8_bullet_offset.py; ICM params)".
  NOTE: the page does not state the path length / time over which the offset is integrated,
  nor the source of the "observed 0.2-0.6 Mpc band"; 08-colliding-clusters-bullet-offset itself
  quotes "the observed 0.2 Mpc offset".

MODEL
  Collisionless component (galaxies + deficit, carries the lensing mass) moves ballistically at v0.
  Bullet gas (column Sigma) is decelerated by ram pressure of the main-cluster ICM at rest:
      dv_gas/dt = - rho_ICM(x_gas) * v_gas^2 / Sigma,   rho_ICM = mu_e m_p n_e(x)
  Offset = x_coll - x_gas at the end. Gravity (same potential for both), gas pressure re-expansion,
  stripping/mass loss, projection and the main cluster's own motion are all neglected.
  Uniform medium closed form: offset = v0 t - (Sigma/rho) ln(1 + rho v0 t / Sigma).

INPUTS -- EVERY ONE IS CHOSEN BY HAND (none is derived in the VP framework, none is fitted here):
  [HAND] n_e      = 0.01 cm^-3, range 0.002-0.024 cm^-3   (page; "cool-core" value)
  [HAND] v0       = 4700 km/s   (page; the shock-front speed of 1E0657-56, Markevitch 2006;
                                 the subcluster itself is argued to be slower, ~2700-3000 km/s,
                                 Springel & Farrar 2007 -- scanned below)
  [HAND] Sigma    = 0.3 kg m^-2 (page; bullet gas column, not sourced on the page)
  [HAND] mu_e     = 1.17        (electrons per proton mass, fully ionised H+He, X=0.7)
  [HAND] geometry / path: NOT given on the page. Two choices shown, neither tuned:
      (i)  uniform medium over a collisionless path L = 0.72 Mpc (the observed separation of the
           bullet mass peak from the main-cluster centre, Clowe et al. 2006) -> t = L/v0;
      (ii) beta-model main cluster n_e(r) = n_e0 [1+(r/r_c)^2]^(-3 beta/2), r_c = 0.25 Mpc,
           beta = 0.7 [HAND, typical], bullet path from x = -1.0 Mpc to +0.72 Mpc through the centre.
  Constants: m_p, Mpc, Gyr (CODATA / IAU).

ALGORITHM
  (i) closed form; (ii) explicit integration in x with dt = 1e-4 of the crossing time (RK2).
  Scan n_e over the page range and v0 over {3000, 4700} km/s.

EXPECTED OUTPUT (page): ~0.41 Mpc at n_e = 0.01; 0.2-0.6 Mpc over n_e = 0.002-0.024.

DETERMINISM: no RNG. Runtime < 5 s. DEPENDENCIES: numpy (matplotlib optional).
"""
import os
import numpy as np

M_P = 1.67262192e-27
MPC = 3.0856775814913673e22
GYR = 3.15576e16
MU_E = 1.17
HERE = os.path.dirname(os.path.abspath(__file__))

NE0, V0, SIG = 0.01, 4700.0, 0.3        # [HAND] page values
L_OBS = 0.72                            # [HAND] Mpc, Clowe et al. 2006 separation
RC, BETA, X_IN = 0.25, 0.7, -1.0        # [HAND] beta-model and entry point


def rho(ne_cm3):
    return MU_E * M_P * ne_cm3 * 1e6


def offset_uniform(ne, v0_kms, Sigma, L_mpc):
    r = rho(ne); v0 = v0_kms * 1e3; t = L_mpc * MPC / v0
    lam = Sigma / r
    return (v0 * t - lam * np.log1p(v0 * t / lam)) / MPC, lam / MPC, t / GYR


def offset_beta(ne0, v0_kms, Sigma, x_in=X_IN, x_out=L_OBS, rc=RC, beta=BETA, nstep=20000):
    v0 = v0_kms * 1e3
    T = (x_out - x_in) * MPC / v0
    dt = T / nstep
    xg, vg = x_in * MPC, v0

    def acc(x, v):
        ne = ne0 * (1 + (x / (rc * MPC)) ** 2) ** (-1.5 * beta)
        return -rho(ne) * v * v / Sigma

    for _ in range(nstep):
        a1 = acc(xg, vg)
        vh, xh = vg + 0.5 * dt * a1, xg + 0.5 * dt * vg
        a2 = acc(xh, vh)
        xg += dt * vh
        vg += dt * a2
    return (x_out * MPC - xg) / MPC, vg / 1e3


if __name__ == "__main__":
    print("=== ch8_bullet_offset.py : ram-pressure lensing-gas offset, physical units ===")
    print("Hand-chosen inputs: n_e, v0, Sigma, mu_e, path length/geometry (see docstring).")
    print(f"  rho_ICM(n_e=0.01) = {rho(0.01):.3e} kg/m^3; stopping column length Sigma/rho = "
          f"{SIG/rho(0.01)/MPC:.3f} Mpc")

    print("\n--- (i) uniform medium, collisionless path L = 0.72 Mpc ---")
    print("   n_e[cm^-3]   v0=4700: offset[Mpc]  (t[Gyr])   v0=3000: offset[Mpc]")
    for ne in (0.002, 0.005, 0.01, 0.015, 0.024):
        o47, lam, t47 = offset_uniform(ne, 4700, SIG, L_OBS)
        o30, _, _ = offset_uniform(ne, 3000, SIG, L_OBS)
        print(f"     {ne:6.3f}         {o47:6.3f}          ({t47:.3f})        {o30:6.3f}")
    o_ref = offset_uniform(NE0, V0, SIG, L_OBS)[0]

    print("\n--- (ii) beta-model main cluster (r_c=0.25 Mpc, beta=0.7), path -1.0 -> +0.72 Mpc ---")
    print("   n_e0[cm^-3]  v0=4700: offset[Mpc] (v_gas,end km/s)   v0=3000: offset[Mpc]")
    rows = []
    for ne in (0.002, 0.005, 0.01, 0.015, 0.024):
        o47, vend = offset_beta(ne, 4700, SIG)
        o30, _ = offset_beta(ne, 3000, SIG)
        rows.append((ne, o47))
        print(f"     {ne:6.3f}          {o47:6.3f}   ({vend:6.0f})              {o30:6.3f}")
    ob_ref = offset_beta(NE0, V0, SIG)[0]

    print("\n--- (iii) sensitivity at n_e = 0.01, v0 = 4700 (uniform, L = 0.72 Mpc) ---")
    for S in (0.15, 0.3, 0.6):
        print(f"   Sigma = {S:4.2f} kg/m^2 -> offset {offset_uniform(NE0, V0, S, L_OBS)[0]:.3f} Mpc")
    for L in (0.4, 0.72, 1.0, 1.5):
        print(f"   path L = {L:4.2f} Mpc   -> offset {offset_uniform(NE0, V0, SIG, L)[0]:.3f} Mpc")

    lo, hi = 0.1, 5.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if offset_uniform(NE0, V0, SIG, mid)[0] < 0.41 else (lo, mid)
    print(f"   (diagnostic, not used: a uniform path of L = {0.5*(lo+hi):.2f} Mpc would be needed for the")
    print("    page's 0.41 Mpc at n_e=0.01, Sigma=0.3; the page does not state any path.)")
    print("   At fixed path the uniform-medium offset is independent of v0 (both depend only on")
    print("   L and Sigma/rho); v0 enters only if the elapsed time, not the path, is fixed.")

    print("\nRESULT")
    print(f"  page reference inputs (n_e=0.01, v=4700, Sigma=0.3): offset = {o_ref:.3f} Mpc (uniform, L=0.72)")
    print(f"                                                        offset = {ob_ref:.3f} Mpc (beta model)")
    print("  The page's 0.41 Mpc is NOT reproduced by either explicit geometry (0.28 / 0.50 Mpc); the page")
    print("  omits the path length, and the offset is set by that path and by Sigma/rho (table iii).")
    print("  ORDER of magnitude (0.1-0.7 Mpc over n_e = 0.002-0.024) is reproduced; the specific")
    print("  0.2-0.6 Mpc band over that n_e range is not (uniform: 0.09-0.41; beta: 0.16-0.70). The band")
    print("  is a consequence of hand-chosen inputs, not a derived number.")
    print("  DEGENERACY: this magnitude is pure gas physics. It is identical for particle dark matter,")
    print("  a VP deficit, or galaxies alone -- it does not test the deficit picture. The full chi^2")
    print("  against real lensing + X-ray maps is still not run [O].")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ne = np.linspace(0.002, 0.024, 60)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(ne, [offset_uniform(n, 4700, SIG, L_OBS)[0] for n in ne], label="uniform, L=0.72 Mpc, 4700 km/s")
        ax.plot(ne, [offset_uniform(n, 3000, SIG, L_OBS)[0] for n in ne], "--", label="uniform, 3000 km/s")
        ax.plot([r[0] for r in rows], [r[1] for r in rows], "o-", label="beta model, 4700 km/s")
        ax.axhspan(0.2, 0.6, color="0.85", label="page band 0.2-0.6 Mpc")
        ax.set_xlabel("n_e [cm^-3]"); ax.set_ylabel("lensing-gas offset [Mpc]"); ax.legend(fontsize=8)
        plt.tight_layout(); plt.savefig(os.path.join(HERE, "ch8_bullet_offset.png"), dpi=110)
        print("  [figure written: ch8_bullet_offset.png]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}] numbers above are the result.")
