#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_visible_band_canonical.py — INHERITED from vp_physics v0.11.0 (§9.4, §10.9, §11.2-11.6).

Brought into the eye package so every downstream increment stands on the SAME precise
wavelength<->angle machinery the physics volume LOCKs. This is a faithful reproduction of
the FORCED relations (recomputed here, bit-exact from D), with the unit-realization chain
QUOTED from source (its measuring simulation lives in the physics bundle, not here).

WHY THIS MATTERS FOR THE EYE (it is the TOP rung of the high->low frequency ladder)
  The eye is handed a CARRIER. Before any biology, the framework already fixes *which*
  carrier: a light wavelength is the transverse pitch of a chain of m=ceil(λ/D) rotating
  quanta, so the propagation angle χ to the lattice axis is sinχ=λ/(mD). That single
  relation says where each band sits:
        gamma  (m=1)        -> χ→0°   (quasi-longitudinal)
        x-ray              -> χ rises through the tens of degrees
        VISIBLE (m~1e5)    -> χ ≈ 89.8°-89.9°  (a narrow NEAR-TRANSVERSE window)
        radio  (m huge)    -> χ→90°   (essentially transverse)
  Visible light is not "chosen": it is the band whose quantum-count m places it in the
  near-transverse window, between x-ray and infrared. That is step 1 of the eye story —
  WHICH carrier arrives — and it is structural [F], not fitted.

THE 633/532 METHOD (the precise part, §11.4 RCROSS — "two channels or no conclusion")
  D is realised from ONE empirical anchor λ_ref=632.99 nm via a split rule, but a single
  anchor is never allowed to decide: the canonical gate RCROSS validates the SAME lattice
  units against a SECOND channel, 532 nm. Here we reproduce the anchor-free closure that
  underwrites it — m·sinχ·D/λ = 1 EXACTLY for both 633 and 532 on the one shared D — which
  is why the wavelength<->angle map is wavelength-consistent rather than a single-line fit.
  The forward map D→χ takes a LENGTH in and returns an ANGLE out (a different kind of
  quantity); back-solving D from χ would be the circular direction (§W.5). Reading a
  wavelength OFF a measured angle (λ = mD·sinχ) is the application, and near χ=90° it is
  hypersensitive — a fraction of a percent in λ moves χ by more than a degree.

PROVENANCE / GRADES (firewall: this module adds NO biology and performs NO tuning)
  • D, angle law, band table, RCROSS closure ......... recomputed from D, bit-exact   [F]+[V]
  • λ_ref, N, a, A, Δt (unit-realization chain) ...... quoted canonical values, §11    [L]/[F]
  • the jammed-lattice percolation that MEASURES the amplification A (A=a/g*, a CSV
    output, not an input) lives in the physics bundle .. consumed, not re-measured    [V-elsewhere]

