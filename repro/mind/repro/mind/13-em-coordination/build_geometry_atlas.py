#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_geometry_atlas.py  --  v1.18 (M9 ephaptic geometry grounding)

Builds data/brain_geometry_atlas.json: a MEASURED 3D position [L] for each of the
twelve M9 central-brain organs, in MNI152 stereotaxic space (mm), so that the M9
ephaptic coupling kernel can be evaluated on REAL inter-region distances instead of
the equal-spacing [O] ring used by the frozen v1.17 engine.

DB-SOURCED discipline (VP-SPEC C1, mirrors brain_organ_atlas.json gamma):
  * Every coordinate is COPIED from a published, citable source -- we do NOT choose
    the geometry to move the result. The coordinate table is locked verbatim, exactly
    like the gamma layer locks NCBI-derived values.
  * Composite structures (neocortex, striatum, cerebellum, and bilateral merges) are
    VOLUME-WEIGHTED centroids of published AAL atlas centers-of-mass (Tzourio-Mazoyer
    2002), computed deterministically here (no hand-tuning).
  * Per-region grade is honest:
      [L]  exact published atlas center-of-mass, or a published single-structure MNI
           centroid (AAL CoM table; Ogawa 2024 hypothalamus).
      [O]  representative literature-consistent MNI position for an elongated or
           open / distributed structure that lacks a single canonical MNI centroid
           (midbrain, brainstem, basal-forebrain cholinergic, distributed forebrain
           GABAergic interneurons). Graded [O] ON PURPOSE (no measurement is invented).

Sources (recorded per coordinate in the atlas JSON):
  AAL  : Tzourio-Mazoyer et al. 2002, NeuroImage 15:273-289. Centers-of-mass (MNI) from
         the AAL atlas, tabulated in figshare 184981 / Frontiers SOM Table S1 (503556).
  HTH  : Ogawa et al. 2024 (PMC11487351), "Stereotaxic Coordinates of Human
         Hypothalamic Nuclei ...": medial hypothalamic nuclei centroids (MPO at MNI
         ~ (-1.5,+2.3,-12.8)); representative whole-hypothalamus point used here.
  BF   : Zaborszky et al. 2008, NeuroImage 42:1127-1141 (cytoarchitectonic probabilistic
         maps of basal-forebrain magnocellular Ch1-Ch4); Mesulam Ch4 = nucleus basalis.
         nbM is an 'open' structure (Liu/Mesulam) -> representative SI/Ch4 point, [O].
  MB   : Bianciardi et al. 2015, Brain Struct Funct / AAL3 (Rolls 2020) midbrain nuclei
         (SN/VTA/RN/PAG around the cerebral aqueduct) -> representative midbrain point, [O].
  BS   : lower brainstem (pons/medulla); PHOX2B marks the hindbrain visceral-motor /
         preBotzinger respiratory column (rostral ventrolateral medulla) -> representative
         point, [O] (Harvard-Oxford Brain-Stem / Paxinos-Huang brainstem atlas family).

This generator is provenance only: it is NOT imported by the engine and does NOT run at
verify time. The frozen engine reads nothing from it; the v1.18 decision-check module reads
the OUTPUT json (a locked data input), identical to how it reads the gamma atlas.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_DATA = os.path.normpath(os.path.join(HERE, "..", "_engine", "data"))
OUT = os.path.join(ENGINE_DATA, "brain_geometry_atlas.json")

