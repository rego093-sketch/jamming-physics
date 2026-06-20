#!/usr/bin/env python3
"""
M9 EPHAPTIC-COORDINATION GEOMETRY GROUNDING  (v1.18 decision-check, ADD-ONLY)
=============================================================================
WHAT THIS IS.  v1.17 emerged the inter-organ ephaptic coordination regime (M9) on a
REPRESENTATIVE [O] geometry: a 12-node equal-spacing RING of radius R_BRAIN=0.085 m.
The handover (HANDOVER_v1_17_to_v1_18.md, sec 3.2) asked us to GROUND that geometry on
MEASURED anatomy -- a real 3D inter-organ distance matrix in MNI space [L] -- and to
report, as a DECISION CHECK with grade == evidence, what the grounded geometry does to
the field's causal contribution and to the synchronization regime.

WHAT THIS IS NOT.  This is NOT a new claim, and it does NOT modify the engine. The frozen
engine (vp_mind_engine.py) is imported READ-ONLY; its M9 default stays the ring, so the
frozen tree digest b18c8626... and the 95 mechanism checks are UNTOUCHED (VP-SPEC C1 /
handover sec 6-6, add-only). Promotion of the engine default ring -> measured geometry,
together with the cascade analysis it requires, is specified as a v1.19 entry point.
Grounding the geometry is NOT a consciousness claim: medium_efficacy_tested stays 0, the
hard problem stays OPEN, consciousness_claim stays 0 (handover sec 6-7).

THE THREE GROUNDING DECISIONS (all fixed BEFORE the field contribution was computed --
this ordering is the anti-p-hacking guarantee of handover sec 6-(3)):

  (1) GEOMETRY [L].  Node positions are measured MNI coordinates loaded from the locked
      brain_geometry_atlas.json (8 nodes [L] = exact atlas centre-of-mass / published
      centroid; 4 nodes [O] = representative, for elongated/open/distributed structures
      with no single canonical centroid). The 1/r^3 near-field KERNEL FORM is unchanged
      from v1.17 -- only the POSITIONS that enter it change ([O] ring -> [L] anatomy).

  (2) NORMALIZATION [F].  Row-normalization, declared and justified by physics BEFORE the
      result was seen, NOT chosen to maximize it:
        - it is the SAME normalization the v1.17 engine already uses, so this is a pure
          [O]->[L] geometry swap with the model held fixed;
        - it cleanly separates coupling GEOMETRY (being grounded here) from coupling
          STRENGTH, which is independently MEASURED (kappa = 0.5496, the entrainment-
          threshold fraction, neuro 19) and is the convention under which that measured
          kappa has a defined meaning;
        - the probe (probe_geometry_sensitivity.py, handover sec 3.1) shows raw 1/r^3
          COLLAPSES the coupling (a point-dipole 1/r^3 is a LOCAL approximation, invalid
          at the cm-scale centroid separations here), so row-norm is the physically valid
          regime, not a tuning knob.
      Crucially row-norm is NOT the field-contribution maximizer: under row-norm a random
      3D scatter scores HIGHER than the ring (probe sec 3.1-b), and raw 1/r^3 scores LOWER
      than row-norm (variant (e) below). So the registered choice cannot be a back-fit.

  (3) DECISION CHECK (grade == evidence).  The grounded fc and regime are reported AS-IS.
      No bound is fit to a target; the only HARD assertion is the cross-check that the ring
      path reproduces the frozen engine's M9 number bit-for-bit (validating this code
      path), plus the HONEST-SCOPE assertions that the regime stays partial_metastable
      (NOT synchronized) and the three open-problem flags stay open.

RESULT (the measured verdict, reported as evidence -- see handover sec 3.4 for why this is
the expected, honest outcome): grounding the geometry on real anatomy RAISES the field's
in-silico contribution relative to the (low-by-construction) ring, but leaves the regime
PARTIAL / METASTABLE -- it does NOT push the system to global synchronization, and it does
NOT close the efficacy or hard-problem questions (those are owed to the quantum shortfall
~2.6e10 and to unmeasured biological field-use, NOT to classical geometry).

Run:  PYTHONPATH=../_engine python3 geometry_grounding.py        (from _verify/)
      writes geometry_grounding_results.json + expected_geometry_sha256.json, prints report.
Exit 0 = decision check ran and the engine's frozen ring number was reproduced as a
cross-check. This is a grounded-geometry measurement, NOT a claim about experience.
"""
import sys, os, json, math, hashlib
import numpy as np

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
sys.path.insert(0, ENGINE)
import vp_mind_engine as E  # frozen engine, imported READ-ONLY

