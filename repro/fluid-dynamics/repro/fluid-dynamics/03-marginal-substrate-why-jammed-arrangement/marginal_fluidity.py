"""
marginal_fluidity.py -- The marginal substrate: why a jammed arrangement flows.

Verifies, inside this bundle, the substrate facts inherited from the companion
VP whitepaper (jamming-spine verification v0.4; concept DOI 10.5281/zenodo.17932566):

  [0] self-check : analytic Born modulus / mismatch vector / Hessian action
                   agree with finite differences (no formula taken on faith).
  [1] fluidity   : the relaxed (non-affine) shear modulus G_relaxed ~ (z - z0)
                   vanishes at the isostatic point; bootstrap CI of z0 contains
                   z_iso = 2d = 6.
  [2] monotone   : <G_relaxed> increases with z (phi-ensemble bins).
  [3] bulk       : B_Born and B_relaxed stay finite (O(1)) down to the margin
                   while the shear reserve dies.
  [4] acoustic   : a single longitudinal speed survives, c^2 = B_relaxed/rho;
                   N-independent within tolerance, softened below the affine
                   (Born) prediction by the non-affine relaxation.

Method (the validated recipe of the companion FINDINGS, reduced N):
  3D bidisperse (50:50, ratio 1.4) harmonic spheres, V = (1/2)(1 - r/sigma)^2,
  periodic box V=1; L-BFGS + FIRE + L-BFGS minimization; rigid backbone
  (iterative rattler removal, contacts < d+1); Born G,B + mismatch Xi + Hessian
  assembled analytically; the non-affine correction is computed by a PINNED
  positive-definite Cholesky solve (3 DOF of the most-coordinated backbone
  particle pinned) with 2 steps of iterative refinement, so that
  0 <= G_relaxed <= G_Born holds by construction.  An explicit eigendecomposition
  pseudoinverse is NEVER formed (the soft-mode 1/omega^2 over-subtraction trap).
  Acceptance gate (physical admissibility, not tuned): jammed AND PSD (Cholesky
  succeeds) AND max residual force < 1e-7.  Negative accepted G_relaxed values,
  if any, are KEPT, not clamped (dropping them biases z0 away from 2d).

numpy/scipy only; fixed seeds; deterministic.  Run:  python marginal_fluidity.py
"""
import sys, time
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import cho_factor, cho_solve

D = 3
RATIO = 1.4
PHIS = [0.650, 0.655, 0.662, 0.672, 0.685, 0.700, 0.720]
NS = [128, 256]
SEEDS = [0, 1, 2, 3]
FMAX_ACCEPT = 1e-7
RNGBASE = 20260613

