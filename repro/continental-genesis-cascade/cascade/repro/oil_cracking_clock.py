#!/usr/bin/env python3
"""
Module 27 reproducibility script - Oil-cracking metastability clock.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

Computes the forward thermal-cracking lifetime tau(T) of light oil from measured
Arrhenius kinetics and the PRESENT-DAY measured reservoir temperature T. tau is a
present-tense quantity (an e-folding lifetime, like a half-life): it does NOT use,
assert, or import any absolute age. Occurrence and basin age stay [O], BOTH
directions. Survival is reported ONLY against the dimensionless ratio r = residence/tau,
never an absolute time, so no chronology enters as load-bearing.
"""
import hashlib, math

SEED = 19  # VP-SPEC convention (no RNG is used; determinism is structural)

# ===== LOCK BLOCK (measured inputs; changing any value defines a new version) =====
R          = 8.314        # J/mol/K   gas constant (CODATA)
EA         = 230.0e3      # J/mol     activation energy, oil -> gas + pyrobitumen (LOCK)
A          = 1.0e13       # 1/s       frequency factor (LOCK)
SEC_PER_YR = 3.15576e7    # s/yr      Julian year
# Present-day MEASURED reservoir temperatures to screen (deg C) - present-tense observable.
T_C_GRID   = [90, 110, 130, 150, 160, 170, 180, 190]
# Honest sensitivity pairs (compensation effect; literature Ea~200-290 kJ/mol, A~1e13-1e28).
SENS       = [(220.0e3, 1.0e13), (230.0e3, 1.0e13), (250.0e3, 1.0e14)]
R_GRID     = [0.1, 1.0, 3.0, 5.0, 10.0]   # dimensionless residence/tau for survival
# =================================================================================

def tau_years(T_C, Ea, Afac):
    T = T_C + 273.15
    k = Afac * math.exp(-Ea / (R * T))    # 1/s forward cracking rate (present-tense)
    return (1.0 / k) / SEC_PER_YR

def human(y):
    if y >= 1.0e9: return f"{y/1.0e9:10.2f} Gyr"
    if y >= 1.0e6: return f"{y/1.0e6:10.2f} Myr"
    if y >= 1.0e3: return f"{y/1.0e3:10.2f} kyr"
    return f"{y:10.2f} yr"

L = []
L.append("OIL-CRACKING METASTABILITY CLOCK  (present-tense; no absolute age used)")
L.append(f"LOCK  Ea={EA/1e3:.1f} kJ/mol   A={A:.2e}/s   R={R} J/mol/K   SEED={SEED}")
L.append("")
L.append("e-folding lifetime tau at the MEASURED reservoir temperature:")
L.append("    T(meas)         tau")
for Tc in T_C_GRID:
    L.append(f"    {Tc:4d} C   {human(tau_years(Tc, EA, A))}")
L.append("")
L.append("sensitivity to kinetics (Ea kJ/mol, A /s) -> tau at 150 C and 190 C:")
for Ea, Af in SENS:
    L.append(f"    Ea={Ea/1e3:5.0f}  A={Af:.0e}   150C: {human(tau_years(150,Ea,Af)).strip()}   190C: {human(tau_years(190,Ea,Af)).strip()}")
L.append("")
L.append("survival of light oil vs DIMENSIONLESS residence  r = residence/tau:")
for r in R_GRID:
    L.append(f"    r={r:5.1f}   remaining fraction = {math.exp(-r):.5f}")
L.append("    (residence is held-out RECORD; only the ratio r is load-bearing)")
L.append("")
L.append("READING (firewall-clean, symmetric):")
L.append("  Light high-H/C oil at a HOT measured temperature is METASTABLE with short tau.")
L.append("  Above ~180-190 C every plausible kinetic choice gives tau << deep-time: there")
L.append("  the deep-time reading carries a heavy PRESERVATION burden. Below, it is kinetics-")
L.append("  sensitive. The recent/continuous-charge reading carries a CHARGE burden instead.")
L.append("  Occurrence and basin age stay [O], BOTH directions; tau itself is [V] present-tense.")

body = "\n".join(L)
print(body)

h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "a2bcfc0dced80f41dfc3f4007482ec4e77afe89f50aaaa29d43a3a2dd38118ce"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
