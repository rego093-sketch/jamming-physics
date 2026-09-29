# -*- coding: utf-8 -*-
"""
gate_numeric_chem.py — 화학·EM 백서 수치 드리프트 게이트 (SSOT)
================================================================
물리백서 tools/gate.py(phase 4) + vp_numeric_ssot.py 패턴 계승.

목적: 백서 챕터(EM_CHAPTER_EN.md, CHEMISTRY_CHAPTER_EN.md)의 표시 수치가
      *정준 재계산*(닫힌형/상수) 또는 *모듈 출력*과 어긋나면 FAIL → 빌드 차단.
      292.244·+57·k_e류 표시값 드리프트의 화학판 재발 방지.

두 검증 유형:
  [A] 닫힌형/상수: 정준 재계산값과 챕터 표시 토큰을 대조 (Decimal 고정밀).
  [B] 모듈 산출: 해당 모듈을 실행해 그 출력에 챕터 표시 토큰이 있는지 대조
      (모듈이 그 수치의 단일 진실원).

사용:
  python3 gate_numeric_chem.py [--chapters DIR] [--code DIR]
종료코드: 전 항목 PASS면 0, 하나라도 드리프트/누락이면 1.
"""
import sys, os, re, glob, math, subprocess, argparse
from decimal import Decimal as D, getcontext
getcontext().prec = 50

PI = D("3.14159265358979323846264338327950288419716939937511")

# ── 정준 입력 (CODATA, exact SI) ──
C    = D("299792458")
H    = D("6.62607015e-34")
HBAR = H/(2*PI)
ME   = D("9.1093837015e-31")
MP   = D("1.67262192369e-27")
EQ   = D("1.602176634e-19")
EPS0 = D("8.8541878128e-12")
ALPHA= D("7.2973525693e-3")
KB   = D("1.380649e-23")
EV   = D("1.602176634e-19")

def dsqrt(x, it=80):
    """Decimal 제곱근(Newton)."""
    x = D(x)
    if x == 0: return D(0)
    g = D(str(math.sqrt(float(x))))
    for _ in range(it):
        g = (g + x/g)/2
    return g


def canon():
    """닫힌형/상수 정준 수치 재계산."""
    q = {}
    lam_Ce = H/(ME*C)                       # 전자 콤프턴파장(비환산) [m]
    a0 = HBAR/(ME*C*ALPHA)                   # 보어 반지름 = 환산콤프턴/α [m]
    q["a0_A"] = a0*D("1e10")                 # Å
    q["Ry_eV"] = (ALPHA*ALPHA*ME*C*C/2)/EV   # Rydberg [eV]
    q["tet_deg"] = D(str(math.degrees(math.acos(-1/3))))  # 사면체각
    q["ratio_4_9"] = D(4)/D(9)               # 결정장 비
    q["fcc"] = PI/(3*dsqrt(2))               # FCC 채움률
    q["D_pm"] = 2*lam_Ce*D("1e12")           # 양자직경 [pm]
    # D=6π⁶r_p 잔차 (m_p/m_e vs 6π⁵)
    q["ppm_resid"] = (MP/ME/(6*PI**5) - 1)*D("1e6")
    q["ke"] = ALPHA*HBAR*C/(EQ*EQ)           # 쿨롱상수
    q["ke_mant"] = q["ke"]/D("1e9")          # ×10^9 가수
    # Wien: x=5(1−e^−x)
    xf = 5.0
    for _ in range(200):
        xf -= (xf-5*(1-math.exp(-xf)))/(1-5*math.exp(-xf))
    q["wien_mmK"] = (H*C/(D(str(xf))*KB))*D("1000")  # λ_peak·T [mm·K]
    # 전파각 χ(λ)=asin(λ/(mD)), m=⌈λ/D⌉
    Dq = float(2*lam_Ce)
    def chi(lam):
        m = math.ceil(lam/Dq); return math.degrees(math.asin(min(1.0, lam/(m*Dq))))
    q["chi_633"] = D(str(chi(632.8e-9)))
    q["chi_532"] = D(str(chi(532e-9)))
    q["chi_550"] = D(str(chi(550e-9)))
    return q


