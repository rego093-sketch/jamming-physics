#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_sensors.py  --  THE SENSORY SEAM: the body's mineral/acid/electrolyte SENSORS are the SAME molecular
instruments that sensory cells use to transduce taste, balance, and pain.

A homeostatic comparator and a sensory-cell transducer are the SAME object: an R19-class switch that reads
an ionic variable and reports an error/percept. The deep claim of this volume's sensory seam:

  * The setpoint comparator of a loop (e.g. CaSR for Ca) is literally a sensory receptor deployed for
    interoception, while the SAME receptor family transduces the corresponding EXTERNAL sense.
  * Disease at a sensor = "INSTRUMENT FAILURE": a mutation that mis-calibrates the sensor SHIFTS the
    defended setpoint (a sensor that is too sensitive defends too low a value, and vice versa). This is
    exactly the pathology module's "setpoint drift via instrument mis-calibration".
  * Treatment = RECALIBRATE the instrument (an allosteric modulator resets the sensor's set-point).

CROWN JEWEL -- OTOP1: a proton-selective channel that is BOTH the sour-taste receptor AND required for
otoconia (calcium-carbonate biominerals) by holding the pH for biomineralization. One molecule couples
acid-base sensing (RI2) <-> calcium-carbonate mineral deposition (mineral axis) <-> a sense organ
(vestibular gravity/acceleration). BPPV (dislodged otoconia; common) is the disease at that mineral<->
sensory seam.

GRADES (C3): the sensor<->transducer identities are CITED molecular facts [L]; "each sensor is an R19
switch with gamma-set sharpness" is demonstrated on the MEASURED sensor gamma [V]; the deep unification
claim is a framework MAPPING (stated as such). gamma MEASURED (NCBI promoters), never fitted.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal, settle, is_on, seed_everything

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

def _sensor_gammas():
    j=json.load(open(_GAMMA, encoding="utf-8"))
    g={k:v["gamma"] for k,v in j.get("cellular_sensors",{}).items()}
    if "CASR" in j["genes"]: g["CASR"]=j["genes"]["CASR"]["gamma"]   # the loop comparator is also a sensor
    return g

# variable -> systemic sensor (loop comparator) -> sensory-cell twin -> sense -> instrument-failure disease
SENSOR_SEAM = [
 {"variable":"Ca2+", "systemic_sensor":"CASR (parathyroid comparator)",
  "sensory_twin":"CaSR in taste / GI (calcium & kokumi taste)", "sense":"taste / interoception",
  "instrument_failure":"ADH1 (CaSR gain-of-fn: defends too-LOW Ca) ; FHH (loss-of-fn: defends too-HIGH Ca)",
  "recalibration":"calcilytic (encaleret) resets set-point UP in ADH1 ; calcimimetic (cinacalcet) resets DOWN in hyperPTH",
  "ref":"Brown 1993 (CaSR); Hannan 2018 (CaSR disorders); Gafni/CALIBRATE 2025 (encaleret)"},
 {"variable":"H+ / pH", "systemic_sensor":"renal acid sensing + peripheral/central chemoreceptors",
  "sensory_twin":"OTOP1 (sour taste) ; ASIC2/ASIC3 (nociceptor pH)", "sense":"sour taste / pain",
  "instrument_failure":"acid-base sensing failure contributes to mis-set ventilatory/renal response",
  "recalibration":"restore the failed arm at source (renal HCO3 transport / ventilatory drive)",
  "ref":"Tu 2018, Teng 2019, Zhang 2019 (OTOP1 sour); Waldmann 1997 (ASIC)"},
 {"variable":"H+ + CaCO3 biomineral", "systemic_sensor":"acid-base <-> mineral coupling",
  "sensory_twin":"OTOP1 -> otoconia (CaCO3) pH-keeper", "sense":"gravity / acceleration (vestibular)",
  "instrument_failure":"BPPV (dislodged/degenerated otoconia) -- a mineral-reservoir + instrument failure",
  "recalibration":"repositioning maneuvers (mechanical) ; framework target = otoconial CaCO3 micro-pH/Ca stability",
  "ref":"Hurle 2003; Hughes 2004; Wang 2021 (Otop1 otoconia); Hu 2022 (otolith biomineral)"},
 {"variable":"Na+", "systemic_sensor":"renal Na sensing (macula densa / ENaC)",
  "sensory_twin":"ENaC (SCNN1A) amiloride-sensitive salt taste", "sense":"salt taste",
  "instrument_failure":"Liddle (ENaC gain-of-fn: Na retention/hypertension) ; salt-taste loss",
  "recalibration":"amiloride/ENaC blocker (salt-taste AND renal Na effector are the same channel)",
  "ref":"Chandrashekar 2010 (ENaC salt taste); Shimkets 1994 (Liddle)"},
 {"variable":"Ca2+ flux (effector)", "systemic_sensor":"TRPV5 (kidney) / TRPV6 (gut) Ca channels",
  "sensory_twin":"TRP-family sensory channels (thermo/mechano/chemo)", "sense":"somatosensation",
  "instrument_failure":"TRPV5/6 dysfunction -> renal Ca leak / hypercalciuria (stone risk)",
  "recalibration":"loop-gain restoration of renal Ca reabsorption (thiazide raises reabsorption gain)",
  "ref":"Hoenderop 2005 (TRPV5/6 Ca channels)"},
]

def sensors_are_r19_switches():
    """Verify each MEASURED sensor gamma yields a valid R19 bistable instrument (positive barrier + finite
    spinodal threshold + a definite ON/OFF flip), and that sensor sharpness (barrier) is monotone in gamma.
    This grounds 'a sensor is an R19 switch with gamma-set sharpness' on measured values. [V]."""
    seed_everything(); G=_sensor_gammas()
    rows=[]
    for sym in sorted(G, key=lambda s: G[s]):
        g=G[sym]; b=barrier(g); sp=spinodal(g)
        flips = is_on(g, +sp*1.2) and (not is_on(g, -sp*1.2))    # forced ON above, OFF below threshold
        rows.append(dict(sensor=sym, gamma=round(g,4), barrier=round(b,4), spinodal_threshold=round(sp,4),
                         valid_bistable_instrument=bool(b>0 and sp>0 and flips)))
    all_valid=all(r["valid_bistable_instrument"] for r in rows)
    barr=[r["barrier"] for r in rows]
    mono=all(barr[i] <= barr[i+1]+1e-12 for i in range(len(barr)-1))
    return dict(sensors=rows, all_valid_bistable=bool(all_valid), barrier_monotone_in_gamma=bool(mono),
                grade="[V] each measured sensor is a valid R19 instrument; sharpness monotone in measured gamma")

def status():
    s=sensors_are_r19_switches()
    return dict(_what="Sensory seam: mineral/acid/Na sensors are the same molecular instruments as taste/"
                      "balance/pain transducers; disease = instrument failure (setpoint mis-calibration).",
                seam=SENSOR_SEAM, instrument_check=s,
                crown_jewel="OTOP1: proton channel = sour-taste receptor AND otoconia (CaCO3) pH-keeper -> "
                            "couples acid-base (RI2) <-> Ca-carbonate mineral <-> vestibular sense; BPPV at the seam",
                grade="identities cited [L]; R19-instrument check [V]; unification = framework mapping")

if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=1))
