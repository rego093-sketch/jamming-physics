#!/usr/bin/env python3
"""
M33 - LATITUDE ENERGY-BALANCE PERMISSION SCREEN  (SH-53, SH-54)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

This is a PHYSICAL-PERMISSION screen (same class as the C1/C2 no-go screens). The only
permitted conclusions are "permitted [F]"/"forbidden" and the STRUCTURAL ordering fork.
Occurrence and all absolute dates/timescales are [O]/RECORD, firewalled BOTH directions.

WHAT IS COMPUTED (present-tense, no chronology):
  - annual-mean and summer-solstice TOA insolation by latitude, from the PRESENT orbit
    (obliquity, eccentricity). No PAST orbital variation is used - that is a D4/D5 object
    the firewall holds out (and is the mainstream's distinctive pacing).
  - a build index (warm-ocean snow engine ~ (SST - T_air) x Clausius-Clapeyron) and a melt
    index = absorbed insolation - OLR of a MELTING ice surface (a melting surface sits at
    ~273 K, so its OLR is ~constant, independent of air temperature). Under TWO controls:
    annual-mean absorbed vs summer absorbed.

WHAT IS WITHHELD ([O]):
  - the fuel MAGNITUDE (reservoir latent heat): enters only symbolically as "SST elevated,
    then declining"; its number inherits SH-5 = [O]. No fuel number is used.
  - any absolute timing of build or termination. The screen reports PERMISSION + ORDERING.

THE FORK (SH-53). Insolation has two different latitude shapes: annual-mean is MONOTONIC
(equator-hot, pole-cold); summer-solstice is NON-MONOTONIC (peaks at the pole, 24h day).
So the termination ORDERING forced as the warm-ocean fuel wanes depends on which energy
balance controls melt - and WHICH controls is itself a present-tense question. That fork,
not a single sweep, is the firewall-clean structural result.

LOCK (present-tense constants; changing any defines a NEW version):
  S0        = 1361.0  W/m^2          (present solar constant)
  OBLIQUITY = 23.44   deg            (present)
  ECC       = 0.0167                 (present eccentricity; small effect, included)
  ALBEDO_ICE= 0.70                   (snow/ice broadband)
  OLR_MELT  = 210.0   W/m^2          (OLR of a melting (~273 K) ice surface)
  K_CC      = 0.07    /degC          (Clausius-Clapeyron saturation slope)
  Zonal-mean present SST and surface-air T (degC) - standard climatology, frozen below.
SEED = 19. Determinism structural (no RNG). Double-SHA-256 self-gate.
"""
import os, math, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
S0        = 1361.0
OBLIQUITY = math.radians(23.44)
ECC       = 0.0167
ALBEDO_ICE= 0.70
OLR_MELT  = 210.0
K_CC      = 0.07
LATS = list(range(0, 91, 15))
SST_ZONAL = {0:27.0, 15:26.0, 30:22.0, 45:14.0, 60:6.0, 75:0.0, 90:-1.8}
TAIR_ANN  = {0:26.0, 15:25.0, 30:20.0, 45:9.0,  60:-1.0,75:-15.0,90:-25.0}

def daily_insol(phi_deg, decl):
    phi = math.radians(phi_deg)
    x = max(-1.0, min(1.0, -math.tan(phi) * math.tan(decl)))
    H0 = math.acos(x)
    return (S0 / math.pi) * (H0 * math.sin(phi) * math.sin(decl)
                             + math.cos(phi) * math.cos(decl) * math.sin(H0))

def annual_mean_insol(phi_deg, n=360):
    tot = 0.0
    for k in range(n):
        lam = 2 * math.pi * k / n
        decl = math.asin(math.sin(OBLIQUITY) * math.sin(lam))
        w = (1 + ECC * math.cos(lam)) ** 2
        tot += w * daily_insol(phi_deg, decl)
    return tot / n

def summer_insol(phi_deg):
    return daily_insol(phi_deg, OBLIQUITY)

def build_index(phi):
    dT = SST_ZONAL[phi] - TAIR_ANN[phi]
    return max(0.0, dT) * (1 + K_CC * max(0.0, dT))

def melt_index(phi, which):
    ins = annual_mean_insol(phi) if which == "annual" else summer_insol(phi)
    return ins * (1 - ALBEDO_ICE) - OLR_MELT   # melting surface OLR ~ const (273 K)

rows = [{
    "lat": phi,
    "ins_ann": annual_mean_insol(phi),
    "ins_sum": summer_insol(phi),
    "build": build_index(phi),
    "melt_ann": melt_index(phi, "annual"),
    "melt_sum": melt_index(phi, "summer"),
} for phi in LATS]

order_ann = [r["lat"] for r in sorted(rows, key=lambda r: -r["melt_ann"])]
order_sum = [r["lat"] for r in sorted(rows, key=lambda r: -r["melt_sum"])]

