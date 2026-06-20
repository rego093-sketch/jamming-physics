#!/usr/bin/env python3
# =============================================================================
#  dna_interpreter.py -- mechanical A4 interpreter (no hand-labels, no comments
#                        deciding roles). Reads the SEVERAL GLOBAL VARIABLES that
#                        the A4 arrangement exposes, straight from sequence.
# -----------------------------------------------------------------------------
#  Faithful to "A Deterministic Two-Layer Interpretation of DNA" (Lee, v11).
#  The whitepaper's thesis: the genome encodes STRUCTURE/POSITION (Layer 1,
#  mechanically readable) while QUANTITY/SETTING/SIGN lives at runtime (Layer 2,
#  NOT sequence-derivable). This engine therefore reads every ADMISSIBLE Layer-1
#  global variable mechanically and EXPLICITLY flags Layer-2 quantities instead
#  of hand-assigning them (which earlier plant scripts did via comment strings).
#
#  GLOBAL VARIABLES read from A4 (all admissible under Article IV):
#   [MATERIAL]   gamma = -mean(NN stacking dG, SantaLucia 1998)  (interfacial
#                tension / stiffness of the condensate), GC, CpG density,
#                AT-run(>=6) fraction, and the stiffness shell-class.
#   [COORDINATE] the A4 arrangement (run_key): which SHELL (class, mean_z, span)
#                the element sits in, the NEAREST ANCHOR (kind, strength=stiffness
#                contrast, distance), motors/loops if annotated, and the 3D HELIX
#                coordinate (rise 3.4 A/bp, twist 34.29 deg/bp -> helical phase).
#   [SWITCH]     the R19 double-well derived FROM gamma: spinodal threshold
#                (2/3sqrt3) gamma^1.5, barrier gamma^2/4 -- the element's own
#                bistable threshold, sequence-set.
#   [LAYER-2]    flagged, never assigned from sequence: the brake/accelerator
#                SIGN, the runtime fill phi, the cascade role.
#
#  DETERMINISM: pure arithmetic + the locked A4 pipeline; bit-for-bit.
# =============================================================================
import os, sys, math
import numpy as np

# the canonical A4 pipeline (Section 3 of the whitepaper). Vendored next to this
# file so the kit runs standalone; falls back to the full bundle if present.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path: sys.path.insert(0, _HERE)
try:
    import key_pipeline_full as K
except ImportError:
    _FW = "/home/claude/dna_study/dna_site_v1_7_deliverable/repro/dna/code"
    if _FW not in sys.path: sys.path.insert(0, _FW)
    import key_pipeline_full as K

# ---- LOCK: locked physical constants (changing any defines a new version) ----
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}              # SantaLucia 1998
RISE_A   = 3.4            # angstrom per base pair (B-DNA)
TWIST_DEG = 34.29        # degrees per base pair (~10.5 bp/turn)

# ----------------------------- MATERIAL reads --------------------------------
def gamma(seq):
    """Interfacial tension / stiffness = -mean(NN stacking dG). Strand-symmetric."""
    s = seq.upper()
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(np.mean(v)) if v else float("nan")

def gc_frac(seq):
    c = [x for x in seq.upper() if x in "ACGT"]
    return sum(1 for x in c if x in "GC")/len(c) if c else float("nan")

def cpg_density(seq):
    s = seq.upper(); n = sum(1 for i in range(len(s)-1) if s[i:i+2]=="CG")
    return n/max(1, len(s)-1)

def atrun_frac(seq, k=6):
    s = seq.upper(); n = len(s); hit = 0
    if n >= k:
        for i in range(n-k+1):
            w = s[i:i+k]
            if w.count("A")==k or w.count("T")==k: hit += 1
    return hit/max(1, n-k+1)

def parse_ft_motors(ft_text):
    """Extract motors (gene TSS) from an NCBI region feature table (rettype=ft).
       Coordinates are region-relative (1-based from the fetched window start). The
       first coordinate of a 'gene' line is its 5' end = TSS; start<=end is '+'.
       The '<'/'>' truncation marks are stripped. This upgrades the COORDINATE read
       from anchors-only to real motors+loops, so anchor_loops becomes a genuine
       count of co-anchored genes and helical contact can be cross-checked."""
    motors, mid = [], 0
    for line in ft_text.splitlines():
        p = line.split('\t')
        if len(p) >= 3 and p[2] == 'gene':
            try:
                s = int(p[0].lstrip('<>')); e = int(p[1].lstrip('<>'))
            except ValueError:
                continue
            motors.append(dict(id=mid, pos=int(s), strand=('+' if s <= e else '-')))
            mid += 1
    return motors

# ----------------------------- SWITCH reads (R19) ----------------------------
def switch_params(g):
    """The element's own R19 bistable threshold, derived from gamma alone."""
    spinodal = (2.0/(3.0*math.sqrt(3.0))) * g**1.5      # |h_sp|: threshold scale
    barrier  = 0.25 * g**2                               # gamma^2/4: barrier height
    return dict(spinodal=spinodal, barrier=barrier,
                rest_state_magnitude=math.sqrt(g))       # |s| of each basin

