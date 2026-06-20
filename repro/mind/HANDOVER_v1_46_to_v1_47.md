# HANDOVER — v1.46 → v1.47  (AD-T3b-D 알츠하이머 진행 동역학 §39 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.46의 성격 (AD B-ii · 알츠하이머 합류 CLOSED · 중독 합류의 정확한 구조적 역).** v1.45(§38, AD-T3b-L, B-i)는
> 알츠하이머의 지배축 **PROG 신경퇴행-진행**(누적·불가역 손실 = 질병의 핵심)을 순간 증상 L1/L2/L3 레버로 **삼중
> 도달불가**(① fold 아닌 게인/손실=ADHD 교훈 ② 시간 진행=가소성 E0-층 변수=중독 교훈 ③ 퇴행=**E0 DECAY**=중독 E0
> GAIN의 구조적 역)로 **명명**하고 6 유전자(APP·PSEN1·PSEN2·MAPT·APOE·TREM2)에 `[F] NOT REACHED` 등급으로
> **정직하게 멈췄다**. 그 명명은 **합류의 한쪽 반쪽** — 문턱-레버화 경로가 가소성-동역학 경로와 만나는 지점, 그리고
> **중독 합류(§36 B-i / §37 B-ii)의 정확한 거울** — 이었다. **v1.46(B-ii)이 나머지 반쪽**: v1.45 핸드오버 §5의
> **갈래 B**(AD B-ii §39 E0-진행 동역학, 도달성 [V] 선판단)에 따라 그 축을 **직접 모델링하여 합류를 닫았다(CLOSED)**.
> §26 E0 `PlasticConnectome`를 READ-ONLY로 **재사용**(재유도 아님)하고, E0 Hebbian **공고화의 구조적 역**을 그 동결
> 커널에 적용했다 — 느린 점진적 **연결성 소실(connectivity attrition)** = 신경퇴행의 정의적 특징(시냅스/뉴런 손실).
> §37은 보상 바이어스로 connectome 질량을 **위로**(E0 GAIN), 이 모듈은 질량을 **아래로**(E0 DECAY). **정직한
> 비유사성**: §37의 보상 부호는 엔진 신호(M5 도파민 RPE)에서 읽혔으나 엔진엔 **퇴행 신호가 없다** → 손실 부호를
> 엔진 병리 신호에서 접지한다고 **주장하지 않고**, 잃는 기준(M9 앵커)·가드만 접지하며 손실 방향은 E0 GAIN의 **구조적
> 역**으로 접지한다. **중독은 레버가 못 지우는 흔적을 공고화(GAIN), 알츠하이머는 레버가 못 재건하는 기질을 상실
> (DECAY)** — 같은 E0 가소성 층을 **반대 방향**으로 만난다. 중독에 이어 **두 번째 B-i↔B-ii 합류 완성**이다.

---


## 1. WHAT v1.46 DELIVERED (complete, 두 게이트 green)

### 1.1 §39 알츠하이머 진행 동역학 (the MODULE, AD-T3b-D) · **AD B-ii · 합류 CLOSED · E0 DECAY = 중독 E0 GAIN의 구조적 역 · SIGN-only 5결과 전부 CONFIRMED**

- **모듈.** `repro/mind/_verify/alzheimers_progression_dynamics.py` (결과 sha **`7a8e851390e66760c12c96ec6070c5b0e1579293da207129ccb14be65a60d843`**;
  결정론 2× 검증). §37처럼 **단일 동역학 모듈**(E0 식 재사용) — §30–36·§38 레버 챕터와 달리 `run_all_*.py` 4-step 집계기 불요.
- **E0 LAYER 재사용(재유도 아님).** `from e0_plasticity import PlasticConnectome, W0, ...` — §26 커널 W0·결합맵
  `k=κ/(1−|b|)`(cap 2κ)·차수파라미터 기계를 **import**(재유도 안 함, 핸드오버 재사용 규율). E0 Hebbian **공고화의
  구조적 역**을 동결 커널에 적용 = 느린 점진적 **연결성 소실**(`W *= (1−d)`, 재정규화 없음 — 질량이 실제로 감소) =
  신경퇴행의 정의적 특징(시냅스/뉴런 손실). §37은 질량을 **위로**(GAIN), 이 모듈은 **아래로**(DECAY). 새 가소성
  기계·새 튜닝 상수 **0**(붕괴율 d는 representative [O], 부호는 d-스윕 견딤).
