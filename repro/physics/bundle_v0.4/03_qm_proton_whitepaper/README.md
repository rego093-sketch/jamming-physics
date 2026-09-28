# 양성자 연속체 모형 + 82/89 기하학 + 전자 생성 메커니즘 DOI 번들 (통합판)

이 압축 번들은 다음 세 가지 축을 **한 번에 재현**할 수 있도록 통합한 패키지입니다.

1. 연속체 회전 모형을 이용한 양성자 반지름 hydrodynamic white paper
2. 82 코어 + (6 진동 + 1 전자) 셸 구조(89 유닛) 기하학 및 몬테카를로 셸 역학
3. 전자기력/전하 스케일링을 위한 최소 수치 실험(`quantum_whitepaper`)

## 디렉토리 구조

- `docs/`
    - `ProtonRadius_Annals_of_Physics_main.pdf` : 연속체 hydrodynamic 길이 선택 본문
    - `ProtonRadius_Annals_of_Physics_supplement.pdf` : 보충 설명(SM)
    - `빛의_속도와_전자1초_수정본_v3.docx` : 전자 1초, 사건률 관련 한글 문서
    - `양성자와_전자의_전자기력의_기원.txt` : 양성자–전자 전자기력 기원 한글 노트
    - `images/`
        - `proton_shell_structure.png` : 82 코어 + 7 셸 구조 개략
        - `proton_shell_mc_histogram.png` : 셸 생존 벡터 히스토그램 예시
        - `proton_core_3sector_geometry.png` : 3-섹터 (예: 37/28/24) 기하학 도식

- `packages/`
    - `proton_geometry_v1/`
        - `code/simulate_proton.py` : 82+7 재밍 격자 기반 89-유닛 구조 생성
        - `code/analyze_vectors.py` : 셸 7개 벡터의 상쇄/생존, 135° 각도, 23.5° 축 기울기 분석
        - `data/proton_89_coords.json` : 89 유닛 좌표 데이터
        - `results/simulation_log.txt` : 예시 실행 로그
        - `docs/proton_electron_em_origin_kr.txt` : 프로톤–전자 EM 기원 한글 설명
    - `jamming_qm_qbook/`
        - `code/proton_radius_model.py` : `R_p = (2/π) λ_C` 및 압력 스케일링 확인
        - `code/proton_shell_mc.py` : 7 셸 유닛 몬테카를로(700회) 데모
        - `code/electron_one_second.py` : 전자 사건열로부터 전자 1초 복원 골격
        - `docs/qm_textbook_outline.md` : 양자역학 교과서급 전개용 개요
    - `quantum_whitepaper/`
        - `code/whitepaper_experiments.py` : hydrodynamic white paper용 4개 수치 실험
        - `data/*.csv` : 위 스크립트로 재생성 가능한 실험 결과

- `scripts/`
    - `verify_all.sh` : 번들 전체를 한 번에 재실행/검증하는 원커맨드 스크립트
    - `make_manifest_sha256.py` : SHA-256 기반 `MANIFEST.sha256` 재생성 스크립트

- `requirements.txt` : 최소 파이썬 패키지 의존성 (numpy, pandas)
- `MANIFEST.sha256` : 번들 내 모든 파일의 SHA-256 해시 목록
- `LOCK` / `LOG` : 번들 버전/생성 정보 및 빌드 로그(간단한 텍스트)

## 재현 방법 (원커맨드)

1. 압축 해제 후 최상위 디렉토리로 이동:

   ```bash
   cd qm_proton_whitepaper_doi_full   # 디렉토리 이름은 상황에 따라 달라질 수 있음
   ```

2. (선택) 파이썬 가상환경 생성:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. 의존성 설치:

   ```bash
   pip install -r requirements.txt
   ```

4. 전체 재현 실행:

   ```bash
   bash scripts/verify_all.sh
   ```

   이 스크립트는 다음을 순서대로 실행합니다.

   - `proton_geometry_v1/code/simulate_proton.py`
   - `proton_geometry_v1/code/analyze_vectors.py`
   - `quantum_whitepaper/code/whitepaper_experiments.py`
   - `jamming_qm_qbook/code/proton_shell_mc.py`
   - 마지막으로 `scripts/make_manifest_sha256.py` 를 호출하여
     `MANIFEST.sha256`를 다시 생성합니다.

위 과정을 통해 **연속체 모형(λ_C 및 R_p)**, **82/89 재밍 기하학**, **7 셸 몬테카를로**,
**전자 1초/전자기력 기하학**까지를 하나의 DOI 번들에서 재현할 수 있습니다.
