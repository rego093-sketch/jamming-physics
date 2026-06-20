# HANDOVER — v1.28 → v1.29  (정신질환 위험유전자 검증 아틀라스 DGENE — 121개 유전자/11개 질환 NCBI 실측·검증 / mind 패키지)

**DOI of record:** 概念 DOI
**10.5281/zenodo.20694404** (Zenodo deposit unchanged; this is a living-version snapshot). Governed by `VP_SPEC_v1_8.md` (C0–C4).

> **세션 시작 규약(고정).** 매 세션은 (1) 이 인계서의 **§7 다음-세션 인계 매니페스트**와 **§8 질병 로드맵**을
> 먼저 펼쳐 확인하고, (2) 작업을 끝낸 뒤 (3) **다음에 인계할 파일을 명시**하며 닫는다.

---

## 1. WHAT v1.28 DELIVERED (complete, all gates green)

v1.28은 D1–D9 결정-검사가 *인용만* 하던 **위험유전자 LOCK을 실제로 확인**하는 빠진 조각을 채웠다. D-계열은
"조현병 >270 loci", "자폐 SFARI 유전자" 같은 산문 LOCK으로 유전자를 *인용*했지만 유전자 자체를 fetch·검증한
적은 없었다. **DGENE**(Disease-GENE verification atlas)는 모든 주요 정신·신경발달 질환(**지적장애 포함**)의
큐레이션된 고신뢰 위험유전자 **121개**의 프로모터를 **NCBI RefSeq(GRCh38)에서 verbatim fetch**하고, 각
유전자의 **γ + provenance(좌표·acc·strand·길이) + 서열 sha256**을 저장한다 — γ는 **LOCKED SantaLucia-1998
NN 지표**(DNA M0 / neuro / mind M9와 동일, 윈도 `[TSS-2000, TSS+500]=2501 bp`)로 계산. raw 서열을 캐시에
담아 γ가 **오프라인 재유도 가능**(C1 재현 경로가 패키지 안에 유지). **v1.18 `geometry_grounding.py`·D1–D9와
동일한 add-only 규율**(엔진 READ-ONLY 임포트 → 엔진 소스 `e61083ae…`·전체 tree `0fbf4988…`·M0–M16
`3a1ebbbb…` 모두 불변). docs 챕터·sitemap·registry 변화 없음 — `_verify/`에만 추가.

| 산출물 | 내용 |
|---|---|
| **커버리지** | **11개 질환군, 121개 유전자, 전부 fetch+검증(실패 0).** 지적장애 **ID=52**, 자폐 ASD=39, 조현병 SCZ=24, 뇌전증/DEE EPI=23, 증후군 SYND=21, 우울 MDD=12, ADHD=11, 양극성 BD=10, 중독 ADDICT=8, 뚜렛 TS=8, 강박 OCD=7. 출처: SCHEMA·PGC3·SFARI·DDG2P·OMIM 등 문헌 인용. |
| **다면발현(pleiotropy)** | **≥3 질환 공유 18개 유전자**(NRXN1·SCN2A·GRIN2B·SYNGAP1·TSC1/2·CACNA1C 등), **32개 공유 쌍**. 인용된 큐레이션의 **직접 readout**(시냅스/염색질/이온채널/mTOR 유전자가 질환을 가로질러 반복) — 모델 산출물이 *아니다*. |
| **지표 동일성 — 정확 증명(≤1e-9)** | 패키지 *자신의* frozen extra-master 유전자(`13-em-coordination/extra_masters.json`) **GSX2/NKX2-1/PHOX2B/DLX2**를 같은 파이프라인으로 재-fetch → 캐시 서열에서 오프라인 재유도한 γ가 frozen 값과 **정확 일치**(1.4606 / 1.5088 / 1.3608 / 1.4260, 전부 ≤1e-9). 같은 지표를 같은 서열에 → 정확 일치 = **바이트 수준 지표 동일성 증명.** FOXG1은 **soft cross-check**로 강등(neuro 패키지의 *별도* RefSeq fetch 인스턴스 = 패치/윈도 스냅샷 차이로 3자리만 일치 Δ=0.0002; 지표 차이가 아니라 **소스 차이**이며 게이트 아님). |
| **사전등록 NULL** | 위험유전자 γ는 패키지 자신의 **뇌-master γ와 구별되지 않아야 한다**(둘 다 신경발달 유전자, γ는 발달-**정체성** 지표이지 질병 축이 아님). 양측 Mann-Whitney U(결정론 정규근사): 위험 γ mean=**1.4439**(n=121) vs master γ mean=**1.4588**(n=12), **U=667.5, z=−0.4594, p=0.6459 → 구별 불가.** 정직한 정답: γ는 위험유전자를 신경발달 master에서 분리 못 함. AS-IS 보고[O]. |
| **유전자-OWED 질환** | 충분히 미세매핑된 질환만 fetch; **불안·PTSD·섭식장애·성격장애**는 약한 후보로 채우는 대신 **다유전자성·아직 fine-mapping 안 됨**으로 명시 문서화(`_documented_polygenic_gene_level_owed`). 정직한 "100%는 아님, 물리적으로 최대한". |

