#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setpoint_failure.py  --  Chronobiology (Circadian) PATHOLOGY module. Covers this package's MAJOR (non-rare)
diseases. Disease here is NOT a local lesion; it is a FAILURE of a defended setpoint driven by a CLOCK --
a loss of clock-imposed rhythm, a phase MISALIGNMENT between the internal clock and external time, or an
attractor-shift in a gated setpoint -- on the SAME R19 substrate that the rest of the framework uses.
RARE / monogenic forms (e.g. familial advanced sleep phase, monogenic CRSWD) are owned by disease_wp and
only cross-referenced here.

GRADES (C3): cited risk / setpoint anchor [L]; reproduced shape from the live discriminants [V]; ABSOLUTE
incidence / rate [O] (obstacle stated). Composition with disease_wp: a monogenic lesion enters as a cited
PARAMETER; the systemic trajectory is computed here. Polygenic / acquired / shift-work disease lives here.

This module is WIRED to the live engine: every failure carries the actual discriminant readout that
demonstrates its mechanism, so the pathology cannot drift from the dynamics that produced it.
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_substrate import barrier, spinodal, settle
import importlib
eng = importlib.import_module("vp_clk_engine")

# mind seam DOI (the FELT/affect layer this package gates into but never claims)
MIND_DOI = "10.5281/zenodo.20694404"


def setpoint_shift(gamma, loop_gain_drop):
    """Effect of a clock/loop-gain drop on a defended setpoint, DERIVED from the R19 double well.

    The defended setpoint sits in a basin whose depth is the R19 barrier B(gamma). A circadian clock
    that gates the setpoint contributes part of that restoring gain: when clock gating is lost (loop_gain_drop
    -> 1) the EFFECTIVE barrier that holds the setpoint shrinks, so the defended state drifts and, in the
    limit, crosses to a pathological basin (Kramers crossing -- the SAME kernel the oncology modules use).
    No new constant: the shift is the cited barrier scaled by the (1 - loop_gain_drop) residual gain."""
    b0 = float(barrier(gamma))
    frac = min(max(loop_gain_drop, 0.0), 0.999)
    residual = b0 * (1.0 - frac)
    # crossing rate ~ exp(-residual/eps) relative to the healthy exp(-b0/eps); report the log-ratio (eps=1)
    rel_log_crossing_rate = round(float(b0 - residual), 6)      # = b0*frac; >0 means faster crossing than healthy
    return dict(healthy_barrier=round(b0, 6), residual_barrier=round(residual, 6),
                rel_log_crossing_rate=rel_log_crossing_rate,
                crossed=bool(frac >= 0.999),
                note="clock gating is part of the restoring gain; losing it shrinks the basin holding the "
                     "setpoint -> drift, then Kramers crossing to a pathological attractor (same kernel as oncology)")


def _findings():
    """Pull the live discriminant outputs once."""
    return eng.research_findings()


