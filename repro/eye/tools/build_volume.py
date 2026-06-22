#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_volume.py — build the multi-chapter HTML volume FROM the increment run.py outputs.

CONTRACT (BLUEPRINT "Definition of done"; VP-SPEC v1.8 §6 + C1/C4):
  * Every displayed number is the CODE'S OWN OUTPUT. The builder runs each chapter's run.py
    (the single source), embeds its VERBATIM transcript in the page (hash-pinned), and any number
    that also appears in prose is registered through F(...) which ASSERTS, at build time, that the
    exact string is a substring of that live transcript. A typo'd or invented number fails the
    build. gate_volume.py re-proves the same thing (HTML↔code drift 0).
  * The disease chapter (E4) stays proposal-only behind the magnitude firewall (no quantitative
    clinical token, no '%') — E4's run.py already guarantees its transcript passes; this builder
    adds no forbidden token to the E4 prose, and gate_volume re-checks the rendered E4 chapter.
  * Retrieval-ready (C4): answer-first lead, self-contained passages, JSON-LD, static HTML, sitemap.

Run from package root:   python3 tools/build_volume.py
Deterministic: re-running produces byte-identical files (run.py outputs are deterministic; the
templating is pure string ops, no time/RNG). Output lives under docs/eye/ (one zip, our lane).
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import _volume_lib as L
from _volume_lib import VOLUME    # structural chapter manifest (used bare throughout)

# ----------------------------------------------------------------------------------------------
# F() — the build-time fact gate. Every number that appears in prose goes through here.
# ----------------------------------------------------------------------------------------------
_CUR_TRANSCRIPT = ""     # concatenation of the current chapter's run transcripts
_CUR_FACTS = []          # [{value, note}] surfaced for the current chapter


def F(value, note=""):
    """Register a displayed number and PROVE it is the code's own output.

    Asserts `value` is a verbatim substring of the current chapter's live transcript, records it
    for the chapter's facts.json, and returns it HTML-safe for inlining in prose. Fact values must
    be free of & < > (they are numbers/units) so they round-trip verbatim into the HTML and the
    gate can substring-check them directly.
    """
    assert not any(c in value for c in "&<>"), f"fact value must be plain (no &<>): {value!r}"
    assert value in _CUR_TRANSCRIPT, (
        f"FACT NOT IN TRANSCRIPT (drift!) — {value!r} is not produced by this chapter's run(s). "
        f"Numbers in prose must be the code's own output."
    )
    _CUR_FACTS.append({"value": value, "note": note})
    return L.esc(value)


# small HTML helpers ----------------------------------------------------------------------------
def g(letter, text):
    """One grade-ledger row, e.g. g('F','...')."""
    cls = {"F": "gF", "V": "gV", "L": "gL", "O": "gO"}.get(letter[0], "gO")
    return f'<tr><td class="grade {cls}">[{letter}]</td><td>{text}</td></tr>'


def grade_ledger(rows):
    return ('<section class="grades"><h2>Grades <span class="muted">(VP-SPEC C3 \u2014 honest)</span></h2>'
            '<table class="gtable"><tbody>' + "".join(rows) + "</tbody></table></section>")


