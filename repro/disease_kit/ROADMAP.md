# ROADMAP — VP Disease Emergence Kit

**개념 DOI 10.5281/zenodo.20755262 · 희귀병(rare / single-gene / hereditary) · CC BY 4.0 · ORCID 0009-0002-7535-8245**

이 로드맵은 "질병을 더 모으자"가 아니라 **무엇이 다르고, 그 다름이 어떻게 고통을 줄이는가**를 기준으로
v0.22.0 시점에 *재설계*되었다. 분석 이력(changelog)의 정본(SSOT)은 `VERSION` 이다 — 여기선 복제하지 않고
설계에 집중한다.

---

## 0. 목적과 차별점 — purpose & differentiation (read this first)

### 한 문장
> 실제 프로모터 DNA 를 **결정론적으로, 할 수 있는 최대로** 창발시켜 그 질병을 *어느 방향으로 밀어야 하는가*
> (axis up / down)까지 도출한다. **한계가 진짜인 곳에서만 멈추고** — 크기·용량·효능은 프로모터 *구조*에서
> *원리적으로* 도출 불가(→ `[O]`); 단일유전자 핵 프로모터 스위치로 *읽히지 않는* 병변(→ 보류) — 그 한계를
> 정직하게 표시한다.

### 원칙: 분석이 되는 곳은 최대로 (도리), 어려운 곳은 한계만큼

1. **일부러 얇게 하지 않는다.** 잘 읽히는 질병은 γ 스위치 하나로 그치지 않고, **DNA 가 뒷받침하는 모든
   결정론적 신호를 끌어낸다** — 다유전자 네트워크의 결합 dwell, 세포-운명 스위치, 조절-병변의 *직접* 읽기,
   열역학 feasibility. 분석이 되는데 안 하는 것은 도리가 아니다. **분석은 최대로 하는 게 옳다.**
2. **한계는 *선택*이 아니라 *실재*다.** 크기 / 용량 / 효능이 `[O]` 인 것은 보수적이어서가 아니라, 프로모터
   *구조*에서 그 수치가 *원리적으로 나오지 않기* 때문(인식의 경계). 보류는 신중해서가 아니라, 그 병변이
   단일유전자 핵 프로모터 스위치로 *실제로 읽히지 않기* 때문.
3. **어려운 것은 한계에 따라 할 만큼 한다** — 그리고 한계가 무는 지점을 `[O]` / `[CAL]` / suspend 로 정직하게
   남긴다. **최대한 읽되, 못 읽는 곳을 읽은 척하지 않는다.**

### 무엇이 다른가 — vs. 남들이 하는 것

차별은 *얇음*이 아니라 **(가능한 최대의 결정론적 분석) + (진짜 한계만 정직히 표시)** 의 결합이다.

| | 남들 | 이 키트 |
|---|---|---|
| 변이 해석(ACMG) | 병원성/양성 **분류** | 분류 안 함 — DNA 가 허용하는 **최대로 밀 방향**을 도출 |
| 신약개발 파이프라인 | 거대·고비용·표적검증 중심 | 분 단위·오프라인·결정론적 **방향**(치료 가설의 출발점) |
| 질병 DB(OMIM/Orphanet) | **목록**화 | 목록 아님 — 스위치를 **창발**해 추론 |
| ML 재배치/예측 | 효능·연관을 **확신**(불가검증·과대주장 빈번) | **크기를 거부**(원리적 한계) — 방향만, falsifier 동반 |
| 지식그래프 | 유전자-약물-질병 **연관** | 통계적 연관 아님 — 물리적 스위치 read + 방향 강제 |

핵심 차별 = **네 가지의 결합** (각각은 단독으론 신기하지 않지만, 함께 묶이면 드물다):

1. **최대의 결정론·재현(drift 0)** — 같은 입력 → 비트-동일 출력. 가능한 한 깊게 읽되, 통계적 추정이 아니라
   **물리적 read**(γ = SantaLucia 1998 최근접쌍 열역학 → R19 cusp → barrier / threshold).
2. **방향-전용 방화벽 = *실재하는* 인식 한계** — 구조 `[V]` · 방향 `[F]` · 크기/용량/효능 `[O]`.
   과대주장 ML 의 정반대.
3. **보류 규칙("없으니 못한다") = *실재하는* 가독성 한계** — 읽히지 않으면 지어내지 않고 보류
   (지금까지 5가지 보류 기전 부류: 이수성 · 임프린팅 · 반복-탈억제 · 미토콘드리아 게놈).
4. **재도출 sanity check** — 창발된 *방향*이 승인약의 방향과 독립적으로 일치(우연이 아니라 점검). 단, *방향*
   일치이지 효능 증명이 아니다.

### 어떻게 고통을 줄이는가 — the suffering-reduction logic

- **승인 치료가 없는 수천 개 단일유전자 희귀질환**: 방향조차 정리 안 된 곳이 많다. 변호 가능한 방향 하나는
  치료 가설의 출발점 — 시장이 작아 제약사가 외면하는 바로 그곳에서. 여기서 분석을 *최대로* 하면 그만큼 더
  쓸모 있는 방향이 나온다.
- **거짓 희망 차단**: 승인약이 사실은 *하류·증상*(Rett/trofinetide, FRDA/omaveloxolone)인지 *스위치-수준*
  (LCA2 유전자치료)인지 구별·기록. 한계 너머를 주장하지 않는 규율 자체가 환자를 보호한다.
- **괴리의 투명한 기록**(HHT 식 downgrade-and-disclose): 스위치는 "브레이크 복원"을 원하는데 임상엔 하류
  차단제뿐일 때, 그 *간극*이 곧 다음 연구 방향이다.
- **재현·무료·CC BY**: 누구나(제약사 포함) 비용을 낮춰 더 나은 치료를 탐색하도록.

### 텔로스: 새 치료를 *싸게 유도* — the catalytic mission (연못에 돌)

이 키트의 최종 목적은 *치료를 직접 발견*하는 것이 아니다(그럴 수 없다 — 크기·효능은 `[O]`). 목적은
**검증 가능한 치료-방향 가설을 가능한 한 싸게 생성**해, *실제로 치료를 개발할 수 있는 행위자*(제약사 ·
임상-연구자 · 환자단체 · 펀더)를 **움직이게** 하는 것이다. 알려진 것이 적은 희귀 단일유전자병일수록 정리된
방향 가설 하나의 한계가치가 크다. **연못에 돌을 던진다** — 파문을 일으켜 움직이게 한다.

**과대보수성은 무익(無益)이다.** 변호 가능한 방향 가설을 *소심함* 때문에 억누르면 아무 유익도 못 준다.
규칙: **생물학이 방향을 강제하는 곳에서는 방향을 낸다 · 정직하게 등급한다 · 크기는 결코 부풀리지 않는다.**
보류는 *실재하는 가독성 한계*에서만(소심함이 아니라). — 이 둘(대담한 생성 + 정직한 표시)은 충돌하지 않는다.

**정직성 = 촉매력의 무게(돌의 질량).** 과대주장된 결과는 *기각*되고 프로그램 전체의 신뢰를 깎는다. 정직하게
범위가 그어진 가설은 *검증된다*. 즉 방화벽은 브레이크가 아니라, 돌이 *가라앉게* 하는 바로 그 무게다 —
"이건 미검증 방향 가설이다([O], falsifier 동반)"라는 정직한 라벨이 있어야 연구자·제약사가 집어든다.

