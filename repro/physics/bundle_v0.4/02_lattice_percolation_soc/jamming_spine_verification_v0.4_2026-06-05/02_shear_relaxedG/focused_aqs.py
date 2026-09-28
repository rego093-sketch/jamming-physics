"""Focused AQS check: apply a small affine shear to a minimized config.
  - WITHOUT minimizing: (sigma - sigma0)/gamma  should = G_Born   (affine response)
  - WITH minimizing:    (sigma - sigma0)/gamma  should = G_relaxed (relaxed response)
If both match the static linear-response values, the AQS machinery (affine+LE+minimize+stress) is correct."""
import numpy as np
from relaxed_shear import make_packing, relaxed_G, backbone_mask, mean_z
from le_shear import forces_stress
from aqs import fire_LE, wrap_LE

pos,R,E,mF = make_packing(128,0.70,1.0,3,steps=8000,polish=True)
keep=backbone_mask(pos,R,1.0); z=mean_z(pos,R,1.0,keep); r=relaxed_G(pos,R,1.0)
print(f"N=128 phi=0.70 sd3: z={z:.3f}  G_Born={r['G_Born']:.4f}  G_relaxed={r['G_relaxed']:.4f}")
_,_,s0,_ = forces_stress(pos,R,1.0,0.0)
print(f"residual stress sigma0 = {s0:+.5f}")
print(f"\n{'gamma':>7} {'G_Born_meas':>12} {'G_relax_meas':>13}")
for gt in [0.0005, 0.001, 0.002, 0.004]:
    # affine only (no minimization): shear positions, measure stress
    pa = pos.copy(); pa[:,0]+=gt*pa[:,1]; pa=wrap_LE(pa,1.0,gt-np.floor(gt))
    _,_,s_aff,_ = forces_stress(pa,R,1.0,gt)
    GB_meas = (s_aff - s0)/gt
    # relaxed (minimize at fixed gamma)
    pr,s_rel,mf = fire_LE(pa,R,1.0,gt,steps=6000,ftol=1e-9)
    GR_meas = (s_rel - s0)/gt
    print(f"{gt:7.4f} {GB_meas:12.4f} {GR_meas:13.4f}   (mF={mf:.0e})")
print(f"\nexpect G_Born_meas -> {r['G_Born']:.4f},  G_relax_meas -> {r['G_relaxed']:.4f}")
