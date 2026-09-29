#!/usr/bin/env python3
"""Build one Zenodo package ZIP per volume for a release.

  python3 tools/build_release.py 2026-09-29 [volume ...]

Each ZIP holds docs/<id>/ (published pages), repro/<id>/ (code and data), DESCRIPTION.md
(release/<tag>/descriptions/<id>.md), LEDGER.json (this volume's claims-ledger rows),
CORPUS_GUIDE.md (AGENTS.md) and MANIFEST.sha256. ZIPs are deterministic (sorted entries,
fixed timestamp) and go to release/<tag>/zips/ (not committed); CHECKSUMS.txt is committed.
"""
import hashlib, json, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"__pycache__", "_build", ".pytest_cache"}
STAMP = (2026, 1, 1, 0, 0, 0)


def files_under(base):
    out = []
    for d, dirs, fs in os.walk(os.path.join(ROOT, base)):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(fs):
            if f.endswith((".pyc", ".pyo")):
                continue
            out.append(os.path.relpath(os.path.join(d, f), ROOT))
    return out


def add(z, arc, data):
    zi = zipfile.ZipInfo(arc, STAMP)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    z.writestr(zi, data)


def main():
    tag = sys.argv[1]
    man = json.load(open(os.path.join(ROOT, "registry", "vp.manifest.json"), encoding="utf-8"))
    rows = json.load(open(os.path.join(ROOT, "registry", "claims_ledger.json"), encoding="utf-8"))["rows"]
    want = sys.argv[2:] or [v["id"] for v in man["volumes"]]
    rel = os.path.join(ROOT, "release", tag)
    os.makedirs(os.path.join(rel, "zips"), exist_ok=True)
    sums = []
    for v in man["volumes"]:
        vid = v["id"]
        if vid not in want:
            continue
        desc = os.path.join(rel, "descriptions", f"{vid}.md")
        if not os.path.isfile(desc):
            sys.exit(f"missing description: {desc}")
        entries = {}
        for p in files_under(f"docs/{vid}") + files_under(f"repro/{vid}"):
            entries[p] = open(os.path.join(ROOT, p), "rb").read()
        entries["DESCRIPTION.md"] = open(desc, "rb").read()
        entries["LEDGER.json"] = json.dumps([r for r in rows if r["volume"] == vid], indent=1, ensure_ascii=False).encode()
        entries["CORPUS_GUIDE.md"] = open(os.path.join(ROOT, "AGENTS.md"), "rb").read()
        mf = "".join(f"{hashlib.sha256(b).hexdigest()}  {p}\n" for p, b in sorted(entries.items()))
        entries["MANIFEST.sha256"] = mf.encode()
        name = f"{vid}_{tag}.zip"
        path = os.path.join(rel, "zips", name)
        with zipfile.ZipFile(path, "w") as z:
            for p in sorted(entries):
                add(z, f"{vid}_{tag}/{p}", entries[p])
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        sums.append(f"{h}  {name}  {os.path.getsize(path)} bytes  {len(entries)} files")
        print(sums[-1])
    if len(want) == len(man["volumes"]):
        open(os.path.join(rel, "CHECKSUMS.txt"), "w").write("\n".join(sums) + "\n")


if __name__ == "__main__":
    main()
