# HANDOVER — v1.58 → v1.59 (WAVE BACK-INTEGRATION: 자식 `vp_wave_computer`의 성과를 비순환적으로 위로 흘려보내기 / 제안 레이어 / mind+frontal_sim)

> 다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → `START_HERE_HANDOVER_v2.md` → 이 문서 순으로 읽으면 맥락이 복원된다. 본 문서는 한국어(세션 언어); 백서 본문(`docs/` HTML)은 C0에 따라 영어 전용이며 이 문서·`UPGRADE_DESIGN…`·`ADDENDUM_W1…`는 거버넌스/설계/애드덤 문서다.

> **v1.59의 성격 (제안·레지스트리 레이어 — 등급은 0개 이동).** 다운스트림 기능-천장 연구 `vp_wave_computer`(L0–L9 + hardening + compression, concept DOI `10.5281/zenodo.20783570`)의 성과를 **어머니(mind/neuro/frontal_sim)로 비순환적으로 역통합**하는 규율·레지스트리·게이트를 연다. **핵심 lock:** 자식은 어머니에서 B1–B5를 상속했으므로 자식의 *성공은 어머니 주장의 증거가 될 수 없다* — 금지된 고리 `A→B→"B가 A를 지지"`. 따라서 위로 흐를 수 있는 채널은 **세 개뿐**: (i) **[P]** 파생 예측(미검증, 각자 real-data 승격 게이트 보유), (ii) **[sharpen]/[tension]** 정직한 음성(기존 주장 약화/한정), (iii) **[realize]** engine-blindness witness(어머니가 맹목인 메커니즘이 *실현 가능*함을 자식이 시연 → 어머니 `[O]`를 "현상 부재"에서 "해상도 한계"로 **재유형화**, 확증·국소화는 0). **어떤 어머니 등급도 `[V]`로 안 올라간다.** `[V]` 승격은 오직 real-data(Phase B)를 통해서만.

---

## 1. WHAT v1.59 DELIVERED (additive; 동결 무변경)

### 1.1 설계 문서 (영어, root) — `UPGRADE_DESIGN_v1_58_to_v1_59_wave_backintegration.md`
- 제안서(`PROPOSAL_…`, 입력으로만 사용)를 **대체**. 제안서와의 차이는 본문에 **[Δ vs proposal]** 로 명시·논증.
- **3-채널 분류** 확립(제안서는 2개로 셌음 — [realize]이 누락). [realize]을 **가장 합당·가장 가치 있는 단일 항목**으로 식별.
- 7개 제안 항목 **triage**: Tier A(W1·P1·P2) / Tier B(S1·S2·P3) / Tier C(P5·P4) / **드롭(S3)**.
- 제안서로부터의 4개 departure: **S3 제거**(어머니가 CLS 이중해리를 *주장 안 함*; §26은 `[O]`로 열림 → 휴면 플래그 `S3°`로 강등) · **S2 격상**(tension→tension+P, PFC/해마 맥락-공급 경로 해부학적 예측 추가) · **P4 강등**(W1과 중복) · **P5 신규**(자식 axiom-compression L9++에서: θ–γ WM 용량은 L0 기초가 아니라 *창발*이라는 예측).
- **구현 제약(제안서 누락):** `[P]`는 미검증이므로 **vp-card가 될 수 없다**(card는 동결 엔진 결과에 묶임, gate.py SSOT drift 0). 모든 `[P]`/`[realize]`는 **별도 레지스트리**에만 살고 real-data 승격 전엔 챕터로 안 들어간다.

### 1.2 레지스트리 (machine-readable) — `manifest/backintegration.csv`
- 9행: **W1**(realize, frontal F1 P2 holding `[O]` 재유형화) · **P1**(θ–γ 용량=min(slots,precision)) · **P2**(PCI inverted-U, R=예측표적) · **S1**(flat γ binding depth-bounded ~2–4) · **S2**(content-gate ⊥ strict-separation; 독립 context 채널 예측) · **P3**(학습이 prediction-sufficiency에서 정지) · **P4**(lead-not-lag holder 서명) · **P5**(θ–γ 창발) · **S3°**(DORMANT, CLS 장이 쓰여질 때만 발동).
- 각 행: `channel`·`mother_target`·`target_grade_now`·`statement_sign_only`·`source_layer`·`provenance([<=W:Ln])`·`promotion_gate_real_data`·`retypes_open_question`·`localizes_claim`·`strengthens_mother_grade`·`is_vp_card`·`status`.

### 1.3 W1 애드덤 (영어) — `frontal_sim/ADDENDUM_W1_realize_temporal_holding.md`
- F1 §3(P2 holding `[O]`)에 부착. **F1 등급 무변경 — P2는 `[O — honest negative]` 유지.** 자식의 반증된 주장("피질 노드가 holder")을 *되살리지 않음*.
- 자식 `vp_wave_computer` L7 성과를 **명시적으로 인용**(forward model이 sensorimotor delay 뚫고 목표 잡음 err≈0; reactive lag≈0.96; open-loop drift≈0.77; 4 seeds, N=96, M=5, digest `17aa27bf…`) — 단 반순환 규율을 평이하게 못박음(자식은 상속받았으니 확증 불가, 국소화도 "시사적일 뿐").
- **[realize] 무브:** holding이 wave 기질에서 *실현 가능*함을 시연 → 읽기 (a)"현상 부재" 배제 → F1 `[O]`는 증명 가능하게 (b)"해상도 한계". 그리고 독자에게 **v2 경로**를 보여줌(v2는 엔진을 깨뜨림=별도 분기; 찾을 서명=lead-not-lag; F1 상속 바=duration-sweep 부호 안정성; 그 전엔 등급 불변).
- 사용자 지시 충실: "자식 성과 언급은 합당 · 이후 가능성을 독자에게 · `[O]` 유지하되 실제 가능성 시연."