**핵심 설계 교훈 (D-계열 교훈의 연속 — γ를 질병 점수로 박지 않는다).** 순진한 기대는 "위험유전자의 γ가
이상치를 보일 것"이지만, **사전등록 NULL이 정확히 그것을 반증**한다(p=0.65). γ는 발달 정체성[F]이지 질병
인과가 아니므로 **분리하지 못하는 것이 정답**이다. 따라서 아틀라스의 가치는 γ 점수가 아니라 **검증된 재현가능
provenance + 인용된 수렴 구조**다. 이것이 no-tuning 규율의 핵심: 목표(질병 분리)에 맞춰 지표를 *선택*하지
않고, 측정값을 정직하게 보고하면 NULL이 유지된다.

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, **v1.28에서 불변**) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine M0–M16 출력 서브트리** (불변 보존점) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **engine source** `vp_mind_engine.py` (v1.28에서 byte-identical) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| D1–D6 `disease_*_results.json` (전부 불변) | (v1.25 핸드오버 §2 참조 — byte-identical 유지) |
| 자폐 D7 `autism_discriminant_results.json` (불변) | `ce836009b24236e8c30ec8c7a36040d937957504875d488904c1cdd7f2483b73` |
| 자폐 메커니즘 D8 `autism_mechanism_results.json` (불변) | `1bebbea253d07bee5da913fa7902703524fbccf9fee45bdbfee3c831ed814418` |
| 조현병 D9 `schizophrenia_results.json` (v1.28에서 불변) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |
| **★ DGENE** `disease_gene_atlas_results.json` (NEW, v1.28) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |

**핵심 보존 불변식 (회귀가 직접 assert):** `sha256_of({M0…M20}) == 0fbf4988…` 이고 `sha256_of({M0…M16})
== 3a1ebbbb…` — **DGENE은 read-only fetch+분석 모듈이므로 엔진 출력은 한 바이트도 안 바뀐다.** v1.28이 더한
것은 `_verify/disease_gene_map.json`(큐레이션 맵) + `_verify/disease_gene_atlas.py`(fetcher+분석기) + 캐시
`disease_gene_promoters.json`(121 서열 + `_metric_controls` 4) + 결과 JSON + 회귀 [DGENE] 블록뿐.

**캐시 메모(중요).** `disease_gene_promoters.json`은 121개 유전자 + `_metric_controls`(GSX2/NKX2-1/PHOX2B/
DLX2)의 **raw 프로모터 서열**을 담는다 — 이것이 γ의 **오프라인 재유도**(네트워크 없이 회귀가 결정론적으로
통과)와 C1 재현 경로를 보장한다. 캐시를 지우면 `python3 disease_gene_atlas.py --fetch`(NCBI 접속 필요,
resumable)로 재획득해야 한다. `--fetch-controls`는 4개 control만 재획득.

**Honesty ledger (전면 불변):** `medium_efficacy_tested=0`, `hard_problem_open=1`, `consciousness_claim=0`,
`new_tuned_constants=0`. **121+4 서열은 *측정*이지 *선택*이 아니다** — 어떤 상수도 목표에 맞춰지지 않음. γ는
프로모터 발달정체성[F]이지 질병 인과 축이 아니며, 모든 질환은 **다유전자성·이질적**(단일 유전자 인과 아님).
**NOT medical advice.**

