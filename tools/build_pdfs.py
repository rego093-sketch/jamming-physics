#!/usr/bin/env python3
"""Print each volume's HTML pages to one PDF per volume (release deliverable).

  python3 tools/build_pdfs.py 2026-09-29 [volume ...]

Serves docs/ on localhost, prints every page with headless Chromium (standard quality),
and merges them with pypdf in reading order: the hub first, then pages in the order the hub
links them, then any remaining pages by path. One bookmark per page. disease_kit is written at
low quality (images recompressed). Per-page PDFs are cached in release/<tag>/pdfs/_pages/.
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
            if vid in LOW_QUALITY:
                for img in pg.images:
                    try:
                        img.replace(img.image, quality=35)
                    except Exception:
                        pass
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
