"""
organ_anatomy.py -- couple the v10 visceral-organ gene-clock SCHEDULE into the Layer-2
ANATOMY geometry (v11).

v10 produced, per visceral organ, a deterministic emergence schedule (tau_on, dwell, a_f(tau))
whose ORDER is a pure measured-gamma readout (organ_atlas.organ_schedule). But that schedule was
NOT yet wired into the actual body: assemble.anatomy_spec still placed only four organ ellipsoids
(heart / lung / liver / gut) by anatomical spec, fully present at every tau, with no link to the
clock. So "organs appear in gamma-order IN THE GROWN BODY" was true only of the schedule, never
demonstrated in the voxel volume (the v10 HANDOFF's "biggest gap").

v11 closes exactly that gap, as GEOMETRY (NOT a new timing-vs-biology claim):

  * Each of the EIGHT schedule organs is given an ellipsoid in the trunk cavity (the four that
    already existed -- heart/lung/liver/gut == midgut -- plus four NEW ones: stomach, pancreas,
    kidney, spleen). The four new placements are anatomical [F] choices sized from the local body
    radius (no number is tuned to hit a target).
  * Every organ ellipsoid is gated by its OWN master gene's emergence curve a_f(tau) (the SAME R19
    fold the body uses): it is ABSENT before its tau_on and grows in afterwards, and its relative
    final prominence is scaled by the gene's measured DWELL. As developmental time tau advances the
    grown organism therefore FILLS WITH ORGAN STRUCTURE IN GAMMA-ORDER, and at tau=1 every organ is
    realised (the body is complete).

ADD-ONLY / NO-ENGINE-EDIT.  This module does not modify assemble.py, anatomy.py, body.py,
gene_clock.py, morpho_core.py or organism/core.py. It IMPORTS them unchanged and overlays the
gene-clock time-gate on top of assemble.anatomy_spec. The body surface (occ) and the Layer-3
convergence proof are therefore untouched -- organs are a label OVERLAY that can never perturb the
morphogenesis that produces the body (verify_organ_anatomy check 4 enforces this).

WHAT THIS MODULE CLAIMS (and does not):
  * [V] the ORDER in which organs appear in the grown body across tau == the schedule order ==
        argsort(spinodal(gamma)); perturb a gamma and the fill order resorts. (One switch: the
        organ fold IS the body fold, asserted < 1e-12.)
  * [F] the gene->organ map, the sign convention (higher spinodal -> later), the absolute tau
        window, and the FOUR new organs' 3-D placements + the dwell-weighted relative final size:
        forced modelling choices, documented, never fitted.
  * [O] whether this gamma-derived order MATCHES real organogenesis timing is NOT asserted here --
        it was TESTED in organ_timing.py against locked Carnegie stages and is a measured NULL
        (promoter stiffness does not predict organ timing). v11 changes nothing about that grade;
        it only realises the deterministic schedule as geometry. Absolute organ sizes/shapes are a
        crude parametric canvas, NOT a claim about real organ volumes.

stdlib + numpy (+ the package's own assemble/anatomy for voxelisation). Deterministic.
"""
import os, json, hashlib
import numpy as np

import assemble as A
import anatomy as AN
import develop as D
import gene_clock as GC
import organ_atlas as OA

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------------------------
# Extended tissue labels.  The base TIS (assemble.py) stops at eye=7/muscle=8/skin=9; the four
# NEW visceral organs get fresh ids so they are distinguishable in the volume.  We extend a LOCAL
# copy -- assemble.TIS itself is left byte-for-byte unchanged (add-only).
# --------------------------------------------------------------------------------------------
TIS_EXT = dict(A.TIS)
TIS_EXT.update({"stomach": 10, "pancreas": 11, "kidney": 12, "spleen": 13})
NAME_EXT = {v: k for k, v in TIS_EXT.items()}

# colours for the four new organs (extends anatomy.ORGAN_COLORS for the optional figure only)
ORGAN_COLORS_EXT = dict(AN.ORGAN_COLORS)
ORGAN_COLORS_EXT.update({
    10: (0.74, 0.55, 0.42),   # stomach (tan)
    11: (0.90, 0.82, 0.45),   # pancreas (sandy yellow)
    12: (0.62, 0.30, 0.42),   # kidney (maroon)
    13: (0.55, 0.30, 0.55),   # spleen (plum)
})