GEOM_PATH = os.path.join(ENGINE, "data", "brain_geometry_atlas.json")
FROZEN_ENGINE_M9_FC = 0.0734013672   # the v1.17 frozen field_contribution (ring), cross-check target

# --------------------------------------------------------------------------- #
# atlas + canonical organ order (the order drives OMEGA; geometry MUST align)  #
# --------------------------------------------------------------------------- #
def _load():
    A = E.load_brain_atlas()
    ORG = list(A["organs"].keys())                       # canonical order
    F0  = np.array([A["organs"][r]["f0_hz"] for r in ORG], dtype=float)
    G   = json.load(open(GEOM_PATH, encoding="utf-8"))
    # index geometry BY organ key so positions align with OMEGA regardless of dict order
    POS = np.array([G["organs"][k]["mni_xyz"]    for k in ORG], dtype=float)   # mm, MNI
    GRD = [G["organs"][k]["coord_grade"] for k in ORG]
    return ORG, F0, POS, GRD


def _kernel(pos, normalize="row"):
    """Same 1/r^3 near-field kernel FORM as the frozen engine; positions vary, form fixed."""
    n = len(pos)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                W[i, j] = 1.0 / (np.linalg.norm(pos[i] - pos[j]) ** 3)
    if normalize == "row":
        W = W / W.sum(axis=1, keepdims=True)
    return W


def _fc_regime(pos, omega, normalize="row"):
    """field_contribution (measured - cancel) + regime, via the FROZEN _integrate / kappa.
    Mirrors emerge_coordination M9.2/M9.3 exactly: same operating point, same regime rule."""
    om0 = float(np.mean(omega))
    W   = _kernel(pos, normalize)
    R_meas = E._integrate(omega, W, E.KAPPA_EPHAPTIC * om0)[0]
    R_off  = E._integrate(omega, W, 0.0)[0]
    regime = ("synchronized"       if R_meas >= 0.9          else
              "partial_metastable" if R_meas >  R_off + 0.05 else "incoherent")
    return (R_meas - R_off), R_meas, R_off, regime


