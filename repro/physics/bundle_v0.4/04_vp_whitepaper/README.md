# VP Whitepaper (rigor v2) — DOI support files

이 폴더는 `vp_whitepaper_v0_1_2_rigor_v2.(tex|pdf)` 본문을 **DOI 번들에서 스스로 지지**할 수 있도록, 최소한의 재현 입력(data)과 산출(outputs), 그리고 이를 생성하는 스크립트(scripts)를 포함한다.

특히 본문 18장(화학/공정 확장)에서 등장하는
- 압력 지수 `P_idx` 정의,
- 동적 진폭 `r_eff` 계산,
- (선택) √2 임계 비교(표 18.3.*),
- (선택) Tb/Tm ≈ 1.6 비율(18.8.*)

을 **“텍스트 주장”이 아니라 “잠긴 입력 → 결정론적 계산 → 산출물”**로 연결한다.

## 폴더 구조(추가된 최소 구성)

- `data/chem/`
  - `species_effective_radius_pm.csv` : 원자/이온 종별 (Z, 유효 반경) 입력
  - `molecule_stoichiometry.csv` : 분자 조성 입력(예: H2O)
  - `observed_amplitudes.csv` : (선택) 보고/실측에서 추출한 진폭 값(표 18.3.*용)
  - `thermo_points.csv` : (선택) 상전이 온도(Tm, Tb) 입력(18.8.*용)

- `LOCK/chem_lock.json`
  - 위 입력들이 어떤 규칙으로 사용되는지(정규화 기준 H, r_vac 등)와
    재현/판정 허용오차(표시 반올림 규칙 포함)를 고정.

- `scripts/`
  - `run_chem_minimal.py` : 데이터+LOCK을 읽고 `outputs/chem/*` 및 `runs/*` 산출.

- `outputs/chem/`
  - 계산 산출(JSON + LaTeX table snippet)

- `runs/run_CHEM_MINIMAL_0001/`
  - 동일 산출물 + checksums + 실행 메타(환경/버전)

- `gate/reports/` (bundle root)
  - 최소 Gate 보고서(본 버전은 화학 파트의 **내부 정합** 및 **표 수치 재현**을 우선 다룸)

## 재현 방법(로컬)

```bash
cd 04_vp_whitepaper
python3 scripts/run_chem_minimal.py
```

성공 시:
- `outputs/chem/` 에 JSON/LaTeX 산출물이 생성되고,
- `runs/run_CHEM_MINIMAL_0001/` 에 동일 산출물 및 checksums가 기록된다.

## 주의(논리적 완결성 관점)

- 본 번들은 **수치 “기계적 일치”**가 목표가 아니라,
  본문에서 사용한 정의(LOCK)와 유도 규칙(derived)이 **끊김 없이 연결**되는지 확인하는 것을 1차 목표로 한다.

- `observed_amplitudes.csv`는 (현재 버전 기준) “실측 원자료”가 아니라
  보고서/문헌에서 *추출한 수치*를 잠근 입력으로 취급한다.
  원자료(PDF/원로그)를 DOI에 포함시키는 경우, `docs/chem/EXTRACTION_PROTOCOL.md`의 규약에 따라
  추출 절차와 페이지/표 매핑을 함께 봉인하는 것을 권장한다.

## v0.3.0 (current)
`vp_whitepaper_v0_3_integrated.tex` is the current whitepaper (supersedes the v0.1.2 rigor file kept here for history). New in v0.3: §8.5 dynamical grinder cross-check, §11.6.5 independent-reproduction [V] table + reproducibility map, §9.4 cross-reference. No locked constant changed.
