#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
precision_routing.py  --  PRECISION (compartment-restricted) restoration routing.

The analgesic package (analgesic_threshold_logic_v2_0, Zenodo concept DOI 10.5281/zenodo.20733420)
distinguishes a SYSTEMIC threshold-raiser (acts body-wide) from a PRECISION local anaesthetic (a regional
block restricted to the anatomical territory of one nerve). The SAME distinction, re-read for the
setpoint-restoration levers (restoration_levers.py), asks WHERE in the body each lever's compartment of
action sits: can a lever be ROUTED to a single tissue (a precision block), or is its node distributed so
that restoration must act systemically?

This module places every restoration target on a CITED anatomical compartment map and classifies how
localisable its lever is:

  PRECISION  -- the lever's node acts in ONE cited tissue compartment -> a clean regional route
                (the local-anaesthesia analog).                       e.g. UCP1 -> {BAT}, MC4R -> {CNS}.
  REGIONAL   -- 2-3 cited compartments (a small territory) -> a semi-localised route.
                                                                       e.g. ADRB3 -> {BAT, white adipose}.
  SYSTEMIC   -- >=4 cited compartments, OR a distributed immune/stromal node with no single locus ->
                restoration cannot be routed to one place; it acts body-wide. e.g. INSR (ubiquitous), TNF.

Three NAMED routes (the worked examples) span the spectrum honestly:
  * BAT-targeted route          -- the thermogenic-disposal depot (UCP1 precision; ADRB3 adipose-regional).
  * central appetite-axis route -- the hypothalamic setpoint (MC4R precision; LEPR central-dominant) --
                                   anatomically routable but central access is an [O] deliverability obstacle.
  * hepatic glucose-disposal    -- INSR is DISTRIBUTED (systemic); liver + skeletal muscle are its dominant
                                   disposal sub-compartments, so this is a dominant-compartment route, NOT a
                                   clean single-compartment precision -- the honest "you cannot local-block
                                   a body-wide receptor" case.

FIREWALL (binding -- identical discipline to restoration_levers.py, sharpened with a PROOF):
  - The compartment assignment + the routing classification are [F] STRUCTURAL, anchored to CITED anatomy.
  - The routing SPECIFICITY score is a function of the CITED COMPARTMENT COUNT ONLY. gamma (the promoter
    switch-threshold read) is NEVER an input to the routing score; it is carried ALONGSIDE each row as
    structural context, exactly as in the restoration prioritisation.
  - This is PROVEN, not just asserted: gamma_independence_gate() recomputes the whole routing map under a
    perturbed gamma atlas and checks that every routing field (compartments / primary / specificity / tier)
    is byte-identical, while ONLY the carried gamma-context column tracks the perturbation. The routing
    geometry is invariant to gamma; the read is carried but firewalled out of the score.
  - ROUTABILITY [F] (anatomy: which compartment) is DISTINCT from DELIVERABILITY [O] (can an intervention
    reach it). A behind-barrier primary compartment (e.g. CNS behind the blood-brain barrier) carries an
    [O] delivery obstacle; the anatomy stays [F].
  - These are falsifiable HYPOTHESES about the compartment of action, NOT a delivery prescription: no route,
    device, injection, implant, dose, efficacy, or safety claim (enforced by the forbidden-claim scan, which
    extends the analgesic scan with a DELIVERY class).

