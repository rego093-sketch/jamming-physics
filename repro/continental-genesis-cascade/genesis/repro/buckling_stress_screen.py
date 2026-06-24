#!/usr/bin/env python3
"""
Continental-Genesis repro screen 1 -- compression-face buckling.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

Turns "a huge lateral push folds/thickens the skin" from an ASSERTION into a CALCULABLE
stress bar. Computes the Euler critical compressive stress for an elastic plate of
thickness h buckling at half-wavelength L:
        sigma_cr = pi^2 E / [12 (1 - nu^2)] * (h/L)^2
This is a present-tense feasibility screen [F]: it uses no age and asserts no occurrence.
It only asks: what lateral stress is required to deform the mantle-skin, and is that
attainable? (Salvaged + regraded from the rejected docx S5.2; the docx used buckling to
prop a global narrative -- here it is just the [F] screen for the compression step.)
"""
import hashlib, math

SEED = 19  # VP-SPEC convention (no RNG; determinism is structural)

# ===== LOCK BLOCK (measured/standard inputs; changing any value defines a new version) =====
E      = 70.0e9     # Pa     Young's modulus of crustal rock (LOCK, mid-range 50-100 GPa)
NU     = 0.25       # -      Poisson's ratio (LOCK)
H_M    = 30.0e3     # m      plate (skin) thickness to screen (LOCK)
L_KM   = [100, 150, 200, 300, 450, 600]      # km   half-wavelengths to screen
ROCK_STRENGTH_MPA = 1000.0   # MPa  ~order of crustal strength; above this, pure Euler
                             #      buckling needs a weak layer / longer wavelength
# =========================================================================================

def sigma_cr_MPa(L_m):
    return (math.pi**2 * E / (12.0 * (1.0 - NU**2)) * (H_M / L_m)**2) / 1.0e6

L = []
L.append("COMPRESSION-FACE BUCKLING -- feasibility screen for 'push -> fold/thicken'")
L.append(f"VP-SPEC  SEED={SEED}  present-tense [F]; no age, no occurrence")
L.append(f"LOCK  E={E/1e9:.0f} GPa   nu={NU}   plate h={H_M/1e3:.0f} km")
L.append("="*64)
L.append("")
L.append("critical lateral compressive stress to buckle the skin:")
L.append("    half-wavelength      sigma_cr        regime")
for Lkm in L_KM:
    s = sigma_cr_MPa(Lkm*1e3)
    reg = "needs weak layer / longer lambda" if s > ROCK_STRENGTH_MPA else "ATTAINABLE tectonic stress"
    L.append(f"    {Lkm:6d} km        {s:9.0f} MPa   {reg}")
L.append("")
L.append("READING (firewall-clean):")
L.append("  * buckling/thickening of the skin is PHYSICALLY PERMITTED at long wavelength")
L.append("    (hundreds of MPa) -> the compression step is FEASIBLE  [F].")
L.append("  * it converts 'huge push' into a CALCULABLE stress bar: the longer the")
L.append("    observed fold wavelength, the lower the required stress. This is a")
L.append("    present-tense, chronology-free constraint on the push MAGNITUDE.")
L.append("  * magnitude/rate of the actual push stays  [O] both ways; only the")
L.append("    threshold (what stress IS needed) is load-bearing here.")
L.append("  * contrast: this sits in the real 100s-MPa-to-GPa regime, UNLIKE the")
L.append("    rejected zircon-reset claim, which missed its own constants by ~10 orders.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "811aba1d1b0e625ad4cf82bca00ebf21d52242fa65076a7f9032f0e6afa020f3"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
