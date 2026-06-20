# INTEGRATED ROADMAP — The Immune Volume as a Cross-Package Hub

> **통합 로드뷰 (re-designed in v0.16.0; spokes 3→5 in v0.17.0; +2 barrier-surface candidates in v0.18.0; v0.19.0 근골격 + v0.20.0 피부 라이브-검증).** 이 문서는 면역 패키지의 로드맵을 **"안에서 밖으로"** 다시 설계한 것이다. v0.19.0은 근골격 볼륨(v0.7.0)에 대해 골수-니치 포인터를 라이브-검증(drift 0)하고 정체성 후보를 정직하게 폐기(RUNX2≠RUNX1)했고(§20), **v0.20.0은 피부 볼륨(integumentary_vp_site v1.0.0)에 대해 표피 장벽 SEAM을 라이브 기질-검증(drift 0)하고 상호 면역-SEAM 핸드셰이크를 확인**했으며, 표피-관용 정체성은 면역-소유 닫힌형으로 유지(실재 표면 확인·반박 없음·엔진검증 아님)된다(§21) — 세 형제 볼륨, 세 결과: gut=검증된 정체성, 근골격=폐기된 정체성, 피부=인접성-검증+상호 핸드셰이크.
> 패키지내 타깃(T6–T35)은 소진됐다 — 이제 면역계를 **다른 VP 볼륨들이 물리적으로 만나는 허브**로 보고,
> 그 허브가 어떤 SEAM(이음매)으로 자라는지를 지도화한다. v0.16.0이 세 SEAM(장·신경·종양)을 결선했고, **v0.17.0이 상속된 인접성
> 둘(circulatory 백혈구 트래피킹·musculoskeletal 골수 니치)을 선언된 일방향-포인터 SEAM으로 승격**해 허브가 **5 스포크**가 됐다. v0.18.0은 장벽-표면 agnosticism으로 호흡·피부 2개 명명 후보를 추가했고, **v0.19.0은 근골격 볼륨(v0.7.0)에 대해 골수-니치 포인터를 라이브-검증(drift 0)하고 정체성 후보를 정직하게 폐기(RUNX2≠RUNX1)**했다(§20).
> 모든 SEAM은 **byte-동일 R19 기질** 위에 있고, **게이트 패키지는 형제 코드를 0개 import** 하며, 엔진 결정론 해시 `e7a2a5b8…`는 **byte-동일로 보존**된다.
> 함께 읽기: `START_HERE.md`(현 상태) · `FUTURE_WORK.md`(전방 계획) · `IRREPRODUCIBILITY_LEDGER.md`(열린 [O] 목록).

---

## 1. The reframe — from intra-package targets to a cross-package hub

For fifteen versions this volume grew **inward**: each release added a stress target (T6 … T35) that read one more
behaviour out of the same R19 substrate — clonal selection, inflammation, lineage order, memory, surveillance,
carcinogenesis, the four therapy levers, central and peripheral tolerance, exhaustion, the disease/treatment axis,
immunosenescence. That intra-package roadmap (`FUTURE_WORK §A` through `§A⁶`) is now **exhausted**: thirty-five
targets, all measured, all graded, the absolute scales honestly left `[O]`.

The next growth is **outward**. The immune system is not an island in the VP program — it is the **hub** where three
other volumes physically meet:

- **Immunosurveillance** touches *every* malignancy the program models — it is already a cross-cutting seam onto every
  cancer kernel.
- **Tolerance** (the T21/T23/T24 saddle-node and its complement) is the same switch that, **localised to the gut
  wall**, IS inflammatory bowel disease — the immune↔digestive meeting point.
- **Inflammation** (the T31 cytokine latch) is what the immune system **writes back** to the mind's mood machinery,
  while the mind's HPA cascade **writes in** to immune suppression — the immune↔mind meeting point.

So the roadmap is no longer a list of organs to simulate. It is a **hub with spokes**: hub *functions*
(surveillance / tolerance / inflammation / hematopoiesis), each becoming one or more *seams* to a sibling volume.

