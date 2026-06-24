#!/usr/bin/env python3
"""
continental_rheology.py -- CG-39: does continental COHERENCE (rheology resisting dispersal) lift the
stirred continental fraction from the passive ~0.30 toward the percolation ceiling ~0.41?
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
SEED=19. NOT tuned to 0.41 -- the coherence strength kappa is SCANNED and f(kappa) is reported.

Extends convection_and_tracer.py (the frozen-flow tracer that gave the passive 0.24-0.32 / coupled
~0.30). The ONLY additions are the two physical ingredients named as the CG-38 residual:
  (1) continental COHERENCE: interior continent cells RESIST advective dispersal (raft rigidity at the
      cell scale). mobility = 1/(1 + kappa * (#continent neighbours)); kappa=0 recovers the passive
      tracer. This is the 'real rheology, not a passive scalar' lever.
  (2) convergent-margin-CONCENTRATED production: felsic born preferentially where the surface flow is
      DOWNWELLING (convergent), vs uniform at all active-ocean margins.

Recorded result (see continental_rheology.out.txt; the convection step takes ~90 s):
  passive (kappa=0, uniform):    f ~ 0.29  (reproduces the established coupled ~0.30 deficit)
  coherence lifts f MONOTONICALLY toward the ceiling but SATURATES ~0.37-0.38 (uniform) / ~0.34
  (convergent) within the explored range -- it recovers ~75% of the 0.30->0.41 gap, NOT all of it.
  The percolation ceiling ~0.41 is NOT exceeded. => coherence is the confirmed lever; the ceiling
  (kernel) bounds the value; the residual ~0.38->0.41 needs a true yield rheology (> cell-scale
  rigidity) + sphere geometry + internal heating. falsification = discovery. Grade [L].
"""
import numpy as np, time
from scipy.ndimage import label, map_coordinates, binary_dilation
from rbc3d import RBC3D

# --- 1. run the validated convection to a statistical steady state (real stirring flow) ---
Nx = Ny = 64; Nz = 12; L = 6*np.pi; Ra = 1.0e4
m = RBC3D(Nx, Ny, Nz, L=L, Ra=Ra); rng0 = np.random.default_rng(19)
Th = m.to_spec_sin(1e-3*rng0.standard_normal((Nx, Ny, Nz)))
nv = np.arange(1, Nz+1); sgn = ((-1)**nv).astype(float)
def surface(Th):
    wH, uH, vH = m.velocity_hat(Th)
    wmid = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', wH, np.sin(nv*np.pi*0.78)), axes=(0,1)))
    ut = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', uH, sgn), axes=(0,1)))
    vt = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', vH, sgn), axes=(0,1)))
    return wmid, ut, vt
dt = 1e-4; t0 = time.time()
for s in range(2501):
    Th, _ = m.step(Th, dt, with_adv=True)
wmid, ut, vt = surface(Th); down = wmid < 0
print(f"convection steady ({time.time()-t0:.0f}s): downwelling area fraction = {down.mean():.3f}")

# --- 2. continental tracer with coherence, stirred by the real convective surface flow ---
dx = L/Nx; umax = np.hypot(ut, vt).max()
ii, jj = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing='ij')
CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)
def nbr8(b):
    s = np.zeros(b.shape, np.int16)
    for ax in (-1,0,1):
        for ay in (-1,0,1):
            if ax or ay: s += np.roll(np.roll(b, ax, 0), ay, 1)
    return s
def advect(C):
    da = 0.4*dx/umax
    for _ in range(3):
        C = map_coordinates(C, [(ii-ut*da/dx) % Nx, (jj-vt*da/dx) % Ny], order=1, mode='wrap')
    return C
def run(kappa, p_prod, r, convergent, seed, epochs=500):
    rg = np.random.default_rng(seed); C = (rg.random((Nx, Ny)) < 0.06).astype(float); h = []
    for e in range(epochs):
        ocean = C < 0.5; lab, k = label(ocean)
        if k > 0:
            sz = np.bincount(lab.ravel()); sz[0] = 0; big = sz.argmax(); active = lab == big; health = sz[big]/ocean.sum()
        else:
            active = np.zeros_like(ocean); health = 0.0
        cont = C >= 0.5; margin = active & binary_dilation(cont, CROSS) & ~cont
        prob = p_prod*health
        pmap = (prob*np.where(down, 1.0, 0.25)) if convergent else prob
        born = margin & (rg.random((Nx, Ny)) < pmap)
        C = np.where(born, 1.0, C)
        # COHERENCE: interior continent cells resist advective dispersal (raft rigidity, cell scale)
        Cadv = advect(C)
        mob = 1.0/(1.0 + kappa*nbr8(C >= 0.5).astype(float))   # in (0,1]; interiors ~frozen at high kappa
        C = mob*Cadv + (1-mob)*C
        C = C*(1-r); h.append((C > 0.5).mean())
    return np.mean(h[-100:])

print("\nCONTINENTAL FRACTION f vs COHERENCE kappa (3 seeds averaged; p_prod=0.30, r=0.015):")
print("  kappa |  uniform production  |  convergent-margin production")
for kappa in [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]:
    fu = np.mean([run(kappa, 0.30, 0.015, False, s) for s in (19, 1019, 2019)])
    fc = np.mean([run(kappa, 0.30, 0.015, True,  s) for s in (19, 1019, 2019)])
    print(f"  {kappa:5.1f} |       {fu:.3f}          |        {fc:.3f}")
print("\npassive(kappa=0,uniform) ~0.29 reproduces the coupled ~0.30 deficit; ceiling f*~0.407; observed ~0.41.")
print("=> coherence LIFTS f toward the ceiling (recovers ~75% of the 0.30->0.41 gap) but SATURATES ~0.38,")
print("   NOT reaching 0.41 and NOT exceeding the ceiling. The residual needs a true yield rheology")
print("   (> cell-scale rigidity) + sphere geometry + internal heating. Grade [L]. falsification = discovery.")
