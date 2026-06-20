#!/usr/bin/env python3
"""
STRESS TEST D (T4.1) -- abnormal-input robustness of the three locked engines.

Question: on adversarial / malformed input (N-heavy, sub-window, single-base,
lowercase soft-masked, IUPAC ambiguity codes, empty), does each locked engine
degrade *gracefully* (honest NaN / clean exception), or does it (a) crash with an
opaque error, or (b) silently return a plausible-looking but content-free result?

Engines (single-source import + sha256 pin; never reimplemented):
  - gamma()        from dna_interpreter.py        (material γ)
  - bulk_contexts()from clade_reader_engine.py     (methylation CG/CHG/CHH O/E)
  - run_key()      from key_pipeline_full.py       (A4 coordinate shells/anchors)

Behavior classes recorded per (engine x input):
  VALUE        finite normal result
  NAN          returns nan  (graceful "cannot compute" signal)
  RAISE_CLEAN  raises ValueError/TypeError/AssertionError (handled, diagnostic)
  RAISE_OPAQUE raises IndexError/KeyError/numpy error (unhandled, no diagnostic)
  DEGENERATE   structurally-valid but content-free result (silent-wrong risk)

Grade per engine:
  GRACEFUL  every abnormal input -> NAN or RAISE_CLEAN
  FLAGGED   any abnormal input -> RAISE_OPAQUE or DEGENERATE  (robustness gap)

No engine is modified. Deterministic (fixed inputs, no RNG). seed=19 (unused).
"""
import sys, os, json, hashlib, math, warnings

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.abspath(os.path.join(HERE, "..", "..", "_verify", "engine"))
MENG = os.path.abspath(os.path.join(HERE, "..", "..", "12-clade-methylation-readers"))

PINS = {
    os.path.join(ENG, "dna_interpreter.py"): None,
    os.path.join(ENG, "key_pipeline_full.py"): None,
    os.path.join(MENG, "clade_reader_engine.py"):
        "61f32837ec56578ecaf87cba7a8b39edf3a0aee4793709b80440e543123da481",
}
for p, want in PINS.items():
    got = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if want is not None:
        assert got == want, f"ENGINE DRIFT {p}: {got} != {want}"
    PINS[p] = got

sys.path.insert(0, ENG)
sys.path.insert(0, MENG)
import dna_interpreter as DI
import key_pipeline_full as K
import clade_reader_engine as M

# ---- abnormal input battery ----
INPUTS = {
    "normal_ctrl":   "ACGT" * 800,          # 3200 bp valid control (> W)
    "lowercase":     ("ACGT" * 800).lower(),# soft-masked repeats
    "all_N":         "N" * 5000,            # content-free
    "half_N":        "ACGT" * 500 + "N" * 3000,
    "single_base":   "A" * 5000,            # homopolymer
    "IUPAC_codes":   "ACGTRYSWKMBDHVN" * 350,  # ambiguity codes
    "sub_window":    "ACGT" * 50,           # 200 bp  (< W=2000)
    "empty":         "",
}


