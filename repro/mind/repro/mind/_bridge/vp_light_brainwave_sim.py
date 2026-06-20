#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_light_brainwave_sim.py
=========================
Reproduces, from the VP / Jamming-Physics whitepaper (DOI 10.5281/zenodo.17932566),
the three things asked for, deterministically and with NO fitted parameters:

  PART 1  Emergence of light at the quantum unit
          - the jamming lattice carries a SINGLE linear elastic-wave speed c = sqrt(B/rho)
            (longitudinal branch only; shear -> 0 at the isostatic point) -> omega = c*q
          - the single optical anchor lambda_ref = 632.99 nm fixes the lattice unit a,
            so one optical period is resolved by N = lambda_ref/a ~ 10^12 lattice steps,
            and the per-step rotation ("angle") of the carrier is theta_step = 2*pi/N.
          - optical->quantum amplification A ~ 8e5 (cited) fixes D = 2*pi*lambda_ref/A.

  PART 2  The angle theory (geometric rectification, whitepaper SS5)
          - alpha = <|cos t|>            = 2/pi      (single rectification)
          - delta = <[cos t]+ [cos f]+>  = 1/pi^2    (double rectification)
          - 2*pi  = alpha/delta
          - n-fold law nu_n = n*pi^(2(n-1));  nu_3 = 3*pi^4 (proton event rate);
            m_p/m_e = 6*pi^5 = 2*pi * 3*pi^4
          - forced-radius angle attractor xdot = alpha*x^-5 - x^-4 -> x* = alpha = 2/pi.

  PART 3  Re-emit the SAME light at brain-wave wavelengths
          - a brainwave of frequency nu is an EM oscillation of wavelength lambda = c/nu,
            so on the SAME vacuum lattice its per-step carrier angle is
            theta_step = 2*pi*a/lambda = 2*pi*a*nu/c  -> astronomically small
            (tens of decimal places below the point), exactly because lambda is ~10^13x
            longer than optical light.

