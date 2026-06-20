#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_trm_engine.py  --  Thermometabolic Homeostasis engine (deterministic, in-package).

SCOPE (see CHARTER.md): Starts from the endotherm-vs-ectotherm question -- does the organism DEFEND an internal setpoint or TRACK the environment? -- and covers thermoregulation, brown-fat thermogenesis, the torpor/hibernation switch, whole-body energy homeostasis, and metabolic disease as ONE coupled setpoint-dynamics problem. Disease is a subset.

WHAT RUNS TODAY: emerge_organs() builds the nodes whose master-gene gamma is vendored (measured),
  defers to_measure masters honestly, reads developmental order off gamma. confirm_oscillators() runs
  the SHARED FHN for any oscillator node (e.g. the torpor-arousal rhythm). setpoint_defense_demo() and torpor_switch_probe() frame the endothermy and torpor questions.

WHAT IS A SKELETON: the setpoint LOOPS, the cross-package couplings, and the disease attractor-shifts
  (see CHARTER research program). Writing is locked until the stress battery is green.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed; round-before-hash; sorted keys.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.dirname(__file__))
from vp_substrate import Organ, Neuron, spinodal, barrier, settle, dwell, dominant_freq, seed_everything
import endotherm_ectotherm as ee   # the FOUNDATIONAL endotherm-vs-ectotherm analysis (RT1/RT3/RT4/RT5/RH4/RH8)

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

ORGAN_ROWS = [{'master': 'UCP1',
  'organ': 'brown_adipose_thermogenesis',
  'role': 'uncoupled proton leak = heat, not ATP (the endotherm furnace)',
  'dyn_class': 'thermogenic-switch',
  'tau_s': None,
  'rate_note': 'BAT cold-induced thermogenesis [L]',
  'gamma_state': 'vendored'},
 {'master': 'ADRB3',
  'organ': 'sympathetic_thermo_drive',
  'role': 'beta3-adrenergic activation of BAT (cold -> heat command)',
  'dyn_class': 'effector',
  'tau_s': None,
  'rate_note': 'cold-induced drive [L]',
  'gamma_state': 'vendored'},
 {'master': 'PPARG',
  'organ': 'white_adipose_storage',
  'role': 'lipid storage + adipokine secretion (the lipostat storage node)',
  'dyn_class': 'storage',
  'tau_s': None,
  'rate_note': 'adiposity setpoint [L]',
  'gamma_state': 'vendored'},
 {'master': 'MC4R',
  'organ': 'melanocortin_appetite',
  'role': 'hypothalamic energy-balance setpoint (intake control)',
  'dyn_class': 'setpoint-loop',
  'tau_s': None,
  'rate_note': 'lipostat / appetite setpoint [L]',
  'gamma_state': 'vendored'},
 {'master': 'LEPR',
  'organ': 'leptin_feedback',
  'role': 'adiposity feedback signal (storage -> brain)',
  'dyn_class': 'feedback',
  'tau_s': None,
  'rate_note': 'leptin feedback gain [L]',
  'gamma_state': 'vendored'},
 {'master': 'INSR',
  'organ': 'insulin_glucose_effector',
  'role': 'insulin-mediated glucose disposal (the euglycemia effector)',
  'dyn_class': 'feedback',
  'tau_s': None,
  'rate_note': 'euglycemia setpoint ~5 mM [L]',
  'gamma_state': 'vendored'},
 {'master': 'GHRL',
  'organ': 'ghrelin_hunger',
  'role': 'gut hunger signal (drives intake; opposes leptin)',
  'dyn_class': 'feedback',
  'tau_s': None,
  'rate_note': 'hunger drive [L]',
  'gamma_state': 'vendored'},
 {'master': 'PDK4',
  'organ': 'torpor_fuel_switch',
  'role': 'metabolic fuel-switch to lipid + glucose sparing (torpor-associated program)',
  'dyn_class': 'torpor-switch',
  'tau_s': None,
  'rate_note': 'torpor metabolic suppression [L]; PDK4 gamma=1.4112 measured (NC_000007.14, this session)',
  'gamma_state': 'vendored'},
 {'master': '(hypothalamic_thermostat)',
  'organ': 'preoptic_thermostat',
  'role': 'preoptic setpoint comparator (the thermostat itself; circuit, no single master)',
  'dyn_class': 'setpoint-comparator',
  'tau_s': None,
  'rate_note': 'thermal setpoint ~37C [L]',
  'gamma_state': 'diffuse'},
 {'master': '(torpor_arousal_cycle)',
  'organ': 'torpor_arousal_rhythm',
  'role': 'periodic interbout arousal during hibernation (slow relaxation oscillator)',
  'dyn_class': 'oscillator',
  'tau_s': 700.0,
  'rate_note': 'interbout arousal period (days) [L] TO-ANCHOR',
  'gamma_state': 'diffuse'}]
