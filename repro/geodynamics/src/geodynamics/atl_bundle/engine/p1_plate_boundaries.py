"""
p1_plate_boundaries.py  --  P1: Atlantic-rim boundary character (subduction vs passive)
================================================================================
Prereg (whitepaper): R_sub = L_subduction / L_perimeter.  UNLOCK if <=0.25; FAIL if >=0.50.
Claim: the Atlantic rim is dominated by passive margins + ridge, not persistent subduction.

DATA PROVENANCE (honest): segment lengths are LITERATURE-DERIVED (cited below), not an
in-sandbox GIS computation over the Bird(2003) PB2002 / Slab2 shapefiles. The verdict is
shown ROBUST to the perimeter definition because Atlantic subduction is so localized.
A full PB2002/Slab2 re-computation is the gold-standard reproduction path (method given).

Cited inputs:
 - Lesser Antilles subduction zone ~850 km (Bouysse & Westercamp 1990; Christeson et al. 2003;
   range 750-900 km across sources).
 - South Sandwich Trench 965 km (Five Deeps multibeam, 2019; Stewart & Jamieson).
 - These are "the only two active island arcs of the Atlantic" (Westbrook 1991).
 - (contested) Gibraltar arc nascent subduction ~200 km (Gutscher et al.; debated).
 - Mid-Atlantic Ridge ~16,000 km (anchors the basin's linear extent).
 - Global subduction length ~51,000 km (Bird 2003 PB2002) for context.
Pure numpy. Deterministic.
"""
import numpy as np

# --- active subduction (convergent) segments of the Atlantic rim [km] ---
L_lesser_antilles = 850.0
L_south_sandwich  = 965.0
L_gibraltar       = 200.0   # contested/nascent

L_sub_base = L_lesser_antilles + L_south_sandwich            # 1815
L_sub_max  = 900.0 + 965.0 + L_gibraltar                     # generous upper bound

# --- perimeter (Atlantic rim) = two passive continental margins ---
MAR = 16000.0                       # Mid-Atlantic Ridge length ~ basin extent
L_perim_base = 2*MAR                # both margins >= basin length -> 32,000 km
L_perim_min  = 1*MAR                # unrealistically small lower bound (one basin length)
L_perim_max  = 40000.0             # following coastline more closely

UNLOCK, FAIL = 0.25, 0.50

print("="*78); print("P1: Atlantic-rim boundary character (R_sub; UNLOCK<=0.25, FAIL>=0.50)"); print("="*78)
print(f"\n  Active subduction (the ONLY two arcs): Lesser Antilles {L_lesser_antilles:.0f} + "
      f"South Sandwich {L_south_sandwich:.0f} = {L_sub_base:.0f} km")
print(f"  Atlantic share of GLOBAL subduction (~51,000 km, Bird 2003): "
      f"{100*L_sub_base/51000:.1f}%  (i.e. the Atlantic hosts almost no subduction)")

def Rsub(Lsub,Lper): return Lsub/Lper
def verdict(r): return "UNLOCK" if r<=UNLOCK else ("FAIL" if r>=FAIL else "HOLD")

r_base = Rsub(L_sub_base, L_perim_base)
print(f"\n  baseline:  R_sub = {L_sub_base:.0f}/{L_perim_base:.0f} = {r_base:.3f}  -> {verdict(r_base)}")
print(f"  R_ridge (MAR/perimeter) = {MAR/L_perim_base:.2f} (divergent boundary dominates the interior)")

# sensitivity sweep: worst-case (max subduction, min perimeter) etc.
print("\n  sensitivity (robustness of the verdict):")
cases=[("max sub, MIN perim (worst)", L_sub_max, L_perim_min),
       ("max sub, base perim",        L_sub_max, L_perim_base),
       ("base sub, max perim",        L_sub_base, L_perim_max),
       ("no Gibraltar, base perim",   L_sub_base, L_perim_base)]
rs=[]
for lbl,ls,lp in cases:
    r=Rsub(ls,lp); rs.append(r)
    print(f"    {lbl:30s} R_sub={r:.3f}  -> {verdict(r)}")
rmax=max(rs+[r_base])
print(f"\n  => even the WORST case R_sub={rmax:.3f} < UNLOCK {UNLOCK}. P1: UNLOCK (PASS), robustly.")
print(f"     The Atlantic rim is overwhelmingly passive margin + ridge; persistent subduction is")
print(f"     confined to two short arcs (~{L_sub_base:.0f} km total).")

print("\n  HONEST: literature-derived segment lengths (cited), not in-sandbox GIS. Gold-standard")
print("  reproduction: rasterize Bird(2003) PB2002 boundary types + Slab2 trenches along an")
print("  Atlantic-rim mask and recompute L_subduction/L_perimeter (method fixed; verdict robust).")

np.savez("p1_results.npz", R_sub_base=r_base, R_sub_worst=rmax,
         L_sub_base=L_sub_base, L_perim_base=L_perim_base,
         unlock=UNLOCK, fail=FAIL, atl_share_global=L_sub_base/51000)
print("\nsaved -> p1_results.npz")
