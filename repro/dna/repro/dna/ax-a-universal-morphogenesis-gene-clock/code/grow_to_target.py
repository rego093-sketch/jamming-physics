"""
grow_to_target.py -- develop a generic form INTO a scanned target's 3D coordinates.

Principle (coarse-to-fine morphogenesis, which is what real development does: gross body
plan first, fine features last):
  * the target is a signed-distance field T(x) (the scan).
  * growth runs over developmental time tau in [0,1]; at each step we low-pass the target
    to scale sigma(tau) (large early -> only the gross blob; ->0 late -> full detail) and
    blend it with the starting form S0 by a(tau) (0 -> S0 egg ; 1 -> target).
  * the moving zero-level-set is the growing organism; nose/ears/etc. appear as sigma
    shrinks past their feature size. DNA/engine sets S0 (size, symmetry); the scan sets
    the individual's coordinates.

Convergence is measured two ways, both -> 0 as the form reaches the scan:
  * surface_rms : RMS |T(target)| sampled at the grown surface (how far off the target).
  * chamfer     : symmetric nearest-point distance between grown and target surfaces.
"""
import numpy as np
import scipy.ndimage as ndi
from scipy.spatial import cKDTree
from skimage import measure
import body as B


def smoothstep(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)


def _mesh(field, axes, smooth=0.6):
    sm = ndi.gaussian_filter((field <= 0).astype(np.float32), smooth)
    if sm.max() < 0.5 or sm.min() > 0.5:
        return None, None
    v, f, n, _ = measure.marching_cubes(sm, 0.5)
    xs, ys, zs = axes
    vm = np.stack([np.interp(v[:, 0], np.arange(len(xs)), xs),
                   np.interp(v[:, 1], np.arange(len(ys)), ys),
                   np.interp(v[:, 2], np.arange(len(zs)), zs)], 1)
    return vm, n


def egg_sdf(P, center, radius):
    return np.linalg.norm(P - np.asarray(center, float), axis=-1) - radius


def grow(target, vox=0.42, n_stages=8, coarse_sigma=7.0, S0=None, gamma=1.287):
    """Return (stages, info). Each stage: dict(tau, occ, verts, normals, rms, chamfer)."""
    box = target.box
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    xs, ys, zs = axes

    Tg = target.sample(P).astype(np.float32)            # the scan field (sampled once)
    tgt_v, tgt_n = _mesh(Tg, axes, smooth=0.6)          # target surface point set
    tree = cKDTree(tgt_v)

    if S0 is None:
        c = np.array([0.0, 0.0, 0.0])
        inside = P[Tg <= 0]
        if len(inside):
            c = inside.mean(0)
        # DNA link: initial blastula radius scales gently with gamma (body-size gene)
        r0 = 0.30 * min(box) * (gamma / 1.287)
        S0 = egg_sdf(P, c, r0).astype(np.float32)

    sigma_px = coarse_sigma / dx
    stages = []
    for i in range(n_stages):
        tau = i / (n_stages - 1)
        a = smoothstep(tau)
        s = sigma_px * (1.0 - tau)
        Tt = ndi.gaussian_filter(Tg, s) if s > 0.6 else Tg
        phi = (1.0 - a) * S0 + a * Tt
        v, n = _mesh(phi, axes, smooth=0.6)
        if v is None:
            continue
        # convergence metrics
        # surface_rms: sample true target SDF at grown verts via trilinear lookup
        gi = np.stack([np.interp(v[:, 0], xs, np.arange(nx)),
                       np.interp(v[:, 1], ys, np.arange(ny)),
                       np.interp(v[:, 2], zs, np.arange(nz))], 1)
        Tvals = ndi.map_coordinates(Tg, gi.T, order=1, mode="nearest")
        rms = float(np.sqrt(np.mean(Tvals ** 2)))
        dist_g2t, _ = tree.query(v, k=1)
        dist_t2g, _ = cKDTree(v).query(tgt_v, k=1)
        chamfer = float(0.5 * (dist_g2t.mean() + dist_t2g.mean()))
        stages.append(dict(tau=tau, occ=(phi <= 0), verts=v, normals=n,
                           rms=rms, chamfer=chamfer))
    info = dict(grid=(nx, ny, nz), voxels=nx * ny * nz, dx=dx,
                target=target.name, target_verts=len(tgt_v),
                tgt_v=tgt_v, tgt_n=tgt_n)
    return stages, info
