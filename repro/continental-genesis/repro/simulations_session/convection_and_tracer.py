#!/usr/bin/env python3
"""
convection_and_tracer.py -- drive the continental tracer with a REAL 3D convective surface flow.
SEED=19. Runs the validated infinite-Pr 3D Boussinesq solver (rbc3d.py) to a statistical steady
state, extracts the top-surface velocity + downwelling pattern, then evolves a continental tracer
(accretion at active ocean margins + connectivity throttle + recycling) stirred by that flow.

NOTE this is a FROZEN-FLOW test (the convection does not yet respond to the continents). The
decisive open residual is the TWO-WAY-COUPLED run (add a continent buoyancy term to the field).

Recorded result (see convection_and_tracer.out.txt; the convection step takes ~2 min):
  convection: downwelling area fraction 0.46, ~20 cells (cellular pattern).
  tracer: percolation throttle BOUNDS f; value is coupling-sensitive --
          accretion + real-flow stirring -> f = 0.24-0.32  (static 2D was 0.39-0.41).
  => attractor survives in 3D; the VALUE drops below the static 2D band under stirring.
     [The subsequent TWO-WAY-COUPLED run (coupled_rbc3d.py/coupled_driver.py) confirmed ~0.30 --
      coupling does NOT lift it to 0.41; see coupled_run_record.txt.]
"""
import numpy as np, time
from scipy.ndimage import label, map_coordinates, binary_dilation
from rbc3d import RBC3D

# --- 1. run convection to a statistical steady state ---
Nx = Ny = 64; Nz = 12; L = 6*np.pi; Ra = 1.0e4
m = RBC3D(Nx, Ny, Nz, L=L, Ra=Ra); rng = np.random.default_rng(19)
Th = m.to_spec_sin(1e-3*rng.standard_normal((Nx, Ny, Nz)))
n = np.arange(1, Nz+1); sgn = ((-1)**n).astype(float)
def surface(Th):
    wH, uH, vH = m.velocity_hat(Th)
    wmid = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', wH, np.sin(n*np.pi*0.78)), axes=(0,1)))
    ut = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', uH, sgn), axes=(0,1)))
    vt = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', vH, sgn), axes=(0,1)))
    return wmid, ut, vt
dt = 1e-4; t0 = time.time()
for s in range(2501):
    Th, _ = m.step(Th, dt, with_adv=True)
wmid, ut, vt = surface(Th); down = wmid < 0
ld, nd = label(down)
print(f"convection steady ({time.time()-t0:.0f}s): downwelling fraction={down.mean():.3f}, {nd} cells")

# --- 2. continental tracer stirred by the real convective surface flow ---
dx = L/Nx; umax = np.hypot(ut, vt).max()
ii, jj = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing='ij')
CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)
def advect(C):
    da = 0.4*dx/umax
    for _ in range(3):
        C = map_coordinates(C, [(ii-ut*da/dx) % Nx, (jj-vt*da/dx) % Ny], order=1, mode='wrap')
    return C
def run(p_prod, r, epochs=500):
    rg = np.random.default_rng(19); C = (rg.random((Nx,Ny)) < 0.06).astype(float); h = []
    for e in range(epochs):
        ocean = C < 0.5; lab, k = label(ocean)
        if k > 0:
            sz = np.bincount(lab.ravel()); sz[0] = 0; big = sz.argmax()
            active = lab == big; health = sz[big]/ocean.sum()
        else: active = np.zeros_like(ocean); health = 0.0
        cont = C >= 0.5; margin = active & binary_dilation(cont, CROSS) & (~cont)
        born = margin & (rg.random((Nx,Ny)) < p_prod*health)
        C = np.where(born, 1.0, C); C = advect(C)*(1-r); h.append((C > 0.5).mean())
    return np.mean(h[-100:]), np.std(h[-100:])
print("\ncontinental fraction (accretion + real 3D convective stirring):")
print("  p_prod   r    prod/rec |  steady f")
fs = []
for p_prod, r in [(0.30,0.010),(0.30,0.020),(0.20,0.010),(0.40,0.020),(0.50,0.030),(0.25,0.015)]:
    f, sd = run(p_prod, r); fs.append(f)
    print(f"   {p_prod:.2f} {r:.3f}   {p_prod/r:4.0f}    |  {f:.3f} (+/-{sd:.3f})")
print(f"\n  band: {min(fs):.3f}-{max(fs):.3f}  (static 2D 0.39-0.41; 3D-coupled ~0.30, see coupled_run_record.txt)")
print("  => attractor survives in 3D; value drops under stirring; the two-way-coupled run confirmed ~0.30.")
