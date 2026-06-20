"""
render_plus.py -- a crisp, deterministic triangle renderer that colours each surface patch
by the MASTER GENE that built it.

The in-package morpho_core.render_mesh is a z-buffered point splat (grainy). This module
instead fills the marching-cubes TRIANGLES with a painter's-algorithm rasteriser (sort faces
far->near, fill exactly, flat Lambert shading). The result is clean and -- crucially -- each
face is tinted by the gene of the nearest grown feature, so the picture literally shows
"which gene laid down which piece of anatomy". Pure numpy, fully deterministic.
"""
import math
import numpy as np
from target import _ellipsoid

# a distinct, readable colour per master gene (RGB 0..1)
GENE_COLOR = {
    # sensory masters
    "PAX6": (0.91, 0.30, 0.55),   # eye        - magenta
    "PAX2": (0.20, 0.62, 0.30),   # ear        - green
    "LHX2": (0.10, 0.72, 0.78),   # nose       - cyan
    "TP63": (0.62, 0.62, 0.66),   # skin/lid   - grey
    "MITF": (0.36, 0.25, 0.55),   # iris       - indigo
    # structural / axial
    "FOXG1": (0.16, 0.45, 0.78),  # cranium    - blue
    "SHH":  (0.55, 0.38, 0.72),   # midline    - purple
    "MYOD1": (0.95, 0.55, 0.18),  # cheek      - orange
    "POU2F3": (0.84, 0.18, 0.18), # lips/taste - red
    # hair / ectodermal appendage program
    "EDAR": (0.40, 0.26, 0.13),   # hair/feather/scale - brown
    "FOXN1": (0.55, 0.40, 0.22),  # eyebrow    - tan
    "HOXC13": (0.30, 0.20, 0.10), # eyelash    - dark brown
    "LEF1": (0.60, 0.60, 0.20),   # whisker    - olive
    # teeth
    "PAX9": (0.93, 0.90, 0.78),   # teeth      - ivory
    # limb / fin identity + digits
    "TBX5": (0.85, 0.65, 0.13),   # forelimb/pectoral - gold
    "TBX4": (0.13, 0.50, 0.55),   # hindlimb/pelvic   - teal
    "HOXD13": (0.70, 0.45, 0.30), # digits     - sienna
    "BMP4": (0.95, 0.78, 0.20),   # beak       - amber
    "SOX9": (0.45, 0.70, 0.85),   # cartilage  - sky
    # fallback
    "SKIN": (0.86, 0.70, 0.55),   # base envelope - flesh
}


def _rot(az_deg, el_deg):
    az = math.radians(az_deg); el = math.radians(el_deg)
    Rz = np.array([[math.cos(az), -math.sin(az), 0],
                   [math.sin(az),  math.cos(az), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0],
                   [0, math.cos(el), -math.sin(el)],
                   [0, math.sin(el),  math.cos(el)]])
    return Rx @ Rz


def face_genes(ftarget, present, centroids):
    """For each face centroid (model space), return the master gene of the nearest grown
    feature (or 'SKIN' if the base envelope is nearest). present : {name: a_f}."""
    n = len(centroids)
    dmin = np.full(n, np.inf); gidx = np.full(n, -1, dtype=int)
    for j, p in enumerate(ftarget.parts):
        s = 1.0 if present is None else float(present.get(p["name"], 1.0))
        di = ftarget._part_sdf(centroids, p, s)
        upd = di < dmin
        dmin[upd] = di[upd]; gidx[upd] = j
    base_d = np.full(n, np.inf)
    for bp in ftarget.base:
        base_d = np.minimum(base_d, _ellipsoid(centroids, bp[1], bp[2]))
    genes = np.empty(n, dtype=object)
    skin = base_d < dmin
    for k in range(n):
        genes[k] = "SKIN" if (skin[k] or gidx[k] < 0) else ftarget.parts[gidx[k]]["gene"]
    return genes


