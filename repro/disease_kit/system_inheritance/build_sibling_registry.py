#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sibling_registry.py  --  VENDOR the cross-system inheritance surface.   [NATIVE, ROADMAP V]

  *** Writes system_inheritance/sibling_registry.json -- a VENDORED, READ-ONLY snapshot of the
      γ-grounded organ-master map that each VP body sibling package OWNS, plus the per-sibling
      ownership boundary (VP_FRAMEWORK_MAP section 6: which "major" dynamics-defined disease each
      sibling owns and the kit therefore EXCLUDES).  This is the exact seam discipline the siblings
      already run (integumentary/immune/digestive vendor read-only snapshots in their inherited/
      directory and never import sibling code): the registry is a SNAPSHOT, never live sibling code.

  PROVENANCE.  Every organ-master γ below is the value MEASURED and FROZEN by the owning sibling
      package's reports/emergence_results.json (γ = SantaLucia 1998 nearest-neighbour stacking ΔG,
      the same engine this kit uses).  The kit never re-derives it -- it is owned by the sibling and
      cited.  Re-vendoring (if a sibling re-measures) re-reads that sibling's frozen emergence_results
      and re-writes this file; the value is never fitted here.

  FIREWALL.  The registry carries STRUCTURE (organ identity + measured γ) and the OWNERSHIP boundary
      ONLY.  No magnitude, no dose, no efficacy.  It is read-only input to pipeline/system_inheritance.py.

