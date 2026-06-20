# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.10 bare-device design, eta~0.4%
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: 0a3af6ec...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
Concrete engineering design: self-oscillating thermomagnetic generator for AC-condenser-grade heat.
Real SI units, real material properties. Honest efficiency (Carnot-bounded) and real coil EMF.
Material: a tuned magnetocaloric alloy La(Fe,Si,Mn)13 with a SHARP (first-order) transition at Tc~37C.
(Pure Gd's Tc=20C is too low for a 25-50C window; La-Fe-Si / FeNiCr alloys tune Tc into 40-60C with a sharp dM.)
"""
import numpy as np, hashlib

# ---------------- material (tuned magnetocaloric alloy, sharp transition) ----------------
Tc   = 310.0          # Curie temp, K (37 C) -- tuned
wt   = 3.0            # transition width, K (sharp, first-order-like)
Ms   = 1.0e6         # saturation magnetization, A/m  (mu0*Ms = 1.26 T)
rho  = 7200.0        # density, kg/m^3
cp   = 500.0         # sensible specific heat, J/(kg K)
Lh   = 3000.0        # latent heat of the first-order transition, J/kg (paid once per cycle)
mu0  = 4e-7*np.pi
def Mof(T): return Ms/(1.0+np.exp((T-Tc)/wt))     # magnetization vs T

# ---------------- operating point (AC condenser) ----------------
Tcold, Thot = 298.0, 323.0     # 25 C sink, 50 C condenser ; available dT = 25 K
dB    = 0.35                    # field swing seen by the tip over its stroke (NdFeB N42), T
Carnot_avail = (Thot-Tcold)/Thot

# ---------------- efficiency vs the element's thermal swing (key design insight) ----------------
dTsw = np.linspace(2, 40, 400)                      # element temperature swing across Tc
dM   = Mof(Tc-dTsw/2) - Mof(Tc+dTsw/2)              # magnetization swing achieved
w_den= dM*dB                                        # magnetic work density per cycle, J/m^3
q_den= rho*(cp*dTsw + Lh)                            # sensible + latent heat per cycle, J/m^3
eta  = w_den/q_den                                  # device efficiency
i_opt= np.argmax(eta)
print("="*70)
print("EFFICIENCY (device is Carnot-bounded; sensible+LATENT heat per cycle is the cost)")
print(f"  available dT = 25 K -> Carnot ceiling = {Carnot_avail*100:.1f}%")
print(f"  best device eta = {eta[i_opt]*100:.2f}% at element swing dTsw = {dTsw[i_opt]:.0f} K")
print(f"  => design the thermal coupling so the TIP swings ~{dTsw[i_opt]:.0f} K across Tc (not the full 25 K)")

# ---------------- the design point (at the efficiency peak) ----------------
dTsw_d = float(dTsw[i_opt])
dM_d   = Mof(Tc-dTsw_d/2)-Mof(Tc+dTsw_d/2)
w_d    = dM_d*dB
eta_d  = w_d/(rho*(cp*dTsw_d+Lh))
print("="*70); print(f"DESIGN POINT: tip swing {dTsw_d:.0f} K -> dM = {dM_d:.2e} A/m, work density {w_d:.2e} J/m^3, eta = {eta_d*100:.2f}% ({eta_d/Carnot_avail*100:.0f}% of Carnot)")

# ---------------- single unit: plate + magnet + coil ----------------
Lx,Ly = 0.020,0.020                 # 20 x 20 mm plate
th     = 0.5e-3                       # 0.5 mm thick
V      = Lx*Ly*th                     # volume
mass   = rho*V
Asurf  = 2*Lx*Ly                      # both faces
h_htc  = 1000.0                       # heat-transfer coeff (good contact/convection), W/m^2K
# cycling frequency: limited by heating/cooling the tip by dTsw_d, driven by ~ (dT_avail) gradient
tau_th = (rho*cp*V)/(h_htc*Asurf) * (dTsw_d/(Thot-Tcold))   # effective thermal time for the swing
f      = 1.0/(4*tau_th)              # ~quarter-cycle per swing
Pmech  = w_d*V*f                     # mechanical power per unit
eta_coil = 0.6                       # electrical extraction efficiency (matched coil/load)
Pelec  = Pmech*eta_coil
Qthru  = rho*(cp*dTsw_d+Lh)*V*f      # heat throughput per unit (sensible + latent)
print("="*70); print("SINGLE UNIT (plate + NdFeB N42 + copper pickup coil)")
print(f"  plate 20x20x0.5 mm, mass {mass*1e3:.2f} g")
print(f"  cycling frequency f = {f:.2f} Hz   (thin films -> several Hz)")
print(f"  mechanical power = {Pmech*1e3:.1f} mW ; electrical (coil) = {Pelec*1e3:.1f} mW ; heat throughput = {Qthru:.2f} W")

# coil EMF
Aelem = Lx*Ly
coupling = 0.4
dPhi = coupling*mu0*dM_d*Aelem        # flux swing linked by coil
N    = 5000
EMF  = N*dPhi/(1.0/(2*f))             # average EMF over a half-cycle
Iout = Pelec/max(EMF,1e-9)
print(f"  coil N = {N} turns (copper) -> EMF ~ {EMF:.2f} V (boost converter to charge battery), I ~ {Iout*1e3:.0f} mA")

# module
pitch = 0.022
units = int(1.0/pitch)**2
Pmod  = Pelec*units
Qmod  = Qthru*units
print("="*70); print("MODULE (1 m^2 panel on a condenser)")
print(f"  ~{units} units -> electrical ~ {Pmod:.0f} W  from heat throughput ~ {Qmod/1e3:.1f} kW  (eta {eta_d*100:.2f}%)")
print(f"  use: self-powered sensors / IoT / trickle charge; NOT primary power. Regeneration is the eta lever.")
print(f"  copper here = the coil winding only (non-magnetic); the active element is the Curie-point alloy.")

key=np.concatenate([eta,[eta_d,f,Pelec,EMF,Pmod]]).astype(np.float64)
print("="*70); print("RESULT sha256 = "+hashlib.sha256(key.tobytes()).hexdigest())

# thickness sweep for panel C
th_s=np.linspace(0.05e-3,2.0e-3,200)
V_s=Lx*Ly*th_s
tau_s=(rho*cp*V_s)/(h_htc*Asurf)*(dTsw_d/(Thot-Tcold))
f_s=1/(4*tau_s)
P_s=w_d*V_s*f_s*eta_coil
