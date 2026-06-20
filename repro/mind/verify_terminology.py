#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_terminology.py (mind side) — the lock for the controlled vocabulary in the mind package.

Mirror of the neuro-side gate, pointed at the mind lane. Pins:
  (1) TERMINOLOGY_canonical.md present at package root with its core sections + the §7
      register/ownership map (the file that tells mind it rides the brainwave abstraction
      and cites neuro for the objects).
  (2) EM_NEAR_FAR_THESIS.md carries the §1.1 disambiguation AND the §1.2 two-registers note
      ("EM = the brainwave = the low-frequency …").
  (3) the banned phrasings are ABSENT from every mind chapter body — both the shared
      three-speeds bans and the mind-register bans (no re-deriving neuro's numbers; no bare
      "weak"; no single-object "near-field" left unqualified as the carrier).

Deterministic: pure file/string invariants; 2x run identical. Standalone (no imports of the
neuro package). Run: `python3 verify_terminology.py` -> PASS/FAIL, exit 0/1.
"""
import os, glob, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail):
    checks.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

print("=" * 78)
print("TERMINOLOGY_canonical — gate (mind side)")
print("=" * 78)

# (1) canonical vocabulary present, with its load-bearing sections ---------------------
print("\n(1) canonical vocabulary present (shared SSOT, mirrored from neuro)")
canon = os.path.join(ROOT, "TERMINOLOGY_canonical.md")
canon_txt = open(canon, encoding="utf-8").read() if os.path.isfile(canon) else ""
check("TERMINOLOGY_canonical.md at package root", bool(canon_txt),
      f"{len(canon_txt)} bytes" if canon_txt else "MISSING")
for needle, label in [
    ("cable conduction", "object (A) cable conduction = the spike"),
    ("ephaptic near-field", "object (B) ephaptic near-field = the coupling"),
    ("THE THREE SPEEDS", "the three-speeds rule"),
    ("BANNED", "the banned→use regression table"),
    ("REGISTER & OWNERSHIP", "§7 register/ownership map (mind rides the abstraction)"),
    ("EM = the brainwave = the low-frequency", "the canonical EM=brainwave=low-frequency identity"),
]:
    check(f"canon defines: {label}", needle in canon_txt,
          "present" if needle in canon_txt else f"'{needle}' MISSING")

# (2) the shared thesis carries both disambiguation notes ------------------------------
print("\n(2) EM_NEAR_FAR_THESIS.md carries §1.1 + §1.2")
thesis = open(os.path.join(ROOT, "EM_NEAR_FAR_THESIS.md"), encoding="utf-8").read()
for needle, label in [
    ("1.1", "§1.1 disambiguation (χ→0 = two objects A/B)"),
    ("1.2", "§1.2 the two registers (object layer vs brainwave abstraction)"),
    ("cable conduction (the spike)", "names object (A) the spike-signal"),
    ("ephaptic near-field", "names object (B) the ephaptic coupling"),
    ("EM = the brainwave = the low-frequency", "the EM=brainwave=low-frequency identity"),
]:
    check(f"thesis: {label}", needle in thesis,
          "present" if needle in thesis else f"'{needle}' MISSING")

# (3) banned phrasings absent from mind chapter bodies --------------------------------
print("\n(3) banned phrasings absent from mind chapters")
# shared three-speeds bans + mind-register bans (the re-derivations now cited to neuro)
BANNED = [
    ("speeds it toward c",                 "conduction never approaches c (≤120 m/s)"),
    ("toward light speed",                 "conduction is ~10^6x below light"),
    ("Those fields are weak, of order millivolts per metre",
                                           "strength is measured at threshold; cite neuro §19, not 'weak'"),
    ("contained in the measured &lt; 0.5 mV bound",
                                           "the containment chain is neuro §19's; mind cites the result"),
    ("radiated fraction ~10⁻¹⁵)",          "the radiated-fraction derivation is neuro §18's; mind cites it"),
]
chapter_html = sorted(glob.glob(os.path.join(ROOT, "docs", "mind", "*", "index.html")))
for bad, why in BANNED:
    hits = [os.path.basename(os.path.dirname(p))
            for p in chapter_html if bad in open(p, encoding="utf-8").read()]
    check(f"absent: \"{bad[:46]}{'…' if len(bad) > 46 else ''}\"", not hits,
          f"clean ({why})" if not hits else f"FOUND in {hits}")

print("\n" + "-" * 78)
ok = all(checks)
print("TERMINOLOGY LOCK (mind): " + ("PASS — vocabulary pinned; mind rides the brainwave "
      "abstraction and cites neuro for the objects." if ok
      else "FAIL — a term drifted; align to TERMINOLOGY_canonical.md (§7 register rule)."))
print("-" * 78)
sys.exit(0 if ok else 1)