def kv(rows):
    """A clean key/number list for 'key results' (rows = [(label_html, value_html), ...])."""
    items = "".join(f'<div class="kv"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    return f'<dl class="kvlist">{items}</dl>'


# ----------------------------------------------------------------------------------------------
# chapter bodies — each returns the inner HTML between the lead and the reproducibility strip.
# every numeric literal is wrapped in F(...) (build-time verified against the live transcript).
# ----------------------------------------------------------------------------------------------
def body_e0():
    return f"""
<section><h2>What this rung establishes</h2>
<p>The eye is handed a carrier it can never follow. Light <em>emerges</em> as the longitudinal
elastic wave of the jammed vacuum lattice, travelling at one speed in quantum units; the quantum
size is the invariant <strong>D = {F("4.852620 pm")}</strong>, derived two ways that agree to
within {F("4.853477 pm")} (the 6\u03c0\u2076\u00b7r_p cross-check). Because D is fixed, the propagation
angle obeys one right triangle, sin\u03c7 = \u03bb/(mD) with m = \u2308\u03bb/D\u2309, so <em>\u03c7 depends on \u03bb
alone</em> \u2014 colour is geometry, not a frequency the receptor could track. This is the WHAT the
downstream switch must convert. <span class="grade gF">[F]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("Invariant quantum size", f"D = {F('4.852620 pm')}"),
  ("Quantum tick \u03c4_q = D/c", F("1.6187e-20 s")),
  ("Light is the lattice wave", f"pulse speed = {F('0.99951 D/\u03c4_q')} (c=1 in quantum units)"),
  ("Red 633 nm \u2192 angle", F("89.9378\u00b0")),
  ("Green 532 nm \u2192 angle", F("89.8248\u00b0")),
  ("Colour separation", f"{F('0.1130\u00b0')} (distinct angles \u21d2 distinct colours)"),
  ("633/532 closure ratio", f"{F('1.189831')} = 633/532 (forced, not fitted)"),
  ("Two-channel closure m\u00b7sin\u03c7\u00b7D/\u03bb", F("1.000000000000000")),
])}
<p>The bands order monotonically in m: gamma is quasi-longitudinal
(\u03c7 = {F("11.8924\u00b0")}, m=1), the <strong>visible window is a narrow near-transverse band</strong>
(\u03c7 \u2248 89.8\u2013{F("89.9378\u00b0")}), and radio is fully transverse (\u03c7 = {F("89.9999\u00b0")}). The
identity of the visible carrier is its angle, cross-validated on two channels (633/532) sharing the
one D. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>The DNA reading \u2014 \u03b3 (LEVEL) and A4 (SHAPE), never \u03b3 alone</h2>
<p>Each master gene is read from its promoter as two orthogonal coordinates of one DNA-stiffness
field: <strong>\u03b3</strong>, the window-mean (LEVEL), and the <strong>A4 coordinate</strong>, the
same signal with the mean removed (SHAPE). On the canonical probes the level spans
\u03b3 = {F("0.7306")} (AT-flat) to {F("2.2051")} (GC-flat), a mixed window reads
\u03b3 = {F("1.4682")} with shape amplitude {F("0.6441")}, and A4 is literally the signal minus \u03b3
(mean(shape) = 0 to machine precision). From \u03b3 alone the switch threshold is the spinodal
(2/3\u221a3)\u00b7\u03b3^1.5 = {F("1.2604")} for the mixed window. Two genes with equal \u03b3 but different A4
shape are <em>not</em> interchangeable \u2014 the emergence reads both. <span class="grade gF">[F]</span></p>
<p class="muted">The full A4 anchor/loop/anchor-relative-phase needs the wider genomic region and an
NCBI feature table; it is a named <span class="grade gO">[O]</span> deferred read, flagged never invented.</p></section>
""", grade_ledger([
    g("F", "Light emerges as the lattice wave c=\u221a(B/\u03c1); D is the invariant quantum size derived, not assumed; the angle law sin\u03c7=\u03bb/(mD); \u03b3 (LEVEL) and A4 (SHAPE) are orthogonal coordinates of one stiffness field."),
    g("V", "c=1 in quantum units; the two-channel closure m\u00b7sin\u03c7\u00b7D/\u03bb=1 to 1e-15; A4 = signal \u2212 \u03b3 (mean(shape)=0 to machine precision)."),
    g("L", "The committed colour anchor 633/532 nm; the canonical DNA probes."),
    g("O", "Absolute angle\u2192firing / photon\u2192Hz scale (\u2192 E2/calibration); the full A4 anchor phase (needs the NCBI feature table). Each obstacle named."),
])


def body_e1():
    return f"""
<section><h2>What this rung establishes</h2>
<p>Colour is sampled as three angles. The three cone opsins are placed on the inherited angle map by
their <em>measured</em> peak wavelength (literature, not \u03b3, not fitted), and land at three distinct
near-transverse angle-bands \u2014 OPN1SW (S/blue) at {F("89.7497\u00b0")}, OPN1MW (M/green) at
{F("89.8006\u00b0")}, OPN1LW (L/red) at {F("89.8428\u00b0")} \u2014 so the eye reads colour as three angles:
trichromacy. The committed 633/532 anchor (red {F("89.9378\u00b0")} \u2260 green {F("89.8248\u00b0")},
separation {F("0.1130\u00b0")}) is the falsifier, asserted with no fitting.
<span class="grade gF">[F]</span><span class="grade gL">[L]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("S\u2013M angle separation", F("0.0509\u00b0")),
  ("S\u2013L angle separation", F("0.0931\u00b0")),
  ("M\u2013L angle separation", F("0.0421\u00b0")),
  ("Lineage order key", "argsort(spinodal(\u03b3)) \u2014 lowest-threshold switch first"),
  ("First cone (OPN1SW)", f"\u03b3 = {F('1.3663')}, spinodal = {F('0.6147')}"),
  ("Stiffest rod gene (PDE6B)", f"\u03b3 = {F('1.5354')}, spinodal = {F('0.7323')}"),
])}
<p>The cone/rod lineage <em>emerges</em> from the shared R19 <code>Organ</code> primitive: emergence
order is the substrate's forced key argsort(spinodal(\u03b3)), and relative size is dwell \u221d \u03b3^1.5.
Whether this substrate order matches real retinal developmental <em>time</em> is an open empirical
question \u2014 reported, not fitted. <span class="grade gF">[F]</span><span class="grade gO">[O]</span></p></section>

<section><h2>A4 breaks \u03b3-ties: equal-\u03b3 genes are not interchangeable</h2>
<p>The order key is a total order: primary spinodal(\u03b3), tie-break the A4 shape. The rod CNG channel's
\u03b1/\u03b2 subunits CNGA1 and CNGB1 are the closest \u03b3 pair in the whole eye atlas
(\u0394\u03b3 = {F("0.0003")}); at three-decimal \u03b3 resolution they <em>collapse</em> to an identical value,
exactly the failure mode of reading \u03b3 alone. Their A4 shape amplitudes differ
({F("0.17130")} vs {F("0.07902")}, a factor of {F("2.17\u00d7")}), so the shape tie-break orders them
deterministically. The full key gives {F("19/19 unique ranks")} \u2014 no collapse.
<span class="grade gV">[V]</span></p></section>
""", grade_ledger([
    g("F", "The angle law \u03bb\u2192\u03c7 and the 633/532 anchor; three distinct angle-bands; the R19 order argsort(spinodal(\u03b3)); dwell \u221d \u03b3^1.5; the A4 tie-break rule."),
    g("V", "Organ spinodal == measured atlas for all genes; the (spinodal, A4) key is a strict total order; CNGA1/CNGB1 collapse under \u03b3-alone and are broken by A4 shape."),
    g("L", "Every \u03b3 (+A4) from NCBI promoters, cached; the cone \u03bbmax (S420/M530/L560, literature). None fitted."),
    g("O", "Absolute angle\u2192firing scale (\u2192 E2); whether the substrate order matches developmental time; the felt colour percept (\u2192 mind volume). Each obstacle named."),
])


def body_e2():
    return f"""
<section><h2>What this rung establishes</h2>
<p>This is where the carrier frequency dies. Rod phototransduction is the inherited R19 switch made
<strong>all-or-none</strong> by its cubic. Settled from the dark rest basin (s\u2080=\u2212\u221a\u03b3), each rod gene
stays dark below its spinodal h*(\u03b3) and snaps on the instant the drive crosses it: a finite,
discontinuous jump of about {F("+2.2905")} for rhodopsin. One quantum of drive across h* flips the
whole switch; anything less does nothing \u2014 single-photon sensitivity, as pure structure. The absolute
photon\u2192drive\u2192Hz scale is a named <span class="grade gO">[O]</span>; the discontinuity is
<span class="grade gV">[V]</span>.</p></section>

<section><h2>Key results</h2>
{kv([
  ("RHO threshold h* = spinodal(\u03b3)", F("0.68733")),
  ("RHO rest basin (\u2212\u221a\u03b3)", F("-1.2132")),
  ("The flip (1.01\u00b7h*)", f"final_s = {F('+1.4025')} (on)"),
  ("Cooperativity order", f"the cubic \u2212s\u00b3, order {F('n=3')} \u2014 where \u2018Hill\u22483\u2019 comes from"),
  ("Cubic switch slope across h*", f"\u2248 {F('157.1')} (formally \u2192 \u221e at the fold)"),
  ("Linear control slope", f"\u2248 {F('0.679')} (smooth, graded)"),
  ("Steepness ratio", f"\u2248 {F('231\u00d7')} \u2014 the cubic makes a STEP"),
])}
<p>The all-or-none behaviour is not assumed \u2014 it is <em>forced</em> by the third-order restoring term
\u2212s\u00b3. Strike out the cubic (a first-order control field, not the substrate) and the threshold, the
basin, and the jump all vanish: the response becomes graded. The cooperativity IS the cubic, and it is
necessary. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>One channel, two genes: A4, not \u03b3 alone</h2>
<p>The four switches order by spinodal(\u03b3) \u2014 lowest threshold first (CNGB1 h* = {F("0.66213")}). The
CNG channel is one channel built from two genes, CNGA1 (\u03b1) and CNGB1 (\u03b2); their \u03b3-LEVEL is degenerate
(\u0394\u03b3 = {F("0.0003")}) yet their A4 SHAPE differs {F("2.17\u00d7")}. Even the two halves of a single
transduction switch are not interchangeable \u2014 the switch reads LEVEL and SHAPE. Whether the substrate
threshold-order matches the real biochemical cascade sequence is a named
<span class="grade gO">[O]</span> (needs kinetics). <span class="grade gV">[V]</span></p></section>
""", grade_ledger([
    g("F", "The all-or-none flip is a saddle-node past h*=spinodal(\u03b3); cooperativity order n=3 = the cubic \u2212s\u00b3; the four switches' order = argsort(spinodal(\u03b3))."),
    g("V", "Every rod gene stays dark below h* and snaps on above it (finite jump); deleting the cubic removes the switch (\u226520\u00d7 steeper than graded control); CNGA1/CNGB1 collapse under \u03b3-alone and are separated by A4 shape."),
    g("L", "Every rod-gene \u03b3 (+A4) from NCBI promoters, cached, byte-identical to atlas."),
    g("O", "Absolute photon\u2192drive\u2192firing (Hz) scale; the literal physiological rod Hill value; whether the substrate order matches the real cascade sequence; the felt percept of light (\u2192 mind volume)."),
])


def body_e3():
    return f"""
<section><h2>What this rung establishes</h2>
<p>WHERE is geometry, and it survives the collapse. Grounded on the internal angle law, Snell's law
is shown to be the transverse-oscillation (phase) match at the interface, with refractive index given
its lattice meaning <strong>n = c_vac/c_med = \u221a((B/\u03c1) ratio)</strong>; here c_eye = c_vac/n with
n = {F("1.3333")}. The wavefront/speed derivation and the index form agree to 0 over an incidence
sweep, and total internal reflection onsets exactly at the critical angle {F("48.5904\u00b0")}.
<span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("Refractive index (lattice meaning)", f"n = c_vac/c_med = {F('1.3333')}"),
  ("Critical angle (eye\u2192air TIR)", F("48.5904\u00b0")),
  ("Surface power (Emsley reduced eye)", f"P = (n\u2082\u2212n\u2081)/R = {F('60.06 D')}"),
  ("Distant point images at", f"v = {F('22.200 mm')} = the axial length (retina)"),
  ("First-order chromatic split", f"|v_red\u2212v_grn| = {F('0.0e+00 mm')} (single index)"),
  ("Colour-angle separation (survives)", f"\u0394\u03c7 = {F('0.1130\u00b0')}"),
])}
<p>The cited Emsley reduced eye (n=4/3, R=5.55 mm) forms a real <em>inverted</em> image: a finite object
maps with m&lt;0 (e.g. {F("-0.01693")} for a distant object), so a point above the axis lands below the
fovea \u2014 the image is a spatial position code. This part is classical ray arithmetic on the
substrate-grounded Snell plus measured n,R, flagged <span class="grade gV">[V-arith]</span>.</p></section>

<section><h2>Two orthogonal channels on one wave</h2>
<p>Refraction conserves frequency, so the colour-angle \u03c7(\u03bb) is preserved through the optics: red and
green remain distinct internal angles (\u0394\u03c7 = {F("0.1130\u00b0")}) while a single index co-locates them on
the retina (chromatic split {F("0.0e+00 mm")}). Optics gives WHERE; the angle law gives WHAT COLOUR \u2014
a robust position channel and a hypersensitive \u03c7 channel on one wave. The chromatic-aberration
<em>magnitude</em> needs the per-\u03bb medium stiffness c_med(\u03bb) and is a named
<span class="grade gO">[O]</span>; no diopter is invented. <span class="grade gF">[F]</span></p></section>
""", grade_ledger([
    g("F", "Snell's law is the transverse-oscillation match; n = c_vac/c_med = \u221a((B/\u03c1) ratio); refraction conserves f, so the colour-angle \u03c7(\u03bb) is preserved \u2014 position (\u03b8) and colour (\u03c7) are two independent channels."),
    g("V", "Wavefront/speed-Snell = index-Snell to &lt;1e-12 rad; TIR onsets exactly at the critical angle; one index co-locates the colours (zero first-order split)."),
    g("L", "The ocular index n=4/3 and surface radius R=5.55 mm (cited Emsley reduced eye); the 633/532 anchor (inherited). None fitted."),
    g("O", "The longitudinal chromatic-aberration magnitude (needs c_med(\u03bb)); the absolute photon\u2192firing scale (\u2190 E2); accommodation dynamics. Each obstacle named."),
])


def body_e4():
    # FIREWALL: this body carries NO quantitative clinical token and NO '%'. Only R19 field
    # values (s, \u03b3, h*) appear. gate_volume re-checks the rendered chapter against E4's MAGNITUDE_BLOCK.
    return f"""
<aside class="scope"><strong>Scope \u2014 theoretical, non-clinical.</strong> This chapter studies the
<em>mechanism layer</em> of congenital vision conditions as a question in physics and
dynamical-systems theory. It does not diagnose, treat, prescribe, screen, or triage; it designs no
molecule and states no quantity. Every statement is direction-only and proposal-only, behind a
machine-checked magnitude firewall. The felt percept of sight is deferred to the mind volume.</aside>

<section><h2>What this rung establishes</h2>
<p>The break in the ladder is the E2 single-photon switch read in reverse. On the frozen field settled
from the dark rest basin, a healthy drive clears the spinodal h*(\u03b3) and flips on (s&gt;0); a
loss-of-function lesion lets the effective drive fall short and the only basin left is the dark one, so
the all-or-none switch <em>cannot flip</em> (s&lt;0). The only difference is whether the drive crosses
h*. For GUCY2D the healthy outcome is s = {F("+1.3711")} and the attenuated outcome is
s = {F("-0.8779")}. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("LOF = field held below h*", "only the dark basin exists \u2192 no flip"),
  ("GUCY2D threshold h* = spinodal(\u03b3)", f"\u03b3 = {F('1.3650')}, h* = {F('0.6138')}"),
  ("The sharp threshold (1.01\u00b7h*)", f"final_s = {F('+1.3505')} (the flip; all-or-none)"),
  ("Most drive-fragile switch", f"CNGB3, \u03b3 = {F('1.2425')}, h* = {F('0.5331')}"),
  ("Stiffest switch", f"PDE6B, \u03b3 = {F('1.5354')}, h* = {F('0.7323')}"),
  ("Structural fragility range", f"h* \u2208 [{F('0.5331, 0.7323')}]"),
])}
<p>The rescue-DIRECTION is forced by the same fold and has exactly two directions: raise the effective
drive back across h*, or lower the effective threshold below the residual drive (shown with a
hypothetical threshold probe while the measured \u03b3 stays frozen). We state the directions only \u2014
how much, by what means, and which agent are firewall-blocked and named
<span class="grade gO">[O]</span>. Nothing is diagnosed, designed, or quantified.</p></section>

<section><h2>The six rank by threshold; A4 rides orthogonal; \u03b3 is context, not the lesion</h2>
<p>The six switches rank by spinodal(\u03b3) as a <em>structural</em> fragility ordering (CNGB3 the most
drive-fragile, PDE6B the stiffest) \u2014 not a clinical severity claim, which would be firewall-blocked.
Among these six the \u03b3-level alone already separates every gene at three decimals, so there is no
\u03b3-tie to dramatise; yet A4 is still read for each, and the closest-\u03b3 pair (GUCY2D, A4 amplitude
{F("0.19649")}) differs in shape by a factor of {F("1.22\u00d7")} \u2014 level and shape stay orthogonal.</p>
<p class="muted"><strong>Honest caveat (stated in the increment):</strong> the measured \u03b3 is the
<em>promoter</em> stiffness, while almost every congenital-blindness lesion is coding/downstream. So
\u03b3 supplies the switch's threshold <em>context</em>, not the lesion itself; mapping a specific coding
lesion onto a change of drive in physical units is a named <span class="grade gO">[O]</span>, inherited
from E2's scale. This gap is stated outright, never hidden behind the geometry.</p></section>
""", grade_ledger([
    g("F", "Loss-of-function = the field held below the saddle-node h*=spinodal(\u03b3) (only the dark basin exists \u2192 no flip); the substrate-inverse lever has exactly two directions; the six switches' threshold order = argsort(spinodal(\u03b3))."),
    g("V", "Every blindness switch flips on under a clearing drive and stays dark under the attenuated drive; the flip is a discontinuous step across h*; both lever directions re-flip the frozen switch; the six \u03b3 are all distinct at 3dp yet each carries A4 shape and the closest-\u03b3 pair is A4-separated. The magnitude firewall is machine-checked."),
    g("L", "Every blindness-gene \u03b3 (+A4) from NCBI promoters, cached, byte-identical to atlas."),
    g("O", "The absolute photon\u2192drive\u2192firing scale and the map from a real (coding) lesion to a change of drive (inherited E2); which lever agent and at what magnitude (firewall-blocked \u2014 none produced); clinical severity/prognosis/onset (firewall-blocked); the felt percept and felt restoration of sight (\u2192 mind volume)."),
])


def body_e5():
    return f"""
<section><h2>What this rung establishes</h2>
<p>The whole collapse, quantified. The carrier is \u03bd = c/\u03bb \u2248 10\u00b9\u2074 Hz \u2014 red 632.99 nm gives
{F("4.736e+14 Hz")} (energy {F("1.959 eV")}), green 532 nm gives {F("5.635e+14 Hz")}
({F("2.331 eV")}) \u2014 yet the ganglion band is ~10\u2013100 Hz, a drop of about
{F("12.7\u201313.7 orders")} of magnitude. The receptor cannot oscillate at 10\u00b9\u2074 Hz; it absorbs E = h\u03bd
as one quantum of drive. The ratio is forced; the absolute neural Hz is a named
<span class="grade gO">[O]</span>. <span class="grade gL">[L]</span><span class="grade gF">[F]</span></p></section>

<section><h2>Mechanism = event-detection + low-pass, not mixing</h2>
{kv([
  ("Intrinsic rhythm (no carrier)", f"f0 = {F('0.01050')} /unit-time"),
  ("Carrier-invariance (no-mixing test)", f"output moves only {F('11.3%')} across a 20\u00d7 carrier span"),
  ("The cubic is the all-or-none event", f"delete \u2212s\u00b3 \u21d2 flip {F('+2.151')} becomes {F('-50.000')} (no threshold)"),
  ("Band \u221d 1/\u03c4 (\u03c4_s = 20)", f"out_dom = {F('0.01875')}"),
  ("Band \u221d 1/\u03c4 (\u03c4_s = 160)", f"out_dom = {F('0.00300')}"),
])}
<p>On the frozen Neuron a fast carrier (24\u00d7\u2013476\u00d7 the intrinsic rhythm) is averaged away (out/f_c \u2192 0);
the output is carrier-frequency-invariant (a mixer would track it); deleting the cubic destroys the
threshold; and the surviving band is set by the recovery \u03c4, scaling as 1/\u03c4. The carrier frequency is
discarded \u2014 colour survives only because it rides the angle (geometry), not a frequency the cell could
follow. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>
""", grade_ledger([
    g("F", "Down-conversion is event-detection + low-pass, not mixing: the output is carrier-frequency-invariant, the cubic is the all-or-none event, and the surviving band scales as 1/\u03c4."),
    g("V", "On the frozen Neuron the fast carrier is averaged away (out/f_c\u21920); deleting \u2212s\u00b3 removes the threshold; the band moves with \u03c4."),
    g("L", "The carrier \u03bd=c/\u03bb and quantum E=h\u03bd at the committed wavelengths; the cited ganglion range ~10\u2013100 Hz."),
    g("O", "The absolute biological Hz at each rung (carrier \u2192 event \u2192 cascade \u03c4 \u2192 spike rate); only the collapse RATIO and the mechanism are forced. Each obstacle named."),
])


def body_e6():
    return f"""
<section><h2>What this rung establishes</h2>
<p>\u2018Visible\u2019 is neither chosen nor geometric. Two unrelated constraints select the same window. The
wavelength is the anchor, mapped exactly to \u03bd = c/\u03bb, period T = 1/\u03bd, and E = h\u03bd with SI-exact
constants \u2014 the HeNe red anchor 632.99 nm is {F("1.95870706 eV")}, the green channel 532 nm is
{F("2.33053005 eV")}, both inside the window. <span class="grade gL">[L]</span><span class="grade gF">[F]</span></p></section>

<section><h2>Geometry places it; photochemistry pins it</h2>
{kv([
  ("Gate (i) \u2014 placement in m", "visible (m\u224810\u2075) sandwiched between x-ray and infrared, near-transverse"),
  ("Gate (ii) \u2014 energy window", f"reversible 11-cis\u2192all-trans, 1.8\u20133.3 eV \u21d2 \u03bb = {F('375.70969222\u2013688.80110241 nm')}"),
  ("Sawtooth, not a kink", f"633 nm deficit {F('0.0621945346\u00b0')} &lt; 750 nm deficit {F('0.1187372397\u00b0')}"),
  ("IR excluded by energy, not geometry", f"10\u00b5m deficit {F('0.0491568932\u00b0')} is smaller than visible's, yet excluded"),
  ("Soft red edge", f"750 nm = {F('1.65312265 eV')} sits {F('0.14687735 eV')} below the 1.8 eV floor"),
])}
<p>The lattice geometry only <em>places</em> the band: the angle is a smooth sawtooth with no kink at
the band edges, so it never gates a band \u2014 an infrared probe is more transverse than visible yet is
excluded by the energy floor, not by any angle. What pins ~380\u2013750 nm is the chromophore's reversible
energy window: a floor to drive the flip, a ceiling before damage. The deep-red edge is soft and we say
so. The molecular tuning of that window is coding/photochemistry \u2014 the promoter-\u03b3 this package reads
has no lever on the retinal pocket, a named <span class="grade gO">[O]</span>. E6 invents no chromophore.
<span class="grade gF">[F]</span><span class="grade gL">[L]</span></p></section>
""", grade_ledger([
    g("F", "Geometry PLACES the band (sandwiched in m, near-transverse) but the angle is a smooth sawtooth that never gates a band; the closure m\u00b7sin\u03c7\u00b7D/\u03bb=1 holds to 1e-15; the exact \u03bd/T/E map from the wavelength anchor."),
    g("L", "The cited reversible isomerisation window 1.8\u20133.3 eV; the already-measured visible anchors (633/532; opsin \u03bbmax 420/530/560)."),
    g("O", "The retinal chromophore energy that sets the floor (coding/photochemistry, outside the promoter-\u03b3) \u2014 the soft red edge is a consequence; obstacle named, no chromophore invented."),
])


def body_e7():
    return f"""
<section><h2>What this rung establishes</h2>
<p>The band the eye speaks in is the cutoff of the transduction low-pass. The frozen recovery law
w \u2190 w + dt\u00b7(s \u2212 \u03b2w)/\u03c4_s (quoted verbatim) <em>is</em> a first-order leaky integrator \u2014 a single-pole
low-pass H(f) = 1/(\u03b2 + i\u00b72\u03c0f\u00b7\u03c4_s). Its one claim, the band is set by the recovery time-constant
f_c = \u03b2/(2\u03c0\u03c4_s), is read off the substrate four ways that agree. <span class="grade gF">[F]</span>
<span class="grade gV">[V]</span></p></section>

<section><h2>Four agreeing reads, and band \u221d 1/\u03c4</h2>
{kv([
  ("DC gain = 1/\u03b2", f"closed form {F('2.0000')}, measured {F('1.99902')}"),
  ("Measured cutoff vs \u03b2/(2\u03c0\u03c4)", f"{F('0.001993')} vs {F('0.001989')}"),
  ("Phase lag at cutoff", f"{F('44.99\u00b0')} (one pole \u21d2 45\u00b0)"),
  ("High-frequency roll-off", f"{F('-19.96 dB/decade')} (one pole \u21d2 \u221220)"),
  ("f_c\u00b7\u03c4 invariant (= \u03b2/2\u03c0)", f"{F('0.079577')}, spread {F('0.27%')}"),
  ("Cutoff halves with \u03c4 (20\u219280)", f"{F('0.003985')} \u2192 {F('0.000999')}"),
])}
<p>Sweeping \u03c4 gives f_c \u221d 1/\u03c4 exactly, and the recovery law carries no \u03b3 term and no carrier term \u2014
so the band is purely \u03c4: orthogonal to the carrier (E5) and to \u03b3. The full frozen neuron inherits this
(its rhythm falls monotonically in \u03c4); \u03b3 is a secondary mover via dwell \u221d \u03b3^1.5. The single-pole
idealisation vs. the real multi-stage cascade and the absolute \u03c4\u2192Hz are named
<span class="grade gO">[O]</span>. <span class="grade gF">[F]</span></p></section>
""", grade_ledger([
    g("F", "The surviving band is f_c = \u03b2/(2\u03c0\u03c4_s), set by the recovery time-constant; it is invariant to both the carrier and \u03b3 \u2014 \u03c4, not the carrier and not \u03b3, fixes the band."),
    g("V", "DC gain 1/\u03b2; the measured cutoff matches \u03b2/(2\u03c0\u03c4); phase lag 44.99\u00b0; roll-off \u221219.96 dB/decade; f_c\u00b7\u03c4 constant \u21d2 f_c \u221d 1/\u03c4."),
    g("L", "The frozen Neuron constants \u03b2=0.5, \u03c4_f=1.0, \u03c4_s=40.0; \u03b3(GUCY2D)=1.365 read byte-equal from the atlas."),
    g("O", "The single-pole idealisation vs. the real multi-stage cascade (rhodopsin\u2192transducin\u2192PDE\u2192cGMP\u2192CNG); the absolute \u03c4\u2192Hz calibration; the full-neuron rhythm is only approximately \u221d1/\u03c4. Each obstacle named."),
])


def body_e8():
    return f"""
<section><h2>What this rung establishes (the spine closes)</h2>
<p>The eye's last step is a re-quantiser, not a mixer. The frozen R19 neuron whose slow recovery set
the band now fires \u2014 each spike a membrane up-crossing, an all-or-none fold-crossing event \u2014 and
re-encodes the graded ~Hz signal as a ganglion spike RATE. The code is thresholded, bounded, and
monotone, and it tracks the slow envelope while never re-introducing the carrier. With E8 the
down-conversion spine E0\u2192E8 is complete. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>A thresholded, bounded, monotone clock</h2>
{kv([
  ("Rheobase floor", "silent at g\u22640.20, fires at g\u22650.30 (the switch must clear its fold)"),
  ("Monotone re-encoding", f"rate rises across the band, {F('0.00783')} \u2192 {F('0.01133')}"),
  ("Near-periodic clock", f"CV(ISI) \u2248 {F('0.00017')}\u2013{F('0.00024')} (\u226A 1)"),
  ("Depolarisation-block ceiling", f"at drive +1.00 the rate falls to {F('0.000167')} (silent)"),
  ("Carrier-invariance", f"rate spread {F('1.53%')} across a 20\u00d7 carrier span (rate \u27c2 carrier)"),
])}
<p>The full-range f\u2013I is a <em>bandpass in drive</em>: a rheobase floor and a depolarisation-block
ceiling, monotone only inside a finite band. The central result closes the loop with E5/E7 \u2014 fix the
envelope and sweep the carrier and the rate is invariant ({F("1.53%")}); raise the envelope and the
rate rises; the spike train sits in the neural low band. The ~13-order down-conversion is preserved
end-to-end. <span class="grade gF">[F]</span></p></section>

<section><h2>Where \u03b3 sits (read-only) and the hand-off</h2>
<p>\u03b3 shifts the f\u2013I position (rheobase) via spinodal(\u03b3), not the band (that is \u03c4, E7) and not the
signal (the drive): at fixed drive a higher-\u03b3 gene fires slower (CNGB3 {F("0.009167")} down to RHO
{F("0.007833")}). Because \u03b3 moves the rate about as much as the drive here, E8 makes no
\u2018\u03b3 negligible\u2019 claim. The felt percept of sight is out of scope \u2014 it hands off to the mind volume
behind the firewall. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>
""", grade_ledger([
    g("F", "The rate code is thresholded (rheobase), bounded (depolarisation-block ceiling \u2014 a bandpass in drive), and monotone; the carrier stays gone (rate \u27c2 carrier, rate \u221d envelope); the train sits in the neural low band \u21d2 the collapse is preserved end-to-end."),
    g("V", "Silent below the rheobase, firing above; strictly monotone across the band; CV(ISI) \u226A 1; depolarisation block at high drive; rate invariant to the carrier, rising with the envelope."),
    g("L", "The frozen Neuron \u03b2=0.5/\u03c4_f=1.0/\u03c4_s=40.0; \u03b3 read byte-equal from the atlas (read-only offset)."),
    g("O", "The absolute Hz/spike-count, the f\u2013I shape, the single-stage collapse of the retinal network, and the felt percept (\u2192 mind volume). Each obstacle named."),
])


def body_e9():
    # FIREWALL: this body carries NO quantitative clinical token and NO '%'. Only angles, margins,
    # wavelengths (nm, never written "nm)"), and READ-ONLY \u03b3 values appear. gate_volume re-checks the
    # rendered chapter against E9's own MAGNITUDE_BLOCK.
    return f"""
<aside class="scope"><strong>Scope \u2014 theoretical, non-clinical.</strong> This chapter studies the
<em>mechanism layer</em> of the most common inherited colour-vision difference (red-green) as a question
in geometry and dynamical-systems theory \u2014 the E1 angle map with one of its samples lost or two of them
converged. It does not diagnose, treat, prescribe, screen, classify a person, or triage; it designs no
molecule and states no clinical quantity. Every statement is structure-only and direction-only, behind a
machine-checked magnitude firewall. The felt experience of colour \u2014 and of colour confusion \u2014 is
deferred to the mind volume.</aside>

<section><h2>What this rung establishes</h2>
<p>Colour, in this volume, is the light's propagation <strong>angle</strong> \u03c7(\u03bb) (E1) \u2014 not a frequency
the receptor could track. So the three cone opsins are three angle-<em>samples</em>, and the three
colour-discrimination axes are simply their pairwise angle <strong>margins</strong>. Read this way the
angle map answers a question it was never tuned to: <em>which</em> colour axis is the most fragile. The
three cones land at {F("89.7497\u00b0")} (S), {F("89.8006\u00b0")} (M) and {F("89.8428\u00b0")} (L), and the
<strong>green-red (M\u2013L) margin is the smallest of the three</strong> \u2014 so red-green is the structurally
most fragile axis. This is forced by the measured peaks and the frozen law, and it matches that red-green
is the most common inherited colour-vision difference. <span class="grade gF">[F]</span><span class="grade gL">[L]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("Invariant quantum size", f"D = {F('4.852620 pm')} (\u03c7 depends on \u03bb alone)"),
  ("S / M / L cone angles", f"{F('89.7497\u00b0')} / {F('89.8006\u00b0')} / {F('89.8428\u00b0')}"),
  ("Blue-green (S\u2013M) margin", F("0.0509\u00b0")),
  ("Green-red (M\u2013L) margin", f"{F('0.0421\u00b0')}  \u2190 smallest (most fragile)"),
  ("Blue-red (S\u2013L) margin", F("0.0931\u00b0")),
  ("How much tighter green-red is", f"{F('1.208\u00d7')} tighter than S\u2013M, {F('2.208\u00d7')} than S\u2013L"),
  ("Coincident \u03bbmax \u21d2 margin", f"{F('0.000000\u00b0')} (exact \u2014 same angle)"),
])}
<p>The fragility ordering is geometry, not a clinical severity claim (which would be firewall-blocked):
the green-red axis simply has the least angular room on the map. <span class="grade gF">[F]</span></p></section>

<section><h2>Dichromacy and anomalous trichromacy are one continuum</h2>
<p>Because \u03c7 is a function of \u03bb <em>alone</em>, two opsins with the same peak map to the
<strong>same angle</strong>, so their margin is <strong>exactly {F("0.000000\u00b0")}</strong>. That single
fact joins the two pictures. <strong>Dichromacy</strong> removes one of the three angle-samples \u2014 lose L
and the samples left are S and M (surviving margin {F("0.0509\u00b0")}), lose M and they are S and L
(surviving margin {F("0.0931\u00b0")}); in both the tight green-red axis vanishes and one chromatic axis
survives. <strong>Anomalous trichromacy</strong> is two peaks <em>converging</em>: held inside one
m-band, where \u03c7 is locally smooth-monotone (sawtooth-proof), the margin falls monotonically \u2014
{F("0.199367\u00b0")} \u2192 {F("0.073276\u00b0")} \u2192 {F("0.032565\u00b0")} \u2192 {F("0.010231\u00b0")} \u2192
{F("0.000000\u00b0")} \u2014 as the gap closes. The limit of convergence <em>is</em> the loss.
<span class="grade gF">[F]</span><span class="grade gV">[V]</span></p>
<p>The lever is therefore a pure <strong>direction</strong>: peaks toward each other shrink the margin
(to zero at coincidence); peaks apart widen it. How anomalous, the real hybrid peak, any clinical
severity \u2014 all are the firewall-blocked <span class="grade gO">[O]</span>; nothing is quantified or
named. <span class="muted">Honest caveat: \u03c7(\u03bb) is hypersensitive and <em>distributional</em> (a
sawtooth, inherited from E1/E6), so the margin is a property of the committed peaks, not a smooth
response to an arbitrary nanometre-scale shift; only the coincidence limit and the local within-band
sense are forced \u2014 stated, not hidden.</span></p></section>

<section><h2>Why it is <em>colour</em>-blindness, not loss of acuity</h2>
<p>The three channels carried on one wave are orthogonal: colour is the angle \u03c7 (E1, the WHAT),
position is the image geometry (E3, the WHERE), and brightness/detection is the R19 switch magnitude
(E2). Removing a cone removes one angle-sample but neither a position-sample nor the switch \u2014 so the
loss is confined to a single colour axis while spatial acuity and the light/dark response stay intact.
That is forced by the channel orthogonality, and it is why the condition is specifically <em>colour</em>
vision, with acuity preserved. The felt experience of colour confusion is the mind volume's.
<span class="grade gF">[F]</span></p></section>

<section><h2>\u03b3 is read read-only; the genomics is measured, not \u03b3</h2>
<p>The opsin genes' \u03b3 (LEVEL) and A4 (SHAPE) are read as a <em>structural</em> excitability offset \u2014
read-only, byte-equal to the frozen atlas: OPN1LW \u03b3 = {F("1.4820")} (spinodal {F("0.6944")}, A4 amplitude
{F("0.09028")}) and OPN1MW \u03b3 = {F("1.4058")} (spinodal {F("0.6415")}, A4 amplitude {F("0.12596")}), a level
offset of \u0394\u03b3 = {F("0.0762")} with shapes differing {F("1.40\u00d7")}. This chapter makes <strong>no</strong>
claim that \u03b3 predicts the opsin peak \u2014 the optical layer (peak \u2192 angle) and the DNA-structural layer
(\u03b3/A4 \u2192 excitability) are kept separate. The genomic architecture that makes red-green X-linked and
male-prevalent \u2014 the OPN1LW/OPN1MW tandem array on the X chromosome \u2014 is measured genomics
<span class="grade gL">[L]</span>, not derivable from the promoter-\u03b3 this package reads: a named
<span class="grade gO">[O]</span>.</p></section>
""", grade_ledger([
    g("F", "Colour is the propagation angle \u21d2 the three cones are three angle-samples and the three discrimination axes are their pairwise margins; the green-red (M\u2013L) margin is the smallest; coincident peaks give an exactly-zero margin (so dichromacy = remove one sample, anomaly = peaks converge \u2014 one continuum); colour (angle) is orthogonal to position (image) and brightness (switch), so the loss costs exactly one colour axis."),
    g("V", "Three distinct cone angles; M\u2013L is the smallest of the three margins; the coincidence margin is exactly 0; the within-m-band convergence is monotone to 0; the remaining cones' R19 switch is unchanged; the cone \u03b3 is byte-equal to the atlas. The magnitude firewall is machine-checked."),
    g("L", "Every cone \u03b3 (+A4) from NCBI promoters, cached, byte-identical to atlas; the cone peaks (S420/M530/L560, literature); red-green is the most common inherited colour-vision difference (epidemiology); the X-linked OPN1LW/OPN1MW tandem-array architecture (genomics)."),
    g("O", "The magnitude of any anomalous shift / the real hybrid peak / any clinical severity (firewall-blocked \u2014 none produced); the sawtooth, distributional \u03c7(\u03bb) (only the coincidence limit + local sense forced); the X-linked genomic architecture (needs the feature table, not the promoter-\u03b3); the felt percept of colour and of colour confusion (\u2192 mind volume)."),
])


def body_e10():
    return f"""
<section><h2>What this rung establishes</h2>
<p>Adaptation needs no new machinery. The eye works from starlight to noon \u2014 a range of many orders
of magnitude \u2014 and the reason is already in the E2 switch. The steady state of the frozen field
\u03b3\u00b7s\u2212s\u00b3+h, read on its upper (light-adapted) branch, is the real root of s\u00b3\u2212\u03b3\u00b7s\u2212h = 0;
for a large background drive the cubic dominates, so <strong>s*(h) \u2192 h^(1/3)</strong> \u2014 a
<em>compressive</em> response. On the rod pigment RHO (\u03b3 = {F("1.4719")}, fold h* = {F("0.68733")}) the
ON-branch steady state saturates onto that cube root: s*/h^(1/3) runs {F("1.467434")} \u2192 {F("1.105351")}
\u2192 {F("1.022769")} \u2192 {F("1.004906")} \u2192 {F("1.001057")} \u2192 {F("1.000228")} as the background climbs.
Every one of those is a <em>true</em> zero of the frozen field (residual \u2248 0). This is normal
physiology \u2014 no clinical magnitude is produced. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("Anchor switch (rod pigment RHO)", f"\u03b3 = {F('1.4719')}, fold h* = spinodal(\u03b3) = {F('0.68733')}"),
  ("ON-branch steady state saturates", f"s*/h^(1/3) \u2192 {F('1.000228')} (onto the cube root)"),
  ("Dynamic range (operating sweep)", f"{F('5.000000')} background decades \u2192 {F('1.500207')} response decades"),
  ("Deep-saturation log-compression", f"{F('6.000000')} \u2192 {F('1.990223')} decades = {F('3.014737')} \u2192 n=3"),
  ("Incremental gain falls (light adapt.)", f"{F('2.004737e-01')} (dim) \u2192 {F('1.546844e-04')} (bright), {F('1296.0')}\u00d7"),
  ("Contrast gain \u2192 1/n (Weber)", f"{F('0.136615')} \u2192 \u2026 \u2192 {F('0.333182')}; pure-cube limit {F('0.333333')}"),
])}
<p>A ~5-decade background range is squeezed into a ~1.5-decade response, and deep in the saturated branch
the log-compression is exactly the cubic order <strong>n = 3</strong> ({F("3.014737")}). That is how one
switch spans the eye\u2019s enormous intensity range without pinning at either end.
<span class="grade gF">[F]</span></p></section>

<section><h2>Gain control, and the Weber law it forces</h2>
<p>The incremental gain is ds*/dh = 1/(3s*\u00b2\u2212\u03b3) (the frozen field\u2019s own slope). It <em>falls</em>
monotonically as the background rises \u2014 {F("2.004737e-01")} in dim light down to {F("1.546844e-04")} in
bright, about {F("1296.0")}\u00d7 \u2014 so a bright surround automatically turns the switch down. No separate
machinery is invoked; gain control is a property of the cube\u2019s steady-state curve. The deeper consequence
is the <strong>contrast</strong> gain (the response to a <em>fractional</em> change), (h/s*)\u00b7ds*/dh: on the
saturated branch s*\u2192h^(1/3), so it tends to (h^(2/3))/(3h^(2/3)) = <strong>1/n = 1/3 exactly</strong>. In the
pure-cube limit it is {F("0.333333")} for any background; the real \u03b3-carrying field converges to it
({F("0.136615")} \u2192 {F("0.270194")} \u2192 {F("0.318497")} \u2192 {F("0.330078")} \u2192 {F("0.332629")} \u2192
{F("0.333182")}). Equal fractional steps feel equal \u2014 a Weber-Fechner-like law, <em>forced by the cube and
independent of \u03b3</em>: a different gene\u2019s threshold gives the same limit ({F("0.333301")} for RHO,
{F("0.333306")} for CNGB3 at a large background). <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p>
<p class="muted">Honest scope: this is the <em>saturated</em> branch. Near the fold (small background) the
\u03b3\u00b7s term still matters and the response is steeper than a clean power law \u2014 the Weber regime is the
cube-root tail, stated, not hidden.</p></section>

<section><h2>Two regimes; where \u03b3 and \u03c4 sit</h2>
<p><strong>Dark</strong> (operating point near the fold h* = {F("0.68733")}): the incremental gain is
highest ({F("2.004737e-01")}) and the single-photon <em>flip</em> (E2) gives the detection threshold.
<strong>Bright</strong> (driven deep into the cube root): low gain ({F("1.546844e-04")}), the response
compressed against saturation. Adaptation is the operating point <em>sliding</em> from the fold into the
cube-root tail. \u03b3 is read <strong>read-only</strong>: \u03b3(RHO) = {F("1.4719")} sets <em>where</em> the dark
fold sits (a sensitivity offset), not the compression law \u2014 which is \u03b3-independent, exactly as the band
was \u03c4-not-\u03b3 in E7 and \u03b3 was an offset in E8. The <em>time course</em> of dark re-sensitisation runs on the
frozen Neuron\u2019s recovery \u03c4_s = {F("40.0")} (\u03b2 = {F("0.5")}), the same constant that set the band (E7) and
the rate code (E8); its structure is forced, the absolute seconds are the inherited
<span class="grade gO">[O]</span>. The felt brightness percept is the mind volume\u2019s.
<span class="grade gF">[F]</span></p></section>
""", grade_ledger([
    g("F", "Light/dark adaptation is the same R19 switch on its steady-state ON branch, where the cubic makes the response saturate (s*\u2192h^(1/3)); the incremental gain ds*/dh = 1/(3s*\u00b2\u2212\u03b3) falls with the background (gain control); the CONTRAST gain \u2192 1/n = 1/3 exactly (a Weber-like law), independent of \u03b3; deep-saturation log-compression \u2192 the cubic order n=3; \u03b3 is an offset, not the law."),
    g("V", "Every s* is a true zero of the frozen field (residual \u2248 0); s*/h^(1/3) \u2192 1 monotonically; the gain falls monotonically dim\u2192bright; the contrast gain rises to 1/3 and the pure-cube limit is exactly 0.333333; the two-gene asymptote agrees; \u03c4_s/\u03b2 and \u03b3 are byte-equal to the frozen substrate/atlas."),
    g("L", "\u03b3(RHO), \u03b3(CNGB3) from NCBI promoters (cached, read-only); Weber\u2019s law and the brightness power-law exponent (~1/3) are the cited psychophysics this matches."),
    g("O", "The absolute background\u2192drive\u2192firing scale (inherited E2/E5) \u2014 so no absolute threshold, Weber fraction, or luminance unit is produced; the absolute \u03c4\u2192seconds of dark adaptation (inherited E7/E8); the molecular adaptation machinery (Ca\u00b2\u207a feedback, pigment bleaching/regeneration) \u2014 the substrate captures the compression, not that feedback loop; the felt brightness percept (\u2192 mind volume). Each obstacle named."),
])


def body_e11():
    # FIREWALL: this body carries NO quantitative clinical token and NO '%'. No power magnitude (the
    # word/unit dioptre is blocked), no axial length (mm is blocked) \u2014 only dimensionless RATIOS and
    # SIGNS appear. gate_volume re-checks the rendered chapter against E11's own MAGNITUDE_BLOCK.
    return f"""
<aside class="scope"><strong>Scope \u2014 theoretical, non-clinical.</strong> This chapter extends E3's
reduced-eye optics to ask, as a question in geometry, how a single refracting eye stays in focus. It
covers a normal mechanism (accommodation) and the mechanism layer of the two commonest refractive
conditions (myopia = near-sighted, hyperopia = far-sighted), and because it touches a condition layer it
is firewalled like the other clinical chapters: it does not diagnose, treat, prescribe, screen, classify a
person, or triage; it designs no molecule and states no clinical quantity \u2014 here the firewall additionally
blocks any power magnitude and any length, so the whole chapter speaks in dimensionless ratios and signs
only. The felt percept of blur or clarity is deferred to the mind volume.</aside>

<section><h2>What this rung establishes</h2>
<p>From E3, a single refracting surface obeys n\u2082/v \u2212 n\u2081/u = P with power P = (n\u2082\u2212n\u2081)/R, so a distant
object images at v_\u221e = n\u2082/P. The retina sits at the eye's axial length L, so the eye is in focus for
distance exactly when v_\u221e = L \u2014 that is, when <strong>P\u00b7L = n\u2082</strong>: a single, dimensionless
<em>match</em> between the eye's <strong>power</strong> (optics) and its <strong>length</strong> (growth).
Define the match ratio <strong>\u03c1 \u2261 P\u00b7L/n\u2082</strong>. On E3's frozen Emsley reduced eye (consumed index
n\u2082 = {F("1.333333")}) the ratio is \u03c1 = {F("1.000000")} <em>exactly</em> \u2014 the cited n and R cohere, this
is not a fit. Emmetropia is not one eye but a whole <em>curve</em>: the product P\u00b7L is fixed, so a longer
eye is emmetropic with proportionally less power. <span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("Emmetropic match (frozen reduced eye)", f"\u03c1 = P\u00b7L/n\u2082 = {F('1.000000')} (exact); n\u2082 = {F('1.333333')}"),
  ("Myopia side (focus in front)", f"\u03c1 = {F('1.050000')} \u2014 too long (axial) OR too powerful (refractive)"),
  ("Hyperopia side (focus behind)", f"\u03c1 = {F('0.950000')}"),
  ("Only the product matters", f"stronger \u00d7 shorter (q\u00b7\u2113 with \u2113 = {F('0.952381')}) \u21d2 \u03c1 = {F('1.000000')}"),
  ("Accommodation, far \u2192 near (P_req/P_\u221e)", f"{F('1.000750')} \u2192 {F('1.007500')} \u2192 {F('1.030000')} \u2192 {F('1.075000')} \u2192 {F('1.187500')} \u2192 {F('1.375000')}"),
  ("Lens rounding at the near end (R_req/R_\u221e)", f"{F('0.727273')} (R\u2193 \u21d2 P\u2191, one-signed)"),
])}
<p>The mismatch sign is the only thing stated: since L \u2212 v_\u221e = (P\u00b7L \u2212 n\u2082)/P, the side is
sign(\u03c1\u22121). How much error, the axial length, the spectacle power \u2014 all firewall-blocked
<span class="grade gO">[O]</span>; none is named. <span class="grade gF">[F]</span></p></section>

<section><h2>Refractive error is a signed mismatch \u2014 two independent routes</h2>
<p>The distant focus is v_\u221e = n\u2082/P and the retina is at L, so the blur side follows the sign of the
mismatch directly. <strong>\u03c1 &gt; 1</strong> puts the distant focus <em>in front</em> of the retina \u2014
<strong>myopia</strong>; <strong>\u03c1 &lt; 1</strong> puts it <em>behind</em> \u2014 <strong>hyperopia</strong>.
Crucially the <em>same</em> error is reachable two independent ways: an eye that is too <strong>long</strong>
(axial) or too <strong>powerful</strong> (refractive) both raise \u03c1 above 1 (here both to {F("1.050000")}),
and both give myopia \u2014 the match cares only about the product P\u00b7L, which is why a stronger eye made
compensatingly shorter returns to \u03c1 = {F("1.000000")}. The correction is stated only as a direction
(myopia \u21d2 reduce power; hyperopia \u21d2 add power). <span class="grade gF">[F]</span></p></section>

<section><h2>Accommodation is a one-signed power lever</h2>
<p>A near object needs <em>more</em> power than a distant one to image on the same retina. For an object at
u = \u2212k\u00b7L (k = distance in eye-lengths), the required power is P_req/P_\u221e = 1 + n\u2081/(n\u2082\u00b7k) \u2014 a pure
number that rises monotonically as the object nears: {F("1.000750")} \u2192 {F("1.007500")} \u2192
{F("1.030000")} \u2192 {F("1.075000")} \u2192 {F("1.187500")} \u2192 {F("1.375000")} as k falls. It is always at
least 1, so accommodation is a strictly <strong>one-signed</strong> (additive) lever: the eye can only
<em>round</em> the lens (R\u2193 \u21d2 P\u2191, the radius ratio R_req/R_\u221e dropping to {F("0.727273")} at the near
end) to pull focus nearer, never the reverse. The far point is the relaxed lever (the ratio \u2192 1 at
distance); the near point is the lever maxed. The amplitude, the near and far distances, and the
presbyopic decline with age are the firewall-blocked <span class="grade gO">[O]</span>.
<span class="grade gF">[F]</span></p></section>

<section><h2>The lever is lattice geometry; the length axis is a dwell-size</h2>
<p>The power lever is the same lattice geometry as E3: P = (n\u2082\u2212n\u2081)/R, so P \u221d 1/R and the lens rounding
is a purely geometric modulation of the transverse-match interface (dP/P = \u2212dR/R), with n = c_vac/c_med =
\u221a((B/\u03c1) ratio) the inherited meaning of refractive index. The other axis, <em>length</em>, is growth: in
the substrate organ size = dwell \u221d \u03b3^1.5 (E1), so the eye's axial length is a <em>dwell-size</em>. Reading
the eye-field master PAX6 read-only (byte-equal to the atlas, \u03b3 = {F("1.5110")}; RAX \u03b3 = {F("1.4538")})
instantiates that law \u2014 the relative size PAX6/RAX = (\u03b3_PAX6/\u03b3_RAX)^1.5 = {F("1.059595")} \u2014 and the law
is monotone in \u03b3, so the growth axis has a forced <em>direction</em>: more ocular growth \u21d2 a longer eye \u21d2
the myopic side of the match. The gene\u2192elongation map, the emmetropization feedback that normally holds
\u03c1 \u2248 1 in a growing eye, and the absolute scale are the named <span class="grade gO">[O]</span>; \u03b3 is
promoter structure only \u2014 never an optical power, a growth rate, or a clinical effect.</p></section>
""", grade_ledger([
    g("F", "Emmetropia is the power\u2194length match \u03c1 = P\u00b7L/n\u2082 = 1 (a curve, not one eye); the mismatch SIGN fixes the side (\u03c1>1 myopia / focus in front, \u03c1<1 hyperopia / behind), reachable two independent ways (too long OR too powerful \u2014 only the product matters); accommodation is a one-signed (additive) monotone power lever via lens rounding (R\u2193 \u21d2 P\u2191); the lever is geometry (dP/P = \u2212dR/R); the length axis is the substrate size law dwell \u221d \u03b3^1.5."),
    g("V", "\u03c1 = 1 exactly on the frozen reduced eye; the geometric blur side equals sign(\u03c1\u22121) on E3's own surface equation for both the axial and refractive routes; an equal-product eye returns to \u03c1 = 1; P_req/P_\u221e rises monotonically and stays at least 1, and the implied lens radius images the near object onto the retina; dP/P = \u2212dR/R; the eye-field \u03b3 is byte-equal to the atlas."),
    g("V", "The single-surface imaging itself is E3's classical ray arithmetic (consumed, not re-derived); E11 adds only the dimensionless match reading on top of it."),
    g("L", "The Emsley reduced-eye n and R (cited, via E3); \u03b3(PAX6), \u03b3(RAX) from NCBI promoters (cached, read-only); that myopia is either axial or refractive is the cited optics this matches."),
    g("O", "The magnitude of any refractive error / the axial length / the spectacle power / the accommodation amplitude / the near and far distances / the presbyopic decline (all firewall-blocked \u2014 none produced); the gene\u2192ocular-elongation map and the emmetropization feedback that normally holds \u03c1 \u2248 1 (needs growth biology, not the promoter-\u03b3); the chromatic/aberration coupling (inherited E3); the felt percept of blur or clarity (\u2192 mind volume)."),
])


def body_e12():
    # FIREWALL: this body carries NO quantitative clinical token and NO '%'. Only R19 field values
    # (s, \u03b3, h*, the fold and its loop width) appear \u2014 every stress is a dimensionless multiple of
    # the gene's OWN fold. gate_volume re-checks the rendered chapter against E12's MAGNITUDE_BLOCK.
    return f"""
<aside class="scope"><strong>Scope \u2014 theoretical, non-clinical.</strong> This chapter studies the
<em>mechanism layer</em> of acquired, degenerative eye disease (the late picture shared across age-related
macular degeneration, glaucoma and diabetic retinopathy) as a question in dynamical-systems theory. Because
it touches a disease layer it is firewalled like the other clinical chapters: it does not diagnose, treat,
prescribe, screen, stage, classify a person, or triage; it designs no molecule and states no clinical
quantity. Every stress here is a <em>dimensionless multiple of the gene's own fold</em> \u2014 no absolute
scale, no clinical magnitude, no percent sign. The felt loss of sight is deferred to the mind volume.</aside>

<section><h2>What this rung establishes</h2>
<p>E4 read a congenital switch as one <em>born below its fold</em>: the drive never clears the spinodal, so
the all-or-none switch is static and <em>never flips</em>. A degenerative disease is the opposite history on
the same frozen field \u2014 a switch that <strong>started healthy</strong> (settled ON, s&gt;0) and is carried
<em>over</em> its own fold by a slowly accumulating stress. On RHO (read-only, \u03b3 = {F("1.4719")}, fold
h*(\u03b3) = {F("0.687330")}, barrier \u03b3\u00b2/4 = {F("0.541622")}) the healthy state settles at
s = {F("1.316420")} and tracks the upper branch as the drive is ramped quasi-statically down (step
\u0394h = {F("0.003878")}); it stays ON through h = 0, last ON at h = {F("-0.687977")}, then at
h = {F("-0.691855")} <strong>collapses in one step</strong> to the degenerate basin (s = {F("-1.401928")}).
The collapse drive is the analytic fold \u2212h* = {F("-0.687330")} (gap {F("0.004525")}, just
{F("1.1667")}\u00d7 the ramp step), and a different healthy start collapses at the same fold
(h = {F("-0.689701")}). Smooth, then sudden: a <strong>tipping point</strong>, E4's spinodal reached
dynamically from the ON side \u2014 the difference between <em>was lost</em> and <em>never flipped</em>.
<span class="grade gF">[F]</span><span class="grade gV">[V]</span></p></section>

<section><h2>Key results</h2>
{kv([
  ("Worked gene (READ-ONLY)", f"RHO \u03b3 = {F('1.4719')}, fold h* = {F('0.687330')}, barrier = {F('0.541622')}"),
  ("Healthy operating point settles ON", f"s = {F('1.316420')} (s&gt;0)"),
  ("Collapse from ON at the fold", f"last ON h = {F('-0.687977')} \u2192 collapse h = {F('-0.691855')} (\u2212h* = {F('-0.687330')})"),
  ("Start-independent (the same fold)", f"a different healthy start collapses at h = {F('-0.689701')}"),
  ("Hysteresis loop width = 2\u00b7h*", f"recover \u2212 collapse = {F('1.383710')} (analytic {F('1.374661')})"),
  ("Basin-shallowing route, same locus", f"erode \u03b3 to {F('0.841231')} under load {F('-0.300000')}; fold h*(\u03b3) = {F('0.296976')} meets it"),
])}
<p>Only directions and signs are stated \u2014 that the state is ON before the fold and degenerate after, that
recovery needs the opposite fold, that a lower \u03b3 tips sooner. Every magnitude (the absolute stress scale,
the irreversibility margin, any staging or prognosis) is firewall-blocked
<span class="grade gO">[O]</span>; none is produced. <span class="grade gF">[F]</span></p></section>

<section><h2>Because the transition is a fold, it is hysteretic \u2014 early differs from late</h2>
<p>Run the stress backwards from the collapsed state (raise the drive): the state does <em>not</em> recover at
the drive where it fell. It stays degenerate through the pre-collapse drive and only re-flips ON
(s = {F("1.401928")}) at the <em>opposite</em> fold +h* = {F("0.687330")}, the drive h = {F("0.691855")}.
Collapse (\u2212h*) and recovery (+h*) are therefore different drives, and the loop width
h_recover \u2212 h_collapse = {F("1.383710")} (the analytic 2\u00b7h*(\u03b3) = {F("1.374661")}) is the
<strong>irreversibility margin</strong>: recovery demands <em>over-correction past</em> +h*, not merely
undoing the stress. This is the substrate's account of why acting on the upper branch <em>before</em> the
fold is categorically unlike acting <em>after</em> \u2014 why early and late are different in kind, not degree.
The margin's magnitude is the firewall-blocked <span class="grade gO">[O]</span>; only that the two folds
<em>differ</em> is stated. <span class="grade gF">[F]</span><span class="grade gO">[O]</span></p></section>

<section><h2>One geometry, many routes \u2014 the multifactorial unification</h2>
<p>AMD, glaucoma and diabetic retinopathy carry <em>three different</em> primary stresses, yet the substrate
says any bistable transducer fails the <em>same</em> way \u2014 by a fold \u2014 whichever parameter the stress
rides. A <strong>load route</strong> moves the drive: at fixed \u03b3 = {F("1.4719")} an anti-drive collapses
the switch at h = {F("-0.691855")} \u2248 \u2212h*(\u03b3) = {F("-0.687330")}. A <strong>basin-shallowing route</strong>
instead erodes \u03b3 under a held load h = {F("-0.300000")} (cell still ON, s = {F("1.094434")}): the fold
itself h*(\u03b3) = 2(\u03b3/3)^1.5 <em>shrinks</em>, rising to meet the fixed load, and (step
\u0394\u03b3 = {F("0.003047")}) collapses at \u03b3 = {F("0.841231")}, where the shrinking fold
h*(\u03b3) = {F("0.296976")} has met the load |h| = {F("0.300000")} (analytic crossing \u03b3_crit =
{F("0.846932")}). <strong>Both routes land on the one fold locus</strong> h = \u2212h*(\u03b3): at the
\u03b3-erosion collapse the load {F("-0.300000")} sits on \u2212h*(\u03b3) = {F("-0.296976")} (gap
{F("0.003024")}). Same saddle-node, different parameter moved \u2014 so the shared <em>late</em> picture is
forced. What the substrate does <em>not</em> fix is the <em>identity</em> of the primary stress (oxidative
vs mechanical vs metabolic): a named <span class="grade gO">[O]</span>.</p></section>

<section><h2>\u03b3 as STRUCTURAL fragility \u2014 and the loudest caveat in the volume</h2>
<p>A shallower basin tips under a smaller stress: a lower \u03b3 means both a smaller barrier \u03b3\u00b2/4 and a
smaller fold h*(\u03b3), so the atlas genes carry a <em>structural</em> fragility ordering by spinodal (read-only,
byte-equal to the frozen atlas) \u2014 most fragile CNGB3 (\u03b3 = {F("1.2425")}, h* = {F("0.533080")}) through
stiffest PDE6B (\u03b3 = {F("1.5354")}, h* = {F("0.732285")}), a fold ratio of {F("1.373687")}, monotone in
\u03b3. This is a <em>structural</em> ordering, never a clinical risk ranking (that would be firewall-blocked).</p>
<p class="muted"><strong>Brutal caveat (loudest in this chapter):</strong> the map from a real
degenerative-disease risk locus to a \u03b3-shift is a named <span class="grade gO">[O]</span> that is
<em>even more open</em> than the monogenic lesions of E4. These diseases are multifactorial, age- and
environment-gated and polygenic \u2014 common variants of small effect, mostly <em>outside</em> a promoter \u2014
so the promoter-\u03b3 this package reads has essentially <em>no monogenic purchase</em> here. The chapter's
content is the dynamical-systems <em>structure</em> (the static\u2194dynamic distinction, the hysteresis, the
one-geometry-many-routes), not a disease prediction. The felt loss of sight is deferred to the mind
volume.</p></section>
""", grade_ledger([
    g("F", "A degenerative disease is a switch carried OVER its fold (dynamic; started ON, s>0), categorically unlike the congenital switch born below it (static, never flips \u2014 E4); a fold-mediated collapse is HYSTERETIC (collapse at \u2212h*, recovery only at +h*, loop width 2\u00b7h*); any bistable transducer fails by the SAME fold whatever parameter the stress rides (load route OR basin-shallowing route, both on the one locus h=\u2212h*(\u03b3)); a shallower basin (lower \u03b3) tips under less stress (spinodal monotone in \u03b3) \u2014 a STRUCTURAL fragility ordering, not a clinical one."),
    g("V", "On the frozen field the down-ramp from ON collapses at \u2212h* (within the ramp step) and is independent of the healthy start; the up-ramp from the collapsed state recovers only at +h*; the \u03b3-erosion route collapses where h*(\u03b3)=|load| and lands on h=\u2212h*(\u03b3); the fragility ordering is monotone; every \u03b3 is byte-equal to the atlas. The magnitude firewall is machine-checked."),
    g("L", "Every retinal-master \u03b3 (NCBI promoters, cached, read-only); that AMD/glaucoma/diabetic retinopathy are acquired, multifactorial degenerations is the cited disease framing this matches."),
    g("O", "The IDENTITY and rate of the primary stress for any specific disease (oxidative vs mechanical vs metabolic \u2014 the substrate fixes the geometry, not the route); the MAP from a real risk locus to a \u03b3-shift (even more open than E4 \u2014 polygenic, age/environment-gated, mostly non-promoter common variants); the irreversibility-margin magnitude / the absolute stress scale / any clinical staging or prognosis (all firewall-blocked \u2014 none produced); the felt percept and felt LOSS of sight (\u2192 mind volume). Each obstacle named."),
])


BODIES = {
    "e0-carrier": body_e0, "e1-angle-to-cone": body_e1, "e2-single-photon-switch": body_e2,
    "e3-image-formation": body_e3, "e4-congenital-blindness": body_e4,
    "e5-frequency-ladder": body_e5, "e6-why-visible": body_e6,
    "e7-cascade-lowpass": body_e7, "e8-graded-to-spike-rate": body_e8,
    "e9-red-green-dichromacy": body_e9, "e10-light-dark-adaptation": body_e10,
    "e11-accommodation-refraction": body_e11, "e12-acquired-degeneration": body_e12,
}


# ==============================================================================================
# rendering machinery
# ==============================================================================================
M = L.META


def _jsonld(ch, page_url):
    crumbs = [("Home", M["site"] + "/"),
              ("The Eye Volume", M["base"]),
              (f"{ch['num']} \u2014 {ch['title'].split(' \u2014 ')[0]}", page_url)]
    graph = [
        {
            "@type": "TechArticle",
            "headline": f"{ch['num']} \u2014 {ch['title']}",
            "description": ch["one_liner"],
            "inLanguage": "en",
            "url": page_url,
            "isPartOf": {"@type": "Book", "name": M["title"], "url": M["base"]},
            "author": {"@type": "Person", "name": M["author"],
                       "identifier": f"https://orcid.org/{M['orcid']}"},
            "license": M["license_url"],
            "creativeWorkStatus": "theoretical research, non-clinical",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                for i, (n, u) in enumerate(crumbs)
            ],
        },
    ]
    obj = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(obj, ensure_ascii=False, indent=2)


