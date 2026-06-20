"""
anatomy.py -- fill the body with rough BONES + ORGANS as a tissue-label volume,
and prove the optimization that stops the added volume from exploding the cost.

The expensive thing in "fill the whole body with structure" is touching voxels. Two
moves keep it cheap:
  (1) a uint8 LABEL volume (not a float64 SDF per part): 8x less memory/bandwidth, and
      boolean region tests instead of sqrt-heavy distance fields.
  (2) per-part BOUNDING-BOX CULLING: each bone/organ writes only its own neighbourhood,
      so total work ~ sum(part bbox volumes), which for many small parts (50+ vertebrae,
      ribs, phalanges) is far below parts x grid. More, smaller parts make this *better*.

`naive_tissue` is the un-culled version (every part scanned over the whole grid) kept
ONLY to measure the speedup honestly.

tissue ids:  0 void · 1 flesh · 2 bone · 3 heart · 4 lung · 5 liver · 6 gut · 7 eye
"""
import numpy as np
import scipy.ndimage as ndi
from assemble import TIS

BONE = TIS["bone"]
ORGAN_COLORS = {
    0: (1.00, 1.00, 1.00), 1: (0.86, 0.62, 0.52), 2: (0.95, 0.94, 0.86),
    3: (0.82, 0.22, 0.24), 4: (0.55, 0.66, 0.85), 5: (0.55, 0.36, 0.30),
    6: (0.80, 0.70, 0.40), 7: (0.10, 0.10, 0.12),
    8: (0.78, 0.40, 0.40), 9: (0.92, 0.80, 0.70),
}
TIS_NAME = {v: k for k, v in TIS.items()}


# ---------------------------------------------------------------- fast region tests
def _idx(xs, lo, hi):
    i0 = max(0, int(np.searchsorted(xs, lo) - 1))
    i1 = min(len(xs), int(np.searchsorted(xs, hi) + 1))
    return i0, i1


def _subgrid(axes, lo, hi):
    xs, ys, zs = axes
    a0, a1 = _idx(xs, lo[0], hi[0]); b0, b1 = _idx(ys, lo[1], hi[1]); c0, c1 = _idx(zs, lo[2], hi[2])
    if a0 >= a1 or b0 >= b1 or c0 >= c1:
        return None
    X, Y, Z = np.meshgrid(xs[a0:a1], ys[b0:b1], zs[c0:c1], indexing="ij")
    return (a0, a1, b0, b1, c0, c1), np.stack([X, Y, Z], -1)


def _ellip(P, c, rad):
    q = (P - np.asarray(c, float)) / np.maximum(np.asarray(rad, float), 1e-6)
    return np.einsum("...k,...k->...", q, q) <= 1.0


def _capsule(P, a, b, ra, rb):
    a = np.asarray(a, float); b = np.asarray(b, float); ba = b - a
    l2 = float(ba @ ba) + 1e-9
    pa = P - a
    t = np.clip(np.einsum("...k,k->...", pa, ba) / l2, 0.0, 1.0)
    proj = a + t[..., None] * ba
    d2 = np.einsum("...k,...k->...", P - proj, P - proj)
    r = ra + t * (rb - ra)
    return d2 <= r * r


