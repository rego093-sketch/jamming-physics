# ATL 재현 번들 (Atlantic Expansion — 물리 코어 prototype)

이 번들은 TGU-ATL-A 백서 업그레이드의 **물리 브릿지 prototype 코드 + 결과 + 그림** 을
하나로 모은 것입니다. 목표: **모든 수치 주장이 재실행으로 검수 가능**.

작성일 2026-06-05 · 작성자 지원: Claude · 언어: 한국어/영어 혼용
참조 계획서: `ATL_upgrade_plan.md` (Part A0 가 이 번들의 결과를 인용)

---

## 구조
```
atl_bundle/
  validate_all.py        # 단일 검증 runner: 모든 claim -> PASS/STOP
  LEDGER.md              # claim -> script -> result -> 기대값/공차 매핑
  SHA256SUMS.txt         # 모든 파일 체크섬 (무결성)
  README.md              # 이 파일
  engine/                # 물리 prototype 스크립트 (numpy/scipy, 결정론적, seed 고정)
    vp_jamming_friction.py      # [1차] 마찰=잼밍 언잼밍-액체화 (고온E->액체화)
    tp_dilatancy_prototype.py   # [확증] 열가압 + 팽창 R_md 경쟁
    feasibility_map.py          # 결합 Λ 타당성 -> viable 깊이 (계산이 범위 결정)
    jamming_microderive.py      # [세부규칙] 1차원리 잼밍: phi_jam, z_iso, 스케일
    jamming_shear_modulus.py    # [세부규칙] Hessian G_relaxed->0 = 마찰붕괴 규칙
    p8_magnetic_test.py         # [C-3] 자기줄무늬 H0(GPTS2020) vs H2(공명) — 최대 외부반증
    c3b_braking_and_stripe_logic.py  # [C-3b] 줄무늬 축퇴 논리 + 감속/브레이크 모델
    c5_velocity_history.py      # [C-5] 자기장=상대시간; 절대척도는 물리(수천 년 허용)+재잼밍 브레이크
    jamming_bistability.py      # [쌍안정] 액체화는 느릴 수 없다 → stick-slip; "느린 정상확장"=시간평균
    c2_trigger.py               # [C-2 게이트] 안티포드 트리거 ΔR vs Ω-NoGo(<50km)
    c4_scalability.py           # [C-4/P7 마스터게이트] 스케일 외삽 (물질=PASS / 시스템Λ=HOLD)
    c16_energy_ledger.py        # [C-16] 통합 에너지원장: work-in/heat/disposal, 이류 sink = 반증가능 P4
    omega_nogo_check.py         # [Ω-NoGo] constraints.yml 전 6항목 점검
    p1_plate_boundaries.py      # [P1] 대서양 경계 성격(섭입 vs 수동); R_sub UNLOCK
    p9_orogeny_deborah.py       # [P9] 오로지니 레짐(Deborah); UHP viscous → HOLD(정직)
    c7_scaling_field_test.py    # [P7 현장] 홍해/Afar/Baikal 대조: 깊이=열적 → 마스터 HOLD 유지
  results/               # 저장된 수치 결과 (*.npz)
  figures/               # 그림 (*.png)
```

## 실행
```bash
# 전체 검증 (빠른 모듈 즉석 재실행 + 잼밍 결과 감사)
python validate_all.py            # -> 30/30 PASS 기대

# 개별 재생성 (느린 잼밍 모듈 포함)
python engine/vp_jamming_friction.py      # ~수초
python engine/tp_dilatancy_prototype.py   # ~1-2분 (regime sweep)
python engine/feasibility_map.py          # ~수초
python engine/jamming_microderive.py      # ~1-3분 (패킹 최소화 sweep)
python engine/jamming_shear_modulus.py    # ~2-4분 (Hessian, 12 seeds)
```

## 핵심 결과 (요약 — 상세는 LEDGER.md)
1. **마찰 해법 (1차, 사용자 명제 "고온에너지→액체화"):** 마찰열이 전단대를 등정압
   한계 $z\to z_{iso}=2d$ 로 밀어 **액체화(unjamming)** → $\mu_{eff}=2.2\times10^{-3}$
   (Ω-NoGo 통과), $\Delta T=25$K(무융). 용융전용 대조는 1462K(융). 에너지는 접촉결합
   파괴(이벤트 잠열)로 소모 → 용융 전에 마찰 붕괴.