---

## 3. GATE / REGRESSION STATUS — REGRESSION 275 / 275 PASS (exit 0)

회귀 **264 → 275**(+11): DGENE 11개(frozen digest 1 + 121유전자 fetch+검증 1 + 오프라인 γ 재유도(γ/sha/서열
mismatch 0) 1 + 지표 동일성 정확 control 1 + 엔진 tree 불변 1 + M0–16 서브트리 불변 1 + 11질환 커버리지(ID 포함)
1 + 교차질환 수렴 1 + 사전등록 NULL 보고 1 + 정직 4-플래그(+NOT medical advice) 1 + overall 1). 기존
게이트(gate.py 7/7·sitemap 16/16·registry 23 locks/15 chapters·boundary 8/8·terminology·em_thesis 6/6·
main_carrier 13/13·expand 14·loro·sensory 15·light_memory 19·phenomenology 19·D1–D9)는 **모두 그대로
통과**(엔진 출력 byte-identical → 영향 없음).

> **gate.py 멱등성 메모(중요·선재 이슈).** `gate.py`의 "build is idempotent" 검사는 `build_search_layer.py`
> 재실행 후 docs 트리 해시를 비교한다. `sitemap.xml`의 `<lastmod>`가 **빌드 *날짜***이므로, **다른 날짜에**
> 빌드된 sitemap을 다른 날 게이트로 돌리면 날짜 1줄 때문에 멱등성이 깨진다(엔진/과학 결과는 byte-identical).
> 이는 **v1.27에서도 동일했던 선재 이슈**(pristine v1.27 zip에서 동일 FAIL 재현: `e383bf42 vs 1e140a78`)이며
> DGENE과 무관하다. **릴리스 위생**으로 zip 직전 `build_search_layer.py`를 1회 돌려 sitemap을 당일 빌드와
> 일치시켰고, 그 결과 gate.py가 **7/7 전부 통과**(`1e140a78 vs 1e140a78`). 연속 2회 빌드는 byte-identical이므로
> 멱등(날짜만 동일하면). **권장 영구 수정(v1.29 후보):** sitemap `<lastmod>`를 빌드 날짜 대신 **결정론적
> 고정값**(예: 릴리스 날짜 상수 또는 생략)으로 바꾸면 날짜-비의존 멱등이 된다 — 단, 이는 docs-빌드 변경이라
> DGENE 스코프 밖이라 본 버전에서는 위생적 재빌드 + 문서화로 처리했다.

> **재현 메모(환경 주의).** 풀 회귀는 모듈별 `emerge_all()`(≈28s) 재호출 때문에 단일 실행이 길다(≈420–600s).
> 무결성은 **결정론 재현**으로 보증: 엔진 소스 byte-identical → `emerge_all()` = `0fbf4988…`; DGENE은 캐시
> 서열에서 γ를 **오프라인 재유도**하므로 네트워크 없이 결정론적, 결과 JSON 2× bit-identical(`980985c6…`),
> standalone PASS([DGENE]와 동일 assert). SEED=19. 로컬에서는 아래로 직접 실행.

### How to reproduce (from package root)

```bash
cd mind_pkg
# (선택, 한 번만) NCBI에서 프로모터 획득 → 캐시. zip에 캐시 동봉되어 평소 불필요.
#   python3 repro/mind/_verify/disease_gene_atlas.py --fetch
# DGENE 단독 (오프라인, 결정론): PASS + RESULT sha256 = 980985c6…
python3 repro/mind/_verify/disease_gene_atlas.py
# 엔진 자기재현: tree_sha256 = 0fbf4988…
python3 repro/mind/_engine/run_all.py
# 풀 회귀: REGRESSION PASS -- 275 checks, SEED=19  (길다 ≈7분)
python3 repro/mind/_verify/run_regression.py
# 검색/재현 게이트: 모두 [ok] (zip 직전 build_search_layer 1회 후)
python3 tools/gate.py
# 나머지 게이트
python3 tools/mind_registry.py && python3 verify_boundary.py && python3 verify_terminology.py
```

---

## 4. ENGINE MAP after v1.28 (M0–M20 불변 + 결정-검사 [D1–D6]·[AUT]·[AUT2]·[SZ] + 측정-입력 [DGENE])