Run:  python3 system_inheritance/build_sibling_registry.py [--write]
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------------------------------
# VENDORED SNAPSHOT.  organ-master (organ -> compartment -> master gene -> measured γ) per sibling,
# read once from each sibling's FROZEN reports/emergence_results.json and recorded here with the
# source package + version + concept DOI.  γ is owned/measured by the sibling (cited [V]).
# --------------------------------------------------------------------------------------------------
SIBLINGS = {
    "cardioresp": {
        "package": "cardioresp_vp_site", "version": "0.5.0",
        "doi_concept": "10.5281/zenodo.20755371", "klass": "machine_dynamics",
        "physical_class": "oscillator + control",
        "organ_masters": [
            {"organ": "heart", "compartment": "cardiac",     "gene": "NKX2-5", "gamma": 1.5130},
            {"organ": "lung",  "compartment": "respiratory", "gene": "NKX2-1", "gamma": 1.5088},
        ],
        "seam_axes": ["cardiac excitation-contraction / rate control", "respiratory drive (RSA oscillator)"],
        "owned_major_disease_EXCLUDED": [
            "lung cancer (carcinogen -> R19 barrier down -> Kramers crossing; dynamics-defined, acquired)",
            "RSA / Cheyne-Stokes respiration dynamics (control-loop, not a gene-defined entity)",
        ],
    },
    "circulatory": {
        "package": "circulatory_vp_site", "version": "0.7.0",
        "doi_concept": "10.5281/zenodo.20754354", "klass": "machine_dynamics",
        "physical_class": "flow + clearance",
        "organ_masters": [
            {"organ": "kidney",  "compartment": "renal",   "gene": "SIX2", "gamma": 1.5556},
            {"organ": "liver",   "compartment": "hepatic", "gene": "HHEX", "gamma": 1.5250},
            {"organ": "vessels", "compartment": "vascular_endothelium", "gene": "(vasculature)", "gamma": None},
        ],
        "seam_axes": ["renal filtration / clearance", "hepatic clearance", "vascular endothelial tone"],
        "owned_major_disease_EXCLUDED": [
            "renal cell carcinoma (acquired, dynamics-defined)",
            "hepatocellular carcinoma (aflatoxin x HBV; acquired)",
        ],
    },
    "digestive": {
        "package": "digestive_vp_site", "version": "0.16.0",
        "doi_concept": "10.5281/zenodo.20755319", "klass": "machine_dynamics",
        "physical_class": "slow transport + metabolic homeostasis",
        "organ_masters": [
            {"organ": "stomach",   "compartment": "gastric",    "gene": "BARX1", "gamma": 1.5609},
            {"organ": "intestine", "compartment": "intestinal", "gene": "CDX2",  "gamma": 1.4500},
            {"organ": "pancreas",  "compartment": "pancreatic", "gene": "PDX1",  "gamma": 1.4732},
            {"organ": "liver",     "compartment": "hepatic",    "gene": "HHEX",  "gamma": 1.5250},
        ],
        "seam_axes": ["gastric acid / motility", "intestinal absorption", "pancreatic endo/exocrine", "hepatic metabolism"],
        "owned_major_disease_EXCLUDED": [
            "colorectal cancer, gastric cancer (H. pylori synergy), pancreatic cancer (acquired)",
        ],
    },
    "musculoskeletal": {
        "package": "musculoskeletal_vp_site", "version": "0.7.0",
        "doi_concept": "10.5281/zenodo.20755760", "klass": "machine_dynamics",
        "physical_class": "structure + mechanical load",
        "organ_masters": [
            {"organ": "skeletal_muscle", "compartment": "skeletal_muscle", "gene": "MYOD1", "gamma": 1.4933},
            {"organ": "cartilage",       "compartment": "cartilage",       "gene": "SOX9",  "gamma": 1.4598},
            {"organ": "limb_skeleton",   "compartment": "limb_skeleton",   "gene": "TBX5",  "gamma": 1.4392},
            {"organ": "bone",            "compartment": "bone",            "gene": "RUNX2", "gamma": 1.2414},
        ],
        "seam_axes": ["skeletal-muscle contractile maintenance", "cartilage matrix", "limb pattern", "bone mineral structure"],
        "owned_major_disease_EXCLUDED": [
            "osteosarcoma (radiation; environmental carcinogenesis weak -- honestly flagged by the owner)",
        ],
    },
    "immune": {
        "package": "immune_hematologic_vp_site", "version": "0.20.0",
        "doi_concept": "10.5281/zenodo.20755280", "klass": "machine_dynamics",
        "physical_class": "population-threshold / clonal",
        "organ_masters": [
            {"organ": "thymus",      "compartment": "thymic",   "gene": "FOXN1", "gamma": 1.4533},
            {"organ": "spleen",      "compartment": "splenic",  "gene": "TLX1",  "gamma": 1.4228},
            {"organ": "bone_marrow", "compartment": "myeloid",  "gene": "RUNX1", "gamma": 1.3225},
            {"organ": "lymphoid",    "compartment": "lymphoid", "gene": "PAX5",  "gamma": 1.4892},
        ],
        "seam_axes": ["thymic T-cell selection", "splenic filtration", "haematopoiesis", "adaptive lymphoid clonality"],
        "owned_major_disease_EXCLUDED": [
            "leukaemia (benzene), lymphoma (acquired); immune evasion = cross-cutting carcinogenesis modulator",
        ],
    },
    "integumentary": {
        "package": "integumentary_vp_site", "version": "1.0.0",
        "doi_concept": "10.5281/zenodo.20754541", "klass": "machine_dynamics",
        "physical_class": "barrier + external stimulus",
        "organ_masters": [
            {"organ": "epidermis",     "compartment": "epidermal",   "gene": "TP63", "gamma": 1.3643},
            {"organ": "keratinocyte",  "compartment": "keratinocyte","gene": "KRT14","gamma": 1.4894},
            {"organ": "melanocyte",    "compartment": "melanocyte",  "gene": "MITF", "gamma": 1.3945},
            {"organ": "skin_appendage","compartment": "skin_appendage","gene": "EDAR","gamma": 1.3696},
        ],
        "seam_axes": ["epidermal barrier", "keratinocyte differentiation", "melanin photoprotection", "appendage patterning"],
        "owned_major_disease_EXCLUDED": [
            "melanoma / SCC (UV) -- the cleanest carcinogenesis case; acquired, dynamics-defined",
        ],
    },
    "reproductive": {
        "package": "reproductive_endocrine_vp_site", "version": "0.7.1",
        "doi_concept": "10.5281/zenodo.20754657", "klass": "machine_dynamics",
        "physical_class": "hormone cycle + germ cell",
        "organ_masters": [
            {"organ": "gonad_testis", "compartment": "gonadal_testis", "gene": "SOX9",  "gamma": 1.4598},
            {"organ": "gonad_ovary",  "compartment": "gonadal_ovary",  "gene": "FOXL2", "gamma": 1.4829},
            {"organ": "germline",     "compartment": "germline",       "gene": "DAZL",  "gamma": 1.3803},
            {"organ": "reproductive_tract", "compartment": "reproductive_tract", "gene": "WT1", "gamma": 1.5182},
        ],
        "seam_axes": ["gonadal determination", "germ-cell maintenance", "reproductive-tract / urogenital duct"],
        "owned_major_disease_EXCLUDED": [
            "breast cancer (estrogen), cervical cancer (HPV), prostate cancer (acquired)",
        ],
    },
    "thermometabolic": {
        "package": "homeostasis_thermometabolic_vp_site", "version": "0.6.0",
        "doi_concept": "10.5281/zenodo.20756934", "klass": "homeostasis",
        "physical_class": "heat + energy setpoint loop",
        "organ_masters": [
            {"organ": "brown_adipose",       "compartment": "thermogenic_BAT",   "gene": "UCP1",  "gamma": 1.4054},
            {"organ": "sympathetic_thermo",  "compartment": "sympathetic_drive", "gene": "ADRB3", "gamma": 1.4462},
            {"organ": "white_adipose",       "compartment": "adipose_storage",   "gene": "PPARG", "gamma": 1.3902},
            {"organ": "melanocortin_appetite","compartment": "hypothalamic_satiety","gene": "MC4R","gamma": 1.2720},
            {"organ": "leptin_feedback",     "compartment": "leptin_axis",       "gene": "LEPR",  "gamma": 1.4554},
            {"organ": "insulin_glucose",     "compartment": "insulin_effector",  "gene": "INSR",  "gamma": 1.4956},
            {"organ": "ghrelin_hunger",      "compartment": "hunger_signal",     "gene": "GHRL",  "gamma": 1.3550},
            {"organ": "torpor_fuel_switch",  "compartment": "fuel_switch",       "gene": "PDK4",  "gamma": 1.4112},
        ],
        "seam_axes": ["thermogenesis", "energy storage", "hypothalamic satiety/appetite", "glucose homeostasis"],
        "owned_major_disease_EXCLUDED": [
            "type-2 diabetes, obesity, metabolic syndrome (loop setpoint failure; dynamics-defined, common)",
        ],
    },
    "hemodynamic": {
        "package": "homeostasis_hemodynamic_vp_site", "version": "0.7.0",
        "doi_concept": "10.5281/zenodo.20756801", "klass": "homeostasis",
        "physical_class": "pressure / volume loop",
        "organ_masters": [
            {"organ": "kidney_volume_integrator", "compartment": "renal_volume", "gene": "SIX2", "gamma": 1.5556},
            {"organ": "raas_endocrine",           "compartment": "raas_axis",    "gene": "REN",  "gamma": 1.3634},
        ],
        "seam_axes": ["MAP = CO x SVR x volume loop", "RAAS endocrine setpoint"],
        "owned_major_disease_EXCLUDED": [
            "essential hypertension, chronic heart failure (setpoint reset; dynamics-defined, common)",
        ],
    },
    "ionic": {
        "package": "homeostasis_ionic_vp_site", "version": "0.8.0",
        "doi_concept": "10.5281/zenodo.20755910", "klass": "homeostasis",
        "physical_class": "mineral / acid-base loop",
        "organ_masters": [
            {"organ": "parathyroid_pth",       "compartment": "parathyroid",     "gene": "GCM2",  "gamma": 1.4642},
            {"organ": "calcium_sensing",       "compartment": "calcium_sensor",  "gene": "CASR",  "gamma": 1.3299},
            {"organ": "vitamin_d_axis",        "compartment": "vitamin_d",       "gene": "VDR",   "gamma": 1.4243},
            {"organ": "bone_mineral_reservoir","compartment": "bone_mineral",    "gene": "RUNX2", "gamma": 1.2414},
            {"organ": "kidney_mineral_acidbase","compartment": "renal_mineral",  "gene": "SIX2",  "gamma": 1.5556},
        ],
        "seam_axes": ["Ca-PO4 (PTH<->vit D<->bone<->kidney)", "pH (lung CO2 + kidney HCO3)", "electrolyte"],
        "owned_major_disease_EXCLUDED": [
            "osteoporosis, hyperparathyroidism, acid-base/electrolyte disorders, nephrolithiasis (loop dysregulation)",
        ],
    },
    "circadian": {
        "package": "circadian_vp_site", "version": "0.3.0",
        "doi_concept": "10.5281/zenodo.20755413", "klass": "time_cross_cutting",
        "physical_class": "coupled oscillator (time)",
        "organ_masters": [
            {"organ": "core_clock_loop", "compartment": "circadian_clock", "gene": "BMAL1", "gamma": 1.3335},
        ],
        "seam_axes": ["~24h clock network (SCN + peripheral) gating every setpoint", "light entrainment"],
        "owned_major_disease_EXCLUDED": [
            "circadian sleep-wake disorders, shift-work metabolic/cardiovascular, shift-work cancer (IARC 2A)",
        ],
    },
    "aging": {
        "package": "aging_senescence_vp_site", "version": "1.4.0",
        "doi_concept": "10.5281/zenodo.20756155", "klass": "time_cross_cutting",
        "physical_class": "slow decline capstone (time)",
        "organ_masters": [
            {"organ": "cellular_senescence",      "compartment": "senescence",       "gene": "TP53",   "gamma": 1.4298},
            {"organ": "senescence_arrest_switch", "compartment": "senescence_arrest","gene": "CDKN2A", "gamma": 1.4424},
            {"organ": "longevity_signaling",      "compartment": "longevity",        "gene": "FOXO3",  "gamma": 1.5942},
            {"organ": "telomere_maintenance",     "compartment": "telomere",         "gene": "TERT",   "gamma": 1.5539},
        ],
        "seam_axes": ["slow setpoint drift of every loop", "cellular senescence (trapped attractor)", "risk multiplier of every carcinogenesis kernel"],
        "owned_major_disease_EXCLUDED": [
            "sarcopenia, frailty/multimorbidity, aging-as-cancer-risk-multiplier (time-axis, not gene-defined)",
        ],
    },
    "sensory": {
        "package": "sensory_organ_vp_site", "version": "0.4.0",
        "doi_concept": "10.5281/zenodo.20755154", "klass": "sensory",
        "physical_class": "instrument physics + R19 transduction",
        "organ_masters": [
            {"organ": "eye_retina_optics",  "compartment": "ocular_retina",  "gene": "PAX6",   "gamma": 1.5110},
            {"organ": "eye_photoreceptor",  "compartment": "photoreceptor",  "gene": "RAX",    "gamma": 1.4541},
            {"organ": "cochlea_frequency",  "compartment": "cochlear",       "gene": "EYA1",   "gamma": 1.3638},
            {"organ": "inner_ear_haircell", "compartment": "inner_ear_hair", "gene": "SOX2",   "gamma": 1.4573},
            {"organ": "taste_chemodetect",  "compartment": "gustatory",      "gene": "TAS1R3", "gamma": 1.5555},
        ],
        "seam_axes": ["eye optics + retinal transduction", "cochlear frequency map", "vestibular balance", "taste/smell chemodetection"],
        "owned_major_disease_EXCLUDED": [
            "cataract, glaucoma, AMD, myopia, presbycusis, diabetic retinopathy, BPPV (acquired/multifactorial)",
        ],
    },
}

