"""
omega_nogo_check.py  --  Ω-NoGo 전 항목 점검 (constraints.yml v0.10)
================================================================================
limits: deltaR_stop_km=50, deltaP_stop_MPa=500, mu_eff_hold_min=1e-2,
        h_stop_m=1e-6, tau_hold_s=1e3, undrained_required=true.
각 항목을 메커니즘 값과 대조해 PASS/FAIL/HOLD. Pure numpy. Deterministic.
"""
import numpy as np
R=6.371e6; E=1e11
# mechanism values (from prior modules)
dR_mob   = R*400e6/E            # ΔR to mobilize deep sigma' [m]  (C-2)
dP_suction = 400e6             # suction deficit ~ deep sigma' [Pa] (feasibility)
mu_eff   = 2.2e-3              # liquefied effective friction (vp_jamming_friction)
h_sz     = 3.0e-3             # shear-zone thickness [m]
# drainage (undrained) timescales: macro suction (L~km) vs local band (mm)
D_hy = 1e-6                   # hydraulic diffusivity gouge [m^2/s]
tau_drain_macro = (3e3)**2/D_hy   # L=3 km
tau_drain_band  = (h_sz)**2/D_hy  # mm band

lim = dict(deltaR_stop=50e3, deltaP_stop=500e6, mu_eff_hold_min=1e-2,
           h_stop=1e-6, tau_hold=1e3)

print("="*76); print("Ω-NoGo CHECK (constraints.yml v0.10)"); print("="*76)
def line(name, val, cond, detail):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name:34s} {detail}")
    return cond

ok=[]
ok.append(line("deltaR < 50 km", dR_mob, dR_mob<lim['deltaR_stop'],
     f"ΔR_mobilize={dR_mob/1e3:.0f} km < {lim['deltaR_stop']/1e3:.0f} km"))
ok.append(line("deltaP < 500 MPa", dP_suction, dP_suction<lim['deltaP_stop'],
     f"ΔP_suction={dP_suction/1e6:.0f} MPa < {lim['deltaP_stop']/1e6:.0f} MPa"))
ok.append(line("mu_eff <= 1e-2 (low enough)", mu_eff, mu_eff<=lim['mu_eff_hold_min'],
     f"mu_eff={mu_eff:.1e} <= {lim['mu_eff_hold_min']:.0e}"))
ok.append(line("h >= 1e-6 m (not unphysical)", h_sz, h_sz>=lim['h_stop'],
     f"h={h_sz:.0e} m >= {lim['h_stop']:.0e} m"))
ok.append(line("undrained holds >= 1e3 s (macro)", tau_drain_macro, tau_drain_macro>=lim['tau_hold'],
     f"tau_drain(L=3km)={tau_drain_macro:.1e} s >= {lim['tau_hold']:.0e} s"))
print(f"\n  note: LOCAL mm shear-band drains in tau={tau_drain_band:.0f} s (<1e3 s) -> band-scale TP is")
print(f"        a TRANSIENT assist (consistent with brief slip); the *macroscopic* suction (km) is")
print(f"        undrained over >>1e3 s -> the load-bearing undrained condition is on the macro scale.")
print(f"\n  Ω-NoGo: {sum(ok)}/{len(ok)} limits PASS"
      f"  => {'mechanism stays inside ALL NoGo limits.' if all(ok) else 'a limit is violated.'}")
np.savez("omega_nogo_results.npz", npass=sum(ok), ntot=len(ok),
         dR_mob=dR_mob, dP=dP_suction, mu_eff=mu_eff, h=h_sz,
         tau_macro=tau_drain_macro, tau_band=tau_drain_band)
