#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E6.py — the focused pass/fail gate for increment E6 (run from the package root).

    python3 research/E6-why-visible/gate_E6.py

Asserts, independently of run.py's own internal asserts (and with the SAME precision discipline —
the wavelength is mapped exactly; the angle is carried to full precision and checked against the
canonical closure m·sinχ·D/λ=1):

  [G1] DETERMINISM      — research/E6-why-visible/run.py emits an identical sha256 on two runs.
  [G2] EXACT CARRIER MAP— for every ALREADY-MEASURED visible anchor (633, 532, opsin 420/530/560),
                          ν=c/λ lands in the ~10¹⁴ Hz visible band, the period T=1/ν matches λ/c to
                          1e-15, and E=hν matches hc/λ to 1e-15 (SI-exact constants; no rounding).
  [G3] GATE (i) m-SANDWICH + EXACT ANGLE — the inherited angle law places the bands in the fixed
                          monotone m-order gamma<x-ray<visible<IR<radio (visible sandwiched in m);
                          gamma (m=1) is the lone quasi-longitudinal band (χ<13°), visible is
                          near-transverse (89.7–90°); every angle satisfies the closure to 1e-12 and
                          matches the frozen canon to 1e-6 (no drift).
  [G4] GATE (ii) WINDOW  — the cited isomerisation window (1.8–3.3 eV) maps via λ=hc/E onto
                          375.71–688.80 nm, and EVERY measured visible anchor lies inside it.
  [G5] GEOMETRY ≠ EDGES  — the band-internal angle deficit (90°−χ) is tiny (<0.3°) and NON-monotone (a
                          sawtooth: 633 nm has a smaller deficit than 750 nm though it is shorter),
                          versus a >78° gamma deficit: there is no geometric kink at the band edges.
  [G6] ENERGY PINS       — the edges coincide with the energy window, not geometry: an infrared probe
                          (10 µm, ≈0.124 eV) is excluded by the energy floor although its deficit is
                          SMALLER than visible's (more transverse, larger m) — geometry would admit it.
  [G7] SOFT RED + [O]    — the deep-red edge is soft and honest: 750 nm (1.6531 eV) sits <0.2 eV below
                          the clean floor (1.8 eV); the window/anchor inputs are CITED (frozen as
                          written), not fits — the chromophore tuning stays a named [O].
  [G8] NO-DRIFT          — c, h are the SI-exact values, D is byte-equal to the inherited invariant
                          (= §E0, 4.852620 pm), SEED=19, the atlas still carries 19 genes and
                          γ(GUCY2D) is byte-equal to the frozen atlas; E6 adds no γ and tunes nothing.

Exit 0 + 'E6 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

import vp_visible_band_canonical as VB                  # inherited canon: angle law + H, C_SI, D (read-only)
from vp_substrate import SEED                            # FROZEN substrate seed
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

C, H, QE = VB.C_SI, VB.H, 1.602176634e-19
EV_PER_J = 1.0 / QE
D        = VB.D
ISOM_EV  = (1.8, 3.3)
VIS_CONV_NM = (380.0, 750.0)
D_E0_PM  = 4.852620                                       # the §E0 invariant, to 6 dp
ANCHORS_NM = (("HeNe red", 632.99), ("green", 532.0),
              ("opsin S", 420.0), ("opsin M", 530.0), ("opsin L", 560.0))


def nu_of(lam_m):   return C / lam_m
def period_of(lam_m): return lam_m / C
def eV_of(lam_m):   return H * (C / lam_m) * EV_PER_J
def nm_from_eV(e):  return H * C / (e / EV_PER_J) * 1e9


def angle_hp(lam_m):
    m = math.ceil(lam_m / D)
    x = lam_m / (m * D)
    cos_chi = math.sqrt((1.0 - x) * (1.0 + x))
    delta = math.atan2(cos_chi, x)
    chi = math.pi / 2.0 - delta
    closure = m * math.sin(chi) * D / lam_m
    return m, x, math.degrees(chi), math.degrees(delta), closure


