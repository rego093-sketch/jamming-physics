#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Digestive / Metabolic STRESS BATTERY.

VP-SPEC discipline (very high bar): each target is exercised under a WIDE sweep (not a single happy
path) and must hold WITHOUT per-target tuning. The dynamics come from the engine (single source); this
file only sweeps + grades. Failures are reported honestly; an [O] with a stated obstacle is acceptable,
a silent pass is not. Writing stays LOCKED until run_battery() is all PASS and
gates.write_research_complete() is called.

Targets
  T1  gastric pacemaker is a robust limit cycle (ISI CV small across a drive sweep)        [V]/[L]
  T2  aboral slow-wave gradient: duodenum (~12 cpm) > ileum (~8 cpm), monotone             [V]/[L]
  T3  a slow-wave phase gradient produces NET ABORAL transport; reverses under control      [V]
  T4  a glucose load returns to the ~5 mM setpoint via the insulin loop                     [V]/[L]
  T5  hypoglycaemia triggers glucagon/hepatic release back to setpoint (bounded loop)       [V]
  ONC carcinogen dose-response reproduces cited RR shapes + Hp x diet super-additivity      [L]/[V]/[O]
  ONC2 C6 neoplastic extension: Barrett's/Correa metaplasia step + HCC/ESCC synergy + MALT regression + anal HPV [L]/[V]/[O]
  DZ1 gastric dysrhythmia (brady/normal/tachy) + ectopic tachy entrainment + gastroparesis  [L]/[V]/[O]
  DZ2 diabetes T1/T2 spectrum: capacity (catastrophic) vs gain (compensated) on one loop     [L]/[V]/[O]
  DZ3 gastritis/peptic-ulcer erosion + gastric-vs-duodenal site split + neoplasia continuum  [L]/[V]/[O]
  DZ4 intestinal motility: slow-transit->colonic-inertia drive axis, CIPO ICC lesion, reversible ileus [V]/[O]
  DZ5 scattered Tier-1: dumping, reflux-erosion, insulinoma/reactive-hypo, FD-motility, SIBO-stasis      [V]/[L]/[O]
  DZ6 sphincter-gate (NEW gate primitive): GERD<->achalasia one gate two failures, spasm, Oddi           [V]/[O]
  DZ7 accommodation reservoir (NEW compliance primitive): functional dyspepsia post-prandial distress    [V]/[F]/[O]
  DZ8 afferent gain (NEW afferent primitive): IBS-C/-M/-D subtype + functional abdominal pain; gain=1/k   [V]/[F]/[O]
  DZ9 immune relapsing-inflammation (NEW primitive): IBD relapse hysteresis + induction/maintenance asymmetry + burden->barrier->CRC bridge (closes s21 small-bowel) [V]/[F]/[L]/[O]
  DZ10 exocrine autocatalysis (NEW primitive): acute pancreatitis irreversible latch past threshold (pre-threshold-only) + large-reserve EPI + PERT rescue [V]/[F]/[L]/[O]
  DZS cross-system seam WIRING (NEW seam layer, no engine/disease change): circulatory hepatic interface consumed as the s24 NAFLD + s25 bile delivery substrate (vendored snapshot, no sibling import); mind felt-symptom firewall (visceral pain s18, biliary colic s25) a one-way pointer; firewall enforced by an architectural lock (0 sibling imports; metabolic state mind-free) [V]/[F]/[O]
  DZD the whole disease layer is 2x-sha256 deterministic (digest identical across runs)       [V]
