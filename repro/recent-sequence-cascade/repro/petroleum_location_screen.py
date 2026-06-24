#!/usr/bin/env python3
"""
Module 31 reproducibility script - Petroleum LOCATION screen (real curated data).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

Uses PUBLISHED curated counts, not invented numbers:
  - tectonic-setting breakdown of the world's 877 giant oil/gas fields
    (Mann, Gahagan & Gordon 2003, AAPG Memoir 78).
  - source-rock concentration: six intervals (~34% of Phanerozoic record) hold >90%
    of conventional oil & gas (Sorkhabi / GeoExpro 2009; Klemme & Ulmishek 1991).
Tectonic setting is a PRESENT-TENSE observable (where petroleum is now). Absolute
interval AGES are RECORD (held out); only the present-tense CONCENTRATION pattern is
load-bearing. Occurrence stays [O], both directions.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (published curated values; sources in the docstring) =====
# Mann et al. 2003 - share of the 877 giant fields by dominant tectonic setting (%):
PASSIVE_MARGIN     = 35   # rifted margins fronting ocean basins (a RIFTING product)
RIFT_AND_SAG       = 31   # continental rifts + overlying sag, esp. failed rifts
COLLISION_FORELAND = 20   # terminal collision belts + foreland basins
OTHER              = 14   # strike-slip, subduction, arc-collision foreland, etc.
N_SETTING_CLASSES  = 6    # the classification's setting classes (for a random null)
# Source-rock concentration (Sorkhabi/GeoExpro; Klemme & Ulmishek):
N_RICH_INTERVALS   = 6
FRAC_OIL_FROM_THEM = 0.90 # ">90%" of conventional oil & gas
FRAC_OF_RECORD     = 0.34 # ~34% of Phanerozoic *time* - RECORD (absolute), held out
# ==========================================================================

rift_assoc = PASSIVE_MARGIN + RIFT_AND_SAG          # both are products of continental rifting
random_two_classes = round(100.0 * 2 / N_SETTING_CLASSES)  # random expectation for any 2 of 6 classes
enrichment = rift_assoc / random_two_classes

L = []
L.append("PETROLEUM LOCATION SCREEN  (curated data; present-tense; no invented numbers)")
L.append(f"SEED={SEED}   source: Mann/Gahagan/Gordon 2003 (877 giants); Sorkhabi 2009")
L.append("")
L.append("[A] WHERE giant petroleum sits, by tectonic setting (Mann et al. 2003):")
L.append(f"      passive margin (rifted) ... {PASSIVE_MARGIN:3d} %")
L.append(f"      rift + sag ............... {RIFT_AND_SAG:3d} %")
L.append(f"      collision + foreland ..... {COLLISION_FORELAND:3d} %")
L.append(f"      other .................... {OTHER:3d} %")
L.append(f"   => RIFTING-associated (passive margin + rift) = {rift_assoc} %  (a clear majority)")
L.append("")
L.append("[B] is that concentration real, or what randomness would give?")
L.append(f"      random expectation for any 2 of {N_SETTING_CLASSES} setting classes ~ {random_two_classes} %")
L.append(f"      observed rifting-associated = {rift_assoc} %  ->  enrichment x{enrichment:.1f}")
L.append("      => petroleum is NON-randomly concentrated toward rifting settings [V].")
L.append("")
L.append("[C] source-rock concentration (Sorkhabi 2009):")
L.append(f"      {N_RICH_INTERVALS} intervals hold > {int(FRAC_OIL_FROM_THEM*100)} % of conventional oil & gas")
L.append(f"      (those intervals = ~{int(FRAC_OF_RECORD*100)} % of Phanerozoic TIME - RECORD, held out)")
L.append("      => petroleum is NOT uniform in the record; it clusters in a few intervals [V].")
L.append("")
L.append("READING (firewall-clean, symmetric, honest):")
L.append("  [V] Petroleum strongly co-locates with RIFTING (~2/3 of giants) and clusters in a")
L.append("      few source intervals + salt-bearing rifted margins (Campos, Santos, North Sea,")
L.append("      Gulf of Mexico, South Atlantic). The cascade PREDICTS exactly this suite.")
L.append("  BUT non-discriminating alone: the mainstream also expects petroleum at rifted")
L.append("      margins (rifting makes basins, restriction, salt, traps). So co-location is [V];")
L.append("      the cascade's EDGE is ECONOMY - one event makes rift+salt+source+warm-anoxic")
L.append("      ocean together vs sustained independent assembly [L], not a knockout.")
L.append("  HONEST CHALLENGE (data vs the single-event reading): the source rocks cluster in")
L.append("      SIX intervals that are RELATIVELY ORDERED by superposition (a present-tense")
L.append("      fact, not just dates). Six ordered levels do NOT equal one event. Per 'data")
L.append("      conflicts -> revise the hypothesis': narrow the source strand to ONE ENGINE")
L.append("      whose signature RECURS, or hold the single-event reading [O]. Do not force it.")
L.append("  Occurrence and absolute ages stay [O]/RECORD, both directions.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode()).hexdigest()
h2 = hashlib.sha256(h1.encode()).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "715093d27b517c7c21fcc0afce2f69ef96ec6e97f7ad47c6cc6e6b5a75775cf7"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
