"""
c19_master_scale.py  --  master-scale 외삽 경계 (실험실 granular -> 3000 km 판)
================================================================================
목적 (신뢰도 강화, AR-1 과 동형):
  메커니즘은 실험실/시뮬 규모(cm 입자, 이상화된 2D frictionless disk)에서 세운
  granular jamming 물리에 기댄다. "이게 대륙 규모(1e6 m) 전단대에 적용되는가"는
  백서가 HOLD 로 둔 'master-scale 외삽' 간극(길이로 ~8-10 자릿수)이다.
  AR-1 과 같은 방식: 해결을 주장하지 않고 *경계*를 짓는다.
   (A) 어떤 무차원군(Π)이 규모 불변으로 전이되는가, 어떤 게 깨지는가 (Buckingham Π).
   (B) 연속체 극한: 입자 수 N->inf 가 만족되면 phi_J 의 유한크기 보정은 사라진다
       (즉 '큰 규모'가 오히려 깨끗한 극한이다 -- 통계가 문제가 아니다).
   (C) 핵심 하중 주장(낮은 mu_eff)은 *실험으로* 검증돼 있다 (Di Toro+ 2011 등):
       지진 속도(~1 m/s)+높은 수직응력에서 동적 약화 mu -> ~0.1, 完全 가압 시 훨씬↓.
       백서의 mu_eff=0.002 가 요구하는 조건을 정량화한다.
  판정: PASS 아닌 정직한 HOLD. 전이되는 부분과 안 되는 부분을 분리하고 반증가능화.
Pure numpy. Deterministic.
"""
import numpy as np

print("="*88)
print("C-19  MASTER-SCALE EXTRAPOLATION BOUNDS  (lab granular -> continental shear zone)")
print("="*88)

# ---- lab vs Earth conditions ----
# grain size, shear-zone thickness, slip velocity, normal stress, densities, moduli
lab   = dict(d=1e-3, h=2e-3, V=1.0, sigma_n=1e6,  rho=2.7e3)   # idealized HV friction lab
earth = dict(d=1e-4, h=3e-3, V=1.0, sigma_n=150e6, rho=2.7e3)  # lithospheric gouge
E_grain   = 5e10     # silicate grain modulus [Pa]
sigma_crush = 3e8    # aggregate grain-crushing stress scale [Pa] (~0.1-1 GPa)
mu_intrinsic = 0.6   # Byerlee dry friction
mu_eff_claim = 2.2e-3

def inertial_number(s):
    gdot = s['V']/s['h']
    return gdot*s['d']*np.sqrt(s['rho']/s['sigma_n'])

# ----------------------------------------------------------------------------
# (A) Dimensionless-group transfer  (which Π match lab<->Earth?)
# ----------------------------------------------------------------------------
print("\n[A] DIMENSIONLESS-GROUP TRANSFER (Buckingham Pi): what carries across scale?")
print("-"*88)
I_lab, I_earth = inertial_number(lab), inertial_number(earth)
print(f"  inertial number  I = gdot*d*sqrt(rho/sigma_n):  lab={I_lab:.2e}, earth={I_earth:.2e}")
print(f"     -> both I << 1  => DENSE/quasi-static granular regime in BOTH  [TRANSFERS]")
PiP_lab   = lab['sigma_n']/E_grain
PiP_earth = earth['sigma_n']/E_grain
print(f"  pressure/hardness sigma_n/E_grain:  lab={PiP_lab:.1e}, earth={PiP_earth:.1e}")
crush_lab   = lab['sigma_n']/sigma_crush
crush_earth = earth['sigma_n']/sigma_crush
print(f"  comminution ratio sigma_n/sigma_crush: lab={crush_lab:.2f}, earth={crush_earth:.2f}")
print(f"     -> earth crosses ~1 (grain crushing) while lab << 1  => REGIME DIFFERS [BREAKS]")
print("  Topological/critical quantities (phi_J, z_iso=2d, exponents G~(z-z_iso),")
print("  p~(phi-phi_J)) are scale-INVARIANT in the idealized limit  [TRANSFER, with caveats].")

# ----------------------------------------------------------------------------
# (B) Continuum limit: is the N->inf (clean) limit satisfied at Earth scale?
# ----------------------------------------------------------------------------
print("\n[B] CONTINUUM LIMIT: finite-size corrections to phi_J vanish as N->inf")
print("-"*88)
N_across = earth['h']/earth['d']
L_inplane = 1e6
N_total = (L_inplane/earth['d'])**2 * N_across
print(f"  grains across shear zone N_across = h/d = {N_across:.0f}  (thin: a localization caveat)")
print(f"  total grain count N_total ~ (L/d)^2 * N_across ~ {N_total:.0e}  (astronomically large)")
print(f"     -> phi_J finite-size correction ~ 1/N_total -> 0  => the LARGE scale is the CLEAN")
print(f"        limit for the jamming fraction; statistics is NOT the obstacle. [FAVORS transfer]")

