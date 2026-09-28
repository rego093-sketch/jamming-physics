#!/usr/bin/env python3
"""
ch8_bullet.py  --  Chapter 8, colliding-cluster offset from DEFICIT RELAXATION.

WHAT THIS DEMONSTRATES (and what it does NOT)
---------------------------------------------
The deficit picture (Ch.8; cosmos-volume PART 09, "Deficit Gravity & Lattice
Refraction") must face the sharpest challenge to any non-particle account of the
mass discrepancy: merging clusters (the "Bullet Cluster" class) in which the
gravitational-lensing mass peak is OFFSET from the X-ray gas peak.

PART 09 (sec.9.4) gives a *minimal transport model* for the deficit field
Delta(x,t) and states the separation conditions exactly:

    d_t Delta + div( Delta*u_Delta - D_Delta*grad Delta ) = (1/tau_Delta)(Delta_eq - Delta)

    (C1) slow relaxation     : tau_Delta  >> tau_coll
    (C2) small diffusion      : sqrt(D_Delta*tau_coll) << L_off
    (C3) advection tracks the COLLISIONLESS galaxies, not the shocked gas:
                                ||u_Delta - u_gal|| << ||u_gal - u_gas||

Separation of the lensing peak (Sigma_eff = Sigma_baryon + Sigma_def) from the
gas peak (Sigma_gas) occurs when, during the merger, the deficit stays with the
collisionless galaxies (C3) and is too slow to reattach to the shocked gas (C1).

This script implements that transport equation for a "bullet" subcluster passing
through a larger cluster and MEASURES the lensing-vs-gas centroid offset shortly
after pericentre, as a function of tau_Delta/tau_coll. It shows:
  * tau_Delta >> tau_coll  -> lensing peak sits on the galaxies -> LARGE offset
                              (same phenomenology as collisionless dark matter);
  * tau_Delta << tau_coll  -> deficit reattaches to the (gas-dominated) baryons
                              -> offset COLLAPSES to the small stellar-baryon floor
                              (the MOND-like failure mode).

HONEST SCOPE  (this is a MECHANISM demo, not a fit):
  - units are normalised/toy (length in model units ~ Mpc, time in crossing
    times); we do NOT input real cluster masses, velocities or weak-lensing maps;
  - therefore we do NOT predict the observed ~0.2 Mpc offset of any real system;
  - the EXISTENCE of the offset is DEGENERATE with collisionless dark matter
    (both produce it by the same "collisionless-during-merger" logic). The
    quantitative cluster gate of PART 09 sec.9.6 (chi^2 against real lensing+X-ray)
    is NOT run here and remains OPEN.
  - A potential *discriminator* is that finite tau_Delta predicts slow post-merger
    REATTACHMENT of the lensing peak toward the gas, whereas collisionless dark
    matter never reattaches. Flagged, not tested.

Realistic-ish fractions are used so the demo is not rigged:
  gas dominates the BARYONS (f_gas = 0.85) and the deficit dominates the TOTAL
  mass (M_def : M_baryon = 5 : 1), as in observed clusters. With those choices the
  offset floor for fast relaxation is the small stellar fraction f_gal*L_off, and
  the ceiling for slow relaxation is ~ (R_def + f_gal)/(R_def + 1) * L_off (the gas
  baryons still sit on the gas), so a large offset is a genuine consequence of
  C1-C3, not of the weighting.

INPUTS: none fitted. DEPENDENCIES: numpy, scipy (matplotlib optional).
DETERMINISM: no RNG.
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid  # (np.trapz is removed in this env)

# ----------------------------------------------------------------------
# parameters (toy / normalised)
# ----------------------------------------------------------------------
v0       = 1.0            # collisionless (galaxy) bulk speed, +x  [model units]
t_c      = 3.0            # time of core passage
tau_coll = 0.8            # collision duration  == drag-pulse width (defines C1)
gamma0   = 1.10           # peak ram-pressure drag rate on the gas during passage
t_obs    = t_c + 1.2*tau_coll   # "observation" time: shortly after pericentre

f_gas    = 0.85           # gas fraction of the BARYONS (clusters: gas >> stars)
f_gal    = 1.0 - f_gas    # galaxy/stellar fraction of the baryons
R_defbar = 5.0            # deficit : baryon mass ratio (clusters are mass-dominated
                          #           by the "dark"/deficit component)

sig_g    = 0.50           # galaxy clump width
sig_s    = 0.60           # gas clump width
sig_d    = 0.50           # initial deficit width
D_Delta  = 0.002          # deficit diffusivity (kept small => C2 satisfied)

# grid / time stepping
xL, xR, N = -2.0, 10.0, 1500
x  = np.linspace(xL, xR, N)
dx = x[1] - x[0]
T  = 6.0
dt = 0.002
nt = int(round(T/dt))
k_obs = int(round(t_obs/dt))

def gaussian(xx, mu, sig):
    g = np.exp(-0.5*((xx-mu)/sig)**2)
    return g/np.trapezoid(g, xx)               # unit-area kernel

def centroid(field):
    return np.trapezoid(x*field, x)/np.trapezoid(field, x)

# ----------------------------------------------------------------------
# galaxy (collisionless) and gas (collisional) kinematics
# ----------------------------------------------------------------------
def galaxy_x(t):                               # ballistic: u_gal = v0  (C3 reference)
    return v0 * t

def gas_track():
    """Integrate the gas centroid with a ram-pressure drag PULSE during passage."""
    xs = np.zeros(nt+1); vs = np.zeros(nt+1)
    xs[0], vs[0] = 0.0, v0
    for k in range(nt):
        t = k*dt
        gamma = gamma0*np.exp(-((t - t_c)/tau_coll)**2)     # drag only near passage
        vs[k+1] = vs[k] - dt*gamma*vs[k]
        xs[k+1] = xs[k] + dt*vs[k+1]
    return xs, vs

xs_arr, vs_arr = gas_track()

# galaxy-gas separation at the observation time (the natural offset scale L_off)
L_off = galaxy_x(t_obs) - xs_arr[k_obs]

# ----------------------------------------------------------------------
# evolve the deficit transport PDE for a given tau_Delta
#   d_t D = -v0 * d_x D  (advect with galaxies, C3 with u_Delta=u_gal=v0)
#           + D_Delta d_xx D                       (diffusion, C2)
#           + (1/tau)(D_eq - D)                     (relaxation toward baryons, C1)
# Sigma_eff = rho_gal + rho_gas + Delta  (deficit normalised to R_defbar*baryons)
# ----------------------------------------------------------------------
def run(tau_Delta, record=False):
    Delta = R_defbar * gaussian(x, 0.0, sig_d)          # total deficit mass = R_defbar
    Mdef  = np.trapezoid(Delta, x)

    off_t = np.zeros(nt+1)
    snaps = {}
    for k in range(nt+1):
        t  = k*dt
        xg = galaxy_x(t)
        xs = xs_arr[k]
        rho_gal = f_gal * gaussian(x, xg, sig_g)         # baryon mass = f_gal
        rho_gas = f_gas * gaussian(x, xs, sig_s)         # baryon mass = f_gas
        rho_bar = rho_gal + rho_gas
        Delta_eq = Mdef * rho_bar / np.trapezoid(rho_bar, x)   # target: track baryons

        Sigma_eff = rho_bar + Delta                      # lensing convergence proxy
        x_lens = centroid(Sigma_eff)
        x_gas  = centroid(rho_gas)
        off_t[k] = x_lens - x_gas

        if record and k == k_obs:
            snaps = dict(rho_gal=rho_gal.copy(), rho_gas=rho_gas.copy(),
                         Sigma_eff=Sigma_eff.copy(), x_lens=x_lens, x_gas=x_gas,
                         x_gal=centroid(rho_gal))
        if k == nt:
            break
        # --- explicit step of the transport PDE (upwind advection, u=v0>0) ---
        adv = v0*(Delta - np.roll(Delta, 1))/dx          # upwind d_x(Delta*v0)
        adv[0] = 0.0
        lap = (np.roll(Delta, -1) - 2*Delta + np.roll(Delta, 1))/dx**2
        lap[0] = lap[-1] = 0.0
        Delta = Delta + dt*(-adv + D_Delta*lap + (Delta_eq - Delta)/tau_Delta)
        Delta = np.clip(Delta, 0.0, None)                # deficit Delta >= 0
        Delta[0] = Delta[-1] = 0.0

    return off_t, off_t[k_obs], snaps

# ----------------------------------------------------------------------
# main: two reference cases + a tau_Delta/tau_coll sweep
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tarr = np.arange(nt+1)*dt

    off_slow_t, off_slow, snap_slow = run(5.0*tau_coll, record=True)   # C1 satisfied
    off_fast_t, off_fast, _         = run(0.1*tau_coll, record=False)  # C1 violated

    ratios = np.array([0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.5, 5.0, 10.0, 20.0])
    off_final = np.array([run(r*tau_coll)[1] for r in ratios])

    diff_scale = np.sqrt(D_Delta*tau_coll)
    floor = f_gal                                        # offset/L_off floor (fast relax)
    ceil  = (R_defbar + f_gal)/(R_defbar + 1.0)          # offset/L_off ceiling (slow relax)

    print("=== colliding-cluster offset from deficit relaxation (PART 09 sec.9.4) ===")
    print(f"  collision duration tau_coll = {tau_coll};  observation time t_obs = {t_obs:.2f}")
    print(f"  galaxy-gas separation at t_obs  L_off = {L_off:.3f}  (offset scale)")
    print(f"  diffusion length sqrt(D*tau_coll) = {diff_scale:.4f}"
          f"  => sqrt(D*tau_coll)/L_off = {diff_scale/L_off:.4f}  "
          f"(<<1 => C2 small-diffusion PASS)")
    print(f"  analytic offset/L_off  floor (fast) = f_gal = {floor:.2f},  "
          f"ceiling (slow) = (R_def+f_gal)/(R_def+1) = {ceil:.2f}\n")

    print("  (C1) SLOW relaxation  tau_Delta/tau_coll = 5.0 :")
    print(f"        offset at t_obs = {off_slow:.3f}  "
          f"(= {off_slow/L_off:.2f} x L_off)  -> lensing tracks GALAXIES "
          f"=> LARGE offset (collisionless-DM-like)")
    print("  (C1) FAST relaxation  tau_Delta/tau_coll = 0.1 :")
    print(f"        offset at t_obs = {off_fast:.3f}  "
          f"(= {off_fast/L_off:.2f} x L_off)  -> deficit reattaches to GAS "
          f"=> offset COLLAPSES toward stellar floor\n")

    print("  sweep tau_Delta/tau_coll -> normalised offset (offset / L_off):")
    for r, o in zip(ratios, off_final):
        flag = "PASS(sep)" if o/L_off > 0.5*(floor+ceil) else "no-sep"
        print(f"     tau_Delta/tau_coll = {r:5.2f}  ->  {o/L_off:4.2f}   {flag}")
    print(f"\n  EXPECTED: offset/L_off rises from ~{floor:.2f} (lensing on gas) to "
          f"~{ceil:.2f} (lensing on galaxies)")
    print("            as tau_Delta/tau_coll grows; transition near tau_Delta/tau_coll ~ 1 (= C1).")
    print("  SCOPE: mechanism demonstrated; NOT a quantitative fit to any real cluster")
    print("         (PART 09 sec.9.6 data gate is open). Offset existence is DEGENERATE")
    print("         with collisionless dark matter.\n")

    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 3, figsize=(16, 4.8))

        # (a) post-passage profiles for the slow-relaxation (C1-satisfied) case
        s = snap_slow
        ax[0].plot(x, s["rho_gal"]/s["rho_gal"].max(), color="tab:blue",
                   label="galaxies (collisionless)")
        ax[0].plot(x, s["rho_gas"]/s["rho_gas"].max(), color="tab:red",
                   label="gas (X-ray, shocked)")
        ax[0].plot(x, s["Sigma_eff"]/s["Sigma_eff"].max(), color="black", lw=2,
                   label=r"lensing $\Sigma_{\rm eff}=\Sigma_b+\Sigma_{\rm def}$")
        ax[0].axvline(s["x_gas"],  color="tab:red",  ls=":", lw=1)
        ax[0].axvline(s["x_lens"], color="black",    ls=":", lw=1)
        ax[0].annotate("", xy=(s["x_lens"], 0.5), xytext=(s["x_gas"], 0.5),
                       arrowprops=dict(arrowstyle="<->", color="dimgray"))
        ax[0].text((s["x_lens"]+s["x_gas"])/2, 0.55,
                   f"offset\n{s['x_lens']-s['x_gas']:.2f}", ha="center",
                   va="bottom", color="dimgray", fontsize=9)
        ax[0].set_xlim(0, 9); ax[0].set_xlabel("x  [model units ~ Mpc]")
        ax[0].set_ylabel("normalised surface density")
        ax[0].set_title(r"(a) just after passage ($\tau_\Delta=5\,\tau_{\rm coll}$): lensing leads gas")
        ax[0].legend(fontsize=8, loc="upper left")

        # (b) offset(t): slow vs fast relaxation
        ax[1].plot(tarr, off_slow_t, color="tab:green",
                   label=r"$\tau_\Delta=5\,\tau_{\rm coll}$ (C1 ok): persists")
        ax[1].plot(tarr, off_fast_t, color="tab:orange",
                   label=r"$\tau_\Delta=0.1\,\tau_{\rm coll}$ (C1 fails): collapses")
        ax[1].axvspan(t_c-tau_coll, t_c+tau_coll, color="gray", alpha=0.15)
        ax[1].axvline(t_obs, color="k", ls="--", lw=0.8)
        ax[1].text(t_c, ax[1].get_ylim()[1]*0.05, "passage", ha="center",
                   fontsize=8, color="gray")
        ax[1].text(t_obs+0.05, ax[1].get_ylim()[1]*0.9, r"$t_{\rm obs}$", fontsize=8)
        ax[1].axhline(0, color="k", lw=0.6)
        ax[1].set_xlabel("time  [crossing times]")
        ax[1].set_ylabel("lensing $-$ gas centroid offset")
        ax[1].set_title("(b) offset history: only slow relaxation keeps it")
        ax[1].legend(fontsize=8, loc="upper left")

        # (c) sweep: offset at t_obs vs tau_Delta/tau_coll
        ax[2].plot(ratios, off_final/L_off, "o-", color="tab:purple")
        ax[2].axvline(1.0, color="gray", ls="--", lw=1)
        ax[2].text(1.1, 0.12, r"$\tau_\Delta\sim\tau_{\rm coll}$", color="gray", fontsize=9)
        ax[2].axhline(floor, color="tab:red", ls=":", lw=1)
        ax[2].text(0.06, floor+0.02, "stellar-baryon floor", color="tab:red", fontsize=8)
        ax[2].axhline(ceil, color="tab:blue", ls=":", lw=1)
        ax[2].text(0.06, ceil-0.06, "lensing-on-galaxies", color="tab:blue", fontsize=8)
        ax[2].axhspan(0.5*(floor+ceil), 1.0, color="tab:green", alpha=0.08)
        ax[2].set_xscale("log")
        ax[2].set_ylim(0.0, 1.0)
        ax[2].set_xlabel(r"$\tau_\Delta/\tau_{\rm coll}$  (relaxation vs collision time)")
        ax[2].set_ylabel(r"offset at $t_{\rm obs}$ / $L_{\rm off}$")
        ax[2].set_title(r"(c) separation gate (C1): offset turns on for $\tau_\Delta\gg\tau_{\rm coll}$")

        plt.tight_layout()
        plt.savefig("ch8_bullet.png", dpi=120)
        print("[figure written: ch8_bullet.png]")
    except Exception as e:
        print(f"[figure skipped: {e}]")
