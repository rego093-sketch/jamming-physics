# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.10 self-sustained thermomagnetic oscillation
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: d6d8a9ab...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
IDEA: a self-oscillating THERMOMAGNETIC harvester for LOW-GRADE heat + a magnet.
A soft-magnetic tip (Curie point Tc tuned to ~40-60C) on a spring, between a HOT surface (near a magnet)
and a COLD region. Mechanism (relaxation oscillator):
  cold tip (T<Tc, M high) -> magnet pulls it to the hot surface -> it heats above Tc -> M collapses ->
  spring pulls it back to cold -> it cools below Tc -> M returns -> magnet pulls it in again -> repeat.
The thermal LAG gives the magnetic force net positive work each cycle -> self-sustained oscillation.
The moving magnetized tip induces EMF in a pickup coil -> ELECTRICITY. Works on small dT (around Tc),
so it runs on LOW-GRADE waste heat where ordinary engines stall. Deterministic + sha256.
"""
import numpy as np, hashlib

# ---- normalized model ----
Tc=0.5; Thot=0.95; Tcold=0.05; wC=0.04      # Curie step
tau=0.55                                     # thermal lag (key for self-oscillation)
A=2.6; lam=0.32                              # magnet pull strength / range (toward x=0)
k=1.0; x_rest=0.78; m=1.0                    # spring (rest in the COLD region)
c_mech=0.06; b_elec=0.55                     # mechanical damping; electrical (harvest) load

def M(T): return 1.0/(1.0+np.exp((T-Tc)/wC))         # magnetization vs temperature
def Tlocal(x): return Thot+(Tcold-Thot)*np.clip(x,0,1)  # hot at x=0, cold at x=1
def Fmag(x,T): return -A*M(T)*np.exp(-x/lam)          # attraction toward magnet at x=0 (negative dir)

dt=0.002; N=60000
x=0.8; v=0.0; T=Tcold
xs=np.zeros(N); vs=np.zeros(N); Ts=np.zeros(N); Ms=np.zeros(N); P=np.zeros(N)
for i in range(N):
    Mt=M(T)
    F_spring=-k*(x-x_rest)
    F_el=-b_elec*(Mt**2)*v                    # electrical damping = generator load
    F=F_spring+Fmag(x,T)+F_el-c_mech*v
    v+=F/m*dt; x+=v*dt
    if x<0: x=0; v=-0.3*v                      # hot wall (magnet face)
    if x>1.1: x=1.1; v=-0.3*v
    T+=(Tlocal(x)-T)/tau*dt
    P[i]=b_elec*(Mt**2)*v*v                    # instantaneous harvested power
    xs[i]=x; vs[i]=v; Ts[i]=T; Ms[i]=Mt

# steady-state metrics (last 60%)
ss=slice(int(0.4*N),N)
amp=xs[ss].max()-xs[ss].min()
# period via zero-crossings of (x - mean)
xc=xs[ss]-xs[ss].mean(); cross=np.where((xc[:-1]<0)&(xc[1:]>=0))[0]
period=(cross[-1]-cross[0])/max(len(cross)-1,1)*dt if len(cross)>1 else np.nan
Pavg=P[ss].mean()
print("THERMOMAGNETIC OSCILLATOR (low-grade heat + magnet -> electricity)")
print(f"  self-sustained oscillation: amplitude(x) = {amp:.2f}, period = {period:.2f} (norm), avg harvested power = {Pavg:.4f}")
print(f"  mechanism: M switches as the tip crosses Tc; thermal lag pumps the oscillation")
print(f"  runs on a SMALL dT around Tc -> tune Tc to ~40-60C with Gd/FeNi alloys -> LOW-GRADE waste heat works")
print("RESULT sha256 = "+hashlib.sha256(np.concatenate([xs[::50],Ts[::50],Ms[::50],P[::50]]).astype(np.float64).tobytes()).hexdigest())
