#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.4 atlas figure from wave_hierarchy_results.json (L3 hierarchy + abstraction)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_hierarchy_results.json"))
N = 256

fig, ax = plt.subplots(2, 2, figsize=(12.8, 9.4))
fig.suptitle("vp_wave_computer v0.4 — L3 hierarchy & abstraction (nested phase coupling)\n"
             "slow phase gates fast sub-field · category from NOVEL instances · "
             "compositional generalization · nesting breaks the flat ceiling  —  "
             "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
             fontsize=11.6, fontweight="bold")

# ---- H1: nested gating -- slow phase SELECTS the cued fast sub-field vs B ----
a = ax[0, 0]
byB = r["H1_nested_gating"]["by_B"]
B = [x["B"] for x in byB]
cor = [x["gate_correct_instance_acc"] for x in byB]
wro = [x["gate_wrong_instance_acc"] for x in byB]
off = [x["gate_off_instance_acc"] for x in byB]
a.plot(B, cor, marker="o", lw=2.4, color="#1f7a3d", label="gate CORRECT (cued slow phase)")
a.plot(B, wro, marker="s", lw=2.2, color="#c0392b", label="gate WRONG (mismatched phase)")
a.plot(B, off, marker="^", lw=1.8, ls="--", color="#888888", label="gate OFF (= flat over all)")
a.axhline(0.95, ls=":", color="grey", lw=1)
sm = r["H1_nested_gating"]["select_margin_sharp"]
a.set_title("H1 — slow phase SELECTS fast sub-field\n"
            f"(levels separate; select margin correct−wrong = +{sm:.2f})  [V]",
            fontweight="bold", fontsize=10.5)
a.set_xlabel("number of category sub-fields,  B")
a.set_ylabel("instance recovery accuracy")
a.set_ylim(-0.04, 1.06)
a.legend(fontsize=8.4, loc="center right")
a.grid(alpha=0.25)
a.text(0.04, 0.30, "OFF==flat at light load\n→ capacity benefit\nmeasured in H4",
       transform=a.transAxes, fontsize=8.2, color="#555555", fontweight="bold")

# ---- H2: abstraction -- category(novel) vs instance vs rho; B-capacity inset ----
b = ax[0, 1]
rc = r["H2_abstraction"]["rho_curve"]
rho = [x["rho"] for x in rc]
catn = [x["category_acc_novel"] for x in rc]
inst = [x["instance_acc_stored"] for x in rc]
wsp = [x["within_spread"] for x in rc]
bdist = [x["between_distance"] for x in rc]
b.plot(rho, catn, marker="o", lw=2.4, color="#1f5fa6", label="category of NOVEL instance (abstraction)")
b.plot(rho, inst, marker="s", lw=2.2, color="#e08a1e", label="instance recall (lower level)")
b.plot(rho, wsp, marker=".", lw=1.4, ls="--", color="#7d3c98", label="within-category spread")
b.plot(rho, bdist, marker=".", lw=1.4, ls=":", color="#555555", label="between-category distance")
b.axhline(0.95, ls=":", color="grey", lw=1)
maxc = r["headline"]["H2_max_categories"]
b.set_title("H2 — ABSTRACTION: category from NOVEL instances\n"
            f"(prototype basins; up to {maxc} categories abstracted)  [V]",
            fontweight="bold", fontsize=10.5)
b.set_xlabel("instance jitter from prototype,  rho")
b.set_ylabel("accuracy / geometry")
b.set_ylim(-0.04, 1.08)
b.legend(fontsize=7.8, loc="center left")
b.grid(alpha=0.25)
b.text(0.52, 0.12, "category stays 1.0 as instances\ndiverge → levels genuinely separate",
       transform=b.transAxes, fontsize=8.0, color="#1f5fa6", fontweight="bold")

