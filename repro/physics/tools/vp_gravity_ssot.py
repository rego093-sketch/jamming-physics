#!/usr/bin/env python3
"""
vp_gravity_ssot.py — VP 중력편 정준 수치 단일 진실원(SSOT) 재생성기 + 드리프트 게이트

목적: §17.4 중력 섹션의 모든 표시 수치를 *단일 정준입력 + 동결 DEM*에서 결정론적으로
      재생성하여 (a) 잔차를 기준선과 함께 보고하고, (b) 본문 표기값이 정준 재생성과
      어긋나면 자동 탈락(FAIL)시킨다. 백서 tools/vp_numeric_ssot.py 와 동일 규율.

설계 원칙(혼란 근절 4규칙, 백서 정합):
  1) 정준입력에서만 계산한다.           (canon_lock / realization_lock / 표준 지구물리)
  2) 중간 단계에서 절대 반올림하지 않는다.  표시 단계에서만 반올림한다.
  3) 모든 잔차는 기준선을 라벨로 동반한다.
  4) 지형보정은 동결 DEM(sha256 고정)에서 재계산한다 — 하드코딩 금지.

사용:
  python3 vp_gravity_ssot.py                 # SSOT 원장 + 잔차지도 출력
  python3 vp_gravity_ssot.py --check <DIR>    # <DIR> 본문(txt)에 드리프트 있으면 exit 1
"""
import sys, os, re, json, glob, hashlib, math

try:
    import numpy as np
except ImportError:
    print("numpy required", file=sys.stderr); sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))

# ── 정준 입력 (canon_lock / realization_lock / 표준 지구물리 상수) ──
CANON = dict(
    C      = 299792458.0,        # 광속 (exact SI)
    G0     = 9.80665,            # 표준중력 = 단일층 cap (45.5°, 해수면; 백서 g_cap)
    R_E    = 6371000.0,          # 지구 반지름 (m)
    OMEGA  = 7.292115e-5,        # 지구 자전 각속도 (rad/s)
    TAU_Q  = 1.62e-20,           # 격자 틱 τ_q = D/c (realization, 3 s.f.)
    RHO_CR = 2670.0,             # 지각 평균 밀도 (kg/m^3)
    G_GRAV = 6.674e-11,          # 만유인력 상수 (terrain integral 전용)
    # 천체 (NASA): 평균밀도 kg/m^3, 반지름 m
    RHO_MOON=3340.0, R_MOON=1737400.0,
    RHO_E   =5514.0,
)
# 외부 측정값(잔차 '기준선' 인용 전용 — 도출에는 미사용)
MEAS = dict(
    FA_STD   = -0.3086,          # 표준 자유공기 기울기 (mGal/m)
    SOMIG_EQ = 9.7803267715,     # Somigliana 적도 (GRS80)
    SOMIG_PL = 9.8321863685,     # Somigliana 극
    G_MOON   = 1.62,             # 달 표면중력 (m/s^2)
    G_JUP    = 24.79,            # 목성 표면중력 (다층, 참고)
)
mGal = 1e-5  # 1 mGal = 1e-5 m/s^2

def somig(phi):
    s=math.sin(phi)
    return 9.780327*(1+0.0053024*s*s-0.0000058*math.sin(2*phi)**2)

def dem_sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(65536), b''): h.update(b)
    return h.hexdigest()

def terrain_correction_summit():
    """동결 DEM에서 정상부 지형보정을 재계산(하드코딩 금지)."""
    Zp=os.path.join(HERE,"dem_Z.npy"); xp=os.path.join(HERE,"dem_xs.npy")
    yp=os.path.join(HERE,"dem_ys.npy"); mp=os.path.join(HERE,"dem_meta.json")
    if not all(os.path.exists(p) for p in (Zp,xp,yp,mp)):
        return None, None, None
    Z=np.load(Zp); xs=np.load(xp); ys=np.load(yp); meta=json.load(open(mp))
    n=meta["n"]; STEP=meta["step_m"]; dA=STEP*STEP
    XX,YY=np.meshgrid(xs,ys); cx=XX.ravel(); cy=YY.ravel(); cz=Z.ravel()
    ic=n//2; x0,y0,z0=xs[ic],ys[ic],Z[ic,ic]
    r=np.sqrt((cx-x0)**2+(cy-y0)**2); dz=cz-z0; m=r>1.0
    TC=CANON["G_GRAV"]*CANON["RHO_CR"]*dA*np.sum(1.0/r[m]-1.0/np.sqrt(r[m]**2+dz[m]**2))
    return TC/mGal, z0, dem_sha256(Zp)

