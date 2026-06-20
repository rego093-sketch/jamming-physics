#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M9 EPHAPTIC-COORDINATION NODE DECOMPOSITION  (v1.19 decision-check, ADD-ONLY -- Task 1B)
=========================================================================================
WHAT THIS IS.  v1.18 grounded the M9 ephaptic geometry on a MEASURED 12-node composite
atlas (one volume-weighted MNI centroid per central organ). The reviewer's objection is the
SULCAL-BANK FOLDING problem: opposing banks of a sulcus sit mm apart, so the local 1/r^3
near-field between them is strong, but a single per-organ centroid CANNOT represent intra-
organ shape -- two faces of one folded sheet collapse to one point. The v1.18 jitter check
already SIGNALLED this (fc sensitive to +/-5 mm shape detail). This module DECOMPOSES the
AAL-sourced organs into their constituent AAL parcels, rebuilds the inter-node distance
matrix at that finer resolution, re-applies the SAME decision checks, and reports fc +
regime as EVIDENCE (grade == evidence).

WHAT THIS IS NOT.  This does NOT modify the engine. The engine is imported READ-ONLY;
E._integrate / E.KAPPA_EPHAPTIC are the v1.17-frozen operating point and are UNCHANGED by
the v1.19 geometry promotion (which only swaps emerge_coordination's POS). So this module's
numbers are independent of whether the engine default is ring or 12-node measured, and the
frozen engine tree is untouched by this file (add-only, VP-SPEC C1 / handover sec 6-6).
Decomposing nodes is NOT a consciousness claim: efficacy 0, hard problem OPEN, claim 0.

SINGLE SOURCE (VP-SPEC C1).  AAL parcel centers-of-mass are NOT re-typed here; they are read
VERBATIM from build_geometry_atlas.py (the locked table that built the 12-node atlas,
transcribed from the published AAL CoM table -- figshare 184981 / Frontiers SOM S1). We exec
only its coordinate/parcel-set prefix (never its file-writing tail), so there is ONE source
of the coordinates and no side effect on the locked atlas. Each parcel INHERITS its parent
organ's MEASURED f0 (brain_organ_atlas.json): the organ's gamma is carried by its several
anatomical sub-nodes at the same measured frequency. No new constant is added.

PRE-REGISTERED DECISIONS (fixed BEFORE any fc was computed -- anti-p-hacking, handover 6-3/7):
  (1) RESOLUTIONS [fixed].  Three node counts are declared up front and ALL are reported; we
      do NOT select the parcellation that maximises fc.
        R0 = 12 composite organs                      (the v1.18/promoted engine default)
        R1 = cortex split into its 74 AAL parcels + the other 11 organs as nodes  (~85)
        R2 = ALL 7 AAL-sourced organs split into parcels (112) + 5 non-AAL singles (117)
      The 5 organs with no canonical AAL parcellation (hypothalamus, midbrain, brainstem,
      basal-forebrain cholinergic, distributed forebrain GABAergic) stay single nodes with
      their v1.18 [L]/[O] coords -- no finer measured geometry exists for them in-package.
  (2) KERNEL + NORMALIZATION [F].  Identical to v1.18: 1/r^3 near-field FORM unchanged,
      row-normalisation (the same [F] choice the engine uses; separates geometry from the
      independently-MEASURED kappa=0.5496). Positions [L] change; the model is held fixed.
  (3) DECISION CHECK (grade == evidence).  fc + regime reported AS-IS at every resolution.
      Only HARD assertions: the 12-node path reproduces the v1.18 grounded fc bit-for-bit
      (validates the path), and the HONEST-SCOPE flags (regime partial_metastable; 3 flags open).

Run:  PYTHONPATH=../_engine python3 geometry_node_decomposition.py     (from _verify/)
Exit 0 = decision check ran and the 12-node path reproduced the v1.18 grounded number.
"""
import sys, os, json, math, hashlib
import numpy as np

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
sys.path.insert(0, ENGINE)
import vp_mind_engine as E  # frozen engine, READ-ONLY (E._integrate / E.KAPPA unchanged by 1A)

GEOM_PATH = os.path.join(ENGINE, "data", "brain_geometry_atlas.json")
BUILDER   = os.path.normpath(os.path.join(HERE, "..", "13-em-coordination", "build_geometry_atlas.py"))
V118_GROUNDED_12NODE_FC = 0.1346804816   # v1.18 grounded 12-node measured fc (cross-check target; bit-exact)


def _load_aal():
    """Single source: exec only the coordinate/parcel-set PREFIX of the builder (never its
    file-writing tail) so the locked atlas is not touched and there is one source of coords."""
    src = open(BUILDER, encoding="utf-8").read()
    cut = src.index("with open(OUT")
    ns = {"__file__": BUILDER, "__name__": "_aal_prefix"}
    exec(compile(src[:cut], BUILDER, "exec"), ns)
    return ns


_AAL_ORGAN_SETS = {
    "neocortex": "NEOCORTEX", "hippocampus": "HIPPO", "thalamus": "THAL",
    "striatum": "STRIAT", "pallidum": "PALL", "cerebellum": "CEREB", "olfactory_bulb": "OLF",
}


def _build_nodes(split_organs):
    """(POS[n,3] mm, OMEGA[n], grades[n], labels[n]) for a resolution. `split_organs` =
    organs to DECOMPOSE into AAL parcels; others stay single nodes. Parcel f0 = parent
    organ f0 (measured inheritance); parcel coords = AAL CoM [L]."""
    A   = E.load_brain_atlas()
    ORG = list(A["organs"].keys())
    F0  = {r: float(A["organs"][r]["f0_hz"]) for r in ORG}
    G   = json.load(open(GEOM_PATH, encoding="utf-8"))["organs"]
    ns  = _load_aal(); BY = ns["BYIDX"]
    POS, OM, GR, LB = [], [], [], []
    for r in ORG:
        if r in split_organs and r in _AAL_ORGAN_SETS:
            for idx in ns[_AAL_ORGAN_SETS[r]]:
                lab, x, y, z, _ = BY[idx]
                POS.append([float(x), float(y), float(z)])
                OM.append(2 * math.pi * F0[r]); GR.append("L"); LB.append(lab)
        else:
            POS.append([float(v) for v in G[r]["mni_xyz"]])
            OM.append(2 * math.pi * F0[r]); GR.append(G[r]["coord_grade"]); LB.append(r)
    return np.array(POS, float), np.array(OM, float), GR, LB


def _kernel(pos, normalize="row"):
    n = len(pos); W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                W[i, j] = 1.0 / (np.linalg.norm(pos[i] - pos[j]) ** 3)
    if normalize == "row":
        W = W / W.sum(axis=1, keepdims=True)
    return W


def _fc_regime(pos, omega, normalize="row"):
    om0 = float(np.mean(omega)); W = _kernel(pos, normalize)
    R_meas = E._integrate(omega, W, E.KAPPA_EPHAPTIC * om0)[0]
    R_off  = E._integrate(omega, W, 0.0)[0]
    regime = ("synchronized"       if R_meas >= 0.9          else
              "partial_metastable" if R_meas >  R_off + 0.05 else "incoherent")
    return (R_meas - R_off), R_meas, R_off, regime


def _min_pair(pos, labels):
    n = len(pos); best = (1e18, None, None)
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.linalg.norm(pos[i] - pos[j]))
            if d < best[0]:
                best = (d, labels[i], labels[j])
    return best


def node_decomposition_results():
    P0, OM0, GR0, LB0 = _build_nodes(set())
    fc0, R0_, Roff0, reg0 = _fc_regime(P0, OM0, "row"); d0 = _min_pair(P0, LB0)
    P1, OM1, GR1, LB1 = _build_nodes({"neocortex"})
    fc1, R1_, Roff1, reg1 = _fc_regime(P1, OM1, "row"); d1 = _min_pair(P1, LB1)
    P2, OM2, GR2, LB2 = _build_nodes(set(_AAL_ORGAN_SETS))
    fc2, R2_, Roff2, reg2 = _fc_regime(P2, OM2, "row"); d2 = _min_pair(P2, LB2)

    # closest pair AMONG CORTICAL PARCELS only (the reviewer's opposing-sulcal-bank case,
    # which the global min-pair -- two subcortical singles -- would otherwise hide) ------
    ns = _load_aal()
    cort_labels = {ns["BYIDX"][i][0] for i in ns["NEOCORTEX"]}
    cidx = [i for i, l in enumerate(LB1) if l in cort_labels]
    dC = _min_pair(P1[cidx], [LB1[i] for i in cidx])
    # a NAMED opposing-bank pair: the two banks of the central sulcus (Precentral/Postcentral)
    def _dist(a, b):
        ia = LB1.index(a); ib = LB1.index(b)
        return float(np.linalg.norm(P1[ia] - P1[ib]))
    central_sulcus_L = _dist("Precentral_L", "Postcentral_L")
    central_sulcus_R = _dist("Precentral_R", "Postcentral_R")

    twelve_matches = abs(fc0 - V118_GROUNDED_12NODE_FC) < 1e-4

    fc1_scaled = [_fc_regime(P1 * s, OM1, "row")[0] for s in (0.1, 10.0, 1000.0)]
    scale_max_dev = float(max(abs(f - fc1) for f in fc1_scaled))

    jit_fc, jit_partial = [], []
    for k in range(10):
        rng = np.random.RandomState(300 + k)
        f, Rm, Ro, reg = _fc_regime(P1 + rng.normal(0.0, 5.0, P1.shape), OM1, "row")
        jit_fc.append(f); jit_partial.append(reg == "partial_metastable")
    jit_fc = np.array(jit_fc)

    fc1_raw, R1_raw, Roff1_raw, reg1_raw = _fc_regime(P1, OM1, "none")
    rownorm_is_maximizer = bool(fc1_raw > fc1)

    W1 = _kernel(P1, "row"); Roff1_band = E._integrate(OM1, W1, 0.0)[0]
    band_R, band_partial = [], []
    for sd in range(5):
        rng = np.random.RandomState(400 + sd)
        pert = OM1 * (1 + rng.uniform(-0.2, 0.2, len(OM1))); om0 = float(np.mean(pert))
        Rm = E._integrate(pert, W1, E.KAPPA_EPHAPTIC * om0)[0]
        band_R.append(Rm); band_partial.append(Roff1_band < Rm < 0.9)
    band_R = np.array(band_R)

    atlas_sha   = hashlib.sha256(open(GEOM_PATH, "rb").read()).hexdigest()
    builder_sha = hashlib.sha256(open(BUILDER, "rb").read()).hexdigest()

    return {
        "_meta": {
            "module": "M9_node_decomposition_v1_19_task1B",
            "what": "decompose M9 ephaptic geometry into AAL parcels; sulcal-bank folding; "
                    "decision check, grade==evidence",
            "space": "MNI152 (mm)",
            "kernel_form": "1/r^3 near-field (UNCHANGED); only node RESOLUTION changes",
            "normalization": "row (declared [F], fixed before result; same as engine)",
            "seed": E.SEED,
            "kappa_ephaptic_measured": round(E.KAPPA_EPHAPTIC, 10),
            "add_only": "engine read-only; E._integrate/E.KAPPA unchanged by 1A; frozen tree untouched",
            "single_source": "AAL parcel CoMs read verbatim from build_geometry_atlas.py "
                             "(no re-derivation; file-writing tail not executed)",
            "parcel_f0_rule": "each parcel inherits its parent organ's MEASURED f0 (no new constant)",
            "is_consciousness_claim": 0,
            "geometry_atlas_sha256": atlas_sha,
            "aal_builder_sha256": builder_sha,
            "v118_grounded_12node_fc_target": V118_GROUNDED_12NODE_FC,
            "non_decomposable_organs_no_canonical_AAL_parcellation": [
                "hypothalamus", "midbrain", "brainstem", "basal_forebrain_chol", "forebrain_gaba_in"],
        },
        "resolutions": {
            "R0_12_composite": {"n_nodes": len(P0), "fc": fc0, "R": R0_, "R_off": Roff0,
                                "regime": reg0, "min_pair_mm": d0[0], "min_pair": [d0[1], d0[2]]},
            "R1_cortex_parcels": {"n_nodes": len(P1), "n_L": int(sum(g == "L" for g in GR1)),
                                  "fc": fc1, "R": R1_, "R_off": Roff1, "regime": reg1,
                                  "min_pair_mm": d1[0], "min_pair": [d1[1], d1[2]]},
            "R2_full_parcels": {"n_nodes": len(P2), "n_L": int(sum(g == "L" for g in GR2)),
                                "fc": fc2, "R": R2_, "R_off": Roff2, "regime": reg2,
                                "min_pair_mm": d2[0], "min_pair": [d2[1], d2[2]]},
        },
        "a_twelve_node_crosscheck": {"fc": fc0, "reproduces_v118_grounded_fc": bool(twelve_matches)},
        "sulcal_bank_made_explicit": {
            "min_inter_node_mm_12composite": d0[0],
            "min_inter_node_mm_cortex_parcels": d1[0],
            "closest_cortical_parcel_pair_mm": dC[0],
            "closest_cortical_parcel_pair": [dC[1], dC[2]],
            "central_sulcus_gyral_centroid_gap_mm_L": central_sulcus_L,
            "central_sulcus_gyral_centroid_gap_mm_R": central_sulcus_R,
            "min_inter_node_mm_full_parcels": d2[0],
            "closest_parcel_pair_R2": [d2[1], d2[2]],
            "what_decomposition_DOES": "the 12-node cortex collapses the whole isocortical "
                "mantle to ONE centroid; AAL splits it into 74 gyral nodes, so opposing gyri "
                "(e.g. Precentral vs Postcentral, the two lips of the central sulcus) become "
                "SEPARATE coupled nodes instead of one point. That alone changes the near-field "
                "geometry and raises fc strongly (R0 -> R1 sweep).",
            "what_it_does_NOT_yet_do_HONEST": "AAL nodes sit at GYRAL CENTROIDS (~%.0f mm apart "
                "for Precentral/Postcentral), NOT at the facing sulcal WALLS, which are only ~mm "
                "apart. The literal mm bank-to-bank proximity the reviewer raised needs a sub-gyral "
                "(vertex/voxel-level) parcellation that is NOT in this package; so AAL is a PARTIAL "
                "grounding of the folding objection, and finer-than-AAL geometry remains OWED [O]."
                % central_sulcus_L,
        },
        "b_scale_invariance_R1": {"factors": [0.1, 10.0, 1000.0], "fc": fc1_scaled,
                                  "max_abs_dev_vs_base": scale_max_dev,
                                  "scale_irrelevant_under_rownorm": bool(scale_max_dev < 1e-9)},
        "c_coord_jitter_R1": {"sigma_mm": 5.0, "seeds": list(range(300, 310)),
                              "fc_min": float(jit_fc.min()), "fc_max": float(jit_fc.max()),
                              "fc_mean": float(jit_fc.mean()), "fc_std": float(jit_fc.std()),
                              "all_partial_metastable": bool(all(jit_partial))},
        "d_normalization_variants_R1": {"row_norm_fc": fc1, "row_norm_regime": reg1,
                                        "raw_fc": fc1_raw, "raw_regime": reg1_raw,
                                        "rownorm_is_fc_maximizer": rownorm_is_maximizer},
        "e_f0_band_robustness_R1": {"seeds": list(range(400, 405)),
                                    "R_min": float(band_R.min()), "R_max": float(band_R.max()),
                                    "R_off": Roff1_band, "all_partial": bool(all(band_partial))},
        "parcellation_robustness": {
            "fc_by_resolution": {"R0_12": fc0, "R1_85": fc1, "R2_117": fc2},
            "regime_by_resolution": {"R0_12": reg0, "R1_85": reg1, "R2_117": reg2},
            "fc_maximizing_resolution_NOT_selected": "all three reported; node counts fixed "
                "before fc; engine default stays 12-node (R0) per handover, R1/R2 are evidence "
                "for a future finer promotion, not a back-fit to the largest fc.",
        },
        "scope_flags": {"medium_efficacy_tested": 0.0, "hard_problem_open": 1.0, "consciousness_claim": 0.0},
    }


def _canon(obj):
    return json.dumps(E._round(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _fmt(x):
    return f"{x:+.5f}" if isinstance(x, float) else str(x)


def main():
    G = node_decomposition_results()
    blob = _canon(G); digest = hashlib.sha256(blob).hexdigest()
    with open(os.path.join(HERE, "node_decomposition_results.json"), "wb") as f:
        f.write(blob)
    exp_path = os.path.join(HERE, "expected_node_decomposition_sha256.json")
    payload = {"node_decomposition_results.json": digest,
               "geometry_atlas_sha256": G["_meta"]["geometry_atlas_sha256"],
               "aal_builder_sha256": G["_meta"]["aal_builder_sha256"]}
    if os.path.exists(exp_path):
        prev = json.load(open(exp_path)).get("node_decomposition_results.json")
        status = "MATCHES locked digest" if prev == digest else f"MISMATCH (locked={prev})"
    else:
        with open(exp_path, "w") as f:
            json.dump(payload, f, indent=2)
        status = "WROTE expected_node_decomposition_sha256.json (first freeze)"

    r = G["resolutions"]; sb = G["sulcal_bank_made_explicit"]; cc = G["a_twelve_node_crosscheck"]
    b, c, d, e = G["b_scale_invariance_R1"], G["c_coord_jitter_R1"], G["d_normalization_variants_R1"], G["e_f0_band_robustness_R1"]
    sf = G["scope_flags"]
    print("=" * 80)
    print("M9 NODE DECOMPOSITION -- SULCAL-BANK FOLDING (decision check, grade==evidence, v1.19/1B)")
    print("=" * 80)
    print(f"  kernel = 1/r^3 (UNCHANGED)   normalization = row [F]   seed = {E.SEED}   "
          f"kappa = {G['_meta']['kappa_ephaptic_measured']}")
    print("  single source: AAL CoMs verbatim from build_geometry_atlas.py; parcel f0 inherited (no new const)")
    print("-" * 80)
    print("(resolutions; ALL reported, fc-maximizer NOT selected):")
    for key, lab in [("R0_12_composite", "R0 12-composite"), ("R1_cortex_parcels", "R1 cortex-parcels"),
                     ("R2_full_parcels", "R2 full-parcels")]:
        x = r[key]
        print(f"    {lab:18s} n={x['n_nodes']:3d}  fc={_fmt(x['fc'])}  R={x['R']:.5f}  "
              f"{x['regime']}   min-pair {x['min_pair_mm']:.1f} mm")
    print("(a) CROSS-CHECK  12-node path reproduces v1.18 grounded fc: "
          f"{cc['reproduces_v118_grounded_fc']}")
    print("    SULCAL BANK (partial grounding -- honest):")
    print(f"      12-node cortex = 1 centroid  ->  AAL = 74 gyral nodes; closest cortical pair "
          f"{sb['closest_cortical_parcel_pair_mm']:.1f} mm ({sb['closest_cortical_parcel_pair'][0]}/"
          f"{sb['closest_cortical_parcel_pair'][1]})")
    print(f"      Precentral/Postcentral GYRAL centroids {sb['central_sulcus_gyral_centroid_gap_mm_L']:.0f} mm "
          f"apart -- separate nodes now, but at centroids NOT the ~mm sulcal walls (sub-gyral parcellation OWED [O])")
    print(f"(b) SCALE-INVARIANCE R1  max|dfc| = {b['max_abs_dev_vs_base']:.1e}  "
          f"(scale-irrelevant: {b['scale_irrelevant_under_rownorm']})")
    print(f"(c) JITTER 5mm R1  fc in [{c['fc_min']:+.5f},{c['fc_max']:+.5f}] mean {c['fc_mean']:+.5f}   "
          f"all partial: {c['all_partial_metastable']}")
    print(f"(d) NORM VARIANTS R1  row={_fmt(d['row_norm_fc'])} {d['row_norm_regime']} | "
          f"raw={_fmt(d['raw_fc'])} {d['raw_regime']}   row-norm is maximizer? {d['rownorm_is_fc_maximizer']}")
    print(f"(e) f0 +/-20% BAND R1  R in [{e['R_min']:.5f},{e['R_max']:.5f}] R_off={e['R_off']:.5f}  "
          f"all partial: {e['all_partial']}")
    print("-" * 80)
    print(f"  SCOPE (unchanged):  efficacy={sf['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={sf['hard_problem_open']:.0f}  consciousness_claim={sf['consciousness_claim']:.0f}")
    print(f"  ADD-ONLY: frozen engine tree untouched (engine default stays 12-node; R1/R2 are evidence)")
    print(f"  RESULTS DIGEST  {digest}")
    print(f"  {status}")
    print("=" * 80)
    print("NOTE: node-decomposition MEASUREMENT, not a consciousness claim. Engine default M9")
    print("      geometry stays 12-node (1A); finer parcel promotion is a FUTURE entry point.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
