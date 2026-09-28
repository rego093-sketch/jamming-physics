"""How surprising is m_p/m_e ~ 6 pi^5? A transparent look-elsewhere estimate.

Grammar (fixed before looking at other constants): n * pi^k with integer n in 1..12 and
integer k in -6..8. Tolerance: the observed relative residual of 6 pi^5 (18.8 ppm).
We count how many members of the grammar land within that tolerance of the measured
ratio, and how large a fraction of log-space [1, 1e4] the grammar covers at that tolerance.
That fraction is the chance that an arbitrary number of this size would be hit by luck.
"""
import math

TARGET = 1836.152673426          # CODATA 2022 m_p/m_e
VALUE = 6 * math.pi ** 5
TOL = abs(VALUE / TARGET - 1)

members = [(n, k, n * math.pi ** k) for n in range(1, 13) for k in range(-6, 9)]
hits = [(n, k) for n, k, v in members if abs(v / TARGET - 1) <= TOL * 1.000001]
in_range = [v for n, k, v in members if 1 <= v <= 1e4]
p_luck = len(in_range) * 2 * TOL / math.log(1e4)

print(f"6 pi^5 = {VALUE:.6f}   measured = {TARGET}   residual = {VALUE / TARGET - 1:+.3e}")
print(f"grammar members hitting within {TOL:.2e}: {hits}")
print(f"grammar members in [1, 1e4]: {len(in_range)}   chance of a lucky hit: {p_luck:.1e}")
