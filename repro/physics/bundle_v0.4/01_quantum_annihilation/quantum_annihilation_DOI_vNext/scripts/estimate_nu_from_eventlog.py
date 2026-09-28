#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estimate_nu_from_eventlog.py
- 목적: runs/run_<ID>/event_log.jsonl에서 카운트 기반 ν_obs(전자/양성자)와 무차원 비율 Np/Ne를 계산.
- 입력:
  (1) run_dir: runs/run_<ID>
  (2) LOCK/analysis_lock.json: 이벤트 타입, 윈도우 길이
  (3) LOCK/realization_lock.json: Δt (tick→SI)
- 출력: 표준 JSON (stdout)
"""

from __future__ import annotations
import argparse, json
from pathlib import Path

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            yield json.loads(line)

def count_events(event_log: Path, obj: str, etype: str, n0: int, n1: int, time_kind: str="det") -> int:
    c = 0
    for e in iter_jsonl(event_log):
        if e.get("object") != obj: 
            continue
        if e.get("event_type") != etype:
            continue
        if time_kind != "both" and e.get("time_kind") != time_kind:
            continue
        t = int(e["tick"])
        if n0 <= t < n1:
            c += int(e.get("q_count", 1))
    return c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=str, help="runs/run_<ID> 폴더")
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    root = run_dir.parents[1]  # .../runs/run_<ID> -> ROOT
    analysis = load_json(root/"LOCK"/"analysis_lock.json")
    realization = load_json(root/"LOCK"/"realization_lock.json")

    dt = float(realization["delta_t_s"])
    wlen = int(analysis["windowing"]["window_length_ticks"])
    warm = int(analysis["windowing"]["warmup_drop_ticks"])
    tkind = analysis.get("event_time_kind", "det")

    e_type = analysis["event_type_for_nu"]["electron"]
    p_type = analysis["event_type_for_nu"]["proton"]

    # 단일 윈도우(예: warmup 이후 첫 window)만 예시로 계산
    n0 = warm
    n1 = warm + wlen
    Ne = count_events(run_dir/"event_log.jsonl","electron", e_type, n0, n1, tkind if tkind!="both" else "det")
    Np = count_events(run_dir/"event_log.jsonl","proton",  p_type, n0, n1, tkind if tkind!="both" else "det")

    dT = (n1-n0)*dt
    nu_e = Ne/dT if dT>0 else None
    nu_p = Np/dT if dT>0 else None
    R = (Np/Ne) if Ne>0 else None

    out = {
        "run_dir": str(run_dir),
        "window": {"n0": n0, "n1": n1, "duration_s": dT},
        "counts": {"Ne": Ne, "Np": Np},
        "nu_obs": {"nu_e_hz": nu_e, "nu_p_hz": nu_p},
        "ratio_count_Np_over_Ne": R
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
