"""
c3e1_run.py -- C3E1: does energy concentrated on a C3 three-sphere cluster leave to ONE side?

A dynamical, reduced 3-D test (see PREREG.json, written before this script was run).
Model: 3-D DEM of soft frictional spheres (translation + rotation), i.e. the lattice
itself, no continuum closure.  Energy is injected as SPIN on a cluster (triangle /
pair / single / 81-core) embedded in a jammed medium (perfect FCC, random jammed
packing, simple cubic).  The angular distribution of the energy flux leaving a
sphere of radius R_s around the cluster is measured and reduced to dipole /
quadrupole / lobe statistics.  Everything below is fixed by PREREG.json; nothing
is tuned.  SEED = 19.

Run:  python3 c3e1_run.py        (~10 min on 4 cores, numpy + scipy)
Writes RESULT.json and c3e1_run.out.txt next to this file.
"""
import json, time, sys, os
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 19
# ---- fixed model constants (PREREG.json "model") -------------------------------
D = 1.0; RAD = 0.5; M = 1.0; INER = 0.4 * M * RAD**2
KN, GN, GT, MU = 1.0, 0.05, 0.5, 0.5
DT = 0.02; CUT = 1.2; REBUILD = 25
OMEGA = 0.2 / RAD            # |omega| * d/2 = 0.2
RS_MAIN = 3.0; RS_ALT = 4.5; TW = 10.0

OUT = []
def log(s=""):
    print(s); OUT.append(s); sys.stdout.flush()

# ---- direction bins -------------------------------------------------------------
def fibonacci(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5**0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
BINS = fibonacci(400)
CONE = np.cos(np.radians(60.0))

# ---- contact forces -----------------------------------------------------------
def pairs_of(x, L):
    xm = np.mod(x, L); xm[xm >= L] = 0.0
    return cKDTree(xm, boxsize=L).query_pairs(CUT, output_type="ndarray")

def cross(a, b):
    return np.stack([a[:, 1]*b[:, 2]-a[:, 2]*b[:, 1], a[:, 2]*b[:, 0]-a[:, 0]*b[:, 2], a[:, 0]*b[:, 1]-a[:, 1]*b[:, 0]], 1)

def dot(a, b): return (a * b).sum(1)

def contact(x, v, w, pr, L):
    i, j = pr[:, 0], pr[:, 1]
    dr = x[j] - x[i]; dr -= L * np.round(dr / L)
    dist = np.sqrt(dot(dr, dr)); dl = 2 * RAD - dist
    on = dl > 0
    i, j, dr, dist, dl = i[on], j[on], dr[on], dist[on], dl[on]
    n = dr / dist[:, None]
    vs = (v[j] - v[i]) - RAD * cross(w[i] + w[j], n)   # contact-point velocity of j minus that of i
    vn = dot(vs, n)
    fn = np.maximum(KN * dl - GN * vn, 0.0)       # normal force on j along +n
    vt = vs - vn[:, None] * n
    ft = -GT * vt                                 # tangential force on j (viscous-Coulomb)
    fm = np.sqrt(dot(ft, ft)); cap = MU * fn
    sc = np.where(fm > cap, cap / np.maximum(fm, 1e-300), 1.0)
    ft *= sc[:, None]
    Fj = fn[:, None] * n + ft
    tj = -RAD * cross(n, ft); ti = tj.copy()      # torque on j: (-R n) x ft ; on i: (R n) x (-ft) = same
    # dissipation rate: -( (fn - k dl) vn + ft.vt )  (>= 0)
    pdiss = -((fn - KN * dl) * vn + dot(ft, vt))
    return i, j, n, dl, Fj, tj, ti, pdiss

def scatter(idx_pos, idx_neg, val, N):
    out = np.empty((N, 3))
    for k in range(3):
        out[:, k] = np.bincount(idx_pos, val[:, k], N) - np.bincount(idx_neg, val[:, k], N)
    return out

def accel(x, v, w, pr, L):
    c = contact(x, v, w, pr, L)
    i, j, n, dl, Fj, tj, ti, pdiss = c
    N = len(x)
    F = scatter(j, i, Fj, N)
    T = np.empty((N, 3))
    for k in range(3):
        T[:, k] = np.bincount(j, tj[:, k], N) + np.bincount(i, ti[:, k], N)
    return F / M, T / INER, c

# ---- media ----------------------------------------------------------------------
def fcc(nc=12, nn=0.98):
    a = nn * np.sqrt(2.0)
    b = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]])
    g = np.array([[i, j, k] for i in range(nc) for j in range(nc) for k in range(nc)], float)
    x = ((g[:, None, :] + b[None]) * a).reshape(-1, 3)
    return x, nc * a

