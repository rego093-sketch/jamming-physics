# START HERE — Reproductive / Gonadal-Endocrine (reproductive_endocrine_vp_site)  ·  v0.7.1-writing

> 이 zip을 **새 창에 넣고 이 파일을 먼저 정독**하면 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질 프리미티브(FHN/R19), VP-SPEC v1.8 전문, 장기 정체성 γ를 내부에 들고 있다.

## 0. 한 줄 정체
Gonads, the gonadal-endocrine (HPG) axis and the germline emerge on the substrate; the menstrual cycle is a slow relaxation oscillator, hormone feedback is a switch, and sex hormones act as the sustained drive in hormone-driven cancers. Brain-facing HPA stays in mind (firewall); this package owns the gonadal axis only. **v0.5.0 opened the germ cell itself (G1–G6); v0.6.0 lets the two gametes MEET and builds a fetus (E1–E6). v0.7.0 then answers, as two separate HTML parts, why conception FAILS (infertility = an operation past a spinodal — categorical, per-cycle p=0; subfertility = a near-threshold Kramers rate the same drive moves exponentially) and how a gene biases offspring sex (the SOX9↔FOXL2 switch tilted by meiotic / sex-chromosome drive, Fisher restoring 1:1) — F1–F6, S1–S6.**

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 **4개 장기를 모두 창발**(FOXL2/DAZL/WT1 γ 수령 완료, 미측정 보류 없음), 진동자 박동 확인, **T1–T5 + G1–G6 + E1–E6 + F1–F6 + S1–S6 판별 배터리**(가메트·배아·불임·성비 포함, 29 suites)·암 모듈 상태, **집필 잠금 여부**를 출력한다. HTML은 만들지 않는다. 배터리만 단독 실행하려면 `python repro/_germline/gametogenesis.py`(→ G1–G6), `python repro/_embryo/embryogenesis.py`(→ E1–E6), `python repro/_fertility/infertility.py`(→ F1–F6), `python repro/_sexratio/sex_ratio.py`(→ S1–S6) — 전부 PASS.

## 2. 이 백서의 범위 (자기 범위를 명확히)
mind가 하듯 **장기를 직접 시뮬레이션으로 창발하여 순환**시킨다. 단 이 패키지는 기계(mechanism) 동역학을 다루며 felt(느낌)는 mind의 몫이다. 분해 기준은 **물리적 클래스**(이 패키지: jamming (hormonal-cycle / germline))이며, 클래스 밖은 형제 패키지 소관 — 아래 이음매로만 인용한다(SSOT).

| master gene | organ | measured γ | physiological role | dyn class |
|---|---|---|---|---|
| SOX9 | gonad_testis | 1.4598 | testis determination (SRY->SOX9) + Sertoli/spermatogenesis support | germline-support |
| FOXL2 | gonad_ovary | 1.4829 | ovarian determination + folliculogenesis (menstrual oscillator) | oscillator |
| DAZL | germline | 1.3803 | gametogenesis (meiotic program) | germline |
| WT1 | reproductive_tract | 1.5182 | gonadal / tract scaffold | structural |

> γ 수령 완료: FOXL2/DAZL/WT1는 동일 DNA `fetch_morpho_gamma` 파이프라인(`repro/_gamma/fetch_gamma.py`, NN-stacking ΔG37 / SantaLucia 1998, promoter TSS-2000..+500)으로 **측정**되었고 `inherited/organ_promoters.cache.json`에 캐시되어 오프라인 비트재현된다(SOX9 1.4598/0.545 재현으로 파이프라인 검증). 발생순서(γ↑): germline → testis → ovary → tract [V].

**상속(IN) — 내부 vendoring됨, 재수령 불필요:**
- mind/neuro: GnRH pulse-generator neural edge (CITE, do NOT re-emerge; mind owns brain-facing HPA, this owns the gonadal HPG response)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT) — 형제 패키지와의 이음매(SSOT 단일소스 유지):**
- sex-hormone levels (systemic; this package is SSOT)

## 3. 판별 타깃 (엄격히 통과시켜야 집필 가능)
- **T1 HPG pulse** — GnRH pulse -> LH/FSH (the gonadotropin pulse generator as an FHN oscillator) [V], rate [L]
- **T2 menstrual cycle** — follicular->luteal as a slow relaxation oscillator, ~28 d period [V], period [L]
- **T3 hormone feedback switch** — estrogen negative feedback + the mid-cycle LH-surge positive feedback (a switch) [V]
- **T4 spermatogenic cycle** — cycle timing / period from the substrate [V]
- **T5 puberty onset** — gonadotropin reactivation as a threshold crossing [V]

