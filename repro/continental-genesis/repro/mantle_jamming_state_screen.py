#!/usr/bin/env python3
"""
Continental-Genesis repro screen 8 -- the mantle's jamming state.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

The author's refinement: the 'heavy fluid' that lets the deep floor flatten is, in jamming
terms, HOT -- near magma. This screen confirms the KERNEL and bounds the DEGREE with data.

KERNEL (correct, [F] in jamming language): the mantle flows like a heavy fluid on long
timescales because it is HOT and sits CLOSE to its unjamming (melting) threshold -- a jammed
solid near the transition. That is exactly why it convects and creeps.

BOUND (present-tense [V], from seismology): it is NOT bulk magma. (1) The mantle TRANSMITS
S-waves through its whole depth -> shear modulus mu > 0 -> SOLID; a liquid has mu = 0 and
passes NO S-waves (that is how we know the OUTER CORE is liquid -- the S-wave shadow). (2) Its
viscosity is ~10^15-10^21x that of magma. So 'magma level' overshoots by ~15-20 orders; the
correct picture is a jammed SOLID near unjamming that CROSSES the threshold only LOCALLY
(ridges by decompression, plumes by heat, subduction by water). The 'thin solid skin over
fluid' maps onto LITHOSPHERE (skin) over ASTHENOSPHERE (hot, near-solidus, ~1% melt, flows).
No absolute age is load-bearing.
"""
import hashlib, math

SEED = 19

# ===== LOCK BLOCK (standard rheology / seismology values) =====
ETA_ASTH   = 1.0e21   # Pa s   asthenosphere viscosity
ETA_LOWER  = 1.0e22   # Pa s   lower-mantle viscosity
ETA_BAS    = 1.0e2    # Pa s   basaltic magma viscosity
ETA_RHY    = 1.0e6    # Pa s   rhyolitic magma viscosity
MU_MANTLE  = 1.0e11   # Pa     mantle shear modulus (>0 => transmits S-waves => SOLID)
MU_LIQUID  = 0.0      # Pa     any true liquid (magma, outer core): mu = 0 => NO S-waves
SEC_PER_YR = 3.15576e7
# homologous-temperature anchors (adiabat vs dry peridotite solidus, upper mantle)
T_ADIABAT_C = 1350.0  # deg C  mantle potential/adiabat temperature
T_SOLIDUS_C = 1500.0  # deg C  approx dry solidus at ~100 km (raised by pressure)
# =============================================================

def maxwell_time_yr(eta, mu):
    return (eta / mu) / SEC_PER_YR

T_h = (T_ADIABAT_C + 273.15) / (T_SOLIDUS_C + 273.15)   # homologous temperature (K/K)

L = []
L.append("THE MANTLE'S JAMMING STATE -- jammed solid near unjamming, NOT magma")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; ages RECORD both ways")
L.append("="*64)
L.append("")
L.append("[1] viscosity: is the mantle 'magma level'?  NO -- by ~15-20 orders.")
L.append(f"    asthenosphere eta = {ETA_ASTH:.0e} Pa s ;  lower mantle = {ETA_LOWER:.0e} Pa s")
L.append(f"    magma eta = {ETA_BAS:.0e} (basalt) .. {ETA_RHY:.0e} (rhyolite) Pa s")
L.append(f"    ratio mantle/magma = {ETA_ASTH/ETA_RHY:.0e} .. {ETA_ASTH/ETA_BAS:.0e}")
L.append("    -> 'magma level' overshoots by ~15-20 orders of magnitude.")
L.append("")
L.append("[2] Maxwell time tau = eta/mu  (solid below tau, fluid above):")
L.append(f"    asthenosphere: tau = {maxwell_time_yr(ETA_ASTH, MU_MANTLE):.0f} yr")
L.append(f"    lower mantle : tau = {maxwell_time_yr(ETA_LOWER, MU_MANTLE):.0f} yr")
L.append("    -> SOLID on short timescales (seismic seconds: S-waves pass), FLUID on long")
L.append("       timescales (convection, Myr). The 'heavy fluid' behaviour is the LONG-")
L.append("       timescale face of a SOLID -- not a liquid.")
L.append("")
L.append("[3] the decisive present-tense BOUND -- S-waves:")
L.append(f"    mantle shear modulus mu = {MU_MANTLE:.0e} Pa  > 0  -> transmits S-waves -> SOLID")
L.append(f"    any true liquid (magma / outer core) mu = {MU_LIQUID:.0f}  -> NO S-waves")
L.append("    OBSERVED: S-waves cross the WHOLE mantle to the core-mantle boundary; the")
L.append("    S-wave SHADOW begins only at the OUTER CORE. => the mantle is SOLID, the outer")
L.append("    core is the liquid. 'Bulk magma mantle' is FALSIFIED. (The shell-over-fluid")
L.append("    intuition is right one level up: LITHOSPHERE skin over ASTHENOSPHERE.)")
L.append("")
L.append(f"[4] but it IS hot, near the unjamming threshold:  T/T_solidus ~ {T_h:.2f}")
L.append(f"    (adiabat ~{T_ADIABAT_C:.0f} C vs dry solidus ~{T_SOLIDUS_C:.0f} C, upper mantle)")
L.append("    -> homologous T ~0.7-0.95: hot, CLOSE to but BELOW melting => jammed near")
L.append("       unjamming. It CROSSES locally -> magma: ridges (decompression), plumes")
L.append("       (heat), subduction (water lowers the solidus). The R19 bistable switch,")
L.append("       exactly: jammed bulk, local unjamming where the threshold is crossed.")
L.append("")
L.append("VERDICT (firewall-clean):")
L.append("  * KERNEL CONFIRMED [F]: the heavy-fluid behaviour = a HOT solid near unjamming;")
L.append("    that is WHY it flows/convects and lets the bare floor flatten (the CG-24")
L.append("    density reason). Jamming language fits: bulk jammed, near the transition.")
L.append("  * DEGREE BOUNDED [V]: it is a SOLID (S-waves), not magma; 'magma level' is off by")
L.append("    ~15-20 orders. Magma is the LOCAL unjammed state, not the bulk.")
L.append("  * the 'thin solid skin over fluid' = LITHOSPHERE over ASTHENOSPHERE (correct).")
L.append("  * rate/when stays [O] both ways.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "8c732f37e2390587831209a7e15362f8f4794acd99f8a142691f992f4fcec9c0"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
