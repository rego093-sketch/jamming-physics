# -*- coding: utf-8 -*-
"""embed96.py -- resolution-trend point for P4. Spectrally embed the developed
N=64 field into N=96 (zero-pad high modes), then relax so the new dissipation-
range modes equilibrate. Checkpointed with a per-call wall-time budget.
Usage: python embed96.py [budget_seconds]"""
import numpy as np, time, sys, os
import ns3d as S

N64, N96, nu, dt = 64, 96, 0.008, 0.004
RELAX = 170
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 220.0
ST96 = "state96.npz"

g = S.grid(N96)
if os.path.exists(ST96):
    z = np.load(ST96); uh, vh, wh = z['uh'], z['vh'], z['wh']; ns = int(z['ns'])
    print(f"resumed N=96 relax step={ns}")
else:
    z = np.load("state64.npz")
    def embed(a64):
        # place N=64 fftn coefficients into N=96 grid preserving frequencies
        out = np.zeros((N96, N96, N96), dtype=complex)
        h = N64 // 2
        idx = list(range(0, h)) + list(range(N96 - h, N96))      # map -h..h-1
        src = list(range(0, h)) + list(range(N64 - h, N64))
        # scale for FFT normalization difference (np.fft.ifftn divides by N^3)
        scale = (N96 ** 3) / (N64 ** 3)
        for ai, oi in zip(src, idx):
            for aj, oj in zip(src, idx):
                out[oi, oj, np.array(idx)] = a64[ai, aj, np.array(src)] * scale
        return out
    uh = embed(z['uh']); vh = embed(z['vh']); wh = embed(z['wh'])
    uh, vh, wh = (uh * g['mask'], vh * g['mask'], wh * g['mask'])
    ns = 0
    print(f"embedded N=64 -> N=96  u_rms={np.sqrt(2*S.energy(uh,vh,wh)):.3f} "
          f"skew={S.skewness(uh,g):+.3f}")

t0 = time.time(); tps = 2.0
while time.time() - t0 + 2 * tps < budget and ns < RELAX:
    uh, vh, wh = S.force(uh, vh, wh, g); uh, vh, wh = S.step(uh, vh, wh, g, nu, dt)
    ns += 1
np.savez(ST96, uh=uh, vh=vh, wh=wh, ns=ns)
sk = S.skewness(uh, g); Z = S.enstrophy(uh, vh, wh, g)
print(f"relax step={ns} skewness={sk:+.3f} Z={Z:.1f} eps={2*nu*Z:.3f} "
      f"{'EQUILIBRATED' if ns >= RELAX and abs(sk) > 0.45 else 'relaxing'} "
      f"({time.time()-t0:.0f}s this call)")
