# MISSION — 트랜스진단 결함-축 아틀라스 (Transdiagnostic Fault-Axis Atlas)

**패키지:** `mind` (Felt Cognition) · DOI `10.5281/zenodo.20694404` · VP-SPEC v1.8 (C0–C4)
**거버닝 로드맵:** `RESEARCH_ROADMAP_post_autism_adhd.md` (패키지에 동봉)
**상태:** v1.51 기준 — T1a(조현병)·T2a(뇌전증)·E0(가소성 층)·T1b(우울/TRD)·E2(상태-스위칭 층)·T2b(양극성)·T3a(중독)·T3b(알츠하이머)·T3c(OCD)·E0-SYNTH(삼부작 종합 §42)·E1(공간-국소화/장-성형 층 §43)·**E1-FOC(첫 영역-특이 응용: 초점 뇌전증 억류 vs 이차 전신화 §44)** 출판 완료, **다음 진입점: 추가 E1 영역-특이 응용(병변 장·off-target 신경조절) 또는 E1×E0 결합 또는 로드맵 잔여(`HANDOVER_v1_51_to_v1_52.md` §5)**

---

## 1. 사명 재정의

Part I(§01–§17)은 창발된 대뇌 위에서 **느낌-인지(felt cognition)** 의 기능 모델을 세웠다. Part II는
같은 대뇌를 **특정한, 명명된 방식으로 고장 내어** 읽는다. v1.32까지 Part II는 자폐를 세 축(T/O/W)으로
분해하고 ADHD를 분리했다. v1.33부터 Part II의 사명을 다음으로 **재정의**한다:

> **정신·신경 질환을 증상 체크리스트가 아니라 공유 메커니즘(T/O/W 축 + 동기화/시간 축)으로 재절단하는
> 트랜스진단 결함-축 아틀라스.**

세 가지 산출물:
1. **층화(stratification)** — 한 진단명 안의 이질성을 어느 축이 고장났는지로 가른다.
2. **개입-축 정합(intervention-axis matching)** — 어떤 연산자(gain·threshold·wiring)가 어떤 축에
   도달하는지 부호-수준으로 예측한다.
3. **메커니즘적 배제(mechanistic ruling-out)** — 어떤 축에도 도달하지 못하는 개입을 in-silico null로
   폐기한다(예: §24의 "더 많은 D2 차단 → 음성/인지" 폐기).

## 2. 규율 (비협상)

물리-유도 · 유전자-접지 · LOCK→Derive→Gate · no-tuning · **SEED=19** · 2×sha256 · **READ-ONLY 엔진** ·
사전등록 부호-전용 예측 · 정직한 등급 · **efficacy=0** · **NOT medical advice** · **Axis-A 방화벽**
(게이트/동기화 손실 ≠ 주관적 경험; `consciousness_claim=0`) · **hard-problem OPEN**.

엔진(`_engine/vp_mind_engine.py`)은 바이트 불변(`e61083ae…`), emergence tree 불변(`0fbf4988…`).
신규 작업은 `_verify/`에 add-only. 새 측정 0 · 새 튜닝 0.

## 3. 공유 축 (아틀라스의 척추)

| 축 | 엔진 핸들 | 정의 |
|---|---|---|
| **T** (threshold) | R19 점화 fold = `spinodal(g)=2(g/3)^1.5=0.3849` | 점화 임계; bias가 fold를 올림/내림 |
| **O** (output/gain) | 노드별 구동 배수 (κ) | 구동 세기; 결핍 시 R 저하·PAC 저하 |
| **W** (wiring) | long-range edge 감쇠 (LAM) | 라우팅 기하; locality 불균형, 스칼라 gain에 불변 |
| **SYNC** (동기화) | 전역 Kuramoto R (측정 ephaptic kernel) | 위상 정렬; over-sync 천장 = θ-cap이 아래 머물 한계 |
| **시간** (state-switch) | **§28 E2 (구현)** | attractor 간 전이(히스테리시스·fold latency=critical slowing); 발작 onset/기분 에피소드 동역학 |

**한 동기화 축 위의 정렬(§25 EP4):**
`autism-T (저점화, R 0.379) < health (선택적, 0.390) < schizophrenia (이상, 0.401) < epilepsy (전점화, 0.422)`

## 4. 로드맵 목표 → 챕터 매핑 (상태)

