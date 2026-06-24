#!/usr/bin/env python3
"""
validate_all.py  --  ATL 재현 번들 단일 검증 runner (검수용)
=============================================================
각 물리 주장(claim)을 스크립트 출력/저장결과에 대해 기대값 + 공차로 검증하고
PASS / STOP 을 출력한다. 빠른 모듈은 즉석 재실행, 느린 잼밍 모듈은 저장된
results/*.npz 를 감사(재생성 명령은 LEDGER.md 참조).

usage:  python validate_all.py
"""
import sys, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE,"engine"))
RES=os.path.join(HERE,"results")

rows=[]
def check(claim, ok, detail):
    rows.append((claim, "PASS" if ok else "STOP", detail))

# ---- C1: VP jamming friction = liquefaction (mu_eff collapses, no melt) ----
try:
    import vp_jamming_friction as vj
    A=vj.run(V=1.0, unjamming=True); B=vj.run(V=1.0, unjamming=False)
    check("C1a VP-jamming liquefaction: mu_eff < Omega-NoGo 1e-2",
          A['muE_final']<1e-2, f"mu_eff={A['muE_final']:.2e}")
    check("C1b liquefaction below melting (no melt)",
          (not A['melted']) and A['Tmax']<1000, f"Tmax={A['Tmax']:.0f}K")
    check("C1c melt-only path DOES melt (contrast)",
          B['melted'], f"Tmax={B['Tmax']:.0f}K")
except Exception as e:
    check("C1 VP-jamming friction", False, f"ERROR {e}")

# ---- C2: thermal pressurization corroboration (undrained weakens, no melt) ----
try:
    import tp_dilatancy_prototype as tp
    o=tp.run(V=1.0, alpha_hy=1e-6)   # undrained baseline (fast single case)
    check("C2 TP corroboration: undrained weakening>50%, no melt",
          o['weakening']>0.5 and not o['melted'], f"weaken={o['weakening']*100:.0f}% Tmax={o['Tmax']:.0f}K")
except Exception as e:
    check("C2 TP corroboration", False, f"ERROR {e}")

# ---- C3: feasibility -- friction pinned by liquefaction => critical depth ~12 km ----
try:
    import feasibility_map as fm
    dc=fm.crit_depth(1.0,0.5,1e3,4e6)/1e3
    check("C3 coupled feasibility: critical depth in 8-20 km band",
          8<=dc<=20, f"crit depth={dc:.1f} km (Lambda~d^2)")
except Exception as e:
    check("C3 feasibility", False, f"ERROR {e}")

# ---- C4: jamming micro-derivation (audited from saved npz) ----
try:
    m=np.load(os.path.join(RES,"jamming_microderive_results.npz"))
    pj=float(m['phi_jam']); ziso=int(m['z_iso'])
    check("C4a jamming phi_jam ~ 0.84 (2D bidisperse)", abs(pj-0.84)<0.02, f"phi_jam={pj:.3f}")
    check("C4b isostatic z_iso = 2d", ziso==4, f"z_iso={ziso} (2D; 3D=6 spine)")
    # z above jam approaches z_iso
    Z=m['Z']; check("C4c z -> z_iso above jamming", Z[-1]>=ziso-0.2 and Z[-1]<6, f"z(phi_max)={Z[-1]:.2f}")
except Exception as e:
    check("C4 jamming micro-derivation", False, f"ERROR {e}")

# ---- C5: relaxed shear modulus -> 0 (friction-collapse rule), G_Born finite ----
try:
    s=np.load(os.path.join(RES,"jamming_shear_results.npz"))
    DZ=s['DZ']; GR=s['GR']; GB=s['GB']
    sl=np.polyfit(DZ,GR,1)[0]
    check("C5a G_relaxed << G_Born near jamming",
          GR[0]<0.5*GB[0], f"G_rel/G_Born={GR[0]/GB[0]:.2f} at z-z_iso={DZ[0]:.2f}")
    check("C5b G_relaxed increases with (z-z_iso) (->0 at iso)",
          sl>0, f"slope dG_rel/dDz={sl:.3f}")
    check("C5c G_Born stays finite O(0.1-1)", 0.05<GB.mean()<1.0, f"G_Born~{GB.mean():.2f}")
