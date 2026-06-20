"""
profile_load.py -- the 'load (time)' study the author asked for.

(1) cost breakdown of one adult build: emergence (registers+clock, the Layer-1 content)
    vs voxelisation vs marching-cubes vs render.
(2) resolution sweep: rebuild the adult at finer/coarser voxel sizes and show wall-clock
    scales ~linearly with voxel count (the SDF union is evaluated per voxel).
"""
import time, json
import numpy as np
import assemble as A, body as B, develop as D, morpho_core as mc
from skimage import measure
import scipy.ndimage as ndi
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

def timed(fn, *a, **k):
    t = time.perf_counter(); r = fn(*a, **k); return r, time.perf_counter() - t

# ---------- (1) breakdown of one adult at reference resolution ----------
def breakdown():
    (reg), t_reg = timed(D.emergent_registers)
    t0 = time.perf_counter()
    _ = D.somite_count(90*0.9); _ = D.digit_count(0.42*16.13); t_clock = time.perf_counter()-t0
    (bp_m), t_build = timed(A.build_body, 1.0, reg)
    bp = bp_m[0]
    extent = (118, 46, 50); nx, ny, nz = 200, 96, 104
    (occ_axes), t_vox = timed(bp.voxelize, nx, ny, nz, extent)
    occ, axes, d = occ_axes
    (sm), t_sm = timed(ndi.gaussian_filter, occ.astype(np.float32), 0.85)
    (mc_out), t_march = timed(measure.marching_cubes, sm, 0.5)
    verts, faces, normals, _ = mc_out
    xs, ys, zs = axes
    vm = np.stack([np.interp(verts[:,0], np.arange(len(xs)), xs),
                   np.interp(verts[:,1], np.arange(len(ys)), ys),
                   np.interp(verts[:,2], np.arange(len(zs)), zs)], 1)
    (_img), t_render = timed(mc.render_mesh, vm, normals, 40, 18)
    parts = [("emergence: AP registers (R19 switch)", t_reg),
             ("emergence: seg/digit clocks", t_clock),
             ("body-plan assembly (SDF setup)", t_build),
             ("voxelisation (SDF union, per-voxel)", t_vox),
             ("surface smoothing", t_sm),
             ("marching cubes (mesh extract)", t_march),
             ("software render (shade+z-buffer)", t_render)]
    return parts, occ.size, len(vm)

# ---------- (2) resolution sweep ----------
def sweep():
    reg = D.emergent_registers()
    bp, _ = A.build_body(1.0, reg)
    base = (118.0, 46.0, 50.0)
    res = []
    for scale in [0.5, 0.7, 1.0, 1.4, 1.8, 2.2]:
        nx = int(round(200*scale)); ny = int(round(96*scale)); nz = int(round(104*scale))
        t0 = time.perf_counter()
        occ, axes, d = bp.voxelize(nx, ny, nz, base)
        sm = ndi.gaussian_filter(occ.astype(np.float32), 0.85)
        verts, faces, normals, _ = measure.marching_cubes(sm, 0.5)
        dt = time.perf_counter() - t0
        res.append(dict(scale=scale, nx=nx, ny=ny, nz=nz, voxels=int(occ.size),
                        filled=int(occ.sum()), verts=int(len(verts)), seconds=round(dt,4)))
    return res

def main():
    parts, vox, nv = breakdown()
    tot = sum(t for _, t in parts)
    print("\n=== ADULT BUILD COST BREAKDOWN (200x96x104 = {:,} voxels, {:,} verts) ===".format(vox, nv))
    for name, t in parts:
        print(f"  {name:<42}{t*1000:8.1f} ms   {100*t/tot:5.1f}%")
    print(f"  {'-'*42}{tot*1000:8.1f} ms   100.0%")
    emg = parts[0][1] + parts[1][1]
    print(f"\n  emergence (Layer-1, reproducible core): {emg*1000:.2f} ms  ({100*emg/tot:.1f}%)")
    print(f"  geometry read-out (parametric canvas):  {(tot-emg)*1000:.2f} ms  ({100*(tot-emg)/tot:.1f}%)")

    rs = sweep()
    print("\n=== RESOLUTION SWEEP (adult; voxel cost is ~linear in voxel count) ===")
    print(f"{'scale':>6}{'grid':>16}{'voxels':>12}{'verts':>9}{'sec':>9}{'ms/Mvox':>10}")
    for r in rs:
        grid = f"{r['nx']}x{r['ny']}x{r['nz']}"
        print(f"{r['scale']:>6.1f}{grid:>16}{r['voxels']:>12,}"
              f"{r['verts']:>9,}{r['seconds']:>9.3f}{1000*r['seconds']/(r['voxels']/1e6):>10.1f}")

    # ---- figure: breakdown bar + sweep line
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.2), facecolor="white")
    names = [p[0].replace("emergence: ", "emg: ") for p in parts]
    times = [p[1]*1000 for p in parts]
    colors = ["#2e7d32","#43a047"] + ["#8d6e63","#a1887f","#bcaaa4","#d7ccc8","#90a4ae"]
    ax1.barh(range(len(names)), times, color=colors)
    ax1.set_yticks(range(len(names))); ax1.set_yticklabels(names, fontsize=9)
    ax1.invert_yaxis(); ax1.set_xlabel("milliseconds"); ax1.set_title("Adult build — where the time goes")
    for i, t in enumerate(times):
        ax1.text(t+max(times)*0.01, i, f"{t:.0f}ms", va="center", fontsize=8)

    vx = np.array([r['voxels'] for r in rs])/1e6
    sc = np.array([r['seconds'] for r in rs])
    ax2.plot(vx, sc*1000, "o-", color="#2e7d32", lw=2, ms=7)
    a = np.polyfit(vx, sc*1000, 1)
    xx = np.linspace(0, vx.max()*1.05, 50)
    ax2.plot(xx, a[0]*xx+a[1], "--", color="#9e9e9e", label=f"linear fit ~{a[0]:.0f} ms/Mvoxel")
    for r in rs:
        ax2.annotate(f"{r['scale']:.1f}x", (r['voxels']/1e6, r['seconds']*1000),
                     textcoords="offset points", xytext=(6,-10), fontsize=8)
    ax2.set_xlabel("voxel count (millions)"); ax2.set_ylabel("voxel+mesh time (ms)")
    ax2.set_title("Load scales ~linearly with resolution"); ax2.legend(); ax2.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("load_profile.png", dpi=98, facecolor="white"); plt.close()
    json.dump(dict(breakdown=[(n, round(t,5)) for n,t in parts], sweep=rs),
              open("load_profile.json","w"), indent=2)
    print("\nsaved load_profile.png + load_profile.json")

if __name__ == "__main__":
    main()
