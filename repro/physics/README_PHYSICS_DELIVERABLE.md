# 물리 백서 변환 결과물 (physics) — 6편 병합용 단일 인계 패키지

> **[v0.11.0 · 2026-06-15]** 표준 **VP_SPEC_v1.7 → v1.8** 업그레이드 적용(도구판 **r6 → r7**).
> v1.8 신설 **C4 검색 준비층**(answer-first 직답 · self-contained vp-card · robots/sitemap/llms ·
> 시리즈 JSON-LD)을 전 47 챕터+허브에 결정론·멱등·반작문으로 추가. 본문·수식·수치 무변경.
> 게이트 **5/5 PASS**(Phase 1·2·3·4 + 신설 SEARCH). 상세: **CHANGELOG_v0_11_0.md**.
> 아래 본문의 일부 수치/표현은 v0.10.0(46챕터·r6) 시점 기록이며, 현재 권위 상태는 이 배너·
> CHANGELOG_v0_11_0.md·reports/ 게이트 JSON 을 따른다(현재: 47 챕터 · r7 · VP_SPEC_v1.8).

표준: **VP_SPEC_v1.8**(동봉, `VP_SPEC_v1_8.md`). 도구판: **r7**. 소스: 저자 봉인 **v0.8** (sha `305a5a24…2271`, src_pin 일치).
이 패키지는 물리편의 **per-paper Phase 0→1→2→3 완성본**이다. 합치기·프로젝트층은 다른 세션에서 수행한다.

## 1. 완성 상태 (SPEC §8 게이트 = 완성 기준)
- Phase 1 (기계 변환): **PASS** — reports/phase1-physics.gate.json
- Phase 2 (결정론 파생): **PASS** — reports/phase2-physics.gate.json
- Phase 3 (허브): **PASS** — reports/phase3-physics.gate.json
- 46/46 섹션 페이지 + 허브 1 · 수식 SVG 1,257(고아 0) · 자리표시자 0(`(Phase 2`·`%%`·katex 0)
- src tex 불변: `305a5a247b3eedac2942d3bbdd0913b72a8c169bd21fba68f755e9ba7e442271`
  (= site_seed/src_pin.csv, 저자 v0.8.0-sealed-final). 본문·수식·수치 일절 미변경.

## 2. 디렉토리 (repo 오버레이 구조 — 그대로 겹치면 됨)
```
docs/physics/            ← 46 챕터 + index.html(허브) + _meta.json   [물리 고유]
docs/eq/physics/         ← 수식 SVG 1,257                            [물리 고유]
docs/assets/             ← 공용 CSS/폰트 (6편 공통, 중복 시 1부만)   [공용]
manifest/physics.csv     ← 물리 manifest                            [물리 고유]
reports/                 ← phase{1,2,3} 게이트 PASS · 원장(phase0-notes) · prefill · STATUS_physics
site_seed/               ← Phase 4 입력(concepts_seed) · grade_vocab · sections_map · src_pin
tools/                   ← r7 (inventory/derive_meta/build_hub/build_search_layer/gate …) [공용]
templates/               ← chapter/hub/concept                       [공용]
VP_SPEC_v1_8.md          ← 작업표준서(v1.8)                          [공용]
```
공용(공통) 항목은 6편이 동일(물리편은 r7·v1.8 로 업그레이드). 병합 시 1부만 두면 된다.

## 3. 병합 세션이 할 일 (이 패키지 밖)
- Phase 4 (개념 사전 concepts/): 6편 site_seed/concepts_seed.csv 통합 → 용어당 1페이지.
- Phase 5 (최상위 index + sitemap.xml + 구 URL 301): 6 허브 링크·카드.
- Phase 6 (전 사이트 최종 게이트): 링크·중량·노드.
- Phase 7 (Scholar 태그·Zenodo 역링크·PDF 1면·README): 허브 head 의 citation 슬롯(`<!-- citation_tags: Phase 7 -->`) 채움.

## 4. 재검증 (병합 전 무결성 확인)
```
# 이 패키지를 repo 루트에 펼친 뒤
rm -rf tools/__pycache__
python3 tools/gate.py --phase 1 --paper physics
python3 tools/gate.py --phase 2 --paper physics
python3 tools/gate.py --phase 3 --paper physics
sha256sum docs/../src/physics/*.tex 2>/dev/null   # 소스 동봉 안 함; src_pin.csv 의 sha 로 대조
```
참고: 소스 tex 자체는 본 패키지에 동봉하지 않음(저자 봉인본은 별도 vp_v0.8_ai_index_upgrade.zip).
무결성은 site_seed/src_pin.csv 의 sha 로 확인.

## 5. 판단·주의 메모
- **data-phase2 속성 유지**: 챕터 페이지의 `data-phase2="abstract|grade"` 는 저자 Phase-1 골격의
  기계 후크로, Phase 2 가 채운 필드에 그대로 남겨 두었다(렌더 비표시·게이트 무영향). 작문/구조 변경을
  최소화하는 SPEC 원칙에 따라 제거하지 않음. 프로덕션 마크업을 더 깔끔히 하려면 Phase 6 에서
  전 사이트 일괄 제거 가능(물리 단독 임의 변경은 하지 않음).
- **결정론 경계**: Phase 2(파생)·Phase 3(허브 골격)은 봉인 본문·메타에서만 채운 결정론 산출(작문 0).
  허브의 1,500~3,000단어 마케팅 산문 개요는 출처·후크가 없는 창작 영역이라 저자 선택 슬롯으로 둠
  (VP_SPEC_v1.7 변경이력 25 참조). 동봉 허브는 결정론 골격만으로 게이트 PASS.
- **AI-index/SEO 자료**(claims·FAQ·spine·VP_INDEX·queries_locked 등)는 SPEC 사이트 변환 범위 밖이라
  본 패키지에 포함하지 않음. 필요 시 저자 vp_v0.8_ai_index_upgrade.zip 에서 별도 레이어로 처리.

— 물리편 per-paper 완성. v0.11.0 / r7 / VP_SPEC_v1.8 / C4 검색 준비층 / src 305a5a24.
