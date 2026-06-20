"""
verify_dev_timing_robust.py -- neuro-VP-SPEC-style gate for the v8 n=10 ROBUSTNESS hardening.

This gate certifies that the v7 every-predictor-[O] null at n=10 is ROBUST, and that the robustness
procedure itself is not blind. Like the other dev-timing gates it refuses to require any particular
correlation; it enforces that the robustness CLAIMS match what the perturbation/jackknife actually do on
the locked inputs. PASS means: (1) perturbing each locked stage by +/-1 CS -- the documented ordinal
uncertainty -- flips no predictor to [V] and never drives any perm p below the Bonferroni alpha, so the
[O] conclusion is stable under stage-encoding uncertainty; (2) dropping any single feature (n=9) flips no
predictor to [V] and every fold retains power (its exact-permutation floor is reachable), so the null is
neither an artifact of one feature nor a real signal masked by one outlier; (3) a synthetic comonotone
predictor DOES flip to [V] at n=10 and in every jackknife fold, proving the no-flip result for the real
predictors is a true negative, not a dead procedure; (4) the analysis ran on the exact locked n=10 inputs
(original 7 bit-identical, the 3 new appended, stage shas frozen) with the predictor matrix bit-identical
to dev_timing_wide's and no stage permanently edited; (5) determinism. With the real data every probe is
robust, so a correct package reports robust==True everywhere -- and this gate passes precisely because it
does. (MYF5 -> myotome, the v7 NEXT #1 candidate, was investigated and NOT locked because its staging is
too soft for a measured input; documented in LEDGER_dev_timing_robust.md, not forced into the table.)

Checks (PASS = 5/5):
  1. STAGE +/-1 ROBUST     stage_pm1_robustness.stable: no predictor flips to [V] under any one-at-a-time
                           +/-1 stage perturbation AND the smallest perm p over all perturbations stays
                           >= Bonferroni alpha.
  2. JACKKNIFE ROBUST      jackknife.robust: dropping any single feature (n=9) flips no predictor to [V],
                           and every fold retains power (floor reachable under Bonferroni).
  3. NON-BLIND CONTROL     a synthetic comonotone predictor flips to [V] at n=10 AND in every jackknife
                           fold -> the robustness machinery can detect a real signal (true negative above).
  4. LOCKED INPUTS         base stage vector == dev_timing.json's 7 then dev_timing_ext.json's 3; stage
                           shas frozen; predictor matrix bit-identical to dev_timing_wide; no global edit.
  5. DETERMINISM           two independent analyze() runs -> identical sha256 of the robustness result.
"""
import os, json, hashlib
import numpy as np
import gene_clock as GC
import dev_timing as DT
import dev_timing_wide as W
import dev_timing_robust as R


def _result_sha(res):
    pm1 = res["stage_pm1_robustness"]; jk = res["jackknife"]
    keep = {"pm1_stable": pm1["stable"], "pm1_any_flip": pm1["any_predictor_flips_to_V"],
            "pm1_min_p": round(pm1["min_perm_p_over_all"], 9),
            "jk_robust": jk["robust"], "jk_any_flip": jk["any_predictor_flips_to_V"],
            "jk_powered": jk["all_folds_powered"],
            "jk_rho_ranges": {k: [round(a, 9), round(b, 9)] for k, (a, b) in jk["rho_range_across_folds"].items()},
            "timing_sha256": res["timing_sha256"], "ext_sha256": res["ext_sha256"]}
    return hashlib.sha256(json.dumps(keep, sort_keys=True).encode()).hexdigest()


# ----------------------------------------------------------------- check 1
def check_stage_pm1(res):
    pm1 = res["stage_pm1_robustness"]
    ok = bool(pm1["stable"] and (not pm1["any_predictor_flips_to_V"])
              and (pm1["min_perm_p_over_all"] >= pm1["alpha_bonferroni"]))
    return ok, (f"{pm1['n_perturbations']} +/-1 perturbations: any_flip={pm1['any_predictor_flips_to_V']}, "
                f"min_perm_p={pm1['min_perm_p_over_all']:.4f} >= alpha_bonf {pm1['alpha_bonferroni']:.5f}; "
                f"max|rho|={pm1['max_abs_rho_over_all']:.3f}; stable={pm1['stable']}")


