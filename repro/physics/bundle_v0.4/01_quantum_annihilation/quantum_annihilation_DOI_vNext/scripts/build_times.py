#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_times.py
- 목적: 정준 ν_p로 Tp=89/ν_p, Tn=82/ν_p 계산(14장 결과를 스크립트로 봉인)
- 주의: ν_p는 관측치가 아니라 canon_derived.json에서 읽는다.
"""

from __future__ import annotations
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 80

def D(x) -> Decimal:
    return Decimal(str(x))

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    root = Path(__file__).resolve().parents[1]
    der = load_json(root / "LOCK" / "canon_derived.json")
    nu_p = Decimal(der["nu_p_per_s"])

    Np, Nn = 89, 82
    Tp = Decimal(Np) / nu_p
    Tn = Decimal(Nn) / nu_p

    print("nu_p =", nu_p)
    print("Tp   =", Tp, "s")
    print("Tn   =", Tn, "s")
    print("Tp/Tn=", Tp / Tn)

if __name__ == "__main__":
    main()
