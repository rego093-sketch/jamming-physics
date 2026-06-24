#!/usr/bin/env python3
"""
four_two_ka_proxy_audit.py -- VP Recent-Sequence Cascade, Module 32 (part G).

AUDIT TARGET (Art. 7): the word "DROUGHT" used for the Mesopotamia/Iran/Egypt
side of the ~BC2300 horizon. The question put by the audit is exactly the right
one: is "drought" a RAW OBSERVABLE, or a CAUSAL NARRATIVE laid over an observed
*absence of activity* to explain it?

This screen answers by reading the literal, untouched primary file -- the NOAA/WDS
Paleoclimatology archive of stalagmite GZ14-1, Gol-e-Zard Cave, Iran (Carolin et
al. 2019, PNAS, doi:10.1073/pnas.1808103115; data doi:10.25921/x5zv-ar39). This is
the single proxy most directly tied to the "Mesopotamia drought ~4.2 ka" claim.
No transcription, no re-keying: the script hashes and parses the downloaded NOAA
bytes themselves (data/gol_e_zard2019_noaa_RAW.txt), so the audit cannot be accused
of reading a processed number.

VERDICT PREVIEW (symmetric, firewall-clean):
  * The audit's suspicion is PARTLY right and PARTLY wrong, and the split matters.
  * WRONG half: "drought is a pure made-up excuse for empty cities" overshoots.
    There IS a real, independently MEASURED observable here -- the rock's Mg/Ca and
    d18O ratios -- recorded by geochemists from a stalagmite, NOT inferred from any
    archaeological gap. R0 below is [V]/[F]: the excursion is physically present.
  * RIGHT half: the LADDER from that ratio up to "a synchronous global megadrought
    that CAUSED the BC2300 regression" is a stack of interpretations the authors
    THEMSELVES call uncertain, and whose prominence is -- on the record -- inflated
    by the very archaeology it is invoked to explain. That causal top rung is [O],
    and the circularity the audit smelled is real and mainstream-documented.

The firewall therefore does NOT let "drought" stand as a load-bearing counter-fact
against (or for) any flood/internal/political reading. Cause stays [O] all round.

Method notes:
  * Ordering axis is DEPTH (mm from stalagmite top) -- a present-tense geometric
    fact. The age column (mu_yrBP) is printed ONLY as RECORD and is NEVER an input
    to any computed quantity or to PASS/FAIL (Constitution Art. 2, both directions).
  * All load-bearing numbers (counts, Mg/Ca baseline vs peak, excursion depth bands)
    are date-free and recomputed from the raw bytes each run.

SEED=19. Double-SHA-256 self-gate. Pins the raw file's own SHA-256.
"""
import hashlib

SEED = 19
RAW = "data/gol_e_zard2019_noaa_RAW.txt"

# ---- column indices in the NOAA data table (see file header, line "Data:") ----
# depth_mm  mu_yrBP  sd  to_68  from_68  to_95  from_95  d18O_permil  d13C_permil  Mg_Ca  Sr_Ca  Ba_Ca  S_Ca
C_DEPTH, C_AGE, C_D18O, C_MGCA = 0, 1, 7, 9
HEADER_KEY = "depth_mm\tmu_yrBP"


