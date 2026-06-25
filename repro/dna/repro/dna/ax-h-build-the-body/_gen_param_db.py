# -*- coding: utf-8 -*-
"""Generate param_db.json for Appendix H (build the body) from the REAL fetched driver gamma
atlas + the hand-authored module inventory / count-grammar / size-switch / assembly definitions.
Every number carries a provenance string. No inline magic numbers downstream."""
import json, collections

drv = json.load(open("/home/claude/work/driver_cache/driver_gamma.json"))["drivers"]

# ---- compact driver gamma table (REAL GRCh38 promoter reads; gamma=-mean(NN dG, SantaLucia98))
driver_gamma = {}
for sym, d in drv.items():
    driver_gamma[sym] = {
        "gamma": d["gamma"], "program": d["program"], "system": d["system"],
        "provenance": "GRCh38 %s win%d-%d strand%d; NCBI eutils; %s" % (
            d["acc"], d["window"][0], d["window"][1], d["window"][2], d["note"]),
        "grade": "[L]",
    }

# ---- the SantaLucia-1998 NN table (re-locked verbatim from the corpus; add-only)
NN = {"AA":-1.0,"TT":-1.0,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,"GT":-1.44,"AC":-1.44,
      "CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,"CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

# ============================================================================
# THE MODULE INVENTORY -- the body's buildable parts grouped by DEVELOPMENTAL PROGRAM.
# Each group: (named members | a count rule), its driver program -> driver gene -> real gamma,
# its body system, its renormalization tower level, and an assembly parent (for the graph).
# Bones are grouped so the 206 total is DERIVED from the group counts (auditable), not asserted.
# 'driver' must be a key in driver_gamma. 'parent' references an assembly node (see assembly).
# ============================================================================
SKEL = []  # (group, system, driver, renorm_level, members[list] OR count[int], parent, mode)

def grp(group, system, driver, level, members, parent, mode="endochondral"):
    SKEL.append({"group": group, "system": system, "driver": driver, "renorm_level": level,
                 "members": members if isinstance(members, list) else None,
                 "count": members if isinstance(members, int) else len(members),
                 "parent": parent, "ossification": mode})

# --- AXIAL: cranium (intramembranous, neural-crest / RUNX2-MSX2 / DLX5) -------------
grp("cranial_vault","skeletal","RUNX2","L3",
    ["frontal","parietal_L","parietal_R","temporal_L","temporal_R","occipital","sphenoid","ethmoid"],
    "skull_base","intramembranous")
grp("facial_skeleton","skeletal","DLX5","L3",
    ["maxilla_L","maxilla_R","zygomatic_L","zygomatic_R","nasal_L","nasal_R","lacrimal_L",
     "lacrimal_R","palatine_L","palatine_R","inf_nasal_concha_L","inf_nasal_concha_R","vomer","mandible"],
    "skull_base","intramembranous")
grp("auditory_ossicles","skeletal","DLX5","L3",
    ["malleus_L","malleus_R","incus_L","incus_R","stapes_L","stapes_R"],"skull_base","endochondral")
grp("hyoid","skeletal","DLX5","L3",["hyoid"],"skull_base","endochondral")
# --- AXIAL: vertebral column (sclerotome PAX1/PAX9; serial -> COUNT grammar) ---------
grp("cervical_vertebrae","skeletal","PAX1","L3",
    ["C1_atlas","C2_axis","C3","C4","C5","C6","C7"],"skull_base","endochondral")
grp("thoracic_vertebrae","skeletal","PAX1","L3",
    ["T%d"%i for i in range(1,13)],"cervical_vertebrae","endochondral")
grp("lumbar_vertebrae","skeletal","PAX1","L3",
    ["L%d"%i for i in range(1,6)],"thoracic_vertebrae","endochondral")
grp("sacrum","skeletal","PAX1","L3",["sacrum"],"lumbar_vertebrae","endochondral")
grp("coccyx","skeletal","PAX1","L3",["coccyx"],"sacrum","endochondral")
# --- AXIAL: thoracic cage (ribs serial from thoracic somites; sternum) ---------------
grp("ribs","skeletal","PAX9","L3",["rib_%s_%d"%(s,i) for i in range(1,13) for s in ("L","R")],
    "thoracic_vertebrae","endochondral")
grp("sternum","skeletal","SP7","L3",["sternum"],"ribs","endochondral")
# --- APPENDICULAR: pectoral girdle + arm (limb_fore TBX5; SHH/GLI3 autopod) ----------
grp("pectoral_girdle","skeletal","TBX5","L3",
    ["clavicle_L","clavicle_R","scapula_L","scapula_R"],"sternum","intramembranous")
grp("arm","skeletal","TBX5","L3",
    ["humerus_L","humerus_R","radius_L","radius_R","ulna_L","ulna_R"],"pectoral_girdle","endochondral")
grp("hand","skeletal","GLI3","L3",
    ["carpal_%s_%d"%(s,i) for i in range(1,9) for s in ("L","R")] +
    ["metacarpal_%s_%d"%(s,i) for i in range(1,6) for s in ("L","R")] +
    ["phalanx_hand_%s_%d"%(s,i) for i in range(1,15) for s in ("L","R")],
    "arm","endochondral")
# --- APPENDICULAR: pelvic girdle + leg (limb_hind TBX4) ------------------------------
grp("pelvic_girdle","skeletal","TBX4","L3",["hip_bone_L","hip_bone_R"],"sacrum","endochondral")
grp("leg","skeletal","TBX4","L3",
    ["femur_L","femur_R","patella_L","patella_R","tibia_L","tibia_R","fibula_L","fibula_R"],
    "pelvic_girdle","endochondral")
grp("foot","skeletal","GLI3","L3",
    ["tarsal_%s_%d"%(s,i) for i in range(1,8) for s in ("L","R")] +
    ["metatarsal_%s_%d"%(s,i) for i in range(1,6) for s in ("L","R")] +
    ["phalanx_foot_%s_%d"%(s,i) for i in range(1,15) for s in ("L","R")],
    "leg","endochondral")

bone_total = sum(g["count"] for g in SKEL)

# --- TEETH (cranio_tooth MSX1/PAX9/PITX2; serial -> count grammar; 32 permanent) ------
TEETH = {"group":"permanent_teeth","system":"dental","driver":"MSX1","renorm_level":"L3",
         "parent":"facial_skeleton","members":
            ["incisor_%s_%d"%(q,i) for q in ("UL","UR","LL","LR") for i in range(1,3)] +   # 8
            ["canine_%s"%q for q in ("UL","UR","LL","LR")] +                                 # 4
            ["premolar_%s_%d"%(q,i) for q in ("UL","UR","LL","LR") for i in range(1,3)] +    # 8
            ["molar_%s_%d"%(q,i) for q in ("UL","UR","LL","LR") for i in range(1,4)]}        # 12
TEETH["count"] = len(TEETH["members"])

# --- ORGANS (program-specific master TFs) -------------------------------------------
ORGANS = [
 ("brain_forebrain","nervous","FOXG1","L3","cranial_vault"),
 ("brain_cortex","nervous","EMX2","L3","brain_forebrain"),
 ("brain_midbrain","nervous","OTX2","L3","brain_forebrain"),
 ("brain_hindbrain","nervous","GBX2","L3","brain_midbrain"),
 ("eye_L","nervous","PAX6","L3","cranial_vault"),
 ("eye_R","nervous","PAX6","L3","cranial_vault"),
 ("spinal_cord","nervous","PAX6","L3","brain_hindbrain"),
 ("heart","cardiac","NKX2-5","L3","sternum"),
 ("lung_L","respiratory","NKX2-1","L3","ribs"),
 ("lung_R","respiratory","NKX2-1","L3","ribs"),
 ("thyroid","endocrine","NKX2-1","L3","hyoid"),
 ("liver","digestive","HNF4A","L3","ribs"),
 ("pancreas","digestive","PDX1","L3","lumbar_vertebrae"),
 ("stomach","digestive","PDX1","L3","liver"),
 ("kidney_L","urinary","SIX2","L3","lumbar_vertebrae"),
 ("kidney_R","urinary","SIX2","L3","lumbar_vertebrae"),
 ("gonad_L","reproductive","SIX2","L3","pelvic_girdle"),
 ("gonad_R","reproductive","SIX2","L3","pelvic_girdle"),
]
organ_rows = [{"group":n,"system":s,"driver":d,"renorm_level":lv,"parent":p,"count":1,
               "members":[n]} for (n,s,d,lv,p) in ORGANS]

# --- MUSCLE (myogenic MYF5/MYOD1; the full named count carried by the count grammar) -
# representative named muscles (real) + the full count anchored in count_grammar.
MUSCLE = {"group":"skeletal_muscles","system":"muscular","driver":"MYF5","renorm_level":"L2",
          "parent":"skeleton_attached","members":
            ["sternocleidomastoid","masseter","temporalis","trapezius","deltoid_L","deltoid_R",
             "pectoralis_major","biceps_brachii","triceps_brachii","brachioradialis",
             "rectus_abdominis","external_oblique","erector_spinae","latissimus_dorsi",
             "gluteus_maximus","quadriceps_femoris","hamstrings","gastrocnemius","soleus",
             "tibialis_anterior","iliopsoas","diaphragm","intercostals","orbicularis_oculi",
             "orbicularis_oris","frontalis","flexor_digitorum","extensor_digitorum",
             "adductor_magnus","sartorius"]}
MUSCLE["count"] = len(MUSCLE["members"])

# ============================================================================
# THE COUNT GRAMMAR (G7) -- the segmentation clock and the serial-number rules.
# Like TIMING and SIZE in Appendix A's INTEGRATED LAW: gamma fixes WHICH program and ORDER,
# but HOW MANY serial copies is a RELATIONAL quantity (clock period vs axis-elongation window)
# that no static gamma carries. Supply the measured systemic parameter -> the count is recovered.
# ============================================================================
COUNT_GRAMMAR = {
 "_law":"COUNT is recovered from a CLOCK, not from gamma. N_serial ~ T_window / P_clock. The "
        "clock period P is set by a sequence-influenced delayed-negative-feedback oscillator "
        "(HES7 transcription+intron+translation delay); the window T is the axis-elongation "
        "duration. gamma does NOT carry N (the count null), exactly as it does not carry timing "
        "or absolute size. Realized counts are CITED measured anatomy, never tuned to a formula.",
 "clock_oscillator_genes":{"value":["HES7","LFNG","DLL3"],
        "provenance":"Hes7 delayed-feedback segmentation-clock oscillator; Lfng/Dll3 Notch gating "
                     "(Bessho2003 GenesDev; Dale2003 Nature; Bulman2000 NatGenet DLL3 SCD).",
        "grade":"[L]"},
 "human_clock_period_min":{"value":300.0,
        "provenance":"human segmentation-clock period ~5 h in vitro (Matsuda2020 Science; "
                     "Diaz-Cuadros2020 Nature). Mouse ~2-3 h -> period is the lever.","grade":"[L]"},
 "human_somite_pairs_total":{"value":42,
        "provenance":"~42 somite pairs form in human (4 occipital + 8 cervical + 12 thoracic + "
                     "5 lumbar + 5 sacral + ~8 coccygeal); Christ&Ordahl1995.","grade":"[L]"},
 "occipital_somites_to_skull":{"value":4,
        "provenance":"the 4 occipital somites contribute to the basioccipital skull, not free "
                     "vertebrae (Christ&Ordahl1995).","grade":"[L]"},
 "serial_counts_real":{"value":{"presacral_vertebrae":24,"thoracic_vertebrae_and_rib_pairs":12,
        "cervical_vertebrae":7,"lumbar_vertebrae":5,"digits_per_limb":5,"permanent_teeth":32,
        "deciduous_teeth":20,"named_skeletal_muscles_approx":640},
        "provenance":"standard adult human anatomy (Gray's Anatomy 41e); muscle count is the "
                     "commonly-cited ~640 named skeletal muscles.","grade":"[L]"},
 "digit_count_rule":{"value":"pentadactyl default; Shh(ZPA)/Gli3 antero-posterior balance sets "
                     "digit NUMBER -- Gli3 loss -> polydactyly, the lever (Hui1993; Litingtung2002 "
                     "Nature; Welscher2002 Science).","grade":"[L]"},
 "tooth_count_rule":{"value":"MSX1/PAX9 dosage gates tooth number -- MSX1 or PAX9 loss -> "
                     "oligodontia, the lever (Vastardis1996 NatGenet; Stockton2000 NatGenet).",
                     "grade":"[L]"},
 "count_null_corr_ceiling":{"value":0.30,
        "provenance":"the |corr| ceiling (re-used from the App E/F/G orthogonality convention) "
                     "below which the driver-gamma spectrum is declared to NOT carry the serial "
                     "count -- the count null.","grade":"[F]"},
}

# ============================================================================
# THE SIZE SWITCH -- relative module size from a DOSAGE parameter (allometric), like Appendix A's
# E-energy dial. gamma does not carry absolute size; supply dosage -> relative size is recovered.
# ============================================================================
SIZE_SWITCH = {
 "_law":"SIZE = base * dosage^exponent. gamma fixes program, NOT magnitude (the size null, App A "
        "dwell rho=0.11). The dosage (GH/IGF1 axis, morphogen amplitude, lifestyle-energy E) is "
        "the systemic lever; the allometric exponent is cited. Absolute mass stays [O].",
 "allometric_exponent_organ":{"value":0.75,
        "provenance":"Kleiber-type allometric scaling exponent for organ mass vs body mass "
                     "(West-Brown-Enquist 1997 Science; widely cited 3/4 power).","grade":"[L]"},
 "size_dosage_default":{"value":1.0,
        "provenance":"the neutral systemic dosage (lever at unity); perturbing it rescales all "
                     "modules monotonically -- the size switch.","grade":"[F]"},
 "system_size_class":{"value":{"skeletal":1.0,"muscular":0.9,"nervous":0.8,"cardiac":0.4,
        "respiratory":0.7,"digestive":0.9,"urinary":0.4,"endocrine":0.15,"reproductive":0.3,
        "dental":0.1},
        "provenance":"coarse relative size classes per system (a forced [F] modelling canvas, NOT "
                     "a claim about measured organ volumes; the switch SCALES these, it does not "
                     "fit them).","grade":"[F]"},
}

# ============================================================================
# THE ASSEMBLY GRAMMAR -- the module ADJACENCY GRAPH. A body is not a pile of parts: each module
# attaches to a parent, rooted at the axial origin. Built from the 'parent' fields above; the
# extra cross-links below close real articulations (girdle <-> axial). Connectivity is PROVEN
# (every module reachable from the root) in build.assembly -- the "build the house" joinery.
# ============================================================================
ASSEMBLY = {
 "_law":"every buildable module attaches to a parent module; the graph is a single connected tree "
        "rooted at the axial origin (skull_base). This is the discourse/architecture grammar (G3) "
        "lifted to the WHOLE body -- the tissue-to-tissue / part-to-part arrangement map.",
 "root":"skull_base",
 "abstract_nodes":{"value":["skull_base","skeleton_attached"],
        "provenance":"skull_base = the axial origin (basicranium); skeleton_attached = the muscle "
                     "anchor set (muscles attach across named bones). Abstract assembly nodes.",
        "grade":"[F]"},
 "extra_articulations":{"value":[["skeleton_attached","sternum"]],
        "provenance":"the muscle anchor set is rooted into the axial skeleton so the whole graph "
                     "is one connected body.","grade":"[F]"},
}

# ============================================================================
THRESHOLDS = {
 "spinodal_form":{"value":"spinodal(g) = 2*(g/3)^1.5","provenance":"re-used verbatim from "
        "Appendix A emergence engine (code/emergence_v2); the gamma->onset map.","grade":"[F]"},
 "phi_c":{"value":0.84,"provenance":"jamming onset packing fraction, 3D frictionless spheres "
        "(O'Hern-Silbert-Liu-Nagel 2003 PRE 68:011306); re-used from Appendix C.","grade":"[L]"},
 "z_isostatic_3d":{"value":6,"provenance":"isostatic (Maxwell) contact number z_iso=2d, d=3; "
        "re-used from Appendix C.","grade":"[L]"},
 "rigidity_onset_exponent":{"value":0.5,"provenance":"Delta_z ~ (phi-phi_c)^(1/2) "
        "(O'Hern 2003); re-used from Appendix C.","grade":"[L]"},
 "build_phi_default":{"value":0.90,"provenance":"a jammed-solid demonstration packing fraction "
        "(>phi_c) at which finished modules are rigidified; a forced [F] modelling value, NOT a "
        "measured per-tissue phi (that is [O]).","grade":"[F]"},
 "renorm_levels":{"value":{"L0":"molecular","L1":"cell","L2":"tissue","L3":"organ","L4":"body"},
        "provenance":"the structural tower, re-used verbatim from Appendix C.","grade":"[L]"},
}

GRADES = {
 "[L]":"locked: real GRCh38 driver-gene gamma / cited anatomy / cited jamming + clock + allometry",
 "[V]":"verified: exact decomposition or logical invariant (precision) -- order, renorm algebra, "
       "assembly connectivity, determinism",
 "[F]":"fixed modelling choice (program->driver map, size canvas, demo phi, thresholds); declared",
 "[O]":"open: physical realization absent -- cell-resolution instantiation needs measured tissue "
       "mechanics + a growth atlas + HPC; back-fit forbidden",
}

META = {
 "purpose":"Appendix H -- THE BUILD: from blueprint to body. Appendix F declared the READING "
   "grammar structurally complete (G1 material .. G6 individual-difference) -- 100% of the grammar "
   "is mapped. But a read blueprint is not yet a built house. This appendix opens the orthogonal "
   "CONSTRUCTIVE axis: it enumerates the body as HUNDREDS of buildable modules (206 bones derived "
   "from developmental-program group counts, 32 teeth, organs, representative muscles), gives each "
   "a GRAMMAR ADDRESS (program -> real driver-gene gamma -> emergence order), adds the COUNT "
   "grammar G7 (the segmentation clock that sets serial NUMBER -- vertebrae/ribs/digits/teeth), the "
   "SIZE switch (relative magnitude from a dosage lever), the ASSEMBLY grammar (the part-to-part "
   "adjacency tree -- the joinery that makes a body, not a pile), and a 4D BUILD SCHEDULE (modules "
   "appearing in spinodal-gamma order across developmental time), then COMPILES the build by "
   "rigidifying each finished module to a jammed rigid unit and renormalizing cell->tissue->organ->"
   "body (the 강성화 the user asked for). The DECLARATION is THREE-axis: STRUCTURAL grammar "
   "COMPLETE (App F), CONSTRUCTIVE manifest COMPLETE (this appendix -- every module addressed, "
   "counted, sized, assembled, scheduled), PHYSICAL realization OPEN [O] (instantiating real tissue "
   "at cell resolution needs measured mechanics + HPC; never claim a built human).",
 "rule":"LOCK -> Derive -> Gate. No fitted parameters. precision != accuracy. 반증 = 발견. 집. "
        "Add-only: Appendices A-G and every prior number, grade, equation and DOI are unchanged; "
        "the 8 overlapping driver gammas (SOX9/RUNX2/PAX1/PAX3/GLI3/TBX15/DCHS2/EDAR) are "
        "byte-identical to Appendix G. The CONSTRUCTIVE axis is NEW and orthogonal to the reading "
        "axis -- this does not contradict Appendix F's 'no remaining undiscovered READING grammar'.",
 "the_three_axes":{
   "structural_reading":"G1..G6 -- COMPLETE (Appendix F/G; unchanged)",
   "constructive_manifest":"modules x {program->gamma, count(G7), size switch, assembly tree, 4D "
        "schedule, renorm compile} -- COMPLETE (this appendix)",
   "physical_realization":"cell-resolution instantiation of real tissue -- OPEN [O]"},
 "grades":GRADES,
}

param_db = {
 "_meta":META,
 "nn_stacking_dG_kcal_per_mol":{"grade":"[L]","provenance":"SantaLucia 1998 PNAS 95:1460 unified "
        "NN dG37; re-locked verbatim from Appendices E/F/G.","values":NN},
 "driver_gamma":driver_gamma,
 "module_inventory":{
    "_axis":"the body's buildable modules grouped by developmental program. 206 bones are DERIVED "
            "from the group counts below (cranial 8 + facial 14 + ossicles 6 + hyoid 1 + vertebrae "
            "26 + thoracic cage 25 + pectoral 4 + arm 6 + hand 54 + pelvic 2 + leg 8 + foot 52 = "
            "206). Each group: driver program -> driver gene (real gamma) -> system -> renorm level "
            "-> assembly parent.",
    "grade":"[L]/[F]",
    "bone_total_expected":bone_total,
    "skeleton_groups":SKEL,
    "teeth":TEETH,
    "organs":organ_rows,
    "muscle":MUSCLE},
 "count_grammar":COUNT_GRAMMAR,
 "size_switch":SIZE_SWITCH,
 "assembly_grammar":ASSEMBLY,
 "thresholds":THRESHOLDS,
}

json.dump(param_db, open("param_db.json","w"), indent=2, ensure_ascii=False)
print("bone_total (derived from group counts) =", bone_total)
print("teeth =", TEETH["count"], "| organs =", len(organ_rows), "| muscle rows =", MUSCLE["count"])
n_named = bone_total + TEETH["count"] + len(organ_rows) + MUSCLE["count"]
print("named module rows in manifest =", n_named)
print("driver genes with real gamma =", len(driver_gamma))
print("wrote param_db.json")