"""
import os, sys, json, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_oncology"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_disease"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_seams"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_analgesic"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import importlib
import numpy as np
eng  = importlib.import_module("vp_dig_engine")
onco = importlib.import_module("carcinogen_dose_response")
dz   = importlib.import_module("disease_modules")
seam = importlib.import_module("seam_wiring")
analg = importlib.import_module("analgesic_logic")
from vp_substrate import Neuron, dominant_freq

def _res(tid, desc, ok, value, grade, obstacle=None):
    return {"target": tid, "description": desc, "status": "PASS" if ok else "FAIL",
            "value": value, "grade": grade, "obstacle_if_open": obstacle}

# --------------------------------------------------------------------------- T1
def t1_gastric_pacemaker():
    cvs, freqs = [], []
    for dr in [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=eng.TAU_STOMACH, beta=0.5)
        S, dt = n.run(drive=float(dr), T=12000.0, dt=0.05)
        sp = Neuron.spikes(S); f = dominant_freq(S, dt); freqs.append(f)
        cvs.append(float(np.diff(sp).std() / np.diff(sp).mean()) if len(sp) >= 3 else 9.9)
    ok = all(c < 0.15 for c in cvs) and all(f > 0 for f in freqs)
    return _res("T1", "gastric ICC is a robust limit cycle; rate anchored to ~3 cpm",
                ok, {"max_ISI_CV": round(max(cvs), 4), "gastric_cpm": round(eng.K_TIME * freqs[3], 3)},
                "[V] limit cycle / [L] rate")

# --------------------------------------------------------------------------- T2
def t2_aboral_gradient():
    mono = True; endp = True
    for N in [8, 12, 16, 20]:
        for dr in [0.50, 0.55, 0.60]:
            c = eng.intestinal_chain(N=N, drive=dr)
            mono &= all(c[i] >= c[i + 1] - 1e-9 for i in range(len(c) - 1))
            endp &= (abs(c[0] - 12) / 12 < 0.15 and abs(c[-1] - 8) / 8 < 0.20)
    c12 = eng.intestinal_chain(N=12)
    ok = mono and endp
    return _res("T2", "aboral slow-wave gradient duodenum(~12)>ileum(~8), monotone over N & drive",
                ok, {"monotone": mono, "endpoints_ok": endp, "duodenum_cpm": c12[0], "ileum_cpm": c12[-1]},
                "[V] gradient / [L] absolute")

# --------------------------------------------------------------------------- T3
def t3_peristalsis():
    fwd = eng.peristalsis_transport(+1); rev = eng.peristalsis_transport(-1)
    rob = True
    for cp in [0.03, 0.05, 0.08]:
        for Dt in [0.15, 0.20, 0.30]:
            if eng.peristalsis_transport(+1, coupling=cp, Dtrans=Dt) <= 0.02: rob = False
    ok = (fwd > 0.05) and (rev < -0.05) and rob
    return _res("T3", "slow-wave phase gradient -> net aboral transport; reverses under control",
                ok, {"aboral_disp_segments": round(fwd, 3), "reversed_disp_segments": round(rev, 3),
                     "robust_over_coupling_Dtrans": rob}, "[V]")

# --------------------------------------------------------------------------- T4
def t4_glucose_load():
    _, Gf = eng.glucose_homeostat(G0=5.0, T=60.0); base = float(Gf[-1]); ok = True; rows = []
    for amp in [1.0, 2.0, 3.0, 4.0, 6.0]:
        _, Gt = eng.glucose_homeostat(G0=base, meal=eng._pulse(amp), T=30.0)
        pk = float(Gt.max()); fn = float(Gt[-1])
        good = (pk > base + 0.3) and (abs(fn - 5.0) < 0.4); ok &= good
        rows.append({"amp": amp, "peak": round(pk, 2), "final": round(fn, 2)})
    return _res("T4", "glucose load returns to the ~5 mM setpoint via the insulin loop",
                ok, {"fasting_mM": round(base, 3), "loads": rows}, "[V] homeostasis / [L] setpoint")

# --------------------------------------------------------------------------- T5
def t5_counter_regulation():
    ok = True; rows = []
    for amp in [1.0, 2.0, 3.0, 4.0]:
        _, Gt = eng.glucose_homeostat(G0=5.0, ins_kick=eng._pulse(amp), T=30.0)
        nd = float(Gt.min()); fn = float(Gt[-1])
        good = (nd < 5.0 - 0.3) and (abs(fn - 5.0) < 0.5 and fn > nd + 0.2) and (float(Gt.max()) < 9.0)
        ok &= good; rows.append({"kick": amp, "nadir": round(nd, 2), "final": round(fn, 2)})
    return _res("T5", "hypoglycaemia triggers glucagon/hepatic release back to setpoint (bounded)",
                ok, {"challenges": rows}, "[V]")

# --------------------------------------------------------------------------- ONC
def onc_oncology():
    v = onco.validate()
    val = {"colorectal_anchor_hit": v["colorectal"]["anchor_hit"],
           "pancreatic_RR_at_30py": v["pancreatic_RR_at_30py"],
           "gastric_super_additive": v["gastric"]["super_additive"],
           "gastric_sub_multiplicative_prediction": v["gastric"]["sub_multiplicative"]}
    return _res("ONC", "carcinogen dose-response reproduces cited RR shapes + Hp x diet super-additivity",
                v["passed"], val, "[L] anchor / [V] shape & synergy / [O] absolute incidence",
                obstacle="absolute incidence rate needs external population calibration (epidemiology)")

def onc2_oncology_extension():
    v = onco.validate_c6()
    eac = v["metaplasia"]["eac"]; gca = v["metaplasia"]["gca_int"]
    hcc = v["synergy"]["hcc"]; escc = v["synergy"]["escc"]
    malt = v["malt"]; anal = v["anal"]
    digs = {onco.c6_digest()[1] for _ in range(3)}          # 2x-sha256 identical across runs
    digest_ok = len(digs) == 1
    val = {
        # (a) metaplasia step: precursor anchor-locked + rate-limiting, dysplasia ladder accelerates, treatment lowers rate
        "eac_anchor_locked_rate_limiting": eac["anchor_hit"] and eac["rate_limiting"],
        "eac_ladder_monotone_accelerating": eac["ladder_monotone"] and eac["ladder_accelerating"],
        "eac_treatment_lowers_rate": eac["treatment_lowers_rate"],
        "gca_int_metaplasia_anchor_locked": gca["anchor_hit"] and gca["rate_limiting"],
        # (b) synergy: super-additive reproduced + sub-multiplicative predicted (both organs, one barrier)
        "hcc_super_additive_sub_multiplicative": hcc["super_additive"] and hcc["sub_multiplicative_prediction"],
        "escc_super_additive_sub_multiplicative": escc["super_additive"] and escc["sub_multiplicative_prediction"],
        # (c) reversible MALT (regresses on g-restore) + single-driver anal (monotone in HPV bias)
        "malt_reversible_on_g_restore": malt["reversible_on_g_restore"],
        "anal_monotone_in_hpv_bias": anal["monotone"],
        # (d) honest out-of-kernel boundary recorded
        "out_of_kernel_sites_recorded": len(v["out_of_kernel"]),
        # determinism
        "c6_digest_sha256": onco.c6_digest()[1],
        "c6_digest_runs_identical": digest_ok,
    }
    return _res("ONC2", "C6 neoplastic extension: Barrett's/Correa metaplasia step (precursor rate-limiting, dysplasia "
                "ladder accelerates, ablation/eradication lowers the next-step rate), HCC (HBVxaflatoxin) and ESCC "
                "(smokexalcohol) synergy reproduce super-additivity AND predict sub-multiplicativity, gastric MALT "
                "regresses on g-restore, anal SCC monotone in HPV bias; the carcinogen-Kramers boundary is stated "
                "honestly (GIST/NET/small-bowel/cholangio out-of-kernel)",
                v["passed"] and digest_ok, val,
                "[L] per-site epidemiological anchors / [V] metaplasia rate-limiting, dysplasia-ladder shape & synergy / "
                "[O] absolute incidence %/yr, exact dysplasia ratios, and the four out-of-kernel sites",
                obstacle="absolute cancer incidence (%/yr) and the exact dysplasia-ladder ratios need external population "
                         "calibration (the model fixes direction + rate-limiting, not the absolute hazard); GIST/NET "
                         "(gene-key -> disease_wp), small-bowel adenocarcinoma (needs the C1 immune layer) and "
                         "cholangiocarcinoma (needs a hepatobiliary+immune layer; circulatory seam) are out-of-kernel")

SUITES = [t1_gastric_pacemaker, t2_aboral_gradient, t3_peristalsis,
          t4_glucose_load, t5_counter_regulation, onc_oncology, onc2_oncology_extension]

# --------------------------------------------------------------------------- DZ1
def dz1_dysrhythmia_gastroparesis():
    d = dz.validate_d1()
    val = {"rhythm_spans_brady_normal_tachy": d["dysrhythmia"]["spans_brady_normal_tachy"],
           "tachy_only_when_faster_focus_couples": d["ectopic"]["tachy_only_when_faster_and_coupled"],
           "emptying_monotone_in_density": d["gastroparesis"]["monotone_in_density"],
           "severe_depletion_pct_of_normal": d["gastroparesis"]["severe_depletion_pct_of_normal"]}
    return _res("DZ1", "gastric dysrhythmia bands + ectopic tachy entrainment + density-graded gastroparesis",
                d["passed"], val, "[L] EGG band / [V] dysrhythmia+entrainment+emptying / [O] absolute emptying rate",
                obstacle="absolute gastric-emptying rate needs clinical (scintigraphy) calibration")

# --------------------------------------------------------------------------- DZ2
def dz2_diabetes_spectrum():
    d = dz.validate_d2()
    val = {"t1_crosses_diabetes_and_severe": d["t1_capacity"]["crosses_diabetes_threshold"] and d["t1_capacity"]["severe_at_deep_depletion"],
           "t2_compensated_and_returns": d["t2_sensitivity"]["sub_severe_across_sweep"] and d["t2_sensitivity"]["return_preserved"],
           "axes_distinct_gap_widens": d["axes_distinct"], "matched_depth_gap": d["matched_depth_gap"],
           "igt_in_pre_diabetes_band": d["igt"]["in_pre_diabetes_band"]}
    return _res("DZ2", "diabetes T1/T2 spectrum: capacity loss catastrophic vs gain loss compensated on one homeostat",
                d["passed"], val, "[L] FPG thresholds / [V] two-axis emergence / [O] absolute prevalence",
                obstacle="absolute diabetes prevalence needs external population calibration (epidemiology)")

# --------------------------------------------------------------------------- DZ3
def dz3_gastritis_ulcer():
    d = dz.validate_d3()
    val = {"erosion_monotone_convex": d["erosion"]["monotone"] and d["erosion"]["convex"],
           "nsaid_anchor_hit": d["erosion"]["anchor_hit"],
           "ulcer_sites_both_cross_distinct_routes": d["ulcer_site_split"]["both_cross"] and d["ulcer_site_split"]["distinct_routes"],
           "continuum_shares_s10_g_Hp": d["continuum"]["same_g_as_cancer_step"]}
    return _res("DZ3", "gastritis/ulcer erosion shape + gastric(defence)-vs-duodenal(acid) split + inflammation->neoplasia continuum",
                d["passed"], val, "[L] NSAID ulcer anchor / [V] shape+split+continuum / [O] absolute incidence",
                obstacle="absolute erosion/ulcer incidence needs clinical/population calibration")

# --------------------------------------------------------------------------- DZD
def dzd_disease_determinism():
    hs = {dz.digest()[1] for _ in range(3)}
    ok = len(hs) == 1
    return _res("DZD", "the disease layer digest is identical across runs (2x-sha256 reproducible)",
                ok, {"disease_sha256": dz.digest()[1], "runs_identical": ok}, "[V]")

# --------------------------------------------------------------------------- DZ4
def dz4_intestinal_motility():
    d = dz.validate_d4()
    val = {"slow_transit_graded_then_inertia_collapse": d["slow_transit_and_inertia"]["graded_monotone"] and d["slow_transit_and_inertia"]["inertia_collapse_below_threshold"],
           "cipo_functional_obstruction_lumen_patent": d["cipo"]["functional_obstruction_lumen_patent"],
           "ileus_reversible_scales_with_duration": d["ileus"]["reversible_scales_with_duration"],
           "icc_lesion_collapses_stomach_and_gut": d["icc_unifying"]["both_sites_collapse_monotonically"]}
    return _res("DZ4", "intestinal motility: slow-transit->colonic-inertia drive axis, CIPO ICC lesion, reversible ileus, one ICC lesion across stomach+gut",
                d["passed"], val, "[V] transit mechanisms / [L-pending] transit anchors / [O] absolute transit time",
                obstacle="absolute colonic transit time needs clinical (radio-opaque marker / scintigraphy) calibration")

# --------------------------------------------------------------------------- DZ5
def dz5_scattered_tier1():
    d = dz.validate_d5()
    a = d["d5a_dumping"]; b = d["d5b_reflux_esophagitis"]; c = d["d5c_insulinoma_reactive_hypo"]
    fd = d["d5d_functional_dyspepsia_motility"]; e = d["d5e_sibo_stasis"]
    val = {
        # D5a dumping (metabolic features emerge on s5; mechanical magnitude is the honest [O])
        "dumping_early_peak_rises_with_speed": a["early_dumping"]["peak_rises_with_emptying_speed"],
        "dumping_late_biphasic_crosses_hypo": a["late_dumping"]["biphasic"] and a["late_dumping"]["fast_delivery_crosses_hypo"],
        "dumping_mechanical_slow_reduces_rapid_saturates": a["mechanical"]["slow_side_reduces"] and a["mechanical"]["rapid_side_saturates"],
        # D5b reflux-oesophagitis erosion (shared s13 Kramers kernel)
        "reflux_erosion_monotone_convex": b["erosion"]["monotone"] and b["erosion"]["convex"],
        "reflux_shares_s13_kappa": b["erosion"]["kappa_shared_with_s13"],
        # D5c insulinoma (mirror of T1) + reactive hypoglycaemia
        "insulinoma_fasting_falls_crosses_hypo": c["insulinoma"]["fasting_monotone_falls"] and c["insulinoma"]["crosses_hypo_threshold"],
        "insulinoma_recovers_on_resection": c["insulinoma"]["recovers_on_resection"],
        "reactive_hypo_nadir_deepens_below_baseline": c["reactive_hypoglycemia"]["nadir_deepens"] and c["reactive_hypoglycemia"]["dips_below_baseline"],
        # D5d functional-dyspepsia motility (mild point on the s11 axis, distinct from severe gastroparesis)
        "fd_mild_delay_distinct_from_severe": fd["fd_motility"]["mild_delay_present"] and fd["fd_motility"]["distinct_from_severe"],
        "fd_mild_emptying_pct": fd["fd_motility"]["mild_emptying_pct"],
        # D5e SIBO-stasis (rising retained proximal fraction as propulsive drive falls)
        "sibo_retention_rises_as_drive_falls": e["sibo"]["retention_monotone_rises_as_drive_falls"],
        "sibo_clears_normal_stasis_low": e["sibo"]["clears_at_normal_drive"] and e["sibo"]["stasis_at_low_drive"],
    }
    return _res("DZ5", "five scattered Tier-1 perturbations: dumping (early/late metabolic + honest mechanical [O]), "
                "reflux-oesophagitis erosion (shared s13 kernel), insulinoma (mirror-of-T1) + reactive hypo, "
                "functional-dyspepsia mild-motility point, SIBO-stasis retention",
                d["passed"], val,
                "[L] hypo/NSAID anchors / [V] emergent metabolic+erosion+stasis mechanisms / "
                "[O] dumping mechanical magnitude, absolute nadir, bacterial load, felt FD component",
                obstacle="dumping rapid-emptying magnitude + absolute glucose nadir need the Tier-2 reservoir/"
                         "pyloric-brake element and clinical calibration; SIBO bacterial load needs a microbial "
                         "layer; the FD felt/distress component needs the Tier-2 accommodation + afferent-gain term")

# --------------------------------------------------------------------------- DZ6
def dz6_sphincter_gate():
    d = dz.validate_d6()
    a = d["d6a_gerd"]; b = d["d6b_achalasia"]; c = d["d6c_esophageal_spasm"]; o = d["d6d_sphincter_of_oddi"]
    val = {
        # D6a GERD: reflux burden rises monotonically as gate tone falls (continent high, incompetent low)
        "gerd_burden_rises_as_tone_falls": a["gerd"]["burden_monotone_rises_as_tone_falls"],
        "gerd_continent_high_incompetent_low": a["gerd"]["continent_at_high_tone"] and a["gerd"]["incompetent_at_low_tone"],
        "gerd_events_at_lowest_tone": a["gerd"]["rows"][-1][1],
        # D6b achalasia: gate stuck closed -> antegrade stasis (the GERD mirror) + aperistalsis
        "achalasia_passes_competent_stasis_when_stuck": b["achalasia"]["passes_when_competent"] and b["achalasia"]["stasis_when_gate_fails_to_open"],
        "achalasia_aperistalsis_degrades_transit": b["achalasia"]["aperistalsis_degrades_transit"],
        # D6c esophageal spasm: coordination loss collapses transit; amplitude cannot rescue
        "spasm_transit_collapses_coordination_lost": c["spasm"]["transit_collapses_as_coordination_lost"],
        "spasm_amplitude_cannot_rescue": c["spasm"]["amplitude_cannot_rescue"],
        # D6d sphincter of Oddi: stuck gate -> outflow obstruction (same gate, biliary outlet)
        "oddi_outflow_obstructs_when_stuck": o["oddi"]["outflow_obstructs_when_gate_stuck"],
    }
    return _res("DZ6", "B1 sphincter-gate cluster on one NEW R19-derived gate primitive: GERD (reflux burden rises as "
                "tone falls) and achalasia (stuck-closed gate -> stasis) as the two opposite failures of one gate, "
                "esophageal spasm (coordination loss collapses transit, amplitude cannot rescue), sphincter of Oddi "
                "(stuck-gate outflow obstruction)",
                d["passed"], val,
                "[V] all motor readings (gate + s4 coordination) / [O] felt chest pain, absolute reflux frequency / "
                "clearance / outflow",
                obstacle="absolute reflux frequency, achalasia clearance, and Oddi outflow need clinical "
                         "(manometry / pH-impedance / scintigraphy) calibration; the felt chest-pain component of "
                         "spasm is afferent-gain (B3 / mind), out of scope for this motor cluster")

# --------------------------------------------------------------------------- DZ7
def dz7_accommodation_reservoir():
    d = dz.validate_d7()
    cv = d["accommodation"]; tx = d["treatment_axis"]; yi = d["yield_identity"]
    val = {
        # premature pressure on a fixed meal rises monotonically as fundic accommodation falls
        "pressure_rises_as_accommodation_falls": cv["pressure_rises_as_accommodation_falls"],
        # compliance (= meal volume tolerated per unit satiation pressure) falls = early satiation
        "compliance_falls_as_accommodation_falls": cv["compliance_falls_as_accommodation_falls"],
        # normal fundus absorbs the meal (low pressure); impaired accommodation = premature pressure
        "normal_absorbs_premature_when_impaired": cv["normal_absorbs_meal"] and cv["premature_pressure_when_impaired"],
        "fd_pressure_pct_of_stiff_baseline": round(100.0 * cv["fd_pressure"] / cv["baseline_stiff_pressure"], 1),
        # treatment direction: raising the compliance term lowers the fixed-meal pressure
        "raising_compliance_lowers_pressure": tx["raising_compliance_lowers_pressure"],
        # substrate identity: the maximal-compliance yield point IS the R19 spinodal (exact)
        "yield_point_is_r19_spinodal": yi["yield_is_r19_spinodal"],
    }
    return _res("DZ7", "B2 accommodation-reservoir reader on one NEW R19-derived compliance primitive: functional "
                "dyspepsia (post-prandial distress) -- impaired fundic accommodation stiffens the reservoir so a fixed "
                "meal raises pressure prematurely (early satiation; compliance falls), monotone under a wide "
                "accommodation sweep; the maximal-compliance yield point is the R19 spinodal (exact); treatment raises "
                "the compliance term to lower the meal pressure",
                d["passed"], val,
                "[V] premature-pressure / early-satiation mechanism (post-prandial-distress axis s15 left open) / "
                "[O] felt distress (B3 afferent gain + mind firewall), absolute meal-volume / pressure scale",
                obstacle="the felt post-prandial-distress symptom needs the B3 visceral afferent-gain term with the "
                         "felt interpretation in `mind` (firewall); the absolute meal-volume and intra-gastric-pressure "
                         "scale is a model unit needing barostat / manometry calibration")

# --------------------------------------------------------------------------- DZ8
def dz8_ibs_afferent_gain():
    d = dz.validate_d8()
    sub = d["ibs_subtype"]; hs = d["visceral_hypersensitivity"]; fap = d["functional_abdominal_pain"]; idn = d["gain_identity"]
    val = {
        # IBS subtype: the s14 transport bias orders C->M->D (retention falls), rapid magnitude saturates (s15 ceiling)
        "ibs_subtype_retention_monotone_orders_C_M_D": sub["retention_monotone_falls_as_drive_rises"] and sub["subtypes_ordered_C_M_D"],
        "ibs_rapid_magnitude_saturates_s15_ceiling": sub["rapid_magnitude_saturates"],
        # visceral hypersensitivity: afferent gain + fixed-distension signal rise (allodynia); crisis past yield
        "hypersensitivity_gain_and_allodynia_rise": hs["gain_rises_with_sensitization"] and hs["signal_rises_allodynia"],
        "allodynia_amplification": hs["allodynia_amplification"],
        "quiescent_subyield_then_provoked_then_spontaneous_firing": (hs["quiescent_at_sub_yield"] and hs["provoked_firing_past_yield"] and hs["spontaneous_firing_past_spinodal"]),
        # functional abdominal pain: pain proxy rises at NORMAL motility (no structural lesion)
        "fap_pain_proxy_rises_at_normal_motility": fap["motility_normal"] and fap["pain_proxy_rises_at_normal_motility"],
        # substrate identity: afferent gain == s17 fundic compliance (1/k), and diverges at the R19 spinodal
        "afferent_gain_equals_s17_compliance": idn["gain_is_b2_compliance"],
        "gain_susceptibility_matches_simulated_response": idn["susceptibility_matches_response"],
        "gain_diverges_at_r19_spinodal": idn["gain_diverges_at_r19_spinodal"],
    }
    return _res("DZ8", "B3 visceral afferent-gain cluster on one NEW R19-derived afferent primitive: IBS subtype "
                "(the s14 transport bias orders IBS-C -> IBS-M -> IBS-D by retained fraction; the rapid-transit "
                "magnitude saturates at the s15 conserved-bolus ceiling) PLUS visceral hypersensitivity (the afferent "
                "gain chi = 1/k and the fixed-distension signal rise monotonically -- allodynia -- with a provoked "
                "then spontaneous firing flip past the R19 spinodal); functional abdominal pain (the pain proxy rises "
                "at normal motility, no structural lesion); and the substrate identity that the afferent gain is the "
                "SAME 1/k the s17 reservoir reads as fundic compliance, diverging at the same R19 spinodal (one "
                "curvature, two readings)",
                d["passed"], val,
                "[V] IBS motility-subtype ordering + visceral hypersensitivity (gain + allodynia) / [F] gain = "
                "compliance identity and divergence-at-spinodal / [O] absolute rapid-transit magnitude (s15 ceiling), "
                "absolute stool frequency, and the felt pain / affective experience (B3 peripheral term only; felt in mind)",
                obstacle="the absolute rapid-transit magnitude needs the Tier-2 reservoir / pyloric-brake element (the "
                         "s15 conserved-bolus ceiling) and clinical transit calibration; the felt visceral pain / "
                         "affective experience is `mind`'s (the firewall keeps only the peripheral afferent-gain term here)")

# --------------------------------------------------------------------------- DZ9
def dz9_immune_ibd():
    d = dz.validate_d9()
    rc = d["relapsing_course"]; nb = d["neoplasia_bridge"]; sl = d["same_layer"]
    val = {
        # relapsing-remitting hysteresis: the up-ramp flips to flare at a HIGHER antigen than the
        # down-ramp returns to remission (the flare basin self-sustains) -- a forced R19 double-well loop
        "relapsing_remitting_hysteresis": rc["relapsing_hysteresis"],
        # induction needs suppression past (antigen + spinodal) to break an established flare
        "induction_needs_suppression_past_antigen_plus_spinodal": rc["induction_needs_suppression_past_antigen_plus_spinodal"],
        # the SAME mid-dose holds remission but cannot break a flare = induction-vs-maintenance asymmetry
        "induction_maintenance_dose_asymmetry": rc["maintenance_threshold_lower_than_induction"],
        "induction_threshold": rc["induction_threshold"],
        "maintenance_threshold": rc["maintenance_threshold"],
        # cumulative inflammatory burden lowers the s7 barrier scale -> CRC RR rises, hitting the cited UC anchor
        "burden_raises_crc_rr_to_anchor": nb["rr_rises_with_burden"] and nb["anchor_hit"],
        # sustained suppression (mucosal healing) collapses the RR back toward baseline
        "suppression_collapses_rr": nb["suppression_collapses_rr"],
        # this closes the section-21 out-of-kernel small-bowel-adenocarcinoma boundary (inflammation route)
        "closes_s21_small_bowel_boundary": nb["closes_small_bowel_boundary"],
        # same element, antigen-dependent regime: celiac flares on gluten, remits gluten-free (driver removal -> barrier recovery)
        "celiac_antigen_dependent_driver_removal_restores_barrier": (sl["celiac_gluten_flare"] and sl["celiac_glutenfree_remission"] and sl["shared_lever_remove_driver_restores_barrier"]),
    }
    return _res("DZ9", "C1 immune relapsing-inflammation cluster on one NEW R19-derived primitive bridged to the "
                "section-7 kernel: inflammatory bowel disease shows relapsing-remitting HYSTERESIS (the flare basin "
                "self-sustains, so the flip-to-flare antigen exceeds the return-to-remission antigen -- a forced R19 "
                "double-well loop), an induction-vs-maintenance dose ASYMMETRY (breaking an established flare needs "
                "suppression past antigen + spinodal, but a lower dose then holds remission -- the same mid-dose has "
                "two outcomes by history), and a cumulative-burden bridge in which chronic inflammation lowers the "
                "SAME section-7 barrier scale that drives carcinogenesis, so the colitis-CRC risk rises to the cited "
                "anchor and collapses again under sustained suppression (mucosal healing) -- closing the section-21 "
                "out-of-kernel small-bowel-adenocarcinoma boundary on the inflammation route; the antigen-dependent "
                "regime (celiac and microscopic / eosinophilic / autoimmune) shares the element via driver removal",
                d["passed"], val,
                "[V] relapsing hysteresis + induction/maintenance asymmetry + burden->barrier->cancer continuity / "
                "[F] the induction and maintenance thresholds are exact spinodal identities / [L] the colitis-CRC RR "
                "anchor / [O] absolute remission and cancer-incidence rates, the celiac absorptive magnitude, and the "
                "felt / affective component",
                obstacle="absolute remission rates and cancer incidence need clinical-cohort calibration; the celiac "
                         "absorptive (villous-surface) magnitude needs an absorption layer; the felt / affective "
                         "component is `mind`'s (the firewall keeps only the inflammatory-drive term here)")

# --------------------------------------------------------------------------- DZ10
def dz10_exocrine_pancreatitis():
    d = dz.validate_d10()
    aa = d["acute_autocatalysis"]; ce = d["chronic_epi"]
    val = {
        # the autoactivation threshold rises with the protective inhibitor (SPINK1 raises it; PRSS1-gain lowers it)
        "autoactivation_threshold_rises_with_inhibitor": aa["threshold_rises_with_inhibitor"],
        "activation_threshold_at_baseline_inhibitor": aa["activation_threshold"],
        # sub-threshold trigger is safe; supra-threshold LATCHES (autocatalytic +g*s self-sustains)
        "subthreshold_safe_suprathreshold_latches": aa["subthreshold_safe"] and aa["suprathreshold_latches"],
        # pre-threshold removal prevents; once latched, NO parameter move reverses it (irreversible)
        "pre_threshold_prevents_post_threshold_irreversible": (aa["pre_threshold_intervention_prevents"] and aa["post_threshold_irreversible"]),
        # a strong-enough inhibitor (> spinodal) abolishes the self-sustaining basin -> reversible
        "strong_inhibitor_abolishes_latch": aa["strong_inhibitor_reversible"],
        # chronic EPI: large secretory reserve -- steatorrhea only past ~90% acinar loss (DiMagno 1973)
        "large_reserve_steatorrhea_only_past_90pct_loss": ce["large_reserve_steatorrhea_only_past_90pct_loss"],
        "epi_adequacy_monotone_in_capacity": ce["adequacy_monotone_in_capacity"],
        # PERT (exogenous enzyme) restores secretory output above the digestive demand
        "pert_restores_adequacy": ce["pert_restores_adequacy"],
    }
    return _res("DZ10", "C2 exocrine-autodigestion cluster on one NEW R19-derived autocatalytic primitive (plus a "
                "module-level secretory-reserve reading): acute pancreatitis is a self-amplifying zymogen cascade -- "
                "the autoactivation threshold rises with the protective inhibitor (SPINK1 up, PRSS1-gain / SPINK1-loss "
                "down), a sub-threshold trigger is safe but a supra-threshold trigger LATCHES because the autocatalytic "
                "term self-sustains, so PRE-threshold removal prevents while an established attack is IRREVERSIBLE to "
                "any parameter move (only a strong-enough inhibitor past the spinodal abolishes the basin) -- the "
                "model's pre-threshold-only intervention logic; chronic pancreatitis / exocrine pancreatic "
                "insufficiency reads the large secretory RESERVE (steatorrhea only past ~90% acinar loss) with PERT "
                "restoring output above the digestive demand",
                d["passed"], val,
                "[V] threshold-rises-with-inhibitor + irreversible supra-threshold latch (pre-threshold-only) + "
                "strong-inhibitor reversibility + large-reserve EPI + PERT rescue / [F] the latch is a forced R19 "
                "hysteresis / [L] the >90%-loss steatorrhea reserve threshold / [O] absolute trigger / inhibitor and "
                "demand scales and established-disease outcomes",
                obstacle="the absolute trigger / inhibitor and digestive-demand scales are model units needing "
                         "clinical calibration; established-disease outcomes (necrosis extent, organ failure) need a "
                         "tissue-injury layer; cystic-fibrosis CFTR is gene-key (`disease_wp` owns the gene defect, "
                         "this package owns the ductal-secretion dynamics)")

# --------------------------------------------------------------------------- DZ11
def dz11_perfusion_ischemia():
    d = dz.validate_d11()
    cm = d["chronic_mesenteric"]; ai = d["acute_ischemia"]; nf = d["nafld"]
    val = {
        # chronic mesenteric ischaemia ("intestinal angina"): the perfusion margin above the rescue
        # threshold falls as post-prandial demand rises, crossing into deficit after a meal
        "margin_falls_as_demand_rises": cm["margin_falls_as_demand_rises"],
        "crosses_to_deficit_postprandially": cm["crosses_to_deficit_postprandially"],
        # revascularisation (stent/bypass) lifts supply so the margin is positive across demand again
        "revascularization_restores_margin": cm["revascularization_restores_margin"],
        # acute occlusion flips viable->ischaemic once supply drops past demand - spinodal (a forced flip)
        "occlusion_flips_to_ischemic": ai["occlusion_flips"] and ai["flips_to_ischemic_when_supply_fails"],
        "flip_threshold": ai["flip_threshold"],
        "salvage_reserve_window": ai["reserve_window"],
        # reperfusion WITHIN the reserve window recovers; partial reperfusion stays infarcted (time-critical)
        "reperfusion_within_window_recovers": ai["reperfusion_recovers_within_window"],
        "partial_reperfusion_stays_ischemic": ai["partial_reperfusion_stays_ischemic"],
        # NAFLD/MASLD metabolic overlap reuses the section-12 type-2 gain-loss homeostat (no new fit);
        # the lipid-deposition layer is declared a `circulatory` seam, not modelled here
        "nafld_reuses_s12_type2_gain_loss": nf["insulin_resistance_reuses_s12_type2_gain_loss"],
        "lipid_layer_is_circulatory_seam": nf["lipid_handling_is_circulatory_seam"],
    }
    return _res("DZ11", "C3 perfusion/vascular Tier-3 cluster on one NEW R19-derived perfusion-viability primitive: "
                "chronic mesenteric ischaemia is intestinal angina -- the perfusion reserve above the rescue threshold "
                "falls as post-prandial demand rises and crosses into deficit after a meal, with revascularisation "
                "restoring a positive margin; acute mesenteric ischaemia (and ischaemic colitis) is a forced viable-> "
                "ischaemic FLIP once supply drops past demand minus the spinodal, with a time-critical salvage window "
                "in which reperfusion recovers the tissue but partial / late reperfusion stays infarcted; the NAFLD / "
                "MASLD metabolic overlap reuses the section-12 type-2 gain-loss homeostat (nothing refitted) while the "
                "lipid-deposition layer is declared a `circulatory` seam",
                d["passed"], val,
                "[V] demand-driven margin collapse + revascularisation rescue + forced occlusion flip + time-critical "
                "salvage window + reuse of the s12 type-2 homeostat / [F] the ischaemic flip and rescue thresholds are "
                "exact spinodal identities / [O] the absolute perfusion / demand scales, the structural infarct extent, "
                "and the `circulatory` lipid-deposition layer",
                obstacle="the absolute perfusion-pressure and metabolic-demand scales are model units needing clinical "
                         "calibration; structural infarction (transmural necrosis, perforation) is an out-of-model "
                         "tissue-injury endpoint; the lipid-handling / steatosis-deposition layer belongs to "
                         "`circulatory` (this package keeps only the perfusion-viability switch and the reused glucose homeostat)")

# --------------------------------------------------------------------------- DZ12
def dz12_hepatobiliary_bile():
    d = dz.validate_d12()
    ch = d["cholelithiasis"]; ds = d["dissolution"]; sm = d["seams"]
    val = {
        # cholelithiasis: bile supersaturation (CSI>1) is METASTABLE, not sufficient -- a stone nucleates
        # only once the cholesterol saturation index passes 1 + spinodal (a nucleation barrier, not a line)
        "supersaturation_metastable_not_sufficient": ch["supersaturation_metastable_not_sufficient"],
        "nucleates_only_past_spinodal": ch["nucleates_only_past_spinodal"],
        "nucleation_csi": ch["nucleation_csi"],
        # dissolution hysteresis: a formed stone persists BELOW saturation and redissolves only far below it
        # -> medical (UDCA) dissolution works only on small, early, still-near-saturation stones
        "stone_persists_below_saturation": ds["stone_persists_below_saturation"],
        "redissolves_only_far_below_saturation": ds["redissolves_only_far_below_saturation"],
        "dissolution_hysteresis_gap": ds["hysteresis_gap"],
        # seams: gallbladder stasis is the B1 sphincter-gate primitive; cholecystitis adds the C1 flare;
        # biliary dyskinesia is the B1 gate; nucleation time is the Kramers barrier-crossing rate
        "stasis_is_b1_gate_seam": sm["stasis_is_b1_gate_seam"],
        "cholecystitis_is_b1_gate_plus_c1_flare": sm["cholecystitis_is_b1_gate_plus_c1_flare"],
        "nucleation_time_is_kramers_rate": sm["nucleation_time_is_kramers_rate"],
    }
    return _res("DZ12", "C4 hepatobiliary/bile Tier-3 cluster on one NEW R19-derived supersaturation/nucleation "
                "primitive: cholelithiasis is cholesterol-bile crystallisation in which supersaturation (CSI>1) is "
                "METASTABLE rather than sufficient -- a stone nucleates only once the saturation index passes 1 plus "
                "the spinodal (a nucleation barrier, the Kramers rate), and a formed stone then shows dissolution "
                "HYSTERESIS, persisting below saturation and redissolving only far below it, which is exactly why "
                "medical (UDCA) dissolution succeeds only on small early stones still near saturation; gallbladder "
                "STASIS is declared the B1 sphincter-gate seam, cholecystITIS the B1 gate plus the cited C1 "
                "inflammatory flare, and biliary dyskinesia the B1 gate -- with `circulatory` (cholesterol delivery) "
                "and `mind` (the felt biliary colic) seams declared",
                d["passed"], val,
                "[V] metastable supersaturation + barrier-gated nucleation + dissolution hysteresis (UDCA only on "
                "small early stones) / [F] the nucleation and dissolution thresholds are exact spinodal identities and "
                "the nucleation time is the Kramers barrier-crossing rate / [O] the absolute saturation-index scale, "
                "the stasis/flare seams owned by B1/C1, and the cholesterol-delivery and felt-pain seams",
                obstacle="the absolute cholesterol-saturation-index scale is a model unit needing clinical calibration; "
                         "gallbladder stasis and cholecystitis are owned by the B1 gate and C1 flare primitives (cited "
                         "seams, not re-modelled here); cholesterol delivery is a `circulatory` seam and the felt "
                         "biliary colic is `mind`'s (the firewall keeps only the crystallisation thermodynamics)")

# --------------------------------------------------------------------------- DZ13
def dz13_structural_wall():
    d = dz.validate_d13()
    dp = d["diverticular_pressure"]; ws = d["wall_strength"]; tb = d["treatment_boundary"]
    val = {
        # diverticular disease: by Laplace P = tension/radius a low-fibre diet (small hard stools gripped by
        # strong segmenting contractions) raises wall pressure as radius falls, herniating past P = spinodal(g_wall)
        "laplace_pressure_rises_as_radius_falls": dp["laplace_pressure_rises_as_radius_falls"],
        "herniates_at_low_fibre_small_radius": dp["herniates_at_low_fibre_small_radius"],
        "herniation_threshold": dp["herniation_threshold"],
        # a WEAKER wall (aging connective tissue, Ehlers-Danlos/Marfan collagen) has a lower threshold, so it
        # herniates at a fixed segmental pressure a normal wall withstands (age-rising diverticulosis prevalence)
        "threshold_falls_as_wall_weakens": ws["threshold_falls_as_wall_weakens"],
        "weaker_wall_herniates_at_same_pressure": ws["weaker_wall_herniates_at_same_pressure"],
        "fixed_test_pressure": ws["pressure"],
        # treatment is the geometry in reverse: dietary fibre bulks the stool (larger radius) and softens the
        # segmenting contractions (lower tension), dropping Laplace P below the herniation threshold
        "fibre_lowers_pressure_below_threshold": tb["fibre_lowers_pressure_below_threshold"],
        # diverticulITIS is the cited C1 flare; mechanical fixed-block obstruction is the s14 functional counterpart
        "diverticulitis_is_c1_flare_seam": tb["diverticulitis_is_c1_flare_seam"],
        "mechanical_block_is_s14_excluded_counterpart": tb["mechanical_block_is_s14_excluded_counterpart"],
    }
    return _res("DZ13", "C5 structural/mechanical Tier-3 cluster on one NEW R19-derived wall-mechanics primitive: "
                "diverticular disease is wall herniation under segmental Laplace pressure -- by P = tension/radius a "
                "low-fibre diet (small hard stools gripped by strong high-pressure segmenting contractions) raises the "
                "wall pressure as the luminal radius falls, and once P exceeds the herniation threshold spinodal(g_wall) "
                "the intact wall buckles out into a diverticulum; a WEAKER wall (aging connective tissue, Ehlers-Danlos "
                "/ Marfan collagen) has a lower threshold and herniates at a fixed pressure a normal wall withstands "
                "(the age-rising prevalence and collagen-disorder association); treatment is the geometry in reverse -- "
                "fibre bulks the stool (larger radius) and softens the segmenting contractions (lower tension), dropping "
                "P back below threshold -- while diverticulITIS is the cited C1 flare and the mechanical FIXED-block "
                "obstructions (hernia incl. hiatal, volvulus, intussusception, adhesions) are the section-14 "
                "functional-module's structural counterpart",
                d["passed"], val,
                "[V] Laplace pressure rising as radius falls + discontinuous herniation + lower threshold of a weaker "
                "wall + fibre treatment dropping P below threshold / [F] the herniation threshold is an exact spinodal "
                "identity / [O] the absolute pressure and wall-strength scales, the C1 diverticulitis seam, and the "
                "s14 mechanical-block counterpart (surgical, out-of-model)",
                obstacle="the absolute Laplace-pressure and wall-strength scales are model units needing clinical "
                         "calibration; diverticulITIS inflammation is the cited C1 flare seam (not re-modelled); the "
                         "mechanical fixed-block obstructions are the section-14 functional module's structural "
                         "counterpart whose lever is relieving the block (often surgical -- out-of-model for parameter therapy)")

# --------------------------------------------------------------------------- DZS
def dzs_cross_system_seams():
    """Cross-system seam WIRING (section 27): the circulatory hepatic delivery substrate consumed by the
    section-24 NAFLD/MASLD and section-25 bile readings, and the mind felt-symptom firewall (visceral pain
    section 18, biliary colic section 25 deferred OUT by a one-way pointer). The wiring is citation/pointer-
    only: a vendored circulatory snapshot consumed here (no sibling import), and a forward-defer pointer to
    mind. The firewall is enforced by an architectural lock -- ZERO sibling imports anywhere in the package
    and a metabolic state with no felt/HPA key -- the SAME lock mind runs neuro-side."""
    v = seam.validate_seams()
    hep = v["circulatory_hepatic_interface"]; nf = v["s24_nafld_delivery"]; bl = v["s25_bile_delivery"]
    fw = v["firewall"]; mp = v["mind_pointer"]; ss = v["ssot_consistency"]
    val = {
        # circulatory is SSOT for the hepatic interface (its CHARTER 'Seams OUT'); digestive consumes the
        # vendored snapshot (Q_H / E / F), verified against circulatory's hepatic_clearance() at vendoring
        "consumes_circulatory_hepatic_Q_H_ml_min": hep["Q_H_ml_min"],
        "consumes_circulatory_extraction_E": hep["E"],
        "consumes_circulatory_bioavailability_F": hep["F"],
        "circulatory_is_ssot_owner": hep["owner_is_ssot"],
        # section 24: the insulin-resistance core REUSES the s12 type-2 homeostat (digestive-owned), the
        # lipid DEPOSITION rests on the consumed circulatory perfusion, the lipid HANDLING is [O] (circulatory)
        "s24_nafld_reuses_s12_type2_gain_loss": nf["reuses_s12_type2_gain_loss"],
        "s24_lipid_delivery_rests_on_consumed_circulatory": nf["delivery_rests_on_consumed_circulatory"],
        "s24_wired": nf["wired"],
        # section 25: the nucleation thermodynamics are digestive-owned, the cholesterol DELIVERY rests on
        # the consumed circulatory perfusion, the absolute CSI scale is [O] (circulatory)
        "s25_nucleation_csi": bl["nucleation_csi"],
        "s25_cholesterol_delivery_rests_on_consumed_circulatory": bl["delivery_rests_on_consumed_circulatory"],
        "s25_wired": bl["wired"],
        # SSOT consistency: both readings consume the SAME snapshot value (internal check, no sibling import)
        "ssot_consumed_Q_H_matches_snapshot": ss["consumed_Q_H_matches_snapshot"],
        "ssot_consumed_F_matches_snapshot": ss["consumed_F_matches_snapshot"],
        # FIREWALL (architectural lock): zero sibling imports anywhere; metabolic state carries no felt/HPA key
        "firewall_sibling_import_count": fw["sibling_import_count"],
        "firewall_python_files_scanned": fw["python_files_scanned"],
        "firewall_metabolic_state_takes_no_felt_input": fw["metabolic_state_takes_no_felt_input"],
        "firewall_holds": fw["firewall_holds"],
        # mind seam is a one-way forward-defer POINTER, not a dependency (consumes no mind value)
        "mind_is_one_way_pointer": mp["one_way_pointer"],
        "mind_consumes_a_value": mp["consumes_a_mind_value"],
        "mind_pointer_not_dependency": mp["pointer_not_dependency"],
    }
    return _res("DZS", "Cross-system seam WIRING on one NEW seam layer (no engine / disease change): the "
                "circulatory hepatic interface (Q_H = 1500 mL/min, E = 0.75, F = 0.25) -- circulatory is the SSOT "
                "owner by its CHARTER 'Seams OUT' -- is consumed as a VENDORED SNAPSHOT (verified against "
                "circulatory's hepatic_clearance() at vendoring, no sibling import) and becomes the DELIVERY "
                "SUBSTRATE on which the section-24 NAFLD/MASLD lipid load (insulin-resistance core reusing the s12 "
                "type-2 homeostat) and the section-25 biliary cholesterol (nucleation thermodynamics digestive-owned) "
                "sit, with the lipid-HANDLING and absolute-CSI scale handed across the firewall as [O]; the mind "
                "felt-symptom seam (visceral pain section 18, biliary colic section 25) is a ONE-WAY forward-defer "
                "POINTER carrying no consumed value; and the firewall is ENFORCED by an architectural lock -- ZERO "
                "sibling imports across all %d package python files and a metabolic state with no felt/HPA key -- the "
                "SAME lock mind runs neuro-side (mind has 0 neuro imports; neuro has 0 mind imports)"
                % fw["python_files_scanned"],
                v["passed"], val,
                "[V] the consumed circulatory hepatic interface (cited DOI 10.5281/zenodo.20754354 + named function, "
                "vendored faithfully) as the delivery substrate for the s24 / s25 readings, and the s12-homeostat reuse "
                "+ nucleation thermodynamics resting on it / [F] the firewall (zero sibling imports; the metabolic "
                "state takes no felt/HPA input; the metabolic state does not re-enter mind's HPA) and the mind one-way "
                "pointer / [O] the lipid-handling and absolute cholesterol-delivery magnitude (circulatory's, no "
                "primitive here) and the felt pain / affect (mind's, DOI 10.5281/zenodo.20694404, deferred by pointer)",
                obstacle="the hepatic lipid-HANDLING (triglyceride accumulation, NASH fibrosis) and the absolute "
                         "cholesterol-saturation-index scale are circulatory-owned -- this package consumes only the "
                         "perfusion / first-pass delivery substrate and keeps the s12 homeostat + crystallisation "
                         "thermodynamics; the FELT visceral pain (section 18) and FELT biliary colic (section 25) are "
                         "mind-owned, reached via mind's M18 interoception route (visceral afferents -> NTS -> insula / "
                         "cingulate, Saper 2002) and deferred OUT by a one-way pointer; the live cross-package harness "
                         "(running both sibling engines together) is the remaining integration step, while each package "
                         "verifies alone from its own zip with the siblings absent")

# --------------------------------------------------------------------------- DZA
def dza_analgesic_target_logic():
    """S28 -- the INHERITED analgesic target layer (analgesic_threshold_logic v2.0, DOI
    10.5281/zenodo.20733420), applied to digestive visceral pain. The 27-target firing-threshold
    reads re-verify bit-for-bit through THIS package's R19 spinodal/barrier (drift 0); the three
    intervention levers each RAISE the section-18 visceral-afferent firing threshold |h_sp| and
    LOWER the gain (back to baseline at full reversal); the GI burden prioritisation re-derives the
    inherited declared-weight score; the precision-visceral-LA map carries the four gut entry ports;
    and the fail-closed forbidden-claim scan is clean (no dose/efficacy/safety/synthesis claim)."""
    a = analg.validate()
    rv = a["reverify"]; gi = a["gi_subset"]; lv = a["lever_de_sensitisation"]
    pr = a["gi_prioritisation"]; px = a["precision_visceral"]; sc = a["forbidden_claim_scan"]
    val = {
        # inherit + re-verify through the digestive substrate (the crux: same R19 spinodal)
        "inherited_27_reads_reverify_drift_zero": rv["drift_zero"],
        "firing_threshold_closed_form_identity": rv["closed_form_identity_h_sp"],
        "n_gi_nociceptor_targets": gi["n_gi_targets"],
        # the central result: 3 levers, read on the section-18 afferent
        "hypersensitivity_amplification": lv["hypersensitivity_amplification"],
        "all_three_levers_raise_firing_threshold": lv["all_levers_raise_firing_threshold"],
        "all_three_levers_lower_afferent_gain": lv["all_levers_lower_gain"],
        "all_three_levers_return_gain_to_baseline": lv["all_levers_return_to_baseline"],
        # drug-class pointer + GI burden prioritisation (inherited weights, gamma NOT folded in)
        "n_visceral_pain_disorders_mapped": a["recommendation_map"]["n_disorders"],
        "gi_prioritisation_reproduces_inherited_score": pr["score_reproduces_inherited"],
        "gamma_not_folded_into_clinical_score": pr["gamma_not_folded_into_score"],
        "gi_prioritisation_top3": pr["top3"],
        # precision visceral LA + the fail-closed firewall scan
        "precision_visceral_entry_ports": list(px["entry_ports"]),
        "forbidden_claim_scan_clean": sc["clean"],
    }
    return _res("DZA", "S28 INHERITED analgesic target logic (analgesic_threshold_logic v2.0, DOI "
                "10.5281/zenodo.20733420) applied to digestive visceral pain: the 27 non-opioid target "
                "firing-threshold reads (gamma -> R19 |h_sp| = 2(g/3)^1.5) RE-VERIFY bit-for-bit through this "
                "package's own spinodal/barrier (drift 0 -- the analgesic firing-threshold scale IS the section-18 "
                "afferent spinodal); the three intervention levers (L1 reduce inward current / L2 open the K_V7 "
                "brake / L3 remove the NGF/CGRP sensitising drive) each RAISE the section-18 visceral-afferent "
                "firing threshold and LOWER the gain back toward baseline; the inherited burden-weighted "
                "prioritisation re-derives on the GI nociceptor subset (top: Na_V1.8, NGF, Na_V1.7) with gamma "
                "NEVER folded into the clinical score; a precision-visceral local-anaesthesia map pairs the four "
                "gut nociceptor entry ports with a charged firing-threshold raiser; and the fail-closed "
                "forbidden-claim scan finds no dose/efficacy/safety/synthesis claim",
                a["passed"], val,
                "[V] each lever raises the section-18 firing threshold / lowers the gain + the GI burden re-derivation / "
                "[F] the firing-threshold = spinodal-margin and gain-divergence R19 identity (drift 0 inheritance) + the "
                "declared-weight prioritisation + the precision-block mechanism SHAPE / [O] every clinical magnitude -- "
                "potency, dose, in-vivo selectivity, differential-block ratio, efficacy -- and the felt/affective pain (`mind`)",
                obstacle="every clinical magnitude (channel voltage, drug potency, dose, in-vivo selectivity, "
                         "differential-block ratio, absolute efficacy) is [O] -- the gamma read places the gene on the "
                         "firing-threshold scale but is never equated with any of them (firewall); the lever strength delta "
                         "is a STRUCTURAL fraction, not a dose (delta<->molecule/dose mapping [O]); and the felt/affective "
                         "pain is `mind`'s (this layer moves only the peripheral afferent-gain term)")

def dz14_remaining_in_substrate():
    d = dz.validate_d14()
    a = d["d14a_dyssynergic_defecation"]["dyssynergic"]
    b = d["d14b_hirschsprung"]["hirschsprung"]
    c = d["d14c_mody"]["mody"]
    e = d["d14d_hepatic_gsd"]["hepatic_gsd"]
    f = d["d14e_autoimmune_gastritis"]["autoimmune_gastritis"]
    val = {
        # D14a dyssynergic defecation: s16 gate at the anorectal outlet; bolus retained when the gate stays closed, drive intact
        "dyssynergic_clears_when_relaxation_competent": a["clears_when_relaxation_competent"],
        "dyssynergic_retained_when_relaxation_fails": a["retained_when_relaxation_fails"],
        "dyssynergic_retained_when_paradoxical_contraction": a["retained_when_paradoxical_contraction"],
        "dyssynergic_lesion_is_gate_not_drive": a["lesion_is_gate_not_drive"],
        # D14b Hirschsprung: segmental aganglionosis blocks transit, distal zone never traversed, bolus retained proximal
        "hirschsprung_transit_blocked_monotone": b["transit_blocked_monotone_with_length"],
        "hirschsprung_distal_zone_never_traversed": b["distal_aganglionic_zone_never_traversed"],
        "hirschsprung_bolus_retained_proximal": b["bolus_retained_proximal_at_transition"],
        # D14c MODY: targeted secretory lesion -> a distinct, stable, regulated curve (NOT the T1 runaway)
        "mody_regulated_returns_to_setpoint": c["regulated_returns_to_setpoint"],
        "mody_distinct_from_t1_runaway": c["distinct_from_t1_runaway"],
        "mody_fasting_mM": c["fasting_mM"],
        # D14d hepatic GSD-I: crippled glycogen-buffer release -> fasting hypoglycaemia + failed counter-reg
        "gsd_fasting_drifts_hypoglycaemic": e["fasting_drifts_hypoglycaemic_as_output_falls"],
        "gsd_counter_regulation_fails": e["counter_regulation_fails_when_buffer_crippled"],
        # D14e autoimmune gastritis: corpus-localised flare drops barrier + acid (coupled); suppression recovers
        "aig_corpus_barrier_and_acid_drop": f["corpus_barrier_and_acid_drop_on_ignition"],
        "aig_acid_coupled_to_corpus_barrier": f["acid_output_coupled_to_corpus_barrier"],
        "aig_suppression_recovers": f["suppression_recovers_corpus_and_acid"],
    }
    return _res("DZ14", "REMAINING in-substrate Tier-1 surface (sections 1A-1D) closed by REUSING validated modules / "
                "primitives with NO new primitive and NO sibling package: dyssynergic defecation (the s16 gate read at "
                "the anorectal outlet -- the achalasia mirror; bolus retained when the outlet stays closed while the "
                "propulsive drive is intact, the gate-not-drive distinction from colonic inertia), Hirschsprung motility "
                "consequence (a segmental aganglionic distal segment = absent oscillators on the s1 emergence + s4 "
                "transport blocks aboral clearance progressively, never traverses the deep aganglionic zone, and retains "
                "the bolus proximal at the transition zone = proximal dilatation; RET gene-key -> disease_wp), MODY "
                "trajectory (a targeted partial beta-secretory lesion on the s12 homeostat -> a distinct, stable, "
                "REGULATED elevated curve distinct from the s12 type-1 catastrophic runaway; PDX1/HHEX gene-key -> "
                "disease_wp), hepatic GSD-I counter-reg consequence (a crippled hepatic glycogen-buffer release arm on "
                "the s6 loop -> fasting glucose drifts hypoglycaemic and a hypoglycaemia challenge can no longer be "
                "returned to the setpoint; G6PC gene-key -> disease_wp), and autoimmune gastritis (the s22 relapsing-"
                "inflammation flare read CORPUS-LOCALISED + the s7 barrier -> a regional barrier lesion + an acid-output "
                "drop coupled to it, with driver suppression recovering both)",
                d["passed"], val,
                "[V] every emergent mechanism (gate-at-outlet retention, segmental block + proximal retention, the "
                "distinct regulated MODY curve, the GSD fasting drift + failed counter-reg, the corpus barrier + acid "
                "drop) / [L] the PDX1/HHEX and G6PC gene links (cited from DNA, gene-key -> disease_wp) / [O] felt and "
                "absorptive magnitudes",
                obstacle="felt straining/pain (-> `mind`), absolute evacuation/transit/glucose scales, the B12/iron "
                         "malabsorption magnitude (absorption layer), and the autoimmune-gastritis carcinoid boundary "
                         "(`disease_wp`) all need clinical calibration; the three gene-key items (Hirschsprung RET, MODY "
                         "PDX1/HHEX, GSD G6PC) are imported-lesion seams owned by `disease_wp` with the consequence "
                         "dynamics owned here")


SUITES += [dz1_dysrhythmia_gastroparesis, dz2_diabetes_spectrum, dz3_gastritis_ulcer,
           dz4_intestinal_motility, dz5_scattered_tier1, dz6_sphincter_gate,
           dz7_accommodation_reservoir, dz8_ibs_afferent_gain,
           dz9_immune_ibd, dz10_exocrine_pancreatitis,
           dz11_perfusion_ischemia, dz12_hepatobiliary_bile, dz13_structural_wall,
           dz14_remaining_in_substrate,
           dzs_cross_system_seams,
           dza_analgesic_target_logic,
           dzd_disease_determinism]

def run_battery():
    base = eng.circulate()
    results = {"emergence_ok": bool(base["organs"]["organs"]),
               "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values())
                                  if base["oscillators"] else False),
               "suites": [fn() for fn in SUITES]}
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in results["suites"])
    return results

if __name__ == "__main__":
    r = run_battery(); print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