def _repro_strip(runs_meta):
    """The reproducibility strip: per-run sha + a collapsible verbatim transcript (the SSOT)."""
    blocks = []
    for rm in runs_meta:
        pre = ('<pre class="transcript" data-run="%s" data-sha="%s">%s</pre>'
               % (L.attr(rm["path"]), rm["sha256"], L.esc(rm["transcript"])))
        blocks.append(
            '<details class="repro"><summary><span class="mono">%s</span>'
            '<span class="sha">sha256 %s</span></summary>%s</details>'
            % (L.attr(rm["path"]), rm["sha256"][:24] + "\u2026", pre)
        )
    note = ('<p class="muted">Every number on this page is the code\u2019s own output. The transcript'
            ' below is the verbatim, hash-pinned stdout of the listed module(s); '
            '<code>tools/gate_volume.py</code> re-runs them and asserts HTML\u2194code drift 0.</p>')
    return ('<section class="reproduction"><h2>Reproducibility</h2>' + note
            + "".join(blocks) + "</section>")


def render_page(ch, idx):
    global _CUR_TRANSCRIPT, _CUR_FACTS
    # 1) capture the live transcript(s) — the single source of every number on the page
    runs_meta = []
    parts = []
    for rel in ch["runs"]:
        t = L.run_capture(rel)
        parts.append(t)
        runs_meta.append({"path": rel, "transcript": t, "sha256": L.sha256_text(t)})
    _CUR_TRANSCRIPT = "".join(parts)
    _CUR_FACTS = []

    # 2) editorial body (F() asserts each prose number is in _CUR_TRANSCRIPT)
    body_html, ledger_html = BODIES[ch["slug"]]()

    # 3) chrome
    page_url = M["base"] + ch["slug"] + "/"
    title_full = f"{ch['num']} \u2014 {ch['title']} | VP Eye Volume"
    prevc = VOLUME[idx - 1] if idx > 0 else None
    nextc = VOLUME[idx + 1] if idx < len(VOLUME) - 1 else None
    nav = ['<nav class="pager">']
    nav.append(f'<a class="prev" href="../{prevc["slug"]}/">\u2190 {prevc["num"]}</a>' if prevc
               else '<a class="prev disabled">\u2190</a>')
    nav.append('<a class="up" href="../">Volume contents</a>')
    nav.append(f'<a class="next" href="../{nextc["slug"]}/">{nextc["num"]} \u2192</a>' if nextc
               else '<a class="next disabled">\u2192</a>')
    nav.append('</nav>')
    nav = "".join(nav)

    crumb = (f'<nav class="crumb" aria-label="Breadcrumb"><a href="{M["base"]}">VP Eye Volume</a>'
             f' / <span>{ch["num"]}</span></nav>')

    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{L.attr(title_full)}</title>
