#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_event_generator.py
- 목적: 최소 예시용 run을 생성한다(진짜 물리 시뮬이 아니라, 형식/검증 파이프라인 데모).
- 주의: 과학적 주장에 대한 증명용이 아니라, DOI 패키지의 '형식 재현성' 확인용이다.
"""

from __future__ import annotations
import json, hashlib, datetime
from pathlib import Path
from decimal import Decimal, getcontext

getcontext().prec = 80

def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))

def write_json(p: Path, obj: dict) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    root = Path(__file__).resolve().parents[2]
    runs = root/"runs"
    run_dir = runs/"run_MINIMAL_0001"
    run_dir.mkdir(parents=True, exist_ok=True)

    # load locks
    canon = load_json(root/"LOCK"/"canon_lock.json")
    real  = load_json(root/"LOCK"/"realization_lock.json")
    anal  = load_json(root/"LOCK"/"analysis_lock.json")

    dt = Decimal(str(real["delta_t_s"]))
    ticks_per_sec = int((Decimal(1)/dt).to_integral_value(rounding="ROUND_HALF_UP"))
    total_seconds = 10
    total_ticks = ticks_per_sec * total_seconds

    sim_lock = {
        "version": "sim_lock_v1",
        "resolution": {"Nx": 10, "Ny": 10, "Nz": 1},
        "boundary_condition": "periodic",
        "seed": 0,
        "warmup_ticks": 0,
        "total_ticks": total_ticks,
        "update_rule_id": "demo_event_generator_v1",
        "notes": "형식 검증용 최소 run"
    }
    write_json(run_dir/"sim_lock.json", sim_lock)

    # make lock chain
    import subprocess, sys
    subprocess.check_call([sys.executable, str(root/"scripts"/"make_lock_chain.py")])
    lc = load_json(root/"LOCK"/"LOCK_CHAIN.json")

    # create run_meta
    run_id = "MINIMAL_0001"
    run_meta = {
        "run_id": run_id,
        "timestamp_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "machine": {"platform": "demo"},
        "code": {"source_hash": "demo", "dirty_flag": True},
        "locks": {
            "canon_lock_sha256": lc["canon_lock_sha256"],
            "realization_lock_sha256": lc["realization_lock_sha256"],
            "analysis_lock_sha256": lc["analysis_lock_sha256"],
            "sim_lock_sha256": sha256_file(run_dir/"sim_lock.json"),
            "lock_chain_sha256": lc["lock_chain_sha256"]
        },
        "sim": {
            "resolution": sim_lock["resolution"],
            "boundary_condition": sim_lock["boundary_condition"],
            "dt_tick": float(real["delta_t_s"]),
            "warmup_ticks": sim_lock["warmup_ticks"],
            "total_ticks": sim_lock["total_ticks"],
            "update_rule_id": sim_lock["update_rule_id"]
        },
        "outputs": {
            "event_log_path": "event_log.jsonl",
            "signal_log_path": "signal_log.jsonl",
            "summary_path": "summary.json",
            "run_checksums_path": "checksums.json"
        }
    }
    write_json(run_dir/"run_meta.json", run_meta)

    # Generate synthetic events: 1 electron TURNOVER per second, proton ANN ~ 292 per second
    # Use canon_derived if exists, else compute approx
    der_path = root/"LOCK"/"canon_derived.json"
    if der_path.exists():
        der = load_json(der_path)
        nu_p = Decimal(der["nu_p_per_s"])
    else:
        nu_p = Decimal("292.3399781225250")

    # per-second proton count as nearest int
    per_sec_p = int((nu_p).to_integral_value(rounding="ROUND_HALF_UP"))

    event_lines=[]
    for s in range(total_seconds):
        t = s*ticks_per_sec
        # electron turnover
        event_lines.append({
            "run_id": run_id, "tick": int(t), "object": "electron",
            "event_type": "TURNOVER", "time_kind": "det", "q_count": 1,
            "sector": None, "meta": {"sec_index": s}
        })
        # proton ann events distributed inside the second
        # place at deterministic offsets
        for k in range(per_sec_p):
            tk = int(t + (k+1) * (ticks_per_sec // (per_sec_p+1)))
            event_lines.append({
                "run_id": run_id, "tick": tk, "object": "proton",
                "event_type": "ANN", "time_kind": "det", "q_count": 1,
                "sector": None, "meta": {"sec_index": s}
            })

    # write event log
    with (run_dir/"event_log.jsonl").open("w", encoding="utf-8") as f:
        for e in event_lines:
            f.write(json.dumps(e, ensure_ascii=False)+"\n")

    # signal_log: 1 sample per second, phi=1, chi=1
    with (run_dir/"signal_log.jsonl").open("w", encoding="utf-8") as f:
        for s in range(total_seconds):
            t = s*ticks_per_sec
            for obj in ["electron","proton"]:
                f.write(json.dumps({
                    "run_id": run_id, "tick": int(t), "object": obj,
                    "phi_core": 1.0, "chi_dir_core": 1.0, "chi_int_core": 1.0
                }, ensure_ascii=False)+"\n")

    # stdout/stderr
    (run_dir/"stdout.log").write_text("demo run\n", encoding="utf-8")
    (run_dir/"stderr.log").write_text("", encoding="utf-8")

    print("Generated", run_dir)

if __name__ == "__main__":
    main()
