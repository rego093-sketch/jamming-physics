#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M53  ORDERING-SEAM DISCHARGE  (B.5 / roadmap T3.2)  -- the last author-held item, released
===========================================================================================
Module 30 closed the cascade's ORDERING seam CONDITIONALLY. Its sub-hypothesis SH-41 reads:

  "The ordering seam closes by one timeline (glaciation PRE-rupture, inherited responses
   POST-rupture) UNDER THE CONDITION that no post-opening response requires an ice-free
   pre-state.  [F] conditional; the condition is checkable, the failure branch pre-registered."

and M30 explicitly DEFERRED the check: "This should be verified against the inherited volume's
content; if any response is found to require an ice-free pre-state, the conflict is real and the
honest fix is to revise the pre-loading magnitude -- not to ignore the conflict (Art. 7)."

This module PERFORMS that deferred verification. It enumerates the inherited post-opening
responses of the parent Atlantic-Expansion volume (as inherited and confirmed in Module 21) and
adjudicates each against ONE question:

      does this response's MECHANISM require the pre-rupture crust to be ICE-FREE?

PRE-REGISTERED DECISION RULE (declared before adjudication, in the frozen ledger):
  the ordering condition is DISCHARGED iff the CONFLICT count is exactly 0.
  Any CONFLICT keeps the seam open and routes to the Art.7 revision branch (revise the
  pre-loading magnitude; do NOT ignore the conflict).

FIREWALL: present-tense MECHANISM only. No absolute age, rate, or occurrence is load-bearing
(all [O]/RECORD, both directions). The check is about ice-free PRESUPPOSITION, not timing.
SEED = 19. No fitted parameter. No new physics. Double-SHA-256 self-gate.

HONEST SCOPE: discharging this condition closes only the ORDERING internal-consistency seam.
It does NOT touch the trigger near-criticality (SH-40), the S0 release (SH-5), or occurrence --
those stay [O]. The loading-vs-unloading direction of the trigger is the separate TRIGGER seam
(M30 section 1, SH-39/40), not this ordering check.
"""
import csv, hashlib
from collections import Counter
from pathlib import Path

SEED = 19
HERE = Path(__file__).resolve().parent
CSV = HERE / "data" / "orderseam_iceFree_ledger.csv"
CSV_SHA256 = "93b09bc511af7822c6a248e404dcf95503b8a1d7d6477cfe551f86c9825b5d2d"  # frozen, pinned

VALID = {"CONSISTENT", "REINFORCED", "CONFLICT"}
# pre-registered: the condition is discharged iff exactly this many CONFLICTs
CONFLICT_BUDGET = 0

EXPECT = "99ae5363120fdae313b6c5d186814abbfccb2531fa99ec4f3ac657ef22586ffa"


def load():
    raw = CSV.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CSV_SHA256, "frozen CSV changed"
    lines = [ln for ln in raw.decode().splitlines() if not ln.lstrip().startswith("#")]
    return list(csv.DictReader(lines))


def main():
    rows = load()
    L = []
    L.append("M53  ORDERING-SEAM DISCHARGE  (B.5 / roadmap T3.2)")
    L.append(f"SEED={SEED}   input=data/orderseam_iceFree_ledger.csv   RAW_FILE_SHA256={CSV_SHA256}")
    L.append("Deferred check from M30/SH-41: does any inherited POST-opening response require an")
    L.append("ICE-FREE pre-rupture state? Pre-registered: condition DISCHARGED iff CONFLICTs == 0.")
    L.append("")

    for r in rows:
        assert r["verdict"] in VALID, f"unknown verdict: {r['verdict']}"
        assert r["requires_ice_free_pre_state"] in ("YES", "NO"), "bad flag"
        # internal consistency: only a YES flag may be a CONFLICT, and a CONFLICT must be YES
        if r["verdict"] == "CONFLICT":
            assert r["requires_ice_free_pre_state"] == "YES", "CONFLICT must require ice-free"
        else:
            assert r["requires_ice_free_pre_state"] == "NO", "non-CONFLICT must not require ice-free"

    tally = Counter(r["verdict"] for r in rows)
    n = len(rows)

    L.append(f"[INHERITED POST-OPENING RESPONSES CHECKED  n = {n}]")
    L.append(f"  {'id':4}{'ice-free?':11}{'verdict':12}response")
    for r in rows:
        resp = r["inherited_response"]
        resp = (resp[:60] + "...") if len(resp) > 63 else resp
        L.append(f"  {r['id']:4}{r['requires_ice_free_pre_state']:11}{r['verdict']:12}{resp}")
    L.append("")

    L.append("[TALLY]")
    for v in ("CONSISTENT", "REINFORCED", "CONFLICT"):
        L.append(f"  {v:12} {tally.get(v, 0)}")
    L.append("")

    conflicts = tally.get("CONFLICT", 0)
    discharged = (conflicts == CONFLICT_BUDGET)

    L.append("[PRE-REGISTERED DECISION]")
    L.append(f"  CONFLICT budget = {CONFLICT_BUDGET};  observed CONFLICTs = {conflicts}")
    assert discharged, ("a CONFLICT was found: the ordering condition FAILS and routes to the "
                        "Art.7 revision branch (revise the pre-loading magnitude).")
    L.append("  observed CONFLICTs == budget -> the ordering condition is DISCHARGED.")
    L.append("")

    reinforced = [r["id"] for r in rows if r["verdict"] == "REINFORCED"]
    L.append("[WHAT THE CHECK FOUND]")
    L.append("  No inherited post-opening response presupposes an ice-free pre-rupture state.")
    L.append(f"  Moreover, {len(reinforced)} response(s) {reinforced} are REINFORCED: they positively")
    L.append("  REQUIRE the glacial pre-state (petroleum source rock needs the meltwater lid), so an")
    L.append("  ice-free pre-state would BREAK them -- the strict opposite of presupposing ice-free.")
    L.append("  The one-timeline reading (glaciation pre-rupture; inherited responses post-rupture)")
    L.append("  therefore holds UNCONDITIONALLY: the M30 condition is met, not merely assumed.")
    L.append("")

    L.append("[GRADE]")
    L.append("  SH-41 promoted from '[F] conditional' to [F] DISCHARGED (condition verified against")
    L.append("  the inherited volume's content, response by response). The B.5 ordering seam is now")
    L.append("  closed unconditionally. RESIDUE (unchanged, [O]): the trigger near-criticality")
    L.append("  (SH-40), the S0 release (SH-5), and occurrence/timing stay [O], both directions.")
    L.append("  No occurrence promoted; no new physics; no dates. Falsification = discovery.")

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
