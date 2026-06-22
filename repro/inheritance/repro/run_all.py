#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  the research gate for the inheritance kit.

Runs, in one deterministic pass:
  (0) NCBI offline VERIFY  -- recompute the RNA-carrier gamma atlas from the cached promoters and confirm
      the SOX9 anchor reproduces (no-tuning fidelity gate).
  (1) the five research batteries:
        R   rna_layer.py                  (the RNA writable channel)
        TG  env_to_germline.py            (environment -> germline transmission, the reprogramming firewall)
        I   transgenerational_immunity.py (immune strengthening + inherited priming)
        V   rna_vaccine.py                (vaccine as a dosed RNA drive)
        GT  gene_therapy.py               (two therapeutic levers)
  (2) a DETERMINISM gate (VP-SPEC C1): each battery emitted twice must be byte-identical (2x sha256).

Emits reports/research_complete.json with all_green. all_green requires: anchor reproduces AND every
battery all_pass AND determinism holds. Nothing is fitted; every number traces to the measured promoter
gamma + the vendored R19 substrate. Run:  python repro/run_all.py
"""
import os, sys, json, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(_HERE, "..")
_ENGINE = os.path.join(_PKG, "engine")
_DATA = os.path.join(_PKG, "data")
_REPORTS = os.path.join(_PKG, "reports")
for _d in (_ENGINE, _DATA):
    sys.path.insert(0, _d)

import rna_layer, env_to_germline, transgenerational_immunity, rna_vaccine, gene_therapy
import rna_species, two_channel, germline_escapee, a4_layer
import coordinate_heritability, a4_application_map, immune_maturation, rna_feasibility_map
import disease_feasibility_map
import feasibility_validation
import parent_of_origin, rna_vaccine_kinetics, lever_map
import fetch_rna_gamma, fetch_imprint_gamma, fetch_disease_gamma
import fetch_bvalidation
import fetch_signlaw_depmap
import fetch_signlaw_crispra


def _sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def main():
    # (0) NCBI offline verify -- anchor-gated, no network (both measured atlases + the A4 windows)
    rna_v = fetch_rna_gamma.verify()
    imp_v = fetch_imprint_gamma.verify()
    dis_v = fetch_disease_gamma.verify()
    a4_v = a4_layer.verify_a4()
    # (0b) (B) held-out validation cache: provenance + structural integrity, and recompute the headline
    #      (B) Spearman from the cache (offline, no network). This gates the FV battery's external target.
    bval_v = fetch_bvalidation.verify()
    # (0c) (B) sign-law '-' arm held-out cache (DepMap 24Q2 CRISPR-KO): provenance + structural integrity,
    #      and recompute the ONCO '-'-arm headline (point-biserial + exact permutation p) from the cache +
    #      the FROZEN atlas (offline, no network). This gates the FV7 sign-law '-' arm score.
    signlaw_v = fetch_signlaw_depmap.verify()
    # (0d) (B) sign-law '+' RESTORE arm held-out cache (Horlbeck 2016 hCRISPRa-v2 K562 growth): provenance +
    #      structural integrity, and recompute the ONCO '+'-arm headline (point-biserial + exact permutation
    #      p) from the cache + the FROZEN atlas (offline, no network). This gates the FV8 sign-law '+' arm
    #      score -- the mirror of FV7 that completes the bidirectional held-out test of the sign-law.
    signlaw_plus_v = fetch_signlaw_crispra.verify()

    # (1) batteries
    batteries = {
        "R_rna_layer": rna_layer.run_battery(),
        "RS_rna_species": rna_species.run_battery(),
        "A4_a4_layer": a4_layer.run_battery(),
        "TC_two_channel": two_channel.run_battery(),
        "TG_env_to_germline": env_to_germline.run_battery(),
        "GE_germline_escapee": germline_escapee.run_battery(),
        "CH_coordinate_heritability": coordinate_heritability.run_battery(),
        "I_transgenerational_immunity": transgenerational_immunity.run_battery(),
        "IM_immune_maturation": immune_maturation.run_battery(),
        "V_rna_vaccine": rna_vaccine.run_battery(),
        "GT_gene_therapy": gene_therapy.run_battery(),
        "AM_a4_application_map": a4_application_map.run_battery(),
        "FM_rna_feasibility_map": rna_feasibility_map.run_battery(),
        "DM_disease_feasibility_map": disease_feasibility_map.run_battery(),
        "FV_feasibility_validation": feasibility_validation.run_battery(),
        "PO_parent_of_origin": parent_of_origin.run_battery(),
        "VK_rna_vaccine_kinetics": rna_vaccine_kinetics.run_battery(),
        "LV_lever_map": lever_map.run_battery(),
    }

    # (2) determinism gate -- each battery emitted twice is byte-identical
    runners = {
        "R_rna_layer": rna_layer.run_battery,
        "RS_rna_species": rna_species.run_battery,
        "A4_a4_layer": a4_layer.run_battery,
        "TC_two_channel": two_channel.run_battery,
        "TG_env_to_germline": env_to_germline.run_battery,
        "GE_germline_escapee": germline_escapee.run_battery,
        "CH_coordinate_heritability": coordinate_heritability.run_battery,
        "I_transgenerational_immunity": transgenerational_immunity.run_battery,
        "IM_immune_maturation": immune_maturation.run_battery,
        "V_rna_vaccine": rna_vaccine.run_battery,
        "GT_gene_therapy": gene_therapy.run_battery,
        "AM_a4_application_map": a4_application_map.run_battery,
        "FM_rna_feasibility_map": rna_feasibility_map.run_battery,
        "DM_disease_feasibility_map": disease_feasibility_map.run_battery,
        "FV_feasibility_validation": feasibility_validation.run_battery,
        "PO_parent_of_origin": parent_of_origin.run_battery,
        "VK_rna_vaccine_kinetics": rna_vaccine_kinetics.run_battery,
        "LV_lever_map": lever_map.run_battery,
    }
    determinism = {}
    det_all = True
    for k, fn in runners.items():
        h1 = _sha(fn()); h2 = _sha(fn())
        determinism[k] = {"sha256": h1, "identical": bool(h1 == h2)}
        det_all &= (h1 == h2)

    all_batteries_pass = all(b["all_pass"] for b in batteries.values())
    anchor_ok = bool(rna_v.get("ok") and rna_v.get("anchor_reproduced")
                     and imp_v.get("ok") and imp_v.get("anchor_reproduced")
                     and dis_v.get("ok") and dis_v.get("cross_all_agree") and a4_v.get("ok"))
    validation_ok = bool(bval_v.get("ok"))
    signlaw_validation_ok = bool(signlaw_v.get("ok"))
    signlaw_plus_arm_validation_ok = bool(signlaw_plus_v.get("ok"))
    all_green = bool(anchor_ok and validation_ok and signlaw_validation_ok
                     and signlaw_plus_arm_validation_ok and all_batteries_pass and det_all)

    report = {
        "kit": "vp_inheritance_kit",
        "phase": "writing",
        "all_green": all_green,
        "ncbi_offline_verify": {
            "rna_carrier": {"ok": rna_v.get("ok"), "anchor_reproduced": rna_v.get("anchor_reproduced"),
                            "n_genes": rna_v.get("n")},
            "imprint": {"ok": imp_v.get("ok"), "anchor_reproduced": imp_v.get("anchor_reproduced"),
                        "n_genes": imp_v.get("n")},
            "disease": {"ok": dis_v.get("ok"), "cross_package_all_reproduce": dis_v.get("cross_all_agree"),
                        "n_oncology": dis_v.get("oncology", {}).get("n"),
                        "n_neurodegeneration": dis_v.get("neurodegeneration", {}).get("n"),
                        "cross_package_consistency": dis_v.get("cross_package_consistency")},
            "a4_coordinates": {"ok": a4_v.get("ok"), "n_windows": a4_v.get("n")},
        },
        "heldout_validation_verify": {
            "ok": bval_v.get("ok"),
            "source_doi": "10.1016/j.cell.2022.05.013",
            "figshare_article": "20029387",
            "provenance_ok": bval_v.get("provenance_ok"),
            "held_out_warrant_ok": bval_v.get("held_out_warrant_ok"),
            "prediction_sign_locked_ok": bval_v.get("prediction_sign_locked_ok"),
            "panel_rule_ok": bval_v.get("panel_rule_ok"),
            "structure_ok": bval_v.get("structure_ok"),
            "primary_spearman_rho_from_cache": bval_v.get("primary_spearman_rho_from_cache"),
            "n_primary": bval_v.get("n_primary"),
            "headline_reproduced": bval_v.get("headline_reproduced"),
            "B_result": "NULL (rho=-0.0760, p=0.6283, n=43, K562 GWPS): the no-tuning (A)-map gamma-ordering "
                        "shows no significant correspondence to on-target CRISPRi knockdown depth; promotes "
                        "no [O] item. See engine/feasibility_validation.py and the ledger.",
        },
        "heldout_signlaw_minus_arm_verify": {
            "ok": signlaw_v.get("ok"),
            "source": "DepMap 24Q2 Public CRISPRGeneEffect (Chronos)",
            "figshare_article": "25880521",
            "provenance_ok": signlaw_v.get("provenance_ok"),
            "held_out_warrant_ok": signlaw_v.get("held_out_warrant_ok"),
            "prediction_sign_locked_ok": signlaw_v.get("prediction_sign_locked_ok"),
            "readout_scope_ok": signlaw_v.get("readout_scope_ok"),
            "structure_ok": signlaw_v.get("structure_ok"),
            "no_smuggled_sign_or_gc": signlaw_v.get("no_smuggled_sign_or_gc"),
            "n_onco_scored": signlaw_v.get("n_onco_scored"),
            "n_neurodegen_out_of_scope": signlaw_v.get("n_neurodegen_out_of_scope"),
            "point_biserial_from_cache": signlaw_v.get("point_biserial_sign_minus_vs_neg_gene_effect"),
            "exact_permutation_p": signlaw_v.get("exact_permutation_p_one_sided"),
            "headline_reproduced": signlaw_v.get("headline_reproduced"),
            "B_result": "SCORED (point-biserial=+0.494, exact one-sided p=0.0227, n=16 onco): under the '-' "
                        "(knockout) operation GOF oncogenes are dependencies and LOF suppressors are not -- "
                        "the corrective sign-law's '-' arm is confirmed on held-out DepMap data, identified "
                        "(orthogonal to GC) and firewall-clean. Promotes the '-' arm [V]; O-22 stays [O] "
                        "(needs the '+' restore arm alone -- FV6's obstacle, not Delta-h), O-21 stays [O]. See FV7.",
        },
        "heldout_signlaw_plus_arm_verify": {
            "ok": signlaw_plus_v.get("ok"),
            "source": "Horlbeck et al. 2016 hCRISPRa-v2 K562 gene growth phenotypes, eLife 5:e19760 (supp. file 10)",
            "elife_article": "19760",
            "doi": "10.7554/eLife.19760",
            "provenance_ok": signlaw_plus_v.get("provenance_ok"),
            "held_out_warrant_ok": signlaw_plus_v.get("held_out_warrant_ok"),
            "prediction_sign_locked_ok": signlaw_plus_v.get("prediction_sign_locked_ok"),
            "readout_scope_ok": signlaw_plus_v.get("readout_scope_ok"),
            "structure_ok": signlaw_plus_v.get("structure_ok"),
            "no_smuggled_sign_or_gc": signlaw_plus_v.get("no_smuggled_sign_or_gc"),
            "n_onco_scored": signlaw_plus_v.get("n_onco_scored"),
            "n_neurodegen_out_of_scope": signlaw_plus_v.get("n_neurodegen_out_of_scope"),
            "point_biserial_from_cache": signlaw_plus_v.get("point_biserial_sign_plus_vs_neg_growth"),
            "exact_permutation_p": signlaw_plus_v.get("exact_permutation_p_one_sided"),
            "headline_reproduced": signlaw_plus_v.get("headline_reproduced"),
            "B_result": "SCORED (point-biserial=+0.4852, exact one-sided p=0.0274, n=16 onco): under the '+' "
                        "(CRISPR-activation) operation LOF suppressors are growth-suppressive and GOF "
                        "oncogenes are not -- the corrective sign-law's '+' RESTORE arm is confirmed on "
                        "held-out Horlbeck 2016 CRISPRa data, identified (orthogonal to GC) and firewall-clean. "
                        "The MIRROR of FV7: together the sign-law is now BIDIRECTIONALLY [V] (both arms, "
                        "direction-only), removing in full the bidirectional-data obstacle. O-22 (per-patient "
                        "yes/no) STILL stays [O] -- its obstacle is now the FIREWALL, not data: a class-level "
                        "direction-only law cannot certify a per-patient corrected outcome, which needs the "
                        "firewalled per-patient magnitude; O-21 (absolute dose) stays [O]. This corrects FV7's "
                        "'+'-arm-alone framing. See FV8.",
        },
        "battery_pass": {k: b["all_pass"] for k, b in batteries.items()},
        "scoreboards": {
            "R_rna_layer": batteries["R_rna_layer"]["R5_scoreboard"],
            "RS_rna_species": batteries["RS_rna_species"]["RS5_scoreboard"],
            "A4_a4_layer": batteries["A4_a4_layer"]["A4_5_scoreboard"],
            "TC_two_channel": batteries["TC_two_channel"]["TC4_scoreboard"],
            "TG_env_to_germline": batteries["TG_env_to_germline"]["TG6_scoreboard"],
            "GE_germline_escapee": batteries["GE_germline_escapee"]["GE4_scoreboard"],
            "CH_coordinate_heritability": batteries["CH_coordinate_heritability"]["CH4_scoreboard"],
            "I_transgenerational_immunity": batteries["I_transgenerational_immunity"]["I4_scoreboard"],
            "IM_immune_maturation": batteries["IM_immune_maturation"]["IM4_scoreboard"],
            "V_rna_vaccine": batteries["V_rna_vaccine"]["V5_scoreboard"],
            "GT_gene_therapy": batteries["GT_gene_therapy"]["GT4_scoreboard"],
            "AM_a4_application_map": batteries["AM_a4_application_map"]["AM4_scoreboard"],
            "FM_rna_feasibility_map": batteries["FM_rna_feasibility_map"]["FM_scoreboard"],
            "DM_disease_feasibility_map": batteries["DM_disease_feasibility_map"]["DM_scoreboard"],
            "FV_feasibility_validation": batteries["FV_feasibility_validation"]["FV_scoreboard"],
            "PO_parent_of_origin": batteries["PO_parent_of_origin"]["PO4_scoreboard"],
            "VK_rna_vaccine_kinetics": batteries["VK_rna_vaccine_kinetics"]["VK3_scoreboard"],
            "LV_lever_map": batteries["LV_lever_map"]["LV5_scoreboard"],
        },
        "determinism_2xsha256": determinism,
        "determinism_all_identical": det_all,
        "discipline": {
            "dna_emergence": "every number traces to the measured promoter gamma (NN-stacking dG37, SantaLucia "
                             "1998) + the measured A4 coordinate (compartment/anchor/helical-contact, vendored "
                             "vp_a4) + the vendored R19 switch; nothing fitted.",
            "two_channel_reads": "gamma is the unwritable SET; the environment/RNA write through the A4 "
                                 "COORDINATE channel (and methylation), never through gamma.",
            "no_tuning": "gamma measured from NCBI; pipeline accepted only because the SOX9 anchor reproduces.",
            "magnitude_firewall": "WHICH switch + SIGN of drive + ORDERING/DECAY read; absolute phenotype/dose/"
                                  "titre/generation-count are runtime [O]; clinical application is firewalled.",
            "single_source_substrate": "inherited/vp_substrate.py is the only copy of the switch math.",
            "grades": "[F] forced / [V] simulation-verified / [O] open / [L] calibration.",
        },
    }
    os.makedirs(_REPORTS, exist_ok=True)
    json.dump(report, open(os.path.join(_REPORTS, "research_complete.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    # also persist the full battery detail for the record
    json.dump(batteries, open(os.path.join(_REPORTS, "emergence_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print(json.dumps({"all_green": all_green, "anchor_ok": anchor_ok, "validation_ok": validation_ok,
                      "signlaw_validation_ok": signlaw_validation_ok,
                      "signlaw_plus_arm_validation_ok": signlaw_plus_arm_validation_ok,
                      "all_batteries_pass": all_batteries_pass, "determinism": det_all,
                      "battery_pass": report["battery_pass"]}, ensure_ascii=False, indent=2))
    if not all_green:
        sys.exit(1)


if __name__ == "__main__":
    main()