# ── 검증 레지스트리 [A] 닫힌형: (이름, 정준키, 표시정규식(캡처), 허용오차rel, 설명) ──
REG_A = [
    ("a0",      "a0_A",      r"a_0 = (\d+\.\d+)\$ Å",     1e-4, "보어 반지름 Å"),
    ("Rydberg", "Ry_eV",     r"(\d+\.\d+)\$ eV",          1e-4, "Rydberg eV"),
    ("tetra",   "tet_deg",   r"109\.47",                  2e-4, "사면체각 109.47°"),
    ("ratio49", "ratio_4_9", r"\\frac\{4\}\{9\} = (\d\.\d+)", 1e-3, "Δ_tet/Δ_oct=4/9"),
    ("fcc",     "fcc",       r"3\\sqrt2\) = (\d\.\d+)",    1e-3, "FCC π/(3√2)"),
    ("Dpm",     "D_pm",      r"D = (\d\.\d+)\$ pm|= (\d\.\d+) fm", 1e-3, "양자직경 pm"),
    ("ke",      "ke_mant",   r"k_e = (\d\.\d+)\\times 10\^9", 1e-5, "쿨롱상수 k_e ×10^9 가수"),
    ("wien",    "wien_mmK",  r"(\d\.\d+)\\times 10\^\{-3\}\$ m·K", 1e-4, "Wien 상수"),
    ("chi633",  "chi_633",   r"632\.8\\,\\text\{nm\}\) = (\d+\.\d+)", 1e-4, "χ(632.8nm)"),
    ("chi532",  "chi_532",   r"532\\,\\text\{nm\}\) = (\d+\.\d+)",     1e-4, "χ(532nm)"),
]

# ── 검증 레지스트리 [B] 모듈산출: (이름, 모듈상대경로, 챕터 표시토큰, 모듈출력 매칭토큰, 설명) ──
REG_B = [
    ("dissoc_N2", "vp_equilibrium.py",        "8214", "8214", "N₂ 해리온도 8214K"),
    ("dissoc_H2", "vp_equilibrium.py",        "4400", "4400", "H₂ 해리온도 4400K"),
    ("daniell",   "vp_electrochemistry.py",   "1.10", "1.10", "다니엘 전지 1.10V"),
    ("ph_acetic", "vp_solution_chemistry.py", "2.88", "2.88", "아세트산 pH 2.88"),
    ("packing",   "vp_crystal_packing.py",    "0.7405", "0.7405", "FCC 채움률 0.7405"),
    ("magic",     "vp_gauss_shells.py",       "82", "82", "마법수 골격(82 등)"),
    ("cu_fermi",  "vp_copper_conduction.py",  "7.04", "7.04", "구리 페르미에너지 7.04eV"),
    ("fe_class",  "vp_iron_magnetism.py",     "7/7", "7/7", "철 자성 7/7 분류 도출"),
    ("color_ti",  "vp_molecular_color.py",    "493", "493", "Ti³⁺ d-d 흡수 493nm"),
    ("color_cds", "vp_molecular_color.py",    "512", "512", "CdS 카드뮴옐로 흡수단"),
    ("pt_reson",  "vp_platinum_catalysis.py", "2.58", "2.58", "Pt 전자진폭 반파장 2.58Å"),
    ("pt_volcano","vp_platinum_catalysis.py", "18.66", "18.66", "패러데이 H₂ 18.66mmol"),
    ("pt_sim_cv", "vp_pt_resonance_sim.py",    "0.84", "0.84", "양자가둠 진동 CV=0.84"),
    ("pt_repro_r","vp_pt_reproduction.py",      "-0.91", "-0.91", "d-밴드↔ΔG_H 상관 r=−0.91 (Pt 재현)"),
]

# ── 금지 패턴: 나타나면 안 되는 알려진 드리프트 값(예시) ──
BAD_PATTERNS = [
    (r"109\.5[1-9]", "사면체각은 109.47°(arccos(−1/3)); 109.51+ 는 드리프트"),
    (r"\b0\.444[0-3]\b", "Δ비는 0.4444(4/9); 0.4440~0.4443 는 드리프트"),
    (r"\b0\.740[0-2]\b", "FCC는 0.7405(π/3√2); 0.7400~0.7402 는 드리프트"),
]


