# HANDOVER — Reproductive / Gonadal-Endocrine (`reproductive_endocrine_vp_site`) · v0.7.1-writing

> 다음 세션이 **확인 없이 즉시** 이어받기 위한 문서. 이 zip을 새 창에 넣고 `python repro/run_all.py`만 돌리면 현재 상태가 전부 재현된다.
> 세션 언어 한국어, 기술 산출물 영어. 자기비하 금지, 정직 등급 유지.

---

## 1. 지금 상태 (한 문장)
v0.6.0까지 **배아(embryo)를 창발**(E1–E6)한 위에, v0.7.0에서 사용자의 두 질문에 **별개의 HTML 파트**로 답했다 — 왜 임신이 **실패**하는가(불임/난임)와 한 유전자가 어떻게 자손을 한 **성별**로 기울이는가(성별 쏠림). 새 `repro/_fertility/`(F1–F6)와 `repro/_sexratio/`(S1–S6) 두 모듈, 각각 같은 기질 위의 판별 배터리: **불임 = spinodal 너머의 연산**(범주적, 주기당 p=0, 미만 드라이브 무반응) vs **난임 = 문턱 근처의 연산**(유한 Kramers 율 — 같은 드라이브가 지수적으로 이동); 그리고 **성(性) = SOX9↔FOXL2 R19 양안정**(SRY 구동, 이력으로 평생 유지), 멘델 50:50 = 기울지 않은 스위치(공정한 동전), 감수분열 구동 = **기울임**(spinodal 너머 고정), 성비 왜곡 = **부호 있는** 기울임(X-shredder→수컷, Y-killer→암컷), 피셔 = 1:1 인구 끌개. 측정된 **성결정 마스터 프로모터 γ**(6유전자, 동일 DNA 파이프라인 수령)가 유일한 새 입력. 두 6-타깃 배터리 **F1–F6·S1–S6 전부 PASS**, 연구 게이트에 편입, 정본 HTML **§13·§14장**(새 식 10개)으로 집필됨. 해시 연구 코어는 **불변**(`f849da7d…`). **v0.7.1**에서 마지막 추적 항목을 종결했다 — 백서 PDF를 §13/§14로 확장(`build_paper.py`에 `sec_infertility`+`sec_sexratio`, 모든 수치 라이브)해 **12→15쪽**으로 재컴파일, HTML(C2)과 PDF를 동기화. 과학·해시·집필 게이트(105/105) 전부 불변.

## 1·1. v0.7.1이 한 일 (paper §13/§14 동기화 — distribution-layer 패치)
- **문제:** v0.7.0은 §13/§14를 정본 **HTML**(C2)로만 집필했고, PDF 백서는 v0.6.0 본문(gamete+embryo)에 머물러 있었다(추적된 열린 항목).
- **해결:** `tools/build_paper.py`에 두 라이브-수치 섹션 생성기 추가. `gather()`가 `infertility`·`sex_ratio` 배터리(+성결정 γ 아틀라스)를 빌드 dict에 편입 → PDF가 엔진과 어긋날 수 없음.
  - **`sec_infertility(D)`** — 8연산 chain-AND; 중심 spinodal/Kramers 해리 **표**(난임 0.0391→0.0610, **1.56×**, 연 0.381→0.530 / 불임 0/0/—); 남성=진동자 처리량(51→7 beats, CatSper γ 1.4019), 여성=서지 스위치+REC8 코헤신 피로(γ 1.4525, 오분리 0.121→0.752); 치료=드라이브(41 vs 0 박동).
  - **`sec_sexratio(D)`** — SOX9 1.4598↔FOXL2 1.4829 양안정+SRY 이력; 멘델 비기울임(2만 감수분열 0.4983); 구동=기울임 0.50→0.8623→1.0; **부호 있는** SSR(X-shredder 1.0/Y-killer 0.0/부분 0.8223); 피셔 1:1(0.5125 유계, 인간 0.512); γ 아틀라스 **표** + **정직 NULL**(축-분리 순열 p=0.10).
  - **`sec_open(D)`** +5행([O], 각 obstacle, C3): 절대 주기당 임신확률 · 연령별 이수성 분율 · 감수분열/성비 기울임 크기 · 인간 0.512 잔차의 원인 · n=3 축-분리 γ. open 표 12행.
  - abstract 다운스트림 호 1문장 + 키워드 확장 + **Fisher 1930** 참고문헌(`{9}`→`{10}`).
