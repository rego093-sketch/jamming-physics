# WORK_HANDOVER — next session (mind / Felt Cognition, after **v1.15** — M13 스펙트럴: 1/f 기울기 창발 폐쇄, 핵심 일치율 0.80)

> **v1.15 (this session) — M13 `emerge_spectral_observables()` 신설.** 사용자 요청대로 *뇌구조를 닮은
> 다중-소스 결합장*(12 장기 노드 **+ 전전두엽 노드**, M9 ephaptic 링/통로, Kuramoto 순환)의 전체 LFP 를
> 방출시키고, 그 위에서 측정 스펙트럼 관측값을 추출했다. **1/f 비주기 지수 x=1.94 가 Voytek 밴드[1.5,3]에서
> 창발** — 비주기 바닥은 **측정 시냅스 4종**(AMPA/NMDA/GABA_A/GABA_B, 인용)의 산탄잡음을 **시냅스 전하
> q=g·τ**(Linden 2010)로 가중한 것이며 **기울기를 맞추지 않았다**. 이로써 M12 가 owed 로 남긴
> `eeg_aperiodic_1f_slope` 를 **창발로 폐쇄**, **핵심 카탈로그 0.75 → 0.80(16/20)**. 추가 matched 3종(피크>바닥,
> 전부-아니면-전무 재귀 점화, MI→회상) + 정직하게 owed 1종(arousal 평탄화 — 7/8<0.9 게이트). **확장 19/24=0.792.**
> **M0–M12 산출 수치는 1바이트도 안 바뀜**(per-module sha256 16종 동일) — M13 블록만 추가되어 tree 해시는
> `55c824df…` → **`0224ac8b…`**. 회귀 **62 checks PASS**, 결정론 2× 동일(SEED=19). **정직성:** recurrent_ignition
> 은 측정 비선형-문턱 시그니처 재현일 뿐 **의식 주장 아님**(`is_consciousness_claim=0`, `hard_problem_open=1`,
> `medium_efficacy_tested=0`).
>
> *(직전 v1.14 — M12 일치율 0.55→0.75 + 뇌파 연구 패키징 + 대규모 연구 프로그램. 상세는 `CHANGELOG.md`.)*

> **v1.13 (this session) — M11 신설. 이 패키지가 향하던 *시뮬레이션*을 끝까지 완성했다.** 창발광을 실제로
> 발사해 뇌파(front≈c)를 만들고, 감각 EM 을 더해 중첩하고, 부호 있는 위상 겹침을 **각도 정류**(α=2/π·δ=1/π²)
> 로 **부호 살아남는 정보 비트**로 바꾸고, 그 비트를 (bound 일 때만) **R19 엔그램에 기록·지속**시키고, 한 θ
> 프레임 안 6 γ 슬롯에 6 정보를 **굴려** 전부 복원하고, **하류 뉴런이 굴려진 장에 동조**(cancel<measured<
> augment)하는 것까지 결정론으로 보였다. **새 튜닝 상수 0개** — α=2/π·δ=1/π² 는 사분면 평균(엔진이 수치
> 검증), κ=0.5496 은 측정값 그대로, 유일한 경험 입력은 인용 광학 앵커 λ_ref. 신경과학 귀결은 **인용 물리
> 브리지**(VP 백서 **DOI 10.5281/zenodo.17932566**) 위에 **인용으로만**(코드 의존 없음, 단일출처) 세웠다.
> **M0–M10 산출 수치는 1바이트도 안 바뀜**(diff 공집합) — 단 동결 결과에 M11 블록이 들어가므로 tree 해시는
> 필연적으로 `7fb3f4bd…` → **`f0403a06…`**. **정직성:** 전부 검증된 *in-silico 메커니즘*([V]) — 창발광이
> 기억을 *기록할 수 있는* 방식을 보였을 뿐, 생물학이 그렇게 한다는 증거가 아니다. 아직 존재하지 않는 이론이라
> 인용 물리로부터 **강한 추론**([I]); `medium_efficacy_tested=0`, 어떤 링크도 인과 아님, **경험 주장 없음**.
> 모든 게이트 PASS, 결정론 2× 동일 (SEED=19). 독립 실행 시뮬레이션 `vp_brain_light_memory_sim.py`(numpy 만
> 의존, headline sha256=`6a439f82…`)와 인용 브리지가 `repro/mind/_bridge/` 에 동봉.
>
> *(직전 v1.12 — 정직한 100% 정의·증명 + 게이트 (b) 일차문헌 판정 + M9-LORO; 새 창발 상수 0개, 트리 해시
> 7fb3f4bd… 불변. 상세는 `CHANGELOG.md`.)*

