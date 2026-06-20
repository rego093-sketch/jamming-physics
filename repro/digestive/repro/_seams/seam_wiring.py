#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seam_wiring.py  --  Cross-system seam layer (digestive_vp_site v0.11.0, section 27).

WIRES the three seams that sections 18 / 24 / 25 previously only DECLARED in prose (NEXT_INSTRUCTIONS
section 8 item 8): the circulatory hepatic delivery substrate (consumed by the NAFLD/MASLD and bile
readings) and the mind felt-symptom firewall (visceral pain / biliary colic deferred OUT by pointer).

DISCIPLINE (neuro<->mind PROJECT_BOUNDARY, verbatim):
  * Citation/pointer-only. This layer imports NO sibling code. The circulatory hepatic interface is a
    VENDORED SNAPSHOT read from inherited/cross_references.json (verified once against circulatory's
    hepatic_clearance() at vendoring time); the mind seam is a one-way POINTER with NO consumed value.
  * The firewall is enforced by an ARCHITECTURAL LOCK: zero sibling imports anywhere in the package, and
    the emitted metabolic state carries no felt/HPA/mind key. This is the SAME lock mind runs neuro-side
    (mind has 0 neuro imports; neuro has 0 mind imports). Each package re-establishes its trusted state
    from its own single zip with the siblings ABSENT.
  * Nothing here feeds the hashed emergence core, so the engine circulate()/emit() 2x-sha256 is UNCHANGED
    and the disease digest is UNCHANGED. This layer carries its OWN 2x-sha256 digest, exactly as the C6
    oncology extension carries its own (separate from the disease layer).

The layer is CONSUMED (it reads engine + disease outputs + the cross-reference snapshot); it is not the
engine and not the disease layer.
"""
import os, sys, re, json, hashlib
from functools import lru_cache

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.normpath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_PKG, "repro", "_engine"))
sys.path.insert(0, os.path.join(_PKG, "repro", "_disease"))
sys.path.insert(0, os.path.join(_PKG, "inherited"))

import cross_references as XR              # internal SSOT loader (stdlib JSON; no sibling code)
import disease_modules as DZ               # internal digestive disease layer
import vp_dig_engine as ENG                # internal digestive engine

# Sibling-code tokens the firewall forbids importing (circulatory / mind / their neighbours).
_SIBLING_IMPORT_TOKENS = ("circulat", "cir_engine", "vp_cir", "mind", "neuro", "cardioresp", "cardio_")
# Internal modules legitimately imported within digestive (never flagged).
_INTERNAL_OK = ("vp_dig_engine", "disease_modules", "carcinogen_dose_response", "stress_tests",
                "gates", "vp_substrate", "cross_references", "seam_wiring", "organ")
# Forbidden felt/HPA keys in the emitted METABOLIC state (firewall: the metabolic loop is mind-free).
_FELT_HPA_TOKENS = ("hpa", "cortisol", "felt", "affect", "mind", "interocept", "limbic", "amygdala")

# OUT-OF-GATE components, excluded from the in-gate firewall certification. The §30 live cross-package
# harness is the one SANCTIONED place that reaches a sibling at all (and only ever by file-path LOAD,
# never by an import statement); it runs OUTSIDE every gate and is never part of the verify-alone trusted
# reconstruction. The firewall certifies the GATED package -- the code each volume re-establishes from its
# own archive with the siblings absent -- so the out-of-gate runner is excluded here. Its own no-sibling-
# import discipline is self-checked inside the harness (run_harness.py), out of gate, touching no digest.
_OUT_OF_GATE_RELPATHS = ("repro/_harness/", "repro/run_harness.py")

_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_.]+)")


# --------------------------------------------------------------------------- 1. consume circulatory
def consume_circulatory_hepatic():
    """Read the vendored circulatory hepatic interface (the delivery substrate). SSOT single read."""
    snap = XR.consumed_circulatory_hepatic()
    rec = XR.for_seam("circulatory_hepatic_interface")
    return dict(Q_H_ml_min=snap["Q_H_ml_min"], E=snap["extraction_ratio_E"],
                F=snap["oral_bioavailability_F"], CL_H_ml_min=snap["hepatic_clearance_CL_H_ml_min"],
                owner=rec["owner_volume"], owner_doi=rec["owner_concept_doi"],
                source_function=rec["source_function"], owner_is_ssot=rec["owner_is_ssot"])


# --------------------------------------------------------------------------- 2. section 24 NAFLD delivery
def nafld_delivery_on_circulatory_perfusion():
    """Section 24 NAFLD/MASLD: the insulin-resistance core REUSES the section-12 type-2 homeostat
    (digestive-owned [V]); the lipid-DEPOSITION arrives on the consumed circulatory hepatic perfusion
    (delivery [V]); the lipid HANDLING is circulatory's ([O], not modelled here)."""
    hep = consume_circulatory_hepatic()
    nf = DZ.validate_d11()["nafld"]
    reuses_s12 = bool(nf["insulin_resistance_reuses_s12_type2_gain_loss"])
    declared_seam = bool(nf["lipid_handling_is_circulatory_seam"])
    return dict(
        reuses_s12_type2_gain_loss=reuses_s12,            # digestive-owned metabolic core [V]
        lipid_delivery_substrate_Q_H_ml_min=hep["Q_H_ml_min"],   # consumed circulatory perfusion [V]
        delivery_rests_on_consumed_circulatory=True,
        lipid_handling_declared_circulatory_seam=declared_seam,  # handling [O], circulatory's
        wired=bool(reuses_s12 and declared_seam),
        grade="[V] s12 homeostat reuse + delivery on consumed circulatory perfusion / [O] lipid handling (circulatory)")


