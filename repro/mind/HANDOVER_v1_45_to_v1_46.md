# HANDOVER — v1.45 → v1.46  (AD-T3b-L 알츠하이머 증상-네트워크 레버 §38 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.45의 성격 (문턱-이동 논리 기존-사례 적용 #7 · 시리즈 3번째이자 가장 깊은 PARTIAL [L]).** v1.37이 상속한
> 문턱-이동 개입 논리를 v1.44 핸드오버 §5의 **갈래 A 잔여**(T3b 알츠하이머, 도달성 [L] 선판단)에 따라 알츠하이머에
> 능동 적용했다. 알츠하이머의 세 증상 기술(콜린성-결핍·글루탐산-흥분독성·네트워크-과흥분)은 모두 **증상 표면**일 뿐,
> 그 아래 지배적 **신경퇴행 진행**(누적·불가역 손실 = 질병의 핵심)을 건드리지 못한다. 이 기질을 상속 L1/L2/L3 프레임에
> **도달성 기준**으로 매핑한 결과가 **시리즈 3번째이자 가장 깊은 PARTIAL [L] 적합**이다. 도달 표면은 **순간 증상(SYMP)
> 작동점**(L1/L2/L3 전부)이고 **분할 부호(SPLIT SIGN)**(콜린성 구동↑·흥분독성↓·억제↑ — 시리즈 최초의 순수-증상
> 다방향 재균형)이지만, 지배적 결함 = **PROG 신경퇴행-진행 축**은 **가장 깊은 이유로 도달불가**다. 앞 두 부분-적합을
> 합치고 그 위에 셋째를 더한다: ① fold가 아닌 **게인/손실**(ADHD 교훈) AND ② 시간에 걸친 **진행** = 가소성(E0-층)
> 변수(중독 교훈) AND ③ 그를 넘어 **퇴행** = 누적·**불가역 손실** = **E0 DECAY**, 중독의 **E0 GAIN의 구조적 역**.
> 중독은 가소성이 흔적을 **공고화**(레버가 못 지움), 알츠하이머는 퇴행이 기질을 **상실**(레버가 못 재건) — 두 질환이
> 같은 E0 가소성 층을 **반대 방향**(축적 vs 손실)으로 만난다. 그래서 순간 콜린성 톤을 완벽 복원하는 레버조차 누적
> 손실을 멈추지 못하고, 콜린에스테라아제 억제제·메만틴은 **증상 전용·진행을 늦추지 못한다**.

---


## 1. WHAT v1.45 DELIVERED (complete, 두 게이트 green)

### 1.1 §38 알츠하이머 증상-네트워크 레버 (the MAP, AD-T3b-L) · **시리즈 3번째·가장 깊은 PARTIAL [L] · L3-지배+L1·L2·분할 부호 · PROG 축 명명-도달불가 = E0 DECAY**

- **모듈.** `repro/mind/_verify/alzheimers_threshold_levers.py` (지도 sha **`68029dab06ed152da919bdc3d0529058d06226356027e803647441a82b4067fe`**;
  결정론 2× 검증). 동일 R19 기질 위 문턱-레버 분해, 새 메커니즘·새 튜닝 상수 0, 엔진 READ-ONLY.
- **8번째 분포 = L3-지배 + L1·L2 둘 다 관여 · 분할 부호.** 레버 9개 중:
  - **L3 4개**(상류 콜린성 구동, **복원↑**): ACHE·BCHE(콜린에스테라아제 — 도네페질/리바스티그민/갈란타민 방향), CHRNA7(α7 니코틴성), CHRM1(M1 무스카린성).
  - **L1 2개**(글루탐산 흥분독성, **감소↓**): GRIN2B·GRIN2A(메만틴 방향).
  - **L2 3개**(억제, **복원↑**): GABRA1·GABRA5·GABRB3(AD 네트워크 과흥분 대항).
  - 교정 부호가 **분할**(콜린성↑·흥분독성↓·억제↑) — **시리즈 최초의 순수-증상 다방향 재균형**. 중독의 L3-지배+L1/L2와 거시 형태는 닮았으나 **분할 부호 + 순수-증상 도달**로 구별.
