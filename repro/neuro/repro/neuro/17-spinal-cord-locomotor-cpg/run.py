#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — slug verification for 17-spinal-cord-locomotor-cpg. Same contract as the §14/§16
neuro slugs: (1) the engine GATE (derived dorsoventral order == measured Briscoe-2000 order;
one material class; CPG complete), (2) DETERMINISM (two runs bit-identical, same sha256),
(3) FIDELITY (regenerated JSON == frozen expected/ to numeric drift 0), and (4) the
exhaustive [F]/[V]/[L]/[O]/[B] ledger is COMPLETE (no ungraded item; every item has a reason;
no silent [O]). Prints SLUG VERIFICATION: PASS/FAIL.
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "_engine"))
EXPECTED = os.path.join(HERE, "expected")
RJSON = "spinal_cpg_results.json"


def number_leaves(o, path="$"):
    out = {}
    if isinstance(o, bool):
        out[path] = ("b", o)
    elif isinstance(o, (int, float)):
        out[path] = ("n", float(o))
    elif isinstance(o, str):
        out[path] = ("s", o)
    elif isinstance(o, dict):
        for k, v in o.items():
            out.update(number_leaves(v, f"{path}.{k}"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(number_leaves(v, f"{path}[{i}]"))
    return out


def _run():
    return subprocess.run([sys.executable, "vp_spinal_cpg.py"], cwd=ENGINE,
                          capture_output=True, text=True, timeout=300)


def main():
    print(f"engine: {ENGINE}")
    gp = os.path.join(ENGINE, RJSON)

    r1 = _run()
    if r1.returncode != 0:
        print(f"  [FAIL] engine exit {r1.returncode}"); print(r1.stderr)
        print("SLUG VERIFICATION: FAIL"); sys.exit(1)
    got = json.load(open(gp, encoding="utf-8"))
    h1 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    r2 = _run()
    h2 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    determ = (h1 == h2)

    gate = bool(got.get("fidelity_pass", False))

    exp = json.load(open(os.path.join(EXPECTED, RJSON), encoding="utf-8"))
    en, gn = number_leaves(exp), number_leaves(got)
    shared = set(en) & set(gn)
    mism = [k for k in shared
            if not (en[k][0] == "n" and gn[k][0] == "n" and abs(en[k][1] - gn[k][1]) <= 1e-9)
            and en[k] != gn[k]]
    fidelity = (len(mism) == 0)

    # exhaustive ledger discipline (C3): no ungraded; every item has reason
    led = got.get("ledger", [])
    counts = got.get("ledger_counts", {})
    grades_ok = all(x.get("grade") in ("F", "V", "L", "O", "B") for x in led)
    reasons_ok = all(x.get("reason") for x in led)
    no_ungraded = counts.get("ungraded", 1) == 0
    ledger_ok = grades_ok and reasons_ok and no_ungraded and len(led) >= 1

    verdict = gate and determ and fidelity and ledger_ok
    print(f"  [{'PASS' if verdict else 'FAIL'}] vp_spinal_cpg.py   "
          f"gate(order==Briscoe; one-material; CPG-complete)={'PASS' if gate else 'FAIL'}  "
          f"determ={'PASS' if determ else 'FAIL'}  "
          f"fidelity={len(shared) - len(mism)}/{len(shared)} leaves  "
          f"ledger[{counts.get('total','?')}: F{counts.get('F','?')}/V{counts.get('V','?')}/"
          f"L{counts.get('L','?')}/O{counts.get('O','?')}/B{counts.get('B','?')}]"
          f"={'OK' if ledger_ok else 'FAIL'}")
    if mism:
        for k in mism[:8]:
            print(f"      drift {k}: expected {en[k]} got {gn[k]}")
    print("=" * 64)
    print("SLUG VERIFICATION: PASS" if verdict else "SLUG VERIFICATION: FAIL")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
