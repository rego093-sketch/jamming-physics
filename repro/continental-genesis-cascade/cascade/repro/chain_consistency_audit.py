#!/usr/bin/env python3
"""
Module 29 reproducibility script - Whole-chain causal CONSISTENCY audit.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning.

Encodes the cascade as a dependency graph (each claim, its grade, what it rests on)
and mechanically checks INTERNAL CONSISTENCY:
  1. the graph is acyclic (no circular reasoning),
  2. which load-bearing [F]/[V] claims are UNCONDITIONAL (rest on nothing open) = the
     genuinely solid backbone, vs CONDITIONAL (secretly rest on an open premise),
  3. which open [O] premises the whole load-bearing chain converges on (ranked) = the
     real weak links,
  4. the unreconciled internal seams that must be closed.
No physics, no dates; this audits the SCAFFOLDING only. Occurrence stays [O].
"""
import hashlib

SEED = 19

# grade: F forced/permitted, V verified present-tense, L leaning, O open/held
# node : (grade, [dependencies], description)
NODES = {
 "substrate"      : ("V", [], "high-pressure water / ice-VII exists"),
 "budget"         : ("O", [], "reservoir large + releasable enough (the budget root)"),
 "flood_mech"     : ("F", [], "gateway-gated catastrophic flood permitted; Nile signature"),
 "flood_occ"      : ("O", [], "the specific Flood occurred (capped)"),
 "ocean_heat"     : ("O", ["budget"], "reservoir release supplies the ocean warming"),
 "warm_ocean"     : ("L", ["flood_mech","ocean_heat"], "warm ocean exists as snow-engine fuel"),
 "snow_rate"      : ("V", [], "maritime snowfall rate measured"),
 "cold_sky"       : ("O", [], "dust-laden cold high-albedo atmosphere (premise)"),
 "c1_rate"        : ("F", ["warm_ocean","snow_rate"], "warm ocean + cold sky builds ice fast"),
 "c1_spatial"     : ("O", ["c1_rate"], "moisture reaches the continent interior"),
 "c1_netaccum"    : ("O", ["c1_rate","cold_sky"], "net accumulation survives under a warm ocean"),
 "gap_floor"      : ("F", ["c1_rate"], "non-immediacy: gap > 0 entailed by finite snow rate"),
 "gap_ceiling"    : ("O", ["budget"], "fuel ceiling finite but number open"),
 "gap_joint"      : ("O", ["budget"], "one budget funds BOTH fuel and trigger load"),
 "glaciation"     : ("L", ["c1_rate","c1_spatial","c1_netaccum"], "rapid continental glaciation"),
 "ice_load"       : ("F", ["glaciation","gap_floor"], "trigger-sufficient ice load by the floor"),
 "c2_trigger"     : ("F", ["ice_load"], "glacial loading triggers rupture; faulting observed"),
 "near_crit"      : ("O", [], "the specific rift was near-critical when loaded"),
 "c2_scaling"     : ("O", ["c2_trigger"], "the small-fault trigger scales to continental rift"),
 "cont_scale"     : ("O", [], "continental-scale extrapolation of the engine (master HOLD)"),
 "engine"         : ("F", [], "void-suction + unjamming engine (inherited, lab-scale reproduced)"),
 "ha_rupture"     : ("L", ["c2_trigger","near_crit","c2_scaling","engine","cont_scale"], "accelerated Atlantic opening"),
 "ha_occ"         : ("O", [], "the rupture occurred (capped)"),
 "termination"    : ("F", ["ha_rupture"], "build/melt asymmetry -> rapid melt (latent heats)"),
 "oil_cracking"   : ("V", [], "light oil is present-tense metastable (cracking clock)"),
 "source_forced"  : ("F", [], "rich source rock forces three coincident conditions"),
 "source_overmat" : ("O", [], "local source over-mature (closure, to measure)"),
 "oil_disc"       : ("O", ["oil_cracking","source_overmat"], "cracking discriminates deep-time vs recent"),
 "source_catas"   : ("O", ["source_forced"], "those conditions REQUIRE a catastrophe (too strong)"),
 "source_econ"    : ("L", ["source_forced","flood_mech","ocean_heat","engine"], "one event supplies all three (strongest card)"),
 "petro_location" : ("L", ["source_econ"], "petroleum discovery location co-locates with cascade signature"),
}

