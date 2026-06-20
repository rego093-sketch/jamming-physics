# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.9a static magnet does no work; cyclotron drift=0
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: 7c8246ab...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
Put a magnet, simulate (Boris pusher -> exact energy conservation in static B).
m dv/dt = q(E + v x B), B = B z-hat.
 - static B alone: electrons trace exact CIRCLES (cyclotron) -- keep oscillating, NET current = 0,
   and kinetic energy is EXACTLY constant (a magnetic force does no work, F ⊥ v).
 - an E-field (bias): real drift -> current, and energy rises (E does work).
=> current is driven by an E-field (changing flux / junction / thermal gradient), never by a static magnet.
Deterministic + sha256.
"""
import numpy as np, hashlib
np.random.seed(0)
q=-1.0; m=1.0; B=1.0; dt=0.02

def boris(vx,vy,Ex,Ey,useB):
    Bf=B if useB else 0.0
    # half E
    vmx=vx+(q*Ex/m)*(dt/2); vmy=vy+(q*Ey/m)*(dt/2)
    # rotation by B (exact, energy-preserving)
    t=q*Bf*dt/(2*m)
    vpx=vmx+vmy*t; vpy=vmy-vmx*t
    s=2*t/(1+t*t)
    vP_x=vmx+vpy*s; vP_y=vmy-vpx*s
    # half E
    vx=vP_x+(q*Ex/m)*(dt/2); vy=vP_y+(q*Ey/m)*(dt/2)
    return vx,vy

# ---------- (A) trajectories in static B ----------
T=900; traj=[]
for k in range(6):
    ang=np.random.uniform(0,2*np.pi); sp=np.random.uniform(0.6,1.4)
    rx,ry=np.random.uniform(-0.5,0.5),np.random.uniform(-0.5,0.5)
    vx,vy=sp*np.cos(ang),sp*np.sin(ang)
    pts=[(rx,ry)]
    for _ in range(T):
        vx,vy=boris(vx,vy,0,0,True); rx+=vx*dt; ry+=vy*dt; pts.append((rx,ry))
    traj.append(np.array(pts))
print("[A] static B: exact circles (cyclotron) -> keeps oscillating, NO net direction")

# ---------- (B) net drift with scattering ----------
N=3000; tau=6.0; steps=1200
def run(Ex,useB):
    ang=np.random.uniform(0,2*np.pi,N); sp=np.random.normal(1.0,0.3,N)
    vx=sp*np.cos(ang); vy=sp*np.sin(ang); mvx=np.zeros(steps)
    for s in range(steps):
        vx,vy=boris(vx,vy,Ex,0.0,useB)
        hit=np.random.random(N)<dt/tau; nh=int(hit.sum())
        if nh>0:
            a2=np.random.uniform(0,2*np.pi,nh); s2=np.random.normal(1.0,0.3,nh)
            vx[hit]=s2*np.cos(a2); vy[hit]=s2*np.sin(a2)
        mvx[s]=vx.mean()
    return mvx
mvx_B=run(0.0,True); mvx_E=run(0.30,False)
print(f"[B] <vx>: magnet only -> {mvx_B[-200:].mean():+.4f} (~0, NO current); E-field -> {mvx_E[-200:].mean():+.4f} (CURRENT)")

# ---------- (C) energy: B does no work (now exact) ----------
def energy(Ex,useB,steps=900):
    ang=np.random.uniform(0,2*np.pi,N); sp=np.random.normal(1.0,0.3,N)
    vx=sp*np.cos(ang); vy=sp*np.sin(ang); KE=np.zeros(steps)
    for s in range(steps):
        vx,vy=boris(vx,vy,Ex,0.0,useB); KE[s]=0.5*m*(vx**2+vy**2).mean()
    return KE
KE_B=energy(0.0,True); KE_E=energy(0.20,False)
print(f"[C] KE: static B {KE_B[0]:.4f}->{KE_B[-1]:.4f} (CONSTANT); E-field {KE_E[0]:.4f}->{KE_E[-1]:.4f} (RISES)")
print("    magnetic force does NO work (F ⊥ v) -> cannot drive or sustain current")
key=np.concatenate([mvx_B,mvx_E,KE_B,KE_E]).astype(np.float64)
print("RESULT sha256 = "+hashlib.sha256(key.tobytes()).hexdigest())
