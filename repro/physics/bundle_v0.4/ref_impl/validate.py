#!/usr/bin/env python3
"""Reference implementation: validate runs/ structure.

Checks only:
- required files exist
- manifest.sha256 matches manifest.json

This is *not* a physics validator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', default='runs')
    args = ap.parse_args()

    runs = Path(args.runs)
    if not runs.exists():
        raise SystemExit(f"missing runs dir: {runs}")

    required = {
        'protocol.locked.json',
        'registry_snapshot.json',
        'run_log.jsonl',
        'metrics.json',
        'manifest.json',
        'manifest.sha256',
    }

    bad = 0
    for rd in sorted([p for p in runs.iterdir() if p.is_dir()]):
        missing = [f for f in required if not (rd / f).exists()]
        if missing:
            print(f"[FAIL] {rd.name} missing: {missing}")
            bad += 1
            continue
        expected = (rd / 'manifest.sha256').read_text(encoding='utf-8').split()[0]
        actual = sha256_file(rd / 'manifest.json')
        if expected != actual:
            print(f"[FAIL] {rd.name} manifest hash mismatch")
            bad += 1
        else:
            print(f"[OK] {rd.name}")

    raise SystemExit(1 if bad else 0)


if __name__ == '__main__':
    main()