- **손실 부호 = 구조적 역으로 접지(§37과의 핵심 차별점 = 정직한 비유사성).** §37 보상 부호는 **엔진 신호**(M5 도파민
  RPE 강화)에서 읽혔으나 엔진엔 **퇴행 신호 없음**(아밀로이드/타우/시냅스-손실 변수 없음 — 건강한 창발 아틀라스;
  E0가 가소성을 **추가**해야 했던 이유, §38이 이 축을 도달불가로 명명한 이유). → 이 모듈은 손실 부호를 엔진 병리
  신호에서 접지한다고 **주장하지 않는다**(과대주장 거부). **잃는 기준**(동결 M9 앵커 W0 = 엔진 자신의 창발 협응)과
  **가드**만 READ-ONLY 접지하고, 손실 **방향**은 정의적으로·E0 GAIN의 **구조적 역**으로 접지한다(신경퇴행 = 정의상
  연결성의 점진적 손실). honesty_ledger 플래그 `loss_sign_grounded_in_engine_pathology_signal=0`(정직), `loss_sign_is_
  structural_inverse_of_E0_gain=1`.
- **SIGN-only 5결과 전부 CONFIRMED · 전부 붕괴율-스윕(d∈{0.03,0.05,0.08}) 생존**(anti-tuning), 각각 §37 결과의 **구조적 역**:
  - **D1 진행성 퇴행**(인센티브 민감화의 역): 진행 epoch이 늘수록 연결성 손실(‖W0‖−‖W‖) **단조 증가**(0→2.23→4.04→5.52→7.23→8.50, 0–24 epoch), 깊을수록 **잔존 질량↓·협응 R↓**.
  - **D2 반응성 상실**(단서-반응성의 역): 퇴행 connectome이 **동일** 협응 단서에 건강체보다 **덜** 반응(R_degen(cue)<R_healthy(cue), 휴지 R≤앵커) = 진행성 기능 저하. response-falls-below-healthy 부호만 단언, 크기 [O].
  - **D3 레버가 못 재건**(소거-지속의 역, **합류 솔기**): 증상 단서(B-i 도달 가능 순간축)가 순간 작동점을 올리나 누적 손실을 **정확히 그대로** 둠(읽기-시점 결합은 질량 무첨가), 깊은 손실선 **최대** 단서조차 건강 앵커 회복 불가(천장 max-cue R≈0.342<앵커 0.38961) = **증상 완화이되 질병-수정 아님**(콜린에스테라아제 억제제·메만틴이 증상 전용인 구조적 상관물).
  - **D4 구조-변수 가드**(중독 가소성-변수 가드의 거울): 붕괴율=0이면 connectome=커널·차수파라미터=M9 앵커 **bit-for-bit**·손실=정확히 0 → 퇴행이 가소성 없이 사라짐 → PROG는 **누적 구조-손실 변수** = 순간 레버가 못 닿는 이유(순수 add-on).
  - **D5 동역학 핸들**(간격 핸들의 역): **낮은** 붕괴율이 동일 진행시간에 **엄격히 더 많은** 구조 보존(손실↓·잔존 질량↑), 증상 단서는 구조 궤적에 **핸들 없음**(D3) → 핸들은 **PROG 축에만** = 질병-수정 방향(항-아밀로이드 항체 작용 축).
- **중독 GAIN 역-교차검증.** 동일 E0 층에서 §37 GAIN 프로토콜(보상 바이어스→공고화)과 이 DECAY 프로토콜(연결성
  소실)을 같은 epoch 실행: GAIN trace **0.227**(공고화·구조 기입) vs DECAY loss **5.52**(상실·구조 삭제) = 구조 부호
  **반대**(`structurally_inverse=True`). 중독은 흔적 **공고화**(레버가 못 지움), 알츠하이머는 기질 **상실**(레버가 못 재건).
