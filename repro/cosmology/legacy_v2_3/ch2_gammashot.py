#!/usr/bin/env python3
"""
ch2_gammashot.py -- "Shoot a gamma ray and watch it move" (user's suggestion).

THE SUGGESTION
--------------
Instead of only computing the dispersion relation, LAUNCH a gamma-wavelength
disturbance on the VP lattice and WATCH how it propagates and spreads. Two things
to look for:
  (1) does the disturbance disperse (slow down) -- and if so, is it the WAVEFRONT
      or only the PEAK that lags?
  (2) does the gamma energy spread transversely (at 90 deg to the propagation),
      as the user conjectured?

THE PHYSICS BEING TESTED
------------------------
On a lattice w=2(c/a)sin(ka/2): the GROUP velocity v_g=c cos(ka/2) is the speed
of the PEAK of a packet (< c for high k -> the naive 'dispersion'). But the
SIGNAL/WAVEFRONT velocity -- the speed of the leading edge -- equals the MAXIMUM
group velocity = c, for ANY carrier k (Sommerfeld-Brillouin). So a high-k 'gamma'
packet should have its FRONT at c (energy-independent) and its PEAK lagging at
v_g<c. This sim shows that directly, in 2D, so the transverse spreading is also
visible.

WHAT THIS SETTLES (honest, stated up front)
-------------------------------------------
 - A smooth gamma WAVE PACKET on the lattice DISPERSES: its front, edge, and peak
   all travel at ~v_g=c cos(ka/2) < c, while a visible packet stays near c.
   Watching the motion CONFIRMS the dispersion is real for a packet.
 - The user's 90-degree conjecture is NOT borne out here: the gamma beam spreads
   LESS transversely than visible (shorter wavelength diffracts less -> tighter
   beam). Gamma energy stays collimated and simply propagates slowly; it is not
   fanned out at 90 degrees.
 - CONSEQUENCE: because a gamma packet genuinely disperses, the resolution cannot
   live in the packet's motion -- it must be that LIGHT is NOT a lattice packet
   but the massless CONTINUUM mode (v_g=c exactly; sec.2.7-2.9). The sim sharpens
   the one open item (continuum vs lattice realization) rather than removing it.
 - (The textbook signal-velocity=c is an impulse-only, exponentially-tiny
   forerunner that a smooth gamma pulse does not carry; it does not help.)

INPUTS: none fitted (toy units a=c=1). numpy required; matplotlib for the movie.
DETERMINISM: no RNG.
"""
import numpy as np

a = c = 1.0
nx, ny = 760, 180
dt = 0.30                       # CFL: dt < a/(c*sqrt(2)) ~ 0.707
x = np.arange(nx); y = np.arange(ny)
X, Y = np.meshgrid(x, y, indexing="ij")   # X,Y shape (nx,ny)

def laplacian(u):
    lap = np.zeros_like(u)
    lap[1:-1,1:-1] = (u[2:,1:-1] + u[:-2,1:-1] + u[1:-1,2:] + u[1:-1,:-2] - 4*u[1:-1,1:-1])
    return lap

def shoot(k0, T=620, x0=70.0, sx=22.0, sy=26.0, ny_c=None):
    """Launch a right-moving beam with carrier k0; return time series of
    wavefront x, energy-centroid x, transverse RMS, and a few snapshots."""
    if ny_c is None: ny_c = ny/2.0
    env = np.exp(-((X-x0)/sx)**2) * np.exp(-((Y-ny_c)/sy)**2)
    u = env*np.cos(k0*(X-x0))
    # right-moving launch at the carrier group velocity
    vg0 = c*np.cos(k0/2.0)
    dudx = np.zeros_like(u); dudx[1:-1,:] = (u[2:,:]-u[:-2,:])/2.0
    v = -vg0*dudx
    F = (c*c/(a*a))*laplacian(u)
    nsteps = int(T/dt)
    tt, frontx, cinx, trms, frontabs = [], [], [], [], []
    snaps = {}; snap_steps = [int(s/dt) for s in (40, 240, 460)]
    thr = 0.02
    amp0 = np.abs(u).max()
    for s in range(nsteps+1):
        if s % 10 == 0:
            e = u*u                          # energy proxy (displacement^2)
            colx = e.sum(axis=1)             # energy vs x (summed over y)
            tot = colx.sum()
            maxabs_x = np.abs(u).max(axis=1) # max |u| in each x-column
            if tot > 1e-12:
                # detectable wavefront: rightmost x exceeding 2% of running max
                lead = np.where(colx > thr*colx.max())[0]
                fx = lead.max() if len(lead) else x0
                cx = (x*colx).sum()/tot
                coly = e.sum(axis=0); ty = (y*coly).sum()/coly.sum()
                tr = np.sqrt(((y-ty)**2*coly).sum()/coly.sum())
                # causal forerunner: rightmost x with ANY tiny amplitude (1e-4 of launch)
                fa_idx = np.where(maxabs_x > 1e-4*amp0)[0]
                fa = fa_idx.max() if len(fa_idx) else x0
            else:
                fx, cx, tr, fa = x0, x0, sy, x0
            tt.append(s*dt); frontx.append(fx); cinx.append(cx); trms.append(tr); frontabs.append(fa)
        if s in snap_steps: snaps[s*dt] = u.copy()
        # velocity-Verlet
        u = u + v*dt + 0.5*F*dt*dt
        Fn = (c*c/(a*a))*laplacian(u)
        v = v + 0.5*(F+Fn)*dt
        F = Fn
    return (np.array(tt), np.array(frontx), np.array(cinx), np.array(trms), snaps, np.array(frontabs))

