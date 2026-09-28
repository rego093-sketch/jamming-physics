"""
proton_shell_mc.py

재밍 격자 82+7 양성자 모형에서,
표면 7개 껍질 유닛의 상쇄/생존 패턴을 살펴보는 간단한 몬테카를로 예제.

* 격자:
    - 정수 좌표 (x, y, z) ∈ {-2, -1, 0, 1, 2}^3 중
      x^2 + y^2 + z^2 = 8 인 점들을 "표면 셀" 후보로 사용한다.
    - 예: (-2,-2,0), (0,-2,-2), (-2,0,-2), ...

* 동역학(단순 골격):
    1. 표면 후보 중에서 7개를 무작위로 선택.
    2. v와 -v 쌍이 동시에 존재하면 상쇄되어 진동(물질파)로 간주하고 제거.
    3. 상쇄되지 않고 남는 벡터를 Survivor로 기록.

실제 백서에서는 700회 시뮬레이션에서 [-2, 0, -2] 방향이
가장 높은 생존 빈도를 보이는 것으로 보고되었다.
여기 코드는 그 구조를 재현하기 위한 최소 예제이며,
정확한 확률 분포는 사용자의 세부 규칙(초기 조건, 재밍 규칙 등)에 맞게
추가 튜닝이 필요하다.
"""

import itertools
import random
import collections
import math
from typing import List, Tuple, Dict


Vector = Tuple[int, int, int]


def surface_candidates(d2: int = 8) -> List[Vector]:
    """
    x^2 + y^2 + z^2 = d2 를 만족하는 격자 점들을 모두 생성.
    기본값 d2=8은 |x|,|y|,|z|<=2 범위에서 양성자 표면을 대표하는 셀 집합과 호환된다.
    """
    cands = []
    for x in range(-2, 3):
        for y in range(-2, 3):
            for z in range(-2, 3):
                if x * x + y * y + z * z == d2:
                    cands.append((x, y, z))
    return cands


def cancel_pairs(vectors: List[Vector]) -> List[Vector]:
    """
    주어진 벡터 리스트에서 v와 -v 쌍을 상쇄시키고,
    상쇄되지 않고 남는 벡터들만 반환.
    """
    chosen_set = set(vectors)
    cancelled = set()
    for v in vectors:
        if v in cancelled:
            continue
        neg = (-v[0], -v[1], -v[2])
        if neg in chosen_set and neg not in cancelled:
            cancelled.add(v)
            cancelled.add(neg)
    survivors = [v for v in vectors if v not in cancelled]
    return survivors


def mc_trial(cands: List[Vector]) -> List[Vector]:
    """
    한 번의 몬테카를로 trial:
    - 후보 셀 중 7개를 무작위 선택,
    - 상쇄 규칙을 적용해 Survivor 리스트를 반환.
    """
    if len(cands) < 7:
        raise ValueError("Need at least 7 candidate sites")
    chosen = random.sample(cands, 7)
    survivors = cancel_pairs(chosen)
    return survivors


def run_mc(n_trials: int = 700, seed: int = 1234) -> Dict[str, object]:
    """
    n_trials 번 시뮬레이션을 돌려
    - Survivor 개수 분포
    - Survivor가 1개일 때 그 방향의 빈도 분포
    를 집계한다.

    반환 값은 후처리/플롯을 위해 dict 형태로 제공한다.
    """
    random.seed(seed)
    cands = surface_candidates()
    length_counter = collections.Counter()
    direction_counter = collections.Counter()

    for _ in range(n_trials):
        survivors = mc_trial(cands)
        length_counter[len(survivors)] += 1
        if len(survivors) == 1:
            direction_counter[survivors[0]] += 1

    return {
        "n_trials": n_trials,
        "length_hist": dict(length_counter),
        "direction_hist": {str(k): v for k, v in direction_counter.items()},
        "candidates": cands,
    }


def demo():
    """
    콘솔 데모:
    - trial 개수 700 기준으로 백서와 유사한 설정을 사용.
    """
    result = run_mc(n_trials=700, seed=42)
    print("=== Proton shell Monte Carlo demo (toy model) ===")
    print(f"Trials         : {result['n_trials']}")
    print(f"Survivor count : {result['length_hist']}")
    print("Single-survivor directions (vector: count):")
    for k, v in sorted(result["direction_hist"].items(), key=lambda kv: -kv[1])[:10]:
        print(f"  {k:>12} : {v:4d}")
    print()
    print("※ 실제 논문에서 보고된 '[-2, 0, -2]'의 최빈성은")
    print("   초기 조건/재밍 규칙 등을 더 정교하게 반영한 코드로 재현할 수 있다.")


if __name__ == "__main__":
    demo()