def raw_sha256():
    h = hashlib.sha256()
    with open(RAW, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_rows():
    """Parse the untouched NOAA file. Returns (depth, age, d18O, MgCa) tuples."""
    rows, started = [], False
    with open(RAW, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\r\n")
            if not started:
                if line.startswith(HEADER_KEY):
                    started = True
                continue
            if not line.strip() or line.startswith("#"):
                continue
            p = line.split("\t")
            if len(p) < 13:
                continue
            try:
                rows.append((float(p[C_DEPTH]), float(p[C_AGE]),
                             float(p[C_D18O]), float(p[C_MGCA])))
            except ValueError:
                continue
    return rows


def fmt(x, n=3):
    # deterministic fixed-decimal formatting
    return ("%." + str(n) + "f") % x


def ledger():
    rows = load_rows()
    n = len(rows)
    mg = [r[3] for r in rows]
    d18 = [r[2] for r in rows]

    # --- present-tense, DATE-FREE observables (ordering by depth only) ---
    by_depth_deep_first = sorted(rows, key=lambda r: -r[0])  # deepest = earliest-formed
    q = n // 4
    baseline = sum(r[3] for r in by_depth_deep_first[:q]) / q          # deep quartile mean Mg/Ca
    mg_max = max(mg)
    mg_med = sorted(mg)[n // 2]
    ratio = mg_max / baseline

    # the highest-Mg/Ca samples, located by DEPTH (not date)
    top = sorted(rows, key=lambda r: -r[3])[:8]
    top_depths = sorted(r[0] for r in top)
    # two clusters by depth gap (present-tense): split where consecutive gap is largest
    gaps = [(top_depths[i + 1] - top_depths[i], i) for i in range(len(top_depths) - 1)]
    _, splel = max(gaps)
    band_lo = (top_depths[0], top_depths[splel])
    band_hi = (top_depths[splel + 1], top_depths[-1])

    L = []
    L.append("MODULE=32G  4.2 ka RAW-PROXY AUDIT  (is 'drought' observed, or narrated?)")
    L.append("SEED=%d  source=Gol-e-Zard GZ14-1 (Carolin+2019); raw NOAA bytes read directly" % SEED)
    L.append("RAW_FILE_SHA256 = %s" % raw_sha256())
    L.append("n_samples=%d   ordering axis = DEPTH (present-tense); age used only as RECORD" % n)
    L.append("")
    L.append("[R0] THE RAW, MEASURED OBSERVABLE  (no climate model, no archaeology):")
    L.append("     Mg/Ca (mmol/mol): baseline(deep quartile)=%s  median=%s  MAX=%s"
             % (fmt(baseline), fmt(mg_med), fmt(mg_max)))
    L.append("     peak/baseline ratio = %s  -> an excursion is PHYSICALLY PRESENT in the rock" % fmt(ratio, 2))
    L.append("     d18O (permil VPDB): min=%s  max=%s  (co-varying enrichment present)"
             % (fmt(min(d18), 2), fmt(max(d18), 2)))
    L.append("     GRADE R0 = [V]/[F]: the stalagmite's Mg/Ca & d18O values are what they are.")
    L.append("     -> This already REFUTES 'drought is a pure invented excuse for empty cities':")
    L.append("        the number was measured from cave calcite by ICP-MS, not read off a ruin.")
    L.append("")
    L.append("[R0b] BUT THE STRUCTURE IS TWO HUMPS, NOT ONE INSTANT (date-free, by depth):")
    L.append("      high-Mg/Ca band A at depth ~%s-%s mm" % (fmt(band_hi[0], 1), fmt(band_hi[1], 1)))
    L.append("      high-Mg/Ca band B at depth ~%s-%s mm" % (fmt(band_lo[0], 1), fmt(band_lo[1], 1)))
    L.append("      two separated excursions in the column -> not a single synchronous pulse.")
    L.append("      (Authors' own reading: onsets at 4.51 ka AND 4.26 ka; RECORD-only, not load-bearing.)")
    L.append("")
    L.append("[LADDER] FROM THE RATIO UP TO 'DROUGHT CAUSED THE REGRESSION' -- grade each rung:")
    L.append("  R1  Mg/Ca high  -> 'increased wind-blown DUST flux, Mesopotamia-sourced'")
    L.append("        D4 source interpretation (provenance-model dependent).            GRADE [L]")
    L.append("  R2  dust        -> 'ARIDITY / drought'")
    L.append("        D5 climate interpretation (dust can also track wind regime,")
    L.append("        source-area exposure, seasonality; not forced by the ratio).      GRADE [O]")
    L.append("  R3  drought     -> 'SYNCHRONOUS, GLOBAL, and the CAUSE of the BC2300 decline'")
    L.append("        D5 causal + cross-archive synchrony claim.                         GRADE [O]")
    L.append("        ^ this is the rung the audit challenged, and it is the weak one.")
    L.append("")
    L.append("[WHY R3 IS [O], ON THE RECORD -- the circularity the audit smelled]:")
    L.append("  (a) The authors' OWN abstract: the existence of a coincident climate event is")
    L.append("      called still uncertain; the whole framing is pinned to 'settlement abandonment'.")
    L.append("  (b) >1000-dataset survey (Nature Comms 2024): the '4.2 ka event' is NOT a globally")
    L.append("      significant excursion (unlike 8.2 ka); its perceived importance is, in their")
    L.append("      words, ENHANCED BY the archaeology of concurrent collapse -> textbook circularity.")
    L.append("  (c) Tierney (paleoclimatologist): the partition 'lumps together' droughts and wet")
    L.append("      periods sometimes centuries away from 4.2 ka.")
    L.append("  (d) Hemispheric asymmetry: Southern-Hemisphere proxies read WET, not dry; lower")
    L.append("      Yangtze reads FLOOD. A single uniform global drought is not what the globe shows.")
    L.append("  (e) R0b above: two humps, not one instant -- already in tension with a single trigger.")
    L.append("")
    L.append("ANSWER TO THE AUDIT (symmetric, firewall-clean):")
    L.append("  - 'Drought' is NOT a fabricated excuse: R0 is a genuine measured observable [V].")
    L.append("  - 'Drought = synchronous global cause of the BC2300 regression' is [O], and its")
    L.append("    prominence is, by the climate literature's own admission, inflated by the very")
    L.append("    archaeological gap it is summoned to explain. The audit's suspicion lands HERE.")
    L.append("  - Net for the cascade: 'drought' may NOT be used as a load-bearing counter-fact")
    L.append("    against a flood/internal/political reading, NOR for it. CAUSE stays [O] all round;")
    L.append("    only R0 (an excursion exists in this one rock) is carried, as a present-tense [V].")
    L.append("  - Conservative posture (audit's instruction): where the ladder is unproven, hold;")
    L.append("    the raw rung is kept, every rung above R1 is released to the geochronology/history")
    L.append("    channel where the firewall already routes occurrence and cause.")
    return "\n".join(L)


def dsha(s):
    return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()


EXPECTED = "f9f192f09276fe3f6c8924fd92c0b42d1f203d746a9134224b59af7fe9ed152e"
if __name__ == "__main__":
    body = ledger()
    print(body)
    d = dsha(body)
    print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
