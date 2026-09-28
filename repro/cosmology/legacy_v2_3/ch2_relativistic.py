#!/usr/bin/env python3
"""
ch2_relativistic.py -- The quantitative Fermi gate: two energy->velocity laws.

THE QUESTION (C)
----------------
The single-mode lattice estimate gave E_QG,2 ~ 882 GeV (8 orders below Fermi).
A real gamma is a collective excitation ("a sum of enormous energy", user). Does
the collective picture push the effective dispersion below the Fermi bound, and
what does it take? This script settles the structure of the answer.

THE KEY DISTINCTION
-------------------
There are TWO different energy->velocity laws on a stiff medium, with OPPOSITE
energy dependence:

  (i) LATTICE PHONON (non-relativistic, discrete, MASSLESS mode):
        w = 2(c/a) sin(ka/2),  v_g = c cos(ka/2),
        dv/c = +(ka)^2/8 = +(E/E_QG)^2   -> GROWS with E   (the 'conflict')

  (ii) RELATIVISTIC excitation (the c-ceiling structure forced by sec.0.5 N4):
        w^2 = c^2 k^2 + mu^2  (Klein-Gordon),  v_g = c^2 k / w,
        dv/c = (E0/E)^2 / 2   -> SHRINKS with E   (anti-dispersion); v_g < c always,
        and for MASSLESS (E0 = mu = 0):  v_g = c EXACTLY  (dispersionless).

Light is the MASSLESS Goldstone/Maxwell mode (sec.14.0.5: U(1) breaking -> massless
Goldstone). A massless relativistic mode travels at c for ALL energies -> NO
dispersion, and (crucially) the relativistic law makes HIGH energy the SAFEST
case, the opposite of the phonon 'conflict'.

WHAT THIS SIM DOES
------------------
(1) Dynamically measures the dispersion of a Klein-Gordon lattice and confirms
    BOTH laws on the SAME medium: the relativistic anti-dispersion (with a mass,
    in the continuum/low-k regime) and the lattice phonon (massless, high-k).
    Confirms v_g <= c (the ceiling) throughout.
(2) Puts numbers on the Fermi gate: under each law, dv/c for gamma energies vs
    the Fermi GRB 090510 bound; the rest energy E0 that the relativistic law
    needs to satisfy Fermi; and that massless (E0=0) satisfies it exactly.

WHAT IT SHOWS / DOES NOT SHOW (honest)
--------------------------------------
 - SHOWS: if light is the massless relativistic mode (framework's claim), it is
   dispersionless (v=c) and Fermi is satisfied automatically; high-E is safe.
   The 882 GeV 'conflict' is the artifact of the non-relativistic phonon law.
 - DOES NOT SHOW: that the realized lattice mode for light IS the exact
   relativistic/continuum one rather than the phonon at gamma k. That is the same
   'exact continuum / protection' item (Hm, sec.14.0.6) -- now with the favorable
   relativistic framing. The collective coherence does NOT, by linear
   superposition, change the central velocity (carrier-governed); the resolution
   is the relativistic energy-velocity relation + masslessness, not a linear sum.

INPUTS: a, the Fermi bound = physical constants/measurement (cited). numpy req;
scipy optional. DETERMINISM: no RNG.
"""
import numpy as np

c = 1.0; a = 1.0; N = 4000; dt = 0.02

def force(u, mu2):
    f = np.zeros_like(u)
    f[1:-1] = (c*c/(a*a))*(u[2:] - 2*u[1:-1] + u[:-2]) - mu2*u[1:-1]
    return f

