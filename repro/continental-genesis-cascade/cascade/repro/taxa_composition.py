#!/usr/bin/env python3
"""
taxa_composition.py -- VP Recent-Sequence Cascade, Module 26 (part B).
Raw taxa-composition audit over a FROZEN subset of p3k14c (Bird et al. 2022,
the public scrubbed/fuzzed cut). Source: data/taxa_subset.csv (records whose
Taxa tag matches the relevant human/megafauna genera; frozen for offline repro).

Reports ONLY raw counts ([V]). Attached 14C ages are D5 = RECORD, firewalled
both directions; used here only as a recorded value, never as truth. No model,
no interpretation. SEED=19. Double-SHA-256 self-gate.

KEY LIMIT (recorded, not hidden): p3k14c is an ARCHAEOLOGICAL radiocarbon DB,
NOT a palaeontological faunal census -> DISCOVERED != EXISTING (Module 23).
Human skeletal records are REDACTED in the public cut; Homo here is coprolite-
dominated. Elephas/Loxodonta = 0 is a GEOGRAPHIC sampling artifact.
"""
import csv, hashlib
SEED = 19
SRC = "data/taxa_subset.csv"
GROUPS = {
    "Homo":    ["homo", "human", "sapiens"],
    "Mammuthus":["mammuthus", "mammoth"],
    "Mammut":  ["mammut americ", "mastodon"],
    "Bison":   ["bison"],
    "Elephas": ["elephas", "loxodonta"],
}
BOUND = 4000.0   # ~2300 BC in uncalibrated 14C BP (approx; ages are RECORD)

def load():
    rows = []
    with open(SRC, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            try: a = float(r["Age"])
            except: continue
            rows.append((a, (r["Taxa"] or "").lower(), (r["Continent"] or "").strip()))
    return rows

def median(xs):
    s = sorted(xs); n = len(s)
    return s[n//2] if n % 2 else (s[n//2-1]+s[n//2])/2

def ledger():
    rows = load()
    L = ["MODULE=26B SEED=%d n_subset=%d boundary_14CBP=%.0f" % (SEED, len(rows), BOUND)]
    for g, ks in GROUPS.items():
        ages = [a for a, t, c in rows if any(k in t for k in ks)]
        if not ages:
            L.append("%s n=0" % g); continue
        older = sum(1 for a in ages if a >= BOUND)
        younger = sum(1 for a in ages if a < BOUND)
        L.append("%s n=%d min=%.0f med=%.0f max=%.0f older>=B=%d younger<B=%d"
                 % (g, len(ages), min(ages), median(ages), max(ages), older, younger))
    return "\n".join(L)

def dsha(s): return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()
EXPECTED = "39cd3b8e1a712fe7f6801362fa034f72aa6c81d8e87ce80e56ca625581a237bd"
if __name__ == "__main__":
    body = ledger(); print(body)
    d = dsha(body); print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
