# -*- coding: utf-8 -*-
"""
tissue.interpreter -- the tissue-level DUAL interpreter (해석기).

Reads one tissue domain and returns its reading SPLIT into the two orthogonal
projections of one morphogen field, exactly mirroring the cell-level reading that
splits a locus into gamma (LEVEL) and A4 (SHAPE):

    morphogen field c(x)
        |
        +--  LEVEL  = mean(c)        -> the SIZE channel   (tissue.level)
        +--  SHAPE  = robust_z(c)    -> the FORM channel   (tissue.shape)
        |
        +--  orthogonality certificate  (tissue.orthogonality)
        +--  grade ledger               (tissue.grading)

The dualization (이원화) is the contribution: SIZE and FORM are not two unrelated
computations (as the old engine treated them -- a magic-number dwell rule for
size, a coarse Jacobi for form). They are the LEVEL and SHAPE of ONE field, the
SAME insight v1.13 brought to the cell level, now made exact at the tissue level.

Deterministic: pure arithmetic over closed forms; 2x SHA-256; fail-closed in the
gate. lambda is inherited from the measured DB; nothing is fitted.
"""
import json, hashlib

from . import lock, level, shape, orthogonality, grading


def interpret_tissue(L_um, theta=None, k=4, lam_um=None):
    """The full dual reading of one tissue domain of axial length L_um.

    Returns a dict with the two projections, the orthogonality certificate, the
    grade ledger, and a completion status -- everything a reviewer needs to see
    that the precision is exact and the accuracy is honestly open.
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    if theta is None:
        theta, _, _ = lock.territory_theta()

    level_read = level.read_level(L_um, lam_um)
    shape_read = shape.read_shape(L_um, theta, k, lam_um)
    ortho = orthogonality.certify(L_um, lam_um)

    reading = {
        "_what": "tissue-level DUAL interpreter: one morphogen field projected into "
                 "LEVEL (size) and SHAPE (form); the cell-level gamma/A4 dualization "
                 "made exact at the tissue scale",
        "input": {"L_um": L_um, "lambda_um": round(lam_um, 8), "theta": theta,
                  "k_territories": k},
        "field": {
            "equation": "D*lap(c) - c/tau + source = 0  (screened-Poisson)",
            "lambda_um": round(lam_um, 8),
            "lambda_grade": "[L]-grounded (measured D, tau)",
            "closed_form_planar": "c(x) = cosh((L-x)/lambda)/cosh(L/lambda)",
        },
        "LEVEL_channel_size": level_read,
        "SHAPE_channel_form": shape_read,
        "orthogonality": ortho,
        "grade_ledger": grading.LEDGER,
        "completion": grading.completion_status(),
    }
    return reading


def reading_hash(reading):
    """Stable 16-char SHA-256 over the reading (determinism witness)."""
    blob = json.dumps(reading, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def developmental_run(devtimes=(1.0, 1.5, 2.0, 3.0), lam_um=None):
    """Run BOTH channels forward over developmental time on a growing domain.
    The LEVEL channel yields the SIZE budget trajectory; the SHAPE channel yields
    the FORM (territory) trajectory and its emergent negative allometry. The two
    channels share ONLY the field -- they are never fitted to each other."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    sizes = level.size_series(devtimes, lam_um)
    forms = []
    for t in devtimes:
        L = level.domain_length_um(t, lam_um)
        forms.append({"devtime": t, "L_um": round(L, 4),
                      **{kk: shape.read_shape(L, lam_um=lam_um)[kk]
                         for kk in ("n_territories", "apical_axial_frac",
                                    "territory_boundaries_um")}})
    allo = shape.form_allometry(list(devtimes), lam_um=lam_um)
    return {
        "LEVEL_size_trajectory": sizes,
        "SHAPE_form_trajectory": forms,
        "emergent_form_negative_allometry": allo,
        "note": "SIZE saturates at the fixed budget lambda; FORM's leading "
                "territory loses body-fraction as L grows -- both from the ONE "
                "field, neither fitted to the other.",
    }
