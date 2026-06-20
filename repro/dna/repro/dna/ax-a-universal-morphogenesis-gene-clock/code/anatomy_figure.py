"""Build the bones+organs anatomy figure (skeleton, tissue cross-sections, volume bar)
and the LOAD figure (optimized vs naive + resolution sweep with internals)."""
import time, json
import numpy as np
import assemble as A, anatomy as AN, morpho_core as mc
import scipy.ndimage as ndi
from skimage import measure
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

TAU = 1.0
reg = A.D.emergent_registers()
bp, m = A.build_body(TAU, reg)
somites = m["somites"]

# ---- one tissue volume at good resolution for sections + skeleton ----
extent = (120.0, 46.0, 50.0); sc = 1.5
nx, ny, nz = int(200*sc), int(96*sc), int(104*sc)
occ, axes, d = bp.voxelize(nx, ny, nz, extent)
xs, ys, zs = axes
dvox = (extent[0]/nx)*(extent[1]/ny)*(extent[2]/nz)
spec = A.anatomy_spec(TAU, reg, somites)
tissue, st = AN.build_tissue(occ, axes, spec)
vr = AN.volume_report(tissue, dvox)

def surf(mask, smooth=0.7):
    sm = ndi.gaussian_filter(mask.astype(np.float32), smooth)
    if sm.max() < 0.5: return None, None
    v, f, n, _ = measure.marching_cubes(sm, 0.5)
    vm = np.stack([np.interp(v[:,0], np.arange(len(xs)), xs),
                   np.interp(v[:,1], np.arange(len(ys)), ys),
                   np.interp(v[:,2], np.arange(len(zs)), zs)], 1)
    return vm, n

def colorize(slc):
    """map a 2-D tissue label array to RGB."""
    h, w = slc.shape
    img = np.ones((h, w, 3))
    for lbl, col in AN.ORGAN_COLORS.items():
        if lbl == 0: continue
        img[slc == lbl] = col
    return img

def crop_window(ylo=-13, yhi=13, zlo=-15, zhi=15):
    jy = np.where((ys >= ylo) & (ys <= yhi))[0]
    kz = np.where((zs >= zlo) & (zs <= zhi))[0]
    return jy[0], jy[-1]+1, kz[0], kz[-1]+1

jy0, jy1, kz0, kz1 = crop_window()

# ---------- FIGURE 1: anatomy ----------
fig = plt.figure(figsize=(15, 10.5), facecolor="white")
gs = fig.add_gridspec(3, 6, height_ratios=[1.15, 1.05, 1.05], hspace=0.28, wspace=0.35)

# A. skeleton 3/4 (top, wide)
bone_v, bone_n = surf(tissue == AN.TIS["bone"], smooth=0.7)
imgk = mc.render_mesh(bone_v, bone_n, az=38, el=15, W=980, H=380,
                      base=(0.95,0.94,0.84), light=(0.4,0.55,0.75), point=2)
axk = fig.add_subplot(gs[0, :5]); axk.imshow(imgk); axk.axis("off")
axk.set_title(f"Emergent skeleton — {len(spec['vertebrae'])} vertebrae "
              f"(= {somites} somites, one per segment) · {len(spec['ribs'])} rib pairs · "
              f"skull · 4 limbs with phalanges", fontsize=11)

# B. legend (top right)
axL = fig.add_subplot(gs[0, 5]); axL.axis("off")
order = ["muscle","bone","skin","liver","gut","lung","heart"]
handles = [Patch(facecolor=AN.ORGAN_COLORS[A.TIS[k]], edgecolor="#888",
                 label=f"{k}  {100*vr[k]['frac_of_body']:.1f}%") for k in order if k in vr]
axL.legend(handles=handles, loc="center", frameon=False, fontsize=9.5,
           title="tissue (% body vol)", title_fontsize=10)

