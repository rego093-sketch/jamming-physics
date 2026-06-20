#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_terminology.py — the lock for TERMINOLOGY_canonical.md

Pins the controlled vocabulary so the recurring drift cannot return:
  (1) TERMINOLOGY_canonical.md present at package root, with its core sections.
  (2) EM_NEAR_FAR_THESIS.md carries the §1.1 disambiguation (χ→0 = two objects A/B).
  (3) The banned phrasings (the ones that conflated the two objects / three speeds)
      are ABSENT from every published chapter body.

Deterministic: no RNG, pure file/string invariants; 2× run identical.
Kept OUT of run_all.py so verify_all stays unchanged; run standalone or alongside
verify_boundary.py. Run: `python3 verify_terminology.py` -> PASS/FAIL, exit 0/1.
"""
import os, glob, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail):
    checks.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

print("=" * 78)
print("TERMINOLOGY_canonical — gate")
print("=" * 78)

# (1) canonical vocabulary present, with its load-bearing sections -------------------
print("\n(1) canonical vocabulary present")
canon = os.path.join(ROOT, "TERMINOLOGY_canonical.md")
canon_txt = open(canon, encoding="utf-8").read() if os.path.isfile(canon) else ""
check("TERMINOLOGY_canonical.md at package root", bool(canon_txt),
      f"{len(canon_txt)} bytes" if canon_txt else "MISSING")
for needle, label in [
    ("cable conduction", "object (A) cable conduction = the spike"),
    ("ephaptic near-field", "object (B) ephaptic near-field = the coupling"),
    ("THE THREE SPEEDS", "the three-speeds rule"),
    ("BANNED", "the banned→use regression table"),
]:
    check(f"canon defines: {label}", needle in canon_txt,
          "present" if needle in canon_txt else f"'{needle}' MISSING")

# (2) the thesis carries the same disambiguation at the source ----------------------
print("\n(2) EM_NEAR_FAR_THESIS.md carries the §1.1 disambiguation")
thesis = open(os.path.join(ROOT, "EM_NEAR_FAR_THESIS.md"), encoding="utf-8").read()
for needle, label in [
    ("1.1", "§1.1 disambiguation section"),
    ("cable conduction (the spike)", "names object (A) the spike-signal"),
    ("ephaptic near-field", "names object (B) the ephaptic coupling"),
]:
    check(f"thesis: {label}", needle in thesis,
          "present" if needle in thesis else f"'{needle}' MISSING")

# (3) banned phrasings absent from every chapter body -------------------------------
print("\n(3) banned phrasings absent from chapters")
# each tuple: (substring that must NOT appear, why it was banned)
BANNED = [
    ("speeds it toward c",                 "conduction never approaches c (≤120 m/s)"),
    ("ionic wave at the conduction speed", "conflates field speed (c) with pattern rate"),
    ("toward light speed",                 "conduction is ~10^6x below light"),
]
chapter_html = sorted(glob.glob(os.path.join(ROOT, "docs", "neuro", "*", "index.html")))
for bad, why in BANNED:
    hits = [os.path.basename(os.path.dirname(p))
            for p in chapter_html if bad in open(p, encoding="utf-8").read()]
    check(f"absent: \"{bad}\"", not hits,
          f"clean ({why})" if not hits else f"FOUND in {hits}")

print("\n" + "-" * 78)
ok = all(checks)
print("TERMINOLOGY LOCK: " + ("PASS — vocabulary pinned; the two χ→0 objects and three speeds "
      "stay distinct." if ok else "FAIL — a term drifted; align to TERMINOLOGY_canonical.md."))
print("-" * 78)
sys.exit(0 if ok else 1)
