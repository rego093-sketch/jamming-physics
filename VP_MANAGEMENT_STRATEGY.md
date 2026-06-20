# VP 통합 관리 전략 (VP MANAGEMENT STRATEGY) v2.1
### 부제: 25-패키지 통합본 — repo = 소스의 결정론·멱등 함수 (구 v1.0 + 실측 인벤토리 흡수)

> **위치**: 최종 업로드(홈페이지 반영용) 압축 파일의 루트에 동봉되는 **상시 관리 정본**.
> **v1.0 → v2.0 변경 요지**: ① "증분 병합(3줄 unzip 덮어쓰기)"을 **주 경로에서 폴백으로 강등**하고, **"통으로 결정론 재생성"을 정상 운영의 기본 경로로 승격**. ② 그 안전 근거인 **멱등(idempotent) 불변식**·**authored/derived 분리**·**lockfile(동적 상태 SSOT)**를 신설. ③ 실측 인벤토리에서 드러난 **이질 레이아웃**(dna `dna/` 루트, disease_wp `code/`+`data/`)·**대용량 바이너리**(disease_wp 149.6MB)·**패키지별 사이트 가구 충돌**을 규칙으로 못박음. ④ SEO 크롤 예산을 지키는 **content-derived `lastmod` / no-wall-clock** 불변식 추가.
> **v2.0 → v2.1 변경**: registry를 **노드표(`nodes.csv`) + 간선표(`seam_edges.csv`)로 정규화**(메시 그래프를 정규화된 관계형 정본으로). **"한 곳 저작·두 갈래 투영"** 원칙 — 횡단 간선은 **중앙 `seam_edges.csv` 한 곳에서만 저작** → ① 렌더 내부 링크(forward + reverse back-link)와 ② 패키지 `seams.json`으로 **투영**(파생물). back-link은 **역방향 계산**(저장 아님). **6개 메시 무결성 게이트**(외래키·통제어휘·중복/자기루프·층 비순환·투영 일치·역투영 일치)를 §4.5·Phase C에 명문화.
> **역할 분담**
> - 이 문서 = 전체(25 패키지·3계층·운영 케이던스)의 **관리 전략**(상시·조직·운영).
> - `VP-SPEC v1.8` = **세션 단위** HTML 변환·게이트 표준(per-session 기술 규범).
> - `VP_BUILD_PROCEDURE v2.1` = 이 전략을 실행 단계로 푼 **빌드 절차서**.
> - 본 문서는 구 `VP_FRAMEWORK_MAP`을 흡수·단일화한다(구 MAP 폐기).
> **충돌 시**: 세션 단위 기술 사안은 VP-SPEC 0장 헌법(C1–C4) 우선, 조직·운영 사안은 본 문서, 단계 절차는 BUILD_PROCEDURE.
> **언어**: 관리 문서는 한국어. **모든 백서·산출물(HTML/PDF)은 영어**.

---

## 0. 한 문단 그림 (단일 전제)

하나의 전제 — **진공 = jammed 탄성 고체**(R19 이중우물 스위치 + FitzHugh–Nagumo 이완 진동자) — 에서 물리와 생물을 모두 유도한다. 단일 기질이 DNA 유전자·뉴런·모든 장기/루프/시계를 *재창발*한다. 패키지는 **물리 클래스·시간 축**으로 분해되고 서로 **seam(이음매) 변수로만** 연결된다(SSOT). 모든 정량은 *측정 입력(잠금·인용)* 또는 *유도*이며 **목표에 맞춰 고르지 않는다(no-tuning)**. 등급은 정직하게 `[F]강제 / [V]시뮬검증 / [L]측정 / [O]개방(사유 명시)`.

---

## 0.5 재생성 불변식 — "통으로"가 안전한 이유 (v2.0 핵심)

> **단일 원칙: `vp-site/` repo는 손으로 누적 편집하는 자산이 아니라, 소스의 결정론적·멱등 함수의 출력이다.**
>
> ```
> vp-site/  =  build_site( {25개 패키지 소스} , registry(정적 계약) , 직전 lockfile )
> ```
>
> 이 함수는 두 성질을 만족해야 한다(게이트로 강제):
> - **결정론(determinism)**: 같은 입력 → **byte-identical** 출력. 동일 입력으로 2회 빌드 → 전체 트리 sha256 동일.
> - **멱등(idempotence)**: 변경되지 않은 패키지는 재생성해도 **출력 바이트가 변하지 않는다**. 따라서 mind 하나만 올려도 git diff에는 **mind 폴더 + 그 파생물만** 뜨고, 나머지 24개는 변화 0.

**왜 이것이 "최상"인가 (사용자 질문에 대한 직답)**
- **유지보수**: 누적 수작업 편집의 표류(drift)가 원천 차단된다. repo가 곧 소스의 사진이므로, "지금 mind 몇 버전이 떠 있나"는 lockfile 한 줄로 답해진다.
- **GitHub**: "통으로" 재생성해도 변경분만 커밋되므로 git 히스토리가 더럽지 않고, 텍스트 외 바이너리를 밖으로 빼므로 repo가 가볍다(§8). 한 repo → 한 배포.
- **구글 SEO**: 슬러그(=URL) 동결 + content-derived `lastmod`(§11) 덕분에, "통으로" 재생성이 **변경된 URL의 lastmod만 갱신**한다. 구글은 바뀐 페이지만 재크롤한다 → 크롤 예산 낭비·랭킹 흔들림 없음. 통으로 바꿔도 SEO가 깨지지 않는 결정적 장치다.