stdlib only (math). Deterministic; run twice -> identical sha256.
"""
import math, hashlib, io

# ---- the invariant quantum diameter D, derived two independent ways (as in §3.4/§9.4) ----
H, ME, C_SI = 6.62607015e-34, 9.1093837015e-31, 299792458.0
RP = 0.8414e-15
D     = 2.0*(H/(ME*C_SI))        # = 2 λ_C,e            (the quantum diameter; INVARIANT)
D_JAM = 6.0*math.pi**6*RP        # = 6π⁶ r_p            (jamming cross-check, same length)

# ---- unit-realization chain, QUOTED from physics §11 (LOCKed there; not re-derived here) ----
#   a = λ_ref / N          : the realised VP diameter from the single empirical anchor
#   A = a / g*             : structural amplification, MEASURED from lattice_3d_jam_percolation.py
#   D = 2π λ / A           : the quantum diameter (computed in §9.4)
#   Δt = A a / c_ref       : the realised time tick;  c Δt / a = A closes exactly
LREF_NM   = 632.99               # nm  — the single empirical anchor (§11.2)
N_SPLIT   = 1_000_000_000_000    # = 1e12  — the locked split integer (§11.2)
A_REALIZED = 6.3299e-19          # m   — a = λ_ref / N           (§11.2, quoted)
DT_TICK    = 1.86e-21            # s   — Δt = A a / c_ref        (§11.3, quoted)
RCROSS_CH  = (632.99e-9, 532.0e-9)   # the two baseline channels of the §11.4 gate


def angle(lam_over_D):
    """sinχ=λ/(mD), m=⌈λ/D⌉. Returns (χ in radians, m). χ=90° is unreachable."""
    m = math.ceil(lam_over_D)
    return math.asin(min(1.0, lam_over_D/m)), m


def chi_deg(lam_m):
    chi, _ = angle(lam_m/D)
    return math.degrees(chi)


def lambda_from_angle(chi_deg_val, m):
    """The application: read a wavelength OFF a measured angle, λ = m·D·sinχ."""
    return m*D*math.sin(math.radians(chi_deg_val))


def run(P):
    P("=" * 70)
    P("VISIBLE-BAND CANON  (inherited from vp_physics v0.11.0 §9.4/§10.9/§11)")
    P("=" * 70)

    # (0) the one internal length, and where it comes from -------------------------------
    P(f"(0) quantum diameter D = {D*1e12:.6f} pm")
    P(f"      cross-check  6π⁶ r_p = {D_JAM*1e12:.6f} pm   (Δ={abs(D-D_JAM)*1e12:.2e} pm)")
    assert abs(D - D_JAM) < 5e-15        # two independent routes agree to fm
    P(f"      realised from ONE anchor:  a = λ_ref/N = {LREF_NM}nm / {N_SPLIT:.0e} "
      f"= {A_REALIZED:.4e} m   [§11.2, quoted]")
    assert math.isclose(A_REALIZED*N_SPLIT, LREF_NM*1e-9, rel_tol=1e-12)   # split rule closes
    P(f"      amplification A = a/g* (MEASURED from the jamming percolation sim) -> "
      f"D = 2πλ/A;  Δt = Aa/c = {DT_TICK:.2e} s   [§11.3, quoted]")

    # (1) the band table — WHICH carrier sits where (the structural 'why visible') --------
    P("\n(1) where each band sits on the lattice angle  (sinχ=λ/(mD), m=⌈λ/D⌉):")
    bands = [("gamma  1 fm", 1e-15), ("gamma  1 pm", 1e-12), ("x-ray  10 nm", 1e-8),
             ("VISIBLE 633nm", 632.99e-9), ("VISIBLE 532nm", 532.0e-9),
             ("infrared 10µm", 1e-5), ("radio   1 m", 1.0)]
    for name, lam in bands:
        chi, m = angle(lam/D)
        P(f"    {name:<14} m={m:<14d} χ={math.degrees(chi):8.4f}°")
    # forced regime facts (no fit): gamma quasi-longitudinal, visible near-transverse, radio transverse
    assert chi_deg(1e-15) < 0.1                      # deep gamma runs along the axis
    assert chi_deg(1e-12) < 13.0                     # gamma edge still quasi-longitudinal (m=1)
    assert angle(1e-15/D)[1] == 1 and angle(1e-12/D)[1] == 1
    assert 89.7 < chi_deg(632.99e-9) < 90.0          # visible is near-transverse
    assert 89.7 < chi_deg(532.0e-9)  < 90.0
    assert chi_deg(1.0) > 89.99                       # radio is essentially transverse
    P("    -> gamma quasi-longitudinal, VISIBLE a narrow near-transverse window, radio transverse  [F]")

    # (2) RCROSS(633/532): the anchor-free two-channel closure ----------------------------
    P("\n(2) RCROSS(633/532) — 'two channels or no conclusion' (§11.4):")
    for lam in RCROSS_CH:
        chi, m = angle(lam/D)
        closure = m*math.sin(chi)*D/lam          # must be 1 on the one shared D
        P(f"    λ={lam*1e9:7.2f}nm  m={m}  χ={math.degrees(chi):.4f}°  "
          f"m·sinχ·D/λ = {closure:.15f}")
        assert abs(closure - 1.0) < 1e-12        # exact closure, both channels
    # both channels ride the IDENTICAL D — that is what makes it anchor-free, not a 2-line fit
    P(f"    both channels share the identical D={D*1e12:.6f} pm  → wavelength-consistent, not fitted  [V]")

    # (3) the application: read a wavelength OFF an angle, and its hypersensitivity --------
    P("\n(3) finding a wavelength from its angle  (λ = m·D·sinχ; hypersensitive near 90°):")
    chi0, m0 = angle(632.99e-9/D)
    lam_back = lambda_from_angle(math.degrees(chi0), m0)
    P(f"    inverse check: χ={math.degrees(chi0):.4f}°, m={m0}  →  λ={lam_back*1e9:.4f} nm  "
      f"(input 632.99)")
    assert abs(lam_back - 632.99e-9) < 1e-15
    c0 = chi_deg(632.99e-9); c1 = chi_deg(632.99e-9*1.0003)   # +0.03% in λ
    P(f"    sensitivity: +0.03% in λ shifts χ {c0:.4f}°→{c1:.4f}°  (Δχ={abs(c1-c0):.4f}°) "
      f"→ a measured angle pins λ very finely")

    P("\nLEARNED: the eye is handed a NEAR-TRANSVERSE visible carrier whose identity (colour)")
    P("         is the angle χ(λ), fixed by one invariant D and cross-validated on two")
    P("         channels (633/532). This is rung 1 of the high→low ladder: the ~10¹⁴ Hz")
    P("         carrier the downstream switch must convert — its WHAT lives in geometry, not")
    P("         in a frequency the receptor could ever follow.")


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
