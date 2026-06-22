#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.7 atlas from wave_world_model_results.json (L6 self-supervised world model:
prediction = forward settling; error = difference wave; error-gated delta rule. The learned
operator is DIRECTIONALLY the L2 transition coupling but halts at prediction-sufficiency)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_world_model_results.json"))
w1, w2, w3, w4 = (r["W1_learning_curve"], r["W2_rollout"],
                  r["W3_surprise"], r["W4_forward_vs_reactive"])

fig, ax = plt.subplots(2, 3, figsize=(18.2, 10.4))
fig.suptitle(
    "vp_wave_computer v0.7 — L6 self-supervised world model "
    "(prediction = forward settling; error = difference wave)\n"
    "self-supervised error reduction · generative rollout · novelty/surprise · "
    "forward model > reactive recall (the C4 break)  —  "
    "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
    fontsize=12.0, fontweight="bold")

# ---- W1a: self-supervised learning curve (held-out error vs exposures, per m) ----
a = ax[0, 0]
ec = w1["exposure_curve"]
ms = sorted({x["m"] for x in ec})
cols = {ms[0]: "#1f5fa6", ms[1]: "#1f7a3d", ms[2]: "#6a1b9a"}
for m in ms:
    pts = [x for x in ec if x["m"] == m]
    E = [x["exposures"] for x in pts]
    er = [x["heldout_error"] for x in pts]
    a.plot(E, er, marker="o", lw=2.6, color=cols[m], label=f"m={m} (stream length)")
a.axhline(w1["trained_plateau"], ls=":", color="#a33", lw=1.4,
          label=f"low plateau = {w1['trained_plateau']:.2f}")
a.set_title("W1 — self-supervised prediction-error reduction  [V]\n"
            "(held-out next-step error from FRESH cues vs TRUE successor; non-circular)",
            fontweight="bold", fontsize=10.4)
a.set_xlabel("training exposures  (offline self-supervised passes)")
a.set_ylabel("held-out next-step error  (1 - overlap)")
a.set_xticks(E)
a.set_ylim(-0.04, 1.06)
a.legend(fontsize=8.4, loc="upper right")
a.grid(alpha=0.25)
a.text(0.5, 0.55, "error gated:\nstops when right",
       transform=a.transAxes, fontsize=7.8, color="#555", fontweight="bold")

# ---- W1b: learned operator vs the analytic L2 coupling (cosine vs exposures) ----
b = ax[0, 1]
for m in ms:
    pts = [x for x in ec if x["m"] == m]
    E = [x["exposures"] for x in pts]
    cs = [x["l2_coupling_cosine"] for x in pts]
    b.plot(E, cs, marker="s", lw=2.6, color=cols[m], label=f"m={m}")
b.axhline(0.9, ls="--", color="#c0392b", lw=1.6, label="magnitude-identity (cos=0.9)")
b.axhline(w1["l2_coupling_cosine_mean"], ls=":", color="#1f7a3d", lw=1.6,
          label=f"reached plateau = {w1['l2_coupling_cosine_mean']:.2f}")
b.set_title("W1-operator — directionally L2, NOT identity  [V align / O identity]\n"
            "(error-gating halts at prediction-sufficiency: the layer's open limit -> L7)",
            fontweight="bold", fontsize=10.4)
b.set_xlabel("training exposures")
b.set_ylabel("cosine(J_asym, analytic L2 transition coupling)")
b.set_xticks(E)
b.set_ylim(-0.04, 1.06)
b.legend(fontsize=8.0, loc="center right")
b.grid(alpha=0.25)

# ---- W2: generative rollout — fidelity vs horizon (iterated forward settling) ----
c = ax[0, 2]
hc = w2["horizon_curve"]
k = [x["step"] for x in hc]
fid = [x["fidelity"] for x in hc]
c.plot(k, fid, marker="o", lw=2.8, color="#1f7a3d", label="rollout fidelity")
c.axhline(w2["fidelity_thresh"], ls=":", color="grey", lw=1.2,
          label=f"faithful thresh = {w2['fidelity_thresh']:.2f}")
db = w2["drift_below_threshold_at_step"]
c.axvline(db, ls="--", color="#c0392b", lw=1.6, label=f"drift onset @ step {db}")
c.set_title("W2 — generative rollout to a finite horizon  [V]\n"
            f"(on-manifold for {w2['onmanifold_steps_min']} steps, then crosstalk drift; honest bound)",
            fontweight="bold", fontsize=10.4)
