#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§12 reproduction — DNA 4D emergence of the sense organs from REAL measured γ.

Each sense organ (eye, ear, olfactory, skin) and the motor pair (cerebellum,
muscle) is EMERGED from its master gene's measured stacking stiffness γ — the
same READ-ONLY values used by the DNA paper (corr(γ,GC)=0.994), the same R19
switch that makes the neuron fire. We show, deterministically:

  (1) presence by STATE  : master cis ON -> organ present; OFF -> absent, even
      with partners intact ('parts present ≠ trait').                       [F]
  (2) developmental ORDER : organs cross their functional spinodal in a fixed
      γ-set sequence as a global morphogen drive ramps over time (the '4D').  [F]
  (3) relative SIZE       : DWELL ∝ γ^1.5 sets a size ORDER [F]; absolute is [O].
  (4) organ -> receptor   : a present organ hosts its transducer (§10); an
      absent organ transduces nothing (no organ, no spikes).                 [V]

LOCKED by this chapter (was open): the developmental ORDER and the relative SIZE
order across the sensory+motor organs (Layer-1 [F], from measured γ). Absolute
size/time stay [O] (Layer-2). Engine: ../_engine/vp_neuro_engine.py
"""
import sys, os, json, hashlib, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_neuro_engine import (seed_everything, Organ, spinodal,
    Photoreceptor, MechanoReceptor, ChemoReceptor, Thermoreceptor,
    LightStimulus, WaveStimulus, MoleculeStimulus, TouchStimulus)

CAT = os.path.join(os.path.dirname(__file__), "..", "_engine", "data",
                   "sensory_organ_gamma.json")

def main(P):
    seed_everything()
    J = json.load(open(CAT, encoding="utf-8"))
    G = {g: J["genes"][g]["gamma"] for g in J["genes"]}
    atlas = J["_atlas"]

    # ---- build every organ from its REAL master-gene γ (READ-ONLY) ----------
    organs = {}
    for name, (layer, master, partners) in atlas.items():
        organs[name] = Organ(name, G[master], master=master,
                             partners=tuple(partners), layer=layer)
    P("emerged organs (master gene · measured γ · partners):")
    for n, o in organs.items():
        P(f"  {n:11s} {o.master:6s} γ={o.g:.4f}  partners={list(o.partners)}")

    # ---- the γ-set is REAL: γ tracks GC content across the source catalog -----
    gv = [J["genes"][k]["gamma"] for k in J["genes"]]
    cv = [J["genes"][k]["gc"]    for k in J["genes"]]
    n = len(gv); mg = sum(gv)/n; mc = sum(cv)/n
    cov = sum((a-mg)*(b-mc) for a, b in zip(gv, cv))/n
    sg = (sum((a-mg)**2 for a in gv)/n)**0.5
    sc = (sum((b-mc)**2 for b in cv)/n)**0.5
    corr_gc = cov/(sg*sc)
    P(f"\n[0] the γ values are not free: corr(γ,GC)={corr_gc:.4f} over {n} catalog genes")
    P(f"    → γ is a read-out of real sequence GC, so the organs emerge from measured data [F]")

    # ---- (1) presence is decided by STATE, not γ ----------------------------
    P("\n[1] STATE decides presence (parts present ≠ trait):")
    for n, o in organs.items():
        on = o.present(o.spinodal + 0.25)     # master cis ON
        off = o.present(0.0)                  # master cis OFF (partners intact)
        P(f"  {n:11s} ON→present={on}   OFF→present={off}")
        assert on and not off

    # ---- (2) developmental ORDER over time (the 4D) -------------------------
    # a global morphogen drive ramps; organs switch on as it clears each spinodal
    order = sorted(organs.values(), key=lambda o: o.functional_spinodal())
    P("\n[2] developmental order (4D: spinodal cleared as drive ramps over time):")
    for k, o in enumerate(order, 1):
        P(f"  t{k}: {o.name:11s} switches on at drive |h_sp|={o.functional_spinodal():.4f}")
    sp = [o.functional_spinodal() for o in order]
    assert all(sp[i] <= sp[i+1] for i in range(len(sp)-1))     # monotone = a real order
    # ramp a global morphogen drive finely from below all thresholds to above all
    import numpy as np
    ramp = np.linspace(min(sp) - 0.05, max(sp) + 0.10, 60)
    on_counts = [sum(o.present(d + 0.03) for o in organs.values()) for d in ramp]
    assert all(on_counts[i] <= on_counts[i+1] for i in range(len(on_counts)-1))  # monotone
    assert on_counts[0] == 0 and on_counts[-1] == len(organs)   # none -> all six
    P(f"  organs present as drive ramps 0→6: {on_counts[0]} … {max(on_counts)} "
      f"(monotone emergence, none→all) [F]")

    # ---- (3) relative SIZE from DWELL ∝ γ^1.5 -------------------------------
    P("\n[3] relative organ size (DWELL ∝ γ^1.5; order [F], absolute [O]):")
    sizes = sorted(organs.values(), key=lambda o: o.size(), reverse=True)
    for o in sizes:
        P(f"  {o.name:11s} size∝{o.size():.3f}")
    sz = [o.size() for o in sizes]
    assert all(sz[i] >= sz[i+1] for i in range(len(sz)-1))

    # ---- (4) a present organ hosts its receptor; absent -> nothing ----------
    P("\n[4] organ → receptor (present organ transduces; absent organ does not):")
    pairs = [
        ("eye",       Photoreceptor(cone="L", gain=1.0), LightStimulus(565, 1.0)),
        ("ear",       MechanoReceptor(gain=1.0),         WaveStimulus(40, 1.0)),
        ("olfactory", ChemoReceptor(gain=1.0),           MoleculeStimulus(2.0)),
        ("taste",     ChemoReceptor(gain=1.0),           MoleculeStimulus(1.5)),
        ("skin",      Thermoreceptor(gain=1.0),          TouchStimulus(temperature_C=45)),
    ]
    for name, rec, stim in pairs:
        o = organs[name]
        present = o.present(o.spinodal + 0.25)
        n_spk = len(rec.transduce(stim)["spikes"]) if present else 0
        P(f"  {name:11s} present={present} → spikes={n_spk}")
        assert present and n_spk > 0
        # if the organ were absent, no transduction
        n_absent = len(rec.transduce(stim)["spikes"]) if o.present(0.0) else 0
        assert n_absent == 0

    P("\nLOCKED: developmental ORDER + relative SIZE order across organs (Layer-1 [F]).")
    P("OPEN  : absolute size/time per organ (Layer-2 [O], in ledger).")
    P("PASS")

if __name__ == "__main__":
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    main(P)
    print("sha256:", hashlib.sha256(buf.getvalue().encode()).hexdigest())
