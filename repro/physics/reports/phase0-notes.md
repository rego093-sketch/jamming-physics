# Phase 0 노트 — 기반 키트 + 물리 견본 드라이런 (봉인)

## 키트 구성 (이후 LOCK 대상, SPEC 1장)
tools/ 4종: inventory.py(파싱·카운트·슬러그·유니코드 **단일 소스 라이브러리**+manifest CLI) ·
split.py(섹션 골격 분할, VP-S aside 변환, eq_list.tsv) · render_eq.js(MathJax SVG+치수 패치) ·
gate.py(8장 게이트→gate.json, tools/src 해시 기록). templates/ 3종(chapter/hub/concept).
docs/assets/css/site.css(2,819B≤50KB) + fonts/README(서브셋은 저자-로컬; 기본=시스템 스택 — 결정 기록).

## 결정 기록
- D-P0-1 (F5) 자동스텁 78 → split이 **드롭**(결정론). 선별 VP-S 50 → `<aside class="claim-strip vps">`
  위치 보존 변환(data-vps/data-cards 기계 속성 포함). 가치박스 → `_meta.json.valuebox_source`(허브 원료).
- D-P0-2 존 태그([SUPERSEDED…] 등) → `<aside class="claim-strip banner">` — 단어수 게이트의
  .claim-strip 제외 규칙과 정합(매니페스트·페이지 양쪽 동일 제외 = by construction 일치).
- D-P0-3 (F3) 섹션코드 확정표: 본문 `NN`(00–17) · Read First=`rf` · W요약=`wsum`, W.0/5/6=`w0/w5/w6` ·
  Jamming Spine=`sp` · 부록 `ax{a–r}`(마침표·**콜론** 표기 모두 인식) · 결합배너=`axepmr` ·
  G-LINK 레지스트리=`axglink` · 후반 회고 6편=`ov/bt/ea/r5/cm/ml` · 버전이력=`vh`. 미분류=zz*→게이트 FLAG.
- D-P0-4 (SPEC 7장 B) 컨테이너에 mathjax 없음 → 세션 산출은 eq_list.tsv(1,281행)+빈 svg 디렉터리,
  게이트는 `PASS_WITH_PENDING_RENDER` 명시. 저자-로컬: `npm i mathjax@3 && node tools/render_eq.js physics`
  → svg 1,281개 + html width/height 자동 패치 → `python3 tools/gate.py --phase 1 --paper physics` 재실행=PASS 기대.
- D-P0-5 단어수 정의 = inventory.convert_body 산출 텍스트(수식 유니코드 포함, aside/abstract/h1/pn 제외).
  manifest와 gate가 같은 함수를 쓰므로 ±0.5% 게이트는 구성상 0% 일치.
- D-P0-6 인라인 수식 = 결정론 latex2unicode(그리스·위첨자·frac→(a)/(b)·기호표). display = 전부 외부 SVG.

## 견본 실측 (physics, src=v0.8.0 sealed b4e28efecf646912)
sections 49 · words 139,113 · inline 6,730 · display 1,281 · fig 4 · tab 49 · dup_slugs 0 ·
**모든 페이지 ≤300KB·DOM≤3,000 충족(위반 0)** — 거대 장(08/13/17 포함)도 한도 내.

## 디버그 이력 (정직 기록)
- BUG-1: display 추출 `\[…\]`가 줄간격 `\\[3pt]`를 수식 시작으로 오인 → rf에서 가치박스 꼬리+산문
  366단어를 가짜 display로 흡수(매니페스트 words 1,942/eq 1). **수정**: 양끝 `(?<!\\)` 후방탐색 +
  가치박스 패턴 다중행(?s) 단일 소스화(split이 inventory 패턴 재사용). 복구: words 2,318 / +28 inline.
- BUG-2: gate tools 해시가 __pycache__ 디렉터리에 크래시 → isfile 필터. split에 스테일 슬러그 디렉터리
  정리 추가(61→49).

## 다음
저자: 위 D-P0-4 두 명령 → PASS 확인 → repo 병합(스펙 5장 3줄 절차). 이후 Phase 1 타 백서 5종 병렬
(같은 tools, src만 교체) · Phase 2 물리는 site_seed/sections_map.csv(74행 프리필)로 창당 부하 절감.

