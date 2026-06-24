#!/usr/bin/env python3
"""
M36 - PETROLEUM LOCATION, WEIGHTED-NULL CORRECTION  (SH-58)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

Review finding (REVIEW sec 3): the M31 location screen computed enrichment = 66%/33% = 2.0x
against a FLAT null (2 of 6 equiprobable tectonic classes). Tectonic settings are NOT
equiprobable by sediment volume; passive margins + rifts hold the bulk of the world's thick
sediment, so even a RANDOM sedimentary basin over-represents them. We recompute enrichment
against a SEDIMENT-VOLUME-WEIGHTED null.

This is built BECAUSE the flat-null x2 is the program's most attackable number; if it
collapses, we retract it (mark-never-erase). A refutation is a finding.

LOCK (curated published shares; sources in-line):
  observed rifting-associated giants (Mann 2003: passive margin 35 + rift/sag 31) = 66%.
  global sediment-VOLUME share by setting (curated band; passive margins dominate global
  sediment volume - e.g. thick prisms of Atlantic-type margins): we carry a defensible
  RANGE for the weighted null rather than a false point value.
    passive+rift volume share = 50% (low) .. 65% (high)   [curated band]
SEED = 19. Double-SHA-256 self-gate.
"""
import os, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
OBS_RIFT = 66.0                 # Mann 2003 passive-margin + rift/sag share of 877 giants
NULL_FLAT = round(100.0 * 2 / 6)   # the old, indefensible flat null
NULL_VOL_LO, NULL_VOL_HI = 50.0, 65.0   # sediment-volume-weighted null (curated band)

enr_flat = OBS_RIFT / NULL_FLAT
enr_vol_hi = OBS_RIFT / NULL_VOL_LO      # most generous enrichment (low null)
enr_vol_lo = OBS_RIFT / NULL_VOL_HI      # least generous enrichment (high null)

L = []
L.append("M36  PETROLEUM LOCATION - WEIGHTED-NULL CORRECTION  (SH-58)")
L.append(f"SEED={SEED}   observed rifting-associated giants = {OBS_RIFT:.0f}% (Mann 2003)")
L.append("")
L.append("[OLD, FLAT NULL - what M31 used]:")
L.append(f"  null (2 of 6 equiprobable classes) = {NULL_FLAT}%  ->  enrichment = {enr_flat:.1f}x")
L.append("  PROBLEM: assumes the 6 tectonic settings are equiprobable BY VOLUME. They are not.")
L.append("")
L.append("[CORRECTED, SEDIMENT-VOLUME-WEIGHTED NULL]:")
L.append(f"  passive+rift sediment-volume share (curated band) = {NULL_VOL_LO:.0f}-{NULL_VOL_HI:.0f}%")
L.append(f"  -> enrichment = {enr_vol_lo:.2f}x .. {enr_vol_hi:.2f}x   (vs the old {enr_flat:.1f}x)")
L.append("")
L.append("[VERDICT]  (honest, mark-never-erase):")
L.append("  X  The 'x2 a random null' claim is RETRACTED. Against a volume-weighted null the")
L.append(f"     enrichment is ~{enr_vol_lo:.1f}-{enr_vol_hi:.1f}x - i.e. petroleum sits at rifting")
L.append("     settings largely BECAUSE that is where the world's thick sediment is. The flat")
L.append("     null inflated the signal.")
L.append("  ok What SURVIVES: petroleum is still NON-uniform and co-locates with rifting [V],")
L.append("     but only MODESTLY above the volume baseline. The cascade's edge therefore was")
L.append("     never the co-location magnitude; it is ECONOMY (one event makes rift+salt+")
L.append("     source+warm-anoxic ocean together) - which is [L] parsimony, not a knockout,")
L.append("     and (M28) is itself contested by the coupled-OAE counter-mechanism. So this")
L.append("     correction WEAKENS a card that was already only suggestive. Logged as a finding.")
L.append("  Occurrence and absolute ages stay [O]/RECORD, both directions.")
L.append("")
L.append("GRADE: SH-58 - flat-null x2 RETRACTED; volume-weighted enrichment ~1.0-1.3x [V];")
L.append("       qualitative co-location stands [V]; the 'strong enrichment' reading falls.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "0f452fdc36e8bb9892d348ed89391b32ad621e9fcce94d8dcb4cef06c297f4ec"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
