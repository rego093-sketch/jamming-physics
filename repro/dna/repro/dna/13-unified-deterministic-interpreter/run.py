#!/usr/bin/env python3
# =============================================================================
#  run.py -- reproduce the §13 unified interpreter and prove determinism (C1).
#    1) run the engine twice -> assert the results JSON is byte-identical (2x sha256)
#    2) assert the engine's gates all pass
#    3) fidelity: compare the freshly-computed results to the frozen expected/ JSON
#  Writes reports-style status to stdout and exits non-zero on any failure.
# =============================================================================
import os, sys, json, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unified_interpreter_engine as E

EXPECTED = os.path.join(HERE, "expected", "unified_results.json")


def _canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=E._jsonable).encode("utf-8")

def _sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ok = True

    # ---- 1) determinism: two independent runs, byte-identical ----
    with contextlib.redirect_stdout(io.StringIO()):
        r1 = E.main(write=True)          # writes expected/unified_results.json
        r2 = E.main(write=False)
    b1, b2 = _canon(r1), _canon(r2)
    h1, h2 = _sha(b1), _sha(b2)
    det = (h1 == h2)
    ok = ok and det
    print(f"[{'PASS' if det else 'FAIL'}] determinism 2x sha256 identical")
    print(f"        sha256(run1) = {h1}")
    print(f"        sha256(run2) = {h2}")

    # ---- 2) engine gates ----
    gates_ok = bool(r1.get("gates_all_pass"))
    ok = ok and gates_ok
    print(f"[{'PASS' if gates_ok else 'FAIL'}] engine gates all pass")
    for k, v in r1["gates"].items():
        print(f"          - {k}: {'PASS' if v else 'FAIL'}")

    # ---- 3) fidelity vs frozen expected/ ----
    if os.path.exists(EXPECTED):
        frozen = _canon(json.load(open(EXPECTED)))
        fid = (_sha(frozen) == h1)
        ok = ok and fid
        print(f"[{'PASS' if fid else 'FAIL'}] fidelity: fresh result == frozen expected/unified_results.json")
    else:
        print("[FAIL] expected/unified_results.json missing")
        ok = False

    # ---- gamma identity headline ----
    gi = r1["gamma_identity"]
    print(f"\n  gamma identity: human_SOX2 gamma_round6 = {gi['gamma_round6']} "
          f"(expect {gi['expected']})  {'OK' if gi['match'] else 'MISMATCH'}")
    print(f"  methylation retention reproduces sec-12: {r1['methylation_retention']['reproduces_section12']}")

    status = "PASS" if ok else "FAIL"
    print(f"\n===== §13 run.py: {status} =====")

    # emit a small gate.json for the reports lane
    rep = {"chapter": "13-unified-deterministic-interpreter",
           "determinism_2x_sha256": det, "sha256": h1,
           "engine_gates": r1["gates"], "engine_gates_all_pass": gates_ok,
           "fidelity_vs_expected": (os.path.exists(EXPECTED) and _sha(frozen) == h1),
           "gamma_identity_match": gi["match"],
           "methylation_retention": r1["methylation_retention"]["reproduces_section12"],
           "overall": status}
    json.dump(rep, open(os.path.join(HERE, "expected", "run_gate.json"), "w"), indent=2)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
