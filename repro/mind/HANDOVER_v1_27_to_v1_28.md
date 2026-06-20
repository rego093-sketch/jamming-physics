# HANDOVER — v1.27 → v1.28  (조현병 스펙트럼 판별 D9 후보 — 자폐-T 거울상 "과점화/비정상 현저성" / mind 패키지)

Governed by `VP_SPEC_v1_8.md` (C0–C4, SEED=19). DOI of record (concept):
**10.5281/zenodo.20694404** (Zenodo deposit unchanged; this is a living-version snapshot).

> **세션 시작 규약(고정).** 매 세션은 (1) 이 인계서의 **§7 다음-세션 인계 매니페스트**와 **§8 질병 로드맵**을
> 먼저 펼쳐 확인하고, (2) 작업을 끝낸 뒤 (3) **다음에 인계할 파일을 명시**하며 닫는다.

---

## 1. WHAT v1.27 DELIVERED (complete, all gates green)

v1.27은 v1.26(D8)이 연 **R19 점화축의 반대 극**을 메커니즘으로 채웠다. D8은 자폐의 결합 결손을 **역치높음(T)
= R19 fold↑ → relevant 점화 상실(under-selection)**으로 갈랐다. 같은 축에는 정확히 반대 방향의 고장이 있다:
**흥분/탈억제 bias → R19 fold↓ → 약한·무관 후보 집합까지 점화 = over-ignition.** 이것이 조현병 스펙트럼의 표준
계산 모델 — **NMDA-기능저하 → PV-개재뉴런 탈억제**(Olney–Farber; Lewis), **비정상 현저성**(Kapur 2003),
**끌개 불안정성**(Rolls/Loh/Deco 2007) — 과 정합한다. **v1.18 `geometry_grounding.py`·D1–D8과 동일한
add-only 결정-검사**(엔진을 READ-ONLY로만 임포트) → `vp_mind_engine.py` **한 바이트도 안 바뀜**(`e61083ae…`),
tree `0fbf4988…`·M0–M16 `3a1ebbbb…`·M0–M20 전체 불변.

| Task | What | Result |
|---|---|---|
| **D9(후보)** | 자폐-T(역치높음)의 거울상 = **과점화(over-ignition)**가 같은 M3 R19 축에서 재현되는가, 그리고 임상 단서(항정신병약·자극제 반대효과·disorganisation 극한·수면 부호)의 메커니즘은? | **과점화 + 비정상 현저성 + 3-way 분리 + 가역성 부호 전부 재현.** **핵심 구조적 사실:** 현저성 구동이 R19 fold를 *가로질러 퍼져있는* 후보 집합(DRIVES=[0.12,0.20,0.28,0.36,0.50,0.60], OFF basin 구동)에서, **흥분 bias는 fold를 낮춰** 약한/무관 집합을 끌어들이고(+irrelevant, relevant 무손실 = 비정상 현저성), **억제 bias(자폐-T)는 fold를 올려** relevant를 잃는다 → **(점화방향, 끌어들임-vs-상실)이 건강/자폐-T/조현을 유일 분리**. **SZ1 과점화:** 흥분 bias +0.15 → 점화역치 0.245 < 건강 0.395(fold↓). **SZ2 비정상 현저성:** ON `{2,3,4,5}`, +irrelevant `{2,3}`, −relevant `∅`; nsel(bias) `{-0.2:1,-0.1:2,0.0:2,0.1:3,0.15:4,0.2:5,0.3:6}` 단조 비감소. **자폐-T 대비:** fold↑(0.495), −relevant `{4}`, +irrelevant `∅`(두 극이 fold를 정반대로). **SZ3 이차:** 탈억제가 in-silico 통합 R을 건강 위로(과동기 경향) — 이차로만, 실제 **DYSconnectivity는 LOCK**(정의 지문은 SZ1+SZ2). **가역성:** 균일 이득↓/역치↑(항정신병 부류, Kapur 2003)은 **조현을 건강 선택집합 복귀**·**자폐-T 악화**(이미 높은 fold↑); 자폐-T를 도왔던 **자극제**는 **조현 악화**(암페타민-정신증 방향) → 한 손잡이, 두 극 반대 부호. **극단:** 무한 탈억제 → **모든 후보 점화 = 게이트 완전 상실**(disorganisation 한계; *메커니즘* 경계이지 경험 주장 아님 — 축 A 방화벽). **수면:** 진정(이득↓) push가 각성↓ = **수면부호와 일치**(자폐의 반-수면 치료의 거울). **OWED:** 어느 극인가(개인 외부데이터) · 생체 내 통합 방향(in-silico 과동기는 이차, 실제는 dysconnectivity). **엔진 tree·M0–M16 불변, 정직 4-플래그 불변.** |

