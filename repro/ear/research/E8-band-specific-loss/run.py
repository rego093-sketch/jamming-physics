#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E8 :  band-specific / frequency-selective hearing loss  (WHERE on the map fails).
                         Composes E4's failure-CLASS axis (drive / structure / readout / amplifier) with
                         E7's PLACE axis (which frequency sits where) to derive the characteristic
                         audiogram SHAPES — high-frequency/down-sloping, the 4 kHz notch, cookie-bite,
                         low-frequency/reverse-slope. Same discipline as E4/E6/E7: the SHAPE and the
                         DIRECTION (which way the audiogram tilts, which side the notch sits) are FORCED;
                         every threshold, slope, notch-Hz, and age stays [O]; the lever is proposal-only,
                         direction-only; the firewall is verbatim; the felt experience is the mind volume's.

WHAT THIS BUILDS (BLUEPRINT.md §E8 / WORK_HANDOVER open item 7).
  E4 answered WHICH locus of the inherited cubic ṡ=g·s−s³+h fails (its STRUCTURE g, its DRIVE h, the
  READOUT downstream, or the CRITICAL regime g→0 — the E3 amplifier). E7 supplied the PLACE axis: the
  inherited √-law Greenwood map CF(x)=A(10^{ax}−k) is strictly increasing apex→base, so each cochlear
  place carries one characteristic frequency. But a real audiogram is frequency-SELECTIVE — loss
  concentrated in a BAND — so a disease is a 2-D object: a failure CLASS acting over a BAND of PLACES.
  E8 composes the two axes (direction-only, proposal-only, firewall) to explain the audiogram SHAPES the
  seed did not yet touch. It proves:

    (A) THE KEYSTONE (parameter-free, exact). Because CF(x) is strictly MONOTONE (E7-D), the place→frequency
        map is an ORDER-ISOMORPHISM: a contiguous band of FAILED PLACES maps to a contiguous band of LOST
        FREQUENCIES, preserving order, and E1's inv_greenwood maps it back exactly. So the audiogram SHAPE
        IS THE IMAGE, under the inherited place map, of WHERE the (E4) failure concentrates:
            failed BASE  (x→1) ⟺ lost HIGH freqs → down-sloping
            failed APEX  (x→0) ⟺ lost LOW  freqs → up-sloping / reverse-slope
            failed MIDDLE        ⟺ lost MID  freqs → cookie-bite
            one over-driven place ⟺ a single-frequency NOTCH at that place's CF.
        No constant is tuned: this is the monotonicity of the inherited map turned into an isomorphism.

    (B) HIGH-FREQUENCY / DOWN-SLOPING (presbycusis, many ototoxic & genetic losses) = a broad degeneration
        × the BASAL band. The base is the highest-CF place, so it CYCLES fastest (CF *is* the cycling
        rate); if mechanical/metabolic load accumulates with cycles, the cumulative-load ORDERING is
        monotone — maximal at the base. So the basal/high-CF places are loaded first → fail first → a
        HIGH-frequency loss. The DIRECTION (basal-first ⇒ down-sloping) is forced; slope/threshold/age [O].

    (C) THE 4 kHz NOTCH (noise-induced) = an over-drive × the TRANSFER-PEAK place. The outer/middle-ear
        transfer is NOT flat: an ear-canal resonance (a high-pass-to-peak) × the E7 ossicular-mass low-pass
        gives a transfer with an interior MAXIMUM at some f_peak strictly BELOW CF_max. The place tuned to
        f_peak receives the most input energy → over-drives → fails first → a NOTCH at that place, BELOW
        the very top (interior x<1). The DIRECTION (a notch below the top, not at it) is forced; the exact
        notch frequency (the canal length + ossicular transfer) is [O].

    (D) MID-FREQUENCY / COOKIE-BITE (several congenital/genetic forms) = a mid-gradient locus × the MIDDLE
        band. A locus whose vulnerability peaks in the MIDDLE of the cochlear gradient (neither the basal
        cumulative-load max nor the apical ion/fluid regime) maps, by the isomorphism, to a MID-frequency
        loss with better edges. The forced part is only mid PLACE → mid FREQUENCY; the mid-CONCENTRATION
        of the locus is a cited/empirical input, not derived — the honestly weakest of the four (N2).

    (E) LOW-FREQUENCY / REVERSE-SLOPE (e.g. WFS1/Wolfram low-frequency SNHL, fluctuating low-freq loss) =
        an apical ion/fluid-regulation locus × the APICAL band. The apex is where the helicotrema relief
        (E7-C: the −A·k offset is apical-only) and the endolymph/ion regulation dominate; an apical-specific
        regulation failure maps, by the isomorphism, to a LOW-frequency / up-sloping loss. The DIRECTION
        (apical ⇒ low-freq) is forced; the locus's apical concentration is cited biology [L]; magnitude [O].

    (F) THE 2-D PICTURE + the LEVER. Each pattern is a (CLASS × BAND) hypothesis: which of E4's loci, over
        which of E7's place bands, reproduces the audiogram SHAPE. The substrate-inverse lever is the E4
        DIRECTION applied AT the E7 band — a 2-D direction (restore which locus, at which band). E4's honest
        negatives CARRY: a STRUCTURE-class basal degeneration is NOT drive-rescuable (E4-C, the bistable
        window 2·spinodal(g)→0 as g→0), so the structural component of a high-frequency loss admits no drive
        rescue; only the DRIVE-class (e.g. the apical reverse-slope ion regime) is switch-recoverable in
        principle — and even then only the DIRECTION is named. No molecule, dose, diagnosis, or efficacy.

    (G) THE META-RESULT. The audiogram SHAPE and every DIRECTION (the tilt, the notch side) are FORCED by
        the order-isomorphism + the basal-load ordering + the transfer-peak side; what stays [O] is every
        MAGNITUDE — thresholds in dB, slopes in dB/oct, the notch frequency in Hz, the age of onset. Same
        form-forced / magnitude-[O] discipline as E6/E7: a closed audiogram (numbers) would be TUNING.

