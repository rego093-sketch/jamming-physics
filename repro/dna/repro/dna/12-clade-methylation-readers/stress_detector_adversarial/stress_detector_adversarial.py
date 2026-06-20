#!/usr/bin/env python3
"""
STRESS TEST C (T2.3) -- methylation auto-detector, adversarial / out-of-panel.

Question: does detect_regime() (the 4-regime methylation auto-detector frozen in
clade_reader_engine.py) generalize to organisms OUTSIDE the 12-organism panel it
was tuned on, or does it misclassify boundary cases?

Method:
  PART 1 (empirical generalization).  Feed the detector 7 out-of-panel organisms
  with well-established methylation biology (120kb RefSeq regions, frozen). Three
  groups:
    - within-class generalization (should classify correctly):
        tomato  -> PLANT      (plant CG+CHG+CHH / RdDM)
        cow,dog -> VERTEBRATE  (mammal global CG)
    - out-of-category (no detector class exists):
        neurospora -> fungal RIP/targeted 5mC
        oyster     -> mollusk gene-body CpG (mosaic, no global)
    - composition stress / false-positive probe (no 5mC at all, 6mA only, AT-rich):
        dictyostelium, tetrahymena -> ~22% GC, no 5mC

  PART 2 (mechanistic null -- WHY any AT-rich misclassification happens).
  For the AT-rich organisms + panel Plasmodium, build two nulls at MATCHED
  composition and re-run the detector:
    - iid-random null: i.i.d. bases at matched mononucleotide marginals. By
      construction E[context O/E]=1.0, so any methylation-category call here is a
      pure estimator/threshold artifact at extreme GC.
    - mono-shuffle null: exact base composition preserved, all di/tri structure
      destroyed. Tests whether the observed depletion is real sequence structure.

  Also re-emits the 12-organism PANEL classification for context (the latent
  Plasmodium finding).

Null hypothesis (detector generalizes): thresholds (T_VERT_CG, T_PLANT_CHG, ...)
separate methylation regimes by biology, not by base composition. Then (a) every
out-of-panel organism lands in its biologically correct class or honest [O], and
(b) iid-random nulls at any GC return 'no_global'.

Grading: CORRECT / MISCLASSIFIED / [O] (no class exists -> closing reason given).
No threshold is changed (that would be a new version). Deterministic, seed=19,
single-source engine import + sha256 pin.
"""
import sys, os, json, hashlib, random

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.abspath(os.path.join(HERE, ".."))      # 12-clade-methylation-readers/
PANEL_DIR  = os.path.abspath(os.path.join(HERE, "..", "..", "11-cross-kingdom-stress-test", "inputs"))

# --- single-source import of the LOCKED engine + sha256 pin (drift detection) ---
ENGINE_PATH = os.path.join(ENGINE_DIR, "clade_reader_engine.py")
ENGINE_SHA  = "61f32837ec56578ecaf87cba7a8b39edf3a0aee4793709b80440e543123da481"
_got = hashlib.sha256(open(ENGINE_PATH, "rb").read()).hexdigest()
assert _got == ENGINE_SHA, f"ENGINE DRIFT: {_got} != {ENGINE_SHA}"
sys.path.insert(0, ENGINE_DIR)
import clade_reader_engine as M   # bulk_contexts, detect_regime, gc, cpg_oe, context_oe

SEED = 19
K_NULL = 40   # null replicates per organism


def read_seq(path):
    return "".join(l.strip() for l in open(path) if not l.startswith(">")).upper()


def classify(seq):
    """Bulk-path classification (no annotations -> per-gene args left None)."""
    cg, chg, chh = M.bulk_contexts(seq)
    reg = M.detect_regime(cg, chg)
    return {"cg_oe": round(cg, 4), "chg_oe": round(chg, 4),
            "chh_oe": round(chh, 4), "gc_pct": round(M.gc(seq) * 100, 2),
            "regime": reg}