c.set_xlabel("rollout step  k  (iterated self-prediction)")
c.set_ylabel("fidelity to the true continuation")
c.set_xticks(k)
c.set_ylim(-0.04, 1.06)
c.legend(fontsize=8.2, loc="lower left")
c.grid(alpha=0.25)

# ---- W3: novelty / surprise — error-wave magnitude vs violation degree ----
d = ax[1, 0]
vc = w3["violation_curve"]
vio = [x["violation"] for x in vc]
sur = [x["surprise"] for x in vc]
sd = [x["surprise_sd"] for x in vc]
d.errorbar(vio, sur, yerr=sd, marker="o", lw=2.8, color="#6a1b9a", capsize=3,
           label="surprise (|error wave|)")
d.axhline(w3["familiar_surprise"], ls=":", color="#1f7a3d", lw=1.4,
          label=f"familiar = {w3['familiar_surprise']:.2f}")
d.axvline(w3["detection_threshold_violation"], ls="--", color="#c0392b", lw=1.6,
          label=f"detect boundary = {w3['detection_threshold_violation']:.2f}")
d.set_title("W3 — novelty flagged by the prediction-error wave  [V]\n"
            f"(graded; familiar~0, full violation~{w3['novel_surprise']:.2f}, margin {w3['novelty_margin']:.2f})",
            fontweight="bold", fontsize=10.4)
d.set_xlabel("transition-violation degree  (fraction of successor flipped)")
d.set_ylabel("surprise  (mean error-wave magnitude)")
d.set_ylim(-0.04, 1.06)
d.legend(fontsize=8.2, loc="upper left")
d.grid(alpha=0.25)

# ---- W4: forward model vs reactive recall, across (m, noise) ----
e = ax[1, 1]
mc = w4["main_curve"]
labels = [f"m{x['m']}\n{x['noise']}" for x in mc]
idx = np.arange(len(mc))
fwd = [x["forward_acc"] for x in mc]
rea = [x["reactive_acc"] for x in mc]
ww = 0.4
e.bar(idx - ww/2, fwd, ww, color="#1f7a3d", label="FORWARD model (L6)")
e.bar(idx + ww/2, rea, ww, color="#c0392b", label="REACTIVE recall (saw every transition)")
e.set_title("W4 — forward model anticipates; reactive returns present  [V]\n"
            "(the C4 break: advantage is DIRECTIONALITY/structure, not a missing abstraction)",
            fontweight="bold", fontsize=10.4)
e.set_xlabel("condition  (stream length m / cue noise)")
e.set_ylabel("next-step accuracy")
e.set_xticks(idx)
e.set_xticklabels(labels, fontsize=7.0)
e.set_ylim(-0.04, 1.06)
e.legend(fontsize=8.2, loc="center right")
e.grid(alpha=0.25, axis="y")

# ---- W4-honest: the regimes where the gap vanishes (recorded negatives) ----
f = ax[1, 2]
groups = ["TRAINED\n(main)", "FIXED-POINT\nstream", "UNTRAINED\nmodel"]
fwd_g = [float(np.mean(fwd)), w4["fixedpoint_forward_acc"], w4["untrained_forward_acc"]]
rea_g = [float(np.mean(rea)), w4["fixedpoint_reactive_acc"], w4["untrained_reactive_acc"]]
gi = np.arange(len(groups))
f.bar(gi - ww/2, fwd_g, ww, color="#1f7a3d", label="FORWARD")
f.bar(gi + ww/2, rea_g, ww, color="#c0392b", label="REACTIVE")
f.set_title("W4-honest — where the forward advantage vanishes  [honest]\n"
            "(fixed-point: no direction to exploit; untrained: no model yet)",
            fontweight="bold", fontsize=10.4)
f.set_xlabel("regime")
f.set_ylabel("next-step accuracy")
f.set_xticks(gi)
f.set_xticklabels(groups, fontsize=8.4)
f.set_ylim(-0.04, 1.06)
f.legend(fontsize=8.4, loc="upper right")
f.grid(alpha=0.25, axis="y")
f.text(0.30, 0.40, "gap present\nonly when the\nstream HAS\nstructure",
       transform=f.transAxes, fontsize=7.6, color="#a33", fontweight="bold")

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("wave_world_model_atlas.png", dpi=120, bbox_inches="tight")
print("wrote wave_world_model_atlas.png")
