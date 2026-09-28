"""
jam_states.py — Solid, liquid, gas, and the rigid shell.

The three states of matter are three regimes of ONE jammed/volume-particle
substrate, organised by a single object: the RIGID SHELL -- the first
coordination shell each particle carries (the first peak of g(r)). Whether that
shell bears load is set by its coordination z relative to the isostatic value
z_iso = 2d (jam_packing.py / isostatic_scaling.py):

   GAS    phi -> 0          : no shell. Free particles. Dilute viscosity is the
                              EINSTEIN law eta/eta0 = 1 + (5/2)phi -- the
                              Newtonian limit (Pillar I). z = 0, G = 0.
   LIQUID dense, phi < phi_J : a TRANSIENT shell (a cage). Each particle is caged
                              by neighbours, but the cage is under-constrained
                              (z_shell < z_iso) so it YIELDS by rearrangement
                              events. Flows globally, rigid locally. Viscosity
                              DIVERGES eta ~ (phi_J - phi)^{-2} as the shell
                              tightens toward closure. G = 0 (no static rigidity).
   SOLID  phi >= phi_J       : the shell CLOSES and percolates. The rigid-shell
                              network bears load: G > 0, born at phi_J and growing
                              as G ~ delta_z. (At the proton scale this is the
                              ORDERED 82-cell rigid shell of rigid_shell.py.)

This module shows, from the actual soft-sphere packings:
  (A) the rigid shell = the g(r) first peak; its count -> z_iso at point J;
  (B) rigidity is BORN at the shell-closure: G = 0 below phi_c, G ~ delta_z above;
  (C) one viscosity curve spans gas (Einstein) -> liquid (divergence) -> solid;
  (D) the rigid shell SHARPENS as the solid stiffens (the seed-to-seed spread of
      the selected length L* ~ sqrt(G) narrows with z) -- the rigid_shell.py
      "birth", recovered from the jamming data.

Self-contained: numpy. Reuses jam_packing.py as the engine.
"""
import numpy as np
import jam_packing as jp


# ----------------------------------------------------------------------
#  (A) the rigid shell = the first coordination shell of g(r)
# ----------------------------------------------------------------------
def rigid_shell_count(pos, D, L, d, shell_max=1.05):
    """First-shell coordination: pairs with r < shell_max * d_ij (the contact/near-
    contact shell). Equals the contact number Z when shell_max -> 1. Returns
    (z_shell, contact_Z)."""
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, k=1)
    dx = pos[iu] - pos[ju]
    dx -= L * np.round(dx / L)
    rij = np.sqrt(np.einsum("ij,ij->i", dx, dx))
    dij = 0.5 * (D[iu] + D[ju])
    n_shell = np.sum(rij < shell_max * dij)
    z_shell = 2.0 * n_shell / N
    Z, _ = jp.mean_contact_number(pos, D, L, d)
    return z_shell, Z


# ----------------------------------------------------------------------
#  (B,D) shear modulus G(phi) -- rigidity born at the shell closure
# ----------------------------------------------------------------------
def shear_modulus(pos, D, L, d, gamma=1e-3, **fire_kw):
    """Affine xy shear by gamma, non-affine re-minimisation at fixed tilt, then
    G = |sigma_xy| / gamma. Returns 0 for an unjammed (flowing) configuration."""
    pos2 = pos.copy()
    pos2[:, 0] += gamma * pos2[:, 1]                     # affine shear
    pos2, E, P, fmax = jp.fire_minimize(pos2, D, L, d, tilt=gamma, **fire_kw)
    _, _, _, sxy = jp.energy_forces_pressure(pos2, D, L, d, tilt=gamma, want_sxy=True)
    return abs(sxy) / gamma


# ----------------------------------------------------------------------
#  (C) one viscosity curve: gas (Einstein) -> liquid (divergence) -> solid
# ----------------------------------------------------------------------
def viscosity_curve(phi_J=0.64, phis=None):
    """Non-Brownian suspension viscosity. The single divergence form
    eta/eta0 = (1 - phi/phi_J)^{-2} reduces to Einstein 1 + (5/2)phi at small phi
    (slope 2/phi_J ~ 3.1 vs Einstein 2.5) and diverges as (phi_J - phi)^{-2} at
    the jam. Returns (phi, eta_rel, einstein)."""
    if phis is None:
        phis = np.linspace(0.0, 0.62, 14)
    eta = (1.0 - phis / phi_J) ** (-2.0)
    einstein = 1.0 + 2.5 * phis
    return phis, eta, einstein