# --------------------------------------------------------------------------------------------------
# COMPARTMENT ANCHORS -- the two body pillars that supply a COMPARTMENT identity but no organ-master γ
# in this snapshot (the neural machine, and the organ-identity SSOT).  The kit reads its OWN causal
# gene's γ for a neural disease (e.g. SCN1A for Dravet); neuro supplies the CNS/PNS compartment anchor,
# DNA supplies the organ-identity SSOT every sibling already cites.  These are NOT γ donors for the
# kit's diseases -- they are compartment labels with cited ownership, kept honest (no fabricated γ).
# --------------------------------------------------------------------------------------------------
ANCHORS = {
    "neuro": {
        "package": "neuro_emergence_chain_integrated", "version": "1.11.0",
        "doi_concept": "10.5281/zenodo.17979015",
        "role": "somatic neural machine (ion-channel -> behaviour); shared FHN/R19/CPG primitive provider",
        "compartments": ["cns", "pns_peripheral_nerve"],
        "note": "compartment anchor only -- no organ-master γ vendored; the kit reads its own causal-gene γ for a neural disease",
    },
    "dna": {
        "package": "dna_vp_site (4D DNA Blueprint)", "version": "1.12",
        "doi_concept": "10.5281/zenodo.20471407",
        "role": "organ IDENTITY + emergence ORDER SSOT (every body sibling cites it); γ measured, read-only, never fitted",
        "compartments": ["organ_identity_ssot"],
        "note": "the upstream owner of organ identity; this registry's organ-master γ values trace to the same measured-γ discipline",
    },
}

