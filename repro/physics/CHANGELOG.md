# ================================================================
# [HTML 정본 재패키징] 2026-06-15 — VP-SPEC v1.7 헌법 적용 · TeX 비동봉 · 합치는 세션용 재료
# ================================================================
# 본문 내용 = v0.10.0 (Time and Gravity) 그대로. 형식·무결성·표준만 정본화.
# 물리 서술/수식/수치 무변경. 아래는 형식·무결성·표준 변경 요약.

## 표준 — VP-SPEC v1.7 헌법(Constitution) 신설
- 0장 헌법(최상위, 모든 조항 우선): C1 재현성 최대 보장 · C2 정본 단일화(HTML 정본, TeX 비동봉)
  · C3 재현 불가 시 사유 명시(서술의 원칙).
- 변경 이력 26–30: 단일 소스 역전(.tex 마스터 → HTML 정본), 드리프트 게이트 정본 전환,
  헌법 게이트 신설, 교차-권 DOI 레지스트리. 2·3·7·8장 헌법 정합 개정.

## 정본 단일화 — TeX 본문 소스 제거(헌법 C2; TeX·HTML 두 재료 충돌 방지, 재현성은 HTML 에서 직접)
- 삭제: txt/(본문 TeX/텍스트 SSOT), manifest/physics.eq_list.tsv(base64 TeX),
  tools/render_eq.js·tools/split.py(TeX 파이프라인), tools/originals/·remediation/.
- 확인: 패키지 내 *.tex 0 · *.eq_list.* 0 · 본문 txt/ 0.
- 유지: 수식 SVG(docs/eq/)는 렌더된 정본; 그 img alt LaTeX 는 정본 SVG 의 접근성 메타(HTML 일부),
  별도 TeX 소스 아님 → 제거 대상 아님.
- on-demand: tools/extract.py 가 정본 HTML → 텍스트/LaTeX 추출(필요할 때만 TeX 출력).

## 드리프트 게이트 정본 전환(헌법 C1·C2)
- gate.py Phase 4 검사 대상 txt/+eq_list → 정본 HTML(docs/physics/ 본문 + 수식 img alt).
  단일 진실원 tools/vp_numeric_ssot.py(표준라이브러리 결정론). --check 도 정본 HTML 대상.
- Phase 2 반작문 정밀화: abstract·description 의 § 섹션 참조(§18 등)는 발명 수치 아님 → 검사 제외.

## 무결성 정합 — 파생 인덱스를 정본 HTML 에 재산출(헌법 C1) · tools/reconcile_derived_to_html.py
  [주의] 원본 v0.10.0 은 phase1·phase2 게이트가 이미 FAIL(선재 결함, 재패키징과 무관 —
   원본에서 재실행해도 동일). 원인은 모두 stale 인덱스/파싱 버그이며 내용 손실 없음.
- §18 행 CSV 파싱 버그 교정(따옴표 없는 제목 쉼표로 한 칸 밀림 → 자동 인용 정상화;
  나머지 7개 쉼표 제목은 원래 정상 인용, 보존).
- stale 카운트 정정 — manifest: §18 eq_display 0→15, §17 88→85, words(w0/§14/§17/§18);
  _meta.json: §18 no 'VH'(오기)→18, eq_inline 15(display 오분류)→0, figures/tables None→실측,
  totals 자기일관(135,133 words / 7,735 eq).
- 고아 SVG 3개 삭제(phy-17-085/086/087; §17.4→§18 승격 후 미참조) → SVG 1,272 = data-eq 1,272.
- §18 메타 description 315자(중간 잘림)→159자(결론 선행, 한도 80–160). 메타데이터 편집(허용).

## 재현불가 원장·DOI 레지스트리 신설
- IRREPRODUCIBILITY_LEDGER.md(헌법 C3): 전 [O] 항목 집계. 핵심 2건 — 절대 중력 크기 g≈9.8m/s²
  (four-wall no-go §17.4+axg) · αₑₘ≈1/137(비증거 §14.5). 둘 다 계산량 폭발/no-go 로 패키지 내부
  결정론 재생성 불가 → [O](측정 입력), 사유를 본문 명시.
- registry/cross_volume_doi.{csv,md}: 형제 9권 개념 DOI(저자 제공). 원 6권 = VP-SPEC 2장 LOCK
  일치, 신규 3권(화학·신경과학·의식)은 개념 DOI 만 기록(제목·약칭 저자 LOCK 대기).

