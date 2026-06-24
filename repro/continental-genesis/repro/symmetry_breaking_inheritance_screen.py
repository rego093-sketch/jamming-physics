#!/usr/bin/env python3
"""
Continental-Genesis repro screen 13 -- why one side? (inherited symmetry-breaking).
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19. PRESENT-TENSE only; dates/sequences RECORD both ways.

INHERITS from the Configured-Continuum (fluid-dynamics) volume, concept DOI 10.5281/zenodo.17972568:
  * a MARGINAL JAMMED substrate is a fluid by arrangement: relaxed shear modulus -> 0 while
    bulk modulus B stays finite (c^2 = B/rho).  [LOCK in that volume]
  * 'marginal' = isostatic margin: the medium is poised at the threshold, with NO restoring
    shear stiffness to a shear/transport perturbation.
This is exactly the M11 picture (mantle: hot, jammed, near unjamming). So we INHERIT the
substrate property, not a new mechanism.

THE AUTHOR'S CLAIM: 'any fluid has imbalance; a leaning/one-sided outflow logic ALWAYS occurs.'
HONEST SPLIT (the firewall + the M14 audit forbid over-inheriting):
  * WHAT IS INHERITED [F]: a marginal (zero-relaxed-shear) medium has NO restoring force against
    a transport perturbation -> perturbations do NOT decay; the symmetric state is NEUTRAL/unstable.
    So a one-sided channel, once seeded, is NOT opposed by the substrate. (Symmetry-breaking is
    PERMITTED -- even favoured -- not forbidden.)
  * WHAT IS NOT INHERITED [O]: that breaking is GUARANTEED, that it picks ONE side (vs many cells),
    its DIRECTION, and its TIMING. 'Always occurs' overstates: marginality removes the RESTORING
    force; it does not by itself force a single global lean. Which/where/when stay [O].
This screen makes that split quantitative with the restoring-stiffness ratio.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (inherited substrate property, present-tense) =====
# relaxed shear modulus at the marginal (isostatic) point, normalized to bulk modulus B.
# Inherited result: G_relaxed -> 0 at the margin; B finite.
G_REL_OVER_B = [1.0, 0.5, 0.1, 0.01, 0.0]   # away-from-margin ... AT margin
# a transport/shear perturbation of unit amplitude: restoring 'force' ~ G_relaxed * k^2 (schematic,
# units of B); we report the restoring stiffness relative to bulk, to show it vanishes.
# =====================================================================

L = []
L.append("WHY ONE SIDE? -- inherited symmetry-breaking capacity (bounded)")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; inherits c^2=B/rho substrate (DOI .17972568)")
L.append("="*64)
L.append("")
L.append("[1] inherited substrate property (present-tense [F], from the fluid-dynamics volume):")
L.append("    at the marginal/isostatic point the RELAXED SHEAR modulus -> 0, B stays finite.")
L.append("    restoring stiffness against a transport perturbation ~ G_relaxed (units of B):")
L.append("       G_rel/B      restoring force vs a sideways/transport perturbation")
for g in G_REL_OVER_B:
    state = "AT MARGIN -> NO restoring force (perturbation does not decay)" if g==0.0 else \
            ("near margin -> weak restoring" if g<=0.1 else "stiff -> perturbation relaxes back")
    L.append(f"       {g:5.2f}        {state}")
L.append("")
L.append("[2] WHAT THIS INHERITS (the legitimate part) [F]:")
L.append("    a medium with ZERO relaxed shear stiffness does NOT restore a symmetric transport")
L.append("    state -> a one-sided channel, once seeded, is NOT opposed by the substrate.")
L.append("    SYMMETRY-BREAKING IS PERMITTED / FAVOURED, not forbidden. This is the inherited")
L.append("    answer to 'why is one-sidedness possible at all': the marginal medium allows it.")
L.append("    (Same substrate as M11: mantle = hot, jammed, near unjamming.)")
L.append("")
L.append("[3] WHAT THIS DOES NOT INHERIT (the over-claim to avoid) [O]:")
L.append("    * that breaking is GUARANTEED ('always occurs') -- marginality removes the")
L.append("      RESTORING force; it does not by itself FORCE a break. Neutral != obligatory.")
L.append("    * that it picks ONE global side vs MANY convection cells (degree-1 vs higher).")
L.append("    * the DIRECTION (which side) and the TIMING (when) -- [O], RECORD both ways.")
L.append("    'Any fluid has imbalance, so a lean always occurs' OVERSTATES: it conflates")
L.append("    'not opposed' (inherited [F]) with 'forced' (NOT inherited, [O]).")
L.append("")
L.append("[4] how this plugs into the assembly chain (M15/CG-30):")
L.append("    M15 STEP 1-3 showed: GIVEN an opening, conservation+buoyancy+kinematics FORCE a")
L.append("    one-sided felsic pile. This screen supplies the missing UPSTREAM permission: the")
L.append("    marginal substrate does not RESIST the initial symmetry break that seeds the")
L.append("    opening. So the chain reads:")
L.append("      marginal substrate (no restoring) --PERMITS--> a symmetry break [F-permits, O-forces]")
L.append("        --IF it occurs--> opening --FORCES--> antipodal closing --FORCES--> one-sided pile [F]")
L.append("    The break is PERMITTED [F] but not FORCED [O]; everything after the opening is FORCED [F].")
L.append("")
L.append("VERDICT (firewall-clean): INHERIT the symmetry-breaking CAPACITY (marginal medium has no")
L.append("restoring shear -> one-sidedness is permitted/favoured, [F]); do NOT inherit INEVITABILITY,")
L.append("side, count, or timing ([O]). This strengthens CG-30 by grounding its one unstated premise")
L.append("(why a break is allowed) in the inherited c^2=B/rho substrate -- without overstating it.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "ca63495cdc2b713f053548f1fb31742a002a8760f4bd76c2d4d13994fe33a551"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
