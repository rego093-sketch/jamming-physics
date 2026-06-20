# CHANGELOG — v0.10.0 (time-gravity lane)

승인 근거: 사용자 승인 세션 + VP_SPEC §1 "approved session". 모든 변경은 결정론적이며 재현 가능.
이전: v0.9.3 (gravity lane). 본 릴리스: **featured 재편 + 시간 섹터 신설 + 정직-부정 기록** → minor bump.

---

## 1. 신설 — §18 「Time and Gravity (one mechanism, two faces)」 (featured)

`txt/18-time-and-gravity.txt` (eq phy-18-000 … phy-18-014, 15개). 구조: 시간과 중력을 **따로 떼되 연결**.

- 시간 트랙 §18.1–18.4: 시계(참조) → 운동 시간지연 + **정확√** → 정확√의 위치 → 시간 게이트
- 중력 트랙 §18.5–18.8: 중력=유입(§17.4 승격) → **river 단일화(연결점)** → 두 속도 → 중력 게이트 + 정직-부정
- 연결 §18.9–18.10: 단일 원리 dτ/dt=√(1−v_loc²/c²) + 우주론 후크 + 등급/scope

## 2. 등급 상승 (No-Tuning; 계수 이동 0)

- **정확√(운동 시간지연)**: [O] 전부 미유도 → **[F] 값 강제** (유한-c 닫힘 + 전자율 등방성; Michelson-for-winding,
  κ=√(1−v²/c²) 유일 — §18.2). 전-벡터 동역학 실현만 [O] 잔류(=§14.0.6).
- **중력 시간지연**: 선도 1+φ_N/c² → **river 정확형 √(1−2GM/rc²)** (G-RIVER, 항등 — §18.6).
- 미해결 차원 축소: 둘 → 하나(정확√ 동역학 하나; 닫히면 운동·중력 동시 전차수 정확).

## 3. 정직-부정 기록 (G-CAP-DEPART)

- **중력 섹터는 접근 가능한 모든 깨끗한 채널에서 GR과 축퇴** — cap(g_restore)은 접촉 수직력만; 적색편이·궤도·
  빛휨·중력파는 비캡 geom 채널 = 정확 Schwarzschild. 중성자별(PSR J0740, 유입속도 0.69c)·링다운(|εΩ|<0.05)에서
  VP=GR 자동 정합(z_VP−z_GR=0 검산). sonic 유동화=지평선; 조기 항복은 배제; 생존창 α≳0.82는 한계-등방
  jamming과 긴장. → 변별 예측 없음(§18.8).
- **scope 진술**(W.0 + §18.10): 검증 무게는 중력이 아니라 우주편(a₀=cH₀/2π, γ선 분산)에 있다. 두 볼륨 동일 결론.

## 4. 중력 승격 (정의 위치 이동, 내용 불변)

- §17.4(유입·cap·terrain·four-wall)을 §18로 승격. **§17.4 본문·수식(phy-17-0xx)·수치 전부 verbatim 보존**
  (검증: 스텁 외 diff 0; eq 수 88=88 동일). §17.4 헤더 아래 PROMOTION NOTE 1블록만 추가.

## 5. 우주론 인계 + 후크

- §18.9에 **처리율-시계 후크**: 시계율=굴절률=같은 신호속도 √(K/ρ_eff) → ρ_eff의 우주적 진화가 둘을 같은
  인자로 변화 → (1+z)=n(t_obs)/n(t_em). 우주편 Ch 7의 (1+z) 근거화 진입점.
- I-TIME-3(우주론 1+z) → 우주편 Ch 7 인계. κ_opt=H₀/c [INPUT]; E-COSMO(§17.2/§17.5) 레지스트리 유지.

## 6. 상호참조

- §14.0.6 상태문에 1줄: "exact v/c scaling"의 *값*은 §18.2에서 강제([F]); 전-벡터 동역학만 잔류. ↔ §18.3 양방향.

## 7. 모듈·게이트·원장 (결정론, 표준라이브러리, 2×sha256 동일, 자체검증)

- `tools/`: vp_timegravity_ssot.py, vp_inflow_competition.py, vp_exact_sqrt.py, vp_cap_depart.py
- 게이트: I-TIME-1/2·G-RIVER·G-EXACT-SQRT·G-INFLOW-COMP(PASS-A/SAT/ASTRO) = PASS; G-CAP-DEPART = 축퇴(판정);
  I-TIME-3 = 우주편 인계.
- `reports/`: time_gravity.gate.json + TIME_GRAVITY/INFLOW_COMPETITION/EXACT_SQRT/CAP_DEPART _LEDGER.csv
- open-items: §14.0.6 full-vector dynamics · 절대 g 크기(m_q, four-wall) · η_rotor→1

## 8. manifest

- `manifest/physics.csv`: §18 행 추가(featured, words 2206, eq 15).
- `manifest/physics.eq_list.tsv`: phy-18-000 … phy-18-014 (15행, base64 TeX) 추가.

## 9. 재현 (5줄)

```
cd tools
python3 vp_exact_sqrt.py            # G-EXACT-SQRT (κ=√(1−v²/c²) 유일)
python3 vp_timegravity_ssot.py      # G-RIVER, I-TIME-1/2, 드리프트
python3 vp_inflow_competition.py    # PASS-A, SAT, ASTRO
python3 vp_cap_depart.py            # G-CAP-DEPART (정직-부정)
python3 vp_timegravity_ssot.py --check ../txt/18-time-and-gravity.txt ../txt/w0-result-scorecard-one-page-summary.txt
```

## 10. docs/ 재생성 안내 (중요)

`docs/` 의 렌더된 HTML은 빌드 파이프라인 산출물이다(원본 docs/도 split.py/render_eq.js/build_hub.py로 생성).
본 통합은 **정본인 txt/ + manifest/ 를 갱신**했으므로, 사이트 HTML은 동일 파이프라인으로 재생성해야 §18이
렌더된다. SSOT(txt/manifest)는 완비; docs/ 재빌드만 남음(변환기 측 작업).
