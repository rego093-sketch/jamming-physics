\
"""
lattice_3d_jam_percolation.py

3D 재밍(무작위 조밀충전) 격자 생성 + 퍼콜레이션 기반 δ_eff := g* 추출 + A=a/δ_eff 계산.
- 주기경계(L=1) 박스
- 단분산 구(모두 동일 반지름)
- 재밍 근처를 만드는 데는 소프트-스피어(FIRE) 최소화 + 반지름 이분탐색(근사)
- 격자는 kNN=12 그래프로 근사
- g* : 0<gap<=g_cut 에지들만으로 소스에서 FAR 노드 비율(target_far) 도달 가능한 최소 g_cut

출력:
- results/real3d_eps_sweep.csv
- images/real3d_A_vs_eps.png
- images/real3d_delta_vs_eps.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import heapq

def min_image(d, L=1.0):
    return d - L*np.rint(d/L)

def forces_energy(pos, R, L=1.0):
    d = pos[:, None, :] - pos[None, :, :]
    d = min_image(d, L)
    r2 = np.einsum("ijk,ijk->ij", d, d)
    np.fill_diagonal(r2, np.inf)
    r = np.sqrt(r2)
    overlap = 2*R - r
    mask = overlap > 0
    E = 0.25*np.sum(overlap[mask]**2)
    fcoef = np.zeros_like(r)
    fcoef[mask] = overlap[mask]/r[mask]
    F = np.einsum("ij,ijk->ik", fcoef, d)
    return E, F

def fire_minimize(pos, R, L=1.0, max_steps=1600, ftol=2e-10):
    pos = pos.copy()
    v = np.zeros_like(pos)
    dt = 2e-3
    dt_max = 5e-2
    alpha = 0.1
    alpha0 = 0.1
    finc, fdec, falpha = 1.1, 0.5, 0.99
    N_min = 5
    n_pos = 0
    for _ in range(max_steps):
        E, F = forces_energy(pos, R, L)
        maxF = float(np.max(np.linalg.norm(F, axis=1)))
        if maxF < ftol:
            return pos, E, maxF
        v += dt*F
        vnorm = np.linalg.norm(v)
        fnorm = np.linalg.norm(F)
        power = float(np.sum(v*F))
        if vnorm > 0 and fnorm > 0:
            v = (1-alpha)*v + alpha*(vnorm/fnorm)*F
        if power > 0:
            n_pos += 1
            if n_pos > N_min:
                dt = min(dt*finc, dt_max)
                alpha *= falpha
        else:
            n_pos = 0
            dt *= fdec
            alpha = alpha0
            v[:] = 0.0
        pos = (pos + dt*v) % L
    return pos, E, maxF

def find_jam_radius(pos0, L=1.0, phi_guess=0.64, it_bis=18):
    N = pos0.shape[0]
    R_guess = (phi_guess / (N*(4/3)*np.pi))**(1/3)
    R_low, R_high = 0.75*R_guess, 1.25*R_guess
    pos_low, E_low, *_ = fire_minimize(pos0, R_low, L)
    pos_high, E_high, *_ = fire_minimize(pos_low, R_high, L)

    def is_unjam(E): return E < 1e-12
    def is_jam(E):   return E > 1e-8

    for _ in range(6):
        if is_unjam(E_low): break
        R_low *= 0.9
        pos_low, E_low, *_ = fire_minimize(pos0, R_low, L)
    for _ in range(6):
        if is_jam(E_high): break
        R_high *= 1.1
        pos_high, E_high, *_ = fire_minimize(pos_low, R_high, L)

    Ra, pos_a, Ea = R_low, pos_low, E_low
    Rb, pos_b, Eb = R_high, pos_high, E_high
    for _ in range(it_bis):
        Rm = 0.5*(Ra+Rb)
        pos_start = pos_a if abs(Rm-Ra) < abs(Rm-Rb) else pos_b
        pos_m, Em, *_ = fire_minimize(pos_start, Rm, L, max_steps=1800, ftol=2e-10)
        if is_unjam(Em):
            Ra, pos_a, Ea = Rm, pos_m, Em
        else:
            Rb, pos_b, Eb = Rm, pos_m, Em
    return Rb, pos_b

def knn_graph(pos, k_nn=12, L=1.0):
    d = pos[:, None, :] - pos[None, :, :]
    d = min_image(d, L)
    r2 = np.einsum("ijk,ijk->ij", d, d)
    np.fill_diagonal(r2, np.inf)
    r = np.sqrt(r2)
    nn = np.argpartition(r, kth=k_nn, axis=1)[:, :k_nn]
    dist = np.take_along_axis(r, nn, axis=1)
    return nn.astype(np.int32), dist

def g_star_exact(nbr, dist, R, src, far_mask, target_far=0.8):
    """
    Exact g* by binary search over sorted positive gaps.
    Uses undirected-ish reachability on directed kNN edges.
    """
    gap = dist - 2*R
    gpos = gap[gap > 0].ravel()
    g_sorted = np.sort(gpos)
    lo, hi = 0, len(g_sorted)-1
    best = float(g_sorted[-1])

    N = nbr.shape[0]
    far_total = int(np.sum(far_mask))

    def reach(g0):
        seen = np.zeros(N, dtype=bool)
        st = [int(src)]
        seen[int(src)] = True
        while st:
            i = st.pop()
            gi = gap[i]; ni = nbr[i]
            m = (gi > 0) & (gi <= g0)
            for nxt in ni[m]:
                nxt = int(nxt)
                if not seen[nxt]:
                    seen[nxt] = True
                    st.append(nxt)
        return seen

    while lo <= hi:
        mid = (lo+hi)//2
        g0 = float(g_sorted[mid])
        seen = reach(g0)
        frac_far = float(np.sum(seen & far_mask) / far_total) if far_total else 0.0
        if frac_far >= target_far:
            best = g0
            hi = mid - 1
        else:
            lo = mid + 1
    return best

def dijkstra_times(nbr, gap, src):
    N, k = nbr.shape
    t = np.full(N, np.inf)
    t[src] = 0.0
    pq = [(0.0, int(src))]
    while pq:
        ti, i = heapq.heappop(pq)
        if ti != t[i]:
            continue
        gi = gap[i]; ni = nbr[i]
        for j in range(k):
            g = float(gi[j])
            if g <= 0:
                continue
            nxt = int(ni[j])
            tj = ti + g  # v0=1 units
            if tj < t[nxt]:
                t[nxt] = tj
                heapq.heappush(pq, (tj, nxt))
    return t

def envelope_speed(dist_src, t_arr, rmin=0.08, rmax=0.48, nbins=12):
    mask = np.isfinite(t_arr) & (t_arr > 0)
    r = dist_src[mask]; t = t_arr[mask]
    bins = np.linspace(rmin, rmax, nbins+1)
    xc=[]; tc=[]
    for i in range(nbins):
        m = (r >= bins[i]) & (r < bins[i+1])
        if np.any(m):
            xc.append(0.5*(bins[i]+bins[i+1]))
            tc.append(np.min(t[m]))
    xc=np.array(xc); tc=np.array(tc)
    if len(xc) < 6:
        return np.nan
    A_fit = np.vstack([xc, np.ones_like(xc)]).T
    slope, b = np.linalg.lstsq(A_fit, tc, rcond=None)[0]
    return 1.0/slope

def main(out_dir="../", N=200, seed=17, k_nn=12, target_far=0.80):
    out_dir = os.path.abspath(out_dir)
    results_dir = os.path.join(out_dir, "results")
    images_dir = os.path.join(out_dir, "images")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    np.random.seed(seed)
    pos0 = np.random.rand(N,3)

    R_jam, pos = find_jam_radius(pos0, it_bis=18)
    phi = N*(4/3)*np.pi*R_jam**3

    center = np.array([0.5,0.5,0.5])
    src = int(np.argmin(np.sum(min_image(pos-center)**2, axis=1)))

    nbr, dist = knn_graph(pos, k_nn=k_nn)
    a_med = float(np.median(dist))

    dist_src = np.linalg.norm(min_image(pos - pos[src]), axis=1)
    far_mask = dist_src >= 0.35

    # sweep eps near jamming
    eps_list = np.array([2e-6, 1.5e-6, 1.2e-6, 1.0e-6, 8e-7, 6e-7, 5e-7, 4e-7], float)

    rows=[]
    for eps in eps_list:
        R = R_jam*(1-eps)
        gap = dist - 2*R
        gstar = g_star_exact(nbr, dist, R, src, far_mask, target_far=target_far)
        A = a_med/gstar
        K = A**2
        t_arr = dijkstra_times(nbr, gap, src)
        c_env = envelope_speed(dist_src, t_arr)
        rows.append([eps, gstar, gstar/a_med, A, K, phi, R_jam, a_med, c_env, c_env/A])

    rows = np.array(rows, float)
    csv_path = os.path.join(results_dir, "real3d_eps_sweep.csv")
    np.savetxt(csv_path, rows, delimiter=",",
               header="eps,delta_eff,delta_over_a,A,K,phi_jam,R_jam,a_med,c_env,c_env_over_A", comments="")

    # plots
    plt.figure()
    plt.loglog(rows[:,0], rows[:,3], marker="o", linestyle="none")
    plt.gca().invert_xaxis()
    plt.xlabel("eps (decompression from jam)")
    plt.ylabel("A = a/δ_eff")
    plt.title("Amplification A from 3D jammed lattice (percolation g*)")
    plt.savefig(os.path.join(images_dir, "real3d_A_vs_eps.png"), dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.loglog(rows[:,0], rows[:,2], marker="o", linestyle="none")
    plt.gca().invert_xaxis()
    plt.xlabel("eps")
    plt.ylabel("δ_eff/a")
    plt.title("Effective neck ratio δ_eff/a from 3D lattice")
    plt.savefig(os.path.join(images_dir, "real3d_delta_vs_eps.png"), dpi=200, bbox_inches="tight")
    plt.close()

    # save run summary
    summary = {
        "N": int(N), "seed": int(seed),
        "k_nn": int(k_nn), "target_far": float(target_far),
        "R_jam": float(R_jam), "phi_jam": float(phi),
        "a_med": float(a_med), "src": int(src),
        "csv": os.path.basename(csv_path)
    }
    with open(os.path.join(results_dir, "real3d_run_summary.json"), "w", encoding="utf-8") as f:
        import json
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("wrote:", csv_path)
    print("wrote images:", "real3d_A_vs_eps.png", "real3d_delta_vs_eps.png")
    print("summary:", summary)

if __name__ == "__main__":
    main()
