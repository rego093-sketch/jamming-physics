# VP 신체 프레임워크 — 전체 지도 (MASTER MAP)

> 한 장으로 보는 "우리가 무엇을 다루고 있는가". 패키지가 많아져 혼란을 덜기 위한 단일 정리 파일.
> 모든 신규 패키지의 **DOI는 TBD — 작성·발행 후 부여(추후 업데이트)**. 개념 DOI와 cross_volume_doi 레지스트리 등록은 집필 단계에서 한다.

---

## 0. 한 문단 그림

하나의 전제 — **진공 = jammed 탄성 고체(R19 이중우물 스위치 + FitzHugh-Nagumo 이완 진동자)** — 에서 물리·생물을 모두 유도한다. 이 단일 기질이 DNA 유전자, 뉴런, 그리고 모든 장기/루프/시계를 *재창발*한다. 신체는 **물리적 클래스/시간 축**으로 분해된 패키지들로 덮이고, 각 패키지는 같은 기질을 공유하되 **seam(이음매) 변수로만** 연결된다(SSOT). 모든 정량은 *측정 입력(잠금·인용)* 또는 *유도*이며 **목표에 맞춰 고르지 않는다(no-tuning)**. 등급은 정직하게 `[F]강제 / [V]시뮬검증 / [L]측정 / [O]개방(사유명시)`.

---

## 1. 토대 — VP 물리 (신체가 그 위에 앉는 6개 비-생물 백서)

VP-SPEC §2 레지스트리의 발행 백서. 신체 프레임워크의 기반이며 이미 성숙·발행됨.

| paper | 핵심 | 상태 |
|---|---|---|
| **physics** (VP Theory) | c²=B/ρ, m_p/m_e=6π⁵ | 발행 (DOI 有) |
| **fluid-dynamics** (Configured Continuum) | 연속체·jamming 분기 | 발행 |
| **cosmology** (Vacuum-Inflow) | a₀=cH₀/2π | 발행 |
| **geodynamics** (Jamming Geodynamics) | 대륙 분리 항복 | 발행 |
| **geochronology** (Cross-Chronometer Limit) | 연대 정확도 한계 | 발행 |
| **chemistry** (VP Chemistry & EM) | 단일 앵커 화학·전자기 | 발행 |

---

## 2. 신체 3대 기둥 (성숙 — 이미 발행, 레지스트리 등재)

| 패키지 | 다루는 것 | 상태 |
|---|---|---|
| **DNA** (4D DNA Blueprint) | **형태/정체성** — 측정 γ로 장기 정체성 + 발생순서 창발. *모든 신체 패키지가 인용하는 SSOT*. | 성숙 v1.12, DOI 有 |
| **neuro** (Neural Emergence Chain) | **체성 신경 기계** — 이온채널→행동. **공유 FHN/R19·CPG 프리미티브 제공자**. | 성숙 v1.10.1, DOI 有 |
| **mind** (Felt Cognition) | **느낌(felt)/정동 층** — 의식의 어려운 문제. 심장은 felt/구심 팔만(기계는 cardioresp). | 성숙 v1.27, DOI 有 |

> **4번째 방법론-성숙 트랙**: **disease_wp** (희귀·유전병 SSOT, v0.13/R11). 방법론·게이트는 성숙(R1–R11 전부 PASS)하나 DOI 등록 대기·심층 35병 단계라 위 3대 발행 기둥과는 분리해 **§6에서 추적**한다. 소유 경계는 §6 계약이 규정한다.

---

## 3. 기계 동역학 패키지 (7) — *이번에 골격 제작, 연구 단계*

장기를 측정 γ로 창발해 *순환*시키고, 동역학·질병(암)을 다룬다. 분해 기준 = **물리적 클래스**(교과서 라벨 아님).

| 패키지 | 물리 클래스 | 핵심 장기 (γ) | 주요 질환/암 | DOI |
|---|---|---|---|---|
| **cardioresp** | 진동자+제어 | 심장(NKX2-5)·폐(NKX2-1) | 폐암(담배/라돈/PM2.5); RSA·Cheyne-Stokes | TBD |
| **circulatory** | 흐름+청소 | 신장(SIX2)·간(HHEX)·혈관 | 신세포암·간세포암(아플라톡신×HBV) | TBD |
| **digestive** | 느린수송+대사항상성 | 위(BARX1)·장(CDX2)·췌장(PDX1)·간 | 대장암·위암(H.pylori 시너지)·췌장암 | TBD |
| **musculoskeletal** | 구조·역학부하 | 근육(MYOD1)·연골(SOX9)·사지(TBX5)·뼈(RUNX2*) | 골육종(방사선; 환경발암 약함—정직표기) | TBD |
| **immune_hematologic** | 집단-역치/클론 | 흉선(FOXN1)·비장(TLX1)·골수(RUNX1*)·림프(PAX5*) | 백혈병(벤젠)·림프종; **면역회피=교차 발암 변조** | TBD |
| **integumentary** | 장벽·외부자극 | 표피(TP63)·각질(KRT14)·멜라닌(MITF)·부속기(EDAR) | **흑색종/SCC(UV)—가장 깨끗한 발암 사례** | TBD |
| **reproductive_endocrine** | 호르몬주기·생식세포 | 고환(SOX9)·난소(FOXL2*)·생식세포(DAZL*)·관(WT1*) | 유방암(에스트로겐)·자궁경부암(HPV)·전립선암 | TBD |