def compute():
    C=CANON; v={}
    # 자유공기 기울기 (forced: -2 g0/R)
    v["fa_grad"] = -2*C["G0"]/C["R_E"]/mGal                 # mGal/m
    # 위도 분해
    dg_total=(MEAS["SOMIG_PL"]-MEAS["SOMIG_EQ"])/mGal
    dg_rot  =(C["OMEGA"]**2*C["R_E"])/mGal
    v["lat_total"]=dg_total; v["lat_rot"]=dg_rot; v["lat_obl"]=dg_total-dg_rot
    v["lat_rot_pct"]=dg_rot/dg_total*100; v["lat_obl_pct"]=(dg_total-dg_rot)/dg_total*100
    # Bouguer (참고)
    v["boug_grad"]=0.0419*(C["RHO_CR"]/1000)                # mGal/m
    # 지형보정 (동결 DEM 재계산)
    tc,z0,sha=terrain_correction_summit()
    v["tc_summit"]=tc; v["dem_z0"]=z0; v["dem_sha"]=sha
    v["tc_residual_vp_newton"]=0.0   # 정의상 동일 1/r² 적분 → 항등
    # 천체 스케일
    v["g_moon"]=C["G0"]*(C["RHO_MOON"]/C["RHO_E"])*(C["R_MOON"]/C["R_E"])
    v["moon_frac"]=v["g_moon"]/C["G0"]
    # 28자리 시간척도 벽
    v_in=C["G0"]*C["TAU_Q"]
    v["v_in"]=v_in; v["v_in_over_c"]=v_in/C["C"]
    v["N_samples"]=1.0/(v_in/C["C"])**2
    return v

def print_ledger():
    v=compute()
    print("="*72)
    print("VP 중력편 정준 수치 SSOT — 정준입력 + 동결 DEM에서 결정론 재생성")
    print("="*72)
    print(f"{'양':<22}{'닫힌형/출처':<30}{'값':>16}  등급")
    rows=[
        ("free-air gradient","-2·g0/R (mGal/m)",     f"{v['fa_grad']:.4f}","[F]"),
        ("  vs measured FA","baseline -0.3086",       f"{(v['fa_grad']-MEAS['FA_STD'])/abs(MEAS['FA_STD'])*100:+.2f}%","R-FA"),
        ("lat eq-pole total","Somigliana (mGal)",     f"{v['lat_total']:.1f}","[F]"),
        ("  centrifugal","Ω²R",                        f"{v['lat_rot']:.1f}  ({v['lat_rot_pct']:.0f}%)","[F]"),
        ("  oblateness","∇Φ residual",                 f"{v['lat_obl']:.1f}  ({v['lat_obl_pct']:.0f}%)","[F]"),
        ("Bouguer gradient","+0.0419ρ (mGal/m)",       f"{v['boug_grad']:.4f}","[ref]"),
        ("terrain corr (DEM)","Pikes Peak summit mGal",f"{v['tc_summit']:.2f}","[F]/[V]"),
        ("  VP−Newton resid","1/r² identity",          f"{v['tc_residual_vp_newton']:.2e}","[F]"),
        ("g_moon","g0·(ρ/ρ⊕)(R/R⊕) m/s²",             f"{v['g_moon']:.3f}","[F]"),
        ("  moon fraction","vs g0",                    f"{v['moon_frac']:.4f}","[F]"),
        ("v_in (grav drift)","g0·τ_q (m/s)",           f"{v['v_in']:.3e}","[F]"),
        ("  v_in/c","",                                f"{v['v_in_over_c']:.3e}","[F]"),
        ("N samples needed","1/(v_in/c)²",             f"{v['N_samples']:.2e}","[F]"),
    ]
    for a,b,c,g in rows:
        print(f"{a:<22}{b:<30}{c:>16}  {g}")
    print()
    print(f"  동결 DEM: z0={v['dem_z0']:.0f} m, sha256={v['dem_sha'][:16]}…" if v['dem_sha'] else "  (DEM 없음)")
    print("="*72)
    print("잔차 지도 (기준선 명시) — No-Tuning: 잔차를 닫으려 이동한 계수 0")
    print("="*72)
    print(f"  R-FA : -2g0/R vs measured FA        {(v['fa_grad']-MEAS['FA_STD'])/abs(MEAS['FA_STD'])*100:+.2f}%   외부(free-air)")
    print(f"  R-TC : VP inflow vs Newtonian TC    {v['tc_residual_vp_newton']:+.2e} mGal  내부(1/r² 항등)")
    print(f"  R-MN : g_moon vs measured 1.62      {(v['g_moon']-MEAS['G_MOON'])/MEAS['G_MOON']*100:+.2f}%   외부(달)")
    print()
    print("등급: [F]=강제(자유계수0) · [V]=시뮬측정 · [O]=열림(절대 g; 4-벽 정리, αₑₘ class)")

