#!/usr/bin/env python3
"""
extract.py — VP_SPEC v1.8 Constitution C2 on-demand extractor.

The single canonical form is the HTML under docs/cosmology/. TeX/text SSOT is NOT
bundled in the distribution; when text or LaTeX is needed it is regenerated from
the canonical HTML on demand by this tool. Equations live as SVG <img> whose alt
attribute carries the full LaTeX (the accessibility-metadata SSOT).

Usage:
  python3 tools/extract.py <slug> [--out DIR]     one chapter
  python3 tools/extract.py --all   [--out DIR]     every chapter

For each chapter it writes, under DIR (default ./_extract, which is gitignored
and never published):
  <slug>.txt   clean prose, equations replaced by [EQ:<id>] placeholders
  <slug>.tex   ordered LaTeX of every equation, keyed by data-eq id
"""
import re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
COS = ROOT / "docs" / "cosmology"


def slugs():
    import json
    m = json.load(open(COS / "_meta.json", encoding="utf-8"))
    return [c["slug"] for c in m["chapters"]]


def extract_one(slug, outdir):
    p = COS / slug / "index.html"
    if not p.exists():
        print(f"  skip (missing): {slug}")
        return
    t = p.read_text(encoding="utf-8")
    body = re.search(r"<main>(.*?)</main>", t, re.S)
    body = body.group(1) if body else t

    # collect equations (data-eq id + alt LaTeX), replace each img with a marker
    eqs = []

    def repl(m):
        tag = m.group(0)
        eid = (re.search(r'data-eq="([^"]+)"', tag) or [None, f"eq{len(eqs)}"])[1]
        alt = (re.search(r'alt="(.*?)"', tag, re.S) or [None, ""])[1]
        eqs.append((eid, html.unescape(alt)))
        return f" [EQ:{eid}] "

    body = re.sub(r"<img\b[^>]*>", repl, body, flags=re.S)

    # drop non-prose furniture, then strip remaining tags
    for pat in (r"<script.*?</script>", r"<style.*?</style>",
                r"<nav\b.*?</nav>", r"<aside\b.*?</aside>",
                r"<figure\b.*?</figure>", r"<table\b.*?</table>"):
        body = re.sub(pat, " ", body, flags=re.S)
    text = re.sub(r"(?s)<[^>]+>", " ", body)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{slug}.txt").write_text(text + "\n", encoding="utf-8")

    tex = [f"% {slug} — extracted from canonical HTML (VP_SPEC v1.8 C2)\n"]
    for eid, latex in eqs:
        tex.append(f"% {eid}\n{latex}\n")
    (outdir / f"{slug}.tex").write_text("\n".join(tex), encoding="utf-8")
    return len(eqs), len(text)


def main(argv):
    out = pathlib.Path("_extract")
    if "--out" in argv:
        i = argv.index("--out")
        out = pathlib.Path(argv[i + 1])
        del argv[i:i + 2]
    out = (ROOT / out) if not out.is_absolute() else out

    targets = slugs() if "--all" in argv else [a for a in argv[1:] if not a.startswith("-")]
    if not targets:
        print(__doc__)
        return 2
    total_eq = 0
    for s in targets:
        r = extract_one(s, out)
        if r:
            total_eq += r[0]
            print(f"  {s}: {r[0]} eq, {r[1]} chars -> {out.name}/{s}.{{txt,tex}}")
    print(f"done: {len(targets)} chapter(s), {total_eq} equations extracted into {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
