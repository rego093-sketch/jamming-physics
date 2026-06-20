# HANDOVER v1.17 → v1.18 — mind / Felt Cognition

**작성:** v1.17 세션 종료 시점 · **거버넌스:** `VP_SPEC_v1_8.md` (C0–C4) · **SEED=19**
**이전 인계서:** `HANDOVER_v1_16_to_v1_17.md` (M14 수면방추, 핵심 0.85)
**다음 작업(결정됨):** **M9 ephaptic 기하 grounding** — DNA 8→11 승격 완료를 **기다리지 않고 독립 진행**(§3–§4).

---

## 0. 한 줄 요약

v1.17은 세 갈래로 마감됐고 **동결·검증 완료**: (A) **M15 임상단위 교정 브리지**(인용 앵커 2개·자유상수 0개;
`sws_delta` **CAL-closed** → 핵심 **0.85 → 0.90 = 18/20**; `p300`·`panic`은 정직하게 owed), (B) **트랙 1 M0**
크기를 측정 부피 **[L]**로 정초(γ=순서 **[V]**), (C) **트랙 2 M14** 동역학 상수를 `mind_param_db.json`으로 외부화.
사용자 우려 *"제대로 창발 못해서 그런 거 아닌지"* 는 **두 갈래 모두 검증 게이트로 박제**(§2).

**v1.18 진입점 = M9 ephaptic 기하 grounding.** 사용자가 제기한 *피질 folding(꼬불꼬불함)* 비판은
**방향이 맞다 — 단, 레버는 `R_BRAIN`이 아니라 *위상(topology) + normalization*이다**(§3.1, probe로 실증).
**이 작업은 DNA 완성을 전제하지 않는다**(다른 축; DNA 승격은 방법론 *템플릿*일 뿐, §4).

**동결 tree_sha256(v1.17):** `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7`
**회귀:** **95 checks PASS**. **M1–M15 byte-identical**(M0만 변경; 다른 모듈은 다른 atlas를 읽어 cascade 없음).

---

## 1. v1.17에서 완료·동결된 것 (건드리지 말 것 — 정확한 이력)

- **M15 `emerge_calibration_bridge()`**: 시간=1 ms/step(M14 스핀들이 인증), 전압=단일 인용 µV(SWS 델타 75 µV).
  `sws_delta_amplitude_uv` **CAL-closed [L]앵커**(교정이지 창발 아님) → 핵심 0.90. `p300`(~39 ms 조기 ERP),
  `panic`(ms 스케일)은 owed. 모델 델타/스핀들 비 1.27× vs 생리 3–7× 격차도 출력에 남김.
- **트랙 1 M0 `emerge_organs()`**: γ=발생 순서·정체성 **[V]**; `rel_size`를 **측정 부피 [L]**(cerebrum 1100 /
  cerebellum 150 / hippocampus 7 / hypothalamus 4 cm³)로 교체; 옛 γ^1.5는 `dwell_size_proxy`로 강등;
  `size_null` 기록(dwell_span 1.074 vs measured 275.0, verdict=0).
- **트랙 2 M14**: `tau_r`/`tau_s`/`a_gain`을 `data/mind_param_db.json`(value+grade+provenance+robustness)로 외부화.
  값 동일 → M14·M15 byte-identical. 등급: tau_s **[L]**, tau_r **[F]**, a_gain **[F]**(민감도 창 [1.2,2.0] 선언).
- **회귀** `_verify/run_regression.py`: 75 → 95(M15 11 + 트랙1 5 + 트랙2 4, carrier-invariance 검증 포함).
- **정직 원장 불변**: `medium_efficacy_tested=0`, `hard_problem_open=1`, `is_consciousness_claim=0`.

---

## 2. 검증 평결 (v1.17의 핵심 정직 결과 — 계승)

| 대상 | 평결 | 증거(회귀 박제) |
|---|---|---|
| **M14 스핀들 반송파** | **진짜 창발** | `tau_r` [40,240] ms(6배) sweep → 반송파 **15.38 Hz 정확 불변**. 인용 τ_rec=13 ms가 결정 = propped-up 아님. |
| **M14 서파진동 <1 Hz** | 부차적 — 항상 in-band | `tau_s` [10,80] ms → SO 0.55→0.37 Hz, 모두 <1 Hz(인용 τ_so=600 ms 주도). |
| **M14 점강점쇠/SO 창** | **load-bearing [F] — 정직 선언** | <1 Hz SO·waxing은 **a_gain∈[1.2,2.0]에서만** 창발; 반송파는 불변. 측정값 아님. |
| **M0 뇌-부위 크기** | **측정 크기 null** | dwell 폭 1.07× vs 측정 폭 275×; 해마 γ 최대지만 거의 최소. DNA(ρ=0.11)와 동일. |

