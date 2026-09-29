#!/usr/bin/env python3
# Demonstrative converter that echoes Nile thickness rows and years
import sys, csv, json

def run(nile_core_csv):
    rows = []
    with open(nile_core_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    print(json.dumps({"nile_cores": rows}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: delta_convert_stub.py data/RSL_Delta_BIO_Finalize/nile_core_map.csv", file=sys.stderr)
        sys.exit(1)
    run(sys.argv[1])
