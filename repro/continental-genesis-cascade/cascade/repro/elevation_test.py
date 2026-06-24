#!/usr/bin/env python3
"""
elevation_test.py -- VP Recent-Sequence Cascade, Module 26 (part C).
The elevation discriminator: a FALSIFIABLE test of the flood-contamination reading.
Prediction (author): apparent 14C age should ANTI-correlate with elevation
(high=young, low=old), especially WITHIN a region.

Data: data/elevation_sample.json -- a SEED=19 reproducible sample of p3k14c
(all Homo + all Mammuthus + 8000 random others) with Copernicus DEM elevation
attached (via open-meteo elevation API), frozen here for offline repro.
NOTE: p3k14c coordinates are fuzzed / county-aggregated -> elevation is noisy
(attenuates correlations). 14C ages are D5=RECORD; used only as a bias indicator
(correlation STRUCTURE), never as truth.

RESULT (recorded): within-region the prediction FAILS / reverses -- Europe and
North America show POSITIVE Spearman (high=OLDER), opposite to prediction; global
elevation bands superficially match the prediction but that is a region-MIX
(Simpson) artifact. Elevation is a poor proxy for the true driver (carbonate
geochemistry). SEED=19. Double-SHA-256 self-gate.
"""
import json, hashlib, math
SEED = 19
SRC = "data/elevation_sample.json"

def spearman(a, b):
    n = len(a)
    ra = _rank(a); rb = _rank(b)
    ma = sum(ra)/n; mb = sum(rb)/n
    num = sum((x-ma)*(y-mb) for x, y in zip(ra, rb))
    da = math.sqrt(sum((x-ma)**2 for x in ra)); db = math.sqrt(sum((y-mb)**2 for y in rb))
    return num/(da*db) if da*db else 0.0

def _rank(v):
    idx = sorted(range(len(v)), key=lambda i: v[i])
    r = [0]*len(v)
    for pos, i in enumerate(idx): r[i] = pos
    return r

def f3(x): return f"{x:.3f}"

def ledger():
    samp = json.load(open(SRC))
    age = [x["age"] for x in samp]; el = [x["elev"] for x in samp]
    L = ["MODULE=26C SEED=%d n=%d" % (SEED, len(samp))]
    L.append("GLOBAL spearman_elev_age=%s" % f3(spearman(el, age)))
    from collections import defaultdict
    byc = defaultdict(list)
    for x in samp: byc[x["cont"]].append(x)
    for c in sorted(byc):
        xs = byc[c]
        if len(xs) < 40: continue
        r = spearman([x["elev"] for x in xs], [x["age"] for x in xs])
        L.append("CONT %s n=%d spearman=%s" % (c, len(xs), f3(r)))
    # elevation bands -> median age (the Simpson-confounded global view)
    bands = [(-100, 0), (0, 200), (200, 500), (500, 1000), (1000, 2000), (2000, 6000)]
    for lo, hi in bands:
        a = sorted(x["age"] for x in samp if lo <= x["elev"] < hi)
        if len(a) > 20:
            med = a[len(a)//2] if len(a) % 2 else (a[len(a)//2-1]+a[len(a)//2])/2
            L.append("BAND %d_%d n=%d median_age=%.0f" % (lo, hi, len(a), med))
    return "\n".join(L)

def dsha(s): return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()
EXPECTED = "cc9db07edf24be97d664e254f2a54d2ad5ddf41e5a22b8a7d2e1dc64a3e07e60"
if __name__ == "__main__":
    body = ledger(); print(body)
    d = dsha(body); print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
