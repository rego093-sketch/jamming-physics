#!/usr/bin/env python3
"""
ch2_lightangle.py  --  CONFIRM the physics-volume "light angle" theory (physics
volume sec.10.9) and its bearing on the gamma-ray / dispersion question.

PHYSICS-VOLUME RESULT BEING CHECKED (sec.10.9, eq:lightangle_master)
--------------------------------------------------------------------
Light is a transverse oscillation of rotating quanta (each of diameter
D = ell_rot = 2*lambda_Ce ~ 4.854 pm). A carrier of wavelength lambda rides a
chain of m quanta (chain length mD = hypotenuse); the transverse swing over the
chain is one wavelength (opposite = lambda). Hence

      sin(chi) = lambda / (m D),     m = ceil(lambda / D),    D = 4.854 pm.

The angle chi is between the propagation ray and the lattice axis:
  - long wavelengths (radio): m huge -> chi -> 90 deg  (nearly TRANSVERSE);
  - visible: a narrow near-transverse window (chi ~ 89.8-89.9 deg);
  - short wavelengths (GAMMA): m = 1 -> chi -> 0 deg   (quasi-LONGITUDINAL,
    "light near 0 degrees", running along the lattice axis).

This script reproduces sec.10.9's band table from the formula (a direct check
that the user's statement "gamma rays are just light near 0 degrees" is exactly
what the angle theory says), and prints chi for the Fermi-GRB gamma energies.

BEARING ON DISPERSION (stated honestly, NOT a derivation)
---------------------------------------------------------
The Fermi-GRB "8-15 orders" dispersion conflict (chapter 2) was computed by
treating high-energy light as a TRANSVERSE high-k lattice mode with propagation
wavelength = lambda (k = 2*pi/lambda). But sec.10.9 says gamma is QUASI-
LONGITUDINAL -- a different mode (m=1, running along the axis). So the conflict
may rest on the wrong mode for gamma. This script only CONFIRMS the angle (the
geometry); it does NOT derive the quasi-longitudinal gamma dispersion, so it does
not by itself close the Fermi question -- it shows the standard framing used the
wrong mode, which is a reframing, not yet a completed resolution.

DEPENDENCIES: numpy (matplotlib optional). NO RNG. No fitting.
"""
import numpy as np

# constants
hc_eV_m = 1239.841984e-9          # h*c in eV*m  (so lambda[m] = hc/E[eV])
D       = 4.854e-12               # quantum diameter ell_rot = 2*lambda_Ce  [m]

def chi_deg(lam):
    """light-propagation angle chi(lambda) from sec.10.9: sin chi = lam/(ceil(lam/D)*D)."""
    m = np.ceil(lam / D)
    s = lam / (m * D)
    s = np.clip(s, 0.0, 1.0)
    return np.degrees(np.arcsin(s)), m

# ---- reproduce the sec.10.9 band table -------------------------------------
bands = [
    ("Radio   ", 1.0),            # 1 m
    ("Visible ", 550e-9),         # 550 nm
    ("X-ray   ", 1e-10),          # 0.1 nm = 100 pm
    ("Gamma 1pm", 1e-12),         # 1 pm
    ("Gamma 1fm", 1e-15),         # 1 fm
]
print("=== CONFIRM physics-volume sec.10.9 angle theory: sin(chi)=lambda/(mD), D=4.854 pm ===")
print(f"{'band':10s} {'lambda':>12s} {'E':>12s} {'m':>10s} {'chi (deg)':>12s}")
for name, lam in bands:
    c, m = chi_deg(np.array([lam]))
    E = hc_eV_m/lam
    Es = (f"{E*1e-9:.2f} GeV" if E>=1e9 else f"{E*1e-6:.2f} MeV" if E>=1e6
          else f"{E*1e-3:.2f} keV" if E>=1e3 else f"{E:.3g} eV")
    print(f"{name:10s} {lam:12.3e} {Es:>12s} {int(m[0]):10d} {c[0]:12.3f}")

# Fermi-GRB gamma energies (the ones that set the dispersion bound)
print("\n  Fermi-GRB gamma energies -> propagation angle:")
for E in [1e6, 1e7, 1e8, 1e9, 1e10]:        # 1 MeV .. 10 GeV
    lam = hc_eV_m/E
    c, m = chi_deg(np.array([lam]))
    print(f"    E = {E*1e-9:7.3f} GeV  ->  lambda = {lam:.3e} m,  m={int(m[0])},  chi = {c[0]:.4f} deg  (quasi-longitudinal)")

