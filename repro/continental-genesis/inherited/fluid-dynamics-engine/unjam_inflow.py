"""
unjam_inflow.py -- rotation unjams the margin; the forced radius is an attractor.

Local demonstrations for the substrate section and for Mechanism M, Step 0,
inherited from the companion VP whitepaper (concept DOI 10.5281/zenodo.17932566):

  [1] rigid rotation is free : under a rigid rotation field u = theta z_hat x r
      every bond extension vanishes identically (first order) -- rotation per se
      costs the packing nothing.
  [2] zero shear reserve     : what a *differential* rotation (shear) must spend
      is the contact-breaking strain gamma* = min_b ov_b/(n_x n_y r)_b, and
      gamma* -> 0 toward the margin (the reserve IS the vanishing overlap).
      Hence at the isostatic point ANY rotational shear breaks contacts and
      unjams: rotation is the fluidization switch, and the directed inflow of
      the companion's Section 8.5.0 has a geometric, not postulated, origin.
  [3] forced-radius attractor: the inherited stiffness-vs-inflow balance
      dx/dt = alpha x^-5 - x^-4 has the unique fixed point x* = alpha with
      F'(x*) = -alpha^-5 = -(pi/2)^5 < 0, and every positive initial radius
      converges to it (global stability).  alpha = 2/pi enters here as an
      inherited constant of the companion (its derivation is NOT reproduced or
      claimed in this bundle); only the attractor structure is verified.

numpy/scipy only; fixed seeds; deterministic.  Run:  python unjam_inflow.py
(Imports the packing generator from marginal_fluidity.py in this directory.)
"""
import numpy as np
from marginal_fluidity import make_packing, backbone, FMAX_ACCEPT, D

PHIS = [0.652, 0.660, 0.672, 0.690, 0.720]
SEEDS = [0, 1, 2]
NLOC = 128

def per_packing(phi, seed):
    x, d, iu, ju, sig, mf = make_packing(NLOC, phi, seed)
    if mf >= FMAX_ACCEPT:
        return None
    keep, bi, bj, rv, r, s = backbone(x, iu, ju, sig, NLOC)
    if keep.sum() < 0.5 * NLOC or len(r) == 0:
        return None
    ov = 1.0 - r / s
    P = float(((ov / s) * r).sum()) / D                  # virial pressure
    n = rv / r[:, None]
    # [1] rigid rotation: delta r per unit theta = n . (z_hat x r_vec) == 0
    zxr = np.stack([-rv[:, 1], rv[:, 0], np.zeros_like(r)], 1)
    rigid = float(np.abs((n * zxr).sum(1)).max())
    # [2] shear reserve: first contact break under simple shear gamma_xy
    drdg = n[:, 0] * n[:, 1] * r                          # dr/dgamma
    ext = drdg > 1e-12                                    # extending bonds
    gb = ov[ext] * s[ext] / drdg[ext]                     # per-bond break strain
    return dict(phi=phi, seed=seed, z=2.0 * len(r) / keep.sum(), P=P,
                gmin=float(gb.min()), g05=float(np.quantile(gb, 0.05)),
                gmed=float(np.median(gb)), rigid=rigid,
                ovmed=float(np.median(ov * s)))

def attractor():
    alpha = 2.0 / np.pi
    F = lambda x: alpha * x**-5 - x**-4
    ends = []
    for x0 in (0.2, 0.5, 1.0, 2.0, 5.0):
        x, t, dt = x0, 0.0, 1e-4
        for _ in range(4_000_000):
            k1 = F(x); k2 = F(x + 0.5 * dt * k1)
            k3 = F(x + 0.5 * dt * k2); k4 = F(x + dt * k3)
            x += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            dt = min(2e-2, dt * 1.001)
            if abs(F(x)) < 1e-14:
                break
        ends.append(x)
    ends = np.array(ends)
    Fp = -5 * alpha * alpha**-6 + 4 * alpha**-5           # F'(x*) = -alpha^-5
    return ends, alpha, Fp

def main():
    print("=" * 76)
    print("unjam_inflow.py -- rotation unjams the margin; forced radius attractor")
    print("=" * 76)
    rows = []
    for phi in PHIS:
        for sd in SEEDS:
            r = per_packing(phi, sd)
            if r:
                rows.append(r)
                print(f"  phi={phi:.3f} sd={sd}: z={r['z']:.3f}  P={r['P']:.3e}"
                      f"  gamma*_min={r['gmin']:.2e}  q05={r['g05']:.2e}"
                      f"  med={r['gmed']:.2e}  rigid-ext={r['rigid']:.0e}",
                      flush=True)
    rigid_max = max(r["rigid"] for r in rows)
    p1 = rigid_max < 1e-12
    print(f"[1] rigid rotation is free: max bond extension per unit theta"
          f" = {rigid_max:.1e}  (== 0 to machine precision): "
          f"{'PASS' if p1 else 'FAIL'}")
    P = np.array([r["P"] for r in rows])
    G5 = np.array([r["g05"] for r in rows]); Gm = np.array([r["gmed"] for r in rows])
    k = np.argsort(P); lo = G5[k[:5]].mean(); hi = G5[k[-5:]].mean()
    c5 = float(np.corrcoef(np.log(P), np.log(G5))[0, 1])
    cm = float(np.corrcoef(np.log(P), np.log(Gm))[0, 1])
    p2 = (hi / lo > 3.0) and (c5 > 0.9) and (cm > 0.9)
    print(f"[2] zero shear reserve (distribution level): the contact-breaking"
          f" strain falls with pressure --")
    print(f"    q05: lowest-P 5 = {lo:.3e} vs highest-P 5 = {hi:.3e}"
          f" (ratio {hi/lo:.1f}x); corr(log q05, log P) = {c5:.2f},"
          f" corr(log med, log P) = {cm:.2f}: {'PASS' if p2 else 'FAIL'}")
    print("    (The very first break, gamma*_min, is an extreme-value statistic"
          " and is reported per packing")
    print("    above for honesty; the physical reserve is the overlap"
          " *distribution*, which vanishes at the")
    print("    margin: as P -> 0 any rotational shear exceeds it --"
          " rotation unjams, and real unjamming is")
    print("    an avalanche of such breaks, not a single bond.)")
    ends, alpha, Fp = attractor()
    p3 = np.all(np.abs(ends - alpha) < 1e-7) and abs(Fp + (np.pi / 2)**5) < 1e-12
    print(f"[3] forced-radius attractor dx/dt = a x^-5 - x^-4 (a = 2/pi,"
          f" inherited constant):")
    print(f"    from x0 in {{0.2,0.5,1,2,5}} all converge to x* = {alpha:.6f};"
          f" max |x-x*| = {np.abs(ends-alpha).max():.1e}")
    print(f"    F'(x*) = -a^-5 = {Fp:.4f}  (= -(pi/2)^5 = {-(np.pi/2)**5:.4f})"
          f" < 0, unique positive root: {'PASS' if p3 else 'FAIL'}")
    print("-" * 76)
    print(f"OVERALL: {'PASS (3/3)' if (p1 and p2 and p3) else 'CHECK ABOVE'}")
    print("Provenance: Step-0/attractor structure inherited from the companion")
    print("whitepaper (concept DOI 10.5281/zenodo.17932566); alpha = 2/pi is an")
    print("inherited constant, not derived or fitted here.")

if __name__ == "__main__":
    main()