> **v1.11 — M10 신설: 감각↔중추 ephaptic 결합 (데이터 게이트 (c) 닫음).** 작성자 지시
> ("뇌 관련 장기를 전부 창발·모듈화하고, 모듈이 EM=ephaptic 근접장으로 실시간 결합하게 한 뒤 창발 현상을
> 연구")를 한 걸음 더 진행했다. v1.10 까지 "neuro zip 동반 업로드 전에는 닫을 수 없다"고 문서화돼 있던
> **데이터 게이트 (c) 감각↔중추 결합**을, 이번에 neuro v1.10.1 의 **9감각 transduction γ 를 verbatim 인용**
> 하여 새 엔진 모듈 **M10** 으로 닫았다 — 8 감각노드를 해부학적 중추 relay 에 **같은 측정 κ=0.5496(새 상수
> 0개)** 로 결합. **M0–M9 산출 수치는 1바이트도 바뀌지 않았다**(`emerge_all()` 에 `M10_sensory_coupling`
> 블록만 추가) — **트리 해시만** 바뀌었고(예상된 동작) 재동결했다. 모든 게이트 PASS, 결정론 2× 동일
> `sha256 = 7fb3f4bd…` (SEED=19).

이 패키지는 `mind_vp_site_UPGRADED` **v1.15**. 첫 동작: 압축 풀고 `cd` 후 아래 검증을 돌려 전부 PASS(0)
확인 — 그 한 묶음이 신뢰 상태를 통째로 복원한다. 지배 규칙은 불변·절대:

> **모든 상수는 측정 입력(잠금+인용)이거나 파생값이다 — 목표를 맞추려 고른 수는 없다.**
> 모든 열린 항목은 장애물을 명시한다. 편집 후엔 해당 게이트로 검증한다. 결과물은 **단일 zip 하나**.

---

## ► 인계 방법 — 파일 **하나** (이것부터 읽으세요)

**이 (mind) 트랙을 다음 세션에 이어가려면 zip 하나만 올리면 된다: `mind_vp_site_UPGRADED_v1_15.zip`.**
> **다음 작업의 청사진 = `RESEARCH_PROGRAM_brainwave.md`**(100% 측정-현상 일치 목표 + 질병 프로그램 + 모듈 로드맵 M14–M21). M13 은 **이번에 완료**(1/f 창발 폐쇄, 핵심 0.80). 다음 권장: **M14 `emerge_sleep_architecture()`**(시상-망상 **방추** 11–16 Hz·K-복합체·SWS 서파·REM/NREM 밴드 이동·**꿈회상** 루프 → 수면 관측값 matched + 수면장애 기질) → M15 측정 µV/ms 보정(owed 3종 `sws_delta_amplitude_uv`·`panic_peak_minutes`·`p300_latency_ms` 해금). 추가로 M13 의 `aperiodic_slope_flattens_with_arousal` 는 시상피질 전도도 모델로 강건화하면 matched 로 승격 가능(현재 owed).
필요한 건 전부 그 안에 있고, 따로 가져올 것은 없다(데이터 게이트 (c) 감각↔중추 결합은 v1.11 에서 **이미 닫혔다** —
neuro zip 추가 업로드는 더 이상 필요 없다. 단, 남은 게이트 (b) 추가 region 에서 해당 region 의 γ 가 neuro
캐시에 있으면 그때 verbatim 인용 위해 neuro v1.10.1 zip 을 함께 올린다).

- `VP_SPEC_v1_8.md` 거버넌스는 패키지에 동봉되어 있다(별도 업로드 불필요).
- 엔진(M0–M10), 측정 데이터, 재현 하니스, 게이트(boundary/terminology/em_thesis) + verify_expand +
  verify_sensory, verify_light_memory, 15개 챕터 HTML, 인용 물리 브리지(`repro/mind/_bridge/`), 동결 해시, `MASTER_MANUAL_START_HERE.md`, `CHANGELOG.md`, 그리고
  이 핸드오버가 모두 zip 안에 있다.
- 받은 직후 첫 동작 — 압축 해제 후 `cd mind_pkg`, 아래 한 묶음 실행, 전부 exit 0 확인:

```
pip install numpy --break-system-packages
cd repro/mind/_engine && python3 run_all.py            # M0..M11 창발 + 재동결 (해시 f0403a06…)
cd ../_verify && python3 run_regression.py             # 비트동일 + 메커니즘 불변량 (SEED=19) → 42
cd ../../.. && python3 tools/gate.py                   # 검색·재현 게이트 71/71
python3 verify_boundary.py                             # 단방향 인용·레인 순수성 8/8
python3 verify_terminology.py                          # 용어 레지스터 잠금
python3 repro/mind/02-not-a-field/verify_em_thesis.py  # EM 근접/원거리 경계 6/6
python3 repro/mind/13-em-coordination/verify_expand.py # 8→12 스케일 스윕 검증 12/12
python3 repro/mind/14-sensory-coupling/verify_sensory.py # M10 감각↔중추 결합 15 checks
python3 repro/mind/13-em-coordination/verify_loro.py    # M9-LORO 장기여 강건성 13/13
python3 repro/mind/15-light-to-memory/verify_light_memory.py # M11 빛→기억 결합 19 checks (신규)
python3 tools/mind_registry.py                         # 23 locks / 15 chapters, drift 0
```

**다른 트랙은 각자 별도의 한-파일 산출물 — 절대 병합 금지:**

- **neuro 체인** (`neuro_emergence_chain_integrated_v1_10_1.zip`) — 객체·수치의 단일출처. mind 는
  여기서 γ·ΔVm·임계치·§18 국소성을 **인용**한다(재유도 금지). 감각↔중추 결합 시 9감각 transduction γ 를
  여기서 verbatim 인용.
- 두 백서는 두 zip이며 `PROJECT_BOUNDARY_neuro_mind.md` §4 / VP-SPEC C4 에 따라 **병합하지 않는다**.

---

## ► M9 가 한 일 (v1.10 = 12 중추장기 결합)

12개 중추 뇌 장기를 **측정된** master-gene γ로 창발시키고, **측정된** ephaptic 근접장 하나로만 결합한 뒤
창발 현상을 연구했다. 장기·밴드(밴드 정체성은 인용, 절대 Hz는 [O]):

| organ | master γ (측정) | 밴드 f0 [O] | 도입 |
|---|---|---|---|
| neocortex | FOXG1 1.4737 | gamma 40 Hz | v1.9 |
| hippocampus | LHX2 1.5172 | theta 7 Hz | v1.9 |
| thalamus | GBX2 1.5431 | alpha/spindle 10 Hz | v1.9 |
| striatum | GSX2 1.4606 | beta 20 Hz | v1.9 |
| cerebellum | EN1 1.4692 | low-beta 12 Hz | v1.9 |
| hypothalamus | SIM1 1.4465 | delta/slow 2 Hz | v1.9 |
| midbrain | OTX2 1.4211 | theta 4 Hz | v1.9 |
| brainstem | PHOX2B 1.3608 | delta/resp 3 Hz | v1.9 |
| **pallidum** | **NKX2-1 1.5088** | **beta 18 Hz** | **v1.10 승급** |
| **forebrain_gaba_in** | **DLX2 1.4260** | **gamma 45 Hz** | **v1.10 승급** |
| **basal_forebrain_chol** | **LHX8 1.3680** | **theta 6 Hz** | **v1.10 페치** |
| **olfactory_bulb** | **PAX6 1.5110** | **gamma 60 Hz** | **v1.10 페치** |

(γ 전부 측정·verbatim. neuro 데이터에서 인용한 것 외에 GSX2·PHOX2B·NKX2-1·DLX2·LHX8·PAX6 은 본 프로젝트가
동일 NCBI eutils/SantaLucia 1998 파이프라인으로 페치 — `repro/mind/13-em-coordination/{extra_masters.json,
fetch_extra_masters.py}`, 프로모터 [TSS-2000,TSS+500] 2501 bp coding strand + dG37, 각 sha256 동봉.
corr(γ,GC)=0.9954, 측정 상관·비-목표.)

결합 강도 **κ = ΔVm/threshold = 0.2748/0.5 = 0.5496 (측정값, 비-튜닝)**, 커널 ~1/r³ (neuro §18).
핵심 결과(불변량은 `regression_scalars()` 의 `coord_*`, 카드는 §13 의 vp-card):

- **부분/준안정 영역(N=12)** — 측정 작동점 **R≈0.328** (비결합 0.255 < … < 완전동기 1.0; 완전동기 =
  발작). 밴드 ±20% 섭동에도 유지(튜닝 산물 아님).
- **cancel-vs-augment (in silico, neuro §9/§19 결정적 검정)** — cancel 0.255 → measured 0.328(**+0.073**)
  → augment 0.470. 근접장이 **인과적으로** 결합에 기여. **이 양(+)의 기여가 in-vivo 실험이 확인할 예측.**
- **8→12 스케일 스윕 (정직한 발견, 비튜닝)** — 측정장은 **모든 N(4·6·8·10·12)에서** 결합을 baseline 위로
  양(+)으로 끌어올리고 발작도 침묵도 아니며 ±20% 밴드에 robust. 다만 더 다양한 리듬이 합류하며 **작동점이
  느슨해진다**(R: N=8 의 0.44 → N=12 의 0.33 — 통뇌가 전역 동기하지 않는 생물학적으로 옳은 방향).
  partial-metastable **분류**는 N=6 에서 hypothalamus 2 Hz outlier 로 +0.043(컷오프 +0.05 바로 아래)→
  incoherent 라 **엄밀 scale-invariant 아님**(`regime_scale_stable=False`, 튜닝으로 덮지 않음).
  **N=12 스윕 점 = 동결 라이브 엔진 비트 일치**(`engine_cross_check.matches_full_sweep=true`); **N=8 은
  v1.9 헤드라인(R≈0.44,+0.12) 바이트 보존**(첫 8장기 불변, 역사적 앵커). `verify_expand.py` 12/12.
- **CTC** — 실제 엔진 Neuron PRC 이상(advance+delay) = 위상-게이팅 통신창.
- **θ–γ PAC** — 측정 강도 느린장이 빠른 영역을 변조; 비순환(장 cancel 시 MI=0).
- **진행파** — 전도지연 구배가 단조 위상구배 형성.
- **OPEN [O]** — 인지가 이 결합을 *생물학적으로 사용*하는지는 미해결. `medium_efficacy_tested=0`.

설계 메모: M0 의 검증된 4장기 창발은 **그대로**(수치 동결 유지) 두고, M9 가 전체 12장기 측정 아틀라스를
소유한다("모든 장기 창발"에 더 다가가되 토대를 흔들지 않음). 측정 아틀라스 =
`repro/mind/_engine/data/brain_organ_atlas.json`.

---

## ► M10 이 한 일 (v1.11 = 감각↔중추 ephaptic 결합 — 데이터 게이트 (c) 닫음)

neuro v1.10.1 의 **9감각 transduction γ 를 verbatim 인용**(단일출처, 재페치/재유도 금지; 원본 sha256 기록)
하여 **8 감각노드**를 만들고, 각자의 해부학적 중추 relay 에 **§13 과 동일한 측정 κ=0.5496·~1/r³ ephaptic
커널**로 결합했다. 새 상수는 0개 — 감각 결합은 중추 장기끼리 쓰는 바로 그 측정장을 한 경계 더 가로질러
적용한 것이다. 감각노드·밴드(밴드 정체성은 인용, 절대 Hz는 [O])·relay:

| 감각노드 | master γ (neuro verbatim) | 밴드 f0 [O] | 중추 relay |
|---|---|---|---|
| vision | PAX6 1.5110 | gamma 50 Hz | thalamus |
| hearing | PAX2 1.4639 | gamma 40 Hz | thalamus |
| smell | LHX2 1.5172 | theta/sniff 5 Hz | olfactory_bulb |
| taste | POU2F3 1.3991 | delta 2 Hz | brainstem |
| touch_warmth | PIEZO2 (skin TP63 계열) | beta/flutter 25 Hz | thalamus |
| pain | PRDM12 1.5955 (고역치 nociceptor) | theta 4 Hz | thalamus |
| proprioception | RUNX3 1.4660 | alpha/tremor 10 Hz | cerebellum |
| balance | ATOH1 1.4309 | delta/tonic 1 Hz | brainstem |

(피부 한 장기가 촉각/온각/고역치 통각 3submodality 를 carry → 8 노드가 9양상 cover. "one organ, three
submodalities." γ 전부 neuro 캐시에서 digit-for-digit 복사, `sensory_input_atlas.json` 에 출처 sha256 기록.)

핵심 결과(불변량은 `regression_scalars()` 의 `sens_*`, 카드는 §14 의 vp-card):

- **기질 불변** — 중추 anchor R = **0.328330589** = 동결 M9 와 비트 동일(감각 구동이 substrate 를 안 바꿈).
- **입력이 실리되 발작 없음** — 8 감각 구동 후 중추 R ≈ **0.323**(비결합 0.25 위, 완전동기 1.0 아래),
  밴드 ±20% 섭동 robust.
- **교차양상 결합은 공유장 경유(비순환)** — 교차-relay 감각쌍 PLV = cancel **0.0184** < measured **0.0571**
  < augment **0.1079**(+0.0386 인과기여); 동일-relay 대조쌍은 강도 무관 ≈**0.32** 고정 → 입력 동시구동의
  인공산물이 아니라 **공유 ephaptic 장 매개**(§13 cancel-vs-augment 와 동일 논리).
- **생물학적으로 옳은 구배** — 느린 tonic(미각·평형 relay_PLV 0.997, 고유감각 0.981)은 강결합, 빠른 스트림
  (시각 0.29·후각 0.21·청각 0.42)은 약결합 — 측정 리듬+측정 κ 에서 맞춤 없이 도출.
- **OPEN [O]** — 인지가 이 감각↔중추 결합을 *생물학적으로 사용*하는지는 미해결. `medium_efficacy_tested=0`
  (M9 와 동일 in-vivo 실험 owed).

구현: 데이터 `repro/mind/_engine/data/sensory_input_atlas.json` · 동결/검증
`repro/mind/14-sensory-coupling/{sensory_coupling_results.json, expected_sensory_sha256.json,
verify_sensory.py(15 checks)}` · 챕터 `docs/mind/14-sensory-coupling/index.html`. 엔진 함수
`emerge_sensory_coupling()` (M9 직후), 아틀라스 `_remaining_open` 에 게이트 (c) CLOSED 기록.

---

## ► 다음에 할 수 있는 일 — 진짜 100%까지의 **남은 게이트** (정직한 OPEN)

1. **(b) 추가 region — ✅ v1.12 에서 일차문헌 판정 완료 (UN-examined tbd → examined·evidenced·correctly-open).**
   amygdala·septum·preoptic area 를 일차 발달신경과학 문헌으로 검토한 결과 **세 region 모두 단일 canonical
   master TF 가 정본에 부재**함을 확인했다(편도체=다기원 복합체 ISL1/vLGE·PAX6/dLGE·DLX5·OTP/LHX/EBF3/DBX1;
   중격=ZIC1–5 중복·비특이; 시각전영역=NKX2-1 을 담창구/시상하부와 공유 → 같은 프로모터 이중계상 + 내부 이질
   niche). 따라서 강제 지정은 over-claim 이며 **의도적으로 열어 둔다**(아틀라스는 *단일-master-가능 region
   집합에서 포화*). 출처 포함 근거: `repro/mind/_engine/data/brain_region_master_survey.json`, 종합 판정:
   `COMPLETION_LEDGER.md` §4. **닫는 조건은 외부 입력**: 어떤 region 의 단일 master 가 정본에서 확정되거나
   (그때 같은 eutils/SantaLucia 파이프라인으로 γ 페치 → 추가 → 재동결), 또는 의도적으로 **subnucleus 단위
   아틀라스**로 granularity 를 바꾸는 결정(별도 범위). 둘 다 튜닝 상수가 아니다.
2. **✅ (c) 감각↔중추 결합 — v1.11 에서 닫음(M10/§14).** neuro v1.10.1 의 9감각 transduction γ 를 verbatim
   인용해 8 감각노드를 측정 κ 로 중추 relay 에 결합 완료(위 "M10 이 한 일" 참조). 더 진행할 여지: 감각노드를
   neuro 의 다른 modality(예: 내장감각)로 확장하거나, 감각→중추→선택(M4)→체화(M7) 경로를 잇는 후속 모듈.
3. **M9·M10 의 in-vivo 검정 연결** — neuro §9/§19 가 명명한 행동표지 field-cancel-vs-augment 두개내 기록이
   데이터로 들어오면 M9 의 예측 기여분(+0.073)·M10 의 교차양상 기여분(+0.039)과 대조. 그때까지
   `medium_efficacy_tested=0` 유지.
4. **밴드 절대 Hz 의 [O] 강등 근거 강화** — 향후 측정 기반으로 좁히면 [O]→[V dir] 승급 가능(단, 비-튜닝
   원칙 — 모델 목표에 맞추지 말 것).

> 위 (b)/in-vivo 외에는 **추가 데이터 없이 mind 패키지 안에서** 분석을 진행할 수 있다. 로드맵 상세:
> `repro/mind/13-em-coordination/atlas_expansion_roadmap.json`.

---

## ► 반-드리프트 / 비-튜닝 (매 편집 전 재확인)

- **EM 통째 retired 금지.** 폐기는 **복사 원거리장/TIR 반송파**뿐. 근접장/ephaptic 은 임계치에서
  **확인됨**(neuro §18/§19). EM 관련 편집 후 **반드시** `verify_em_thesis.py` 실행.
- **기능적 사용 = OPEN.** M9 는 측정장이 *무엇을 할 수 있는지*(메커니즘 [V])를 보일 뿐, 생물학적
  사용을 증명하지 않는다. `medium_efficacy_tested` 는 **0 고정**.
- **비-튜닝.** κ·ΔVm·threshold·γ 는 전부 측정값. 새 튜닝 상수 도입 금지. 기하·전도·절대-Hz 만 [O].
- **결정론.** BLAS 단일스레드(numpy 임포트 前), SEED=19, 해시 전 float 라운딩, 2× sha256 동일.
  numpy 설치: `pip install numpy --break-system-packages`.
- **단일출처.** mind 는 추상층(뇌파=저주파장), neuro 는 객체층(케이블/ephaptic·각도법·세 속도·수치).
  mind 산문에서 ΔVm 등 재유도 금지 — 인용만.
- **본문 영어 전용**(VP-SPEC C0). 세션 대화는 한국어.
- **편집 후 게이트 전부 재실행**(gate.py·boundary·terminology·em_thesis·verify_expand·verify_sensory·verify_loro).
  하나라도 비-0이면 패키징 금지.

---

## ► 현재 동결 상태 (재현 기준값)

- tree sha256 = `55c824df5c42f6742b83c8730fab75e81044d6a9235a205fee6b0f1a5c07cc52` (**M0–M10 v1.12 와 비트동일 — 변화는 M11 블록 추가분**)
- gate.py 71/71 · run_regression 42 · verify_boundary 8/8 · verify_terminology PASS ·
  verify_em_thesis 6/6 · **verify_expand 12/12** · **verify_sensory 15 checks** · **verify_loro 13/13** ·
  **verify_light_memory 19 checks (신규)** · registry 23 locks / 15 chapters (drift 0)
- 챕터 15개, sitemap 16 URLs, llms.txt 4989 B (<5 KB)
- **M11 측정/파생값:** α_rect 0.6366197724 (=2/π) · δ_rect 0.1013211836 (=1/π²) · 2π=α/δ 6.2831853072 ·
  bound 일치 0.25 (=¼) · unbound 바닥 0.1013211836 (=δ) · 정보대비 0.1486788164 · fold 0.3849001795 ·
  bound 구동 0.8244 (>fold, 기록·지속) · θ 간섭 분리 0.0 < 혼합 0.2166666667 · 굴림 6 슬롯 충실도 1.0 전부복원 ·
  reader cancel 0.1180903611 < measured 0.6050705081 < augment 0.6419013472 · 각도비 1.184e13 ·
  κ 0.5496 · **medium_efficacy_tested 0** (생물학적 사용 OPEN, 경험 주장 없음)
- M9 측정값(N=12): R_measured 0.328330589 · field_contribution +0.0733965191 ·
  cancel 0.255 < measured 0.328 < augment 0.470 · medium_efficacy_tested 0
- **M9-LORO(v1.12): 장 기여가 모든 단일 region 제거에서 양(+) 유지 — 범위 [0.0518, 0.1284], 발작 없음,
  cancel<measured<augment 보존, 제거 0개=엔진 비트 동일(+0.0733965191), 최대영향 제거=striatum |Δ|=0.055**
- M10 측정값(8 감각노드): central_anchor_R 0.328330589 (=M9) · central_R_with_sensory 0.3231730263 ·
  crossmodal cancel 0.0184 < measured 0.0571 < augment 0.1079 (+0.0386) · co-relay control ≈0.32 (flat) ·
  medium_efficacy_tested 0