**그런데 — 돌이 실제로 가라앉으려면 정직하게 짚을 것**: 키트의 `[F]` 방향은 *이미 인용된* GOF/LOF 생물학에서
강제된다. 따라서 *맨방향*("결핍 효소를 보충하라", "과활성 채널을 억제하라")은 대개 전문가에겐 *이미 자명*하다 —
신규성이 낮다. **제약사를 움직이는 건 자명한 방향이 아니다.** 촉매적 신규성은 세 곳에 산다:

1. **승인약-없는 꼬리(III-A) = 최우선 산출물.** 방향은 강제되는데 승인 약제가 *없는* 질병(현재 resolved 꼬리
   10개). 여기서만 키트의 방향이 진짜 *추가*된다. 이것을 묻지 말고 **가장 행동가능한 형태**로 표면화한다:
   질병 → 축 → 강제 방향 → *후보 약물 클래스* → **가장 싼 반증 실험**.
2. **교차질환 재배치 가설(repurposing) = 가장 높은 레버리지(NEW).** 키트의 *같은-축·같은-lever* 구조는
   "질병 X(승인약 없음)가 질병 Y(승인약 Z 있음)와 동일 축-교란 서명을 공유 → **Z의 기전 클래스가 X의 검증가능
   방향 가설**"을 자동 surfacing할 수 있다. 희귀병 신약의 가장 싼 길이 바로 *재배치(repurposing)*다 — 이것이
   제약사·임상의를 움직이는 실제 돌이다(맨방향이 아니라).
3. **switch↔임상 간극의 폭로(III-B).** 스위치는 "브레이크 복원"을 원하는데 임상엔 하류 차단제뿐일 때, 그
   *간극*이 곧 자명하지 않은 다음 연구 방향이다.

→ 다음 계획(§3 v0.28.0+)은 이 셋을 **명시적 산출물**로 만든다 — 재배치 스캐너 + 촉매적 open-directions 카드.

---

## 1. 불변 설계 원칙 — invariants (the firewall = real limits, honestly marked)

방화벽은 보수성이 아니라 *실재하는 인식 한계*다 — 그것이 신뢰의 근거이자 차별점이다. 어떤 확장도 이 선을 넘지
않으며, 분석은 이 선 *안쪽에서 최대로* 한다.

- 방향만 `[F]`; 크기·친화도·용량·효능·치료율은 `[O]` (프로모터 구조에서 원리적으로 도출 불가). 넘으면
  GATE 1 빌드 실패.
- 읽히지 않으면 보류 — 강제 read 금지(가독성의 실재 한계).
- 결정론 drift 0; 모든 산출물 `determinism_sha`.
- 등급 `[V]` / `[F]` / `[O]` / `[CAL]` + 질병당 ≥1 측정가능 falsifier.
- 개인 의료조언 아님. (YMYL: 미검증 가설의 *무료 공개를 책임 있게* 만드는 것이 바로 이 한계 표시다.)

---

## 2. 다섯 기둥 — the five pillars (this is the roadmap)

### 기둥 I — READ 를 최대로: 분석이 되는 모든 곳에서 최대 분석 (도리)

방화벽을 넘지 않으면서 *창발 자체를 가능한 한 풍부하게.* 한계(크기·가독)에서만 멈춘다.
각 트랙: 무엇 · 합격 · 등급.

- **I-A 다유전자 네트워크 창발** (relay-ODE; `engine/emergence_engine.py`, `engine/param_db.json` — 이미 stub).
  - 무엇: 두 개 이상 스위치가 상호작용하는 작은 네트워크를 창발해 *결합 dwell 순서*를 보고
    (FGFR3 ↔ CNP/NPR2; TSC1 ↔ TSC2 ↔ mTOR; ENG ↔ ACVRL1). 지금은 가장 깊은 단일 스위치만 primary —
    네트워크는 *상호작용 방향*을 추가한다.
  - 합격: 기존 단일-스위치 read byte-identical 보존(drift 0) + 네트워크 read 는 *추가* 산출물.
  - 등급: 순서 `[F]`, 크기 `[O]`.

- **I-B 조절-병변 직접 read** (γ 가 *좌위*가 아니라 *병변 자체*를 읽는 가장 강한 read).
  - 무엇: 대부분 병변은 *코딩*이라 방화벽상 γ 는 *좌위 스위치*만 읽는다. 그러나 일부 병변은
    **프로모터 / 인핸서 / 조절부**에 있다(β-thal 프로모터 변이, haemophilia B Leyden 안드로겐-반응 프로모터,
    HBB/HBG HPFH, α-thal 조절부). 그런 질병에선 γ 가 *바로 그 병변*을 읽는다 — 한 단계 강한 read.
  - 산출물: 조절-병변 질환 우선 식별·추가, "γ reads the lesion itself" 태그로 코딩-병변 read 와 구분.
  - 등급: 구조 `[V]`(병변 직접), 방향 `[F]`, 크기 `[O]`.

- **I-C 세포-운명 스위치 창발** (`engine/organism/core.py`, `engine/vp_neuro_engine.py`).
  - 무엇: 축(농도 / throughput)에서 *세포-운명* 스위치로 확장 — 질병이 "잘못 맞춰진 운명 스위치"인 경우.
  - 등급: 방향 `[F]`, 크기 `[O]`.

- **I-D 방향 *신뢰도* (크기 아님)**. ✅ **v0.24.0 SHIPPED — `direction_confidence` 필드 + 점수판 노출.**
  - 무엇: 크기는 금지지만 *방향 자체의 견고함*은 정직하게 등급화 가능 — (역할 × 기전) 호출이 얼마나 깨끗한가?
    문헌에서 GOF/LOF 가 다투어지는가? 질병당 `direction_confidence`(clean / cited-contested / ambiguous) +
    근거. ambiguous 면 강제하지 말고 그렇게 말한다(→ 기둥 II-C).
  - 등급: 정성 `[F]`(근거 인용), 결코 크기로 환산하지 않음. **기본 clean(구성상 모호하지 않음), 레지스트리
    필드로 재정의; 58 clean / 3 cited-contested(RHO-adRP · α1-항트립신 · Rett) / 0 ambiguous; 파이프라인이
    무시하는 advisory 필드 → analysis.json 해시 불변(drift-0-safe).**

- **I-E 측정 열역학 pathway B** (`[CAL]`).
  - 무엇: 저자가 실측 ΔH / ΔS / ΔG_bind 를 줄 때만 `[CAL]` 로 Sabatier 창이 *방향-feasibility*를 말하게.
    친화도 / 효능 / 용량은 출력 안 함.

- **I-F 기존 read 최대화 retrofit** (도리의 소급 적용).
  - 무엇: 이미 ship 한 단일-스위치 read 중 DNA 가 네트워크 / 운명 / 조절-병변 read 를 뒷받침하는 것을 *추가*
    분석으로 보강. drift-0-safe additive(기존 산출물 불변, 새 필드만 추가).

### 기둥 II — 방법 검증: "최대로 한 방향"을 *변호 가능·반증 가능*하게

이 키트의 과학적 등뼈. 방향 청구를 *방법으로서* 반증가능하게 만든다.

- **II-A 방향-회수 점수판** (the empirical backbone). ✅ **v0.24.0 SHIPPED — `pipeline/direction_recovery.py`.**
  - 무엇: 모든 resolved 질병에서 창발 방향 == 승인약 방향인지 정량 집계(N / total, 부류별)를 *단일 점수판*으로
    동결. 지금도 매 질병이 이를 *개별* 재도출하지만, 이를 하나의 동결 산출물로 격상.
  - 정직성: *방향* 일치율이지 효능 주장이 아님 · 회고적. 불일치 사례는 *숨기지 않고* 기록(그게 정보다).
  - 합격: 점수판이 freeze 에 포함, drift 0. **결과: 61/61 방향 회수; 승인약-없는 고가치 꼬리 9개 표면화;
    축/lever/직접·간접/승인상태별 분해; 읽기전용 → per-disease 해시 불변; 이빨 있는 self-test; frozen sha 4def995f40d5.**

