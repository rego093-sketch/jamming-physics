#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_timegravity_ssot.py
VP Theory — Time & Gravity canonical numeric ledger (SSOT) + drift gate.

Deterministic, standard-library only (math/re/csv/hashlib). 2x sha256 identical.
No-Tuning: no coefficient is migrated to close any residual.

Verifies / records:
  G-RIVER   : river kinematic factor sqrt(1 - v_river^2/c^2) == exact Schwarzschild
              sqrt(1 - 2GM/rc^2), as an algebraic identity (v_river = escape velocity).
  LEADING   : motion 1 - v^2/2c^2 ; gravity 1 + phi_N/c^2 ; combined.
  TWO-V     : mass-current v ~ 1/r^2 (bookkeeping)  vs  river v ~ 1/sqrt(r) (potential).
  REL-MATCH : O(c^-2) identical to the GPS combined expression; O(c^-4) departure shown.

Grades: [F] forced ; [F?] structural (exact form conditional on the open exact-sqrt) ;
        [O] open (absolute magnitude = m_q scalar, four-wall; exact sqrt = section 14.0.6).

Usage:
  python3 vp_timegravity_ssot.py                 # ledger + gates + CSV
  python3 vp_timegravity_ssot.py --check FILE...  # drift gate over text files (exit 1 on drift)