No tuning: COMPARTMENTS / ROUTING are declared from cited anatomy; the specificity is a parameter-free
reciprocal of the cited compartment count; the gamma read is the inherited measured atlas.
"""
import os, sys, json, copy

_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)  # sibling restoration_levers (reuse the scan machinery)
import restoration_levers as RL
from restoration_levers import _collect_assertion_strings, EXCLUDE_KEY_RE, NEG_RE  # noqa: F401

_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
from vp_substrate import spinodal, barrier  # gamma -> R19 read (carried as context ONLY)


def _gamma_atlas():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]


# ---------------------------------------------------------------------------
#  CITED anatomical compartments (declared, [F] structural -- NOT engine output).
# ---------------------------------------------------------------------------
COMPARTMENTS = {
    "BAT":              "brown adipose tissue (the thermogenic disposal depot)",
    "WHITE_ADIPOSE":    "white adipose tissue (storage + adipokine source)",
    "CNS_HYPOTHALAMUS": "hypothalamic appetite / thermostat circuitry (the central setpoint)",
    "LIVER":            "hepatic glucose output / disposal",
    "SKELETAL_MUSCLE":  "skeletal-muscle insulin-mediated glucose uptake",
    "GUT":              "enteroendocrine hunger-signal source",
    "SYSTEMIC_IMMUNE":  "distributed immune / stromal compartment (no single locus)",
}
_DISTRIBUTED = "SYSTEMIC_IMMUNE"           # a compartment that is itself body-wide
_BARRIER = {"CNS_HYPOTHALAMUS"}            # primary compartments behind an access barrier -> [O] deliverability

# Per target: the CITED compartment list (where the lever's node acts), the PRIMARY (precision-target)
# compartment, the cited anatomical basis, and -- if the primary compartment is behind a barrier -- the
# [O] delivery obstacle. compartments/primary are anatomy, declared, never fitted.
ROUTING = {
    # --- thermogenic-disposal depot -------------------------------------------------
    "UCP1":  dict(compartments=["BAT"], primary="BAT", lever="S2",
                  basis="cited: UCP1 expression is essentially restricted to brown (and beige) adipocytes",
                  obstacle="[O] deliverability: the BAT depot mass is small and variable (recruitable), so reaching it is an open access problem (cited)"),
    "ADRB3": dict(compartments=["BAT", "WHITE_ADIPOSE"], primary="BAT", lever="S2",
                  basis="cited: beta3-adrenergic receptors predominate on adipocytes (brown + white / beige)",
                  obstacle=None),
    # --- central appetite / thermostat ----------------------------------------------
    "MC4R":  dict(compartments=["CNS_HYPOTHALAMUS"], primary="CNS_HYPOTHALAMUS", lever="S2",
                  basis="cited: MC4R energy-balance signalling is hypothalamic (paraventricular nucleus)",
                  obstacle="[O] deliverability: central access is limited by the blood-brain barrier (cited)"),
    "LEPR":  dict(compartments=["CNS_HYPOTHALAMUS", "WHITE_ADIPOSE"], primary="CNS_HYPOTHALAMUS", lever="S1",
                  basis="cited: lipostat-relevant leptin sensing is dominated by hypothalamic neurons; peripheral LEPR also present",
                  obstacle="[O] deliverability: the dominant (central) sensing site is behind the blood-brain barrier (cited)"),
    "GHRL":  dict(compartments=["GUT", "CNS_HYPOTHALAMUS"], primary="GUT", lever="S2",
                  basis="cited: ghrelin is produced in the stomach (gut source) and acts on hypothalamic neurons -- a gut->brain axis",
                  obstacle=None),
    # --- storage node ---------------------------------------------------------------
    "PPARG": dict(compartments=["WHITE_ADIPOSE", "BAT"], primary="WHITE_ADIPOSE", lever="S1",
                  basis="cited: PPAR-gamma is the master adipocyte regulator, dominant in adipose tissue (white, with brown / beige)",
                  obstacle=None),
    # --- hepatic / oxidative glucose disposal ---------------------------------------
    "INSR":  dict(compartments=["LIVER", "SKELETAL_MUSCLE", "WHITE_ADIPOSE", "CNS_HYPOTHALAMUS"],
                  primary="LIVER", lever="S1",
                  basis="cited: the insulin receptor is ubiquitously expressed; the metabolically dominant disposal / sensing compartments are liver, skeletal muscle, adipose, and brain",
                  obstacle="[O] routability is limited: a body-wide receptor cannot be confined to one compartment; liver + skeletal muscle are the dominant disposal sub-compartments (a dominant-compartment route, not a single-compartment precision)"),
    "PDK4":  dict(compartments=["LIVER", "SKELETAL_MUSCLE"], primary="LIVER", lever="S3",
                  basis="cited: the PDK4 fuel-switch operates in oxidative tissues, dominantly liver and skeletal muscle",
                  obstacle=None),
    # --- distributed sensitiser -----------------------------------------------------
    "TNF":   dict(compartments=["SYSTEMIC_IMMUNE"], primary="SYSTEMIC_IMMUNE", lever="S3",
                  basis="cited: chronic low-grade inflammation is a distributed immune / stromal program with no single tissue locus",
                  obstacle="[O] routability is limited: a distributed program has no single compartment to route to (systemic by nature)"),
}

# Named routes (the worked examples). Membership is by PRIMARY compartment; declared, cited.
NAMED_ROUTES = {
    "BAT-targeted": dict(
        compartment="BAT",
        what="restoration aimed at the brown-fat thermogenic-disposal depot (raise disposal, S2 side)",
        members=["UCP1", "ADRB3"],
        character="the cleanest precision route: UCP1 acts in a single cited compartment"),
    "central appetite-axis": dict(
        compartment="CNS_HYPOTHALAMUS",
        what="restoration aimed at the hypothalamic appetite / thermostat setpoint (cut intake forcing / re-sensitise leptin)",
        members=["MC4R", "LEPR"],
        character="anatomically routable (MC4R single-compartment) but central access is an [O] deliverability obstacle"),
    "hepatic glucose-disposal": dict(
        compartment="LIVER",
        what="restoration aimed at hepatic / oxidative glucose disposal (re-sensitise insulin signalling, remove the PDK4 program)",
        members=["INSR", "PDK4"],
        character="the honest distributed case: INSR is body-wide, so this is a dominant-compartment route (liver + muscle), not a single-compartment precision"),
}


# ---------------------------------------------------------------------------
#  ROUTING CLASSIFICATION  -- parameter-free, from the CITED compartment count ONLY.
#  gamma is NOT read here. (Proven by gamma_independence_gate.)
# ---------------------------------------------------------------------------
def _breadth(compartments):
    """Effective tissue breadth = number of distinct cited compartments; a distributed
    (SYSTEMIC_IMMUNE) node counts as the full compartment universe (maximal breadth)."""
    if _DISTRIBUTED in compartments:
        return len(COMPARTMENTS)
    return len(compartments)


def _tier(compartments):
    if _DISTRIBUTED in compartments:
        return "SYSTEMIC"
    n = len(compartments)
    if n <= 1:
        return "PRECISION"
    if n <= 3:
        return "REGIONAL"
    return "SYSTEMIC"


def _routing_rows(atlas):
    """Build the routing rows. The ROUTING fields are anatomy (no gamma). The gamma read is
    attached ONLY as carried context, so the same function proves the separation when called
    with a perturbed atlas."""
    rows = []
    for sym, r in ROUTING.items():
        comps = list(r["compartments"])
        breadth = _breadth(comps)
        g = atlas.get(sym, {}).get("gamma")
        ctx = (None if g is None
               else dict(gamma=round(float(g), 6), h_sp=round(float(spinodal(g)), 6),
                         barrier=round(float(barrier(g)), 6)))
        rows.append(dict(
            target=sym, lever=r["lever"],
            compartments=comps, primary=r["primary"],
            n_compartments=breadth,
            specificity=round(1.0 / breadth, 6),     # <-- ONLY input is the cited compartment count
            tier=_tier(comps),
            primary_behind_barrier=bool(r["primary"] in _BARRIER),
            delivery_obstacle=r["obstacle"],
            basis=r["basis"],
            gamma_context=ctx,                        # carried ALONGSIDE, NEVER folded into specificity/tier
            grade_routing="[F] structural: compartment of action from cited anatomy (ORDER [F])",
            grade_deliverability=("[O] cited: reaching the primary compartment is an open access problem"
                                  if r["obstacle"] else "[F] no stated access barrier")))
    # order by specificity desc (most precisely routable first) -- structural, NOT a clinical ranking
    rows.sort(key=lambda x: (-x["specificity"], x["target"]))
    return rows


def build_routing_map():
    rows = _routing_rows(_gamma_atlas())
    from collections import Counter
    tier_counts = Counter(x["tier"] for x in rows)
    return dict(
        title="Precision restoration-routing map (PRECISION / REGIONAL / SYSTEMIC by cited compartment)",
        compartments=COMPARTMENTS,
        tiers={"PRECISION": "one cited compartment -> a clean regional route (local-anaesthesia analog)",
               "REGIONAL": "2-3 cited compartments -> a semi-localised route",
               "SYSTEMIC": ">=4 compartments or a distributed node -> restoration acts body-wide"},
        rows=rows,
        tier_distribution=dict(tier_counts),
        named_routes=NAMED_ROUTES,
        firewall=("the compartment of action + the PRECISION/REGIONAL/SYSTEMIC class are [F] STRUCTURAL from "
                  "cited anatomy; the routing SPECIFICITY is a parameter-free reciprocal of the cited "
                  "compartment COUNT and gamma is NEVER an input to it (gamma is carried alongside as the "
                  "promoter switch-threshold context and is firewalled out of the score -- proven by the "
                  "gamma-independence gate). ROUTABILITY [F] (which compartment) is distinct from "
                  "DELIVERABILITY [O] (whether an intervention can reach it). These are falsifiable "
                  "HYPOTHESES about the compartment of action, not a delivery prescription -- no route, "
                  "device, dose, efficacy, or safety claim."))


# ---------------------------------------------------------------------------
#  GAMMA-INDEPENDENCE GATE (the firewall, PROVEN -- not merely asserted).
#  Recompute the routing under a perturbed gamma atlas; the routing geometry must be
#  byte-identical, while ONLY the carried gamma-context column tracks the perturbation.
# ---------------------------------------------------------------------------
def _strip_context(rows):
    """Routing geometry only (everything EXCEPT the carried gamma-context)."""
    out = []
    for r in rows:
        rr = {k: v for k, v in r.items() if k != "gamma_context"}
        out.append(rr)
    return out


def gamma_independence_gate():
    real = _gamma_atlas()
    perturbed = copy.deepcopy(real)
    # perturb every gamma drastically (and None one out) -- a routing that reads gamma WOULD move
    for i, sym in enumerate(sorted(perturbed.keys())):
        if "gamma" in perturbed[sym]:
            perturbed[sym]["gamma"] = None if i == 0 else round(float(perturbed[sym]["gamma"]) * 0.5 + 0.137, 6)
    rows_real = _routing_rows(real)
    rows_pert = _routing_rows(perturbed)
    geom_real = json.dumps(_strip_context(rows_real), ensure_ascii=False, sort_keys=True)
    geom_pert = json.dumps(_strip_context(rows_pert), ensure_ascii=False, sort_keys=True)
    routing_invariant = (geom_real == geom_pert)
    # and confirm the carried context DID track gamma (so the column is genuinely the read, just firewalled)
    ctx_real = [r["gamma_context"] for r in rows_real]
    ctx_pert = [r["gamma_context"] for r in rows_pert]
    context_tracks_gamma = (ctx_real != ctx_pert)
    return dict(
        title="Gamma-independence of the routing score (firewall proof)",
        routing_geometry_invariant_under_gamma_perturbation=bool(routing_invariant),
        carried_context_column_does_track_gamma=bool(context_tracks_gamma),
        overall="PASS" if (routing_invariant and context_tracks_gamma) else "FAIL",
        principle=("the routing compartments / primary / specificity / tier do not change when every gamma is "
                   "perturbed (gamma is not an input to the score); only the alongside gamma-context column "
                   "tracks the perturbation -- the read is carried but firewalled out of the routing."))


# ---------------------------------------------------------------------------
#  ROUTING-ANATOMY HONESTY GATE (fail-closed).  Every assignment is cited; every SYSTEMIC node is
#  honestly flagged (not over-claimed as precision); every behind-barrier primary carries an [O] obstacle.
# ---------------------------------------------------------------------------
def anatomy_honesty_gate():
    m = build_routing_map(); failures = []
    def check(name, cond):
        if not cond: failures.append(name)
        return cond
    for r in m["rows"]:
        check(f"{r['target']} routing cites an anatomical basis", bool(r["basis"].strip()))
        # a distributed / >=4-compartment node must be SYSTEMIC, never sold as precision
        if _DISTRIBUTED in r["compartments"] or r["n_compartments"] >= 4:
            check(f"{r['target']} (distributed) classified SYSTEMIC, not precision", r["tier"] == "SYSTEMIC")
        # a primary compartment behind a barrier must carry an [O] delivery obstacle
        if r["primary_behind_barrier"]:
            ob = (r["delivery_obstacle"] or "")
            check(f"{r['target']} behind-barrier primary carries [O] delivery obstacle",
                  ob.strip().startswith("[O]"))
    # every named route must declare its character honestly (the distributed route must say so)
    nr = m["named_routes"]
    check("hepatic route declares the distributed/dominant-compartment caveat",
          "distributed" in nr["hepatic glucose-disposal"]["character"].lower())
    check("central route declares the [O] deliverability obstacle",
          "[o]" in nr["central appetite-axis"]["character"].lower())
    fwl = m["firewall"].lower()
    check("firewall states routability [F] is distinct from deliverability [O]",
          "routab" in fwl and "deliverab" in fwl)
    return dict(title="Routing-anatomy honesty pass -- cited, SYSTEMIC nodes not oversold, barriers graded [O]",
                overall="PASS" if not failures else "FAIL", failures=failures,
                principle=("anatomy places the compartment [F]; a distributed node is SYSTEMIC (cannot be locally "
                           "routed) and a barrier to the primary compartment is an [O] deliverability obstacle, "
                           "never silently dropped."))


# ---------------------------------------------------------------------------
#  FORBIDDEN-CLAIM SCAN (fail-closed) -- the analgesic scan EXTENDED with a DELIVERY class.
#  Naming a compartment is allowed ([F] cited anatomy); prescribing a route / device / dose is not.
#  obstacle / basis / firewall / grade fields are excluded (checked for presence instead).
# ---------------------------------------------------------------------------
import re
PATTERNS = dict(RL.PATTERNS)  # DOSING / SYNTHESIS / EFFICACY_AS_FACT / SAFETY_AS_FACT
PATTERNS["DELIVERY"] = [r"\binject(s|ed|ing)?\b", r"\bimplant(s|ed|ing)?\b", r"\bcatheter\b",
                        r"\binfus(e|ed|ing|ion)\b", r"\bintrathecal\b", r"\bnanoparticles?\b",
                        r"\bdeliver(y|ed)\s+via\b"]
NEGATION_GUARDED = set(RL.NEGATION_GUARDED) | {"DELIVERY"}
EXCLUDE_KEY_RE_LOCAL = re.compile(r"(firewall|grade|principle|^label$|note$|basis|obstacle|character)", re.I)


def _collect_scanned(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if EXCLUDE_KEY_RE_LOCAL.search(str(k)):   # citation / grade / obstacle field -> not scanned
                continue
            _collect_scanned(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_scanned(v, out)
    elif isinstance(obj, str):
        out.append(obj)


def _negated(text, start):
    return bool(NEG_RE.search(text[:start]))


def forbidden_claim_scan():
    blobs = []
    _collect_scanned(build_routing_map(), blobs)
    text = "  ||  ".join(blobs)
    hits = []
    for cls, pats in PATTERNS.items():
        for pat in pats:
            for m in re.finditer(pat, text, re.I):
                if cls in NEGATION_GUARDED and _negated(text, m.start()):
                    continue
                hits.append({"class": cls, "match": m.group(0)})
    return dict(title="Forbidden-claim firewall scan (dosing / synthesis / efficacy / safety / DELIVERY)",
                overall="PASS" if not hits else "FAIL", hits=hits,
                note="obstacle/basis/firewall/grade/character keys are excluded from the scanned text and checked for presence instead")


# ---------------------------------------------------------------------------
#  FALSIFICATION REGISTER -- a named, measurable falsifier per routing hypothesis.
# ---------------------------------------------------------------------------
FALSIFIERS = {
    "PR1": ("If restricting a lever's action to its single cited compartment (e.g. UCP1->BAT alone) fails to "
            "move the systemic setpoint while only body-wide action does, the PRECISION (single-compartment) "
            "premise for that node is wrong -- the loop effect is not compartment-localised."),
    "PR2": ("If a node classified SYSTEMIC (distributed) turns out, in an independent compartment-restriction "
            "assay, to have its restoration effect dominated by ONE compartment, the distributed classification "
            "(and the 'cannot be locally routed' claim) is wrong."),
    "PR3": ("If a primary compartment graded routable-but-undeliverable [O] (e.g. a CNS target behind the "
            "blood-brain barrier) is in fact reached by a standard systemic route with no barrier penalty, the "
            "[O] deliverability obstacle for that node is wrong."),
    "FRAMEWORK": ("If the routing specificity ordering (the cited compartment count) is uncorrelated with an "
                  "independent tissue-expression-breadth readout for these nodes, the cited-anatomy basis of the "
                  "routing is weakened (the classification would not hold)."),
}


def falsification_register():
    return dict(title="Precision-routing falsification register",
                falsifiers=FALSIFIERS,
                gate="every routing proposal id (PR1-PR3) plus FRAMEWORK has a named, measurable falsifier",
                all_have_falsifier=all(k in FALSIFIERS for k in ("PR1", "PR2", "PR3", "FRAMEWORK")))


def build():
    gi = gamma_independence_gate()
    ah = anatomy_honesty_gate()
    fc = forbidden_claim_scan()
    fr = falsification_register()
    return dict(
        _what="Precision (compartment-restricted) restoration routing -- the analgesic local-anaesthesia "
              "distinction (regional block vs systemic) re-read for the setpoint-restoration levers. "
              "HYPOTHESES only, firewall-bound (gamma never folded into the routing score; proven).",
        routing_map=build_routing_map(),
        gamma_independence=gi,
        anatomy_honesty=ah,
        forbidden_scan=fc,
        falsification=fr,
        all_gates_pass=bool(gi["overall"] == "PASS" and ah["overall"] == "PASS"
                            and fc["overall"] == "PASS" and fr["all_have_falsifier"]))


def emit():
    """Deterministic serialisation of build() for a 2xsha256 self-check (mirrors the engine C1 discipline)."""
    import hashlib
    s = json.dumps(build(), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    b = build()
    print(json.dumps(b["routing_map"]["tier_distribution"], ensure_ascii=False))
    print("gamma-independence:", b["gamma_independence"]["overall"],
          "| routing invariant under gamma perturbation:",
          b["gamma_independence"]["routing_geometry_invariant_under_gamma_perturbation"],
          "| context tracks gamma:", b["gamma_independence"]["carried_context_column_does_track_gamma"])
    print("anatomy honesty:", b["anatomy_honesty"]["overall"],
          "| forbidden-claim scan:", b["forbidden_scan"]["overall"],
          "| falsifiers:", b["falsification"]["all_have_falsifier"])
    print("ALL PRECISION-ROUTING GATES PASS:", b["all_gates_pass"])
    _, h = emit(); print("routing sha256:", h)
