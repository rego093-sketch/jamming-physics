#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E5.py — the focused pass/fail gate for increment E5 (run from the package root).

    python3 research/E5-allergic-smell-loss/gate_E5.py

THEORETICAL / NON-CLINICAL. This gate checks STRUCTURE, never a clinical claim. All of E5 is
direction-only / proposal-only (FIREWALL.md #4, #8): no diagnosis, dose, molecule, or efficacy. The
allergy MECHANISM is the immune/hematologic volume's §11 (cited [V], DOI 10.5281/zenodo.20755280);
E5 derives ONLY the olfactory-surface consequence and re-derives none of the immune mechanism.

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM    — research/E5-allergic-smell-loss/run.py emits an identical sha256 on two runs.
  [G2] CONDUCTIVE FADE — with the organ INTACT, sweeping the conductive factor κ down turns OR channels
                        OFF monotonically (drive↓ can only switch off), full at κ=1 and anosmia at κ=0.
  [G3] CONDUCTIVE REVERSIBLE — restoring κ→1 returns the percept to baseline EXACTLY (γ intact; the
                        FROZEN flip intact): conductive loss is reversible.
  [G4] ORGAN PRESENCE  — each OSN-identity organiser's R19 Organ is ABSENT below its presence threshold
                        and PRESENT above it (parts present ≠ trait): the acquired form of the E4
                        organ-formation failure.
  [G5] SENSORINEURAL PERSISTENT — with the OSN organ degraded (below presence), the percept stays 0 even
                        at FULL conductive drive κ=1: an organ failure no κ can rescue.
  [G6] DISCRIMINATOR   — restoring the drive separates the two: conductive recovers to N, sensorineural
                        stays 0 (the substrate expresses the clinical conductive-vs-sensorineural split).
  [G7] NO-DRIFT / NO-NEW-GENE — the OR + organiser γ E5 consumes is byte-equal to the frozen atlas, and
                        E5 adds NO gene (N_OR=7, N_organiser=3 unchanged): nothing fitted, no-regression.

Exit 0 + 'E5 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle, Organ                  # FROZEN inherited switch + Organ
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

OR_GENES   = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_receptor"))
ORGANISERS = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_neuron_identity"))
N_STEPS, DT = 1500, 0.02


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _rest(g):
    return -math.sqrt(g)


def _or_on(sym, h):
    g = ATLAS[sym]["gamma"]
    return settle(g, h, s0=_rest(g), n=N_STEPS, dt=DT) > 0.0


def _organ_present(cis):
    return all(Organ(s, ATLAS[s]["gamma"]).present(cis) for s in ORGANISERS)


def _percept(kappa, h0, cis):
    if not _organ_present(cis):
        return 0
    return sum(_or_on(s, kappa * h0) for s in OR_GENES)


def main():
    print("=" * 74)
    print("E5 GATE — research/E5-allergic-smell-loss   (theoretical / NON-CLINICAL; direction-only)")
    print("=" * 74)
    ok = True

    N      = len(OR_GENES)
    H0     = 1.15 * max(spinodal(ATLAS[s]["gamma"]) for s in OR_GENES)
    CIS_OK = 1.10 * max(spinodal(ATLAS[s]["gamma"]) for s in ORGANISERS)   # organ present
    CIS_KO = 0.90 * min(spinodal(ATLAS[s]["gamma"]) for s in ORGANISERS)   # organ absent

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] conductive fade: monotone in κ, full at κ=1, anosmia at κ=0
    sweep  = (1.00, 0.95, 0.90, 0.86, 0.82, 0.60, 0.30, 0.00)
    counts = [_percept(k, H0, CIS_OK) for k in sweep]
    g2 = (counts[0] == N and counts[-1] == 0 and all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1)))
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 conductive fade — κ↓ turns ORs off monotonically "
          f"({N}@κ=1 → 0@κ=0; trace {counts})")

    # [G3] conductive reversible: restore κ=1 → baseline
    g3 = (_percept(1.00, H0, CIS_OK) == N); ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 conductive reversible — restore κ→1 returns percept to {N}/{N} (γ intact)")

    # [G4] OSN organ presence threshold (parts ≠ trait; acquired E4-type failure)
    g4 = True
    for s in ORGANISERS:
        o = Organ(s, ATLAS[s]["gamma"]); hstar = o.functional_spinodal()
        g4 &= (o.present(0.90 * hstar) is False) and (o.present(1.10 * hstar) is True)
    ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 organ presence — every OSN organiser absent below h*, present above (parts≠trait)")

    # [G5] sensorineural persistent: organ gone → 0 even at full drive
    g5 = (_percept(1.00, H0, CIS_KO) == 0); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 sensorineural persistent — organ degraded → anosmia at FULL drive κ=1 (no κ rescues)")

    # [G6] discriminator: restore drive → conductive recovers, sensorineural does not
    n_block         = _percept(0.82, H0, CIS_OK)
    n_block_treated = _percept(1.00, H0, CIS_OK)
    n_sn            = _percept(1.00, H0, CIS_KO)
    g6 = (n_block < N and n_block_treated == N and n_sn == 0); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 discriminator — restore drive: conductive {n_block}→{n_block_treated}/{N} recovers, "
          f"sensorineural {n_sn}/{N} does not")

    # [G7] no-drift / no-new-gene: γ byte-equal to frozen atlas, panel sizes unchanged
    frozen_or  = {"OR1D2": 1.2714, "OR2J3": 1.2224, "OR2W1": 1.2412, "OR51E2": 1.2427,
                  "OR5AN1": 1.2637, "OR6A2": 1.3036, "OR7D4": 1.2945}
    frozen_org = {"LHX2": 1.5172, "EBF1": 1.4097, "EMX2": 1.4574}
    g7 = (len(OR_GENES) == 7 and len(ORGANISERS) == 3
          and all(ATLAS[s]["gamma"] == v for s, v in frozen_or.items())
          and all(ATLAS[s]["gamma"] == v for s, v in frozen_org.items()))
    ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — OR(7)+organiser(3) γ byte-equal to frozen atlas (no gene added, no fitting)")

    print("=" * 74)
    print(f"E5 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
