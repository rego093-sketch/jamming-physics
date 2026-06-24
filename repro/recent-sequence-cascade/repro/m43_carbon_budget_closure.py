#!/usr/bin/env python3
"""
M43 - CARBON BUDGET CLOSURE: does the source rock hold enough carbon for the oil?
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE inputs.

THE 'ONE EVENT' COUPLING, AS A NUMBER. If the cascade deposited the source rock and that
source charged the giant fields, the organic carbon physically present in the source must
SUFFICE to generate the known oil-in-place. This is a mass-balance the coupling must pass.
All quantities are present-tense measured (TOC, thickness, area, oil volume); no rate or
date enters. Timing stays [O].

METHOD (present-tense, order-of-magnitude):
  rock volume   = thickness x area
  rock mass     = volume x rock_density
  organic C     = rock mass x TOC
  expelled oil  = organic C x generation-expulsion efficiency (good marine source ~15-30%)
  oil volume    = oil mass / oil_density
  CLOSE if generated oil >= known oil-in-place (within an order of magnitude).

We run a GENERIC world-class source kitchen and compare to giant-province oil-in-place.

LOCK (present-tense, curated ranges):
  TOC = 0.05 (5%)            thickness = 50 m         area = 1.0e11 m^2 (1e5 km^2 kitchen)
  rock_density = 2400 kg/m^3 oil_density = 850 kg/m^3 bbl_per_m3 = 6.2898
  eff_lo, eff_hi = 0.15, 0.30  (generation x expulsion efficiency, marine type II)
  OIP_giant_Gbbl = 100 .. 900  (in-place range spanned by single giant provinces)
SEED = 19. Double-SHA-256 self-gate.
"""
import os, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
TOC = 0.05; THICK = 50.0; AREA = 1.0e11
RHO_ROCK = 2400.0; RHO_OIL = 850.0; BBL = 6.2898
EFF_LO, EFF_HI = 0.15, 0.30
OIP_LO_G, OIP_HI_G = 100.0, 900.0   # Gbbl in-place, single giant province span

vol_rock = THICK*AREA                       # m^3
mass_rock = vol_rock*RHO_ROCK               # kg
org_C = mass_rock*TOC                        # kg C
def gen_bbl(eff):
    oil_mass = org_C*eff
    return (oil_mass/RHO_OIL)*BBL/1e9        # Gbbl
gen_lo, gen_hi = gen_bbl(EFF_LO), gen_bbl(EFF_HI)

out = []
out.append("M43  CARBON BUDGET CLOSURE  (present-tense mass balance; SEED=19)")
out.append("")
out.append("[SOURCE KITCHEN  (generic world-class)]:")
out.append(f"  TOC={TOC*100:.0f}%  thickness={THICK:.0f} m  area={AREA:.0e} m^2 (1e5 km^2)")
out.append(f"  rock volume = {vol_rock:.2e} m^3 ; rock mass = {mass_rock:.2e} kg")
out.append(f"  organic carbon present = {org_C:.2e} kg C")
out.append("")
out.append("[GENERATED OIL  (organic C x generation-expulsion efficiency)]:")
out.append(f"  efficiency {EFF_LO:.0%}-{EFF_HI:.0%}  ->  generated oil = {gen_lo:.0f} - {gen_hi:.0f} Gbbl")
out.append("")
out.append("[COMPARE to giant-province OIL-IN-PLACE]:")
out.append(f"  single giant province in-place span = {OIP_LO_G:.0f} - {OIP_HI_G:.0f} Gbbl")
closes = gen_hi >= OIP_LO_G
out.append("")
out.append("[VERDICT]:")
if closes:
    out.append(f"  CLOSES. A 1e5 km^2, 5% TOC, 50 m kitchen generates ~{gen_lo:.0f}-{gen_hi:.0f} Gbbl -")
    out.append(f"  the SAME ORDER as a giant province's in-place oil ({OIP_LO_G:.0f}-{OIP_HI_G:.0f} Gbbl).")
    out.append("  The organic carbon physically present in a cascade-deposited source rock is")
    out.append("  SUFFICIENT to charge the giant accumulations. The 'one event' coupling passes")
    out.append("  the carbon mass-balance at order-of-magnitude. [V] (present-tense quantities).")
else:
    out.append("  SHORTFALL - would need a larger kitchen or higher efficiency. Logged honestly.")
out.append("")
out.append("  Note (honest): this shows SUFFICIENCY, not uniqueness - mainstream source rocks")
out.append("  close the same budget (it is the same rock). What it rules OUT is the objection")
out.append("  'there isn't enough carbon for one-event charging' - there is. It also scales:")
out.append("  larger kitchens (Arabian-scale, ~1e6 km^2) over-supply by ~10x, consistent with")
out.append("  expulsion/migration losses. Timing/occurrence remain [O], both directions.")
out.append("")
out.append("[GRADE] carbon mass-balance CLOSES at order-of-magnitude [V]; removes the")
out.append("  'insufficient carbon' objection to one-event charging; non-unique; timing [O].")

body = "\n".join(out)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "2f44f336226e05b9f6891eedf56394ec713f5d247ec35a21e653a481d194c831"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
