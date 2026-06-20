# IRREPRODUCIBILITY_LEDGER — VP Chemistry & Electromagnetism

VP-SPEC v1.7 헌법 C3 산출물. 백서 전체의 `[O]` 등급 항목을 한 곳에 집계한다 —
각 항목의 **위치 · 종류(open/refuted) · 재현 불가(또는 미유도)의 구체적 사유 · 재현/마감 경로**.

- Paper: VP Chemistry & Electromagnetism: Derived from a Single Anchor on the Jamming-Lattice Substrate
- code: `chm` · DOI(개념): 10.5281/zenodo.20680540 · ORCID: 0009-0002-7535-8245
- 정본: `docs/chemistry/` HTML (헌법 C2). 본 원장의 모든 사유는 정본 본문과 교차 확인된다.

## `[O]` 등급의 두 종류 (이 백서의 용법)

이 백서에서 `[O]` = **open / refuted**. C3 사유 명시 의무는 두 경우 모두에 적용된다.

1. **Open (미유도, 장애물 명시).** 기하(VP geometry)만으로는 절대 크기를 고정할 수 없고,
   닫으려면 외부 물리(스크리닝·비조화·밴드효과·게이지 구조 등)가 필요한 항목. 사유 = 그 장애물.
2. **Refuted (반증, 사유 명시).** 제안된 기구가 직접 검증으로 틀렸음이 드러난 항목. 사유 = 왜 틀렸는가.
   이 백서의 refuted 항목은 **반증 자체가 결정론 모듈로 재현**된다(2× sha256) — 즉 "재현 불가"가 아니라
   "재현된 반증"이다. 재현 모듈을 함께 표기한다.

물리 백서(자매 권)의 대표 계산-게이트 `[O]`(절대 중력 g·미세구조상수 αₑₘ)는 그 권의 원장에 집계된다.
본 원장은 chemistry 권에 한정한다.

---

## 집계표 (전 `[O]` 항목)

