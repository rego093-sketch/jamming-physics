# HANDOVER — homeostasis_ionic_vp_site  ·  → v0.8.0 (3-레버 치료 조직화 원리; 개념 DOI 배선 완료)

**상태:** v0.8.0 · 연구 **COMPLETE (all gates green)** · `PHASE=writing` · 정본 `docs/` **빌드 완료**(16 섹션).
다음 세션 우선순위: **(1) cross_volume_doi 레지스트리 등록**(형제 볼륨과 함께) · (2) 사이트 루트 공유 후 seam 교차링크. **개념 DOI `10.5281/zenodo.20755910` 발행·배선 완료**(JSON-LD identifier/sameAs · claim-strip · footer · llms.txt), 교차볼륨 인용 = 진통제 DOI `10.5281/zenodo.20733420`. **Tier 로드맵 + 치료 조직화 층 모두 완결됨**(아래 §0).
(Tier-1 종간 축 v0.5.0 · Tier-2 질병 확장 v0.6.0 · Tier-3 분자 동역학+종별 γ v0.7.0 · **3-레버 치료 원리 v0.8.0** = 모두 완료.)

부트스트랩: `START_HERE.md` → 이 문서 → `CHARTER.md` → **`REMEDIATION_PLAN.md`**(보완 로드맵) → `IRREPRODUCIBILITY_LEDGER.md`.

---

## 0. 이번 세션(v0.8.0)이 한 일 — 3-레버 치료 조직화 원리 (교차볼륨 상속 + 소유 질병 개선책)

Tier 로드맵 완결 위에 얹은 **새로운 층**. 진통제 볼륨(개념 DOI `10.5281/zenodo.20733420`)의 **치료 조직화 기술을 상속**받아 이 권의
DNA-근거 루프 위에서 증명. 이미 측정된 마스터 유전자 γ 5개(RUNX2 1.2414 · CASR 1.3299 · VDR 1.4243 · GCM2 1.4642 · SIX2 1.5556;
NCBI + SantaLucia 1998; **fitting 없음**) → 장벽 b=γ²/4 → 루프게인 k 위에서 레버가 읽힘. **간이 시뮬이 아니라 측정 γ 사슬에 근거한
치료 프레임**. 가산적 — 연구 게이트 sha(`35d31461…`) 불변, 엔진 트리 byte-identical.

- **3-레버 원리** (`repro/_therapy/three_lever.py`, NEW): 방어 셋포인트 dx/dt=−k(x−x*)+load+noise 는 정확히 3개의 독립 핸들 —
  **L1** load(소스) · **L2** 루프게인 k(게인) · **L3** 목표 x*(셋포인트). 이 권 자체의 OU 법칙에서 재현한 **비대칭 정리**:
  *분산 σ²/2k 를 좁히는 것은 오직 L2* (L1은 평균만 낮춤; L3는 방어값을 지속적으로 이동) [V]. **L2 게인 천장 = 측정-γ 장벽 b=γ²/4**
  (γ에 단조; 최심 SIX2, 최천 RUNX2) — 가장 강력한 레버가 창발된 게놈에서 여유분을 상속 [V]. 27개 비-오피오이드 진통 타깃이
  L1/L2/L3에 1:1 사상 [L] (양 볼륨이 같은 R19 역치 객체, 두 부위). **크로스워크:** 이 권에 이미 유도된 모든 치료가 정확히 한 레버로
  재독해 — 셋포인트 리셋(칼시미메틱/칼실리틱, 지속 센서 리셋)=**L3**; 저장고 재충전(애나볼릭>항흡수), 이중항체 창, 신장 HCO₃ arm
  복원=**L2**(분산을 좁히는 결과들); otoconia/결석-spinodal/구동원 제거=**L1**. 전부 라이브 검증 [V].