def iid_random(seq, rng):
    """i.i.d. bases at matched mononucleotide marginals. E[O/E]=1.0 by construction."""
    bases = [b for b in seq if b in "ACGT"]
    n = len(bases)
    from collections import Counter
    c = Counter(bases)
    pool = "ACGT"
    weights = [c[b] for b in pool]
    return "".join(rng.choices(pool, weights=weights, k=n))


def mono_shuffle(seq, rng):
    """Exact base composition preserved, all di/tri-nucleotide structure destroyed."""
    bases = [b for b in seq if b in "ACGT"]
    rng.shuffle(bases)
    return "".join(bases)


def null_battery(seq, label):
    """Run iid-random and mono-shuffle nulls; report regime distribution."""
    out = {}
    for name, fn in (("iid_random", iid_random), ("mono_shuffle", mono_shuffle)):
        rng = random.Random(SEED)  # deterministic per null type
        regimes, cgs, chgs = [], [], []
        for _ in range(K_NULL):
            s = fn(seq, rng)
            cg, chg, _ = M.bulk_contexts(s)
            regimes.append(M.detect_regime(cg, chg))
            cgs.append(cg); chgs.append(chg)
        from collections import Counter
        dist = dict(Counter(regimes))
        out[name] = {
            "regime_counts": {k: dist[k] for k in sorted(dist)},
            "cg_oe_mean": round(sum(cgs) / len(cgs), 4),
            "chg_oe_mean": round(sum(chgs) / len(chgs), 4),
            "methylation_class_called": any(
                ("PLANT" in r or "VERTEBRATE" in r or "INSECT_targeted" in r) for r in regimes),
        }
    return out


def grade(label, regime, expected_kind):
    """expected_kind: 'PLANT' | 'VERTEBRATE' | 'NO_GLOBAL' | 'OUT_OF_CATEGORY'."""
    has_meth_class = ("PLANT" in regime or "VERTEBRATE" in regime
                      or "INSECT_targeted" in regime)
    if expected_kind == "PLANT":
        return "CORRECT" if "PLANT" in regime else "MISCLASSIFIED"
    if expected_kind == "VERTEBRATE":
        return "CORRECT" if "VERTEBRATE" in regime else "MISCLASSIFIED"
    if expected_kind == "NO_GLOBAL":
        # organism has no global 5mC; any global methylation class is a false positive
        return "MISCLASSIFIED" if has_meth_class else "CORRECT"
    if expected_kind == "OUT_OF_CATEGORY":
        # no detector class exists for this biology -> [O] unless it false-positives
        return "[O]_false_positive" if has_meth_class else "[O]_no_class"
    return "UNKNOWN"