def sc(nc=16, s=0.98):
    g = np.array([[i, j, k] for i in range(nc) for j in range(nc) for k in range(nc)], float)
    return g * s, nc * s

def fire_min(x, L, ftol=1e-10, maxit=200000):
    """frictionless harmonic energy minimisation (FIRE)."""
    N = len(x); v = np.zeros_like(x); dt, dtmax = 0.05, 0.5; a = 0.1; np_ = 0
    pr = pairs_of(x, L); it0 = 0
    for it in range(maxit):
        if it - it0 >= 20: pr = pairs_of(x, L); it0 = it
        i, j = pr[:, 0], pr[:, 1]
        dr = x[j] - x[i]; dr -= L * np.round(dr / L); d = np.linalg.norm(dr, axis=1)
        dl = np.maximum(2 * RAD - d, 0); f = (KN * dl / np.maximum(d, 1e-12))[:, None] * dr
        F = np.zeros_like(x); np.add.at(F, j, f); np.add.at(F, i, -f)
        fmax = np.abs(F).max()
        if fmax < ftol: break
        P = np.sum(F * v)
        if P > 0:
            vn = np.linalg.norm(v); Fn = np.linalg.norm(F)
            v = (1 - a) * v + a * F / Fn * vn; np_ += 1
            if np_ > 5: dt = min(dt * 1.1, dtmax); a *= 0.99
        else:
            v[:] = 0; dt *= 0.5; a = 0.1; np_ = 0
        v += dt * F; x = x + dt * v
    return np.mod(x, L), fmax, it

def rcp(N, phi, rng):
    L = (N * (np.pi / 6) / phi) ** (1 / 3)
    x = rng.random((N, 3)) * L
    x, fmax, it = fire_min(x, L)
    return x, L, fmax, it