```
                          ┌───────────────────────────────────┐
                          │   IMMUNE / HEMATOLOGIC  (the hub)  │
                          │   surveillance · tolerance ·       │
                          │   inflammation · hematopoiesis     │
                          │              — one R19 substrate   │
                          └───────────────────────────────────┘
                            ╱               │               ╲
             immunosurveillance        tolerance          inflammation
            (1/(1−escape), T10)     (T21/T23/T24)          (T31 latch)
                  ╱                       │                       ╲
                 ▼                        ▼                        ▼
        ┌──────────────┐      ┌────────────────────┐      ┌──────────────────┐
        │  ONCOLOGY    │      │   DIGESTIVE        │      │   MIND           │
        │  every cancer│      │   IBD mucosal latch│      │   HPA→σ (IN,sign)│
        │  kernel      │      │   = T23/T24 here   │      │   M→mood (OUT,→) │
        └──────────────┘      └────────────────────┘      └──────────────────┘
         (oldest spoke)        (gut–immune seam)            (neuro–immune seam)

           hematopoiesis (bone_marrow_hematopoiesis, RUNX1) — NEW in v0.17.0
                  ╱                                              ╲
                 ▼                                                ▼
        ┌──────────────────────┐                    ┌──────────────────────────┐
        │  CIRCULATORY         │                    │   MUSCULOSKELETAL        │
        │  leukocyte effectors │                    │   marrow niche houses    │
        │  → vasculature       │                    │   the hematopoietic root │
        │  (pointer OUT)       │                    │   (pointer; identity cand)│
        └──────────────────────┘                    └──────────────────────────┘
         (leukocyte-trafficking seam)                (marrow-niche seam)
```

---

## 2. The hub's four functions, and how each becomes a seam

| hub function | the in-package machinery | the seam it projects to | direction |
|---|---|---|---|
| **immunosurveillance** | `immune_escape_factor` = site-independent 1/(1−escape) multiplier (chapter 5, T10), Lever D (T15) therapy face | onto **every** VP cancer kernel (oncology hub) | OUT (multiplier) |
| **tolerance** | T21 central deletion · T23 autoimmune break (saddle-node) · T24 peripheral suppression (complement) | **digestive** gut mucosa (IBD = the switch localised); also the *target* of the mind IN direction | shared-substrate identity (gut) / SIGN in (neuro) |
| **inflammation** | T31 systemic cytokine latch (self-sustaining tone M, time-critical break) | **mind** depression chronification (§27) as the inflammatory contributor | OUT (one-way pointer) |
| **hematopoiesis** *(v0.17.0)* | the hematopoietic root `bone_marrow_hematopoiesis` (RUNX1, γ=1.3225, spinodal 0.585385) producing the leukocyte effector populations | **circulatory** vasculature (effectors traffic through it) and **musculoskeletal** marrow niche (houses the root) | OUT (two one-way pointers; musculoskeletal carries a named identity-upgrade candidate) |

The deep point: **the immune volume does not gain new physics by becoming a hub.** Every seam re-uses machinery this
volume already measured and graded. What the hub adds is the demonstration that **one substrate, derived once, is read
consistently across the sibling volumes without a refit** — and the discipline that keeps that demonstration honest.

---

## 3. Current spokes — delivered (v0.16.0 × 3 declared, v0.17.0 × 2 declared; v0.18.0 × 2 barrier-surface candidates; v0.19.0 musculoskeletal + v0.20.0 skin LIVE-verified)