- **결과:** `.tex` **37,656→47,476자**, `\today` 미사용 → **2회 빌드 바이트 동일**(sha `3d5f5c64…`), 제목면 Version **0.7.1-writing**, 개념 DOI 불변. `.pdf` **클린 재컴파일**(`pdflatex`/`latexmk`, 미해결 참조 **0**), **12→15쪽**, A4. `docs/`는 **무수정**(사이트는 패키지 버전 문자열을 임베드하지 않음) — §11–§14장과 집필 게이트 105/105 그대로. 코어 해시 `f849da7d…` 불변, `run_all.py` ALL_GREEN.

## 1·2. v0.7.0이 한 일 (infertility/subfertility + sex determination/sex-ratio)
- **새 모듈 두 개** — `repro/_fertility/infertility.py`(F1–F6) + `repro/_sexratio/`(`fetch_sexratio_gamma.py` 측정 성결정 γ 수령 + `sex_ratio.py` S1–S6). 둘 다 vendored R19 스위치 + FHN 진동자만 사용, 결정론(SEED=19), 게이트 편입 시 코어 해시 불변.
- **측정 성결정 γ 아틀라스(↑):** SRY **1.2550**(AT-rich 이상치) · DMRT1 1.4423 · SOX9 1.4598 · RSPO1 1.4669 · FOXL2 1.4829 · WNT4 1.5992. 정소축 평균 1.3857 < 난소축 평균 1.5163. 패널은 **γ를 보기 전 축으로 선언**, SOX9·FOXL2 두 앵커 재현 시에만 저장, 오프라인 비트재현.
- **F1** 임신 = 8개 기질 연산의 **AND**; 한 게이트라도 0이면 임신 0(고리 하나 끊기면 불임) **[V]**.
- **F2 (중심 주장)** 불임 = spinodal **너머**(범주적, 주기당 p=0, 미만 드라이브로 안 움직임) / 난임 = 문턱 **근처**(유한 Kramers 율). 고정 nudge가 난임 주기확률을 0.039→0.061(**1.56×**, 연 0.38→0.53)로 올리지만, 같은 nudge가 불임(deficit 1.6·h_sp)은 **0 그대로** — 같은 드라이브, 지수적 vs 전무 **[V]**.
- **F3** 남성 인자 = 진동자 **처리량**: 무정자증 = R19 스위치 **OFF**(범주적); 정자 수/운동성 = 박동률(51→7 beats); CatSper(γ 1.4019) = 별도 supra-spinodal 게이트 **[V]**.
- **F4** 여성 인자 = 배란 서지 스위치 + **REC8 코헤신 피로**: 무배란 = 서지 OFF; 연령별 오분리(이수성) 확률이 **0.121→0.752**(나이 25→45)로 상승(붙잡힌 장벽 γ²/4·코헤신이 감쇠); POI = 조기 래치 상실 **[V]**(절대 분율은 [O], 상승 *형태*만 주장).
- **F5** 치료 = 기질 **이동**: hCG = supra-spinodal 킥; 박동성 GnRH 재시동(41 vs 0, §9 인용); ICSI/IVF = 게이트 우회 **[V]/[L]** 역행예측.
- **S1** 성 = **양안정** 스위치(SOX9↔FOXL2, h=0에서 동심), SRY = 일시적 supra-spinodal 플립 후 **유지**; 성체는 supra-spinodal에서만 전분화(FOXL2/DMRT1-KO) **[V]**.
- **S2** 멘델 50:50 = **기울지 않은** 분리 스위치(2만 감수분열 앙상블 0.4983, 해석 0.50) — 공정한 동전 **[V]**.
- **S3** 분리 왜곡 = **기울임**(점진 → supra-spinodal 고정): TR 0.50 → 0.86(미만) → **1.0**(초과; t-haplotype/SD 한계) **[V]**.
- **S4** 성비 왜곡 = **부호 있는** 성염색체 가메트-킬러: X-shredder SSR **1.0**(수컷), Y-killer **0.0**(암컷), 약한 구동 0.82(부분) — 한 메커니즘, 두 부호 **[V]**.
- **S5** 피셔: 인구 성비 1:1 = **안정 끌개**(0.20/0.80에서 0.50 복귀; 약한 지속 구동도 0.5125까지만; 인간 SSR ~0.512 = 작은 잔차) **[V]**.
- **S6** γ 아틀라스 + **사전등록** 축-분리 검정: 난소축이 높게 트렌드(1.5163 vs 1.3857)지만 SRY 강한 이상치 + 축당 n=3 → 순열검정 **p=0.10, 비유의 — NULL 정직 보고**; 챕터의 검증된 주장은 이에 의존하지 않음 **[V on the test]**.
- **배선:** `stress_tests.py`(F1–F6·S1–S6를 `all_targets_pass`에 편입(29 suites) + `fertility_all_pass`/`sexratio_all_pass`), `gates.py`(`fertility_pass`/`sexratio_pass` 노출), `run_all.py` §[3]에 두 배터리 + 성결정 γ 아틀라스. 상수는 한 번만 설정, 절대 타깃에 적합 안 함.
- **집필:** HTML **§13 `13-infertility-and-subfertility`** + **§14 `14-sex-determination-and-sex-ratio-distortion`** + 허브 헤드라인 2개 + 식 10개(`rep-inf-001..005`, `rep-sxr-001..005`) → **14장 · 10078단어 · 식 28개**, writing-gate **105/105**, 2회 빌드 바이트 동일, `llms.txt` 14장용 재작성(<5 KB). **PDF는 §13/§14 미반영 — 추적 중인 열린 항목**(HTML이 정본 C2, PDF 재생성은 다음 세션).