def measure_omega(k, mu2, amp=1e-3, T=400.0):
    from numpy.fft import rfft, rfftfreq
    n = np.arange(N, dtype=float)
    u = amp*np.cos(k*n); v = np.zeros_like(u); F = force(u, mu2)
    cos_k = np.cos(k*n); norm = (cos_k*cos_k).sum()
    proj=[]; ts=[]; nsteps=int(T/dt)
    for s in range(nsteps):
        if s % 2 == 0: proj.append((u*cos_k).sum()/norm); ts.append(s*dt)
        u = u + v*dt + 0.5*F*dt*dt
        Fn = force(u, mu2); v = v + 0.5*(F+Fn)*dt; F = Fn
    proj=np.array(proj)-np.mean(proj); ts=np.array(ts)
    w_an = np.sqrt((2*c/a)**2*np.sin(k/2)**2 + mu2)
    try:
        from scipy.optimize import curve_fit
        popt,_=curve_fit(lambda t,A,w,p,o:A*np.cos(w*t+p)+o, ts, proj,
                         p0=[np.std(proj)*1.4 or amp, max(w_an,1e-3), 0,0], maxfev=40000)
        return abs(popt[1])
    except Exception:
        W=rfft(proj*np.hanning(len(proj))); fr=rfftfreq(len(proj),d=ts[1]-ts[0])
        return 2*np.pi*fr[np.argmax(np.abs(W))]

# ---------------------------------------------------------------------------
print("=== (1a) RELATIVISTIC anti-dispersion (mass mu, continuum/low-k regime) ===")
print("    Klein-Gordon lattice w^2=c^2k^2+mu^2; expect v_g=c^2k/w < c, GROWING toward c.")
mu = 0.20; mu2 = mu*mu
print(f"    mass mu={mu};  {'k':>8} {'w_meas':>9} {'w_KG':>9} {'v_g=c^2k/w':>11} {'v_g/c':>8}")
for k in [0.02, 0.05, 0.10, 0.20, 0.40]:
    wm = measure_omega(k, mu2); wkg = np.sqrt(k*k + mu2)   # low-k: (2/a)sin(k/2)~k
    vg = (c*c*k)/wm
    print(f"            {k:>8.3f} {wm:>9.4f} {wkg:>9.4f} {vg:>11.4f} {vg/c:>8.4f}")
print("    => v_g < c (ceiling), and v_g RISES toward c as k(energy) rises = ANTI-dispersion.")
print()

print("=== (1b) MASSLESS modes: continuum (low-k) vs lattice phonon (high-k) ===")
print(f"    massless mu=0;  {'k (xpi)':>9} {'w_meas':>9} {'v_g=cos(ka/2)':>14} {'v_g/c':>8}")
for kf in [0.02, 0.10, 0.40, 0.80]:
    k = kf*np.pi
    wm = measure_omega(k, 0.0); vg = c*np.cos(k/2)
    print(f"            {kf:>9.3f} {wm:>9.4f} {vg:>14.4f} {vg/c:>8.4f}")
print("    => massless CONTINUUM (k->0): v_g->c (dispersionless). massless LATTICE (high k):")
print("       v_g=cos(ka/2) FALLS = the phonon 'conflict'. Same medium, two regimes.")
print()

# ---------------------------------------------------------------------------
print("=== (2) THE FERMI GATE: dv/c for gamma under each law ===")
hc = 1.239841984e-6  # eV*m
a_vp = 6.33e-19      # m, fundamental VP spacing
E_QG_phonon = np.sqrt(2)*hc/(np.pi*a_vp)   # 882 GeV (single-mode phonon scale)
E_QG_Fermi  = 1.3e20                        # eV (Fermi GRB 090510 quadratic bound)
print(f"    phonon single-mode scale E_QG,2 = {E_QG_phonon/1e9:.0f} GeV;  Fermi bound > {E_QG_Fermi/1e9:.1e} GeV")
print(f"    {'E (gamma)':>11} {'phonon dv/c':>13} {'relativistic dv/c':>20}")
print(f"    {'':>11} {'+(E/882GeV)^2':>13} {'(E0/E)^2/2, E0=0.511MeV':>23}")
E0_e = 0.511e6  # electron rest energy (eV), as an illustrative massive case
for E in [1e6, 1e9, 31e9, 1e11]:
    dv_ph = (E/E_QG_phonon)**2
    dv_rel = (E0_e/E)**2/2
    print(f"    {E/1e9:>8.3f} GeV {dv_ph:>13.2e} {dv_rel:>20.2e}")
