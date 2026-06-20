# 재현불가 원장 (IRREPRODUCIBILITY LEDGER) — VP physics

VP-SPEC v1.7 **헌법 C3**(재현 불가 시 사유 명시 — 서술의 원칙)의 집계 문서. 패키지 내부의
결정론 재생성으로 **재현할 수 없는 정량**을 한 곳에 모은다. 각 항목은 ① `[O]` 등급, ② 재현 불가의
구체적 사유(장애물), ③ 정본 HTML 내 위치, ④ 재현되는 것/안 되는 것의 경계를 명시한다.
사유 없는 `[O]` 는 헌법 게이트 FAIL 이다. 본 원장의 모든 항목은 정본 HTML 본문과 교차 확인된다.

> 재현성 등급(이 백서 어휘): `[F]` forced(강제·유도) · `[V]` verified(검증) · `[H]` hypothesis(가설)
> · `[O]` open(미해결·외부/측정 입력). 본 원장은 `[O]` 중 **정량이 재현 불가한 항목**만 다룬다.

---

## 1. 절대 중력 크기 (absolute gravity magnitude, g ≈ 9.8 m s⁻²)

- **등급:** `[O]` (구조 [F] + 절대 척도 [O])
- **위치(정본 HTML):** §17.4 "Gravity: cap mechanism and the four-wall theorem"
  (`docs/physics/17-extensions-optional-reading/`), 기하 유도 시도는 부록
  `docs/physics/axg-geometric-derivation-gravity-lattice-yield/`.
- **재현 불가 사유(장애물 — four-wall 정리):** 잠금격자 primitives 만으로 중력의 **절대 척도**를
  고정하려 하면 네 개의 "벽"(four walls)에 막힌다. 이는 백서가 **증명한 no-go**("the no-go proven,
  not confessed")이다. 즉 절대 크기는 패키지 내부의 결정론 계산으로 산출할 수 없고, 전(全)물리 잠금
  계산은 HPC급 계산 게이트에 막혀 재생성 불가하다. 따라서 절대 척도는 **정직하게 외부(측정) 입력**으로
  둔다(`absolute honestly external`). 단일 스칼라 `m_q`(= `G*=gτ_q/c` 와 연결)가 그 외부 척도다.
- **재현되는 것:** 중력 시간지연의 **형상·비율**(강하/탈출속도 river `√(2GM/r)`, `√(1−v²/c²)` 인자,
  cap 메커니즘으로서의 등가원리), Moon→중성자별 전 구간 비율(SSOT 모듈 `vp_timegravity_ssot.py`,
  `vp_gravity_ssot.py` 가 결정론 재생성).
- **재현 안 되는 것:** 위 비율에 곱해질 **절대 상수의 크기**(즉 g 의 절대값) — `[O]`, 측정 입력.

## 2. 전자기 미세구조 상수 (fine-structure constant, αₑₘ ≈ 1/137)

- **등급:** `[O]` (비증거 non-evidence)
- **위치(정본 HTML):** §14.5 STATUS NOTE
  (`docs/physics/14-force-lattice-tension-1-r2/`).
- **재현 불가 사유:** αₑₘ 는 **유도되지 않는다**. 닫힌형 `137 ≈ 4π(11 − δ_proj)`(=137.0364…)는
  **수치적 우연(coincidence)이자 비증거(non-evidence)** 로 표시된다 — 그 조립이 강제되지 않고(not
  forced), `4π` 는 **단위 인공물(unit artefact)** 이며, αₑₘ 는 **에너지에 따라 흐른다(runs with
  energy)**. 따라서 절대 g 와 동일한 계산-게이트 인식 등급이며 값은 **측정 입력**이다.
- **재현되는 것:** 격자 장력에서 `1/r²` 그린함수 형(force-lattice tension)의 **구조**.
- **재현 안 되는 것:** `1/137` 이라는 **무차원 결합 강도의 값** — `[O]`, 측정 입력.

---

## 3. 두 항목의 공통 인식 등급

저자 표현(부록 axg): "구조 유도 [F]" 와 "측정에서 고정한 절대 척도 [O]" 의 정직한 분리는
표준물리의 위계 문제(hierarchy problem)와 **같은 인식 상황**이다. 두 항목 모두 — 절대 중력 크기와
αₑₘ — **계산량 폭발/no-go 로 패키지 내부 결정론 재생성이 불가능**하므로 `[O]`(외부·측정 입력)로
둔다. 본 백서는 이 둘을 숨기지 않고 등급·사유를 본문에 명시한다(헌법 C3 충족).

## 4. 참조 위치 (이 두 항목을 인용하는 거버넌스/감사/요약 면)
- §01 거버넌스(`01-governance-no-tuning-lock-gate`) — no-tuning/LOCK 원칙에서 [O] 취급 규정.
- 감사 로그(`ea-epistemic-audit-log-what-happened`) — [O] 재분류 경위.
- 메타 교훈(`ml-meta-lessons-future-reviewers-contributors`), 버전 이력(`vh-...reclassification-log`).
- 한 장 요약(`w0-result-scorecard-one-page-summary`) — 전 항목 등급표에 [O] 명시.

## 5. 게이트 연동
헌법 게이트(VP-SPEC 8장)는 ① 모든 `[O]` 항목이 본문에 사유를 가지는지, ② 본 원장이 그 항목·사유·
위치를 빠짐없이 집계하는지를 정본 HTML 과 교차 확인한다. 수치 재현은 `tools/vp_*.py`(결정론,
2×sha256)가, 표시 드리프트 0 은 `gate.py --phase 4`(정본 HTML 대상)가 보장한다.
