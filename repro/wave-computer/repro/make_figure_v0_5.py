#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.5 atlas figure from wave_inference_results.json (L4 resonance inference)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_inference_results.json"))

fig, ax = plt.subplots(2, 3, figsize=(18.2, 10.4))
fig.suptitle(
    "vp_wave_computer v0.5 — L4 resonance inference (the pivot)\n"
    "derive the gate (no oracle) · constraint satisfaction = settling · analogy = resonance · "
    "probabilistic = noisy settling  —  consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
    fontsize=12.2, fontweight="bold")

# ---- I1a: derive-the-gate, then route (gate inference + end-to-end vs rho) ----
a = ax[0, 0]
rc = r["I1_derive_then_route"]["rho_curve"]
rho = [x["rho"] for x in rc]
a.plot(rho, [x["gate_inference_acc"] for x in rc], marker="o", lw=2.6, color="#6a1b9a",
       label="gate DERIVED from raw cue")
a.plot(rho, [x["derived_instance_acc"] for x in rc], marker="s", lw=2.4, color="#1f7a3d",
       label="instance: DERIVED gate")
a.plot(rho, [x["oracle_instance_acc"] for x in rc], marker="^", lw=1.8, ls="--", color="#1f5fa6",
       label="instance: ORACLE gate (S4 bound)")
a.plot(rho, [x["flat_instance_acc"] for x in rc], marker="v", lw=1.8, ls=":", color="#888888",
       label="instance: FLAT (no gate)")
a.axhline(0.95, ls=":", color="grey", lw=1)
a.set_title("I1 — DERIVE the gate, then route  [V]\n"
            "(gate read from the cue; derived == oracle where separable)",
            fontweight="bold", fontsize=10.6)
a.set_xlabel("within-category jitter  rho")
a.set_ylabel("accuracy")
a.set_ylim(-0.04, 1.06)
a.legend(fontsize=8.0, loc="center left")
a.grid(alpha=0.25)
a.text(0.40, 0.06, "rho=0.4: upper geometry\nno longer separable →\ngate inference degrades",
       transform=a.transAxes, fontsize=7.8, color="#a33", fontweight="bold")

# ---- I1b: the derivability vs strict-separability TRADE-OFF (schema sweep) ----
b = ax[0, 1]
fc = r["I1_derived_capacity"]["frac_curve"]
sf = [x["schema_frac"] for x in fc]
b.plot(sf, [x["gate_inference_acc"] for x in fc], marker="o", lw=2.6, color="#6a1b9a",
       label="gate inference (derivability)")
b.plot(sf, [x["oracle_strict_acc"] for x in fc], marker="s", lw=2.4, color="#c0392b",
       label="ORACLE strict recall (separability)")
b.plot(sf, [x["derived_id_acc"] for x in fc], marker="^", lw=2.2, color="#1f7a3d",
       label="DERIVED id (which instance)")
b.plot(sf, [x["flat_id_acc"] for x in fc], marker="v", lw=1.8, ls=":", color="#888888",
       label="FLAT id")
b.axhline(0.9, ls=":", color="grey", lw=1)
b.set_title("I1-stress — derivability ⊥ strict-separability  [O]\n"
            "(gate↑ forces strict↓: no point has both)  id-advantage survives  [V]",
            fontweight="bold", fontsize=10.6)
b.set_xlabel("schema fraction (shared category structure)")
b.set_ylabel("accuracy")
b.set_ylim(-0.04, 1.06)
b.legend(fontsize=8.0, loc="center right")
b.grid(alpha=0.25)

# ---- I2: constraint satisfaction = settling (frustration vs optimum vs random) ----
c = ax[0, 2]
sbf = r["I2_constraint_satisfaction"]["satisfied_by_frustration"]
f = [x["frustration"] for x in sbf]
ach = [x["satisfied_bestof"] for x in sbf]
opt = [1.0 / (1.0 + ff) for ff in f]
c.plot(f, ach, marker="o", lw=2.6, color="#1f7a3d", label="settling achieves (best-of)")
c.plot(f, opt, marker="s", lw=2.0, ls="--", color="#1f5fa6", label="optimum 1/(1+f)")
c.axhline(r["I2_constraint_satisfaction"]["random_baseline"], ls=":", color="#c0392b", lw=1.6,
          label="random colouring (0.5)")
c.set_title("I2 — CONSTRAINT SATISFACTION = SETTLING  [V]\n"
            "(solves satisfiable ~1.0 ≫ random; tracks the frustration optimum)",
            fontweight="bold", fontsize=10.6)
c.set_xlabel("frustration f (odd-cycle edges added)")
c.set_ylabel("satisfied-edge fraction")
c.set_ylim(0.4, 1.04)
c.legend(fontsize=8.2, loc="lower left")
c.grid(alpha=0.25)