def fit_from(verts, az, el, W, H, margin=0.08, zoom=1.0):
    """Compute a projection fit (center, scale) from a vertex set so multiple frames share it."""
    R = _rot(az, el)
    P = verts @ R.T
    mn, mx = P.min(0), P.max(0)
    cx, cy = 0.5 * (mn[0] + mx[0]), 0.5 * (mn[1] + mx[1])
    span = max(mx[0] - mn[0], mx[1] - mn[1], 1e-6)
    s = zoom * (1 - 2 * margin) * min(W, H) / span
    return dict(R=R, cx=cx, cy=cy, s=s, W=W, H=H)


def render_tris(verts, faces, gene_per_face, fit, az=32, el=16,
                light=(0.45, 0.55, 0.8), ambient=0.34, bg=(1, 1, 1), edge=0.0):
    """Painter's-algorithm flat-shaded triangle render, each face tinted by its gene.
    verts:(V,3) faces:(F,3) gene_per_face:(F,) fit: dict from fit_from(). Returns (H,W,3) uint8."""
    R = fit["R"]; cx, cy, s = fit["cx"], fit["cy"], fit["s"]; W, H = fit["W"], fit["H"]
    P = verts @ R.T
    # to pixels: x->col (right), y->row (up => flip)
    col = (P[:, 0] - cx) * s + W / 2.0
    row = H / 2.0 - (P[:, 1] - cy) * s
    z = P[:, 2]

    tri = P[faces]                                   # (F,3,3) rotated
    fn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(fn, axis=1, keepdims=True); ln[ln == 0] = 1
    fn = fn / ln
    fn[fn[:, 2] < 0] *= -1.0                          # face the camera (+z)
    L = np.array(light, float); L /= np.linalg.norm(L)
    shade = ambient + (1 - ambient) * np.clip(fn @ L, 0, 1)   # (F,)

    base_cols = np.array([GENE_COLOR.get(g, GENE_COLOR["SKIN"]) for g in gene_per_face])
    fcol = np.clip(base_cols * shade[:, None], 0, 1)

    depth = z[faces].mean(1)                          # painter: far (small z) first
    order = np.argsort(depth)

    img = np.ones((H, W, 3), float) * np.array(bg, float)
    C = np.stack([col[faces], row[faces]], -1)        # (F,3,2) screen coords

    for fi in order:
        x0, y0 = C[fi, 0]; x1, y1 = C[fi, 1]; x2, y2 = C[fi, 2]
        minx = int(max(0, math.floor(min(x0, x1, x2))))
        maxx = int(min(W - 1, math.ceil(max(x0, x1, x2))))
        miny = int(max(0, math.floor(min(y0, y1, y2))))
        maxy = int(min(H - 1, math.ceil(max(y0, y1, y2))))
        if maxx < minx or maxy < miny:
            continue
        xs = np.arange(minx, maxx + 1)
        ys = np.arange(miny, maxy + 1)
        gx, gy = np.meshgrid(xs + 0.5, ys + 0.5)
        d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(d) < 1e-9:
            continue
        a = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) / d
        b = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) / d
        c = 1.0 - a - b
        inside = (a >= -1e-4) & (b >= -1e-4) & (c >= -1e-4)
        if not inside.any():
            continue
        sub = img[miny:maxy + 1, minx:maxx + 1]
        sub[inside] = fcol[fi]
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def render_stage(ftarget, stage, fit, az=32, el=16, **kw):
    """Render one grown stage with gene-coloured faces. Uses the stage's faces + present."""
    v = stage.get("verts_f"); f = stage.get("faces")
    if v is None or f is None or len(f) == 0:
        return np.ones((fit["H"], fit["W"], 3), np.uint8) * 255
    centroids = v[f].mean(1)
    g = face_genes(ftarget, stage.get("present"), centroids)
    return render_tris(v, f, g, fit, az=az, el=el, **kw)


def legend_handles(genes_used):
    """matplotlib proxy handles for a gene-colour legend (import mpatches lazily)."""
    import matplotlib.patches as mpatches
    return [mpatches.Patch(color=GENE_COLOR.get(g, GENE_COLOR["SKIN"]), label=g)
            for g in genes_used]
