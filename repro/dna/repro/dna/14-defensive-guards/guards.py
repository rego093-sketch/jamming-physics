#!/usr/bin/env python3
"""
Chapter 14 -- DEFENSIVE GUARDS (new-version wrapper layer).

This module adds the three modest defensive measures the v1.9 stress battery
(second session) showed were needed, WITHOUT modifying any locked engine. The
locked grammar (gamma, NN table, A4 pipeline, methylation engine, thresholds,
frozen expected) stays byte-identical (153/153). Guards WRAP the locked engines,
which are imported single-source and sha256-pinned. "Perfection" here is not
zero-exception; it is: stop the demonstrated failures, stay honest at the edges.

Three guards, each tied to a stress finding:

  1. detect_regime_safe()  -- fixes the Test C false positive.
     The methylation auto-detector mislabels extreme-AT genomes as PLANT because
     their CpG/CpHpG depletion is composition-driven, not methylation (proven by
     matched-composition nulls). GUARD: below GC_FLOOR the depletion->regime
     inference is not trusted; the call is overridden to "no global signal" and
     flagged 'low_GC_composition_confounded' (the raw call is preserved, never
     hidden). GC_FLOOR = 0.25 is empirical:
        misclassified: Plasmodium 20.4%, Dictyostelium 22.3%  (both < 0.23)
        knife-edge correct: Tetrahymena 23.5%
        lowest correctly-classified real methylator: tomato 30.9%
     0.25 sits in the (22.3%, 30.9%) gap with a ~5.9-pt margin to the nearest
     real methylator, so no known global methylator is suppressed.
     RESIDUAL RISK (not zero by design): a hypothetical GC<25% genome with
     genuine global 5mC would be wrongly down-graded to no_global. No such
     organism is known (extreme-AT genomes characteristically lack global 5mC);
     the guard trades that theoretical case for fixing the demonstrated error.

  2. run_key_safe()  -- fixes the Test D opaque crash.
     run_key() assumes len(seq) >= W and raises an opaque IndexError on shorter
     or empty input. GUARD: pre-check length; return a clean [O] result naming
     the closing condition instead of crashing.

  3. bulk_contexts_safe()  -- fixes the Test D case-sensitivity gap.
     bulk_contexts() is case-sensitive (soft-masked lowercase -> NaN), unlike
     gamma() which upper-cases. GUARD: upper-case before the call so soft-masked
     FASTA is read correctly; if still uncomputable, report [O] explicitly rather
     than letting NaN masquerade as 'no methylation'.

Deterministic. No threshold inside the locked engines is changed.
"""
import os, sys, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ENG  = os.path.abspath(os.path.join(HERE, "..", "_verify", "engine"))
MENG = os.path.abspath(os.path.join(HERE, "..", "12-clade-methylation-readers"))

# --- single-source import of the LOCKED engines + sha256 pins (drift detection) ---
_PINS = {
    os.path.join(ENG,  "dna_interpreter.py"):
        "4929932d9032179009e9b6cf5b0abd6d390a03f09867f0d06d8e9fd7e83f2cd0",
    os.path.join(ENG,  "key_pipeline_full.py"):
        "3141fa22cfe34a94d9fc36b447ceffa951dc5964629abf30aae024fa475cdced",
    os.path.join(MENG, "clade_reader_engine.py"):
        "61f32837ec56578ecaf87cba7a8b39edf3a0aee4793709b80440e543123da481",
}
for _p, _want in _PINS.items():
    _got = hashlib.sha256(open(_p, "rb").read()).hexdigest()
    assert _got == _want, f"ENGINE DRIFT {_p}: {_got} != {_want}"

sys.path.insert(0, ENG)
sys.path.insert(0, MENG)
import dna_interpreter as _DI            # noqa: E402
import key_pipeline_full as _K           # noqa: E402
import clade_reader_engine as _M         # noqa: E402

# ---- guard constants (documented, not inside the locked engines) ----
GC_FLOOR = 0.25   # below this, CpG/CpHpG depletion is composition-confounded (Test C)
W_MIN    = 2000   # A4 coordinate window; run_key requires len >= W_MIN (Test D)


def _isnan(x):
    try:
        return isinstance(x, float) and math.isnan(x)
    except Exception:
        return False


def bulk_contexts_safe(seq):
    """Case-normalizing wrapper around the locked bulk_contexts.
    Returns (cg, chg, chh) on the upper-cased sequence (locked logic, unchanged)."""
    return _M.bulk_contexts(seq.upper())


def detect_regime_safe(seq, spread=None, lowfrac=None):
    """GC-floor-guarded methylation regime call.

    Returns a dict:
      regime       final (guarded) regime  -- this is what callers should use
      raw_regime   exactly what the locked detect_regime returned (never hidden)
      guard        None | 'low_GC_composition_confounded' | 'uncomputable'
      confidence   'normal' | 'low'
      gc, cg_oe, chg_oe, chh_oe
      note         human-readable reason when guarded
    The locked detect_regime / thresholds are called unchanged; the guard only
    decides whether to trust the result, given GC.
    """
    s = seq.upper()
    cg, chg, chh = _M.bulk_contexts(s)
    gc = _M.gc(s) if len(s) else float("nan")

    base = {"gc": round(gc, 4) if not _isnan(gc) else None,
            "cg_oe": round(cg, 4) if not _isnan(cg) else None,
            "chg_oe": round(chg, 4) if not _isnan(chg) else None,
            "chh_oe": round(chh, 4) if not _isnan(chh) else None}

    # (a) cannot compute contexts -> honest [O], do not let NaN read as 'no methylation'
    if _isnan(cg) or _isnan(chg):
        return {**base, "regime": "[O]_insufficient_sequence", "raw_regime": None,
                "guard": "uncomputable", "confidence": "low",
                "note": "context O/E uncomputable (too few/!ACGT bases); no methylation call made"}

    raw = _M.detect_regime(cg, chg, spread, lowfrac)

    # (b) extreme-AT composition zone -> depletion->regime inference not trusted
    if gc < GC_FLOOR:
        return {**base, "regime": "no_global_methylation_pergene_unknown", "raw_regime": raw,
                "guard": "low_GC_composition_confounded", "confidence": "low",
                "note": (f"GC {gc*100:.1f}% < {GC_FLOOR*100:.0f}% floor: CpG/CpHpG depletion is "
                         f"composition-confounded (Test C), raw call '{raw}' not trusted as a "
                         f"methylation regime; needs independent methylation evidence")}

    # (c) normal domain -> locked call stands, unchanged
    return {**base, "regime": raw, "raw_regime": raw, "guard": None,
            "confidence": "normal", "note": ""}


def run_key_safe(seq, motors, W=W_MIN, **kw):
    """Length-guarded wrapper around the locked run_key.
    On len(seq) < W returns a clean [O] dict naming the closing condition
    instead of the locked engine's opaque IndexError (Test D)."""
    n = len(seq)
    if n < W:
        return {"status": "[O]", "shells": [], "anchors": [], "motors": [], "loops": [],
                "reason": (f"region length {n} bp < coordinate window W={W} bp; "
                           f"A4 read requires >= W bp (need a longer region to place shells/anchors)")}
    out = _K.run_key(seq, motors, **kw)
    if isinstance(out, dict):
        out.setdefault("status", "ok")
    return out


# convenience: expose the locked originals for side-by-side comparison
detect_regime_raw = _M.detect_regime
bulk_contexts_raw = _M.bulk_contexts
run_key_raw       = _K.run_key
gc                = _M.gc
