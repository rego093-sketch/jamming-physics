# 코드북(Codebook) · 스키마 요약

## R6_IntCal_Marine_combined.csv
- calBP(int): 보정연대(Before Present)
- C14_age(int): 방사성탄소 원시연대
- C14_sigma(int): 1σ 불확도
- curve_id(str): IntCal20/Marine20 등

## R7_DeltaR_Med_repro.csv
- region, site, layer(str): 지중해 분지/유적/층위
- marine_id, terr_id(str): 해양/육상 시료 식별자
- deltaR(int): 해양 저장소 보정(yr)
- deltaR_sigma(int): 1σ
- window_ka(str): 창(예: "6-4")
- QC_flag(str): PASS/FAIL

## R8_RSL_repro.csv
- basin, site, datum, proxy, age_model(str)
- Age_BP(float): 연대(BP)
- RSL_m(float): 상대해수면(m)
- RSL_sigma(float): 1σ(m)
- tectonic_corr(float): 국지 융기/침강 보정(m)
- GIA_model(str): 예 "ICE-6G_C"
- QC_flag(str)

## R9_SPD_repro.csv
- lab_id, material, context(str)
- lat, lon(float)
- C14_age(int), C14_sigma(int), delta13C(float)
- curve(str): IntCal20 등
- provenance(str): EUROEVOL/p3k14c 등

## R10_seismic_summary.csv
- line_id(str), lat, lon(float)
- thickness_m(float), thickness_sigma_m(float)
- facies(str), method(str), QC_flag(str)

## R10_compaction_curve.csv
- phi0(float): 초기 공극률
- c(float): 압밀 계수(1/m)
- z_min_m, z_max_m(float): 깊이 범위
- reference(str), QC_flag(str)

## R10_bulk_density_summary.csv
- Q1, Median, Q3(float): 벌크 밀도 사분위(t/m³)
- method(str), n(int), QC_flag(str)
