#!/usr/bin/env python3
"""NC1 — Newtonian-closure gate on a sheared 2-D particle arrangement (numpy only).

Model A: athermal overdamped bidisperse harmonic disks (Durian mean-field drag),
         Lees-Edwards shear -> sigma_xy(gdot) at many phi  (P1, P2, P3)
Model B: thermal inertial liquid of the same disks, eta by two routes:
         (1) SLLOD NEMD stress, (2) periodic-perturbation velocity profile  (P4)
Model C: athermal inertial disks with pair damping (Bagnold control)  (P5)

Frozen protocol: PREREG.json.  Deterministic: SEED = 19.
Usage: python3 nc1_run.py [--quick]
"""
import json, sys, time, hashlib, os
import numpy as np
from multiprocessing import Pool

SEED = 19
HERE = os.path.dirname(os.path.abspath(__file__))
QUICK = "--quick" in sys.argv
N = 64 if QUICK else 512
R_SMALL, R_LARGE = 0.5, 0.7
SKIN = 0.3


# ----------------------------------------------------------------- geometry
def make_system(n, phi, rng):
    rad = np.where(np.arange(n) < n // 2, R_SMALL, R_LARGE).astype(float)
    L = np.sqrt(np.pi * np.sum(rad ** 2) / phi)
    pos = rng.random((n, 2)) * L
    return pos, rad, L


def min_image(dx, dy, L, shift):
    ny = np.round(dy / L)
    dx = dx - ny * shift
    dy = dy - ny * L
    dx = dx - np.round(dx / L) * L
    return dx, dy


def wrap_le(pos, L, shift, vel=None, gdotL=0.0):
    """Lees-Edwards wrap; lab velocities (if given) jump by -/+ gdot*L."""
    ny = np.floor(pos[:, 1] / L)
    if np.any(ny != 0):
        pos[:, 0] -= ny * shift
        pos[:, 1] -= ny * L
        if vel is not None and gdotL != 0.0:
            vel[:, 0] -= ny * gdotL
    pos[:, 0] -= np.floor(pos[:, 0] / L) * L


class NList:
    def __init__(self, rad):
        n = len(rad)
        self.I, self.J = np.triu_indices(n, 1)
        self.rsum_all = rad[self.I] + rad[self.J]

    def build(self, pos, L, shift):
        dx = pos[self.I, 0] - pos[self.J, 0]
        dy = pos[self.I, 1] - pos[self.J, 1]
        dx, dy = min_image(dx, dy, L, shift)
        m = dx * dx + dy * dy < (self.rsum_all + SKIN) ** 2
        self.i, self.j, self.rsum = self.I[m], self.J[m], self.rsum_all[m]


def pair_geometry(pos, nl, L, shift):
    dx = pos[nl.i, 0] - pos[nl.j, 0]
    dy = pos[nl.i, 1] - pos[nl.j, 1]
    dx, dy = min_image(dx, dy, L, shift)
    d = np.sqrt(dx * dx + dy * dy)
    ov = nl.rsum - d
    c = ov > 0
    return dx[c], dy[c], d[c], ov[c], nl.i[c], nl.j[c]


def contact_forces(pos, nl, L, shift, n, k=1.0, cvel=None, gdot=0.0, b=0.0):
    """Harmonic repulsion (+ optional normal damping on lab relative velocity).
    Returns F (n,2), virial sums Wxy=sum r_x f_y, Wxx+Wyy, n_contacts, U."""
    dx, dy, d, ov, i, j = pair_geometry(pos, nl, L, shift)
    nx, ny = dx / d, dy / d
    fmag = k * ov
    if b > 0.0 and cvel is not None:
        # lab relative velocity = peculiar difference + affine gdot*dy xhat
        vrx = cvel[i, 0] - cvel[j, 0] + gdot * dy
        vry = cvel[i, 1] - cvel[j, 1]
        fmag = fmag - b * (vrx * nx + vry * ny)
    fx, fy = fmag * nx, fmag * ny
    F = np.empty((n, 2))
    F[:, 0] = np.bincount(i, fx, n) - np.bincount(j, fx, n)
    F[:, 1] = np.bincount(i, fy, n) - np.bincount(j, fy, n)
    Wxy = np.sum(dx * fy)
    Wtr = np.sum(dx * fx + dy * fy)
    return F, Wxy, Wtr, len(d), 0.5 * k * np.sum(ov * ov)


def blocks(x, nb=10):
    x = np.asarray(x)
    m = len(x) // nb
    if m == 0:
        return float(np.mean(x)), float("nan")
    b = x[: m * nb].reshape(nb, m).mean(1)
    return float(b.mean()), float(b.std(ddof=1) / np.sqrt(nb))


# ------------------------------------------------------ model A: overdamped
def run_overdamped(args):
    phi, gdot, idx = args
    rng = np.random.default_rng(SEED * 1000 + idx)
    pos, rad, L = make_system(N, phi, rng)
    nl = NList(rad)
    dt, zeta = 0.1, 1.0
    # remove initial overlaps (FIRE-free: plain overdamped relaxation, no shear)
    shift, strain = 0.0, 0.0
    nl.build(pos, L, shift)
    ref = pos.copy()
    for _ in range(2000):
        F = contact_forces(pos, nl, L, shift, N)[0]
        pos += dt * F / zeta
        wrap_le(pos, L, shift)
        if np.max(np.abs(pos - ref)) > 0.25 * SKIN:  # crude (wrap-safe enough: triggers rebuild)
            nl.build(pos, L, shift); ref = pos.copy()
    nl.build(pos, L, shift)
    na = np.zeros((N, 2)); strain_at_build = 0.0
    tr_strain, meas_strain = (0.2, 0.3) if QUICK else (1.0, 2.0)
    nsteps = int(round((tr_strain + meas_strain) / (gdot * dt)))
    ntr = int(round(tr_strain / (gdot * dt)))
    every = max(1, (nsteps - ntr) // 2000)
    S, P, Z = [], [], []
    A = L * L
    for s in range(nsteps):
        F, Wxy, Wtr, nc, _ = contact_forces(pos, nl, L, shift, N)
        if s >= ntr and (s - ntr) % every == 0:
            S.append(-Wxy / A); P.append(Wtr / (2 * A)); Z.append(2.0 * nc / N)
        dr = dt * F / zeta
        pos[:, 0] += gdot * dt * pos[:, 1]
        pos += dr
        na += dr
        strain += gdot * dt
        shift = (strain % 1.0) * L
        wrap_le(pos, L, shift)
        if 2 * np.sqrt(np.max(np.sum(na * na, 1))) + (strain - strain_at_build) * (2 * R_LARGE + SKIN) > SKIN:
            nl.build(pos, L, shift); na[:] = 0.0; strain_at_build = strain
    sig, sig_e = blocks(S); p, p_e = blocks(P); z, _ = blocks(Z)
    return dict(phi=phi, gdot=gdot, sigma=sig, sigma_err=sig_e, eta=sig / gdot,
                eta_err=sig_e / gdot, p=p, z=z, steps=nsteps, L=L)


# --------------------------------------------- inertial SLLOD core (B and C)
def relax(pos, rad, L, nl, n, steps=3000):
    ref = pos.copy()
    for _ in range(steps):
        F = contact_forces(pos, nl, L, 0.0, n)[0]
        pos += 0.1 * F
        wrap_le(pos, L, 0.0)
        if np.max(np.abs(pos - ref)) > 0.25 * SKIN:
            nl.build(pos, L, 0.0); ref = pos.copy()
    nl.build(pos, L, 0.0)


def sllod(pos, c, rad, L, nl, n, gdot, dt, nsteps, ntr, T=None, b=0.0,
          accel=None, sample_every=10):
    """Velocity-Verlet SLLOD (lab-frame Newton for gdot != 0) with Lees-Edwards.
    c = peculiar velocity (m = 1). T: isokinetic target (None = no thermostat).
    accel: amplitude A of body force A cos(k y) xhat (periodic perturbation; gdot must be 0).
    Returns sampled -P_xy (stress route) or V (profile amplitude)."""
    strain = 0.0; shift = 0.0; strain_b = 0.0
    kw = 2 * np.pi / L
    A = L * L
    na = np.zeros((n, 2))
    F, Wxy, *_ = contact_forces(pos, nl, L, shift, n, cvel=c, gdot=gdot, b=b)
    out, Zs = [], []
    for s in range(nsteps):
        if accel is not None:
            F = F.copy(); F[:, 0] += accel * np.cos(kw * pos[:, 1])
        c[:, 0] -= 0.5 * dt * gdot * c[:, 1]
        c += 0.5 * dt * F
        dr = dt * c
        pos[:, 0] += gdot * dt * pos[:, 1]
        pos += dr; na += dr
        strain += gdot * dt; shift = (strain % 1.0) * L
        wrap_le(pos, L, shift)   # peculiar velocity is unchanged across LE images
        if 2 * np.sqrt(np.max(np.sum(na * na, 1))) + (strain - strain_b) * (2 * R_LARGE + SKIN) > SKIN:
            nl.build(pos, L, shift); na[:] = 0.0; strain_b = strain
        F, Wxy, Wtr, nc, _ = contact_forces(pos, nl, L, shift, n, cvel=c, gdot=gdot, b=b)
        if accel is not None:
            Fa = F.copy(); Fa[:, 0] += accel * np.cos(kw * pos[:, 1])
        else:
            Fa = F
        c += 0.5 * dt * Fa
        c[:, 0] -= 0.5 * dt * gdot * c[:, 1]
        if T is not None:
            if accel is None:
                c -= c.mean(0)
                c *= np.sqrt(T * (n - 1) / (0.5 * np.sum(c * c)))
            else:  # profile-unbiased: rescale only the part off the cos/sin profile
                cy, sy = np.cos(kw * pos[:, 1]), np.sin(kw * pos[:, 1])
                Vc = 2 * np.mean(c[:, 0] * cy); Vs = 2 * np.mean(c[:, 0] * sy)
                prof = Vc * cy + Vs * sy
                u = c.copy(); u[:, 0] -= prof
                u -= u.mean(0)
                u *= np.sqrt(T * (n - 1) / (0.5 * np.sum(u * u)))
                c = u; c[:, 0] += prof
        if s >= ntr and (s - ntr) % sample_every == 0:
            if accel is None:
                Pxy = (np.sum(c[:, 0] * c[:, 1]) + Wxy) / A
                out.append(-Pxy)
            else:
                out.append(2 * np.mean(c[:, 0] * np.cos(kw * pos[:, 1])))
            Zs.append(2.0 * nc / n)
    return np.array(out), float(np.mean(Zs)), c


def run_thermal(args):
    kind, val, idx = args            # kind: 'nemd' (val = gdot) or 'pp' (val = A)
    rng = np.random.default_rng(SEED * 1000 + 500 + idx)
    phi, T, dt = 0.70, 0.01, 0.05
    pos, rad, L = make_system(N, phi, rng)
    nl = NList(rad); nl.build(pos, L, 0.0)
    relax(pos, rad, L, nl, N)
    c = rng.normal(0, np.sqrt(T), (N, 2))
    t_eq, t_tr, t_ms = (50, 50, 300) if QUICK else (500, 500, 5000)
    _, _, c = sllod(pos, c, rad, L, nl, N, 0.0, dt, int(t_eq / dt), int(t_eq / dt), T=T)
    rho = N / (L * L); kw = 2 * np.pi / L
    if kind == "nemd":
        x, z, _ = sllod(pos, c, rad, L, nl, N, val, dt, int((t_tr + t_ms) / dt), int(t_tr / dt), T=T)
        s, se = blocks(x)
        return dict(route="NEMD", gdot=val, sigma=s, sigma_err=se, eta=s / val, eta_err=se / val, z=z)
    x, z, _ = sllod(pos, c, rad, L, nl, N, 0.0, dt, int((t_tr + t_ms) / dt), int(t_tr / dt), T=T, accel=val)
    V, Ve = blocks(x)
    eta = rho * val / (V * kw * kw)
    return dict(route="PP", A=val, V=V, V_err=Ve, eta=eta, eta_err=eta * Ve / V, k=kw, rho=rho,
                max_shear_rate=V * kw, z=z)


def run_bagnold(args):
    gdot, idx = args
    rng = np.random.default_rng(SEED * 1000 + 900 + idx)
    pos, rad, L = make_system(N, 0.75, rng)
    nl = NList(rad); nl.build(pos, L, 0.0)
    relax(pos, rad, L, nl, N)
    c = np.zeros((N, 2)); dt = 0.05
    tr, ms = (0.2, 0.3) if QUICK else (1.0, 2.0)
    nst = int(round((tr + ms) / (gdot * dt))); ntr = int(round(tr / (gdot * dt)))
    x, z, _ = sllod(pos, c, rad, L, nl, N, gdot, dt, nst, ntr, T=None, b=1.0,
                    sample_every=max(1, (nst - ntr) // 2000))
    s, se = blocks(x)
    return dict(gdot=gdot, sigma=s, sigma_err=se, z=z)


# ---------------------------------------------------------------- analysis
def powerfit(x, y):
    p = np.polyfit(np.log(x), np.log(y), 1)
    return float(p[0])


def hb_fit(g, s):
    """sigma = sy + K g^n ; grid over n, linear LSQ for (sy, K); SE of sy from residuals."""
    best = None
    for n in np.linspace(0.05, 1.5, 291):
        X = np.column_stack([np.ones_like(g), g ** n])
        coef, *_ = np.linalg.lstsq(X, s, rcond=None)
        r = s - X @ coef
        rss = float(r @ r)
        if best is None or rss < best[0]:
            best = (rss, n, coef, X)
    rss, n, coef, X = best
    dof = max(1, len(g) - 3)
    cov = rss / dof * np.linalg.inv(X.T @ X)
    return dict(sigma_y=float(coef[0]), sigma_y_se=float(np.sqrt(cov[0, 0])), K=float(coef[1]), n=float(n))


def div_fit(phi, eta):
    """eta = A (phic - phi)^-beta : grid over phic, linear fit in logs."""
    best = None
    for pc in np.linspace(max(phi) + 1e-3, 0.95, 2000):
        X = np.column_stack([np.ones_like(phi), np.log(pc - phi)])
        coef, *_ = np.linalg.lstsq(X, np.log(eta), rcond=None)
        r = np.log(eta) - X @ coef
        if best is None or r @ r < best[0]:
            best = (float(r @ r), pc, coef)
    return dict(phi_c=float(best[1]), beta=float(-best[2][1]), A=float(np.exp(best[2][0])), rss_log=best[0])


def main():
    t0 = time.time()
    pre = json.load(open(os.path.join(HERE, "PREREG.json")))
    A = pre["model_A_athermal_overdamped"]
    phis, rates = A["phi"], A["gdot"]
    tasksA = [(p, g, i) for i, (p, g) in enumerate((p, g) for p in phis for g in rates)]
    tasksA.sort(key=lambda t: t[1])  # slowest first
    B = [("nemd", g, i) for i, g in enumerate([0.002, 0.005, 0.01, 0.02])] + \
        [("pp", a, 10 + i) for i, a in enumerate([0.002, 0.004])]
    C = [(g, i) for i, g in enumerate(pre["model_C_control_inertial_athermal"]["gdot"])]
    with Pool(int(os.environ.get("NC1_PROCS", os.cpu_count() or 4))) as pool:
        ja = pool.map_async(run_overdamped, tasksA, chunksize=1)
        jb = pool.map_async(run_thermal, B, chunksize=1)
        jc = pool.map_async(run_bagnold, C, chunksize=1)
        resA, resB, resC = ja.get(), jb.get(), jc.get()
    resA.sort(key=lambda r: (r["phi"], r["gdot"]))

    def curve(phi):
        rr = sorted([r for r in resA if r["phi"] == phi], key=lambda r: r["gdot"])
        return np.array([r["gdot"] for r in rr]), np.array([r["sigma"] for r in rr]), rr

    table = {}
    for p in phis:
        g, s, rr = curve(p)
        pos = s > 0
        table[str(p)] = dict(
            n_low3=powerfit(g[:3], s[:3]) if np.all(s[:3] > 0) else None,
            n_loc_lowest=powerfit(g[:2], s[:2]) if np.all(s[:2] > 0) else None,
            eta_lowest=rr[0]["eta"], eta_2nd=rr[1]["eta"],
            z_lowest=rr[0]["z"], p_lowest=rr[0]["p"])

    # P1
    p1 = {}
    for p in [0.70, 0.75, 0.80]:
        t = table[str(p)]
        ok_n = t["n_low3"] is not None and abs(t["n_low3"] - 1) <= 0.10
        ok_eta = abs(t["eta_lowest"] / t["eta_2nd"] - 1) <= 0.20
        p1[str(p)] = dict(n=t["n_low3"], eta_ratio_low2=t["eta_lowest"] / t["eta_2nd"], pass_=bool(ok_n and ok_eta))
    P1 = all(v["pass_"] for v in p1.values())
    # P2
    ph2 = np.array([0.70, 0.75, 0.78, 0.80, 0.82])
    e2 = np.array([table[str(p)]["eta_lowest"] for p in ph2])
    mono = bool(np.all(np.diff(e2) > 0)); ratio = float(e2[-1] / e2[0])
    df = div_fit(ph2, e2)
    P2 = bool(mono and ratio >= 10 and 0.82 <= df["phi_c"] <= 0.88 and df["beta"] > 0)
    # P3
    p3 = {}
    for p in [0.85, 0.86]:
        g, s, _ = curve(p)
        hb = hb_fit(g, s)
        nl_ = table[str(p)]["n_loc_lowest"]
        p3[str(p)] = dict(n_loc_lowest=nl_, hb=hb,
                          pass_=bool(nl_ is not None and nl_ <= 0.5 and hb["sigma_y"] > 3 * hb["sigma_y_se"] and hb["sigma_y"] > 0))
    P3 = all(v["pass_"] for v in p3.values())
    # P4
    nemd = sorted([r for r in resB if r["route"] == "NEMD"], key=lambda r: r["gdot"])
    pp = [r for r in resB if r["route"] == "PP"]
    eta_nemd = float(np.mean([r["eta"] for r in nemd[:2]]))
    eta_pp = float(np.mean([r["eta"] for r in pp]))
    P4 = bool(abs(eta_nemd / eta_pp - 1) <= 0.20)
    # P5
    resC.sort(key=lambda r: r["gdot"])
    gC = np.array([r["gdot"] for r in resC]); sC = np.array([r["sigma"] for r in resC])
    nC = powerfit(gC, sC) if np.all(sC > 0) else None
    P5 = bool(nC is not None and 1.7 <= nC <= 2.3)

    result = dict(
        experiment="NC1_newtonian_closure", seed=SEED, N=N, quick=QUICK,
        runtime_s=round(time.time() - t0, 1),
        prereg_sha256=hashlib.sha256(open(os.path.join(HERE, "PREREG.json"), "rb").read()).hexdigest(),
        model_A_runs=resA, model_A_table=table,
        model_B_runs=resB, model_C_runs=resC,
        verdicts=dict(
            P1=dict(pass_=P1, per_phi=p1),
            P2=dict(pass_=P2, phi=ph2.tolist(), eta=e2.tolist(), monotone=mono, ratio_082_070=ratio, fit=df),
            P3=dict(pass_=P3, per_phi=p3),
            P4=dict(pass_=P4, eta_NEMD=eta_nemd, eta_PP=eta_pp, ratio=eta_nemd / eta_pp),
            P5=dict(pass_=P5, n=nC, gated=False)))
    out = os.path.join(HERE, "RESULT_quick.json" if QUICK else "RESULT.json")
    json.dump(result, open(out, "w"), indent=1, default=float)
    print(json.dumps(result["verdicts"], indent=1, default=float))
    for p in phis:
        print(p, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in table[str(p)].items()})
    print("B:", [(r["route"], r.get("gdot", r.get("A")), round(r["eta"], 3)) for r in resB])
    print("C:", [(r["gdot"], r["sigma"]) for r in resC])
    print("runtime", result["runtime_s"])


if __name__ == "__main__":
    main()
