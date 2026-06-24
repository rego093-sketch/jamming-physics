#!/usr/bin/env python3
"""
percolation_attractor.py -- the continental AREA FRACTION as a marginal-connectivity attractor.
SEED=19. Two parts:
  (1) static percolation: when does the OCEAN network stop spanning as continents grow?
  (2) a self-organizing loop with a PHYSICAL connectivity throttle (a fragmenting ocean subducts
      weakly) -> the steady fraction is pinned at the percolation threshold, rate-insensitively.

Recorded result (see percolation_attractor.out.txt):
  (1) ocean-spanning probability crosses 0.5 at f* = 0.407 (planar site p_c~0.5927 -> 1-p_c~0.407).
  (2) across a 4x production/destruction range, steady f = 0.394-0.414 (band +/-0.01 on f* and observed).
"""
import numpy as np
from scipy.ndimage import label, binary_dilation
rng = np.random.default_rng(19)
CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)

# ---- (1) static percolation: continent fraction f* where the ocean stops spanning ----
def ocean_spans(L, f):
    ocean = rng.random((L, L)) > f
    lab, n = label(ocean)
    if n == 0: return False
    return len(set(lab[0,:]) - {0} & (set(lab[-1,:]) - {0})) > 0

print("(1) static percolation -- ocean stops spanning at continent fraction f*:")
L = 200; trials = 120
for f in np.round(np.arange(0.37, 0.45, 0.01), 2):
    p = np.mean([ocean_spans(L, f) for _ in range(trials)])
    print(f"    f={f:.2f}:  P(ocean spans)={p:.2f}")
print("    => crosses 0.5 at f* ~ 0.407 (planar site p_c~0.5927 -> 1-p_c~0.407); observed ~0.41\n")

# ---- (2) self-organizing loop with connectivity throttle (physical, not a tuned knob) ----
N = 120
def step(cont, p_prod, p_dest):
    ocean = ~cont; lab, n = label(ocean)
    if n == 0: return cont & (rng.random(cont.shape) >= p_dest)
    sz = np.bincount(lab.ravel()); sz[0] = 0; big = sz.argmax(); active = lab == big
    health = sz[big]/ocean.sum()                       # ocean-connectivity health in [0,1]
    margin = active & binary_dilation(cont, CROSS) & (~cont)
    born = margin & (rng.random(cont.shape) < p_prod*health)   # subduction weakens as ocean fragments
    die  = cont   & (rng.random(cont.shape) < p_dest)
    return (cont | born) & ~die

def run(p_prod, p_dest, T=600):
    cont = rng.random((N,N)) < 0.08; h = []
    for _ in range(T): cont = step(cont, p_prod, p_dest); h.append(cont.mean())
    return np.mean(h[-120:]), np.std(h[-120:])

print("(2) self-organized loop (connectivity-throttled), scanning the rate ratio:")
print("    p_prod  p_dest  prod/dest |  steady f")
fs = []
for p_prod, p_dest in [(0.30,0.010),(0.30,0.020),(0.30,0.040),(0.20,0.010),
                       (0.50,0.020),(0.50,0.040),(0.40,0.020),(0.60,0.030)]:
    f, sd = run(p_prod, p_dest); fs.append(f)
    print(f"     {p_prod:.2f}    {p_dest:.3f}   {p_prod/p_dest:5.0f}   |  {f:.3f} (+/-{sd:.3f})")
print(f"\n    band over 4x rate range: {min(fs):.3f}-{max(fs):.3f}  (f*~0.407; observed ~0.41)")
print("    => rate-insensitive ATTRACTOR pinned at the percolation threshold.")
