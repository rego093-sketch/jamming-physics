#!/usr/bin/env python3
"""
continental_yield.py -- CG-39 refinement: a TRUE finite yield strength (not the cell-scale mobility
proxy of continental_rheology.py). A continental block DEFORMS only where the convective STRAIN RATE
exceeds yield Y; below yield the block translates RIGIDLY (block-mean velocity). Y is SCANNED, never
tuned -- f(Y) is reported, including the parameter-free RIGID LIMIT (Y->inf).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/  SEED=19.

This tests the v1.5 conjecture that the ~0.38->0.41 residual is the cell-scale-rigidity approximation
under-counting true continental strength. Distinct physics from the mobility model: mobility freezes a
cell by its neighbour count, so EDGE cells always stay mobile (continents erode at the rim for any kappa);
a stress-based yield lets a whole sub-yield block -- edges included -- translate as a rigid body.

Recorded result (see continental_yield.out.txt; the convection step takes ~90 s):
  passive (Y=0):              f ~ 0.29  (reproduces the coupled ~0.30 deficit)
  rising Y lifts f but it SATURATES ~0.34 (uniform) / ~0.33 (convergent) by Y/Srms ~ 2 and stays there
  all the way to the RIGID LIMIT (Y->inf): f ~ 0.34. => making continents perfectly rigid rafts does
  NOT bring the stirred fraction to the ceiling -- rigid blocks are still ADVECTED into the downwelling
  pattern, which throttles accretion below ~0.41. This FALSIFIES the 'yield strength closes the gap'
  conjecture: rheology (mobility ~0.38 AND yield-rigid ~0.34) recovers PART of the deficit but BOTH
  saturate SHORT of the observed 0.41. The residual is therefore NOT continental rheology -- it points
  to sphere geometry + internal heating (narrower downwellings), or the planar ceiling 0.407 is the
  bound a flat stirred box approaches from below but cannot attain. falsification = discovery. Grade [O] for closure.
"""
import numpy as np, time
from scipy.ndimage import label, map_coordinates, binary_dilation, mean as ndmean
from rbc3d import RBC3D

# --- 1. convection to steady state (same validated solver / flow) ---
Nx = Ny = 64; Nz = 12; L = 6*np.pi; Ra = 1.0e4
m = RBC3D(Nx, Ny, Nz, L=L, Ra=Ra); rng0 = np.random.default_rng(19)
Th = m.to_spec_sin(1e-3*rng0.standard_normal((Nx, Ny, Nz)))
nv = np.arange(1, Nz+1); sgn = ((-1)**nv).astype(float)
def surf(Th):
    wH, uH, vH = m.velocity_hat(Th)
    wmid = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', wH, np.sin(nv*np.pi*0.78)), axes=(0,1)))
    ut = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', uH, sgn), axes=(0,1)))
    vt = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', vH, sgn), axes=(0,1)))
    return wmid, ut, vt
dt = 1e-4; t0 = time.time()
for s in range(2501):
    Th, _ = m.step(Th, dt, with_adv=True)
wmid, ut, vt = surf(Th); down = wmid < 0; dx = L/Nx
# strain-rate second invariant from the surface flow (parameter-free)
dudx = (np.roll(ut,-1,0)-np.roll(ut,1,0))/(2*dx); dudy = (np.roll(ut,-1,1)-np.roll(ut,1,1))/(2*dx)
dvdx = (np.roll(vt,-1,0)-np.roll(vt,1,0))/(2*dx); dvdy = (np.roll(vt,-1,1)-np.roll(vt,1,1))/(2*dx)
exx = dudx; eyy = dvdy; exy = 0.5*(dudy+dvdx)
S = np.sqrt(0.5*(exx**2+eyy**2)+exy**2); Srms = np.sqrt((S**2).mean())
print(f"convection steady ({time.time()-t0:.0f}s): downwelling = {down.mean():.3f}, strain Srms = {Srms:.3f}")

# --- 2. continental tracer with a finite yield strength (rigid below yield, deform above) ---
umax = np.hypot(ut, vt).max()
ii, jj = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing='ij')
CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)
def advect(C, U, V):
    da = 0.4*dx/umax
    for _ in range(3):
        C = map_coordinates(C, [(ii-U*da/dx) % Nx, (jj-V*da/dx) % Ny], order=1, mode='wrap')
    return C
def run(Yrel, p_prod, r, convergent, seed, epochs=500):
    Y = Yrel*Srms; rg = np.random.default_rng(seed); C = (rg.random((Nx, Ny)) < 0.06).astype(float); h = []
    for e in range(epochs):
        ocean = C < 0.5; lab, k = label(ocean)
        if k > 0:
            sz = np.bincount(lab.ravel()); sz[0] = 0; big = sz.argmax(); active = lab == big; health = sz[big]/ocean.sum()
        else:
            active = np.zeros_like(ocean); health = 0.0
        cont = C >= 0.5; margin = active & binary_dilation(cont, CROSS) & ~cont
        prob = p_prod*health; pmap = (prob*np.where(down, 1.0, 0.25)) if convergent else prob
        born = margin & (rg.random((Nx, Ny)) < pmap); C = np.where(born, 1.0, C)
        # block-mean (rigid) velocity field vs the true (deforming) flow, switched by local yield
        clab, kc = label(C >= 0.5)
        Ur = np.zeros_like(ut); Vr = np.zeros_like(vt)
        if kc > 0:
            idx = np.arange(1, kc+1); um = ndmean(ut, clab, idx); vm = ndmean(vt, clab, idx)
            nz = clab > 0; Ur[nz] = um[clab[nz]-1]; Vr[nz] = vm[clab[nz]-1]
        Cr = advect(C, Ur, Vr); Cd = advect(C, ut, vt)
        C = np.where(S < Y, Cr, Cd)                 # below yield: rigid block translation; above: deform
        C = C*(1-r); h.append((C > 0.5).mean())
    return np.mean(h[-100:])

print("\nf vs RELATIVE yield Y/Srms (3 seeds; p_prod=0.30, r=0.015). Y=0 = passive; large = rigid limit:")
print("  Y/Srms  |  uniform  |  convergent")
for Yrel in [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 1e6]:
    fu = np.mean([run(Yrel, 0.30, 0.015, False, s) for s in (19, 1019, 2019)])
    fc = np.mean([run(Yrel, 0.30, 0.015, True,  s) for s in (19, 1019, 2019)])
    tag = "  <- RIGID LIMIT (Y->inf)" if Yrel > 1e5 else ""
    print(f"  {Yrel:7.2f} |   {fu:.3f}   |    {fc:.3f}{tag}")
print("\npassive ~0.29; mobility-model saturated ~0.38; this yield model saturates ~0.34 even RIGID; ceiling ~0.407; observed 0.41.")
print("=> FALSIFIES 'yield strength closes the gap': two rheology encodings BOTH saturate SHORT of 0.41.")
print("   Residual is NOT rheology -> sphere geometry + internal heating, or the value sits at the planar")
print("   ceiling a flat stirred box only approaches. No tuning (rigid limit is parameter-free). falsification = discovery.")
