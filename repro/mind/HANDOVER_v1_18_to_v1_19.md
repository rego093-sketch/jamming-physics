# HANDOVER v1.18 → v1.19 — mind / Felt Cognition

**작성:** v1.18 세션 종료 시점 · **거버넌스:** `VP_SPEC_v1_8.md` (C0–C4) · **SEED=19**
**이전 인계서:** `HANDOVER_v1_17_to_v1_18.md` (M9 ephaptic 기하 grounding 지시)
**다음 작업(결정됨):** **M9 엔진 기본값 승격(ring→측정 기하) + cascade 분석**, 그리고 **노드 분해(sulcal-bank folding)** — §3.

---

## 0. 한 줄 요약

v1.18은 직전 인계서 §3.2의 지시 — **M9 ephaptic 결합 기하를 측정 해부학으로 정초** — 를 **add-only 결정-검사(decision-check)로 완결·동결**했다. 12-노드 등간격 **링 [O]** 를 **MNI 측정 좌표 거리행렬 [L]**(8노드 정확 CoM, 4노드 대표 [O])로 바꾸고, 그 효과를 **grade == evidence 로 있는 그대로** 보고했다.

**평결(측정 결과, 정직하게 보고):** 실제 해부 기하는 장의 in-silico 기여를 **링 대비 약 1.8배로 끌어올린다**(fc **+0.07340 → +0.13468**, row-norm). **그러나 체제(regime)는 여전히 `partial_metastable`** — 전역 동기로 가지 않는다(R 0.329→0.390 < 0.9). 즉 **folding 정초는 efficacy/hard-problem을 닫지 않는다.** 이는 §3.4가 예고한 정직한 예상 결과 그대로다.

**핵심 add-only 원칙(직전 인계서 §6-6 준수):** 잠긴 엔진 `vp_mind_engine.py`는 **한 글자도 바꾸지 않았다.** M9 엔진 기본값은 여전히 링이므로 **동결 tree_sha256 `b18c8626…` 와 기존 95 checks가 그대로 유지**된다. 기하 정초는 엔진을 read-only 로 import 하는 **별도 모듈** `_verify/geometry_grounding.py` 로 구현했고, 회귀에 **17개 결정-검사 체크를 추가**(95 → **112 checks PASS**)했다.

**동결 해시.**
- 엔진 frozen tree (불변): `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7`
- 기하 atlas (locked [L] 입력): `99daa8f5cc66edb79bf84921a2222e3db74dc53c9146253b32a9b13e43c9b8e4`
- 기하 결정-검사 결과 (locked, 2× bit-identical): `8ad43a72b2f8282cae801ed8468c883b79eab0c79363ebd98621cbbfc18ff80f`

---

## 1. v1.18에서 완료·동결된 것 (건드리지 말 것 — 정확한 이력)

- **신규 `_engine/data/brain_geometry_atlas.json`** — 12 부위 MNI152(mm) 좌표 + 등급 + 출처.
  - **[L] 8노드**(정확 atlas CoM / 출판 centroid): neocortex(체적가중 AAL centroid), hippocampus, thalamus,
    striatum, cerebellum, hypothalamus, pallidum, olfactory_bulb. 합성 부위는 **AAL CoM 체적가중 centroid**(결정론적 계산).
  - **[O] 4노드**(단일 정준 centroid 없는 연장형/개방형/분산형): midbrain, brainstem, forebrain_gaba_in,
    basal_forebrain_chol.
  - 출처: AAL(Tzourio-Mazoyer 2002), 시상하부(Ogawa 2024), 기저전뇌(Zaborszky 2008/Mesulam) 등 — atlas docstring에 전수 기록.
  - **kernel 형태는 v1.17과 동일**(1/r³ 근접장); 바뀐 것은 **위치뿐**([O] 링 → [L] 해부).
- **신규 `_verify/geometry_grounding.py`** — **add-only 결정-검사 모듈**, 잠긴 엔진을 read-only import.
  세 가지 정초 결정을 **fc를 보기 전에 고정**(안티 p-해킹):
  1. **기하 [L]** — 측정 MNI 좌표(위 atlas), 부위키 정렬(`brain_organ_atlas` 키 순서로 인덱싱 → OMEGA와 정합 보장).
  2. **normalization [F]** — **row-normalization**, 물리 근거로 결과 전에 선언(아래 §2 근거). v1.17 엔진과 **동일 normalization** → 순수 [O]→[L] 기하 swap.
  3. **결정-검사(grade==evidence)** — fc·regime을 **있는 그대로** 보고. 유일한 hard assertion = 링 교차검사(아래).
