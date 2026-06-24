"""
corotation.py — The mechanism the 82 = 3^4+1 (C3) structure actually teaches:
how SMALL rotations are FORCED to co-rotate, and how that builds a LARGE rotation
with INFLOW and OUTFLOW. (Not a literal count of vortices in a typhoon.)

The chain, each step demonstrable:

  (1) FORCED CO-ROTATION. Meshing rotors prefer to counter-rotate; a consistent
      counter-rotation is a proper 2-coloring of the contact graph, possible IFF
      the graph is bipartite (no odd cycles). The triangle -- the minimal C3 --
      is an odd cycle, NOT 2-colorable: counter-rotation is frustrated, so the
      rotors must CO-rotate, leaving one unsatisfiable contact = the +1 nozzle.
      Co-rotation makes circulation ADD (N*gamma) rather than cancel.

  (2) CO-ROTATION -> LARGER ROTATION. Like-sign (co-rotating) vortices MERGE into
      a single larger core; opposite-sign do not. (2D Navier-Stokes.)

  (3) LARGE ROTATION -> THROUGH-FLOW. A coherent rotation Omega drives a radial
      inflow in the friction (Ekman) layer; continuity turns it into an axial
      outflow. The transport scales as the Ekman depth sqrt(nu/Omega).

This is scale-free: the same forced-co-rotation-with-nozzle operates on the
quantum lattice (the 82 core) and in macroscopic rotating flows.
"""
import numpy as np
from itertools import product
from scipy.ndimage import label

trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
L = 2 * np.pi

# ----------------------------------------------------------------- (1)
def _two_color_frustration(adj):
    n = len(adj); color = [-1] * n
    for s in range(n):
        if color[s] != -1: continue
        color[s] = 0; stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if color[v] == -1: color[v] = 1 - color[u]; stack.append(v)
    frus = sum(1 for u in range(n) for v in adj[u] if v > u and color[u] == color[v])
    return frus, frus == 0

def _lattice_adj(kind, Lr=6):
    idx = lambda i, j: (i % Lr) * Lr + (j % Lr); adj = [set() for _ in range(Lr * Lr)]
    for i, j in product(range(Lr), range(Lr)):
        nb = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        if kind == "triangular": nb += [(i+1, j+1), (i-1, j-1)]
        for a, b in nb: adj[idx(i, j)].add(idx(a, b))
    return adj

def forced_corotation():
    """Return {lattice: (frustrated_edges, bipartite)} and the triangle (C3) unit."""
    out = {k: _two_color_frustration(_lattice_adj(k)) for k in ("square", "triangular")}
    out["triangle_C3"] = _two_color_frustration([{1, 2}, {0, 2}, {0, 1}])
    return out

# ----------------------------------------------------------------- (2)
def merge_pair(same_sign, N=128, nu=1e-3, T=5.0, d=0.45, r0=0.6, A=2.0):
    """2D NS: return number of connected strong-rotation blobs at time T."""
    dx = L / N; k1 = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kx = k1[:, None] * np.ones((1, N)); ky = np.ones((N, 1)) * k1[None, :]
    k2 = kx**2 + ky**2; k2i = 1 / np.where(k2 == 0, 1, k2); k2i[0, 0] = 0
    m1 = np.abs(k1) <= (2/3) * np.abs(k1).max(); mask = m1[:, None] & m1[None, :]
    x = np.linspace(0, L, N, endpoint=False); X, Y = np.meshgrid(x, x, indexing="ij")
    def g(x0, y0, s):
        dX = X - x0 - L * np.round((X - x0) / L); dY = Y - y0 - L * np.round((Y - y0) / L)
        return s * A * np.exp(-(dX**2 + dY**2) / r0**2)
    w = g(L/2 - d, L/2, 1.0) + g(L/2 + d, L/2, 1.0 if same_sign else -1.0); w -= w.mean()
    wh = np.fft.fft2(w); dt = 0.15 * dx
    E1 = np.exp(-nu * k2 * dt); E2 = np.exp(-nu * k2 * dt / 2)
    def NL(wh):
        ph = wh * k2i; u = np.real(np.fft.ifft2(1j * ky * ph)); v = np.real(np.fft.ifft2(-1j * kx * ph))
        wx = np.real(np.fft.ifft2(1j * kx * wh)); wy = np.real(np.fft.ifft2(1j * ky * wh))
        return -np.fft.fft2(u * wx + v * wy) * mask
    for _ in range(int(T / dt)):
        N1 = NL(wh); a = E2*(wh+0.5*dt*N1); N2 = NL(a); b = E2*wh+0.5*dt*N2
        N3 = NL(b); c = E1*wh+dt*E2*N3; N4 = NL(c)
        wh = E1*wh + (dt/6)*(E1*N1+2*E2*N2+2*E2*N3+N4)
    w = np.real(np.fft.ifft2(wh)); aw = np.abs(w)
    _, nc = label(aw > 0.4 * aw.max()); return nc

# ----------------------------------------------------------------- (3)
def ekman_transport(Omega, nu, W_inf=1.0, Nz=4000, Zmax=12.0):
    """Radial inflow transport of the Ekman layer (feeds the axial outflow)."""
    delta = np.sqrt(nu / Omega); z = np.linspace(0, Zmax * delta, Nz)
    u = np.real(W_inf * (1 - np.exp(-(1 + 1j) * z / delta)))
    return trap(W_inf - u, z), delta

if __name__ == "__main__":
    fc = forced_corotation()
    print("(1) forced co-rotation (counter-rotation = graph 2-coloring):")
    for k in ("square", "triangular", "triangle_C3"):
        frus, bip = fc[k]
        print(f"    {k:12s}: frustrated edges={frus:3d}, bipartite={bip} "
              f"-> {'counter-rotate (net 0)' if bip else 'CO-ROTATE forced (net != 0)'}")
    print("    => circulation ADDS under co-rotation; the one frustrated contact = +1 nozzle.")
    print("(2) co-rotation -> larger rotation (2D Navier-Stokes merger):")
    for same, lab in [(True, "co-rotating"), (False, "opposite  ")]:
        nc = merge_pair(same)
        print(f"    {lab}: strong-rotation blobs = {nc} "
              f"-> {'MERGED to one larger rotation' if nc == 1 else 'stays separate'}")
    print("(3) large rotation -> through-flow (Ekman pumping):")
    Os = np.array([1., 2., 4., 8., 16.]); Ms = np.array([ekman_transport(O, 1e-3)[0] for O in Os])
    s = np.polyfit(np.log(Os), np.log(Ms), 1)[0]
    print(f"    radial inflow transport ~ Omega^{s:+.3f} (theory -1/2, Ekman depth sqrt(nu/Omega))")
    print("    radial inflow -> axial outflow: rotation forces a through-flow (eye updraft).")
    print("CHAIN: forced co-rotation -> merger/large rotation -> inflow & outflow.")
