"""
electron_one_second.py

'빛의 속도와 전자 1초' 문서에서 정의한 구조를 따르는
전자 1초 검증용 코드 골격.

핵심 개념 (문서 요약):
- 전자 사건 시퀀스 {n_k} (격자 tick 인덱스)
- tick 시간 간격 Δt (zeptosecond 스케일, 빛-속도 구현에서 LOCK된 값)
- 사건 간 간격: Δn_k = n_{k+1} - n_k
- SI 시간으로 환산: T_k = Δn_k · Δt
- 전자 1초 추정치: T̃_e = median_k(T_k)
- 이상적으로 T̃_e → 1.0 s 근방으로 수렴해야 함.

여기서는:
- {n_k}를 생성하는 간단한 모형(포아송 과정)을 제공하고,
- 위 정의에 따라 T̃_e를 계산하는 도구 함수를 구현한다.
"""

import random
import statistics
from dataclasses import dataclass
from typing import List


@dataclass
class ElectronEvents:
    """
    전자 사건 시퀀스를 표현하는 데이터 클래스.

    attributes
    ----------
    n : List[int]
        사건이 발생한 tick 인덱스 목록 (단조 증가 가정).
    delta_t : float
        tick 하나의 물리적 시간 (초 단위). 'realization_lock'에서 온 값과 대응.
    """
    n: List[int]
    delta_t: float

    def intervals_in_ticks(self) -> List[int]:
        """
        Δn_k = n_{k+1} - n_k 리스트를 반환.
        """
        return [self.n[i+1] - self.n[i] for i in range(len(self.n)-1)]

    def intervals_in_seconds(self) -> List[float]:
        """
        T_k = Δn_k · Δt 리스트를 반환.
        """
        return [dn * self.delta_t for dn in self.intervals_in_ticks()]

    def electron_second_estimate(self) -> float:
        """
        T̃_e = median_k(T_k)를 계산.
        """
        T = self.intervals_in_seconds()
        if not T:
            raise ValueError("Need at least two events to define an interval")
        return statistics.median(T)


def generate_poisson_events(rate_hz: float, duration_s: float, delta_t: float, seed: int = 1234) -> ElectronEvents:
    """
    단순 포아송(무메모리) 사건율 모형으로 전자 사건 시퀀스를 생성.

    parameters
    ----------
    rate_hz : float
        초당 평균 사건 수 (예: ν_e ≈ 1 Hz 정도라면 1.0).
    duration_s : float
        전체 시뮬레이션 시간 (초). 충분히 길게 잡을수록 통계가 좋아짐.
    delta_t : float
        tick 하나의 길이 (초). 빛-속도 격자에서 LOCK된 값과 연결 가능.
    seed : int
        난수 시드.

    returns
    -------
    ElectronEvents
        생성된 사건 인덱스와 Δt를 담은 객체.
    """
    random.seed(seed)

    n_ticks_total = int(duration_s / delta_t)
    if n_ticks_total <= 0:
        raise ValueError("duration_s must be larger than delta_t")

    # 포아송(rate_hz) 과정에서 사건 사이 시간은 지수분포(평균 1/rate_hz)
    # 이 시간 간격을 tick 수로 환산해 누적.
    events = []
    t_ticks = 0
    while t_ticks < n_ticks_total:
        # 지수분포로 도약 시간 샘플
        dt_cont = random.expovariate(rate_hz)    # [s]
        dn = max(1, int(round(dt_cont / delta_t)))
        t_ticks += dn
        if t_ticks >= n_ticks_total:
            break
        events.append(t_ticks)

    # n_0를 0에서 시작하는 형태로 맞추고 싶다면 아래와 같이 앞에 0을 추가할 수도 있다.
    if events and events[0] != 0:
        events.insert(0, 0)

    return ElectronEvents(n=events, delta_t=delta_t)


def demo():
    """
    예제:
    - ν_e ≈ 1 Hz, Δt = 1e-21 s, duration = 10 s 로 설정.
    - 생성된 사건열에서 전자 1초 추정치 T̃_e가 1초 근방인지 확인.
    """
    rate_hz = 1.0
    delta_t = 1e-21     # zeptosecond 스케일 예시
    duration_s = 10.0

    ev = generate_poisson_events(rate_hz, duration_s, delta_t, seed=2025)
    Te = ev.electron_second_estimate()

    print("=== Electron 1-second toy demo ===")
    print(f"Number of events      : {len(ev.n)}")
    print(f"Δt (tick size)        : {delta_t:.2e} s")
    print(f"Estimated T_e (median): {Te:.4f} s")
    print("※ 실제 문서의 ν_e=1 정준 전개 및 Φ/χ 분해는")
    print("   여기 뼈대를 기반으로 더 정교한 규칙을 채워 넣어 구현할 수 있다.")


if __name__ == "__main__":
    demo()
