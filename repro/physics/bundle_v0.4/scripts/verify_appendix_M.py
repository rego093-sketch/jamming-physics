#!/usr/bin/env python3
"""Deterministic verifier for Appendix M (mass unification invariants).

This file exists because the whitepaper TeX embeds it as a named artifact.

Computes, from LOCK inputs only:
  - U_lat, m_H, m_p, m_e
  - I_H, I_p, I_e
  - dev_max and a Gate verdict using dev_tol_max from gate_lock

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
    gate_p = root / "registry" / "gate_lock.json"
    snap_p = root / "registry" / "registry_snapshot.json"

    canon = read_json(canon_p)
    realz = read_json(realz_p)
    prot = read_json(prot_p)
    gate = read_json(gate_p)
    snap = read_json(snap_p) if snap_p.exists() else None

    # [LOCK]
    pi = d(canon["constants"]["pi"])
    h = d(canon["constants"].get("h_J_s") or canon["constants"].get("h_Js") or "6.62607015e-34")

    c_ref = d(realz["inputs"]["c_ref_m_s"])
    a_m = d(realz["inputs"]["a_m"])

    r_p = d(canon["inputs"]["r_p_m"])
    D_anch = d(canon["inputs"]["D_anch_m"])

    GeV_to_J = d(
        prot.get("unit_conversions", {}).get("GeV_to_J")
        or prot.get("unit_conventions", {}).get("GeV_to_J")
    )

    delta = Decimal(1) / (pi * pi)

    # [DERIVED]
    U_lat_J = (h * c_ref) / a_m
    U_lat_GeV = U_lat_J / GeV_to_J

    m_H = U_lat_GeV / (Decimal(5) * pi)

    lambda_C = (pi / Decimal(2)) * r_p
    S_p = lambda_C / a_m
    m_p = U_lat_GeV / S_p

    # Electron channel on its Compton length (lambda_C,e = D_anch/2).
    # The earlier r_e = (D_anch/2)*delta form was retracted: it gives m_e = pi^2 * 0.511 MeV
    # (5.04 MeV) and still passed, because I_e = m_e*S/U_lat is 1 by construction.
    lambda_Ce = D_anch / Decimal(2)
    S = lambda_Ce / a_m
    m_e = U_lat_GeV / S
    # D_anch := 2*lambda_C,e, so m_e = hc/lambda_C,e is a round trip; this check only catches a
    # wrong electron channel (such as the retracted pi^2 form) or a mis-locked D_anch. It is not a prediction.
    m_e_ref_GeV = Decimal("0.51099895069e-3")  # CODATA 2022
    e_rel = abs(m_e - m_e_ref_GeV) / m_e_ref_GeV

    I_H = (m_H * (Decimal(5) * pi)) / U_lat_GeV
    I_p = (m_p * S_p) / U_lat_GeV
    I_e = (m_e * S) / U_lat_GeV

    dev_max = max(abs(I_H - 1), abs(I_p - 1), abs(I_e - 1))
    # I_* are identities by definition; the external electron check is what can fail.
    e_check_tol = Decimal("1e-3")

    dev_tol = d(
        gate.get("tolerances", {}).get(
            "dev_tol_max",
            gate.get("thresholds", {}).get("numeric_rel_tol_default", "1e-12"),
        )
    )

    status = "PASS" if (dev_max <= dev_tol and e_rel <= e_check_tol) else "FAIL"

    out: Dict[str, Any] = {
        "script": "verify_appendix_M.py",
        "scope": "Appendix M (mass unification invariants)",
        "registry_snapshot_id": (snap or {}).get("registry_snapshot_id"),
        "locks": (snap or {}).get("locks"),
        "hashes": {
            "canon_lock_sha256": sha256_file(canon_p),
            "realization_lock_sha256": sha256_file(realz_p),
            "protocol_lock_sha256": sha256_file(prot_p),
            "gate_lock_sha256": sha256_file(gate_p),
            "registry_snapshot_sha256": sha256_file(snap_p) if snap_p.exists() else None,
        },
        "locked": {
            "pi": dstr(pi),
            "h_J_s": dstr(h),
            "c_ref_m_s": dstr(c_ref),
            "a_m": dstr(a_m),
            "r_p_m": dstr(r_p),
            "D_anch_m": dstr(D_anch),
            "GeV_to_J": dstr(GeV_to_J),
            "dev_tol_max": dstr(dev_tol),
        },
        "derived": {
            "U_lat_GeV": dstr(U_lat_GeV),
            "m_H_GeV": dstr(m_H),
            "m_p_GeV": dstr(m_p),
            "m_e_GeV": dstr(m_e),
            "lambda_C_m": dstr(lambda_C),
            "S_p_dimless": dstr(S_p),
            "lambda_Ce_m": dstr(lambda_Ce),
            "m_e_vs_CODATA_rel": dstr(e_rel),
            "S_dimless": dstr(S),
            "I_H": dstr(I_H),
            "I_p": dstr(I_p),
            "I_e": dstr(I_e),
            "dev_max": dstr(dev_max),
        },
        "gate_eval": {
            "gate_id": "G-RATIO-MASS-UNIFICATION",
            "status": status,
        },
        "notes": [
            "All values are derived deterministically from registry locks.",
            "This Gate is an internal consistency check of definitions (Appendix M).",
        ],
    }

    text = json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.write:
        Path(args.write).write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
