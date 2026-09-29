#!/usr/bin/env python3
"""Build docs/claims-ledger/index.html from registry/claims_ledger.json.
Regenerate, never hand-edit the page. Also ensures the page is listed in docs/sitemap.xml."""
import json, os, html, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "registry", "claims_ledger.json")
OUT = os.path.join(ROOT, "docs", "claims-ledger", "index.html")
SITEMAP = os.path.join(ROOT, "docs", "sitemap.xml")
URL = "https://jamming-physics.org/claims-ledger/"
ORDER = json.load(open(os.path.join(ROOT, "registry", "vp.manifest.json")))["volumes"]
CLASSES = [
    ("independent-prediction", "computed by repo code from inputs that do not contain the compared value, then compared with an external observation"),
    ("anchor-restatement", "the output equals, or is set by, an input, anchor or calibration chosen from the compared value"),
    ("identity", "holds by algebra or by construction"),
    ("interpretation", "a mapping of observed facts onto VP, with no numeric test"),
    ("open", "stated [O], or no code or data in the repository reproduces it"),
]
e = lambda s: html.escape("" if s is None else str(s))


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    rows = d["rows"]
    cnt = collections.Counter(r["class"] for r in rows)
    byvol = collections.defaultdict(list)
    for r in rows:
        byvol[r["volume"]].append(r)
    disc = [r for r in rows if r.get("discriminating")]
    p = []
    p.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claims Ledger | Jamming Physics</title>
<meta name="description" content="Every headline and central claim of the 32 VP volumes, classed by what the repository evidence shows: independent prediction, anchor restatement, identity, interpretation or open.">
<link rel="canonical" href="{URL}">
<style>
:root{{--ink:#1c1d21;--mut:#5b5e66;--bg:#fff;--line:#e6e6ea;--ac:#0a5a8a}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--ink:#e4e4e8;--mut:#a0a3ab;--bg:#15161a;--line:#2e3038;--ac:#6fb3e0}}}}
:root[data-theme="dark"]{{--ink:#e4e4e8;--mut:#a0a3ab;--bg:#15161a;--line:#2e3038;--ac:#6fb3e0}}
*{{box-sizing:border-box}}body{{margin:0;color:var(--ink);background:var(--bg);font:16px/1.6 Georgia,'Times New Roman',serif}}
main{{max-width:980px;margin:0 auto;padding:0 16px 64px}}
.crumb{{max-width:980px;margin:0 auto;padding:10px 16px;font:14px/1.4 system-ui,sans-serif;color:var(--mut)}}
a{{color:var(--ac);text-decoration:none}}a:hover{{text-decoration:underline}}
h1{{font-size:1.7em;margin:.6em 0 .2em}}h2{{font-size:1.18em;margin:1.8em 0 .5em;padding-bottom:.2em;border-bottom:1px solid var(--line)}}
.tw{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font:13.5px/1.45 system-ui,sans-serif}}
th,td{{border-bottom:1px solid var(--line);padding:.35em .45em;text-align:left;vertical-align:top}}th{{color:var(--mut);font-weight:600}}
.c{{white-space:nowrap;font-weight:600}}.num{{text-align:right}}
.lead{{border-left:3px solid var(--ac);padding:.3em 0 .3em .8em;margin:1em 0}}
</style>
</head>
<body>
<nav class="crumb"><a href="/">Jamming Physics</a> › Claims ledger</nav>
<main>
<h1>Claims ledger</h1>
<p class="lead">This page lists every headline and central claim of the 32 volumes. Each claim is classed by what the evidence in this repository actually shows, not by the grade printed on its page. Internal coherence is not evidence. The claims that can decide the framework are the independent predictions and the discriminating tests. Generated from <code>registry/claims_ledger.json</code> ({len(rows)} rows, built {e(d.get('built'))}).</p>
<h2>Classes</h2><div class="tw"><table><tr><th>class</th><th class="num">rows</th><th>meaning</th></tr>""")
    for c, m in CLASSES:
        p.append(f"<tr><td class=c>{c}</td><td class=num>{cnt.get(c,0)}</td><td>{e(m)}</td></tr>")
    p.append("</table></div>")
    p.append(f"<h2>Discriminating tests ({len(disc)})</h2><p>These are tests where VP and standard science predict different outcomes and the test can be run. None has been run on data yet.</p><div class=tw><table><tr><th>volume</th><th>claim</th><th>test</th></tr>")
    for r in disc:
        p.append(f"<tr><td>{e(r['volume'])}</td><td>{e(r['claim'])}</td><td>{e(r.get('test'))}</td></tr>")
    p.append("</table></div>")
    for v in ORDER:
        rs = byvol.get(v["id"], [])
        if not rs:
            continue
        p.append(f"<h2 id=\"{e(v['id'])}\"><a href=\"{e(v['hub'])}\">{e(v.get('short', v['id']))}</a></h2><div class=tw><table><tr><th>claim</th><th>class</th><th>residual / result</th><th>evidence</th></tr>")
        for r in rs:
            p.append(f"<tr><td>{e(r['claim'])}</td><td class=c>{e(r['class'])}</td><td>{e(r.get('residual'))}</td><td>{e(r.get('evidence'))}</td></tr>")
        p.append("</table></div>")
    p.append("</main>\n</body>\n</html>\n")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(p))
    sm = open(SITEMAP, encoding="utf-8").read()
    if URL not in sm:
        today = datetime.date.today().isoformat()
        sm = sm.replace("</urlset>", f"  <url><loc>{URL}</loc><lastmod>{today}</lastmod><priority>0.9</priority></url>\n</urlset>")
        open(SITEMAP, "w", encoding="utf-8").write(sm)
    print(f"[ledger] {len(rows)} rows, {len(disc)} discriminating -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
