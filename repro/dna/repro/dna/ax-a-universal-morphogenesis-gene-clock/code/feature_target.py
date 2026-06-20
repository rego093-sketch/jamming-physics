"""
feature_target.py -- a TARGET whose surface is a set of NAMED features, each tagged with a
master gene, each able to GROW from nothing (a nub seated on the body envelope) up to full
size. This is what lets gene_clock schedule feature emergence: the field at developmental
time tau is the smin of the always-present base (cranium+jaw envelope) and each feature
scaled by its gene's a_f(tau).

The face is the same analytic human head used by target.face_target(), refactored so each
ellipsoid/cone is a GROWABLE, GENE-TAGGED part. The gene map (real measured gamma per gene
in data/sensory_organ_gamma.json):

  feature group     master gene   confidence
  ---------------   -----------   ----------------------------------------------------
  eyes              PAX6          [V] master (the eye master gene)
  ears              PAX2          [V] master (otic placode)
  nose (+nostrils)  LHX2          [V] master (olfactory placode)
  skin envelope     TP63          [V] master (epidermis)            -- the base, earliest
  cranium (+brow)   FOXG1         [F] representative (forebrain underlies the vault)
  jaw/chin/midline  SHH           [F] representative (patterns the facial midline/mandible)
  cheeks            MYOD1         [F] representative (facial musculature)
  lips/mouth        POU2F3        [F] representative (oral/taste field)

The sensory masters (eye/ear/nose/skin) are genuine; the structural groups are honestly
labelled representative (neuro "representative, cited" discipline). Swap GENE_MAP / the part
list for any other organism and the same gene_clock + grow_gene_clock work -> general.

A FeatureTarget exposes:
  .sample(P, scales)    signed distance with each feature grown by scales[name] in [0,1]
                        (scales=None or all 1.0 -> the full target = target.face_target()).
  .features             [(name, gene)] in a fixed order
  .feature_box(name)    (center, half) AABB of a feature at full size (per-feature metrics)
  .landmarks, .box, .name
"""
import numpy as np
import body as B
from target import _ellipsoid


def _seat(center, env_c, env_r):
    """Project a feature centre onto the approximate envelope sphere (its growth origin)."""
    v = np.asarray(center, float) - np.asarray(env_c, float)
    n = np.linalg.norm(v)
    return np.asarray(env_c, float) + (env_r / n) * v if n > 1e-6 else np.asarray(env_c, float)


def _ell_grown(P, center, r, scale, env_c, env_r):
    """Ellipsoid that grows from a nub on the envelope (scale~0) to full (scale=1):
    centre lerps seat->true, radii scale up. eps keeps it a tiny solid, not empty."""
    s = max(float(scale), 1e-3)
    seat = _seat(center, env_c, env_r)
    c = (1.0 - s) * seat + s * np.asarray(center, float)
    return _ellipsoid(P, c, np.asarray(r, float) * s)


def _cone_grown(P, a, b, ra, rb, scale, env_c, env_r):
    s = max(float(scale), 1e-3)
    sa, sb = _seat(a, env_c, env_r), _seat(b, env_c, env_r)
    aa = (1.0 - s) * sa + s * np.asarray(a, float)
    bb = (1.0 - s) * sb + s * np.asarray(b, float)
    return B.sdf_round_cone(P, aa, bb, ra * s, rb * s)


