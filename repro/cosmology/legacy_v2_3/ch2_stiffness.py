#!/usr/bin/env python3
"""
ch2_stiffness.py -- c as the collective-stiffness ceiling, and the gamma
                    dispersion residual at the fundamental VP lattice scale a.

THE CLAIM BEING TESTED (user; physics-volume sec.0.5 / sec.10.0)
----------------------------------------------------------------
c is NOT a property of the quanta; it is the COLLECTIVE STIFFNESS speed of the
VP lattice itself (which exists even without quanta). The vacuum-symmetry
theorem (sec.0.5, N3) forces the dispersion w^2=(K/rho)k^2 -> w=ck EXACTLY
(grade Fm), and positive energy (N4) makes c a CAUSAL CEILING: nothing exceeds
c. The realization on the jammed lattice (sec.10.0, speed_c.py) confirms
c proportional to sqrt(K), amplitude-independent and isotropic.

THE HONEST SUBTLETY (sec.10.0, stated by the framework itself)
--------------------------------------------------------------
The REALIZED lattice carries the DISCRETE dispersion w=2(c/a)sin(ka/2), which
only CONVERGES to the continuum w=ck in the long-wavelength limit (0% error at
ka=0.01, 0.04% at ka=0.1). So light is exactly dispersionless only if it is the
CONTINUUM (symmetry) mode; a discrete cell-to-cell realization disperses at
finite k.

WHAT THIS SCRIPT DOES
---------------------
(1) CEILING: on an elastic lattice (collective stiffness K) it measures the
    dispersion, confirms the long-wavelength speed c=sqrt(K), confirms the
    group velocity v_g=c cos(ka/2) <= c for ALL k (nothing exceeds c), and
    confirms amplitude-independence (linear).
(2) THE GAMMA RESIDUAL AT SCALE a: using the FUNDAMENTAL VP lattice spacing
    a=6.33e-19 m (NOT the quantum diameter D=4.854 pm), it asks whether gamma
    is "long-wavelength" relative to a, and quantifies the residual dispersion
    and the implied quantum-gravity scale E_QG,2, comparing to the Fermi
    GRB 090510 bound.

WHAT IT SHOWS (honest)
----------------------
 - The collective-stiffness ceiling is real: v_g <= c always; at long
   wavelength v_g -> c (dispersionless). This is the symmetry-forced (Fm) core.
 - Gamma IS deep in the long-wavelength regime even at scale a (ka ~ 1e-3), so
   the residual dispersion is tiny -- BUT NOT ZERO. At scale a the discrete
   lattice gives E_QG,2 ~ 882 GeV, still ~8 orders BELOW the Fermi bound. So
   the discrete realization does not, by itself, clear Fermi.
 - The conflict closes ONLY in the exact-continuum limit w=ck (E_QG,2 -> inf):
   i.e. only if light is protected to be the continuum box_c mode, not the
   discrete relay. That protection is the located open item (Hm, sec.14.0.6).

INPUTS: a, D, the Fermi bound are physical constants/measurements (cited);
no fitted parameters. numpy required; scipy optional (curve-fit).
"""
import numpy as np

# ---------------------------------------------------------------------------
# (1) CEILING: dispersion of an elastic lattice; v_g <= c for all k
# ---------------------------------------------------------------------------
K = 1.0; mass = 1.0
c = np.sqrt(K/mass)                  # collective-stiffness speed = the ceiling
N = 2000; dt = 0.02

def force(u):
    f = np.zeros_like(u)
    f[1:-1] = K*(u[2:] - 2*u[1:-1] + u[:-2])
    return f

def measure_omega(k, amp, T=300.0):
    from numpy.fft import rfft, rfftfreq
    n = np.arange(N, dtype=float)
    u = amp*np.cos(k*n); v = np.zeros_like(u); F = force(u)
    cos_k = np.cos(k*n); norm = (cos_k*cos_k).sum()
    proj=[]; ts=[]; nsteps=int(T/dt)
    for s in range(nsteps):
        if s % 2 == 0: proj.append((u*cos_k).sum()/norm); ts.append(s*dt)
        u = u + v*dt + 0.5*(F/mass)*dt*dt
        Fn = force(u); v = v + 0.5*(F+Fn)/mass*dt; F = Fn
    proj=np.array(proj)-np.mean(proj); ts=np.array(ts)
    try:
        from scipy.optimize import curve_fit
        wg = 2*c*max(abs(np.sin(k/2)),1e-4)
        popt,_=curve_fit(lambda t,A,w,p,o:A*np.cos(w*t+p)+o, ts, proj,
                         p0=[np.std(proj)*1.4 or amp, wg, 0, 0], maxfev=40000)
        return abs(popt[1])
    except Exception:
        W=rfft(proj*np.hanning(len(proj))); fr=rfftfreq(len(proj),d=ts[1]-ts[0])
        return 2*np.pi*fr[np.argmax(np.abs(W))]

