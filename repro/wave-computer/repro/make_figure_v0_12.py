#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.12 atlas from wave_axiom_audit_results.json (POST-PROGRAM COMPRESSION:
the axiom-independence audit). Six panels:
  P1  AX1 data-encoded field : intact vs a magnitude-matched RANDOM field -> recall collapses.
  P2  AX2 symmetry           : sweep the antisymmetric break kappa -> a graded tolerance, then collapse.
  P3  AX3 nonlinearity       : intact vs the first-order LINEAR consensus flow -> recall collapses.
  P4  AX4 settling           : intact vs NO settle (field inert; read = the corrupted cue).
  P5  AX5 metastable band    : sweep a uniform ferromagnetic drive -> forced to R=1, recall collapses.
  P6  verdict                : 8 inherited invariants -> 5 operational axioms, every axiom load-bearing
                               -> IRREDUCIBLE (no further compression); firewall intact.
FUNCTION only. No tuned constants. Ablations on the FROZEN L0; L0 never edited.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_axiom_audit_results.json"))
C1, C2, C3, C4, C5 = (r["C1_AX1_data_field"], r["C2_AX2_symmetry"], r["C3_AX3_nonlinearity"],
                      r["C4_AX4_settling"], r["C5_AX5_band"])
V, H, CTRL = r["C6_verdict"], r["headline"], r["intact_positive_control"]
SEP = 0.5

BLUE, GREEN, PURPLE, RED, ORANGE, GREY = \
    "#1f5fa6", "#1f7a3d", "#6a1b9a", "#c0392b", "#e08214", "#8a8a8a"

fig, ax = plt.subplots(2, 3, figsize=(18.6, 11.6))
fig.suptitle(
    "vp_wave_computer v0.12 — POST-PROGRAM COMPRESSION: the axiom-independence audit\n"
    "the 8 inherited invariants (brain B1-B5, physics P1-P3) compress to 5 operational L0 axioms; "
    "ablate each -> every one collapses a core capability -> the set is IRREDUCIBLE (no further compression)\n"
    "FIREWALL: a functional structural result, the hard-problem blank stays OPEN  —  "
    "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0  ·  ablations on the FROZEN L0, never edited",
    fontsize=10.6, fontweight="bold")

# ---------------------------------------------------------------- P1 AX1 data field
a = ax[0, 0]
x = np.arange(2); w = 0.34
a.bar(x - w/2, [C1["intact_capacity"], C1["ko_capacity"]], w, color=GREEN, label="capacity (frac recalled)")
a.bar(x + w/2, [C1["intact_overlap"], C1["ko_overlap"]], w, color=BLUE, alpha=0.85, label="overlap (recovery)")
a.axhline(SEP, color=GREY, ls=":", lw=1.3, label=f"collapse margin {SEP}")
a.set_title("P1 · AX1 data-encoded coupling field  [V]\n"
            "intact Hebbian vs a magnitude-matched RANDOM field", fontsize=10, fontweight="bold")
a.set_xticks(x); a.set_xticklabels(["intact\n(data encoded)", "knock-out\n(random field)"])
a.set_ylim(0, 1.08); a.set_ylabel("recall"); a.legend(fontsize=8, loc="upper right"); a.grid(alpha=0.25, axis="y")

# ---------------------------------------------------------------- P2 AX2 symmetry (graded)
a = ax[0, 1]
kp = [row["kappa"] for row in C2["by_kappa"]]
cap = [row["capacity"] for row in C2["by_kappa"]]
ov = [row["overlap"] for row in C2["by_kappa"]]
a.plot(kp, cap, "o-", color=GREEN, lw=2.4, ms=7, label="capacity")
a.plot(kp, ov, "s--", color=BLUE, lw=1.8, ms=6, alpha=0.85, label="overlap")
a.axhline(SEP, color=GREY, ls=":", lw=1.3, label=f"collapse margin {SEP}")
a.axvline(C2["asymmetry_tolerance_kappa"], color=ORANGE, ls="-.", lw=1.6, alpha=0.8,
          label=f"tolerance kappa={C2['asymmetry_tolerance_kappa']:g}")
a.set_title("P2 · AX2 field symmetry (reciprocity)  [V]\n"
            "antisymmetric break: a graded tolerance, then collapse", fontsize=10, fontweight="bold")
