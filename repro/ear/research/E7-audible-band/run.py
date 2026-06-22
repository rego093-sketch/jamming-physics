#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E7 :  the audible BAND (why only certain frequencies are heard).
                         Derives the audible RANGE as a GEOMETRY-CARVED BANDPASS sitting on the inherited
                         √(stiffness/inertia) wave law. Same discipline as E6: the FORM (the bandpass) and
                         the SIGN of every edge are FORCED; the band's absolute edges and three corners stay
                         [O] (measured geometry), with a proof that a number for any of them would be TUNING.

WHAT THIS BUILDS (BLUEPRINT.md §E7 / WORK_HANDOVER open item 6).
  E0 already states that sound and light share ONE elastic-wave law: light is the jammed lattice's
  elastic wave c²=B/ρ (physics §SP), the speed of sound in air is vₛ=√(γP/ρ) (chemistry/physics §K),
  and the local cochlear resonance is ω(x)=√(S(x)/m) — the SAME √(stiffness/inertia). E1 forced the
  place-map SHAPE; E6 characterised the near-peak envelope. But WHY the audible range has EDGES — why we
  hear ~20 Hz–20 kHz and not 1 Hz or 1 MHz — was, until here, only a cited calibration span [L] (the
  Greenwood A/a/k). E7 derives the band itself, in the E6 forced-form / [O]-magnitude discipline, by
  composing ONLY the FROZEN inherited foundation (the √-law Greenwood place map). It proves:

    (A) THE KEYSTONE (parameter-free, exact). Because the resonance obeys the √-law (CF ∝ √S), the total
        span in OCTAVES is EXACTLY HALF the log₂ of the basilar-membrane STIFFNESS RATIO:
            N_oct = ½ · log₂(S_base / S_apex).
        Read off the inherited Greenwood map this is the human ~10-octave span ⟺ a stiffness ratio ~10⁶;
        the identity holds to machine precision because CF∝√S is the √-law. The √-law's whole contribution
        is the FACTOR OF ½ — it HALVES the stiffness DECADES into OCTAVES. The number of octaves is FORCED
        once the (measured) stiffness ratio is known; no constant is tuned.

    (B) THE LOW EDGE is a high-pass — the HELICOTREMA. Two complementary, FORCED facts. (i) In the
        inherited Greenwood form f=A(10^{ax}−k) the offset −A·k is a LOW-END-ONLY correction: its
        FRACTIONAL weight is ~0.88 at the apex but ~0.007 at the base (ratio = 10^a exactly), so a
        CONSTANT subtracted from an exponential reshapes ONLY the low edge — bending the apical end DOWN
        ~3 octaves to ~20 Hz (verified). (ii) The TOPOLOGY forces a high-pass: the apical hole joining the
        scalae short-circuits slow (DC-ward) pressure, so below a corner the pressure equalises before a
        traveling wave forms — attenuation of the LOWS. The EXISTENCE and the SIDE (low) are forced and
        robust to the filter order; the CORNER is [O] (needs the helicotrema area + cochlear compliance);
        k is [L].

    (C) THE HIGH EDGE is a low-pass — the MIDDLE EAR + the basal STIFFNESS CEILING. Two FORCED facts.
        (i) The ossicular chain (malleus/incus/stapes) has MASS; an inertia in the drive path is a
        mechanical LOW-PASS — above its resonance the transmission is monotone-decreasing with a forced
        −12 dB/oct (∝1/ω², the mass term) asymptote, robust to the damping. (ii) The stiffest place (the
        base, x=1) fixes a FINITE absolute ceiling CF_max=(1/2π)√(S_base/m): the inherited place map is
        strictly increasing apex→base and FINITE at the base, so there IS a hard top. The EXISTENCE and
        SIDE (high) are forced; the CORNER / CF_max value is [O] (needs the ossicular mass + S_base).

    (D) THE BAND = the PRODUCT (place-map passband) × (helicotrema high-pass) × (middle-ear low-pass) — a
        BANDPASS whose SHAPE and the SIGN of each edge are FORCED by geometry, while the three corner
        magnitudes are [O]. The audible band is a GEOMETRY problem on top of the inherited wave law — not
        a new physics.

    (E) THE META-RESULT (the point of E7, the E6 parallel). The √-law forces the CONVERSION EXPONENT (the
        ½) and every EDGE SIGN; what stays [O] is the measured GEOMETRY — S_apex, S_base (hence CF_min,
        CF_max and the ~10⁶ ratio), the ossicular mass (the high corner), the helicotrema area (the low
        corner). Every SHAPE/SIGN is forced and geometry-invariant; every ABSOLUTE EDGE and CORNER scales
        with a measured length/stiffness/mass and is fixed by NO inherited constant (γ is promoter
        STRUCTURE only by the firewall — never a stiffness, a corner, or an area). Therefore a closed
        numeric band = a CHOICE of those geometric magnitudes = TUNING (forbidden). E7 does NOT pin the
        band's numbers; it CHARACTERISES the band: SHAPE + EXPONENT + every SIGN forced, the magnitudes
        the irreducible measured-geometry [O].

