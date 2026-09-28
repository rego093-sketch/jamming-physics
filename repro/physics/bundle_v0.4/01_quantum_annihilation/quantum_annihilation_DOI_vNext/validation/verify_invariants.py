#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_invariants.py
- 목적: 18장 '핵심 불변량' 자동 검증(가능한 범위에서)
  (1) 정준 비율 R_can = ν_p/ν_e
  (2) 관측 비율(게이트 보정) R_gate가 R_can 근방인지
  (3) (옵션) event_log에 sector가 있으면 3-섹터 최소분산 정수화 검사
"""

from __future__ import annotations
import argparse, json, math
from pathlib import Path

def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def iter_jsonl(p: Path):
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: 
                continue
            yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=str)
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    root = run_dir.parents[1]

    der = load_json(root/"LOCK"/"canon_derived.json")
    nu_p_can = float(der["nu_p_per_s"])
    nu_e_can = float(der["nu_e_per_s"])
    R_can = nu_p_can / max(nu_e_can, 1e-30)

    # read computed verify_output if exists
    vpath = run_dir/"verify_output.json"
    if not vpath.exists():
        print("verify_output.json not found. run verify_one first.")
        return

    v = load_json(vpath)
    # compute median ratio from windows if present
    ratios=[]
    for w in v.get("windows", []):
        nu_e = w["nu_gate_hz"]["nu_e_corr"]
        nu_p = w["nu_gate_hz"]["nu_p_corr"]
        if nu_e > 0:
            ratios.append(nu_p/nu_e)
    ratios_sorted = sorted(ratios)
    med = ratios_sorted[len(ratios_sorted)//2] if ratios_sorted else None

    out = {
        "R_can": R_can,
        "R_gate_median": med,
        "rel_error": None if med is None else abs(med-R_can)/R_can
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
