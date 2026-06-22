#!/usr/bin/env python3
"""KEY: map a DNA region (sequence + optional GFF annotation) to an A4 arrangement.

Deterministic. Requires only numpy and the standard library. This module is a
direct transcription of Section 3 of the whitepaper: it computes a windowed
stiffness signal, segments it into shells, places anchors at shell boundaries,
extracts motors (transcription starts) from annotation, and joins motors to
their nearest anchors as loops. It then runs admissibility gates.
"""
import numpy as np

# ---- LOCK: fixed parameters. Changing any of these defines a new version. ----
LOCK = dict(
    W=2000, step=500,                 # window length and step, in base pairs
    w_gc=1.0, w_cpg=0.5, w_at=-0.5,   # stiffness-signal weights (Section 3.2)
    smooth_radius=2,                  # moving-average half-width, in windows
    min_shell_bp=5000,                # merge shells shorter than this
    loop_k=2,                         # number of nearest anchors per motor
    eps=1e-9,
)


def read_fasta(path):
    seqs, name, buf = {}, None, []
    with open(path) as fh:
        for line in fh:
            if line.startswith('>'):
                if name is not None:
                    seqs[name] = ''.join(buf)
                name, buf = line[1:].split()[0], []
            else:
                buf.append(line.strip().upper())
    if name is not None:
        seqs[name] = ''.join(buf)
    return seqs


def windowed_observables(seq, W, step):
    """Return (centers, GC, CpG, AT6) per window using cumulative sums."""
    a = np.frombuffer(seq.encode('ascii'), dtype=np.uint8)
    n = len(a)
    A, C, G, T = 65, 67, 71, 84
    is_a, is_c, is_g, is_t = (a == A), (a == C), (a == G), (a == T)
    is_acgt = is_a | is_c | is_g | is_t
    is_gc = is_g | is_c
    cg = np.zeros(n, dtype=bool)            # CpG: C at i, G at i+1
    cg[:-1] = is_c[:-1] & is_g[1:]
    at6 = np.zeros(n, dtype=bool)           # start of a run of >=6 A or >=6 T
    if n >= 6:
        ca = np.concatenate([[0], np.cumsum(is_a)])
        ct = np.concatenate([[0], np.cumsum(is_t)])
        run_a = (ca[6:] - ca[:-6]) == 6
        run_t = (ct[6:] - ct[:-6]) == 6
        at6[:len(run_a)] = run_a | run_t
    cum_gc = np.concatenate([[0], np.cumsum(is_gc)])
    cum_ac = np.concatenate([[0], np.cumsum(is_acgt)])
    cum_cg = np.concatenate([[0], np.cumsum(cg)])
    cum_a6 = np.concatenate([[0], np.cumsum(at6)])
    starts = np.arange(0, max(1, n - W + 1), step)
    ends = starts + W
    denom = cum_ac[ends] - cum_ac[starts]
    keep = denom > 0
    starts, ends, denom = starts[keep], ends[keep], denom[keep]
    gc = (cum_gc[ends] - cum_gc[starts]) / denom
    cpg = (cum_cg[ends] - cum_cg[starts]) / max(1, W - 1)
    a6f = (cum_a6[ends] - cum_a6[starts]) / max(1, W - 5)
    centers = starts + W // 2
    return centers, gc, cpg, a6f


def stiffness_signal(gc, cpg, at6, lock=LOCK):
    return lock['w_gc'] * gc + lock['w_cpg'] * cpg + lock['w_at'] * at6


def robust_z(x, eps):
    m = np.median(x)
    d = np.median(np.abs(x - m))
    return (x - m) / (1.4826 * max(d, eps))


def smooth(z, radius):
    if radius <= 0 or len(z) == 0:
        return z
    pad = np.pad(z, radius, mode='edge')
    ker = np.ones(2 * radius + 1) / (2 * radius + 1)
    return np.convolve(pad, ker, mode='valid')