## 검수
- 게이트 phase 1·2·3·4 전부 PASS(원본 phase1·2 FAIL → 정합 후 PASS).
- 결정론 수치 모듈 2회 산출 sha256 동일. 정본 HTML 표시 드리프트 0.

# ---------------- 이하 원본 v0.10.0 / v0.8 이력 (보존) ----------------

# >>> v0.10.0 (time-gravity lane): featured §18 'Time and Gravity' added; gravity promoted from §17.4; exact-sqrt value [O]->[F]; G-CAP-DEPART honest-negative (gravity degenerate with GR); (1+z) handed to cosmology volume. See CHANGELOG_v0_10_0.md.

# CHANGELOG — physics_site_v0_8 정밀 보정 (PRECISE FIX)

승인 근거: 사용자 정밀 처리 승인 + VP_SPEC §1 "approved session" (LOCK 도구 수정 허용).
모든 변경은 결정론적이며 재현 가능합니다. 원본 LOCK 도구는 `tools/originals/` 에 보존.

---

## 1. 산출물(docs/)이 만들어진 경로 (provenance)

```
v0.8 소스(.tex)  →  [stock LOCK 파이프라인: split.py/inventory.py/render_eq.js]  →  원본 사이트(r6)
                 →  [remediation/fix_residues.py  : Phase-6 결정론적 사후 보정]
                 →  [remediation/recompute_meta.py: manifest/_meta 재동기화]
                 →  [tools/build_hub.py           : 허브 결정론적 재생성]
                 →  본 docs/  (잔류물 0, 상호참조 완비, 게이트 3종 PASS)
```

중요: v0.8 소스 `.tex` 는 업로드/번들 어디에도 없어(번들엔 v0.6, 업로드엔 v0.7만 존재)
**변환기를 v0.8 로 재실행할 수 없었습니다.** 따라서 산출 docs/ 는 *재변환이 아니라*
검증된 사후 보정(fix_residues.py)으로 생성했습니다. 변환기 자체의 근본 수정
(tools/inventory.py)은 **v0.8 재실행 시 적용/재게이트**하면 동일한 청정 결과를 사후 보정 없이
직접 산출하도록 만든 것이며, v0.7 에서 검증했습니다.

---

## 2. tools/gate.py — 적용됨(APPLIED, 산출 reports/ 가 이 버전으로 생성)

근본 버그: Phase-2 링크 점검이 href 의 URL 프래그먼트(`#id`)를 제거하지 않고 파일 경로로
취급 → 교차 페이지 앵커 링크(`/physics/<slug>/#<id>`)의 대상 파일 존재 검증이 사실상
불가능했음.

수정: Phase-2 링크 루프에서 경로와 프래그먼트를 분리.
```python
path = m.group(1).split("#", 1)[0]   # 프래그먼트 분리 후 파일 경로만 검증
```
효과: 새로 주입한 201개 교차 페이지 상호참조 href 가 게이트의 실제 검증 대상이 됨.
원본: `tools/originals/gate.py.orig`.

---

## 3. tools/inventory.py — 패치됨(PATCHED, v0.7 검증·v0.8 재실행 시 사용)

대상 함수: `convert_body`. 8개 근본 원인 수정. 원본: `tools/originals/inventory.py.orig`.
재현 스크립트: `remediation/patch_converter.py`.

| # | 근본 원인 | 수정 |
|---|---|---|
| 1 | 심볼 폴백 `\\([A-Za-z]+)\b` 가 `_`/`^`/숫자 앞에서 실패 → `\lambda_{ref}` 누출 | `(?![A-Za-z])` 경계로 교체 |
| 2 | 같은 폴백이 공백 누락 병합어를 통째로 흡수(`\alphaand`) | 최장 일치 접두 분리(`\alphaand`→`α and`) |
| 3 | `\textbf/\textit/\emph/\texttt/\caption/\footnote` 가 비중첩 `[^{}]*` → 중첩 중괄호 실패 | 중괄호 균형 추출기 `repl_cmd_braced` |
| 4 | `\IfFileExists{F}{T}{Fa}`·`\input` 미처리 → 스캐폴딩 누출 | `strip_iffileexists`: 골격 제거, 폴백 보존 |
| 5 | 구조 명령 `\setlength/\setcounter/\arabic/\endhead` 미처리 | 제거 규칙 확장 |
| 6 | `\hrule`·`\rule{w}{h}` 미처리 | `<hr>` 로 변환 |
| 7 | `\textsc/\textsubscript/\textsuperscript/\verb/\boldsymbol/\mathbf` 등 미처리 | unwrap/`<sub>`/`<sup>`/`<code>`/심볼화 |
| 8 | 누락 심볼/악센트/연산자(`\dot \uparrow \cos`) | 악센트(결합문자)·화살표·수학연산자 맵 추가 |
| 9 | **`\texttt{}` 가 코드 내용을 `latex2unicode` 로 통과시켜 밑줄→아래첨자 손상** | **`code_safe()` 도입, texttt 를 code_safe 로 (8항 상세는 §8)** |

