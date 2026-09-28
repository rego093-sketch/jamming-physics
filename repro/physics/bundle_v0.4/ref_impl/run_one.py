#!/usr/bin/env python3
"""Reference implementation: run one job into runs/<run_id>/.

Targets whitepaper §16.2 (run directory + log format):
- run_id format: YYYYMMDDThhmmssZ ⨯ pid ⨯ short_digest (eq. S16_02_runid)
- run_log.jsonl line schema: {ts,run_id,pid,ver,phase,event,payload} (eq. S16_02_log_schema)
- protocol.locked.json: canonicalized protocol copy + digests

Determinism policy:
- Timestamp date is taken from `registry/protocol_lock.json::created` (YYYY-MM-DD)
- Timestamp time is derived from the job digest (so no wall-clock dependency)
- short_digest is derived from the canonical JSON digest of the protocol

This preserves stable outputs while respecting the document-level format contracts.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def to_jsonable(x: Any) -> Any:
    """Convert PyYAML-loaded objects (including dates) to JSON-serializable forms."""
    if isinstance(x, (datetime.date, datetime.datetime)):
        return x.isoformat()
    if isinstance(x, dict):
        return {str(k): to_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_jsonable(v) for v in x]
    return x


def canonical_json_dumps(obj: Any) -> str:
    return json.dumps(to_jsonable(obj), sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def canonical_digest(obj: Any) -> str:
    return sha256_bytes(canonical_json_dumps(obj).encode('utf-8'))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(obj), indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(to_jsonable(r), ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n')


def list_files(base: Path) -> List[Path]:
    return sorted([p for p in base.rglob('*') if p.is_file()], key=lambda p: p.as_posix())


def build_manifest(base: Path) -> List[Dict[str, Any]]:
    return [
        {
            'path': p.relative_to(base).as_posix(),
            'sha256': sha256_file(p),
            'bytes': p.stat().st_size,
        }
        for p in list_files(base)
    ]


def hms_from_digest(digest_hex: str) -> str:
    """Deterministic hhmmss from digest prefix."""
    # Use first 8 hex chars -> 32-bit integer
    x = int(digest_hex[:8], 16)
    sec = x % 86400
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}{m:02d}{s:02d}"


def ymd_from_created(created: Any) -> str:
    """Convert created (string/date) into YYYYMMDD."""
    if isinstance(created, (datetime.date, datetime.datetime)):
        return created.strftime('%Y%m%d')
    s = str(created)
    # Accept 'YYYY-MM-DD' or already 'YYYYMMDD'
    if len(s) == 10 and s[4] == '-' and s[7] == '-':
        return s.replace('-', '')
    if len(s) == 8 and s.isdigit():
        return s
    # Fallback: strip non-digits
    digits = ''.join(ch for ch in s if ch.isdigit())
    return digits[:8] if len(digits) >= 8 else '19700101'


def load_protocol(protocol_path: Path) -> Tuple[Any, str, str, str]:
    """Return (protocol_obj, raw_sha256, canon_sha256, canon_json)."""
    raw_bytes = protocol_path.read_bytes()
    raw_sha = sha256_bytes(raw_bytes)

    if protocol_path.suffix.lower() in {'.yaml', '.yml'}:
        obj = yaml.safe_load(raw_bytes.decode('utf-8'))
    else:
        obj = json.loads(raw_bytes.decode('utf-8'))

    canon_json = canonical_json_dumps(obj)
    canon_sha = sha256_bytes(canon_json.encode('utf-8'))
    return obj, raw_sha, canon_sha, canon_json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', help='bundle root')
    ap.add_argument('--protocol', required=True)
    ap.add_argument('--job_json', required=True, help='job spec as JSON string')
    ap.add_argument('--out', default='runs')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    job = json.loads(args.job_json)

    # Global lock meta for deterministic timestamp + version
    protocol_lock = json.loads((root / 'registry' / 'protocol_lock.json').read_text(encoding='utf-8'))
    created_ymd = ymd_from_created(protocol_lock.get('created', '1970-01-01'))
    ver = protocol_lock.get('version', 'v0')

    pid = str(job.get('pid', 'UNKNOWN'))

    # job digest (deterministic) used for hhmmss
    job_digest = canonical_digest(job)
    hhmmss = hms_from_digest(job_digest)

    # protocol canonical digest -> short_digest
    protocol_path = (root / args.protocol).resolve()
    protocol_obj, protocol_raw_sha, protocol_canon_sha, protocol_canon_json = load_protocol(protocol_path)
    short_digest = protocol_canon_sha[:12]

    timestamp = f"{created_ymd}T{hhmmss}Z"
    run_id = f"{timestamp}__{pid}__{short_digest}"

    run_dir = root / args.out / run_id
    if run_dir.exists():
        raise SystemExit(f"run_dir already exists: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=False)

    # protocol.locked.json
    write_json(run_dir / 'protocol.locked.json', {
        'protocol_path': Path(args.protocol).as_posix(),
        'protocol_raw_sha256': protocol_raw_sha,
        'protocol_canonical_json_sha256': protocol_canon_sha,
        'protocol_canonical_json': protocol_obj,
    })

    # locks_snapshot/
    locks_snapshot = run_dir / 'locks_snapshot'
    locks_snapshot.mkdir(parents=True, exist_ok=True)
    for lock_name in ['canon_lock.json', 'realization_lock.json', 'analysis_lock.json', 'locks.sha256']:
        src = root / 'locks' / lock_name
        if src.exists():
            shutil.copy2(src, locks_snapshot / lock_name)

    # registry_snapshot.json
    rs_src = root / 'snapshot' / 'registry_snapshot' / 'registry_snapshot.json'
    if rs_src.exists():
        shutil.copy2(rs_src, run_dir / 'registry_snapshot.json')

    # Execute steps (deterministic: scripts use protocol_lock.created)
    log_rows: List[Dict[str, Any]] = []

    def log(phase: str, event: str, payload: Dict[str, Any]) -> None:
        log_rows.append({
            'ts': timestamp,
            'run_id': run_id,
            'pid': pid,
            'ver': ver,
            'phase': phase,
            'event': event,
            'payload': payload,
        })

    log('init', 'START', {'job_id': job.get('job_id'), 'job_digest': job_digest, 'protocol_short_digest': short_digest})

    if job.get('params', {}).get('build_derived'):
        cmd = ['python3', str(root / 'scripts' / 'build_derived.py')]
        subprocess.check_call(cmd)
        log('build_derived', 'OK', {'cmd': cmd})

    if job.get('params', {}).get('run_gates'):
        cmd = ['python3', str(root / 'scripts' / 'run_gates.py')]
        subprocess.check_call(cmd)
        log('run_gates', 'OK', {'cmd': cmd})

    if job.get('params', {}).get('seal_snapshot'):
        cmd = ['python3', str(root / 'scripts' / 'seal_snapshot.py')]
        subprocess.check_call(cmd)
        log('seal_snapshot', 'OK', {'cmd': cmd})

    # Copy outputs into run_dir/outputs/
    out_dir = run_dir / 'outputs'
    (out_dir / 'derived').mkdir(parents=True, exist_ok=True)
    (out_dir / 'gate_reports').mkdir(parents=True, exist_ok=True)

    # derived
    for p in (root / 'derived').rglob('*'):
        if p.is_file():
            rel = p.relative_to(root / 'derived')
            dst = out_dir / 'derived' / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)

    # gate reports
    for p in (root / 'gate' / 'reports').glob('gate_report_*.json'):
        shutil.copy2(p, out_dir / 'gate_reports' / p.name)

    # artifacts.md (human quick index)
    artifacts_md = """# artifacts

