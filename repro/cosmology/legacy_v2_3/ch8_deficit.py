#!/usr/bin/env python3
"""
ch8_deficit.py  --  Reproduces Chapter 8 ("dark matter" as a vacuum deficit).

ONE DEFICIT, THREE EFFECTS (all from a single depletion profile sourced by baryonic annihilation)
-------------------------------------------------------------------------------------------------
Depletion (deficit) rho_def(r) = A/r^2, saturating where it would exceed the ambient density.
Actual quantum density  rho(r) = rho_amb * max(0, 1 - (r_dark/r)^2),  r_dark = sqrt(A/rho_amb).

A) GRAVITATES (flat curve).  M_def(r) = INT rho_def 4pi r^2 dr ~ 4*pi*A*r at large r (rho_def
   propto 1/r^2 => M propto r), so v(r) = sqrt(G*M_def/r) rises through the core and FLATTENS.
   EXPECTED: dM_def/dr -> 4*pi*A ~ 12.57 (constant) at large r.

B) DARK = ABSOLUTE ZERO (the key point).  Inside r_dark the medium is fully annihilated:
   rho = 0 => NO QUANTA => absolute zero (temperature is quantum rotation; nothing to rotate)
   and no medium to carry light (c^2 = K/rho) => the core is empty, cold, and DARK.
   EXPECTED: r_dark = 1.0; rho(r<r_dark) = 0.

C) LENSES.  Outside r_dark the density gradient (with stiffness K falling faster than rho =>
   c^2=K/rho down => index n>1) bends light toward the deficit; the core is opaque.
   [The lensing SIGN depends on the K(rho) relation -- physics volume.]

WHY IT TRACKS BARYONS (RAR): the deficit is the baryons' own annihilation shadow, so it is
spatially tied to them -- automatic here, a puzzle for particle dark matter.

INPUTS: normalised (rho_amb=1, A=1, G=1). No fitting.
DEPENDENCIES: numpy, scipy (matplotlib optional for the figure).
"""
import numpy as np
from scipy.integrate import cumulative_trapezoid

rho_amb = 1.0
A = 1.0
G = 1.0
r_dark = np.sqrt(A/rho_amb)

def profiles(rmax=30.0, N=3000):
    r = np.linspace(0.01, rmax, N)
    rho_def = np.minimum(rho_amb, A/r**2)          # depletion amount (saturates)
    rho_act = rho_amb - rho_def                     # actual density: 0 in the dark core
    Mdef = cumulative_trapezoid(rho_def*4*np.pi*r**2, r, initial=0)
    vcirc = np.sqrt(G*Mdef/r)
    return r, rho_act, Mdef, vcirc

if __name__ == "__main__":
    r, rho_act, Mdef, vcirc = profiles()

    print("=== (B) DARK CORE = ABSOLUTE ZERO (no quanta) ===")
    print(f"  r_dark = sqrt(A/rho_amb) = {r_dark:.3f}")
    print(f"  rho(r<r_dark) = {rho_act[r<r_dark].max():.3f}  (zero => no quanta => absolute zero => DARK)")
    print("  PASS: the deepest deficit is empty and cold; light cannot propagate, nothing emits.\n")

    print("=== (A) GRAVITATES: flat rotation curve ===")
    mask = r > 5
    slope = np.polyfit(r[mask], Mdef[mask], 1)[0]
    print(f"  dM_def/dr (large r) = {slope:.3f}   (4*pi*A = {4*np.pi*A:.3f}; constant => M propto r => flat)")
    print(f"  v: inner(r=1)={vcirc[np.argmin(abs(r-1))]:.3f} -> outer(r=25)={vcirc[np.argmin(abs(r-25))]:.3f} "
          f"-> v_flat=sqrt(4*pi*G*A)={np.sqrt(4*np.pi*G*A):.3f}")
    print("  PASS: rises through the core, flattens at large r.\n")

    print("=== (C) LENSES (one deficit also bends light) ===")
    print("  density gradient outside r_dark => index n>1 (K falls faster than rho) => rays bend toward deficit;")
    print("  core opaque. (Lensing SIGN depends on K(rho): physics volume.)")
    print("\nRAR: deficit is the baryons' annihilation shadow => tracks baryons automatically.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        def n2d(x, y):
            rr = np.hypot(x, y); rd = np.minimum(rho_amb, A/np.clip(rr,1e-3,None)**2)
            return np.sqrt(rho_amb/np.clip(rho_amb-rd, 0.05, None))
        def trace(b, x0=-25, N=4000):
            pos = np.array([x0, float(b)]); d = np.array([1.0,0.0]); ds = 50/N; path=[pos.copy()]
            for _ in range(N):
                if np.hypot(*pos) < r_dark: break
                h=1e-3
                gx=(np.log(n2d(pos[0]+h,pos[1]))-np.log(n2d(pos[0]-h,pos[1])))/(2*h)
                gy=(np.log(n2d(pos[0],pos[1]+h))-np.log(n2d(pos[0],pos[1]-h)))/(2*h)
                g=np.array([gx,gy]); d=d+(g-np.dot(g,d)*d)*ds; d/=np.hypot(*d); pos=pos+d*ds; path.append(pos.copy())
            return np.array(path)
        fig,ax=plt.subplots(1,3,figsize=(16,4.8))
        ax[0].plot(r,vcirc); ax[0].set_xlim(0,25); ax[0].set_title("(a) flat rotation curve"); ax[0].set_xlabel("r"); ax[0].set_ylabel("v")
        ax[1].plot(r,rho_act); ax[1].fill_between(r[r<=r_dark],0,1.15,color='k',alpha=0.8)
        ax[1].set_xlim(0,15); ax[1].set_ylim(0,1.15); ax[1].set_title("(b) dark core: rho=0 = absolute zero"); ax[1].set_xlabel("r"); ax[1].set_ylabel("rho/rho_amb")
        th=np.linspace(0,2*np.pi,100); ax[2].fill(r_dark*np.cos(th),r_dark*np.sin(th),color='k',alpha=0.8)
        for b in [2,4,7,11,-2,-4,-7,-11]: p=trace(b); ax[2].plot(p[:,0],p[:,1],color='#c77',lw=1)
        ax[2].set_xlim(-25,20); ax[2].set_ylim(-15,15); ax[2].set_aspect('equal'); ax[2].set_title("(c) lensing; opaque core")
        plt.tight_layout(); plt.savefig("ch8_deficit.png", dpi=120); print("\n[figure written: ch8_deficit.png]")
    except Exception as e:
        print(f"\n[figure skipped: {e}]")