\* = master 유전자는 명명됐으나 γ 미측정 → 정직하게 "측정 대상(DNA 파이프라인)"으로 보류(날조 아님).

---

## 4. 통합 항상성 패키지 (3) — *이번 제작, 연구 단계*

장기를 재창발하지 않고 형제 seam에서 **루프를 폐합**한다. 질병 = 방어 setpoint의 실패(attractor-shift). "정의 변수가 어느 단일 장기도 소유하지 않는 루프 양"일 때 통합이 필수.

| 패키지 | 항상성 축 | 핵심 | 주요 질환 | DOI |
|---|---|---|---|---|
| **homeostasis_thermometabolic** | 열+에너지 | **항온/변온 근본 → 열생성(UCP1)·겨울잠 스위치·에너지 항상성**. 질병은 *일부*. | T2당뇨·비만·대사증후군 (겨울잠 다리 가설) | TBD |
| **homeostasis_hemodynamic** | 압력/용적 | MAP=CO×SVR×용적 루프; 고혈압=setpoint 재설정 | 본태성 고혈압·만성 심부전 | TBD |
| **homeostasis_ionic** | 미네랄/산염기 | Ca-PO4(PTH↔비타민D↔뼈↔신장)·pH(폐CO₂+신장HCO₃)·전해질 | 골다공증·부갑상선항진·산염기/전해질장애·신결석 | TBD |

> **thermometabolic 특기**: "왜 곰은 겨울잠을 자나"가 큰 축. `torpor_switch_probe()`가 *깨어남↔휴면이 R19 불연속 스위치인가 연속 다이얼인가*를 spinodal로 framing. 곰-vs-인간 = 스위치가 인간 게놈에 잠겨 있나 없나(종간 비교). 연구과제 5층 14개.

---

## 5. 시간/교차-절단 층 (2) + 특수감각 (1) — *이번 제작, 연구 단계*

| 패키지 | 성격 | 핵심 | 주요 질환 | DOI |
|---|---|---|---|---|
| **circadian** | 시간(결합 진동자) | ~24h 시계망(SCN+말초), 자유진동+빛 entrainment, **모든 setpoint를 gating** | 일주기 수면각야장애·교대근무 대사/심혈관·교대근무 암(IARC 2A) | TBD |
| **aging_senescence** | 시간(쇠퇴 capstone) | 모든 setpoint의 느린 표류 + 세포노화(갇힌 attractor). **전 발암 커널의 위험 승수** | 근감소·노쇠/다질환·노화=암 위험승수 | TBD |
| **sensory_organ** | 기기 물리+R19 변환 | 눈 광학·달팽이관 주파수지도·전정 균형·미각/후각. **광학/음향은 고전물리(정직)**, R19는 세포 변환 | 백내장·녹내장·황반변성·근시·노인성난청·당뇨망막병증·BPPV | TBD |

---

## 6. 질병 소유권 계약 (OWNERSHIP CONTRACT) — 충돌 방지의 핵심

> **분할 축은 "신체 부위"가 아니라 "병인(etiology) 클래스"다.** disease_wp도, 기계/항상성 패키지도 *모든 부위*를 건드린다(신장도 둘 다, 심장도 둘 다). 부위로 나누면 충돌한다. **무엇이 그 병을 설명하는 과학 기계인가**로 나눈다.

| 소유자 | 병인 클래스 | 설명 기계 | 예 |
|---|---|---|---|
| **disease_wp** (rare-disease SSOT) | **단일유전자·희귀·유전병** (유전자-키) | 유전자→분자기전→primary-system 분류 + 정직 burden order | Marfan(FBN1)·DMD·Gaucher·PKU·CF·낫적혈구 |
| **기계 동역학 7 + 감각 1** | **후천성·다인자·흔한 병** (동역학-키) | 발암물질→R19 장벽↓→Kramers 교차 / setpoint 동역학 실패 | 폐암·흑색종·SCC·국소 부정맥·신RCC |
| **통합 항상성/시간 3+2** | **루프 조절이상** (단일 장기 아님) | 형제 seam에서 방어 setpoint 폐합 실패(attractor-shift) | 당뇨·고혈압·비만·골다공증·노화 |