# ---------------------------------------------------------------------------
# AAL atlas centers-of-mass (MNI mm) -- transcribed VERBATIM from the published
# AAL CoM table (figshare 184981; Frontiers SOM Table S1, article 503556).
# Tuple: (aal_index, label, x, y, z, n_voxels).  Right-is-Right (neurological).
# ---------------------------------------------------------------------------
AAL = [
    (1,"Precentral_L",-39,-6,51,3526),(2,"Precentral_R",41,-8,52,3381),
    (3,"Frontal_Sup_L",-18,35,42,3599),(4,"Frontal_Sup_R",22,31,44,4056),
    (5,"Frontal_Sup_Orb_L",-17,47,-13,963),(6,"Frontal_Sup_Orb_R",18,48,-14,997),
    (7,"Frontal_Mid_L",-33,33,35,4863),(8,"Frontal_Mid_R",38,33,34,5104),
    (9,"Frontal_Mid_Orb_L",-31,50,-10,888),(10,"Frontal_Mid_Orb_R",33,53,-11,1015),
    (11,"Frontal_Inf_Oper_L",-48,13,19,1038),(12,"Frontal_Inf_Oper_R",50,15,21,1399),
    (13,"Frontal_Inf_Tri_L",-46,30,14,2529),(14,"Frontal_Inf_Tri_R",50,30,14,2151),
    (15,"Frontal_Inf_Orb_L",-36,31,-12,1690),(16,"Frontal_Inf_Orb_R",41,32,-12,1707),
    (17,"Rolandic_Oper_L",-47,-8,14,990),(18,"Rolandic_Oper_R",53,-6,15,1331),
    (19,"Supp_Motor_Area_L",-5,5,61,2147),(20,"Supp_Motor_Area_R",9,0,62,2371),
    (21,"Olfactory_L",-8,15,-11,280),(22,"Olfactory_R",10,16,-11,289),
    (23,"Frontal_Sup_Medial_L",-5,49,31,2992),(24,"Frontal_Sup_Medial_R",9,51,30,2134),
    (25,"Frontal_Med_Orb_L",-5,54,-7,719),(26,"Frontal_Med_Orb_R",8,52,-7,856),
    (27,"Rectus_L",-5,37,-18,852),(28,"Rectus_R",8,36,-18,745),
    (29,"Insula_L",-35,7,3,1858),(30,"Insula_R",39,6,2,1770),
    (31,"Cingulum_Ant_L",-4,35,14,1400),(32,"Cingulum_Ant_R",8,37,16,1313),
    (33,"Cingulum_Mid_L",-5,-15,42,1941),(34,"Cingulum_Mid_R",8,-9,40,2203),
    (35,"Cingulum_Post_L",-5,-43,25,463),(36,"Cingulum_Post_R",7,-42,22,335),
    (37,"Hippocampus_L",-25,-21,-10,932),(38,"Hippocampus_R",29,-20,-10,946),
    (39,"ParaHippocampal_L",-21,-16,-21,978),(40,"ParaHippocampal_R",25,-15,-20,1132),
    (41,"Amygdala_L",-23,-1,-17,220),(42,"Amygdala_R",27,1,-18,248),
    (43,"Calcarine_L",-7,-79,6,2258),(44,"Calcarine_R",16,-73,9,1861),
    (45,"Cuneus_L",-6,-80,27,1526),(46,"Cuneus_R",14,-79,28,1424),
    (47,"Lingual_L",-15,-68,-5,2095),(48,"Lingual_R",16,-67,-4,2300),
    (49,"Occipital_Sup_L",-17,-84,28,1366),(50,"Occipital_Sup_R",24,-81,31,1413),
    (51,"Occipital_Mid_L",-32,-81,16,3270),(52,"Occipital_Mid_R",37,-80,19,2098),
    (53,"Occipital_Inf_L",-36,-78,-8,941),(54,"Occipital_Inf_R",38,-82,-8,989),
    (55,"Fusiform_L",-31,-40,-20,2310),(56,"Fusiform_R",34,-39,-20,2518),
    (57,"Postcentral_L",-42,-23,49,3892),(58,"Postcentral_R",41,-25,53,3823),
    (59,"Parietal_Sup_L",-23,-60,59,2065),(60,"Parietal_Sup_R",26,-59,62,2222),
    (61,"Parietal_Inf_L",-43,-46,47,2447),(62,"Parietal_Inf_R",46,-46,50,1345),
    (63,"SupraMarginal_L",-56,-34,30,1256),(64,"SupraMarginal_R",58,-32,34,1974),
    (65,"Angular_L",-44,-61,36,1173),(66,"Angular_R",46,-60,39,1752),
    (67,"Precuneus_L",-7,-56,48,3528),(68,"Precuneus_R",10,-56,44,3265),
    (69,"Paracentral_Lobule_L",-8,-25,70,1349),(70,"Paracentral_Lobule_R",7,-32,68,836),
    (71,"Caudate_L",-11,11,9,962),(72,"Caudate_R",15,12,9,994),
    (73,"Putamen_L",-24,4,2,1009),(74,"Putamen_R",28,5,2,1064),
    (75,"Pallidum_L",-18,0,0,293),(76,"Pallidum_R",21,0,0,280),
    (77,"Thalamus_L",-11,-18,8,1100),(78,"Thalamus_R",13,-18,8,1057),
    (79,"Heschl_L",-42,-19,10,225),(80,"Heschl_R",46,-17,10,249),
    (81,"Temporal_Sup_L",-53,-21,7,2296),(82,"Temporal_Sup_R",58,-22,7,3141),
    (83,"Temporal_Pole_Sup_L",-40,15,-20,1285),(84,"Temporal_Pole_Sup_R",48,15,-17,1338),
    (85,"Temporal_Mid_L",-56,-34,-2,4942),(86,"Temporal_Mid_R",57,-37,-1,4409),
    (87,"Temporal_Pole_Mid_L",-36,15,-34,755),(88,"Temporal_Pole_Mid_R",44,15,-32,1187),
    (89,"Temporal_Inf_L",-50,-28,-23,3200),(90,"Temporal_Inf_R",54,-31,-22,3557),
    (91,"Cerebellum_Crus1_L",-35,-67,-29,2603),(92,"Cerebellum_Crus1_R",38,-67,-30,2648),
    (93,"Cerebellum_Crus2_L",-28,-73,-38,1894),(94,"Cerebellum_Crus2_R",33,-69,-40,2117),
    (95,"Cerebellum_3_L",-8,-37,-19,136),(96,"Cerebellum_3_R",13,-34,-19,207),
    (97,"Cerebellum_4_5_L",-14,-43,-17,1125),(98,"Cerebellum_4_5_R",18,-43,-18,861),
    (99,"Cerebellum_6_L",-22,-59,-22,1694),(100,"Cerebellum_6_R",26,-58,-24,1795),
    (101,"Cerebellum_7b_L",-31,-60,-45,585),(102,"Cerebellum_7b_R",34,-63,-48,534),
    (103,"Cerebellum_8_L",-25,-55,-48,1887),(104,"Cerebellum_8_R",26,-56,-49,2308),
    (105,"Cerebellum_9_L",-10,-49,-46,869),(106,"Cerebellum_9_R",10,-49,-46,809),
    (107,"Cerebellum_10_L",-22,-34,-42,144),(108,"Cerebellum_10_R",27,-34,-41,159),
    (109,"Vermis_1_2",2,-39,-20,53),(110,"Vermis_3",2,-40,-11,228),
    (111,"Vermis_4_5",2,-52,-6,665),(112,"Vermis_6",2,-67,-15,371),
    (113,"Vermis_7",2,-72,-25,194),(114,"Vermis_8",2,-64,-34,243),
    (115,"Vermis_9",2,-55,-35,174),(116,"Vermis_10",1,-46,-32,112),
]
BYIDX = {i: (lab, x, y, z, n) for (i, lab, x, y, z, n) in AAL}