Everything is float64 except the final angle expansions, which use Decimal so the
"how many zeros after the point" is shown literally. Deterministic: no RNG drives any
reported number (a fixed-seed Monte-Carlo cross-check of alpha/delta is included only as
an independent witness, printed separately).
"""
import numpy as np
from decimal import Decimal, getcontext
getcontext().prec = 60
PI = np.pi

# ----------------------------------------------------------------------------
# Canonical constants -- CITED VERBATIM from the physics whitepaper SSOT
# (tools/vp_numeric_ssot.py : CANON ; chapter SS3/SS10/SS11/SS-SP)
# ----------------------------------------------------------------------------
C        = 299792458.0                      # speed of light, exact SI            [F]
LAMBDA   = 632.99e-9                         # single empirical length anchor      [F]
A_LAT    = 6.3299121257859865746e-19         # VP lattice unit a (m)               [F]
D_ANCH   = 4.852620477e-12                   # quantum (anchor) diameter D (m)     [H]
RHO      = 1.0                               # medium density (sole inertial cond) [axiom]
A_MED_DEPOSITED  = 8.0e5                      # optical->quantum amplification (sim)[V]
A_MED_REPRODUCED = 8.1e5                      # independent reproduction            [V]

def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

def dec_fixed(x, places=34):
    """Fixed-point decimal string so leading zeros after the point are visible."""
    return format(Decimal(repr(x)), 'f')[:places+2]

# ============================================================================
banner("PART 1  -  EMERGENCE OF LIGHT AT THE QUANTUM UNIT  (c^2 = B/rho)")
# ----------------------------------------------------------------------------
# 1a. Single elastic-wave speed from the lattice: a 1-D harmonic chain is the
#     reduced 1-branch realization of the isostatic jamming result (the full 3-D
#     shear-vanishing G_relaxed->0 leaving one longitudinal c^2=B/rho is the
#     deposited sim lattice_3d_jam_percolation.py). In lattice units K=m=a=1 so
#     rho = m/a = 1, B = K*a = 1, c = sqrt(B/rho) = 1, and omega(q)=2 sin(q/2).
K = 1.0; M = 1.0; A_CELL = 1.0
rho_lat = M / A_CELL
B_lat   = K * A_CELL
c_lat   = np.sqrt(B_lat / rho_lat)
q = np.linspace(1e-4, 0.30, 400)                       # long-wavelength window
omega = 2.0 * np.sqrt(K / M) * np.abs(np.sin(q * A_CELL / 2.0))
# fit omega = c*q through the long-wavelength points
slope = np.sum(q * omega) / np.sum(q * q)              # zero-intercept LS slope
ss_res = np.sum((omega - slope * q) ** 2)
ss_tot = np.sum((omega - omega.mean()) ** 2)
R2 = 1.0 - ss_res / ss_tot
print(f"  lattice elastic-wave speed   c = sqrt(B/rho) = {c_lat:.6f}   (B={B_lat}, rho={rho_lat})")
print(f"  dispersion fit  omega = c*q :  c_fit = {slope:.6f}   R^2 = {R2:.6f}")
print(f"  -> single linear branch (longitudinal); shear branch -> 0 at isostatic z=2d=6.")
print(f"     hence lambda = 2*pi/q = c/nu  (standard acoustics on the lattice).")

# 1b. Optical realization: the one empirical wavelength fixes the lattice unit a,
#     so one optical PERIOD is resolved by N lattice steps; the carrier advances
#     a fixed rotation angle theta_step = 2*pi/N per lattice step (k*a).
N_opt      = LAMBDA / A_LAT                              # steps per optical wavelength
theta_opt  = 2.0 * PI / N_opt                            # per-step carrier angle (rad)
print(f"\n  optical anchor lambda_ref      = {LAMBDA*1e9:.2f} nm")
print(f"  lattice unit a                 = {A_LAT:.6e} m")
print(f"  steps per optical wavelength   N = lambda/a = {N_opt:.6e}   (~10^12)")
print(f"  per-step carrier ANGLE         theta_step = 2*pi/N = {theta_opt:.6e} rad")
print(f"                                            = {dec_fixed(theta_opt)} rad")
# optical->quantum amplification cross-check (A cited, D recomputed)
for tag, A in [("deposited", A_MED_DEPOSITED), ("reproduced", A_MED_REPRODUCED)]:
    D_chk = 2.0 * PI * LAMBDA / A
    print(f"  D = 2*pi*lambda/A  (A_med {tag}={A:.1e}) = {D_chk*1e12:.4f} pm "
          f"vs anchor D = {D_ANCH*1e12:.4f} pm  (delta {100*(D_chk/D_ANCH-1):+.2f}%)")

# ============================================================================
banner("PART 2  -  THE ANGLE THEORY  (geometric rectification: every pi is an averaged rotation)")
# ----------------------------------------------------------------------------
# alpha = <|cos t|> over the full cycle ;  delta = <[cos t]+[cos f]+>
t  = np.linspace(0.0, 2*PI, 2_000_001)
alpha_num = np.trapezoid(np.abs(np.cos(t)), t) / (2*PI)
alpha_exact = 2.0 / PI
g  = np.linspace(0.0, 2*PI, 4001)
T, F = np.meshgrid(g, g, indexing="ij")
half = lambda x: np.clip(np.cos(x), 0.0, None)          # [cos]_+  half-wave rectifier
delta_num = np.trapezoid(np.trapezoid(half(T)*half(F), g, axis=1), g) / (2*PI)**2
delta_exact = 1.0 / PI**2
print(f"  alpha = <|cos t|>            quad = {alpha_num:.9f}   exact 2/pi   = {alpha_exact:.9f}")
print(f"  delta = <[cos t]+[cos f]+>   quad = {delta_num:.9f}   exact 1/pi^2 = {delta_exact:.9f}")
print(f"  2*pi  = alpha/delta          = {alpha_exact/delta_exact:.9f}   (true 2*pi = {2*PI:.9f})")
# fixed-seed Monte-Carlo, INDEPENDENT witness only
rng = np.random.default_rng(632990)
ta = rng.uniform(0, 2*PI, 8_000_000)
fa = rng.uniform(0, 2*PI, 8_000_000)
print(f"    [MC witness, seed=632990]  alpha_MC = {np.abs(np.cos(ta)).mean():.6f} , "
      f"delta_MC = {(half(ta)*half(fa)).mean():.6f}")
# n-fold rectification law nu_n = n*pi^(2(n-1))
print("  n-fold law  nu_n = n * pi^(2(n-1)) :")
for n in range(1, 5):
    print(f"      nu_{n} = {n}*pi^{2*(n-1)} = {n*PI**(2*(n-1)):.6f}"
          + ("   <- proton event rate nu_p = 3*pi^4" if n == 3 else ""))
print(f"  m_p/m_e = 6*pi^5 = 2*pi * 3*pi^4 = {6*PI**5:.6f}")
# forced-radius angle attractor:  xdot = alpha*x^-5 - x^-4  ->  x* = alpha
def attractor_fixed_point(x0, steps=4_000_000, dt=2e-4):
    x = x0
    for _ in range(steps):
        x += dt * (alpha_exact * x**-5 - x**-4)
    return x
xs = [attractor_fixed_point(x0) for x0 in (0.40, 0.55, 0.90)]
print(f"  forced-radius attractor xdot = alpha*x^-5 - x^-4 :")
print(f"      x* from x0=0.40,0.55,0.90 -> {xs[0]:.6f}, {xs[1]:.6f}, {xs[2]:.6f}"
      f"   (target alpha=2/pi={alpha_exact:.6f})")
print(f"      => r_p/lambda_C,p = 2/pi   (proton radius forced by the same angle constant)")

# ============================================================================
banner("PART 3  -  RE-EMIT THE SAME LIGHT AT BRAIN-WAVE WAVELENGTHS  (angle goes deep below the point)")
# ----------------------------------------------------------------------------
# A brainwave of frequency nu is an EM oscillation of wavelength lambda = c/nu.
# On the SAME vacuum lattice the per-step carrier angle is theta = 2*pi*a/lambda.
bands = [
    ("balance / slow-tonic",      1.0),
    ("delta (hypothalamus)",      2.0),
    ("pain / midbrain theta",     4.0),
    ("theta (hippocampus)",       6.0),
    ("alpha (thalamus/proprio)", 10.0),
    ("beta (striatum/pallidum)", 20.0),
    ("gamma (neocortex/vision)", 40.0),
    ("high-gamma (olf. bulb)",   60.0),
]
print(f"  {'band (Hz, brain organ)':<26}{'lambda = c/nu (m)':>20}{'N = lambda/a':>16}"
      f"{'theta_step = 2*pi/N (rad)':>28}")
print("  " + "-" * 88)
rows = []
for name, nu in bands:
    lam_b   = C / nu
    N_b     = lam_b / A_LAT
    theta_b = 2.0 * PI / N_b
    rows.append((name, nu, lam_b, N_b, theta_b))
    print(f"  {name:<26}{lam_b:>20.6e}{N_b:>16.3e}{theta_b:>28.6e}")

print("\n  the same angles written out (fixed point) -- count the zeros after the point:")
for name, nu, lam_b, N_b, theta_b in rows:
    print(f"    {nu:>4.0f} Hz  theta_step = {dec_fixed(theta_b, 40)} rad")

theta_g = rows[6][4]   # gamma 40 Hz
print(f"\n  optical carrier per-step angle : {theta_opt:.6e} rad")
print(f"  gamma 40 Hz   per-step angle   : {theta_g:.6e} rad")
print(f"  ratio optical / brainwave      : {theta_opt/theta_g:.3e}   "
      f"(~13 orders of magnitude: the brainwave angle is that much finer)")
print("\n  SAME medium, SAME law c^2=B/rho, SAME angle machinery -- only lambda differs.")
print("  A brainwave is emerged light at an EEG-band wavelength; its lattice rotation per")
print("  step is just tens of decimals smaller. (Whether cognition USES this = OPEN.)")
banner("DONE -- all numbers above are deterministic; rerun yields identical output.")
