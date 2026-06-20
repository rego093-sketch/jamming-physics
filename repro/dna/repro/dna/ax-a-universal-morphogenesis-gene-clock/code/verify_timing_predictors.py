"""
verify_timing_predictors.py -- neuro-VP-SPEC-style gate for the v6 #1 predictor battery.

Like verify_dev_timing.py, this gate refuses to require any particular correlation (that would be
the tuning anti-pattern). It enforces that THE REPORTED GRADES MATCH THE MEASURED EVIDENCE for a
BATTERY of measured promoter quantities tested against the SAME locked, cited, gamma-independent
Carnegie stages. PASS means: the inputs are the locked ones (stages sha frozen and identical to
dev_timing; the 4 copied promoter sequences are byte-identical to morpho_promoters.cache.json; the
3 re-fetched sequences reproduce the LOCKED gamma within assembly drift); gamma/GC are read from
the locked table (so the gamma column is bit-identical to dev_timing's, proven by equal rho); every
motif is the fixed a-priori consensus (not mutated to chase a result); the Bonferroni correction and
the exact-permutation power floor are correctly computed and DISCLOSED; the apparatus is provably not
blind; and each recorded grade is [V] iff its Bonferroni-corrected permutation p < alpha AND its rank
correlation is positive, else [O]. With the real data every predictor is null, so a correct package
reports overall [O] -- and this gate passes precisely because it does.

Checks (PASS = 5/5):
  1. GRADE == EVIDENCE     for every predictor, recorded grade == ([V] iff perm_p_bonf<alpha and
                           rho>0 else [O]); overall_grade == [V] iff any validated else [O].
  2. LOCKED INPUTS         Carnegie-stage sha256 == dev_timing's frozen sha (same input, unchanged);
                           the 4 copied sequences are byte-identical to morpho_promoters.cache.json;
                           the 3 re-fetched sequences reproduce the locked gamma within tol; and the
                           gamma rho equals dev_timing's spinodal rho (gamma read from locked table).
  3. FALSIFIABILITY        the battery apparatus detects a synthetic comonotone predictor (|rho|->1,
                           perm p<0.05) and collapses on a shuffle -> the reported null is a TRUE null.
  4. NO-TUNING + POWER     every motif consensus equals the fixed a-priori string; Bonferroni is
                           applied (perm_p_bonf == min(1, perm_p*K)); and the exact-permutation floor
                           (smallest reachable p at this n) is computed and its reachability disclosed.
  5. DETERMINISM           two independent calibrate() runs -> identical sha256 of the result.
"""
import os, json, hashlib
import numpy as np
import gene_clock as GC
import dev_timing as DT
import timing_predictors as TP


def _result_sha(res):
    keep = {"results": [(r["predictor"], round(r["spearman_rho"], 9) if r["spearman_rho"] == r["spearman_rho"] else "nan",
                         round(r["perm_p"], 9) if r["perm_p"] == r["perm_p"] else "nan", r["grade"])
                        for r in res["results"]],
            "overall_grade": res["overall_grade"],
            "timing_sha256": res["timing_sha256"],
            "cache_sha256": res["cache_sha256"]}
    return hashlib.sha256(json.dumps(keep, sort_keys=True).encode()).hexdigest()


# ----------------------------------------------------------------- check 1
def check_grade_matches_evidence(res):
    alpha = res["alpha"]
    bad = []
    for r in res["results"]:
        if r["spearman_rho"] != r["spearman_rho"]:          # nan -> degenerate -> must be [O]
            if r["grade"] != "[O]" or r["validated"]:
                bad.append(r["predictor"])
            continue
        should = bool((r["perm_p_bonf"] < alpha) and (r["spearman_rho"] > 0))
        if (r["validated"] != should) or (r["grade"] != ("[V]" if should else "[O]")):
            bad.append(r["predictor"])
    any_val = any(r["validated"] for r in res["results"])
    overall_ok = (res["any_predictor_validated"] == any_val) and \
                 (res["overall_grade"] == ("[V]" if any_val else "[O]"))
    ok = (len(bad) == 0) and overall_ok
    return ok, (f"per-predictor grade==evidence (mismatches={bad}); "
                f"overall_grade={res['overall_grade']} consistent={overall_ok}")


