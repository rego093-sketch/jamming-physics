#!/usr/bin/env python3
"""
gap_window.py -- VP Recent-Sequence Cascade, Module 25.
Bounded flood -> rift GAP-WINDOW screen.

This is a PHYSICAL-PERMISSION screen (same kind as the C1/C2 no-go screens,
Modules 13-14). The ONLY permitted conclusions are "not forbidden [F]" or
"forbidden". Occurrence and absolute chronology are [O], firewalled in BOTH
directions (Constitution Art. 2, Art. 4; Blueprint Part 2 Tier-B).

WHAT IS FIXED (author):
  FLOOR = 100 yr   -- the firm, load-bearing floor: H-A (Atlantic expansion)
                      begins AT LEAST 100 yr after H-F (flood); NOT immediate.

WHAT IS DERIVED (Tier-A D0/D1 constants only -- identical to Blueprint v2
Part 2 ledger; nothing fitted):
  - non-immediacy is ENTAILED, not assumed (finite snowfall forbids instant load)
  - the load that FLOOR + the snow engine mechanically guarantees by 100 yr
  - the gap<->load CO-CONSTRAINT (one snow engine; one flood budget)

WHAT IS WITHHELD ([O]):
  - the CEILING tau_fuel = Q_flood / (acc * rho_w * L_vap). It is FINITE (this is
    what keeps the chain ONE relaxation, Blueprint Part 1), but its NUMBER
    inherits SH-5 (flood budget) = [O]. Reported symbolically, never as a number.
  - "2300 BC / 2200 BC", and the statement that the gap *took* any wall-clock
    value: absolute chronology = D5 = RECORD, forbidden as load-bearing both ways.

LOCK (changing any constant below defines a NEW version):
  rho_ice = 917    kg/m^3        (D0)
  g       = 9.81   m/s^2         (D0)
  rho_w   = 1000   kg/m^3        (D0)
  L_vap   = 2.50e6 J/kg          (D0)
  acc     = [1.0, 4.0] m w.e./yr (D0/D1 observed maritime snowfall band)
SEED = 19 convention. Determinism is proven by a double-SHA-256 self-gate.
"""
import hashlib

SEED = 19  # convention; computation is deterministic, no RNG used

# ---- LOCK: Tier-A D0/D1 constants ------------------------------------------
RHO_ICE = 917.0
G       = 9.81
RHO_W   = 1000.0
L_VAP   = 2.50e6
ACC     = (1.0, 4.0)            # m water-equivalent / yr (observed band)
FLOOR   = 100.0                 # yr, author-fixed firm floor
SEC_PER_YR = 3.15e7
WE_PER_ICE = RHO_ICE / RHO_W    # ice thickness -> water-equivalent (= 0.917)

# ---- elementary, derivation-only relations ---------------------------------
def ice_from_we(we):                       # m w.e. -> m ice
    return we / WE_PER_ICE

def stress_MPa(h_ice):                      # m ice -> basal load (MPa)
    return RHO_ICE * G * h_ice / 1e6

def gap_for_stress(sigma_MPa, acc):         # min gap (yr) to reach sigma at acc
    h_ice = sigma_MPa * 1e6 / (RHO_ICE * G)
    we = h_ice * WE_PER_ICE
    return we / acc

def load_at_gap(gap, acc):                  # (m ice, MPa) accumulated in gap yr
    we = acc * gap
    h = ice_from_we(we)
    return h, stress_MPa(h)

def latent_flux(acc):                       # W/m^2 latent heat extracted by engine
    return acc / SEC_PER_YR * RHO_W * L_VAP

# co-constraint coefficient: sigma_MPa = K * acc * tau
K_COCON = RHO_ICE * G / (WE_PER_ICE * 1e6)  # ~ 9.81e-3

def f3(x):  return f"{x:.3f}"

def ledger():
    L = []
    L.append(f"MODULE=25 SEED={SEED}")
    L.append(f"LOCK rho_ice={f3(RHO_ICE)} g={f3(G)} rho_w={f3(RHO_W)} "
             f"L_vap={L_VAP:.3e} acc={ACC} floor={f3(FLOOR)}")
    # (1) non-immediacy ENTAILED: min gap to reach each trigger stress
    for s in (1.0, 4.0, 9.0, 27.0):
        for a in ACC:
            L.append(f"MINGAP sigma_MPa={f3(s)} acc={f3(a)} gap_yr={f3(gap_for_stress(s, a))}")
    # (2) load that FLOOR + engine guarantees
    for a in ACC:
        h, s = load_at_gap(FLOOR, a)
        L.append(f"FLOOR_LOAD acc={f3(a)} ice_m={f3(h)} sigma_MPa={f3(s)}")
    # (3) full ice-age load gap requirement
    for H in (1000.0, 3000.0):
        we = H * WE_PER_ICE
        L.append(f"FULLLOAD ice_m={f3(H)} sigma_MPa={f3(stress_MPa(H))} "
                 f"gap_lo_yr={f3(we/ACC[1])} gap_hi_yr={f3(we/ACC[0])}")
    # (4) co-constraint coefficient (one snow engine)
    L.append(f"COCONSTRAINT sigma_MPa=K*acc*tau K={K_COCON:.4e}")
    # (5) latent heat extraction flux (one flood budget funds duration AND load)
    for a in ACC:
        L.append(f"LATENT_FLUX acc={f3(a)} W_m2={f3(latent_flux(a))}")
    # (6) ceiling: symbolic only -- number inherits SH-5 = [O]
    L.append("CEILING tau_fuel=Q_flood/(acc*rho_w*L_vap) Q_flood=SH-5=[O] number_withheld")
    return "\n".join(L)

def double_sha256(s):
    return hashlib.sha256(hashlib.sha256(s.encode("utf-8")).digest()).hexdigest()

# Frozen reproducibility gate (double SHA-256 of the ledger body):
EXPECTED_2XSHA256 = "8235bff6fa934b4e4910aac1cf56aa54112a16fed71f0cd2faf9918da3cb6058"

if __name__ == "__main__":
    body = ledger()
    print(body)
    digest = double_sha256(body)
    print("\n2xSHA256 = " + digest)
    if EXPECTED_2XSHA256 != "__PENDING__":
        assert digest == EXPECTED_2XSHA256, (
            "REPRO GATE FAILED:\n  got      " + digest +
            "\n  expected " + EXPECTED_2XSHA256)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED_2XSHA256 to the value above)")
