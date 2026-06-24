#!/usr/bin/env python3
"""VP-SPEC v1.9 6-M.3 — normalize every vp-card's dictionary link (authoritative).

For each `aside.vp-card`, the dictionary link is made to AGREE with data-locked:
strip any existing data-concept attr + /concepts link, then — if data-locked
resolves (via the concept aka map) to a canonical dictionary term — add exactly
`data-concept="{id}"` + one `/concepts/#{id}` link. Volume-local quantities,
untagged cards, and data-locked="true" end up with no dictionary link.
Idempotent and self-correcting (fixes stale/wrong/duplicate tags).
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DC_ATTR = re.compile(r'\s*data-concept="[^"]*"')
DC_LINK = re.compile(r'\s*·?\s*<a href="/concepts/#[^"]*">[^<]*</a>')
CARD = re.compile(r'<aside class="vp-card"([^>]*)>(.*?)</aside>', re.S)


def main():
    concepts = json.load(open(os.path.join(ROOT, "registry/concepts.json"), encoding="utf-8"))
    aka2id = {}
    for e in concepts["entries"]:
        for k in [e["id"]] + e.get("aka", []):
            aka2id[k] = e["id"]
    stats = {"cards": 0, "linked": 0, "fixed": 0, "files": 0}

    def repl(m):
        stats["cards"] += 1
        attrs, content = m.group(1), m.group(2)
        clean_a = DC_ATTR.sub("", attrs)
        clean_c = DC_LINK.sub("", content)
        dl = re.search(r'data-locked="([^"]+)"', attrs)
        resolves = dl and dl.group(1) != "true" and dl.group(1) in aka2id
        if resolves:
            cid = aka2id[dl.group(1)]
            new_a = clean_a + f' data-concept="{cid}"'
            new_c = clean_c.rstrip() + f' · <a href="/concepts/#{cid}">용어</a>'
        else:
            new_a, new_c = clean_a, clean_c
        out = f'<aside class="vp-card"{new_a}>{new_c}</aside>'
        if out != m.group(0):
            stats["fixed"] += 1
            if resolves and "data-concept=" not in attrs:
                stats["linked"] += 1
        return out

    for f in glob.glob(os.path.join(ROOT, "docs/**/index.html"), recursive=True):
        html = open(f, encoding="utf-8", errors="ignore").read()
        new = CARD.sub(repl, html)
        if new != html:
            open(f, "w", encoding="utf-8").write(new)
            stats["files"] += 1
    print(f"scanned {stats['cards']} vp-cards; normalized {stats['fixed']} "
          f"(new links {stats['linked']}) across {stats['files']} files")


if __name__ == "__main__":
    main()
