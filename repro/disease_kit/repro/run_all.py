#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  VP Disease Emergence Kit  --  master reproduction harness.

From the package root:   python3 repro/run_all.py
Runs fully OFFLINE using the bundled NCBI promoter cache (fetch/cache/). Network is
needed only if you add a NEW gene whose promoter is not yet cached.

Pipeline (executed in dependency order; fail-closed at the first failure):

    S1  engine self-test        R19 substrate identity + bistability + gamma/emergence determinism
    S2  emerge + treat (--all)  for every registered disease:
                                  NCBI DNA -> emerge_disease (R19 perturbation read)
                                           -> treatment_switch  (pathway A)
                                           -> treatment_chem    (pathway B, if candidates)
                                           -> honesty_gate       (claim scan + falsifier register)
                                -> diseases/<slug>/analysis.json
    S3  honesty gate (global)   every RESOLVED disease must carry OVERALL: PASS
    S4  determinism freeze      sha256 of every analysis.json; compare to
                                repro/expected_sha256.json (or write it on first run)
    S5  modules + site          inherited (M10/M11/M5v2) + native (II-A/III-A2/III-A) modules and the
                                ROADMAP IV-A canonical site, each READ-ONLY over the frozen artifacts
                                with their OWN separate freezes (per-disease freeze never touched)
    S6  system-inheritance      ROADMAP V: for each multi-system INTRACTABLE disease, inherit the REAL
                                measured organ-master γ of every affected sibling system and surface
                                which compartments the lead corrective lever REACHES vs leaves as a GAP
                                (the next direction); read-only, own freeze

