\
"""
toy_2d_neck_threshold.py

2D 장난감 모델:
- 반지름 R인 이동 원(입자)이
- 반지름 R인 고정 원 4개가 만든 "목(neck)"을 통과할 수 있는지
- 마찰 0 / 탄성 1을 가정한 '겹치면 밀어내는' (스프링) 반발력으로 근사
- 임계 속도/에너지(대략적인 E_min)를 스캔/이분법으로 추정

출력:
- results/toy2d_threshold_scan.csv
- images/toy2d_trajectory.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def simulate(v0, R=1.0, d=1.6, k_spring=1e5, dt=1e-4, t_max=2.0, mass=1.0,
             x0=0.0, y0=-4.0, y_pass=4.0):
    fixed_centers = np.array([[ d,0.0],[-d,0.0],[0.0, d],[0.0,-d]], dtype=float)
    pos = np.array([x0,y0], float)
    vel = np.array([0.0,v0], float)
    steps = int(t_max/dt)
    for _ in range(steps):
        # force at pos
        F = np.zeros(2)
        for c in fixed_centers:
            r_vec = pos - c
            dist = float(np.linalg.norm(r_vec))
            overlap = 2*R - dist
            if overlap > 0 and dist > 1e-12:
                F += k_spring * overlap * (r_vec/dist)

        acc = F/mass
        # velocity verlet
        pos = pos + vel*dt + 0.5*acc*dt*dt

        F2 = np.zeros(2)
        for c in fixed_centers:
            r_vec = pos - c
            dist = float(np.linalg.norm(r_vec))
            overlap = 2*R - dist
            if overlap > 0 and dist > 1e-12:
                F2 += k_spring * overlap * (r_vec/dist)
        acc2 = F2/mass
        vel = vel + 0.5*(acc+acc2)*dt

        # pass criterion
        if pos[1] > y_pass and vel[1] > 0:
            return True, pos, vel
        # crude fail criterion
        if pos[1] < y0-0.5 and vel[1] < 0:
            return False, pos, vel
    return False, pos, vel

def trajectory(v0, R=1.0, d=1.6, k_spring=1e5, dt=1e-4, t_max=2.0, mass=1.0,
               x0=0.0, y0=-4.0):
    fixed_centers = np.array([[ d,0.0],[-d,0.0],[0.0, d],[0.0,-d]], dtype=float)
    pos = np.array([x0,y0], float)
    vel = np.array([0.0,v0], float)
    steps = int(t_max/dt)
    xs=[]; ys=[]
    for _ in range(steps):
        xs.append(pos[0]); ys.append(pos[1])
        F = np.zeros(2)
        for c in fixed_centers:
            r_vec = pos - c
            dist = float(np.linalg.norm(r_vec))
            overlap = 2*R - dist
            if overlap > 0 and dist > 1e-12:
                F += k_spring * overlap * (r_vec/dist)
        acc = F/mass
        pos = pos + vel*dt + 0.5*acc*dt*dt

        F2 = np.zeros(2)
        for c in fixed_centers:
            r_vec = pos - c
            dist = float(np.linalg.norm(r_vec))
            overlap = 2*R - dist
            if overlap > 0 and dist > 1e-12:
                F2 += k_spring * overlap * (r_vec/dist)
        acc2 = F2/mass
        vel = vel + 0.5*(acc+acc2)*dt
    return np.array(xs), np.array(ys), fixed_centers

def main(out_dir="../"):
    out_dir = os.path.abspath(out_dir)
    results_dir = os.path.join(out_dir, "results")
    images_dir = os.path.join(out_dir, "images")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    R = 1.0
    d = 1.6
    opening_width = 2*d - 2*R

    # scan
    v_scan = np.linspace(5.0, 80.0, 16)
    scan_rows=[]
    for v0 in v_scan:
        passed, pos, vel = simulate(v0, R=R, d=d)
        scan_rows.append([v0, int(passed), pos[0], pos[1], vel[0], vel[1]])
    scan_path = os.path.join(results_dir, "toy2d_threshold_scan.csv")
    np.savetxt(scan_path, np.array(scan_rows), delimiter=",",
               header="v0,passed,x,y,vx,vy", comments="")

    # binary search threshold
    lo, hi = 5.0, 80.0
    for _ in range(24):
        mid = 0.5*(lo+hi)
        passed, *_ = simulate(mid, R=R, d=d)
        if passed:
            hi = mid
        else:
            lo = mid
    v_th = hi
    E_th = 0.5 * 1.0 * v_th**2

    # save summary txt
    summary_path = os.path.join(results_dir, "toy2d_threshold_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"R={R}\n")
        f.write(f"d={d}\n")
        f.write(f"opening_width=2d-2R={opening_width}\n")
        f.write(f"estimated v_threshold={v_th}\n")
        f.write(f"estimated E_threshold={E_th}\n")

    # plot a trajectory near threshold
    xs, ys, fixed = trajectory(v_th, R=R, d=d)
    theta = np.linspace(0, 2*np.pi, 240)
    plt.figure()
    for c in fixed:
        plt.plot(c[0]+R*np.cos(theta), c[1]+R*np.sin(theta))
    plt.plot(xs, ys)
    plt.gca().set_aspect("equal", "box")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"2D neck trajectory near threshold v≈{v_th:.2f}")
    img_path = os.path.join(images_dir, "toy2d_trajectory.png")
    plt.savefig(img_path, dpi=200, bbox_inches="tight")
    plt.close()

    print("wrote:", scan_path)
    print("wrote:", summary_path)
    print("wrote:", img_path)

if __name__ == "__main__":
    main()
