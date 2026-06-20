#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_shared_ssot.py — the cross-package drift guard for the shared SSOT set.

The neuro and mind papers are two files, two lanes, never merged
(PROJECT_BOUNDARY_neuro_mind.md). The ONLY files that must be identical in both are
the small shared single-source-of-truth set:

    EM_NEAR_FAR_THESIS.md          (the EM regime + the two registers)
    TERMINOLOGY_canonical.md       (the controlled vocabulary + §7 ownership map)
    PROJECT_BOUNDARY_neuro_mind.md (this boundary)

This helper is shipped byte-identical at the root of BOTH packages. It does two jobs:

  self-check (no args)        every shared file is present locally and carries its
                             load-bearing markers; prints each file's sha256.
  --with  <sibling_root>      assert the three shared files are byte-identical between
                             this package and the sibling. Exit 1 on any drift.
  --push  <sibling_root>      copy THIS package's three shared files into the sibling
                             (overwrite), then re-assert byte-identity.

Deterministic: pure file hashing + substring presence; 2x run identical.
Run:
  python3 sync_shared_ssot.py
  python3 sync_shared_ssot.py --with ../mind            # from the neuro package
  python3 sync_shared_ssot.py --with ../neuro           # from the mind package
  python3 sync_shared_ssot.py --push ../mind            # neuro -> mind (one-way mirror)
"""
import os, sys, hashlib, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# the shared set, with the markers each must carry (so a stale/partial copy is caught)
SHARED = {
    "EM_NEAR_FAR_THESIS.md": [
        "1.1",                                # the A/B disambiguation
        "1.2",                                # the two registers
        "EM = the brainwave = the low-frequency",
        "cable conduction (the spike)",
        "ephaptic near-field",
    ],
    "TERMINOLOGY_canonical.md": [
        "cable conduction",
        "ephaptic near-field",
        "THE THREE SPEEDS",
        "BANNED",
        "REGISTER & OWNERSHIP",                # §7
        "EM = the brainwave = the low-frequency",
    ],
    "PROJECT_BOUNDARY_neuro_mind.md": [
        "Shared artifacts",                    # §6
        "sync_shared_ssot.py",
        "one-way",
    ],
}

checks = []
def rec(ok, msg):
    checks.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {msg}")

def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def self_check():
    print("self-check — shared SSOT present locally with load-bearing markers")
    for fn, needles in SHARED.items():
        p = os.path.join(ROOT, fn)
        if not os.path.isfile(p):
            rec(False, f"{fn}: MISSING at package root")
            continue
        txt = open(p, encoding="utf-8").read()
        missing = [n for n in needles if n not in txt]
        rec(not missing,
            f"{fn}: sha256 {sha256(p)[:16]}…  "
            + ("all markers present" if not missing else f"MISSING markers {missing}"))

def compare(sibling):
    print(f"byte-identity — this package  vs  {sibling}")
    sib = os.path.abspath(sibling)
    for fn in SHARED:
        a, b = os.path.join(ROOT, fn), os.path.join(sib, fn)
        if not os.path.isfile(a):
            rec(False, f"{fn}: missing here"); continue
        if not os.path.isfile(b):
            rec(False, f"{fn}: missing in sibling ({sib})"); continue
        ha, hb = sha256(a), sha256(b)
        rec(ha == hb, f"{fn}: {'identical' if ha == hb else f'DRIFT  here={ha[:12]}…  sibling={hb[:12]}…'}")

def push(sibling):
    sib = os.path.abspath(sibling)
    print(f"push — copying this package's shared SSOT into {sib}")
    for fn in SHARED:
        a, b = os.path.join(ROOT, fn), os.path.join(sib, fn)
        if not os.path.isfile(a):
            rec(False, f"{fn}: missing here, cannot push"); continue
        shutil.copy2(a, b)
        print(f"    copied {fn}")
    compare(sibling)

def main(argv):
    print("=" * 78)
    print("shared SSOT — sync / drift guard")
    print("=" * 78)
    self_check()
    if len(argv) >= 2 and argv[0] in ("--with", "--push"):
        print("-" * 78)
        (push if argv[0] == "--push" else compare)(argv[1])
    elif argv:
        print(f"\nunrecognised args: {argv}\n(use no args, or --with <root>, or --push <root>)")
        return 2
    print("-" * 78)
    ok = all(checks)
    print("SHARED SSOT: " + ("PASS — shared set present and consistent."
                             if ok else "FAIL — a shared file is missing, stale, or drifted."))
    print("-" * 78)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
