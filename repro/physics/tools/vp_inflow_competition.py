#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_inflow_competition.py
VP Theory — quantum inflow competition: universality, cap=nuclear-saturation, falsifier.

Deterministic, standard-library only (math/csv/hashlib). 2x sha256 identical.
No-Tuning: SEMF coefficients are [CAL] (measured, used consistently) and are NOT fitted
to the VP claims; they are the standard textbook values, used to exhibit the SHAPE.

Blocks:
  PASS-A  : common slowdown factor f cancels in nu_p/nu_e -> m_p/m_e = 6*pi^5 preserved (LPI).
  DIFFER  : differential f_e != f_p -> implied m_p/m_e drift vs LPI bounds (Reading-B falsifier).
  SAT     : binding-energy/nucleon SATURATES (the cap); iron peak; competition reading of SEMF.
  ASTRO   : nu(phi_A)/nu(phi_B) is m_q-free (mapping symmetry); g_Moon/g_Earth cancels G/m_q.

Grades: [F] forced (ratio identity, scalar-free ratio) ; [F?] structural (cap == saturation
shape) ; [CAL] measured inputs (SEMF coeffs) ; [O] absolute scale (a_V, m_q).
"""

import math
import csv
import io
import hashlib

# ---- framework canon (referenced, not re-derived) ----
NU_E  = 1.0
NU_P  = 3.0 * math.pi**4
MP_ME = 6.0 * math.pi**5          # = 2*pi*NU_P                                   [F]

# ---- SEMF coefficients [CAL] (standard textbook, MeV) — NOT tuned to VP ----
A_V, A_S, A_C, A_A, A_P = 15.8, 18.3, 0.714, 23.2, 12.0

# Empirical binding-energy/nucleon (MeV) — MATCHING TARGET only, not derived.
EMPIRICAL_BA = {2: 1.112, 4: 7.074, 12: 7.680, 16: 7.976, 56: 8.790, 238: 7.570}

# ----------------------------------------------------------------------------
# PASS-A : universality (common f) preserves the mass ratio (LPI)
# ----------------------------------------------------------------------------
def mp_me_under_common_f(f):
    """nu_e -> nu_e*f, nu_p -> nu_p*f ; m_p/m_e = 2*pi*(nu_p*f)/(nu_e*f) = 6*pi^5 (f cancels)."""
    nu_e, nu_p = NU_E * f, NU_P * f
    return 2.0 * math.pi * (nu_p / nu_e)

# ----------------------------------------------------------------------------
# DIFFER : Reading-B falsifier — differential factors drift the ratio
# ----------------------------------------------------------------------------
def mp_me_under_differential(f_e, f_p):
    nu_e, nu_p = NU_E * f_e, NU_P * f_p
    return 2.0 * math.pi * (nu_p / nu_e)

# Empirical bounds that constrain a rotor-scale anisotropy delta = f_p/f_e - 1.
LPI_BOUNDS = {"atomic/nuclear clock (historical)": 1e-6,
              "optical-clock comparison (current)": 1e-18}

def differential_falsifier():
    """Reading-B falsifier: differential f_e != f_p drifts m_p/m_e by ~delta (leading order).
    Only deltas above double-precision resolution (~1e-15) are computed numerically; the
    tighter empirical bound is stated, not computed (it is below fp resolution here)."""
    base = MP_ME
    rows = []
    for delta in (1e-3, 1e-6, 1e-9, 1e-12):     # all > fp floor: drift is resolvable
        ratio = mp_me_under_differential(1.0, 1.0 + delta)     # f_e=1, f_p=1+delta
        rel = (ratio - base) / base
        rows.append((delta, ratio, rel))
    return rows

# ----------------------------------------------------------------------------
# SAT : cap == nuclear binding saturation (SEMF), with competition reading
# ----------------------------------------------------------------------------
def semf_binding_per_nucleon(A, Z):
    """Bethe-Weizsaecker B/A in MeV. Pairing for even-even / odd-odd."""
    N = A - Z
    pairing = 0.0
    if A % 2 == 0:
        if Z % 2 == 0 and N % 2 == 0:
            pairing = +A_P / math.sqrt(A)
        else:
            pairing = -A_P / math.sqrt(A)
    B = (A_V * A
         - A_S * A**(2.0/3.0)
         - A_C * Z * (Z - 1) / A**(1.0/3.0)
         - A_A * (N - Z)**2 / A
         + pairing)
    return B / A

def z_valley(A):
    """Most-stable Z along the valley of stability (minimize SEMF asymmetry+Coulomb)."""
    # closed form: Z* = A / (2 + a_C/(2 a_A) * A^(2/3))
    return A / (2.0 + (A_C / (2.0 * A_A)) * A**(2.0/3.0))

def sat_curve():
    rows, best = [], (None, -1.0)
    for A in (4, 8, 12, 16, 24, 40, 56, 60, 90, 120, 150, 200, 238):
        Z = round(z_valley(A))
        ba = semf_binding_per_nucleon(A, int(Z))
        if ba > best[1]:
            best = (A, ba)
        rows.append((A, int(Z), ba))
    return rows, best  # best = (A_peak, BA_peak)

# ----------------------------------------------------------------------------
# ASTRO : nu(phi_A)/nu(phi_B) is m_q-free (mapping symmetry)
# ----------------------------------------------------------------------------
def astro_ratio_scalar_free():
    """g = G M / R^2 ; ratio g_Moon/g_Earth cancels G (=> the [O] m_q scalar cancels)."""
    G = 6.67430e-11
    bodies = {"Moon": (7.342e22, 1.7374e6), "Earth": (5.9722e24, 6.371e6)}
    def g(name):
        M, R = bodies[name]
        return G * M / R**2
    g_moon, g_earth = g("Moon"), g("Earth")
    ratio_withG = g_moon / g_earth
    # same ratio with G set to an ARBITRARY other value -> identical (proves G/m_q cancels)
    Galt = 1.2345e-9
    def galt(name):
        M, R = bodies[name]
        return Galt * M / R**2
    ratio_altG = galt("Moon") / galt("Earth")
    return g_moon, g_earth, ratio_withG, ratio_altG, abs(ratio_withG - ratio_altG)

# ----------------------------------------------------------------------------
# Ledger + self-tests
# ----------------------------------------------------------------------------
def build_csv():
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
    w.writerow(["# VP inflow-competition ledger (deterministic; standard-library)"])
    w.writerow(["# NU_E=1[F]; NU_P=3*pi^4[F]; MP_ME=6*pi^5[F]; SEMF coeffs=[CAL] textbook (not tuned)"])
    w.writerow([])
    w.writerow(["block", "key", "value", "grade", "note"])
    # PASS-A
    for f in (1.0, 0.999999, 1.0 - 1e-3):
        w.writerow(["PASS-A", "m_p/m_e @ f=%.6g" % f, "%.6f" % mp_me_under_common_f(f),
                    "[F]", "common f cancels -> 6*pi^5 preserved (LPI)"])
    # DIFFER
    for (delta, ratio, rel) in differential_falsifier():
        w.writerow(["DIFFER", "delta=f_p/f_e-1=%.0e" % delta, "m_p/m_e=%.6f rel=%.2e" % (ratio, rel),
                    "[H/O]", "Reading-B: drift ~ delta (leading)"])
    for name, b in LPI_BOUNDS.items():
        w.writerow(["DIFFER", "empirical bound: %s" % name, "delta < %.0e" % b, "[H/O]",
                    "Reading-B excluded if rotor-scale delta exceeds this"])
    # SAT
    rows, (Apk, BApk) = sat_curve()
    for (A, Z, ba) in rows:
        emp = EMPIRICAL_BA.get(A)
        note = "iron-peak region" if A in (56, 60) else ("vs empirical %.3f" % emp if emp else "")
        w.writerow(["SAT", "B/A @ A=%d (Z=%d)" % (A, Z), "%.3f MeV" % ba, "[F?]", note])
    w.writerow(["SAT", "peak", "A=%d, B/A=%.3f MeV" % (Apk, BApk), "[F?]",
                "cap ceiling = saturation; a_V=%.1f [CAL]; absolute scale=[O]" % A_V])
    # ASTRO
    gm, ge, rG, ralt, d = astro_ratio_scalar_free()
    w.writerow(["ASTRO", "g_Moon/g_Earth", "%.5f" % rG, "[F]", "scalar-free"])
    w.writerow(["ASTRO", "same ratio with arbitrary G", "%.5f (diff %.1e)" % (ralt, d), "[F]",
                "G (=> m_q) cancels in the ratio"])
    return buf.getvalue()

def selftest():
    # PASS-A: common f preserves ratio EXACTLY for any f>0
    for f in (1.0, 0.5, 1e-3, 0.999999):
        assert abs(mp_me_under_common_f(f) - MP_ME) < 1e-9, "common-f universality broken"
    # DIFFER: a differential delta drifts the ratio by exactly delta (to leading order)
    delta = 1e-9
    r = mp_me_under_differential(1.0, 1.0 + delta)
    assert abs((r - MP_ME) / MP_ME - delta) < 1e-15 + 1e-6*delta, "differential falsifier mis-scaled"
    # SAT: binding/nucleon peaks in the iron region and saturates near ~8.8 MeV
    _, (Apk, BApk) = sat_curve()
    assert 50 <= Apk <= 65, "iron peak outside [50,65]: A=%d" % Apk
    assert 8.5 <= BApk <= 8.9, "saturation B/A outside [8.5,8.9]: %.3f" % BApk
    # SAT: it is a saturation (B/A at A=16 already within ~12%% of the peak -> flat plateau)
    ba16 = semf_binding_per_nucleon(16, 8)
    assert ba16 / BApk > 0.85, "no plateau: B/A(16)/peak too small"
    # ASTRO: ratio is independent of G (scalar-free)
    _, _, rG, ralt, d = astro_ratio_scalar_free()
    assert d < 1e-12, "astro ratio not scalar-free"
    assert 0.16 <= rG <= 0.17, "g_Moon/g_Earth out of expected band: %.5f" % rG
    return True

def main():
    assert selftest(), "selftest failed"
    csv_text = build_csv()
    h1 = hashlib.sha256(csv_text.encode()).hexdigest()
    h2 = hashlib.sha256(build_csv().encode()).hexdigest()
    assert h1 == h2, "non-deterministic output"
    with open("INFLOW_COMPETITION_LEDGER.csv", "w", encoding="utf-8") as fh:
        fh.write(csv_text)

    print("=" * 78)
    print("VP INFLOW-COMPETITION  —  deterministic ledger")
    print("=" * 78)
    print("[PASS-A] universality: common f cancels in nu_p/nu_e")
    for f in (1.0, 0.999999, 0.9):
        print("  f=%-10.6g  ->  m_p/m_e = %.6f   (target 6*pi^5 = %.6f)"
              % (f, mp_me_under_common_f(f), MP_ME))
    print("  => m_p/m_e invariant under common slowdown -> LPI preserved  [F]")
    print()
    print("[DIFFER] Reading-B falsifier: differential f_e != f_p drifts the ratio")
    for (delta, ratio, rel) in differential_falsifier():
        print("  delta=f_p/f_e-1=%.0e  ->  m_p/m_e drift rel=%.2e   (drift ~ delta)" % (delta, rel))
    for name, b in LPI_BOUNDS.items():
        print("  empirical bound [%s]: rotor-scale delta < %.0e" % (name, b))
    print("  => Reading-B excluded if delta exceeds the tightest bound (optical clocks ~1e-18)  [H/O]")
    print()
    print("[SAT] cap == nuclear binding/nucleon saturation (SEMF; coeffs [CAL], not tuned)")
    rows, (Apk, BApk) = sat_curve()
    for (A, Z, ba) in rows:
        emp = EMPIRICAL_BA.get(A)
        tail = ("   (empirical %.3f)" % emp) if emp else ""
        print("  A=%-3d Z=%-3d  B/A = %.3f MeV%s" % (A, Z, ba, tail))
    print("  => peak A=%d, B/A=%.3f MeV; plateau from A~16 = the cap ceiling  [F?]" % (Apk, BApk))
    print("     (a_V=%.1f MeV cooperative-inflow ceiling [CAL]; absolute scale = [O] m_q class)" % A_V)
    print()
    print("[ASTRO] mapping symmetry: nu(phi_A)/nu(phi_B) is m_q-free")
    gm, ge, rG, ralt, d = astro_ratio_scalar_free()
    print("  g_Moon/g_Earth = %.5f   (with arbitrary G: %.5f, diff %.1e)" % (rG, ralt, d))
    print("  => the [O] absolute scalar cancels in body-to-body ratios  [F]")
    print()
    print("No-Tuning: SEMF coeffs are standard [CAL], not fitted to VP. ledger sha256 = %s" % h1)
    print("wrote: INFLOW_COMPETITION_LEDGER.csv")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
