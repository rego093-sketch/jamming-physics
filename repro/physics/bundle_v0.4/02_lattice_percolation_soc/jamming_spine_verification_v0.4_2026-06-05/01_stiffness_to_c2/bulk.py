"""
bulk.py -- relaxed (non-affine) BULK modulus B by exact linear response,
mirroring the VALIDATED shear method (pinned reduced solve, PSD gate).

Affine (Born) bulk modulus for harmonic contacts (phi=0.25(2R-r)^2, K=phi''=0.5):
    B_aff = (1/(d^2 V)) * sum_contacts K r^2  +  ((d-1)/d) * P ,
    P  = (1/(d V)) sum K*ov*r     (pressure of the repulsive packing).
Non-affine drive (coefficient of eps in d^2E/deps du_i), harmonic:
    Xi^bulk_i = K * sum_{j~i} r * nhat_{ij}   (assembled +i, -j).
Relaxed:
    B_rel = B_aff - (1/(d^2 V)) Xi^bulk^T H^+ Xi^bulk ,
with H^+ Xi^bulk from the SAME pinned reduced Cholesky solve as relaxed_G:
variationally guarantees 0 <= correction, i.e. B_rel <= B_aff, and Cholesky
success is the PSD (stable-minimum) gate.

Speed of sound:  c^2 = B_rel / rho ,  rho = N_total / V  (m=1).
Near jamming G->0 while B stays finite -> single surviving longitudinal speed.
"""
import numpy as np, scipy.linalg as sla
from numpy.linalg import norm
from relaxed_shear import (d, K, contacts, hessian_dense, backbone_mask,
                           mean_z, make_packing, relaxed_G)

def born_bulk(pos, R, L):
    i, j, r, ov, nh = contacts(pos, R, L); N = pos.shape[0]; V = L ** d
    P    = float(np.sum(K * ov * r)) / (d * V)
    curv = float(np.sum(K * r ** 2))                  # = d2E/deps2 (pure 2nd order)
    B_aff = curv / (d ** 2 * V) + (d - 1) / d * P
    contrib = (K * r)[:, None] * nh
    Xi = np.zeros((N, d)); np.add.at(Xi, i, contrib); np.add.at(Xi, j, -contrib)
    return B_aff, Xi.ravel(), curv, P, V, len(i)

def fd_born_bulk(pos, R, L, h=1e-6):
    """Finite-difference affine bulk modulus, FIXED contact list (validates born_bulk)."""
    i, j, r0, ov0, nh = contacts(pos, R, L)
    eps = np.array([-2., -1., 0., 1., 2.]) * h
    E   = np.array([0.25 * np.sum((2 * R - (1 + e) * r0) ** 2) for e in eps])
    eV  = (1 + eps) ** d - 1.0
    c2  = np.polyfit(eV, E, 2)[0]                      # E = c2 eV^2 + ...
    return (2 * c2) / L ** d

def relaxed_bulk(pos, R, L, Ntot=None):
    keep = backbone_mask(pos, R, L); nbb = int(keep.sum())
    if nbb < d + 2:
        return dict(ok=False, reason="backbone too small", nbb=nbb)
    p = pos[keep]
    B_aff, Xi, curv, P, V, nc = born_bulk(p, R, L)
    H = hessian_dense(p, R, L); Nb = p.shape[0]
    i, j, _, _, _ = contacts(p, R, L); cc = np.bincount(np.r_[i, j], minlength=Nb)
    p0 = int(np.argmax(cc))
    free = np.ones(d * Nb, bool); free[d * p0:d * p0 + d] = False
    Hr = H[np.ix_(free, free)]; br = Xi[free]
    try:
        cf = sla.cho_factor(Hr, lower=True, check_finite=False)
        dr = sla.cho_solve(cf, br, check_finite=False)
        for _ in range(2):
            dr = dr + sla.cho_solve(cf, br - Hr @ dr, check_finite=False)
        psd = True; solver = "chol"
    except sla.LinAlgError:
        dr, *_ = np.linalg.lstsq(Hr, br, rcond=None); psd = False; solver = "lstsq"
    nonaff = float(br @ dr) / (d ** 2 * V)
    B_rel = B_aff - nonaff
    res = norm(Hr @ dr - br) / max(norm(br), 1e-30)
    Ntot = Ntot if Ntot is not None else pos.shape[0]
    rho = Ntot / V
    return dict(ok=True, B_Born=B_aff, B_relaxed=B_rel, nonaff=nonaff, P=P,
                curv=curv, nbb=nbb, n_contacts=nc, V=V, solver=solver, psd=psd,
                lin_residual=res, rho=rho,
                c2_Born=B_aff / rho, c2_relaxed=B_rel / rho)
