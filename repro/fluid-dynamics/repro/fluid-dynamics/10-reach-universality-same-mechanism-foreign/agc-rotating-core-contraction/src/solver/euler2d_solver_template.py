"""
Minimal template for a 2D compressible Euler solver (HLLC-based).

- State vector: [rho, rho*u, rho*v, E]
- EOS: ideal gas / Tait / stiffened gas (select via eos_type)
- Boundary: rotating cylinder via ghost-cell BC

실제 구현은 논문 및 내부 보고서의 수치해석 섹션을 참고하여 작성하십시오.
"""

import numpy as np


class CompressibleEulerSolver:
    def __init__(self, nx, ny, eos_type="ideal"):
        self.nx = nx
        self.ny = ny
        self.eos_type = eos_type
        self.U = np.zeros((4, nx, ny))

    def compute_fluxes(self):
        """Implement HLLC or other Riemann solver here."""
        raise NotImplementedError

    def apply_boundary_conditions(self):
        """Implement rotating-wall ghost-cell BC here."""
        raise NotImplementedError

    def step(self, dt):
        """Advance one time step (e.g. RK2/RK3)."""
        raise NotImplementedError