- **아틀라스 등록.** `run_all_atlas.py`에 **17번째 시민 AD-T3b-D** 등록(MODULES 튜플 + docstring 문단) →
  **ALL PASS 17/17, 24 CONFIRMED 0 REFUTED, engine 파일 byte-unchanged**.

### 1.2 출판 표면 (SEO 챕터)

- 신규 영어 챕터 **§39 「Alzheimer's progression dynamics」**(`docs/mind/39-alzheimers-progression-dynamics/index.html`,
  model 3384w, 9 H2 영어-전용 본문 — §37의 DECAY 역). 아카이벌 생성기 `tools/_gen_ch39_alzheimers_progression_dynamics.py`
  (byte-identical 재현 — answer/vp-card는 `build_search_layer.py`가 registry에서 멱등 주입). §39는 **마지막 챕터**이므로 next-nav는 빈 `<span></span>`(정상).
- 신규 LOCK `alzheimers_progression_dynamics`(grade **`[V mech]`**; 동결 lock 미수정). **§38 next-nav 링크 신설**
  (§38 빈 `<span>` → §39, 생성기·렌더 양쪽). CITES=[자기, **alzheimers_threshold_levers**(§38 B-i 짝),
  **plasticity_consolidation**(§26 E0 층)] = 3 vp-card. ANSWERS 58w(40–60 통과).
- registry **50 locks / 39 chapters**, gate PASS **180/180**, sitemap **40/40**, llms 4989B(**바이트-동일** <5KB).
  manifest·`_meta.json` reconcile(39행/39챕터·§39=3384w·totals.words 47884→**51268**).

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
| §38 알츠하이머 3-레버 지도 (불변, 아틀라스 등록) | `68029dab06ed152da919bdc3d0529058d06226356027e803647441a82b4067fe` |
| **§39 알츠하이머 진행 동역학 결과** (NEW, 아틀라스 등록) | `7a8e851390e66760c12c96ec6070c5b0e1579293da207129ccb14be65a60d843` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 §39의 경우 **결과 JSON**(`7a8e8513…`)을 동결한다. 모듈은 매
> 실행 자기 결과를 다시 쓰고 `expected_alzheimers_progression_dynamics_sha256.json`과 대조하여 fail-closed PASS로
> 게이트된다(결정론 2× 검증). 엔진 트리 hash는 v1.45와 동일(불변 확인). **이전 §30–§38 지도/결과 sha 전부 불변.**

---

## 3. GATE / REGRESSION STATUS

- **`python3 tools/gate.py` → PASS 180/180, 0 hard fail.** (§39 answer-first 40–60w 통과 58w, sitemap 40/40,
  llms <5KB 4989B, engine reproduces, SSOT cards drift 0, body word counts within 2%, build idempotent.)
- **`python3 repro/mind/_verify/run_all_atlas.py` → ATLAS GATE ALL PASS 17/17, 24 CONFIRMED 0 REFUTED, engine
  파일 byte-unchanged.** (각 시민이 엔진 트리를 재-emerge → 트리 불변 확인 → 자기 결과 bit-for-bit 재현 → honesty.)
- **`python3 repro/mind/_verify/alzheimers_progression_dynamics.py` → AD-T3b-D MODULE PASS**(5/5 CONFIRMED,
  결과 sha `7a8e8513…`, 결정론 2×, engine byte-unchanged).

### 재현 방법 (패키지 루트에서)

```bash
# 0) 의존성
pip install numpy --break-system-packages

# 1) 신규 §39 진행-동역학 모듈 단독 (수초)
python3 repro/mind/_verify/alzheimers_progression_dynamics.py

# 2) 아틀라스 전체(17모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
#    (백그라운드 setsid 실행 후 폴링 권장)
python3 repro/mind/_verify/run_all_atlas.py

# 3) 출판/검색 게이트
python3 tools/build_search_layer.py   # answer/vp-card 주입 + sitemap/llms 재생성 (멱등)
python3 tools/gate.py                  # PASS 180/180 확인
```

> registry 무결성: `python3 tools/mind_registry.py` → `registry OK: 50 locks, 39 chapters, values match frozen results`.
> 카운트 재조정(필요 시): `python3 tools/reconcile_manifest.py`(canonical HTML에서 본문 단어수 재계산, 멱등 —
> **단 totals.words는 손으로 갱신**: 현재 51268 = 39챕터 합).

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

