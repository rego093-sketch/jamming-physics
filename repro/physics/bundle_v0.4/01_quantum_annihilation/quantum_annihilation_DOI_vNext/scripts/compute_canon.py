#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_canon.py
- 목적: LOCK/canon_lock.json에서 파생 정준값을 *결정론적으로* 계산하여 LOCK/canon_derived.json에 저장.
- 특징:
  1) Decimal 고정 정밀도 사용
  2) π를 문자열로 고정(플랫폼별 math.pi 차이 방지)
  3) 결과를 관측치로 역보정하지 않음(무피팅)
"""

from __future__ import annotations
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 80

PI_STR = "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
PI = Decimal(PI_STR)

def D(x) -> Decimal:
    # JSON float를 문자열로 감싸면 Decimal 변환이 안정적
    return Decimal(str(x))

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    canon_path = root / "LOCK" / "canon_lock.json"
    canon = load_json(canon_path)

    D_anch = D(canon["D_anch_m"])
    r_p    = D(canon["r_p_m"])

    delta = Decimal(1) / (PI * PI)          # δ = 1/π²
    r0    = D_anch / Decimal(2)             # r0 = D_anch/2
    s_p   = r0 / r_p                         # s_p = r0/r_p
    nu_p  = s_p * delta                      # ν_p = s_p δ

    r_e   = D_anch / (Decimal(2) * PI * PI) # r_e = D_anch/(2π²)
    s_e   = r0 / r_e                         # s_e = π²
    nu_e  = s_e * delta                      # ν_e = 1 (항등)

    out = {
        "pi_str": PI_STR,
        "D_anch_m": str(D_anch),
        "r_p_m": str(r_p),
        "r0_m": str(r0),
        "delta_1_over_pi2": str(delta),
        "s_p": str(s_p),
        "nu_p_per_s": str(nu_p),
        "r_e_m": str(r_e),
        "s_e": str(s_e),
        "nu_e_per_s": str(nu_e),
        "notes": "Derived deterministically from canon_lock.json (no fitting)."
    }

    save_json(root / "LOCK" / "canon_derived.json", out)

    print("=== CANON DERIVED ===")
    for k in ["D_anch_m","r_p_m","r0_m","delta_1_over_pi2","s_p","nu_p_per_s","r_e_m","s_e","nu_e_per_s"]:
        print(f"{k} = {out[k]}")

if __name__ == "__main__":
    main()