**핵심 구분 한 줄**: disease_wp = *유전자가 정의하는* 병 / 기계·항상성 = *동역학이 정의하는* 병. 같은 R19·Kramers 커널이되 한쪽은 셀-레벨 유전자 병변, 한쪽은 시스템-레벨 setpoint 표류.

### 6.1 겹침 구역 tie-break (실제 충돌이 나는 지점)

1. **단일유전자가 정의하고 희귀** → **disease_wp**. (정의 자체가 유전자-키.)
2. **흔한 후천성 병이지만 단일유전자 아형 존재** (가족성 HCM · MODY · 가족성 고콜레스테롤혈증 · 유전성 RCC(VHL) · BRCA 유방암 · Lynch 대장암) → **기계/항상성 패키지가 "흔한 병 + 동역학"을 소유**, disease_wp는 *단일유전자 아형을 명명된 엔티티로 소유*하고 유전자-병변 파라미터를 export. **양방향 교차참조**.
3. **발암 암** (폐암·흑색종·SCC 등 — 발암물질→R19 장벽↓로 *구성상* 후천성) → **기계 패키지**, 절대 disease_wp 아님. **유전성 암 증후군** (Li-Fraumeni · VHL · Lynch · 유전성 망막모세포종 · 유전성 유방난소암) → **disease_wp**, 기계 패키지가 교차참조.

### 6.2 합성 규칙 (seam — 겹치지 않고 *합성*)

disease_wp가 단일유전자 병변(예: MODY = GCK setpoint 파라미터)을 **소유** → 기계/통합 패키지가 그 파라미터를 **유전자-키로 import**해 전신 궤적 계산. disease_wp는 *유전자-병변 사실*의 SSOT, 기계 패키지는 *시스템 동역학 결과*의 SSOT. 물리적 병합 없이 계약으로 연결(라이브 배선은 §9.2 미구현 항목).

### 6.3 disease_wp 현황 (이 트랙의 관리자 = disease_wp R-체인 패키지)

| 항목 | 값 |
|---|---|
| paper_id / code | `disease` / `dis` — *Systemic Genetic & Rare Disease Mechanisms* |
| 버전 | **v0.13** (Phase R11 complete) |
| 스코프 | ClinVar 열거 **7,672**병 → in-scope(systemic) **6,167** (neuro 1,282 / cardiac 170 / psych 37 제외 — 전부 로그, 무단 누락 0) |
| 심층 코호트 | **35병** 풀 dossier (R1–R11): 유전자기능·variant_spectrum·기전·임상·burden·치료, 질병 1개당 독립 HTML 1장 |
| burden order | 정직 **provisional [H]** / order_locked **4/35** (Achondrogenesis II · NPD-A · Tyrosinemia II · Marfan) |
| 등급 출처 | Orphanet(onset [L] 28) · GBD2013(disability [L] 13) · HPO Severity subtree HP:0012824(severity [L]) · PMC-OA(progression [L], **frozen-R3 tier**) · GeneReviews(treatment [L] 33) |
| 게이트 | R1–R11 + consolidation + unmet-need + W1 사이트 **전부 PASS**, carried 엔진 핀 drift 0 |
| DOI | 등록 대기 (날조 accession 없음) |
| 정직 미완 | `organ_system`은 6,167 인덱스에서 아직 **미분류**(hint 공란) — 심층 코호트 외 확장은 향후. severity는 open data로 부분만 [L] 가능(6병이 lock 한 발짝 앞, 정직하게 [H] 보류). |

> **경계 작동 보증**: disease_wp는 이미 `in_scope` 플래그 + 제외 사유 로그로 neuro/mind 경계를 감사 가능하게 유지한다("name it, don't hide it"). 위 §6.1 tie-break는 기계/항상성 패키지에 대한 **동일 규율의 한 축 추가**일 뿐 — 신규 메커니즘 아님.

---

## 7. 공유 기질 & 규율 (전 패키지 공통)

