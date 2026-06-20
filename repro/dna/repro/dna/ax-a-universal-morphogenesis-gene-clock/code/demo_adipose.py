"""
demo_adipose.py -- Layer 4 (adipose / energy-balance) demonstration.

Shows the user's thesis directly: ONE genome, made lean->heavy by an ENERGY dial, changes the
FACE and the BODY; and a high-propensity ("thrifty") obesity genome reaches the same change at a
lower energy than a lean one -- gene x environment, no HPC, no learned data.

Outputs (results/):
  adipose_face.png        -- a face, lean->heavy, fat depots glowing; W:H ratio rising
  adipose_body.png        -- a body, lean->heavy; waist:hip + adiposity index rising
  adipose_quadruped.png   -- an animal: the same axis is general (belly/rump/dewlap)
  adipose_gene_x_env.png  -- SAME environment, lean vs thrifty genome -> different fat (the gene effect)
  adipose.json            -- every number behind the figures (energies, alpha, AI, W:H, WHR, sha256)

Rendering: the lean surface is flesh-toned; each triangle is tinted toward a warm FAT colour by the
local depot weight * activation, so you SEE where this genome+energy puts fat. Deterministic.
"""
import os, json, hashlib
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from skimage import measure
from scipy import ndimage as ndi

import body as B
import render_plus as RP
import adipose as AD
import adipose_atlas as AA

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

SKIN = np.array(RP.GENE_COLOR["SKIN"], float)     # lean tissue (flesh)
FAT = np.array((0.97, 0.80, 0.42), float)         # adipose (warm cream/amber)

VIEW = {"face": (28, 12), "body": (24, 8), "quadruped": (30, 10)}


# --------------------------------------------------------------------- meshing (keeps faces)
def mesh_faces(sampler, box, vox, smooth=0.6):
    """Marching-cubes surface of phi'<=0 returning (verts, faces) in world units."""
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    field = sampler(P).astype(np.float32)
    sm = ndi.gaussian_filter((field <= 0).astype(np.float32), smooth)
    if sm.max() < 0.5 or sm.min() > 0.5:
        return None, None
    v, f, _, _ = measure.marching_cubes(sm, 0.5)
    xs, ys, zs = axes
    vm = np.stack([np.interp(v[:, 0], np.arange(len(xs)), xs),
                   np.interp(v[:, 1], np.arange(len(ys)), ys),
                   np.interp(v[:, 2], np.arange(len(zs)), zs)], 1)
    return vm, f.astype(int)


def fat_face_colors(verts, faces, depot, alpha):
    """Per-face colour: flesh blended toward FAT by local depot weight * activation in [0,1]."""
    centroids = verts[faces].mean(1)
    w = depot.weight(centroids)                     # (F,) depot occupancy at the face
    mix = np.clip(alpha * w, 0.0, 1.0)[:, None]     # how 'fat' this patch reads
    return SKIN[None, :] * (1 - mix) + FAT[None, :] * mix


def _paint(verts, faces, face_cols, fit, light=(0.45, 0.55, 0.8), ambient=0.36, bg=(1, 1, 1)):
    """Painter's-algorithm flat-shaded triangle render with EXPLICIT per-face colours.
    (Same projection/shading math as render_plus.render_tris, but colours are given, not gene-keyed.)"""
    import math
    R = fit["R"]; cx, cy, s = fit["cx"], fit["cy"], fit["s"]; W, H = fit["W"], fit["H"]
    P = verts @ R.T
    col = (P[:, 0] - cx) * s + W / 2.0
    row = H / 2.0 - (P[:, 1] - cy) * s
    z = P[:, 2]
    tri = P[faces]
    fn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(fn, axis=1, keepdims=True); ln[ln == 0] = 1
    fn = fn / ln
    fn[fn[:, 2] < 0] *= -1.0
    L = np.array(light, float); L /= np.linalg.norm(L)
    shade = ambient + (1 - ambient) * np.clip(fn @ L, 0, 1)
    fcol = np.clip(np.asarray(face_cols) * shade[:, None], 0, 1)
    depth = z[faces].mean(1)
    order = np.argsort(depth)
    img = np.ones((H, W, 3), float) * np.array(bg, float)
    C = np.stack([col[faces], row[faces]], -1)
    for fi in order:
        x0, y0 = C[fi, 0]; x1, y1 = C[fi, 1]; x2, y2 = C[fi, 2]
        minx = int(max(0, math.floor(min(x0, x1, x2)))); maxx = int(min(W - 1, math.ceil(max(x0, x1, x2))))
        miny = int(max(0, math.floor(min(y0, y1, y2)))); maxy = int(min(H - 1, math.ceil(max(y0, y1, y2))))
        if maxx < minx or maxy < miny:
            continue
        xs = np.arange(minx, maxx + 1); ys = np.arange(miny, maxy + 1)
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


