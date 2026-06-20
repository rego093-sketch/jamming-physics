#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_discipline.py  --  inherited analgesic_threshold_logic_v2_0 DISCIPLINE layer (fail-closed).

Runs the five inherited gates in dependency order (D5 scans D2/D3/D4 outputs, so it runs last) and freezes
their determinism hashes. This is the immune instantiation of the analgesic package's repro/run_all.py
(DOI 10.5281/zenodo.20733420): same no-tuning / honest-grading / fail-closed-firewall discipline.

    D1 inherit_reverify             re-derive the 4 master gammas + R19 threshold structure, drift 0
    D2 burden_prioritisation        declared-weight TARGET prioritisation (ranks targets, not drugs)
    D3 external_mechanism_honesty   clinical efficacy of real therapies graded cited [L], never derived
    D4 falsification_register       a measurable falsifier for every load-bearing claim
    D5 forbidden_claim_scan         fail-closed firewall: no numeric dose / synthesis / novel-efficacy / safety

SPEED (v0.13.0): the five gates run IN-PROCESS via runpy (their real __main__ blocks, so the frozen JSON is
byte-identical) instead of five subprocess interpreters, and the inherited/ imports (gamma_pipeline, vp_substrate)
are loaded once and reused across gates. run() also memoises its result for the process, so a battery that calls
it from both run_all and research_gate pays for ONE discipline pass, not two. No frozen hash changes; no gate is
relaxed; any non-SystemExit error fails closed.

Callable: run() -> {"overall": "PASS"|"FAIL", ...} (used by gates.research_gate()).
CLI:      python3 run_discipline.py    -> OVERALL: PASS (5/5 + determinism)
"""
import os, sys, json, hashlib, runpy, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("D1 inherit-reverify",        "inherit_reverify.py"),
    ("D2 burden-prioritisation",   "burden_prioritisation.py"),
    ("D3 mechanism-honesty (gate)", "external_mechanism_honesty.py"),
    ("D4 falsification",           "falsification_register.py"),
    ("D5 forbidden-claim (gate)",  "forbidden_claim_scan.py"),
]
FROZEN = [
    "expected/reverify.json",
    "expected/priority_ranking.json",
    "expected/mechanism_honesty.json",
    "expected/falsification.json",
    "expected/claim_scan.json",
]

_RESULT = None   # process-level memo: a battery run verifies a fixed state, so the result is reused (saves the
                 # second discipline pass when run_all and research_gate both ask). force=True bypasses it.


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _run_gate_inprocess(script):
    """Execute a gate's real __main__ in-process (no new interpreter). The gate writes its expected/*.json with
    exactly the same code as before, so the frozen bytes are identical. Returns True iff it exits cleanly;
    SystemExit code 0/None => PASS, any other code or any exception => fail closed."""
    path = os.path.join(HERE, script)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            runpy.run_path(path, run_name="__main__")
        return True, ""                      # gate completed without raising (all gates normally SystemExit)
    except SystemExit as e:
        code = e.code
        return ((code is None) or (code == 0)), buf.getvalue()
    except Exception as e:                   # import/compute failure => fail closed (matches old returncode!=0)
        return False, (buf.getvalue() + "\n" + repr(e))


def run(verbose=False, force=False):
    global _RESULT
    if _RESULT is not None and not force:
        return _RESULT
    results, passed = {}, 0
    for label, script in STEPS:
        ok, captured = _run_gate_inprocess(script)
        results[label] = ok
        if verbose:
            print("[%s] %s" % ("PASS" if ok else "FAIL", label))
            if not ok and captured:
                print(captured[-1200:])
        if not ok:
            _RESULT = {"overall": "FAIL", "failed_at": label, "results": results}
            return _RESULT
        passed += 1

    cur = {p: sha(os.path.join(HERE, p)) for p in FROZEN}
    exp_path = os.path.join(HERE, "expected_sha256.json")
    drift = []
    if os.path.exists(exp_path):
        exp = json.load(open(exp_path))
        drift = [p for p in FROZEN if exp.get(p) != cur[p]]
        if not drift:
            passed += 1
    else:
        json.dump(cur, open(exp_path, "w"), indent=1)
        passed += 1
    overall = "PASS" if not drift else "FAIL"
    _RESULT = {"overall": overall, "results": results, "determinism_drift": drift,
               "checks_passed": passed, "checks_total": len(STEPS) + 1}
    return _RESULT


if __name__ == "__main__":
    print("=" * 64)
    print("INHERITED DISCIPLINE -- analgesic_threshold_logic_v2_0 (DOI 10.5281/zenodo.20733420)")
    print("=" * 64)
    out = run(verbose=True, force=True)
    if out["overall"] != "PASS":
        print("=" * 64)
        print("OVERALL: FAIL", out.get("failed_at", out.get("determinism_drift")))
        sys.exit(1)
    print("[PASS] determinism -- %d frozen hashes match (drift 0)" % len(FROZEN))
    print("=" * 64)
    print("OVERALL: PASS (%d/%d checks)" % (out["checks_passed"], out["checks_total"]))
