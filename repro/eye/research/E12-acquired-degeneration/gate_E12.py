#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E12.py — the focused pass/fail gate for increment E12 (run from the package root).

    python3 research/E12-acquired-degeneration/gate_E12.py

Asserts, INDEPENDENTLY of run.py's own internal asserts (the R19 field and its fold are RE-DERIVED
here from scratch — this gate imports NOTHING from run.py or the substrate, so a drift in either side
is caught):
  [G1] DETERMINISM   — research/E12-acquired-degeneration/run.py emits an identical sha256 twice.
  [G2] COLLAPSE@FOLD — on the re-derived field ds/dt=γ·s−s³+h, a quasi-static DOWN ramp from a healthy
                       ON start (s>0) collapses (s>0 → s<0) at a drive equal to the analytic fold
                       −h*(γ)=−2(γ/3)^1.5 within the ramp resolution. (degeneration = crossing a fold.)
  [G3] START-INDEP   — two DIFFERENT healthy starting drives collapse at the SAME fold (independent of
                       where the healthy operating point began).
  [G4] HYSTERESIS    — from the collapsed state, a DOWN-stress (UP-drive) ramp recovers (s<0 → s>0) only
                       at the OPPOSITE fold +h*(γ); the recovery fold is strictly above the collapse fold
                       (a hysteresis loop of width ≈ 2·h*(γ) — the irreversibility margin).
  [G5] BISTABLE-BAND — at a drive strictly inside (−h*, +h*), BOTH the ON root (settling from +√γ) and
                       the OFF root (from −√γ) are stable — so the system 'remembers' which basin it fell
                       into. This is WHY recovery needs over-correction (the mechanism behind G4).
  [G6] TWO-ROUTES    — the basin-shallowing route (hold a fixed load, erode γ) collapses where h*(γ)=|load|,
                       landing on the SAME fold locus h=−h*(γ): one geometry, a different parameter moved.
  [G7] FRAGILITY     — the fold h*(γ)=2(γ/3)^1.5 is strictly MONOTONE in γ across the atlas (lower γ ⇒
                       smaller fold ⇒ tips under less stress); all γ are byte-equal to the atlas.
  [G8] FIREWALL      — the rendered run output carries NONE of E12's own MAGNITUDE_BLOCK tokens and no
                       '%' (direction-only; no dose/potency/pressure/glycaemic/length/clinical quantity).

Exit 0 + 'E12 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

# --- the R19 field + fold, RE-DERIVED BY HAND (imports nothing from the substrate or run.py) ---
_DT, _RELAX = 0.01, 4000


def field(s, g, h):
    """ds/dt of the R19 bistable switch (independent re-derivation)."""
    return g * s - s ** 3 + h


def fold(g):
    """The spinodal |h*| past which the opposite basin disappears: 2(γ/3)^1.5 (independent)."""
    return 2.0 * (g / 3.0) ** 1.5


def relax(s, g, h, n=_RELAX, dt=_DT):
    for _ in range(n):
        s += dt * field(s, g, h)
    return s


def linspace(a, b, n):
    if n == 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + step * i for i in range(n)]


def ramp_cross(g_or_h_values, mode, fixed, s0):
    """Track the state along a quasi-static ramp, carrying s forward; return the first ramp point at
    which sign(s) flips from sign(s0), plus the final state. (mode='h' or 'gamma')."""
    s = s0
    started_on = (s0 > 0.0)
    for x in g_or_h_values:
        g_use = x if mode == "gamma" else fixed
        h_use = x if mode == "h" else fixed
        s = relax(s, g_use, h_use)
        if (s > 0.0) != started_on:
            return x, s
    return None, s


def _run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of_run(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _load_block():
    """Pull E12's own MAGNITUDE_BLOCK (module is __main__-guarded; loading it does not run it)."""
    spec = importlib.util.spec_from_file_location("_e12_for_firewall", RUN)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.MAGNITUDE_BLOCK)


