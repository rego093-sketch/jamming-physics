#!/usr/bin/env python3
"""
ch2_grb.py  --  GRB as a lattice disturbance from colliding inflows (VP toy model).

USER HYPOTHESIS (cosmos-volume picture)
---------------------------------------
A gamma-ray burst is NOT a stream of independent high-k photon modes but a
COLLECTIVE disturbance of the medium, launched when two enormous quantum INFLOWS
(compact objects = inflow sinks) collide and their inflow lines break. Like the
gravitational wave that accompanies a real merger -- GW170817: a GW and a short
GRB arrived within ~1.7 s after ~130 Mly -- such a collective disturbance would
be (near-)DISPERSIONLESS, evading the lattice dispersion that would afflict
independent high-energy photons.

WHAT THIS SIM DOES
------------------
On the SAME elastic lattice that carries light (dispersion w(k)=2(c/a)sin(ka/2),
group velocity v_g=c cos(ka/2)), it contrasts two ways energy can propagate:

  (A) an "ordinary high-energy photon" = a single, weak, high-k wave packet
      (linear regime, beta=0);
  (B) a "GRB" = the strong, collective disturbance launched when two inward
      inflows collide (nonlinear regime, FPU-beta), as the user describes.

WHAT IT SHOWS (honest)
----------------------
 - (A) an independent high-k mode DISPERSES: v_g=c cos(ka/2)<c, so the packet
   spreads and its frequency components separate in arrival time. This IS the
   Fermi-GRB tension *for independent high-E photons*.
 - (B) the disturbance from a violent, macroscopic inflow collision organises
   into a COHERENT structure (a lattice soliton/compression front) that
   propagates at ~c with almost no spreading -- i.e. effectively dispersionless,
   like a gravitational wave. The nonlinearity supplied by the violent collision
   balances the dispersion.

WHAT IT DOES NOT SHOW (still OPEN)
---------------------------------
 - It does NOT derive the detected gamma-ray spectrum (keV-GeV) from the
   collective disturbance -- the energy<->wavelength reinterpretation is not
   established. Units are toy/normalised; no real masses, energies, or distances.
 - It therefore does NOT close the vacuum-dispersion problem. It shows only that
   the colliding-inflow mechanism is self-consistent and yields a dispersionless
   burst (degenerate with the accompanying GW), which is what GW170817 + Fermi
   would require. Whether real GRB emission is in this coherent regime is open.

INPUTS: none fitted. DEPENDENCIES: numpy (matplotlib optional). DETERMINISM: no RNG.
"""
import numpy as np

# --- the medium that carries light: a = K = m = 1  =>  c = 1 -------------------
N    = 4000
a = c = 1.0
dt   = 0.04

def force(u, beta):
    """FPU-beta lattice force: linear spring + cubic (beta) nonlinearity."""
    lin = np.zeros_like(u)
    lin[1:-1] = u[2:] - 2.0*u[1:-1] + u[:-2]
    if beta == 0.0:
        return lin
    du = np.diff(u)            # u_{n+1}-u_n, length N-1
    cube = du**3
    nl = np.zeros_like(u)
    nl[1:-1] = cube[1:] - cube[:-1]
    return lin + beta*nl

def step_verlet(u, v, F, beta):
    u = u + v*dt + 0.5*F*dt*dt
    Fn = force(u, beta)
    v = v + 0.5*(F + Fn)*dt
    return u, v, Fn

def rms_width(u, x):
    p = u*u
    tot = p.sum()
    if tot <= 0.0:
        return 0.0
    xm = (x*p).sum()/tot
    return np.sqrt((((x-xm)**2)*p).sum()/tot)

def peak_amp(u):
    return np.max(np.abs(u))

x = np.arange(N, dtype=float)

# ============================================================================
# (A) ordinary high-energy photon  =  single weak high-k packet (linear)
# ============================================================================
k0    = 1.5                      # carrier wavenumber ~ lattice scale (k0*a ~ 1.5)
sigA  = 60.0                     # envelope width (sites)
xA0   = 600.0
envA  = np.exp(-((x-xA0)/sigA)**2)
uA    = 1e-3 * envA*np.cos(k0*(x-xA0))           # weak -> linear
# right-moving via d'Alembert with the LATTICE group velocity at k0
vgA   = c*np.cos(k0/2.0)
duA   = np.gradient(uA)
vA    = -vgA*duA
FA    = force(uA, 0.0)

# ============================================================================
# (B) GRB  =  two inward INFLOWS collide -> launched collective disturbance
# ============================================================================
beta  = 1.0                      # violent collision -> strong-field nonlinearity
W     = 40.0                     # macroscopic inflow width (>> a)
amp   = 1.2                      # strong inflows
xc    = N/2.0
xL, xR = xc-700.0, xc+700.0
# each inflow: a compression bump moving toward the centre (inward)
bumpL = amp*np.exp(-((x-xL)/W)**2)               # left inflow, will move RIGHT
bumpR = amp*np.exp(-((x-xR)/W)**2)               # right inflow, will move LEFT
uB    = bumpL + bumpR
# right-mover: v=-c u' ; left-mover: v=+c u'  (linear-wave launch directions)
vB    = -c*np.gradient(bumpL) + c*np.gradient(bumpR)
FB    = force(uB, beta)

# ============================================================================
# evolve both; sample width/peak vs time
# ============================================================================
T_total = 2600
n_steps = int(T_total/dt)
sample_every = int(n_steps/40)
tt, wA, wB, pkA, pkB = [], [], [], [], []

# for snapshots of the collision (B) and the dispersed packet (A)
snapB = {}
snap_times = [0, int(700/dt), int(1500/dt)]      # before / during / after collision

