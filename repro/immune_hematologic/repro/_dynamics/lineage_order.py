#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lineage_order.py  --  T3: hematopoietic / lymphoid developmental order is a gamma readout.

FUNDAMENTAL claim (not a label): the order in which these compartments switch ON in development is set
by the functional spinodal |h*| = 2(g/3)^1.5 -- LOWER gamma = lower threshold = earlier emergence. With
all four master-gene gammas now MEASURED, the ascending-gamma order is a falsifiable prediction:

    bone_marrow_hematopoiesis (RUNX1, g=1.3225)  ->  spleen (TLX1, 1.4228)
        ->  thymus (FOXN1, 1.4533)  ->  lymphoid_adaptive (PAX5, 1.4892)

SIGN validation vs CITED embryology [L]: hematopoiesis is the EARLIEST blood program (yolk-sac / AGM /
fetal-liver HSC emergence precedes lymphoid organogenesis) and the ADAPTIVE lymphoid compartment
(PAX5-driven mature B lineage, affinity-selected memory) matures LATEST (largely peri-/post-natal).
The kernel places exactly these two at the endpoints. (The spleen<->thymus middle pair sits within
measurement and is not independently anchored -- stated honestly, not claimed.)              [V] order

GRADES (C3): order shape [V]; endpoint sign [L] (cited embryology); fine middle ranking [O] (not anchored).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal

# cited developmental anchoring: which compartment is earliest / latest (sign only)
EARLIEST = "bone_marrow_hematopoiesis"   # blood program emerges first (yolk-sac/AGM/fetal-liver)
LATEST   = "lymphoid_adaptive"           # affinity-selected memory matures last (peri/post-natal)

def t3_lineage_order(gammas):
    rows = [dict(organ=k, gamma=round(v, 4), functional_spinodal=round(spinodal(v), 6)) for k, v in gammas.items()]
    order = [r["organ"] for r in sorted(rows, key=lambda r: r["gamma"])]
    endpoints_ok = (order[0] == EARLIEST and order[-1] == LATEST)
    return dict(target="T3",
                claim="developmental order = ascending gamma (lower threshold emerges earlier)",
                order_ascending=order, rows=sorted(rows, key=lambda r: r["gamma"]),
                cited_earliest=EARLIEST, cited_latest=LATEST,
                endpoints_match_embryology=bool(endpoints_ok),
                middle_pair_grade="[O] spleen<->thymus ordering within measurement, not independently anchored",
                all_pass=bool(endpoints_ok), grade="[V] order / [L] endpoint sign")

def run(gammas):
    return dict(T3=t3_lineage_order(gammas))

if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis":1.3225,"spleen":1.4228,"thymus":1.4533,"lymphoid_adaptive":1.4892}
    print(json.dumps(run(G), ensure_ascii=False, indent=2))
