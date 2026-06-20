# STATUS — VP 사이트 변환 (인계용 단일 상태표)

마지막 갱신: 물리편 Phase 3 완료 시점. 이 파일이 진행 상태의 단일 출처다.
표준서 = VP_SPEC_v1_7.md. 도구 = r6. 상태는 오직 파일로만 승계한다(대화 기억 의존 금지).

## 1. 불변(LOCK) 핵심값
- src tex sha (물리, 봉인): 305a5a247b3eedac2942d3bbdd0913b72a8c169bd21fba68f755e9ba7e442271
  → 본문·수식·수치는 어떤 Phase 에서도 불변. 변하면 즉시 중단·복구.
- 표준 기계: **r6** (tools_sha16 = f637878baee1d719). 원장: reports/phase0-notes.md.
- repo: github.com/rego093-sketch/jamming-physics (LOCK). 게시 루트 docs/.

## 2. 백서별 진행 (per-paper 0→1→2→3, 이후 프로젝트 4→5→6→7)
| paper | 0 | 1 | 2 | 3 | 비고 |
|---|---|---|---|---|---|
| physics | ✅ | ✅ | ✅ | ✅ | **per-paper 전 Phase 완료.** 49섹션. 게이트 1/2/3 전부 PASS. |
| geodynamics | — | — | — | — | **원본 미보유** — 시작하려면 저자 tex 필요 |
| dna | — | — | — | — | 원본 미보유 |
| cosmology | — | — | — | — | 원본 미보유 |
| (5th) | — | — | — | — | 레지스트리 2장 참조, 원본 미보유 |
| (6th) | — | — | — | — | 원본 미보유 |

현재 워크스페이스에는 **물리편 원본만** 존재. 다른 5편은 저자 원본(tex)이 들어와야 진행 가능.

## 3. 프로젝트 Phase (전 백서 Phase 3 이후 착수)
- Phase 4 (개념 사전 concepts/): 백서 횡단 — 전 백서 용어 필요. **대기**.
- Phase 5 (최상위 index+sitemap+301): 6개 허브 링크 — 6편 허브 필요. **대기**(현재 물리 1편뿐).
- Phase 6 (전 사이트 최종 게이트): **대기**.
- Phase 7 (Scholar/Zenodo/PDF 1면/README): 저자 협업 — **대기**.

## 4. 물리편 산출물 위치
- 사이트: docs/physics/  (49 챕터 + index.html 허브)
- 메타: docs/physics/_meta.json (chapters[].one_liner 22 / grade 13, hub abstract 채움)
- 게이트: reports/phase{1,2,3}-physics.gate.json — 모두 verdict PASS
- 도구(r6): tools/{inventory,split,gate}.py · tools/render_eq.js · tools/derive_meta.py · tools/build_hub.py

## 5. 재개·검증 명령 (복사용)
```
cd /home/claude/work/r3
# 클린 복원점(물리 docs Phase 2 전 상태): /tmp/physics_backup
# 전체 재생성(물리): split→render 는 Phase 1 산출 유지, Phase 2·3 만 재실행
rm -rf tools/__pycache__
python3 tools/derive_meta.py --paper physics      # Phase 2 파생
python3 tools/build_hub.py   --paper physics      # Phase 3 허브
python3 tools/gate.py --phase 1 --paper physics   # → reports/phase1-physics.gate.json
python3 tools/gate.py --phase 2 --paper physics
python3 tools/gate.py --phase 3 --paper physics
# 불변 확인
sha256sum src/physics/*.tex   # 305a5a24… 이어야 함
```
주의: 게이트는 tools_sha 계산상 매 실행 전 `rm -rf tools/__pycache__` 권장.

## 6. 다음 세션이 할 일 (우선순위)
1. (입력 있으면) 다른 백서 원본 tex 수령 → 해당 paper 로 Phase 1(inventory/split/render/gate)
   → Phase 2(derive_meta) → Phase 3(build_hub). 물리편과 동일 도구·절차.
2. (6편 허브 준비되면) Phase 5 최상위 index+sitemap+301, 이어 Phase 6 최종 게이트.
3. derive_meta/build_hub 의 REGISTRY 딕셔너리에 새 paper 항목 추가(약칭·repo·headline·xlinks).
4. 모든 변경은 reports/phase0-notes.md 원장에 도구판(rN) 기록 + 본 STATUS 갱신.
