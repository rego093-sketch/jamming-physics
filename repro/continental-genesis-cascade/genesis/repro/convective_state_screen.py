#!/usr/bin/env python3
"""
Continental-Genesis repro screen 9 -- the present-state synthesis.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

The author's present-state picture: below circulates (and, being near unjamming, is MORE mobile
than a far-from-melting solid); the skin is cooled/solid; the felsic 'oil-scum' is gathered on
ONE side; crumpling has largely happened; energy is supplied slowly yet the system is MAINTAINED
(quasi-steady). This screen checks each clause against present-tense physics.

Result: the picture is [F]/[V] COHERENT but largely DEGENERATE with mainstream (it is mantle
convection + a rigid lid + an internal heat engine). The ONE non-degenerate EDGE is the
hemispheric asymmetry of the continents ('oil-scum on one side') -- the PUZZLE_MAP #1 edge.
No absolute age is load-bearing.
"""
import hashlib, math

SEED = 19

# ===== LOCK BLOCK (standard whole-mantle values) =====
RHO   = 3300.0     # kg/m^3
G     = 9.8        # m/s^2
ALPHA = 3.0e-5     # 1/K
DT    = 2500.0     # K     temperature drop across the convecting mantle
D     = 2.89e6     # m     mantle depth
KAPPA = 1.0e-6     # m^2/s thermal diffusivity
ETA   = 1.0e22     # Pa s  (whole-mantle effective viscosity)
RA_CRIT = 1000.0   # -     critical Rayleigh number for onset of convection
# energy budget
Q_SURF = 46.0e12   # W     total surface heat flow (~46 TW)
Q_RAD  = 24.0e12   # W     radiogenic heat production (Urey ratio ~0.5)
M_MANTLE = 4.0e24  # kg
CP    = 1200.0     # J/kg/K
SEC_PER_GYR = 3.15576e16
# present-tense observables (cited, not computed)
PLATE_V_CM_YR = "1-10"     # GPS-measured plate speeds
LAND_HEMI_PCT = 81         # % of Earth's land inside the land hemisphere (pole ~47N 2W)
# =====================================================

def rayleigh():
    return RHO * G * ALPHA * DT * D**3 / (KAPPA * ETA)

Ra = rayleigh()
Q_sec = Q_SURF - Q_RAD                      # secular + core cooling
dTdt_K_per_Gyr = (Q_sec / (M_MANTLE * CP)) * SEC_PER_GYR   # rough mantle cooling rate

L = []
L.append("PRESENT-STATE SYNTHESIS -- convecting interior, frozen lid, slow drive")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; ages RECORD both ways")
L.append("="*64)
L.append("")
L.append("[1] 'below circulates' -- Rayleigh number:")
L.append(f"    Ra = rho g alpha dT D^3 /(kappa eta) = {Ra:.2e}")
L.append(f"    Ra / Ra_crit = {Ra/RA_CRIT:.2e}   (>> 1)")
L.append("    -> the mantle MUST convect. The interior moves.  [F]")
L.append("    (near-unjamming, M11 -> low viscosity -> the mobile layer; more mobile than a")
L.append("     far-from-melting solid, but still slow: plates move ~"+PLATE_V_CM_YR+" cm/yr, GPS-measured.)")
L.append("")
L.append("[2] 'skin is cooled/solid' -- the rigid lid:")
L.append("    the lithosphere is the cold conductive boundary layer of this convection;")
L.append("    solid, S-wave-fast, the frozen top of a convecting solid (M11).  [V]")
L.append("")
L.append("[3] 'energy supplied slowly yet maintained' -- the heat engine:")
L.append(f"    surface heat flow Q_surf = {Q_SURF/1e12:.0f} TW ; radiogenic Q_rad = {Q_RAD/1e12:.0f} TW")
L.append(f"    Urey ratio Q_rad/Q_surf = {Q_RAD/Q_SURF:.2f}  (energy IS supplied, continuously)")
L.append(f"    residual (secular + core) = {Q_sec/1e12:.0f} TW -> mantle cools ~{dTdt_K_per_Gyr:.0f} K/Gyr")
L.append("    -> QUASI-STEADY on Myr (maintained), but slowly COOLING on Gyr.  [F]/[V]")
L.append("    (so 'maintained' is right short-term; honestly it is a slowly-cooling steady state.)")
L.append("")
L.append("[4] 'crumpling has largely happened' -- frozen vs active:")
L.append("    present-tense [V]: most large crustal deformation sits in OLD orogens that are")
L.append("    now relatively quiet; ACTIVE deformation is localized at boundaries. But whether")
L.append("    the crumpling happened FAST/ONCE or SLOW/REPEATED is rate/history -> [O] both ways.")
L.append("")
L.append("[5] 'oil-scum gathered on ONE side' -- THE EDGE:")
L.append(f"    present-tense [V]: continents are hemispherically asymmetric -- the land hemisphere")
L.append(f"    (pole ~47N 2W) holds ~{LAND_HEMI_PCT}% of all land; the antipodal hemisphere is ~89% ocean.")
L.append("    mainstream has NO settled 'why' for this degree-1 asymmetry -> the PUZZLE_MAP #1 EDGE.")
L.append("    this is the ONE clause that is NOT degenerate -- where a single-rupture/condensation")
L.append("    picture could say something distinctive, and where evidence is worth pursuing.")
L.append("")
L.append("VERDICT (firewall-clean):")
L.append("  * clauses [1]-[3] are [F]/[V] COHERENT but DEGENERATE -- they are mantle convection +")
L.append("    a rigid lid + an internal heat engine (textbook). Value = internal coherence, not")
L.append("    new evidence; do NOT file as evidence for the thesis (PUZZLE_MAP discipline).")
L.append("  * clause [4] is [V] in distribution but [O] in rate/history.")
L.append("  * clause [5] (hemispheric asymmetry) is the NON-degenerate EDGE -> pursue here.")
L.append("  * 'maintained' = quasi-steady short-term, slowly cooling on Gyr. rate/when [O].")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "f5b55cbdcf7fa5720c4f188e80f9e6a52d40b64210eff5449b3477841bf335bb"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
