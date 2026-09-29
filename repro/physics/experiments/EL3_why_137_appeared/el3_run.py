"""EL3: audit of why a0/(D/4pi) = 137 appeared in EL2 (implements PREREG.json). Deterministic."""
import json, os, hashlib, math
HERE = os.path.dirname(os.path.abspath(__file__))
inv_alpha = 137.035999084          # CODATA 2018
a0_codata = 52.9177210903e-12      # CODATA Bohr radius = reduced lambda_C / alpha (computed from alpha)
lamC = 2.42631023867e-12
D_anch = 4.852620477e-12           # s13 anchor, locked to 2 lambda_C
lam_ref = 632.99e-9                # s10 light anchor
A_lat, A_lo, A_hi = 7.79e5, 6.95e5, 8.53e5   # jamming-run amplification (w0 scorecard, E2)
D_circ_median, D_circ_best = 4.96e-12, 4.8542e-12
mpme = 1836.15267343

r = lambda a0, D: a0 / (D / (4 * math.pi))
P1_val = r(a0_codata, D_anch) / inv_alpha - 1
el2_bridge, el2_target = 137.0367, 137.0353
rounding = 52.918 / 52.9177210903 - 1              # EL2 bridge used a0 rounded to 52.918 pm
target_offset = el2_target / inv_alpha - 1          # EL2 energy-ratio target vs CODATA (higher-order terms in E_ion)
reduced_mass = target_offset
P1_explained = abs((el2_bridge / el2_target - 1) - (rounding - target_offset)) < 2e-6

indep = {
    "D_lattice_A_central": 2 * math.pi * lam_ref / A_lat,
    "D_lattice_A_low": 2 * math.pi * lam_ref / A_lo,
    "D_lattice_A_high": 2 * math.pi * lam_ref / A_hi,
    "D_circulation_median": D_circ_median,
    "D_circulation_best_selected": D_circ_best,
}
P2 = {k: {"D_pm": v * 1e12, "inv_alpha": r(a0_codata, v), "rel": r(a0_codata, v) / inv_alpha - 1} for k, v in indep.items()}
vals = [P2["D_lattice_A_low"]["inv_alpha"], P2["D_lattice_A_high"]["inv_alpha"]]
P2_contains = min(vals) <= inv_alpha <= max(vals)
P2_centre_off = abs(P2["D_lattice_A_central"]["rel"]) > 0.01
A_needed = math.pi * lam_ref / lamC
res = {
    "P1_circular": {"rel": P1_val, "verdict": "CONFIRMED (identity)" if abs(P1_val) < 1e-8 else "NOT circular",
                    "EL2_residual_explained": P1_explained, "rounding": rounding, "reduced_mass_term": reduced_mass},
    "P2_independent_D": {"cases": P2, "interval_contains_137": P2_contains, "centre_off_by_more_than_1pct": P2_centre_off,
                         "verdict": "CONFIRMED" if (P2_contains and P2_centre_off) else "NOT as predicted"},
    "P3_information": {"A_needed_for_D_eq_2lamC": A_needed, "A_lattice": A_lat,
                       "E2_ratio": A_lat / A_needed,
                       "hydrogen_radius_in_quanta_a0_over_D": a0_codata / D_anch,
                       "equals_1_over_4pi_alpha": inv_alpha / (4 * math.pi),
                       "old_form_11_minus_delta_proj": 11 - a0_codata / D_anch},
}
txt = json.dumps(res, indent=2)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(f"P1 a0_CODATA/(D_anch/4pi)/inv_alpha - 1 = {P1_val:.1e} -> {res['P1_circular']['verdict']}; EL2 residual explained: {P1_explained}")
for k, v in P2.items():
    print(f"P2 {k:28s} D = {v['D_pm']:.3f} pm -> 1/alpha = {v['inv_alpha']:7.2f} ({v['rel']:+.3f})")
print(f"P2 interval contains 137: {P2_contains}; centre off >1%: {P2_centre_off} -> {res['P2_independent_D']['verdict']}")
p3 = res["P3_information"]
print(f"P3 A needed {A_needed:.4e} vs lattice {A_lat:.2e} (E2 ratio {p3['E2_ratio']:.3f}); hydrogen radius = {p3['hydrogen_radius_in_quanta_a0_over_D']:.4f} D = 11 - {p3['old_form_11_minus_delta_proj']:.4f}")