class FeatureTarget:
    def __init__(self, base_parts, feature_parts, landmarks, box, name, k=1.6,
                 env_c=(0.0, 0.0, 2.0), env_r=9.0):
        self.base = base_parts            # [(kind, *args)] always full
        self.parts = feature_parts        # [dict(name, gene, kind, *geom)]
        self.landmarks = landmarks
        self.box = box
        self.name = name
        self.k = k
        self.env_c = np.asarray(env_c, float)
        self.env_r = float(env_r)
        self.features = [(p["name"], p["gene"]) for p in self.parts]

    def _part_sdf(self, P, p, scale):
        if p["kind"] == "ell":
            return _ell_grown(P, p["c"], p["r"], scale, self.env_c, self.env_r)
        return _cone_grown(P, p["a"], p["b"], p["ra"], p["rb"], scale, self.env_c, self.env_r)

    def sample(self, P, scales=None):
        d = None
        for bp in self.base:                       # base envelope, always full
            di = _ellipsoid(P, bp[1], bp[2])
            d = di if d is None else B.smin(d, di, self.k)
        for p in self.parts:
            s = 1.0 if scales is None else float(scales.get(p["name"], 1.0))
            di = self._part_sdf(P, p, s)
            d = di if d is None else B.smin(d, di, self.k)
        return d

    def feature_box(self, name):
        for p in self.parts:
            if p["name"] == name:
                if p["kind"] == "ell":
                    c = np.asarray(p["c"], float); h = np.asarray(p["r"], float) * 1.6
                else:
                    a = np.asarray(p["a"], float); b = np.asarray(p["b"], float)
                    c = 0.5 * (a + b); h = np.abs(b - a) * 0.6 + max(p["ra"], p["rb"]) * 1.6
                return c, h
        return None


# --------------------------------------------------------------------- the human face
def face_features():
    """The analytic human head as growable, gene-tagged features (same geometry as
    target.face_target(); sample(scales=None) reproduces it)."""
    base = [
        ("ell", (0.0, 6.0, -1.0), (10.5, 12.5, 11.5)),   # cranium shell (envelope)
        ("ell", (0.0, -5.0, 2.0), (7.5, 9.0, 8.5)),      # face/jaw shell (envelope)
    ]
    P = [
        dict(name="cranium", gene="FOXG1", kind="ell",
             c=(0.0, 7.0, 0.0), r=(9.5, 10.5, 9.5)),                       # vault fill (brow folded in)
        dict(name="brow",    gene="FOXG1", kind="ell",
             c=(0.0, 3.2, 8.2), r=(8.0, 1.7, 3.0)),
        dict(name="jaw",     gene="SHH",   kind="ell",
             c=(0.0, -10.5, 4.5), r=(3.6, 3.4, 4.2)),                      # chin/jaw midline
        dict(name="cheek_L", gene="MYOD1", kind="ell", c=(-5.2, -2.5, 6.0), r=(4.2, 4.6, 4.2)),
        dict(name="cheek_R", gene="MYOD1", kind="ell", c=(5.2, -2.5, 6.0),  r=(4.2, 4.6, 4.2)),
        dict(name="nose",    gene="LHX2",  kind="cone",
             a=(0.0, 1.0, 8.5), b=(0.0, -4.5, 11.6), ra=2.0, rb=1.1),
        dict(name="nose_tip", gene="LHX2", kind="ell", c=(0.0, -5.2, 9.6), r=(1.9, 1.2, 1.6)),
        dict(name="nostril_L", gene="LHX2", kind="ell", c=(-1.7, -5.6, 9.0), r=(1.3, 1.0, 1.4)),
        dict(name="nostril_R", gene="LHX2", kind="ell", c=(1.7, -5.6, 9.0),  r=(1.3, 1.0, 1.4)),
        dict(name="eye_L",   gene="PAX6",  kind="ell", c=(-3.9, 2.0, 8.6), r=(2.3, 1.8, 2.0)),
        dict(name="eye_R",   gene="PAX6",  kind="ell", c=(3.9, 2.0, 8.6),  r=(2.3, 1.8, 2.0)),
        dict(name="lips",    gene="POU2F3", kind="ell", c=(0.0, -7.6, 8.6), r=(3.1, 1.4, 2.1)),
        dict(name="ear_L",   gene="PAX2",  kind="ell", c=(-10.6, 1.5, -0.5), r=(1.3, 4.2, 3.4)),
        dict(name="ear_R",   gene="PAX2",  kind="ell", c=(10.6, 1.5, -0.5),  r=(1.3, 4.2, 3.4)),
    ]
    lm = {
        "crown": (0, 18, 0), "nasion": (0, 1.5, 9), "nose_tip": (0, -5.2, 11.4),
        "mouth": (0, -7.6, 10.0), "chin": (0, -11.5, 6.0),
        "eye_L": (-3.9, 2.0, 10.0), "eye_R": (3.9, 2.0, 10.0),
        "ear_L": (-11.5, 1.5, -1.0), "ear_R": (11.5, 1.5, -1.0),
    }
    return FeatureTarget(base, P, lm, box=(34.0, 44.0, 34.0), name="human_face_genes")


