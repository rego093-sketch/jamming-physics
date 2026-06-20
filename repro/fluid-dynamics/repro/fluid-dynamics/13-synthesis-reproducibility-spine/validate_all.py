"""validate_all.py — one-shot reproducibility validation for the VP fluid whitepaper.
Run: python validate_all.py   (needs numpy, scipy, pandas; rotcore CSV path optional)
Prints PASS/FAIL for each verified claim."""
import numpy as np, ns2d, metriplectic_vortex as mv
ok = lambda b: "PASS" if b else "FAIL"
print("VP FLUID WHITEPAPER — REPRODUCIBILITY VALIDATION")
# 1 Euler invariants
o = ns2d.run(128, 0.0, seed=7, T=4.0, k_peak=4.0)
dE=(o['E'].max()-o['E'].min())/o['E'][0]; dZ=(o['Z'].max()-o['Z'].min())/o['Z'][0]
print(f"[1] 2D Euler energy+enstrophy conserved (nu=0):    {ok(dE<1e-5 and dZ<1e-4)}  (dE={dE:.1e}, dZ={dZ:.1e})")
# 2 energy budget identity
o = ns2d.run(128, 0.01, seed=7, T=6.0, k_peak=4.0)
dEdt=np.gradient(o['E'],o['t']); rel=np.abs((-dEdt[2:-2])-o['eps_nu'][2:-2])/o['eps_nu'][2:-2]
print(f"[2] Energy budget dE/dt = -eps_nu (NS identity):   {ok(rel.max()<1e-4)}  (max rel={rel.max():.1e})")
# 3 enstrophy monotone -> max eps_nu = 2 nu Z0
print(f"[3] Enstrophy monotone => max_eps proportional nu:  {ok((np.diff(o['Z'])<=1e-12).all())}")
# 4 metriplectic budget closure + saturation
b1=mv.steady(0.05); b2=mv.steady(0.0001)
print(f"[4] Metriplectic budget closes (eps_tot=I):        {ok(abs(b1['eps_tot']-0.21)<1e-9 and abs(b2['eps_tot']-0.21)<1e-9)}")
print(f"[5] Onsager saturation eps_bind->I as nu->0:       {ok(b2['eps_bind']>0.995*0.21 and b1['eps_nu']>b2['eps_nu'])}")
print("\nNote: rotcore RCCI metrics reproduce published tables to 1e-12 (see verify_rotcore.py).")