def segment_shells(centers, z, L, min_shell_bp):
    """Tercile-label, run-length into contiguous shells, merge short ones."""
    n = len(z)
    if n == 0:
        return [[0, L, 1, 0.0]]
    q1, q2 = np.percentile(z, 33), np.percentile(z, 66)
    lab = np.where(z <= q1, 0, np.where(z <= q2, 1, 2))
    mids = [0] + [int((centers[i] + centers[i + 1]) // 2) for i in range(n - 1)] + [int(L)]
    shells, start = [], 0
    for i in range(1, n + 1):
        if i == n or lab[i] != lab[start]:
            shells.append([mids[start], mids[i], int(lab[start]),
                           float(np.mean(z[start:i]))])
            start = i
    changed = True
    while changed and len(shells) > 1:
        changed = False
        for i, sh in enumerate(shells):
            if sh[1] - sh[0] < min_shell_bp:
                if i > 0 and i < len(shells) - 1:
                    left, right = shells[i - 1], shells[i + 1]
                    tgt = i - 1 if abs(left[3] - sh[3]) <= abs(right[3] - sh[3]) else i + 1
                elif i > 0:
                    tgt = i - 1
                else:
                    tgt = i + 1
                ln_t = shells[tgt][1] - shells[tgt][0]
                ln_s = sh[1] - sh[0]
                mean = (shells[tgt][3] * ln_t + sh[3] * ln_s) / max(1, ln_t + ln_s)
                if tgt == i - 1:
                    shells[i - 1] = [shells[i - 1][0], sh[1], shells[i - 1][2], mean]
                else:
                    shells[i + 1] = [sh[0], shells[i + 1][1], shells[i + 1][2], mean]
                del shells[i]
                changed = True
                break
    for sh in shells:                       # relabel by final mean after merging
        sh[2] = 0 if sh[3] <= q1 else (1 if sh[3] <= q2 else 2)
    return shells


def build_anchors(shells, L):
    anchors = [dict(id=0, pos=0, kind='region_edge', strength=0.0)]
    aid = 1
    for i in range(1, len(shells)):
        strength = abs(shells[i][3] - shells[i - 1][3])
        anchors.append(dict(id=aid, pos=int(shells[i][0]),
                            kind='shell_boundary', strength=float(strength)))
        aid += 1
    anchors.append(dict(id=aid, pos=int(L), kind='region_edge', strength=0.0))
    return anchors


def read_gff_tss(path, seqid, L):
    motors, mid = [], 0
    with open(path) as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            f = line.rstrip('\n').split('\t')
            if len(f) < 8 or f[0] != seqid or f[2] not in ('gene', 'mRNA', 'transcript'):
                continue
            start, end, strand = int(f[3]), int(f[4]), f[6]
            tss = start if strand == '+' else end
            if 0 <= tss <= L:
                motors.append(dict(id=mid, pos=int(tss), strand=strand))
                mid += 1
    return motors


def build_loops(motors, anchors, k):
    loops, lid = [], 0
    apos = np.array([a['pos'] for a in anchors])
    for m in motors:
        d = np.abs(apos - m['pos'])
        for j in np.argsort(d)[:k]:
            loops.append(dict(id=lid, motor_id=m['id'],
                              anchor_id=anchors[int(j)]['id'], d=int(d[int(j)])))
            lid += 1
    return loops


def gates(A4, L):
    sh, an = A4['shells'], A4['anchors']
    checks = [
        ('shells_cover_region', bool(sh) and sh[0][0] == 0 and sh[-1][1] == L),
        ('shells_contiguous', all(sh[i][1] == sh[i + 1][0] for i in range(len(sh) - 1))),
        ('anchors_in_range', all(0 <= a['pos'] <= L for a in an)),
        ('anchor_ids_unique', len({a['id'] for a in an}) == len(an)),
    ]
    return [(name, 'PASS' if ok else 'FAIL') for name, ok in checks]


def run_key(seq, gff=None, seqid=None, lock=LOCK):
    L = len(seq)
    centers, gc, cpg, at6 = windowed_observables(seq, lock['W'], lock['step'])
    z = smooth(robust_z(stiffness_signal(gc, cpg, at6, lock), lock['eps']),
               lock['smooth_radius'])
    shells = segment_shells(centers, z, L, lock['min_shell_bp'])
    motors = read_gff_tss(gff, seqid, L) if (gff and seqid) else []
    anchors = build_anchors(shells, L)
    loops = build_loops(motors, anchors, lock['loop_k']) if motors else []
    A4 = dict(length=L, shells=shells, anchors=anchors,
              motors=motors, loops=loops, lock=lock)
    A4['gates'] = gates(A4, L)
    return A4


if __name__ == '__main__':
    import glob
    kd = glob.glob('ecoli_full/ncbi_dataset/data/GCA_000005845.2*')[0]
    kf = glob.glob(kd + '/*genomic.fna')[0]
    kg = kd + '/genomic.gff'
    fa = read_fasta(kf)
    seqid = max(fa, key=lambda k: len(fa[k]))
    seq = fa[seqid]
    A4 = run_key(seq, gff=kg, seqid=seqid)
    print(f"seqid={seqid}  length={A4['length']:,} bp")
    print(f"shells={len(A4['shells'])}  anchors={len(A4['anchors'])}  "
          f"motors={len(A4['motors'])}  loops={len(A4['loops'])}")
    lab = {0: 'soft', 1: 'mid', 2: 'stiff'}
    print("first 6 shells [start, end, class, mean_z]:")
    for s in A4['shells'][:6]:
        print(f"  {s[0]:>9,} {s[1]:>9,}  {lab[s[2]]:<5} z={s[3]:+.2f}")
    print("gates:", A4['gates'])
    a = np.frombuffer(seq.encode('ascii'), dtype=np.uint8)
    isat = (a == 65) | (a == 84); isacgt = isat | (a == 67) | (a == 71)
    def atpct(s, e):
        sl = slice(s, e)
        return 100 * isat[sl].sum() / max(1, isacgt[sl].sum())
    soft = [atpct(s[0], s[1]) for s in A4['shells'] if s[2] == 0]
    stiff = [atpct(s[0], s[1]) for s in A4['shells'] if s[2] == 2]
    if soft and stiff:
        print(f"mean AT% soft = {np.mean(soft):.1f} ; stiff = {np.mean(stiff):.1f}")