| # | 위치 | 항목 | 종류 | 사유 / 장애물 | 재현·마감 경로 |
|---|------|------|------|----------------|----------------|
| 1 | §1 EM.9/12 (01-electromagnetism) | 완전 벡터 **E/B** 컬 구조(Faraday ∇×E, Ampère–Maxwell ∇×B; 자기장 절대 크기) | open | 스칼라/세로(종) AQD 처리는 독립 가로(횡)-벡터(자기/복사) 섹터를 공급하지 못한다. EM 장의 **주요 미해결 구조 항목**. 세로(쿨롱/E) 섹터·동역학·인과는 EM.12에서 닫힘. | 미유도(새 물리 필요). physics §14.0.6 참조 |
| 2 | §1 EM.10 (01-electromagnetism) | γγ 생성 동역학 (γγ→e⁺e⁻) | open | 광자 충돌로부터 전하가 생성되는 과정을 **격자 동역학 수준**에서 기술하는 경로가 아직 없다. | 미유도 |
| 3 | §2 CH.2–3 (02-chemistry-single-anchor) | 절대 다전자 이온화에너지(IE)·전자친화도 | open | 전자 스크리닝(Clementi–Raimondi). Slater 규칙은 경향만 줌(주족 평균 ~22% 오차, EA 부호 8/18만 정답). 노블가스 닫힘·주기 길이는 [F]로 정확. | calibration 입력으로 보강(`vp_dblock_chemistry.py`) |
| 4 | §2 CH.4 (02-chemistry-single-anchor) | 고립쌍 결합각 압축의 **정밀 크기** (CH₄→NH₃→H₂O) | open | 방향(109.5°→107°→104.5°)은 [F?]로 맞으나, 정확한 크기는 기하만으로 고정 불가. | 미유도(방향만 강제) |
| 5 | §2 CH.5 / 부록 (02-chemistry-single-anchor) | 절대 결합 해리 에너지 | open | per-bond 비조화(Morse β=a·rₑ; 고립쌍·극성)가 필요. 직접 검정에서 β가 결합차수와 무상관(r=+0.18) → √2 기하만으로 마감 불가. | `vp_bond_energy.py`(반증된 √2-단독 가설 포함) |
| 6 | §2 CH.5 / §4 CC.3 | 다중밴드 정밀 색(d⁹ Cu²⁺, d⁸ Ni²⁺) | open | 단일-Δ 점모형으로는 부족(넓은 다중밴드 흡수가 적색까지 꼬리). 분광화학 계열은 [CAL]. | 미유도(단일-Δ 한계) |
| 7 | §2 CH.9 (02-chemistry-single-anchor) | 절대 활성화에너지 Eₐ·터널링 | open | 전이상태 구조가 필요(기하 너머). 충돌속도·Eyring 보편인자는 [F]. | 미유도 |
| 8 | §2 CH.11 (02-chemistry-single-anchor) | 절대 pKₐ 예측 | open | 용매화(solvation) 필요. 개별 pKₐ는 [CAL], Henderson–Hasselbalch 형태는 [F]. | calibration 입력 |
| 9 | §3 CM.9 (03-conduction-copper-magnetism-iron) | 비정수 편력(itinerant) 자기 모멘트(Fe 2.22, Co 1.72, Ni 0.62 μ_B) | open | 편력/밴드 효과. 국소 Hund 계산은 정수 경향만 줌. 정렬-회전이라는 자성의 **원리**는 [F]. | 미유도(밴드 효과) |
| 10 | §6 CA.2 (06-applications) | 암모니아 절대 속도·촉진제(K₂O/Al₂O₃)·표면 미시반응 | open | d-밴드 에너지 서술자 너머의 표면 미시반응이 필요. apex 위치(Fe/Ru)는 잡힘. | 미유도 |
| 11 | §6 CA.3 (06-applications) | OER 스케일링 한계 돌파 | open | 단일자리 촉매에서 물분해는 영구적으로 비쌈 — 깨려면 스케일링 관계 파괴(이작용성/3D 자리)가 필요. | 미유도(설계 규칙으로 명시) |
| 12 | §6 CA.4 (06-applications) | 자기-진폭 담수화 소자 | **refuted** | 채널 가로 자기에너지 ~10⁻² k_BT. 장은 휘저을(MHD) 수 있어도 진폭으로 담수화 불가. 검증된 대안(역삼투 등)으로 대체. | `vp_desalination.py` (반증 재현) |
| 13 | §6 CA.5/CA.7 (06-applications) | 절대 전류밀도·완전 미시반응 | open | 보정 서술자 너머. ΔE_CO·ε_d·평형전위·스케일링 오프셋은 [CAL]. | 미유도 |
| 14 | §7 CA.9a (07-low-grade-waste-heat-electricity) | 정적 자석이 구리 전도전자를 한 방향 전류로 정렬 | **refuted** | Lorentz 힘 F=qv×B ⊥ v → 일을 하지 않음. Boris 적분에서 사이클로트론 표류 ⟨v⟩≈0·운동에너지 불변. 전류는 E-장이 구동(구리는 3d¹⁰ 비자성·Seebeck 1.8 µV/K 무시가능). | `vp_magnet_lorentz.py` sha256 7c8246ab (반증 재현, 2× 동일) |
| 15 | §7 CA.9b (07-low-grade-waste-heat-electricity) | 히트펌프로 폐열을 승온 후 엔진 발전 | **refuted** | 히트펌프와 엔진은 역과정(COP·η_Carnot=1). 연결 시 최선의 경우 엑서지(40°C 기준 4.8%)만 회수, 실물 부품으로는 순 −65%. | `vp_heatpump_exergy.py` sha256 64e26ee6 (반증 재현, 2× 동일) |
| 16 | §7 CA.9c (07-low-grade-waste-heat-electricity) | 검은 구리가 모은 열로 전기를 "생성" | **refuted** | 검은 구리는 흡수체(α≈0.96, 광학)이지 변환기가 아님 — 열전·광전·엔진 기구 없음, Seebeck 무시가능, 1085°C에서 융해라 고온 방출체도 불가. | `vp_blackcu_absorber_not_generator.py` sha256 0067cbe1 (반증 재현, 2× 동일) |

부록(`ax-o-open-items-register-...`)은 §1의 EM `[O]` 항목(#1 완전 벡터 섹터, #2 γγ 생성)과 §2·§3의 open 항목을
백서 내부 등록표로 재집계하며, 본 원장과 일치한다. §1에는 `[H]`(전역 U(1) Goldstone 장거리 EM)와
`[CAL]`(αₑₘ≈1/137: 형태는 유도, 크기는 측정 입력) 항목도 있으나 이들은 `[O]`가 아니므로 본 C3 원장의 집계
대상이 아니다(부록 등급표에 사유와 함께 보존).

---

## C3 적합성 요약

- 정본 본문의 모든 `[O]` 항목(위 16건)은 재현 불가(또는 미유도)의 **구체적 사유를 본문에 명시**한다 → 사유 없는 `[O]` 0건.
- **refuted 4건**(#12, #14, #15, #16)은 반증 자체가 결정론 모듈로 재현된다(2× sha256 동일) — 재현된 반증.
- **open 12건**은 닫으려면 외부 물리(스크리닝·비조화·밴드·게이지·용매화·미시반응)가 필요하다는 장애물이 명시되어 있다.
- 본 원장은 정본 HTML 과 교차 확인되며, 항목·사유·위치가 본문과 1:1 대응한다.
