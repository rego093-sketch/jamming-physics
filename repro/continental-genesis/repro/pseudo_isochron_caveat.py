#!/usr/bin/env python3
"""
Continental-Genesis repro screen 3 -- pseudo-isochron non-uniqueness CAVEAT.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning; absolute ages RECORD both ways.

A two-component physical MIXING line is algebraically identical to an isochron. This is a
real, well-known property of isochron dating (errorchrons / mixing lines). The math is
correct [V]. But it proves NON-UNIQUENESS of an isochron age -- NOT that any age is
'young'. It therefore SUPPORTS the firewall's posture (dates are RECORD, [O] BOTH ways)
and is NEVER load-bearing for a recent reading. Salvaged + regraded from the docx S5.1:
the docx used it to claim deep time is fake; here it is a caveat that an isochron alone
cannot settle an age in either direction.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (two end-member sources; illustrative, fixed) =====
# Two end-members A and B in isochron space (X=P/S, Y=D/S). Chosen to give a POSITIVE-
# slope array -- only a positive-slope line can masquerade as an isochron (isochron slope
# = e^(lambda t) - 1 > 0). The sign subtlety is itself part of the caveat.
XA, YA = 2.0, 1.0      # (P/S, D/S) of end-member A
XB, YB = 10.0, 6.0     # (P/S, D/S) of end-member B
LAMBDA = 1.55125e-10   # 1/yr  238U decay constant (for the pseudo-age readout only)
F_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]   # mixing fractions (fraction of B)
# ===================================================================

def mix(f):
    return ((1-f)*XA + f*XB, (1-f)*YA + f*YB)

# slope of the mixing line (time-INDEPENDENT; pure chemistry)
m = (YB - YA) / (XB - XA)
import math
# pseudo-age a naive reader would extract from slope = e^(lambda t) - 1
t_pseudo = math.log(1.0 + abs(m)) / LAMBDA if (1.0 + m) > 0 else float('nan')

L = []
L.append("PSEUDO-ISOCHRON -- mixing line is identical to an isochron (CAVEAT, not refutation)")
L.append(f"VP-SPEC  SEED={SEED}  dates RECORD, [O] both ways")
L.append("="*64)
L.append("")
L.append("two end-members mixed by fraction f (chemistry only, NO time elapsed):")
L.append("       f        X=P/S        Y=D/S")
for f in F_GRID:
    x, y = mix(f)
    L.append(f"     {f:4.2f}     {x:7.3f}     {y:7.3f}")
L.append("")
L.append("the mixed points fall on a straight line  Y = mX + c  with")
L.append(f"     slope m = (YB-YA)/(XB-XA) = {m:.4f}   (TIME-INDEPENDENT)")
L.append("a reader who mistakes this line for an isochron would 'measure':")
L.append(f"     e^(lambda t) - 1 = |m|  ->  t_pseudo = {t_pseudo/1e9:.2f} Ga  (from ZERO elapsed time)")
L.append("")
L.append("READING (firewall-clean):")
L.append("  * the linear array is REAL and the algebra is exact  [V].")
L.append("  * it proves an isochron age is NON-UNIQUE: a mixing line of the right")
L.append("    chemistry reproduces any 'age' with no time elapsed.")
L.append("  * THEREFORE it does NOT establish 'young'. It establishes that an isochron")
L.append("    ALONE cannot settle an age -- in EITHER direction.")
L.append("  * this is exactly the firewall: absolute ages stay RECORD, occurrence [O].")
L.append("  * (real U-Pb adds concordia + 204Pb to TEST for mixing; and only POSITIVE-slope")
L.append("    arrays masquerade as isochrons, so the caveat is not automatic -- it is never")
L.append("    load-bearing for recency, only a reason an isochron alone cannot close an age.)")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "3f835b8ce42409ae091ef427f58ef11ec25132517ced85cef6ec32faaa93f610"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