**가메트 배터리 G1–G6 (생식세포 자체, v0.5.0)** — `repro/_germline/`, 측정 가메트 프로그램 γ(13유전자, 동일 DNA 파이프라인, SOX9·DAZL 두 앵커 재현 시에만 저장)만 새 입력. 연구 게이트에 편입, 해시 코어 불변.
- **G1** 감수분열 = 1복제 + 2**순서**분열(환원→균등), REC8 2단계 코헤신(shugoshin 보호 부호가 순서 강제) [V]
- **G2** 생식세포는 **동일하지 않다** — 독립분리 2²³ + 교차 간섭 = 기질 불응기를 염색체축에 사상(obligate CO), floor 10⁴⁷ [V]
- **G3** 정자 운동 — 편모 박동 = 이완진동자 사다리의 **최속단**; CatSper Ca²⁺ = 과활성화 이득 스위치(진폭↑·박동↓) [V]; 9+2 축사 정수 9 [O]
- **G4** 난자 논리 — 중기-II = 붙잡힌 스위치; 수정 = spinodal 초과 일방 플립; 다정자 차단 = past-spinodal 비가역 [V]
- **G5** 가메트 γ 아틀라스 + **사전등록** 모듈-분리 검정(NULL 허용, 정직 보고); 재조합 코어 클러스터만 주장 [V]
- **G6** 정자/난자 **이중성** — 한 기질 → 자유진동자(정자) vs 붙잡힌 스위치(난자); 대칭(4 정자) vs 비대칭(1 난자+3 극체) → anisogamy [V]/[L]; 진화적 '왜' [O]

**배아 배터리 E1–E6 (수정 → 태아, v0.6.0)** — `repro/_embryo/`, 측정 발생 마스터 γ(17유전자, 동일 DNA 파이프라인, 단계/HOX로 선언 후 측정, SOX9·DAZL 두 앵커 재현 시에만 저장)만 새 입력. 연구 게이트에 편입, 해시 코어 불변. (사람은 **개념적**으로 — γ 기반 유전자시계이지 전체 게놈 합성이 아님.)
- **E1** syngamy + **DNA 창발** — 정자(진동자)가 난자(붙잡힌 스위치)를 supra-spinodal로 일방 플립(다정자 차단 유지); 두 반수체 전핵 융합 → 2배체 복원(1N+1N→2N); 새 게놈은 **10⁹⁴** floor로 고유(가메트 floor의 제곱) [V]
- **E2** cleavage — 2ⁿ **대칭** 분열(난자형성 1+3과 대비), 세포질 질량 **보존**(난할 ≠ 성장); ICM/TE 결정 = R19 양안정 스위치 [V]
- **E3** ZGA — 모체→접합체 전이 = **1단계 spinodal 교차**(모체 저장 ZAR1/NLRP5에서 OFF → spinodal 초과 시 ON); 이 패키지가 소유한 가메트 프로그램에서 배아 자체 게놈으로의 인계 [V]
- **E4** **유전자시계**가 몸을 만든다 — 창발순서 = argsort(spinodal(γ)); **사전등록** 단계검정(γ↑ 다능성<배엽<기관) **지지**(Spearman ρ≈0.55, p≈0.02); HOX 3′→5′ 공선성 검정은 부분 결과(NULL 허용). **방화벽:** 유전자시계 법칙 + 전신 아틀라스는 DNA 4D-Blueprint 패키지 SSOT(인용) — 여기서는 측정 시연 [V on the demonstration]
- **E5** 전체 호 — 특정 정자 + 특정 난자 → syngamy → cleavage → ZGA → 유전자시계 body plan → 태아(고유 게놈, ICM 유래), end-to-end 결정론 [V]
- **E6** 정직 스코어보드 + 방화벽 재천명: [V] 사건/순서; [L] 측정 γ + 구조 앵커; [O] 절대 임신 시점(사춘기 연령처럼) + 전신 아틀라스(DNA SSOT)

**불임/난임 배터리 F1–F6 (왜 임신이 실패하는가, v0.7.0)** — `repro/_fertility/`, 같은 기질 위에서 임신 실패를 답한다. 새 γ 없음(가메트 기계 γ + 종양 챕터의 `exp(−ΔV/D)` 재사용).
- **F1** 임신 = 8개 기질 연산의 **AND**; 한 게이트라도 0이면 임신 0(고리 하나 끊기면 불임) [V]
- **F2 (중심)** 불임 = spinodal **너머**(범주적, 주기당 p=0, 미만 드라이브 무반응) / 난임 = 문턱 **근처**(유한 Kramers 율); 같은 nudge가 난임은 1.56× 올리고 불임은 0 그대로 — 지수적 vs 전무 [V]
- **F3** 남성 인자 = 진동자 **처리량**(무정자증 = 스위치 OFF, 수/운동성 = 박동률 51→7) + CatSper 게이트 [V]
- **F4** 여성 인자 = 배란 서지 스위치 + **REC8 코헤신 피로**(오분리 0.121→0.752, 나이 25→45); POI = 조기 래치 상실 [V]; 절대 분율 [O]
- **F5** 치료 = 기질 이동(hCG = supra-spinodal 킥; 박동성 GnRH 재시동 41 vs 0; ICSI/IVF = 게이트 우회) [V]/[L]
- **F6** 정직 스코어보드 + 방화벽(임상 관리는 임상의 몫)