- **II-B 시간 hold-out 시험**.
  - 무엇: 치료 방향이 *특정 컷오프 이후* 확립된 질병으로 "그때 우리가 그 방향을 불렀겠는가"를 점검
    (예측적 성격의 회고).

- **II-C 모호-방향 정직성**.
  - 무엇: 방향이 진짜로 모호한 질병에선 키트가 *그렇게 말해야* 한다(낮은 `direction_confidence`),
    억지로 부르지 않는다 — 거짓 신호를 막는다.

- **II-D 질병별 falsifier → 방법 반증가능성**.
  - 무엇: 이미 질병당 ≥1 측정가능 falsifier. 이를 "이 *방법*이 틀렸다면 무엇이 관찰되어야 하는가"의 집합으로
    격상.

### 기둥 III — REACH: 방향이 고통을 가장 많이 줄이는 곳

"질병 추가"는 여기 살되, *수집*이 아니라 *영향*으로 재정렬한다.

- **III-A 승인-치료-없는 꼬리 우선** (한계가치 최대) — **촉매 미션의 1차 산출물**.
  - M10 부담순위(B / U / D)가 이미 있다. 최고가치 = 부담↑ · 미충족↑인데 *문헌에 방향이 아직 없는* 질병.
    거기서 키트의 방향이 진짜로 *추가*된다(승인약이 있으면 키트는 sanity check 일 뿐 — 한계가치 낮음).
  - 산출물: M10 출력에서 "no-approved-therapy ∧ high-burden" 후보 자동 surfacing.
  - **촉매적 open-directions 카드**(NEW, IV-A 와 연결): 꼬리 각 질병을 *가장 행동가능한* 한 장으로 —
    질병 → 축 → 강제 방향 → *후보 약물 클래스*(III-A2 재배치 스캐너 결과) → **가장 싼 반증 실험** →
    정직한 `[O]`/status. 이것을 공개 사이트의 *묻힌 트랙*이 아니라 **헤드라인**으로 — 연구자가 집어들도록
    활성화 에너지를 낮춘다.

- **III-A2 교차질환 재배치 스캐너** (same-axis repurposing) — **가장 높은 레버리지(NEW 모듈)**.
  - 무엇: 키트의 *같은-축·같은-방향·같은-lever-클래스* 구조를 이용해 질병쌍을 자동 surfacing —
    질병 X(승인약 *없음*)가 질병 Y(승인약 Z *있음*)와 동일 축-교란 서명(emergent_axis-family × 교정 방향 ×
    lever 클래스)을 공유하면 → **"Z 의 *기전 클래스*가 X 의 검증가능 방향 가설"**. 희귀병 신약의 가장 싼 길 =
    재배치. *맨방향*이 아니라 바로 이것이 제약사·임상의를 움직이는 돌이다.
  - 산출물: 동결 `repurposing_hypotheses.json`(점수판, drift-0; direction_recovery 와 동형). 각 가설은
    (X, Y, 공유 축, Z 의 기전 클래스, falsifier) 튜플.
  - 방화벽(엄격): *기전 클래스 방향*만 — 결코 용량·효능·특정 제품 청구 아님. 모든 가설에 `[O]` +
    falsifier + **정직 주석**: "same-axis ≠ same-disease — X-고유 이유로 재배치는 실패할 수 있다"(가설이지
    예측이 아님). 자명한 동어반복(같은 질병군 내 이미 알려진 클래스)은 *낮은-신규성*으로 명시 강등.
  - 등급: 방향 `[F]`(공유 축 강제), 후보-클래스 매칭 `[F]`, 크기·재배치-성공확률 `[O]`.

- **III-B downgrade-and-disclose read**(HHT 형) — 고정보(자명하지 않은 다음 방향).
  - 스위치 논리와 임상이 갈리는 질병은 *간극을 드러내므로* 정보가 크다. 적극 식별.

- **III-C 능력-확장 축 / lever** (*방향의 종류*를 넓히는 것으로 프레이밍; 수집 아님).
  - 채널병증(롱QT KCNQ1/SCN5A, Dravet SCN1A, 주기성마비 SCN4A/CACNA1S), GPCR(신성요붕증 AVPR2/AQP2,
    상염색체우성 RP **RHO** = 망막 proteinopathy, CASR), DNA 복구(XP / 판코니 / AT = 게놈-유지 축),
    섬모병증(PCD / PKD / BBS), 콜라겐·결합조직(OI COL1A1, Marfan FBN1, EB). 대부분 switch-drug 부재 →
    HHT 식 downgrade 또는 `[O]`-heavy 정직 read.

- **III-D 새 SUSPEND 기전 부류** (규율 과시).
  - 취약X(FMR1 CGG 확장 → 프로모터 *메틸화 침묵*; FSHD 수축-탈억제의 정반대), 인접유전자결실(22q11),
    체세포 모자이크(Proteus AKT1, McCune-Albright GNAS = 비-생식계열), 2차 mtDNA(MELAS tRNA),
    2차 이수성(13 / 18).

### 기둥 IV — PUBLISH: 방향이 *행동할 수 있는 사람*에게 닿도록

- **IV-A 정본 HTML / AI-검색 ingestion** (VP-SPEC v1.8 §6-R: answer-first, 자기완결 절, JSON-LD, bot-접근).
  방향 신호가 연구자 · 임상 · 환자단체에 도달하는 경로.
- **IV-B DOI(완료) + 질병별 인용 가능 페이지**.
- **IV-C YMYL 규율** = 미검증 가설의 *무료 공개를 책임 있게* 만드는 것이 곧 방화벽.

### 기둥 V — INHERIT: 구조를 형제 패키지에서 상속 (multi-system intractable read)

> **구조를 모르면서 희귀병을 다루니 어렵다.** 키트는 단일유전자 *프로모터*는 읽지만, 그 병이 **건드리는
> 장기-계통의 구조**(측정된 γ, 구획, seam 축)는 형제 패키지가 이미 안다. 다계통 난치병은 그 구조를
> *상속*해 읽어야 더 멀리 간다 — 그것이 기둥 V 다.

- **V-A 형제 레지스트리**(`system_inheritance/sibling_registry.json`, 동결) — 13개 형제 organ-system
  패키지에서 **49개 organ-master γ**(예: 심장/NKX2-5/1.513, 신장/SIX2/1.5556, 췌장/PDX1/1.4732,
  골격근/MYOD1/1.4933, 망막/PAX6/1.511 …) + 2개 anchor(neuro: cns·pns, dna: organ-identity SSOT)를
  **그대로 벤더링**(재계산 금지 — 형제의 동결 값이 정본). 각 형제에 `owned_major_disease_EXCLUDED` 명시.

- **V-B 다계통 매니페스트**(`system_inheritance/multisystem_manifest.json`, 동결) — 키트 안에서 *이미
  RESOLVED 인* 다계통 난치병만 골라(보류 규칙 통과), 그 병이 건드리는 각 구획에 (형제, organ, γ-donor 또는
  anchor, *인용된* 이유)를 명시 + falsifier 동반. v0.30.0 = 8개 시연 질병(Fabry/GLA, Pompe/GAA,
  cystic fibrosis/CFTR, cystinosis/CTNS, tuberous sclerosis/TSC2, Bardet-Biedl/BBS1, Wilson/ATP7B,
  haemochromatosis/HFE).

