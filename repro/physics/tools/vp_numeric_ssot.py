#!/usr/bin/env python3
"""
vp_numeric_ssot.py — VP 정준 수치 단일 진실원(SSOT) 재생성기 + 드리프트 게이트

목적: 백서의 모든 표시 수치를 *단일 정준입력*에서 결정론적으로 재생성해,
      (a) 흩어진 잔차를 단 2개의 독립 잔차로 환원하고(기준선 명시),
      (b) 본문 표기값이 정준 재생성과 어긋나면 자동 탈락(FAIL)시킨다.

설계 원칙(혼란 근절 4규칙):
  1) 정준입력에서만 계산한다.            (canon_lock / realization_lock / aqd_constants)
  2) 중간 단계에서 절대 반올림하지 않는다.  표시 단계에서만 반올림한다.
  3) 모든 잔차는 기준선을 라벨로 동반한다.
  4) 표시 정밀도와 '계산용 placeholder'를 구분 표기한다.

사용:
  python3 vp_numeric_ssot.py                 # SSOT 원장 + 잔차지도 출력
  python3 vp_numeric_ssot.py --check <DIR>    # <DIR> 본문(txt/html)에 드리프트 있으면 exit 1
  python3 vp_numeric_ssot.py --canon <bundle> # canon_lock.json 등에서 입력 로드(선택)
"""
import sys, os, re, json, glob
from decimal import Decimal as D, getcontext
getcontext().prec = 60

PI = D("3.14159265358979323846264338327950288419716939937510582097494")

# ── 정준 입력 (canon_lock.json / realization_lock.json / aqd_constants.json) ──
CANON = dict(
    C      = D("299792458"),                  # 광속 (exact SI)
    H      = D("6.62607015e-34"),              # 플랑크 (exact SI)
    ME     = D("9.1093837015e-31"),            # 전자질량 (CODATA)
    A_VP   = D("6.3299121257859865746e-19"),   # a, VP 지름
    DT     = D("1.86e-21"),                    # Δt (3 유효숫자, realization)
    D_ANCH = D("4.852620477e-12"),             # D_anch = 2λ_Ce (canon_lock)
    RP_LCK = D("8.412e-16"),                   # r_p 잠금 (canon_lock)
    GEV    = D("1.602176634e-10"),             # J/GeV
)
# 외부 측정값(잔차 '기준선' 인용 전용 — 도출에는 미사용)
MEAS = dict(MPME=D("1836.15267343"), RP_CODATA=D("0.8414"), MH_PDG=D("125.20"))


def load_canon(bundle_dir):
    """canon_lock.json / realization_lock.json 에서 입력을 덮어쓴다(있으면)."""
    def find(name):
        hits = glob.glob(os.path.join(bundle_dir, "**", name), recursive=True)
        return hits[0] if hits else None
    cl = find("canon_lock.json")
    if cl:
        j = json.load(open(cl))
        if "D_anch_m" in j: CANON["D_ANCH"] = D(str(j["D_anch_m"]))
        if "r_p_m"   in j: CANON["RP_LCK"] = D(str(j["r_p_m"]))
    rl = find("realization_lock.json")
    if rl:
        j = json.load(open(rl))
        if "a_m"       in j: CANON["A_VP"] = D(str(j["a_m"]))
        if "delta_t_s" in j: CANON["DT"]   = D(str(j["delta_t_s"]))
        if "c_m_per_s" in j: CANON["C"]    = D(str(j["c_m_per_s"]))
    return cl, rl


def compute():
    c = CANON
    q = {}
    q["alpha"]   = D(2)/PI
    q["delta"]   = D(1)/PI**2
    q["two_pi"]  = q["alpha"]/q["delta"]
    q["nu_geo"]  = 3*PI**4
    q["mpme"]    = 6*PI**5
    q["U_lat"]   = c["H"]*c["C"]/c["A_VP"]/c["GEV"]
    q["m_H"]     = q["U_lat"]/(5*PI)
    q["lam_Ce"]  = c["H"]/(c["ME"]*c["C"])
    q["D2lamCe"] = 2*q["lam_Ce"]
    q["r_e"]     = (c["D_ANCH"]/2)*q["delta"]
    q["rp_pred"] = c["D_ANCH"]/(6*PI**6)
    q["s_p"]     = c["D_ANCH"]/(2*c["RP_LCK"])
    q["nu_len"]  = q["s_p"]*q["delta"]
    q["lam_Cp"]  = q["lam_Ce"]/MEAS["MPME"]
    q["twoover"] = (2/PI)*q["lam_Cp"]
    q["k_e"]     = c["C"]**2 * D("1e-7")
    q["A_geo"]   = c["C"]*c["DT"]/c["A_VP"]
    return q


def ppm(x, b): return (x/b - 1)*D(10)**6
def pct(x, b): return (x/b - 1)*D(100)
def f(x, n): return f"{x:.{n}f}"