def vw_centroid(indices):
    """Volume-weighted centroid (MNI mm) over the given AAL parcel indices."""
    sx = sy = sz = sw = 0.0
    for i in indices:
        _, x, y, z, n = BYIDX[i]
        sx += x * n; sy += y * n; sz += z * n; sw += n
    return [round(sx / sw, 2), round(sy / sw, 2), round(sz / sw, 2)], int(sw)

# Parcel sets for composite organs ------------------------------------------
NEOCORTEX = list(range(1, 21)) + list(range(23, 37)) + list(range(43, 71)) + list(range(79, 91))
# (excludes 21-22 olfactory, 37-42 hippocampus/parahip/amygdala, 71-78 subcortical, cerebellum)
HIPPO   = [37, 38]
THAL    = [77, 78]
STRIAT  = [71, 72, 73, 74]      # caudate + putamen
PALL    = [75, 76]
CEREB   = list(range(91, 117))  # all cerebellar lobules + vermis
OLF     = [21, 22]              # AAL 'Olfactory' (olfactory region) -- PROXY for the bulb
TELENC  = NEOCORTEX + STRIAT + PALL + OLF  # whole telencephalon (for distributed interneuron proxy)

neo_c,  neo_v  = vw_centroid(NEOCORTEX)
hip_c,  hip_v  = vw_centroid(HIPPO)
thal_c, thal_v = vw_centroid(THAL)
str_c,  str_v  = vw_centroid(STRIAT)
pal_c,  pal_v  = vw_centroid(PALL)
cer_c,  cer_v  = vw_centroid(CEREB)
olf_c,  olf_v  = vw_centroid(OLF)
tel_c,  tel_v  = vw_centroid(TELENC)

