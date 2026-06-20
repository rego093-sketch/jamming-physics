# ================================================================
# [v0.11.0] 2026-06-15 — VP-SPEC v1.7 → v1.8 (C4 검색 준비층) · 도구판 r6 → r7
# ================================================================
# 대상: vp_physics (물리편, 47 챕터 + 허브 1). 저자 승인 업그레이드.
# 본문 서술·수식·수치 일절 미변경. 추가 요소는 전부 본문 단어수 제외영역에만 주입.
# 표준: VP_SPEC_v1.8(동봉). 소스 봉인: v0.8 (src_pin 일치, 불변).

## 0. 한 줄 요약
v1.8 의 신설 항목인 **C4 Retrieval-Readiness(검색 준비층)**를 결정론·멱등·반작문 원칙으로
물리편 전 47 챕터 + 허브에 적용했다. 생성형 검색(RAG/AI 개요)이 페이지를 문단 단위로
인용·자기완결적으로 소화할 수 있도록 **answer-first 직답**, **self-contained vp-card**,
**기계 접근 파일(robots/sitemap/llms)**, **시리즈 JSON-LD(저자·ORCID·DOI)**를 추가했다.

## 1. 표준·도구판
- 표준: **VP_SPEC_v1.7 → v1.8**. v1.8 델타 = C4 검색 준비층(6장 템플릿 순서, 8장 SEARCH GATE 신설).
- 도구판: **r6 → r7**. 저자 승인 하에 결정론 생성기를 확장(변환 세션의 "도구 미개작" 규칙은
  변환용이며, 승인된 표준 업그레이드에는 적용되지 않음). r6 산출물은 100% 보존.
- r6 백업: `tools/.r6_backup/`(derive_meta·gate 의 r6 원본). gate 의 tools 지문(tools_sha16)은
  `tools/*` 비재귀·dotfile 제외 → 백업 폴더는 지문에서 자동 제외.

## 2. derive_meta r6 → r7 (결정론 메타 생성기)
r6 의 모든 동작 보존(title·description·JSON-LD·abstract·grade 를 봉인 본문에서만 채움).
v1.8 추가:
- **(A) answer-first** `<p class="answer">` — `</h1>` 직후 삽입. 엔티티 주어 + 본문 파생
  핵심 클레임/리드 문장 + "Grade [X] 명칭" 접미. 40~60 단어 목표. 멱등(기존 제거 후 재삽입).
- **(B) self-contained vp-card** `<aside class="vp-card" data-locked="ID">` — 페이지 본문에
  인용된 잠금량마다 1장. `심볼 = 값 — 의미 [등급] 명칭. <a>정준 유도 §N</a>`. 자기 정준
  섹션에는 생략. 멱등.
- 6장 템플릿 순서 준수: h1 → answer → abstract → claim-strip → 본문.
- **반작문 불변**: answer·abstract·description 의 모든 수치는 본문 ∪ 레지스트리에 존재해야 함
  (위반 시 해당 섹션 None 반환·미적용). § 섹션 참조는 발명 수치에서 제외.

### 2.1 텍스트 품질 보정(r7.1)
변환 산문이 아닌 봉인 본문에서 직답을 증류하므로, 예산 절단·괄호·수식 단편으로 인한
인공물을 결정론적으로 제거(내용 추가 0):
- 괄호 인지 문장 분할(괄호 내부 .!?— 에서는 미분할 → "5π)." 류 고아 단편 방지).
- 단편 정리: 짝 없는 ')' 제거, 닫히지 않은 '(' 이후 절단, ',.'·'..' 구두점 다듬기.
- 순수 수식 단편 배제(3자 이상 알파벳 단어 1개 이상 요구).
- 포함보호 dedup(접두·부분 중복 문장 제거·교체 → §13 접두 중복 해소).
- 엔티티 접두 괄호 균형(`subj45` → §04 "(1:" · §10 "(clock-free" 불균형 해소).
- 예산 절단 말미의 매달린 접속/전치사(and/or·and·of·to·the…) 제거.

### 2.2 멱등성·환류 차단(r7.2) — 본 업그레이드의 핵심 수정
**증상**: 6개 챕터(07·10·12·18·w0·w5)에서 직답·abstract 의 제목 접두가 실행마다 1회씩
누적("3-Sector…: 3-Sector…: …")되어 비멱등.
**원인**: 파생 소스 `body_noaside` 가 `<aside>`·`<p class="abstract">` 는 제거하나
**자기 주입한 `<p class="answer">` 는 제거하지 않음**. `figure_snippet()`가 그 직답 텍스트를
다시 소스로 읽어 abstract 에 덧붙이고, `build_answer` 가 거기에 또 `subj:` 를 붙이는 무한 환류.
**수정**:
- `body_noaside` 에서 `<p class="answer">` 도 제거(자기 주입 직답 환류 차단). 이제 생성기는
  봉인 본문에서만 파생 → 1회 실행으로 기존 오염 교정, 2회째부터 동일 출력(멱등).
