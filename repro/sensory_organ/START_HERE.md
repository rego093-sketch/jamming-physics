# START HERE — Special-Sense Organs (sensory_organ_vp_site)  ·  v0.4.0-published

> 이 zip을 **새 창에 넣고 이 파일 → CHARTER.md 순서로 읽으면** 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질(FHN/R19), VP-SPEC v1.8 전문, 노드 정체성 γ를 내부에 들고 있다.  **개념 DOI: 10.5281/zenodo.20755154 (최신본으로 해상). Living version: https://jamming-physics.org/sensory-organs/ . v0.4.0에서 발행(DOI 부여 + PDF/TeX 디포짓) 완료.**

## 0. 한 줄 정체
The special-sense ORGANS as physical instruments: ocular optics/accommodation, the cochlear basilar-membrane frequency map, vestibular inertial sensing, and taste/olfaction chemodetection. Organ optics/acoustics are CLASSICAL physics (documented, linked); the R19 substrate handles the cellular transduction switch. neuro owns transduction->spike. Cataract, glaucoma, AMD, presbycusis are the disease axis.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 9개 섹션 출력: [1] 측정 γ에서 노드 **창발**(미측정 master는 정직하게 "측정 대상" 보류) + 발생순서 검증, [2] 진동자, **[3] 분자 변환기**(모든 감각 변환기 = R19 쌍안정 이온채널 스위치; CNG/MET/TAS 채널, NCBI 인용), **[4] 와우 Hopf 증폭기**(임계점 μ=0에서 세제곱근 압축 지수 1/3, 무-튜닝), **[5] 기관 광학/음향**(고전물리, 인용·검증), [6] 스트레스 배터리, [7] 병리(setpoint 표류 법칙), **[8] 근본 치료**(치료 = 역(逆) 기질 연산), [9] 게이트(결정론 + 집필잠금). HTML은 만들지 않는다.

> **v0.4.0 상태:** 집필(writing) 확장 마감 + **발행(published) 완료**. 검증 코퍼스에서 제목별 정본 HTML을 결정론적으로 생성하고, 이번 판에서 **개념 DOI `10.5281/zenodo.20755154`를 부여**했다(생성기 경유 — 하드에디트 아님). claim-strip·JSON-LD(`identifier`/`sameAs`)·footer·랜딩·`llms.txt`·`_meta.json`의 `DOI: TBD`가 전부 실값으로 교체되어 `docs/` 내 **TBD 0건**, 재빌드 **바이트 동일**, 검색/SEO 게이트 **0 FAIL / 0 WARN**. 또한 동일 코퍼스에서 **결정론적 LaTeX/PDF 백서**(`dist/sensory_organ_vp_site.{tex,pdf}`, 18쪽, 선택가능 텍스트, 표지에 *Living version* = 허브 URL + DOI)를 생성했다 — `tools/build_tex.py` + `tools/build_pdf.sh`, **독립 컴파일 바이트 동일**(PDF sha256 `c6593c81…`, TeX sha256 `6e76c5dd…`). 연구는 그대로 green(`reports/research_complete.json` all_green=true, 2×sha256 `6a68bc48…`, RS1–RS5 PASS) — 발행은 검증 결과를 렌더/유도만 하며 **새로운 [O]를 만들지 않았다**. PHASE=`published`. 다음 세션의 단계는 **모노레포 통합**(repro/ 푸시, cross-volume 레지스트리에 10번째 권 등록).

## 2. 범위 (물리적/시간적 클래스)
mind처럼 **시뮬레이션으로 창발하여 순환**시키되, 정체성·발생순서는 DNA 인용(SSOT), 동역학만 추가. 클래스 밖은 형제 소관 — 아래 seam으로만 인용.

| master gene | node | measured γ | role | dyn class |
|---|---|---|---|---|
| PAX6 | eye_retina_optics | 1.511 | retinal photoreceptor mosaic + the ocular dioptric system (optics classical; switch R19) | sensor |
| RAX | eye_photoreceptor | 1.4541 | photoreceptor phototransduction switch (R19 cellular) | sensor-switch |
| EYA1 | cochlea_frequency_map | 1.3638 | basilar-membrane tonotopic frequency analysis (mechanics classical; switch R19) | sensor |
| SOX2 | inner_ear_haircell | 1.4573 | cochlear/vestibular hair-cell mechanotransduction (R19 switch) | sensor-switch |
| (vestibular_system) | vestibular_balance | —(diffuse) | semicircular-canal + otolith inertial sensing (balance) | sensor |
| TAS1R3 | taste_chemodetection | 1.5555 | taste receptor chemodetection (sweet/umami; bitter via TAS2R) | sensor |

