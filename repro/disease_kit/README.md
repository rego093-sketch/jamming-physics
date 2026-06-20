# VP Disease Emergence Kit — v0.31.0

**DNA 를 창발하여 질병을 읽고, 합당한 치료 방향을 도출한다.**
*Emerge real DNA → read a disease as a switch perturbation → reason about treatment.*

Independent research · Young Jae Lee (이영재) · ORCID 0009-0002-7535-8245 · CC BY 4.0
**Concept DOI: 10.5281/zenodo.20755262** · rare / single-gene / hereditary disease (희귀병)
**Sibling whitepaper (burden & standard-of-care context):** `disease_wp` — concept DOI **10.5281/zenodo.20763842** (CC BY 4.0)
Part of the jamming-physics.org programme (VP Theory / Jamming Physics).

---

## 0.40. v0.31.0 — 질병 추가: 첫 백질이영양증(MLD) + 아홉 번째 보류 클래스(DM1) (read this first)

v0.31.0 은 **질병 추가** 릴리스다(ROADMAP §3.7 슬롯). 엔진 변경 **없이**(리드는 기존 `replace` 레버 재사용),
`analysis.json` 무수정 → **78개 prior per-disease 해시 drift 0**(78 → **80** = 68 RESOLVED + 12 SUSPENDED); 6 module ·
4 site · 1 system-inheritance 해시 불변/재동결.

- **+1 RESOLVED — `metachromatic_leukodystrophy` (ARSA):** 키트 **첫 백질이영양증**·**첫 sulfatide 기질**. 아릴설파타제 A
  효소/LOF → 리소좀 sulfatide(3-O-황산갈락토실세라마이드)-이화 축 **DOWN**(축적이 희소돌기아교세포[CNS]·슈반세포[PNS]
  탈수초화) → 리드 `replace` = **승인 ex-vivo 자가 HSC 유전자치료 atidarsagene autotemcel**(Lenmeldy FDA 2024 /
  Libmeldy EMA 2020), 인과 **ARSA 에 DIRECT** — 이식 후손(혈뇌장벽 통과 공여-유래 미세아교세포 포함)이 효소를 교차-교정.
  **승인이지만 결정적 한계는 크기 아닌 TIMING**: 발현전/초기증상 환자 전용(탈수초화 확립되면 교정 창 닫힘; 대부분 발병 후
  진단) → 효과 정도 `[O]`; 척수강내 ERT 2차 arm 은 investigational(재조합 효소는 BBB 비통과). γ 1.4806 chr22;
  **`lysosomal_enzyme_replacement`** 축-family(*교정 생화학*이지 HSC *전달방식*이 아님 → Gaucher/Fabry/Pompe/MPS-I 와
  함께, 버든-티어 형제 X-ALD[`peroxisomal_substrate_load`]와는 분리); 티어 **B3/U4/D4**.
- **+1 SUSPENDED — `myotonic_dystrophy_type_1` (DMPK):** **아홉 번째 보류 기전 클래스** — repeat-EXPANSION 구동 **독성-RNA
  GOF / spliceopathy**. DMPK 3′-UTR CTG 팽창(~50 ~ >3,500)은 전사되나 **비번역**(독성 단백 없음); 변이 CUG-반복 전사체가
  **핵 foci** 에 축적되어 **MBNL1/2** 스플라이싱 인자를 격리(CELF1 상호 안정화) → **TRANS** spliceopathy(CLCN1→근긴장증,
  INSR→인슐린저항, SCN5A→전도장애)를 근육/심장/CNS 전반에 — "RNA dominance". 병변은 3′-UTR 반복 **복제수** + 독성-RNA
  **상태**가 **다른 유전자**의 전사체에 trans 작용하는 것이지 DMPK 프로모터 **SEQUENCE** 변화가 아님(DMPK 프로모터는
  γ 1.5132 로 완전 가독이나 3′-UTR 반복-길이·trans 독성-RNA spliceopathy 는 비가독). 삼핵산-반복 분류를 **운명별로 완성**:
  Huntington[HTT CAG, **coding** → 독성 **단백**, RESOLVED] / fragile X[FMR1 CGG, **5′-UTR/프로모터** → 메틸화 **침묵**,
  보류] / DM1[DMPK CTG, **3′-UTR** → 독성 **RNA** in trans, 보류]. 가독성으로만 보류, 치료 부재 때문 아님(승인 DMT 없음;
  DMPK-저하/CUG-표적 ASO·siRNA, MBNL-치환 소분자 모두 investigational). 성인발병 최다 근이영양증(~1:8,000).

