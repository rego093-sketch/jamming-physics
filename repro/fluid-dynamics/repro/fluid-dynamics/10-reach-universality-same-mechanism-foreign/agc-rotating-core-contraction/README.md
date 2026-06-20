# Reproducibility package (DOI) skeleton
# "Anomalous Geometric Contraction of Hyper-Rotating Cores via Shockwave Confinement in High-Density Stiff Media"

이 패키지는 논문에 보고된 핵심 결과를 재현하기 위해 설계된 DOI용 데이터/코드 구조입니다.

- 그림/표 이미지는 포함하지 않습니다.
- 각 그림·표에 해당하는 **수치 데이터는 CSV 파일로 제공**됩니다.
- 시뮬레이션 코드는 템플릿 상태이며, 실제 구현과 데이터 채우기는 사용자가 보유한 코드/결과를 기반으로 보강하면 됩니다.

## 주요 디렉터리

- `env/` : Python/Conda 환경 정의
- `src/` : Euler–HLLC 솔버 및 후처리(post-processing) 템플릿
- `cases/` : 검증 케이스 및 본문 주요 케이스 설정
- `data/`
  - `processed_for_figures/` : 각 그림용 CSV (일부는 예시 데이터까지 포함)
  - `tables/` : 표(Table)용 CSV (Table 2, EOS 파라미터 등)
  - `verification/` : shock tube 등 검증용 CSV 스켈레톤
  - `sensitivity/` : 민감도 분석용 CSV 스켈레톤
- `docs/` : 재현 가이드 및 아날로그 설명 템플릿
- `metadata/` : 케이스-데이터-그림 매핑 정보
