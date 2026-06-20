# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.12 data-centre economics
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: 13d054c5...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
Data-center / large-cooling case: where the thermomagnetic harvester's economics make sense.
1 MW IT data center in a hot region. 24/7/365. Reject heat ~50C (low grade) -> harvester.
Key: lots of hours + big reject heat + in HOT regions there's NO heat-reuse demand -> electricity is the only valorization.
Power, payback, CO2. Deterministic + sha256.
"""
import numpy as np, hashlib

# ---- data center ----
IT=1000.0                      # kW IT load
COP=3.5                        # efficient chiller (hot region)
Pcool=IT/COP                   # kW cooling electrical
Qrej=IT+Pcool                  # kW reject heat (IT + chiller work)
# harvester at dT~20K (reject 50C, sink 30C via evaporative): Carnot 6.2%, eff-opt regen
Carnot=20/323.0
eta_mech=0.577*Carnot          # eff-opt regen ~ 58% of Carnot
eta_elec=eta_mech*0.6*0.85
Pgen=eta_elec*Qrej             # kW electrical
PUE0=(IT+Pcool)/IT; PUE1=(IT+Pcool-Pgen)/IT
print("="*66); print("1 MW DATA CENTER (hot region, COP 3.5):")
print(f"  cooling draws {Pcool:.0f} kW ; rejects {Qrej:.0f} kW heat (~50C, low grade)")
print(f"  Carnot(dT=20K)={Carnot*100:.1f}% -> eta_mech {eta_mech*100:.2f}% -> eta_elec {eta_elec*100:.2f}%")
print(f"  HARVESTER output = {Pgen:.1f} kW continuous  (= {Pgen/Pcool*100:.0f}% of cooling electricity)")
print(f"  PUE: {PUE0:.3f} -> {PUE1:.3f}")

# ---- annual (24/7/365) ----
hours=8760.0; price=0.10; gco2=0.7
MWh=Pgen*hours/1000.0
print("="*66); print(f"ANNUAL (24/7 = {hours:.0f} h, ${price}/kWh, {gco2} kgCO2/kWh):")
print(f"  energy {MWh:.0f} MWh/yr -> ${MWh*1000*price:,.0f}/yr , {MWh*gco2:.0f} t CO2/yr")

# ---- capital & payback ----
mass=900.0                     # kg magnetocaloric (eff-opt)
cap_lo,cap_hi=90000,130000; cap=110000
save_yr=MWh*1000*price
print("="*66); print("CAPITAL & PAYBACK:")
print(f"  ~{mass:.0f} kg magnetocaloric + magnets + regenerator + coils + pump + power electronics")
print(f"  system capital ~ ${cap_lo:,}-{cap_hi:,} (mid ${cap:,})")
print(f"  annual saving ${save_yr:,.0f}/yr -> payback {cap/save_yr:.1f} yr (range {cap_lo/save_yr:.1f}-{cap_hi/save_yr:.1f})")
print(f"  15-yr net ~ ${15*save_yr-cap:,.0f} ; 15-yr CO2 {15*MWh*gco2:,.0f} t")
# price sensitivity
print(f"  payback @ $0.07/kWh: {cap/(MWh*1000*0.07):.1f} yr ; @ $0.15/kWh: {cap/(MWh*1000*0.15):.1f} yr")

# ---- residential vs data center contrast ----
res_W=109; res_h=2500; res_yr=res_W*res_h/1000*price
print("="*66); print("WHY DATA CENTER (vs a home AC):")
print(f"  home AC : {res_W} W, {res_h} h/yr -> ${res_yr:.0f}/yr (hardware cost >> saving: no payback)")
print(f"  data ctr: {Pgen*1000:.0f} W, {hours:.0f} h/yr -> ${save_yr:,.0f}/yr (pays back ~{cap/save_yr:.0f} yr)")
key=np.array([Pgen,MWh,save_yr,cap/save_yr,PUE1]).astype(np.float64)
print("="*66); print("RESULT sha256 = "+hashlib.sha256(key.tobytes()).hexdigest())