**결론(운영 기본값)**: 정상 업그레이드는 **"통으로 재생성"이 기본**이다. 증분 부분 패치는 *파생 영향 반경이 증명 가능하게 0일 때만* 허용하는 폴백이다(§10). 즉 사용자의 직관("간단하면 부분, 여러 번이면 통으로")을 더 안전한 기준으로 정밀화한다: **"간단하다"의 정의 = 파생층 의존이 0인 편집**. 그 증명 자체가 일이므로, 기본은 통으로다.

---

## 1. 현 상황 — 생물 중심 25 패키지 (실측 인벤토리 반영)

- **총 25개. 생물 관련 19개 — 무게중심은 생물**, 물리 6개는 그 아래 심층 기질.
- 구성: 물리 토대 **6** · 교량(DNA·neuro·mind) **3** · 기계 동역학 장기 **7** · 통합 항상성 **3** · 시간/감각 **3** · 진통 레버 **1** · 질병 SSOT **2**.
- **실측에서 확인된 정제 포인트(v2.0 신규)**:
  - **버전은 본 문서가 고정하지 않는다.** 업로드 시점 실측만 봐도 mind=v1.49, immune=v0.20, digestive=v0.16, circulatory=v0.7, reproductive=v0.7.1 등으로 **이미 문서·기억보다 앞서 있다.** 현재 버전·SHA·DOI의 SSOT는 **lockfile**(§4.6)이며, 본 문서·registry는 *정적 계약*만 들고 포인터로 연결한다(드리프트 방지).
  - **내부 레이아웃이 비균일**: `neuro·mind·physics`는 `docs/`+`repro/`+`tools/` 표준, 그러나 **dna는 콘텐츠 루트가 `dna/`**, **disease_wp는 `docs/`+`code/`+`data/`+`methodology/`**. → 흡수는 균일성을 가정하지 못하고 **패키지별 어댑터**(§ BUILD_PROCEDURE Phase B)로 정규화한다.
  - **대용량/바이너리 실재**: `disease_wp`가 149.6MB(Orphanet `en_product1.xml` 53MB + `en_product4.xml` 49MB + `inscope_esummary.jsonl.gz` 18MB), `integumentary`는 `paper/`에 `.tex`+`.pdf` 동봉. → 이 구체 대상들은 **repo 밖(Zenodo)** 로 빠진다(§8).
  - **패키지가 자기 사이트 가구를 들고 있음**: mind만 봐도 `sitemap.xml`·`llms-full.txt`·`css`를 자체 보유 → 통합 시 충돌·중복. **흡수 시 패키지 레벨 사이트 가구는 폐기**하고 통합층 단일본만 발행(§3.5·§ BUILD_PROCEDURE Phase B).
  - 질병 트랙은 **KIT(재현 엔진) + WP(사례 dossier) 2개로 분리** 확정. **진통(analgesic) 횡단 치료 레버** 추가. 신규 패키지는 **모두 개념 DOI 발급 완료**(§4). 구 MAP "DOI는 TBD"는 무효.

---

## 2. 3계층 아키텍처 (관리 불변식 — VP-SPEC §2 산출 3계층)

| 계층 | 위치 | 역할 | 상태 |
|---|---|---|---|
| **검색층** | `jamming-physics.org` HTML(`docs/`) | 색인·랭킹·링크 표면 (구글 SEO + Scholar + 생성형 검색/RAG) | 항상 canonical |
| **검증층** | GitHub repo(`repro/`) | 코드·재현 데이터 열람·실행 | 압축 해제, 게시 제외 |
| **인용·보존층** | Zenodo | 버전 동결 PDF + repro zip + 대용량 데이터 + **패키지별 개념 DOI** | 변경 불가 스냅샷 |

- 단일 repo `vp-site/` = **단일 진실 원천**. 단, **그 진실은 "함수의 출력"이지 "수작업 누적물"이 아니다**(§0.5). Pages 게시 루트 = `docs/`만. `repro/`는 게시 제외 → 색인 오염 0.

---

## 3. 단일 repo 통합 원칙 ("통으로" = 한 repo, 25 폴더)

- **통으로 관리 = 하나의 `vp-site/` repo.** 25 패키지는 그 안의 `docs/{paper_id}/` + `repro/{paper_id}/` 폴더.
- 이것이 **구글 + GitHub 복안을 극대화**한다:
  - **검색/RAG**: 횡단 링크 그물망(§5·VP-SPEC §10)이 위상 권위(topical authority)를 만들려면 25개가 *같은 도메인*에서 상호 링크해야 한다. 분산 사이트는 내부 링크 자산을 흩뜨려 더 나쁘다. RAG는 구절 단위 인용이므로 answer-first 구절이 한 사이트에 모여야 인용된다.
  - **GitHub**: 한 repo → Pages(`/docs`) → 한 배포; GitHub→Zenodo 웹훅으로 통째 동결.
- **"통으로"와 "25개 단위"는 모순이 아니라 층위가 다른 같은 것**: 한 repo(통) 안의 25 폴더(단위). v2.0은 여기에 한 줄을 더한다 — **그 repo는 매번 소스로부터 재생성되는 함수의 출력**이라는 것(§0.5).

---

## 3.5 authored vs derived 분리 (v2.0 핵심 — 안전한 재생성의 축)

> "통으로 재생성"이 안전한 유일한 이유는, **무엇이 손으로 쓴 것이고 무엇이 기계가 만든 것인지가 깔끔히 갈리기 때문**이다. 재생성은 derived만 다시 만든다. authored는 패키지 업그레이드로만 바뀐다.