# ---- simulation -----------------------------------------------------------------
def run(x0, L, spins, cen, T=TW, rs=(RS_MAIN, RS_ALT), late=None, frame=None):
    """spins: {index: omega vector}. Returns flux statistics per R_s.
    late: (t0, t1) window for the late-time KE dipole (closed-box test)."""
    x = x0.copy(); N = len(x)
    v = np.zeros((N, 3)); w = np.zeros((N, 3))
    for k, om in spins.items(): w[k] = om
    E0 = sum(0.5 * INER * np.dot(om, om) for om in spins.values())
    p0 = M * OMEGA * RAD
    pr = pairs_of(x, L)
    a, al, c = accel(x, v, w, pr, L)
    U0 = 0.5 * KN * np.sum(c[3] ** 2)
    acc = {r: dict(bins=np.zeros(len(BINS)), vec=np.zeros(3), Q=np.zeros((3, 3)), tot=0.0) for r in rs}
    ediss = 0.0; nst = int(round(T / DT)); maxP = 0.0; late_ke = np.zeros(len(BINS)); late_vec = np.zeros(3); late_tot = 0.0
    maxbal = 0.0
    for s in range(1, nst + 1):
        t = s * DT
        v += 0.5 * DT * a; w += 0.5 * DT * al
        x += DT * v
        if s % REBUILD == 0: pr = pairs_of(x, L)
        if s % REBUILD == 1 or s == 1:
            dp = x - cen; dp -= L * np.round(dp / L); dp = np.sqrt(dot(dp, dp))
            near = np.zeros(N, bool)
            for r in rs: near |= np.abs(dp - r) < 1.5
        a, al, c = accel(x, v, w, pr, L)
        v += 0.5 * DT * a; w += 0.5 * DT * al
        i, j, n, dl, Fj, tj, ti, pdiss = c
        ediss += DT * pdiss.sum()
        if t <= TW + 1e-9:
            sel = near[i] | near[j]
            i, j, Fj, tj, ti = i[sel], j[sel], Fj[sel], tj[sel], ti[sel]
            ri = x[i] - cen; ri -= L * np.round(ri / L)
            rj = x[j] - cen; rj -= L * np.round(rj / L)
            di = np.linalg.norm(ri, axis=1); dj = np.linalg.norm(rj, axis=1)
            Pj = dot(Fj, v[j]) + dot(tj, w[j])
            Pi = -dot(Fj, v[i]) + dot(ti, w[i])
            for r, A in acc.items():
                out_j = (di < r) & (dj >= r); out_i = (dj < r) & (di >= r)
                fl = np.concatenate([0.5 * (Pj - Pi)[out_j], 0.5 * (Pi - Pj)[out_i]])
                pc = np.concatenate([(0.5 * (ri + rj))[out_j], (0.5 * (ri + rj))[out_i]])
                if len(fl) == 0: continue
                u = pc / np.linalg.norm(pc, axis=1)[:, None]
                b = np.argmax(u @ BINS.T, axis=1)
                np.add.at(A["bins"], b, fl * DT)
                A["vec"] += (fl[:, None] * u).sum(0) * DT
                A["Q"] += np.einsum("k,ki,kj->ij", fl, u, u) * DT - np.eye(3) * fl.sum() * DT / 3
                A["tot"] += fl.sum() * DT
        if s % 50 == 0 or s == nst:
            P = M * v.sum(0); maxP = max(maxP, np.linalg.norm(P) / p0)
            ke = 0.5 * M * np.sum(v * v) + 0.5 * INER * np.sum(w * w)
            U = 0.5 * KN * np.sum(c[3] ** 2)
            maxbal = max(maxbal, abs(ke + (U - U0) + ediss - E0) / E0)
            if late and late[0] <= t <= late[1]:
                sp = set(spins.keys())
                msk = np.ones(N, bool); msk[list(sp)] = False
                r = x[msk] - cen; r -= L * np.round(r / L); dd = np.linalg.norm(r, axis=1)
                kk = 0.5 * M * np.sum(v[msk] ** 2, 1) + 0.5 * INER * np.sum(w[msk] ** 2, 1)
                sel = dd > 1.5; u = r[sel] / dd[sel][:, None]
                late_vec += (kk[sel][:, None] * u).sum(0); late_tot += kk[sel].sum()
    ke = 0.5 * M * np.sum(v * v) + 0.5 * INER * np.sum(w * w)
    ke_cl = sum(0.5 * M * v[k] @ v[k] + 0.5 * INER * w[k] @ w[k] for k in spins)
    res = dict(E0=E0, frac_dissipated=ediss / E0, frac_ke_cluster_end=ke_cl / E0,
               max_momentum_rel=maxP, max_energy_balance_err=maxbal, stats={})
    for r, A in acc.items():
        res["stats"][str(r)] = stats(A, frame)
    if late:
        res["late_ke_dipole"] = float(np.linalg.norm(late_vec) / late_tot) if late_tot > 0 else None
    return res