- **질병 개선책** (`repro/_therapy/disease_remediation.py`, NEW): **소유** 질병 9종 각각 **손상된 OU 파라미터에서 1차 레버를 선택**,
  OU 법칙으로 시연, 인용·정직등급 개선책으로 전환. 차별적 처방: 골다공증 **애나볼릭-우선**(drain 잠그기 전에 게인 재충전: 테리파라타이드/
  아발로파라타이드/로모소주맙 → 그 다음 비스포스포네이트/데노수맙); 부갑상선기능항진증 & ADH1 = **셋포인트 리셋**(시나칼셋 down /
  엔칼레렛 up); CKD-MBD = **다중-arm 실패 → 3레버 동시**; 칼슘 결석 = **고정 역치 질병이라 L2 적용 불가**(L1 가용 basin 유지 + L3 곱
  셋포인트 하향). 소유 = 흔한/다인자/후천성/노화성 루프 질환; 희귀·단일유전자 → disease_wp(인용), 발암 암 → 기계 볼륨;
  **VP_FRAMEWORK_MAP §6 경계 불침범**.
- **배선:** `run_all.py` 섹션 **[15] THREE-LEVER PRINCIPLE · [16] DISEASE REMEDIATION** 추가(GATES → **[17]**) ·
  `literature_anchors.py` **A-3LEVER · A-ANALGESIC** 2개 anchor + 1개 INTERACTION(진통제 DOI 참조) ·
  `build_docs.py` `_research()`에 TL/DR 추가, 개념 DOI 배선(TBD→`10.5281/zenodo.20755910`), **§14·§15·§16** 페이지.
- **검증:** 연구 게이트 sha `35d31461…` **불변**(all_green, 결정론 2× sha256 동일) · 두 치료 모듈은 `vp_loops`/기존 모듈만 import,
  게이트 미급전 · docs 13섹션 → **16섹션** · 신규 [O] 항목 **없음**(두 모듈 모두 기존 OU 법칙 재사용; 절대 임상 크기는 종전대로 [O]/[H]).

---

## 0a. 직전 세션(v0.7.0)이 한 일 — Tier-3 (G5·G6 닫음, "모두 커버" 완결)

사용자 감사의 마지막 두 미결(분자 수송 **동역학** G5 · 종별 마스터 유전자 **γ** G6)을 닫아 Tier 로드맵을 완결. 두 증분 모두 **가산적** —
연구 게이트 sha(`35d31461…`) 불변, docs는 byte-identical 재빌드.

- **G5 분자 수송 동역학** (`repro/_engine/transport_dynamics.py`, NEW): 새 **FORCED** 프리미티브 — 게이팅된 채널의
  **GHK 정전장 플럭스**(Nernst에서 반전·정류) + Boltzmann/Hill 게이팅. 핵심 결과는 **연결**: 셋포인트에서 막 플럭스 기울기
  **k = −dJ/dC 가 곧 OU 루프게인** [V] — 채널 수가 셋포인트 안정성을 정하고, loss-of-function 수송체 = *막에서의 loop-gain-drop*
  (TRPV5/6→신장 Ca 소모; ENaC/SCNN1A→PHA1; H⁺-ATPase/ATP6V→원위 RTA [L]). GHK+게이팅 [F]; k=−dJ/dC [V]; 절대 컨덕턴스 [O].
  결정론 2× sha; 빌드 중 버그 2건 수정(플럭스 부호 반전 → OU 폭발/NaN; vitamin_d_gating은 플럭스 **크기**(abs) 보고).
- **G6 종별 γ** (`repro/_engine/comparative_gamma.py`, NEW; `inherited/comparative_promoters.cache.json`): **HONEST NEGATIVE**.
  osmoregulatory 마스터 유전자 **ATP1A1**(Na⁺,K⁺-ATPase α-1) 프로모터 γ를 6종(굴·은상어·홍어·제브라피시·제노푸스·인간)
  NCBI 실측 — 인간 앵커 재현, 오프라인 재현 [V], 파이프라인 건전(독립 연골어류 2종 γ±0.0003). 그러나 γ는 루프게인 k에 **비단조**
  (Spearman 0.65; k=3.0 제노푸스 γ > k=4.0 인간 γ)이고 프로모터 **GC**를 거의 완벽 추종(Spearman 1.0). → 종별 γ는 잘못된 도구;
  종내 γ-사다리는 단일유전자 종간 비교로 전이되지 않음. 비교 절대 k는 [O] 유지하되 **GC 교란을 명시된 사유**로 가짐.
  (빌드 중 결론 prose 1건 교정: k=3.0 쌍이 "전 범위 초과"라던 표현 → 측정 부울과 모순 → "대부분 차지 + 비단조"로 수정.)
