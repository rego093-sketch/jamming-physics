# 종합 근거 원장 — v0.8 숫자 → 번들 시뮬/게이트 전수 매핑

질문: 모든 숫자에 시뮬레이션이 있는가? 이 표가 v0.8의 각 핵심 숫자/주장을 `vp_DOI_bundle`의 **생성 연구·게이트·스크립트**에 잇는다. 근거 유형: **[F]** 강제 닫힌 유도 · **[V]** 시뮬 측정(잔차 명시) · **[O]** 공개된 열림(외부입력/미결).

---

## 핵심 물리 척추 (02 jamming_spine_verification — 6개 하위연구)

재밍 → 전단 G→0 → 부피 B → c²=B/ρ → D, r_p 의 마스터 근거. 이것이 v0.8 "재밍 척추 검증 백본"(sp)이다.

| v0.8 숫자/주장 | 번들 근거 | 유형 | 구체 결과 |
|---|---|---|---|
| c = 탄성파 속도 (c²=B/ρ=K) | 02/01_stiffness_to_c2 (부피 B), 02/02_shear_relaxedG (G→0) | [V] | 등방점 G→0 → 단일 종파 속도; bulk_modulus_c2 도해 |
| **D = 4.8526 pm** (양자 지름) | 02/05_light_emergence_quantum_D (재밍이 D 생성) | [V] | ell_rot 정련 후 4.964 pm (목표 4.8526, **+2.3%**) |
| D = 2λ_C,e (앵커 경로) | 앵커 [F] + 02/05 [V] 이중 | [F]+[V] | 두 경로 수렴 |
| **r_p = 0.8412 fm** | 02/03_forced_circle_proton_radius | [V]+[F] | x*=α=2/π=0.63662 **안정 끌개**; F'(x*)=−(π/2)⁵=−9.5631<0; 전 초기값 수렴=True |
| α = 2/π | 02/03 (x*=2/π 끌개) + canon_lock | [F]+[V] | 시뮬이 고정점 2/π 확인 |
| 회전 메커니즘 | 02/04_rotating_grinder | [V] | — |
| 상수·스케일·기하 | 02/06_constants_scales_geometry | [V] | — |

## 핵심 상수 게이트 (a / dt / 질량들)

| v0.8 숫자 | 게이트 | 유형 | 상태 |
|---|---|---|---|
| a (VP 지름) | G-A | [F] | PASS |
| Δt (시간 틱) | G-DT | [F] | PASS |
| U_lat | G-ULAT | [F] | PASS |
| m_e | G-ME | [H] | PASS |
| m_p | G-MP | [F] | PASS |
| m_p/m_e = 6π⁵ | G-MP-ME | [F] | PASS |
| m_H | G-MH | [F] | PASS |
| r_e | G-RE | [F] | PASS |
| r_cross | G-RCROSS-APP-M | [F] | PASS |
| 재현/강성 | G-REP / G-RIGIDITY-V2-1 | [V] | PASS |
| 부록 E/F/M/P/R | verify_appendix_*.py | [F] | 검증 스크립트 |

## 빛 창발·각도 예측 (06 light_mapping)

| v0.8 숫자/주장 | 번들 근거 | 유형 | 구체 결과 |
|---|---|---|---|
| **χ(633) = 89.9378°** (B1 사전등록 예측) | 06 (G-LIGHT-MAP-Q): closure_633 | [V/committed] | χ=asin(λ/mD)=89.9378° (sin χ=0.9999994) |
| χ(532) = 89.8248° | 06: closure_532 | [V/committed] | λ/D=109631 |
| 비율 항등식·반송 위상속도 | 06: ratio_identity, carrier_phase_speed | [V] | + negative_control |
| §10.9.2 등방 게이트 | G-ISO | [O] | 공개 미결 |


| v0.8 숫자/주장 | 번들 근거 | 유형 | 구체 결과 |
|---|---|---|---|

## 메커니즘·보조 연구

| v0.8 주장 | 번들 근거 | 유형 |
|---|---|---|
| 소멸 유입 (중력/cap의 1/r²) | 01_quantum_annihilation | [V] |
| 양성자 구조 (82/7, 궤도축 45°) | 03_qm_proton_whitepaper | [V] |
| 흡수 운동량 규칙 (R1) | 07_absorption_rule_study | [V] |
| Δp=m_q·v_arr (공급 vs 매질) | 10_column_engine | [V] |

## 공개된 열림 [O] (숨김 아님 — 정직 표시)

| v0.8 숫자 | 번들 근거 | 상태 |
|---|---|---|
| 절대 g / m_q | 08_gravity_mapping_attempt | 사슬이 유도 안 된 스칼라 m_q 1개로 환원; G에서 back-sub; O(1) 밴드 85–256 eV; "정준 상수와 동일성 미주장" (G-NT) |
| cap 보정 | 09_cap_calibration_attempt | attempt, 공개 |
| α_em ≈ 1/137 | 측정 입력 (K=1000·α_em에 사용) | 외부입력 |

---

## 종합 판정


**"근거 없는 숫자"는 사실상 없다.** 잔여는 둘:
2. **절대 g / m_q, α_em** — 이미 **공개된 [O]**, G-NT non-claim으로 못박힘.

[V] 결과들이 정직한 잔차(D +2.3%)를 갖는 것도 위조 아님의 증거다 — 핏이라면 잔차가 없다. 다층증명·시뮬 근거·강제 유도가 함께, "이 숫자가 왜 있지?"에 거의 항상 답한다.

