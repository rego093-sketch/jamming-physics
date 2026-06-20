"""
stages.py -- emerge the whole developmental series from one egg to the adult tetrapod,
render each stage, and PROFILE THE LOAD (wall-clock + voxel/vertex counts) per stage.

Voxel size is held ~constant across stages, so the cost grows with the animal's actual
size (bigger body -> more voxels -> more time): that is the 'load (time)' to look at.
"""
import time, json, math
import numpy as np
import assemble as A, morpho_core as mc, body as B
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

VOX = 0.60   # target voxel size in model units (held constant -> cost ~ body volume)

# developmental stages: (key, tau, english, biological landmark)
STAGES = [
    ("egg",      None, "egg / blastula",        "pre-pattern sphere (no AP axis yet)"),
    ("neurula",  0.06, "neurula / tailbud",     "AP gradient read -> axis + head register"),
    ("pharyng",  0.16, "segmentation",          "somite clock laying trunk segments"),
    ("tadpole",  0.30, "larva (tadpole)",       "tail fin + gills, no limbs  [prior stop]"),
    ("budlimb",  0.50, "pre-metamorphic",       "limb buds appear, fin still high"),
    ("climax",   0.66, "metamorphic climax",    "limbs extend, fin + gills resorbing"),
    ("juvenile", 0.82, "froglet / efts",        "four limbs out, fin nearly gone"),
    ("adult",    1.00, "adult tetrapod",        "4 legs, 4/5 digits, tail, no fin"),
]

def extent_and_res(L):
    ex = max(1.30 * L, 16.0); ey = max(0.64 * L, 11.0); ez = max(0.60 * L, 10.0)
    nx = int(round(ex / VOX)); ny = int(round(ey / VOX)); nz = int(round(ez / VOX))
    return (ex, ey, ez), (nx, ny, nz)

def build_stage(key, tau):
    if tau is None:                      # egg: a single undifferentiated sphere
        L0 = 14.0
        bp = B.BodyPlan(blend=1.0); bp.add_sphere([0, 0, 0], 5.4)
        m = dict(tau=0.0, axis_len=L0, somites=0, digits_fore=0, digits_hind=0,
                 limb_extension=0.0, fin_kept=0.0, note="pre-pattern")
        return bp, m, L0
    bp, m = A.build_body(tau)
    return bp, m, m["axis_len"]

def main():
    rows = []
    panels = []
    rng_total = time.perf_counter()
    for key, tau, en, bio in STAGES:
        bp, m, L = build_stage(key, tau)
        extent, (nx, ny, nz) = extent_and_res(L)
        if key == "egg":                 # egg: cubic box sized to the sphere, cheap+smooth
            extent = (16.0, 16.0, 16.0); nx, ny, nz = 64, 64, 64
        hf = None if tau is None else (-L/2 + m["registers"]["head_end"] * L, 0.45) \
             if "registers" in m else None
        t0 = time.perf_counter()
        occ, verts, normals, axes = A.voxelize_and_mesh(bp, nx, ny, nz, extent,
                                                        smooth=0.85, head_flatten=hf)
        dt = time.perf_counter() - t0
        nv = 0 if verts is None else len(verts)
        rows.append(dict(key=key, en=en, bio=bio, tau=m.get("tau", 0.0),
                         axis_len=round(L, 2), voxels=int(occ.size),
                         filled=int(occ.sum()), verts=nv,
                         somites=m.get("somites", 0),
                         digits=f'{m.get("digits_fore",0)}/{m.get("digits_hind",0)}',
                         seconds=round(dt, 4)))
        # bigger splats for sparser (smaller) bodies so every stage renders solid
        if key == "egg":
            psize = 7
        else:
            psize = 2 if nv > 9000 else (3 if nv > 3500 else 4)
        img = mc.render_mesh(verts, normals, az=40, el=18, W=460, H=330,
                             base=(0.46, 0.62, 0.36), light=(0.5, 0.65, 0.6), point=psize) \
              if verts is not None else np.ones((330, 460, 3), np.uint8) * 255
        panels.append((key, en, bio, m, img))
    total = time.perf_counter() - rng_total

    # ---- montage 2 x 4
    fig, axs = plt.subplots(2, 4, figsize=(18, 9.0), facecolor="white")
    for ax, (key, en, bio, m, img) in zip(axs.ravel(), panels):
        ax.imshow(img); ax.axis("off")
        sub = ""
        if m.get("somites", 0): sub += f"somites {m['somites']}  "
        if m.get("digits_hind", 0): sub += f"digits {m['digits_fore']}/{m['digits_hind']}"
        ax.set_title(f"{en}    $\\tau$={m.get('tau',0):.2f}\n{sub}", fontsize=10.5, pad=4)
        ax.text(0.5, 0.02, bio, transform=ax.transAxes, ha="center",
                va="bottom", fontsize=8.0, color="#666", style="italic")
    fig.suptitle("Emergent development of an idealized urodele (salamander) tetrapod "
                 "from the R19 bistable switch\nexternal form — one egg to adult, "
                 "every register and count emerged from the switch + segmentation clock",
                 fontsize=12.5, y=0.995)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.02, wspace=0.02, hspace=0.18)
    plt.savefig("stage_series.png", dpi=98, facecolor="white"); plt.close()

    # ---- timing table
    print("\n=== DEVELOPMENTAL STAGE LOAD (constant voxel size, single CPU) ===")
    print(f"{'stage':<20}{'tau':>5}{'axis':>7}{'voxels':>10}{'filled':>9}"
          f"{'verts':>8}{'somite':>7}{'dig':>6}{'sec':>9}")
    for r in rows:
        print(f"{r['en']:<20}{r['tau']:>5.2f}{r['axis_len']:>7.1f}{r['voxels']:>10,}"
              f"{r['filled']:>9,}{r['verts']:>8,}{r['somites']:>7}{r['digits']:>6}"
              f"{r['seconds']:>9.3f}")
    print(f"{'-'*81}\n{'TOTAL all 8 stages':<58}{total:>9.3f}s")
    json.dump(dict(stages=rows, total_seconds=round(total, 4), voxel_size=VOX),
              open("stage_timing.json", "w"), indent=2)
    print("saved stage_series.png + stage_timing.json")

if __name__ == "__main__":
    main()
