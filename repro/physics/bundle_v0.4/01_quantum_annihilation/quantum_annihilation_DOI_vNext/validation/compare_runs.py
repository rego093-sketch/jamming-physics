#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_runs.py
- 목적: runs 폴더 내 여러 run의 summary.json 또는 verify_output.json을 비교하여
        해상도/seed/경계 변화에 따른 수렴성(16장)을 빠르게 점검한다.
- 현재 버전: 최소 구현(중앙값 오차/비율만 요약)
"""

from __future__ import annotations
import json
from pathlib import Path

def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def main():
    root = Path(".").resolve()
    run_dirs = sorted([p for p in (root/"runs").glob("run_*") if p.is_dir()])
    rows=[]
    for rd in run_dirs:
        p = rd/"verify_output.json"
        if not p.exists():
            p = rd/"summary.json"
            if not p.exists():
                continue
        d = load_json(p)
        rid = d.get("run_id", rd.name)
        med = d.get("med_rel_err", {})
        rows.append((rid, med.get("e"), med.get("p"), med.get("ratio"), d.get("pass_fail",{}).get("level2_science")))
    print("run_id,med_err_e,med_err_p,med_err_ratio,level2")
    for r in rows:
        print(",".join([str(x) for x in r]))

if __name__ == "__main__":
    main()
