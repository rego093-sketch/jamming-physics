"""Toy event-flux extractor for the jet_regime reference stub.

In the full framework this would read link-event logs and map them to an
observational cone/cylinder. Here we simply generate deterministic synthetic
"events" with a direction vector and a positive flux weight.
"""

from __future__ import annotations

import math
from typing import List, Dict, Tuple


def random_unit_vector(rng) -> Tuple[float, float, float]:
    u = rng.rand()
    v = rng.rand()
    theta = 2.0 * math.pi * u
    z = 2.0 * v - 1.0
    r = math.sqrt(max(0.0, 1.0 - z*z))
    return (r*math.cos(theta), r*math.sin(theta), z)


def generate_events(rng, n_steps: int) -> List[Dict[str, float]]:
    events = []
    for _ in range(n_steps):
        x,y,z = random_unit_vector(rng)
        # Toy positive flux: biased toward +z to mimic collimation when seed fixed.
        w = 1.0 + 0.5*max(0.0, z)
        events.append({"dx": x, "dy": y, "dz": z, "flux": w})
    return events
