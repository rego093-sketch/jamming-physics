"""
feasibility_map.py  --  "모델이 어디서 사는가"를 계산이 답하게 한다
=====================================================================
이전 Sim 3는 mu_eff, sigma_n, dP, 기하를 *서로 독립* 인 넓은 사전분포로 두어
Pr(Lambda>1)=12% -> STOP 이었다. 그러나 이들은 깊이 d로 *결합* 되어 있다:

  - 마찰은 더 이상 자유변수가 아니다: VP 잼밍 액체화(WP-T1)가 정한다.
      액체화 상태 tau_res = eta_flow * (V/h)  (점성, sigma_n 무관)
      => mu_eff(d) = tau_res / sigma'(d)        (깊을수록 작아짐!)
  - 정상응력: sigma'(d) = (rho - rho_w) g d     (부력 리소스태틱)
  - 흡입 한계: 결손은 주변압을 넘을 수 없다 -> dP(d) = kappa * sigma'(d)  (보수적)
  - 기하: A_cross/A_base = d / W   (슬랩 두께 / 블록 폭)

  => Lambda = (dP * A_cross)/(mu_eff * sigma' * A_base)
            = kappa * (d/W) / mu_eff
            = kappa * h * (rho-rho_w) * g * d^2 / (W * eta_flow * V)

핵심: Lambda ~ d^2 (깊이 제곱으로 증가). 액체화 마찰은 깊을수록 작아지고
(점성 전단응력은 고정인데 정상응력이 커지므로), 가용 흡입은 깊을수록 커진다.
=> 데이터가 viable 깊이를 직접 말한다 (이론 가정이 아니라 계산).

Pure numpy. Deterministic. 모든 수는 물리 스케일.
"""
import numpy as np

# ---- fixed physical scales ----
g      = 9.8
rho    = 2900.0       # crustal density [kg/m^3]
rho_w  = 1000.0       # pore fluid density
h      = 3.0e-3       # liquefied shear-zone thickness [m]
mu_dry = 0.6          # dry Coulomb cap (if not liquefied)

def sigma_eff(d):                       # effective normal stress on detachment [Pa]
    return (rho - rho_w) * g * d

def mu_eff_liquefied(d, V, eta_flow):   # friction PINNED by VP-jamming liquefaction
    tau_res = eta_flow * (V / h)        # viscous (State-3) shear stress
    mu = tau_res / sigma_eff(d)
    return np.minimum(mu, mu_dry)       # cannot exceed dry Coulomb

def Lambda(d, V, kappa, eta_flow, W):
    dP = kappa * sigma_eff(d)           # suction deficit (<= ambient, conservative)
    mu = mu_eff_liquefied(d, V, eta_flow)
    Across_over_Abase = d / W
    return (dP * Across_over_Abase) / (mu * sigma_eff(d))

def crit_depth(V, kappa, eta_flow, W):
    """smallest depth where Lambda>=1 (None if none up to 200 km)."""
    dd = np.linspace(200, 2.0e5, 4000)
    L = Lambda(dd, V, kappa, eta_flow, W)
    idx = np.where(L >= 1.0)[0]
    return dd[idx[0]] if len(idx) else None

if __name__ == "__main__":
    print("="*74)
    print("FEASIBILITY: friction pinned by liquefaction -> where does Lambda>1 live?")
    print("="*74)
    # baseline parameters
    V0, kap0, eta0, W0 = 1.0, 0.5, 1.0e3, 4.0e6
    print(f"baseline: V={V0} m/s, kappa(deficit frac)={kap0}, eta_flow={eta0:.0e} Pa s, W={W0/1e3:.0f} km\n")

    for d_km in [2,5,10,15,20,30,50,80]:
        d=d_km*1e3
        mu=mu_eff_liquefied(d,V0,eta0); L=Lambda(d,V0,kap0,eta0,W0)
        tag = "  <-- Lambda>1 (FEASIBLE)" if L>=1 else ""
        print(f"  depth {d_km:3d} km: sigma'={sigma_eff(d)/1e6:6.0f} MPa  "
              f"mu_eff={mu:8.2e}  Lambda={L:7.2f}{tag}")

    dcrit = crit_depth(V0,kap0,eta0,W0)
    print(f"\n  => critical depth (Lambda=1): {dcrit/1e3:.1f} km" if dcrit else "  none")
    print(f"  => DATA SAYS: model lives at detachment depth >~ {dcrit/1e3:.0f} km (NOT shallow).")

    print("\n"+"-"*74)
    print("SENSITIVITY of critical depth (km) to the uncertain parameters:")
    print("-"*74)
    print("  vs slip rate V (kappa=0.5, eta=1e3, W=4000km):")
    for V in [0.01,0.1,1.0,10.0]:
        dc=crit_depth(V,0.5,1e3,4e6)
        print(f"     V={V:6.2f} m/s -> crit depth = {dc/1e3:5.1f} km" if dc else f"     V={V}: none<200km")
    print("  vs liquefied viscosity eta_flow (V=1, kappa=0.5, W=4000km):")
    for e in [1e2,1e3,1e4,1e5]:
        dc=crit_depth(1.0,0.5,e,4e6)
        print(f"     eta={e:.0e} Pa s -> crit depth = {dc/1e3:5.1f} km" if dc else f"     eta={e:.0e}: none<200km")
    print("  vs deficit fraction kappa (V=1, eta=1e3, W=4000km):")
    for k in [0.1,0.3,0.5,1.0]:
        dc=crit_depth(1.0,k,1e3,4e6)
        print(f"     kappa={k:.1f} -> crit depth = {dc/1e3:5.1f} km" if dc else f"     kappa={k}: none<200km")
    print("  vs block width W (V=1, kappa=0.5, eta=1e3):")
    for w in [1e6,2e6,4e6,8e6]:
        dc=crit_depth(1.0,0.5,1e3,w)
        print(f"     W={w/1e3:4.0f} km -> crit depth = {dc/1e3:5.1f} km" if dc else f"     W={w/1e3:.0f}km: none<200km")

    # save map for plotting: Lambda over (depth, V)
    dd=np.linspace(1e3,1.0e5,200); VV=np.logspace(-2,1,200)
    DD,VVg=np.meshgrid(dd,VV)
    Lmap=Lambda(DD,VVg,0.5,1e3,4e6)
    np.savez("feasibility_results.npz", dd=dd, VV=VV, Lmap=Lmap, dcrit=dcrit)
    print("\nsaved -> feasibility_results.npz")