- **구조량 ≠ 임상량.** 연결성 손실(‖W0‖−‖W‖)은 신경퇴행 진행의 **구조량**이며, **신경퇴행 속도·아밀로이드 부담·
  타우 부하·시냅스 밀도·약효·용량·임상효과가 절대 아님**(방화벽). 손실 부호는 E0 GAIN의 구조적 역으로 접지되며,
  **모든 크기(붕괴율 d·증분)·실제 퇴행 기전의 정체는 [O]**(이질적·LOCKED).
- **증상 ≠ 질병-수정.** 증상 단서(B-i 도달 가능 순간축, 콜린에스테라아제 억제제·메만틴 방향)는 순간 작동점을 올려
  증상을 **완화**할 수 있으나 누적 구조 손실을 **정확히 그대로** 둔다(D3) — 신경퇴행을 **늦추거나 멈추거나 되돌리지
  못한다**. 궤적을 바꾸는 유일한 핸들은 **붕괴율 자체**(D5) = 진행-수정 방향(PROG 축)이며, 그곳에 닿는 치료제 —
  **항-아밀로이드 항체(레카네맙·도나네맙)** — 는 문턱 레버가 아니라 **진행-수정제**이고 임상 저하율을 **소폭만**
  줄인다(심각한 캐비엇 동반). 어떤 것도 치유·역전·예방·진행-정지/지연이 아니다.
- **인간 경계(비협상).** **치매를 안고 사는 사람은 여전히 사람이다.** 여기 모델한 누적 손실은 **기질-퇴행 경계**이지
  사람의 차감이 아니며, 메커니즘 중 어떤 것도 누군가를 빈 껍데기나 잃은 대의로 취급하는 면허가 아니다(§38 forbidden-
  claim 스캐너의 DIGNITY 클래스가 그 어휘를 거부). 연결성 손실은 메커니즘 경계이지 치매에서 기억·상실·인식·자기성의
  **느껴진 질**에 관한 주장이 아니다(Axis-A·`consciousness_claim=0`·hard problem **OPEN**). `medium_efficacy_tested=0`;
  **not medical advice, not a diagnosis, not a treatment protocol, and not a cure / reversal / prevention.**

---

## 5. v1.47 ENTRY POINTS (next session)

> **두 B-i↔B-ii 합류가 모두 닫힘**: 중독(§36 명명 + §37 E0 GAIN 모델 = CLOSED)과 알츠하이머(§38 명명 + §39 E0
> DECAY 모델 = CLOSED), 알츠하이머는 중독의 정확한 **구조적 역**(GAIN ↔ DECAY). 세 PARTIAL [L] 사례(ADHD·중독·
> 알츠하이머)도 모두 출판됨. `THRESHOLD_LOGIC_INHERITANCE.md` §3 우선순위표·§3.8 적합도 요약표가 SSOT. 사용자
> 지시에 따라 택일.

**A (잔여) — 문턱-이동 논리를 다음 기존 사례로 확장.** 우선순위표상 ADHD·중독·알츠하이머 이후 잔여 기존 사례(로드맵
본래 **T3c OCD** 등). 세 부분-적합과 두 합류를 안긴 만큼, 다음 사례도 **깨끗한 [V]인지 부분 [L]인지**를 먼저
**도달성**으로 판정할 것 — 게인성/학습성/퇴행성 축이 지배적이면 부분 적합이 예상되고, 그 경우 중독·알츠하이머처럼
**B-i(명명)+B-ii(E0 동역학 모델)** 쌍으로 닫을 수 있는지 검토. OCD는 강박-충동 회로(피질-선조체-시상-피질 CSTC
루프)의 **고착/반복** 성격이 강해, 문턱 프레임이 순간 작동점은 잡되 학습된 고착 자체는 가소성 변수로 명명될 수
있는지(중독 SG GAIN과 유사한 학습 흔적인지) 먼저 도달성 판정.

