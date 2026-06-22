#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/_volume_lib.py — the ONE shared spine for the HTML volume builder and its drift gate.

Why this file exists (VP-SPEC v1.8 C1 — maximum reproducibility):
  The volume's reproducibility contract is "every displayed number is the code's own output,
  HTML↔code drift 0". To make that contract un-foolable, the BUILDER and the GATE must agree
  bit-for-bit on (a) how each increment's run.py output is captured, (b) how it is hashed, and
  (c) how it is escaped into HTML. If they used two copies of that logic they could silently
  diverge — so both import this single module. The chapter STRUCTURE (which run.py feeds which
  chapter) also lives here, as the single source both sides read.

What is NOT here:
  The editorial prose lives in build_volume.py (its own single source). This module carries only
  the mechanical, drift-critical helpers + the structural manifest. It imports nothing from the
  research increments except E4's MAGNITUDE_BLOCK tuple (so the disease-chapter firewall is the
  increment's own list verbatim, never a hand-copied duplicate).

No network, stdlib only. Deterministic.
"""
import os, sys, json, hashlib, subprocess, importlib.util, html as _html

# ----------------------------------------------------------------------------------------------
# package root (cwd-independent)
# ----------------------------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs", "eye")


# ----------------------------------------------------------------------------------------------
# the drift-critical primitives — IDENTICAL for builder and gate
# ----------------------------------------------------------------------------------------------
def run_capture(rel):
    """Run an increment/foundation module as a subprocess and return its RAW stdout (unstripped).

    This is THE single capture path. Builder and gate both call it, so the bytes they hash are
    produced the same way (same interpreter, same cwd=ROOT, text mode). The run.py modules are
    pure math with no RNG / no timestamps / no absolute paths, so the bytes are deterministic and
    portable (verify_seed.py [2] separately proves 2×-run determinism).
    """
    p = os.path.join(ROOT, rel)
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"run failed: {rel}\n{r.stderr[-800:]}")
    return r.stdout


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def esc(s):
    """HTML-escape element text for <pre>: only & < > (quotes are legal in element content).

    Exact inverse of unesc() on transcript content (which contains no pre-existing entities),
    so the gate can recover the byte-identical transcript from the page.
    """
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unesc(s):
    """Inverse of esc(): &lt;->< , &gt;->> , &amp;->& (order matters: amp last)."""
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def attr(s):
    """Escape a string for use inside a double-quoted HTML attribute."""
    return _html.escape(s, quote=True)


# ----------------------------------------------------------------------------------------------
# the disease-chapter firewall list — imported VERBATIM from E4's run.py (no hand-copy)
# ----------------------------------------------------------------------------------------------
def load_magnitude_block(rel="research/E4-congenital-blindness/run.py"):
    """Return an increment's MAGNITUDE_BLOCK tuple by importing the module (no execution: it is
    __main__-guarded). The gate asserts each disease/condition chapter carries none of its own
    increment's tokens + no '%', exactly mirroring that increment's machine-checked MAGNITUDE FIREWALL.
    Defaults to E4 for backward compatibility."""
    path = os.path.join(ROOT, rel)
    name = "_run_for_firewall_" + os.path.basename(os.path.dirname(path)).replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.MAGNITUDE_BLOCK)


# ----------------------------------------------------------------------------------------------
# the STRUCTURAL manifest — the single source of "which runs feed which chapter"
# (editorial prose is build_volume.py's; this is only the skeleton both sides verify against)
# ----------------------------------------------------------------------------------------------
VOLUME = [
    dict(
        slug="e0-carrier", num="E0",
        title="The carrier the eye is handed — light, its angle, and the DNA reading",
        one_liner="Rung 1: light emerges as the jammed-lattice wave at the invariant quantum size "
                  "D = 4.852620 pm, colour is its propagation angle \u03c7(\u03bb), and each master gene "
                  "is read as \u03b3 (LEVEL) + A4 (SHAPE).",
        runs=[
            "inherited/vp_light_emergence_quantum.py",
            "inherited/vp_color_by_angle.py",
            "inherited/vp_visible_band_canonical.py",
            "inherited/vp_dna_reading.py",
        ],
    ),
    dict(
        slug="e1-angle-to-cone", num="E1",
        title="Angle \u2192 cone — trichromacy as three angle-bands",
        one_liner="The three cone opsins sit at three distinct propagation angles \u03c7(\u03bbmax) "
                  "\u21d2 trichromacy; the cone/rod lineage emerges from the R19 switch ordered by "
                  "spinodal(\u03b3), with A4 shape breaking \u03b3-ties.",
        runs=["research/E1-angle-to-cone/run.py"],
    ),
    dict(
        slug="e2-single-photon-switch", num="E2",
        title="The single-photon switch — the all-or-none collapse",
        one_liner="One quantum of drive across the spinodal h*(\u03b3) flips the R19 switch "
                  "discontinuously; the cooperativity IS the cubic \u2212s\u00b3 (order n=3) and is "
                  "necessary. This is the event-detector that discards the carrier frequency.",
        runs=["research/E2-single-photon-switch/run.py"],
    ),
    dict(
        slug="e3-image-formation", num="E3",
        title="Image formation — the WHERE channel survives the collapse",
        one_liner="Snell's law is the transverse-oscillation match and n = c_vac/c_med = "
                  "\u221a((B/\u03c1) ratio); the reduced eye forms a real inverted image (a spatial "
                  "position code) while the colour-angle \u03c7(\u03bb) rides through untouched.",
        runs=["research/E3-image-formation/run.py"],
    ),
    dict(
        slug="e4-congenital-blindness", num="E4",
        title="Congenital blindness — the switch that cannot flip (theoretical, non-clinical)",
        one_liner="On the frozen substrate, loss-of-function is the R19 switch held below its own "
                  "spinodal so the all-or-none flip never fires; the rescue-DIRECTION is forced by "
                  "the same fold and stated direction-only behind a machine-checked magnitude firewall.",
        runs=["research/E4-congenital-blindness/run.py"],
    ),
    dict(
        slug="e5-frequency-ladder", num="E5",
        title="The frequency ladder, quantified — a ~13-order collapse",
        one_liner="\u03bd_light \u2248 10\u00b9\u2074 Hz drops ~13 orders to the ~10\u2013100 Hz neural band by "
                  "event-detection + low-pass, NOT mixing: the output is carrier-frequency-invariant "
                  "and the surviving band scales as 1/\u03c4.",
        runs=["research/E5-frequency-ladder/run.py"],
    ),
    dict(
        slug="e6-why-visible", num="E6",
        title="Why the band is visible — geometry places it, photochemistry pins it",
        one_liner="Two unrelated constraints select ~380\u2013750 nm: lattice geometry sandwiches "
                  "visible in m between x-ray and infrared, but the angle never gates a band \u2014 the "
                  "reversible 11-cis\u2192all-trans energy window (~1.8\u20133.3 eV) pins the edges.",
        runs=["research/E6-why-visible/run.py"],
    ),
    dict(
        slug="e7-cascade-lowpass", num="E7",
        title="The cascade as the band-setting low-pass — f_c = \u03b2/(2\u03c0\u03c4)",
        one_liner="The frozen recovery law w \u2190 w + dt\u00b7(s\u2212\u03b2w)/\u03c4_s IS a single-pole "
                  "low-pass; the surviving band is the cutoff f_c = \u03b2/(2\u03c0\u03c4_s), invariant to "
                  "both the carrier and \u03b3 \u2014 it is \u03c4 that fixes the band.",
        runs=["research/E7-cascade-lowpass/run.py"],
    ),
    dict(
        slug="e8-graded-to-spike-rate", num="E8",
        title="Graded \u2192 spike-rate re-quantisation — the hand-off (spine complete)",
        one_liner="The retina re-encodes the graded signal as a ganglion spike RATE: a thresholded "
                  "(rheobase), bounded (depolarisation-block ceiling), monotone clock that tracks the "
                  "slow envelope and never re-introduces the carrier \u2014 the collapse is preserved end-to-end.",
        runs=["research/E8-graded-to-spike-rate/run.py"],
    ),
    dict(
        slug="e9-red-green-dichromacy", num="E9",
        title="Red-green colour vision \u2014 the angle map with one sample lost (theoretical, non-clinical)",
        one_liner="Colour is the propagation angle, so the three cones are three angle-samples and the "
                  "three discrimination axes are their pairwise margins; the green-red (M-L) margin is the "
                  "smallest \u21d2 the angle map forces red-green as the most fragile colour axis, and "
                  "coincident \u03bbmax gives an exactly-zero margin \u2014 dichromacy (lose a sample) and "
                  "anomalous trichromacy (peaks converge) are one continuum, stated direction-only behind "
                  "a machine-checked magnitude firewall.",
        runs=["research/E9-red-green-dichromacy/run.py"],
    ),
    dict(
        slug="e10-light-dark-adaptation", num="E10",
        title="Light/dark adaptation \u2014 gain control as the switch on its saturating branch",
        one_liner="Adaptation needs no new machinery: it is the same R19 switch on its steady-state ON "
                  "branch, where the cubic makes the response saturate (s* \u2192 h^(1/3)) \u2014 so a huge "
                  "background range is log-compressed (by the cubic order n=3), the incremental gain falls "
                  "automatically as the surround brightens, and the FRACTIONAL (contrast) gain is constant "
                  "at exactly 1/n = 1/3, a Weber-Fechner-like law forced by the cube and independent of \u03b3.",
        runs=["research/E10-light-dark-adaptation/run.py"],
    ),
    dict(
        slug="e11-accommodation-refraction", num="E11",
        title="Accommodation & refractive error \u2014 the power\u2194length match (theoretical, non-clinical)",
        one_liner="E3's single-surface eye is in focus for distance exactly when its power and its length "
                  "satisfy P\u00b7L = n\u2082 (the match ratio \u03c1 = 1, a whole curve); refractive error is the "
                  "signed mismatch \u2014 \u03c1>1 puts the distant focus in front (myopia), \u03c1<1 behind "
                  "(hyperopia), reachable by an eye too long OR too powerful (only the product matters); "
                  "accommodation is a one-signed power lever (round the lens, R\u2193 \u21d2 P\u2191) that pulls near "
                  "objects into focus, and the growth axis follows the substrate size law dwell \u221d \u03b3^1.5 "
                  "\u2014 all stated direction-only behind a machine-checked magnitude firewall.",
        runs=["research/E11-accommodation-refraction/run.py"],
    ),
    dict(
        slug="e12-acquired-degeneration", num="E12",
        title="Acquired & degenerative disease \u2014 the switch carried over its fold (theoretical, non-clinical)",
        one_liner="A degenerative disease is not a switch born unable to flip (the static congenital failure of "
                  "E4) but a switch that worked and is carried OVER its own fold by accumulating stress: on the "
                  "frozen R19 field the healthy basin survives a slow stress up to the spinodal \u2212h*(\u03b3), then "
                  "collapses in one step \u2014 a tipping point. Because the transition is a fold it is HYSTERETIC "
                  "(collapse at \u2212h*, recovery only at +h*, loop width 2\u00b7h* \u2014 so early differs categorically "
                  "from late), and because any bistable transducer fails by a fold the SAME catastrophe geometry is "
                  "reached by many routes (load the switch, or shallow its basin) \u2014 so the shared late picture "
                  "across AMD, glaucoma and diabetic retinopathy is forced while the identity of each primary stress, "
                  "and the disease genetics, stay emphatically open. All stated direction-only behind a "
                  "machine-checked magnitude firewall.",
        runs=["research/E12-acquired-degeneration/run.py"],
    ),
]

# disease/condition chapters: each must pass the magnitude firewall of its OWN increment.
# (gate_volume re-checks the rendered HTML against the increment's MAGNITUDE_BLOCK + no '%'.)
DISEASE_CHAPTERS = {
    "e4-congenital-blindness": "research/E4-congenital-blindness/run.py",
    "e9-red-green-dichromacy": "research/E9-red-green-dichromacy/run.py",
    "e11-accommodation-refraction": "research/E11-accommodation-refraction/run.py",
    "e12-acquired-degeneration": "research/E12-acquired-degeneration/run.py",
}


def chapter_by_slug(slug):
    for c in VOLUME:
        if c["slug"] == slug:
            return c
    raise KeyError(slug)


# files the volume must contain (no-omission, checked by gate_volume + listed in seed.json)
def expected_files():
    files = ["docs/eye/index.html", "docs/eye/assets/volume.css",
             "docs/eye/sitemap.xml", "docs/eye/robots.txt", "docs/eye/llms.txt"]
    for c in VOLUME:
        files.append(f"docs/eye/{c['slug']}/index.html")
        files.append(f"docs/eye/facts/{c['slug']}.json")
    return files


META = dict(
    title="VP \u2014 The Eye Volume: the high\u2192low down-conversion ladder (E0\u2192E8) + mechanism extensions (E9\u2013E12)",
    author="Young Jae Lee",
    orcid="0009-0002-7535-8245",
    license="CC BY 4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    doi_concept="10.5281/zenodo.20790134",
    site="https://jamming-physics.org",
    base="https://jamming-physics.org/eye/",   # intended canonical home once merged to the live site
)