| spoke | seam type | mechanism (closed-form / measured) | owner split | grade |
|---|---|---|---|---|
| **oncology hub** | one-way OUT multiplier | immune_escape_factor → 1/(1−escape) on every cancer kernel; Lever D therapy face | immune owns the escape seam (T10, measured); absolute incidence (K, μ0) [O] | [V] / [O] |
| **gut–immune** | shared-substrate identity + vendored snapshot | digestive IBD induction 0.8849 = antigen 0.50 + spinodal 0.3849 (T23 saddle-node); maintenance 0.1151 = antigen − spinodal (T24 complement); relapsing = T23 irreversibility | immune owns systemic tolerance primitive; digestive owns mucosal localisation + absolute antigen scale [O] + felt visceral [O] | [V] / [O] |
| **neuro–immune (IN)** | sign-only descriptor | mind HPA/cortisol → raises T24 suppressor σ (stress immunosuppression); σ swept, no value imported | direction immune-side [F]; magnitude (cortisol→σ gain) mind/anchor-owned [O] | [F] / [O] |
| **neuro–immune (OUT)** | one-way pointer | T31 cytokine tone M → mind §27 inflammatory contributor to depression | immune owns cytokine tone M (T31, [V]); felt low mood mind-owned [O] | [V] / [O] |
| **circulatory** *(v0.17.0)* | one-way pointer OUT | leukocyte effector populations (R19 ON-committed, rooted at bone_marrow_hematopoiesis RUNX1 γ=1.3225, spinodal 0.585385) traffic → circulatory vasculature; no circulatory value consumed | immune owns the effector populations (measured [V]); circulatory owns absolute vascular transport scale [O] | [V] / [F] / [O] |
| **musculoskeletal** *(v0.17.0; LIVE-VERIFIED v0.19.0)* | one-way pointer — **live-verified** (drift 0); identity candidate **RETIRED** | hematopoietic root (bone_marrow_hematopoiesis RUNX1, spinodal 0.585385, barrier 0.437252) housed in the marrow niche; pointer live-verified against musculoskeletal_vp_site v0.7.0 (substrate drift 0); the named identity upgrade is RETIRED on live evidence (the MSK niche is built by RUNX2, spinodal 0.53237264 ≠ 0.585385 — houses but is not the same switch) | immune owns the hematopoietic primitive (measured [V]); musculoskeletal owns absolute bone-niche scale [O] | [V] / [F] / [O] |
| **integumentary (skin)** *(v0.18.0 candidate; LIVE-VERIFIED v0.20.0)* | barrier-surface seam — **live substrate-verified** (drift 0) + **reciprocal immune-seam handshake**; identity immune-owned closed-form | epidermal barrier shares the byte-identical substrate (drift 0), surface REAL (epidermis TP63 spinodal 0.61335644, keratinocyte KRT14 spinodal 0.69962471); the skin volume independently declares `out__immune_hematologic__urticaria` (reciprocal); the epidermal-tolerance identity (induction = epidermal-antigen + spinodal(1.0)) stays immune-owned closed-form — the skin defers the immune tolerance switch as an out-seam, so it is confirmed-real-surface, **not contradicted**, **not engine-verified** | immune owns the barrier-agnostic tolerance primitive (measured [V]); skin owns absolute epidermal-antigen scale [O] (DOI 10.5281/zenodo.20754541) | [V] / [F] / [O] |

**Verification artefacts (all separate from the engine emit hash `e7a2a5b8…`):**
- Seam layer digest: `9357f23b…` (carries its own 2×sha256; SSOT `inherited/cross_references.json`).
- Live harness contract digest: `2b07d4d5…` (hashes only the immune-side contract → byte-identical with/without siblings).
- Firewall: **0 sibling imports** across 52 scanned files; emergence state carries no felt/HPA/cortisol/mind key.
- Live harness: 5/5 cross-volume checks PASS (substrate drift 0 ×2, gut latch identity live, neuro endpoint live).

---

## 4. Promoted adjacencies — now declared spokes (v0.17.0)

These two immune ↔ sibling relationships were inherited *adjacencies* (the substrate shared, the biology meeting)
through v0.16.0; **v0.17.0 PROMOTED both to explicitly declared one-way-pointer seams in `cross_references.json`**
(they are now rows in §3). Kept here for the audit trail of how they were promoted:

- **Circulatory — leukocyte trafficking.** ✅ **DECLARED (§3).** The circulatory volume (concept DOI
  10.5281/zenodo.20754354) carries the vascular transport on which immune cells traffic. Now a declared **one-way
  pointer** seam (immune effector populations → circulatory transport), no refit, firewall + byte-identical engine
  hash preserved. Owner split: immune owns the effector populations [V]; circulatory owns the absolute vascular
  transport scale [O].
