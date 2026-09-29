from __future__ import annotations

import sys
from pathlib import Path

from common import repo_root, sha256_file, read_sha256sums

def main() -> int:
    root = repo_root()
    sums_path = root / "checksums" / "SHA256SUMS.txt"
    if not sums_path.exists():
        print(f"ERROR: missing {sums_path}")
        return 2

    pairs = read_sha256sums(sums_path)
    if not pairs:
        print("ERROR: SHA256SUMS.txt is empty or unparsable")
        return 2

    bad = 0
    missing = 0
    for expected, rel in pairs:
        fpath = (root / rel).resolve()
        try:
            fpath.relative_to(root.resolve())
        except Exception:
            print(f"ERROR: path escapes repo root: {rel}")
            bad += 1
            continue

        if not fpath.exists():
            print(f"MISSING: {rel}")
            missing += 1
            continue

        got = sha256_file(fpath)
        if got.lower() != expected.lower():
            print(f"FAIL: {rel}\n  expected={expected}\n  got     ={got}")
            bad += 1

    total = len(pairs)
    ok = total - bad - missing
    print(f"checksum summary: OK={ok} FAIL={bad} MISSING={missing} TOTAL={total}")
    return 0 if (bad == 0 and missing == 0) else 1

if __name__ == "__main__":
    raise SystemExit(main())
