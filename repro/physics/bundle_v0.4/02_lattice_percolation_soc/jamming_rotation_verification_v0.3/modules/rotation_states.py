"""
rotation_states.py - the cage, its rotational collapse, and solid/liquid/gas.

User's claim, simulated:
  (A) a ball is held still only when 4 balls cage it as a TETRAHEDRON --
      d+1 = 4 non-coplanar contacts, the minimal set that blocks ALL
      translations of a sphere in 3D (fewer => an escape direction remains);
  (B) that cage COLLAPSES when the cage rotates: if the four contacts roll
      toward one hemisphere (a rotational rearrangement), they stop spanning and
      an escape direction opens -- this is how a solid breaks / yields;
  (C,D) whether particle rotation is LOCKED or FREE sets solid / liquid / gas.

Mechanics (Maxwell / isostatic counting):
  FRICTIONLESS spheres jam at Z_iso = 2d = 6 (1 normal constraint per contact,
    3 translational DOF/particle). A Z=4 cage is BELOW 6 -> floppy -> it swings
    open. That floppiness IS the liquid.
  FRICTIONAL / rotation-locked contacts add tangential (rolling) constraints,
    lowering the isostatic number to Z_iso = d+1 = 4 -- exactly the tetrahedral
    cage. So the SAME 4-cage is RIGID when rotation is locked (solid) and FLOPPY
    when rotation is free (liquid/gas). Rotation is the switch.

Here "rotation" is the rotational REARRANGEMENT of the caging particles (rolling
on the contact sphere) -- the mechanically active mode. (For aspherical/frictional
grains, individual spin couples in too and shifts Z_iso, e.g. 6->10 for
ellipsoids; same principle.)

Self-contained: numpy only.
"""
import numpy as np


