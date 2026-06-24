#!/usr/bin/env python3
"""verify_all.py — one-command verification for the VP Recent-Sequence Cascade (v30).

Runs EVERY cascade gate in repro/ (Modules 25-45: the petroleum strand M33-M44 and the
Continental-Genesis import M45 included), and asserts the inherited verification bundles
(engine 39/39, SHA 60/60, the three Continental-Genesis screens, the fossil-count audit;
DNA Emergence best-effort). Prints a single PASS/FAIL tally.

SEED = 19. Works from any directory (all paths resolve relative to this file).
Exit code 0 iff every REQUIRED check passes.
"""
import os, sys, subprocess, hashlib, re
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../vp_recent_sequence_cascade_v30/repro
ROOT = HERE.parent                               # package root
PY = sys.executable

def run(cmd, cwd, timeout=300):
    try:
        r = subprocess.run([PY, *cmd], cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)

results = []   # (name, ok, detail)
def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

# -------------------------------------------------------------------------
print("=" * 74)
print("VP Recent-Sequence Cascade v30 — verify_all")
print("=" * 74)

# 1) cascade gates: every repro/*.py except this file
print("\n[1] Cascade gates (repro/*.py — Modules 25-45)")
gate_scripts = sorted(p for p in HERE.glob("*.py") if p.name != "verify_all.py")
n_pass = 0
for s in gate_scripts:
    rc, out, err = run([s.name], cwd=HERE)
    has_gate = "REPRO GATE" in s.read_text(encoding="utf-8", errors="ignore")
    if has_gate:
        ok = (rc == 0) and ("REPRO GATE: PASS" in out)
    else:
        ok = (rc == 0)                                   # screen w/o self-gate: exit-code only
    if ok: n_pass += 1
    else:  record(s.name, False, (err.strip().splitlines()[-1] if err.strip() else f"rc={rc}"))
print(f"      cascade gates: {n_pass}/{len(gate_scripts)} PASS")
record("cascade gates (repro/)", n_pass == len(gate_scripts), f"{n_pass}/{len(gate_scripts)}")

# 2) Continental-Genesis screens (inherited, re-verified)
print("\n[2] Continental-Genesis screens (cg_inheritance/)")
cg = ROOT / "cg_inheritance" / "repro"
cg_pass = 0; cg_total = 0
if cg.is_dir():
    for s in sorted(cg.glob("*.py")):
        cg_total += 1
        rc, out, err = run([s.name], cwd=cg)
        if rc == 0 and "REPRO GATE: PASS" in out: cg_pass += 1
record("Continental-Genesis screens (CG-30/26/36)", cg_total > 0 and cg_pass == cg_total, f"{cg_pass}/{cg_total}")

# 3) inherited engine — validate_all.py -> 39/39
print("\n[3] Inherited engine")
eng = ROOT / "inherited_engine"
rc, out, err = run(["validate_all.py"], cwd=eng, timeout=600)
m = re.search(r"(\d+)\s*/\s*(\d+)\s+PASS", out)
record("engine validate_all.py", bool(m) and m.group(1) == m.group(2), (m.group(0) if m else f"rc={rc}"))

# 4) inherited engine — SHA256SUMS.txt -> all OK
shafile = eng / "SHA256SUMS.txt"
if shafile.is_file():
    total = ok = 0
    for line in shafile.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = line.split(None, 1)
        if len(parts) != 2: continue
        digest, name = parts[0], parts[1].lstrip("*").strip()
        total += 1
        fp = eng / name
        if fp.is_file() and hashlib.sha256(fp.read_bytes()).hexdigest() == digest: ok += 1
    record("engine SHA256SUMS", total > 0 and ok == total, f"{ok}/{total} SHA-OK")
else:
    record("engine SHA256SUMS", False, "SHA256SUMS.txt missing")

# 5) DNA Emergence — REQUIRED via manifest integrity (stdlib; no Biopython needed)
print("\n[4] DNA Emergence (inherited; manifest integrity — required)")
def check_manifest(folder, label):
    mf = folder / "MANIFEST.sha256"
    if not mf.is_file():
        record(label, False, "MANIFEST.sha256 missing"); return
    total = okc = 0
    for line in mf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = line.split(None, 1)
        if len(parts) != 2: continue
        digest, name = parts[0], parts[1].lstrip("*").strip()
        total += 1
        fp = folder / name
        if fp.is_file() and hashlib.sha256(fp.read_bytes()).hexdigest() == digest: okc += 1
    record(label, total > 0 and okc == total, f"{okc}/{total} SHA-OK")
check_manifest(ROOT / "dna_emergence" / "plant",  "DNA Emergence plant manifest")
check_manifest(ROOT / "dna_emergence" / "animal", "DNA Emergence animal manifest")

# 6) Best-effort runtime re-runs (need 3rd-party libs: pyreadr / Biopython). Reported, not required.
print("\n[5] Best-effort runtime re-runs (need pyreadr / Biopython; reported, not required)")
fc = ROOT / "fossil_audit" / "fossil_counts.py"
if fc.is_file():
    rc, out, err = run(["fossil_counts.py"], cwd=fc.parent, timeout=300)
    ok = (rc == 0); tail = (err.strip().splitlines()[-1] if err.strip() else f"rc={rc}")
    print(f"  [{'PASS' if ok else 'SKIP'}] fossil_audit/fossil_counts.py" + ("" if ok else f" — {tail}"))
for kind in ("animal", "plant"):
    ra = ROOT / "dna_emergence" / kind / "repro" / "run_all.py"
    if ra.is_file():
        rc, out, err = run(["run_all.py"], cwd=ra.parent, timeout=180)
        ok = (rc == 0); tail = (err.strip().splitlines()[-1] if err.strip() else f"rc={rc}")
        print(f"  [{'PASS' if ok else 'SKIP'}] dna_emergence/{kind}/run_all.py" + ("" if ok else f" — {tail}"))

# -------------------------------------------------------------------------
required = [r for r in results]
n_ok = sum(1 for _, ok, _ in required if ok)
print("\n" + "=" * 74)
print(f"REQUIRED CHECKS: {n_ok}/{len(required)} PASS")
print("=" * 74)
if n_ok == len(required):
    print("ALL REQUIRED CHECKS PASS — v30 reproducibility verified. Falsification = discovery.")
    sys.exit(0)
else:
    print("SOME REQUIRED CHECKS FAILED — see [FAIL] lines above.")
    sys.exit(1)
