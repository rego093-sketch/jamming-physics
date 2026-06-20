"""
demo_life_course.py -- render the LIFE COURSE of one genome as a single continuous R19 fold.

This is the picture behind life_course.py: a single individual lived forward across the TIME axis
(the gene clock decides which features have emerged at developmental time tau) and then the ENERGY
axis (the adipose fold inflates the mature body by alpha(E, genome) over the anatomical depot).
Read left to right it is ONE process -- small lean child -> grown lean adult -> grown heavier adult
-- and both halves are literally the SAME spinodal switch (asserted < 1e-12 inside LifeCourse).

Outputs (results/):
  life_course_face.png  -- a face over a chosen life: infant -> child -> adolescent -> adult lean
                           -> adult surplus -> adult heavy. Each panel: tau, E, alpha, #features
                           emerged (the gamma readout), occupancy volume, face W:H.
  life_course_body.png  -- the same life on the body scene (waist:hip rises with E at maturity).
  life_course.json      -- one_switch delta, emergence order (gamma readout), and every number
                           behind both montages (tau, E, A, alpha, n_emerged, volume, index, sha).

Rendering reuses demo_adipose's exact render path (marching cubes -> painter's-algorithm flat
shading, faces tinted toward a warm fat colour by local depot*alpha) so the life-course frames are
drawn the same way as the energy sweeps. The lean reference frame (adult lean, E=E_lean) has
alpha == 0, so it is the pure gene-clock surface -- the energy axis perturbs nothing there.
Deterministic.
"""
import os, json
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import render_plus as RP
import life_course as LC
import demo_adipose as DA          # reuse mesh_faces / fat_face_colors / _paint / _sha_field

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)


def _largest_frame_fit(lc, points, vox, az, el, W, H):
    """One shared projection fit, built from the frame with the largest spatial extent so every
    life point fits the same canvas. The adult-heavy point (full development + inflation) is the
    largest, so the whole life is drawn at one consistent scale -- you SEE the child as small."""
    best_v, best_extent = None, -1.0
    for _label, tau, E in points:
        s, _dev = lc.sampler(tau, E)
        v, _f = DA.mesh_faces(s, lc.ft.box, vox)
        if v is None:
            continue
        extent = float(np.linalg.norm(v.max(0) - v.min(0)))
        if extent > best_extent:
            best_extent, best_v = extent, v
    if best_v is None:
        best_v = np.zeros((3, 3))
    return RP.fit_from(best_v, az, el, W, H, margin=0.10)


def life_montage(lc, points, vox, scene_name, panel=(360, 460)):
    """Render one row over a chosen life; annotate the developmental + energy state at each point.
    Returns the per-point metric rows (and writes results/life_course_<scene>.png)."""
    W, H = panel
    az, el = DA.VIEW.get(lc.scene, (28, 12))
    fit = _largest_frame_fit(lc, points, vox, az, el, W, H)

    n = len(points)
    fig = plt.figure(figsize=(2.7 * n, 3.9))
    rows = []
    for i, (label, tau, E) in enumerate(points):
        s, dev = lc.sampler(tau, E)
        img, v = DA.render_inflated(s, lc.depot, lc.ft.box, vox, fit, az, el)
        vol, _grid, _dx = lc.occupancy_volume(s, vox)
        if lc.scene == "face":
            idx = DA.AD.face_width_height_ratio(v); idx_lab = f"W:H {idx:.3f}"; idx_name = "WH"
        else:
            idx = DA.AD.waist_hip_ratio(v, 8.0, -5.0); idx_lab = f"WHR {idx:.3f}"; idx_name = "WHR"
        ax = fig.add_subplot(1, n, i + 1)
        ax.imshow(img); ax.axis("off")
        emerged = f"{dev.n_emerged()}/{len(lc.ft.features)}"
        ax.set_title(f"{label}\ntau={tau:.2f}  E={E:+.2f}\nalpha={s.alpha:.2f}  feats {emerged}\n"
                     f"vol={vol:.0f}  {idx_lab}", fontsize=8.5)
        rows.append(dict(label=label, tau=float(tau), E=float(E),
                         A_developmental=float(LC.smoothstep(tau)),
                         alpha_adipose=float(s.alpha),
                         n_emerged=dev.n_emerged(), n_features=len(lc.ft.features),
                         occupancy_volume=float(vol), index=float(idx), index_name=idx_name,
                         sha=DA._sha_field(s, lc.ft.box, vox)))
    fig.suptitle(f"life course ({scene_name}): one genome, one continuous R19 fold -- "
                 f"child -> adult (TIME) -> heavy (ENERGY)", fontsize=12, y=1.02)
    fig.tight_layout()
    out = os.path.join(RES, f"life_course_{lc.scene}.png")
    fig.savefig(out, dpi=120, bbox_inches="tight"); plt.close(fig)
    print(f"  wrote {out}")
    return rows


def main():
    print("life-course demo  (gene clock TIME x adipose ENERGY = one R19 fold)")
    points = LC.default_life()

    data = {}
    # face scene
    lc_face = LC.LifeCourse(scene="face")
    data["_one_switch"] = float(lc_face.one_switch)
    data["_order_is_gamma_readout"] = lc_face.order_is_gamma_readout()
    data["_emergence_order"] = lc_face.emergence_order()
    print(f"  one continuous fold (time==energy==body): {lc_face.one_switch:.2e}")
    print(f"  emergence order (gamma readout={lc_face.order_is_gamma_readout()}): "
          f"{' < '.join(lc_face.emergence_order())}")
    print("  face montage ...")
    data["face"] = life_montage(lc_face, points, vox=0.8, scene_name="face")

    # body scene -- same life, the composition axis shows on waist:hip
    print("  body montage ...")
    lc_body = LC.LifeCourse(scene="body", android=0.6)
    data["body"] = life_montage(lc_body, points, vox=0.9, scene_name="body")

    out = os.path.join(RES, "life_course.json")
    with open(out, "w") as fh:
        json.dump(data, fh, indent=2)
    print(f"  wrote {out}")
    print("done.")


if __name__ == "__main__":
    main()
