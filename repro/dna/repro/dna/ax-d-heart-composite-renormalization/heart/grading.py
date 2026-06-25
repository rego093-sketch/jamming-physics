# -*- coding: utf-8 -*-
"""
heart.grading -- the honest per-channel grade ledger for the heart composite-renormalization
accuracy test. The ONE place precision != accuracy is enforced.

The point of this appendix is to push toward ACCURACY (not just precision) on the heart --
the case that 'failed' in Appendix A. So the ledger is unusually explicit about which
results are parameter-free measured/logical truths [V]/[L], which are consistency checks
[L]/[O], and which remain illustrations [F] or open obstacles [O]. We do NOT declare the
heart 'solved'; we report exactly how far the accuracy push gets and name the single
measurement that would close it.
"""

GRADE_MEANINGS = {
    "[L]": "locked: independently measured/published value or exact theorem, cited",
    "[V]": "verified: exact theorem / logical certainty / parameter-free inequality (precision)",
    "[F]": "fixed modelling choice (monotone schedule / central value); declared",
    "[O]": "open: precision/consistency real but the tight co-registered measurement is absent; named",
}


LEDGER = [
    {
        "channel": "exact two-phase bracket  B_Reuss <= B_eff <= B_Voigt  (cell + ECM)",
        "grade": "[V]",
        "basis": "exact elastic-mixture theorems (Voigt 1889 isostrain upper, Reuss 1929 "
                 "isostress lower, Hill 1952 bounds) with BOTH phases real (B>0); evaluated "
                 "exactly. No free parameter.",
        "kind": "precision",
    },
    {
        "channel": "RESULT A -- pure cell-jamming insufficiency (falsification)",
        "grade": "[V]",
        "basis": "parameter-free inequality on MEASURED moduli: embryonic cell ceiling "
                 "(~1.25 kPa) << measured tissue (~10-18 kPa), so the stiff ECM phase / "
                 "cell maturation is necessary; pure jamming (Appendix C) is falsified for "
                 "the trajectory.",
        "kind": "precision",
    },
    {
        "channel": "RESULT B -- gamma orthogonal to the stiffening (explanation of the null)",
        "grade": "[V]",
        "basis": "logical certainty: gamma is sequence-fixed -> time-invariant -> cannot "
                 "encode a rising trajectory; reproduces the measured Appendix A heart null "
                 "(rho=+0.071, p=0.882).",
        "kind": "precision",
    },
    {
        "channel": "measured phase moduli (cell, ECM) and tissue trajectory",
        "grade": "[L]",
        "basis": "independently measured, cited: single-cardiomyocyte AFM (immature ~1.25 "
                 "kPa, adult ~35 kPa), decellularized myocardial ECM (LV ~5, SAN ~17 kPa), "
                 "myocardium stiffening 0.1+0.3*day / E2<1 -> E14~10 / adult 10-50 kPa.",
        "kind": "grounded",
    },
    {
        "channel": "RESULT C -- two-phase bracket contains the measured ventricular tissue",
        "grade": "[L]",
        "basis": "consistency: the exact bracket from measured ventricular inputs (cell 35, "
                 "LV ECM 5 kPa, phi_cell 0.8) contains the measured adult ventricular tissue "
                 "(~18 kPa). Input-sensitive (isolated cells stiffer than bulk); a tight "
                 "prediction needs a co-registered preparation.",
        "kind": "grounded",
    },
    {
        "channel": "composition-flow trajectory reproduces the embryonic->adult span",
        "grade": "[F]",
        "basis": "illustration: monotone measured-grounded schedules (ECM fraction rising, "
                 "cell jamming ramping) at FIXED measured phase moduli reproduce the "
                 "stiffening span; the schedule SHAPE is a modelling choice, the phase "
                 "moduli are measured.",
        "kind": "choice",
    },
    {
        "channel": "collagen volume-fraction trajectory phi_ecm(t)",
        "grade": "[F]",
        "basis": "the RISE is measured (collagen rises faster than heart weight; "
                 "neonatal-high collagen); the exact per-stage fraction shape is a "
                 "documented monotone choice standing in for co-registered stereology.",
        "kind": "choice",
    },
    {
        "channel": "TIGHT quantitative trajectory prediction (zero free parameters)",
        "grade": "[O]",
        "basis": "ACCURACY not yet tight. Needs a SINGLE co-registered developmental series "
                 "in ONE preparation: (E_tissue, phi_ECM, phi_cell, B_cell, B_ECM) per "
                 "stage. With it the composite predicts E_tissue(t) parameter-free and the "
                 "match becomes a tight accuracy [V].",
        "kind": "accuracy_open",
        "named_obstacle": "co-registered developmental series (tissue modulus + both volume "
                          "fractions + both phase moduli) in one preparation",
    },
    {
        "channel": "active tension contribution (myosin) vs passive composite",
        "grade": "[O]",
        "basis": "ACCURACY untested. Majkut shows the contraction wave speed is LINEAR in "
                 "E_t (active), distinct from the passive VP elastic wave c=sqrt(B/rho); "
                 "separating active from passive needs a measured tension series.",
        "kind": "accuracy_open",
        "named_obstacle": "measured active-tension vs passive-stiffness decomposition per "
                          "developmental stage",
    },
    {
        "channel": "large-strain (nonlinear strain-stiffening) behaviour",
        "grade": "[O]",
        "basis": "ACCURACY untested. Collagen and myocardium strain-stiffen; the bracket "
                 "here is the small-strain modulus. Large-strain needs a measured "
                 "stress-strain curve per stage.",
        "kind": "accuracy_open",
        "named_obstacle": "measured per-stage stress-strain curves (nonlinear modulus)",
    },
]


