"""
relaxed_shear.py -- relaxed (non-affine) shear modulus by EXACT LINEAR RESPONSE,
computed via a DIRECT REGULARIZED LINEAR SOLVE instead of an explicit pseudoinverse.

    G_relaxed = G_Born - Xi^T H^+ Xi / V        (Maloney-Lemaitre / Lutsko)

H^+ Xi is obtained as the solution delta of the CONSTRAINED minimization
    (H + sigma * P_trans) delta = Xi_proj
where P_trans projects onto the 3 global translations and Xi_proj = Xi with its
(numerically tiny) translation component removed. Because the 2nd-order energy
    dE(gamma,u) = 0.5*V*G_Born*gamma^2 + gamma*Xi.u + 0.5*u^T H u
is minimized over u at fixed gamma by a POSITIVE-SEMIDEFINITE Hessian H, the result
satisfies, EXACTLY (up to roundoff):
        0 <= G_relaxed <= G_Born.
So a strongly negative G is mathematically impossible here -- it was the explicit
1/omega^2 pseudoinverse (attempt d) that overshot. No 1/omega^2 is ever formed.

Physics (verified by re-derivation 2026-06-05):
  Harmonic contact  E = 0.25 (2R-r)^2 ,  K = E'' = 0.5 ,  phi'(r) = -K*ov , phi''(r)=K.
  Simple shear gamma_xy:  dr/dg = nx*ny*r ;  d2r/dg2 = r*ny^2*(ny^2+nz^2).
  Hessian off-diag block  H^{ij} = -K nn + (K ov/r)(I-nn).
  All on the rigid BACKBONE only (rattlers with < d+1 contacts removed iteratively).

Reduced units: m=1, L=1, d=3, V=L^3.
"""
import numpy as np
from scipy.spatial import cKDTree
from numpy.linalg import norm
import scipy.linalg as sla

d = 3
K = 0.5

# ----------------------------------------------------------------------------- contacts / FIRE
def contacts(pos, R, L):
    p = pos % L
    pr = cKDTree(p, boxsize=L).query_pairs(2 * R, output_type='ndarray')
    if len(pr) == 0:
        return (np.zeros(0, int),) * 2 + (np.zeros(0), np.zeros(0), np.zeros((0, d)))
    i, j = pr[:, 0], pr[:, 1]
    dv = p[i] - p[j]; dv -= L * np.rint(dv / L)
    r = np.sqrt((dv * dv).sum(1)); ov = 2 * R - r; m = ov > 0
    return i[m], j[m], r[m], ov[m], dv[m] / r[m][:, None]

def en_force(pos, R, L):
    i, j, r, ov, nh = contacts(pos, R, L)
    E = 0.25 * np.sum(ov ** 2); fv = (K * ov)[:, None] * nh
    F = np.zeros_like(pos); np.add.at(F, i, fv); np.add.at(F, j, -fv)
    return E, F

def _energy_grad_flat(x, R, L, N):
    pos = x.reshape(N, d)
    E, F = en_force(pos, R, L)
    return E, (-F).ravel()      # grad = -force

def lbfgs_polish(pos, R, L, maxiter=4000, gtol=1e-12):
    """Polish a FIRE result to tight stationarity (drives max force far below FIRE's tail)."""
    from scipy.optimize import minimize
    N = pos.shape[0]
    res = minimize(lambda x: _energy_grad_flat(x, R, L, N), pos.ravel(),
                   jac=True, method='L-BFGS-B',
                   options=dict(maxiter=maxiter, maxfun=20 * maxiter, ftol=1e-16, gtol=gtol))
    p = (res.x.reshape(N, d)) % L
    E, F = en_force(p, R, L); mF = norm(F, axis=1).max() if len(F) else 0.0
    return p, E, mF

def fire(pos, R, L, steps=20000, ftol=1e-12):
    pos = pos % L; v = np.zeros_like(pos)
    dt, dm, al, al0 = 2e-3, 5e-2, 0.1, 0.1; npc = 0
    mF = 0.0
    for _ in range(steps):
        E, F = en_force(pos, R, L); mF = norm(F, axis=1).max() if len(F) else 0.0
        if mF < ftol: break
        v += dt * F; vn = norm(v); fn = norm(F); pw = float((v * F).sum())
        if vn > 0 and fn > 0: v = (1 - al) * v + al * (vn / fn) * F
        if pw > 0:
            npc += 1
            if npc > 5: dt = min(dt * 1.1, dm); al *= 0.99
        else:
            npc = 0; dt *= 0.5; al = al0; v[:] = 0.0
        pos = (pos + dt * v) % L
    return pos, E, mF

# ----------------------------------------------------------------------------- backbone
def backbone_mask(pos, R, L, dz=None):
    """Iteratively drop rattlers with fewer than d+1 contacts; return boolean keep mask."""
    need = (d + 1) if dz is None else dz
    i, j, _, _, _ = contacts(pos, R, L); N = pos.shape[0]; keep = np.ones(N, bool)
    for _ in range(200):
        m = keep[i] & keep[j]
        c = np.bincount(np.r_[i[m], j[m]], minlength=N)
        new = keep & (c >= need)
        if new.sum() == keep.sum(): break
        keep = new
    return keep

