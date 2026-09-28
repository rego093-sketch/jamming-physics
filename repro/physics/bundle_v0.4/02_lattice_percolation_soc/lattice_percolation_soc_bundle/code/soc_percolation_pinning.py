\
"""
soc_percolation_pinning.py

SOC(자기조직화 임계 퍼콜레이션) 루프:
- 실제 3D 재밍 격자(무작위 조밀충전)에서 시작
- 빠른 에지 기준 g0 고정: gap<=g0 이면 '활성(빠름)'
- 느린 압축(ε 감소)으로 임계(예: FAR 80% 도달)를 향해 이동
- 임계 도달 시: 연결 클러스터에 작은 킥 + 겹침 제거(FIRE 최소화) + ε 완화(증가)
- 반복하면 g* (퍼콜레이션 임계 목갭)가 g0 근처로 pinning 되는지 관측

출력:
- results/soc_run3_timeseries.csv
- results/soc_run3_avalanches.csv
- images/soc_run3_*.png
"""

import os, json, heapq
import numpy as np
import matplotlib.pyplot as plt

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

def fire_minimize(pos, R, L=1.0, max_steps=900, ftol=2e-7):
    pos = pos.copy()
    v = np.zeros_like(pos)
    dt = 2e-3
    dt_max = 4e-2
    alpha = 0.12
    alpha0 = 0.12
    finc, fdec, falpha = 1.1, 0.5, 0.99
    N_min = 5
    n_pos = 0
    for _ in range(max_steps):
        E, F = forces_energy(pos, R, L)
        maxF = float(np.max(np.linalg.norm(F, axis=1)))
        if maxF < ftol:
            return pos
        v += dt * F
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
    return pos

def find_jam_radius(pos0, L=1.0, phi_guess=0.64, it_bis=14):
    N = pos0.shape[0]
    R_guess = (phi_guess / (N*(4/3)*np.pi))**(1/3)
    R_low, R_high = 0.8*R_guess, 1.2*R_guess
    pos_low = fire_minimize(pos0, R_low, L)
    pos_high = fire_minimize(pos_low, R_high, L)

    def energy(pos, R):
        E, _ = forces_energy(pos, R, L)
        return E

    E_low = energy(pos_low, R_low)
    E_high = energy(pos_high, R_high)

    def is_unjam(E): return E < 1e-12
    def is_jam(E):   return E > 1e-6

    for _ in range(4):
        if is_unjam(E_low): break
        R_low *= 0.92
        pos_low = fire_minimize(pos0, R_low, L)
        E_low = energy(pos_low, R_low)

    for _ in range(4):
        if is_jam(E_high): break
        R_high *= 1.08
        pos_high = fire_minimize(pos_low, R_high, L)
        E_high = energy(pos_high, R_high)

    Ra, pos_a, Ea = R_low, pos_low, E_low
    Rb, pos_b, Eb = R_high, pos_high, E_high

    for _ in range(it_bis):
        Rm = 0.5*(Ra+Rb)
        pos_start = pos_a if abs(Rm-Ra) < abs(Rm-Rb) else pos_b
        pos_m = fire_minimize(pos_start, Rm, L)
        Em = energy(pos_m, Rm)
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

def reachable_fast(nbr, dist, R, g0, src):
    # active if dist <= 2R + g0 (gap<=g0, overlaps 포함)
    thresh = 2*R + g0
    N, k = nbr.shape
    seen = np.zeros(N, dtype=bool)
    st = [int(src)]
    seen[int(src)] = True
    while st:
        i = st.pop()
        m = dist[i] <= thresh
        for nxt in nbr[i][m]:
            nxt = int(nxt)
            if not seen[nxt]:
                seen[nxt] = True
                st.append(nxt)
    return seen

def g_star_exact(nbr, dist, R, src, far_mask, target=0.8):
    # gap_pos := max(dist-2R, 0) 값들 중 최소 임계값을 이진탐색
    gap_pos = np.maximum(dist - 2*R, 0.0).ravel()
    g_sorted = np.sort(gap_pos)
    lo, hi = 0, len(g_sorted)-1
    best = float(g_sorted[-1])
    far_total = int(np.sum(far_mask))

    def far_fraction(seen):
        return float(np.sum(seen & far_mask)/far_total) if far_total else 0.0

    while lo <= hi:
        mid = (lo+hi)//2
        g0 = float(g_sorted[mid])
        seen = reachable_fast(nbr, dist, R, g0, src)
        if far_fraction(seen) >= target:
            best = g0
            hi = mid - 1
        else:
            lo = mid + 1
    return best