- **시리즈 3번째이자 가장 깊은 PARTIAL [L]**(fit_index_in_series=3, deepest_partial=True). 도달 표면 = 순간 증상(SYMP) 축(L1/L2/L3); 지배 결함 = **PROG 신경퇴행-진행 축**은 **가장 깊은 이유**로 도달불가: ① fold 아닌 게인/손실(ADHD) AND ② 시간 진행=가소성 E0-층 변수(중독) AND ③ **퇴행=누적·불가역 손실=E0 DECAY**(중독 E0 GAIN의 **구조적 역**).
- **PROG 축 6 유전자 명명·`[F] NOT REACHED`**(`out_of_reach_targets`): APP(아밀로이드 원천·상염색체-우성 조기-발병), PSEN1/PSEN2(γ-세크레타제 촉매 소단위), MAPT(타우), APOE(최강 흔한 위험 대립유전자 ε4), TREM2(미세아교 수용체) — γ 동반·비-레버.
- **γ는 도달성과 직교(ORTHOGONAL), 더 깨끗.** 최강 3개 프로모터(CHRM1 γ≈1.513·ACHE γ≈1.510·CHRNA7 γ≈1.496)=모두 도달 가능 콜린성 레버; 최약 2개(BCHE γ≈1.233·GABRA1 γ≈1.246)=또한 도달 가능 레버; 6개 out-of-reach PROG=강성 **중간 군집**(|h_sp|≈0.622–0.693) → 강성은 어느 축인지도 도달 가능성도 예측 못함.
- **5개 read verbatim 재사용**(γ 가닥-대칭): GRIN2A·GRIN2B·GABRA5·GABRB3(자폐 캐시), GABRA1(뇌전증 캐시). 10개(ACHE·BCHE·CHRNA7·CHRM1·APP·PSEN1·PSEN2·MAPT·APOE·TREM2) GRCh38 strand-aware live fetch(provenance `alzheimers_levers_promoters.cache.json`).
- **부담-가중 우선순위**(declared B0.40/U0.35/G0.25, cited tiers; `alzheimers_burden_prioritisation.py`). **미충족 시그니처=가장 깊은 부분-적합**: 순위 최상단 비실행 — **APP #1**(4.75)·**APOE #2**(4.50) 둘 다 out-of-reach PROG(질병-수정=분야 최대 미충족, 레카네맙/도나네맙조차 임상 저하율 소폭만 감소), 선두 실행 가능 **ACHE #3**(4.30), floor=**3**(ADHD 2보다 높음). **decoupling**: 최강 프로모터 CHRM1 #6(최상위 아님), 최우선 APP 강성 7위.
- **금지-주장 스캐너 = 치매 2클래스 추가**(fail-closed, negation-guarded, 미끼 자기-테스트): **CURE_REVERSAL**(역전/치유/예방/진행-정지/잃은-기억-복원/뉴런-재생/기적-치유)·**DIGNITY**(빈-껍데기/더는-사람이-아님/식물인간/이미-사라짐/치료-가치-없음). 자신의 인용 면책 문구가 스캐너를 오발화하지 않도록 `slow/disease-modifying` 패턴을 부정-가드 CURE_REVERSAL로 이동하고 항체 서술을 "임상 저하율을 소폭 줄임"으로 정밀화(인용 정확성 유지).
- **L3-정직성 게이트**(`alzheimers_l3_honesty.py`, PASS): L3 지배 + L1>0 AND L2>0 + 분할-부호 SYMP 도메인 제한 + PROG-축 명명-도달불가 + PARTIAL [L]·deepest 단언.
- **4-step 집계기**(`run_all_alzheimers_levers.py`, ALL PASS): map → burden → l3_honesty → forbidden_scan + TRUE 결정론 재검(map 재실행·결과 재해시 vs expected = True).
- **아틀라스 등록.** `run_all_atlas.py`에 **16번째 시민 AD-T3b-L** 등록 → **ALL PASS 16/16, 19 CONFIRMED 0 REFUTED, engine 파일 byte-unchanged**.

### 1.2 출판 표면 (SEO 챕터)

- 신규 영어 챕터 **§38 「Alzheimer's threshold levers」**(`docs/mind/38-alzheimers-threshold-levers/index.html`,
  model 4100w, 9 H2 영어-전용 본문). 아카이벌 생성기 `tools/_gen_ch38_alzheimers_levers.py`(byte-identical 재현 —
  answer/vp-card는 `build_search_layer.py`가 registry에서 멱등 주입).