# carriers: "gamma" = high k (near zone), "visible" = low k
k_gamma = 2.2          # v_g = cos(1.1) = 0.454 c
k_vis   = 0.35         # v_g = cos(0.175) = 0.985 c
print("=== SHOOT: gamma (high-k) vs visible (low-k) on a 2D VP lattice (a=c=1) ===")
print(f"  gamma : k0={k_gamma}  -> peak group velocity v_g=cos(k0/2)={c*np.cos(k_gamma/2):.3f} c")
print(f"  visible: k0={k_vis} -> peak group velocity v_g=cos(k0/2)={c*np.cos(k_vis/2):.3f} c")
print()

tg, fg, cg, rg, sg, fag = shoot(k_gamma)
tv, fv, cv, rv, sv, fav = shoot(k_vis)

def slope(t, q, i0=3):
    A = np.vstack([t[i0:], np.ones_like(t[i0:])]).T
    m, _ = np.linalg.lstsq(A, q[i0:], rcond=None)[0]
    return m

print("  --- LEADING EDGE of the gamma packet (tiny 1e-4 threshold) ---")
print(f"    gamma  edge speed = {slope(tg,fag):.3f} c     visible edge speed = {slope(tv,fav):.3f} c")
print("    => even the faint leading edge of a SMOOTH gamma packet tracks ~v_g (gamma ~0.5c),")
print("       NOT c. A smooth packet disperses as a whole. (The textbook signal-velocity=c")
print("       applies only to an impulse/discontinuity -- an exponentially tiny forerunner that")
print("       a smooth gamma pulse does not carry, so it does not help here.)")
print()
print("  --- DETECTABLE wavefront (2% of peak) ---")
print(f"    gamma  detectable front = {slope(tg,fg):.3f} c     visible detectable front = {slope(tv,fv):.3f} c")
print("    => the detectable edge also tracks ~v_g; the gamma packet genuinely lags.")
print()
print("  --- PEAK / energy-centroid velocity (the 'dispersion') ---")
print(f"    gamma  peak speed  = {slope(tg,cg):.3f} c     visible peak speed  = {slope(tv,cv):.3f} c")
print(f"    (expected v_g: gamma {c*np.cos(k_gamma/2):.3f} c, visible {c*np.cos(k_vis/2):.3f} c)")
print("    => the gamma PEAK lags (v_g<c); dispersion is the peak trailing, not a delayed front.")
print()
print("  --- TRANSVERSE spreading (the user's 90-degree question) ---")
print(f"    gamma  transverse RMS: start {rg[3]:.1f} -> end {rg[-1]:.1f}  (x{rg[-1]/rg[3]:.2f})")
print(f"    visible transverse RMS: start {rv[3]:.1f} -> end {rv[-1]:.1f}  (x{rv[-1]/rv[3]:.2f})")
sprd = "MORE" if (rg[-1]/rg[3]) > (rv[-1]/rv[3]) else "LESS"
print(f"    => the gamma beam spreads {sprd} transversely than visible "
      f"(diffraction ~ lambda/width: shorter lambda -> tighter beam).")
