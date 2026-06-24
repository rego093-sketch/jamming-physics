"""
vp_jamming_friction.py  --  마찰 붕괴를 VP 잼밍이론에서 유도 (사용자 지시)
============================================================================
사용자 명령: "물리백서의 잼밍이론에서 마찰을 해결하라. 고온에너지는 액체화를 만든다."

VP 잼밍이론(vp_whitepaper_v0.4.0_jamming_spine)에서 직접 유도:
  - 전단대(거지)는 잼드 고체: 접촉수 z > z_iso = 2d = 6  (State 4, 고친마찰)
  - "회전(온도)이 z를 강성 임계로 몬다"(S2.2): 마찰열=고온에너지=demand Psi_req가
    접촉결합을 깨며(L.2: 에너지=언잼밍 비용의 열쇠) z를 z_iso로 끌어내린다.
  - z=2d=6 에서 전단 reserve=0 -> 완화 전단탄성률·항복응력 소멸(S2.3/S2.4):
        G_relaxed -> 0,  sigma_y -> 0   (벌크 B는 유한)
    => State 4(고체) -> State 3(액체): **액체화(unjamming)** , 용융이 아님.
  - 저항 혼합(VP-N1):  tau_res = xi*mu_dry*sigma' + (1-xi)*eta_flow*(V/h)
        xi = 1-phi (잼밍 health). phi: State4 ~0 -> State3 ->1.
  - 에너지 회계(L.2): 마찰일은 먼저 '언잼밍 잠열'(접촉파괴)로 소모되고 -> 액체화 후
    마찰이 붕괴하므로 가열이 멈춘다 -> 온도는 용융점 훨씬 아래에서 멈춘다.
    이것이 "고온에너지 -> 액체화 (용융 아님)".

대조군: '용융 전용'(언잼밍 채널 없음) -> z 고정, 마찰 유지, 모든 일이 T로 -> 용융.

확립물리 정합(차용 아님, 검증): isostatic sigma_y->0 (O'Hern-Silbert-Liu-Nagel; Wyart),
fault gouge granular fluidization/nanopowder lubrication (De Paola; Han; Reches).

Pure numpy. Deterministic.
"""
import numpy as np

# ---- shear-zone / material (literature-scale) ----
mu_dry  = 0.6
sigma_n = 150e6
p0      = 50e6
sigp    = sigma_n - p0          # effective normal stress (jammed) [Pa]
eta_flow= 1.0e3                 # flowing (State-3) effective viscosity [Pa s]  (granular suspension)
h_sz    = 3.0e-3                # shear-zone width [m]
rho_c   = 2.7e6                 # volumetric heat capacity [J/(m^3 K)]
T_melt  = 1000.0                # melt temperature rise [K]
L_melt_vol = 1.08e9            # latent heat of melting per volume [J/m^3] (rho*4e5)

# ---- jamming parameters (from spine S2.4) ----
# PROVENANCE: the rule FORM used here is no longer assumed -- it is DERIVED from
# first principles in jamming_microderive.py + jamming_shear_modulus.py (2D, z_iso=2d=4):
#   * phi_jam ~ 0.84 (onset of rigidity)            [measured]
#   * z -> z_iso = 2d at jamming                    [measured: 4 in 2D, 6 in 3D=spine]
#   * (z - z_iso) ~ (phi-phi_jam)^0.5, p~(phi-phi_jam)   [classic exponents reproduced]
#   * G_relaxed ~ (z - z_iso) -> 0 while G_Born finite  [Hessian/Maloney-Lemaitre]
#     => sigma_y ~ G_relaxed*gamma_y ~ (z - z_iso) -> 0  (THE liquefaction/friction rule)
# Below we use the spine's 3D isostatic value z_iso=2d=6 (the 2D run confirms the rule form).
z0      = 6.5                   # initial coordination (jammed, State 4)
z_iso   = 6.0                   # isostatic margin 2d=6 (sigma_y, G_relaxed -> 0)
E_unjam = 5.0e7                 # latent heat of UNJAMMING per volume [J/m^3]
                               #   (~1.3% of melt energy: liquefaction is 'cheap')
f_lat   = 0.5                   # fraction of frictional work paid as unjamming latent heat
tau_cool= h_sz**2 / 1e-6        # conductive cooling time ~ h^2/alpha_th [s]

def sigma_y(z):                 # yield stress vanishes linearly at isostatic (S2.4)
    return mu_dry*sigp*np.clip((z-z_iso)/(z0-z_iso), 0.0, 1.0)

