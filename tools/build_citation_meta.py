#!/usr/bin/env python3
"""tools/build_citation_meta.py — Highwire/Google Scholar citation meta tags for every volume hub.

Regenerates one block per hub, between <!--vp-cite-start--> and <!--vp-cite-end-->, from
registry/vp.manifest.json (DOI, hub) and the hub's own <title>. Idempotent.
  * removes older citation_* meta tags and the "Phase 7" slot comments (including HTML-escaped ones
    that rendered as visible text);
  * citation_publication_date is written ONLY when the volume's own pages carry a date
    (JSON-LD datePublished or an earlier citation tag); otherwise it is left out and listed;
  * no citation_pdf_url unless a real .pdf is known (a DOI landing page is not a PDF).
Usage: python3 tools/build_citation_meta.py [--check]
"""
import glob, json, re, sys, collections

AUTHOR = "Young Jae Lee"
man = json.load(open("registry/vp.manifest.json", encoding="utf-8"))
check = "--check" in sys.argv
missing_date, changed = [], []

def volume_date(vid):
    c = collections.Counter()
    for p in glob.glob(f"docs/{vid}/**/index.html", recursive=True):
        s = open(p, encoding="utf-8").read()
        for d in re.findall(r'"datePublished"\s*:\s*"(\d{4}(?:-\d{2}-\d{2})?)"', s): c[d] += 1
        for d in re.findall(r'name="citation_publication_date" content="(\d{4}(?:[-/]\d{2}[-/]\d{2})?)"', s): c[d.replace("/", "-")] += 1
    if not c: return None
    full = [d for d in c if len(d) == 10]
    d = max(full, key=lambda x: c[x]) if full else max(c, key=c.get)
    return d.replace("-", "/")

for v in man["volumes"]:
    vid = v["id"]; p = f"docs/{vid}/index.html"; s = open(p, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    title = re.sub(r"\s*\|\s*Jamming Physics\s*$", "", t).strip()
    date = volume_date(vid)
    if not date: missing_date.append(vid)
    url = "https://jamming-physics.org" + v["hub"]
    tags = [("citation_title", title), ("citation_author", AUTHOR)]
    if date: tags.append(("citation_publication_date", date))
    tags += [("citation_doi", v["doi"]), ("citation_abstract_html_url", url), ("citation_language", "en")]
    block = "<!--vp-cite-start-->\n" + "\n".join(f'<meta name="{k}" content="{val.replace(chr(34), "&quot;")}">' for k, val in tags) + "\n<!--vp-cite-end-->\n"
    n = s
    n = re.sub(r"<!--vp-cite-start-->.*?<!--vp-cite-end-->\n?", "", n, flags=re.S)
    n = re.sub(r'[ \t]*<meta name="citation_[a-z_]+"[^>]*>\n?', "", n)
    n = re.sub(r"[ \t]*(?:&lt;|<)!--\s*(?:Phase 7: Highwire[^>]*|citation_tags: Phase 7)\s*-->\n?", "", n)
    n = re.sub(r"(?:&lt;)!--\s*(vp-series-jsonld[^>]*)-->", r"<!-- \1-->", n)          # un-escape the visible series marker
    n = re.sub(r"\n{3,}", "\n\n", n) if n != s else n
    n = n.replace("</head>", block + "</head>", 1)
    if n != s:
        changed.append(vid)
        if not check: open(p, "w", encoding="utf-8").write(n)
print(f"[citation] hubs {'needing change' if check else 'updated'}: {len(changed)}/{len(man['volumes'])}")
print(f"[citation] no date found on the volume's own pages (date left out): {missing_date}")
sys.exit(1 if (check and changed) else 0)
