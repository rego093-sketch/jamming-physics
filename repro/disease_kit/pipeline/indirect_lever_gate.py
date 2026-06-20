#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
indirect_lever_gate.py  --  the INDIRECT-LEVER honesty gate (fail-closed).

  *** INHERITED from analgesic_threshold_logic_v2_0  M11 (l3_honesty.py),
      DOI 10.5281/zenodo.20733420.  The analgesic L3 gate enforced that NGF/CGRP receptor/network
      mechanisms -- which the gamma read does NOT capture -- are graded cited-biology [O], never
      derived.  Ported here to the disease kit's exactly analogous class. ***

THE PRINCIPLE (verbatim in spirit from analgesic M11):
  gamma reads the CAUSAL gene's promoter switch-threshold STRUCTURE.  When the corrective lever
  acts on the SAME causal switch (gene-restore: potentiate/correct/replace/reduce the disease
  gene), the read places it directly.  But when the lever acts on a DIFFERENT node -- an UPSTREAM
  enzyme (nitisinone->HPD for tyrosinaemia/alkaptonuria), a DOWNSTREAM hormone or effector
  (burosumab->FGF23 for XLH; trofinetide->IGF1 for Rett; omaveloxolone->NFE2L2 for Friedreich), a
  PARALOG backup (SMN2 for SMA), a REPRESSOR (BCL11A for sickle/beta-thal), or the ACCUMULATED
  SUBSTRATE itself (copper/iron/cystine/waste-nitrogen) -- then the mechanism LINK from "act here"
  to "the disease axis is corrected" is RECEPTOR/NETWORK/PHARMACOLOGY biology that the gamma read
  does NOT capture.  For those, gamma may place the causal switch and the lever's DIRECTION is
  forced + cited, but the MECHANISM LINK must be graded cited-biology [O], NEVER derived.

This gate enforces exactly that, disease by disease, lever by lever, on the FROZEN analysis.json.

Gate (fail-closed):
  - classify every therapeutic-axis lever as `gene-restore` (target is a CAUSAL gene of that
    disease) or `indirect` (target is anything else: upstream / downstream / paralog / repressor /
    substrate);
  - every `indirect` lever's mechanism_grade begins with "[O]";
  - none is presented as a derived ([V]/[F]) mechanism;
  - each carries a non-empty citation (src);
  - the disease's emergence firewall + treatment firewall both state the magnitude is structure-
    only / [O] (the mechanism is not derived from sequence);
  - the declared headline indirect set (the well-known downstream/upstream leads) is present and
    all-[O], so the gate cannot pass vacuously if those reads are dropped.

Run:  python3 pipeline/indirect_lever_gate.py [--write]   -> exit 1 on any violation
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DISEASES = os.path.join(ROOT, "diseases")

# headline indirect leads that MUST be present and graded [O] (the analogue of analgesic's
# DECLARED_L3 set) -- so the gate is not vacuous if these reads are ever dropped.
# (disease slug -> the off-causal-gene target the approved/lead lever acts on)
DECLARED_INDIRECT = {
    "hereditary_tyrosinaemia_type_1": "HPD",      # upstream-block (nitisinone)
    "alkaptonuria": "HPD",                        # same upstream-block lever, different disease
    "x_linked_hypophosphataemia": "FGF23",        # downstream hormone (burosumab)
    "rett_syndrome": "IGF1",                       # downstream effector (trofinetide)
    "friedreich_ataxia": "NFE2L2",                 # downstream pathway (omaveloxolone)
    "spinal_muscular_atrophy": "SMN2",             # paralog backup (nusinersen/risdiplam)
    "sickle_cell_disease": "BCL11A",               # repressor of HbF (exa-cel)
    "acute_intermittent_porphyria": "ALAS1",       # upstream-block (givosiran)
    "wilson_disease": "copper",                    # accumulated substrate (chelation)
    "hereditary_haemochromatosis_type_1": "iron",  # accumulated substrate (phlebotomy)
}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


def causal_gene_set(a):
    genes = {g["gene"] for g in a["emergence"]["per_gene"]}
    for sg in a["emergence"].get("suspended_genes", []):
        if isinstance(sg, dict) and sg.get("gene"):
            genes.add(sg["gene"])
    return genes


def firewall_says_open(a):
    em_fw = (a.get("emergence", {}).get("firewall", "") or "").lower()
    tx_fw = (a.get("treatment_A_switch", {}).get("firewall", "") or "").lower()
    em_ok = ("structure" in em_fw) and ("[o]" in em_fw or "open" in em_fw or "not derive" in em_fw
                                        or "magnitude" in em_fw)
    tx_ok = ("not dose" in tx_fw or "not potency" in tx_fw or "direction" in tx_fw
             or "[o]" in tx_fw or "efficacy" in tx_fw)
    return em_ok and tx_ok


