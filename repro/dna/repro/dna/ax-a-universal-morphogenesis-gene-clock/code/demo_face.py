import time, json, numpy as np
import target as T, grow_to_target as G, morpho_core as mc
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ft = T.face_target()
t0=time.perf_counter()
stages, info = G.grow(ft, vox=0.42, n_stages=8, coarse_sigma=7.0)
dt=time.perf_counter()-t0
print(f"grow: {dt:.2f}s  grid {info['grid']} = {info['voxels']:,} vox  stages {len(stages)}")
for s in stages:
    print(f"  tau={s['tau']:.2f}  surface_rms={s['rms']:5.2f}  chamfer={s['chamfer']:5.2f}  verts={len(s['verts']):,}")

# montage of growth + convergence curve
n=len(stages)
fig=plt.figure(figsize=(16,6.5),facecolor="white")
gs=fig.add_gridspec(2,n,height_ratios=[1.0,0.0001])
for i,s in enumerate(stages):
    img=mc.render_mesh(s['verts'],s['normals'],az=22,el=6,W=300,H=360,
                       base=(0.86,0.68,0.60),light=(0.3,0.5,0.8),point=2)
    ax=fig.add_subplot(gs[0,i]); ax.imshow(img); ax.axis("off")
    ax.set_title(f"$\\tau$={s['tau']:.2f}\nrms {s['rms']:.1f}", fontsize=9)
fig.suptitle("Growing a generic egg INTO a scanned human-face target (coarse-to-fine) — "
             "cranium first, then nose/brow/ears/lips emerge as detail sharpens", fontsize=12, y=1.02)
plt.tight_layout(); plt.savefig("face_growth.png",dpi=98,facecolor="white",bbox_inches="tight"); plt.close()

# convergence curves
fig2,(a1,a2)=plt.subplots(1,2,figsize=(13,4.4),facecolor="white")
taus=[s['tau'] for s in stages]
a1.plot(taus,[s['rms'] for s in stages],"o-",color="#b23",lw=2,ms=6)
a1.set_xlabel("developmental time $\\tau$"); a1.set_ylabel("surface RMS to target")
a1.set_title("Form converges onto the scanned coordinates"); a1.grid(alpha=0.3)
a2.plot(taus,[s['chamfer'] for s in stages],"o-",color="#26a",lw=2,ms=6)
a2.set_xlabel("developmental time $\\tau$"); a2.set_ylabel("Chamfer distance to target")
a2.set_title("Symmetric surface error -> 0"); a2.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("face_convergence.png",dpi=98,facecolor="white"); plt.close()
print("saved face_growth.png + face_convergence.png")
json.dump({"stages":[{k:s[k] for k in ('tau','rms','chamfer')} for s in stages],
           "grid":info['grid'],"voxels":info['voxels'],"seconds":round(dt,3)},
          open("face_growth.json","w"),indent=2)