- **Musculoskeletal — marrow niche.** ✅ **DECLARED (§3) as a one-way pointer; identity upgrade NAMED, not claimed.**
  This volume's `bone_marrow_hematopoiesis` organ (RUNX1, γ=1.3225, spinodal 0.585385) is the immune-side endpoint of
  that niche. Declared NOW as the weaker, verifiable-from-this-zip **one-way pointer** (hematopoietic root → bone
  niche). The stronger **shared-substrate identity** (niche threshold = the bone_marrow_hematopoiesis spinodal
  0.585385, the gut-seam pattern) is a **named candidate** with a stated promotion path (add to the §17 live harness,
  confirm drift 0 + niche-threshold equality) and falsifier — *not* claimed, because verifying an identity needs the
  live musculoskeletal engine, absent in this session.

Both are now *declared seams*; the musculoskeletal one carries a *named identity-upgrade candidate* awaiting a live
cross-package run.

---

## 4-bis. Barrier-surface agnosticism — the footing for new barrier spokes (v0.18.0)

The gut–immune identity (induction = antigen + spinodal(1.0); maintenance = antigen − spinodal(1.0)) is not specific
to the gut. Write the thresholds for an **arbitrary** barrier-surface antigen *a* at the shared mucosal R19 scale
(g = 1.0): the surface-independent **offset** from that surface's own antigen baseline is
induction − *a* = +spinodal(1.0) and maintenance − *a* = −spinodal(1.0). Across an illustrative 5-point antigen
sweep ({0.30, 0.40, 0.50, 0.60, 0.70}) the offset is **invariant == ±0.38490018 to the eighth decimal** — it never
depends on *a*. So the tolerance saddle-node is **barrier-surface-agnostic**: it behaves identically at every barrier
surface, only the surface's own antigen baseline differs. The gut (antigen 0.50) is the **one vendored, live-verified
point** on a barrier-agnostic line. This is a CLOSED-FORM **[F]** result resting on the MEASURED **[V]** T23
saddle-node + T24 suppressor complement; it is owned and verified in this package and feeds nothing hashed-core (the
engine emit() hash stays byte-identical, the seam layer carries its own 2×sha256). It is the structural footing that
makes the respiratory and skin barrier-immunity candidates (§5 #1, #2) principled rather than assumed: each real
surface's **absolute** antigen scale is [O], owned by that surface's future volume. (New chapter 19.)

---

## 5. Future spokes — candidates (emerge / identify, do not assume)

Same discipline as the intra-package roadmap: a spoke is only wired when its identity is **closed-form on the shared
substrate** (identity seam) or a **clearly one-way pointer** (no consumed sibling value). No spoke fabricates an
absolute scale.

1. **Respiratory mucosal immunity** *(new barrier-surface application of the gut–immune pattern).* ✅ **DONE as a
   NAMED CANDIDATE (v0.18.0).** A future respiratory/lung VP volume would localise the **same T23/T24 tolerance
   switch** to the airway mucosa — exactly the gut–immune *shared-substrate identity* seam re-applied to a different
   barrier surface. Grounded by **barrier-surface agnosticism** (§4-bis below): the surface-independent offset is
   invariant == ±spinodal(1.0)=±0.38490018 across the antigen sweep, so airway induction/maintenance would be
   airway-antigen ± spinodal in closed form. Declared as a NAMED candidate in `cross_references.json`, NOT a declared
   seam — it needs the live respiratory volume + that volume's **owned** absolute airway-antigen scale ([O] here).
   **Follow-up:** add the respiratory volume to the §17 live harness and confirm substrate drift 0 + airway threshold
   == airway-antigen ± spinodal; on success, promote to a *verified* identity. Falsifier: if the offset were not
   ±spinodal across the sweep, the candidate dies (the gut seam + agnosticism proof survive).
2. **Skin barrier immunity** *(epidermal barrier, same pattern).* ✅ **RESOLVED — LIVE substrate-verified
   (v0.20.0).** Named as a candidate in v0.18.0; with integumentary_vp_site v1.0.0 (concept DOI
   10.5281/zenodo.20754541) now on disk, it was tested in the §18 live harness: substrate drift measured **0** (the
   epidermal barrier and the immune tolerance machinery share one byte-identical R19 substrate, the barrier surface
   REAL — epidermis TP63 spinodal 0.61335644, keratinocyte KRT14 spinodal 0.69962471), and the skin volume
   **independently declares a reciprocal immune out-seam** (`out__immune_hematologic__urticaria`) — a bidirectional
   handshake. But the skin volume models the barrier STRUCTURE + autoantibody-adhesion saddle-nodes
   (pemphigus/pemphigoid — the same R19 formalism on a different compartment) and does NOT implement the immune
   tolerance switch (it names immune effects as un-modelled out-seams), so the epidermal-tolerance IDENTITY stays
   **immune-owned closed-form**: confirmed-real-surface, **not contradicted**, but **not engine-verified**. The
   absolute epidermal-antigen scale remains [O] (skin-owned). A **third distinct outcome** — between the gut
   (verified identity) and the marrow niche (retired identity), the honest middle. See §21 / new chapter 21.
3. **Promote circulatory & musculoskeletal adjacencies to declared seams.** ✅ **DONE (v0.17.0).** Both are now
   declared one-way-pointer entries in `cross_references.json` (§3/§4), each with its own snapshot-free pointer and
   the firewall + byte-identical engine hash preserved. **Follow-up ✅ RESOLVED (v0.19.0) — honest negative:** the
   musculoskeletal seam carried a *named* shared-substrate-identity upgrade candidate. With musculoskeletal_vp_site
   v0.7.0 now on disk, it was tested in the §18 live harness: substrate drift measured **0** (the one-way pointer is
   now **LIVE-VERIFIED** against the real MSK engine), but the **identity candidate is RETIRED** — the MSK volume
   builds the niche via OSTEOBLASTS (RUNX2, γ=1.2414, spinodal 0.53237264), a different master gene and spinodal
   from the hematopoietic RUNX1 (0.58538506; gap 0.05301242), and exposes no marrow-niche hematopoietic-commit
   threshold. The niche **houses** hematopoiesis but is not the same R19 switch; the threshold-equality identity
   does not reduce. The v0.17.0 falsifier fired exactly as written; nothing was tuned to rescue it; the pointer
   survives. Biologically correct (the osteoblastic niche supports but is distinct from the HSC). See §20 / new
   chapter 20.
4. **Neuro–immune magnitude anchor (closes one [O], only if principled).** The cortisol→σ gain is permanently `[O]`
   *in-package*. It could be **cited** ([L]) from an external endocrine–immune dataset — never fitted inside the
   substrate. If and only if a principled external anchor exists, the magnitude moves from `[O]` to cited-`[L]`; the
   direction stays `[F]`.

Every future spoke is **either** an identity seam (strongest — both volumes read the same R19) **or** a one-way
pointer (states where something travels, consumes no sibling value). The hub never imports sibling code into a gate.

---

## 6. The discipline that makes a hub safe

A hub is dangerous precisely because it touches everything. These rules (all enforced, not asserted) keep it honest:

- **Zero sibling imports in any gated package.** The research gate (`repro/run_all.py`) and the canonical build
  (`tools/build_docs.py`) compute nothing from a sibling and never import one. Scan: 0 violations / 52 files.
- **Verify-alone.** Each volume re-establishes its entire trusted state from its OWN zip with the siblings absent.
  The live harness runs OUTSIDE every gate and SKIPS cleanly when siblings are not on disk.
- **Separate digests.** The engine emit hash (`e7a2a5b8…`) is computed by `circulate()` ALONE. The seam layer
  (`ead505bb…`) and the harness contract (`78f5696c…`) each carry their OWN 2×sha256 and never feed the hashed core.
- **Owner split.** For every cross-package quantity, exactly one volume OWNS the absolute scale; the others carry it
  `[O]` with the owner named. (Mucosal antigen scale → digestive; cortisol→σ gain → mind/anchor; felt dimensions →
  their respective volumes.)
- **Seam-type taxonomy** (strongest to weakest):
  1. **shared-substrate identity** — both volumes read the same R19; the claim is a closed-form equality (gut–immune).
  2. **vendored snapshot** — read a value verified once against the source function (the IBD snapshot the gut seam consumes).
  3. **one-way pointer** — states WHERE an item travels, consumes no sibling value (cytokine → mood; surveillance → cancer kernels).
  4. **sign-only descriptor** — consumes a DIRECTION, never a magnitude (cortisol → σ); the magnitude stays `[O]`.

---

## 7. Falsifiers for the hub claims

Per VP-SPEC, every load-bearing seam claim names a measurable observation that would kill it:

- **Gut–immune identity** — dies if digestive's live `ibd_relapsing_course()` induction/maintenance thresholds stop
  equalling antigen ± spinodal on the shared substrate, or if the substrate drift between volumes is ever non-zero.
- **Neuro–immune IN (sign)** — dies if a sustained cortisol/stress drive *raised* surveillance (lowered T24 σ); the
  claim is only the sign, so a wrong sign refutes it.
- **Neuro–immune OUT (pointer)** — dies if the mind §27 depression module stopped listing an inflammatory contributor
  (the pointer would then land on nothing), or if the immune volume were found to consume a mind value (it would no
  longer be one-way).
- **Oncology hub** — dies if the escape multiplier were not site-independent (if 1/(1−escape) failed to collapse the
  cross-site curves).
- **Circulatory (leukocyte trafficking)** — dies if the immune volume were found to consume a circulatory value (it
  would no longer be one-way), or if the cross-volume substrate drift to circulatory were ever non-zero.
- **Musculoskeletal (marrow niche)** — the *pointer* dies if the immune volume consumed a musculoskeletal value, or
  if the substrate drift were non-zero. **v0.19.0 outcome (tested live against musculoskeletal_vp_site v0.7.0):** the
  substrate drift measured **0**, so the pointer is **live-verified and survives**. The *named identity-upgrade
  candidate* **FIRED its falsifier and is RETIRED**: the live musculoskeletal marrow-niche threshold did NOT reduce
  to the bone_marrow_hematopoiesis spinodal 0.58538506 — the MSK niche is built by RUNX2 (spinodal 0.53237264 ≠
  0.58538506) and exposes no hematopoietic-commit threshold, so the identity does not hold. The pointer survives that
  (a pointer asserts no equality). This is the discipline working as designed — a named candidate met its live test
  and was retired honestly, nothing tuned to rescue it.
- **Integumentary (skin barrier)** — the *adjacency* dies if the substrate drift between volumes were non-zero, or
  if the skin volume consumed an immune value. **v0.20.0 outcome (tested live against integumentary_vp_site
  v1.0.0):** the substrate drift measured **0**, so the barrier surface and the immune tolerance machinery share
  one byte-identical R19 substrate (barrier surface REAL — epidermis TP63, keratinocyte KRT14), and the skin volume
  **independently declares a reciprocal immune out-seam** — the adjacency is **live-verified and reciprocated**. The
  *epidermal-tolerance identity* is neither verified nor contradicted: the skin volume does not implement an immune
  tolerance switch (it models the barrier structure and names immune effects as out-seams), so there is no epidermal
  threshold to equate. The identity stands as the immune-owned closed-form result of barrier-surface agnosticism,
  with a confirmed real surface. Its *future* falsifier: if a skin tolerance module later exposed an epidermal
  threshold that did NOT reduce to epidermal-antigen + spinodal(1.0), the identity would be retired (the
  barrier-agnosticism proof + the gut seam survive); if it DID, the identity would be promoted to engine-verified.
- **Firewall** — dies the instant a sibling import appears in a gated file, or the emergence state acquires a
  felt/HPA/mind key.

---

*This roadmap is planning + architecture only. It states honestly what is a closed-form identity on the shared
substrate, what is a one-way pointer, and what absolute scale is owned elsewhere and therefore permanently `[O]` here.
The cross-package claims are DIRECTION/CLASS and structural-identity statements — **not** medical advice, **not** a
validation of VP theory.*