```
[engine]  vp_mind_engine.py  M0–M20  (READ-ONLY, tree 0fbf4988…, M0–M16 3a1ebbbb…)  — 불변
--- _verify/ 결정-검사 (엔진 READ-ONLY 임포트, 임상 *방향*만 섭동) ---
[D1–D6] disease_stress_tests.py   만성스트레스·불안·우울·PTSD·자율실조·번아웃
[AUT]   autism_discriminant.py    자폐 D7 — 결합경로 vs 전두엽 (3신호 + 판별)
[AUT2]  autism_mechanism_discriminant.py  자폐 D8 — 회선/출력/역치 3-way + 가역성
[SZ]    schizophrenia_discriminant.py     조현 D9 — 자폐-T 거울상 "과점화"
--- _verify/ 측정-입력 (엔진 READ-ONLY emerge로 불변 assert, NCBI 실측) ---
[DGENE] disease_gene_atlas.py     정신질환 위험유전자 121개 검증 아틀라스 (NEW v1.28)
        ├ disease_gene_map.json            121 유전자 → 질환/기능클래스 큐레이션 맵
        ├ disease_gene_promoters.json      캐시: 121 raw 서열 + _metric_controls 4
        └ expected_disease_gene_atlas_sha256.json  결과 동결 980985c6…
```

엔진 모듈 맵(M0–M20) 자체는 v1.20과 동일 — §4 상세는 `HANDOVER_v1_20_to_v1_21.md §4` 참조.
**[DGENE]은 결정-검사(D-계열)와 다른 범주다:** 엔진을 섭동하지 않고, 외부 측정값(유전자 프로모터)을 LOCKED
지표로 검증해 D-계열의 *인용* LOCK을 *재현가능*하게 만든다(type-(1) 측정-입력 advance, COMPLETION_LEDGER §1).

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **엔진은 READ-ONLY.** 모든 add-only 모듈(D-계열 결정-검사 + DGENE 측정-입력)은 엔진을 임포트만 하고
   섭동/측정 후 `sha256_of` 재계산으로 tree·M0–M16 불변을 assert한다. 엔진 기본값 변경은 **오직 VP-SPEC §6-6**.
2. **no-tuning 절대.** 모든 값은 (i) 측정-입력(locked+cited) 또는 (ii) 파생 — 목표에 맞춰 *선택* 금지.
   *DGENE 적용:* 121+4 프로모터 서열은 NCBI에서 **측정**, γ는 LOCKED SantaLucia로 **파생**. **사전등록 NULL을
   먼저 박고**(γ가 질병을 분리해야 한다 ❌) 측정값이 그것을 반증하게 둔다 — 정직한 NULL이 정답.
3. **지표 동일성은 패키지 자신의 frozen 값으로 정확 증명한다.** 외부 소스(neuro 등)의 같은-유전자 값은 패치/
   윈도 스냅샷이 다를 수 있으므로 **정확 게이트로 쓰지 말 것**(FOXG1 교훈: Δ=0.0002는 지표가 아니라 소스 차이).
   패키지 자신의 extra_masters 유전자는 같은 파이프라인으로 ≤1e-9 정확 일치해야 한다 — 이것이 진짜 게이트.
4. **γ는 발달정체성[F]이지 질병 인과가 아니다.** 어떤 add-only 작업도 γ로 질병 점수/병인을 *주장*하면 안 된다.
   질환은 다유전자성·이질적(LOCK). 검증된 provenance + 인용 수렴만 주장. **NOT medical advice** 전면 유지.
5. **honesty 4-플래그 불변** + 정직한 OWED 명시. *DGENE 적용:* 유전자-OWED 질환(불안/PTSD/섭식/성격)은
   다유전자성·미세매핑 미완으로 문서화 — 약한 후보로 채우지 말 것("100%는 아님, 최대한"의 실천).
6. **C1 재현은 패키지 안에서.** raw 서열을 캐시에 담아 γ가 네트워크 없이 오프라인 재유도되게 한다(회귀 결정론).

---

## 6. v1.29 ENTRY POINTS (작업 후보)