A SUSPENDED disease (no analyzable single-gene DNA, e.g. a whole-chromosome dosage
disorder) is NOT a failure: it is an honest hold, recorded in its analysis.json and
counted separately.
"""
import os, sys, json, hashlib, subprocess

REPRO = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(REPRO, ".."))
PIPELINE = os.path.join(ROOT, "pipeline")
DISEASES = os.path.join(ROOT, "diseases")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(script_path, args, cwd):
    return subprocess.run([sys.executable, script_path, *args],
                          cwd=cwd, capture_output=True, text=True)


def main():
    checks = 0
    print("#" * 64)
    print("# VP DISEASE EMERGENCE KIT  --  run_all.py  (offline reproduction)")
    print("#" * 64)

    # ---- S1: engine self-test -------------------------------------------------
    print("\n[S1] engine self-test")
    r = run(os.path.join(REPRO, "engine_selftest.py"), [], REPRO)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        print("\nOVERALL: FAIL at S1 (engine self-test)")
        sys.exit(1)
    checks += 1

    # ---- S2: emerge + treat every disease ------------------------------------
    print("\n[S2] emerge + treat (--all --offline)")
    r = run(os.path.join(PIPELINE, "analyze_disease.py"), ["--all", "--offline"], PIPELINE)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        print("\nOVERALL: FAIL at S2 (analysis)")
        sys.exit(1)
    checks += 1

    # collect produced artifacts
    registry = json.load(open(os.path.join(DISEASES, "_registry.json"), encoding="utf-8"))
    slugs = list(registry["diseases"].keys())
    artifacts = {}
    for slug in slugs:
        p = os.path.join(DISEASES, slug, "analysis.json")
        if not os.path.exists(p):
            print(f"\nOVERALL: FAIL — missing artifact for '{slug}'")
            sys.exit(1)
        artifacts[slug] = (p, json.load(open(p, encoding="utf-8")))

    # ---- S3: global honesty gate ---------------------------------------------
    print("\n[S3] global honesty gate (every RESOLVED disease must PASS)")
    resolved = suspended = 0
    for slug, (_p, a) in artifacts.items():
        if a.get("status") == "SUSPENDED":
            suspended += 1
            print(f"  [HOLD] {slug:18s} suspended (honest hold; not counted as failure)")
            continue
        resolved += 1
        gate = a.get("honesty_gates", {}).get("OVERALL")
        ok = (gate == "PASS")
        print(f"  [{'PASS' if ok else 'FAIL'}] {slug:18s} honesty_gates OVERALL={gate}")
        if not ok:
            print(f"\nOVERALL: FAIL — honesty gate not PASS for '{slug}'")
            sys.exit(1)
    print(f"  -> {resolved} resolved (all gates PASS), {suspended} suspended (held)")
    checks += 1

    # ---- S4: determinism freeze ----------------------------------------------
    print("\n[S4] determinism freeze (sha256 of each analysis.json)")
    cur = {slug: sha(p) for slug, (p, _a) in sorted(artifacts.items())}
    exp_path = os.path.join(REPRO, "expected_sha256.json")
    if os.path.exists(exp_path):
        exp = json.load(open(exp_path))
        # DRIFT = an ALREADY-FROZEN disease whose hash changed (a real regression).
        # NEW   = a disease not yet in the freeze -> appended on first sight, never a failure.
        # (A brand-new disease must be compared only against itself once frozen; before that it
        #  has no expected hash, so it is 'new', not 'drift'.)
        drift = [s for s in cur if s in exp and exp[s] != cur[s]]
        new = [s for s in cur if s not in exp]
        if drift:
            for s in drift:
                print(f"  [DRIFT] {s}: expected {exp.get(s,'-')[:12]} got {cur[s][:12]}")
            print("\nOVERALL: FAIL — determinism hash drift")
            sys.exit(1)
        for s in cur:
            print(f"  [PASS] {s:18s} {cur[s][:12]}")
        if new:
            # new disease added since freeze: append, don't fail
            exp.update({s: cur[s] for s in new})
            json.dump(exp, open(exp_path, "w"), indent=1, sort_keys=True)
            print(f"  [ADD] appended {len(new)} new disease hash(es) to expected_sha256.json")
        print(f"  -> {len(cur)} frozen hashes match (drift 0)")
    else:
        json.dump(cur, open(exp_path, "w"), indent=1, sort_keys=True)
        for s in cur:
            print(f"  [INIT] {s:18s} {cur[s][:12]}")
        print(f"  -> wrote expected_sha256.json ({len(cur)} hashes); re-run to verify drift 0")
    checks += 1

    # ---- S5: inherited modules (analgesic M10/M11/M5v2) + native II-A scoreboard ----
    # These READ the frozen artifacts above and produce their OWN frozen outputs, so the
    # per-disease freeze (S4) is never disturbed. DOI 10.5281/zenodo.20733420.
    print("\n[S5] modules (burden-prioritisation + indirect-lever gate + direction-recovery scoreboard + hardened scan)")
    r = run(os.path.join(REPRO, "modules", "run_modules.py"), [], ROOT)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        print("\nOVERALL: FAIL at S5 (modules)")
        sys.exit(1)
    checks += 1

    # ---- S6: multi-system inheritance layer (ROADMAP V, native) ----------------------
    # READS the frozen per-disease analysis.json + the vendored sibling_registry / manifest and
    # produces its OWN frozen output (system_inheritance/system_inheritance_map.json), so the
    # per-disease freeze (S4), the module freeze (S5) and the site freeze are all untouched.  The
    # module runs its own byte-identical-rebuild + provenance/firewall/exclusion teeth; here we add a
    # cross-run drift guard against repro/expected_system_inheritance_sha256.json.
    print("\n[S6] multi-system inheritance (intractable disease: inherit organ-system γ + reach/gap directions)")
    SI_FREEZE = os.path.join(REPRO, "expected_system_inheritance_sha256.json")
    old_si = json.load(open(SI_FREEZE)).get("sha256") if os.path.exists(SI_FREEZE) else None
    r = run(os.path.join(PIPELINE, "system_inheritance.py"), ["--write"], ROOT)
    sys.stdout.write(r.stdout)
    if r.returncode != 0 or "OVERALL: PASS" not in r.stdout:
        sys.stderr.write(r.stderr)
        print("\nOVERALL: FAIL at S6 (system-inheritance)")
        sys.exit(1)
    new_si = json.load(open(SI_FREEZE)).get("sha256", {})
    if old_si is not None:
        si_drift = [k for k in new_si if k in old_si and old_si[k] != new_si[k]]
        if si_drift:
            for k in si_drift:
                print(f"  [DRIFT] {k}: expected {old_si[k][:12]} got {new_si[k][:12]}")
            print("\nOVERALL: FAIL -- system-inheritance hash drift")
            sys.exit(1)
        for k in sorted(new_si):
            print(f"  [PASS] {k:46s} {new_si[k][:12]}")
        print(f"  -> {len(new_si)} system-inheritance hash(es) match (drift 0)")
    else:
        for k in sorted(new_si):
            print(f"  [INIT] {k:46s} {new_si[k][:12]}")
        print(f"  -> wrote expected_system_inheritance_sha256.json ({len(new_si)} hash(es)); re-run to verify drift 0")
    checks += 1

    print("\n" + "#" * 64)
    print(f"OVERALL: PASS ({checks}/6 stages; {resolved} resolved, {suspended} suspended)")
    print("#" * 64)


if __name__ == "__main__":
    main()