## r2 — 저자 독립재검(위반 0; 최대 110KB/1,199 DOM) 후 병합 전 지시 이행
- 지시① 병합 자격=PASS만: 유지(저자-로컬 렌더→gate 재실행). width/height 빈값은 렌더가 채우는 구조(확인 일치).
- 지시② slugs.csv → manifest/ : **도구 패치**(inventory 경로 일원화) — 수작업 이동 반복 제거.
- 지시③ eq_list → manifest/{paper}.eq_list.tsv : **도구 패치**(split 산출·render_eq 입력 모두) — 게시 루트 오염 원천 차단.
- 지시④ 그림: 소스 검증 결과 v0.7·v0.8 동일하게 figure env=4(전부 TikZ, includegraphics 0) — 변환 충실,
  구 v0.4 HTML의 인라인 SVG 276은 본 소스의 그림이 아님(별도 산물로 추정). 후속 실결함(TikZ→src 빈값)을
  r2로 마감: split이 `/assets/img/{code}-fig-NN.svg` 전역 일련 경로 부여 + 본 세션에서 TikZ 4종을
  standalone+pdflatex+pdftocairo로 SVG 자산화(명령 기록: `pdflatex fig{i}.tex; pdftocairo -svg`). repro/ 공백=정상(Phase 7 게이트 관할) 동의.
- 거버넌스: tools LOCK 해시 승계 — a372302058d43090(r1, 저자 교차확인 일치) → r2 해시(아래 보고).
  사유=지시②③④의 도구화(5개 백서 세션 반복 비용 제거). 승인 근거=저자 '병합 전 지시' 메시지. r1 zip 보존.

## 검수 회신 + r3 — 내용 누락 전수 감사 (저자 지시)
**eq_list 판정: 소실 아님, 이동임.** r2 zip 내 `manifest/physics.eq_list.tsv`(181,788B·1,281행) 실재 — 지시③의 도구화 결과로
docs/ 밖 manifest/ 산출이 표준이 됨(render_eq.js 입력 경로 동일 패치). 가시화: split 로그에 경로 상시 출력 추가.
**감사 발견(전부 r3로 마감):** V1 \\left/\\right 치환이 \\rightarrow를 "arrow"로 파괴 → 단어경계 가드. V2 verbatim 44블록
미처리(ASCII 다이어그램 훼손) → 주석제거 前 추출, &lt;pre&gt; 원형 보존(줄수 보존 감사 항목화). V3 quote 14·description 8·
table 5·longtable 2·mdframed 1 미처리 → 핸들러 추가(+일반 caption). V4 중첩 인라인 서식 단일패스 → 고정점 루프.
V5 eq alt의 \\label/\\tag 노이즈 제거(원문은 eq_list에 무손실). V6 전문 abstract(소스 117행) 미수록 → _meta.json
paper_abstract_source 캡처(Phase 3 자재). V7 longtable 렌더-카운터 불일치(게이트가 즉시 검출: 16장·부록I tab 1≠0) → 카운터 정합.
V8 수식 라벨 앵커 부재(eqref 착지점 없음) → figure.eq에 id=원문 label 부여. +권고G 채택: Phase 2 게이트에 "(Phase 2" 자리표시자 잔존검사 추가. +보조 검사기 tools/audit.py(비구속·보고 전용) 신설.

