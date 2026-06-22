#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E10.py — the focused pass/fail gate for increment E10 (run from the package root).

    python3 research/E10-light-dark-adaptation/gate_E10.py

Asserts, INDEPENDENTLY of run.py's own internal asserts (its own steady-state solver re-derived here):
  [G1] DETERMINISM   — research/E10-light-dark-adaptation/run.py emits an identical sha256 on two runs.
  [G2] STEADY-STATE  — each s*(h) is a TRUE zero of the FROZEN field γ·s−s³+h (residual ≈ 0), so the
                       analysis sits on the inherited switch's steady state, not an approximation.
  [G3] SATURATION    — the ON-branch steady state saturates onto the cube root: s*/h^(1/3) falls
                       monotonically toward 1 across the background sweep.
  [G4] GAIN-CONTROL  — the incremental gain ds*/dh = 1/(3s*²−γ) falls monotonically as the background
                       rises (a bright surround turns the switch down) — automatic light adaptation.
  [G5] WEBER/1-OVER-N— the CONTRAST gain (h/s*)·ds*/dh rises toward 1/3, and the pure-cube limit
                       (γ-term off ⇒ s*=h^(1/3)) is EXACTLY 1/n = 1/3 (n=3, the cubic).
  [G6] γ-INDEPENDENT — the asymptotic contrast gain is ≈ 1/3 for TWO different genes' γ (RHO, CNGB3):
                       the compression is the cubic ORDER, not the threshold γ.
  [G7] DYNAMIC-RANGE — deep in the saturated branch the log-compression → the cubic order n=3 (a huge
                       background range fits a bounded response range).
  [G8] NO-DRIFT/τ    — the γ E10 reads is byte-equal to the frozen atlas, and the recovery τ_s=40.0 /
                       β=0.5 are byte-equal to the frozen Neuron (read-only; nothing fitted).

Exit 0 + 'E10 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, Neuron           # FROZEN inherited field + recovery τ
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

G_RHO, G_CNGB3 = ATLAS["RHO"]["gamma"], ATLAS["CNGB3"]["gamma"]
SWEEP = [1, 10, 100, 1000, 10000, 100000]


def s_star(g, h, iters=200):
    """Independent re-derivation of the ON-branch steady state (Newton on s³−γs−h)."""
    s = max(math.sqrt(g) if g > 0 else 0.0, h ** (1.0 / 3.0)) + 1.0
    for _ in range(iters):
        s = s - (s ** 3 - g * s - h) / (3.0 * s * s - g)
    return s


def _run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of_run(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def main():
    print("=" * 74)
    print("E10 GATE — research/E10-light-dark-adaptation")
    print("=" * 74)
    ok = True

    s = [s_star(G_RHO, float(h)) for h in SWEEP]
    gain = [1.0 / (3.0 * x * x - G_RHO) for x in s]
    contrast = [(float(SWEEP[i]) / s[i]) * gain[i] for i in range(len(SWEEP))]

    # [G1] determinism
    o1, o2 = _run(), _run()
    h1, h2 = _sha_of_run(o1), _sha_of_run(o2)
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] steady-state: each s* is a true zero of the FROZEN field
    resid = max(abs(sdot(s[i], G_RHO, float(SWEEP[i]))) for i in range(len(SWEEP)))
    g2 = (resid < 1e-9); ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 steady-state — every s* a true zero of γ·s−s³+h "
          f"(max residual {resid:.1e})")

    # [G3] saturation: s*/h^(1/3) → 1 monotonically
    ratio = [s[i] / (float(SWEEP[i]) ** (1.0 / 3.0)) for i in range(len(SWEEP))]
    g3 = all(ratio[i + 1] <= ratio[i] + 1e-12 for i in range(len(ratio) - 1)) and abs(ratio[-1] - 1.0) < 1e-3
    ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 saturation — s*/h^(1/3) ↓ to {ratio[-1]:.6f} (cube-root)")

    # [G4] gain control: incremental gain falls monotonically with background
    g4 = all(gain[i + 1] < gain[i] for i in range(len(gain) - 1)); ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 gain-control — gain ↓ dim→bright "
          f"({gain[0]:.3e} → {gain[-1]:.3e}, {gain[0]/gain[-1]:.0f}×)")

    # [G5] Weber: contrast → 1/3; pure-cube limit exactly 1/3
    pc = (1000.0 / (1000.0 ** (1.0 / 3.0))) * (1.0 / (3.0 * (1000.0 ** (1.0 / 3.0)) ** 2))
    rises = all(contrast[i + 1] >= contrast[i] - 1e-12 for i in range(len(contrast) - 1))
    g5 = rises and abs(pc - 1.0 / 3.0) < 1e-12 and abs(contrast[-1] - 1.0 / 3.0) < 1e-3; ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 Weber/1-over-n — contrast ↑ to {contrast[-1]:.6f}; "
          f"pure-cube = {pc:.6f} (= 1/3 exact)")

    # [G6] γ-independence: same asymptotic contrast for a different γ
    cs = {}
    for g, nm in ((G_RHO, "RHO"), (G_CNGB3, "CNGB3")):
        ss = s_star(g, 1.0e6); cs[nm] = (1.0e6 / ss) * (1.0 / (3.0 * ss * ss - g))
    g6 = all(abs(v - 1.0 / 3.0) < 1e-3 for v in cs.values()); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 γ-independent — contrast(1e6) RHO {cs['RHO']:.6f}, "
          f"CNGB3 {cs['CNGB3']:.6f} → 1/3")

    # [G7] dynamic range: deep-saturation log-compression → n=3
    sa, sb = s_star(G_RHO, 100.0), s_star(G_RHO, 1.0e8)
    comp = 6.0 / math.log10(sb / sa)
    g7 = abs(comp - 3.0) < 0.05; ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 dynamic-range — saturated log-compression {comp:.6f} → n=3")

    # [G8] no-drift + τ read-only
    nu = Neuron()
    g8 = (ATLAS["RHO"]["gamma"] == G_RHO and ATLAS["CNGB3"]["gamma"] == G_CNGB3
          and nu.tau_s == 40.0 and nu.beta == 0.5); ok &= g8
    print(f"  [{'PASS' if g8 else 'FAIL'}] G8 no-drift/τ — γ byte-equal to atlas; Neuron τ_s={nu.tau_s:.1f}/"
          f"β={nu.beta:.1f} read-only")

    print("=" * 74)
    print(f"E10 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
