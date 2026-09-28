# JAMMING VERIFICATION INDEX — 통합 색인 (v0.4.0)

이 통합 번들은 VP 잼밍-기질 이론의 재현성 코드/결과를 **두 검증 경로**로 담는다.
각 결과의 **정본(canonical)** 위치와 버전을 아래에 고정한다.

| 결과 | 정본 모듈 | 버전 | 비고 |
|---|---|---|---|
| α=2/π, δ=1/π², 2π=α/δ, 정수코어 81=3⁴/21 | `…/jamming_spine_verification_v0.4_2026-06-05/06_constants_scales_geometry/verify_constants_and_scales.py` | **v0.4** | 스케일분리·offset 명시 강화 (구 final_verification.py) |
| 부피탄성률 B 직접 측정, c²=B/ρ | `…/v0.4…/01_stiffness_to_c2/bulk.py` (+ relaxed_shear.py) | **v0.4** | 신규: B 직접 |
| **relaxed 전단탄성률 G→0 @ z_iso=2d=6 (5 독립 관측량)** | `…/v0.4…/02_shear_relaxedG/relaxed_shear.py` (+ le_shear, aqs, collect_spectra) | **v0.4** | **신규** — 메인백서 §5 미해결 종결 |
| 강제 양성자 반경 r_p=(2/π)λ_Cp 끌개, F'(x*)=−(π/2)⁵ | `…/v0.4…/03_forced_circle_proton_radius/forced_circle_attractor.py` | **v0.4** | 위상선·전역성 강화 (구 stiffness_size.py) |
| 회전 그라인더 자기제한 코어, x*∼1/Ω | `…/v0.4…/04_rotating_grinder/vp_grinder_3d.py` | **v0.4** | 재구현 (구 proton_formation_3d.py) |
| 양자 지름 D=2πλ/A | `…/v0.4…/05_light_emergence_quantum_D/ellrot_verify.py` | **v0.4** | A 원본은 v0.3/AQD 정본 의존(deps/README 참조) |
| 증폭 A=a_med/g* (격자 출력), A-스케일링 N=750 | `…/jamming_rotation_verification_v0.3/modules/verify_amplification_A.py`, `…/lattice_percolation_soc_bundle/…/soc_N750/` | v0.3 | **유지** — N=750 대형런은 v0.3가 정본 |

## 버전 관계
- **v0.4(2026-06-05)** 가 잼밍-기질 *역학* 검증의 정본이다. 특히 02 relaxed-G(5관측량)는 v0.3에 없던 신규 결과로, 백서의 "단일속도 c²=B/ρ" 주춧돌을 단언에서 검증으로 끌어올린다.
- **v0.3** 은 (i) N=750 증폭 A 대형런과 (ii) 19개 모듈의 광범위 검증 기록을 위해 **유지**한다.
- LOCK 상수는 두 버전에서 **불변**. v0.4는 [V] 기록의 추가일 뿐 기존 결론을 바꾸지 않는다.

## 정직한 경계 (객관)
- 검증됨(역학): c²=B/ρ 단일속도, relaxed-G→0(5관측량), 강제 반경 전역끌개, 회전이 크기 창발, A=격자출력.
- 정의 의존(수치): 3π⁴·6π⁵·6π⁶ 은 [MAP-1]("섹터 lock 1개=π²") 한 점에 의존(α·δ와 동일 지위). 6π⁶은 6π⁵의 변장.
- 앵커 의존(스케일): 절대 pm 값은 단일 앵커 λ=632.99nm + A_geo=cΔt/a 교차검증(0.16%).
- 열린 3고리: (1) 회전→정확히 z=2d, (2) [MAP-1] 기하 유도, (3) Δt의 c-독립성.
