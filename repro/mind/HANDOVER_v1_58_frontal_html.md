# HANDOVER v1.58 - vp_frontal Sim 2 -> canonical HTML (docs/mind/frontal/)

> 다음 세션은 이 zip 하나만 올리고 MASTER_MANUAL_START_HERE.md -> START_HERE_HANDOVER_v2.md -> 이 문서 순으로 읽으면 맥락이 복원된다. 본 문서는 한국어(세션 언어); 백서 본문(docs/)은 C0에 따라 영어 전용.

## 무엇을 했나
Sim 2(vp_frontal)는 종료(sim2_complete=True, project_closes=True)됐으나 그 서사가 거버넌스 마크다운에만 있었다. 이번 세션은 그것을 정본 사이트의 분리된 검색-수용 HTML 섹션으로 렌더했다 - docs/mind/frontal/ 아래 허브 1 + 챕터 9. 길게 서술된 부분은 SEO 관점에서 축약하지 않고 페이지로 분리했고, 지나치게 축약된 핸드오버 불릿을 자체완결 산문으로 확장했으며, 서론(허브)부터 폐쇄(08)까지 prev/next로 잇는 단일 서사로 구조화했다. 재검수 반영: 2.2의 Session-1 빌드 모듈 5종 + 2.3의 21-모듈 체인이 출처 페이지에만 있던 누락을 02 전용 페이지로 보강했고, 허브에 뇌 커버리지(포화 12영역, 14 faculty, 원칙적 제외)를 명시한 범위 절을 추가했다.

## 산출 (additive)
- docs/mind/frontal/index.html (허브, CreativeWorkSeries; 범위 절 포함) + 01..09/index.html (챕터, 02=Session-1).
- docs/assets/img/frontal/v2_atlas.png (Chunk-E 아틀라스 도식; 08에서 참조).
- docs/mind/index.html에 Part III TOC 블록; docs/sitemap.xml에 10 URL.
- 각 페이지: answer-first(40-60w), abstract, claim-strip, vp-card, JSON-LD(ScholarlyArticle+BreadcrumbList), prev/next nav. firewall 부착(consciousness_claim=0, hard problem OPEN, efficacy=0, not medical advice).

## 불변 (동결 유지)
- repro/frontal/ 엔진, 모듈, 결과, digest 전부 byte-unchanged(read-only). M9 앵커 R=0.38961455156044245, 엔진 sha e61083ae... 그대로. 모든 수치 원본 보존.
- 50-챕터 Sim-1 manifest/mind.csv, docs/mind/_meta.json 미변경 - Part III는 Sim-1 챕터가 아니라 sitemap-등록, 허브-링크된 하위 섹션.

## 뇌 커버리지 (범위 절 SSOT 요지)
organ 수준: brain_organ_atlas가 단일 명확 발생 마스터를 가진 주요 영역 집합에서 포화(12영역 포함; amygdala, septum, preoptic area는 마스터 비단일/공유로 원칙적 제외, brain_region_master_survey의 completeness 진술 근거). 기능 수준: 14 faculty 중 10 구축, 4 미결(language, volition, social cognition, metacognition). 임상: 약 9개 질환 + 공간 응용. 범위 밖: subnuclei 입도, 완전 해부/생리 지도(운동 미세회로, glia/혈관, 말초/자율계). = cognition/affect/consciousness 동역학 모델로서 주요 영역과 인지 기능의 대부분을 다루며 경계를 명시.

## 다음 작업 후보
검증 게이트(tools/gate.py)는 50-챕터 매니페스트 기준이므로 frontal 페이지는 매니페스트 밖이다. 원하면 차기 세션에서 frontal 전용 게이트를 tools/에 추가할 수 있다. 본 세션은 본문 무변경 정본화에 한정.
