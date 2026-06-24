#!/usr/bin/env python3
# ======================================================================
# VP Recent-Sequence — C1-quant NoGo SCREEN  (H-F -> H-G coupling)
# ----------------------------------------------------------------------
# Question (Constitution Art.5): does the "warm ocean + cold sky = snow
# engine" link (C1) require PHYSICALLY ABSURD parameters (a STOP / NoGo),
# or is rapid continental-scale glaciation physically PERMITTED?
#
# This is a PERMISSION screen, NOT an occurrence claim. Occurrence of any
# past glaciation stays [O] (Art.4). The screen only asks: forbidden or not.
#
# FIREWALL (Art.2-3), applied as the operating rule (BOTH directions):
#   ADMISSIBLE (used)      : lab-measured thermodynamic constants;
#                            OBSERVED present-day maritime snowfall rates;
#                            PRESENT-DAY MEASURED ice-sheet volumes.
#   FORBIDDEN (not used)   : absolute chronology (e.g. "ice ages ~100 kyr");
#                            RECONSTRUCTED LGM ice volumes;
#                            paleoclimate model output.
#   NOT load-bearing       : no fitted parameter; every number is a measured
#                            constant or an EXPLICITLY-RANGED assumption.
#
# Honesty: we report whatever the arithmetic gives, over a RANGE of
# assumptions, including any combination that DOES hit a STOP. We use the
# realized (circulation-limited) water-cycle response, not the C-C ceiling.
# SEED=19 (convention; no RNG exercised).
# ======================================================================
import numpy as np
np.random.seed(19)

# ---- MEASURED CONSTANTS (present-tense, lab; firewall-admissible) ----
L_v      = 2.45e6      # J/kg  latent heat of vaporization at ~25 C ocean surface
L_f      = 3.34e5      # J/kg  latent heat of fusion (atmospheric heat-rejection term)
c_p_sw   = 3990.0      # J/(kg K) specific heat of seawater
rho_sw   = 1027.0      # kg/m^3 seawater density
rho_ice  = 917.0       # kg/m^3 glacier ice density
A_ocean  = 3.61e14     # m^2   present ocean area (measured)

# ---- PRESENT-DAY MEASURED ice volumes (firewall-clean yardsticks; NOT LGM) ----
V_greenland_km3 = 2.85e6     # km^3  Greenland ice sheet (measured)
V_antarctica_km3= 26.5e6     # km^3  Antarctic ice sheet (measured)
V_total_land_km3= 30.0e6     # km^3  ~all present land ice (measured)
H_greenland_m   = 1670.0     # m     Greenland mean ice thickness (measured)

# ---- OBSERVED maritime snowfall, expressed as water-equivalent (m w.e./yr) ----
# Coastal/maritime climates (Pacific NW, coastal Alaska, Patagonia, Norway,
# Japan "snow country") observably deliver ~1-4 m water-equivalent per year.
# Global-mean precipitation is ~1 m/yr. Range chosen to bracket the observed.
acc_rate_we = np.array([1.0, 2.0, 3.0, 4.0])   # m water-equiv / yr (OBSERVED band)

# Realized water-cycle intensification is ~half the Clausius-Clapeyron ceiling
# (~3-4 %/K realized vs ~7 %/K ceiling). We do NOT lean on the ceiling.
CC_ceiling_perK   = 0.07
realized_perK     = 0.035   # conservative (circulation-limited; governance/07)

def km3_to_kg_ice(V_km3):
    return V_km3 * 1e9 * rho_ice          # km^3 -> m^3 -> kg

print("="*72)
print("C1-quant NoGo SCREEN — warm ocean + cold sky -> rapid glaciation?")
print("PERMISSION screen only; occurrence stays [O]. Firewall bidirectional.")
print("="*72)

# ====================================================================
# SUB-SCREEN A — ENERGY SUFFICIENCY
# Is the ocean's heat reservoir large enough to FUND (via latent heat of
# evaporation) the water needed to build an observed-scale ice sheet?
# Latent heat to evaporate the water comes from the ocean COOLING.
# ====================================================================
print("\n--- A. ENERGY SUFFICIENCY (ocean heat reservoir -> evaporable water -> ice) ---")
ocean_heat_per_K_per_m = rho_sw * A_ocean * c_p_sw   # J per (K of cooling)(m of depth)
print(f"Ocean heat content = {ocean_heat_per_K_per_m:.2e} J per (K * m of surface-layer depth)")

