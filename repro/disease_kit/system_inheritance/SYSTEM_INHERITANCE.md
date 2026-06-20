# SYSTEM-INHERITANCE — 다(多)시스템 난치병을 위한 장기-시스템 상속 계층 (ROADMAP V)

**대상 패키지:** `vp_disease_emergence_kit` (개념 DOI 10.5281/zenodo.20755262 · 희귀병 · CC BY 4.0 · ORCID 0009-0002-7535-8245)
**상속 원천:** VP body 형제 패키지 13종 (장기-master γ) + 2 compartment anchor (neuro / dna)
**governance:** VP-SPEC v1.8 지배. Constitution C3(정직한 hold) · C4(retrieval-readiness)와 정합.

이 문서는 사용자 지시 *"여러 시스템에서 상속받아 필요한 상속 시스템으로 난치병을 더 해석하고 치료 방향을
제시하라 — 단, 각 분야가 이미 다룬 주요질환을 제외한 난치병으로 한정하라"* 에 대한 설계 응답이다.

---

## 0. 한 문장 — 왜 필요한가

> **구조를 모르면서 희귀병을 다루기는 어렵다.** 단일 원인유전자 병변(난치병)은 *여러 장기 시스템에 동시에*
> 발현한다. 이 kit 은 이미 그 *하나의* 원인유전자 프로모터를 읽어 스위치 perturbation 과 교정 *방향*을
> 도출한다 — 그러나 그 병변이 닿는 *각 장기 시스템의 구조*까지는 알지 못한다. 그 구조는 VP body 형제
> 패키지들이 **측정·소유·동결**해 둔 자산이다. 본 계층은 그 구조(실측 organ-master γ)를 **읽기 전용으로
> 상속**하고, lead 교정 lever 가 *어느 compartment 에 닿고(REACH) 어느 곳을 빈틈으로 남기는가(GAP)*를
> 구조적으로 드러낸다. **각 GAP 이 곧 다음, 비자명한 치료 방향이다.**

---

## 1. 핵심 불변식 (analgesic 상속에서 검증된 그 방법 그대로)

| | 원칙 | 구현 |
|---|---|---|
| **읽기 전용** | 신규 계층은 형제의 *동결된* 산출물과 본 kit 의 *동결된* per-disease `analysis.json` 을 **읽기만** 한다. | `system_inheritance.py` 는 어떤 형제 코드도 import 하지 않고, 어떤 `analysis.json` 도 수정하지 않는다. |
| **자체 freeze** | 신규 계층은 **자체 별도 freeze** 를 가진다. | `repro/expected_system_inheritance_sha256.json` (1 hash). per-disease(78) · module(6) · site(4) freeze 는 **불변**. |
| **γ 비재계산** | organ-master γ 는 형제 패키지에서 *측정*된 값을 **그대로 인용**한다(no-tuning). | `sibling_registry.json` 은 vendored snapshot — γ 를 다시 계산하지 않는다(SantaLucia 1998 NN-stacking dG, 공유 substrate). |
| **방향-only firewall** | STRUCTURE(어느 장기) + DIRECTION(어느 compartment 에 닿는가)만. 크기는 항상 `[O]`. | compartment reach 는 *인용된 정성 biodistribution* (닿는가/안 닿는가). 교정의 *정도*는 `[O]`. magnitude 스캔이 dose/efficacy/rate/p-value 차단. |
| **§6 ownership** | gene-defined → 이 kit; dynamics-defined → 형제. 형제의 *주요질환* 제외. | exclusion gate 가 모든 manifest 질병을 형제의 `owned_major_disease_EXCLUDED` 목록과 대조해 fail-closed. |

> 이것이 본 kit 에서 78개 per-disease 해시를 v0.19.0 이후 drift 0 으로 유지해 온 바로 그 방법이다. 신규
> 계층도 동일하게 *읽기만 하고, 자기 것만 동결한다.*

---

## 2. 3-파트 구조

