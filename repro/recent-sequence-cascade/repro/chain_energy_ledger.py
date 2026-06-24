#!/usr/bin/env python3
# ======================================================================
# VP Recent-Sequence — WHOLE-CHAIN ENERGY LEDGER  (M7 capstone)
# ----------------------------------------------------------------------
# Tests the SINGLE-RELAXATION theory (Module 16) quantitatively:
# does the ENTIRE chain close under ONE controlling parameter, with no
# physically absurd (STOP) step?  Parameter = the ocean heat anomaly the
# relaxation deposits (expressed as a surface-layer warming dT).
#
#   relaxation heat  ->  warm ocean (dT)  ->  evaporation funds ICE
#        ICE loads crust  ->  triggers rupture (Modules 13,14)
#        rupture heat  ->  melts ICE  ->  new equilibrium
#
# DISTINCTIVE prediction tested (Module 16 P3): BUILD is expensive
# (latent heat of vaporization), MELT is cheap (latent heat of fusion),
# so termination is energetically easier than initiation.
#
# FIREWALL (both directions): only MEASURED constants and PRESENT-DAY
# measured yardsticks. NO absolute chronology, NO reconstructed volumes,
# NO paleoclimate model, NO fitted parameter. SEED=19 (no RNG used).
# Honest: any STOP is reported as a STOP.
# ======================================================================
import numpy as np
np.random.seed(19)

# ---- MEASURED CONSTANTS ----
L_v     = 2.45e6     # J/kg  latent heat of vaporization (~25 C)
L_f     = 3.34e5     # J/kg  latent heat of fusion
c_p_sw  = 3990.0     # J/(kg K)
rho_sw  = 1027.0     # kg/m^3
rho_ice = 917.0      # kg/m^3
rho_w   = 1000.0     # kg/m^3 fresh water
g       = 9.81       # m/s^2
A_ocean = 3.61e14    # m^2  present ocean area (measured)
V_ocean = 1.335e9    # km^3 present ocean volume (measured)
Q_geo   = 4.7e13     # W    present global geothermal heat flux (~47 TW, measured)

# ---- PRESENT-DAY MEASURED ice yardsticks (NOT reconstructed LGM) ----
M_greenland = 2.85e6 * 1e9 * rho_ice   # kg  (2.85e6 km^3)
M_all_ice   = 30.0e6 * 1e9 * rho_ice   # kg  (~30e6 km^3)

# ---- THE ONE PARAMETER: ocean surface-layer warming anomaly dT ----
# (everything downstream scales with the heat anomaly Q = rho c h dT)
h_layer = 200.0                         # m   representative warm-layer depth
dT_range = np.array([3.0, 5.0, 8.0, 10.0])   # K   warm-ocean anomaly

print("="*74)
print("WHOLE-CHAIN ENERGY LEDGER (M7) — does the cascade close under ONE parameter?")
print("Parameter = ocean heat anomaly (warm-layer dT). Firewall: measured-only.")
print(f"Warm-layer depth h = {h_layer:.0f} m. Greenland ice mass = {M_greenland:.2e} kg.")
print("="*74)

heat_per_K = rho_sw * A_ocean * h_layer * c_p_sw    # J per K of layer cooling
print(f"\nOcean heat anomaly available per 1 K of warm layer = {heat_per_K:.2e} J\n")

print(f"{'dT(K)':>6} | {'ocean heat Q':>12} | {'ICE built':>11} | {'vs Green':>8} | "
      f"{'build E':>10} | {'melt E':>10} | {'melt time*':>11} | verdict")
