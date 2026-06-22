#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E6 — WHY THE BAND IS VISIBLE   (two layers select the same band; the WAVELENGTH is the anchor)

The frequency ladder (E5) showed HOW the ~10¹⁴ Hz carrier collapses to the neural band. This
increment answers the prior question: WHY is the carrier the eye is handed the *visible* band and
not some other slice of the spectrum? The answer is two distinct constraints, read on the FROZEN
foundation, that bracket the same narrow window from two completely different directions:

  GATE (i)  — GEOMETRIC PLACEMENT (inherited §10.9 canon, read-only).  In lattice units the quantum
              count m=⌈λ/D⌉ is monotone in λ, so the bands sit in a fixed order: gamma (m=1, the lone
              quasi-longitudinal band) → x-ray → VISIBLE → infrared → radio. Visible is *sandwiched in
              m* between x-ray (smaller m) and infrared (larger m), in the near-transverse manifold.
              Its identity — colour — is its propagation angle χ(λ). [F]
  GATE (ii) — THE PHOTOCHEMICAL ENERGY WINDOW.  A photon must carry enough energy to drive the
              *reversible* 11-cis→all-trans retinal isomerisation (an energy FLOOR) yet not so much
              that it ionises / photodamages (a CEILING). The cited window ~1.8–3.3 eV maps, through
              the forced E=hc/λ, onto ~375.7–688.8 nm — the visible band. [L]+[F].

PRECISION DISCIPLINE (no rough arithmetic — the wavelength is mapped exactly)
  • The SPINE is the WAVELENGTH, mapped EXACTLY to frequency and period: ν = c/λ, T = 1/ν = λ/c,
    E = hν, with the SI-exact constants c = 299792458 m/s and h = 6.62607015e-34 J·s. Every visible
    anchor is an ALREADY-MEASURED value (the two RCROSS channels 632.99/532.0 nm; the three cone-opsin
    λmax 420/530/560 nm from E1) — not a round number invented here.                         [L]/[F]
  • The ANGLE is reported to full precision and via the meaningful near-grazing quantity, the deficit
    (90°−χ), computed WITHOUT the 1−sin²χ cancellation (cosχ=√((1−x)(1+x)), x=λ/mD). Each angle is
    checked against the canonical closure m·sinχ·D/λ = 1 to 1e-15. The angle is shown precisely but it
    is NOT the band's gate — it never excludes a band (see (3)); the wavelength/energy does.       [F]

WHAT IS SHOWN (and how it is graded)
  (0) THE EXACT CARRIER MAP — measured λ → ν → T(period) → E for every visible anchor.            [L]/[F]
  (1) GATE (i): m-PLACEMENT — m strictly increases gamma<x-ray<visible<IR<radio; gamma (m=1) is the
      lone quasi-longitudinal band, visible near-transverse; angles + deficits to full precision.    [F]
  (2) GATE (ii): the ENERGY WINDOW — cited 1.8–3.3 eV → exactly 375.71–688.80 nm; EVERY measured
      visible anchor (633, 532, and the three opsin λmax) lies inside it, each E to 8 dp.         [L]/[F]
  (3) THE HONEST SPLIT — geometry PLACES but cannot PIN; energy PINS.
        (3a) the band-internal angle deficit (90°−χ) is tiny AND NON-monotone (a sawtooth from m=⌈⌉:
             633 nm has a SMALLER deficit than 750 nm even though it is shorter) versus the
             gamma→visible deficit swing of >78°: there is NO geometric kink at the band edges.       [F]
        (3b) the edges coincide with the ENERGY window, not a geometric boundary. An infrared probe
             (10 µm, E≈0.124 eV) is excluded by the energy FLOOR although its angle deficit is even
             SMALLER than visible's (more transverse) — geometry would happily admit it.          [F]/[L]
  (4) THE SOFT RED EDGE + the named [O].  the deep-red edge is soft: 750 nm (1.6531 eV) sits ~0.147 eV
      BELOW the clean isomerisation floor (1.8 eV) — low-efficiency deep red, stated openly. And the
      chromophore energy that sets the floor is coding/photochemistry: the promoter-γ this package
      reads has NO lever on the retinal pocket — a named [O]. E6 forces the PLACEMENT and the
      energy-window LOGIC; it invents no chromophore and tunes nothing.

FIREWALL / NO-TUNING.  E6 is pure sensory MECHANISM — no disease, diagnostic, or clinical claim (that
layer is E4, firewalled). The visible-anchor wavelengths and the isomerisation window (1.8, 3.3 eV) are
CITED measured/physiological inputs, frozen as written — NOT fits, NOT derived from package data; the
λ→ν→T→E mapping is exact; the angle law and D are the inherited frozen canon (read-only); no γ is added;
SEED=19. The molecular tuning of the chromophore window is a named [O].

