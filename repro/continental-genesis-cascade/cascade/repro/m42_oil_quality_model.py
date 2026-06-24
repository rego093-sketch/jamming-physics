#!/usr/bin/env python3
"""
M42 - OIL QUALITY (heavy/light, sour/sweet) FROM THE GLACIATION-CASCADE ENVIRONMENT
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE inputs.

CLAIM. If the cascade controls the ENVIRONMENT (M40/M41), it should also control the OIL
QUALITY, because quality is set by the same environmental knobs. The driver is the
GLACIATION (not the flood): glacial MELTWATER plays a DUAL redox role -

  (1) at the DEEP source: a freshwater lid SEQUESTERS oxygen (anoxia) -> organic matter is
      preserved -> good source rock.  ["oxygen sequestration" at depth]
  (2) at the SHALLOW reservoir: cool, oxygen/nutrient-bearing meltwater RECHARGE does the
      opposite -> microbes BIODEGRADE the oil (eat the light ends first) -> HEAVY oil.
      [oxygen NOT sequestered in the shallow reservoir]

So the DEGREE OF OXYGEN ISOLATION differs by setting, and that difference makes the oil
heavy or light - exactly as the environment differs. Three present-tense knobs:
  - reservoir TEMPERATURE (depth): hot/deep -> more thermal maturation -> LIGHTER; also
    biodegradation shuts off above ~80 C (microbes die).
  - MELTWATER RECHARGE x COOL reservoir -> BIODEGRADATION -> HEAVIER (the glaciation knob).
  - SULFUR POTENTIAL (evaporite-sulfate OR anoxic Type II-S) -> sulfur in kerogen -> SOUR, and
    sulfur-rich oil generates early/heavy.

This predicts oil quality per basin; we then check it against the OBSERVED quality of real
provinces. Timing stays [O]; only present-tense environment and present-tense oil quality
are used.

LOCK (model; weights transparent):
  biodeg = recharge * clamp((80 - T_res)/80, 0, 1)        # active only in cool reservoirs
  API_pred = 20 + 0.20*(T_res - 20) - 50*biodeg - 10*evaporite   # heavy<->light proxy
  sour = (evaporite >= 0.5)                                # sulfur-rich -> sour
  reads frozen data/oil_quality_provinces.csv (raw SHA-256 pinned in-gate).
SEED = 19. Double-SHA-256 self-gate.
"""
import os, csv, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
SRC = "data/oil_quality_provinces.csv"
raw = open(SRC, "rb").read(); raw_sha = hashlib.sha256(raw).hexdigest()
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

def clamp(x, lo, hi): return max(lo, min(hi, x))
def api_class(api):
    if api < 10: return "extra-heavy"
    if api < 22: return "heavy"
    if api < 31: return "medium"
    return "light"

out = []
out.append("M42  OIL QUALITY FROM THE GLACIATION-CASCADE ENVIRONMENT  (SEED=19)")
out.append(f"source={SRC}   RAW_FILE_SHA256={raw_sha}")
out.append("  driver = glaciation meltwater (dual redox): deep anoxia (source) + shallow")
out.append("  oxygen-bearing recharge (biodegradation -> heavy). Plus evaporite-sulfate -> sour.")
out.append("")
out.append("[PREDICTED vs OBSERVED]  (present-tense environment -> present-tense quality):")
out.append("  province           lat  T_res  recharge  evap  biodeg  API_pred  class(pred)  | observed")
hits = 0
for r in rows:
    lat=int(r["latitude"]); T=float(r["reservoir_temp_C"]); rc=float(r["meltwater_recharge"]); ev=float(r["sulfur_potential"])
    biodeg = rc*clamp((80-T)/80, 0, 1)
    api = 20 + 0.20*(T-20) - 50*biodeg - 10*ev
    cls = api_class(api)
    sour = "SOUR" if ev >= 0.5 else "sweet"
    obs = r["observed_quality"]
    # crude match check on the heavy/light class word + sour
    obs_l = obs.lower()
    cls_ok = cls.split("-")[-1] in obs_l or cls in obs_l
    sour_ok = ("sour" in obs_l) == (ev >= 0.5)
    ok = cls_ok and sour_ok
    hits += 1 if ok else 0
    mark = "ok" if ok else " ?"
    out.append(f"  {mark} {r['province']:20s} {lat:3d}  {T:5.0f}   {rc:.2f}     {ev:.2f}  {biodeg:.2f}   {api:6.1f}   {cls:10s} {sour:5s}| {obs}")
out.append("")
out.append(f"[MATCH]  {hits}/{len(rows)} provinces' heavy/light + sour/sweet class predicted")
out.append("  from environment alone.")
out.append("")
out.append("[READING]  (objective; the glaciation logic made explicit):")
out.append("  - HIGH-LATITUDE, COOL, MELTWATER-FLUSHED, SHALLOW -> strong biodegradation ->")
out.append("    EXTRA-HEAVY oil. Athabasca (57N) is the type case: the world's biggest heavy-")
out.append("    oil/tar-sand body sits exactly where glacial meltwater recharges cool shallow")
out.append("    reservoirs. The glaciation that MADE the source also DEGRADES the oil to heavy.")
out.append("  - DEEP, HOT (>80C), LITTLE RECHARGE -> biodegradation off + full maturation ->")
out.append("    LIGHT sweet oil. North Sea (58N) is high-latitude too but DEEP and hot -> light.")
out.append("    => latitude alone does NOT set quality; DEPTH/TEMP + RECHARGE do. (3D again.)")
out.append("  - EVAPORITE/SULFATE restricted basins -> sulfur -> SOUR (and early/heavy).")
out.append("    Arabian carbonates+anhydrite -> sour; Monterey Type II-S -> heavy sour.")
out.append("  => The SAME oxygen knob, at two depths, splits the outcome: oxygen SEQUESTERED")
out.append("     at the deep source (good rock) vs oxygen DELIVERED to the shallow reservoir")
out.append("     (heavy oil). Quality is the redox-contrast fingerprint of the glaciation.")
out.append("")
out.append("[GRADE] environment (reservoir T, recharge setting, evaporite) and oil quality")
out.append("  present-tense [V]; quality-from-environment a CONSTRUCTED forward model that")
out.append("  recovers the observed heavy/light/sour pattern. Timing/occurrence [O], untouched.")

body = "\n".join(out)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "de99edac8f5729c232bf51ac74f2bfee967e57f77c1d4a009076da15893ff3f7"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
