# VP 잼밍 척추 — 재현성 패키지 (2026-06-05)

이 패키지는 VP(Volume Particle) 잼밍-기질 이론의 핵심 줄기를 뒷받침하는 **모든 실행
코드와 결과**(시뮬·그림·CSV/NPZ·분석 스크립트)를 모듈별로 정리하고, 내부에 설명을 단
것이다. 작업 언어 한국어. 모든 수치는 본 세션에서 실제로 돌려 얻었다.

> **등급 표기**: [F] 닫힌 형태 증명/측정 · [V] 시뮬레이션 검증 · [D] 정의(MAP-1)에 의존 · [A] 단일 앵커(절대 스케일).
> **정직성 원칙**: 역학은 증명/검증됐고, 수치 사다리(3π⁴/6π⁵/6π⁶)는 정의 한 점([MAP-1])에 의존한다. "증명 완료"로 과장하지 않는다.

---

## 0. 한 줄 줄기 (the spine)

```
무한강성·완전충전 입자
  → 회전(온도)↑ → 자기조직화 한계잼밍  z = 2d = 6          [02, 05]
  → 한계 ⇒ 전단 G→0,  부피 B 유한                          [01, 02]   [V]
  → 단일 생존 종파속도  c² = B/ρ = K                        [01]       [V]
  → 선형분산 ⇒ 파장 λ=c/ν ; 양자지름 D = 2πλ/A = 4.85 pm    [05]       [V/A]
  → (회전이) 강성껍질 반경 못박음  r_p = (2/π)λ_Cp = 0.84 fm [03, 04]   [V/F]
  ───────────────────────────────────────────────────────────────
  두 크기:  양성자 r_p = 0.84 fm   |   양자 D = 4.85 pm  (= 6π⁶·r_p)
```

## 1. 양성자 ≠ 양자 (절대 혼동 금지)
| | 양성자 PROTON | 양자 QUANTUM |
|---|---|---|
| 크기 | 반경 **0.84 fm** (10⁻¹⁵ m) | 지름 **4.85 pm** (10⁻¹² m) |
| 출처 | 강성껍질 균형 r⁻⁵/r⁻⁴ → x*=2/π ; 그라인더 82-cell(z=6) | **파장식** D=2πλ/A (= 2λ_Ce) |
| 모듈 | **03**(반경 끌개), **04**(그라인더) | **05**(빛 창발) |
| 관계 | — | **D = 6π⁶·r_p = π·(m_p/m_e)·r_p ≈ 5768 r_p** |

두 객체는 6π⁶배(~5768) 떨어진 **다른 스케일**이다. (이전에 "같은 원"이라 혼동했던 것을 바로잡음.)

---

## 2. 모듈 지도

| 모듈 | 무엇을 보이나 | 핵심 결과 | 등급 |
|---|---|---|---|
| **01_stiffness_to_c2** | 부피탄성률 B 직접계산 → 단일속도 | z=6 에서 B 유한(0.76–0.95), G→0; c²/a²=0.107(N-무관) | [V] |
| **02_shear_relaxedG** | 전단 G→0 (§5 미해결문제 해결) | G_relaxed→0 @ z≈5.9–5.95; ω*∝Δz(R²=0.997); η→∞; AQS; σ_y→0 | [V] |
| **03_forced_circle_proton_radius** | 강제된 양성자 반경 | 유일 안정 끌개 x*=2/π=0.6366, F'(x*)=−9.56; 전역 수렴 → r_p=0.8412 fm | [F]/[V] |
| **04_rotating_grinder** | 회전이 코어·길이를 만듦 | 정상 ~82-cell 코어(z=6=2d); R_rms ∝ 1/Ω (회전이 크기 결정) | [V] |
| **05_light_emergence_quantum_D** | 양자 지름 = 파장식 | D=2πλ/A; A=a_med/g\* 순수 격자; ℓ_rot 중앙값 4.96pm, best 4.854pm | [V]/[A] |
| **06_constants_scales_geometry** | 상수·스케일·기하 (순수 수학) | 2/π, δ=1/π², 2π=α/δ [F]; 3π⁴→6π⁵→6π⁶=π·m_p/m_e [D]; 코어 81=3⁴ | [F]/[D] |

각 모듈 폴더의 `README.md` 에 물리·파일·실행법·결과가 자세히 있다.

---

## 3. 빠른 실행 (단일 CPU, 수 분 내)

```bash
# 순수 수학 검증 (즉시, 시뮬 아님)
cd 06_constants_scales_geometry && python3 verify_constants_and_scales.py

# 강제 양성자 반경 끌개 (즉시) + 그림
cd 03_forced_circle_proton_radius && python3 forced_circle_attractor.py

# 양자 지름 ell_rot=2πλ/A 데이터 검증 (즉시)
cd 05_light_emergence_quantum_D && python3 ellrot_verify.py

# 부피/전단 탄성률 생산런 (수 분; 결과는 results_bulk/ 에 이미 동봉)
cd 01_stiffness_to_c2 && python3 bulk_run.py 256 0 4

# 회전 그라인더 (~23s) + Ω 스윕
cd 04_rotating_grinder && python3 vp_grinder_3d.py && python3 grind_sweep.py
```
각 모듈의 `RESULTS_*.txt`(있는 경우)는 위 분석 스크립트의 실제 콘솔 출력이다.