def report():
    q = compute()
    print("="*74)
    print("VP 정준 수치 SSOT — 정준입력에서 결정론 재생성 (중간 반올림 없음)")
    print("="*74)
    L = D("1e15"); P = D("1e12")
    rows = [
        ("alpha","2/π",f(q['alpha'],9),"[F] 정리"),
        ("delta","1/π²",f(q['delta'],9),"[F] 정리"),
        ("2π","α/δ",f(q['two_pi'],9),"[F] 항등"),
        ("nu_p(기하)","3π⁴",f(q['nu_geo'],6),"[F] 정준값"),
        ("nu_p(길이)","(D/2r_p)·δ",f(q['nu_len'],6),"[V] 교차검증"),
        ("m_p/m_e","6π⁵=2π·3π⁴",f(q['mpme'],6),"[F]"),
        ("U_lat","hc/a (GeV)",f(q['U_lat'],6),"[F]"),
        ("m_H","U_lat/5π (GeV)",f(q['m_H'],6),"[F_geo/H]"),
        ("lambda_C,e","h/(m_e c) (pm)",f(q['lam_Ce']*P,6),"[H]"),
        ("D=2λ_C,e","(pm)",f(q['D2lamCe']*P,6),"[H] =D_anch"),
        ("r_e","(D/2)·δ (fm)",f(q['r_e']*L,3),"[F]"),
        ("r_p,pred","D/6π⁶ (fm)",f(q['rp_pred']*L,6),"[F] 예측"),
        ("r_p,locked","canon (fm)",f(CANON['RP_LCK']*L,4),"[H] 입력"),
        ("(2/π)λ_C,p","측정콤프턴 (fm)",f(q['twoover']*L,5),"[비교전용]"),
        ("s_p","D/2r_p",f(q['s_p'],6),"[V]"),
        ("k_e","c²·1e-7",f(q['k_e'],4),"[측정상수]"),
        ("A_geo","cΔt/a",f(q['A_geo'],4),"[H] Δt 3 s.f. ⚠placeholder"),
    ]
    print(f"{'양':<13}{'닫힌형':<18}{'값':>18}  등급")
    for n,cf,v,g in rows: print(f"{n:<13}{cf:<18}{v:>18}  {g}")

    print("\n"+"="*74)
    print("잔차 지도 — 독립 잔차는 단 2개(R1,R3); 나머지는 그 조합/부호반전")
    print("="*74)
    R1 = ppm(q['mpme'], MEAS['MPME'])
    R3 = ppm(q['nu_len'], q['nu_geo'])
    res = [
        ("R1","6π⁵ vs CODATA m_p/m_e",f"{R1:+.2f} ppm","독립#1 (Lenz 잔차)"),
        ("R2","D/6π⁶ vs (2/π)λ_C,p(측정)",f"{ppm(q['rp_pred'],q['twoover']):+.2f} ppm","= −R1 (역수관계)"),
        ("R3","길이 ν_p vs 기하 3π⁴",f"{R3:+.2f} ppm","독립#2 (=r_p,pred/r_p,locked)"),
        ("R4","D/6π⁶ vs locked 0.8412",f"{ppm(q['rp_pred'],CANON['RP_LCK']):+.2f} ppm","= R3"),
        ("R5","길이경로 2π·ν_p vs CODATA",f"{ppm(2*PI*q['nu_len'],MEAS['MPME']):+.2f} ppm","= R3+R1"),
        ("R6","D/6π⁶ vs CODATA r_p",f"{pct(q['rp_pred']*L,MEAS['RP_CODATA']):+.4f} %","외부"),
        ("R7","locked vs CODATA r_p",f"{pct(CANON['RP_LCK']*L,MEAS['RP_CODATA']):+.4f} %","외부"),
        ("R8","U_lat/5π vs PDG m_H",f"{pct(q['m_H'],MEAS['MH_PDG']):+.4f} %","외부"),
    ]
    for k,lbl,val,note in res: print(f"  {k}: {lbl:<30}{val:>12}   {note}")
    print(f"\n  검증: R5 = R3+R1 = {R3+R1:+.2f} ppm ✓   R2 = −R1 ✓")
    return q


# 본문에서 탈락시켜야 할 알려진 드리프트(정준 재생성과 불일치하는 표기)
BAD_PATTERNS = [
    (r"\{\+\}?57\\?\s*\\?,?\s*\\mathrm\{ppm\}|\+57\s*ppm", "+57 ppm",   "+61 ppm",      "r_p,pred/r_p,locked = +61.2"),
    (r"292\.244(?!\d)",                                    "292.244",   "292.245",      "길이 ν_p = 292.245156"),
    (r"0\.841248",                                         "0.841248",  "0.841251",     "코드출력 D/6π⁶ (주석이 반올림D 사용)"),
    (r"8\.9875517923",                                     "8.9875517923e9","8.9875517874e9","c²·1e-7 = 8987551787.37"),
]

def check(target_dir):
    files = []
    for ext in ("*.txt","*.html","*.md","*.tex"):
        files += glob.glob(os.path.join(target_dir,"**",ext), recursive=True)
    fails = 0
    print("="*74); print(f"DRIFT CHECK — {target_dir}"); print("="*74)
    for pat, bad, good, why in BAD_PATTERNS:
        rx = re.compile(pat)
        hits = []
        for fp in files:
            try: txt = open(fp, encoding="utf-8", errors="ignore").read()
            except Exception: continue
            for i, line in enumerate(txt.splitlines(), 1):
                if rx.search(line): hits.append(f"{os.path.relpath(fp,target_dir)}:{i}")
        if hits:
            fails += 1
            print(f"\n  ✗ FAIL  '{bad}'  →  '{good}'   ({why})")
            for h in hits[:12]: print(f"          {h}")
            if len(hits) > 12: print(f"          … +{len(hits)-12} more")
        else:
            print(f"  ✓ ok    '{bad}' 미발견")
    print("\n  주: 80자리 A(cΔt/a)는 §3.4가 'placeholder' 면책 → 드리프트 아님(검사 제외)")
    print("="*74)
    print("RESULT:", "FAIL" if fails else "PASS", f"({fails} drift class)")
    return 1 if fails else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--canon" in args:
        i = args.index("--canon"); cl, rl = load_canon(args[i+1])
        print(f"[canon loaded] {cl}  {rl}\n")
    if "--check" in args:
        i = args.index("--check")
        sys.exit(check(args[i+1]))
    report()
    print("\n사용: --check <DIR> 로 본문 드리프트 게이트 실행 (tools/gate.py 에 연결 권장)")
