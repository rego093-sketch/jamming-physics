#!/usr/bin/env python3
"""tools/update_sitemap_lastmod.py — set each <lastmod> in docs/sitemap.xml to the date the page file last
changed in git (committed date, YYYY-MM-DD). A file with uncommitted changes gets today's date.
Only <lastmod> values change; the URL set is left as it is. Deterministic for a given git state."""
import datetime, os, re, subprocess
from urllib.parse import urlparse
SM = "docs/sitemap.xml"
s = open(SM, encoding="utf-8").read()
today = datetime.date.today().isoformat()
out = subprocess.run(["git", "log", "--name-only", "--format=@%cs", "--", "docs"], capture_output=True, text=True).stdout
last = {}; d = None
for line in out.splitlines():
    if line.startswith("@"): d = line[1:]
    elif line.strip() and line not in last: last[line] = d
dirty = set(subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "docs"], capture_output=True, text=True).stdout.split())
def path_of(loc):
    p = urlparse(loc).path
    return "docs" + (p + "index.html" if p.endswith("/") else p)
changed = 0
def fix(m):
    global changed
    loc, lm = m.group(1), m.group(2)
    f = path_of(loc)
    new = today if f in dirty else last.get(f, lm)
    if new != lm: changed += 1
    return m.group(0).replace(f"<lastmod>{lm}</lastmod>", f"<lastmod>{new}</lastmod>")
s2 = re.sub(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", fix, s)
open(SM, "w", encoding="utf-8").write(s2)
missing = [f for f in (path_of(l) for l in re.findall(r"<loc>([^<]+)</loc>", s)) if not os.path.exists(f)]
print(f"[sitemap] lastmod updated: {changed}; urls whose file is missing: {len(missing)}")
