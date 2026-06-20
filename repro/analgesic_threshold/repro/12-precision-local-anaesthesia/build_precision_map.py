#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_precision_map.py  —  M12 (v2): precision (pain-selective) local-anaesthesia map.

Ordinary local anaesthetics are lipophilic, so they enter EVERY axon at the site and block its
Na_V indiscriminately -> loss of pain AND touch AND motor function. The published precision
mechanism makes a firing-threshold raiser FIBRE-SELECTIVE by controlling its ENTRY ROUTE rather
than its target: a permanently-charged Na_V blocker cannot cross the membrane from outside, so it
enters a neuron ONLY through an open large-pore channel; TRPV1/TRPA1 are large-pore gates on
nociceptors and NOT on large touch afferents or motor efferents. Open the nociceptor's port ->
the charged blocker enters ONLY nociceptors -> blocks their Na_V -> pain-selective block.
(Binshtok, Bean & Woolf, Nature 2007; differential nociceptive-vs-motor block, TRPV1-KO-attenuated.)

So precision local anaesthesia = (nociceptor-selective ENTRY PORT) x (firing-threshold RAISER).
This module reads, on the same NCBI/SantaLucia pipeline, the threshold/selectivity STRUCTURE of
the two halves and assembles a precision-block map of entry-port x Na_V-target pairings.

HONESTY (binding, same firewall):
  - the MECHANISM SHAPE (selective entry -> selective block) is [F] structural, anchored to the
    cited differential-block experiments;
  - gamma-|h_sp| reads are [V]; their place in the map is [F];
  - the differential-block magnitude, margin, duration, toxicity, and clinical utility for any
    specific combination are [O] — asserted nowhere. NO molecule is designed, NO formulation,
    concentration, route, or dose is given. Charged-blocker tool compounds (QX-314, chloroprocaine)
    are named ONLY as cited experimental anchors, not as proposed therapeutics.

