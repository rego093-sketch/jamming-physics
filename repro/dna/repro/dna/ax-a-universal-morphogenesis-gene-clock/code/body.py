"""
body.py -- turn a body plan (axial radius profile + attachment list) into a voxel body.

The *placement* of every part (head/trunk/tail registers, limb AP stations, fin extent,
segment count) is decided upstream by the R19 switches + the segmentation clock; this file
only renders those decisions as switch-gated implicit solids and voxelises them.  The
continuum tissue-mechanics that would physically grow these shapes from cells is the [O]
obstacle (see LEDGER) -- here the shape is an implicit-surface read-out of the pattern.

All SDFs are vectorised over the whole grid (numpy), so cost scales with voxel count: this
is where the 'load (time)' the author wants to see is paid.
"""
import numpy as np


def grid(nx, ny, nz, extent):
    """Centered coordinate grid. extent=(Lx,Ly,Lz) in model units. Returns P (nx,ny,nz,3) and spacing."""
    xs = np.linspace(-extent[0] / 2, extent[0] / 2, nx)
    ys = np.linspace(-extent[1] / 2, extent[1] / 2, ny)
    zs = np.linspace(-extent[2] / 2, extent[2] / 2, nz)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    P = np.stack([X, Y, Z], axis=-1)
    dx = xs[1] - xs[0]
    return P, (xs, ys, zs), dx


def sdf_round_cone(P, a, b, ra, rb):
    """Signed distance to a tapered capsule (round cone) from a to b with end radii ra,rb.
    Vectorised Inigo-Quilez round-cone. P: (...,3). a,b: (3,). returns (...)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    ba = b - a
    l2 = float(ba @ ba)
    rr = ra - rb
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pa = P - a
    y = pa @ ba
    z = y - l2
    cross = pa * l2 - np.multiply.outer(y, ba)
    x2 = np.sum(cross * cross, axis=-1)
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    out = (np.sqrt(np.maximum(x2 * a2 * il2, 0.0)) + y * rr) * il2 - ra      # default (cone flank)
    cond_b = np.sign(z) * a2 * z2 > k
    cond_a = np.sign(y) * a2 * y2 < k
    out = np.where(cond_b, np.sqrt(x2 + z2) * il2 - rb, out)
    out = np.where((~cond_b) & cond_a, np.sqrt(x2 + y2) * il2 - ra, out)
    return out


def sdf_sphere(P, c, r):
    c = np.asarray(c, float)
    return np.linalg.norm(P - c, axis=-1) - r


def sdf_slab_blade(P, x0, x1, z_center, half_thick, top, bottom):
    """A thin midline fin blade between AP x0..x1, vertical span bottom..top, thin in z.
    Returns an SDF-like field (box distance)."""
    cx = (x0 + x1) / 2; hx = (x1 - x0) / 2
    cy = (top + bottom) / 2; hy = (top - bottom) / 2
    qx = np.abs(P[..., 0] - cx) - hx
    qy = np.abs(P[..., 1] - cy) - hy
    qz = np.abs(P[..., 2] - z_center) - half_thick
    qx = np.maximum(qx, 0); qy = np.maximum(qy, 0); qz = np.maximum(qz, 0)
    return np.sqrt(qx * qx + qy * qy + qz * qz) - 0.0


def smin(d1, d2, k):
    """Polynomial smooth-min union (blends parts so joints are organic, not faceted)."""
    h = np.clip(0.5 + 0.5 * (d2 - d1) / k, 0, 1)
    return d2 * (1 - h) + d1 * h - k * h * (1 - h)


class BodyPlan:
    """Collects implicit parts, then voxelises. Units: model length along AP ~ [-50,50]."""
    def __init__(self, blend=1.4):
        self.parts = []          # list of ('cone'|'sphere'|'blade', payload)
        self.blend = blend

    def add_axis(self, stations):
        """stations: list of (x, y_center, radius). Builds the tapered axial tube."""
        for (x0, y0, r0), (x1, y1, r1) in zip(stations[:-1], stations[1:]):
            self.parts.append(("cone", ([x0, y0, 0.0], [x1, y1, 0.0], max(r0, .2), max(r1, .2))))

    def add_limb(self, base, tip, r_base, r_tip, blend=True):
        self.parts.append(("cone", (list(base), list(tip), r_base, r_tip)))

    def add_sphere(self, c, r):
        self.parts.append(("sphere", (list(c), r)))

    def add_blade(self, x0, x1, top, bottom, thick=0.7):
        self.parts.append(("blade", (x0, x1, 0.0, thick, top, bottom)))

    def field(self, P):
        d = None
        for kind, pl in self.parts:
            if kind == "cone":
                a, b, ra, rb = pl
                di = sdf_round_cone(P, a, b, ra, rb)
            elif kind == "sphere":
                c, r = pl
                di = sdf_sphere(P, c, r)
            else:
                x0, x1, zc, th, top, bot = pl
                di = sdf_slab_blade(P, x0, x1, zc, th, top, bot)
            d = di if d is None else smin(d, di, self.blend)
        return d

    def _aabb(self, pl, kind, pad):
        if kind == "cone":
            a, b, ra, rb = pl
            a = np.asarray(a, float); b = np.asarray(b, float); rr = max(ra, rb) + pad
            lo = np.minimum(a, b) - rr; hi = np.maximum(a, b) + rr
        elif kind == "sphere":
            c, r = pl; c = np.asarray(c, float)
            lo = c - (r + pad); hi = c + (r + pad)
        else:
            x0, x1, zc, th, top, bot = pl
            lo = np.array([min(x0, x1) - pad, bot - pad, zc - th - pad])
            hi = np.array([max(x0, x1) + pad, top + pad, zc + th + pad])
        return lo, hi

    def voxelize(self, nx, ny, nz, extent):
        """Occupancy via local (bbox-culled) implicit union: each part only writes its
        own neighbourhood, so cost ~ sum(part volumes) not parts*grid."""
        P, axes, dx = grid(nx, ny, nz, extent)
        xs, ys, zs = axes
        d = np.full((nx, ny, nz), 1e9, dtype=np.float32)
        pad = 2.2 * self.blend
        for kind, pl in self.parts:
            lo, hi = self._aabb(pl, kind, pad)
            ix0 = max(0, int(np.searchsorted(xs, lo[0]) - 1)); ix1 = min(nx, int(np.searchsorted(xs, hi[0]) + 1))
            iy0 = max(0, int(np.searchsorted(ys, lo[1]) - 1)); iy1 = min(ny, int(np.searchsorted(ys, hi[1]) + 1))
            iz0 = max(0, int(np.searchsorted(zs, lo[2]) - 1)); iz1 = min(nz, int(np.searchsorted(zs, hi[2]) + 1))
            if ix0 >= ix1 or iy0 >= iy1 or iz0 >= iz1:
                continue
            sub = P[ix0:ix1, iy0:iy1, iz0:iz1, :]
            if kind == "cone":
                a, b, ra, rb = pl; di = sdf_round_cone(sub, a, b, ra, rb)
            elif kind == "sphere":
                c, r = pl; di = sdf_sphere(sub, c, r)
            else:
                x0, x1, zc, th, top, bot = pl; di = sdf_slab_blade(sub, x0, x1, zc, th, top, bot)
            dsub = d[ix0:ix1, iy0:iy1, iz0:iz1]
            d[ix0:ix1, iy0:iy1, iz0:iz1] = smin(dsub, di.astype(np.float32), self.blend)
        occ = (d <= 0.0)
        return occ, axes, d