def failures():
    f = _findings()
    rc4, rc5, rc6, tx1 = f["RC4"], f["RC5"], f["RC6"], f["TX1"]
    return [
        # ---- 1. Circadian rhythm sleep-wake disorders (the direct phenotype) --------------------------------
        {
            "site": "circadian rhythm sleep-wake disorders (DSWPD, ASWPD, non-24h, ISWRD, shift-work, jet lag)",
            "class": "clock<->environment phase misalignment (the clock runs, but at the wrong phase vs the demand schedule)",
            "mechanism": "the self-sustained SCN clock (RC1) free-runs near ~24 h; entrainment is PRC-limited to ~1 h/day "
                         "(RC2), so a large internal/external phase gap cannot be closed quickly -> sustained misalignment.",
            "discriminant": {"RC5_reentrainment_cycles": rc5["reentrainment_cycles"],
                             "RC5_demand_aligned_cortisol": rc5["externally_aligned_cortisol_amp"]},
            "anchor": "chronotype / phase-marker data (DLMO) [L]; PRC-limited re-entrainment reproduced [V]; "
                      "absolute prevalence [O]",
            "disease_wp_xref": "familial advanced sleep-phase (PER2/CK1d) and monogenic CRSWD are owned by disease_wp "
                               "as named monogenic entities; their clock-gene lesion enters here as a cited phase parameter",
        },
        # ---- 2. Shift-work metabolic & cardiovascular risk -------------------------------------------------
        {
            "site": "shift-work metabolic & cardiovascular disease (T2D, obesity, hypertension, MetS components)",
            "class": "loss of clock-imposed rhythm on gated metabolic + pressure setpoints (cross-cutting seam)",
            "mechanism": "the clock IMPOSES a daily rhythm on defended setpoints (RC4: gated vs ablated cortisol amplitude "
                         ">50x). Chronic misalignment flattens / phase-shifts that gating -> the metabolic and hemodynamic "
                         "setpoints (homeostasis_thermometabolic / _hemodynamic seams) lose their daily organisation.",
            "discriminant": {"RC4_gated_amp": rc4["gated_cortisol_amplitude"],
                             "RC4_ablated_amp": rc4["ablated_cortisol_amplitude"],
                             "RC4_clock_creates_rhythm": rc4["clock_creates_rhythm"]},
            "anchor": "RR vs shift-work exposure [L]; cross-loop gating disruption reproduced [V]; absolute incidence [O]",
            "disease_wp_xref": "common acquired disease owned here; monogenic MODY / familial dyslipidaemia subtypes "
                               "remain disease_wp entities (composition rule §6.2 of the framework map)",
        },
        # ---- 3. Shift-work cancer risk (IARC 2A) ----------------------------------------------------------
        {
            "site": "night-shift-work cancer risk (IARC Group 2A: 'circadian disruption')",
            "class": "clock-gated elevation of the Kramers crossing rate (clock control of the R19 switch + immune gating)",
            "mechanism": "losing clock gating shrinks the effective barrier holding cellular setpoints -> raises the "
                         "crossing rate (setpoint_shift below). This is the SAME oncology kernel the mechanical packages "
                         "use; circadian disruption is a RATE MULTIPLIER on it, not a separate carcinogen.",
            "discriminant": {"setpoint_shift_at_gain_drop_0.5":
                                 setpoint_shift(1.0, 0.5), "interpretation":
                                 "a 50% loss of clock gating raises the log-crossing-rate by b0*0.5 vs the gated basin"},
            "anchor": "RR vs cumulative night-shift years (IARC 2A anchor) [L]; clock-gated crossing reproduced [V]; "
                      "absolute attributable fraction [O]",
            "disease_wp_xref": "hereditary cancer syndromes (Li-Fraumeni etc.) are disease_wp; the acquired shift-work "
                               "rate multiplier is owned here",
        },
        # ---- 4. Seasonal / circadian-misalignment depression (THE MIND SEAM) ------------------------------
        {
            "site": "seasonal & circadian-misalignment depression (the CIRCADIAN contributor mind LOCKED)",
            "class": "circadian export INTO mind's affect layer -- a TIMING perturbation of the HPA setpoint, not "
                     "depression itself",
            "mechanism": "circadian misalignment flattens the gated HPA cortisol rhythm (RC6 flattening index grows "
                         "monotonically 0->~2 with misalignment). A sustained, demand-misaligned cortisol signal IS "
                         "mind's WITHDRAWAL-bias handle (b<0): it lowers effective coupling k=kappa/(1+|b|) -> "
                         "hypo-coordination, and under mind's E0 plasticity layer the excursion CHRONIFIES.",
            "discriminant": {"RC6_hpa_flattening_index": rc6["hpa_flattening_index"],
                             "RC6_sign_matches_mind": rc6["sign_consistent_with_mind_depression_handle"]},
            "anchor": "seasonal-affective / phase-shift mood data [L]; flattening SIGN + mind-direction consistency [V]; "
                      "MAGNITUDE of the handle [O] (owned by mind)",
            "firewall": "SIGN only; efficacy=0; the FELT quality of low mood stays in mind (consciousness_claim=0, hard "
                        "problem OPEN). This package supplies the timing perturbation; mind owns the affect.",
            "mind_xref": "mind 27 (depression / TRD chronification) explicitly LOCKED the CIRCADIAN contributor; "
                         f"this entry supplies it. Mind concept DOI {MIND_DOI}.",
        },
        # ---- 5. Circadian disruption in autism (cross-ref mind autism D-series) ----------------------------
        {
            "site": "circadian / sleep disruption in autism (comorbid; aggravates the coupling substrate)",
            "class": "circadian export INTO mind's autism layer -- a TIMING / sleep-consolidation perturbation that "
                     "loads onto mind's coupling-organisation reading of autism, NOT a claim that the clock causes autism",
            "mechanism": "autism shows a high rate of circadian/melatonin-rhythm and sleep abnormalities. In this "
                         "framework the clock gates HPA and supports sleep-dependent consolidation; a disrupted clock "
                         "degrades that gating and the nightly window in which cross-frequency coupling is consolidated. "
                         "mind models autism as a BRAINWAVE-PATHWAY / coupling-organisation problem (PAC down, E/I toward "
                         "excitation); circadian disruption is a SIGN-level aggravator of that same coupling substrate.",
            "discriminant": {"RC4_clock_gates_setpoint": rc4["clock_creates_rhythm"],
                             "RC6_misalignment_flattens_HPA": rc6["flattening_grows_with_misalignment"]},
            "anchor": "melatonin-rhythm / actigraphy data in autism [L]; clock-gating + misalignment SIGN reproduced [V]; "
                      "absolute effect on phenotype [O]",
            "firewall": "SIGN only; efficacy=0. The clock does NOT cause autism here; it perturbs the timing/sleep "
                        "substrate that mind's coupling pathology lives on. The coupling/felt pathology stays in mind.",
            "mind_xref": "mind 18 (autism three-axis: pathway vs excitability vs frontal) and mind 19 (autism chemical "
                         f"limits) own the autism mechanism; this is a timing seam into them. Mind concept DOI {MIND_DOI}.",
        },
    ]