- **기질**: `inherited/vp_substrate.py` — R19 이중우물(`sdot/spinodal/barrier/settle`) + FHN `Neuron` + `Organ/dwell`. neuro 엔진에서 verbatim vendoring(단일 소스, 수정 금지).
- **창발 공식**: 발암 = 발암물질이 세포 R19 스위치 장벽을 낮춤 → Kramers 교차 → RR(dose). 질병 = setpoint 루프가 같은 방식으로 병적 basin 교차. **동일 커널, 셀↔시스템 레벨**.
- **no-tuning**: γ는 측정(NN-stacking ΔG37) 또는 미측정→"측정 대상". 절대 fitting 없음.
- **연구 우선 게이트**: `build_docs.py`는 ① `research_gate` all_green(결정론 2×sha256 + 스트레스 배터리 전체 PASS) ② `PHASE=writing` 전엔 집필 **거부**.
- **집필 정본**: HTML(C2). 제목별 별도 SEO HTML(C4: answer-first·JSON-LD·claim-strip·vp-card). 본문 영어(C0). [O] 사유 명시(C3).
- **인수인계**: 새 창은 `START_HERE.md → CHARTER.md`만 읽으면 자족. 단일 zip 반환(파편화 금지).

---

## 8. 현황 한눈 (신규 13개)

| 패키지 | 버전 | γ grounding | 연구과제 수 | 게이트 | 단계 |
|---|---|---|---|---|---|
| cardioresp | 0.1.0 | 충실(2/2) | 5 | 미통과 | 연구 |
| circulatory | 0.1.0 | 충실(2 vendored) | 5 | 미통과 | 연구 |
| digestive | 0.1.0 | 충실(4/4) | 5 | 미통과 | 연구 |
| musculoskeletal | 0.1.0 | 부분(3 vendored,1 측정대상) | 5 | 미통과 | 연구 |
| immune_hematologic | 0.1.0 | 부분(2+2) | 5 | 미통과 | 연구 |
| integumentary | 0.1.0 | 충실(4/4) | 5 | 미통과 | 연구 |
| reproductive_endocrine | 0.1.0 | 부분(1+3) | 5 | 미통과 | 연구 |
| homeostasis_thermometabolic | 0.1.0 | 충실(7 vendored) | **14** | 미통과 | 연구 |
| homeostasis_hemodynamic | 0.1.0 | 부분(1+1) | 5 | 미통과 | 연구 |
| homeostasis_ionic | 0.1.0 | 부분(1+4) | 5 | 미통과 | 연구 |
| circadian | 0.1.0 | 측정대상 위주(0+1) | 5 | 미통과 | 연구 |
| sensory_organ | 0.1.0 | 충실(5 vendored) | 5 | 미통과 | 연구 |
| aging_senescence | 0.1.0 | 측정대상 위주(0+4) | 6 | 미통과 | 연구 |

전부 `python repro/run_all.py`로 즉시 실행됨(노드 창발 + 진동자/probe + 게이트). 동역학·스트레스·질병 모듈 본체는 다음 연구 세션에서 채움.

---

## 9. 아직 남은 큰 일 (아키텍처 외)

1. **연구 본체** — 위 13개의 동역학/스트레스/질병 모듈이 전부 TODO. 게이트 0/13 통과. *전체 작업의 ~95%*.
2. **교차-패키지 통합 하니스** — seam은 *선언된 계약*일 뿐, 형제 출력을 읽는 라이브 배선 없음. "한 몸" 결합 실행 러너가 미구현(대사증후군 클러스터 등 다계 현상은 결합해야 창발). **disease_wp의 유전자-키 파라미터 export(§6.2)도 이 미배선 계약의 한 사례** — MODY=GCK 등은 계약상 선언됐으나 기계 패키지가 실제로 읽는 배선은 아직 없음.
3. **SSOT 드리프트 가드** — 13개가 각자 vp_substrate·VP_SPEC 복사 vendoring. neuro 원본과 byte-identical 유지 강제 가드 필요(프리미티브 변경 시 조용히 stale 방지).
4. **출판 레지스트리** — 신규 13개의 DOI·cross_volume_doi·jamming-physics.org 사이트 편입은 각 패키지 집필 완료 후(현재 전부 TBD).

---

## 10. 전체 카운트

- 토대 물리 6 + 신체 기둥 3(DNA·neuro·mind) + **신규 신체 13**(기계 7·항상성 3·시간 2·감각 1) + **disease_wp 1** = 신체 생리 관련 **17 패키지**.
- 신규 13은 모두 **연구 단계 골격**(v0.1.0-research), DOI 추후.
- **disease_wp**는 방법론-성숙(v0.13/R11, 전 게이트 PASS)·DOI 등록 대기. 심층은 **35병 dossier**, 열거 인덱스는 6,167병(장기 분류는 향후). 소유 경계는 §6 계약. **분할 안 함** — 희귀병 SSOT는 부위가 아니라 병인으로 단일 볼륨 유지(쪼개면 §9.3 드리프트 + 다계 엔티티 파편화).
