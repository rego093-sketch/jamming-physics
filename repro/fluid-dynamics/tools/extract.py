#!/usr/bin/env python3
# tools/extract.py — VP-SPEC v1.8 Constitution C2 on-demand extractor.
# The canonical material is docs/ HTML; TeX body source is NOT bundled. When a
# human needs text/LaTeX, it is produced *from the canonical HTML* here:
#   - equation LaTeX  <- the img alt of each rendered SVG (accessibility meta)
#   - prose text      <- the body, tags stripped
# Output is plain markdown. Also used to assemble docs/llms-full.txt.
#
# Usage:
#   python3 tools/extract.py --paper fluid-dynamics            # all sections -> stdout
#   python3 tools/extract.py --paper fluid-dynamics --slug 06-...   # one section
import re, os, csv, glob, argparse

def manifest(root,p):
    return list(csv.DictReader(open(f"{root}/manifest/{p}.csv",encoding="utf-8")))

def main_block(h):
    m=re.search(r"<main>(.*)</main>",h,re.S); return m.group(1) if m else h

def to_markdown(h):
    t=main_block(h)
    t=re.sub(r'<aside class="claim-strip".*?</aside>',"",t,flags=re.S)
    # display equations -> $$ LaTeX $$ (from the SVG img alt = canonical accessibility meta)
    t=re.sub(r'<figure class="eq">\s*<img[^>]*?alt="([^"]*)"[^>]*>\s*</figure>',
             lambda m:"\n\n$$ "+m.group(1).strip()+" $$\n\n", t, flags=re.S)
    # inline equation images -> $LaTeX$
    t=re.sub(r'<img class="eqi"[^>]*?alt="([^"]*)"[^>]*>', lambda m:" $"+m.group(1).strip()+"$ ", t)
    t=re.sub(r"<h1>(.*?)</h1>", lambda m:"# "+_clean(m.group(1)), t, flags=re.S)
    t=re.sub(r"<h2>(.*?)</h2>", lambda m:"\n## "+_clean(m.group(1)), t, flags=re.S)
    t=re.sub(r"<h3>(.*?)</h3>", lambda m:"\n### "+_clean(m.group(1)), t, flags=re.S)
    t=re.sub(r"<h4>(.*?)</h4>", lambda m:"\n#### "+_clean(m.group(1)), t, flags=re.S)
    t=re.sub(r'<p class="answer">(.*?)</p>', lambda m:"\n> **Answer.** "+_clean(m.group(1))+"\n", t, flags=re.S)
    t=re.sub(r'<p class="abstract">(.*?)</p>', lambda m:"\n*Abstract.* "+_clean(m.group(1))+"\n", t, flags=re.S)
    t=re.sub(r"<[^>]+>"," ",t)
    t=re.sub(r"[ \t]+"," ",t)
    t=re.sub(r"\n{3,}","\n\n",t)
    return t.strip()

def _clean(s):
    s=re.sub(r"<[^>]+>"," ",s); return re.sub(r"\s+"," ",s).strip()

def section_md(root,p,slug):
    f=f"{root}/docs/{p}/{slug}/index.html"
    if not os.path.exists(f): return ""
    return to_markdown(open(f,encoding="utf-8").read())

def run(root,p,slug):
    if slug:
        print(section_md(root,p,slug)); return
    out=[]
    for r in manifest(root,p):
        md=section_md(root,p,r["slug"])
        if md: out.append(md)
    print("\n\n---\n\n".join(out))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--paper",required=True); ap.add_argument("--root",default="."); ap.add_argument("--slug",default=None)
    a=ap.parse_args(); run(a.root,a.paper,a.slug)
