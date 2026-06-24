#!/usr/bin/env python3
"""
Continental-Genesis repro screen 23 -- CG-39 CLOSEOUT: is the real ocean/plate network 4-connected
(-> ceiling 0.41) or ~6-connected (-> ceiling 0.50)? This decides the predicted value directly.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, NO fitted parameter; PRESENT-TENSE only; dates/duration RECORD both ways.

Screen 22 showed the percolation ceiling is connectivity-dependent (f* ~ 0.41 at z=4, ~0.50 at z=6).
This screen estimates the COORDINATION of the real plate network -- not by guessing, but by exact
topology. A sphere tiled into F plates whose boundaries meet at TRIPLE junctions (the generic, stable
case) satisfies Euler V-E+F=2 with 2E=3V, giving the mean coordination z = 6 - 12/F EXACTLY. For any
realistic plate count this is z ~ 5-6, NOT 4.

RESULT: z(F=15) = 5.2; z ranges 4.3 (F=7) to 5.8 (F=52). The natural plate network is ~6-connected
(closer to triangular than square), so the percolation ceiling it implies is f* ~ 0.46-0.50 -- which
OVERSHOOTS observed 0.41. So 0.41 is NOT uniquely forced: it sits BELOW the natural-network ceiling,
in the band where stirring holds the fraction down (screens 20-21 undershoot 0.30-0.38). The mechanism
fixes the REGIME (a sub-majority ~0.4-0.5), not the exact value. falsification = discovery. CG-39 closes at [L]/[O].
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
        if sum(ocean_spans(N, f, SEED + 1000*fi + t, bonds) for t in range(trials))/trials < 0.5:
            return f
    return None

L = []
L.append("CG-39 CLOSEOUT -- is the real plate/ocean network z=4 (-> 0.41) or z~6 (-> 0.50)?")
L.append(f"VP-SPEC  SEED={SEED}  NO fit; exact topology (Euler) + percolation calibration; present-tense")
L.append("="*78)
L.append("")
L.append("(a) EXACT topology of a plate tessellation (Euler V-E+F=2; triple junctions 2E=3V):")
L.append("    => E = 3F - 6 ; mean coordination z = 2E/F = 6 - 12/F  (F = number of plates).")
for F in [7, 12, 15, 25, 52]:
    L.append(f"      F={F:3d} plates -> z = 6 - 12/{F} = {6 - 12/F:.2f}")
L.append("    => realistic plate counts give z ~ 5-6 (z=5.2 at the ~15 commonly-cited plates), NOT 4.")
L.append("")
L.append("(b) percolation ceiling at the bracketing integer connectivities (self-contained union-find):")
f4 = fstar([(0,1),(1,0)]); f6 = fstar([(0,1),(1,0),(1,1)])
L.append(f"      z=4 (square):     f* ~ {f4:.2f}")
L.append(f"      z=6 (triangular): f* ~ {f6:.2f}")
L.append(f"    => a z~5-6 network sits between these: implied ceiling f* ~ 0.46-0.50.")
L.append("")
L.append("VERDICT (falsification = discovery): the real plate network is ~6-connected, so its percolation ceiling is")
L.append("  ~0.46-0.50 -- it OVERSHOOTS observed 0.41. Consequences, stated plainly:")
L.append("  * The answer to 'z=4 or z~6' is z~6 (exact topology). So the clean 0.41 = z=4 match of screen 22")
L.append("    is NOT the natural network's prediction; the natural network predicts a HIGHER ceiling.")
L.append("  * Observed 0.41 therefore sits BELOW the natural-network ceiling (~0.46-0.50), in the band where")
L.append("    stirring holds the fraction down (the 0.30-0.38 undershoot, screens 20-21). 0.41 is the result")
L.append("    of (connectivity ceiling ~0.46-0.50) MINUS (a stirring undershoot) -- not a single forced number.")
L.append("  * What survives is ROBUST and was the real claim all along: the continental fraction is a")
L.append("    percolation-bounded quantity in the correct REGIME -- a sub-majority ~0.4-0.5, not ~0.1 or ~0.9.")
L.append("    The mechanism (c2=B/rho -> felsic accumulates -> ocean must stay connected to subduct) fixes")
L.append("    THAT. It does NOT uniquely pin 0.41; the precise value lies in the ~0.30-0.50 model bracket.")
L.append("  GRADE: [L] for 'sub-majority percolation regime ~0.4-0.5'; [O] for the exact value 0.41 (set by")
L.append("  the connectivity-ceiling-minus-stirring interplay, within model uncertainty). CG-39 closes here:")
L.append("  the residual was chased to its floor and the honest verdict is regime-yes, exact-value-no. [O] timing forever.")

body = "\n".join(L)
print(body)
assert 4.2 < 6 - 12/7 < 4.4 and 5.7 < 6 - 12/52 < 5.8, "Euler arithmetic off"
assert f4 is not None and f6 is not None and f4 < f6 and 0.39 <= f4 <= 0.44 and 0.48 <= f6 <= 0.52, f"f* calibration off: {f4},{f6}"
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "c34e8adab1af568e45b4cbb4dfe763d7abfbdcd2c223a10b26e07ff40399025b"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
