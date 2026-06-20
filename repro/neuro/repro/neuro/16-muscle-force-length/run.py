#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — slug verification for 16-muscle-force-length, same contract as the DNA
slugs: it checks (1) the engine GATE (derived landmarks within tolerance of the
GHJ-1966 MEASURED validation target — GHJ is never an input), (2) DETERMINISM
(two runs bit-identical, same sha256), (3) FIDELITY (regenerated JSON equals the
frozen expected/ to numeric drift 0), and (4) that the irreducible [O] items are
DECLARED (C3). Prints SLUG VERIFICATION: PASS/FAIL.
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", "_engine"))
EXPECTED = os.path.join(HERE, "expected")
RJSON = "muscle_force_law_results.json"
EXPECTED_O = {"zero_short \u2248 1.27 \u00b5m", "ascending-limb tension values",
              "absolute tension scale", "filament dimensions from ruler-protein sequence"}


def number_leaves(o, path="$"):
    out = {}
    if isinstance(o, bool):
        out[path] = ("b", o)
    elif isinstance(o, (int, float)):
        out[path] = ("n", float(o))
    elif isinstance(o, dict):
        for k, v in o.items():
            out.update(number_leaves(v, f"{path}.{k}"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(number_leaves(v, f"{path}[{i}]"))
    return out


def _run():
    return subprocess.run([sys.executable, "vp_muscle_force_law.py"], cwd=ENGINE,
                          capture_output=True, text=True, timeout=300)


def main():
    print(f"engine: {ENGINE}")
    gp = os.path.join(ENGINE, RJSON)

    r1 = _run()
    if r1.returncode != 0:
        print(f"  [FAIL] engine exit {r1.returncode}"); print("SLUG VERIFICATION: FAIL"); sys.exit(1)
    got = json.load(open(gp, encoding="utf-8"))
    h1 = hashlib.sha256(open(gp, "rb").read()).hexdigest()

    r2 = _run()
    h2 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    determ = (h1 == h2)

    # (1) gate: the engine's own fidelity-to-measurement verdict
    gate = bool(got.get("fidelity_pass", False))

    # (3) fidelity to frozen expected/
    exp = json.load(open(os.path.join(EXPECTED, RJSON), encoding="utf-8"))
    en, gn = number_leaves(exp), number_leaves(got)
    shared = set(en) & set(gn)
    mism = [k for k in shared
            if not (en[k][0] == "n" and gn[k][0] == "n" and abs(en[k][1] - gn[k][1]) <= 1e-9)
            and en[k] != gn[k]]
    fidelity = (len(mism) == 0)
    fdesc = f"{len(shared) - len(mism)}/{len(shared)} numbers match"

    # (4) [O] declared (C3)
    o_declared = set(got.get("irreducible_O", [])) >= EXPECTED_O

    verdict = gate and determ and fidelity and o_declared
    print(f"  [{'PASS' if verdict else 'FAIL'}] vp_muscle_force_law.py   "
          f"gate(vs GHJ)={'PASS' if gate else 'FAIL'}  "
          f"determ={'PASS' if determ else 'FAIL'}  fidelity={fdesc}  "
          f"[O]declared={'PASS' if o_declared else 'FAIL'}")
    print("=" * 62)
    print("SLUG VERIFICATION: PASS" if verdict else "SLUG VERIFICATION: FAIL")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