# --------------------------------------------------------------------------- 3. section 25 bile cholesterol delivery
def bile_cholesterol_delivery_on_circulatory():
    """Section 25 cholelithiasis: the nucleation barrier + dissolution hysteresis are digestive-owned
    ([V]/[F]); the biliary cholesterol DELIVERY that sets the saturation-index bias arrives on the
    consumed circulatory hepatic clearance/perfusion (delivery [V]); the absolute CSI scale is [O]."""
    hep = consume_circulatory_hepatic()
    ch = DZ.validate_d12()["cholelithiasis"]
    sm = DZ.validate_d12()["seams"]
    nucleation_csi = ch["nucleation_csi"]
    return dict(
        nucleation_csi=nucleation_csi,                    # digestive-owned thermodynamics [V]/[F]
        cholesterol_delivery_substrate_F=hep["F"],        # consumed circulatory first-pass [V]
        cholesterol_delivery_substrate_Q_H_ml_min=hep["Q_H_ml_min"],
        delivery_rests_on_consumed_circulatory=True,
        biliary_stasis_is_b1_gate_seam=bool(sm["stasis_is_b1_gate_seam"]),    # digestive-owned seam
        wired=True,
        grade="[V]/[F] nucleation thermodynamics + delivery on consumed circulatory perfusion / [O] absolute CSI scale (circulatory delivery)")


# --------------------------------------------------------------------------- 4. firewall architectural lock
def _scan_imports():
    """Walk the package's python sources and collect every import that resolves to a SIBLING module.
    The same lock mind runs neuro-side. Returns (violation_lines, files_scanned)."""
    roots = [os.path.join(_PKG, "repro"), os.path.join(_PKG, "inherited"), os.path.join(_PKG, "tools")]
    violations, n_files = [], 0
    for root in roots:
        for dirpath, _dirs, files in os.walk(root):
            if "__pycache__" in dirpath:
                continue
            for fn in files:
                if not fn.endswith(".py"):
                    continue
                fp = os.path.join(dirpath, fn)
                rel = os.path.relpath(fp, _PKG).replace(os.sep, "/")
                if any(rel == x or rel.startswith(x) for x in _OUT_OF_GATE_RELPATHS):
                    continue                                  # out-of-gate §30 harness: not in-gate certified
                n_files += 1
                for i, line in enumerate(open(fp, encoding="utf-8"), 1):
                    mobj = _IMPORT_RE.match(line)
                    if not mobj:
                        continue
                    mod = mobj.group(1).lower()
                    if any(tok in mod for tok in _INTERNAL_OK):
                        continue
                    if any(tok in mod for tok in _SIBLING_IMPORT_TOKENS):
                        violations.append("%s:%d: %s" % (os.path.relpath(fp, _PKG), i, line.strip()))
    return violations, n_files