| 구분 | 무엇 | 언제 바뀌나 | 비고 |
|---|---|---|---|
| **AUTHORED (패키지별)** | `docs/{id}/*.html` 본문·구조, `repro/{id}/*`, `tools/{id}/*` | **그 패키지를 업그레이드할 때만** | 패키지 소스 zip이 이 부분의 SSOT |
| **DERIVED (통합층, 매 빌드 재생성)** | 최상위 `index.html`, `sitemap.xml`, `robots.txt`, `llms.txt`/`llms-full.txt`, 허브 상단·`concepts/` 횡단 내부링크 주입, 페이지별 JSON-LD, Scholar Highwire 태그, `_meta.json`, **패키지 `seams.json`(메시 자족 선언, 파생)**, `lockfile` | **매 빌드** (멱등) | nodes+edges+lockfile만으로 24개 본문 없이 재생성 가능 |

**핵심 따름정리**: DERIVED 통합층은 **registry(의존 간선) + lockfile(상태) + 바뀐 패키지 본문**의 함수다. 즉 mind 하나를 갱신할 때 **나머지 24개 본문을 로드하지 않아도** 통합층 전체(인덱스·사이트맵·횡단링크·JSON-LD)를 일관 재생성할 수 있다. registry가 다른 24개의 *압축 표현*이기 때문이다(§9). → "통으로 일관성"과 "슬라이스 로드"가 충돌하지 않는다.

**한 곳 저작·두 갈래 투영(메시)**: 횡단 간선은 **중앙 `seam_edges.csv`(§4.5) 한 곳에서만 저작**하고, 빌드가 두 갈래로 투영한다 — (1) **렌더 링크**(from 페이지의 forward `<a>` + to의 `concepts/` reverse back-link, SEO 표면), (2) **패키지 `seams.json`**(자족 발행용 파생물). back-link은 `to`로 **역방향 계산**해 얻으며 손으로 쓰지 않는다(사실당 진실 하나). 간선을 두 곳에서 저작하지 않는다 — 패키지 `seams.json`은 투영이지 **절대 그 반대가 아니다**.

**수치 주입의 멱등성**: 정본 HTML 안의 수치는 표시 슬롯(`<span data-ssot="key">…</span>`)에 결정론 모듈이 **그 자리에만** 다시 써넣는다. HTML 구조를 reflow하지 않으므로, 값이 같으면 재생성 후 바이트가 동일하다(C1 + 멱등 양립).

---

## 4. 패키지 레지스트리 — 정적 계약 (25행, AI 세션의 그물망 인덱스)

> 이 표가 `registry/nodes.csv`의 **노드표** 정본이다(=정적 계약). 여기엔 *거의 안 바뀌는 것*만 둔다: `paper_id`·`code`·title·**개념 DOI**·계층·etiology 소유. **횡단 간선은 이 표가 아니라 §4.5 `seam_edges.csv`(간선표)가 정본**이고, *자주 바뀌는 상태*(현재 버전·content SHA·version DOI·lastmod)는 §4.6 `integrated_versions.lock.csv`(lockfile)가 정본 — **3파일 분리로 드리프트를 막는다**(노드=정적·간선=정적·상태=동적).
> `paper_id` = 깨끗한 ASCII 슬러그(= URL, **영구 동결**, §7·§11). DOI는 **개념 DOI**(최신본으로 해상).
> 아래 표의 `seam(유도/간선)` 열은 **사람용 요약**이며, **기계 정본은 §4.5 seam_edges.csv**다(이 표를 파싱하지 않는다).

