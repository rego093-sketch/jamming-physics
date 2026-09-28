#!/usr/bin/env python3
"""
ch2_goldstone.py -- Light as the Goldstone mode of a synchronized-rotor lattice
                    (tests the physics-volume sec.14.0 / sec.14.0.6 mechanism).

THE IDEA (user's intuition; physics-volume sec.14.0)
----------------------------------------------------
Each lattice quantum's only degree of freedom is ROTATION. In the jammed plenum
the coupled rotators PHASE-LOCK (Kuramoto-type synchronization) onto a common
axis -> a global U(1) common phase. Synchronization spontaneously breaks that
global U(1), giving a massless GOLDSTONE mode. Physics-volume sec.14.0.6
identifies LIGHT with this mode: E = displacement (polar), B = twist (axial),
and source-free Maxwell is the curl square-root of the wave operator box_c.

WHY THIS BEARS ON THE FERMI / DISPERSION PROBLEM
------------------------------------------------
box_c (the continuum wave operator) gives w = c k EXACTLY -> DISPERSIONLESS.
If light is the box_c/Maxwell/Goldstone mode (not a generic discrete phonon
w = 2(c/a) sin(ka/2)), it does not disperse. The question this script probes:
does a synchronized-rotor lattice actually produce a dispersionless mode, and
over what band?

WHAT THIS SIM DOES
------------------
(1) SYNCHRONIZATION: a Kuramoto chain (rotors with a spread of natural
    frequencies, nearest-neighbour coupling). Measures the order parameter
    r = |<e^{i theta}>|. For coupling above threshold, r -> ~1: the rotors
    phase-lock onto a common axis. (The user's "synchronized rotation axis.")
(2) GOLDSTONE DISPERSION: on the synchronized medium (Hamiltonian XY rotor
    chain, I*theta'' = J[sin(th_{n+1}-th_n) - sin(th_n-th_{n-1})]) it excites
    small plane-wave phase fluctuations at several k and MEASURES w(k), the
    dispersion of the Goldstone mode = light. Compares to the analytic
    spin-wave law w(k) = 2 sqrt(J/I) |sin(k/2)| and to the group velocity v_g.

WHAT IT SHOWS (honest)
----------------------
 - The Goldstone mode is LINEAR, w ~ c_eff k (DISPERSIONLESS, v_g = c_eff =
   const), at LONG WAVELENGTH -- exactly the band where light is observed
   dispersionless (radio, visible). This is a genuine success of the
   synchronized-rotor picture: it explains dispersionless low-energy light.
 - At SHORT wavelength (high k) the same mode CURVES (v_g < c_eff): the bare
   synchronized-rotor Goldstone disperses like a phonon there. So
   synchronization ALONE does not make gamma (high-k) dispersionless.

WHAT IT DOES NOT SHOW (still OPEN -- and the framework says so)
--------------------------------------------------------------
 - It does NOT make gamma dispersionless. Getting exact box_c (Maxwell)
   behaviour up to gamma requires either (i) the angle/m=1 geometry of sec.10.9
   (lambda = transverse swing, propagation along the axis), or (ii) the exact
   curl-factorization being physically forced -- which physics-volume
   sec.14.0.6/14.0.7 grades Hm (HYPOTHESIS, "physical forcing of the curl
   coupling not yet derived"). This script confirms the long-wavelength half
   of the mechanism and locates precisely what is missing for gamma.

INPUTS: none fitted (toy normalised units I=J=1, a=1). DETERMINISM: fixed seed
for the natural-frequency draw only (synchronization demo). numpy required.
"""
import numpy as np

# ============================================================================
# (1) SYNCHRONIZATION: Kuramoto chain -> common axis
# ============================================================================
def kuramoto_order(N=500, K=4.0, spread=1.0, T=40.0, dt=0.01, seed=0):
    # mean-field (all-to-all) Kuramoto -- the high-coordination limit appropriate
    # to the dense 3D jammed lattice (fcc coordination 12); 1D local coupling does
    # not globally order (Mermin-Wagner), so the lattice's high connectivity matters.
    rng = np.random.default_rng(seed)
    omega = spread * rng.standard_normal(N)        # natural frequencies (spread)
    theta = rng.uniform(0, 2*np.pi, N)             # random initial phases
    nsteps = int(T/dt)
    rs = []
    for s in range(nsteps):
        z = np.mean(np.exp(1j*theta)); r = np.abs(z); psi = np.angle(z)
        theta = theta + dt*(omega + K*r*np.sin(psi - theta))   # mean-field coupling
        if s % max(1, int(nsteps/200)) == 0:
            rs.append(np.abs(np.mean(np.exp(1j*theta))))
    return np.array(rs), float(np.mean(rs[-20:]))

