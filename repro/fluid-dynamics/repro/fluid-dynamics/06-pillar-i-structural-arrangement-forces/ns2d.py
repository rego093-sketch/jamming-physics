"""
ns2d.py — Self-contained, deterministic pseudo-spectral 2D Navier-Stokes solver
(vorticity form) for the VP fluid-dynamics whitepaper reproducibility program.

PDE (doubly periodic box, side L=2*pi):
    d_t w + (u . grad) w = nu * lap w        (no forcing -> decaying turbulence)
    lap psi = -w ,  u = d_y psi ,  v = -d_x psi   (sign convention w = v_x - u_y)

Diagnostics:
    Z(t)        = 1/2 <w^2>            (enstrophy, area-averaged)
    eps_nu(t)   = 2 nu Z(t)            (viscous enstrophy dissipation = - dE-spectral... see notes)
    E(t)        = 1/2 <|u|^2>          (kinetic energy)
    Urms(t)     = sqrt(<|u|^2>)
    Re_eff(t)   = Urms(t) * L / nu

Numerics: 2/3 dealiasing, RK4 with exact integrating factor on the viscous term
(stable for the viscous part at any dt). Everything below is fixed by (N, nu, seed).
"""
import numpy as np

L = 2.0 * np.pi

def _wavenumbers(N):
    k1 = np.fft.fftfreq(N, d=1.0 / N)          # integer wavenumbers 0,1,...,-1
    kx = k1[:, None] * np.ones((1, N))
    ky = np.ones((N, 1)) * k1[None, :]
    k2 = kx**2 + ky**2
    k2_inv = 1.0 / np.where(k2 == 0, 1.0, k2)
    k2_inv[0, 0] = 0.0
    return kx, ky, k2, k2_inv

def _dealias_mask(N):
    k1 = np.fft.fftfreq(N, d=1.0 / N)
    kmax = N / 3.0
    m1 = np.abs(k1) <= kmax
    return m1[:, None] & m1[None, :]

def initial_vorticity(N, seed, k_peak=3.0, target_Z=1.476):
    """Band-limited isotropic random vorticity, fixed seed, normalized so 1/2<w^2>=target_Z.
    Spectrum amplitude ~ k * exp(-(k/k_peak)^2) with random phases (Hermitian-symmetric via rfft route)."""
    rng = np.random.default_rng(seed)
    kx, ky, k2, _ = _wavenumbers(N)
    kk = np.sqrt(k2)
    # random complex field, then shape its spectrum
    phase = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
    amp = (kk) * np.exp(-(kk / k_peak) ** 2)
    amp[0, 0] = 0.0
    w_hat = phase * amp
    # enforce reality by symmetrizing in physical space
    w = np.real(np.fft.ifft2(w_hat))
    w -= w.mean()
    Z = 0.5 * np.mean(w**2)
    w *= np.sqrt(target_Z / Z)
    return w

def _rhs_nonlinear(w_hat, kx, ky, k2_inv, mask):
    """Return FFT of -(u.grad)w (dealiased). Viscous term handled separately."""
    psi_hat = w_hat * k2_inv
    u_hat = 1j * ky * psi_hat        # u =  d_y psi
    v_hat = -1j * kx * psi_hat       # v = -d_x psi
    wx_hat = 1j * kx * w_hat
    wy_hat = 1j * ky * w_hat
    u = np.real(np.fft.ifft2(u_hat)); v = np.real(np.fft.ifft2(v_hat))
    wx = np.real(np.fft.ifft2(wx_hat)); wy = np.real(np.fft.ifft2(wy_hat))
    adv = u * wx + v * wy
    adv_hat = np.fft.fft2(adv) * mask
    return -adv_hat

def diagnostics(w_hat, kx, ky, k2_inv, nu):
    psi_hat = w_hat * k2_inv
    u_hat = 1j * ky * psi_hat
    v_hat = -1j * kx * psi_hat
    u = np.real(np.fft.ifft2(u_hat)); v = np.real(np.fft.ifft2(v_hat))
    w = np.real(np.fft.ifft2(w_hat))
    E = 0.5 * np.mean(u**2 + v**2)
    Z = 0.5 * np.mean(w**2)
    Urms = np.sqrt(np.mean(u**2 + v**2))
    eps_nu = 2.0 * nu * Z
    Re_eff = Urms * L / nu if nu > 0 else float("nan")
    return dict(E=E, Z=Z, Urms=Urms, eps_nu=eps_nu, Re_eff=Re_eff)

def run(N, nu, seed=12345, T=10.0, dt=None, k_peak=3.0, target_Z=1.476,
        sample_every=1, t0_window=2.0):
    """Integrate to time T. Returns time series dict. Window for <Re_eff> is [t0_window, T]."""
    kx, ky, k2, k2_inv = _wavenumbers(N)
    mask = _dealias_mask(N)
    if dt is None:
        # advective CFL-ish: dt ~ c * dx / Umax; dx=2pi/N, Umax~O(1)
        dt = 0.25 * (L / N) / 1.0
    w = initial_vorticity(N, seed, k_peak=k_peak, target_Z=target_Z)
    w_hat = np.fft.fft2(w)
    nsteps = int(round(T / dt))
    # integrating factor for viscosity over dt and dt/2
    Lop = -nu * k2
    E1 = np.exp(Lop * dt); E2 = np.exp(Lop * dt / 2.0)
    ts, Zs, Es, Urs, eps, Res = [], [], [], [], [], []
    def record(t):
        d = diagnostics(w_hat, kx, ky, k2_inv, nu)
        ts.append(t); Zs.append(d['Z']); Es.append(d['E'])
        Urs.append(d['Urms']); eps.append(d['eps_nu']); Res.append(d['Re_eff'])
    record(0.0)
    for n in range(nsteps):
        # Integrating-factor RK4 (derived in repro notes); E1=exp(L dt), E2=exp(L dt/2)
        N1 = _rhs_nonlinear(w_hat, kx, ky, k2_inv, mask)
        W1 = E2 * (w_hat + 0.5 * dt * N1)
        N2 = _rhs_nonlinear(W1, kx, ky, k2_inv, mask)
        W2 = E2 * w_hat + 0.5 * dt * N2
        N3 = _rhs_nonlinear(W2, kx, ky, k2_inv, mask)
        W3 = E1 * w_hat + dt * E2 * N3
        N4 = _rhs_nonlinear(W3, kx, ky, k2_inv, mask)
        w_hat = E1 * w_hat + (dt / 6.0) * (E1 * N1 + 2 * E2 * N2 + 2 * E2 * N3 + N4)
        t = (n + 1) * dt
        if (n + 1) % sample_every == 0:
            record(t)
    out = dict(t=np.array(ts), Z=np.array(Zs), E=np.array(Es),
               Urms=np.array(Urs), eps_nu=np.array(eps), Re_eff=np.array(Res),
               N=N, nu=nu, seed=seed, dt=dt, T=T)
    win = out['t'] >= t0_window
    out['Re_eff_winmean'] = float(np.mean(out['Re_eff'][win]))
    out['max_eps_nu'] = float(np.max(out['eps_nu']))
    out['Z0'] = float(out['Z'][0])
    return out

if __name__ == "__main__":
    o = run(64, 0.005, T=10.0)
    print(f"N=64 nu=0.005: Z0={o['Z0']:.5f} max_eps={o['max_eps_nu']:.6g} "
          f"<Re_eff>={o['Re_eff_winmean']:.3f}")
