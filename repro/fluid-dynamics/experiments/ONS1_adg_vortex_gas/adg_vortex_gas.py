#!/usr/bin/env python3
"""ONS1 -- independent re-implementation of the forward-merger point-vortex gas
(Average Discrete Gradient integrator) described in SM S1, S3, S5 of
"Vortex-Merger Thermodynamics in 2D Turbulence: A Metriplectic Scenario for the
Onsager Anomaly".  numpy + stdlib only.  All model choices are frozen in
PREREG.json (written before this file).

Model
-----
* N like-signed point vortices, Gamma_i = 1 initially, torus L = 2*pi.
* H_flow = 1/2 sum_{i!=j} G_i G_j G(x_i - x_j), G = zero-mean doubly periodic
  Green's function of -Laplacian (neutralising background).  G is evaluated
  with the rapidly convergent row sum
      G(x,y) = -(1/4pi) sum_{m=-M}^{M} ln[(cosh(y-2pi m)-cos x)/cosh(2pi m)]
               + y^2/(8 pi^2) + const            (x, y minimum-imaged)
  (error ~ exp(-(2M-1)pi); M = 3 -> 1.5e-7), const fixed so that <G> = 0.
* Conservative step: AVF / mean-value discrete gradient (SM Eq. 18-19),
  z* - z = dt J int_0^1 grad H(z + xi (z*-z)) dxi, 3-point Gauss-Legendre,
  solved by (simplified) Newton with the exact AVF Jacobian.
* Merger: |x_i-x_j| < r_c -> one vortex, Gamma_i+Gamma_j, circulation-weighted
  centre; H_int += -Delta H_flow (SM Eq. 5 / 22).
* Units: E0 = H_flow(t=0), U0 = sqrt(2 E0)/L, T0 = L/U0; eps in E0/T0.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

L = 2.0 * math.pi
M_IMG = 3
_MS = np.arange(-M_IMG, M_IMG + 1, dtype=float)
_QM = np.exp(-2.0 * math.pi * _MS)            # e^{-2 pi m}
_LNCOSH = np.log(np.cosh(2.0 * math.pi * _MS))
GL_X, GL_W = np.polynomial.legendre.leggauss(3)
GL_X = 0.5 * (GL_X + 1.0)
GL_W = 0.5 * GL_W
G_CONST = 0.0  # set by calibrate_const()


def wrap(d):
    return d - L * np.round(d / L)


def green(dx, dy, hess=False):
    """G, Gx, Gy (and Gxx, Gxy) for minimum-imaged separations (arrays)."""
    s2x = np.sin(0.5 * dx) ** 2
    cx = np.cos(dx)
    sx = np.sin(dx)
    ey = np.exp(dy)
    G = np.zeros_like(dx)
    Gx = np.zeros_like(dx)
    Gy = np.zeros_like(dx)
    if hess:
        Gxx = np.zeros_like(dx)
        Gxy = np.zeros_like(dx)
    for m, q, lc in zip(_MS, _QM, _LNCOSH):
        a = ey * q                        # e^{Y}, Y = y - 2 pi m
        C = 0.5 * (a + 1.0 / a)
        S = 0.5 * (a - 1.0 / a)
        sh = 0.5 * (np.sqrt(a) - 1.0 / np.sqrt(a))  # sinh(Y/2)
        D = 2.0 * sh * sh + 2.0 * s2x     # cosh Y - cos x, cancellation-free
        G -= np.log(D) - lc
        Gx -= sx / D
        Gy -= S / D
        if hess:
            D2 = D * D
            Gxx -= (C * cx - 1.0) / D2
            Gxy += S * sx / D2
    f = 1.0 / (4.0 * math.pi)
    G = f * G + dy * dy / (8.0 * math.pi ** 2) + G_CONST
    Gx = f * Gx
    Gy = f * Gy + dy / (4.0 * math.pi ** 2)
    if hess:
        return G, Gx, Gy, f * Gxx, f * Gxy
    return G, Gx, Gy


def calibrate_const(n=2048):
    """Choose G_CONST so that the cell average of G vanishes."""
    global G_CONST
    G_CONST = 0.0
    h = L / n
    c = -math.pi + h * (np.arange(n) + 0.5)
    tot = 0.0
    for row in np.array_split(c, 16):
        X, Y = np.meshgrid(c, row, indexing="xy")
        tot += green(X, Y)[0].sum()
    G_CONST = -tot / n ** 2
    return G_CONST


def pair_arrays(X):
    dx = wrap(X[:, 0][:, None] - X[:, 0][None, :])
    dy = wrap(X[:, 1][:, None] - X[:, 1][None, :])
    np.fill_diagonal(dx, 1.0)  # dummy, masked below
    np.fill_diagonal(dy, 1.0)
    return dx, dy


def energy(X, Gam):
    dx, dy = pair_arrays(X)
    G = green(dx, dy)[0]
    np.fill_diagonal(G, 0.0)
    return 0.5 * Gam @ G @ Gam


def velocity(X, Gam, jac=False):
    dx, dy = pair_arrays(X)
    if jac:
        G, Gx, Gy, Gxx, Gxy = green(dx, dy, hess=True)
    else:
        G, Gx, Gy = green(dx, dy)
    for A in ((Gx, Gy, Gxx, Gxy) if jac else (Gx, Gy)):
        np.fill_diagonal(A, 0.0)
    V = np.empty_like(X)
    V[:, 0] = Gy @ Gam
    V[:, 1] = -(Gx @ Gam)
    if not jac:
        return V
    n = len(Gam)
    Gyy = -Gxx + 1.0 / L ** 2  # lap G = 1/L^2 off the singularity
    np.fill_diagonal(Gyy, 0.0)
    Jm = np.zeros((2 * n, 2 * n))
    # dVx_i/dx_k etc (Vx = sum_j Gam_j Gy(x_i-x_j), Vy = -sum_j Gam_j Gx)
    for (r, c, B, sgn) in ((0, 0, Gxy, 1.0), (0, 1, Gyy, 1.0),
                           (1, 0, Gxx, -1.0), (1, 1, Gxy, -1.0)):
        blk = -sgn * B * Gam[None, :]
        blk[np.diag_indices(n)] = sgn * (B @ Gam)
        Jm[r::2, c::2] = blk
    return V, Jm


def log_terms(dx, dy):
    """Free-space kernel -(1/2pi) ln r: gradient and Hessian."""
    r2 = dx * dx + dy * dy
    f = 1.0 / (2 * math.pi)
    Gx, Gy = -f * dx / r2, -f * dy / r2
    Gxx = -f * (dy * dy - dx * dx) / (r2 * r2)
    Gxy = 2 * f * dx * dy / (r2 * r2)
    return Gx, Gy, Gxx, Gxy


def pair_log_velocity(Z, Gam, I, J):
    V = np.zeros_like(Z)
    if len(I) == 0:
        return V
    dx = wrap(Z[I, 0] - Z[J, 0])
    dy = wrap(Z[I, 1] - Z[J, 1])
    Gx, Gy, _, _ = log_terms(dx, dy)
    V[I, 0] += Gam[J] * Gy
    V[I, 1] += -Gam[J] * Gx
    V[J, 0] += -Gam[I] * Gy
    V[J, 1] += Gam[I] * Gx
    return V


def pair_log_jac(Z, Gam, I, J):
    n = len(Gam)
    Jm = np.zeros((2 * n, 2 * n))
    if len(I) == 0:
        return Jm
    dx = wrap(Z[I, 0] - Z[J, 0])
    dy = wrap(Z[I, 1] - Z[J, 1])
    _, _, Gxx, Gxy = log_terms(dx, dy)
    Hb = np.stack([np.stack([Gxy, -Gxx], -1), np.stack([-Gxx, -Gxy], -1)], -2)
    for a, b, gb in ((I, J, Gam[J]), (J, I, Gam[I])):
        blk = gb[:, None, None] * Hb
        for r in range(2):
            for c in range(2):
                Jm[2 * a + r, 2 * a + c] += blk[:, r, c]
                Jm[2 * a + r, 2 * b + c] -= blk[:, r, c]
    return Jm


def match_pairs(X, Gam, dt_ref, om_pair=0.05):
    """Greedy disjoint matching of stiff pairs (omega*dt_ref > om_pair)."""
    dx, dy = pair_arrays(X)
    r2 = dx * dx + dy * dy
    np.fill_diagonal(r2, np.inf)
    om = (Gam[:, None] + Gam[None, :]) / (2 * math.pi * r2)
    cand = np.argwhere(np.triu(om * dt_ref > om_pair, 1))
    order = np.argsort(r2[cand[:, 0], cand[:, 1]]) if len(cand) else []
    used = set()
    I, J = [], []
    for k in order:
        i, j = cand[k]
        if i in used or j in used:
            continue
        used.update((i, j))
        I.append(i)
        J.append(j)
    I, J = np.array(I, int), np.array(J, int)
    om_rest = om.copy()
    om_rest[I, J] = 0.0
    om_rest[J, I] = 0.0
    return I, J, om_rest.max()


def rotate_pairs(X, Gam, I, J, tau):
    """Exact flow of the free-space pair Hamiltonians -(Gi Gj/2pi) ln|d|."""
    if len(I) == 0:
        return X
    X = X.copy()
    gi, gj = Gam[I], Gam[J]
    d = np.stack([wrap(X[I, 0] - X[J, 0]), wrap(X[I, 1] - X[J, 1])], -1)
    c = X[J] + (gi / (gi + gj))[:, None] * d
    ang = (gi + gj) / (2 * math.pi * (d ** 2).sum(-1)) * tau
    ca, sa = np.cos(ang), np.sin(ang)
    dn = np.stack([ca * d[:, 0] - sa * d[:, 1], sa * d[:, 0] + ca * d[:, 1]], -1)
    X[I] = c + (gj / (gi + gj))[:, None] * dn
    X[J] = c - (gi / (gi + gj))[:, None] * dn
    return X


def adg_step(X, Gam, dt, I, J, tol=1e-12, maxit=40):
    """Strang step: exact near-pair rotation (dt/2) | AVF discrete-gradient
    step (SM Eq. 18-19) on the remaining, non-stiff Hamiltonian
    H_far = H_flow - sum_pairs[-(Gi Gj/2pi) ln|d|] (dt) | rotation (dt/2).
    The AVF sub-step conserves H_far to quadrature/solver tolerance; the
    rotation conserves each pair term exactly.  Returns (Z, its) or (None, its)."""
    Y = rotate_pairs(X, Gam, I, J, 0.5 * dt)
    V0, J0 = velocity(Y, Gam, jac=True)
    V0 = V0 - pair_log_velocity(Y, Gam, I, J)
    J0 = J0 - pair_log_jac(Y, Gam, I, J)
    A = np.eye(2 * len(Gam)) - 0.5 * dt * J0
    Z = Y + dt * V0
    for it in range(1, maxit + 1):
        Vbar = np.zeros_like(Y)
        for xi, w in zip(GL_X, GL_W):
            Zq = Y + xi * (Z - Y)
            Vbar += w * (velocity(Zq, Gam) - pair_log_velocity(Zq, Gam, I, J))
        R = (Z - Y - dt * Vbar).reshape(-1)
        if not np.all(np.isfinite(R)):
            return None, it
        dZ = np.linalg.solve(A, R).reshape(-1, 2)
        Z = Z - dZ
        if np.abs(dZ).max() < tol:
            return rotate_pairs(Z, Gam, I, J, 0.5 * dt), it
    return None, maxit


# ---------------------------------------------------------------- mergers --
def interaction(xp, Xo, Go, kind="periodic"):
    """sum_k Go_k * G(xp - Xo_k) for one point against others."""
    dx = wrap(xp[0] - Xo[:, 0])
    dy = wrap(xp[1] - Xo[:, 1])
    if kind == "periodic":
        return float(green(dx, dy)[0] @ Go)
    # SM-literal free-space log with minimum image, Eq. (4)
    return float((-np.log(np.hypot(dx, dy)) / (2 * math.pi)) @ Go)


def energy_literal(X, Gam):
    dx, dy = pair_arrays(X)
    r = np.hypot(dx, dy)
    np.fill_diagonal(r, 1.0)
    return 0.5 * Gam @ (-np.log(r) / (2 * math.pi)) @ Gam


def do_mergers(X, Gam, A, rc, t, log):
    """Merge all pairs closer than rc (closest first). A = core radii."""
    dH_tot = 0.0
    while len(Gam) > 1:
        dx, dy = pair_arrays(X)
        r = np.hypot(dx, dy)
        np.fill_diagonal(r, np.inf)
        k = int(np.argmin(r))
        i, j = divmod(k, len(Gam))
        if r[i, j] >= rc:
            break
        gi, gj = Gam[i], Gam[j]
        others = np.array([k2 for k2 in range(len(Gam)) if k2 not in (i, j)])
        Xo, Go = X[others], Gam[others]
        gn = gi + gj
        d = np.array([dx[j, i], dy[j, i]])  # x_j - x_i (min image)
        xn = X[i] + (gj / gn) * d
        rij = float(r[i, j])
        pair_G = float(green(np.array([d[0]]), np.array([d[1]]))[0][0])
        before = gi * interaction(X[i], Xo, Go) + gj * interaction(X[j], Xo, Go) + gi * gj * pair_G
        after = gn * interaction(xn, Xo, Go)
        dH = after - before
        # SM-literal accounting (free-space log, minimum image)
        pair_lit = -math.log(rij) / (2 * math.pi)
        dH_lit = (gn * interaction(xn, Xo, Go, "lit")
                  - gi * interaction(X[i], Xo, Go, "lit") - gj * interaction(X[j], Xo, Go, "lit")
                  - gi * gj * pair_lit)
        # finite-core (Rankine) self energies, area-conserving merger
        ai, aj = A[i], A[j]
        an = math.sqrt(ai * ai + aj * aj)
        def eself(g, a):
            return g * g / (4 * math.pi) * (math.log(1.0 / a) + 0.25)
        dE_self = eself(gn, an) - eself(gi, ai) - eself(gj, aj)
        log.append(dict(t=t, gi=float(gi), gj=float(gj), r=rij, dH=dH, pair=-gi * gj * pair_G,
                        dH_lit=dH_lit, dE_core=dH + dE_self))
        dH_tot += dH
        keep = np.ones(len(Gam), bool)
        keep[j] = False
        X[i] = wrap(xn + math.pi) - math.pi
        Gam[i] = gn
        A[i] = an
        X, Gam, A = X[keep], Gam[keep], A[keep]
    return X, Gam, A, dH_tot


# ------------------------------------------------------------------ run ----
def initial_state(N, seed, K=5, sigma=0.3):
    rng = np.random.default_rng(seed)
    centres = rng.uniform(-math.pi, math.pi, size=(K, 2))
    lab = np.arange(N) % K
    X = centres[lab] + sigma * rng.standard_normal((N, 2))
    return wrap(X + math.pi) - math.pi


def run(N, rc, seed, t_max_T0=1.0, t_trans_T0=0.2, pre_T0=0.05, omega_dt=0.5,
        dt_max_T0=1.0 / 2000, wall_limit=None, verbose=False, track=None):
    """track: list of distance thresholds; records first-passage times of every
    pair below each threshold (diagnostic, meaningful for merger-free runs)."""
    t_wall = time.time()
    X = initial_state(N, seed)
    Gam = np.ones(N)
    A = np.full(N, rc / 2.0)
    E0 = energy(X, Gam)
    U0 = math.sqrt(2.0 * E0) / L
    T0 = L / U0
    stats = dict(steps=0, max_step_drift=0.0, sum_abs_drift=0.0, newton_fail=0, newton_its=0)

    def evolve(X, Gam, A, t, t_end, merge, log, Hint, samples):
        while t < t_end - 1e-15:
            dtm = min(dt_max_T0 * T0, t_end - t)
            I, J, om_rest = match_pairs(X, Gam, dtm)
            dt = min(dtm, omega_dt / om_rest)
            H0 = energy(X, Gam)
            while True:
                Z, it = adg_step(X, Gam, dt, I, J)
                stats["newton_its"] += it
                if Z is not None:
                    break
                stats["newton_fail"] += 1
                dt *= 0.5
            H1 = energy(Z, Gam)
            stats["steps"] += 1
            stats["max_step_drift"] = max(stats["max_step_drift"], abs(H1 - H0) / E0)
            stats["sum_abs_drift"] += abs(H1 - H0) / E0
            X = wrap(Z + math.pi) - math.pi
            t += dt
            if merge:
                X, Gam, A, dH = do_mergers(X, Gam, A, rc, t, log)
                Hint -= dH
            samples.append((t, Hint, len(Gam)))
            if track is not None and merge:
                dx, dy = pair_arrays(X)
                rr = np.hypot(dx, dy)
                np.fill_diagonal(rr, np.inf)
                for k, thr in enumerate(track):
                    hit = (rr < thr) & np.isinf(first[k])
                    first[k][hit] = t
            if wall_limit and time.time() - t_wall > wall_limit:
                raise TimeoutError
        return X, Gam, A, t, Hint

    # Hamiltonian pre-run, mergers off
    X, Gam, A, _, _ = evolve(X, Gam, A, 0.0, pre_T0 * T0, False, [], 0.0, [])
    E0 = energy(X, Gam)   # identical to IC energy up to drift
    E0_lit = energy_literal(X, Gam)
    log, samples = [], []
    if track is not None:
        first = [np.full((N, N), np.inf) for _ in track]
        dx, dy = pair_arrays(X)
        rr = np.hypot(dx, dy)
        np.fill_diagonal(rr, np.inf)
        below0 = [int(np.triu(rr < thr, 1).sum()) for thr in track]
    X, Gam, A, _, Hint_trans = evolve(X, Gam, A, 0.0, t_trans_T0 * T0, True, log, 0.0, samples)
    Hflow_trans = energy(X, Gam)
    X, Gam, A, _, Hint_end = evolve(X, Gam, A, t_trans_T0 * T0, t_max_T0 * T0, True, log, Hint_trans, samples)
    Hflow_end = energy(X, Gam)
    win = (t_max_T0 - t_trans_T0) * T0
    unit = E0 / T0
    in_win = [e for e in log if e["t"] > t_trans_T0 * T0]
    def rate(key, sign=-1.0):
        return sign * sum(e[key] for e in in_win) / win / unit
    res = dict(
        N=N, rc=rc, seed=seed, E0=E0, T0=T0, E0_lit=E0_lit,
        Re_eff=L / rc,
        eps_bind=(Hint_end - Hint_trans) / win / unit,
        eps_tot=-(Hflow_end - Hflow_trans) / win / unit,
        n_mergers=len(log), n_mergers_window=len(in_win), N_final=len(Gam),
        H_int_final_over_E0=Hint_end / E0,
        eps_bind_pairterm=rate("pair"),
        eps_bind_gauge_lnL=None,  # filled below
        eps_bind_literal=rate("dH_lit"),
        eps_bind_literal_E0lit=rate("dH_lit") * E0 / E0_lit,
        eps_bind_core=rate("dE_core"),
        mean_release_per_merger_over_pair_selfterm=(
            float(np.mean([e["dH"] / e["pair"] for e in log])) if log else None),
        mean_release_per_merger=(float(np.mean([-e["dH"] for e in log])) if log else None),
        wall_s=time.time() - t_wall, **stats, mergers=log,
    )
    if track is not None:
        tt = t_trans_T0 * T0
        res["first_passage"] = dict(thresholds=list(track), below_at_switch_on=below0,
            new_in_transient=[int(np.triu((f > 0) & (f <= tt), 1).sum()) - 0 for f in first],
            new_in_window=[int(np.triu((f > tt) & np.isfinite(f), 1).sum()) for f in first])
    # gauge A: G' = G + C with G' ~ -(1/2pi) ln(r/L) at short range
    g0 = G_CONST_REG
    C = math.log(L) / (2 * math.pi) - g0
    dH_alt = [e["dH"] - C * e["gi"] * e["gj"] for e in in_win]
    E0_alt = E0 + 0.5 * C * (N * N - N)
    res["eps_bind_gauge_lnL"] = -sum(dH_alt) / win / unit
    res["eps_bind_gauge_lnL_E0alt"] = -sum(dH_alt) / win / (E0_alt / T0) if E0_alt > 0 else None
    res["E0_gauge_lnL"] = E0_alt
    if verbose:
        print({k: v for k, v in res.items() if k != "mergers"}, flush=True)
    return res


def regular_part():
    """g0 = lim_{r->0} [G(r) + (1/2pi) ln r] for the zero-mean G."""
    r = 1e-4
    G = green(np.array([r]), np.array([0.0]))[0][0]
    return G + math.log(r) / (2 * math.pi)


calibrate_const()
G_CONST_REG = regular_part()


def _job(args):
    kw = dict(args)
    try:
        return run(**kw)
    except TimeoutError:
        return dict(kw, timeout=True)


if __name__ == "__main__":
    import multiprocessing as mp
    here = os.path.dirname(os.path.abspath(__file__))
    cfg = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    Ns = cfg.get("N", [200])
    rcs = cfg.get("rc", [0.01, 0.005, 0.002])
    seeds = cfg.get("seeds", [101, 102, 103, 104, 105])
    extra = cfg.get("kw", {})
    out = cfg.get("out", "runs.json")
    jobs = [dict(N=N, rc=rc, seed=s, **extra) for N in Ns for rc in rcs for s in seeds]
    t0 = time.time()
    with mp.Pool(cfg.get("procs", 4)) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    print(f"{len(jobs)} runs in {time.time()-t0:.1f}s")
    with open(os.path.join(here, out), "w") as f:
        json.dump(dict(G_CONST=G_CONST, g0=G_CONST_REG, cfg=cfg, runs=res), f, indent=1)