This run contains:

- outputs/derived/*
- outputs/gate_reports/*
- protocol.locked.json
- locks_snapshot/*
- registry_snapshot.json
- run_log.jsonl
- metrics.json
- manifest.json + manifest.sha256
"""
    (run_dir / 'artifacts.md').write_text(artifacts_md, encoding='utf-8')

    # run_log.jsonl
    log('final', 'END', {'status': 'ok'})
    write_jsonl(run_dir / 'run_log.jsonl', log_rows)

    # metrics.json
    metrics = {
        'run_id': run_id,
        'pid': pid,
        'ver': ver,
        'job_id': job.get('job_id'),
        'job_digest': job_digest,
        'protocol_raw_sha256': protocol_raw_sha,
        'protocol_canonical_json_sha256': protocol_canon_sha,
        'n_gate_reports': len(list((root / 'gate' / 'reports').glob('gate_report_*.json'))),
    }
    write_json(run_dir / 'metrics.json', metrics)

    # manifest.json + manifest.sha256
    manifest = build_manifest(run_dir)
    write_json(run_dir / 'manifest.json', manifest)
    (run_dir / 'manifest.sha256').write_text(sha256_file(run_dir / 'manifest.json') + '  manifest.json\n', encoding='utf-8')

    print(f"[OK] wrote run: {run_dir}")


if __name__ == '__main__':
    main()
