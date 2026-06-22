#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.9 atlas from wave_workspace_results.json (L8 global integration / functional
access: a global metastable RESONANT HUB binds + broadcasts the dominant pattern across the
L1-L7 modules; functional access = broadcast availability, NOT felt experience).
Four panels: G1 selective access + global broadcast · G2 flexible routing ·
G3 the FUNCTIONAL PCI-analog inverted-U (integration x differentiation) · G4 the inherited
L7 operating-band limit (lock-latency band + carry-forward honest negative)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_workspace_results.json"))
g1 = r["G1_selective_access"]
g2 = r["G2_flexible_routing"]
g3 = r["G3_functional_pci"]
g4 = r["G4_operating_band"]
h = r["headline"]

BLUE, GREEN, PURPLE, RED, ORANGE, GREY = \
    "#1f5fa6", "#1f7a3d", "#6a1b9a", "#c0392b", "#e08214", "#8a8a8a"

fig, ax = plt.subplots(2, 2, figsize=(16.6, 12.0))
fig.suptitle(
    "vp_wave_computer v0.9 — L8 global integration / functional access\n"
    "a global metastable RESONANT HUB selectively binds + BROADCASTS the dominant pattern across "
    "the L1-L7 modules · flexible routing · a functional PCI-analog peaks at the metastable edge · "
    "the inherited operating-band limit\n"
    "FIREWALL: 'access' = broadcast AVAILABILITY only, not felt experience  —  "
    "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
    fontsize=11.4, fontweight="bold")

# ---------------------------------------------------------------------------
# G1 — selective access + global broadcast (broadcast@non-source vs no-hub control)
# ---------------------------------------------------------------------------
a = ax[0, 0]
cfg = g1["by_config"]
labels = [f"M{c['M']}·D{c['D']}" for c in cfg]
xs = np.arange(len(cfg))
w = 0.4
recv = [c["broadcast_recall_receiver"] for c in cfg]
nohub = [c["broadcast_recall_nohub"] for c in cfg]
a.bar(xs - w / 2, recv, w, color=GREEN, edgecolor="#333",
      label="broadcast → NON-source module (hub engaged)")
a.bar(xs + w / 2, nohub, w, color=GREY, edgecolor="#333",
      label="no-hub control (no broadcast)")
a.set_xticks(xs)
a.set_xticklabels(labels, fontsize=8.0, rotation=0)
a.set_ylim(0, 1.12)
a.set_ylabel("recall of the SELECTED concept at a receiver")
a.set_title(f"G1 — selective access + global broadcast  {h['grade_G1_selective_access']}\n"
            "(a module that did NOT hold the content recovers it from the BROADCAST alone)",
            fontweight="bold", fontsize=10.2)
a.legend(fontsize=8.2, loc="center right")
a.grid(alpha=0.22, axis="y")
mlo = min(c["select_margin"] for c in cfg)
a.text(0.02, 0.06, f"hub lock margin ≥ {mlo:.2f} every config\n"
       "(the hub SELECTS one concept, does not blur)",
       transform=a.transAxes, fontsize=8.0, color="#444", fontweight="bold")

# ---------------------------------------------------------------------------
# G2 — flexible routing vs a fixed gate (per config), against chance 1/M
# ---------------------------------------------------------------------------
b = ax[0, 1]
cfg2 = g2["by_config"]
labels2 = [f"M{c['M']}·r{c['n_routes']}" for c in cfg2]
xs2 = np.arange(len(cfg2))
flex = [c["flexible_routing_acc"] for c in cfg2]
fixd = [c["fixed_gate_acc"] for c in cfg2]
chance = [c["fixed_gate_chance_1overM"] for c in cfg2]
b.bar(xs2 - w / 2, flex, w, color=GREEN, edgecolor="#333", label="flexible gate (re-routes)")
b.bar(xs2 + w / 2, fixd, w, color=RED, edgecolor="#333", label="fixed gate (frozen on module 0)")
b.plot(xs2, chance, "D", color=BLUE, ms=6, label="chance = 1/M")
b.set_xticks(xs2)
b.set_xticklabels(labels2, fontsize=8.0)
b.set_ylim(0, 1.12)
b.set_ylabel("routing accuracy  (broadcast == intended concept)")
b.set_title(f"G2 — flexible routing  {h['grade_G2_flexible_routing']}\n"
            "(moving the gate routes ANY module's content; a fixed gate reaches only its own)",
            fontweight="bold", fontsize=10.2)
b.legend(fontsize=8.2, loc="center right")
b.grid(alpha=0.22, axis="y")