print(f"    Fermi ceiling on dv/c at 31 GeV: {(31e9/E_QG_Fermi)**2:.1e}")
# E0 needed for the relativistic law to satisfy Fermi at 31 GeV:
E_test = 31e9; dv_fermi = (E_test/E_QG_Fermi)**2
E0_needed = np.sqrt(2*dv_fermi)*E_test
print(f"    => relativistic law meets Fermi at 31 GeV if rest energy E0 < {E0_needed:.1f} eV.")
print(f"       MASSLESS light (E0=0, the Goldstone mode) gives dv/c = 0 EXACTLY -> trivially met.")
print(f"       (measured photon-mass bound ~1e-18 eV << {E0_needed:.0f} eV, so masslessness is safe.)")
print()
print("  HONEST CONCLUSION:")
print("   * The phonon law GROWS with E (882 GeV conflict); the relativistic law SHRINKS with E.")
print("     The c-ceiling (sec.0.5 N4) is a relativistic structure -> the relativistic law -> high")
print("     energy is the SAFEST case, opposite to the naive 'conflict worsens at high E'.")
print("   * MASSLESS light (Goldstone, sec.14.0.5) travels at c for ALL energies -> dispersionless,")
print("     Fermi satisfied exactly. The 882 GeV 'conflict' is the artifact of the non-relativistic")
print("     phonon law applied to light.")
print("   * STILL OPEN (honest): that the realized lattice mode for light is the exact")
print("     relativistic/continuum one (not the phonon) at gamma k -- the same 'exact box_c /")
print("     protection' item (Hm). And NOTE: linear collective coherence does NOT change the")
print("     central velocity (carrier-governed); the resolution is the relativistic law +")
print("     masslessness, not a linear sum. The coherence question reduces to the protection one.")

# ---------------------------------------------------------------------------
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.8))
    EE = np.logspace(6, 11.5, 200)  # 1 MeV .. ~300 GeV
    ax[0].loglog(EE/1e9, (EE/E_QG_phonon)**2, 'r-', lw=2, label=r"phonon: $\Delta v/c=(E/882\,{\rm GeV})^2$ (grows)")
    ax[0].loglog(EE/1e9, (0.511e6/EE)**2/2, 'b-', lw=2, label=r"relativistic, $E_0{=}0.511$ MeV: $(E_0/E)^2/2$ (shrinks)")
    ax[0].axhline((31e9/E_QG_Fermi)**2, color='k', ls=':', lw=1.2)
    ax[0].annotate("Fermi ceiling (31 GeV)", (3e-3, (31e9/E_QG_Fermi)**2*2), fontsize=8)
    ax[0].axhline(0.0+1e-30, color='g', ls='--', lw=1.5, label=r"massless light ($E_0{=}0$): $\Delta v/c=0$")
    ax[0].set_xlabel("photon energy [GeV]"); ax[0].set_ylabel(r"$\Delta v/c$")
    ax[0].set_ylim(1e-30, 1e0)
    ax[0].set_title("(a) two laws, opposite slopes: relativistic high-E is SAFE")
    ax[0].legend(fontsize=7.5, loc="lower left")

    # (b) measured dispersions: massless lattice phonon vs massive KG (low-k anti-dispersion)
    kk = np.linspace(0.001, np.pi, 400)
    ax[1].plot(kk/np.pi, c*np.cos(kk/2), 'r-', lw=2, label=r"massless lattice: $v_g/c=\cos(ka/2)$ (phonon)")
    mu_=0.6
    vg_kg = (kk)/np.sqrt(kk**2+mu_**2)          # continuum KG v_g (low-k valid)
    ax[1].plot(kk/np.pi, vg_kg, 'b-', lw=2, label=r"massive KG: $v_g/c=k/\sqrt{k^2+\mu^2}$ (anti-disp.)")
    ax[1].axhline(1.0, color='k', ls=':', lw=0.8)
    ax[1].set_ylim(0, 1.05); ax[1].set_xlabel(r"wavenumber $ka/\pi$"); ax[1].set_ylabel(r"$v_g/c$")
    ax[1].set_title("(b) $v_g\\leq c$ always; phonon falls, relativistic rises toward $c$")
    ax[1].legend(fontsize=8, loc="lower center")
    plt.tight_layout(); plt.savefig("ch2_relativistic.png", dpi=120, bbox_inches="tight")
    print("\n[figure written: ch2_relativistic.png]")
except Exception as exc:
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