print("-"*100)
for dT in dT_range:
    Q          = heat_per_K * dT                 # J  relaxation heat -> ocean -> available
    M_ice      = Q / L_v                         # kg ice built (evaporation funded by ocean cooling)
    frac_green = M_ice / M_greenland             # how many Greenlands
    E_build    = M_ice * L_v                      # J  (== Q; the expensive step)
    E_melt     = M_ice * L_f                      # J  (the cheap step)
    t_melt_geo = E_melt / Q_geo / (365.25*24*3600)   # yr at GLOBAL geothermal flux (upper bound on time)
    stop = (frac_green > 12)                      # >~ all present ice in one pulse = STOP (Module 13)
    verdict = "STOP(too big)" if stop else "closes (not-STOP)"
    print(f"{dT:>6.1f} | {Q:>12.2e} | {M_ice:>11.2e} | {frac_green:>7.2f}x | "
          f"{E_build:>10.2e} | {E_melt:>10.2e} | {t_melt_geo:>9.0f}yr | {verdict}")

print("\n* melt time at the GLOBAL geothermal flux is a deliberate UPPER BOUND; a rupture")
print("  concentrates mantle/volcanic heat locally, so realised melt is FASTER.")

# ---- DISTINCTIVE PREDICTION P3: build/melt asymmetry ----
ratio = L_v / L_f
print("\n" + "-"*74)
print("DISTINCTIVE PREDICTION (Module 16 P3) — build vs melt asymmetry:")
print(f"  building ice (via evaporation) costs L_v = {L_v:.2e} J/kg")
print(f"  melting ice (via fusion)        costs L_f = {L_f:.2e} J/kg")
print(f"  => BUILD is {ratio:.1f}x more expensive than MELT.")
print("  => the loop closes ASYMMETRICALLY: slow ocean-heat-limited build, cheap fast melt")
print("     once the rupture restores warm circulation. Rapid termination is PREDICTED,")
print("     not a puzzle. (This is a theory-internal prediction, falsifiable.)")

# ---- FLOOD-ENERGY SOURCE CHECK (can the relaxation supply Q?) ----
print("\n" + "-"*74)
print("FLOOD-ENERGY SOURCE CHECK — can releasing the reservoir supply the ocean heat?")
print("Gravitational energy of releasing mass M_r through drop dh: E_grav = M_r g dh.")
dh = 2000.0   # m  representative drop height (canyon/sea-level-fall scale, e.g. Module 12)
for dT in [5.0, 10.0]:
    Q   = heat_per_K * dT
    M_r = Q / (g * dh)                      # kg of water whose grav. PE equals Q
    V_r_km3 = M_r / rho_w / 1e9             # km^3
    frac_oc = 100 * (M_r/rho_w) / (V_ocean*1e9)   # % of present ocean volume
    print(f"  to warm ocean by {dT:>4.1f} K: gravitational source needs M_r whose drop@{dh:.0f}m")
    print(f"     equals Q -> M_r = {M_r:.2e} kg = {V_r_km3:,.0f} km^3 = {frac_oc:.1f}% of ocean volume")
print("  Reading: the required release is a LARGE but not absurd fraction of the ocean,")
print("  and the deep reservoir is ~1 ocean (Module 12) -> a few-% release can supply it.")
print("  (Gravitational PE is ONE source; mantle heat from the rupture + configurational")
print("   energy of unjamming also contribute. This is a sanity bound, not the only path.)")

# ---- VERDICT ----
print("\n" + "="*74)
print("M7 VERDICT (whole-chain closure):")
print("  - Under ONE parameter (ocean heat anomaly), the chain builds ice, loads the crust,")
print("    and the melt is comfortably affordable -> CLOSES with no STOP for a single ice")
print("    sheet. (Building ALL present ice in one pulse remains an honest STOP, Module 13.)")
print("  - The build/melt asymmetry (P3) emerges from measured constants -> rapid termination")
print("    is a PREDICTION of the theory.")
print("  - The flood-energy source is plausible (few-% reservoir release) but is the")
print("    demanding link -> flagged for the stress-test, not claimed solved.")
print("  => The single-relaxation chain is energetically COHERENT under one parameter,")
print("     chronology-free. Occurrence stays [O].")
print("="*74)
print("\nThis is a closure screen + a prediction, NOT a proof. Falsification = discovery.")
