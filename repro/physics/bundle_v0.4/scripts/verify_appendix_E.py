#!/usr/bin/env python3
"""Deterministic verifier for Appendix E (electron mass chain).

This file exists because the whitepaper TeX embeds it as a named artifact.
It is *not* a physics "validation"; it is a reproducible computation trace
from LOCK inputs.

Computes (from registry locks only):
  - delta (default universal: 1/pi^2)
  - U_lat := h*c_ref/a
  - r_e := (D_anch/2)*delta
  - S := r_e/a
  - m_e := U_lat/S

Outputs a JSON object to stdout (and optionally to --write).
All numeric values are stored as decimal strings for cross-platform
reproducibility.
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
    D_anch = d(canon["inputs"]["D_anch_m"])

    GeV_to_J = d(
        prot.get("unit_conversions", {}).get("GeV_to_J")
        or prot.get("unit_conventions", {}).get("GeV_to_J")
    )

    # delta: either explicit numeric or derived universal rule 1/pi^2
    delta_item = canon.get("constants", {}).get("delta_rect", "1/pi^2")
    if isinstance(delta_item, (int, float)):
        delta = d(delta_item)
        delta_mode = "numeric"
    else:
        # Treat any non-numeric form as the universal regime unless explicitly overridden.
        delta = Decimal(1) / (pi * pi)
        delta_mode = "universal_1_over_pi_sq"

    # [DERIVED]
    U_lat_J = (h * c_ref) / a_m
    U_lat_GeV = U_lat_J / GeV_to_J

    r_e = (D_anch / Decimal(2)) * delta
    S = r_e / a_m
    m_e_GeV = U_lat_GeV / S

    out: Dict[str, Any] = {
        "script": "verify_appendix_E.py",
        "scope": "Appendix E (electron mass)",
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
            "D_anch_m": dstr(D_anch),
            "GeV_to_J": dstr(GeV_to_J),
            "delta_mode": delta_mode,
        },
        "derived": {
            "delta": dstr(delta),
            "U_lat_J": dstr(U_lat_J),
            "U_lat_GeV": dstr(U_lat_GeV),
            "r_e_m": dstr(r_e),
            "S_dimless": dstr(S),
            "m_e_GeV": dstr(m_e_GeV),
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
