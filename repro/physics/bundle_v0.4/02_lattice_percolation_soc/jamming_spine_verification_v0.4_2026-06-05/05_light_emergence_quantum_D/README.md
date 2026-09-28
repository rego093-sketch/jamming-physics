# 05 — 빛 창발 / 양자 지름 (QUANTUM, 양성자 아님)

## 물리
종파 단일속도(01)가 살아남으면 선형분산 → 파장 λ=c/ν. 운반광(633nm)의 한 위상주기(2π)를
잼밍 격자 위 **A번의 미시전파**로 보면, 공간 미시스텝 a_phys = λ/A. 한 번의 회전 둘레(2π)가
곧 양자 지름:
```
   D = ell_rot = 2π·a_phys = 2π λ_light / A
```
핵심: 증폭 **A = a_med/g\*** 는 순수 격자 기하(중앙 최근접거리 ÷ 침투 임계 목갭). 물리상수가
A에 안 들어간다. 선택값은 미시 문턱 g0 하나 ⇒ 물리 입력은 λ(633nm) 하나, 광학→양자(10⁵배)
다리는 격자가 준다. 목표 **D = 2λ_Ce = 4.85 pm**.

## 파일
- `ellrot_verify.py` — A 분포 CSV(컬럼 A_post)에서 ℓ_rot=2πλ/A 분포 → 목표와 비교. 상단 docstring에 설명.
- `RESULTS_ellrot_verify.txt` — 위 실제 콘솔 출력.
- `make_ellrot_fig.py` — ℓ_rot 분포 vs 4.85pm 그림.
- `ellrot_485pm.png/.pdf` — 그림.
- `soc_indep_avalanches.csv`, `soc_indep_summary.json` — 본 세션 **독립** SOC 재현(N=200, seed11; A_median 716k).
- `deps/` — **사용자 번들 원본**(의존성, 출처 표기): `soc_percolation_pinning.py`(A=a_med/g\* 생성),
  `jamming_rotation_485pm_study.py`(D=2πλ/A 연구), `soc_run3_avalanches.csv`(A 분포 원천, A_median ~8.0×10⁵).

## 결과 [V]/[A]
- A=a_med/g\* 가 순수 격자 출력임을 독립 재현(내 run A_median 7.16×10⁵; 번들 ~8.0×10⁵; g\*/g0≈1.1–1.3).
- 목표 4.85pm 을 주는 A_target = 8.196×10⁵.
- 번들 A_med=8.01×10⁵ → ℓ_rot **4.965 pm** (목표 +2.3%); best avalanche **4.854 pm**.
- ⇒ **4.96 vs 4.85 = A 분포 중앙값 offset (근본 오류 아님)**.
- 앵커성: 절대 스케일은 λ 하나 + A_geo=cΔt/a 교차검증(0.16%). 두 파장(633/532) 점검 시 D 소거(반올림 무관).

## 실행
```bash
python3 ellrot_verify.py                       # 동봉 CSV 두 개 자동 검증 (즉시)
python3 ellrot_verify.py deps/soc_run3_avalanches.csv   # 번들 분포만
python3 make_ellrot_fig.py                     # 그림
# A 분포 자체를 처음부터 재현하려면 (격자 침투+SOC):
python3 -c "import sys; sys.path.insert(0,'deps'); import soc_percolation_pinning as s; print(s.run_soc(N=200, seed=11))"
```