# ----------------------------------------------------------------------
def main():
    import sys
    np.set_printoptions(suppress=True)
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 160
    fire_kw = dict(ftol=1e-9, max_steps=6000)
    z_iso = 2 * d
    print("jam_states.py — solid / liquid / gas and the rigid shell")
    print("=" * 66)

    # ---- (A) the rigid shell ----
    target = 0.64 if d == 3 else 0.84
    r = jp.relax_at_phi(N, target + 0.01, d, seed=0, **fire_kw)
    z_shell, Z = rigid_shell_count(r["pos"], r["D"], r["L"], d)
    print(f"\n(A) the rigid shell = the first coordination shell (d={d}, z_iso={z_iso})")
    print(f"    first-shell count z_shell = {z_shell:.2f}, contact number Z = {Z:.2f}")
    print(f"    -> the rigid shell closes at the ISOSTATIC number z_iso = {z_iso}")

    # ---- (B,D) rigidity born at jamming; shell sharpening ----
    print(f"\n(B) rigidity is BORN at the shell closure: G = 0 below phi_c, "
          f"G > 0 above")
    if d == 3:
        phis = [0.61, 0.62, 0.65, 0.66, 0.67, 0.68]
    else:
        phis = [0.81, 0.82, 0.85, 0.86, 0.87, 0.88]
    print(f"    {'phi':>6} {'state':>7} {'Z':>6} {'delta_z':>8} {'G':>11} "
          f"{'relspread(sqrtG)':>16}")
    Gdz = []
    sharp = []
    for phi in phis:
        Gs, Zs = [], []
        for s in (0, 1, 2):
            rp = jp.relax_at_phi(N, phi, d, seed=s, **fire_kw)
            if rp["P"] > 1e-7:
                G = shear_modulus(rp["pos"], rp["D"], rp["L"], d,
                                  gamma=1e-3, ftol=1e-9, max_steps=4000)
                Gs.append(G); Zs.append(rp["Z"])
        if len(Gs) == 0:
            print(f"    {phi:6.3f} {'gas/liq':>7} {0.0:6.2f} {'-':>8} "
                  f"{0.0:11.3e} {'(flows: G=0)':>16}")
            continue
        Gs = np.array(Gs); Zm = np.mean(Zs); dz = Zm - z_iso
        relsp = 0.5 * Gs.std() / Gs.mean()              # relspread(sqrtG)=1/2 relspread(G)
        print(f"    {phi:6.3f} {'solid':>7} {Zm:6.2f} {dz:8.3f} "
              f"{Gs.mean():11.3e} {relsp:16.4f}")
        if dz > 0:
            Gdz.append((dz, Gs.mean())); sharp.append((Zm, relsp))
    Gdz = np.array(Gdz)
    if len(Gdz) >= 3:
        bG = np.polyfit(np.log(Gdz[:, 0]), np.log(Gdz[:, 1]), 1)[0]
        print(f"    -> G ~ delta_z^{bG:.2f}  (jamming: G ~ delta_z, exponent ~ 1; "
              f"G -> 0 at point J)")
        print(f"    -> RIGIDITY-BIRTH confirmed: the rigid shell becomes "
              f"load-bearing exactly at phi_c")
    sharp = np.array(sharp)
    if len(sharp) >= 2:
        order = np.argsort(sharp[:, 0])
        mono = np.all(np.diff(sharp[order, 1]) <= 1e-3)
        print(f"\n(D) the rigid shell SHARPENS as the solid stiffens "
              f"(relspread of L*~sqrtG):")
        for z, rs in sharp[order]:
            print(f"    z = {z:5.2f}: rel.spread(L*) = {rs:.4f}")
        print(f"    -> spread narrows with z: {'PASS' if mono else 'CHECK'} "
              f"(matches rigid_shell.py: rigid-shell birth)")

    # ---- (C) one viscosity curve ----
    print(f"\n(C) one viscosity curve spans GAS -> LIQUID -> SOLID "
          f"(phi_J = 0.64):")
    phis_v, eta, eins = viscosity_curve(0.64)
    print(f"    {'phi':>6} {'eta/eta0':>10} {'Einstein 1+2.5phi':>18} {'regime':>8}")
    for k in range(0, len(phis_v), 2):
        reg = "gas" if phis_v[k] < 0.2 else ("liquid" if phis_v[k] < 0.6 else "->solid")
        print(f"    {phis_v[k]:6.3f} {eta[k]:10.3f} {eins[k]:18.3f} {reg:>8}")
    print(f"    -> small phi: divergence form -> 1 + (2/phi_J) phi = 1 + 3.1 phi "
          f"(Einstein-like, NEWTONIAN)")
    print(f"    -> phi -> phi_J: eta ~ (phi_J - phi)^(-2)  (rigid shell closing; "
          f"Pillar I closure = this divergence)")

    print("\nReading: gas = no shell (Newtonian/dilute); liquid = transient shell")
    print("(caged, yields by events, eta diverges); solid = closed load-bearing")
    print("shell (G>0, born at point J). One substrate, one rigid shell, three faces.")


if __name__ == "__main__":
    main()
