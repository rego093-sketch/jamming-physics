\
"""
make_manifest.py

Create a SHA256 manifest for all files in the bundle (for DOI archival reproducibility).

Usage:
    python code/make_manifest.py

Output:
    manifest_sha256.txt  (at repo root)

Rules:
- Excludes the manifest file itself.
- Excludes __pycache__ and typical temporary files.

No external dependencies.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


EXCLUDE_NAMES = {
    "manifest_sha256.txt",
}
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
}


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> None:
    here = Path(__file__).resolve()
    root = here.parent.parent

    files = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if p.name in EXCLUDE_NAMES:
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        # avoid hidden OS junk
        if p.name.startswith(".DS_Store"):
            continue
        files.append(p)

    files.sort(key=lambda x: str(x.relative_to(root)).lower())

    out_lines = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        out_lines.append(f"{sha256_file(p)}  {rel}")

    out_path = root / "manifest_sha256.txt"
    out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} with {len(out_lines)} entries.")


if __name__ == "__main__":
    main()
