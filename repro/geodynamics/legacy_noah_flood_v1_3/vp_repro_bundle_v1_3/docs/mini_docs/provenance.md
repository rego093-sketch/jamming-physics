# 데이터 출처 및 정제 규칙 (Provenance)

원출처(요약):
- IntCal.org (R6; IntCal20), 14CHRONO Marine Reservoir DB (R7)
- PALSEA/HOLSEA, PALEO-SEAL (R8 RSL 표준화 자료)
- EUROEVOL, p3k14c (R9 유럽 인골 SPD)
- Stanley & Warne 1994, PANGAEA (R10 나일 삼각주 베이스라인/현장물성)

정제 규칙:
- (site, Age_BP, C14_age, lab_id) 복합키 기준 중복 제거
- ΔR는 같은 층(same-layer) paired 시료만 포함, n≥10/분지 권장
- RSL은 ICE-6G_C 등의 GIA 모델 표기와 국지 융기/침강 메모 필수
- SPD는 δ13C, 보정곡선(curve), provenance 열을 포함(QC: 지표 누락 시 제외)
