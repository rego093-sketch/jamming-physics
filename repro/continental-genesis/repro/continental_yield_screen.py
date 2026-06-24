#!/usr/bin/env python3
"""
Continental-Genesis repro screen 21 -- CG-39 refinement: is the ~0.38->0.41 residual closed by a TRUE
finite yield strength (the v1.5 conjecture), or not?
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, NO fitted parameter; PRESENT-TENSE only; dates/duration RECORD both ways.

v1.5 (screen 20 / module 23) left the residual open and named three CANDIDATE missing ingredients:
a true yield rheology (> the cell-scale mobility proxy), sphere geometry, internal heating. This screen
TESTS the first candidate. The shipped sim simulations_session/continental_yield.py implements a real
stress-based yield: a continental block DEFORMS only where the convective strain rate exceeds yield Y;
below yield it translates RIGIDLY (block-mean velocity, edges included -- the physics the neighbour-count
mobility proxy could NOT do). Y is SCANNED to the parameter-free RIGID LIMIT (Y->inf). NO tuning.

This screen carries (a) the SELF-CONTAINED stdlib percolation ceiling f* ~ 0.407 (the bound), and (b)
the graded findings of the rheology sims. RESULT: the yield model saturates ~0.34 even fully rigid --
SHORT of 0.41. Two rheology encodings (mobility ~0.38, yield-rigid ~0.34) BOTH saturate below the
ceiling. The conjecture 'yield strength closes the gap' is FALSIFIED. falsification = discovery.
"""
import hashlib, random

SEED = 19

def ocean_spans(N, f, seed):
    random.seed(seed)
    open_ = [random.random() >= f for _ in range(N*N)]
    parent = list(range(N*N))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for r in range(N):
        for c in range(N):
            if not open_[r*N+c]: continue
            if c+1 < N and open_[r*N+c+1]: union(r*N+c, r*N+c+1)
            if r+1 < N and open_[(r+1)*N+c]: union(r*N+c, (r+1)*N+c)
    top = {find(c) for c in range(N) if open_[c]}
    bot = {find((N-1)*N+c) for c in range(N) if open_[(N-1)*N+c]}
    return len(top & bot) > 0

def span_prob(N, f, trials):
    return sum(ocean_spans(N, f, SEED + 1000*int(round(f*100)) + t) for t in range(trials))/trials

L = []
L.append("CG-39 refinement -- does a TRUE finite yield strength close the ~0.38->0.41 residual?")
L.append(f"VP-SPEC  SEED={SEED}  NO fit; yield Y SCANNED to the parameter-free RIGID LIMIT; present-tense")
L.append("="*78)
L.append("")
L.append("(a) SELF-CONTAINED deterministic percolation (stdlib): the ceiling f* (the bound to be reached):")
N = 60; trials = 24
cross = None
for f in [round(0.37+0.01*i, 2) for i in range(8)]:
    p = span_prob(N, f, trials)
    L.append(f"    continent fraction f={f:.2f}:  P(ocean spans) = {p:.2f}")
    if cross is None and p < 0.5: cross = f
L.append(f"    -> ceiling f* ~ 0.41 (planar site p_c ~ 0.5927 -> 1 - p_c ~ 0.407). This is the target.")
L.append("")
L.append("(b) SHIPPED SIM -- continental_yield.py (real stress-based yield; f vs Y/Srms, 3 seeds):")
L.append("    a block deforms only where strain rate > Y; below yield it translates RIGIDLY (edges too).")
L.append("       Y/Srms:    0.0   0.25   0.5   1.0   2.0   4.0   inf(rigid)")
L.append("       uniform:   0.29  0.30   0.25  0.32  0.34  0.34   0.34")
L.append("       converg:   0.00  0.00   0.00  0.24  0.33  0.33   0.33")
L.append("    -> rising Y lifts f but it SATURATES ~0.34 (uniform) / ~0.33 (convergent) and STAYS there")
L.append("       to the RIGID LIMIT. Making continents perfectly rigid does NOT reach the ceiling: rigid")
L.append("       blocks are still ADVECTED into the downwelling pattern, throttling accretion below 0.41.")
L.append("")
L.append("(c) CROSS-REF -- the other rheology encoding (screen 20 / continental_rheology.py):")
L.append("    the cell-scale mobility proxy saturates ~0.38 (uniform). So TWO independent rheology")
L.append("    encodings -- mobility ~0.38 AND stress-yield (rigid) ~0.34 -- BOTH saturate SHORT of 0.41.")
L.append("")
L.append("VERDICT (falsification = discovery): the v1.5 conjecture 'a true yield rheology closes ~0.38->0.41' is FALSIFIED.")
L.append("  * Continental rheology is a CONFIRMED partial lever (lifts the stirred 0.29-0.30 to 0.34-0.38),")
L.append("    but it is NOT sufficient -- neither encoding reaches the percolation ceiling from below.")
L.append("  * The percolation ceiling ~0.41 remains the binding upper bound (coherence cannot exceed it,")
L.append("    screen 20; rheology cannot attain it from below, here). Observed 0.41 sits ON that ceiling.")
L.append("  * The residual is therefore NOT rheology. It points to the two UNtested candidates -- sphere")
L.append("    geometry (a closed surface, no periodic-box stirring artifacts) and internal heating")
L.append("    (narrower downwellings) -- OR the planar ceiling 0.407 IS the bound and a flat stirred box")
L.append("    only approaches it from below while the real spherical, internally-heated Earth sits at it.")
L.append("  GRADE [O] for closure (reopened: the named closer was tested and failed); [L] for the bound")
L.append("  and for rheology-as-partial-lever. NO fitted parameter (Y scanned, rigid limit is parameter-")
L.append("  free). A prior conjecture of THIS package was tested and rejected. Occurrence/timing [O] forever.")

body = "\n".join(L)
print(body)
assert cross is not None and 0.39 <= cross <= 0.43, f"ceiling crossing out of band: {cross}"
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "a4683e2f573fdba56293d34cbb3618674584274dc6baa0442a9adea15c31ede9"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
