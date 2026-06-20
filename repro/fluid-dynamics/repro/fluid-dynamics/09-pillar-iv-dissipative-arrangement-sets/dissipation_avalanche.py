# -*- coding: utf-8 -*-
"""
dissipation_avalanche.py -- P4 of the open-problems memo, EXECUTED.

CLAIM UNDER TEST (framework prediction, NEW and falsifiable).
If the dissipation events of developed 3D turbulence are local unjamming
avalanches of the marginal substrate (Pillar IV x Section 3), the thresholded
dissipation structures must obey the marginal-stability avalanche law

    P(s) ~ s^{-tau},   tau = 2 - theta/(1+theta) * d/d_f      (Lin-Wyart),

with stationary 3D theta ~ 0.5-0.6 and sheet-like structures d_f ~ 2, giving the
PRE-REGISTERED band tau ~ 1.4-1.5 -- and crucially NOT an exponential (an
intrinsic scale would falsify the identification).

METHOD. Develop forced 3D turbulence with the validated ns3d solver (inviscid
energy conserved to machine precision; velocity-derivative skewness -> ~ -0.5,
the canonical developed value). Compute the full-resolution local dissipation
eps(x) = 2 nu S_ij S_ij from spectral strain. Threshold at h*<eps>; extract
PERIODIC connected components (6-connectivity + union-find across the three
periodic face pairs); record component volume s. Pool over decorrelated
snapshots. Fit tau by maximum likelihood (Clauset-Shalizi-Newman, discrete,
KS-selected lower cutoff s_min) cross-checked by logarithmic-bin regression;
measure the structure fractal dimension d_f (gyration radius vs volume on
non-wrapping components) to confirm the sheet-like input; verify power-law over
exponential by a log-likelihood ratio. No tuning: thresholds and fit ranges are
reported across a grid and the prediction band is fixed in advance.
"""
import numpy as np, time
from scipy import ndimage
import ns3d as S


# ----------------------------------------------------------------------------- #
#  dissipation field (full resolution, spectral strain)                         #
# ----------------------------------------------------------------------------- #
def dissipation_field(uh, vh, wh, g, nu):
    """eps(x) = 2 nu sum_ij S_ij^2, S_ij = 1/2 (d_i u_j + d_j u_i)."""
    kk = [g['kx'], g['ky'], g['kz']]
    uh3 = [uh, vh, wh]
    du = [[S.Fi(1j * kk[i] * uh3[j]) for j in range(3)] for i in range(3)]
    eps = np.zeros_like(du[0][0])
    for i in range(3):
        for j in range(3):
            Sij = 0.5 * (du[i][j] + du[j][i])
            eps += Sij * Sij
    return 2.0 * nu * eps


# ----------------------------------------------------------------------------- #
#  periodic connected components (6-connectivity)                               #
# ----------------------------------------------------------------------------- #
def _union_find(n):
    parent = list(range(n + 1))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return find, union


def periodic_components(binary):
    """Label binary array with PERIODIC boundaries (6-conn). Return (merged_label
    array, sizes dict {root: volume}, wraps set of roots that touch a periodic
    seam)."""
    struct = ndimage.generate_binary_structure(3, 1)          # 6-connectivity
    lab, n = ndimage.label(binary, structure=struct)
    if n == 0:
        return lab, {}, set()
    find, union = _union_find(n)
    wraps = set()
    for axis in range(3):
        lo = [slice(None)] * 3; hi = [slice(None)] * 3
        lo[axis] = 0; hi[axis] = -1
        a = lab[tuple(lo)]; b = lab[tuple(hi)]
        m = (a > 0) & (b > 0)
        for va, vb in zip(a[m].tolist(), b[m].tolist()):
            union(va, vb); wraps.add(va); wraps.add(vb)
    roots = np.array([find(i) for i in range(n + 1)])
    counts = np.bincount(lab.ravel(), minlength=n + 1)
    sizes = {}
    for i in range(1, n + 1):
        r = roots[i]; sizes[r] = sizes.get(r, 0) + int(counts[i])
    wrap_roots = {find(w) for w in wraps}
    return roots[lab], sizes, wrap_roots


