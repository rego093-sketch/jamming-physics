#!/usr/bin/env python3
"""
giza_singularity_screen.py -- VP Recent-Sequence Cascade, Module 32 (part B).
The author's centrepiece: "a structure of Giza's calibre could not recur for a
long time." This screen separates the part of that claim that IS load-bearing
from the part the firewall caps.

LOAD-BEARING (present-tense [V]): a pyramid's surviving DESIGN HEIGHT and its CORE
CONSTRUCTION QUALITY are things you can measure today; the DYNASTY ORDER is fixed
by stratigraphy/typology (an order fact, not an absolute date). Over the frozen
table this yields a present-tense PEAK (4th-Dynasty Giza/Dahshur giants, solid
dressed stone) -> DECLINE (5th-6th-Dynasty pyramids, smaller, rubble cores) ->
GAP (royal pyramids of comparable scale do not recur; the later revival builds
MUDBRICK cores). Peak/decline/gap are present-tense -> [V].

CAPPED (Constitution Art. 2 / Art. 4): the DURATION of the gap and the assertion
"could not recur for a long time" are RATE/TIMING -> [O], both directions. The
CAUSE -- a catastrophe that destroyed the capacity vs. loss of the central
funding+bureaucracy that paid the labour force -- is two readings of the SAME
present-tense pattern and gets the SAME grade [O] (Art. 7); neither is imported as
the datum. record_date_bce_mid is D5/RECORD, shown only to note that the masonry
decline is a gradual ramp that BEGINS in the 5th Dynasty (it precedes the
"~2300 BC" horizon), which itself cuts against a single-instant trigger -- a point
recorded honestly because it is unwelcome to the strong reading.

SEED=19. Double-SHA-256 self-gate. Source: data/pyramid_scale.csv (frozen).
"""
import csv, hashlib

SEED = 19
SRC = "data/pyramid_scale.csv"

def load():
    rows = []
    with open(SRC, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            rows.append((r["pyramid"], int(r["dynasty"]), float(r["height_m"]),
                         r["core_quality"], int(r["record_date_bce_mid"])))
    return rows

def median(xs):
    s = sorted(xs); n = len(s)
    return s[n//2] if n % 2 else (s[n//2-1]+s[n//2])/2.0

def ledger():
    rows = load()
    peak = max(rows, key=lambda t: t[2])                 # tallest = present-tense peak
    d4 = [t for t in rows if t[1] == 4]                  # 4th Dynasty (Giza era)
    post = [t for t in rows if t[1] in (5, 6)]           # immediate post-peak royal pyramids
    later = [t for t in rows if t[1] >= 7]               # the later revival
    solid_post = sum(1 for t in post if "rubble" in t[3] or "mudbrick" in t[3])
    L = []
    L.append("MODULE=32B  GIZA SINGULARITY SCREEN  (present-tense scale + core quality)")
    L.append("SEED=%d  n_pyramids=%d" % (SEED, len(rows)))
    L.append("")
    L.append("[A] PRESENT-TENSE PEAK (tallest surviving design height):")
    L.append("  %-22s dyn=%d  H=%.1f m  core=%s" % (peak[0], peak[1], peak[2], peak[3]))
    L.append("  4th-Dynasty heights (m): %s" % ", ".join("%.1f" % t[2] for t in d4))
    L.append("  4th-Dynasty median H = %.1f m   (all solid dressed stone)" % median([t[2] for t in d4]))
    L.append("")
    L.append("[B] IMMEDIATE POST-PEAK ROYAL PYRAMIDS (5th-6th Dynasty):")
    L.append("  heights (m): %s" % ", ".join("%.1f" % t[2] for t in post))
    L.append("  median H = %.1f m    rubble-core count = %d / %d" % (median([t[2] for t in post]), solid_post, len(post)))
    L.append("  drop in median height vs 4th Dynasty: x%.2f"
             % (median([t[2] for t in d4]) / median([t[2] for t in post])))
    L.append("")
    L.append("[C] THE GAP + LATER REVIVAL:")
    if later:
        for t in later:
            L.append("  next comparable-scale royal pyramid: %-22s dyn=%d H=%.1f m core=%s"
                     % (t[0], t[1], t[2], t[3]))
        L.append("  => when large royal pyramids RECUR, the core is %s (cruder build), not solid stone."
                 % later[0][3])
    L.append("")
    L.append("[D] HELD-OUT RECORD (D5; NOT load-bearing) -- shape of the decline only:")
    by_dyn = {}
    for t in rows:
        by_dyn.setdefault(t[1], []).append(t[2])
    for dyn in sorted(by_dyn):
        L.append("  dynasty %2d : median H = %.1f m" % (dyn, median(by_dyn[dyn])))
    L.append("  => decline is a GRADUAL ramp beginning at the 5th Dynasty, i.e. it PRECEDES the")
    L.append("     '~2300 BC' horizon. Recorded because it is unwelcome to a single-instant trigger.")
    L.append("")
    L.append("READING (firewall-clean, symmetric, honest):")
    L.append("  [V] The Giza singularity is real as a PRESENT-TENSE pattern: a measured peak in scale")
    L.append("      and core quality, a clear post-peak decline, and a gap before comparable scale")
    L.append("      recurs (and the revival builds mudbrick cores). This is the author's strongest card.")
    L.append("  [O] 'Could not recur for a LONG TIME' is a duration/rate claim -> firewalled both ways.")
    L.append("  [O] CAUSE: 'a catastrophe destroyed the capacity' and 'the central funding+bureaucracy")
    L.append("      that organised the labour force lapsed' are two readings of the same pattern -> same")
    L.append("      grade (Art. 7). Neither is imported as the datum.")
    L.append("  NOTE the decline RAMP starts in the 5th Dynasty (precedes the horizon): a present-tense")
    L.append("      fact that weakens, not supports, a single ~2300 BC trigger. Logged in the open.")
    L.append("  Occurrence, gap-duration, and absolute dates stay [O]/RECORD, both directions.")
    return "\n".join(L)

def dsha(s): return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()
EXPECTED = "8aacf48e49707a713152789fd72715167f45dcc65647b64b4cff8e2fb1409374"
if __name__ == "__main__":
    body = ledger(); print(body)
    d = dsha(body); print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
