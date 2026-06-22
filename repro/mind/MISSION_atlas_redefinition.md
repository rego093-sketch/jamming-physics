# MISSION — 트랜스진단 결함-축 아틀라스 (Transdiagnostic Fault-Axis Atlas)

**패키지:** `mind` (Felt Cognition) · DOI `10.5281/zenodo.20694404` · VP-SPEC v1.8 (C0–C4)
**거버닝 로드맵:** `RESEARCH_ROADMAP_post_autism_adhd.md` (패키지에 동봉)
**상태:** v1.57 기준 — T1a(조현병)·T2a(뇌전증)·E0(가소성 층)·T1b(우울/TRD)·E2(상태-스위칭 층)·T2b(양극성)·T3a(중독)·T3b(알츠하이머)·T3c(OCD)·E0-SYNTH(삼부작 종합 §42)·E1(공간-국소화/장-성형 층 §43)·E1-FOC(첫 영역-특이 응용: 초점 뇌전증 억류 vs 이차 전신화 §44)·E1-LES(둘째 영역-특이 응용: 뇌졸중/병변 장 국소 결손 vs 원격 디아스키시스 §45)·E1-NMOD(셋째·마지막 영역-특이 응용: 표적 신경조절 깨끗 전달 vs off-target 누출 §46 — E1 응용 삼부작 CLOSED)·**E1×E0(아틀라스 최초의 교차축 결합: 공간-가소성 각인 국소 전달 vs 중계 공고화 §47 — §43 공간 층[어디]을 §26 가소성 층[지속]에 혼인, 깨끗한 전달 ≠ 깨끗한 각인·중계 각인이 기본값[결합이 §46 깨끗-기본값을 뒤집음])**·**E1×E2(둘째 교차축 결합: 공간 스위치 레버리지 = 어느 초점 구동이 집합 상태를 가장 쉽게 뒤집는가 §48 — §43 공간 층[어디]을 §28 상태-전환 층[쌍안정 뒤집기]에 혼인, §29 양극성 에피소드의 공간 형제[§29는 언제·§48은 어디], flip 역치 순위 = 방송-레버리지 순위·장벽-불변·고정 비전환 소수 {thalamus,olfactory_bulb}, 스위치성이 §46 순간-발자국 축 AND §43 도달 축 둘 다와 디커플링 = 보편 reach→switchability 법칙 부재[reach 허브 cerebellum이 스위치 최난 10/12])**·**E0×E2(셋째 교차축 결합: kindling = 반복 상태-flip이 더 쉬워지는가 §49 — §26 가소성 층[진화하는 connectome]을 §28 상태-전환 층[쌍안정 flip]에 혼인, §29 양극성 에피소드가 [O]로 남긴 trace→threshold 링크를 닫음; 반복 flip이 trace ‖dW‖를 strictly-mono 심화하고 flip 역치 p*=spinodal(g)/L을 un-kindled fold 아래로 내림[kindling, 0.3849→0.3783]·장벽-불변·hysteresis 루프 좁아짐+latency 짧아짐·kindling은 공고화적 not 퇴행적[진짜 새 결합 결과+정직한 음성: '침식' 가설 거부, R 상승 0.3896→0.3964·연결체가 앵커 이상으로 끝남 = easier-flip과 침식 디커플링]·trace가 kindling 변수)**·**CROSS-SYNTH(교차축 결합 메타-종합 캡스톤: 세 결합·세 디커플링·하나의 규율 §50 — 세 교차축 결합[E1×E0 §47·E1×E2 §48·E0×E2 §49]을 단일 family로 인증; 세 층 E0/E1/E2의 세 쌍별 edge를 모두 실현[각 층 정확히 두 결합·degree 2·완전한 삼각형, 프로그램적 검증]·셋이 공통적으로 단일-축 결과를 디커플링/거부하고 정직히 보고[깨끗한 전달≠각인·스위치성⊥발자국·도달·easier-flip⊥침식]; 소스 3 SHA 비트-단위 재검증 후 읽기·엔진 READ-ONLY byte-unchanged·새 측정/기계/튜닝 상수 0·§42 E0-triad 종합이 한 층의 세 읽기를 닫은 것과 평행하게 세 층의 세 결합을 닫음 = **교차축 결합 아크 완결**)** 출판 완료, **다음 진입점: 교차축 결합 추가 응용(억제성-구동 E1×E2 변주·다중-노드 동시 구동·공간-국소화된 kindling[E1×E0×E2 삼중 결합 — 도달성 선판단 필수]), 또는 로드맵 잔여(`HANDOVER_v1_57_to_v1_58.md` §5)**

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
| **E1-LES** | **뇌졸중/병변 장: 국소 결손 vs 원격 디아스키시스 (E1 둘째 응용)** | **§45** | **✅ DONE (v1.52)** | E1 공간 층의 둘째 영역-특이 응용 = §44 초점-뇌전증의 **파괴-병변 쌍대**; `SpatialField` import(재유도 아님)로 각 영역을 **SILENCING** 바이어스 b<0(노드 **침묵 not 삭제** — 동결 W0 보존)로 병변화 → 국소-결손/원격-디아스키시스(von Monakow) 분할 **구동-불변**(디아스키시스 집합 {hippocampus,midbrain} 고정 = E1.3 중계 집합; sub-floor −0.3서 thalamus 진입, 정직히 제외)·원격 디아스키시스=off-target 우세(midbrain ≈3.0×·hippocampus ≈1.2×·국소 cerebellum ≈0.06×)·**전역 교란 ≠ 원격 디아스키시스**(최대 전역 교란자는 **국소-결손성 소뇌** = 병변이 최대 국소이면서 전역 교란 극대화; **§44와 정직한 대비** — reach 허브가 **구동-불변 아님**[소뇌→midbrain @−0.9], 두 분리축)·디아스키시스=소수 중계-허브 클래스(국소 결손이 기본값); 영-병변 구동 M9 bit-identical; [L] 방향 임상 대응(교차 소뇌 디아스키시스·von Monakow, 환자-예측 아님) |
| **E1-NMOD** | **표적 신경조절: 깨끗한 전달 vs off-target 누출 (E1 셋째·마지막 응용 — 삼부작 CLOSED)** | **§46** | **✅ DONE (v1.53)** | E1 공간 층의 셋째·마지막 영역-특이 응용 = §44 초점-뇌전증의 **치료적 재독(therapeutic re-reading)**; `SpatialField` import(재유도 아님)로 각 영역에 §44와 **동일한 흥분성** 바이어스 b>0(자극 전극 DBS/TMS/tDCS로 재프레이밍)를 겨눠 → 깨끗-전달(self-localising)/off-target-누출(relay) 분할 **구동-불변**(누출 집합 {hippocampus,midbrain} 고정 = E1.3 중계 집합; **sub-floor caveat 없음** — 가장 약한 0.3 포함 안정, §45와 정직한 대비)·off-target 누출=off-target 우세(hippocampus ≈4.2×·midbrain ≈1.6×·깨끗 cerebellum ≈0.04×)·**깨끗한 전달 ≠ 전역 약함**(최대 전역-도달 타깃은 **깨끗-전달성 소뇌** = 가장 깨끗한 타깃이 가장 강함, '초점=약함' 반박; reach 허브 **구동-불변**[§44 상속, §45와 대비]; 두 누출 타깃이 R **반대 방향**[hippo 내림/midbrain 올림] = 누출은 제어 가능 점-대-점 중계 아님, 두 분리축)·누출=소수 중계-허브 클래스(깨끗 전달이 기본값); **공간 수치는 §44 자신의 것**(같은 흥분 구동, 평이하게 명시 — 새것은 치료적 재독·N3 디커플링); 영-자극 구동 M9 bit-identical; [L] 방향 임상 대응(DBS/TMS/tDCS off-target 효과, 환자-예측 아님) |
| **E1×E0** | **공간-가소성 각인: 국소 전달 vs 중계 공고화 (아틀라스 최초의 교차축 결합)** | **§47** | **✅ DONE (v1.54)** | 아틀라스 **최초의 교차축 결합** = §43 공간 층(어디 WHERE, 순간 발자국)을 §26 가소성 층(지속 LASTING, 시간 흔적)에 **혼인**; 두 층 **모두 import**(재유도 아님), 유일한 새 객체는 둘을 잇는 결합 적분기 `_integrate_coupled`(노드별 공간 구동을 **진화하는** connectome 위에서 스텝·쌍별 위상-일치 누적 → 지속 흔적 ΔW). 강도 b0∈{0.3,0.5,0.7,0.9} **그리고** 율 η∈{0.03,0.05,0.08} **이중 스윕** 생존: 국소-각인/중계-각인 분할 **구동-불변**(국소 집합 {brainstem,cerebellum,pallidum,striatum} 고정 = 엄격한 소수 넷)·중계 각인=off-target 우세 흔적(neocortex ≈6.3×·forebrain_gaba_in ≈5.7×·국소 brainstem ≈0.63×)·**깨끗한 전달 ≠ 깨끗한 각인**(흔적-중계 집합[8]이 §46 장-중계 집합 {hippocampus,midbrain}[2]를 **진부분집합으로 포함** = 가소성이 각인 비국소화; 여섯 부위가 장은 깨끗 전달·흔적은 off-target 각인; 보편 focal>diffuse 흔적 법칙 부재[3/12만], 정직한 무-튜닝)·**중계 각인이 구조적 기본값**(8/12, **§46의 깨끗-기본값 10/12을 결합이 뒤집음** — 순간 발자국은 기본 focal이나 지속 표지는 기본 비국소화); 영-구동+η=0 M9 bit-identical·η=0서 W 동일·focal 정확 복귀(E0.3 상속); [L] 방향 임상 대응(자극-유발 가소성[rTMS/tDCS 후효과·DBS]이 망-분산, 환자-예측 아님) |
| **E1×E2** | **공간 스위치 레버리지: 어느 초점 구동이 집합 상태를 가장 쉽게 뒤집는가 (둘째 교차축 결합 · §29 양극성 에피소드의 공간 형제)** | **§48** | **✅ DONE (v1.55)** | **둘째 교차축 결합** = §43 공간 층(어디 WHERE)을 §28 상태-전환 층(쌍안정 뒤집기 FLIP, fold·latency)에 **혼인** = **§29 양극성 에피소드의 공간 형제**(§29는 집합 상태가 **언제** 시간 구동 하 뒤집히는지·§48은 **어디** 어느 초점 구동이 가장 싸게 뒤집는지); 두 층 **모두 import**(재유도 아님 — `SpatialField`+`BistableSwitch`), 유일한 새 객체는 둘을 잇는 `LeverageSwitch`. 구동되는 것은 노드별 장이 아니라 §28 **단일 집합** 쌍안정 상태이므로 유효 구동 = 구동 노드의 **방송 레버리지** `lev_j = colsum_j of W0`(동결 커널 열 합 = 노드가 주입하는 총 1-스텝 ephaptic 전류 = 순수 readout, 새 상수 0), `h_eff(j,b0)=b0·lev_j`, DOWN 출발·fold `spinodal(g)` 교차 시 flip, 역치 `b0*=spinodal(g)/lev_j`(레버리지에 반비례). 강도 b0∈{0.3,0.5,0.7,0.9} **그리고** 장벽 g∈{0.7,1.0,1.3} **이중 스윕** 생존: **flip-threshold 순위 = 방송-레버리지 순위·장벽-불변**(가장 쉬움 basal_forebrain_chol lev≈1.79 b0≈0.22 → cerebellum 겨우 b0≈1.0; **고정 비전환 소수 {thalamus,olfactory_bulb}** lev≈0.21 절대 안 뒤집힘)·**뒤집기-용이성이 레버리지 추적 + critical slowing**(역치·latency 둘 다 레버리지에 단조 감소, brainstem 최대 latency ≈5.68 발산)·**스위치성이 §46 순간-발자국 축 AND §43 도달 축 둘 다와 디커플링**(§46 장-중계 {hippocampus,midbrain} 스위치 MID-rank 5–6·스위치 허브 basal_forebrain_chol은 §46 self-localising; **§43 reach 허브 cerebellum이 스위치-rank 10/12** = 가장 어려운, 뒤집기-어려운 집합 {thalamus,olfactory_bulb,cerebellum} 전부 §46 self-localising = **보편 reach→switchability 법칙 부재**, 멀리 도달·깨끗 전달·집합 상태 뒤집기는 세 다른 속성, 정직한 무-튜닝)·**다수-전환가능(10/12)+고정 비전환 소수(2)**(§46의 깨끗-전달 기본값 10/12과의 정직한 대비); 영-구동(b0=0→h_eff=0) E.settle bit-identical·fold E.spinodal(E2.4 상속); [L] 방향 임상 대응(최고-레버리지 허브 basal_forebrain_chol·hypothalamus = 전역 뇌상태/각성 제어 허브가 상태 전환 게이팅, 환자-예측 아님) |
| **E0×E2** | **Kindling: 반복 상태-flip이 더 쉬워지는가 (셋째 교차축 결합 · §29 양극성 에피소드가 [O]로 남긴 trace→threshold 링크를 닫음)** | **§49** | **✅ DONE (v1.56)** | 아틀라스 **셋째 교차축 결합** = §26 가소성 층(진화하는 connectome·지속 흔적)을 §28 상태-전환 층(쌍안정 flip·fold)에 **혼인**, 그리고 §29 양극성 에피소드(B3)가 **명명만 하고 [O]로 남긴** trace→threshold 결합을 **닫는** 모듈; 두 층 **모두 import**(재유도 아님), 어느 층도 단독으로 못 묻는 질문(E0엔 쌍안정 flip 없음·E2엔 진화하는 connectome 없어 반복 축적 불가) = **반복 flip이 단일 집합 쌍안정 상태를 더 쉽게 만드는가**. 유일한 새 객체는 §28 셀을 §26 connectome 통해 구동하는 kindling switch: 반복 flip 에피소드가 위상-Hebb 갱신을 구동해 connectome이 공고화하고, 외부 push p의 유효 구동이 connectome의 **협응 게인** L(W)=R(W)/R_anchor(진화하는 connectome의 순서변수를 동결 M9 앵커로 정규화, 순수 readout, W0서 =1, §48 방송-레버리지를 **전역** 결맞음 게인으로 일반화)로 스케일 → flip 역치 p*=spinodal(g)/L이 connectome 공고화에 따라 **내려감**. 율 η∈{0.03,0.05,0.08} **그리고** 장벽 g∈{0.7,1.0,1.3} **이중 스윕** 생존: (K1) 반복 flip이 trace ‖dW‖를 **strictly-monotone 심화**(0→0.43)하고 flip 역치가 un-kindled fold **아래로**(g=1.0: 0.3849→0.3783) = **kindling**·**장벽-불변**(매 깊이서 kindled 역치가 그 깊이 자신의 fold 아래, p*=spinodal(g)/L) = **§29 [O] 공급**; (K2) push-space hysteresis 루프 **좁아짐**(2·spinodal(g)/L, 0.770→0.757)+고정 push서 교차 **latency 짧아짐**(4.96→4.72); (K3, 진짜 새 결합 결과+정직한 음성) **kindling은 공고화적 not 퇴행적** — '반복 flip이 협응을 **침식**해 더 쉽게 flip한다'는 깨끗한 가설 **거부**: 역치가 내려가는 동안 협응 R(W)이 **상승**(0.3896→0.3964)하고 kindled connectome이 앵커 **이상**으로 끝남(덜이 아니라 **더** 협응) = easier-flip과 침식이 **디커플링**, 역치는 **공고화**로 내려감(최저 율서 첫 에피소드 무시할 만한 transient 정직히 공개); (K4) **단일 일관 공고화 솔기** — 역치가 누적 trace ‖dW‖에 monotone-감소(trace가 **kindling 변수** = §29가 남긴 명시적 trace→threshold 법칙), [L] 방향-전용 임상 대응(Goddard 전기적 kindling·양극성 주기 가속 = 반복이 다음 전이 역치를 내림, 환자-예측 아님). η=0이면 connectome 동결·R = 동결 M9 앵커 **bit-for-bit**·게인 L=1·역치 = un-kindled fold(E0.4 상속), 영 push면 집합 상태 E.settle **bit-for-bit**(E2.4 상속); 27번째 시민 E0E2-KINDLING(`3880e63f…`)·`KindlingSwitch` 결합 객체·새 튜닝 상수 0·엔진 byte-unchanged; 방화벽 절대(집합 쌍안정 상태·flip 역치·trace·협응 게인은 STRUCTURAL, 느껴진 기분·의식·재발-용이성 절대 아님·실제 connectome/kindling 역치/환자-예측 아님·Axis-A·consciousness_claim=0·hard problem OPEN·efficacy=0·NOT medical advice) |
| T3c | OCD | — | ⏳ Tier-3 | |
| **CROSS-SYNTH** | **교차축 결합 메타-종합: 세 결합·세 디커플링·하나의 규율 (캡스톤 — 세 교차축 결합[§47 E1×E0·§48 E1×E2·§49 E0×E2]을 단일 family로 인증)** | **§50** | **✅ DONE (v1.57)** | 메타-종합(새 측정 0·새 기계 0·새 튜닝 상수 0): 세 교차축 결합 §47 공간-가소성 각인(E1×E0)·§48 공간 스위치 레버리지(E1×E2)·§49 kindling(E0×E2)을 **단일 FAMILY로 인증**(T1–T5); 소스 3 결과 SHA(§47 `cdb16230…`·§48 `bd3a9e23…`·§49 `3880e63f…`) **비트-단위 재검증 후 읽기**·엔진 READ-ONLY byte-unchanged. **핵심 = 세 층 E0/E1/E2의 완전한 삼각형**: 세 결합이 세 쌍별 edge {E1,E0}·{E1,E2}·{E0,E2}를 **모두** 실현하고 **각 층이 정확히 두 결합에 등장**(E0∈§47,§49·E1∈§47,§48·E2∈§48,§49 = degree 2, 프로그램적 검증)·각 결합이 구동 끄면 동결 엔진 bit-for-bit 복귀. **공통 형태 = 디커플링**: 각 결합의 진짜 새 결과가 디커플링이고 셋 모두 깨끗한 단일-축 가설을 거부·정직히 보고 — 깨끗한 전달 ≠ 깨끗한 각인(§47 C3, 흔적-중계 ⊃ 장-중계 8⊃2)·스위치성 ⊥ 발자국 AND 도달(§48 C3, reach 허브 cerebellum switch rank 10/12)·easier-flip ⊥ 침식(§49 K3, R 0.3896→0.3964 상승)·"공간이 시간을 만나면 각인이 전달과·공간이 상태를 만나면 flip이 발자국·도달과·시간이 상태를 만나면 kindling이 침식과 디커플링". 결합당 하나의 새 잇는 객체(imprint readout·leverage switch·kindling switch)·각 두 층 read-only 재사용·새 튜닝 0·하나의 결합 규율 세 번(두 축 스윕·bit-for-bit 복귀[각 층 가드 상속]·정직 보고). §42 E0-triad 종합(한 층의 세 **읽기**)을 거울로 하되 **세 층의 세 결합**을 닫음 = **교차축 결합 아크 완결**. 28번째이자 마지막 시민 CROSS-SYNTH(`028fdbcc…`)·`[V synth]`·방화벽 절대·3중 상속(각인·레버리지·flip 역치·trace·협응 게인은 STRUCTURAL·느껴진 상태/의식/재발-용이성/실제 connectome/타깃 전환성/환자-예측 아님·Axis-A·consciousness_claim=0·hard problem OPEN·efficacy=0·NOT medical advice) |

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
