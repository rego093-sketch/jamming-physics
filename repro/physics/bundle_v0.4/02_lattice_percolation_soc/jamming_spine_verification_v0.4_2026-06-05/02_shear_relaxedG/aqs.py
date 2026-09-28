"""aqs.py -- Athermal Quasi-Static (AQS) simple shear under Lees-Edwards.
Each step: affine increment x_i += dgamma*y_i  +  box tilt gamma += dgamma, then FULLY MINIMIZE at
fixed gamma. Gives the gamma_dot->0 stress-strain curve sigma(gamma): elastic rise (slope = relaxed
shear modulus G_relaxed) -> yield -> steady plateau (yield stress sigma_y). Same harmonic contacts.

Double duty:
  (1) sigma_y(z): the gamma_dot->0 yield stress, vanishing at z_iso=6 (dynamic analog of G->0).
  (2) elastic slope dsigma/dgamma|_0 == G_relaxed  => an INDEPENDENT finite-strain cross-check of the
      static linear-response modulus (HANDOVER §5 step 4).
Reduced units m=1,L=1,d=3,K=0.5.
"""
import numpy as np
from numpy.linalg import norm
from le_shear import forces_stress
d = 3; K = 0.5

def wrap_LE(pos, L, g_box):
    hi = pos[:, 1] >= L; lo = pos[:, 1] < 0
    pos[hi, 0] -= g_box * L; pos[lo, 0] += g_box * L
    pos[:, 1] = pos[:, 1] % L
    pos[:, 0] = pos[:, 0] % L; pos[:, 2] = pos[:, 2] % L
    return pos

def fire_LE(pos, R, L, gamma, steps=4000, ftol=1e-10):
    g_box = gamma - np.floor(gamma)
    pos = wrap_LE(pos.copy(), L, g_box)
    v = np.zeros_like(pos); dt, dm, al, al0 = 2e-3, 5e-2, 0.1, 0.1; npc = 0; mF = 0.0
    for _ in range(steps):
        E, F, sxy, nc = forces_stress(pos, R, L, gamma)
        mF = norm(F, axis=1).max() if len(F) else 0.0
        if mF < ftol: break
        v += dt * F; vn = norm(v); fn = norm(F); pw = float((v * F).sum())
        if vn > 0 and fn > 0: v = (1 - al) * v + al * (vn / fn) * F
        if pw > 0:
            npc += 1
            if npc > 5: dt = min(dt * 1.1, dm); al *= 0.99
        else:
            npc = 0; dt *= 0.5; al = al0; v[:] = 0.0
        pos = pos + dt * v
        pos = wrap_LE(pos, L, g_box)
    E, F, sxy, nc = forces_stress(pos, R, L, gamma)
    return pos, sxy, mF

def aqs_run(pos0, R, L, dgamma=0.003, gamma_max=0.5, fire_steps=4000):
    pos = pos0.copy() % L
    gam = 0.0; gs = []; ss = []; mfs = []
    nsteps = int(round(gamma_max / dgamma))
    for _ in range(nsteps):
        pos[:, 0] += dgamma * pos[:, 1]
        gam += dgamma
        pos = wrap_LE(pos, L, gam - np.floor(gam))
        pos, sxy, mF = fire_LE(pos, R, L, gam, steps=fire_steps)
        gs.append(gam); ss.append(sxy); mfs.append(mF)
    return np.array(gs), np.array(ss), np.array(mfs)