- 신규 LOCK `alzheimers_threshold_levers`(grade `[L partial · O links]`; 동결 lock 미수정). **§37 next-nav 링크 신설**
  (§37 빈 `<span>` → §38, 생성기·렌더 양쪽). CITES=[자기, **addiction_threshold_levers**(§36 형제 부분-적합),
  **plasticity_consolidation**(§26 E0 층 — AD out-of-reach 축=E0 DECAY=중독 GAIN의 역)] = 3 vp-card. ANSWERS 57w(40–60 통과).
- registry **49 locks / 38 chapters**, gate PASS **175/175**, sitemap **39/39**, llms 4989B(**바이트-동일** <5KB).
  manifest·`_meta.json` reconcile(38행/38챕터·§38=4100w·totals.words 43784→**47884**).

---

## 2. FROZEN HASHES (이것들로 검증 — 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine file** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **M0–16 subtree** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| M9 anchor R (불변) | `0.38961455156044245` |
| §30 양극성 3-레버 지도 (불변, 아틀라스 등록) | `a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef` |
| §31 뇌전증 3-레버 지도 (불변, 아틀라스 등록) | `22879b696cf9226efc660acdea1f017a8018c3d1eb93f324f32da53dbfc14fcf` |
| §32 우울 3-레버 지도 (불변, 아틀라스 등록) | `d07aab40ba56ee5dd234d65ee8691ac80458a9c71b6355bacfccbd1efdb69f30` |
| §33 조현병 3-레버 지도 (불변, 아틀라스 등록) | `8e0137bccfe6dfe751af078a1e340accef578698992e569703865c6c27fe8c30` |
| §34 자폐 3-레버 지도 (불변, 아틀라스 등록) | `5b65a271ac182fecc744f20e2bb035043f81c9c1bc3f15608547ec00a31b77c4` |
| §35 ADHD 드라이브-톤 지도 (불변, 아틀라스 등록) | `d29a3dc8971250ff31d8bc37329a9ce3b1e067a0af81cf869950ce47b1505a35` |
| §36 중독 보상-구동 지도 (불변, 아틀라스 등록) | `f23e3c126f30e5f137db2773223212625f5e08a9fb34f97583fcad312380e2bb` |
| §37 중독 민감화 동역학 결과 (불변, 아틀라스 등록) | `20dfb3e902ffba2132617669f1e065bc6bcf399cb91e338c4cf2711142e845e3` |
| **§38 알츠하이머 3-레버 지도** (NEW, 아틀라스 등록) | `68029dab06ed152da919bdc3d0529058d06226356027e803647441a82b4067fe` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 §38의 경우 **결과 JSON**(`68029dab…`)을 동결한다. 모듈은 매
> 실행 자기 결과를 다시 쓰고 `expected_alzheimers_threshold_levers_sha256.json`과 대조하여 fail-closed PASS로
> 게이트된다(결정론 2× 검증). 엔진 트리 hash는 v1.44와 동일(불변 확인). **이전 §30–§37 지도/결과 sha 전부 불변.**

---

## 3. GATE / REGRESSION STATUS

- **`python3 tools/gate.py` → PASS 175/175, 0 hard fail.** (§38 answer-first 40–60w 통과 57w, sitemap 39/39,
  llms <5KB 4989B, engine reproduces, SSOT cards drift 0, body word counts within 2%, build idempotent.)
- **`python3 repro/mind/_verify/run_all_atlas.py` → ATLAS GATE ALL PASS 16/16, 19 CONFIRMED 0 REFUTED, engine
  파일 byte-unchanged.** (각 시민이 엔진 트리를 재-emerge → 트리 불변 확인 → 자기 결과 bit-for-bit 재현 → honesty.)
- **`python3 repro/mind/_verify/run_all_alzheimers_levers.py` → AD-T-L HARNESS ALL PASS**(map→burden→l3_honesty→
  forbidden_scan, 지도 sha `68029dab…`, 결정론 2×).

### 재현 방법 (패키지 루트에서)

