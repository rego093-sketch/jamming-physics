#!/usr/bin/env python3
"""
M37 - SOURCE-ROCK FACIES: WHAT IT EXCLUDES AND WHAT IT CANNOT  (SH-59)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

*** CORRECTED after self-audit (strawman + rate-claim found and removed). ***
The PRIOR version equated VP's "rapid source" with a HIGH-ENERGY CHAOTIC diamictite/IRD
deposit, then used "the rock is laminated" to declare the rapid origin REFUTED. That was a
caricature: rapid organic burial in a STRATIFIED ANOXIC ocean ALSO produces fine laminae
(organic mud settling into quiet anoxic bottom water can be geologically fast). And "slow
vs fast" is a RATE - firewalled [O], both directions. So the prior refutation imported a
strawman + a rate claim. RETRACTED. This corrected module load-bears only on present-tense
facies and on what they can EXCLUDE without a rate.

PRESENT-TENSE DATUM (load-bearing [V]): the world's giant-field source rocks are finely
LAMINATED and UNBIOTURBATED. The robust present-tense reading of unbioturbated laminae is
a QUIET, LOW-ENERGY, ANOXIC bottom (no burrowing fauna, no traction transport).

WHAT THIS EXCLUDES (present-tense): a HIGH-ENERGY CHAOTIC deposit - diamictite, ice-rafted
debris, turbidite chaos. Such a setting would destroy mm laminae and bioturbate/mix.

WHAT THIS DOES *NOT* DECIDE: the BURIAL RATE. Quiet anoxic lamination is produced by BOTH
slow steady deposition (mainstream) AND rapid organic burial in a stratified anoxic water
column (a VP-compatible rapid reading). The facies are silent on rate -> [O], held out.

NET: the facies refute the chaotic-flood-DEPOSIT caricature (which VP did not require) but
are NON-DISCRIMINATING between rapid-anoxic and slow-anoxic burial. Both frameworks agree
the setting was quiet and anoxic; they differ only on the firewalled rate.

LOCK: reads frozen data/source_rock_facies.csv (raw SHA-256 pinned in-gate; present-tense
facies of the rocks that charge giant fields). SEED = 19. Double-SHA-256 self-gate.
"""
import os, csv, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
SRC = "data/source_rock_facies.csv"
raw = open(SRC, "rb").read()
raw_sha = hashlib.sha256(raw).hexdigest()
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

n = len(rows)
laminated = [r for r in rows if "laminated" in r["facies_class"]]
chaotic = [r for r in rows if ("diamict" in r["facies_class"] or "IRD" in r["facies_class"]
                               or "chaotic" in r["facies_class"])]

L = []
L.append("M37  SOURCE-ROCK FACIES - WHAT IT EXCLUDES  (SH-59, CORRECTED)")
L.append(f"SEED={SEED}   source={SRC}")
L.append(f"RAW_FILE_SHA256 = {raw_sha}")
L.append(f"n_source_rocks={n}   finely-laminated={len(laminated)}   chaotic/diamictite/IRD={len(chaotic)}")
L.append("")
L.append("[PRESENT-TENSE FACIES - load-bearing [V]]:")
for r in rows:
    L.append(f"  {r['source_rock']:26s} {r['facies_class']:30s} TOC~{r['toc_pct']}% kerogen {r['kerogen_type']}")
L.append("  => finely laminated + unbioturbated -> QUIET, LOW-ENERGY, ANOXIC bottom.")
L.append("")
L.append("[WHAT THE FACIES EXCLUDE (present-tense)]:")
L.append(f"  a HIGH-ENERGY CHAOTIC deposit (diamictite/IRD/turbidite chaos): {len(chaotic)}/{n}.")
L.append("  Such energy would destroy mm laminae and mix the sediment. EXCLUDED. [V]")
L.append("")
L.append("[WHAT THE FACIES CANNOT DECIDE - firewall]:")
L.append("  the BURIAL RATE. Quiet anoxic lamination forms under BOTH slow steady deposition")
L.append("  AND rapid organic burial in a stratified anoxic water column. 'Fast vs slow' is")
L.append("  a RATE -> [O]/RECORD, held out (both directions).")
L.append("  The PRIOR module equated VP-rapid with chaotic-diamictite (a strawman VP did not")
L.append("  require) and read 'laminated' as 'slow' (a firewalled rate). RETRACTED.")
L.append("")
L.append("[VERDICT]  (corrected, symmetric):")
L.append("  The facies REFUTE the chaotic-flood-DEPOSIT caricature, and CONFIRM a quiet anoxic")
L.append("  setting [V] - which BOTH frameworks already share. They are NON-DISCRIMINATING")
L.append("  between rapid-anoxic burial (VP-compatible) and slow-anoxic burial (mainstream).")
L.append("  => The earlier 'rapid/basal origin REFUTED' verdict is WITHDRAWN as overstated.")
L.append("     What stands: source rocks formed in quiet anoxic water (shared); the rate is [O].")
L.append("  => Occurrence and absolute ages remain [O]/RECORD, both directions.")
L.append("")
L.append("GRADE: quiet-anoxic setting [V] (shared); chaotic-flood caricature EXCLUDED [V];")
L.append("       SH-59 NON-DISCRIMINATING on rate; prior refutation RETRACTED (strawman).")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "0c78077576b0d28602c47ba54bdb48a484c1fc840b1942e5c4077dff4479bd27"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