**성결정/성비 배터리 S1–S6 (한 유전자가 성별을 기울인다, v0.7.0)** — `repro/_sexratio/`, 측정 성결정 마스터 γ(6유전자, 축으로 선언 후 측정, SOX9·FOXL2 두 앵커 재현 시에만 저장)만 새 입력. 연구 게이트 편입, 해시 코어 불변.
- **S1** 성 = **양안정** 스위치(SOX9↔FOXL2, SRY 구동 후 유지), supra-spinodal에서만 전분화 [V]
- **S2** 멘델 50:50 = **기울지 않은** 분리 스위치(앙상블 0.4983) — 공정한 동전 [V]
- **S3** 분리 왜곡 = **기울임**(점진 0.86 → supra-spinodal 고정 1.0) [V]
- **S4** 성비 왜곡 = **부호 있는** 성염색체 가메트-킬러(X-shredder 1.0 수컷 / Y-killer 0.0 암컷) [V]
- **S5** 피셔: 인구 성비 1:1 = **안정 끌개**(인간 SSR ~0.512 = 작은 잔차) [V]
- **S6** γ 아틀라스(SRY 1.2550 이상치 … WNT4 1.5992) + 사전등록 축-분리 검정 **NULL 정직 보고**(순열 p=0.10) [V on the test]

## 4. 담당구역 질환 + 암 (mind과 다른 점)
이 패키지의 **담당구역 질환**을 모두 망라하되, 특히 외부자극(발암물질) 노출 시 암이 **얼마나 더** 발생하는지의 메커니즘을 연구한다. VP-native 커널: 발암물질 = R19 스위치의 지속 이상 드라이브 h_c → 장벽 낮춤 → 악성 basin Kramers 교차율↑ → **RR(dose)** = rate(dose)/rate(0). 판별 = 용량-반응 형상 vs 인용 역학 앵커. 등급: 앵커 [L]/형상 [V]/절대 발생률 [O](장애물 명시). 위치: `repro/_oncology/`.
- **breast carcinoma** ← cumulative estrogen exposure (HRT, early menarche); ionizing radiation  · anchor: estrogen-exposure RR (HRT cohorts) [L]; hormone as sustained drive [V]
- **cervical carcinoma** ← HPV infection x co-factors (smoking)  · anchor: HPV infection x carcinogen synergy RR (like H. pylori/gastric) [L]; synergy [V]
- **prostate carcinoma** ← androgen exposure; age  · anchor: androgen-driven; absolute RR less clean -> honest [O]; shape [V]

## 5. 절대 규칙 — 연구 먼저, 집필 나중 (명시) — **집필 해제됨 (v0.4.0)**
**매우 높은 수준의 엄격한 연구(많은 스트레스 실험 포함)를 완료하기 전에는 집필하지 않는다.** 이 규칙은 지켜졌다 —
연구가 모두 그린이 된 뒤에야 신중한 결정으로 집필이 열렸다.
- `tools/build_docs.py`는 `gates.writing_locked()`가 True인 동안 **무조건 거부**.
- 잠금 해제 3조건: ① `research_gate()` `all_green` ② `gates.write_research_complete()` ③ 루트 `PHASE`를 `writing`으로.
- **현재 세 조건 모두 충족(v0.4.0~)** → `writing_locked()` = `(False, "writing unlocked")`. 집필 사이트 빌드 완료
  (§6 규칙대로 **14장**[§11 가메트 · §12 배아 · §13 불임 · §14 성비 포함] 정본 HTML + 허브 + sitemap/robots/llms, **105/105** 준수, 바이트 결정론). 게이트는 빌드마다 다시
  평가되므로, 모듈이 회귀하면 빌드는 다시 거부한다(잠금은 의식이 아니라 메커니즘).

## 6. 집필 시 규칙 (VP-SPEC v1.8 — 전문은 루트 `VP_SPEC_v1_8.md`)
- **정본은 HTML**(C2). `docs/` 아래 HTML이 정본 ("html이 정본").
- **제목별 별도 HTML**(C4/6장): 섹션당 1페이지, answer-first(`<p class="answer">` 40–60단어), 자체완결, JSON-LD(ScholarlyArticle·BreadcrumbList), canonical, claim-strip(등급+재현링크+DOI), 인용 잠금량마다 vp-card.
- **본문 영어**(C0), 표·그림 포함. 모든 정량 결정론 재생성(C1, 2×sha256), 모든 `[O]`는 사유 명시(C3).
- 출력: `docs/<slug>/index.html` + `docs/index.html`(허브) + `_meta.json` + `sitemap.xml` + `robots.txt`(봇 허용) + `llms.txt`.

## 7. 사용자 반환 규약
- 종료 시 **압축파일 1개**만 반환(내부 경로 = 패키지 상대경로). 파편화 금지. 받은 자료에 추가/수정분 합쳐 단일 zip 반환(C0).

## 8. 인수인계 (자동)
새 창은 이 `START_HERE.md` → `CHARTER.md` 순서만 읽으면 범위·이음매·타깃·암·게이트·집필규칙을 모두 파악한다. 세션 간 상태는 파일로만 전달되며(이전 대화 기억에 의존 금지, VP-SPEC §1), 종료 시 단일 zip으로 다음 세션에 넘어간다.