- **배선:** `run_all.py` 섹션 **[12] TRANSPORT DYNAMICS · [13] COMPARATIVE GAMMA** 추가(GATES → **[14]**) ·
  `literature_anchors.py` **A-GHK·A-TRPV·A-ENAC·A-HATPASE·A-ATP1A1** 5개 anchor + 5개 INTERACTIONS ·
  `build_docs.py` `_research()`에 TR/CG 추가, **§12·§13** 페이지 · §11 forward-ref를 §12/§13로 갱신.
- **검증:** 연구 게이트 sha `35d31461…` **불변**(all_green) · docs 11섹션 → **13섹션**(재빌드 byte-identical) · answer-first 58/57단어(40–60 밴드).
  남는 유일한 신규 [O] = G5 절대 전기생리 캘리브레이션(단일채널 컨덕턴스/밀도).

---

## 1. 직전 세션(v0.6.0)이 한 일 — Tier-2 질병 커버리지 (G2·G3·G4 닫음)

사용자 감사: "이온불균형 질병 — 모두 커버했나?" 병리 챕터는 대표 7종을 6개 실패모드로 닫고 희귀/특정형은 cited
parameter로 진입시키는 구조였음. **주요 3종**(마그네슘·CKD-MBD·종양성 고칼슘혈증)이 명시 안 됨이었음. v0.6.0이
이를 **기존 6개 실패모드 재사용(새 프리미티브 없음)** 으로 닫음.

### 새 모듈 `repro/_pathology/tier2_ion_diseases.py` (NEW)
- **G2 마그네슘:** 저/고Mg혈증 = loop-gain drop / buffer-arm failure 모드를 **세 번째 방어 이온**에 적용. 이 권 자체의
  `vp_loops.ou_setpoint`(err=load/k) 재사용 — 실패 arm(낮은 k)에서 Mg-손실 구동 시 저Mg혈증(TRPM6/Gitelman),
  Mg-섭취 구동 시 고Mg혈증. 둘 다 1/k에 단조, 비(比) 4.0× == 게인비, 분산 폭증(Var=σ²/2k). [V]방향.
- **G3 CKD-MBD:** 신장 적분기 게인의 **다중-arm 동시 저하**. 신장 게인을 단계적으로 낮추면 인용 KDIGO 연쇄 재현 —
  PO4↑(err=load/k)·1,25-vitD↓·Ca↓·PTH↑(이차성 부갑상선기능항진증) 네 가지 모두 단조; Ca×PO4 곱은 초기엔 거의 정상,
  진행 CKD에서 침전 천장으로 상승(1.25→2.21). [V]연쇄 방향.
- **G4 종양성 고칼슘혈증(PTHrP):** **setpoint drift UP** = 외인성·억제불가 PTHrP 구동이 방어 Ca를 위로 이동(= T1 reset의
  역). 내인성 PTH는 적절히 **억제**됨(임상 지문: 원발성 부갑상선기능항진증과 구별). [V]방향.
- **등급:** 방향 [V]; 인용 setpoint/변이/지침 [L](혈청 Mg ~0.85 mM; Schlingmann 2002 TRPM6; Gitelman SLC12A3;
  KDIGO 2017 CKD-MBD; Stewart 2005 NEJM PTHrP); 절대 크기·CKD 진행 타이밍 [O]. `status()` 결정론(2× sha 동일).

### 배선
- `run_all.py` 섹션 **[11] TIER-2 ION DISEASES** 추가(GATES → **[12]**) · `literature_anchors.py` **A-MG·A-CKD·A-PTHRP**
  3개 anchor + 3개 INTERACTIONS 추가 · 정본 docs **§11 "Magnesium, CKD-MBD and humoral hypercalcemia"** 페이지
  (answer 56단어·JSON-LD×2·claim-strip, C4 충족; 세 질병별 표 + 재현 + 등급).
- **가산적** — `research_gate()`(γ-창발+스트레스 배터리)는 이 모듈 미import → **연구 sha `35d31461…` 불변**, all_green.
  docs: 10섹션 → **11섹션**(재빌드 바이트 동일; HTML concat sha는 빌드 날짜 내장).

