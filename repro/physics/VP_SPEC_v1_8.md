# VP 사이트 변환 작업표준서 (VP-SPEC) v1.8 — 정본 HTML · 재현성 헌법 · AI-검색 수용성

> jamming-physics.org 의 9개 백서(physics·fluid-dynamics·cosmology·geodynamics·dna·geochronology·chemistry·neuro·mind)를, 생성형 검색(RAG·AI 개요)이 **구절 단위로 추출·인용**할 수 있는 결정론적 다중 페이지 정본 HTML 로 변환하는 단일 기준. 정본은 docs/ HTML 하나이며, 세션은 이 표준서와 충돌하는 어떤 창의적 변경도 하지 않는다. LOCK → Derive → Gate: 입력은 잠그고, 규칙대로 산출하고, 카운트로 검증한다.
>
> **사용법(작업 세션):** 로드할 것 = 이 표준 + registry/cross_volume_doi.csv + 대상 docs/ HTML + tools/. **과거 스펙 버전·변경 이력 로드 금지** — 이 문서는 로그를 싣지 않는다(규칙만). 충돌 시 0장 헌법이 모든 조항에 우선한다.

## 0. 헌법 (Constitution) — 최상위 규범, 모든 조항에 우선

> 본 장은 VP-SPEC 의 최상위 규범이다. 1장 이하 어떤 조항·게이트·관행과 충돌하더라도
> 헌법이 항상 우선한다. 세 원칙은 "재현성"이라는 단일 가치를 산출물 구조로 강제한다.

**C1 — 재현성 최대 보장 (Maximum reproducibility).**
모든 정량 주장은 결정론적으로 재현 가능해야 한다. 재현의 정본은 `docs/` HTML 이며, 수치는
`tools/` 의 표준라이브러리 결정론 모듈로 재생성되고(동일 입력 → 동일 출력, 2×sha256 동일),
게이트가 정본 HTML 의 표시값을 그 재생성값과 대조한다(드리프트 0). 재현 경로가 패키지 내부에서
끊기지 않아야 한다 — 외부 도구·비공개 데이터·수작업 단계에 의존하는 수치는 그 사실을 명시한다.

**C2 — 정본 단일화 (Single canonical material: HTML; TeX 비동봉).**
정본은 HTML 하나다. TeX 본문 소스(`.tex`, `txt/` 본문, `{paper}.eq_list.tsv` 의 base64 TeX)는
머지·배포 패키지에 **동봉하지 않는다.** 사유: 같은 내용을 TeX·HTML 두 재료로 들면 한쪽 수정이
다른 쪽과 어긋나(상호 드리프트) 재현성의 기준 자체가 무너진다. 재현성은 정본(HTML)에서 직접
보장되어야 한다. TeX 가 필요하면 정본에서 on-demand 로 출력한다(`tools/extract.py` 가 수식 SVG 의
`img alt` LaTeX 와 구조를 추출 → 사람이 읽는 텍스트/LaTeX). 수식의 정본 표현은 **렌더된 SVG** 이며,
SVG/HTML 내부의 `alt`·`title` LaTeX 는 접근성 메타데이터로서 HTML 재료의 일부이지 별도 소스가
아니다(제거 대상 아님; 6·7장 참조).

**C3 — 재현 불가 시 사유 명시 (서술의 원칙).**
어떤 정량이 원리적으로 재현 불가하면(계산량 폭발로 패키지 내 결정론 재생성이 불가능한 경우 포함),
그 항목은 반드시 ① `[O]` 등급으로 표시하고 ② 재현 불가의 **구체적 사유(장애물)** 를 본문에 명시한다.
사유 없는 `[O]` 표기는 게이트 FAIL 이다. 재현불가 원장(`IRREPRODUCIBILITY_LEDGER.md`)이 전 `[O]`
항목·사유·위치를 한 곳에 집계한다. 대표 예(물리 백서):
- **절대 중력 크기(g≈9.8 m s⁻²)** — 사유: four-wall(네-벽) 정리가 절대 척도를 고정하려면 전(全)물리
  잠금격자 계산이 필요하나 이는 HPC급 계산 게이트에 막혀 패키지 내 재생성 불가(§17.4.4). 비율·형상은
  재현되나 절대 크기는 `[O]`.
- **전자기 미세구조 상수(αₑₘ≈1/137)** — 사유: 닫힌형 137≈4π(11−δ_proj)는 비강제 조립이며 4π 는 단위
  인공물이고 αₑₘ 는 에너지에 따라 흐른다(런닝). 따라서 유도가 아니라 비증거(non-evidence)로 표시되고
  값은 측정 입력(§14.5). 절대 g 와 동일한 계산-게이트 인식 등급(`[O]`)이다.

**C4 — 검색 수용성 (Retrieval-Readiness).**
정본은 생성형 검색(RAG·AI 개요)이 **구절(passage) 단위로 추출·인용**할 수 있어야 한다. 생성형 검색은
질의를 하위 질의로 fan-out → 전체 페이지가 아니라 구절을 검색 → 합성 → 가장 구체적·귀속가능한 추출을
인용한다. 따라서 강제 요건은 ① **answer-first**(페이지·섹션이 자체완결 직답으로 시작) ② **자체완결 명제**
(검색된 구절이 주변 없이 이해됨 — 미해소 참조 금지) ③ **구조화 데이터**(JSON-LD) ④ **기계 접근**(정적
HTML·봇 허용·sitemap). C4 는 C1–C3 과 충돌하지 않는다: 유도의 단일출처(SSOT)는 유지하되 결과의
**진술**을 자체완결화한다(6-R장). 구현·검사 규칙은 6-R장과 8장 검색 게이트.

---



## 1. 원칙과 금지사항

원칙
1. 변환의 주체는 코드다. 모델이 본문을 받아쓰는 방식은 금지한다.
2. 모든 세션은 종료 전 8장의 게이트를 실행하고 결과(gate.json)를 남긴다.
3. 읽기 전용(LOCK): src/, manifest/, slugs.csv, tools/, templates/, 2장 레지스트리.
4. 한 세션 = 한 과업. 범위는 4장의 세션 매트릭스를 따른다.
5. 세션 간 상태는 오직 파일로만 전달한다. 이전 대화 기억에 의존하지 않는다.
6. 레인 규칙: 세션은 자기 과업의 경로 밖 파일을 생성·수정하지 않는다.
   백서 세션의 레인: docs/{paper_id}/, docs/eq/{paper_id}/,
   manifest/{paper_id}.csv, reports/. 공용 파일(docs/index.html, sitemap.xml,
   assets/, concepts/, tools/, templates/)은 지정 Phase(0·4·5·6) 외 접근 금지.
   레인 밖 파일이 handoff zip 에 들어 있으면 그 자체로 게이트 FAIL 이다.

