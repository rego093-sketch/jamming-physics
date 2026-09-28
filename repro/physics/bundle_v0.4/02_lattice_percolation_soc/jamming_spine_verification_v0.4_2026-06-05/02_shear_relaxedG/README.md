# 02 — 전단 G→0 (백서 §5 미해결문제의 해결·검증)

## 물리
한계잼밍 z=z_iso=2d=6 에서 전단 강성에 필요한 접촉이 딱 임계라 **잉여가 0** ⇒ 완화 전단
탄성률 G_relaxed → 0. 이것이 종파만 남기는(01의 c²=B/ρ) 전제다. 다섯 독립 관측이 같은
문턱 z=6 을 가리킨다.

## 방법 (검증된 핀-해 — 01과 공유)
backbone 최고배위 입자 3 DOF 핀 → 양정치 축약 Hessian → Cholesky(PSD 게이트) → 반복정제.
변분적으로 0 ≤ G_rel ≤ G_Born. Lees-Edwards 전단(le_shear.py)과 AQS(aqs.py)는 별도 검증됨.

## 파일 (핵심)
- `relaxed_shear.py` — 공유 인프라(패킹/Hessian/backbone/Born/relaxed G).
- `le_shear.py` — Lees-Edwards 유한변형 전단(검증됨). `aqs.py` — 준정적 전단.
- 러너: `production_run.py`(relaxedG vs z), `collect_spectra.py`(DOS·ω*), `flow_run.py`(흐름곡선),
  `aqs_run.py`/`focused_aqs.py`(항복).  검증: `validate_le.py`, `validate_aqs.py`.
- 그림 생성: `make_figure.py`, `make_dos_figure.py`, `make_flow_figure.py`, `make_aqs_figure.py`, `fig_finite_size.py`.
- `analyze.py` — z₀ bootstrap 등 분석.
- `FINDINGS_relaxedG.md` — 본 모듈의 상세 발견 기록.
- `results/` — `relaxedG.csv`, `flowcurve.csv`, `aqs_sigmay.csv`, `spectra/`(35 npz), `aqs_curves/`(8 npz), 그림(png/pdf 다수).

## 결과 [V] — 다섯 관측이 z=6 으로 수렴
1. **G_relaxed → 0** @ z≈5.9–5.95 (z₀ bootstrap: N=512→5.90, N=1024→5.95).
2. **ω* = 0.143(z−6.015)**, R²=0.997 (boson-peak 주파수 선형 소멸).
3. **η → ∞** (점성 발산, 흐름곡선).
4. **AQS 기울기 = G_relaxed** (<1% 일치).
5. **σ_y → 0** (항복응력 소멸).

## 실행
```bash
python3 production_run.py      # relaxedG vs z (수 분~)
python3 make_figure.py         # relaxedG_vs_z 그림
python3 validate_le.py         # Lees-Edwards 검증
```
(주의: N=750 이상 대형런은 수 시간 — 피할 것. 결과 CSV/NPZ 는 이미 동봉.)