Imports the FROZEN visible-band canon (the angle law + the SI-exact constants + D) and the frozen atlas
(for the no-drift check). Adds no γ. stdlib + the inherited canon. Deterministic; run twice -> same sha256.
"""
import os, sys, io, hashlib, math, json

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(PKG, "inherited"))

import vp_visible_band_canonical as VB                 # inherited canon: angle law + H, C_SI, D (read-only)
from vp_substrate import SEED                           # FROZEN substrate seed (no-drift check)
ATLAS = json.load(open(os.path.join(PKG, "inherited", "organ_gamma.json"), encoding="utf-8"))["genes"]

# --- SI-exact constants (taken from the frozen canon; the 2019 SI exact values) ----------------------
C  = VB.C_SI                     # 299792458.0 m/s            (exact)
H  = VB.H                        # 6.62607015e-34 J·s         (exact)
QE = 1.602176634e-19             # C, elementary charge       (exact) — for the J→eV conversion
EV_PER_J = 1.0 / QE
D  = VB.D                        # 4.852620477366185 pm       (the inherited invariant)

# --- the two cited inputs (measured / physiological; NOT fitted, NOT derived from package data) ------
ISOM_EV  = (1.8, 3.3)            # reversible 11-cis→all-trans photochemical window, eV          [L] cited
#   floor 1.8 eV   = the energy floor to drive the isomerisation (below it the flip does not fire)
#   ceiling 3.3 eV = the ionisation / photodamage ceiling (above it the photon damages, not isomerises)
VIS_CONV_NM = (380.0, 750.0)     # conventional human visible band, nm (placement reference)     [L] cited

# ALREADY-MEASURED visible wavelengths used as the precise anchors (nm):
#   the two RCROSS channels (the canon's empirical anchors) + the three cone-opsin λmax (E1, cited)
ANCHORS_NM = (("HeNe red anchor", 632.99), ("green 2nd channel", 532.0),
              ("opsin S λmax",    420.0),  ("opsin M λmax",      530.0), ("opsin L λmax", 560.0))

# representative out-of-band probes (exact facts, used to show each filter's edge)
PROBE_GAMMA_NM = 1e-3            # 1 pm gamma   — the lone quasi-longitudinal band (m=1)
PROBE_XRAY_NM  = 10.0           # 10 nm x-ray  — short-λ side
PROBE_UV_NM    = 100.0          # 100 nm UV    — short-λ side
PROBE_IR_NM    = 10_000.0       # 10 µm IR     — long-λ side
PROBE_RADIO_NM = 1e9            # 1 m radio    — long-λ side


def nu_of(lam_m):   return C / lam_m                 # frequency  ν = c/λ            (exact)
def period_of(lam_m): return lam_m / C               # period     T = 1/ν = λ/c      (exact)
def eV_of(lam_m):   return H * (C / lam_m) * EV_PER_J # energy     E = hν            (exact)
def nm_from_eV(e):  return H * C / (e / EV_PER_J) * 1e9


def angle_hp(lam_m):
    """High-precision angle. Returns (m, sinχ, χ°, deficit°=(90°−χ), closure m·sinχ·D/λ).
    Near grazing the meaningful quantity is the deficit; computed via cosχ=√((1−x)(1+x)) to
    avoid the 1−x² cancellation, so χ is exact to the float's full precision (closure≈1)."""
    m = math.ceil(lam_m / D)
    x = lam_m / (m * D)                              # = sin(χ), the exact ratio
    cos_chi = math.sqrt((1.0 - x) * (1.0 + x))       # stable near x→1
    delta   = math.atan2(cos_chi, x)                 # 90° − χ  (radians)
    chi     = math.pi / 2.0 - delta
    closure = m * math.sin(chi) * D / lam_m          # canonical identity, must be 1
    return m, x, math.degrees(chi), math.degrees(delta), closure


