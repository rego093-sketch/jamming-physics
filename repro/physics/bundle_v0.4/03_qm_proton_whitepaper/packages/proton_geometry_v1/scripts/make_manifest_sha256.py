#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/make_manifest_sha256.py

Generate MANIFEST.sha256 at the bundle root with SHA-256 hashes
for all files except the manifest itself.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

EXCLUDE = {"MANIFEST.sha256"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(".").resolve()
    files = sorted(
        [
            p
            for p in root.rglob("*")
            if p.is_file() and p.name not in EXCLUDE
        ]
    )
    lines = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")
    (root / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote MANIFEST.sha256 with", len(files), "files")


if __name__ == "__main__":
    main()