> ⚠️ 빌드 버그 수정 기록: 신규 §11 소스 작성 시 유니코드 이스케이프를 이중 백슬래시(`\\u2192`)로 써 HTML에 리터럴
> `\u2192`가 노출됐던 것을 단일(`\u2192`)로 교정(24곳) — 나머지 파일 규약과 일치. 교정 후 §11 리터럴 아티팩트 0,
> 모든 문자(→ × ² ₄ α γ σ —) 정상 렌더, 재빌드 바이트 동일.

---

## 1b. 직전 세션(v0.5.0)이 한 일 — 비교 이온조절 축 추가 (감사 최대 갭 G1 닫음)

사용자 감사: "이온을 정밀 이용하는 동물 vs 아닌 동물 구분 / 정밀 유지 기제 / 이온 질병 — 모두 커버했나?"
점검 결과 이 권은 **인간 한 종** 모델이라 **종간 구분이 범위 밖**이었음(가장 큰 갭). v0.5.0이 이를 **가산적으로** 닫음.

### 새 모듈 `repro/_engine/comparative_ionoregulation.py` (NEW)
- **같은 R19 기질** 위에서 이 권 **자체의 OU 법칙**(`vp_loops.ou_setpoint`, step error = load/k) 재사용.
  단일 손잡이 = loop gain k(외부 염도 부하에 맞선 내부 방어 강도). **순응자(낮은 k)=환경 추종 / 조절자(높은 k)=내부 방어.**
- 5개 osmotic 전략(인용 [L]): osmoconformer(k 1.0, 환경 100% 추종, 해양 무척추동물) < urea-retaining elasmobranch
  (2.0, 상어·가오리: 요소+TMAO 순응·무기이온 조절) < hyper/hypoosmotic regulator(3.0, 담수/해수 경골어) <
  terrestrial regulator(4.0, 포유류=이 권 baseline, 25%만 추종 = 최정밀).
- **재현(결정론):** 염도 부하에서 순응자 내부 1.00 끌려감 vs 육상 조절자 0.25 방어 → 비 4.0× == 게인비 k_reg/k_conf(4.0).
  환경 스윕: 순응자 변동 100% 추종, 조절자 25% → 조절자가 정밀 이온 사용자. 내부 이탈은 k에 대해 단조.
- **등급:** 분류군↔전략 배정 [L]; 순서·분리 [V]; 절대 k·염도 견딤범위 [O]; **종별 마스터 유전자 γ 미측정 [O]/[H]**.

### 배선
- `run_all.py` 섹션 **[10] COMPARATIVE** 추가(GATES→**[11]**) · `literature_anchors.py` **A-OSMO** 추가 ·
  정본 docs **§10 "Comparative ionoregulation"** 페이지(answer 57단어·JSON-LD×2·claim-strip, C4 충족).
- **가산적** — `research_gate()`(γ-창발+스트레스 배터리)는 이 모듈 미import → **연구 sha `35d31461…` 불변**, all_green.
  docs concat sha: v0.4.0 `6d6a2000…` → **v0.5.0 `d6a67a25…`**(10섹션, 재빌드 바이트 동일).

### 보완계획서 `REMEDIATION_PLAN.md` (NEW)
- **왜 v0.4.0이 "모두 커버"에 미달했는가**(scope mismatch: 단일 종 임상 항상성 ≠ 비교 이온조절) + 갭 인벤토리(G1–G6)
  + 티어 로드맵 + 1차 완료 + 다음 과제. "모두 커버"는 다-증분 프로그램이며 티어로 순차 달성.

---

## 2. ★DOI 발행 후 배선 (자체완결 절차) — 발행 후 단 2곳

1. **`tools/build_docs.py` 24행** `DOI="TBD"` → 실제 concept DOI. (11행 주석도 동일 갱신.)
2. **cross_volume_doi 레지스트리 등록**(전역 사이트 루트; 이 zip 단독엔 레지스트리 없음 → 전역 조립 레인).
3. **재빌드** `python tools/build_docs.py` → 모든 페이지 DOI 채움. 재빌드 바이트 동일(현재 concat `d6a67a25…`,
   DOI 치환 후 그 값으로 새 고정). 연구 게이트 미접촉 → sha `35d31461…` 그대로.
> 가짜 DOI 넣지 않음 — `DOI="TBD"`가 의도된 상태(정직성).

---

## 3. 파일 변경 (원본+추가 — 파편화 없음)

