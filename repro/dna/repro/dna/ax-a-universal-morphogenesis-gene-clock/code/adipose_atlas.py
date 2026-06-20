"""
adipose_atlas.py -- bodies + anatomical DEPOT maps for the Layer-4 adipose engine.

Provides, for each organism, (a) the lean target (reusing the gene-tagged feature atlas where
possible) and (b) a DepotMap: WHERE subcutaneous fat sits, placed on real anatomy. The same
adipose fold (gene x energy) then sets HOW MUCH; the depot sets WHERE; the product inflates the
lean surface. Depot geometry is a forced [F] choice (declared); the amount law is measured-gamma
+ the energy dial.

Human depots follow textbook subcutaneous anatomy:
  FACE: buccal (cheek) fat pad, submental/jowl (double chin), preorbital lid fullness, jawline.
  BODY: abdominal/visceral (central, ANDROID 'apple') vs gluteofemoral hip+thigh (GYNOID 'pear'),
        mixed by `android` in [0,1] (sex/pattern influenced; default 0.5, a forced [F]).
Animal depots show the same axis is general: a quadruped grows a sagging belly + rump + dewlap;
a bird lays down premigratory furcular/abdominal fat (a real, dramatic seasonal phenotype).
"""
import numpy as np
from feature_target import FeatureTarget
from feature_atlas_plus import (head_features_plus, quadruped_features_plus,
                                fish_features_plus, bird_features)
from adipose import DepotMap


# ===================================================================== a compact human BODY
def human_body():
    """A recognisable standing humanoid as growable, gene-tagged soft parts: head, neck, thorax,
    abdomen, pelvis, thighs, upper arms. Soft ellipsoids/cones so adipose inflation reads as a
    fuller torso/hips. sample(scales=None) is the lean body. Coordinates: y up, x L-R, z front."""
    base = [
        ("ell", (0.0, 16.0, 0.0), (11.5, 10.0, 7.5)),   # thorax shell (envelope)
        ("ell", (0.0, -1.0, 0.5), (10.0, 11.0, 7.0)),   # abdomen+pelvis shell (envelope)
    ]
    P = [
        dict(name="head",   gene="FOXG1", kind="ell", c=(0.0, 32.0, 0.0), r=(6.0, 7.0, 6.5)),
        dict(name="neck",   gene="SHH",   kind="cone", a=(0.0, 26.0, 0.0), b=(0.0, 30.0, 0.0),
             ra=3.0, rb=3.5),
        dict(name="thorax", gene="SHH",   kind="ell", c=(0.0, 16.0, 0.0), r=(11.0, 9.0, 7.0)),
        dict(name="abdomen", gene="SHH",  kind="ell", c=(0.0, 4.0, 0.5),  r=(8.5, 7.0, 6.0)),
        dict(name="pelvis", gene="SHH",   kind="ell", c=(0.0, -5.0, 0.0), r=(9.5, 6.0, 7.0)),
        dict(name="thigh_L", gene="TBX4", kind="cone", a=(-4.5, -9.0, 0.0), b=(-5.0, -26.0, 0.0),
             ra=4.5, rb=3.0),
        dict(name="thigh_R", gene="TBX4", kind="cone", a=(4.5, -9.0, 0.0), b=(5.0, -26.0, 0.0),
             ra=4.5, rb=3.0),
        dict(name="arm_L",  gene="TBX5",  kind="cone", a=(-11.0, 18.0, 0.0), b=(-13.0, 4.0, 0.0),
             ra=3.0, rb=2.4),
        dict(name="arm_R",  gene="TBX5",  kind="cone", a=(11.0, 18.0, 0.0), b=(13.0, 4.0, 0.0),
             ra=3.0, rb=2.4),
    ]
    lm = {"head": (0, 32, 0), "navel": (0, 4, 6), "pelvis": (0, -5, 0)}
    return FeatureTarget(base, P, lm, box=(46.0, 84.0, 28.0), name="human_body",
                         k=1.8, env_c=(0.0, 6.0, 0.0), env_r=14.0)


