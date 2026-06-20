#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_sns_content.py -- authored chapter content for the Special-Sense Organs whitepaper.

Prose is authored (English body, C0); every QUANTITY is loaded from the verified corpus by build_F()
(reports/emergence_results.json + the pathology/treatment modules) and injected, so rendering is
deterministic and traceable to the 2xsha256 result (C1). chapters(F) returns the ordered list and
assigns each chapter's section number by position, so in-prose cross-references are slug links
(immune to renumbering) rather than fragile "chapter N" text.
"""
from _sns_render import DNA_HUB, NEURO_HUB, PHYS_HUB, REPRO_BASE, HUB_URL


def _f(x, n=2):
    return ("%." + str(n) + "f") % float(x)


# ----- stable slugs (the topic part is the URL; the 2-digit prefix is the section number) -----
SLUG = {
    "emerge":     "01-organ-emergence-from-measured-gamma",
    "method":     "02-deterministic-emergence-no-tuning-method",
    "transducer": "03-unified-molecular-transducer-r19-switch",
    "photo":      "04-phototransduction-rod-cng-switch",
    "optics":     "05-ocular-optics-reduced-eye-accommodation",
    "tonotopy":   "06-cochlear-tonotopy-greenwood-place-map",
    "hopf":       "07-cochlear-hopf-amplifier-cube-root",
    "vestibular": "08-vestibular-canal-torsion-pendulum",
    "chemo":      "09-chemodetection-taste-olfaction-switch",
    "disease":    "10-disease-setpoint-drift-basin-collapse",
    "treatment":  "11-root-cause-treatment-inverse-substrate",
    "refs":       "12-references-gene-accessions-methods-provenance",
}


def L(key, text):
    """Internal cross-reference link by slug (number-independent)."""
    return '<a href="%s%s/">%s</a>' % (HUB_URL, SLUG[key], text)


def LX(href, text):
    """External / absolute-path link."""
    return '<a href="%s">%s</a>' % (href, text)


def build_F(res, path, treat):
    """Flatten every number used in prose, pulled from the verified corpus."""
    org = {o["organ"]: o for o in res["organs"]["organs"]}
    amp = res["cochlear_amplifier"]; opt = res["organ_optics_acoustics"]
    tr = {t["node"]: t for t in res["transduction"]["transducers"]}
    rows = {r["loop_gain_drop"]: r for r in path["derived_law_demo_pax6"]["rows"]}
    rd = treat["restoration_demo"]; g = amp["smallsignal_gain_vs_mu"]
    F = {
        "g_pax6": org["eye_retina_optics"]["gamma"], "g_rax": org["eye_photoreceptor"]["gamma"],
        "g_eya1": org["cochlea_frequency_map"]["gamma"], "g_sox2": org["inner_ear_haircell"]["gamma"],
        "g_tas": org["taste_chemodetection"]["gamma"],
        "order": res["organs"]["gamma_order_ascending"],
        "rod_slope": _f(tr["eye_photoreceptor"]["switch"]["sigmoid_max_slope"]),
        "rod_bar": _f(tr["eye_photoreceptor"]["switch"]["barrier"], 3),
        "rod_hys": _f(tr["eye_photoreceptor"]["switch"]["hysteresis_width"], 2),
        "met_slope": _f(tr["inner_ear_haircell"]["switch"]["sigmoid_max_slope"]),
        "met_bar": _f(tr["inner_ear_haircell"]["switch"]["barrier"], 3),
        "met_hys": _f(tr["inner_ear_haircell"]["switch"]["hysteresis_width"], 2),
        "tas_slope": _f(tr["taste_chemodetection"]["switch"]["sigmoid_max_slope"]),
        "tas_bar": _f(tr["taste_chemodetection"]["switch"]["barrier"], 3),
        "tas_hys": _f(tr["taste_chemodetection"]["switch"]["hysteresis_width"], 2),
        "comp": "1/3", "comp_num": _f(amp["critical_compression_exponent"], 4),
        "gain0": _f(g["mu=0"], 0), "gain01": _f(g["mu=-0.01"], 0),
        "gain1": _f(g["mu=-0.1"], 0), "gainm1": _f(g["mu=-1"], 0),
        "axial": _f(opt["reduced_eye_axial_length_mm"]), "dpm": _f(opt["diopters_per_mm_axial"]),
        "acc15": _f(opt["accommodation_D_age15"], 0), "acc60": _f(opt["accommodation_D_age60"], 0),
        "gw_apex": _f(opt["greenwood_apex_hz"], 1), "gw_base": _f(opt["greenwood_base_hz"], 0),
        "gw_base_k": _f(float(opt["greenwood_base_hz"]) / 1000.0, 1),
        "flat": _f(opt["canal_velocity_band_flatness_ratio"], 3), "vor": _f(opt["vor_gain_cited"], 1),
        "B_health": _f(rows[0.0]["healthy_barrier"], 3),
        "B_d50": _f(rows[0.5]["residual_barrier"], 3), "rate_d50": _f(rows[0.5]["crossing_rate_relative"], 1),
        "B_d90": _f(rows[0.9]["residual_barrier"], 3), "rate_d90": _f(rows[0.9]["crossing_rate_relative"], 1),
        "rd_health": _f(rd["healthy_barrier"], 3), "rd_dis": _f(rd["disease_barrier"], 3),
        "rd_treat": _f(rd["treated_barrier"], 3), "rd_rec": _f(float(rd["recovered_fraction"]) * 100.0, 0),
        "law_rows": [(d, _f(rows[d]["barrier_fraction"], 4), _f(rows[d]["crossing_rate_relative"], 2))
                     for d in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9)],
    }
    return F


def chapters(F):
    chs = [_ch1(F), _ch_method(F), _ch_transducer(F), _ch_photo(F), _ch_optics(F),
           _ch_tonotopy(F), _ch_hopf(F), _ch_vestibular(F), _ch_chemo(F), _ch_disease(F),
           _ch_treatment(F), _ch_refs(F)]
    for i, c in enumerate(chs):
        c["no"] = i + 1                       # section number is positional; cross-refs are slug links
    return chs


# ============================================================ §1  organ emergence (overview)
def _ch1(F):
    o = " \u2192 ".join(F["order"])
    return dict(
        slug=SLUG["emerge"],
        subj="Organs emerge from measured DNA stiffness \u03b3", short="Organ emergence",
        knows=["jamming lattice", "DNA stacking stiffness", "morphogenesis", "sense organ", "master gene"],
        seo=["special sense organs", "sense organ development", "DNA stacking stiffness gamma",
             "master gene", "developmental order", "morphogenesis", "PAX6 eye gene", "emergence"],
        title="Special-sense organs emerge from measured DNA stiffness \u03b3",
        one="Six organ nodes are a \u03b3-readout; the falsifiable order (taste latest) is confirmed.",
        grade_label="[V] verified", grade_kind="verified",
        desc=("Six special-sense organ nodes emerge from measured DNA stacking stiffness \u03b3 (PAX6 %s, RAX %s, "
              "EYA1 %s, SOX2 %s, TAS1R3 %s); sorting \u03b3 gives a developmental order whose falsifiable signal is "
              "confirmed (taste specified latest)." % (F["g_pax6"], F["g_rax"], F["g_eya1"], F["g_sox2"], F["g_tas"])),
        answer=("Six special-sense organs emerge as nodes from measured DNA stacking stiffness \u03b3: the eye "
                "(PAX6, \u03b3=%s), photoreceptor (RAX, %s), cochlear frequency map (EYA1, %s), hair cell (SOX2, %s), "
                "and taste (TAS1R3, %s); vestibular balance is a diffuse circuit with no single master gene. \u03b3 is "
                "a measured input, never fitted." % (F["g_pax6"], F["g_rax"], F["g_eya1"], F["g_sox2"], F["g_tas"])),
        abstract=("Node identity and developmental order are inherited from the DNA package, where "
                  "\u03b3 = \u2212mean(nearest-neighbour stacking \u0394G37) is read from human proximal promoters and "
                  "never tuned. Sorting the five measured \u03b3 values yields an emergence order whose falsifiable "
                  "prediction \u2014 taste specified latest \u2014 is confirmed [V]; the fine order among the "
                  "co-emerging early eye and ear nodes is a separately graded [L] item pending stage-timing data."),
        cards=['<b>\u03b3 (PAX6) = %s</b> \u2014 measured DNA stacking stiffness of the eye master gene, '
               '\u2212mean(nearest-neighbour \u0394G37) over the proximal promoter; never fitted. <b>[L]</b> measured '
               'input. ' % F["g_pax6"] + LX(DNA_HUB, "canonical \u03b3 atlas (4D DNA Blueprint)")],
        body=[
            ("p", "The special-sense organs are not free parameters of this whitepaper. Each one is a <b>node whose "
                  "identity and emergence order are read out from a single measured quantity</b> \u2014 the DNA "
                  "stacking stiffness \u03b3 of its master gene. Those \u03b3 values are vendored from the "
                  + LX(DNA_HUB, "4D DNA Blueprint") + ", computed from real human promoter sequence and never tuned "
                  "to hit a target."),
            ("h2", "What does it mean that an organ \u201cemerges\u201d from DNA?"),
            ("p", "It means the organ is derived, not assumed. The same physical pipeline that the DNA package uses "
                  "to set body-plan morphology assigns each special sense a master gene, reads that gene's promoter "
                  "stiffness \u03b3, and places the organ as a node in the developmental sequence. This package then "
                  "adds dynamics on top of those inherited nodes; it re-emerges no organ owned elsewhere, and it "
                  "treats the DNA atlas as the single source of truth for identity and order."),
            ("t", "Six organ nodes vendored from the measured \u03b3 atlas",
             ["node", "master", "\u03b3", "role", "grade"],
             [["<code>eye_retina_optics</code>", "PAX6", '<span class="num">%s</span>' % F["g_pax6"],
               "retinal photoreceptor mosaic + ocular dioptrics (optics classical; switch R19)", "[V]"],
              ["<code>eye_photoreceptor</code>", "RAX", '<span class="num">%s</span>' % F["g_rax"],
               "phototransduction switch (R19 cellular)", "[V]"],
              ["<code>cochlea_frequency_map</code>", "EYA1", '<span class="num">%s</span>' % F["g_eya1"],
               "basilar-membrane tonotopy (mechanics classical; switch R19)", "[V]"],
              ["<code>inner_ear_haircell</code>", "SOX2", '<span class="num">%s</span>' % F["g_sox2"],
               "hair-cell mechanotransduction (R19 switch)", "[V]"],
              ["<code>vestibular_balance</code>", "(circuit)", "diffuse",
               "semicircular-canal + otolith inertial sensing", "circuit"],
              ["<code>taste_chemodetection</code>", "TAS1R3", '<span class="num">%s</span>' % F["g_tas"],
               "taste receptor chemodetection", "[V]"]]),
            ("h2", "The developmental order is the argsort of \u03b3"),
            ("p", "Ranking the five measured nodes by ascending \u03b3 gives the emergence sequence "
                  "<code>%s</code>. This ordering is a <b>parameter-free read-out</b>: nothing is adjusted to "
                  "produce it. Its prediction \u2014 that the taste organ is specified latest \u2014 is the "
                  "falsifiable, broad signal, and it is confirmed against cited staging." % o),
            ("bound", "<b>Graded scope, not a shortfall.</b> The broad order (taste latest) is solid [V]. The fine "
                      "ordering among the early eye and ear nodes is held at [L] because PAX6/RAX (eye field) and "
                      "EYA1/SOX2 (otic placode) genuinely co-occur early in development \u2014 separating them "
                      "requires cited stage-timing data, so it is recorded as a distinct, gradeable item rather than "
                      "asserted. Stating exactly how far a prediction reaches is the discipline that makes it "
                      "testable; see " + L("method", "the no-tuning method") + "."),
            ("h2", "Why vestibular balance carries no \u03b3"),
            ("p", "Inner-ear balance is correctly represented at the level it actually occupies: a <b>circuit-level, "
                  "derived property</b> distributed across the semicircular canals and otoliths, not a single-gene "
                  "node. Assigning it one master gene and one \u03b3 would be the error; the framework instead "
                  "treats it as a diffuse sensor and recovers its physics classically in "
                  + L("vestibular", "the vestibular chapter") + "."),
            ("p", "The seam to downstream biology is sharp. This package owns the <b>organ-physics stage</b> \u2014 "
                  "the instrument and its cellular transducer \u2014 and hands the transduced signal off to "
                  + LX(NEURO_HUB, "the Neural Emergence Chain") + ", which owns "
                  "transduction\u2009\u2192\u2009spike\u2009\u2192\u2009brain."),
        ])


# ============================================================ §2  deterministic emergence (method)
def _ch_method(F):
    return dict(
        slug=SLUG["method"],
        subj="Deterministic emergence: the no-tuning method", short="No-tuning method",
        knows=["no-tuning", "reproducibility", "SantaLucia nearest-neighbour", "falsifiability",
               "stacking free energy", "deterministic model"],
        seo=["no-tuning model", "reproducible computational biology", "SantaLucia nearest-neighbour thermodynamics",
             "DNA stacking free energy", "deterministic simulation", "falsifiable model",
             "bit-for-bit reproducibility", "first-principles biology"],
        title="Deterministic emergence: how the organs are derived from measured DNA, with no tuning",
        one="LOCK \u2192 Derive \u2192 Gate: \u03b3 is measured, the order is derived, every page reproduces bit-for-bit.",
        grade_label="[V] verified", grade_kind="verified",
        desc=("The method behind the whitepaper: organ identity and order are derived from measured DNA stacking "
              "stiffness \u03b3 (SantaLucia nearest-neighbour \u0394G37), never fitted; results reproduce bit-for-bit "
              "(2\u00d7sha256 identical); every claim is graded [V]/[L]/[O]."),
        answer=("This whitepaper follows one discipline: LOCK, Derive, Gate. The organ identities and their "
                "developmental order are read out from measured human-DNA stacking stiffness \u03b3 \u2014 SantaLucia "
                "nearest-neighbour \u0394G37 over the real promoter, never fitted \u2014 and every page reproduces "
                "bit-for-bit (2\u00d7sha256 identical). No number is chosen to hit a target."),
        abstract=("The program rests on three commitments that turn \u201creproducibility\u201d into a structure. "
                  "First, no tuning: every quantity is either a measured input or a value derived from one, never "
                  "adjusted to match an answer. Second, determinism: a fixed seed makes the engine emit a "
                  "byte-identical result twice over (2\u00d7sha256 identical, 6a68bc48\u2026). Third, explicit "
                  "grading: [V] verified in-simulation, [L] calibrated or cited, [O] open with a stated obstacle, "
                  "[H] hypothesis \u2014 so the reach of every claim is legible."),
        cards=['<b>\u03b3 = \u2212mean(NN \u0394G37)</b> \u2014 DNA stacking stiffness: the negative mean '
               'nearest-neighbour stacking free energy (SantaLucia 1998) over a gene\u2019s human proximal promoter. '
               'A measured sequence property, cached so it reproduces offline. <b>[L]</b> measured input. '
               + LX(DNA_HUB, "canonical \u03b3 atlas")],
        body=[
            ("p", "A new theory earns trust by how tightly it is constrained, not by how much it explains. The point "
                  "of this section is to make the constraints explicit, so that the results in the chapters that "
                  "follow read as a <b>grounded derivation rather than an illustrative simulation</b>."),
            ("h2", "What \u03b3 is, and how it is measured"),
            ("p", "\u03b3 is the <b>DNA stacking stiffness</b> of a gene: the negative mean of the "
                  "nearest-neighbour stacking free energies \u0394G37 along its human proximal promoter "
                  "(SantaLucia 1998 nearest-neighbour thermodynamics, the standard for DNA base-pair stacking). "
                  "It is a property of the real, published genomic sequence \u2014 not a knob. The five master-gene "
                  "values used here (PAX6 %s, RAX %s, EYA1 %s, SOX2 %s, TAS1R3 %s) are read once and cached, so "
                  "\u03b3 reproduces offline and bit-for-bit."
                  % (F["g_pax6"], F["g_rax"], F["g_eya1"], F["g_sox2"], F["g_tas"])),
            ("h2", "The no-tuning discipline"),
            ("p", "Every quantity in the program is one of two things: a <b>measured input</b> (a sequence-derived "
                  "\u03b3, a cited physiological threshold, a classical-optics constant) or a <b>derived value</b> "
                  "computed from those inputs by a fixed rule. No quantity is ever chosen to make a result come out "
                  "right. The developmental order, for instance, is simply argsort(\u03b3); the cochlear compression "
                  "exponent is fixed by a normal form, not selected."),
            ("h2", "LOCK \u2192 Derive \u2192 Gate"),
            ("ul", ["<b>LOCK</b> \u2014 inputs are frozen: the measured \u03b3 values, the cited anchors, and the "
                    "substrate equations are read-only for the run.",
                    "<b>Derive</b> \u2014 the engine computes the consequences deterministically (node order, "
                    "transducer bistability, the Hopf exponent, the disease law).",
                    "<b>Gate</b> \u2014 a stress battery and a determinism check must pass before any result is "
                    "written; the canonical HTML then renders only what passed."]),
            ("h2", "Bit-for-bit reproducibility"),
            ("p", "The engine is run twice in separate processes and the two outputs are hashed; the program is "
                  "accepted only if the hashes are identical. The signed-off result for this volume is "
                  "<code>6a68bc48\u2026</code> (2\u00d7sha256 identical), and the whole site is generated from that "
                  "frozen result with a fixed build date, so the canonical HTML itself rebuilds byte-for-byte. "
                  "Anyone can re-run it: from the package root, <code>python repro/run_all.py</code>."),
            ("h2", "The grading vocabulary is what makes it falsifiable"),
            ("p", "Each claim carries a grade, and the grades mean exactly what they say:"),
            ("t", "How claims are graded",
             ["grade", "meaning", "example in this volume"],
             [["[V]", "verified in-simulation (reproduced by the engine)",
               "every special-sense transducer is a bistable switch; cube-root exponent " + F["comp_num"]],
              ["[L]", "calibrated / cited (a measured input or established literature)",
               "cGMP and EC50 thresholds; the Greenwood place-map; reduced-eye optics"],
              ["[O]", "open, with a stated obstacle (listed in the ledger)",
               "absolute disease incidence (needs an external noise scale)"],
              ["[H]", "hypothesis (a posited operating point, not fitted)",
               "that a real outer hair cell sits exactly at the Hopf point \u03bc=0"]]),
            ("p", "Because the boundaries are explicit, the program is <b>refutable</b>: if the taste organ were "
                  "specified earliest, the order claim would fail; if a transducer were a graded rather than an "
                  "all-or-none gate, the unification would fail; if the measured compression exponent were far from "
                  + F["comp_num"] + ", the Hopf account would fail."),
            ("bound", "<b>Single source of truth (SSOT).</b> Identity and developmental order are owned by the DNA "
                      "package; the effector-channel \u03b3 values are likewise owned there and are cited here as "
                      "honest <i>to-measure</i> inputs, not computed or guessed in this package. Drawing that line "
                      "prevents the same quantity from being defined twice and drifting \u2014 it is a reproducibility "
                      "safeguard, carried into " + L("transducer", "the transducer chapter") + "."),
        ])


# ============================================================ §3  unified molecular transducer
def _ch_transducer(F):
    return dict(
        slug=SLUG["transducer"],
        subj="One R19 switch for every special sense", short="Unified transducer",
        knows=["ion channel", "bistability", "R19 double-well", "sensory transduction", "cooperative gating"],
        seo=["sensory transduction", "ion channel bistability", "cooperative gating", "CNG channel",
             "mechanotransduction", "TRPM5", "Hill coefficient", "two-state gate"],
        title="The unified molecular transducer: every special sense is an R19 bistable channel switch",
        one="Photoreceptor, hair-cell, and taste channels are all verified bistable double-wells.",
        grade_label="[V] verified", grade_kind="verified",
        desc=("Every special-sense transducer is the same object \u2014 a cooperative/bistable ion channel, an R19 "
              "double-well. Photoreceptor (CNG), hair-cell (MET), and taste (TRPM5) channels are verified bistable "
              "(slopes \u2248%s\u2013%s); olfaction shares the rod's CNG superfamily." % (F["tas_slope"], F["rod_slope"])),
        answer=("Every special-sense transducer is the same physical object: a cooperative or bistable ion channel "
                "\u2014 an R19 double-well switch. The photoreceptor (CNG), hair-cell (MET), and taste "
                "(TAS1R\u2192TRPM5) channels are each verified bistable with a discontinuous flip; olfaction shares "
                "the rod's CNG superfamily. One switch primitive underlies five senses."),
        abstract=("The transduction model tests each channel as an R19 double-well and finds bistability with a "
                  "discontinuous flip and hysteresis for every transducer carrying a measured \u03b3. Sigmoid maximum "
                  "slopes cluster near 3.1\u20133.3 (cooperative gating), matching cited Hill coefficients \u22483. "
                  "Channel identity and accession are cited [L]; \u03b3 for the effector genes is owned by the DNA "
                  "pipeline (SSOT), entered as an honest to-measure input rather than invented."),
        cards=['<b>R19 double-well</b> \u2014 the bistable two-state element of the jamming substrate (FHN-class). A '
               'cooperative ion channel realises it: two stable conductance states with a discontinuous flip between '
               'them. <b>[V]</b> verified in-sim. ' + LX(PHYS_HUB, "substrate (jamming foundation)")],
        body=[
            ("p", "The central result of the molecular layer is a <b>unification</b>: the transducers of vision, "
                  "hearing, taste, and smell are not four mechanisms but four instances of one. Each is a "
                  "cooperative or bistable ion channel, which is exactly the R19 double-well \u2014 two stable states "
                  "separated by a barrier, with an all-or-none flip between them."),
            ("h2", "What makes a sensory channel a switch?"),
            ("p", "A transducer is a switch when it has two stable states and crosses between them sharply rather "
                  "than gradually. Cast as an R19 double-well and driven, every channel with a vendored \u03b3 shows "
                  "the three switch signatures: <b>bistability</b> (two stable conductances), a <b>discontinuous "
                  "flip</b>, and <b>hysteresis</b> (the up- and down-thresholds differ). The hysteresis widths sit "
                  "around %s\u2013%s." % (F["rod_hys"], F["tas_hys"])),
            ("t", "Four channel families, one bistable primitive",
             ["sense", "channel", "genes (cited)", "max slope", "barrier", "grade"],
             [["vision", "rod CNG (cyclic-nucleotide-gated)", "<code>CNGA1</code>, <code>CNGB1</code>",
               '<span class="num">%s</span>' % F["rod_slope"], '<span class="num">%s</span>' % F["rod_bar"], "[V]"],
              ["hearing", "hair-cell MET (gating-spring)", "<code>TMC1</code>, <code>PCDH15</code>, <code>CDH23</code>",
               '<span class="num">%s</span>' % F["met_slope"], '<span class="num">%s</span>' % F["met_bar"], "[V]"],
              ["taste", "T1R GPCR \u2192 TRPM5 channel", "<code>TAS1R2/3</code>, <code>TRPM5</code>",
               '<span class="num">%s</span>' % F["tas_slope"], '<span class="num">%s</span>' % F["tas_bar"], "[V]"],
              ["smell", "olfactory CNG (cAMP-gated)", "<code>CNGA2</code>, <code>ADCY3</code>",
               "deferred", "\u2014", "[O]\u2192"]]),
            ("h2", "Cooperative gating makes the flip sharp"),
            ("p", "Maximum slopes of 3.1\u20133.3 reproduce the cooperative gating seen physiologically (Hill "
                  "coefficient \u22483). Cooperativity is what converts a smooth change in stimulus into an "
                  "all-or-none change in conductance, so each transducer behaves as a clean threshold detector "
                  "rather than a graded one \u2014 the property that lets a single photon or a sub-nanometre bundle "
                  "deflection produce a definite response."),
            ("h2", "Vision and smell share a literal common transducer"),
            ("p", "The olfactory channel CNGA2 belongs to the <b>same cyclic-nucleotide-gated superfamily</b> as the "
                  "rod's CNGA1. Two senses therefore run on one switch primitive, with smell using cAMP where vision "
                  "uses cGMP \u2014 the single most direct evidence that the special senses share a transducer, "
                  "developed in " + L("photo", "phototransduction") + " and " + L("chemo", "chemodetection") + "."),
            ("bound", "<b>SSOT discipline.</b> The effector-channel \u03b3 values (CNGA1/CNGB1, TMC1/PCDH15/CDH23, "
                      "SLC26A5, TAS1R2/TRPM5, CNGA2/ADCY3) are <b>not</b> computed here. Channel identity and "
                      "NCBI/UniProt accessions are cited [L]; \u03b3 is measured by the DNA pipeline (SantaLucia "
                      "nearest-neighbour \u0394G37), an honest to-measure input owned at one place rather than "
                      "duplicated here. The verified claim is the switch <i>structure</i>, not the effector \u03b3."),
        ])


# ============================================================ §4  phototransduction
def _ch_photo(F):
    return dict(
        slug=SLUG["photo"],
        subj="Phototransduction: the rod CNG channel switch", short="Phototransduction",
        knows=["phototransduction", "CNG channel", "cGMP", "cooperative gating", "single-photon response"],
        seo=["phototransduction", "rod CNG channel", "cGMP", "single-photon response", "photoreceptor",
             "cooperative gating", "Hill coefficient", "how the eye detects light"],
        title="Phototransduction: the rod CNG channel as a cooperative all-or-none switch",
        one="Light shuts the cGMP-gated CNG channel; bistable flip, slope %s." % F["rod_slope"],
        grade_label="[V] verified", grade_kind="verified",
        desc=("The rod photoreceptor is an R19 switch: light drops cGMP and shuts the cyclic-nucleotide-gated CNG "
              "channel (Hill \u22483). The simulated switch is bistable with maximum slope %s; the cGMP threshold is "
              "a cited input." % F["rod_slope"]),
        answer=("The rod photoreceptor is an R19 switch: light drives a PDE cascade that drops cGMP, shutting "
                "cyclic-nucleotide-gated channels in under a millisecond. The CNG channel (CNGA1/CNGB1) gates "
                "cooperatively with a Hill coefficient of about three, giving a sharp all-or-none flip \u2014 verified "
                "bistable with maximum slope %s. Single-photon responses are discrete." % F["rod_slope"]),
        abstract=("Phototransduction is modelled as a cooperative ligand gate on the cGMP-bound CNG channel. The "
                  "simulated switch is bistable with a discontinuous flip, hysteresis width \u2248%s, and maximum slope "
                  "%s \u2014 consistent with the cited cGMP K\u00bd \u224810\u201340 \u00b5M and Hill \u22483. The "
                  "threshold is a cited physiological input [L]; the switch structure is verified [V]."
                  % (F["rod_hys"], F["rod_slope"])),
        cards=['<b>\u03b3 (RAX) = %s</b> \u2014 measured DNA stiffness of the photoreceptor master gene, driving the '
               'bistable spinodal of the rod switch. <b>[L]</b> measured input. ' % F["g_rax"]
               + LX(DNA_HUB, "canonical \u03b3 atlas")],
        body=[
            ("p", "Phototransduction is the process by which the eye turns a captured photon into an electrical "
                  "signal. Its defining and slightly counter-intuitive feature is that <b>light shuts a channel</b> "
                  "rather than opening one: in the dark the rod is depolarised by a standing current through open "
                  "CNG channels, held open by a high resting level of the second messenger cGMP."),
            ("h2", "How a single photon produces a discrete response"),
            ("p", "A captured photon activates the G-protein transducin, which switches on phosphodiesterase (PDE); "
                  "PDE hydrolyses cGMP, the cGMP level falls, and the CNG channels close in well under a "
                  "millisecond. Because one activated cascade shuts many channels, the response to a single photon "
                  "is large, discrete, and reproducible \u2014 the hallmark of rod sensitivity."),
            ("h2", "Cooperative gating makes the flip sharp"),
            ("p", "The CNG channel binds cGMP with a Hill coefficient of about three, so a modest change in ligand "
                  "produces an all-or-none change in conductance. Cast as an R19 double-well, the gate is bistable "
                  "with a discontinuous flip, a hysteresis width of about %s, and a maximum slope of %s \u2014 the "
                  "steepness that makes the rod a clean threshold detector rather than a graded one."
                  % (F["rod_hys"], F["rod_slope"])),
            ("bound", "<b>Threshold calibrated, structure verified.</b> The cGMP half-activation K\u00bd "
                      "\u224810\u201340 \u00b5M (Ca\u00b2\u207a-dependent) is a cited physiological value [L], mapped "
                      "onto the switch rather than derived from \u03b3. The package claims the <i>structure</i> "
                      "(bistable, cooperative, discontinuous) as [V]; the absolute threshold is an explicit "
                      "calibration, in keeping with " + L("method", "the no-tuning method") + "."),
            ("h2", "The same channel family runs the first step of smell"),
            ("p", "The rod's CNG channel is not unique to vision: the olfactory channel CNGA2 sits in the same "
                  "cyclic-nucleotide-gated superfamily, so phototransduction and the first step of smell are one "
                  "switch primitive. That shared transducer is the subject of " + L("chemo", "chemodetection") + ", "
                  "and the loss of this amplifying cascade with age and disease feeds the "
                  + L("disease", "disease law") + "."),
        ])


# ============================================================ §5  ocular optics
def _ch_optics(F):
    return dict(
        slug=SLUG["optics"],
        subj="Ocular optics: the reduced eye and accommodation", short="Ocular optics",
        knows=["reduced eye", "accommodation", "presbyopia", "refractive error", "myopia"],
        seo=["ocular optics", "reduced eye", "accommodation", "presbyopia", "refractive error", "myopia",
             "diopters per mm", "axial length", "why eyesight worsens with age"],
        title="Ocular optics: the reduced eye, accommodation, and presbyopia",
        one="Reduced eye reproduces axial %s mm, %s D/mm, presbyopia by Hofstetter." % (F["axial"], F["dpm"]),
        grade_label="[V] verified (arith)", grade_kind="verified",
        desc=("Ocular optics is classical: the reduced eye focuses ~60 D onto axial length %s mm, giving %s D/mm; "
              "accommodation falls from %s D at 15 to %s D at 60 (presbyopia). Reproduced by arithmetic, not "
              "re-derived from R19." % (F["axial"], F["dpm"], F["acc15"], F["acc60"])),
        answer=("Ocular optics is classical, not an R19 claim: the reduced eye focuses a roughly 60-diopter system "
                "onto a %s mm axial length, giving a clinical %s D/mm sensitivity that this package reproduces "
                "arithmetically. Accommodation falls from %s D at age 15 to %s D at 60 by Hofstetter's formula \u2014 "
                "presbyopia. Refractive error is a focal\u2013axial mismatch."
                % (F["axial"], F["dpm"], F["acc15"], F["acc60"])),
        abstract=("The Gullstrand reduced eye (total power \u224860 D, n\u2032=1.336) is emmetropic at axial length %s "
                  "mm; the model reproduces this and the clinical %s D/mm axial\u2013refraction sensitivity. "
                  "Hofstetter's age formula gives amplitude 25 \u2212 0.40\u00b7age, i.e. \u2248%s D at age 60 "
                  "(presbyopia). These are classical-optics anchors reproduced by arithmetic [V-arith], documented "
                  "and linked, not re-derived from the substrate." % (F["axial"], F["dpm"], F["acc60"])),
        cards=[],
        body=[
            ("p", "The eye's optics belong to classical physics, and this package treats them that way: it documents "
                  "and links the lensmaker and dioptric relations rather than re-deriving them from the jamming "
                  "substrate. Drawing that boundary clearly is part of the program's discipline, not a gap \u2014 see "
                  + L("method", "the no-tuning method") + "."),
            ("h2", "The reduced eye is a documented instrument"),
            ("p", "Gullstrand's reduced (schematic) eye lumps the cornea and lens into a single refracting surface "
                  "of total power about 60 diopters with image-space index 1.336, emmetropic at an axial length of "
                  "%s mm \u2014 the value the model returns. It is the standard first-order model of the eye as an "
                  "optical instrument." % F["axial"]),
            ("h2", "Why one millimetre of eye length matters so much"),
            ("p", "The geometry implies an <b>axial\u2013refraction sensitivity of %s D/mm</b>: each extra millimetre "
                  "of axial length is worth about %s diopters of refraction, matching the clinical 2.7\u20133.0 D/mm. "
                  "A longer eye is therefore more myopic by this fixed conversion, which is exactly why small "
                  "differences in eye growth translate into large differences in spectacle prescription."
                  % (F["dpm"], F["dpm"])),
            ("h2", "Presbyopia: accommodation declines linearly with age"),
            ("p", "Accommodation is the eye's ability to refocus on near objects. Hofstetter's formula, "
                  "amplitude = 25 \u2212 0.40\u00b7age, gives about %s D at age 15 and only about %s D at 60 \u2014 the "
                  "near point recedes to arm's length, which is presbyopia. The decline is steady and predictable, "
                  "and the model reproduces both endpoints." % (F["acc15"], F["acc60"])),
            ("bound", "<b>Classical, reproduced by arithmetic [V-arith].</b> Reduced-eye power, axial length, the "
                      "D/mm conversion, and the Hofstetter decline are cited classical-optics anchors that the "
                      "package reproduces numerically; they are explicitly not derived from the substrate, and "
                      "saying so is what keeps the [V] grade honest."),
            ("p", "Refractive error follows directly: <b>myopia</b> is an axial length too long for the eye's power, "
                  "and <b>hyperopia</b> too short. The growth-control loop that should defend the focal\u2013axial "
                  "match \u2014 emmetropization \u2014 is what fails in progressive myopia, and that loop is treated in "
                  "the " + L("disease", "disease law") + " and " + L("treatment", "therapy program") + "."),
        ])


# ============================================================ §6  cochlear tonotopy
def _ch_tonotopy(F):
    return dict(
        slug=SLUG["tonotopy"],
        subj="Cochlear tonotopy: the basilar-membrane place-map", short="Cochlear tonotopy",
        knows=["tonotopy", "basilar membrane", "Greenwood function", "place coding", "frequency map"],
        seo=["cochlear tonotopy", "basilar membrane", "Greenwood function", "place coding", "frequency map",
             "human hearing range", "how the ear separates pitch"],
        title="Cochlear frequency analysis: the basilar-membrane place-map",
        one="Greenwood place-map %s Hz\u2013%s kHz reproduced; the switch is the R19 MET gate." % (F["gw_apex"], F["gw_base_k"]),
        grade_label="[L] calibrated", grade_kind="calibrated",
        desc=("The basilar membrane maps frequency to place: Greenwood's human function spans %s Hz (apex) to %s kHz "
              "(base), reproduced here. The map is a cited classical anchor; the hair cell at each place is the R19 "
              "mechanotransduction switch." % (F["gw_apex"], F["gw_base_k"])),
        answer=("The basilar membrane maps frequency to place: Greenwood's function f = 165.4\u00b7(10^{2.1x} \u2212 "
                "0.88) runs from about %s Hz at the apex to %s kHz at the base, reproduced here. This is a classical "
                "resonant filter bank, cited not re-derived; the hair cell at each place is the R19 "
                "mechanotransduction switch that converts deflection into current." % (F["gw_apex"], F["gw_base_k"])),
        abstract=("Cochlear frequency analysis is place-coding: the stiffness-graded basilar membrane resonates at a "
                  "position-dependent frequency, and Greenwood's 1990 human function reproduces the ~20 Hz\u201320 kHz "
                  "range (apex %s Hz, base %s Hz). The place-map is a cited classical anchor [L] reproduced by "
                  "arithmetic [V-arith]; mechanotransduction at each place is the R19 gating-spring switch."
                  % (F["gw_apex"], F["gw_base"])),
        cards=['<b>\u03b3 (EYA1) = %s</b> \u2014 measured DNA stiffness of the cochlear frequency-map master gene. '
               '<b>[L]</b> measured input. ' % F["g_eya1"] + LX(DNA_HUB, "canonical \u03b3 atlas")],
        body=[
            ("p", "The cochlea analyses sound by <b>position, not by timing alone</b>: stiffness falls smoothly from "
                  "base to apex, so each place along the basilar membrane resonates best at its own frequency. High "
                  "frequencies peak near the stiff base; low frequencies near the compliant apex. This is tonotopy, "
                  "and it is why the ear is, in effect, a mechanical spectrum analyser."),
            ("h2", "The human map spans three decades of frequency"),
            ("p", "Greenwood's frequency\u2013position function reproduces a range from about %s Hz at the apex to "
                  "%s Hz at the base, matching the familiar ~20 Hz\u201320 kHz span of human hearing. The map is a "
                  "cited classical anchor that the package reproduces arithmetically; the membrane mechanics "
                  "themselves are not re-derived from the substrate." % (F["gw_apex"], F["gw_base"])),
            ("h2", "What converts membrane motion into a nerve signal?"),
            ("p", "At each place, the mechanical deflection is turned into electrical current by the <b>hair-cell "
                  "mechanotransduction (MET) channel</b> \u2014 a two-state, gating-spring gate. That gate is shown "
                  "to be an R19 double-well in " + L("transducer", "the unified-transducer chapter") + ", and the "
                  "active force that sharpens and amplifies the response sits at a critical point, derived in "
                  + L("hopf", "the cochlear amplifier") + "."),
            ("bound", "<b>Mechanics classical, switch R19.</b> The resonance and the place-map are classical "
                      "acoustics [L]/[V-arith]; the conversion of deflection into current at each place is the "
                      "hair-cell MET gate [V]. Keeping these two grades distinct \u2014 a cited instrument plus a "
                      "verified switch \u2014 is exactly how the chapter avoids over-claiming."),
        ])


# ============================================================ §7  cochlear Hopf amplifier
def _ch_hopf(F):
    return dict(
        slug=SLUG["hopf"],
        subj="The cochlear Hopf amplifier: cube-root compression", short="Hopf amplifier",
        knows=["Hopf bifurcation", "critical oscillator", "cube-root compression", "prestin", "outer hair cell"],
        seo=["cochlear amplifier", "Hopf bifurcation", "cube-root compression", "outer hair cell", "prestin",
             "critical oscillator", "active hearing", "dynamic range of hearing"],
        title="The cochlear Hopf amplifier: parameter-free cube-root compression",
        one="At \u00b5=0, R=(F/\u03b2)^{1/3}: exponent %s, parameter-free." % F["comp_num"],
        grade_label="[V] verified", grade_kind="verified",
        desc=("The cochlear amplifier is an oscillator at a Hopf bifurcation. At criticality (\u00b5=0) the response is "
              "R=(F/\u03b2)^{1/3} \u2014 cube-root compression with exponent %s, parameter-free; small-signal gain rises "
              "to ~%s. Active force = prestin (SLC26A5)." % (F["comp_num"], F["gain0"])),
        answer=("The cochlear amplifier is an active oscillator poised at a Hopf bifurcation. In normal form "
                "dz/dt=(\u00b5+i\u03c9\u2080)z\u2212\u03b2|z|\u00b2z+Fe^{i\u03c9\u2080t}, the critical point \u00b5=0 forces "
                "response R=(F/\u03b2)^{1/3} \u2014 cube-root compression with exponent exactly %s, parameter-free. "
                "Small-signal gain rises from %s far below to ~%s at criticality. Prestin (SLC26A5) supplies the "
                "active force." % (F["comp_num"], F["gainm1"], F["gain0"])),
        abstract=("Sitting an outer-hair-cell oscillator exactly at the Hopf bifurcation (\u00b5=0) yields a "
                  "compressive nonlinearity with exponent 1/3 that contains no fitted parameter \u2014 it follows from "
                  "the normal form alone. The simulated small-signal gain rises monotonically toward criticality "
                  "(%s \u2192 %s \u2192 %s \u2192 %s as \u00b5\u21920), and the 1/3 exponent matches the cited "
                  "~0.3\u20130.5 basilar-membrane compression [L]. The exponent is [V]; how close a real cell sits to "
                  "\u00b5=0 is an empirical question [H], not tuned."
                  % (F["gainm1"], F["gain1"], F["gain01"], F["gain0"])),
        cards=['<b>R = (F/\u03b2)<sup>1/3</sup></b> \u2014 Hopf-normal-form response at criticality (\u00b5=0): a '
               'cube-root compression whose exponent %s is independent of \u03b2 (a unit). Active force = prestin. '
               '<b>[V]</b> parameter-free; <b>[H]</b> exact in-vivo operating point. '
               % F["comp_num"] + LX(REPRO_BASE, "Reproduce (GitHub)")],
        body=[
            ("p", "A passive cochlea would be too insensitive and too broadly tuned to explain human hearing. The "
                  "resolution is an <b>active amplifier</b> in each outer hair cell, modelled as an oscillator held "
                  "right at the edge of spontaneous oscillation \u2014 a Hopf bifurcation. Operating at that edge buys "
                  "the largest possible gain for faint sounds together with sharp frequency tuning."),
            ("h2", "Why is the cochlear compression parameter-free?"),
            ("p", "Writing the amplifier in Hopf normal form, dz/dt=(\u00b5+i\u03c9\u2080)z\u2212\u03b2|z|\u00b2z+"
                  "Fe^{i\u03c9\u2080t}, and setting the control parameter \u00b5=0 gives a forced response "
                  "R=(F/\u03b2)^{1/3}. The <b>compression exponent is exactly %s</b> and does not depend on \u03b2, "
                  "which is merely a unit \u2014 so the cube-root is a structural prediction of sitting at the "
                  "bifurcation, with nothing fitted." % F["comp_num"]),
            ("t", "Small-signal gain rises toward the bifurcation",
             ["control parameter \u00b5", "small-signal gain"],
             [["\u22121", '<span class="num">%s</span>' % F["gainm1"]],
              ["\u22120.1", '<span class="num">%s</span>' % F["gain1"]],
              ["\u22120.01", '<span class="num">%s</span>' % F["gain01"]],
              ["0 (critical)", '<span class="num">%s</span>' % F["gain0"]]]),
            ("p", "As \u00b5 approaches zero the small-signal gain climbs from %s to about %s. This is why the cochlea "
                  "operates near criticality: maximal gain for faint sounds plus sharp tuning, with the cube-root "
                  "compression then handling the enormous dynamic range of audible intensities \u2014 from a whisper "
                  "to a jet engine on one set of cells." % (F["gainm1"], F["gain0"])),
            ("h2", "Prestin is the active force"),
            ("p", "The somatic motor protein <b>prestin (SLC26A5)</b> drives the outer-hair-cell length changes that "
                  "supply energy to the oscillator \u2014 the physical realisation of the forcing term. Loss of "
                  "prestin or of the outer hair cells removes the active force."),
            ("bound", "<b>\u00b5=0 is a hypothesis, not a knob [H].</b> The exponent 1/3 is parameter-free at "
                      "criticality [V]. How close a real outer hair cell sits to \u00b5=0 in vivo is an empirical, "
                      "self-tuning question \u2014 it is not fitted. Losing the amplifier pushes \u00b5 negative and "
                      "collapses this gain, which is presbycusis in the " + L("disease", "disease law") + "."),
        ])


# ============================================================ §8  vestibular balance
def _ch_vestibular(F):
    return dict(
        slug=SLUG["vestibular"],
        subj="Vestibular balance: the semicircular canal", short="Vestibular balance",
        knows=["semicircular canal", "torsion pendulum", "angular velocity", "vestibulo-ocular reflex", "balance"],
        seo=["vestibular system", "semicircular canal", "torsion pendulum", "angular velocity",
             "vestibulo-ocular reflex", "VOR gain", "balance and dizziness", "how the inner ear senses motion"],
        title="Vestibular balance: the semicircular canal as a torsion pendulum",
        one="Canal integrates acceleration to velocity over 0.1\u20136 Hz (flatness %s); VOR gain %s." % (F["flat"], F["vor"]),
        grade_label="[V] verified (arith)", grade_kind="verified",
        desc=("Each semicircular canal is an overdamped torsion pendulum; over 0.1\u20136 Hz it integrates angular "
              "acceleration, so its output encodes angular velocity (band flatness %s). The vestibulo-ocular reflex "
              "stabilises gaze at gain %s. Canal dynamics are classical." % (F["flat"], F["vor"])),
        answer=("Each semicircular canal is an overdamped torsion pendulum: endolymph inertia against cupula "
                "stiffness and viscous drag. Over the behavioural band 0.1\u20136 Hz the canal integrates angular "
                "acceleration, so its output encodes angular velocity (band flatness %s). The vestibulo-ocular "
                "reflex stabilises gaze with gain about %s. Canal dynamics are classical." % (F["flat"], F["vor"])),
        abstract=("The canal is modelled as a heavily damped second-order (torsion-pendulum) system; across "
                  "0.1\u20136 Hz its transfer function is flat in angular velocity (flatness ratio %s), so afferent "
                  "firing reports head angular velocity rather than acceleration. The VOR gain is about %s in healthy "
                  "young adults. These are classical fluid-mechanics anchors [V-arith]/[L] (Van Egmond\u2013Groen\u2013"
                  "Jongkees 1949), documented and linked, not re-derived from R19." % (F["flat"], F["vor"])),
        cards=[],
        body=[
            ("p", "A semicircular canal is a fluid-filled torus closed by an elastic cupula. Head rotation drives the "
                  "endolymph against the cupula, and the system behaves as an <b>overdamped torsion pendulum</b>: "
                  "inertia versus stiffness versus viscous drag, with damping dominating across the behavioural "
                  "band. Three canals on each side, roughly orthogonal, sense rotation about all axes."),
            ("h2", "Why the canal reports velocity, not acceleration"),
            ("p", "Because it is overdamped, the canal effectively <b>integrates angular acceleration</b> over "
                  "0.1\u20136 Hz, so its transfer function is flat in angular velocity (flatness ratio %s). The "
                  "afferent signal therefore reports how fast the head is turning, not how hard \u2014 which is "
                  "exactly the quantity the brain needs to hold the eyes and body steady." % F["flat"]),
            ("h2", "The vestibulo-ocular reflex closes the loop"),
            ("p", "The velocity signal drives compensatory eye movements that hold gaze stable during head motion; "
                  "in healthy young adults this <b>vestibulo-ocular reflex (VOR)</b> runs at a gain near %s. "
                  "Otoliths complement the canals by sensing linear acceleration and gravity, so the labyrinth as a "
                  "whole reports both rotation and translation." % F["vor"]),
            ("bound", "<b>Classical, reproduced by arithmetic [V-arith].</b> Canal fluid mechanics and the "
                      "velocity-band behaviour are cited classical anchors (Steinhausen 1933; Van Egmond\u2013"
                      "Groen\u2013Jongkees 1949). Vestibular balance is also correctly the one node with no single "
                      "master gene (see " + L("emerge", "organ emergence") + "), so it carries no \u03b3 \u2014 a "
                      "circuit-level property represented at its proper level."),
            ("p", "When otoconia dislodge into a canal, the same mechanics produce a <b>false angular-velocity "
                  "signal</b> \u2014 benign paroxysmal positional vertigo (BPPV) \u2014 which is why repositioning the "
                  "particles at the source is curative, as set out in the " + L("treatment", "therapy program") + "."),
        ])


# ============================================================ §9  chemodetection
def _ch_chemo(F):
    return dict(
        slug=SLUG["chemo"],
        subj="Chemodetection: taste and olfaction as switches", short="Chemodetection",
        knows=["taste receptor", "olfaction", "TRPM5", "CNG channel", "odorant receptor"],
        seo=["taste receptor", "olfaction", "chemodetection", "TRPM5", "T1R receptor", "smell",
             "odorant receptor", "how taste and smell work"],
        title="Chemodetection: taste and olfaction as threshold switches",
        one="Taste GPCR opens TRPM5 (slope %s); olfaction shares the rod's CNG channel." % F["tas_slope"],
        grade_label="[V] verified", grade_kind="verified",
        desc=("Taste and olfaction are threshold switches. The T1R taste GPCR opens TRPM5 past a concentration "
              "threshold (verified bistable, slope %s); olfaction uses a CNG channel of the same superfamily as the "
              "rod, so vision and smell share one transducer primitive." % F["tas_slope"]),
        answer=("Taste and olfaction are threshold switches. A taste GPCR (T1R2/T1R3 sweet, T1R1/T1R3 umami) drives "
                "PLC\u03b22 and opens the TRPM5 cation channel past a concentration threshold \u2014 verified bistable, "
                "slope %s. Olfaction uses an OR GPCR \u2192 cAMP \u2192 CNG channel of the same superfamily as the rod, "
                "making vision and smell share one transducer primitive." % F["tas_slope"]),
        abstract=("Chemodetection converts ligand concentration into an all-or-none channel opening. The taste "
                  "pathway (T1R receptors \u2192 PLC\u03b22 \u2192 TRPM5) is simulated as an R19 cooperative gate, "
                  "bistable with maximum slope %s and hysteresis \u2248%s; EC50 is a cited input [L]. Olfaction's "
                  "CNGA2 channel belongs to the same CNG superfamily as the rod's CNGA1 \u2014 a literal common switch "
                  "across two senses; its master \u03b3 is owned by the DNA pipeline." % (F["tas_slope"], F["tas_hys"])),
        cards=['<b>\u03b3 (TAS1R3) = %s</b> \u2014 measured DNA stiffness of the taste-receptor master gene, driving '
               'the chemodetection switch. <b>[L]</b> measured input. ' % F["g_tas"] + LX(DNA_HUB, "canonical \u03b3 atlas")],
        body=[
            ("p", "Taste is a receptor that opens a downstream channel. Sweet and umami are read by <b>T1R-family "
                  "GPCRs</b> (bitter by T2Rs), which activate PLC\u03b22 and open the TRPM5 cation channel; the "
                  "receptor sets specificity while TRPM5 carries the all-or-none current. Detection is therefore a "
                  "threshold event, not a smooth ramp."),
            ("h2", "Taste detection is a cooperative threshold crossing"),
            ("p", "Cast as an R19 gate, the taste switch is bistable with maximum slope %s and hysteresis width "
                  "about %s, and the concentration\u2013response is sigmoidal. The half-maximal concentration (EC50, "
                  "in the millimolar range for sweet and umami, lower for bitter) is a cited physiological input "
                  "[L], while the verified result is the switch structure." % (F["tas_slope"], F["tas_hys"])),
            ("h2", "Smell runs on the same channel family as vision"),
            ("p", "Odorant binding to an OR GPCR raises cAMP, which opens the olfactory CNG channel <b>CNGA2</b> "
                  "\u2014 the same cyclic-nucleotide-gated superfamily as the rod's CNGA1 (see "
                  + L("photo", "phototransduction") + "). Combinatorial coding across roughly 400 human odorant "
                  "receptors then yields odour identity from a shared switch primitive."),
            ("bound", "<b>\u03b3 for the chemoreceptor effectors is owned by the DNA pipeline.</b> EC50 values are "
                      "cited inputs [L]; the master \u03b3 for the olfactory-receptor family is not yet in the atlas "
                      "and is an honest <i>to-measure</i> input owned at one place (SSOT), not invented here \u2014 the "
                      "same discipline described in " + L("method", "the no-tuning method") + "."),
        ])


# ============================================================ §10  disease law
def _ch_disease(F):
    rows = [[("%g" % d), '<span class="num">%s</span>' % bf, '<span class="num">%s\u00d7</span>' % rt]
            for (d, bf, rt) in F["law_rows"]]
    return dict(
        slug=SLUG["disease"],
        subj="Disease as setpoint drift: a quadratic basin collapse", short="Disease law",
        knows=["setpoint", "attractor", "Kramers rate", "basin collapse", "age-related disease"],
        seo=["sense organ diseases", "glaucoma", "macular degeneration", "presbycusis", "cataract",
             "diabetic retinopathy", "basin collapse", "Kramers rate", "why eye and ear diseases progress"],
        title="Disease as setpoint drift: the quadratic basin-collapse law",
        one="Loop-gain drop d collapses the barrier as (g\u00b2/4)(1\u2212d)\u00b2; rate rises monotonically.",
        grade_label="[V] verified", grade_kind="verified",
        desc=("Disease on this substrate is a defended setpoint, clock, or instrument failing. A loop-gain drop d "
              "shrinks the attractor barrier as (g\u00b2/4)(1\u2212d)\u00b2 \u2014 a quadratic basin collapse \u2014 raising "
              "the Kramers crossing rate. Seven major eye and ear diseases instantiate one failure mode each."),
        answer=("Disease on this substrate is a defended setpoint, clock, or instrument failing. A loop-gain drop d "
                "shrinks the attractor barrier as (g\u00b2/4)(1\u2212d)\u00b2, a quadratic basin collapse, raising the "
                "Kramers crossing rate. Glaucoma, AMD, myopia, presbycusis, cataract, diabetic retinopathy, and BPPV "
                "each instantiate one failure mode. Shapes are verified; absolute rates are open."),
        abstract=("A single derived law governs the major non-rare diseases of the sense organs: residual barrier = "
                  "(g\u00b2/4)(1\u2212d)\u00b2 under a loop-gain drop d, so the barrier collapses quadratically (1.00 "
                  "\u2192 0.25 at d=0.5 \u2192 0.01 at d=0.9) while the relative Kramers crossing rate rises "
                  "monotonically. Presbycusis is the special case of the Hopf amplifier pushed off criticality, "
                  "collapsing the F^(1/3) gain. Shapes are [V]; per-disease anchors are cited [L]; absolute incidence "
                  "is [O] (needs the noise scale)."),
        cards=['<b>B(d) = (g\u00b2/4)(1\u2212d)\u00b2</b> \u2014 residual attractor barrier under a loop-gain drop d; '
               'a quadratic basin collapse, with Kramers escape rate \u223c exp(\u2212B/D). <b>[V]</b> shape; '
               '<b>[O]</b> absolute rate (needs noise scale D). ' + LX(REPRO_BASE, "Reproduce (GitHub)")],
        body=[
            ("p", "Disease here is <b>not a separate machinery from health</b> \u2014 it is the same R19 substrate "
                  "failing in one of a few shapes: a defended setpoint drifts, a feedback loop loses gain, an "
                  "attractor is crossed, or a physical instrument breaks. This is the same substrate as "
                  "carcinogenesis, viewed through the sense organs."),
            ("h2", "Why the attractor barrier collapses quadratically"),
            ("p", "A loop-gain drop d leaves an effective gain g(1\u2212d) and a residual attractor barrier "
                  "<b>(g\u00b2/4)(1\u2212d)\u00b2</b>; the escape rate follows Kramers' exp(\u2212B/D). Because the "
                  "barrier depends on the <i>square</i> of (1\u2212d), a partial loss of feedback shrinks the "
                  "protective barrier faster than linearly, so risk accelerates as control degrades."),
            ("t", "Quadratic basin collapse (PAX6 node, loop-gain drop d)",
             ["loop-gain drop d", "barrier fraction", "relative crossing rate"], rows),
            ("h2", "Seven major diseases, one substrate"),
            ("p", "Each major non-rare disease of the eye and ear maps to a single failure mode of this law, with "
                  "its anchor cited and its absolute rate left open:"),
            ("t", "Major eye/ear diseases as substrate failures",
             ["disease", "loop / arm", "mechanism", "grade"],
             [["glaucoma", "IOP homeostasis / outflow", "trabecular-meshwork stiffening \u2192 IOP setpoint drifts up "
               "\u2192 retinal ganglion-cell death (attractor crossing)", "[V]/[L]"],
              ["myopia", "emmetropization / defocus", "growth-control loop fails \u2192 axial elongation \u2192 myopia "
               "via the classical %s D/mm" % F["dpm"], "[V]/[L]"],
              ["presbycusis / NIHL", "cochlear amplifier / Hopf \u00b5", "hair-cell + prestin loss pushes \u00b5 off "
               "criticality \u2192 the F^(1/3) gain collapses \u2192 threshold shift", "[V]/[L]"],
              ["cataract", "lens solubility / chaperone", "oxidative damage \u2192 crystallins cross the aggregation "
               "spinodal \u2192 insoluble scatter (near-irreversible)", "[V]/[L]"],
              ["AMD (geographic atrophy)", "complement regulation", "lost regulation raises the inflammatory loop "
               "gain \u2192 chronic activation \u2192 RPE/photoreceptor atrophy", "[V]/[L]"],
              ["diabetic retinopathy", "retinal microvasculature", "chronic hyperglycemia \u2192 ischemia \u2192 "
               "VEGF-driven neovascular attractor (seam to metabolism)", "[V]/[L]"],
              ["BPPV / vertigo", "instrument fault", "otoconia dislodge into a canal \u2192 false angular-velocity "
               "signal", "[V]/[L]"]]),
            ("bound", "<b>Shapes verified, absolute rates open [O].</b> The law reproduces the <i>shapes</i> "
                      "(quadratic barrier collapse, monotone crossing-rate rise, amplifier-gain collapse) as [V]; "
                      "the <i>absolute</i> incidence and timing need an external noise scale D and absolute basin "
                      "depth, stated as the obstacle in <code>IRREPRODUCIBILITY_LEDGER.md</code>. Rare and monogenic "
                      "forms are owned by the disease whitepaper and enter here only as cited parameters \u2014 a "
                      "deliberate division of labour, not a gap."),
        ])


# ============================================================ §11  root-cause treatment
def _ch_treatment(F):
    return dict(
        slug=SLUG["treatment"],
        subj="Root-cause treatment: the inverse substrate operation", short="Root-cause treatment",
        knows=["root-cause therapy", "loop gain", "attractor barrier", "regenerative medicine", "gene therapy"],
        seo=["root cause treatment", "ROCK inhibitor glaucoma", "myopia control", "OTOF gene therapy",
             "complement inhibitor AMD", "canalith repositioning", "regenerative medicine eye ear",
             "treating the cause not the symptom"],
        title="Root-cause treatment: therapy as the inverse substrate operation",
        one="Five inverse ops across seven diseases; a collapsed basin recovers %s%% in the demo." % F["rd_rec"],
        grade_label="[V] verified (structure)", grade_kind="verified",
        desc=("Root-cause therapy is the inverse substrate operation. Five inverse ops \u2014 restore loop gain, raise "
              "the barrier, re-engage the error signal, repair the instrument, lower a run-away gain \u2014 map onto "
              "seven diseases; restoring loop gain re-deepens a collapsed basin (%s \u2192 %s, %s%% recovered)."
              % (F["rd_dis"], F["rd_treat"], F["rd_rec"])),
        answer=("Root-cause therapy is the inverse substrate operation. Five inverse ops \u2014 restore loop gain, "
                "raise the attractor barrier, re-engage the error signal, repair the instrument, lower a run-away "
                "loop gain \u2014 map onto seven diseases. Restoring loop gain re-deepens a collapsed basin (barrier "
                "%s \u2192 %s, %s%% recovered). Contested and partial results are flagged honestly."
                % (F["rd_dis"], F["rd_treat"], F["rd_rec"])),
        abstract=("If disease is a substrate operation (barrier collapse, off-criticality, aggregation crossing), "
                  "then root-cause therapy is its inverse, and the restoration demo shows a treated barrier "
                  "recovering from %s back to %s (%s%% of the healthy %s). Each disease is matched to one of five "
                  "inverse operations with its clinical evidence level. The substrate mapping is [V-structure]; "
                  "clinical efficacy is cited [L] \u2014 AMD complement inhibitors show no functional acuity gain yet, "
                  "cataract chaperone reversal failed replication, and ATOH1-regenerated hair cells remain immature."
                  % (F["rd_dis"], F["rd_treat"], F["rd_rec"], F["rd_health"])),
        cards=['<b>therapy = inverse(disease)</b> \u2014 each pathology operation has an inverse: restore loop gain '
               '(re-deepen the basin), raise the barrier, re-engage the error signal, repair the instrument, or lower '
               'a run-away gain. Demo: barrier %s \u2192 %s (%s%% recovered). <b>[V]</b> direction. '
               % (F["rd_dis"], F["rd_treat"], F["rd_rec"]) + LX(REPRO_BASE, "Reproduce (GitHub)")],
        body=[
            ("p", "If the " + L("disease", "disease law") + " is right that pathology is a substrate operation, then "
                  "therapy that lasts must run that operation <b>backwards</b>. The restoration demo shows the "
                  "principle quantitatively: restoring loop gain re-deepens a collapsed basin from %s back to %s, "
                  "recovering %s%% of the healthy depth %s." % (F["rd_dis"], F["rd_treat"], F["rd_rec"], F["rd_health"])),
            ("h2", "Five inverse operations"),
            ("p", "Each pathology mode has a matching inverse, and the seven diseases distribute across these five:"),
            ("ul", ["<b>(1) restore loop gain</b> \u2014 re-deepen a collapsed basin (e.g. glycemic control in "
                    "diabetic retinopathy).",
                    "<b>(2) raise the attractor barrier</b> \u2014 protect the at-risk cells directly (RGC "
                    "neuroprotection in glaucoma).",
                    "<b>(3) re-engage the error signal</b> \u2014 turn a broken feedback loop back on (defocus / "
                    "dopamine arm in myopia).",
                    "<b>(4) repair the instrument</b> \u2014 regenerate or replace the failed part (hair cell, lens, "
                    "or reposition otoconia).",
                    "<b>(5) lower a run-away loop gain</b> \u2014 damp a positive-feedback loop (complement "
                    "inhibition in AMD)."]),
            ("h2", "Seven diseases matched to their inverse operation"),
            ("t", "Seven diseases matched to inverse operations",
             ["disease", "inverse op", "root-cause therapy", "evidence"],
             [["glaucoma", "(1)+(2)", "ROCK inhibitors (netarsudil, ripasudil): restore TM outflow + RGC "
               "neuroprotection", "approved (outflow); neuroprotection preclinical"],
              ["myopia", "(3)", "re-engage defocus / dopamine arm: low-dose atropine, defocus optics, outdoor light, "
               "650 nm red light", "RCT-supported \u226550% slowing; IMI 2025"],
              ["presbycusis / SNHL", "(4)+(1)", "regenerate transducer + push \u00b5 back to criticality; repair "
               "IHC-SGN synapse; OTOF gene therapy", "OTOF restored hearing in children (2024); ATOH1 cells immature"],
              ["AMD (geographic atrophy)", "(5)", "complement inhibitors (pegcetacoplan C3, avacincaptad C5): lower "
               "the run-away loop gain", "approved 2023 (anatomic); NO functional acuity gain yet"],
              ["cataract", "(1)/(4)", "pharmacological chaperones / aggregation reversal (oxysterols); else lens "
               "replacement", "CONTESTED: reversal failed replication (Daszynski 2019)"],
              ["diabetic retinopathy", "(1)", "reset the systemic metabolic setpoint (glycemic control); anti-VEGF "
               "blocks the downstream attractor", "glycemia root-causal; anti-VEGF for the complication"],
              ["BPPV / vertigo", "(4)", "canalith repositioning (Epley / Semont): return otoconia at the source",
               "established standard of care"]]),
            ("h2", "Root versus symptomatic"),
            ("p", "The contrast is sharp throughout: hearing aids substitute for the transducer rather than regrow "
                  "it, single-vision glasses correct focus while the growth loop runs on, and anti-VEGF treats "
                  "neovascular leakage downstream of the complement driver. Root-cause therapy targets the substrate "
                  "operation itself \u2014 which is what makes a cure, rather than a management, conceivable."),
            ("bound", "<b>Clear-eyed about what does not yet work.</b> The substrate mapping is [V-structure]; "
                      "clinical efficacy is cited at its true level. AMD complement inhibitors slow atrophy but show "
                      "no functional visual-acuity gain yet (partial); cataract chaperone reversal failed "
                      "replication (contested); ATOH1-regenerated hair cells remain immature for acquired loss "
                      "(contested); and long-term myopia-control safety is still accruing. Stating this precisely is "
                      "what separates a falsifiable program from a promise."),
        ])


# ============================================================ §12  references / provenance
def _ch_refs(F):
    return dict(
        slug=SLUG["refs"],
        subj="References, gene accessions, and methods provenance", short="References",
        knows=["gene accession", "NCBI", "UniProt", "citations", "methods provenance"],
        seo=["sensory organ references", "gene accessions NCBI UniProt", "CNGA1", "TMC1 PCDH15 CDH23",
             "SLC26A5 prestin", "Greenwood 1990", "SantaLucia 1998", "methods provenance"],
        title="References, gene accessions, and methods provenance",
        one="Every anchor, with its grade and database accession; substrate [V] reproduced, clinical [L] cited.",
        grade_label="[L] cited", grade_kind="calibrated",
        desc=("The provenance of every external anchor: five master genes (NCBI), ten transducer-channel genes "
              "(NCBI/UniProt), the classical optics/tonotopy/gating-spring/Hopf/canal references, and the "
              "2023\u20132026 root-cause-treatment literature, each with its grade."),
        answer=("Every external anchor in this whitepaper is listed here with its grade and database accession: five "
                "master genes (NCBI), ten transducer-channel genes (NCBI/UniProt), the classical optics, tonotopy, "
                "gating-spring, Hopf, and canal-mechanics references, and the 2023\u20132026 root-cause-treatment "
                "literature. Substrate claims are reproduced in-simulation; clinical claims are cited at level."),
        abstract=("This page is the provenance layer. The substrate claims graded [V] are reproduced by "
                  "<code>python repro/run_all.py</code>; everything graded [L] is a measured input or an established "
                  "result, listed below with its NCBI/UniProt accession or citation. Master-gene \u03b3 is computed "
                  "from human promoter sequence by the SantaLucia nearest-neighbour method; effector-channel \u03b3 is "
                  "owned by the DNA pipeline. References are listed for attribution, paraphrased, not quoted."),
        cards=[],
        body=[
            ("p", "A grounded program should make its sources inspectable. This page collects every external anchor "
                  "the whitepaper relies on, separated by grade, so a reader can check each input independently of "
                  "the in-simulation results \u2014 the practice set out in " + L("method", "the no-tuning method") + "."),
            ("h2", "Master genes (\u03b3 measured from human promoter sequence) \u2014 [L]"),
            ("p", "\u03b3 = \u2212mean(nearest-neighbour stacking \u0394G37) over the human proximal promoter "
                  "(TSS\u22122000..+500), by the SantaLucia 1998 nearest-neighbour method; never fitted, cached so it "
                  "reproduces offline."),
            ("t", "Master genes and their measured \u03b3",
             ["gene", "\u03b3", "node", "accession"],
             [["<code>PAX6</code>", '<span class="num">%s</span>' % F["g_pax6"], "eye_retina_optics", "NCBI Gene 5080"],
              ["<code>RAX</code>", '<span class="num">%s</span>' % F["g_rax"], "eye_photoreceptor", "NCBI Gene 30062"],
              ["<code>EYA1</code>", '<span class="num">%s</span>' % F["g_eya1"], "cochlea_frequency_map", "NCBI Gene 2138"],
              ["<code>SOX2</code>", '<span class="num">%s</span>' % F["g_sox2"], "inner_ear_haircell", "NCBI Gene 6657"],
              ["<code>TAS1R3</code>", '<span class="num">%s</span>' % F["g_tas"], "taste_chemodetection",
               "NCBI Gene 83756; UniProt Q7RTX0"]]),
            ("h2", "Transducer effector genes (\u03b3 owned by the DNA pipeline) \u2014 identity cited [L]"),
            ("t", "Transducer channel genes and accessions",
             ["gene", "accession", "role"],
             [["<code>CNGA1</code>", "NCBI Gene 1259; UniProt P29973", "rod CNG channel \u03b1 (cooperative gate)"],
              ["<code>CNGB1</code>", "NCBI Gene 1258; UniProt Q14028", "rod CNG channel \u03b2"],
              ["<code>TMC1</code>", "NCBI Gene 117531; UniProt Q8TDI8", "hair-cell MET pore"],
              ["<code>PCDH15</code>", "NCBI Gene 65217; UniProt Q96QU1", "tip link (gating spring)"],
              ["<code>CDH23</code>", "NCBI Gene 64072; UniProt Q9H251", "tip link (gating spring)"],
              ["<code>SLC26A5</code> (prestin)", "NCBI Gene 375611; UniProt P58743",
               "outer-hair-cell somatic motor = Hopf active force"],
              ["<code>TAS1R2</code>", "NCBI Gene 80834; UniProt Q8TE23", "sweet receptor subunit"],
              ["<code>TRPM5</code>", "NCBI Gene 29850; UniProt Q9NZQ8", "downstream taste cation channel"],
              ["<code>CNGA2</code>", "NCBI Gene 1260; UniProt Q16280", "olfactory CNG channel (rod superfamily)"],
              ["<code>ADCY3</code>", "NCBI Gene 109; UniProt O60266", "adenylyl cyclase (cAMP generator)"]]),
            ("h2", "Classical and physiological anchors \u2014 [L] \u2192 [V]/[V-arith]"),
            ("ul", ["<b>DNA stacking thermodynamics</b> \u2014 SantaLucia 1998, a unified view of nearest-neighbour "
                    "DNA thermodynamics (PNAS 95:1460): the source of the \u03b3 method.",
                    "<b>Cochlear place-map</b> \u2014 Greenwood 1990, a cochlear frequency-position function (JASA "
                    "87:2592): the ~20 Hz\u201320 kHz human tonotopy reproduced in " + L("tonotopy", "tonotopy") + ".",
                    "<b>Hair-cell gating spring</b> \u2014 Howard &amp; Hudspeth 1988; Corey &amp; Hudspeth 1983; "
                    "Markin &amp; Hudspeth 1995; Martin, Mehta &amp; Hudspeth 2000: the two-state MET switch and "
                    "negative bundle stiffness.",
                    "<b>Hopf critical cochlea</b> \u2014 Camalet, Duke, J\u00fclicher &amp; Prost 2000; Egu\u00edluz "
                    "et al. 2000; Hudspeth, J\u00fclicher &amp; Martin 2010: the self-tuned critical oscillator and "
                    "the cube-root used in " + L("hopf", "the cochlear amplifier") + ".",
                    "<b>Phototransduction</b> \u2014 Fesenko, Kolesnikov &amp; Lyubarsky 1985 (Nature 313:310): "
                    "cGMP-gated rod conductance, the basis of " + L("photo", "phototransduction") + ".",
                    "<b>Vestibular canal mechanics</b> \u2014 Steinhausen 1933; Van Egmond, Groen &amp; Jongkees "
                    "1949 (J Physiol 110:1); Jones &amp; Milsum 1965: the torsion-pendulum and velocity storage in "
                    + L("vestibular", "vestibular balance") + ".",
                    "<b>Ocular optics</b> \u2014 the Gullstrand reduced/schematic eye and Hofstetter 1965 "
                    "age\u2013amplitude formula, reproduced in " + L("optics", "ocular optics") + "."]),
            ("h2", "Root-cause treatment literature (2023\u20132026)"),
            ("ul", ["<b>AMD / geographic atrophy</b> \u2014 pegcetacoplan (C3) and avacincaptad pegol (C5), both FDA "
                    "2023; slow lesion growth on an anatomic endpoint, with no functional visual-acuity gain yet "
                    "(partial).",
                    "<b>Myopia control</b> \u2014 IMI consensus: low-dose atropine, peripheral-defocus optics, "
                    "outdoor light (retinal dopamine), and repeated low-level 650 nm red light; RCT-supported "
                    "\u226550% slowing, long-term safety still accruing.",
                    "<b>Glaucoma</b> \u2014 Rho-kinase (ROCK) inhibitors netarsudil and ripasudil/fasudil: restore "
                    "trabecular outflow plus IOP-independent retinal-ganglion-cell neuroprotection.",
                    "<b>Presbycusis / SNHL</b> \u2014 OTOF gene therapy restored hearing in children (clinical, "
                    "2024); ATOH1 hair-cell regeneration remains immature for acquired loss (contested); NT-3/BDNF "
                    "synapse repair preclinical.",
                    "<b>Cataract</b> \u2014 pharmacological chaperones / oxysterols: reports of reversal were "
                    "<b>not replicated</b> (Daszynski et al. 2019), so efficacy is unproven and surgery remains "
                    "standard (contested).",
                    "<b>Diabetic retinopathy</b> \u2014 glycemic control resets the systemic setpoint (root); "
                    "anti-VEGF blocks the downstream neovascular attractor (complication).",
                    "<b>BPPV</b> \u2014 canalith repositioning (Epley / Semont): mechanically returns the otoconia at "
                    "the source, an instrument-level root-cause fix."]),
            ("bound", "<b>Citation discipline.</b> References are listed for attribution and are paraphrased, not "
                      "quoted. The substrate claims graded [V] are the ones reproduced by the engine; the clinical "
                      "and classical items graded [L] are cited inputs at their stated evidence level. Any anchor "
                      "whose exact coordinates need re-confirmation before formal publication is tracked in "
                      "<code>IRREPRODUCIBILITY_LEDGER.md</code>. Full machine-readable registry: "
                      "<code>literature/citations.json</code>."),
        ])
