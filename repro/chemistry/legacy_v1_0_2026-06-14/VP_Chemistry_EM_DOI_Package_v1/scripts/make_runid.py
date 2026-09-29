# -*- coding: utf-8 -*-
"""
make_runid.py — deterministic SHA256SUMS.txt + RUNID.txt for the package.
RunID = sha256(code_hash + doc_hash + data_hash), each a sha256 over the sorted
per-file hashes of that class. Standard library only; run from the package root:
    python3 scripts/make_runid.py
"""
import hashlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE = {"SHA256SUMS.txt", "RUNID.txt"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def all_files():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in sorted(dn) if not d.startswith(".") and d != "__pycache__"]
        for f in sorted(fn):
            if f in EXCLUDE or f.startswith("."):
                continue
            full = os.path.join(dp, f)
            out.append((os.path.relpath(full, ROOT).replace(os.sep, "/"), full))
    return sorted(out)


def class_hash(pairs, pred):
    h = hashlib.sha256()
    for rel, full in pairs:
        if pred(rel):
            h.update((rel + ":" + sha256_file(full) + "\n").encode())
    return h.hexdigest()


def main():
    pairs = all_files()
    # SHA256SUMS.txt
    lines = [f"{sha256_file(full)}  {rel}" for rel, full in pairs]
    with open(os.path.join(ROOT, "SHA256SUMS.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")

    code_h = class_hash(pairs, lambda r: r.endswith(".py"))
    doc_h = class_hash(pairs, lambda r: r.startswith("whitepaper/") and not r.endswith(".py"))
    data_h = class_hash(pairs, lambda r: r.endswith(".csv"))
    runid = hashlib.sha256((code_h + doc_h + data_h).encode()).hexdigest()

    with open(os.path.join(ROOT, "RUNID.txt"), "w") as f:
        f.write("RunID (deterministic):\n  " + runid + "\n\n")
        f.write("Definition:\n  RunID = sha256(code_hash + doc_hash + data_hash)\n\n")
        f.write("Component hashes:\n")
        f.write(f"  code_hash: {code_h}   (*.py, {sum(1 for r,_ in pairs if r.endswith('.py'))} files)\n")
        f.write(f"  doc_hash:  {doc_h}   (whitepaper/)\n")
        f.write(f"  data_hash: {data_h}   (*.csv, {sum(1 for r,_ in pairs if r.endswith('.csv'))} files)\n\n")
        f.write(f"Files checksummed: {len(pairs)}\nGenerated 2026-06-14.\n")

    print(f"SHA256SUMS.txt: {len(pairs)} files")
    print(f"RUNID: {runid}")


if __name__ == "__main__":
    main()