# Map each anatomy organ NAME to its schedule organ_feature (organ_atlas.ORGAN_MASTERS).
# The existing four anatomy organs map onto four of the schedule masters; the existing "gut"
# ellipsoid carries the midgut/intestine master (CDX2). The four new names map onto the rest.
ORGAN_NAME_TO_FEATURE = {
    "heart":    "heart_tube",            # NKX2-5
    "lung":     "lung_bud",              # NKX2-1
    "liver":    "hepatic_diverticulum",  # HHEX
    "gut":      "midgut_intestine",      # CDX2 (the existing posterior-gut ellipsoid)
    "stomach":  "gastric_dilation",      # BARX1  (new)
    "pancreas": "dorsal_pancreatic_bud", # PDX1   (new)
    "kidney":   "metanephric_cap",       # SIX2   (new)
    "spleen":   "splenic_primordium",    # TLX1   (new)
}

# the gene-clock onset slope used for the body-feature schedule (gene_clock.feature_schedule
# default); reused verbatim so the organ a_f(tau) is the SAME clock, not a second one.
ONSET_SLOPE = 14.0
# below this a_f the organ is treated as ABSENT (it has not switched on yet) and is dropped from
# the spec so it writes no voxels. The R19 onset is a near-step, so any small value in (0, 0.5)
# selects the same appearance tau (the choice is not a tuned knob -- see verify check 3).
OFF_EPS = 1e-2

# reference grid for the gate's voxel checks (the body extent is assemble/anatomy_figure's).
# Coarse enough to be fast, fine enough that all eight organs resolve to tens of voxels.
GATE_EXTENT = (120.0, 46.0, 50.0)
GATE_GRID = (140, 66, 72)


# --------------------------------------------------------------------------------------------
def load_schedule(include_midgut=True):
    """The v10 gene-clock visceral-organ schedule (pure measured-gamma readout)."""
    return OA.organ_schedule(include_midgut=include_midgut)


def dwell_weights(sched):
    """Relative final-size weight per organ feature: measured dwell normalised to max == 1.
    A gene-clock readout (dwell ~ gamma^1.5); used as a gentle [F] relative-prominence factor."""
    dw = {o: sched["features"][o]["dwell"] for o in sched["order"]}
    wmax = max(dw.values())
    return {o: dw[o] / wmax for o in dw}


def organ_scale(feature, tau, sched, slope=ONSET_SLOPE):
    """a_f(tau) in [0,1] for one organ's master gene -- the SAME emergence curve the body uses.
    ~0 (clipped to eps) before the gene's tau_on, a sharp R19 onset at tau_on, ~1 by tau=1."""
    d = sched["features"][feature]
    return float(GC.emergence_curve(d["gamma"], [tau], d["tau_on"], slope=slope)[0])


# --------------------------------------------------------------------------------------------
def new_visceral_organs(tau, reg):
    """The FOUR new visceral-organ ellipsoids (stomach, kidney x2, pancreas, spleen) at their
    UNGATED anatomical base size, sized from the local body radius (no tuned constants).

    Order matters for label priority: the small/peripheral organs (pancreas, then spleen) are
    LAST so the central viscera do not overwrite them on overlap. (Label priority does not affect
    the build_tissue == naive_tissue invariant -- both iterate this same list in the same order.)
    All placements are [F] (a crude parametric viscera canvas, not a real-anatomy claim).
    """
    L = 18.0 + 72.0 * (tau ** 0.7)
    _, fin_keep = D.metamorph_state(tau)
    he, ts = reg["head_end"], reg["tail_start"]
    x_of = lambda u: A._u_to_x(u, L)
    r_of = lambda u: float(A._radius_profile(np.array([u]), reg, L, fin_keep)[0])
    trunk_mid = 0.5 * (he + ts)

    O = []
    # stomach (BARX1): left, ventro-lateral, anterior-mid abdomen
    ust = he + 0.150
    O.append(dict(label=TIS_EXT["stomach"], name="stomach",
                  c=(float(x_of(ust)), float(-0.05 * r_of(ust)), float(+0.34 * r_of(ust))),
                  rad=(0.055 * L, 0.50 * r_of(ust), 0.44 * r_of(ust))))
    # kidneys (SIX2): paired, retroperitoneal, dorsal, posterior-mid trunk; bean (elongate-x)
    uk = trunk_mid + 0.02
    for s in (+1, -1):
        O.append(dict(label=TIS_EXT["kidney"], name="kidney",
                      c=(float(x_of(uk)), float(0.34 * r_of(uk)), float(s * 0.50 * r_of(uk))),
                      rad=(0.075 * L, 0.40 * r_of(uk), 0.30 * r_of(uk))))
    # pancreas (PDX1): dorsal-central, transverse (elongate-x), retroperitoneal; painted late
    up = he + 0.185
    O.append(dict(label=TIS_EXT["pancreas"], name="pancreas",
                  c=(float(x_of(up)), float(0.22 * r_of(up)), 0.0),
                  rad=(0.090 * L, 0.30 * r_of(up), 0.70 * r_of(up))))
    # spleen (TLX1): left dorsal apex pocket (dorsal mesogastrium); painted LAST so it survives
    us = he + 0.128
    O.append(dict(label=TIS_EXT["spleen"], name="spleen",
                  c=(float(x_of(us)), float(0.42 * r_of(us)), float(+0.30 * r_of(us))),
                  rad=(0.060 * L, 0.46 * r_of(us), 0.42 * r_of(us))))
    return O