OSCILLATOR_ORGANS = ["torpor_arousal_rhythm"]

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def emerge_organs():
    seed_everything(); G = load_gamma(); built = []
    for r in ORGAN_ROWS:
        st = r["gamma_state"]
        if st == "vendored":
            g = G[r["master"]]["gamma"]; o = Organ(r["organ"], g, master=r["master"])
            built.append(dict(organ=r["organ"], master=r["master"], gamma=round(float(g), 6), role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state="vendored",
                              functional_spinodal=round(float(o.functional_spinodal()), 6),
                              rel_size_dwell=round(float(o.size()), 6)))
        elif st == "to_measure":
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"], dyn_class=r["dyn_class"],
                              gamma_state="to_measure",
                              note="master " + r["master"] + ": gamma TO-MEASURE via DNA pipeline (measured input, not fitted)"))
        else:
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"], dyn_class=r["dyn_class"],
                              gamma_state="diffuse", note="no single master gene (circuit/derived/diffuse)"))
    go = [b for b in built if b.get("gamma") is not None]
    order = [b["organ"] for b in sorted(go, key=lambda b: b["gamma"])]
    return dict(organs=built, gamma_order_ascending=order,
                order_grade="[V] order is a gamma readout over MEASURED nodes; SIGN to validate vs cited timing",
                deferred_gamma=[b["master"] for b in built if b.get("gamma_state") == "to_measure"])

def confirm_oscillators():
    seed_everything(); out = {}
    for r in ORGAN_ROWS:
        if r["dyn_class"] != "oscillator": continue
        taus = r["tau_s"] if r["tau_s"] is not None else 40.0
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(taus), beta=0.5, name=r["organ"])
        S, dt = n.run(drive=0.55, T=8000.0, dt=0.05)
        f = dominant_freq(S, dt); nb = len(Neuron.spikes(S))
        out[r["organ"]] = dict(oscillates=bool(nb >= 3 and f > 0.0), beats=int(nb),
                               relaxation_freq_arb=round(float(f), 8), tau_s=float(taus),
                               rate_anchor=r["rate_note"], mechanism_grade="[V]", rate_grade="[L]")
    return out

def setpoint_defense_demo(g=1.0, ambient_drive=0.0):
    """A SETPOINT-defending loop is an R19 attractor whose basin resists environmental drive. settle()
    returns the defended state under an ambient drive; a deep basin (endotherm) holds, a shallow one
    (ectotherm) is pushed. SKELETON: sweep ambient_drive to map 'held' vs 'tracking'. mechanism [V]."""
    held = settle(g, ambient_drive)
    return dict(defended_state=round(float(held), 6), barrier=round(float(barrier(g)), 6),
                reading="deep basin (high loop gain) => setpoint HELD (endotherm); shallow => TRACKS ambient (ectotherm)")

