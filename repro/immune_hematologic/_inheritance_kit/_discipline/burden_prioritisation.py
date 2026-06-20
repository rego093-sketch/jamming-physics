#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
burden_prioritisation.py  --  D2: burden/unmet-need/tractability-weighted TARGET prioritisation.

INHERITED TECHNIQUE: analgesic_threshold_logic_v2_0 / M10 (10-burden-prioritisation),
DOI 10.5281/zenodo.20733420. The analgesic package ranks molecular TARGETS by DECLARED
burden/unmet/druggability weights (cited 1-5 tiers), never drugs or doses, and carries gamma-|h_sp|
ALONGSIDE but never folds it into the score. This is the immune analogue: it ranks the immune /
hematologic disease-treatment AXES already proven in this volume (the T27-T33 axis + core malignancy /
inflammation) by declared public-health weights, so a research team can see WHERE a basin-acting lever
would relieve the most suffering first.

DISCIPLINE (identical to the inherited module):
  - weights are DECLARED up front (not reverse-fit to produce any ranking);
  - tiers are coarse ordinals (1..5) with a cited public-health basis (GBD/WHO-class burden), NOT
    precise statistics;
  - the score ranks intervention TARGETS / disease axes, NEVER a drug, a dose, an efficacy, or a patient;
  - gamma and |h_sp| of the representative organ are carried for CONTEXT only and are NEVER folded
    into the score (the firewall: a promoter switch-threshold read is not a disease-burden number).

Gate (fail-closed): weights sum to 1; every target carries all three declared tiers in 1..5 and a
cited basis; the ranking is a pure function of the declared weights x tiers (reproducible); the
firewall field is present. Run: python3 burden_prioritisation.py -> expected/priority_ranking.json
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.normpath(os.path.join(HERE, "..", ".."))
for sub in ("_engine",):
    sys.path.insert(0, os.path.join(PKG, "repro", sub))
sys.path.insert(0, os.path.join(PKG, "inherited"))
import vp_imm_engine as ENG
import vp_substrate as VS

# ---- DECLARED weights (fixed before any ranking is computed; not reverse-fit) ----
WEIGHTS = {"burden": 0.40, "unmet_durability": 0.40, "tractability_basin_lever": 0.20}

# ---- the disease-treatment TARGETS already established in this volume ----
# tiers are DECLARED coarse ordinals (1 lowest .. 5 highest) with a cited public-health basis.
#   burden                  = global disease burden (prevalence x severity), GBD/WHO-class ordinal
#   unmet_durability        = how poorly current therapy DURABLY cures (proportion relapsing/failed)
#   tractability_basin_lever= how cleanly THIS volume names a basin-acting (durable-class) lever
# organ = representative organ whose gamma/|h_sp| is carried ALONGSIDE (never scored)
TARGETS = [
    {"id": "HEME_MALIGNANCY", "axis": "hematologic malignancy (AML/APL/leukemia-lymphoma)",
     "lever": "A basin re-flip / D surveillance restoration", "organ": "bone_marrow_hematopoiesis",
     "burden": 5, "unmet_durability": 4, "tractability_basin_lever": 5,
     "basis": "GBD: leukaemia+lymphoma high mortality; two clean durable cures exist (APL=ATRA[L], CAR-T=D[L]) -> high tractability"},
    {"id": "AUTOIMMUNE_RETOLERIZE", "axis": "systemic autoimmunity (re-tolerization, T27)",
     "lever": "re-tolerization across the saddle-node", "organ": "lymphoid_adaptive",
     "burden": 5, "unmet_durability": 5, "tractability_basin_lever": 3,
     "basis": "GBD: autoimmune diseases ~5-8% prevalence, lifelong; standard care is suppression-only (relapse on withdrawal) -> high unmet durability"},
    {"id": "SEPSIS_LATCH_BREAK", "axis": "systemic inflammatory latch / sepsis (T31)",
     "lever": "latch-break within the break window", "organ": "lymphoid_adaptive",
     "burden": 5, "unmet_durability": 5, "tractability_basin_lever": 2,
     "basis": "GBD: sepsis ~11M deaths/yr; no durable latch-break therapy in practice (window narrow) -> high burden+unmet, low present tractability"},
    {"id": "TRANSPLANT_ALLOTOL", "axis": "transplant rejection (allo-tolerance induction, T32)",
     "lever": "tolerance induction (durable) vs lifelong immunosuppression", "organ": "lymphoid_adaptive",
     "burden": 3, "unmet_durability": 4, "tractability_basin_lever": 3,
     "basis": "transplant recipients lifelong on suppression with attendant harm; durable allo-tolerance is the basin-acting goal"},
    {"id": "IMMUNODEFICIENCY_RECON", "axis": "immunodeficiency reconstitution (T30)",
     "lever": "reconstitution above the coverage threshold", "organ": "bone_marrow_hematopoiesis",
     "burden": 3, "unmet_durability": 3, "tractability_basin_lever": 4,
     "basis": "primary+acquired immunodeficiency; reconstitution (HSCT/gene therapy) is an established durable-class route -> good tractability"},
    {"id": "ALLERGY_DESENS", "axis": "allergic sensitization / desensitization (T29)",
     "lever": "desensitization (durable de-escalation)", "organ": "lymphoid_adaptive",
     "burden": 4, "unmet_durability": 3, "tractability_basin_lever": 3,
     "basis": "GBD: allergic disease very high prevalence, mostly low-mortality; immunotherapy offers a durable-class path for a subset"},
    {"id": "IMMUNE_EXHAUSTION", "axis": "immune exhaustion (chronic infection/tumor, T25)",
     "lever": "exhaustion reversal / surveillance restoration", "organ": "lymphoid_adaptive",
     "burden": 4, "unmet_durability": 4, "tractability_basin_lever": 3,
     "basis": "chronic viral infection + tumor escape; checkpoint reversal is a partial, heterogeneous durable-class lever"},
    {"id": "AUTOIMMUNE_CYTOPENIA", "axis": "lineage-targeted autoimmune cytopenia (T33)",
     "lever": "re-tolerization restoring lineage output", "organ": "bone_marrow_hematopoiesis",
     "burden": 2, "unmet_durability": 3, "tractability_basin_lever": 3,
     "basis": "ITP/AIHA/PRCA; relapsing on suppression, output recovers on re-tolerization in the model"},
    {"id": "CHRONIC_INFLAMMATION", "axis": "chronic inflammation containment (T2/T9 hysteresis)",
     "lever": "drive removal below the spinodal (preventive) vs latch containment", "organ": "spleen",
     "burden": 4, "unmet_durability": 3, "tractability_basin_lever": 2,
     "basis": "broad chronic inflammatory burden; once latched the basin persists, so durable cure is hard (mostly containment)"},
    {"id": "EPITOPE_SPREADING", "axis": "epitope spreading (autoimmune progression, T28)",
     "lever": "early re-tolerization before the repertoire broadens", "organ": "lymphoid_adaptive",
     "burden": 2, "unmet_durability": 4, "tractability_basin_lever": 2,
     "basis": "progressive autoimmunity; window for durable reversal narrows as spreading proceeds -> high unmet, low late tractability"},
]


