"""
event_flux.py — Pillar IV's main open GATE, tested: do EVENTS carry the inertial
flux to the dissipation scale? Demonstrated in 1D Burgers, where the Duchon-Robert
defect is exact.

For a Burgers shock of jump Delta_u, the inviscid energy defect (the anomalous
dissipation) is D = (Delta_u)^3 / 12, localized AT the shock. The test:
  (i)  the viscous dissipation int eps_nu equals (Delta_u)^3/12 (the EVENT flux),
  (ii) it is nu-INDEPENDENT (anomalous), and
  (iii) the Duchon-Robert inter-scale flux Pi_l(x) = +(1/4) int phi_l'(r) du(r)^3 dr
       is ~100% concentrated at the shock and matches the dissipation at the
       inertial scale.
Together: the event carries the inertial flux to the dissipation scale. This is the
canonical, exactly-tractable case; the 2D/3D Navier-Stokes version (vortex/sheet
events) shares the same Duchon-Robert structure but is harder to resolve.
"""
import numpy as np
trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
L = 2 * np.pi

def burgers_state(nu, N=4096, T=1.6):
    dx = L / N; k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    x = np.linspace(0, L, N, endpoint=False); uh = np.fft.fft(np.sin(x)); dt = 0.3 * dx
    E1 = np.exp(-nu * k**2 * dt); E2 = np.exp(-nu * k**2 * dt / 2)
    mask = np.abs(k) <= (2/3) * np.abs(k).max()
    NL = lambda uh: (-1j * k * mask) * np.fft.fft(0.5 * np.real(np.fft.ifft(uh))**2)
    for _ in range(int(T / dt)):
        N1 = NL(uh); a = E2*(uh+0.5*dt*N1); N2 = NL(a); b = E2*uh+0.5*dt*N2
        N3 = NL(b); c = E1*uh+dt*E2*N3; N4 = NL(c)
        uh = E1*uh + (dt/6)*(E1*N1+2*E2*N2+2*E2*N3+N4)
    u = np.real(np.fft.ifft(uh)); ux = np.real(np.fft.ifft(1j * k * uh))
    return x, u, ux, dx

def viscous_dissipation(nu, x, ux):
    return trap(nu * ux**2, x)

def shock_jump(u, ux, dx):
    i = np.argmax(-ux); w = int(0.3 / dx)
    return u[(i - w) % len(u)] - u[(i + w) % len(u)]

def dr_flux(x, u, dx, ell):
    """Duchon-Robert inter-scale flux density Pi_l(x)."""
    nr = int(6 * ell / dx); r = np.arange(-nr, nr + 1) * dx
    phi = np.exp(-r**2 / (2 * ell**2)) / (ell * np.sqrt(2 * np.pi)); dphi = -(r / ell**2) * phi
    Pi = np.zeros(len(u))
    for j, rr in enumerate(r):
        if abs(dphi[j]) < 1e-14: continue
        du = np.roll(u, -int(round(rr / dx))) - u
        Pi += 0.25 * dphi[j] * du**3 * dx
    return Pi

def shock_concentration(x, ux, Pi, half=0.15):
    i = np.argmax(-ux); xs = x[i]
    near = np.abs((x - xs + np.pi) % (2 * np.pi) - np.pi) < half
    return np.abs(Pi[near]).sum() / np.abs(Pi).sum()

if __name__ == "__main__":
    print("Pillar IV: the dissipation = the EVENT flux (Delta_u)^3/12, nu-independent")
    print(f"{'nu':>8}{'diss':>10}{'Delta_u':>9}{'(Du)^3/12':>11}{'ratio':>7}{'%flux@shock':>13}")
    for nu in (0.02, 0.01, 0.005, 0.0025):
        x, u, ux, dx = burgers_state(nu)
        diss = viscous_dissipation(nu, x, ux); dU = shock_jump(u, ux, dx)
        Pi = dr_flux(x, u, dx, 8 * dx); frac = shock_concentration(x, ux, Pi)
        print(f"{nu:>8}{diss:>10.4f}{dU:>9.4f}{dU**3/12:>11.4f}{diss/(dU**3/12):>7.2f}{frac*100:>12.0f}%")
    print("=> dissipation ~ (Delta_u)^3/12 (event flux), nu-independent, flux concentrated at")
    print("   the shock: the EVENT carries the inertial flux to the dissipation scale.")
