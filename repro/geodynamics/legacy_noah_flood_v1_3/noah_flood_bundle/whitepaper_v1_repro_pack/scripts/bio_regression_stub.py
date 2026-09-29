#!/usr/bin/env python3
# Minimal reproducible summary (no external libs required)
import sys, csv
from collections import Counter

def summarize_variants(tsv_path: str):
    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rs_count = Counter(r["rsID"] for r in reader)
    print("Variant count by rsID:", dict(rs_count))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: bio_regression_stub.py human_pigment_variants.tsv", file=sys.stderr)
        sys.exit(1)
    summarize_variants(sys.argv[1])
