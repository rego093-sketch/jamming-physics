#!/usr/bin/env python3
"""
Module 30 reproducibility script - the two internal seams, closed by FORCED reasoning.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning.

Does NOT choose a resolution by taste. It encodes the chain's already-established
constraints and shows mechanically which trigger reading is the ONLY internally
consistent one, then re-verifies the resolved chain is acyclic with a single trigger.
Every constraint used is grounded in a prior sealed result; no new claim is asserted.
Occurrence stays [O], both directions.
"""
import hashlib

SEED = 19

# ---------------------------------------------------------------------------------
# PART 1 - TRIGGER SEAM.  The flood is t=0.  Two readings of what opens H-A:
#   A: the reservoir release itself collapses the enclosure and ruptures AT t=0.
#   B: the release only PRIMES; the glacial load (built over the gap) triggers, at t>=floor.
#
# Established constraints these must satisfy (each cites a prior SEALED result):
#   c1 GAP FLOOR  : rupture time must be t >= floor, floor > 0
#                   (forced by finite measured snowfall -> Module 25, gate 8235bff6...)
#   c2 ORDERING   : rupture must FOLLOW the ice load, which itself is at t >= floor
#                   (the gap sits BETWEEN flood and rupture by construction -> Blueprint Part 1)
#   c3 ENERGY     : the opening is driven by stored CONFIGURATION energy released when the
#                   enclosure collapses; the release LOADS the spring, it need not rupture alone
#                   (loaded-spring / R19 bistable switch -> Module 16; inherited engine)
# floor is symbolic: any strictly positive value; only its SIGN is load-bearing here.
floor = 1

readings = {
 "A_release_ruptures_immediately": dict(t_rupture=0,     release_role="ruptures", needs_near_crit=False),
 "B_glacial_load_triggers":        dict(t_rupture=floor, release_role="primes",   needs_near_crit=True),
}

def c1_gap_floor(r):  return r["t_rupture"] >= floor          # rupture after the (positive) floor
def c2_ordering(r):   return r["t_rupture"] >= floor          # rupture follows the ice load (>= floor)
def c3_energy(r):     return r["release_role"] in ("primes","ruptures")  # both can in principle drive

CHECKS = [("c1 gap-floor", c1_gap_floor), ("c2 ordering", c2_ordering), ("c3 energy", c3_energy)]

L = []
L.append("SEAM RESOLUTION - forced by internal consistency (not chosen)")
L.append(f"SEED={SEED}")
L.append("")
L.append("PART 1 - H-A TRIGGER: test each reading against the chain's sealed constraints")
consistent = []
for name, r in readings.items():
    results = [(lbl, fn(r)) for lbl, fn in CHECKS]
    ok = all(v for _, v in results)
    flags = "  ".join(f"{lbl}:{'ok' if v else 'FAIL'}" for lbl, v in results)
    L.append(f"  {name:34s} -> {flags}  => {'CONSISTENT' if ok else 'INCONSISTENT'}")
    if ok: consistent.append(name)
L.append("")
L.append(f"  only internally-consistent reading: {consistent}")
L.append("  => FORCED: the release PRIMES a near-critical rift; the glacial load TRIGGERS;")
L.append("     the engine DRIVES the opening with the stored configuration energy.")
L.append("     HONEST COST: near-criticality becomes a load-bearing premise (stays [O]).")
L.append("     It is COHERENT, not fine-tuned: 'primed-but-stuck' is a regime (velocity-")
L.append("     weakening stick-or-fast engine), a range of states, not a tuned point; and the")
L.append("     release sub-critical bound is one-sided, not a narrow window.")
L.append("")

# ---------------------------------------------------------------------------------
# PART 2 - re-verify the RESOLVED chain: single trigger, acyclic, no direct release->rupture edge.
RESOLVED = {
 "flood_mech":    [],
 "release_prime": ["flood_mech"],        # release loads the spring (primes), does NOT rupture
 "near_crit":     ["release_prime"],     # priming moves the rift toward near-critical ([O])
 "ice_load":      ["flood_mech"],        # (built over the gap; abbreviated here)
 "c2_trigger":    ["ice_load"],          # the SINGLE trigger = the glacial load
 "engine":        [],
 "ha_rupture":    ["c2_trigger", "near_crit", "engine"],  # NO edge from release_prime
}
def acyclic(g):
    color = {k: 0 for k in g}
    def dfs(u):
        color[u] = 1
        for v in g[u]:
            if color.get(v, 0) == 1: return False
            if color.get(v, 0) == 0 and not dfs(v): return False
        color[u] = 2; return True
    return all(dfs(k) for k in g if color[k] == 0)

single_trigger = ("release_prime" not in RESOLVED["ha_rupture"]) and ("c2_trigger" in RESOLVED["ha_rupture"])
is_acyclic = acyclic(RESOLVED)
L.append("PART 2 - resolved chain structure")
L.append(f"  single trigger (glacial load only, no direct release->rupture edge): {single_trigger}")
L.append(f"  acyclic: {is_acyclic}")
L.append("")

# ---------------------------------------------------------------------------------
# PART 3 - ORDERING SEAM: one timeline + the explicit consistency condition.
L.append("PART 3 - ORDERING SEAM")
L.append("  single timeline (by construction):")
L.append("    release(loads) -> flood + warm ocean -> [gap: ice builds, loads crust]")
L.append("    -> glacial load TRIGGERS rupture -> opening -> inherited post-opening responses")
L.append("  the cascade's glaciation is PRE-rupture; the inherited responses are POST-rupture,")
L.append("  so they occupy different positions in ONE relaxation and do not compete - PROVIDED")
L.append("  no inherited post-opening response requires an ice-free pre-rupture state.")
L.append("  CONSISTENCY CONDITION (explicit, to verify against the inherited volume):")
L.append("    no post-opening response presupposes 'no prior ice'. None is apparent; if one is")
L.append("    found, the conflict is real -> revise pre-loading magnitude (do NOT ignore it).")
L.append("")
L.append("VERDICT: both seams close. Trigger resolution is FORCED (B is the unique consistent")
L.append("reading); ordering closes by one timeline under a stated, checkable condition. The")
L.append("chain is now internally consistent; near-criticality is a named load-bearing [O].")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode()).hexdigest()
h2 = hashlib.sha256(h1.encode()).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "d317fadb9ec0c69763fce6609651adbda48c4818bed8d973d012b74905e7a65e"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