## 1·3. v0.6.0이 한 일 (the embryo — fertilisation → fetus)
- **새 모듈 `repro/_embryo/`** — `fetch_embryo_gamma.py`(측정 발생 γ 수령: 동일 NN-stacking ΔG37 파이프라인, 17유전자; 단계/HOX로 γ 보기 전 선언; SOX9·DAZL 두 앵커 재현 시에만 저장; 오프라인 비트재현) + `embryogenesis.py`(E1–E6 배터리, 결정론 `bdf77110…`).
- **측정 발생 γ 아틀라스(↑):** NANOG 1.3479 · SOX17 1.3821 · GATA4 1.3933 · HOXB4 1.4453 · PAX3 1.4479 · CDX2 1.4500 · SOX2 1.4576 · SOX9 1.4598 · PDX1 1.4732 · POU5F1 1.4874 · HOXA1 1.4923 · MYOD1 1.4937 · FOXA2 1.4986 · PAX6 1.5110 · NKX2-5 1.5130 · TBXT 1.5130 · HOXA13 1.5427. **단계 평균 상승**(사전등록): 다능성 1.4310 < 배엽 1.4373 < 기관 1.4916.
- **E1** syngamy + DNA 창발 — 정자(진동자)가 난자(붙잡힌 스위치)를 supra-spinodal 일방 플립(미만은 안 넘어감, 다정자 차단 유지); 두 반수체 전핵 융합 → 2N,2C(→2N,4C after S); 새 게놈 **10⁹⁴** floor 고유(가메트 10⁴⁷ 제곱) **[V]**.
- **E2** cleavage — 2ⁿ **대칭** 분열(1→2→4→…→64; 난자형성 1+3과 대비), 세포질 질량 **보존**(난할 ≠ 성장, 각 할구 1/2ⁿ); ICM/TE = R19 양안정 스위치 **[V]**.
- **E3** ZGA — 모체→접합체 전이 = **1단계 spinodal 교차**(모체 저장 ZAR1 1.4226/NLRP5 1.3475/MOS 1.3619에서 OFF → 점프 1.6551 @ drive 0.3913 ≈ spinodal 0.3849 ON); 가메트 프로그램→배아 자체 게놈 인계 **[V]**.
- **E4** 유전자시계 = argsort(spinodal(γ)) = γ 오름차순; **사전등록 단계검정 ρ=0.5507, p=0.0200 → 지지**(γ가 발생단계 추적); HOX 3′→5′ 공선성 ρ=0.50, p=0.50 → 최후방(HOXA13) 최고 γ, 부분 결과 정직 보고; **방화벽**: 유전자시계 법칙 + 전신 아틀라스 = DNA 4D-Blueprint SSOT(인용, 미소유) **[V on the demonstration]**.
- **E5** 전체 호 — 특정 정자+난자(결정론 draw) → syngamy→cleavage→ZGA→body plan → 태아(고유 게놈 10⁹⁴, 17 구조, ICM 유래); arc 전부 PASS **[V]**.
- **E6** 정직 스코어보드 + 방화벽 재천명; [O] 절대 임신 시점(사춘기 연령처럼) + 전신 아틀라스(DNA SSOT).
- **배선:** `stress_tests.py`(E1–E6를 `all_targets_pass`에 편입 + `embryo_all_pass`), `gates.py`(`embryo_pass` 노출), `run_all.py` §[3]에 배아 타깃 + 발생 γ 아틀라스. **`inherited/embryo_identity.md`** 이음매 노트 추가.
- **집필:** HTML **§12 `12-embryogenesis-fertilisation-to-fetus`** + 인덱스 헤드라인 + 식 5개(`rep-emb-001..005`) → **12장 · 7939단어 · 식 18개**, writing-gate **91/91**, 2회 빌드 바이트 동일. PDF는 `sec_embryo` 추가로 **10→12쪽**, `.tex` 바이트 동일.

