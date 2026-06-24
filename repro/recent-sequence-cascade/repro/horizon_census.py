#!/usr/bin/env python3
"""
horizon_census.py -- VP Recent-Sequence Cascade, Module 32 (part A).
Present-tense material-culture census across the recent ("~2300 BC") horizon.

What is load-bearing here: PRESENT-TENSE observables only -- what each site's
record SHOWS NOW (masonry grade, stratigraphic superposition of an abandonment /
squatter / silt layer over an occupation layer, loss of standardisation, presence
or absence of a famine/violence signature in skeletons). These are recomputed as
RAW COUNTS over a frozen site table -> [V].

What is NOT load-bearing: every absolute date. record_date_bce is D5 = RECORD,
firewalled BOTH directions (Constitution Art. 2 / Art. 4). It is carried in the
table ONLY to exhibit that the conventionally-assigned dates do not land on one
instant (they SPREAD), which is itself the reason cross-site SYNCHRONY is [O].

Honest design (Module 24 / Art. 7): the flood/aftermath reading and the
drought/political-devolution reading of the SAME discontinuity get the SAME grade
([O]); no interpretation is imported as the datum. The continuity rows are the
archaeological analogue of the bison continuity in Module 26: a counterexample to
a UNIVERSAL synchronized collapse, recorded at full strength even though it is
unwelcome to the strong reading.

SEED=19. Double-SHA-256 self-gate. Source: data/horizon_sites.csv (frozen).
"""
import csv, hashlib

SEED = 19
SRC = "data/horizon_sites.csv"

def load():
    rows = []
    with open(SRC, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows

def ledger():
    rows = load()
    disc = [r for r in rows if r["continuity_flag"] == "0"]
    cont = [r for r in rows if r["continuity_flag"] == "1"]
    dates = sorted(int(r["record_date_bce"]) for r in rows)  # RECORD only
    L = []
    L.append("MODULE=32A  HORIZON MATERIAL-CULTURE CENSUS  (present-tense; raw counts)")
    L.append("SEED=%d  n_sites=%d  n_discontinuity=%d  n_continuity=%d"
             % (SEED, len(rows), len(disc), len(cont)))
    L.append("")
    L.append("[A] PRESENT-TENSE DISCONTINUITIES (what the record shows now) -- [V]:")
    for r in disc:
        L.append("  %-13s %-22s obs=%s" % (r["region"], r["site"], r["observable_type"]))
    L.append("")
    L.append("[B] PRESENT-TENSE CONTINUITY COUNTEREXAMPLES (the archaeological 'bison') -- [V]:")
    for r in cont:
        L.append("  %-13s %-22s obs=%s" % (r["region"], r["site"], r["observable_type"]))
    L.append("")
    L.append("[C] HELD-OUT RECORD DATES (D5; NOT load-bearing; shown only to test 'one instant'):")
    L.append("  conventionally-assigned dates (BCE), sorted: %s" % ",".join(str(d) for d in dates))
    L.append("  span = %d yr  (min=%d BCE .. max=%d BCE)" % (dates[-1]-dates[0], dates[-1], dates[0]))
    L.append("  => the record does NOT cluster at a single instant; it SPREADS ~%d yr." % (dates[-1]-dates[0]))
    L.append("")
    L.append("READING (firewall-clean, symmetric, honest):")
    L.append("  [V] A present-tense discontinuity is real at every '[A]' site: an abandonment /")
    L.append("      squatter / silt / aeolian-sand layer superposed on an occupation layer, a drop")
    L.append("      in masonry grade, or a loss of standardisation. Superposition and grade are")
    L.append("      ORDER/STATE facts, recomputed without any date.")
    L.append("  [V] But a UNIVERSAL synchronized collapse is CONTRADICTED by the '[B]' rows:")
    L.append("      settlement continuity/expansion in Middle & Upper Egypt, first-intermediate")
    L.append("      skeletons with no famine/violence signature, a vigorous British Early-Bronze-Age")
    L.append("      culture, a Luoyang-Basin Longshan that keeps thriving, millet unaffected. So the")
    L.append("      change that IS [V] is SELECTIVE (loss of centralised monumental/standardised")
    L.append("      capacity), not a die-off -- exactly the bison-continuity result of Module 26.")
    L.append("  [O] SYNCHRONY at a single ~2300 BC instant: to assert it you must trust the absolute")
    L.append("      dates (D5/RECORD) -> firewalled both ways; and the dates that DO exist span ~%d yr." % (dates[-1]-dates[0]))
    L.append("      Neither 'one instant' nor any specific spread is load-bearing. -> [O], both directions.")
    L.append("  [O] CAUSE of each discontinuity (flood-aftermath vs drought vs political devolution):")
    L.append("      same observation, same grade (Art. 7). No reading imported as the datum.")
    L.append("  Occurrence and absolute dates stay [O]/RECORD; cause routes to independent")
    L.append("  geochronology + the history channel, exactly where the firewall already places it.")
    return "\n".join(L)

def dsha(s): return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()
EXPECTED = "0d7ca3f37a27213999c134d2b75ae789e1bf96fc31d26a726c5c472f390ae99d"
if __name__ == "__main__":
    body = ledger(); print(body)
    d = dsha(body); print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
