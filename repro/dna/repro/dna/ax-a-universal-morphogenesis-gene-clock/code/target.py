"""
target.py -- a TARGET is a real entity captured as 3D coordinates: a signed-distance
field T(x) plus semantic landmarks. This is the "scan" the form must grow to.

Two providers, one interface:
  * face_target()   -- an analytic human head/face (stand-in for a real face scan;
                       a real point-cloud scan would replace sdf_target() identically).
  * animal_target() -- reuse the developmental body builder as a target silhouette,
                       so the same growth code reaches any animal we can describe.

A target exposes:
  .sample(P)  -> signed distance on a coord array (neg inside)
  .landmarks  -> {name: (x,y,z)}  semantic anchor coordinates
  .box        -> (Lx,Ly,Lz) suggested voxel extent
"""
import numpy as np
import body as B


def _ellipsoid(P, c, r):
    """IQ approximate ellipsoid SDF (neg inside). c,r length-3."""
    c = np.asarray(c, float); r = np.asarray(r, float)
    p = P - c
    q = p / r
    k0 = np.sqrt(np.einsum("...k,...k->...", q, q))
    k1 = np.sqrt(np.einsum("...k,...k->...", q / r, q / r))
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


class Target:
    def __init__(self, sdf_fn, landmarks, box, name):
        self._sdf = sdf_fn; self.landmarks = landmarks; self.box = box; self.name = name
    def sample(self, P):
        return self._sdf(P)


# ---------------------------------------------------------------- human face target
def face_target():
    """Analytic human head: cranium+jaw egg, nose, brow, eye bulges, cheeks, ears, lips,
    chin. Front = +z, up = +y, right = +x. Units: head height ~ 30."""
    k = 1.6  # smin blend
    parts = [
        ("ell", (0.0, 6.0, -1.0), (10.5, 12.5, 11.5)),   # cranium (tall, deep)
        ("ell", (0.0, -5.0, 2.0), (7.5, 9.0, 8.5)),      # face / jaw (forward, narrower)
        ("ell", (0.0, -10.5, 4.5), (3.6, 3.4, 4.2)),     # chin
        ("ell", (-5.2, -2.5, 6.0), (4.2, 4.6, 4.2)),     # cheek L
        ("ell", (5.2, -2.5, 6.0), (4.2, 4.6, 4.2)),      # cheek R
        ("ell", (0.0, 3.2, 8.2), (8.0, 1.7, 3.0)),       # brow ridge
        ("cone", (0.0, 1.0, 8.5), (0.0, -4.5, 11.6), 2.0, 1.1),  # nose bridge->tip
        ("ell", (0.0, -5.2, 9.6), (1.9, 1.2, 1.6)),      # nose tip ball
        ("ell", (-1.7, -5.6, 9.0), (1.3, 1.0, 1.4)),     # left nostril wing
        ("ell", (1.7, -5.6, 9.0), (1.3, 1.0, 1.4)),      # right nostril wing
        ("ell", (-3.9, 2.0, 8.6), (2.3, 1.8, 2.0)),      # eye bulge L
        ("ell", (3.9, 2.0, 8.6), (2.3, 1.8, 2.0)),       # eye bulge R
        ("ell", (0.0, -7.6, 8.6), (3.1, 1.4, 2.1)),      # lips
        ("ell", (-10.6, 1.5, -0.5), (1.3, 4.2, 3.4)),    # ear L (flat in x)
        ("ell", (10.6, 1.5, -0.5), (1.3, 4.2, 3.4)),     # ear R
    ]
    def sdf(P):
        d = None
        for pr in parts:
            if pr[0] == "ell":
                di = _ellipsoid(P, pr[1], pr[2])
            else:
                _, a, b, ra, rb = pr
                di = B.sdf_round_cone(P, a, b, ra, rb)
            d = di if d is None else B.smin(d, di, k)
        return d
    lm = {
        "crown": (0, 18, 0), "glabella": (0, 4, 9), "nasion": (0, 1.5, 9),
        "nose_tip": (0, -5.2, 11.4), "subnasale": (0, -6.0, 9.5),
        "mouth": (0, -7.6, 10.0), "chin": (0, -11.5, 6.0),
        "eye_L": (-3.9, 2.0, 10.0), "eye_R": (3.9, 2.0, 10.0),
        "cheek_L": (-5.5, -2.5, 9.0), "cheek_R": (5.5, -2.5, 9.0),
        "ear_L": (-11.5, 1.5, -1.0), "ear_R": (11.5, 1.5, -1.0),
    }
    return Target(sdf, lm, box=(34.0, 44.0, 34.0), name="human_face")


# ---------------------------------------------------------------- animal target (reuse body)
def animal_target(tau=1.0, reg=None):
    """Use the developmental body itself as a target field, so growth code can reach any
    animal the engine can describe. Returns a Target backed by the body SDF (neg inside)."""
    import assemble as A
    if reg is None:
        reg = A.D.emergent_registers()
    bp, m = A.build_body(tau, reg)
    L = m["axis_len"]
    def sdf(P):
        return bp.field(P)            # body SDF, neg inside
    lm = {"head": (-L/2 + reg["head_end"]*L*0.5, 0, 0),
          "tail_tip": (L/2, 0, 0),
          "forelimb": (A._u_to_x(reg["forelimb"], L), 0, 0),
          "hindlimb": (A._u_to_x(reg["hindlimb"], L), 0, 0)}
    return Target(sdf, lm, box=(1.32*L, 0.66*L, 0.62*L), name="salamander")