# ----------------------------- COORDINATE reads ------------------------------
def helix_coord(bp_from_reference):
    """3D helix offset of a position RELATIVE TO A REFERENCE point (e.g. its anchor).
       The absolute phase from an arbitrary window edge is meaningless; the
       physically meaningful quantity is the phase BETWEEN two loci -- whether a
       motor (TSS) and its anchor sit on the SAME rotational face of the helix
       (face ~0 or ~1) and so can contact, or OPPOSITE faces (~0.5)."""
    twist = (abs(bp_from_reference) * TWIST_DEG) % 360.0
    face = twist/360.0
    same_face = min(face, 1.0-face) < 0.17      # within ~60 deg of aligned
    return dict(rise_to_anchor_nm=round(bp_from_reference*RISE_A/10.0, 1),
                anchor_twist_deg=round(twist, 1),
                anchor_helical_face=round(face, 3),
                contact_competent=bool(same_face))

def locate_in_A4(A4, offset):
    """Place an element offset within the A4 arrangement: its shell + nearest anchor,
       including the 3D helical phase of the element relative to that anchor."""
    lab = {0:"soft", 1:"mid", 2:"stiff"}
    shell_idx, shell = None, None
    for i, s in enumerate(A4["shells"]):
        if s[0] <= offset < s[1]:
            shell_idx, shell = i, s; break
    if shell is None:                       # offset at the far edge
        shell_idx, shell = len(A4["shells"])-1, A4["shells"][-1]
    ap = np.array([a["pos"] for a in A4["anchors"]])
    j = int(np.argmin(np.abs(ap - offset)))
    an = A4["anchors"][j]
    n_loops = sum(1 for lp in A4.get("loops", []) if lp["anchor_id"] == an["id"])
    out = dict(shell_index=shell_idx,
               shell_class=lab[shell[2]], shell_mean_z=round(shell[3], 3),
               shell_span_bp=int(shell[1]-shell[0]),
               nearest_anchor_id=an["id"], anchor_kind=an["kind"],
               anchor_strength=round(float(an["strength"]), 3),
               anchor_distance_bp=int(abs(an["pos"]-offset)),
               anchor_loops=n_loops)
    out.update(helix_coord(an["pos"]-offset))     # 3D phase relative to the anchor
    return out

# ----------------------------- the full interpretation -----------------------
def interpret_element(region_seq, elem_offset, prom_seq, A4=None,
                      region_terciles=None, gff=None, seqid=None, motors=None):
    """Mechanical Layer-1 interpretation of one element (e.g. a promoter switch).
       region_seq : the wide genomic window the element lives in (for A4 coordinates)
       elem_offset: the element's start offset within region_seq (e.g. the TSS)
       prom_seq   : the element sequence itself (the promoter window) for MATERIAL
       motors     : optional list of motor dicts (region-relative TSS) from a feature
                    table -> real loops, enriching the coordinate read.
       Everything returned is sequence-derived; Layer-2 is flagged, not assigned."""
    if A4 is None:
        A4 = K.run_key(region_seq, gff=gff, seqid=seqid)
    if motors:                                   # build real loops from annotation
        A4 = dict(A4); A4["motors"] = motors
        A4["loops"] = K.build_loops(motors, A4["anchors"], A4["lock"]["loop_k"])
    g = gamma(prom_seq)
    material = dict(gamma=round(g, 4), gc=round(gc_frac(prom_seq), 4),
                    cpg_density=round(cpg_density(prom_seq), 5),
                    atrun_frac=round(atrun_frac(prom_seq), 5))
    switch = {k: round(v, 4) for k, v in switch_params(g).items()}
    coordinate = locate_in_A4(A4, elem_offset)       # includes anchor-relative 3D phase
    coordinate["region_motor_count"] = len(A4.get("motors", []))
    layer2 = dict(
        brake_or_accelerator="LAYER-2 (cascade sign; not sequence-derivable)",
        runtime_fill_phi="LAYER-2 (set at runtime)",
        cascade_role="LAYER-2 (wiring; requires network context)")
    return dict(material=material, switch=switch, coordinate=coordinate,
                layer2_flags=layer2)

def mechanical_summary(interp):
    """One-line MECHANICAL reading -- only what sequence licenses (no role label)."""
    m, c, s = interp["material"], interp["coordinate"], interp["switch"]
    return (f"gamma={m['gamma']} ({c['shell_class']}-shell, mean_z={c['shell_mean_z']}); "
            f"anchor d={c['anchor_distance_bp']}bp str={c['anchor_strength']} "
            f"face={c['anchor_helical_face']}{'(contact)' if c['contact_competent'] else ''}; "
            f"R19 threshold={s['spinodal']}; sign=LAYER-2")

if __name__ == "__main__":
    # smoke test on a synthetic region
    import random; random.seed(7)
    reg = "".join(random.choice("ACGT") for _ in range(60000))
    prom = reg[30000:32500]
    interp = interpret_element(reg, 30000, prom)
    import json; print(json.dumps(interp, indent=2))
    print("\nMECHANICAL:", mechanical_summary(interp))
