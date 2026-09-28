#!/usr/bin/env python3
"""Reference implementation: run a plan.json into runs/.

This executor is intentionally minimal and deterministic.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--protocol', required=True)
    ap.add_argument('--plan', required=True)
    ap.add_argument('--out', default='runs')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    plan = json.loads((root / args.plan).read_text(encoding='utf-8'))

    for job in plan.get('jobs', []):
        subprocess.check_call([
            'python3', str(root / 'ref_impl' / 'run_one.py'),
            '--root', str(root),
            '--protocol', args.protocol,
            '--job_json', json.dumps(job, ensure_ascii=False, sort_keys=True),
            '--out', args.out,
        ])


if __name__ == '__main__':
    main()
