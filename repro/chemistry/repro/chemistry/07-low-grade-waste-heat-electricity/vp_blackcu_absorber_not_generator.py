# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module
# Paper section: CA.9c black copper is absorber, not converter
# Deterministic, standard-library + numpy only. Run twice -> identical sha256.
# Expected RESULT sha256 prefix: 0067cbe1...
# (Compute core extracted from the working session script; plotting removed -
#  the hash is computed over the numeric arrays only, so it is unchanged.)

# -*- coding: utf-8 -*-
"""
Can 'heat pump collects heat -> black copper generates electricity' work? No -- two failure points.
Key misconception: black copper is an ABSORBER (radiation->heat), NOT a converter (heat->electricity).
1) heat pump (electric) to gather/upgrade heat FOR GENERATION = net loss (inverse argument, shown earlier).
2) black copper has NO heat->electricity mechanism: Seebeck ~1.8 uV/K (negligible), not a TPV cell, not an
   engine, and it MELTS at 1085C so it can't even be a high-T TPV emitter.
Real heat->electricity: HIGH-temp heat (concentrate / resistive) -> hot store -> a REAL converter (turbine or TPV cell).
"""
import hashlib, numpy as np

S_cu = 1.8e-6      # copper Seebeck, V/K (negligible)
Tmelt_cu = 1085.0  # C
print("BLACK COPPER — what it is and isn't")
print(f"  ABSORBER: solar absorptance ~0.95 -> turns radiation INTO heat. YES (this is its job)")
print(f"  CONVERTER heat->electricity: NO.  Seebeck ~{S_cu*1e6:.1f} uV/K (negligible); not a TPV cell; not an engine")
print(f"  melts at {Tmelt_cu:.0f} C -> cannot be a high-T TPV emitter (those run 1000-2400 C)")
print("Two failure points:")
print("  (1) heat pump (electric) to gather heat for GENERATION = net loss (COP x eta_Carnot = 1)")
print("  (2) black copper cannot convert heat -> electricity (absorber, not converter)")
print("Real chain: HIGH-temp heat (concentrate solar / resistive) -> hot sand -> turbine (~35-50%) or TPV cell (~40%)")
print("RESULT sha256 = "+hashlib.sha256(np.array([S_cu,Tmelt_cu]).tobytes()).hexdigest())