for name, V_km3 in [("Greenland", V_greenland_km3),
                    ("all present land ice", V_total_land_km3)]:
    m_ice   = km3_to_kg_ice(V_km3)
    E_needed= m_ice * L_v          # J the ocean must give up (evaporation latent heat)
    # express as ocean cooling: choose depth, get required dT  (and vice versa)
    Km_required = E_needed / ocean_heat_per_K_per_m   # K*m  (degrees * metres)
    print(f"\n  Build {name}: ice mass {m_ice:.2e} kg ; latent heat to evaporate it"
          f" = {E_needed:.2e} J")
    print(f"    => ocean cooling budget required = {Km_required:,.0f} K*m. Equivalent to:")
    for h in [100, 400, 1000]:
        dT = Km_required / h
        verdict = "ABSURD (STOP)" if dT > 30 else "reasonable (not a STOP)"
        print(f"       cool top {h:5d} m by  {dT:5.1f} K   -> {verdict}")

print("\n  Reading A: a continental (Greenland-scale) ice sheet is funded by cooling")
print("  the upper ~1 km of ocean by only a few K -> NOT a STOP. Building ALL present")
print("  land ice in ONE pulse needs ~10x that (absurd) -> repeated/deeper tapping")
print("  required; honest STOP for 'all ice at once', not for a single ice sheet.")

# ====================================================================
# SUB-SCREEN B — ACCUMULATION RATE
# At OBSERVED maritime snowfall rates, how long to build continental ice?
# This is the scenario's distinctive "FAST" claim. Compare to nothing dated.
# ====================================================================
print("\n--- B. ACCUMULATION RATE (observed snowfall -> time to build ice; chronology-free) ---")
print(f"  Target ice thickness (measured Greenland mean): {H_greenland_m:.0f} m")
print(f"  Observed maritime snowfall band (water-equiv): {list(acc_rate_we)} m/yr\n")
print(f"  {'snowfall (m w.e./yr)':>22} | {'ice growth (m/yr)':>17} | {'years to build':>15} | verdict")
for r in acc_rate_we:
    ice_growth = r * rho_sw/rho_ice          # water-equiv -> ice thickness rate
    yrs = H_greenland_m / ice_growth
    verdict = "ABSURD (STOP)" if yrs > 1e5 else "fast, not a STOP"
    print(f"  {r:>22.1f} | {ice_growth:>17.2f} | {yrs:>15,.0f} | {verdict}")

print("\n  Reading B: at OBSERVED maritime rates, continental ice thickness accumulates")
print("  in CENTURIES to ~1.5 millennia -> the 'fast' claim is NOT forbidden. (We did")
print("  NOT compare against any ~100-kyr orbital pacing; that is chronology, firewalled.)")

# ====================================================================
# SUB-SCREEN C — MOISTURE-SUPPLY ENHANCEMENT (sanity, realized not ceiling)
# A warm ocean raises evaporation. Use REALIZED ~3.5%/K, not the 7%/K ceiling.
# ====================================================================
print("\n--- C. MOISTURE ENHANCEMENT (realized ~3.5%/K, NOT the 7%/K ceiling) ---")
for dT_ocean in [3, 5, 8, 10]:
    enh = (1 + realized_perK)**dT_ocean - 1
    enh_ceiling = (1 + CC_ceiling_perK)**dT_ocean - 1
    print(f"  ocean warmer by {dT_ocean:2d} K: realized evap +{100*enh:4.0f}%"
          f"  (ceiling would be +{100*enh_ceiling:4.0f}%)")
print("  Reading C: a modestly warmer ocean raises moisture supply by tens of %,")
print("  reinforcing B's rates -> consistent, not absurd. We use the lower realized value.")

# ====================================================================
# VERDICT + OPEN SUB-GATES (the honest part — not papered over)
# ====================================================================
print("\n"+"="*72)
print("VERDICT (C1-quant screen):")
print("  A (energy)      : PASS / not-STOP for a continental ice sheet.")
print("  B (rate)        : PASS / not-STOP — centuries to millennia at observed rates.")
print("  C (moisture)    : consistent (realized enhancement, not ceiling).")
print("  => C1's RATE-CAPABILITY is PHYSICALLY PERMITTED. Occurrence stays [O].")
print("\nOPEN SUB-GATES (HOLD — genuinely unresolved, reported not hidden):")
print("  (i)  SPATIAL: high maritime snowfall is coastal/banded; continent-WIDE")
print("       uniform accumulation is NOT shown by a 0-D budget. (governance/07 caveat)")
print("  (ii) MELT: accumulation needs cold continents (summers not ablating). A warm")
print("       ocean ALSO warms nearby land -> real tension; requires cold/high-albedo")
print("       atmosphere (S1 dust). Open.")
print("  (iii)CONDITIONAL: the whole screen assumes the WARM OCEAN exists (S0/S1, [O]).")
print("       We screen GIVEN a warm ocean; we do not prove the warm ocean here.")
print("="*72)
print("\nThis is a NoGo screen: 'not forbidden', not 'proven'. Falsification = discovery.")