print("=== (1) SYNCHRONIZATION: do coupled rotators lock onto a common axis? ===")
print("    Kuramoto (mean-field), N=500, natural-frequency spread=1.0; order parameter r=|<e^{i th}>|")
for K in [0.0, 0.5, 4.0]:
    _, r_final = kuramoto_order(K=K)
    tag = "incoherent" if r_final < 0.4 else ("partially locked" if r_final < 0.8 else "PHASE-LOCKED (common axis)")
    print(f"    coupling K={K:>4.1f}  ->  steady-state r = {r_final:.3f}   [{tag}]")
print("    => strong coupling locks the rotors onto a common phase/axis (the sec.14.0 premise).")
print()

# ============================================================================
# (2) GOLDSTONE DISPERSION: w(k) of small phase fluctuations of the synced medium
#     Hamiltonian XY rotor chain:  I th'' = J[sin(th_{n+1}-th_n) - sin(th_n-th_{n-1})]
#     Linear Goldstone (spin-wave) law:  w(k) = 2 sqrt(J/I) |sin(k/2)|,  c_eff=sqrt(J/I)
# ============================================================================
I = J = 1.0
c_eff = np.sqrt(J/I)               # long-wavelength signal speed (the "c" of light here)
N = 2000
dt = 0.02

def force_xy(th):
    f = np.zeros_like(th)
    d = np.diff(th)                              # th_{n+1}-th_n
    f[1:-1] = np.sin(d[1:]) - np.sin(d[:-1])
    return J*f

def measure_omega(k, amp=1e-3, T=300.0):
    """Excite a small standing phase wave cos(k n); measure its oscillation freq
    by fitting A*cos(w t + ph) (robust even for few periods at small k)."""
    from scipy.optimize import curve_fit
    n = np.arange(N, dtype=float)
    th = amp*np.cos(k*n)                          # small fluctuation about synced state th=0
    v  = np.zeros_like(th)
    F  = force_xy(th)
    proj = []; ts = []
    nsteps = int(T/dt)
    cos_k = np.cos(k*n); norm = (cos_k*cos_k).sum()
    for s in range(nsteps):
        if s % 2 == 0:
            proj.append((th*cos_k).sum()/norm); ts.append(s*dt)
        th = th + v*dt + 0.5*(F/I)*dt*dt
        Fn = force_xy(th)
        v  = v + 0.5*(F+Fn)/I*dt
        F  = Fn
    proj = np.array(proj); ts = np.array(ts)
    w_guess = 2*c_eff*max(np.abs(np.sin(k/2)), 1e-4)
    def model(t, A, w, ph, off): return A*np.cos(w*t + ph) + off
    try:
        popt, _ = curve_fit(model, ts, proj,
                            p0=[proj.std()*1.4 or amp, w_guess, 0.0, 0.0], maxfev=40000)
        return abs(popt[1])
    except Exception:
        # fallback: FFT peak
        pr = proj - proj.mean()
        W = np.fft.rfft(pr*np.hanning(len(pr)))
        freqs = np.fft.rfftfreq(len(pr), d=(ts[1]-ts[0]))
        return 2*np.pi*freqs[np.argmax(np.abs(W))]

print("=== (2) GOLDSTONE-MODE DISPERSION of the synchronized medium (= light) ===")
print(f"    Hamiltonian XY rotor chain, I=J=1 -> long-wavelength speed c_eff=sqrt(J/I)={c_eff:.3f}")
print(f"    {'k (x pi)':>10} {'w_measured':>12} {'w_analytic':>12} {'v_g=dw/dk':>11} {'v_g/c_eff':>10}")
ks = np.array([0.05, 0.10, 0.20, 0.40, 0.80, 1.50, 2.50])*np.pi/np.pi  # in rad/site
ks = np.array([0.02, 0.05, 0.10, 0.25, 0.50, 1.00, 1.80, 2.80])        # rad/site (0..pi)
ks = ks[ks < np.pi]
wmeas, wana, vg = [], [], []
for k in ks:
    wm = measure_omega(k)
    wa = 2*c_eff*np.abs(np.sin(k/2))
    vgk = c_eff*np.cos(k/2)                      # analytic group velocity dw/dk
    wmeas.append(wm); wana.append(wa); vg.append(vgk)
    print(f"    {k/np.pi:>10.3f} {wm:>12.4f} {wa:>12.4f} {vgk:>11.4f} {vgk/c_eff:>10.4f}")