## 1·4. v0.5.0이 한 일 (the gamete itself — germline)
- **새 모듈 `repro/_germline/`** — `fetch_germline_gamma.py`(측정 γ 수령: 동일 NN-stacking ΔG37 / SantaLucia 1998 / promoter TSS−2000..+500 / GRCh38.p14; 온라인 좌표해석은 NCBI datasets v2, 평시는 캐시 오프라인 재현) + `gametogenesis.py`(G1–G6 배터리). 패널은 **γ를 보기 전에 기능으로 선언**(체리피킹 없음); SOX9·DAZL 두 앵커가 재현되지 않으면 저장 거부.
- **측정 γ 아틀라스(↑):** TEKT1 1.3400 · NLRP5 1.3475 · MOS 1.3619 · DAZL 1.3803 · CATSPER1 1.4019 · DMC1 1.4056 · MLH1 1.4085 · SPO11 1.4105 · PRDM9 1.4165 · ZAR1 1.4226 · DNAH1 1.4469 · ZP3 1.4486 · REC8 1.4525. 재조합 코어(SPO11/DMC1/MLH1/PRDM9)는 ≈1.406–1.417로 조밀.
- **G1** 감수분열 = 1복제 + **2분열**(환원→균등), REC8 2단계 코헤신(arm separase 0.684 → centromeric 1.085; shugoshin 보호의 *부호*가 순서를 강제, 튜닝 아님) **[V]**.
- **G2** 생식세포는 **동일하지 않다**: 독립분리 정확히 2²³=8,388,608 + 교차 **간섭 = 기질의 불응기**를 염색체축에 사상(Fano 0.108 vs Poisson 0.976, gap CV 0.26, obligate CO) → 구별가능 floor 10⁴⁷ **[V]**.
- **G3** 정자 편모 = **가장 빠른** 이완진동자(4-클럭 사다리 26.2<132.45<674.95<1133.65); 과활성화 = CatSper 이득 상승으로 진폭↑(2.21→2.83) **그리고** 박동↓(77→57) **[V]**; 9+2 축사의 정수 9는 **[O]**(역적합 아님, 미유도 선언).
- **G4** 난자 = 중기-II에 **붙잡힌 스위치**(−1.088); 수정 = spinodal(0.3849) 초과 일방 플립(미만은 안 넘어감); 다정자 차단 = past-spinodal 비가역 **[V]**.
- **G5** γ 아틀라스 + **사전등록** 모듈-분리 검정: 순열검정 **NULL**(F 0.109, p 0.617) 정직 보고; 양성 하위검정 = 재조합 코어 조밀 클러스터(CV 0.0028 vs 패널 0.0253, p 0.0014) → 좁은 주장만 **[V]**.
- **G6** 정자/난자 **이중성**(자유진동자 vs 붙잡힌 스위치); 대칭 4 정자 vs 비대칭 1 난자+3 극체; anisogamy(난자:극체 49×, 난자:정자 부피 ~18,963×) **[V]/[L]**; 진화적 '왜'는 **[O]**.
- **배선:** `stress_tests.py`(G1–G6를 `all_targets_pass`에 편입 + `germline_all_pass`), `gates.py`(`germline_pass` 노출), `run_all.py` §[3]에 가메트 타깃 + γ 아틀라스. **`inherited/germline_identity.md`** 이음매 노트 추가.
- **집필:** HTML **§11 `11-gametogenesis-the-gamete-itself`** + 인덱스 헤드라인 + 식 5개(`rep-gmt-001..005`) → **11장 · 6417단어 · 식 13개**, writing-gate **84/84**, 2회 빌드 바이트 동일. PDF는 `sec_gamete` 추가로 **9→10쪽**, `.tex` 바이트 동일.