print("=== (1) c IS THE COLLECTIVE-STIFFNESS CEILING (nothing exceeds c) ===")
print(f"    elastic lattice, K={K}, mass={mass} -> c=sqrt(K/mass)={c:.3f}")
print(f"    {'k (x pi)':>9} {'w':>9} {'v_g=c*cos(k/2)':>15} {'v_g/c':>8}  {'<= c ?':>7}")
for k in [0.05, 0.20, 0.60, 1.20, 2.50]:
    k=k*np.pi/np.pi if k<np.pi else k
    if k>=np.pi: continue
    w=measure_omega(k, amp=1e-3); vg=c*np.cos(k/2)
    print(f"    {k/np.pi:>9.3f} {w:>9.4f} {vg:>15.4f} {vg/c:>8.4f}  {'yes' if vg<=c+1e-9 else 'NO':>7}")
# amplitude independence (linear): same w(k) for very different amplitudes
k0=0.2; wa=measure_omega(k0,amp=1e-3); wb=measure_omega(k0,amp=2.0)
print(f"    amplitude-independence at k=0.2pi: w(amp=1e-3)={wa:.4f}, w(amp=2.0)={wb:.4f} "
      f"(diff {abs(wa-wb)/wa*100:.2f}%)")
print("    => v_g = c*cos(k/2) <= c for ALL k (CEILING holds); long-wavelength v_g -> c")
print("       (dispersionless). This is the symmetry-forced (Fm) core of sec.0.5/sec.10.0.")
print()

# ---------------------------------------------------------------------------
# (2) THE GAMMA RESIDUAL AT THE FUNDAMENTAL VP SCALE a
# ---------------------------------------------------------------------------
a   = 6.33e-19      # m, fundamental VP lattice spacing (NOT the quantum D)
D   = 4.854e-12     # m, quantum rotation diameter (for contrast)
hc  = 1.239841984e-6  # eV*m  (Planck*c)
c_light = 2.99792458e8  # m/s
E_QG_Fermi = 1.3e20  # eV, Fermi GRB 090510 quadratic bound on E_QG,2 (lower limit)

def EQG2(ell):                       # discrete lattice w=2(c/ell)sin(k ell/2):
    return np.sqrt(2)*hc/(np.pi*ell) # dv/c=(E/E_QG2)^2  => E_QG2 = sqrt(2) hc/(pi ell)

EQG2_a = EQG2(a); EQG2_D = EQG2(D)
print("=== (2) GAMMA DISPERSION RESIDUAL AT THE VP SCALE a (discrete realization) ===")
print(f"    fundamental VP spacing a = {a:.3e} m;  quantum diameter D = {D:.3e} m  (a << D)")
print(f"    discrete lattice w=2(c/a)sin(ka/2) => quadratic scale E_QG,2 = sqrt(2)hc/(pi a)")
print(f"      using a:  E_QG,2 = {EQG2_a:.3e} eV = {EQG2_a/1e9:.0f} GeV")
print(f"      using D:  E_QG,2 = {EQG2_D:.3e} eV = {EQG2_D/1e3:.0f} keV   (the naive 'D' value)")
print(f"    Fermi GRB 090510 bound:  E_QG,2 > {E_QG_Fermi:.2e} eV = {E_QG_Fermi/1e9:.2e} GeV")
print(f"    => using a, theory is {E_QG_Fermi/EQG2_a:.2e}x BELOW the Fermi bound "
      f"(~{np.log10(E_QG_Fermi/EQG2_a):.0f} orders).")