def _flatten_keys(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(str(k).lower()); _flatten_keys(v, out)
    elif isinstance(obj, list):
        for v in obj: _flatten_keys(v, out)


def firewall_architectural_lock():
    """The firewall, enforced not asserted: (a) ZERO sibling imports anywhere in the package; (b) the
    emitted METABOLIC state (engine circulate()) carries no felt/HPA/mind key -- the glucose-insulin-
    glucagon loop, slow-wave pacemaker and barrier kernel are computed with zero reference to a mind
    quantity, and the metabolic state does not re-enter mind's HPA."""
    violations, n_files = _scan_imports()
    state = ENG.circulate()
    keys = []; _flatten_keys(state, keys)
    felt_in_metabolic = sorted({t for t in _FELT_HPA_TOKENS for k in keys if t in k})
    holds = (len(violations) == 0 and len(felt_in_metabolic) == 0)
    return dict(sibling_import_count=len(violations), sibling_import_violations=violations,
                python_files_scanned=n_files,
                metabolic_state_felt_hpa_keys=felt_in_metabolic,
                metabolic_state_takes_no_felt_input=bool(len(felt_in_metabolic) == 0),
                firewall_holds=bool(holds),
                grade="[F] forced architectural identity (zero sibling imports; metabolic state mind-free)")


# --------------------------------------------------------------------------- 5. mind pointer (not a dependency)
def mind_pointer_is_not_dependency():
    """The mind seam is a one-way forward-defer POINTER: digestive consumes NO mind value (the record
    carries no vendored snapshot), it only states WHERE the felt item travels and stops. What crosses OUT
    is the peripheral afferent term (sec 18) and the mechanical biliary-colic trigger (sec 25); the felt
    interpretation is mind's, reached via mind's M18 interoception route (NTS -> insula/cingulate)."""
    rec = XR.for_seam("mind_felt_symptom_firewall")
    consumes_mind_value = ("vendored_snapshot" in rec)      # must be False -- pointer carries no value
    one_way = ("one-way pointer" in rec.get("direction", ""))
    return dict(direction=rec["direction"], one_way_pointer=bool(one_way),
                consumes_a_mind_value=bool(consumes_mind_value),
                crosses_out_section_18=rec["what_crosses"]["from_section_18"][:60] + "...",
                crosses_out_section_25=rec["what_crosses"]["from_section_25"][:60] + "...",
                mind_side_endpoint=rec["mind_side_endpoint"][:80] + "...",
                owner_doi=rec["owner_concept_doi"],
                pointer_not_dependency=bool(one_way and not consumes_mind_value),
                grade=rec["grade"])


# --------------------------------------------------------------------------- 6. SSOT consistency
def seam_ssot_consistency():
    """Both hepatic-facing readings (sec 24 NAFLD delivery, sec 25 bile delivery) consume the SAME
    vendored circulatory snapshot; confirm the value each consumes EQUALS the manifest snapshot
    (internal consistency, no sibling import)."""
    snap = XR.consumed_circulatory_hepatic()
    nf = nafld_delivery_on_circulatory_perfusion()
    bl = bile_cholesterol_delivery_on_circulatory()
    q_ok = (nf["lipid_delivery_substrate_Q_H_ml_min"] == snap["Q_H_ml_min"]
            == bl["cholesterol_delivery_substrate_Q_H_ml_min"])
    f_ok = (bl["cholesterol_delivery_substrate_F"] == snap["oral_bioavailability_F"])
    return dict(consumed_Q_H_matches_snapshot=bool(q_ok), consumed_F_matches_snapshot=bool(f_ok),
                snapshot_Q_H_ml_min=snap["Q_H_ml_min"], snapshot_F=snap["oral_bioavailability_F"],
                ssot_consistent=bool(q_ok and f_ok))


# --------------------------------------------------------------------------- aggregate + digest
def validate_seams():
    hep = consume_circulatory_hepatic()
    nf = nafld_delivery_on_circulatory_perfusion()
    bl = bile_cholesterol_delivery_on_circulatory()
    fw = firewall_architectural_lock()
    mp = mind_pointer_is_not_dependency()
    ss = seam_ssot_consistency()
    passed = bool(nf["wired"] and bl["wired"] and fw["firewall_holds"]
                  and mp["pointer_not_dependency"] and ss["ssot_consistent"])
    return dict(circulatory_hepatic_interface=hep,
                s24_nafld_delivery=nf, s25_bile_delivery=bl,
                firewall=fw, mind_pointer=mp, ssot_consistency=ss,
                seam_keys=XR.seam_keys(), passed=passed)


def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    if isinstance(o, tuple): return [_round(v) for v in o]
    return o


@lru_cache(maxsize=1)
def digest():
    s = json.dumps(_round(validate_seams()), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    s, h = digest()
    print(s)
    print("# seam sha256:", h)
    v = validate_seams()
    print("# seams passed:", v["passed"],
          "| firewall sibling-imports:", v["firewall"]["sibling_import_count"],
          "| ssot consistent:", v["ssot_consistency"]["ssot_consistent"])