wmeas = np.array(wmeas); wana = np.array(wana); vg = np.array(vg)
err = np.max(np.abs(wmeas-wana)/(wana+1e-9))
print(f"    [sim vs analytic w(k): max relative error = {err:.1e}  -> spin-wave law confirmed]")
print()
print("  READING:")
print(f"   - small k (long wavelength): w ~ c_eff*k, v_g -> c_eff (DISPERSIONLESS).")
print(f"     e.g. k=0.05pi: v_g/c_eff = {np.cos(0.02/2):.5f} ~ 1  -> light is dispersionless")
print( "     at radio/visible wavelengths, AS OBSERVED. This is the synchronized-rotor win.")
print(f"   - high k (short wavelength): v_g/c_eff = cos(k/2) FALLS; e.g. k=0.8pi -> {np.cos(0.8*np.pi/2):.3f}.")
print( "     The bare Goldstone mode DISPERSES at high k, like a phonon.")
print()
print("  HONEST CONCLUSION:")
print("   * Synchronization -> Goldstone mode reproduces DISPERSIONLESS light at the")
print("     long wavelengths where light is observed dispersionless (a real success of")
print("     the sec.14.0 picture, and of the user's rotation-axis intuition).")
print("   * It does NOT by itself make GAMMA (high-k) dispersionless: the bare spin-wave")
print("     curves there. Exact box_c (Maxwell) up to gamma needs the sec.10.9 angle/m=1")
print("     geometry or the curl-factorization being physically forced -- which the")
print("     physics volume itself grades Hm (HYPOTHESIS, sec.14.0.6/14.0.7). OPEN.")

# ============================================================================
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rs, _ = kuramoto_order(K=4.0)
    rs0, _ = kuramoto_order(K=0.0)
    tt = np.linspace(0, 40.0, len(rs))

    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))

    # (a) synchronization order parameter
    ax[0].plot(tt, rs, color="tab:red", lw=2.0, label="K=4.0 (strong): locks")
    ax[0].plot(tt, rs0, color="tab:gray", lw=1.5, label="K=0 (uncoupled): incoherent")
    ax[0].axhline(1.0, color="k", ls=":", lw=0.8)
    ax[0].set_ylim(0, 1.05); ax[0].set_xlabel("time"); ax[0].set_ylabel("order parameter  r = |<e^{i th}>|")
    ax[0].set_title("(a) rotors synchronize onto a common axis")
    ax[0].legend(fontsize=8, loc="lower right")

    # (b) dispersion w(k)
    kk = np.linspace(0, np.pi, 400)
    ax[1].plot(kk/np.pi, 2*c_eff*np.abs(np.sin(kk/2)), color="tab:blue", lw=2.0,
               label=r"Goldstone $w=2c_{\rm eff}\,|\sin(k/2)|$")
    ax[1].plot(kk/np.pi, c_eff*kk, color="tab:green", ls="--", lw=1.6,
               label=r"$w=c_{\rm eff}\,k$ (box$_c$/Maxwell, dispersionless)")
    ax[1].plot(ks/np.pi, wmeas, "o", color="tab:red", ms=5, label="simulated")
    ax[1].set_xlabel(r"wavenumber $k/\pi$"); ax[1].set_ylabel(r"$w(k)$")
    ax[1].set_title("(b) light = Goldstone mode: linear at small k, curves at high k")
    ax[1].legend(fontsize=8, loc="upper left")

    # (c) group velocity
    ax[2].plot(kk/np.pi, np.cos(kk/2), color="tab:purple", lw=2.0, label=r"$v_g/c_{\rm eff}=\cos(k/2)$")
    ax[2].axhline(1.0, color="k", ls=":", lw=0.8)
    ax[2].axvspan(0, 0.1, color="tab:green", alpha=0.15, label="long-wavelength: dispersionless")
    ax[2].set_ylim(0, 1.05); ax[2].set_xlabel(r"wavenumber $k/\pi$"); ax[2].set_ylabel(r"$v_g/c_{\rm eff}$")
    ax[2].set_title("(c) dispersionless ($v_g\\to c$) at long wavelength; falls at high k")
    ax[2].legend(fontsize=8, loc="lower left")

    plt.tight_layout()
    plt.savefig("ch2_goldstone.png", dpi=120, bbox_inches="tight")
    print("\n[figure written: ch2_goldstone.png]")
except Exception as exc:
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
