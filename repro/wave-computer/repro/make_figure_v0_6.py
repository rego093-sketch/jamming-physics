#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.6 atlas figure from wave_consolidation_results.json (L5 dual learning
systems: fast episodic + slow semantic; offline-replay consolidation; the L4 [O]->[V])."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_consolidation_results.json"))

fig, ax = plt.subplots(2, 3, figsize=(18.2, 10.4))
fig.suptitle(
    "vp_wave_computer v0.6 — L5 dual learning systems (fast episodic + slow semantic)\n"
    "offline-replay consolidation · catastrophic-forgetting stress · the L4 [O]->[V] closure "
    "(independent context channel)  —  consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
    fontsize=12.0, fontweight="bold")

# ---- C1a: consolidation -> a slow store that GENERALISES (vs stream length) ----
a = ax[0, 0]
c1 = r["C1_consolidation_prototype"]
Lc = c1["L_curve"]
L = [x["L_stream"] for x in Lc]
base = c1["single_instance_baseline"]
a.plot(L, [x["semantic_proto_overlap"] for x in Lc], marker="o", lw=2.8, color="#1f7a3d",
       label="SLOW (consolidated) store")
a.plot(L, [x["episodic_proto_overlap"] for x in Lc], marker="s", lw=2.2, ls="--", color="#1f5fa6",
       label="FAST (episodic) store")
a.axhline(base, ls=":", color="#a33", lw=1.4, label=f"single-instance baseline (1-2rho={base:.2f})")
a.set_title("C1 — consolidation builds a generalising slow store  [V]\n"
            "(slow generalises to NOVEL instances, > baseline; but does NOT beat fast)",
            fontweight="bold", fontsize=10.4)
a.set_xlabel("stream length  L  (episodes / category, replay=3)")
a.set_ylabel("overlap with TRUE prototype (novel probes)")
a.set_xticks(L)
a.set_ylim(0.5, 1.04)
a.legend(fontsize=8.2, loc="lower right")
a.grid(alpha=0.25)
a.text(0.03, 0.06, "both Hebbian stores\nsuperpose -> emergent\nprototype (see C4)",
       transform=a.transAxes, fontsize=7.8, color="#555", fontweight="bold")

# ---- C1b: extra replay gives NO further gain (re-samples a fixed biased set) ----
b = ax[0, 1]
rc = c1["replay_curve"]
rp = [x["replay"] for x in rc]
b.plot(rp, [x["semantic_proto_overlap"] for x in rc], marker="o", lw=2.8, color="#1f7a3d",
       label="SLOW store (L=8)")
b.plot(rp, [x["episodic_proto_overlap"] for x in rc], marker="s", lw=2.2, ls="--", color="#1f5fa6",
       label="FAST store (L=8)")
b.axhline(base, ls=":", color="#a33", lw=1.4)
b.set_title("C1-bound — extra replay does NOT keep denoising  [honest]\n"
            "(each cycle re-samples the same fixed biased instance set)",
            fontweight="bold", fontsize=10.4)
b.set_xlabel("replay cycles  (offline reactivations)")
b.set_ylabel("overlap with TRUE prototype")
b.set_xticks(rp)
b.set_ylim(0.5, 1.04)
b.legend(fontsize=8.2, loc="lower left")
b.grid(alpha=0.25)

# ---- C2: dual reduces CATASTROPHIC FORGETTING vs single store (vs K tasks) ----
c = ax[0, 2]
c2 = r["C2_catastrophic_forgetting"]
Kc = c2["K_curve"]
K = [x["K_tasks"] for x in Kc]
single = [x["single_store_forgetting"] for x in Kc]
dual = [x["dual_store_forgetting"] for x in Kc]
c.plot(K, single, marker="v", lw=2.6, color="#c0392b", label="SINGLE store (palimpsest)")
c.plot(K, dual, marker="o", lw=2.8, color="#1f7a3d", label="DUAL (+ slow additive store)")
c.fill_between(K, dual, single, color="#1f7a3d", alpha=0.10)
c.set_title("C2 — dual reduces catastrophic forgetting  [V]\n"
            "(dual << single at every load; honest: dual itself grows slowly)",
            fontweight="bold", fontsize=10.4)
c.set_xlabel("number of sequential tasks  K")
c.set_ylabel("task-0 forgetting  (acc drop, paired probes)")
c.set_xticks(K)
c.set_ylim(-0.04, 0.8)
c.legend(fontsize=8.4, loc="upper left")
c.grid(alpha=0.25)