2. **세부규칙 1차원리 유도:** $\phi_{jam}\approx0.84$, $z_{iso}=2d$(2D 4 / 3D 6),
   $(z-z_{iso})\propto(\phi-\phi_{jam})^{1/2}$, $p\propto(\phi-\phi_{jam})$,
   그리고 **$G_{relaxed}\propto(z-z_{iso})\to0$ (벌크 $G_{Born}$ 유한)** = 마찰붕괴 규칙
   $\sigma_y\to0$. (스파인 S2.4 를 독립 재현.)
3. **확증:** 열가압(Rice 2006) 경로도 비배수에서 82% 약화·무융 → 같은 결론 독립 재현.
4. **타당성(계산이 범위 결정):** 마찰을 액체화로 고정하면 $\Lambda\propto d^2$ →
   임계깊이 ~12 km. 위 경계는 취성-연성 전이 → **viable 창 ~12–26 km, 차가운
   craton 선호, 따뜻한 젊은 지각에선 닫힘** (지리적 검증 예측).
5. **C-3 자기줄무늬(최대 외부반증):** 실제 GPTS2020 역전 barcode 는 강한 **비주기**
   (CV(durations)=0.86, 스펙트럼 집중도 0.15, coherence 0.04) → **H2(공명 동결) FAIL**;
   단, **줄무늬는 균일 시간압축에 축퇴**(C-3b: 두 모델 위치차 $10^{-14}$ km) → 빠름의 하중반증은
   줄무늬 기하가 아니라 *절대연대*. ⟹ 등속-빠름·감속-표준시계만 배제; "급한 초기+감속" 생존.
6. **C-5 시간척도 (백서 틀 = 수천 년):** 자기장은 *상대* 시간만 기록(C-3b 축퇴) → 절대 시간척도는
   줄무늬가 아닌 *물리* 가 정함. 수천 년 개방은 액체화 상태에서 **~3–32 Pa의 미미한 구동력**이면
   충분(물리적 허용). 브레이크 = **mm 전단대 재잼밍 τ=h²/κ≈9초**(빠름→짧은 사건; 이전의 50 Myr
   리소스피어 냉각은 *틀린 층*). 한계: 수천 년 *절대* 주장은 방사성·천문 절대연대와 충돌 →
   **연대 firewall**(별도 논증); 단 줄무늬는 반증 못 하고 물리는 허용함.
7. **잼밍 쌍안정 (느린 액체화는 불가능):** 액체화 유지엔 전단열>냉각이 필요 →
   $V_{crit}=\sqrt{8k\,\Delta T_{unjam}/\eta}\approx$ **mm/s–m/s** (cm/yr보다 ~$10^8$배 빠름).
   정상 전단응력이 액체화 천이에서 **속도-약화(465배 강하) → 불안정 → stick-slip**.
   3000 km 개방의 *누적* 미끄러짐은 **~69일**뿐; 외형상 cm/yr "정상 확장"은 드문 고속 슬립의
   **시간평균 인공물**. ⟹ 운동 양식은 *막힘-급동*(잼밍 예측)이지 *느린 정상*이 아니다.

## 등급 (토대 문서 규약)
- 측정/유도된 규칙(잼밍 sim): **[DERIVE]**
- 대륙 규모로의 외삽: **[GATE]** (마스터 GATE — 무차원수 보존 필요, 미검증)
- 확립물리(O'Hern–Silbert–Liu–Nagel, Wyart; Rice 2006)는 *차용이 아니라 외부 확증*.

## 한계 (정직)
- 잼밍 sim 은 계산속도를 위해 **2D**(z_iso=4). 스파인은 3D(z_iso=6); 2D는 규칙
  *형태* 를 검증, 3D 값은 스파인이 확립.
- $G_{relaxed}$ 는 N=144·12 seeds 평균; 중간 구간 잔여 노이즈 있음(유한크기). 추세
  ($\propto\Delta z\to0$)와 $G_{Born}$ 유한은 견고.
- 모든 대륙 규모 수치는 [GATE]: 소규모(mm·m·초)에서 검증된 물리의 외삽.