def stats(A, frame):
    tot = A["tot"]; bins = A["bins"]; pos = np.maximum(bins, 0); ps = pos.sum()
    cosm = BINS @ BINS.T
    cone = (cosm >= CONE).astype(float) @ pos
    k = int(np.argmax(cone)); nmax = BINS[k]
    kopp = int(np.argmax(BINS @ -nmax))
    f_lobe = cone[k] / ps; bip = cone[kopp] / cone[k]
    D = np.linalg.norm(A["vec"]) / tot if tot > 0 else float("nan")
    q = 1.5 * np.linalg.eigvalsh(A["Q"] / tot).max() if tot > 0 else float("nan")
    out = dict(total_out_flux=float(tot), D=float(D), q=float(q), f_lobe=float(f_lobe),
               bipolarity=float(bip), dipole_vec_lab=(A["vec"] / tot).tolist())
    # POST-HOC (not in PREREG; added after the first run showed net flux ~ 0 makes D ill-conditioned):
    gross = np.abs(bins).sum()
    out["posthoc_gross_flux"] = float(gross); out["posthoc_positive_flux"] = float(ps)
    out["posthoc_D_gross"] = float(np.linalg.norm(A["vec"]) / gross) if gross > 0 else float("nan")
    out["posthoc_vec_gross_lab"] = (A["vec"] / gross).tolist() if gross > 0 else [0.0, 0.0, 0.0]
    if frame is not None and gross > 0: out["posthoc_vec_gross_frame"] = (frame @ (A["vec"] / gross)).tolist()
    if frame is not None:
        out["dipole_vec_cluster_frame"] = (frame @ (A["vec"] / tot)).tolist()
        out["lobe_dir_cluster_frame"] = (frame @ nmax).tolist()
    return out

# ---- cluster helpers ------------------------------------------------------------
def pbc(d, L): return d - L * np.round(d / L)

def triangle_frame(x, tri, L):
    p = [x[tri[0]], x[tri[0]] + pbc(x[tri[1]] - x[tri[0]], L), x[tri[0]] + pbc(x[tri[2]] - x[tri[0]], L)]
    cen = (p[0] + p[1] + p[2]) / 3
    nz = np.cross(p[1] - p[0], p[2] - p[0]); nz /= np.linalg.norm(nz)
    ex = p[1] - cen; ex -= (ex @ nz) * nz; ex /= np.linalg.norm(ex)
    ey = np.cross(nz, ex)
    return np.mod(cen, L), nz, np.stack([ex, ey, nz]), p

def configs(x, tri, L, rng):
    """the five PREREG configurations at one triangle site; returns list of (name, spins, cen, frame)."""
    cen, nz, fr, p = triangle_frame(x, tri, L)
    a, b, c = tri                      # b is 'sphere 2' (the odd one in T+-+); frustrated edge = a-c
    out = [("T+++", {a: OMEGA * nz, b: OMEGA * nz, c: OMEGA * nz}, cen, fr),
           ("T+-+", {a: OMEGA * nz, b: -OMEGA * nz, c: OMEGA * nz}, cen, fr)]
    # pair a-b : spin axis random perpendicular to bond
    bond = p[1] - p[0]; bond /= np.linalg.norm(bond)
    r = rng.standard_normal(3); r -= (r @ bond) * bond; r /= np.linalg.norm(r)
    pc = np.mod((p[0] + p[1]) / 2, L); pfr = np.stack([bond, np.cross(r, bond), r])
    out += [("P++", {a: OMEGA * r, b: OMEGA * r}, pc, pfr),
            ("P+-", {a: OMEGA * r, b: -OMEGA * r}, pc, pfr)]
    s = rng.standard_normal(3); s /= np.linalg.norm(s)
    e1 = np.cross(s, [1.0, 0, 0]); e1 /= np.linalg.norm(e1)
    out += [("S", {a: OMEGA * s}, np.mod(p[0], L), np.stack([e1, np.cross(s, e1), s]))]
    return out

