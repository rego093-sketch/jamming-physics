#!/usr/bin/env python3
"""Print each volume's HTML pages to one PDF per volume (release deliverable).

  python3 tools/build_pdfs.py 2026-09-29 [volume ...]

Serves docs/ on localhost, prints every page with headless Chromium (standard quality),
and merges them with pypdf in reading order: the hub first, then pages in the order the hub
links them, then any remaining pages by path. One bookmark per page. disease_kit is written at
low quality: all page bodies joined into one HTML and printed once (fonts embedded once). Per-page PDFs are cached in release/<tag>/pdfs/_pages/.
Output: release/<tag>/pdfs/<id>_<tag>.pdf (not committed).
"""
import concurrent.futures as cf, functools, http.server, os, re, subprocess, sys, threading
from pypdf import PdfWriter, PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
PORT = 8765
LOW_QUALITY = {"disease_kit"}


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Quiet, directory=DOCS)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def pages_in_order(vid):
    base = os.path.join(DOCS, vid)
    allp = sorted(os.path.relpath(os.path.join(d, "index.html"), DOCS)
                  for d, _, fs in os.walk(base) if "index.html" in fs)
    hub = f"{vid}/index.html"
    order, seen = [hub], {hub}
    for href in re.findall(r'href="([^"#?]+)', open(os.path.join(DOCS, hub), encoding="utf-8").read()):
        if href.startswith(("http", "mailto:")):
            continue
        path = os.path.normpath(href.lstrip("/") if href.startswith("/") else os.path.join(vid, href))
        cand = path if path.endswith(".html") else os.path.join(path, "index.html")
        if cand in allp and cand not in seen:
            order.append(cand); seen.add(cand)
    return order + [p for p in allp if p not in seen]


def print_page(rel, out):
    if os.path.isfile(out) and os.path.getsize(out) > 0:
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    url = f"http://127.0.0.1:{PORT}/{rel[:-len('index.html')]}"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=4000", f"--print-to-pdf={out}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    return out


def print_combined(vid, order, out):
    """Low-quality path: join every page's <main> into one HTML with the volume CSS inlined and
    print once, so fonts are embedded once instead of once per page."""
    # plain print styling: no card borders or backgrounds (those are drawn as vector paths and
    # make the file several times larger); text, headings and tables only
    css = ("@page{margin:10mm}body{font:8.5pt/1.3 serif;color:#000;column-count:2;column-gap:6mm}"
           "section{break-before:column}"
           "h1{font-size:14pt}h2{font-size:12pt}"
           "h3,h4{font-size:10.5pt}*{background:none!important;border-radius:0!important;box-shadow:none!important}"
           "div,section,aside{border:0!important;padding:0!important;margin:.2em 0!important}"
           "table{border-collapse:collapse}*{border:0!important;outline:0!important}td,th{padding:1pt 4pt 1pt 0!important}"
           "nav,header,footer,.crumb{display:none}img,svg{max-width:100%}")
    parts = []
    for rel in order:
        h = open(os.path.join(DOCS, rel), encoding="utf-8").read()
        m = re.search(r"<main[^>]*>(.*?)</main>", h, re.S) or re.search(r"<body[^>]*>(.*?)</body>", h, re.S)
        body = re.sub(r"<script.*?</script>", "", m.group(1) if m else "", flags=re.S)
        body = re.sub(r'(src|href)="/', rf'\1="http://127.0.0.1:{PORT}/', body)
        parts.append(f'<section>{body}</section>')
    src = out[:-4] + ".html"
    os.makedirs(os.path.dirname(src), exist_ok=True)
    open(src, "w", encoding="utf-8").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(parts)}</body></html>')
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--disable-pdf-tagging", f"--print-to-pdf={out}", "file://" + src],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    return out


def title_of(rel):
    m = re.search(r"<title>(.*?)</title>", open(os.path.join(DOCS, rel), encoding="utf-8").read(), re.S)
    t = re.sub(r"\s+", " ", m.group(1)).strip() if m else rel
    return re.sub(r"&amp;", "&", t.split(" | ")[0])


def main():
    tag = sys.argv[1]
    import json
    vols = [v["id"] for v in json.load(open(os.path.join(ROOT, "registry", "vp.manifest.json")))["volumes"]]
    want = sys.argv[2:] or vols
    outdir = os.path.join(ROOT, "release", tag, "pdfs")
    srv = serve()
    for vid in [v for v in vols if v in want]:
        order = pages_in_order(vid)
        if vid in LOW_QUALITY:
            out = os.path.join(outdir, f"{vid}_{tag}.pdf")
            tmp = print_combined(vid, order, os.path.join(outdir, "_pages", f"{vid}_combined.pdf"))
            w = PdfWriter(clone_from=tmp)
            for pg in w.pages:
                pg.compress_content_streams()
            w.add_metadata({"/Title": f"{vid} — Jamming Physics ({tag})", "/Author": "Young Jae Lee",
                            "/CreationDate": "D:20260929000000Z", "/ModDate": "D:20260929000000Z"})
            with open(out, "wb") as f:
                w.write(f)
            print(f"{vid}: {len(order)} html pages -> {len(w.pages)} pdf pages (combined, low quality), {os.path.getsize(out)/1048576:.1f} MB")
            continue
        cache = [os.path.join(outdir, "_pages", vid, p.replace("/", "__") + ".pdf") for p in order]
        with cf.ThreadPoolExecutor(6) as ex:
            list(ex.map(print_page, order, cache))
        w = PdfWriter()
        for rel, pdf in zip(order, cache):
            if not os.path.isfile(pdf) or os.path.getsize(pdf) == 0:
                print(f"  [skip] {rel}: no output"); continue
            start = len(w.pages)
            w.append(PdfReader(pdf))
            w.add_outline_item(title_of(rel), start)
        for pg in w.pages:
            pg.compress_content_streams()
        w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        w.add_metadata({"/Title": f"{vid} — Jamming Physics ({tag})", "/Author": "Young Jae Lee",
                        "/CreationDate": "D:20260929000000Z", "/ModDate": "D:20260929000000Z"})
        out = os.path.join(outdir, f"{vid}_{tag}.pdf")
        with open(out, "wb") as f:
            w.write(f)
        print(f"{vid}: {len(order)} html pages -> {len(w.pages)} pdf pages, {os.path.getsize(out)/1048576:.1f} MB")
    srv.shutdown()


if __name__ == "__main__":
    main()
