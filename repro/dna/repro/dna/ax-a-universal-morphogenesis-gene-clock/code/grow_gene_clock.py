"""
grow_gene_clock.py -- target-driven growth whose feature schedule is the GENE CLOCK.

The original grow_to_target.grow uses ONE global low-pass sigma(tau): every feature emerges
purely by its physical size. This version replaces that with a per-feature schedule from
gene_clock: each feature switches on at a tau set by its master gene's R19 spinodal (real
measured gamma) and grows out of the body envelope. Three time-scales are layered, each
from the engine:

  1. egg -> body envelope        A(tau) = smoothstep(tau)         (the blastula fills out)
  2. per-feature EMERGENCE        a_f(tau) from the gene's R19 fold (the new gene-clock heart;
                                  order + relative timing are a readout of measured gamma)
  3. sub-feature CRISPENING       residual low-pass sigma_res(tau)=s0*(1-tau)   (fine detail last)

At tau=1: A=1, every a_f=1, sigma_res=0  ->  phi = the full scan  ->  convergence -> 0,
so the headline proof ("the form reaches the scanned coordinates") is preserved; what is
new is that the PATH (which feature appears when) is now gene-determined, not hand-tuned.

Convergence is measured globally AND per feature (every feature reaching its own
coordinates as it emerges):
  * surface_rms   : RMS of the FULL target SDF sampled on the grown surface.
  * chamfer       : symmetric nearest-point distance to the full target surface.
  * feature_rms[f]: RMS of the full target SDF on grown verts inside feature f's AABB.
"""
import numpy as np
import scipy.ndimage as ndi
from scipy.spatial import cKDTree
from skimage import measure
import body as B
import gene_clock as GC
from grow_to_target import smoothstep, _mesh, egg_sdf
from skimage import measure as _measure


def _mesh_f(field, axes, smooth=0.6):
    """Like grow_to_target._mesh but ALSO returns the triangle faces (for crisp rendering)."""
    sm = ndi.gaussian_filter((field <= 0).astype(np.float32), smooth)
    if sm.max() < 0.5 or sm.min() > 0.5:
        return None, None, None
    v, f, n, _ = _measure.marching_cubes(sm, 0.5)
    xs, ys, zs = axes
    vm = np.stack([np.interp(v[:, 0], np.arange(len(xs)), xs),
                   np.interp(v[:, 1], np.arange(len(ys)), ys),
                   np.interp(v[:, 2], np.arange(len(zs)), zs)], 1)
    return vm, f.astype(np.int32), n


def grow_gene_clock(ftarget, vox=0.45, n_stages=9, coarse_sigma=6.0,
                    gamma_body=1.287, tau0=0.12, tau1=0.92, sign=+1):
    """ftarget : a FeatureTarget (gene-tagged growable features).
    Returns (stages, info, schedule). Each stage: tau, occ, verts, normals, rms, chamfer,
    present (dict name->a_f), feature_rms (dict name->RMS-in-bbox or None)."""
    one_switch = GC.assert_one_switch()                       # prove same R19 across packages
    gammas, prov = GC.load_gamma()
    sched = GC.feature_schedule(ftarget.features, gammas, tau0=tau0, tau1=tau1,
                                sign=sign, n_tau=n_stages)
    taus = sched["taus"]

    box = ftarget.box
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    xs, ys, zs = axes

    Tfull = ftarget.sample(P, None).astype(np.float32)        # the full scan (all features)
    tgt_v, tgt_n = _mesh(Tfull, axes, smooth=0.6)
    tree = cKDTree(tgt_v)

    # egg seed: blastula radius scales gently with the body-size gene's gamma
    inside = P[Tfull <= 0]
    c = inside.mean(0) if len(inside) else np.zeros(3)
    r0 = 0.30 * min(box) * (gamma_body / 1.287)
    S0 = egg_sdf(P, c, r0).astype(np.float32)

    sigma0_px = coarse_sigma / dx

    # precompute per-feature AABB index masks (for per-feature convergence)
    fboxes = {}
    for fname, _ in ftarget.features:
        cen, half = ftarget.feature_box(fname)
        fboxes[fname] = (cen, half)

    stages = []
    for i in range(n_stages):
        tau = taus[i]
        A = smoothstep(tau)
        # per-feature presence a_f(tau) from the gene clock
        present = {f: float(sched["features"][f]["a"][i]) for f, _ in ftarget.features}
        Tt = ftarget.sample(P, present).astype(np.float32)    # features grown to a_f
        s_res = sigma0_px * (1.0 - tau)                       # sub-feature crispening
        Tt = ndi.gaussian_filter(Tt, s_res) if s_res > 0.6 else Tt
        phi = (1.0 - A) * S0 + A * Tt

        v, n = _mesh(phi, axes, smooth=0.6)
        if v is None:
            continue
        vf, faces, nf = _mesh_f(phi, axes, smooth=0.6)   # same surface, with faces for rendering
        # global convergence vs the FULL target
        gi = np.stack([np.interp(v[:, 0], xs, np.arange(nx)),
                       np.interp(v[:, 1], ys, np.arange(ny)),
                       np.interp(v[:, 2], zs, np.arange(nz))], 1)
        Tvals = ndi.map_coordinates(Tfull, gi.T, order=1, mode="nearest")
        rms = float(np.sqrt(np.mean(Tvals ** 2)))
        dist_g2t, _ = tree.query(v, k=1)
        dist_t2g, _ = cKDTree(v).query(tgt_v, k=1)
        chamfer = float(0.5 * (dist_g2t.mean() + dist_t2g.mean()))
        # per-feature convergence: verts inside each feature's AABB
        frms = {}
        for f, (cen, half) in fboxes.items():
            m = np.all(np.abs(v - cen) <= half, axis=1)
            frms[f] = float(np.sqrt(np.mean(Tvals[m] ** 2))) if m.sum() >= 5 else None
        stages.append(dict(tau=float(tau), occ=(phi <= 0), verts=v, normals=n,
                           faces=faces, verts_f=vf, normals_f=nf,
                           rms=rms, chamfer=chamfer, present=present, feature_rms=frms))

    info = dict(grid=(nx, ny, nz), voxels=nx * ny * nz, dx=dx, target=ftarget.name,
                target_verts=len(tgt_v), tgt_v=tgt_v, tgt_n=tgt_n,
                one_switch_delta=one_switch, gamma_provenance=prov)
    return stages, info, sched
