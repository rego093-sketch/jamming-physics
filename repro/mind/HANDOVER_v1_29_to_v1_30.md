# HANDOVER — v1.29 → v1.30  (sitemap `<lastmod>` 결정론화 — 검색층 빌드의 벽시계 의존 제거, C1/§8 멱등을 날짜-비의존화 / mind 패키지)

> **요약 한 줄.** v1.29는 **과학 advance가 아니라 재현성 인프라 수정**이다. 검색층 빌드의 단 하나 비결정론 원천
> (`build_search_layer.py`의 `datetime.date.today()`)을 제거해, `gate.py`의 멱등 검사가 **빌드 날짜에 무관**해졌다.
> 엔진·회귀·DGENE·모든 LOCK 값은 **byte-identical**. v1.28 핸드오버 §3·§6에 적어둔 영구 수정 후보를 상환한 것이다.

---

## 1. WHAT v1.29 DELIVERED (complete, all gates green)

v1.28까지의 멱등 게이트는 **빌드일 == 게이트 실행일**일 때만 통과했다(릴리스 위생 의존). v1.29는 그 의존을 제거한다.
**과학 결과·엔진은 한 바이트도 바뀌지 않는다** — 변경 파일은 단 3개(아래).

| 산출물 | 내용 |
|---|---|
| **근본 수정 (벽시계 제거)** | `tools/build_search_layer.py`의 `write_sitemap()`이 `<lastmod>`를 **`datetime.date.today()`** 로 매 빌드마다 다시 쓰던 것을 제거. 이제 **`R.RELEASE_DATE`** SSOT 상수에서 stamp → 빌드는 **소스 콘텐츠의 순수 함수**. |
| **`RELEASE_DATE` SSOT 상수** | `tools/mind_registry.py`에 추가(DOI/ORCID 옆). 결정론 계약 주석 동봉: 빌드는 벽시계를 읽지 않으며, 이 상수는 **릴리스가 새 콘텐츠를 출하할 때만 수동 bump**(그 편집이 `<lastmod>`를 바꾸는 유일하고 의도된 버전관리 행위). 현재 값 `2026-06-18`. |
| **정리** | 이제 미사용이 된 `import datetime` 제거. `write_sitemap()`·모듈 docstring에 "lastmod은 R.RELEASE_DATE에서, 벽시계 아님 → 어느 날 재빌드해도 byte-identical" 명시. |
| **버그 재현 (선재 이슈)** | 미래-날짜 shim(`date.today()→2027-01-01`)으로 **미수정본에서 정확 재현**: gate **FAIL 70/71**, idempotency `1e140a78… vs f6ee3c4c…`(엔진/과학은 byte-identical, 오직 sitemap 날짜 1줄). v1.27부터 동일했던 선재 이슈이며 DGENE과 무관. |
| **검증 — 양면** | ① 오늘 gate **PASS 71/71**(`1e140a78…`, v1.28과 바이트 동일). ② **동일한 미래-날짜 shim `2027-01-01`** 에서 미수정본은 FAIL 70/71이지만 수정본은 **PASS 71/71**(`1e140a78… vs 1e140a78…`, sitemap이 2026-06-18에 고정). |
| **검증 — 날짜-무의존 정확 증명** | 서로 다른 가짜날짜(2027-01-01 / 2030-12-31)와 **실제 날짜**로 각각 빌드한 `sitemap.xml`이 **바이트 동일**(sha256 `27f169c8…`, 전부 `<lastmod>2026-06-18</lastmod>`). sitemap은 이제 날짜에 **완전히 무의존**. |