### 2.1 registry — `sibling_registry.json` (vendored, read-only)
`build_sibling_registry.py` 가 생성. 13 형제의 **49 organ-master 유전자 + 실측 γ**, 2 compartment anchor,
그리고 §6 ownership contract(형제별 제외 주요질환)를 담는다. 예시 γ (형제 frozen report 에서 그대로 인용):

| 형제 | organ-master | gene | γ (측정) |
|---|---|---|---|
| cardioresp | heart / lung | NKX2-5 / NKX2-1 | 1.513 / 1.5088 |
| circulatory | kidney / liver | SIX2 / HHEX | 1.5556 / 1.525 |
| digestive | pancreas / intestine | PDX1 / CDX2 | 1.4732 / 1.45 |
| musculoskeletal | skeletal_muscle / limb | MYOD1 / TBX5 | 1.4933 / 1.4392 |
| thermometabolic | melanocortin_appetite | MC4R | 1.272 |
| sensory | eye_retina_optics | PAX6 | 1.511 |
| reproductive | reproductive_tract / gonad_testis | WT1 / SOX9 | 1.5182 / 1.4598 |

(neuro = cns/pns compartment anchor — γ 공여 없음; 신경계 질병은 kit 이 *자기* 원인유전자 γ 를 읽는다.
dna = organ-identity SSOT.)

### 2.2 manifest — `multisystem_manifest.json`
이미 RESOLVED 인 **8개 다시스템 난치병**에 대해, 단일 병변이 발현하는 **필요한** 장기 시스템 부분집합과
각 발현의 인용, 그리고 *biodistribution 을 읽을* lead modality 를 선언한다. (DEMONSTRATION set — 나머지는
이후 버전에서 roll out: kit 의 표준 "보여준 뒤 확장" 패턴.)

### 2.3 module — `pipeline/system_inheritance.py` [NATIVE, fail-closed]
disease 마다:

1. **provenance handshake (fail-closed)** — ① `analysis.json` 이 RESOLVED (suspension rule 준수; SUSPENDED
   질병은 *읽히는 단일유전자 프로모터가 없으므로* 여기서 처리되지 않는다) ② manifest `causal_gene` ==
   frozen `emergence.primary_switch.gene` (gene handshake) ③ manifest lever == frozen lead lever ④ manifest
   `lead_modality_signature` ⊂ frozen `agent_class` (즉 우리가 biodistribution 을 읽는 그 약물이 kit 이 이미
   강제한 바로 그 agent 와 동일).
2. **γ 해소** — 각 affected 시스템을 registry 의 *실측* organ-master γ 로 해소(또는 선언된 neural anchor).
   해소 실패 → fail closed.
3. **REACH 분류** — compartment → reach-class(systemic_perfused / neural / cornea / retina / satiety);
   modality → 닿는 class 집합(인용된 정성 biodistribution). **REACHED iff class(compartment) ∈
   reaches(modality), 아니면 GAP.**
4. **다음 방향** — 각 GAP compartment 를 다음 치료 방향으로 표면화([F] 방향 / [O] 크기).

---

## 3. v0.30.0 census (8 질병 · 실측 결과)

```
diseases=8  inherited_links=31  γ-systems=27  reached=26  gap(next-direction)=5
```

| 질병 | gene | lead modality | REACH | GAP = 다음 방향 |
|---|---|---|---|---|
| Fabry | GLA | enzyme_replacement_iv | 혈관내피·신·심 | **PNS 소섬유**(BBB — 효소가 신경계 미도달) |
| Pompe | GAA | enzyme_replacement_iv | 골격근·심·호흡근 | — (열거 시스템 모두 perfused) |
| cystic_fibrosis | CFTR | cftr_modulator_oral | 호흡·췌·장·간·생식관 | — *caveat: genotype_limited* (responsive allele 만) |
| cystinosis | CTNS | small_molecule_substrate_depleter | 신 | **무혈관 cornea**(topical 별도 필요) |
| tuberous_sclerosis | TSC2 | mtor_inhibitor_systemic | CNS(SEGA)·신·피부·심·폐 | — (rapalogue 가 CNS SEGA 도달) |
| Bardet-Biedl | BBS1 | melanocortin4_agonist | 시상하부 satiety | **retina · 신 · limb**(agonist 가 satiety node 만 — kit 최대 다-compartment 빈틈) |
| Wilson | ATP7B | metal_chelator_systemic | 간·CNS·cornea (모두) | — *대조 사례* |
| haemochromatosis-1 | HFE | therapeutic_phlebotomy | 간·췌·심·관절·생식선 (모두) | — *대조 사례* |