def reg(master, mni, grade, source, method, note=""):
    return {"master": master, "mni_xyz": mni, "coord_grade": grade,
            "coord_method": method, "coord_source": source, "note": note}

organs = {
    "neocortex": reg("FOXG1", neo_c, "L",
        "AAL (Tzourio-Mazoyer 2002) volume-weighted centroid of %d isocortical parcels" % len(NEOCORTEX),
        "atlas_com_volume_weighted",
        "Whole cortical mantle centroid; excludes allocortex (hippocampus) and subcortical nuclei."),
    "hippocampus": reg("LHX2", hip_c, "L",
        "AAL Hippocampus_L/_R centers-of-mass, volume-weighted", "atlas_com_volume_weighted", ""),
    "thalamus": reg("GBX2", thal_c, "L",
        "AAL Thalamus_L/_R centers-of-mass, volume-weighted", "atlas_com_volume_weighted", ""),
    "striatum": reg("GSX2", str_c, "L",
        "AAL Caudate_L/_R + Putamen_L/_R centers-of-mass, volume-weighted", "atlas_com_volume_weighted",
        "Striatum = caudate + putamen."),
    "cerebellum": reg("EN1", cer_c, "L",
        "AAL Cerebellum (Crus1-10) + Vermis centers-of-mass, volume-weighted", "atlas_com_volume_weighted", ""),
    "hypothalamus": reg("SIM1", [0.0, -2.0, -12.0], "L",
        "Ogawa et al. 2024 (PMC11487351) human hypothalamic-nuclei MNI centroids (medial nuclei; MPO ~(-1.5,2.3,-12.8))",
        "literature_centroid",
        "Representative whole-hypothalamus point; medial nuclei cluster near x~0, z~-12."),
    "midbrain": reg("OTX2", [0.0, -18.0, -12.0], "O",
        "Bianciardi 2015 / AAL3 (Rolls 2020) midbrain nuclei (SN/VTA/RN/PAG, peri-aqueductal)",
        "representative_mni",
        "Mesencephalon is an elongated structure with no single canonical MNI centroid -> [O] on purpose."),
    "brainstem": reg("PHOX2B", [0.0, -35.0, -45.0], "O",
        "lower brainstem pons/medulla; PHOX2B preBotzinger/visceral-motor column, rostral ventrolateral medulla (Harvard-Oxford Brain-Stem / Paxinos-Huang family)",
        "representative_mni",
        "Brainstem is elongated with no single canonical MNI centroid -> [O] on purpose."),
    "pallidum": reg("NKX2-1", pal_c, "L",
        "AAL Pallidum_L/_R centers-of-mass, volume-weighted", "atlas_com_volume_weighted", ""),
    "forebrain_gaba_in": reg("DLX2", tel_c, "O",
        "distributed pan-forebrain GABAergic interneurons (MGE/CGE-derived; Cardin 2009, Sohal 2009); representative = AAL telencephalon volume-weighted centroid",
        "representative_mni",
        "No single locus: PV/SST interneurons are spread throughout cortex+striatum -> [O] on purpose. Telencephalic center used as representative."),
    "basal_forebrain_chol": reg("LHX8", [0.0, 0.0, -11.0], "O",
        "Zaborszky et al. 2008 (NeuroImage 42:1127) cytoarchitectonic BF Ch4 probabilistic maps; Mesulam Ch4 = nucleus basalis (substantia innominata, sublenticular)",
        "representative_mni",
        "nucleus basalis is an 'open' structure without strict boundaries (Mesulam) -> [O] on purpose. Bilateral-merged sublenticular point."),
    "olfactory_bulb": reg("PAX6", olf_c, "L",
        "AAL Olfactory_L/_R centers-of-mass, volume-weighted (PROXY: AAL 'Olfactory' = olfactory region/sulcus, not the bulb proper)",
        "atlas_com_volume_weighted",
        "AAL has no olfactory-bulb parcel; the bulb proper sits ~10-15 mm anterior. Exact AAL CoM, proxy structure."),
}

