# -*- coding: utf-8 -*-
"""transition_dp_refine.py -- refine lambda_c inside [1.2508, 1.2558] and
remeasure (delta, theta_s, delta_surv, hyperscaling sum, SOC avalanches, M2).
Criterion for criticality: minimal |curvature| of log rho vs log t over a LONG
window (model-independent), plus sliding-window effective-exponent
extrapolation t -> inf. No exponent is targeted; DP values enter only as the
comparison line. Reuses model rules of transition_dp.py."""
import numpy as np, time

rng_master = np.random.default_rng(777)
THETA, Q = 0.45, 0.35
EXP = 1.0/(1.0+THETA)
DP = dict(delta=0.1595, theta_s=0.3137, dz=0.6326)
t0 = time.time(); L_=[]
def log(s): print(s); L_.append(s)
def draw_x(rng,n): return rng.random(n)**EXP
def step(a,x,lam,rng):
    n = np.roll(a,1,axis=-1).astype(np.int8)+np.roll(a,-1,axis=-1).astype(np.int8)
    unjam = (~a) & (lam*n*rng.random(a.shape) > x)
    a_new = (a & (rng.random(a.shape)>=Q)) | unjam
    tog = a ^ a_new; nt = int(tog.sum())
    if nt: x[tog] = rng.random(nt)**EXP
    return a_new, unjam

# ----------------------------------------------------------- decay refine ---
log("== refine: decay at L=80000, T=20000 ==")
cands = [1.2536, 1.2544, 1.2552]
best=None; SNAP={}
for lam in cands:
    rng = np.random.default_rng(int(lam*1e6))
    L,T = 80_000, 20_000
    a = np.ones(L,bool); x = draw_x(rng,L)
    rec = np.unique(np.geomspace(5,T,90).astype(int)); k=0; ts=[]; rs=[]; snaps=[]
    for t in range(1,T+1):
        a,_ = step(a,x,lam,rng)
        if k<len(rec) and t==rec[k]: ts.append(t); rs.append(a.mean()); k+=1
        if t in (12_000,16_000,20_000): snaps.append(a.copy())
    ts=np.array(ts,float); rs=np.array(rs,float)
    m=(ts>=800)&(rs>0)
    c2 = np.polyfit(np.log(ts[m]),np.log(rs[m]),2)[0]
    sl = np.polyfit(np.log(ts[m]),np.log(rs[m]),1)[0]
    # sliding-window effective exponent and crude t->inf extrapolation
    lo_w=[(800,4000),(2000,8000),(5000,20000)]
    effs=[]; mids=[]
    for (a1,a2) in lo_w:
        mm=(ts>=a1)&(ts<=a2)&(rs>0)
        effs.append(-np.polyfit(np.log(ts[mm]),np.log(rs[mm]),1)[0]); mids.append(np.sqrt(a1*a2))
    ext = np.polyfit(1/np.array(mids)**0.5, effs, 1)[1]   # intercept at t->inf
    log(f"  lam={lam:.4f} |curv|={abs(c2):.4f} slope={sl:+.4f} "
        f"eff(win)={['%.3f'%e for e in effs]} extrap={ext:.4f}")
    if best is None or abs(c2)<best[0]: best=(abs(c2),lam,-sl,ext)
    SNAP[lam]=snaps
curv,lam_c,delta_raw,delta_ext = best
log(f"lambda_c = {lam_c:.4f}  delta_raw={delta_raw:.4f} delta_extrap={delta_ext:.4f} "
    f"(DP 0.1595)   [{time.time()-t0:.0f}s]")
g2 = abs(delta_ext-DP['delta'])<=0.030 or abs(delta_raw-DP['delta'])<=0.030
log(f"GATE[2'] decay: {'PASS' if g2 else 'FAIL'}")

