#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_exact_sqrt.py
VP Theory — exact sqrt(1 - v^2/c^2) for the rotation-emission clock, from medium mechanics.

NO RELATIVITY is used (no Lorentz invariance, no spacetime geometry). NO light-clock across D.
Only: (i) signals propagate in the medium at the elastic-wave speed c (the framework's c = sqrt(K/rho)),
      (ii) the electron rate nu_e (hence mass m_e = 2*pi*nu_e) is ISOTROPIC (framework calibration node).

Mechanism ("Michelson-for-winding"):
  A winding is a signal that must CLOSE a loop at speed c. For a moving excitation whose longitudinal
  scale is contracted by factor kappa, the round-trip closure time of an arm of proper length L at
  rest-angle theta to the velocity is (derived analytically, medium rest frame):

      T(theta; kappa, v) = 2L * sqrt( kappa^2 c^2 cos^2(theta) + (c^2 - v^2) sin^2(theta) ) / (c^2 - v^2)

  T is theta-INDEPENDENT  <=>  kappa^2 c^2 = c^2 - v^2  <=>  kappa = sqrt(1 - v^2/c^2).
  At that unique kappa:  T = (2L/c)/sqrt(1 - v^2/c^2)  =>  rate = T0/T = sqrt(1 - v^2/c^2), all orientations.

  => Demanding the rate be isotropic FORCES kappa = sqrt(1-v^2/c^2), and the rate is then EXACTLY
     sqrt(1-v^2/c^2) to all orders. The leading expansion is 1 - v^2/2c^2 (matches the handoff [F]).

Grades:
  [F]  finite-c closure (medium signal at c)            -> orientation-dependent unless contracted
  [F]  rate isotropy (m_e isotropic; m = 2*pi*nu)       -> requirement
  [F]  => kappa = sqrt(1-v^2/c^2) UNIQUE (this module)  -> value of the exact factor is forced
  [O]  ab-initio dynamical realization of the contraction in the full transverse/vector sector
       (Heaviside/Searle ellipsoid) = section 14.0.6 exact-v/c open item. VALUE forced; full
       dynamical derivation open.

Deterministic, standard-library only (math). 2x sha256 identical.
"""

import math
import hashlib
import io
import csv

C = 1.0   # work in units c = 1 (dimensionless); v is then v/c. Pure geometry, no physical scale.
L = 1.0   # proper arm length (cancels in rate ratios)

def T_roundtrip(theta, kappa, v):
    """Closure round-trip time for an arm of proper length L at rest-angle theta, moving at v,
    longitudinally contracted by kappa. Analytic medium-frame result (see header)."""
    num = math.sqrt(kappa**2 * C**2 * math.cos(theta)**2 + (C**2 - v**2) * math.sin(theta)**2)
    return 2.0 * L * num / (C**2 - v**2)

def T_rest():
    return 2.0 * L / C

def anisotropy(kappa, v, n=720):
    """max_theta T - min_theta T over a full orientation sweep (the 'fringe shift')."""
    vals = [T_roundtrip(math.pi * k / n, kappa, v) for k in range(n + 1)]
    return max(vals) - min(vals)

def best_kappa_numeric(v, lo=1e-9, hi=1.0, iters=200):
    """Golden-section minimize anisotropy(kappa) over kappa -> the contraction the medium must adopt.
    Found numerically (NOT assumed) so we can compare the minimizer to sqrt(1-v^2/c^2)."""
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c1 = b - gr * (b - a)
    c2 = a + gr * (b - a)
    f1, f2 = anisotropy(c1, v), anisotropy(c2, v)
    for _ in range(iters):
        if f1 < f2:
            b, c2, f2 = c2, c1, f1
            c1 = b - gr * (b - a)
            f1 = anisotropy(c1, v)
        else:
            a, c1, f1 = c1, c2, f2
            c2 = a + gr * (b - a)
            f2 = anisotropy(c2, v)
    return (a + b) / 2

def rate_at(kappa, v):
    """Orientation-averaged rate T_rest / <T>(theta); at kappa=sqrt(1-v^2/c^2) it is theta-exact."""
    n = 720
    vals = [T_roundtrip(math.pi * k / n, kappa, v) for k in range(n + 1)]
    Tmean = sum(vals) / len(vals)
    return T_rest() / Tmean

# ----------------------------------------------------------------------------
def scan():
    rows = []
    for v in (0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99):
        kappa_forced = math.sqrt(1.0 - v**2 / C**2)     # the claim
        kappa_found = best_kappa_numeric(v)             # numerically minimize anisotropy
        aniso_at_forced = anisotropy(kappa_forced, v)   # should be ~0
        aniso_no_contraction = anisotropy(1.0, v)       # kappa=1 (no contraction): residual fringe
        # rate at the forced kappa, and the exact target:
        rate_forced = rate_at(kappa_forced, v)
        sqrt_exact = math.sqrt(1.0 - v**2 / C**2)
        lead = 1.0 - 0.5 * v**2 / C**2
        rows.append((v, kappa_forced, kappa_found, abs(kappa_found - kappa_forced),
                     aniso_at_forced, aniso_no_contraction, rate_forced, sqrt_exact, lead))
    return rows

def build_csv(rows):
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
    w.writerow(["# VP exact-sqrt derivation: Michelson-for-winding (deterministic, c=1 units)"])
    w.writerow(["# T(theta;kappa,v)=2L*sqrt(kappa^2 cos^2 + (1-v^2) sin^2)/(1-v^2); isotropy=>kappa=sqrt(1-v^2)"])
    w.writerow([])
    w.writerow(["v_over_c", "kappa_forced=sqrt(1-v^2)", "kappa_found_numeric", "abs_diff",
                "anisotropy@forced", "anisotropy@no_contraction", "rate@forced",
                "sqrt_exact", "leading_1-v^2/2", "grade"])
    for (v, kf, kn, d, a0, anc, rf, se, ld) in rows:
        w.writerow([("%.3f" % v), ("%.12f" % kf), ("%.12f" % kn), ("%.2e" % d),
                    ("%.2e" % a0), ("%.4e" % anc), ("%.12f" % rf), ("%.12f" % se), ("%.12f" % ld),
                    "[F]"])
    return buf.getvalue()

def selftest():
    for v in (0.01, 0.1, 0.3, 0.6, 0.9, 0.99):
        kf = math.sqrt(1.0 - v**2)
        # 1) anisotropy is (machine) zero at kappa = sqrt(1-v^2)
        assert anisotropy(kf, v) < 1e-12, "anisotropy not zero at sqrt(1-v^2): v=%.3f" % v
        # 2) the numerically-found minimizer equals sqrt(1-v^2)
        kn = best_kappa_numeric(v)
        assert abs(kn - kf) < 1e-6, "found kappa != sqrt(1-v^2): v=%.3f (%.8f vs %.8f)" % (v, kn, kf)
        # 3) at the forced kappa the rate is EXACTLY sqrt(1-v^2) (orientation-independent)
        assert abs(rate_at(kf, v) - kf) < 1e-9, "rate != sqrt(1-v^2) at forced kappa: v=%.3f" % v
        # 4) WITHOUT contraction (kappa=1) there is residual anisotropy (proves contraction is needed)
        assert anisotropy(1.0, v) > 1e-6, "no residual anisotropy without contraction: v=%.3f" % v
        # 5) leading expansion matches 1 - v^2/2 to O(v^4)
        assert abs(kf - (1 - 0.5 * v**2)) < v**4, "leading expansion mismatch: v=%.3f" % v
    return True

def main():
    assert selftest(), "selftest failed"
    rows = scan()
    csv_text = build_csv(rows)
    h1 = hashlib.sha256(csv_text.encode()).hexdigest()
    h2 = hashlib.sha256(build_csv(scan()).encode()).hexdigest()
    assert h1 == h2, "non-deterministic"
    with open("EXACT_SQRT_LEDGER.csv", "w", encoding="utf-8") as fh:
        fh.write(csv_text)

    print("=" * 84)
    print("VP EXACT sqrt(1 - v^2/c^2)  —  rotation-emission clock, medium mechanics (no relativity)")
    print("=" * 84)
    print("Claim: finite-c closure + rate isotropy  =>  contraction kappa = sqrt(1-v^2/c^2) UNIQUE,")
    print("       and the rate is then EXACTLY sqrt(1-v^2/c^2) for every winding orientation.")
    print()
    print(" v/c   kappa=sqrt(1-v^2)   kappa_found(min aniso)   aniso@forced   aniso@no-contract   rate@forced=sqrt?")
    for (v, kf, kn, d, a0, anc, rf, se, ld) in rows:
        ok = "YES" if abs(rf - se) < 1e-9 else "no"
        print("  %-5.3f %-18.12f %-22.12f %-13.2e %-18.4e %s (%.12f)"
              % (v, kf, kn, a0, anc, ok, rf))
    print()
    print("Reading the columns:")
    print("  * kappa_found (numerically minimizing the orientation 'fringe') == sqrt(1-v^2/c^2):")
    print("    the contraction is NOT assumed; it is the unique minimizer, recovered to ~1e-6.")
    print("  * aniso@no-contraction (kappa=1) is NONZERO: without contraction the rate is anisotropic")
    print("    (= a Michelson-Morley fringe for the winding) -> contraction is REQUIRED.")
    print("  * rate@forced == sqrt(1-v^2/c^2) exactly (all orders); leading term 1 - v^2/2c^2 [F].")
    print()
    print("=> The exact factor's VALUE is FORCED by (finite-c closure) + (electron-rate isotropy).")
    print("   Remaining [O]: ab-initio dynamical realization of the contraction in the full")
    print("   transverse/vector sector (Heaviside/Searle ellipsoid) = section 14.0.6.")
    print("   Via the river identity, this also fixes gravitational dilation sqrt(1-2GM/rc^2) exactly.")
    print()
    print("No-Tuning: no coefficient migrated. ledger sha256 = %s" % h1)
    print("wrote: EXACT_SQRT_LEDGER.csv")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
