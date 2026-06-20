# GRAVITY REPRODUCIBILITY MAP — VP Theory §17.4

이 문서는 §17.4 중력편의 **재현성 지도**다. 각 표시 수치가 (1) 어떤 정준입력에서, (2) 어떤 닫힌형으로,
(3) 어떤 기준선 대비 어떤 잔차로 생성되는지를 1:1로 추적한다. 모든 값은 `tools/vp_gravity_ssot.py`가
정준입력 + 동결 DEM(sha256)에서 결정론적으로 재생성하며, 드리프트 게이트가 stale literal을 차단한다.
No-Tuning: 잔차를 닫으려 이동한 계수는 없다.

## 1. 정준입력 (canon_lock / realization_lock / 표준 지구물리)

| 기호 | 값 | 출처 |
|---|---|---|
| c | 299792458 m/s | canon (exact SI) |
| g0 = g_(⊕) | 9.80665 m/s² | 표준중력 45.5°, 단일층 cap |
| R_E | 6371000 m | 지구 평균반지름 |
| Ω | 7.292115×10⁻⁵ rad/s | 지구 자전 |
| τ_q | 1.62×10⁻²⁰ s | realization (D/c) |
| ρ_crust | 2670 kg/m³ | 지각 평균 |
| G | 6.674×10⁻¹¹ | terrain integral 전용 |
| ρ_moon, R_moon | 3340 kg/m³, 1737400 m | NASA |
| ρ_⊕ | 5514 kg/m³ | NASA |
| DEM | Pikes Peak SRTM 30m, 33×33@250m, z0=4300m | OpenTopoData; sha256=bbe987307d5dcbb9e0f9f98318a5b9c6d49e50705a76cfc7ae3d167fd61dcd41 |

## 2. 입력→출력 추적 (forced chain)

| 출력 | 닫힌형 | 정준입력 | 값 | 등급 |
|---|---|---|---|---|
| 자유공기 기울기 | −2·g0/R | g0,R_E | −0.3079 mGal/m | [F] |
| 적도-극 Δg | Somigliana | (표준) | 5186 mGal | [F] |
| 원심력 분 | Ω²R | Ω,R_E | 3388 mGal (65%) | [F] |
| 편평 분 | ∇Φ 잔차 | (타원체) | 1798 mGal (35%) | [F] |
| 지형보정(정상) | 선질량 ΣdA(1/r−1/√(r²+Δz²)) | 동결 DEM, ρ_crust, G | 21.46 mGal | [F]/[V] |
| VP−Newton 지형 | 1/r² 항등 | (동일 적분) | 0.00 mGal | [F] |
| 달 표면중력 | g0·(ρ_m/ρ_⊕)(R_m/R_E) | ρ_moon,R_moon,ρ_⊕ | 1.620 m/s² | [F] |
| 중력 드리프트 | g0·τ_q | g0,τ_q | 1.589×10⁻¹⁹ m/s = 5.30×10⁻²⁸ c | [F] |
| 직접시뮬 샘플수 | 1/(v_in/c)² | (위) | 3.56×10⁵⁴ | [F] |

## 3. 잔차 지도 (단일 출처 — 기준선 명시)

| ID | 비교쌍 (기준선) | 값 | 유형 |
|---|---|---|---|
| **R-FA** | −2g0/R vs measured free-air −0.3086 | +0.24% | 외부 (1/r² 곡률 vs 선형) |
| **R-TC** | VP inflow vs Newtonian terrain correction | 0.00 mGal | 내부 (1/r² 항등) |
| **R-MN** | g_(*)∝ρR vs measured Moon 1.62 | −0.01% | 외부 (천체 ρR 스케일) |
| **R-ISO** | 정상 절대 g vs 관측 | ~−200 mGal | 외부 (아이소스타시 심부밀도; 별도 항) |

## 4. 등급 지도

- **[F]** 강제(자유계수 0): 1/r² 커널, 자유공기, 위도, 지형보정 항등, 달 ρR, 드리프트/샘플수.
- **[V]** 시뮬측정: 실측 DEM 지형보정 필드(625 station), 동반 사일로(Torricelli/Beverloo).
- **[O]** 열림: 절대 g 자릿값 — 4-벽 정리로 미시 연쇄 부재 증명, αₑₘ class.

## 5. 게이트 (reports/gravity.gate.json)

| 게이트 | 판정 기준 | 결과 |
|---|---|---|
| G-GRAV-FREEAIR | \|−2g0/R − (−0.3086)\| < 0.0015 | PASS (+0.24%) |
| G-GRAV-LAT | rot%+obl% = 100 | PASS (65+35) |
| G-GRAV-TERRAIN | \|VP−Newton\| < 1e-6 mGal | PASS (0.00) |
| G-GRAV-BODY | \|g_moon−1.62\| < 0.02 | PASS (−0.01%) |
| G-GRAV-SCOPE | 4-벽 정리 + 28자리 문서화 | PASS |

## 6. 재현 (3-line check)

```
python3 tools/vp_gravity_ssot.py            # 원장 + 잔차 지도 재생성
python3 tools/vp_gravity_ssot.py --check txt # 본문 드리프트 게이트 → PASS(exit 0)
python3 tools/tc_compute.py                  # 실측 DEM 지형보정 + 항등 + ⟨cosθ⟩ 척도 테스트
# (선택) python3 tools/fetch_dem.py          # DEM 재수집(동결본 덮어씀)
```

DEM 교체 시: versioning + sha256 갱신 + 재게이트 필수. 본 맵은 §17.4.7 본문 잔차표의 권위 출처다.