**상속(IN) — 내부 vendoring + 형제 seam 인용:**
- neuro: transduction->spike->brain is neuro's; this pkg hands off the transduced signal (cited)
- circulatory: ocular / cochlear perfusion (cited)
- circadian: retinal light also feeds the master clock (seam to circadian)
- DNA: identity + order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT):**
- transduced sensory signal -> neuro (this pkg is SSOT for the organ-physics stage)
- retinal light -> circadian_vp_site (entrainment input)

## 3. 판별 타깃 (발굴된 연구과제 — CHARTER에 전체 프로그램) — v0.2.0 전부 PASS
- **RS1** ocular optics: accommodation focuses the dioptric system; refractive error = focal/axial mismatch (CLASSICAL optics, documented + linked, NOT an R19 claim) — axial 22.27 mm, 2.69 D/mm, presbyopia 1 D@60 [V-arith]
- **RS2** phototransduction: rod CNG channel as an R19 bistable/cooperative switch — all-or-none, discontinuous flip [V]; cGMP threshold [L]
- **RS3** cochlear tonotopy: Greenwood place-map 20 Hz..21 kHz [L] + MET gating-spring switch [V] + **Hopf amplifier cube-root compression exp=1/3 at criticality [V]**
- **RS4** vestibular: semicircular-canal torsion pendulum computes angular VELOCITY over 0.1–6 Hz (flatness=0.018); VOR gain ~1.0; canal dynamics classical [V]
- **RS5** chemodetection: taste/olfaction receptor → cation channel as an R19 threshold switch [V]; olfaction shares the SAME CNG family as the rod; EC50 [L]

**근본(아래로) — 분자 변환기 + 치료 + 문헌:** [3] 모든 변환기 = R19 쌍안정 채널(CNGA1/CNGB1·TMC1/PCDH15/CDH23·TAS1R2/TAS1R3/TRPM5·CNGA2/ADCY3, 전부 NCBI/UniProt 인용; γ는 DNA 파이프라인 `_to_measure`로 이양). [8] 근본 치료 = 역 기질 연산(loop-gain 복원/장벽 상승/오차신호 재결합/기기 수리/폭주 loop-gain 하강) — 7개 질환, 반론/부분 항목 정직 표기(AMD 기능적 시력개선 아직 없음·백내장 가역화 재현실패·ATOH1 미성숙). 전체 인용: `literature/CITATIONS.md` + `literature/citations.json`.

## 4. 주요 질환 (이 패키지가 다루는 비-희귀 질환)
질병 = 방어 setpoint/시계/감각기관의 실패(loop-gain 하락 / setpoint 표류 / attractor-shift / 기기 실패), 발암과 동일한 R19 기질. 위치: `repro/_pathology/`. **희귀·단일유전자 질환은 disease_wp 소관 — 여기선 교차참조만** 하고 파라미터로 합성한다.
- **cataract** ← lens opacification (age / UV / oxidative) -> optical scattering  · opacity vs cited age/UV [L]; UV cross-ref integumentary; rare congenital -> disease_wp
- **glaucoma** ← intraocular-pressure setpoint failure -> retinal ganglion-cell loss  · IOP setpoint + RGC loss [V]; cited [L]
- **age-related macular degeneration** ← photoreceptor / RPE degeneration (age)  · degeneration vs cited age [L]; cross-ref aging
- **refractive error (myopia)** ← axial-length / focal mismatch (classical optics)  · prevalence vs cited [L]; optics classical
- **presbycusis / noise-induced hearing loss** ← hair-cell loss (age / acoustic over-drive)  · threshold shift vs cited age/noise dose [L]; hair-cell over-drive [V]
- **diabetic retinopathy** ← microvascular damage from chronic hyperglycemia (seam to thermometabolic/diabetes)  · cross-ref thermometabolic; microvascular [V]
- **BPPV / vertigo** ← otolith displacement -> false motion signal  · mechanical displacement [V]; cited [L]

