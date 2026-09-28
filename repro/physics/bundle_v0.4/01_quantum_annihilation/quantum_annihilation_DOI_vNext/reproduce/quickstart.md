# Quickstart (재현 3단계)

```bash
# 0) (권장) 가상환경 생성 후 requirements 설치
pip install -r reproduce/requirements.txt

# 1) LOCK 체인 생성
python scripts/make_lock_chain.py

# 2) 정준 파생값 계산(ν_p=292.339978..., ν_e=1 항등)
python scripts/compute_canon.py

# 3) 전체 run 자동 검증(PASS/FAIL)
bash validation/verify_all.sh
```

- `validation/_out/summary_table.csv`에 각 run의 PASS/FAIL이 저장됩니다.
- DOI 릴리즈 이후에는 `validation/verify_one.py --write` 사용을 금지합니다(불변성 원칙).
