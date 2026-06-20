#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
repro_manifest.py  --  file-level reproducibility manifest.

Inherited technology (from analgesic_threshold_logic v2.0): a SHA256 fingerprint of the WHOLE
delivered package, not just the engine output. Any silent byte-drift in a shipped file is caught.

  freeze()  -- walk the canonical source tree, write manifest/SHA256SUMS.txt (sorted, 2-space format
               compatible with `sha256sum -c`).
  verify()  -- recompute every hash and report matched / changed / missing / extra. Fail-closed:
               an empty or absent manifest is a FAIL, never a silent pass.

Scope. The freeze covers code (repro/, tools/), the canonical site (docs/), inherited assets
(inherited/), the content manifest (manifest/cardioresp_vp_site.csv), and every governance document
at the package root. It EXCLUDES runtime outputs (reports/), the manifest file itself, and bytecode
caches. Report determinism is proven separately by the drift-0 gate, so excluding reports/ from the
frozen set keeps the manifest stable while losing no reproducibility guarantee.
"""
import os, hashlib, json, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.abspath(os.path.join(_HERE, "..", ".."))
_MANIFEST = os.path.join(_PKG, "manifest", "SHA256SUMS.txt")

_EXCLUDE_DIRS  = {"reports", "zenodo", "__pycache__", ".git", ".ipynb_checkpoints"}
_EXCLUDE_EXT   = {".pyc", ".pyo"}
_EXCLUDE_RELS  = {os.path.relpath(_MANIFEST, _PKG).replace(os.sep, "/")}


def _iter_files():
    for root, dirs, files in os.walk(_PKG):
        dirs[:] = [d for d in dirs if d not in _EXCLUDE_DIRS]
        for fn in sorted(files):
            ap = os.path.join(root, fn)
            rp = os.path.relpath(ap, _PKG).replace(os.sep, "/")
            if rp in _EXCLUDE_RELS:
                continue
            if os.path.splitext(fn)[1] in _EXCLUDE_EXT:
                continue
            yield rp, ap


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def compute():
    return {rp: _sha256(ap) for rp, ap in _iter_files()}


def freeze():
    m = compute()
    lines = ["%s  %s" % (m[rp], rp) for rp in sorted(m)]
    os.makedirs(os.path.dirname(_MANIFEST), exist_ok=True)
    with open(_MANIFEST, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)


def _read_manifest():
    out = {}
    if not os.path.exists(_MANIFEST):
        return out
    for ln in open(_MANIFEST, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln:
            continue
        digest, _, rp = ln.partition("  ")
        if rp:
            out[rp] = digest
    return out


def verify():
    recorded = _read_manifest()
    current  = compute()
    changed = sorted(rp for rp in recorded if rp in current and recorded[rp] != current[rp])
    missing = sorted(rp for rp in recorded if rp not in current)
    extra   = sorted(rp for rp in current if rp not in recorded)
    ok = bool(recorded) and not changed and not missing and not extra
    return {"ok": ok, "n_recorded": len(recorded), "n_current": len(current),
            "changed": changed, "missing": missing, "extra": extra}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "freeze":
        print("froze %d entries -> manifest/SHA256SUMS.txt" % freeze())
    else:
        print(json.dumps(verify(), ensure_ascii=False, indent=2))
