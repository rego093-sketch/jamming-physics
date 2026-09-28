"""Metric estimators for the jet_regime reference stub.

These are toy metrics meant to provide deterministic outputs that match the
whitepaper's module-structure promises (§17.2). They are NOT physical claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


def normalize(v: Tuple[float,float,float]) -> Tuple[float,float,float]:
    x,y,z=v
    n=math.sqrt(x*x+y*y+z*z)
    if n==0.0:
        return (0.0,0.0,1.0)
    return (x/n,y/n,z/n)


def dot(a: Tuple[float,float,float], b: Tuple[float,float,float]) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def angle(a: Tuple[float,float,float], b: Tuple[float,float,float]) -> float:
    c = max(-1.0, min(1.0, dot(normalize(a), normalize(b))))
    return math.acos(c)


@dataclass(frozen=True)
class JetMetrics:
    J: float
    dJ: Tuple[float,float,float]
    theta_J: float
    P_J: float
    M_J: float


def compute_axis(events: List[Dict[str,float]]) -> Tuple[float,float,float]:
    sx=sy=sz=0.0
    for e in events:
        w=float(e.get('flux',1.0))
        sx += w*float(e['dx'])
        sy += w*float(e['dy'])
        sz += w*float(e['dz'])
    return normalize((sx,sy,sz))


def compute_metrics(events: List[Dict[str,float]], q_star: float = 0.7, theta_star: float = 0.35) -> JetMetrics:
    if not events:
        return JetMetrics(J=float('nan'), dJ=(0.0,0.0,1.0), theta_J=float('nan'), P_J=float('nan'), M_J=float('nan'))

    axis = compute_axis(events)
    total_flux = sum(float(e.get('flux',1.0)) for e in events)

    # Collimation: fraction of flux within theta_star of axis.
    in_flux = 0.0
    angles=[]
    for e in events:
        d=(float(e['dx']), float(e['dy']), float(e['dz']))
        th = angle(axis, d)
        angles.append(th)
        if th <= theta_star:
            in_flux += float(e.get('flux',1.0))

    J = 0.0 if total_flux==0.0 else in_flux/total_flux

    # Width: q_star quantile of angle distribution.
    angles_sorted = sorted(angles)
    k = max(0, min(len(angles_sorted)-1, int(q_star*(len(angles_sorted)-1))))
    theta_J = angles_sorted[k]

    # Persistence/stability: stub as 1.0 (single-window toy)
    P_J = 1.0
    M_J = 1.0

    return JetMetrics(J=J, dJ=axis, theta_J=theta_J, P_J=P_J, M_J=M_J)


def to_json(m: JetMetrics) -> Dict[str, float]:
    return {
        'J': m.J,
        'dJ_x': m.dJ[0],
        'dJ_y': m.dJ[1],
        'dJ_z': m.dJ[2],
        'theta_J': m.theta_J,
        'P_J': m.P_J,
        'M_J': m.M_J,
    }
