"""
morpho_core.py -- the field-level primitives for emerging a body from the R19 switch.

Two things live here:
  (1) settle_field / switch_on : the SAME cusp (fold) bistable as organism.core.settle,
      vectorised over a 3-D drive field. It is validated against the scalar in-package
      organism.core to |dx| <= 1e-9 (C1: the field substrate is the in-package single
      source, just evaluated on an array).
  (2) a tiny deterministic software renderer (orthographic + z-buffer + Lambert) so the
      emerged external form can be looked at without any 3-D engine.

The biology mapping (whitepaper 'form <- gamma', Layer 1):
  - each developmental gene has a material scalar gamma (DNA NN-stiffness, 1.2..1.4 regime).
  - a morphogen concentration at a cell's position is the drive h that tilts the well.
  - organism.core decides ON/OFF with hysteresis -> smooth gradients become sharp domains.
"""
import math
import numpy as np
from organism import core   # the in-package R19 substrate (single source)


# ----------------------------------------------------------------------------------
# (1) the bistable switch as a field  (mirror of organism.core, array form)
# ----------------------------------------------------------------------------------
def spinodal(g):
    return (2.0 / (3.0 * math.sqrt(3.0))) * (g ** 1.5)


def settle_field(g, h, s_prev):
    """Stable equilibrium of  s^3 - g*s - h = 0  reached from s_prev, vectorised.

    g : scalar material stiffness (>0).  h, s_prev : float arrays of equal shape.
    Returns the settled state s (same shape).  Identical rule to core.settle:
      monostable -> the one real root; bistable -> upper root if s_prev>r2 else lower.
    """
    h = np.asarray(h, dtype=np.float64)
    s_prev = np.asarray(s_prev, dtype=np.float64)
    out = np.empty(h.shape, dtype=np.float64)

    disc = 4.0 * g ** 3 - 27.0 * h ** 2          # >0 three real roots; <0 one
    bist = disc > 0.0
    mono = ~bist

    # --- bistable cells: trigonometric three-root form ---
    if np.any(bist):
        hb = h[bist]
        arg = (3.0 * math.sqrt(3.0) * hb) / (2.0 * g ** 1.5)
        arg = np.clip(arg, -1.0, 1.0)
        m = 2.0 * math.sqrt(g / 3.0)
        a = np.arccos(arg) / 3.0
        r0 = m * np.cos(a)                       # k=0  (largest)
        r1 = m * np.cos(a - 2.0 * math.pi / 3.0) # k=1
        r2 = m * np.cos(a - 4.0 * math.pi / 3.0) # k=2
        rs = np.sort(np.stack([r0, r1, r2], axis=0), axis=0)   # ascending: lo, mid, hi
        lo, mid, hi = rs[0], rs[1], rs[2]
        on_upper = s_prev[bist] > mid
        out[bist] = np.where(on_upper, hi, lo)

    # --- monostable cells: Cardano single real root ---
    if np.any(mono):
        hm = h[mono]
        rad = np.sqrt(np.maximum(hm * hm / 4.0 - g ** 3 / 27.0, 0.0))
        def cbrt(x):
            return np.copysign(np.abs(x) ** (1.0 / 3.0), x)
        out[mono] = cbrt(hm / 2.0 + rad) + cbrt(hm / 2.0 - rad)
    return out


def switch_on(g, h, s_prev):
    """Boolean ON map: the settled state is on the upper (positive) stable branch."""
    return settle_field(g, h, s_prev) > 0.0


def validate_against_core(seed=19, n=4000):
    """Prove settle_field == organism.core.settle on a random grid of (g,h,s)."""
    rng = np.random.default_rng(seed)
    g_samples = rng.uniform(1.15, 1.45, n)         # the package gamma regime
    max_err = 0.0
    for g in g_samples:
        sp = spinodal(g)
        h = rng.uniform(-1.6 * sp, 1.6 * sp, 7)    # straddle the fold both sides
        s_prev = rng.uniform(-2.5, 2.5, 7)
        ref = np.array([core.settle(g, float(hh), float(ss))
                        for hh, ss in zip(h, s_prev)])
        got = settle_field(g, h, s_prev)
        max_err = max(max_err, float(np.max(np.abs(ref - got))))
    return max_err


# ----------------------------------------------------------------------------------
# (2) deterministic software renderer  (orthographic, z-buffer, Lambert)
# ----------------------------------------------------------------------------------
def _rot_matrix(az_deg, el_deg):
    az = math.radians(az_deg); el = math.radians(el_deg)
    Rz = np.array([[ math.cos(az), -math.sin(az), 0],
                   [ math.sin(az),  math.cos(az), 0],
                   [ 0,             0,            1]])
    Rx = np.array([[1, 0,            0],
                   [0, math.cos(el), -math.sin(el)],
                   [0, math.sin(el),  math.cos(el)]])
    return Rx @ Rz


def render_mesh(verts, normals, az=35, el=18, W=540, H=360,
                light=(0.4, 0.5, 0.85), base=(0.93, 0.74, 0.55),
                bg=(1, 1, 1), point=2, scale=None, center=None, ambient=0.30):
    """Render a vertex/normal cloud (e.g. from marching_cubes) as a shaded splat image.

    Fast and deterministic: rotate -> orthographic project -> z-buffer splat each vertex
    as a small disk shaded by ambient + diffuse*max(0, n.L).  Returns an (H,W,3) uint8.
    """
    R = _rot_matrix(az, el)
    L = np.array(light, float); L /= np.linalg.norm(L)
    base = np.array(base, float)

    P = verts @ R.T                              # rotate vertices
    N = normals @ R.T                            # rotate normals
    if center is None:
        center = 0.5 * (P.min(0) + P.max(0))
    P = P - center
    span = (P.max(0) - P.min(0))
    if scale is None:
        scale = 0.82 * min(W, H) / max(span[0], span[1], 1e-6)
    sx = (P[:, 0] * scale + W * 0.5)
    sy = (-P[:, 1] * scale + H * 0.5)            # image y down
    depth = P[:, 2]

    shade = ambient + (1 - ambient) * np.clip(N @ L, 0, 1)
    col = (base[None, :] * shade[:, None])       # (M,3)

    img = np.ones((H, W, 3), float) * np.array(bg, float)[None, None, :]
    zbuf = np.full((H, W), -1e18, float)

    ix = np.round(sx).astype(int); iy = np.round(sy).astype(int)
    order = np.argsort(depth)                    # paint back (far) -> front (near)
    ix, iy, depth, col = ix[order], iy[order], depth[order], col[order]

    rad = point
    for dx in range(-rad, rad + 1):
        for dy in range(-rad, rad + 1):
            if dx * dx + dy * dy > rad * rad:
                continue
            xx = ix + dx; yy = iy + dy
            ok = (xx >= 0) & (xx < W) & (yy >= 0) & (yy < H)
            xs, ys, ds, cs = xx[ok], yy[ok], depth[ok], col[ok]
            # z-test per pixel; later (nearer, since sorted ascending depth) wins
            better = ds > zbuf[ys, xs]
            ys2, xs2, cs2 = ys[better], xs[better], cs[better]
            zbuf[ys2, xs2] = ds[better]
            img[ys2, xs2] = cs2
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)