금지사항
- 본문 의미·수식·수치 변경, 임의 요약, 임의 삭제 금지. 허용되는 추가는
  abstract 요약문단, 재현성 스트립, 메타데이터, 내부 링크뿐이다.
- tools/ 스크립트 재작성 금지(버그 발견 시 보고만; 수정은 별도 승인 세션에서).
- 게이트 FAIL 산출물을 docs/ 에 남긴 채 종료 금지(원인 보고 후 종료).

---

## 2. 백서 레지스트리 (LOCK — 전 세션 공통 데이터)

| paper_id (URL 폴더) | code | 정식 제목 (영) | title 접미 약칭* | DOI(개념) | 대표 결과(텍스트 수식) | 유도 관계 |
|---|---|---|---|---|---|---|
| physics | phy | The Vacuum as a Jammed Elastic Solid, and the Speed of Light as Its Elastic-Wave Speed | VP Theory | 10.5281/zenodo.17932566 | c² = B/ρ ; m_p/m_e = 6π⁵ (−19 ppm) | 기반(foundation) |
| fluid-dynamics | flu | The Configured Continuum | Configured Continuum | 10.5281/zenodo.17972568 | ∂ρ/∂t + ∇·(ρu) = 0 ; ρ Du/Dt = ∇·T | jamming 분기 |
| cosmology | cos | Gravity, Galaxies, and Cosmology as Vacuum Inflow | Vacuum-Inflow Cosmology | 10.5281/zenodo.20568874 | a₀ = cH₀/2π ≈ 1.08×10⁻¹⁰ m s⁻² | inflow 분기 |
| geodynamics | geo | A Jamming–Unjamming Mechanism for Rapid Continental Break-up | Jamming Geodynamics | 10.5281/zenodo.17978934 | Ψ_eff > Ψ_y | 수렴(jamming+연대학) |
| dna | dna | A Deterministic Two-Layer Interpretation of DNA | 4D DNA Blueprint | 10.5281/zenodo.20471407 | form ← γ (Layer 1) ; quantity ← φ (Layer 2) | jamming 분기 |
| geochronology | chr | Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit | Cross-Chronometer Limit | 10.5281/zenodo.20568673 | 이물(고령) 혼입 ⇒ 연대 고령 편향 | 방법론(수렴 지원) |
| chemistry | chm | VP Chemistry & Electromagnetism: Derived from a Single Anchor on the Jamming-Lattice Substrate | VP Chemistry & EM‡ | 10.5281/zenodo.20680540 | c²=B/ρ (0.06% sim) ; arccos(−1/3) ; φ_RCP=0.7405 ; d-band 촉매 | jamming 분기(physics Vol I 인용) |
| neuro | neu | From Ion Channels to Behaviour: A Falsifiable Neural Emergence Chain | Neural Emergence Chain‡ | 10.5281/zenodo.17979015 | 작업기억 용량 ≈ θ/γ (7±2), tACS 인과 | 분기(자체 사슬) |
| mind | mnd | Felt Cognition: Parallel Micro-Eddies, the Stream of Thought, and the Open Problem of Experience | Felt Cognition‡ | 10.5281/zenodo.20694404 | stream = θ-프레임 직렬 선택 ; hard problem OPEN | frontier(neuro 인용, 일방) |

\* **원 6종**(physics·fluid-dynamics·cosmology·geodynamics·dna·geochronology) 약칭은 v1.6 에서
저자 확정으로 LOCK 됨 — 변경 금지.
‡ **v1.7 추가 3종**(chemistry·neuro·mind): 정식 제목·개념 DOI 는 Zenodo 에서 직접 확인(2026-06-15,
전 권 동일 저자 Lee Young Jae, ORCID 0009-0002-7535-8245). **제목·개념 DOI 는 확정이며 title 접미
약칭은 위 표기를 제안값으로 둔다 — 약칭만 저자 최종 LOCK 대기**(약칭 변경 시 이 표만 고치면 됨).
개념 DOI 는 최신본으로 해상된다(chemistry→20680541 v1.0 · neuro→20694299 v2 · mind→20694405 v1.0;
2026-06-15 확인). site 슬러그: neuro=/neuro, mind=/mind, chemistry=미확인. 최신본 DOI·요지·슬러그
상세는 `registry/cross_volume_doi.md`. 모든 세션은 이 표만 참조하며 원본 사이트를 재조사하지 않는다.

재현 코드 저장소(검증층): 사이트가 올라간 바로 그 공개 repo 를 함께 쓴다 —
`github.com/rego093-sketch/jamming-physics` (생성 확인 완료 — LOCK).
repo 루트의 repro/ 아래 구조는 사이트 슬러그와 1:1 —
`repro/{paper_id}/{슬러그}/` 안에 그 섹션의 스크립트·데이터·기대 출력.
GitHub Pages 게시 루트는 docs/ 만으로 한정한다(3장 참조). 따라서 repro/ 는
github.com 에서만 열람되고 jamming-physics.org 의 URL 이 되지 않으므로
robots·sitemap 조치 없이 색인 오염이 원천 차단된다.
Zenodo 의 repro zip 은 이 repo 릴리스의 동결 사본이다(GitHub–Zenodo 웹훅 자동 아카이브 —
사이트와 검증 코드가 한 릴리스 = 한 DOI 스냅샷으로 함께 동결된다).

산출 3계층 (역할 분담 — 혼동 금지)
- 검색층: jamming-physics.org 의 HTML — 색인·랭킹·링크의 표면. 항상 canonical.
- 검증층: GitHub repo — 사람이 코드·데이터를 열람·실행하는 곳. 압축 해제 상태.
- 인용·보존층: Zenodo — 버전 동결 PDF + repro zip + DOI. 변경 불가 스냅샷.