# --------------------------------------------------------------------- gene-tagged animals
# Same atlas, different body plan -> the SAME gene_clock + grow_gene_clock work (generality).
# Sensory masters are genuine (eye=PAX6, ear=PAX2, nose/olfactory=LHX2); axial/appendicular
# groups are representative [F] (trunk/tail=SHH midline; limbs/fins=MYOD1 muscle; head=FOXG1).
def quadruped_features():
    base = [
        ("ell", (-5.0, 6.0, 0.0), (16.0, 7.0, 7.0)),     # trunk shell (envelope)
        ("ell", (28.0, 14.0, 0.0), (7.0, 6.0, 5.0)),     # head shell (envelope)
    ]
    P = [
        dict(name="trunk", gene="SHH",  kind="cone", a=(-26, 6, 0), b=(16, 7, 0), ra=6.5, rb=7.5),
        dict(name="neck",  gene="SHH",  kind="cone", a=(16, 8, 0),  b=(28, 15, 0), ra=4.5, rb=3.0),
        dict(name="head",  gene="FOXG1", kind="ell", c=(31, 17, 0), r=(5.5, 4.0, 4.0)),
        dict(name="muzzle", gene="LHX2", kind="cone", a=(33, 16, 0), b=(39, 15, 0), ra=2.4, rb=1.8),
        dict(name="ear_L", gene="PAX2", kind="ell", c=(29, 21, 2.5),  r=(1.5, 2.2, 1.0)),
        dict(name="ear_R", gene="PAX2", kind="ell", c=(29, 21, -2.5), r=(1.5, 2.2, 1.0)),
        dict(name="eye_L", gene="PAX6", kind="ell", c=(33, 18, 2.6),  r=(1.1, 1.1, 0.9)),
        dict(name="eye_R", gene="PAX6", kind="ell", c=(33, 18, -2.6), r=(1.1, 1.1, 0.9)),
        dict(name="tail",  gene="SHH",  kind="cone", a=(-30, 5, 0), b=(-40, 12, 0), ra=2.2, rb=1.0),
    ]
    legs = {("foreL", -22, -4.5), ("foreR", -22, 4.5), ("hindL", 10, -4.5), ("hindR", 10, 4.5)}
    for nm, sx, sz in legs:
        P.append(dict(name=f"leg_{nm}", gene="MYOD1", kind="cone",
                      a=(sx, 2, sz), b=(sx, -16, sz), ra=2.6, rb=1.8))
    lm = {"nose": (40, 15, 0), "head": (31, 17, 0), "tail": (-40, 12, 0)}
    return FeatureTarget(base, P, lm, box=(96, 50, 30), name="quadruped_genes",
                         k=1.4, env_c=(0.0, 7.0, 0.0), env_r=18.0)


def fish_features():
    base = [("ell", (0, 0, 0), (22, 9, 5))]              # body shell (envelope)
    P = [
        dict(name="body", gene="SHH",  kind="ell", c=(0, 0, 0), r=(22, 9, 5)),
        dict(name="head", gene="FOXG1", kind="ell", c=(-19, 1, 0), r=(4, 5, 4)),
        dict(name="caudal", gene="SHH", kind="cone", a=(18, 0, 0), b=(28, 0, 0), ra=4.0, rb=1.0),
        dict(name="eye_L", gene="PAX6", kind="ell", c=(-17, 2, 3.6),  r=(1.3, 1.3, 1.0)),
        dict(name="eye_R", gene="PAX6", kind="ell", c=(-17, 2, -3.6), r=(1.3, 1.3, 1.0)),
    ]
    lm = {"snout": (-23, 1, 0), "tail": (28, 0, 0)}
    return FeatureTarget(base, P, lm, box=(72, 32, 16), name="fish_genes",
                         k=1.2, env_c=(0.0, 0.0, 0.0), env_r=12.0)