**해석의 균형:** Wilson(chelator 가 간·뇌·각막 구리 모두 mobilise)과 haemochromatosis(phlebotomy 가
혈장 평형으로 전 실질 iron pool 도달)는 *대조 사례*다 — reach 읽기가 막연한 비관이 아니라 **modality 별
구조적 사실**임을 증명한다. Bardet-Biedl 의 3-compartment 빈틈(망막·신·사지)은 가장 선명한 미충족 방향이다.

---

## 4. §6 — 무엇을 제외하는가 (난치병으로 한정)

exclusion gate(`system_inheritance.py`)는 VP_FRAMEWORK_MAP §6.1 을 강제한다:

- **이 kit 소유:** gene-defined / 단일유전자 / 다시스템 / 난치(難治) monogenic 질병. (8 질병 전부 causal_gene
  보유 — positively 확인.)
- **제외 (형제 소유):** dynamics-defined / common / acquired 주요질환 — 암, 제2형 당뇨, 본태성 고혈압,
  일반 골다공증, 후천 감각질환. 이들은 machine/homeostasis/time 형제(dynamics-key)가 소유한다.
- **gate 동작:** 모든 manifest 질병명을 형제의 `owned_major_disease_EXCLUDED` 목록과 정규화 token 대조 →
  충돌 시 fail. (현재 충돌 0; 향후 실수도 잡는다.)

---

## 5. drift 안전장치 (요약)

| freeze | 내용 | v0.30.0 상태 |
|---|---|---|
| `expected_sha256.json` | 78 per-disease analysis.json | **drift 0 (불변)** |
| `expected_modules_sha256.json` | 6 module 출력 | **drift 0 (불변)** |
| `expected_site_sha256.json` | 4 site 파일 | v0.30.0 재동결(버전 문자열만 변경) |
| `expected_system_inheritance_sha256.json` | **신규** 1 hash (system_inheritance_map.json) | INIT → drift 0 |

`run_all.py` 에 **S6** 추가(5 → 6 stage). S6 은 모듈 자체의 byte-identical rebuild + provenance/firewall/
exclusion teeth + negative teeth(틀린 signature·틀린 gene·주입된 주요질환·reach 분류 spot-check)를 돌리고,
cross-run drift guard 를 더한다.

---

## 6. 확장 절차 (다음 다시스템 난치병 추가 시)

1. 대상 질병이 kit 에서 **RESOLVED** 인지 확인(아니면 먼저 RESOLVED 시키거나 hold — suspension rule).
2. `multisystem_manifest.json` 에 항목 추가: `causal_gene`(= frozen primary_switch.gene), `lead_lever_frozen`,
   `lead_modality`(+ `lead_modality_signature` = frozen agent_class 의 부분문자열), `inherited_systems`
   (각 (sibling, organ) 은 registry 에 해소 가능해야 함), `falsifier`.
3. 필요 시 `MODALITY_REACH` / `COMPARTMENT_CLASS` 에 *인용된* 항목 추가(reach 는 교과서적 biodistribution
   만 — ERT/mAb 가 BBB 미통과 같은, 혹은 질병 자신의 frozen `analysis.json` 에 이미 있는 사실만 단정).
4. `python3 pipeline/system_inheritance.py` → teeth PASS 확인 → `--write` 로 재동결 → `run_all.py` 2회로
   drift 0 확인.

---

*Direction-only. 같은 axis ≠ 같은 질병. 진단·치료·완치가 아니며 개인 의료 자문이 아니다.
Orphanet · NORD · GeneReviews · ClinicalTrials.gov 및 담당 의사를 참조하라.*