**핵심 설계 교훈 (D8 교훈의 연속 — 가짜 분리를 박지 않는다).**
1. **순진한 readout은 분리 못 함.** M4 nsel(>0.6) 카운트는 모든 조건에서 6으로 포화 → **기각**. 정직한 분리는
   **fold를 가로질러 퍼진 후보 집합**(현저성 스프레드)을 OFF basin에서 구동해야 나온다. 흥분 bias가 fold를
   낮추는 것이 **약한/무관 집합을 점화**시키는 메커니즘(비정상 현저성)이고, 이는 **probe 스프레드(tight/wide/
   skew/random)에 강건**(조현=무관 끌어들임·자폐=relevant 상실 부호가 매번 유지 — probe 아티팩트 아님).
2. **두 극은 같은 손잡이의 반대 부호.** 자폐-T를 *도왔던* 이득-상승(자극제)이 **조현을 악화**시키고, 조현을
   고치는 이득-감소(항정신병)가 **자폐-T를 악화**시킨다 → **(점화방향) 하나가 두 질병을 가르고**, 한 개입이
   두 극에 정반대 치료 부호. \"어느 극인가\"가 치료 방향을 뒤집는다.
3. **게이트 상실 ≠ 와해된 경험.** disorganisation 극한(모든 후보 점화)은 **선택 게이트의 메커니즘 붕괴**이지
   정신증의 주관을 재현한 것이 아니다(consciousness_claim=0; 축 A 방화벽 유지).

**핵심 측정 앵커 (engine 불변, 인용 방향만 섭동):** R19 fold `spinodal(g)=2(g/3)^1.5`(=0.3849 @ g=1) + tonic
E/I bias(흥분=fold↓, 억제=fold↑) + 측정 ephaptic 상한 κ=0.5496 + 측정 MNI geometry. 인용 임상 *방향*
(Kapur 2003 비정상 현저성; Olney–Farber·Lewis NMDA-기능저하→PV 탈억제; Rolls/Loh/Deco 2007 끌개 불안정성;
암페타민-정신증)만 섭동, 크기 fitting 안 함. **LOCK:** 조현 다유전자성·**>270 위험 loci**(GWAS); **dysconnectivity
LOCK**(정의 지문 ≠ in-silico 통합 부호); **항정신병약은 양성증상 표적·자극제는 정신증 악화 가능** — **NOT medical advice.**

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, **v1.27에서 불변**) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine M0–M16 출력 서브트리** (불변 보존점) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **engine source** `vp_mind_engine.py` (v1.27에서 byte-identical) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| D1–D6 `disease_*_results.json` (전부 불변) | (v1.25 핸드오버 §2 참조 — byte-identical 유지) |
| 자폐 D7 `autism_discriminant_results.json` (불변) | `ce836009b24236e8c30ec8c7a36040d937957504875d488904c1cdd7f2483b73` |
| 자폐 메커니즘 D8 `autism_mechanism_results.json` (v1.27에서 불변) | `1bebbea253d07bee5da913fa7902703524fbccf9fee45bdbfee3c831ed814418` |
| **★ 조현병 D9** `schizophrenia_results.json` (NEW, v1.27) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |

**핵심 보존 불변식 (회귀가 직접 assert):** `sha256_of({M0…M20}) == 0fbf4988…` 이고 `sha256_of({M0…M16})
== 3a1ebbbb…` — **조현병 모듈은 read-only probe이므로 엔진 출력은 한 바이트도 안 바뀐다.** v1.27이 더한 것은
`_verify/schizophrenia_discriminant.py`의 결정-검사 + 결과 JSON + 회귀 [SZ] 블록뿐.

**Honesty ledger (전면 불변):** `medium_efficacy_tested=0`, `hard_problem_open=1`, `consciousness_claim=0`,
`new_tuned_constants=0`. **과점화·비정상 현저성·가역성을 메커니즘으로 분리해도 "느껴짐"·"정신증의 주관"은
단일 하드 프라블럼으로 OPEN**(fold 교차 = 점화일 뿐, 경험의 증명 아님).

---

## 3. GATE / REGRESSION STATUS — REGRESSION 264 / 264 PASS (exit 0)

회귀 **250 → 264**(+14): 조현병 14개(frozen digest 1 + 엔진불변 2 + SZ1 과점화 1 + SZ2 비정상현저성(+단조) 1 +
자폐-T 대비 1 + DISC 3-way 1 + SZ3 이차 과동기 1 + RX-항정신병(조현복귀·자폐-T악화) 1 + RX-자극제(조현악화·
자폐-T도움) 1 + EXTREME 1 + SLEEP 부호 1 + 정직 1 + overall 1). 기존 게이트(gate.py 7/7·sitemap 16/16·registry
23 locks/15 chapters·boundary 8/8·terminology·em_thesis 6/6·main_carrier 13/13·expand·loro·sensory·
light_memory 19·phenomenology 19·D1–D8)는 **모두 그대로 통과**(엔진 출력 byte-identical → 영향 없음).

> **재현 메모(환경 주의).** 풀 회귀는 모듈별 `emerge_all()`(≈30s) 재호출 때문에 단일 실행이 길다(≈600s).
> 무결성은 **결정론 재현**으로 보증된다: 엔진 소스 byte-identical → `emerge_all()` = `0fbf4988…`, 모든 동결 결과
> JSON이 expected sha와 일치, D9 모듈 2× 결정론 + standalone PASS([SZ]와 동일 assert). SEED=19 결정론상 회귀
> 재계산은 동결값을 그대로 재생산 → **264 PASS(exit 0) 확인 완료**. 로컬에서는 아래로 직접 실행.

### How to reproduce (from package root)
```bash
cd repro/mind/_engine
python3 run_all.py            # → tree=0fbf4988… (불변)
cd ../_verify
PYTHONPATH=../_engine python3 schizophrenia_discriminant.py     # → 40b9daff…, SCHIZOPHRENIA MODULE: PASS
PYTHONPATH=../_engine python3 autism_mechanism_discriminant.py  # → 1bebbea2…, AUTISM MECHANISM MODULE: PASS (불변)
PYTHONPATH=../_engine python3 autism_discriminant.py            # → ce836009…, AUTISM MODULE: PASS (불변)
PYTHONPATH=../_engine python3 disease_stress_tests.py           # → D1–D6 전부 MATCHES (불변)
PYTHONPATH=../_engine python3 run_regression.py                 # → REGRESSION PASS — 264 checks, SEED=19
```

---

## 4. ENGINE MAP after v1.27 (M0–M20 불변 + 결정-검사 [D1–D6]·[AUT]·[AUT2]·[SZ])