except Exception as e:
    check("C5 relaxed shear modulus", False, f"ERROR {e}")

# ---- C6: P8 magnetic stripes -- H0 (chronology) vs H2 (resonance) ----
try:
    p=np.load(os.path.join(RES,"p8_results.npz"))
    check("C6a P8: reversal barcode irregular (CV>0.5, not periodic)",
          float(p['cv_dur'])>0.5, f"CV(durations)={float(p['cv_dur']):.2f}")
    check("C6b P8: H2 resonance FAILS (spectrum broad & incoherent)",
          (not bool(p['H2_unlock'])) and float(p['concentration'])<0.5 and float(p['coh'])<0.5,
          f"concentration={float(p['concentration']):.2f}, coherence={float(p['coh']):+.2f}")
except Exception as e:
    check("C6 P8 magnetic stripes", False, f"ERROR {e}")

# ---- C7: C-3 logical trace -- stripe pattern degenerate under time-rescaling ----
try:
    cc=np.load(os.path.join(RES,"c3b_results.npz"))
    maxdiff=float(np.max(np.abs(cc['pos_std']-cc['pos_fast'])))
    check("C7 stripes degenerate under uniform time-compression (positions identical)",
          maxdiff<1e-6, f"max|pos diff|={maxdiff:.1e} km (slow-std vs 50x-compressed)")
except Exception as e:
    check("C7 stripe degeneracy", False, f"ERROR {e}")

# ---- C8: C-5 corrected -- relative-time stripes + physics-set thousands-of-yr timescale ----
try:
    v=np.load(os.path.join(RES,"c5_results.npz"))
    ratio=float(v['ratio_rel']); drive=v['drive_Pa']; tsz=float(v['tau_rejam_sz'])
    check("C8a stripes give a RELATIVE deceleration shape (early/late > 2)",
          ratio>2.0, f"relative early/late ratio = {ratio:.1f} (chronology-agnostic)")
    check("C8b thousands-of-yr opening is PHYSICS-PERMITTED (liquefied driving < 100 Pa)",
          float(np.max(drive))<100, f"driving stress {drive.min():.0f}-{drive.max():.0f} Pa for 1e4-1e3 yr")
    check("C8c brake = mm shear-zone re-jam is FAST (tau < 1e3 s) => self-limiting brief event",
          tsz<1e3, f"tau_rejam(mm)={tsz:.0f} s (vs lithosphere ~50 Myr: wrong layer)")
except Exception as e:
    check("C8 velocity history", False, f"ERROR {e}")

# ---- C9: jamming bistability -- a liquefied shear zone cannot creep slowly ----
try:
    b=np.load(os.path.join(RES,"jamming_bistability_results.npz"))
    Vc=float(b['Vc']); vw=b['vw']; tdays=float(b['t_cum_days'])
    v_cmyr=0.03/3.15e7
    check("C9a sustained liquefaction needs V>>cm/yr (no slow-liquefied state)",
          Vc/v_cmyr>1e6, f"V_crit={Vc:.2e} m/s ~ {Vc/v_cmyr:.0e}x cm/yr")
    check("C9b velocity-weakening region exists => unstable => stick-slip",
          bool(vw.any()), f"vw points={int(vw.sum())}")
    check("C9c cumulative sliding to open 3000 km is brief (<1 yr)",
          tdays<365, f"{tdays:.0f} days of actual slip (rest stuck)")
except Exception as e:
    check("C9 jamming bistability", False, f"ERROR {e}")

# ---- C10: trigger ΔR within Ω-NoGo ----
try:
    t=np.load(os.path.join(RES,"c2_results.npz"))
    di=float(t['dR_init']); dm=float(t['dR_mob']); ds=float(t['deltaR_stop'])
    check("C10 trigger: init & mobilization ΔR both < 50 km (Ω-NoGo)",
          di<ds and dm<ds, f"ΔR init={di/1e3:.1f} km, mobilize={dm/1e3:.0f} km < {ds/1e3:.0f} km")
except Exception as e:
    check("C10 trigger ΔR", False, f"ERROR {e}")

