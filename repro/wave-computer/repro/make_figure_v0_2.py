#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.2 atlas figure from wave_resonance_results.json."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_resonance_results.json"))
N = 512

fig, ax = plt.subplots(2, 2, figsize=(12.8, 9.4))
fig.suptitle("vp_wave_computer v0.2 — resonance / superposition / one-shot / parallelism\n"
             "the SUM of waves is information; matching is physics, not arithmetic  —  "
             "consciousness_claim=0, new_tuned_constants=0",
             fontsize=12.5, fontweight="bold")

# ---- R1: superposition recognition ----
a = ax[0, 0]
sup = r["R1_superposition"]
K = [s["K"] for s in sup]
acc = [s["recognition_acc"] for s in sup]
ab = [s["absent_score_sd"] for s in sup]
a.plot(K, acc, marker="o", lw=2.2, color="#1f5fa6", label="recognition accuracy")
a.fill_between(K, [1 - x for x in ab], 1.0, color="#1f5fa6", alpha=0.10,
               label="±crosstalk band (absent sd)")
a.axhline(0.95, ls=":", color="grey", lw=1)
cap = r["headline"]["superposition_recognition_capacity_K"]
a.axvline(cap, ls="--", color="#c0392b", lw=1.4,
          label=f"capacity K≈{cap} (~{cap/N:.0%} of N)")
a.set_title("R1 — SUM of waves = information\n(one composite holds K items; read by resonance)",
            fontweight="bold", fontsize=10.5)
a.set_xlabel("items superposed in ONE composite wave,  K")
a.set_ylabel("recognition accuracy")
a.set_ylim(0.5, 1.04)
a.legend(fontsize=8.5, loc="lower left")
a.grid(alpha=0.25)

# ---- R2: match steps vs P (the O(1) demonstration) ----
b = ax[0, 1]
ms = r["R2_match_steps"]
P = [m["P"] for m in ms]
st = [m["converge_steps_mean"] for m in ms]
sd = [m["converge_steps_sd"] for m in ms]
rs = [m["recall_success"] for m in ms]
b.errorbar(P, st, yerr=sd, marker="o", lw=2.2, capsize=3, color="#1f7a3d",
           label="wave settling steps (physical-time proxy)")
b.axhline(np.mean(st), ls="--", color="#1f7a3d", lw=1, alpha=0.6)
# overlay a hypothetical digital O(P) scan (arbitrary scale, to show contrast)
b.plot(P, [10 * p + 60 for p in P], ls=":", color="#c0392b", lw=2,
       label="digital scan O(P) (illustrative)")
b.set_title("R2 — MATCH without compute, O(1) in P\n(steps flat as #stored grows -> physics tests all at once)",
            fontweight="bold", fontsize=10.5)
b.set_xlabel("number of patterns stored in one field,  P")
b.set_ylabel("steps to converge")
b.set_ylim(0, max(10 * max(P) + 60, max(st)) * 1.1)
b.legend(fontsize=8.5, loc="upper left")
b.grid(alpha=0.25)
# annotate flatness
spread = r["headline"]["match_steps_spread_within_capacity"]
b.text(0.5 * max(P), np.mean(st) + 8, f"spread over P=2..{max(P)}: only {spread} steps",
       fontsize=8.5, color="#1f7a3d", fontweight="bold")

# ---- R3: one-shot online learning ----
c = ax[1, 0]
os_ = r["R3_one_shot"]
ns = [x["n_stored"] for x in os_]
jl = [x["recall_just_learned"] for x in os_]
rt = [x["recall_earlier_retained"] if x["recall_earlier_retained"] is not None else np.nan
      for x in os_]
c.plot(ns, jl, marker="o", ms=4, lw=2, color="#7d3c98",
       label="just-learned (1 exposure)")
c.plot(ns, rt, marker="s", ms=4, lw=2, color="#e08a1e",
       label="earlier pattern (retained)")
c.axhline(0.95, ls=":", color="grey", lw=1)
c.set_title("R3 — ONE-SHOT online learning (no backprop)\n(each pattern learned in 1 update; no catastrophic forgetting)",
            fontweight="bold", fontsize=10.5)
c.set_xlabel("patterns streamed (learned one-shot, in order)")
c.set_ylabel("recall overlap")
c.set_ylim(0.6, 1.03)
c.legend(fontsize=9, loc="lower left")
c.grid(alpha=0.25)

# ---- R4: scaling — cost vs P ----
d = ax[1, 1]
tp = r["R4_throughput"]
Pv = [x["P_stored"] for x in tp["cost_vs_P"]]
wave = [x["wave_physical_steps"] for x in tp["cost_vs_P"]]
dig = [x["digital_scan_ops"] for x in tp["cost_vs_P"]]
d.loglog(Pv, dig, marker="s", lw=2.2, color="#c0392b",
         label="digital / neural  O(P·N)")
d.loglog(Pv, wave, marker="D", lw=2.4, color="#1f7a3d",
         label="wave substrate  O(1) in P")
d.set_title("R4 — PARALLELISM: match cost vs #stored [O]\n(content-addressable in ~constant physical time)",
            fontweight="bold", fontsize=10.5)
d.set_xlabel("patterns stored,  P")
d.set_ylabel("cost to resolve one query")
d.legend(fontsize=9, loc="center left")
d.grid(alpha=0.25, which="both")
d.text(1e3, 4e2, "[O] projection\nhardware deferred", fontsize=8.5,
       color="#555555", ha="center")

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("wave_resonance_atlas.png", dpi=140, bbox_inches="tight")
print("wrote wave_resonance_atlas.png")