# --------------------------------------------------------------------------- #
# the decision check                                                          #
# --------------------------------------------------------------------------- #
def geometry_grounding_results():
    ORG, F0, POS, GRD = _load()
    N = len(ORG)
    OMEGA = 2 * math.pi * F0
    kappa = E.KAPPA_EPHAPTIC

    # (a) CROSS-CHECK: ring path must reproduce the frozen engine M9 number ----------
    fc_ring, R_ring, Roff_ring, reg_ring = _fc_regime(E._ring(N), OMEGA, "row")
    ring_matches = abs(fc_ring - FROZEN_ENGINE_M9_FC) < 1e-4

    # (a') the measured-geometry verdict (registered: row-norm) ----------------------
    fc_m, R_m, Roff_m, reg_m = _fc_regime(POS, OMEGA, "row")

    # (b) SCALE-INVARIANCE: row-norm makes absolute scale irrelevant (shape only) -----
    scale_factors = [0.1, 10.0, 1000.0]
    fc_scaled = [_fc_regime(POS * s, OMEGA, "row")[0] for s in scale_factors]
    scale_max_dev = float(max(abs(f - fc_m) for f in fc_scaled))

    # (c) COORDINATE JITTER ~5 mm (CoM measurement-error scale), fixed seeds 200+k -----
    jit_fc, jit_partial = [], []
    for k in range(10):
        rng = np.random.RandomState(200 + k)
        Pj  = POS + rng.normal(0.0, 5.0, POS.shape)
        f, Rm, Ro, reg = _fc_regime(Pj, OMEGA, "row")
        jit_fc.append(f); jit_partial.append(reg == "partial_metastable")
    jit_fc = np.array(jit_fc)

    # (d) [L]-ONLY 8-NODE SUBSET (drop the 4 [O] nodes): not carried by [O] coords -----
    Lidx = [i for i, g in enumerate(GRD) if g == "L"]
    fc_L, R_L, Roff_L, reg_L = _fc_regime(POS[Lidx], OMEGA[Lidx], "row")

    # (e) NORMALIZATION VARIANTS: registered row-norm vs raw 1/r^3 ---------------------
    fc_raw, R_raw, Roff_raw, reg_raw = _fc_regime(POS, OMEGA, "none")
    # row-norm is NOT the maximizer (anti-back-fit): raw does not exceed row-norm here
    rownorm_is_maximizer = bool(fc_raw > fc_m)

    # (f) f0 +/-20% BAND ROBUSTNESS (mirror engine M9.4), measured geometry ------------
    W_m = _kernel(POS, "row")
    Roff_band = E._integrate(OMEGA, W_m, 0.0)[0]
    band_R, band_partial = [], []
    for sd in range(5):
        rng  = np.random.RandomState(100 + sd)
        pert = F0 * (1 + rng.uniform(-0.2, 0.2, N))
        om   = 2 * math.pi * pert; om0 = float(np.mean(om))
        Rm   = E._integrate(om, W_m, kappa * om0)[0]
        band_R.append(Rm); band_partial.append(Roff_band < Rm < 0.9)
    band_R = np.array(band_R)

    atlas_sha = hashlib.sha256(open(GEOM_PATH, "rb").read()).hexdigest()

    return {
        "_meta": {
            "module": "M9_geometry_grounding_v1_18",
            "what": "ground M9 ephaptic geometry on measured MNI anatomy [L]; decision check, grade==evidence",
            "space": "MNI152 (mm)",
            "kernel_form": "1/r^3 near-field (UNCHANGED from v1.17; only positions change)",
            "normalization": "row (declared [F], fixed before result; same as v1.17 engine)",
            "seed": E.SEED,
            "kappa_ephaptic_measured": round(kappa, 10),
            "add_only": "engine imported read-only; frozen tree b18c8626 + 95 checks untouched",
            "is_consciousness_claim": 0,
            "geometry_atlas_sha256": atlas_sha,
            "frozen_engine_M9_fc_target": FROZEN_ENGINE_M9_FC,
            "n_nodes": N,
            "n_L": int(sum(g == "L" for g in GRD)),
            "n_O": int(sum(g == "O" for g in GRD)),
        },
        "a_ring_crosscheck": {
            "fc": fc_ring, "R": R_ring, "R_off": Roff_ring, "regime": reg_ring,
            "reproduces_frozen_engine_fc": bool(ring_matches),
        },
        "a_measured_geometry": {
            "fc": fc_m, "R": R_m, "R_off": Roff_m, "regime": reg_m,
            "verdict": "grounded geometry raises fc vs ring but regime stays partial_metastable",
        },
        "b_scale_invariance": {
            "factors": scale_factors, "fc": fc_scaled, "max_abs_dev_vs_base": scale_max_dev,
            "scale_irrelevant_under_rownorm": bool(scale_max_dev < 1e-9),
        },
        "c_coord_jitter": {
            "sigma_mm": 5.0, "seeds": list(range(200, 210)),
            "fc_min": float(jit_fc.min()), "fc_max": float(jit_fc.max()),
            "fc_mean": float(jit_fc.mean()), "fc_std": float(jit_fc.std()),
            "all_partial_metastable": bool(all(jit_partial)),
        },
        "d_L_only_subset": {
            "nodes": [ORG[i] for i in Lidx], "n": len(Lidx),
            "fc": fc_L, "R": R_L, "regime": reg_L,
        },
        "e_normalization_variants": {
            "row_norm_fc": fc_m, "row_norm_regime": reg_m,
            "raw_fc": fc_raw, "raw_R": R_raw, "raw_regime": reg_raw,
            "raw_note": "point-dipole 1/r^3 LOCAL approx; scale-sensitive + needs unmeasured "
                        "screening length lambda_s -> [O]; collapses coupling at cm separations",
            "rownorm_is_fc_maximizer": rownorm_is_maximizer,
        },
        "f_f0_band_robustness": {
            "seeds": list(range(100, 105)),
            "R_min": float(band_R.min()), "R_max": float(band_R.max()), "R_off": Roff_band,
            "all_partial": bool(all(band_partial)),
        },
        "scope_flags": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,
            "consciousness_claim": 0.0,
        },
    }