def run_soc(out_dir="../",
            N=200, seed=2, steps=9000,
            eps_init=4e-5,
            drive_step=8e-8,
            release_scale=1.0e-5,
            target_far=0.80,
            g0=2e-7,
            kick_sigma_factor=10.0,
            eps_min=-2e-3,
            eps_max=1.2e-4,
            k_nn=12):
    out_dir = os.path.abspath(out_dir)
    results_dir = os.path.join(out_dir, "results")
    images_dir = os.path.join(out_dir, "images")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    L = 1.0
    np.random.seed(seed)
    pos0 = np.random.rand(N,3)*L
    R_jam, pos = find_jam_radius(pos0, L=L, it_bis=14)
    phi_jam = N*(4/3)*np.pi*R_jam**3

    # src near center
    center = np.array([0.5,0.5,0.5])
    src = int(np.argmin(np.sum(min_image(pos-center, L)**2, axis=1)))

    nbr, dist = knn_graph(pos, k_nn=k_nn, L=L)
    a_med = float(np.median(dist))
    dist_src = np.linalg.norm(min_image(pos - pos[src], L), axis=1)
    far_mask = dist_src >= 0.35

    sigma = float(kick_sigma_factor * g0)

    eps = float(eps_init)
    eps_log = np.zeros(steps)
    far_log = np.zeros(steps)

    av_sizes=[]; av_eps=[]; av_gstar=[]; av_A=[]
    for t in range(steps):
        R = R_jam*(1-eps)
        seen = reachable_fast(nbr, dist, R, g0, src)
        far_total = int(np.sum(far_mask))
        ff = float(np.sum(seen & far_mask)/far_total) if far_total else 0.0

        eps_log[t]=eps
        far_log[t]=ff

        if ff >= target_far:
            cluster = np.where(seen)[0]
            S = int(len(cluster))
            av_sizes.append(S)
            av_eps.append(eps)

            # kick and relax
            pos[cluster] = (pos[cluster] + sigma*np.random.randn(S,3)) % L
            pos = fire_minimize(pos, R, L=L, max_steps=900, ftol=2e-7)

            # rebuild graph and masks
            nbr, dist = knn_graph(pos, k_nn=k_nn, L=L)
            a_med = float(np.median(dist))
            dist_src = np.linalg.norm(min_image(pos - pos[src], L), axis=1)
            far_mask = dist_src >= 0.35

            gstar = g_star_exact(nbr, dist, R, src, far_mask, target=target_far)
            A = a_med/gstar if gstar > 0 else float("inf")
            av_gstar.append(gstar)
            av_A.append(A)

            # dissipation
            eps += release_scale*(S/N)
            eps = min(eps, eps_max)
        else:
            eps -= drive_step
            eps = max(eps, eps_min)

    # save CSVs
    ts_path = os.path.join(results_dir, "soc_run3_timeseries.csv")
    np.savetxt(ts_path, np.column_stack([np.arange(steps), eps_log, far_log]),
               delimiter=",", header="step,eps,far_reach_fraction", comments="")

    av_path = os.path.join(results_dir, "soc_run3_avalanches.csv")
    if len(av_sizes) > 0:
        av = np.column_stack([
            np.arange(len(av_sizes)),
            np.array(av_sizes, int),
            np.array(av_eps, float),
            np.array(av_gstar, float),
            np.array(av_A, float),
        ])
        np.savetxt(av_path, av, delimiter=",",
                   header="av_idx,size_S,eps_at_trigger,gstar_post,A_post", comments="")
    else:
        np.savetxt(av_path, np.zeros((0,5)), delimiter=",",
                   header="av_idx,size_S,eps_at_trigger,gstar_post,A_post", comments="")

    # save summary json
    summary = {
        "N": int(N), "seed": int(seed), "steps": int(steps),
        "R_jam": float(R_jam), "phi_jam": float(phi_jam),
        "k_nn": int(k_nn), "target_far": float(target_far),
        "g0": float(g0), "sigma": float(sigma),
        "eps_init": float(eps_init), "drive_step": float(drive_step),
        "release_scale": float(release_scale),
        "eps_min": float(eps_min), "eps_max": float(eps_max),
        "n_avalanches": int(len(av_sizes)),
        "A_median": float(np.median(av_A)) if len(av_A) else None,
        "A_p10": float(np.quantile(av_A, 0.1)) if len(av_A) else None,
        "A_p90": float(np.quantile(av_A, 0.9)) if len(av_A) else None,
        "gstar_over_g0_median": float(np.median(np.array(av_gstar)/g0)) if len(av_gstar) else None,
    }
    with open(os.path.join(results_dir, "soc_run3_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # plots (no explicit colors)
    plt.figure()
    plt.plot(eps_log)
    plt.xlabel("step")
    plt.ylabel("eps")
    plt.title("SOC: eps(t)")
    plt.savefig(os.path.join(images_dir, "soc_run3_eps_t.png"), dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(far_log)
    plt.axhline(target_far, linestyle="--")
    plt.xlabel("step")
    plt.ylabel("FAR reach fraction (gap<=g0)")
    plt.title("SOC: percolation criterion hits and relaxes")
    plt.savefig(os.path.join(images_dir, "soc_run3_far_hits.png"), dpi=200, bbox_inches="tight")
    plt.close()

    if len(av_sizes) > 0:
        plt.figure()
        plt.plot(av_gstar, marker="o", linestyle="none")
        plt.axhline(g0, linestyle="--")
        plt.xlabel("avalanche index")
        plt.ylabel("g* (post-avalanche)")
        plt.title("SOC: g* pinning around g0")
        plt.savefig(os.path.join(images_dir, "soc_run3_gstar_pinning.png"), dpi=200, bbox_inches="tight")
        plt.close()

        plt.figure()
        plt.plot(av_A, marker="o", linestyle="none")
        plt.xlabel("avalanche index")
        plt.ylabel("A=a/g*")
        plt.title("SOC: amplification A")
        plt.savefig(os.path.join(images_dir, "soc_run3_A.png"), dpi=200, bbox_inches="tight")
        plt.close()

    print("wrote:", ts_path)
    print("wrote:", av_path)
    print("wrote images: soc_run3_eps_t.png, soc_run3_far_hits.png, soc_run3_gstar_pinning.png, soc_run3_A.png")
    print("summary:", summary)

    return summary

def main(out_dir="../"):
    run_soc(out_dir=out_dir)

if __name__ == "__main__":
    main()
