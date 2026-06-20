#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
renal_phosphate.py  --  the ACTUAL renal phosphate threshold (TmP/GFR), narrowing the RI5 [O].

Context: vp_loops.ri5_phosphate already reproduces the FGF23 lowering-arm MECHANISM [V] and keeps the
Ca x PO4 product below precipitation [V]; but the absolute renal transport maximum was deferred as an
"[O] needs external calibration" item. This module CLOSES the deferrable part of that gap: it implements
the standard clinical computation of the phosphate threshold (Walton & Bijvoet 1975 nomogram) -- exact
algebra on MEASURABLE inputs -- so the threshold is no longer an invented number but a reproducible
function, and it is cross-checked against the published adult reference range.

What remains [O] is now PRECISE and honest: gamma (DNA) sets loop STABILITY (basin barrier b=g^2/4 -> loop
gain k), NOT the absolute setpoint VALUE. So "predict TmP/GFR from gamma alone" stays open BY DESIGN -- the
value is clinical [CAL] / exact-algebra [F], never gamma-derived. The framework never claimed otherwise;
this module makes the boundary explicit and reproducible instead of merely deferring it.

GRADES (VP-SPEC C3): TmP/GFR algebra exact [F]; clinical inputs measured [CAL]; reference-range cross-check
[L]; FGF23/PTH LOWER the threshold (direction) [V]/[L]; gamma -> absolute value [O] (stated, by design).
Determinism (C1): pure deterministic algebra (no RNG); round-before-return.
"""

# adult TmP/GFR reference interval (mmol/L); Payne 1998 Ann Clin Biochem / Walton & Bijvoet 1975 Lancet
REF_LOW, REF_HIGH = 0.80, 1.35


def trp(PP, PCr, UP, UCr):
    """Tubular Reabsorption of Phosphate fraction: TRP = 1 - (UP*PCr)/(PP*UCr). Dimensionless.
    P in mmol/L, Cr in mmol/L (ratio is unit-free)."""
    return 1.0 - (UP * PCr) / (PP * UCr)


def tmp_gfr(PP, PCr, UP, UCr):
    """Walton & Bijvoet (1975) renal phosphate threshold, mmol/L -- the EXACT published nomogram:
         TRP <= 0.86 :  TmP/GFR = TRP * PP                      (linear region)
         TRP  > 0.86 :  TmP/GFR = (0.3*TRP)/(1 - 0.8*TRP) * PP  (Bijvoet non-linear correction)
    Returns (TmP_GFR, TRP)."""
    t = trp(PP, PCr, UP, UCr)
    val = (t * PP) if t <= 0.86 else (0.3 * t) / (1.0 - 0.8 * t) * PP
    return val, t


# three physiologically coherent clinical regimes (fasting; P/UP/PP in mmol/L, Cr in mmol/L).
# FGF23 (and PTH) are phosphaturic -> they LOWER TmP/GFR; the inputs below encode that axis.
CASES = {
    "normal":             dict(PP=1.13, PCr=0.080, UP=16.0, UCr=12.0),  # mid reference
    "high_fgf23_XLH":     dict(PP=0.65, PCr=0.080, UP=30.0, UCr=12.0),  # FGF23 high -> low threshold (hypophosphatemia)
    "low_fgf23_hypoPTH":  dict(PP=1.80, PCr=0.080, UP=8.0,  UCr=12.0),  # FGF23/PTH low -> high threshold (hyperphosphatemia)
}


def status():
    cases = {}
    for name, c in CASES.items():
        val, t = tmp_gfr(**c)
        cases[name] = dict(inputs=c, TRP=round(t, 4), TmP_GFR_mmol_L=round(val, 4),
                           in_reference_range=bool(REF_LOW <= val <= REF_HIGH))
    ordered = [cases[k]["TmP_GFR_mmol_L"] for k in ("high_fgf23_XLH", "normal", "low_fgf23_hypoPTH")]
    return dict(
        _what="Renal phosphate threshold TmP/GFR computed EXACTLY (Walton-Bijvoet 1975) from clinical inputs; "
              "the RI5 absolute-transport-maximum [O] is now a reproducible function, not an invented number.",
        reference_range_mmol_L=[REF_LOW, REF_HIGH],
        cases=cases,
        normal_in_reference=bool(cases["normal"]["in_reference_range"]),
        threshold_falls_with_fgf23=bool(ordered[0] < ordered[1] < ordered[2]),  # high-FGF23 < normal < low-FGF23
        setpoint_is_threshold="plasma phosphate is defended near TmP/GFR; above it -> phosphaturia (the 'spill')",
        residual_open="gamma does NOT predict the absolute TmP/GFR value -- by design gamma sets loop STABILITY "
                      "(barrier b=g^2/4 -> gain k), not the measured/cited VALUE; the value is [CAL] clinical / "
                      "[F] exact algebra, never gamma-derived [O]",
        anchor="Walton & Bijvoet 1975 Lancet (nomogram); Payne 1998 Ann Clin Biochem (reference interval); "
               "FGF23/PTH phosphaturia lowers TmP/GFR (CKD-MBD / XLH literature)",
        grade="[F] TmP/GFR algebra exact; [CAL] clinical inputs; [L] reference-range cross-check; "
              "[V]/[L] FGF23/PTH lower the threshold (direction); [O] gamma->absolute-value (stated, by design)")


if __name__ == "__main__":
    import json
    print(json.dumps(status(), ensure_ascii=False, indent=2))
