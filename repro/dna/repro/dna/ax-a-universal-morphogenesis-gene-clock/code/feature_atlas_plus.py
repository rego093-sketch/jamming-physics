"""
feature_atlas_plus.py -- the EXPANDED gene-tagged morphogenesis atlas.

Same machinery as feature_target.FeatureTarget (each part is a GROWABLE, GENE-TAGGED
ellipsoid/round-cone that emerges out of the body envelope), but with a much richer set
of parts so the gene clock has more heterochrony to express:

  HUMAN HEAD (head_features_plus): the original face + scalp hair, eyebrows, eyelashes,
  eyelids, iris, philtrum, teeth, tongue and a neck -- 13 distinct master genes.

  ANIMALS, gene-tagged appendages (the priority-#3a follow-on): the emergence ORDER of
  fins / limbs / digits / beak / feathers / whiskers is now ALSO a readout of measured DNA:
    bird_features        beak=BMP4, wings=TBX5, legs=TBX4, feet=HOXD13, crest/feathers=EDAR
    quadruped_features_plus  forelegs=TBX5, hindlegs=TBX4, paws=HOXD13, whiskers=LEF1, coat=EDAR, horns=SOX9
    fish_features_plus   pectoral=TBX5, pelvic=TBX4, median fins=SHH, gills=SOX9, scales=EDAR

gene -> feature confidence (neuro "representative, cited" discipline):
  [V] master   : eye=PAX6, ear=PAX2, nose/olfactory=LHX2, skin/eyelid=TP63, hair/feather/scale=EDAR,
                 iris pigment=MITF, tooth=PAX9, forelimb/pectoral=TBX5, hindlimb/pelvic=TBX4,
                 digits=HOXD13, beak=BMP4.
  [F] repr.    : cranium=FOXG1, jaw/midline/axis=SHH, cheek/muscle=MYOD1, lips/oral=POU2F3,
                 eyebrow shaft=FOXN1, eyelash keratin=HOXC13, cartilage/bone=SOX9.

Every gene's gamma is the MEASURED value in data/morpho_gamma.json (read-only, never fitted).
"""
import numpy as np
import body as B
from target import _ellipsoid
from feature_target import FeatureTarget


