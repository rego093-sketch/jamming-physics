#!/usr/bin/env python3
"""
M41 - 3D BASIN-GEOMETRY SOURCE-ROCK MODEL  (constructive, objective)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE inputs.

WHY THIS MODULE. M40 was FLAT (latitude only) and wrongly peaked at the equatorial OPEN
ocean. That ignored the third dimension: ice piles thick on CONTINENTS (land, mid-high
latitude), and when it melts FAST the meltwater + ground rock (glacial flour) FLUSHES OFF
the continent into the adjacent MARGIN / RESTRICTED basin - which is exactly where source
rocks form. So the master variable is BASIN GEOMETRY (restriction) + meltwater routing,
NOT zonal climate. This module rebuilds the scenario in that 3D frame.

TWO ROUTES TO AN ANOXIC, PRODUCTIVE BASIN (both gated by RESTRICTION):
  (A) HIGH-LATITUDE MELTWATER ROUTE: thick continental ice melts -> freshwater lid +
      glacial-flour nutrients flush into the down-slope basin -> stratified, fertilised.
  (B) LOW-LATITUDE WARM ROUTE: warm (event) ocean + tropical upwelling/runoff productivity
      in a restricted/evaporitic basin -> stratified, fertilised.
OPEN OCEAN gets neither restriction nor a lid -> well-mixed, oxygenated -> BARREN.

PRESENT-TENSE INPUTS (load-bearing [V]): the locations where thick ice sheets sat
(mid-high-lat continents), basin-restriction classes (open / passive margin / restricted-
rift-or-epeiric), tropical productivity geography, glacial flour as a nutrient. The VP
"warm event ocean" (flat-warm SST) is carried per the author's framing (the fuel warmed the
ocean at all latitudes). The favourability field is a CONSTRUCTED forward index from these
inputs (weights in this header, transparent). No occurrence/rate/timing claim -> [O] untouched.

LOCK (weights; changing any defines a NEW version):
  warmth_event = 0.85 (flat warm event ocean)
  restriction: open=0.10  margin=0.55  restricted=1.00
  ice_cont[lat]  (where thick ice sat; peaks ~60 deg)
  trop_prod[lat] (warm upwelling/runoff productivity; peaks at equator)
  strat   = 0.45*meltwater_lid + 0.55*warmth_event ; anoxia = restriction*strat
  nutrient= 0.50*meltwater_lid + 0.40*trop_prod + 0.10
  prod    = nutrient*(0.40 + 0.60*warmth_event)
  F       = prod * anoxia * restriction    (restriction also = accommodation/depocentre)
SEED = 19. Double-SHA-256 self-gate.
"""
import os, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
WARMTH = 0.85
REST = {"open_ocean":0.10, "passive_margin":0.55, "restricted_basin":1.00}
LATS = [0,15,30,45,60,75,90]
ICE  = {0:0.00,15:0.05,30:0.15,45:0.60,60:1.00,75:0.85,90:0.40}   # continental ice load
TROP = {0:1.00,15:0.90,30:0.55,45:0.40,60:0.30,75:0.15,90:0.10}   # warm productivity

def favour(lat, rtype):
    R = REST[rtype]; ML = ICE[lat]
    strat = 0.45*ML + 0.55*WARMTH
    anoxia = R*strat
    nutrient = 0.50*ML + 0.40*TROP[lat] + 0.10
    prod = nutrient*(0.40 + 0.60*WARMTH)
    return prod*anoxia*R

grid = {t:{L:favour(L,t) for L in LATS} for t in REST}
Fmax = max(v for t in grid for v in grid[t].values()) or 1.0
N = {t:{L:grid[t][L]/Fmax for L in LATS} for t in REST}

out = []
out.append("M41  3D BASIN-GEOMETRY SOURCE-ROCK MODEL  (constructive; SEED=19)")
out.append("  warm event ocean (flat SST) + ice-on-continents + basin restriction")
out.append("")
out.append("[SOURCE-ROCK FAVOURABILITY  F(latitude x basin type), normalised 0-1]:")
out.append("  lat | open ocean | passive margin | restricted/rift basin")
for L in LATS:
    o=N["open_ocean"][L]; m=N["passive_margin"][L]; r=N["restricted_basin"][L]
    bar = "#"*int(round(r*24))
    out.append(f"  {L:3d} |   {o:.2f}     |     {m:.2f}       |   {r:.2f}  {bar}")
out.append("")
# peaks
restr = N["restricted_basin"]
peak = max(LATS, key=lambda x: restr[x])
order = sorted(LATS, key=lambda x: -restr[x])
out.append("[READING]  (objective; inputs present-tense [V]):")
out.append("  MASTER VARIABLE = basin RESTRICTION, not latitude:")
out.append(f"    open ocean is BARREN at every latitude (max {max(N['open_ocean'].values()):.2f}) -")
out.append("      well-mixed, oxygenated; no lid -> no source rock. (No oil in the deep ocean.)")
out.append("    restricted/rift basins are FAVOURABLE; passive margins intermediate.")
out.append("  Within restricted basins the favourability is TWO-ENDED:")
out.append(f"    - a HIGH-LATITUDE peak at {peak} deg (continental ice melts -> meltwater lid +")
out.append("      glacial-flour nutrients flush off the continent): route (A).")
out.append("    - a LOW-LATITUDE shoulder (warm productive restricted seas): route (B).")
out.append("    - a dip near 30 deg (arid, between the two productivity sources).")
out.append(f"  restricted-basin ranking (most->least): {order}")
out.append("")
out.append("[ANSWER TO 'why doesn't it form at high latitude?']:")
out.append("  It DOES. The flat M40 wrongly killed it by ignoring that the thick ice sits on")
out.append("  the CONTINENT and, melting fast, flushes its meltwater+sediment into the down-")
out.append("  slope margin/rift basin. In 3D the high-latitude restricted basins become a")
out.append("  PEAK, not a void. Latitude alone was the wrong axis; basin geometry is the axis.")
out.append("")
out.append("[GRADE] inputs (ice-sheet locations, basin restriction, glacial flour, tropical")
out.append("  productivity) present-tense [V]; warm-event SST per author framing; favourability")
out.append("  a CONSTRUCTED forward index. No rate/timing/occurrence claim -> [O] untouched.")

body = "\n".join(out)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "582e3ac51aa826b73797f90642bc212f4a904282c7604d8fae56568fb6fc4dd0"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
