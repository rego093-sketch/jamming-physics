"""Metric estimators for the rot_aniso reference stub.

These estimators are *toy* definitions used to provide deterministic metrics and
Gate examples. They are NOT experimental claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


def g_of_mu(mu: float, chi_rot: float) -> float:
    """Toy anisotropy function g(mu; chi_rot).

    The paper (§17.1) requires a locked coupling form; this stub uses a simple
    polynomial form that is deterministic and smooth.
    """
    g0 = 1.0 + mu * mu
    g1 = mu
    return g0 + chi_rot * g1


def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def std(xs: List[float]) -> float:
    if not xs:
        return float("nan")
    m = mean(xs)
    return math.sqrt(mean([(x - m) ** 2 for x in xs]))


def normalize(v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    x, y, z = v
    n = math.sqrt(x * x + y * y + z * z)
    if n == 0.0:
        return (1.0, 0.0, 0.0)
    return (x / n, y / n, z / n)


def dot(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@dataclass(frozen=True)
class RotAnisoMetrics:
    beta_g: float
    A_parallel: float
    A_perp: float
    Delta_bb: float


def compute_metrics(
    axis_u: Tuple[float, float, float],
    chi_rot: float,
    directions: List[Tuple[float, float, float]],
) -> RotAnisoMetrics:
    """Compute toy metrics from a list of directions."""
    u = normalize(axis_u)
    mus = [max(-1.0, min(1.0, dot(u, d))) for d in directions]
    gs = [g_of_mu(mu, chi_rot) for mu in mus]

    # Toy anisotropy magnitude
    m_g = mean(gs)
    beta_g = 0.0 if m_g == 0 else std(gs) / abs(m_g)

    # Response proxy A(d): larger when aligned with axis (toy)
    As = [1.0 / (1.0 + abs(chi_rot) * (1.0 - abs(mu))) for mu in mus]

    # Split into parallel/perp using |mu| threshold
    par = [A for A, mu in zip(As, mus) if abs(mu) >= 0.7]
    perp = [A for A, mu in zip(As, mus) if abs(mu) <= 0.3]
    A_parallel = mean(par) if par else float("nan")
    A_perp = mean(perp) if perp else float("nan")

    # Backbone change: stubbed to 0 (no graph in this toy)
    Delta_bb = 0.0

    return RotAnisoMetrics(beta_g=beta_g, A_parallel=A_parallel, A_perp=A_perp, Delta_bb=Delta_bb)


def to_json(metrics: RotAnisoMetrics) -> Dict[str, float]:
    return {
        "beta_g": metrics.beta_g,
        "A_parallel": metrics.A_parallel,
        "A_perp": metrics.A_perp,
        "Delta_bb": metrics.Delta_bb,
    }