## 1·5. v0.4.1이 한 일 (Zenodo 배포 준비)
- **DOI 확정**: `pending` → **개념 DOI `10.5281/zenodo.20754657`**(버전 독립, 항상 최신 버전으로 해석 → 인용에 쓰는 정식 식별자). claim-strip·footer·`_meta.json`(`type:"concept"`)·`llms.txt`·논문 제목면·참고문헌에 클릭 가능한 링크로 반영. `docs/`에 `pending` 문자열 전무. 버전별 DOI는 패키지 식별자로 쓰지 않음.
- **`tools/build_paper.py` 신설**: 같은 모듈을 import해 모든 수치를 빌드시 라이브 추출 → PDF가 엔진과 어긋날 수 없음. `\today` 미사용(제목면에 고정 버전+DOI) → `.tex` 런 간 **바이트 동일**.
- **`paper/` 2파일**: `reproductive_endocrine_vp.tex`(~28.5 KB) + `reproductive_endocrine_vp.pdf`(9쪽, A4, 컬러 등급 배지, DOI/ORCID 링크, 9개 참고문헌; `pdflatex` clean, 미해결 참조 0).

## 1·6. v0.4.0이 한 일 (writing)
- **`tools/build_docs.py` 구현**: VP-SPEC v1.8 §6 준수 제목별 생성기. `writing_locked()`가 True면 거부; 풀리면 10장 + 허브 + 사이트 아티팩트 빌드.
- **`docs/` 24파일**: 허브 1 + 챕터 10(`<slug>/index.html`) + 식 SVG 8(`eq/*.svg`) + `_meta.json` + `sitemap.xml` + `robots.txt`(7봇) + `llms.txt`(<5 KB) + `assets/css/site.css`; 챕터 매니페스트 CSV.
- 페이지마다 answer-first(40–60단어) · abstract · claim-strip · 인용 잠금량별 vp-card · JSON-LD ×2 · canonical · 외부 CSS · prev/next. 식 SVG는 고정 hashsalt + Date 억제 → 바이트 안정. 자체검사 `reports/writing_gate.json` **77/77**, `docs/` 2회 빌드 바이트 동일.