**v0.8.0 (3-레버 치료 조직화 원리):**

| 파일 | 상태 | 내용 |
|---|---|---|
| `repro/_therapy/three_lever.py` | **NEW** | L1/L2/L3 핸들 + 비대칭 정리(only L2 tightens σ²/2k) + 측정-γ 게인 천장 b=γ²/4 + 진통제 27타깃 1:1 사상 + 기존 T1/T2/H-시리즈 라이브 크로스워크 + status() 결정론 |
| `repro/_therapy/disease_remediation.py` | **NEW** | 소유 질병 9종 → 손상 OU 파라미터에서 1차 레버 선택 + 4개 아키타입 시연(variance-limited/setpoint-drift/threshold-margin/reservoir) + 인용·정직등급 개선책 + status() |
| `repro/run_all.py` | 갱신 | 섹션 [15] THREE-LEVER PRINCIPLE · [16] DISEASE REMEDIATION 추가, GATES → [17], tlever/drem import |
| `repro/_engine/literature_anchors.py` | 갱신 | anchor **A-3LEVER · A-ANALGESIC**(진통제 볼륨 DOI 10.5281/zenodo.20733420) + INTERACTION 1행 (게이트 미급전) |
| `tools/build_docs.py` | 갱신 | 개념 DOI 배선(`DOI="10.5281/zenodo.20755910"`, DOI_URL/ANALGESIC_DOI/_URL); `ld_article()` identifier/sameAs + 교차볼륨 citation + knowsAbout 키워드 확장; claim-strip DOI 링크; `_research()`에 TL/DR; **§14·§15·§16** 페이지; VPCARD_3LEVER |
| `CHARTER.md` / `START_HERE.md` / `HANDOVER.md` / `IRREPRODUCIBILITY_LEDGER.md` / `VERSION` | 갱신 | v0.8.0 + 3-레버 증분·DOI 배선 반영 (VERSION 0.7.0→0.8.0) |

**v0.7.0 (Tier-3 — 분자 수송 동역학 + 종별 γ):**

| 파일 | 상태 | 내용 |
|---|---|---|
| `repro/_engine/transport_dynamics.py` | **NEW** | G5 GHK 정전장 플럭스(Nernst 반전·정류) + Boltzmann/Hill 게이팅 + k=−dJ/dC=OU 루프게인 [V] + LOF=막 loop-gain-drop + status() |
| `repro/_engine/comparative_gamma.py` | **NEW** | G6 ATP1A1 6종 실측(HONEST NEGATIVE: γ는 k에 비단조, GC 추종) + status() |
| `inherited/comparative_promoters.cache.json` | **NEW** | ATP1A1 6종 프로모터 캐시(오프라인 재현) |
| `repro/run_all.py` / `literature_anchors.py` / `tools/build_docs.py` | 갱신 | 섹션 [12]/[13](GATES→[14]) · A-GHK/A-TRPV/A-ENAC/A-HATPASE/A-ATP1A1 · §12/§13 페이지 |

**v0.6.0 (Tier-2 질병 커버리지):**

| 파일 | 상태 | 내용 |
|---|---|---|
| `repro/_pathology/tier2_ion_diseases.py` | **NEW** | G2 마그네슘(저/고Mg, ou_setpoint err=load/k 재사용) + G3 CKD-MBD(신장 게인 다중-arm 저하, ou+pth_curve) + G4 HHM/PTHrP(setpoint drift UP, T1의 역) + status() 결정론(2× sha) |
| `repro/run_all.py` | 갱신 | 섹션 [11] TIER-2 ION DISEASES 추가, GATES → [12], t2dis import |
| `repro/_engine/literature_anchors.py` | 갱신 | anchor **A-MG**(Schlingmann 2002/Gitelman/de Baaij 2015) · **A-CKD**(KDIGO 2017) · **A-PTHRP**(Stewart 2005 NEJM) + INTERACTIONS 3행 |
| `tools/build_docs.py` | 갱신 | `_research()`에 T2=t2dis.status(); §11 페이지(세 질병 표·재현·등급); 유니코드 이스케이프 단일 백슬래시 교정(24곳) |
| `CHARTER.md` / `START_HERE.md` / `HANDOVER.md` / `REMEDIATION_PLAN.md` / `IRREPRODUCIBILITY_LEDGER.md` / `VERSION` | 갱신 | v0.6.0 + Tier-2 행·[O] 항목 반영 (VERSION 0.5.0→0.6.0) |