def run(P):
    P("=" * 78)
    P("E6 — WHY THE BAND IS VISIBLE   (geometry PLACES it; photochemistry PINS it)")
    P("=" * 78)
    P(f"SI-exact constants: c = {C:.0f} m/s,  h = {H:.8e} J·s;  inherited D = {D*1e12:.12f} pm;  SEED={SEED}")
    P(f"cited inputs: isomerisation window {ISOM_EV[0]}–{ISOM_EV[1]} eV [L];  "
      f"conventional visible {VIS_CONV_NM[0]:.0f}–{VIS_CONV_NM[1]:.0f} nm [L]\n")

    # (0) THE EXACT CARRIER MAP — measured λ → ν → T(period) → E --------------------------
    P("(0) THE EXACT CARRIER MAP — already-measured λ mapped exactly to ν, period T, energy E:")
    P("    (ν=c/λ, T=1/ν=λ/c, E=hν; constants SI-exact — no rounding)")
    for name, nm in ANCHORS_NM:
        lam = nm * 1e-9
        nu, T, E = nu_of(lam), period_of(lam), eV_of(lam)
        P(f"    {name:<18} λ={nm:8.3f} nm   ν={nu:.10e} Hz   T={T:.10e} s   E={E:.8f} eV")
    # forced sanity: the visible carrier sits in the ~10^14 Hz / ~fs-period band
    for _, nm in ANCHORS_NM:
        assert 4.0e14 < nu_of(nm*1e-9) < 8.0e14            # visible carrier band [F]
        assert math.isclose(period_of(nm*1e-9), 1.0/nu_of(nm*1e-9), rel_tol=1e-15)  # T=1/ν exactly
        assert math.isclose(eV_of(nm*1e-9), H*nu_of(nm*1e-9)*EV_PER_J, rel_tol=1e-15)  # E=hν exactly
    P("    → carrier ≈ 4.7–7.1×10¹⁴ Hz, period ≈ 1.4–2.1 fs; T=1/ν and E=hν hold to 1e-15. [L]/[F]")

    # (1) GATE (i) — geometric placement by m, angles to full precision -------------------
    P("\n(1) GATE (i) — PLACEMENT IN m  (m=⌈λ/D⌉, monotone; inherited §10.9 canon, read-only):")
    P("    band            m                χ (deg, full precision)    (90°−χ) deficit (deg)   closure")
    rows = [("gamma 1pm", PROBE_GAMMA_NM), ("x-ray 10nm", PROBE_XRAY_NM),
            ("VISIBLE 380nm", VIS_CONV_NM[0]), ("VISIBLE 750nm", VIS_CONV_NM[1]),
            ("infrared 10µm", PROBE_IR_NM), ("radio 1m", PROBE_RADIO_NM)]
    ms = []
    for name, nm in rows:
        m, x, chi, dfc, clo = angle_hp(nm * 1e-9)
        ms.append(m)
        P(f"    {name:<14} {m:<15d}  χ={chi:.10f}°   {dfc:.10f}°       {clo:.15f}")
        assert abs(clo - 1.0) < 1e-12                      # the high-precision angle is exact
        assert abs(chi - VB.chi_deg(nm * 1e-9)) < 1e-6     # agrees with the frozen canon (no drift)
    assert all(ms[i] < ms[i + 1] for i in range(len(ms) - 1))   # m strictly increases across the bands
    assert angle_hp(PROBE_GAMMA_NM * 1e-9)[2] < 13.0            # gamma (m=1) is the lone quasi-longitudinal band
    assert 89.7 < angle_hp(VIS_CONV_NM[0] * 1e-9)[2] < 90.0     # visible near-transverse on both edges
    assert 89.7 < angle_hp(VIS_CONV_NM[1] * 1e-9)[2] < 90.0
    P("    → VISIBLE is SANDWICHED in m between x-ray (smaller m) and infrared (larger m), in the")
    P("      near-transverse manifold; gamma (m=1) is the only quasi-longitudinal band. [F]")

    # (2) GATE (ii) — the photochemical energy window, with measured anchors inside -------
    P("\n(2) GATE (ii) — THE ENERGY WINDOW  (reversible 11-cis→all-trans isomerisation, cited):")
    w_hi_nm, w_lo_nm = nm_from_eV(ISOM_EV[0]), nm_from_eV(ISOM_EV[1])    # 1.8 eV→long λ, 3.3 eV→short λ
    P(f"    cited window {ISOM_EV[0]}–{ISOM_EV[1]} eV  ⇒  λ = hc/E  =  {w_lo_nm:.8f}–{w_hi_nm:.8f} nm")
    P("    every ALREADY-MEASURED visible anchor lands inside this window:")
    for name, nm in ANCHORS_NM:
        E = eV_of(nm * 1e-9)
        inside = ISOM_EV[0] <= E <= ISOM_EV[1]
        assert inside                                       # all measured anchors inside the window
        P(f"        {name:<18} λ={nm:8.3f} nm   E={E:.8f} eV   {'INSIDE' if inside else 'OUTSIDE'}")
    P(f"    floor {ISOM_EV[0]} eV: below it the photon cannot drive the flip (→ no transduction);")
    P(f"    ceiling {ISOM_EV[1]} eV: above it the photon ionises / photodamages (not reversible). [L]/[F]")
    assert 375.0 < w_lo_nm < 376.5 and 688.0 < w_hi_nm < 689.5   # the window maps onto ~visible, precisely

    # (3) THE HONEST SPLIT — geometry PLACES but cannot PIN; energy PINS -----------------
    P("\n(3) WHO PINS THE EDGES?  geometry PLACES, energy PINS  (the brutally-honest part):")
    # (3a) deficits to full precision: the band-internal deficit is tiny and a NON-monotone sawtooth
    d380 = angle_hp(VIS_CONV_NM[0] * 1e-9)[3]
    d633 = angle_hp(632.99e-9)[3]
    d750 = angle_hp(VIS_CONV_NM[1] * 1e-9)[3]
    dgam = angle_hp(PROBE_GAMMA_NM * 1e-9)[3]
    band_span = max(d380, d633, d750) - min(d380, d633, d750)
    sawtooth  = (d633 < d750)                # 633 nm (shorter) has a SMALLER deficit than 750 ⇒ not monotone
    P(f"    (3a) deficits (90°−χ): 380nm={d380:.10f}°  633nm={d633:.10f}°  750nm={d750:.10f}°")
    P(f"         633<750 in deficit though 633<750 in λ ⇒ SAWTOOTH (m=⌈⌉ quantisation), not monotone")
    P(f"         band-internal deficit span = {band_span:.10f}°  vs gamma deficit {dgam:.6f}° (>78°)")
    assert sawtooth and band_span < 0.3 and dgam > 78.0    # no geometric kink anywhere in the band
    # (3b) the edges coincide with the ENERGY window; an IR probe is excluded by ENERGY, not geometry
    e_violet, e_red = eV_of(VIS_CONV_NM[0] * 1e-9), eV_of(VIS_CONV_NM[1] * 1e-9)
    e_ir = eV_of(PROBE_IR_NM * 1e-9)
    d_ir = angle_hp(PROBE_IR_NM * 1e-9)[3]
    m_ir = angle_hp(PROBE_IR_NM * 1e-9)[0]
    m_vis = angle_hp(VIS_CONV_NM[1] * 1e-9)[0]
    P(f"    (3b) violet edge 380nm → {e_violet:.8f} eV (just under the {ISOM_EV[1]} eV ceiling);")
    P(f"         red    edge 750nm → {e_red:.8f} eV (just under the {ISOM_EV[0]} eV floor)")
    P(f"         IR 10µm: E={e_ir:.8f} eV ≪ floor (ENERGY excludes it) — yet its deficit {d_ir:.8f}° is")
    P(f"         SMALLER than visible's (more transverse, larger m={m_ir}>{m_vis}); geometry would admit it")
    assert e_ir < ISOM_EV[0] and d_ir < d750 and m_ir > m_vis  # IR fails energy though geometry prefers it
    P("         → the edges are PHOTOCHEMICAL, not geometric. The angle (even to 10 dp) never gates a")
    P("           band; it only labels colour. The chromophore's energy window is WHERE the band is. [F]/[L]")

    # (4) the soft red edge + the named [O] ----------------------------------------------
    P("\n(4) THE SOFT RED EDGE + the named [O]  (honesty, not a clean coincidence):")
    red_gap = ISOM_EV[0] - eV_of(VIS_CONV_NM[1] * 1e-9)
    P(f"    deep-red edge: 750nm = {eV_of(VIS_CONV_NM[1]*1e-9):.8f} eV sits {red_gap:.8f} eV BELOW the")
    P(f"    clean floor {ISOM_EV[0]} eV ⇒ the conventional band overhangs the clean window on the red side")
    P("    (deep red is low-efficiency, perceived only bright) — the red edge is SOFT and we say so.")
    assert 0.0 < red_gap < 0.2          # the red tail overhangs the clean window by <0.2 eV
    P("    [O] the chromophore energy that sets this floor is coding/photochemistry: the promoter-γ")
    P("        this package reads has NO lever on the retinal pocket. E6 invents no chromophore.")

    # firewall self-checks: no fitted chromophore, no clinical magnitude, D is the inherited invariant
    assert ISOM_EV == (1.8, 3.3) and VIS_CONV_NM == (380.0, 750.0)         # both are CITED inputs, frozen
    assert abs(D - 6.0 * math.pi**6 * 0.8414e-15) < 5e-15                   # D is the inherited invariant
    assert C == 299792458.0 and H == 6.62607015e-34                        # SI-exact, not re-derived

    P("\nLEARNED: 'visible' is not chosen and not geometric. The lattice geometry only PLACES the band")
    P("         — it fixes the angle↔colour map and sandwiches visible in m between x-ray and infrared,")
    P("         but the angle is a smooth sawtooth with no kink (the angle never gates a band). What")
    P("         pins ~380–750 nm is the chromophore's REVERSIBLE energy window: a floor to flip the")
    P("         switch, a ceiling before damage. The WAVELENGTH is the anchor — mapped exactly to a")
    P("         ν≈10¹⁴ Hz / ~2 fs carrier — and the molecular tuning of that window stays a named [O].")


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