# ---- I3: analogy = resonance (fill + proportional analogy vs role load) ----
d = ax[1, 0]
fl = r["I3_analogy_resonance"]["fill_curve"]
an = r["I3_analogy_resonance"]["analogy_curve"]
J = [x["J_roles"] for x in fl]
d.plot(J, [x["fill_acc"] for x in fl], marker="o", lw=2.6, color="#1f7a3d",
       label="fill a missing factor")
d.plot(J, [x["analogy_acc"] for x in an], marker="s", lw=2.4, color="#e08a1e",
       label="proportional analogy A:B::C:?")
d.axhline(0.95, ls=":", color="grey", lw=1)
jf = r["I3_analogy_resonance"]["useful_fill_load_Jstar"]
ja = r["I3_analogy_resonance"]["useful_analogy_load_Jstar"]
d.set_title("I3 — ANALOGY = RESONANCE  [V]\n"
            f"(fill robust J*≥{jf}; analogy ceiling J*={ja} = honest crosstalk limit)",
            fontweight="bold", fontsize=10.6)
d.set_xlabel("role load J (terms bundled per record)")
d.set_ylabel("accuracy")
d.set_ylim(-0.04, 1.06)
d.legend(fontsize=8.4, loc="lower left")
d.grid(alpha=0.25)

# ---- I4: probabilistic = noisy settling (temperature -> sampling; prior/evidence inset) ----
e = ax[1, 1]
tc = r["I4_probabilistic_settling"]["temperature_curve"]
T = [x["temperature"] for x in tc]
ent = [x["occupancy_entropy_bits"] for x in tc]
e.plot(T, ent, marker="o", lw=2.6, color="#6a1b9a", label="occupancy entropy (sampling)")
e.set_title("I4 — PROBABILISTIC = NOISY SETTLING  [V]\n"
            "(temperature ↑ → entropy ↑: noise = sampling, attractor = MAP)",
            fontweight="bold", fontsize=10.6)
e.set_xlabel("temperature T  (small N: shallow basins)")
e.set_ylabel("occupancy entropy (bits)")
e.set_ylim(-0.03, 1.05)
e.grid(alpha=0.25)
e.legend(fontsize=8.4, loc="upper left")
# inset: prior & evidence laws (p_A vs sweep)
pr = r["I4_probabilistic_settling"]["prior_curve"]
ev = r["I4_probabilistic_settling"]["evidence_curve"]
ei = e.inset_axes([0.56, 0.12, 0.4, 0.42])
ei.plot(range(len(pr)), [x["p_A_sampled"] for x in pr], marker="o", lw=1.8, color="#1f7a3d",
        label="prior↑")
ei.plot(range(len(ev)), [x["p_A_sampled"] for x in ev], marker="s", lw=1.8, color="#1f5fa6",
        label="evidence↑")
ei.set_title("Bayes laws", fontsize=7.6)
ei.set_ylabel("p(A)", fontsize=7.2)
ei.set_xticks([])
ei.tick_params(labelsize=6.6)
ei.legend(fontsize=6.4, loc="lower right")
ei.grid(alpha=0.2)

# ---- verdict panel ----
v = ax[1, 2]
v.axis("off")
h = r["headline"]
lines = [
    "L4 — RESONANCE INFERENCE  (the pivot): verdict",
    "",
    f"I1  derive the gate, then route ............ {h['grade_I1_derive_then_route']}",
    f"      gate read from raw cue, no oracle (sep. band acc {h['I1_mean_gate_inference_acc_separable']:.2f})",
    f"I1' strict capacity under derivation ....... {h['grade_I1_strict_capacity']}  (honest negative)",
    f"      derivability ⊥ strict-separability trade-off {h['grade_I1_tradeoff_mechanism']}",
    f"      (id-level advantage survives; strict needs a context channel → L5)",
    f"I2  constraint satisfaction = settling ..... {h['grade_I2_constraint_settling']}",
    f"I3  analogy = resonance .................... {h['grade_I3_analogy']}",
    f"I4  probabilistic = noisy settling ......... {h['grade_I4_probabilistic']}",
    "",
    "→ Inference WITHOUT computation HOLDS on the",
    "   cognitive forms (gate, CSP, analogy, sampling).",
    "   One principled limit: strict-fidelity capacity",
    "   needs an independently-supplied context, not",
    "   content-only derivation. No hybrid forced; the",
    "   limit is recorded for L5 (dual systems).",
    "",
    "firewall: consciousness_claim = 0,  hard_problem_open = 1",
    "discipline: every claim swept · honest negatives kept ·",
    "no tuning · deterministic · brain R/WM anchors NOT transferred",
]
v.text(0.02, 0.98, "\n".join(lines), transform=v.transAxes, fontsize=9.0,
       va="top", ha="left", family="monospace",
       bbox=dict(boxstyle="round,pad=0.6", fc="#f5f3ef", ec="#6a1b9a", lw=1.4))

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("wave_inference_atlas.png", dpi=120)
print("wrote wave_inference_atlas.png")