```bash
# 0) 의존성
pip install numpy --break-system-packages

# 1) 신규 §38 레버 하니스 단독 (수초)
python3 repro/mind/_verify/run_all_alzheimers_levers.py

# 2) 아틀라스 전체(16모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
#    (백그라운드 setsid 실행 후 폴링 권장)
python3 repro/mind/_verify/run_all_atlas.py

# 3) 출판/검색 게이트
python3 tools/build_search_layer.py   # answer/vp-card 주입 + sitemap/llms 재생성 (멱등)
python3 tools/gate.py                  # PASS 175/175 확인
```

> registry 무결성: `python3 tools/mind_registry.py` → `registry OK: 49 locks, 38 chapters, values match frozen results`.
> 카운트 재조정(필요 시): `python3 tools/reconcile_manifest.py`(canonical HTML에서 본문 단어수 재계산, 멱등 —
> **단 totals.words는 손으로 갱신**: 현재 47884 = 38챕터 합).

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

- **구조량 ≠ 임상량.** 프로모터 `|h_sp|`는 유전자 자신의 스위치 강성이며, **신경퇴행 속도·아밀로이드 부담·타우 부하·
  수용체 점유·약효·용량·임상효과가 절대 아님**(방화벽). γ는 점수에 합산되지 않고 맥락으로만 동반된다.
- **증상 전용, 진행 안 늦춤.** 도달 가능 레버(콜린에스테라아제 억제제·메만틴 방향)는 **순간 작동점**에 작용한다 — 증상을
  완화할 수 있으나 신경퇴행을 **늦추거나 멈추거나 되돌리지 못한다**. 지도는 어떤 레버 방향도 질병-수정이라 주장하지 않는다.
  진행 축에 닿는 유일한 치료제 — **항-아밀로이드 항체(레카네맙·도나네맙)** — 는 **out-of-reach PROG 축**에 작용하며,
  문턱 레버가 아니라 **진행-수정제**이고 임상 저하율을 **소폭만** 줄인다(심각한 캐비엇 동반).
- **인간 경계(비협상).** **치매를 안고 사는 사람은 여전히 사람이다.** DIGNITY 클래스는 장식이 아니다 — 알츠하이머를
  둘러싼 비인간화 어휘(빈-껍데기·잃은-대의)를 거부한다. 알츠하이머는 기질의 퇴행이지 사람의 차감이 아니며, 여기 기술된
  메커니즘 중 어떤 것도 누군가를 빈 껍데기나 잃은 대의로 취급하는 면허가 아니다. 프로모터 읽힘·레버 배정은 메커니즘
  경계이지 치매에서 기억·상실·자기성의 **느껴진 질**에 관한 주장이 아니다(Axis-A·`consciousness_claim=0`·hard problem
  **OPEN**). `medium_efficacy_tested=0`; **not medical advice, not a diagnosis, not a treatment protocol, and not a
  cure / reversal / prevention.**

---

## 5. v1.46 ENTRY POINTS (next session)

> **세 PARTIAL [L] 사례가 모두 출판됨**: ADHD(L3-only, 첫 부분), 중독(L3-지배+L1/L2, 둘째 부분 + B-i↔B-ii 합류
> CLOSED), 알츠하이머(L3-지배+L1/L2·분할 부호, 셋째이자 가장 깊은 부분 = E0 DECAY = 중독 GAIN의 역). `THRESHOLD_
> LOGIC_INHERITANCE.md` §3 우선순위표·§3.8 적합도 요약표가 SSOT. 사용자 지시에 따라 택일.

**A (잔여) — 문턱-이동 논리를 다음 기존 사례로 확장.** 우선순위표상 ADHD·중독·알츠하이머 이후 잔여 기존 사례(로드맵
본래 **T3c OCD** 등). 세 부분-적합을 안긴 만큼, 다음 사례도 **깨끗한 [V]인지 부분 [L]인지**를 먼저 **도달성**으로 판정할
것 — 게인성/학습성/퇴행성 축이 지배적이면 부분 적합이 예상되고, 그 경우 중독처럼 **B-i(명명)+B-ii(E0 동역학 모델)**
쌍으로 닫을 수 있는지 검토.