def _score(t):
    return round(sum(WEIGHTS[k] * t[k] for k in WEIGHTS) / (5.0 * sum(WEIGHTS.values())), 6)


def run():
    res = ENG.circulate()
    G = {o["organ"]: o["gamma"] for o in res["organs"]["organs"] if o.get("gamma") is not None}

    ranked = []
    for t in TARGETS:
        g = G.get(t["organ"])
        ctx = None
        if g is not None:
            ctx = {"organ": t["organ"], "gamma": round(g, 6), "h_sp": round(VS.spinodal(g), 6),
                   "note": "carried for CONTEXT only; NEVER folded into the score"}
        ranked.append({"id": t["id"], "axis": t["axis"], "lever": t["lever"],
                       "tiers": {k: t[k] for k in WEIGHTS}, "basis": t["basis"],
                       "score": _score(t), "gamma_context": ctx})
    ranked.sort(key=lambda r: (-r["score"], r["id"]))
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    out = {"title": "D2 burden-weighted TARGET prioritisation (declared weights; ranks targets, not drugs)",
           "inherited_from": "analgesic_threshold_logic_v2_0/M10 (DOI 10.5281/zenodo.20733420)",
           "declared_weights": WEIGHTS,
           "firewall": ("This ranks immune/hematologic intervention TARGETS / disease axes by DECLARED "
                        "public-health burden weights x cited 1-5 tiers. It is NOT a drug ranking, NOT a "
                        "dose, NOT an efficacy or safety claim, and NOT medical advice. gamma/|h_sp| are "
                        "carried for context and are NEVER folded into the score (a promoter switch-threshold "
                        "read is not a disease-burden number). Weights are declared up front, not reverse-fit."),
           "grade": "[V] reproducible function of declared weights x tiers / [O] absolute burden statistics (declared ordinals, not measured here)",
           "ranking": ranked}
    return out


def _gate(out):
    fail = []
    if round(sum(WEIGHTS.values()), 6) != 1.0:
        fail.append("weights_sum!=1")
    for r in out["ranking"]:
        for k in WEIGHTS:
            v = r["tiers"][k]
            if not (isinstance(v, int) and 1 <= v <= 5):
                fail.append("tier_out_of_range:%s.%s" % (r["id"], k))
        if not r.get("basis", "").strip():
            fail.append("missing_basis:%s" % r["id"])
    # ranking must be a pure function of declared weights x tiers (recompute, compare)
    recomputed = sorted(out["ranking"], key=lambda r: (-_score(r["tiers"]), r["id"]))
    if [r["id"] for r in recomputed] != [r["id"] for r in out["ranking"]]:
        fail.append("ranking_not_pure_function")
    if not out.get("firewall", "").strip():
        fail.append("missing_firewall")
    return fail


if __name__ == "__main__":
    out = run()
    fail = _gate(out)
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    out["overall"] = "PASS" if not fail else "FAIL"
    out["failures"] = fail
    json.dump(out, open(os.path.join(HERE, "expected", "priority_ranking.json"), "w"), indent=1)
    print("D2 burden-weighted TARGET prioritisation  (declared weights %s)" % WEIGHTS)
    for r in out["ranking"]:
        gc = r["gamma_context"]
        gtxt = ("  [ctx %s g=%.3f |h_sp|=%.3f]" % (gc["organ"], gc["gamma"], gc["h_sp"])) if gc else ""
        print("  #%2d  score=%.3f  %-22s %s%s" % (r["rank"], r["score"], r["id"], r["axis"], gtxt))
    print("  firewall: ranks TARGETS only; gamma/|h_sp| never in score; weights declared not reverse-fit")
    print("OVERALL:", out["overall"], ("" if not fail else fail))
    raise SystemExit(0 if not fail else 1)
