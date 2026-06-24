#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M50  SH-5 RESERVOIR-BUDGET BOUND  --  the dominant [O] root, bounded present-tense
=================================================================================
SH-5 (the S0 reservoir's sufficiency) is the bottleneck the whole chain converges on: the
whitepaper flags flood-energy sourcing as "the demanding link" and carries an honest HOLD on
it. The roadmap (T2.2) asks: "what present-tense measurement bounds the releasable deep-water
fraction?" This module supplies the present-tense bound that the roadmap names.

WHAT IS PRESENT-TENSE (load-bearing [V]):
  - the deep-water INVENTORY: ringwoodite inclusions carry ~1.4 wt% H2O (a direct present
    sample), and transition-zone / bulk-mantle water is estimated at order ~1-2 ocean masses
    (1 ocean mass ~= 1.4e21 kg).
  - the water REQUIREMENTS: one large ice sheet ~5e18 kg; the whole present cryosphere
    ~2.6e19 kg; an illustrative ~0.1 ocean-mass surface flood pulse ~1.4e20 kg.

THE BOUND (a ratio of present magnitudes, no event, no rate, no date):
  inventory / requirement. If inventory >> requirement, then the INVENTORY is NOT the binding
  constraint, and the residual open question is narrowed to the RELEASABLE FRACTION + the
  release mechanism (which stay [O]). If inventory < requirement, SH-5 would be FORBIDDEN [F].

FIREWALL: present-tense inventories/requirements only. No release event, fraction, rate or
date is asserted; the RELEASE stays [O]/RECORD, both directions. SEED = 19. No fitted
parameter. Double-SHA-256 self-gate.

HONEST SCOPE: most figures are LIT (published estimates, wide ranges); they are used only to
bound an ORDER-OF-MAGNITUDE inventory/requirement ratio, not a precise number. The result
bounds the INVENTORY; it does NOT establish that any release occurred or that the releasable
fraction suffices -- those remain [O].
"""
import csv, hashlib, math
from pathlib import Path

SEED = 19
HERE = Path(__file__).resolve().parent
CSV = HERE / "data" / "s0_reservoir_budget.csv"
CSV_SHA256 = "0c5b71aa26f5cd3836a52e18ac87ca241331573e03baa4387413ea0bb31d5085"  # frozen, pinned
OCEAN_MASS_KG = 1.4e21

EXPECT = "363c6d3d504f7695ddf065bf0939decf9b906c3b5759a44f9703b484272a3341"  # pinned


def load():
    raw = CSV.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CSV_SHA256, "frozen CSV changed"
    lines = [ln for ln in raw.decode().splitlines() if not ln.lstrip().startswith("#")]
    return list(csv.DictReader(lines))


def main():
    rows = load()
    inv = {r["quantity"]: float(r["value_kg"]) for r in rows if r["kind"].startswith("inventory") and r["quantity"] != "ringwoodite_inclusion_H2O_wtpct"}
    req = {r["quantity"]: float(r["value_kg"]) for r in rows if r["kind"] == "requirement"}

    L = []
    L.append("M50  SH-5 RESERVOIR-BUDGET BOUND")
    L.append(f"SEED={SEED}   input=data/s0_reservoir_budget.csv   RAW_FILE_SHA256={CSV_SHA256}")
    L.append(f"unit: 1 ocean mass = {OCEAN_MASS_KG:.2e} kg")
    L.append("")
    L.append("[PRESENT-TENSE INVENTORY  (load-bearing [V] in magnitude)]")
    for k, v in inv.items():
        L.append(f"  {k:34}{v:.2e} kg  = {v/OCEAN_MASS_KG:6.2f} ocean masses")
    L.append("")
    L.append("[PRESENT-TENSE REQUIREMENTS]")
    for k, v in req.items():
        L.append(f"  {k:34}{v:.2e} kg  = {v/OCEAN_MASS_KG:6.3f} ocean masses")
    L.append("")

    inv_min = min(inv.values())
    req_max = max(req.values())
    ratio = inv_min / req_max
    L.append("[BOUND  (smallest inventory / largest requirement)]")
    L.append(f"  inventory_min = {inv_min:.2e} kg ; requirement_max = {req_max:.2e} kg")
    L.append(f"  inventory_min / requirement_max = {ratio:.1f}x  (~{math.log10(ratio):.1f} orders)")
    forbidden = inv_min < req_max
    L.append(f"  -> {'FORBIDDEN [F]: inventory below requirement' if forbidden else 'inventory EXCEEDS the largest requirement by ~' + format(ratio,'.0f') + 'x'}")
    L.append("")
    L.append("[INTERPRETATION]")
    L.append("  The present-tense deep-water INVENTORY is bounded [V] and, in magnitude,")
    L.append("  exceeds even the largest water requirement by ~an order of magnitude. So the")
    L.append("  INVENTORY is NOT the binding constraint on the chain.")
    L.append("  The residual open question NARROWS to the RELEASABLE FRACTION and the release")
    L.append("  mechanism/rate -- i.e. what fraction of this inventory can actually be mobilised")
    L.append("  to the surface in one event, and how. That stays [O]: no present-tense")
    L.append("  measurement here bounds a release fraction, and asserting one would import an")
    L.append("  occurrence. SH-5 is thus REFRAMED, not closed: inventory [V]-sufficient-in-")
    L.append("  magnitude; release fraction + mechanism remain the honest [O] root.")
    L.append("")
    L.append("[GRADE]")
    L.append("  SH-5: deep-water INVENTORY bounded present-tense [V] and not magnitude-limiting;")
    L.append("  RELEASABLE FRACTION + mechanism stay [O]-HOLD (the demanding link, now")
    L.append("  localised). This tightens the dominant [O] root from 'unbounded' to 'inventory")
    L.append("  ample, release fraction unknown'. Occurrence/ages [O]/RECORD, both directions.")
    L.append("  Falsification = discovery.")

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