def management():
    """Chronotherapy / management section -- the TREATMENT axis, derived from the RC2 PRC (TX1). DIRECTION and
    TIMESCALE only; efficacy is firewalled to 0; this is NOT medical advice."""
    tx1 = _findings()["TX1"]
    return {
        "principle": "treat circadian disease by RE-ALIGNING the clock with a PRC-correct zeitgeber, not by sedating a "
                     "symptom. The control law is the phase-response curve (RC2a); timing IS the therapy.",
        "levers": [
            {"lever": "timed bright light", "phase_rule": "morning light ADVANCES, evening light DELAYS (light PRC)",
             "use": "advance a delayed clock (DSWPD) with morning light; delay an advanced clock (ASWPD) with evening light",
             "grade": "[V] direction / [L] clinical timing window / [O]=0 efficacy"},
            {"lever": "timed melatonin", "phase_rule": "melatonin PRC is ~ANTIPHASE to light (~12 h apart): evening "
                                                       "melatonin ADVANCES",
             "use": "evening low-dose melatonin to advance a delayed clock; the antiphase relation is reproduced "
                    f"(light/melatonin antiphase = {tx1['light_melatonin_antiphase']})",
             "grade": "[V] direction / [L] timing / [O]=0 efficacy"},
            {"lever": "wake therapy (sleep deprivation)", "phase_rule": "no clock re-alignment; a transient homeostatic "
                                                                        "lift of the depressed operating point (mind seam)",
             "use": "rapid but TRANSIENT antidepressant lift; relapses after recovery sleep unless paired with a "
                    "phase-stabilising lever (light/melatonin) -- direction/timescale only",
             "grade": "[V] direction / [O] magnitude / efficacy=0"},
            {"lever": "behavioural entrainment (timed meals / activity / dark discipline)",
             "phase_rule": "strengthen zeitgeber amplitude -> wider Arnold tongue (RC2b) -> more robust entrainment",
             "use": "stabilise the phase that the pharmacological/light levers set; weak zeitgebers entrain only near "
                    "the natural period",
             "grade": "[V] direction / [O] magnitude"},
        ],
        "wrong_phase_warning": "the SAME zeitgeber at the WRONG phase WORSENS misalignment (TX1: wrong-phase delay grows "
                               f"the gap, resulting wrong-phase delay = {tx1['resulting_delay_h_wrong_phase']}). Timing "
                               "sign is the whole therapy; mis-timed light/melatonin is iatrogenic.",
        "firewall": "efficacy=0; not medical advice; this section asserts the DIRECTION and TIMESCALE of chronotherapy "
                    "(the clock's control law), never a dose-response or an outcome claim.",
        "mind_seam_note": f"the mood levers act on the timing perturbation this package exports; the affect response is "
                          f"owned by mind (concept DOI {MIND_DOI}).",
    }


def status():
    return {
        "model": "R19 clock-gated setpoint failure: loss of clock-imposed rhythm / phase misalignment / attractor-shift "
                 "in a gated setpoint, on the shared R19 substrate (same Kramers kernel as the oncology modules)",
        "status": "LIVE: 5 failures wired to the discriminants (3 clock-misalignment diseases + 2 mind seams: "
                  "circadian depression contributor + autism timing aggravator) + 4-lever chronotherapy management",
        "setpoint_shift_law": "DERIVED: clock gating is part of the restoring gain; losing it shrinks the effective "
                              "R19 barrier holding the setpoint -> drift -> Kramers crossing (setpoint_shift())",
        "failures": failures(),
        "management": management(),
        "grades": "cited anchor [L] / reproduced shape from live discriminants [V] / absolute incidence-rate [O] (obstacle stated)",
        "disease_wp_composition": "rare/monogenic CRSWD = cited parameter in; systemic trajectory = computed here",
        "mind_composition": "circadian SUPPLIES mind's LOCKED circadian depression contributor and a timing aggravator "
                            f"for mind's autism module; SIGN only, efficacy=0, felt/affect stays in mind ({MIND_DOI})",
    }


if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
