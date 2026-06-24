#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M46  MAGNITUDE-RATIO DISCRIMINATOR  (SH-26)  -- the one genuinely-discriminating test
=====================================================================================
m39 ended by naming the only test that could separate the cascade from the mainstream
past the rate firewall:

  "A genuinely DISCRIMINATING version would need a magnitude RATIO the one-parameter
   budget predicts and independent-magnitude mainstream does NOT (the open C-2 candidate,
   SH-26) - still UNBUILT."

This module BUILDS it, and runs it on the only internally-consistent frozen present-tense
dataset we have (the South Atlantic conjugate-margin segments, M39's data).

THE LOGIC (why this is NOT the degenerate M39 co-variation):
  - One conserved relaxation (one parameter) would set the WHOLE suite, so ALL pairwise
    magnitude ratios should be UNIVERSAL CONSTANTS -> LOW scatter (low CV).
  - The mainstream treats the magnitudes as INDEPENDENT: salt is set by accommodation +
    restriction + arid climate; the source rock by productivity + anoxia. Different
    controls -> the CROSS-CONTROL ratios should SCATTER.
  - salt/extension is MECHANICAL (more stretch -> more accommodation -> more salt) in BOTH
    frameworks, so it is DEGENERATE (M39 already showed r=+0.99). It is reported but is
    NOT the discriminator.
  - The DISCRIMINATOR is the CROSS-CONTROL ratios: source/extension and salt/source.
      one-parameter  -> tight (low CV)
      mainstream     -> scattered (high CV)

FIREWALL: present-tense geometry / richness only (extension, salt thickness, source TOC).
No ages, rates, or occurrence are load-bearing; they stay [O]/RECORD both directions.
SEED = 19. No fitted parameter. Pre-registered thresholds (declared before the data is read).
Double-SHA-256 self-gate.

HONEST SCOPE (stated up front, not after the result):
  (1) The six SA segments are ONE rift system, not independent realisations of different
      coupled events; a within-system tight ratio is weaker evidence than an across-system one.
  (2) Source magnitude is proxied by TOC (richness), NOT by volume (thickness x area);
      the frozen set has no source thickness. A decisive run needs source VOLUME.
  (3) n = 6. The decisive across-system protocol is specified below and is UNRUN: it needs
      VERIFIED magnitudes across INDEPENDENT salt-giant systems. Fabricating those numbers
      would violate the framework (no unverified data, no fitting), so it is left [O]/unbuilt.
"""
import csv, hashlib, os, statistics
from pathlib import Path

SEED = 19
HERE = Path(__file__).resolve().parent
CSV = HERE / "data" / "sa_margin_segments.csv"
CSV_SHA256 = "c36ae5f4b9eb9495f44559db97485a11d2292e748c581c5c4dd146a6565a284e"  # frozen, pinned

# ---- PRE-REGISTERED thresholds (declared BEFORE reading the data; not fitted) ----
CV_TIGHT = 0.15      # CV below this = "tight"  (one-parameter universal-constant consistent)
CV_SCATTER = 0.35    # CV above this = "scattered" (independent-magnitude / mainstream)
# 0.15 <= CV <= 0.35  = "intermediate" (does not cleanly discriminate)

EXPECT = "0436b048754b62895024e905aea08aed36339991d6f07e11796d9399083a675d"


def midpoint(rng):
    a, b = rng.split("_")
    return (float(a) + float(b)) / 2.0


def cv(xs):
    m = statistics.mean(xs)
    s = statistics.pstdev(xs)
    return m, s, (s / m if m else float("nan"))


def classify(c):
    if c < CV_TIGHT:
        return "tight (one-parameter consistent)"
    if c > CV_SCATTER:
        return "scattered (independent-magnitude / mainstream)"
    return "intermediate (does NOT cleanly discriminate)"


def main():
    # integrity of the frozen input
    raw = CSV.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    assert got == CSV_SHA256, f"frozen CSV changed: {got}"

    rows = list(csv.DictReader(raw.decode().splitlines()))
    seg = []
    for r in rows:
        beta = float(r["beta_extension"])
        salt = float(r["salt_thickness_km"])
        toc = midpoint(r["source_toc_pct"])
        ext = beta - 1.0  # extension strain
        seg.append((r["segment"], ext, salt, toc))

    L = []
    L.append("M46  MAGNITUDE-RATIO DISCRIMINATOR  (SH-26)")
    L.append(f"SEED={SEED}   input=data/sa_margin_segments.csv   RAW_FILE_SHA256={CSV_SHA256}")
    L.append(f"PRE-REGISTERED: CV<{CV_TIGHT} tight ; CV>{CV_SCATTER} scattered ; between=intermediate")
    L.append("")
    L.append("[PRESENT-TENSE MAGNITUDES per conjugate-margin segment]")
    L.append(f"  {'segment':16}{'ext=beta-1':>11}{'salt_km':>9}{'TOC%':>7}"
             f"{'salt/ext':>10}{'src/ext':>10}{'salt/src':>10}")
    se, sre, ssr = [], [], []
    for name, ext, salt, toc in seg:
        a, b, c = salt / ext, toc / ext, salt / toc
        se.append(a); sre.append(b); ssr.append(c)
        L.append(f"  {name:16}{ext:>11.2f}{salt:>9.2f}{toc:>7.1f}{a:>10.3f}{b:>10.3f}{c:>10.3f}")
    L.append("")

    results = {}
    L.append("[RATIO SCATTER  (coefficient of variation across segments)]")
    for label, xs, key in [("salt/extension   (MECHANICAL - degenerate, both frameworks)", se, "salt_ext"),
                           ("source(TOC)/extension   (CROSS-CONTROL - discriminating)", sre, "src_ext"),
                           ("salt/source(TOC)        (CROSS-CONTROL - discriminating)", ssr, "salt_src")]:
        m, s, c = cv(xs)
        results[key] = c
        L.append(f"  {label}")
        L.append(f"      mean={m:.3f}  sd={s:.3f}  CV={c:.3f}  ->  {classify(c)}")
    L.append("")

    # ---- the discriminator verdict: based on the two CROSS-CONTROL ratios only ----
    cross = [results["src_ext"], results["salt_src"]]
    cross_class = [classify(c) for c in cross]
    all_tight = all(c < CV_TIGHT for c in cross)
    all_scatter = all(c > CV_SCATTER for c in cross)
    L.append("[DISCRIMINATOR VERDICT  (cross-control ratios source/ext & salt/source only)]")
    L.append(f"  salt/ext is degenerate (CV={results['salt_ext']:.3f}, mechanical) -> set aside, as designed.")
    if all_tight:
        verdict = "ONE-PARAMETER FAVOURED (both cross-control ratios tight)"
    elif all_scatter:
        verdict = "MAINSTREAM / INDEPENDENT-MAGNITUDE FAVOURED (both cross-control ratios scattered)"
    else:
        verdict = "INCONCLUSIVE - cross-control ratios are INTERMEDIATE; does NOT cleanly discriminate"
    L.append(f"  source/ext: CV={results['src_ext']:.3f} -> {cross_class[0]}")
    L.append(f"  salt/source: CV={results['salt_src']:.3f} -> {cross_class[1]}")
    L.append(f"  => {verdict}")
    L.append("")
    L.append("[HONEST CAVEATS - load-bearing on the grade]")
    L.append("  (1) all six segments are ONE rift system, not independent coupled events;")
    L.append("      a within-system ratio cannot be a UNIVERSAL constant test.")
    L.append("  (2) source magnitude proxied by TOC (richness), not VOLUME (thickness x area).")
    L.append("  (3) n=6. The decisive test is the SAME ratio across INDEPENDENT salt-giant")
    L.append("      systems (S.Atlantic, Gulf of Mexico, Red Sea, Zechstein, Messinian,")
    L.append("      Pricaspian) with VERIFIED source VOLUMES - UNRUN; fabricating those")
    L.append("      numbers would violate the framework, so it stays [O]/unbuilt.")
    L.append("")
    L.append("[GRADE]")
    L.append("  SH-26 discriminator BUILT and specified. Within-system run: salt/ext tight")
    L.append("  (degenerate); cross-control ratios INTERMEDIATE -> does NOT cleanly")
    L.append("  discriminate. Net [L]/inconclusive present-tense; joins M37 (basal-character)")
    L.append("  and M39 (P5 co-variation) as a THIRD present-tense axis that is degenerate")
    L.append("  between the frameworks. The cross-system decisive test stays [O]/UNRUN.")
    L.append("  Occurrence and absolute ages stay [O]/RECORD, both directions.  Falsification = discovery.")

    ledger = "\n".join(L)
    print(ledger)
    print()
    dsha = hashlib.sha256(hashlib.sha256(ledger.encode("utf-8")).digest()).hexdigest()
    print(f"2xSHA256 = {dsha}")
    if EXPECT == "PLACEHOLDER":
        print("REPRO GATE: (EXPECT unset - pin this value)")
    else:
        assert dsha == EXPECT, f"LEDGER CHANGED: {dsha} != {EXPECT}"
        print("REPRO GATE: PASS")


if __name__ == "__main__":
    main()