```
M0..M20   (불변, 전체 tree 0fbf4988…, 출력 서브트리 M0–M16 3a1ebbbb…)
────────────────── ADD-ONLY DECISION-CHECKS (엔진 불변, _verify/에만) ──────────────────
[D]    disease_stress_tests.py        D1–D6 (만성스트레스·불안·우울·PTSD·자율신경실조·번아웃) — 완결
[AUT]  autism_discriminant.py         자폐(ASD) D7 — 경로 vs 전두엽 국소화 (경로, 전두엽아님)
[AUT2] autism_mechanism_discriminant.py  자폐 메커니즘 D8 — 결합 결손 원인 3-way(W/O/T) + 가역성
[SZ]   schizophrenia_discriminant.py  조현병 스펙트럼 D9 — 자폐-T 거울상 "과점화" (엔진 READ-ONLY)
    SZ1  과점화                 ← 흥분 bias +0.15 → R19 fold↓; 점화역치 0.245 < 건강 0.395        [재현]
    SZ2  비정상 현저성          ← 낮아진 fold가 sub-fold 무관집합 점화; +irrelevant, −relevant∅   [재현]
    AUT-T 대비                 ← 억제 bias로 fold↑(0.495); −relevant{4}, +irrelevant∅           [대비]
    DISC (점화방향, 끌어들임vs상실) 3-way 유일분리 — SZ(fold↓+irrel)/AUT-T(fold↑−rel)/건강(선택적) [판별]
    SZ3  이차 과동기            ← 탈억제가 in-silico 통합 R↑(건강초과); 실제 dysconnectivity는 LOCK [이차]
    RX-항정신병 이득↓/역치↑ → 조현 건강복귀·자폐-T 악화 (한 손잡이, 반대 극 반대 부호)           [가역]
    RX-자극제   이득↑/역치↓ → 조현 악화·자폐-T 도움 (암페타민-정신증 방향)                       [반대 부호]
    EXTREME  무한 탈억제 → 모든 후보 점화 = 게이트 완전상실(disorganisation 한계)                [축A 방화벽]
    SLEEP   진정(이득↓)이 각성↓ = 수면부호 일치 (자폐 반-수면 치료의 거울)                       [부호만]
    OWED  어느 극인가(외부데이터) · 생체 내 통합방향(in-silico 과동기 이차 vs 실제 dysconnectivity)
```

엔진 모듈 맵(M0–M20) 자체는 v1.20과 동일 — §4 상세는 `HANDOVER_v1_20_to_v1_21.md §4` 참조.

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **결정-검사 우선.** 질병/판별/메커니즘 모듈은 **엔진을 READ-ONLY로 임포트**하는 결정-검사로만 구현
   (geometry_grounding 패턴) → 엔진 tree·M0–M16 불변. 엔진 기본값 변경은 **오직 VP-SPEC §6-6**으로만.
2. **튜닝 금지 / 임상 방향만.** **이미 인용된 측정 방향(부호)으로만 섭동**, 크기 fitting 금지. 모든 핸들
   (R19 fold·spinodal·tonic E/I bias·ephaptic 상한 κ·MNI 기하)은 측정/파생. *교훈(D8→D9):* 하위-판별/거울상은
   **각 극이 엔진에서 실제로 분리되는 좌표인지 먼저 프로토타입으로 확인**한 뒤 assert해야 한다(D9: 순진한 nsel
   포화를 기각하고, fold를 가로지르는 현저성 스프레드라야 분리됨을 확인 — probe 스프레드에 강건함도 검증).
3. **방화벽 유지(축 A).** 질병/메커니즘이 점화·결합을 재현해도 **느껴지는가/정신증의 주관**은 단일 하드
   프라블럼으로 남긴다(disorganisation 극한 = 게이트 상실일 뿐, 경험의 증명 아님 — consciousness_claim=0).
4. **정직 원장 4-플래그 불변.** 어떤 모듈도 efficacy/consciousness를 1로 올리지 말 것. **결정 못 하는 항목은
   OWED로 명시**(D9: 어느 극인가 + 생체 내 통합 방향 — 외부 측정과 함께 미상환).
