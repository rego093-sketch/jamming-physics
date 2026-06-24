#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M49  SH-26 CROSS-SYSTEM RATIO -- PROTOCOL HARNESS + POPULATION TEMPLATE
======================================================================
M46 built the WITHIN-system magnitude-ratio test (South Atlantic) and found it INCONCLUSIVE,
then named the DECISIVE form -- the SAME ratio across INDEPENDENT salt-giant systems -- and
refused to fabricate the cross-system numbers, leaving it [O]/unbuilt:

  "fabricating those numbers would violate the framework (no unverified data, no fitting),
   so it is left [O]/unbuilt rather than guessed."  -- M46

This module does the honest next step WITHOUT breaking that rule:
  (1) it BUILDS the decisive cross-system protocol as a runnable harness;
  (2) it pins the canonical salt-giant POPULATION (so there is no cherry-picking) with
      EXPLICIT data-quality flags;
  (3) it RUNS on the only column responsibly fillable now -- present-tense salt VOLUME at
      literature order-of-magnitude (LIT_OOM) -- and SKIPS the to-be-verified (TBV) inputs;
  (4) it grades the result honestly.

THE PROTOCOL (what WOULD decide SH-26):
  one conserved relaxation (one parameter) -> the cross-control ratio source_volume/extension
  (and salt/source) is a UNIVERSAL CONSTANT across independent systems -> LOW CV (tight).
  independent-magnitude mainstream -> those ratios SCATTER across systems -> HIGH CV.
  Decision rule (pre-registered): CV < 0.15 tight (one-parameter) ; CV > 0.35 scattered
  (mainstream) ; between = intermediate/inconclusive.

WHAT THE RUN CAN SHOW NOW:
  - salt VOLUME alone scatters across ~an order of magnitude between systems -> by itself it
    is NOT a universal constant. (This is expected and is NOT the discriminator: salt volume
    tracks basin size/accommodation in BOTH frameworks.)
  - the DISCRIMINATING cross-control ratio needs matched source_volume + extension, which are
    TBV -> the harness reports the verdict as [O]/INCONCLUSIVE pending verified inputs, and
    prints EXACTLY which fields each system still needs.

FIREWALL: present-tense magnitudes only; no age/rate/occurrence load-bearing ([O]/RECORD,
both directions). SEED = 19. No fitted parameter. Double-SHA-256 self-gate.

HONEST SCOPE: the salt volumes are LIT_OOM (citable, not verified primary); they are used
ONLY to demonstrate the harness and the salt-volume scatter, NOT as a load-bearing ratio.
The decisive ratio stays [O]/unbuilt until the TBV inputs are verified -- exactly M46's rule.
"""
import csv, hashlib, math, statistics
from pathlib import Path

SEED = 19
HERE = Path(__file__).resolve().parent
CSV = HERE / "data" / "saltgiant_population.csv"
CSV_SHA256 = "f0b1d93669d03caa7e77686b777eece1fc12cd4a5d9ca98507b479da5a27b79c"  # frozen, pinned

# pre-registered decision rule (declared before reading data; not fitted)
CV_TIGHT, CV_SCATTER = 0.15, 0.35

EXPECT = "6783b794b91a59faa4bfb2b469d5745eeae7d5623236e4ab6add9c4e057606a4"  # pinned


def load():
    raw = CSV.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CSV_SHA256, "frozen CSV changed"
    lines = [ln for ln in raw.decode().splitlines() if not ln.lstrip().startswith("#")]
    return list(csv.DictReader(lines))


def cv(xs):
    m = statistics.mean(xs); s = statistics.pstdev(xs)
    return m, s, (s / m if m else float("nan"))


def main():
    rows = load()
    L = []
    L.append("M49  SH-26 CROSS-SYSTEM RATIO -- PROTOCOL HARNESS + POPULATION TEMPLATE")
    L.append(f"SEED={SEED}   input=data/saltgiant_population.csv   RAW_FILE_SHA256={CSV_SHA256}")
    L.append(f"PRE-REGISTERED: CV<{CV_TIGHT} tight(one-parameter) ; CV>{CV_SCATTER} scattered(mainstream) ; between=inconclusive")
    L.append("")
    L.append("[CANONICAL POPULATION  (fixed in advance -> no cherry-picking)]")
    L.append(f"  {'system':22}{'salt_km3':>12}{'quality':>9}{'source_vol':>12}{'extension':>11}")
    salts, missing = [], {}
    for r in rows:
        sysn = r["system"]
        sv = r["salt_volume_km3"].strip()
        sq = r["salt_quality"].strip()
        srcv = r["source_volume_km3"].strip() or "TBV"
        ext = r["extension_strain"].strip() or "TBV"
        L.append(f"  {sysn:22}{(sv or 'TBV'):>12}{sq:>9}{srcv:>12}{ext:>11}")
        if sv and sq == "LIT_OOM":
            salts.append(float(sv))
        need = []
        if not r["source_volume_km3"].strip():
            need.append("source_volume_km3")
        if not r["extension_strain"].strip():
            need.append("extension_strain")
        if need:
            missing[sysn] = need
    L.append("")

    # --- what is computable now: salt-volume scatter (NOT the discriminator) ---
    L.append("[COMPUTABLE NOW: salt VOLUME scatter across systems  (NOT the discriminator)]")
    m, s, c = cv(salts)
    lo, hi = min(salts), max(salts)
    L.append(f"  n={len(salts)}  mean={m:,.0f} km3  CV={c:.3f}  span={hi/lo:.1f}x  (~{math.log10(hi/lo):.1f} orders)")
    L.append(f"  -> salt volume is NOT a universal constant (CV={c:.3f}); it tracks basin")
    L.append("     size/accommodation in BOTH frameworks -> NOT discriminating, as designed.")
    L.append("")

    # --- the discriminating ratio: blocked on verified inputs ---
    L.append("[DISCRIMINATING cross-control ratio: source_volume/extension & salt/source]")
    L.append("  REQUIRES matched, verified source_volume + extension per system. Status:")
    for sysn, need in missing.items():
        L.append(f"    {sysn:22} NEEDS: {', '.join(need)}")
    L.append("  -> not computable at verified quality -> NOT run (no fabrication).")
    L.append("")

    L.append("[VERDICT]")
    L.append("  cross-system SH-26 protocol is BUILT and the canonical population is fixed.")
    L.append("  Run status: INCONCLUSIVE / [O] -- the discriminating ratio is blocked on the")
    L.append("  TBV inputs above; salt volume alone scatters (degenerate). The decisive test")
    L.append("  stays [O]/unbuilt until verified source volumes + extensions are supplied,")
    L.append("  exactly as M46 required. This module converts SH-26 from 'unnamed-unbuilt' to")
    L.append("  'protocol-built + population-fixed + exact verified-data gap pinned'.")
    L.append("")
    L.append("[GRADE]")
    L.append("  SH-26 cross-system: protocol [L] (built, pre-registered, no-tuning); decisive")
    L.append("  RUN stays [O]/unbuilt pending verified inputs. No present-tense discriminator")
    L.append("  is produced -> consistent with M37/M39/M46 and Module 47. Occurrence/ages")
    L.append("  [O]/RECORD, both directions. Falsification = discovery.")

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
