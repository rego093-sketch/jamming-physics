#!/usr/bin/env python3
"""
M40 - PER-LATITUDE DEGLACIAL -> PETROLEUM-SOURCE SCENARIO  (constructive, objective)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE inputs.

PURPOSE. This is NOT a refutation audit and makes NO VP-vs-mainstream comparison. It BUILDS
OUT, latitude by latitude, the cascade's own scenario: as ice melts at each latitude, with
the rainfall field, where are the conditions for organic-rich SOURCE-ROCK burial (the seed
of petroleum) most favoured? It resolves the detail that an averaged treatment hides.

THREE PRESENT-TENSE DRIVERS (all load-bearing [V], computed/observed; no chronology):
  (1) ANGLE OF INCIDENCE. Annual-mean insolation from the present orbit: the equator
      receives sun near-overhead (high flux per area), the pole obliquely (low). Equator hot.
  (2) WATER-VAPOUR GREENHOUSE. Saturation vapour pressure e_s(SST) (Clausius-Clapeyron,
      Tetens): the warm equatorial ocean holds ~6-7x the column water vapour of the pole.
      That vapour TRAPS outgoing longwave -> amplifies equatorial warmth; the dry pole traps
      little -> cold. (This is WHY the observed SST gradient is as steep as it is.)
  (3) RAINFALL. Present zonal-mean precipitation (ITCZ wet equator; arid descending
      subtropics ~30 deg; wet mid-latitude storm tracks; dry cold poles).

COUPLING TO THE MELT (the cascade scenario). During deglaciation the ice (high-latitude)
delivers MELTWATER; meltwater + rainfall = a FRESHWATER LID -> surface stratification ->
bottom-water ANOXIA (cuts O2 resupply), which PRESERVES organic matter. Rainfall + meltwater
also deliver NUTRIENTS (weathering/runoff) -> high surface PRODUCTIVITY. Warm water (driver 1+2)
holds less O2 -> further favours anoxia. Source-rock burial is therefore maximised where
PRODUCTIVITY x PRESERVATION is greatest, and is ENHANCED during the meltwater pulse.

SCENARIO INDEX (a constructed forward index, transparently weighted; the INPUTS are [V]):
  warmth  W(phi)  = norm(SST)                         [drivers 1+2, observed]
  wet     R(phi)  = norm(precip)                       [driver 3, observed]
  melt    M(phi)  = norm(ice presence ~ cold latitude) [meltwater source during deglaciation]
  productivity  Prod = W * R                           [warm + nutrient-rich runoff]
  stratification S    = norm(R + M)                    [freshwater lid: rain + meltwater]
  low-O2 factor  Lox  = 0.5 + 0.5*W                    [warm water lower O2; floor 0.5]
  preservation  Pres = S * Lox
  SOURCE FAVOURABILITY  F(phi) = Prod * Pres           [reported normalised to its max]

LOCK: SST_ZONAL (observed); reads frozen data/zonal_precip.csv (raw SHA-256 pinned in-gate);
insolation from present orbit. SEED = 19. Double-SHA-256 self-gate.
"""
import os, csv, math, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
S0, OBL, ECC = 1361.0, math.radians(23.44), 0.0167
SST_ZONAL = {0:27.0,15:26.0,30:22.0,45:14.0,60:6.0,75:0.0,90:-1.8}
SRC = "data/zonal_precip.csv"
raw = open(SRC, "rb").read(); raw_sha = hashlib.sha256(raw).hexdigest()
prc = {int(r["lat"]): (float(r["precip_mm_yr"]), r["regime"]) for r in csv.DictReader(open(SRC, encoding="utf-8"))}
LATS = sorted(SST_ZONAL)

def daily(phi, decl):
    phi = math.radians(phi); x = max(-1, min(1, -math.tan(phi)*math.tan(decl)))
    H0 = math.acos(x)
    return (S0/math.pi)*(H0*math.sin(phi)*math.sin(decl)+math.cos(phi)*math.cos(decl)*math.sin(H0))
def annual(phi, n=360):
    return sum((1+ECC*math.cos(2*math.pi*k/n))**2 * daily(phi, math.asin(math.sin(OBL)*math.sin(2*math.pi*k/n))) for k in range(n))/n