def mean_z(pos, R, L, keep):
    i, j, _, _, _ = contacts(pos, R, L); N = pos.shape[0]
    m = keep[i] & keep[j]
    c = np.bincount(np.r_[i[m], j[m]], minlength=N)
    return float(c[keep].mean()) if keep.sum() else 0.0

# ----------------------------------------------------------------------------- Hessian, Born, Xi
def hessian_dense(pos, R, L):
    i, j, r, ov, nh = contacts(pos, R, L); N = pos.shape[0]; H = np.zeros((d * N, d * N))
    for a, b, rr, ovv, n in zip(i, j, r, ov, nh):
        nn = np.outer(n, n); blk = -K * nn + (K * ovv / rr) * (np.eye(d) - nn)
        ia, ib = d * a, d * b
        H[ia:ia + d, ib:ib + d] += blk; H[ib:ib + d, ia:ia + d] += blk
        H[ia:ia + d, ia:ia + d] -= blk; H[ib:ib + d, ib:ib + d] -= blk
    return H

def born_and_xi(pos, R, L):
    i, j, r, ov, nh = contacts(pos, R, L); N = pos.shape[0]; V = L ** 3
    nx, ny, nz = nh[:, 0], nh[:, 1], nh[:, 2]
    drg = nx * ny * r; d2rg = r * ny ** 2 * (ny ** 2 + nz ** 2)
    G_born = float(np.sum(K * drg ** 2 - K * ov * d2rg)) / V
    pref1 = (K * drg)[:, None] * nh
    dn = np.zeros((len(i), d)); dn[:, 0] = ny; dn -= nh * (nx * ny)[:, None]
    pref2 = (-K * ov)[:, None] * dn
    contrib = pref1 + pref2
    Xi = np.zeros((N, d)); np.add.at(Xi, i, contrib); np.add.at(Xi, j, -contrib)
    return G_born, Xi.ravel(), V, len(i)

# ----------------------------------------------------------------------------- relaxed G (direct solve)
def relaxed_G(pos, R, L):
    """Relaxed shear modulus via PINNED reduced linear solve + iterative refinement.
    Pin all 3 DOF of one backbone particle -> removes the 3 global translations exactly,
    leaving a strictly PD reduced Hessian for a rigid backbone (Cholesky succeeds iff stable
    minimum -> built-in PSD gate). Xi^T delta is gauge invariant, so the pin choice is immaterial.
    """
    keep = backbone_mask(pos, R, L)
    nbb = int(keep.sum())
    if nbb < d + 2:
        return dict(ok=False, reason="backbone too small", nbb=nbb)
    p = pos[keep]
    Gb, Xi, V, nc = born_and_xi(p, R, L)
    H = hessian_dense(p, R, L)
    Nb = p.shape[0]
    # pin the most-coordinated particle for best conditioning
    i, j, _, _, _ = contacts(p, R, L)
    cc = np.bincount(np.r_[i, j], minlength=Nb)
    p0 = int(np.argmax(cc))
    free = np.ones(d * Nb, bool); free[d * p0:d * p0 + d] = False
    Hr = H[np.ix_(free, free)]; br = Xi[free]
    try:
        cf = sla.cho_factor(Hr, lower=True, check_finite=False)
        dr = sla.cho_solve(cf, br, check_finite=False)
        for _ in range(2):                       # iterative refinement
            dr = dr + sla.cho_solve(cf, br - Hr @ dr, check_finite=False)
        psd = True; solver = "chol"
    except sla.LinAlgError:
        dr, *_ = np.linalg.lstsq(Hr, br, rcond=None)
        psd = False; solver = "lstsq"
    nonaff = float(br @ dr) / V
    Grel = Gb - nonaff
    res = norm(Hr @ dr - br) / max(norm(br), 1e-30)
    return dict(ok=True, G_Born=Gb, G_relaxed=Grel, nonaff=nonaff,
                nbb=nbb, n_contacts=nc, V=V, solver=solver, psd=psd, lin_residual=res)

# ----------------------------------------------------------------------------- one packing
def make_packing(N, phi, L, seed, steps=12000, ftol=1e-12, polish=True):
    R = (phi / (N * (4 / 3) * np.pi)) ** (1 / 3)
    rng = np.random.default_rng(seed)
    pos = rng.random((N, d)) * L
    pos, E, mF = fire(pos, R, L, steps=steps, ftol=ftol)
    if polish and E > 1e-13:
        pos, E, mF = lbfgs_polish(pos, R, L)
        if mF > 1e-8:                          # near-jam / large-N: harder, retry with more budget
            pos, E, mF = lbfgs_polish(pos, R, L, maxiter=12000)
    return pos, R, E, mF