- 방어선: `build_answer` 가 풀 문장이 제목(subj)으로 시작하면 그 접두를 제거(중복 2차 차단).
**검증**: 두 차례 연속 실행 시 47 챕터 md5 동일. 제목 반복 0 · 구조 인공물 0.

## 3. build_search_layer (신규, 결정론·멱등) — docs 레벨 기계 접근 파일
`python3 tools/build_search_layer.py --paper physics`
- **docs/robots.txt** — 7 봇 명시(Googlebot·Bingbot·OAI-SearchBot·GPTBot·PerplexityBot·
  ClaudeBot·Google-Extended) 전부 Allow:/ + 기본 + `Sitemap:` 라인.
- **docs/sitemap.xml** — `docs/**/index.html` glob 에서 도출(게이트 카운트와 항상 일치).
  허브 우선(priority 1.0) + 47 챕터(0.8), lastmod=빌드일.
- **docs/llms.txt** — 4,812 B(<5 KB). 요약 + 정준 결과(c²=B/ρ, m_p/m_e=6π⁵, δ=1/π², α=2/π,
  λ_anchor=632.99 nm) + 저자·DOI + LOCK→Derive→Gate + 허브 링크 + 섹션 색인.
- **허브 패치** — `docs/physics/index.html` head 에 **CreativeWorkSeries** JSON-LD 주입
  (멱등 마커 `<!-- vp-series-jsonld r7 -->`): name "Jamming Physics — VP Theory (Volume
  Particle)", author Person + sameAs ORCID, identifier DOI, hasPart 47 챕터 URL.
  기존 CollectionPage/WebSite/BreadcrumbList 블록은 보존.

### 3.1 허브 패치 멱등성 수정
**증상**: 매 실행마다 시리즈 블록 앞 빈 줄 1개 누적.
**원인**: 제거 정규식이 마커+스크립트만 지우고 뒤따르는 개행은 남김 → 삽입이 새 개행 추가.
**수정**: 제거 정규식에 후행 `\s*` 추가 → 누적된 빈 줄 흡수·붕괴, 재삽입 동일. 3회 실행
마커 영역 11 자 고정(불변).

## 4. gate r6 → r7 (게이트)
r6 Phase 1/2/3/4 전부 보존. v1.8 추가:
- **`words_of()` 에 `<p class="answer">` 제외 추가**(핵심). 6장이 직답을 본문 단어수에서
  제외하므로(vp-card 는 aside 로 기존 제외), 직답 주입 후에도 본문 단어수 불변(±0.5%) →
  Phase 1/2 단어 게이트 그대로 PASS(검증: phase2 violations=[]).
- **신규 `phase_search`**(`--phase search`): (a) answer-first 존재(hard) + 40~60 단어
  (soft: 밴드 밖 WARN, <12 단어만 hard-FAIL); (b) 인용 잠금마다 self-contained vp-card
  (레지스트리 단일 출처, bare "§X 참조" 0); (c) 챕터 JSON-LD ScholarlyArticle+BreadcrumbList
  +ORCID, 허브 CreativeWorkSeries/Book+BreadcrumbList+ORCID; (d) robots 7봇+Sitemap,
  sitemap <loc>==전체 docs index.html(48), llms <5 KB; (e) 문단 길이 soft.

## 5. 잠금 레지스트리 (신규) — registry/vp_locks.csv
self-contained vp-card 의 단일 출처. 10 잠금:
`lock_id, symbol, value, meaning, grade, canon_slug, match_token`.
δ(1/π²,F), α(2/π,F), ν_p(3π⁴,F), m_p/m_e(6π⁵,F), D(4.8526 pm,F), λ_anchor(632.99 nm,F),
c²(B/ρ,V), φ_jam(0.633,V), α_em(≈1/137,O), g*(c²·Ψ_yield,F).

### 5.1 CSV 인용 버그 수정(중요)
초기 수기 작성 CSV 에서 α_em 의 의미 필드("a measured input, NOT derived")에 **따옴표 없는
쉼표**가 있어 열이 1칸 밀림 → grade·canon_slug·match_token 파손(canon_slug 가 "O" 로 읽혀
잘못된 `/physics/O/` 링크·엉뚱한 페이지에 카드 방출). Python `csv.writer`(QUOTE_MINIMAL)로
전체 재생성하여 해소. 검증: 10행 정상 파싱, α_em grade=O·canon=§14·token=1/137,
`/physics/O/` 링크 0.