def es(T):  # Tetens, hPa
    return 6.112*math.exp(17.62*T/(243.12+T))

ins = {L: annual(L) for L in LATS}
vap = {L: es(SST_ZONAL[L]) for L in LATS}
def norm(d):
    lo, hi = min(d.values()), max(d.values()); 
    return {k: (v-lo)/(hi-lo) for k, v in d.items()}

W = norm(SST_ZONAL)
R = norm({L: prc[L][0] for L in LATS})
M = norm({L: -SST_ZONAL[L] for L in LATS})        # ice/meltwater ~ cold latitudes
Prod = {L: W[L]*R[L] for L in LATS}
S = norm({L: R[L]+M[L] for L in LATS})
Lox = {L: 0.5+0.5*W[L] for L in LATS}
Pres = {L: S[L]*Lox[L] for L in LATS}
Fraw = {L: Prod[L]*Pres[L] for L in LATS}
Fmax = max(Fraw.values()) or 1.0
F = {L: Fraw[L]/Fmax for L in LATS}

L = []
L.append("M40  PER-LATITUDE DEGLACIAL -> PETROLEUM-SOURCE SCENARIO  (constructive; SEED=19)")
L.append(f"source(precip)={SRC}   RAW_FILE_SHA256={raw_sha}")
L.append("")
L.append("[DRIVER 1+2  WARMTH = angle-of-incidence insolation + water-vapour greenhouse]:")
L.append("  lat  annual_insol(W/m2)  SST(C)  e_s(hPa)  vapour x vs pole")
ep = vap[90]
for La in LATS:
    L.append(f"  {La:3d}     {ins[La]:7.1f}        {SST_ZONAL[La]:5.1f}   {vap[La]:6.1f}     {vap[La]/ep:4.2f}x")
L.append("  => equator near-overhead sun + ~6.6x water vapour -> trapped longwave -> hot;")
L.append("     pole oblique sun + dry -> little trapping -> cold. The gradient is physical.")
L.append("")
L.append("[DRIVER 3  RAINFALL (present zonal-mean)]:")
for La in LATS:
    L.append(f"  {La:3d}   {prc[La][0]:5.0f} mm/yr   {prc[La][1]}")
L.append("  => wet equator (ITCZ), arid ~30deg (descending), wet mid-lat (storms), dry poles.")
L.append("")
L.append("[COUPLED PER-LATITUDE SOURCE-ROCK FAVOURABILITY during the melt]:")
L.append("  lat   warmth  wet   melt   Prod   Pres   FAVOURABILITY F (norm)")
for La in LATS:
    bar = "#" * int(round(F[La]*30))
    L.append(f"  {La:3d}    {W[La]:.2f}   {R[La]:.2f}  {M[La]:.2f}   {Prod[La]:.2f}   {Pres[La]:.2f}   {F[La]:.2f}  {bar}")
peak = max(LATS, key=lambda x: F[x])
order = sorted(LATS, key=lambda x: -F[x])
L.append("")
L.append("[SCENARIO READING]  (objective; the inputs are present-tense [V]):")
L.append(f"  Favourability PEAKS at {peak} deg (warm + wet + meltwater/strat anoxia + low O2).")
L.append(f"  Latitudinal ranking (most->least favourable): {order}")
L.append("  Structure: a strong EQUATORIAL/low-latitude peak (warm humid productive +")
L.append("  anoxic), a SECONDARY mid-latitude high (wet storm tracks + meltwater lid), and")
L.append("  MINIMA at the arid subtropics (~30deg deserts: productive-starved) and the cold")
L.append("  dry poles (preservation without productivity). As ice melts, the meltwater lid")
L.append("  spreads equatorward and BROADENS the anoxic window -> the melt phase is when")
L.append("  source burial is maximised, latitude by latitude.")
L.append("")
L.append("[GRADE]  drivers (insolation, water-vapour, rainfall) present-tense [V]; the")
L.append("  favourability field is a CONSTRUCTED forward scenario from those [V] inputs.")
L.append("  No occurrence/rate/timing claim is made (those remain [O], untouched). This is")
L.append("  detail-building of the cascade scenario, not a discriminating test.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "3c899ccbd43f93323eab44b90c34e37876bc0bb572c0073e2c46d7e9a58bd141"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
