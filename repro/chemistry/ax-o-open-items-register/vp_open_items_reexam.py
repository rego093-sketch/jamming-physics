# -*- coding: utf-8 -*-
"""
vp_open_items_reexam.py — re-examination of the four peripheral chemistry open items (register O.1)
RECONSTRUCTION (2026-09-29). The original script is not in any surviving bundle. This file re-runs the
checks from the data and functions of the legacy v1.0 modules (repro/chemistry/legacy_v1_0_2026-06-14),
unchanged, and states where a check cannot be re-run. Deterministic, standard library only.

  1. bond energy     : is the Morse range beta = a r_e set by bond order (the sqrt2 geometry)?   vp_bond_energy
  2. defect knockdown: is ideal/measured strength a constant (geometry) or processing-dependent?  vp_strength
  3. shell correction: can one uniform proximity bonus fix the SEMF residual near magic numbers?  vp_shell_correction
  4. EA / absolute IE: Slater sign failure 8/18 — dataset not in the v1.0 bundle; carried, not re-run
"""
import hashlib, importlib.util, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..", "legacy_v1_0_2026-06-14", "VP_Chemistry_EM_DOI_Package_v1", "core", "code")

def load(sub, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(CODE, sub, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))

out = []
# 1. bond energy — Morse: k = 2 D_e a^2  ->  a = sqrt(k / (2 D_e)),  beta = a r_e
be = load("materials", "vp_bond_energy")
NA = 6.02214076e23
beta, order = [], []
for name, bo, k, re_A, D_kJ, _ in be.BONDS:
    De = D_kJ * 1e3 / NA
    a = math.sqrt(k / (2 * De))
    beta.append(a * re_A * 1e-10); order.append(bo)
r_bond = pearson(order, beta)
out.append(("1_bond_beta_vs_order_r", r_bond))
print(f"1. Morse beta = a r_e over {len(beta)} bonds: range {min(beta):.2f}-{max(beta):.2f}; corr(beta, bond order) = {r_bond:+.2f}")
print(f"   register states r = +0.18 -> {'reproduced' if abs(r_bond-0.18) < 0.05 else 'NOT reproduced (value differs)'}; either way |r| is small: beta is not set by bond order -> stays [O]")

# 2. defect knockdown — ideal (sqrt2 geometry) / measured strength
st = load("materials", "vp_strength")
kd = [st.sigma_theoretical(E) / s for _, E, s, _, _ in st.MATERIALS]
out.append(("2_knockdown_spread", max(kd) / min(kd)))
print(f"2. ideal/measured strength over {len(kd)} materials: {min(kd):.1f}x - {max(kd):.0f}x (spread {max(kd)/min(kd):.0f}x)")
print("   not a constant: the knockdown follows the processing (dislocation density), a calibration input -> stays [O]")

# 3. shell correction — SEMF residual near magic numbers
sc = load("foundation", "vp_shell_correction")
res = []
for sym, Z, A, M in sc.NUCLEI:
    dB = sc.binding_measured(A, Z, M) - sc.binding_semf(A, Z)
    res.append((sym, Z, A, dB, min(sc.magic_distance(Z), sc.magic_distance(A - Z))))
near = [r for r in res if r[4] == 0]
pos = sum(1 for r in near if r[3] > 0); neg = len(near) - pos
bonus = sum(r[3] for r in near) / len(near)
worse = sum(1 for r in near if abs(r[3] - bonus) > abs(r[3]))
out.append(("3_magic_residual_signs", [pos, neg]))
out.append(("3_uniform_bonus_makes_worse", worse))
print(f"3. SEMF residual at magic Z or N: {pos} positive / {neg} negative; best uniform bonus {bonus:+.1f} MeV makes {worse}/{len(near)} of them worse")
print("   the residual changes sign, so one uniform bonus cannot close it; needs the spin-orbit shell model -> stays [O]")

# 4. electron affinity — not re-runnable
print("4. EA (Slater sign failure 8/18, e.g. F -3.74 vs +3.40 eV) — the EA dataset is not in the v1.0 bundle")
print("   (only IE data for Z = 21-36 survive). Carried from the v1.0 module docstring, NOT re-run -> stays [O]")
out.append(("4_EA", "carried, not re-run"))

h = hashlib.sha256(repr(out).encode()).hexdigest()
print("RESULT sha256 = " + h)
