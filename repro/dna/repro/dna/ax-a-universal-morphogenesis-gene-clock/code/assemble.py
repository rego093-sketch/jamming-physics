"""
assemble.py -- map the emergent registers + developmental time tau onto the implicit body,
then voxelise & render.  Geometry placement/extent is driven by develop.py's emergent
registers, somite count, digit count and metamorphosis switch; the solid shapes are the
parametric canvas (the [O] tissue-mechanics is not reproduced).
"""
import math
import numpy as np
import body as B
import develop as D
import morpho_core as mc
from skimage import measure
import scipy.ndimage as ndi


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def _u_to_x(u, L):
    return -L / 2 + u * L


def _radius_profile(u, reg, L, fin_keep):
    """Body radius as a function of AP fraction u, from emergent registers."""
    he, ts = reg["head_end"], reg["tail_start"]
    R_head, R_trunk = 0.052 * L, 0.055 * L
    r = np.zeros_like(u)
    # head: a flat-ish salamander wedge -- pointed snout, broad jaw/cheek, neck pinch at he
    head = u < he
    uu = np.clip(u[head] / max(he, 1e-3), 0, 1)
    # rises from a small snout, peaks ~2/3 back (cheeks), pinches at the neck
    r[head] = R_head * (0.30 + 0.92 * np.sin(uu ** 0.72 * math.pi) ** 1.1) \
              * (1.0 - 0.18 * uu)
    # trunk: plateau with gentle taper toward tail_start
    trunk = (u >= he) & (u < ts)
    ut = (u[trunk] - he) / max(ts - he, 1e-3)
    r[trunk] = R_trunk * (1.0 - 0.14 * ut) * (0.95 + 0.05 * np.cos(ut * math.pi))
    # tail: long, slow taper to a point at u=1
    tail = u >= ts
    ux = (u[tail] - ts) / max(1 - ts, 1e-3)
    r[tail] = R_trunk * 0.80 * (1 - ux) ** 0.78 + 0.25
    return np.maximum(r, 0.2)


def limb_segments(base, out_sign, length, girth, digits, bend=0.55, back=0.20):
    """Centerline of one tetrapod limb, shared by the flesh solid and the bone placer.

    Returns (stylo, zeugo, digits_segs, wrist) where each segment is (p0,p1,r0,r1):
      stylo = humerus/femur, zeugo = radius+ulna / tibia+fibula, digits = phalange fan.
    The bone placer reuses these centerlines with a thinner radius -> bones sit *inside*
    the flesh along the same axis (no second geometry definition to drift out of sync).
    """
    bx, by, bz = base
    out = out_sign
    joint = [bx + back * length, by - 0.45 * length, bz + out * (0.55 * length)]
    wrist = [joint[0] + 0.10 * length, joint[1] - bend * length, joint[2] + out * (0.40 * length)]
    stylo = (list(base), joint, girth * 1.0, girth * 0.72)
    zeugo = (joint, wrist, girth * 0.72, girth * 0.5)
    dl = 0.42 * length
    digit_segs = []
    for k in range(digits):
        frac = (k / max(digits - 1, 1)) - 0.5            # -0.5..0.5
        tip = [wrist[0] + dl * (0.85 - 0.6 * abs(frac)) + dl * 0.2,
               wrist[1] - 0.18 * length,
               wrist[2] + out * dl * (0.25 + 0.9 * (frac + 0.5))]
        digit_segs.append((wrist, tip, girth * 0.34, girth * 0.16))
    return stylo, zeugo, digit_segs, wrist


def _add_limb(bp, base, out_sign, length, girth, digits, bend=0.55, back=0.20):
    """A bent tetrapod limb ending in a splayed autopod (digit count from the distal clock)."""
    if length < 0.6:
        return
    stylo, zeugo, digit_segs, wrist = limb_segments(base, out_sign, length, girth, digits,
                                                    bend=bend, back=back)
    bp.add_limb(stylo[0], stylo[1], stylo[2], stylo[3])
    bp.add_limb(zeugo[0], zeugo[1], zeugo[2], zeugo[3])
    bp.add_sphere(wrist, girth * 0.55)
    for (p0, p1, r0, r1) in digit_segs:
        bp.add_limb(p0, p1, r0, r1)