- **V-C REACH/GAP 네이티브 모듈**(`pipeline/system_inheritance.py`, fail-closed·자기동결·방화벽) —
  각 질병마다 **PROVENANCE 핸드셰이크**(RESOLVED 확인, 매니페스트 causal_gene == 동결 primary_switch.gene,
  매니페스트 lever == 동결 lead lever, signature ⊂ 동결 agent_class, modality ∈ MODALITY_REACH)를 강제한
  뒤, 리드 치료 modality 가 *닿는* 구획(REACHED)과 *비껴가는* 구획(GAP)을 분할한다. **GAP = 자명하지 않은
  다음 치료 방향** — 예: ERT(Fabry) → 말초신경(pns) 미도달; cysteamine(cystinosis) → 각막 미도달;
  setmelanotide(Bardet-Biedl) → 망막·신장·사지골격 미도달. Wilson·haemochromatosis 는 *대조군*(전 구획
  도달). 출력 `system_inheritance_map.json` 동결.

- **V-D 배제 게이트**(VP_FRAMEWORK_MAP §6) — 키트가 손대는 질병이 형제의 `owned_major_disease_EXCLUDED`
  와 충돌하지 않음을 토큰-정규화 충돌 검사로 강제. "각 분야가 이미 다룬 주요질환은 제외, 다계통 *난치병*만"
  이라는 범위를 *기계적으로* 지킨다. 음성-치아(negative-teeth): 배제-주요질환을 일부러 주입하면 잡아낸다.

- **방화벽**(엄격) — 상속된 γ 는 REAL(형제 동결 값); 구획 매핑은 질병 자신의 동결 summary 에서 인용한
  `[F]`; **도달/비도달은 *방향*(정성적·인용된 biodistribution)일 뿐 — 교정의 *정도*는 항상 `[O]`**.
  교과서적으로 확실한 비도달(예: ERT 가 BBB 통과 못함)만 GAP 으로 단언. 같은 단위-바운드 magnitude regex 로
  게이트 → γ 소수·저널 인용("347:111")은 오탐 안 냄.

- **확장 패턴**: v0.30.0 8개는 **시연 세트**다 — "먼저 시연하고 굴려 나간다(demonstrate then roll out)".
  나머지 다계통 난치병은 후속 버전에서 매니페스트에 추가(절차는 `HANDOFF.md` §4 / `SYSTEM_INHERITANCE.md`).

---

## 3. 우선순위 — sequencing (next, in order). 한 릴리스 = 한 DOI 스냅샷.

1. ✅ **v0.23.0 — 능력 확장 1축(III-C): 채널병증 쌍 DONE.** 채널병증 1개(롱QT 또는 Dravet) 대신 **둘 다**
   추가 — `long_qt_syndrome_3`(SCN5A GOF, 첫 심장 이온채널 축, 첫 채널-GOF read, 첫 `restrain`-채널 lever:
   메실레틴) + `dravet_syndrome`(SCN1A LOF, 첫 신경 이온채널 축, 헌팅턴 패턴: zorevunersen 임상시험) — CFTR/K_ATP
   외 **두 가지 새 채널 lever 방향**을 연 전압개폐 Na 채널 **거울쌍**(심장 GOF↑/restrain ↔ 신경 LOF↓/replace,
   Wilson/Menkes 구리쌍의 채널 유사물). +1 보류(MELAS / mtDNA tRNA MT-TL1, 두 번째 mtDNA 보류 — 단백질코딩 →
   tRNA 유전자로 일반화). 엔진 변경 없음(둘 다 기존 lever 재사용 → 63개 기존 해시 drift 0; 66 total).
   *(이번 릴리스는 drift-0 질병추가에 집중 — II-A 방향-회수 점수판 모듈과 I-D `direction_confidence` 필드는
   엔진/스키마 변경이라 검증 중심 릴리스로 이연.)*
2. ✅ **v0.24.0 — 검증 등뼈(II-A) + 방향 신뢰도(I-D) + READ 최대화(I-A / I-B / I-F) DONE.**
   방향-회수 점수판을 키트 **최초의 네이티브 모듈** `pipeline/direction_recovery.py`(II-A)로 동결 —
   분산된 재도출 대신 단일 점수판이 질병별로 "엔진이 (역할×기전)에서 *강제한* 교정 방향"이 "독립 문헌이
   추구하는 선도 약제의 방향"과 일치하는지 채점: **61/61 방향 회수**(교정축 UP 36 / DOWN 25; 직접 34 / 간접 27;
   승인 52 / 임상 6 / 임상시험 3), **승인약-없는 고가치 꼬리 9개** 표면화(임상 6: 맥락막결손·HHT·헌팅턴·멘케스·
   RHO-adRP·XLRP; 임상시험 3: Dravet·MECP2중복·신성요붕증). `direction_confidence` 필드(I-D) 도입 —
   기본 `clean`(강제 역할×기전이 *구성상* 모호하지 않음), 레지스트리 필드로 `cited-contested`/`ambiguous` 재정의:
   3개 cited-contested(RHO-adRP 대립유전자 클래스; α1-항트립신 두-장기-반대-방향; Rett MECP2 양방향 용량민감) →
   58 clean / 3 cited-contested / 0 ambiguous. 둘 다 읽기전용 → 모든 analysis.json 해시 바이트동일(S2 전체 재생성
   으로 drift 0 확인). **+2 resolved**(RHO adRP / RHO — 네 번째 안과 read, 첫 안과 단백질병증, `reduce` QR-1123
   임상 미승인 = 헌팅턴 패턴; 신성요붕증 / AVPR2 — 첫 GPCR/cAMP 수용체-신호 축, `correct` 약리샤페론 임상시험
   미승인), **+1 보류**(Kearns-Sayre / 단일 거대 mtDNA 결실 — 세 번째 mtDNA 보류, 점돌연변이→구조적 재배열로
   일반화). 엔진 변경 없음(둘 다 기존 lever `reduce`/`correct` 재사용 → 66개 기존 해시 drift 0; **69 total**;
   모듈 3→4 재동결, drift 0).
3. ✅ **v0.25.0 — READ 추가(질병추가 릴리스): 안과 다섯 클래스 완성 + GPCR 양방향 완성 + 여섯 번째 보류 기전 DONE.**
   **+2 resolved**: `usher_syndrome_type_2a`(USH2A structural/LOF, axis DOWN — 다섯 번째 안과 read이자 **첫 증후군성
   (청-시각) read**, 한 망막에서 **다섯 분자기계 클래스 완성**[효소·수송·프레닐화·단백질병증·구조접착]; `correct`
   엑손-13-건너뛰기 ASO ultevursen/QR-421a, 임상 미승인 = 헌팅턴 패턴, 다섯 번째) + `nephrogenic_siad`(AVPR2
   accelerator/GOF, axis UP — **두 번째 GPCR 축**이자 v0.24.0 X-연관 NDI 의 **같은 AVPR2 locus 위 정확한 GOF 거울상**
   [동일 γ 1.4618·동일 건강 dwell 1.60672, 질병은 위 vs NDI 아래 — Rett/MECP2중복 용량거울 패턴을 GPCR 에서 실현];
   `restrain` vaptan tolvaptan **승인**·직접이나 유전자형 제한[Arg137 vaptan-저항]). **+1 보류**:
   `digeorge_22q11_2_deletion_syndrome`(22q11.2 인접유전자 미세결실 — **여섯 번째 보류 기전 부류**, 염색체-용량 보류를
   전염색체 이수성[다운, GAIN]→하위염색체 분절 LOSS 로 일반화). 엔진 변경 없음(둘 다 기존 lever `correct`/`restrain`
   재사용, 새 역할·기전·축·lever 없음 → 69개 기존 동결 해시 drift 0; **72 total per-disease + 4 module**; 캐시 94→98
   [USH2A, ADGRV1, WHRN, TBX1]). II-A 점수판 **63/63** 재실행(승인약-없는 꼬리 10), I-D 60 clean / 3 cited-contested /
   0 ambiguous; 각 lead 출시 전 웹 검증.