# ----------------------------------------------------------------------------
# (C) Dimensionality + the LOAD-BEARING low-mu_eff: what experiment says
# ----------------------------------------------------------------------------
print("\n[C] DIMENSIONALITY & the load-bearing low friction (vs experiment)")
print("-"*88)
print("  phi_J value depends on dimension/regime, NOT used as a free win:")
print("    2D bidisperse frictionless ~ 0.842 (paper's value); 3D random close packing ~ 0.64.")
print("    A planar gouge zone is quasi-2D but grains are 3D -> the 0.842 vs 0.64 choice")
print("    must be justified or swept. [REGIME/dimensionality HOLD]")
# experimentally, dynamic weakening gives mu~0.1; mu_eff=0.002 needs near-lithostatic pore P:
lam_required = 1.0 - mu_eff_claim/mu_intrinsic   # mu_eff = mu*(1-lambda), lambda=Pp/sigma_n
mu_exp_typical = 0.1
weakening_exp = mu_intrinsic/mu_exp_typical
weakening_claim = mu_intrinsic/mu_eff_claim
print(f"  Experiment (Di Toro+ 2011; Tohoku <0.2; landslides 0.05-0.2): dynamic mu ~ {mu_exp_typical}")
print(f"     i.e. a ~{weakening_exp:.0f}x weakening is EXPERIMENTALLY CONFIRMED at sigma_n up to ~100 MPa, V~1 m/s.")
print(f"  Paper's mu_eff = {mu_eff_claim} is a ~{weakening_claim:.0f}x weakening -- at/*beyond* the experimental tail.")
print(f"     It is reachable ONLY in the near-complete liquefaction / thermal-pressurization limit:")
print(f"     mu_eff = mu*(1 - Pp/sigma_n)  =>  required Pp/sigma_n = lambda = {lam_required:.4f}")
print(f"     i.e. pore pressure within {100*(1-lam_required):.2f}% of lithostatic. EXTREME but well-defined,")
print(f"     and physically the SAME endpoint mainstream thermal-pressurization models reach (sigma'->0).")

# ----------------------------------------------------------------------------
# verdict + falsifier
# ----------------------------------------------------------------------------
print("\n[VERDICT]  master-scale = HOLD (honest), separated into transfer vs non-transfer")
print("-"*88)
print("  TRANSFERS: dense-granular regime (I<<1 both); continuum limit (N->inf clean);")
print("    the QUALITATIVE jamming/unjamming structure; the EXISTENCE of dramatic dynamic")
print("    weakening (experimentally confirmed at lithospheric sigma_n, V~1 m/s).")
print("  DOES NOT (yet) TRANSFER: the exact phi_J (2D 0.842 vs 3D 0.64; high-P; fractal gouge;")
print("    grain crushing) and especially mu_eff=0.002, which requires near-lithostatic pore")
print("    pressure (lambda~0.997) -- the load-bearing extreme. => master-scale is HOLD.")

print("\n[PRE-REGISTERED FALSIFIER]  (master-scale; lock in config/constraints.yml)")
print("-"*88)
print("  UNLOCK if high-P (sigma_n ~ 100 MPa), high-V (~1 m/s) gouge experiments OR natural")
print("    fault fabrics demonstrate SUSTAINED mu_eff <~ 0.01 (lambda >~ 0.98) over the required")
print("    displacement -- AND the comminution/fractal-gouge evolution matches the prediction.")
print("  FAIL if the lowest SUSTAINED mu_eff achievable at lithospheric conditions is >~ 0.1:")
print("    then the suction work cannot close (C16/C17 budgets fail) and the rapid branch is")
print("    rejected; the slow default is not displaced.")
print("  This gates the *magnitude*, not the existence, of weakening. It does not by itself")
print("  establish the timescale (chronology firewall remains separate).")

# ---- save (audited :: C19) ----
np.savez("c19_master_scale_results.npz",
         I_lab=I_lab, I_earth=I_earth, N_total=N_total, N_across=N_across,
         crush_lab=crush_lab, crush_earth=crush_earth,
         lam_required=lam_required, weakening_exp=weakening_exp, weakening_claim=weakening_claim,
         phi_2d=0.842, phi_3d=0.64)
print("\nsaved -> c19_master_scale_results.npz")
print(f"  AUDIT: I_earth={I_earth:.1e}<<1; N_total~{N_total:.0e}; sigma_n/sigma_crush(earth)={crush_earth:.2f}; "
      f"mu_eff=0.002 needs lambda={lam_required:.4f}")
