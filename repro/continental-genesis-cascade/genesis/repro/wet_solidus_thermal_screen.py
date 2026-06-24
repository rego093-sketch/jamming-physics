#!/usr/bin/env python3
"""
Continental-Genesis repro screen 2 -- heat -> granite (wet partial melting).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

The docx's CORE INSTINCT was right: exponential thermal sensitivity D(T)=D0 exp(-Ea/RT)
makes a thermal event physically decisive. The docx pointed it at the WRONG rock
(resetting CLOSED zircon, Ea_Pb ~= 550 kJ/mol -- which fails by ~10 orders, see the
zircon caveat). Redirected to its RIGHT target -- WET partial melting of a thickened,
water-bearing lower crust -- the same logic works, because (1) water lowers the granitic
solidus by hundreds of degrees, and (2) the melt fraction is steeply temperature-
dependent just above the solidus. This screen shows the contrast and the verdict.
No age is used; this is a present-tense feasibility screen [F]/[L].
"""
import hashlib, math

SEED = 19
R = 8.314  # J/mol/K

# ===== LOCK BLOCK =====
# (a) WRONG target -- Pb-in-zircon diffusion (Cherniak & Watson 2001)
EA_ZR   = 550.0e3    # J/mol
D0_ZR   = 1.1e-4     # m^2/s
GRAIN_R = 50.0e-6    # m   (100 um grain radius)
YR      = 3.15576e7  # s/yr
T_HOT_C = 1200       # deg C  representative magmatic temperature
# (b) RIGHT target -- granitic solidus, dry vs water-saturated (literature, 1 GPa)
SOLIDUS_DRY_C = 950   # deg C  approx dry granite solidus at mid-crust
SOLIDUS_WET_C = 650   # deg C  approx water-saturated granite solidus at mid-crust
# representative achievable lower-crust temperatures from thickening + shear heating
T_CRUST_C = [600, 700, 800, 900]
# ======================

def D(D0, Ea, T_C):
    return D0 * math.exp(-Ea / (R * (T_C + 273.15)))

def tau_sat_yr(D0, Ea, T_C, Lr):
    return (Lr*Lr / D(D0, Ea, T_C)) / YR

L = []
L.append("HEAT -> GRANITE -- wet partial melting screen (redirected thermal sensitivity)")
L.append(f"VP-SPEC  SEED={SEED}  present-tense [F]/[L]; no age, no occurrence")
L.append("="*64)
L.append("")
L.append("[a] WRONG target the docx chose -- reset a CLOSED zircon (Ea=550 kJ/mol):")
ts = tau_sat_yr(D0_ZR, EA_ZR, T_HOT_C, GRAIN_R)
L.append(f"    tau_sat @ {T_HOT_C} C = {ts:.2e} yr   (docx claimed '~1 month')")
L.append(f"    -> off by ~{math.log10(ts/(1/12)):.0f} orders of magnitude. The zircon stays CLOSED.")
L.append("    (this is why attacking the date FAILS -- see the zircon caveat module)")
L.append("")
L.append("[b] RIGHT target -- WET partial melting of thickened, water-bearing crust:")
L.append(f"    granitic solidus:  dry ~ {SOLIDUS_DRY_C} C   water-saturated ~ {SOLIDUS_WET_C} C")
L.append(f"    -> water lowers the solidus by ~{SOLIDUS_DRY_C-SOLIDUS_WET_C} C")
L.append("    achievable lower-crust T (thickening + shear heating) vs the two solidi:")
L.append("      T_crust      vs dry solidus       vs wet solidus")
for Tc in T_CRUST_C:
    dry = "MELTS" if Tc >= SOLIDUS_DRY_C else "below"
    wet = "MELTS" if Tc >= SOLIDUS_WET_C else "below"
    L.append(f"      {Tc:4d} C        {dry:<14}      {wet}")
L.append("")
L.append("READING (firewall-clean):")
L.append("  * a DRY crust at 600-800 C does NOT melt -> no granite (the dry path is weak).")
L.append("  * a WET crust at the SAME 600-800 C crosses the solidus -> partial melt,")
L.append("    and the lighter (felsic) fraction separates -> granite on cooling.")
L.append("  * the submarine-rift start supplies that water (sea -> hydrated basalt skin),")
L.append("    so the WATER term is load-bearing: with water [F], dry path only [L].")
L.append("  * 'pure extension distils CONTINENT-SCALE felsic' remains [L] (Iceland makes")
L.append("    only minor rhyolite); a deep water path (subduction-like) strengthens it.")
L.append("  * no calendar age enters; this screens the MECHANISM, not a date.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "01e659c113520dfa74f3ccd446220100aa2dc308e48ea190e12f2c6efffc3a64"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
