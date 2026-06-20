#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
carcinogen_dose_response.py  --  Musculoskeletal ONCOLOGY module (load-bearing class).

VP-NATIVE CANCER MECHANISM (shared kernel): a cell-fate is the SAME R19 bistable switch used to emerge
the organ. A carcinogen acts as a SUSTAINED aberrant drive h_c that LOWERS the escape barrier out of the
healthy basin; the malignant-crossing rate is Kramers-like

        rate(h_c) = rate0 * exp( -barrier_eff(h_c) / scale ),   barrier_eff -> 0 as |h_c| -> spinodal,

so the dose-response RR(dose) = rate(dose)/rate(0) is MONOTONE and CONVEX (accelerating) -- the signature
of barrier-limited escape. The DISCRIMINANT is this SHAPE against a CITED epidemiological anchor, NOT an
absolute incidence.

LINEAGE MAPPING (uses the measured organ gamma; never fitted):
  osteosarcoma            <- osteoblast-lineage switch = RUNX2 (bone)   gamma = 1.2414
  soft-tissue sarcoma     <- myogenic-lineage switch   = MYOD1 (muscle) gamma = 1.4933
                             (rhabdomyosarcoma: MYOD1 is the canonical rhabdomyosarcoma marker)

GRADES (VP-SPEC C3):
  - Kramers dose-response SHAPE (monotone, convex, RR>1) ........ [V] verified on the substrate
  - radiation RR for bone sarcoma rises with dose .............. [L] cited (radium dial painters; Tucker 1987; UNSCEAR)
  - absolute incidence (cases / person-year) .................. [O] kernel gives RELATIVE risk only; baseline hazard not fixed
  - osteosarcoma is mostly GENETIC, not environmental .......... [O] honest scope limit (RB1, TP53/Li-Fraumeni, Paget); do NOT overclaim
  - chemical soft-tissue-sarcoma dose-response ................. [O] no clean cited dose-response anchor (confounded, low incidence)