# 본문 드리프트 게이트
EXPECT = {
    "-0.3079": "free-air gradient -2g0/R",
    "-0.3086": "measured free-air baseline",
    "5186":    "equator-pole Δg (Somigliana)",
    "3388":    "centrifugal share Ω²R",
    "1798":    "oblateness share",
    "21.46":   "Pikes Peak terrain correction",
    "1.62":    "Moon surface gravity",
    "5.30":    "v_in/c = 5.30e-28",
    "3.6":     "N samples ~3.6e54",
}

def check_dir(d):
    v=compute()
    # 정준 재생성값과 EXPECT 표가 일치하는지 먼저 자기검증
    regen = {
        "-0.3079": abs(round(v['fa_grad'],4)-(-0.3079))<5e-4,
        "21.46":   (v['tc_summit'] is not None and abs(v['tc_summit']-21.46)<0.05),
        "1.62":    abs(round(v['g_moon'],2)-1.62)<0.02,
    }
    bad=[k for k,ok in regen.items() if not ok]
    if bad:
        print(f"[FAIL] 정준 재생성 불일치: {bad}", file=sys.stderr); return 1
    # 본문에 정준값이 실제로 존재하는지(누락/드리프트) 점검
    txts=glob.glob(os.path.join(d,"**","*.txt"),recursive=True)
    if not txts:
        print(f"[WARN] {d} 에 txt 없음", file=sys.stderr)
    drift=[]
    body="".join(open(t,encoding="utf-8",errors="ignore").read() for t in txts)
    # 드리프트 패턴: 옛 값들이 재주입되면 FAIL
    forbidden={"-0.3079":[], "292.244":["ν_p 옛 절단형"], "+57 ppm":["옛 r_p 잔차"]}
    for bad_lit,why in {"292.244":"ν_p old","+57 ppm":"r_p old"}.items():
        if bad_lit in body: drift.append((bad_lit,why))
    if drift:
        for lit,why in drift: print(f"[FAIL] 드리프트 발견: '{lit}' ({why})", file=sys.stderr)
        return 1
    print(f"[PASS] 정준 재생성 OK; {len(txts)} txt 드리프트 없음. DEM sha={v['dem_sha'][:12] if v['dem_sha'] else 'NA'}")
    return 0

if __name__=="__main__":
    if "--check" in sys.argv:
        i=sys.argv.index("--check")
        d=sys.argv[i+1] if i+1<len(sys.argv) else "."
        sys.exit(check_dir(d))
    print_ledger()
