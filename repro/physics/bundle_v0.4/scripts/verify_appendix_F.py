#!/usr/bin/env python3
"""Deterministic verifier for Appendix F (integer decomposition of nu_p_can).

This appendix is an *interpretive* (NON-LOCK) decomposition of the already-LOCKed
canonical proton event rate nu_p_can (Section 9.4):

  nu_p_can = N_act + eps, with N_act := floor(nu_p_can), eps := nu_p_can - N_act.

It also computes a candidate discrete mapping:
  82*4 - 9*4 = 292
which is kept as a hypothesis until the meanings of "point", "static inlet", and
"4-point locking" are explicitly locked.

Outputs a JSON object to stdout (and optionally to --write).
All numeric values are stored as decimal strings for cross-platform reproducibility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Dict

getcontext().prec = 120


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def d(x: Any) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def dstr(x: Decimal) -> str:
    return str(x)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", default="", help="Optional output path for the JSON log")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]

    canon_p = root / "registry" / "canon_lock.json"
    prot_p = root / "registry" / "protocol_lock.json"
    snap_p = root / "registry" / "registry_snapshot.json"

    canon = read_json(canon_p)
    prot = read_json(prot_p)
    snap = read_json(snap_p) if snap_p.exists() else None

    # [LOCK] constants
    pi = d(canon["constants"]["pi"])
    D_anch = d(canon["inputs"]["D_anch_m"])
    r_p = d(canon["inputs"]["r_p_m"])

    # delta: either explicit numeric or derived universal rule 1/pi^2
    delta_item = canon.get("constants", {}).get("delta_rect", "1/pi^2")
    if isinstance(delta_item, (int, float)):
        delta = d(delta_item)
        delta_mode = "numeric"
    else:
        delta = Decimal(1) / (pi * pi)
        delta_mode = "universal_1_over_pi_sq"

    # [DERIVED] Section 9.4
    s_p = D_anch / (Decimal(2) * r_p)
    nu = s_p * delta

    # integer decomposition (NON-LOCK interpretive step)
    # (nu>0 in this model; int() is floor for positive values)
    N_act = int(nu)
    eps = nu - Decimal(N_act)

    # candidate discrete mapping (hypothesis parameters; not locked)
    N_core = 82
    points_per = 4
    N_static_q = 9
    N_cap = N_core * points_per
    N_static = N_static_q * points_per
    N_active_points = N_cap - N_static

    out: Dict[str, Any] = {
        "script": "verify_appendix_F.py",
        "scope": "Appendix F (NON-LOCK interpretive decomposition)",
        "registry_snapshot_id": (snap or {}).get("registry_snapshot_id"),
        "locks": (snap or {}).get("locks"),
        "hashes": {
            "canon_lock_sha256": sha256_file(canon_p),
            "protocol_lock_sha256": sha256_file(prot_p),
            "registry_snapshot_sha256": sha256_file(snap_p) if snap_p.exists() else None,
        },
        "locked": {
            "pi": dstr(pi),
            "D_anch_m": dstr(D_anch),
            "r_p_m": dstr(r_p),
            "delta_mode": delta_mode,
        },
        "derived": {
            "delta": dstr(delta),
            "s_p_dimless": dstr(s_p),
            "nu_p_can_s_inv": dstr(nu),
        },
        "interpretive": {
            "N_act_floor": N_act,
            "eps": dstr(eps),
        },
        "hypothesis_candidate_mapping": {
            "N_core": N_core,
            "points_per": points_per,
            "N_static_q": N_static_q,
            "N_cap": N_cap,
            "N_static": N_static,
            "N_active_points": N_active_points,
        },
        "notes": [
            "N_act/eps decomposition is an interpretive (NON-LOCK) layer on top of Section 9.4.",
            "The 82*4 - 9*4 mapping is a candidate discrete interpretation; meanings must be locked before it can become a gated claim.",
        ],
    }

    text = json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True) + "
"
    if args.write:
        Path(args.write).write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