# ---- C11: P7 master gate -- material invariant (PASS) / system Λ scale-explicit (HOLD) ----
try:
    c=np.load(os.path.join(RES,"c4_results.npz"))
    dc=c['dcrit_km']; dlab=float(c['d_lab_needed'])
    check("C11a P7 scale prediction: d_crit shrinks with basin (Atlantic>RedSea>Afar)",
          dc[0]>dc[1]>dc[2], f"d_crit={dc[0]:.0f}/{dc[1]:.1f}/{dc[2]:.1f} km (Atl/Red/Afar)")
    check("C11b MASTER gate HOLD: system feasibility not lab-reproducible (needs absurd geom)",
          dlab>0.1, f"lab sample would need d={dlab:.2f} m at W=1cm (absurd) => HOLD not PASS")
except Exception as e:
    check("C11 master gate", False, f"ERROR {e}")

# ---- C12: full Ω-NoGo ----
try:
    o=np.load(os.path.join(RES,"omega_nogo_results.npz"))
    check("C12 Ω-NoGo: mechanism inside ALL limits (5/5)",
          int(o['npass'])==int(o['ntot']), f"{int(o['npass'])}/{int(o['ntot'])} limits PASS")
except Exception as e:
    check("C12 Ω-NoGo", False, f"ERROR {e}")

# ---- C13: P1 Atlantic-rim boundary character (data module) ----
try:
    p=np.load(os.path.join(RES,"p1_results.npz"))
    rb=float(p['R_sub_base']); rw=float(p['R_sub_worst']); ul=float(p['unlock']); sh=float(p['atl_share_global'])
    check("C13 P1: R_sub UNLOCK (<=0.25) even worst-case; passive-margin ocean",
          rw<ul, f"R_sub base={rb:.3f}, worst={rw:.3f} < {ul}; Atlantic={100*sh:.1f}% of global subduction")
except Exception as e:
    check("C13 P1 boundaries", False, f"ERROR {e}")

# ---- C14: P9 orogeny Deborah regime (cross-check; honest HOLD) ----
try:
    q=np.load(os.path.join(RES,"p9_results.npz"))
    Ds=float(q['De_standard']); Df=float(q['De_fast'])
    check("C14 P9: regime split correct (UHP viscous De<1; mechanism slip brittle De>1) => HOLD",
          Ds<1 and Df>1, f"De_standard={Ds:.1e} (<1 viscous), De_fast={Df:.1e} (>1 brittle)")
except Exception as e:
    check("C14 P9 orogeny", False, f"ERROR {e}")

# ---- C15: P7 field test -- does d_crit ~ sqrt(W) survive natural analogs? (honest) ----
try:
    c=np.load(os.path.join(RES,"c7_field_results.npz"), allow_pickle=True)
    rW=float(c['rho_W']); rC=float(c['rho_cold'])
    win_open = bool(np.all(c['d_crit'] < c['d_obs']))
    check("C15 P7 field test reproduces: depth is THERMAL (rho_cold>0.9), NOT width (rho_W<0.6); HOLD",
          rC>0.9 and rW<0.6 and win_open,
          f"rho(d,W)={rW:+.2f} (no sqrtW), rho(d,coldness)={rC:+.2f}; windows open => master gate HOLD")
except Exception as e:
    check("C15 P7 field test", False, f"ERROR {e}")

# ---- C16: unified energy ledger (heat real / conduction insufficient / advection testable) ----
try:
    e=np.load(os.path.join(RES,"c16_energy_ledger_results.npz"))
    fh=float(e['frac_heat']); dTc=float(e['dT_cond']); Tm=float(e['T_melt']); fl=float(e['fluid_km3'])
    check("C16a heat is a SMALL fraction of W_in (<20%); bulk is basin PE",
          fh<0.20, f"Q_fric/W_in={100*fh:.1f}%  (heat={fh*float(e['W_in']):.1e} J of {float(e['W_in']):.1e} J)")
    check("C16b conduction-only ΔT is melt-order (=> advection REQUIRED, not optional)",
          dTc>0.3*Tm, f"ΔT_cond~{dTc:.0f} K vs melt {Tm:.0f} K (3 kyr): conduction insufficient")
    check("C16c advective sink => LARGE, testable hydrothermal flux (>=1e4 km^3)",
          fl>=1e4, f"required fluid throughput ~{fl:.1e} km^3 (falsifiable P4-thermal magnitude)")