def find_triangles(x, L, k, rng, minsep=4.0):
    pr = pairs_of(x, L)
    d = np.linalg.norm(pbc(x[pr[:, 1]] - x[pr[:, 0]], L), axis=1)
    pr = pr[d < 2 * RAD]
    nb = [set() for _ in range(len(x))]
    for i, j in pr: nb[i].add(j); nb[j].add(i)
    order = rng.permutation(len(x)); tris = []; cens = []
    for i in order:
        lst = sorted(nb[i])
        found = None
        for jj in lst:
            for kk in lst:
                if kk > jj and kk in nb[jj]: found = (i, jj, kk); break
            if found: break
        if not found: continue
        cen = triangle_frame(x, found, L)[0]
        if all(np.linalg.norm(pbc(cen - c, L)) > minsep for c in cens):
            tris.append(found); cens.append(cen)
        if len(tris) == k: break
    return tris

# ---- main -----------------------------------------------------------------------
def _job(args):
    key, x, L, spins, cen, frame, T, late = args
    t0 = time.time(); r = run(x, L, spins, cen, T=T, late=late, frame=frame); r["wall_s"] = time.time() - t0
    return key, r

def _rcp_job(args):
    k, seed = args
    t0 = time.time(); x, L, fmax, it = rcp(4000, 0.66, np.random.default_rng(seed))
    return k, x, L, fmax, it, time.time() - t0

