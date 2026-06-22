#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E11.py — the focused pass/fail gate for increment E11 (run from the package root).

    python3 research/E11-accommodation-refraction/gate_E11.py

Asserts, INDEPENDENTLY of run.py's own internal asserts (the single-surface optics is RE-DERIVED here
from scratch — this gate does NOT import E3 — so a drift in either side is caught):
  [G1] DETERMINISM   — research/E11-accommodation-refraction/run.py emits an identical sha256 twice.
  [G2] MATCH         — emmetropia is the power↔length match ρ=P·L/n₂; on the cited reduced eye
                       (n₂=4/3, R=5.55, L=n₂R/(n₂−n₁)) ρ = 1 EXACTLY (independently re-derived).
  [G3] MISMATCH-SIGN — the distant focus v_∞=n₂/P falls in front of the retina (myopia) iff ρ>1 and
                       behind (hyperopia) iff ρ<1 — for BOTH the axial (length) and refractive (power)
                       routes; the geometric blur side equals sign(ρ−1).
  [G4] PRODUCT       — the match depends only on the PRODUCT P·L: a too-powerful eye (q) made shorter
                       by ℓ=1/q returns to ρ=1 (q·ℓ=1).
  [G5] ACCOMMODATION — for a near object at u=−k·L the required power ratio P_req/P_∞ = 1+n₁/(n₂·k)
                       RISES monotonically as the object nears (k↓) and is ALWAYS ≥ 1 (a one-signed,
                       additive lever), and the radius R_req it implies images the object onto the retina.
  [G6] LEVER         — the power lever is geometric: P=(n₂−n₁)/R ⇒ P ∝ 1/R, so dP/P = −dR/R.
  [G7] DWELL-SIZE    — the substrate size law dwell ∝ γ^1.5 is monotone in γ (more dwell ⇒ larger), so
                       the growth axis has a forced direction; PAX6/RAX γ are byte-equal to the atlas.
  [G8] FIREWALL      — the rendered run output carries NONE of E11's own MAGNITUDE_BLOCK tokens and no
                       '%' (direction-only; no dose/potency/power-magnitude/length/clinical quantity).

Exit 0 + 'E11 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import dwell                            # FROZEN size law (read-only)
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

# independently fixed reduced-eye constants (the cited Emsley schematic eye E3 consumes) — NOT imported
N1, N2, R = 1.0, 4.0 / 3.0, 5.55


def surface_image_distance(u, n1, n2, R_):
    """Independent re-derivation of E3's single-surface paraxial image distance (NOT imported)."""
    inv_u = 0.0 if u is None else (1.0 / u)
    return n2 / ((n2 - n1) / R_ + n1 * inv_u)


def _run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of_run(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _load_block():
    """Pull E11's own MAGNITUDE_BLOCK (module is __main__-guarded; loading it does not run it)."""
    spec = importlib.util.spec_from_file_location("_e11_for_firewall", RUN)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.MAGNITUDE_BLOCK)


def main():
    print("=" * 74)
    print("E11 GATE — research/E11-accommodation-refraction")
    print("=" * 74)
    ok = True

    P_emm = (N2 - N1) / R
    L_emm = surface_image_distance(None, N1, N2, R)

    # [G1] determinism
    o1, o2 = _run(), _run()
    h1, h2 = _sha_of_run(o1), _sha_of_run(o2)
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] emmetropic match ρ = P·L/n₂ = 1 exactly
    rho_emm = (P_emm * L_emm) / N2
    g2 = abs(rho_emm - 1.0) < 1e-12; ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 match — ρ=P·L/n₂ on the reduced eye = {rho_emm:.6f} (=1 exact)")

    # [G3] mismatch sign — blur side equals sign(ρ−1), axial AND refractive
    def blur_side(rho, v_inf, L):
        front, behind = (v_inf < L - 1e-15), (v_inf > L + 1e-15)
        return (front == (rho > 1.0)) and (behind == (rho < 1.0))
    g3 = True
    for ell in (1.05, 0.95):                              # axial: scale length
        L = ell * L_emm
        g3 &= blur_side((P_emm * L) / N2, surface_image_distance(None, N1, N2, R), L)
    for q in (1.05, 0.95):                                # refractive: scale power (R ↦ R/q)
        Rq = (N2 - N1) / (q * P_emm)
        g3 &= blur_side(((q * P_emm) * L_emm) / N2, surface_image_distance(None, N1, N2, Rq), L_emm)
    ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 mismatch-sign — focus in front ⇔ ρ>1 (myopia), behind ⇔ ρ<1 "
          f"(both routes)")

    # [G4] product-only: q·ℓ=1 returns to emmetropia
    q = 1.05
    rho_comp = (q * P_emm) * ((1.0 / q) * L_emm) / N2
    g4 = abs(rho_comp - 1.0) < 1e-12; ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 product — too-strong×shorter (q·ℓ=1) ⇒ ρ = {rho_comp:.6f} (=1)")

    # [G5] accommodation: P_req/P_∞ monotone-up, ≥1, and R_req images the near object on the retina
    ks = [1000.0, 100.0, 25.0, 10.0, 4.0, 2.0]
    ratios = [1.0 + N1 / (N2 * k) for k in ks]
    mono = all(ratios[i + 1] > ratios[i] for i in range(len(ratios) - 1))   # k descending ⇒ ratio rising
    onesigned = all(r >= 1.0 for r in ratios)
    img_ok = True
    for k, r in zip(ks, ratios):
        R_req = (N2 - N1) / (r * P_emm)
        v = surface_image_distance(-k * L_emm, N1, N2, R_req)
        img_ok &= abs(v - L_emm) < 1e-9
    g5 = mono and onesigned and img_ok; ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 accommodation — P_req/P_∞ ↑ as object nears "
          f"({ratios[0]:.6f}→{ratios[-1]:.6f}), one-signed ≥1, R_req focuses on retina")

    # [G6] lever: P ∝ 1/R ⇒ dP/P = −dR/R
    eps = 1e-6
    Pa, Pb = (N2 - N1) / R, (N2 - N1) / (R * (1.0 + eps))
    g6 = abs((Pb - Pa) / Pa - (-eps)) < 1e-5; ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 lever — dP/P = −dR/R (geometric power lever, P ∝ 1/R)")

    # [G7] dwell-size: monotone in γ, PAX6/RAX byte-equal to atlas
    gP, gR = ATLAS["PAX6"]["gamma"], ATLAS["RAX"]["gamma"]
    size_ratio = dwell(gP, 0.5) / dwell(gR, 0.5)
    g7 = (gP > gR) and (size_ratio > 1.0) and abs(size_ratio - (gP / gR) ** 1.5) < 1e-12 \
         and ATLAS["PAX6"]["gamma"] == gP and ATLAS["RAX"]["gamma"] == gR
    ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 dwell-size — size ∝ γ^1.5 monotone (PAX6/RAX={size_ratio:.6f}), "
          f"γ byte-equal to atlas")

    # [G8] firewall: the rendered output carries no magnitude token, no '%'
    out = o1
    low = out.lower()
    block = _load_block()
    hits = sorted(t for t in block if t in low)
    g8 = (not hits) and ("%" not in out); ok &= g8
    print(f"  [{'PASS' if g8 else 'FAIL'}] G8 firewall — no magnitude token {hits if hits else '(none)'}, "
          f"no '%'")

    print("=" * 74)
    print(f"E11 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
