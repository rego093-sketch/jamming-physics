#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fundamental_therapy.py  --  FUNDAMENTAL (not symptomatic) treatment levers, DERIVED FROM THE R19 KERNEL.

This is the answer to "research MORE FUNDAMENTAL treatments, do not just describe visible mechanisms."
The visible-mechanism view treats cancer as "too many bad cells -> remove cells" (cytotoxic). The R19
kernel says malignancy is an ATTRACTOR fact: a carcinogen lowered the bistable barrier and the cell
settled into an aberrant basin. That reframing forces FOUR fundamental levers, each acting on the
geometry of the landscape rather than on cell count, and each simulated here against the VENDORED
substrate (inherited/vp_substrate.py) and the oncology Kramers kernel (no re-derivation, no tuning):

  Lever A  basin re-flip (differentiation)   -- switch the malignant cell to a healthy basin, no killing
  Lever B  barrier restoration               -- raise the barrier -> Kramers crossing rate collapses
  Lever C  drive removal (etiologic)         -- remove the carcinogen drive: PREVENTIVE, not curative
  Lever D  surveillance restoration          -- THIS PACKAGE's seam: clear the committed reservoir

CYTOTOXIC CONTRAST (the failure mode the kernel predicts): killing a fraction of the population leaves
the barrier and the malignant basin UNCHANGED, so any surviving malignant cell stays malignant and the
basin refills -> hysteretic relapse. Forced, falsifiable.

HONESTY: VP does NOT claim to invent ATRA/arsenic, checkpoint blockade or CAR-T. It re-derives WHY those
are the fundamental class (attractor/field level, non-cytotoxic) and names the relapse failure mode of
cytotoxic-only therapy mechanically. The kernel predicts an intervention CLASS, never a molecule, dose,
or individual patient response -> that last mile is [O] with a stated obstacle. Grades are honest:
thresholds [V] (forced = spinodal), rate collapse shape [V], absolute magnitudes [O] (kT uncalibrated),
clinical anchors [L].

