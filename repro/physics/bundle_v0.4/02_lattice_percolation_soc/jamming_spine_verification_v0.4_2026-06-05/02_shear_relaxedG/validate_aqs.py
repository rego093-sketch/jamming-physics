"""Validate AQS: elastic slope dsigma/dgamma|_0 should equal the static relaxed modulus G_relaxed.
Deep phi=0.70 (G well-defined). Also show the stress-strain curve -> yield plateau (sigma_y)."""
import numpy as np, time
from relaxed_shear import make_packing, relaxed_G, backbone_mask, mean_z
from aqs import aqs_run
pos,R,E,mF = make_packing(256,0.70,1.0,3,steps=8000,polish=True)
keep=backbone_mask(pos,R,1.0); z=mean_z(pos,R,1.0,keep); r=relaxed_G(pos,R,1.0)
print(f"phi=0.70 N=256 sd3: z={z:.3f}  G_Born={r['G_Born']:.3f}  G_relaxed(static)={r['G_relaxed']:.4f}")
t0=time.time()
g,s,mf = aqs_run(pos,R,1.0,dgamma=0.0025,gamma_max=0.4,fire_steps=5000)
s=np.abs(s)
print(f"AQS done: {len(g)} steps, max residual force across steps = {mf.max():.1e}  [{time.time()-t0:.0f}s]")
# elastic slope: fit over the first elastic points (gamma < first yield). Use gamma<=0.015.
el = g<=0.015
slope = np.polyfit(g[el], s[el], 1)[0] if el.sum()>=3 else float('nan')
# yield stress: mean over steady plateau gamma in [0.15,0.4]
pl = (g>=0.15)&(g<=0.4); sy = s[pl].mean(); sy_e = s[pl].std()/np.sqrt(pl.sum())
print(f"elastic slope (gamma<=0.015) = {slope:.4f}   vs   G_relaxed = {r['G_relaxed']:.4f}   ratio={slope/r['G_relaxed']:.2f}")
print(f"yield stress sigma_y (plateau gamma in[0.15,0.4]) = {sy:.4f} +/- {sy_e:.4f}")
idx=np.linspace(0,len(g)-1,12).astype(int)
print("gamma:", " ".join(f"{g[i]:.3f}" for i in idx))
print("sigma:", " ".join(f"{s[i]:.4f}" for i in idx))
