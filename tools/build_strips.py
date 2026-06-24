#!/usr/bin/env python3
"""VP-SPEC v1.9 6-M.2 — inject the inherits-strip into every volume hub.

Reads docs/{paper_id}/_decl.json.inherits_modules and writes an
`aside.inherits-strip` (links to /modules/#id) right after the hub's
claim-strip (or after <h1> if none). Idempotent: re-running is a no-op.
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABEL = {  # short strip labels (full names live in modules.json)
    "kernel": "R19 switch",
    "light_emergence": "Quantum light",
    "dna_interpretation": "DNA interpretation",
    "rotor_inflow": "Rotor inflow",
}


def _links(mods):
    return "".join(f'<a href="/modules/#{m}">{LABEL.get(m, m)}</a>' for m in mods)


def strip_html(owns, inherits):
    seg = ""
    if owns:
        seg += f'<span class="lbl">Defines:</span>{_links(owns)}'
    if inherits:
        seg += f'<span class="lbl">Inherits:</span>{_links(inherits)}'
    return (f'<aside class="inherits-strip" aria-label="Common-module provenance">{seg}</aside>')


def main():
    n_done = 0
    for decl_path in sorted(glob.glob(os.path.join(ROOT, "docs/*/_decl.json"))):
        pid = os.path.basename(os.path.dirname(decl_path))
        hub = os.path.join(ROOT, f"docs/{pid}/index.html")
        if not os.path.isfile(hub):
            continue
        html = open(hub, encoding="utf-8").read()
        # remove any existing strip so content always reflects the current _decl
        html = re.sub(r'<aside class="inherits-strip".*?</aside>\n?', "", html, flags=re.S)
        d = json.load(open(decl_path, encoding="utf-8"))
        strip = strip_html(d.get("owns_modules", []), d.get("inherits_modules", []))
        # prefer: right after the claim-strip aside
        new, k = re.subn(r'(<aside class="claim-strip[^>]*>.*?</aside>)',
                         r"\1\n" + strip, html, count=1, flags=re.S)
        if k == 0:  # fallback: right after the first </h1>
            new, k = re.subn(r"(</h1>)", r"\1\n" + strip, html, count=1)
        if k == 0:
            print(f"WARN no anchor in {pid} hub — skipped")
            continue
        open(hub, "w", encoding="utf-8").write(new)
        n_done += 1
    print(f"inherits-strip: (re)written on {n_done} hubs")


if __name__ == "__main__":
    main()
