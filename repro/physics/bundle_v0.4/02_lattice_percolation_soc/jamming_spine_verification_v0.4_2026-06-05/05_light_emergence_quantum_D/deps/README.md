# deps/ — 정본은 AQD 원본 (dedup됨)

본 모듈(05_light_emergence_quantum_D)의 A 분포 재현은 아래 AQD 원본 스크립트/데이터에 의존한다.
중복 봉인을 피하기 위해 사본을 제거하고 정본 경로만 둔다 (checksums 충돌 방지).

- `soc_percolation_pinning.py`  →  ../../../../01_quantum_annihilation/quantum_annihilation_DOI_vNext/src/simulator/legacy_bundle/soc_percolation_pinning.py
- `jamming_rotation_485pm_study.py` → 같은 legacy_bundle/
- `soc_run3_avalanches.csv` (n=82 avalanche 데이터) → 같은 legacy_bundle/  (ellrot_verify.py가 읽는 입력)

ellrot_verify.py 실행 시 위 정본을 이 폴더로 복사하거나 경로를 조정하라.