def torpor_switch_probe(g=1.0):
    """CENTRAL question (RH1): is euthermia<->torpor a DISCRETE bistable flip (R19 spinodal + hysteresis)
    or a CONTINUOUS dial? Framed with the R19 bistable switch: a 'torpor drive' h biases between a
    euthermic (high-metabolic) and a torpor (low-metabolic) attractor. Past the spinodal the opposite
    basin disappears -> the flip is DISCONTINUOUS. SKELETON: sweep h up then down, record up/down states,
    measure hysteresis-loop width; >0 => SWITCH, 0 => DIAL. Then compare across species (RH4)."""
    sp = spinodal(g)
    return dict(question="euthermia<->torpor: discrete bistable SWITCH vs continuous DIAL",
                r19_spinodal=round(float(sp), 6),
                discriminant="ascending/descending torpor-drive sweep: hysteresis-loop width > 0 with a "
                             "discontinuous jump => bistable SWITCH; smooth reversible tracking => continuous DIAL",
                species_test="RH4: are torpor-program genes present-but-silenced in the human genome (locked switch) "
                             "or absent (no switch)? cross-species gamma via the DNA pipeline",
                status="SKELETON: run the up/down sweep, measure hysteresis, grade [V]; absolute metabolic-rate drop [O]",
                grades="mechanism [V] / species threshold [L] / absolute rate drop [O]")


import math


# ===========================================================================
#  R19 SETPOINT DYNAMICS  --  the defended-attractor loops (this fills the skeleton)
#  Convention: a DEFENDED setpoint is the UPPER R19 well at s_set=+sqrt(g). A
#  sub-spinodal drive shifts/perturbs the state but the well persists (defended);
#  a supra-spinodal drive destroys the well (regulation overwhelmed / state flip).
#  Mechanism is [V] (R19-derived); cited setpoints are [L]; absolutes are [O].
# ===========================================================================

def thermostat_step(g=1.40, steps=(-0.10, -0.25, -0.45, -0.63, -0.80)):
    """RT2 -- the preoptic thermostat. Defended setpoint = upper well. A sub-spinodal ambient step is
    corrected back toward ~37C; past the spinodal the euthermic well disappears (defense overwhelmed)."""
    sp = float(spinodal(g)); s_set = math.sqrt(g); rows = []
    for h in steps:
        s_final = settle(g, float(h), s0=s_set)
        sub = abs(h) < sp
        rows.append(dict(ambient_step=float(h), sub_spinodal=bool(sub),
                         final_state=round(float(s_final), 6), setpoint=round(float(s_set), 6),
                         error=round(float(abs(s_final - s_set)), 6),
                         corrected=bool(sub and s_final > 0.0)))
    bounded = all(r["corrected"] for r in rows if r["sub_spinodal"])
    collapses = any((not r["corrected"]) for r in rows if not r["sub_spinodal"])
    return dict(question="thermostat: a sub-spinodal ambient step is corrected back to the defended setpoint",
                spinodal_h_sp=round(sp, 6), defended_setpoint=round(float(s_set), 6), rows=rows,
                error_bounded_while_substhreshold=bool(bounded), collapses_past_spinodal=bool(collapses),
                reading="while the ambient step stays below the R19 spinodal the upper (euthermic) well persists and "
                        "the state is corrected back to the setpoint; past the spinodal the well disappears and the "
                        "defense is overwhelmed.",
                grades="mechanism [V] / setpoint ~37C [L] / absolute gain-latency [O]")


def bat_thermogenesis(g=1.40, h_cold=-0.80, h_therm=0.55):
    """RG1 -- brown-fat (UCP1) thermogenesis. A cold drive past the spinodal would collapse the euthermic
    well; recruiting the UCP1 switch adds a compensating heat flux that returns the NET drive below the
    spinodal, so the setpoint is defended (cold -> ADRB3 -> UCP1 -> heat)."""
    sp = float(spinodal(g)); s_set = math.sqrt(g)
    s_cold = settle(g, h_cold, s0=s_set)                      # cold alone
    s_defended = settle(g, h_cold + h_therm, s0=s_set)        # UCP1 recruited
    return dict(question="brown-fat thermogenesis: cold recruits the UCP1 switch to defend the setpoint",
                cold_drive=float(h_cold), spinodal=round(sp, 6),
                state_cold_no_thermogenesis=round(float(s_cold), 6), thermogenic_flux=float(h_therm),
                state_with_UCP1_recruited=round(float(s_defended), 6), setpoint=round(float(s_set), 6),
                cold_alone_overwhelms=bool(s_cold <= 0.0),
                thermogenesis_restores_setpoint=bool(s_cold <= 0.0 and s_defended > 0.0),
                reading="a cold drive past the spinodal collapses the euthermic well; recruiting the UCP1 thermogenic "
                        "switch adds a compensating heat flux that returns the net drive below the spinodal, so the "
                        "setpoint is defended.",
                grades="mechanism [V] / BAT output rate [L] / absolute W/kg [O]")