| paper_id | code | 정식 제목(영) | 개념 DOI | 계층 | etiology 소유 | seam(유도/간선) |
|---|---|---|---|---|---|---|
| physics | phy | The Vacuum as a Jammed Elastic Solid (VP Theory) | 10.5281/zenodo.17932566 | 토대 | — | 기반(foundation) |
| fluid-dynamics | flu | The Configured Continuum | 10.5281/zenodo.17972568 | 토대 | — | physics(jamming) |
| cosmology | cos | Vacuum-Inflow Cosmology | 10.5281/zenodo.20568874 | 토대 | — | physics(inflow) |
| geodynamics | geo | Jamming–Unjamming Geodynamics | 10.5281/zenodo.17978934 | 토대 | — | physics + geochronology(수렴) |
| geochronology | chr | Cross-Chronometer Accuracy Limit | 10.5281/zenodo.20568673 | 토대(방법) | — | 방법론 |
| chemistry | chm | VP Chemistry & Electromagnetism | 10.5281/zenodo.20680540 | 토대 | — | physics(jamming) |
| dna | dna | 4D DNA Blueprint | 10.5281/zenodo.20471407 | 교량(형태 SSOT) | — | physics(jamming); **모든 신체가 인용** |
| neuro | neu | Neural Emergence Chain | 10.5281/zenodo.17979015 | 교량(프리미티브 제공) | 동역학 | physics(자체 사슬); **FHN/R19/CPG 제공** |
| mind | mnd | Felt Cognition | 10.5281/zenodo.20694404 | 교량(felt 층) | — | neuro(인용, 일방); **의존 싱크(leaf)** |
| cardioresp | car | Cardiorespiratory (진동자+제어) | 10.5281/zenodo.20755371 | 기계 동역학 | 동역학(폐암·RSA·Cheyne-Stokes) | DNA(γ) + neuro |
| circulatory | cir | Circulatory (흐름+청소) | 10.5281/zenodo.20754354 | 기계 동역학 | 동역학(신·간세포암) | DNA(γ) |
| digestive | dig | Digestive (느린수송+대사) | 10.5281/zenodo.20755319 | 기계 동역학 | 동역학(위·대장·췌장암) | DNA(γ) |
| musculoskeletal | msk | Musculoskeletal (구조·역학부하) | 10.5281/zenodo.20755760 | 기계 동역학 | 동역학(골육종) | DNA(γ) + **analgesic(레버 상속)** |
| immune_hematologic | imm | Immune / Hematologic (집단-역치·클론) | 10.5281/zenodo.20755280 | 기계 동역학 | 동역학(백혈병·림프종) + 면역회피=발암 변조 | DNA(γ) |
| integumentary | itg | Integumentary (장벽·외부자극) | 10.5281/zenodo.20754541 | 기계 동역학 | 동역학(흑색종/SCC, UV) | DNA(γ) |
| reproductive_endocrine | rep | Reproductive / Endocrine (호르몬주기·생식세포) | 10.5281/zenodo.20754657 | 기계 동역학 | 동역학(유방·자궁경부·전립선암) | DNA(γ) |
| homeostasis_thermometabolic | thm | Thermometabolic Homeostasis (열+에너지·겨울잠) | 10.5281/zenodo.20756934 | 통합 항상성 | 루프(T2당뇨·비만·대사증후군) | 형제 seam 폐합 |
| homeostasis_hemodynamic | hem | Hemodynamic Homeostasis (압력/용적, MAP 루프) | 10.5281/zenodo.20756801 | 통합 항상성 | 루프(본태성 고혈압·만성 심부전) | 형제 seam 폐합 |
| homeostasis_ionic | ion | Ionic Homeostasis (미네랄·산염기) | 10.5281/zenodo.20755910 | 통합 항상성 | 루프(골다공증·산염기·전해질·신결석) | 형제 seam 폐합 |
| circadian | cyc | Circadian (~24h 결합 진동자) | 10.5281/zenodo.20755413 | 시간 | 루프(일주기 장애·교대근무암 IARC 2A) | **모든 setpoint를 gating** |
| aging_senescence | age | Aging / Senescence (쇠퇴 capstone) | 10.5281/zenodo.20756155 | 시간(capstone) | 위험 승수(노화 = 전 발암 위험승수) | 전 패키지 setpoint 표류 |
| sensory_organ | sen | Sensory Organs (기기 물리 + R19 변환) | 10.5281/zenodo.20755154 | 감각 | 동역학(백내장·녹내장·황반변성 등) | DNA(γ); 광학/음향=고전물리(정직) |
| analgesic_threshold | anl | Analgesic Threshold Logic (3-레버 L1/L2/L3) | 10.5281/zenodo.20733420 | 횡단 치료 레버 | 치료 레버(통증 역치) | **형제(근골격 등)가 상속** |
| disease_wp | dis | Systemic Genetic & Rare Disease Mechanisms — Cases | 10.5281/zenodo.20763842 | 질병 SSOT(사례) | 유전자-키(Marfan·DMD·Gaucher·PKU·CF·낫적혈구) | 유전자→기전; 기계 패키지가 교차참조 |
| disease_kit | dkt | Rare Disease Reproduction KIT (재현 엔진) | 10.5281/zenodo.20755262 | 질병 SSOT(재현) | 유전자-키(재현 엔진) | `disease_wp`의 재현 도구 |

> 토대 6 + 교량 3 = **9 (VP-SPEC §2 발행 정본, paper_id/code/DOI LOCK)**. 나머지 16은 생물 신규.
> 신규 16종 code 약칭은 **제안값**, 저자 최종 LOCK 대기(변경 시 이 표만 수정).

---

## 4.5 seam 간선표 — 메시 그래프 정본 (v2.1 신규)

> 파일: `registry/seam_edges.csv`. **전 패키지 간 횡단 관계의 단일 저작 정본**(= "지도"). AI 세션이 `nodes.csv`와 함께 로드하는 그물망 인덱스. 패키지별 `seams.json`은 이 파일의 *투영(생성물)*이며 **절대 그 반대가 아니다**(한 곳 저작).

**스키마 (유향 간선, 1행 = 1간선)**

| 열 | 의미 |
|---|---|
| `from` | 관계 동사의 **주어** 패키지(의존/인용/작용하는 쪽). forward 링크가 이 페이지에 렌더 |
| `to` | 관계 동사의 **목적어** 패키지(제공/피작용하는 쪽). reverse back-link이 이 페이지에 렌더 |
| `relation` | 통제 어휘(아래 enum 중 하나) |
| `to_anchor` | (선택) `to` 내부 특정 concept/섹션 deep-link. 기본 = `to` 허브 index |
| `anchor_text` | (선택) 링크 표시 텍스트(SEO 앵커). 기본 = relation + to-title에서 유도 |
| `grade` | (선택) seam의 정직 등급 `[F]/[V]/[L]/[O]` |

**방향 규약**: `from → to` = "from이 to에 대해 relation을 행한다"(from=주어, to=목적어). 예: `cardioresp → dna (cites_gamma)` = cardioresp이 dna의 γ를 인용. forward 링크는 from 페이지에("→ to"), reverse back-link은 to 페이지에("← from") 렌더 — **둘 다 이 한 행의 함수**.

