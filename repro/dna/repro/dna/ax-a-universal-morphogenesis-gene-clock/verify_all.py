#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py — ONE command that verifies the ENTIRE
universal_morphogenesis_geneclock package, in the exact style of
neuro_emergence_chain_integrated v1.9's verify_all.py.

Three layers, strictest first to last:

  [1] GATE SUITE       — the five add-only gates must each print
                         "OVERALL: PASS (5/5)" and exit 0. (This is what the
                         package already had, now behind one entry point.)
  [2] SOURCE INTEGRITY — sha256 of every governed source file AND every
                         measured input (the .py engine/verify modules and the
                         measured gamma / Carnegie-stage data) must equal the
                         frozen expected_sha256.json, with ZERO drift. This is
                         the bit-for-bit pin the package was missing: it catches
                         any silent edit to the engine OR to a measured table,
                         which is precisely the invariant the HANDOFF demands
                         ("data/*_gamma.json must keep the measured gamma
                         bit-for-bit; never tuned").
  [3] FIDELITY         — the gate-regenerated results/*_verify.json must equal
                         the frozen repro/morpho/expected/*.json leaf-for-leaf
                         (every pass_ bool and every msg string identical). This
                         catches cross-session numeric drift even when a single
                         run is still internally deterministic — the one thing
                         a per-run 2x-sha check cannot see.

Phase 4 systemic-recovery fold-in (add-only) adds, without disturbing the three
layers above:

  [1b] EMERGENCE GATES — the three folded-in gates under code/emergence_v2/
                         (verify_emergence / _organs / _trajectory) must each
                         print their native "OVERALL: N/N -> PASS". They are
                         pinned bit-for-bit by [2] (governed_files walks all of
                         code/, so the folded-in .py/.json are pinned too).
  [3b] EMERGENCE FIDELITY — those gates emit no results/*.json, so the
                         cross-session numeric pin is each gate's headline PASS
                         count plus the engine's self-reported deterministic
                         result-hash, frozen in
                         repro/morpho/expected/emergence_gate_baseline.json.

Usage (from the package root):
    python3 verify_all.py                 # verify; exit 0 only if all pass
    python3 verify_all.py --freeze        # re-record the frozen baseline after
                                          #   an INTENTIONAL, gate-passing change
    python3 verify_all.py --list          # list the governed/pinned file set

The freeze workflow mirrors neuro's "delete the key, run once to record, run
again to confirm": --freeze re-runs the gates, refuses to freeze unless they
pass, then writes expected_sha256.json + repro/morpho/expected/. Re-freezing is
always a DELIBERATE act, never automatic.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(ROOT, "code")
RESULTS = os.path.join(ROOT, "results")
EXPECTED_DIR = os.path.join(ROOT, "repro", "morpho", "expected")
SHA_FILE = os.path.join(ROOT, "expected_sha256.json")

# (gate module stem, the results/*.json it regenerates)
GATES = [
    ("verify_gene_clock",  "gene_clock_verify.json"),
    ("verify_morpho_plus", "morpho_plus_verify.json"),
    ("verify_adipose",     "adipose_verify.json"),
    ("verify_dev_timing",  "dev_timing_verify.json"),
    ("verify_timing_predictors", "timing_predictors_verify.json"),
    ("verify_dev_timing_wide", "dev_timing_wide_verify.json"),
    ("verify_dev_timing_robust", "dev_timing_robust_verify.json"),
    ("verify_morpho_decomposition", "morpho_decomposition_verify.json"),
    ("verify_life_course", "life_course_verify.json"),
    ("verify_organ_timing", "organ_timing_verify.json"),
    ("verify_organ_anatomy", "organ_anatomy_verify.json"),
    ("verify_heart_substages", "heart_substages_verify.json"),
]

# ----------------------------------------------------------------------------
# Phase 4 systemic-recovery fold-in (add-only): the three emergence gates.
# Each lives under code/emergence_v2/ and is location-independent (loads its
# engine + param_db via __file__), so it runs correctly from cwd=code/ with a
# sub-path stem. They are pinned bit-for-bit by layer [2] automatically; their
# numeric fidelity baseline (no JSON emitted) lives in EMERGENCE_BASELINE.
# (stem relative to code/, baseline label)
EMERGENCE_GATES = [
    ("emergence_v2/verify_emergence",            "emergence_heart"),
    ("emergence_v2/verify_emergence_organs",     "emergence_organs"),
    ("emergence_v2/verify_emergence_trajectory", "emergence_trajectory"),
    ("emergence_v2/verify_emergence_organs_wide", "emergence_organs_wide"),
    ("emergence_v2/verify_emergence_morphogen",  "emergence_morphogen"),
]
EMERGENCE_BASELINE = os.path.join(EXPECTED_DIR, "emergence_gate_baseline.json")

# ----------------------------------------------------------------------------
# governed source + measured-input set (the bit-for-bit pinned set)
# ----------------------------------------------------------------------------
def governed_files():
    """Every .py and every measured-input .json under code/, repo-relative.

    Demos and fetch scripts are included on purpose: under VP-SPEC bit-for-bit
    governance, ANY change to the released code is re-frozen deliberately, not
    silently tolerated. The .json set is the measured-input pin (gamma tables,
    Carnegie stages, promoter caches)."""
    out = []
    for dirpath, _dirs, names in os.walk(CODE):
        for n in sorted(names):
            if n.endswith(".py") or n.endswith(".json"):
                out.append(os.path.relpath(os.path.join(dirpath, n), ROOT))
    return sorted(out)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_shas():
    return {f: sha256_file(os.path.join(ROOT, f)) for f in governed_files()}


# ----------------------------------------------------------------------------
# JSON leaf diff (numeric leaves to tolerance; bool/str exact) — neuro slug style
# ----------------------------------------------------------------------------
def leaves(o, path="$"):
    out = {}
    if isinstance(o, bool):
        out[path] = ("b", o)
    elif isinstance(o, (int, float)):
        out[path] = ("n", float(o))
    elif isinstance(o, str):
        out[path] = ("s", o)
    elif isinstance(o, dict):
        for k, v in o.items():
            out.update(leaves(v, f"{path}.{k}"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(leaves(v, f"{path}[{i}]"))
    elif o is None:
        out[path] = ("z", None)
    return out


def diff_json(expected, got, tol=1e-9):
    en, gn = leaves(expected), leaves(got)
    drift = []
    for k in sorted(set(en) | set(gn)):
        if k not in en:
            drift.append((k, "MISSING_IN_FROZEN", gn[k]))
        elif k not in gn:
            drift.append((k, en[k], "MISSING_IN_REGEN"))
        else:
            te, ve = en[k]
            tg, vg = gn[k]
            if te == "n" and tg == "n":
                if abs(ve - vg) > tol:
                    drift.append((k, en[k], gn[k]))
            elif en[k] != gn[k]:
                drift.append((k, en[k], gn[k]))
    return drift


# ----------------------------------------------------------------------------
# [1] gate suite
# ----------------------------------------------------------------------------
def gate_passed(stdout):
    """True if a gate reported success in EITHER convention. The morpho gates
    print 'OVERALL: PASS (5/5 ...)'; the folded-in emergence gates print
    'OVERALL: 7/7 -> PASS'. An OVERALL: FAIL in either form vetoes."""
    if "OVERALL: FAIL" in stdout:
        return False
    if "OVERALL: PASS" in stdout:
        return True
    return re.search(r"OVERALL:\s*\d+\s*/\s*\d+\s*->\s*PASS", stdout) is not None


def emergence_fingerprint(stdout):
    """Cross-session fidelity pin for an emergence gate that emits no JSON:
    its headline PASS count plus the engine's self-reported deterministic
    result-hash(es) (12-hex). Both are numeric invariants of the run, robust to
    float-formatting noise, and change iff the underlying science changes."""
    m = re.search(r"OVERALL:\s*(\d+)\s*/\s*(\d+)\s*->\s*PASS", stdout)
    counts = f"{m.group(1)}/{m.group(2)}" if m else None
    shas = sorted(set(re.findall(r"\b[0-9a-f]{12}\b", stdout)))
    return {"counts": counts, "shas": shas}


def run_gate(stem):
    p = subprocess.run([sys.executable, f"{stem}.py"], cwd=CODE,
                       capture_output=True, text=True, timeout=900)
    ok = (p.returncode == 0) and gate_passed(p.stdout)
    last = [ln for ln in (p.stdout or p.stderr).strip().splitlines()
            if "OVERALL" in ln]
    tail = last[-1] if last else (p.stdout or p.stderr).strip().splitlines()[-1:] or [""]
    return ok, (tail if isinstance(tail, str) else (tail[0] if tail else "")), p


# ----------------------------------------------------------------------------
# verify
# ----------------------------------------------------------------------------
def verify():
    results = []
    print("=" * 78)
    print("UNIVERSAL MORPHOGENESIS / GENE-CLOCK — full verification")
    print("=" * 78)

    # [1] gates (these also regenerate results/*_verify.json for layer [3])
    print("\n[1] gate suite (each must print OVERALL: PASS 5/5)")
    for stem, _json in GATES:
        ok, tail, _p = run_gate(stem)
        results.append((f"gate {stem}", ok, tail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {stem:24s} {tail[:48]}")

    # [1b] folded-in systemic-recovery emergence gates (Phase 4, add-only).
    # Each runs in place under code/emergence_v2/ (location-independent via
    # __file__); pinned bit-for-bit by [2]; numeric baseline checked in [3b].
    print("\n[1b] emergence gate suite (systemic-recovery fold-in; OVERALL: N/N -> PASS)")
    emergence_runs = {}
    for stem, label in EMERGENCE_GATES:
        ok, tail, p = run_gate(stem)
        emergence_runs[label] = p.stdout
        results.append((f"emergence {label}", ok, tail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:22s} {tail[:52]}")

    # [2] source integrity (bit-for-bit pin over engine + measured inputs)
    print("\n[2] source integrity (sha256 pin: engine + measured gamma/stage data)")
    if not os.path.exists(SHA_FILE):
        results.append(("source_integrity", False,
                        "expected_sha256.json missing — run --freeze"))
        print("  [FAIL] expected_sha256.json missing — run: python3 verify_all.py --freeze")
    else:
        frozen = json.load(open(SHA_FILE, encoding="utf-8"))
        current = compute_shas()
        added = sorted(set(current) - set(frozen))
        removed = sorted(set(frozen) - set(current))
        changed = sorted(f for f in (set(current) & set(frozen))
                         if current[f] != frozen[f])
        ok = not (added or removed or changed)
        npin = len(frozen)
        msg = (f"{npin} files pinned, drift 0"
               if ok else
               f"DRIFT changed={len(changed)} added={len(added)} removed={len(removed)}")
        results.append(("source_integrity", ok, msg))
        print(f"  [{'PASS' if ok else 'FAIL'}] {msg}")
        for f in changed[:8]:
            print(f"      changed: {f}")
        for f in added[:8]:
            print(f"      added (unpinned): {f}")
        for f in removed[:8]:
            print(f"      removed (was pinned): {f}")

    # [3] fidelity (regenerated verify-JSON == frozen expected/, leaf drift 0)
    print("\n[3] fidelity (regenerated results vs frozen repro/morpho/expected, drift 0)")
    if not os.path.isdir(EXPECTED_DIR):
        results.append(("fidelity", False,
                        "repro/morpho/expected missing — run --freeze"))
        print("  [FAIL] repro/morpho/expected/ missing — run: python3 verify_all.py --freeze")
    else:
        all_ok = True
        for _stem, jname in GATES:
            regen_p = os.path.join(RESULTS, jname)
            froz_p = os.path.join(EXPECTED_DIR, jname)
            if not os.path.exists(froz_p):
                all_ok = False
                print(f"  [FAIL] {jname:26s} no frozen baseline")
                continue
            if not os.path.exists(regen_p):
                all_ok = False
                print(f"  [FAIL] {jname:26s} gate did not regenerate it")
                continue
            drift = diff_json(json.load(open(froz_p, encoding="utf-8")),
                              json.load(open(regen_p, encoding="utf-8")))
            ok = not drift
            all_ok &= ok
            nleaf = len(leaves(json.load(open(froz_p, encoding="utf-8"))))
            print(f"  [{'PASS' if ok else 'FAIL'}] {jname:26s} {nleaf - len(drift)}/{nleaf} leaves match")
            for k, e, g in drift[:6]:
                print(f"      drift {k}: frozen={e} regen={g}")
        results.append(("fidelity", all_ok,
                        "all verify-JSON match frozen" if all_ok else "DRIFT"))

    # [3b] emergence fidelity: each emergence gate's (PASS count + engine
    # result-hash) fingerprint must equal the frozen baseline. This is the
    # cross-session numeric pin for the JSON-less emergence gates, mirroring [3].
    print("\n[3b] emergence fidelity (PASS count + engine result-hash vs frozen baseline)")
    if not os.path.exists(EMERGENCE_BASELINE):
        results.append(("emergence_fidelity", False,
                        "emergence_gate_baseline.json missing — run --freeze"))
        print("  [FAIL] emergence_gate_baseline.json missing — run: python3 verify_all.py --freeze")
    else:
        frozen_e = json.load(open(EMERGENCE_BASELINE, encoding="utf-8"))
        e_ok = True
        for _stem, label in EMERGENCE_GATES:
            got = emergence_fingerprint(emergence_runs.get(label, ""))
            exp = frozen_e.get(label)
            ok = (exp == got)
            e_ok &= ok
            shown = f"{got.get('counts')} sha={','.join(got.get('shas') or [])}"
            print(f"  [{'PASS' if ok else 'FAIL'}] {label:22s} {shown}")
            if not ok:
                print(f"      drift: frozen={exp} regen={got}")
        results.append(("emergence_fidelity", e_ok,
                        "all emergence fingerprints match frozen" if e_ok else "DRIFT"))

    npass = sum(1 for _, ok, _ in results if ok)
    verdict = all(ok for _, ok, _ in results)
    print("\n" + "=" * 78)
    print(f"OVERALL: {'PASS' if verdict else 'FAIL'}  ({npass}/{len(results)} checks)")
    print("=" * 78)
    return verdict


# ----------------------------------------------------------------------------
# freeze (deliberate re-record of the baseline)
# ----------------------------------------------------------------------------
def freeze():
    print("Re-freeze requested. Running ALL gates first (will not freeze unless every gate passes)...")
    failed = []
    for stem, _json in GATES:
        ok, tail, _p = run_gate(stem)
        print(f"  [{'PASS' if ok else 'FAIL'}] {stem:24s} {tail[:48]}")
        if not ok:
            failed.append(stem)
    emergence_runs = {}
    for stem, label in EMERGENCE_GATES:
        ok, tail, p = run_gate(stem)
        emergence_runs[label] = p.stdout
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:24s} {tail[:48]}")
        if not ok:
            failed.append(label)
    if failed:
        print(f"\nREFUSING to freeze: gates not passing: {', '.join(failed)}")
        sys.exit(1)

    # [2] write expected_sha256.json (now also pins the folded-in code/ files)
    shas = compute_shas()
    with open(SHA_FILE, "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print(f"\nfroze source pin: {len(shas)} files -> {os.path.relpath(SHA_FILE, ROOT)}")

    # [3] morpho fidelity baselines. Preserve any EXISTING baseline byte-for-byte
    # (add-only: a fold-in must not perturb a frozen morpho baseline); only write
    # a baseline that is missing.
    os.makedirs(EXPECTED_DIR, exist_ok=True)
    for _stem, jname in GATES:
        src = os.path.join(RESULTS, jname)
        dst = os.path.join(EXPECTED_DIR, jname)
        if os.path.exists(dst):
            print(f"kept existing fidelity baseline (unchanged): {jname}")
        elif os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"froze fidelity baseline: {jname}")
        else:
            print(f"WARNING: {jname} not produced by its gate — fidelity baseline incomplete")

    # [3b] emergence fidelity baseline (PASS count + engine result-hash)
    e_base = {label: emergence_fingerprint(emergence_runs[label])
              for _stem, label in EMERGENCE_GATES}
    with open(EMERGENCE_BASELINE, "w", encoding="utf-8") as f:
        json.dump(e_base, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print(f"froze emergence baseline: {os.path.relpath(EMERGENCE_BASELINE, ROOT)} "
          f"({len(e_base)} gates)")
    print("\nBaseline frozen. Re-run `python3 verify_all.py` to confirm OVERALL: PASS.")


def main():
    ap = argparse.ArgumentParser(description="universal_morphogenesis_geneclock single-entry verifier")
    ap.add_argument("--freeze", action="store_true",
                    help="re-record the frozen baseline after an intentional, gate-passing change")
    ap.add_argument("--list", action="store_true", help="list the governed/pinned file set and exit")
    args = ap.parse_args()
    if args.list:
        for f in governed_files():
            print(f)
        return
    if args.freeze:
        freeze()
        return
    sys.exit(0 if verify() else 1)


if __name__ == "__main__":
    main()