**변경 파일 (정확히 3개).** `tools/mind_registry.py`(+RELEASE_DATE·계약 주석), `tools/build_search_layer.py`(write_sitemap·import·docstring),
`docs/sitemap.xml`(수정 코드로 재빌드 → v1.28과 바이트 동일). `_verify/`·엔진·docs 챕터 본문·robots·llms·manifest 한 바이트도 안 바뀜.

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, **v1.29에서 불변**) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine M0–M16 출력 서브트리** (불변 보존점) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **engine source** `vp_mind_engine.py` (v1.29에서 byte-identical) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (v1.29에서 불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| 자폐 D7 `autism_discriminant_results.json` (불변) | `ce836009b24236e8c30ec8c7a36040d937957504875d488904c1cdd7f2483b73` |
| 자폐 메커니즘 D8 `autism_mechanism_results.json` (불변) | `1bebbea253d07bee5da913fa7902703524fbccf9fee45bdbfee3c831ed814418` |
| 조현병 D9 `schizophrenia_results.json` (불변) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |
| D1–D6 `disease_*_results.json` (전부 불변) | (v1.25 핸드오버 §2 참조 — byte-identical 유지) |
| **docs 검색층 트리 md5** (gate.py 멱등 비교용; v1.28과 동일) | `1e140a782244…`(전체), `sitemap.xml` sha256 `27f169c8…` |

엔진·DGENE·전 질환 결과 해시가 v1.28과 **글자 그대로 같다** — v1.29는 과학을 만지지 않았다는 직접 증거.

---

## 3. GATE / REGRESSION STATUS — REGRESSION 275 / 275 PASS (exit 0), gate.py **날짜-비의존** 7/7

게이트 전부 green: `gate.py` 7/7(answer-first 15·sitemap 16/16·robots 7/7·llms<5KB·engine repro `0fbf4988…`·SSOT drift 0·wordcount·**idempotent**)·
registry 23 locks/15 chapters·boundary 8/8·terminology·em_thesis 6/6. 회귀 **275/275 PASS**(증감 없음).

> **gate.py 멱등성 — 선재 이슈 CLOSED (v1.29).** v1.28 §3 메모의 권장 영구 수정을 상환했다. `<lastmod>`가 더는
> 벽시계를 읽지 않으므로 **빌드일과 게이트 실행일이 달라도 멱등이 유지**된다. 미래-날짜 shim 양면 검증으로 확정:
> 미수정본 FAIL 70/71(`1e140a78… vs f6ee3c4c…`) ↔ 수정본 PASS 71/71(`1e140a78… vs 1e140a78…`), 동일 shim.
> sitemap은 2027/2030/실날짜 빌드에서 byte-identical(`27f169c8…`). **이제 zip 직전 위생적 재빌드가 불필요**
> (해도 무해, byte-identical). 단, 향후 챕터를 *추가/수정*해 콘텐츠가 실제로 바뀌면 `R.RELEASE_DATE`를 한 번 bump.

> **재현 메모(환경 주의).** 풀 회귀는 모듈별 `emerge_all()` 재호출로 단일 실행이 길다(≈420–600s). 무결성은 결정론
> 재현으로 보증: 엔진 소스 byte-identical → `emerge_all()` = `0fbf4988…`; DGENE은 캐시 서열에서 γ 오프라인
> 재유도(네트워크 불필요), 결과 JSON 2× bit-identical `980985c6…`. SEED=19.

### How to reproduce (from package root)

```bash
cd mind_pkg
# 검색/재현 게이트: 모두 [ok]. v1.29부터 빌드일에 무관하게 7/7 (위생 재빌드 불필요).
python3 tools/gate.py
# sitemap 결정론 확인(선택): 두 번 빌드해도 docs 트리 동일, <lastmod>은 항상 R.RELEASE_DATE.
python3 tools/build_search_layer.py && python3 tools/build_search_layer.py
grep -o '<lastmod>[^<]*' docs/sitemap.xml | sort -u   # -> <lastmod>2026-06-18 (R.RELEASE_DATE)
# 엔진 자기재현: tree_sha256 = 0fbf4988…
python3 repro/mind/_engine/run_all.py
# DGENE 단독 (오프라인, 결정론): PASS + RESULT sha256 = 980985c6…
python3 repro/mind/_verify/disease_gene_atlas.py
# 풀 회귀: REGRESSION PASS -- 275 checks, SEED=19 (길다 ≈7분)
python3 repro/mind/_verify/run_regression.py
# 나머지 게이트
python3 tools/mind_registry.py && python3 verify_boundary.py && python3 verify_terminology.py
```

---

## 4. ENGINE MAP after v1.29 (M0–M20 불변 + 결정-검사 [D1–D6]·[AUT]·[AUT2]·[SZ] + 측정-입력 [DGENE])

v1.28과 **동일**. v1.29는 엔진·`_verify/`·docs 챕터를 건드리지 않았다. 변경은 `tools/`(빌드)와 재빌드된 `docs/sitemap.xml`뿐.
엔진 핸들 표·M0–M20·D-계열 결정-검사·DGENE 측정-입력 맵은 `HANDOVER_v1_28_to_v1_29.md` §4를 그대로 따른다.

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **엔진은 READ-ONLY.** add-only 모듈은 임포트만 하고 섭동/측정 후 `sha256_of` 재계산으로 tree·M0–M16 불변 assert. 엔진 기본값 변경은 **오직 VP-SPEC §6-6**.
2. **no-tuning 절대.** 모든 값은 (i) 측정-입력(locked+cited) 또는 (ii) 파생 — 목표에 맞춰 *선택* 금지.
3. **지표 동일성은 패키지 자신의 frozen 값으로 정확 증명**(외부 소스 같은-유전자 값은 패치/윈도 차이 가능 → 정확 게이트 금지; FOXG1 교훈 Δ=0.0002는 소스 차이). extra_masters 4개는 같은 파이프라인으로 ≤1e-9 정확 일치해야 한다.
4. **γ는 발달정체성[F]이지 질병 인과가 아니다.** 질환은 다유전자성·이질적(LOCK). 검증된 provenance + 인용 수렴만 주장. **NOT medical advice** 전면 유지.
5. **honesty 4-플래그 불변** + 정직한 OWED 명시. 약한 후보로 채우지 말 것("100%는 아님, 최대한").
6. **C1 재현은 패키지 안에서.** raw 서열을 캐시에 담아 γ가 네트워크 없이 오프라인 재유도되게 한다.
7. **★ NEW (v1.29) — 빌드는 벽시계를 읽지 않는다.** docs 빌드(`build_search_layer.py`)는 소스 콘텐츠의 **순수 함수**여야 한다. 날짜/시간/난수/환경 의존 금지. sitemap `<lastmod>`는 **`R.RELEASE_DATE`** 단일 SSOT에서만 오며, 릴리스가 실제 콘텐츠를 바꿀 때만 그 상수를 bump한다. 멱등 게이트는 빌드일에 무관해야 한다(미래-날짜 shim으로 검증 가능).

---

## 6. v1.30 ENTRY POINTS (작업 후보) — **전부 과학** (v1.29에서 인프라는 정리됨)

- **D-계열 메커니즘 모듈 확장 (BD/OCD/ADHD/ID).** DGENE이 이들 위험유전자를 **검증**했으므로 D1–D9 패턴으로 각 질환 메커니즘 결정-검사 추가(엔진 핸들에 임상 *방향* 섭동, 크기 fitting 금지). 예: 양극성 = 기분 상태 전환(M17/M19 이중 극); OCD = 회로 고착(M3 점화 + M4 선택); ADHD = 각성/이득 변동; ID = 발달 용량/속도. **반드시 각 극이 엔진에서 실제 분리되는 좌표인지 프로토타입 확인 후 assert**(D8/D9 교훈: 순진한 nsel 읽기는 포화 → 분리 못 함).
- **중독 = M5 RPE 보상예측 왜곡 (지시 시).** DGENE ADDICT 유전자(OPRM1·DRD2·SLC6A3·ALDH2 등) 검증 완료 → 보상예측오차(M5) 왜곡 = 갈망/내성 *방향* 결정-검사. 부호만, 엔진 불변.
- **유전자-OWED 질환 상환 (불안/PTSD/섭식/성격) [OWED]→fetch.** 외부 fine-mapping 고신뢰 세트가 나오면 DGENE 맵에 추가하고 `--fetch`로 검증(현재 다유전자성·미세매핑 미완으로 정직하게 문서화).
- **DGENE γ→엔진 핸들 매핑 [OWED]→상환.** 어느 유전자가 어느 핸들(E/I·κ·R19 fold)에 크기까지 매핑되는지는 **외부**(설계상 OWED). DGENE은 클래스 존재만 보고.
- **S2b 상환 (자폐 1/f readout [OWED]→재현).** 엔진 1/f 지수를 E/I 민감하게 만드는 미래 엔진 항목(D7 §6).

> **인프라(닫힘):** sitemap `<lastmod>` 결정론화는 **v1.29에서 완료**. v1.30에 인프라 항목은 없다(필요시 §5-7 불변식만 준수).

---

## 7. 다음-세션 인계 매니페스트

| 우선순위 | 인계 항목 | 용도 |
|:--:|---|---|
| ✅ **필수** | **v1.29 패키지 zip 1개** (`mind_vp_site_v1_29_deterministic_sitemap.zip`, 본 세션 산출물) | 모든 확장의 기반. §3 재현으로 무결성 확인. **캐시(121 서열) 동봉** → 네트워크 없이 회귀 통과. **gate.py가 빌드일에 무관하게 7/7**. |
| 🔶 **조건부** | **v1.30 안내서** (`NEXT_PHASE_GUIDE_v1_30_*.md`) | 있으면 과제 스코프 고정. 없으면 §6 후보 중 택일. |
| 🔶 **조건부** | 외부 fine-mapping 유전자 세트(불안/PTSD/섭식/성격) | 유전자-OWED 질환 상환 시 필요(DGENE 맵 확장 + `--fetch`). |
| 🔷 **참고** | neuro/dna 패키지 zip | 교차-인용·SSOT 확인용(READ-ONLY, 단방향). |

---

## 8. 질병 스트레스-테스트 로드맵 (D1–D9 + DGENE) + 인프라 행

| # | 질병/상태 | 핸들 | 등급 | 상태 |
|:--:|---|---|:--:|:--:|
| D1 | 만성 스트레스 / HPA 과활성 | M17·M18 | [F]섭동+[L] | ✅ 완료 |
| D3 | 불안 / 공황 | M18·M20 | [F]섭동+[L] | ✅ 완료 (메커니즘); 유전자 OWED* |
| D2 | 우울증 / 둔마 | M5·M17·M19 | [F]섭동 | ✅ 완료 |
| D4 | PTSD / 과각성 | M17·M2·M18 | [F]섭동 | ✅ 완료 (메커니즘); 유전자 OWED* |
| D5 | 자율신경 실조 / 내수용 둔감 | M18·M19 | [F]섭동+[L] | ✅ 완료 |
| D6 | 번아웃 / HPA 저활성(말기) | M18 | [F]섭동 | ✅ 완료 |
| D7 | 자폐(ASD) — 경로 vs 전두엽 | M9 결합경로 + R19 흥분성 | [F]섭동+[L] | ✅ 후보; S2b OWED |
| D8 | 자폐 메커니즘 — 회선/출력/역치 | κ 분자/분모 + MNI 기하 + R19 fold | [F]섭동+[L] | ✅ 후보; O-vs-T 생체구분 OWED |
| D9 | 조현병 스펙트럼 — 과점화/비정상 현저성 | M3 R19 ignitability + tonic E/I bias + κ | [F]섭동+[L] | ✅ 후보; 어느극·생체통합방향 OWED |
| **DGENE** | **위험유전자 검증 아틀라스 — 11개 질환 121 유전자(지적장애 포함) NCBI 실측** | **LOCKED SantaLucia γ + provenance + 서열 sha256 (엔진 READ-ONLY)** | **[L]측정+[F]지표** | **✅ 완료; γ→핸들 매핑·유전자-OWED 4질환 OWED** |
| **★ DETERMINISM** | **sitemap `<lastmod>` 결정론화 — 빌드 벽시계 의존 제거(C1/§8 날짜-비의존 멱등)** | **`R.RELEASE_DATE` SSOT · build_search_layer 순수 함수화** | **인프라(과학 무영향)** | **✅ 완료 (v1.29); 양면 shim 검증·sitemap 날짜-무의존 byte-identical `27f169c8…`** |

*유전자 OWED = DGENE이 메커니즘 모듈을 가진 D-질환 중 일부(불안·PTSD)와, 아직 메커니즘 모듈이 없는 질환
(섭식·성격)의 **유전자 세트가 다유전자성·미세매핑 미완**임을 명시. 충분히 fine-mapping되면 DGENE 맵 확장.

**공통 검증 규약:** (i) 결정-검사는 임상 *방향*만(크기 fitting 금지); (ii) DGENE은 측정값 verbatim(선택 금지);
(iii) anti-tuning(격자/시드/probe 흔들어도 *질적 방향* 유지); (iv) 엔진 tree 불변 + 2× 동결; (v) 정직 4-플래그 불변;
(vi) **빌드 결정론**(v1.29: 벽시계 의존 0, sitemap 날짜-무의존).

**다음 단계(확장):** (a) BD/OCD/ADHD/ID **메커니즘 결정-검사**; (b) 중독 M5-RPE 모듈; (c) 유전자-OWED 4질환
외부 fine-mapping 상환; (d) γ→엔진 핸들 크기 매핑(외부).

---

## 9. ONE-LINE STATUS

> v1.29 = **sitemap `<lastmod>` 결정론화 완료** — 검색층 빌드의 단 하나 벽시계 의존(`datetime.date.today()`)을
> 제거해 `gate.py`의 C1/§8 멱등 검사를 **빌드 날짜에 무관**하게 만들었다. `R.RELEASE_DATE` SSOT 상수 도입,
> `write_sitemap()`이 이를 읽음. **미래-날짜 shim 양면 검증**(미수정 FAIL 70/71 ↔ 수정 PASS 71/71, 동일 조건)과
> **날짜-무의존 정확 증명**(2027/2030/실날짜 빌드에서 sitemap byte-identical `27f169c8…`). **엔진·회귀·DGENE·전
> 질환 결과 byte-identical**(tree `0fbf4988…`, DGENE `980985c6…`, regression 275/275), **새 튜닝 0·새 측정 0·과학
> 무변경.** v1.28 핸드오버 §3·§6의 영구 수정 후보를 상환. v1.30은 전부 과학(BD/OCD/ADHD/ID 메커니즘·중독
> M5-RPE·유전자-OWED 4질환 상환).