"""
import os, sys, math, json
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal
_HERE = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

def _gene_gamma(name):
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"][name]["gamma"]

SITES = [
    {"site": "osteosarcoma", "lineage_master": "RUNX2", "organ": "bone",
     "carcinogens": "ionizing radiation (therapeutic/occupational)",
     "anchor": "radiation RR for bone sarcoma rises with dose [L] (radium dial painters; Tucker et al. 1987; UNSCEAR); "
               "environmental-carcinogen link WEAK -> osteosarcoma mostly genetic [O]; do not overclaim",
     "aetiology_caveat": "osteosarcoma is predominantly GENETIC (RB1, TP53/Li-Fraumeni, Paget), not environmental [O]: "
                         "the dose-response applies only to the radiation-attributable fraction; not overclaimed",
     "has_dose_anchor": True},
    {"site": "soft-tissue sarcoma (rhabdomyosarcoma-type)", "lineage_master": "MYOD1", "organ": "skeletal_muscle",
     "carcinogens": "ionizing radiation; some chemicals",
     "anchor": "radiotherapy-induced sarcoma RR [L]; chemical dose-response has NO clean cited anchor [O] "
               "(confounded, low incidence) -> radiation modelled, chemicals reported as baseline-crossing only",
     "aetiology_caveat": "chemical soft-tissue-sarcoma dose-response has NO clean cited anchor [O] (confounded, low "
                         "incidence): only the radiation channel is modelled; chemicals reported as baseline-crossing only",
     "has_dose_anchor": True},
    {"site": "chondrosarcoma", "lineage_master": "SOX9", "organ": "cartilage",
     "carcinogens": "IDH1/2 neomorphic mutation (D-2-hydroxyglutarate); NOT an environmental dose",
     "anchor": "cartilage-lineage tumour mapped to the SOX9 chondrocyte switch; aetiology is metabolic/genetic "
               "(IDH1/2), not an environmental exposure -> no dose anchor [O]; the kernel demonstrates the "
               "barrier-lowering SHAPE under a sustained aberrant drive only",
     "aetiology_caveat": "chondrosarcoma is driven by IDH1/2 neomorphic metabolism (2-HG), not an environmental "
                         "dose [O]: there is no exposure dose-response to anchor; the SHAPE is shown for a sustained "
                         "aberrant drive (the metabolic oncometabolite), and the dose axis is the normalized drive, not a cited exposure",
     "has_dose_anchor": False},
    {"site": "Ewing sarcoma", "lineage_master": "RUNX2", "organ": "bone",
     "carcinogens": "EWSR1-FLI1 fusion oncoprotein (constitutive driver); NOT an environmental dose",
     "anchor": "fusion-driven small-round-cell tumour; cell-of-origin DEBATED (mesenchymal/neural-crest stem cell), "
               "so the bone-mesenchyme context gamma (RUNX2) is a stand-in only -> lineage assignment [O]; "
               "the driver is the EWSR1-FLI1 fusion, not master-gene dosage; no environmental dose anchor [O]",
     "aetiology_caveat": "Ewing sarcoma is driven by the EWSR1-FLI1 FUSION with a DEBATED cell-of-origin [O]: it is not "
                         "one of the four measured lineage switches, so RUNX2 is only a bone-mesenchyme context stand-in; "
                         "there is no environmental dose-response to anchor; the kernel shows the barrier-lowering SHAPE for "
                         "a sustained fusion-like aberrant drive, with the dose axis = normalized drive, not a cited exposure",
     "has_dose_anchor": False},
]

# ---- kernel -----------------------------------------------------------------
def barrier_eff(gamma, h_c):
    """Escape barrier under a sustained aberrant drive h_c. The bistable barrier b0=gamma^2/4 is lowered
    as the drive approaches the spinodal sp=2(gamma/3)^1.5 (where the healthy basin vanishes)."""
    b0 = barrier(gamma); sp = spinodal(gamma)
    frac = min(max(abs(h_c) / sp, 0.0), 0.999) if sp > 0 else 0.0
    return b0 * (1.0 - frac)

def crossing_rate(gamma, h_c, rate0=1.0, scale=None):
    """Kramers-like malignant-crossing rate (barrier-limited escape)."""
    scale = scale if scale is not None else max(barrier(gamma), 1e-6)
    return rate0 * math.exp(-barrier_eff(gamma, h_c) / scale)

def relative_risk(gamma, dose_frac):
    """RR at a normalized exposure dose_frac in [0,1) = fraction of the spinodal aberrant drive.
    The absolute dose->drive scale is NOT fitted (that is the [O] piece); we sweep the normalized drive
    and verify the SHAPE, which is the anchor-free qualitative signature of barrier-limited escape."""
    sp = spinodal(gamma)
    h_c = dose_frac * sp
    r0 = crossing_rate(gamma, 0.0)
    return crossing_rate(gamma, h_c) / r0 if r0 > 0 else float("inf")

def dose_response_curve(gamma, doses=None):
    if doses is None:
        doses = [round(0.05 * i, 3) for i in range(0, 19)]   # 0.00 .. 0.90 fraction of spinodal
    return [{"dose_frac": d, "RR": relative_risk(gamma, d)} for d in doses]

# ---- verification -----------------------------------------------------------
def _verify_site(site):
    g = _gene_gamma(site["lineage_master"])
    curve = dose_response_curve(g)
    RR = [p["RR"] for p in curve]
    rr0_ok      = abs(RR[0] - 1.0) < 1e-9                                  # RR(0) == 1 by construction
    monotone    = all(RR[i] <= RR[i+1] + 1e-12 for i in range(len(RR)-1)) # rises with dose
    # convex / accelerating: discrete 2nd difference non-negative over the sweep (Kramers signature)
    d2 = [RR[i+1] - 2*RR[i] + RR[i-1] for i in range(1, len(RR)-1)]
    convex      = all(x >= -1e-9 for x in d2)
    elevated    = RR[-1] > 1.5                                            # meaningful excess at high dose
    shape_ok    = rr0_ok and monotone and convex and elevated
    # The dose AXIS meaning depends on whether a cited environmental exposure exists: for radiation sites it is a
    # (normalized) exposure dose [L]; for fusion/metabolic-driven sites it is the normalized aberrant DRIVE, and the
    # dose-response is a SHAPE demonstration only (aetiology genetic/metabolic [O]).
    if site.get("has_dose_anchor"):
        shape_grade = "dose-response SHAPE monotone+convex+RR>1 [V]; radiation RR anchor [L]"
        axis = "normalized exposure dose (fraction of spinodal drive)"
    else:
        shape_grade = ("barrier-lowering SHAPE monotone+convex+RR>1 [V] under a sustained aberrant drive; "
                       "aetiology genetic/metabolic, NO environmental dose anchor [O]")
        axis = "normalized aberrant drive (fraction of spinodal) -- NOT a cited exposure dose"
    open_items = [
        "absolute incidence (cases/person-year) [O]: kernel gives RELATIVE risk only; baseline hazard not fixed by the substrate",
        site["aetiology_caveat"],
    ]
    return {"site": site["site"], "lineage_master": site["lineage_master"], "organ": site["organ"],
            "gamma": round(g, 6), "carcinogens": site["carcinogens"], "anchor": site["anchor"],
            "dose_axis_meaning": axis, "has_dose_anchor": bool(site.get("has_dose_anchor")),
            "RR_at_dose": {"0.0": round(RR[0], 4), "0.45": round(relative_risk(g, 0.45), 4),
                           "0.90": round(RR[-1], 4)},
            "RR0_is_one": rr0_ok, "monotone_in_dose": monotone, "convex_accelerating": convex,
            "elevated_at_high_dose": elevated,
            "shape_grade": shape_grade,
            "open_items": open_items,
            "status": "PASS" if shape_ok else "FAIL",
            "curve": [{"dose_frac": p["dose_frac"], "RR": round(p["RR"], 4)} for p in curve]}

def run_oncology():
    sites = [_verify_site(s) for s in SITES]
    return {"kernel": "R19 barrier-lowering -> Kramers crossing -> RR(dose); SHAPE is the discriminant, absolute incidence [O]",
            "sites": sites,
            "all_sites_shape_ok": all(s["status"] == "PASS" for s in sites),
            "grade_summary": "dose-response shape [V] / radiation RR anchor [L] / absolute incidence + genetic-dominance + chemical anchor [O]"}

def status():
    return run_oncology()

if __name__ == "__main__":
    print(json.dumps(run_oncology(), ensure_ascii=False, indent=2))