# ===================================================================== depot maps
def face_depot(android=0.5):
    """Subcutaneous facial fat for head_features_plus (head spans y in [-19,18], face front z+)."""
    regions = [
        dict(c=(-5.5, -3.0, 6.5), r=(4.0, 4.5, 4.0), w=1.0, tag="face"),   # buccal pad L
        dict(c=(5.5, -3.0, 6.5),  r=(4.0, 4.5, 4.0), w=1.0, tag="face"),   # buccal pad R
        dict(c=(0.0, -11.0, 4.0), r=(5.5, 4.0, 5.0), w=1.0, tag="face"),   # submental / jowl
        dict(c=(0.0, -8.0, 5.0),  r=(7.0, 4.0, 5.0), w=0.7, tag="face"),   # lower-face / jawline
        dict(c=(0.0, 2.5, 8.0),   r=(7.0, 2.5, 3.0), w=0.35, tag="face"),  # preorbital fullness
        dict(c=(0.0, 0.0, 7.0),   r=(8.0, 4.0, 4.0), w=0.4, tag="face"),   # upper cheek / temple
    ]
    return DepotMap(regions, android=android, name="face_depot")


def body_depot(android=0.5):
    """Central (android) abdominal/visceral vs gluteofemoral (gynoid) hip+thigh, for human_body."""
    regions = [
        dict(c=(0.0, 4.0, 2.5),  r=(10.0, 9.0, 8.0), w=1.0, tag="central"),       # belly (forward)
        dict(c=(0.0, 6.0, 0.0),  r=(13.0, 6.0, 7.0), w=0.6, tag="central"),       # flank/love-handle
        dict(c=(0.0, -5.0, -1.0), r=(12.0, 7.0, 8.0), w=1.0, tag="gluteofemoral"), # hips/buttock
        dict(c=(-5.0, -16.0, 0.0), r=(6.0, 9.0, 6.0), w=0.7, tag="gluteofemoral"), # thigh L
        dict(c=(5.0, -16.0, 0.0),  r=(6.0, 9.0, 6.0), w=0.7, tag="gluteofemoral"), # thigh R
        dict(c=(0.0, 25.0, 1.0),  r=(4.0, 3.0, 4.0), w=0.3, tag="face"),           # submental
    ]
    return DepotMap(regions, android=android, name="body_depot")


def quadruped_depot(android=0.6):
    """A quadruped gaining weight: sagging belly + flank + rump + dewlap (+ a fat-tail base)."""
    regions = [
        dict(c=(-5.0, 2.0, 0.0),  r=(20.0, 6.0, 8.0), w=1.0, tag="central"),        # belly (sag)
        dict(c=(-5.0, 7.0, 0.0),  r=(18.0, 5.0, 8.0), w=0.6, tag="central"),        # flank/ribs
        dict(c=(8.0, 6.0, 0.0),   r=(8.0, 6.0, 7.0), w=0.7, tag="gluteofemoral"),   # rump
        dict(c=(24.0, 11.0, 0.0), r=(5.0, 4.0, 5.0), w=0.4, tag="face"),            # dewlap/neck
        dict(c=(-32.0, 5.0, 0.0), r=(5.0, 4.0, 6.0), w=0.5, tag="face"),            # fat-tail base
    ]
    return DepotMap(regions, android=android, name="quadruped_depot")


def bird_depot(android=0.5):
    """Premigratory fattening: furcular (wishbone), abdominal and flank fat -- a real seasonal
    phenotype where small birds can double mass before migration."""
    regions = [
        dict(c=(6.0, 2.0, 0.0),  r=(10.0, 6.0, 6.0), w=1.0, tag="central"),  # abdominal
        dict(c=(10.0, 6.0, 0.0), r=(5.0, 4.0, 5.0), w=0.7, tag="face"),      # furcular (throat/breast)
        dict(c=(-2.0, 1.0, 0.0), r=(8.0, 5.0, 7.0), w=0.6, tag="central"),   # flank
    ]
    return DepotMap(regions, android=android, name="bird_depot")


# convenient scene registry: organism -> (lean target, depot map)
SCENES = {
    "face":      lambda android=0.5: (head_features_plus(),        face_depot(android)),
    "body":      lambda android=0.5: (human_body(),                body_depot(android)),
    "quadruped": lambda android=0.6: (quadruped_features_plus(),   quadruped_depot(android)),
    "bird":      lambda android=0.5: (bird_features(),             bird_depot(android)),
}
