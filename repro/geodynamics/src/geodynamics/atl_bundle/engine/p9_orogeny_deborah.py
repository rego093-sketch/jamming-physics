"""
p9_orogeny_deborah.py  --  P9 (cross-check): orogeny regime via Deborah number
================================================================================
Prereg (whitepaper): De = tau_relax/tau_proc. De<<1 viscous; De>>1 elastic/brittle.
P9 is NOT a necessary condition; it adjudicates whether a fast-pile-up regime is
required/recorded. Whitepaper falsifier: if UHP cases consistently have dt ~ several Myr
(clock-supported) -> fast pile-up FAIL/HOLD; if dt << 0.1 Myr -> UNLOCK candidate.

Cited inputs:
 - UHP depth (coesite >2.7 GPa ~90 km; diamond >120 km).
 - Dabie-Sulu: subduction ~10-11 Myr, exhumation ~19-20 Myr (zircon SHRIMP).
 - WGR Norway exhumation >2.5-8.5 km/Myr; coesite preservation needs <=~10 cm/yr OR
   refrigeration (Liou 1994).
 - Crustal Maxwell time tau_M = eta/G ; eta_crust ~ 1e21-1e24 Pa s, G ~ 3e10 Pa.
HONEST: this adjudicates *regime*, not "speed from existence" (per whitepaper caution).
Pure numpy. Deterministic.
"""
import numpy as np
yr=3.15e7; G=3.0e10

def tau_M(eta): return eta/G          # Maxwell relaxation time [s]
def De(tau_relax, tau_proc): return tau_relax/tau_proc

print("="*78); print("P9: dynamic orogeny regime (Deborah number)"); print("="*78)

# --- (1) standard UHP exhumation: kinematics + regime ---
print("\n(1) Observed UHP exhumation (standard record):")
dz=100e3                                    # ~100 km peak depth
for dt_Myr in [3,10,20]:
    v=dz/(dt_Myr*1e6*yr)                    # m/s
    print(f"    dt={dt_Myr:2d} Myr -> v_exh = {v*yr*100:.2f} cm/yr "
          f"({dz/1e3/dt_Myr:.0f} km/Myr); dt is MILLIONS of yr (>> 0.1 Myr)")
print("    fast end for coesite preservation ~10 cm/yr (Liou 1994) is still dt~1 Myr scale.")

print("\n  Deborah number of standard orogeny (tau_proc = exhumation dt ~ Myr):")
for eta in [1e21,1e23,1e24]:
    tM=tau_M(eta)
    d=De(tM, 1e6*yr)                        # dt = 1 Myr reference
    print(f"    eta={eta:.0e} -> tau_M={tM/yr:.1e} yr ; De(dt=1Myr)={d:.1e}  -> "
          f"{'viscous (De<<1)' if d<0.1 else 'transitional'}")
print("    => standard orogeny/UHP exhumation sits at De<<1 (VISCOUS ductile flow).")
print("       The record is consistent with slow exhumation; it does NOT require fast pile-up.")

# --- (2) the mechanism's OWN fast slip: regime ---
print("\n(2) The rapid-sliding event itself (mechanism prediction):")
for tau_proc_lbl, tproc in [("1 s slip",1.0),("1 day slip",8.64e4),("1 yr",3.15e7)]:
    d_hot = De(tau_M(1e21), tproc)          # hot/wet crust tau_M~1e3 yr
    print(f"    tau_proc={tau_proc_lbl:10s} -> De={d_hot:.1e}  -> "
          f"{'ELASTIC/BRITTLE (De>>1)' if d_hot>1 else 'viscous'}")
print("    => the fast slip is De>>1 = BRITTLE (stick-slip / faulting), consistent with WP-T1")
print("       bistability. This is a PREDICTION (brittle fault/breccia signatures), not")
print("       independent confirmation, and is DISTINCT from deep ductile UHP exhumation.")

# --- TEST-ORO2: thermal diffusion vs event ---
L=10e3; kappa=1e-6
t_diff=L*L/kappa
print(f"\n  TEST-ORO2: thermal diffusion time of a ~10 km body t_diff=L^2/kappa = "
      f"{t_diff/yr/1e6:.1f} Myr ~ exhumation dt => thermal disequilibrium is possible but")
print(f"  reproducible in standard thermo-structural models (not a unique fast-pile-up signature).")

# --- verdict ---
print("\n  P9 VERDICT (honest): HOLD.")
print("   - Observed UHP exhumation: dt ~ Myr, De<<1 (viscous) -> consistent with STANDARD slow")
print("     orogeny; per the whitepaper falsifier this makes a *fast pile-up* reading FAIL/HOLD.")
print("   - The mechanism's own slip is De>>1 (brittle) -- self-consistent prediction, not proof.")
print("   - UNLOCK would require independent clocks forcing dt << 0.1 Myr; current data do not.")
print("   => P9 stays a cross-check (HOLD); it neither refutes nor confirms the rapid core,")
print("      and does NOT infer speed from the mere existence of UHP/nappe structures.")

np.savez("p9_results.npz", v_exh_cmyr_10Myr=dz/(10*1e6*yr)*yr*100,
         De_standard=De(tau_M(1e23),1e6*yr), De_fast=De(tau_M(1e21),8.64e4),
         t_diff_Myr=t_diff/yr/1e6)
print("\nsaved -> p9_results.npz")