**B (알츠하이머 B-ii — E0-진행 동역학) — §39 후보.** §38(B-i)은 알츠하이머의 지배축 **PROG 신경퇴행 진행 = E0 DECAY**
를 순간 레버로 **도달불가로 명명**했다(중독 §36 B-i와 같은 정직한 절반). 중독이 §37(B-ii)에서 SG GAIN을 §26 E0
가소성 층에 **직접 모델링**하여 합류를 닫았듯, 알츠하이머의 E0 **DECAY**(누적 손실)도 E0 층을 READ-ONLY로 재사용해
SIGN-only로 다룰 수 있는지 검토 — 단, 중독은 E0 **GAIN**(흔적 축적)이었고 알츠하이머는 E0 **DECAY**(기질 상실)라
**구조적으로 역**이므로, 손실을 어떻게 부호-접지(예: 결합 약화/소거 방향)하고 가드(η=0 복귀)할지 먼저 설계. **새 장애를
열기 전에 도달성 판정 먼저.**

**규율 리마인더 (모든 v1.46 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`); (iii) HTML
본문 English-only(C0), 이 같은 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — 현재 4989B로 **여유
거의 없음(≈11바이트)**, 신규 챕터는 sitemap만; `write_llms()`의 손-큐레이트 슬러그 목록을 건드리지 말 것 — Part-II
챕터는 애초에 거기 없음, 검증됨); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN
방화벽 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 매번 압축 파일 1개(별도 index.html 금지); (vii) 변경 후
**두 게이트(`gate.py` 175+, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성
금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: E0 동역학 모듈은 `from e0_plasticity import PlasticConnectome`
패턴(§37이 선례), 공유 유전자 γ 캐시 재사용(자폐/뇌전증/우울/조현병/ADHD/중독 캐시). **아틀라스 전체 재현은 ~6분**
(모듈마다 엔진 재-emerge) — 백그라운드 `setsid` 실행 후 폴링 권장. **새 장애 모듈 전에** 세 부분-적합 패턴(지배축
out-of-reach 명명, fold vs 게인 vs 학습 흔적 vs **퇴행/E0 DECAY**)과 §37의 **B-i↔B-ii 합류 패턴**(명명 ↔ 모델+핸들)을
먼저 읽고 **어떤 축이 도달 가능/불가**인지를 먼저 정할 것. **거버넌스 거짓 양성 주의**: 인용된 면책 문구(예: "진행을
늦추지 못함", "치유가 아님")가 자기 스캐너를 오발화할 수 있으므로, 부정-가드 클래스 설계와 인용 정밀화(§38이 선례:
`slow/disease-modifying`을 부정-가드로 이동, 항체 서술 정밀화)를 따를 것.

---

## 6. 변경 파일 목록 (v1.45 add-only)

**신규:**
- `repro/mind/_verify/alzheimers_threshold_levers.py` (+ `_results.json`,
  `expected_alzheimers_threshold_levers_sha256.json`)
- `repro/mind/_verify/alzheimers_burden_prioritisation.py` (+ `alzheimers_burden_prioritisation.json`)
- `repro/mind/_verify/alzheimers_l3_honesty.py`
- `repro/mind/_verify/alzheimers_forbidden_claim_scan.py` (+ `alzheimers_claim_scan.json`)
- `repro/mind/_verify/_build_alzheimers_levers_cache.py` (+ `alzheimers_levers_promoters.cache.json`)
- `repro/mind/_verify/run_all_alzheimers_levers.py` (4-step 집계기)
- `docs/mind/38-alzheimers-threshold-levers/index.html`
- `tools/_gen_ch38_alzheimers_levers.py`
- `HANDOVER_v1_45_to_v1_46.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 **AD-T3b-L** 16번째 시민 + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개 — `alzheimers_threshold_levers`)
- `docs/mind/37-addiction-sensitization-dynamics/index.html` (next-nav 링크만 — 빈 `<span>` → §38)
- `tools/_gen_ch37_addiction_sensitization_dynamics.py` (NEXT 링크만 — 위 next-nav 병행)
- `manifest/mind.csv` (38행), `docs/mind/_meta.json` (38챕터 + totals.words **47884**)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§3.7 알츠하이머 신설·§3.8 적합도 표 행 추가·§5 갱신),
  `CHANGELOG.md` (v1.45 엔트리), `MASTER_MANUAL_START_HERE.md` (롤링 포인터 → v1.45)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`(39 URL), `docs/llms.txt`(바이트-동일 4989B),
  `docs/llms-full.txt`, `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