"""

import math
import sys
import re
import csv
import io
import hashlib

# ----------------------------------------------------------------------------
# Canonical inputs (canon_lock / standard).  Absolute G-magnitude is [O] (m_q class).
# ----------------------------------------------------------------------------
C = 299792458.0            # m/s, exact SI
G = 6.67430e-11            # used for shapes/ratios; its magnitude is the [O] m_q scalar

# Test bodies (NASA): name -> (M [kg], R [m]).  NeutronStar probes the cap regime.
BODIES = {
    "Moon":        (7.342e22,        1.7374e6),
    "Earth":       (5.9722e24,       6.371e6),
    "Sun":         (1.989e30,        6.963e8),
    "WhiteDwarf":  (1.0 * 1.989e30,  7.0e6),
    "NeutronStar": (1.4 * 1.989e30,  1.2e4),
}

# Framework canon rates (referenced, never re-derived here).
NU_E  = 1.0                      # electron canonical event rate, eq phy-12-014   [F]
NU_P  = 3.0 * math.pi**4         # proton grind rate, LOCK-NU-N (n-fold law)       [F]
MP_ME = 6.0 * math.pi**5         # = 2*pi*NU_P  (mass-rate identity m = 2*pi*nu)   [F]

# ----------------------------------------------------------------------------
# Field quantities (all from the single potential phi_N).
# ----------------------------------------------------------------------------
def phi_N(M, R):                 # Newtonian potential (negative)              [F form]
    return -G * M / R

def v_river(M, R):               # river = free-fall/escape velocity = sqrt(-2 phi_N) [F form]
    return math.sqrt(2.0 * G * M / R)

def v_masscurrent(M, R, r):      # incompressible mass-current shape ~ 1/r^2 (DISTINCT bookkeeping)
    return v_river(M, R) * (R / r) ** 2

# Time-dilation factors -------------------------------------------------------
def f_grav_leading(M, R):        # 1 + phi_N/c^2                                [F leading]
    return 1.0 + phi_N(M, R) / C**2

def f_grav_river(M, R):          # sqrt(1 - v_river^2/c^2)  -> exact, cond. on exact sqrt  [F?]
    return math.sqrt(1.0 - v_river(M, R)**2 / C**2)

def f_schwarzschild(M, R):       # sqrt(1 - 2GM/rc^2)  exact GR  (MATCHING TARGET only)
    return math.sqrt(1.0 - 2.0 * G * M / (R * C**2))

def f_motion_leading(v):         # 1 - v^2/2c^2                                 [F leading]
    return 1.0 - 0.5 * v**2 / C**2

def f_motion_exact(v):           # sqrt(1 - v^2/c^2)   exact factor is [O] (not derived from medium)
    return math.sqrt(1.0 - v**2 / C**2)

# ----------------------------------------------------------------------------
# Gates
# ----------------------------------------------------------------------------
def gate_river():
    """G-RIVER: river kinematic factor == exact Schwarzschild, identically (machine-exact)."""
    rows, ok = [], True
    for name, (M, R) in BODIES.items():
        fr = f_grav_river(M, R)
        fs = f_schwarzschild(M, R)
        identical = (fr == fs)            # v_river^2 = 2GM/r  =>  1 - v_river^2/c^2 = 1 - 2GM/rc^2
        ok = ok and identical
        rows.append((name, R, v_river(M, R), v_river(M, R) / C, fr, fs, abs(fr - fs), identical))
    return ok, rows

def gate_rel_match():
    """REL-MATCH: leading combined == GPS expression at O(c^-2); show O(c^-4) departure vs river."""
    rows = []
    # one moving clock (GPS-like orbit speed) in each body's field, at the surface
    v_orb = 3874.0  # m/s (GPS-like); illustrative co-moving speed
    for name, (M, R) in BODIES.items():
        x = -phi_N(M, R) / C**2          # = GM/Rc^2 (small parameter)
        f_lead = f_grav_leading(M, R) - 0.5 * v_orb**2 / C**2     # GPS combined expression
        f_riv_exact = f_grav_river(M, R) * f_motion_exact(v_orb)  # exact medium-kinematic compose
        # analytic gravity-only departure of leading vs exact: O(x^2)
        depart_grav = f_grav_leading(M, R) - f_schwarzschild(M, R)
        rows.append((name, x, f_lead, f_riv_exact, depart_grav, 0.5 * x**2))
    return rows

def gate_two_velocity():
    """TWO-V: at fixed body, contrast mass-current (1/r^2) vs river (1/sqrt r) radial profiles."""
    name = "Earth"
    M, R = BODIES[name]
    rows = []
    for k in (1.0, 2.0, 4.0, 8.0):       # r = k * R
        r = k * R
        vmc = v_masscurrent(M, R, r)                 # ~ 1/r^2
        vrv = math.sqrt(2.0 * G * M / r)             # river at r ~ 1/sqrt(r)
        rows.append((name, k, vmc, vmc / v_river(M, R), vrv, vrv / v_river(M, R)))
    return rows

# ----------------------------------------------------------------------------
# Ledger emission
# ----------------------------------------------------------------------------
def build_ledger_csv():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["# VP Time-Gravity SSOT ledger (deterministic; standard-library)"])
    w.writerow(["# provenance: C=299792458 exact; G=6.67430e-11 (magnitude=[O] m_q);",
                "NU_E=1[F]; NU_P=3*pi^4[F]; MP_ME=6*pi^5[F]"])
    w.writerow([])
    w.writerow(["quantity", "closed_form", "value", "unit", "grade", "note"])
    w.writerow(["NU_E", "1 (eq phy-12-014)", repr(NU_E), "-", "[F]", "electron clock unit"])
    w.writerow(["NU_P", "3*pi^4", "%.6f" % NU_P, "s^-1", "[F]", "proton grind (LOCK-NU-N)"])
    w.writerow(["m_p/m_e", "6*pi^5 = 2*pi*NU_P", "%.6f" % MP_ME, "-", "[F]",
                "mass-rate identity; -19 ppm vs measured 1836.153"])
    w.writerow([])
    w.writerow(["# G-RIVER : sqrt(1 - v_river^2/c^2) == exact Schwarzschild sqrt(1 - 2GM/rc^2)"])
    w.writerow(["body", "R_m", "v_river_mps", "v_river_over_c", "f_river", "f_schwarzschild",
                "abs_diff", "identical", "grade"])
    ok_riv, rows = gate_river()
    for (name, R, vr, vrc, fr, fs, d, ident) in rows:
        w.writerow([name, "%.4g" % R, "%.6g" % vr, "%.6e" % vrc,
                    "%.15f" % fr, "%.15f" % fs, "%.3e" % d, ident, "[F?]"])
    w.writerow([])
    w.writerow(["# REL-MATCH : leading combined (GPS expr) vs exact medium-kinematic; O(x^2) departure"])
    w.writerow(["body", "x=GM/Rc^2", "f_leading_GPS", "f_exact_river*motion",
                "grav_depart_lead_vs_exact", "predicted_O(x^2)=x^2/2", "grade"])
    for (name, x, fl, fe, dep, ox2) in gate_rel_match():
        w.writerow([name, "%.6e" % x, "%.15f" % fl, "%.15f" % fe, "%.3e" % dep, "%.3e" % ox2,
                    "[F]@O(c^-2)"])
    w.writerow([])
    w.writerow(["# TWO-V : mass-current (~1/r^2, bookkeeping) vs river (~1/sqrt r, time-dilation)"])
    w.writerow(["body", "r_over_R", "v_masscurrent", "vmc_over_vriverR",
                "v_river_at_r", "vriv_over_vriverR", "grade"])
    for (name, k, vmc, vmcn, vrv, vrvn) in gate_two_velocity():
        w.writerow([name, "%.1f" % k, "%.6g" % vmc, "%.6e" % vmcn, "%.6g" % vrv, "%.6f" % vrvn,
                    "[F] shapes"])
    return buf.getvalue(), ok_riv

# ----------------------------------------------------------------------------
# Drift gate (--check): scan text files for canonical literals; flag mismatches.
# ----------------------------------------------------------------------------
# (regex capturing a number near a canonical token) -> (canonical value, rel-tol, label)
# Patterns cover both ASCII-lock (6*pi^5) and prose/unicode (6π⁵) forms.
DRIFT_RULES = [
    (re.compile(r"6\s*[\*x·]?\s*(?:pi|π)\s*(?:\^?\s*5|⁵)\D{0,40}?(\d{4}\.\d+)"),
     1836.118109, 5e-5, "6*pi^5"),
    (re.compile(r"3\s*[\*x·]?\s*(?:pi|π)\s*(?:\^?\s*4|⁴)\D{0,40}?(\d{3}\.\d+)"),
     292.2271, 5e-4, "3*pi^4"),
    # Earth river / escape velocity, however phrased (v_riv, river, escape, Earth) near the number
    (re.compile(r"(?:v_?riv|river|escape|Earth)\D{0,40}?(\b1[0-2]\s?\d{3}(?:\.\d+)?\b)\s*m"),
     11186.0, 5e-3, "Earth v_river"),
]

def drift_check(paths):
    issues, checked = [], 0
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        for rgx, canon, tol, label in DRIFT_RULES:
            for m in rgx.finditer(text):
                checked += 1
                try:
                    val = float(m.group(1))
                except (ValueError, IndexError):
                    continue
                if canon != 0 and abs(val - canon) / abs(canon) > tol:
                    issues.append((p, label, val, canon, abs(val - canon) / abs(canon)))
    return checked, issues

# ----------------------------------------------------------------------------
# Self-tests (assert) + determinism
# ----------------------------------------------------------------------------
def selftest():
    # G-RIVER is an exact identity for every body
    ok_riv, _ = gate_river()
    assert ok_riv, "G-RIVER FAIL: river factor != exact Schwarzschild"
    # mass-rate ratio is exactly 6*pi^5 and equals 2*pi*NU_P
    assert abs(MP_ME - 2.0 * math.pi * NU_P) < 1e-12, "mass-rate identity broken"
    assert abs(MP_ME - 1836.1181) < 1e-3, "6*pi^5 value drift"
    # leading gravity matches exact Schwarzschild to O(x^2)
    M, R = BODIES["Earth"]
    x = -phi_N(M, R) / C**2
    dep = abs(f_grav_leading(M, R) - f_schwarzschild(M, R))
    assert dep <= 1.0 * x**2, "leading-vs-exact departure exceeds O(x^2)"
    # two velocities have DIFFERENT radial scaling (1/r^2 vs 1/sqrt r): at r=4R they must differ
    Mr = 4.0 * R
    vmc = v_masscurrent(M, R, Mr) / v_river(M, R)     # = (R/4R)^2 = 1/16
    vrv = math.sqrt(2.0 * G * M / Mr) / v_river(M, R)  # = 1/2
    assert abs(vmc - 1.0/16.0) < 1e-9 and abs(vrv - 0.5) < 1e-9, "two-velocity scaling wrong"
    return True

def main(argv):
    if len(argv) > 1 and argv[1] == "--check":
        checked, issues = drift_check(argv[2:])
        if issues:
            print("DRIFT GATE: FAIL (%d issue(s); %d literal(s) checked)" % (len(issues), checked))
            for p, label, val, canon, rel in issues:
                print("  %s : %s = %.6g  vs canon %.6g  (rel %.2e)" % (p, label, val, canon, rel))
            return 1
        print("DRIFT GATE: PASS (%d literal(s) checked, 0 drift)" % checked)
        return 0

    assert selftest(), "selftest failed"
    csv_text, ok_riv = build_ledger_csv()

    # determinism: regenerate, hash twice, require identical
    csv_text2, _ = build_ledger_csv()
    h1 = hashlib.sha256(csv_text.encode()).hexdigest()
    h2 = hashlib.sha256(csv_text2.encode()).hexdigest()
    assert h1 == h2, "non-deterministic output"

    out_path = "TIME_GRAVITY_NUMERIC_LEDGER.csv"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(csv_text)

    # human-readable summary
    print("=" * 78)
    print("VP TIME-GRAVITY SSOT  —  deterministic ledger")
    print("=" * 78)
    print("NU_E = %s [F]   NU_P = 3*pi^4 = %.6f s^-1 [F]   m_p/m_e = 6*pi^5 = %.6f [F]"
          % (NU_E, NU_P, MP_ME))
    print()
    print("[G-RIVER]  sqrt(1 - v_river^2/c^2)  ==  sqrt(1 - 2GM/rc^2)   (exact Schwarzschild)")
    _, rows = gate_river()
    print("  %-12s %-12s %-9s %-20s %-20s %-9s" %
          ("body", "v_river[m/s]", "v/c", "f_river", "f_schwarzschild", "identical"))
    for (name, R, vr, vrc, fr, fs, d, ident) in rows:
        print("  %-12s %-12.6g %-9.3e %-20.15f %-20.15f %s" % (name, vr, vrc, fr, fs, ident))
    print("  => G-RIVER: %s  (river velocity IS the escape velocity; factor IS Schwarzschild)"
          % ("PASS" if ok_riv else "FAIL"))
    print()
    print("[REL-MATCH]  leading 1+phi/c^2 - v^2/2c^2 == GPS expression at O(c^-2);")
    print("             gravity leading vs exact departs at O(x^2), x=GM/Rc^2:")
    for (name, x, fl, fe, dep, ox2) in gate_rel_match():
        print("  %-12s x=%.3e   depart(lead vs exact)=%.3e   ~ x^2/2=%.3e" % (name, x, dep, ox2))
    print()
    print("[TWO-V]  mass-current ~1/r^2 (bookkeeping)  vs  river ~1/sqrt r (time-dilation):")
    for (name, k, vmc, vmcn, vrv, vrvn) in gate_two_velocity():
        print("  r=%.0fR :  v_mc/v_R = %.4e (1/r^2)   v_river/v_R = %.4f (1/sqrt r)"
              % (k, vmcn, vrvn))
    print()
    print("grades: [F] forced ; [F?] river=exact (cond. on exact-sqrt [O]) ; [O] m_q, exact-sqrt")
    print("No-Tuning: no coefficient migrated. ledger sha256 = %s" % h1)
    print("wrote: %s" % out_path)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