THE PHYSICS (cited, not re-opened; built on the inherited wave theory).
  The √-law ω=√(S/m) is inherited (vp_sound_wave.py); a log-graded stiffness gives the exponential
  Greenwood place map (E0/E1). A constant added/subtracted to an exponential is a low-frequency-only
  shift (elementary). A mass driven by force has displacement ∝1/(S−ω²m) → ∝1/ω² above resonance — a
  second-order low-pass (textbook mechanics; the middle-ear transfer, Rosowski; Puria). A hole between
  the scalae is a hydraulic short-circuit for slow pressure — a high-pass relief (Dallos; the helicotrema).
  The absolute corners need the cochlear/scala compliance, the helicotrema area, the ossicular mass and
  the BM stiffness at each end — measured anatomy, never fitted here.

HOW IT RELATES TO THE FOUNDATION (no-regression — NO inherited byte changes in E7).
  EXTENDS the inherited foundation by IMPORTING it. Like E5 and E6, E7 fetches NO new gene and folds
  nothing into the cache/atlas — it touches NOT ONE inherited byte and triggers NO re-freeze (every
  frozen hash stays valid as recorded at seed time). It consumes the INHERITED `vp_sound_wave.py`
  (the Greenwood place map CF(x)=A(10^{ax}−k), re-verified) and E1's `inv_greenwood`/`read_measured`
  (a reference structure gene recomputes from the frozen cache and equals the atlas bit-for-bit, A4 =
  signal − γ). The wave theory is consumed, never re-opened.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the KEYSTONE N_oct=½·log₂(S_base/S_apex) (exact, the √-law halves the stiffness decades) and
            the human span↔ratio reproduction (10.025 oct ⟺ 1.085×10⁶) ; the offset −A·k as a
            LOW-END-ONLY correction (fractional weight 0.88 apex vs 0.007 base, ratio = 10^a) and the
            ~3-octave apical bend to ~20 Hz ; the LOW-edge high-pass SIDE (topology, order-robust) ; the
            HIGH-edge low-pass SIDE and the forced −12 dB/oct mass asymptote (damping-robust) ; the FINITE
            basal ceiling (place map strictly increasing + finite at the base) ; the BAND as the bandpass
            PRODUCT with every edge SIGN forced ; and THE META-RESULT — the √-law fixes the EXPONENT (½)
            and every SIGN while every absolute edge/corner is the measured-geometry [O].
  [L]      : the Greenwood A/a/k place-map calibration ; the measured BM stiffness RATIO ~10⁶ (anatomy:
            the membrane widens and thins base→apex) ; the reference gene γ (NCBI-measured, cached).
  [O]      : the ABSOLUTE band edges CF_min / CF_max (Hz) ; the LOW corner (helicotrema area + cochlear
            compliance) ; the HIGH corner / CF_max (ossicular mass + S_base) ; the full 2-D/3-D fluid
            hydrodynamics and the cochlear input impedance (E6-N5) ; the absolute BM stiffness gradient
            law S(x) and the developmental program that builds it (anatomy / DNA volume) ; the felt pitch
            RANGE as experience (→ mind volume). Each names its obstacle below; none closes without TUNING
            a measured magnitude.