4. ✅ **v0.26.0 — READ 추가(질병추가 릴리스): 첫 응고-FACTOR GOF + 두 번째 증후군성 섬모병증 + 일곱 번째 보류 기전 DONE.**
   **+2 resolved**: `factor_v_leiden`(F5 accelerator/GOF, axis UP — 키트 **첫 응고-FACTOR 기능획득**이자
   antithrombin/SERPINC1 브레이크-소실의 **같은 응고축 위 정확한 가속자-GOF 거울상**; R506Q 가 첫 APC 절단부위 제거 →
   APC-저항 factor Va → `restrain` 한 단계 하류 **승인 DOAC**[apixaban/rivaroxaban/dabigatran, 또는 warfarin], VTE
   적응증 **승인·온라벨**이나 F5 에 **간접** = LEPR 패턴) + `bardet_biedl_syndrome`(BBS1 accelerator/LOF, axis DOWN —
   USH2A 에 이은 **두 번째 증후군성 섬모병증**, 한 BBSome-소단위 병변을 비만+망막+신장 가로질러 read; `potentiate`
   MC4R 작용제 **setmelanotide/Imcivree**[2022-04 FDA 승인, BBS 비만 전용], **승인**이나 BBSome 우회 = **간접**, 비만
   arm 한정). **+1 보류**: `fragile_x_syndrome`(FMR1 — **일곱 번째 보류 기전 부류**, 반복-팽창 구동 프로모터 CpG-메틸화
   침묵; CGG 5'-UTR 팽창>200 → CpG섬 과메틸화 → FMR1 침묵 → FMRP 소실; FSHD 수축-탈억제 보류의 **정확한 거울상**
   [같은 반복/후성 축, 반대 방향]이자 헌팅턴과 **같은-병변-부류 대조**[CGG 프로모터-침묵 보류 vs CAG 코딩-독성 해결];
   FMR1 프로모터는 참조 DNA 로 완벽히 읽힘[γ 1.4563, 패널 최고 CpG 밀도 0.0508]이나 메틸화/반복길이 병변이 엔진에
   불가시 — 치료 부재가 아닌 **엔진-가독성** 으로 보류). 엔진 변경 없음(둘 다 기존 lever `restrain`/`potentiate`
   재사용, 새 역할·기전·축·lever 없음 → 72개 기존 동결 해시 drift 0; **75 total per-disease + 4 module**; 캐시 98→105
   [F5, F2, PROC, BBS1, BBS10, MC4R, FMR1]). 두 resolved lead 모두 **승인-그러나-간접** → 간접-lever 인구조사 55→57.
   II-A 점수판 **65/65** 재실행(승인약-없는 꼬리 10 불변, 승인 55), I-D 62 clean / 3 cited-contested / 0 ambiguous;
   각 lead 출시 전 웹 검증.