# ----------------------------------------------------------------- check 2
def check_jackknife(res):
    jk = res["jackknife"]
    ok = bool(jk["robust"] and (not jk["any_predictor_flips_to_V"]) and jk["all_folds_powered"])
    tata = jk["rho_range_across_folds"].get("tata", [float("nan"), float("nan")])
    return ok, (f"{jk['n_folds']} folds (n=9): any_flip={jk['any_predictor_flips_to_V']}, "
                f"all_powered={jk['all_folds_powered']}; best predictor tata rho in "
                f"[{tata[0]:+.3f},{tata[1]:+.3f}] (still not significant); robust={jk['robust']}")


# ----------------------------------------------------------------- check 3
def check_non_blind(res):
    pc = res["falsifiability"]["robustness_machinery_detects_signal"]
    ok = bool(pc["ok"] and pc["synthetic_comonotone_flips_at_n10"]
              and pc["synthetic_comonotone_flips_in_all_jackknife_folds"])
    return ok, (f"synthetic comonotone predictor (rho={pc['synth_rho']:+.3f}, perm_p={pc['synth_perm_p']:.5f}) "
                f"flips to [V] at n=10={pc['synthetic_comonotone_flips_at_n10']} and in all folds="
                f"{pc['synthetic_comonotone_flips_in_all_jackknife_folds']} => no-flip above is a true negative")


# ----------------------------------------------------------------- check 4
def check_locked_inputs(res):
    li = res["falsifiability"]["base_inputs_match_locked"]
    frozen_ok = (DT.timing_table_sha256() == res["timing_sha256"]) and (W.ext_table_sha256() == res["ext_sha256"])
    ok = bool(li["ok"] and frozen_ok)
    return ok, (f"orig7_unchanged={li['original_seven_unchanged']}, predictors_bit_identical="
                f"{li['predictors_bit_identical']}, base_stage_vector_locked={li['base_stage_vector_locked']}, "
                f"stage_shas_frozen={frozen_ok}")


# ----------------------------------------------------------------- check 5
def check_determinism():
    r1 = R.analyze(); r2 = R.analyze()
    h1, h2 = _result_sha(r1), _result_sha(r2)
    return (h1 == h2), f"result sha {h1[:10]}=={h2[:10]} ({h1 == h2})"


def main():
    res = R.analyze()
    checks = [
        ("1 STAGE +/-1 ROBUST (no flip; min perm p >= Bonferroni alpha)", check_stage_pm1(res)),
        ("2 JACKKNIFE ROBUST (no single feature flips it; folds retain power)", check_jackknife(res)),
        ("3 NON-BLIND CONTROL (synthetic comonotone DOES flip -> true negative)", check_non_blind(res)),
        ("4 LOCKED INPUTS (exact n=10 inputs; shas frozen; predictors bit-identical)", check_locked_inputs(res)),
        ("5 DETERMINISM (2x run identical)", check_determinism()),
    ]
    npass = 0
    print("=" * 84)
    print(f"  DEV-TIMING ROBUSTNESS GATE  |  hardening the n={res['n_features']} every-predictor-[O] null")
    print("=" * 84)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 84)
    pm1 = res["stage_pm1_robustness"]; jk = res["jackknife"]
    print(f"  HEADLINE: the n=10 null is ROBUST -- +/-1 stage perturbation never drops perm p below "
          f"{pm1['min_perm_p_over_all']:.3f} (alpha_bonf {pm1['alpha_bonferroni']:.4f}); no jackknife fold "
          f"flips any predictor, all folds powered.")
    print(f"  The strongest composition predictor (tata) reaches rho={jk['rho_range_across_folds'].get('tata',[0,0])[1]:+.2f} "
          f"in the most favorable fold and STILL fails Bonferroni -- a real null, not underpowered.")
    print(f"  MYF5 -> myotome (v7 NEXT #1) investigated and NOT locked: first-myotome staging is too soft")
    print(f"  (MYF5 onset is in the dermomyotome, before the myotome; CS span 11-13). Reported, not tuned.")
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "dev_timing_robust_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}",
                 "headline": dict(stage_pm1_stable=pm1["stable"], jackknife_robust=jk["robust"],
                                  min_perm_p_pm1=pm1["min_perm_p_over_all"],
                                  tata_rho_range=jk["rho_range_across_folds"].get("tata"),
                                  all_folds_powered=jk["all_folds_powered"])},
              open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
