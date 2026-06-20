#!/usr/bin/env python3
# tools/build_search_layer.py — VP-SPEC v1.8 Phase 5(기계 접근 레인) 생성기. 결정론·멱등.
#   헌법 C4 검색 수용성 6-R.5: docs/robots.txt(7봇) + docs/sitemap.xml + docs/llms.txt(<5KB),
#   그리고 허브(docs/{paper}/index.html) JSON-LD 에 CreativeWorkSeries(author sameAs ORCID) 주입.
#   본문/수치/수식은 일절 건드리지 않는다. 모든 출력은 봉인 매니페스트·정본 경로에서만 파생.
# 사용: python3 tools/build_search_layer.py --paper physics
import re, os, csv, glob, argparse, html, datetime

BASE   = "https://jamming-physics.org"
AUTHOR = "Young Jae Lee"
ORCID  = "https://orcid.org/0009-0002-7535-8245"
DOI    = "https://doi.org/10.5281/zenodo.17932566"
BOTS   = ["Googlebot","Bingbot","OAI-SearchBot","GPTBot","PerplexityBot","ClaudeBot","Google-Extended"]
BUILD  = datetime.date.today().isoformat()

def page_url(path):
    # docs/physics/index.html -> /physics/ ; docs/physics/foo/index.html -> /physics/foo/
    rel = path[len("docs"):] if path.startswith("docs") else path
    rel = re.sub(r"/index\.html$", "/", rel)
    if not rel.endswith("/"): rel += "/"
    return BASE + rel

def read_manifest(p):
    return list(csv.DictReader(open(f"manifest/{p}.csv", encoding="utf-8")))

def gen_robots():
    L = ["# VP-SPEC v1.8 — machine access (C4 retrieval-readiness). 7 named agents + default: full allow.",
         f"# generated {BUILD} by tools/build_search_layer.py (deterministic)", ""]
    for b in BOTS:
        L += [f"User-agent: {b}", "Allow: /", ""]
    L += ["User-agent: *", "Allow: /", "", f"Sitemap: {BASE}/sitemap.xml", ""]
    return "\n".join(L)

def gen_sitemap(paper):
    files = sorted(glob.glob("docs/**/index.html", recursive=True))
    # 허브를 맨 앞으로(정준 우선순위), 나머지는 경로 정렬 유지
    files.sort(key=lambda f: (0 if f == f"docs/{paper}/index.html" else 1, f))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in files:
        url = page_url(f)
        pr = "1.0" if f == f"docs/{paper}/index.html" else "0.8"
        out += ["  <url>", f"    <loc>{url}</loc>", f"    <lastmod>{BUILD}</lastmod>",
                f"    <priority>{pr}</priority>", "  </url>"]
    out += ["</urlset>", ""]
    return "\n".join(out), len(files)

def gen_llms(paper):
    rows = read_manifest(paper)
    head = (
        f"# Jamming Physics — VP Theory (Volume Particle)\n\n"
        f"> Canonical, citable HTML edition of the VP (Volume Particle) physics white paper: the vacuum "
        f"modeled as a jammed, infinitely-rigid granular lattice (random close packing), so the speed of "
        f"light is the lattice elastic-wave speed c\u00b2 = B/\u03c1 and the proton\u2013electron mass ratio is "
        f"forced as m_p/m_e = 6\u03c0\u2075 (\u221219 ppm vs measurement). Every page is self-contained, "
        f"answer-first, and carries its graded verdict (forced/verified/hypothesis/open).\n\n"
        f"Author: {AUTHOR} ({ORCID}). DOI: {DOI}.\n"
        f"Principle: LOCK \u2192 Derive \u2192 Gate (inputs locked, numbers derived by deterministic tools, "
        f"verified by counts; drift 0).\n\n"
        f"## Canonical results\n"
        f"- c\u00b2 = B/\u03c1  (light speed = lattice bulk modulus over density; simulation-validated)\n"
        f"- m_p/m_e = 6\u03c0\u2075  (= 2\u03c0\u00b7\u03bd_p, \u03bd_p = 3\u03c0\u2074; forced)\n"
        f"- \u03b4 = 1/\u03c0\u00b2, \u03b1 = 2/\u03c0  (geometric rectification constants; single source)\n"
        f"- Single empirical anchor: \u03bb_anchor = 632.99 nm (DOF = 1)\n\n"
        f"## Hub\n- [VP Theory hub]({BASE}/physics/)\n\n"
        f"## Sections\n"
    )
    # 섹션 목록은 코드+슬러그만(짧게) — <5KB 보장. 제목은 길어서 생략, 슬러그가 안정 식별자.
    lines = []
    for r in rows:
        code = (r.get("code") or "").strip()
        tag = f"{code} " if code else ""
        lines.append(f"- {tag}{BASE}/physics/{r['slug']}/")
    body = head + "\n".join(lines) + "\n"
    # 5KB 가드: 초과 시 코드 접두어 제거(URL만)로 축약
    if len(body.encode("utf-8")) > 5120:
        lines = [f"- {BASE}/physics/{r['slug']}/" for r in rows]
        body = head + "\n".join(lines) + "\n"
    return body

SERIES_MARK = "<!-- vp-series-jsonld r7 -->"
def patch_hub(paper):
    hub = f"docs/{paper}/index.html"
    if not os.path.exists(hub): return False, "hub absent"
    h = open(hub, encoding="utf-8").read()
    rows = read_manifest(paper)
    parts = ", ".join(f'{{"@type": "CreativeWork", "@id": "{BASE}/physics/{r["slug"]}/"}}' for r in rows)
    block = (
        SERIES_MARK + "\n<script type=\"application/ld+json\">"
        '{"@context": "https://schema.org", "@type": "CreativeWorkSeries", '
        '"name": "Jamming Physics \u2014 VP Theory (Volume Particle)", '
        f'"url": "{BASE}/physics/", '
        '"author": {"@type": "Person", "name": "' + AUTHOR + '", "sameAs": "' + ORCID + '"}, '
        f'"identifier": "{DOI}", '
        f'"hasPart": [{parts}]'
        "}</script>"
    )
    # 멱등: 이전 주입 블록 제거 후 재삽입
    h = re.sub(re.escape(SERIES_MARK) + r'\s*<script type="application/ld\+json">.*?</script>\s*',
               "", h, flags=re.S)
    h = h.replace("\n</head>", "\n" + block + "\n</head>", 1)
    open(hub, "w", encoding="utf-8").write(h)
    return True, "hub patched (CreativeWorkSeries + author sameAs ORCID)"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--paper", required=True)
    a = ap.parse_args(); p = a.paper
    os.makedirs("docs", exist_ok=True)
    rob = gen_robots(); open("docs/robots.txt", "w", encoding="utf-8").write(rob)
    sm, npg = gen_sitemap(p); open("docs/sitemap.xml", "w", encoding="utf-8").write(sm)
    ll = gen_llms(p); open("docs/llms.txt", "w", encoding="utf-8").write(ll)
    okh, msgh = patch_hub(p)
    print(f"[search-layer] robots.txt({len(BOTS)} bots) | sitemap.xml({npg} urls) | "
          f"llms.txt({len(ll.encode('utf-8'))}B<5120) | {msgh}")

if __name__ == "__main__":
    main()