- **D-계열 메커니즘 모듈 확장 (BD/OCD/ADHD/ID).** DGENE이 이제 이들 질환의 위험유전자를 **검증**했으므로,
  D1–D9 패턴으로 각 질환의 메커니즘 결정-검사를 추가할 수 있다(엔진 핸들에 임상 *방향* 섭동, 크기 fitting 금지).
  예: 양극성 = 기분 상태 전환(M17/M19 이중 극); OCD = 회로 고착(M3 점화 + M4 선택); ADHD = 각성/이득 변동.
  반드시 **각 극이 엔진에서 실제로 분리되는 좌표인지 프로토타입 확인 후 assert**(D8/D9 교훈).
- **중독 = M5 RPE 보상예측 왜곡 (지시 시).** DGENE ADDICT 유전자(OPRM1·DRD2·SLC6A3·ALDH2 등) 검증 완료 →
  보상예측오차(M5) 왜곡 = 갈망/내성 *방향* 결정-검사. 반드시 부호만, 엔진 불변.
- **유전자-OWED 질환 상환 (불안/PTSD/섭식/성격) [OWED]→fetch.** 외부에서 fine-mapping된 고신뢰 유전자
  세트가 나오면 DGENE 맵에 추가하고 `--fetch`로 검증(현재는 다유전자성·미세매핑 미완으로 정직하게 문서화).
- **DGENE γ→엔진 핸들 매핑 [OWED]→상환.** 어느 유전자가 어느 엔진 핸들(E/I·κ·R19 fold)에 크기까지
  매핑되는지는 **외부**(설계상 OWED). DGENE은 클래스 존재(GLU/GABA/ION vs SYN/CHROM/TF/SIG)만 보고.
- **sitemap `<lastmod>` 결정론화 (gate.py 날짜-비의존 멱등).** §3 메모 참조 — 빌드 날짜 대신 고정값/생략으로
  바꾸면 멱등 검사가 날짜에 무관해진다(작은 docs-빌드 수정; 과학 결과 무영향).
- **S2b 상환 (자폐 1/f readout [OWED]→재현).** 엔진 1/f 지수를 E/I 민감하게 만드는 미래 엔진 항목(D7 §6).

---

## 7. 다음-세션 인계 매니페스트

| 우선순위 | 인계 항목 | 용도 |
|:--:|---|---|
| ✅ **필수** | **v1.28 패키지 zip 1개** (`mind_vp_site_v1_28_disease_gene_atlas.zip`, 본 세션 산출물) | 모든 확장의 기반. §3 재현으로 무결성 확인. **캐시(121 서열) 동봉** → 네트워크 없이 회귀 통과. |
| 🔶 **조건부** | **v1.29 안내서** (`NEXT_PHASE_GUIDE_v1_29_*.md`) | 있으면 과제 스코프 고정. 없으면 §6 후보 중 택일. |
| 🔶 **조건부** | 외부 fine-mapping 유전자 세트(불안/PTSD/섭식/성격) | 유전자-OWED 질환 상환 시 필요(DGENE 맵 확장 + `--fetch`). |
| 🔷 **참고** | neuro/dna 패키지 zip | 교차-인용·SSOT 확인용(READ-ONLY, 단방향). |

---

## 8. 질병 스트레스-테스트 로드맵 (D1–D6 완결 + 자폐 D7/D8 + 조현 D9 + 유전자 검증 DGENE)