def main():
    from multiprocessing import Pool
    t00 = time.time(); rng = np.random.default_rng(SEED); R = {"prereg": "PREREG.json", "seed": SEED}
    log("C3E1 three-sphere directed ejection -- DEM, 3-D, spin injection, closed periodic box")
    log(f"constants: k_n={KN} g_n={GN} g_t={GT} mu={MU} dt={DT} |omega|R={OMEGA*RAD} R_s={RS_MAIN} (alt {RS_ALT}) T_w={TW}")
    pool = Pool(4); jobs = []

    # ---------------- medium A : FCC ----------------
    x, L = fcc(); N = len(x)
    c0 = np.array([L / 2] * 3); i0 = int(np.argmin(np.linalg.norm(x - c0, axis=1)))
    nz = np.array([1.0, 1, 1]) / np.sqrt(3)
    dd = pbc(x - x[i0], L); dist = np.linalg.norm(dd, axis=1)
    nbrs = np.where((dist > 0.1) & (dist < 1.0))[0]
    inpl = [k for k in nbrs if abs(dd[k] @ nz) < 1e-6]
    tri = None
    for a_ in inpl:
        for b_ in inpl:
            if b_ > a_ and abs(np.linalg.norm(pbc(x[a_] - x[b_], L)) - 0.98) < 1e-6: tri = (i0, int(a_), int(b_)); break
        if tri: break
    cen, nzt, fr, p = triangle_frame(x, tri, L)
    dc = pbc(x - cen, L); h = dc @ nzt; rr = np.linalg.norm(dc - h[:, None] * nzt, axis=1)
    cap_side = [float(np.sign(h[k])) for k in range(N) if rr[k] < 1e-6 and 0.1 < abs(h[k]) < 1.0]
    log(f"\n[A] FCC N={N} L={L:.3f}; (111) triangle {tri}; normal {np.round(nzt,3)}; tetrahedral CAP sphere on side {cap_side} of the normal, octahedral HOLE on the other")
    RA = {"N": N, "L": L, "triangle": list(tri), "cap_side_sign_along_normal": cap_side}
    cA = configs(x, tri, L, np.random.default_rng(SEED + 1))
    jobs.append((("A", "P5"), x, L, cA[0][1], cen, fr, 200.0, (150.0, 200.0)))   # longest first
    for name, spins, cc, frm in cA:
        jobs.append((("A", name), x, L, spins, cc, frm, TW, None))

    # ---------------- medium C : SC 81-core ----------------
    xs, Ls = sc(); c0s = np.array([8 * 0.98] * 3)
    g = np.round((xs - c0s) / 0.98).astype(int); r2 = (g ** 2).sum(1)
    core = np.where(r2 <= 6)[0]
    RC = {"core_size": int(len(core)), "R2_eq_7_count": int(np.sum(r2 == 7))}
    zax = np.array([0, 0, 1.0])
    for eps in (0.0, 1e-6, 1e-4):
        xe = xs + eps * np.random.default_rng(SEED + 7).standard_normal(xs.shape)
        for nm in ("C81co", "C81chk", "noinj"):
            if nm == "C81co": spins = {int(k): OMEGA * zax for k in core}
            elif nm == "C81chk": spins = {int(k): OMEGA * zax * (1 if (g[k].sum() % 2 == 0) else -1) for k in core}
            else: spins = {int(core[0]): 1e-12 * zax}
            jobs.append((("C", f"{nm}@eps={eps:.0e}"), xe, Ls, spins, c0s, np.eye(3), TW, None))
    asyncA = pool.map_async(_job, jobs)

    # ---------------- medium B : RCP (packings first) ----------------
    names = ["T+++", "T+-+", "P++", "P+-", "S"]
    packs = pool.map(_rcp_job, [(0, SEED + 100), (1, SEED + 101)])
    RB = {"packings": [], "runs": {nm: [] for nm in names}, "sites": []}
    jobsB = []
    for k, xb, Lb, fmax, it, wall in packs:
        pr = pairs_of(xb, Lb); dl = 2 * RAD - np.linalg.norm(pbc(xb[pr[:, 1]] - xb[pr[:, 0]], Lb), axis=1)
        z = 2 * np.sum(dl > 0) / len(xb)
        log(f"\n[B] RCP packing {k}: N=4000 L={Lb:.3f} FIRE its={it} residual |F|max={fmax:.1e} z={z:.2f} mean overlap={dl[dl>0].mean():.4f} ({wall:.0f}s)")
        RB["packings"].append(dict(L=Lb, fire_its=it, residual_fmax=fmax, z=float(z), mean_overlap=float(dl[dl > 0].mean())))
        for s_, tr in enumerate(find_triangles(xb, Lb, 6, rng)):
            RB["sites"].append([k, [int(t) for t in tr]])
            for name, spins, cc, frm in configs(xb, tr, Lb, rng):
                jobsB.append((("B", name, k, s_), xb, Lb, spins, cc, frm, TW, None))
    resB = pool.map(_job, jobsB)
    resA = dict(asyncA.get()); pool.close()

    for name in ["T+++", "T+-+", "P++", "P+-", "S"]:
        r = resA[("A", name)]; st = r["stats"][str(RS_MAIN)]
        r["angle_to_111_deg"] = float(np.degrees(np.arccos(min(1.0, abs(st["dipole_vec_cluster_frame"][2]) / max(st["D"], 1e-300)))))
        log(f"  {name:5s} D={st['D']:.4f} q={st['q']:.3f} f_lobe={st['f_lobe']:.3f} bip={st['bipolarity']:.3f} "
            f"dip(frame x',y',normal)={np.round(st['dipole_vec_cluster_frame'],4)} out/E0={st['total_out_flux']/r['E0']:.3f} "
            f"diss/E0={r['frac_dissipated']:.3f} bal={r['max_energy_balance_err']:.1e} || post-hoc gross/E0={st['posthoc_gross_flux']/r['E0']:.4f} "
            f"D_gross={st['posthoc_D_gross']:.4f} vec_gross(frame)={np.round(st.get('posthoc_vec_gross_frame',[0,0,0]),4)}")
        RA[name] = r
    r5 = resA[("A", "P5")]; RA["P5_long"] = r5
    log(f"  [P5] T+++ FCC to t=200: max|P|/p0={r5['max_momentum_rel']:.2e} balance err={r5['max_energy_balance_err']:.2e} "
        f"dissipated={r5['frac_dissipated']:.3f} cluster KE left={r5['frac_ke_cluster_end']:.3f} late KE dipole={r5['late_ke_dipole']:.4f} ({r5['wall_s']:.0f}s)")
    R["A_FCC"] = RA

    for key, r in sorted(resB, key=lambda kr: (kr[0][2], kr[0][3])):
        RB["runs"][key[1]].append(r)
    summ = {}
    for nm in names:
        for rs in (RS_MAIN, RS_ALT):
            S = [r["stats"][str(rs)] for r in RB["runs"][nm]]
            vec = np.mean([np.array(s["dipole_vec_cluster_frame"]) * s["total_out_flux"] for s in S], 0)
            tot = np.mean([s["total_out_flux"] for s in S])
            vecs = np.array([np.array(s["dipole_vec_cluster_frame"]) * s["total_out_flux"] for s in S]) / tot
            summ[f"{nm}@{rs}"] = dict(D_sys=float(np.linalg.norm(vec) / tot), D_sys_vec_frame=(vec / tot).tolist(),
                                      noise_floor_Dsys=float(np.linalg.norm(vecs.std(0, ddof=1)) / np.sqrt(len(S))),
                                      D_run_mean=float(np.mean([s["D"] for s in S])),
                                      D_run_sem=float(np.std([s["D"] for s in S], ddof=1) / np.sqrt(len(S))),
                                      f_lobe_mean=float(np.mean([s["f_lobe"] for s in S])),
                                      bip_mean=float(np.mean([s["bipolarity"] for s in S])),
                                      q_mean=float(np.mean([s["q"] for s in S])),
                                      out_over_E0_mean=float(np.mean([r["stats"][str(rs)]["total_out_flux"] / r["E0"] for r in RB["runs"][nm]])),
                                      n=len(S),
                                      posthoc_D_gross_run_mean=float(np.mean([s["posthoc_D_gross"] for s in S])),
                                      posthoc_D_sys_gross=float(np.linalg.norm(np.mean([np.array(s["posthoc_vec_gross_frame"]) * s["posthoc_gross_flux"] for s in S], 0)) / np.mean([s["posthoc_gross_flux"] for s in S])),
                                      posthoc_gross_over_E0_mean=float(np.mean([r["stats"][str(rs)]["posthoc_gross_flux"] / r["E0"] for r in RB["runs"][nm]])),
                                      posthoc_net_over_gross_mean=float(np.mean([s["total_out_flux"] / s["posthoc_gross_flux"] for s in S])),
                                      posthoc_frac_dissipated_mean=float(np.mean([r["frac_dissipated"] for r in RB["runs"][nm]])))
    RB["summary"] = summ
    log("\n[B] summary over 12 sites (cluster-frame averaged)   R_s=3  |  R_s=4.5")
    for nm in names:
        a_, b_ = summ[f"{nm}@{RS_MAIN}"], summ[f"{nm}@{RS_ALT}"]
        log(f"  {nm:5s} D_sys={a_['D_sys']:.3f} (1-sigma floor {a_['noise_floor_Dsys']:.3f}) D_run={a_['D_run_mean']:.3f}+-{a_['D_run_sem']:.3f} "
            f"f_lobe={a_['f_lobe_mean']:.3f} bip={a_['bip_mean']:.3f} q={a_['q_mean']:.3f} out/E0={a_['out_over_E0_mean']:.3f} "
            f"| D_sys={b_['D_sys']:.3f} D_run={b_['D_run_mean']:.3f}  vec(x',y',z')={np.round(a_['D_sys_vec_frame'],3)}")
    log("  POST-HOC (not preregistered): normalise by GROSS |flux| (net/gross ~ 0 makes the PREREG D ill-conditioned)")
    for nm in names:
        a_ = summ[f"{nm}@{RS_MAIN}"]
        log(f"  {nm:5s} gross/E0={a_['posthoc_gross_over_E0_mean']:.4f} net/gross={a_['posthoc_net_over_gross_mean']:+.3f} "
            f"D_gross(run mean)={a_['posthoc_D_gross_run_mean']:.3f} D_sys_gross={a_['posthoc_D_sys_gross']:.3f} diss/E0(t=10)={a_['posthoc_frac_dissipated_mean']:.4f}")
    R["B_RCP"] = RB

    log(f"\n[C] SC N={len(xs)}; 81-core size={len(core)} (R^2=7 shell count={RC['R2_eq_7_count']})")
    for eps in (0.0, 1e-6, 1e-4):
        for nm in ("C81co", "C81chk", "noinj"):
            k = f"{nm}@eps={eps:.0e}"; r = resA[("C", k)]; RC[k] = r; st = r["stats"][str(RS_MAIN)]; st2 = r["stats"][str(RS_ALT)]
            if nm == "noinj":
                log(f"  eps={eps:.0e} {nm:6s} out flux (no injection; medium self-motion)={st['total_out_flux']:.2e}")
            else:
                log(f"  eps={eps:.0e} {nm:6s} D={st['D']:.2e} q={st['q']:.3f} f_lobe={st['f_lobe']:.3f} bip={st['bipolarity']:.3f} "
                    f"| R_s=4.5 D={st2['D']:.2e}  out/E0={st['total_out_flux']/r['E0']:.3f} diss/E0={r['frac_dissipated']:.3f} || post-hoc D_gross={st['posthoc_D_gross']:.2e} gross/E0={st['posthoc_gross_flux']/r['E0']:.3f}")
    R["C_SC81"] = RC

    # ---------------- verdicts (exactly as PREREG) ----------------
    s3 = lambda nm: summ[f"{nm}@{RS_MAIN}"]
    V = {}
    V["P1_triangle_one_lobe_RCP"] = bool(s3("T+++")["D_sys"] >= 0.25 and s3("T+++")["f_lobe_mean"] >= 0.45 and s3("T+++")["bip_mean"] <= 0.5)
    ctrl = max(s3(n)["D_sys"] for n in ("P++", "P+-", "S"))
    V["P2_controls_not_directed_RCP"] = bool(all(s3(n)["D_sys"] <= 0.10 for n in ("P++", "P+-", "S")) and s3("T+++")["D_sys"] >= 2 * ctrl)
    A3 = RA["T+++"]["stats"][str(RS_MAIN)]
    V["P3_triangle_one_lobe_FCC"] = bool(A3["D"] >= 0.25 and RA["T+++"]["angle_to_111_deg"] <= 20
                                         and RA["S"]["stats"][str(RS_MAIN)]["D"] <= 0.02 and RA["P++"]["stats"][str(RS_MAIN)]["D"] <= 0.02)
    V["P4_nozzle_contact"] = bool(s3("T+-+")["D_sys"] > s3("T+++")["D_sys"])
    parts = dict(momentum=bool(r5["max_momentum_rel"] < 1e-8), balance=bool(r5["max_energy_balance_err"] < 1e-3),
                 late_dipole=bool(r5["late_ke_dipole"] <= 0.10), dissipated_ge_half=bool(r5["frac_dissipated"] >= 0.5))
    V["P5_closed_box_annihilation"] = all(parts.values()); V["P5_parts"] = parts
    c1 = RC["C81co@eps=1e-04"]["stats"][str(RS_MAIN)]["D"]; c2 = RC["C81chk@eps=1e-04"]["stats"][str(RS_MAIN)]["D"]
    V["P6_81core_spontaneous_lobe"] = bool(c1 >= 0.25 and c2 <= 0.10)
    R["verdicts"] = V
    log("\nVERDICTS: " + json.dumps(V))
    log(f"total wall time {time.time()-t00:.0f}s")
    with open(os.path.join(HERE, "RESULT.json"), "w") as f:
        json.dump(R, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if np.isscalar(o) else str(o)))
    with open(os.path.join(HERE, "c3e1_run.out.txt"), "w") as f:
        f.write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