**Freeze 부기:** S4 가 2개 신규 per-disease 해시 자동 추가(`16ac25dae822`, `46adac7d0b44`); **S5 재동결** —
direction-recovery 67/67→68/68(승인 57→58, 무승인 꼬리 10 **불변**: MLD 승인), 버든 랭킹에 MLD(#17), indirect 카운트
**58 불변**(MLD 리드 DIRECT → per-disease census 에 `n_indirect=0` 등재), MLD 를 `lysosomal_enzyme_replacement` 로 분류.
`open_directions_cards`·`claim_scan_v2` **불변**(MLD 는 승인-치료 **DONOR** — 무승인-꼬리 recipient 도 orphan 도 아니어서
재배치/orphan 카드 무발생, 거짓-주장 스캔 무발화). 사이트 재동결(catalogue corpus 67→68 resolved); system-inheritance
해시 불변(MLD 단일계통; DM1 보류 — 둘 다 다계통 manifest 비진입). 캐시 **112→114**(ARSA, DMPK). ledger **B33** +
§C(DM1 9번째 + McCune-Albright 8번째 백필). 각 리드 출하 전 **웹 검증**.

`python3 repro/run_all.py` → **6/6 스테이지**(68 resolved + 12 suspended), 80 per-disease + 6 module + 4 site + 1
system-inheritance 해시 drift 0. 개념 DOI 불변(10.5281/zenodo.20755262, 희귀병).

---

## 0.39. v0.30.0 — system-inheritance: 다(多)시스템 난치병의 장기-시스템 상속 (이전 릴리스)

v0.30.0 은 **system-inheritance** 릴리스다(ROADMAP V). 질병을 *더 수집*하지 않고, **이미 RESOLVED 인 다시스템
난치병이 닿는 각 장기 시스템의 구조를 상속**해 치료 방향을 한 겹 더 연다. 질병·엔진 변경 없음, `analysis.json`
무수정 → **78개 per-disease 해시 drift 0**(6 module · 4 site 해시도 불변); **새 네 번째 freeze(1 hash)** 추가.
개념 DOI·캐시(112) 불변.

> **텔로스:** 구조를 모르면서 희귀병을 다루기는 어렵다. 단일 원인유전자 병변은 여러 장기에 동시에 발현하는데,
> kit 은 그 *하나의* 프로모터(스위치 perturbation + 교정 방향)는 읽지만 각 장기 *시스템의 구조*는 모른다. 그
> 구조는 VP body 형제들이 측정·동결해 둔 자산 — 그것을 **읽기 전용으로 상속**하고 lead lever 의 compartment
> **REACH vs GAP** 을 드러낸다. 각 GAP 이 곧 다음, 비자명한 치료 방향이다.

- **(V-registry)** `system_inheritance/sibling_registry.json` (`build_sibling_registry.py` 생성) — 13 형제의
  **49 organ-master 유전자 + 실측 γ**(SantaLucia 1998 NN-stacking dG, 재계산 아님 — 그대로 인용; 예: heart/NKX2-5
  1.513, kidney/SIX2 1.5556, MC4R 1.272, eye/PAX6 1.511), 2 compartment anchor(neuro cns/pns; dna 정체성 SSOT),
  §6 ownership contract(형제별 제외 주요질환).
- **(V-manifest)** `system_inheritance/multisystem_manifest.json` — 이미 RESOLVED 인 **8 다시스템 난치병**
  (Fabry/GLA, Pompe/GAA, cystic_fibrosis/CFTR, cystinosis/CTNS, tuberous_sclerosis/TSC2, Bardet-Biedl/BBS1,
  Wilson/ATP7B, haemochromatosis-1/HFE)의 필요한 장기 시스템 부분집합 + 인용 + lead modality. (DEMONSTRATION
  set — 나머지는 이후 버전 roll out.)
- **(V-module)** `pipeline/system_inheritance.py` [NATIVE, fail-closed] — 동결 `analysis.json` + vendored
  registry/manifest 를 읽기 전용으로. disease 마다 **provenance handshake**(RESOLVED[suspension rule];
  causal_gene == frozen primary_switch.gene; lever == frozen lead lever; signature ⊂ frozen agent_class) 후
  각 affected 시스템을 *실측* registry γ(또는 neural anchor)로 해소, lead lever 의 compartment **REACH** 를
  *인용된 정성 biodistribution*(reach-class ∈ modality reach-set)으로 분류. **census: 8 질병 · 31 link · γ-system 27
  · reached 26 · GAP 5**(Fabry→PNS 소섬유[BBB]; cystinosis→무혈관 cornea[topical]; Bardet-Biedl→retina+신+limb
  [MC4R agonist 가 satiety node 만]). Wilson(chelator 가 간·뇌·각막 모두)·haemochromatosis(phlebotomy 가 전 실질)는
  **대조 사례** — reach 읽기가 막연한 비관이 아닌 *modality 별 구조적 사실*임을 증명.
- **방화벽:** STRUCTURE(어느 장기·실측 γ) + DIRECTION(어느 compartment 에 닿는가)만 — reach 는 *닿는가/안 닿는가*
  의 인용된 방향; 교정의 *정도*는 항상 `[O]`. magnitude 스캔이 dose/efficacy/rate/p-value 차단(γ 상수·저널 인용은
  magnitude 아님). **exclusion gate(§6)**: 모든 manifest 질병은 gene-defined 이고 형제의 주요질환과 충돌 없음 —
  암·제2형 당뇨·본태성 고혈압·일반 골다공증·후천 감각질환은 제외(형제 소유).

`python3 repro/run_all.py` → **6/6 스테이지**(S6 추가; 67 resolved + 11 suspended), 78 per-disease + 6 module + 4 site
+ **1 system-inheritance** 해시 drift 0. 설계 정본은 `system_inheritance/SYSTEM_INHERITANCE.md`; 전체 변경 정본은
`VERSION`. ledger B32.

---

## 0.4. v0.28.0 — 무엇이 바뀌었나 (이전 릴리스)

v0.28.0 은 **촉매 미션(catalytic-mission)** 릴리스다 — 질병을 *더 수집*하지 않고, **이미 가진 "승인약-없는 꼬리"를
*행동가능*하게** 만든다(§0 텔로스 "연못의 돌"). 질병·엔진 변경 없음, `analysis.json` 무수정 → **78개 per-disease 해시
drift 0**; 모듈 동결 4→6, **새 세 번째 site 동결(4 파일)**. 개념 DOI·캐시(112) 불변.

- **(III-A2) 교차질병 재배치 스캐너** `pipeline/repurposing_scanner.py` — MOLECULAR CORRECTIVE-AXIS 수준의 curated
  `axis_family` 분류(39 families; 미분류 resolved 있으면 **gate FAIL-CLOSED** → 향후 모든 추가에 정직한 분류 강제)로
  (axis_family × 교정방향 × lever_class) 버킷마다 "승인약-없는 RECIPIENT ↔ 승인약-보유 DONOR" 가설 surfacing →
  **4 가설(2 families) + 6 orphan** (장부 정합: 4 ∪ 6 = 승인약-없는 꼬리 10):
  `retinal_gene_replacement|UP|replace` {choroideremia ← LCA2/voretigene; XLRP ← LCA2};
  `toxic_gof_protein|UP|reduce` {huntington ← SOD1-ALS/tofersen + TTR; RHO-adRP ← SOD1-ALS + TTR};
  orphan {dravet, HHT, mecp2-중복, menkes, X-linked NDI, usher-2a}. **두 가설군 모두 정직하게 저-신규성
  (CONFIRMATORY)** — recipient 가 이미 그 클래스를 추구 중이므로 알려진 방향을 *복원*하는 것이고, 이것이 매칭 논리를
  **검증(VALIDATE)** 한다(새 치료 과대주장이 아님). 방화벽: (axis_family × 방향 × lever_class) 서명 + 가설마다 falsifier,
  용량/효능/역가는 항상 [O]. 동결 `repurposing_hypotheses.json` b840a499f8e8.
- **(III-A) 촉매 open-directions 카드** `pipeline/open_directions_card.py` — 꼬리를 **10장**(4 repurposing-candidate
  + 6 orphan)의 행동가능 연구카드로: 동결 스캐너 분할 + 각 질병의 동결 corrective-방향 falsifier(`measurable_by` =
  *가장 싼 반증 실험*, **날조 없음**)만 읽는다; repurposing 카드는 donor-귀속 후보 클래스 부착("subretinal AAV gene
  replacement"; "SOD1-lowering ASO" + "TTR-lowering siRNA/ASO"), orphan 카드는 정직하게 클래스 없음. 행동가능 ==
  반증가능. 동결 `open_directions_cards.json` 61c29db81807.
- **(IV-A) 정본 retrieval-ready HTML 사이트** `pipeline/build_site.py` — 동결 JSON + VERSION 메타(시계 안 읽음 →
  byte-identical 재빌드)만 읽어 `site/` 4파일: `index.html`(면책 배너가 **첫 `<body>` 요소**; answer-first
  `<p class="answer">` 40-60 단어[=54]; **꼬리·재배치 두 테이블이 헤드라인**; method/firewall 절; JSON-LD @graph =
  WebSite + Person[ORCID, sameAs DOI] + Dataset + 2× Claim/Rating[O]), `sitemap.xml`, `robots.txt`(STAGING
  `Disallow: /` + 7개 검색봇 production allow-list 주석으로 한 줄 cutover), `llms.txt`(<5 KB[=1753 B]). 페이지 방화벽
  = NUMERIC-MAGNITUDE 패턴 게이트(키워드 금지 아님) → 면책 문구·질병 수가 오탐을 안 낸다. site self-test = 두
  in-process 빌드가 **BYTE-IDENTICAL**. `python3 pipeline/build_site.py --write` 로 재빌드.
- **(보강) M5v2 claim-scanner**: scope 3 → 5 모듈, DOSING 패턴 경화 — bare `dose`/`dosage` 제거(정당 생물학
  "gene dosage"/"dose-response window" 에 오탐; mecp2 중복 질환의 동결 `analysis.json` 에서 새 모듈 출력으로 그대로
  surfacing); 정량형 `\d mg`·mg/kg·twice/once daily·bid/tid/qd·per kg·"dose of \d" 만 발화 → **더 정확**(약화 아님).
  심은 self-test("50 mg/kg twice daily; Kd=3nM; cures…safe")는 여전히 ≥3 클래스 발화. `analysis.json` 무수정 → 78
  해시 drift 0. claim_scan_v2 **f4019841bab2**(이전 bf528df05aa8 — scope 3→5 + DOSING 경화로 *설계상* 변경).

`python3 repro/run_all.py` → 5/5 스테이지(67 resolved + 11 suspended), 78 per-disease + 6 module + 4 site 해시 drift 0.
전체 변경 정본은 `VERSION`. ledger B31.

---

## 0.41. v0.27.0 — 무엇이 바뀌었나 (이전 릴리스)

v0.27.0 은 **질병추가 + 환자-면책** 릴리스다: **+2 resolved**(atypical_hemolytic_uremic_syndrome / CFH — 키트 첫
보체-캐스케이드 read, 보체 축 UP → C5 에서 승인-그러나-간접 eculizumab/ravulizumab 로 `restrain`; mucopolysaccharidosis
type I / IDUA — 아홉째 리소좀 read, 첫 글리코사미노글리칸 기질, 축 DOWN → 승인 ERT laronidase 로 `replace`), **+1
suspended**(mccune_albright_syndrome / GNAS — 여덟째 등재 기전 클래스, 유전 참조에 없는 후-접합 **체세포 모자이시즘**),
엔진 변경 없음 → 75개 → 78개 per-disease, 모듈 4개. 캐시 105→112. **추가: 환자용 시뮬레이션 면책 인프라**
(`pipeline/disclaimer_banner.py` 단일진실원천 한·영 배너 + `pipeline/explain_disease.py` 사람-대면 출력 시 배너 *맨 위
강제*) — 읽기전용, 해시 불변; 면책은 이제 구속 규정. 전체 변경 정본은 `VERSION`.

---

## 0.42. v0.26.0 — 무엇이 바뀌었나 (이전 릴리스)

v0.26.0 는 **질병추가** 릴리스다. 실제 NCBI 프로모터 DNA 에 검증한 **2개 resolved + 1개 suspended**, **엔진 변경 0**
(두 resolved lead 모두 기존 lever 재사용 — Factor V Leiden `restrain`, Bardet–Biedl `potentiate`; 새 역할·기전·
축사상·lever 없음) → 이전 72개 동결 해시 drift 0, 총 **75개 per-disease (65 resolved + 10 suspended)** + 모듈 4개.
개념 DOI 불변(10.5281/zenodo.20755262). 각 lead 의 승인 상태는 출시 전 **웹 검증**. THE THEME: **승인-그러나-간접 쌍**
— 두 resolved read 모두 **인과 유전자를 건드리지 않는 온라벨 승인약**을 재도출 → 간접-lever 인구조사 **55 → 57**
(두 신규 lead 이 **모두** 간접인 첫 릴리스).

**Factor V Leiden (F5, accelerator/GOF → 응고 추진 axis UP)** — 키트의 **첫 procoagulant-FACTOR 기능획득** read. F5 는
응고인자 V 를 코딩하고, R506Q(Leiden) 대립유전자는 factor Va 의 **첫 활성화단백질C(APC) 절단부위를 제거** → 활성
보조인자가 **APC-저항성**이 되어 너무 느리게 분해 → 트롬빈 생성이 제어 없이 진행 → axis UP(accelerator/GOF; 교정
lever 는 **억제**). 이는 키트에 이미 있는 **antithrombin/SERPINC1 브레이크-소실의 정확한 가속자-GOF 거울상**: 둘 다
**같은 응고축을 UP** 으로 밀어 정맥혈전증으로 향하나, FVL 은 **응고 가속자를 과구동**하는 반면 antithrombin 결핍은
**응고 브레이크를 해제** — 한 축, 두 반대 분자 경로, 깔끔한 (유전자×기전) 서명. **F5-표적 약물은 없으므로**, 강제
"응고 억제" 방향은 한 단계 하류 트롬빈/factor Xa 에 작용하는 **일반 승인 항응고제**(**DOAC** — apixaban/rivaroxaban/
dabigatran, 또는 warfarin)를 재도출 — **`approved`** 이며 정맥혈전색전증(VTE)에 **온라벨**이나 F5 에 **간접**(연쇄를
억제하지 Leiden 보조인자를 직접 치지 않음) → 크기/용량/효능 **[O]**; 2번째 **investigational** 팔은 APC-저항 보조인자를
`correct`(대립유전자-특이, 전임상) 동시도출. 이는 **LEPR 패턴**(승인+간접)이지 승인약-없는 꼬리 항목이 *아님* —
약물은 승인·온라벨이며, 단지 인과 유전자 *옆에서* 작용. 방향 [F]/크기 [O]; **`direction_confidence` = clean**
(accelerator × GOF → axis UP 은 명확). context F2(트롬빈 — lead 의 실제 표적), PROC(단백질 C — 무력화된 브레이크).
γ 1.3512 chr1 1q24.2 −가닥, barrier 0.45644. dwell[UP] 1.42786 < 1.6027 < 1.96331. OMIM 188055. file-hash 08a664f1e7be.

**Bardet–Biedl 증후군 (BBS1, accelerator/LOF → 시상하부 멜라노코르틴 포만신호 axis DOWN)** — 키트의 **두 번째
증후군성 섬모병증**(USH2A 와 짝), 한 BBSome-소단위 병변을 **비만 + 망막병증 + 신장 + 다지증**에 걸쳐 읽는 read. BBS1
은 가장 흔한 BBS 유전자이며 M390R 대립유전자가 **BBSome**(섬모 수송 외피) 조립을 손상 → 화물(렙틴-멜라노코르틴 포만
기구 및 광수용체/신장 섬모 화물 포함)이 오배송 → 시상하부 포만신호 **실패** → 과식성 비만 → axis DOWN(accelerator/
LOF; 교정 lever 는 **강화**). 강제 "포만 추진 상향" 방향은 **setmelanotide / Imcivree**(**MC4R 작용제**, **2022-04
FDA 가 BBS 비만에 특이 승인**)를 재도출 — **`approved`** 이나 **간접**(고장난 BBSome 을 **우회**해 하류 MC4R 수용체를
직접 구동), 그리고 **비만 arm 전용** 승인(망막병증·신장 arm 승인약 없음) → 크기/효능 **[O]**; 2번째 **investigational**
팔은 BBS1 을 `replace`(유전자치료, 전임상) 동시도출. 다시 **승인-그러나-간접 / LEPR** 형태 — 그리고 setmelanotide 의
LEPR/POMC 결핍에서의 *직접* 사용과 대비되는 지점: 같은 약이지만 BBS 에선 **수송 실패의 우회**이지 결손 리간드의
대체가 아님. 방향 [F]/크기 [O]; **`direction_confidence` = clean**(포만-DOWN read 는 명확; 비만-전용 승인은 **범위
[O]** 진술이지 방향 분기가 아님). context BBS10(2번째로 흔한 BBS locus), MC4R(lead 의 실제 표적). γ 1.4268 chr11
11q13.2 +가닥, barrier 0.50894. dwell[DOWN] 1.00253 < 1.27186 < 1.54936. OMIM 209900. file-hash ffce28b20709.

**Fragile X 증후군 / 취약X (FMR1) — 보류(SUSPENDED): 반복-팽창 구동 프로모터 CpG-메틸화 침묵.** FMR1 5'-UTR 의 CGG
반복이 완전돌연변이(>200)로 팽창하면 FMR1 프로모터의 **CpG섬 과메틸화**를 유발 → 이질염색질로 포장 → FMR1 전사
**침묵** → FMRP(시냅스 번역 억제자) 소실 → 지적장애·자폐·대고환증의 취약X 표현형. FMR1 프로모터는 사실 **참조 DNA 로
완벽히 읽힘**(캐시 γ 1.4563, chrX; **패널 전체 최고 CpG 밀도 0.0508** — 즉 완전돌연변이에서 메틸화-침묵되는 바로 그
강한 CpG섬)이나, 엔진은 **비메틸화 참조** 상태를 읽고 **메틸화·반복길이 채널이 없어** 침묵 병변을 읽지 못함. 이는
**FSHD 보류의 정확한 거울상**(DUX4 를 탈억제[활성화]하는 반복 **수축**)이며 — 같은 반복/후성 축, 반대 방향 — 헌팅턴
(해결됨)과는 **같은-병변-부류 대조**: HTT 의 CAG 팽창은 **코딩** 영역이라 엔진이 locus-스위치 수준에서 읽는 독성
단백질을 만드나, FMR1 의 CGG 팽창은 **프로모터/후성**이라 엔진이 못 읽는 메틸화-침묵으로 작동. **치료 부재가 아닌
순전히 엔진-가독성으로 보류**(FMR1-재활성/탈메틸화 전략은 의미 있는 FMRP 를 복원 못 했고, mGluR5/GABA-B 시험
[mavoglurant, arbaclofen]은 하류 신호를 다룸; 승인 질병조절치료 없음). **일곱 번째 보류 기전 클래스** — 이수성(다운)·
각인(PWS/Angelman/BWS)·반복-**수축**탈억제(FSHD)·미토콘드리아 게놈(LHON/MELAS; Kearns-Sayre)·인접유전자 미세결실
(22q11.2) 여섯과 구별. 유병률 ~1:4,000 남성, ~1:8,000 여성 — 가장 흔한 유전성 지적장애 원인. OMIM 300624. file-hash
ef373b93d869. (ledger §C; Verkerk 1991 Cell 65:905; Pieretti 1991 Cell 66:817; Oberlé 1991 Science 252:1097)

캐시 98 → 105 유전자(F5 1.3512, F2 1.4194, PROC 1.4439, BBS1 1.4268, BBS10 1.4200, MC4R 1.2720, FMR1 1.4563 추가).
모듈 4개 재동결(burden 63→65, 방향-회수 63→65; 간접 census **55→57** — 두 lead 모두 간접; direction_recovery
ff77aaaad029, disease_priority_ranking f6a652e2a084, indirect_lever_honesty d91bd82a7d9b, claim_scan_v2 bf528df05aa8
불변), drift 0. 점수판: **65/65** 회수(축 UP 38 / DOWN 27; 직접 35 / 간접 30); clean 62 / cited-contested 3 /
ambiguous 0; 승인약-없는 꼬리 **10 불변**(임상 7 + 임상시험 3); 승인 **55**(+FVL 항응고제, +BBS setmelanotide — 둘 다
승인이라 꼬리 불변). 전체 변경 정본은 `VERSION`.

---

## 0.40. v0.24.0 — 무엇이 바뀌었나 (이전 릴리스)

v0.24.0 는 **질병추가 + 키트 최초의 네이티브 모듈** 릴리스다. 실제 NCBI 프로모터 DNA 에 검증한 **2개 resolved + 1개
suspended**, **엔진 변경 0**(두 resolved lead 모두 기존 lever 재사용 — RHO-adRP `reduce`, 신성요붕증 `correct`)
→ 이전 66개 per-disease 해시 drift 0, 총 **69개 (61 resolved + 8 suspended)**. 개념 DOI 불변(10.5281/zenodo.20755262).
THE THEME: **firewall 양끝의 폭 확장 + firewall 이 늘 함의하던 자기-감사**.

**RHO 상염색체우성 망막색소변성/adRP (RHO, brake/GOF → 간상세포 유지 axis DOWN)** — 키트의 **네 번째 안과 read**
이자 **첫 안과 단백질병증**(toxic-GOF). adRP RHO 대립유전자(P23H 가 전형, class-II 잘못접힘)는 **독성 GAIN-of-function**
으로 작용 — 잘못접힌 로돕신이 응집하여 간상세포 단백질항상성을 압도 → **HTT/TTR/SOD1 단백질병증 패턴**(과활성 병적
BRAKE, axis DOWN), 앞선 세 안과 read 의 수송/효소-LOF 패턴(RPE65 망막순환효소, RPGR 섬모수송, CHM/REP1 Rab프레닐화)
과 결정적으로 다름 — 한 망막에서 네 안과 유전자가 **네 분자기계 클래스**를 망라, RHO 가 **제거할 독성 단백질**인 첫 read.
lead `reduce` 독성 변이체 via 대립유전자특이 knockdown(**QR-1123** P23H ASO, 1/2상 NCT04123626) — `clinical`,
**솔직히 미승인**(RHO-adRP 승인약 없음, 크기 [O]) = **헌팅턴 패턴**(키트 네 번째) + 변이-비특이 `replace` ablate-and-replace
(EDIT-103, 전임상). **`direction_confidence` = cited-contested**(toxic-reduce 방향은 toxic-GOF 다수에선 깨끗하나
class-I LOF 소수에선 대립유전자-클래스 논쟁; Athanasiou 2018, Mendes 2005). γ 1.4719 chr3 3q22.1, barrier 0.54162.
dwell[DOWN] 1.05043 < 1.33264 < 1.62340. OMIM 613731. context PRPH2. file-hash 1ff8ee6a7b87.

**X-연관 신성요붕증/X-linked NDI (AVPR2, accelerator/LOF → V2R→cAMP→AQP2 수분재흡수 axis DOWN)** — 키트의 **첫
GPCR / 수용체-cAMP-신호 축**. AVPR2 는 V2 바소프레신 수용체(Gs-연관 GPCR)를 코딩 — 집합관 주세포에서 바소프레신
결합 시 cAMP→PKA→정단부 AQP2 삽입→소변농축; 질병 대립유전자는 대부분 **잘못접혀 ER 에 갇히는 missense**(수송-클래스
LOF) → 정상 바소프레신에도 V2R 신호 소실 → 집합관이 소변을 농축 못함 → axis DOWN. 키트에서 인과 노드가 효소·수송체·
채널·구조단백·분비인자가 아니라 **호르몬 수용체(GPCR)**인 첫 read. lead `correct` ER-갇힌 수용체 via 세포투과
**약리샤페론**(준-억제농도 비펩티드 V2R 길항제로 접힘 주형화·ER 배출 회복; SR49059/relcovaptan 인체 개념증명
Bernier 2006; SR121463) — `investigational`, **솔직히 미승인**(thiazide+amiloride+NSAID 는 하류 NON-lever) +
`replace`(AVPR2 유전자/기능 복원). missense-구제 한정; 방향 [F]/크기 [O]; **`direction_confidence` = clean**.
γ 1.4618 chrX Xq28, barrier 0.53421. dwell[DOWN] 1.03964 < 1.31895 < 1.60672. OMIM 304800. context AQP2, AVP.
file-hash a12ce969d0cd.

**Kearns-Sayre 증후군 — 보류(SUSPENDED): 단일 거대 mtDNA 결실.** ~16.6kb 원형 mtDNA 의 **단일 거대 결실**(4977bp
"common deletion" ND5..ATP8 가 전형, 다수 유전자를 한꺼번에 제거, 대개 산발성, 이질형질성). **세 번째 mtDNA 보류**로,
mtDNA 보류를 **점돌연변이(LHON 단백질코딩 / MELAS tRNA)에서 구조적 재배열(거대 결실)로 일반화** — 보류가 미토콘드리아-
게놈 기전에 키되 병변 유형(점 vs 구조)과 무관함을 증명. **핵 트랙이 점/코딩 병변과 구조/반복 병변(FSHD)을 모두 보류하는
것의 mtDNA 유사물**. 핵 프로모터 창 없음; 결실을 표적하는 질병변경 치료 없음(전도차단 감시·심박동기 보조). OMIM 530000.
file-hash 4c005fab8b3d. (ledger B28 / §C)

**키트 최초의 네이티브 모듈 `pipeline/direction_recovery.py` (ROADMAP II-A) — 읽기전용 방향-회수 점수판.** 상속받은
진통제 M10/M11/M5v2 와 달리 이 모듈은 디지즈 키트 **네이티브**다: 엔진이 (역할×기전)에서 약물과 무관하게 *강제한*
교정 방향이, 레지스트리에 기록된 — 독립 임상 문헌이 추구하는 — 선도 약제의 실제 axis_effect 와 일치하는지 질병별로
채점. 반증가능 주장: 선도 약제가 반대로 미는 resolved 질병이 단 하나라도 있으면 (역할×기전)→방향 사상이 깨진다.
**결과: 61/61 방향 회수**(교정축 UP 36 / DOWN 25; 직접 34 / 간접 27; 승인 52 / 임상 6 / 임상시험 3). 축·lever·
직접/간접·승인상태별 분해 + **승인약-없는 고가치 꼬리 9개** 표면화. firewall: 방향 회수 + 승인 상태만(방향 [F], 크기 [O]);
동결 산출물 위 읽기전용 → per-disease 해시 불변; 이빨 있는 self-test; M5v2 스캔 범위에 추가. frozen sha 4def995f40d5.
**ROADMAP I-D `direction_confidence`**: 질병별 신뢰도 스탬프(기본 clean — 구성상 모호하지 않음 — 레지스트리 필드로
cited-contested/ambiguous 재정의); 3개 cited-contested(RHO-adRP, α1-항트립신 두-장기-반대, Rett MECP2 양방향);
58 clean / 3 cited-contested / 0 ambiguous; 파이프라인이 무시 → analysis.json 해시 바이트동일(S2 전체 재생성 drift 0).

캐시 89 → 94 유전자(RHO, AVPR2, AQP2, PRPH2, AVP 추가). 모듈 3 → 4 재동결, drift 0. 전체 변경 정본은 `VERSION`.

---

## 0.4.1. v0.23.0 — (이전 릴리스)

v0.23.0 은 **첫 채널병증 쌍** 릴리스다 — 키트의 **첫 심장 이온채널 축**과 **첫 신경 이온채널 축**을 전압개폐
**Na 채널 거울쌍**으로 추가한다. 실제 NCBI 프로모터 DNA 에 검증한 **2개 resolved + 1개 suspended**, **엔진 변경 0**
(두 resolved lead 모두 기존 lever 재사용 — LQT3 `restrain`, Dravet `replace`) → 이전 63개 per-disease 해시
drift 0, 총 66개 (59 resolved + 7 suspended). 개념 DOI 불변(10.5281/zenodo.20755262).

**롱QT 3형/Long QT type 3 (SCN5A, channel/GOF → 심장 후기 Na 전류 axis UP)** — 키트의 **첫 심장 이온채널 축**
(HCM 의 기계적 축과 구별), **첫 채널 GAIN-of-function read**, **첫 `restrain`-채널 lever**. SCN5A GOF 가 NaV1.5
불활성화를 손상시켜 평탄기에 지속성 후기 Na 전류를 남겨 활동전위/QT 를 연장 → `restrain` 후기 Na 전류 via
**메실레틴**(승인된 후기-INa 차단 IB군 항부정맥제, LQT3 유전자특이 치료, Mazzanti 2016 JACC) — CFTR/K_ATP 의
*potentiate*-LOF-채널과 **반대 방향**. 솔직히 **유전형 의존**(메실레틴 감수성/비감수성 SCN5A 대립유전자, 방향 [F]/
크기 [O]; 고위험군은 ICD 가 주축); β차단제(LQTS 전체 1차약)는 **하류 NON-lever**(LQT3 에선 덜 효과적·심지어
유발성). KCNQ1(LQT1)/KCNH2(LQT2)는 **반대 기전의 K 채널 LOF** → **수렴이 아닌 맥락**(키트가 증후군 이름이 아니라
(유전자×기전)을 읽음을 증명). γ 1.5256 chr3 3p22.2. dwell[UP] 1.71304 < 1.92280 < 2.35543. OMIM 603830.
file-hash 9147aa8b17dd.

**드라베 증후군/Dravet (SCN1A, channel/LOF → GABA성 중간뉴런 NaV1.1 전류 axis DOWN)** — 키트의 **첫 신경
이온채널(뇌전증) 축**이자 **LQT3 의 거울**. SCN1A 반접합부족이 빠른발화 억제성 중간뉴런의 NaV1.1 을 낮춰 억제가
붕괴 → 뇌전증성 뇌병증. SCN5A 와 같은 전압개폐 Na 채널 **계열**이나 **반대** 장기(뇌 중간뉴런 vs 심장)·기전(LOF
vs GOF)·축(DOWN vs UP)·lever(replace/restore vs restrain) — **Wilson/Menkes 구리쌍의 채널 유사물**. lead 는
NaV1.1 상향조절 via **zorevunersen/STK-001**(TANGO ASO, 3상 EMPEROR) `replace`, **임상시험 단계** — **헌팅턴
패턴**(승인된 fenfluramine/cannabidiol/stiripentol 은 하류·완화적·NaV1.1 미복원 → NON-lever). axis-DOWN read 는
임상 **Na 채널 차단제 금기**(phenytoin/carbamazepine 가 드라베 악화 — 이미 결핍된 채널을 더 막아 축을 더 낮춤)를
**예측**한다. SCN1A γ 1.2450(chr2 2q24.3, AT-rich)는 키트에서 **두 번째로 낮은 γ**(DMD 1.2388 다음). dwell[DOWN]
0.81716 < 1.03669 < 1.26288. OMIM 607208. file-hash 4a049497fac9.

**MELAS — 보류(SUSPENDED): mtDNA tRNA 점돌연변이 (m.3243A>G in MT-TL1, tRNA-Leu(UUR) 유전자).** **두 번째 mtDNA
보류**로, mtDNA 보류를 **단백질코딩 Complex I 유전자(LHON: MT-ND4/ND1/ND6)에서 미토콘드리아 tRNA 유전자(MELAS)로
클래스내 일반화** — Beckwith–Wiedemann(11p15.5)이 임프린팅을 15q 밖으로 일반화한 것의 유사물(새 부류가 아니라,
mtDNA 보류가 미토콘드리아-게놈 기전에 키되 유전자 클래스(단백질코딩 vs tRNA)와 무관함을 증명). 핵 프로모터 창 없음,
이질형질성, 모계유전; 보조요법(일본 MELAS 승인 타우린 등) 존재에도 **엔진 가독성**만으로 보류. OMIM 540000.
file-hash e77853002039. (ledger B27 / §C)

캐시 84 → 89 유전자(SCN5A, SCN1A, KCNQ1, KCNH2, SCN8A 추가). 전체 변경 정본은 `VERSION`.

---

## 0.41. v0.22.0 — 무엇이 바뀌었나 (이전 릴리스)

v0.22.0 은 **개념 DOI 등록 + 질병 추가** 릴리스다. 키트가 **자체 Zenodo 개념 DOI 10.5281/zenodo.20755262**
(CC BY 4.0, ORCID 0009-0002-7535-8245)를 획득했고 **희귀병(rare/single-gene/hereditary)** 자료로 규정된다 —
모든 릴리스 버전이 이 개념 DOI 로 해상된다(VERSION·README·HANDOFF·ROADMAP·VP-SPEC DOI 레지스트리의 `disease`/`dis`
행에 적용). 실제 NCBI 프로모터 DNA 에 대해 검증한 **2개 resolved + 1개 suspended**, **엔진 변경 0** (두 resolved
lead 모두 기존 lever 재사용 — choroideremia `replace`, congenital hyperinsulinism `potentiate`) → 이전 60개
per-disease 해시 drift 0, 총 63개 (57 resolved + 6 suspended). 주제는 **방화벽 양끝의 메커니즘-부류 확장**이다.

**맥락막결손/Choroideremia(CHM, accelerator/LOF → Rab-프레닐화/소포운반 유지 axis DOWN)** — 키트의 **세 번째
안과 read** 이자 **세 번째 안과 유전자 부류**. CHM 은 REP1(Rab Escort Protein 1)을 코딩하여 Rab GTPase 를 Rab
geranylgeranyl transferase 에 제시해 프레닐화(막부착·소포운반에 필수)시키며, LOF 는 일부 Rab(특히 Rab27a)을
저-프레닐화 상태로 남긴다 — 상염색체 파라로그 REP2(CHML)가 다른 조직을 부분 보상하므로 변성이 **망막에 국한**
(RPE·광수용체·맥락막)된다. LCA2(RPE65)는 레티노이드-회로 **효소** 결핍, XLRP(RPGR)는 **섬모-운반** 결핍, 본 질환은
**Rab-프레닐화/소포운반** 결핍 — 같은 망막의 세 가지 다른 분자 기계인데 lead 교정 lever 는 모두 같은 부류, 유전자
복원이다. lead 는 망막하 AAV2-REP1 유전자치료(**timrepigene emparvovec/BIIB111**)로 CHM 을 `replace` 하지만
`clinical` 상태로 **솔직히 미승인** — 3상 STAR(Biogen, NCT03496012, 2021)가 **1차 평가변수 실패 AND 핵심 2차
평가변수 효능 미입증** → 크기는 열린 [O], cure 주장 안 함 — **헌팅턴 패턴**(키트 내 세 번째). chrX Xq21.2,
γ 1.3083, barrier 0.42791. dwell[DOWN] 0.88026 < 1.11675 < 1.36041. OMIM 303100. file-hash e0837a48f0f2.

**선천성 고인슐린혈증/Congenital hyperinsulinism(KCNJ11+ABCC8, channel/LOF → 베타세포 K_ATP 채널 전도도
axis DOWN)** — **새로운 조절분비(regulated-secretion) 이온채널 축**이자 키트의 **여섯 번째 2-원인유전자 수렴**.
KCNJ11(Kir6.2, 공극)+ABCC8(SUR1, 설포닐우레아-수용체 조절 소단위)은 ATP 감수성 K+ 채널의 두 소단위로 세포질
ATP/ADP 를 막전위에 연결하는 — 포도당-자극 인슐린 분비의 재분극 **브레이크**; 어느 소단위든 LOF 는 채널 개방을
막아 베타세포가 지속 탈분극, 포도당과 무관하게 인슐린 분비 → 고인슐린혈성 저혈당. 이는 **낭성섬유증 패턴**
(channel/LOF → axis DOWN → 채널 `potentiate`)을 **다른 채널·다른 축**으로 옮긴 것 — CF 는 상피 염화물-수송
채널(CFTR), 본 질환은 키트의 **첫 조절호르몬분비 이온채널 축**(K_ATP). 한 필수 채널의 두 소단위가 11p15.1 에
인접, **KCNJ11/Kir6.2(공극)가 더 깊은 프로모터 스위치(primary)**. lead 는 K_ATP 채널 개방제 **diazoxide
(Proglycem)** — 승인된 1차 약물을 스위치가 독립 재도출, 그리고 v0.21.0 lead 와 달리 **DIRECT** lever(표적
KCNJ11 이 primary switch). 단 정직한 한계: diazoxide 는 잔존/운반-가능 채널만 여므로, 이 두 유전자에 가장
귀속되는 형태 — 양대립 채널-null ABCC8/KCNJ11 — 은 특징적으로 **diazoxide-무반응**이라 준전절제술로 관리됨;
방향(K_ATP 전도도 복원)은 [F], 실현 반응성/크기는 [O]. KCNJ11 chr11 11p15.1, γ 1.5068, barrier 0.56761
(primary) > ABCC8 γ 1.4657, barrier 0.53707. dwell[DOWN] 1.08801 < 1.38032 < 1.68148. OMIM 256450.
file-hash 7e3606a67927.

**레베르 유전성 시신경병증/LHON** — **SUSPENDED**(미토콘드리아-게놈/mtDNA 점돌연변이). 원인은 mtDNA 점돌연변이
— 가장 흔히 MT-ND4 의 m.11778G>A(~60-80%), 그리고 MT-ND1 m.3460 / MT-ND6 m.14484 — 으로 호흡쇄 복합체 I
유전자에 있으며 **핵 단일유전자 프로모터 스위치가 아니다**. (1) 병변이 ~16.6kb 환형 **미토콘드리아** 게놈에 있어
중·경쇄 프로모터에서 다중시스트론 전사 후 가공 — MT-ND4 에 **핵형 TSS −2000..+500 프로모터 창이 없다**(키트
데이터 경로는 핵 RefSeq 프로모터만 해상); (2) 침투도가 **이형질성(heteroplasmy) 의존·불완전**; (3) 유전이
**모계**. **다섯 번째 보류 메커니즘 부류** — 이수성(Down)·임프린팅(PWS/Angelman/BWS)·반복-탈억제(FSHD/DUX4)
와 구별되며 보류 규칙이 **미토콘드리아 게놈으로 일반화**됨을 증명. **가장 날카로운 규율 지점:** LHON 은 **승인
약물이 있음에도** 보류된다 — idebenone(Raxone, EU·이스라엘·한국 등 승인; 미 FDA 우선심사 진행 중, 2026 초)
및 유전자치료 프로그램(lenadogene nolparvovec). idebenone 은 **하류**(망막신경절세포 항산화·전자운반 지원)로
작용해 mtDNA 병변을 다루지 않는다. 보류는 **엔진이 병변을 읽을 수 있는가**(엔진-가독성)에만 달렸지 치료 존재
여부가 아니다 — 헌팅턴/XLRP/choroideremia 패턴의 **역(逆)**(거기선 DNA 가독·치료 미입증, 여기선 치료 승인·
DNA 가 핵-프로모터 엔진에 비가독). OMIM 535000. file-hash 96bc957e0e09. 자세히는 `VERSION` / `HANDOFF.md` §1
/ 원장 B26·§C.

---

## 0.42. v0.21.0 — 이전 릴리스 (kept for history)

v0.21.0 은 **규율 과시(discipline-showcase) 릴리스**다. 주제는 **부정적 증거 앞에서의 정직성**: 두 resolved
read 모두 lead 가 솔직히 *깨끗한 승인 스위치-약물이 아니며*, 키트는 약을 억지로 만들어내지 않고 스위치 논리와
임상 현실 사이의 괴리를 **기록**한다. 실제 NCBI 프로모터 DNA 에 대해 검증한 **2개 resolved + 1개 suspended**:
**X-염색체 색소성 망막염(RPGR, accelerator/LOF → 광수용체 유지 axis DOWN)** — 키트의 **두 번째 안과 read**
이자 LCA2 의 레티노이드-회로 효소(RPE65)에 대한 **섬모-운반(ciliary-trafficking)** 대조. lead 는 AAV 유전자
치료 **bota-vec(botaretigene sparoparvovec)** 으로 RPGR 를 `replace` 하지만 `clinical` 상태로 **솔직히 미승인**
— 3상 LUMEOS(NCT04671433)가 **1차 평가변수 실패**, 따라서 *크기*는 열린 [O], 치료(cure)를 주장하지 않는다 —
**헌팅턴 패턴**(resolved + lead clinical-미승인). **구조적 최초: RPGR 의 γ 1.3915 가 SMN1 과 비트-동일** — 다른
좌위(chrX vs chr5)·다른 질병·다른 축 → **질병은 (역할 × 기전) read 이지, γ 숫자 자체가 아님**을 키트 내부에서
증명. **유전성 출혈성 모세혈관확장증/HHT(ENG + ACVRL1, brake/LOF → 혈관-정온 브레이크 상실 axis UP)** — **새로운
내피 TGF-β / BMP9-10-ALK1 혈관 축**, 키트의 **다섯 번째 2-원인유전자 수렴**. 이는 **보류가 아니라 다운그레이드**다:
DNA 는 읽히므로(resolved) 스위치 논리는 "브레이크를 복원하라"(investigational)고 정확히 말하지만 — **전 세계에 HHT
승인 표적 치료가 없다.** 임상 약은 브레이크를 복원하지 않는 **오프라벨 하류 항혈관신생제**(bevacizumab; pomalidomide
/ PATH-HHT)뿐이며, 표적 VEGFA 가 원인 유전자 집합 *밖*이라 mechanism_grade 가 [O] 로 강제됨 → lead 는 **간접 오프라벨
VEGFA 억제**로 귀결되고, 키트는 **괴리를 투명하게 기록**한다(스위치는 브레이크 복원을 원하지만 임상은 하류 차단만 제공).
그리고 **안면견갑상완 근이영양증/FSHD(D4Z4 반복 수축 + DUX4 탈억제)** — **네 번째 보류 메커니즘 부류**(반복-탈억제)
로, 이수성(Down)·임프린팅(PWS/Angelman/BWS)과 구별되며 보류 규칙이 반복/후성유전 탈억제로 일반화됨을 증명. **엔진
변경 0** (두 resolved lead 모두 기존 lever `replace`/`restrain` 재사용) → 이전 57개 per-disease 해시 drift 0, 총
60개 (55 resolved + 5 suspended). 새 resolved 질병의 부담 티어는 둘 다 **D = 3** (동결된 `clinical` lead 상태의
floor/cap 에 의해 강제 — 순위가 미승인 증거를 넘어 치료가능성을 과장하지 않음) + U = 5 (승인 치료 없음). 캐시 72→79
유전자. 동결 운영은 v0.20.0 모델대로: S4 자동 추가, S5 재동결(부담 순위 + indirect 인구 53→55). 자세히는 `VERSION`
/ `HANDOFF.md` §1 / 원장 B25·§C.

---

## 0.45. v0.20.0 — 이전 릴리스 (kept for history)

v0.20.0 은 **질병 추가 릴리스**다. 실제 NCBI 프로모터 DNA 에 대해 검증한 **2개 resolved + 1개 suspended**:
**결절성 경화증(TSC1+TSC2, brake/LOF → mTORC1 axis UP → everolimus/sirolimus 재도출)** — 키트의 **첫 세포내
신호전달(mTOR) 축**이자 **네 번째 2-원인유전자 수렴**; **폰 히펠–린다우병(VHL, brake/LOF → HIF-2α 안정화 axis
UP → belzutifan 재도출)** — 키트의 **첫 저산소-감지(HIF) 축**, "브레이크 상실 → 전사인자 안정화" 라는 새로운 대조;
그리고 **베크위트–비데만 증후군(11p15.5 imprinting)** — **세 번째 임프린팅 보류이자 15q11–q13 이외 첫 좌위**로,
보류 규칙이 임프린팅 *메커니즘*에 따라 작동하며 좌위를 넘어 일반화됨을 증명. **엔진 변경 0** (두 lead 모두 기존
`restrain` 재사용) → 이전 54개 per-disease 해시 drift 0, 총 57개 (53 resolved + 4 suspended), 3× 검증.
캐시 65→72 유전자. 이 릴리스는 v0.19.0 모듈 상속 이후 **첫 질병 추가**라서, 동결 운영의 본보기다: per-disease
동결(S4)은 새 해시를 **자동 추가**하고, 상속-모듈 동결(S5)은 **재동결**한다(부담-우선순위 순위와 indirect-lever
인구가 51→53 으로 정당하게 증가하므로). 모듈은 여전히 `analysis.json` 을 건드리지 않는다 — 그것이 54개 해시를
drift 0 으로 유지하는 불변식이다. 자세히는 `VERSION` / `HANDOFF.md` §1 / 원장 B24·§C.

---

## 0.5. v0.19.0 — 상속 기술 (read this second)

v0.19.0 은 **새 질병을 추가하지 않는다.** 대신 `analgesic_threshold_logic_v2_0`
(DOI 10.5281/zenodo.20733420) 의 v2.0 고유 기술 세 가지를 **상속(inherit)** 하여 키트 전체에
적용한다. 키트의 `honesty_gate.py` 는 이미 진통제 **v1.0** 의 M5/M6(금지청구 스캔 + falsifier)을
상속했으나, **v2.0 에서 추가된 세 기술은 빠져 있었다.** 이제 그것을 들여온다 — 단, 기존 54개
질병 산출물(`analysis.json`)의 해시는 **한 비트도 바뀌지 않는다**(drift 0). 새 모듈은 분석 산출물을
**읽기만** 하고 자기 자신의 동결 해시를 따로 갖는다(진통제 M10/M11/M12 가 `threshold_map` 을
읽기만 하는 것과 동일한 방식).

| 상속/네이티브 | 출처 | 무엇을 하는가 | 키트 적용 |
|---|---|---|---|
| **A. 부담가중 우선순위** (상속) | M10 `build_prioritisation.py` | 선언 가중치(B 0.40·U 0.35·D 0.25)로 **타깃이 아니라 질병**을 인용-티어로 순위; γ/barrier 는 firewall 에 따라 점수에 **섞지 않고** 구조적 맥락으로만 동반 | `pipeline/prioritise_diseases.py` — 61개 resolved 질병 순위 |
| **B. 간접-레버 정직성 게이트** (상속) | M11 `l3_honesty.py` | γ 가 포착 못 하는 기전 링크(진통제의 L3 = NGF/CGRP 수용체·네트워크)를 **[O] 인용-생물학으로 강제**, 파생([V]/[F]) 금지, fail-closed | `pipeline/indirect_lever_gate.py` — causal 유전자가 **아닌** 곳(upstream/downstream/paralog/repressor/substrate)에 작용하는 모든 lever (현재 57종) |
| **C. 강화 청구 스캐너 v2.0** (상속) | M5 v2.0 `forbidden_claim_scan.py` | **부정문 가드**("not a dose" 오탐 차단) + **self-test**(주입 위반이 안 잡히면 빌드 실패) + **신규 모듈 스캔** | `pipeline/claim_scanner_v2.py` — A·B·**D** 산출물을 스캔 |
| **D. 방향-회수 점수판** (**네이티브, v0.24.0**) | ROADMAP II-A (상속 아님) | resolved 질병별로 엔진이 (역할×기전)에서 *강제한* 방향이 독립 문헌의 선도 약제 방향과 일치하는지 채점 — 반증가능 주장; 축·lever·직접/간접·승인상태별 분해 + 승인약-없는 고가치 꼬리 표면화; 방향 [F]/크기 [O], 읽기전용 | `pipeline/direction_recovery.py` — **61/61 방향 회수**, 꼬리 9개(임상 6 + 임상시험 3); + I-D `direction_confidence`(58 clean / 3 cited-contested / 0 ambiguous) |

**진통제 M12(정밀 국소마취 맵)는 의도적으로 상속하지 않는다.** "선택적 진입 포트(TRPV1/TRPA1) ×
하전 차단제" 라는 도식은 통각수용체 약리에 고유하며 유전질환에 대응물이 없다 — 억지로 들여오면
키트의 "보류 규칙(없으니 못한다)"을 스스로 위반하게 된다. 사유는 ROADMAP §3 과 ledger 에 기록.

상속 모듈은 마스터 하니스의 **S5** 단계로 실행된다:
```bash
python3 repro/run_all.py                     # S1~S4(질병 drift 0) + S5(모듈 drift 0)
python3 repro/modules/run_modules.py         # 모듈만 단독 실행(상속 3 + 네이티브 II-A)
python3 pipeline/prioritise_diseases.py      # 부담가중 질병 순위(stdout)
python3 pipeline/direction_recovery.py       # 방향-회수 점수판(stdout) — 네이티브 II-A
```

상속의 **기존 연구사례 확대 적용 계획**은 `docs/INHERITANCE_PLAN_analgesic_v2.md` 참조.

---

## 0. 무엇이 바뀌었나 — the pivot (read this first)

**형제 작업** `disease_wp` (concept DOI **10.5281/zenodo.20763842**, CC BY 4.0)는 7,600여 희귀질환을 **수집·분류·부담순 정렬**하고 표준치료를 정리한, 재현가능한 **부담순위 + 표준치료 맥락 레이어**다(살아있는 형제 패키지). 그 분류·정리는 그것으로 충분하다.
**이 키트는 분류를 하지 않는다.** 대신:

> 실제 NCBI DNA 를 가져와 → R19 스위치로 **창발(emergence)** 시키고 →
> 질병을 그 스위치에 가해진 **섭동(perturbation)** 으로 읽고 →
> *합당한 치료 방향*만을 도출한다.

| | 형제 — `disease_wp` (부담·표준치료 맥락) | 이 키트 (this kit) |
|---|---|---|
| 단위 | 질병 카탈로그 (7,672개) | 질병 **메커니즘** (유전자 스위치) |
| 행위 | 수집·분류·부담순 정렬 | **DNA 창발 → 섭동 읽기 → 치료 추론** |
| 데이터 | 2차 요약 | **실제 NCBI 프로모터 DNA** (γ = SantaLucia 1998) |
| 산출 | 목록 | `analysis.json` (창발 + 치료 A/B + 정직성 게이트) |
| DNA 없으면 | 그래도 목록에 넣음 | **보류한다 (없으니 못한다)** — 버리지 않고 사유 기록 |

The classification work is done. This kit pulls **real DNA**, actually **emerges** the
disease-relevant switch, reads the disease as a **perturbation** of it, and reasons about
**reasonable treatment directions** — nothing more, nothing fabricated.

---

## 1. 두 갈래 치료 로직 — two treatment pathways

For each disease the kit emerges the problematic gene's promoter switch, then offers:

- **Pathway A — switch adjustment** (`pipeline/treatment_switch.py`)
  Like `analgesic_threshold_logic`: find levers that push the emergent axis **back toward
  healthy** (oppose / reduce / potentiate / restore / replace the switch). Rank by whether each
  CORRECTS or WORSENS the pathology, and by real-world approval status. Emerge the
  disease/treated/healthy **dwell** and check the ordering.

- **Pathway B — drug feasibility** (`pipeline/treatment_chem.py` + `engine/chem_toolkit.py`)
  Like `handoff_chemistry`: VP chemistry (ΔG = ΔH − TΔS at body temperature; the tetrahedral
  109.47° primitive; the Sabatier catalyst-as-matchmaker window). Reports an equilibrium
  **feasibility direction** for candidate corrections, and flags `[O]` everything it doesn't
  have a measured number for.

Both are reached **by emerging the problematic protein/cell**, exactly as directed.

---

## 2. 정직성 방화벽 — the firewall (what the kit refuses to say)

```
  DNA promoter  --γ-->  switch threshold (|h_sp|, barrier)        [V] reproducible read
  role × mechanism  -->  perturbation DIRECTION (axis up/down)     [F] forced + cited biology
  corrective lever  -->  OPPOSES pathology direction               [F] forced
  HOW FAR anything moves (magnitude, effect, dose, cure %)         [O] OPEN — never derived
```

γ reads promoter **switch STRUCTURE only** — never voltage, affinity, potency, dose, or clinical
effect. **Direction is forced and cited; magnitude is always open.** The build **fails closed**
(`pipeline/honesty_gate.py`) if that line is crossed. Nothing here is medical advice, a drug, or
a treatment recommendation for any individual. See `docs/CONSTITUTION.md`.

---

## 3. 보류 규칙 — the suspension rule ("없으니 못한다")

If a disease has **no analyzable single-gene promoter DNA** (a whole-chromosome trisomy, a large
structural/copy-number change, a polygenic trait with no single causal switch, an
epigenetic/imprinting cause), the kit does **not** force a read. It records a **SUSPENSION** with
the specific reason. Suspension is **disclosed, not dropped**; it never counts as a failure.
**Down syndrome ships suspended** as the worked example of this discipline.

---

## 4. 지금 들어있는 질병 — what's in v0.24.0 (61 RESOLVED + 8 SUSPENDED)

| slug | gene(s) | role/mech | axis | lead corrective lever (status) | status |
|---|---|---|---|---|---|
| `achondroplasia` | FGFR3 | brake/GOF | DOWN | oppose NPR2 via CNP analogue (vosoritide) — **approved** | RESOLVED |
| `cystic_fibrosis` | CFTR | channel/LOF | DOWN | potentiate CFTR (ivacaftor) — **approved** | RESOLVED |
| `phenylketonuria` | PAH | enzyme/LOF | DOWN | replace PAH (pegvaliase) + BH4 (sapropterin) — **approved** | RESOLVED |
| `sickle_cell_disease` | HBB | structural/LOF* | DOWN | oppose BCL11A → re-induce HbF (exa-cel) — **approved** | RESOLVED |
| `familial_hypercholesterolaemia` | LDLR, PCSK9 | channel/LOF + brake/GOF | DOWN | oppose PCSK9 (evolocumab / inclisiran) — **approved** | RESOLVED |
| `gaucher_disease` | GBA1 | enzyme/LOF | DOWN | replace GBA1 (enzyme replacement) + substrate reduction [B] — **approved** | RESOLVED |
| `spinal_muscular_atrophy` | SMN1 | structural/LOF | DOWN | potentiate SMN2 splicing (nusinersen / risdiplam) — **approved** | RESOLVED |
| `duchenne_muscular_dystrophy` | DMD | structural/LOF* | DOWN | replace DMD via micro-dystrophin gene transfer (delandistrogene moxeparvovec) — **approved** | RESOLVED |
| `huntington_disease` | HTT | brake/GOF* | DOWN | reduce HTT via HTT-lowering ASO (tominersen) — *clinical*; **no DMT approved** | RESOLVED |
| `rett_syndrome` | MECP2 | master_TF/LOF* | DOWN | potentiate IGF1 via trofinetide — **approved** (downstream); MECP2-restoring levers *investigational* | RESOLVED |
| `alpha1_antitrypsin_deficiency` | SERPINA1 | structural/LOF* | DOWN | replace SERPINA1 via A1AT augmentation — **approved** (two-sided; hepatic Z-polymer = distinct axis) | RESOLVED |
| `hereditary_tyrosinaemia_type_1` | FAH | brake/LOF* | **UP** | **restrain** HPD via nitisinone/NTBC — **approved** (upstream blockade) | RESOLVED |
| `wilson_disease` | ATP7B | brake/LOF* | **UP** | **restrain** copper via chelation (penicillamine/trientine) + zinc — **approved** | RESOLVED |
| `mecp2_duplication_syndrome` | MECP2 | master_TF/**GOF*** | **UP** | **restrain** MECP2 via MECP2-lowering ASO — *investigational* (mirror of Rett; **no DMT approved**) | RESOLVED |
| `transthyretin_amyloidosis` | TTR | brake/GOF* | DOWN | **reduce** TTR via silencer (patisiran/vutrisiran) + **correct** via stabiliser (tafamidis) — **approved** | RESOLVED |
| `acute_intermittent_porphyria` | HMBS | brake/LOF* | **UP** | **restrain** ALAS1 via givosiran + hemin — **approved** (upstream blockade) | RESOLVED |
| `primary_hyperoxaluria_type_1` | AGXT | brake/LOF* | **UP** | **restrain** HAO1 via lumasiran — **approved** (upstream restraint); + nedosiran (LDHA) | RESOLVED |
| `hereditary_angioedema` | SERPING1 | brake/LOF* | **UP** | **restrain** KLKB1 via plasma-kallikrein inhibitor (lanadelumab/berotralstat) — **approved**; + icatibant (BDKRB2), C1-INH replacement | RESOLVED |
| `fabry_disease` | GLA | enzyme/LOF* | DOWN | **replace** GLA via enzyme replacement (agalsidase) — **approved**; + migalastat chaperone (amenable alleles) — **approved** | RESOLVED |
| `ornithine_transcarbamylase_deficiency` | OTC | brake/LOF* | **UP** | **restrain** waste-nitrogen via scavenger (glycerol phenylbutyrate / Ammonul) — **approved**; + citrulline/arginine repletion; + restore OTC (transplant) | RESOLVED |
| `x_linked_hypophosphataemia` | PHEX | brake/LOF* | **UP** | **restrain** FGF23 via anti-FGF23 mAb (burosumab) — **approved** (hormone axis; conventional phosphate/vit-D is downstream-symptomatic, not a switch lever) | RESOLVED |
| `pompe_disease` | GAA | enzyme/LOF* | DOWN | **replace** GAA via enzyme replacement (alglucosidase / avalglucosidase alfa) — **approved**; + cipaglucosidase + miglustat chaperone co-dose — **approved** | RESOLVED |
| `hypophosphatasia` | ALPL | enzyme/LOF* | DOWN | **replace** TNSALP via bone-targeted enzyme replacement (asfotase alfa) — **approved**; + gene-therapy TNSALP restore (preclinical). Opposite bone-mineral defect to XLH; vit-D/Ca/phosphate + B6 are downstream-symptomatic, not switch levers | RESOLVED |
| `leber_congenital_amaurosis_2` | RPE65 | enzyme/LOF* | DOWN | **replace** RPE65 via subretinal AAV gene therapy (voretigene neparvovec) — **approved** (first in-vivo gene therapy in the US); + oral cis-retinoid chromophore supply (clinical). First ocular read; gene-restore IS the lead | RESOLVED |
| `hypertrophic_cardiomyopathy` | MYH7 + MYBPC3 | accel/GOF + brake/LOF* | **UP** | **restrain** the hypercontractile sarcomere via cardiac myosin inhibitor (mavacamten) — **approved**; + aficamten (clinical) + restore MYBPC3 brake (preclinical). First mechanical/contractile axis; β-blockers/CCB/disopyramide are downstream-symptomatic, not switch levers | RESOLVED |
| `familial_chylomicronaemia_syndrome` | LPL | brake/LOF* | **UP** | **restrain** APOC3 via APOC3 antisense (olezarsen) — **approved** (first FCS-specific therapy, FDA 2024); + volanesorsen (approved) + plozasiran (clinical) + LPL restore (gene therapy). Released-brake **lipid** axis (triglyceride); opposite mode to FH's LDL level-restore | RESOLVED |
| `friedreich_ataxia` | FXN | accelerator/LOF* | DOWN | potentiate NFE2L2/Nrf2 via omaveloxolone — **approved** (first DMT, FDA 2023; **downstream** — does NOT restore frataxin); + replace FXN (gene therapy, investigational) + dimethyl fumarate (clinical). Deficiency-driven neurodegeneration; GAA intron-1 repeat outside the firewall | RESOLVED |
| `congenital_leptin_deficiency` | LEP | accelerator/LOF* | DOWN | **replace** the hormone via recombinant leptin (metreleptin) — **approved**. Hormone-axis DOWN/replace — the sign-contrast to XLH's hormone-axis UP/restrain; setmelanotide (MC4R) treats the receptor-deficient siblings, not this ligand deficiency | RESOLVED |
| `hereditary_haemochromatosis_type_1` | HFE | brake/LOF* | **UP** | **restrain** the iron burden via therapeutic phlebotomy/venesection — **approved/standard**; + iron chelation (deferoxamine/deferasirox/deferiprone, approved) + restore hepcidin brake (mini-hepcidin, investigational). Second toxic-metal overload — **iron**, the contrast to Wilson's copper in both metal AND modality (physical removal vs chelating drug) | RESOLVED |
| `leptin_receptor_deficiency` | LEPR | accelerator/LOF* | DOWN | **potentiate** the downstream MC4R via setmelanotide — **approved** (receptor-bypass; the ligand-replace metreleptin is futile here and is deliberately NOT a lever); + restore LEPR (investigational). Completes the **ligand/receptor pair** with CLD: ligand-replace (CLD) vs receptor-bypass (LEPR) on one satiety cascade | RESOLVED |
| `aadc_deficiency` | DDC | enzyme/LOF* | DOWN | **replace** the deficient gene via intraputaminal AAV-DDC gene therapy (eladocagene exuparvovec) — **approved** (first US brain-delivered gene therapy, FDA 2024). Gene-restore IS the lead — the contrast to FRDA's downstream-only lead; B6/PLP cofactor + dopamine-agonists/MAO-B are downstream-symptomatic, not switch levers | RESOLVED |
| `cystinosis` | CTNS | brake/LOF* | **UP** | **restrain** the lysosomal cystine burden via cysteamine substrate-depletion — **approved**; + restore CTNS (autologous HSPC gene therapy, investigational). Fifth lysosomal-storage read but the **first small-molecule substrate-depleter** lever class (transport defect, not catabolic — vs enzyme-replacement Gaucher/Fabry/Pompe) | RESOLVED |
| `alkaptonuria` | HGD | brake/LOF* | **UP** | **restrain** HPD via nitisinone/NTBC — **approved** (EMA 2020; the **same upstream-block lever as tyrosinaemia** — one lever, two diseases, since HPD is upstream of both the HGD and FAH lesions); + restore HGD (investigational) | RESOLVED |
| `haemophilia_b` | F9 | accelerator/LOF* | DOWN | **replace** factor IX via liver-directed AAV F9-Padua gene transfer (etranacogene dezaparvovec) — **approved** (first haemophilia B gene therapy, FDA 2022); + factor IX protein replacement (recombinant/EHL) — **approved**. The kit's **first coagulation axis**; gene-restore-as-lead (extends RPE65/AADC onto haemostasis) | RESOLVED |
| `menkes_disease` | ATP7A | accelerator/LOF* | DOWN | **replace** copper downstream of the broken transporter via parenteral copper-histidine — status **`clinical`** (long-standing clinical/orphan use, NOT a conventional approval; efficacy `[O]`); + ATP7A restore (investigational). The **exact opposite-sign contrast to Wilson** — sibling copper ATPases, same metal, opposite sign AND lever (Wilson UP/chelate vs Menkes DOWN/replace) | RESOLVED |
| `sod1_amyotrophic_lateral_sclerosis` | SOD1 | brake/GOF* | DOWN | **reduce** toxic SOD1 via tofersen (SOD1 ASO) — **approved** (FDA 2023, first genetically targeted ALS therapy). Toxic-GOF "reduce the poison" pattern (HTT/TTR) carried onto **motor neurons**; the structural-LOF contrast to SMA on the same cell type | RESOLVED |
| `haemophilia_a` | F8 | accelerator/LOF* | DOWN | **mimic** the missing FVIII cofactor via emicizumab (bispecific antibody bridging FIXa–FX) — **approved**; + valoctocogene roxaparvovec (AAV F8 gene therapy, approved) + factor VIII protein replacement. Completes the **coagulation A/B pair**; introduces the kit's **first cofactor-MIMIC lever** (function without the molecule — works past anti-FVIII inhibitors) | RESOLVED |
| `lysosomal_acid_lipase_deficiency` | LIPA | enzyme/LOF* | DOWN | **replace** the deficient enzyme via recombinant LAL (sebelipase alfa) — **approved** (FDA/EMA 2015); + LIPA gene therapy (investigational). The **sixth lysosomal-storage read** but the **first on a neutral-lipid (cholesteryl-ester) substrate** — enzyme-replacement carried to a new substrate chemistry; the contrast to cystinosis's transporter substrate-depleter on the same organelle | RESOLVED |
| `cryopyrin_associated_periodic_syndrome` | NLRP3 | accelerator/GOF* | **UP** | **restrain** the over-produced IL-1β via anti-IL-1β mAb (canakinumab) — **approved** (FDA 2009); + anakinra (IL1R1 antagonist) / rilonacept (IL-1 trap), approved; + investigational NLRP3 inhibitors. The kit's **first inflammasome / autoinflammatory axis** — an IL-1 over-production contrast to HAE's bradykinin over-production (same axis-UP mode, different mediator + lever target) | RESOLVED |
| `sitosterolaemia` | ABCG5 + ABCG8 | brake/LOF* | **UP** | **restrain** the sterol-absorption route via NPC1L1 inhibitor (ezetimibe); + cholestyramine adjunct. A **new sterol-absorption axis** with a small-molecule absorption-blocker lever — the contrast to FH's LDL-receptor level axis; the kit's **second two-causal-gene convergence** (ABCG5 primary by barrier depth, after HCM) | RESOLVED |
| `deficiency_of_il1_receptor_antagonist` | IL1RN | brake/LOF | **UP** | **restrain** (net axis effect) — **anakinra** (recombinant IL-1Ra), which supplies the missing antagonist to restore the lost brake at IL1R1; + canakinumab / rilonacept — **approved**. Completes the **IL-1 axis as a PAIR with CAPS** (CAPS = IL-1 over-production / NLRP3-GOF vs DIRA = IL-1 brake-loss / IL1RN-LOF); the "one drug, two opposite lesions" record | RESOLVED |
| `hereditary_antithrombin_deficiency` | SERPINC1 | brake/LOF | **UP** | **restrain** (net axis effect) — **antithrombin concentrate** (plasma-derived / recombinant, FDA 2009) restoring the serpin brake on thrombin/factor Xa; + factor-Xa inhibitors / warfarin — **approved**. The coagulation-axis **sign-contrast to haemophilia** (DOWN/bleeding vs UP/clotting — axis complete BOTH directions); the **third serpin** read | RESOLVED |
| `cerebrotendinous_xanthomatosis` | CYP27A1 | enzyme/LOF | **DOWN** | **replace** — **chenodeoxycholic acid** (chenodiol / Ctexli, FDA 2025; CDCA-Leadiant EMA 2017) supplies the missing bile acid AND restores its own CYP7A1 feedback, suppressing the cholestanol shunt — **approved**. A **new bile-acid-synthesis axis** (the kit's 4th distinct lipid axis) | RESOLVED |
| `beta_thalassaemia` | HBB | structural/LOF | **DOWN** | **potentiate** terminal erythroid maturation — **luspatercept** (activin-receptor ligand trap, FDA 2019) — the distinctive β-thal lead; + oppose BCL11A → HbF re-induction (exa-cel, shared with sickle) + replace HBB (betibeglogene autotemcel) — **approved**. The **"same HBB locus, two lesion TYPES"** contrast to sickle cell (QUALITATIVE Glu6Val vs this QUANTITATIVE deficiency); identical γ to sickle but different hash | RESOLVED |
| `niemann_pick_disease_type_c` | NPC1 | brake/LOF | **UP** | **restrain** via substrate reduction — **miglustat** (glucosylceramide-synthase inhibitor, EMA for NPC); + arimoclomol (HSP co-inducer, `correct`, FDA 2024) — **approved**. The **seventh lysosomal read** and a trafficking/transport defect — the cargo-contrast to cystinosis (cholesterol/sphingolipid vs cystine exporter) | RESOLVED |
| `classical_homocystinuria` | CBS | enzyme/LOF | **DOWN** | **restrain** accumulated homocysteine via the alternative BHMT remethylation route — **betaine** (Cystadane, FDA 1996); + **correct** via the CBS cofactor pyridoxine/B6 (the BH4/PKU-style arm) + methionine-restricted diet — **approved**. A **new sulfur-amino-acid axis** — the metabolic contrast to PKU's aromatic axis | RESOLVED |
| `niemann_pick_disease_type_a_b` | SMPD1 | enzyme/LOF | **DOWN** | **replace** the deficient acid sphingomyelinase — **olipudase alfa** (Xenpozyme, FDA/EMA/Japan 2022) — **approved**; CNS/BBB reach held [O]. The **eighth lysosomal read**, the enzyme-catabolic contrast to NPC type C on the same eponym | RESOLVED |
| `x_linked_adrenoleukodystrophy` | ABCD1 | brake/LOF | **UP** | **restrain** (by NET) the VLCFA burden — **elivaldogene autotemcel** (Skysona, FDA 2022) + allo-HSCT (clinical) — **approved**; Lorenzo's oil demoted to a biomarker-only NON-lever. The kit's **first peroxisomal axis** (VLCFA-import defect), the import/export contrast to the lysosomal reads | RESOLVED |
| `cystinuria` | SLC3A1, SLC7A9 | brake/LOF (two-gene) | **UP** | **restrain** free urinary cystine via the thiol binder **tiopronin** (Thiola, FDA 1988) + alkalinisation — **approved**. The **third two-causal-gene convergence**, the "cystine, two transporters" contrast to cystinosis | RESOLVED |
| `tetrahydrobiopterin_deficiency` | PTS | enzyme/LOF | **DOWN** | **replace** the missing BH4 cofactor — **sapropterin** (Kuvan, FDA 2007) + monoamine arm (L-dopa+carbidopa, 5-HTP) — **approved**. The **fourth cofactor-responsive aminoacidopathy** and the "one drug, two lever roles" contrast to PKU (sapropterin `replace`s the cofactor here vs `correct`s the PAH apoenzyme in PKU) | RESOLVED |
| `familial_mediterranean_fever` | MEFV | accelerator/GOF | **UP** | **restrain** the pyrin inflammasome via **colchicine** (FMF first-line, microtubule mechanism) + IL-1 blockade (canakinumab, FDA crFMF) — **approved**. The **third autoinflammatory read** and **first on the pyrin inflammasome**, completing the CAPS/DIRA/FMF IL-1 trio | RESOLVED |
| `tuberous_sclerosis_complex` | TSC1, TSC2 | brake/LOF (two-gene) | **UP** | **restrain** the over-active mTORC1 via the mTOR inhibitor **everolimus / sirolimus** (approved for TSC SEGA / renal AML / seizures) + restore the TSC2 GAP brake (investigational) — **approved**. The kit's **first intracellular-signalling (mTOR) axis** and **fourth two-causal-gene convergence** (TSC2 primary) | RESOLVED |
| `von_hippel_lindau_disease` | VHL | brake/LOF | **UP** | **restrain** the stabilised HIF-2α via **belzutifan** (Welireg, FDA 2021) + restore pVHL HIF-degradation (investigational) — **approved**. The kit's **first hypoxia-sensing (HIF) axis** — the brake-loss → transcription-factor-stabilisation contrast to the metabolite/transport released-brake reads | RESOLVED |
| `x_linked_retinitis_pigmentosa` | RPGR | accelerator/LOF* | **DOWN** | **replace** RPGR via subretinal AAV gene transfer (**botaretigene sparoparvovec / bota-vec**) — status **`clinical`, NOT approved**: Phase 3 LUMEOS missed its primary endpoint, magnitude `[O]` — the **Huntington pattern**. The **second ocular read** (ciliary-trafficking contrast to LCA2's retinoid-cycle enzyme); **structural first — γ 1.3915 is bit-identical to SMN1, proving the disease is the (role × mechanism) read, not the γ number** | RESOLVED |
| `hereditary_haemorrhagic_telangiectasia` | ENG, ACVRL1 | brake/LOF (two-gene) | **UP** | **DOWNGRADED — no approved targeted therapy exists**: switch logic forces restore-the-brake (`restrain` ENG/ALK1, *investigational*); the only clinical agents are off-label downstream anti-angiogenics (`restrain` VEGFA — **bevacizumab**, **pomalidomide** / PATH-HHT, both INDIRECT → `[O]`, approved only for malignancy). The kit records the switch-logic↔clinic **divergence** transparently. A **new endothelial TGF-β / ALK1 vascular axis** and the **fifth two-causal-gene convergence** (ENG primary) | RESOLVED |
| `choroideremia` | CHM | accelerator/LOF* | **DOWN** | **replace** CHM via subretinal AAV2-REP1 gene transfer (**timrepigene emparvovec / BIIB111**) — status **`clinical`, NOT approved**: Phase 3 STAR missed its primary AND key secondary endpoints, magnitude `[O]` — the **Huntington pattern**. The kit's **THIRD ocular read** and **THIRD ocular gene class**: a Rab-prenylation / vesicular-trafficking (REP1) deficiency — the contrast to LCA2's retinoid-cycle enzyme (RPE65) and XLRP's ciliary-trafficking (RPGR); context gene CHML (REP2, the retina-restriction reason) | RESOLVED |
| `congenital_hyperinsulinism` | KCNJ11, ABCC8 | channel/LOF (two-gene) | **DOWN** | **potentiate** the K_ATP channel via the opener **diazoxide** (Proglycem) — **approved** first-line but **genotype-limited**: biallelic-null ABCC8/KCNJ11 forms are characteristically diazoxide-unresponsive (managed by near-total pancreatectomy), responsiveness held `[O]`; DIRECT lever (KCNJ11/Kir6.2 pore is the primary switch). The kit's **first regulated-secretion ion-channel axis** (the CF pattern on a hormone-secretion channel) and **sixth two-causal-gene convergence**; context gene GLUD1 (diazoxide-responsive non-channel contrast) | RESOLVED |
| `long_qt_syndrome_3` | SCN5A | channel/**GOF** | **UP** | **restrain** the late sodium current via **mexiletine** (late-INa-blocking class-IB antiarrhythmic) — **approved**, gene-specific for LQT3, but **genotype-dependent** (mexiletine-sensitive vs -insensitive alleles), magnitude `[O]`, ICD mainstay. The kit's **FIRST cardiac ion-channel axis**, **FIRST channel GAIN-of-function read** and **FIRST `restrain`-channel lever** (opposite of CFTR/K_ATP potentiate-LOF); β-blockers a downstream NON-lever; KCNQ1/KCNH2 (LQT1/2 K+ LOF) framed as CONTEXT, not convergence | RESOLVED |
| `dravet_syndrome` | SCN1A | channel/**LOF** | **DOWN** | **replace** (upregulate) NaV1.1 via **zorevunersen / STK-001** (TANGO ASO, Phase 3 EMPEROR) — **`investigational`, NOT approved**, magnitude `[O]` — the **Huntington pattern** (approved fenfluramine/CBD/stiripentol are downstream/palliative NON-levers). The kit's **FIRST neuronal ion-channel (epilepsy) axis** and the **MIRROR of LQT3** (same Na-channel family, opposite organ/mechanism/axis/lever — the Wilson/Menkes analogue); the axis-DOWN read **predicts** the Na-channel-blocker contraindication (phenytoin/carbamazepine worsen Dravet) | RESOLVED |
| `rho_autosomal_dominant_retinitis_pigmentosa` | RHO | brake/**GOF** | **DOWN** | **reduce** the toxic misfolded mutant via allele-specific knockdown (**QR-1123** P23H ASO, Phase 1/2) — **`clinical`, NOT approved**, magnitude `[O]` — the **Huntington pattern** + mutation-agnostic `replace` ablate-and-replace (EDIT-103, preclinical). The kit's **FOURTH ocular read** and **FIRST OCULAR PROTEINOPATHY** (the HTT/TTR/SOD1 toxic-GOF pattern on the retina — four ocular genes now span four molecular machine classes). **`direction_confidence` = cited-contested** (clean for the toxic-GOF majority, allele-class-contested for the class-I LOF minority); context PRPH2 | RESOLVED |
| `nephrogenic_diabetes_insipidus_x_linked` | AVPR2 | accelerator/**LOF** | **DOWN** | **correct** the ER-retained misfolded V2R via a cell-permeant **pharmacochaperone** (sub-inhibitory non-peptide V2R antagonist; SR49059/relcovaptan human proof-of-concept) — **`investigational`, NOT approved** (thiazide+amiloride+NSAID are downstream NON-levers) + `replace` AVPR2. The kit's **FIRST GPCR / receptor-cAMP-signalling axis** (causal node is a hormone RECEPTOR for the first time); missense-rescuable only, direction `[F]`/magnitude `[O]`; **`direction_confidence` = clean**; context AQP2, AVP | RESOLVED |
| `down_syndrome` | — | whole-chromosome aneuploidy | — | — | **SUSPENDED** |
| `prader_willi_syndrome` | — | imprinting / structural (paternal 15q11–q13) | — | — | **SUSPENDED** |
| `angelman_syndrome` | — | imprinting / structural (maternal 15q11–q13) | — | — | **SUSPENDED** |
| `beckwith_wiedemann_syndrome` | — | imprinting (11p15.5 — a 3rd imprinting hold, FIRST off 15q) | — | — | **SUSPENDED** |
| `facioscapulohumeral_muscular_dystrophy` | — | repeat-derepression (D4Z4 contraction / SMCHD1-LOF → DUX4 on 4qA — a **4th held MECHANISM class**) | — | — | **SUSPENDED** |
| `leber_hereditary_optic_neuropathy` | — | mitochondrial-genome / mtDNA point mutation (MT-ND4 m.11778G>A + MT-ND1/MT-ND6; heteroplasmy; maternal — a **5th held MECHANISM class**, suspended **despite** an approved drug) | — | — | **SUSPENDED** |
| `melas` | — | mitochondrial-genome / mtDNA point mutation (m.3243A>G in **MT-TL1**, the tRNA-Leu(UUR) **gene**; heteroplasmy; maternal — the **2nd mtDNA suspend**, generalising the mtDNA hold from protein-coding to a **tRNA** gene, the within-class analogue of how BWS generalised imprinting beyond 15q) | — | — | **SUSPENDED** |
| `kearns_sayre_syndrome` | — | mitochondrial-genome / **single large-scale mtDNA DELETION** (the 4977-bp "common deletion" ND5..ATP8 the archetype; sporadic; heteroplasmy/tissue-distribution — the **3rd mtDNA suspend**, generalising the mtDNA hold from a **POINT mutation** to a **STRUCTURAL rearrangement**, the mtDNA analogue of how the nuclear track holds both point and structural/repeat lesions) | — | — | **SUSPENDED** |

\* **coding-lesion / locus-switch reads (firewall):** sickle cell (HBB coding missense), Duchenne
(DMD frame-disrupting deletion), Huntington (HTT exon-1 CAG repeat expansion), Rett (MECP2
coding/nonsense), and the v0.4.0 additions — α1-antitrypsin (SERPINA1 Glu342Lys), tyrosinaemia
(FAH point mutations), Wilson (ATP7B point mutations), the MECP2 duplication (a copy-number
gain), transthyretin amyloidosis (TTR destabilising variants e.g. Val30Met/Val122Ile), acute
intermittent porphyria (HMBS point mutations), and the v0.6.0 additions — primary hyperoxaluria
type 1 (AGXT point mutations e.g. Gly170Arg) and hereditary angioedema (SERPING1 loss-of-function
variants) — all carry their disease lesion in the *coding* sequence or as a structural change, not in
the promoter. The v0.7.0 addition — Fabry (GLA missense/splice e.g. Gly328Arg, the IVS4+919 cardiac
variant) — is read the same way: γ reads the GLA promoter locus-switch structure while the LOF
direction is forced by biology, and because Fabry is X-linked its penetrance/severity (zygosity,
X-inactivation skewing, residual-activity %) are held `[O]`, never derived from γ (ledger B10). The
v0.8.0 additions are read the same way — OTC (coding/splice, e.g. the late-onset Arg40His allele;
X-linked Xp11.4, so penetrance held `[O]` by B10), PHEX (loss-of-function variants/deletions across
the gene; X-linked dominant Xp22.11), and Pompe/GAA (coding/splice, e.g. the common late-onset
IVS1 c.-32-13T>G leaky-splice allele; **autosomal** recessive 17q25.3, so no X-linked caveat at all).
The v0.9.0 additions are read the same way — hypophosphatasia (ALPL coding e.g. Glu191Lys/Ala116Thr;
1p36.12; both recessive and dominant via residual activity / dominant-negative dimerisation),
RPE65 Leber congenital amaurosis (coding/splice e.g. Pro25Leu/Tyr368His; recessive 1p31.3), and
hypertrophic cardiomyopathy (MYH7 missense e.g. Arg403Gln; MYBPC3 truncating/splice e.g. the South
Asian founder deletion; both dominant, 14q11.2 / 11p11.2) — and HCM is the first **two-causal-gene**
resolved read where both switches perturb the **same** axis (the mechanical/contractile axis) UP, with
the deeper switch (MYH7) picked as primary by barrier depth.
The v0.10.0 additions are read the same way — familial chylomicronaemia (LPL loss-of-function
variants/large deletions, 8p21.3, autosomal recessive), Friedreich ataxia (the pathogenic FXN GAA-repeat
expansion sits in **intron 1** — structural, outside the promoter window, noted not modelled; 9q21.11,
recessive), and congenital leptin deficiency (LEP frameshift/nonsense e.g. the Δ133G founder allele,
7q32.1, recessive) — FCS is the kit's first **lipid released-brake** read (the LPL brake on plasma
triglyceride), Friedreich is a **deficiency-driven** neurodegeneration (contrast to the HTT/TTR
toxic-aggregate reads), and leptin deficiency closes the **hormone-axis-DOWN** sign-contrast against
XLH's hormone-axis-UP.
The v0.11.0 additions are read the same way — hereditary haemochromatosis type 1 (HFE coding lesions
C282Y/H63D, 6p22.2, autosomal recessive — outside the promoter window, noted not modelled), leptin-receptor
deficiency (LEPR loss-of-function/truncating variants, 1p31.3, recessive), and AADC deficiency (the DDC
founder splice variant IVS6+4A>T and other coding/splice lesions, 7p12.2, recessive — intronic splice
lesion outside the promoter window) — HFE is the kit's **second toxic-metal overload** (iron, the Wilson/copper
contrast in both metal and modality), LEPR closes the **ligand/receptor pair** with congenital leptin deficiency
(receptor-bypass vs ligand-replace on one cascade), and AADC is a **gene-restore-IS-the-lead** neurodegeneration
(the contrast to FRDA's downstream-only lead). γ reads each promoter locus-switch structure only; the LOF/axis
direction is forced by biology and every magnitude is held `[O]`.
The v0.12.0 additions are read the same way — cystinosis (CTNS structural/coding lesions, the common
57-kb founder deletion and truncating/missense alleles, 17p13.2, autosomal recessive — outside the
promoter window, noted not modelled), alkaptonuria (HGD coding e.g. p.Met368Val, 3q13.33, recessive),
and haemophilia B (F9 coding/nonsense, Xq27.1, X-linked recessive — penetrance held `[O]` by B10; the
'haemophilia B Leyden' F9-promoter androgen-responsive variants are a separate regulatory class, noted
not modelled) — cystinosis is the kit's **fifth lysosomal-storage read** but the first with a
**small-molecule substrate-depleter** lever (a transport defect, not a catabolic enzyme deficiency),
alkaptonuria demonstrates **one upstream-block lever (nitisinone / HPD) serving two diseases** (it and
tyrosinaemia, because HPD lies upstream of both the HGD and FAH lesions), and haemophilia B opens the
kit's **first coagulation-cascade axis** as a gene-restore-as-lead read (extending RPE65/AADC onto
haemostasis).
In each, γ reads the **locus switch structure** and the axis **direction** is forced
by the cited GOF/LOF biology; the promoter firewall is respected — γ never encodes the coding
lesion's magnitude (always `[O]`). Notes make this explicit per gene in the registry.

The v0.13.0 additions follow the same firewall, with **one small additive engine change** — a new
cofactor-`mimic` lever (a different molecule performing the missing element's function; emicizumab
bridging FIXa–FX, distinct from `replace`/`correct`), purely additive so every prior frozen hash
stays drift 0. Menkes disease (ATP7A coding/splice lesions, Xq21.1, X-linked — outside the promoter
window) is the **exact opposite-sign copper contrast to Wilson**: sibling P-type copper ATPases, the
same metal but the opposite sign AND lever (Wilson copper-overload/chelate vs Menkes copper-deficiency/
replace), with the copper-histidine approval status held honestly at `clinical`. SOD1-ALS (SOD1 coding
variants, 21q22.11, dominant toxic-GOF — Bruijn 1998) carries the toxic-aggregate "**reduce the poison**"
pattern (HTT/TTR) onto **motor neurons** via tofersen, the structural-LOF contrast to SMA on the same
cell type. Haemophilia A (F8 coding/inversion lesions, Xq28, X-linked — penetrance `[O]`) **completes
the coagulation A/B pair** with haemophilia B (F8 cofactor vs F9 protease of the same intrinsic-tenase
step) and introduces the cofactor-mimic lever class.

The v0.14.0 additions follow the same firewall with **no engine change at all** — every new disease
reuses an existing lever, so all 39 prior frozen hashes stay drift 0. Lysosomal acid lipase deficiency
(LIPA coding/splice lesions, e.g. the common exon-8 splice-junction E8SJM allele, 10q23.31, autosomal
recessive — outside the promoter window) is the kit's **sixth lysosomal-storage read** but the first on
a **neutral-lipid (cholesteryl-ester) substrate**, re-deriving the enzyme-`replace` lever (sebelipase
alfa) on a new substrate chemistry — the contrast to cystinosis's transporter substrate-depleter on the
same organelle. CAPS (NLRP3 gain-of-function missense, e.g. the recurrent p.Arg260Trp, 1q44, autosomal
dominant) is the kit's **first inflammasome / autoinflammatory axis**, re-deriving IL-1 blockade
(canakinumab, `restrain`-coded by net axis effect on the over-produced IL-1β) — an IL-1 over-production
contrast to HAE's bradykinin over-production. Sitosterolaemia (ABCG5 / ABCG8 loss-of-function variants,
both at 2p21 in a head-to-head locus — outside the promoter window, recessive) is the kit's **second
two-causal-gene convergence** after HCM (ABCG5 picked primary by barrier depth) and opens a **new
sterol-absorption axis**, re-deriving ezetimibe (`restrain` the NPC1L1 absorption route) — the
sterol-absorption contrast to FH's LDL-receptor level axis. γ reads each promoter locus-switch structure
only; the LOF/GOF and axis direction are forced by biology and every magnitude is held `[O]`.

The v0.15.0 additions likewise follow the same firewall with **no engine change at all** — every new
disease reuses an existing lever (`restrain`, `replace`), so all 42 prior frozen hashes stay drift 0 (45
total). DIRA (IL1RN null/truncating loss-of-function, e.g. the recurrent 2q14.1 genomic deletion, recessive
— outside the promoter window) makes the **inflammasome / IL-1 axis a matched PAIR with CAPS** — DIRA is
**loss of the IL-1 brake** (IL1RN-LOF) vs CAPS's IL-1β **over-production** (NLRP3-GOF) — re-deriving
**anakinra** (recombinant IL-1Ra, `restrain` by net axis effect, supplying the missing antagonist to restore
the brake at IL1R1), the elegant "one drug (anakinra), two opposite IL-1 lesions" record. Hereditary
antithrombin deficiency (SERPINC1 reactive-site / heparin-binding missense + null variants, 1q25.1, dominant
thrombophilia — outside the promoter window) **completes the coagulation axis in BOTH directions** — a
clotting-axis-**UP** (a missing **anti**-coagulant serpin brake → thrombosis), the exact sign-contrast to
haemophilia's bleeding-axis-**DOWN** — and is the **third serpin** read (after A1AT level-DOWN and HAE
bradykinin-UP), re-deriving **antithrombin concentrate** (`restrain` by net axis effect; the heparin caveat —
heparin acts *through* antithrombin — recorded). Cerebrotendinous xanthomatosis (CYP27A1 missense/nonsense/
splice, 2q35, recessive — outside the promoter window) opens a **new bile-acid-synthesis axis** (the kit's
**fourth distinct lipid axis**, after LDL-level / sterol-absorption / lysosomal-catabolism), re-deriving
**chenodeoxycholic acid** (chenodiol/Ctexli, FDA 2025; the `replace` lever — supplies the missing bile acid
*and* restores its own CYP7A1 feedback, suppressing the cholestanol shunt; statins/LDL apheresis are
downstream NON-levers). γ reads each promoter locus-switch structure only; the LOF and axis direction are
forced by biology and every magnitude is held `[O]`.

The v0.16.0 additions likewise follow the same firewall with **no engine change at all** — every new
disease reuses an existing lever (`potentiate`, `oppose`, `replace`, `restrain`, `correct`), so all 45 prior
frozen hashes stay drift 0 (48 total). β-thalassaemia (HBB quantitative β+/β0 loss-of-function — promoter/
splice/nonsense lesions, 11p15.4, recessive — a magnitude question outside the promoter window) **completes
the haemoglobinopathy pair on ONE HBB locus by lesion TYPE**: sickle cell is a QUALITATIVE HBB defect
(Glu6Val → HbS polymerises), β-thalassaemia is a QUANTITATIVE one (too little normal β-globin → ineffective
erythropoiesis) — one gene, two lesion types — re-deriving the distinctive `potentiate`-maturation lead
**luspatercept** (FDA 2019, not a sickle therapy) plus shared HbF re-induction (oppose BCL11A) and HBB gene
addition; its γ is **identical to the sickle-cell read** (same locus, 1.2779) yet its hash differs, a clean
demonstration that the kit keys on the disease perturbation rather than the locus. Niemann-Pick type C (NPC1
coding/missense, e.g. p.Ile1061Thr, 18q11.2, recessive — outside the promoter window) is the kit's **seventh
lysosomal read** but a **trafficking/transport** defect — a lost cholesterol/sphingolipid EXPORT brake →
lysosomal load UP — re-deriving substrate-reduction **miglustat** (`restrain`) with arimoclomol (`correct`,
FDA 2024); the contrast both to the enzyme-replacement lysosomal reads and to **cystinosis on a different
cargo** (cystine vs cholesterol/sphingolipid export). Classical homocystinuria (CBS missense, the
B6-responsive p.Ile278Thr / non-responsive p.Gly307Ser, 21q22.3, recessive — outside the promoter window)
opens a **new sulfur-amino-acid axis** (transsulfuration throughput DOWN, homocysteine accumulates), the
contrast to PKU's aromatic amino-acid axis, re-deriving **betaine** (`restrain` via the alternative BHMT
remethylation route, bypassing CBS) with a **pyridoxine/B6 cofactor `correct`** arm (the BH4/PKU-style
cofactor restore) — no approved CBS enzyme-replacement is asserted. γ reads each promoter locus-switch
structure only; the LOF and axis direction are forced by biology and every magnitude is held `[O]`.

The v0.17.0 additions likewise follow the same firewall with **no engine change at all** — both new
diseases reuse an existing lever (`replace`, `restrain`), so all 48 prior frozen hashes stay drift 0
(51 total). **Niemann-Pick disease type A/B** (SMPD1 enzyme/LOF — acid-sphingomyelinase deficiency,
11p15.4, recessive) is the kit's **eighth lysosomal read** and the **enzyme-catabolic contrast to
Niemann-Pick type C** on the very same eponym: type A/B is a sphingomyelin-hydrolysing ENZYME deficiency
corrected by enzyme replacement — **olipudase alfa** (Xenpozyme, FDA/EMA/Japan 2022, `replace`) — whereas
type C is a cholesterol-TRANSPORT defect corrected by substrate reduction, so one disease name resolves to
two utterly different switch reads; the CNS / blood-brain-barrier reach of the systemic enzyme is honestly
held `[O]`. **X-linked adrenoleukodystrophy** (ABCD1 brake/LOF — peroxisomal VLCFA-import failure, Xq28,
X-linked) opens the kit's **first peroxisomal axis** (every prior storage read was lysosomal): the lost
β-oxidation 'brake' lets very-long-chain fatty acids accumulate (axis UP), re-deriving **elivaldogene
autotemcel** (Skysona, FDA 2022; gene-addition lead coded `restrain` by net axis effect) with allogeneic
HSCT held `clinical` — an IMPORT-defect contrast to the lysosomal EXPORT reads, with Lorenzo's oil correctly
demoted to a biomarker-only NON-lever and the notorious genotype-phenotype unpredictability held `[O]`.
**Cystinuria** (SLC3A1 + SLC7A9 brake/LOF — the two obligate subunits of the renal rBAT/b0,+AT cystine
transporter, 2p21 / 19q13.11, recessive) is the kit's **third two-causal-gene convergence**: lost cystine
reabsorption lets stone-forming urinary cystine accumulate (axis UP, deeper SLC7A9 primary), re-deriving the
thiol cystine-binder **tiopronin** (Thiola, FDA 1988, `restrain`) with urinary-alkalinisation adjuncts — the
"cystine, two transporters" parallel-thiol contrast to **cystinosis** (same amino acid, but apical renal
transporter vs lysosomal exporter, and a different compartment). γ reads each promoter locus-switch structure
only; the LOF and axis direction are forced by biology and every magnitude is held `[O]`.

The v0.18.0 additions likewise follow the same firewall with **no engine change at all** — the two new
resolved diseases reuse an existing lever (`replace`, `restrain`), so all 51 prior frozen hashes stay drift 0
(54 total). **Tetrahydrobiopterin (BH4) deficiency** (PTS enzyme/LOF — 6-pyruvoyltetrahydropterin synthase,
the committed de-novo BH4-synthesis step, 11q23.1, recessive) is the kit's **fourth cofactor-responsive
aminoacidopathy** and the elegant **"one drug, two lever roles"** contrast to PKU: BH4 is the obligate cofactor
of phenylalanine, tyrosine AND tryptophan hydroxylase, so its loss yields the **same accumulating metabolite as
PKU** (phenylalanine) PLUS the dopamine/serotonin depletion PKU never causes — and the SAME drug, **sapropterin**
(synthetic BH4, Kuvan, FDA 2007), reads as a `replace`-the-missing-cofactor arm here but a `correct`/chaperone-
of-the-PAH-apoenzyme arm in PKU, the identical molecule resolving to a different lever depending on which node
the disease perturbs; a monoamine-replacement arm (L-dopa + carbidopa, 5-HTP) PKU does not need is added.
**Familial Mediterranean fever** (MEFV accelerator/GOF — pyrin, the pyrin-inflammasome sensor, B30.2/SPRY
functional gain-of-function, 16p13.3, classically recessive) is the kit's **third autoinflammatory read** and
the **first on the PYRIN inflammasome** — a second, distinct inflammasome SENSOR after NLRP3, completing the
**CAPS/DIRA/FMF IL-1 trio** (NLRP3 over-production + IL1RN brake-loss + pyrin over-activation) — re-deriving the
iconic **colchicine** (`restrain` via a CYTOSKELETAL/microtubule suppression of inflammasome assembly NOT used in
CAPS or DIRA, still mapping to restrain by net axis effect → no new lever) with IL-1 blockade (canakinumab,
FDA-approved for colchicine-resistant FMF; anakinra) second-line. And **Angelman syndrome** (UBE3A — loss of the
**maternally**-expressed allele in 15q11–q13, by maternal deletion / paternal UPD / imprinting-centre defect /
~10% maternal point mutation) is held **SUSPENDED** as the **reciprocal imprinting hold to Prader-Willi**:
Prader-Willi is loss of the **paternal** genes of the **same** region, Angelman the **maternal** UBE3A, so the
kit now suspends the same 15q11–q13 locus from BOTH parental origins — demonstrating the suspension rule keys on
the imprinting MECHANISM, independent of parent-of-origin. γ reads each promoter locus-switch structure only;
the LOF/GOF and axis direction are forced by biology and every magnitude is held `[O]`.

Tier-2 specifics: **Huntington** is read as a dominant *toxic gain-of-function* (an over-active
pathological brake on striatal-neuron homeostasis), and the kit honestly reports that no
disease-modifying therapy is yet approved — the corrective lever (lower mutant HTT) is clinical/
investigational. **Rett** is **dosage-sensitive in both directions** (too little MeCP2 → Rett;
too much → MECP2 duplication syndrome), so it nearly approaches suspension; it resolves with the
narrow-dosage caveat recorded, and the one approved drug (trofinetide) is correctly flagged as
acting *downstream* (IGF-1/synaptic maturation) rather than restoring the MeCP2 switch.

**Axis-UP class (new in v0.4.0).** v0.2.0–v0.3.0 modelled only *axis-DOWN* diseases (the disease
lowers a beneficial output — loss-of-function or an over-active brake). v0.4.0 makes the dwell
engine **axis-aware** so it also handles *gain-of-toxicity* and *dosage-excess* diseases, where the
disease **over-shoots** the axis and the corrective lever **restrains** it back down. Three of the
new four are axis-UP and exercise the previously-unused `restrain` lever: **tyrosinaemia** (FAH is a
released brake on toxic fumarylacetoacetate/succinylacetone → the kit re-derives the counter-intuitive
approved drug **nitisinone**, which blocks the *upstream* HPD step rather than restoring FAH);
**Wilson** (ATP7B is a released brake on copper → **chelation/zinc** remove or block copper); and
**MECP2 duplication syndrome** (MeCP2 over-dosage), the **mirror of Rett on the same cached MECP2
locus** — Rett lowers MeCP2 (axis DOWN, dwell *below* healthy), the duplication raises it (axis UP,
dwell *above* the same healthy value): one gene, both dosage directions, both firewalled. The locked
dwell form γ^1.5/(K+brake) is unchanged and all 12 prior frozen hashes stay drift 0.

Each resolved disease emerged from real NCBI promoter DNA, with the pathology direction forced
by cited GOF/LOF biology, a ranked corrective-lever map, a dwell-ordering check, and ≥1 named
falsifier. The logic **independently re-derives the approved (or lead clinical) lever** in every
case (vosoritide for achondroplasia; PCSK9 inhibitors for FH; enzyme replacement for Gaucher;
SMN2 splicing modifiers for SMA; BCL11A/HbF re-induction for sickle cell; micro-dystrophin transfer
for Duchenne; HTT-lowering for Huntington; trofinetide for Rett; A1AT augmentation for AATD;
**nitisinone** for tyrosinaemia; **chelation** for Wilson; MeCP2-lowering for the MECP2 duplication;
**patisiran/tafamidis** for transthyretin amyloidosis; **givosiran** for acute porphyria;
**nitrogen scavengers** for OTC deficiency; **burosumab** for X-linked hypophosphataemia; **enzyme
replacement** for Pompe; **asfotase alfa** for hypophosphatasia; **voretigene neparvovec** for
RPE65 Leber congenital amaurosis; **mavacamten** for hypertrophic cardiomyopathy)
— a sanity check, not a coincidence. The **two suspensions are of different kinds** (whole-chromosome
aneuploidy vs an imprinting/structural cause), demonstrating the "없으니 못한다" rule on more than one
failure mode.

---

## 5. 실행법 — how to run (fully offline)

From the package root:

```bash
python3 repro/run_all.py            # engine self-test + emerge+treat all + gates + determinism freeze
```

Runs **offline** on the bundled NCBI promoter cache (`fetch/cache/`). It re-derives every γ,
emerges every disease, runs both treatment pathways, passes the honesty gates, and verifies the
result hashes are **bit-identical** across runs (drift 0).

Single disease, or add network for a new gene:

```bash
python3 pipeline/analyze_disease.py achondroplasia --offline   # one disease, full JSON to stdout
python3 pipeline/analyze_disease.py --all --offline            # all, summary lines
python3 fetch/ncbi_gene_promoter.py SOX9                       # live NCBI fetch (network) → caches γ
```

---

## 6. 구조 — layout

```
engine/        vendored VP engine (self-contained, no external paths)
  gamma_lib_v10.py, key_pipeline_full.py, dna_interpreter.py   γ + A4 DNA read
  vp_neuro_engine.py, organism/core.py                          R19 switch substrate
  emergence_engine.py, param_db.json                            relay-ODE gene-network emergence
  chem_toolkit.py                                               VP chemistry (ΔG, Sabatier, geometry)
fetch/         NCBI eutils promoter fetcher + bundled offline cache
pipeline/      emerge_disease · treatment_switch (A) · treatment_chem (B) · honesty_gate · analyze_disease
               prioritise_diseases · indirect_lever_gate · claim_scanner_v2   ← v0.19.0 inherited (analgesic v2.0)
diseases/      _registry.json + per-disease analysis.json (the shipped artifacts)
repro/         run_all.py (master harness, S1–S5) + engine_selftest.py + expected_sha256.json
  modules/     run_modules.py + expected/ (the 3 inherited-module outputs) ; expected_modules_sha256.json
docs/          CONSTITUTION · VP_SPEC_v1_8 · IRREPRODUCIBILITY_LEDGER · INHERITANCE_PLAN_analgesic_v2
HANDOFF.md     ← next session starts here
ROADMAP.md     emergence-first plan + how to add a disease
```

---

## 7. 등급 — grading

`[V]` verified reproducible · `[F]` forced (locked rule + cited biology) · `[O]` open ·
`[CAL]` external calibrated input. Every `[O]` item is collected in
`docs/IRREPRODUCIBILITY_LEDGER.md`. Bit-reproducible; fail-closed gates; falsifier per disease.

**License:** CC BY 4.0. Reuse — including commercial reuse by pharmaceutical companies — is
encouraged. The point is to lower cost and broaden the search for better treatments.