---

## 4. 핵심 숫자 (본 세션 실측)
- 단일속도: **c²/a²|_{z=6}=0.107** (N=256:0.108, N=512:0.107) = affine z/2d²(=0.167)의 0.65배.
- B_relaxed@z=6 = 0.76(N256)/0.95(N512) 유한; G_relaxed@z=6 = 0.009/−0.0005 →0; Born=FD 4.7e-7.
- 강제 반경: x*=2/π=0.6366, F'(x*)=−9.56(<0), 전역 끌개 → r_p=(2/π)·1.32141fm = **0.8412 fm** (CODATA 0.8414, −0.02%).
- 그라인더: N 3000→301, 코어 ~79–81≈82(=#{r²≤6}=81+1), z_core≈8.9; R_rms 3.48→2.98 (Ω 0.04→0.24).
- 빛 창발: A_target(정확4.85)=8.196×10⁵; bundle A_med=8.01×10⁵→ℓ_rot 4.965pm(+2.3%); best 4.854pm.
- 상수: 2/π=0.63662, 1/π=0.31831, δ=1/π²=0.10132, 2π=α/δ=6.28319; 3π⁴=292.227; 6π⁵=1836.118(CODATA 1836.153, **−18.8 ppm**); 6π⁶=5768.34=π·(m_p/m_e).

---

## 5. 정직한 상태 (요약)
- **증명·검증된 역학**: 무한강성→c²(단일속도), 전단 연화, 강제 반경(전역 끌개), 회전이 크기 창발, 파장 λ=c/ν, A=격자 출력.
- **정의에 기댐 [D]**: 3π⁴·6π⁵·6π⁶ 은 전부 `[MAP-1]`("섹터간 위상 lock 1개 = π²") 한 점에 의존(α·δ와 동일 지위). 6π⁶은 독립 상수가 아니라 질량비 6π⁵의 변장.
- **단일 앵커 [A]**: 절대 pm 스케일은 λ(633nm) 하나 + A_geo=cΔt/a 교차검증(0.16%).
- **열린 3고리**: (1) 회전→정확히 z=2d, (2) [MAP-1] 기하 유도, (3) Δt 독립성. 이 셋을 닫으면 척추 완결·수비학 혐의 소멸.

---

## 6. 폴더 구조
```
VP_jamming_reproducibility_2026-06-05/
├─ README.md                        (이 파일)
├─ MANIFEST.txt                     (전체 파일 목록 + 한 줄 설명)
├─ 01_stiffness_to_c2/              bulk.py, relaxed_shear.py, bulk_run.py, fig_bulk.py, results_bulk/, 그림
├─ 02_shear_relaxedG/               relaxed_shear.py, le_shear.py, aqs.py + 러너/그림/FINDINGS + results/(spectra 35, aqs 8 npz)
├─ 03_forced_circle_proton_radius/  forced_circle_attractor.py(+RESULTS), 그림
├─ 04_rotating_grinder/             vp_grinder_3d.py, grind_sweep.py, fig_rot.py, 그림
├─ 05_light_emergence_quantum_D/    ellrot_verify.py(+RESULTS), make_ellrot_fig.py, soc_indep_*, 그림, deps/(번들 원천)
├─ 06_constants_scales_geometry/    verify_constants_and_scales.py(+RESULTS)
└─ docs/                            VP_jamming_spine_DRAFT.md, VP_theory_chain..., HANDOVER...
```

## 7. 의존성·출처
- `05_.../deps/` 의 `soc_percolation_pinning.py`, `jamming_rotation_485pm_study.py`, `soc_run3_avalanches.csv` 는
  **사용자의 AQD 번들(v0.3.0) 원본 코드/데이터**다(A 분포 재현용 의존성으로 동봉). 그 외 모든 파일은 본 세션에서 생성.
- `01`·`02` 의 `relaxed_shear.py` 는 공유 인프라(패킹/Hessian/backbone/relaxed G·B). `bulk.py` 가 이를 import.
- 환경: numpy 2.4.4(`np.trapezoid`, `np.linalg.eigvalsh`), scipy 1.17.1, 단일 CPU. matplotlib 그림 라벨은 영문(한글 폰트 부재).
- `docs/VP_theory_chain_stiffness_to_D.md` 는 초기 사슬 문서로 일부 "양성자=양자" 표현 오류가 있다(척추 초안 §1이 정본). `VP_inevitability_chain.md` 는 미완 초안이라 미포함.
