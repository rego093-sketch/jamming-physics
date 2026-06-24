"""
coupled_driver.py <ckpt.npz> <budget_steps> <q_insul>
Two-way-coupled run: convection (with continent insulation source) co-evolves with the continental
tracer. Same accretion rule as the frozen-flow test (active-ocean margins), so the ONLY new effects
vs frozen flow are: (1) the flow co-evolves, (2) continent INSULATION feeds back into buoyancy,
(3) continents ride the LARGE-SCALE (low-pass) flow only (raft rigidity). Checkpointed: rerun to
continue. SEED=19.
"""
import sys, time, numpy as np
from scipy.ndimage import label, map_coordinates, binary_dilation
from coupled_rbc3d import CoupledRBC3D

CKPT = sys.argv[1] if len(sys.argv) > 1 else "ckpt.npz"
BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 800
Q_INSUL = float(sys.argv[3]) if len(sys.argv) > 3 else 7.0

Nx = Ny = 64; Nz = 12; L = 6*np.pi; Ra = 1.0e4; dt = 5e-5
TRACER_EVERY = 5
P_PROD = 0.30; R_REC = 0.015
K_CUT = 4.0                              # raft advection: keep only |k_horizontal| < K_CUT (large scale)
m = CoupledRBC3D(Nx, Ny, Nz, L=L, Ra=Ra, q_insul=Q_INSUL)
dx = L/Nx; CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)
ii, jj = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing='ij')
nvec = np.arange(1, Nz+1); sgn = ((-1)**nvec).astype(float)
KXm = (2*np.pi/L*np.fft.fftfreq(Nx)*Nx)[:, None]; KYm = (2*np.pi/L*np.fft.fftfreq(Ny)*Ny)[None, :]
lowpass = (KXm**2 + KYm**2) < K_CUT**2

def surface(Th):
    wH, uH, vH = m.velocity_hat(Th)
    wmid = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', wH, np.sin(nvec*np.pi*0.78)), axes=(0,1)))
    ut = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', uH, sgn), axes=(0,1)))
    vt = np.real(np.fft.ifft2(np.einsum('xyn,n->xy', vH, sgn), axes=(0,1)))
    # raft rigidity: continents ride the large-scale flow only
    us = np.real(np.fft.ifft2(np.fft.fft2(ut)*lowpass)); vs = np.real(np.fft.ifft2(np.fft.fft2(vt)*lowpass))
    return wmid, ut, vt, us, vs

rng = np.random.default_rng(19)
# ---- load or initialise ----
try:
    d = np.load(CKPT)
    Th = d['Th_re'] + 1j*d['Th_im']; C = d['C']; nstep = int(d['nstep']); phase = str(d['phase'])
    print(f"resumed {CKPT} at step {nstep}, phase {phase}, f={(C>0.5).mean():.3f}")
except FileNotFoundError:
    Th = m.to_spec_sin(1e-3*rng.standard_normal((Nx, Ny, Nz))); C = np.zeros((Nx, Ny)); nstep = 0; phase = "develop"
    print(f"init fresh (q_insul={Q_INSUL})")

def save():
    np.savez(CKPT, Th_re=Th.real, Th_im=Th.imag, C=C, nstep=nstep, phase=phase)

def advect(C, uA, vA):
    da = 0.4*dx/(np.hypot(uA, vA).max()+1e-9)
    for _ in range(3):
        C = map_coordinates(C, [(ii-uA*da/dx) % Nx, (jj-vA*da/dx) % Ny], order=1, mode='wrap')
    return C

t0 = time.time(); done = 0
while done < BUDGET:
    wmid, ut, vt, us, vs = surface(Th)
    Csmooth = np.real(np.fft.ifft2(np.fft.fft2(C)*lowpass)) if phase=="couple" else C
    Th, _ = m.step_coupled(Th, dt, C, with_adv=True, Csrc=Csmooth); nstep += 1; done += 1
    if phase == "develop" and nstep >= 2600:
        C = (rng.random((Nx, Ny)) < 0.06).astype(float); phase = "couple"   # seed continents
    if phase == "couple" and nstep % TRACER_EVERY == 0:
        ocean = C < 0.5; lab, k = label(ocean)
        if k > 0:
            sz = np.bincount(lab.ravel()); sz[0] = 0; big = sz.argmax(); active = lab == big; health = sz[big]/ocean.sum()
        else: active = np.zeros_like(ocean); health = 0.0
        cont = C >= 0.5; margin = active & binary_dilation(cont, CROSS) & (~cont)
        born = margin & (rng.random((Nx, Ny)) < P_PROD*health)
        C = np.where(born, 1.0, C); C = advect(C, us, vs)*(1-R_REC)
    if not np.isfinite(np.abs(Th).max()):
        print(f"  BLOWUP at step {nstep} -- not saving corrupted state"); sys.exit(1)
    if done % 500 == 0:
        save(); f = (C > 0.5).mean(); rw = np.sqrt((wmid**2).mean())
        print(f"  step {nstep}  rms_w={rw:5.1f}  down={(wmid<0).mean():.2f}  f={f:.3f}  ({time.time()-t0:.0f}s)", flush=True)
save()
print(f"saved {CKPT} at step {nstep}, phase {phase}, f={(C>0.5).mean():.3f}  ({time.time()-t0:.0f}s)")
