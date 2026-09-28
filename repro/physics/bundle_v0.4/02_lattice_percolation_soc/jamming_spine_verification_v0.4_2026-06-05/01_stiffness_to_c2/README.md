# 01 — 강성 → c² (부피탄성률 → 단일 종파속도)

## 물리
잼밍 매질은 회전/온도로 한계잼밍(z=2d=6)에 놓인다. 이 한계에서 **전단은 연화(G→0)**하지만
**부피 압축은 단단(B 유한)**하다. 횡파가 죽고 종파 하나만 남으므로 생존 속도는
```
    c² = B/ρ = K   (집단강성)
```
"무한강성에서 c²"의 뜻: 접촉강성 k→∞면 c→∞이니, 유한 c는 유한 K(=B/ρ)를 고른다.

## 방법 (검증된 핀-해)
같은 패킹에서 Born 강성 + 비affine 완화를 정확 선형응답으로 계산:
- B_aff = (1/d²V)Σk r² + ((d−1)/d)P,  비affine 구동 Ξ^bulk_i = K·Σ r·n̂,  B_rel = B_aff − (1/d²V)Ξᵀδ.
- backbone 가장 높은 배위 입자 3 DOF 핀 → 양정치 축약 Hessian → Cholesky(=PSD 게이트) → 2회 반복정제.
- 게이트: Born 해석식 = 유한차분(4.7e-7 일치), 0 ≤ B_rel ≤ B_Born.

## 파일
- `relaxed_shear.py` — 공유 인프라: 패킹 생성/FIRE/접촉/backbone/Hessian/Born/relaxed G (bulk가 import).
- `bulk.py` — 부피탄성률 B(affine·relaxed), c²=B/ρ. (상단 docstring에 식·게이트 설명.)
- `bulk_run.py` — 생산 러너(B·G 같은 패킹에서). 사용: `python3 bulk_run.py <N> <start> <count>`.
- `fig_bulk.py` — B_relaxed & G_relaxed vs z, c²/a² vs z 그림.
- `results_bulk/bulkG.csv` — 결과 데이터(N=256: 58 cfgs, N=512: 18 cfgs; φ 0.636–0.720).
- `bulk_modulus_c2.png/.pdf` — 그림.

## 결과 [V]
- z=6 에서 **B_relaxed 유한** = 0.76(N256)/0.95(N512), R²=0.97–0.98.
- z=6 에서 **G_relaxed → 0** = 0.009(N256)/−0.0005(N512).
- **c²/a²|_{z=6} = 0.107** (N-무관) = affine z/2d²(=0.167)의 0.65배(비affine 연화 35%).
- 이전 분산측정 c_L²/a²=0.09–0.15 가 이를 포괄 ⇒ 단일 종파속도 c²=B/ρ 확정.

## 실행
```bash
python3 bulk_run.py 256 0 4     # 일부 cfg 재생산 (수 분)
python3 fig_bulk.py             # 그림 재생성 (results_bulk/bulkG.csv 필요)
```