## 2. 즉시 실행 → 기대 출력
```bash
python repro/run_all.py
```
- [1] organ emergence: **4/4 측정 γ** — germline(DAZL 1.3803) · gonad_testis(SOX9 1.4598) · gonad_ovary(FOXL2 1.4829) · reproductive_tract(WT1 1.5182); 발생순서(γ↑) germline→testis→ovary→tract; **미측정 보류 없음**
- [2] oscillator: `gonad_ovary` oscillates, 7 beats (FHN γ=1; rhythm은 τ 의존)
- [3] **T1–T5 + G1–G6 + E1–E6 + F1–F6 + S1–S6 all PASS** (가메트·배아·불임·성비 배터리 포함, 29 suites); 가메트·발생·성결정 γ 아틀라스 출력; `germline … True`, `embryo … True`, `fertility (infertility/subfertility) all pass: True`, `sexratio (determination + distortion) all pass: True`
- [4] oncology **PASS** (γ-independence max spread 0.0; breast monotone; prostate concave+plateau; cervical mult-low/saturating-high)
- [5] therapy **PASS** (BAT cycling resistant fold 13.6×; GnRH 41 vs 0)
- [6] disease **PASS** (8 disorders)
- [7] research gate **ALL_GREEN: True** (`emergence=stress=germline=embryo=fertility=sexratio=oncology=therapy=disease=True`); **WRITING: UNLOCKED** (`PHASE == writing`)

```bash
python repro/_germline/gametogenesis.py    # 가메트 배터리 단독 → G1–G6 전부 PASS
python repro/_fertility/infertility.py     # 불임/난임 배터리 단독 → F1–F6 전부 PASS
python repro/_sexratio/sex_ratio.py        # 성비 배터리 단독 → S1–S6 전부 PASS
```

```bash
python tools/build_docs.py     # 집필: docs/ 정본 사이트 재생성 (멱등 — 2회 빌드 바이트 동일)
```
- rendered **28** display equations → `docs/eq` · pages: **14** · words: **10078** · display eqs: **28**
- hub + `_meta.json` + `sitemap.xml`(15) + `robots.txt`(7봇) + `llms.txt`(<5 KB) + `site.css` + manifest CSV
- writing-gate **105 / 105 → ALL PASS** (`reports/writing_gate.json`); `docs/` 2회 빌드 바이트 동일

```bash
python tools/build_paper.py                                              # 배포: paper/…tex 재생성 (라이브 수치, \today 미사용 → 바이트 동일)
cd paper && latexmk -pdf -interaction=nonstopmode reproductive_endocrine_vp.tex   # → …pdf (15쪽, pdflatex clean, 미해결 참조 0)
```
- `paper/reproductive_endocrine_vp.tex`(~47.5 KB) + `paper/reproductive_endocrine_vp.pdf`(15쪽, A4). 개념 DOI `10.5281/zenodo.20754657` 제목면·참고문헌에 링크. **PDF는 이제 §11–§14 전부 반영(v0.7.1) — `sec_infertility`/`sec_sexratio` 포함, HTML(C2)의 충실한 무드리프트 미러.** `.tex` 2회 빌드 바이트 동일(sha `3d5f5c64…`).

deterministic core sha256 = `f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4` (2× identical, byte-identical, process-stable).
γ 오프라인 재현 확인: `python repro/_gamma/fetch_gamma.py` → `ok: true` (캐시에서 γ 재계산 + SOX9 앵커 1.4598/0.545 교차검증, 네트워크 불필요).
- 집필 단계 변경은 **얼어붙은 과학 위에 얹힌 것**: 해시 코어(`f849da7d…`)는 v0.3.0과 **동일** — writing은 과학을 읽기만 하고 바꾸지 않는다.

