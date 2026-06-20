# -*- coding: utf-8 -*-
"""dev64.py -- develop forced 3D turbulence with checkpointing and a per-call
wall-time budget (mirrors run3d.py). Run repeatedly; it resumes from state.npz
until the field is developed (skewness magnitude > 0.45 and >= TARGET steps).
Usage: python dev64.py [budget_seconds]"""
import numpy as np, time, sys, os
import ns3d as S

N, nu, dt = 64, 0.008, 0.004
TARGET = 600
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 220.0
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state64.npz")

g = S.grid(N)
if os.path.exists(STATE):
    z = np.load(STATE); uh, vh, wh = z['uh'], z['vh'], z['wh']; ns = int(z['ns'])
    print(f"resumed step={ns}")
else:
    uh, vh, wh = S.randIC(N, g, seed=1); ns = 0
    print(f"init N={N} nu={nu} dt={dt}")

t0 = time.time(); tps = 0.48
while time.time() - t0 + 2 * tps < budget and ns < TARGET:
    uh, vh, wh = S.force(uh, vh, wh, g); uh, vh, wh = S.step(uh, vh, wh, g, nu, dt)
    ns += 1
    if ns % 8 == 0:
        tps = (time.time() - t0) / (ns - int(z['ns']) if os.path.exists(STATE) else ns) \
              if ns > 0 else 0.48

np.savez(STATE, uh=uh, vh=vh, wh=wh, ns=ns)
sk = S.skewness(uh, g); Z = S.enstrophy(uh, vh, wh, g)
dev = abs(sk) > 0.45 and ns >= TARGET
print(f"step={ns} skewness={sk:+.3f} Z={Z:.1f} eps={2*nu*Z:.3f} "
      f"{'DEVELOPED' if dev else 'developing'}  ({time.time()-t0:.0f}s this call)")