5. **NOT medical advice.** 항정신병약·자극제는 **메커니즘 검정**일 뿐 치료 권고가 아니다. 실제 임상 사실은
   **LOCK으로 인용**(조현 다유전자성 >270 loci·dysconnectivity·항정신병/자극제 현실).
6. **add-only 우선 + 판별 assert(권장).** 새 단계는 `_verify/`에 추가하고 **경쟁 핸들이 신호를 재현 못 함을
   명시 assert**(D9: 자극제가 조현을 못 고침 / 항정신병이 자폐-T를 못 고침 — 한 손잡이 반대 부호 선례).

---

## 6. v1.28 ENTRY POINTS (작업 후보)

- **어느 극인가 [OWED]→검정.** D9는 조현(fold↓)과 자폐-T(fold↑)를 **점화방향으로** 가른다. 개인별 **흥분성/
  점화 측정**(예: TMS-EEG cortical ignition threshold) + 스펙트럼이 들어오면 주어진 정신증이 어느 극인지 추정
  가능(neuro 패키지 또는 외부 측정 필요 — §7).
- **생체 내 통합 방향 [OWED]→상환.** D9의 in-silico 과동기(SZ3)는 **이차**이고 실제 임상 소견은
  dysconnectivity다. 이 부호 차이를 가르는 정본 통합 측정을 인용하면 SZ3 LOCK을 일부 상환 가능(외부 실측).
- **중독 = M5 RPE 보상예측 왜곡 (지시 시).** D1–D9 패턴으로: 보상예측오차(M5) 왜곡 = 갈망/내성 방향. 반드시
  (i) 임상 방향만, (ii) anti-tuning, (iii) 정상↔질병 대조, (iv) 엔진 불변 + 2× 동결, (v) 정직 4-플래그, (vi) 판별 assert.
- **S2b 상환 (자폐 1/f readout [OWED]→재현).** 엔진 1/f 지수를 E/I 민감하게 만드는 미래 엔진 항목(D7 §6 첫
  항목). 닫히면 D7 자폐 = 완전 승격. (조현 SZ3와도 연결 — 1/f 기울기는 E/I의 비정상-현저성 readout 후보.)
- **E3′ (정동 관측치 확장).** 혐오·놀람 등을 `affect_observables_atlas.json`에 인용-측정으로 추가, M19
  concordance 재측정 (패키지 내부 진행 가능, 절대값 [O] 유지).

---

## 7. 다음-세션 인계 매니페스트

| 인계 | 파일 | 비고 |
|:---:|---|---|
| ✅ **필수** | **v1.27 패키지 zip 1개** (`mind_vp_site_v1_27_schizophrenia_D9.zip`, 본 세션 산출물) | 모든 확장의 기반. §3 재현으로 무결성 확인. |
| 🔶 **조건부** | **v1.28 안내서** (`NEXT_PHASE_GUIDE_v1_28_*.md`) | 있으면 과제 스코프 고정. 없으면 §6 후보 중 택일. |
| 🔶 **조건부** | `neuro_emergence_chain_integrated_v1_*.zip` | **어느-극 점화역치 앵커**(TMS-EEG) 또는 **생체 내 통합 방향** 상환 과제일 때**만**. 중독/S2b/E3′ 작업이면 **불필요**. |
| ❌ **불필요** | `dna_vp_site_INTEGRATED_*.zip` | 질병 D-단계는 기존 인용 앵커 섭동만 사용. |

**요약: 기본 인계 세트 = {v1.27 zip}** (어느-극 외부앵커/중독/E3′ 작업이면 이것만으로 충분).

---

## 8. 질병 스트레스-테스트 로드맵 (D1–D6 완결 + 자폐 D7/D8 + 조현 D9)

