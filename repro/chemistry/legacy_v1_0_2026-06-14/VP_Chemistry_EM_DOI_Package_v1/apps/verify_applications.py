# -*- coding: utf-8 -*-
"""
verify_applications.py — VP 화학 응용 패키지 검증 하니스 (Stream E2)
==================================================================
촉매·비료·물정수·ESS·신소재 6개 모듈 + 케이스 원장을 한 번에 재검증한다.
물리 백서의 verify_chemistry.py 정신: 실행·결정론·표준라이브러리·원장 무결성.

검증 항목:
  [A] 실행 — 6개 모듈 무오류 실행 (assert 내장 전부 통과).
  [B] 결정론 — 각 모듈 2회 실행 stdout sha256 동일.
  [C] 표준라이브러리 전용 — math 외 import 없음.
  [D] 원장 무결성 — 3개 cases CSV 스키마·등급·스크립트 참조 일치.

실행: python3 verify_applications.py
종료코드 0 = 전부 PASS.
"""
import subprocess, sys, hashlib, csv, os, re

MODULES = ["vp_dband_catalysis.py", "vp_ammonia_synthesis.py", "vp_water_electrolysis.py",
           "vp_magnet_desalination.py", "vp_ess_thermal.py", "vp_new_materials.py",
           "vp_ess_thermoelectric.py", "vp_ess_ac_condenser.py", "vp_co2_reduction.py"]
LEDGERS = ["cases_catalysis.csv", "cases_water.csv", "cases_energy_materials.csv", "cases_co2.csv"]
ALLOWED_IMPORTS = {"math", "import math", "from math"}
VALID_GRADES = {"F", "F?", "CAL", "V", "H", "O", "refuted"}
HERE = os.path.dirname(os.path.abspath(__file__))


def run(mod):
    """모듈 실행 → (성공여부, stdout)."""
    p = subprocess.run([sys.executable, os.path.join(HERE, mod)],
                       capture_output=True, text=True)
    return p.returncode == 0, p.stdout


def main():
    print("=" * 64)
    print("VP 화학 응용 패키지 — 검증 하니스 (촉매·비료·물정수·ESS·신소재)")
    print("=" * 64)
    ok_all = True

    # [A] 실행 + [B] 결정론
    print("\n[A] 실행 · [B] 결정론 (2회 sha256)")
    print("-" * 64)
    for m in MODULES:
        ok1, out1 = run(m)
        ok2, out2 = run(m)
        h1 = hashlib.sha256(out1.encode()).hexdigest()[:12]
        h2 = hashlib.sha256(out2.encode()).hexdigest()[:12]
        det = (h1 == h2)
        exe = ok1 and ok2
        ok_all &= exe and det
        print(f"  {m:<28} 실행 {'OK ' if exe else 'FAIL'} · 결정론 {'OK' if det else 'FAIL'} ({h1})")

    # [C] 표준라이브러리 전용
    print("\n[C] 표준라이브러리 전용 (math 외 import 없음)")
    print("-" * 64)
    for m in MODULES:
        src = open(os.path.join(HERE, m), encoding="utf-8").read()
        imports = re.findall(r'^(?:import|from)\s+(\w+)', src, re.M)
        bad = [i for i in imports if i not in {"math", "subprocess", "sys", "hashlib", "csv", "os", "re"}
               and i != "math"]
        # 응용 모듈은 math만 허용
        bad = [i for i in imports if i != "math"]
        ok = (len(bad) == 0)
        ok_all &= ok
        print(f"  {m:<28} {'OK (math만)' if ok else 'FAIL: ' + ','.join(bad)}")

    # [D] 원장 무결성
    print("\n[D] 케이스 원장 무결성 (스키마·등급·스크립트 참조)")
    print("-" * 64)
    header = ["domain", "system", "vp_principle", "quantity", "predicted",
              "measured", "residual", "grade", "script", "note"]
    total_rows = 0
    modset = set(MODULES)
    for L in LEDGERS:
        path = os.path.join(HERE, L)
        with open(path, encoding="utf-8") as f:
            rows = list(csv.reader(f))
        hdr_ok = (rows[0] == header)
        body = rows[1:]
        grades_ok = all(r[7] in VALID_GRADES for r in body if len(r) >= 8)
        scripts_ok = all(r[8] in modset for r in body if len(r) >= 9)
        ok = hdr_ok and grades_ok and scripts_ok
        ok_all &= ok
        total_rows += len(body)
        print(f"  {L:<30} {len(body):>2}행 · 스키마 {'OK' if hdr_ok else 'X'} · "
              f"등급 {'OK' if grades_ok else 'X'} · 스크립트 {'OK' if scripts_ok else 'X'}")
    print(f"  {'합계':<30} {total_rows}행")

    # 종합
    print("\n" + "=" * 64)
    if ok_all:
        print(f"결과: ALL PASS — 모듈 {len(MODULES)}/{len(MODULES)} · 원장 {total_rows}행 · 외부의존 0")
        print("=" * 64)
        sys.exit(0)
    else:
        print("결과: FAIL — 위 항목 확인")
        print("=" * 64)
        sys.exit(1)


if __name__ == "__main__":
    main()
