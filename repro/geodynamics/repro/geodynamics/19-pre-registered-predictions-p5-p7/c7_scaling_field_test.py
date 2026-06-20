"""
c7_scaling_field_test.py  --  P7 field test: does d_crit ~ sqrt(W) survive natural analogs?
================================================================================
GOAL: narrow the master-scale HOLD using Red Sea / Afar / Baikal / E.Africa / Atlantic.
Prediction (C-4): the suction-friction feasibility edge d_crit ~ sqrt(W)
  (Atlantic W=4000km -> ~12 km; Red Sea ~3.3; Afar ~2.7; Baikal ~1.5 km).

HONEST CAVEAT (decisive): the *observed* detachment/seismogenic depth is the BRITTLE-DUCTILE
transition (BDT), which is set by lithospheric TEMPERATURE / AGE / composition, NOT by basin
width. So observed depth ~ the UPPER (thermal) bound d_BDT, NOT the lower feasibility edge d_crit.
We therefore test two things and report exactly what the data say.

Cited observed seismogenic/BDT depths (km) and widths (km):
 - Afar (hot, plume/magmatic): crust ~15 km at spreading centres (Hammond 2011); shallow seismicity
 - Red Sea (warm-young, magmatic): high T limits seismogenic depth; ~15-20 km on-axis
 - Baikal (COLD, ~100-200 Myr / Archean-bordering): Ts ~35-40 km NE, ~25 km central (Deverchere 2001; Emmerson 2006)
 - East African Rift (variable; deeper where lithosphere is thick/cold): up to ~40 km (Craig 2021)
 - Atlantic rifted margin (cold craton target): detachments root mid-crust/Moho ~20 km
BDT physics: shallower (~10-20 km) in warm young crust, deeper (~20-40 km) in cold old crust;
also depends on strain rate (Wikipedia/Sibson; Zuza & Cao: Ts inversely correlated with heat flow).
Pure numpy/scipy. Deterministic.
"""
import numpy as np
from scipy.stats import spearmanr

# basin: (name, width_km, d_obs_km observed seismogenic/BDT, coldness_rank 1=hot..4=cold)
B=[("Afar",        200.0, 10.0, 1.0),
   ("Red Sea",     300.0, 18.0, 2.0),
   ("E. Africa",    60.0, 30.0, 3.5),
   ("Baikal",       60.0, 37.0, 4.0),
   ("Atlantic",   4000.0, 20.0, 3.0)]
names=[b[0] for b in B]; W=np.array([b[1] for b in B]); d_obs=np.array([b[2] for b in B])
cold=np.array([b[3] for b in B])

# predicted feasibility edge d_crit ~ sqrt(W), normalized to Atlantic (W=4000 -> 12 km)
d_crit = 12.0*np.sqrt(W/4000.0)

print("="*80); print("P7 FIELD TEST: does d_crit ~ sqrt(W) survive Red Sea/Afar/Baikal/E.Africa?"); print("="*80)
print(f"\n{'basin':10s} {'W(km)':>7s} {'d_crit~sqrtW':>12s} {'d_obs(BDT)':>11s} {'coldness':>9s}")
for i,n in enumerate(names):
    print(f"{n:10s} {W[i]:7.0f} {d_crit[i]:12.1f} {d_obs[i]:11.0f} {cold[i]:9.1f}")

print("\n(1) is the observed depth controlled by sqrt(W)?  (the prediction)")
rho_W,p_W = spearmanr(W, d_obs)
print(f"    Spearman(d_obs, W) = {rho_W:+.2f} (p={p_W:.2f})")
print(f"    DECISIVE counterexample: Baikal (W={W[3]:.0f} km, COLD) d_obs={d_obs[3]:.0f} km")
print(f"      is DEEPER than Afar (W={W[0]:.0f} km, HOT) d_obs={d_obs[0]:.0f} km --- i.e. the NARROWER")
print(f"      basin is DEEPER. That is OPPOSITE to d ~ sqrt(W). => sqrt(W) is NOT the control.")

print("\n(2) is the observed depth controlled by lithospheric coldness/age?  (thermal)")
rho_c,p_c = spearmanr(cold, d_obs)
print(f"    Spearman(d_obs, coldness) = {rho_c:+.2f} (p={p_c:.2f})  => thermal/age control dominates.")

print("\n(3) feasibility-window consistency [d_crit, d_BDT]:")
for i,n in enumerate(names):
    open_ = d_crit[i] < d_obs[i]
    print(f"    {n:10s} window [{d_crit[i]:.1f}, {d_obs[i]:.0f}] km  {'OPEN' if open_ else 'CLOSED'}")
print("    => d_crit (lower edge) is below d_BDT everywhere, so the window is formally open;")
print("       but the OBSERVED depth equals the thermal cap d_BDT, NOT the d_crit edge.")

print("\nHONEST VERDICT (master gate stays HOLD):")
print("  - The sqrt(W) feasibility-edge prediction is NOT confirmed by observed detachment depths,")
print("    because those depths are the thermally-controlled BDT (cold->deep, hot->shallow), not d_crit.")
print("    Baikal(narrow,cold,deep) vs Afar(wide,hot,shallow) directly contradicts a sqrt(W) reading.")
print("  - What IS corroborated is the mechanism's SEPARATE siting prediction: deep detachment")
print("    requires COLD THICK OLD lithosphere (Baikal ~37 km, E.Africa thick-litho ~30-40 km),")
print("    while hot rifts (Afar) are shallow. So 'cold craton favored' has empirical support.")
print("  - Net: the natural analogs do NOT isolate d_crit, so they do NOT close the master HOLD.")
print("    Closing it needs scale-matched continuum simulation (d_crit not observable in rifts).")

np.savez("c7_field_results.npz", W=W, d_obs=d_obs, d_crit=d_crit, cold=cold,
         rho_W=rho_W, rho_cold=rho_c, names=np.array(names))
print("\nsaved -> c7_field_results.npz")