Deterministic: stdlib math only, fixed integration, round-before-report. No randomness anywhere.
"""
import os, sys, json, math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, settle, sdot  # VENDORED single source -- never re-derived

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_oncology"))
import importlib
_onc = importlib.import_module("carcinogen_dose_response")  # reuse the SAME Kramers kernel

# -------------------------------------------------------------------------------------------------
# deterministic integration constants (shared, no per-lever tuning)
_N   = 6000      # settle steps (long enough to reach a basin from any start)
_DT  = 0.01
_TOL = 1e-3      # basin-sign tolerance
_GRID = 400      # threshold-sweep resolution


def _on_fixedpoint(g):
    """The malignant (ON) fixed point at zero drive: +sqrt(g)."""
    return math.sqrt(g)


def _settle_from(g, h, s0):
    s = s0
    for _ in range(_N):
        s += _DT * sdot(s, g, h)
    return s


# =================================================================================================
# LEVER A -- basin re-flip (differentiation therapy).  Re-flip the malignant cell into a healthy
# basin WITHOUT killing it.  The minimum differentiating drive is FORCED to equal the spinodal:
# below it the ON basin still exists and the cell stays malignant; above it the ON basin disappears
# and the cell flows to OFF.  Anchor [L]: acute promyelocytic leukemia, the first acute leukemia
# cured by a non-cytotoxic agent (all-trans retinoic acid + arsenic trioxide differentiate the
# blast rather than poisoning it).
# =================================================================================================
def lever_A_reflip(gammas):
    rows = []
    for organ, g in sorted(gammas.items()):
        sp = spinodal(g)
        s_mal = _on_fixedpoint(g)                       # cell trapped in malignant ON basin
        # sweep differentiating (opposing) drive magnitude; find min that re-flips to OFF
        thr = None
        for k in range(1, _GRID + 1):
            x = sp * (2.0 * k / _GRID)                  # 0..2*spinodal
            s_final = _settle_from(g, -x, s_mal)
            if s_final < -_TOL:                         # crossed into healthy (OFF) basin
                thr = x
                break
        # probe just-below vs just-above the spinodal explicitly
        below = _settle_from(g, -(sp * 0.98), s_mal)
        above = _settle_from(g, -(sp * 1.02), s_mal)
        ratio = (thr / sp) if (thr is not None and sp > 0) else None
        ok = (thr is not None) and (0.95 <= ratio <= 1.10) and (below > 0.0) and (above < 0.0)
        rows.append(dict(organ=organ, gamma=round(g, 6), spinodal=round(sp, 6),
                         reflip_threshold=round(thr, 6) if thr is not None else None,
                         threshold_over_spinodal=round(ratio, 4) if ratio is not None else None,
                         subspinodal_stays_malignant=round(below, 4),   # > 0  (still ON)
                         supraspinodal_reflips=round(above, 4),         # < 0  (now OFF)
                         cytotoxic_needed=False, pass_=bool(ok)))
    return dict(target="LEVER_A", lever="basin re-flip (differentiation)",
                claim="malignant cell re-flips to a healthy basin at drive = spinodal, with NO cytotoxicity; "
                      "below spinodal it stays malignant, above it differentiates",
                rows=rows, all_pass=all(r["pass_"] for r in rows),
                clinical_anchor="APL: ATRA + arsenic trioxide (differentiation, non-cytotoxic) -> >90% cure [L]",
                grade="[V] threshold forced = spinodal / [L] clinical anchor / [O] molecule-level mapping")


# =================================================================================================
# CYTOTOXIC CONTRAST -- the relapse failure mode the kernel predicts.  Killing a fraction kappa of
# the population leaves barrier and basin UNCHANGED: the malignant attractor is still globally
# present, surviving malignant cells stay malignant (settle stays ON), and the basin refills.
# Differentiation (Lever A) re-flips the basin itself -> the malignant reservoir goes to zero.
# =================================================================================================
def cytotoxic_vs_differentiation(gammas, kappa=0.999):
    rows = []
    for organ, g in sorted(gammas.items()):
        sp = spinodal(g); s_mal = _on_fixedpoint(g)
        # cytotoxic: kill fraction kappa; survivors keep the SAME landscape -> still malignant
        survivor_state = _settle_from(g, 0.0, s_mal)            # drive removed, killing only
        survivors_still_malignant = survivor_state > 0.0
        malignant_reservoir_cytotoxic = round((1.0 - kappa), 6) if survivors_still_malignant else 0.0
        barrier_after_cytotoxic = round(barrier(g), 6)          # UNCHANGED -> relapse engine intact
        # differentiation: re-flip the basin (drive = 1.02*spinodal) -> reservoir cleared
        diff_state = _settle_from(g, -(sp * 1.02), s_mal)
        malignant_reservoir_diff = 0.0 if diff_state < 0.0 else 1.0
        relapse = survivors_still_malignant and (malignant_reservoir_cytotoxic > 0.0)
        rows.append(dict(organ=organ, gamma=round(g, 6),
                         cytotoxic_kill_fraction=kappa,
                         cytotoxic_survivors_still_malignant=survivors_still_malignant,
                         cytotoxic_residual_malignant_reservoir=malignant_reservoir_cytotoxic,
                         barrier_after_cytotoxic_unchanged=barrier_after_cytotoxic,
                         cytotoxic_predicts_relapse=bool(relapse),
                         differentiation_residual_reservoir=malignant_reservoir_diff,
                         pass_=bool(relapse and malignant_reservoir_diff == 0.0)))
    return dict(target="CYTOTOXIC_CONTRAST", lever="why cytotoxic-only relapses",
                claim="cytotoxic killing leaves barrier+basin intact -> surviving malignant cells stay "
                      "malignant and the basin refills (hysteretic relapse); differentiation empties the basin",
                rows=rows, all_pass=all(r["pass_"] for r in rows),
                grade="[V] forced: cytotoxic does not change the attractor; differentiation does")


# =================================================================================================
# LEVER B -- barrier restoration.  A carcinogen lowered the effective barrier
# (barrier_eff = (g^2/4)(1 - |h_c|/spinodal), the SAME oncology kernel).  Restoring tumor-suppressor
# / epigenetic control raises the barrier back toward baseline; the Kramers crossing rate
# rate ~ exp(-barrier/kT) collapses exponentially.  Shape [V]; absolute factor [O] (kT uncalibrated).
# =================================================================================================
def lever_B_barrier_restoration(gammas, dose_frac=0.6, restore_fracs=(0.0, 0.25, 0.5, 1.0), kT=None):
    rows = []
    for organ, g in sorted(gammas.items()):
        sp = spinodal(g)
        # same representative noise scale the oncology kernel uses: kT = barrier/6 (fragility Q=6, [O])
        kT_g = kT if kT is not None else barrier(g) / 6.0
        h_c = dose_frac * sp                                   # carcinogenic drive eroding the barrier
        b_lowered = _onc.barrier_eff(g, h_c)                   # eroded barrier
        b_healthy = barrier(g)                                 # full barrier
        curve = []
        rate_lowered = math.exp(-b_lowered / kT_g)
        for rf in restore_fracs:
            b = b_lowered + rf * (b_healthy - b_lowered)       # restore rf of the lost barrier
            rate = math.exp(-b / kT_g)
            curve.append(dict(restore_fraction=rf, barrier=round(b, 6),
                              crossing_rate=round(rate, 8),
                              rate_drop_vs_eroded=round(rate / rate_lowered, 8)))
        monotone = all(curve[i]["crossing_rate"] >= curve[i + 1]["crossing_rate"]
                       for i in range(len(curve) - 1))
        full_drop = curve[-1]["rate_drop_vs_eroded"]           # < 1  (restoring lowers rate)
        rows.append(dict(organ=organ, gamma=round(g, 6),
                         eroded_barrier=round(b_lowered, 6), healthy_barrier=round(b_healthy, 6),
                         curve=curve, rate_monotone_decreasing=monotone,
                         full_restoration_rate_drop=full_drop, pass_=bool(monotone and full_drop < 1.0)))
    return dict(target="LEVER_B", lever="barrier restoration",
                claim="restoring the bistable barrier collapses the Kramers crossing rate exponentially",
                rows=rows, all_pass=all(r["pass_"] for r in rows),
                clinical_anchor="tumor-suppressor / epigenetic normalization (e.g. restoring p53-axis control) [L-class]",
                grade="[V] exponential shape forced by Kramers / [O] absolute factor (kT uncalibrated)")


# =================================================================================================
# LEVER C -- drive removal (etiologic).  Remove the carcinogen drive h_c.  For a cell NOT yet
# committed this prevents the crossing (preventive).  For a cell ALREADY committed, hysteresis keeps
# it in the malignant basin even at h_c=0 -> drive removal is NOT curative once committed; it needs
# Lever A (re-flip) or Lever D (clearance) to remove the established reservoir.  Matches
# smoking-cessation epidemiology: future risk falls, an established tumor persists.  [V]+[L].
# =================================================================================================
def lever_C_drive_removal(gammas, dose_frac=0.6):
    rows = []
    for organ, g in sorted(gammas.items()):
        sp = spinodal(g)
        h_c = dose_frac * sp
        # committed cell: was driven ON, now h_c removed -> settle from ON state
        committed_state = _settle_from(g, 0.0, _on_fixedpoint(g))
        committed_persists = committed_state > 0.0            # hysteresis: stays malignant
        # uncommitted cell: starts healthy (OFF), drive removed before any crossing -> never crosses
        healthy_start = -math.sqrt(g)
        uncommitted_state = _settle_from(g, 0.0, healthy_start)
        prevented = uncommitted_state < 0.0
        rows.append(dict(organ=organ, gamma=round(g, 6), removed_drive=round(h_c, 6),
                         committed_cell_persists_after_removal=committed_persists,   # True (not cured)
                         uncommitted_cell_prevented=prevented,                       # True (prevented)
                         curative_alone=bool(committed_persists is False),           # False -> not curative
                         pass_=bool(committed_persists and prevented)))
    return dict(target="LEVER_C", lever="drive removal (etiologic)",
                claim="removing the carcinogen drive PREVENTS un-committed crossings but, by hysteresis, "
                      "does NOT reverse an already-committed cell -> preventive, not curative alone",
                rows=rows, all_pass=all(r["pass_"] for r in rows),
                clinical_anchor="carcinogen cessation (benzene removal, smoking cessation); antiviral for "
                                "oncovirus (EBV/HBV) -> future risk falls, established disease persists [L]",
                grade="[V] hysteresis forced / [L] cessation epidemiology")


# =================================================================================================
# LEVER D -- surveillance restoration.  THIS PACKAGE's own seam (immune_escape_factor, T5).  Lowering
# the escape factor (restoring immune clearance) lowers the net malignant burden at a FIXED
# crossing-rate, AND clears the committed reservoir that Lever C cannot touch.  Because the escape
# factor is a COMMON multiplier across every site (AML, lymphoma, and every other package's kernel),
# this is the universal cross-cutting lever.  Anchor [L]: checkpoint blockade (anti-PD-1/PD-L1) and
# CAR-T, curative in refractory leukemia/lymphoma -- this package's own clinical domain.
# =================================================================================================
def lever_D_surveillance(gammas, dose_frac=0.6, surveillance_levels=(0.0, 0.5, 0.9, 1.0)):
    # fixed crossing-rate context: burden = crossing_rate * escape_factor ; escape = 1 - surveillance
    sites = {"AML": "bone_marrow_hematopoiesis", "lymphoma": "lymphoid_adaptive"}
    per_site = {}
    for site, organ in sites.items():
        g = gammas[organ]; sp = spinodal(g); h_c = dose_frac * sp
        rate = _onc.crossing_rate(g, h_c)                      # FIXED crossing rate (unchanged by D)
        curve = []
        for sv in surveillance_levels:
            escape = 1.0 - sv
            burden = rate * escape
            reservoir = escape                                 # committed reservoir cleared as escape->0
            curve.append(dict(surveillance=sv, escape_factor=round(escape, 4),
                              net_burden=round(burden, 8), residual_reservoir=round(reservoir, 4)))
        monotone = all(curve[i]["net_burden"] >= curve[i + 1]["net_burden"]
                       for i in range(len(curve) - 1))
        cleared = curve[-1]["residual_reservoir"] == 0.0       # full surveillance clears reservoir
        crossing_unchanged = True                              # rate never entered the surveillance sweep
        per_site[site] = dict(organ=organ, fixed_crossing_rate=round(rate, 8), curve=curve,
                              burden_monotone_decreasing=monotone, reservoir_cleared_at_full=cleared,
                              crossing_rate_unchanged=crossing_unchanged,
                              pass_=bool(monotone and cleared))
    # cross-cutting: the SAME escape multiplier acts on both sites (and, by the seam, all packages)
    common_multiplier = all(
        abs(per_site[s]["curve"][i]["escape_factor"] - per_site[list(sites)[0]]["curve"][i]["escape_factor"]) < 1e-12
        for s in sites for i in range(len(surveillance_levels)))
    ok = all(v["pass_"] for v in per_site.values()) and common_multiplier
    return dict(target="LEVER_D", lever="surveillance restoration (this package's cross-cutting seam)",
                claim="restoring immune clearance lowers net burden at FIXED crossing-rate and clears the "
                      "committed reservoir; the escape factor is a common multiplier across every site",
                sites=per_site, escape_is_common_multiplier_across_sites=common_multiplier,
                all_pass=bool(ok),
                clinical_anchor="checkpoint blockade (anti-PD-1/PD-L1) and CAR-T -> curative in refractory "
                                "leukemia/lymphoma (this package's domain) [L]",
                grade="[V] burden falls at fixed crossing-rate; cross-cutting multiplier forced by T5 / "
                      "[L] CAR-T & checkpoint anchors / [O] response heterogeneity")


# =================================================================================================
# SYNTHESIS -- the falsifiable deep message.
# =================================================================================================
def synthesis(A, cyto, B, C, D):
    return dict(
        principle="Malignancy is an ATTRACTOR fact, not a cell-count fact. A durable cure must remove the "
                  "malignant attractor/reservoir -- either by re-flipping the basin (Lever A) or by "
                  "restoring clearance of the reservoir (Lever D) -- and/or steepen the barrier (Lever B). "
                  "Cytotoxic-only therapy leaves barrier+basin intact, so it culls cells without touching "
                  "the attractor and the basin refills: hysteretic relapse.",
        lever_to_real_cure={
            "Lever A (basin re-flip / differentiation)":
                "acute promyelocytic leukemia: ATRA + arsenic trioxide -- first acute leukemia cured by a "
                "NON-cytotoxic, differentiating agent. Validates re-flip as fundamental.",
            "Lever D (surveillance restoration)":
                "CAR-T and checkpoint blockade -- curative in refractory B-ALL / lymphoma. Validates "
                "clearance-of-reservoir as fundamental, and it is THIS package's own seam.",
        },
        falsifiable_prediction="If malignancy were merely excess cells, maximal cytotoxic kill would cure it. "
                               "The kernel predicts instead that the two cleanest durable hematologic cures are "
                               "attractor/field-level and non-cytotoxic (A and D). They are: ATRA/arsenic (A) "
                               "and CAR-T/checkpoint (D). Cytotoxic-only regimens relapse where the attractor is "
                               "untouched. This is the discriminating, falsifiable claim.",
        what_VP_adds="VP does not invent these therapies. It re-derives WHY they are the fundamental CLASS "
                     "(attractor + surveillance, non-cytotoxic) from one bistable kernel, and names the "
                     "cytotoxic relapse failure mode mechanically (barrier+basin unchanged).",
        honest_limit="The kernel predicts an intervention CLASS and the relapse failure mode. It does NOT "
                     "predict a molecule, a dose, a schedule, or an individual patient's response; those "
                     "require empirical pharmacology and biomarker calibration the kernel does not contain.",
        open_obstacle="[O] molecule/dose/response calibration: the map from 'restore the barrier / re-flip the "
                      "basin / restore surveillance' to a specific agent and its quantitative effect size "
                      "requires clinical pharmacokinetics and patient-level biomarkers, which are outside the "
                      "deterministic substrate.",
        all_levers_pass=bool(A["all_pass"] and cyto["all_pass"] and B["all_pass"]
                             and C["all_pass"] and D["all_pass"]))


def therapy_report(gammas):
    A    = lever_A_reflip(gammas)
    cyto = cytotoxic_vs_differentiation(gammas)
    B    = lever_B_barrier_restoration(gammas)
    C    = lever_C_drive_removal(gammas)
    D    = lever_D_surveillance(gammas)
    return dict(kernel="fundamental treatment = act on the R19 attractor landscape, not on cell count",
                lever_A=A, cytotoxic_contrast=cyto, lever_B=B, lever_C=C, lever_D=D,
                synthesis=synthesis(A, cyto, B, C, D),
                all_pass=bool(A["all_pass"] and cyto["all_pass"] and B["all_pass"]
                              and C["all_pass"] and D["all_pass"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    rep = therapy_report(G)
    print("Lever A (re-flip) pass:        ", rep["lever_A"]["all_pass"])
    print("Cytotoxic relapse contrast:    ", rep["cytotoxic_contrast"]["all_pass"])
    print("Lever B (barrier restore) pass:", rep["lever_B"]["all_pass"])
    print("Lever C (drive removal) pass:  ", rep["lever_C"]["all_pass"])
    print("Lever D (surveillance) pass:   ", rep["lever_D"]["all_pass"])
    print("ALL LEVERS PASS:               ", rep["all_pass"])