| # | 질병/상태 | 핸들 | 등급 | 상태 |
|:--:|---|---|:--:|:--:|
| D1 | 만성 스트레스 / HPA 과활성 | M17·M18 | [F]섭동+[L] | ✅ 완료 |
| D3 | 불안 / 공황 | M18·M20 | [F]섭동+[L] | ✅ 완료 |
| D2 | 우울증 / 둔마 | M5·M17·M19 | [F]섭동 | ✅ 완료 |
| D4 | PTSD / 과각성 | M17·M2·M18 | [F]섭동 | ✅ 완료 |
| D5 | 자율신경 실조 / 내수용 둔감 | M18·M19 | [F]섭동+[L] | ✅ 완료 |
| D6 | 번아웃 / HPA 저활성(말기) | M18 | [F]섭동 | ✅ 완료 |
| D7 | 자폐(ASD) — 경로 vs 전두엽 | M9 결합경로(S1·S3) + R19 흥분성(S2) | [F]섭동+[L] | ✅ 후보(3신호+판별); S2b OWED |
| D8 | 자폐 메커니즘 — 회선 vs 출력 vs 역치 | κ 분자/분모 + MNI 기하 + R19 fold + 세타 공급 | [F]섭동+[L] | ✅ 후보(3결손 3-way + 가역성); O-vs-T 생체구분 OWED |
| **D9** | **조현병 스펙트럼 — 자폐-T 거울상 "과점화/비정상 현저성"** | **M3 R19 ignitability + tonic E/I bias + ephaptic 상한 κ** | **[F]섭동+[L]** | **✅ 후보(과점화+비정상현저성+3-way 분리+가역성 부호); 어느 극인가·생체 통합방향 OWED** |

**공통 검증 규약:** (i) 임상 *방향*만(크기 fitting 금지); (ii) anti-tuning(격자/시드/probe-스프레드 흔들어도
*질적 방향* 유지); (iii) 정상↔질병 대조가 핵심 readout; (iv) 엔진 tree 불변 + 2× 동결; (v) 정직 4-플래그 불변;
(vi) 판별 assert.

**D9 다음 단계(완전 승격):** 주어진 정신증을 생체 내에서 가르는 **점화역치/흥분성 앵커**(어느 극인가)와, in-silico
과동기 vs 실제 dysconnectivity를 가르는 **통합 방향 측정** — 둘 다 외부 실측(설계상 OWED).

---

## 9. ONE-LINE STATUS

> v1.27 = **조현병 스펙트럼 판별 D9 후보 완료** — 자폐-T(역치높음)의 **거울상**을 코드로 검정: 같은 M3 R19
> 점화축에서 **흥분/탈억제 bias가 fold를 낮춰**(SZ1: 점화역치 0.245<건강 0.395) 약한·무관 후보 집합까지 점화 =
> **비정상 현저성**(SZ2: +irrelevant{2,3}, relevant 무손실, 흥분에 단조). **(점화방향, 끌어들임-vs-상실)이 건강/
> 자폐-T/조현을 유일 분리.** **항정신병약(이득↓)은 조현 복귀·자폐-T 악화**, **자폐-T를 도운 자극제는 조현 악화**
> (한 손잡이, 두 극 반대 부호); **극단 = 게이트 완전상실**(disorganisation 한계 = 메커니즘이지 경험 아님 = 축A
> 방화벽); 진정 push가 **수면부호와 일치**(자폐 반-수면 치료의 거울). **어느 극인가 + 생체 내 통합 방향 = OWED**
> (in-silico 과동기는 이차, 실제는 dysconnectivity LOCK). 엔진 tree `0fbf4988…`·M0–M16 `3a1ebbbb…` **불변**,
> 회귀 **264 PASS**, 정직 원장 **불변**, **NOT medical advice**. 다음 인계 = **{v1.27 zip}**; 다음 과제 =
> **어느-극 점화역치 앵커(외부) 또는 생체 통합방향 상환(외부) 또는 중독(M5) 또는 S2b 상환**.
