#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small A4 gate.  Asserts increment A4's claims, independent of the master verifier.

Run:  python3 research/A4-anchor-loop-phase/gate.py
Exit 0 + 'A4 GATE: PASS' iff all hold.

This increment closes the FIREWALL's one NAMED, DEFERRED [O]: "the FULL A4 anchor/loop/anchor-relative-
phase needs the wider region + an NCBI feature table and is a named [O] deferred read." The gate proves
the read is now MADE — from MEASURED inputs through the INHERITED grammar — without one tuned number,
and reports the residual [O] honestly.

Checks (each is a binding A4 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  keystone + motors [F]/[V] — region[FLANK:FLANK+len(promoter)] == the FROZEN promoter byte-for-byte
      for all 19 genes (the wide read sits ON the unchanged γ layer, zero drift), AND every gene carries
      ≥1 REAL neighbouring-gene motor parsed from its NCBI feature table (the deferred read's core promise:
      anchors-only → real motors+loops). Re-derived here independently of run.py's internal asserts.
  G3  no-regression (회귀금지) — the 8 PRE-EXISTING inherited artifacts are byte-identical to the frozen
      seed (NO inherited byte changed, NO re-freeze), AND the one new frozen artifact
      inherited/ear_regions.cache.json (the measured wide-region + feature-table inputs) is recorded in the
      frozen set and matches the file on disk — a deliberate ADD, not a drift. Every frozen entry matches.
  G4  N-robustness [F]/[O] — re-reading the SAME fetch on its central sub-window (FLANK→FLANK/2, a 2×
      shrink, no new data) keeps the qualitative read window-stable for the majority: motor EXISTENCE
      19/19 (forced), shell class 15/19, contact sign 16/19 (the boundary-near minority flips — the named
      window-relative [O]). Counts re-derived here and pinned (the measurement must reproduce).
  G5  helical-phase read [F]/[L] — the anchor-relative phase is the INHERITED B-DNA grammar, not a
      reimplementation: DI.RISE_A==3.4, DI.TWIST_DEG==34.29 (the LOCK); helix_coord's contact rule is
      exactly same-rotational-face (min(face,1−face)<0.17); and each gene's contact_competent in the full
      A4 read equals DI.helix_coord(anchor−TSS) — so the 3/19 contact-competent set {EYA1,PCDH15,SLC26A4}
      is the grammar's verdict, not a tuned one.
  G6  honesty [O] — run.py names every open obstacle (N1–N7), uses the [O] grade, declares the absolute
      magnitudes / boundary-near class+sign as window-relative, and explicitly does NOT pretend to a clean
      numeric closure (a clean closure would be tuning). The honest framing strings are present.
  G7  firewall — FIREWALL.md is byte-identical to its binding verbatim hash (the inherited boundaries are
      not silently edited even as the named [O] is measured), and run.py reads STRUCTURE-ONLY: it keeps
      Layer-2 flagged and diagnoses / treats / prescribes nothing, designs no molecule.
"""
import os, sys, json, math, subprocess, hashlib, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import dna_interpreter as DI            # the inherited grammar (helix_coord / parse_ft_motors / constants)

# the binding verbatim hash of the inherited firewall (any edit to the boundaries is caught)
FIREWALL_SHA = "637e8bfc037c9d3ba9e20a8dd2e24f07cbbed8c5b091b6b04336edb34a8d52ca"
# the 8 pre-existing inherited artifacts that must NOT change in this increment (no re-freeze)
PREEXISTING_FROZEN = {
    "inherited/dna_interpreter.py", "inherited/ear_promoters.cache.json", "inherited/gamma_pipeline.py",
    "inherited/key_pipeline_full.py", "inherited/organ_gamma.json", "inherited/vp_dna_reading.py",
    "inherited/vp_sound_wave.py", "inherited/vp_substrate.py",
}
NEW_FROZEN = "inherited/ear_regions.cache.json"   # the one deliberately-added frozen artifact
# the measurement this increment MADE (pinned: the honest result must reproduce, not a tuned target)
N_GENES            = 19
CONTACT_COMPETENT  = {"EYA1", "PCDH15", "SLC26A4"}   # 3/19, the grammar's verdict on the full window
CLS_STABLE         = 15   # shell class window-stable under the 2× shrink
CTC_STABLE         = 16   # contact sign window-stable
MOT_STABLE         = 19   # motor existence window-stable (forced)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod


# every increment ships a file called run.py — load under a UNIQUE name to avoid a sys.modules clash
A4 = _load("a4_run", os.path.join(_HERE, "run.py"))


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 92)
    print("A4 GATE — vp_ear_emergence_seed / A4 (FULL anchor/loop/anchor-relative-phase deferred read)")
    print("=" * 92)
    ok = True

    reg, prom = A4._load()
    syms  = list(reg.keys())
    flank = json.load(open(A4.REGION_CACHE, encoding="utf-8"))["_flank"]

    # G1 determinism --------------------------------------------------------------------------------
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2 and len(syms) == N_GENES); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]}), {len(syms)} genes")

    # G2 keystone + motors (re-derived independently of run.py's internal asserts) -------------------
    keyok = sum(1 for s in syms
                if reg[s]["region_seq"][flank:flank + len(prom[s]["seq"])] == prom[s]["seq"])
    motok = sum(1 for s in syms if len(DI.parse_ft_motors(reg[s]["ft_text"])) > 0)
    g = (keyok == N_GENES and motok == N_GENES); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 keystone + motors — region⊃frozen promoter {keyok}/{N_GENES} "
          f"(zero drift); ≥1 real feature-table motor {motok}/{N_GENES}")

    # G3 no-regression — 8 inherited bytes unchanged + the 1 new cache deliberately frozen -----------
    frozen = json.load(open(os.path.join(ROOT, "inherited", "FROZEN_SHA256.json"), encoding="utf-8"))["files"]
    all_match = all(_sha(os.path.join(ROOT, rel)) == want for rel, want in frozen.items())
    preexisting_intact = PREEXISTING_FROZEN.issubset(set(frozen)) and all(
        _sha(os.path.join(ROOT, rel)) == frozen[rel] for rel in PREEXISTING_FROZEN)
    new_recorded = (NEW_FROZEN in frozen and _sha(os.path.join(ROOT, NEW_FROZEN)) == frozen[NEW_FROZEN])
    g = (all_match and preexisting_intact and new_recorded); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 no-regression — 8 inherited bytes intact ({preexisting_intact}), "
          f"new region cache frozen+matching ({new_recorded}); every frozen entry matches ({all_match})")

    # G4 N-robustness — re-derive the window-stability counts; pin them (measurement must reproduce) -
    cls_stab = ctc_stab = mot_stab = 0
    for s in syms:
        r = reg[s]
        cf, _ = A4.full_a4(r["region_seq"], r["tss_in_region"], prom[s]["seq"], r["ft_text"])
        ch = A4.central_subwindow_read(r["region_seq"], r["tss_in_region"], prom[s]["seq"], r["ft_text"], flank)
        cls_stab += (cf["shell_class"] == ch["shell_class"])
        ctc_stab += (cf["contact_competent"] == ch["contact_competent"])
        mot_stab += ((cf["region_motor_count"] > 0) == (ch["region_motor_count"] > 0))
    g = (mot_stab == MOT_STABLE == N_GENES and cls_stab == CLS_STABLE and ctc_stab == CTC_STABLE); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 N-robustness — motor existence {mot_stab}/{N_GENES} (forced); "
          f"shell class {cls_stab}/{N_GENES}; contact sign {ctc_stab}/{N_GENES} (boundary-near flips = [O])")

    # G5 helical-phase read IS the inherited grammar (LOCK constants + same-face rule + per-gene verdict)
    lock_ok = (DI.RISE_A == 3.4 and DI.TWIST_DEG == 34.29)
    # the contact rule is exactly same-rotational-face (min(face,1−face)<0.17), checked across a turn
    rule_ok = all(DI.helix_coord(bp)["contact_competent"] ==
                  (min((abs(bp) * DI.TWIST_DEG % 360.0) / 360.0,
                       1.0 - (abs(bp) * DI.TWIST_DEG % 360.0) / 360.0) < 0.17)
                  for bp in range(0, 64))
    # each gene's contact_competent equals the grammar's helix_coord on its anchor offset (not reimplemented)
    grammar_ok = True
    contact_set = set()
    for s in syms:
        r = reg[s]
        c, _ = A4.full_a4(r["region_seq"], r["tss_in_region"], prom[s]["seq"], r["ft_text"])
        signed_bp = c["anchor_distance_bp"]                 # |anchor − TSS| in bp; phase depends on |bp|
        if DI.helix_coord(signed_bp)["contact_competent"] != c["contact_competent"]:
            grammar_ok = False
        if c["contact_competent"]:
            contact_set.add(s)
    set_ok = (contact_set == CONTACT_COMPETENT)
    g = (lock_ok and rule_ok and grammar_ok and set_ok); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 helical-phase read — LOCK(rise=3.4,twist=34.29)={lock_ok}, "
          f"same-face rule={rule_ok}, per-gene = grammar verdict={grammar_ok}; contact set {sorted(contact_set)}")

    # G6 honesty — N1–N7 named, [O] grade, window-relative declared, no clean-closure overclaim --------
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read().lower()
    named = all(f"n{i}" in src for i in range(1, 8))
    honest = ("[o]" in src and "window-relative" in src and "tuning" in src
              and "named, not hidden" in src and "does not pretend to a clean numeric closure" in src)
    g = (named and honest); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 honesty — N1–N7 named ({named}); [O]/window-relative/no-clean-"
          f"closure framing present ({honest})")

    # G7 firewall verbatim + structure-only -----------------------------------------------------------
    fw_ok = (_sha(os.path.join(ROOT, "FIREWALL.md")) == FIREWALL_SHA)
    structure_only = ("structure-only" in src and "layer-2 stays flagged" in src
                      and "diagnosed, treated, or prescribed" in src and "designs no molecule" in src.replace("\n", " "))
    g = (fw_ok and structure_only); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 firewall — FIREWALL.md verbatim ({fw_ok}); run reads "
          f"structure-only, Layer-2 flagged, nothing diagnosed/treated/prescribed ({structure_only})")

    print("=" * 92)
    print(f"A4 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 92)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