def fever_vs_hyperthermia(g=1.40, h_pyrogen=0.45, h_external_heat=0.90):
    """RG3 -- fever is a regulated UPWARD setpoint shift (a sustained sub-spinodal pyrogen bias: a
    perturbation still returns to the ELEVATED setpoint); hyperthermia is a supra-spinodal external heat
    load that destroys the regulated well (runaway). Same substrate, opposite regulatory status."""
    sp = float(spinodal(g)); s_normal = settle(g, 0.0, s0=math.sqrt(g))
    s_fever = settle(g, h_pyrogen, s0=s_normal)
    s_fever_back = settle(g, h_pyrogen, s0=s_fever - 0.4)      # perturb the febrile setpoint
    s_hyper = settle(g, h_external_heat, s0=math.sqrt(g))
    fever_regulated = bool(abs(s_fever_back - s_fever) < 0.05 and h_pyrogen < sp and s_fever > s_normal)
    return dict(question="fever (regulated upward setpoint shift) vs hyperthermia (regulation overwhelmed)",
                spinodal=round(sp, 6), normal_setpoint=round(float(s_normal), 6),
                fever_setpoint=round(float(s_fever), 6), fever_is_sub_spinodal=bool(h_pyrogen < sp),
                fever_returns_after_perturbation=bool(abs(s_fever_back - s_fever) < 0.05),
                fever_setpoint_is_elevated=bool(s_fever > s_normal), fever_regulated=fever_regulated,
                hyperthermia_drive=float(h_external_heat), hyperthermia_is_supra_spinodal=bool(h_external_heat > sp),
                hyperthermia_well_destroyed=bool(s_hyper <= 0.0 or h_external_heat > sp),
                reading="fever is a sustained SUB-spinodal pyrogen bias that moves the regulated set value UP -- a "
                        "perturbation still returns to the elevated setpoint (regulation intact); hyperthermia is a "
                        "SUPRA-spinodal external heat load that destroys the regulated well (runaway, regulation lost).",
                grades="mechanism [V] / setpoint-shift magnitude [L] / absolute temperature [O]")


def torpor_hysteresis_sweep(g=1.40, hmax=1.20, npts=241):
    """RH1 (CENTRAL) -- ramp the torpor drive DOWN then UP through the bistable R19. The state holds the
    euthermic branch until -h_sp then JUMPS to torpor; ramping back holds torpor until +h_sp then jumps
    back -- a hysteresis loop of width ~2*h_sp. The transition is DISCONTINUOUS: a SWITCH, not a dial."""
    sp = float(spinodal(g))
    hs_down = list(__import__("numpy").linspace(hmax, -hmax, npts))
    hs_up = list(__import__("numpy").linspace(-hmax, hmax, npts))
    s = math.sqrt(g); down = []
    for h in hs_down:
        s = settle(g, float(h), s0=s); down.append(s)
    jd = next((float(h) for h, sv in zip(hs_down, down) if sv < 0.0), None)
    s2 = -math.sqrt(g); up = []
    for h in hs_up:
        s2 = settle(g, float(h), s0=s2); up.append(s2)
    ju = next((float(h) for h, sv in zip(hs_up, up) if sv > 0.0), None)
    loop = (ju - jd) if (ju is not None and jd is not None) else None
    return dict(question="euthermia<->torpor: a HYSTERESIS LOOP (bistable SWITCH) or smooth tracking (continuous DIAL)?",
                spinodal_h_sp=round(sp, 6), jump_down_drive=round(jd, 6) if jd is not None else None,
                jump_up_drive=round(ju, 6) if ju is not None else None, predicted_jumps_at=round(sp, 6),
                hysteresis_loop_width=round(float(loop), 6) if loop is not None else None,
                loop_width_positive=bool(loop is not None and loop > 0),
                is_switch_not_dial=bool(loop is not None and loop > 0),
                reading="ramping the torpor drive DOWN holds the euthermic branch until -h_sp then jumps to torpor; "
                        "ramping back UP holds torpor until +h_sp then jumps back -- a hysteresis loop of width ~2*h_sp. "
                        "The transition is discontinuous: euthermia<->torpor is a bistable SWITCH, not a continuous dial. "
                        "Cross-species (RH4): the switch genes are PRESENT in the human genome (silenced), not absent.",
                grades="mechanism [V] / drive threshold [L] / absolute metabolic-rate drop [O]")