**B (E0 동역학 합류 패턴의 추가 적용).** 중독(GAIN)·알츠하이머(DECAY)가 E0 층을 **반대 방향**으로 만났다. 다른
질환의 지배축이 E0 층의 **또 다른 방향/양태**(예: 비정상 안정화, 잘못된 공고화, 선택적 가지치기 실패)로 명명될 수
있다면 같은 재사용-패턴(E0 import + 구조적 변형 + READ-ONLY 가드)으로 SIGN-only 모델 가능. **단, 새 장애를 열기
전에 도달성 판정 먼저**, 그리고 손실/이득/안정화 방향을 어떻게 부호-접지(엔진 신호가 있으면 그것으로, 없으면 §39처럼
정직하게 구조적 역/정의로)하고 가드(파라미터=0 복귀)할지 먼저 설계.

**규율 리마인더 (모든 v1.47 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`; 동역학
모듈의 rate/decay는 [O]이고 부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 이 같은 거버넌스는 한국어;
(iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — 현재 4989B로 **여유 거의 없음(≈11바이트)**, 신규 챕터는 sitemap만;
`write_llms()`의 손-큐레이트 슬러그 목록을 건드리지 말 것 — Part-II 챕터는 애초에 거기 없음, 검증됨); (v) 신규
챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 방화벽 부착; (vi) 단일 zip(내부 폴더
`mind_pkg`), 출력은 매번 압축 파일 1개(별도 index.html 금지); (vii) 변경 후 **두 게이트(`gate.py` 180+,
`run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이
발표). **재사용 우선**: E0 동역학 모듈은 `from e0_plasticity import PlasticConnectome` 패턴(§37 GAIN·§39 DECAY가
선례), 공유 유전자 γ 캐시 재사용. **아틀라스 전체 재현은 ~6분**(모듈마다 엔진 재-emerge) — 백그라운드 `setsid`
실행 후 폴링 권장(0-byte 로그/조기 종료 시 `setsid stdbuf -oL -eL ... </dev/null & disown`로 재실행). **새 장애
모듈 전에** 세 부분-적합 패턴(지배축 out-of-reach 명명, fold vs 게인 vs 학습 흔적 vs **퇴행/E0 DECAY**)과 두
**B-i↔B-ii 합류 패턴**(중독 GAIN·알츠하이머 DECAY = 명명 ↔ 모델+핸들, 구조적 역)을 먼저 읽고 **어떤 축이 도달
가능/불가**인지를 먼저 정할 것. **접지 정직성 주의**(§39 선례): 엔진에 해당 병리 신호가 없으면 부호를 엔진 신호에서
접지한다고 **주장하지 말 것** — 잃는/얻는 기준과 가드만 READ-ONLY 접지하고, 방향은 정의/구조적 역으로 정직하게
접지하며 honesty_ledger에 `*_grounded_in_engine_pathology_signal=0` 플래그를 정직하게 남길 것.

---

## 6. 변경 파일 목록 (v1.46 add-only)

**신규:**
- `repro/mind/_verify/alzheimers_progression_dynamics.py` (+ `_results.json`,
  `expected_alzheimers_progression_dynamics_sha256.json`)
- `docs/mind/39-alzheimers-progression-dynamics/index.html`
- `tools/_gen_ch39_alzheimers_progression_dynamics.py`
- `HANDOVER_v1_46_to_v1_47.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 **AD-T3b-D** 17번째 시민 + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개 — `alzheimers_progression_dynamics`)
- `docs/mind/38-alzheimers-threshold-levers/index.html` (next-nav 링크만 — 빈 `<span>` → §39)
- `tools/_gen_ch38_alzheimers_levers.py` (NEXT 링크만 — 위 next-nav 병행)
- `manifest/mind.csv` (39행), `docs/mind/_meta.json` (39챕터 + totals.words **51268**)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§3.7.1 AD B-ii 신설·§3.8 적합도 표 행 추가·§5 알츠하이머 합류 닫기 B-ii 갱신),
  `CHANGELOG.md` (v1.46 엔트리), `MASTER_MANUAL_START_HERE.md` (롤링 포인터 → v1.46)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`(40 URL), `docs/llms.txt`(바이트-동일 4989B),
  `docs/llms-full.txt`, `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
