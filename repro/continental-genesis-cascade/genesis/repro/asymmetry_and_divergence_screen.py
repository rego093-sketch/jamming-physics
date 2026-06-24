#!/usr/bin/env python3
"""
Continental-Genesis repro screen 10 -- where the thesis really diverges from mainstream.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

Tests CG-28 (the hemispheric continental asymmetry) AS A DISCRIMINATOR, and -- following the
author's own point ("the divergence is at WHY continents formed in the first place") -- locates
the real divergence.

RESULT (firewall-honest): the asymmetry is a [V] observable, but as a DISCRIMINATOR it is
DEGENERATE, and its strong 'primordial permanent scar' reading is DISFAVORED by data (continents
reconfigure; today's spread is MORE even than Pangaea -> the asymmetry is FADING, not fixed;
Pacific = the persistent Panthalassa superocean). So CG-28 is DOWNGRADED. The genuine divergence
is the ORIGIN/COMPOSITION question (how felsic crust was first made) -- which mainstream's
supercontinent cycle ASSUMES, not explains. That divergence is precisely CG-12 (can a rupture
distil continent-scale felsic WITHOUT subduction?), and the present-tense ARC GEOCHEMICAL
signature of bulk continental crust is the test -- which currently LEANS mainstream.
No absolute age is load-bearing.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK =====
LAND_FRAC_GLOBAL = 0.29     # land = ~29% of Earth's surface
LAND_HEMI_SHARE  = 0.81     # land hemisphere holds ~81% of all land (pole ~47N 2W)
PANGAEA_SURF_FRAC = 0.33    # Pangaea covered ~1/3 of the surface, ~one hemisphere
# =====================

def hemi_land_pct(share):
    # land in a hemisphere / area of that hemisphere (hemisphere = 0.5 of surface)
    return (share * LAND_FRAC_GLOBAL) / 0.5

land_hemi = hemi_land_pct(LAND_HEMI_SHARE) * 100
water_hemi = hemi_land_pct(1 - LAND_HEMI_SHARE) * 100
ratio = LAND_HEMI_SHARE / (1 - LAND_HEMI_SHARE)

L = []
L.append("WHERE THE THESIS REALLY DIVERGES -- asymmetry as discriminator, and the origin")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; ages RECORD both ways")
L.append("="*64)
L.append("")
L.append("[1] the asymmetry, quantified (present-tense [V]):")
L.append(f"    land hemisphere: {land_hemi:.0f}% land  |  water hemisphere: {100-water_hemi:.0f}% ocean")
L.append(f"    one-sided concentration ratio = {ratio:.1f} : 1  (degree-1 / hemispheric)")
L.append("")
L.append("[2] is the asymmetry a DISCRIMINATOR for the single-rupture thesis?  NO.")
L.append("    mainstream explains it cleanly AND the strong 'primordial scar' reading is")
L.append("    DISFAVORED by data:")
L.append("    * Pacific = the persistent Panthalassa superocean (direct continuation).")
L.append("    * continents demonstrably RECONFIGURE (Vaalbara..Rodinia..Pangaea); the")
L.append("      asymmetry's orientation has changed repeatedly -> not a fixed scar.")
L.append(f"    * Pangaea was ~{PANGAEA_SURF_FRAC*100:.0f}% surface in ~one hemisphere (MORE concentrated);")
L.append("      today's spread is MORE even -> the asymmetry is FADING, not permanent.")
L.append("    => the asymmetry is DEGENERATE (both accounts fit the snapshot via different")
L.append("       histories), and the permanent-scar reading LEANS AGAINST the data.")
L.append("    => CG-28 DOWNGRADED: a real [V] observable, but NOT where the thesis diverges.")
L.append("")
L.append("[3] where it ACTUALLY diverges (the author's point) -- the ORIGIN:")
L.append("    the supercontinent cycle / Panthalassa ASSUMES continental crust exists; it")
L.append("    describes how it MOVES, not WHY felsic crust exists or how the FIRST crust formed.")
L.append("    THAT is the genuine divergence -- and it is precisely CG-12:")
L.append("      mainstream: felsic grows at SUBDUCTION ARCS over ~4 Gyr (water-fluxed melting).")
L.append("      thesis:     felsic distils from a RUPTURE's wet-remelt face (M05).")
L.append("    both use wet melting -> the divergence is the SETTING/efficiency, testable by:")
L.append("")
L.append("[4] the present-tense test of the origin -- ARC GEOCHEMICAL signature:")
L.append("    bulk continental crust is andesitic with a Nb-Ta depletion ('arc signature').")
L.append("    this is mainstream's main present-tense evidence for ARC growth -> currently")
L.append("    LEANS MAINSTREAM. For the thesis to diverge it must either (a) show a rupture")
L.append("    path that REPRODUCES the arc signature, or (b) find felsic WITHOUT it at scale.")
L.append("    Tied to CG-12: if pure extension cannot make continent-scale felsic (Iceland =")
L.append("    minor rhyolite), the thesis NEEDS a subduction-like deep-water path -> CONVERGES")
L.append("    with mainstream; if it can, it DIVERGES. CG-12 is the real pivot, not the asymmetry.")
L.append("")
L.append("VERDICT (firewall-clean):")
L.append("  * CG-28 (asymmetry) DOWNGRADED: [V] observable, DEGENERATE discriminator, strong")
L.append("    reading disfavored. Not the divergence point. (Corrects its prior elevation.)")
L.append("  * the author is RIGHT that the divergence is the ORIGIN ('why continents at all').")
L.append("    Precisely: CG-12 (rupture vs arc felsic) + the arc-signature test -- which today")
L.append("    LEANS mainstream. The thesis's real, falsifiable edge is there, not in the map.")
L.append("  * rate/when stays [O] both ways. falsification = discovery.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "985b4c39ba139a9dd38f3950473a16805aea370795b0efff9da5c137be09d6b6"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
