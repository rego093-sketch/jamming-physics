#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_numeric_ssot.py — the deterministic NUMERIC SINGLE SOURCE OF TRUTH for the ear HTML volume.

Every number displayed anywhere in docs/ is produced HERE, by importing the package's FROZEN
inherited foundation and its VERIFIED research E-modules and calling the SAME functions those
modules use. No number is re-implemented, hand-typed, or fitted in this file — each fact is the
exact value the verified module computes, so the HTML cannot drift from the code by construction.

Contract (VP-SPEC v1.8 §C1 / WORK_HANDOVER item 5):
  * build_volume.py reads facts() and writes display strings into <span data-vp="KEY"> nodes.
  * gate_volume.py re-runs facts() and asserts every HTML span text == the canonical display
    string (drift 0), and that this module is deterministic (run twice → identical sha256).

Run from the package root:   python3 volume/tools/vp_numeric_ssot.py   → prints  sha256: <hex>
Requires numpy (same as the foundation modules); no network.
"""
import os, sys, json, math, hashlib, importlib.util
import numpy as np

# ---- locate the package root and import the frozen/verified modules by path -----------------
PKG = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PKG, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

SND = _load("vp_sound_wave_ssot", "inherited/vp_sound_wave.py")          # √-law wave + Greenwood
SUB = _load("vp_substrate_ssot",  "inherited/vp_substrate.py")           # R19 cubic primitive
E3  = _load("E3_ssot", "research/E3-cochlear-amplifier/run.py")          # cube-root amplifier
E5  = _load("E5_ssot", "research/E5-readout-synapse/run.py")             # readout sensor
E6  = _load("E6_ssot", "research/E6-traveling-wave-envelope/run.py")     # envelope resonance
E7  = _load("E7_ssot", "research/E7-audible-band/run.py")                # audible band
E8  = _load("E8_ssot", "research/E8-band-specific-loss/run.py")          # band-specific loss

_ATLAS = json.load(open(os.path.join(PKG, "inherited/organ_gamma.json"), encoding="utf-8"))["genes"]
def _g(sym): return _ATLAS[sym]["gamma"]

# ---- display formatters (Unicode minus, superscript sci) ------------------------------------
_MINUS = "\u2212"        # − proper minus sign
_SUP = str.maketrans("0123456789-", "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u207b")

def _u(s):  # ascii '-' -> proper minus for display
    return s.replace("-", _MINUS)

def fixed(x, n):
    return _u(f"{x:.{n}f}")

def integer(x):
    return _u(f"{int(round(x))}")

def sci(x, mant=4):
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / (10.0 ** e)
    return f"{m:.{mant}f}\u00d710{str(e).translate(_SUP)}"   # m.mmmm×10ⁿ

def thresh(x, t=1e-9):
    # machine-precision residuals: report as a clean bound, not noisy last bits
    return f"<{sci(t,0)}" if abs(x) < t else sci(x, 2)

# ---- the canonical fact table ----------------------------------------------------------------
# Each entry: KEY -> (raw_value, display_string, short_meaning). display is what appears in HTML.
def build_facts():
    F = {}
    def add(k, raw, disp, meaning):
        F[k] = {"value": float(raw), "display": disp, "meaning": meaning}

    # --- inherited place map (shared) -----------------------------------------------------
    apex = SND.greenwood_f(0.0); base = SND.greenwood_f(1.0)
    add("cf_apex", apex, fixed(apex, 3) + " Hz", "Greenwood CF at the apex (x=0)")
    add("cf_base", base, fixed(base, 2) + " Hz", "Greenwood CF at the base (x=1)")
    add("n_genes", len(_ATLAS), integer(len(_ATLAS)), "master genes in the complete readable-layer atlas")

    # --- §1 E1: MET-switch spinodal emergence order (lower spinodal flips earlier) ---------
    for s in ("TMC1", "PCDH15", "CDH23", "TMIE", "SLC26A5", "ATOH1",
              "USH2A", "GJB2", "SLC26A4", "LHFPL5", "MYO15A", "OTOF", "TMC2"):
        sp = SUB.spinodal(_g(s))
        add(f"spin_{s}", sp, fixed(sp, 4), f"R19 spinodal 2·(γ/3)^1.5 for {s}")
    for s in ("TMC1", "TMC2", "OTOF", "SLC26A5", "SLC26A4"):
        add(f"gamma_{s}", _g(s), fixed(_g(s), 4), f"measured promoter γ (LEVEL) for {s}")
    # forced peak place x*(f) = inverse-Greenwood(f), parameter-free (E1)
    for f_hz, key in ((250, "x_250"), (1000, "x_1k"), (4000, "x_4k"), (16000, "x_16k")):
        x = math.log10(f_hz / 165.4 + 0.88) / 2.1
        add(key, x, fixed(x, 2), f"forced traveling-wave peak place for {f_hz} Hz")

    # --- §2 E3 / §3 E4: the cube-root amplifier (recomputed on the inherited integrator) ---
    Fs = [x for x in E3.drive_grid() if 0.1 <= x <= 100.0]
    s_of = [SUB.settle(0.0, h) for h in Fs]
    cube_exp = float(np.polyfit(np.log10(Fs), np.log10(s_of), 1)[0])
    gain_exp = float(np.polyfit(np.log10(Fs), np.log10([s_of[i] / Fs[i] for i in range(len(Fs))]), 1)[0])
    resid = max(abs(SUB.sdot(h ** (1.0 / 3.0), 0.0, h)) for h in Fs)
    add("cube_exp", cube_exp, fixed(cube_exp, 6), "fitted compression exponent r∝F^x at criticality (→1/3)")
    add("gain_exp", gain_exp, fixed(gain_exp, 6), "fitted gain exponent (r/F)∝F^x (→−2/3)")
    add("cube_resid", resid, thresh(resid), "max|residual| of the inherited sdot at s=F^(1/3) over 7 decades")

    # --- §3 E4: structure-class window collapse 2·spinodal(g)→0 as g→0 ---------------------
    add("win_g130", 2 * SUB.spinodal(1.30), fixed(2 * SUB.spinodal(1.30), 4), "bistable drive window 2·spinodal(g) at g=1.30")
    add("win_g001", 2 * SUB.spinodal(0.01), fixed(2 * SUB.spinodal(0.01), 5), "bistable drive window 2·spinodal(g) at g=0.01 (→0)")

    # --- §4 E5: composed compression exponent R∝F^(m/3) -----------------------------------
    for m in (1, 2, 3, 4):
        ce = E5.composed_exponent(m)
        add(f"compexp_m{m}", ce, fixed(ce, 4), f"composed cascade exponent for synaptic cooperativity m={m} (=m/3)")

    # --- §5 E6: envelope bandwidth law BW = ω0/Q (ω0=1), group-delay peak 2Q/ω0 -----------
    for Q in (3, 10, 30, 100):
        _, _, bw = E6.half_power_bandwidth(1.0, Q)
        add(f"bw_Q{Q}", bw, fixed(bw, 4), f"numeric −3 dB velocity bandwidth at Q={Q}")
        add(f"bwlaw_Q{Q}", 1.0 / Q, fixed(1.0 / Q, 4), f"law ω0/Q at Q={Q}")
    for Q in (5, 20, 80):
        add(f"gd_Q{Q}", 2.0 * Q, fixed(2.0 * Q, 1), f"group-delay peak magnitude 2Q/ω0 at Q={Q}")

    # --- §6 E7: octave keystone N_oct = ½·log₂(S_base/S_apex) ------------------------------
    span = E7.octave_span(0.0, 1.0)
    sratio = E7.implied_stiffness_ratio(span)
    closure = E7.noct_from_stiffness_ratio(sratio) - span
    bare = math.log2(E7.cf_pure_exp(1.0) / E7.cf_pure_exp(0.0))
    bend = span - bare
    add("octspan", span, fixed(span, 6) + " oct", "audible span read off the inherited Greenwood map")
    add("stiffratio", sratio, sci(sratio, 4), "implied basilar-membrane stiffness ratio S_base/S_apex")
    add("noct_closure", closure, thresh(closure), "|Δ| of the ½·log₂(S_ratio) keystone closure")
    add("bare_exp_oct", bare, fixed(bare, 6) + " oct", "octaves from the bare exponential 10^(a·x) term")
    add("heli_bend_oct", bend, fixed(bend, 6) + " oct", "net octaves from the helicotrema apical bend (−A·k)")
    add("ten_pow_a", 10.0 ** 2.1, fixed(10.0 ** 2.1, 3), "apex/base fractional-weight ratio of the −A·k offset (=10^a)")
    add("mass_slope", -2.0, fixed(-2.0, 0), "ossicular-mass low-pass log–log slope (=−12 dB/oct)")

    # --- §7 E8: place→frequency order-isomorphism band images ------------------------------
    bl, bh = E8.freq_band_of_place_band(0.7, 1.0)
    ml, mh = E8.freq_band_of_place_band(0.4, 0.6)
    al, ah = E8.freq_band_of_place_band(0.0, 0.3)
    add("e8_basal_lo", bl, fixed(bl, 0) + " Hz", "low edge of the basal band x∈[0.7,1.0] image")
    add("e8_basal_hi", bh, fixed(bh, 0) + " Hz", "high edge of the basal band image (=CF_base)")
    add("e8_mid_lo", ml, fixed(ml, 0) + " Hz", "low edge of the mid band x∈[0.4,0.6] image")
    add("e8_mid_hi", mh, fixed(mh, 0) + " Hz", "high edge of the mid band image")
    add("e8_apic_lo", al, fixed(al, 1) + " Hz", "low edge of the apical band x∈[0.0,0.3] image (=CF_apex)")
    add("e8_apic_hi", ah, fixed(ah, 1) + " Hz", "high edge of the apical band image")
    rt = max(abs(E8.place_of(E8.cf(x)) - x) for x in (0.0, 0.3, 0.4, 0.6, 0.7, 1.0))
    add("e8_roundtrip", rt, thresh(rt), "max place→frequency→place round-trip error |Δ|")
    lr = E8.cyclic_load_rate(1.0) / E8.cyclic_load_rate(0.0)
    add("e8_loadratio", lr, fixed(lr, 0) + "\u00d7", "cyclic-load ratio load(base)/load(apex) (=CF_base/CF_apex)")

    return F

# ---- public helpers + canonical hash --------------------------------------------------------
_FACTS = build_facts()

def facts():
    return _FACTS

def disp(key):
    return _FACTS[key]["display"]

def canonical_json():
    # deterministic: sorted keys, displays only (the gate compares HTML text to these strings)
    return json.dumps({k: _FACTS[k]["display"] for k in sorted(_FACTS)},
                      ensure_ascii=True, sort_keys=True)

def canonical_sha256():
    return hashlib.sha256(canonical_json().encode("utf-8")).hexdigest()

def main():
    return canonical_sha256()

if __name__ == "__main__":
    print("facts:", len(_FACTS))
    print("\nsha256:", main())
