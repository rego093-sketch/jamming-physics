#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restoration_levers.py  --  SETPOINT-RESTORATION via the three-lever technology
(applied from analgesic_threshold_logic_v2_0, Zenodo concept DOI 10.5281/zenodo.20733420).

The analgesic package raises a nociceptor's firing threshold |h_sp| from three directions. The SAME
three-lever frame, re-read for homeostatic setpoint failure (pathology = a defended setpoint that drifted
or crossed to a disease basin, see setpoint_failure.py), gives three directions to RESTORE the setpoint:

  S1  RESTORE the feedback gain / DEEPEN the basin   (analog of analgesic L2 "increase outward current"):
      re-sensitise the loop so the effective stiffness g_eff rises back toward g -- a deeper, more robust
      euglycemic / adiposity basin.                                   nodes: INSR, LEPR, PPARG.   [F] structural
  S2  REDUCE the pathological forcing / lower the drift drive  (analog of analgesic L1 "reduce inward current"):
      lower the chronic forcing h_path that pushes the state toward the disease basin -- by cutting intake
      drive or by raising thermogenic disposal.                       nodes: MC4R, GHRL, UCP1, ADRB3. [F] structural
  S3  REMOVE the upstream sensitising / uncoupling program  (analog of analgesic L3 "remove sensitising drive"):
      remove the chronic program that LOWERED the crossing threshold -- the uncoupled fuel-sparing of the
      hibernation bridge (PDK4) and the chronic inflammatory sensitiser.  nodes: PDK4, TNF-axis.  [O] cited

THE ENGINE READS, on one scale, the promoter switch-threshold STRUCTURE (gamma -> R19 |h_sp|, barrier) of the
genes behind all three levers. For every node the map carries: lever, push direction, measured gamma, R19
|h_sp| / barrier, the CITED Layer-2 biology + source, and the [V]/[F]/[O] grades.

FIREWALL (binding -- identical discipline to the analgesic package):
  - gamma / spinodal |h_sp| / barrier are the engine's READ of the locus' promoter switch-threshold STRUCTURE.
    They are [V] (reproducible); their ORDER is [F] (forced).
  - This is NOT a glucose level, NOT an HbA1c, NOT an insulin dose, NOT a clinical effect. Any such mapping is
    Layer-2 and [O] -- never asserted here.
  - lever + push direction are [F] structural, anchored to the CITED clinical axes.
  - S3 (the uncoupling/inflammatory program) mechanism link is [O]: the gamma read places the gene in the
    lever map but does NOT derive the receptor/network mechanism (enforced by the S3 honesty gate).
  - These are falsifiable HYPOTHESES grounded in the foundational setpoint mechanism, NOT medical advice; no
    dosing, no efficacy, no safety claim, no clinical responsibility.