# ---- C3: THE L4 [O]->[V] CLOSURE — strict recovery vs load (4 arms) ----
d = ax[1, 0]
c3 = r["C3_context_channel_capacity"]
Tc = c3["T_curve"]
T = [x["T"] for x in Tc]
d.plot(T, [x["oracle_strict_acc"] for x in Tc], marker="^", lw=1.9, ls="--", color="#1f5fa6",
       label="ORACLE gate")
d.plot(T, [x["context_strict_acc"] for x in Tc], marker="o", lw=2.9, color="#6a1b9a",
       label="CONTEXT channel (L5)")
d.plot(T, [x["content_strict_acc"] for x in Tc], marker="s", lw=2.4, color="#1f7a3d",
       label="CONTENT-derived (L4's loser)")
d.plot(T, [x["flat_strict_acc"] for x in Tc], marker="v", lw=1.8, ls=":", color="#888888",
       label="FLAT (no gate)")
d.axhline(0.9, ls=":", color="grey", lw=1)
d.set_title("C3 — L4 [O]->[V]: independent context channel  [V]\n"
            "(context ~ ORACLE >> content >> flat at the strict wall)",
            fontweight="bold", fontsize=10.4)
d.set_xlabel("load  T = B x m  (m independent instances / category)")
d.set_ylabel("STRICT recovery  (overlap >= 0.95)")
d.set_xticks(T)
d.set_ylim(-0.04, 1.06)
d.legend(fontsize=8.2, loc="center left")
d.grid(alpha=0.25)

# ---- C3-robustness: context channel vs context-cue corruption ----
e = ax[1, 1]
cc = c3["ctx_curve"]
cx = [x["ctx_corrupt"] for x in cc]
e.plot(cx, [x["gate_context_acc"] for x in cc], marker="o", lw=2.8, color="#6a1b9a",
       label="context GATE accuracy")
e.plot(cx, [x["context_strict_acc"] for x in cc], marker="s", lw=2.4, color="#1f7a3d",
       label="context STRICT recovery")
e.axhline(0.9, ls=":", color="grey", lw=1)
e.set_title("C3-stress — robust to context-cue corruption  [V]\n"
            f"(gate >= 0.9 up to corruption {c3['context_cue_robustness_boundary']:.1f}; recorded boundary)",
            fontweight="bold", fontsize=10.4)
e.set_xlabel("context-cue corruption  (flip fraction on the tag)")
e.set_ylabel("accuracy")
e.set_xticks(cx)
e.set_ylim(-0.04, 1.06)
e.legend(fontsize=8.4, loc="lower left")
e.grid(alpha=0.25)

# ---- C4: the CLS dissociation — SINGLE holds, DOUBLE does not (vs rho) ----
f = ax[1, 2]
c4 = r["C4_cls_dissociation"]
roc = c4["rho_curve"]
rho = [x["rho"] for x in roc]
f.plot(rho, [x["fast_memorization"] for x in roc], marker="o", lw=2.6, color="#c0392b",
       label="FAST memorisation")
f.plot(rho, [x["slow_memorization"] for x in roc], marker="o", lw=2.2, ls="--", color="#e08a2e",
       label="SLOW memorisation")
f.plot(rho, [x["fast_generalization"] for x in roc], marker="s", lw=2.6, color="#1f5fa6",
       label="FAST generalisation")
f.plot(rho, [x["slow_generalization"] for x in roc], marker="s", lw=2.2, ls="--", color="#1f7a3d",
       label="SLOW generalisation")
f.set_title("C4 — CLS double dissociation does NOT hold  [O]\n"
            "(single dissociation only: FAST also generalises via superposition)",
            fontweight="bold", fontsize=10.4)
f.set_xlabel("within-category spread  rho")
f.set_ylabel("accuracy")
f.set_xticks(rho)
f.set_ylim(-0.04, 1.06)
f.legend(fontsize=7.8, loc="center left")
f.grid(alpha=0.25)
f.text(0.50, 0.06, "fast gen ~ 1.0 everywhere\n=> slow never wins gen\n=> no double dissociation",
       transform=f.transAxes, fontsize=7.8, color="#a33", fontweight="bold")

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("wave_consolidation_atlas.png", dpi=120, bbox_inches="tight")
print("wrote wave_consolidation_atlas.png")