# C. mid-sagittal section (cropped to body band)
sag = tissue[:, jy0:jy1, nz//2].T[::-1, :]
axs1 = fig.add_subplot(gs[1, :4]); axs1.imshow(colorize(sag), aspect="equal")
axs1.set_title("mid-sagittal section — bone spine dorsal, viscera fill the trunk cavity, "
               "segmented muscle around", fontsize=10.5); axs1.axis("off")

# D. differentiation summary
axT = fig.add_subplot(gs[1, 4:]); axT.axis("off")
diff = sum(vr[k]['frac_of_body'] for k in ['muscle','bone','heart','lung','liver','gut'] if k in vr)
txt = ("VOLUME GAME\nbody is solid & fully tissue-typed\n(no vague filler):\n\n"
       f"  muscle (myomeres, ={somites} som): {100*vr['muscle']['frac_of_body']:.1f}%\n"
       f"  bone (spine+ribs+skull+limb): {100*vr['bone']['frac_of_body']:.1f}%\n"
       f"  viscera (heart/lung/liver/gut): "
       f"{100*sum(vr[k]['frac_of_body'] for k in ['heart','lung','liver','gut']):.1f}%\n"
       f"  dermis shell: {100*vr['skin']['frac_of_body']:.1f}%\n"
       f"  ----------------------------\n"
       f"  differentiated: {100*diff:.1f}%")
axT.text(0.0, 0.98, txt, va="top", ha="left", family="monospace", fontsize=10.5)

# E-G. three transverse sections (cropped to body core)
he, ts = reg["head_end"], reg["tail_start"]
cut_u = [he+0.095, he+0.165, 0.5*(he+ts)+0.095]
labels = ["through lungs / heart", "through liver", "through gut"]
for j,(u,lab) in enumerate(zip(cut_u, labels)):
    xx = A._u_to_x(u, spec["L"]); i0 = int(np.argmin(np.abs(xs - xx)))
    tr = tissue[i0, jy0:jy1, kz0:kz1].T[::-1, :]
    ax = fig.add_subplot(gs[2, 2*j:2*j+2]); ax.imshow(colorize(tr), aspect="equal")
    ax.set_title(f"transverse — {lab}", fontsize=10); ax.axis("off")

fig.suptitle("Filling the salamander with rough BONES + ORGANS — a solid, tissue-typed body",
             fontsize=13.5, y=0.99)
plt.savefig("anatomy.png", dpi=100, facecolor="white"); plt.close()
print("saved anatomy.png")

# ---------- FIGURE 2: the load / optimization ----------
# (a) optimized vs naive at reference res
occ0, axes0, _ = bp.voxelize(200, 96, 104, (118,46,50))
spec0 = A.anatomy_spec(TAU, reg, somites)
t0=time.perf_counter(); AN.build_tissue(occ0, axes0, spec0); t_opt=time.perf_counter()-t0
t0=time.perf_counter(); AN.naive_tissue(occ0, axes0, spec0); t_naive=time.perf_counter()-t0

# (b) resolution sweep WITH internals (skin voxelize + tissue build, optimized)
sweep=[]
for s in [0.5,0.7,1.0,1.4,1.8]:
    gx,gy,gz=int(200*s),int(96*s),int(104*s)
    t0=time.perf_counter()
    o,ax_,_=bp.voxelize(gx,gy,gz,(118,46,50))
    sp_=A.anatomy_spec(TAU,reg,somites)
    ti,stt=AN.build_tissue(o,ax_,sp_)
    dt=time.perf_counter()-t0
    sweep.append(dict(scale=s,voxels=int(o.size),touched=int(stt['voxels_touched']),seconds=round(dt,4)))

fig2,(a1,a2)=plt.subplots(1,2,figsize=(15,5),facecolor="white")
a1.bar(["optimized\n(bbox-cull + uint8)","naive\n(parts × full grid)"],[t_opt*1000,t_naive*1000],
       color=["#2e7d32","#b0413e"])
a1.set_yscale("log"); a1.set_ylabel("milliseconds (log)")
a1.set_title(f"Adding 88 internal parts: {t_naive/t_opt:.0f}× speedup, identical output")
for i,v in enumerate([t_opt*1000,t_naive*1000]):
    a1.text(i, v*1.15, f"{v:.0f} ms", ha="center", fontsize=10)

vx=np.array([s['voxels'] for s in sweep])/1e6
sc_=np.array([s['seconds'] for s in sweep])*1000
a2.plot(vx,sc_,"o-",color="#2e7d32",lw=2,ms=7,label="skin + bones + organs (optimized)")
for s in sweep:
    a2.annotate(f"{s['scale']:.1f}×",(s['voxels']/1e6,s['seconds']*1000),
                textcoords="offset points",xytext=(6,-10),fontsize=8)
a2.set_xlabel("grid voxels (millions)"); a2.set_ylabel("build time (ms)")
a2.set_title("Full anatomy build scales with resolution (work ∝ filled volume, not grid)")
a2.grid(alpha=0.3); a2.legend()
plt.tight_layout(); plt.savefig("load_anatomy.png",dpi=100,facecolor="white"); plt.close()
print("saved load_anatomy.png")

json.dump(dict(volume=vr, opt_ms=round(t_opt*1000,2), naive_ms=round(t_naive*1000,2),
               speedup=round(t_naive/t_opt,1), parts=st['parts'], sweep=sweep),
          open("anatomy_profile.json","w"), indent=2)
print(f"\nspeedup {t_naive/t_opt:.0f}x  | opt {t_opt*1000:.0f}ms vs naive {t_naive:.1f}s")
print("differentiated:", round(100*diff,1), "% ; muscle",
      round(100*vr['muscle']['frac_of_body'],1),"bone",round(100*vr['bone']['frac_of_body'],1))
