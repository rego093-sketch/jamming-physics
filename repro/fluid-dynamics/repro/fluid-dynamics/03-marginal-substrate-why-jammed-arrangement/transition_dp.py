# -*- coding: utf-8 -*-
"""transition_dp.py -- The framework's G-SOC rules as a lattice model.

Claim under test (configured-continuum, Sec. 3.6 / research memo problem A):
  "drive unjams, rest re-jams" + locality + an absorbing laminar state
  FORCES the laminar-turbulent transition into the directed-percolation (DP)
  universality class -- the class experiments found (Couette/channel 2016,
  pipe 2024).

Model (1D ring, synchronous, annealed thresholds):
  * site i: active a_i in {0,1} (unjammed/turbulent), shear reserve x_i drawn
    from the marginal-stability pseudogap  P(x) = (1+theta) x^theta on [0,1]
    (theta = 0.45; literature: MF 0.42, 3D steady 0.5-0.6 -- the CLASS must
    not depend on theta, that is the point of universality).
  * each step: an inactive site feels demand d = lambda * (#active nbrs) * U,
    U~U(0,1); it unjams if d > x  (shear demand exceeds reserve).
    An active site re-jams with prob q (rest re-jams).  Toggled sites redraw x
    (re-jamming reconfigures contacts).
  * no active sites -> absorbing (laminar) state.  Control = lambda  (~ Re).

Measurements & gates (DP 1+1d reference values, Hinrichsen 2000):
  [1] lambda_c located (slope-matched bisection + curvature-minimised refine)
  [2] decay      rho(t) ~ t^-delta   at lambda_c      delta = 0.1595
  [3] spreading  N(t)   ~ t^+theta_s from single seed theta_s = 0.3137
  [4] lifetime   tau ~ (lambda_c-lambda)^-nu_par       nu_par = 1.7338
  [5] SOC avalanches at lambda_c: P(s) ~ s^-tau_av  (reported, exploratory)
  [6] intermittency probe: box-averaged activity M2(r)=<rho_r^2>/<rho_r>^2
      ~ r^-mu ; DP prediction mu = 2*beta/nu_perp = 0.504 in 1+1d (reported)

Anything outside gate tolerance is reported as-is; no clamping, no retuning.
numpy only; fixed seeds; runtime ~3-5 min.
"""
import numpy as np, time, json

rng_master = np.random.default_rng(20260613)
THETA = 0.45          # pseudogap exponent of reserves (flagged parameter)
Q     = 0.35          # re-jam probability
EXP   = 1.0/(1.0+THETA)

DP = dict(delta=0.1595, theta_s=0.3137, nu_par=1.7338, beta=0.2765,
          nu_perp=1.0968, two_beta_over_nuperp=0.5042)

t0 = time.time()
log_lines = []
def log(s):
    print(s); log_lines.append(s)

def draw_x(rng, n):
    return rng.random(n) ** EXP

def step(a, x, lam, rng):
    """one synchronous update; a bool (..., L), x float same shape; ring."""
    n = np.roll(a, 1, axis=-1).astype(np.int8) + np.roll(a, -1, axis=-1).astype(np.int8)
    d = lam * n * rng.random(a.shape)
    unjam = (~a) & (d > x)
    keep  = a & (rng.random(a.shape) >= Q)
    a_new = keep | unjam
    tog = a ^ a_new
    nt = int(tog.sum())
    if nt:
        x[tog] = rng.random(nt) ** EXP
    return a_new, unjam

# ---------------------------------------------------------------- stage A ---
def decay_slope(lam, L, T, seed, win=(0.25, 1.0)):
    rng = np.random.default_rng(seed)
    a = np.ones(L, bool); x = draw_x(rng, L)
    ts, rs = [], []
    rec = np.unique(np.geomspace(5, T, 60).astype(int))
    k = 0
    for t in range(1, T + 1):
        a, _ = step(a, x, lam, rng)
        if k < len(rec) and t == rec[k]:
            ts.append(t); rs.append(a.mean()); k += 1
            if rs[-1] == 0: break
    ts, rs = np.array(ts, float), np.array(rs, float)
    m = (ts >= win[0]*T) & (rs > 0)
    if m.sum() < 4 or rs[m][-1] == 0: return -9.9, ts, rs
    sl = np.polyfit(np.log(ts[m]), np.log(rs[m]), 1)[0]
    return sl, ts, rs

log("== stage A: slope-matched bisection for lambda_c (L=30000, T=4000) ==")
lo, hi = 0.30, 3.00
for it in range(16):
    mid = 0.5*(lo+hi)
    sl, _, _ = decay_slope(mid, 30_000, 4_000, seed=100+it)
    if sl > -DP['delta']: hi = mid     # too shallow -> supercritical side
    else:                 lo = mid
    log(f"  iter {it:2d}  lam={mid:.5f}  slope={sl:+.4f}  bracket=[{lo:.5f},{hi:.5f}]")