**저장은 한 방향, back-link은 계산**: 간선은 한 방향(주어→목적어)만 저장한다. "누가 X를 인용하나"(back-link)는 `to=X`로 **역방향 계산**해 얻으며 손으로 쓰지 않는다(사실당 진실 하나; 양방향 저장은 드리프트). 대칭 관계(`converges_with`)도 한 행만 저장하고 양쪽에 상호 렌더.

**팬아웃은 행으로 전개(와일드카드 금지)**: circadian이 전 패키지 setpoint를 gating하면 *대상마다 1행*(`circadian → cardioresp (gates_setpoint)`, …). 와일드카드는 그래프를 가리고 투영 게이트 ⑤를 모호하게 하므로 금지.

**통제 어휘 (relation enum — 현재 멤버)**

| relation | from(주어) → to(목적어) 의미 | 예 |
|---|---|---|
| `derives_from` | from이 to(물리 토대)에서 유도 | fluid-dynamics → physics; dna → physics; neuro → physics |
| `converges_with` | 두 토대가 수렴(대칭, 1행) | geodynamics → geochronology |
| `cites_gamma` | from이 to(dna)의 γ(promoter ΔG)를 인용 | cardioresp → dna; integumentary → dna |
| `uses_primitive` | from이 to(neuro)의 FHN/R19/CPG 프리미티브를 사용 | cardioresp → neuro |
| `cites` | from이 to를 일방 인용 | mind → neuro |
| `inherits_lever` | from이 to(analgesic)의 3-레버를 상속 | musculoskeletal → analgesic |
| `gene_key_import` | from(기계/항상성)이 to(disease_wp)의 유전자-키 파라미터를 import | reproductive_endocrine → disease_wp |
| `seam_closure` | from(항상성)이 형제 to의 seam을 폐합 | homeostasis_ionic → cardioresp |
| `gates_setpoint` | from(circadian)이 to의 setpoint를 gating | circadian → cardioresp |
| `risk_multiplier` | from(aging)이 to의 위험을 승수 | aging_senescence → cardioresp |
| `reproduction_tool` | from(disease_kit)이 to(disease_wp)의 재현 엔진 | disease_kit → disease_wp |

> physics는 별도 relation이 아니라 **다수 `derives_from`의 to(in-degree 허브)** 로서 토대 루트가 된다. `gene_key_import`의 **reverse 투영**이 disease_wp 측 "export(소비처)" 관계를 표현하므로 export를 별도 행으로 저장하지 않는다(§5 ② 양방향 계약 = 1행 + reverse 투영).

**두 갈래 투영 (seam_edges.csv 단일 정본의 함수)**
- **투영 1 — 렌더 링크(SEO 표면)**: 각 간선 → from 허브 상단 forward `<a>`(VP-SPEC §10 1문장 유도 링크) + to의 `concepts/` reverse back-link. 구글·RAG·사용자가 보는 그래프.
- **투영 2 — 패키지 자족 선언(Zenodo)**: 각 패키지의 incoming+outgoing 간선을 추출 → `docs/{paper_id}/seams.json`. 패키지를 Zenodo로 따로 발행해도 메시 내 위치가 자족적으로 보이게 함(파생물, 정본 아님). 형식:
  ```json
  { "paper_id": "cardioresp",
    "depends_on": [ {"to":"dna","relation":"cites_gamma"}, {"to":"neuro","relation":"uses_primitive"} ],
    "cited_by":  []
  }
  ```
  (`cited_by`는 `to=cardioresp`로 역방향 계산해 채운다 — 저장 아님.)

**무결성 게이트 (6)**: seam_edges.csv는 빌드 시 6개 게이트로 검증된다 — ① 외래키(from·to ∈ nodes), ② 통제 어휘, ③ 중복·자기루프 0, ④ 층 비순환(`derives_from` 부분그래프), ⑤ 투영 일치(forward: 간선 ↔ 렌더 링크 1:1), ⑥ 역투영 일치(back-link ↔ 역방향 계산). 정의·판정은 BUILD_PROCEDURE Phase C 종료 게이트.

---

## 4.6 lockfile — 동적 상태 SSOT (v2.1: §4.5 → §4.6 이동)

> 파일: `registry/integrated_versions.lock.csv`. **현재 무엇이 통합되어 떠 있는가**의 단일 진실. 매 빌드에서 `build_site.py`가 갱신한다. 사람이 손으로 고치지 않는다.

| 열 | 의미 |
|---|---|
| `paper_id` | registry와 1:1 |
| `integrated_version` | 현재 통합된 패키지 버전(예: `v1.49`). 소스 파일명에서 추출하되 **슬러그·URL과 무관** |
| `content_sha256` | 그 패키지 정본의 **2×sha256**(아래 정의). lastmod·version DOI 등 *휘발 필드는 공란 처리 후* 해시 |
| `zenodo_version_doi` | 마지막으로 발행된 **버전** DOI(개념 DOI 아님) |
| `lastmod` | 마지막 *실질* 변경 ISO 날짜. `content_sha256`가 직전과 같으면 직전 값을 **그대로 이월**(§11) |
| `ingest_adapter` | 흡수 정규화 프로필(`standard` / `dna-root` / `disease-code-data` 등) |
| `notes` | `[O]` 사유, 대용량 오프로드 메모 등 |

**content_sha256 정의**: `docs/{paper_id}/**` + `repro/{paper_id}/**`의 *정본 바이트*를, 경로 사전순으로 이어 붙여 2회 sha256. 단 `lastmod`/`dateModified`/`build_id` 슬롯은 해시 전에 공란화(자기참조 방지). → **이 값이 바뀌었을 때만** lastmod 갱신·Zenodo 새 버전이 트리거된다(§10 델타 버저닝).

