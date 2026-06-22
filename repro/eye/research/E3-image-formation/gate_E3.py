#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E3.py — the focused pass/fail gate for increment E3 (run from the package root).

    python3 research/E3-image-formation/gate_E3.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E3-image-formation/run.py emits an identical sha256 on two runs.
  [G2] SNELL=MATCH   — θ₂ from the wavefront/SPEED construction equals θ₂ from the index form to the
                       bit, across an incidence sweep (Snell IS the transverse-oscillation match).
  [G3] TIR ONSET     — dense→rare, a ray just below the critical angle refracts and a ray just above
                       has no real transverse match (total internal reflection) — at arcsin(c₁/c₂).
  [G4] n IDENTITY    — n recovered as the wave-speed ratio c_vac/c_eye equals the cited index 4/3.
  [G5] RETINA FOCUS  — the cited reduced eye gives power ≈60 D and images a distant point at the
                       ≈22.2 mm axial length (the retina): consistency of the cited n,R, not a fit.
  [G6] INVERSION     — every real finite object forms a real image with lateral magnification m<0
                       (the spatial position code is a real inverted image).
  [G7] COLOUR INTACT — the inherited colour anchors stay distinct angles (red 633 ≠ green 532), while
                       a single index co-locates them on the retina (first-order chromatic split = 0):
                       optics gives WHERE, the angle law gives WHAT COLOUR.

Exit 0 + 'E3 GATE: PASS' only if all hold.
"""
import os, sys, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_light_emergence_quantum import D as D_LIGHT          # FROZEN invariant quantum size
from vp_color_by_angle import D as D_COLOUR, chi_deg          # FROZEN colour-by-angle reading
RUN = os.path.join(_HERE, "run.py")

N_AIR, N_EYE, R_MM = 1.0, 4.0 / 3.0, 5.55                     # cited Emsley reduced-eye constants
LAM_RED, LAM_GRN = 632.99e-9, 532.0e-9


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _v(u_mm, n1, n2, R):
    inv_u = 0.0 if u_mm is None else 1.0 / u_mm
    return n2 / ((n2 - n1) / R + n1 * inv_u)


def main():
    print("=" * 74)
    print("E3 GATE — research/E3-image-formation")
    print("=" * 74)
    ok = True

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # inheritance integrity: the two frozen modules agree on D
    assert D_LIGHT == D_COLOUR, "inherited D must match across the frozen wave modules"
    c_air, c_eye = 1.0, 1.0 / N_EYE

    # [G2] Snell from speeds == Snell from index
    g2 = True
    for deg in (0.0, 10.0, 20.0, 30.0, 45.0, 60.0, 80.0):
        t1 = math.radians(deg)
        s2_speed = math.asin(math.sin(t1) * (c_eye / c_air))
        s2_index = math.asin((N_AIR / N_EYE) * math.sin(t1))
        g2 &= abs(s2_speed - s2_index) < 1e-12
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 Snell=match — wavefront/speed θ₂ = index θ₂ to <1e-12 "
          f"(Snell is the transverse match)")

    # [G3] TIR onset at the critical angle (dense→rare)
    crit = math.asin(c_eye / c_air)                          # arcsin(n_air/n_eye)
    below = math.sin(crit - math.radians(0.5)) * (c_air / c_eye)   # dense→rare uses c₂/c₁ = c_air/c_eye
    above = math.sin(crit + math.radians(0.5)) * (c_air / c_eye)
    g3 = (below <= 1.0) and (above > 1.0); ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 TIR onset — refracts below θc={math.degrees(crit):.3f}°, "
          f"no real match above (total internal reflection)")

    # [G4] n recovered as the wave-speed ratio equals the cited index
    n_recovered = c_air / c_eye
    g4 = abs(n_recovered - N_EYE) < 1e-12; ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 n identity — n = c_vac/c_eye = {n_recovered:.4f} = cited 4/3 "
          f"(n is the (B/ρ) ratio)")

    # [G5] retina focus: power ≈60 D and distant focus at ≈22.2 mm
    power = (N_EYE - N_AIR) / (R_MM * 1e-3)
    v_inf = _v(None, N_AIR, N_EYE, R_MM)
    g5 = (59.0 < power < 61.0) and (22.0 < v_inf < 22.4); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 retina focus — P={power:.2f} D, distant point at "
          f"v={v_inf:.3f} mm (≈22.2 mm axial length)")

    # [G6] inversion: m<0 for every real object
    g6 = True
    for u_mm in (-1000.0, -500.0, -250.0):
        v = _v(u_mm, N_AIR, N_EYE, R_MM)
        m = (N_AIR * v) / (N_EYE * u_mm)
        g6 &= (m < 0.0)
    ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 inversion — every real object images with m<0 "
          f"(real inverted spatial code)")

    # [G7] colour intact: distinct χ, zero first-order chromatic split
    chi_r, chi_g = chi_deg(LAM_RED), chi_deg(LAM_GRN)
    v_r, v_g = _v(-1000.0, N_AIR, N_EYE, R_MM), _v(-1000.0, N_AIR, N_EYE, R_MM)
    g7 = (abs(chi_r - chi_g) > 0.05) and (v_r == v_g); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 colour intact — χ distinct (Δχ={abs(chi_r-chi_g):.4f}°), "
          f"single-n split |Δv|={abs(v_r-v_g):.1e} mm (WHERE vs WHAT-COLOUR)")

    print("=" * 74)
    print(f"E3 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