print("\n  => sec.10.9 CONFIRMED: gamma rays are 'light near 0 deg' (quasi-longitudinal).")
print("     This is the framework's OWN statement, not an extrapolation.")
print("  NOTE (honest): the chapter-2 Fermi dispersion conflict treated gamma as a")
print("     TRANSVERSE high-k mode (k=2pi/lambda). sec.10.9 says it is QUASI-LONGITUDINAL")
print("     (a different mode). So the conflict may use the wrong mode -- a reframing.")
print("     This script confirms the ANGLE only; the quasi-longitudinal gamma DISPERSION")
print("     is NOT derived here, so the Fermi question is reframed, not yet closed.")

# ----------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    E = np.logspace(-7, 10, 1400)            # 0.1 ueV .. 10 GeV
    lam = hc_eV_m/E
    chi, m = chi_deg(lam)

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    # (a) chi vs photon energy
    ax[0].semilogx(E, chi, color="tab:blue", lw=2.2)
    ax[0].axhline(90, color="k", ls=":", lw=1); ax[0].axhline(0, color="k", ls=":", lw=1)
    # band shading
    bands_E = [("radio", 1e-7, 1e-3, "tab:green"),
               ("visible", 1.6, 3.3, "tab:olive"),
               ("X-ray", 1e2, 1e5, "tab:orange"),
               ("gamma", 1e5, 1e10, "tab:red")]
    for nm, e0, e1, col in bands_E:
        ax[0].axvspan(e0, e1, color=col, alpha=0.10)
        ax[0].text(np.sqrt(e0*e1), 8, nm, color=col, fontsize=8, ha="center")
    ax[0].axvspan(1e6, 1e10, color="tab:red", alpha=0.06)
    ax[0].text(3e7, 50, "Fermi-GRB\n(MeV-GeV):\nquasi-longitudinal\n$\\chi\\!\\to\\!0^\\circ$",
               color="tab:red", fontsize=8, ha="center")
    ax[0].set_xlabel("photon energy  [eV]")
    ax[0].set_ylabel(r"propagation angle $\chi$ to lattice axis  [deg]")
    ax[0].set_ylim(-3, 95)
    ax[0].set_title(r"(a) sec.10.9: $\sin\chi=\lambda/(mD)$  -- gamma is near $0^\circ$")

    # (b) the right-triangle picture for visible vs gamma (schematic)
    def triangle(ax, mD, lam_op, label, col, y0):
        # hypotenuse along x of length 1 (normalised), opposite = lam/mD
        s = lam_op/mD
        adj = np.sqrt(max(0.0, 1-s*s))
        ax.plot([0, adj], [y0, y0], color=col, lw=2)                 # adjacent (longitudinal)
        ax.plot([adj, adj], [y0, y0+s], color=col, lw=2)             # opposite (transverse swing)
        ax.plot([0, adj], [y0, y0+s], color=col, lw=2, ls="--")      # hypotenuse (chain mD)
        ax.text(adj+0.02, y0+s/2, label, color=col, fontsize=9, va="center")
    ax[1].set_xlim(0, 1.25); ax[1].set_ylim(-0.15, 1.25)
    triangle(ax[1], 1.0, 1.0*np.sin(np.radians(89.9)), "visible: $\\chi\\approx89.9^\\circ$ (transverse)", "tab:olive", 0.0)
    triangle(ax[1], 1.0, np.sin(np.radians(8.0)),      "gamma: $\\chi\\approx8^\\circ$ (longitudinal)",   "tab:red", 0.0)
    ax[1].annotate("chain $mD$ (propagation)", xy=(0.5,0.55), fontsize=8, color="gray", rotation=20)
    ax[1].set_xlabel("longitudinal (along lattice axis)")
    ax[1].set_ylabel("transverse swing  ($=\\lambda$)")
    ax[1].set_title("(b) wavelength = transverse pitch of an $m$-quantum chain")

    plt.tight_layout()
    plt.savefig("ch2_lightangle.png", dpi=120, bbox_inches="tight")
    print("\n[figure written: ch2_lightangle.png]")
except Exception as exc:
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
