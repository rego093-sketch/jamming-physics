"""
jamming_bistability.py  --  잼밍 쌍안정: "느린 액체화는 불가능" (사용자 통찰의 1차원리)
================================================================================
사용자: "액체화된게 너무 느리면 그것도 이상하다." -- 정확하다.
잼밍은 쌍안정(bistable)이다: 막힘(State4, 고마찰) 또는 흐름(State3, 저마찰·빠름).
*느린 액체화* 라는 안정 가지는 없다. 이유(메커니즘, 수비학 아님):
  액체화 유지 = 전단열이 냉각을 이겨 전단대 온도를 언잼 임계 dT_unjam 위로 유지.
  전단열 Q_gen = tau*V = eta*V^2/h ;  전단대 정상 온도상승 dT(V) = eta*V^2/(8k).
  유지 조건 dT(V) >= dT_unjam  =>  V >= V_crit = sqrt(8 k dT_unjam / eta).
  V_crit ~ mm/s..m/s  >>  cm/yr(3e-10 m/s).  => 액체화는 *느릴 수 없다*.

결과: 정상 전단응력 tau_ss(V)이 액체화 천이에서 *속도-약화*(d tau/dV<0) => 불안정
=> 중간 속도에 머물 수 없음 => 운동은 "막힘 or 빠름"(stick-slip). 외형상 cm/yr은
brief 고속 슬립의 *시간평균* 일 뿐. (확립 단층물리: 전단열 폭주 / rate-weakening 불안정.)

Pure numpy. Deterministic.
"""
import numpy as np

k=3.0          # thermal conductivity [W/m/K]
dT_unjam=25.0  # unjamming temperature rise [K] (from vp_jamming_friction)
eta=1.0e3      # liquefied gouge viscosity [Pa s]
h=3.0e-3       # shear-zone thickness [m]
mu_dry=0.6     # jammed Coulomb friction
sigma=200e6    # effective normal stress at ~12 km [Pa]
yr=3.15e7

def dT_of_V(V):  return eta*V**2/(8*k)
def V_crit(eta): return np.sqrt(8*k*dT_unjam/eta)

def tau_ss(V):
    """steady shear stress: jammed Coulomb (low V) -> liquefied viscous (high V)."""
    xi=1.0/(1.0+np.exp(-(dT_of_V(V)-dT_unjam)/(0.2*dT_unjam)))   # liquefaction fraction 0->1
    return (1-xi)*mu_dry*sigma + xi*(eta*V/h)

if __name__=="__main__":
    print("="*78)
    print("JAMMING BISTABILITY: a liquefied shear zone CANNOT creep slowly")
    print("="*78)
    Vc=V_crit(eta)
    print(f"\n  V_crit = sqrt(8 k dT_unjam/eta) = {Vc:.2e} m/s  ({Vc*1e3:.0f} mm/s)")
    print(f"  (range over eta=1e2..1e6 Pa s: {V_crit(1e6):.2e}..{V_crit(1e2):.2e} m/s = mm/s..m/s)")
    vcmyr=0.03/yr
    print(f"  cm/yr spreading = {vcmyr:.2e} m/s  => V_crit is ~{Vc/vcmyr:.0e}x faster than cm/yr")
    print(f"  => below V_crit the shear heat ~ eta V^2/h is negligible; the band cools and")
    print(f"     RE-JAMS (State3->4). Sustained liquefaction REQUIRES seismic-scale V. (user's point.)")

    # steady friction curve: show velocity-weakening (instability)
    V=np.logspace(-10,1,400)
    tau=tau_ss(V)
    # locate velocity-weakening region (d tau/d log V < 0)
    dtau=np.gradient(tau, np.log10(V))
    vw = dtau<0
    print(f"\n  steady shear stress tau_ss(V):")
    print(f"    jammed branch (V<<V_crit): tau ~ mu_dry*sigma = {mu_dry*sigma/1e6:.0f} MPa (stuck)")
    print(f"    liquefied branch (V~V_crit): tau = eta V/h ~ {eta*Vc/h/1e6:.2f} MPa (free)")
    print(f"    => stress DROP ~{mu_dry*sigma/(eta*Vc/h):.0f}x across liquefaction = strong")
    print(f"       VELOCITY-WEAKENING (d tau/dV<0) over V in "
          f"[{V[vw][0]:.1e}, {V[vw][-1]:.1e}] m/s => UNSTABLE => stick-slip.")

    # stick-slip time-average reconciliation
    print(f"\n  STICK-SLIP reconciliation (why mainstream sees 'slow steady'):")
    s=3.0e6; Vslip=0.5
    t_cum=s/Vslip
    print(f"    open {s/1e3:.0f} km at V_slip={Vslip} m/s -> cumulative actual sliding = "
          f"{t_cum:.1e} s = {t_cum/86400:.0f} days only.")
    for vapp in [30,92]:
        duty=(vapp*1e-3/yr)/Vslip
        print(f"    apparent avg {vapp} mm/yr => duty cycle {duty:.1e} (sliding {duty*100:.1e}% of time);")
    print(f"    => the SAME ~{t_cum/86400:.0f} days of fast slip, packed sparsely, LOOKS like slow steady")
    print(f"       spreading when time-averaged. 'Slow' is an averaging artifact of stick-slip.")

    print("\n  HONEST scope:")
    print("   - V_crit depends on eta (uncertain) but is robustly mm/s..m/s = orders above cm/yr")
    print("     (a scale result, NOT a tuned coincidence).")
    print("   - This fixes the MOTION MODE (fast episodic, not slow steady) = what jamming predicts,")
    print("     consistent with the rapid hypothesis. It does NOT by itself fix the ABSOLUTE timescale")
    print("     (how sparsely the slips are packed) -- that needs the trigger recurrence + absolute")
    print("     dating (chronology firewall).")

    np.savez("jamming_bistability_results.npz", V=V, tau=tau, Vc=Vc, vw=vw,
             t_cum_days=t_cum/86400)
    print("\nsaved -> jamming_bistability_results.npz")
