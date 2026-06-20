#!/usr/bin/env python3
# repro/dna/lactase-three-layer-stack/run.py
#   v1.9 research extension -- the COMPLETE lactase interpretation across three layers
#   (gamma -> M -> E) with an exhaustive [F]/[O] ledger: closing the gray zone.
#
# Checks: (1) engine prints "ALL GATES: PASS", (2) regenerated results match frozen
# expected/ to numeric drift 0, (3) determinism (2x run bit-identical).
# gamma + measured features are READ-ONLY (frozen in ../_engine/data/lactase_interpretation.json);
# dynamics are pure arithmetic on locked gamma -> deterministic.
import os, sys, subprocess, json, hashlib

HERE     = os.path.dirname(os.path.abspath(__file__))
ENGINE   = os.path.normpath(os.path.join(HERE, "..", "_engine"))
EXPECTED = os.path.join(HERE, "expected")
GATE_MARKERS = ("ALL GATES: PASS",)
CASES = [("lactase_three_layer_4d.py", "lactase_three_layer_results.json")]

def number_leaves(o, path="$"):
    out = {}
    if isinstance(o, bool):                 out[path] = ("b", o)
    elif isinstance(o, (int, float)):       out[path] = ("n", float(o))
    elif isinstance(o, dict):
        for k, v in o.items():              out.update(number_leaves(v, f"{path}.{k}"))
    elif isinstance(o, list):
        for i, v in enumerate(o):           out.update(number_leaves(v, f"{path}[{i}]"))
    return out

def _run(script):
    return subprocess.run([sys.executable, script], cwd=ENGINE, capture_output=True, text=True, timeout=600)

def main():
    print(f"engine: {ENGINE}")
    ok = True
    for script, rjson in CASES:
        gp = os.path.join(ENGINE, rjson)
        r1 = _run(script)
        gate = any(m in r1.stdout for m in GATE_MARKERS)
        if r1.returncode != 0 or not gate:
            print(f"  [FAIL] {script:30} gate marker missing (exit {r1.returncode})"); ok = False; continue
        h1 = hashlib.sha256(open(gp, "rb").read()).hexdigest(); got = json.load(open(gp, encoding="utf-8"))
        _run(script); h2 = hashlib.sha256(open(gp, "rb").read()).hexdigest(); determ = (h1 == h2)
        exp_path = os.path.join(EXPECTED, rjson)
        if os.path.exists(exp_path):
            exp = json.load(open(exp_path, encoding="utf-8"))
            en, gn = number_leaves(exp), number_leaves(got); shared = set(en) & set(gn)
            mism = [k for k in shared if not (en[k][0]=="n" and gn[k][0]=="n" and abs(en[k][1]-gn[k][1])<=1e-9) and en[k]!=gn[k]]
            fidelity = (len(mism) == 0); fdesc = f"{len(shared)-len(mism)}/{len(shared)} numbers match"
        else:
            fidelity = False; fdesc = "expected/ MISSING"
        verdict = gate and determ and fidelity; ok = ok and verdict
        print(f"  [{'PASS' if verdict else 'FAIL'}] {script:30} gate=PASS  determ={'PASS' if determ else 'FAIL'}  fidelity={fdesc}")
    print("=" * 62)
    print("SLUG VERIFICATION: PASS" if ok else "SLUG VERIFICATION: FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
