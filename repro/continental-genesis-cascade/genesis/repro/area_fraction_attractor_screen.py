#!/usr/bin/env python3
"""
Continental-Genesis repro screen 18 -- the continental AREA FRACTION as a marginal-connectivity
(percolation) self-organized attractor, and its 3D-convection stress test.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19; PRESENT-TENSE geometry/dynamics; no dates; no fitted parameter.

CLAIM (CG-38): the ~40% continental fraction is NOT a number set by rates -- it is a self-organized
attractor pinned at the MARGINAL CONNECTIVITY of the COMPLEMENTARY oceanic network. Continents grow
until the ocean skin is at the edge of percolation; a fragmenting ocean throttles its own subduction
(weak return-flow) and thus its felsic production -> f is pinned near the percolation threshold,
independent of the production/destruction rate constants.

This screen carries (a) a SELF-CONTAINED deterministic percolation gate (stdlib only, SEED=19) that
reproduces the planar threshold, and (b) the graded findings of the heavier numpy/scipy simulations
shipped under repro/simulations_session/ (re-runnable; their recorded outputs are stored there).
"""
import hashlib, random

SEED = 19
random.seed(SEED)

# ===== (a) self-contained deterministic percolation: when does the OCEAN stop spanning? =====
# continent (blocked) with prob f; ocean (open)=1-f. Union-find; ocean spans top<->bottom?
def ocean_spans(N, f, seed):
    rng = random.Random(seed)
    open_ = [rng.random() > f for _ in range(N*N)]      # True = ocean
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

N = 60; trials = 20
fvals = [0.38, 0.40, 0.41, 0.42, 0.44]
span_prob = {}
for f in fvals:
    s = sum(ocean_spans(N, f, SEED + 1000*int(round(f*100)) + t) for t in range(trials))
    span_prob[f] = s/trials

L = []
L.append("AREA FRACTION -- a self-organized MARGINAL-CONNECTIVITY (percolation) attractor (CG-38)")
L.append(f"VP-SPEC  SEED={SEED}  present-tense geometry/dynamics; no dates; no fit")
L.append("="*70)
L.append("")
L.append("INSIGHT: continents are NOT the instantaneous downwelling footprint (trenches are thin lines,")
L.append("continents are broad). Felsic is buoyant and ACCUMULATES. The geometric ceiling is set by the")
L.append("OCEAN network: the skin must stay connected (ridge->trench) to keep subducting. Continents grow")
L.append("until the ocean is at the EDGE of percolation; a fragmenting ocean throttles its own subduction")
L.append("(weak return-flow) -> felsic production stalls -> f is pinned at the percolation threshold.")
L.append("This is the SAME marginal/critical signature as the c^2=B/rho substrate -- self-organized to a")
L.append("critical support, independent of the rate constants.")
L.append("")
L.append("(a) SELF-CONTAINED deterministic percolation (stdlib, SEED=19): when does the OCEAN stop spanning?")
L.append(f"    planar lattice {N}x{N}, {trials} trials/point -- continent fraction f vs P(ocean spans):")
for f in fvals:
    L.append(f"      f(continent)={f:.2f}:  P(ocean spans) = {span_prob[f]:.2f}")
