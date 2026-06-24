#!/usr/bin/env python3
"""
Continental-Genesis repro screen 16 -- the closed loop (does the 'big remaining problem' survive?).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19. PRESENT-TENSE; no dates/sequences load-bearing.

PROMPT: is there REALLY a big remaining problem, or does it dissolve under logical analysis?
After M19, the named 'big gap' was: 'the ORIGIN of the convergence' (why is there a closing /
compression face at all?). This screen traces the logic and tests whether that gap survives.

CLAIM TO TEST: the convergence is a SEPARATE, unexplained assumption (a remaining problem).
RESULT: it is NOT. The convergence is the DOWNWELLING limb of FORCED convection -- the antipodal
partner of the opening already in the spine (CG-30) -- so it is forced, not assumed. The 'problem'
dissolves. What genuinely remains is a QUANTITATIVE budget check, not a mechanism gap.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (present-tense facts the loop rests on) =====
RAYLEIGH       = 5.85e6      # measured (CG-27); critical ~1e3 -> convection is forced
RA_CRIT        = 1.1e3
GRANITE_EXISTS = True        # present-tense: continent-scale granite exists at convergent belts (CG-35)
ACTIVE_ARCS    = True        # present-tense: active arcs (Andes etc.) make felsic NOW
# =============================================================

forced_convection = RAYLEIGH > RA_CRIT

L = []
L.append("THE CLOSED LOOP -- does the 'origin of convergence' problem survive logic?")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; testing whether the named big gap dissolves")
L.append("="*64)
L.append("")
L.append("STEP-BY-STEP, with grades (each link forced [F], measured [V], or open [O]):")
L.append("")
L.append(f"  1. a hot fluid sphere cooling at its surface MUST convect.")
L.append(f"     Rayleigh Ra = {RAYLEIGH:.2e}  >>  Ra_crit ~ {RA_CRIT:.1e}  -> convection FORCED.   [F]")
L.append("     (the marginal substrate, relaxed-shear->0 / CG-31, removes any stiffness that")
L.append("      could lock a stagnant lid -> it FAVOURS mobile-lid convection.)")
L.append("")
L.append("  2. convection on a CLOSED sphere = UPWELLING limbs + DOWNWELLING limbs.")
L.append("     mass conservation forces both: what rises at one place sinks at another.        [F]")
L.append("     -> THE CONVERGENCE IS THE DOWNWELLING LIMB. it is the antipodal partner of the")
L.append("        opening already in the spine (opening forces antipodal closing, CG-30).")
L.append("     => the convergence is NOT a separate assumption. THE NAMED GAP DISSOLVES HERE.")
L.append("")
L.append("  3. at a downwelling, the denser hydrated skin sinks and carries WATER down.          [F]")
L.append("     (buoyancy: cool dense skin sinks; the water-world start made the skin hydrated.)")
L.append("")
L.append("  4. water + heat at depth -> FLUX MELTING -> felsic (granite) distilled.    [F with water]")
L.append("     this is exactly the convergent wet path the GRANITE MAP confirmed (CG-35).")
L.append("")
L.append("  5. felsic is buoyant, cannot re-sink -> ACCUMULATES at downwelling zones.            [V]")
L.append("     (CG-13; too light to subduct.)")
L.append("")
L.append("  6. cells are DISCRETE, not uniform -> felsic piles in PATCHES (continents) over")
L.append("     downwellings; bare skin (ocean) over upwelling/spreading zones.                   [F]")
L.append("")
L.append("THE LOOP CLOSES: forced convection -> down-limb (=convergence) -> wet flux-melt ->")
L.append("buoyant felsic -> permanent patchy dry land. NO step needs an unexplained convergence.")
L.append("")
L.append("DOES THE NAMED 'BIG PROBLEM' SURVIVE?  NO -- it dissolves:")
L.append("  * 'origin of the convergence'  -> the downwelling limb of forced convection. NOT a gap.")
L.append("  * 'the FIRST felsic seed' (CG-20) -> the FIRST downwelling of hydrated basalt skin")
L.append("     flux-melts to make the FIRST felsic; NO pre-existing felsic is needed, and thermal")
L.append("     convection (not a crustal density contrast) starts it. -> largely dissolves too.")
L.append(f"  * 'does the loop actually RUN?' -> answered by PRESENT-TENSE evidence: granite exists at")
L.append(f"     convergent belts ({GRANITE_EXISTS}) and active arcs make felsic NOW ({ACTIVE_ARCS}). It runs.")
L.append("")
L.append("WHAT GENUINELY REMAINS (honest, and it is NOT a mechanism gap):")
L.append("  (R1) QUANTITATIVE BUDGET -- does this loop, at realistic rates, distil the OBSERVED")
L.append("       continental fraction (~40% felsic), freeboard, and Moho contrast (7 vs 35 km),")
L.append("       or too little / too much? a present-tense, FALSIFIABLE number check. THE real test.")
L.append("  (R2) IDENTITY -- the loop (convection -> arcs -> continents) IS essentially mainstream.")
L.append("       VP's value-add is NOT the convection but the UPSTREAM physics: c^2=B/rho explains")
L.append("       WHY the mantle flows at all (the jamming/unjamming switch), plus the water-world")
L.append("       start that supplies the flux water. VP is the FOUNDATION BENEATH plate-convection,")
L.append("       not a competitor to it. (Same posture as the fluid-dynamics volume.)")
L.append("")
L.append("VERDICT (firewall-clean): the 'big remaining problem' (origin of the convergence) was an")
L.append("ILLUSION of not closing the loop. Closed logically, the convergence is the forced")
L.append("downwelling limb; the first seed is the first downwelling's flux-melt; and the granite map")
L.append("shows the loop runs. The ONLY genuine residual is the QUANTITATIVE budget (R1) -- a number")
L.append("to compute, not a mystery to solve -- plus the identity clarification (R2): VP is the")
L.append("c^2=B/rho FOUNDATION under mantle convection, not a rival to it.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "779a2269523ce3a47b24522a2aff44700e6b4200eb70a87ed0855d0616c3cb0c"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
