"""
verify_dev_timing.py -- neuro-VP-SPEC-style gate for the developmental-timing calibration.

This gate is unusual on purpose: it does NOT require a particular correlation value (that would be
exactly the tuning anti-pattern the whole package forbids -- one would just fiddle the gene->feature
map or the sign until 'PASS' lit up). Instead it enforces that THE REPORTED GRADE MATCHES THE
MEASURED EVIDENCE. PASS means: the calibration was performed correctly on a locked, cited, gamma-
independent input; the model schedule is a pure measured-gamma readout; the apparatus is provably
not blind; and the honesty grade ([V] only if a significant positive rank correlation exists, else
[O]) equals what the numbers actually say. With the real data the correlation is null, so a correct
package reports [O] -- and this gate passes precisely because it does.

Checks (PASS = 5/5):
  1. ONE SWITCH            spinodal_genclock == morpho_core.spinodal  (< 1e-12).
  2. LOCKED CITED INPUT    dev_timing.json: provenance present; every test gene is a genuine [V]
                           master; every observed stage is an integer; table sha256 is frozen; and
                           (anti-back-fit) the stages are independent of the gamma table and are
                           NOT a suspiciously perfect match to the gamma order (|rho| < 0.99).
  3. GRADE == EVIDENCE     the derived schedule is a pure gamma readout (order==argsort spinodal);
                           rho, perm-p are computed; and the recorded grade is [V] iff (perm p<0.05
                           and rho>0) else [O]. The honesty invariant -- the claim never outruns the
                           evidence.
  4. FALSIFIABILITY        the apparatus detects a true signal (synthetic gamma ordered to the
                           stages -> |rho|->1) and collapses on a shuffle -> the reported null is a
                           TRUE null (promoter stiffness != timing), not a dead test.
  5. DETERMINISM           two independent calibrate() runs -> identical sha256 of the result.
"""
import os, io, json, hashlib, contextlib
import numpy as np
import gene_clock as GC
import morpho_core as mc
import dev_timing as DT


def _result_sha(res):
    keep = {k: res[k] for k in ("spearman_rho", "pearson_r", "permutation_p", "timing_validated",
                                "grade", "derived_order", "observed_order", "timing_sha256")}
    return hashlib.sha256(json.dumps(keep, sort_keys=True).encode()).hexdigest()


# ----------------------------------------------------------------- check 1
def check_one_switch():
    gs = np.linspace(1.2, 1.8, 241)
    d = max(abs(GC.spinodal(g) - mc.spinodal(g)) for g in gs)
    return d < 1e-12, f"max|delta spinodal| = {d:.2e}"


# ----------------------------------------------------------------- check 2
def check_locked_cited_input(res):
    feats, prov, J = DT.load_dev_timing()
    prov_ok = len(prov) > 40 and "_grade" in J and J["_grade"].startswith("[L]")
    masters_ok = all(g in DT.V_MASTERS for _, g, _ in feats)
    ints_ok = all(isinstance(s, int) for _, _, s in feats)
    frozen_ok = (DT.timing_table_sha256() == res["timing_sha256"])
    ind_ok, ind = DT.stages_independent_of_gamma()
    ok = prov_ok and masters_ok and ints_ok and frozen_ok and ind_ok
    return ok, (f"prov={prov_ok}, [V]-masters_only={masters_ok}, integer_stages={ints_ok}, "
                f"sha_frozen={frozen_ok}, gamma-independent={ind['stages_unchanged_under_gamma_perturbation']} "
                f"& not_backfit={ind['not_backfit']} (|rho|={ind['abs_rho']:.3f})")


# ----------------------------------------------------------------- check 3
def check_grade_matches_evidence(res):
    readout_ok = res["order_is_gamma_readout"]
    # recompute the grade rule independently and require the recorded grade to match it
    should_validate = bool((res["permutation_p"] < 0.05) and (res["spearman_rho"] > 0))
    grade_ok = (res["timing_validated"] == should_validate) and \
               (res["grade"] == ("[V]" if should_validate else "[O]"))
    ok = bool(readout_ok and grade_ok)
    verdict = "predicts" if res["timing_validated"] else "does NOT predict (honest null)"
    return ok, (f"order==argsort(spinodal)={readout_ok}; rho={res['spearman_rho']:+.3f} "
                f"perm_p={res['permutation_p']:.3f} -> grade {res['grade']} ({verdict}); "
                f"grade==evidence={grade_ok}")


# ----------------------------------------------------------------- check 4
def check_falsifiability():
    ok, det = DT.apparatus_detects_signal()
    return ok, (f"rho(gamma ordered to stages)={det['rho_when_gamma_matches_stages']:+.3f} (->1), "
                f"rho(stages shuffled)={det['rho_when_stages_shuffled']:+.3f} (small) => true null")


# ----------------------------------------------------------------- check 5
def check_determinism():
    r1 = DT.calibrate(); r2 = DT.calibrate()
    h1, h2 = _result_sha(r1), _result_sha(r2)
    return (h1 == h2), f"result sha {h1[:10]}=={h2[:10]} ({h1 == h2})"


def main():
    res = DT.calibrate()
    checks = [
        ("1 ONE SWITCH (gene-clock fold == body fold)", check_one_switch()),
        ("2 LOCKED CITED INPUT (Carnegie stages, gamma-independent)", check_locked_cited_input(res)),
        ("3 GRADE == EVIDENCE (claim never outruns data)", check_grade_matches_evidence(res)),
        ("4 FALSIFIABILITY (apparatus detects a real signal)", check_falsifiability()),
        ("5 DETERMINISM (2x run identical)", check_determinism()),
    ]
    npass = 0
    print("=" * 78)
    print(f"  DEVELOPMENTAL-TIMING CALIBRATION GATE  |  {res['n_features']} [V]-master features")
    print("=" * 78)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 78)
    print(f"  HEADLINE: promoter-stiffness gamma vs observed staging -> Spearman "
          f"rho={res['spearman_rho']:+.3f} (perm p={res['permutation_p']:.2f}); grade {res['grade']}.")
    print(f"  This is the HONEST result: the order is a deterministic gamma function that has now")
    print(f"  been TESTED against biology and does not (yet) match -- a measured [O], not a hedge.")
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "dev_timing_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}", "headline": dict(
                    spearman_rho=res["spearman_rho"], permutation_p=res["permutation_p"],
                    grade=res["grade"], timing_validated=res["timing_validated"])},
              open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