# ---- H3: compositional generalization -- enum vs held-out vs load (+depth) ----
c = ax[1, 0]
lc = r["H3_compositional"]["load_curve"]
combos = [x["combinations"] for x in lc]
en = [x["enumerated_decode_acc"] for x in lc]
ho = [x["heldout_decode_acc"] for x in lc]
gv = [x["generated_is_category_valid"] for x in lc]
gn = [x["generated_is_novel"] for x in lc]
c.plot(combos, en, marker="o", lw=2.4, color="#1f7a3d", label="ENUMERATED combos decode")
c.plot(combos, ho, marker="s", lw=2.2, ls="--", color="#c0392b", label="HELD-OUT (never-built) decode")
c.plot(combos, gv, marker="^", lw=1.6, color="#1f5fa6", label="generated = valid member")
c.plot(combos, gn, marker="v", lw=1.6, color="#e08a1e", label="generated = genuinely novel")
c.axhline(0.95, ls=":", color="grey", lw=1)
dc = r["H3_compositional"]["depth_curve"]
d3 = [x for x in dc if x["depth"] == 3][0]["levels"]
c.set_title("H3 — COMPOSITIONAL generalization (zero gap)\n"
            f"depth-3 decode: sup={d3['superordinate']:.2f}/cat={d3['category']:.2f}/mod={d3['modifier']:.2f}  [V]",
            fontweight="bold", fontsize=10.5)
c.set_xlabel("number of factor combinations,  K×J")
c.set_ylabel("decode accuracy")
c.set_ylim(-0.04, 1.06)
c.set_xscale("log")
c.legend(fontsize=7.8, loc="center left")
c.grid(alpha=0.25, which="both")
c.text(0.40, 0.18, "held-out == enumerated (gap=0)\n→ systematic, not memorised",
       transform=c.transAxes, fontsize=8.0, color="#c0392b", fontweight="bold")

# ---- H4: hierarchy vs flat -- the decisive ceiling test (strict criterion) ----
d = ax[1, 1]
h4 = r["H4_hierarchy_vs_flat"]["curve"]
T = [x["T_total"] for x in h4]
fs = [x["flat_strict_acc"] for x in h4]
hs = [x["hier_strict_acc"] for x in h4]
fid = [x["flat_id_acc"] for x in h4]
d.plot(T, fs, marker="s", lw=2.6, color="#c0392b", label="FLAT, strict clean-up (≥0.95)")
d.plot(T, hs, marker="o", lw=2.6, color="#1f7a3d", label="HIERARCHICAL, strict clean-up")
d.plot(T, fid, marker=".", lw=1.6, ls="--", color="#888888", label="flat, forgiving argmax-id")
d.axhline(0.9, ls=":", color="grey", lw=1)
ft = r["H4_hierarchy_vs_flat"]["flat_usable_T_strict"]
ht = r["H4_hierarchy_vs_flat"]["hier_usable_T_strict"]
d.axvline(ft, ls="--", color="#c0392b", lw=1.2)
# alpha~0.06 strict capacity wall for the flat field
d.axvline(0.06 * N, ls=":", color="#c0392b", lw=1.0, alpha=0.6)
d.set_title("H4 — HIERARCHY breaks the FLAT ceiling\n"
            f"(strict: flat usable T={ft} → hierarchy holds to T={ht}, ~{ht//max(ft,1)}×)  [V]",
            fontweight="bold", fontsize=10.5)
d.set_xlabel("total instances stored,  T = m·B")
d.set_ylabel("instance recovery accuracy")
d.set_ylim(-0.04, 1.06)
d.legend(fontsize=8.0, loc="center right")
d.grid(alpha=0.25)
d.text(0.30, 0.42, "criterion-dependent:\nforgiving id readout hides\nthe gap (easy 10% cue)",
       transform=d.transAxes, fontsize=8.0, color="#555555", fontweight="bold")

fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("wave_hierarchy_atlas.png", dpi=140, bbox_inches="tight")
print("wrote wave_hierarchy_atlas.png")