검증(v0.7): convert_body 가시 텍스트 잔류물 **124→1**(남은 1=`\WPVersion` 버전 빌드
매크로, WPMAC 1줄 등록 항목). 코드 스팬 아래첨자 손상 **720→16**(나머지는 §8-B HTML
보정이 마무리). 출력 품질 표본 검증 통과.

---

## 4. remediation/fix_residues.py — Phase-6 결정론적 사후 보정 (docs/ 에 적용됨)

`<pre>/<code>/<script>/<style>` 블록과 모든 태그를 한 번에 불투명 센티넬로 치환 → 탈태그
텍스트 변환 → 복원. 적용:
- 가시 텍스트 LaTeX 명령 **122→0**, em-dash `---` **151→0**.
- 상호참조 href 주입: 총 **838개**(동일 페이지 637 + 교차 페이지 201).
- 구조 수술 23건(§18·axh `\IfFileExists` 스캐폴딩 제거(폴백 보존), axl 제목 구분자 복원).
- **`\_`→아래첨자 식별자 손상 보정**(`repair_code_underscores`, §8-B 상세).

무결성: 픽스 전/후 HTML 태그 균형 오류 프로파일 **완전 동일**(14건 모두 변환기 원산 기존
경고, 원본 r6 에도 동일) → 새 불균형 0. `alt=` 속성 **바이트 동일**(1285=1285).

호출: `python3 remediation/fix_residues.py --paper physics --root <site> --cross-page`

---

## 5. remediation/recompute_meta.py — manifest/_meta 재동기화 (적용됨)

- manifest `words`: ±0.5% 초과 **7개 페이지만** 재계산, 나머지 42개는 기준선 유지(단어
  게이트 독립 재검증). `_meta.json` 챕터 동기화, 제목 대시 정규화, `totals.words=138713`.
- eq/그림/표 카운트 전부 불변 확인(변동 시 중단).

호출: `python3 remediation/recompute_meta.py --paper physics --root <site>`
이후 `python3 tools/build_hub.py --paper physics`.

---

## 6. 의도적으로 변경하지 않은 것 (정직성·반날조 원칙)

- **끊어진 수식 참조 6건**(eq:S09_03_re_step2, eq:S09_03_step2, eq:S09_04_delta_def,
  eq:S09_04_rp_lock, eq:S11_02_a_final, eq:S13_06_me): 해당 수식이 별도 그림으로 존재하지
  않음 → id 발급은 날조 → href 없이 유지, v0.8 소스 확인 필요.
- **§18 화학 표(\IfFileExists 폴백)**: v0.6 번들에 존재하나 v0.8 src_pin "스텁0" → 주입은
  위험·범위 외. 스캐폴딩만 제거, 폴백 보존, v0.8 플래그.
- **인라인 수학 `_{ref}`/`^{5}`**: 빌드 채택 스타일 → 보존.
- **수학-텍스트 사전존재 간격 결함**(예: "rbreaks"): 단어 경계 추정은 날조 → 보존.

---

## 7. 최종 상태

- 가시 텍스트 잔류물: LaTeX 명령 0, em-dash `---` 0, 코드 스팬 아래첨자 손상 0.
- 상호참조 href: 838개 주입(교차 페이지 201 포함).
- 게이트 Phase 1/2/3: **전부 PASS**.
- HTML 무결성: 새 태그 불균형 0, alt 바이트 동일(1285), 정상 수학 첨자(`Bₑff` 등) 보존.
- manifest/_meta/허브: 상호 일관(totals.words=138713).

---

## 8. `\_`→아래첨자 식별자 손상 — 공유 도구(변환기) 사안 [추가 보정]

증상: 접근번호·파일 경로·snake_case 식별자의 밑줄이 유니코드 아래첨자로 바뀌어 깨짐
(예: `01_stiffness_to_c2`→`01ₛtiffnessₜo_c2`, `..._v0.4_2026-...`→`..._v0.4₂026-...`).