### 1.4 게이트 (deterministic, root) — `verify_backintegration.py`
- `tools/gate.py`(어머니)·`frontal_gate.py`(frontal)와 **나란히** 실행; 둘 다 대체 안 함, 무거운 러너 임포트 안 함.
- 6개 검사(전부 hard): ①provenance 존재 ②모든 `[P]`에 real-data 게이트 ③(no silent promotion) provenance 행에 bare-`[V]` 없음 ④**[realize] 방향 검사**(반드시 어머니 `[O]` 가리킴·`absence→resolution_limit`·`localizes_claim=0`·`strengthens_mother_grade=0`) ⑤`[P]`/`[realize]`가 vp-card로 밀반입 안 됨 ⑥어떤 행도 어머니 등급 강화·반증된 주장 국소화 안 함.
- **이빨 증명:** 적대적 3-공격 주입(순환 [realize]·card 밀반입 [P]·게이트 없는 [P]) → 각각 check 1/4/6·5·2가 FAIL로 차단 확인. 깨끗한 레지스트리 6/6 PASS, 결정론적 2× byte-identical.

---

## 2. GATES (finalize 전 필수)
- `python3 verify_backintegration.py` → **PASS (6/6)**, 결정론적. *(이 세션에서 통과 확인)*
- `python3 repro/frontal/_gate/engine_tripwire.py` → **TRIPWIRE PASS**: 엔진 sha `e61083ae…` byte-identical · 3개 층 byte-identical · M9 앵커 `R=0.38961455156044245` bit-for-bit · frontal 적분기==엔진. *(이 세션에서 통과 확인)*
- `python3 tools/gate.py` → 변경 없음으로 통과해야 함(챕터·card·sitemap·manifest 무변경; 신규 파일은 50-챕터 매니페스트·sitemap 밖). *(엔진 재현 ~5분; 구조 검사는 동결 무변경이라 by construction 통과)*
- `python3 repro/frontal/_gate/frontal_gate.py --full-tree` → 변경 없음으로 통과해야 함(frontal repro 트리 byte-unchanged). *(~29초+)*

---

## 3. KEY FACTS / SHAs
- **동결(무변경):** 엔진 `vp_mind_engine.py` sha `e61083ae956206e9…`; emergence tree `0fbf4988…`; M9 앵커 `R=0.38961455156044245`; F1 결과 sha `21bf28f6…`. mind 50-챕터 manifest/`_meta.json`/sitemap(61 loc=61 page) 전부 byte-identical.
- **인용된 다운스트림(어머니 밖):** `vp_wave_computer` v0.12, L7 embodiment digest `17aa27bf…`, concept DOI `10.5281/zenodo.20783570`. (자식의 다른 앵커: L2b/L8/L4/L9++ 등 — `backintegration.csv`의 `source_layer` 참조.)
- **신규 산출 SHA(이 세션):** `UPGRADE_DESIGN…md` `f5391b18…` · `backintegration.csv` `f99c6bea…`(root 원본; 패키지 내 manifest/ 사본은 동일 내용) · `verify_backintegration.py`(경로 1줄만 manifest/로 조정).

---

## 4. 불변 (firewall, 무변경)
`efficacy=0` · `consciousness_claim=0` · `hard_problem_open=1` · `new_tuned_constants=0` · 의료 조언 아님 · one-way 의존성 유지(mind→neuro, frontal_sim은 자식에 의존 안 함; 자식은 위로 realizability witness + 미검증 예측으로만 기여, `verify_backintegration.py`가 감사). **어떤 등급도 `[V]`로 안 올라감.**

---

## 5. 다음 작업 후보 (우선순위)
1. **W1 HTML 정본화 (v1.59→v1.60 render pass).** 이번 세션은 게이트 안전(sitemap 61=61 불변)을 위해 markdown-only. v1.58이 frontal 서사를 `docs/mind/frontal/`로 렌더한 것과 동일하게, W1 애드덤을 `docs/mind/frontal/10-w1-realize-holding/index.html`로 렌더(answer-first/JSON-LD/vp-card-없음/prev-next) + sitemap +1 + frontal hub TOC 링크. **주의:** HTML 추가 시 `gate.py`의 sitemap 불변(loc==page)을 반드시 같이 갱신.
2. **Phase B (real-data, `[V]`로 가는 유일한 길) 시작.** P1→공개 MEG/EEG WM 코퍼스(induced gamma-jitter); P2→TMS-EEG PCI vs synchrony(의식 gradient); P3→learning/RPE 데이터; S1→center-embedding 코퍼스. sign-only 사전등록을 구체 데이터셋에 매핑.
3. **Phase C (sharpen, 외부 데이터 불필요).** S1·S2를 어머니 동결 엔진에서 내부 일관성 검사로 실행(엔진이 depth-bound/trade-off를 같이 보이는가; 못 보이면 `[O]` 기록 후 v2로 연기 — W1/F1과 같은 Hard Limit 1 경계).
4. **F2/v2 입력 반영.** W1의 v2-기질 입력(lead-not-lag 서명 + duration-sweep 바)을 frontal F2(stereotypy=T×W×E0)·v2 설계 노트에 명시.

*v1.59는 확증을 0개 추가하고, 예측·정직한-음성·하나의 열린-질문 재유형화를 추가한다. hard problem은 명시적 빈칸으로 남는다(`consciousness_claim=0`, `hard_problem_open=1`). 의료 조언 아님.*