a.set_xlabel("asymmetry break  kappa  (|antisym part| / ||J||)"); a.set_ylabel("recall")
a.set_ylim(0, 1.08); a.legend(fontsize=8, loc="lower left"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- P3 AX3 nonlinearity
a = ax[0, 2]
x = np.arange(2); w = 0.26
a.bar(x - w, [C3["intact_capacity"], C3["ko_capacity"]], w, color=GREEN, label="capacity")
a.bar(x, [C3["intact_overlap"], C3["ko_overlap"]], w, color=BLUE, alpha=0.85, label="overlap")
a.bar(x + w, [C3["intact_R"], C3["ko_R"]], w, color=ORANGE, alpha=0.85, label="global R (coherence)")
a.axhline(SEP, color=GREY, ls=":", lw=1.3)
a.set_title("P3 · AX3 coupling nonlinearity (sin dtheta)  [V]\n"
            "intact vs first-order LINEAR consensus flow (same J)", fontsize=10, fontweight="bold")
a.set_xticks(x); a.set_xticklabels(["intact\n(nonlinear)", "knock-out\n(linear)"])
a.set_ylim(0, 1.08); a.set_ylabel("value"); a.legend(fontsize=8, loc="upper right"); a.grid(alpha=0.25, axis="y")

# ---------------------------------------------------------------- P4 AX4 settling
a = ax[1, 0]
x = np.arange(3); w = 0.5
vals = [C4["intact_overlap"], C4["ko_overlap"], C4["ko_equals_cue_level"]]
cols = [GREEN, RED, GREY]
a.bar(x, vals, w, color=cols)
for xi, vv in zip(x, vals):
    a.text(xi, vv + 0.02, f"{vv:.2f}", ha="center", fontsize=9, fontweight="bold")
a.axhline(SEP, color=GREY, ls=":", lw=1.3)
a.set_title("P4 · AX4 settling / clock-free relaxation  [V]\n"
            "no relaxation -> the field is INERT (read = the corrupted cue)", fontsize=10, fontweight="bold")
a.set_xticks(x); a.set_xticklabels(["intact\n(settle)", "knock-out\n(no settle)", "corrupted\ncue level"])
a.set_ylim(0, 1.08); a.set_ylabel("overlap (recovery)"); a.grid(alpha=0.25, axis="y")

# ---------------------------------------------------------------- P5 AX5 metastable band
a = ax[1, 1]
dr = [row["drive"] for row in C5["by_drive"]]
cap = [row["capacity"] for row in C5["by_drive"]]
Rv = [row["R"] for row in C5["by_drive"]]
a.plot(dr, cap, "o-", color=GREEN, lw=2.4, ms=7, label="capacity (recall)")
a.axhline(SEP, color=GREY, ls=":", lw=1.3, label=f"collapse margin {SEP}")
a.set_xlabel("uniform ferromagnetic drive  d"); a.set_ylabel("capacity", color=GREEN)
a.set_ylim(0, 1.08); a.tick_params(axis="y", labelcolor=GREEN)
a2 = a.twinx()
a2.plot(dr, Rv, "s--", color=RED, lw=2.0, ms=6, label="global R (coherence)")
a2.set_ylabel("global R  ->  1 = full sync", color=RED); a2.set_ylim(0, 1.08); a2.tick_params(axis="y", labelcolor=RED)
a.set_title("P5 · AX5 metastable operating band  [V]\n"
            "force R->1 (full coherence): one global state, recall collapses", fontsize=10, fontweight="bold")
l1, lab1 = a.get_legend_handles_labels(); l2, lab2 = a2.get_legend_handles_labels()
a.legend(l1 + l2, lab1 + lab2, fontsize=8, loc="center right"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- P6 verdict
a = ax[1, 2]; a.axis("off")
load = V["load_bearing_per_axiom"]
def ok(b): return "PASS" if b else "----"
lines = [
    ("AXIOM-INDEPENDENCE AUDIT  (post-program compression)", "head"),
    ("", "sp"),
    ("inheritance compression (structural):", "sub"),
    ("  8 inherited invariants (B1-B5, P1-P3)", "txt"),
    ("    -> 5 operational L0 axioms", "txt"),
    ("  (B5 theta-gamma capacity = a higher-layer L2/L3", "txt"),
    ("   realization, NOT an L0 axiom -> deferred)", "txt"),
    ("", "sp"),
    ("each axiom ABLATED on the frozen L0 -> load-bearing?", "sub"),
    (f"  [{ok(load['AX1_data_encoded_field'])}]  AX1  data-encoded coupling field", "res"),
    (f"  [{ok(load['AX2_field_symmetry'])}]  AX2  field symmetry (reciprocity)", "res"),
    (f"  [{ok(load['AX3_coupling_nonlinearity'])}]  AX3  coupling nonlinearity (sin)", "res"),
    (f"  [{ok(load['AX4_settling_clockfree'])}]  AX4  settling / clock-free relax", "res"),
    (f"  [{ok(load['AX5_metastable_band'])}]  AX5  metastable operating band", "res"),
    ("", "sp"),
    (f"  intact positive control passes:  {ok(CTRL['passes'])}", "res"),
    (f"  redundant axioms found:  {V['redundant_axioms'] if V['redundant_axioms'] else 'none'}", "txt"),
    ("", "sp"),
    (f"  VERDICT:  axiom set IRREDUCIBLE = {V['axiom_set_irreducible']}", "verdict"),
    ("  every axiom is independent -> the 5-axiom core", "verdict"),
    ("  is MINIMAL; no further compression.  [V]", "verdict"),
    ("", "sp"),
    ("FIREWALL  consciousness_claim=0  hard_problem_open=1", "fire"),
    ("NO-TUNING  new_tuned_constants=0", "fire"),
]
y = 1.0
for text, kind in lines:
    if kind == "sp":
        y -= 0.016; continue
    if kind == "head":
        a.text(0.0, y, text, fontsize=11.6, fontweight="bold", color=PURPLE, transform=a.transAxes)
    elif kind == "sub":
        a.text(0.0, y, text, fontsize=9.8, fontweight="bold", color=BLUE, transform=a.transAxes)
    elif kind == "res":
        a.text(0.0, y, text, fontsize=9.5, fontweight="bold", color=GREEN, family="monospace", transform=a.transAxes)
    elif kind == "verdict":
        a.text(0.0, y, text, fontsize=10.0, fontweight="bold", color=GREEN, transform=a.transAxes)
    elif kind == "fire":
        a.text(0.0, y, text, fontsize=9.2, fontweight="bold", color=RED, family="monospace", transform=a.transAxes)
    else:
        a.text(0.0, y, text, fontsize=9.0, color="#222222", transform=a.transAxes)
    y -= 0.040

fig.tight_layout(rect=[0, 0, 1, 0.945])
fig.savefig("wave_axiom_audit_atlas.png", dpi=130, bbox_inches="tight")
print("wrote wave_axiom_audit_atlas.png")