No tuning: spinodal/barrier are the locked R19 forms; gamma is measured (inherited atlas).
"""
import os, sys, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier

_HERE = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

def _gamma_atlas():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

# ---------------------------------------------------------------------------
#  CITED Layer-2 context (NOT engine output) -- source-tagged. lever in {S1,S2,S3}.
#  push = the restoration direction; src = the cited clinical/biological axis.
# ---------------------------------------------------------------------------
S1 = "[F] structural: re-sensitise the loop -> g_eff rises -> deeper, more robust basin (anchored to cited axes)"
S2 = "[F] structural: lower the chronic forcing h_path (cut intake drive / raise thermogenic disposal)"
S3 = "[O] cited biology: gamma places the gene in the lever map; the uncoupling/inflammatory mechanism is NOT derived"

CONTEXT = {
    # --- S1 : restore feedback gain / deepen the basin -------------------------------
    "INSR":  dict(lever="S1", push="restore insulin-signalling gain (insulin sensitisation) -> deepen the euglycemic basin",
                  axis="insulin sensitivity (glucose disposal loop)", grade_mechanism=S1,
                  src="cited: insulin-resistance / sensitisation axis (clinical glucose-loop literature)"),
    "LEPR":  dict(lever="S1", push="restore leptin feedback gain (re-sensitise the lipostat) -> deepen the adiposity basin",
                  axis="leptin feedback (adiposity -> brain)", grade_mechanism=S1,
                  src="cited: leptin-resistance / lipostat feedback axis"),
    "PPARG": dict(lever="S1", push="restore adipocyte insulin sensitivity (storage-node disposal) -> deepen disposal basin",
                  axis="adipocyte insulin sensitivity (storage node)", grade_mechanism=S1,
                  src="cited: PPAR-gamma insulin-sensitising axis"),
    # --- S2 : reduce the pathological forcing / lower the drift drive ----------------
    "MC4R":  dict(lever="S2", push="raise melanocortin tone -> reduce intake forcing -> lower the drift drive",
                  axis="melanocortin appetite setpoint (intake control)", grade_mechanism=S2,
                  src="cited: melanocortin-4 energy-balance axis"),
    "GHRL":  dict(lever="S2", push="reduce hunger signalling (ghrelin axis) -> lower the intake forcing",
                  axis="ghrelin hunger drive (opposes leptin)", grade_mechanism=S2,
                  src="cited: ghrelin hunger axis"),
    "UCP1":  dict(lever="S2", push="recruit thermogenic disposal -> raise expenditure -> lower the NET energy-surplus forcing",
                  axis="brown-fat thermogenic disposal", grade_mechanism=S2,
                  src="cited: UCP1 brown-fat energy-expenditure axis"),
    "ADRB3": dict(lever="S2", push="sympathetic recruitment of thermogenesis -> raise disposal -> lower net forcing",
                  axis="beta3 sympathetic thermogenic command", grade_mechanism=S2,
                  src="cited: beta3-adrenergic thermogenesis axis"),
    # --- S3 : remove the upstream sensitising / uncoupling program (cited [O]) -------
    "PDK4":  dict(lever="S3", push="remove the chronic uncoupled fuel-sparing program (the hibernation-bridge misfire, RD4)",
                  axis="PDK4 fuel-sparing program (torpor<->insulin-resistance bridge)", grade_mechanism=S3,
                  src="cited: PDK4 co-upregulation in torpor and insulin resistance (RD4 bridge biology)"),
    "TNF":   dict(lever="S3", push="remove the chronic low-grade inflammatory sensitiser that lowers the crossing threshold",
                  axis="chronic low-grade inflammation (upstream sensitiser)", grade_mechanism=S3,
                  src="cited: chronic inflammation / insulin-resistance sensitisation axis (gamma not in this atlas)"),
}

# CITED priority tiers per target (B=burden, U=unmet-need, D=mechanistic-directness, 1..5) + one-line basis.
# The weights below are DECLARED, not tuned to a desired answer (mirrors analgesic M10).
WEIGHTS = {"B": 0.40, "U": 0.35, "D": 0.25}
TIERS = {
    "INSR":  dict(B=5, U=4, D=5, basis="cited: T2D burden very high; sensitisation directly addresses the glucose-loop gain"),
    "LEPR":  dict(B=4, U=4, D=3, basis="cited: obesity burden high; leptin re-sensitisation is harder (central resistance)"),
    "PPARG": dict(B=4, U=3, D=4, basis="cited: insulin-sensitising storage node; established axis"),
    "MC4R":  dict(B=4, U=4, D=4, basis="cited: appetite-forcing reduction; strong energy-balance node"),
    "GHRL":  dict(B=3, U=3, D=3, basis="cited: hunger-axis modulation; moderate directness"),
    "UCP1":  dict(B=4, U=4, D=3, basis="cited: expenditure side of energy balance; recruitment is the open challenge"),
    "ADRB3": dict(B=3, U=3, D=3, basis="cited: sympathetic command; effector-level, indirect on setpoint"),
    "PDK4":  dict(B=4, U=4, D=2, basis="cited: bridge program; S3 mechanism is cited [O], directness deliberately low"),
    "TNF":   dict(B=3, U=3, D=2, basis="cited: upstream sensitiser; broad, non-specific, low directness"),
}

def _node_read(sym, atlas):
    g = atlas.get(sym, {}).get("gamma")
    if g is None:
        return dict(gamma=None, h_sp=None, barrier=None)
    return dict(gamma=round(float(g), 6), h_sp=round(float(spinodal(g)), 6), barrier=round(float(barrier(g)), 6))

def build_lever_map():
    atlas = _gamma_atlas(); rows = []
    for sym, ctx in CONTEXT.items():
        rd = _node_read(sym, atlas)
        rows.append(dict(target=sym, lever=ctx["lever"], push_direction=ctx["push"], axis=ctx["axis"],
                         gamma=rd["gamma"], h_sp=rd["h_sp"], barrier=rd["barrier"],
                         grade_read="[V] reproducible promoter switch-threshold read; ORDER [F]",
                         grade_mechanism=ctx["grade_mechanism"], src=ctx["src"]))
    # order by |h_sp| descending where present (structural context only -- NOT a clinical ranking)
    rows.sort(key=lambda r: (-1 if r["h_sp"] is None else r["h_sp"]), reverse=True)
    return dict(
        title="Setpoint-restoration three-lever map (S1 restore-gain / S2 reduce-forcing / S3 remove-sensitiser)",
        levers={"S1": "restore feedback gain / deepen the basin",
                "S2": "reduce the pathological forcing / lower the drift drive",
                "S3": "remove the upstream sensitising / uncoupling program (cited [O])"},
        rows=rows,
        firewall=("gamma reads the promoter switch-threshold STRUCTURE only (an R19 |h_sp|); it is NOT a glucose "
                  "level, NOT an HbA1c, NOT an insulin dose, NOT a clinical effect. lever + push are [F] structural; "
                  "the S3 uncoupling/inflammatory mechanism link is [O] cited biology, never derived. These are "
                  "falsifiable HYPOTHESES grounded in the foundational setpoint mechanism, not medical advice."))

def build_prioritisation():
    rows = []
    for sym, t in TIERS.items():
        score = WEIGHTS["B"] * t["B"] + WEIGHTS["U"] * t["U"] + WEIGHTS["D"] * t["D"]
        rd = _node_read(sym, _gamma_atlas())
        rows.append(dict(target=sym, lever=CONTEXT[sym]["lever"], B=t["B"], U=t["U"], D=t["D"],
                         score=round(float(score), 4), basis=t["basis"],
                         gamma_h_sp_context=rd["h_sp"]))   # carried ALONGSIDE, never folded into score
    rows.sort(key=lambda r: (-r["score"], r["target"]))
    return dict(title="Restoration-target prioritisation (rank TARGETS, not drugs)",
                weights=WEIGHTS, weights_note="DECLARED editorial weights, not tuned to a desired answer",
                ranking=rows,
                firewall=("score = w_B*B + w_U*U + w_D*D over CITED 1..5 tiers; the gamma-|h_sp| read is carried as "
                          "structural context and is NEVER folded into the clinical priority score (a promoter-stiffness "
                          "read is not a clinical magnitude). Ranking is [F] from cited tiers + declared weights."))

# ---------------------------------------------------------------------------
#  S3 HONESTY GATE (fail-closed)  -- mirrors analgesic M11.
# ---------------------------------------------------------------------------
S3_DECLARED = {"PDK4", "TNF"}

def s3_honesty_gate():
    m = build_lever_map(); failures = []
    def check(name, cond):
        if not cond: failures.append(name)
        return cond
    s3_rows = [r for r in m["rows"] if r["lever"] == "S3"]
    for r in s3_rows:
        gm = r.get("grade_mechanism", "").strip()
        is_open = gm.startswith("[O]")
        not_derived = not (gm.startswith("[V]") or gm.startswith("[F]"))
        cited = bool(r.get("src", "").strip())
        check(f"S3 target {r['target']} graded [O] cited (open={is_open} not_derived={not_derived} cited={cited})",
              is_open and not_derived and cited)
    check("declared S3 set present", S3_DECLARED.issubset({r["target"] for r in s3_rows}))
    fw = m.get("firewall", "").lower()
    check("map firewall states the S3 mechanism link is [O]", "[o]" in fw and "s3" in fw)
    return dict(title="S3 honesty pass -- uncoupling/inflammatory mechanism link graded [O], never derived",
                overall="PASS" if not failures else "FAIL", failures=failures,
                principle=("the gamma read places an S3 gene in the lever map but the uncoupling/network mechanism is "
                           "NOT captured by the read and is graded cited-biology [O]."))

# ---------------------------------------------------------------------------
#  FALSIFICATION REGISTER  -- mirrors analgesic M6 (a named falsifier per proposal).
# ---------------------------------------------------------------------------
FALSIFIERS = {
    "SP1": ("If restoring feedback gain (re-sensitisation) in a loop that has ALREADY crossed to the disease basin "
            "fails to return the state, while only reducing the chronic forcing does, the S1 'deepen-the-basin-alone "
            "restores' premise is wrong (gain restoration is insufficient once crossed)."),
    "SP2": ("If lowering the chronic forcing abolishes the defended setpoint entirely (the loop holds NO setpoint "
            "without the forcing -- no bounded return to a healthy value), the S2 'controlled return to a healthy "
            "setpoint' premise fails."),
    "SP3": ("If removing the upstream uncoupling/inflammatory program does NOT raise the crossing threshold (spinodal) "
            "of the disease basin in an independent loop-gain assay, the S3 'remove-the-sensitiser' premise is wrong."),
    "FRAMEWORK": ("If the gamma-derived |h_sp| ordering of the setpoint-node set is uncorrelated with ANY independent "
                  "promoter-switch readout, the read's organising relevance to these loci is weakened (the read remains "
                  "[V] as a number, but its claim to order the nodes would not hold)."),
}

def falsification_register():
    return dict(title="Restoration falsification register",
                falsifiers=FALSIFIERS,
                gate="every proposal id (SP1-SP3) plus FRAMEWORK has a named, measurable falsifier",
                all_have_falsifier=all(k in FALSIFIERS for k in ("SP1", "SP2", "SP3", "FRAMEWORK")))

# ---------------------------------------------------------------------------
#  FORBIDDEN-CLAIM SCAN (fail-closed)  -- mirrors analgesic M5. The lever map /
#  prioritisation assertion text must carry NO dosing / synthesis / efficacy /
#  safety claim. firewall / grade keys are excluded (checked for presence instead).
# ---------------------------------------------------------------------------
PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b", r"\btablets?\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b", r"\bguaranteed\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS"}
NEG_RE = re.compile(r"(no|not|never|without)\s+(a\s+|an\s+|any\s+)?$", re.I)
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|^label$|note$|basis)", re.I)

def _collect_assertion_strings(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if EXCLUDE_KEY_RE.search(str(k)):  # firewall/grade/basis field -> not scanned
                continue
            _collect_assertion_strings(v, out)
    elif isinstance(obj, list):
        for v in obj: _collect_assertion_strings(v, out)
    elif isinstance(obj, str):
        out.append(obj)

def _negated(text, start):
    return bool(NEG_RE.search(text[:start]))

def forbidden_claim_scan():
    blobs = []
    _collect_assertion_strings(build_lever_map(), blobs)
    _collect_assertion_strings(build_prioritisation(), blobs)
    text = "  ||  ".join(blobs)
    hits = []
    for cls, pats in PATTERNS.items():
        for pat in pats:
            for m in re.finditer(pat, text, re.I):
                if cls in NEGATION_GUARDED and _negated(text, m.start()):
                    continue
                hits.append({"class": cls, "match": m.group(0)})
    return dict(title="Forbidden-claim firewall scan (dosing/synthesis/efficacy/safety)",
                overall="PASS" if not hits else "FAIL", hits=hits,
                note="firewall/grade/basis keys are excluded from the scanned text and checked for presence instead")

def build():
    return dict(
        _what="Setpoint-restoration via the analgesic three-lever technology, grounded in the foundational "
              "setpoint mechanism. HYPOTHESES only -- no medical advice (firewall).",
        lever_map=build_lever_map(),
        prioritisation=build_prioritisation(),
        s3_honesty=s3_honesty_gate(),
        falsification=falsification_register(),
        forbidden_scan=forbidden_claim_scan(),
        all_gates_pass=bool(s3_honesty_gate()["overall"] == "PASS"
                            and falsification_register()["all_have_falsifier"]
                            and forbidden_claim_scan()["overall"] == "PASS"))

if __name__ == "__main__":
    b = build()
    print(json.dumps(b, ensure_ascii=False, indent=2)[:1500])
    print("\nALL RESTORATION GATES PASS:", b["all_gates_pass"])
