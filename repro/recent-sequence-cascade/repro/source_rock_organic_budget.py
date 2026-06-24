#!/usr/bin/env python3
"""
Module 28 reproducibility script - Source-rock organic-richness budget.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

A present-tense mass balance. From MEASURED organic-carbon rain, MEASURED burial
efficiency, and MEASURED bulk mineral sedimentation, it computes the resulting
organic-carbon weight fraction (TOC) and what is needed to reach the observed TOC
of real source rocks. No absolute age or reconstructed past rate is used; the
inputs are present-day measured fluxes (same class as the observed snowfall rate
in Module 25). Occurrence stays [O], both directions. The DILUTION paradox is
made explicit.
"""
import hashlib

SEED = 19  # VP-SPEC convention (no RNG; determinism is structural)

# ===== LOCK BLOCK (present-day measured fluxes; g per m2 per yr unless noted) =====
R_OXIC_OPEN = 5.0    # open-ocean background organic-C rain to seafloor (measured)
R_HIGH_PROD = 60.0   # high-productivity / mass-supply ("event-like") organic-C rain
BE_OXIC     = 0.01   # burial efficiency, normal oxic seafloor (~1% survives)
BE_ANOXIC   = 0.20   # burial efficiency, anoxic / euxinic (~20% survives)
M_NORMAL    = 100.0  # ordinary clastic mineral dilution
M_LOW       = 15.0   # low-clastic / restricted (rift) basin dilution
OM_PER_OC   = 2.0    # organic-matter mass per organic-carbon mass (H,O,N included)
TOC_TARGETS = [0.01, 0.02, 0.05, 0.10, 0.20]  # observed source-rock TOC fractions
# =================================================================================

def toc(R_org, BE, M):
    OCb = R_org * BE                      # buried organic-carbon flux
    return OCb / (M + OM_PER_OC * OCb)    # organic-C weight fraction (TOC)

def org_needed_fraction(target):
    # buried organic-C flux required, as a fraction of mineral flux M, to reach target TOC:
    # target = OCb / (M + 2*OCb)  ->  OCb/M = target / (1 - 2*target)
    return target / (1.0 - OM_PER_OC * target)

L = []
L.append("SOURCE-ROCK ORGANIC BUDGET  (present-tense mass balance; no absolute age)")
L.append(f"LOCK  OM/OC={OM_PER_OC}  SEED={SEED}")
L.append("")
L.append("resulting TOC for four present-day flux regimes:")
L.append(f"  (1) oxic, open ocean, normal dilution      TOC = {toc(R_OXIC_OPEN, BE_OXIC, M_NORMAL)*100:7.3f} %")
L.append(f"  (2) anoxic, normal supply, normal dilution  TOC = {toc(R_OXIC_OPEN, BE_ANOXIC, M_NORMAL)*100:7.3f} %")
L.append(f"  (3) anoxic, normal supply, LOW dilution      TOC = {toc(R_OXIC_OPEN, BE_ANOXIC, M_LOW)*100:7.3f} %")
L.append(f"  (4) anoxic, HIGH supply, LOW dilution        TOC = {toc(R_HIGH_PROD, BE_ANOXIC, M_LOW)*100:7.3f} %")
L.append("")
L.append("to REACH an observed TOC, buried organic-C must be this fraction of mineral flux:")
for t in TOC_TARGETS:
    L.append(f"  TOC = {t*100:5.1f} %   ->   buried organic-C >= {org_needed_fraction(t)*100:7.2f} % of mineral flux")
L.append("  (DILUTION paradox: faster mineral burial RAISES M in the denominator)")
L.append("")
L.append("READING (firewall-clean, symmetric):")
L.append("  Normal oxic burial yields ~0.05% TOC. Reaching the several-to-tens-% TOC of real")
L.append("  source rocks FORCES three conditions AT ONCE: high organic supply, anoxic")
L.append("  preservation, and low mineral dilution. That requirement is forced. Whether it is")
L.append("  met by a single coupled event (mass-mortality supply + self-generated anoxia +")
L.append("  rift-basin low dilution) or by sustained background coincidence is [O], both ways.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "d6221d6ed5f66f3d0c8971c366986828c0ff12ae90a88ce3dc05bacb0ccd5e12"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