**build_id 규칙**: 어떤 "빌드 식별자"도 **벽시계 시각이 아니라 입력의 해시**로 만든다(`build_id = sha256(전체 트리)`). → no-op 빌드는 build_id가 같아 git diff가 0(§11).

---

## 5. 의존성·소유권 그물망 (충돌 방지의 핵심)

> **분할 축은 "신체 부위"가 아니라 "병인(etiology) 클래스"다.** 부위로 나누면 충돌한다(신장·심장은 여러 패키지가 함께 건드린다). **무엇이 그 병을 설명하는 과학 기계인가**로 나눈다.

| 소유자 | 병인 클래스 | 설명 기계 |
|---|---|---|
| **disease_wp / disease_kit** | 단일유전자·희귀·유전 (유전자-키) | 유전자 → 분자기전 → primary-system 분류 + 정직 burden order |
| **기계 동역학 7 + 감각 1** | 후천·다인자·흔한 (동역학-키) | 발암물질 → R19 장벽↓ → Kramers 교차 / setpoint 동역학 실패 |
| **통합 항상성/시간 3 (+circadian·aging)** | 루프 조절이상 (단일 장기 아님) | 형제 seam에서 방어 setpoint 폐합 실패(attractor-shift) |

**핵심 한 줄**: `disease_wp` = *유전자가 정의하는* 병 / 기계·항상성 = *동역학이 정의하는* 병. 같은 R19·Kramers 커널, 한쪽은 셀-레벨 유전자 병변, 한쪽은 시스템-레벨 setpoint 표류.

**겹침 tie-break**: ① 단일유전자·희귀 → `disease_wp`. ② 흔한 후천성 + 단일유전자 아형(가족성 HCM·MODY·BRCA·Lynch) → 기계/항상성이 "흔한 병+동역학"을 소유, `disease_wp`는 아형을 명명·export, **양방향 교차참조**. ③ 발암 암(폐암·흑색종 등) → 기계 패키지(절대 disease 아님); 유전성 암 증후군(Li-Fraumeni·VHL 등) → `disease_wp`.

**합성(seam)**: `disease_wp`가 유전자-병변 파라미터(예: MODY=GCK setpoint)를 **소유** → 기계/항상성 패키지가 **유전자-키로 import**해 전신 궤적 계산. 물리적 병합 없이 계약으로 연결.

**핵심 허브**: DNA = 모든 신체가 인용하는 **형태/정체성 SSOT**. neuro = **공유 FHN/R19/CPG 프리미티브 제공자**. mind = felt 층(**의존 싱크** — 아무도 mind를 import하지 않음 → 잦은 갱신의 blast-radius 최소, §10 worked example). analgesic = **횡단 치료 레버**(형제 상속).

**이 그물망의 기계 정본 = §4.5 `seam_edges.csv`**(유향 간선표). 위 소유권·tie-break·합성 관계는 모두 그 간선으로 인코딩되고, 빌드가 렌더 링크 + 패키지 `seams.json`으로 투영한다. 양방향 교차참조(예: `gene_key_import`)도 **1행 저장 + reverse 투영**으로 실현 — back-link은 손으로 쓰지 않고 역방향 계산한다(§4.5).

---

## 6. 정본 = 재현성 투영 (위치가 달라도 SHA가 묶는다)

- 정본은 `docs/` HTML 하나(C2). 수치는 `tools/`의 결정론 모듈로 **표시 슬롯에 멱등 재생성**(2×sha256, §3.5). 게이트가 정본 HTML 표시값 ↔ 재생성값 **0 드리프트** 강제(C1).
- **수치는 손으로 고치지 않고 항상 재생성** → docs와 repro가 어긋날 수 없다.
- 무거운 산출물(PDF·대용량 데이터)이 Zenodo에 있어도, **정체성은 폴더가 아니라 해시**다: docs가 SHA를 인용하고 산출물이 곧 그 SHA이며 version DOI가 그 동결본을 가리킨다.

---

## 7. 명명 · URL · 인코딩 규칙 (실측 병리 확인 → 영구 동결로 격상)

- `paper_id` = **깨끗한 ASCII 슬러그**(= URL), **한 번 정하면 영구 동결**(§11의 SEO 불변식). **DOI·한글 라벨은 폴더명·경로에 박지 않고** `_meta.json`/registry의 **필드**로 둔다.
- **실측 근거**: 현 업로드 폴더명이 `…_10.5281zenodo.20471407/…`처럼 **DOI 슬래시가 제거**돼 있고 한글이 CP949라 타 OS·웹서버에서 mojibake가 난다. 또 `… (1).zip`·버전 문자열이 파일명에 박혀 있다. 슬러그 동결 규칙이 이 셋(URL 불안정·DOI 슬래시 손실·CP949 깨짐·버전/중복 오염)을 **동시 해소**한다.
- 흡수 시 소스 파일명의 버전·`(1)`은 **버린다**. 버전은 lockfile의 `integrated_version` 필드로만 기록한다.

---

## 8. GitHub · Zenodo 한도 규칙 (바이너리는 repo 밖 — 구체 대상 명시)

