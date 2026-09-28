#!/usr/bin/env python3
"""Build release_manifest.json and release_manifest.sha256 (bundle root).

The whitepaper (§16.3.3) treats release_manifest.json as the top-level manifest
for the release.

Policy:
- Enumerate ALL files under the bundle root.
- Exclude `release_manifest.json` and `release_manifest.sha256` themselves.
- Stable ordering by path.
- Hash algorithm: sha256.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

EXCLUDE = {"release_manifest.json", "release_manifest.sha256"}


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b=f.read(1024*1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    entries=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file():
            continue
        rel=p.relative_to(root).as_posix()
        if rel in EXCLUDE:
            continue
        entries.append({
            "path": rel,
            "bytes": p.stat().st_size,
            "sha256": sha256_file(p),
        })

    out_json = root/'release_manifest.json'
    out_json.write_text(json.dumps(entries, indent=2, ensure_ascii=False, sort_keys=True)+"\n", encoding='utf-8')
    digest = sha256_file(out_json)
    (root/'release_manifest.sha256').write_text(f"{digest}  release_manifest.json\n", encoding='utf-8')
    print('[OK] wrote', out_json, 'entries', len(entries))


if __name__=='__main__':
    main()