## 도구 변경 원장 (LOCK 승계 기록 — 기록 없는 기계 교체 금지 원칙)
| 판 | tools_sha16 | 변경 사유 | 승인 근거 |
|---|---|---|---|
| r1 | a372302058d43090 | 초판 봉인(개발 중 BUG-1 display 오인·BUG-2 해시 크래시 수정 포함) | Phase 0 세션 |
| r2 | b9fb359a8b58f8f0 | 지시②③④ 도구화: slugs→manifest/, eq_list→manifest/, TikZ 그림 자산 경로 주입 | 저자 '병합 전 지시' |
| r3 | fe57b4341aaf2644 | 감사 결함 V1~V7 마감 + 권고G(자리표시자 게이트) + audit.py 추가; 2차 보강: 인라인 후 서식 재패스·맨몸 parbox 언랩·기호 화이트리스트 정리·라벨 앵커(V8)·표 colspec 중괄호 인식·part 표제·기호맵 보강 | 저자 '검수·누락 점검' 지시 |
| r4 | 88189d26d667085c | render_eq.js 견고화(산출물 동일·치수산식/파일명 불변): undefined 매크로가 1281행 루프를 977/1281에서 중단시키던 결함 제거(전체 패키지셋 로드) · 본문 \providecommand 매크로(상수 \aVP \Danch \rproton \lrot \Beta·종 표기 \Fm \Hm \Vm \Om \Hmplus \Am) 사전선언으로 PDF와 동일 렌더 · retry-safe tex2svgPromise(폰트 비동기 로드 phy-15-015 처리) · 식별 단위 try/catch | D-P0-4가 명시한 저자-로컬 렌더 경로 = Phase 1 PASS 차단 요인(렌더 도구가 svg를 생산해야 게이트 통과). 원본 render_eq.r3 보존. |
| r5 | 09674e4df90bd579 | **(v1.7) tools/derive_meta.py 신설(Phase 2 결정론 파생)** + gate.py phase2 정정 — abstract·desc 반작문(수치⊆본문) 및 키피겨 조건부(본문에 대표 수치 있는 섹션만, aside·DOI 제외 기반) 규칙 추가. 편집 한정 = head·.abstract·grade span(전부 gate 단어수 제외영역 → 본문 단어수 구성상 불변). 본문·수식·수치 무변경. | 저자 'Phase 2 진행 + 축소 근거 판단, 아니면 VP_SPEC_v1.7 업그레이드' 지시 → 판단 결과 축소 근거 없음 → v1.7 승격·승인. |
| r6 | f637878baee1d719 | **(v1.7) tools/build_hub.py 신설(Phase 3 결정론 허브)** — _meta.json+hub.html 로 docs/{p}/index.html 생성: 전 챕터 링크(고아 0)·횡단 링크(§10)·페이지 abstract·등급 원장 개요. 출처는 봉인 본문/메타뿐(장문 산문 작문 없음 — 1,500~3,000단어 마케팅 개요는 저자 선택 슬롯). 본문·수식·수치 무변경. | 저자 'data 관리하며 진행' 지시 하 Phase 3 진행 — Phase 2 와 동일 결정론 원칙 적용(작문 불가 영역은 저자 위임). |
표준 기계 = **r6**(Phase 0~3 도구 포함). r1~r4 기배포분이 있다면 r5로 교체. src 해시 불변(305a5a247b3eedac… — 본문·수식·수치 무변경, 도구만 교체).

## 빌드·렌더 검증 기록 (physics, 본 세션 — 봉인 tex 충실재현)
- **렌더 실행:** `node tools/render_eq.js physics`(r4) → svg **1,281/1,281**(실패 0) · html data-eq width/height **1,281개 전수 패치**(빈값 0) · merror **0**(전 svg; 상수·종 매크로 식들도 실값 렌더) · 고아검사 3종(svg↔html↔eq_list) **0/0/0**.
- **게이트 재실행:** `python3 tools/gate.py --phase 1 --paper physics` → **PASS**(이전 PASS_WITH_PENDING_RENDER 해소). display_total=svg_files=1,281 · 위반 0 · sections 49/49. → `reports/phase1-physics.gate.json` 갱신.
- **tex→PDF 충실재현(독립 확인):** 봉인 tex 단독(선택적 `\IfFileExists{outputs/...table_*.tex}` 6표 부재 = 저자 봉인 빌드의 else-분기와 동일) → pdflatex 4-패스 수렴 → **478쪽 · 오류 0 · 미정의 참조 0**(저자 로그 vp_whitepaper_v0_8_draft.log와 쪽수·무오류 일치). latexmk 단독은 패스 상한으로 hub:* 219건을 일시 미정의로 표기하나 \label{hub:*} 30종이 실재 → 패스 추가 시 0 수렴(거버넌스 메모). PDF는 본 보고 묶음에 동봉.
- **불변 확인:** src tex sha = 305a5a247b3eedac2942d3bbdd0913b72a8c169bd21fba68f755e9ba7e442271 (src_pin.csv의 v0.8.0-sealed-final과 동일) — 물리·수식·수치 일절 미변경. 본 세션 변경분은 도구(r4)와 그 산출물(svg/html 치수/게이트 판정)에 국한.