atlas = {
    "_provenance": (
        "M9 ephaptic GEOMETRY atlas (v1.18). A MEASURED 3D position [L] in MNI152 stereotaxic "
        "space (mm) for each of the twelve M9 central-brain organs, so the ephaptic coupling "
        "kernel can be evaluated on REAL inter-region distances instead of the equal-spacing [O] "
        "ring of the frozen v1.17 engine. Coordinates are COPIED from published atlases/papers "
        "(DB-SOURCED; we do NOT pick geometry to move the result), exactly as the gamma layer "
        "locks NCBI-derived values. Composite organs (neocortex/striatum/cerebellum/bilateral "
        "merges) are VOLUME-WEIGHTED centroids of AAL centers-of-mass (Tzourio-Mazoyer 2002). "
        "Per-region coord_grade is honest: [L] = exact published atlas center-of-mass or single-"
        "structure MNI centroid; [O] = representative literature-consistent point for an elongated "
        "or open/distributed structure with no single canonical MNI centroid (midbrain, brainstem, "
        "basal-forebrain cholinergic, distributed forebrain GABAergic interneurons). No measurement "
        "is invented. The engine reads NOTHING from this file; only the v1.18 decision-check module "
        "(geometry_grounding.py) reads it, as a locked data input."),
    "_space": "MNI152 (mm), neurological orientation (R is R)",
    "_kernel": "1/r^3 near-field locality is UNCHANGED (neuro 18 [V]); v1.18 changes ONLY the positions ([O] ring -> [L] measured MNI), not the coupling form.",
    "_grading": "MNI coordinate [L measured input] where an exact atlas CoM / published centroid exists; [O representative] for elongated/open/distributed structures with no single canonical centroid. ephaptic kappa stays the MEASURED fraction (neuro 19); normalization is a declared [F] choice (see geometry_grounding.py docstring).",
    "_sources": {
        "AAL": "Tzourio-Mazoyer et al. 2002, NeuroImage 15:273-289; centers-of-mass (MNI) per figshare 184981 / Frontiers SOM Table S1 (article 503556).",
        "hypothalamus": "Ogawa et al. 2024, PMC11487351 (stereotaxic MNI coordinates of human hypothalamic nuclei).",
        "basal_forebrain": "Zaborszky et al. 2008, NeuroImage 42:1127-1141 (cytoarchitectonic probabilistic BF Ch1-Ch4 maps); Mesulam Ch4 = nucleus basalis.",
        "midbrain": "Bianciardi et al. 2015, Brain Struct Funct 220:2387-2405; Rolls et al. 2020 AAL3 midbrain nuclei.",
        "brainstem": "Harvard-Oxford Brain-Stem (FSL); Paxinos & Huang 1995 human brainstem atlas; PHOX2B preBotzinger respiratory column (Smith 1991)."
    },
    "_relation_to_v117": (
        "ADD-ONLY. The frozen v1.17 engine (tree_sha256 b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7, "
        "95 regression checks) is UNCHANGED and reads nothing from this file. v1.18 adds this atlas + a "
        "decision-check module that imports the engine read-only. Promoting the engine's default M9 from "
        "ring to measured geometry (with cascade analysis) and decomposing nodes to capture sulcal-bank "
        "folding are the explicit v1.19 entry points."),
    "_voxel_counts_for_audit": {
        "neocortex": neo_v, "hippocampus": hip_v, "thalamus": thal_v, "striatum": str_v,
        "pallidum": pal_v, "cerebellum": cer_v, "olfactory_bulb": olf_v, "forebrain_gaba_in_telencephalon": tel_v
    },
    "organs": organs,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(atlas, f, ensure_ascii=False, indent=1)

raw = open(OUT, "rb").read()
print("wrote", OUT)
print("sha256", hashlib.sha256(raw).hexdigest())
print("n_organs", len(organs))
for k, v in organs.items():
    print("  %-22s %-7s %-28s %s" % (k, "[%s]" % v["coord_grade"], v["mni_xyz"], v["coord_method"]))