5. ✅ **v0.27.0 — READ 추가(질병추가) + 환자 면책 인프라 DONE.** 로드맵이 제안한 세 슬롯 중 둘을 그대로,
   하나는 정직히 대체해 출시: **+2 resolved** — `atypical_hemolytic_uremic_syndrome`(CFH 브레이크-소실, axis UP —
   키트 **첫 보체-연쇄** read, `restrain` 승인 항-C5 **eculizumab/ravulizumab** 하류 작용 = 응고 read 와 유사한
   간접 연쇄-lever, 응고와 구별되는 새 연쇄축; γ 1.2845 chr1) + `mucopolysaccharidosis_type_i`(IDUA 효소-LOF,
   axis DOWN — **아홉 번째 리소좀** read이자 **첫 글리코사미노글리칸 기질**, `replace` 승인 ERT **laronidase** 직접,
   단 BBB 미통과 → 중증 Hurler CNS 미해결 `[O]`; γ 1.4522 chr4). *제안된 TTR-안정자 슬롯은 트랜스티레틴
   아밀로이드증이 이미 resolved 이므로 MPS I 로 대체* — 새 기질 클래스가 더 큰 한계가치. **+1 보류**:
   `mccune_albright_syndrome`(GNAS — **여덟 번째 보류 기전 부류** = 접합후 **체세포 모자이시즘**, 활성화 병변이
   유전된 참조 서열에 없음; 생식계열 프로모터는 읽히나[γ 1.4256 chr20] 비-유전·체성 병변은 불가독 → '유전 서열에
   없음'으로 보류, 치료 부재 아님). 엔진 변경 없음(둘 다 기존 lever `restrain`/`replace` 재사용 → 75개 기존 동결
   해시 drift 0; **78 total per-disease + 4 module**; 캐시 105→112). II-A 점수판 **67/67**(승인약-없는 꼬리 10 불변,
   승인 57), 간접 census 57→58(aHUS), I-D 64 clean / 3 cited-contested / 0 ambiguous. **추가: 환자용 시뮬레이션
   면책 인프라**(저자 지시) — `pipeline/disclaimer_banner.py`(단일진실원천, 한·영 배너: "DNA 창발 컴퓨터
   시뮬레이션, 현실과 다를 수 있음 · 의료조언 아님 · 방향만·크기 `[O]` · 새 치료 발견 아님 · Orphanet/NORD/
   GeneReviews 안내") + `pipeline/explain_disease.py`(사람-대면 출력 시 배너를 *맨 위·설명 전에* 강제) — 읽기전용,
   해시 불변; Constitution + §5 구속 규정. *(III-A surfacing · IV-A HTML 헤드라인은 v0.28.0 으로 이연.)*

6. ✅ **v0.28.0 — 촉매 미션 구현(III-A2 + III-A 카드 + IV-A 헤드라인): "연못의 돌"을 *행동가능*하게. — DONE (SHIPPED & GREEN).**
   이 릴리스는 *질병 수집*이 아니라 **잠재 가치를 실제로 행사**하는 데 집중했다(§0 텔로스). 질병·엔진 변경 없음,
   `analysis.json` 무수정 → **78개 per-disease 해시 drift 0**; 모듈 동결 4→6, **새 세 번째 site 동결(4 파일)**.
   - ✅ **(a) III-A2 재배치 스캐너**(`pipeline/repurposing_scanner.py`): MOLECULAR CORRECTIVE-AXIS 수준의 curated
     `axis_family` 분류(39 families, 미분류 resolved 있으면 **gate FAIL-CLOSED**)로 (axis_family × 방향 × lever_class)
     버킷마다 "승인약-없는 RECIPIENT ↔ 승인약-보유 DONOR(동일 서명)" 가설 surfacing → **4 가설(2 families) + 6 orphans**
     (장부 정합: 4 ∪ 6 = 승인약-없는 꼬리 10): retinal_gene_replacement|UP|replace {choroideremia ← LCA2/voretigene;
     XLRP ← LCA2}; toxic_gof_protein|UP|reduce {huntington ← SOD1-ALS/tofersen + TTR; RHO-adRP ← SOD1-ALS + TTR}; orphans
     {dravet, HHT, mecp2-dup, menkes, X-linked NDI, usher-2a}. **두 가설군 모두 정직하게 저-신규성(CONFIRMATORY)** —
     recipient 가 이미 그 클래스를 추구 중 → 알려진 방향을 복원하는 것이고, 이것이 매칭 논리를 **검증(VALIDATE)** 한다(과대
     주장이 아님). 동결 `repurposing_hypotheses.json` b840a499f8e8, self-test 有齒.
   - ✅ **(b) III-A 촉매 open-directions 카드**(`pipeline/open_directions_card.py`): 꼬리를 **10장**(4 repurposing-candidate
     + 6 orphan)으로 — 동결 스캐너 분할 + 각 질병의 동결 corrective-방향 falsifier(`measurable_by` = 가장 싼 반증 실험,
     **날조 없음**)만 읽는다; repurposing 카드는 donor-귀속 후보 클래스 부착("subretinal AAV gene replacement";
     "SOD1-lowering ASO" + "TTR-lowering siRNA/ASO"), orphan 카드는 정직하게 클래스 없음; 행동가능 == 반증가능. 동결
     `open_directions_cards.json` 61c29db81807.
   - ✅ **(c) IV-A 정본 HTML 사이트**(`pipeline/build_site.py`): 동결 JSON + VERSION 메타(시계 안 읽음 → byte-identical
     재빌드)만 읽어 `site/` 4파일 — `index.html`(면책 배너가 *첫 `<body>` 요소*; answer-first `<p class="answer">` 40-60
     단어[=54]; **꼬리·재배치 두 테이블이 헤드라인**; method/firewall 절; JSON-LD @graph = WebSite + Person[ORCID, sameAs
     DOI] + Dataset + 2× Claim/Rating[O]), `sitemap.xml`, `robots.txt`(STAGING `Disallow: /` + 7개 검색봇 production
     allow-list 주석), `llms.txt`(<5 KB[=1753 B]). 페이지 방화벽 = NUMERIC-MAGNITUDE 패턴 게이트(키워드 금지 아님) →
     면책 문구·질병 수가 오탐을 안 낸다. site self-test = 두 in-process 빌드가 BYTE-IDENTICAL. 동결 site 해시 4개.
   - ✅ **(보강) M5v2 claim-scanner**: scope 3 → 5 모듈, DOSING 패턴 경화(bare dose/dosage 제거 — "gene dosage"/
     "dose-response window" 정당 생물학에 오탐; 정량형 `\d mg`·mg/kg·twice daily 등만 발화) → **더 정확**(약화 아님);
     심은 self-test 여전히 ≥3 클래스 발화; `analysis.json` 무수정 → 78 해시 drift 0. claim_scan_v2 f4019841bab2.
   - ⏸ **(d, 이연) READ 추가는 꼬리-적합 질병 우선**: 선택적 구성요소였고 v0.29.0 의 자연스러운 첫 과제로 이연 —
     웹 검증한 새 승인약-없는-꼬리 단일유전자 희귀병을 추가하면 스캐너 재실행 시 다섯째 가설/일곱째 orphan 이 surfacing.

7. ✅ **v0.29.0 → 출하 v0.31.0 — 질병 추가 릴리스 DONE (SHIPPED & GREEN).** 추가 후 재배치 스캐너 재실행 완료.
   실현: **+1 RESOLVED metachromatic_leukodystrophy/ARSA**(첫 백질이영양증·첫 sulfatide 기질; 효소/LOF → 리소좀
   sulfatide-이화 축 DOWN → 리드 `replace` = 승인 ex-vivo HSC 유전자치료 atidarsagene autotemcel, 인과 ARSA 에
   DIRECT; **승인이나 결정적 한계는 크기 아닌 TIMING** — 발현전/초기증상 환자 전용, 효과 정도 [O]; `lysosomal_enzyme_replacement`
   축-family, 티어 B3/U4/D4 = X-ALD 백질이영양증/HSC-유전자치료 형제 형태) **+ 1 SUSPENDED myotonic_dystrophy_type_1/DMPK**
   (**아홉 번째 보류 기전 클래스**: repeat-EXPANSION 독성-RNA GOF/spliceopathy — 3′-UTR CTG 확장 → 핵 CUG-foci 가 MBNL1/2
   격리 → TRANS spliceopathy; DMPK 프로모터 SEQUENCE 변화 아님, γ 1.5132 가독; 삼핵산-반복 분류를 운명별로 완성:
   Huntington[CAG coding→독성 단백, RESOLVED]/fragile X[CGG 5′-UTR→메틸화 침묵, 보류]/DM1[CTG 3′-UTR→독성 RNA, 보류]).
   78 → 80 per-disease(68 resolved + 12 suspended) drift 0; **S5 재동결**(direction-recovery 67/67→68/68, 승인 57→58,
   무승인 꼬리 10 불변; indirect 카운트 58 불변 — MLD 리드 DIRECT; MLD 를 `lysosomal_enzyme_replacement` 로 분류);
   `open_directions_cards`·`claim_scan_v2` 불변(MLD 는 승인-치료 DONOR — 꼬리-recipient 도 orphan 도 아님); 사이트 재동결
   (corpus 67→68); system-inheritance 해시 불변. 캐시 112→114(ARSA, DMPK). ledger B33 + §C(DM1 9번째 + McCune-Albright
   8번째 백필). 각 리드 출하 전 웹 검증. **다음 disease-adding 슬롯**: 열 번째 보류 클래스 후보 등 — 웹 검증 후 슬롯 확정.

   (원래 계획·이월 후보, 기록용:) 기존 규율 유지(리드 승인상태 웹 검증 BEFORE 출하; 가능하면 엔진 불변 → 기존 해시 drift 0; 단일 읽기 가능
   핵-프로모터 스위치 없으면 정직 보류). **새 규율: 질병 추가 후 III-A2 스캐너 + III-A 카드 재실행** — 새 승인약-없는
   RECIPIENT 또는 새 승인약 DONOR 가 가설/orphan 을 만들거나 닫을 수 있고, fail-closed `axis_family` 게이트가 새
   resolved 질병의 분자-교정축 family 분류(기존 또는 신규)를 **강제**한다. 후보 방향(v0.27.0 슬레이트에서 이월,
   일부 출하됨): 이미 캐시된 **TTR** 위 **첫 systemic proteinopathy-STABILISER** 축(유전성 TTR 아밀로이드 — 불안정화
   GOF → 응집 축 UP → 안정화, 리드 승인 tetramer-안정제 **tafamidis** / silencer **patisiran/vutrisiran**; 주의: 이는
   기존 `toxic_gof_protein|UP|reduce` 재배치 family 의 DONOR 가 되어 huntington/RHO-adRP 가설을 **강화**할 수 있음);
   보류 측은 8개 등재 클래스(aneuploidy / imprinting / repeat-CONTRACTION / mtDNA / contiguous-gene-microdeletion /
   repeat-EXPANSION-methylation-silencing / post-zygotic somatic mosaicism)와 진짜로 구별되는 **NINTH** 클래스 후보.
   정확한 슬롯은 웹 검증 후 확정, 새 resolved 마다 (B,U,D) 티어 + falsifier.

각 단계: 기존 해시 drift 0, 추가 시 S5 재동결, 새 resolved 마다 (B,U,D) 티어 + falsifier, 보류 시 §C.
질병 추가법의 절차는 `HANDOFF.md` §3.

8. ✅ **v0.30.0 — system-inheritance(기둥 V) DONE.** 질병·엔진 변경 **없이**(78 per-disease + 6 module + 4 site
   해시 전부 drift 0), 형제 organ-system 패키지에서 **구조를 상속**하는 읽기-전용 레이어를 추가 — "구조를 모르고
   희귀병 다루기 어렵다"는 통찰의 구현. (V-A) 13개 형제에서 **49 organ-master γ** + 2 anchor 를 동결 벤더링한
   `sibling_registry.json`; (V-B) 키트 내 *이미 RESOLVED 인* 다계통 난치병 8개를 인용된 이유·falsifier 와 함께
   매핑한 `multisystem_manifest.json`; (V-C) PROVENANCE 핸드셰이크(causal_gene/lever/agent_class/modality 동결
   대조) 후 리드 modality 의 **REACH vs GAP** 를 분할하는 네이티브 모듈 `pipeline/system_inheritance.py`
   (fail-closed·자기동결·방화벽) — **GAP = 자명하지 않은 다음 치료 방향**(ERT→말초신경, cysteamine→각막,
   setmelanotide→망막·신장·사지; Wilson·haemochromatosis 는 전-구획 도달 대조군); (V-D) VP_FRAMEWORK_MAP §6
   **배제 게이트**로 "각 분야 이미-다룬 주요질환 제외, 다계통 *난치병*만" 범위를 토큰-정규화 충돌검사로 기계 강제.
   인구조사: 8 질병 · 31 상속 링크 · 27 γ-시스템 · 26 도달 · 5 GAP. 방화벽: 상속 γ 는 REAL, 구획맵 `[F]` 인용,
   도달/비도달은 *방향*뿐 — 교정 정도는 항상 `[O]`. 새 harness **S6** + 동결
   `repro/expected_system_inheritance_sha256.json`(map d734d3dbdc8e, byte-identical 재빌드). 음성-치아 4종(나쁜
   signature·나쁜 gene 거부, 주입된 배제-주요질환 포착, reach 스팟체크). 8개는 **시연 세트**(demonstrate then
   roll out) — 나머지 다계통 난치병은 후속 매니페스트 추가. 개념 DOI·캐시 불변.

---

## 4. 절대 하지 않을 것 — non-goals (실재 한계, by constitution)

- 용량 · 요법 · 경로 · 합성 · 제형 — 영원히 금지.
- 효능 / 안전 / 역가 / PK 주장 금지. 방향만; 크기 `[O]`.
- DNA 가 단일유전자 스위치가 아니면 강제 read 금지 — 보류.
- 목표 적중 튜닝 금지; 사유 없는 비재현 수치 금지.
- 개인 의료조언 금지.

---

## 5. 지금까지 — done to date

전체 변경 이력의 정본(SSOT)은 **`VERSION`** 의 changelog. 요약(v0.26.0): **65 resolved + 10 suspended**;
**7가지 보류 기전 부류**(이수성 · 임프린팅 · 반복-탈억제 · 미토콘드리아 게놈[mtDNA 클래스가 점돌연변이
(LHON 단백질코딩 / MELAS tRNA)→구조적 결실(Kearns-Sayre)로 클래스내 일반화] · **인접유전자 미세결실**[22q11.2 —
염색체-용량 보류를 전염색체 이수성→하위염색체 분절 LOSS 로 일반화] · **반복-팽창 프로모터 메틸화 침묵**[Fragile X /
FMR1 — CGG 5'-UTR 팽창>200 → CpG섬 과메틸화 → FMR1 침묵; FSHD 수축-탈억제의 정확한 거울상, 헌팅턴 CAG 코딩-독성과
같은-병변-부류 대조; 프로모터는 읽히나 메틸화/반복길이 병변이 불가시 — 엔진-가독성 보류]); **6개 2-원인유전자 수렴**;
**첫 채널병증 쌍**(SCN5A GOF / SCN1A LOF 전압개폐 Na 채널 거울쌍); **첫 응고-FACTOR 기능획득**(factor V Leiden /
F5 — antithrombin/SERPINC1 브레이크-소실의 같은 응고축 위 가속자-GOF 거울상, `restrain` 승인 DOAC 간접 lever);
**다섯 개 안과 read**(망막순환효소·섬모수송·Rab프레닐화·안과단백질병증·**구조접착** — 한 망막 다섯 분자기계 클래스
완성, USH2A 가 **첫 증후군성 청-시각 read**); **두 증후군성 섬모병증**(USH2A ↔ Bardet-Biedl/BBS1 — BBSome
수송실패를 비만+망막+신장 가로질러 read, `potentiate` setmelanotide 간접 lever); **GPCR/
수용체-cAMP 신호 축을 양방향 완성**(AVPR2 — NDI LOF↓ `correct` 약리샤페론 ↔ NSIAD GOF↑ `restrain` vaptan,
같은 locus 위 Rett/MECP2중복 용량거울 패턴); 그리고 키트 **최초의 네이티브 모듈** — II-A 방향-회수 점수판
(**65/65 방향 회수**, 승인약-없는 꼬리 10개, 간접-lever 인구조사 57) + I-D `direction_confidence`(62 clean /
3 cited-contested / 0 ambiguous); drift 0; 개념 DOI 등록. 이 로드맵은 v0.22.0 기준 *재설계*다 — changelog 복제 대신 설계에 집중한다.

**v0.28.0(촉매 미션, §3.6 DONE)** — 질병·엔진 변경 없이 **연못의 돌을 행동가능**하게: (III-A2) 분자-교정축 `axis_family`
(39 families, fail-closed) 위 **교차질병 재배치 스캐너**(4 가설 + 6 orphan = 승인약-없는 꼬리 10 정합; 두 가설군 모두 정직한
저-신규성/CONFIRMATORY → 매칭 논리 검증), (III-A) **open-directions 카드 10장**(4 후보 + 6 orphan, 각자 동결 falsifier =
가장 싼 반증 실험), (IV-A) 키트 첫 **정본 retrieval-ready HTML 사이트**(배너-first · answer-first · JSON-LD · staging
robots · llms.txt <5 KB; 동결 JSON+VERSION 에서 byte-identical 재빌드). M5v2 scope 3→5 + DOSING 경화(더 정확). 78
per-disease drift 0; 모듈 4→6; 새 site 동결 4파일. 개념 DOI·캐시(112) 불변.

**v0.30.0(system-inheritance, 기둥 V·§3.8 DONE)** — 질병·엔진 변경 **없이**(78 per-disease + 6 module + 4 site 해시
전부 drift 0) 형제 organ-system 패키지에서 **구조를 상속**하는 읽기-전용 레이어: (V-A) 13개 형제의 **49 organ-master γ**
+ 2 anchor 를 동결 벤더링(`sibling_registry.json`, 재계산 금지 — 형제 동결 값이 정본), (V-B) 키트 내 *이미 RESOLVED 인*
다계통 난치병 8개를 인용 이유·falsifier 와 함께 매핑(`multisystem_manifest.json` — Fabry/Pompe/CF/cystinosis/TSC/
Bardet-Biedl/Wilson/haemochromatosis), (V-C) PROVENANCE 핸드셰이크(causal_gene·lever·agent_class·modality 를 동결
artifact 와 대조) 후 리드 modality 의 **REACH vs GAP** 를 분할하는 네이티브 모듈(`pipeline/system_inheritance.py`,
fail-closed·자기동결·방화벽) — **GAP = 자명하지 않은 다음 치료 방향**(ERT→말초신경, cysteamine→각막, setmelanotide→
망막·신장·사지골격; Wilson·haemochromatosis 전-구획 도달 대조군), (V-D) VP_FRAMEWORK_MAP §6 **배제 게이트**로 "각 분야
이미-다룬 주요질환 제외, 다계통 *난치병*만" 범위를 토큰-정규화 충돌검사로 기계 강제. 인구조사 8 질병·31 상속 링크·27 γ-시스템·
26 도달·5 GAP. 방화벽: 상속 γ 는 REAL, 구획맵 `[F]` 인용, 도달/비도달은 *방향*뿐(교정 정도 항상 `[O]`). 새 harness **S6** +
동결 `expected_system_inheritance_sha256.json`(map d734d3dbdc8e, byte-identical 재빌드), 음성-치아 4종. 8개는 **시연
세트**(demonstrate then roll out). 개념 DOI·캐시 불변.

**v0.31.0(질병 추가, §3.7 슬롯 DONE)** — +1 RESOLVED **metachromatic_leukodystrophy/ARSA**(키트 첫 백질이영양증·첫
sulfatide 기질; 효소/LOF → 리소좀 sulfatide-이화 축 DOWN → 리드 `replace` = 승인 ex-vivo HSC 유전자치료
**atidarsagene autotemcel**, 인과 ARSA 에 DIRECT; **승인이나 결정적 한계는 크기 아닌 TIMING** — 발현전/초기증상 전용,
효과 정도 `[O]`; `lysosomal_enzyme_replacement` 축-family — *교정 생화학*이지 HSC *전달방식*이 아니므로 Gaucher/Fabry/
Pompe/MPS-I 와 함께, 버든-티어 형제 X-ALD[`peroxisomal_substrate_load`]와는 분리; 티어 B3/U4/D4), +1 SUSPENDED
**myotonic_dystrophy_type_1/DMPK**(**아홉 번째 보류 기전 클래스**: repeat-EXPANSION 독성-RNA GOF/spliceopathy — 3′-UTR
CTG 확장 → 핵 CUG-foci 가 MBNL1/2 격리 → TRANS spliceopathy[CLCN1/INSR/SCN5A]; DMPK 프로모터 SEQUENCE 변화 아님,
γ 1.5132 가독이나 3′-UTR 반복-길이·trans 독성-RNA 는 비가독; 삼핵산-반복 분류를 *운명*별로 완성 —
Huntington[CAG coding→독성 단백, RESOLVED]/fragile X[CGG 5′-UTR→메틸화 침묵, 보류]/DM1[CTG 3′-UTR→독성 RNA in trans,
보류]). 엔진 변경 **없음**(리드는 기존 `replace` 재사용) → 78 prior per-disease drift 0; 78 → **80**(68 resolved +
12 suspended) + 6 module + 4 site + 1 system-inheritance 해시. **S5 재동결**(direction-recovery 67/67→68/68, 승인
57→58, 무승인 꼬리 10 불변; indirect 카운트 **58 불변** — MLD 리드 DIRECT; MLD 를 `lysosomal_enzyme_replacement` 분류);
`open_directions_cards`·`claim_scan_v2` **불변**(MLD 는 승인-치료 DONOR — 꼬리-recipient 도 orphan 도 아님 → 카드/거짓-
주장 스캔 무영향). 사이트 재동결(corpus 67→68 resolved); system-inheritance 해시 불변(MLD 단일계통; DM1 보류 — 둘 다
다계통 manifest 비진입). 캐시 **112→114**(ARSA 1.4806 chr22, DMPK 1.5132 chr19). ledger **B33** + §C(DM1 9번째 클래스
+ McCune-Albright 8번째 클래스 백필 — 기존 §C 표 공백 보정). 각 리드 출하 전 웹 검증. 개념 DOI 불변.

**v0.32.0(질병 추가 DONE)** — +4 RESOLVED, +1 SUSPENDED, 엔진 변경 **없음**(리드 전부 기존 레버 `restrain`×2/`replace`×2)
→ 80 prior per-disease drift 0; 80 → **85**(72 resolved + 13 suspended). 각 리드 출하 전 웹 검증.
(A) **scn4a_skeletal_muscle_channelopathy/SCN4A** — 키트 **첫 골격근 이온채널**, **LQT3(SCN5A)의 골격근 쌍둥이**(동일 생물물리
— 불활성화 장애로 인한 지속 후기 Na 전류; 같은 약!): 채널/GOF → 막흥분성 축 **UP** → 리드 `restrain` = **mexiletine**
(class-IB Na-채널 차단제, **첫 질병특이 승인 항근긴장제** NaMuscla EMA 2018; 3상 MYOMEX) + 간접 arm **dichlorphenamide**
(Keveyis FDA 2015, CAI — 산-염기/K⁺ 경유, NaV1.4 비작용); genotype-의존 크기 `[O]`; γ 1.5187 chr17; `skeletal_muscle_sodium_channel`; B2/U3/D4.
(B) **neonatal_severe_hyperparathyroidism/CASR** — **첫 칼슘감지-GPCR 축**(AVPR2 물-GPCR 축과 구별): CaSR=PTH 억제 브레이크,
브레이크/LOF → PTH/혈청-Ca 축 **UP** → 리드 `restrain` = 잔여 수용체를 **potentiate** 하는 calcimimetic **cinacalcet**(DIRECT
CaSR 알로스테릭), 관련 부갑상선항진증에 승인·off-label, **genotype-의존**(진성 null → 부갑상선절제=물리적 대안); γ 1.3299 chr3;
`calcium_sensing_gpcr`; B2/U3/D4.
(C) **biotinidase_deficiency/BTD** — 코팩터 **재활용** 효소/LOF: 유리 biotin 풀 DOWN → 4개 카르복실화효소 미충전(축 **DOWN**)
→ 가장 단순한 `replace`: **경구 biotin** 이 풀을 채워 재충전, 재활용 결함 우회; 가장 **치료가능한** 선천대사질환(신생아 선별,
저렴, 증상전 정상 경과), TIMING-제한(기성립 난청/시신경위축 비가역); γ 1.3560 chr3; `cofactor_recycling_replacement`; B2/U2/D5.
(D) **primary_carnitine_deficiency/SLC22A5** — 능동 카르니틴 **수입체**(accelerator)/LOF: 세포 카르니틴 고갈 → 장쇄 지방산
산화 붕괴(축 **DOWN**) → 질량작용 `replace` = 고용량 **levocarnitine**(Carnitor FDA 승인), 조기 시작 시 심근증 **가역**; γ 1.3724
chr5; `carnitine_transport_replacement`; B2/U2/D5.
(E) **charcot_marie_tooth_1a/PMP22** — **열 번째 보류 기전 클래스**, **첫 카피수 GAIN / 유전자-중복-용량** 보류: ~1.4-Mb
17p11.2 직렬 **중복**이 PMP22 3번째 카피 → **용량과다** 과발현 → **가장 흔한 유전성 신경병증**. PMP22 프로모터 SEQUENCE 는
완벽 가독(γ 1.3883 chr17)·**비변이** — 병변은 **카피수 GAIN**, 엔진은 locus당 프로모터 1개 γ 만 읽고 카피수 표현 없음 →
용량 중복 비가독. 9개 기존 클래스와 구별; **HNPP 의 거울상**(같은 영역 결실 → 반수체부족), 전형적 '유전자 용량' 질환(3카피
→ CMT1A; 1 → HNPP; 2 → 정상). 가독성 **때문에만** 보류(치료 부재 아님 — 승인 질병조절약 없음, 보조·보조기·수술=물리적 경로;
PMP22-저하 PXT3003 3상 완료, ASO/유전자편집 연구중). 프리즈 부기(표준): S4 5개 신규 해시 자동추가(80→85, 80 불변); **S5
재동결**(direction-recovery 68/68→72/72, 승인 58→62, 꼬리 10 불변; indirect **58 불변**; 4개 신규 = singleton 축-family → 재배치
가설/orphan/꼬리 불변, axis_family 게이트 72개 분류 0 누락); 사이트 재동결(corpus 68→72); system-inheritance 불변. 캐시
**114→120**(SCN4A/CASR/BTD/SLC22A5/CLCN1/PMP22). ledger **B34** + §C(CMT1A 10번째 클래스). 개념 DOI 불변.
