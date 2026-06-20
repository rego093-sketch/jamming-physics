#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  Digestive / Metabolic RESEARCH entry point.
Drop the package into a fresh chat and run:  python repro/run_all.py
Emerges organs from measured gamma, circulates dynamics (what exists so far), runs the stress battery
+ oncology status, writes results to reports/, and reports whether WRITING is unlocked. Builds no HTML.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_oncology", "_disease", "_seams", "_analgesic", "_harness"):
    sys.path.insert(0, os.path.join(_HERE, sub))
sys.path.insert(0, os.path.join(_HERE, "..", "inherited"))
import importlib
eng    = importlib.import_module("vp_dig_engine")
stress = importlib.import_module("stress_tests")
gates  = importlib.import_module("gates")
onco   = importlib.import_module("carcinogen_dose_response")
dz     = importlib.import_module("disease_modules")
seam   = importlib.import_module("seam_wiring")
analg  = importlib.import_module("analgesic_logic")
harness = importlib.import_module("cross_package_harness")

def main():
    print("=" * 78)
    print("Digestive / Metabolic  --  RESEARCH PHASE (writing is locked until gates are green)")
    print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] ORGAN EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-11s <- %-8s %s  [%s]  %s" % (o["organ"], o["master"], tag, o["dyn_class"], o["role"]))
    print("    developmental order (gamma asc): %s" % res["organs"]["gamma_order_ascending"])

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    for name, v in res["oscillators"].items():
        print("    %-11s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    print("\n[3] STRESS BATTERY")
    batt = stress.run_battery()
    for su in batt["suites"]:
        print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[4] ONCOLOGY (carcinogen dose-response)")
    for s2 in onco.status()["sites"]:
        print("    %-24s <- %s" % (s2["site"], s2["carcinogens"]))
    print("    status: %s" % onco.status()["status"])

    print("\n[4+] C6 NEOPLASTIC EXTENSION (same barrier-Kramers kernel; metaplasia step + synergy + reversibility)")
    c6 = onco.validate_c6()
    eac = c6["metaplasia"]["eac"]; gca = c6["metaplasia"]["gca_int"]
    print("     metaplasia: Barrett's->EAC precursor RR=%.1f (rate-limiting=%s), gastric IM RR=%.1f; dysplasia ladder accelerates=%s; ablation/eradication lowers next-step rate=%s"
          % (eac["rr_metaplastic"], eac["rate_limiting"], gca["rr_metaplastic"],
             eac["ladder_accelerating"], eac["treatment_lowers_rate"]))
    hcc = c6["synergy"]["hcc"]; escc = c6["synergy"]["escc"]
    print("     synergy: HCC HBVxaflatoxin joint RR=%.1f (cited ~%.0f) super-additive=%s sub-multiplicative-predicted=%s; ESCC smokexalcohol joint RR=%.1f (cited ~%.0f) super-additive=%s"
          % (hcc["RR_joint"], hcc["cited_joint"], hcc["super_additive"], hcc["sub_multiplicative_prediction"],
             escc["RR_joint"], escc["cited_joint"], escc["super_additive"]))
    print("     reversible: gastric MALT regresses on g-restore=%s (RR %.1f->1.0 on eradication); single-driver: anal SCC monotone in HPV bias=%s"
          % (c6["malt"]["reversible_on_g_restore"], c6["malt"]["RR_Hp"], c6["anal"]["monotone"]))
    print("     out-of-kernel (honest [O]): %s" % ", ".join(o["site"] for o in c6["out_of_kernel"]))
    print("     C6 passed=%s | digest 2xsha256=%s..." % (c6["passed"], onco.c6_digest()[1][:12]))

    print("\n[5] DISEASE MODULES (Tier-1 perturbations of validated modules; phenotype emerges, never fitted)")
    dv = dz.validate()
    d1 = dv["d1_dysrhythmia_gastroparesis"]; d2 = dv["d2_diabetes"]; d3 = dv["d3_gastritis_ulcer"]
    tachy = d1["ectopic"]["fast_focus_coupled_cpm"]
    print("    D1 dysrhythmia+gastroparesis  pass=%s | bands brady/normal/tachy=%s, ectopic tachy=%.1f cpm, severe-depletion emptying=%.0f%% of normal"
          % (d1["passed"], d1["dysrhythmia"]["spans_brady_normal_tachy"], tachy,
             d1["gastroparesis"]["severe_depletion_pct_of_normal"]))
    print("    D2 diabetes T1/T2 spectrum    pass=%s | T1 deepest fasting=%.1f mM (catastrophic), T2 deepest=%.1f mM (compensated), gap widens=%s"
          % (d2["passed"], d2["t1_capacity"]["deepest_fasting"], d2["t2_sensitivity"]["deepest_fasting"], d2["axes_distinct"]))
    print("    D3 gastritis/ulcer            pass=%s | NSAID erosion anchor hit=%s, gastric ulcer RR=%.0f (defence), duodenal RR=%.0f (acid), shares s10 g_Hp=%s"
          % (d3["passed"], d3["erosion"]["anchor_hit"], d3["ulcer_site_split"]["gastric"]["RR"],
             d3["ulcer_site_split"]["duodenal"]["RR"], d3["continuum"]["same_g_as_cancer_step"]))
    d4 = dv["d4_intestinal_motility"]; un = d4["icc_unifying"]["density_axis"]
    print("    D4 intestinal motility        pass=%s | drive axis slow-transit→inertia collapse=%s, CIPO functional-obstruction=%s, ileus reversible=%s"
          % (d4["passed"], d4["slow_transit_and_inertia"]["inertia_collapse_below_threshold"],
             d4["cipo"]["functional_obstruction_lumen_patent"], d4["ileus"]["reversible_scales_with_duration"]))
    print("       unifying ICC lesion: stomach %.0f%%→%.0f%% and gut %.0f%%→%.0f%% over density 1.0→0.1 (one cause, two sites)"
          % (un[0][1], un[-1][1], un[0][2], un[-1][2]))
    d5 = dv["d5_scattered_tier1"]
    d5a = d5["d5a_dumping"]; d5c = d5["d5c_insulinoma_reactive_hypo"]
    d5d = d5["d5d_functional_dyspepsia_motility"]; d5e = d5["d5e_sibo_stasis"]
    print("    D5 scattered Tier-1           pass=%s | dumping early-peak↑ + late biphasic→hypo=%s (mechanical magnitude honest [O]),"
          % (d5["passed"], d5a["late_dumping"]["biphasic"] and d5a["late_dumping"]["fast_delivery_crosses_hypo"]))
    print("       reflux erosion shares s13 kernel=%s, insulinoma mirror-of-T1 deepest fasting=%.2f mM + resection-recovers=%s,"
          % (d5["d5b_reflux_esophagitis"]["erosion"]["convex"], d5c["insulinoma"]["deepest_fasting"], d5c["insulinoma"]["recovers_on_resection"]))
    print("       FD mild emptying=%.0f%% (distinct from severe gastroparesis 24%%), SIBO retention rises as drive falls=%s"
          % (d5d["fd_motility"]["mild_emptying_pct"], d5e["sibo"]["retention_monotone_rises_as_drive_falls"]))
    d6 = dv["d6_sphincter_gate"]
    g6 = d6["d6a_gerd"]["gerd"]; b6 = d6["d6b_achalasia"]["achalasia"]
    s6 = d6["d6c_esophageal_spasm"]["spasm"]; o6 = d6["d6d_sphincter_of_oddi"]["oddi"]
    print("    D6 sphincter-gate (NEW prim)  pass=%s | GERD reflux %d->%d events as tone 1.2->0.05 (continent->incompetent);"
          % (d6["passed"], g6["rows"][0][1], g6["rows"][-1][1]))
    print("       achalasia: gate stuck closed -> stasis (the GERD mirror) + aperistalsis transit %.0f%%; spasm: coordination-loss"
          % (b6["aperistalsis"][-1][1]))
    print("       collapses transit to %.0f%% and amplitude cannot rescue=%s; Oddi: stuck-gate outflow obstruction=%s"
          % (s6["coordination_axis"][-1][1], s6["amplitude_cannot_rescue"], o6["outflow_obstructs_when_gate_stuck"]))
    d7 = dv["d7_accommodation_reservoir"]; cv7 = d7["accommodation"]
    print("    D7 accommodation reservoir (NEW prim)  pass=%s | FD post-prandial distress: impaired accommodation -> meal pressure %.0f%% of stiff baseline"
          % (d7["passed"], 100.0 * cv7["fd_pressure"] / cv7["baseline_stiff_pressure"]))
    print("       compliance falls as accommodation falls (early satiation)=%s; yield point = R19 spinodal (exact)=%s; treatment raises compliance -> lowers pressure=%s"
          % (cv7["compliance_falls_as_accommodation_falls"], d7["yield_identity"]["yield_is_r19_spinodal"],
             d7["treatment_axis"]["raising_compliance_lowers_pressure"]))
    d8 = dv["d8_afferent_gain"]; sub8 = d8["ibs_subtype"]; hs8 = d8["visceral_hypersensitivity"]; idn8 = d8["gain_identity"]
    print("    D8 afferent gain (NEW prim)  pass=%s | IBS subtype by transport bias: retained C=%.2f -> M=%.2f -> D=%.2f (ordered=%s; rapid magnitude saturates at s15 ceiling=%s)"
          % (d8["passed"], sub8["ibs_c_retained"], sub8["ibs_m_retained"], sub8["ibs_d_retained"],
             sub8["subtypes_ordered_C_M_D"], sub8["rapid_magnitude_saturates"]))
    print("       visceral hypersensitivity: afferent gain rises + allodynia (same distension x%.2f signal)=%s, provoked->spontaneous firing past yield=%s; functional abdominal pain rises at normal motility=%s"
          % (hs8["allodynia_amplification"], hs8["signal_rises_allodynia"],
             hs8["spontaneous_firing_past_spinodal"], d8["functional_abdominal_pain"]["pain_proxy_rises_at_normal_motility"]))
    print("       identity: afferent gain == s17 fundic compliance (1/k, exact)=%s; gain diverges at the R19 spinodal = the s17 reservoir yield=%s; felt pain -> mind (firewall)"
          % (idn8["gain_is_b2_compliance"], idn8["gain_diverges_at_r19_spinodal"]))
    d9 = dv["d9_immune_ibd"]; rc9 = d9["relapsing_course"]; nb9 = d9["neoplasia_bridge"]
    print("    D9 immune relapsing-inflammation (NEW prim)  pass=%s | IBD relapsing-remitting hysteresis=%s; induction needs suppression past antigen+spinodal (thr=%.3f) but a LOWER maintenance dose (thr=%.3f) holds remission (induction/maintenance asymmetry)"
          % (d9["passed"], rc9["relapsing_hysteresis"], rc9["induction_threshold"], rc9["maintenance_threshold"]))
    print("       burden->barrier->cancer bridge: cumulative inflammation lowers the SAME s7 barrier -> colitis-CRC RR 1.0->%.1f (anchor hit=%s), collapses to 1.0 on sustained suppression=%s; closes the s21 small-bowel boundary=%s"
          % (nb9["burden_rr"][-1][2], nb9["anchor_hit"], nb9["suppression_collapses_rr"], nb9["closes_small_bowel_boundary"]))
    print("       same element, antigen regime: celiac flares on gluten + remits gluten-free (driver removal -> barrier recovery)=%s; felt/affective -> mind (firewall); absolute incidence + celiac absorptive magnitude [O]"
          % (d9["same_layer"]["shared_lever_remove_driver_restores_barrier"]))
    d10 = dv["d10_exocrine_pancreatitis"]; aa10 = d10["acute_autocatalysis"]; ce10 = d10["chronic_epi"]
    print("    D10 exocrine autocatalysis (NEW prim)  pass=%s | acute pancreatitis: autoactivation threshold rises with inhibitor (=%.3f at baseline); sub-threshold safe + supra-threshold LATCHES=%s"
          % (d10["passed"], aa10["activation_threshold"], aa10["subthreshold_safe"] and aa10["suprathreshold_latches"]))
    print("       pre-threshold removal prevents but an established attack is IRREVERSIBLE to any parameter move=%s (only a strong inhibitor past spinodal abolishes the basin=%s) -- pre-threshold-only intervention"
          % (aa10["pre_threshold_intervention_prevents"] and aa10["post_threshold_irreversible"], aa10["strong_inhibitor_reversible"]))
    print("       chronic EPI: large secretory reserve (steatorrhea only past ~90%% acinar loss)=%s; PERT restores output above demand=%s; CFTR gene-key -> disease_wp; absolute trigger/demand scales [O]"
          % (ce10["large_reserve_steatorrhea_only_past_90pct_loss"], ce10["pert_restores_adequacy"]))
    d11 = dv["d11_perfusion_ischemia"]; cm11 = d11["chronic_mesenteric"]; ai11 = d11["acute_ischemia"]
    print("    D11 perfusion-viability (NEW prim)  pass=%s | chronic mesenteric ischaemia (intestinal angina): perfusion margin falls as post-prandial demand rises + crosses to deficit=%s, revascularization restores margin=%s"
          % (d11["passed"], cm11["crosses_to_deficit_postprandially"], cm11["revascularization_restores_margin"]))
    print("       acute occlusion flips viable->ischaemic past demand-spinodal (thr=%.3f) + time-critical salvage window=%.3f: reperfusion within window recovers=%s, partial/late stays infarcted=%s (structural infarct [O])"
          % (ai11["flip_threshold"], ai11["reserve_window"], ai11["reperfusion_recovers_within_window"], ai11["partial_reperfusion_stays_ischemic"]))
    print("       NAFLD/MASLD overlap reuses s12 type-2 gain-loss homeostat (no refit)=%s; lipid-deposition layer = circulatory seam=%s"
          % (d11["nafld"]["insulin_resistance_reuses_s12_type2_gain_loss"], d11["nafld"]["lipid_handling_is_circulatory_seam"]))
    d12 = dv["d12_hepatobiliary_bile"]; ch12 = d12["cholelithiasis"]; ds12 = d12["dissolution"]
    print("    D12 supersaturation/nucleation (NEW prim)  pass=%s | cholelithiasis: bile supersaturation (CSI>1) is METASTABLE not sufficient=%s, nucleates only past 1+spinodal (CSI=%.3f, the Kramers barrier)"
          % (d12["passed"], ch12["supersaturation_metastable_not_sufficient"], ch12["nucleation_csi"]))
    print("       dissolution hysteresis: a formed stone persists below saturation=%s + redissolves only far below it=%s -> UDCA works only on small early stones (gap=%.3f)"
          % (ds12["stone_persists_below_saturation"], ds12["redissolves_only_far_below_saturation"], ds12["hysteresis_gap"]))
    print("       seams: gallbladder stasis = B1 gate=%s; cholecystitis = B1 gate + C1 flare=%s; circulatory (cholesterol) + mind (biliary colic) seams declared; absolute CSI scale [O]"
          % (d12["seams"]["stasis_is_b1_gate_seam"], d12["seams"]["cholecystitis_is_b1_gate_plus_c1_flare"]))
    d13 = dv["d13_structural_wall"]; dp13 = d13["diverticular_pressure"]; ws13 = d13["wall_strength"]; tb13 = d13["treatment_boundary"]
    print("    D13 wall-mechanics (NEW prim)  pass=%s | diverticular disease: Laplace P=tension/radius rises as radius falls=%s, herniates past P=spinodal(g_wall) at low-fibre small radius=%s (thr=%.3f)"
          % (d13["passed"], dp13["laplace_pressure_rises_as_radius_falls"], dp13["herniates_at_low_fibre_small_radius"], dp13["herniation_threshold"]))
    print("       weaker wall (aging/collagen disorder) has a lower threshold -> herniates at a fixed pressure a normal wall withstands=%s (age-rising prevalence); fibre treatment drops P below threshold=%s"
          % (ws13["weaker_wall_herniates_at_same_pressure"], tb13["fibre_lowers_pressure_below_threshold"]))
    print("       diverticulITIS = cited C1 flare seam=%s; mechanical fixed-block obstruction (hernia/volvulus/intussusception/adhesions) = s14 functional counterpart=%s (surgical, out-of-model); absolute pressure/strength scales [O]"
          % (tb13["diverticulitis_is_c1_flare_seam"], tb13["mechanical_block_is_s14_excluded_counterpart"]))
    d14 = dv["d14_remaining_in_substrate"]
    dsy = d14["d14a_dyssynergic_defecation"]["dyssynergic"]; hir = d14["d14b_hirschsprung"]["hirschsprung"]
    mod = d14["d14c_mody"]["mody"]; gsd = d14["d14d_hepatic_gsd"]["hepatic_gsd"]; aig = d14["d14e_autoimmune_gastritis"]["autoimmune_gastritis"]
    print("    D14 remaining in-substrate (NO new prim; closes Tier-1 surface)  pass=%s | dyssynergic defecation = s16 gate at the anorectal OUTLET (achalasia mirror): bolus retained when relaxation fails=%s + when paradoxically contracted=%s, propulsive DRIVE intact=%s (gate-not-drive vs colonic inertia)"
          % (d14["passed"], dsy["retained_when_relaxation_fails"], dsy["retained_when_paradoxical_contraction"], dsy["lesion_is_gate_not_drive"]))
    print("       Hirschsprung = s1 emergence + s4 segmental aganglionosis (absent oscillators): transit blocked monotone with dead-segment length=%s, deep aganglionic zone never traversed=%s, bolus retained proximal at transition=%s (proximal dilatation); RET gene-key -> disease_wp"
          % (hir["transit_blocked_monotone_with_length"], hir["distal_aganglionic_zone_never_traversed"], hir["bolus_retained_proximal_at_transition"]))
    print("       MODY = s12 homeostat targeted partial beta-secretory lesion (PDX1/HHEX gene-key -> disease_wp): a DISTINCT stable REGULATED curve (fasting=%.2f mM, returns to setpoint=%s) distinct from the s12 type-1 catastrophic runaway=%s"
          % (mod["fasting_mM"], mod["regulated_returns_to_setpoint"], mod["distinct_from_t1_runaway"]))
    print("       hepatic GSD-I = s6 crippled glycogen-buffer RELEASE (G6PC gene-key -> disease_wp): fasting glucose drifts hypoglycaemic as hepatic output falls=%s, counter-regulation can no longer return to setpoint=%s (failed counter-reg)"
          % (gsd["fasting_drifts_hypoglycaemic_as_output_falls"], gsd["counter_regulation_fails_when_buffer_crippled"]))
    print("       autoimmune gastritis = s22 CORPUS-localised flare + s7 barrier: regional corpus barrier + acid output drop together=%s, acid coupled to corpus/parietal scale=%s (achlorhydria), driver suppression recovers both=%s; B12/iron malabsorption + carcinoid boundary [O]"
          % (aig["corpus_barrier_and_acid_drop_on_ignition"], aig["acid_output_coupled_to_corpus_barrier"], aig["suppression_recovers_corpus_and_acid"]))
    print("    disease layer 2xsha256 deterministic: %s  (sha=%s...)" % (len({dz.digest()[1] for _ in range(2)}) == 1, dz.digest()[1][:12]))

    print("\n[5+] CROSS-SYSTEM SEAM WIRING (NEW seam layer; engine + disease digests UNCHANGED)")
    sv = seam.validate_seams(); hep = sv["circulatory_hepatic_interface"]; fw = sv["firewall"]; mp = sv["mind_pointer"]
    print("     circulatory hepatic interface CONSUMED (vendored snapshot, no sibling import): Q_H=%.0f mL/min, E=%.2f, F=%.2f  <- owner %s (SSOT, DOI %s)"
          % (hep["Q_H_ml_min"], hep["E"], hep["F"], hep["owner"], hep["owner_doi"]))
    print("     s24 NAFLD/MASLD: insulin-resistance core reuses s12 type-2 homeostat=%s; lipid DEPOSITION rests on consumed circulatory perfusion=%s; lipid HANDLING [O] (circulatory)"
          % (sv["s24_nafld_delivery"]["reuses_s12_type2_gain_loss"], sv["s24_nafld_delivery"]["delivery_rests_on_consumed_circulatory"]))
    print("     s25 bile: nucleation thermodynamics digestive-owned (CSI=%.3f); cholesterol DELIVERY rests on consumed circulatory perfusion=%s; absolute CSI scale [O] (circulatory)"
          % (sv["s25_bile_delivery"]["nucleation_csi"], sv["s25_bile_delivery"]["delivery_rests_on_consumed_circulatory"]))
    print("     mind felt-symptom seam (visceral pain s18, biliary colic s25): one-way forward-defer POINTER=%s, consumes a mind value=%s -> mind M18 interoception route (owner DOI %s)"
          % (mp["one_way_pointer"], mp["consumes_a_mind_value"], mp["owner_doi"]))
    print("     FIREWALL (architectural lock, the SAME lock mind runs neuro-side): sibling imports across %d package files = %d; metabolic state takes no felt/HPA input=%s; firewall holds=%s"
          % (fw["python_files_scanned"], fw["sibling_import_count"], fw["metabolic_state_takes_no_felt_input"], fw["firewall_holds"]))
    print("     seams passed=%s | SSOT consistent=%s | seam layer 2xsha256=%s..." % (sv["passed"], sv["ssot_consistency"]["ssot_consistent"], seam.digest()[1][:12]))

    print("\n[5++] ANALGESIC TARGET LAYER -- INHERITED (analgesic_threshold_logic v2.0; engine + disease digests UNCHANGED)")
    av = analg.validate(); rv = av["reverify"]; lv = av["lever_de_sensitisation"]; pr = av["gi_prioritisation"]
    print("     INHERIT + RE-VERIFY (DOI %s): %d non-opioid target firing-threshold reads re-derive through THIS package's R19 spinodal/barrier, |h_sp| drift=%.1e barrier drift=%.1e -> drift_zero=%s"
          % (rv["concept_doi"], rv["n_targets"], rv["max_h_sp_drift"], rv["max_barrier_drift"], rv["drift_zero"]))
    print("     the analgesic firing-threshold scale IS the section-18 afferent spinodal -> %d GI nociceptor targets across L1/L2/L3" % av["gi_subset"]["n_gi_targets"])
    print("     3 levers on the section-18 afferent (sensitised gain x%.2f): all RAISE the firing threshold=%s + all LOWER the gain back to baseline=%s (L1 reduce inward / L2 open K_V7 / L3 remove NGF-CGRP drive)"
          % (lv["hypersensitivity_amplification"], lv["all_levers_raise_firing_threshold"], lv["all_levers_lower_gain"] and lv["all_levers_return_to_baseline"]))
    print("     drug-class POINTER for %d visceral-pain disorders (IBS, FAP, FD pain, biliary colic, oesophageal spasm); GI burden prioritisation top3=%s (declared weights, gamma NOT folded into score=%s)"
          % (av["recommendation_map"]["n_disorders"], pr["top3"], pr["gamma_not_folded_into_score"]))
    print("     FIREWALL: every clinical magnitude (potency/dose/selectivity-in-vivo/differential-block/efficacy) [O]; felt pain `mind`; forbidden-claim scan clean=%s; analgesic layer 2xsha256=%s..."
          % (av["forbidden_claim_scan"]["clean"], analg.digest()[1][:12]))
    print("     analgesic layer passed=%s" % av["passed"])

    print("\n[6] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked()
    print("    WRITING LOCKED: %s  (%s)" % (locked, why))

    print("\n[6+] CROSS-PACKAGE HARNESS (out-of-gate; verify-alone preserved -- NOT part of any gate)")
    hc = harness.digestive_side_contract(); _hs, hh = harness.digest()
    print("     in-package cross-package CONTRACT (computed from THIS archive alone, siblings ABSENT):")
    print("       shared-substrate closed-form identity |h_sp|=(2/3 sqrt3) g^1.5 holds at all 27 map gammas=%s; barrier g^2/4"
          % hc["substrate"]["closed_form_identity_ok"])
    print("       inherited 27-target analgesic map re-derives through THIS spinodal, drift_zero=%s (|h_sp| drift=%.1e)"
          % (hc["analgesic_map"]["drift_zero"], hc["analgesic_map"]["max_h_sp_drift"]))
    print("       circulatory hepatic snapshot consumed (vendored, no import): Q_H=%.0f E=%.2f F=%.2f; neuro felt-symptom endpoint SCN9A in map=%s"
          % (hc["circulatory_seam"]["vendored_Q_H_ml_min"], hc["circulatory_seam"]["vendored_E"],
             hc["circulatory_seam"]["vendored_F"], hc["neuro_endpoint"]["scn9a_in_map"]))
    print("     harness 2xsha256=%s...  (digest is sibling-independent: identical whether or not siblings are on disk)" % hh[:12])
    print("     the LIVE cross-volume check (loads circulatory+musculoskeletal+neuro engines in one process) is SEPARATE:")
    print("       run  python repro/run_harness.py  with the sibling packages present. It is OUTSIDE the gate and")
    print("       cannot affect this sibling-free research run or the canonical build (each volume verifies alone).")

    print("\nNext: build out _engine dynamics + _verify sweeps + _oncology anchors until all_green,")
    print("then gates.write_research_complete(), set PHASE=writing, and only THEN run tools/build_docs.py.")

if __name__ == "__main__":
    main()