**v0.5.0 (비교 이온조절 축):**

| 파일 | 상태 | 내용 |
|---|---|---|
| `repro/_engine/comparative_ionoregulation.py` | **NEW** | 5개 osmotic 전략 + OU 법칙 재사용 + 순응자/조절자 분리 [V] + 환경 스윕 + status() |
| `REMEDIATION_PLAN.md` | **NEW** | 보완계획서(미달 원인·갭 인벤토리 G1–G6·티어 로드맵·1차 완료·다음 과제) |
| `repro/run_all.py` | 갱신 | 섹션 [10] COMPARATIVE 추가, GATES → [11], comp import |
| `repro/_engine/literature_anchors.py` | 갱신 | anchor A-OSMO(비교생리: Schmidt-Nielsen/Evans/Ballantyne) 추가 |
| `tools/build_docs.py` | 갱신 | `_research()`에 C=comp.status(); §10 "Comparative ionoregulation" 페이지(표·재현·next-task [O]/[H]) |

연구층 핵심(γ 엔진·스트레스 배터리·`reports/research_complete.json`), RI5 TmP/GFR(v0.3.0), 프런티어 4가설(v0.3–0.4.0)은 **불변**.

## 4. 재현 방법 (새 창)
```
python repro/run_all.py     # … + [9]frontier(4) + [10]comparative + [11]Tier-2 + [12]transport + [13]comp-γ + [15]three-lever + [16]disease-remediation + [17]게이트 (all_green=True)
python tools/build_docs.py  # docs/ 정본 HTML 재빌드 (PHASE=writing, 16섹션, 개념 DOI 박힘)
```
불변량: 연구 sha **`35d31461…`**(2× 동일, v0.8.0 가산적 불변 — γ-창발·스트레스 배터리는 치료 모듈 미import) ·
docs 재빌드(16섹션; 개념 DOI `10.5281/zenodo.20755910` JSON-LD/claim-strip/footer/llms.txt 박힘) · 16섹션 전부 C2/C4(answer 40–60·
JSON-LD×2·claim-strip·canonical·정직 grade·영어 본문) · 신규 모듈 2× sha 동일.

## 5. 잔여 항목 (보완 Tier-3 + 전역 조립)
**`REMEDIATION_PLAN.md` E절에 자체완결 핸드오버(재사용 프리미티브·인용·예상 등급) 상세.** 요약:
- ✅ **Tier-1 (v0.5.0):** G1 종간 구분(비교 이온조절). **완료.**
- ✅ **Tier-2 (v0.6.0):** G2 마그네슘 · G3 CKD-MBD/이차성 PTH · G4 종양성 고칼슘혈증(PTHrP) — 모두 기존 6 실패모드
  재사용으로 닫음. 인간 질병 커버 대표 7종 → 주요 거의 전부. **완료.**
- ✅ **Tier-3 (v0.7.0):** G5 분자 수송체 동역학(GHK 플럭스·게이팅, k=−dJ/dC=OU 게인) · G6 종별 γ 실측(HONEST NEGATIVE:
  GC 교란으로 [O] 유지, 사유 명시). **완료 — Tier 로드맵 완결.**
- ✅ **치료 조직화 층 (v0.8.0):** 3-레버 원리(L1/L2/L3, 비대칭 정리, 측정-γ 천장) + 진통제 볼륨 상속 + 소유 질병 9종
  개선책. **완료.**
- ⏳ **전역 조립(다음):** **cross_volume_doi 레지스트리 등록**(형제 권과 함께) · **형제 권 교차링크**(전역 루트 공유 시) ·
  **RI5 γ→절대값**(설계상 [O], 정직하게 유지). 개념 DOI는 **발행·배선 완료**(`10.5281/zenodo.20755910`).

## 6. 불변 규칙 (유지)
γ는 측정값(피팅 금지) · 결정론(seed/round/2×sha) · 정직한 grade + [O]/[H] 사유 명시 · 본문 영어 · 단일 zip(원본+추가) ·
연구 게이트 sha `35d31461…` 보존(새 작업은 가산적, γ-창발·스트레스 배터리 불변).