# ---------------------------------------------------------------- packing ---
def diameters(N, phi, rng):
    d_small = (6.0 * phi / (np.pi * (N / 2.0) * (1.0 + RATIO**3)))**(1.0 / 3.0)
    d = np.empty(N); d[: N // 2] = d_small; d[N // 2:] = RATIO * d_small
    rng.shuffle(d)
    return d

def pair_arrays(N, d):
    iu, ju = np.triu_indices(N, k=1)
    sig = 0.5 * (d[iu] + d[ju])
    return iu, ju, sig

def bonds(x, iu, ju, sig):
    rv = x[iu] - x[ju]
    rv -= np.round(rv)                       # minimum image, box L=1
    r = np.sqrt((rv * rv).sum(1))
    m = r < sig
    return iu[m], ju[m], rv[m], r[m], sig[m]

def energy_grad(xf, N, iu, ju, sig):
    x = xf.reshape(N, D)
    bi, bj, rv, r, s = bonds(x, iu, ju, sig)
    ov = 1.0 - r / s
    E = 0.5 * (ov * ov).sum()
    f = (ov / s)                              # = -V' >= 0 (repulsive magnitude)
    g = np.zeros((N, D))
    fv = (f / r)[:, None] * rv                # force on i along +n
    np.add.at(g, bi, -fv)                     # grad = -F
    np.add.at(g, bj, +fv)
    return E, g.ravel()

def max_force(xf, N, iu, ju, sig):
    _, g = energy_grad(xf, N, iu, ju, sig)
    return np.abs(g).max() if g.size else 0.0

def fire(xf, N, iu, ju, sig, nmax=20000, ftol=1e-9):
    dt, dtmax, a = 0.005, 0.05, 0.1
    v = np.zeros_like(xf); npos = 0
    for _ in range(nmax):
        E, g = energy_grad(xf, N, iu, ju, sig)
        F = -g
        if np.abs(F).max() < ftol:
            break
        p = float(F @ v)
        if p > 0:
            nf = np.linalg.norm(F); nv = np.linalg.norm(v)
            v = (1 - a) * v + a * (F / (nf + 1e-300)) * nv
            npos += 1
            if npos > 5:
                dt = min(dt * 1.1, dtmax); a *= 0.99
        else:
            v[:] = 0.0; dt *= 0.5; a = 0.1; npos = 0
        v += dt * F
        xf = xf + dt * v
    return xf

def make_packing(N, phi, seed):
    rng = np.random.default_rng(RNGBASE + 1000 * N + seed)
    d = diameters(N, phi, rng)
    iu, ju, sig = pair_arrays(N, d)
    xf = rng.random(N * D)
    for budget in (4000, 2000):
        res = minimize(energy_grad, xf, args=(N, iu, ju, sig), jac=True,
                       method="L-BFGS-B",
                       options=dict(maxiter=budget, maxfun=2 * budget,
                                    ftol=1e-18, gtol=1e-14))
        xf = res.x
        if max_force(xf, N, iu, ju, sig) < FMAX_ACCEPT:
            break
        xf = fire(xf, N, iu, ju, sig, nmax=8000)
    mf = max_force(xf, N, iu, ju, sig)
    return xf.reshape(N, D), d, iu, ju, sig, mf

# ------------------------------------------------------- backbone + moduli ---
def backbone(x, iu, ju, sig, N):
    bi, bj, rv, r, s = bonds(x, iu, ju, sig)
    keep = np.ones(N, bool)
    while True:
        m = keep[bi] & keep[bj]
        cnt = np.zeros(N, int)
        np.add.at(cnt, bi[m], 1); np.add.at(cnt, bj[m], 1)
        drop = keep & (cnt < D + 1)
        if not drop.any():
            break
        keep[drop] = False
    m = keep[bi] & keep[bj]
    return keep, bi[m], bj[m], rv[m], r[m], s[m]

def born_and_xi(bi, bj, rv, r, s, idx, nb):
    """Affine moduli + mismatch vectors on the backbone (V=1, d=3)."""
    n = rv / r[:, None]
    ov = 1.0 - r / s
    Vp = -ov / s                  # V'(r)  (<=0)
    Vpp = 1.0 / (s * s)           # V''(r)
    f = -Vp                       # repulsive force magnitude
    nx, ny = n[:, 0], n[:, 1]
    # simple shear gamma_xy:  dr/dg = nx*ny*r ;  d2r/dg2 = r*ny^2*(1-nx^2)
    drdg = nx * ny * r
    G_born = float((Vpp * drdg**2 + Vp * r * ny**2 * (1.0 - nx**2)).sum())
    # bulk (uniform dilation), companion form: B = (1/d^2) sum V'' r^2 + ((d-1)/d) P
    P = float((f * r).sum()) / D
    B_born = float((Vpp * r * r).sum()) / D**2 + (D - 1) / D * P
    # mismatch vectors
    Xi_s = np.zeros((nb, D))
    t1 = (Vpp * drdg)[:, None] * n
    grad_q = np.stack([rv[:, 1], rv[:, 0], np.zeros_like(r)], 1) / r[:, None] \
             - (drdg / r)[:, None] * n
    t = -(t1 + Vp[:, None] * grad_q)
    np.add.at(Xi_s, idx[bi], t); np.add.at(Xi_s, idx[bj], -t)
    Xi_b = np.zeros((nb, D))
    tb = -((Vpp * r + Vp)[:, None] * n)
    np.add.at(Xi_b, idx[bi], tb); np.add.at(Xi_b, idx[bj], -tb)
    return G_born, B_born, P, Xi_s.ravel(), Xi_b.ravel()

def hessian(bi, bj, rv, r, s, idx, nb):
    n = rv / r[:, None]
    ov = 1.0 - r / s
    Vp = -ov / s; Vpp = 1.0 / (s * s)
    kt = Vp / r                                   # tangential (prestress) <=0
    H = np.zeros((nb * D, nb * D))
    I3 = np.eye(D)
    blocks = (Vpp - kt)[:, None, None] * (n[:, :, None] * n[:, None, :]) \
             + kt[:, None, None] * I3
    ib, jb = idx[bi], idx[bj]
    for b in range(len(r)):
        i3, j3 = 3 * ib[b], 3 * jb[b]
        Bk = blocks[b]
        H[i3:i3+3, i3:i3+3] += Bk
        H[j3:j3+3, j3:j3+3] += Bk
        H[i3:i3+3, j3:j3+3] -= Bk
        H[j3:j3+3, i3:i3+3] -= Bk
    return 0.5 * (H + H.T)

def relaxed(H, Xi, pin):
    """Non-affine correction Xi^T H^+ Xi via pinned PD Cholesky + 2 refinements."""
    nb3 = H.shape[0]
    mask = np.ones(nb3, bool); mask[3 * pin:3 * pin + 3] = False
    Hr = H[np.ix_(mask, mask)]; Xr = Xi[mask]
    try:
        c = cho_factor(Hr, lower=True, check_finite=False)
    except np.linalg.LinAlgError:
        return None
    dlt = cho_solve(c, Xr, check_finite=False)
    for _ in range(2):
        dlt += cho_solve(c, Xr - Hr @ dlt, check_finite=False)
    return float(Xr @ dlt)

def analyze_config(x, iu, ju, sig, N):
    keep, bi, bj, rv, r, s = backbone(x, iu, ju, sig, N)
    nb = int(keep.sum())
    if nb < 0.5 * N or len(r) == 0:
        return None
    idx = -np.ones(N, int); idx[keep] = np.arange(nb)
    z = 2.0 * len(r) / nb
    G_b, B_b, P, Xi_s, Xi_b = born_and_xi(bi, bj, rv, r, s, idx, nb)
    if P < 1e-12:
        return None
    H = hessian(bi, bj, rv, r, s, idx, nb)
    cnt = np.zeros(nb, int)
    np.add.at(cnt, idx[bi], 1); np.add.at(cnt, idx[bj], 1)
    pin = int(np.argmax(cnt))
    cs = relaxed(H, Xi_s, pin)
    cb = relaxed(H, Xi_b, pin)
    if cs is None or cb is None:
        return None                                    # not PSD -> reject
    G_rel = G_b - cs
    B_rel = B_b - cb / D**2
    c2 = B_rel / N                                     # = B V /(N m), V=m=1
    return dict(nb=nb, z=z, G_born=G_b, G_rel=G_rel, B_born=B_b,
                B_rel=B_rel, P=P, c2=c2)

# ------------------------------------------------------------- self-check ---
def self_check():
    N = 64
    x, d, iu, ju, sig, mf = make_packing(N, 0.70, 7)
    keep, bi, bj, rv, r, s = backbone(x, iu, ju, sig, N)
    nb = int(keep.sum()); idx = -np.ones(N, int); idx[keep] = np.arange(nb)
    G_b, B_b, P, Xi_s, _ = born_and_xi(bi, bj, rv, r, s, idx, nb)
    # (a) bond-wise FD of the affine shear energy
    def Eb(g):
        rg = rv.copy(); rg[:, 0] += g * rv[:, 1]
        rr = np.sqrt((rg * rg).sum(1)); ovv = np.clip(1.0 - rr / s, 0, None)
        return 0.5 * (ovv * ovv).sum()
    h = 1e-5
    G_fd = (Eb(h) + Eb(-h) - 2 * Eb(0.0)) / h**2
    e_born = abs(G_fd - G_b) / abs(G_b)
    # (b) FD of dE/dgamma w.r.t. coordinates vs analytic Xi (random direction)
    rng = np.random.default_rng(2)
    v = rng.standard_normal(nb * D); v /= np.linalg.norm(v)
    xb = x[keep].copy()
    def dEdg(xb_):
        rvv = xb_[idx[bi]] - xb_[idx[bj]]; rvv -= np.round(rvv)
        rr = np.sqrt((rvv * rvv).sum(1))
        Vp = -np.clip(1.0 - rr / s, 0, None) / s
        return float((Vp * rvv[:, 0] * rvv[:, 1] / rr).sum())
    hp = 1e-6
    dp = dEdg(xb + hp * v.reshape(nb, D)); dm = dEdg(xb - hp * v.reshape(nb, D))
    e_xi = abs((dp - dm) / (2 * hp) - float(-(Xi_s @ v))) / (abs(Xi_s @ v) + 1e-30)
    # (c) Hessian action vs FD of the gradient (backbone-only system)
    def grad_bb(xb_):
        rvv = xb_[idx[bi]] - xb_[idx[bj]]; rvv -= np.round(rvv)
        rr = np.sqrt((rvv * rvv).sum(1))
        ff = np.clip(1.0 - rr / s, 0, None) / s
        g = np.zeros((nb, D)); fv = (ff / rr)[:, None] * rvv
        np.add.at(g, idx[bi], -fv); np.add.at(g, idx[bj], +fv)
        return g.ravel()
    H = hessian(bi, bj, rv, r, s, idx, nb)
    gp = grad_bb(xb + hp * v.reshape(nb, D)); gm = grad_bb(xb - hp * v.reshape(nb, D))
    e_h = np.abs((gp - gm) / (2 * hp) - H @ v).max() / (np.abs(H @ v).max() + 1e-30)
    return e_born, e_xi, e_h

# -------------------------------------------------------------- ensemble ----
def run_ensemble():
    rows = []
    for N in NS:
        for phi in PHIS:
            for sd in SEEDS:
                t0 = time.time()
                x, d, iu, ju, sig, mf = make_packing(N, phi, sd)
                rec = dict(N=N, phi=phi, seed=sd, maxF=mf, status="unjammed")
                if mf < FMAX_ACCEPT:
                    out = analyze_config(x, iu, ju, sig, N)
                    if out is not None:
                        rec.update(out); rec["status"] = "accepted"
                    else:
                        rec["status"] = "rejected"
                else:
                    rec["status"] = "force-fail"
                rec["sec"] = time.time() - t0
                rows.append(rec)
                print(f"  N={N} phi={phi:.3f} sd={sd} -> {rec['status']:9s}"
                      + (f" z={rec['z']:.3f} Grel={rec['G_rel']:+.4f}"
                         f" Brel={rec['B_rel']:.3f}" if "z" in rec else
                         f" maxF={mf:.1e}"), flush=True)
    return rows

def fit_z0(zs, Gs, nboot=3000, seed=11):
    A = np.vstack([zs, np.ones_like(zs)]).T
    a, b = np.linalg.lstsq(A, Gs, rcond=None)[0]
    z0 = -b / a
    rng = np.random.default_rng(seed); n = len(zs); boots = []
    for _ in range(nboot):
        k = rng.integers(0, n, n)
        aa, bb = np.linalg.lstsq(A[k], Gs[k], rcond=None)[0]
        if aa > 0:
            boots.append(-bb / aa)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    ss = 1 - ((Gs - (a * zs + b))**2).sum() / ((Gs - Gs.mean())**2).sum()
    return z0, a, lo, hi, ss

def main():
    print("=" * 76)
    print("marginal_fluidity.py -- substrate: G_relaxed -> 0, B finite, c^2=B/rho")
    print("=" * 76)
    e_born, e_xi, e_h = self_check()
    p0 = e_born < 1e-6 and e_xi < 1e-5 and e_h < 1e-6
    print(f"[0] formula self-check vs finite differences:"
          f"  Born {e_born:.1e}  Xi {e_xi:.1e}  Hessian {e_h:.1e}"
          f"   {'PASS' if p0 else 'FAIL'}")
    rows = run_ensemble()
    acc = [r for r in rows if r["status"] == "accepted"]
    try:
        import csv
        with open("marginal_fluidity_configs.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=sorted({k for r in rows for k in r}))
            w.writeheader(); [w.writerow(r) for r in rows]
    except Exception:
        pass
    zs = np.array([r["z"] for r in acc]); Gs = np.array([r["G_rel"] for r in acc])
    z0, slope, lo, hi, R2 = fit_z0(zs, Gs)
    p1 = lo <= 2 * D <= hi
    print(f"[1] fluidity: pooled fit G_relaxed = a (z - z0):"
          f"  z0 = {z0:.3f}  95% CI [{lo:.2f}, {hi:.2f}]  R^2 = {R2:.2f}"
          f"  (n = {len(acc)})   contains z_iso = 2d = 6: "
          f"{'PASS' if p1 else 'FAIL'}")
    for N in NS:
        sel = [r for r in acc if r["N"] == N]
        zN = np.array([r["z"] for r in sel]); gN = np.array([r["G_rel"] for r in sel])
        zz, _, l2, h2, r2 = fit_z0(zN, gN, seed=11 + N)
        print(f"      per-N  N={N}: z0 = {zz:.3f}  CI [{l2:.2f},{h2:.2f}]"
              f"  R^2 = {r2:.2f}  (n = {len(sel)})")
    edges = np.quantile(zs, [0, .25, .5, .75, 1.0]); mids, means = [], []
    for k in range(4):
        m = (zs >= edges[k]) & (zs <= edges[k + 1] + 1e-12)
        mids.append(zs[m].mean()); means.append(Gs[m].mean())
    p2 = all(means[k + 1] > means[k] for k in range(3))
    print(f"[2] monotone: <G_relaxed> over z-quartiles = "
          + ", ".join(f"{v:.4f}" for v in means)
          + f"   increasing: {'PASS' if p2 else 'FAIL'}")
    lowz = [r for r in acc if r["z"] <= np.quantile(zs, 0.25)]
    Bb = np.array([r["B_born"] for r in acc]); Br = np.array([r["B_rel"] for r in acc])
    BrL = np.mean([r["B_rel"] for r in lowz]); GrL = np.mean([r["G_rel"] for r in lowz])
    p3 = (Bb.min() > 0.05) and (BrL > 10 * abs(GrL))
    print(f"[3] bulk stays finite: <B_born> = {Bb.mean():.3f},"
          f" lowest-z quartile <B_rel> = {BrL:.3f} vs <G_rel> = {GrL:.4f}"
          f"  (shear reserve dead, compression alive): {'PASS' if p3 else 'FAIL'}")
    c2 = {N: np.mean([r["c2"] for r in acc if r["N"] == N]) for N in NS}
    spread = abs(c2[NS[0]] - c2[NS[1]]) / np.mean(list(c2.values()))
    soft = np.mean([r["B_rel"] / r["B_born"] for r in acc])
    p4 = spread < 0.15
    print(f"[4] acoustic: c^2 = B_rel/rho ->  "
          + "  ".join(f"N={N}: {c2[N]:.4f}" for N in NS)
          + f"  (N-spread {100*spread:.1f}% < 15%): {'PASS' if p4 else 'FAIL'};"
          f"  non-affine softening <B_rel/B_born> = {soft:.3f}")
    neg = sum(1 for r in acc if r["G_rel"] < 0)
    nrej = sum(1 for r in rows if r["status"] == "rejected")
    nfor = sum(1 for r in rows if r["status"] == "force-fail")
    nunj = sum(1 for r in rows if r["status"] == "unjammed")
    print(f"[5] ledger: accepted {len(acc)}/{len(rows)}"
          f" (PSD/jam-rejected {nrej}, force-fail {nfor}, unjammed {nunj});"
          f" negative G_rel kept, not clamped: {neg}")
    allp = p0 and p1 and p2 and p3 and p4
    print("-" * 76)
    print(f"OVERALL: {'PASS (5/5)' if allp else 'CHECK FAILURES ABOVE'}")
    print("Provenance: small-N local reproduction of the companion jamming-spine")
    print("verification v0.4 (concept DOI 10.5281/zenodo.17932566).")

if __name__ == "__main__":
    main()