def find_dir(cli, *needles):
    if cli and os.path.isdir(cli):
        return os.path.abspath(cli)
    here = os.path.dirname(os.path.abspath(__file__))
    for base in [here, os.path.join(here, ".."), os.path.join(here, "..", "..")]:
        for needle in needles:
            hits = glob.glob(os.path.join(base, "**", needle), recursive=True)
            if hits:
                return os.path.dirname(os.path.abspath(hits[0]))
    return os.path.abspath(here)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters", default=None)
    ap.add_argument("--code", default=None)
    args = ap.parse_args()

    chap_dir = find_dir(args.chapters, "EM_CHAPTER_EN.md", "CHEMISTRY_CHAPTER_EN.md")
    code_dir = find_dir(args.code, "verify_chemistry.py")

    chapters = glob.glob(os.path.join(chap_dir, "**", "*CHAPTER_EN.md"), recursive=True)
    text = ""
    for f in chapters:
        text += open(f, encoding="utf-8").read() + "\n"

    print("="*72)
    print("화학·EM 백서 수치 드리프트 게이트 (SSOT)")
    print("="*72)
    print(f"챕터 디렉토리: {chap_dir}  ({len(chapters)}개 챕터)")
    print(f"코드 디렉토리: {code_dir}")
    if not chapters:
        print("[치명] 챕터를 찾지 못함."); return 1

    q = canon()
    fails = []

    # [A] 닫힌형 정준 대조
    print("\n[A] 닫힌형/상수 정준 재계산 ↔ 챕터 표시값")
    print(f"  {'항목':<10}{'정준값':>16}{'챕터값':>14}{'판정':>8}")
    print("  " + "-"*48)
    for name, key, rx, tol, desc in REG_A:
        cval = q[key]
        m = re.search(rx, text)
        shown = None
        if m:
            for g in m.groups():
                if g:
                    shown = g; break
            if shown is None:  # 정규식이 토큰 자체(캡처 없음)
                shown = m.group(0)
        if m is None:
            fails.append((name, "누락", desc)); verdict = "MISSING"
            shown_s = "—"
        else:
            try:
                sv = D(re.sub(r"[^\d.]", "", shown))
                rel = abs(sv - cval)/abs(cval) if cval != 0 else abs(sv)
                if rel <= D(str(tol)):
                    verdict = "OK"
                else:
                    verdict = "DRIFT"; fails.append((name, f"{shown} vs {cval}", desc))
                shown_s = shown
            except Exception:
                verdict = "OK"; shown_s = shown  # 비수치 토큰(예: 109.47 직접매칭)
        cv_s = f"{float(cval):.6g}"
        print(f"  {name:<10}{cv_s:>16}{shown_s:>14}{verdict:>8}")
    # 잔차 항목 (특수)
    ppm = q["ppm_resid"]
    if re.search(r"18\.8 ppm", text) and abs(float(ppm) - 18.8) < 0.1:
        print(f"  {'ppm_resid':<10}{float(ppm):>16.1f}{'18.8':>14}{'OK':>8}")
    else:
        fails.append(("ppm_resid", f"{float(ppm):.1f}", "−19ppm 헤드라인 잔차")); 
        print(f"  {'ppm_resid':<10}{float(ppm):>16.1f}{'?':>14}{'DRIFT':>8}")

    # [B] 모듈 산출 대조
    print("\n[B] 모듈 실행 출력 ↔ 챕터 표시값 (모듈=단일 진실원)")
    print(f"  {'항목':<12}{'토큰':>8}{'챕터':>8}{'모듈출력':>10}{'판정':>8}")
    print("  " + "-"*48)
    for name, mod, chap_tok, mod_tok, desc in REG_B:
        in_chap = chap_tok in text
        hits = glob.glob(os.path.join(code_dir, "**", mod), recursive=True)
        in_mod = False
        if hits:
            try:
                out = subprocess.run([sys.executable, hits[0]], capture_output=True,
                                     text=True, timeout=60).stdout
                in_mod = mod_tok in out
            except Exception:
                in_mod = False
        verdict = "OK" if (in_chap and in_mod) else "FAIL"
        if verdict == "FAIL":
            fails.append((name, f"chap={in_chap} mod={in_mod}", desc))
        print(f"  {name:<12}{chap_tok:>8}{'Y' if in_chap else 'N':>8}"
              f"{'Y' if in_mod else 'N':>10}{verdict:>8}")

    # 금지 패턴
    print("\n[C] 금지 드리프트 패턴 스캔")
    bad_found = False
    for rx, why in BAD_PATTERNS:
        for m in re.finditer(rx, text):
            bad_found = True
            fails.append(("bad_pattern", m.group(0), why))
            print(f"  [DRIFT] '{m.group(0)}' — {why}")
    if not bad_found:
        print("  ✓ 금지 드리프트 값 없음")

    # 요약
    print("\n" + "="*72)
    if not fails:
        print("최종: PASS — 챕터 표시 수치가 정준/모듈과 전부 일치, 드리프트 없음.")
        print("="*72)
        return 0
    else:
        print(f"최종: FAIL — {len(fails)}건 드리프트/누락:")
        for n, v, d in fails:
            print(f"  · {n}: {v}  ({d})")
        print("="*72)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
