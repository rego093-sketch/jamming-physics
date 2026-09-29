#!/usr/bin/env python3
"""tools/record_page_notes.py — record how many correction notes (<aside class="lt-note">) each page carries.

The gate fails if any page later carries FEWER notes than recorded. This catches an old volume builder
(or any regeneration) silently overwriting corrected pages. Counts only ever go up: run this after adding
notes. Usage: python3 tools/record_page_notes.py [--check]"""
import glob, json, sys
REC = "registry/page_notes.json"
cur = {}
for p in sorted(glob.glob("docs/**/*.html", recursive=True)):
    n = open(p, encoding="utf-8", errors="ignore").read().count('<aside class="lt-note"')
    if n: cur[p] = n
try: old = json.load(open(REC, encoding="utf-8"))
except FileNotFoundError: old = {}
lost = {p: (n, cur.get(p, 0)) for p, n in old.items() if cur.get(p, 0) < n}
if "--check" in sys.argv:
    print(f"[notes] pages with correction notes: {len(cur)}; pages that lost notes: {len(lost)}")
    for p, (a, b) in list(lost.items())[:5]: print(f"   {p}: {a} -> {b}")
    sys.exit(1 if lost else 0)
merged = {p: max(old.get(p, 0), cur.get(p, 0)) for p in set(old) | set(cur)}
json.dump(dict(sorted(merged.items())), open(REC, "w", encoding="utf-8"), indent=0)
print(f"[notes] recorded {len(merged)} pages, {sum(merged.values())} notes; lost now: {len(lost)}")