<meta name="description" content="{L.attr(ch['one_liner'])}">
<link rel="canonical" href="{L.attr(page_url)}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="../assets/volume.css">
<script type="application/ld+json">
{_jsonld(ch, page_url)}
</script>
</head>
<body>
<header class="topbar"><a class="brand" href="{M['base']}">VP \u00b7 The Eye Volume</a>
<span class="tag">theoretical research \u00b7 non-clinical \u00b7 {M['license']}</span></header>
<main class="chapter">
{crumb}
<h1>{ch['num']} <span class="sub">{L.esc(ch['title'])}</span></h1>
<p class="lead">{L.esc(ch['one_liner'])}</p>
{body_html}
{ledger_html}
{_repro_strip(runs_meta)}
{nav}
</main>
<footer class="foot">
<p>{M['title']} \u00b7 {M['author']} (<a href="https://orcid.org/{M['orcid']}">ORCID {M['orcid']}</a>)
\u00b7 <a href="{M['license_url']}">{M['license']}</a> \u00b7 concept DOI {M['doi_concept']}.</p>
<p class="muted">Mechanism-layer theory only. No diagnosis, no treatment, no clinical magnitudes. The felt
percept of sight is deferred to the mind volume.</p>
</footer>
</body>
</html>
"""
    # 4) write page + facts manifest
    outdir = os.path.join(L.DOCS, ch["slug"])
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(head)

    facts_dir = os.path.join(L.DOCS, "facts")
    os.makedirs(facts_dir, exist_ok=True)
    facts_obj = {
        "chapter": ch["slug"], "num": ch["num"], "title": ch["title"],
        "runs": [{"path": rm["path"], "sha256": rm["sha256"]} for rm in runs_meta],
        "facts": _CUR_FACTS,
    }
    with open(os.path.join(facts_dir, ch["slug"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(facts_obj, f, ensure_ascii=False, indent=2)
    return len(_CUR_FACTS), [rm["sha256"] for rm in runs_meta]


# ---- the hub ---------------------------------------------------------------------------------
LADDER_SVG = """<svg viewBox="0 0 880 150" class="ladder" role="img"
 aria-label="The down-conversion ladder from a 10^14 Hz carrier to a 10-100 Hz spike rate">
