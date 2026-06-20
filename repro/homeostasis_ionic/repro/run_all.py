#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py  --  Mineral / Acid-Base / Electrolyte Homeostasis RESEARCH entry. Drop into a fresh chat:
    python repro/run_all.py
Emerges nodes from MEASURED gamma, runs the setpoint LOOPS (RI1-RI5) + the substrate gain/OU laws, the
SENSORY seam, the LITERATURE cross-checks, the PATHOLOGY failure laws, and the FUNDAMENTAL therapy
simulations, then prints the gate / writing-lock status. HTML is not built here."""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_pathology", "_therapy"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng=importlib.import_module("vp_ion_engine"); loops=importlib.import_module("vp_loops")
stress=importlib.import_module("stress_tests"); gates=importlib.import_module("gates")
path=importlib.import_module("setpoint_failure"); sensors=importlib.import_module("vp_sensors")
lit=importlib.import_module("literature_anchors"); ther=importlib.import_module("fundamental_therapy")
renal=importlib.import_module("renal_phosphate"); frontier=importlib.import_module("frontier_quant")
comp=importlib.import_module("comparative_ionoregulation")
t2dis=importlib.import_module("tier2_ion_diseases")
trans=importlib.import_module("transport_dynamics")
cgam=importlib.import_module("comparative_gamma")
tlever=importlib.import_module("three_lever")
drem=importlib.import_module("disease_remediation")

def main():
    print("="*82); print("Mineral / Acid-Base / Electrolyte Homeostasis  --  RESEARCH PHASE"); print("="*82)
    res=eng.circulate(); s,h=eng.emit(res)
    reports=os.path.join(_HERE,"..","reports"); os.makedirs(reports,exist_ok=True)
    open(os.path.join(reports,"emergence_results.json"),"w",encoding="utf-8").write(s)

    print("\n[1] NODE EMERGENCE (from MEASURED gamma; NCBI promoters, SantaLucia 1998; never fitted)")
    for o in res["organs"]["organs"]:
        g=o.get("gamma"); tag=("g="+str(g)) if g is not None else o.get("note","")
        print("    %-26s <- %-7s %-10s [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"): print("    gamma TO-MEASURE: %s" % res["organs"]["deferred_gamma"])

    print("\n[2] SUBSTRATE LAWS (gamma -> loop stiffness; OU setpoint statistics)")
    L=loops.run_loops()
    gl=L["gain_law"]; print("    barrier(gamma) monotone up: %s ; pulse-displacement monotone down: %s  -> gamma sets loop stiffness k" %
                            (gl["barrier_monotone_increasing_in_gamma"], gl["displacement_monotone_decreasing_in_gamma"]))
    ol=L["ou_law"]; print("    OU laws: Var=sigma^2/2k %s ; step error=load/k %s ; integral arm zeroes error %s" %
                          (ol["variance_law_Var_eq_sigma2_over_2k"], ol["rejection_law_err_eq_load_over_k"], ol["integral_arm_zeroes_steady_error"]))

    print("\n[3] STRESS BATTERY (RI1-RI5; disturbance rejection / two-timescale / trade-off / threshold)")
    batt=stress.run_battery()
    for su in batt["suites"]: print("    %-4s [%-4s] %s" % (su["target"], su["status"], json.dumps(su["value"])))
    print("    substrate laws ok: %s ; ALL TARGETS PASS: %s" % (batt["substrate_laws_ok"], batt["all_targets_pass"]))

    print("\n[4] SENSORY SEAM (homeostatic sensors = sensory-cell transducers; measured sensor gamma)")
    sc=sensors.status()["instrument_check"]
    print("    all measured sensors valid R19 instruments: %s ; sharpness monotone in gamma: %s" %
          (sc["all_valid_bistable"], sc["barrier_monotone_in_gamma"]))
    print("    crown jewel: OTOP1 = sour-taste receptor AND otoconia(CaCO3) pH-keeper -> acid-base<->mineral<->vestibular; BPPV at the seam")

    print("\n[5] LITERATURE CROSS-CHECKS (cited anchors [L]/[F] vs simulated [V])")
    cc=lit.status()
    for c in cc["cross_checks"]: print("    %-12s %-44s -> %s" % (c["anchor"], c["cited"][:44], c["verdict"]))
    print("    all cross-checks consistent: %s" % cc["all_cross_checks_consistent"])

    print("\n[6] PATHOLOGY (disease = failure of setpoint/clock/sense-organ on R19; 6 modes)")
    ps=path.status(); print("    derived failure laws demonstrated: %s" % ps["laws_demonstrated"])
    for f in ps["failures"]: print("    %-46s <- %s" % (f["site"], f["mode"]))

    print("\n[7] FUNDAMENTAL THERAPY (root-directed; keyed to failure mode)")
    ts=ther.status()
    t1=ts["simulations"]["T1_setpoint_reset"]; t2=ts["simulations"]["T2_reservoir_refill"]
    print("    T1 set-point reset normalizes defended value: %s (%.3f -> %.3f)" % (t1["normalized"], t1["defended_untreated"], t1["defended_treated"]))
    print("    T2 reservoir: anabolic refill %.2f > anti-resorptive %.2f > untreated %.2f (anabolic beats: %s)" %
          (t2["anabolic_final"], t2["antiresorptive_final"], t2["untreated_final"], t2["anabolic_beats_antiresorptive"]))
    print("    demonstrations pass: %s ; frontier hypotheses: %d (ALL FOUR now quantified [V] -> see [9])" % (ts["demonstrations_pass"], len(ts["frontier_hypotheses"])))

    print("\n[8] RENAL PHOSPHATE THRESHOLD (TmP/GFR) -- closing the RI5 absolute-maximum [O] with exact algebra)")
    rp=renal.status()
    for k in ("high_fgf23_XLH","normal","low_fgf23_hypoPTH"):
        c=rp["cases"][k]; print("    %-20s TmP/GFR=%.3f mmol/L  TRP=%.3f  in-ref:%s" % (k, c["TmP_GFR_mmol_L"], c["TRP"], c["in_reference_range"]))
    print("    normal in reference [0.80-1.35]: %s ; FGF23 LOWERS the threshold (XLH<normal<hypoPTH): %s" %
          (rp["normal_in_reference"], rp["threshold_falls_with_fgf23"]))
    print("    residual [O]: gamma sets STABILITY not the VALUE -> absolute TmP/GFR is [CAL]/[F], not gamma-derived (by design)")

    print("\n[9] FRONTIER QUANT (all FOUR [H] hypotheses given a reproduced MECHANISM; magnitudes stay [O])")
    fq=frontier.status(); hr=fq["H_RESET"]; hd=fq["H_DUAL"]; ha=fq["H_ARM"]; ho=fq["H_OTOC"]
    print("    H-RESET sensor reset  defended attractor == comparator set-point for ALL Hill slopes (%s): reset durable, symptom relapses [V] direction" %
          "/".join(hr["sensor_family"]))
    print("    H-DUAL  window area   dual=%.2f > single=%.2f > untreated=%.2f  (%.1fx; single window closes) [V] ordering" %
          (hd["integrated_window_dual"], hd["integrated_window_single"], hd["integrated_window_untreated"], hd["dual_over_single_ratio"]))
    print("    H-ARM   arm restore   variance buffer/restore=%.2fx (~k_hi/k_lo=%.1f); fresh-load err buffer=%.2f > restore=%.2f -> restore tightens & rejects [V] direction" %
          (ha["variance_ratio_buffer_over_restore"], ha["predicted_ratio_k_high_over_k_low"], ha["fresh_load_excursion_buffering"], ha["fresh_load_excursion_restoration"]))
    print("    H-OTOC  calcite Omega  phys=%.3f -> acidosis=%.3f / low-Ca=%.3f (both <1 = dissolution-prone) [V] direction" %
          (ho["omega_physiological"], ho["omega_acidosis"], ho["omega_low_calcium"]))
    print("    frontier demonstrations pass: %s" % fq["demonstrations_pass"])

    print("\n[10] COMPARATIVE IONOREGULATION (which animals defend ions vs conform -- same R19 substrate, volume's own OU law) [REMEDIATION v0.5.0]")
    cs=comp.status()
    for r in cs["strategies"]:
        print("    %-30s k=%.1f  internal offset under salinity load=%.2f  (%s)" % (r["strategy"], r["k"], r["internal_offset"], r["clade"]))
    print("    conformer tracks environment (offset %.2f) > terrestrial regulator defends (offset %.2f); ratio %.1fx == gain ratio k_reg/k_conf=%.1f [V]" %
          (cs["strategies"][0]["internal_offset"], cs["strategies"][-1]["internal_offset"],
           cs["tracking_ratio_conformer_over_regulator"], cs["predicted_ratio_k_reg_over_k_conf"]))
    print("    sweep: conformer tracks %.0f%% of the environmental range, regulator only %.0f%% -> regulator is the precise ion user [V]" %
          (100*cs["sweep_conformer_fraction_tracked"], 100*cs["sweep_regulator_fraction_tracked"]))
    print("    strategy assignment cited [L]; ordering/separation [V]; absolute k & salinity tolerance [O]; per-species master-gene gamma not yet measured [O]/[H]")
    print("    comparative demonstrations pass: %s" % cs["demonstrations_pass"])

    print("\n[11] TIER-2 ION DISEASES (magnesium / CKD-MBD / humoral hypercalcemia -- existing failure modes reused, no new primitive) [REMEDIATION v0.6.0]")
    td=t2dis.status()
    mg=td["G2_magnesium"]; ck=td["G3_ckd_mbd"]; hh=td["G4_humoral_hypercalcemia_pthrp"]
    print("    G2 magnesium  arm-failure offset hypo=%.2f / hyper=%.2f vs healthy +-%.2f; ratio %.1fx == gain ratio %.1f; variance blow-up %s [V]" %
          (mg["hypomagnesemia_offset"], mg["hypermagnesemia_offset"], abs(mg["healthy_offset_under_intake"]),
           mg["excursion_ratio"], mg["predicted_gain_ratio"], mg["variance_blows_up"]))
    print("    G3 CKD-MBD    renal gain down -> PO4 up %s / vitD down %s / Ca down %s / PTH up (2ndary HPT) %s; CaxPO4 %.2f->%.2f climbs to ceiling %s [V]" %
          (ck["phosphate_rises"], ck["vitamin_d_falls"], ck["calcium_falls"], ck["pth_rises_secondary_hyperparathyroidism"],
           ck["ca_po4_product_start"], ck["ca_po4_product_advanced"], ck["ca_po4_product_climbs_to_ceiling_in_advanced_ckd"]))
    print("    G4 HHM/PTHrP  defended Ca rises with PTHrP %s -> hypercalcemia %s with endogenous PTH SUPPRESSED %s (inverse of T1 reset) [V]" %
          (hh["calcium_rises_with_pthrp"], hh["hypercalcemia_when_tumor_present"], hh["endogenous_pth_suppressed_despite_high_ca"]))
    print("    cited setpoints/variants/guidelines [L] (Mg ~0.85 mM; TRPM6/Gitelman; KDIGO CKD-MBD; PTHrP Stewart 2005); directions [V]; absolute magnitudes/timing [O]")
    print("    Tier-2 demonstrations pass: %s" % td["demonstrations_pass"])

    print("\n[12] TRANSPORT DYNAMICS (molecular 'how' beneath the loop arms: GHK constant-field flux + channel gating -- NEW PRIMITIVE) [REMEDIATION v0.7.0 / Tier-3 G5]")
    tr=trans.status()
    gh=tr["GHK_constant_field_flux"]; vd=tr["vitamin_d_channel_gating"]
    gg=tr["molecular_gain_grounds_loop_gain_k"]; lf=tr["loss_of_function_is_loop_gain_drop"]
    print("    GHK flux  reverses exactly at Nernst (E=%.2f mV, J=0) %s, changes sign across reversal %s, rectifies %s [F]/[V]" %
          (gh["nernst_mV"], gh["reverses_at_nernst"], gh["flux_changes_sign_across_reversal"], gh["ghk_rectifies"]))
    print("    gating    vitamin-D (VDR->TRPV5/6) raises channel open-probability %s and Ca reabsorptive flux %s monotonically (Hill x GHK) [L]/[V]" %
          (vd["open_probability_rises_with_vitd"], vd["ca_flux_rises_with_vitd"]))
    print("    GROUNDING k_molecular = -dJ/dC IS the OU loop gain: rises with channel number %s, steeper gate raises k %s; fed to ou_setpoint recovers Var=sigma^2/2k %s and err=load/k %s [V]" %
          (gg["k_rises_with_channel_number"], gg["steeper_gate_raises_k"], gg["ou_variance_law_recovered"], gg["ou_rejection_law_recovered"]))
    print("    LOF       a loss-of-function transporter drops k %.2f->%.2f (%s), offset grows x%.1f == gain ratio %.1f, variance blows up %s -- loop-gain-drop AT THE MEMBRANE [V]" %
          (lf["k_healthy"], lf["k_lof"], lf["lof_drops_k"], lf["offset_ratio"], lf["predicted_ratio_k_healthy_over_k_lof"], lf["variance_lof"] > lf["variance_healthy"]))
    print("    cited LOF phenotypes [L] (TRPV5/6 renal Ca wasting; ENaC/SCNN1A -> PHA1; H+-ATPase/ATP6V -> distal RTA); GHK+gating [F]; k=-dJ/dC [V]; absolute conductances/densities [O]")
    print("    transport-dynamics demonstrations pass: %s" % tr["demonstrations_pass"])

    print("\n[13] COMPARATIVE GAMMA (per-species osmoregulatory master-gene gamma -- ATP1A1 measured across the osmotic-strategy axis) [REMEDIATION v0.7.0 / Tier-3 G6 -- HONEST NEGATIVE]")
    cg=cgam.status(); gtt=cg["grounding_test"]
    print("    measured ATP1A1 (Na+,K+-ATPase a1) promoter gamma across 6 species (NCBI, SantaLucia 1998, never fitted); human anchor reproduced %s; offline-reproducible %s [V]" %
          (gtt["human_atp1a1_anchor_reproduced"], cg["measurement_offline_reproducible"]))
    print("    elasmobranch replicate (two k=2.0 species) gamma spread %.4f < 0.01 -> pipeline sound %s [V]" %
          (gtt["elasmobranch_replicate_spread"], gtt["replicate_consistent"]))
    print("    NEGATIVE: Spearman(gamma,k)=%.3f -> gamma grounds k = %s (non-monotone: k=3.0 amphibian gamma exceeds k=4.0 mammal)" %
          (gtt["spearman_gamma_vs_k"], gtt["gamma_grounds_k"]))
    print("    CONFOUND: Spearman(gamma,GC)=%.3f -> gamma tracks promoter GC = %s (a lineage/genome-background property; the within-genome ladder does not transfer cross-genome)" %
          (gtt["spearman_gamma_vs_gc"], gtt["gamma_tracks_promoter_gc"]))
    print("    -> comparative absolute k STAYS [O], now with the GC confound as its stated reason (not a bare placeholder); gamma measured [V]; strategy<->clade [L]")
    print("    comparative-gamma demonstrations pass (measurement sound AND negative correctly shown): %s" % cg["demonstrations_pass"])

    print("\n[15] THREE-LEVER THERAPEUTIC PRINCIPLE (L1 source / L2 gain / L3 setpoint -- inherited from the non-opioid analgesic volume, concept DOI 10.5281/zenodo.20733420) [v0.8.0]")
    tl=tlever.status(); asym=tl["lever_asymmetry"]; dna=tl["gain_lever_dna_ceiling"]; cw=tl["existing_results_crosswalk"]
    print("    ASYMMETRY (volume's own OU law): error=load/k set by L1+L2 ; variance=sigma^2/2k set ONLY by L2 -> ONLY L2 tightens variance: %s" % asym["only_L2_tightens_variance"])
    print("    baseline mean=%.3f var=%.5f | L1(load down) mean=%.3f var=%.5f (var unchanged) | L2(gain up) mean=%.3f var=%.5f (var halved) | L3 relocates target durably=%s" %
          (asym["baseline"]["mean_error"], asym["baseline"]["variance"], asym["L1_source"]["mean_error"], asym["L1_source"]["variance"],
           asym["L2_gain"]["mean_error"], asym["L2_gain"]["variance"], asym["L3_setpoint"]["relocates_durably"]))
    print("    DNA GROUNDING: the L2 gain ceiling per arm = node barrier b=gamma^2/4, gamma MEASURED; monotone in gamma %s (deepest=%s, shallowest=%s)" %
          (dna["gain_ceiling_monotone_in_measured_gamma"], dna["deepest_node"], dna["shallowest_node"]))
    print("    CROSSWALK (existing results re-read as one lever each, pulled live): L3=%s ; L2=%s ; L1=%s ; all validated=%s" %
          (cw["by_lever"]["L3"], cw["by_lever"]["L2"], cw["by_lever"]["L1"], cw["all_existing_results_validated"]))
    print("    three-lever demonstrations pass: %s" % tl["demonstrations_pass"])

    print("\n[16] DISEASE REMEDIATION under the three levers (owned diseases only; primary lever SELECTED from the corrupted OU parameter; improvement proposals) [v0.8.0]")
    dr=drem.status(); rt=dr["remediation"]
    for d in rt["diseases"]:
        print("    %-58s corrupted=%-42s -> %s" % (d["disease"][:58], d["corrupted_parameter"][:42], d["primary_lever"]))
    print("    by primary lever: L1=%d L2=%d L3=%d ; selection-rule demonstrations pass: %s" %
          (len(rt["by_primary_lever"].get("L1",[])), len(rt["by_primary_lever"].get("L2",[])), len(rt["by_primary_lever"].get("L3",[])), rt["selection_rule_demonstrations_pass"]))
    print("    scope discipline: %s" % dr["scope_note"][:96])
    print("    disease-remediation demonstrations pass: %s" % dr["demonstrations_pass"])

    print("\n[17] GATES")
    rg=gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why=gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    if rg["all_green"] and locked:
        print("\n    -> research is GREEN. To unlock writing: gates.write_research_complete(); echo writing > PHASE; then tools/build_docs.py")

if __name__ == "__main__":
    main()
