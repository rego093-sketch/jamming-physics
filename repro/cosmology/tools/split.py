#!/usr/bin/env python3
# tools/split.py — VP-SPEC Phase 0 tool 2/4 (RECONSTRUCTION, 2026-09-29).
# The original split.py is not in any surviving bundle. This rebuild does the step the pipeline names
# (preprocess_cosmology.py -> inventory.py -> split.py -> render_eq.js -> derive_meta.py -> build_hub.py -> gate.py):
# split the preprocessed whitepaper .tex into one body fragment per section, using ONLY the shared library
# inventory.py (section parsing, deterministic codes/slugs, body->HTML). Display equations are left as
# placeholders for render_eq.js. Deterministic; stdlib only.
#
# Usage:  python3 tools/split.py <paper_id> <preprocessed.tex> [--out build/split] [--check docs/<paper_id>]
#   --check lists slugs present in the tex but missing under docs/<paper_id>/ and vice versa.
# Limitation: the cosmology source VP_EarthCosmos_v2.tex is not in this repository, so the deployed pages
# cannot be regenerated from here; the deployed pages also carry later hand-added notes (lt-note asides).
import argparse, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inventory as inv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paper_id"); ap.add_argument("src")
    ap.add_argument("--out", default="build/split"); ap.add_argument("--check", default=None)
    a = ap.parse_args()
    tex, secs, rows = inv.build(a.paper_id, a.src)
    root = os.path.join(a.out, a.paper_id); os.makedirs(root, exist_ok=True)
    index = []
    for s, r in zip(secs, rows):
        d = os.path.join(root, s["slug"]); os.makedirs(d, exist_ok=True)
        body = s["cv"]["html"]
        open(os.path.join(d, "body.html"), "w", encoding="utf-8").write(body + "\n")
        json.dump({"displays": s["cv"]["displays"]}, open(os.path.join(d, "displays.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        index.append({"code": s["code"], "slug": s["slug"], "title": s["title_u"], "words": r["words"],
                      "body_sha256": hashlib.sha256(body.encode()).hexdigest()})
    json.dump(index, open(os.path.join(root, "split_index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[split] {a.paper_id}: {len(index)} sections -> {root}")
    if a.check:
        have = {n for n in os.listdir(a.check) if os.path.isdir(os.path.join(a.check, n))}
        want = {x["slug"] for x in index}
        print(f"[check] missing in {a.check}: {sorted(want - have)}"); print(f"[check] extra in {a.check}: {sorted(have - want)}")

if __name__ == "__main__":
    main()