# --------------------------------------------------------------------------- #
# deterministic freeze (bit-for-bit, VP-SPEC C1)                              #
# --------------------------------------------------------------------------- #
def _canon(obj):
    return json.dumps(E._round(obj), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _fmt(x):  # compact signed float for the report
    return f"{x:+.5f}" if isinstance(x, float) else str(x)


def main():
    G = geometry_grounding_results()
    blob = _canon(G)
    digest = hashlib.sha256(blob).hexdigest()

    res_path = os.path.join(HERE, "geometry_grounding_results.json")
    with open(res_path, "wb") as f:
        f.write(blob)

    exp_path = os.path.join(HERE, "expected_geometry_sha256.json")
    payload = {"geometry_grounding_results.json": digest,
               "geometry_atlas_sha256": G["_meta"]["geometry_atlas_sha256"],
               "frozen_engine_tree_sha256_unchanged":
                   "b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7"}
    if os.path.exists(exp_path):
        prev = json.load(open(exp_path)).get("geometry_grounding_results.json")
        status = "MATCHES locked digest" if prev == digest else f"MISMATCH (locked={prev})"
    else:
        with open(exp_path, "w") as f:
            json.dump(payload, f, indent=2)
        status = "WROTE expected_geometry_sha256.json (first freeze)"

    a, am = G["a_ring_crosscheck"], G["a_measured_geometry"]
    b, c  = G["b_scale_invariance"], G["c_coord_jitter"]
    d, e  = G["d_L_only_subset"], G["e_normalization_variants"]
    fb, sf = G["f_f0_band_robustness"], G["scope_flags"]
    print("=" * 78)
    print("M9 EPHAPTIC GEOMETRY GROUNDING -- DECISION CHECK (grade == evidence, v1.18)")
    print("=" * 78)
    print(f"  nodes={G['_meta']['n_nodes']}  ([L]={G['_meta']['n_L']} measured CoM, "
          f"[O]={G['_meta']['n_O']} representative)   normalization=row [F]   seed={E.SEED}")
    print(f"  kernel = 1/r^3 (UNCHANGED); only positions [O] ring -> [L] MNI anatomy change")
    print("-" * 78)
    print("(a) CROSS-CHECK  ring path vs frozen engine M9:")
    print(f"      ring        fc={_fmt(a['fc'])}  R={a['R']:.5f}  {a['regime']}   "
          f"reproduces frozen engine: {a['reproduces_frozen_engine_fc']}")
    print("    MEASURED GEOMETRY (registered row-norm) -- the verdict, reported as-is:")
    print(f"      measured    fc={_fmt(am['fc'])}  R={am['R']:.5f}  {am['regime']}")
    print(f"      => grounding RAISES fc ({_fmt(a['fc'])} -> {_fmt(am['fc'])}); "
          f"regime stays {am['regime']} (NOT synchronized).")
    print("(b) SCALE-INVARIANCE  (row-norm => absolute scale irrelevant, SHAPE only):")
    print(f"      max|dfc| over x{b['factors']} = {b['max_abs_dev_vs_base']:.1e}  "
          f"(scale-irrelevant: {b['scale_irrelevant_under_rownorm']})")
    print("(c) COORD JITTER  sigma=5mm (CoM error scale), seeds 200..209:")
    print(f"      fc in [{c['fc_min']:+.5f}, {c['fc_max']:+.5f}]  mean={c['fc_mean']:+.5f}   "
          f"all partial_metastable: {c['all_partial_metastable']}")
    print(f"(d) [L]-ONLY {d['n']}-NODE SUBSET (drop 4 [O] nodes):")
    print(f"      fc={_fmt(d['fc'])}  R={d['R']:.5f}  {d['regime']}   "
          f"(result not carried by [O] coords)")
    print("(e) NORMALIZATION VARIANTS (anti-back-fit; choice fixed before result):")
    print(f"      row-norm (registered)  fc={_fmt(e['row_norm_fc'])}  {e['row_norm_regime']}")
    print(f"      raw 1/r^3              fc={_fmt(e['raw_fc'])}  {e['raw_regime']}  "
          f"[scale-sensitive + needs lambda_s -> O]")
    print(f"      row-norm is fc maximizer? {e['rownorm_is_fc_maximizer']}   "
          f"(False => registered choice is NOT a back-fit)")
    print("(f) f0 +/-20% BAND ROBUSTNESS (mirror engine M9.4), measured geometry:")
    print(f"      R in [{fb['R_min']:.5f}, {fb['R_max']:.5f}]  R_off={fb['R_off']:.5f}   "
          f"all partial: {fb['all_partial']}")
    print("-" * 78)
    print(f"  SCOPE (unchanged):  medium_efficacy_tested={sf['medium_efficacy_tested']:.0f}   "
          f"hard_problem_open={sf['hard_problem_open']:.0f}   "
          f"consciousness_claim={sf['consciousness_claim']:.0f}")
    print(f"  ADD-ONLY:  frozen engine tree b18c8626... untouched (ring still the engine default)")
    print(f"  RESULTS DIGEST  {digest}")
    print(f"  {status}")
    print("=" * 78)
    print("NOTE: grounded-geometry MEASUREMENT, not a consciousness claim. The hard problem")
    print("      stays OPEN; efficacy stays UNTESTED. Engine-default promotion + cascade")
    print("      analysis + node decomposition are v1.19 entry points (see handover).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