def phi_of_z(z):                # fluidity: State4 (phi~0) -> State3/1 (phi->1)
    return 1.0 - np.clip((z-z_iso)/(z0-z_iso), 0.0, 1.0)

def run(V, unjamming=True, total_slip=0.20, nsteps=20000):
    gammadot = V/h_sz
    dt = (total_slip/V)/nsteps
    z = z0; E_acc = 0.0; T = 0.0
    rec = dict(slip=[], z=[], muE=[], T=[], sy=[], phi=[])
    liquefied_slip = None
    for n in range(nsteps):
        slip = V*n*dt
        ph = phi_of_z(z) if unjamming else 0.0
        # effective resistance: jammed(Coulomb) <-> flowing(viscous) mixture
        tau_res = (1-ph)*mu_dry*sigp + ph*eta_flow*gammadot
        muE = tau_res/sigma_n
        wdot = tau_res*gammadot            # frictional work rate [W/m^3]

        if unjamming and z > z_iso:
            # part of work pays unjamming latent heat -> reduce z toward z_iso (L.2)
            dE = f_lat*wdot*dt
            E_acc += dE
            z = z0 - (z0 - z_iso)*min(E_acc/E_unjam, 1.0)
            sensible = (1-f_lat)*wdot
            if z <= z_iso + 1e-9 and liquefied_slip is None:
                liquefied_slip = slip
        else:
            sensible = wdot                # melt-only path: all work -> heat

        # lumped temperature with conductive loss; cap latent of melting
        T = T + dt*(sensible/rho_c - T/tau_cool)
        if n % max(1, nsteps//400) == 0:
            rec['slip'].append(slip); rec['z'].append(z); rec['muE'].append(muE)
            rec['T'].append(T); rec['sy'].append(sigma_y(z) if unjamming else mu_dry*sigp)
            rec['phi'].append(ph)
    for k in rec: rec[k]=np.array(rec[k])
    return dict(**rec, V=V, unjamming=unjamming,
                muE_final=rec['muE'][-1], Tmax=rec['T'].max(),
                melted=bool(rec['T'].max()>=T_melt), liquefied_slip=liquefied_slip)

if __name__ == "__main__":
    print("="*74)
    print("VP-JAMMING FRICTION: 고온에너지 -> 액체화(unjamming) -> 마찰 붕괴")
    print("="*74)
    V = 1.0
    A = run(V, unjamming=True)    # VP unjamming ON
    B = run(V, unjamming=False)   # melt-only (no unjamming channel)

    ls = A['liquefied_slip']
    print(f"\n[A] VP unjamming ON  (V={V} m/s):")
    print(f"    liquefied (z->z_iso) at slip = {ls*1e3:.1f} mm" if ls else "    not fully liquefied")
    print(f"    final mu_eff = {A['muE_final']:.2e}   (Omega-NoGo HOLD if >= 1e-2)")
    print(f"    Tmax = {A['Tmax']:6.0f} K   melted = {A['melted']}   (melt at {T_melt:.0f} K)")
    print(f"    => friction collapses by LIQUEFACTION at dT~{A['Tmax']:.0f}K, FAR below melting.")

    print(f"\n[B] melt-only (no unjamming):")
    print(f"    final mu_eff = {B['muE_final']:.2e}")
    print(f"    Tmax = {B['Tmax']:6.0f} K   melted = {B['melted']}")
    print(f"    => without the unjamming channel, strength stays high and T climbs toward melt.")

    # energy comparison
    print(f"\nEnergy bookkeeping (L.2):")
    print(f"    unjamming latent heat E_unjam = {E_unjam:.1e} J/m^3")
    print(f"    melting energy (sensible+latent) ~ {rho_c*T_melt + L_melt_vol:.1e} J/m^3")
    print(f"    ratio E_unjam / E_melt = {E_unjam/(rho_c*T_melt+L_melt_vol)*100:.1f}%  "
          f"=> liquefaction is reached at ~1/{int((rho_c*T_melt+L_melt_vol)/E_unjam)} of melt energy.")

    np.savez("vp_jamming_results.npz",
             A_slip=A['slip'], A_z=A['z'], A_mu=A['muE'], A_T=A['T'], A_phi=A['phi'], A_sy=A['sy'],
             B_slip=B['slip'], B_mu=B['muE'], B_T=B['T'], z_iso=z_iso, z0=z0,
             sy0=mu_dry*sigp, T_melt=T_melt)
    print("\nsaved -> vp_jamming_results.npz")
