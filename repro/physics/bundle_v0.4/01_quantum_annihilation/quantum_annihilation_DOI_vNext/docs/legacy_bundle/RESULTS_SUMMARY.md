# 결과 요약(이번 번들에 저장된 CSV/이미지 기준)

## 2D 토이(목 통과 임계)
- 고정 원 4개가 만든 목을 이동 원 1개가 통과하기 위한 v_th(임계 속도)와 E_th를 스캔/이분법으로 찾음.
- 결과는 results/toy2d_threshold_scan.csv 및 images/toy2d_trajectory.png 참고.

## 3D 재밍 격자(단분산, 주기경계)
- 재밍 근처에서 구 배치를 만든 뒤, kNN=12 그래프에서 g* (FAR 80% 퍼콜레이션 임계)를 δ_eff로 정의.
- δ_eff/a ~ 10^-6, A~10^6 규모가 실제 격자에서 자연스럽게 등장함.
- 결과 스윕은 results/real3d_eps_sweep.csv, 그림은 images/real3d_*.png 참고.

## SOC(자기조직화 임계 퍼콜레이션)
- 고정된 미시 임계 g0(빠른 에지 기준) 아래에서,
  느린 압축(ε 감소) + 임계 도달 시 눈사태(킥+최소화) + 완화(ε 증가)
  로 구성된 SOC를 돌려 g*가 g0 근처로 핀닝되는지 확인.
- 결과는 results/soc_run3_timeseries.csv, results/soc_run3_avalanches.csv 와 images/soc_run3_*.png 참고.


## MST Option–B 단위 구현 + RCROSS(633/532 nm)
- SOC 결과에서 구조증폭 계수 A를 추정(A_post의 robust geo-mean).
- 633 nm(아이오딘 안정화 He–Ne)를 운영 닻(Operational Anchor)으로 삼아
  격자 길이 단위 a, 시간 단위 Δt 를 구현.
- 532 nm에 대해 RCROSS 게이트(3-tier dev_max)로 교차 검증.
- 산출물: results/mst_unit_realization.json, results/mst_rcross.csv, images/mst_rcross.png

## 격자에서의 가시광선 캐리어(파동) 데모
- MST로 확정된 (a, Δt) 위에서 633 nm/532 nm 진행파 모드를 희소 샘플링으로 생성.
  (1e12 셀을 직접 할당하지 않고, 해석적 traveling-wave를 샘플링)
- 산출물: results/visible_wave_summary.json,
  images/visible_wave_{633,532}_space.png / _time.png / _xt.png

## 재밍 떨림의 4.85 pm 회전 스케일(추가 분석)
- SOC 눈사태 로그에서 A_post를 이용해 ℓ_rot = 2πλ/A (λ=633nm)로 정의한 “회전 원호 길이”를 계산.
- 이벤트(avalanche index 18)에서 ℓ_rot ≈ 4.854 pm가 확인됨.
- 스크립트: code/jamming_rotation_485pm_study.py
- 결과: results/jamming_rotation_485pm_*.{csv,json}, 이미지: images/jamming_rot_*.png