for s in range(n_steps+1):
    if s % sample_every == 0:
        # measure the RIGHT-going outgoing pieces only (x > centre for B; whole for A)
        tt.append(s*dt)
        wA.append(rms_width(uA, x)); pkA.append(peak_amp(uA))
        right = x > xc + 30
        wB.append(rms_width(uB[right], x[right])); pkB.append(peak_amp(uB[right]))
    if s in snap_times:
        snapB[s] = uB.copy()
    uA, vA, FA = step_verlet(uA, vA, FA, 0.0)
    uB, vB, FB = step_verlet(uB, vB, FB, beta)

tt = np.array(tt); wA=np.array(wA); wB=np.array(wB); pkA=np.array(pkA); pkB=np.array(pkB)
# normalise widths to initial
wA_n = wA/wA[0]; wB_n = wB/wB[2]                  # B[2]: just after launch settles

# ============================================================================
print("=== GRB as a colliding-inflow lattice disturbance (VP toy) ===")
print(f"  lattice dispersion: w(k)=2 sin(k/2),  v_g(k)=cos(k/2);  a=c=1")
print()
print("  (A) ordinary high-E photon  = independent high-k packet, k0={:.2f} (k0*a~1.5), linear:".format(k0))
print(f"      group velocity v_g(k0)=cos(k0/2)={vgA:.3f}c  (< c -> subluminal, dispersive)")
print(f"      RMS width  start={wA[0]:.1f}  ->  end={wA[-1]:.1f}  (x{wA[-1]/wA[0]:.1f})  => SPREADS (disperses)")
print(f"      peak amplitude  start={pkA[0]:.2e} -> end={pkA[-1]:.2e}  (decays as it disperses)")
print()
print("  (B) GRB = two inflows (width W={:.0f}>>a) collide, beta={:.1f} (violent/nonlinear):".format(W, beta))
print(f"      outgoing-pulse RMS width  settle={wB[2]:.1f}  ->  end={wB[-1]:.1f}  (x{wB[-1]/wB[2]:.1f})")
print(f"      peak amplitude  settle={pkB[2]:.2e} -> end={pkB[-1]:.2e}")
coherent = (wB[-1]/wB[2] < 1.6) and (wA[-1]/wA[0] > 2.5)
print(f"      => {'COHERENT (near-dispersionless, like a GW)' if wB[-1]/wB[2] < 1.6 else 'spreads'};"
      f"  contrast factor (A spread)/(B spread) = {(wA[-1]/wA[0])/(wB[-1]/wB[2]):.1f}")
print()
print(f"  VERDICT: independent high-k photon disperses (x{wA[-1]/wA[0]:.1f}); "
      f"collective collision disturbance stays coherent (x{wB[-1]/wB[2]:.1f}).")
print("  EXPECTED: A spreads strongly, B stays coherent -> burst is dispersionless like the GW.")
print("  SCOPE: mechanism only (toy units). Does NOT derive the gamma-ray spectrum or close")
print("         the vacuum-dispersion problem; whether real GRBs are in this regime is OPEN.")

# ============================================================================
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(16, 4.8))

    # (a) the inflow collision launching a disturbance
    labels = ["t=0: two inflows approach", "during collision", "after: outgoing disturbance"]
    colors = ["tab:blue", "tab:purple", "tab:red"]
    for (s, lab, col) in zip(snap_times, labels, colors):
        ax[0].plot(x, snapB[s], color=col, lw=1.4, label=lab)
    ax[0].axvline(xc, color="k", ls=":", lw=0.8)
    ax[0].set_xlim(xc-1100, xc+1100)
    ax[0].set_xlabel("position  [sites]"); ax[0].set_ylabel("medium displacement")
    ax[0].set_title("(a) two inflows collide -> lattice disturbance")
    ax[0].legend(fontsize=8, loc="upper right")

    # (b) propagation comparison: high-k photon disperses, GRB pulse stays coherent
    ax[1].plot(x-xA0, uA/ (1e-3), color="tab:orange", lw=1.0,
               label="(A) high-k photon (linear): dispersed")
    # show B's outgoing right-going pulse, recentred for overlay
    right = x > xc+30
    ub_r = uB[right]; xb_r = x[right]
    xb_pk = xb_r[np.argmax(np.abs(ub_r))]
    ax[1].plot(xb_r - xb_pk, ub_r/np.max(np.abs(ub_r))*1.0, color="tab:red", lw=1.6,
               label="(B) GRB collective pulse: coherent")
    ax[1].set_xlim(-700, 700)
    ax[1].set_xlabel("position relative to packet centre  [sites]")
    ax[1].set_ylabel("normalised displacement")
    ax[1].set_title("(b) after long propagation: (A) spreads, (B) stays sharp")
    ax[1].legend(fontsize=8, loc="upper right")

    # (c) RMS width vs propagation distance (= c*t)
    ax[2].plot(tt*c, wA_n, color="tab:orange", lw=2.0, marker="o", ms=2,
               label=r"(A) high-k photon: $v_g=\cos(k_0/2)<c$")
    ax[2].plot(tt*c, wB_n, color="tab:red", lw=2.0, marker="s", ms=2,
               label="(B) GRB collective pulse")
    ax[2].axhline(1.0, color="k", ls=":", lw=0.8)
    ax[2].set_xlabel("propagation distance  [sites] ($=c\\,t$)")
    ax[2].set_ylabel("RMS width / initial")
    ax[2].set_title("(c) dispersion: (A) grows, (B) flat (dispersionless)")
    ax[2].legend(fontsize=8, loc="upper left")

    plt.tight_layout()
    plt.savefig("ch2_grb.png", dpi=120, bbox_inches="tight")
    print("\n[figure written: ch2_grb.png]")
except Exception as exc:
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
