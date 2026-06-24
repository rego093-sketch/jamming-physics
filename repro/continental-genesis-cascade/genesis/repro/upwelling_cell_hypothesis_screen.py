#!/usr/bin/env python3
"""
Continental-Genesis repro screen 14 -- the mid-Pacific upwelling-cell hypothesis (CORRECTED v2).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19. PRESENT-TENSE only; dates/sequences RECORD both ways.

THE AUTHOR'S HYPOTHESIS (typhoon analogue): energy arrives FROM BELOW (hot core/mantle); it
drives a rotating cell that VENTS UPWARD at the centre and SPREADS laterally at the top; the
present continental structure is downstream of that primary vent; an equatorial centre may have
a centrifugal reason.

CORRECTION LOG (v1 -> v2, mark-never-erase): v1 of this screen split 'inflow/suction' and
'upward venting' as if they were COMPETING directions and concluded co-rotation forces INFLOW,
NOT ejection. THAT WAS WRONG. They are ONE mass-conserving circulation: a bottom-heated buoyant
column RISES at the centre, which PULLS fluid IN at the base (= the suction), and rotation
ORGANISES that convergent feed into a coherent vortex (Ekman pumping has an UP-leg through the
interior). Base-inflow and centre-uprise are the SAME loop. The decisive constraint: energy
supplied FROM BELOW cannot drive a NET-DOWNWARD vent (that would carry energy back to its source
against the gradient) -- 'it would sink into the core' is a reductio, not an option.

INHERITS (fluid-dynamics DOI .17972568): C3(three-body) frustration FORCES co-rotation; vortices
MERGE into one coherent rotation; coherent rotation drives an Ekman through-flow (pumping). Plus
the marginal substrate is hot/near-unjamming (M11) and rotation is its UNJAMMING switch (Sec.3).
"""
import hashlib, math

SEED = 19

# ===== LOCK BLOCK (present-tense) =====
OMEGA_EARTH = 7.292e-5     # rad/s
R_EARTH     = 6.371e6      # m
G_GRAV      = 9.81         # m/s^2
# ======================================

a_cf_eq   = OMEGA_EARTH**2 * R_EARTH
ratio_cfg = a_cf_eq / G_GRAV

L = []
L.append("MID-PACIFIC UPWELLING-CELL HYPOTHESIS (CORRECTED v2) -- bottom-heated rotating vent")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; inherits co-rotation+unjamming (DOI .17972568)")
L.append("="*64)
L.append("")
L.append("CORRECTION (v1->v2): v1 wrongly split 'suction' vs 'upward venting' as rival directions")
L.append("and said co-rotation forces INFLOW not ejection. WRONG -- they are ONE circulation.")
L.append("")
L.append("[1] the energy source fixes the sign (the author's decisive point):")
L.append("    heat is supplied FROM BELOW (hot core/mantle, near-unjamming -- M11).")
L.append("    a flow DRIVEN from below CANNOT vent net-DOWNWARD: that would transport energy back")
L.append("    toward its source, against the gradient. => 'would it sink into the core?' NO.")
L.append("    the forced sense of a bottom-heated cell is RISE at centre + SPREAD at top.  [F]")
L.append("")
L.append("[2] it is ONE mass-conserving loop, not two rival flows:")
L.append("    buoyant column RISES at centre  --(mass conservation)-->  pulls fluid IN at the base")
L.append("    (= the 'suction')  --(rotation organises)-->  coherent vortex (Ekman pumping, UP-leg")
L.append("    through the interior)  -->  outflow/SPREAD aloft. base-inflow and centre-uprise are")
L.append("    the SAME circulation. v1's error was reporting only the bottom (inflow) leg.  [F]")
L.append("")
L.append("[3] what the rotation does vs what buoyancy does (kept honest):")
L.append("    * BUOYANCY supplies the LIFT (hot/near-unjammed mantle rising -- M05/M11).  [L->F given heat-from-below]")
L.append("    * ROTATION supplies the ORGANISATION: C3 frustration FORCES co-rotation; vortices")
L.append("      MERGE; coherent rotation FORCES the convergent Ekman feed.  [F] inherited")
L.append("    together: a bottom-heated ROTATING cell that pumps UP at the axis and spreads at top")
L.append("    -- i.e. 'three rotations meet -> a vent' is CORRECT once the driver is heat-from-below.")
L.append("    (rotation does not LIFT the material; it organises the rising cell and its feed.)")
L.append("")
L.append("[4] lateral spread -> present structure (downstream):")
L.append("    a rising column SPREADS at the top (plume-head) and drives lateral transport of the")
L.append("    vented material -- generic + inherited [F/L]. 'THIS vent seeded the PRESENT continents'")
L.append("    and 'the vent stayed FIXED over deep time' embed history -> [O] both ways (M14:")
L.append("    continents reconfigure; a fixed primary vent is not present-tense-established).")
L.append("")
L.append("[5] equator / centrifugal (author flags tentative):")
L.append(f"    equatorial centrifugal accel = Omega^2 R = {a_cf_eq:.4f} m/s^2 = {ratio_cfg*100:.2f}% of g.")
L.append("    real but ~0.34% of gravity: sustains the 21 km bulge and WEAKLY biases long-wavelength")
L.append("    structure toward the spin axis. too small to PIN a vent location alone.")
L.append("    GRADE: [L] weak equatorial bias ; [O] as a vent-locator.")
L.append("")
L.append("ASSEMBLED (corrected, honest):")
L.append("  FORCED [F]: energy-from-below => a bottom-heated cell vents UP at the axis and spreads")
L.append("    at the top (sinking into the core is excluded); rotation FORCES the coherent vortex +")
L.append("    convergent Ekman feed. The typhoon analogue is APT and the upward vent is the FORCED")
L.append("    sense -- v1's inflow-only reading is RETRACTED.")
L.append("  STILL OPEN: buoyancy is the LIFT term [L] (needs the heat-from-below, which M11 supplies);")
L.append("    the vent being FIXED/PRIMARY for PRESENT continents [O]; equator/centrifugal [L]/[O].")
L.append("")
L.append("VERDICT (firewall-clean): with energy supplied from below, the FORCED sense of a three-")
L.append("rotation cell is UP-and-OUT at the vent (it cannot sink to the core) -- the author is right,")
L.append("and the v1 'inflow not ejection' split was an error (now corrected). Rotation organises;")
L.append("buoyancy lifts; together they make the vent. Location/fixity/equator stay [L]/[O].")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "399566a3d87df5e1a0be6fc60492c9f149377844ab6b976101577ddc33f39716"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