def build_body(tau, reg=None, blend=1.5):
    """Return (BodyPlan, metrics) for developmental time tau in [0,1]."""
    if reg is None:
        reg = D.emergent_registers()
    L = 18 + 72 * (tau ** 0.7)                       # axial elongation over time
    limb_on, fin_keep = D.metamorph_state(tau)
    somites, s0, period = D.somite_count(L * 0.9)

    # per-limb autopod lengths -> distal clock -> digit counts (fore 4 / hind 5 emerge)
    fore_len = (0.16 * L) * 1.00 * limb_on
    hind_len = (0.16 * L) * 1.12 * limb_on
    digits_fore, _ = D.digit_count(0.42 * max(fore_len, 1.4))
    digits_hind, _ = D.digit_count(0.42 * max(hind_len, 1.4))

    bp = B.BodyPlan(blend=blend)
    # ---- axial tube from emergent radius profile
    nst = 46
    us = np.linspace(0.0, 1.0, nst)
    rr = _radius_profile(us, reg, L, fin_keep)
    # near-straight axis with only a faint head lift so the snout clears the ground
    yc = np.where(us < reg["head_end"],
                  0.025 * L * np.sin(us / max(reg["head_end"], 1e-3) * math.pi), 0.0)
    stations = [(float(_u_to_x(u, L)), float(yc[i]), float(rr[i])) for i, u in enumerate(us)]
    bp.add_axis(stations)

    # ---- head detail: eyes set on top-sides of the skull + (larval) external gills
    he = reg["head_end"]
    eye_u = he * 0.60
    ex = _u_to_x(eye_u, L); eye_r = 0.026 * L
    hr = _radius_profile(np.array([eye_u]), reg, L, fin_keep)[0]
    ey = 0.55 * hr + 0.025 * L                       # sit on top of the head
    ez = hr * 0.62
    bp.add_sphere([ex, ey, ez], eye_r)
    bp.add_sphere([ex, ey, -ez], eye_r)
    # snout: small rounded tip on the axis (no downward offset)
    bp.add_sphere([_u_to_x(0.015, L), 0.0, 0.0], 0.022 * L)
    gill = max(0.0, fin_keep - 0.35) * (1 - limb_on)
    if gill > 0.05:
        gx = _u_to_x(he * 0.95, L)
        gr = _radius_profile(np.array([he * 0.95]), reg, L, fin_keep)[0]
        for s in (+1, -1):
            for j in range(3):
                bp.add_sphere([gx + j * 0.012 * L, 0.03 * L + j * 0.01 * L, s * (gr + 0.02 * L)],
                              (0.018 + 0.004 * j) * L * gill)

    # ---- tail fin (dorsal + ventral blades), height scales with fin_keep
    ts = reg["tail_start"]
    if fin_keep > 0.05:
        x0 = _u_to_x(max(ts - 0.05, 0.4), L); x1 = _u_to_x(0.995, L)
        fh = 0.075 * L * fin_keep
        bp.add_blade(x0, x1, top=fh, bottom=-fh, thick=0.5)

    # ---- four limbs at emergent fore/hind stations, length from metamorphosis switch
    for u_lab, scale, ndig in ((reg["forelimb"], 1.0, digits_fore),
                               (reg["hindlimb"], 1.12, digits_hind)):
        bx = _u_to_x(u_lab, L)
        br = _radius_profile(np.array([u_lab]), reg, L, fin_keep)[0]
        Llimb = (0.16 * L) * scale * limb_on
        for s in (+1, -1):
            _add_limb(bp, [bx, -0.25 * br, s * br * 0.85], s, Llimb,
                      girth=0.030 * L * (0.7 + 0.3 * scale), digits=ndig)

    metrics = dict(tau=round(tau, 4), axis_len=round(L, 3), somites=somites,
                   somite_len=round(s0, 4), clock_period=round(period, 4),
                   digits_fore=digits_fore, digits_hind=digits_hind,
                   limb_extension=round(limb_on, 4),
                   fin_kept=round(fin_keep, 4),
                   registers={k: round(v, 4) for k, v in reg.items()})
    return bp, metrics


def voxelize_and_mesh(bp, nx, ny, nz, extent, smooth=0.8, head_flatten=None):
    occ, axes, d = bp.voxelize(nx, ny, nz, extent)
    if head_flatten is not None:
        # squash the body dorsoventrally toward the head so the skull is flat, not a ball.
        xs, ys, zs = axes
        x_he, strength = head_flatten           # AP x where flattening fades out, max squash
        X = xs[:, None, None]; Y = ys[None, :, None]
        w = np.clip((x_he - X) / (x_he - xs[0] + 1e-6), 0, 1)   # 1 at snout -> 0 at neck
        keep = (np.abs(Y) <= (1.0 - strength * w) * np.abs(ys).max()) | (np.abs(Y) < 1e-9)
        occ = occ & np.broadcast_to(keep, occ.shape)
    sm = ndi.gaussian_filter(occ.astype(np.float32), smooth)
    if sm.max() < 0.5:
        return occ, None, None, axes
    verts, faces, normals, _ = measure.marching_cubes(sm, level=0.5)
    xs, ys, zs = axes
    verts_m = np.stack([np.interp(verts[:, 0], np.arange(len(xs)), xs),
                        np.interp(verts[:, 1], np.arange(len(ys)), ys),
                        np.interp(verts[:, 2], np.arange(len(zs)), zs)], axis=1)
    return occ, verts_m, normals, axes


# ============================================================================
#  anatomy spec -- bones + organs derived from the SAME emergent registers.
#  The vertebral column has ONE vertebra per somite, so the skeleton's
#  segment count IS the segmentation-clock count (the on-thesis link).
# ============================================================================
# tissue label ids (shared with anatomy.py)
TIS = {"void": 0, "flesh": 1, "bone": 2, "heart": 3, "lung": 4, "liver": 5, "gut": 6,
       "eye": 7, "muscle": 8, "skin": 9}


