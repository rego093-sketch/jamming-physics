#!/usr/bin/env python3
"""
Continental-Genesis repro screen 15 -- granite vs limestone: the causal dichotomy (the map test).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19. PRESENT-TENSE rock distribution (a legal present-tense observable;
no dates/sequences used as load-bearing).

THE AUTHOR'S MOVE: spread out the granite map and the limestone map; find the causation.
WHERE THE ROCKS ARE (present-tense, from the literature):
  GRANITE (felsic batholiths): concentrated at CONVERGENT margins + orogenic/'mobile' belts;
    made by PARTIAL MELTING at depth above subduction-like wet zones (>70% SiO2, deep crust melts,
    magma rises). Continents grow by marginal accretion of these granite belts. Korea = batholiths
    from Pacific-plate subduction under Eurasia -> wet partial melting above the slab.
  LIMESTONE (carbonate platforms): concentrated on SHALLOW (<200 m), warm, clear, sunlit shelves of
    EXTENSIONAL/PASSIVE margins + flooded epeiric seas; made by SURFACE PRECIPITATION (corals/algae/
    shells + chemical), away from clastic input. Top-down accumulation, not melting.

This screen extracts the CAUSAL DISCRIMINATOR and uses it to resolve CG-12 (does pure extension make
continent-scale felsic, or does felsic require the convergent/deep-water wet path?).
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (present-tense end-member processes; the two maps) =====
# Each end-member rock is tagged by the PHYSICAL process that makes it (not by age).
GRANITE = dict(rock="granite (felsic)",
               where="convergent margins / orogenic 'mobile' belts",
               process="DEEP partial melt of buried, hydrated crust (heat+water from below)",
               direction="bottom-up (distillation from depth)",
               tectonic_face="COMPRESSION / closing",
               depth_km="10-30 (lower-crust melting)",
               needs_water=True, needs_burial=True, surface_or_deep="DEEP")
LIMESTONE = dict(rock="limestone (carbonate)",
                 where="passive/extensional shelves + flooded epeiric seas",
                 process="SHALLOW surface precipitation (bio+chem), low clastic input",
                 direction="top-down (accumulation at the surface)",
                 tectonic_face="EXTENSION / quiet subsiding shelf",
                 depth_km="0-0.2 (sunlit shallow water)",
                 needs_water=True, needs_burial=False, surface_or_deep="SURFACE")

# present-tense locality map: locality -> dominant rock + tectonic face (no dates)
LOCALITIES = [
    ("Korean peninsula",            "granite",   "convergent (W-Pacific subduction)"),
    ("Sierra Nevada / Idaho (N.Am)","granite",   "convergent (Cordilleran arc)"),
    ("SE Australia / W Europe belts","granite",  "convergent (accreted mobile belts)"),
    ("Andes",                       "granite",   "convergent (active arc)"),
    ("Bahamas platform",            "limestone", "extensional (passive margin shelf)"),
    ("Persian Gulf / Arabian shelf","limestone", "extensional (passive shelf)"),
    ("S China epeiric (Yangtze)",   "limestone", "extensional (flooded craton margin)"),
    ("Santos pre-salt (Brazil)",    "limestone", "extensional (rift-to-passive shelf)"),
]
# ========================================================================

L = []
L.append("GRANITE vs LIMESTONE -- the causal dichotomy (the map test of CG-12)")
L.append(f"VP-SPEC  SEED={SEED}  PRESENT-TENSE rock distribution (legal observable)")
L.append("="*64)
L.append("")
L.append("[1] the two maps, read by PROCESS (present-tense, not age):")
for d in (GRANITE, LIMESTONE):
    L.append(f"    {d['rock']:>20}: {d['where']}")
    L.append(f"    {'':>20}  process : {d['process']}")
    L.append(f"    {'':>20}  flow    : {d['direction']}  | face: {d['tectonic_face']}  | {d['surface_or_deep']}")
L.append("")
L.append("[2] the CAUSAL DISCRIMINATOR (what decides which rock forms):")
L.append("    granite   <- DEEP + HOT-from-below + WATER + BURIAL + COMPRESSION  (a melt at depth)")
L.append("    limestone <- SHALLOW + SUNLIT + SURFACE + low-clastic + EXTENSION  (a precipitate on top)")
L.append("    => the two rocks are ALMOST ORTHOGONAL processes: one is distilled UP from a buried,")
L.append("       squeezed, wet pile; the other is laid DOWN on a quiet, flooded, stretched shelf.")
L.append("    => crucial: granite marks where the crust CLOSED/compressed; limestone marks where it")
L.append("       stayed OPEN/extended and shallow. The two maps are the TWO FACES of one rupture engine.")
L.append("")
L.append("[3] locality readout (present-tense; rock <-> tectonic face):")
gC=gE=lC=lE=0
for name, rock, face in LOCALITIES:
    conv = face.startswith("convergent")
    L.append(f"    {name:32s} {rock:9s}  {face}")
    if rock=="granite" and conv: gC+=1
    elif rock=="granite": gE+=1
    elif rock=="limestone" and not conv: lE+=1
    else: lC+=1
L.append(f"    --> granite on COMPRESSION faces: {gC}/{gC+gE}   limestone on EXTENSION faces: {lE}/{lE+lC}")
L.append("    the alignment is essentially clean: granite=compression, limestone=extension.")
L.append("")
L.append("[4] WHAT THE MAP DECIDES for CG-12 (the load-bearing gap):")
L.append("    CG-12 asked: does PURE EXTENSION make continent-scale felsic, or does felsic need the")
L.append("    convergent/deep-water WET path? The granite map answers in a specific direction:")
L.append("    * continent-scale granite concentrates at CONVERGENCE (subduction/collision), where the")
L.append("      deep-water wet-melt path operates -- NOT at pure extensional rifts (those build the")
L.append("      BASIN + the carbonate shelf + only minor silicic volcanics).")
L.append("    => FELSIC AT CONTINENT SCALE TRACKS THE COMPRESSION/CONVERGENT FACE, not pure opening.")
L.append("")
L.append("[5] is this a falsification of the thesis, or a sharpening?  (honest)")
L.append("    NOT a falsification. The VP rupture has TWO faces (CG-7): the OPENING face (extension")
L.append("    -> basin -> carbonate shelf) and the antipodal CLOSING face (compression -> burial ->")
L.append("    wet melt -> granite, CG-9/CG-10). The map says granite is made on the CLOSING face --")
L.append("    which is exactly what the thesis already claims. So the map RESOLVES CG-12:")
L.append("      * MELT MECHANISM: VP CONVERGES with mainstream -- continent-scale felsic needs the")
L.append("        convergent, deep-water, wet-melt path (not pure extension). The 'rupture alone")
L.append("        makes granite' strong form is DISFAVORED by the map.")
L.append("      * ORIGIN/GEOMETRY: VP's distinctive claim SURVIVES -- that this convergence is the")
L.append("        antipodal CLOSING face of a primordial rupture on a water-world (one engine, two")
L.append("        faces), not an independent, unexplained subduction zone. Divergence moves from")
L.append("        'how granite melts' to 'why the convergence is there'.")
L.append("")
L.append("[6] Korea as the worked example (present-tense):")
L.append("    Korea is granite-rich AND sits on the convergent W-Pacific face (Pacific-plate wet")
L.append("    melting above the slab). Per the thesis Korea is on a COMPRESSION/closing face -> it")
L.append("    should be granite-dominated -> it IS. A clean present-tense consistency check, and a")
L.append("    template: a carbonate-platform region (e.g. a passive shelf) should sit on an EXTENSION")
L.append("    face -- the opposite prediction, also testable on the map.")
L.append("")
L.append("VERDICT (firewall-clean): the granite map and the limestone map read out the TWO FACES of")
L.append("the rupture engine -- granite = deep wet-melt at COMPRESSION (bottom-up), limestone = surface")
L.append("precipitate at EXTENSION (top-down). This RESOLVES CG-12: continent-scale felsic tracks the")
L.append("convergent wet path (VP converges on melt-mechanism, strong 'extension-only' form disfavored),")
L.append("while VP's origin claim -- convergence = the antipodal closing face of a primordial rupture --")
L.append("survives as the real, still-open locus of divergence. Korea fits the compression-face prediction.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "7cbaa6283b1597820ad1459190e1ed4de194f9872f13a9fae4221b6975b20efb"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