def timed_anatomy_spec(tau, reg, somites, slope=ONSET_SLOPE, off_eps=OFF_EPS):
    """assemble.anatomy_spec + the eight-organ gene-clock time-gate.

    Starts from the UNMODIFIED assemble.anatomy_spec (bones + the original four organs), appends
    the four new visceral organs, then multiplies EVERY organ's radii by

        scale = a_f(tau ; gamma, tau_on)   (the R19 onset: absent before tau_on, ~1 by tau=1)
        x  w  = dwell(gamma)/max(dwell)    (gentle [F] relative-prominence weight)

    Organs whose a_f < off_eps (not yet switched on) are DROPPED (they write nothing). The bones,
    skull, ribs, vertebrae and limb bones are passed through unchanged. Returns the spec dict with
    the gated organ list plus per-organ metadata and the schedule order/readout flag.
    """
    sched = load_schedule(include_midgut=True)
    w = dwell_weights(sched)

    spec = A.anatomy_spec(tau, reg, somites)            # bones + original 4 organs (UNCHANGED)
    base_organs = list(spec["organs"]) + new_visceral_organs(tau, reg)

    kept, meta = [], {}
    for o in base_organs:
        feat = ORGAN_NAME_TO_FEATURE[o["name"]]
        d = sched["features"][feat]
        s = organ_scale(feat, tau, sched, slope=slope)
        wi = w[feat]
        present = bool(s >= off_eps)
        meta[o["name"]] = dict(feature=feat, gene=d["gene"], gamma=d["gamma"],
                               tau_on=d["tau_on"], dwell=d["dwell"], weight=wi,
                               scale=s, present=present)
        if not present:
            continue
        og = dict(o)
        og["rad"] = tuple(float(r * s * wi) for r in o["rad"])
        kept.append(og)

    spec["organs"] = kept
    spec["_schedule_order"] = sched["order"]
    spec["_order_is_gamma_readout"] = sched["order_is_gamma_readout"]
    spec["_organ_meta"] = meta
    spec["_tau"] = float(tau)
    return spec


# --------------------------------------------------------------------------------------------
def anatomy_appearance_order(taus=None, slope=ONSET_SLOPE, threshold=0.5):
    """The order in which organs first reach scale a_f >= threshold as tau advances.

    This is the order organs APPEAR in the grown body. Because every a_f shares the same slope and
    its R19 onset is a near-step centred at the gene's tau_on, the crossing tau is monotone in
    tau_on for any threshold in (0,1) -- so the appearance order equals argsort(tau_on) == the
    schedule order (a pure gamma readout), independent of the tau grid or the threshold.

    Returns (ordered_feature_list, {feature: appearance_tau}).
    """
    sched = load_schedule(include_midgut=True)
    if taus is None:
        taus = np.linspace(0.0, 1.0, 401)
    order_ref = sched["order"]
    appear = {}
    for feat in order_ref:
        a = np.array([organ_scale(feat, float(t), sched, slope=slope) for t in taus])
        idx = int(np.argmax(a >= threshold))
        appear[feat] = float(taus[idx]) if a[idx] >= threshold else 1.0
    ordered = sorted(order_ref, key=lambda f: (appear[f], order_ref.index(f)))
    return ordered, appear


