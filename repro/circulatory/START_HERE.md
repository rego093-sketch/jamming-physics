# START HERE — Circulatory Transport (circulatory_vp_site)  ·  v0.1.0

> 이 zip을 **새 창에 넣고 이 파일을 먼저 정독**하면 상위 백서 없이 바로 연구를 시작할 수 있다.
> 이 패키지는 **자족적**이다: 기질 프리미티브(FHN/R19), VP-SPEC v1.8 전문, 장기 정체성 γ, (심폐는) 심박 앵커를 내부에 들고 있다.

## 0. 한 줄 정체
Vasculature (Windkessel pressure-flow), kidney (glomerular filtration + osmoregulation loop) and liver (hepatic clearance) emerge as a transport+clearance network driven by the cardiac pump boundary condition.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 장기를 **창발**하고, 진동자(FHN)가 박동함을 확인하고, 스트레스 배터리·암 모듈 상태를 출력하고,
**집필 잠금 여부**를 보고한다. (HTML은 만들지 않는다 — 집필은 게이트로 막혀 있다.)

## 2. 이 백서의 범위 (자기 범위를 명확히)
mind가 하듯 **장기를 직접 시뮬레이션으로 창발하여 순환**시킨다. 단 이 패키지는 기계(mechanism) 동역학을 다루며 felt(느낌) 층이 아니다 — felt/내수용은 mind의 몫이다.

**창발 대상 장기 (정체성·발생순서는 DNA에서 인용, 동역학만 이 패키지가 추가):**

| master gene | organ | physiological role | dyn class |
|---|---|---|---|
| SIX2 | kidney | metanephric nephron: filtration + tubular transport + osmoregulation | control-loop |
| HHEX | liver | hepatic blood flow + first-pass clearance/metabolism | clearance |
| (vasculature) | vessels | pressure-driven flow network (no single master gene; mesodermal/diffuse) | transport |

**상속(IN) — 내부 vendoring됨, 재수령 불필요:**
- cardioresp: cardiac output + arterial PaO2/PaCO2 (boundary conditions, cited)
- DNA: organ identity (SIX2, HHEX) + emergence order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT) — 형제 패키지와의 이음매(SSOT 단일소스 유지):**
- renal clearance of solutes -> shared interstitial milieu
- hepatic clearance kinetics -> digestive_vp_site (first-pass seam)

## 3. 판별 타깃 (엄격히 통과시켜야 집필 가능)
- **T1 MAP** — mean arterial pressure = CO x SVR reproduces cited resting ~93 mmHg from the pump BC [V], abs [O]
- **T2 Windkessel** — diastolic pressure decay time constant = R x C matches cited aortic value [V]
- **T3 GFR autoregulation** — tubuloglomerular feedback holds GFR flat across a BP range (plateau) [V]
- **T4 osmoregulation** — an osmotic load is corrected by the ADH loop to setpoint ~285 mOsm/kg [L] [V]
- **T5 hepatic clearance** — first-pass extraction ratio sets oral bioavailability for a cited tracer [V]

## 4. 암(cancer) — mind와 다른 점
외부자극(발암물질) 노출 시 암이 **얼마나 더** 발생하는지의 메커니즘을 연구한다. VP-native 커널: 발암물질 = R19 스위치의 지속적 이상 드라이브 h_c → 장벽을 낮춤 → 악성 basin으로의 Kramers 교차율↑ → **RR(dose)** = rate(dose)/rate(0). 판별 = 용량-반응 기울기/형상을 인용된 역학 앵커에 맞춤. 등급: 앵커 [L] / 형상 재현 [V] / 절대 발생률 [O](장애물 명시). 위치: `repro/_oncology/`.
- **renal cell carcinoma** ← tobacco smoke; trichloroethylene; aristolochic acid  · anchor: RR vs exposure (smoking, TCE cohorts) [L]; shape [V]
- **hepatocellular carcinoma** ← aflatoxin B1; chronic HBV/HCV; ethanol  · anchor: aflatoxin x HBV multiplicative synergy RR [L]; barrier-lowering synergy [V]

## 5. 절대 규칙 — 연구 먼저, 집필 나중 (명시)
**매우 높은 수준의 엄격한 연구(많은 스트레스 실험 포함)를 완료하기 전에는 집필을 시작하지 않는다.**
- `tools/build_docs.py`는 `gates.writing_locked()`가 True인 동안 **무조건 거부**한다.
- 잠금 해제 조건 셋이 모두 충족돼야 집필이 열린다: ① `repro/_verify/gates.py`의 `research_gate()`가 `all_green` ② `gates.write_research_complete()` 호출로 `reports/research_complete.json` 생성 ③ 루트 `PHASE` 파일을 `writing`으로 변경.

## 6. 집필 시 규칙 (VP-SPEC v1.8 — 전문은 루트 `VP_SPEC_v1_8.md`)
- **정본은 HTML** (C2). `docs/` 아래 HTML이 정본이다 ("html이 정본").
- **제목별로 별도 HTML** (C4 / 6장): 구글·RAG 추출을 위해 섹션당 1페이지. answer-first(`<p class="answer">` 40–60단어), 자체완결, JSON-LD(ScholarlyArticle·BreadcrumbList), canonical, claim-strip(등급+재현링크+DOI), 인용 잠금량마다 vp-card.
- **본문은 영어** (C0). 표·그림 포함. 모든 정량은 결정론 재생성(C1, 2×sha256). 모든 `[O]`는 사유 명시(C3).
- 출력: `docs/<slug>/index.html`(섹션별) + `docs/index.html`(허브) + `_meta.json` + `sitemap.xml` + `robots.txt`(봇 허용) + `llms.txt`.

## 7. 사용자 반환 규약
- 작업 종료 시 **압축파일 1개**만 반환(내부 경로 = 패키지 상대경로). 파편화 금지. 받은 자료에 추가/수정분을 합쳐 단일 zip으로 반환 (C0).

## 8. 디렉토리
```
circulatory_vp_site/
├── START_HERE.md            ← (이 파일) 새 창 부팅
├── CHARTER.md               ← 범위·이음매·타깃·암 범위 (정본 스코프)
├── VP_SPEC_v1_8.md          ← 작업표준 전문 (집필 시 적용)
├── PHASE                    ← "research" (집필 잠금 해제 전 고정)
├── VERSION
├── inherited/               ← vendoring된 상속 자산 (재수령 불필요)
│   ├── vp_substrate.py      ← FHN Neuron + R19 (프리미티브 단일소스, 수정 금지)
│   ├── organ_gamma.json     ← 이 패키지 장기들의 측정 γ (DNA에서)
│   ├── organ_identity.md    ← master gene → organ, 등급 [V] (DNA atlas 인용)
│
├── repro/
│   ├── _engine/vp_cir_engine.py   ← 장기 창발 + 순환 (창발은 지금 실행; 동역학은 골격)
│   ├── _verify/stress_tests.py     ← 스트레스 배터리 (타깃 명시, TODO)
│   ├── _verify/gates.py            ← 연구/집필 PHASE 게이트
│   ├── _oncology/carcinogen_dose_response.py  ← 발암물질 용량-반응 커널 (골격)
│   ├── run_all.py                  ← 연구 진입점
│   └── REPRODUCE.md
├── tools/build_docs.py      ← 집필 HTML 생성 (게이트 통과 전 거부)
├── docs/                    ← (집필 전 비어 있음) 정본 HTML 생성 위치
├── manifest/circulatory_vp_site.csv
├── reports/                 ← gate.json / research_complete.json
└── IRREPRODUCIBILITY_LEDGER.md
```
