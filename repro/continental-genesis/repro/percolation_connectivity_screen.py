#!/usr/bin/env python3
"""
Continental-Genesis repro screen 22 -- CG-39 resolution: is the ceiling 0.41 a geometry-UNIVERSAL bound,
or the value for a specific connectivity? (The 'sphere geometry' candidate, made decidable.)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, NO fitted parameter; PRESENT-TENSE only; dates/duration RECORD both ways.

A full spherical convection solver is out of scope here, so 'sphere geometry' is tested where it is
actually DECIDABLE: percolation thresholds depend on the network's COORDINATION NUMBER z, and changing
geometry (square grid / triangulated sphere / hex tiling) changes z. This screen computes the continent
ceiling f* = 1 - p_c (the fraction where the OCEAN stops spanning) for z = 4, 6, 8 with one union-find,
to ask whether 0.41 is universal or the z=4 value. SEED=19, no tuning -- just the geometric thresholds.

RESULT: f* rises strongly with z -- ~0.41 (z=4) -> ~0.50 (z=6) -> ~0.61 (z=8). The observed 0.41 matches
ONLY the 4-connected case. So 0.41 is NOT a universal bound; it is the z=4 percolation threshold, and the
match to observation is a FALSIFIABLE claim about the effective connectivity of the real ocean network.
falsification = discovery -- testing geometry-robustness DOWNGRADES the certainty of the specific value 0.41.
"""
import hashlib, random

SEED = 19

def ocean_spans(N, f, seed, bonds):
    random.seed(seed)
    op = [random.random() >= f for _ in range(N*N)]
    par = list(range(N*N))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: par[ra] = rb
    for r in range(N):
        for c in range(N):
            if not op[r*N+c]: continue
            for dr, dc in bonds:
                rr, cc = r+dr, c+dc
                if 0 <= rr < N and 0 <= cc < N and op[rr*N+cc]: uni(r*N+c, rr*N+cc)
    top = {find(c) for c in range(N) if op[c]}
    bot = {find((N-1)*N+c) for c in range(N) if op[(N-1)*N+c]}
    return len(top & bot) > 0

def fstar(bonds, N=72, trials=20):
    for fi in range(30, 66):
        f = fi/100
        p = sum(ocean_spans(N, f, SEED + 1000*fi + t, bonds) for t in range(trials))/trials
        if p < 0.5:
            return f
    return None

# forward bond sets (union-find symmetrises) -> effective coordination z
BONDS = {
    "z=4  (square grid; the sim's ocean connectivity)": [(0,1),(1,0)],
    "z=6  (triangular; a geodesic-sphere tiling)":       [(0,1),(1,0),(1,1)],
    "z=8  (square + diagonals; dense connectivity)":     [(0,1),(1,0),(1,1),(1,-1)],
}

L = []
L.append("CG-39 resolution -- is the ceiling 0.41 universal, or the value for a specific connectivity?")
L.append(f"VP-SPEC  SEED={SEED}  NO fit; pure geometric percolation thresholds; present-tense")
L.append("="*78)
L.append("")
L.append("continent ceiling f* = 1 - p_c (where the OCEAN network stops spanning) vs coordination z:")
fs = {}
for name, bonds in BONDS.items():
    f = fstar(bonds); fs[name] = f
    L.append(f"    {name:48s}:  f* ~ {f:.2f}")
z4 = fs["z=4  (square grid; the sim's ocean connectivity)"]
z6 = fs["z=6  (triangular; a geodesic-sphere tiling)"]
z8 = fs["z=8  (square + diagonals; dense connectivity)"]
L.append("")
L.append(f"    -> f* RISES strongly with connectivity: {z4:.2f} (z=4) -> {z6:.2f} (z=6) -> {z8:.2f} (z=8).")
L.append("       (higher z => the ocean spans more easily => tolerates MORE continent before disconnecting.)")
L.append("")
L.append("VERDICT (falsification = discovery): the percolation ceiling is NOT a geometry-universal constant.")
L.append("  * 0.41 (planar site p_c~0.5927 -> 1-p_c~0.407) is the **z=4** value -- the 4-connected ocean the")
L.append("    simulation grid uses. The observed continental fraction ~0.41 matches ONLY this case; a")
L.append("    triangulated sphere (z=6) would put the ceiling at ~0.50, a denser network (z=8) at ~0.61.")
L.append("  * So the earlier '0.41 sits ON the percolation ceiling' holds only FOR 4-connectivity. Reaching")
L.append("    exactly 0.41 is therefore NOT a missing-convection-physics gap (sphere/heating would not")
L.append("    'close' it); it is the z=4 threshold. The stirred-box undershoot (0.34-0.38, screens 20-21)")
L.append("    sits below the z=4 ceiling because vigorous stirring + a finite box hold it there.")
L.append("  * The match to observation becomes a FALSIFIABLE empirical claim: the effective coordination of")
L.append("    the real subductable-ocean network is ~4. This is NOT obviously right -- a naive plate-adjacency")
L.append("    graph (each plate borders ~5-6 others) is z~5-6 and would predict f*~0.45-0.50, not 0.41. The")
L.append("    correct network model (continuum/grid ~4 vs plate-graph ~6) is open and decides the value.")
L.append("  GRADE [L] for 'the area fraction is a percolation bound, and that bound is z-dependent'; [O] for")
L.append("  the SPECIFIC value 0.41 (contingent on z~4, an open and falsifiable empirical question). This")
L.append("  DOWNGRADES the certainty of the value vs the v1.5 framing -- the honest direction. [O] forever on timing.")

body = "\n".join(L)
print(body)
assert z4 is not None and 0.39 <= z4 <= 0.44, f"z=4 ceiling out of band: {z4}"
assert z4 < z6 < z8, f"ceiling not monotone in z: {z4},{z6},{z8}"
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "49a92b6c3db69f8b83ea46fc67298e7283f7b049d4345fea6d121d5ba9a59f98"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
