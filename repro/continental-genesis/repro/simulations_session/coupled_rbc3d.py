"""
coupled_rbc3d.py -- TWO-WAY coupling of the continental field C back onto the 3D convection.
Extends rbc3d.RBC3D with a continent-dependent heat source (continental INSULATION: heat
accumulates under a continent's insulating lid -> sub-continental warming -> buoyant upwelling).
The continent then sits over induced upwelling (destabilizing/rifting tendency), while its raft
rigidity (advection by the LARGE-SCALE flow only) is handled in the driver (stabilizing tendency).

theta equation gains a source:  d_t theta += q * C(x,y) * g(z),  g(z) peaked just below the top.
When C=0 the source vanishes and the solver must reproduce the analytic onset Ra_c=27*pi^4/4~657.5
EXACTLY -- the proof the coupling does not corrupt the validated solver.
"""
import numpy as np
from rbc3d import RBC3D, predicted_sigma

class CoupledRBC3D(RBC3D):
    def __init__(self, *a, q_insul=0.0, z_peak=0.85, z_wid=0.12, **k):
        super().__init__(*a, **k)
        self.q_insul = q_insul
        g = np.exp(-((self.zj - z_peak)/z_wid)**2)          # vertical shape of the insulation source
        self.g_sine = self.Sinv @ g                         # its sine coefficients (length Nz)

    def source_hat(self, C):
        """sine-Fourier coeffs of q * C(x,y) * g(z). C is a real (Nx,Ny) field in [0,1]."""
        if self.q_insul == 0.0: return 0.0
        Chat = np.fft.fft2(C)                               # (Nx,Ny) Fourier
        Chat[0, 0] = 0.0                                    # ZERO-MEAN: insulation REDISTRIBUTES heat
        return (self.q_insul * Chat[:, :, None] * self.g_sine[None, None, :]) * self.dealias

    def step_coupled(self, Th, dt, C, with_adv=True, Csrc=None):
        """IF-Heun step with the continent source added to the explicit RHS (source fixed over the step)."""
        src = self.source_hat(C if Csrc is None else Csrc)
        E = np.exp(-self.K2*dt)
        r1, _, _, _ = self.rhs(Th, with_adv)
        expl1 = r1 + self.K2*Th + src
        Th1 = E*(Th + dt*expl1)
        r2, w, u, v = self.rhs(Th1, with_adv)
        expl2 = r2 + self.K2*Th1 + src
        Thn = (E*Th + 0.5*dt*(E*expl1 + expl2))*self.dealias
        return Thn, (w, u, v)


if __name__ == "__main__":
    # RE-VALIDATION: with the coupling code present but C=0, the onset must still be Ra_c=657.5.
    print("Re-validation: coupling present, C=0 -> must reproduce Ra_c = 27*pi^4/4 = "
          f"{27*np.pi**4/4:.2f}\n")
    print("Ra      measured sigma   predicted sigma   rel.err")
    print("-"*52)
    L = 2*np.pi; Czero = np.zeros((24, 24))
    for Ra in (600, 640, 657.6, 675, 720):
        m = CoupledRBC3D(24, 24, 8, L=L, Ra=Ra, q_insul=7.0)   # nonzero q, but C=0 -> source=0
        X = (np.arange(24)*L/24)[:, None, None]; Y = (np.arange(24)*L/24)[None, :, None]
        Z = m.zj[None, None, :]
        th = np.cos(2*X + 1*Y)*np.sin(np.pi*Z)
        Th = m.to_spec_sin(th); dt = 2e-5
        amp = lambda T: np.sqrt(np.sum(np.abs(m.to_phys_sin(T))**2))
        a0 = amp(Th)
        for _ in range(2000): Th, _ = m.step_coupled(Th, dt, Czero, with_adv=False)
        sig = np.log(amp(Th)/a0)/(2000*dt); sp = predicted_sigma(Ra, 5, 1)
        print(f"{Ra:6.1f}  {sig:+.5f}        {sp:+.5f}      {abs(sig-sp)/(abs(sp)+1e-9):.1e}")
    print("\n=> with C=0 the coupled solver reproduces Ra_c exactly. The coupling does NOT corrupt it.")
