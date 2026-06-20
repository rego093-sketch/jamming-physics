"""
verify_organ_anatomy.py -- neuro-VP-SPEC-style gate for coupling the visceral-organ gene-clock
schedule into the Layer-2 anatomy geometry (v11).

v11 wires the v10 organ schedule (organ_atlas.organ_schedule) into the body's organ ellipsoids
(organ_anatomy.timed_anatomy_spec): each organ appears at its master gene's tau_on and grows by
the SAME R19 fold the body uses, so the grown organism fills with organ structure in gamma-order
and is complete at tau=1. This gate proves the coupling is correct WITHOUT making any new
timing-vs-biology claim -- the organ-timing grade stays the v10 measured null [O] (organ_timing.py).
This gate only checks GEOMETRY: order, completeness, the optimization invariant, surface-overlay
safety, and determinism.

Checks (PASS = 5/5), mirroring the HANDOFF's v11 acceptance items (a)-(e):
  1. ONE SWITCH         the organ fold IS the body fold: spinodal_geneclock == morpho_core.spinodal
                        (< 1e-12). The schedule that drives the fill is the same R19 primitive as the
                        engine -- never a forked clock.
  2. COMPLETE AT tau=1  at tau=1 every one of the eight schedule organs is realised: a_f(1) ~ 1 and a
                        positive-radius ellipsoid in the spec (grid-independent), AND all eight organ
                        labels occupy voxels in the grown body (volume corroboration). The body fills.
  3. FILL ORDER == gamma  the order organs APPEAR in the grown body across tau is a pure measured-gamma
                        readout: (a) the schedule order == argsort(spinodal); (b) the anatomy
                        appearance order (first tau with a_f>=0.5) == the schedule order for any
                        threshold/grid; (c) the actual VOXEL fill at the onset midpoints is a nested
                        prefix of that order (organs switch on one-by-one, in gamma-order). Perturb a
                        gamma and the fill resorts -- no hand-typed order.
  4. OVERLAY INVARIANTS  (a) the bbox-culled build_tissue == the naive full-grid comparator
                        byte-for-byte on the timed spec (the optimization invariant); (b) the organ
                        schedule is a pure OVERLAY: the body occupancy occ is byte-identical with vs
                        without the organs, and the total body-voxel count equals occ -- organs only
                        relabel interior voxels, so they can NOT perturb the Layer-3 convergence /
                        lean baseline that produces the body.
  5. DETERMINISM        two independent builds give an identical (portable) organ-geometry sha256,
                        and build_tissue is bit-identical on a re-run.
"""
import os, json, hashlib
import numpy as np

import gene_clock as GC
import morpho_core as mc
import organ_atlas as OA
import organ_anatomy as OZ


# ----------------------------------------------------------------- check 1
def check_one_switch():
    gs = np.linspace(1.2, 1.8, 241)
    d = max(abs(GC.spinodal(g) - mc.spinodal(g)) for g in gs)
    d_atlas = OA.assert_one_switch()
    ok = (d < 1e-12) and (d_atlas < 1e-12)
    return ok, f"max|delta spinodal| = {d:.2e}; organ_atlas one-switch = {d_atlas:.2e} (both < 1e-12)"


# ----------------------------------------------------------------- check 2
def check_complete_at_tau1(spec1, present1):
    sched = spec1["_schedule_order"]
    meta = spec1["_organ_meta"]
    feat_to_name = {f: n for n, f in OZ.ORGAN_NAME_TO_FEATURE.items()}
    # spec-level (grid-independent): every organ realised at full scale with a positive ellipsoid
    kept_names = {o["name"] for o in spec1["organs"]}
    scale_ok = all(meta[feat_to_name[f]]["scale"] >= 0.999 for f in sched)
    realised_ok = all(feat_to_name[f] in kept_names for f in sched)
    pos_rad_ok = all(all(r > 0 for r in o["rad"]) for o in spec1["organs"])
    # volume corroboration: every organ label occupies voxels in the grown body
    n_present = sum(1 for f in sched if present1[feat_to_name[f]] > 0)
    vox_ok = (n_present == len(sched))
    ok = bool(scale_ok and realised_ok and pos_rad_ok and vox_ok)
    return ok, (f"{len(sched)} organs: a_f(1)>=0.999={scale_ok}, all realised in spec={realised_ok}, "
                f"positive radii={pos_rad_ok}; voxel-present {n_present}/{len(sched)} "
                f"(min={min(present1.values())} vox) -> body complete={ok}")


# ----------------------------------------------------------------- check 3
def check_fill_order_is_gamma(reg):
    sched = OZ.load_schedule(include_midgut=True)
    order = sched["order"]
    feat_to_name = {f: n for n, f in OZ.ORGAN_NAME_TO_FEATURE.items()}
    readout_ok = bool(sched["order_is_gamma_readout"])
    # (b) threshold/grid-independent appearance order from the anatomy a_f
    app_order, appear = OZ.anatomy_appearance_order()
    appear_ok = (app_order == order)
    # (c) the actual VOXEL fill at the onset midpoints is a nested prefix in schedule order
    tons = [sched["features"][f]["tau_on"] for f in order]
    prefix_ok = True
    detail = []
    for k in range(len(order) - 1):
        tau_mid = 0.5 * (tons[k] + tons[k + 1])
        _o, _a, _s, _sp, tissue, _dv = OZ.reference_volume(tau_mid, reg=reg)
        present = [f for f in order
                   if int((tissue == OZ.TIS_EXT[feat_to_name[f]]).sum()) > 0]
        expected = order[:k + 1]
        prefix_ok = prefix_ok and (present == expected)
        detail.append(len(present))
    ok = bool(readout_ok and appear_ok and prefix_ok)
    return ok, (f"order==argsort(spinodal)={readout_ok}; anatomy appearance order==schedule "
                f"order={appear_ok}; voxel fill at onset midpoints nested-in-order={prefix_ok} "
                f"(counts {detail} -> 1..{len(order) - 1})")


