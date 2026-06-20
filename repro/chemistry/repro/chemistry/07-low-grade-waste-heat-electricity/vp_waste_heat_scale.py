# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.12 fleet scale
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: b59d22a5...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
How much does the thermomagnetic harvester save in VERY HOT regions (India scale)?
Honest per-unit + fleet, and compared to the bigger lever (efficiency / negawatts).
Grounded: India ~110M room ACs; AC ~25-30% of peak; coal-heavy grid.
"""
import numpy as np, hashlib

# ---- representative 1-ton AC in a very hot region ----
Qcool=3500.0; COP=2.8                      # cooling W; real hot-climate COP
Pac=Qcool/COP                               # AC electrical draw
Qrej=Qcool+Pac                              # reject heat
eta_elec=0.023                              # harvester wall-plug eff (eff-optimized regen design)
Pgen=eta_elec*Qrej                          # harvester output
frac_h=Pgen/Pac
# efficiency / negawatts lever (super-efficient AC + better heat rejection): ~30% of draw
sav_eff=0.30*Pac
# combined (efficiency first, then harvest the reduced reject heat)
Pac2=Pac-sav_eff; Qrej2=Qcool+Pac2; Pgen2=eta_elec*Qrej2
sav_comb=sav_eff+Pgen2
print("="*66); print("PER 1-TON AC (very hot region, COP=2.8):")
print(f"  AC draws {Pac:.0f} W ; rejects {Qrej:.0f} W heat")
print(f"  HARVESTER generates {Pgen:.0f} W  = {frac_h*100:.1f}% of the AC's electricity")
print(f"  EFFICIENCY (better AC + heat rejection) saves {sav_eff:.0f} W = 30%")
print(f"  COMBINED saves {sav_comb:.0f} W = {sav_comb/Pac*100:.0f}%")

# ---- annual (very hot region: ~2500 cooling-hours/yr) ----
hours=2500.0; price=0.08; gco2=0.7          # $/kWh ; kgCO2/kWh (coal-heavy)
def yr(Pw): return Pw*hours/1000.0          # kWh/yr
kwh_h, kwh_e = yr(Pgen), yr(sav_eff)
print("="*66); print(f"ANNUAL per unit ({hours:.0f} h/yr, ${price}/kWh, {gco2} kgCO2/kWh):")
print(f"  harvester : {kwh_h:.0f} kWh -> ${kwh_h*price:.0f}/yr , {kwh_h*gco2:.0f} kg CO2/yr")
print(f"  efficiency: {kwh_e:.0f} kWh -> ${kwh_e*price:.0f}/yr , {kwh_e*gco2:.0f} kg CO2/yr")

# ---- India fleet (110 million room ACs) ----
N=110e6
TWh_h, TWh_e = N*kwh_h/1e9, N*kwh_e/1e9
Mt_h, Mt_e = N*kwh_h*gco2/1e9, N*kwh_e*gco2/1e9
GW_h, GW_e = N*Pgen/1e9, N*sav_eff/1e9
print("="*66); print(f"INDIA FLEET (~{N/1e6:.0f}M room ACs):")
print(f"  harvester : {TWh_h:.0f} TWh/yr , {Mt_h:.0f} Mt CO2/yr , ~{GW_h:.0f} GW peak shaved (if universal)")
print(f"  efficiency: {TWh_e:.0f} TWh/yr , {Mt_e:.0f} Mt CO2/yr , ~{GW_e:.0f} GW peak (the policy lever)")
print(f"  context: India AC peak ~70 GW now -> ~180 GW by 2035 (~30% of national peak)")
key=np.array([Pgen,sav_eff,kwh_h,TWh_h,Mt_h,GW_h]).astype(np.float64)
print("="*66); print("RESULT sha256 = "+hashlib.sha256(key.tobytes()).hexdigest())
