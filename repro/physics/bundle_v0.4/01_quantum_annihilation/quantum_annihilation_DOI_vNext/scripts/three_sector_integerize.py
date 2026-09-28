#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
three_sector_integerize.py
- 목적: 120° 3-섹터 최소분산 정수화(14장) 구현
- 규칙:
  N=3m   -> (m,m,m)
  N=3m+1 -> (m+1,m,m)
  N=3m+2 -> (m+1,m+1,m)
- 보조: |V|^2 = (3/2) Σ n_i^2 - (1/2) N^2  (120° 벡터 합의 제곱)
"""

from __future__ import annotations
from typing import Tuple

def integerize_3sector(N: int) -> Tuple[int, int, int]:
    if N < 0:
        raise ValueError("N must be >= 0")
    m, r = divmod(N, 3)
    if r == 0:
        return (m, m, m)
    if r == 1:
        return (m+1, m, m)
    return (m+1, m+1, m)

def V2(n1: int, n2: int, n3: int) -> int:
    N = n1 + n2 + n3
    return int( (3*(n1*n1 + n2*n2 + n3*n3) - (N*N)) // 2 )

def main():
    for N in [89, 82, 90, 91]:
        n1,n2,n3 = integerize_3sector(N)
        print(f"N={N} -> (n1,n2,n3)=({n1},{n2},{n3}), |V|^2={V2(n1,n2,n3)}")

if __name__ == "__main__":
    main()