# Unreconciled internal seams (must be closed by reasoning; no data needed):
SEAMS = [
 "TRIGGER: H-A trigger is doubly specified - immediate void-collapse vs delayed glacial load",
 "ORDERING: glaciation-before-opening vs the inherited volume's post-opening responses",
]

def ancestors(n, seen=None):
    if seen is None: seen=set()
    for d in NODES[n][1]:
        if d not in seen:
            seen.add(d); ancestors(d, seen)
    return seen

# 1) acyclicity (DFS)
def has_cycle():
    WHITE,GREY,BLACK=0,1,2
    color={k:WHITE for k in NODES}
    bad=[]
    def dfs(u):
        color[u]=GREY
        for v in NODES[u][1]:
            if color[v]==GREY: bad.append((u,v)); return True
            if color[v]==WHITE and dfs(v): return True
        color[u]=BLACK; return False
    for k in NODES:
        if color[k]==WHITE: dfs(k)
    return bad

cyc = has_cycle()

# 2) classify load-bearing nodes
solid, conditional = [], []
for n,(g,deps,desc) in NODES.items():
    if g in ("F","V"):
        opens = sorted(a for a in ancestors(n) if NODES[a][0]=="O")
        if not opens: solid.append(n)
        else: conditional.append((n, opens))
    elif g=="L":
        opens = sorted(a for a in ancestors(n) if NODES[a][0]=="O")
        conditional.append((n, opens))

# 3) rank open premises by how many load-bearing claims rest on them
load_bearing = [n for n,(g,_,_) in NODES.items() if g in ("F","V","L")]
dep_count = {}
for n in load_bearing:
    for a in ancestors(n):
        if NODES[a][0]=="O":
            dep_count[a]=dep_count.get(a,0)+1
ranked = sorted(dep_count.items(), key=lambda x:(-x[1], x[0]))

L=[]
L.append("WHOLE-CHAIN CAUSAL CONSISTENCY AUDIT  (scaffolding only; no physics, no dates)")
L.append(f"SEED={SEED}   nodes={len(NODES)}   load-bearing={len(load_bearing)}")
L.append("")
L.append(f"[1] ACYCLIC (no circular reasoning): {'YES' if not cyc else 'NO -> '+str(cyc)}")
L.append("")
L.append("[2] UNCONDITIONAL solid backbone ([F]/[V], rest on nothing open):")
for n in sorted(solid):
    L.append(f"      + {n:14s} {NODES[n][2]}")
L.append("")
L.append("[3] LOAD-BEARING OPEN PREMISES the chain converges on (ranked by dependents):")
for a,c in ranked:
    L.append(f"      ! {a:14s} (carries {c:2d} load-bearing claims)  {NODES[a][2]}")
L.append("")
L.append("[4] CONDITIONAL claims (strong only IF their open premises hold):")
for n,opens in sorted(conditional):
    L.append(f"      ~ {n:14s} <= {', '.join(opens) if opens else '(none)'}")
L.append("")
L.append("[5] UNRECONCILED INTERNAL SEAMS (must be closed; reasoning, no data):")
for s in SEAMS:
    L.append(f"      X {s}")
L.append("")
L.append("READING: the scaffolding is acyclic (no circular reasoning). The solid backbone")
L.append("stands unconditionally. Everything else is CONDITIONAL on a few open premises that")
L.append("the chain converges on - leave them [O], do not force them. Two internal seams")
L.append("remain and MUST be closed for internal consistency. Occurrence stays [O], both ways.")

body="\n".join(L)
print(body)
h1=hashlib.sha256(body.encode()).hexdigest()
h2=hashlib.sha256(h1.encode()).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT="31e359621859fcce08b26e8701d6e57b1650df509066ae869bfef2b79ad96c35"
assert h2==EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