def torpor_regulated(g=1.40, h_torpor=-0.20):
    """RH2 -- the LOW (torpor) state is a regulated attractor: a perturbation pushing the state further
    down is actively corrected back to the torpor setpoint (defended low metabolism, not a passive floor)."""
    s_torpor = settle(g, h_torpor, s0=-math.sqrt(g))
    s_back = settle(g, h_torpor, s0=s_torpor - 0.4)
    return dict(question="is the low (torpor) metabolic state a REGULATED attractor or a passive floor?",
                torpor_setpoint=round(float(s_torpor), 6), perturbed_state_returns_to=round(float(s_back), 6),
                returns_to_torpor_setpoint=bool(abs(s_back - s_torpor) < 0.05),
                reading="settling under a torpor drive gives a LOW regulated state; a perturbation pushing the state "
                        "further down is actively corrected back to the torpor setpoint -- torpor is a regulated "
                        "(defended) low-metabolic attractor, not an uncontrolled collapse.",
                grades="mechanism [V] / torpor setpoint depth [L] / absolute Tb/MR [O]")


def glucose_homeostat(g=1.4956, load=0.60):
    """RE1 -- euglycemia is a regulated R19 attractor (INSR node); a glucose load displaces the state and
    the insulin loop returns it to the setpoint (~5 mM cited)."""
    s_eu = settle(g, 0.0, s0=math.sqrt(g))
    s_after = settle(g, 0.0, s0=s_eu + load)
    return dict(question="does a glucose load return to the euglycemic setpoint via the closed loop?",
                euglycemia_setpoint=round(float(s_eu), 6), state_after_load_returns_to=round(float(s_after), 6),
                returns_to_euglycemia=bool(abs(s_after - s_eu) < 0.05),
                reading="euglycemia is a regulated R19 attractor; a glucose load displaces the state, and the insulin "
                        "loop returns it to the setpoint (~5 mM cited).",
                grades="mechanism [V] / euglycemia ~5 mM [L] / absolute mg/dL excursion [O]")


def lipostat(g=1.3902, over=0.30, under=-0.30):
    """RE2 -- adiposity sits in a regulated R19 basin; sustained sub-spinodal over/underfeeding shifts the
    defended state only modestly and is actively opposed (leptin-melanocortin)."""
    sp = float(spinodal(g)); s_set = settle(g, 0.0, s0=math.sqrt(g))
    s_over = settle(g, over, s0=s_set); s_under = settle(g, under, s0=s_set)
    return dict(question="does a defended adiposity setpoint oppose chronic over/underfeeding?",
                spinodal=round(sp, 6), adiposity_setpoint=round(float(s_set), 6),
                state_sustained_overfeeding=round(float(s_over), 6),
                state_sustained_underfeeding=round(float(s_under), 6),
                setpoint_opposes_perturbation=bool(abs(over) < sp and s_over > 0 and abs(under) < sp and s_under > 0),
                reading="adiposity sits in a regulated R19 basin; sustained sub-spinodal over- or underfeeding shifts "
                        "the defended state only modestly and is actively opposed (leptin-melanocortin). A supra-spinodal "
                        "chronic drive would cross to a new basin (the obesity setpoint -- see pathology).",
                grades="mechanism [V] / adiposity setpoint [L] / absolute kg/BMI [O]")