OWNERSHIP_CONTRACT = {
    "_about": "VP_FRAMEWORK_MAP section 6 etiology-class contract, recorded here for the exclusion gate.",
    "kit_owns": "single-gene / rare / hereditary, MULTI-SYSTEM, INTRACTABLE (난치) monogenic disease "
                "(gene-defined). The kit reads the ONE causal-gene promoter and inherits the STRUCTURAL "
                "context of every organ system that gene's lesion manifests in.",
    "kit_excludes": "the 'major' (common / acquired / multifactorial / dynamics-defined) disease each "
                    "sibling owns -- the cancers, type-2 diabetes, essential hypertension, common "
                    "osteoporosis, the acquired sensory diseases. Those are owned by the sibling machine/"
                    "homeostasis/time packages (dynamics-key), NOT by this kit. 'Name it, do not hide it.'",
    "tie_break": "VP_FRAMEWORK_MAP section 6.1: gene-defined -> this kit / disease_wp; dynamics-defined -> "
                 "the sibling. A common disease with a monogenic subtype: the kit owns the gene-defined "
                 "monogenic entity, the sibling owns the common-disease dynamics; cross-reference, do not merge.",
}


def build():
    return {
        "_about": "VENDORED, READ-ONLY cross-system inheritance surface for the VP Disease Emergence Kit "
                  "(ROADMAP V / system-inheritance). γ values are MEASURED and OWNED by the sibling "
                  "packages (cited [V]); this kit never re-derives or fits them. Seam discipline: snapshot "
                  "only, no sibling code imported, the kit's own freeze, the 78 per-disease hashes untouched.",
        "_doi_kit": "10.5281/zenodo.20755262",
        "_gamma_method": "SantaLucia 1998 nearest-neighbour stacking ΔG (the shared VP substrate engine)",
        "_firewall": "STRUCTURE (organ identity + measured γ) + OWNERSHIP boundary only; NO magnitude / dose / efficacy.",
        "ownership_contract": OWNERSHIP_CONTRACT,
        "siblings": SIBLINGS,
        "compartment_anchors": ANCHORS,
        "counts": {
            "sibling_packages": len(SIBLINGS),
            "organ_masters_with_gamma": sum(
                1 for s in SIBLINGS.values() for o in s["organ_masters"] if isinstance(o["gamma"], (int, float))
            ),
            "compartment_anchors": len(ANCHORS),
        },
    }


def main():
    reg = build()
    write = "--write" in sys.argv
    out = os.path.join(HERE, "sibling_registry.json")
    if write:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(reg, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"wrote {os.path.relpath(out)}")
    c = reg["counts"]
    print(f"siblings={c['sibling_packages']}  organ-masters-with-γ={c['organ_masters_with_gamma']}  "
          f"anchors={c['compartment_anchors']}")
    print("OVERALL: PASS")


if __name__ == "__main__":
    main()
