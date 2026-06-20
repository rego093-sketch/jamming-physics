"""
length_selection.py — Verification of the dynamical length-selection law that
anchors the thesis "a length is specified by arrangement" (the JFM/PRF line).

Dispersion of a binding(k^2)-vs-penalty(k^4) competition:
        lambda(k) = mu + eps k^2 - sigma k^4 ,   eps, sigma > 0
Stationarity d lambda/dk = 0  =>  k_star = sqrt(eps / (2 sigma)),
hence the SELECTED length
        L_star = 2 pi / k_star = 2 pi sqrt(2 sigma / eps)  ~  (sigma/eps)^{1/2},
INDEPENDENT of the growth offset mu. The control exponent is therefore exactly
        d log L_star / d log(sigma/eps) = 1/2     (the "one-half law").

This module verifies (i) the analytic extremum and its mu-independence, and
(ii) that a fully nonlinear 2D Swift-Hohenberg pattern saturates onto k_star and
reproduces the 1/2 exponent. Everything is fixed by (mu, eps, sigma, seed).
"""
import numpy as np

def k_star(eps, sigma):
    """Analytic selected wavenumber."""
    return np.sqrt(eps / (2.0 * sigma))

def selected_k_nonlinear(mu, eps, sigma, wavelengths=12, N=128, T=12.0, dt=0.005, seed=1):
    """Integrate 2D Swift-Hohenberg  d_t psi = (mu + eps lap - sigma lap^2) psi - psi^3
    via IF-RK2; return the spectral-peak wavenumber of the saturated pattern."""
    kp = k_star(eps, sigma)
    L = wavelengths * (2.0 * np.pi / kp)
    rng = np.random.default_rng(seed)
    dx = L / N
    k1 = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx = k1[:, None]; ky = k1[None, :]; k2 = kx**2 + ky**2
    lam = mu + eps * k2 - sigma * k2**2
    psi = 0.01 * rng.standard_normal((N, N)); ph = np.fft.fft2(psi)
    E1 = np.exp(lam * dt)
    nl = lambda P: np.fft.fft2(-np.real(np.fft.ifft2(P))**3)
    for _ in range(int(T / dt)):
        N1 = nl(ph); a = E1 * ph + dt * E1 * N1; N2 = nl(a)
        ph = E1 * ph + 0.5 * dt * (E1 * N1 + N2)
    psi = np.real(np.fft.ifft2(ph))
    P = np.abs(np.fft.fft2(psi))**2; P[0, 0] = 0.0
    kr = np.sqrt(k2).ravel(); Pr = P.ravel()
    kb = np.linspace(0.05, np.abs(k1).max(), 120)
    idx = np.digitize(kr, kb)
    spec = np.array([Pr[idx == i].sum() for i in range(1, len(kb))])
    kc = 0.5 * (kb[1:] + kb[:-1])
    return kc[np.argmax(spec)]

def one_half_law(cases=((1.0, 0.15), (1.0, 0.25), (1.0, 0.4), (0.6, 0.4), (0.5, 0.5)),
                 mu=0.1):
    """Return measured slope d log L_star / d log(sigma/eps) from nonlinear runs."""
    ratios, Ls = [], []
    for eps, sigma in cases:
        ks = selected_k_nonlinear(mu, eps, sigma)
        ratios.append(sigma / eps); Ls.append(2.0 * np.pi / ks)
    slope = np.polyfit(np.log(ratios), np.log(Ls), 1)[0]
    return slope

if __name__ == "__main__":
    print("[T1] analytic extremum, mu-independence:")
    for mu in (-0.5, 0.0, 0.5):
        k = np.linspace(0.01, 5, 200000); lam = mu + 1.0 * k**2 - 0.25 * k**4
        print(f"   mu={mu:+.1f}: k*_analytic={k_star(1.0,0.25):.5f}  argmax={k[np.argmax(lam)]:.5f}")
    print(f"[T2] nonlinear one-half law: slope = {one_half_law():.4f}  (theory 0.5; JFM beta_hat~0.501)")
