# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.11 microchannel eps-f, pumping
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: aa296c82...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
Counterflow microchannel regenerator for the thermomagnetic AMR generator.
Nail down practical f and eta with real heat-transfer + fluid mechanics.
 - effectiveness: eps = K/(K+f), K = Nu*k_f/(2 d_c^2 rho_f c_f)  (laminar parallel-plate, NTU=K/f)
   => smaller channel d_c -> higher K -> higher f at a given eps.
 - pumping loss fraction: P_pump/P_gen = 48*mu*f*L^2/(d_c*t_p*w)
   => SHORT flow length L and not-too-small d_c keep pumping small.
 - net efficiency = eta_regen(eps(f)) * (1 - pump_frac).
Fluid = water. Deterministic + sha256.
"""
import numpy as np, hashlib

# ---- thermomagnetic side (from prior turns) ----
Carnot=0.077; R=18.2; w=2.45e5; t_p=50e-6
eta_coil=0.6; eta_pe=0.85
def eta_regen(eps): return Carnot/(1.0+(1.0-eps)*R)
# ---- fluid: water ----
k_f=0.6; rho_f=1000.0; c_f=4186.0; mu=1.0e-3; Nu=7.54
def Kof(dc): return Nu*k_f/(2.0*dc**2*rho_f*c_f)      # ~frequency scale (Hz)
def eps_of(f,dc): return Kof(dc)/(Kof(dc)+f)
def pumpfrac(f,dc,L): return 48.0*mu*f*L**2/(dc*t_p*w)
def eta_net(f,dc,L): return eta_regen(eps_of(f,dc))*(1.0-pumpfrac(f,dc,L))

print("="*70); print("CHANNEL GAP sets the eps-f scale K:")
for dc in [0.20e-3,0.15e-3,0.12e-3,0.10e-3]:
    K=Kof(dc); print(f"  d_c={dc*1e6:4.0f} um: K={K:5.1f} Hz -> eps=0.90 @ f={K/9:4.1f} Hz, eps=0.95 @ f={K/19:4.1f} Hz")

# two operating points (d_c=0.12mm, short plate L=20mm)
dc=0.12e-3; L=0.020
print("="*70); print(f"OPERATING POINTS (d_c=120 um, flow length L=20 mm, water):")
for f in [1.5,4.0]:
    eps=eps_of(f,dc); er=eta_regen(eps); pf=pumpfrac(f,dc,L); en=eta_net(f,dc,L); ee=en*eta_coil*eta_pe
    print(f"  f={f:4.1f} Hz: eps={eps:.3f}, eta_regen={er*100:.2f}%, pump={pf*100:4.1f}%, NET eta_mech={en*100:.2f}% ({en/Carnot*100:.0f}% of Carnot), eta_elec={ee*100:.2f}%")

# resulting output + material from a 10 kW AC's ~13 kW reject heat
Qsrc=13000.0
print("="*70); print(f"FROM A 10 kW AC's ~13 kW REJECT HEAT:")
for f,name in [(1.5,"efficiency-optimized"),(4.0,"power/size-balanced")]:
    en=eta_net(f,dc,L); ee=en*eta_coil*eta_pe; Wel=Qsrc*ee
    Vsolid=eta_regen(eps_of(f,dc))*Qsrc/(w*f)            # active-material volume needed
    print(f"  {name:22s} f={f:.1f} Hz: {Wel:5.0f} W elec ; active material {Vsolid*1e3:4.2f} L ; mass {Vsolid*7200:4.1f} kg")

# flow sanity (f=4Hz)
f=4.0; u=2*f*L; Re=rho_f*u*(2*dc)/mu; dp=12*mu*u*L/dc**2
print("="*70); print(f"FLOW SANITY @ f=4 Hz: fluid velocity {u:.2f} m/s, Re={Re:.0f} (laminar), dP/channel {dp:.0f} Pa")
key=np.array([Kof(dc),eps_of(4,dc),eta_net(1.5,dc,L),eta_net(4,dc,L),pumpfrac(4,dc,L)]).astype(np.float64)
print("RESULT sha256 = "+hashlib.sha256(key.tobytes()).hexdigest())