L.append(f"    -> P crosses 0.5 at f* ~ 0.41 (planar site p_c ~ 0.5927 -> 1 - p_c ~ 0.407).")
L.append(f"       OBSERVED continental fraction ~ 0.41 sits on this geometric threshold.")
L.append("")
L.append("(b) SELF-ORGANIZED LOOP (numpy, repro/simulations_session/percolation_attractor.py; SEED=19):")
L.append("    felsic accretes at active (connected) ocean margins, throttled by ocean-connectivity health;")
L.append("    recycled at rate r. Scanning the production/destruction ratio over 4x (prod/dest = 8..30):")
L.append("      steady f = 0.39 - 0.41 -- a band of +/-0.01 centred on f* and on observed ~0.41,")
L.append("      FAR narrower than the 4x rate variation -> the percolation ceiling is a rate-insensitive")
L.append("      ATTRACTOR (not a rate artefact). The connectivity throttle is a PHYSICAL dependence")
L.append("      (a fragmenting ocean subducts weakly), not a tuned knob.")
L.append("")
L.append("(c) 3D-CONVECTION STRESS TEST (repro/simulations_session/: rbc3d.py + tracer; SEED=19):")
L.append("    an infinite-Pr (mantle) 3D Boussinesq solver, VALIDATED against the analytic onset")
L.append("    Ra_c = 27*pi^4/4 ~ 657.5 (single-mode growth matches linear theory to ~1e-7), produces a")
L.append("    realistic cellular surface (downwelling area fraction 0.46, ~20 cells). Driving the tracer")
L.append("    with this REAL convective surface flow:")
L.append("      - the percolation throttle still BOUNDS f and compresses the rate-dependence (attractor")
L.append("        survives in 3D);")
L.append("      - the VALUE is coupling-sensitive: static 2D = 0.39-0.41; 3D frozen-flow STIRRING = 0.24-0.32")
L.append("        (convective stirring disperses continents, lowering the ceiling).")
L.append("")
L.append("(d) TWO-WAY-COUPLED 3D run -- EXECUTED (repro/simulations_session/coupled_rbc3d.py + coupled_driver.py):")
L.append("    continent INSULATION feeds back into the buoyancy field (zero-mean = self-limiting) and the")
L.append("    convection co-evolves with the continents (which ride the large-scale flow = raft rigidity).")
L.append("    RE-VALIDATED: with C=0 the coupled solver reproduces Ra_c=657.5 exactly (coupling does not")
L.append("    corrupt it). RESULT: within the stable window the coupled fraction settles in a statistical")
L.append("    steady state around f ~ 0.30 (range ~0.27-0.36), ROBUST to the coupling strength (q=0 baseline")
L.append("    and self-limiting insulation alike). This CONFIRMS the frozen-flow lower bound and the")
L.append("    percolation mechanism; it does NOT reach the observed 0.41.")
L.append("    NUMERICAL CAVEAT: at the strongly-supercritical Ra=1e4, 64x64x12 is stable only for a finite")
L.append("    window (~7000 steps) -- EVEN THE q=0 baseline eventually blows up -- so the long-time limit is")
L.append("    the under-resolved convection, not the coupling; a fully-converged long run needs higher")
L.append("    resolution / implicit (or hyperviscous / adaptive-dt) stabilization.")
L.append("")
L.append("HONEST reading (falsification = discovery): vigorous convective stirring disperses a PASSIVE continental tracer,")
L.append("holding f near ~0.30. Real Earth's mantle is at far higher Ra (~1e6-1e7) -> stirs even MORE ->")
L.append("would push a passive tracer LOWER, not higher. So the observed 0.41 must be sustained by physics")
L.append("this passive model OMITS: continental coherence/strength resisting dispersal (a real rheology, not")
L.append("a passive scalar), felsic production CONCENTRATED at convergent margins, sphere geometry, internal")
L.append("heating. The coupled run did NOT confirm the convenient 0.41 -- it confirmed ~0.30 and SHARPENED")
L.append("the residual into a specific list of omitted, testable physics.")
L.append("")
L.append("GRADE: [L]. The percolation ATTRACTOR is now confirmed as a robust bounding mechanism (~0.25-0.41)")
L.append("across THREE independent settings -- static 2D (0.39-0.41), 3D-frozen (0.24-0.32), 3D-two-way-")
L.append("coupled (~0.30). NOT [F]: the connectivity threshold is model-dependent (planar -> 0.41; the real")
L.append("plate-network's effective connectivity giving f* ~ observed is a falsifiable prediction), and the")
L.append("coupled value (~0.30) sits BELOW observed 0.41. The decisive run is DONE; the residual is no longer")
L.append("'run the coupled case' but 'supply the omitted continental rheology + convergent-margin production")
L.append("(and a numerically-stable high-Ra long run) to test whether they lift ~0.30 to the observed 0.41.'")
L.append("")
L.append("R2 (IDENTITY) -- what VP adds: THREE present-tense observables are the SAME marginal/critical")
L.append("attractor: (1) substrate jammed at the UNJAMMING margin (c^2=B/rho); (2) freeboard pinned at the")
L.append("SEA-LEVEL margin (erosion-isostasy feedback, screen 17); (3) area pinned at the PERCOLATION")
L.append("margin (subduction-connectivity feedback, here). The convection loop itself is essentially")
L.append("mainstream; VP's distinctiveness is this marginal-criticality FOUNDATION beneath it, NOT a rival.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "bfd00bd952d9ff97ba7f4dfc09659ca05df9c5799a72919e579be6d508ca2cb0"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