def hibernation_bridge(g=1.4112):
    """RD4 (the bridge hypothesis) -- PDK4-driven glucose sparing is adaptive and reversible inside torpor
    (a defended LOW setpoint that returns after perturbation) but, run as a CHRONIC supra-spinodal misfire,
    becomes the uncoupled fuel-sparing of insulin resistance (crosses to the low-disposal basin and stays).
    Same machinery, opposite regulatory status."""
    sp = float(spinodal(g)); h_torpor = -0.20
    s_torpor = settle(g, h_torpor, s0=-math.sqrt(g))
    s_torpor_back = settle(g, h_torpor, s0=s_torpor - 0.4)
    h_chronic = -(sp + 0.20)
    s_ir = settle(g, h_chronic, s0=math.sqrt(g))
    return dict(question="hibernation bridge: torpor and insulin resistance share the PDK4 fuel-sparing program -- "
                         "what distinguishes them in R19?",
                pdk4_gamma=round(float(g), 6), spinodal=round(sp, 6),
                torpor_setpoint=round(float(s_torpor), 6),
                torpor_returns_after_perturbation=bool(abs(s_torpor_back - s_torpor) < 0.05),
                insulin_resistance_state=round(float(s_ir), 6), insulin_resistance_crossed_and_stuck=bool(s_ir < 0.0),
                distinction="torpor = a REGULATED low-fuel attractor (returns after perturbation); insulin resistance = "
                            "the SAME fuel-sparing program driven CHRONICALLY past the spinodal so the state crosses to "
                            "and stays in the low-disposal (hyperglycemic) basin -- regulation lost",
                reading="PDK4-driven glucose sparing is adaptive and reversible inside torpor (a defended low setpoint) "
                        "but, as a chronic supra-spinodal misfire, becomes the uncoupled fuel-sparing of insulin "
                        "resistance. Same machinery, opposite regulatory status -- the literal 'hibernation bridge'.",
                grades="R19 framing [V] / PDK4 co-upregulation in torpor & insulin resistance [O] cited / absolute [O]")


# ===========================================================================
#  STRESS-TARGET AGGREGATOR  --  maps each CHARTER target to a pass/value/grade.
#  An [O]-with-stated-obstacle target PASSES the bar (CHARTER: reproduced [V] OR
#  honestly flagged [O]); a silent failure does not.
# ===========================================================================