| # | 질병/상태 | 핸들 | 등급 | 상태 |
|:--:|---|---|:--:|:--:|
| D1 | 만성 스트레스 / HPA 과활성 | M17·M18 | [F]섭동+[L] | ✅ 완료 |
| D3 | 불안 / 공황 | M18·M20 | [F]섭동+[L] | ✅ 완료 (메커니즘); 유전자 OWED* |
| D2 | 우울증 / 둔마 | M5·M17·M19 | [F]섭동 | ✅ 완료 |
| D4 | PTSD / 과각성 | M17·M2·M18 | [F]섭동 | ✅ 완료 (메커니즘); 유전자 OWED* |
| D5 | 자율신경 실조 / 내수용 둔감 | M18·M19 | [F]섭동+[L] | ✅ 완료 |
| D6 | 번아웃 / HPA 저활성(말기) | M18 | [F]섭동 | ✅ 완료 |
| D7 | 자폐(ASD) — 경로 vs 전두엽 | M9 결합경로(S1·S3) + R19 흥분성(S2) | [F]섭동+[L] | ✅ 후보; S2b OWED |
| D8 | 자폐 메커니즘 — 회선/출력/역치 | κ 분자/분모 + MNI 기하 + R19 fold + 세타 공급 | [F]섭동+[L] | ✅ 후보; O-vs-T 생체구분 OWED |
| D9 | 조현병 스펙트럼 — 자폐-T 거울상 "과점화/비정상 현저성" | M3 R19 ignitability + tonic E/I bias + ephaptic 상한 κ | [F]섭동+[L] | ✅ 후보; 어느극·생체통합방향 OWED |
| **DGENE** | **위험유전자 검증 아틀라스 — 11개 질환 121 유전자 (지적장애 포함) NCBI 실측** | **LOCKED SantaLucia γ + provenance + 서열 sha256 (엔진 READ-ONLY)** | **[L]측정+[F]지표** | **✅ 완료 (121/121 검증·오프라인 재유도·지표 동일성 정확 증명·사전등록 NULL 유지); γ→핸들 매핑·유전자-OWED 4질환 OWED** |

*유전자 OWED = DGENE이 메커니즘 모듈을 가진 D-질환 중 일부(불안·PTSD)와, 아직 메커니즘 모듈이 없는 질환
(섭식·성격)의 **유전자 세트가 다유전자성·미세매핑 미완**임을 명시한 것. 충분히 fine-mapping되면 DGENE 맵 확장.

**공통 검증 규약:** (i) 결정-검사는 임상 *방향*만(크기 fitting 금지); (ii) DGENE은 측정값 verbatim(선택 금지);
(iii) anti-tuning(격자/시드/probe 흔들어도 *질적 방향* 유지 / DGENE은 NULL을 먼저 박음); (iv) 엔진 tree 불변 +
2× 동결; (v) 정직 4-플래그 불변; (vi) 판별/지표-동일성 assert.

**DGENE 다음 단계(확장):** (a) 검증된 유전자를 발판으로 BD/OCD/ADHD/ID **메커니즘 결정-검사** 추가(D-계열
패턴); (b) 중독 M5-RPE 모듈; (c) 유전자-OWED 4질환 외부 fine-mapping 상환; (d) γ→엔진 핸들 크기 매핑(외부).

---

## 9. ONE-LINE STATUS

> v1.28 = **정신질환 위험유전자 검증 아틀라스 DGENE 완료** — D-계열이 *인용만* 하던 유전자 LOCK을 **실제로
> 확인**: 모든 주요 정신·신경발달 질환(**지적장애 포함, 11개 질환군**)의 고신뢰 위험유전자 **121개** 프로모터를
> **NCBI RefSeq에서 verbatim fetch**, LOCKED SantaLucia γ + provenance + 서열 sha256으로 **오프라인 재유도
> 가능**하게 검증(실패 0). **지표 동일성은 패키지 자신의 frozen extra-master 4개(GSX2/NKX2-1/PHOX2B/DLX2)로
> ≤1e-9 정확 증명**(FOXG1은 소스차이 soft check로 강등). **사전등록 NULL**(위험 γ vs 뇌-master γ, **U=667.5,
> p=0.65**)은 **구별 불가 → AS-IS 보고**: γ는 발달정체성[F]이지 질병 점수가 아니다(정직한 정답). 18개 다면발현
> 유전자·32 공유쌍 = 인용 큐레이션의 직접 readout. 유전자-OWED 4질환(불안/PTSD/섭식/성격)은 다유전자성·
> 미세매핑 미완으로 문서화("100%는 아님, 최대한"). 엔진 tree `0fbf4988…`·M0–M16 `3a1ebbbb…` **불변**, 결과
> `980985c6…`(2× bit-identical), 회귀 **264→275 PASS**, 정직 원장 **불변(0/1/0/0)**, **NOT medical advice**.
> 다음 인계 = **{v1.28 zip}**; 다음 과제 = **D-계열 메커니즘 확장(BD/OCD/ADHD/ID) 또는 중독(M5) 또는
> 유전자-OWED 4질환 상환 또는 sitemap lastmod 결정론화**.
