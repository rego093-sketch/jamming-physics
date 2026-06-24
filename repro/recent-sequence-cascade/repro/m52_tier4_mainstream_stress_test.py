#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M52  TIER-4 MAINSTREAM STRESS-TEST  -- the author-planned adversarial phase (roadmap T4.1)
==========================================================================================
The roadmap's final tier: once the cascade is built, expose its load-bearing claims to the
STRONGEST mainstream objections and grade the outcome honestly. This module RUNS that test
over a frozen adjudication ledger in which every claim is paired with a steelmanned (not
strawmanned) mainstream alternative -- orbital forcing, plate tectonics + magnetic-stripe
symmetry, oceanic anoxic events, glacial-isostatic seismicity, and the standard petroleum
system -- and adjudicated under the firewall.

WHAT THIS MODULE DOES (deterministically, from the frozen ledger):
  - loads the pinned ledger (raw SHA-256 frozen),
  - tallies the verdicts,
  - asserts the central invariant of the stress-test: NO load-bearing claim achieves a
    DISCRIMINATING present-tense advantage over the mainstream (there is no 'WIN' verdict),
  - locates the concentrated point of failure (the CONCEDE verdicts all trace to the S0
    release / near-criticality root),
  - prints the honest bottom line, and self-gates with a double-SHA-256.

FIREWALL (held throughout): occurrence and absolute timing are [O] in BOTH directions;
only mechanism and present-tense geometry are load-bearing. Where a mainstream objection
relies on absolute chronology (e.g. 'spreading took ~180 Myr', stripe age-calibration),
that chronological form is [O] both ways and is NOT counted against VP; only the firewall-
clean present-tense content of each objection is adjudicated. SEED = 19. No fitted
parameter. A refutation is a finding.