# ------------------------------------------------------------- optimized builder
def build_tissue(occ, axes, spec, erode=1):
    """Label every interior voxel as flesh, carve organs, then overlay bone.
    bbox-culled + boolean: cost ~ sum(part bbox volumes). Returns (tissue uint8, stats)."""
    xs, ys, zs = axes
    tissue = occ.astype(np.uint8)                       # 1 = flesh inside, 0 = void
    interior = ndi.binary_erosion(occ, iterations=erode) if erode else occ
    touched = 0

    def paint(lo, hi, mask_fn, label, restrict=None, clip_body=True):
        nonlocal touched
        s = _subgrid(axes, lo, hi)
        if s is None:
            return
        (a0, a1, b0, b1, c0, c1), P = s
        touched += P.shape[0] * P.shape[1] * P.shape[2]
        m = mask_fn(P)
        if clip_body:
            m &= occ[a0:a1, b0:b1, c0:c1]
        if restrict is not None:
            m &= restrict[a0:a1, b0:b1, c0:c1]
        tissue[a0:a1, b0:b1, c0:c1][m] = label

    # ---- ORGANS (sit under the skin: restrict to eroded interior; don't overwrite bone) ----
    for o in spec["organs"]:
        c, rad = o["c"], o["rad"]
        lo = [c[i] - rad[i] for i in range(3)]; hi = [c[i] + rad[i] for i in range(3)]
        paint(lo, hi, lambda P, c=c, rad=rad: _ellip(P, c, rad), o["label"], restrict=interior)

    # ---- SKELETON (overlays everything; label BONE) ----
    # vertebral rod
    x0, x1, rr = spec["spine_rod"]
    paint([x0, -rr, -rr], [x1, rr, rr],
          lambda P, a=(x0, 0, 0), b=(x1, 0, 0), r=rr: _capsule(P, a, b, r, r), BONE)
    # vertebrae (one per somite)
    for (x, y, r) in spec["vertebrae"]:
        paint([x - r, y - r, -r], [x + r, y + r, r],
              lambda P, c=(x, y, 0.0), rad=(r, r, r): _ellip(P, c, rad), BONE)
    # ribs: ventro-lateral C-arc hugging the body wall in the trunk
    for (x, Rarc, th) in spec["ribs"]:
        def rib_mask(P, x=x, Rarc=Rarc, th=th):
            near_x = np.abs(P[..., 0] - x) <= th
            rad = np.sqrt(P[..., 1] ** 2 + P[..., 2] ** 2)
            shell = np.abs(rad - Rarc) <= th
            lower = P[..., 1] <= 0.45 * Rarc                # open dorsally (a C, not an O)
            return near_x & shell & lower
        paint([x - th, -Rarc - th, -Rarc - th], [x + th, 0.5 * Rarc + th, Rarc + th], rib_mask, BONE)
    # skull: cranial vault = bone shell in the head ellipsoid
    sx, sy, sz, rx, ry, rz = spec["skull"]
    paint([sx - rx, sy - ry, sz - rz], [sx + rx, sy + ry, sz + rz],
          lambda P, c=(sx, sy, sz), rad=(rx, ry, rz):
              _ellip(P, c, rad) & ~_ellip(P, c, (0.62 * rx, 0.62 * ry, 0.62 * rz)), BONE)
    # limb bones (capsules along the flesh centerline)
    for (p0, p1, r0, r1) in spec["limb_bones"]:
        lo = [min(p0[i], p1[i]) - max(r0, r1) for i in range(3)]
        hi = [max(p0[i], p1[i]) + max(r0, r1) for i in range(3)]
        paint(lo, hi, lambda P, a=p0, b=p1, ra=r0, rb=r1: _capsule(P, a, b, ra, rb), BONE)

    n_parts = (1 + len(spec["vertebrae"]) + len(spec["ribs"]) + 1 + len(spec["limb_bones"])
               + len(spec["organs"]))

    # ---- differentiate the leftover flesh: interior -> axial MUSCLE (segmented into
    #      myomeres by the SAME somite clock), the 1-voxel shell -> SKIN. Now every
    #      body voxel carries a tissue (the volume is fully occupied, not vague filler).
    still_flesh = (tissue == TIS["flesh"])
    tissue[still_flesh & interior] = TIS["muscle"]
    tissue[still_flesh & ~interior] = TIS["skin"]

    stats = dict(parts=n_parts, voxels_touched=int(touched), grid_voxels=int(occ.size),
                 naive_voxels=int(n_parts * occ.size))
    return tissue, stats


# ------------------------------------------------------------- naive builder (for timing only)
def naive_tissue(occ, axes, spec, erode=1):
    """Same result, but every part is scanned over the WHOLE grid (no bbox cull, full
    coordinate arrays each time). Kept only to measure how much the culling saves."""
    xs, ys, zs = axes
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    P = np.stack([X, Y, Z], -1)
    tissue = occ.astype(np.uint8)
    interior = ndi.binary_erosion(occ, iterations=erode) if erode else occ
    for o in spec["organs"]:
        m = _ellip(P, o["c"], o["rad"]) & interior
        tissue[m] = o["label"]
    x0, x1, rr = spec["spine_rod"]
    tissue[_capsule(P, (x0, 0, 0), (x1, 0, 0), rr, rr) & occ] = BONE
    for (x, y, r) in spec["vertebrae"]:
        tissue[_ellip(P, (x, y, 0.0), (r, r, r)) & occ] = BONE
    for (x, Rarc, th) in spec["ribs"]:
        rad = np.sqrt(P[..., 1] ** 2 + P[..., 2] ** 2)
        m = (np.abs(P[..., 0] - x) <= th) & (np.abs(rad - Rarc) <= th) & (P[..., 1] <= 0.45 * Rarc)
        tissue[m & occ] = BONE
    sx, sy, sz, rx, ry, rz = spec["skull"]
    m = _ellip(P, (sx, sy, sz), (rx, ry, rz)) & ~_ellip(P, (sx, sy, sz), (0.62 * rx, 0.62 * ry, 0.62 * rz))
    tissue[m & occ] = BONE
    for (p0, p1, r0, r1) in spec["limb_bones"]:
        tissue[_capsule(P, p0, p1, r0, r1) & occ] = BONE
    # identical final differentiation as the optimized path
    still = (tissue == TIS["flesh"])
    tissue[still & interior] = TIS["muscle"]
    tissue[still & ~interior] = TIS["skin"]
    return tissue


# ------------------------------------------------------------- volume accounting
def volume_report(tissue, dvox):
    """Per-tissue volume (model^3) and fraction of body. dvox = voxel volume."""
    body = int((tissue > 0).sum())
    out = {}
    for lbl in range(10):
        n = int((tissue == lbl).sum())
        if lbl == 0:
            continue
        out[TIS_NAME[lbl]] = dict(voxels=n, volume=round(n * dvox, 2),
                                  frac_of_body=round(n / max(body, 1), 4))
    out["_body_voxels"] = body
    out["_body_volume"] = round(body * dvox, 2)
    return out