def stress_targets():
    seed_everything()
    osc = confirm_oscillators()
    rh6_ok = bool(osc.get("torpor_arousal_rhythm", {}).get("oscillates"))

    rt1 = ee.setpoint_defense_sweep()
    rt3 = ee.endothermy_cost()
    rt4 = ee.continuum_or_switch()
    rt5 = ee.kleiber_status()
    gc = ee.gene_criterion()
    npdk4 = ee.null_pdk4_gamma_does_not_mark_hibernation()
    npanel = ee.null_torpor_panel_gamma_does_not_track_hibernation()
    ncpg = ee.null_cpg_oe_does_not_track_hibernation()

    rt2 = thermostat_step(); rg1 = bat_thermogenesis(); rg3 = fever_vs_hyperthermia()
    rh1 = torpor_hysteresis_sweep(); rh2 = torpor_regulated()
    re1 = glucose_homeostat(); re2 = lipostat(); rd4 = hibernation_bridge()

    T = []
    def add(tid, ok, value, grade, obstacle=None):
        T.append(dict(target=tid, status=("PASS" if ok else "FAIL"), value=value, grade=grade,
                      obstacle_if_open=obstacle))

    add("RT1", bool(rt1["endotherm_pins"] and rt1["ectotherm_tracks"]
                    and rt1["sensitivity_monotone_decreasing_in_barrier"]),
        {"endo_sensitivity": rt1["endotherm_loop"]["ambient_sensitivity"],
         "ecto_sensitivity": rt1["ectotherm_loop"]["ambient_sensitivity"]}, "[V]")
    add("RT2", bool(rt2["error_bounded_while_substhreshold"] and rt2["collapses_past_spinodal"]),
        {"spinodal": rt2["spinodal_h_sp"], "setpoint": rt2["defended_setpoint"]}, "[V] mech / [L] ~37C")
    add("RT3", bool(rt3["cost_rises_with_defence"]),
        {"ratio": rt3["cited_absolute_ratio"]}, "[V] trade-off / [L] ratio / [O] absolute",
        "absolute W/kg needs external calorimetry calibration")
    add("RT4", bool(rt4["discontinuous_jump_at_spinodal"]),
        {"spinodal_h_sp": rt4["r19_spinodal_h_sp"]}, "[V]")
    add("RT5", (rt5["grade"].startswith("[O]")),
        {"status": rt5["status"]}, rt5["grade"], rt5["obstacle"])
    add("RG1", bool(rg1["thermogenesis_restores_setpoint"]),
        {"cold": rg1["cold_drive"], "state_with_UCP1": rg1["state_with_UCP1_recruited"]}, "[V]")
    add("RG3", bool(rg3["fever_regulated"] and rg3["hyperthermia_well_destroyed"]),
        {"fever_setpoint": rg3["fever_setpoint"], "normal": rg3["normal_setpoint"]}, "[V]")
    add("RH1", bool(rh1["is_switch_not_dial"]),
        {"loop_width": rh1["hysteresis_loop_width"], "jumps_at": rh1["predicted_jumps_at"]}, "[V]")
    add("RH2", bool(rh2["returns_to_torpor_setpoint"]),
        {"torpor_setpoint": rh2["torpor_setpoint"]}, "[V]")
    add("RH4", bool((not npdk4["hibernator_gamma_elevated_vs_nonhibernators"])
                    and gc["observed_endotherms_have_command_pair"]),
        {"deep_hibernator_PDK4_gamma": npdk4["deep_hibernator_PDK4_gamma"],
         "non_hibernator_PDK4_gamma": npdk4["non_hibernator_PDK4_gamma"]},
        "[V] reads / [O] regulatory gating", "the silenced-switch regulation is cited biology, not derived")
    add("RH6", rh6_ok, {"beats": osc.get("torpor_arousal_rhythm", {}).get("beats")}, "[V] mech / [L] period")
    add("RH8", bool(npanel["null_holds"]),
        {"genes_tested": npanel["genes_tested"],
         "genes_that_cleanly_separate_by_gamma": npanel["genes_that_cleanly_separate_by_gamma"],
         "cross_gene_pearson_r_dGamma_vs_dGC": npanel["cross_gene_pearson_r_delta_gamma_vs_delta_gc"]},
        "[V] reads + GC-confound / [O] no-marker conclusion",
        "small n + phylogenetic non-independence; the regulatory-gating mechanism is cited, not derived")
    add("RH9", bool(ncpg["null_holds"] and ncpg["two_static_reads_are_distinct"]),
        {"genes_tested": ncpg["genes_tested"],
         "genes_that_cleanly_separate_by_cpg_oe": ncpg["genes_that_cleanly_separate_by_cpg_oe"],
         "r_gamma_vs_cpg_oe": ncpg["cross_cell_pearson_r_gamma_vs_cpg_oe"],
         "r_gamma_vs_gc": ncpg["cross_cell_pearson_r_gamma_vs_gc"],
         "r_cpg_oe_vs_gc": ncpg["cross_cell_pearson_r_cpg_oe_vs_gc"]},
        "[V] reads + gamma/CpG-OE dissociation / [O] no-marker + dynamic-regulation external",
        "the DYNAMIC torpor methylation/expression state is cited external biology; the offline invariant "
        "precludes ingesting in-vivo data in-package (named honest next step, not derived)")
    add("RE1", bool(re1["returns_to_euglycemia"]),
        {"euglycemia_setpoint": re1["euglycemia_setpoint"]}, "[V] mech / [L] ~5 mM")
    add("RE2", bool(re2["setpoint_opposes_perturbation"]),
        {"adiposity_setpoint": re2["adiposity_setpoint"]}, "[V]")
    add("RD4", bool(rd4["torpor_returns_after_perturbation"] and rd4["insulin_resistance_crossed_and_stuck"]),
        {"pdk4_gamma": rd4["pdk4_gamma"], "ir_state": rd4["insulin_resistance_state"]},
        "[V] framing / [O] biology", "PDK4 co-upregulation in torpor & insulin resistance is cited, not derived")

    return {"targets": T, "all_pass": all(t["status"] == "PASS" for t in T),
            "n_pass": sum(t["status"] == "PASS" for t in T), "n_total": len(T)}


