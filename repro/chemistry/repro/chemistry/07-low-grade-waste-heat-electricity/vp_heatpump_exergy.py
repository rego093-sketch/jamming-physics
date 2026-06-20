# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.9b heat-pump/engine inversion; exergy ceiling
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: 64e26ee6...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
Can we heat-pump AC-condenser heat UP and generate electricity? Honest physics.
1) Exergy ceiling: max convertible fraction of low-grade heat = 1 - T0/T  (absolute, any method).
2) Heat pump & heat engine are INVERSES (COP x eta_Carnot = 1) -> chaining cancels; reversibly it only
   recovers the waste heat's exergy (returning the pump electricity); really it nets NEGATIVE.
3) 'Collecting better' raises QUANTITY (more total electricity at same low %), not EFFICIENCY.
4) The real prize hidden in the instinct: better heat REJECTION raises AC COP -> electricity SAVED
   (negawatts) >> electricity generated. Huge in hot climates (India).
Deterministic + sha256.
"""
import numpy as np, hashlib

T0 = 298.0   # ambient 25C

# ---------- (1) exergy ceiling ----------
Tc = np.linspace(305, 423, 300)         # source temp K (32..150C)
exergy = 1 - T0/Tc
def ex(c): return 1 - T0/(c+273.15)
print("="*66); print("EXERGY CEILING (max heat->electricity, ANY method incl. heat pump)")
for c in [40,50,60,80,100,150]:
    print(f"  {c:3d}C waste heat: ceiling {ex(c)*100:4.1f}%  (real device ~ a third to half of this)")

# ---------- (2) does the heat pump help? net per unit WASTE heat ----------
Tcond = 50.0                  # AC condenser temp (hot climate)
ceil = ex(Tcond)              # 7.7%
# direct bottoming ORC on the condenser (real)
direct_orc = 0.03             # ~3% of waste heat -> electricity (real, no heat pump)
# heat-pump upgrade 50->150C then ORC (real)
COP_real = 2.2; orc150 = 0.10
W_pump = 1.0/COP_real; Qcold = 1.0 - W_pump; Wout = 1.0*orc150
net_hp_real = (Wout - W_pump)/Qcold      # net electricity per unit waste heat
# heat-pump loop reversible -> equals exergy ceiling (no advantage)
net_hp_rev = ceil
print("="*66); print("DOES THE HEAT PUMP HELP?  (net electricity per unit waste heat)")
print(f"  exergy ceiling (any method)          : {ceil*100:+5.1f}%")
print(f"  direct bottoming ORC (real, no pump) : {direct_orc*100:+5.1f}%")
print(f"  heat-pump UPGRADE + ORC (reversible) : {net_hp_rev*100:+5.1f}%  (= ceiling, NO advantage)")
print(f"  heat-pump UPGRADE + ORC (real)       : {net_hp_real*100:+5.1f}%  (LOSS: pump eats more than engine makes)")
print(f"  => heat pump & engine are inverses (COP x eta_Carnot = 1); chaining cannot generate net")

# ---------- (3) the real prize: AC COP vs condenser temperature ----------
Tcd = np.linspace(33, 62, 300)          # condenser temp C
Tevap = 280.0                            # evaporator ~7C
cop_carnot = Tevap/((Tcd+273.15)-Tevap)
cop_real = 0.45*cop_carnot               # 2nd-law ~0.45
def cop(c): return 0.45*(Tevap/((c+273.15)-Tevap))
print("="*66); print("THE REAL PRIZE: better heat REJECTION raises AC COP (electricity SAVED)")
for c in [60,50,40,35]:
    print(f"  condenser {c}C: AC COP ~ {cop(c):.1f}  -> elec/cooling = {1/cop(c):.3f}")
print(f"  lowering condenser 50C->35C: COP {cop(50):.1f}->{cop(35):.1f} = {(1-cop(50)/cop(35))*100:.0f}% less electricity")

# ---------- (4) verdict: per unit CONDENSER heat ----------
# saved by COP 2.9->4.5 (50->35C): per unit Q_hot
c1,c2 = cop(50),cop(35)
# Q_hot = Q_cool(1+1/COP); W_ac=Q_cool/COP ; per unit Q_hot at COP c1:
Qcool_per_Qhot = 1/(1+1/c1)
saved = Qcool_per_Qhot*(1/c1 - 1/c2)     # electricity saved per unit Q_hot
generated = direct_orc                    # via bottoming ORC
print("="*66); print("VERDICT (electricity per unit CONDENSER heat)")
print(f"  better heat rejection (SAVED, negawatts) : {saved*100:+5.1f}%   <-- biggest, free")
print(f"  direct bottoming ORC (GENERATED)         : {generated*100:+5.1f}%")
print(f"  heat-pump upgrade + generate             : {net_hp_real*100:+5.1f}%   (loss)")

key=np.concatenate([exergy,cop_real,[net_hp_real,saved,generated]]).astype(np.float64)
print("="*66); print(f"RESULT sha256 = {hashlib.sha256(key.tobytes()).hexdigest()}")