- 파일당 HTML **≤300KB**, DOM **≤3,000 노드**(VP-SPEC §8). GitHub 파일당 하드 한도 100MB.
- **repo에서 빠지는 구체 대상(실측)**:
  - `disease_wp`의 외부 데이터 덤프 — Orphanet `en_product1.xml`(53MB)·`en_product4.xml`(49MB)·`inscope_esummary.jsonl.gz`(18MB) 등. 단일 패키지가 149.6MB → 이대로 커밋하면 repo가 폭증. **→ Zenodo 데이터 레코드로 분리**, `repro/disease_wp/README`에서 DOI 링크. repo에는 *그 데이터의 sha256과 다운로드 스크립트*만 남긴다.
  - `integumentary`의 `paper/*.tex` + `*.pdf`(백서) — **repo 비동봉**(C2: 정본은 docs HTML). PDF는 Zenodo 백서로, .tex는 제거(필요 시 on-demand 추출).
  - 모든 패키지의 `.tex`·`txt/` TeX 본문 소스 — 제거(VP-SPEC C2).
- 패키지별 개념 DOI = 동결 스냅샷. GitHub→Zenodo 웹훅 = repo 릴리스 아카이브.
- **결과: repo는 텍스트만 → 1GB 권장선 한참 아래**(통으로여도 가볍다). 실측 텍스트 총량(데이터 제외)은 패키지당 1~21MB 수준.

---

## 9. AI 세션 운영 (슬라이스 — "통으로 일관성"과 양립)

- **세션 로드 = `VP-SPEC` + `VP_BUILD_PROCEDURE` + `registry/nodes.csv`(노드표) + `registry/seam_edges.csv`(간선표=지도) + `registry/…lock.csv`(상태) + 바뀐 패키지 본문 + 해당 `tools/`.** **나머지 24개 본문은 로드하지 않는다.**
- 근거(§3.5 따름정리): DERIVED 통합층(인덱스·사이트맵·횡단링크·`seams.json`·JSON-LD·lockfile)은 **nodes+edges+lockfile의 함수**이므로(횡단 링크는 `seam_edges.csv` 간선의 순수 함수), 다른 24개의 *압축 표현*만으로 전체 일관 재생성이 가능하다. → "통으로 바꾼다"가 "전부 로드한다"를 뜻하지 않는다.
- 규율: `LOCK → Derive → Gate`, `SEED=19`, `2×sha256`, `no-tuning`, 정직 등급 `[F]/[V]/[L]/[O]`, `[O]` 사유 명시. 본문 무변경(편집 허용 = head · answer · abstract · claim-strip · vp-card · 내부링크 · JSON-LD).

---

## 10. 운영 케이던스 (지속 업그레이드 — v2.0: 통으로 재생성 기본)

> **기본 경로 = 통으로 결정론 재생성.** 부분 패치는 폴백(§10.C).

### 10.A 정상 업그레이드 (PRIMARY — 통으로 재생성)
1. 저자가 새 패키지 zip을 교체 투입(예: `mind_vp_site_v1_49…` → `mind_vp_site_v1_65…`).
2. AI 세션에 §9 슬라이스를 건네고 `build_site.py` 재실행 → `vp-site/` 재생성 + lockfile 갱신.
3. **diff 리뷰**: `git add -A && git status`. **기대 diff = 바뀐 패키지 폴더 + 그 파생물(인덱스 카드·사이트맵 lastmod·횡단링크·registry/lockfile 행)만.** 그 외 폴더가 바뀌었으면 **멱등 위반 → FAIL**(원인: 비결정론 또는 벽시계 시각 유입). 수정 전 push 금지.
4. 커밋 `"regen: {paper_id} {old}→{new} (gate PASS)"` → push → Pages 자동 배포.
5. **Zenodo 델타 버저닝**: lockfile에서 `content_sha256`가 바뀐 패키지**만** 그 **개념 DOI**로 새 버전 발행 → version DOI를 lockfile에 기입. (바뀌지 않은 24개는 재발행하지 않는다 — 멱등 덕분에 가능.)

### 10.B mind 워크드 예시 (사용자 시나리오)
mind은 **의존 싱크**(§5)다. 아무도 mind를 import하지 않으므로 v1.49→v1.65 통으로 재생성의 영향 반경은:
`docs/mind/**` 교체 + `index.html`의 mind 카드 + `sitemap.xml`의 mind URL `lastmod` + mind↔neuro 횡단링크(타깃 URL 불변이라 텍스트만) + registry/lockfile의 mind 행. **나머지 24개 byte-identical.** → 가장 싸고 안전한 통으로 케이스. mind은 7.6MB·텍스트only·.tex/PDF/대용량 없음(실측)이라 한도 걱정도 없다.

### 10.C 부분 패치 (FALLBACK — 파생 영향 0일 때만)
- **허용 조건(엄격)**: 그 편집이 DERIVED 층에 의존이 *증명 가능하게 0*일 때만. 예: claim-strip의 깨진 외부 href 하나 교정처럼, 사이트맵·llms·answer-snippet·JSON-LD·registry 어디에도 미러되지 않는 필드.
- 본문 텍스트·수치·제목·설명을 건드리면 파생물(answer/abstract/llms-full/JSON-LD description/sitemap)이 따라 바뀌어야 하므로 **부분 패치 금지 → 통으로 재생성**.
- 즉 사용자의 "간단하면 부분"은 유효하되, **"간단"의 정의를 "파생 의존 0"으로 못박는다.** 증명이 일이면 그냥 통으로.

### 10.D 공통
- 버전마다 **4문서 SSOT**(CHANGELOG · MASTER_MANUAL · COMPLETION_LEDGER · HANDOVER) 유지. 단일 zip 반환(파편화 금지).
- **연구→집필 게이트**: `build_docs.py`는 `research_gate` all_green(결정론 2×sha256 + 스트레스 배터리 전체 PASS) 및 `PHASE=writing` 전에는 집필 거부.