Run:  python3 build_precision_map.py   -> expected/precision_block_map.json
"""
import os, sys, json

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
INHER  = os.path.normpath(os.path.join(HERE, "..", "_inherited_data"))
NAV    = os.path.normpath(os.path.join(HERE, "..", "02-read-nav-channels"))
sys.path.insert(0, ENGINE)
import vp_neuro_engine as VN

inher = json.load(open(os.path.join(INHER, "full_sensory_gamma.json")))["genes"]
nav   = json.load(open(os.path.join(NAV, "nav_channels_gamma.json")))["genes"]

def G(sym):
    return inher[sym]["gamma"] if sym in inher else nav[sym]["gamma"]

def read(sym):
    g = G(sym)
    return {"gene": sym, "gamma": round(g, 6),
            "spinodal_h_sp": round(VN.spinodal(g), 6), "barrier": round(VN.barrier(g), 6)}

# ENTRY PORTS — nociceptor-restricted large-pore gates (selectivity is the cited Layer-2 fact).
ENTRY_PORTS = {
  "TRPV1": dict(role="primary nociceptor-restricted large-pore entry port",
                selectivity_cited="expressed on C-fibre nociceptors; absent from large touch afferents / motor efferents",
                src="Caterina 1997 Nature 389:816; Binshtok 2007 Nature 449:607"),
  "TRPA1": dict(role="nociceptor-restricted large-pore entry port",
                selectivity_cited="nociceptor-enriched; co-expressed with TRPV1 on C-fibres",
                src="Story 2003 Cell 112:819; Brackley 2017 (TRPA1 as a QX-314 entry route)"),
  # alternative gates for tissues/conditions where TRPV1 is sparse (optional, cited):
  "P2RX3": dict(role="alternative nociceptor-selective entry port (ATP-gated large pore)",
                selectivity_cited="nociceptor-restricted (DRG); ATP-gated",
                src="Cockayne 2000 Nature 407:1011"),
  "ASIC3": dict(role="alternative entry port (proton-gated; acidic tissue)",
                selectivity_cited="DRG/muscle acid sensor; engaged in acidic/inflamed tissue",
                src="Sutherland 2001 PNAS 98:711"),
  "TRPM8": dict(role="alternative entry port (cold-gated)",
                selectivity_cited="cold-sensing subset; for cold-responsive fibres",
                src="Bautista 2007 Nature 448:204"),
}

# BLOCKER TARGETS — the Na_V the entered charged blocker shuts to RAISE the firing threshold.
BLOCKER_TARGETS = {
  "SCN10A": dict(channel="Na_V1.8",
                 selectivity_cited="TTX-resistant, HIGH nociceptor-selectivity (DRG) — cleanest target once delivery is selective",
                 src="Akopian 1996 Nature 379:257"),
  "SCN9A":  dict(channel="Na_V1.7",
                 selectivity_cited="nociceptor-enriched AP-threshold channel",
                 src="Cox 2006 Nature 444:894"),
}

MECH_SHAPE_GRADE = "[F] structural: selective ENTRY (nociceptor-restricted port) -> selective BLOCK (entered Na_V) — anchored to Binshtok 2007"
MAGNITUDE_GRADE  = "[O] OPEN: differential-block margin, duration, toxicity, formulation, concentration, dose, route — asserted nowhere"

def build():
    ports   = {p: {**read(p), **ENTRY_PORTS[p]} for p in ENTRY_PORTS}
    targets = {t: {**read(t), **BLOCKER_TARGETS[t]} for t in BLOCKER_TARGETS}

    # primary pairings: the two co-expressed nociceptor ports x the two nociceptor Na_V targets.
    PRIMARY = [("TRPV1", "SCN10A"), ("TRPV1", "SCN9A"), ("TRPA1", "SCN10A"), ("TRPA1", "SCN9A")]
    ALT     = [("P2RX3", "SCN10A"), ("ASIC3", "SCN10A"), ("TRPM8", "SCN10A")]

    def pairing(port, tgt, tier):
        return {
            "entry_port": port, "entry_port_h_sp": ports[port]["spinodal_h_sp"],
            "entry_port_selectivity_cited": ports[port]["selectivity_cited"],
            "blocker_target": tgt, "blocker_channel": targets[tgt]["channel"],
            "blocker_target_h_sp": targets[tgt]["spinodal_h_sp"],
            "blocker_target_selectivity_cited": targets[tgt]["selectivity_cited"],
            "tier": tier,
            "hypothesis": (f"Open the nociceptor-restricted {port} port so a permanently-charged Na_V blocker "
                           f"enters only nociceptors, then raise the firing threshold by shutting "
                           f"{targets[tgt]['channel']} there — confining the block to the pain fibre."),
            "mechanism_shape_grade": MECH_SHAPE_GRADE,
            "magnitude_grade": MAGNITUDE_GRADE,
        }

    pairings = ([pairing(p, t, "primary") for p, t in PRIMARY]
                + [pairing(p, t, "alternative") for p, t in ALT])

    return {
        "title": "Precision (pain-selective) local-anaesthesia map",
        "mechanism": "precision local anaesthesia = (nociceptor-selective entry port) x (firing-threshold raiser)",
        "anchor_cited": ("Binshtok, Bean & Woolf, Nature 2007 (charged Na_V blocker entering via TRPV1 produces "
                         "differential nociceptive-vs-motor block; TRPV1-KO-attenuated). Charged-blocker tool "
                         "compounds (QX-314, chloroprocaine) are cited experimental anchors, not proposed therapeutics."),
        "firewall": ("READS the threshold/selectivity STRUCTURE of the two halves. The mechanism SHAPE is [F]; "
                     "every clinical magnitude and any formulation/concentration/route/dose is [O], asserted nowhere. "
                     "No molecule is designed."),
        "precision_metric": {
            "name": "differential block ratio",
            "definition": "duration/strength of nociceptive block versus motor block",
            "target_property": "a genuine precision agent MAXIMISES nociceptive block while MINIMISING motor block",
            "grade": "[O] target property stated as a PREDICTION, not a measured result",
        },
        "falsifier": ("If opening the nociceptor-selective port does NOT produce a differential (pain-selective) "
                      "block — i.e. motor/touch are blocked as much as pain — the entry-port-selectivity premise "
                      "is wrong for that port/tissue."),
        "entry_ports": ports, "blocker_targets": targets,
        "n_pairings": len(pairings), "pairings": pairings,
    }

if __name__ == "__main__":
    m = build()
    json.dump(m, open(os.path.join(HERE, "expected", "precision_block_map.json"), "w"), indent=1)
    print("M12 precision local-anaesthesia map (entry-port x Na_V-target pairings):")
    print(f"  {'tier':12} {'entry-port':10} {'|h_sp|':>7}   x   {'Na_V target':12} {'|h_sp|':>7}")
    for p in m["pairings"]:
        print(f"  {p['tier']:12} {p['entry_port']:10} {p['entry_port_h_sp']:7.4f}   x   "
              f"{p['blocker_channel']:12} {p['blocker_target_h_sp']:7.4f}")
    print(f"  precision metric: {m['precision_metric']['name']} ([O] prediction)")
    print(f"  falsifier present: differential-block test")
    print(f"wrote expected/precision_block_map.json  ({m['n_pairings']} pairings)")