단일 소스 원칙 (v1.7 헌법 C2 — 역전): **정본은 `docs/` HTML 하나다.** 백서 HTML 이 최신이며,
머지·배포 패키지에는 TeX 본문 소스(`.tex`·`txt/`·`{paper}.eq_list.tsv`)를 **동봉하지 않는다**
(두 재료의 상호 드리프트로 재현성이 훼손되기 때문 — 재현성은 정본 HTML 에서 직접 보장한다).
TeX 가 필요하면 정본에서 on-demand 로 출력한다(`tools/extract.py`: 수식 SVG 의 img alt LaTeX 추출).
인용층 PDF 는 차기 버전에서 정본 HTML 로부터 생성하며 분할·재구조화하지 않는다.
[구 원칙 "src/.tex 가 마스터, PDF·HTML 동시 빌드"는 헌법 C2 로 폐기됨.]

---

## 3. 디렉토리 설계도

```
vp-site/                          ← 공개 GitHub repo = 단일 진실 원천 (Pages 게시 루트는 docs/ 만)
├── VP_SPEC_v1.8.md               ← 이 표준서 (모든 세션에 첨부)
├── tools/                        ← Phase 0 산출, 이후 LOCK (세션은 실행만)
│   ├── inventory.py              ← 표준라이브러리(단어수·섹션코드·슬러그). gate.py 가 word_count 공유
│   ├── derive_meta.py            ← (v1.7) Phase 2 결정론 파생: title·desc·abstract·grade 채움
│   ├── build_hub.py              ← (v1.7) Phase 3 결정론 허브: 목차·횡단 링크·개요 생성
│   ├── extract.py                ← (v1.7) 정본 HTML → 텍스트/LaTeX on-demand 출력(img alt 추출, 헌법 C2)
│   ├── reconcile_derived_to_html.py ← (v1.7) manifest·_meta.json 카운트를 정본 HTML 에서 재산출(헌법 C1)
│   ├── vp_numeric_ssot.py + vp_*.py ← 결정론 수치 단일진실원·재생성 모듈(2×sha256). 재현성 엔진
│   └── gate.py                   ← 8장 게이트 일괄 판정 → gate.json
├── templates/chapter.html  hub.html  concept.html
├── repro/{paper_id}/{슬러그}/    ← 재현 스크립트·데이터·기대 출력 (검증층, 게시 제외)
├── manifest/{paper_id}.csv  slugs.csv          ← 읽기 전용 (정본 HTML 의 파생 인덱스)
├── registry/cross_volume_doi.{csv,md}          ← (v1.7) 형제 백서 개념 DOI 레지스트리
├── docs/                        ← 배포 사이트 루트 = **정본(canonical)**, 헌법 C2
│   ├── index.html  sitemap.xml  robots.txt  llms.txt  llms-full.txt
│   ├── assets/css/site.css(≤50KB)  assets/fonts/(woff2 2~3)  assets/img/
│   ├── eq/{paper_id}/{code}-{섹션코드}-{일련3}.svg   ← 수식 정본(렌더 SVG); img alt LaTeX = 접근성 메타
│   ├── physics/            ├── fluid-dynamics/   ├── cosmology/
│   ├── geodynamics/        ├── dna/              ├── geochronology/
│   ├── chemistry/          ├── neuro/            ├── mind/   ← v1.7 추가 3권(2장 레지스트리)
│   │   각 백서 폴더 공통: index.html(허브), _meta.json(요약 카드),
│   │                     {슬러그}/index.html (섹션당 1폴더)
│   └── concepts/{용어 슬러그}/index.html
├── reports/{phase}-{paper}-{범위}.gate.json
└── IRREPRODUCIBILITY_LEDGER.md   ← (v1.7) 전 [O] 항목·재현불가 사유·위치 집계(헌법 C3)
```

> **머지·배포 패키지(헌법 C2):** 위 트리에서 `src/{paper_id}/(.tex)`, `txt/`(본문 TeX/텍스트 SSOT),
> `{paper}.eq_list.tsv`(base64 TeX), `render_eq.js`·`split.py`(TeX→SVG/소스 분할 파이프라인)는
> **동봉하지 않는다.** 정본은 `docs/` HTML 하나이며, TeX 가 필요하면 `extract.py` 로 정본에서
> on-demand 출력한다. (full-rebuild 가 필요한 별도 빌드 세션만 src/·split·render 파이프라인을 사용.)

URL 매핑: docs/ 하위 경로 = URL. 기존 허브 경로(/physics/ 등 레지스트리의
paper_id)는 그대로 재사용한다(리다이렉트 불필요, 내용만 교체).
게시 루트는 docs/ 만이며 repro/·src/·tools/·manifest/ 는 사이트 URL 이 되지
않는다(Pages 폴더 설정 또는 Actions 배포로 강제). repro 열람 링크는 도메인이
아니라 github.com 트리 뷰로 건다(Pages 는 디렉터리 목록을 생성하지 않음).
Pages 설정: Settings → Pages → Deploy from a branch → main → /docs.
스테이징(도메인 이전 전): docs/robots.txt 를 "User-agent: *" / "Disallow: /" 로
두고, 컷오버 시 정식 robots.txt 로 교체한다. 컷오버 = 구 repo(new)에서 커스텀
도메인 해제 → 새 repo 에 연결 → 구 repo Archive. DNS 는 변경 없음.

슬러그 규칙 — 결정론 알고리즘 (tools/split.py 가 자동 생성, 수작업 개입 금지)
1) 섹션 제목을 소문자 ascii 로 변환(발음 구별 기호·기호 제거)
2) 영숫자 외 문자는 하이픈으로, 연속 하이픈은 1개로
3) 불용어 제거: the a an of and as its for to in on with from
4) 앞에서 5단어까지만 취하고 `{번호 2자리}-` 접두 (부록은 `ax-{문자}-`)
   예) "8. Discrete Proton Structure (82+7)" → 08-discrete-proton-structure-82-7
5) 결과를 manifest/{paper_id}.csv 의 slug 열에 기록 — 이것이 그 백서의 슬러그 확정표
- 배포 후 슬러그 변경 금지. 알고리즘 결과가 충돌하거나 비면 게이트 FAIL 후 보고.

수식 SVG 파일명: `{code}-{섹션코드}-{일련3자리}.svg`
- 섹션코드: 본문 2자리(08), 부록 ax{문자}(axg). 예) phy-08-012.svg, phy-axg-003.svg

---

## 4. 세션 매트릭스 — 어느 창에서 무엇을 하는가