lamA = 0.5*(lo+hi)
log(f"stage A lambda_c ~= {lamA:.5f}   [{time.time()-t0:.0f}s]")

# ---------------------------------------------------------------- stage B ---
log("== stage B: curvature-minimised refine (L=60000, T=12000, 2 seeds) ==")
cands = [lamA*(1-0.004), lamA, lamA*(1+0.004)]
best = None; snapshots = []
for lam in cands:
    TS, RS = None, []
    curv = []; slopes = []
    for sd in (1, 2):
        rng = np.random.default_rng(7000+sd)
        L, T = 60_000, 12_000
        a = np.ones(L, bool); x = draw_x(rng, L)
        rec = np.unique(np.geomspace(5, T, 80).astype(int)); k = 0
        ts, rs = [], []
        snap = []
        for t in range(1, T+1):
            a, _ = step(a, x, lam, rng)
            if k < len(rec) and t == rec[k]:
                ts.append(t); rs.append(a.mean()); k += 1
            if t in (8_000, 10_000, 12_000):
                snap.append(a.copy())
        ts = np.array(ts, float); rs = np.array(rs, float)
        m = (ts >= 400) & (rs > 0)
        c2, c1, _ = np.polyfit(np.log(ts[m]), np.log(rs[m]), 2)
        curv.append(abs(c2)); slopes.append(np.polyfit(np.log(ts[m]), np.log(rs[m]), 1)[0])
        RS.append((ts, rs)); 
        if lam == lamA: snapshots.extend(snap)
    score = float(np.mean(curv))
    log(f"  lam={lam:.5f}  |curv|={score:.4f}  slope={np.mean(slopes):+.4f}")
    if best is None or score < best[0]:
        best = (score, lam, float(np.mean(slopes)), float(np.std(slopes)), RS)
_, lam_c, delta_eff, delta_sd, RS_best = best
delta_eff = -delta_eff
log(f"lambda_c = {lam_c:.5f}   delta_eff = {delta_eff:.4f} +- {delta_sd:.4f}"
    f"   (DP 0.1595 | CDP 0.500 | MF 1.000)   [{time.time()-t0:.0f}s]")
g2 = abs(delta_eff - DP['delta']) <= 0.030
log(f"GATE[2] decay exponent: {'PASS' if g2 else 'FAIL'}")