## 5. 절대 규칙 — 연구 먼저, 집필 나중
**엄격한 연구(많은 스트레스 실험) 완료 전 집필 금지.** `tools/build_docs.py`는 잠금 동안 거부. 해제: ① `research_gate()` all_green ② `write_research_complete()` ③ `PHASE=writing`.

## 6. 집필 규칙 (VP-SPEC v1.8 — 루트 `VP_SPEC_v1_8.md`)
정본 HTML(C2) · 제목별 별도 SEO HTML(C4: answer-first·JSON-LD·claim-strip·vp-card) · 본문 영어(C0) · 정량 결정론 재생성(C1) · 모든 [O] 사유 명시(C3). **개념 DOI `10.5281/zenodo.20755154` 부여 완료 — 생성기가 claim-strip·JSON-LD·footer·랜딩·llms·`_meta.json`에 실값을 방출한다.** 출력: `docs/<slug>/index.html` + 허브 + sitemap/robots/llms + `dist/`의 PDF/TeX.

## 7. 인수인계 (자동)
새 창은 이 파일 → `CHARTER.md`(연구 프로그램 전체)만 읽으면 범위·이음매·연구과제·질환·게이트·집필규칙·DOI상태를 전부 파악한다. 상태는 파일로만 전달, 종료 시 단일 zip으로 다음 세션에. 반환은 압축파일 1개(파편화 금지, C0).

**v0.4.0 인계 — 발행(DOI + PDF/TeX) 완료, 다음 세션 = 모노레포 통합:** 연구 서명 + 집필(확장) + 발행 모두 완료.
① **DOI 부여:** 개념 DOI `10.5281/zenodo.20755154`를 생성기(`tools/_sns_render.py`의 `DOI`/`DOI_URL`)에 주입,
claim-strip·footer·랜딩·`llms.txt`·`_meta.json`의 `DOI: TBD`를 실값으로 교체하고 챕터 JSON-LD `ScholarlyArticle`에
`identifier`+`sameAs`(=DOI URL)·시리즈 `identifier` 추가. `docs/` 재빌드 **바이트 동일**, 검색/SEO 게이트 **0 FAIL/0 WARN**,
`docs/` 내 **`TBD` 0건**. (하드에디트 금지 — `docs/`는 전부 생성기 재실행으로만 바뀜. site.css의 죽은 `.doi-tbd`는 활성 `.doi` 링크로 정리.)
② **PDF/TeX:** `tools/build_tex.py`가 **동일한** `_sns_content`(산문=데이터) + **동일한** 검증 수치(2×sha256 `6a68bc48…`)에서
LaTeX를 렌더 → 사이트와 드리프트 불가. `tools/build_pdf.sh`(SOURCE_DATE_EPOCH + `\pdfinfoomitdate`/`\pdftrailerid`)로
컴파일 → `dist/sensory_organ_vp_site.{tex,pdf}`. 18쪽, 스케일러블 Type-1 폰트(선택가능 텍스트), 표지에 *Living version*(허브 URL + DOI) +
locked-quantity 결과표, 12챕터(answer-first 박스·vp-card·표·참고문헌). **독립 컴파일 바이트 동일**: PDF sha256 `c6593c81…`,
TeX sha256 `6e76c5dd…`.
③ **게이트:** `gates.writing_locked()`를 PHASE ∈ {writing, published} 에 대해 unlock 하도록 확장(안전 보존 — research_complete.json
all_green 여전히 필수). PHASE=`published`.
**남은 단계(다음 세션):** ① `repro/`를 모노레포 `repro/sensory-organs/`로 푸시(REPRO_BASE 경로는 이미 그 자리로 설정됨),
② Zenodo 레코드(개념 DOI 20755154)에 PDF + repro zip 업로드 + 허브 역링크, ③ 상위 `registry/cross_volume_doi.{csv,md}`에 10번째
권으로 등록. **하드 에디트 금지 — 변경은 생성기 재실행으로만.** 반환은 압축파일 1개(파편화 금지, C0).
