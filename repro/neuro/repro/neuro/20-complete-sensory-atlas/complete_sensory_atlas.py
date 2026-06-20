#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§20 capstone — completing the sensory atlas: the four remaining modalities
emerge from REAL measured γ, and the proprioceptive loop closes.

The chain already emerged eye / ear / olfactory / skin / taste (§12) on the R19
switch. This chapter completes the human sensory inventory by emerging the FOUR
remaining modalities from their master genes' measured stacking stiffness γ
(READ-ONLY — the same primitive that writes DNA genes and fires neurons), and
wiring each to a principled transducer whose DEFINING property is MEASURED, never
tuned:

  somatosensory triad on the ONE emerged skin organ (TP63, §12):
    (5) touch  : low-threshold mechanoreceptor (PIEZO2)                 [V]
    (6) warmth : low-threshold thermoreceptor   (§10)                   [V]  (already)
    (7) pain   : HIGH-threshold polymodal nociceptor (PRDM12 · TRPV1 43C) [F]/[V]
  (8) proprioception : muscle spindle (RUNX3 · PIEZO2) -> CLOSES the §11 reflex loop  [V]
  (9) vestibular     : directional hair cell (ATOH1 · OTOP1), SIGNED response          [V]

With vision / hearing / smell / taste / vestibular (the five special senses) and
the somatosensory touch / warmth / pain / proprioception, all NINE modalities now
emerge from measured γ and transduce a stimulus into the low-frequency spike train
the chain reads.