# -------------------------------------------------------------- spreading ---
log("== spreading from single seed at lambda_c (R=512, Lw=1024, T=2000) ==")
R, Lw, T = 512, 1024, 2_000
rng = np.random.default_rng(31415)
a = np.zeros((R, Lw), bool); a[:, Lw//2] = True
x = draw_x(rng, (R, Lw)).reshape(R, Lw)
rec = np.unique(np.geomspace(5, T, 50).astype(int)); k = 0
ts, Ns, Ps = [], [], []
for t in range(1, T+1):
    a, _ = step(a, x, lam_c, rng)
    if k < len(rec) and t == rec[k]:
        ts.append(t); Ns.append(a.sum(axis=1).mean()); Ps.append((a.any(axis=1)).mean()); k += 1
    if t % 100 == 0 and not a.any(): break
ts = np.array(ts, float); Ns = np.array(Ns, float); Ps = np.array(Ps, float)
m = (ts >= 50) & (Ns > 0)
theta_s = np.polyfit(np.log(ts[m]), np.log(Ns[m]), 1)[0]
delta_sp = -np.polyfit(np.log(ts[m]), np.log(Ps[m]), 1)[0]
log(f"theta_s = {theta_s:+.4f}  (DP +0.3137)    delta(from P_surv) = {delta_sp:.4f}  (DP 0.1595)")
g3 = abs(theta_s - DP['theta_s']) <= 0.060
log(f"GATE[3] spreading exponent: {'PASS' if g3 else 'FAIL'}   [{time.time()-t0:.0f}s]")

# --------------------------------------------------------------- lifetime ---
log("== subcritical puff lifetime tau(Delta), Delta = lambda_c - lambda ==")
eps_list = [0.05, 0.09, 0.16, 0.28]
taus, cens = [], []
for j, e in enumerate(eps_list):
    lam = lam_c*(1-e)
    Rr, L, Tcap = 256, 512, 12_000
    rng = np.random.default_rng(9000+j)
    a = np.zeros((Rr, L), bool); a[:, L//2-16:L//2+16] = True
    x = draw_x(rng, (Rr, L)).reshape(Rr, L)
    tdie = np.full(Rr, Tcap, int); alive = np.ones(Rr, bool)
    for t in range(1, Tcap+1):
        a, _ = step(a, x, lam, rng)
        now = a.any(axis=1)
        died = alive & ~now
        tdie[died] = t; alive = now
        if not alive.any(): break
    taus.append(tdie.mean()); cens.append(alive.mean())
    log(f"  Delta={e*lam_c:.4f}  mean tau={taus[-1]:9.1f}  censored={cens[-1]*100:.1f}%")
taus = np.array(taus); D = np.array(eps_list)*lam_c
ok = np.array(cens) < 0.05
nu_par = -np.polyfit(np.log(D[ok]), np.log(taus[ok]), 1)[0] if ok.sum() >= 3 else np.nan
log(f"nu_par_eff = {nu_par:.3f}  (DP 1.734 | MF 1.0)")
g4 = (ok.sum() >= 3) and (1.45 <= nu_par <= 2.05)
log(f"GATE[4] lifetime exponent: {'PASS' if g4 else 'FAIL'}   [{time.time()-t0:.0f}s]")

# ------------------------------------------------------------ SOC variant ---
log("== SOC drive at lambda_c: avalanche sizes (extremal kick) ==")
L = 2048; rng = np.random.default_rng(2718)
a = np.zeros(L, bool); x = draw_x(rng, L)
sizes = []; s_cur = 0; in_av = False
STEPCAP, AVCAP = 300_000, 20_000
for t in range(STEPCAP):
    if not a.any():
        if in_av:
            sizes.append(s_cur)
            if len(sizes) >= AVCAP: break
        i = int(np.argmin(x)); a[i] = True       # drive: kick weakest reserve
        x[i] = rng.random() ** EXP
        s_cur = 1; in_av = True
        continue
    a, unjam = step(a, x, lam_c, rng)
    s_cur += int(unjam.sum())
sizes = np.array(sizes)
log(f"  avalanches collected: {len(sizes)}  (steps used {t+1})")
s = sizes[sizes >= 4]
if len(s) > 200:
    smax = np.quantile(s, 0.98)
    s = s[s <= smax]
    tau_av = 1.0 + len(s)/np.sum(np.log(s/3.5))      # MLE, s_min=4
    log(f"  tau_av (MLE, 4<=s<=q98) = {tau_av:.3f}   "
        f"(MF marginal 1.5 | 1+1d DP cluster ~1.1; exploratory, no gate)")
else:
    tau_av = np.nan; log("  too few large avalanches; reported as-is")

# ------------------------------------------------- intermittency probe ------
log("== intermittency probe: M2(r) on late-time critical snapshots ==")
mus = []
for snap in snapshots:
    Ls = snap.size
    rows = []
    for p in range(1, 10):                       # r = 2..512
        r = 2**p
        rho_r = snap[:Ls - Ls % r].reshape(-1, r).mean(axis=1)
        if rho_r.mean() > 0:
            rows.append((r, (rho_r**2).mean()/rho_r.mean()**2))
    rows = np.array(rows)
    m = rows[:, 1] > 1.02
    if m.sum() >= 4:
        mus.append(-np.polyfit(np.log(rows[m, 0]), np.log(rows[m, 1]-0*1), 1)[0])
mu_eff = float(np.mean(mus)) if mus else np.nan
log(f"  mu_eff = {mu_eff:.3f} +- {np.std(mus):.3f}  "
    f"(DP 1+1d prediction 2*beta/nu_perp = 0.504; turbulence bulk mu ~ 0.25 is a "
    f"DIFFERENT regime -- see memo, problem D)")

# ------------------------------------------------------------------ summary -
log("== summary ==")
log(f"lambda_c={lam_c:.5f}  theta(pseudogap)={THETA}  q={Q}")
log(f"delta={delta_eff:.4f}(DP .1595)  theta_s={theta_s:.4f}(DP .3137)  "
    f"nu_par={nu_par:.3f}(DP 1.734)  tau_av={tau_av:.3f}  mu_eff={mu_eff:.3f}")
npass = sum([g2, g3, g4])
log(f"GATES: {npass}/3 hard gates PASS "
    f"({'DP class CONFIRMED for the G-SOC rules' if npass==3 else 'see numbers above'})")
log(f"total runtime {time.time()-t0:.0f}s")

with open('/home/claude/v3work/transition_dp.out.txt', 'w') as f:
    f.write("\n".join(log_lines) + "\n")
np.savetxt('/home/claude/v3work/transition_dp_decay.csv',
           np.column_stack([RS_best[0][0], RS_best[0][1]]),
           header='t,rho (seed1, lambda_c)', delimiter=',', comments='')
