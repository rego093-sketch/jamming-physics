#!/usr/bin/env python3
# Demonstrative reader for RSL_all_sites.csv; prints site counts
import sys, csv
from collections import Counter

def run(rsl_csv):
    with open(rsl_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        sites = [r["site_id"] for r in reader]
    cnt = Counter(sites)
    for k, v in cnt.items():
        print(f"{k}: {v} rows")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: rsl_fit_stub.py data/RSL_Delta_BIO_Finalize/RSL_all_sites.csv", file=sys.stderr)
        sys.exit(1)
    run(sys.argv[1])
