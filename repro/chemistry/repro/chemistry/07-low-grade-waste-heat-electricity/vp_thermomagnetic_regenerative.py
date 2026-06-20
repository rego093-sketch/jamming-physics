# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.11 regenerative eta 2.7-4.0%
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: aa45e145...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
High-efficiency thermomagnetic generator = Active Magnetic Regenerator (AMR) run as a generator.
Two levers:
 (1) REGENERATION: recover the sensible+latent heat shuttled each cycle. This is what kills eta (0.4%)
     without it. Regenerative (Ericsson/Stirling-like) efficiency: eta = Carnot/(1+(1-eps)*R),
     R = (shuttled heat)/(isothermal magnetic heat). eps->1 => eta->Carnot.
 (2) THIN-FILM STACK: f ~ 1/thickness -> ~10x power density, and it's what makes a high-eps counterflow
     regenerator physically realizable (many out-of-phase films exchanging heat).
Honest ceiling: Carnot (7.7% for dT=25K). Deterministic + sha256.
"""
import numpy as np, hashlib

# operating point + material (from the design turn)
Tcold,Thot=298.0,323.0; Carnot=(Thot-Tcold)/Thot
dM=7.0e5; dB=0.35; w=dM*dB                      # magnetic work density, J/m^3
rho=7200.0; cp=500.0; Lh=3000.0; dTsw=10.0
Qsh=rho*(cp*dTsw+Lh)                             # heat shuttled per cycle (sensible+latent), J/m^3
QHiso=w/Carnot                                   # isothermal magnetic heat at hot, J/m^3
R=Qsh/QHiso
def eta_mech(eps): return Carnot/(1.0+(1.0-eps)*R)
eta_coil=0.6; eta_pe=0.85                        # coil extraction; power electronics
def eta_elec(eps): return eta_mech(eps)*eta_coil*eta_pe

print("="*70)
print(f"R (shuttled / isothermal-magnetic heat) = {R:.1f}   Carnot ceiling = {Carnot*100:.1f}%")
print("REGENERATION is the efficiency lever:")
for eps in [0.0,0.5,0.8,0.9,0.95,0.99]:
    print(f"  eps={eps:4.2f}:  eta_mech={eta_mech(eps)*100:5.2f}%   eta_elec={eta_elec(eps)*100:5.2f}%")

# thin-film: frequency & power density
t0,f0=0.5e-3,0.7                                  # reference plate
def freq(t): return f0*(t0/t)
def Pdens(t): return w*freq(t)                    # W/m^3
print("="*70); print("THIN-FILM STACK is the power/realizability lever:")
for t in [0.5e-3,0.1e-3,50e-6,20e-6]:
    print(f"  thickness {t*1e6:5.0f} um: f={freq(t):5.1f} Hz, power density={Pdens(t)/1e6:5.2f} MW/m^3")

# performance from a real 10 kW AC's reject heat (~13 kW)
Qsrc=13000.0
def Wel(eps): return Qsrc*eta_elec(eps)
print("="*70); print(f"FROM A 10 kW AC's ~{Qsrc/1e3:.0f} kW REJECT HEAT (electrical output):")
print(f"  baseline plate (no regen):        {Wel(0.0):5.0f} W   (eta_elec {eta_elec(0.0)*100:.2f}%)")
print(f"  regen eps=0.90 (realistic):       {Wel(0.90):5.0f} W   (eta_elec {eta_elec(0.90)*100:.2f}%)")
print(f"  regen eps=0.95 (optimistic):      {Wel(0.95):5.0f} W   (eta_elec {eta_elec(0.95)*100:.2f}%)")
print(f"  Carnot ceiling (x coil x PE):     {Qsrc*Carnot*eta_coil*eta_pe:5.0f} W   (the hard wall)")
key=np.array([R,eta_mech(0.9),eta_mech(0.95),Pdens(50e-6),Wel(0.9)]).astype(np.float64)
print("="*70); print("RESULT sha256 = "+hashlib.sha256(key.tobytes()).hexdigest())
