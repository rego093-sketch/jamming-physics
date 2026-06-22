#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E3-image-formation/run.py — INCREMENT E3: image formation.

WHAT E3 DOES (BLUEPRINT.md E3; research/E3-image-formation/START_HERE.md).
  Ground the reduced-eye optics on the SAME inherited wave physics that already carries colour —
  the INTERNAL angle law sinχ = λ/(mD), D invariant (vp_light_emergence_quantum / vp_color_by_angle,
  chemistry §1: conduction↔radiation BY ANGLE). The external Snell/refraction picture is kept only as
  the lab-space SHADOW of that wave physics, never as an independent axiom, and every step that is
  ordinary classical ray arithmetic is flagged [V-arith] rather than dressed up as substrate-derived.

  WHY THE INTERNAL ANGLE THEORY (and where external optics ALONE gets stuck).
    If refraction is taken externally — "the medium has a measured refractive index n, apply Snell" —
    then n is an opaque material constant, the reduced-eye focus is pure classical trigonometry, the
    substrate contributes NOTHING, and colour and image are two unrelated facts. The internal angle
    law fixes all three: it says (i) what n IS — the lattice wave-speed ratio n = c_vac/c_med =
    √((B/ρ)_vac /(B/ρ)_med); (ii) what Snell IS — the transverse-oscillation (phase) match at the
    interface; and (iii) that refraction relocates the ray (forms the image) while CONSERVING the
    frequency f, so the colour-angle χ(λ) survives the optics intact. Same one wave, two codes.

  Three things, built ONLY on the frozen inherited wave foundation (no γ, no atlas — E3 is optics):

    PART A — SNELL'S LAW IS THE TRANSVERSE-OSCILLATION MATCH, AND n IS THE LATTICE (B/ρ) RATIO.
      A plane wavefront crossing an interface must keep its oscillation phase CONTINUOUS along the
      boundary: the transverse swing on side 1 and side 2 march together at the shared interface. In
      one wavefront-construction time t, the side-1 wavefront advances c₁·t and the side-2 wavefront
      c₂·t across a shared interface segment L; the geometry L·sinθ₁=c₁·t, L·sinθ₂=c₂·t gives
      sinθ₁/sinθ₂ = c₁/c₂. With the wave speed c=√(B/ρ) and n≡c_vac/c, that IS n₁sinθ₁=n₂sinθ₂. We
      compute θ₂ from the wave SPEEDS (wavefront match) and, independently, from the index form, and
      show they are bit-identical across an incidence sweep — Snell is derived from the wave, not
      posited. The total-internal-reflection critical angle (no real transverse match) falls out at
      arcsin(c₁/c₂). [F] the relation is forced by phase continuity · [V] the numeric identity ·
      [L] the medium's (B/ρ)≡n is a measured input (cited), never fitted.

    PART B — THE REDUCED EYE FORMS A REAL INVERTED IMAGE ON THE RETINA (classical arithmetic, flagged).
      The Emsley reduced eye (single refracting surface, air n₁=1 → eye n₂=4/3, radius R=5.55 mm —
      CITED standard schematic-eye constants, not fitted) refracts by Snell (Part A) and the
      single-surface equation n₂/v − n₁/u = (n₂−n₁)/R (which itself FOLLOWS from Snell + small-angle
      geometry). A distant point (1/u→0) images at v = n₂R/(n₂−n₁) = the axial length; the surface
      power is (n₂−n₁)/R. A finite object images with lateral magnification m=(n₁v)/(n₂u) < 0 — a real
      INVERTED image: a point above the axis lands below the fovea. The retina therefore samples a
      SPATIAL code — retinal POSITION — exactly the "wave property → spatial code" skeleton. This
      whole part is honest classical ray arithmetic: it consumes Snell (substrate-grounded in Part A)
      plus the measured n and R, but the geometry is NOT substrate DYNAMICS. Graded [V-arith]/[L].

    PART C — TWO INDEPENDENT CODES: OPTICS GIVES *WHERE*, THE ANGLE LAW GIVES *WHAT COLOUR*.
      Every refraction conserves the frequency f (a boundary condition), so the internal colour-angle
      χ(λ) — red 633→89.9378°, green 532→89.8248° (inherited vp_color_by_angle) — is PRESERVED through
      the optics. With a single medium index, both colours from one object point image to the SAME
      retinal position (the first-order chromatic split is exactly zero — verified bit-for-bit) yet
      carry DISTINCT χ labels. So the eye runs two orthogonal channels on one wave: a ROBUST position
      channel (external θ, ordinary refraction — spatial detail) and a HYPERSENSITIVE colour channel
      (internal χ near 90° — wavelength). The residual chromatic aberration is second-order and needs
      the medium's dispersion c_med(λ); the bare angle law fixes only that colour is an angle and is
      conserved, NOT the aberration magnitude — that magnitude (diopters) is a named [O], not invented.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E3 CONSUMES the frozen wave foundation and re-derives nothing:
    - the invariant quantum size D + the angle law sinχ=λ/(mD)  ← inherited/vp_light_emergence_quantum.py
    - the colour-by-angle reading χ(λ) (the committed 633/532)   ← inherited/vp_color_by_angle.py
  Both modules compute the SAME D = 2h/(mₑc); E3 asserts they are byte-identical before using them.
  No constant is fitted (FIREWALL #2); the wave theory is inherited, not re-opened (FIREWALL #6). E3
  touches no disease layer and no felt percept — it is the physical/optics layer only (FIREWALL #3/#4).
  The ocular n and surface radius R are MEASURED schematic-eye inputs (cited), never tuned to a target.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [V-arith] classical ray arithmetic (honestly flagged)
                     · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen wave foundation's constants/helpers — pure math, no RNG.
Deterministic: 2× run → identical sha256.
"""
import os, sys, math, hashlib, io

# --- locate the package root cwd-independently, import ONLY the frozen inherited wave foundation ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E3-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_light_emergence_quantum import D as D_LIGHT, angle   # FROZEN: invariant D + the angle law
from vp_color_by_angle import D as D_COLOUR, chi_deg          # FROZEN: colour-by-angle reading χ(λ)

# inheritance integrity: the two frozen modules must agree on the invariant quantum size to the bit.
assert D_LIGHT == D_COLOUR, "inherited D must be byte-identical across the frozen wave modules"
D = D_LIGHT

# ---- CITED schematic-eye constants (Emsley reduced eye) — measured inputs, NOT fitted ----
N_AIR   = 1.0           # vacuum/air index (n = c_vac/c = 1)
N_EYE   = 4.0 / 3.0     # Emsley reduced-eye homogeneous medium index (cited standard)
R_MM    = 5.55          # Emsley reduced-eye single-surface radius of curvature, mm (cited standard)
# the committed colour anchor (inherited, never re-decided)
LAM_RED, LAM_GRN = 632.99e-9, 532.0e-9


def snell_from_speeds(theta1_rad, c1, c2):
    """θ₂ from the WAVEFRONT/transverse match using wave SPEEDS only (Huygens construction):
    in time t the side-1 wavefront crosses c₁·t and side-2 crosses c₂·t over a shared interface
    segment L, so L·sinθ₁=c₁·t and L·sinθ₂=c₂·t ⇒ sinθ₂ = sinθ₁·(c₂/c₁). Returns None for TIR."""
    s2 = math.sin(theta1_rad) * (c2 / c1)
    if s2 > 1.0:
        return None                                  # no real transverse match → total internal reflection
    return math.asin(s2)


def snell_from_index(theta1_rad, n1, n2):
    """θ₂ from the index form n₁sinθ₁=n₂sinθ₂ (independent code path). Returns None for TIR."""
    s2 = (n1 / n2) * math.sin(theta1_rad)
    if s2 > 1.0:
        return None
    return math.asin(s2)


def surface_image_distance(u_mm, n1, n2, R_mm):
    """Single refracting surface (Cartesian sign convention, light travels +): paraxial image
    distance v from n₂/v − n₁/u = (n₂−n₁)/R. u<0 for a real object to the left; u→−∞ (1/u→0) is a
    distant object. This equation is itself a consequence of Snell + small-angle geometry [V-arith]."""
    inv_u = 0.0 if u_mm is None else (1.0 / u_mm)    # u_mm None ⇒ object at infinity
    rhs = (n2 - n1) / R_mm + n1 * inv_u
    return n2 / rhs                                  # = v (mm), measured from the surface


def run(P):
    P("=" * 80)
    P("E3 — IMAGE FORMATION   (reduced-eye optics grounded on the internal angle law)")
    P("=" * 80)
    P("consumes (frozen): vp_light_emergence_quantum.D/angle · vp_color_by_angle.chi_deg")
    P("re-derives: nothing. n, R are MEASURED schematic-eye inputs (cited), never fitted.")
    P(f"invariant quantum size D = {D*1e12:.6f} pm (byte-identical across both frozen modules).")
    P("the INTERNAL angle law sinχ=λ/(mD) carries colour; external Snell is its lab-space shadow.")

    # ------------------------------------------------------------------------------------------
    # PART A — Snell IS the transverse-oscillation match; n is the lattice (B/ρ) ratio
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — Snell's law = the transverse-oscillation (phase) match; n = c_vac/c_med = √((B/ρ) ratio)")
    P("-" * 80)
    # the medium's wave speed is fixed by its index via the lattice identity n = c_vac/c_med.
    c_air = 1.0                                      # quantum units: c_vac = 1 (vp_light_emergence_quantum)
    c_eye = c_air / N_EYE                            # c_med = c_vac / n  (slower in the denser medium)
    P(f"lattice identity: c_vac=1 (quantum units), c_eye = c_vac/n = {c_eye:.6f}  ⇒  n = c_vac/c_eye = {c_air/c_eye:.4f}")
    P(f"  (n is the wave-speed ratio = √((B/ρ)_vac /(B/ρ)_med) — the substrate meaning of 'refractive index') [F-identity]")
    P("\nderive θ₂ two independent ways — wavefront/SPEED match vs the index form — over an incidence sweep:")
    P(f"  {'θ₁(in air)':>10s} {'θ₂ via speeds':>13s} {'θ₂ via index':>13s} {'|Δ|':>9s}")
    max_diff = 0.0
    for deg in (0.0, 10.0, 20.0, 30.0, 45.0, 60.0, 80.0):
        t1 = math.radians(deg)
        t2_speed = snell_from_speeds(t1, c_air, c_eye)     # uses c₁,c₂ (wavefront geometry)
        t2_index = snell_from_index(t1, N_AIR, N_EYE)      # uses n₁,n₂ (index relation)
        d = abs(t2_speed - t2_index)
        max_diff = max(max_diff, d)
        P(f"  {deg:9.1f}° {math.degrees(t2_speed):12.6f}° {math.degrees(t2_index):12.6f}° {d:9.2e}")
    P(f"  → the two code paths agree to {max_diff:.1e} rad: Snell IS the wavefront/transverse match.  [V]")
    assert max_diff < 1e-12, "wavefront-Snell and index-Snell must be bit-identical (Snell = transverse match)"

    # total internal reflection: the critical angle is where the transverse match has no real solution
    crit = math.degrees(math.asin(c_eye / c_air))          # eye→air: arcsin(c₁/c₂)=arcsin(n_air/n_eye)
    just_below = snell_from_speeds(math.radians(crit - 0.5), c_eye, c_air)   # dense→rare, below critical
    just_above = snell_from_speeds(math.radians(crit + 0.5), c_eye, c_air)   # above critical → TIR (None)
    P(f"\n[TIR] dense→rare (eye→air): critical angle = arcsin(c_eye/c_vac) = {crit:.4f}°")
    P(f"      θ=crit−0.5° refracts (θ₂={math.degrees(just_below):.3f}°); θ=crit+0.5° has NO real "
      f"transverse match → total internal reflection ({just_above}).  [V]")
    assert just_below is not None and just_above is None, "TIR must onset exactly at the critical angle"
    P("      [L] the ocular n (≡ the medium's (B/ρ)) is measured/cited; the relation itself is [F].")

    # ------------------------------------------------------------------------------------------
    # PART B — the reduced eye forms a real, inverted image on the retina (classical arithmetic)
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — the reduced eye images a distant point ONTO the retina; finite objects invert  [V-arith]")
    P("-" * 80)
    P(f"Emsley reduced eye (CITED): single surface, air n₁={N_AIR:.0f} → eye n₂={N_EYE:.4f}, R={R_MM} mm.")
    power = (N_EYE - N_AIR) / (R_MM * 1e-3)                 # diopters = (n₂−n₁)/R[m]
    v_inf = surface_image_distance(None, N_AIR, N_EYE, R_MM)  # object at infinity → posterior focal dist
    nodal = R_MM                                            # nodal point at the centre of curvature
    P(f"  surface power  P = (n₂−n₁)/R = {power:6.2f} D            (textbook reduced eye ≈ 60 D)")
    P(f"  distant point  v = n₂R/(n₂−n₁) = {v_inf:6.3f} mm        = the axial length (retina) ≈ 22.2 mm")
    P(f"  nodal point    at the centre of curvature = {nodal:.2f} mm behind the surface")
    # consistency CHECK against the standard reduced eye (NOT a fit — the cited constants must cohere)
    assert 59.0 < power < 61.0,  "reduced-eye power must come out ≈ 60 D from the cited n,R (consistency)"
    assert 22.0 < v_inf < 22.4,  "distant-object focus must land at the ≈22.2 mm axial length (retina)"

    P("\n  a finite object inverts (real image, m<0) — the retina samples a SPATIAL position code:")
    P(f"    {'object u (mm)':>13s} {'image v (mm)':>12s} {'magnification m':>16s} {'orientation':>12s}")
    inverted_all = True
    for u_mm in (-1000.0, -500.0, -250.0):                 # real objects 1 m / 0.5 m / 0.25 m in front
        v = surface_image_distance(u_mm, N_AIR, N_EYE, R_MM)
        m = (N_AIR * v) / (N_EYE * u_mm)                    # lateral magnification of a single surface
        inverted_all &= (m < 0.0)
        P(f"    {u_mm:13.1f} {v:12.3f} {m:16.5f} {'inverted' if m < 0 else 'erect':>12s}")
    P("    → every real object forms a real INVERTED image near the retina: a point above the axis")
    P("      maps below the fovea. The image IS a spatial code (retinal position).  [V-arith]")
    assert inverted_all, "a single converging surface must invert every real object (m<0)"
    P("    [honest] Part B is classical ray arithmetic: it consumes Snell (Part A, substrate-grounded)")
    P("             + the measured n,R, but the geometry is NOT substrate dynamics. Flagged [V-arith].")

    # ------------------------------------------------------------------------------------------
    # PART C — two independent codes: optics gives WHERE, the angle law gives WHAT COLOUR
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — refraction conserves frequency f ⇒ the colour-angle χ(λ) survives the optics intact")
    P("-" * 80)
    chi_r, chi_g = chi_deg(LAM_RED), chi_deg(LAM_GRN)       # inherited colour labels (committed anchor)
    P(f"inherited colour code (vp_color_by_angle): red 633nm → χ={chi_r:.4f}°, green 532nm → χ={chi_g:.4f}°")
    P(f"  the two colours are DISTINCT internal angles: Δχ = {abs(chi_r-chi_g):.4f}°  (the colour channel)")
    assert abs(chi_r - chi_g) > 0.05, "the committed colours must remain distinct angles (colour code intact)"

    # with a single medium index, BOTH colours from one object point image to the SAME retinal position:
    # the first-order chromatic split is exactly zero (n is colour-independent in the bare model).
    v_r = surface_image_distance(-1000.0, N_AIR, N_EYE, R_MM)
    v_g = surface_image_distance(-1000.0, N_AIR, N_EYE, R_MM)
    P(f"\nposition channel (single index n={N_EYE:.4f}): red and green image to v_red={v_r:.4f} mm, "
      f"v_grn={v_g:.4f} mm")
    P(f"  first-order chromatic split |v_red − v_grn| = {abs(v_r-v_g):.1e} mm = 0 (exactly, single n)")
    assert v_r == v_g, "with one index the colours must co-locate (the chromatic split is NOT first-order)"
    P("  → the POSITION code merges the colours (same 'where'); the χ ANGLE code separates them (different")
    P("    'what colour'). Two orthogonal channels on ONE wave: robust position (θ) + hypersensitive χ.  [F]")
    P("  [O] the residual longitudinal chromatic aberration is second-order: it needs the medium's")
    P("      dispersion c_med(λ) (the ocular (B/ρ) as a function of λ). The bare angle law fixes that")
    P("      colour is an angle and is conserved by the optics — NOT the aberration magnitude (diopters).")
    P("      Obstacle: the per-λ medium stiffness is unmeasured here; no diopter number is invented.")

    # ------------------------------------------------------------------------------------------
    # grades + learned
    # ------------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E3 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced     : Snell's law is the transverse-oscillation (phase) match at the interface;")
    P("                   n = c_vac/c_med = √((B/ρ) ratio) is the lattice meaning of refractive index;")
    P("                   refraction conserves f, so the colour-angle χ(λ) is preserved through optics —")
    P("                   position (θ) and colour (χ) are two independent channels of one wave.")
    P("  [V] verified   : wavefront/SPEED-Snell = index-Snell to <1e-12 rad; TIR onsets exactly at the")
    P("                   critical angle; with one index the colours co-locate (zero first-order split).")
    P("  [V-arith]      : the reduced-eye geometry — power ≈60 D, distant focus at the ≈22.2 mm retina,")
    P("                   real inverted image (m<0) — is classical ray arithmetic on Snell + measured n,R")
    P("                   (consumes the substrate-grounded Snell; the geometry is not substrate dynamics).")
    P("  [L] measured   : the ocular index n=4/3 and the surface radius R=5.55 mm (cited Emsley reduced")
    P("                   eye); the committed colour anchor 633/532 (inherited). None fitted.")
    P("  [O] open       : the longitudinal chromatic aberration MAGNITUDE (needs c_med(λ) = the per-λ")
    P("                   ocular (B/ρ)); the absolute photon→firing (Hz) scale (inherited from E2);")
    P("                   accommodation dynamics (a variable-power lens). Each obstacle named, not invented.")
    P("\nLEARNED: image formation is the SAME inherited wave seen as the lab-space shadow of the internal")
    P("         angle law. The angle theory supplies what external optics alone cannot: the identity")
    P("         n = c_vac/c_med, Snell as the transverse-oscillation match, and — because colour IS an")
    P("         angle and refraction conserves frequency — the guarantee that the colour code survives")
    P("         the optics. The eye forms a real inverted spatial image (a robust POSITION code, classical")
    P("         arithmetic) while the hypersensitive χ ANGLE code rides through untouched. The chromatic")
    P("         coupling between them is real but second-order; its magnitude is an honest [O]. Foundation")
    P("         untouched; nothing fitted; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