| 목표 | 조건 | 챕터 | 상태 | 비고 |
|---|---|---|---|---|
| (기반) | 자폐 T/O/W | §18–19 | ✅ DONE (v1.32) | 세 축 분해, 화학 도달 한계 |
| (기반) | θ-cap | §20–21 | ✅ DONE (v1.32) | wiring 축 외부 페이스메이커, 실현가능성 [O] |
| (기반) | ADHD 분리 | §22 | ✅ DONE (v1.32) | gain/arousal 축, wiring 온전 |
| (기반) | 가상 임상 | §23 | ✅ DONE (v1.32) | 집단 그림, dose-cap 잔여 발견 |
| **T1a** | **조현병** | **§24** | **✅ DONE (v1.33)** | 과점화 거울 극; 증상-도메인 axis 지도 |
| **T2a** | **뇌전증** | **§25** | **✅ DONE (v1.33)** | 과동기화 극; 발작 = 게이트 붕괴 |
| **E0** | **가소성 층** | **§26** | **✅ DONE (v1.34)** | 위상-상관 Hebb; 공고화·spaced>massed·가역→만성 스위치; η=0 M9 bit-identical; `PlasticConnectome` 재사용 |
| **T1b** | **우울/TRD** | **§27** | **✅ DONE (v1.35)** | 저-협응 작동점의 만성화; HPA 핸들; 지연발현=공고화 타임스케일; TRD=흔적 깊이; `PlasticConnectome` 재사용 |
| **E2** | **상태-스위칭 층** | **§28** | **✅ DONE (v1.36)** | R19 셀을 시간에 걸쳐 읽음; 히스테리시스·fold latency 발산(§25 발작 시간경과 청산)·장벽=스위칭 임계; const-drive가 엔진 settle bit-identical; `BistableSwitch` 재사용 |
| **T2b** | **양극성** | **§29** | **✅ DONE (v1.36)** | 한 valence 축의 두 극(조증>health>울증); 삽화=bistable 전이; kindling=E0 흔적 축적; 안정제=장벽 올리기; `BistableSwitch`+`PlasticConnectome` import |
| **T3a** | **중독** | **§36/§37** | **✅ DONE (v1.43/v1.44)** | SG 통합-민감화-게인 = E0 GAIN; B-i 문턱-레버(도달불가 명명)+B-ii E0 동역학(직접 모델) 합류 CLOSED; `PlasticConnectome` 재사용 |
| **T3b** | **알츠하이머** | **§38/§39** | **✅ DONE (v1.45/v1.46)** | PROG 신경퇴행-진행 = E0 DECAY(중독 GAIN의 구조적 역); B-i+B-ii 합류 CLOSED; `PlasticConnectome` 재사용 |
| **T3c** | **강박(OCD)** | **§40/§41** | **✅ DONE (v1.47/v1.48)** | 병적 안정화 = E0 STABILISATION(제3 양태·GAIN과 family 공유·자기-지속 읽기로 구별); B-i+B-ii 합류 CLOSED; `PlasticConnectome` 재사용 |
| **E0-SYNTH** | **E0 삼부작 종합** | **§42** | **✅ DONE (v1.49)** | 메타-종합(새 측정 0): GAIN/DECAY/STABILISATION을 단일 E0 층의 세 읽기로 인증(T1–T5); 소스 3 SHA 비트-단위 재검증 후 읽기; 아크 완결 |
| **E1** | **공간-국소화 / 장-성형 층** | **§43** | **✅ DONE (v1.50)** | 스칼라 Kglob→노드별 벡터 Kvec(공간 프로파일)·노드별 국소-결맞음 장 READ-ONLY; 장 고정 구조(국소+정규화 정확)·이질 도달+구동-안정 소뇌 허브·자기-국소/중계 분류 구동-불변({hippocampus,midbrain} 고정)·**보편 focal>diffuse 법칙 부재**(영역-특이 요구); 균일 구동 M9 bit-identical; `SpatialField` 재사용(공간 형제) |
| **E1-FOC** | **초점 뇌전증: 억류 vs 이차 전신화 (E1 첫 응용)** | **§44** | **✅ DONE (v1.51)** | E1 공간 층의 첫 영역-특이 응용 = §25 과동기화 뇌전증의 공간적 정련; `SpatialField` import(재유도 아님)로 각 영역을 focal 발진 초점 구동 → 억류(국소 잔류)/방송(이차 전신화) 분할 **구동-불변**(방송 집합 {hippocampus,midbrain} 고정)·방송=off-target 우세(이차 전신화의 구조)·**off-target 확산 ≠ 전역 과동기화**(소뇌가 최대 전역 reach인데 억류성, 두 방송 초점이 R 반대 방향 = 두 분리축, 정직한 무-튜닝)·방송=소수 중계-허브 클래스(억류가 기본값); 영-발진 구동 M9 bit-identical; [L] 방향 임상 대응(내측측두엽=이차-전신화 전형, 환자-예측 아님) |
| T3b | 알츠하이머 | — | ⏳ Tier-3 | |
| T3c | OCD | — | ⏳ Tier-3 | |

**정직한 제외(범위 외):** 내용/서사 지배 조건 — 공포증, 인격/해리 장애, 신체상 축. 이들은 T/O/W
동역학이 아니라 내용에 의해 지배되며, 현 프레임워크의 메커니즘 핸들로는 닿지 않는다.

## 5. 재현

```
cd repro/mind/_verify && python3 run_all_atlas.py     # 아틀라스 게이트 (T1a, T2a, E0, T1b, E2, T2b) — 7/7
cd repro/mind/_verify && python3 run_all_d9.py         # 자폐 코호트 (v1.32)
cd repro/mind/_verify && python3 run_all_vc.py         # θ-cap virtual clinical (v1.32)
python3 tools/gate.py                                  # 전체 사이트 게이트 (118/118)
python3 tools/mind_registry.py                         # 레지스터 검증 (36 locks / 25 chapters)
```

동결 해시: 엔진 file `e61083ae…` · tree `0fbf4988…` · `schizophrenia_results.json` `40b9daff…` ·
`schizophrenia_symptom_domains_results.json` `0499f74f…` · `epilepsy_oversync_results.json` `d363f0a5…`.

## 6. 한 줄 요약

> 자폐에서 보정한 T/O/W 점화 축과 동기화 축은 **자폐만의 것이 아니다.** 조현병은 그 축의 반대 극이고,
> 뇌전증은 그 축의 천장이다. 같은 엔진, 같은 축, 다른 작동점 — efficacy=0, not medical advice.