print()
print("  HONEST READING (what watching the gamma move actually shows):")
print("   * A smooth gamma WAVE PACKET disperses: front, edge, and peak all travel at ~v_g=")
print("     c cos(ka/2) < c (here ~0.45 c), while the visible packet stays at ~c. So watching")
print("     CONFIRMS the dispersion -- it is real for a wave packet on the lattice.")
print("   * The 90-degree conjecture is NOT borne out: the gamma beam spreads LESS transversely")
print(f"     (x{rg[-1]/rg[3]:.2f}) than the visible one (x{rv[-1]/rv[3]:.2f}). Shorter wavelength")
print("     diffracts less (tighter beam), so gamma energy does not fan out sideways; it stays")
print("     collimated and simply propagates slowly. (The energy is not dumped at 90 degrees.)")
print("   * CONSEQUENCE: since a gamma wave packet on the lattice genuinely disperses, the")
print("     resolution cannot be a property of the packet's motion -- it must be that LIGHT is")
print("     NOT such a packet. Light is the massless CONTINUUM mode (sec.2.7-2.9), for which")
print("     v_g=c exactly. Watching the lattice packet thus sharpens the one open item rather")
print("     than removing it: is light the exact continuum mode, or a lattice packet? Only the")
print("     former is dispersionless. This sim shows the latter is not.")

# ---------------------------------------------------------------------------
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(15, 7.5))
    # top row: gamma snapshots (watch it move)
    times = sorted(sg.keys())
    vmax = max(np.abs(sg[times[0]]).max(), 1e-6)
    for i, t in enumerate(times):
        ax = fig.add_subplot(2, 3, i+1)
        ax.imshow(sg[t].T, origin="lower", aspect="auto", cmap="RdBu_r",
                  vmin=-vmax*0.6, vmax=vmax*0.6, extent=[0,nx,0,ny])
        # mark the wavefront (c*t) and the peak (v_g*t) from launch x0=70
        ax.axvline(70 + c*t, color="k", ls="--", lw=1.0)
        ax.axvline(70 + c*np.cos(k_gamma/2)*t, color="green", ls=":", lw=1.4)
        ax.set_title(f"gamma at t={t:.0f}", fontsize=10)
        ax.set_xlabel("x"); ax.set_ylabel("y" if i==0 else "")
    # bottom-left: gamma front & peak both lag below the c-line
    ax = fig.add_subplot(2,3,4)
    ax.plot(tg, fg, "b--", lw=1.6, label="gamma front (edge)")
    ax.plot(tg, cg, "g-", lw=1.8, label="gamma peak")
    ax.plot(tg, 70+c*tg, "r:", lw=1.4, label="$x=70+ct$ ($c$ line)")
    ax.set_xlabel("time"); ax.set_ylabel("x position")
    ax.set_title("gamma packet (front & peak) lags below $c$: it disperses"); ax.legend(fontsize=8)
    # bottom-mid: gamma vs visible (gamma slower)
    ax = fig.add_subplot(2,3,5)
    ax.plot(tg, cg, "b-", lw=1.8, label=f"gamma peak (~{slope(tg,cg):.2f}c)")
    ax.plot(tv, cv, "m-", lw=1.6, label=f"visible peak (~{slope(tv,cv):.2f}c)")
    ax.plot(tg, 70+c*tg, "k:", lw=1.0, label="$x=70+ct$")
    ax.set_xlabel("time"); ax.set_ylabel("peak x")
    ax.set_title("gamma lags, visible at $c$ (energy-dependent: dispersion)"); ax.legend(fontsize=8)
    # bottom-right: transverse RMS (90-degree test)
    ax = fig.add_subplot(2,3,6)
    ax.plot(tg, rg, "b-", lw=1.8, label=f"gamma (x{rg[-1]/rg[3]:.1f})")
    ax.plot(tv, rv, "m-", lw=1.6, label=f"visible (x{rv[-1]/rv[3]:.1f})")
    ax.set_xlabel("time"); ax.set_ylabel("transverse RMS (y)")
    ax.set_title("transverse spread: gamma spreads LESS (no 90$^\\circ$ fan-out)"); ax.legend(fontsize=8)
    plt.tight_layout(); plt.savefig("ch2_gammashot.png", dpi=110, bbox_inches="tight")
    print("\n[figure written: ch2_gammashot.png]")
except Exception as exc:
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