# ----------------------------------------------------------------------------- #
#  power-law fitting                                                            #
# ----------------------------------------------------------------------------- #
def _discrete_alpha(x, xmin):
    """Discrete-power-law MLE exponent (Clauset et al. eq. B.17 approximation)."""
    x = x[x >= xmin]
    n = len(x)
    if n < 10:
        return np.nan, n
    alpha = 1.0 + n / np.sum(np.log(x / (xmin - 0.5)))
    return alpha, n


def _ks_distance_discrete(x, xmin, alpha):
    """KS distance between empirical CDF and a discrete power law, x>=xmin."""
    x = np.sort(x[x >= xmin])
    n = len(x)
    if n < 10:
        return np.inf
    xs = np.arange(xmin, x.max() + 1)
    # zeta tail via direct sum (sizes are bounded by the grid, so this is finite)
    w = xs.astype(float) ** (-alpha)
    cdf_model = np.cumsum(w) / np.sum(w)
    # empirical CDF evaluated on xs
    emp = np.searchsorted(x, xs, side='right') / n
    return np.max(np.abs(cdf_model - emp))


def clauset_fit(sizes, xmin_grid=None):
    """Scan xmin, choose the value minimizing KS distance; return dict."""
    x = np.asarray(sizes, dtype=float)
    x = x[x >= 2]                                              # drop singletons (1 cell)
    if xmin_grid is None:
        lo, hi = 2, int(np.percentile(x, 90))
        xmin_grid = np.unique(np.round(np.geomspace(lo, max(hi, lo + 1), 18)).astype(int))
    best = None
    for xmin in xmin_grid:
        a, n = _discrete_alpha(x, xmin)
        if not np.isfinite(a) or n < 30:
            continue
        ks = _ks_distance_discrete(x, xmin, a)
        if best is None or ks < best['ks']:
            se = (a - 1.0) / np.sqrt(n)
            best = dict(alpha=a, se=se, xmin=int(xmin), ntail=n, ks=ks)
    return best


