#!/usr/bin/env python3
"""
R2 stage 2 — boundary review (SCOPE.md primary-system rule, applied to data).

R1's scope filter was NAME-BASED. Now that every in-scope entity carries a
MedGen clinical definition (real organ-involvement text), re-examine the
boundary classes the R1 handover flagged: lysosomal / storage / leukodystrophy
and neurocutaneous. Decide IN vs OUT by the *primary/defining* system, reading
the actual definition.

Discipline (SCOPE.md + constitution C-D6):
  * Classify by the PRIMARY system. Storage diseases are a systemic family;
    they stay IN and the CNS axis is CROSS-REFERENCED (not duplicated), UNLESS
    the entity is essentially a pure-CNS neurodegenerative disorder with no
    systemic organ disease — then it belongs to the sibling (OUT).
  * "Name it, don't hide it": every excluded entity is logged with the reason
    and the cited evidence; nothing is silently dropped.
  * Conservative: auto-move OUT only on a DOUBLE gate (strong CNS signal AND a
    recognized neurodegenerative-storage name AND no systemic-organ signal).
    Everything else is recorded for author review but left IN with a cross-ref
    flag where CNS is co-involved.

INVESTIGATION ONLY. Deterministic: pure function of disease_index.csv (no network).

Inputs : data/curated/disease_index.csv  (from r2_enrich_inscope.py)
Outputs: data/curated/disease_index.csv  (rewritten: in_scope updated for moves,
                                           + cns_cross_reference column)
         reports/r2_boundary_review.csv   (full audit of every candidate)
"""
import csv, os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX  = os.path.join(ROOT, "data", "curated", "disease_index.csv")
REV  = os.path.join(ROOT, "reports", "r2_boundary_review.csv")

# Candidate gate: storage/lysosomal family by name or hint.
STORAGE_NAME = re.compile(
    r"lysosom|gangliosid|sphingolip|mucopolysacchar|mucolipid|leukodystroph|"
    r"sulfatase|cerebrosid|sandhoff|tay-sachs|\bgm1\b|\bgm2\b|niemann|"
    r"metachromat|batten|ceroid|krabbe|fucosidos|mannosidos|"
    r"aspartylglucosamin|salla|sialidos|schindler|farber", re.I)

# Recognized PRIMARY-neurodegenerative-storage names (the OUT short-list gate).
NEURO_STORAGE = re.compile(
    r"tay-sachs|sandhoff|\bgm2\b|metachromat|krabbe|canavan|"
    r"neuronal ceroid|batten|\bgm1 gangliosidosis type 2\b|"
    r"infantile gm1|sialidos|multiple sulfatase|mucolipidosis type iv|"
    r"\bgm1 gangliosidosis type 3\b", re.I)

# Neurocutaneous (keep IN, cross-reference CNS per handover).
NEUROCUT = re.compile(r"tuberous sclerosis|neurofibromatos|\bnf1\b|\bnf2\b|"
                      r"sturge-weber|von hippel-lindau|incontinentia pigmenti", re.I)

# --- CNS-primacy signals (negation-aware) ---
CNS_SIGNALS = [
    ("primary_cns_disease", r"primary central nervous system disease"),
    ("neurodegeneration",   r"neurodegener"),
    ("psychomotor_regression", r"psychomotor (regression|deterioration)"),
    ("dev_regression",      r"developmental regression|loss of (developmental|motor|acquired) (milestones|skills)|regression of"),
    ("progressive_neuro",   r"progressive neurolog|relentless neurolog|neurologic deterioration"),
    ("leukodystrophy",      r"leukodystroph|white matter"),
    ("cherry_red_spot",     r"cherry-red spot"),
    ("dementia",            r"\bdementia\b"),
    ("intellectual_primary",r"intellectual disability|cognitive (decline|impairment)"),
    ("seizures",            r"\bseizure|epilep"),
]
CNS_NEG = re.compile(
    r"absence of primary central nervous system|no central nervous system manifest|"
    r"without (primary )?central nervous system|absence of .{0,25}neurolog|"
    r"no (primary )?neurolog", re.I)

# --- systemic-organ signals ---
SYS_SIGNALS = [
    ("hepatosplenomegaly", r"hepatospleno|splenomegaly|hepatomegaly"),
    ("skeletal",           r"skeletal|\bbone\b|dysostos|\brickets\b|short stature|coarse fac"),
    ("visceral",           r"\bvisceral\b"),
    ("cardiac_organ",      r"cardiomyopath|cardiac valv|valv(e|ular)|aortic"),
    ("corneal",            r"cornea"),
    ("renal",              r"\brenal\b|\bkidney|nephro|fanconi"),
    ("pulmonary",          r"pulmonar|\blung|respiratory (infection|failure|insufficien)"),
    ("hematologic",        r"anemi|thrombocyto|pancytopen|bone marrow"),
    ("hepatic",            r"\bliver\b|hepatic|cirrhos"),
    ("growth_feeding",     r"growth failure|failure to (gain|thrive)|feeding difficult"),
    ("joint_connective",   r"\bjoint|contractur"),
]