def precision_channels():
    return [e for e in LEDGER if e["kind"] == "precision"]


def grounded_channels():
    return [e for e in LEDGER if e["kind"] == "grounded"]


def open_accuracy_channels():
    return [e for e in LEDGER if e["kind"] == "accuracy_open"]


def declared_grades():
    return sorted({e["grade"] for e in LEDGER})


def completion_status():
    """Earned-completion test. The heart accuracy push achieves: an exact two-phase bracket
    [V], a parameter-free falsification of pure jamming [V], a logical explanation of the
    Appendix A null [V], measured phase moduli [L], and bracket-consistency with the
    measured tissue [L]. It does NOT achieve a tight zero-parameter trajectory prediction --
    three accuracy channels remain [O]. So completion is honestly False; the heart is now
    MECHANISTICALLY EXPLAINED and BRACKETED, not yet quantitatively closed."""
    open_ch = open_accuracy_channels()
    return {
        "complete": False,
        "reason": "the heart is converted from an unexplained Appendix-A null into a "
                  "mechanistically explained, exactly-bracketed, falsification-tested case: "
                  "the stiffening axis is composition (ECM)+maturation, pure jamming is "
                  "falsified [V], gamma-orthogonality is explained [V], and the exact "
                  "bracket from measured ventricular inputs contains the measured tissue "
                  "[L]. But a TIGHT zero-parameter trajectory prediction is not yet made -- "
                  "three accuracy channels remain [O]. Precision/consistency earned; full "
                  "accuracy not yet claimed.",
        "open_channels": [{"channel": e["channel"],
                           "named_obstacle": e["named_obstacle"]} for e in open_ch],
        "what_would_close_it": "obtain the co-registered developmental series in one "
                               "preparation, feed measured (phi_ECM, phi_cell, B_cell, "
                               "B_ECM) per stage into the SAME composite, predict E_tissue(t) "
                               "with zero free parameters, compare to the measured "
                               "E_tissue(t) with a shuffle control and a pre-registered "
                               "sign; then and only then mark the heart trajectory 정확.",
        "distance_to_close": "ONE measured dataset (named above). The machinery, the "
                             "measured phase moduli, the falsification, and the explanation "
                             "are already in place.",
    }