- **신규 `_verify/expected_geometry_sha256.json`** — 결과·atlas·엔진-tree 해시 잠금.
- **회귀** `_verify/run_regression.py`: **95 → 112**(+17 M9-geom; 아래 §2 표). frozen tree·기존 95 불변.
- **정직 원장 불변**: `medium_efficacy_tested=0`, `hard_problem_open=1`, `consciousness_claim=0`.

---

## 2. 검증 평결 (v1.18의 핵심 정직 결과)

| 검사 | 평결 | 증거(회귀 박제) |
|---|---|---|
| **(a) 링 교차검사** | **통과 — 코드경로 검증** | 모듈의 링 경로가 동결 엔진 M9 수치를 재현: fc **+0.07340**(|Δ|<1e-4). 독립 코드가 동결값을 재현 → 하네스 신뢰. |
| **(a′) 측정 기하 평결** | **fc 상승, 체제는 부분동기** | fc **+0.13468**(링 대비 +0.061), R **0.390** → **`partial_metastable`**(R<0.9, **동기 아님**). grade==evidence. |
| **(b) 척도 불변성** | **확인 — 형상만 문제** | row-norm 하에 좌표 ×0.1/×10/×1000 → fc 변화 **2.6e-15**. 절대 척도는 무관, **상대 형상**이 fc를 정함. [O] R_BRAIN 약분과 동치. |
| **(c) 좌표 jitter ±5mm** | **체제 강건** | seed 200–209, σ=5mm(CoM 측정오차 규모) → 10/10 모두 partial_metastable. fc∈[+0.091,+0.307](형상 세부에 민감 → §3 노드분해 동기). |
| **(d) [L]-only 8노드** | **[O]에 의존 안 함** | 4개 [O] 노드 제거해도 fc **+0.08118**, partial_metastable. 결과는 약등급 좌표가 만든 게 아니다. |
| **(e) normalization 변형** | **anti-back-fit 입증** | raw 1/r³ → fc **+0.025**, **incoherent**(붕괴; cm 분리에서 점쌍극자 국소근사 무효, λ_s 미측정 [O]). **row-norm은 fc 최대화기가 아님**(raw가 더 낮음; 또 §3.1-b에서 random scatter > ring). 등록된 선택은 back-fit일 수 없다. |
| **(f) f0 ±20% 대역** | **체제 강건(M9.4 동형)** | seed 100–104, 측정 기하 → R∈[0.375,0.411], 모두 부분동기. 체제는 특정 대역의 산물 아님. |

**한 줄:** 측정 기하는 fc를 올리지만 **부분동기 체제는 그대로**다. 미결(efficacy·hard problem)의 원인은 **양자 shortfall 2.6e10**과 "생물이 장을 *쓰는지*" 미측정이지 **고전 기하가 아니다**. 기하 정초는 **의식 주장이 아니다.**

---

## 3. v1.19 진입점 (다음 작업 — 결정됨)

직전 인계서 §3.2는 세 항목을 제시했고, v1.18은 **항목 1(거리행렬 [L])·항목 3(등록 normalization [F])·결정-검사**를 완결했다. 남은 두 갈래가 v1.19다.

### 3.1 [진입점 A] 엔진 기본값 승격: ring → 측정 기하 + **cascade 분석** (직전 §3.2의 "엔진 반영")

