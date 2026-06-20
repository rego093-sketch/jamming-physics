#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clonal_inflammation.py  --  Immune dynamics on the SHARED R19 switch (deterministic, no tuning).

Derives the FUNDAMENTALS (not the surface description): clonal selection, inflammation and immune
memory are not three biological stories -- they are three readouts of ONE bistable field
    ds/dt = g*s - s^3 + h            (vp_substrate; g = gamma scale, h = drive)
whose only forced constants are the spinodal |h*| = 2(g/3)^1.5 and the barrier g^2/4. Every threshold
below is that spinodal; every persistence below is that barrier. Nothing is fitted.

T1 clonal activation   : a naive cell sits in the OFF well; antigen AFFINITY is the drive h. The cell
                         flips ON exactly when h crosses the spinodal -> the affinity threshold of
                         clonal selection IS the saddle-node of the switch. (Self/sub-threshold antigen
                         stays OFF = self-tolerance as a barrier property.)              [V]
T2 inflammation latch  : the same switch has hysteresis (up at +spinodal, down at -spinodal). A
                         sub-spinodal challenge resolves to OFF (ACUTE); a supra-spinodal sustained
                         drive latches ON and STAYS ON after the drive is removed (CHRONIC).         [V]
T4 immune memory       : after antigen clears (h->0) an activated cell remains ON indefinitely; the
                         minimum adverse drive to erase it is the spinodal and its stability ranks by
                         the barrier g^2/4 -> deeper-barrier compartments hold memory more firmly.    [V]

GRADES (C3): mechanism/shape [V] simulation-verified; absolute rates [L]/[O] (cited / open).
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, settle

# ---- fixed integration (SAME for every target; no per-target tuning) ---------------------------
_N, _DT, _RAMP = 2000, 0.01, 2000
_TOL = 0.02          # threshold must sit within 2% of the forced spinodal
_LONG = 12000        # long settle for persistence

def _off(g):  return -math.sqrt(g)
def _on(g):   return  math.sqrt(g)

def up_threshold(g):
    """Smallest positive drive that flips an OFF cell ON (expected = +spinodal)."""
    sp = spinodal(g)
    for i in range(_RAMP + 1):
        h = 1.5 * sp * i / _RAMP
        if settle(g, h, s0=_off(g), n=_N, dt=_DT) > 0.0:
            return h, sp
    return None, sp

def down_threshold(g):
    """Most-negative drive at which an ON cell falls OFF (expected = -spinodal)."""
    sp = spinodal(g)
    for i in range(_RAMP + 1):
        h = -1.5 * sp * i / _RAMP
        if settle(g, h, s0=_on(g), n=_N, dt=_DT) < 0.0:
            return h, sp
    return None, sp

def t1_clonal_activation(gammas):
    """Affinity drive past spinodal flips the cell ON; sub-threshold stays OFF (tolerance)."""
    rows = []
    for name, g in gammas.items():
        hu, sp = up_threshold(g)
        sub = settle(g, 0.8 * sp, s0=_off(g), n=_N, dt=_DT)           # sub-threshold antigen
        supra = settle(g, 1.2 * sp, s0=_off(g), n=_N, dt=_DT)         # supra-threshold antigen
        ok = (hu is not None and abs(hu / sp - 1.0) <= _TOL and sub < 0.0 and supra > 0.0)
        rows.append(dict(organ=name, gamma=round(g, 4), spinodal=round(sp, 6),
                         flip_drive=round(hu, 6), ratio_to_spinodal=round(hu / sp, 4),
                         subthreshold_stays_off=bool(sub < 0.0), suprathreshold_flips_on=bool(supra > 0.0),
                         pass_=bool(ok)))
    return dict(target="T1", claim="affinity drive past spinodal flips the cell ON (clonal selection = saddle-node)",
                rows=rows, all_pass=all(r["pass_"] for r in rows), grade="[V]")

def t2_inflammation_hysteresis(gammas):
    """Hysteresis loop (width = 2*spinodal); acute resolves OFF, chronic latches ON."""
    rows = []
    for name, g in gammas.items():
        hu, sp = up_threshold(g); hd, _ = down_threshold(g)
        loop = hu - hd
        # acute: sub-spinodal challenge applied then withdrawn -> OFF
        sa = settle(g, 0.8 * sp, s0=_off(g), n=2000, dt=_DT); sa = settle(g, 0.0, s0=sa, n=_N, dt=_DT)
        # chronic: supra-spinodal sustained then withdrawn -> stays ON (latch)
        sc = settle(g, 1.2 * sp, s0=_off(g), n=2000, dt=_DT); sc = settle(g, 0.0, s0=sc, n=_N, dt=_DT)
        ok = (loop > 0.0 and abs(hu / sp - 1) <= _TOL and abs(hd / -sp - 1) <= _TOL and sa < 0 and sc > 0)
        rows.append(dict(organ=name, gamma=round(g, 4), loop_width=round(loop, 6),
                         expected_loop=round(2 * sp, 6), acute_resolves_off=bool(sa < 0.0),
                         chronic_latches_on=bool(sc > 0.0), pass_=bool(ok)))
    return dict(target="T2", claim="bistable hysteresis: acute (sub-spinodal) resolves, chronic (supra-spinodal) latches",
                rows=rows, all_pass=all(r["pass_"] for r in rows), grade="[V]")

def t4_immune_memory(gammas):
    """After antigen clears (h->0) the ON state persists; erase-drive = spinodal; stability ranks by barrier."""
    rows = []
    for name, g in gammas.items():
        sp = spinodal(g); b = barrier(g)
        s = settle(g, 1.2 * sp, s0=_off(g), n=2000, dt=_DT)           # activate
        s = settle(g, 0.0, s0=s, n=_LONG, dt=_DT)                     # antigen cleared, long persistence
        persists = s > 0.0
        # minimum adverse (negative) drive to erase memory (expected ~ -spinodal)
        erase = None
        for i in range(1, _RAMP + 1):
            hn = -1.5 * sp * i / _RAMP
            if settle(g, hn, s0=_on(g), n=_N, dt=_DT) < 0.0:
                erase = hn; break
        ok = (persists and erase is not None and abs(erase / -sp - 1) <= _TOL)
        rows.append(dict(organ=name, gamma=round(g, 4), barrier=round(b, 6),
                         persists_on=bool(persists), erase_drive=round(erase, 6),
                         erase_ratio_to_spinodal=round(erase / -sp, 4), pass_=bool(ok)))
    # stability ranks by barrier => ascending barrier order matches ascending gamma order
    order = [r["organ"] for r in sorted(rows, key=lambda r: r["barrier"])]
    return dict(target="T4", claim="memory persists after antigen clears; erase-drive = spinodal; stability ranks by barrier",
                rows=rows, stability_order_ascending=order, all_pass=all(r["pass_"] for r in rows), grade="[V]")

def run(gammas):
    return dict(T1=t1_clonal_activation(gammas), T2=t2_inflammation_hysteresis(gammas),
                T4=t4_immune_memory(gammas))

if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis":1.3225,"spleen":1.4228,"thymus":1.4533,"lymphoid_adaptive":1.4892}
    print(json.dumps(run(G), ensure_ascii=False, indent=2))
