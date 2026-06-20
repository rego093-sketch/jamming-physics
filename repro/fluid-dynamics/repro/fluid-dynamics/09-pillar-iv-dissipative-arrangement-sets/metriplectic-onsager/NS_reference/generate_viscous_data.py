"""Navier--Stokes reference data for the viscous dissipation curve.

This script implements a modest 2D pseudo-spectral solver for decaying
Navier--Stokes turbulence in a periodic box.  It is intentionally
minimal and tuned for qualitative agreement with standard 2D scaling
(effective Reynolds number increases as viscosity decreases and the
peak viscous dissipation decreases accordingly).

Running this file regenerates

- ``NS_reference/viscous_dissipation_vs_Re.csv``
- ``NS_reference/viscous_dissipation_vs_Re.png``

which are used by :mod:`src.plot_dissipation_saturation`.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulation parameters (kept moderate for accessibility)
N = 64             # grid resolution
L = 2.0 * np.pi    # domain size
t_max = 2.0
dt = 0.002
n_vortices = 20
vortex_radius = 0.2
viscosities = [0.05, 0.02, 0.01, 0.005]


@dataclass
class TwoDNS:
    N: int
    L: float
    nu: float

    def __post_init__(self) -> None:
        self.dx = self.L / self.N
        x = np.arange(self.N) * self.dx
        self.X, self.Y = np.meshgrid(x, x)

        k = 2.0 * np.pi * np.fft.fftfreq(self.N, d=self.dx)
        self.KX, self.KY = np.meshgrid(k, k)
        self.K2 = self.KX ** 2 + self.KY ** 2
        self.K2[0, 0] = 1.0  # avoid divide-by-zero; will reset later

        # 2/3 de-aliasing mask
        kmax = np.max(np.abs(k))
        self.dealias = (np.abs(self.KX) < (2.0 / 3.0) * kmax) & (
            np.abs(self.KY) < (2.0 / 3.0) * kmax
        )

        # allocate vorticity in Fourier space
        self.w_hat = np.zeros((self.N, self.N), dtype=complex)

    # ----- Initial condition -------------------------------------------------
    def initialise_gaussian_vortices(self, n_vortices: int, radius: float) -> None:
        w = np.zeros((self.N, self.N), dtype=float)

        rng = np.random.default_rng(12345)
        for _ in range(n_vortices):
            x0 = rng.random() * self.L
            y0 = rng.random() * self.L
            amp = rng.choice([-1.0, 1.0]) * 10.0

            r2 = (self.X - x0) ** 2 + (self.Y - y0) ** 2
            w += amp * np.exp(-r2 / (radius ** 2))

        # remove mean vorticity
        w -= np.mean(w)
        self.w_hat = np.fft.fft2(w)

    # ----- Helper functions --------------------------------------------------
    def _velocity_from_vorticity(self, w_hat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        psi_hat = -w_hat / self.K2
        psi_hat[0, 0] = 0.0

        u_hat = 1j * self.KY * psi_hat
        v_hat = -1j * self.KX * psi_hat

        u = np.real(np.fft.ifft2(u_hat))
        v = np.real(np.fft.ifft2(v_hat))
        return u, v

    def _rhs(self, w_hat: np.ndarray) -> np.ndarray:
        u, v = self._velocity_from_vorticity(w_hat)

        dw_dx = np.real(np.fft.ifft2(1j * self.KX * w_hat))
        dw_dy = np.real(np.fft.ifft2(1j * self.KY * w_hat))

        nonlinear = -(u * dw_dx + v * dw_dy)
        nl_hat = np.fft.fft2(nonlinear) * self.dealias

        diff_hat = -self.nu * self.K2 * w_hat
        diff_hat[0, 0] = 0.0  # no forcing of mean mode

        return nl_hat + diff_hat

    # ----- Time stepping -----------------------------------------------------
    def step(self, dt: float) -> None:
        k1 = self._rhs(self.w_hat)
        k2 = self._rhs(self.w_hat + 0.5 * dt * k1)
        k3 = self._rhs(self.w_hat + 0.5 * dt * k2)
        k4 = self._rhs(self.w_hat + dt * k3)
        self.w_hat = self.w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    # ----- Diagnostics -------------------------------------------------------
    def diagnostics(self) -> tuple[float, float, float]:
        w = np.real(np.fft.ifft2(self.w_hat))
        Z = 0.5 * np.mean(w ** 2)
        eps_nu = 2.0 * self.nu * Z

        u, v = self._velocity_from_vorticity(self.w_hat)
        U_rms = np.sqrt(np.mean(u ** 2 + v ** 2))
        Re_eff = U_rms * self.L / self.nu
        return Z, eps_nu, Re_eff


def main() -> None:
    results: list[dict[str, float]] = []

    print(f"{'nu':>8}  {'Re_eff (avg)':>12}  {'max eps_nu':>12}")
    print("-" * 38)

    for nu in viscosities:
        sim = TwoDNS(N=N, L=L, nu=nu)
        sim.initialise_gaussian_vortices(n_vortices=n_vortices, radius=vortex_radius)

        n_steps = int(t_max / dt)
        eps_hist: list[float] = []
        Re_hist: list[float] = []

        for step in range(n_steps):
            sim.step(dt)
            if step % 10 == 0:
                _, eps, Re_eff = sim.diagnostics()
                eps_hist.append(eps)
                Re_hist.append(Re_eff)

        max_eps = float(np.max(eps_hist))
        mean_Re = float(np.mean(Re_hist))

        results.append({"nu": nu, "Re_eff": mean_Re, "eps_nu": max_eps})
        print(f"{nu:8.4f}  {mean_Re:12.1f}  {max_eps:12.4e}")

    df = pd.DataFrame(results).sort_values("Re_eff")
    out_csv = pathlib.Path(__file__).resolve().parent / "viscous_dissipation_vs_Re.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved Navier--Stokes viscous data to: {out_csv}")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["Re_eff"], df["eps_nu"], "o--", label=r"$\varepsilon_\nu$ (Navier--Stokes)")
    ax.set_xscale("log")
    ax.set_xlabel(r"Effective Reynolds Number ($Re_{eff}$)")
    ax.set_ylabel("Dissipation Rate")
    ax.set_title("Viscous Dissipation Trend (Navier--Stokes reference)")
    ax.grid(True, which="both", ls="-")
    ax.legend()
    fig.tight_layout()

    plot_path = pathlib.Path(__file__).resolve().parent / "viscous_dissipation_vs_Re.png"
    fig.savefig(plot_path, dpi=300)
    print(f"Saved NS reference plot to: {plot_path}")


if __name__ == "__main__":
    main()