THE BIOLOGY / PHYSIOLOGY (cited, not re-opened; consumed from the DNA + biology volumes and E4).
  • presbycusis: age-related down-sloping high-frequency SNHL; basal hair-cell / strial / neural loss is
    earliest and most severe (Schuknecht's taxonomy; the base is metabolically and mechanically hardest-
    worked). • noise-induced loss: the ~3–6 kHz "notch" (the C5-dip), classically attributed to the
    external/middle-ear transfer maximum concentrating energy there (the ear-canal resonance ~3 kHz +
    the ossicular transfer). • cookie-bite: a mid-frequency trough, several autosomal-dominant/recessive
    congenital forms. • reverse-slope (low-frequency) SNHL: e.g. WFS1/Wolframin (DFNA6/14/38), often
    apical/low-frequency and fluctuating, tied to endolymph/ion homeostasis. Identity/function are cited;
    E8 derives only the SHAPE DIRECTION each implies once mapped onto the inherited place axis.

THE PHYSICS (cited, built on E7's forced geometry).
  CF(x) strictly increasing (E7-D) ⇒ the place→frequency map is monotone, hence an order-isomorphism on
  intervals (elementary). CF is a frequency, i.e. a cycling RATE; cumulative cyclic load therefore orders
  with CF (a biophysical premise — cited, see N5). The outer/middle-ear transfer = a canal resonance ×
  the ossicular-mass low-pass (E7-D) ⇒ an interior transfer maximum below CF_max (the energy-delivery
  peak; Rosowski; Puria). The absolute corners, the notch frequency, the load rate, and the dB
  thresholds need measured anatomy/physiology, never fitted here.

HOW IT RELATES TO THE FOUNDATION (no-regression — NO inherited byte changes in E8).
  EXTENDS the inherited foundation by IMPORTING it. Like E5/E6/E7, E8 fetches NO new gene and folds
  nothing into the cache/atlas — it touches NOT ONE inherited byte and triggers NO re-freeze (every
  frozen hash stays valid as recorded at seed time). It consumes the INHERITED √-law place map
  (`vp_sound_wave.greenwood_f`), E1's `inv_greenwood` + `read_measured` (one already-cached gene per E4
  class recomputes from the frozen cache and equals the atlas bit-for-bit, A4 = signal − γ), the
  INHERITED cubic's `spinodal` (to carry E4's structure-class negative), and E7's place geometry. E4's
  failure classes are consumed as labels (cited biology), never re-derived. WFS1 is named only as a
  CITED clinical archetype of the apical/reverse-slope pattern — no new γ is measured for it.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the KEYSTONE — the place→frequency ORDER-ISOMORPHISM (contiguous place band ⟺ contiguous
            frequency band, exact inv_greenwood round-trip) and the four shape DIRECTIONS it forces ;
            the basal-first cumulative-load ORDERING (load ∝ CF, strictly increasing ⇒ argmax at base) ⇒
            the down-sloping DIRECTION ; the outer/middle-ear transfer's interior MAXIMUM below CF_max ⇒
            the notch BELOW the top (interior place) ; the apical→low and mid→mid images ; and that E4's
            structure-class drive-non-rescuability CARRIES to a high-frequency structural loss.
  [L]      : the Greenwood A/a/k place-map calibration ; each reproduced gene's γ (NCBI-measured, cached) ;
            the failure-class LABELS and the loci's band CONCENTRATIONS (cited biology — presbycusis basal,
            cookie-bite mid, WFS1 apical), NOT derived from γ here.
  [O]      : every MAGNITUDE — dB thresholds, dB/oct slopes, the notch frequency (Hz), the age of onset,
            the cumulative-load RATE ; the molecule / dose / in-vivo selectivity / efficacy of ANY lever
            (firewall — proposal-only) ; the READOUT-class (synapse) rescue (E4-D, a different substrate) ;
            the full fluid hydrodynamics / cochlear input impedance (E6-N5, E7-N5) ; and the felt
            experience of band-specific loss (→ mind volume). Each names its obstacle below.

