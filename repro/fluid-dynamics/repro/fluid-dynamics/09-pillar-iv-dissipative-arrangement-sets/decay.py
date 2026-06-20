# -*- coding: utf-8 -*-
"""decay.py N statefile logfile [budget_s] -- free decay (forcing OFF) from a
developed field (the Goto-Vassilicos release protocol), logging the C_eps(Re_lam)
trajectory. Checkpointed: each call advances the decay within a wall-time budget,
appends diagnostics to the CSV log, and saves the state for resume."""
import numpy as np, time, sys, os
import ns3d as S
import nonequilibrium_dissipation as ND

N = int(sys.argv[1]); STATE = sys.argv[2]; LOG = sys.argv[3]
budget = float(sys.argv[4]) if len(sys.argv) > 4 else 220.0
nu, dt = 0.008, 0.004
LOG_EVERY = 12

g = S.grid(N)
z = np.load(STATE); uh, vh, wh = z['uh'], z['vh'], z['wh']
t = float(z['t']) if 't' in z else 0.0
step0 = int(z['dstep']) if 'dstep' in z else 0

new = not os.path.exists(LOG)
f = open(LOG, "a")
if new:
    f.write("step,t,E,Z,eps,up,L,lam,Re_lam,C_eps,eta,kmax_eta,skew\n")
    d = ND.diagnostics(uh, vh, wh, g, nu)
    f.write(f"0,0,{d['E']:.6f},{d['Z']:.4f},{d['eps']:.6f},{d['up']:.6f},"
            f"{d['L']:.6f},{d['lam']:.6f},{d['Re_lam']:.4f},{d['C_eps']:.6f},"
            f"{d['eta']:.6f},{d['kmax_eta']:.4f},{d['skew']:.4f}\n")
    f.flush()
    print(f"decay start N={N}: Re_lam={d['Re_lam']:.1f} C_eps={d['C_eps']:.3f}")

t0 = time.time(); tps = 1.9 if N >= 96 else 0.55; s = step0
while time.time() - t0 + 2 * tps < budget:
    uh, vh, wh = S.step(uh, vh, wh, g, nu, dt)   # NO forcing -> free decay
    t += dt; s += 1
    if s % LOG_EVERY == 0:
        d = ND.diagnostics(uh, vh, wh, g, nu)
        f.write(f"{s},{t:.4f},{d['E']:.6f},{d['Z']:.4f},{d['eps']:.6f},{d['up']:.6f},"
                f"{d['L']:.6f},{d['lam']:.6f},{d['Re_lam']:.4f},{d['C_eps']:.6f},"
                f"{d['eta']:.6f},{d['kmax_eta']:.4f},{d['skew']:.4f}\n")
        f.flush()
        tps = (time.time() - t0) / (s - step0)
np.savez(STATE, uh=uh, vh=vh, wh=wh, t=t, dstep=s)
f.close()
d = ND.diagnostics(uh, vh, wh, g, nu)
print(f"decay step={s} t={t:.2f}: Re_lam={d['Re_lam']:.1f} C_eps={d['C_eps']:.3f} "
      f"E={d['E']:.3f} eps={d['eps']:.4f} kmax*eta={d['kmax_eta']:.2f} "
      f"({time.time()-t0:.0f}s, {s-step0} steps this call)")
