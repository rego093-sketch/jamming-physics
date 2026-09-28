"""Production: for each (N,phi,seed) compute relaxed BULK B and relaxed SHEAR G on the
SAME packing. Resumable via CSV. Shows B finite while G->0 as z->6 (single speed c=√(B/ρ))."""
import numpy as np, csv, os, sys
from relaxed_shear import make_packing, mean_z, backbone_mask, relaxed_G
from bulk import relaxed_bulk

OUT = "results_bulk/bulkG.csv"
os.makedirs("results_bulk", exist_ok=True)
FIELDS = ["N","phi","seed","nbb","z","B_Born","B_relaxed","P","G_Born","G_relaxed",
          "c2_relaxed","rho","psdB","psdG","resB","resG","maxF"]

def done_keys():
    if not os.path.exists(OUT): return set()
    with open(OUT) as f:
        return {(r["N"],r["phi"],r["seed"]) for r in csv.DictReader(f)}

def append(row):
    new = not os.path.exists(OUT)
    with open(OUT,"a",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        if new: w.writeheader()
        w.writerow(row)

def run(N, phis, seeds, L=1.0):
    have=done_keys()
    for seed in seeds:
        for phi in phis:
            key=(str(N),f"{phi}",str(seed))
            if key in have: continue
            pos,R,E,mF = make_packing(N,phi,L,seed)
            keep = backbone_mask(pos,R,L); nbb=int(keep.sum())
            z = mean_z(pos,R,L,keep)
            rb = relaxed_bulk(pos,R,L,Ntot=N)
            rg = relaxed_G(pos,R,L)
            if not rb.get("ok") or not rg.get("ok"):
                print(f"N={N} phi={phi} seed={seed}: skip (bb small {nbb})"); 
                continue
            row=dict(N=N,phi=phi,seed=seed,nbb=nbb,z=f"{z:.4f}",
                     B_Born=f"{rb['B_Born']:.6e}",B_relaxed=f"{rb['B_relaxed']:.6e}",
                     P=f"{rb['P']:.4e}",G_Born=f"{rg['G_Born']:.6e}",G_relaxed=f"{rg['G_relaxed']:.6e}",
                     c2_relaxed=f"{rb['c2_relaxed']:.6e}",rho=f"{rb['rho']:.4f}",
                     psdB=int(rb['psd']),psdG=int(rg['psd']),
                     resB=f"{rb['lin_residual']:.1e}",resG=f"{rg['lin_residual']:.1e}",maxF=f"{mF:.1e}")
            append(row)
            print(f"N={N} phi={phi:.3f} seed={seed} z={z:.3f} nbb={nbb} "
                  f"B_rel={rb['B_relaxed']:.3e} G_rel={rg['G_relaxed']:.3e} "
                  f"c2={rb['c2_relaxed']:.3e} B/G={rb['B_relaxed']/max(rg['G_relaxed'],1e-30):.1f}")

if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 256
    phis=[0.636,0.640,0.645,0.652,0.660,0.672,0.686,0.700,0.720]
    s0=int(sys.argv[2]) if len(sys.argv)>2 else 0
    s1=int(sys.argv[3]) if len(sys.argv)>3 else 4
    run(N, phis, range(s0,s1))
    print("chunk done.")