FIREWALL. γ reads promoter STRUCTURE only — never a channel function, a drive magnitude, a load rate, a
band edge, a dB threshold, an in-vivo selectivity, or a clinical effect (a reference gene per class is
reproduced offline ONLY to show the cache still recomputes and NO byte moved). The disease layer is
PROPOSAL-ONLY: direction-only (class × band) failure modes and substrate-inverse lever DIRECTIONS.
Nothing here diagnoses, treats, or prescribes; no molecule is designed; no dose, threshold, or efficacy
is stated. The felt experience of band-specific hearing loss is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io, importlib.util
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E8-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate  as SUB                               # the R19 cubic (spinodal — carries E4's negative)
import vp_sound_wave as SND                               # √-law Greenwood place map CF(x)=A(10^{ax}−k)


def _load(name, path):
    """Load a module by file path under a UNIQUE name (every increment ships a file called run.py;
    importing under the bare name 'run' would collide in sys.modules — this keeps them distinct)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# reuse E1's read_measured + inv_greenwood (cache==atlas, A4⊥, exact place inverse) under a unique name
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))

# one ALREADY-CACHED E4 gene per failure class (NO new fetch, NO re-freeze) — to show the cross-axis
# composition reads the SAME frozen atlas. class labels are CITED biology (E4), never derived from γ.
CLASS_REF = [
    ("SLC26A4", "drive",     "pendrin — endolymph ion/pH homeostasis (the ion/fluid regime)"),
    ("MYO15A",  "structure", "myosin XVa — stereocilia structure (the gating apparatus)"),
    ("OTOF",    "readout",   "otoferlin — ribbon-synapse Ca²⁺ sensor (downstream of the flip)"),
    ("SLC26A5", "amplifier", "prestin — OHC somatic motor at criticality (the E3 gain)"),
]


# ============================================================================================
#  the two inherited axes, composed.   apex x=0 (low CF) → base x=1 (high CF).  CF ∝ √S (√-law).
# ============================================================================================
def cf(x):
    """E7 / inherited Greenwood characteristic frequency at fractional place x (apex→base)."""
    return SND.greenwood_f(x)


def place_of(f_hz):
    """E1 inverse place map: the cochlear place x carrying characteristic frequency f (exact inverse)."""
    return E1.inv_greenwood(f_hz)


def freq_band_of_place_band(x0, x1):
    """The IMAGE of a contiguous place band [x0,x1] under the monotone place map = a contiguous
    frequency band [CF(x0),CF(x1)]. The KEYSTONE: failed-places → lost-frequencies, order preserved."""
    return cf(x0), cf(x1)


def cyclic_load_rate(x):
    """The cumulative-load ORDERING proxy: load accrues with cycles, and CF *is* the cycling rate, so
    the per-place load rate orders with CF(x). Strictly increasing apex→base ⇒ argmax at the base.
    Only the ORDERING (basal-first) is the claim; the absolute rate is [O]."""
    return cf(x)


# ---- the outer/middle-ear transfer (the noise-notch energy-delivery peak) — SIGN/SHAPE forced -----
def canal_resonance(f, f_c, n=2):
    """An ear-canal quarter-wave resonance as a high-pass-to-peak in r=f/f_c (n-th order). Brings the
    transfer UP toward a peak; combined with the ossicular low-pass it yields an interior maximum."""
    r = f / f_c
    return (r ** n) / math.sqrt(1.0 + r ** (2 * n))


def ossicle_lowpass(f, f_c, zeta=0.7):
    """The E7 ossicular-MASS 2nd-order low-pass in r=f/f_c (−12 dB/oct asymptote). Brings the transfer
    DOWN above its corner; the SIDE is forced (E7-D)."""
    r = f / f_c
    return 1.0 / math.sqrt((1.0 - r * r) ** 2 + (2.0 * zeta * r) ** 2)


def ear_transfer(f, f_canal, f_oss):
    """The outer/middle-ear energy-delivery transfer = (canal resonance) × (ossicular low-pass). Drawn
    with ILLUSTRATIVE corners ([O], passed in only to SHOW the SHAPE); the claim is the interior peak."""
    return canal_resonance(f, f_canal) * ossicle_lowpass(f, f_oss)


# =====================================================================================================
def run(P):
    P("=" * 98)
    P("E8 — band-specific / frequency-selective hearing loss  ·  E4's CLASS axis × E7's PLACE axis")
    P("     a disease is a 2-D object: a failure CLASS acting over a BAND of places. The audiogram SHAPE")
    P("     is the IMAGE, under the inherited monotone place map, of WHERE the failure concentrates.")
    P("     SHAPE + every DIRECTION forced ; thresholds/slopes/notch-Hz/ages [O] ; lever proposal-only.")
    P("=" * 98)

    # -- PART 0 : one cached gene per E4 class reproduces offline; NO inherited byte changed ----------
    P("\n[0] one already-cached gene per E4 CLASS reproduces offline (γ LEVEL + A4 SHAPE, frozen cache):")
    recs = {}
    for sym, cls, note in CLASS_REF:
        r = E1.read_measured(sym); recs[sym] = r
        P(f"    [PASS] {sym:8s} γ(level)={r['gamma']:.4f}  A4 amp={r['shape_amplitude']:.5f}  "
          f"class=[{cls:9s}]  ({note})")
    P("    -> every γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9). NO gene was")
    P("       fetched and NO inherited byte changed in E8 (no re-freeze — frozen hashes stay valid). [V]")
    P("    FIREWALL: γ is promoter STRUCTURE only — NOT a band edge, NOT a load rate, NOT a dB threshold.")

    # -- PART A : THE KEYSTONE — the audiogram is the IMAGE of the failed-place band (order-isomorphism)
    P("\n[A] the keystone — the place→frequency map is an ORDER-ISOMORPHISM (CF strictly monotone, E7-D):")
    xs = np.linspace(0.0, 1.0, 4001)
    vals = np.array([cf(x) for x in xs])
    increasing = bool(np.all(np.diff(vals) > 0))
    P(f"    inherited CF(x) strictly increasing apex→base = {increasing}  (CF_apex={cf(0.0):.1f} Hz, "
      f"CF_base={cf(1.0):.1f} Hz)")
    P("    ⇒ a contiguous band of FAILED PLACES maps to a contiguous band of LOST FREQUENCIES, order")
    P("      preserved, and E1's inv_greenwood maps it back EXACTLY. The audiogram SHAPE = this image:")
    cases = [("BASAL  (x∈[0.7,1.0])", 0.7, 1.0, "HIGH freqs lost → DOWN-sloping"),
             ("MIDDLE (x∈[0.4,0.6])", 0.4, 0.6, "MID  freqs lost → cookie-bite"),
             ("APICAL (x∈[0.0,0.3])", 0.0, 0.3, "LOW  freqs lost → up-sloping / reverse")]
    for label, x0, x1, shape in cases:
        f0, f1 = freq_band_of_place_band(x0, x1)
        xb0, xb1 = place_of(f0), place_of(f1)
        assert abs(xb0 - x0) < 1e-9 and abs(xb1 - x1) < 1e-9     # the isomorphism round-trips exactly
        P(f"       {label} → CF∈[{f0:8.1f},{f1:8.1f}] Hz   {shape}   (inv round-trip |Δ|<1e-9)")
    assert increasing
    P("    -> no constant is tuned: this is the monotonicity of the INHERITED place map turned into an")
    P("       isomorphism between place-bands and frequency-bands. WHERE fails ⇒ WHICH band is lost.  [F]/[V]")

    # -- PART B : HIGH-FREQUENCY / DOWN-SLOPING (presbycusis) = degeneration × the BASAL band ---------
    P("\n[B] HIGH-FREQUENCY / DOWN-SLOPING (presbycusis, ototoxic, many genetic) = degeneration × BASE:")
    loads = np.array([cyclic_load_rate(x) for x in xs])
    load_mono = bool(np.all(np.diff(loads) > 0))
    P("    the base is the highest-CF place, so it CYCLES fastest (CF *is* the cycling rate); if load")
    P("    accumulates with cycles, the cumulative-load ORDERING is monotone — maximal at the base:")
    P(f"       load-rate ∝ CF strictly increasing apex→base = {load_mono}  (argmax at base x=1)")
    P(f"       load(base)/load(apex) = CF(1)/CF(0) = {cyclic_load_rate(1.0)/cyclic_load_rate(0.0):.0f}× "
      f"(the base is the hardest-worked place)")
    assert load_mono
    P("    -> the basal / high-CF places are loaded FIRST ⇒ fail FIRST ⇒ a HIGH-frequency loss that")
    P("       progresses down the map (presbycusis is classically basal/high-frequency-first, Schuknecht).")
    P("       The DIRECTION (basal-first ⇒ DOWN-sloping) is forced; the slope/threshold/age are [O].  [F]")

    # -- PART C : the 4 kHz NOTCH (noise) = over-drive × the TRANSFER-PEAK place ----------------------
    P("\n[C] the 4 kHz NOTCH (noise-induced) = an over-drive × the outer/middle-ear TRANSFER-PEAK place:")
    P("    the energy-delivery transfer = (ear-canal resonance) × (E7 ossicular-mass low-pass) — drawn")
    P("    with ILLUSTRATIVE corners ([O], to SHOW the shape) it is UNIMODAL with an interior MAXIMUM:")
    f_canal, f_oss = 2500.0, 5000.0                      # ILLUSTRATIVE ONLY — [O], not a claim, not tuned
    fs = np.geomspace(100.0, 30000.0, 6000)
    T = np.array([ear_transfer(f, f_canal, f_oss) for f in fs])
    ip = int(np.argmax(T)); f_peak = float(fs[ip])
    unimodal = bool(np.all(np.diff(T[:ip]) > 0) and np.all(np.diff(T[ip:]) < 0))
    x_notch = place_of(f_peak)
    P(f"       transfer unimodal (rises then falls) = {unimodal}")
    P(f"       transfer PEAK f_peak = {f_peak:.0f} Hz (ILLUSTRATIVE) → notch place x = {x_notch:.4f} "
      f"(interior, below the base)")
    P(f"       f_peak < CF_max ({cf(1.0):.0f} Hz) = {f_peak < cf(1.0)}  ⇒ the notch sits BELOW the very top")
    assert unimodal and 0.0 < x_notch < 1.0 and f_peak < cf(1.0)
    P("    -> the place tuned to the transfer maximum receives the MOST input energy ⇒ over-drives ⇒ fails")
    P("       first ⇒ a NOTCH at that place — a mid-high dip BELOW the top, not at it (the classic ~3–6 kHz")
    P("       C5-dip). The DIRECTION (a notch BELOW the top) is forced; the exact notch Hz is [O] (it needs")
    P("       the ear-canal length + the ossicular transfer — placing a number would be TUNING).  [F]")

    # -- PART D : MID-FREQUENCY / COOKIE-BITE = a mid-gradient locus × the MIDDLE band ----------------
    P("\n[D] MID-FREQUENCY / COOKIE-BITE (several congenital/genetic forms) = a mid-gradient locus × MID:")
    fm0, fm1 = freq_band_of_place_band(0.4, 0.6)
    P(f"    a locus whose vulnerability peaks in the MIDDLE of the cochlear gradient maps, by the")
    P(f"    isomorphism, to a MID-frequency loss with better edges: x∈[0.4,0.6] → CF∈[{fm0:.0f},{fm1:.0f}] Hz.")
    P("    -> the FORCED part is only mid PLACE → mid FREQUENCY (the isomorphism). The mid-CONCENTRATION")
    P("       of the locus (neither basal cumulative-load nor apical ion-regime) is a CITED/empirical input,")
    P("       NOT derived here — this is the honestly WEAKEST of the four shapes (see N2).  [F-image; L-locus]")

    # -- PART E : LOW-FREQUENCY / REVERSE-SLOPE (WFS1 archetype) = apical ion/fluid locus × APEX -------
    P("\n[E] LOW-FREQUENCY / REVERSE-SLOPE (e.g. WFS1/Wolfram low-freq SNHL) = apical ion/fluid locus × APEX:")
    fa0, fa1 = freq_band_of_place_band(0.0, 0.3)
    P(f"    the APEX is where the helicotrema relief (E7-C: the −A·k offset is apical-only) and the")
    P(f"    endolymph/ion regulation dominate; an apical-specific regulation failure maps to LOW freqs:")
    P(f"       x∈[0.0,0.3] → CF∈[{fa0:.1f},{fa1:.1f}] Hz  ⇒ a low-frequency / up-sloping (reverse) loss")
    P("    -> the DIRECTION (apical ⇒ LOW-frequency) is forced by the place map; the locus's apical")
    P("       concentration is CITED biology [L] (WFS1/Wolframin is a low-frequency, often fluctuating SNHL")
    P("       tied to endolymph/ion homeostasis — a DRIVE/ion-regime class in E4 terms); magnitude [O].  [F]")
    P("       (WFS1 is named only as the CITED clinical archetype — no new γ is measured for it. firewall.)")

    # -- PART F : the 2-D (class × band) TABLE + the lever DIRECTION (E4 × E7), proposal-only ---------
    P("\n[F] the 2-D picture — each audiogram is a (CLASS × BAND) hypothesis; the lever = E4 direction @ E7 band:")
    P("    +------------------- +------------- +------------------ +------------------------------------+")
    P("    | audiogram shape    | E4 class     | E7 band (place)   | lever DIRECTION (proposal-only)    |")
    P("    +------------------- +------------- +------------------ +------------------------------------+")
    P("    | down-sloping (HF)  | structure/   | basal  (x→1)      | act on g @ base (NO drive rescue — |")
    P("    |  = presbycusis     |  amplifier   |                   |  E4-C); restore g→0⁺ for amplifier |")
    P("    | 4 kHz NOTCH        | over-drive   | transfer-peak     | reduce over-drive @ the peak place |")
    P("    |  = noise-induced   |  (h excess)  |  place (interior) |  (a DRIVE-axis direction)          |")
    P("    | cookie-bite (MID)  | mid-gradient | middle (x≈0.5)    | act on the mid-locus @ mid band    |")
    P("    | reverse-slope (LF) | drive/ion    | apical (x→0)      | restore the apical ion regime      |")
    P("    |  = WFS1 archetype  |  regime      |                   |  toward +spinodal(g) (recoverable) |")
    P("    +------------------- +------------- +------------------ +------------------------------------+")
    # E4's structure-class negative CARRIES: a structural basal loss is NOT drive-rescuable
    g_intact, g_lost = 1.30, 0.01
    w_intact, w_lost = 2.0 * SUB.spinodal(g_intact), 2.0 * SUB.spinodal(g_lost)
    P(f"    E4's honest negative CARRIES — the bistable window 2·spinodal(g) collapses as g→0 "
      f"(g={g_intact}:{w_intact:.4f} → g={g_lost}:{w_lost:.5f}):")
    assert w_intact > 20.0 * w_lost and w_lost < 1e-3
    P("       so the STRUCTURAL component of a high-frequency loss admits NO drive rescue (the switch is")
    P("       gone, not un-driven); only the DRIVE-class (the apical reverse-slope ion regime) is switch-")
    P("       recoverable IN PRINCIPLE — and even then only the DIRECTION is named. Every cell is a")
    P("       DIRECTION: no molecule, dose, in-vivo selectivity, diagnosis, or efficacy (firewall).")

    # -- PART G : THE META-RESULT — SHAPE/DIRECTION forced; every magnitude [O] -----------------------
    P("\n[G] the point of E8 — the audiogram SHAPE and every DIRECTION are forced; every MAGNITUDE is [O]:")
    P("    FORCED & parameter-free : the place→frequency ORDER-ISOMORPHISM and the four shape DIRECTIONS")
    P("                              (basal→HF down-slope · apical→LF reverse · mid→cookie-bite · the")
    P("                              transfer-peak notch BELOW the top) · the basal-first load ORDERING")
    P("                              · that E4's structure-class drive-non-rescue CARRIES.")
    P("    [O] measured magnitude  : every dB threshold · every dB/oct slope · the notch frequency (Hz) ·")
    P("                              the age of onset · the cumulative-load RATE · the absolute band edges.")
    P("    The inherited map and the cubic give only the ORDER and the SIGNS; the magnitudes need measured")
    P("    anatomy/physiology and γ is promoter STRUCTURE only (firewall) — never a load rate, a band edge,")
    P("    or a dB. ⇒ a closed numeric audiogram = a CHOICE of those magnitudes = TUNING (forbidden). So E8")
    P("    does NOT pin an audiogram; it CHARACTERISES the SHAPE: every DIRECTION forced, every magnitude")
    P("    the irreducible measured [O] — the E6/E7 discipline, now on the 2-D (class × band) object.  [F]")

    # -- honest negatives preserved -------------------------------------------------------------------
    P("\n[honest negatives — preserved, not hidden]")
    P("    N1  every MAGNITUDE is [O] — the dB thresholds, the dB/oct slopes, the notch frequency in Hz,")
    P("        the age of onset, the load rate, the absolute band edges. Only the SHAPE and the DIRECTIONS")
    P("        (the tilt, the notch SIDE) are forced. A number on any of them would be TUNING.")
    P("    N2  COOKIE-BITE is the WEAKEST of the four — the isomorphism forces only mid PLACE → mid")
    P("        FREQUENCY; the mid-CONCENTRATION of the locus is a cited/empirical input, not derived. E8")
    P("        does not explain WHY a given gene's vulnerability peaks mid-cochlea; that is [O] (the locus's")
    P("        position on the cochlear gradient — anatomy / the DNA volume).")
    P("    N3  the NOTCH FREQUENCY (~3–6 kHz) is [O] — it needs the ear-canal length + the ossicular")
    P("        transfer. Only the EXISTENCE of an interior transfer peak (hence a notch BELOW the top) is")
    P("        forced; the illustrative f_peak above is NOT a claim.")
    P("    N4  PRESBYCUSIS is multi-factorial (sensory, strial/metabolic, neural — Schuknecht's types). E8")
    P("        forces only the basal-first DIRECTION of the cyclic-load component; the full cellular")
    P("        taxonomy and the relative weights of the mechanisms are cited/[O], not derived.")
    P("    N5  the cumulative-load argument forces the ORDERING (basal-first) but ASSUMES load accrues")
    P("        monotone with cycling rate — a cited biophysical premise, not derived here. The RATE, the")
    P("        accrual law, and any threshold are [O].")
    P("    N6  real audiograms are individual and noisy; E8 is a SHAPE-DIRECTION claim about the population")
    P("        TENDENCY of each etiology, NOT a per-patient predictor. Overlap between etiologies (e.g. a")
    P("        noise notch on a presbycusic slope) is expected and not resolved here.")
    P("    N7  the READOUT class (OTOF/synapse) has no place-band SHAPE in this transduction map — its")
    P("        failure is downstream of the flip (E4-D); a band-specific readout audiogram needs the")
    P("        synaptic substrate, which is [O]. And the FELT experience of band-specific loss (losing")
    P("        consonants in HF loss, losing bass in LF loss) is the MIND volume's (firewall).")

    # -- naming note (the E-numbering; consistent with E6/E7's handling) ------------------------------
    P("\n[naming note] E8 delivers BLUEPRINT-E8 CONTENT (band-specific loss) in the unambiguous folder")
    P("    research/E8-band-specific-loss/. As with E6/E7 the EXISTING folders are NOT renamed (to preserve")
    P("    every frozen hash and the no-omission set), so the v0.3.0 E1/E2 label slip stays flagged as a")
    P("    separate bookkeeping item; E8's own folder is unambiguous.")

    P("\nLEARNED (E8): band-specific hearing loss is a 2-D object — an E4 failure CLASS acting over an E7")
    P("  PLACE band. Because the inherited place map CF(x) is strictly monotone, the place→frequency map is")
    P("  an ORDER-ISOMORPHISM, so the audiogram SHAPE IS THE IMAGE of WHERE the failure concentrates: a")
    P("  basal failure → high-frequency down-slope (presbycusis; the base cycles fastest, so it is loaded")
    P("  first), an apical failure → low-frequency reverse-slope (WFS1/ion regime), a mid failure →")
    P("  cookie-bite, and a localized over-drive at the outer/middle-ear transfer peak → a notch BELOW the")
    P("  top (the noise C5-dip). The lever is the E4 DIRECTION applied AT the E7 band, proposal-only, and")
    P("  E4's structure-class negative carries (a structural high-frequency loss has no drive rescue). Every")
    P("  DIRECTION is forced; every threshold, slope, notch-Hz, and age is the irreducible measured [O] — a")
    P("  closed audiogram would be TUNING. FORM/DIRECTION forced; magnitude [O] — the E6/E7 discipline.")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
