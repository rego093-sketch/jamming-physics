"""Validate LE minimum-image: compare vectorized forces_stress vs brute-force triclinic enumeration,
at several shear strains gamma (incl. >1 to test wrap), on a real jammed config."""
import numpy as np
from relaxed_shear import make_packing
from le_shear import forces_stress, forces_stress_bruteforce

pos,R,E,mF = make_packing(200, 0.70, 1.0, 3, steps=8000, polish=True)
print(f"config: N=200 phi=0.70  R={R:.4f}  E={E:.3e}")
print(f"{'gamma':>7} {'nc_vec':>7} {'nc_bf':>6} {'dF_max':>10} {'sxy_vec':>11} {'sxy_bf':>11} {'rel_err':>9}")
for gamma in [0.0, 0.07, 0.5, 0.93, 1.37, 2.6]:
    Ev,Fv,sv,ncv = forces_stress(pos,R,1.0,gamma)
    Eb,Fb,sb,ncb = forces_stress_bruteforce(pos,R,1.0,gamma)
    dF = np.abs(Fv-Fb).max()
    rel = abs(sv-sb)/max(abs(sb),1e-12)
    print(f"{gamma:7.3f} {ncv:7d} {ncb:6d} {dF:10.2e} {sv:11.3e} {sb:11.3e} {rel:9.2e}")
print("\nPASS if dF_max ~ 1e-15 and contact counts match at every gamma.")