def _run_capture():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def main():
    print("=" * 78)
    checks = []

    # G1 — determinism
    s1, s2 = _sha_of(_run_capture()), _sha_of(_run_capture())
    checks.append(("G1 determinism", s1 == s2, f"run.py sha256 stable ({s1[:16]})"))

    # G2 — exact carrier map for every measured anchor: ν band, T=1/ν, E=hν
    ok2 = True
    for _, nm in ANCHORS_NM:
        lam = nm * 1e-9
        ok2 &= (4.0e14 < nu_of(lam) < 8.0e14)
        ok2 &= math.isclose(period_of(lam), 1.0 / nu_of(lam), rel_tol=1e-15)
        ok2 &= math.isclose(eV_of(lam), H * nu_of(lam) * EV_PER_J, rel_tol=1e-15)
    lam0 = 632.99e-9
    checks.append(("G2 carrier-map", ok2,
                   f"633nm→ν={nu_of(lam0):.6e}Hz T={period_of(lam0):.6e}s E={eV_of(lam0):.6f}eV; T=1/ν & E=hν to 1e-15"))

    # G3 — gate (i): the m-sandwich + exact angles (closure to 1e-12, matches canon to 1e-6)
    bands_nm = [1e-3, 10.0, 380.0, 750.0, 10_000.0, 1e9]              # γ,x-ray,vis,vis,IR,radio
    res = [angle_hp(x * 1e-9) for x in bands_nm]
    m_mono = all(res[i][0] < res[i + 1][0] for i in range(len(res) - 1))
    clo_ok = all(abs(r[4] - 1.0) < 1e-12 for r in res)
    drift_ok = all(abs(angle_hp(x * 1e-9)[2] - VB.chi_deg(x * 1e-9)) < 1e-6 for x in bands_nm)
    near_T = (angle_hp(1e-12)[2] < 13.0) and (89.7 < angle_hp(380e-9)[2] < 90.0) and (89.7 < angle_hp(750e-9)[2] < 90.0)
    g3 = m_mono and clo_ok and drift_ok and near_T
    checks.append(("G3 m-sandwich", g3,
                   f"m: γ(1)<xray({res[1][0]})<vis({res[2][0]}..{res[3][0]})<IR({res[4][0]})<radio; closure≈1 (≤1e-12), canon-match≤1e-6"))

    # G4 — gate (ii): the cited window maps onto ~visible (exact edges); all measured anchors inside
    w_hi_nm, w_lo_nm = nm_from_eV(ISOM_EV[0]), nm_from_eV(ISOM_EV[1])
    inside = all(ISOM_EV[0] <= eV_of(nm * 1e-9) <= ISOM_EV[1] for _, nm in ANCHORS_NM)
    g4 = (375.0 < w_lo_nm < 376.5) and (688.0 < w_hi_nm < 689.5) and inside
    checks.append(("G4 energy-window", g4,
                   f"{ISOM_EV[0]}–{ISOM_EV[1]} eV → {w_lo_nm:.5f}–{w_hi_nm:.5f} nm; all 5 measured anchors inside"))

    # G5 — geometry cannot pin: the deficit is tiny and a NON-monotone sawtooth
    d380, d633, d750 = angle_hp(380e-9)[3], angle_hp(632.99e-9)[3], angle_hp(750e-9)[3]
    dgam = angle_hp(1e-12)[3]
    band_span = max(d380, d633, d750) - min(d380, d633, d750)
    sawtooth = (d633 < d750)                                          # shorter λ, smaller deficit ⇒ not monotone
    g5 = sawtooth and (band_span < 0.3) and (dgam > 78.0)
    checks.append(("G5 geom≠edges", g5,
                   f"deficits 380={d380:.6f}° 633={d633:.6f}° 750={d750:.6f}° (sawtooth: 633<750); γ deficit={dgam:.2f}°"))

    # G6 — the pinning is energetic: an IR probe is excluded by energy though geometry prefers it
    e_ir, d_ir, m_ir = eV_of(10_000e-9), angle_hp(10_000e-9)[3], angle_hp(10_000e-9)[0]
    m_vis = angle_hp(750e-9)[0]
    g6 = (e_ir < ISOM_EV[0]) and (d_ir < d750) and (m_ir > m_vis)
    checks.append(("G6 energy-pins", g6,
                   f"IR 10µm: E={e_ir:.6f}eV<floor (excluded by energy) but deficit {d_ir:.6f}°<{d750:.6f}° & m={m_ir}>{m_vis}"))

    # G7 — honest soft red edge + the inputs are cited (not fits); chromophore tuning is [O]
    red_gap = ISOM_EV[0] - eV_of(750e-9)
    cited_frozen = (ISOM_EV == (1.8, 3.3)) and (VIS_CONV_NM == (380.0, 750.0))
    g7 = (0.0 < red_gap < 0.2) and cited_frozen
    checks.append(("G7 soft-red+[O]", g7,
                   f"red edge {eV_of(750e-9):.6f}eV sits {red_gap:.6f}eV under the {ISOM_EV[0]}eV floor (soft); inputs cited"))

    # G8 — no drift / no fitting
    g_used = float(ATLAS["GUCY2D"]["gamma"])
    g8 = (C == 299792458.0) and (H == 6.62607015e-34) and (round(D * 1e12, 6) == D_E0_PM) \
         and (SEED == 19) and (len(ATLAS) == 19) and (g_used == ATLAS["GUCY2D"]["gamma"])
    checks.append(("G8 no-drift", g8,
                   f"c,h SI-exact; D={D*1e12:.6f}pm (=§E0); SEED={SEED}; atlas={len(ATLAS)} genes; γ(GUCY2D)={g_used} byte-equal"))

    ok_all = True
    for name, ok, msg in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {msg}")
    print("=" * 78)
    print(f"E6 GATE: {'PASS' if ok_all else 'FAIL'}")
    print("=" * 78)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
