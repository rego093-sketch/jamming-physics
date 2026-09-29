
import numpy as np

def make_wavenumbers(N, L=1.0):
    k1d = 2*np.pi*np.fft.fftfreq(N, d=L/N)
    kx, ky = np.meshgrid(k1d, k1d, indexing='ij')
    K2 = kx*kx + ky*ky
    return kx, ky, K2

def sector_mask(kx, ky, theta0, half_angle):
    ang = np.arctan2(ky, kx)
    # wrap angle difference to [-pi, pi]
    d = np.angle(np.exp(1j*(ang - theta0)))
    return (np.abs(d) <= half_angle).astype(float)

def radial_window(kx, ky, k0, sigma_k):
    K = np.sqrt(kx*kx + ky*ky)
    return np.exp(-0.5*((K - k0)/sigma_k)**2)

def dealias_mask(N):
    # 2/3 rule
    cutoff = int(np.floor(N/3.0))
    mask = np.ones((N, N), dtype=float)
    mask[(np.abs(np.fft.fftfreq(N))*N > cutoff)[:,None] | (np.abs(np.fft.fftfreq(N))*N > cutoff)[None,:]] = 0.0
    return mask

def jacobian(psi, omega, L=1.0):
    N = psi.shape[0]
    kx, ky, K2 = make_wavenumbers(N, L)
    # gradients via spectral differentiation
    psi_hat = np.fft.fft2(psi)
    om_hat = np.fft.fft2(omega)
    psi_x = np.fft.ifft2(1j*kx*psi_hat).real
    psi_y = np.fft.ifft2(1j*ky*psi_hat).real
    om_x  = np.fft.ifft2(1j*kx*om_hat).real
    om_y  = np.fft.ifft2(1j*ky*om_hat).real
    return psi_x*om_y - psi_y*om_x

def compute_streamfunction(omega, L=1.0):
    N = omega.shape[0]
    kx, ky, K2 = make_wavenumbers(N, L)
    om_hat = np.fft.fft2(omega)
    psi_hat = np.zeros_like(om_hat, dtype=complex)
    # Invert Laplacian: ∇²ψ = ω -> ψ̂ = -ω̂/K², with zero mean
    mask = K2 != 0
    psi_hat[mask] = -om_hat[mask]/K2[mask]
    psi_hat[~mask] = 0.0
    psi = np.fft.ifft2(psi_hat).real
    return psi, psi_hat

def energy_spectrum(psi_hat, L=1.0, nbins=None):
    N = psi_hat.shape[0]
    kx, ky, K2 = make_wavenumbers(N, L)
    # velocity in spectral: u = (-∂yψ, ∂xψ)
    ux_hat = -1j*ky*psi_hat
    uy_hat =  1j*kx*psi_hat
    Ek_hat = 0.5*(np.abs(ux_hat)**2 + np.abs(uy_hat)**2)
    K = np.sqrt(kx*kx + ky*ky)
    kmax = np.max(K)
    if nbins is None:
        nbins = N//2
    bins = np.linspace(0, kmax, nbins+1)
    which = np.digitize(K.ravel(), bins) - 1
    E = np.zeros(nbins)
    for i in range(nbins):
        mask = which == i
        if np.any(mask):
            E[i] = Ek_hat.ravel()[mask].sum()
    k_centers = 0.5*(bins[:-1] + bins[1:])
    return k_centers, E

def run_dns(N=64, L=1.0, dt=0.005, steps=500, save_every=50, 
            nu=1e-3, alpha=5e-3, 
            k0=8.0, sigma_k=0.5, theta_deg=30.0, Omega=1.0,
            tau=0.5, A0=0.5, sigmaA=0.2, seed=0):
    rng = np.random.default_rng(seed)
    kx, ky, K2 = make_wavenumbers(N, L)
    mask_dealias = dealias_mask(N)
    omega_hat = np.zeros((N,N), dtype=complex)  # start from rest
    theta0 = 0.0
    half_angle = np.deg2rad(theta_deg/2.0)
    # OU state
    A = A0
    sqrt_dt = np.sqrt(dt)

    frames = []
    A2_accum = 0.0
    A2_count = 0

    def forcing_hat(t, A_value):
        theta = Omega * t
        sector = sector_mask(kx, ky, theta, half_angle)
        radial = radial_window(kx, ky, k0, sigma_k)
        f = A_value * sector * radial
        # de-alias and symmetry: real omega -> conjugate symmetry automatically via ifft2
        return f

    def rhs(omega_hat, t, A_value):
        # Physical fields
        omega = np.fft.ifft2(omega_hat).real
        psi, psi_hat = compute_streamfunction(omega, L=L)
        # Nonlinear Jacobian
        J = jacobian(psi, omega, L=L)
        J_hat = np.fft.fft2(J)
        # Linear terms in spectral
        lap_hat = -K2 * omega_hat
        linear = nu * lap_hat - alpha * omega_hat
        # Forcing in spectral (already in spectral shape)
        F_hat = forcing_hat(t, A_value)
        # RHS in spectral
        rhs_hat = -J_hat + linear + F_hat
        # de-alias
        rhs_hat *= mask_dealias
        return rhs_hat

    t = 0.0
    saved = 0
    spectra = []
    for n in range(steps):
        # OU update for A
        dW = rng.normal() * sqrt_dt
        A += (-(A - A0)/tau)*dt + np.sqrt(2*sigmaA**2/tau)*dW
        A2_accum += A*A
        A2_count += 1

        # RK4 on spectral omega_hat
        k1 = rhs(omega_hat, t, A)
        k2 = rhs(omega_hat + 0.5*dt*k1, t + 0.5*dt, A)
        k3 = rhs(omega_hat + 0.5*dt*k2, t + 0.5*dt, A)
        k4 = rhs(omega_hat + dt*k3, t + dt, A)
        omega_hat = omega_hat + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        t += dt

        if (n+1) % save_every == 0:
            omega = np.fft.ifft2(omega_hat).real
            psi, psi_hat = compute_streamfunction(omega, L=L)
            k, E = energy_spectrum(psi_hat, L=L, nbins=N//2)
            spectra.append((k, E))
            saved += 1

    # Average spectrum over saved frames
    if len(spectra) > 0:
        k = spectra[0][0]
        E_avg = np.mean([Ei for _, Ei in spectra], axis=0)
        k_peak = k[np.argmax(E_avg[1:]) + 1]  # avoid k=0
    else:
        k, E_avg, k_peak = np.array([0.0]), np.array([0.0]), 0.0

    stats = {
        "k_peak": float(k_peak),
        "L_star": float(2*np.pi/k_peak if k_peak > 0 else np.nan),
        "A2_mean": float(A2_accum/max(1,A2_count)),
    }
    return k, E_avg, stats