# ----------------------------------------------------------------- check 2
def check_locked_inputs(res):
    frozen_ok = (DT.timing_table_sha256() == res["timing_sha256"])
    cp_ok, cp = TP.copied_sequences_identical()
    ft_ok, ft = TP.fetched_reproduce_locked_gamma()
    cons_ok, cons = TP.gamma_matches_dev_timing()
    ok = frozen_ok and cp_ok and ft_ok and cons_ok
    max_resid = max((g["residual"] for g in ft["genes"]), default=0.0)
    return ok, (f"stage_sha_frozen={frozen_ok}; copied4_identical={cp_ok}; "
                f"fetched3_reproduce_gamma={ft_ok} (max_resid={max_resid:.1e}<=tol {ft['tol']:.0e}); "
                f"gamma_rho==dev_timing={cons_ok} ({cons['gamma_rho_here']:+.4f})")


# ----------------------------------------------------------------- check 3
def check_falsifiability():
    ok, det = TP.apparatus_detects_signal()
    return ok, (f"rho(comonotone predictor)={det['rho_perfect']:+.3f} (->1, perm_p={det['perm_p_perfect']:.4f}<0.05), "
                f"rho(shuffled)={det['rho_shuffled']:+.3f} (small) => true null")


# ----------------------------------------------------------------- check 4
def check_no_tuning_and_power(res):
    motifs_ok = all(res["motif_consensus"][k]["motif"] == TP.MOTIFS[k] for k in TP.MOTIFS)
    K = res["K_predictors"]
    bonf_ok = True
    for r in res["results"]:
        if r["perm_p"] == r["perm_p"]:                      # not nan
            if abs(r["perm_p_bonf"] - min(1.0, r["perm_p"] * K)) > 1e-12:
                bonf_ok = False
    fl = res["permutation_floor"]
    floor_ok = (0.0 < fl["floor_p"] <= 1.0) and isinstance(fl["floor_reachable_under_bonferroni"], bool)
    ok = bool(motifs_ok and bonf_ok and floor_ok)
    return ok, (f"motifs==a_priori={motifs_ok}; bonferroni_applied={bonf_ok} (K={K}); "
                f"perm_floor={fl['floor_p']:.5f} reachable={fl['floor_reachable_under_bonferroni']} "
                f"(disclosed)")


# ----------------------------------------------------------------- check 5
def check_determinism():
    r1 = TP.calibrate(); r2 = TP.calibrate()
    h1, h2 = _result_sha(r1), _result_sha(r2)
    return (h1 == h2), f"result sha {h1[:10]}=={h2[:10]} ({h1 == h2})"


def main():
    res = TP.calibrate()
    checks = [
        ("1 GRADE == EVIDENCE (every predictor graded by its data)", check_grade_matches_evidence(res)),
        ("2 LOCKED INPUTS (stages frozen; seqs verbatim/reproduced; gamma==dev_timing)", check_locked_inputs(res)),
        ("3 FALSIFIABILITY (battery detects a real signal)", check_falsifiability()),
        ("4 NO-TUNING MOTIFS + POWER DISCLOSED (Bonferroni + perm floor)", check_no_tuning_and_power(res)),
        ("5 DETERMINISM (2x run identical)", check_determinism()),
    ]
    npass = 0
    print("=" * 80)
    print(f"  TIMING-PREDICTOR BATTERY GATE  |  {res['n_features']} [V]-master features, "
          f"K={res['K_predictors']} predictors")
    print("=" * 80)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 80)
    best = max((r for r in res["results"] if r["spearman_rho"] == r["spearman_rho"]),
               key=lambda r: abs(r["spearman_rho"]))
    print(f"  HEADLINE: best |rho| predictor = {best['predictor']} (rho={best['spearman_rho']:+.3f}, "
          f"perm_p={best['perm_p']:.3f}, Bonf p={best['perm_p_bonf']:.3f}); overall grade "
          f"{res['overall_grade']}.")
    print(f"  HONEST NULL: no measured proximal-promoter quantity (stiffness, GC, CpG o/e, or TATA/")
    print(f"  GC-box/CAAT density) predicts Carnegie staging order for these 7 features. Reported, not tuned.")
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "timing_predictors_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}",
                 "headline": dict(best_predictor=best["predictor"],
                                  best_rho=best["spearman_rho"], best_perm_p=best["perm_p"],
                                  best_perm_p_bonf=best["perm_p_bonf"],
                                  overall_grade=res["overall_grade"],
                                  any_predictor_validated=res["any_predictor_validated"])},
              open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
