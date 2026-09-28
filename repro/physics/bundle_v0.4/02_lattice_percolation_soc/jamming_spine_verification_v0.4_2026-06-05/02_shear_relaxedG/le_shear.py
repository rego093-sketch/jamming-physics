"""le_shear.py -- finite-shear-rate ATHERMAL OVERDAMPED dynamics under Lees-Edwards (Durian /
Olsson-Teitel model), same harmonic contacts as the static work. Measures the steady-state shear
stress -> flow curve sigma(gamma_dot) and yield stress sigma_y(phi). Tests the LITERAL real-time
question: near z_iso the relaxation time diverges so the system cannot follow the drive and flows.

Sheared periodic box = triclinic lattice  v1=(L,0,0), v2=(Delta,L,0), v3=(0,0,L),  Delta=g_box*L,
g_box = gamma mod 1. Overdamped EOM (zeta=1):  dr_i/dt = gamma_dot * y_i * xhat + F_i.
Virial shear stress:  sigma_xy = (1/V) sum_{contacts} f_x(i<-j) * r_y(i-j).
Reduced units m=1,L=1,d=3,K=0.5.
"""
import numpy as np
d = 3; K = 0.5

def le_minimg(dr, L, g_box):
    """Apply Lees-Edwards minimum image to separation array dr (...,3). g_box = gamma mod 1."""
    dx, dy, dz = dr[..., 0].copy(), dr[..., 1].copy(), dr[..., 2].copy()
    ny = np.round(dy / L)
    dy = dy - ny * L
    dx = dx - ny * g_box * L          # shear coupling on y-wrap
    dx = dx - np.round(dx / L) * L
    dz = dz - np.round(dz / L) * L
    return np.stack([dx, dy, dz], axis=-1)

def forces_stress(pos, R, L, gamma):
    """Vectorized O(N^2) contact forces + energy + virial shear stress under LE shear strain gamma."""
    N = pos.shape[0]; V = L ** 3; g_box = gamma - np.floor(gamma)
    dr = pos[:, None, :] - pos[None, :, :]            # (N,N,3): r_i - r_j
    dr = le_minimg(dr, L, g_box)
    r2 = (dr * dr).sum(-1)
    iu = np.triu_indices(N, 1)
    rr = np.sqrt(r2[iu]); ov = 2 * R - rr
    m = ov > 0
    ii, jj = iu[0][m], iu[1][m]
    rvec = dr[iu][m]; rmag = rr[m]; ovm = ov[m]
    nh = rvec / rmag[:, None]
    fmag = K * ovm
    fij = fmag[:, None] * nh                           # force on i from j
    F = np.zeros((N, d))
    np.add.at(F, ii, fij); np.add.at(F, jj, -fij)
    E = 0.25 * np.sum(ovm ** 2)
    sigma_xy = float(np.sum(fij[:, 0] * rvec[:, 1])) / V   # (1/V) sum f_x * r_y
    return E, F, sigma_xy, int(m.sum())

def forces_stress_bruteforce(pos, R, L, gamma):
    """Reference: explicit triclinic image enumeration (a,b,c in -1..1). For VALIDATION only."""
    N = pos.shape[0]; V = L ** 3; g_box = gamma - np.floor(gamma)
    v1 = np.array([L, 0.0, 0.0]); v2 = np.array([g_box * L, L, 0.0]); v3 = np.array([0.0, 0.0, L])
    shifts = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            for c in (-1, 0, 1):
                shifts.append(a * v1 + b * v2 + c * v3)
    shifts = np.array(shifts)                          # (27,3)
    F = np.zeros((N, d)); E = 0.0; sxy = 0.0; nc = 0
    for i in range(N):
        for j in range(i + 1, N):
            base = pos[i] - pos[j]
            cand = base[None, :] + shifts               # (27,3)
            dist2 = (cand * cand).sum(1)
            k = np.argmin(dist2); rvec = cand[k]; rmag = np.sqrt(dist2[k])
            ov = 2 * R - rmag
            if ov > 0:
                n = rvec / rmag; f = K * ov * n
                F[i] += f; F[j] -= f; E += 0.25 * ov ** 2
                sxy += f[0] * rvec[1]; nc += 1
    return E, F, sxy / V, nc

def run_shear(pos0, R, L, gdot, gamma_total=3.0, dt=0.05, gamma_eq=1.0):
    """Overdamped LE shear at rate gdot to total strain gamma_total. Returns strain & stress arrays;
    steady-state mean stress uses strain > gamma_eq."""
    pos = pos0.copy() % L
    nsteps = int(np.ceil(gamma_total / (gdot * dt)))
    g_hist = np.empty(nsteps); s_hist = np.empty(nsteps)
    for s in range(nsteps):
        gamma = gdot * dt * s
        E, F, sxy, nc = forces_stress(pos, R, L, gamma)
        g_hist[s] = gamma; s_hist[s] = sxy
        # overdamped update: affine advection + force; zeta=1
        pos[:, 0] += dt * (gdot * pos[:, 1] + F[:, 0])
        pos[:, 1] += dt * F[:, 1]
        pos[:, 2] += dt * F[:, 2]
        # wrap with Lees-Edwards on the y-boundary
        g_box = gamma - np.floor(gamma)
        hi = pos[:, 1] >= L; lo = pos[:, 1] < 0
        pos[hi, 0] -= g_box * L; pos[lo, 0] += g_box * L
        pos[:, 1] = pos[:, 1] % L
        pos[:, 0] = pos[:, 0] % L; pos[:, 2] = pos[:, 2] % L
    mask = g_hist > gamma_eq
    sig_mean = float(np.mean(s_hist[mask])) if mask.any() else float(np.mean(s_hist))
    sig_std = float(np.std(s_hist[mask])) if mask.any() else float(np.std(s_hist))
    return g_hist, s_hist, sig_mean, sig_std
