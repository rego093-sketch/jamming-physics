# Worked Examples

이 문서는 “누구나 같은 방식으로” 계산하게 하기 위한 최소 예시를 모았다.

## 예시 A: 정준 νₚ 계산(결정론)
1) r0 = D_anch/2  
2) s_p = r0 / r_p  
3) δ = 1/π²  
4) ν_p = s_p·δ

실행:
```bash
python scripts/compute_canon.py
cat LOCK/canon_derived.json
```

## 예시 B: 3-섹터 정수화(89/82)
```bash
python scripts/three_sector_integerize.py
```

## 예시 C: event_log에서 ν_obs 추정
```bash
python scripts/estimate_nu_from_eventlog.py runs/run_MINIMAL_0001
```

## 예시 D: 전체 run PASS/FAIL
```bash
bash validation/verify_all.sh
cat runs/summary_table.csv
```