def render_inflated(sampler, depot, box, vox, fit, az, el, smooth=0.6):
    """Render one inflated surface, faces tinted by where fat sits. Returns (img, verts)."""
    v, f = mesh_faces(sampler, box, vox, smooth=smooth)
    if v is None:
        return np.ones((fit["H"], fit["W"], 3), np.uint8) * 255, None
    cols = fat_face_colors(v, f, depot, sampler.alpha)
    img = _paint(v, f, cols, fit, light=(0.45, 0.55, 0.8), ambient=0.36)
    return img, v


def _sha_field(sampler, box, vox):
    """Deterministic hash of the sampled thickness field on a fixed grid (reproducibility)."""
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    fld = np.round(sampler(P), 6).astype(np.float64)
    return hashlib.sha256(fld.tobytes()).hexdigest()[:16]


# --------------------------------------------------------------------- an energy sweep figure
def energy_sweep(scene, energies, genome="neutral", android=0.5, vox=0.9, t_max=3.0,
                 metric="whr", waist_y=8.0, hip_y=-5.0, title=None):
    """Render `scene` over a list of energies (lean->heavy); annotate an anthropometric index."""
    target, depot = AA.SCENES[scene](android)
    model = AD.AdiposeModel()
    box = target.box
    az, el = VIEW.get(scene, (28, 12))

    # build the heaviest frame first so all frames share one projection fit
    heavy = AD.inflate_sampler(target, model, depot, max(energies), genome, t_max=t_max)
    vH, fH = mesh_faces(heavy, box, vox)
    fit = RP.fit_from(vH if vH is not None else np.zeros((3, 3)), az, el, 360, 460, margin=0.10)

    n = len(energies)
    fig = plt.figure(figsize=(2.7 * n, 3.7))
    rows = []
    for i, E in enumerate(energies):
        s = AD.inflate_sampler(target, model, depot, E, genome, t_max=t_max)
        img, v = render_inflated(s, depot, box, vox, fit, az, el)
        ai, vE, vL = AD.adiposity_index(s, AD.inflate_sampler(target, model, depot, model.E_lean,
                                                              genome, t_max=t_max), box, vox)
        if metric == "wh":
            idx = AD.face_width_height_ratio(v); lab = f"W:H {idx:.3f}"
        else:
            idx = AD.waist_hip_ratio(v, waist_y, hip_y); lab = f"WHR {idx:.3f}"
        ax = fig.add_subplot(1, n, i + 1)
        ax.imshow(img); ax.axis("off")
        ax.set_title(f"E={E:+.2f}   alpha={s.alpha:.2f}\nAI={ai:+.3f}   {lab}", fontsize=9)
        rows.append(dict(E=float(E), alpha=float(s.alpha), AI=float(ai),
                         V=float(vE), V_lean=float(vL), index=float(idx),
                         sha=_sha_field(s, box, vox)))
    fig.suptitle(title or f"{scene}: one genome, lean -> heavy (genome={genome})",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    out = os.path.join(RES, f"adipose_{scene}.png")
    fig.savefig(out, dpi=120, bbox_inches="tight"); plt.close(fig)
    print(f"  wrote {out}")
    return rows


# --------------------------------------------------------------------- gene x environment figure
def gene_x_environment(scene="body", E=0.2, android=0.6, vox=0.9, t_max=3.0,
                       waist_y=8.0, hip_y=-5.0):
    """SAME environment E; lean vs thrifty obesity genome -> different adiposity (the gene effect)."""
    target, depot = AA.SCENES[scene](android)
    model = AD.AdiposeModel()
    box = target.box
    az, el = VIEW.get(scene, (24, 8))

    genomes = ["lean", "neutral", "thrifty"]
    heavy = AD.inflate_sampler(target, model, depot, E, "thrifty", t_max=t_max)
    vH, _ = mesh_faces(heavy, box, vox)
    fit = RP.fit_from(vH if vH is not None else np.zeros((3, 3)), az, el, 360, 460, margin=0.10)

    # ONE shared canonical-lean reference (lean genome at E_lean): AI here is ABSOLUTE adiposity
    # relative to a lean body, so it orders by genome even after the fold saturates -- the gene
    # effect. (Per-genome self-referential AI is reserved for the within-genome energy sweeps.)
    shared_ref = AD.inflate_sampler(target, model, depot, model.E_lean, "lean", t_max=t_max)

    fig = plt.figure(figsize=(2.9 * len(genomes), 3.9))
    rows = []
    for i, g in enumerate(genomes):
        s = AD.inflate_sampler(target, model, depot, E, g, t_max=t_max)
        img, v = render_inflated(s, depot, box, vox, fit, az, el)
        ai, vE, vL = AD.adiposity_index(s, shared_ref, box, vox)
        whr = AD.waist_hip_ratio(v, waist_y, hip_y)
        P = model.propensity(g)
        ax = fig.add_subplot(1, len(genomes), i + 1)
        ax.imshow(img); ax.axis("off")
        ax.set_title(f"{g}   P_geno={P:+.2f}\nalpha={s.alpha:.2f}  AI={ai:+.3f}  WHR={whr:.3f}",
                     fontsize=9)
        rows.append(dict(genome=g, P_geno=float(P), alpha=float(s.alpha), AI=float(ai),
                         WHR=float(whr), sha=_sha_field(s, box, vox)))
    fig.suptitle(f"gene x environment: same E={E:+.2f}, different obesity genome ({scene})",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    out = os.path.join(RES, "adipose_gene_x_env.png")
    fig.savefig(out, dpi=120, bbox_inches="tight"); plt.close(fig)
    print(f"  wrote {out}")
    return rows


def main():
    print("Layer 4 adipose demo")
    print("one-switch (adipose fold == body fold):", AD.assert_one_switch_adipose())
    data = {"_one_switch_adipose": AD.assert_one_switch_adipose(),
            "_genome_propensity": {g: AD.AdiposeModel().propensity(g)
                                   for g in ("lean", "neutral", "thrifty")}}

    Es = [-1.0, -0.4, 0.2, 0.6, 1.0]
    print("face sweep ...");      data["face"] = energy_sweep("face", Es, metric="wh", vox=0.7,
                                                              t_max=2.2)
    print("body sweep ...");      data["body"] = energy_sweep("body", Es, metric="whr", vox=0.9,
                                                              android=0.6, t_max=3.0)
    print("quadruped sweep ..."); data["quadruped"] = energy_sweep("quadruped", Es, metric="whr",
                                                                   vox=1.1, android=0.6, t_max=3.0,
                                                                   waist_y=2.0, hip_y=6.0)
    print("gene x environment ..."); data["gene_x_env"] = gene_x_environment("body", E=0.2)

    out = os.path.join(RES, "adipose.json")
    with open(out, "w") as fh:
        json.dump(data, fh, indent=2)
    print(f"  wrote {out}")
    print("done.")


if __name__ == "__main__":
    main()
