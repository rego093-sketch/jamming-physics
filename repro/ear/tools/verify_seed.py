#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_seed.py — the one-command gate for a VP emergence SEED package.

Run from the package root:   python3 tools/verify_seed.py
Reads  seed.json  (the package's self-description) and asserts these, in order:

  [1] NO-REGRESSION (회귀금지).  Every inherited artifact is byte-identical to the frozen
      hash recorded at seed time (inherited/FROZEN_SHA256.json).
  [2] THEORY REPRODUCES.  Each foundation module runs clean (internal asserts hold) and is
      DETERMINISTIC — run twice, identical sha256. (Eye: light emergence + colour-by-angle.
      Ear: the √(B/ρ) sound wave + Greenwood-shape tonotopy. Both: the full DNA reading.)
  [3] DNA READING RECOMPUTES OFFLINE — γ (LEVEL) **and** A4 (SHAPE).  For every master gene the
      reading is recomputed from the cached promoter bytes with the inherited canonical grammar
      and must equal the atlas bit-for-bit: γ, shell_class, stiff_frac, shape_amplitude. The A4
      orthogonality |mean(shape)|≈0 (A4 = signal − γ) is asserted per gene. corr(γ,GC) and the
      count of genes whose A4 SHAPE is non-trivial (where reading γ ALONE would be lossy) are
      reported. No network.
  [4] NO-OMISSION (누락금지).  Every artifact the seed promises (seed.json "completeness") is present.

  [5] E-NUMBERING CONSISTENT (정합).  The folder-label ⟷ BLUEPRINT-canonical map (e_numbering.json)
      agrees with the filesystem and seed.json: every research/E*/ folder is mapped (both directions),
      every mapped run.py is a registered foundation module, the blueprint_E assignment is injective,
      and the two documented slip pairs (folder E1⟷blueprint E2, folder E6⟷blueprint E1) match exactly —
      so the reconciliation (open item #4) cannot silently drift. See E_NUMBERING.md.

Exit 0 + 'SEED VERIFY: PASS' only if all pass. Requires numpy (same as the foundation modules); no network.
"""
import os, sys, json, hashlib, subprocess, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG  = json.load(open(os.path.join(ROOT, "seed.json"), encoding="utf-8"))
sys.path.insert(0, os.path.join(ROOT, "inherited"))   # import the inherited canonical grammar + reading


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run_module_twice(rel):
    p = os.path.join(ROOT, rel)
    outs = []
    for _ in range(2):
        r = subprocess.run([sys.executable, p], capture_output=True, text=True, cwd=ROOT)
        if r.returncode != 0:
            return False, None, r.stderr.strip()[-400:]
        line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
        outs.append(line[-1].split("sha256:")[1].strip() if line else r.stdout)
    return (outs[0] == outs[1]), outs[0], None


def main():
    print("=" * 78)
    print(f"SEED VERIFY — {CFG['package']}  v{CFG.get('version','?')}")
    print("=" * 78)
    ok_all = True

    # [1] NO-REGRESSION ----------------------------------------------------------------
    print("\n[1] no-regression (회귀금지) — inherited artifacts byte-identical to frozen seed:")
    frozen = json.load(open(os.path.join(ROOT, CFG["frozen_sha"]), encoding="utf-8"))["files"]
    for rel, want in sorted(frozen.items()):
        p = os.path.join(ROOT, rel)
        got = sha(p) if os.path.exists(p) else "MISSING"
        ok = (got == want); ok_all &= ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {rel:46s} {got[:16]}")

    # [2] THEORY REPRODUCES ------------------------------------------------------------
    print("\n[2] theory reproduces — foundation modules deterministic + asserts hold:")
    for rel in CFG["foundation_modules"]:
        det, h, err = run_module_twice(rel)
        ok = det and err is None; ok_all &= ok
        tag = (h[:16] if h else "") if ok else (err or "non-deterministic")
        print(f"    [{'PASS' if ok else 'FAIL'}] {rel:46s} {tag}")

    # [3] DNA READING RECOMPUTES OFFLINE — γ (LEVEL) and A4 (SHAPE) ---------------------
    print("\n[3] DNA reading recomputes offline — γ (LEVEL) + A4 (SHAPE), cache bit-for-bit:")
    import vp_dna_reading as R
    cache = json.load(open(os.path.join(ROOT, CFG["gamma_cache"]), encoding="utf-8"))["genes"]
    atlas = json.load(open(os.path.join(ROOT, "inherited/organ_gamma.json"), encoding="utf-8"))["genes"]
    gam, gc = [], []
    nmismatch = 0; n_ortho_fail = 0; n_textured = 0
    for sym, rec in sorted(cache.items()):
        rr = R.read_promoter(rec["seq"])
        a = atlas.get(sym, {})
        fields_ok = all(rr[k] == a.get(k) for k in ("gamma", "shape_amplitude", "shape_range", "stiff_side_frac"))
        seq_ok = (hashlib.sha256(rec["seq"].encode()).hexdigest() == rec["seq_sha256"])
        if not (fields_ok and seq_ok): nmismatch += 1
        if rr["shape_mean_abs"] >= 1e-9: n_ortho_fail += 1     # A4 = signal − γ must hold
        if rr["shape_amplitude"] > 0.0:  n_textured += 1       # γ-alone would be lossy here
        gam.append(rr["gamma"]); gc.append(rr["gc"])
    n = len(gam); mg, mc = sum(gam)/n, sum(gc)/n
    cov = sum((gam[i]-mg)*(gc[i]-mc) for i in range(n))
    sg = math.sqrt(sum((x-mg)**2 for x in gam)); sc = math.sqrt(sum((x-mc)**2 for x in gc))
    corr = cov/(sg*sc) if sg and sc else 0.0
    ok = (nmismatch == 0 and n_ortho_fail == 0); ok_all &= ok
    print(f"    [{'PASS' if nmismatch==0 else 'FAIL'}] {n} genes: γ+A4 recompute identical to atlas "
          f"(mismatches={nmismatch}); corr(γ,GC)={corr:.3f}")
    print(f"    [{'PASS' if n_ortho_fail==0 else 'FAIL'}] A4 orthogonality |mean(shape)|≈0 (A4 = signal − γ) "
          f"for all genes (failures={n_ortho_fail})")
    print(f"    [info] {n_textured}/{n} genes carry non-trivial A4 SHAPE — where reading γ ALONE is lossy")

    # [4] NO-OMISSION ------------------------------------------------------------------
    print("\n[4] no-omission (누락금지) — every promised artifact present:")
    miss = [f for f in CFG["completeness"] if not os.path.exists(os.path.join(ROOT, f))]
    ok = (not miss); ok_all &= ok
    if miss:
        for f in miss: print(f"    [FAIL] MISSING: {f}")
    else:
        print(f"    [PASS] all {len(CFG['completeness'])} promised artifacts present")

    # [5] E-NUMBERING CONSISTENT (정합) — folder labels ⟷ BLUEPRINT-canonical, machine-checked --------
    print("\n[5] E-numbering consistent — folder labels ⟷ BLUEPRINT-canonical (e_numbering.json):")
    emap = json.load(open(os.path.join(ROOT, "e_numbering.json"), encoding="utf-8"))
    folders = emap["folders"]
    disk = sorted(d for d in os.listdir(os.path.join(ROOT, "research"))
                  if os.path.isdir(os.path.join(ROOT, "research", d)) and d.startswith("E"))
    mapped = sorted(f["folder"] for f in folders)
    fmods = set(CFG["foundation_modules"])
    # (a) folder set equality, both directions (no-omission + no-phantom of research folders)
    set_ok = (set(disk) == set(mapped)); ok_all &= set_ok
    print(f"    [{'PASS' if set_ok else 'FAIL'}] {len(mapped)} folders mapped == {len(disk)} on disk"
          + ("" if set_ok else f"  (disk-only={sorted(set(disk)-set(mapped))}, "
                               f"map-only={sorted(set(mapped)-set(disk))})"))
    # (b) every mapped run.py exists AND is a registered foundation module
    run_ok = True
    for f in folders:
        if not os.path.exists(os.path.join(ROOT, f["run"])) or f["run"] not in fmods:
            run_ok = False; print(f"    [FAIL] {f['folder']}: run missing-or-unregistered ({f['run']})")
    ok_all &= run_ok
    if run_ok:
        print(f"    [PASS] every mapped run.py exists and is a registered foundation module ({len(folders)})")
    # (c) blueprint_E assignment is an injection (each canonical increment maps to ≤1 folder)
    bps = [f["blueprint_E"] for f in folders]
    inj_ok = (len(bps) == len(set(bps))); ok_all &= inj_ok
    print(f"    [{'PASS' if inj_ok else 'FAIL'}] blueprint_E assignment is injective"
          + ("" if inj_ok else f"  (dupes={sorted(b for b in set(bps) if bps.count(b) > 1)})"))
    # (d) the two documented slip pairs match the folders table exactly (no silent fix / drift)
    by_folder = {f["folder"]: f for f in folders}; slip_ok = True
    for pair in emap["documented_slip"]["pairs"]:
        f = by_folder.get(pair["folder"], {})
        if f.get("folder_E") != pair["folder_E"] or f.get("blueprint_E") != pair["blueprint_E"]:
            slip_ok = False; print(f"    [FAIL] slip-pair drift: {pair}")
    ok_all &= slip_ok
    if slip_ok:
        print(f"    [PASS] {len(emap['documented_slip']['pairs'])} documented slip pair(s) match "
              f"(folder E1⟷blueprint E2, folder E6⟷blueprint E1)")
    # (e) every non-null canonical carrier_folder round-trips to a real mapped folder
    carriers = [c["carrier_folder"] for c in emap["blueprint_canonical"] if c["carrier_folder"]]
    car_ok = all(c in set(mapped) for c in carriers); ok_all &= car_ok
    print(f"    [{'PASS' if car_ok else 'FAIL'}] {len(carriers)} canonical carrier_folder(s) "
          f"round-trip to a real folder")

    print("\n" + "=" * 78)
    print(f"SEED VERIFY: {'PASS' if ok_all else 'FAIL'}")
    print("=" * 78)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
