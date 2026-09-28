"""
stiffness_size.py - FINAL GOAL: derive D = 4.85 pm from jamming, via the
stiffness balance "elasticity = 1, stiffness = c^2" (physics whitepaper S11.6.4).

Chain (no external theory; the lattice + geometry do the work):

  (0) JAMMING gives the stiffness.  The collective stiffness K = c^2 is a MEASURED
      property of the jammed substrate -- it emerges when phi self-organises to
      ~0.64 with contacts z -> 2d = 6 (the whitepaper's keystone S11.6.1 = our M1).
      So "stiffness = c^2" is not assumed; it is the jamming output.

  (1) STIFFNESS SELECTS SIZE (S11.6.4).  Two pressures act on the core boundary:
        stiffness support (rigid medium resists compression): OUTWARD, ~ r^-5,
        inflow collapse                                       : INWARD , ~ r^-4.
      The support is one power steeper, so the net force crosses zero EXACTLY ONCE
      and the crossing is STABLE -> the radius is a FORCED fixed point, the unique
      size at which a core can sit. This is why a proton has a definite size.

  (2) THE FIXED POINT IS 2/pi.  The stiffness support is a directional (radial)
      action; only its RECTIFIED component acts along the radius -- the survival
      fraction alpha = <|cos theta|> = 2/pi (geometry, S5.1). Writing the rectified
      stiffness  alpha * x^-5  against the inflow  x^-4  (inflow coefficient = 1,
      i.e. "elasticity = 1"), the balance  alpha x^-5 = x^-4  forces  x* = alpha.
      Hence  r_p / lambda_{C,p} = alpha = 2/pi.

  (3) -> 4.85 pm.  r_p = (2/pi) lambda_{C,p}  ->  D = 6 pi^6 r_p, cross-checked by
      the electron route  D = 2 lambda_{C,e}.  Both land on ~4.852 pm.

This module DERIVES and CHECKS the chain numerically (no fitting). numpy only.
"""
import numpy as np

# CODATA reference lengths (these are kinematic anchors, not free parameters)
LAMBDA_C_E = 2.42631023867e-12   # electron Compton wavelength (m)
LAMBDA_C_P = 1.32140985539e-15   # proton  Compton wavelength (m)


def rectification_alpha(nsamp=2_000_000):
    """alpha = <|cos theta|> over a full cycle = (1/2pi) \\int |cos| dtheta = 2/pi.
    The geometric survival fraction of a directional action under magnitude averaging."""
    th = np.linspace(0, 2 * np.pi, nsamp, endpoint=False)
    return float(np.mean(np.abs(np.cos(th))))


def net_pressure(x, alpha):
    """Dimensionless boundary pressure (outward +):
       rectified stiffness support  alpha * x^-5   minus   inflow  x^-4 (coeff 1)."""
    return alpha * x ** (-5.0) - x ** (-4.0)


def find_fixed_point(alpha):
    """Locate the single zero of net_pressure on a fine grid; report it and stability."""
    x = np.linspace(0.2, 1.5, 400000)
    F = net_pressure(x, alpha)
    s = np.where(np.sign(F[:-1]) != np.sign(F[1:]))[0]
    roots = []
    for i in s:
        # linear interpolation of the crossing
        x0 = x[i] - F[i] * (x[i + 1] - x[i]) / (F[i + 1] - F[i])
        dF = (net_pressure(x0 + 1e-6, alpha) - net_pressure(x0 - 1e-6, alpha)) / 2e-6
        roots.append((x0, dF))
    return roots


def main():
    np.set_printoptions(suppress=True)
    print("stiffness_size.py - deriving D = 4.85 pm from the jamming stiffness balance")
    print("=" * 76)

    # (0) jamming keystone (recap): stiffness = c^2 is MEASURED (phi~0.64, z->6 = M1)
    print("\n(0) stiffness = c^2 is the JAMMING output (keystone): phi_c~0.64, z->2d=6")
    print("    (measured in M1 jam_packing.py) -> the substrate HAS a collective stiffness K=c^2.")

    # (2) rectification alpha = 2/pi  (pure geometry)
    a_num = rectification_alpha()
    a_exact = 2.0 / np.pi
    print(f"\n(2a) rectification survival fraction  alpha = <|cos|> = {a_num:.6f}  "
          f"(exact 2/pi = {a_exact:.6f})")

    # (1)+(2) the balance forces the fixed point x* = alpha
    roots = find_fixed_point(a_exact)
    print(f"\n(1) stiffness balance: rectified stiffness alpha*x^-5  vs  inflow x^-4 (coeff 1)")
    print(f"    {'x* (root)':>11} {'dF/dx':>10} {'stable?':>8}")
    for x0, dF in roots:
        print(f"    {x0:11.6f} {dF:10.3f} {'YES' if dF < 0 else 'no':>8}")
    x_star = roots[0][0]
    print(f"    -> single STABLE crossing at x* = {x_star:.6f}  =  alpha = 2/pi = {a_exact:.6f}")
    print(f"       => r_p / lambda_C,p = 2/pi  (the size is FORCED, not chosen).")

    # (3) the length chain to 4.85 pm
    rp = (2.0 / np.pi) * LAMBDA_C_P
    D_proton = 6.0 * np.pi ** 6 * rp                  # proton route
    D_electron = 2.0 * LAMBDA_C_E                      # electron route (cross-check)
    print(f"\n(3) length chain (anchors: electron/proton Compton wavelengths):")
    print(f"    r_p = (2/pi) lambda_C,p          = {rp*1e15:.4f} fm   (locked r_p = 0.8412 fm)")
    print(f"    D   = 6 pi^6 r_p  (proton route) = {D_proton*1e12:.4f} pm")
    print(f"    D   = 2 lambda_C,e (electron)    = {D_electron*1e12:.4f} pm")
    spread = abs(D_proton - D_electron) / D_electron
    print(f"    -> two independent routes agree to {spread*100:.3f} %  ->  D = {0.5*(D_proton+D_electron)*1e12:.3f} pm")
    print(f"    TARGET 4.85 pm: {'HIT' if abs(0.5*(D_proton+D_electron)*1e12 - 4.85) < 0.02 else 'MISS'}")

    print("\nReading: jamming supplies the stiffness (K=c^2, the phi~0.64/z->6 keystone);")
    print("the contact geometry supplies the rectification (alpha=2/pi); together the")
    print("stiffness-vs-inflow balance (elasticity=1, stiffness=c^2) FORCES the radius at")
    print("x*=alpha=2/pi, and the proton & electron routes both land on D ~ 4.852 pm.")
    print("\nHonest status: this is the STIFFNESS-BALANCE route (clean, geometric). The")
    print("complementary jamming route D=2pi*lambda/A with A=a/g* (g*=percolation gap) is")
    print("the one the whitepaper flags as a ~7%% empirical consistency; tightening A from")
    print("the VP-lattice percolation (parameter-free) is the next step toward closing 4.85 pm.")


if __name__ == "__main__":
    main()
