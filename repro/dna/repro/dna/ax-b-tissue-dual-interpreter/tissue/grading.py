# -*- coding: utf-8 -*-
"""
tissue.grading -- the honest per-channel grade ledger for the tissue interpreter.

It enforces the single distinction the whole handover is built on:
    PRECISION (정밀): how exactly/reproducibly the engine computes ITS OWN formula.
    ACCURACY  (정확): how closely that formula matches an INDEPENDENT measurement.

Every [V] below means "reproduces bit-for-bit / exact closed form" -- it is
PRECISION, not a match to a measurement. The two channels that would be ACCURACY
(size vs a real organ mass; form vs measured contact) are graded [O] with the
EXACT missing dataset named -- never quietly claimed as accurate (prohibition B1).

This module does not compute anything physical; it is the contract that the
interpreter and the gate both read, so the grades are declared in ONE place and
cannot drift between the code and the prose.
"""

GRADE_MEANINGS = {
    "[L]": "locked: independently measured / universal law, cited; legitimate input",
    "[V]": "verified: exact closed form / bit-for-bit reproducible (PRECISION, not "
           "a measurement match)",
    "[F]": "fixed modelling choice (functional form / generic central value); declared",
    "[O]": "open: precision-exact but NO independent measurement compared yet; the "
           "specific missing dataset is named",
}


# the per-channel grade ledger -- the tissue mirror of the cell-level table
LEDGER = [
    {
        "channel": "intrinsic length lambda = sqrt(D*tau)",
        "grade": "[L]",
        "basis": "composed of two MEASURED morphogen constants (D, tau; Kicheva "
                 "2007), read from the locked DB; no fit",
        "kind": "grounded",
    },
    {
        "channel": "LEVEL projection = mean(c) = (lambda/L)*tanh(L/lambda)",
        "grade": "[V]",
        "basis": "exact closed-form integral of the screened-Poisson field; "
                 "deterministic, bit-for-bit",
        "kind": "precision",
    },
    {
        "channel": "SHAPE projection = robust_z(c); territory boundaries "
                   "x_k = L - lambda*acosh(theta_k*cosh(L/lambda))",
        "grade": "[V]",
        "basis": "exact closed-form threshold crossings; SAME robust_z operator as "
                 "the cell-level A4; deterministic",
        "kind": "precision",
    },
    {
        "channel": "orthogonality LEVEL ⟂ SHAPE",
        "grade": "[V]",
        "basis": "SHAPE invariant under source-scale and background-offset to "
                 "machine epsilon (analytic) + non-redundant on a geometry panel "
                 "(numeric)",
        "kind": "precision",
    },
    {
        "channel": "territory partition theta",
        "grade": "[F]",
        "basis": "positional-information threshold; modelling choice; interpreter "
                 "required theta-robust over [0.3, 0.7]",
        "kind": "choice",
    },
    {
        "channel": "developmental supply exponent alpha (extent ~ devtime^alpha)",
        "grade": "[F]",
        "basis": "single UNIVERSAL rule applied identically to all; never per-organ",
        "kind": "choice",
    },
    {
        "channel": "SIZE magnitude vs real organ mass",
        "grade": "[O]",
        "basis": "ACCURACY untested. Needs a MEASURED per-organ developmental "
                 "growth-rate atlas; the engine does NOT compare (would be back-fit)",
        "kind": "accuracy_open",
        "named_obstacle": "per-organ developmental growth-rate atlas "
                          "(e.g. staged organ-mass trajectories)",
    },
    {
        "channel": "FORM (territory partition) vs real anatomy",
        "grade": "[O]",
        "basis": "ACCURACY untested. Needs MEASURED enhancer-promoter contact "
                 "(Hi-C/Micro-C/capture-C) or a tissue-territory boundary map",
        "kind": "accuracy_open",
        "named_obstacle": "measured chromatin contact (Hi-C/Micro-C/capture-C) "
                          "or staged tissue-territory boundary map",
    },
]


def precision_channels():
    return [e for e in LEDGER if e["kind"] == "precision"]


def open_accuracy_channels():
    return [e for e in LEDGER if e["kind"] == "accuracy_open"]


def declared_grades():
    """All grade symbols this interpreter uses -- the gate checks they are exactly
    the four sanctioned ones and that each carries a basis string."""
    return sorted({e["grade"] for e in LEDGER})


def completion_status():
    """The earned-completion test (handover 04): complete IFF every readable
    channel is either ACCURATE (a number landed on a measurement) or HONESTLY
    BOUNDED (precision-exact + named [O] obstacle). Here, two channels are still
    [O] (size-vs-mass, form-vs-contact) -> NOT complete; precision is real, the
    accuracy work is named. We say so plainly (no false victory)."""
    open_ch = open_accuracy_channels()
    return {
        "complete": False,
        "reason": "two channels precision-exact but accuracy-untested [O]; named "
                  "obstacles below. Precision (정밀) is earned; accuracy (정확) is "
                  "not yet claimed.",
        "open_channels": [{"channel": e["channel"],
                           "named_obstacle": e["named_obstacle"]} for e in open_ch],
        "what_would_close_it": "supply the named measured datasets, run the rank "
                               "test vs barrier/contact with a shuffle control, "
                               "pre-register the sign; then and only then mark 정확.",
    }