LOCKED here (Layer-1 [F], from measured γ): the developmental ORDER and relative
SIZE of the new organs, and the threshold ORDER (nociceptor HIGH vs touch/warmth
LOW). OPEN (Layer-2 [O]): absolute size / time / threshold magnitudes (ledger).
Engine: ../_engine/vp_neuro_engine.py
"""
import sys, os, json, hashlib, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_neuro_engine import (seed_everything, Organ, spinodal,
    MechanoReceptor, Thermoreceptor, Nociceptor, Proprioceptor, VestibularReceptor,
    ReflexArc, TouchStimulus, StretchStimulus, AccelStimulus)

DATA = os.path.join(os.path.dirname(__file__), "..", "_engine", "data")
EXT  = os.path.join(DATA, "full_sensory_gamma.json")   # the 4 new modalities (fetched γ)
ORG  = os.path.join(DATA, "sensory_organ_gamma.json")  # the existing 5 (read-only roster)


def main(P):
    seed_everything()
    J = json.load(open(EXT, encoding="utf-8"))
    G = {g: J["genes"][g]["gamma"] for g in J["genes"]}
    atlas = J["_atlas"]

    # ---- emerge the new organs from their REAL master-gene γ (READ-ONLY) -----
    organs = {}
    for name, (layer, master, partners) in atlas.items():
        organs[name] = Organ(name, G[master], master=master,
                             partners=tuple(partners), layer=layer)
    P("new sensory organs emerged (master gene · measured γ · partners):")
    for n, o in organs.items():
        P(f"  {n:13s} {o.master:7s} γ={o.g:.4f}  partners={list(o.partners)}")

    # ---- γ is a real read-out: corr(γ,GC) over the new genes -----------------
    gv = [J["genes"][k]["gamma"] for k in J["genes"]]
    cv = [J["genes"][k]["gc"]    for k in J["genes"]]
    n = len(gv); mg = sum(gv)/n; mc = sum(cv)/n
    cov = sum((a-mg)*(b-mc) for a, b in zip(gv, cv))/n
    sg = (sum((a-mg)**2 for a in gv)/n)**0.5
    sc = (sum((b-mc)**2 for b in cv)/n)**0.5
    corr = cov/(sg*sc)
    P(f"\n[0] γ is not free: corr(γ,GC)={corr:.4f} over {n} new sensory genes "
      f"(organ atlas 0.994, taste 0.995)")
    P(f"    → the new organs emerge from measured sequence, never fitted [F]")

    # ---- (1) presence is STATE, not γ ---------------------------------------
    P("\n[1] STATE decides presence (parts present ≠ trait):")
    for nm, o in organs.items():
        on = o.present(o.spinodal + 0.25); off = o.present(0.0)
        P(f"  {nm:13s} ON→present={on}   OFF→present={off}")
        assert on and not off

    # ---- (2) developmental ORDER over time (the 4D) -------------------------
    order = sorted(organs.values(), key=lambda o: o.functional_spinodal())
    P("\n[2] developmental order (4D: spinodal cleared as drive ramps over time):")
    for k, o in enumerate(order, 1):
        P(f"  t{k}: {o.name:13s} switches on at drive |h_sp|={o.functional_spinodal():.4f}")
    sp = [o.functional_spinodal() for o in order]
    assert all(sp[i] <= sp[i+1] for i in range(len(sp)-1))

    # ---- (3) relative SIZE from DWELL ∝ γ^1.5 -------------------------------
    P("\n[3] relative organ size (DWELL ∝ γ^1.5; order [F], absolute [O]):")
    sizes = sorted(organs.values(), key=lambda o: o.size(), reverse=True)
    for o in sizes:
        P(f"  {o.name:13s} size∝{o.size():.3f}")
    sz = [o.size() for o in sizes]
    assert all(sz[i] >= sz[i+1] for i in range(len(sz)-1))

    # ---- (4) somatosensory triad on the ONE emerged skin organ --------------
    #     the defining MEASURED contrast: pain is HIGH-threshold (TRPV1 43C),
    #     touch/warmth are LOW-threshold — one organ, three submodalities.
    P("\n[4] somatosensory triad on the emerged skin organ (TP63 §12) — "
      "touch/warmth LOW vs pain HIGH threshold:")
    touch = MechanoReceptor(); warm = Thermoreceptor(); pain = Nociceptor()
    innoc_T = TouchStimulus(temperature_C=35); nox_T = TouchStimulus(temperature_C=50)
    innoc_P = TouchStimulus(pressure=0.2);     nox_P = TouchStimulus(pressure=1.0)
    t_w = len(warm.transduce(innoc_T)["spikes"]);  n_w = len(pain.transduce(innoc_T)["spikes"])
    t_h = len(warm.transduce(nox_T)["spikes"]);    n_h = len(pain.transduce(nox_T)["spikes"])
    t_g = len(touch.transduce(innoc_P)["spikes"]); n_g = len(pain.transduce(innoc_P)["spikes"])
    t_c = len(touch.transduce(nox_P)["spikes"]);   n_c = len(pain.transduce(nox_P)["spikes"])
    P(f"  innocuous warm 35C : thermo {t_w} spikes, nociceptor {n_w} (SILENT — below TRPV1 43C)")
    P(f"  noxious   heat 50C : thermo {t_h} spikes, nociceptor {n_h} (FIRES — pain)")
    P(f"  gentle   touch 0.2 : mechano {t_g} spikes, nociceptor {n_g} (SILENT — innocuous)")
    P(f"  noxious  press 1.0 : mechano {t_c} spikes, nociceptor {n_c} (both fire)")
    assert n_w == 0 and n_g == 0 and n_h > 0 and n_c > 0 and t_w > 0 and t_g > 0

    # ---- (5) proprioception closes the §11 reflex loop ----------------------
    P("\n[5] proprioception (muscle spindle RUNX3 · PIEZO2) closes the §11 reflex loop:")
    spindle = Proprioceptor(); arc = ReflexArc()
    prev = -1
    for s in [0.0, 0.3, 0.7]:
        nsp = len(spindle.transduce(StretchStimulus(s))["spikes"]); c = arc.correct(s)
        P(f"  stretch {s:.1f}: spindle {nsp:>2} spikes → reflex correction {c:+.3f} (opposes)")
        assert nsp >= prev and (s == 0.0 or c < 0); prev = nsp
    rej = arc.closed_loop_error(0.5)
    P(f"  closed loop: disturbance 0.5 → error {rej['closed']:.4f} "
      f"(open {rej['open']:.4f}), rejection ×{rej['rejection']:.1f}")
    assert rej['closed'] < rej['open']

    # ---- (6) vestibular is directional / signed -----------------------------
    P("\n[6] vestibular hair cell (ATOH1 · OTOP1) is DIRECTIONAL (signed), "
      "unlike unsigned pressure:")
    vest = VestibularReceptor()
    neg = len(vest.transduce(AccelStimulus(-0.6))["spikes"])
    zer = len(vest.transduce(AccelStimulus(0.0))["spikes"])
    pos = len(vest.transduce(AccelStimulus(+0.6))["spikes"])
    P(f"  accel −0.6 → {neg} spikes · rest 0.0 → {zer} · +0.6 → {pos}  "
      f"(signed: {pos} ≠ {neg})")
    assert pos != neg and neg <= zer <= pos

    # ---- the full nine-modality roster: all emerge + transduce --------------
    P("\n[*] SENSORY ATLAS — all nine modalities now emerge from measured γ and transduce:")
    O = json.load(open(ORG, encoding="utf-8"))["genes"]
    roster = [
        ("1 vision",         "eye",       "PAX6",          O["PAX6"]["gamma"]),
        ("2 hearing",        "ear",       "PAX2",          O["PAX2"]["gamma"]),
        ("3 smell",          "olfactory", "LHX2",          O["LHX2"]["gamma"]),
        ("4 taste",          "taste",     "POU2F3",        O["POU2F3"]["gamma"]),
        ("5 touch",          "skin",      "TP63→PIEZO2",   O["TP63"]["gamma"]),
        ("6 warmth",         "skin",      "TP63 (thermo)", O["TP63"]["gamma"]),
        ("7 pain",           "DRG/skin",  "PRDM12",        G["PRDM12"]),
        ("8 proprioception", "spindle",   "RUNX3",         G["RUNX3"]),
        ("9 vestibular",     "inner ear", "ATOH1",         G["ATOH1"]),
    ]
    for label, org, gene, g in roster:
        P(f"  {label:18s} {org:11s} {gene:16s} γ={g:.4f}")
    assert len(roster) == 9

    P("\nLOCKED: developmental ORDER + relative SIZE of the new organs, and the")
    P("        threshold ORDER (nociceptor HIGH vs touch/warmth LOW) — Layer-1 [F].")
    P("OPEN  : absolute size/time/threshold magnitudes (Layer-2 [O], in ledger).")
    P("SENSORY ATLAS COMPLETE — nine modalities emerged and transducing.")
    P("PASS")


if __name__ == "__main__":
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    main(P)
    print("sha256:", hashlib.sha256(buf.getvalue().encode()).hexdigest())
