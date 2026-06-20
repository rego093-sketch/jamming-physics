"""
organism.core — the R19 jamming-bistable substrate, transparent and in-package
===============================================================================
WHY THIS FILE EXISTS (VP-SPEC C1, and the whitepaper's stated goal):
  The DNA engine read `from organism import core` for the R19 substrate (settle /
  spinodal). When that kit is not shipped, the reproduction path breaks INSIDE the
  package -- exactly what C1 forbids ("재현 경로가 패키지 내부에서 끊기면 안 된다").
  The goal of this whitepaper is code that is 100% interpretable to the limit of
  Python, with nothing hidden. So the substrate is reconstructed here from first
  principles -- not guessed: it is validated to reproduce the frozen engine outputs
  to |dx| <= 1e-9 (run.py fidelity), and three independent constants match exactly
  (spinodal 0.5806, silenced_state -1.358, flip_age 27).

THE PHYSICS (one paragraph). The R19 master switch is the cusp (fold) normal form
  of a jammed bistable: state s relaxes down a double-well whose tilt is the drive h
  and whose width is the material scalar gamma. Gradient flow  ds/dt = -(s^3 - g*s - h),
  so equilibria solve the depressed cubic

        s^3 - g*s - h = 0.

  Its discriminant is  D = 4*g^3 - 27*h^2.  D > 0 gives three real roots (two stable
  outer + one unstable middle = bistable); D < 0 gives one real root (monostable).
  The bistable<->monostable boundary D = 0 is  h = ± (2 / (3*sqrt(3))) * g^1.5  --
  which IS the spinodal. The switch is hysteretic because, started on a branch, the
  state stays on it until that branch folds away at the spinodal, then drops.
"""
import math

# ----------------------------------------------------------------------------------
def spinodal(g):
    """Fold threshold |h_sp| = (2 / 3*sqrt(3)) * g^1.5  == the cubic's discriminant edge."""
    return (2.0 / (3.0 * math.sqrt(3.0))) * (g ** 1.5)


def _real_roots(g, h):
    """Real roots of  s^3 - g*s - h = 0  (depressed cubic, p=-g, q=-h), sorted ascending."""
    disc = 4.0 * g ** 3 - 27.0 * h ** 2          # >0: three real; <0: one real
    if disc >= 0.0:
        # three real roots (trigonometric form; handles the double-root edge at disc==0)
        # arccos argument is exactly 1 at |h| = spinodal, giving the degenerate fold
        arg = (3.0 * math.sqrt(3.0) * h) / (2.0 * g ** 1.5)
        arg = max(-1.0, min(1.0, arg))           # clamp float noise at the fold
        m = 2.0 * math.sqrt(g / 3.0)
        a = math.acos(arg) / 3.0
        roots = [m * math.cos(a - 2.0 * math.pi * k / 3.0) for k in (0, 1, 2)]
    else:
        # one real root (Cardano)
        rad = math.sqrt(h * h / 4.0 - g ** 3 / 27.0)
        cbrt = lambda x: math.copysign(abs(x) ** (1.0 / 3.0), x)
        roots = [cbrt(h / 2.0 + rad) + cbrt(h / 2.0 - rad)]
    return sorted(roots)


def settle(g, h, s_start):
    """Stable equilibrium the state relaxes to from s_start (the hysteresis rule).

    Monostable (one root): return it. Bistable (three roots r1<r2<r3; r2 unstable,
    the basin boundary): from s_start return the upper stable root r3 if s_start is on
    its side (s_start > r2), else the lower stable root r1. This makes the switch stay
    on its current branch until that branch folds away -> one-way (hysteretic) flip.
    """
    roots = _real_roots(g, h)
    if len(roots) == 1:
        return roots[0]
    r1, r2, r3 = roots
    return r3 if s_start > r2 else r1


def sdot(s, g, h):
    """Gradient flow ds/dt = -(s^3 - g*s - h)  (provided for completeness; settle is its long-time limit)."""
    return -(s ** 3 - g * s - h)


# ----------------------------------------------------------------------------------
class Gate:
    """Minimal deterministic check harness used by the engines: records each
    claim's pass/fail; all_pass() is True iff every recorded check passed.
    (Verification-only; affects stdout, never the results JSON.)"""
    def __init__(self):
        self._results = []

    def check(self, ok, claim, detail=""):
        ok = bool(ok)
        self._results.append(ok)
        print(f"    [{'PASS' if ok else 'FAIL'}] {claim}" + (f"  --  {detail}" if detail else ""))
        return ok

    def all_pass(self):
        return all(self._results)


# ----------------------------------------------------------------------------------
if __name__ == "__main__":
    # self-validation against the three independently-known engine constants
    g = 1.3153                                    # LCT human gamma (read-only)
    print(f"spinodal(g={g}) = {spinodal(g):.4f}   (engine: 0.5806)")
    # silenced state: h_eff at age~60 (m0=0.7843) is about -0.7167 -> OFF root
    print(f"settle(g, h=-0.7167, +1) = {settle(g, -0.7167, +1.0):.3f}   (engine silenced_state: -1.358)")
    # flip is at the spinodal crossing of h_eff(age); discontinuity ~ 2*sqrt(g)
    print(f"2*sqrt(g) = {2*math.sqrt(g):.3f}   (engine jump ~ 2.0)")