L = []
L.append("M33  LATITUDE ENERGY-BALANCE PERMISSION SCREEN  (present-tense; no chronology)")
L.append(f"SEED={SEED}   orbit: obliquity=23.44deg ecc=0.0167   albedo_ice={ALBEDO_ICE}")
L.append("")
L.append("[INSOLATION FIELD]  (computed from present orbit only):")
L.append("  lat   annual-mean   summer-solstice   (W/m^2)")
for r in rows:
    L.append(f"  {r['lat']:3d}     {r['ins_ann']:7.1f}        {r['ins_sum']:7.1f}")
L.append("  -> annual-mean is MONOTONIC (equator-hot, pole-cold).")
L.append("  -> summer-solstice is NON-MONOTONIC (peaks at the pole; 24h daylight).")
L.append("     This is the mainstream's control variable (the ~65N-summer Milankovitch knob).")
L.append("")
L.append("[MELT INDEX = absorbed insolation - OLR(melting surface)]  (per band, both controls):")
L.append("  lat   build_idx   melt(annual)   melt(summer)")
for r in rows:
    L.append(f"  {r['lat']:3d}    {r['build']:7.2f}     {r['melt_ann']:8.1f}      {r['melt_sum']:8.1f}")
L.append("  -> CAVEAT (credibility): with a UNIFORM ice albedo 0.70 and NO meridional heat")
L.append("     transport, this toy screen returns melt<0 at every latitude. That all-latitude")
L.append("     lock is a KNOWN energy-balance-model ARTIFACT - real low-latitude ice melts")
L.append("     (dirty/melting-ice albedo falls to ~0.4-0.5, plus poleward heat transport).")
L.append("     So the low-latitude lock is NOT load-bearing and is discarded.")
L.append("  -> The CREDIBLE present-tense fact is at HIGH latitude: Antarctic and Greenland ice")
L.append("     is insolation-locked NOW (it persists through the polar summer despite high")
L.append("     summer insolation). That high-latitude lock is OBSERVED [V] and is resonant")
L.append("     with the VP bistable substrate. [F]: high-latitude termination is fuel-driven")
L.append("     (ocean heat from below / albedo drop), not insolation-driven.")
L.append("")
L.append("[SH-54  BUILD permission under a warm ocean]:")
L.append("  build_idx is positive and RISES toward the pole (cold air -> larger SST-air")
L.append("  contrast -> stronger snow engine): the high-latitude band is most build-favoured")
L.append("  while a warm ocean supplies fuel. [F] permitted; the warm ocean is BOTH fuel and")
L.append("  (via summer insolation) the melt-threat (Module 29). Screened, not forbidden.")
L.append("")
L.append("[SH-53  TERMINATION-ORDERING FORK]  (structural; forced by the insolation field):")
L.append("  As the (symbolic) warm-ocean fuel wanes, the band that flips to MELT-DOMINATED")
L.append("  first is the one with the largest (least-negative) melt index. That ordering")
L.append("  DEPENDS on which control governs melt:")
L.append(f"    annual-mean control -> equatorward-FIRST (monotonic): {order_ann}")
L.append(f"    summer control      -> pole/high-lat-WEIGHTED:        {order_sum}")
L.append("  => The ORDERING is FORCED by present-tense insolation geometry, but the BRANCH")
L.append("     (which control) is itself a present-tense screen, not a free choice. [L]/[F].")
L.append("  => VP-distinctive reading = the annual-mean monotonic equatorward-first sweep")
L.append("     under ONE declining-fuel parameter. Mainstream = summer/65N-paced,")
L.append("     hemispherically phased. They predict DIFFERENT present-tense geometry -> the")
L.append("     discriminating test is SH-55 (next module).")
L.append("")
L.append("READING (firewall-clean, symmetric):")
L.append("  [F] HIGH-LATITUDE ice is insolation-locked NOW (observed; Antarctica/Greenland");
L.append("      persist through polar summer) - a present-tense bistable fact; termination is")
L.append("      fuel-driven there. A high-latitude BUILD band is permitted under a warm ocean.")
L.append("      (The all-latitude lock from the toy screen is an albedo/transport artifact.)")
L.append("  [L] the termination ordering is forced into a FORK by the insolation field; the")
L.append("      fuel MAGNITUDE and all absolute timing stay [O], both directions.")
L.append("  The fork - not a single sweep - is the honest structural result. The naive")
L.append("  'low-latitude melts first' is only the ANNUAL branch; summer insolation (peaking")
L.append("  at the pole) is exactly why the mainstream control differs. Falsification = discovery.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "6afe63f90dd23bf9599b7bd6afc771b1973bcc63cea73986755c50815eeabb5d"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