| Phase | 창 단위 | 과업 | 입력(부하) | 산출 |
|---|---|---|---|---|
| 0 | 1~2창 | 기반 고정: tools/ 4종, templates/, site.css, 폰트 서브셋, 레지스트리 약칭·slugs.csv 확정 | 표준서+물리 견본 (중) | tools/, templates/, assets/, slugs.csv |
| 1 | 백서당 1창 | ① tools/inventory.py 로 manifest 생성 ② tools/split.py 로 섹션 골격 분할+수식 LaTeX 추출 ③ render_eq ④ gate | 표준서+tools+원본 (소: 코드가 처리) | manifest/{p}.csv, docs/{p}/*, eq/, gate.json |
| 2 | **1 derive run + gate** | **결정론 파생(tools/derive_meta.py): title·description·abstract·grade·JSON-LD·breadcrumb 를 봉인 본문 후크에서 채움. 교차/횡단 링크는 Phase 1 골격 유지** | Phase 1 골격 + prefill (소: 코드가 처리) | 수정 html, _meta.json chapters(one_liner·grade) 갱신 |
| 3 | **build_hub run + gate** | **결정론 허브(tools/build_hub.py): 목차(고아 0)+횡단 링크(10장)+abstract+등급 원장 개요. 1,500~3,000단어 산문 개요는 저자 선택(작문 영역)** | _meta.json+abstract 모음 (소: 코드가 처리) | {p}/index.html, _meta.json abstract |
| 4 | 1~2창 | 개념 사전(용어당 1페이지, 백서 횡단 접착제) | 스크립트 추출 용어·문맥 (중) | concepts/* |
| 5 | 1창 | 최상위 인덱스+sitemap+사라지는 구 URL 301 표 | _meta.json ×6+현 랜딩 (소) | index.html, sitemap.xml |
| 6 | 1창 | 전 사이트 최종 게이트(링크·중량·노드) | tools/gate.py (소) | final.gate.json |
| 7 | 1창+저자 | 학술 채널 정합: Scholar 태그·Zenodo 역링크·PDF 1면·repo README (12장) | _meta.json ×6+레지스트리 (소) | 허브 head 갱신, 체크리스트 |

순서: 0 → (백서별 1→2→3, 6개 병렬 가능) → 4 → 5 → 6 → 7.
Phase 2 는 (v1.7) 백서당 **1 derive run + gate**(결정론). 전체 프로젝트 약 12~20창.
[구 v1.6 추정 "물리 8~12창"은 Phase 2 를 수작업 편집으로 본 값 — derive_meta.py 도입으로 폐기.]

---

## 5. 세션 핸드오프 프로토콜 (창 간 파일 전달 규약)

새 창은 이전 창의 파일을 보지 못한다. 전달은 아래 규약으로만 한다.

세션 시작 시 저자가 업로드하는 것
1. VP_SPEC_v1.8.md (항상)
2. 해당 Phase 의 tools/ 스크립트와 templates/ (Phase 1~6)
3. 과업 입력: 원본(Phase 1) 또는 이전 산출 섹션 html(Phase 2~) + 해당 manifest 행 + slugs.csv
4. 8 장 시작 지시문(12장)에 과업 범위 기입

세션 종료 시 세션이 산출하는 것
1. `handoff_{phase}-{paper}-{범위}.zip` 1개 — 내부 경로는 repo 상대경로 그대로
   (zip 루트에 docs/, manifest/, reports/ 가 오도록). 저자는 repo 루트에서 unzip 만 한다.
2. gate.json 의 PASS/FAIL 요약을 채팅으로 보고. FAIL 시 zip 에 docs/ 반영 금지.
3. _meta.json 은 항상 zip 에 포함(다음 세션·Phase 5 의 입력이므로).

저자 병합 절차 (받은 zip 처리는 이 3줄이 전부)
1) repo 루트에서 받은 순서대로 unzip — 덮어쓰기 허용(zip 은 해당 경로의 최신 전체본)
2) reports/ 의 새 gate.json 이 PASS 인지 확인 (FAIL zip 은 병합하지 않고 반려)
3) 커밋: "phase{P} {paper} {범위} (gate PASS)" → push 하면 Pages 자동 반영

---

## 6. 페이지 표준 템플릿 (챕터 페이지) — 9개 백서 공용

{P.x}는 2장 레지스트리의 해당 백서 값. Phase 1 이 골격 생성, Phase 2 가 {중괄호}를 채운다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{주제, ≤45자} — {P.약칭} §{N} | Jamming Physics</title>
<meta name="description" content="{80~160자, 결론 선행}">
<link rel="canonical" href="https://jamming-physics.org/{P.paper_id}/{slug}/">
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="preload" href="/assets/fonts/text.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ScholarlyArticle",
 "headline":"{주제}",
 "isPartOf":{"@type":"CreativeWork","name":"{P.정식 제목}",
   "sameAs":"https://doi.org/{P.DOI}"},
 "position":{N},
 "author":{"@type":"Person","name":"Young Jae Lee",
   "sameAs":"https://orcid.org/0009-0002-7535-8245"},
 "license":"https://creativecommons.org/licenses/by/4.0/"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Home","item":"https://jamming-physics.org/"},
 {"@type":"ListItem","position":2,"name":"{P.약칭}","item":"https://jamming-physics.org/{P.paper_id}/"},
 {"@type":"ListItem","position":3,"name":"§{N} {짧은 제목}"}]}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › <a href="/{P.paper_id}/">{P.약칭}</a> › §{N}</nav></header>
<main>
<h1>{h1 — title 주제부와 동일 의미, 정확히 1개}</h1>

<p class="answer">{answer-first: 자체완결 직답 40~60단어. 엔티티 명명 + 핵심 값/결론 + 등급. 와인드업 금지. 본문 단어수 제외. 헌법 C4·6-R.3.}</p>

<p class="abstract">{평문 2~3문장. 이 섹션의 결론과 핵심 수치를 유니코드 수식으로 포함.}</p>

<aside class="claim-strip">
  <span class="grade g-{forced|calibrated|open}">{원문 등급 표기}</span>
  <span class="gate">LOCK → Derive → Gate</span>
  <a href="https://github.com/rego093-sketch/jamming-physics/tree/main/repro/{P.paper_id}/{slug}/" rel="noopener">재현 코드 (GitHub)</a>
  <a href="https://doi.org/{P.DOI}" rel="noopener">DOI 스냅샷</a>
</aside>

<!-- 6-R.2: 본문이 다른 섹션의 잠금 정량(α·δ·νₚ 등)을 인용하면, 그 정량마다 자체완결 카드 1개를 둔다.
     값+한줄 의미+등급+정본 유도 링크. (유도가 아니라 결과 진술이므로 SSOT 위반 아님.) 예: -->
<aside class="vp-card" data-locked="delta"><b>δ = 1/π²</b> — 이중 정류 생존상수(두 half-wave 평균의 곱, max-entropy 측도). <b>[F]</b> forced. <a href="/physics/05-geometric-rectification-constants-single-source/#delta">정본 유도 §5.2</a></aside>

{본문 — 원본 그대로 이관. h2/h3 계단식, h1 추가 금지. 각 섹션 첫 문장 = 그 섹션의 직답(6-R.3), 단락 ≤3문장}

<figure class="eq">
  <img src="/eq/{P.paper_id}/{P.code}-{섹션코드}-{일련3}.svg" width="{W}" height="{H}"
       loading="lazy" alt="{LaTeX 원문}">
</figure>

<nav class="pn">
  <a rel="prev" href="/{P.paper_id}/{이전 슬러그}/">← §{N−1}</a>
  <a href="/{P.paper_id}/">백서 목차</a>
  <a rel="next" href="/{P.paper_id}/{다음 슬러그}/">§{N+1} →</a>
</nav>
</main>
<footer>{공통 푸터: DOI, ORCID, CC BY 4.0}</footer>
</body>
</html>
```

재현성 스트립 규칙 (백서 가치 표출 장치)
- abstract 바로 아래 고정 배치. (v1.7) 등급 어휘는 레지스트리 기반으로 LOCK —
  본문 토큰 [F]/[H]/[V]/[O] → 클래스 g-forced/g-hypothesis/g-verified/g-open,
  표기 "[X] 이름"(grade_vocab_{paper}.csv 근거). 원문에 등급 토큰이 있는 섹션에만 부여.
  페이지 등급(.claim-strip.page 의 grade span) = 그 섹션 VP-S aside 토큰의 최빈값
  (동률 시 우선순위 F>V>H>O). 토큰이 없는 섹션은 등급 배지 생략(임의 부여 금지).
  GitHub 링크는 2장의 repo 폴더 규칙(슬러그 1:1)을 따르며, 폴더가 아직 없으면 게이트 FAIL.
- 이 스트립은 "주장마다 등급·재현 경로가 달린다"는 이 백서군의 차별점을
  모든 페이지에서 기계가 읽는 일관 구조로 노출하기 위한 것이다.

기타 템플릿 규칙
- 첫 화면에서 수식 이미지보다 abstract 평문이 먼저 온다.
- 교차 참조("§7에서")는 모두 해당 페이지로의 a 링크. 같은 대상 링크는 페이지당 첫 1회.
- 인라인 CSS/JS/폰트 임베드 금지. KaTeX/MathJax span 출력 잔존 금지.

---

## 6-D. Phase 2 결정론 파생 규칙 (tools/derive_meta.py, v1.7)

Phase 1 골격의 `data-phase2` 후크와 정형 마커를 입력으로 {중괄호}를 **봉인 본문에서만**
채운다. 출처 우선순위 밖의 텍스트는 생성하지 않는다(임의 작문·요약 금지). 편집 대상은
`<head>`(title·description·JSON-LD headline·breadcrumb) + `.abstract` `<p>` + 페이지
`.claim-strip` 의 grade span 으로 한정한다 — 셋 다 8장 gate 의 단어수 제외영역이므로
본문 단어수(±0.5%)는 구성상 불변이다.

1) **subj45 (제목 주제부, ≤45자)** = h1 을 결정론 축약. (a) 후미 괄호 `(…)` 제거 →
   (b) 후미 부제(`:`,`---`,`—`,`;`,` from `) 절단 → (c) 단어경계 절단(중간 절단 금지).
   title = `{subj45} — {P.약칭} §{N} | Jamming Physics` (접미부·§N 은 골격 값 재사용).
   JSON-LD headline·breadcrumb 짧은 제목도 subj45 로 통일.
2) **description (80~160자, 결론 선행)** = 섹션 대표 클레임(없으면 리드 문장)을 선두로,
   80자 미만이면 다음 문장으로 보강, 160자 초과면 마지막 공백에서 절단. 속성 안전(`"`→`'`).
3) **abstract (평문 ≤3문장, 키피겨 1회)** = 출처 우선순위로 리드 2문장 구성
   [큐레이트 클레임 `<q class="one">` → prefill one_liner 풀 → 서사 `<p>` →
   구조(`<li>/<td>/<div class="box">` 등) → 표제]. 키피겨(텍스트 수식)가 없으면
   **aside·DOI 링크 제외 본문**에서 첫 키피겨 주변 절을 3번째 문장으로 발췌(gate FIG 와 동일 기반).
   본문에 대표 수치가 전혀 없는 섹션은 수식 없이 평문만(강제 주입 금지 — 23번 게이트 면제와 정합).
4) **grade** = 6장 규칙대로 섹션 VP-S aside 토큰 최빈값 → g-클래스·표기. 없으면 생략.
5) **정규화(내용 무변경)** = 인라인 math 구분자 `$` 제거(내부 보존), 구두점 앞 공백 정리.
6) **반작문 자체검사(fail-closed)** = abstract·description 의 모든 수치 토큰이 본문∪레지스트리에
   없으면 그 섹션을 기록하지 않고 종료(원인 보고). 8장 게이트가 동일 규칙을 재검증한다.
- _meta.json chapters[]의 one_liner(대표 클레임)·grade 를 같은 출처에서 갱신.
- 결정론·재현 가능: 동일 입력 → 동일 출력(해시 고정). 본문·수식·수치는 일절 건드리지 않는다.

---

## 6-R. AI-검색 수용성 (Retrieval-Readiness) — 헌법 C4 구현

생성형 검색이 정본을 구절 단위로 추출·인용하도록 만드는 강제 규칙. 검색 게이트(8장)가 검사한다.

### 6-R.1 검색 파이프라인 모델 (설계 기준)
생성형 검색은 **질의 fan-out**(질문을 하위 질의로 분해) → **구절 검색**(전체 페이지가 아니라 passage 임베딩
검색) → **합성** → **가장 구체적·귀속가능한 추출 인용** 순으로 작동한다. 따라서 모든 페이지는 다수의 하위
질의 각각에 대해 **독립적으로 인용 가능한 자체완결 구절**을 제공해야 한다. (근거: 자체완결 명제 청크는
참조-분산 청크 대비 retrieval 충실도가 크게 높다.)

### 6-R.2 SSOT vs 자체완결 — 핵심 해법 (유도는 단일출처, 결과 진술은 자체완결)
SSOT("한 번 유도, 나머진 참조", 5·7장)는 드리프트를 막지만(C1), 검색된 구절이 "δ는 §5.2에서 유도"처럼
**미해소 참조**만 담으면 그 구절은 주변 없이는 무의미해 인용되지 않는다(지시 대상 미해소 문제). 해결:

- **유도/증명의 단일출처는 유지**한다(정본 1곳, 드리프트 0 — 5·7장·canon_lock 그대로).
- **잠금 정량을 쓰는 모든 페이지는 그 정량마다 자체완결 카드를 1개 포함**한다: 값 + 한 줄 평이한 의미 +
  등급 + 정본 유도로의 명시 링크. 카드만으로 해당 구절이 주변 없이 이해되어야 한다.

```html
<aside class="vp-card" data-locked="delta">
  <b>δ = 1/π²</b> — 이중 정류 생존상수(두 half-wave 평균의 곱, max-entropy 측도). <b>[F]</b> forced.
  <a href="/physics/05-geometric-rectification-constants-single-source/#delta">정본 유도 §5.2</a>
</aside>
```

**원칙(중요):** 결과의 자체완결 **재진술**은 SSOT 위반이 아니다 — 금지되는 것은 유도/증명의 중복이지,
값·의미의 진술이 아니다. 금지: 본문 결론 구절에서 잠금 정량을 **값·의미 재진술 없이** "§X 참조"로만 처리.

### 6-R.3 answer-first · 원자 명제 · 짧은 단락
- 페이지와 **모든 섹션의 첫 문장**은 그 단위의 직답(엔티티 명명 + 값/결론)이다. 와인드업 금지 — 엔진은
  깔끔한 주장을 추출하지 도입부를 추출하지 않는다. 페이지 직답은 `<p class="answer">`(40–60단어, 본문
  단어수 제외)로 고정한다.
- 단락은 ≤3문장. 한 청크 = 한 질문에 대한 자체완결 답.
- 핵심 주장마다 **수치 + 귀속**(어느 잠금 lock_id / 섹션 / DOI). 비교·정의·단계는 표·리스트로(추출률↑).

### 6-R.4 구조화 데이터 (JSON-LD, `<head>` 내) — 기계 대면 사실층
페이지 유형별 최소 스키마(JSON-LD 는 `<head>` 전달이 선호됨). 6-D 의 결정론 파생에 JSON-LD 생성 포함.

- **챕터 페이지** = `ScholarlyArticle`:
```json
{"@context":"https://schema.org","@type":"ScholarlyArticle",
 "headline":"{섹션 제목}","isPartOf":{"@type":"CreativeWorkSeries","name":"{2장 약칭}","identifier":"{개념 DOI}"},
 "author":{"@type":"Person","name":"Young Jae Lee","sameAs":"https://orcid.org/0009-0002-7535-8245"},
 "identifier":"{개념 DOI}","datePublished":"{ISO}","dateModified":"{ISO}",
 "isBasedOn":"{repro URL}","knowsAbout":["jamming lattice","rectification constant","{핵심 엔티티}"]}
```
- **용어/개념 페이지** = `DefinedTerm`(정의 질의 인용↑):
```json
{"@context":"https://schema.org","@type":"DefinedTerm","name":"δ (rectification constant)",
 "termCode":"delta","description":"이중 정류 생존상수 1/π²","inDefinedTermSet":"https://jamming-physics.org/concepts/"}
```
- **검증/반증 프레임 페이지(선택):** 자체 등급은 `Claim` + `Rating` 으로 표현. ClaimReview 는 본래 제3자
  주장 팩트체크용이므로 신중히 사용.
- 공통: `BreadcrumbList`, 볼륨 허브 = `CreativeWorkSeries`/`Book`, 저자 `sameAs`(ORCID·DOI).

### 6-R.5 접근 계층 (1차 신호; llms.txt 는 보조·전방호환)
- `docs/robots.txt`: AI·검색 봇 **허용** — Googlebot, Bingbot, OAI-SearchBot, GPTBot, PerplexityBot,
  ClaudeBot, Google-Extended (기본 차단 주의). 게시 루트가 docs/ 뿐이므로 repro/·tools/ 색인 오염은 원천 차단.
- 정적 HTML(SSR) — JS 렌더 의존 금지(AI 크롤러는 raw HTML 의존). 본 정본은 정적 HTML 이므로 충족.
- `docs/sitemap.xml`: 전 docs/ index.html(noindex 제외) 열거.
- `docs/llms.txt`(<5KB): 권위 있는 1문단 블록쿼트 요약 + 기능별 섹션(core·research·concepts·policies)의
  우선순위 링크. `docs/llms-full.txt`: 정본 본문 마크다운 평문(extract.py 묶음). 보조 신호로 취급(1차는
  구조화 데이터·시맨틱 HTML·sitemap).

---

## 7. 수식 규칙

판정 한 줄: "키보드로 한 줄 평문처럼 자연스럽게 쳐지는가?"

A. 유니코드 텍스트
- 한 줄 인라인 식: c² = B/ρ, 6π⁵, a₀ = cH₀/2π, Ψ_eff > Ψ_y
- 각 페이지 대표 결과 1~3개는 abstract 또는 본문 문장에 반드시 텍스트로 1회 이상.

B. 외부 SVG (디스플레이 수식 전부)
- 수식의 **정본 표현은 렌더된 SVG** 다(헌법 C2). img 필수 속성: src, width, height,
  loading="lazy", alt="{LaTeX 원문}". 이 `alt` LaTeX 는 정본 SVG 의 접근성 메타로서 HTML 재료의
  일부다 — 별도 TeX 소스가 아니며 제거 대상이 아니다.
- **TeX 소스(`.tex`·`txt/`·`eq_list.tsv`)는 패키지에 비동봉**(헌법 C2). SVG 는 이미 렌더되어 정본에
  포함되므로 재현에 TeX 소스가 필요 없다. TeX/텍스트가 필요하면 `tools/extract.py` 로 정본 HTML 에서
  on-demand 추출한다(img alt → LaTeX, 본문 구조 → 텍스트).
- [구 규칙: render_eq.js(MathJax)로 LaTeX→SVG 일괄 렌더 + eq_list.csv 산출 — TeX 소스 단계로,
  HTML 정본화(헌법 C2) 이후 패키지에서는 비활성. SVG 재생성이 필요한 별도 빌드 세션에서만 사용.]

C. MathML 은 수식이 드문 허브·개념 페이지에 한해 허용. 챕터 전면 적용 금지.

---

## 8. 게이트 체크리스트 (세션 종료 조건) — tools/gate.py 가 판정

Phase 1 (기계 변환)
- [ ] 섹션 수 = manifest 행 수
- [ ] 섹션별 수식(인라인+디스플레이) 카운트 = manifest 1:1
- [ ] 디스플레이 수식 수 = svg 파일 수 (고아·누락 0)
- [ ] html 내 'class="katex' 잔존 0
- [ ] 그림·표 카운트 = manifest 일치
- [ ] 파일당 HTML ≤300KB, DOM 노드 ≤3,000

Phase 2 (결정론 파생 — tools/derive_meta.py)
- [ ] title: 주제부 ≤45자, 전체 ≤90자, 패턴 "{주제} — {P.약칭} §N | Jamming Physics"
- [ ] description 80~160자 · h1 정확히 1개 · abstract `<p>` 존재
- [ ] (v1.7) abstract 키피겨(텍스트 수식)는 **본문(aside·DOI 링크 제외)에 대표 수치가 있는 섹션에만** 요구
      — 수치 없는 안내/구조 섹션은 면제(수식 강제 = 수치 무변경 위반)
- [ ] (v1.7) 반작문: abstract·description 의 모든 수치 토큰이 본문에 존재(invent-number 0)
- [ ] 본문 단어수: <main>에서 .abstract·.claim-strip·.vps aside·h1·nav 제외 후 manifest 와 ±0.5% 이내
- [ ] 재현성 스트립 존재(등급은 본문 토큰 있을 때만, 레지스트리 어휘) · `(Phase 2` 잔존 0 · 내부 링크 깨짐 0

Phase 3/5/6
- [ ] 허브: 전 챕터 링크(고아 0) + 10장 횡단 링크 ≥1
- [ ] 인덱스: 9 허브 링크(2장 레지스트리 전 권), 카드 수치 = _meta.json 일치
- [ ] sitemap URL 수 = docs/ 내 index.html 수(noindex 제외)
- [ ] 사라지는 구 URL → 신 URL 301 매핑표 존재
- [ ] gate.json 에 tools/ 스크립트 버전 해시 기록

Phase 4 (수치 드리프트 — 정본 HTML, v1.7 헌법 C1·C2)
- [ ] 단일 진실원 `tools/vp_numeric_ssot.py`(표준라이브러리 결정론)가 도는가 + 핵심 잔차 일치
- [ ] 정본 HTML(`docs/{paper}/` 본문 텍스트 + 수식 img alt LaTeX)의 표시 수치가 정준 재생성과 0 드리프트
      — 검사 대상은 정본 HTML 이며 TeX 소스(txt/·eq_list)는 비동봉(헌법 C2). `--check` 도 정본 HTML 대상.
- [ ] 결정론 모듈 2회 실행 산출(LEDGER)의 sha256 동일

헌법 게이트 (v1.7 — C1·C2·C3, 머지/배포 전 필수)
- [ ] **C2 정본 단일화**: 패키지에 TeX 본문 소스 0 — `find . -name '*.tex'`, `*.eq_list.*`,
      `txt/` 본문 모두 부재. 수식 SVG 와 그 img alt LaTeX(접근성 메타)는 정본으로 유지.
- [ ] **C1 파생 정합**: `manifest/{paper}.csv`·`_meta.json` 의 게이트 검사 카운트
      (words·eq_display·figures·tables)가 정본 HTML 재산출값과 일치(`tools/reconcile_derived_to_html.py`).
      data-eq 합 = 잔존 SVG 수(고아 0).
- [ ] **C3 재현불가 사유**: 모든 `[O]` 등급 항목이 재현 불가 사유(장애물)를 본문에 명시.
      `IRREPRODUCIBILITY_LEDGER.md` 가 전 `[O]` 항목·사유·위치를 집계하며 본문과 교차 확인된다.

검색 게이트 (v1.8 — C4 검색 수용성, 변환·머지 산출물에 적용)
- [ ] **answer-first**: 페이지 첫 콘텐츠 블록이 `<p class="answer">` 자체완결 직답(엔티티+값/결론, 40~60단어).
- [ ] **자체완결 카드**: 본문이 인용하는 잠금 정량마다 `aside.vp-card`(값+의미+등급+정본 유도 링크) 1개;
      값·의미 재진술 없는 순수 "§X 참조" 결론 구절 0 (6-R.2).
- [ ] **JSON-LD**: 페이지 유형 스키마 유효(챕터=ScholarlyArticle, 용어=DefinedTerm) + `sameAs` ORCID·DOI;
      `<head>` 전달. 허브=CreativeWorkSeries/Book, BreadcrumbList 존재.
- [ ] **접근**: `robots.txt` 가 7개 봇(Googlebot·Bingbot·OAI-SearchBot·GPTBot·PerplexityBot·ClaudeBot·
      Google-Extended) 허용 · `sitemap.xml` 에 페이지 존재 · `docs/llms.txt` 존재·<5KB.
- [ ] **단락**: 본문 단락 대부분 ≤3문장(소프트; 장문 블록 경고).

---

## 9. 요약 카드 — docs/{paper_id}/_meta.json

```json
{
  "paper_id": "physics", "code": "phy",
  "title": "(2장 레지스트리의 정식 제목)",
  "short": "VP Theory (레지스트리 약칭)",
  "doi": "10.5281/zenodo.17932566",
  "hub_url": "/physics/",
  "branch": "foundation | jamming | inflow | convergence | methods",
  "abstract": "≤80단어 평문 (Phase 3)",
  "headline_results": ["c² = B/ρ", "m_p/m_e = 6π⁵ (−19 ppm)"],
  "chapters": [
    {"no": 8, "slug": "08-discrete-proton-structure-82-7",
     "title": "Discrete proton structure (82+7)",
     "one_liner": "(Phase 2)", "grade": "forced|calibrated|open|null",
     "words": 10921, "eq_inline": 412, "eq_display": 119}
  ],
  "totals": {"words": 147353, "eq": 6742, "figures": 276, "tables": 30}
}
```

Phase 5 는 9개 백서를 다시 읽지 않고 이 카드 9장만 읽는다.

---

## 10. 횡단 링크 규칙 — 유도 지도를 사이트 구조로

레지스트리의 "유도 관계" 열이 곧 링크 지도다. 한 전제에서 여섯 분야가
유도된다는 이 프로그램의 핵심 가치를, 사람과 구글이 모두 읽는 링크로 구현한다.

1. 허브 상단 1문장(고정 패턴): 비기반 백서는
   "이 백서는 {VP Theory의 jamming|inflow 분기}에서 유도된다 → /physics/"
   물리 허브는 "이 기반에서 다섯 백서가 유도된다" + 5개 허브 링크.
2. geodynamics 허브는 physics(jamming) 와 geochronology(연대 방법) 둘 다에 링크(수렴).
3. 챕터 본문에서 타 백서 개념이 처음 등장하면 해당 허브 또는 concepts 페이지로 링크.
4. concepts 페이지는 그 용어가 등장하는 모든 백서 허브를 역링크한다(횡단 접착제).

---

## 11. 최상위 인덱스(docs/index.html) — Phase 5

원칙: 인덱스는 "9개 백서를 이해해 쓰는 글"이 아니라 "_meta.json 9장의 조립"이다.
1. 입력: 카드 ×6 + 현행 랜딩 html. 현행 랜딩의 서사(한 줄 전제 → 6카드 →
   유도 지도 → 방법론 → DOI 푸터)는 유지, 데이터만 카드 기준 갱신.
2. 백서 카드 = title + headline_results 1개(텍스트 수식) + DOI + 허브 링크.
3. 홈은 허브 6개까지만 링크(챕터 나열 금지 — 챕터는 허브·sitemap 의 역할).
4. JSON-LD: WebSite + Person(ORCID) + CollectionPage(hasPart 로 백서 6).
5. 게이트: 9 허브 링크 유효, 카드 수치 = _meta.json 일치.

---

## 12. 학술 채널·아카이브 정합 — Phase 7

PDF·DOI·재현 파일을 검색층과 기계 판독 가능하게 연결하는 단계.

A. 허브 페이지 (세션 작업)
- head 에 Highwire citation 태그 5종: citation_title, citation_author,
  citation_publication_date, citation_doi, citation_pdf_url(Zenodo PDF 직링크).
  Google Scholar 진입 경로. Zenodo 자체의 Scholar 색인은 일정치 않으므로
  자기 허브의 citation 태그가 확실한 경로다.

B. Zenodo 레코드 (저자 수작업 — 세션은 레코드별 체크리스트 산출)
- 각 레코드 related identifiers 에 "isDescribedBy → 해당 허브 URL" 추가.
  사이트(sameAs DOI) ↔ Zenodo(related URL) 양방향 고리로
  "이 사이트 = 이 DOI 저작"이 기계 판독된다.
- repro zip 은 GitHub 릴리스 자동 아카이브(웹훅)로 생성·유지.

C. PDF (차기 버전부터, 단일 소스 빌드에 편입)
- 1면 머리에 1행 명기: 허브 URL + DOI ("Living version: …").
- PDF 문서 메타데이터(제목·저자·키워드) 채움. 텍스트 기반 유지(스캔 금지).
- 본문 재구조화 불필요. PDF 내 링크는 절대 URL.

D. GitHub repo (저자/세션 공동) — 사이트와 동일 repo
- repro/ 아래 압축 해제 상태, 폴더 = repro/{paper_id}/{슬러그}/ (2장 규칙).
- Pages 게시 루트가 docs/ 로 한정되어 있는지 확인 — repro/ 가 사이트 URL 로
  새어 나오면 게이트 FAIL.
- 루트 README: 백서 ↔ repro 폴더 ↔ DOI 대응표.
  각 섹션 폴더에 한 줄 README(무엇을 검증하는지 + 기대 출력).
- 대용량 데이터(단일 100MB 초과 또는 총량 수백 MB 이상)는 repo 에 두지 않고
  Zenodo 레코드에 올린 뒤 폴더 README 에서 링크한다(Pages·clone 부담 방지).

Phase 7 게이트
- [ ] 허브 6개 모두 citation 태그 5종 존재, citation_pdf_url 200 응답
- [ ] 전 챕터 claim-strip 의 GitHub 링크가 실제 폴더와 1:1 (404 = FAIL)
- [ ] https://jamming-physics.org/repro/ 가 404 인지 확인 (게시 분리 검증)
- [ ] Zenodo 6 레코드에 허브 역링크 존재 (저자 확인 체크)
- [ ] 차기 PDF 1면에 허브 URL·DOI 표기 (버전 게이트)

---

## 13. 새 창 표준 시작 지시문 (복사용)

```
[로드: VP_SPEC_v1.8.md(먼저 정독) + registry/cross_volume_doi.csv + 대상 docs/ HTML + tools/·templates/]
[로드 금지: 과거 스펙 버전·변경 이력 — 이 표준만으로 충분, 토큰 절약]
이번 세션 과업: Phase {P} / {paper_id} / {범위 예: §8–§10}
헌법 우선(C1 재현성·C2 HTML 정본/TeX 비동봉·C3 [O] 사유·C4 검색 수용성).
백서 정보는 2장 레지스트리의 {paper_id} 행만 사용한다(웹 재조사 금지).
본문 무변경 — 편집은 head·answer·abstract·claim-strip·vp-card·내부링크·JSON-LD 뿐.
산출: 3·6·6-R·7장 규칙 준수 + 5장 규약의 handoff zip 1개. 수치는 tools/vp_*ssot.py 결정론(2×sha256).
종료 조건: 8장의 해당 Phase 게이트 + 헌법 게이트 + 검색 게이트 전부 PASS, gate.json 포함, 요약 보고.
금지: 1장 금지사항. 표준서와 충돌하는 제안은 실행하지 말고 보고만 할 것.
Phase 1 이상인데 tools/·templates/ 첨부가 없으면 어떤 산출도 만들지 말고 "Phase 0 키트 누락"만 보고하고 종료.
```

— 끝 (v1.8) —
