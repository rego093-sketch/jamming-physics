#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.3 atlas figure from wave_structure_results.json."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_structure_results.json"))
N = 512

fig, ax = plt.subplots(2, 2, figsize=(12.8, 9.4))
fig.suptitle("vp_wave_computer v0.3 — L1 representation COMPLETE (permute · tree depth) + L2 START (trajectory · theta-gamma WM)\n"
             "from a static set to ordered structure and dynamic sequence  —  "
             "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
             fontsize=11.8, fontweight="bold")

# ---- L1a: permute -> ordered sequence recall vs length ----
a = ax[0, 0]
seq = r["L1a_permute_sequence"]
L = [s["L"] for s in seq]
acc = [s["position_recall_acc"] for s in seq]
sd = [s["position_recall_sd"] for s in seq]
a.errorbar(L, acc, yerr=sd, marker="o", lw=2.2, capsize=3, color="#1f5fa6",
           label="position-indexed recall")
a.axhline(0.95, ls=":", color="grey", lw=1)
cap = r["headline"]["L1_permute_ordered_capacity_L"]
a.axvline(cap, ls="--", color="#c0392b", lw=1.4, label=f"useful length L*≈{cap}")
a.set_title("L1a — PERMUTE closes the algebra\n(bind · bundle · permute -> ordered sequence)",
            fontweight="bold", fontsize=10.5)
a.set_xlabel("sequence length encoded in ONE wave,  L")
a.set_ylabel("position recall accuracy")
a.set_ylim(0.5, 1.04)
a.legend(fontsize=9, loc="lower left")
a.grid(alpha=0.25)

# ---- L1b: tree depth-capacity (both branchings) ----
b = ax[0, 1]
colors = {"b2": "#1f7a3d", "b3": "#7d3c98"}
for key, blk in r["L1b_tree_depth"].items():
    d = [x["depth"] for x in blk["curve"]]
    acc = [x["structured_query_acc"] for x in blk["curve"]]
    sd = [x["acc_sd"] for x in blk["curve"]]
    ds = blk["useful_depth_d_star"]
    b.errorbar(d, acc, yerr=sd, marker="o", lw=2.2, capsize=3, color=colors[key],
               label=f"branching b={blk['branching']}  (d*={ds})")
b.axhline(0.95, ls=":", color="grey", lw=1)
b.set_title("L1b — role-value TREE depth-capacity\n(milestone + stress: crosstalk collapse with depth)",
            fontweight="bold", fontsize=10.5)
b.set_xlabel("tree depth queried,  d")
b.set_ylabel("structured-query accuracy")
b.set_ylim(0.0, 1.05)
b.legend(fontsize=9, loc="lower left")
b.grid(alpha=0.25)
b.text(0.55, 0.40, "useful depth is SHALLOW\n-> L3 hierarchy needed\nfor deeper structure",
       transform=b.transAxes, fontsize=8.5, color="#555555", fontweight="bold")

# ---- L2a: heteroclinic replay vs lambda (predict-next + ordered replay) ----
c = ax[1, 0]
het = r["L2a_heteroclinic"]
lam = [x["lambda"] for x in het["curve"]]
pn = [x["predict_next_acc"] for x in het["curve"]]
pnsd = [x["predict_next_sd"] for x in het["curve"]]
rep = [x["ordered_replay_mean"] for x in het["curve"]]
repsd = [x["ordered_replay_sd"] for x in het["curve"]]
c.errorbar(lam, pn, yerr=pnsd, marker="o", lw=2.2, capsize=3, color="#1f7a3d",
           label="predict-next (single hop μ→μ+1)  [V]")
c.errorbar(lam, rep, yerr=repsd, marker="s", lw=2.2, capsize=3, color="#e08a1e",
           label="sustained full-cycle replay  [V]")
c.axhline(1.0 / 6, ls=":", color="#c0392b", lw=1, label="stuck at fixed point (1/m)")
band = het["replay_band_lambda"]
if band:
    c.axvspan(min(band), max(band), color="#1f7a3d", alpha=0.08)
c.set_title("L2a — metastable TRAJECTORY (delayed-asymmetric)\n(sequence learn → replay → predict; sweep coupling λ)",
            fontweight="bold", fontsize=10.5)
c.set_xlabel("asymmetric (delayed) coupling strength,  λ")
c.set_ylabel("accuracy / fraction of cycle in order")
c.set_ylim(-0.03, 1.06)
c.legend(fontsize=8.3, loc="center right")
c.grid(alpha=0.25)

# ---- L2b: theta-gamma WM capacity vs jitter for each n_slot ----
d = ax[1, 1]
grid = r["L2b_theta_gamma_wm"]["grid"]
nslots = sorted({g["n_slot"] for g in grid})
pal = ["#1f5fa6", "#1f7a3d", "#e08a1e", "#c0392b"]
for i, ns in enumerate(nslots):
    sub = [g for g in grid if g["n_slot"] == ns]
    j = [g["jitter_sigma"] for g in sub]
    capm = [g["wm_capacity_mean"] for g in sub]
    d.plot(j, capm, marker="o", lw=2.0, color=pal[i % len(pal)],
           label=f"{ns} gamma slots")
    d.axhline(ns, ls=":", color=pal[i % len(pal)], lw=0.8, alpha=0.5)
d.axhspan(4, 9, color="grey", alpha=0.10, label="Miller range (4–9)")
d.set_title("L2b — THETA-GAMMA working memory\n(capacity = min(slots, precision limit); ~7 = 7 slots, not transferred)",
            fontweight="bold", fontsize=10.5)
d.set_xlabel("gamma-slot phase jitter,  σ  (finite precision)")
d.set_ylabel("WM capacity (items recalled)")
d.legend(fontsize=8.0, loc="upper right")
d.grid(alpha=0.25)

fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("wave_structure_atlas.png", dpi=140, bbox_inches="tight")
print("wrote wave_structure_atlas.png")
