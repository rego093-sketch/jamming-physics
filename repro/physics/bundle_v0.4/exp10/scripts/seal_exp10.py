#!/usr/bin/env python3
"""Seal exp10 snapshot (manifest + checksums + release_tag + registry_snapshot).

Whitepaper alignment (VP §10.4.7–10.4.9):
- snapshot/manifest.json enumerates every file with role/producer/lock_refs/regime_id/depends_on/hash_ref/bytes
- snapshot/checksums.txt provides sha256 for all files (except those excluded via checksum_exclusions)
- snapshot/release_tag.json records a minimal immutable tag (version + lock_ids)
- snapshot/registry_snapshot/registry contains a frozen copy of exp10/registry

This is a deterministic utility and does not generate figures (no images).
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def role_for(rel: str) -> str:
    if rel.startswith('registry/'):
        return 'registry'
    if rel.startswith('configs/'):
        return 'config'
    if rel.startswith('inputs/'):
        return 'input'
    if rel.startswith('scripts/'):
        return 'script'
    if rel.startswith('outputs/'):
        if rel.endswith('.json') and ('/report_' in rel):
            return 'gate_report'
        return 'output'
    if rel.startswith('snapshot/registry_snapshot/'):
        return 'registry'
    if rel.startswith('snapshot/'):
        return 'snapshot'
    return 'other'


def producer_for(rel: str) -> str:
    if rel.startswith('outputs/2d_throat/'):
        return 'script:run_2d_throat.py'
    if rel.startswith('outputs/3d_jamming/'):
        return 'script:run_3d_jamming.py'
    if rel.startswith('outputs/soc_pinning/'):
        return 'script:run_soc_pinning.py'
    if rel.startswith('snapshot/'):
        return 'script:seal_exp10.py'
    return 'manual'


def regime_for(rel: str) -> str:
    if rel.startswith('outputs/2d_throat/'):
        return 'DIM-2'
    if rel.startswith('outputs/3d_jamming/'):
        return 'DIM-3'
    if rel.startswith('outputs/soc_pinning/'):
        return 'SOC-PINNING'
    return 'GLOBAL'


def depends_for(rel: str) -> List[str]:
    # Minimal dependency lists aligned with §10.4.
    if rel.startswith('outputs/2d_throat/'):
        return [
            'configs/regime.yaml',
            'configs/domain.yaml',
            'configs/thresholds.yaml',
            'inputs/geometry/nodes2d.csv',
            'inputs/graphs/edges2d.edgelist',
        ]
    if rel.startswith('outputs/3d_jamming/'):
        return [
            'configs/regime.yaml',
            'configs/domain.yaml',
            'configs/probes.yaml',
            'inputs/geometry/nodes3d.csv',
            'inputs/graphs/edges3d.edgelist',
        ]
    if rel.startswith('outputs/soc_pinning/'):
        return [
            'configs/soc.yaml',
            'configs/thresholds.yaml',
            'inputs/events/events.csv',
            'inputs/graphs/Gopen.edgelist',
            'inputs/graphs/backbone.edgelist',
        ]
    return []


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    snap = root / 'snapshot'
    snap.mkdir(parents=True, exist_ok=True)

    # registry snapshot copy
    rs = snap / 'registry_snapshot'
    rs.mkdir(parents=True, exist_ok=True)
    dst = rs / 'registry'
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(root / 'registry', dst)

    # lock refs
    lock_files = ['canon_lock.json','realization_lock.json','analysis_lock.json','protocol_lock.json','gate_lock.json']
    lock_ids = {}
    for lf in lock_files:
        p = root / 'registry' / lf
        if p.exists():
            try:
                lock_ids[lf] = read_json(p).get('lock_id')
            except Exception:
                lock_ids[lf] = None
        else:
            lock_ids[lf] = None

    # deterministic date for tagging
    prot_path = root / 'registry' / 'protocol_lock.json'
    created = None
    if prot_path.exists():
        try:
            created = read_json(prot_path).get('created')
        except Exception:
            created = None

    # release_tag
    release_tag = {
        'package': 'exp10',
        'version': 'v0.2.6',
        'created': created,
        'lock_ids': lock_ids,
        'notes': ['toy deterministic exp10 package seal']
    }
    (snap / 'release_tag.json').write_text(json.dumps(release_tag, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    # exclusions (checksums file cannot include itself)
    exclusions = ['snapshot/checksums.txt']
    (snap / 'checksum_exclusions.txt').write_text('\n'.join(exclusions)+'\n', encoding='utf-8')

    # list files under exp10/
    files = [p for p in root.rglob('*') if p.is_file()]

    def rel(p: Path) -> str:
        return p.relative_to(root).as_posix()

    # checksums
    sha_map: Dict[str, str] = {}
    lines: List[str] = []
    for p in sorted(files, key=lambda p: rel(p)):
        rp = rel(p)
        if rp in exclusions:
            continue
        h = sha256_file(p)
        sha_map[rp] = h
        lines.append(f"{h}  ./{rp}")
    (snap / 'checksums.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')

    # manifest
    lock_refs = [v for v in lock_ids.values() if v]
    manifest: List[Dict[str, Any]] = []
    for p in sorted(files, key=lambda p: rel(p)):
        rp = rel(p)
        manifest.append({
            'path': rp,
            'role': role_for(rp),
            'producer': producer_for(rp),
            'lock_refs': lock_refs,
            'regime_id': regime_for(rp),
            'depends_on': depends_for(rp),
            'hash_ref': (f"./{rp}" if rp in sha_map else None),
            'bytes': p.stat().st_size,
        })

    (snap / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    print('[OK] sealed exp10 snapshot')


if __name__ == '__main__':
    main()
