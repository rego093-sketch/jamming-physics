#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_chemistry.py — VP 화학 이론 패키지 재현성·정합성 검증 하니스
================================================================
목적: 화학 이론서가 주장하는 재현성(결정론·표준라이브러리·케이스 원장)을
      *제3자가 한 번의 실행으로* 검증할 수 있게 한다. 본 스크립트 자체도
      외부 의존이 없으며(표준 라이브러리만), 산출은 결정론적이다.

검증 항목
  [A] 전 모듈 실행: research/**/vp_*.py 가 오류 없이 종료(exit 0)하는가
  [B] 결정론: 각 모듈을 2회 실행해 stdout sha256 이 동일한가
  [C] 의존성: import 가 표준 라이브러리(math 등)로 한정되는가
  [D] 케이스 원장: cases.csv 각 행 필드수·등급 어휘·총 건수 정합

사용법:
  python3 verify_chemistry.py --root <화학패키지 루트>
      (루트 = VP_CHEMISTRY_THEORY.md 와 research/ 가 있는 디렉토리)
  옵션 없으면 스크립트 위치 기준 ../VP_Chemistry_Theory 또는 ./ 를 자동 탐색.

종료 코드: 모든 항목 PASS 면 0, 하나라도 FAIL 이면 1.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import csv
import glob

# 표준 라이브러리로 인정하는 최상위 모듈(외부 의존이 아닌 것)
STDLIB_ALLOW = {
    "math", "cmath", "fractions", "decimal", "itertools", "functools",
    "collections", "statistics", "random", "sys", "os", "csv", "json",
    "re", "string", "bisect", "heapq", "copy", "typing", "dataclasses",
    "argparse", "textwrap", "pprint",
}
# 케이스 원장에서 허용하는 등급 토큰(복합 포함)
GRADE_ALLOW = {"F", "F?", "CAL", "V", "O", "H", "F+O", "F+CAL", "F?+O", "F+CAL+O", "F+CAL+H", "V+CAL"}


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def find_root(cli_root):
    if cli_root:
        return os.path.abspath(cli_root)
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [
        os.path.join(here, "..", "VP_Chemistry_Theory"),
        os.path.join(here, "VP_Chemistry_Theory"),
        here, os.path.join(here, ".."),
    ]
    for c in cands:
        if (os.path.isdir(os.path.join(c, "research")) or
                os.path.isdir(os.path.join(c, "code"))):
            return os.path.abspath(c)
    return os.path.abspath(here)


def run_once(path):
    """모듈 1회 실행 → (exit_code, stdout)."""
    try:
        p = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=120,
        )
        return p.returncode, p.stdout
    except Exception as e:  # noqa: BLE001
        return 999, f"__EXC__ {e}"


def check_imports(path):
    """파일에서 최상위 import 모듈명을 추출, 표준라이브러리 밖이면 반환."""
    foreign = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\s*(?:import|from)\s+([a-zA-Z_][\w]*)", line)
            if m:
                mod = m.group(1)
                if mod not in STDLIB_ALLOW:
                    foreign.add(mod)
    return foreign


def audit_cases(csv_path):
    """cases.csv 정합 감사 → (총건수, 어긋난행[(line,nfields)], 비표준등급[(line,grade)])."""
    bad_fields, bad_grade = [], []
    n = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        ncols = len(header)
        gi = header.index("grade") if "grade" in header else None
        for i, row in enumerate(reader, start=2):
            n += 1
            if len(row) != ncols:
                bad_fields.append((i, len(row)))
            elif gi is not None and row[gi] not in GRADE_ALLOW:
                bad_grade.append((i, row[gi]))
    return n, ncols, bad_fields, bad_grade


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="화학 패키지 루트")
    args = ap.parse_args()
    root = find_root(args.root)

    scripts = sorted(glob.glob(os.path.join(root, "**", "vp_*.py"),
                               recursive=True))
    print("=" * 72)
    print("VP 화학 패키지 검증 하니스")
    print("=" * 72)
    print(f"루트: {root}")
    print(f"모듈 수: {len(scripts)}")
    print(f"python: {sys.version.split()[0]}")
    print()

    if not scripts:
        print("[치명] research/ 에서 vp_*.py 를 찾지 못함. --root 를 확인하라.")
        return 1

    a_fail, b_fail, c_fail = [], [], []
    foreign_all = set()

    print("[A/B/C] 모듈별 실행·결정론·의존성")
    print(f"  {'모듈':<46}{'실행':<6}{'결정론':<8}{'표준라이브러리'}")
    print("  " + "-" * 70)
    for s in scripts:
        rel = os.path.relpath(s, root)
        rc1, out1 = run_once(s)
        rc2, out2 = run_once(s)
        runok = (rc1 == 0)
        det = (sha256_text(out1) == sha256_text(out2))
        foreign = check_imports(s)
        foreign_all |= foreign
        if not runok:
            a_fail.append(rel)
        if not det:
            b_fail.append(rel)
        if foreign:
            c_fail.append((rel, sorted(foreign)))
        print(f"  {rel:<46}{'OK' if runok else 'FAIL':<6}"
              f"{'OK' if det else 'DIFF':<8}{'OK' if not foreign else ','.join(sorted(foreign))}")
    print()

    # [D] cases ledgers (모든 cases*.csv 재귀 탐색)
    print("[D] 케이스 원장 정합")
    csv_paths = sorted(glob.glob(os.path.join(root, "**", "cases*.csv"),
                                 recursive=True))
    d_ok = True
    if not csv_paths:
        print("  cases*.csv 없음 → SKIP")
    else:
        for csv_path in csv_paths:
            rel = os.path.relpath(csv_path, root)
            n, ncols, bad_fields, bad_grade = audit_cases(csv_path)
            ok = not bad_fields and not bad_grade
            print(f"  {rel}: {n}건 ({ncols}필드) → {'OK' if ok else 'FAIL'}")
            for ln, nf in bad_fields:
                d_ok = False
                print(f"    [FAIL] L{ln}: 필드수 {nf} != {ncols}")
            for ln, g in bad_grade:
                d_ok = False
                print(f"    [FAIL] L{ln}: 비표준 등급 {g!r}")
    print()

    # 요약
    print("=" * 72)
    print("요약")
    print("=" * 72)
    print(f"[A] 실행 무오류 : {len(scripts)-len(a_fail)}/{len(scripts)}"
          + ("" if not a_fail else f"  FAIL={a_fail}"))
    print(f"[B] 결정론      : {len(scripts)-len(b_fail)}/{len(scripts)}"
          + ("" if not b_fail else f"  FAIL={b_fail}"))
    print(f"[C] 표준라이브러리: {'전 모듈 통과' if not c_fail else 'FAIL'}"
          + ("" if not c_fail else f" {c_fail}"))
    print(f"    관측된 import 최상위: {sorted(foreign_all) or '없음(표준라이브러리만)'}")
    print(f"[D] 원장 정합   : {'PASS' if d_ok else 'FAIL'}")
    overall = (not a_fail) and (not b_fail) and (not c_fail) and d_ok
    print()
    print("최종:", "PASS (모든 항목 통과)" if overall else "FAIL (위 항목 확인)")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