def anatomy_spec(tau, reg, somites):
    """Return dict of skeletal centerlines + organ ellipsoids in model coords.

    Everything is sized from the emergent registers + the somite count, so no new
    free pattern is introduced: bones and organ placement inherit the switch decisions.
    """
    L = 18 + 72 * (tau ** 0.7)
    limb_on, fin_keep = D.metamorph_state(tau)
    he, ts = reg["head_end"], reg["tail_start"]
    x_of = lambda u: _u_to_x(u, L)
    r_of = lambda u: float(_radius_profile(np.array([u]), reg, L, fin_keep)[0])

    spec = dict(L=L, limb_on=limb_on)

    # ---- vertebral column: a central rod + one centrum per somite (= clock count) ----
    spine_x0, spine_x1 = x_of(he * 0.55), x_of(0.992)     # skull base -> tail tip
    n_vert = max(1, somites)                               # ONE vertebra per somite
    vx = np.linspace(spine_x0, spine_x1, n_vert)
    # vertebra radius tracks the local body radius (bigger in trunk, taper in tail)
    vu = np.clip((vx + L / 2) / L, 0, 1)
    vr = np.array([r_of(u) for u in vu])
    spec["spine_rod"] = (spine_x0, spine_x1, 0.16)         # thin neural rod radius (model)
    # centrum radius: a healthy fraction of the local body radius; bigger share in the tail
    spec["vertebrae"] = [(float(x), 0.0, float(0.46 * max(rr, 0.6)))
                         for x, rr in zip(vx, vr)]          # (x, y, centrum radius)

    # ---- ribs: from trunk vertebrae, curving ventro-laterally around the cavity ----
    ribs = []
    for x, _, rr in spec["vertebrae"]:
        u = (x + L / 2) / L
        if he < u < ts:                                    # only the trunk bears ribs
            R = r_of(u)
            ribs.append((float(x), float(0.92 * R), 0.11)) # (x, arc radius, rib thickness)
    spec["ribs"] = ribs

    # ---- skull: a flattened ellipsoid filling the head register ----
    hx = x_of(he * 0.5)
    spec["skull"] = (float(hx), 0.0, 0.0,
                     float(0.55 * he * L), float(0.55 * r_of(he * 0.5)), float(0.85 * r_of(he * 0.5)))

    # ---- limb bones: reuse the flesh centerline, thinner radius (bone inside flesh) ----
    spec["limb_bones"] = []
    if limb_on > 0.05:
        for u_lab, scale in ((reg["forelimb"], 1.0), (reg["hindlimb"], 1.12)):
            bx = x_of(u_lab); br = r_of(u_lab)
            Llimb = (0.16 * L) * scale * limb_on
            girth = 0.030 * L * (0.7 + 0.3 * scale)
            ndig = 4 if scale < 1.05 else 5
            for s in (+1, -1):
                stylo, zeugo, digits, wrist = limb_segments(
                    [bx, -0.25 * br, s * br * 0.85], s, Llimb, girth, ndig)
                # bone = ~42% of the flesh girth, along the same centerline
                for seg in (stylo, zeugo):
                    p0, p1, r0, r1 = seg
                    spec["limb_bones"].append((p0, p1, 0.42 * r0, 0.42 * r1))
                for (p0, p1, r0, r1) in digits:
                    spec["limb_bones"].append((p0, p1, 0.5 * r0, 0.5 * r1))

    # ---- organs: ellipsoids tiling the trunk cavity (rough viscera, mostly filling it) ----
    # each is short along x (absolute half-length) and wide in y,z (~fills the local
    # cross-section), placed at successive AP stations so the cavity is mostly occupied.
    trunk_mid = 0.5 * (he + ts)
    organs = []
    # heart: small, ventral, just behind the head
    uh = he + 0.045
    organs.append(dict(label=TIS["heart"], name="heart",
                       c=(float(x_of(uh)), float(-0.22 * r_of(uh)), 0.0),
                       rad=(0.040 * L, 0.50 * r_of(uh), 0.50 * r_of(uh))))
    # paired lungs: dorso-lateral, anterior trunk
    ul = he + 0.095
    for s in (+1, -1):
        organs.append(dict(label=TIS["lung"], name="lung",
                           c=(float(x_of(ul)), float(0.26 * r_of(ul)), float(s * 0.42 * r_of(ul))),
                           rad=(0.060 * L, 0.62 * r_of(ul), 0.46 * r_of(ul))))
    # liver: large, fills mid-anterior cross-section, long enough to meet the gut
    uv = he + 0.165
    organs.append(dict(label=TIS["liver"], name="liver",
                       c=(float(x_of(uv)), float(-0.04 * r_of(uv)), 0.0),
                       rad=(0.060 * L, 0.92 * r_of(uv), 0.94 * r_of(uv))))
    # gut: large, fills the rest of the trunk back to the pelvis
    ug = trunk_mid + 0.095
    organs.append(dict(label=TIS["gut"], name="gut",
                       c=(float(x_of(ug)), float(-0.02 * r_of(ug)), 0.0),
                       rad=(0.090 * L, 0.92 * r_of(ug), 0.94 * r_of(ug))))
    spec["organs"] = organs
    return spec
