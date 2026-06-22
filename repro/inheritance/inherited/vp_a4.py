#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_a4.py  --  VENDORED A4 coordinate/structure channel (DO NOT re-derive).

The DNA engine reads a sequence MECHANICALLY into four channels. This kit already vendors the MATERIAL +
SWITCH channels (gamma, R19) in vp_substrate.py. This module vendors the **A4 COORDINATE channel**: the
structural arrangement a sequence exposes -- the stiffness-signal compartment SHELLS (soft/mid/stiff), the
shell-boundary ANCHORS, the motor->anchor LOOPS, and the 3D HELICAL PHASE of an element relative to its
anchor (whether it sits on the same rotational face and can CONTACT). Direct transcription of the
whitepaper's KEY pipeline (Section 3) + interpreter coordinate reads. Single source; report bugs to the
DNA engine owner, do not rewrite the math.

WHY A4 MATTERS HERE.  gamma is the SET, fixed in the genome -- the environment cannot rewrite it. The
environment writes information through the *other* channels: it reorganises the A4 ARRANGEMENT (which
compartment shell a region sits in, which anchors are looped/contacted) WITHOUT changing the sequence, and
a small RNA acts by sequence COMPLEMENTARITY -- it specifies an A4 COORDINATE (a position/anchor) and
deposits a drive there. So for RNA / environmental inheritance the A4 channel is central, not optional.