<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
<path d="M0,0 L7,3 L0,6 Z" fill="currentColor"/></marker></defs>
<g font-size="13" text-anchor="middle">
<rect x="8"   y="40" width="150" height="56" rx="8" class="box"/>
<text x="83" y="63">~10\u00b9\u2074 Hz carrier</text><text x="83" y="82" class="dim">angle \u03c7(\u03bb) = colour</text>
<rect x="208" y="40" width="150" height="56" rx="8" class="box"/>
<text x="283" y="63">R19 event-detector</text><text x="283" y="82" class="dim">one photon \u2192 one flip</text>
<rect x="408" y="40" width="150" height="56" rx="8" class="box"/>
<text x="483" y="63">cascade low-pass</text><text x="483" y="82" class="dim">f_c = \u03b2/(2\u03c0\u03c4)</text>
<rect x="608" y="40" width="150" height="56" rx="8" class="box"/>
<text x="683" y="63">spike RATE</text><text x="683" y="82" class="dim">~10\u2013100 Hz</text>
<line x1="160" y1="68" x2="206" y2="68" stroke="currentColor" marker-end="url(#ar)"/>
<line x1="360" y1="68" x2="406" y2="68" stroke="currentColor" marker-end="url(#ar)"/>
<line x1="560" y1="68" x2="606" y2="68" stroke="currentColor" marker-end="url(#ar)"/>
<text x="772" y="72" text-anchor="start" class="dim">\u2192 mind</text>
</g></svg>"""


def render_hub(page_shas):
    page_url = M["base"]
    toc = []
    for c in VOLUME:
        toc.append(
            f'<li><a href="{c["slug"]}/"><span class="cnum">{c["num"]}</span>'
            f'<span class="ctitle">{L.esc(c["title"])}</span></a>'
            f'<p class="cone">{L.esc(c["one_liner"])}</p></li>'
        )
    toc_html = '<ol class="toc">' + "".join(toc) + "</ol>"

    abstract = (
        "<p>This volume walks the complete high\u2192low <strong>down-conversion ladder</strong> by "
        "which the eye turns a ~10\u00b9\u2074 Hz electromagnetic carrier into a ~10\u2013100 Hz neural spike "
        "code. The thesis, proved rung by rung on a frozen R19 substrate and a DNA reading measured "
        "from public NCBI promoters, is that the eye down-converts by <em>event-detection + low-pass "
        "integration, not by mixing</em>: a single photon\u2019s energy drives one discrete all-or-none "
        "flip (the carrier frequency is discarded), the cascade\u2019s time-constant sets the surviving "
        "band, and the carrier\u2019s identity \u2014 colour \u2014 is preserved orthogonally in the propagation "
        "angle \u03c7(\u03bb), which is why colour survives a ~13-order frequency collapse. WHERE (the image) "
        "is geometry too.</p>"
    )

    grades = (
        "<table class=\"gtable\"><tbody>"
        + g("F", "forced \u2014 the wave emergence, the angle law, the R19 switch structure, the "
                 "emergence order argsort(spinodal(\u03b3)), the DNA reading \u03b3 (LEVEL) + A4 (SHAPE).")
        + g("V", "verified \u2014 deterministic recomputation (2\u00d7sha256) of every displayed number, "
                 "byte-identical across runs, HTML\u2194code drift 0.")
        + g("L", "measured/calibrated \u2014 every \u03b3 from NCBI promoters (cached); the cited "
                 "wavelengths and schematic-eye constants.")
        + g("O", "open \u2014 the absolute Hz at every ladder rung (only the collapse RATIO is forced); "
                 "the chromophore energy that pins the visible band; the felt percept (\u2192 mind volume).")
        + "</tbody></table>"
    )

    obj = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": M["title"],
        "inLanguage": "en",
        "url": page_url,
        "author": {"@type": "Person", "name": M["author"],
                   "identifier": f"https://orcid.org/{M['orcid']}"},
        "license": M["license_url"],
        "about": "first-principles theory of how vision emerges; the high\u2192low down-conversion ladder",
        "creativeWorkStatus": "theoretical research, non-clinical",
        "hasPart": [{"@type": "TechArticle", "name": f"{c['num']} \u2014 {c['title']}",
                     "url": page_url + c["slug"] + "/"} for c in VOLUME],
    }
    jsonld = json.dumps(obj, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{L.attr(M['title'])}</title>
<meta name="description" content="A first-principles, fully-reproducible theory of how vision emerges: the high\u2192low down-conversion ladder E0\u2192E8 from a 10^14 Hz carrier to a 10-100 Hz spike rate. Theoretical research, non-clinical.">
<link rel="canonical" href="{L.attr(page_url)}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/volume.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>
<header class="topbar"><a class="brand" href="{page_url}">VP \u00b7 The Eye Volume</a>
<span class="tag">theoretical research \u00b7 non-clinical \u00b7 {M['license']}</span></header>
<main class="hub">
<h1>The Eye Volume <span class="sub">the high\u2192low down-conversion ladder (E0\u2192E8)</span></h1>
<p class="lead">How the eye turns a ~10\u00b9\u2074 Hz light carrier into a ~10\u2013100 Hz neural spike code \u2014
by event-detection and low-pass integration, not mixing. Colour survives the ~13-order collapse because
it is geometry (the propagation angle \u03c7), not a frequency the receptor could follow.</p>

<aside class="scope"><strong>Scope \u2014 theoretical, non-clinical.</strong> This is purely academic
computational research, not a medical product and not medical advice. The congenital-blindness chapter
(E4) studies the mechanism layer only \u2014 direction-only and proposal-only behind a machine-checked
magnitude firewall. It does not diagnose, treat, prescribe, or quantify. The felt percept of sight is
deferred to the mind volume.</aside>

<figure class="ladderfig">{LADDER_SVG}
<figcaption>The spine: carrier \u2192 single-photon R19 event-detector \u2192 cascade low-pass (f_c=\u03b2/(2\u03c0\u03c4))
\u2192 spike rate. Colour (angle) and place (image) ride through as geometry.</figcaption></figure>

<section><h2>Abstract</h2>{abstract}</section>

<section><h2>Contents</h2>{toc_html}</section>

<section class="grades"><h2>Grades across the volume <span class="muted">(VP-SPEC C3)</span></h2>{grades}</section>

<section><h2>Reproducibility</h2>
<p>The reproduction master is this HTML. Every quantitative claim is regenerated by the increment
modules under <code>research/</code> and the frozen foundation under <code>inherited/</code>; each
chapter embeds the verbatim, hash-pinned transcript of its source module(s). Rebuild and check from the
package root:</p>
<pre class="cmd">python3 tools/verify_seed.py     # SEED VERIFY: PASS  (foundation frozen, determinism, no-omission)
python3 tools/build_volume.py    # regenerate docs/eye/ from the run.py outputs
python3 tools/gate_volume.py     # VOLUME GATE: PASS  (HTML\u2194code drift 0, firewall, retrieval-ready)</pre>
<p class="muted">No number here is fitted: \u03b3 is measured (never tuned), the carrier \u03bd=c/\u03bb and quantum
E=h\u03bd use SI-exact constants, and the substrate is byte-frozen (SEED=19). Each open quantity is graded
<span class="grade gO">[O]</span> with its obstacle named.</p>
</section>
</main>
<footer class="foot">
<p>{M['title']} \u00b7 {M['author']} (<a href="https://orcid.org/{M['orcid']}">ORCID {M['orcid']}</a>)
\u00b7 <a href="{M['license_url']}">{M['license']}</a> \u00b7 concept DOI {M['doi_concept']}.</p>
</footer>
</body>
</html>
"""
    with open(os.path.join(L.DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ---- static assets (CSS) + retrieval-readiness files -----------------------------------------
CSS = """:root{
  --ink:#1a1d24; --dim:#5b6470; --line:#dfe3ea; --bg:#ffffff; --panel:#f6f8fb;
  --accent:#1f6f8b; --F:#0a7d33; --V:#1f6f8b; --Lc:#7a5c00; --O:#b23a48;
  --mono:"SFMono-Regular",ui-monospace,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);background:var(--bg);
  font-family:Georgia,"Times New Roman",serif;line-height:1.62;
  font-size:18px;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;
  padding:12px 22px;border-bottom:1px solid var(--line);background:var(--panel);
  font-family:system-ui,sans-serif;font-size:13px}
.topbar .brand{font-weight:700;color:var(--ink)}
.topbar .tag{color:var(--dim);letter-spacing:.02em}
main{max-width:820px;margin:0 auto;padding:30px 22px 64px}
h1{font-size:30px;line-height:1.2;margin:.4em 0 .15em}
h1 .sub{display:block;font-size:17px;color:var(--dim);font-weight:400;margin-top:.35em}
h1 .cnum,h1 .num{color:var(--accent)}
h2{font-size:21px;margin:1.7em 0 .5em;padding-bottom:.2em;border-bottom:1px solid var(--line)}
.lead{font-size:20px;color:#2a2f38;margin:.2em 0 1.1em}
.sub{font-weight:400}
.crumb{font-family:system-ui,sans-serif;font-size:13px;color:var(--dim);margin-bottom:.4em}
p{margin:.7em 0}
code{font-family:var(--mono);font-size:.86em;background:var(--panel);padding:.05em .35em;border-radius:4px}
em{font-style:italic}
.muted,.dim{color:var(--dim)}
.muted{font-size:15.5px}
/* scope / firewall banner */
.scope{background:#fff7f4;border:1px solid #f1d6cf;border-left:4px solid var(--O);
  padding:12px 16px;border-radius:8px;font-size:15.5px;margin:1.1em 0}
/* grade chips */
.grade{font-family:var(--mono);font-size:.72em;font-weight:700;padding:.06em .3em;border-radius:4px;
  margin-left:.25em;vertical-align:.06em;white-space:nowrap}
.gF{color:#fff;background:var(--F)} .gV{color:#fff;background:var(--V)}
.gL{color:#fff;background:var(--Lc)} .gO{color:#fff;background:var(--O)}
/* key/value list */
.kvlist{display:grid;grid-template-columns:1fr;gap:0;margin:1em 0;border:1px solid var(--line);
  border-radius:10px;overflow:hidden}
.kv{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:10px;
  padding:9px 14px;border-top:1px solid var(--line);font-size:16px}
.kv:first-child{border-top:0}
.kv dt{margin:0;color:var(--dim)}
.kv dd{margin:0;font-family:var(--mono);font-size:14.5px;color:var(--ink)}
/* grade ledger table */
.gtable{width:100%;border-collapse:collapse;margin:.4em 0;font-size:15.5px}
.gtable td{vertical-align:top;padding:7px 10px;border-top:1px solid var(--line)}
.gtable td.grade{width:42px;font-family:var(--mono);font-weight:700}
.gtable td.gF{color:var(--F)} .gtable td.gV{color:var(--V)}
.gtable td.gL{color:var(--Lc)} .gtable td.gO{color:var(--O)}
/* reproducibility */
.reproduction{margin-top:1.8em;padding-top:.3em}
details.repro{border:1px solid var(--line);border-radius:8px;margin:.5em 0;background:var(--panel)}
details.repro summary{cursor:pointer;padding:9px 14px;font-family:system-ui,sans-serif;font-size:13px;
  display:flex;justify-content:space-between;gap:12px;align-items:center}
details.repro .sha{color:var(--dim);font-family:var(--mono)}
.mono{font-family:var(--mono)}
pre.transcript,pre.cmd{font-family:var(--mono);font-size:12.5px;line-height:1.5;white-space:pre;
  overflow:auto;background:#0f1420;color:#d6e0ef;padding:14px 16px;border-radius:0 0 8px 8px;margin:0}
pre.cmd{border-radius:8px;font-size:13px}
/* pager */
.pager{display:flex;justify-content:space-between;gap:10px;margin-top:2.2em;padding-top:1em;
  border-top:1px solid var(--line);font-family:system-ui,sans-serif;font-size:14px}
.pager a{padding:6px 12px;border:1px solid var(--line);border-radius:8px}
.pager a.disabled{color:var(--line);pointer-events:none}
/* hub */
.toc{list-style:none;padding:0;margin:1em 0;counter-reset:none}
.toc li{border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:.55em 0}
.toc a{display:flex;gap:12px;align-items:baseline;color:var(--ink);font-weight:600;font-size:18px}
.toc .cnum{font-family:var(--mono);color:var(--accent);font-weight:700;min-width:34px}
.toc .cone{margin:.35em 0 0;color:var(--dim);font-size:15px;font-weight:400}
.ladderfig{margin:1.4em 0}
.ladder{width:100%;height:auto;color:var(--accent)}
.ladder .box{fill:var(--panel);stroke:var(--line)}
.ladder text{fill:var(--ink);font-family:system-ui,sans-serif}
.ladder text.dim{fill:var(--dim);font-size:11px}
figcaption{color:var(--dim);font-size:14.5px;margin-top:.5em}
.foot{max-width:820px;margin:0 auto;padding:20px 22px 50px;border-top:1px solid var(--line);
  color:var(--dim);font-family:system-ui,sans-serif;font-size:13px}
@media (max-width:560px){.kv{grid-template-columns:1fr;gap:2px}body{font-size:17px}}
"""


def write_assets():
    adir = os.path.join(L.DOCS, "assets")
    os.makedirs(adir, exist_ok=True)
    with open(os.path.join(adir, "volume.css"), "w", encoding="utf-8") as f:
        f.write(CSS)


def write_retrieval_files():
    base = M["base"]
    urls = [base] + [base + c["slug"] + "/" for c in VOLUME]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc></url>")
    sm.append("</urlset>\n")
    with open(os.path.join(L.DOCS, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    robots = ("User-agent: *\nAllow: /\n\nSitemap: " + base + "sitemap.xml\n")
    with open(os.path.join(L.DOCS, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    lines = [f"# {M['title']}",
             "> A first-principles, fully-reproducible theory of how vision emerges: the high\u2192low "
             "down-conversion ladder E0\u2192E8. Theoretical research, non-clinical. " + M["license"] + ".",
             "", "## Chapters"]
    for c in VOLUME:
        lines.append(f"- [{c['num']} \u2014 {c['title']}]({M['base']}{c['slug']}/): {c['one_liner']}")
    lines += ["", "## Notes",
              "- Reproduction master is the HTML; every number is regenerated by the run.py modules "
              "(2\u00d7sha256, drift 0). \u03b3 is measured from NCBI promoters, never fitted.",
              "- The E4 congenital-blindness chapter is direction-only / proposal-only behind a "
              "machine-checked magnitude firewall (no dose, potency, efficacy, or clinical magnitude).",
              "- The felt percept of sight is deferred to the mind volume.", ""]
    with open(os.path.join(L.DOCS, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    # clean rebuild of docs/eye (idempotent, deterministic)
    import shutil
    if os.path.isdir(L.DOCS):
        shutil.rmtree(L.DOCS)
    os.makedirs(L.DOCS, exist_ok=True)

    print("=" * 78)
    print("BUILD VOLUME — docs/eye/  (generated FROM run.py outputs; numbers are code's own)")
    print("=" * 78)
    write_assets()
    page_shas = {}
    total_facts = 0
    for idx, ch in enumerate(VOLUME):
        nfacts, shas = render_page(ch, idx)
        total_facts += nfacts
        page_shas[ch["slug"]] = shas
        print(f"  [page] {ch['num']:3s} {ch['slug']:26s} facts={nfacts:2d}  "
              f"runs={len(shas)}  src-sha={','.join(s[:10] for s in shas)}")
    render_hub(page_shas)
    write_retrieval_files()
    print(f"\n  hub + {len(VOLUME)} chapters + facts + css + sitemap/robots/llms written.")
    print(f"  total surfaced facts (each verified \u2208 its live transcript): {total_facts}")
    print("=" * 78)
    print("BUILD VOLUME: DONE")
    print("=" * 78)


if __name__ == "__main__":
    main()
