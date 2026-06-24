#!/usr/bin/env python3
"""
Continental-Genesis repro screen 7 -- the isostatic-compensation law for thick relief.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

Replaces the ROUGH CG-22/23 wording ("bare skin folds long-lambda/low-amplitude") with a
PRECISE, falsifiable law plus a present-tense [V] discriminator (free-air gravity / Moho).

LAW: the maximum ISOSTATICALLY-COMPENSATED relief a crust can support is
        h_max ~= dH * (rho_m - rho_c) / (rho_m - rho_top)     [m]
 (rho_top = rho_water for submarine, ~0 for subaerial), where dH is the crustal thickening
 available. Tall COMPENSATED relief therefore needs a deep, LIGHT root -- i.e. thick FELSIC
 crust. Normal (7 km basaltic) ocean skin cannot make one. Consequences, all checkable now:
   * continental collision (felsic, 35->70 km): h ~ 5 km, COMPENSATED (deep root, small FAA).
   * normal ocean skin folded/doubled (basalt, 7->14 km): h ~ 1 km only (central Indian Ocean).
   * over-thick igneous plateau (basalt LIP, 7->30 km): h ~ a few km, COMPENSATED (special case).
   * any TALLER relief on normal ocean skin (e.g. Gorringe ~5 km) is UNCOMPENSATED -- large
     positive free-air anomaly, shallow flat Moho, held DYNAMICALLY by active thrust stress at
     an incipient boundary -> transient, not a stable mountain.
The free-air gravity anomaly + Moho depth is the [V] test that can FALSIFY this law (a
compensated multi-km bare-ocean high with a deep light root would break it).
No absolute age is load-bearing.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (measured densities; thickening scenarios) =====
RHO_M     = 3300.0   # kg/m^3  mantle
RHO_FEL   = 2800.0   # kg/m^3  felsic continental crust
RHO_BAS   = 2900.0   # kg/m^3  basaltic oceanic crust
RHO_W     = 1027.0   # kg/m^3  seawater
# scenarios: (label, rho_crust, dH_m, subaerial?)
SCEN = [
    ("continental collision (felsic 35->70 km)", RHO_FEL, 35.0e3, True),
    ("normal ocean skin doubled (basalt 7->14)", RHO_BAS,  7.0e3, False),
    ("igneous plateau / LIP (basalt 7->30 km)",  RHO_BAS, 23.0e3, False),
]
# =================================================================

def h_max(rho_c, dH, subaerial):
    rho_top = 0.0 if subaerial else RHO_W
    return dH * (RHO_M - rho_c) / (RHO_M - rho_top)

L = []
L.append("ISOSTATIC-COMPENSATION LAW FOR THICK RELIEF  (precise CG-24)")
L.append(f"VP-SPEC  SEED={SEED}  present-tense [F]/[V]; no age, no occurrence")
L.append(f"LOCK  rho_m={RHO_M:.0f} rho_felsic={RHO_FEL:.0f} rho_basalt={RHO_BAS:.0f} rho_water={RHO_W:.0f}")
L.append("="*64)
L.append("")
L.append("max COMPENSATED relief  h_max = dH*(rho_m-rho_c)/(rho_m-rho_top):")
L.append("    scenario                                    h_max")
for label, rc, dH, sub in SCEN:
    L.append(f"    {label:<42} {h_max(rc,dH,sub):6.0f} m")
L.append("")
L.append("  -> normal 7 km basaltic skin, even DOUBLED, supports only ~1 km compensated")
L.append("     relief -- matching the central Indian Ocean (1-2 km diffuse folds).")
L.append("  -> felsic collision supports ~5 km (deep light root) -- continental mountains.")
L.append("  -> only special igneous OVER-thickening (LIP) gives a few km of basaltic relief,")
L.append("     and even that stays below continental heights (basalt's smaller contrast).")
L.append("")
L.append("PRESENT-TENSE [V] CENSUS (verified) -- the test set:")
L.append("    case                 relief   wavelength   compensation (free-air / Moho)   verdict")
L.append("    central Indian Ocean 1-2 km   100-300 km   flexural/low; diffuse folding    FITS (no root, low h)")
L.append("    oceanic LIP plateau  ~2-3 km  >1000 km     COMPENSATED (thick basalt root)  FITS (basalt-capped)")
L.append("    Gorringe Bank        ~5 km    ~80-200 km   UNCOMPENSATED (+FAA, shallow Moho) FITS (dynamic, boundary)")
L.append("    continental orogen   5-8 km   broad        COMPENSATED (deep FELSIC root)   the felsic-root case")
L.append("")
L.append("READING (firewall-clean):")
L.append("  * the ROUGH claim 'bare skin stays low-amplitude' is now a PRECISE LAW: tall")
L.append("    COMPENSATED relief requires a deep light (felsic) root; normal ocean skin")
L.append("    cannot build one, so it is capped at ~1-2 km (central Indian Ocean).")
L.append("  * multi-km relief on bare ocean skin (Gorringe) is UNCOMPENSATED and dynamic --")
L.append("    diagnosed by a LARGE POSITIVE free-air anomaly + shallow flat Moho. Transient.")
L.append("  * FALSIFIER: a compensated multi-km bare-ocean high with a DEEP LIGHT root (small")
L.append("    free-air anomaly, deep Moho, no felsic) would break the law. None known -> stands.")
L.append("")
L.append("HONEST grade & scope:")
L.append("  * the compensation arithmetic is [F]; the free-air/Moho census is [V].")
L.append("  * DEGENERATE as a discriminator -- compensated-vs-uncompensated topography is")
L.append("    textbook isostasy. Its value here is (a) it makes CG-22/23 PRECISE & FALSIFIABLE")
L.append("    (replacing rough wording with a law + a gravity test), and (b) internal economy:")
L.append("    the SAME felsic-buoyancy that distils continents (M05-06) and gates crumpling")
L.append("    (M08) also sets why only FELSIC crust carries compensated mountains. One engine.")
L.append("  * CG-24 grade: [F]/[V] precise law; rate/when stays [O] both ways.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "b309631e99cebc627c34fa1fcb1fdea629339f920e85429c4c2e5bd87f2b38ed"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
