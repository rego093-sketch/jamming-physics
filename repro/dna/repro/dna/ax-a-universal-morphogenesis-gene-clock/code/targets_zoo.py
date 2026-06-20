"""targets_zoo.py -- a few analytic animal targets (stand-ins for scans) so the SAME
grow() engine can be shown reaching many body plans. Each is an SDF + landmarks."""
import numpy as np
import body as B
from target import Target, _ellipsoid


def _union(parts, k=1.4):
    def sdf(P):
        d = None
        for pr in parts:
            if pr[0] == "ell":
                di = _ellipsoid(P, pr[1], pr[2])
            elif pr[0] == "cone":
                di = B.sdf_round_cone(P, pr[1], pr[2], pr[3], pr[4])
            else:  # blade
                _, x0, x1, top, bot, zc, th = pr
                di = B.sdf_slab_blade(P, x0, x1, zc, th, top, bot)
            d = di if d is None else B.smin(d, di, k)
        return d
    return sdf


def quadruped_target():
    """dog/horse-like: horizontal trunk, neck, head, 4 legs, tail."""
    parts = [
        ("cone", (-26, 6, 0), (16, 7, 0), 6.5, 7.5),    # trunk
        ("cone", (16, 8, 0), (28, 15, 0), 4.5, 3.0),    # neck up
        ("ell", (31, 17, 0), (5.5, 4.0, 4.0)),          # head
        ("cone", (33, 16, 0), (39, 15, 0), 2.4, 1.8),   # muzzle
        ("ell", (29, 21, 2.5), (1.5, 2.2, 1.0)),        # ear L
        ("ell", (29, 21, -2.5), (1.5, 2.2, 1.0)),       # ear R
        ("cone", (-30, 5, 0), (-40, 12, 0), 2.2, 1.0),  # tail
    ]
    for sx in (-22, 10):                                  # fore/hind leg pairs
        for sz in (-4.5, 4.5):
            parts.append(("cone", (sx, 2, sz), (sx, -16, sz), 2.6, 1.8))
            parts.append(("ell", (sx + 2, -16, sz), (3.0, 1.5, 2.0)))   # paw
    lm = {"nose": (40, 15, 0), "head": (31, 17, 0), "tail": (-40, 12, 0)}
    return Target(_union(parts), lm, box=(96, 50, 30), name="quadruped")


def fish_target():
    """streamlined body + caudal + dorsal fins."""
    parts = [
        ("ell", (0, 0, 0), (22, 9, 5)),                 # body
        ("cone", (18, 0, 0), (28, 0, 0), 4.0, 1.0),     # caudal peduncle
        ("blade", 26, 36, 9, -9, 0.0, 1.2),             # tail fin
        ("blade", -6, 12, 12, 1, 0.0, 1.0),             # dorsal fin
        ("ell", (-19, 1, 0), (4, 5, 4)),                # head
        ("ell", (-17, 2, 3.6), (1.3, 1.3, 1.0)),        # eye R
        ("ell", (-17, 2, -3.6), (1.3, 1.3, 1.0)),       # eye L
    ]
    lm = {"snout": (-23, 1, 0), "tail": (36, 0, 0)}
    return Target(_union(parts, k=1.2), lm, box=(80, 32, 16), name="fish")


def bird_target():
    """body + head + beak + folded wings + tail."""
    parts = [
        ("ell", (0, 0, 0), (12, 9, 7)),                 # body
        ("cone", (8, 6, 0), (15, 13, 0), 3.5, 2.6),     # neck
        ("ell", (17, 15, 0), (3.6, 3.4, 3.2)),          # head
        ("cone", (19, 15, 0), (25, 14, 0), 1.4, 0.5),   # beak
        ("blade", -10, 6, 7, -7, 6.5, 1.0),             # wing R (z+)
        ("blade", -10, 6, 7, -7, -6.5, 1.0),            # wing L (z-)
        ("cone", (-10, 0, 0), (-22, -4, 0), 3.0, 1.0),  # tail
        ("cone", (2, -8, 2.5), (2, -16, 2.5), 1.3, 0.9),# leg R
        ("cone", (2, -8, -2.5), (2, -16, -2.5), 1.3, 0.9),# leg L
    ]
    lm = {"beak": (25, 14, 0), "head": (17, 15, 0), "tail": (-22, -4, 0)}
    return Target(_union(parts, k=1.3), lm, box=(56, 44, 20), name="bird")


ZOO = {"quadruped": quadruped_target, "fish": fish_target, "bird": bird_target}