## 6. 레인(lane) 주의 — robots/sitemap/llms 는 Phase 5/0 기계 접근 레인 산물
이 세 파일은 본래 최상위(Phase 5) 또는 Phase 0 기계 접근 레인에 속한다. 본 패키지에서
생성한 이유는 **v1.8 SEARCH GATE(8장)가 완결 산출물 기준으로 이들을 요구**하기 때문이다.
6편 통합 세션에서 최상위 sitemap/robots 로 승격·병합할 때, 본 docs 레벨 파일은 물리편
단독 기준의 잠정본으로 간주하면 된다(허브·47 챕터 URL 은 정준 베이스 그대로라 병합 안전).

## 7. 게이트 결과 (v1.8 완성 기준)
- Phase 1 (기계 변환): **PASS** — 47 섹션/47 디렉토리, 1,272 수식 SVG(고아 0), violations=[].
- Phase 2 (결정론 파생·반작문·단어 불변): **PASS** — violations=[].
- Phase 3 (허브): **PASS**.
- Phase 4 (드리프트): **PASS** — violations=[].
- **Phase SEARCH (v1.8 신설): PASS** — answer-first 47/47, vp-card 108, 40~60 밴드 43/47,
  hard violations=[].
- 도구 지문 tools_sha16: `7d2cedb4a2e553ba`(r7 도구 반영).
- 멱등성: 전체 파이프라인(챕터+허브+기계파일) 2회 연속 실행 md5 동일.

## 8. 미해결·주의
- **40~60 밴드 밖 4 페이지**(axc-archive-schema 18w · axd-glossary 14w · axm 38w · cm 36w):
  본질적으로 짧은 색인/용어/부록 페이지로, 작문(반작문 위반) 없이는 40 단어에 못 미친다.
  게이트가 soft WARN 으로 정확히 보고(hard-FAIL 아님). 의도된 산출.
- 문단 길이 soft WARN(>3 문장) 다수: v1.8 8장에서 SOFT 항목. 본문 서술 보존 우선이라
  강제 분할하지 않음.
- 허브의 1,500~3,000 단어 마케팅 산문은 여전히 저자 선택 슬롯(출처·후크 없는 창작 영역).

— 물리편 v0.11.0. r7 / VP_SPEC_v1.8 / C4 검색 준비층 / src 305a5a24(불변).

## r7.x — 최종 문구 산문 품질 패스 (answer-first / abstract 비문 교정)

생성 텍스트(직답 `<p class="answer">`·요약 `<p class="abstract">`)의 비문을 도구 단계에서 결정론적으로 교정(HTML 수기 편집 0 → 멱등 유지). 본문 텍스트/수치/수식은 불변.

- **산문 필터 `_is_prose`**: 문장 시작의 절번호(`1.2.4`)·로마자목록(`(iii)`)·라벨코드(`F-SCHEMA-003`/`[D-11.1-1]`/`(R-c1)`)·원시 TeX(`\tau`,`c^{2}`)·소문자(라틴) 연속 단편(`used below…`)·공백누락 접합(`anchorλ_ref`,`byA_geo`,`radius0.8414`)·과도 기호수프(알파벳 비율<0.45)·고아 단편(<4어, `They.`/`This.`)를 배제. 문장 **중간**의 적법한 lock 인용은 보존.
- **완전 문장 예산**: 40~60어를 단어 슬라이스로 채우던 로직 제거 → 말미 절단 단편(`…from being.`,`…verification.`,`the wh`) 원천 차단.
- **`_trim_tail`**: 말미 매달린 접속/전치사/종속절(`…set by.`,`…locked to π, then.`)·2자 비단어(`wh`) 제거. 단문자/대문자 수식기호(R,C,X)는 보존.
- **`_presplit`**: `---`·`--`(em-dash 대용)을 문장 경계로 정규화. 단일 em-dash `—`는 내부 연결로 보존.
- **`clean()` `$`→공백**: 인라인 수식 `$…$` 경계 보존(`speed$c²$`→`speed c²`).
- **`_clean_sent` 강화**: `{}`·`( (…) )`·`:.`·인접 중복어(`as as`) 정리.
- **`subj45` 재작성**: `---` 분리·말미 매달림 정리(`Reviewers and:`→`…Reviewers`, `Misreadings ---`→`…Misreadings`).
- **abstract figure 처리 재작성**: greedy `GATEFIG` 가 스코어카드 표 전체(~1900자)·고아 단편을 abstract 에 덤프하던 버그 수정. 짧고 깨끗한 수식 구절(≤16어 산문 우선, 없으면 단일 정준 토큰 `c²=B/ρ`·`6π⁵`)로 한정해 Phase-2 `abstract-texteq`(검색-대표 수치) 요건 충족.

검증: derive_meta 재생성 후 47/47 충전·answer-first 47·vp-cards 108 유지, 반작문 위반 0, **전체 패키지 멱등(2회 md5 동일)**, **5개 게이트(phase 1/2/3/4 + search) 전부 PASS**. 산문 정리로 일부 페이지가 40어 미만이 되어 search 게이트 소프트 WARN 은 증가(하드 위반 0).
