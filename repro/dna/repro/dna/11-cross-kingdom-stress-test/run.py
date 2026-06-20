#!/usr/bin/env python3
# repro/dna/11-cross-kingdom-stress-test/run.py
#   v1.10 research extension (Workstream U: UNIVERSALITY) -- the cross-kingdom generality
#   stress test of the three readable layers (gamma material, M methylation-substrate, E
#   helical), on 12 organisms of real NCBI genomic DNA spanning vertebrates, invertebrates,
#   plants, a fungus, and an AT-extremist protist, plus the histone-H4 ortholog.
#
# Checks (identical discipline to chapters 09/10):
#   (1) the engine prints "ALL GATES: PASS",
#   (2) the regenerated cross_kingdom_results.json matches this folder's frozen expected/
#       to numeric drift 0 (every shared number/bool leaf, |dx| <= 1e-9),
#   (3) determinism: two consecutive runs are bit-identical (same sha256).
# All sequence is READ-ONLY (frozen FASTAs in inputs/ + inputs_ortholog/, NCBI provenance in
# inputs/_provenance.json). gamma is RECOMPUTED from those FASTAs -> the reproduction path is
# in-package (Constitution C1). The reads are pure arithmetic on locked sequence -> deterministic.
# Run from anywhere:  python3 run.py
import os, sys, subprocess, json, hashlib

HERE     = os.path.dirname(os.path.abspath(__file__))
ENGINE   = HERE
EXPECTED = os.path.join(HERE, "expected")
GATE_MARKERS = ("ALL GATES: PASS",)
CASES = [("cross_kingdom_engine.py", "cross_kingdom_results.json")]

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
    return subprocess.run([sys.executable, script], cwd=ENGINE, capture_output=True, text=True, timeout=900)

def main():
    print(f"engine: {ENGINE}")
    ok = True
    for script, rjson in CASES:
        gp = os.path.join(ENGINE, rjson)
        r1 = _run(script)
        gate = any(m in r1.stdout for m in GATE_MARKERS)
        if r1.returncode != 0 or not gate:
            print(f"  [FAIL] {script:26} gate marker missing (exit {r1.returncode})")
            if r1.stderr: print(r1.stderr[-800:])
            ok = False; continue
        h1  = hashlib.sha256(open(gp, "rb").read()).hexdigest()
        got = json.load(open(gp, encoding="utf-8"))
        _run(script)                                       # determinism
        h2  = hashlib.sha256(open(gp, "rb").read()).hexdigest()
        determ = (h1 == h2)
        exp_path = os.path.join(EXPECTED, rjson)
        if os.path.exists(exp_path):
            exp = json.load(open(exp_path, encoding="utf-8"))
            en, gn = number_leaves(exp), number_leaves(got)
            shared = set(en) & set(gn)
            mism = [k for k in shared
                    if not (en[k][0] == "n" and gn[k][0] == "n" and abs(en[k][1]-gn[k][1]) <= 1e-9)
                    and en[k] != gn[k]]
            fidelity = (len(mism) == 0)
            fdesc = f"{len(shared)-len(mism)}/{len(shared)} numbers match"
        else:
            fidelity = False; fdesc = "expected/ MISSING"
        verdict = gate and determ and fidelity
        ok = ok and verdict
        print(f"  [{'PASS' if verdict else 'FAIL'}] {script:26} "
              f"gate=PASS  determ={'PASS' if determ else 'FAIL'}  fidelity={fdesc}")
    print("=" * 62)
    print("SLUG VERIFICATION: PASS" if ok else "SLUG VERIFICATION: FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