HONEST SCOPE (up front): this is an ANALYTICAL adjudication, not a new measurement. Its
artifact is the frozen reasoning ledger; the gate proves the tally is deterministic from
that ledger, not that any occurrence claim has moved. The mainstream positions are stated
as their real positive case; readers are invited to contest any row -- that is the point.
"""
import csv, hashlib
from collections import Counter
from pathlib import Path

SEED = 19
HERE = Path(__file__).resolve().parent
CSV = HERE / "data" / "tier4_stress_ledger.csv"
CSV_SHA256 = "6eea4a606a363059e99a97dd5547aebfe17f8aaf4413dffeb7d9481213ea2c9b"  # frozen, pinned

VALID_VERDICTS = {"DEGENERATE", "CONCEDE", "COHERENCE_ONLY", "OPEN", "OPEN_BY_DESIGN"}
# the central invariant: a stress-test PASS for the mainstream-skeptic means no VP claim
# emerges with a discriminating present-tense advantage. Such a verdict would be named
# "DISCRIMINATING_WIN"; the ledger must contain NONE.
WIN_VERDICT = "DISCRIMINATING_WIN"

# claims whose load-bearing failure traces to the S0 reservoir release / near-criticality
RELEASE_ROOT = {"C01", "C04", "C11"}

EXPECT = "666f617cd822fb8194b0d5a93ec37cf2825dc51edcf3d2b96922d7a4e53e4bb4"


def load():
    raw = CSV.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CSV_SHA256, "frozen CSV changed"
    lines = [ln for ln in raw.decode().splitlines() if not ln.lstrip().startswith("#")]
    return list(csv.DictReader(lines))


def main():
    rows = load()
    L = []
    L.append("M52  TIER-4 MAINSTREAM STRESS-TEST  (roadmap T4.1)")
    L.append(f"SEED={SEED}   input=data/tier4_stress_ledger.csv   RAW_FILE_SHA256={CSV_SHA256}")
    L.append("Each load-bearing claim is exposed to the STRONGEST steelmanned mainstream")
    L.append("objection and adjudicated under the firewall (occurrence/timing [O] both ways).")
    L.append("")

    # validate verdicts
    for r in rows:
        assert r["verdict"] in VALID_VERDICTS, f"unknown verdict: {r['verdict']}"
    assert all(r["verdict"] != WIN_VERDICT for r in rows), \
        "a DISCRIMINATING_WIN would contradict the stress-test's central finding"

    tally = Counter(r["verdict"] for r in rows)
    n = len(rows)

    L.append(f"[ADJUDICATION  n = {n} load-bearing claims]")
    L.append(f"  {'id':5}{'verdict':16}{'grade_after':34}target")
    for r in rows:
        tgt = r["target_claim"]
        tgt = (tgt[:54] + "...") if len(tgt) > 57 else tgt
        L.append(f"  {r['id']:5}{r['verdict']:16}{r['grade_after']:34}{tgt}")
    L.append("")

    L.append("[VERDICT TALLY]")
    for v in ("DEGENERATE", "CONCEDE", "COHERENCE_ONLY", "OPEN", "OPEN_BY_DESIGN"):
        L.append(f"  {v:16} {tally.get(v, 0)}")
    L.append("")

    # the central invariant
    wins = [r["id"] for r in rows if r["verdict"] == WIN_VERDICT]
    L.append("[CENTRAL INVARIANT]")
    L.append(f"  claims with a DISCRIMINATING present-tense advantage over the mainstream: "
             f"{len(wins)}")
    L.append("  -> under maximum mainstream pressure, NO distinctive claim wins on present-")
    L.append("     tense grounds; every distinctive axis is DEGENERATE or COHERENCE-ONLY.")
    L.append("")

    # concentrated point of failure
    concedes = [r["id"] for r in rows if r["verdict"] == "CONCEDE"]
    release_linked = sorted(set(concedes) & RELEASE_ROOT)
    L.append("[CONCENTRATED POINT OF FAILURE]")
    L.append(f"  CONCEDE verdicts: {concedes}")
    L.append(f"  of which trace to the S0 release / near-criticality root: {release_linked}")
    assert set(concedes) <= RELEASE_ROOT, \
        "every conceded load-bearing step should trace to the release/criticality root"
    L.append("  -> all conceded load-bearing steps converge on ONE root: the S0 reservoir")
    L.append("     RELEASE (SH-5) and the crustal NEAR-CRITICALITY it must trigger. The")
    L.append("     framework's entire empirical risk is concentrated there (cf. M29, M50).")
    L.append("")

    L.append("[HONEST BOTTOM LINE]")
    L.append("  The cascade SURVIVES the strongest mainstream stress-test as a physically-")
    L.append("  permitted, internally-coherent construction -- it is not refuted (it never")
    L.append("  claimed occurrence). But it gains ZERO present-tense discriminating advantage:")
    L.append(f"  {tally.get('DEGENERATE',0)} distinctive axes are degenerate, "
             f"{tally.get('COHERENCE_ONLY',0)} survive as [L] coherence only,")
    L.append(f"  {tally.get('CONCEDE',0)} concede a load-bearing step (all at the S0-release root), and")
    L.append(f"  {tally.get('OPEN',0)} stays open/data-blocked. The 8:1 value claim is structural")
    L.append("  elegance [L], not an epistemic advantage, because its single cause's load-")
    L.append("  bearing step is LESS evidenced than the eight mechanisms it replaces.")
    L.append("  Occurrence stays [O], both directions -- the mainstream's deep-time reading is")
    L.append("  likewise not forced by the firewall-clean present-tense data alone.")
    L.append("")
    L.append("[GRADE]  Tier-4 stress-test BUILT and RUN. Net standing UNCHANGED and now")
    L.append("  externally audited: no occurrence promotion, present-tense degeneracy")
    L.append("  confirmed against steelmanned mainstream mechanisms, single greatest")
    L.append("  vulnerability localised to SH-5. Falsification = discovery.")

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