def logbin_fit(sizes, xmin, xmax, nbins=14):
    """Log-binned PDF slope over [xmin, xmax]: P(s) ~ s^{-tau}."""
    x = np.asarray(sizes, dtype=float)
    x = x[(x >= xmin) & (x <= xmax)]
    if len(x) < 30:
        return np.nan, np.nan, 0
    edges = np.geomspace(xmin, xmax, nbins + 1)
    cnt, _ = np.histogram(x, bins=edges)
    width = np.diff(edges)
    centers = np.sqrt(edges[:-1] * edges[1:])
    pdf = cnt / (width * len(x))
    ok = cnt >= 5
    if ok.sum() < 4:
        return np.nan, np.nan, int(ok.sum())
    lx, ly = np.log(centers[ok]), np.log(pdf[ok])
    A = np.vstack([lx, np.ones_like(lx)]).T
    coef, res, *_ = np.linalg.lstsq(A, ly, rcond=None)
    slope = coef[0]
    yhat = A @ coef
    ss_res = np.sum((ly - yhat) ** 2); ss_tot = np.sum((ly - ly.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return -slope, r2, int(ok.sum())


def exp_vs_power_llr(sizes, xmin):
    """Log-likelihood ratio (per point) between power law and exponential for
    x>=xmin. Positive favors power law. Returns (LLR_per_point, sign)."""
    x = np.asarray(sizes, dtype=float)
    x = x[x >= xmin]
    n = len(x)
    if n < 30:
        return np.nan
    a, _ = _discrete_alpha(x, xmin)
    xs = np.arange(xmin, x.max() + 1).astype(float)
    Zp = np.sum(xs ** (-a))
    ll_p = -a * np.log(x) - np.log(Zp)
    lam = 1.0 / (x.mean() - xmin + 1.0)                       # exp MLE rate (shifted)
    Ze = np.sum(np.exp(-lam * (xs - xmin)))
    ll_e = -lam * (x - xmin) - np.log(Ze)
    return float(np.mean(ll_p - ll_e))


def fractal_dim(merged_label, sizes, wrap_roots, vmin=20):
    """d_f from gyration radius vs volume on NON-wrapping components (V ~ Rg^d_f)."""
    roots = [r for r, v in sizes.items() if v >= vmin and r not in wrap_roots]
    if len(roots) < 12:
        return np.nan, np.nan, 0
    Rg, V = [], []
    for r in roots:
        coords = np.argwhere(merged_label == r).astype(float)
        c = coords.mean(0)
        rg = np.sqrt(np.mean(np.sum((coords - c) ** 2, axis=1)))
        if rg > 0:
            Rg.append(rg); V.append(coords.shape[0])
    Rg = np.log(np.array(Rg)); V = np.log(np.array(V))
    A = np.vstack([Rg, np.ones_like(Rg)]).T
    coef, *_ = np.linalg.lstsq(A, V, rcond=None)
    yhat = A @ coef
    ss_res = np.sum((V - yhat) ** 2); ss_tot = np.sum((V - V.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return coef[0], r2, len(roots)


# ----------------------------------------------------------------------------- #
#  driver                                                                       #
# ----------------------------------------------------------------------------- #
def develop(N, nu, dt, nsteps, seed=1, log=print):
    g = S.grid(N); uh, vh, wh = S.randIC(N, g, seed=seed)
    t0 = time.time()
    for _ in range(nsteps):
        uh, vh, wh = S.force(uh, vh, wh, g); uh, vh, wh = S.step(uh, vh, wh, g, nu, dt)
    sk = S.skewness(uh, g); Z = S.enstrophy(uh, vh, wh, g)
    log(f"  developed N={N} nu={nu}: skewness={sk:+.2f}, Z={Z:.1f}, "
        f"eps={2*nu*Z:.3f}  ({time.time()-t0:.0f}s)")
    return uh, vh, wh, g, sk


def collect(N, nu, dt, nsteps, nsnap, gap, thresholds, seed=1, log=print):
    """Develop, then collect nsnap snapshots separated by `gap` steps; pool
    component volumes per threshold."""
    uh, vh, wh, g, sk = develop(N, nu, dt, nsteps, seed=seed, log=log)
    pooled = {h: [] for h in thresholds}
    frac = {h: [] for h in thresholds}
    last = None
    for s in range(nsnap):
        for _ in range(gap):
            uh, vh, wh = S.force(uh, vh, wh, g); uh, vh, wh = S.step(uh, vh, wh, g, nu, dt)
        eps = dissipation_field(uh, vh, wh, g, nu)
        em = eps.mean()
        for h in thresholds:
            ml, sizes, wraps = periodic_components(eps > h * em)
            pooled[h].extend(sizes.values())
            df, r2df, ndf = fractal_dim(ml, sizes, wraps)
            if np.isfinite(df):
                frac[h].append((df, ndf))
        last = (eps, em)
    return pooled, frac, sk, g, last


if __name__ == "__main__":
    # quick pipeline validation on a small, fast developed field
    print("== pipeline validation (N=48, fast) ==")
    pooled, frac, sk, g, last = collect(
        N=48, nu=0.010, dt=0.005, nsteps=300, nsnap=3, gap=30,
        thresholds=[1.0, 2.0])
    for h in (1.0, 2.0):
        sizes = np.array(pooled[h])
        fit = clauset_fit(sizes)
        if fit:
            tau_lb, r2, nb = logbin_fit(sizes, fit['xmin'], sizes.max())
            llr = exp_vs_power_llr(sizes, fit['xmin'])
            dfm = np.mean([d for d, _ in frac[h]]) if frac[h] else np.nan
            print(f"  h={h}: nstruct={len(sizes)}  tau_MLE={fit['alpha']:.3f}"
                  f"+-{fit['se']:.3f} (xmin={fit['xmin']}, ntail={fit['ntail']}, "
                  f"KS={fit['ks']:.3f})  tau_logbin={tau_lb:.3f} (R2={r2:.3f})  "
                  f"LLR(pl/exp)={llr:+.3f}  d_f={dfm:.2f}")
        else:
            print(f"  h={h}: insufficient structures ({len(sizes)})")
    print("  (validation only -- production numbers come from the N=64 run below)")