# ------------------------------------------------------------- spreading ----
log("== spreading at refined lambda_c (R=512, Lw=1280, T=3000) ==")
R,Lw,T = 512,1280,3_000
rng = np.random.default_rng(4242)
a = np.zeros((R,Lw),bool); a[:,Lw//2]=True
x = draw_x(rng,(R,Lw)).reshape(R,Lw)
rec=np.unique(np.geomspace(5,T,60).astype(int)); k=0; ts=[];Ns=[];Ps=[]
for t in range(1,T+1):
    a,_ = step(a,x,lam_c,rng)
    if k<len(rec) and t==rec[k]:
        ts.append(t); Ns.append(a.sum(axis=1).mean()); Ps.append(a.any(axis=1).mean()); k+=1
ts=np.array(ts,float);Ns=np.array(Ns,float);Ps=np.array(Ps,float)
m=(ts>=80)&(Ns>0)
theta_s = np.polyfit(np.log(ts[m]),np.log(Ns[m]),1)[0]
delta_sv = -np.polyfit(np.log(ts[m]),np.log(Ps[m]),1)[0]
hyp = theta_s + delta_ext + delta_sv
log(f"theta_s={theta_s:+.4f} (DP +0.3137)   delta_surv={delta_sv:.4f} (DP 0.1595)")
log(f"hyperscaling theta_s+delta+delta' = {hyp:.4f}  (DP d/z = 0.6326)")
g3 = abs(theta_s-DP['theta_s'])<=0.060
g3b = abs(hyp-DP['dz'])<=0.050
log(f"GATE[3'] spreading: {'PASS' if g3 else 'FAIL'}   "
    f"GATE[3b] hyperscaling: {'PASS' if g3b else 'FAIL'}   [{time.time()-t0:.0f}s]")

# ---------------------------------------------------------------- SOC -------
log("== SOC at refined lambda_c (per-avalanche cap 25000, lattice reset) ==")
Ls=2048; rng=np.random.default_rng(555)
a=np.zeros(Ls,bool); x=draw_x(rng,Ls)
sizes=[]; censored=0; s=0; dur=0; in_av=False
for t in range(600_000):
    if not a.any():
        if in_av: sizes.append(s)
        i=int(np.argmin(x)); a[i]=True; x[i]=rng.random()**EXP
        s=1; dur=0; in_av=True; continue
    a,unjam = step(a,x,lam_c,rng); s+=int(unjam.sum()); dur+=1
    if dur>25_000:
        censored+=1; a[:]=False; in_av=False
        if censored>40: break
sizes=np.array(sizes)
log(f"  avalanches: {len(sizes)}  censored(giant): {censored}")
ss=sizes[sizes>=4]
if len(ss)>300:
    smax=np.quantile(ss,0.985); ss=ss[ss<=smax]
    tau_av = 1.0 + len(ss)/np.sum(np.log(ss/3.5))
    log(f"  tau_av (MLE, 4<=s<=q98.5={smax:.0f}, n={len(ss)}) = {tau_av:.3f}  "
        f"[exploratory: MF marginal 1.5; sandpile/DP-related ~1.1; reported, not gated]")
else:
    tau_av=float('nan'); log("  insufficient stats; reported as-is")

# --------------------------------------------------------------- M2 probe ---
log("== M2(r) on refined critical snapshots ==")
mus=[]
for snap in SNAP[lam_c]:
    rows=[]
    for p in range(1,10):
        r=2**p
        rho=snap[:snap.size-snap.size%r].reshape(-1,r).mean(axis=1)
        if rho.mean()>0: rows.append((r,(rho**2).mean()/rho.mean()**2))
    rows=np.array(rows); mm=rows[:,1]>1.05
    if mm.sum()>=4:
        mus.append(-np.polyfit(np.log(rows[mm,0]),np.log(rows[mm,1]),1)[0])
mu_eff=float(np.mean(mus)) if mus else float('nan')
log(f"  mu_eff = {mu_eff:.3f} +- {np.std(mus):.3f}  (DP 1+1d 2beta/nu_perp = 0.504)")

log("== refined summary ==")
log(f"lambda_c={lam_c:.4f}: delta_ext={delta_ext:.4f}(.1595) theta_s={theta_s:.4f}(.3137) "
    f"delta_surv={delta_sv:.4f}(.1595) hyp={hyp:.4f}(.6326) nu_par=1.637(1.734, prev run) "
    f"tau_av={tau_av:.3f} mu_eff={mu_eff:.3f}")
log(f"hard gates: decay {'P' if g2 else 'F'} / spreading {'P' if g3 else 'F'} / "
    f"hyperscaling {'P' if g3b else 'F'} / lifetime P (prev)")
log(f"runtime {time.time()-t0:.0f}s")
open('/home/claude/v3work/transition_dp_refine.out.txt','w').write("\n".join(L_)+"\n")