# ===================================================================== rich human head
def head_features_plus():
    """The analytic human head, enriched: original face features PLUS scalp hair,
    eyebrows, eyelashes, eyelids, iris, philtrum, teeth, tongue and a neck.
    sample(scales=None) is the full head (every feature at full size)."""
    base = [
        ("ell", (0.0, 6.0, -1.0), (10.5, 12.5, 11.5)),   # cranium shell (envelope)
        ("ell", (0.0, -5.0, 2.0), (7.5, 9.0, 8.5)),      # face/jaw shell (envelope)
    ]
    P = [
        # --- vault / forehead (FOXG1) ---
        dict(name="cranium", gene="FOXG1", kind="ell", c=(0.0, 7.0, 0.0), r=(9.5, 10.5, 9.5)),
        dict(name="brow",    gene="FOXG1", kind="ell", c=(0.0, 3.2, 8.2), r=(8.0, 1.7, 3.0)),
        # --- jaw / midline (SHH) ---
        dict(name="jaw",     gene="SHH",   kind="ell", c=(0.0, -10.5, 4.5), r=(3.6, 3.4, 4.2)),
        dict(name="philtrum", gene="SHH",  kind="cone", a=(0.0, -5.4, 9.4), b=(0.0, -6.9, 9.6),
             ra=0.45, rb=0.7),
        # --- cheeks (MYOD1) ---
        dict(name="cheek_L", gene="MYOD1", kind="ell", c=(-5.2, -2.5, 6.0), r=(4.2, 4.6, 4.2)),
        dict(name="cheek_R", gene="MYOD1", kind="ell", c=(5.2, -2.5, 6.0),  r=(4.2, 4.6, 4.2)),
        # --- nose / olfactory (LHX2) ---
        dict(name="nose",     gene="LHX2", kind="cone", a=(0.0, 1.0, 8.5), b=(0.0, -4.5, 11.6),
             ra=2.0, rb=1.1),
        dict(name="nose_tip", gene="LHX2", kind="ell", c=(0.0, -5.2, 9.6), r=(1.9, 1.2, 1.6)),
        dict(name="nostril_L", gene="LHX2", kind="ell", c=(-1.7, -5.6, 9.0), r=(1.3, 1.0, 1.4)),
        dict(name="nostril_R", gene="LHX2", kind="ell", c=(1.7, -5.6, 9.0),  r=(1.3, 1.0, 1.4)),
        # --- eyes (PAX6) + iris (MITF) + eyelids (TP63) + eyelashes (HOXC13) ---
        dict(name="eye_L",   gene="PAX6",  kind="ell", c=(-3.9, 2.0, 8.6), r=(2.3, 1.8, 2.0)),
        dict(name="eye_R",   gene="PAX6",  kind="ell", c=(3.9, 2.0, 8.6),  r=(2.3, 1.8, 2.0)),
        dict(name="iris_L",  gene="MITF",  kind="ell", c=(-3.9, 2.0, 10.0), r=(0.9, 0.9, 0.5)),
        dict(name="iris_R",  gene="MITF",  kind="ell", c=(3.9, 2.0, 10.0),  r=(0.9, 0.9, 0.5)),
        dict(name="lid_up_L", gene="TP63", kind="ell", c=(-3.9, 3.0, 8.9), r=(2.5, 0.6, 1.5)),
        dict(name="lid_up_R", gene="TP63", kind="ell", c=(3.9, 3.0, 8.9),  r=(2.5, 0.6, 1.5)),
        dict(name="lid_lo_L", gene="TP63", kind="ell", c=(-3.9, 1.0, 8.9), r=(2.5, 0.5, 1.5)),
        dict(name="lid_lo_R", gene="TP63", kind="ell", c=(3.9, 1.0, 8.9),  r=(2.5, 0.5, 1.5)),
        dict(name="lash_L",  gene="HOXC13", kind="ell", c=(-3.9, 3.4, 9.7), r=(2.4, 0.22, 0.6)),
        dict(name="lash_R",  gene="HOXC13", kind="ell", c=(3.9, 3.4, 9.7),  r=(2.4, 0.22, 0.6)),
        # --- eyebrows (FOXN1) ---
        dict(name="brow_L",  gene="FOXN1", kind="ell", c=(-3.9, 4.2, 9.0), r=(2.7, 0.5, 1.0)),
        dict(name="brow_R",  gene="FOXN1", kind="ell", c=(3.9, 4.2, 9.0),  r=(2.7, 0.5, 1.0)),
        # --- mouth (POU2F3) + teeth (PAX9) + tongue (POU2F3) ---
        dict(name="lips",    gene="POU2F3", kind="ell", c=(0.0, -7.6, 8.6), r=(3.1, 1.4, 2.1)),
        dict(name="teeth_up", gene="PAX9", kind="ell", c=(0.0, -7.2, 8.7), r=(2.6, 0.45, 0.9)),
        dict(name="teeth_lo", gene="PAX9", kind="ell", c=(0.0, -8.0, 8.7), r=(2.6, 0.45, 0.9)),
        dict(name="tongue",  gene="POU2F3", kind="ell", c=(0.0, -7.7, 7.6), r=(1.7, 0.6, 1.3)),
        # --- ears (PAX2) ---
        dict(name="ear_L",   gene="PAX2",  kind="ell", c=(-10.6, 1.5, -0.5), r=(1.3, 4.2, 3.4)),
        dict(name="ear_R",   gene="PAX2",  kind="ell", c=(10.6, 1.5, -0.5),  r=(1.3, 4.2, 3.4)),
        # --- scalp hair (EDAR -- ectodermal-appendage master) ---
        dict(name="hair_crown", gene="EDAR", kind="ell", c=(0.0, 11.5, -1.0), r=(9.8, 5.5, 9.8)),
        dict(name="hair_back",  gene="EDAR", kind="ell", c=(0.0, 5.0, -9.5),  r=(8.5, 8.0, 4.0)),
        dict(name="hair_L",     gene="EDAR", kind="ell", c=(-9.2, 6.0, -2.0), r=(2.8, 7.0, 7.5)),
        dict(name="hair_R",     gene="EDAR", kind="ell", c=(9.2, 6.0, -2.0),  r=(2.8, 7.0, 7.5)),
        dict(name="fringe",     gene="EDAR", kind="ell", c=(0.0, 12.5, 6.5),  r=(7.5, 2.2, 3.5)),
        # --- neck (SHH axis) ---
        dict(name="neck",    gene="SHH",   kind="cone", a=(0.0, -12.0, 2.0), b=(0.0, -19.0, 0.0),
             ra=4.6, rb=5.0),
    ]
    lm = {
        "crown": (0, 18, 0), "nasion": (0, 1.5, 9), "nose_tip": (0, -5.2, 11.4),
        "mouth": (0, -7.6, 10.0), "chin": (0, -11.5, 6.0),
        "eye_L": (-3.9, 2.0, 10.0), "eye_R": (3.9, 2.0, 10.0),
        "ear_L": (-11.5, 1.5, -1.0), "ear_R": (11.5, 1.5, -1.0),
    }
    return FeatureTarget(base, P, lm, box=(42.0, 56.0, 42.0), name="human_head_plus",
                         k=1.4, env_c=(0.0, 2.0, 1.0), env_r=11.0)