except Exception as ex:
    check("C16 energy ledger", False, f"ERROR {ex}")

# ---- C17: AR-1 energy-source audit (honest HOLD; candidates bounded) ----
try:
    s=np.load(os.path.join(RES,"c17_energy_source_results.npz"))
    check("C17a H-E1 (release of stored internal energy) is the ONLY admissible source class",
          bool(s['he1_ok']) and (not bool(s['he2_gen_ok'])) and (not bool(s['he3_ok'])),
          f"H-E1 admissible; H-E2-gen & H-E3 excluded")
    check("C17b H-E2 generation needs >>global heat flow (excluded as generation)",
          float(s['heat_mult_1kyr'])>10.0, f"need {float(s['heat_mult_1kyr']):.0f}x whole-Earth heat over 1 kyr")
    check("C17c H-E3 core-field energy is orders short (excluded as a source)",
          float(s['U_mag_strong'])<1e-3*float(s['W_in']),
          f"U_mag(strong)~{float(s['U_mag_strong']):.1e} J << W_in {float(s['W_in']):.0e} J")
except Exception as ex:
    check("C17 energy source", False, f"ERROR {ex}")

# ---- C18: P29 coherence statistics machinery (corrected null + LEE + N_eff + jackknife) ----
try:
    p=np.load(os.path.join(RES,"c18_p29_coherence_results.npz"))
    praw=float(p['p_raw']); plee=float(p['p_LEE']); nlee=float(p['N_LEE'])
    neff=float(p['N_eff']); nn=int(p['N']); ncl=int(p['nclass']); jw=float(p['jackknife_worst_p'])
    check("C18a look-elsewhere correction applied (N_LEE>1; p_LEE >= p_raw)",
          nlee>1.0 and plee>=praw-1e-12, f"N_LEE={nlee:.0f}, p_raw={praw:.2e} -> p_LEE={plee:.2e}")
    check("C18b independence accounting present (distinct proxy_class reported; N_eff <= N)",
          ncl>=1 and neff<=nn+1e-9, f"proxy_class={ncl}, N_eff={neff:.2f} of N={nn}")
    check("C18c jackknife fragility computed (valid prob; worst-case >= full-set p_LEE)",
          0.0<=jw<=1.0 and jw>=plee-1e-9, f"jackknife worst p_LEE={jw:.2e} >= full {plee:.2e}")
except Exception as ex:
    check("C18 P29 coherence machinery", False, f"ERROR {ex}")

# ---- C19: master-scale extrapolation bounds (transfer vs non-transfer; honest HOLD) ----
try:
    m=np.load(os.path.join(RES,"c19_master_scale_results.npz"))
    Ie=float(m['I_earth']); Nt=float(m['N_total']); ce=float(m['crush_earth']); lam=float(m['lam_required'])
    check("C19a dense-granular regime transfers (inertial number I<<1 at Earth scale)",
          Ie<1e-2, f"I_earth={Ie:.1e} << 1 (quasi-static/dense; same regime as lab)")
    check("C19b continuum limit clean (N_total>>1 => phi_J finite-size correction ->0)",
          Nt>1e12, f"N_total~{Nt:.0e}; large scale is the CLEAN jamming-fraction limit")
    check("C19c load-bearing mu_eff=0.002 is bounded: needs near-lithostatic pore P (honest HOLD)",
          0.99<lam<1.0 and ce>0.1, f"lambda_req={lam:.4f} (Pp within {100*(1-lam):.2f}% lithostatic); sigma_n/sigma_crush={ce:.2f} (crushing regime differs)")
except Exception as ex:
    check("C19 master-scale bounds", False, f"ERROR {ex}")

# ---- report ----
print("="*78)
print("ATL REPRODUCIBILITY BUNDLE -- VALIDATION LEDGER")
print("="*78)
w=max(len(r[0]) for r in rows)
npass=sum(1 for r in rows if r[1]=="PASS")
for c,v,d in rows:
    print(f"  [{v}] {c:<{w}}  | {d}")
print("-"*78)
print(f"  {npass}/{len(rows)} PASS")
print("="*78)
sys.exit(0 if npass==len(rows) else 1)
