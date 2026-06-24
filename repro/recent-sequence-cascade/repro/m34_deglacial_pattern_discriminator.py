#!/usr/bin/env python3
"""
M34 - DEGLACIATION-PATTERN: WHAT PRESENT-TENSE GEOMETRY CAN AND CANNOT DECIDE  (SH-55)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

*** CORRECTED after self-audit (firewall violation found and removed). ***
The PRIOR version of this module used "the Antarctic Cold Reversal LEADS the Younger Dryas"
(a hemispheric ANTIPHASE) and labelled nested ridges as "readvances" - both are CHRONOLOGY
(who happened before whom), which the Constitution caps at [O]/RECORD, firewalled BOTH
directions. Using firewalled timing as load-bearing AGAINST VP was a Constitution breach.
That refutation is RETRACTED. This corrected module load-bears ONLY on present-tense
landform geometry.

PRESENT-TENSE DATUM (load-bearing [V]): in many regions, BOTH hemispheres, the deglaciated
terrain carries MULTIPLE NESTED MORAINE RIDGES - i.e. the former ice margin occupied
several distinct positions, now preserved as landforms.

WHAT THAT GEOMETRY DOES *NOT* DECIDE (without dating = [O], held out):
  - whether any ridge is a RE-ADVANCE (ice grew back out) vs a STILLSTAND/pause during an
    overall retreat. Both leave nested ridges. Distinguishing them needs a chronology.
  - any hemispheric PHASE relation (lead/lag). That is absolute/relative timing -> RECORD.

So nested-ridge geometry is CONSISTENT with a stepped-but-monotonic retreat AND with a
readvancing retreat. It does NOT discriminate the one-declining-fuel reading from the
orbital reading. NON-DISCRIMINATING. (Note: the strict-monotonic "clean sweep" was itself
MY framing in M33's annual branch; the present-tense record neither confirms nor refutes
it - it is simply silent, because the discriminator is the firewalled timing.)

LOCK: reads frozen data/deglacial_pattern_sites.csv (raw SHA-256 pinned in-gate;
present-tense landform facts only). SEED = 19. Double-SHA-256 self-gate.
"""
import os, csv, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
SRC = "data/deglacial_pattern_sites.csv"
raw = open(SRC, "rb").read()
raw_sha = hashlib.sha256(raw).hexdigest()
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

n = len(rows)
n_multi = sum(1 for r in rows if r["multiple_moraine_ridges"] == "yes")
nh = sum(1 for r in rows if r["hemisphere"] == "N")
sh = sum(1 for r in rows if r["hemisphere"] == "S")

L = []
L.append("M34  DEGLACIATION-PATTERN - PRESENT-TENSE GEOMETRY ONLY  (SH-55, CORRECTED)")
L.append(f"SEED={SEED}   source={SRC}")
L.append(f"RAW_FILE_SHA256 = {raw_sha}")
L.append(f"n_regions={n}  (N={nh}, S={sh})   with multiple nested moraine ridges = {n_multi}/{n}")
L.append("")
L.append("[PRESENT-TENSE LANDFORM FACT - load-bearing [V]]:")
for r in rows:
    L.append(f"  {r['hemisphere']}  {r['region']:28s} {r['present_landform']}")
L.append("  => the former ice margin occupied MULTIPLE distinct positions (nested ridges),")
L.append("     in both hemispheres. This is present-tense geometry.")
L.append("")
L.append("[FIREWALL CHECK - what this geometry CANNOT decide]:")
L.append("  - re-advance vs stillstand/pause: BOTH produce nested ridges; separating them")
L.append("    needs a chronology -> [O]/RECORD, held out (both directions).")
L.append("  - hemispheric lead/lag (phase): absolute/relative timing -> RECORD, held out.")
L.append("  The PRIOR module used a hemispheric ANTIPHASE ('cold reversal leads the YD') as")
L.append("  load-bearing against VP. That is firewalled chronology. RETRACTED as a breach.")
L.append("")
L.append("[VERDICT]  (corrected, symmetric):")
L.append("  Nested-ridge geometry is CONSISTENT with a stepped-monotonic retreat AND with a")
L.append("  readvancing retreat. It does NOT discriminate the one-declining-fuel reading from")
L.append("  the orbital reading. NON-DISCRIMINATING on present-tense grounds.")
L.append("  => The earlier 'clean sweep REFUTED' verdict is WITHDRAWN: it depended on")
L.append("     firewalled timing, not on data. On present-tense evidence the glaciation strand")
L.append("     is DEGENERATE (M20), neither confirmed nor refuted here.")
L.append("  => Occurrence and all absolute ages/phases remain [O]/RECORD, both directions.")
L.append("")
L.append("GRADE: present-tense nested-moraine geometry [V] (shared by both frameworks);")
L.append("       SH-55 NON-DISCRIMINATING; prior refutation RETRACTED (firewall breach).")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "c6930cc3e47bbf26fc9b3014c25d224a4a7b98bfd77ddcbf2be9264f9a6d3087"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
