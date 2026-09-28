#!/usr/bin/env python3
"""Re-generate `00_metadata/MANIFEST.sha256` for the unified bundle.

This is an integrity list of all files (SHA-256) in the bundle, relative to
bundle root.

Policy:
- Exclude `00_metadata/MANIFEST.sha256` itself.
- Stable ordering by path.
- UTF-8 output.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

EXCLUDE = {"00_metadata/MANIFEST.sha256"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "00_metadata" / "MANIFEST.sha256"

    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel in EXCLUDE:
            continue
        files.append(rel)

    lines = []
    for rel in sorted(files):
        h = sha256_file(root / rel)
        lines.append(f"{h}  ./{rel}")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {out} ({len(lines)} files)")


if __name__ == "__main__":
    main()
