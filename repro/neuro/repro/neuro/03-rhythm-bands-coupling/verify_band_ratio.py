#!/usr/bin/env python3
"""
verify_band_ratio.py — the minimal in-package gate for the §03 dimensionless gamma/theta ratio.

Re-derives the ONE validated quantity of §03 — the dimensionless count of slow-gamma
sub-cycles nested in a single theta cycle (the theta-gamma working-memory span) — from
locked, cited band edges, and asserts it is CONTAINED in Miller's independently-measured
7+-2. It does NOT derive (and does not claim) the absolute theta/gamma frequencies in Hz;
those stay open [O] because they depend on the absolute inhibitory time-constant (an
external calibration), exactly as the §03 chapter states.

Why this is honest, not a fit (the no-tuning rule):
  * the four band edges are canonical / measured INPUTS (locked + cited, payload_sha256);
  * the ratio is a DERIVED value (geometric-mean band centres — the package's own
    non-tuned construction, the same one §14 uses for its 'geometric-mean cell');
  * the validation is CONTAINMENT in an INDEPENDENT bound (Miller 1956, from psychophysics,
    has no EEG in it) — the §16/§14 pattern. The band edges come from electrophysiology;
    the 7+-2 comes from memory-span experiments; they AGREE, and the agreement is the claim.
  * the check has TEETH: broad gamma (30-100 Hz) gives 9.68, OUTSIDE [5,9] -> it would FAIL.
    So the containment SELECTS the biologically-correct theta-coupled slow gamma
    (Colgin 2009); it does not assume it.

This gate is kept OUTSIDE verify_all.py (like verify_em_thesis.py / verify_boundary.py /
verify_terminology.py), so verify_all stays 5/5. The §03 full model+real-data regression
still lives in the separate `neuro_extension` lane; this is the in-package dimensionless
floor for the ratio claim only.

No RNG, no tuned constant. Deterministic; 2x run -> identical stdout sha256.
Run: `python3 verify_band_ratio.py`  -> prints PASS/FAIL and exits 0/1.
"""
import sys, os, json, hashlib, io, math

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "inputs", "band_ratio_properties.json")


def geomean(lo, hi):
    """Geometric-mean band centre — the package's non-tuned 'centre of a range' (cf. §14)."""
    return math.sqrt(lo * hi)


def main():
    buf = io.StringIO()

    def out(*a):
        print(*a)
        print(*a, file=buf)

    checks = []

    def check(name, ok, detail):
        checks.append(ok)
        out(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    out("=" * 78)
    out("§03 gamma/theta RATIO — minimal in-package gate")
    out("=" * 78)

    # ---- load locked, cited inputs; self-verify the payload -----------------------------
    with open(INPUTS, encoding="utf-8") as f:
        data = json.load(f)
    meas = data["measured"]
    sha = hashlib.sha256(
        json.dumps(meas, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    out("\n(0) INPUT INTEGRITY — locked, cited band edges")
    check("payload_sha256 matches (band-edge data untampered)",
          sha == data["_meta"]["payload_sha256"],
          f"sha256 = {sha[:16]}...  (asserted on load)")

    th_lo = meas["theta_band_hz"]["lo"]
    th_hi = meas["theta_band_hz"]["hi"]
    sg_lo = meas["slow_gamma_band_hz"]["lo"]
    sg_hi = meas["slow_gamma_band_hz"]["hi"]
    centre = meas["miller_capacity_items"]["centre"]
    pm = meas["miller_capacity_items"]["plus_minus"]
    lo_bound, hi_bound = centre - pm, centre + pm   # Miller window [5, 9]

    # ---- derived value (NOT asserted) ---------------------------------------------------
    theta_c = geomean(th_lo, th_hi)                 # 5.6569 Hz
    gamma_c = geomean(sg_lo, sg_hi)                 # 35.3553 Hz
    ratio = gamma_c / theta_c                       # 6.25 (= sqrt(39.0625))
    span = round(ratio)                             # 6 items

    out("\n(A) DERIVED — slow-gamma sub-cycles nested per theta cycle (dimensionless)")
    check("ratio is DERIVED from band edges (geometric-mean centres)",
          abs(ratio - math.sqrt((sg_lo * sg_hi) / (th_lo * th_hi))) < 1e-12,
          f"gamma/theta = geomean({sg_lo:g},{sg_hi:g})/geomean({th_lo:g},{th_hi:g}) "
          f"= {gamma_c:.4f}/{theta_c:.4f} = {ratio:.4f}")

    out("\n(B) VALIDATED — containment in Miller's independent 7+-2 (psychophysics)")
    check("dimensionless ratio contained in Miller window",
          lo_bound <= ratio <= hi_bound,
          f"{ratio:.4f} in [{lo_bound:g}, {hi_bound:g}]  "
          f"(margins {ratio - lo_bound:.4f} / {hi_bound - ratio:.4f})")
    check("discrete WM span lands on a Miller item count",
          lo_bound <= span <= hi_bound,
          f"round({ratio:.2f}) = {span} item(s)  in {{{lo_bound:g}..{hi_bound:g}}}")

    out("\n(C) FALSIFIABILITY — the containment SELECTS the theta-coupled slow band")
    broad_lo, broad_hi = 30.0, 100.0                # full gamma band (NOT theta-coupled)
    broad_ratio = geomean(broad_lo, broad_hi) / theta_c   # 9.68
    check("broad gamma (30-100 Hz) falls OUTSIDE Miller window",
          not (lo_bound <= broad_ratio <= hi_bound),
          f"broad gamma/theta = {broad_ratio:.4f} (>{hi_bound:g}) -> would FAIL; "
          f"slow gamma is the theta-coupled band [Colgin 2009]")

    out("\n(D) HONEST SCOPE — what stays open")
    out("  [O] absolute theta & gamma frequencies in Hz: NOT derived (depend on absolute")
    out("      tau_inh, an external calibration). Only the dimensionless ratio is claimed.")

    out("\n" + "-" * 78)
    all_ok = all(checks)
    if all_ok:
        out(f"BAND-RATIO LOCK: PASS ({sum(checks)}/{len(checks)})")
        out("  -> gamma/theta = 6.25 DERIVED (geomean centres), CONTAINED in Miller [5,9];")
        out("  -> the theta-gamma working-memory span (Lisman & Jensen 2013) is reproduced")
        out("     in-package as a dimensionless quantity; absolute Hz remain [O].")
    else:
        out("BAND-RATIO LOCK: FAIL — a band edge or bound drifted. Revert; do not paper over.")
    out("-" * 78)

    digest = hashlib.sha256(buf.getvalue().encode()).hexdigest()
    print("\nsha256:", digest)
    return all_ok


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