## 3. 절대 건드리지 말 것
- `inherited/vp_substrate.py` — vendored, 수정 금지. 프리미티브만 사용.
- `inherited/organ_promoters.cache.json` — **프로모터 서열의 SSOT**. 4개 유전자(FOXL2/DAZL/WT1/SOX9) 각각 2501 bp 프로모터 서열 + accession/strand/TSS/window/GC/γ/seq_sha256 동봉. γ는 이 캐시에서 **오프라인 비트재현**(네트워크 불필요). NCBI 재조회는 캐시를 새로 빌드할 때만 — `python repro/_gamma/fetch_gamma.py --fetch`. 평시 검증은 `--fetch` 없이(오프라인 기본) `ok: true` 확인.
- `inherited/germline_promoters.cache.json` — **가메트 프로그램 13유전자 프로모터 서열의 SSOT**(v0.5.0 추가). 동일 규약(2501 bp + γ + seq_sha256), 오프라인 비트재현. 재조회는 `python repro/_germline/fetch_germline_gamma.py --fetch`(SOX9·DAZL 두 앵커 재현 시에만 저장). 평시는 `--fetch` 없이 `ok: true` 확인. **γ는 측정 입력이며 절대 손으로 고치지 않는다.**
- `inherited/sexdet_promoters.cache.json` + `sexdet_gamma.json` — **성결정 6유전자 프로모터 서열의 SSOT**(v0.7.0 추가; SRY/SOX9/DMRT1/FOXL2/RSPO1/WNT4). 동일 규약(γ + seq_sha256), 오프라인 비트재현. 재조회는 `python repro/_sexratio/fetch_sexratio_gamma.py --fetch`(SOX9·FOXL2 두 앵커 재현 시에만 저장). 평시는 `--fetch` 없이 `ok: true`. **성결정 γ도 측정 입력, 손대지 않는다.**
- 핵심 주의: 속성은 `self.g`(≠`self.gamma`); `E`/`I`는 `run()` 인자. γ=1, β=0.5, E=I=1 FHN은 **모든** bias에서 자율 한계순환 — 유일한 침묵 레버는 drive ≳ 2×spinodal 탈분극 차단. (그래서 FHA=저**주파수**, 폐경=latch 상실로 모델링; "저드라이브 침묵"·"진폭 감쇠"는 기질 비충실로 **폐기됨**.)
- **무튜닝:** τ_s는 주기를 정하지만 주기는 [L] 앵커 — 임상 타이밍을 *유도한다고 주장하지 않음*. NOISE_D/per_year/κ/amp는 명시 입력, 절대 타깃에 맞춰 적합하지 않음.

## 4. 다음에 할 수 있는 일 (우선순위)
0. ~~**γ 수령**~~ — **완료(v0.3.0)**. ~~**집필 단계 진입**~~ — **완료(v0.4.0)**. ~~**Zenodo 배포 준비**~~ — **완료(v0.4.1)**. ~~**생식세포(germline) — G1–G6 + §11장**~~ — **완료(v0.5.0)**. ~~**배아(embryo) — E1–E6 + 발생 γ + §12장**~~ — **완료(v0.6.0)**. ~~**불임/난임 + 성결정/성비 — F1–F6·S1–S6 + 성결정 γ + §13·§14장**~~ — **완료(v0.7.0)**: 두 6-타깃 배터리 전부 PASS, 연구 게이트 편입(29 suites), HTML 14장/105-105, 성결정 γ 6유전자. 코어 해시 불변. (위 §1·2 참조.) ~~**남은 추적 항목: `build_paper.py`를 §13/§14로 확장 후 PDF 재컴파일**~~ — **완료(v0.7.1)**: `sec_infertility`+`sec_sexratio`(라이브 수치), open 표 +5행, Fisher 참고문헌; PDF 12→15쪽 클린 재컴파일, `.tex` 바이트 동일, HTML(C2)과 동기화. (위 §1·1 참조.)
1. **다음 신중한 단계 — 실제 Zenodo 업로드.** 3파일(`paper/reproductive_endocrine_vp.tex` · `paper/reproductive_endocrine_vp.pdf` · 재현성 zip)을 **개념 DOI `10.5281/zenodo.20754657`** 아래 업로드. 개념 DOI는 버전 독립이며 이미 모든 산출물에 박혀 있어 Publish 시 DOI 교체가 필요 없다. 적립을 다시 키링(re-key)할 경우에만 `build_docs.py`/`build_paper.py`의 `DOI` 상수 1곳씩 바꾸고 재빌드(사이트+논문 자동 추종). **DOI는 절대 임의로 만들지 않음(C1/C3).**
2. **확장 후보(선택, 연구 규율 그대로):** 더 많은 발암물질 앵커, 자궁내막증 진행 동역학, pulsed-TRT 스케줄 스윕. 이들은 **연구 게이트**로 재진입(집필 게이트 아님). 새 과학이 코어에 들어가면 코어 해시는 정당하게 바뀐다.
3. **재빌드 시 주의:** 챕터·논문 본문 숫자를 손으로 고치지 말 것 — 전부 모듈에서 라이브로 온다. 과학을 바꾸려면 모듈을 고치고 게이트를 다시 통과시킨 뒤 `build_docs.py`/`build_paper.py`를 재실행하면 사이트와 PDF가 따라온다.

