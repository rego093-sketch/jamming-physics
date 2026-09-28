#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_one.py  (read-only by default)
- 목적:
  1) run 폴더(runs/run_<ID>)의 무결성(Level0), 스키마(Level1), 과학적 지표(Level2)를 자동 검증
  2) summary.json이 존재하면, 재계산 결과와 PASS/FAIL 일치 여부를 확인
  3) (옵션) --write 로 summary.json / checksums.json 생성(빌드 단계에서만 사용 권장)

주의:
- DOI 릴리즈 후에는 --write 사용 금지(불변성 원칙).
"""

from __future__ import annotations
import argparse, json, hashlib, platform, sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

try:
    import jsonschema
except Exception as e:
    jsonschema = None

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            yield json.loads(line)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def validate_schema(obj: Any, schema_path: Path, ctx: str, reasons: List[str]) -> bool:
    if jsonschema is None:
        reasons.append(f"[Level1] jsonschema 미설치: 스키마 검증 스킵({ctx})")
        return True
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=obj, schema=schema)
        return True
    except Exception as e:
        reasons.append(f"[Level1] schema fail({ctx}): {e}")
        return False

def compute_lock_chain(root: Path) -> Tuple[dict, List[str], bool]:
    reasons: List[str] = []
    ok = True
    lc_path = root/"LOCK"/"LOCK_CHAIN.json"
    if not lc_path.exists():
        return ({}, ["[Level0] LOCK_CHAIN.json 누락"], False)

    lc = load_json(lc_path)

    canon = root/"LOCK"/"canon_lock.json"
    real  = root/"LOCK"/"realization_lock.json"
    anal  = root/"LOCK"/"analysis_lock.json"
    for p in [canon, real, anal]:
        if not p.exists():
            reasons.append(f"[Level0] LOCK 파일 누락: {p}")
            ok = False
    if not ok:
        return (lc, reasons, False)

    sha_c = sha256_file(canon)
    sha_r = sha256_file(real)
    sha_a = sha256_file(anal)
    chain = sha256_bytes((sha_c + sha_r + sha_a).encode("utf-8"))

    if lc.get("canon_lock_sha256") != sha_c:
        reasons.append("[Level0] canon_lock_sha256 불일치")
        ok = False
    if lc.get("realization_lock_sha256") != sha_r:
        reasons.append("[Level0] realization_lock_sha256 불일치")
        ok = False
    if lc.get("analysis_lock_sha256") != sha_a:
        reasons.append("[Level0] analysis_lock_sha256 불일치")
        ok = False
    if lc.get("lock_chain_sha256") != chain:
        reasons.append("[Level0] lock_chain_sha256 불일치")
        ok = False

    return (lc, reasons, ok)

def load_canon_derived(root: Path) -> dict:
    der_path = root/"LOCK"/"canon_derived.json"
    if der_path.exists():
        return load_json(der_path)
    # 없으면 계산 스크립트 실행을 유도(여기서는 최소 파생만 계산)
    canon = load_json(root/"LOCK"/"canon_lock.json")
    import math
    D_anch = float(canon["D_anch_m"])
    r_p    = float(canon["r_p_m"])
    r0 = D_anch/2.0
    delta = 1.0/(math.pi**2)
    s_p = r0/r_p
    nu_p = s_p*delta
    r_e = D_anch/(2.0*(math.pi**2))
    s_e = r0/r_e
    nu_e = s_e*delta
    return {
        "D_anch_m": str(D_anch),
        "r_p_m": str(r_p),
        "r0_m": str(r0),
        "delta_1_over_pi2": str(delta),
        "s_p": str(s_p),
        "nu_p_per_s": str(nu_p),
        "r_e_m": str(r_e),
        "s_e": str(s_e),
        "nu_e_per_s": str(nu_e),
        "notes": "fallback derived (float). 권장: scripts/compute_canon.py 실행."
    }

def compute_u(phi: float, chi_dir: float, chi_int: float) -> float:
    # 단순 기본형(필요 시 analysis_lock에서 확장 가능)
    # phi ∈ [0,1], chi_dir ∈ [-1,1], chi_int ∈ [-1,1]
    # u는 [0,1] 범위를 목표로 한다.
    # 여기서는: u = clamp(phi) * clamp(|chi_dir|) * clamp((chi_int+1)/2)
    def clamp01(x: float) -> float:
        return 0.0 if x < 0 else (1.0 if x > 1 else x)
    return clamp01(phi) * clamp01(abs(chi_dir)) * clamp01((chi_int + 1.0)/2.0)

def window_edges(total_ticks: int, warmup_drop: int, wlen: int, overlap_ratio: float) -> List[Tuple[int,int]]:
    if wlen <= 0:
        return []
    step = int(round(wlen * (1.0 - overlap_ratio)))
    if step <= 0:
        step = wlen
    edges=[]
    n0 = warmup_drop
    while n0 + wlen <= total_ticks:
        edges.append((n0, n0+wlen))
        n0 += step
    return edges

def compute_window_metrics(run_dir: Path, root: Path, reasons: List[str]) -> dict:
    analysis = load_json(root/"LOCK"/"analysis_lock.json")
    realization = load_json(root/"LOCK"/"realization_lock.json")
    der = load_canon_derived(root)

    dt = float(realization["delta_t_s"])
    wlen = int(analysis["windowing"]["window_length_ticks"])
    warm = int(analysis["windowing"]["warmup_drop_ticks"])
    overlap = float(analysis["windowing"]["overlap_ratio"])

    e_type = analysis["event_type_for_nu"]["electron"]
    p_type = analysis["event_type_for_nu"]["proton"]
    tkind  = analysis.get("event_time_kind","det")

    # load logs
    event_path = run_dir/"event_log.jsonl"
    if not event_path.exists():
        reasons.append("[Level1] event_log.jsonl 누락")
        return {"windows": []}

    # signal log optional
    signal_path = run_dir/"signal_log.jsonl"
    signal_samples = []
    if signal_path.exists() and analysis.get("estimators",{}).get("use_signal_log_if_present", True):
        for s in iter_jsonl(signal_path):
            if s.get("object") in ("electron","proton"):
                signal_samples.append(s)
        # tick 정렬
        signal_samples.sort(key=lambda x: int(x["tick"]))

    # parse events once
    events=[]
    for e in iter_jsonl(event_path):
        if tkind != "both" and e.get("time_kind") != tkind:
            continue
        if e.get("object") not in ("electron","proton"):
            continue
        if e.get("event_type") not in (e_type, p_type):
            # 다른 이벤트 타입이 있어도 무방(검증에는 미사용)
            continue
        events.append(e)

    # total_ticks from run_meta or sim_lock
    meta = load_json(run_dir/"run_meta.json")
    total_ticks = int(meta["sim"]["total_ticks"])

    edges = window_edges(total_ticks, warm, wlen, overlap)
    if not edges:
        reasons.append("[Level2] 윈도우가 0개(총틱/윈도우 설정 확인)")
        return {"windows":[]}

    # helper: get ubar/f_pass per object in window using signal samples(샘플 평균)
    def duty_for(obj: str, n0: int, n1: int) -> Tuple[float,float]:
        if not signal_samples:
            return (1.0, 1.0)  # 신호가 없으면 기본 1로 처리(단, report에 기록)
        vals=[]
        for s in signal_samples:
            if s.get("object") != obj:
                continue
            t = int(s["tick"])
            if n0 <= t < n1:
                phi = float(s.get("phi_core",1.0))
                cd  = float(s.get("chi_dir_core",1.0))
                ci  = float(s.get("chi_int_core",1.0))
                vals.append((phi,cd,ci))
        if not vals:
            return (1.0, 1.0)
        # pass 조건: u_min과 별개로, 단순히 u>0로 통과로 정의(상세는 15장 확장)
        u_list=[compute_u(*v) for v in vals]
        ubar = sum(u_list)/len(u_list)
        fpass = sum(1 for u in u_list if u > 0.0)/len(u_list)
        return (ubar, fpass)

    nu_p_can = float(der["nu_p_per_s"])
    nu_e_can = float(der["nu_e_per_s"])
    # nu_e_can은 이상적으로 1.0

    u_min = float(analysis["thresholds"]["u_min"])
    pf = analysis["passfail"]
    eps_e = float(pf["eps_nu_e_rel"])
    eps_p = float(pf["eps_nu_p_rel"])
    eps_r = float(pf["eps_ratio_rel"])
    min_e = int(pf["min_events_per_window_e"])
    min_p = int(pf["min_events_per_window_p"])

    win_rows=[]
    rel_errors_e=[]
    rel_errors_p=[]
    rel_errors_r=[]

    for (n0,n1) in edges:
        dur = (n1-n0)*dt
        # count events in window
        Ne=0; Np=0
        for e in events:
            t=int(e["tick"])
            if not (n0 <= t < n1):
                continue
            if e["object"]=="electron" and e["event_type"]==e_type:
                Ne += int(e.get("q_count",1))
            if e["object"]=="proton" and e["event_type"]==p_type:
                Np += int(e.get("q_count",1))

        nu_e = Ne/dur if dur>0 else 0.0
        nu_p = Np/dur if dur>0 else 0.0

        ubar_e, fpass_e = duty_for("electron", n0, n1)
        ubar_p, fpass_p = duty_for("proton",  n0, n1)

        # gate-corrected
        ubar_e_eff = max(ubar_e, u_min)
        ubar_p_eff = max(ubar_p, u_min)
        nu_e_corr = nu_e/ubar_e_eff
        nu_p_corr = nu_p/ubar_p_eff

        # errors (only if enough events)
        err_e = None
        err_p = None
        err_r = None
        if Ne >= min_e:
            err_e = abs(nu_e_corr - nu_e_can) / max(nu_e_can, 1e-30)
            rel_errors_e.append(err_e)
        if Np >= min_p:
            err_p = abs(nu_p_corr - nu_p_can) / max(nu_p_can, 1e-30)
            rel_errors_p.append(err_p)
        if (Ne >= min_e) and (Np >= min_p):
            ratio = nu_p_corr / max(nu_e_corr, 1e-30)
            err_r = abs(ratio - nu_p_can) / max(nu_p_can, 1e-30)  # since nu_e_can=1
            rel_errors_r.append(err_r)

        win_rows.append({
            "n0": n0, "n1": n1, "duration_s": dur,
            "counts": {"Ne": Ne, "Np": Np},
            "nu_obs_hz": {"nu_e": nu_e, "nu_p": nu_p},
            "gate": {"ubar_e": ubar_e, "ubar_p": ubar_p, "fpass_e": fpass_e, "fpass_p": fpass_p},
            "nu_gate_hz": {"nu_e_corr": nu_e_corr, "nu_p_corr": nu_p_corr},
            "rel_err": {"e": err_e, "p": err_p, "ratio": err_r}
        })

    # run-level pass: median error <= eps
    def median(x: List[float]) -> Optional[float]:
        if not x: return None
        xs=sorted(x)
        m=len(xs)//2
        return xs[m] if len(xs)%2==1 else 0.5*(xs[m-1]+xs[m])

    med_e = median(rel_errors_e)
    med_p = median(rel_errors_p)
    med_r = median(rel_errors_r)

    level2_ok = True
    if med_e is None:
        reasons.append("[Level2] 전자 윈도우에서 min_events 조건을 만족한 샘플이 없음")
        level2_ok = False
    else:
        if med_e > eps_e:
            reasons.append(f"[Level2] 전자 ν_e/ubar 오차(중앙값) {med_e:.4g} > eps {eps_e}")
            level2_ok = False

    if med_p is None:
        reasons.append("[Level2] 양성자 윈도우에서 min_events 조건을 만족한 샘플이 없음")
        level2_ok = False
    else:
        if med_p > eps_p:
            reasons.append(f"[Level2] 양성자 ν_p/ubar 오차(중앙값) {med_p:.4g} > eps {eps_p}")
            level2_ok = False

    if med_r is None:
        reasons.append("[Level2] 비율(R) 윈도우 샘플이 없음")
        level2_ok = False
    else:
        if med_r > eps_r:
            reasons.append(f"[Level2] 비율(R) 오차(중앙값) {med_r:.4g} > eps {eps_r}")
            level2_ok = False

    return {
        "windows": win_rows,
        "med_rel_err": {"e": med_e, "p": med_p, "ratio": med_r},
        "level2_ok": level2_ok
    }

def verify_checksums(run_dir: Path, reasons: List[str]) -> bool:
    cs_path = run_dir/"checksums.json"
    if not cs_path.exists():
        reasons.append("[Level0] checksums.json 누락")
        return False
    cs = load_json(cs_path)
    ok = True
    mapping = {
        "event_log_sha256": run_dir/"event_log.jsonl",
        "signal_log_sha256": run_dir/"signal_log.jsonl",
        "summary_sha256": run_dir/"summary.json",
        "stdout_sha256": run_dir/"stdout.log",
        "stderr_sha256": run_dir/"stderr.log"
    }
    for key, p in mapping.items():
        if key not in cs:
            # signal_log는 optional로 취급
            if key == "signal_log_sha256":
                continue
            reasons.append(f"[Level0] checksums.json에 {key} 누락")
            ok = False
            continue
        if not p.exists():
            reasons.append(f"[Level0] 파일 누락: {p.name}")
            ok = False
            continue
        sha = sha256_file(p)
        if cs[key] != sha:
            reasons.append(f"[Level0] {p.name} sha256 불일치")
            ok = False
    return ok

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=str, help="runs/run_<ID> 폴더")
    ap.add_argument("--write", action="store_true", help="summary.json/ checksums.json 생성(릴리즈 후 사용 금지)")
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.exists():
        print("run_dir not found:", run_dir, file=sys.stderr)
        sys.exit(2)

    root = run_dir.parents[1]
    reasons: List[str] = []

    # Level0: lock chain
    lc, lock_reasons, lock_ok = compute_lock_chain(root)
    reasons.extend(lock_reasons)

    # Level0: run checksums
    checksums_ok = False
    if (run_dir/"checksums.json").exists():
        checksums_ok = verify_checksums(run_dir, reasons)
    else:
        if args.write:
            # write 모드에서는 나중에 생성
            checksums_ok = True
        else:
            reasons.append("[Level0] checksums.json 누락")
            checksums_ok = False

    level0_ok = lock_ok and checksums_ok

    # Level1: schema validation
    level1_ok = True
    # run_meta
    meta_path = run_dir/"run_meta.json"
    if not meta_path.exists():
        reasons.append("[Level1] run_meta.json 누락")
        level1_ok = False
        meta = None
    else:
        meta = load_json(meta_path)
        level1_ok &= validate_schema(meta, root/"schema"/"run_meta.schema.json", "run_meta", reasons)

    # event_log lines
    event_path = run_dir/"event_log.jsonl"
    if not event_path.exists():
        reasons.append("[Level1] event_log.jsonl 누락")
        level1_ok = False
    else:
        if jsonschema is not None:
            sch = load_json(root/"schema"/"event_log_line.schema.json")
            for idx, e in enumerate(iter_jsonl(event_path)):
                try:
                    jsonschema.validate(instance=e, schema=sch)
                except Exception as ex:
                    reasons.append(f"[Level1] event_log line {idx} schema fail: {ex}")
                    level1_ok = False
                    break

    # signal_log lines (optional)
    sig_path = run_dir/"signal_log.jsonl"
    if sig_path.exists() and jsonschema is not None:
        sch = load_json(root/"schema"/"signal_log_line.schema.json")
        for idx, s in enumerate(iter_jsonl(sig_path)):
            try:
                jsonschema.validate(instance=s, schema=sch)
            except Exception as ex:
                reasons.append(f"[Level1] signal_log line {idx} schema fail: {ex}")
                level1_ok = False
                break

    # LOCK schema
    for nm, sch in [("canon_lock","canon_lock.schema.json"),("realization_lock","realization_lock.schema.json"),("analysis_lock","analysis_lock.schema.json")]:
        obj = load_json(root/"LOCK"/f"{nm}.json")
        level1_ok &= validate_schema(obj, root/"schema"/sch, nm, reasons)

    # Level2: compute metrics
    level2_ok = False
    metrics = {"windows": []}
    if level0_ok and level1_ok:
        metrics = compute_window_metrics(run_dir, root, reasons)
        level2_ok = bool(metrics.get("level2_ok", False))
    else:
        reasons.append("[Level2] Level0/1 FAIL로 인해 과학 지표 검증 스킵")

    # Prepare summary object (computed)
    analysis_sha = sha256_file(root/"LOCK"/"analysis_lock.json")
    computed_summary = {
        "run_id": meta["run_id"] if meta else run_dir.name,
        "analysis_lock_hash": analysis_sha,
        "windows": metrics.get("windows", []),
        "med_rel_err": metrics.get("med_rel_err", {}),
        "pass_fail": {
            "level0_integrity": bool(level0_ok),
            "level1_schema": bool(level1_ok),
            "level2_science": bool(level2_ok),
            "reasons": reasons
        }
    }

    # If summary exists, compare pass_fail (strict)
    stored_ok = True
    sum_path = run_dir/"summary.json"
    if sum_path.exists():
        stored = load_json(sum_path)
        # schema check
        stored_ok &= validate_schema(stored, root/"schema"/"summary.schema.json", "summary", reasons)
        if stored.get("pass_fail", {}) != computed_summary.get("pass_fail", {}):
            # 사유 문자열이 달라질 수 있으니 최소 비교만:
            sp = stored.get("pass_fail", {})
            cp = computed_summary.get("pass_fail", {})
            if (sp.get("level0_integrity"), sp.get("level1_schema"), sp.get("level2_science")) != (cp.get("level0_integrity"), cp.get("level1_schema"), cp.get("level2_science")):
                reasons.append("[Compare] stored summary pass_fail mismatch")
                stored_ok = False
    else:
        if args.write:
            write_json(sum_path, computed_summary)
        else:
            reasons.append("[Level1] summary.json 누락(릴리즈 패키지에는 포함 권장)")
            stored_ok = False

    # write mode: create checksums.json
    if args.write:
        # stdout/stderr placeholder may not exist; create empty if missing
        for fn in ["stdout.log","stderr.log"]:
            p = run_dir/fn
            if not p.exists():
                p.write_text("", encoding="utf-8")

        cs = {
            "run_id": computed_summary["run_id"],
            "event_log_sha256": sha256_file(run_dir/"event_log.jsonl"),
            "summary_sha256": sha256_file(run_dir/"summary.json"),
            "stdout_sha256": sha256_file(run_dir/"stdout.log"),
            "stderr_sha256": sha256_file(run_dir/"stderr.log"),
        }
        if (run_dir/"signal_log.jsonl").exists():
            cs["signal_log_sha256"] = sha256_file(run_dir/"signal_log.jsonl")
        write_json(run_dir/"checksums.json", cs)

    # Final exit code
    all_ok = level0_ok and level1_ok and level2_ok and stored_ok
    if not all_ok:
        print(json.dumps(computed_summary, ensure_ascii=False, indent=2))
        sys.exit(1)
    else:
        print(json.dumps(computed_summary, ensure_ascii=False, indent=2))
        sys.exit(0)

if __name__ == "__main__":
    main()