def count_signals(text, signals, neg=None):
    hits = []
    low = text or ""
    for name, pat in signals:
        if re.search(pat, low, re.I):
            hits.append(name)
    if neg and hits and neg.search(low):
        # demote: a global negation of CNS removes the soft CNS signals but we
        # keep an explicit primary_cns_disease only if not itself negated.
        pass
    return hits

def main():
    rows = list(csv.DictReader(open(IDX, encoding="utf-8")))
    review = []
    moved = 0
    crossref = 0

    for r in rows:
        if r["in_scope"] != "true":
            r["cns_cross_reference"] = "false"
            continue
        name = r["entity"]; defn = r["clinical_definition"]; hint = r["organ_system_hint"]
        is_storage = ("lysosomal" in hint) or bool(STORAGE_NAME.search(name))
        is_neurocut = bool(NEUROCUT.search(name))
        if not (is_storage or is_neurocut):
            r["cns_cross_reference"] = "false"
            continue

        cns_hits = count_signals(defn, CNS_SIGNALS)
        # honor explicit negation of CNS for the storage spectrum
        negated = bool(CNS_NEG.search(defn or ""))
        sys_hits = count_signals(defn, SYS_SIGNALS)
        cns_score = len(cns_hits)
        sys_score = len(sys_hits)

        # decision
        decision = "keep_in"
        reason = ""
        cross = "false"
        if is_neurocut:
            decision = "keep_in_crossref_cns"
            reason = "neurocutaneous multi-system: primary systemic features kept; CNS cross-referenced (handover)"
            cross = "true"
        else:
            neuro_name = bool(NEURO_STORAGE.search(name))
            pure_cns = (cns_score >= 2) and (sys_score == 0) and (not negated)
            if neuro_name and pure_cns:
                decision = "move_out"
                reason = ("primary CNS neurodegenerative storage confirmed from MedGen definition "
                          f"(CNS signals: {','.join(cns_hits)}; no systemic-organ signal)")
            elif cns_score >= 1 and not negated:
                decision = "keep_in_crossref_cns"
                reason = (f"systemic storage with CNS involvement (systemic: {','.join(sys_hits) or 'name-class'}; "
                          f"CNS: {','.join(cns_hits)}) -> keep IN, cross-reference CNS axis")
                cross = "true"
            else:
                decision = "keep_in"
                reason = "systemic storage; no primary-CNS signal in definition"

        r["cns_cross_reference"] = cross
        if decision == "move_out":
            r["in_scope"] = "false"
            r["exclusion_reason"] = f"R2 boundary review: {reason}"
            moved += 1
        elif cross == "true":
            crossref += 1

        review.append({
            "entity": name, "medgen_cui": r["medgen_cui"], "organ_system_hint": hint,
            "candidate_class": "neurocutaneous" if is_neurocut else "storage",
            "cns_score": cns_score, "cns_signals": ";".join(cns_hits),
            "cns_negated": "true" if negated else "false",
            "sys_score": sys_score, "sys_signals": ";".join(sys_hits),
            "decision": decision, "reason": reason,
            "evidence_source": f"medgen:esummary:definition:2026-06-17",
        })

    # rewrite index with the new column, preserving order/columns
    cols = list(rows[0].keys())
    if "cns_cross_reference" not in cols:
        cols.append("cns_cross_reference")
    for r in rows:
        r.setdefault("cns_cross_reference", "false")
    with open(IDX, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

    review.sort(key=lambda x: (x["decision"] != "move_out", x["entity"].lower()))
    rcols = ["entity", "medgen_cui", "organ_system_hint", "candidate_class",
             "cns_score", "cns_signals", "cns_negated", "sys_score", "sys_signals",
             "decision", "reason", "evidence_source"]
    os.makedirs(os.path.dirname(REV), exist_ok=True)
    with open(REV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=rcols); w.writeheader(); w.writerows(review)

    n_in = sum(1 for r in rows if r["in_scope"] == "true")
    digest = hashlib.sha256(open(IDX, "rb").read()).hexdigest()[:12]
    print("--- R2 boundary review ---")
    print(f"  candidates reviewed       : {len(review)}")
    print(f"  MOVED OUT (primary CNS)    : {moved}")
    print(f"  kept IN + CNS cross-ref    : {crossref}")
    print(f"  in-scope after review      : {n_in}")
    print(f"  review log: {REV}")
    print(f"  index sha256[:12]: {digest}")
    print()
    print("  moved-out entities:")
    for x in review:
        if x["decision"] == "move_out":
            print(f"    - {x['entity'][:55]:55s} [{x['cns_signals']}]")

if __name__ == "__main__":
    main()