## 5. 4-문서 SSOT 위치
`CHANGELOG.md`(이번 증가 내역) · `MASTER_MANUAL.md`(운영·잠긴 물리·재현 규약) · `COMPLETION_LEDGER.md`(완료/등급/열린 항목) · `HANDOVER.md`(이 문서). 모든 버전 증가마다 4개 동시 갱신.

## 6. 사용자 규약 (기억)
- 한국어 세션, 영어 산출물. **확인 일시정지 없이 직접 실행**, 압축 트랜스크립트에서 즉시 재개, 임베디드 핸드오버 자율 정독.
- 종료 시 **단일 zip 1개**만 반환(내부 경로 = 패키지 상대), 파편화 금지, present_files + 간단한 한국어 결과 요약.
- 등급 어휘 [O]/[L]/[V]/[F]는 정직성 — 자기비하 어조와 구별해서 유지.

## 7. 한 줄 인계
**v0.7.1: 백서 PDF를 §13/§14로 확장해 추적 항목 종결 — `build_paper.py`에 `sec_infertility`+`sec_sexratio`(모든 수치 라이브), PDF 12→15쪽 클린 재컴파일, HTML(C2)과 동기화, 과학·해시(`f849da7d…`)·집필 게이트(105/105) 전부 불변.** (그 아래 과학은 v0.7.0: 불임/난임 + 성결정/성비를 F1–F6·S1–S6 판별로 답함, 측정 성결정 γ 6유전자 아틀라스.) 핵심 발견: **불임과 난임은 슬라이더가 아니라 spinodal 하나를 사이에 둔 두 쪽**(범주적 p=0 vs 유한 Kramers 율 — 같은 드라이브가 전무 vs 지수적)이고, **성(性)은 기울일 수 있는 동전**(멘델 = 기울지 않은 SOX9↔FOXL2 스위치, 감수분열 구동 = 기울임, 성염색체 구동 = 부호 있는 성비 왜곡, 피셔 = 1:1 끌개). 정직한 NULL 하나 동봉(S6 축-분리 p=0.10). **이제 PDF·HTML이 §11–§14 전부 일치한다.** 다음 손이 할 일은 (a) 실제 **Zenodo 업로드**(3파일: `.tex`·`.pdf`·재현성 zip; 개념 DOI `10.5281/zenodo.20754657` 이미 반영, Publish 시 DOI 교체 불필요), 또는 (b) 선택적 연구 확장(더 많은 발암물질 앵커·자궁내막증 동역학·pulsed-TRT 스윕 — 연구 게이트 재진입, 새 과학이 코어에 들어가면 해시는 정당하게 바뀜). 모두 무튜닝·결정론·정직 등급을 그대로 따른다. 임상 조언 아님.