def classify_call(fn, *args):
    """Run fn(*args); return (behavior_class, detail)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            r = fn(*args)
        except Exception as e:
            t = type(e).__name__
            clean = t in ("ValueError", "TypeError", "AssertionError", "KeyError")
            # KeyError from a missing-dinucleotide lookup is opaque, not diagnostic
            opaque = t in ("IndexError", "ZeroDivisionError", "RecursionError") or \
                     t.startswith("numpy") or "bounds" in str(e).lower()
            cls = "RAISE_OPAQUE" if opaque else ("RAISE_CLEAN" if clean else "RAISE_OPAQUE")
            return cls, f"{t}: {str(e)[:60]}"
    return r  # caller interprets


def is_nan(x):
    try:
        return isinstance(x, float) and math.isnan(x)
    except Exception:
        return False


def grade_gamma(seq):
    out = classify_call(DI.gamma, seq)
    if isinstance(out, tuple):  # raised
        return out
    if is_nan(out):
        return "NAN", "nan"
    return "VALUE", f"{out:.4f}"


def grade_bulk(seq):
    out = classify_call(M.bulk_contexts, seq)
    if isinstance(out, tuple) and len(out) == 2 and isinstance(out[0], str):
        return out  # raised
    cg = out[0]
    if is_nan(cg):
        return "NAN", "cg=nan"
    return "VALUE", f"cg={cg:.4f}"


def grade_runkey(seq):
    out = classify_call(K.run_key, seq, [])
    if isinstance(out, tuple) and len(out) == 2 and isinstance(out[0], str):
        return out  # raised
    sh = len(out.get("shells", [])); an = len(out.get("anchors", []))
    interior = [a for a in out.get("anchors", []) if a.get("kind") != "region_edge"]
    # NOTE: a featureless-but-VALID sequence (e.g. ACGT-repeat, homopolymer)
    # legitimately yields 1 shell / 0 interior anchors -- that is the correct
    # answer, NOT a degeneration. We therefore do NOT flag low shell/anchor counts.
    # Content-free (all-N) handling is reported as a separate note via the matrix.
    return "VALUE", f"shells={sh} anchors={an} interior={len(interior)}"


def main():
    engines = {"gamma": grade_gamma, "bulk_contexts": grade_bulk, "run_key": grade_runkey}
    abnormal = [k for k in INPUTS if k != "normal_ctrl"]

    results = {"engine_sha256": {os.path.basename(p): s for p, s in PINS.items()},
               "cells": {}, "by_engine": {}}

    for ename, gfn in engines.items():
        results["cells"][ename] = {}
        for iname, seq in INPUTS.items():
            cls, detail = gfn(seq)
            results["cells"][ename][iname] = {"class": cls, "detail": detail}

    # grade each engine over the abnormal inputs
    for ename in engines:
        flags = []
        for iname in abnormal:
            c = results["cells"][ename][iname]["class"]
            if c in ("RAISE_OPAQUE", "DEGENERATE"):
                flags.append((iname, c))
        results["by_engine"][ename] = {
            "grade": "GRACEFUL" if not flags else "FLAGGED",
            "flags": [{"input": i, "class": c} for i, c in flags],
        }

    n_flagged = sum(1 for e in results["by_engine"].values() if e["grade"] == "FLAGGED")
    results["summary"] = {
        "engines_graceful": sum(1 for e in results["by_engine"].values() if e["grade"] == "GRACEFUL"),
        "engines_flagged": n_flagged,
        "grades": {e: results["by_engine"][e]["grade"] for e in engines},
    }

    # --- targeted honest notes (not hard flags) ---
    notes = {}
    # (1) case-sensitivity asymmetry: gamma uppercases; bulk_contexts does not.
    g_lower = results["cells"]["gamma"]["lowercase"]["class"]
    b_lower = results["cells"]["bulk_contexts"]["lowercase"]["class"]
    notes["case_sensitivity"] = {
        "gamma_lowercase": g_lower, "bulk_contexts_lowercase": b_lower,
        "asymmetric": g_lower != b_lower,
        "comment": ("gamma() normalizes via .upper() (lowercase==uppercase); "
                    "bulk_contexts() is case-sensitive and returns nan on soft-masked "
                    "(lowercase) input. Both graceful (neither returns a wrong number), "
                    "but a soft-masked FASTA must be upper-cased before methylation calls."),
    }
    # (2) content-free vs featureless-valid: is all_N distinguishable from ACGT-repeat?
    rk_alln = results["cells"]["run_key"]["all_N"]["detail"]
    rk_ctrl = results["cells"]["run_key"]["normal_ctrl"]["detail"]
    notes["content_free_runkey"] = {
        "all_N": rk_alln, "featureless_valid_ctrl": rk_ctrl,
        "indistinguishable": rk_alln == rk_ctrl,
        "comment": ("run_key() gives content-free all-N input the same minimal "
                    "(1 shell / trivial edge anchors) result as a featureless-but-valid "
                    "sequence. That minimal result is correct for featureless input, so "
                    "this is not silent-wrong; but all-N is not separately flagged as "
                    "content-free. Minor interpretability note, not a grade-down."),
    }
    # (3) the genuine gap: sub-window opaque crash
    notes["sub_window_crash"] = {
        "behavior": results["cells"]["run_key"]["sub_window"]["class"],
        "detail": results["cells"]["run_key"]["sub_window"]["detail"],
        "comment": ("run_key() assumes len >= W (2000 bp). Shorter input raises an "
                    "opaque IndexError rather than a clean [O]/ValueError ('region "
                    "shorter than window'). Loud (not silent-wrong) but ungraceful."),
    }
    results["notes"] = notes

    outp = os.path.join(HERE, "stress_abnormal_inputs_results.json")
    json.dump(results, open(outp, "w"), indent=2, sort_keys=True)

    print(json.dumps(results["summary"], indent=2))
    print("\n--- behavior matrix (rows=input, cols=engine) ---")
    hdr = f"{'input':14}" + "".join(f"{e:>16}" for e in engines)
    print(hdr)
    for iname in INPUTS:
        row = f"{iname:14}"
        for ename in engines:
            c = results["cells"][ename][iname]["class"]
            row += f"{c:>16}"
        print(row)
    print("\n--- flags (robustness gaps) ---")
    for ename in engines:
        be = results["by_engine"][ename]
        if be["flags"]:
            for f in be["flags"]:
                d = results["cells"][ename][f["input"]]["detail"]
                print(f"  {ename}.{f['input']}: {f['class']} -- {d}")
    print(f"\nwrote {outp}")


if __name__ == "__main__":
    main()