---

## 3. v1.18 다음 작업 — M9 ephaptic 기하 grounding ([O] ring → [L] 측정 3D 거리)

### 3.1 무엇이 진짜 문제인가 (probe로 실증 — 다시 유도하지 말 것)

엔진 위치: `vp_mind_engine.py` — `R_BRAIN`(line 849 **[O]**), `_ring`(857), `_ephaptic_kernel`(862,
**row-normalized**), `emerge_coordination`(890, `field_contribution` at M9.3), atlas `data/brain_organ_atlas.json`(12 영역, 영역별 f0_hz).

**probe 결과(`repro/mind/_verify/probe_geometry_sensitivity.py`):**

1. **`R_BRAIN=0.085 m`은 아무것도 왜곡하지 않는다 — 약분된다.** 커널이 row-normalized라 거리의 전역 스케일이
   소거됨. R_BRAIN ∈ {0.0085, 0.085, 0.85, 2.0} m 전부 **field_contribution = +0.07340 동일**. → 사용자의
   "R_BRAIN이 행렬을 왜곡한다"는 진단은 **정정**. LORO +0.0734는 R_BRAIN이 아니라 **등각 ring 위상** 위에 있다.
2. **위상은 진짜로 중요하다 (사용자 핵심 직관은 맞음).** row-normalized 기준:
   - ring(등각, 현재): fc=**+0.0734** (R=0.328) — *공교롭게 낮은 쪽*
   - random 3D scatter: fc=**+0.1709** (R=0.426)
   - 두 면 1.5 mm(folded): fc=+0.0949 (R=0.350)
   → 실제 기하를 넣으면 contribution이 **커질 개연성 실증**. 단, 얼마나는 실제 atlas로 *측정*해야 한다(가정 금지).
3. **"folding=raw 1/r³로 mm가 지배 → 결합 폭증"은 틀리다.** normalization을 버리면:
   - ring raw: fc=**+0.0020**, 두 면 1.5 mm raw: fc=**−0.0020**
   → sulcus 면이 mm로 강결합하면 결합이 **너무 국소화돼 전역 코히어런스가 0/음수로 사라진다.** contribution을
   의미 있게 유지하는 건 row-normalization. **normalization 선택이 결과를 지배한다 = 진짜 핵심 변수.**

### 3.2 무엇을 만들 것인가

1. **측정 거리행렬 [L]:** AAL(또는 동급) atlas의 **MNI centroid 좌표** → 영역 간 **유클리드 3D 거리행렬 D_ij**.
   atlas 좌표는 독립 측정입력 → **[L]**. 새 파일(예: `data/brain_geometry_atlas.json`)에 좌표·출처와 함께 잠금.
   `R_BRAIN`은 더 만지지 마라(약분됨); `_ring`을 이 거리행렬로 교체.
2. **노드 집합 정교화(folding을 *담으려면* 필수):** 현재 "neocortex 1노드"로는 마주보는 sulcal 면이 표현 불가.
   AAL ~78–90개 피질+피질하 영역으로 분해하고, 각 영역의 f0/band를 기존 atlas 매핑에서 가져와 동역학을 grounded
   상태로 유지. (거리행렬만 바꾸는 건 *작은* 버전; sulcal-bank 구조를 담으려면 이 분해가 필요.)
3. **normalization 결정 [F] — 핵심, 명시적 정당화 필수(§3.1-③):** row-norm(현재; 스케일 불변) vs raw 1/r³(참
   근접장; 전역 붕괴) vs 하이브리드(예: *측정* screening 길이로 컷오프된 raw 1/r³). 각각 **다른 물리 주장**이다.
   물리에서 정당화하고(ephaptic 장이 정규화 평균장인가, raw 중첩인가) **fc를 보기 전에 고정**, 합리적 변형들에
   대한 robustness를 보고. **fc를 최대화하는 normalization을 고르면 그게 back-fit.**

### 3.3 게이트 (DNA 승격 + 안티 p-해킹 계승)