def reference_volume(tau, reg=None, grid=GATE_GRID, extent=GATE_EXTENT,
                     slope=ONSET_SLOPE, off_eps=OFF_EPS):
    """Build body -> voxelise -> timed spec -> bbox-culled tissue, at the reference grid.
    Returns (occ, axes, somites, spec, tissue, dvox)."""
    if reg is None:
        reg = D.emergent_registers()
    nx, ny, nz = grid
    bp, m = A.build_body(tau, reg)
    somites = m["somites"]
    occ, axes, _d = bp.voxelize(nx, ny, nz, extent)
    spec = timed_anatomy_spec(tau, reg, somites, slope=slope, off_eps=off_eps)
    tissue, _stats = AN.build_tissue(occ, axes, spec)
    dvox = (extent[0] / nx) * (extent[1] / ny) * (extent[2] / nz)
    return occ, axes, somites, spec, tissue, dvox


def organ_labels_present(tissue, labels=None):
    """Which visceral-organ labels actually occupy voxels in `tissue`."""
    if labels is None:
        labels = [TIS_EXT[k] for k in ("heart", "lung", "liver", "gut",
                                       "stomach", "pancreas", "kidney", "spleen")]
    return {NAME_EXT[l]: int((tissue == l).sum()) for l in labels}


def canonical_spec_sha(spec):
    """Environment-independent sha256 of the organ geometry (sorted, rounded). Pure arithmetic
    over the frozen gamma table + fixed placement -> portable + deterministic."""
    rows = sorted(
        [(o["name"], int(o["label"]),
          tuple(round(float(c), 6) for c in o["c"]),
          tuple(round(float(r), 6) for r in o["rad"])) for o in spec["organs"]]
    )
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


# --------------------------------------------------------------------------------------------
def _fmt():
    reg = D.emergent_registers()
    sched = load_schedule(include_midgut=True)
    order = sched["order"]
    feat_to_name = {f: n for n, f in ORGAN_NAME_TO_FEATURE.items()}

    spec1 = timed_anatomy_spec(1.0, reg, A.build_body(1.0, reg)[1]["somites"])
    meta = spec1["_organ_meta"]

    L = ["=" * 92,
         "  VISCERAL-ORGAN ANATOMY  |  v10 gene-clock schedule COUPLED into Layer-2 geometry (v11)",
         "=" * 92,
         f"  {'organ (anat)':12s} {'gene':7s} {'feature':22s} {'tau_on':>7s} {'dwell':>7s}"
         f" {'w':>6s} {'a_f(1)':>7s}"]
    for feat in order:
        name = feat_to_name[feat]
        m = meta[name]
        L.append(f"  {name:12s} {m['gene']:7s} {feat:22s} {m['tau_on']:7.4f} {m['dwell']:7.4f}"
                 f" {m['weight']:6.3f} {m['scale']:7.4f}")
    L.append("-" * 92)
    L.append("  DNA-derived fill order in the grown body (earliest -> latest appearance):")
    L.append("    " + " < ".join(feat_to_name[f] for f in order))
    app_order, appear = anatomy_appearance_order()
    L.append(f"  anatomy appearance order == schedule order : {app_order == order}")
    L.append(f"  order_is_gamma_readout (order == argsort spinodal) : {sched['order_is_gamma_readout']}")
    L.append(f"  one-switch (organ fold == body fold) max|delta|    : {OA.assert_one_switch():.2e}")

    # gamma-ordered fill of the actual voxel volume, at a few tau checkpoints
    L.append("-" * 92)
    L.append("  gamma-ordered fill of the VOXEL body (organs present vs tau):")
    for tau in (0.15, 0.30, 0.45, 0.65, 0.72, 0.90, 1.00):
        _occ, _ax, _som, _sp, tissue, _dv = reference_volume(tau, reg=reg)
        present = [feat_to_name[f] for f in order
                   if int((tissue == TIS_EXT[feat_to_name[f]]).sum()) > 0]
        L.append(f"    tau={tau:.2f} ({len(present)}/8): " + ", ".join(present))
    L.append("=" * 92)
    L.append("  NOTE: this is GEOMETRY. Whether the gamma-order matches real organogenesis timing")
    L.append("        is a measured NULL (organ_timing.py); v11 asserts only that the grown body")
    L.append("        fills with organs in gamma-order and is complete at tau=1.")
    return "\n".join(L)


if __name__ == "__main__":
    print(_fmt())