- v1.18은 의도적으로 **엔진 기본값을 링으로 두었다**(add-only, 동결 보존). 측정 기하가 fc·regime에 미치는 효과는 **결정-검사로 박제**됐으니, v1.19에서 `emerge_coordination()`의 `POS = _ring(N)` 을 **측정 거리행렬로 교체**할 근거가 갖춰졌다.
- **이건 동결 해시를 *의도적으로* 바꾸는 작업**이다. 따라서:
  - **cascade 검증 필수.** v1.18 분석 결과: `emerge_coordination()`은 `emerge_all()` 안에서 **1회 호출**되고, 그 출력 스칼라(`field_contribution`, `R_measured`, `regime` 등)는 **최종 출력 dict로만** 흘러가며 **다른 emerge 함수가 소비하지 않는다.** 즉 M9 변경은 **잘 격리**되어 있다 — 바뀌는 것은 **M9 스칼라 + tree 해시뿐**, 다른 모듈은 byte-identical일 것으로 예상(반드시 재확인).
  - **이력 보존.** `CHANGELOG.md`에 **v1.17 동결 해시 `b18c8626…`를 영구 기록**하고, 새 tree 해시를 새 frozen으로 등록. v1.18 결정-검사 결과(`8ad43a72…`)는 승격 전 평결의 박제로 남긴다.
  - **회귀 갱신.** 승격 후 M9 스칼라가 측정값으로 바뀌므로 `expected_sha256.json` 재동결 + 해당 M9 체크 갱신. 기하 결정-검사 17개는 그대로 유지(이제 엔진 기본과 일치하므로 (a) 교차검사 타깃을 새 값으로 갱신).
  - **정직성 유지.** fc가 올라가도 regime은 partial_metastable이므로 **efficacy=0, hard_problem_open=1, consciousness_claim=0 불변**. 승격은 *기하를 정초*하는 것이지 *의식을 닫는 게* 아니다.

### 3.2 [진입점 B] 노드 분해: sulcal-bank folding (직전 §3.2 항목 2 — v1.18에서 **정직하게 보류**됨)

- 직전 인계서가 지적한 **피질 folding(꼬불꼬불함)** 비판의 핵심: 마주보는 sulcal bank가 mm 단위로 근접해 **국소 1/r³ 결합이 강해진다**. 이는 **12노드로는 포착 불가** — 부위 *내부* 형상이 필요하다.
- **v1.18 한계 인정.** 12개 부위-중심 좌표는 *부위 간* 기하만 담는다. (c) jitter 검사에서 fc가 형상 세부에 민감했던 것(±5mm가 fc를 +0.09–+0.31로 흔듦)이 바로 이 신호 — **fine 구조가 중요**하다.
- **v1.19 작업.** AAL ~78–90 노드(또는 더 미세한 parcellation)로 **분해**해 sulcal-bank 근접을 명시적으로 표현. 거리행렬을 그 해상도로 재구성하고, 동일한 결정-검사(척도불변·jitter·normalization·band)를 재적용. **여전히 측정 좌표 [L]** 이어야 하고, normalization은 동일 [F] 규율.
- **주의(안티 p-해킹).** 노드 수·parcellation 선택은 **fc를 보기 전에 고정**. 여러 parcellation을 robustness로 보고하되 fc 최대화기를 고르지 말 것.

---

## 4. 재현

```bash
cd repro/mind/_engine && PYTHONPATH=. python3 run_all.py
#   -> tree b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7 (불변), 2× 결정론

cd ../_verify && PYTHONPATH=../_engine python3 run_regression.py
#   -> REGRESSION PASS -- 112 checks (95 기존 + 17 M9-geom)

# M9 기하 결정-검사 단독 실행 (결과 JSON + 해시 재생성):
cd repro/mind/_verify && PYTHONPATH=../_engine python3 geometry_grounding.py
#   -> 결과 digest 8ad43a72... (2× bit-identical), 링 교차검사 True, regime partial_metastable

# (참고) v1.17 기하 민감도 probe (위상·normalization이 fc를 지배함을 재현):
cd repro/mind/_verify && PYTHONPATH=../_engine python3 probe_geometry_sensitivity.py
```

---

## 5. 정직성 제약 (절대 어기지 말 것 — 계승)

1. 측정값을 지어내지 마라. 없는 측정은 [O](노드 분해 시 좌표는 반드시 측정 출처).
2. 타깃에 파라미터를 맞추지 마라(back-fit 금지). 엔진은 채점값을 읽지 않는다.
3. **normalization·기하·parcellation을 결과(fc) 동기로 고르지 마라.** fc를 보기 전에 고정하고 robustness를 보고(안티 p-해킹).
4. 교정을 창발인 양 쓰지 마라.
5. `grade == evidence`. p>0.05면 효과가 커도 [O].
6. **add-only가 기본.** 단, **§3.1 엔진 승격은 동결 해시를 *의도적으로* 바꾸는 명시적 예외** — 반드시 cascade 재확인 + 이력에 v1.17 해시 영구 보존 + 회귀 재동결. 그 외 잠긴 자산은 한 글자도 바꾸지 마라.
7. **기하 grounding·노드 분해는 의식 주장이 아니다.** `efficacy=0`, `hard_problem_open=1`, `consciousness_claim=0` 유지.