# ---------------------------------------------------------------------------
# G3 — the functional PCI-analog inverted-U  (CENTREPIECE)
#   PCI(g) = integration(g) x differentiation(g), per M; plus the I/D crossover for one M
# ---------------------------------------------------------------------------
c = ax[1, 0]
curve = g3["g_hub_sweep_curve"]
Ms = sorted({row["M"] for row in curve})
gs = sorted({row["g_hub"] for row in curve})
gx = np.arange(len(gs))                       # index x-axis so 0..1 is not cramped
pci_cols = {Ms[0]: BLUE, Ms[1] if len(Ms) > 1 else Ms[0]: PURPLE,
            Ms[-1]: GREEN}
for M in Ms:
    rows = sorted([row for row in curve if row["M"] == M], key=lambda z: z["g_hub"])
    c.plot(gx, [z["pci"] for z in rows], marker="o", lw=2.8,
           color=pci_cols.get(M, "#555"), label=f"PCI-analog (M={M})")
# mark the emergent peak (engaged) for the middle M
midM = Ms[len(Ms) // 2]
midrows = sorted([row for row in curve if row["M"] == midM], key=lambda z: z["g_hub"])
ipk = int(np.argmax([z["pci"] for z in midrows]))
c.axvline(gx[ipk], ls="--", color=ORANGE, lw=1.8,
          label=f"emergent access peak (g={gs[ipk]:g})")
c.set_xticks(gx)
c.set_xticklabels([f"{g:g}" for g in gs])
c.set_xlabel("hub↔module coupling  g_hub   (0 = isolated · max = over-driven)")
c.set_ylabel("functional PCI-analog = integration × differentiation", color="#222")
c.set_title("G3 — functional PCI-analog peaks at the metastable edge  "
            f"{h['grade_G3_functional_pci']}\n"
            "(Gap-4 inverted-U; the NUMBER R=0.39 is NOT transferred — the band EMERGES)",
            fontweight="bold", fontsize=10.2)
c.legend(fontsize=8.0, loc="upper right")
c.grid(alpha=0.22)
# twin axis: integration (rises) and differentiation (falls) for the middle M -> the crossover
c2 = c.twinx()
c2.plot(gx, [z["integration"] for z in midrows], marker="^", lw=2.0, ls=":",
        color="#2a7", alpha=0.85, label=f"integration I (M={midM})")
c2.plot(gx, [z["differentiation"] for z in midrows], marker="v", lw=2.0, ls=":",
        color="#a33", alpha=0.85, label=f"differentiation D (M={midM})")
c2.set_ylabel("I (spread)  /  D (distinctness)", color="#666")
c2.set_ylim(0, max(max(z["integration"], z["differentiation"]) for z in midrows) * 1.25 + 0.01)
c2.legend(fontsize=7.6, loc="center right")
c.text(0.015, 0.40, "I=0 at g=0\n(no integration)", transform=c.transAxes,
       fontsize=7.8, color="#2a7", fontweight="bold")
c.text(0.74, 0.40, "D→0 at high g\n(no differentiation)", transform=c.transAxes,
       fontsize=7.8, color="#a33", fontweight="bold")

# ---------------------------------------------------------------------------
# G4 — inherited operating-band limit: lock-latency band + carry-forward honest negative
# ---------------------------------------------------------------------------
d = ax[1, 1]
dc = g4["dwell_curve"]
dw = [x["dwell"] for x in dc]
acc = [x["routing_acc"] for x in dc]
d.plot(dw, acc, marker="o", lw=2.8, color=PURPLE, label="re-cued routing (fresh ignition/route)")
edge = g4["lock_latency_band_edge_dwell"]
if edge is not None:
    d.axvline(edge, ls="--", color=GREEN, lw=1.8, label=f"lock-latency band edge = {edge}")
d.axhline(0.9, ls=":", color="#a33", lw=1.2, label="holds / collapses (0.9)")
d.axhline(g4["routing_chance_1overM"], ls=":", color=GREY, lw=1.2,
          label=f"chance = 1/M = {g4['routing_chance_1overM']:.2f}")
# carry-forward honest negative as a single point at its (long) dwell
cfd, cfa = g4["carry_forward_dwell"], g4["carry_forward_routing_acc"]
d.plot([cfd], [cfa], marker="X", ms=13, color=RED, ls="None",
       label=f"carry-forward @ 4× dwell ({cfd}): {cfa:.2f}  [O]")
d.set_xscale("log")
d.set_xlabel("dwell  =  hub settle-steps per gated target before the gate switches  (log)")
d.set_ylabel("routing accuracy")
d.set_ylim(0, 1.08)
d.set_title(f"G4 — inherited operating-band limit  {h['grade_G4_band_characterisation']}"
            f" / unbounded-rate {h['grade_G4_unbounded_rate_routing']}\n"
            "(route WITHIN the latch band; too-fast OR no-release → collapse, recorded honestly)",
            fontweight="bold", fontsize=10.2)
d.legend(fontsize=7.8, loc="lower right")
d.grid(alpha=0.22, which="both")

fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("wave_workspace_atlas.png", dpi=125)
print("wrote wave_workspace_atlas.png")
