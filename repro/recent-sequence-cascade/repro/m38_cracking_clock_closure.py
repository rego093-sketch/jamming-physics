#!/usr/bin/env python3
"""
M38 - TWO CLOCKS: THERMAL vs GEOLOGICAL SURVIVAL OF AN OIL ACCUMULATION  (SH-60)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

*** CORRECTED after self-audit (biased thermal-only framing found and fixed). ***
The PRIOR version computed only the THERMAL cracking time (~1 Gyr at 90C) and concluded
"oil survives deep time, so its presence is uninformative -> no recency edge." That was
sloppy and one-sided: it ignored that the TRAP and RESERVOIR ROCK do not survive a billion
years. A shallow/moderate accumulation is destroyed far sooner by the ROCK CYCLE - either
buried deeper and cooked to gas/graphite, or exhumed and eroded and the oil lost/biodegraded
at surface. (Cf. Babylon: a surface structure is buried/erased on millennial scales;
geological structures on 10^6-10^8 yr scales.) The BINDING clock is the shorter one.

PRESENT-TENSE COMPARISON (both clocks are date-free survival timescales [V]; using either
to assign an ABSOLUTE age is [O]):
  THERMAL clock  tau_T(90C)   ~ Gyr        (loose upper bound on the oil MOLECULE)
  GEOLOGICAL clock tau_G = overburden / exhumation_rate, both PRESENT-TENSE measured.
For a typical few-km trap and a typical exhumation rate, tau_G ~ 10^7-10^8 yr << tau_T.

CONSEQUENCE: the presence of a PRODUCIBLE shallow oil accumulation NOW bounds its residence
BELOW the rock-cycle destruction time ~ tau_G, i.e. far below a Gyr. This REFUTES "billion-
year retention" - a reading my prior module wrongly leaned on, and one the mainstream does
NOT hold either (mainstream source rocks are ~10^7-10^8 yr, within tau_G, with active
re-migration/loss). BUT tau_G ~ 10^7-10^8 yr does NOT pin "recent": 10^8 yr also satisfies
it. So the absolute residence stays [O]/RECORD, BOTH directions.

LOCK (present-tense; measured kinetics identical to M27; representative present rates/depths):
  A   = 1.0e13 /s   Ea = 220.0e3 J/mol   R = 8.314 J/mol/K   T_RES = 90.0 C
  OVERBURDEN_KM band = 2.0 .. 4.0 km      EXHUMATION_MM_YR band = 0.05 .. 0.30 mm/yr
SEED = 19. Double-SHA-256 self-gate.
"""
import os, math, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
A, EA, RGAS = 1.0e13, 220.0e3, 8.314
T_RES_C = 90.0
SEC_PER_YR = 3.15576e7
OVB_LO, OVB_HI = 2.0, 4.0          # km of overburden over a moderate trap
EXH_LO, EXH_HI = 0.05, 0.30        # mm/yr, present-tense exhumation/erosion rates

def tau_thermal_years(T_c):
    T = T_c + 273.15
    k = A * math.exp(-EA / (RGAS * T))
    return (1.0 / k) / SEC_PER_YR

tau_T = tau_thermal_years(T_RES_C)
# geological destruction time = overburden / exhumation rate (present-tense quantities)
def tau_geol_years(ovb_km, exh_mm_yr):
    return (ovb_km * 1e6) / exh_mm_yr      # (km->mm) / (mm/yr) = yr
tg_fast = tau_geol_years(OVB_LO, EXH_HI)   # thin cover, fast erosion -> shortest
tg_slow = tau_geol_years(OVB_HI, EXH_LO)   # thick cover, slow erosion -> longest

def fmt(y):
    if y >= 1e9: return f"{y/1e9:.2f} Gyr"
    if y >= 1e6: return f"{y/1e6:.1f} Myr"
    if y >= 1e3: return f"{y/1e3:.1f} kyr"
    return f"{y:.0f} yr"

L = []
L.append("M38  TWO CLOCKS: THERMAL vs GEOLOGICAL SURVIVAL  (SH-60, CORRECTED)")
L.append(f"SEED={SEED}   T_RES={T_RES_C:.0f}C   kinetics A={A:.0e}/s Ea={EA/1e3:.0f}kJ/mol (=M27)")
L.append("")
L.append("[THERMAL CLOCK - oil molecule]:")
L.append(f"  tau_T(90C) = {fmt(tau_T)}   (loose UPPER bound; the molecule alone)")
L.append("")
L.append("[GEOLOGICAL CLOCK - trap/rock survival]  (present-tense rates x depths):")
L.append(f"  overburden {OVB_LO:.0f}-{OVB_HI:.0f} km / exhumation {EXH_LO:.2f}-{EXH_HI:.2f} mm/yr")
L.append(f"  tau_G = {fmt(tg_fast)} (thin/fast)  ..  {fmt(tg_slow)} (thick/slow)")
L.append(f"  -> tau_G ~ 10^7-10^8 yr  <<  tau_T ~ {fmt(tau_T)}.  The GEOLOGICAL clock BINDS.")
L.append("")
L.append("[VERDICT]  (corrected, symmetric):")
L.append("  A producible shallow accumulation existing NOW means the trap+rock have NOT been")
L.append("  destroyed by burial-metamorphism or exhumation-erosion -> residence is bounded")
L.append("  BELOW tau_G, i.e. FAR below a Gyr. This REFUTES 'billion-year retention'.")
L.append("  -> My prior module leaned on Gyr-retention ('oil survives deep time, no problem').")
L.append("     That is WITHDRAWN: it was thermal-only and ignored the rock cycle. The user's")
L.append("     Persian-Gulf/Babylon objection is correct on the physics.")
L.append("  -> BUT the firewall holds BOTH ways: tau_G ~ 10^7-10^8 yr is ALSO satisfied by a")
L.append("     ~10^8 yr residence (the mainstream value), not only by a recent one. So the")
L.append("     ABSOLUTE residence (recent vs 10^8) stays [O]/RECORD. The rock cycle kills the")
L.append("     Gyr reading; it does NOT, by itself, establish recency.")
L.append("  => Net standing of the clock: present-tense bound residence << rock cycle [V];")
L.append("     deep-time-vs-recent discrimination [O], both directions.")
L.append("")
L.append("GRADE: SH-60 - geological clock binds below the rock cycle [V] (Gyr-retention")
L.append("       REFUTED, prior framing retracted); absolute residence [O] both ways.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "a6631c170e1d07a7eca131a8dd7b4b34e2ca231690b6388c2ed61653f6803489"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