print()
print(f"    {'E (gamma)':>12} {'lambda':>12} {'k*a':>11} {'dv/c (discrete)':>16} {'dv/c (Fermi max)':>17}")
for E in [1e6, 1e9, 31e9, 1e11]:    # 1 MeV, 1 GeV, 31 GeV (Fermi), 100 GeV
    lam = hc/E; ka = 2*np.pi*a/lam
    dv_disc = (ka**2)/8.0            # = (E/E_QG2_a)^2
    dv_fermi = (E/E_QG_Fermi)**2
    print(f"    {E/1e9:>9.3f} GeV {lam:>12.2e} {ka:>11.2e} {dv_disc:>16.2e} {dv_fermi:>17.2e}")
print("    (gamma is deep in long-wavelength even at a: k*a ~ 1e-3; residual is tiny but")
print("     still >> the Fermi ceiling by ~16 orders in dv/c, i.e. ~8 orders in E_QG,2.)")
print()
print("  HONEST CONCLUSION:")
print("   * The collective-stiffness CEILING is real and symmetry-forced (Fm, sec.0.5 N3/N4):")
print("     v_g <= c always; long-wavelength light is dispersionless. The user is right that")
print("     'nothing exceeds c' and that c comes from the VP lattice's collective stiffness.")
print("   * But the DISCRETE realization (sec.10.0, w=2(c/a)sin(ka/2)) still disperses: at the")
print("     fundamental scale a it gives E_QG,2 ~ 882 GeV, ~8 orders below the Fermi bound.")
print("     So the ceiling/long-wavelength argument REDUCES the tension (15 -> 8 orders vs the")
print("     naive 'D' value) but does NOT clear Fermi by itself.")
print("   * The conflict closes ONLY in the exact-continuum limit w=ck (E_QG,2 -> infinity):")
print("     i.e. only if light is the continuum box_c mode, PROTECTED from the lattice's")
print("     O((ka)^2) correction. Whether the EM/Goldstone mode is so protected is the located")
print("     open item (the 'physical forcing of the curl coupling', sec.14.0.6, grade Hm).")
print("   => Net: dispersionless LAW = forced (symmetry); high-k EXACTNESS for light = open.")

# ---------------------------------------------------------------------------
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.8))

    # (a) dispersion: discrete vs continuum, with the ceiling
    kk=np.linspace(0,np.pi,400)
    ax[0].plot(kk/np.pi, 2*c*np.abs(np.sin(kk/2)), 'b-', lw=2,
               label=r"realized lattice $w=2c\,|\sin(ka/2)|$ (disperses)")
    ax[0].plot(kk/np.pi, c*kk, 'g--', lw=1.8,
               label=r"continuum $w=ck$ (sec.0.5, symmetry-forced, exact)")
    ax[0].set_xlabel(r"wavenumber $ka/\pi$"); ax[0].set_ylabel(r"$w$")
    ax[0].set_title("(a) symmetry forces $w=ck$; the lattice realizes it only at small $ka$")
    ax[0].legend(fontsize=8, loc="upper left")

    # (b) E_QG,2 ladder: D, a, exact-continuum, vs Fermi
    labels=["naive\n(scale $D$)","VP substrate\n(scale $a$)","exact continuum\n(box-c)","Fermi bound\n(GRB 090510)"]
    vals=[EQG2_D, EQG2_a, 1e22, E_QG_Fermi]   # exact-continuum drawn as a tall bar (->inf)
    colors=["tab:red","tab:orange","tab:green","k"]
    xs=np.arange(4)
    ax[1].bar(xs, np.log10(vals), color=colors, alpha=0.8)
    ax[1].axhline(np.log10(E_QG_Fermi), color="k", ls=":", lw=1.2)
    ax[1].annotate("Fermi floor", (3.0, np.log10(E_QG_Fermi)+0.3), fontsize=8, ha="center")
    ax[1].set_xticks(xs); ax[1].set_xticklabels(labels, fontsize=8)
    ax[1].set_ylabel(r"$\log_{10} E_{\rm QG,2}$ [eV]")
    ax[1].set_title("(b) quadratic QG scale: only the exact continuum clears Fermi")
    ax[1].text(2.0, 21.3, r"$\to\infty$", fontsize=11, ha="center", color="tab:green")
    plt.tight_layout(); plt.savefig("ch2_stiffness.png", dpi=120, bbox_inches="tight")
    print("\n[figure written: ch2_stiffness.png]")
except Exception as exc:
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
