"""
axioms.py — Verification of the axiomatic core (treatise Part II), the foundation
the four pillars rest on.

(1) U2 conservation structure. The Ward two-body kernel
        U2 = A(r) + B(r)(L_i.L_j) + C(r)(L_i.rhat)(L_j.rhat)
    gives a CENTRAL pairwise force; total force = 0, so momentum P is conserved.
    In 2D the C-term vanishes (L || z, rhat _|_ z), leaving a pure central force.

(2) No-Go theorem. A pure two-body U2 potential conserves P, so the centre of mass
    cannot accelerate: a co-rotating pair has NO self-propulsion. A real 2D dipole
    DOES self-propel, by its Biot-Savart (Kelvin) impulse v = Gamma/(2 pi d) -- a
    degree of freedom no pairwise potential possesses. Two bodies are not enough.

(3) U3 2D reduction. The parity-even triple-product
        S_ijk = sum_cyc L_i . (r_ij x r_ik)
    reduces in 2D to  S_ijk = 2 A_tri (L_i + L_j + L_k), with A_tri the signed
    triangle area. Because A_tri depends on all three vertices, the third core
    mediates a TRANSVERSE force on the (i,j) pair CM -- the self-propulsion channel
    the No-Go theorem forbids to two bodies. The triangle is the irreducible unit.
"""
import numpy as np

cross_z = lambda a, b: a[0] * b[1] - a[1] * b[0]   # z-component of 2D cross product

# ---------------------------------------------------------------- (1)
def U2_forces(X, L, A=np.exp, Ap=lambda r: -np.exp(-r),
              Bp=lambda r: -0.5 * np.exp(-r)):
    """Central pairwise forces from U2 = A(r)+B(r) L_i L_j (2D). Returns array of forces."""
    n = len(X); F = np.zeros_like(X)
    for i in range(n):
        for j in range(n):
            if i == j: continue
            d = X[i] - X[j]; r = np.hypot(d[0], d[1]); rhat = d / r
            F[i] += -(Ap(r) + Bp(r) * L[i] * L[j]) * rhat   # along rhat => central
    return F

def u2_is_central_and_conservative(seed=0):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, (2, 2)); L = np.array([1.0, 1.0])
    F = U2_forces(X, L); rhat = (X[0] - X[1]) / np.hypot(*(X[0] - X[1]))
    return abs(cross_z(F[0], rhat)), np.linalg.norm(F.sum(0))   # (non-centrality, |sum F|)

# ---------------------------------------------------------------- (2)
def nogo_cm_displacement(seed=1, steps=2000, dt=2e-3):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, (2, 2)); L = np.array([1.0, 1.0]); V = np.zeros_like(X); X0 = X.mean(0)
    for _ in range(steps):
        F = U2_forces(X, L); V += dt * F; X += dt * V
    return np.linalg.norm(X.mean(0) - X0)        # ~0 : no self-propulsion

def dipole_self_propulsion_speed(Gamma=1.0, d=1.0):
    return Gamma / (2 * np.pi * d)               # Kelvin impulse, != 0

# ---------------------------------------------------------------- (3)
def S_direct(X, L):
    i, j, k = 0, 1, 2
    return (L[i] * cross_z(X[j] - X[i], X[k] - X[i])
            + L[j] * cross_z(X[k] - X[j], X[i] - X[j])
            + L[k] * cross_z(X[i] - X[k], X[j] - X[k]))

def signed_area(X):
    return 0.5 * cross_z(X[1] - X[0], X[2] - X[0])

def u3_reduction_error(seed=2, trials=5):
    rng = np.random.default_rng(seed); e = 0.0
    for _ in range(trials):
        X = rng.uniform(-2, 2, (3, 2)); L = rng.uniform(-2, 2, 3)
        e = max(e, abs(S_direct(X, L) - 2 * signed_area(X) * L.sum()))
    return e

def u3_transverse_force(X=None, L=None, d0=1.0, ell=2.0, h=1e-6):
    if X is None: X = np.array([[0., 0.], [1., 0.], [0.4, 0.9]])
    if L is None: L = np.array([1., 1., 1.])
    def U3(Xq):
        P = (np.hypot(*(Xq[1]-Xq[0])) + np.hypot(*(Xq[2]-Xq[1])) + np.hypot(*(Xq[0]-Xq[2])))
        return d0 * np.exp(-P / ell) * S_direct(Xq, L)
    Fcm = np.zeros(2)
    for a in range(2):
        e = np.zeros(2); e[a] = h; Xp = X.copy(); Xm = X.copy()
        Xp[0] += e; Xp[1] += e; Xm[0] -= e; Xm[1] -= e
        Fcm[a] = -(U3(Xp) - U3(Xm)) / (2 * h)
    r01 = (X[1] - X[0]); r01 = r01 / np.hypot(*r01)
    return np.linalg.norm(Fcm), abs(cross_z(Fcm, r01))   # (|F|, transverse component)

if __name__ == "__main__":
    nc, sumF = u2_is_central_and_conservative()
    print(f"(1) U2: non-centrality |F x rhat|={nc:.1e}, |sum F|={sumF:.1e}  -> central, P conserved")
    print(f"(2) No-Go: 2-body CM displacement={nogo_cm_displacement():.1e} (~0, no self-propulsion);")
    print(f"          real dipole self-propels at v={dipole_self_propulsion_speed():.4f} != 0")
    print(f"(3) U3 reduction: max|S - 2 A_tri (sum L)|={u3_reduction_error():.1e} (machine precision)")
    F, Ft = u3_transverse_force()
    print(f"    U3 force on pair CM: |F|={F:.4f}, transverse={Ft:.4f} != 0 -> self-propulsion restored")