def main():
    prov = json.load(open(os.path.join(HERE, "inputs", "_provenance.json")))

    # expected_kind per adversarial organism (from known biology)
    expected = {
        "tomato": "PLANT", "cow": "VERTEBRATE", "dog": "VERTEBRATE",
        "neurospora": "OUT_OF_CATEGORY", "oyster": "OUT_OF_CATEGORY",
        "dictyostelium": "NO_GLOBAL", "tetrahymena": "NO_GLOBAL",
    }
    at_rich_null_targets = {"dictyostelium", "tetrahymena"}  # + plasmodium from panel

    results = {"seed": SEED, "k_null": K_NULL, "engine_sha256": ENGINE_SHA,
               "adversarial": {}, "panel_recheck": {}, "nulls": {}}

    # ---- PART 1: adversarial out-of-panel classification ----
    for o in prov["organisms"]:
        lbl = o["label"]
        seq = read_seq(os.path.join(HERE, "inputs", f"{lbl}.fa"))
        c = classify(seq)
        g = grade(lbl, c["regime"], expected[lbl])
        results["adversarial"][lbl] = {
            **c, "known_biology": o["known_biology"],
            "expected_kind": expected[lbl], "grade": g}

    # ---- PART 1b: re-check the 12-organism PANEL (latent Plasmodium finding) ----
    panel_prov = json.load(open(os.path.join(PANEL_DIR, "_provenance.json")))
    panel_expected = {
        "human": "VERTEBRATE", "mouse": "VERTEBRATE", "chicken": "VERTEBRATE",
        "frog": "VERTEBRATE", "zebrafish": "VERTEBRATE",
        "arabidopsis": "PLANT", "rice": "PLANT", "maize": "PLANT",
        "fly": "NO_GLOBAL", "worm": "NO_GLOBAL", "yeast": "NO_GLOBAL",
        "plasmodium": "NO_GLOBAL",  # trace only
    }
    for lbl in panel_prov["organisms"]:
        seq = read_seq(os.path.join(PANEL_DIR, f"{lbl}.fa"))
        c = classify(seq)
        g = grade(lbl, c["regime"], panel_expected[lbl])
        results["panel_recheck"][lbl] = {
            **c, "expected_kind": panel_expected[lbl], "grade": g}

    # ---- PART 2: mechanistic null for AT-rich misclassifiers (+ panel plasmodium) ----
    null_targets = []
    for lbl in at_rich_null_targets:
        null_targets.append((lbl, os.path.join(HERE, "inputs", f"{lbl}.fa")))
    null_targets.append(("plasmodium", os.path.join(PANEL_DIR, "plasmodium.fa")))
    for lbl, path in null_targets:
        seq = read_seq(path)
        results["nulls"][lbl] = {
            "observed_regime": classify(seq)["regime"],
            "gc_pct": round(M.gc(seq) * 100, 2),
            **null_battery(seq, lbl)}

    # ---- summary ----
    adv = results["adversarial"]
    n_correct = sum(1 for v in adv.values() if v["grade"] == "CORRECT")
    n_misclass = sum(1 for v in adv.values() if v["grade"] == "MISCLASSIFIED")
    n_o = sum(1 for v in adv.values() if v["grade"].startswith("[O]"))
    results["summary"] = {
        "adversarial_n": len(adv),
        "correct": n_correct, "misclassified": n_misclass, "out_of_category": n_o,
        "within_class_generalization": {
            k: adv[k]["grade"] for k in ("tomato", "cow", "dog")},
        "composition_false_positive": {
            k: adv[k]["grade"] for k in ("dictyostelium", "tetrahymena")},
        "panel_plasmodium_grade": results["panel_recheck"]["plasmodium"]["grade"],
    }

    outp = os.path.join(HERE, "stress_detector_adversarial_results.json")
    json.dump(results, open(outp, "w"), indent=2, sort_keys=True)
    print(json.dumps(results["summary"], indent=2))
    print("\n--- adversarial classification ---")
    for lbl, v in adv.items():
        print(f"{lbl:14} GC={v['gc_pct']:>5.1f}% CG={v['cg_oe']:>6.3f} CHG={v['chg_oe']:>5.2f} "
              f"-> {v['regime']:36} [{v['grade']}]  (exp {v['expected_kind']})")
    print("\n--- mechanistic null (AT-rich) : does the methylation-class call survive matched-composition nulls? ---")
    for lbl, v in results["nulls"].items():
        ir = v["iid_random"]; ms = v["mono_shuffle"]
        print(f"{lbl:13} GC={v['gc_pct']:>5.1f}% obs={v['observed_regime']:34}")
        print(f"   iid_random : CHG_OE~{ir['chg_oe_mean']:.3f} meth_class_called={ir['methylation_class_called']}  {ir['regime_counts']}")
        print(f"   mono_shuf  : CHG_OE~{ms['chg_oe_mean']:.3f} meth_class_called={ms['methylation_class_called']}  {ms['regime_counts']}")
    print(f"\nwrote {outp}")


if __name__ == "__main__":
    main()
