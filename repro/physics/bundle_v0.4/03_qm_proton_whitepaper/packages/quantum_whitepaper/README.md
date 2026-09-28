# quantum_whitepaper 패키지

hydrodynamic proton-radius white paper(연속체 회전 모형)에 대응하는
최소 수치 실험 모음입니다.

포함된 내용:

- `code/whitepaper_experiments.py`
    - 실험 1: `R_p = (2/π) λ_C` 수치 검증, 실험값과의 상대 오차 기록.
    - 실험 2: `p_in(x) = x^-4`, `p_stiff(x) = α x^-5` 곡선과 교점 구조.
    - 실험 3: 기하 상수 `α` 변화에 대한 `R_p` 민감도(선형 스케일링) 확인.
    - 실험 4: Swift–Hohenberg 분산 관계에서 `L* ∝ (σ/ε)^(1/2)` 스케일링.

- `data/*.csv`
    - 위 4개 실험이 생성하는 결과 표(csv).

## 실행 방법

패키지 루트(최상위 DOI 번들)에서:

```bash
# 가상환경 예시
python -m venv .venv
source .venv/bin/activate  # Windows에서는 .venv\Scripts\activate

pip install -r requirements.txt

# quantum_whitepaper 실험만 다시 돌리고 싶을 때
python packages/quantum_whitepaper/code/whitepaper_experiments.py         packages/quantum_whitepaper
```

실행이 끝나면 `packages/quantum_whitepaper/data` 디렉토리에
`experiment1_*.csv` ~ `experiment4_*.csv`가 다시 생성됩니다.