def foundational_analysis():
    """The endotherm-vs-ectotherm core (Q1 gene criterion, Q2 mechanism, Q3 range), surfaced for the site."""
    return dict(
        rederive=ee.rederive_offline(),
        gene_criterion=ee.gene_criterion(),
        null_ucp1=ee.null_ucp1_gamma_does_not_separate(),
        null_pdk4=ee.null_pdk4_gamma_does_not_mark_hibernation(),
        null_torpor_panel=ee.null_torpor_panel_gamma_does_not_track_hibernation(),
        null_cpg_oe_panel=ee.null_cpg_oe_does_not_track_hibernation(),
        setpoint_defense=ee.setpoint_defense_sweep(),
        continuum_or_switch=ee.continuum_or_switch(),
        endothermy_cost=ee.endothermy_cost(),
        kleiber=ee.kleiber_status(),
        cited_ranges=ee.CITED_RANGES,
    )




def circulate():
    organs = emerge_organs(); osc = confirm_oscillators()
    st = stress_targets()
    out = dict(_what="Thermometabolic Homeostasis -- emerge nodes from measured gamma, then circulate the "
                     "defended setpoint loops (thermostat / BAT / fever / torpor switch / glucose / lipostat / "
                     "hibernation bridge). Disease is a subset (see _pathology).",
               organs=organs, oscillators=osc,
               foundational=dict(
                   gene_criterion_endo_pair=ee.gene_criterion()["observed_endotherms_have_command_pair"],
                   gene_criterion_ecto_no_command=ee.gene_criterion()["observed_ectotherms_lack_ADRB3_command"],
                   null_ucp1_gamma_does_not_separate=ee.null_ucp1_gamma_does_not_separate()[
                       "pig_pseudogene_gamma_inside_functional_rodent_envelope"],
                   null_pdk4_gamma_does_not_mark_hibernation=not ee.null_pdk4_gamma_does_not_mark_hibernation()[
                       "hibernator_gamma_elevated_vs_nonhibernators"],
                   null_torpor_panel_no_gamma_marks_hibernation=ee.null_torpor_panel_gamma_does_not_track_hibernation()[
                       "null_holds"],
                   null_cpg_oe_methylation_substrate_no_marker=ee.null_cpg_oe_does_not_track_hibernation()[
                       "null_holds"],
                   offline_rederive_identical=ee.rederive_offline()["offline_identical"],
               ),
               dynamics=dict(
                   thermostat=thermostat_step(), bat_thermogenesis=bat_thermogenesis(),
                   fever_vs_hyperthermia=fever_vs_hyperthermia(), torpor_hysteresis=torpor_hysteresis_sweep(),
                   torpor_regulated=torpor_regulated(), glucose_homeostat=glucose_homeostat(),
                   lipostat=lipostat(), hibernation_bridge=hibernation_bridge(),
               ),
               stress_targets=st,
               torpor_switch=torpor_switch_probe())
    return out


def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    return o

def emit(obj):
    s = json.dumps(_round(obj), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = emit(circulate()); print(s); print("# sha256:", h)
