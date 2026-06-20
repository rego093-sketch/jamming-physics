#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_modules.py  --  harness for the v0.19.0 inherited modules + the v0.24.0 native scoreboard.

  Inherited from analgesic_threshold_logic_v2_0 (DOI 10.5281/zenodo.20733420):
    M10 -> pipeline/prioritise_diseases.py   (burden-weighted DISEASE prioritisation)
    M11 -> pipeline/indirect_lever_gate.py   (indirect-lever honesty gate, fail-closed)
    M5v2-> pipeline/claim_scanner_v2.py      (hardened claim scan: negation guard + self-test +
                                              new-module scope)
  Native to this kit (ROADMAP II-A/III-A2/III-A, added v0.24.0 / v0.28.0):
    II-A  -> pipeline/direction_recovery.py   (direction-recovery scoreboard: is the forced
                                               role x mechanism direction recovered by the lead
                                               agent, disease by disease; fail-closed; read-only)
    III-A2-> pipeline/repurposing_scanner.py  (cross-disease repurposing scanner: same-axis approved
                                               donor -> candidate corrective-direction for a
                                               no-approved recipient; fail-closed; read-only)
    III-A -> pipeline/open_directions_card.py (no-approved tail as actionable, falsifiable cards;
                                               fail-closed; read-only over the scanner + falsifiers)

After the modules, ROADMAP IV-A builds the canonical retrieval-ready site (pipeline/build_site.py:
banner-first, answer-first, JSON-LD, robots/sitemap/llms) deterministically from the frozen scanner
+ cards, and freezes repro/expected_site_sha256.json.

Runs each module fail-closed, regenerates its expected/ output, then FREEZES every output's
sha256 against repro/expected_modules_sha256.json (drift 0).  This is a SEPARATE freeze from the
per-disease repro/expected_sha256.json, so the frozen disease hashes are never touched.

Run:  python3 repro/modules/run_modules.py
"""
import os, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))                 # repro/modules
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PIPELINE = os.path.join(ROOT, "pipeline")
EXPECTED = os.path.join(HERE, "expected")
FREEZE = os.path.join(ROOT, "repro", "expected_modules_sha256.json")

MODULES = [
    ("M10 burden-prioritisation", "prioritise_diseases.py", "disease_priority_ranking.json"),
    ("M11 indirect-lever gate",   "indirect_lever_gate.py", "indirect_lever_honesty.json"),
    ("II-A direction-recovery (native)", "direction_recovery.py", "direction_recovery.json"),
    ("III-A2 repurposing-scanner (native)", "repurposing_scanner.py", "repurposing_hypotheses.json"),
    ("III-A open-directions-cards (native)", "open_directions_card.py", "open_directions_cards.json"),
    ("M5v2 hardened claim-scan",  "claim_scanner_v2.py",    "claim_scan_v2.json"),
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(script, args):
    return subprocess.run([sys.executable, os.path.join(PIPELINE, script), *args],
                          cwd=ROOT, capture_output=True, text=True)


def main():
    print("#" * 64)
    print("# VP DISEASE EMERGENCE KIT  --  inherited modules (analgesic M10/M11/M5v2) + native II-A")
    print("#" * 64)

    # the scanner (M5v2) must run AFTER every module it scans (incl. native II-A) -> order is fixed above.
    for label, script, _out in MODULES:
        r = run(script, ["--write"])
        sys.stdout.write(r.stdout)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        ok = (r.returncode == 0) and ("PASS" in r.stdout or "wrote" in r.stdout)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            print(f"\nOVERALL: FAIL at {label}")
            sys.exit(1)

    # determinism freeze (separate from the per-disease freeze)
    print("\n[freeze] sha256 of each module output")
    cur = {out: sha(os.path.join(EXPECTED, out)) for _l, _s, out in MODULES}
    if os.path.exists(FREEZE):
        exp = json.load(open(FREEZE))
        drift = [k for k in cur if k in exp and exp[k] != cur[k]]
        new = [k for k in cur if k not in exp]
        if drift:
            for k in drift:
                print(f"  [DRIFT] {k}: expected {exp.get(k,'-')[:12]} got {cur[k][:12]}")
            print("\nOVERALL: FAIL -- module hash drift")
            sys.exit(1)
        for k in sorted(cur):
            print(f"  [PASS] {k:34s} {cur[k][:12]}")
        if new:
            exp.update({k: cur[k] for k in new})
            json.dump(exp, open(FREEZE, "w"), indent=1, sort_keys=True)
            print(f"  [ADD] appended {len(new)} new module hash(es)")
        print(f"  -> {len(cur)} module hashes match (drift 0)")
    else:
        json.dump(cur, open(FREEZE, "w"), indent=1, sort_keys=True)
        for k in sorted(cur):
            print(f"  [INIT] {k:34s} {cur[k][:12]}")
        print(f"  -> wrote expected_modules_sha256.json ({len(cur)} hashes); re-run to verify drift 0")

    # ---- ROADMAP IV-A: canonical retrieval-ready site (deterministic over the frozen scanner+cards) ----
    # build_site.py runs its OWN byte-identical-rebuild self-test (in-run determinism); here we add a
    # cross-run drift guard against repro/expected_site_sha256.json.
    print("\n[site] ROADMAP IV-A canonical site (banner-first, answer-first, JSON-LD, robots/sitemap/llms)")
    SITE_FREEZE = os.path.join(ROOT, "repro", "expected_site_sha256.json")
    old_site = None
    if os.path.exists(SITE_FREEZE):
        old_site = json.load(open(SITE_FREEZE)).get("sha256")
    r = run("build_site.py", ["--write"])
    sys.stdout.write(r.stdout)
    if r.returncode != 0 or "OVERALL: PASS" not in r.stdout:
        sys.stderr.write(r.stderr)
        print("\nOVERALL: FAIL at site build (IV-A)")
        sys.exit(1)
    new_site = json.load(open(SITE_FREEZE)).get("sha256", {})
    if old_site is not None:
        site_drift = [k for k in new_site if k in old_site and old_site[k] != new_site[k]]
        if site_drift:
            for k in site_drift:
                print(f"  [DRIFT] site/{k}: expected {old_site[k][:12]} got {new_site[k][:12]}")
            print("\nOVERALL: FAIL -- site hash drift")
            sys.exit(1)
        for k in sorted(new_site):
            print(f"  [PASS] site/{k:12s} {new_site[k][:12]}")
        print(f"  -> {len(new_site)} site hashes match (drift 0)")
    else:
        for k in sorted(new_site):
            print(f"  [INIT] site/{k:12s} {new_site[k][:12]}")
        print(f"  -> wrote expected_site_sha256.json ({len(new_site)} hashes); re-run to verify drift 0")

    print("\n" + "#" * 64)
    print(f"OVERALL: PASS ({len(MODULES)}/{len(MODULES)} modules: 3 inherited + 3 native "
          f"[II-A, III-A2, III-A]; {len(cur)} module hashes) + IV-A site ({len(new_site)} files)")
    print("#" * 64)


if __name__ == "__main__":
    main()