# ===================================================================== bird (NEW)
def bird_features():
    """A bird: gene-tagged beak (BMP4), wings (TBX5), legs (TBX4), feet/talons (HOXD13),
    crest + flight + tail feathers (EDAR), head (FOXG1), eyes (PAX6), axial body/neck/tail (SHH)."""
    base = [
        ("ell", (0.0, 0.0, 0.0), (12.0, 8.0, 6.0)),      # body shell (envelope)
        ("ell", (15.0, 11.0, 0.0), (4.5, 4.0, 3.8)),     # head shell (envelope)
    ]
    P = [
        dict(name="body",  gene="SHH",   kind="ell", c=(0.0, 0.0, 0.0), r=(12.0, 8.0, 6.0)),
        dict(name="neck",  gene="SHH",   kind="cone", a=(8.0, 3.0, 0.0), b=(13.5, 9.0, 0.0),
             ra=3.0, rb=2.2),
        dict(name="head",  gene="FOXG1", kind="ell", c=(15.0, 11.0, 0.0), r=(4.5, 4.0, 3.8)),
        dict(name="beak_up", gene="BMP4", kind="cone", a=(18.0, 11.2, 0.0), b=(24.5, 10.6, 0.0),
             ra=1.7, rb=0.45),
        dict(name="beak_lo", gene="BMP4", kind="cone", a=(18.0, 10.0, 0.0), b=(23.0, 9.7, 0.0),
             ra=1.2, rb=0.4),
        dict(name="eye_L", gene="PAX6", kind="ell", c=(17.0, 12.2, 2.4),  r=(1.1, 1.1, 0.9)),
        dict(name="eye_R", gene="PAX6", kind="ell", c=(17.0, 12.2, -2.4), r=(1.1, 1.1, 0.9)),
        dict(name="crest", gene="EDAR", kind="ell", c=(13.5, 15.0, 0.0), r=(2.0, 2.8, 1.2)),
        dict(name="wing_L", gene="TBX5", kind="ell", c=(-6.0, 4.0, 9.0),  r=(9.5, 1.6, 5.0)),
        dict(name="wing_R", gene="TBX5", kind="ell", c=(-6.0, 4.0, -9.0), r=(9.5, 1.6, 5.0)),
        dict(name="primaries_L", gene="EDAR", kind="ell", c=(-14.0, 5.0, 11.0), r=(5.5, 1.0, 2.6)),
        dict(name="primaries_R", gene="EDAR", kind="ell", c=(-14.0, 5.0, -11.0), r=(5.5, 1.0, 2.6)),
        dict(name="tail",  gene="SHH",  kind="cone", a=(-11.0, 1.0, 0.0), b=(-20.0, 4.0, 0.0),
             ra=2.5, rb=1.2),
        dict(name="tail_fan", gene="EDAR", kind="ell", c=(-20.0, 4.0, 0.0), r=(3.0, 1.0, 6.0)),
        dict(name="leg_L", gene="TBX4", kind="cone", a=(2.0, -6.0, 2.6), b=(3.0, -14.0, 2.6),
             ra=1.0, rb=0.7),
        dict(name="leg_R", gene="TBX4", kind="cone", a=(2.0, -6.0, -2.6), b=(3.0, -14.0, -2.6),
             ra=1.0, rb=0.7),
        dict(name="foot_L", gene="HOXD13", kind="ell", c=(4.5, -15.0, 2.6),  r=(2.0, 0.5, 1.3)),
        dict(name="foot_R", gene="HOXD13", kind="ell", c=(4.5, -15.0, -2.6), r=(2.0, 0.5, 1.3)),
    ]
    lm = {"beak": (24.5, 10.6, 0), "head": (15, 11, 0), "tail": (-20, 4, 0)}
    return FeatureTarget(base, P, lm, box=(52.0, 38.0, 26.0), name="bird_genes",
                         k=1.5, env_c=(0.0, 3.0, 0.0), env_r=12.0)