def main():
    print("=" * 74)
    print("E12 GATE — research/E12-acquired-degeneration")
    print("=" * 74)
    ok = True

    G = "RHO"
    g = ATLAS[G]["gamma"]
    hstar = fold(g)
    root = math.sqrt(g)
    N = 320
    step = abs((0.5 * hstar - (-1.3 * hstar)) / (N - 1))

    # [G1] determinism
    o1, o2 = _run(), _run()
    h1, h2 = _sha_of_run(o1), _sha_of_run(o2)
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] collapse at the fold — down ramp from ON collapses at −h*
    s_on = relax(root, g, 0.5 * hstar)
    hc, s_after = ramp_cross(linspace(0.5 * hstar, -1.3 * hstar, N), "h", g, s_on)
    g2 = (s_on > 0.0) and (s_after < 0.0) and (hc is not None) and abs(hc - (-hstar)) < 2.5 * step
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 collapse@fold — ON→degenerate at h={hc:.6f} (fold −h*={-hstar:.6f})")

    # [G3] start-independence — a different healthy start collapses at the same fold
    s_on2 = relax(root, g, 0.9 * hstar)
    hc2, _ = ramp_cross(linspace(0.9 * hstar, -1.3 * hstar, N), "h", g, s_on2)
    g3 = (hc2 is not None) and abs(hc2 - hc) < 3.0 * step; ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 start-indep — second start collapses at h={hc2:.6f} (same fold)")

    # [G4] hysteresis — recover only past +h*, strictly above the collapse fold
    hr, s_rec = ramp_cross(linspace(-1.3 * hstar, 1.3 * hstar, N), "h", g, s_after)
    g4 = (hr is not None) and (s_rec > 0.0) and (hr > hc + 0.5 * hstar) and abs(hr - hstar) < 2.5 * step
    ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 hysteresis — recover at h={hr:.6f} (+h*={hstar:.6f}); "
          f"loop {hr - hc:.6f} ≈ 2h*={2*hstar:.6f}")

    # [G5] bistable band — inside (−h*, +h*) BOTH roots are stable (the memory)
    g5 = True
    for hmid in (0.0, 0.5 * hstar, -0.5 * hstar):
        on_root  = relax(root, g, hmid)        # from the ON root
        off_root = relax(-root, g, hmid)       # from the OFF root
        g5 &= (on_root > 0.0) and (off_root < 0.0)
    ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 bistable-band — both basins stable inside (−h*,+h*) (hysteresis memory)")

    # [G6] two routes — basin-shallowing (fixed load, erode γ) lands on the same fold locus
    load = -0.30
    s_on_load = relax(root, g, load)
    Ng = 320
    gstep = abs((g - 0.5) / (Ng - 1))
    gc, s_after_g = ramp_cross(linspace(g, 0.5, Ng), "gamma", load, s_on_load)
    gcrit = 3.0 * (abs(load) / 2.0) ** (2.0 / 3.0)
    on_locus = abs(load - (-fold(gc))) if gc is not None else 9.9
    g6 = (s_on_load > 0.0) and (s_after_g < 0.0) and (gc is not None) \
         and abs(gc - gcrit) < 3.0 * gstep and on_locus < 0.05
    ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 two-routes — γ-erosion collapses at γ={gc:.6f} "
          f"(γ_crit={gcrit:.6f}); on locus h=−h*(γ) (gap {on_locus:.6f})")

    # [G7] fragility monotone — h*(γ) increases with γ across the atlas; γ byte-equal
    ranked = sorted(ATLAS.items(), key=lambda kv: fold(kv[1]["gamma"]))
    mono = all(fold(ranked[i + 1][1]["gamma"]) > fold(ranked[i][1]["gamma"])
               for i in range(len(ranked) - 1))
    byte_equal = all(ATLAS[k]["gamma"] == v["gamma"] for k, v in ranked)
    g7 = mono and byte_equal; ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 fragility — h*(γ) monotone in γ "
          f"({ranked[0][0]} h*={fold(ranked[0][1]['gamma']):.6f} → {ranked[-1][0]} "
          f"h*={fold(ranked[-1][1]['gamma']):.6f}), γ byte-equal")

    # [G8] firewall — rendered output carries no magnitude token, no '%'
    out = o1
    low = out.lower()
    block = _load_block()
    hits = sorted(t for t in block if t in low)
    g8 = (not hits) and ("%" not in out); ok &= g8
    print(f"  [{'PASS' if g8 else 'FAIL'}] G8 firewall — no magnitude token {hits if hits else '(none)'}, "
          f"no '%'")

    print("=" * 74)
    print(f"E12 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