Grades (VP-SPEC C3): [F] forced / [V] simulation-verified / [O] open / [L] calibration.
"""
import numpy as np
import math

# ---- LOCK: SantaLucia 1998 NN dG37 + B-DNA helical constants (changing any defines a new version) ----
NN = {"AA": -1.00, "TT": -1.00, "AT": -0.88, "TA": -0.58, "CA": -1.45, "TG": -1.45,
      "GT": -1.44, "AC": -1.44, "CT": -1.28, "AG": -1.28, "GA": -1.30, "TC": -1.30,
      "CG": -2.17, "GC": -2.24, "GG": -1.84, "CC": -1.84}
RISE_A = 3.4             # angstrom per base pair (B-DNA)
TWIST_DEG = 34.29        # degrees per base pair (~10.5 bp/turn)

LOCK = dict(W=2000, step=500, w_gc=1.0, w_cpg=0.5, w_at=-0.5,
            smooth_radius=2, min_shell_bp=5000, loop_k=2, eps=1e-9)


# ----------------------------- MATERIAL reads (gamma channel) ----------------------------
def gamma(seq):
    s = seq.upper()
    v = [-NN[s[i:i + 2]] for i in range(len(s) - 1) if s[i:i + 2] in NN]
    return float(np.mean(v)) if v else float("nan")

def gc_frac(seq):
    c = [x for x in seq.upper() if x in "ACGT"]
    return sum(1 for x in c if x in "GC") / len(c) if c else float("nan")

def cpg_density(seq):
    s = seq.upper(); n = sum(1 for i in range(len(s) - 1) if s[i:i + 2] == "CG")
    return n / max(1, len(s) - 1)

def cpg_oe(seq):
    """CpG observed/expected (Gardiner-Garden & Frommer) -- the methylation-island signal, ~orthogonal to GC."""
    s = seq.upper(); L = len(s); nC = s.count("C"); nG = s.count("G"); nCpG = s.count("CG")
    return (nCpG * L) / (nC * nG) if nC and nG else 0.0

def atrun_frac(seq, k=6):
    s = seq.upper(); n = len(s); hit = 0
    if n >= k:
        for i in range(n - k + 1):
            w = s[i:i + k]
            if w.count("A") == k or w.count("T") == k:
                hit += 1
    return hit / max(1, n - k + 1)


# ----------------------------- SWITCH reads (R19) ----------------------------
def switch_params(g):
    spinodal = (2.0 / (3.0 * math.sqrt(3.0))) * g ** 1.5
    barrier = 0.25 * g ** 2
    return dict(spinodal=spinodal, barrier=barrier, rest_state_magnitude=math.sqrt(g))


# ----------------------------- A4 KEY pipeline (Section 3) -------------------
def windowed_observables(seq, W, step):
    a = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
    n = len(a)
    A, C, G, T = 65, 67, 71, 84
    is_a, is_c, is_g, is_t = (a == A), (a == C), (a == G), (a == T)
    is_acgt = is_a | is_c | is_g | is_t
    is_gc = is_g | is_c
    cg = np.zeros(n, dtype=bool); cg[:-1] = is_c[:-1] & is_g[1:]
    at6 = np.zeros(n, dtype=bool)
    if n >= 6:
        ca = np.concatenate([[0], np.cumsum(is_a)]); ct = np.concatenate([[0], np.cumsum(is_t)])
        run_a = (ca[6:] - ca[:-6]) == 6; run_t = (ct[6:] - ct[:-6]) == 6
        at6[:len(run_a)] = run_a | run_t
    cum_gc = np.concatenate([[0], np.cumsum(is_gc)]); cum_ac = np.concatenate([[0], np.cumsum(is_acgt)])
    cum_cg = np.concatenate([[0], np.cumsum(cg)]); cum_a6 = np.concatenate([[0], np.cumsum(at6)])
    starts = np.arange(0, max(1, n - W + 1), step); ends = starts + W
    denom = cum_ac[ends] - cum_ac[starts]; keep = denom > 0
    starts, ends, denom = starts[keep], ends[keep], denom[keep]
    gc = (cum_gc[ends] - cum_gc[starts]) / denom
    cpg = (cum_cg[ends] - cum_cg[starts]) / max(1, W - 1)
    a6f = (cum_a6[ends] - cum_a6[starts]) / max(1, W - 5)
    centers = starts + W // 2
    return centers, gc, cpg, a6f

def stiffness_signal(gc, cpg, at6, lock=LOCK):
    return lock["w_gc"] * gc + lock["w_cpg"] * cpg + lock["w_at"] * at6

def robust_z(x, eps):
    m = np.median(x); d = np.median(np.abs(x - m))
    return (x - m) / (1.4826 * max(d, eps))

def smooth(z, radius):
    if radius <= 0 or len(z) == 0:
        return z
    pad = np.pad(z, radius, mode="edge"); ker = np.ones(2 * radius + 1) / (2 * radius + 1)
    return np.convolve(pad, ker, mode="valid")

def segment_shells(centers, z, L, min_shell_bp):
    n = len(z)
    if n == 0:
        return [[0, L, 1, 0.0]]
    q1, q2 = np.percentile(z, 33), np.percentile(z, 66)
    lab = np.where(z <= q1, 0, np.where(z <= q2, 1, 2))
    mids = [0] + [int((centers[i] + centers[i + 1]) // 2) for i in range(n - 1)] + [int(L)]
    shells, start = [], 0
    for i in range(1, n + 1):
        if i == n or lab[i] != lab[start]:
            shells.append([mids[start], mids[i], int(lab[start]), float(np.mean(z[start:i]))]); start = i
    changed = True
    while changed and len(shells) > 1:
        changed = False
        for i, sh in enumerate(shells):
            if sh[1] - sh[0] < min_shell_bp:
                if 0 < i < len(shells) - 1:
                    left, right = shells[i - 1], shells[i + 1]
                    tgt = i - 1 if abs(left[3] - sh[3]) <= abs(right[3] - sh[3]) else i + 1
                elif i > 0:
                    tgt = i - 1
                else:
                    tgt = i + 1
                ln_t = shells[tgt][1] - shells[tgt][0]; ln_s = sh[1] - sh[0]
                mean = (shells[tgt][3] * ln_t + sh[3] * ln_s) / max(1, ln_t + ln_s)
                if tgt == i - 1:
                    shells[i - 1] = [shells[i - 1][0], sh[1], shells[i - 1][2], mean]
                else:
                    shells[i + 1] = [sh[0], shells[i + 1][1], shells[i + 1][2], mean]
                del shells[i]; changed = True; break
    for sh in shells:
        sh[2] = 0 if sh[3] <= q1 else (1 if sh[3] <= q2 else 2)
    return shells

def build_anchors(shells, L):
    anchors = [dict(id=0, pos=0, kind="region_edge", strength=0.0)]; aid = 1
    for i in range(1, len(shells)):
        strength = abs(shells[i][3] - shells[i - 1][3])
        anchors.append(dict(id=aid, pos=int(shells[i][0]), kind="shell_boundary", strength=float(strength))); aid += 1
    anchors.append(dict(id=aid, pos=int(L), kind="region_edge", strength=0.0))
    return anchors

def build_loops(motors, anchors, k):
    loops, lid = [], 0
    apos = np.array([a["pos"] for a in anchors])
    for m in motors:
        d = np.abs(apos - m["pos"])
        for j in np.argsort(d)[:k]:
            loops.append(dict(id=lid, motor_id=m["id"], anchor_id=anchors[int(j)]["id"], d=int(d[int(j)]))); lid += 1
    return loops

def run_key(seq, motors=None, lock=LOCK):
    """Map a sequence to its A4 arrangement (shells, anchors, optional motors->loops). Deterministic."""
    L = len(seq)
    centers, gc, cpg, at6 = windowed_observables(seq, lock["W"], lock["step"])
    z = smooth(robust_z(stiffness_signal(gc, cpg, at6, lock), lock["eps"]), lock["smooth_radius"])
    shells = segment_shells(centers, z, L, lock["min_shell_bp"])
    anchors = build_anchors(shells, L)
    motors = motors or []
    loops = build_loops(motors, anchors, lock["loop_k"]) if motors else []
    return dict(length=L, shells=shells, anchors=anchors, motors=motors, loops=loops, lock=lock)


# ----------------------------- COORDINATE reads (A4) ------------------------------
def helix_coord(bp_from_reference):
    """3D helix offset relative to a reference (anchor): same rotational face (~0/1) => contact-competent."""
    twist = (abs(bp_from_reference) * TWIST_DEG) % 360.0
    face = twist / 360.0
    same_face = min(face, 1.0 - face) < 0.17
    return dict(rise_to_anchor_nm=round(bp_from_reference * RISE_A / 10.0, 1),
                anchor_twist_deg=round(twist, 1), anchor_helical_face=round(face, 3),
                contact_competent=bool(same_face))

def locate_in_A4(A4, offset):
    """Place an element offset within the A4 arrangement: its shell + nearest anchor + 3D helical phase."""
    lab = {0: "soft", 1: "mid", 2: "stiff"}
    shell_idx, shell = None, None
    for i, s in enumerate(A4["shells"]):
        if s[0] <= offset < s[1]:
            shell_idx, shell = i, s; break
    if shell is None:
        shell_idx, shell = len(A4["shells"]) - 1, A4["shells"][-1]
    ap = np.array([a["pos"] for a in A4["anchors"]])
    j = int(np.argmin(np.abs(ap - offset)))
    an = A4["anchors"][j]
    n_loops = sum(1 for lp in A4.get("loops", []) if lp["anchor_id"] == an["id"])
    out = dict(shell_index=shell_idx, shell_class=lab[shell[2]], shell_mean_z=round(shell[3], 3),
               shell_span_bp=int(shell[1] - shell[0]), nearest_anchor_id=an["id"], anchor_kind=an["kind"],
               anchor_strength=round(float(an["strength"]), 3), anchor_distance_bp=int(abs(an["pos"] - offset)),
               anchor_loops=n_loops)
    out.update(helix_coord(an["pos"] - offset))
    return out