# ===================================================================== quadruped (expanded)
def quadruped_features_plus():
    """Quadruped with limb-identity genes (forelegs=TBX5, hindlegs=TBX4), digits (paws=HOXD13),
    whiskers (LEF1), coat (EDAR), horns (SOX9) on top of the axial body / head / sensory plan."""
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
        # whiskers (LEF1), coat (EDAR), horns (SOX9)
        dict(name="whisker_L", gene="LEF1", kind="ell", c=(37, 14.5, 2.6), r=(3.0, 0.25, 0.5)),
        dict(name="whisker_R", gene="LEF1", kind="ell", c=(37, 14.5, -2.6), r=(3.0, 0.25, 0.5)),
        dict(name="coat", gene="EDAR", kind="ell", c=(-6, 11.5, 0.0), r=(17.0, 2.2, 7.0)),
        dict(name="horn_L", gene="SOX9", kind="cone", a=(30, 21, 2.0), b=(31, 26, 3.0), ra=0.9, rb=0.3),
        dict(name="horn_R", gene="SOX9", kind="cone", a=(30, 21, -2.0), b=(31, 26, -3.0), ra=0.9, rb=0.3),
    ]
    # forelegs TBX5, hindlegs TBX4, each with a paw/claw HOXD13
    legs = [("foreL", -22, -4.5, "TBX5"), ("foreR", -22, 4.5, "TBX5"),
            ("hindL", 10, -4.5, "TBX4"), ("hindR", 10, 4.5, "TBX4")]
    for nm, sx, sz, gene in legs:
        P.append(dict(name=f"leg_{nm}", gene=gene, kind="cone",
                      a=(sx, 2, sz), b=(sx, -16, sz), ra=2.6, rb=1.8))
        P.append(dict(name=f"paw_{nm}", gene="HOXD13", kind="ell",
                      c=(sx + 1.5, -17, sz), r=(2.6, 1.0, 2.2)))
    lm = {"nose": (40, 15, 0), "head": (31, 17, 0), "tail": (-40, 12, 0)}
    return FeatureTarget(base, P, lm, box=(96, 58, 30), name="quadruped_plus_genes",
                         k=1.4, env_c=(0.0, 7.0, 0.0), env_r=18.0)


# ===================================================================== fish (expanded)
def fish_features_plus():
    """Fish with paired-fin identity (pectoral=TBX5, pelvic=TBX4), median fins (dorsal/anal/caudal
    =SHH), gills/operculum (SOX9), scales (EDAR) on top of the axial body / head / eyes."""
    base = [("ell", (0, 0, 0), (22, 9, 5))]              # body shell (envelope)
    P = [
        dict(name="body", gene="SHH",  kind="ell", c=(0, 0, 0), r=(22, 9, 5)),
        dict(name="head", gene="FOXG1", kind="ell", c=(-19, 1, 0), r=(4, 5, 4)),
        dict(name="eye_L", gene="PAX6", kind="ell", c=(-17, 2, 3.6),  r=(1.3, 1.3, 1.0)),
        dict(name="eye_R", gene="PAX6", kind="ell", c=(-17, 2, -3.6), r=(1.3, 1.3, 1.0)),
        # paired fins: pectoral (TBX5) + pelvic (TBX4)
        dict(name="pectoral_L", gene="TBX5", kind="ell", c=(-10, -2, 5.5), r=(4.0, 0.7, 3.0)),
        dict(name="pectoral_R", gene="TBX5", kind="ell", c=(-10, -2, -5.5), r=(4.0, 0.7, 3.0)),
        dict(name="pelvic_L", gene="TBX4", kind="ell", c=(2, -7, 3.5), r=(3.0, 0.6, 2.2)),
        dict(name="pelvic_R", gene="TBX4", kind="ell", c=(2, -7, -3.5), r=(3.0, 0.6, 2.2)),
        # median fins: dorsal / anal / caudal (SHH midline)
        dict(name="dorsal", gene="SHH", kind="ell", c=(2, 10, 0), r=(7.0, 4.0, 0.6)),
        dict(name="anal",   gene="SHH", kind="ell", c=(6, -9, 0), r=(4.5, 2.5, 0.6)),
        dict(name="caudal", gene="SHH", kind="cone", a=(20, 0, 0), b=(28, 0, 0), ra=4.5, rb=1.0),
        dict(name="caudal_fan", gene="SHH", kind="ell", c=(28, 0, 0), r=(1.0, 6.0, 0.6)),
        # gills / operculum (SOX9) + scales (EDAR)
        dict(name="operculum", gene="SOX9", kind="ell", c=(-13, 0, 4.2), r=(2.5, 4.5, 1.0)),
        dict(name="operculum_R", gene="SOX9", kind="ell", c=(-13, 0, -4.2), r=(2.5, 4.5, 1.0)),
        dict(name="scales", gene="EDAR", kind="ell", c=(2, 0, 0), r=(20.0, 7.5, 4.0)),
    ]
    lm = {"snout": (-23, 1, 0), "tail": (28, 0, 0)}
    return FeatureTarget(base, P, lm, box=(72, 40, 18), name="fish_plus_genes",
                         k=1.2, env_c=(0.0, 0.0, 0.0), env_r=12.0)


# convenient registry
ATLAS = {
    "human_head": head_features_plus,
    "bird": bird_features,
    "quadruped": quadruped_features_plus,
    "fish": fish_features_plus,
}
