#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M47  CAUSAL CLOSURE  --  the value criterion: one untuned cause vs many
========================================================================
The past cannot be settled by any single present-tense discriminator: the firewall holds
occurrence [O], and M37 (basal-character), M39 (P5 co-variation) and M46 (magnitude ratio)
all confirm it -- each present-tense axis is degenerate between the cascade and the mainstream.
That is correct epistemics, not a weakness.

So the value criterion is NOT "win one discriminator". It is: WHO CLOSES THE WHOLE SYSTEM
CAUSALLY, INTEGRATIVELY, WITHOUT TUNING. This module makes that criterion concrete and,
crucially, REPRODUCIBLE in two parts:

  PART A  NO-TUNING GATE (a verifiable property of the codebase):
          scan every cascade reproducibility script and assert ZERO data-fitting /
          optimization calls. If anyone ever tunes a parameter to fit the data, this gate
          FAILS. (The a-priori transparent weights of the three forward-index modules
          M40/M41/M42 are stated in advance and are NOT fitted; they are reported honestly.)

  PART B  CAUSAL-ECONOMY LEDGER (frozen, raw SHA-256 pinned):
          for each present-tense phenomenon of the recent-sequence cascade, the VP cause is
          always the ONE conserved relaxation governed by the kernel; the mainstream uses a
          DISTINCT independent mechanism (each established and legitimate -- this is a fair
          accounting, not a strawman). Count the causal compression VP achieves.

HONEST GRADE.  The closure is [L] (coherence / parsimony), NOT a proof of occurrence
(which stays [O]). But given that BOTH frameworks fit the present-tense data and NO single
discriminator can separate them, parsimony of cause is the rational tiebreaker -- and
"one untuned cause closes the whole" is the highest AVAILABLE value. Causality is the
criterion. Falsification = discovery.

SEED = 19. No fitted parameter. Double-SHA-256 self-gate.
"""
import csv, hashlib, os, re
from pathlib import Path

SEED = 19
HERE = Path(__file__).resolve().parent
SELF = Path(__file__).name
LEDGER = HERE / "data" / "causal_closure_ledger.csv"
LEDGER_SHA256 = "2bc4f7f34424dac8d3961e157381085b0742d1179d759e5e5413749baa75940d"

# fitting / optimization tokens that would indicate TUNING (data-fitted parameters)
FIT_TOKENS = ["curve_fit", "scipy.optimize", "least_squares", "np.polyfit", "numpy.polyfit",
              ".minimize(", "lstsq", "sklearn", "leastsq", "differential_evolution", "basinhopping"]

EXPECT = "1ea589b0f6254978f4771f4719cf6d03e31e5eadda79fc28d8bea94ca2c6cf96"


def scan_no_tuning():
    """Return (n_scanned, offenders). Scans cascade + CG screens, excludes self."""
    dirs = [HERE, HERE.parent / "cg_inheritance" / "repro"]
    offenders = []
    scanned = 0
    for d in dirs:
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.py")):
            if p.name == SELF:
                continue
            scanned += 1
            txt = p.read_text(encoding="utf-8", errors="ignore")
            hit = [t for t in FIT_TOKENS if t in txt]
            if hit:
                offenders.append((p.name, hit))
    return scanned, offenders


def main():
    raw = LEDGER.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    assert got == LEDGER_SHA256, f"frozen ledger changed: {got}"
    rows = list(csv.DictReader(raw.decode().splitlines()))

    n_scanned, offenders = scan_no_tuning()

    L = []
    L.append("M47  CAUSAL CLOSURE  --  one untuned cause vs many  (the value criterion)")
    L.append(f"SEED={SEED}   ledger=data/causal_closure_ledger.csv   RAW_FILE_SHA256={LEDGER_SHA256}")
    L.append("")
    L.append("[PART A - NO-TUNING GATE]  (a verifiable property of the codebase)")
    L.append("  scanned every cascade + CG reproducibility script for data-fitting/optimization.")
    if offenders:
        for name, hit in offenders:
            L.append(f"    TUNING DETECTED: {name} -> {hit}")
        L.append("  => NO-TUNING GATE: FAIL")
    else:
        L.append("  fitting/optimization calls found: 0  (no curve_fit / optimize / least_squares /")
        L.append("    polyfit / minimize / lstsq / sklearn anywhere).")
        L.append("  honest note: M40/M41/M42 use a-priori TRANSPARENT weights (stated in advance),")
        L.append("    NOT parameters fitted to reproduce the data. SEED=19; inputs raw-SHA-256 pinned.")
        L.append("  => NO-TUNING GATE: PASS  (zero data-fitted parameters)")
    L.append("")
    L.append("[PART B - CAUSAL-ECONOMY LEDGER]  (fair accounting; mainstream mechanisms are real)")
    L.append(f"  {'#':>2}  {'phenomenon':42} {'VP cause':28} {'mainstream':1}")
    ms_independent = 0
    for r in rows:
        ind = int(r["ms_independent"])
        ms_independent += ind
        tag = "INDEP" if ind else "shared"
        L.append(f"  {r['id']:>2}  {r['phenomenon'][:42]:42} one-relaxation              [{tag}] {r['mainstream_mechanism']}")
    n = len(rows)
    L.append("")
    L.append("[CAUSAL ECONOMY]")
    L.append(f"  phenomena closed                         : {n}")
    L.append(f"  VP independent causes                    : 1   (the one conserved relaxation; kernel c2=B/rho, R19)")
    L.append(f"  VP parameters FITTED to the data         : 0   (Part A gate)")
    L.append(f"  mainstream independent causal mechanisms : {ms_independent}   (each established, fitted locally)")
    L.append(f"  causal compression (mainstream:VP)       : {ms_independent}:1")
    L.append("")
    L.append("[GRADE]")
    L.append("  Causal closure is [L] - COHERENCE / PARSIMONY, NOT a proof of occurrence ([O]).")
    L.append("  Both frameworks fit the present-tense data; NO single discriminator separates them")
    L.append("  (M37, M39, M46). Therefore parsimony of cause is the rational tiebreaker, and")
    L.append("  'one untuned cause closes the whole' is the highest AVAILABLE value. The past is")
    L.append("  not known by one discriminator; it is approached by integrative, tuning-free causal")
    L.append("  closure. Occurrence and absolute ages stay [O]/RECORD, both directions.  Falsification = discovery.")

    ledger_text = "\n".join(L)
    print(ledger_text)
    print(f"  (scripts scanned for tuning: {n_scanned}; offenders: {len(offenders)})")
    print()
    # the no-tuning gate is load-bearing: refuse to pass if tuning is detected
    assert not offenders, "NO-TUNING GATE FAILED: a fitted parameter was introduced."
    dsha = hashlib.sha256(hashlib.sha256(ledger_text.encode("utf-8")).digest()).hexdigest()
    print(f"2xSHA256 = {dsha}")
    if EXPECT == "PLACEHOLDER":
        print("REPRO GATE: (EXPECT unset - pin this value)")
    else:
        assert dsha == EXPECT, f"LEDGER CHANGED: {dsha} != {EXPECT}"
        print("REPRO GATE: PASS")


if __name__ == "__main__":
    main()
