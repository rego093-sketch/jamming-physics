#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
system_inheritance.py  --  MULTI-SYSTEM INHERITANCE layer for intractable disease.  [NATIVE, ROADMAP V]

  *** NATIVE to the VP Disease Emergence Kit (not inherited code).  ROADMAP V: a single causal-gene
      lesion in a MULTI-SYSTEM, INTRACTABLE (난치) disease manifests in several organ systems at once.
      Reading the ONE causal-gene promoter (which this kit already does) tells you the switch
      perturbation and the corrective DIRECTION -- but NOT the structure of every organ system the
      lesion touches.  That structure is OWNED, measured, and frozen in the VP body siblings.  This
      layer INHERITS, read-only, the γ-grounded structural context of each affected organ system from
      system_inheritance/sibling_registry.json, and then surfaces -- structurally -- which compartments
      the lead corrective lever REACHES versus leaves as a GAP.  Each GAP is the next, non-obvious
      treatment DIRECTION (the compartment a researcher must address with a different route/modality). ***

  WHAT IS READ (FROZEN / READ-ONLY -- the per-disease freeze repro/expected_sha256.json is never touched):
    - system_inheritance/sibling_registry.json    (VENDORED real measured organ-master γ from 13 siblings)
    - system_inheritance/multisystem_manifest.json (the NECESSARY inherited systems per disease + falsifier)
    - diseases/_registry.json                       (which slugs exist; statuses)
    - diseases/<slug>/analysis.json                 (each disease's OWN frozen switch read + lead lever)

  PROVENANCE HANDSHAKE (fail-closed, per disease):
    1. the disease must be RESOLVED in its frozen analysis.json   (suspension rule respected -- a
       SUSPENDED disease has no analyzable single-gene promoter and is NOT processed here);
    2. the manifest causal_gene must equal the frozen emergence.primary_switch.gene   (gene handshake);
    3. the manifest lead_lever_frozen.lever must equal the frozen lead_corrective_lever.lever;
    4. the manifest lead_modality_signature must be a SUBSTRING of the frozen agent_class
       (so the modality whose biodistribution we read is the SAME agent the kit already forced);
    5. every inherited_system must resolve to a REAL organ-master γ in the registry (or to a declared
       neural compartment anchor) -- otherwise fail closed.

  THE REACH READ (DIRECTION-ONLY):
    A compartment is mapped to a reach-CLASS (systemic_perfused / neural / cornea / retina / satiety).
    A lead modality is mapped to the SET of classes it reaches, each with a CITED biodistribution basis.
    REACHED  iff  class(compartment) ∈ reaches(modality);  otherwise GAP.
    This is a QUALITATIVE biodistribution direction (does the modality class reach the compartment at
    all), cited.  The DEGREE of correction in any compartment is ALWAYS [O].  No dose, no efficacy.

  EXCLUSION GATE (VP_FRAMEWORK_MAP §6, fail-closed):
    The kit owns gene-defined monogenic disease.  Every manifest disease must be gene-defined and must
    NOT be one of the 'major' (dynamics-defined, common/acquired) diseases a sibling owns.  The gate
    asserts gene-definition and screens every manifest disease name against the siblings' declared
    owned_major_disease_EXCLUDED list.

  FIREWALL: STRUCTURE (which organ systems, measured γ) + DIRECTION (which compartments the lead lever
  reaches) only.  A magnitude scan rejects any asserted dose / efficacy / response-rate / p-value in the
  emitted artifact (γ structural constants and journal citations are not magnitudes).

USAGE:
  python3 pipeline/system_inheritance.py            # build map + self-test, print summary
  python3 pipeline/system_inheritance.py --write    # also freeze repro/expected_system_inheritance_sha256.json
  python3 pipeline/system_inheritance.py --selftest  # determinism + gate teeth (exit 0/1) -- for run_all S6
"""
import os
import re
import sys
import copy
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SI = os.path.join(ROOT, "system_inheritance")
DISEASES = os.path.join(ROOT, "diseases")

REGISTRY = os.path.join(SI, "sibling_registry.json")
MANIFEST = os.path.join(SI, "multisystem_manifest.json")
OUT = os.path.join(SI, "system_inheritance_map.json")
FREEZE = os.path.join(ROOT, "repro", "expected_system_inheritance_sha256.json")

DOI_KIT = "10.5281/zenodo.20755262"
FAIL = []


def check(name, cond):
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {name}")
    if not cond:
        FAIL.append(name)
    return bool(cond)


# ==================================================================================================
# STATIC structural tables  (the cited biodistribution model -- DIRECTION only, no magnitude)
# ==================================================================================================
# Each disease-affected compartment -> a coarse reach CLASS.  The class, not the organ-master γ,
# decides reach: γ is the STRUCTURE of the organ system; the class is the delivery compartment the
# modality must physically reach.  (The eye organ-master PAX6 is the γ donor for the whole ocular
# system; the disease then specifies WHICH ocular sub-compartment -- cornea vs retina -- is hit.)
COMPARTMENT_CLASS = {
    # systemically perfused parenchyma -- reached by any systemically-distributed agent
    "vascular_endothelium": "systemic_perfused",
    "renal": "systemic_perfused",
    "cardiac": "systemic_perfused",
    "hepatic": "systemic_perfused",
    "skeletal_muscle": "systemic_perfused",
    "respiratory": "systemic_perfused",
    "pancreatic": "systemic_perfused",
    "intestinal": "systemic_perfused",
    "epidermal": "systemic_perfused",
    "joint": "systemic_perfused",
    "gonadal_testis": "systemic_perfused",
    "reproductive_tract": "systemic_perfused",
    "limb_skeleton": "systemic_perfused",
    # privileged / barrier compartments -- reached only by specific routes
    "cns": "neural",
    "pns_peripheral_nerve": "neural",
    "ocular_cornea": "cornea",
    "ocular_retina": "retina",
    "hypothalamic_satiety": "satiety",
}

# Each lead-modality CLASS -> the set of reach-classes it physically reaches, with a CITED basis.
# 'reaches' is authoritative for REACH/GAP; 'misses' is a declared cross-check (must be disjoint from
# 'reaches'); 'caveat' is a structural qualifier surfaced to the reader (never a magnitude).
MODALITY_REACH = {
    "enzyme_replacement_iv": {
        "reaches": {"systemic_perfused"},
        "misses": {"neural", "cornea", "retina", "satiety"},
        "basis": ("IV recombinant enzyme distributes to perfused parenchyma via mannose-6-phosphate / "
                  "mannose receptor uptake but does NOT cross the blood-brain barrier or enter avascular "
                  "/ privileged compartments"),
        "cited": "Desnick & Schuchman 2012 (ERT biodistribution)",
    },
    "cftr_modulator_oral": {
        "reaches": {"systemic_perfused"},
        "misses": set(),
        "caveat": "genotype_limited: corrects only modulator-responsive CFTR alleles, not class-I "
                  "(no-protein) genotypes",
        "basis": ("oral small-molecule modulator distributes to all CFTR-expressing epithelia, but the "
                  "switch is restored only where residual / responsive CFTR protein is present"),
        "cited": "Middleton 2019 NEJM (CFTR modulator pharmacology)",
    },
    "small_molecule_substrate_depleter_systemic": {
        "reaches": {"systemic_perfused"},
        "misses": {"cornea"},
        "basis": ("oral aminothiol depletes cystine in perfused tissues but penetrates the AVASCULAR "
                  "cornea poorly, so corneal crystals require a separate topical route"),
        "cited": "Gahl 2002 NEJM 347:111; Kaiser-Kupfer 1990",
    },
    "mtor_inhibitor_systemic": {
        "reaches": {"systemic_perfused", "neural"},
        "misses": {"cornea", "retina", "satiety"},
        "basis": ("rapalogue distributes systemically AND achieves CNS exposure sufficient to shrink the "
                  "subependymal giant-cell astrocytoma (everolimus is approved for SEGA)"),
        "cited": "Krueger 2010 NEJM 363:1801",
    },
    "melanocortin4_agonist": {
        "reaches": {"satiety"},
        "misses": {"systemic_perfused", "neural", "cornea", "retina"},
        "basis": ("the agonist acts at the hypothalamic MC4R satiety node DOWNSTREAM of the broken "
                  "cilium; it does not repair the ciliopathy in retina, kidney or limb"),
        "cited": "Pomeroy/Clement 2021 (setmelanotide in BBS)",
    },
    "metal_chelator_systemic": {
        "reaches": {"systemic_perfused", "neural", "cornea"},
        "misses": {"retina", "satiety"},
        "basis": ("copper chelator mobilises copper from hepatic, neural (basal-ganglia) AND corneal "
                  "deposits -- the contrast case where the systemic route reaches every affected "
                  "compartment"),
        "cited": "Roberts & Schilsky 2008 Hepatology",
    },
    "therapeutic_phlebotomy": {
        "reaches": {"systemic_perfused"},
        "misses": set(),
        "basis": ("removing red-cell iron lowers the whole parenchymal iron pool via plasma transferrin "
                  "equilibration, reaching all perfused parenchymal compartments"),
        "cited": "Pietrangelo 2010 Gastroenterology",
    },
}


# ==================================================================================================
# load (read-only)
# ==================================================================================================
def _load_inputs():
    reg = json.load(open(REGISTRY, encoding="utf-8"))
    man = json.load(open(MANIFEST, encoding="utf-8"))
    diseases_reg = json.load(open(os.path.join(DISEASES, "_registry.json"), encoding="utf-8"))
    return reg, man, diseases_reg


def _frozen_analysis(slug):
    p = os.path.join(DISEASES, slug, "analysis.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding="utf-8"))


def _resolve_organ_master(reg, sibling, organ):
    """Return the registry organ-master dict for (sibling, organ), or None."""
    sib = reg.get("siblings", {}).get(sibling)
    if not sib:
        return None
    for om in sib.get("organ_masters", []):
        if om.get("organ") == organ:
            return om
    return None


def _is_anchor_compartment(reg, sibling, compartment):
    """True if (sibling, compartment) is a declared neural/identity compartment anchor."""
    anch = reg.get("compartment_anchors", {}).get(sibling)
    if not anch:
        return False
    return compartment in anch.get("compartments", [])


# ==================================================================================================
# core build  (pure function of the frozen inputs)
# ==================================================================================================
def _build_disease_record(slug, dz, reg, analysis, errors):
    """Build the inheritance record for one manifest disease.  Append fail-closed reasons to errors."""
    rec = {
        "slug": slug,
        "disease": dz["disease"],
        "causal_gene": dz["causal_gene"],
        "intractable_rationale": dz["intractable_rationale"],
    }

    # --- provenance handshake (fail-closed) ---------------------------------------------------
    if analysis is None:
        errors.append(f"{slug}: no frozen analysis.json")
        return None
    if analysis.get("status") != "RESOLVED":
        errors.append(f"{slug}: not RESOLVED (status={analysis.get('status')}) -- suspension rule")
        return None
    psw = analysis.get("emergence", {}).get("primary_switch", {})
    if psw.get("gene") != dz["causal_gene"]:
        errors.append(f"{slug}: gene handshake fail (manifest {dz['causal_gene']} != frozen {psw.get('gene')})")
        return None
    lead = analysis.get("treatment_A_switch", {}).get("lead_corrective_lever", {})
    frozen_lever = lead.get("lever")
    frozen_agent = lead.get("agent_class", "")
    if frozen_lever != dz["lead_lever_frozen"]["lever"]:
        errors.append(f"{slug}: lever handshake fail (manifest {dz['lead_lever_frozen']['lever']} != frozen {frozen_lever})")
        return None
    sig = dz["lead_modality_signature"]
    if sig.lower() not in frozen_agent.lower():
        errors.append(f"{slug}: signature '{sig}' not in frozen agent_class '{frozen_agent}'")
        return None
    modality = dz["lead_modality"]
    if modality not in MODALITY_REACH:
        errors.append(f"{slug}: unknown lead_modality '{modality}'")
        return None

    mr = MODALITY_REACH[modality]
    reaches = mr["reaches"]

    rec["frozen_primary_switch"] = {
        "gene": psw.get("gene"), "role": psw.get("role"),
        "mechanism": psw.get("mechanism"),
        "emergent_axis_direction": psw.get("emergent_axis_direction"),
    }
    rec["lead_corrective_lever"] = {
        "lever": frozen_lever,
        "agent_class_frozen": frozen_agent,             # echoed verbatim from the disease's own freeze
        "lead_modality": modality,
        "modality_signature_matched": sig,
        "status": lead.get("status"),
    }
    rec["modality_reach_model"] = {
        "reaches_classes": sorted(reaches),
        "basis": mr["basis"],
        "cited": mr["cited"],
    }
    if "caveat" in mr:
        rec["modality_reach_model"]["caveat"] = mr["caveat"]

    # --- resolve each inherited organ system to REAL γ + classify reach -----------------------
    systems = []
    real_gamma_count = 0
    for s in dz["inherited_systems"]:
        comp = s["compartment"]
        sibling = s["sibling"]
        organ = s.get("organ")
        klass = COMPARTMENT_CLASS.get(comp)
        if klass is None:
            errors.append(f"{slug}: compartment '{comp}' not in COMPARTMENT_CLASS")
            return None

        donor_gene = None
        gamma = None
        donor_kind = None
        if s.get("anchor"):
            if not _is_anchor_compartment(reg, sibling, comp):
                errors.append(f"{slug}: anchor compartment '{comp}' not declared for sibling '{sibling}'")
                return None
            donor_kind = "compartment_anchor"      # neural: kit reads its own causal-gene γ, no donor γ
        else:
            om = _resolve_organ_master(reg, sibling, organ)
            if om is None:
                errors.append(f"{slug}: ({sibling},{organ}) does not resolve to a registry organ-master")
                return None
            donor_gene = om.get("gene")
            gamma = om.get("gamma")
            donor_kind = "organ_master_gamma" if gamma is not None else "structural_compartment_no_gamma"
            if gamma is not None:
                real_gamma_count += 1

        reached = klass in reaches
        systems.append({
            "compartment": comp,
            "reach_class": klass,
            "sibling": sibling,
            "organ": organ,
            "donor_kind": donor_kind,
            "donor_gene": donor_gene,
            "gamma": gamma,
            "reach": "REACHED" if reached else "GAP",
            "manifestation": s["reason"],
            "cited": s["cited"],
        })

    if real_gamma_count < 1:
        errors.append(f"{slug}: no inherited system resolves to a real organ-master γ")
        return None

    reached = [x["compartment"] for x in systems if x["reach"] == "REACHED"]
    gap = [x["compartment"] for x in systems if x["reach"] == "GAP"]

    rec["inherited_systems"] = systems
    rec["reach_summary"] = {
        "n_systems": len(systems),
        "n_with_measured_gamma": real_gamma_count,
        "reached": reached,
        "gap": gap,
    }
    # the catalytic output: each GAP compartment is the next, non-obvious treatment DIRECTION
    rec["next_directions"] = [
        {
            "compartment": x["compartment"],
            "reach_class": x["reach_class"],
            "unmet_because": (f"the lead modality ({modality}) does not reach the "
                              f"{x['reach_class']} compartment"),
            "manifestation": x["manifestation"],
            "cited": x["cited"],
            "direction_grade": "[F]",       # forced + cited direction
            "magnitude_grade": "[O]",       # degree of any future correction is ungraded
        }
        for x in systems if x["reach"] == "GAP"
    ]
    rec["falsifier"] = dz["falsifier"]
    rec["grades"] = {
        "organ_system_structure_gamma": "[V] measured + owned by the sibling package, vendored read-only",
        "compartment_manifestation": "[F] forced, cited from the disease's own clinical literature",
        "compartment_reach_direction": "[F] forced, cited biodistribution (reach yes/no only)",
        "correction_magnitude": "[O] ungraded -- no dose, efficacy, or response rate",
    }
    return rec


def _exclusion_gate(man, reg, errors):
    """VP_FRAMEWORK_MAP §6: every manifest disease must be gene-defined and must NOT be a sibling's
    owned 'major' (dynamics-defined) disease.  Returns the audit block."""
    excluded = []
    for sk, sv in reg.get("siblings", {}).items():
        for d in sv.get("owned_major_disease_EXCLUDED", []):
            excluded.append({"sibling": sk, "major_disease": d, "_norm": _norm(d)})

    collisions = []
    for slug, dz in man["diseases"].items():
        if not dz.get("causal_gene"):
            errors.append(f"exclusion gate: {slug} has no causal_gene (not gene-defined)")
        name_norms = {_norm(dz["disease"]), _norm(slug)}
        for ex in excluded:
            for nn in name_norms:
                # a collision is a non-trivial token overlap between a kit disease and an excluded major
                if nn and ex["_norm"] and (nn in ex["_norm"] or ex["_norm"] in nn):
                    collisions.append({"kit_disease": slug, "excluded": ex["major_disease"], "sibling": ex["sibling"]})
    if collisions:
        for c in collisions:
            errors.append(f"exclusion gate: kit disease '{c['kit_disease']}' collides with sibling "
                          f"'{c['sibling']}' major disease '{c['excluded']}'")
    return {
        "rule": "VP_FRAMEWORK_MAP §6.1: gene-defined -> this kit; dynamics-defined -> the sibling.",
        "n_excluded_major_diseases_registered": len(excluded),
        "n_manifest_diseases_gene_defined": sum(1 for dz in man["diseases"].values() if dz.get("causal_gene")),
        "collisions": collisions,
        "status": "PASS" if not collisions and all(dz.get("causal_gene") for dz in man["diseases"].values()) else "FAIL",
    }


_STOP = {"acquired", "common", "essential", "dynamics", "defined", "the", "and", "of", "type",
         "disease", "syndrome", "x", "aflatoxin", "hbv", "multifactorial"}


def _norm(s):
    """Normalise a disease label to its core content tokens (strip parentheticals + qualifiers)."""
    s = re.sub(r"\(.*?\)", " ", str(s)).lower()
    toks = [t for t in re.split(r"[^a-z0-9]+", s) if t and t not in _STOP and len(t) > 2]
    return " ".join(sorted(set(toks)))


def build_map():
    reg, man, diseases_reg = _load_inputs()
    errors = []

    records = {}
    for slug in sorted(man["diseases"].keys()):
        dz = man["diseases"][slug]
        analysis = _frozen_analysis(slug)
        rec = _build_disease_record(slug, dz, reg, analysis, errors)
        if rec is not None:
            records[slug] = rec

    exclusion = _exclusion_gate(man, reg, errors)

    n_reached = sum(len(r["reach_summary"]["reached"]) for r in records.values())
    n_gap = sum(len(r["reach_summary"]["gap"]) for r in records.values())

    out = {
        "_about": ("MULTI-SYSTEM INHERITANCE map (ROADMAP V).  For each multi-system, INTRACTABLE "
                   "monogenic disease RESOLVED in this kit, the NECESSARY organ systems its single "
                   "causal-gene lesion manifests in -- each inherited read-only with the sibling's REAL "
                   "measured organ-master γ -- and which compartments the lead corrective lever reaches "
                   "versus leaves as a GAP (the next treatment direction).  DIRECTION + STRUCTURE only."),
        "_doi_kit": DOI_KIT,
        "_firewall": ("STRUCTURE (organ systems + measured γ) + DIRECTION (compartment reach yes/no), "
                      "cited.  Degree of correction in any compartment is always [O].  No dose, efficacy, "
                      "response rate, or individual medical advice."),
        "_inputs_frozen_readonly": [
            "system_inheritance/sibling_registry.json",
            "system_inheritance/multisystem_manifest.json",
            "diseases/<slug>/analysis.json (per disease, frozen)",
        ],
        "method": {
            "gamma_source": reg.get("_gamma_method"),
            "reach_model": "cited qualitative biodistribution (reach class membership); magnitude [O]",
            "compartment_classes": sorted(set(COMPARTMENT_CLASS.values())),
            "modalities_modelled": sorted(MODALITY_REACH.keys()),
        },
        "exclusion_gate": exclusion,
        "counts": {
            "diseases": len(records),
            "inherited_system_links": sum(r["reach_summary"]["n_systems"] for r in records.values()),
            "organ_systems_with_measured_gamma": sum(r["reach_summary"]["n_with_measured_gamma"] for r in records.values()),
            "compartments_reached": n_reached,
            "compartments_gap_next_direction": n_gap,
        },
        "diseases": records,
    }
    return out, errors


# ==================================================================================================
# gate (firewall + structural) + determinism self-test
# ==================================================================================================
def _serialize(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True)


MAGNITUDE_PATTERNS = [
    r"\d+\s*mg(?:/kg)?\b",                                          # 50 mg, 10 mg/kg
    r"\d+(?:\.\d+)?\s*%",                                           # 45%
    r"\d+(?:\.\d+)?\s*percent\b",
    r"(?:response rate|cure rate|efficacy|hazard ratio|odds ratio)\s+of\s+\d",
    r"\d+\s+of\s+\d+\s+patients\b",
    r"p\s*[<=]\s*0?\.\d+",                                          # p<0.05
]


def gate(out, errors):
    del FAIL[:]

    check("all manifest diseases passed the provenance handshake (no fail-closed errors)", not errors)
    if errors:
        for e in errors:
            print(f"        - {e}")

    # every emitted disease is RESOLVED, gene-handshaked, signature-matched
    ok_resolved = all(
        r["lead_corrective_lever"]["modality_signature_matched"].lower()
        in r["lead_corrective_lever"]["agent_class_frozen"].lower()
        for r in out["diseases"].values()
    )
    check("every emitted disease's signature is a substring of its frozen agent_class", ok_resolved)

    # every inherited system resolved to a real γ or a declared anchor
    ok_resolved_sys = True
    for r in out["diseases"].values():
        for s in r["inherited_systems"]:
            if s["donor_kind"] == "organ_master_gamma" and not isinstance(s["gamma"], (int, float)):
                ok_resolved_sys = False
            if s["donor_kind"] == "compartment_anchor" and s["gamma"] is not None:
                ok_resolved_sys = False
    check("every inherited system resolves to a real organ-master γ or a declared compartment anchor", ok_resolved_sys)

    # reach classification is internally consistent: REACHED iff class in modality reaches
    ok_reach = True
    for r in out["diseases"].values():
        reaches = set(r["modality_reach_model"]["reaches_classes"])
        for s in r["inherited_systems"]:
            want = "REACHED" if s["reach_class"] in reaches else "GAP"
            if s["reach"] != want:
                ok_reach = False
    check("reach/gap is consistent (REACHED iff compartment class in modality reach set)", ok_reach)

    # every GAP surfaces a next-direction; reach/gap partition the systems
    ok_part = True
    for r in out["diseases"].values():
        sys_n = r["reach_summary"]["n_systems"]
        if len(r["reach_summary"]["reached"]) + len(r["reach_summary"]["gap"]) != sys_n:
            ok_part = False
        if len(r["next_directions"]) != len(r["reach_summary"]["gap"]):
            ok_part = False
    check("reached + gap partition every inherited system; each gap yields one next-direction", ok_part)

    # MODALITY_REACH internal: reaches and misses disjoint
    ok_disjoint = all(not (v["reaches"] & v.get("misses", set())) for v in MODALITY_REACH.values())
    check("modality reach model: reaches ∩ misses = ∅ for every modality", ok_disjoint)

    # exclusion gate (§6) holds
    check("exclusion gate (VP_FRAMEWORK_MAP §6) PASS -- no kit disease collides with a sibling major disease",
          out["exclusion_gate"]["status"] == "PASS")

    # FIREWALL: no asserted numeric magnitude leaked into the artifact (γ + journal cites are not magnitudes)
    text = _serialize(out).lower()
    leaked = [p for p in MAGNITUDE_PATTERNS if re.search(p, text)]
    if leaked:
        print(f"        - magnitude leak patterns: {leaked}")
    check("no asserted numeric magnitude (dose/efficacy/rate/p-value) in the artifact (firewall)", not leaked)

    return not FAIL


def _negative_teeth():
    """Synthetic, in-memory teeth: corruptions the module MUST reject."""
    reg, man, _ = _load_inputs()
    results = []

    # (a) wrong signature -> handshake must reject
    man_bad = copy.deepcopy(man)
    victim = sorted(man_bad["diseases"].keys())[0]
    man_bad["diseases"][victim]["lead_modality_signature"] = "ZZZ_not_in_agent_class"
    errs = []
    rec = _build_disease_record(victim, man_bad["diseases"][victim], reg,
                                _frozen_analysis(victim), errs)
    results.append(("bad-signature rejected", rec is None and any("signature" in e for e in errs)))

    # (b) wrong gene -> gene handshake must reject
    man_bad2 = copy.deepcopy(man)
    man_bad2["diseases"][victim]["causal_gene"] = "WRONGGENE"
    errs2 = []
    rec2 = _build_disease_record(victim, man_bad2["diseases"][victim], reg,
                                 _frozen_analysis(victim), errs2)
    results.append(("bad-gene rejected", rec2 is None and any("gene handshake" in e for e in errs2)))

    # (c) injected excluded major disease -> exclusion gate must catch it
    man_bad3 = copy.deepcopy(man)
    man_bad3["diseases"]["renal_cell_carcinoma"] = {
        "disease": "Renal cell carcinoma", "causal_gene": "VHL",
        "lead_lever_frozen": {"lever": "restrain"}, "lead_modality": "x",
        "lead_modality_signature": "x", "inherited_systems": [], "falsifier": {},
        "intractable_rationale": "x",
    }
    errs3 = []
    audit = _exclusion_gate(man_bad3, reg, errs3)
    results.append(("excluded-major-disease collision caught", audit["status"] == "FAIL"))

    # (d) reach classification spot-checks
    spot = (
        COMPARTMENT_CLASS["pns_peripheral_nerve"] not in MODALITY_REACH["enzyme_replacement_iv"]["reaches"]  # ERT misses PNS
        and COMPARTMENT_CLASS["ocular_cornea"] in MODALITY_REACH["metal_chelator_systemic"]["reaches"]       # chelator reaches cornea
        and COMPARTMENT_CLASS["renal"] not in MODALITY_REACH["melanocortin4_agonist"]["reaches"]             # MC4R agonist misses kidney
        and COMPARTMENT_CLASS["cns"] in MODALITY_REACH["mtor_inhibitor_systemic"]["reaches"]                 # rapalogue reaches CNS
    )
    results.append(("reach spot-checks (ERT/PNS gap, chelator/cornea reach, MC4R/renal gap, mTOR/CNS reach)", spot))

    return results


def selftest():
    """TEETH: byte-identical rebuild (determinism) + structural/firewall gate + negative teeth."""
    out1, e1 = build_map()
    out2, e2 = build_map()
    deterministic = _serialize(out1) == _serialize(out2) and e1 == e2
    structural = gate(out1, e1)

    neg = _negative_teeth()
    for name, ok in neg:
        check(f"negative-teeth: {name}", ok)
    negative_ok = all(ok for _n, ok in neg)

    ok = deterministic and structural and negative_ok
    print(f"  [self-test] system-inheritance teeth: deterministic-rebuild={deterministic}  "
          f"gate={structural}  negative-teeth={negative_ok}  -> {'OK' if ok else 'BROKEN'}")
    return ok


# ==================================================================================================
# main
# ==================================================================================================
if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)

    out, errors = build_map()
    payload = _serialize(out)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(payload + "\n")

    teeth_ok = selftest()
    digest = hashlib.sha256((payload + "\n").encode("utf-8")).hexdigest()
    rel_out = os.path.relpath(OUT, ROOT)
    result = {
        "title": "Multi-system inheritance map for intractable disease (VP_SPEC v1.8; ROADMAP V)",
        "native_to": "vp_disease_emergence_kit (ROADMAP V); read-only over the frozen siblings + per-disease freeze",
        "doi_kit": DOI_KIT,
        "files": [rel_out],
        "sha256": {rel_out: digest},
        "counts": out["counts"],
        "overall": "PASS" if teeth_ok else "FAIL",
    }
    if "--write" in sys.argv:
        json.dump(result, open(FREEZE, "w"), indent=1, sort_keys=True)
        print(f"  wrote {os.path.relpath(FREEZE, ROOT)}")

    print("Multi-system inheritance map  [NATIVE / ROADMAP V]")
    print(f"  wrote {rel_out}  {digest[:16]}  ({len(payload)+1} B)")
    c = out["counts"]
    print(f"  diseases={c['diseases']}  inherited_links={c['inherited_system_links']}  "
          f"γ-systems={c['organ_systems_with_measured_gamma']}  "
          f"reached={c['compartments_reached']}  gap(next-direction)={c['compartments_gap_next_direction']}")
    print(f"OVERALL: {result['overall']}")
    sys.exit(0 if teeth_ok else 1)
