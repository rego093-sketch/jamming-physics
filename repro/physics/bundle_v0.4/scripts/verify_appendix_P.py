#!/usr/bin/env python3
"""Deterministic verifier for Appendix P (proton mass chain).

This file exists because the whitepaper TeX embeds it as a named artifact.
It computes lambda_C, S_p, and m_p from LOCK inputs only.

Outputs a JSON object to stdout (and optionally to --write).
All numeric values are stored as decimal strings.
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
    realz_p = root / "registry" / "realization_lock.json"
    prot_p = root / "registry" / "protocol_lock.json"
    snap_p = root / "registry" / "registry_snapshot.json"

    canon = read_json(canon_p)
    realz = read_json(realz_p)
    prot = read_json(prot_p)
    snap = read_json(snap_p) if snap_p.exists() else None

    # [LOCK] constants
    pi = d(canon["constants"]["pi"])
    h = d(canon["constants"].get("h_J_s") or canon["constants"].get("h_Js") or "6.62607015e-34")

    c_ref = d(realz["inputs"]["c_ref_m_s"])
    a_m = d(realz["inputs"]["a_m"])
    r_p = d(canon["inputs"]["r_p_m"])

    GeV_to_J = d(
        prot.get("unit_conversions", {}).get("GeV_to_J")
        or prot.get("unit_conventions", {}).get("GeV_to_J")
    )

    # [DERIVED]
    U_lat_J = (h * c_ref) / a_m
    U_lat_GeV = U_lat_J / GeV_to_J

    lambda_C = (pi / Decimal(2)) * r_p
    S_p = lambda_C / a_m
    m_p_GeV = U_lat_GeV / S_p

    out: Dict[str, Any] = {
        "script": "verify_appendix_P.py",
        "scope": "Appendix P (proton mass)",
        "registry_snapshot_id": (snap or {}).get("registry_snapshot_id"),
        "locks": (snap or {}).get("locks"),
        "hashes": {
            "canon_lock_sha256": sha256_file(canon_p),
            "realization_lock_sha256": sha256_file(realz_p),
            "protocol_lock_sha256": sha256_file(prot_p),
            "registry_snapshot_sha256": sha256_file(snap_p) if snap_p.exists() else None,
        },
        "locked": {
            "pi": dstr(pi),
            "h_J_s": dstr(h),
            "c_ref_m_s": dstr(c_ref),
            "a_m": dstr(a_m),
            "r_p_m": dstr(r_p),
            "GeV_to_J": dstr(GeV_to_J),
        },
        "derived": {
            "U_lat_J": dstr(U_lat_J),
            "U_lat_GeV": dstr(U_lat_GeV),
            "lambda_C_m": dstr(lambda_C),
            "S_p_dimless": dstr(S_p),
            "m_p_GeV": dstr(m_p_GeV),
        },
        "notes": [
            "All values are derived deterministically from registry locks.",
            "This log is intended for reproducibility tracing, not experimental validation.",
        ],
    }

    text = json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.write:
        Path(args.write).write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