근본 원인(공유 도구): `inventory.convert_body` 의 `\texttt{}` 처리기가 내용을
`latex2unicode` 로 통과시킴 → `latex2unicode` 의 `_(\w)`→아래첨자 규칙(SUB 표
`0123456789+-=()aeoxhklmnpst`)이 코드/경로의 **리터럴 밑줄**까지 아래첨자로 변환. SUB 표에
있는 문자(s,t,l,p,숫자 등)만 바뀌므로 경로가 불규칙하게 깨짐. `\path{}` 는 내용을 그대로
(`<code>\1</code>`) 두므로 **정상** — 이 비대칭이 진단의 결정적 단서.

규모(실측, "826"은 받아들이지 않고 직접 측정):
- v0.7 소스: `\texttt{}` 2381개 중 **781개**가 아래첨자-손상 가능 밑줄 포함(+ `\path` 27개 중
  11개는 손상 가능하나 \path 는 정상 처리되어 무해).
- 산출 출력: `<code>/<pre>` 내부 아래첨자 문자 **720개**, 식별자 접미 **768개**.
- 768개 중 672개는 코드 스팬 내부(명백한 손상), **96개는 코드 밖**이며 *혼재* —
  손상 식별자(`unitₛystem`=unit_system, `conversionₚolicy`, `realizationₗock`, `sₚath`)
  + **정상 수학 첨자**(`Bₑff`=B_eff, `ρₑff`=ρ_eff, 즉 `_{eff}` 의 올바른 렌더링).
  코드 스팬 안은 일괄 역변환 안전, 코드 밖은 맹목 역변환 불가(정상 수학 훼손 위험).

정직한 공개: 본 정밀 보정의 **이전 라운드는 이 손상을 잡지 못했습니다.** fix_residues.py 가
`<code>/<pre>` 를 불투명 보호 대상으로 처리했고 변환기 패치도 texttt 의 `latex2unicode` 호출을
보존했기 때문입니다. 직전 배포 패키지에는 720+768이 그대로 남아 있었습니다.

수정(2-파트):

(A) 변환기 소스(tools/inventory.py, v0.8 재실행용) — `code_safe()` 헬퍼 추가:
`\_ \& \% \# \{ \}` 등 이스케이프만 해제 + HTML 이스케이프, **아래첨자/수학 변환 없음.**
`\texttt{}` 를 `latex2unicode(a)` → `code_safe(a)` 로 교체(2개 사이트). 검증(v0.7): 코드
스팬 아래첨자 **720→16**(98%). 잔여 16은 저자가 식별자를 수학 모드(`$...$`)에 넣었거나 JSON
키가 든 드문 구성 — 변환기 수준에서 모호(수학 모드의 `_`는 첨자가 정상)하므로 (B)가 마무리.

(B) HTML 보정(remediation/fix_residues.py, 배포 산출물에 적용) — `repair_code_underscores()`:
`<code>/<pre>` 스팬에서 아래첨자를 포함한 **식별자 토큰**(경로/버전 문자열)을 수집해
손상→복원 맵을 만들고, 그 **정확한 문자열**을 페이지 전체에서 치환(긴 토큰 우선). 코드 스팬과
**본문/abstract/description 의 동일 식별자**가 함께 복원되어 수치 일관성 유지. 정상 수학
첨자(`Bₑff` 등)는 코드 스팬에 없으므로 맵에 들어가지 않고 **절대 건드리지 않음.** 결과: 코드
스팬 아래첨자 **720→0**, `Bₑff` 보존 확인, alt 바이트 동일.

게이트 상호작용: 코드 스팬만 역변환하면 w6 본문은 `_2026`(정상)이나 abstract 의 `₂026`(코드
밖)이 남아 본문엔 "2026"·abstract엔 "026" → **반작문 게이트(invent-number:026) 실패**. 페이지
전역 맵이 abstract 동일 식별자까지 `_2026` 으로 복원 → 양쪽 "2026" → PASS. "026"은 애초에
아래첨자가 "2026"을 쪼개 만든 **가짜 수치**.

프로그램 차원 권고(§1): 원인이 **공유 변환기**이므로 `\texttt` 로 코드/경로를 표기하는 **모든
백서(물리·DNA 등)에 동일 발생**. (A) `code_safe` 패치를 공유 변환기에 일괄 적용하면 전 백서
재발 방지(재실행 시 사후 보정 불필요). 코드 밖 프로즈에만 존재하고 코드 스팬에 동반하지 않는
손상 식별자는 출력에서 정상 수학과 모호하므로 (A) 소스 적용 + 재실행이 가장 깨끗한 해소책.