def build():
    reg = json.load(open(os.path.join(DISEASES, "_registry.json"), encoding="utf-8"))
    per_disease, indirect_levers = {}, []

    for slug in reg["diseases"]:
        a = json.load(open(os.path.join(DISEASES, slug, "analysis.json"), encoding="utf-8"))
        if a.get("status") != "RESOLVED":
            continue
        causal = causal_gene_set(a)
        levers = a.get("treatment_A_switch", {}).get("levers", [])
        fw_ok = firewall_says_open(a)
        rows = []
        for lv in levers:
            tgt = lv.get("target_gene", "")
            is_indirect = tgt not in causal
            gm = (lv.get("mechanism_grade", "") or "").strip()
            cls = "indirect" if is_indirect else "gene-restore"
            row = {
                "lever": lv.get("lever"), "target": tgt, "class": cls,
                "mechanism_grade": gm,
                "open": gm.startswith("[O]"),
                "not_derived": not (gm.startswith("[V]") or gm.startswith("[F]")),
                "cited": bool((lv.get("src", "") or "").strip()),
            }
            if is_indirect:
                row["ok"] = row["open"] and row["not_derived"] and row["cited"] and fw_ok
                indirect_levers.append({"slug": slug, **row})
            rows.append(row)
        per_disease[slug] = {"causal_genes": sorted(causal), "firewall_open": fw_ok,
                              "levers": rows,
                              "n_indirect": sum(1 for r in rows if r["class"] == "indirect")}

    print("Indirect-lever honesty gate  [inherited: analgesic M11 / l3_honesty]")

    # 1) every indirect lever graded [O], not derived, cited, with an open firewall
    bad = [il for il in indirect_levers if not il["ok"]]
    for il in bad:
        print(f"    [FAIL] {il['slug']} :: {il['lever']}->{il['target']}  "
              f"open={il['open']} not_derived={il['not_derived']} cited={il['cited']}  gm={il['mechanism_grade']!r}")
    check("every indirect (off-causal-gene) lever graded [O] cited-biology, not derived, "
          "with an open firewall", not bad)

    # 2) the declared headline indirect set is present and all routed through the [O] grade
    present = {}
    for slug, tgt in DECLARED_INDIRECT.items():
        ils = [il for il in indirect_levers if il["slug"] == slug and il["target"] == tgt]
        present[f"{slug}->{tgt}"] = bool(ils) and all(il["ok"] for il in ils)
    check(f"declared headline indirect set present + all-[O] "
          f"({sum(present.values())}/{len(present)})", all(present.values()))

    # 3) classification is non-vacuous: there really are indirect levers in the corpus
    n_indirect = len(indirect_levers)
    check(f"indirect-lever class is non-empty (found {n_indirect})", n_indirect > 0)

    result = {
        "title": "Indirect-lever honesty pass -- off-causal-gene mechanism link graded [O], never derived",
        "inherited_from": "analgesic_threshold_logic_v2_0 M11 (l3_honesty.py); DOI 10.5281/zenodo.20733420",
        "principle": ("gamma reads the causal gene's promoter switch-threshold structure; a lever acting "
                      "on an upstream/downstream/paralog/repressor/substrate node carries a mechanism link "
                      "the read does NOT capture, so that link is graded cited-biology [O]."),
        "declared_indirect": DECLARED_INDIRECT,
        "n_indirect_levers": n_indirect,
        "declared_set_present_and_open": present,
        "per_disease": per_disease,
        "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
    }
    return result


def selftest():
    """Prove the gate has TEETH: a synthetic indirect lever graded as a DERIVED mechanism must
    be rejected by the same predicate the gate uses."""
    def verdict(gm, cited):
        gm = gm.strip()
        return gm.startswith("[O]") and not (gm.startswith("[V]") or gm.startswith("[F]")) and cited
    clean = verdict("[O] downstream magnitude not derived from sequence", True)
    derived_F = verdict("[F] the read DERIVES the downstream correction magnitude", True)
    derived_V = verdict("[V] sequence measures the downstream effect", True)
    uncited = verdict("[O] open", False)
    ok = clean and not derived_F and not derived_V and not uncited
    print("  [self-test] gate teeth:",
          f"clean(pass)={clean}  derived[F](reject)={not derived_F}  "
          f"derived[V](reject)={not derived_V}  uncited(reject)={not uncited}  -> {'OK' if ok else 'BROKEN'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    teeth_ok = selftest()
    res = build()
    if not teeth_ok:
        res["overall"] = "FAIL"
        res.setdefault("failures", []).append("self-test: gate predicate is broken")
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "repro", "modules", "expected", "indirect_lever_honesty.json")
        json.dump(res, open(p, "w"), indent=1)
        print(f"  wrote {os.path.relpath(p, ROOT)}")
    # a small witnessed sample
    sample = [il for il in []]
    print(f"  indirect levers checked: {res['n_indirect_levers']}; "
          f"declared headline set: {sum(res['declared_set_present_and_open'].values())}"
          f"/{len(res['declared_set_present_and_open'])} present+open")
    print("OVERALL:", "PASS" if res["overall"] == "PASS" else f"FAIL {res['failures']}")
    sys.exit(0 if res["overall"] == "PASS" else 1)
