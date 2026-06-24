#!/usr/bin/env python3
"""
synchrony_window_check.py -- VP Recent-Sequence Cascade, Module 32 (part C).
FIREWALL-NEUTRAL screen on the SYNCHRONY question: "all these regions declined at
the SAME time (~2300 BC)." This is the load-bearing claim of the strong reading,
and the screen shows precisely why it is capped at [O] in BOTH directions -- it is
an inference structure, true under any chronology, importing no past-occurrence model.

Two facts do the work:
  (1) Stratigraphic SUPERPOSITION gives ORDER WITHIN A SINGLE SITE only (layer B
      lies above layer A here). It NEVER, by itself, ties layer B at site X to
      layer B' at site Y. Cross-site simultaneity is not an order fact.
  (2) Therefore the ONLY bridge from "each site declines" to "all sites decline
      together" is the absolute-date column -- which is D5 / RECORD, forbidden as
      a load-bearing premise both ways (Constitution Art. 2). Remove it and the
      synchrony claim has no support; trust it and you have violated the firewall.

The screen also quantifies, from the held-out RECORD dates alone (used only to
refute 'one instant', never as truth), the SPREAD of the conventionally-assigned
dates, and contrasts the welcome reading (compress them to an instant) with the
unwelcome one (they really are centuries apart): the firewall caps BOTH -> [O].

SEED=19. Double-SHA-256 self-gate. Source: data/horizon_sites.csv (frozen).
"""
import csv, hashlib

SEED = 19
SRC = "data/horizon_sites.csv"

def load_dates():
    ds = []
    with open(SRC, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if r["continuity_flag"] == "0":              # the discontinuity sites
                ds.append((r["region"], int(r["record_date_bce"])))
    return ds

def ledger():
    ds = load_dates()
    vals = sorted(d for _, d in ds)
    spread = vals[-1] - vals[0]
    L = []
    L.append("MODULE=32C  SYNCHRONY-WINDOW CHECK  (firewall-neutral inference structure)")
    L.append("SEED=%d  n_discontinuity_sites=%d" % (SEED, len(ds)))
    L.append("")
    L.append("[1] WHAT SUPERPOSITION CAN AND CANNOT DO:")
    L.append("    within-site:  layer_above > layer_below            -> ORDER fact, present-tense [V]")
    L.append("    cross-site :  (site X layer) ?= (site Y layer)      -> NOT an order fact")
    L.append("    => superposition localises a decline at each site; it cannot make two sites simultaneous.")
    L.append("")
    L.append("[2] THE ONLY BRIDGE TO SYNCHRONY IS THE DATE COLUMN (D5/RECORD):")
    for region, d in sorted(ds, key=lambda t: t[1]):
        L.append("    %-13s conventionally-assigned: %d BCE   [RECORD, held out]" % (region, d))
    L.append("    sorted dates (BCE): %s" % ",".join(str(v) for v in vals))
    L.append("    SPREAD = %d yr  (%d BCE .. %d BCE)" % (spread, vals[-1], vals[0]))
    L.append("")
    L.append("[3] THE TWO READINGS, AND WHY THE FIREWALL CAPS BOTH:")
    L.append("    welcome reading   : 'compress the %d-yr spread to one instant ~2300 BC' -- needs the" % spread)
    L.append("                        dates to be wrong in a particular way -> uses RECORD as load-bearing.")
    L.append("    unwelcome reading : 'the spread is real; declines are centuries apart, not one event'")
    L.append("                        -- needs the dates to be RIGHT -> also uses RECORD as load-bearing.")
    L.append("    Constitution Art. 2: absolute dates are forbidden as load-bearing in BOTH directions.")
    L.append("    => neither 'one instant' nor 'centuries apart' may be asserted here.")
    L.append("")
    L.append("READING (firewall-clean, symmetric, honest):")
    L.append("  [V] Each site's discontinuity is present-tense and local (superposition + state).")
    L.append("  [O] Cross-site SYNCHRONY at a single ~2300 BC instant is UNDECIDED, both directions:")
    L.append("      it cannot be built from superposition, and the only alternative bridge is the")
    L.append("      absolute-date column, which the firewall forbids as load-bearing either way.")
    L.append("  The synchrony question is therefore routed, intact, to independent geochronology and")
    L.append("  the history channel -- it is not settled, and not refuted, by the material record alone.")
    return "\n".join(L)

def dsha(s): return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()
EXPECTED = "d9b3b86c281eaf24b0ee0d12126861397d8a9e1da0b6c41f4d8fa6e157f4540a"
if __name__ == "__main__":
    body = ledger(); print(body)
    d = dsha(body); print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