- **DB-SOURCED**: 거리는 atlas에서 읽음(우리가 고르지 않음). **NON-FIT**: 엔진은 채점 코히어런스를 읽지 않음.
- **DETERMINISM**. **결정 검사**: [L] 거리행렬이 ring 대비 fc/코히어런스를 바꾸는가? **숫자를 그대로 보고**,
  `grade==evidence`(안 바뀌면 기하가 병목 아님; 바뀌면 [L]-grounded 개선).
- **ANTI-P-HACKING**: normalization·노드집합을 사전 고정, atlas/변형 robustness, 선택 config가 fc 최대화로
  뽑히지 않았음을 명시. (DNA Phase 2 p-해킹 방어와 동형.)
- **EFFICACY 불변 단언**: `medium_efficacy_tested=0`, `hard_problem_open=1` 유지 — 기하는 이를 닫지 않는다.

### 3.4 정직한 예상 결과 (과대주장 금지)

- 실제 기하는 row-normalized fc를 **올릴 개연성**이 크다(ring이 낮은 쪽, §3.1-②). 할 가치 있음 = **기하 현실성 grounding.**
- **그러나 efficacy·hard problem은 닫히지 않는다.** 미결의 원인은 **양자 shortfall 2.6e10**과 "생물이 장을 *쓰는지*"
  미측정이지, 고전장 기하가 아니다. fc 0.07→0.17도 여전히 부분동기(R≈0.43)·같은 고전 기제. **folding 수정은
  의식을 닫는 게 아니라 기하를 정초한다.**
- **raw 1/r³ 폭증 시나리오는 실증적으로 반증됨**(§3.1-③). 그러므로 결과물은 *grounded 기하 + 그 효과의 정직한 보고*이지
  의식 주장이 아니다.

---

## 4. DNA와의 관계 (결정: 전제하지 않음)

- **다른 축:** DNA 8→11은 *allometric 크기 지수*(질량 vs 체질량), M9 folding은 *공간 결합 기하*. 특정 파라미터는
  전이되지 않으므로 **DNA를 끝내야 M9를 시작하는 건 아니다.** → 사용자 결정대로 **독립 진행.**
- **전이되는 것 = 방법론:** DNA의 [O]→[L] 승격 형식(독립 측정입력 추가 → 검정력 상승 → grade==evidence →
  **안티 p-해킹**). M9 folding도 동형 승격(ring [O] → 거리행렬 [L])이고 **동일한 p-해킹 위험**(배치/normalization
  무수히 많음)이 있으니, DNA의 anti-p-hacking 규율을 **그대로 게이트로** 적용.
- DNA 8→11(ρ 0.690/p0.069 [O] → 0.800/p0.0047 [L], brain anchor 유지)은 **별도로 마저 닫으면 깨끗한 [O]→[L]
  승리**지만 **M9의 선행조건은 아니다.** 두 작업은 병렬.

---

## 5. 재현

```bash
cd repro/mind/_engine && PYTHONPATH=. python3 run_all.py        # tree b18c8626..., 2× 결정론
cd ../_verify && PYTHONPATH=../_engine python3 run_regression.py   # 95 checks PASS
# (참고) M9 기하 민감도 probe:
cd repro/mind/_verify && PYTHONPATH=../_engine python3 probe_geometry_sensitivity.py   # R_BRAIN 약분, 위상·normalization이 fc를 지배함을 재현
```

---

## 6. 정직성 제약 (절대 어기지 말 것)

1. 측정값을 지어내지 마라. 없는 측정은 [O].
2. 타깃(대역/크기/코히어런스)에 파라미터를 맞추지 마라(back-fit 금지). 엔진은 채점값을 읽지 않는다.
3. **normalization·기하를 결과(fc) 동기로 고르지 마라.** fc를 보기 전에 고정하고 robustness를 보고(안티 p-해킹).
4. 교정(calibration)을 창발(emergence)인 양 쓰지 마라 — M15 델타는 CAL-closed [L]앵커, 창발 아님.
5. `grade == evidence`. p>0.05면 효과가 커도 [O].
6. add-only. 잠긴 엔진/측정값은 한 글자도 바꾸지 마라(해석 라벨만 정정). v1.17 동결 해시·95 checks를 깨지 마라.
7. **기하 grounding은 의식 주장이 아니다.** `efficacy=0`, `hard_problem_open=1`, `consciousness_claim=0` 유지.