---

## 11. SEO 보호 불변식 (v2.0 신규 — "통으로"가 랭킹을 안 깨는 장치)

> 통으로 재생성이 구글에 "전부 바뀌었다"로 읽히면 크롤 예산이 낭비되고 랭킹이 흔들린다. 아래 불변식이 그걸 막는다 — 이게 "GitHub·SEO 둘 다 만족"의 SEO 쪽 핵심이다.

1. **슬러그(=URL) 영구 동결**: `docs/{paper_id}/…` 경로는 한 번 정하면 안 바뀐다. → 링크 자산·피인용·구글 인덱스가 재생성에도 보존(§7).
2. **content-derived `lastmod`**: 사이트맵 `lastmod`와 JSON-LD `dateModified`는 **벽시계가 아니라 패키지 `content_sha256`의 변화 날짜**(§4.6)에서 나온다. → mind만 바뀐 빌드는 mind URL의 lastmod만 갱신, 구글은 mind만 재크롤.
3. **no-wall-clock in artifacts**: 생성되는 어떤 파일에도 `now()`를 박지 않는다. build_id=입력 해시. → no-op 빌드 diff 0, 스푸리어스 재크롤·스푸리어스 Zenodo 버전 방지.
4. **canonical 안정**: 각 페이지 `<link rel="canonical">`는 동결 슬러그 URL. 재생성에도 불변.
5. **검증층 비색인**: `repro/`는 게시 제외(Pages=`/docs`만) → `/repro/` 404, 색인 오염 0(§ BUILD_PROCEDURE Phase F).
6. **answer-first + 자체완결 구절**: `<p class="answer">`(40~60단어)·`aside.vp-card`·단락 ≤3문장 → RAG/생성형 검색 인용 표면(VP-SPEC 검색 게이트).
7. **구조화 데이터**: ScholarlyArticle/DefinedTerm + `sameAs`(ORCID·DOI), `WebSite`+`Person`+`CollectionPage`(홈), Scholar Highwire 5종(`citation_pdf_url`=Zenodo PDF 직링크).
8. **robots 7봇**(Googlebot·Bingbot·OAI-SearchBot·GPTBot·PerplexityBot·ClaudeBot·Google-Extended) + `sitemap.xml` + `llms.txt`(<5KB).

---

## 12. CI / 결정론 검증 (v2.0 신규 — 권장)

- **GitHub Action(권장)**: push마다 ① `build_site.py`를 컨테이너에서 재실행, ② 산출 트리를 커밋 트리와 비교해 **diff 0 단언**(결정론 위반 시 CI FAIL), ③ `gate.py` 전 게이트 + 링크체커 실행. → 사람 손 없이 "repo=함수 출력" 불변식을 강제. 솔로+AI 워크플로에 적합(무료·무인).
- **로컬 결정론 게이트**: 동일 입력 2회 빌드 → 전체 트리 sha256 동일(§0.5). 불일치 = 비결정론 소스 추적.

---

## 13. 롤백 (v2.0 신규)

- **repo**: 통으로 재생성이 잘못됐으면 `git revert`(또는 직전 커밋 체크아웃)로 즉시 복구. repo가 함수 출력이라 상태가 깨끗하다.
- **Zenodo**: 발행된 version DOI는 불변(되돌릴 수 없음). 개념 DOI는 *최신 발행본*으로 해상하므로, 잘못된 버전을 이미 발행했다면 **수정본을 새 버전으로 재발행**해 개념 DOI가 올바른 본을 가리키게 한다. lockfile의 `zenodo_version_doi`를 그에 맞춰 갱신.
- **lastmod 주의**: 롤백으로 content가 이전 상태로 돌아가면 `content_sha256`도 이전 값이 되어 lastmod가 자동 정합된다(§11.2).

---

## 부록 A. 남은 큰 일 (아키텍처 외 — 설계 차원)

1. **교차-패키지 라이브 배선**: seam은 *선언된 계약*일 뿐, 형제 출력을 읽는 결합 러너 미구현. 다계 현상(대사증후군 클러스터 등)은 결합 실행해야 창발. `disease_wp`의 유전자-키 export(§5)도 이 미배선 계약의 한 사례. (단, **DERIVED 횡단 링크 자체는 registry 간선의 함수로 이미 자동화**된다 — 미배선은 *수치 결합 실행*에 한정.)
2. **SSOT 드리프트 가드**: 각 패키지가 `inherited/vp_substrate.py`·VP-SPEC를 vendoring → **neuro 원본과 byte-identical 유지 강제 가드** 필요. v2.0의 결정론·CI 게이트가 이 가드의 자연스러운 거처(빌드 시 vendored 사본 ↔ neuro 원본 해시 대조).
3. **이질 레이아웃 어댑터 정착**: dna(`dna/` 루트)·disease_wp(`code/`+`data/`)·integumentary(`paper/`) 등 비표준 패키지를 흡수하는 정규화 프로필을 `ingest_adapter`로 lockfile에 명시·고정(§4.6·§ BUILD_PROCEDURE Phase B).
4. **대용량 오프로드 정착**: disease_wp Orphanet XML 등 → Zenodo 데이터 레코드 + repo 내 sha256/다운로드 스크립트 패턴 표준화(§8).
5. **사이트 편입 잔여**: 신규 16종 `docs/` 사이트 편입 + Scholar 태그 + Zenodo 역링크 진행(BUILD_PROCEDURE 참조).

— 끝 (VP MANAGEMENT STRATEGY v2.1) —
