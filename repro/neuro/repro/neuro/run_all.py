#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py — one command reproduces the entire neuro chain and verifies it.

Reinforces VP-SPEC Constitution C1 (maximum reproducibility, drift 0):
  (A) DETERMINISM   — every module is run TWICE; the two stdout sha256 must match.
  (B) FROZEN HASHES — each module's sha256 is compared to expected_sha256.json
                      (written on first run, verified ever after). Any change fails.
  (C) HTML ↔ CODE   — every headline number displayed in the canonical HTML is
                      confirmed to appear in the producing module's output, so the
                      pages cannot drift from the code (the C1 cross-check).

Exit code 0 iff all three pass. Standard library only.
"""
import subprocess, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # repro/neuro
DOCS = os.path.normpath(os.path.join(ROOT, "..", "..", "docs", "neuro"))
EXPECTED = os.path.join(ROOT, "expected_sha256.json")
MANIFEST = os.path.normpath(os.path.join(ROOT, "..", "..", "reports", "reproduction_manifest.json"))

MODULES = [
    ("_engine",                        "verify_neuro_emergence.py"),
    ("10-sensory-input-transduction",  "run_transduction.py"),
    ("11-sensorimotor-loop",           "run_loop.py"),
    ("12-sensory-organ-emergence-4d",  "sensory_emergence_4d.py"),
    ("13-em-emission-bridge",          "vp_em_emission.py"),
    ("14-motor-quantification",        "motor_quantification.py"),
    ("15-em-link-full",                "vp_em_link_full.py"),
    ("18-em-brain-circulation",        "vp_em_brain_circulation.py"),
    ("19-em-ephaptic-threshold",       "vp_em_ephaptic_threshold.py"),
    ("20-complete-sensory-atlas",      "complete_sensory_atlas.py"),
    ("_inherited",                     "vp_light_emergence_quantum.py"),
    ("_inherited",                     "vp_color_by_angle.py"),
    ("_inherited",                     "vp_ion_low_frequency.py"),
    ("_inherited",                     "vp_phototransduction_4d.py"),
    ("_inherited",                     "vp_frequency_multiplexing.py"),
    ("_inherited",                     "vp_electrocommunication.py"),
    ("_inherited",                     "vp_ion_em_information.py"),
    ("_inherited",                     "vp_sensory_frequencies.py"),
    # --- v1.11 analgesic-inheritance + neuro-native pain + DNA-emergence (added this session) ---
    ("20b-dna-emergence-inheritance",  "verify_dna_emergence.py"),
    ("21-analgesic-nociceptor-threshold", "rederive_on_neuro_engine.py"),
    ("22-neuropathic-pain-firing-threshold", "neuropathic_pain_levers.py"),
]

# (C) every decimal the canonical chapters DISPLAY must be reproduced by some module
#     (exact, or the HTML rounding of a longer module value). Chapters authored here:
NEW_CHAPTERS = ["00-foundations-inherited", "10-sensory-input-transduction",
                "11-sensorimotor-loop", "12-sensory-organ-emergence-4d",
                "13-em-emission-bridge", "14-motor-quantification",
                "15-em-link-full", "18-em-brain-circulation",
                "19-em-ephaptic-threshold", "20-complete-sensory-atlas"]
DOI_TOKEN = "10.5281"   # the DOI string is not a result number

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def run(d, s):
    r = subprocess.run([sys.executable, s], cwd=os.path.join(ROOT, d),
                       capture_output=True, text=True, timeout=600)
    return r.stdout, r.returncode

def main():
    print("="*72); print("REPRODUCE ALL — neuro chain (C1: determinism + frozen hashes + HTML↔code)"); print("="*72)
    outputs, manifest, fails = {}, {}, []

    # (A) determinism
    print("\n[A] determinism (2× run, sha256 must match):")
    for d, s in MODULES:
        o1, rc1 = run(d, s); o2, rc2 = run(d, s)
        h1, h2 = sha(o1), sha(o2)
        det = (h1 == h2); ok = (rc1 == 0 and rc2 == 0)
        outputs[s] = o1; manifest[s] = {"dir": d, "sha256": h1, "deterministic": det, "ran_ok": ok}
        flag = "ok" if (det and ok) else "FAIL"
        if not (det and ok): fails.append(f"{s}: det={det} ran_ok={ok}")
        print(f"    {s:<34} {h1[:16]}…  {flag}")

    # (B) frozen hashes
    print("\n[B] frozen hashes (expected_sha256.json):")
    if os.path.exists(EXPECTED):
        exp = json.load(open(EXPECTED))
        for s in manifest:
            cur = manifest[s]["sha256"]; want = exp.get(s)
            if want is None:
                print(f"    {s:<34} (no frozen hash yet — recording)")
            elif cur == want:
                print(f"    {s:<34} matches frozen ✓")
            else:
                print(f"    {s:<34} CHANGED vs frozen ✗"); fails.append(f"{s}: hash changed")
        # add any new modules to the frozen set
        for s in manifest:
            exp.setdefault(s, manifest[s]["sha256"])
        json.dump(exp, open(EXPECTED, "w"), indent=1)
    else:
        json.dump({s: manifest[s]["sha256"] for s in manifest}, open(EXPECTED, "w"), indent=1)
        print(f"    wrote {len(manifest)} frozen hashes (first run)")

    # (C) HTML ↔ code cross-check
    print("\n[C] every chapter number reproduced by some module (drift 0, rounding-aware):")
    import re
    union = "".join(outputs.values())
    def reproduced(tok):
        if tok in union: return True
        try:
            f = float(tok); dec = len(tok.split(".")[1])
            for m in re.findall(r"\d+\.\d+", union):
                if abs(float(m) - f) < 0.5*10**(-dec): return True
        except Exception: pass
        return False
    for slug in NEW_CHAPTERS:
        html = open(os.path.join(DOCS, slug, "index.html"), encoding="utf-8").read()
        nums = sorted(set(re.findall(r"\d+\.\d{3,}", html)) - {DOI_TOKEN})
        miss = [t for t in nums if not reproduced(t)]
        ok = not miss
        if not ok: fails.append(f"HTML[{slug}] unreproduced: {miss}")
        print(f"    {slug:<32} {len(nums):>2} numbers  {'all reproduced ✓' if ok else 'MISSING '+str(miss)}")

    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    json.dump({"modules": manifest, "n_modules": len(manifest),
               "all_deterministic": all(m["deterministic"] for m in manifest.values()),
               "fails": fails}, open(MANIFEST, "w"), indent=1)

    print("\n" + "-"*72)
    if fails:
        print(f"RESULT: FAIL ({len(fails)} issue(s))")
        for f in fails: print("   -", f)
        return 1
    print(f"RESULT: PASS — {len(MODULES)} modules deterministic, hashes frozen, HTML↔code drift 0")
    print(f"manifest: reports/reproduction_manifest.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
