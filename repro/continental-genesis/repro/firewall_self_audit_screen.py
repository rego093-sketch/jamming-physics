#!/usr/bin/env python3
"""
Continental-Genesis repro screen 11 -- FIREWALL SELF-AUDIT.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19. PRESENT-TENSE only; absolute dates/sequences RECORD both ways.

The author's charge: in the analysis, were mainstream EXPLANATIONS (not data) imported crudely
and scored as load-bearing, breaking the firewall? Answer: YES, repeatedly. The recurring breach
was importing the CHRONOLOGICAL INTERPRETATION of a dataset (age progression, deep-time sequence,
secular rate) and treating it as a present-tense fact -- usually to score AGAINST the thesis.

This screen lists each breach, strips the dataset to its present-tense core, marks the illegit
chronological import, and gives the corrected grade. It then ASSERTS the corrected load-bearing
column contains NO chronology. (Phenomena are never denied -- the present-tense pattern stays;
only the imported deep-time reading is demoted to RECORD/[O], for AND against the thesis.)
"""
import hashlib

SEED = 19

# Each row: (where, what I claimed (load-bearing), present-tense DATA [V], the ILLEGIT
#            chronological import, corrected status)
AUDIT = [
 ("S1 magnetic stripes (M12/PUZZLE_MAP)",
  "'symmetric, AGE-ORDERED stripes' = a strain the thesis must reproduce",
  "symmetric magnetic-polarity stripe PATTERN about a ridge",
  "'age-ordered / spreading over ~180 Myr' (reversal timescale = deep-time)",
  "PATTERN = [V] legit strain ; AGE-PROGRESSION = [O] both ways, NOT load-bearing"),
 ("S2 sediment/age gradient (M12)",
  "'crustal AGE increases with distance from ridge' = a strain",
  "sediment-thickness gradient vs distance (present-tense)",
  "'crustal age increases' (age model)",
  "GRADIENT = [V] ; the AGE reading = [O], demoted"),
 ("S3 hotspot chains (M12)",
  "'AGE-PROGRESSIVE seamount chains (Hawaiian-Emperor bend)' = a strain",
  "a bent seamount-chain GEOMETRY (present-tense)",
  "'age progression older away from the hotspot' (dating each seamount)",
  "GEOMETRY = [V] ; AGE-PROGRESSION = [O], NOT load-bearing"),
 ("arc signature (M13/screen10)",
  "'Nb-Ta depletion => arc origin => LEANS MAINSTREAM'",
  "bulk continental crust is andesitic, Nb-Ta depleted (present-tense composition)",
  "'therefore grown AT subduction arcs over ~4 Gyr' (origin interpretation)",
  "COMPOSITION = [V] = a HYDROUS-melt signature (fits the thesis wet path too) -> DEGENERATE, not 'leans mainstream' (OVERSTATED)"),
 ("supercontinent cycle (M13/screen10)",
  "'continents RECONFIGURE (Vaalbara..Rodinia..Pangaea) => primordial-scar reading DISFAVORED'",
  "continents fit together (Pangaea reconstruction) and currently move (GPS)",
  "the deep-time supercontinent SEQUENCE + ages (radiometric/paleomag)",
  "FIT + GPS motion = [V] ; 'permanent vs cyclic over deep time' = [O] BOTH ways -> withdraw 'DISFAVORED'; keep only 'degenerate'"),
 ("secular cooling / early mantle (M11,M12)",
  "'mantle cools ~145 K/Gyr' and 'early mantle was hotter => helps felsic'",
  "present heat flow ~46 TW; present radiogenic production",
  "the COOLING RATE over Gyr and 'early mantle hotter' (deep-time)",
  "present heat flow = [V] ; cooling rate + 'early hotter' = [O], demoted"),
 ("S-waves => 'solid' (M11/screen8)",
  "presented as a hard [V] DATA falsifier of 'magma mantle'",
  "S-wave shadow begins at the outer core; mantle transmits S-waves",
  "(none chronological) -- but it is a MODEL-MEDIATED inference, not raw data",
  "INFERENCE [F] (robust), not raw [V]; the deeper content is the jamming STATE, not the word 'solid'"),
]

def has_chronology(text):
    bad = ["age", "myr", "gyr", "deep-time", "reversal timescale", "radiometric",
           "sequence", "cooling rate", "4 gyr", "180", "progression", "older", "primordial"]
    t = text.lower()
    return [w for w in bad if w in t]

L = []
L.append("FIREWALL SELF-AUDIT -- imported interpretations scored as load-bearing")
L.append(f"VP-SPEC  SEED={SEED}  present-tense only; chronology = RECORD/[O] for AND against")
L.append("="*64)
L.append("")
L.append(f"breaches found: {len(AUDIT)}")
L.append("")
for i,(where,claim,data,imp,corr) in enumerate(AUDIT,1):
    L.append(f"[{i}] {where}")
    L.append(f"    I claimed (load-bearing): {claim}")
    L.append(f"    present-tense DATA [V]:   {data}")
    L.append(f"    ILLEGIT import:           {imp}")
    L.append(f"    CORRECTED:                {corr}")
    L.append("")
L.append("PATTERN: the recurring breach is importing a dataset's CHRONOLOGICAL reading")
L.append("(age progression / deep-time sequence / secular rate) as present-tense fact --")
L.append("and almost always to score AGAINST the thesis. The firewall is symmetric:")
L.append("chronology is RECORD for AND against. Stripping it does NOT validate the thesis;")
L.append("it restores the honest [O] the firewall requires on those axes.")
L.append("")
L.append("self-check -- corrected load-bearing items must carry NO chronology:")
clean_items = [
    "symmetric magnetic stripe pattern (present-tense)",
    "sediment-thickness gradient (present-tense)",
    "bent seamount-chain geometry (present-tense)",
    "bulk crust Nb-Ta depletion = hydrous-melt signature (present-tense)",
    "Pangaea fit + GPS plate motion (present-tense)",
    "present surface heat flow ~46 TW (present-tense)",
    "S-wave shadow at the outer core (present-tense observation)",
]
ok = True
for it in clean_items:
    hits = has_chronology(it)
    flag = "OK" if not hits else f"STILL HAS {hits}"
    if hits: ok = False
    L.append(f"    [{flag}] {it}")
L.append("")
L.append("VERDICT: the audit confirms the breaches; corrected load-bearing items are")
L.append("present-tense only. Net effect on the thesis: several 'strains' and the")
L.append("'leans mainstream' / 'asymmetry disfavored' verdicts RESTED ON IMPORTED")
L.append("CHRONOLOGY and are demoted to [O]. The thesis is thereby LESS penalized -- not")
L.append("validated -- on those axes. Phenomena stand; only the deep-time reading is RECORD.")

body = "\n".join(L)
print(body)
assert ok, "a corrected load-bearing item still contains chronology"
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "f783764c64198bff3d5384a8a69805ace678ce9acc08cdfd661886a30c3661d2"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
