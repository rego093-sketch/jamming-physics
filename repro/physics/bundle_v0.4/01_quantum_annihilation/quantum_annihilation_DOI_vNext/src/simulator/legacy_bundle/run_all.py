\
"""
run_all.py

한 번에 결과(CSV) + 이미지(PNG)를 생성합니다.
- 2D 토이(목 임계) -> results/, images/
- 3D 재밍 격자에서 δ_eff=g* 및 A 스윕 -> results/, images/
- SOC(자기조직화 임계 퍼콜레이션) -> results/, images/
- (추가) 재밍 떨림의 회전 스케일(4.85 pm) -> results/, images/
"""

import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

def main():
    # 2D toy
    from toy_2d_neck_threshold import main as toy_main
    toy_main(out_dir=ROOT)

    # 3D percolation extraction
    from lattice_3d_jam_percolation import main as real3d_main
    real3d_main(out_dir=ROOT, N=200, seed=17, k_nn=12, target_far=0.80)

    # SOC run (g0=2e-7: aiming for A~1e6)
    from soc_percolation_pinning import run_soc
    run_soc(out_dir=ROOT, N=200, seed=2, steps=9000,
            eps_init=4e-5,
            drive_step=8e-8,
            release_scale=1.0e-5,
            target_far=0.80,
            g0=2e-7,
            kick_sigma_factor=10.0,
            eps_min=-2e-3,
            eps_max=1.2e-4,
            k_nn=12)


    # MST Option–B unit realisation (633 nm anchor) + RCROSS(532)
    from mst_optionb_unit_realization import run as mst_run
    mst_run(root=ROOT)

    # Visible-wave carrier demo on the realised lattice (sparse sampling)
    from lattice_visible_wave_emergence import run as wave_run
    wave_run(root=ROOT)


    # Jamming rotation scale study (4.85 pm) from SOC avalanche A_post
    from jamming_rotation_485pm_study import main as rot_main
    rot_main(out_dir=ROOT)

if __name__ == "__main__":
    main()