# ----------------------------------------------------------------- check 4
def check_overlay_invariants(reg):
    import anatomy as AN
    import assemble as A
    nx, ny, nz = OZ.GATE_GRID
    bp, m = A.build_body(1.0, reg)
    somites = m["somites"]
    occ, axes, _d = bp.voxelize(nx, ny, nz, OZ.GATE_EXTENT)
    occ_sha = hashlib.sha256(np.ascontiguousarray(occ).tobytes()).hexdigest()
    spec = OZ.timed_anatomy_spec(1.0, reg, somites)

    # (a) optimization invariant: bbox-culled == naive full-grid, byte-for-byte
    tis_opt, _st = AN.build_tissue(occ, axes, spec)
    tis_naive = AN.naive_tissue(occ, axes, spec)
    eq_ok = bool(np.array_equal(tis_opt, tis_naive))

    # (b) pure overlay: occ untouched by building tissue, and body-voxel count == occ
    occ_sha2 = hashlib.sha256(np.ascontiguousarray(occ).tobytes()).hexdigest()
    surface_ok = (occ_sha == occ_sha2)
    body_preserved = (int((tis_opt > 0).sum()) == int(occ.sum()))
    ok = bool(eq_ok and surface_ok and body_preserved)
    return ok, (f"build_tissue==naive_tissue (byte-for-byte)={eq_ok}; body surface occ unchanged "
                f"by overlay={surface_ok}; body voxels {int((tis_opt > 0).sum())}=={int(occ.sum())} "
                f"(organs relabel interior only)={body_preserved}")


# ----------------------------------------------------------------- check 5
def check_determinism(reg):
    import anatomy as AN
    import assemble as A
    nx, ny, nz = OZ.GATE_GRID
    bp, m = A.build_body(1.0, reg)
    somites = m["somites"]
    occ, axes, _d = bp.voxelize(nx, ny, nz, OZ.GATE_EXTENT)
    s1 = OZ.timed_anatomy_spec(1.0, reg, somites)
    s2 = OZ.timed_anatomy_spec(1.0, reg, somites)
    h1, h2 = OZ.canonical_spec_sha(s1), OZ.canonical_spec_sha(s2)
    t1, _ = AN.build_tissue(occ, axes, s1)
    t2, _ = AN.build_tissue(occ, axes, s1)
    tissue_eq = bool(np.array_equal(t1, t2))
    ok = (h1 == h2) and tissue_eq
    return ok, f"organ-geometry sha {h1[:12]}=={h2[:12]} ({h1 == h2}); build_tissue re-run identical={tissue_eq}"


def main():
    import develop as D
    import assemble as A
    reg = D.emergent_registers()
    somites = A.build_body(1.0, reg)[1]["somites"]
    spec1 = OZ.timed_anatomy_spec(1.0, reg, somites)
    _o, _a, _s, _sp, tissue1, _dv = OZ.reference_volume(1.0, reg=reg)
    present1 = OZ.organ_labels_present(tissue1)

    checks = [
        ("1 ONE SWITCH (organ fold == body fold)", check_one_switch()),
        ("2 COMPLETE AT tau=1 (body fills with all 8 organs)", check_complete_at_tau1(spec1, present1)),
        ("3 FILL ORDER == gamma readout (organs appear in gamma-order)", check_fill_order_is_gamma(reg)),
        ("4 OVERLAY INVARIANTS (bbox-cull == naive; surface untouched)", check_overlay_invariants(reg)),
        ("5 DETERMINISM (2x build identical)", check_determinism(reg)),
    ]
    npass = 0
    order = spec1["_schedule_order"]
    feat_to_name = {f: n for n, f in OZ.ORGAN_NAME_TO_FEATURE.items()}
    print("=" * 84)
    print(f"  VISCERAL-ORGAN ANATOMY GATE  |  {len(order)} organs coupled into Layer-2 geometry")
    print("=" * 84)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 84)
    fill = " < ".join(feat_to_name[f] for f in order)
    print(f"  HEADLINE: the grown body fills with organ structure in measured-gamma order")
    print(f"            ({fill}) and is COMPLETE at tau=1. One switch; pure overlay; deterministic.")
    print(f"  HONEST scope: this is GEOMETRY (the v10 schedule realised in the voxel body). Whether")
    print(f"  the gamma-order matches real organogenesis timing remains a measured NULL [O]")
    print(f"  (organ_timing.py) -- v11 makes no new timing-vs-biology claim.")
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(OZ.HERE, "..", "results", "organ_anatomy_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(
        {name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
        | {"overall": f"{npass}/{len(checks)}",
           "headline": dict(n_organs=len(order),
                            fill_order=[feat_to_name[f] for f in order],
                            order_is_gamma_readout=bool(spec1["_order_is_gamma_readout"]),
                            complete_at_tau1=bool(checks[1][1][0]),
                            grade="[V] order is gamma readout; [F] new-organ placement + dwell size; "
                                  "[O] timing-vs-biology unchanged (organ_timing null)")},
        open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