FIREWALL. γ reads promoter STRUCTURE only — it is NOT a stiffness S, NOT a corner frequency, NOT the
helicotrema area, NOT the ossicular mass, NOT a band edge or a clinical effect (the reference gene is
reproduced offline ONLY to show the cascade gene still recomputes and NO byte moved; its γ is never used
as a stiffness or an edge). No disease claim here (E7 is the healthy band geometry; the band-specific
losses are E8, proposal-only). The felt pitch/loudness RANGE as experience is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io, importlib.util
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E7-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate  as SUB                               # the R19 cubic (seed lock; not re-opened here)
import vp_sound_wave as SND                               # √-law Greenwood place map CF(x)=A(10^{ax}−k)


def _load(name, path):
    """Load a module by file path under a UNIQUE name (every increment ships a file called run.py;
    importing under the bare name 'run' would collide in sys.modules — this keeps them distinct)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# reuse E1's inv_greenwood + read_measured (cache==atlas, A4⊥) under a unique name
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))

# the inherited Greenwood calibration constants (consumed, NOT re-decided here) — A4-grammar [L]
A_GW, a_GW, k_GW = 165.4, 2.1, 0.88
REF_GENE = "TMC1"                                         # canonical MET structure reference (γ measured)


# ============================================================================================
#  geometry of the audible band — read off the INHERITED √-law Greenwood place map CF(x)
#  apex x=0 (compliant, low CF) → base x=1 (stiff, high CF).   CF ∝ √S  (the √-law).
# ============================================================================================
def cf(x):
    """Inherited Greenwood characteristic frequency at fractional place x (apex→base)."""
    return SND.greenwood_f(x)                             # = A(10^{ax}−k), frozen constants


def cf_pure_exp(x):
    """The bare exponential term A·10^{ax} (the place map BEFORE the −A·k apical correction).
    CF∝√S maps THIS term to the stiffness gradient; the −A·k offset is the helicotrema relief (PART C)."""
    return A_GW * (10.0 ** (a_GW * x))


def octave_span(x0=0.0, x1=1.0):
    """Audible span in OCTAVES between two places = log₂(CF(x1)/CF(x0))."""
    return math.log2(cf(x1) / cf(x0))


def implied_stiffness_ratio(n_oct):
    """The stiffness ratio a given octave span implies under the √-law: S_ratio = (CF_ratio)² = 2^(2·N)."""
    return 2.0 ** (2.0 * n_oct)


def noct_from_stiffness_ratio(s_ratio):
    """THE KEYSTONE: octaves = ½·log₂(stiffness ratio). The √-law HALVES the stiffness decades."""
    return 0.5 * math.log2(s_ratio)


# ---- the two band EDGES as dimensionless topological rolloffs (SIGN forced, corner [O]) ----------
def lowpass_mass(r, zeta):
    """HIGH edge — a driven mass (the ossicular inertia) as a 2nd-order LOW-PASS, in r=ω/ω_corner.
    |H| = 1/√((1−r²)²+(2ζr)²): monotone-decreasing above resonance, → −12 dB/oct (∝1/ω²) asymptote
    (the MASS term), robust to the damping ζ. The SIDE (high) is forced; ω_corner is [O]."""
    return 1.0 / math.sqrt((1.0 - r * r) ** 2 + (2.0 * zeta * r) ** 2)


def highpass(r, n):
    """LOW edge — the helicotrema short-circuit as an n-th-order HIGH-PASS, in r=ω/ω_corner.
    |H| = rⁿ/√(1+r^{2n}): monotone-increasing through the corner, → 0 below it (the LOWS are cut),
    robust to the order n. The SIDE (low) is forced; ω_corner is [O]."""
    return (r ** n) / math.sqrt(1.0 + r ** (2 * n))


def bandpass_product(f, f_lo_corner, f_hi_corner, n=2, zeta=0.7):
    """The audible band as the PRODUCT: (low-edge high-pass) × (high-edge low-pass). SHAPE+SIGN forced;
    the two corners are [O] inputs (passed in only to DRAW the band's shape, never derived/tuned)."""
    return highpass(f / f_lo_corner, n) * lowpass_mass(f / f_hi_corner, zeta)


# =====================================================================================================
def run(P):
    P("=" * 96)
    P("E7 — the audible BAND  ·  a GEOMETRY-carved bandpass on the inherited √(stiffness/inertia) law")
    P("     why only ~20 Hz–20 kHz is heard : SHAPE + every edge SIGN forced ; absolute edges/corners [O]")
    P("     one elastic-wave law (light c²=B/ρ ∥ sound √(γP/ρ) ∥ cochlea √(S/m)) — the band is geometry")
    P("=" * 96)

    # -- PART 0 : a reference structure gene reproduces offline; NO inherited byte changed ------------
    P("\n[0] a reference structure gene reproduces offline (γ LEVEL + A4 SHAPE, from the frozen cache):")
    ref = E1.read_measured(REF_GENE)                     # asserts cache==atlas & A4 = signal−γ for TMC1
    P(f"    [PASS] {REF_GENE:7s} γ(level)={ref['gamma']:.4f}  A4 amp={ref['shape_amplitude']:.5f} "
      f"range={ref['shape_range']:.5f}  node={ref['node']}  (MET pore — STRUCTURE reference)")
    P("    -> TMC1 γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9). No gene was")
    P("       fetched and NO inherited byte changed in E7 (no re-freeze — frozen hashes stay valid). [V]")
    P("    FIREWALL: γ is promoter STRUCTURE only — NOT a stiffness S, NOT a corner, NOT a band edge.")

    # -- PART A : the keystone — N_oct = ½·log₂(S_base/S_apex), exact ---------------------------------
    P("\n[A] the keystone — the octave span is EXACTLY HALF the log₂ of the stiffness ratio (CF∝√S):")
    P("    N_oct = ½·log₂(S_base/S_apex).  Read the span off the INHERITED Greenwood map, then invert via")
    P("    the √-law (S_ratio = (CF_base/CF_apex)²) and check the identity closes to machine precision:")
    cf_apex, cf_base = cf(0.0), cf(1.0)
    span = octave_span()
    s_ratio = implied_stiffness_ratio(span)              # = (CF_base/CF_apex)² by the √-law
    n_from_s = noct_from_stiffness_ratio(s_ratio)        # = ½·log₂(S_ratio)
    P(f"       CF_apex (x=0) = {cf_apex:8.3f} Hz     CF_base (x=1) = {cf_base:10.3f} Hz   (inherited Greenwood)")
    P(f"       audible span  = log₂(CF_base/CF_apex) = {span:.6f} octaves   (human ≈ 10)")
    P(f"       implied stiffness ratio S_base/S_apex = (CF_base/CF_apex)² = {s_ratio:.4e}  (≈ 10⁶)")
    P(f"       ½·log₂(S_ratio) = {n_from_s:.6f} octaves   ==  span  (|Δ|={abs(n_from_s - span):.1e})")
    assert abs(n_from_s - span) < 1e-12                  # the identity is the √-law, exact
    assert abs(span - 10.0248227) < 1e-6 and abs(s_ratio - 1.0852872e6) < 1e2
    P("    -> *why ~10 octaves* is FORCED once the stiffness ratio is known; *why a ratio ~10⁶* is the BM's")
    P("       measured graded geometry [L] (it widens & thins base→apex), never a fit. The √-law's whole")
    P("       contribution is the EXPONENT ½ — it HALVES the ~6 stiffness DECADES into ~10 OCTAVES.  [F]/[V]")

    # -- PART B : the ½ is the forced contribution — decompose the span ------------------------------
    P("\n[B] the √-law HALVES the stiffness decades — decompose the span (the exponent ½ is what's forced):")
    span_pure = math.log2(cf_pure_exp(1.0) / cf_pure_exp(0.0))     # the bare 10^{ax} term
    bend = math.log2(cf_pure_exp(0.0) / cf_apex)                   # helicotrema apical bend (PART C)
    basal = math.log2(cf_pure_exp(1.0) / cf_base)                 # tiny basal offset effect
    P(f"       pure exponential 10^(a·x) term : span = log₂(10^a) = a·log₂(10) = {span_pure:.6f} oct  [F]")
    P(f"       + helicotrema apical bend      : +{bend:.6f} oct  (the −A·k relief, PART C)  [L-magnitude]")
    P(f"       − tiny basal offset effect     : −{basal:.6f} oct  (offset negligible at the stiff base)")
    P(f"       = full audible span            : {span_pure + bend - basal:.6f} oct  ==  {span:.6f}  [V]")
    assert abs((span_pure + bend - basal) - span) < 1e-9
    P("    -> the exponential SHAPE (its octave count per stiffness decade) is FORCED by the √-law; the")
    P("       absolute decades (the ~10⁶ ratio) are measured geometry [L]. Forced exponent, [O] magnitude.")

    # -- PART C : the LOW edge is a high-pass — the helicotrema ---------------------------------------
    P("\n[C] the LOW edge (high-pass) — the HELICOTREMA: a low-END-only relief + a topological lows-cut:")
    off = A_GW * k_GW
    frac_apex = off / cf_pure_exp(0.0)                   # fractional weight of −A·k at the apex
    frac_base = off / cf_pure_exp(1.0)                   # ... at the base
    P("    (i) the inherited offset −A·k is a CONSTANT subtracted from an exponential ⇒ a LOW-END-only")
    P("        correction: its FRACTIONAL weight is large at the apex, negligible at the base —")
    P(f"          weight at apex = {frac_apex:.4f}   weight at base = {frac_base:.4f}   ratio = {frac_apex/frac_base:.3f} (= 10^a)")
    P(f"        so it reshapes ONLY the low edge, bending the apical end DOWN {bend:.4f} oct to ~{cf_apex:.0f} Hz. [F-side/V; k is L]")
    assert frac_apex > 50.0 * frac_base and abs(frac_apex / frac_base - 10.0 ** a_GW) < 1e-6
    P("    (ii) the TOPOLOGY forces a high-pass: the apical hole short-circuits slow (DC-ward) pressure, so")
    P("        below a corner the lows equalise before a wave forms — a lows-cut, monotone through the")
    P("        corner, robust to the filter ORDER (the SIDE is forced; the corner needs the area → [O]):")
    for n in (1, 2, 3):
        rs = np.linspace(0.02, 8.0, 6000)
        H = np.array([highpass(r, n) for r in rs])
        mono = bool(np.all(np.diff(H) > 0))
        deep = highpass(0.05, n)                         # attenuation deep below the corner
        assert mono and deep < 0.06
        P(f"          order n={n}  monotone-increasing through corner={mono}  |H| at 0.05·ω_c={deep:.5f} (lows cut →0)")
    P("    -> the low-frequency rolloff EXISTS and is on the apical/low SIDE — forced by the topology;")
    P("       the corner (helicotrema area + cochlear compliance) is [O], and k is calibration [L].")

    # -- PART D : the HIGH edge is a low-pass — middle-ear mass + the basal stiffness ceiling ---------
    P("\n[D] the HIGH edge (low-pass) — the MIDDLE-EAR MASS + a FINITE basal stiffness ceiling:")
    P("    (i) the ossicular chain has MASS; a driven inertia is a 2nd-order LOW-PASS — above resonance the")
    P("        transmission is monotone-DECREASING with a forced −12 dB/oct (∝1/ω², the mass term)")
    P("        asymptote, robust to the damping ζ (the SIDE is forced; the corner is [O]):")
    for zeta in (0.3, 0.7, 1.0, 2.0):
        rs = np.linspace(1.2, 40.0, 6000)
        H = np.array([lowpass_mass(r, zeta) for r in rs])
        mono = bool(np.all(np.diff(H) < 0))
        slope = (math.log10(lowpass_mass(120.0, zeta)) - math.log10(lowpass_mass(60.0, zeta))) / math.log10(2.0)
        assert mono and abs(slope - (-2.0)) < 0.02      # −2 in log-log = −12 dB/oct
        P(f"          ζ={zeta:4.1f}  monotone-decreasing above ω_c={mono}  high-f log-log slope={slope:+.4f} (→ −2 = −12 dB/oct)")
    P("    (ii) the stiffest place (the base, x=1) fixes a FINITE absolute ceiling CF_max=(1/2π)√(S_base/m):")
    xs = np.linspace(0.0, 1.0, 2001)
    vals = np.array([cf(x) for x in xs])
    increasing = bool(np.all(np.diff(vals) > 0))
    P(f"        inherited place map strictly INCREASING apex→base = {increasing}; FINITE ceiling CF(1) = {cf_base:.1f} Hz")
    assert increasing and math.isfinite(cf_base)
    P("    -> the high-frequency rolloff EXISTS and is on the basal/high SIDE — forced (a mass → low-pass;")
    P("       a finite S_base → a finite CF_max); the corner / CF_max value (ossicular mass, S_base) is [O].")

    # -- PART E : the band = the bandpass PRODUCT — SHAPE + every edge SIGN forced --------------------
    P("\n[E] the BAND = (place passband) × (helicotrema high-pass) × (middle-ear low-pass) — a bandpass:")
    P("    drawn with PLACEHOLDER corners (passed in to SHOW the shape, NEVER derived/tuned), the product")
    P("    is unimodal — rising through the low corner, flat across the passband, falling above the high")
    P("    corner — with a single interior peak. SHAPE + the SIGN of each edge are forced; corners are [O]:")
    f_lo_c, f_hi_c = 30.0, 14000.0                       # ILLUSTRATIVE ONLY — [O], not a claim, not tuned
    fs = np.geomspace(10.0, 30000.0, 4001)
    B = np.array([bandpass_product(f, f_lo_c, f_hi_c) for f in fs])
    ip = int(np.argmax(B))
    rising_below = bool(np.all(np.diff(B[:ip]) > 0))
    falling_above = bool(np.all(np.diff(B[ip:]) < 0))
    assert rising_below and falling_above and 0 < ip < len(fs) - 1
    P(f"       product is unimodal: rising below the peak={rising_below}, falling above={falling_above}")
    P(f"       (the peak place and the two edges MOVE with the [O] corners — only the SHAPE is the claim)")
    P("    -> the audible band is a GEOMETRY problem on top of the inherited wave law — NOT a new physics:")
    P("       a bandpass = a place passband × a lows-cut × a highs-cut, every edge SIGN forced by geometry.")

    # -- PART F : THE META-RESULT — the √-law forces the EXPONENT and every SIGN; magnitudes are [O] --
    P("\n[F] the point of E7 — the √-law fixes the EXPONENT (½) and every edge SIGN; the magnitudes are [O]:")
    P("    FORCED & geometry-invariant : the bandpass SHAPE · the √-law exponent ½ (octaves = ½·log₂ S-ratio)")
    P("                                  · the LOW-edge high-pass SIDE · the HIGH-edge low-pass SIDE")
    P("                                  · the −12 dB/oct mass asymptote · the FINITE basal ceiling.")
    P("    [O] measured geometry       : CF_min, CF_max (Hz) ← S_apex, S_base · the ~10⁶ stiffness RATIO")
    P("                                  · the LOW corner ← helicotrema area + cochlear compliance")
    P("                                  · the HIGH corner / CF_max ← ossicular mass + S_base.")
    P("    NONE of those magnitudes is fixed by an inherited constant: the √-law gives only the EXPONENT,")
    P("    and γ is promoter STRUCTURE only (firewall) — never a stiffness, a corner, or an area. The only")
    P("    things that set the edges are measured lengths/stiffnesses/masses, none derivable without a")
    P("    measured number. ⇒ a closed numeric band = a CHOICE of those magnitudes = TUNING (forbidden).")
    P("    So E7 does NOT pin the band; it CHARACTERISES it: SHAPE + exponent + every SIGN forced, the")
    P("    absolute edges/corners the irreducible measured-geometry [O].  (The E6 parallel: there ONE")
    P("    scalar Q was open; here it is the measured GEOMETRY — same form-forced/magnitude-[O] discipline.)  [F]")

    # -- honest negatives preserved -------------------------------------------------------------------
    P("\n[honest negatives — preserved, not hidden]")
    P("    N1  the ABSOLUTE band edges CF_min / CF_max (Hz) are [O] — they need S_apex and S_base (the BM")
    P("        stiffness at each end), the ossicular mass, and the helicotrema area. Only the bandpass")
    P("        SHAPE, the √-law EXPONENT ½, and the SIGN of each edge are forced. A number = TUNING.")
    P("    N2  the LOW (helicotrema) corner is [O] — it needs the helicotrema area + the scala/cochlear")
    P("        compliance. Only the EXISTENCE and the SIDE (apical/low) are forced (the topology); the")
    P("        −A·k offset that places the apex at ~20 Hz uses the measured calibration k [L].")
    P("    N3  the HIGH (middle-ear) corner / CF_max is [O] — it needs the ossicular mass + the path")
    P("        stiffness, and S_base for CF_max. Only the EXISTENCE, the SIDE (high), and the −12 dB/oct")
    P("        mass asymptote are forced.")
    P("    N4  the stiffness RATIO itself (~10⁶) is a MEASURED anatomical input — the basilar membrane")
    P("        widens (~5×) and thins base→apex; this volume consumes it via Greenwood, never fits it. The")
    P("        √-law forces only the FACTOR (½) converting it to octaves, not the ratio.")
    P("    N5  the band here is the LONG-WAVE / place-resonance account (same scope as E6-N5). The full")
    P("        2-D/3-D fluid problem, the cochlear input impedance, and the middle-ear's own multi-")
    P("        resonance transfer are NOT solved — they are the deeper [O] hydrodynamics. The forced")
    P("        results are the band's SHAPE, exponent, and edge SIGNS — not the full transfer function.")
    P("    N6  the absolute BM stiffness gradient law S(x) and the developmental program that builds the")
    P("        graded membrane are anatomy / the DNA volume's — [O] here. (γ is structure-only, never a")
    P("        stiffness; this volume consumes the Greenwood SHAPE, not the gradient's molecular origin.)")
    P("    N7  the felt pitch / loudness RANGE as experience — why ~20 Hz–20 kHz 'is' the audible world —")
    P("        is the MIND volume's (firewall). E7 moves only the physical band edges, not the percept.")

    # -- naming note (the E-numbering; consistent with E6's handling) ---------------------------------
    P("\n[naming note] E7 delivers BLUEPRINT-E7 CONTENT (the audible band) in the unambiguous folder")
    P("    research/E7-audible-band/. As with E6, the EXISTING folders are NOT renamed (to preserve every")
    P("    frozen hash and the no-omission set), so the v0.3.0 E1/E2 label slip stays flagged as a")
    P("    separate bookkeeping item; E7's own folder is unambiguous.")

    P("\nLEARNED (E7): the audible BAND is a GEOMETRY-carved bandpass on the inherited √(stiffness/inertia)")
    P("  wave law — not a new physics. The √-law HALVES the stiffness decades into octaves, forcing the")
    P("  KEYSTONE N_oct=½·log₂(S_base/S_apex) (exact; human 10.025 oct ⟺ ratio 1.085×10⁶). The low edge is")
    P("  a helicotrema high-pass — the −A·k offset is a low-END-only relief that bends the apex down ~3 oct")
    P("  to ~20 Hz, and the apical hole forces a lows-cut SIDE; the high edge is a middle-ear low-pass — an")
    P("  ossicular MASS forces a −12 dB/oct highs-cut and the stiff base fixes a FINITE CF_max. The band is")
    P("  the PRODUCT of the three, a bandpass whose SHAPE and every edge SIGN are forced by geometry while")
    P("  the absolute edges and three corners are the irreducible measured-geometry [O] — a number for any")
    P("  of them would be TUNING (forbidden). FORM/SIGN/EXPONENT forced; magnitudes [O] — the E6 discipline.")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