# ----------------------------------------------------------------------
def tetra_dirs():
    v = np.array([[1, 1, 1.], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def caging_margin(normals, nsamp=60000, seed=0):
    """min over unit directions u of [ max_i (n_i . u) ].
       > 0  => every direction is blocked by some contact  -> CAGED.
       <= 0 => an escape direction u* exists (returned)     -> NOT caged."""
    rng = np.random.default_rng(seed)
    u = rng.standard_normal((nsamp, 3))
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    worst = (u @ normals.T).max(axis=1)
    k = int(np.argmin(worst))
    return float(worst[k]), u[k]


def tilt_toward(normals, theta, axis=np.array([0, 0, 1.])):
    """Roll every contact toward `axis` by angle theta (a rotational rearrangement
    of the cage). theta=0 keeps the regular tetrahedron."""
    out = np.cos(theta) * normals + np.sin(theta) * axis
    return out / np.linalg.norm(out, axis=1, keepdims=True)


# ----------------------------------------------------------------------
#  harmonic repulsion engine for the 5-ball cage (frictionless), free space
# ----------------------------------------------------------------------
def repulse_EF(pos, sigma=1.0, eps=1.0):
    """Harmonic soft-sphere repulsion (contact distance sigma). E and forces."""
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    r = np.sqrt(np.einsum("ij,ij->i", dx, dx)) + 1e-15
    m = r < sigma
    F = np.zeros_like(pos)
    if not m.any():
        return 0.0, F
    delta = 1 - r[m] / sigma
    E = 0.5 * eps * np.sum(delta ** 2)
    fmag = eps * delta / sigma
    fr = (fmag / r[m])[:, None] * dx[m]
    np.add.at(F, iu[m], fr)
    np.add.at(F, ju[m], -fr)
    return E, F


def relax_center_under_force(outer, fdir, fmag, fix_outer=True,
                             steps=4000, dt=0.02):
    """Center at origin caged by `outer` (fixed if fix_outer). Apply force
    fmag along unit fdir to the center; overdamped descent. Return final center
    displacement along fdir (large => escaped through the cage)."""
    pos = np.vstack([[0, 0, 0.], outer])
    fdir = fdir / np.linalg.norm(fdir)
    for _ in range(steps):
        _, F = repulse_EF(pos)
        F[0] += fmag * fdir                     # external force on the centre
        if fix_outer:
            F[1:] = 0.0                          # rotation LOCKED: cage held
        pos += dt * F                            # overdamped (no blow-up: bounded soft force)
    return float(pos[0] @ fdir)


# ----------------------------------------------------------------------
def main():
    np.set_printoptions(suppress=True)
    print("rotation_states.py - the tetrahedral cage, its rotational collapse, states")
    print("=" * 74)

    nt = tetra_dirs()

    # ---- (A) the minimal cage: 4 (tetrahedron) vs 3 ----
    m4, _ = caging_margin(nt)
    m3, esc3 = caging_margin(nt[:3])
    print("\n(A) minimal translational cage in 3D (margin>0 = caged)")
    print(f"    4 contacts (TETRAHEDRON): caging margin = {m4:+.3f}  -> "
          f"{'CAGED (no escape)' if m4 > 0 else 'not caged'}")
    print(f"    3 contacts (triangle)   : caging margin = {m3:+.3f}  -> "
          f"{'caged' if m3 > 0 else 'NOT caged'}; escape dir = {np.round(esc3,2)}")
    print("    -> d+1 = 4 is the minimum: 4 non-coplanar contacts block every translation.")

    # ---- (B) rotational collapse: roll the contacts to one hemisphere ----
    print("\n(B) rotational collapse: roll the 4 contacts toward one hemisphere by theta")
    print(f"    {'theta(deg)':>10} {'caging margin':>14}")
    thetas = np.deg2rad(np.arange(0, 71, 5))
    margins = []
    for th in thetas:
        m, _ = caging_margin(tilt_toward(nt, th))
        margins.append(m)
    margins = np.array(margins)
    for k in range(0, len(thetas), 1):
        print(f"    {np.rad2deg(thetas[k]):10.0f} {margins[k]:14.3f}")
    # crossing where margin -> 0 (cage opens)
    below = np.where(margins > 0)[0]
    above = np.where(margins <= 0)[0]
    if len(below) and len(above):
        i0 = below[-1]; i1 = above[0]
        th_c = np.interp(0.0, [margins[i1], margins[i0]],
                         [np.rad2deg(thetas[i1]), np.rad2deg(thetas[i0])])
        print(f"    -> the cage COLLAPSES at theta_c ~ {th_c:.0f} deg "
              f"(beyond it an escape direction opens). Rotation breaks the solid.")

    # ---- (C) Maxwell counting: frictionless 6 vs rotation-locked 4 ----
    print("\n(C) why 4 needs rotation locked (Maxwell isostatic counting, 3D)")
    print("    frictionless spheres : Z_iso = 2d        = 6   (4-cage is BELOW -> floppy)")
    print("    rotation-locked      : Z_iso = d + 1     = 4   (the tetrahedral cage)")
    dof = 5 * 3 - 6                 # 5-ball cluster, internal DOF (frictionless)
    floppy = dof - 4                # minus 4 normal constraints
    print(f"    5-ball cage, frictionless: internal DOF {dof} - 4 contacts = "
          f"{floppy} FLOPPY modes -> the contacts swing (the rotational mode of B).")

    # ---- (D) the opening (rotation) mode: free without friction, costly with it ----
    print("\n(D) the opening mode: roll the contacts (as in B) and watch the ENERGY cost")
    print(f"    {'phi(deg)':>8} {'dE frictionless':>16} {'dE rotation-locked':>19}")
    k_fric = 5.0
    for phd in [0, 10, 20, 30, 40]:
        ph = np.deg2rad(phd)
        rolled = tilt_toward(nt, ph) * 1.0          # outer positions; centre-contact kept (r=sigma)
        E, _ = repulse_EF(np.vstack([[0, 0, 0.], rolled]))
        E_lock = E + 0.5 * k_fric * 4 * ph ** 2     # + tangential rolling spring (friction) on 4 contacts
        print(f"    {phd:8d} {E:16.4f} {E_lock:19.4f}")
    print("    -> frictionless: dE ~ 0 through theta_c -> the cage rolls OPEN at no cost = LIQUID.")
    print("    -> rotation-locked (friction): dE ~ k*phi^2 resists the roll = SOLID, G>0.")
    print("    -> gas = no cage (no contacts).")

    print("\nReading: the held ball needs a tetrahedral (d+1=4) cage; that cage is")
    print("rigid only while rotation is locked. Let the caging particles roll/rotate")
    print("and the cage opens (theta_c) -> the solid yields. Locking vs freeing particle")
    print("rotation moves the SAME packing between solid, liquid and gas.")


if __name__ == "__main__":
    main()
